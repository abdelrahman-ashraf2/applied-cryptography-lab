"""Visualize AES modes while retaining ciphertext for complete decryption."""

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import asdict, dataclass
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image, ImageDraw, ImageFont


MODES = ("ECB", "CBC", "CFB", "OFB", "CTR")


@dataclass
class ModeRecord:
    mode: str
    ciphertext_bytes: int
    visual_file: str
    iv_or_nonce_hex: str | None
    round_trip_verified: bool


def _cipher(mode: str, key: bytes, *, decrypt: bool = False, iv_or_nonce: bytes | None = None):
    if mode == "ECB":
        return AES.new(key, AES.MODE_ECB), None
    if mode == "CBC":
        value = iv_or_nonce or secrets.token_bytes(AES.block_size)
        return AES.new(key, AES.MODE_CBC, iv=value), value
    if mode == "CFB":
        value = iv_or_nonce or secrets.token_bytes(AES.block_size)
        return AES.new(key, AES.MODE_CFB, iv=value, segment_size=128), value
    if mode == "OFB":
        value = iv_or_nonce or secrets.token_bytes(AES.block_size)
        return AES.new(key, AES.MODE_OFB, iv=value), value
    if mode == "CTR":
        value = iv_or_nonce or secrets.token_bytes(8)
        return AES.new(key, AES.MODE_CTR, nonce=value), value
    raise ValueError(f"Unsupported mode: {mode}")


def _encrypt(mode: str, plaintext: bytes, key: bytes) -> tuple[bytes, bytes | None]:
    cipher, parameter = _cipher(mode, key)
    prepared = pad(plaintext, AES.block_size) if mode in ("ECB", "CBC") else plaintext
    return cipher.encrypt(prepared), parameter


def _decrypt(mode: str, ciphertext: bytes, key: bytes, parameter: bytes | None) -> bytes:
    cipher, _ = _cipher(mode, key, decrypt=True, iv_or_nonce=parameter)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, AES.block_size) if mode in ("ECB", "CBC") else plaintext


def _visual_bytes(ciphertext: bytes, length: int) -> bytes:
    if len(ciphertext) < length:
        raise ValueError("Ciphertext is shorter than the source pixel data")
    return ciphertext[:length]


def create_comparison(image_files: list[tuple[str, Path]], output_path: Path) -> None:
    thumbnails: list[tuple[str, Image.Image]] = []
    for label, path in image_files:
        image = Image.open(path).convert("RGB")
        image.thumbnail((320, 240))
        thumbnails.append((label, image.copy()))
    card_width, card_height = 340, 280
    columns = 3
    rows = (len(thumbnails) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * card_width, rows * card_height), "#07111f")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, (label, image) in enumerate(thumbnails):
        x = (index % columns) * card_width + (card_width - image.width) // 2
        y = (index // columns) * card_height + 30
        draw.text((index % columns * card_width + 12, index // columns * card_height + 10), label, fill="#6ee7ff", font=font)
        canvas.paste(image, (x, y))
    canvas.save(output_path)


def process_image(image_path: str | Path, output_dir: str | Path = "mode_results", key: bytes | None = None) -> dict:
    """Encrypt a user-selected image in five modes, render comparisons, and verify decryption."""
    source_path = Path(image_path).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"Image not found: {source_path}")
    key = key or secrets.token_bytes(16)
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must contain 16, 24, or 32 bytes")

    destination = Path(output_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as opened:
        source = opened.convert("RGB")
    size = source.size
    plaintext = source.tobytes()
    original_file = destination / "original.png"
    source.save(original_file)

    records: list[ModeRecord] = []
    comparison_files: list[tuple[str, Path]] = [("Original", original_file)]
    for mode in MODES:
        ciphertext, parameter = _encrypt(mode, plaintext, key)
        recovered = _decrypt(mode, ciphertext, key, parameter)
        verified = recovered == plaintext
        visual_file = destination / f"{mode.lower()}_visual.png"
        Image.frombytes("RGB", size, _visual_bytes(ciphertext, len(plaintext))).save(visual_file)
        comparison_files.append((mode, visual_file))
        records.append(
            ModeRecord(
                mode=mode,
                ciphertext_bytes=len(ciphertext),
                visual_file=visual_file.name,
                iv_or_nonce_hex=parameter.hex() if parameter else None,
                round_trip_verified=verified,
            )
        )

    Image.frombytes("RGB", size, plaintext).save(destination / "decrypted_check.png")
    comparison_path = destination / "comparison.png"
    create_comparison(comparison_files, comparison_path)
    manifest = {
        "source_file": source_path.name,
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "dimensions": list(size),
        "color_mode": "RGB",
        "key_fingerprint_sha256": hashlib.sha256(key).hexdigest(),
        "all_round_trips_verified": all(record.round_trip_verified for record in records),
        "modes": [asdict(record) for record in records],
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {**manifest, "output_dir": str(destination), "comparison_file": str(comparison_path), "session_key_hex": key.hex()}
