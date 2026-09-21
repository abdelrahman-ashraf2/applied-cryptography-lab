"""A tiny reversible Feistel network for learning, not production security."""

from __future__ import annotations


DEFAULT_KEYS = (12, 34, 56, 78)


def _validate_keys(keys: tuple[int, ...]) -> None:
    if not keys:
        raise ValueError("At least one round key is required")
    if any(not 0 <= key <= 255 for key in keys):
        raise ValueError("Every round key must be a byte (0..255)")


def _round_function(right: int, key: int) -> int:
    return ((right * 17) ^ key) & 0xFF


def _transform_block(block: bytes, keys: tuple[int, ...]) -> bytes:
    left, right = block
    for key in keys:
        left, right = right, left ^ _round_function(right, key)
    return bytes((left, right))


def _inverse_block(block: bytes, keys: tuple[int, ...]) -> bytes:
    left, right = block
    for key in reversed(keys):
        left, right = right ^ _round_function(left, key), left
    return bytes((left, right))


def encrypt_bytes(data: bytes, keys: tuple[int, ...] = DEFAULT_KEYS) -> bytes:
    """Encrypt bytes with a toy two-byte Feistel network and PKCS#7 padding."""
    _validate_keys(keys)
    padding_length = 2 - (len(data) % 2)
    padded = data + bytes((padding_length,)) * padding_length
    return b"".join(_transform_block(padded[i : i + 2], keys) for i in range(0, len(padded), 2))


def decrypt_bytes(ciphertext: bytes, keys: tuple[int, ...] = DEFAULT_KEYS) -> bytes:
    """Reverse :func:`encrypt_bytes` and validate its padding."""
    _validate_keys(keys)
    if not ciphertext or len(ciphertext) % 2:
        raise ValueError("Ciphertext must contain complete two-byte blocks")
    padded = b"".join(_inverse_block(ciphertext[i : i + 2], keys) for i in range(0, len(ciphertext), 2))
    padding_length = padded[-1]
    if padding_length not in (1, 2) or padded[-padding_length:] != bytes((padding_length,)) * padding_length:
        raise ValueError("Invalid padding or incorrect keys")
    return padded[:-padding_length]


def encrypt_text(message: str, keys: tuple[int, ...] = DEFAULT_KEYS) -> str:
    return encrypt_bytes(message.encode("utf-8"), keys).hex()


def decrypt_text(ciphertext_hex: str, keys: tuple[int, ...] = DEFAULT_KEYS) -> str:
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError as exc:
        raise ValueError("Ciphertext must be valid hexadecimal") from exc
    return decrypt_bytes(ciphertext, keys).decode("utf-8")
