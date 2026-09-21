"""Command-line interface for the Applied Cryptography Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .diffie_hellman import simulate_mitm
from .dsa_demo import public_key, sign, verify
from .feistel import decrypt_text, encrypt_text
from .image_modes import process_image


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crypto-lab", description="Interactive applied cryptography demonstrations")
    subparsers = parser.add_subparsers(dest="command", required=True)

    feistel = subparsers.add_parser("feistel", help="Encrypt and decrypt a UTF-8 message with a toy Feistel network")
    feistel.add_argument("--message", help="Message to process; prompts when omitted")

    dh = subparsers.add_parser("dh-mitm", help="Demonstrate a Diffie-Hellman man-in-the-middle attack")
    dh.add_argument("--prime", type=int, default=23)
    dh.add_argument("--generator", type=int, default=5)
    dh.add_argument("--alice-private", type=int, default=6)
    dh.add_argument("--bob-private", type=int, default=15)
    dh.add_argument("--mallory-for-alice", type=int, default=9)
    dh.add_argument("--mallory-for-bob", type=int, default=7)

    image = subparsers.add_parser("image-modes", help="Visualize five AES modes using an image you choose")
    image.add_argument("image", nargs="?", help="Path to the input image; prompts when omitted")
    image.add_argument("--output", default="mode_results", help="Directory for generated files")
    image.add_argument("--key-hex", help="Optional 16/24/32-byte AES key in hexadecimal")

    dsa = subparsers.add_parser("dsa", help="Sign and verify a message with tiny teaching parameters")
    dsa.add_argument("--message", help="Message to sign; prompts when omitted")
    dsa.add_argument("--tampered-message", default="This message was modified")
    dsa.add_argument("--private-key", type=int, default=24)
    dsa.add_argument("--nonce", type=int, help="Fixed nonce for repeatable classroom output")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    if args.command == "feistel":
        message = args.message if args.message is not None else input("Message: ")
        ciphertext = encrypt_text(message)
        print(json.dumps({"message": message, "ciphertext_hex": ciphertext, "decrypted": decrypt_text(ciphertext)}, indent=2))
    elif args.command == "dh-mitm":
        result = simulate_mitm(args.prime, args.generator, args.alice_private, args.bob_private, args.mallory_for_alice, args.mallory_for_bob)
        print(json.dumps(result.to_dict(), indent=2))
    elif args.command == "image-modes":
        image_path = args.image or input("Image path: ").strip().strip('"')
        key = bytes.fromhex(args.key_hex) if args.key_hex else None
        result = process_image(Path(image_path), args.output, key)
        print(json.dumps(result, indent=2))
        print("Keep the session key private if you reuse these encrypted bytes; it is not stored in manifest.json.")
    elif args.command == "dsa":
        message = args.message if args.message is not None else input("Message: ")
        signature = sign(message, args.private_key, args.nonce)
        signer_public_key = public_key(args.private_key)
        print(json.dumps({
            "message": message,
            "public_key": signer_public_key,
            "signature": {"r": signature.r, "s": signature.s},
            "valid_original": verify(message, signature, signer_public_key),
            "valid_tampered": verify(args.tampered_message, signature, signer_public_key),
        }, indent=2))
