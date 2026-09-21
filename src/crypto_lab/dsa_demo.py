"""A tiny DSA-style signature demo using deliberately small teaching parameters."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass


P, Q, H = 283, 47, 2
G = pow(H, (P - 1) // Q, P)


def hash_message(message: str) -> int:
    return int.from_bytes(hashlib.sha256(message.encode("utf-8")).digest(), "big") % Q


@dataclass(frozen=True)
class Signature:
    r: int
    s: int


def public_key(private_key: int) -> int:
    if not 1 <= private_key < Q:
        raise ValueError(f"Private key must be between 1 and {Q - 1}")
    return pow(G, private_key, P)


def sign(message: str, private_key: int, nonce: int | None = None) -> Signature:
    """Sign a real message. A fixed nonce is accepted only for repeatable lessons."""
    public_key(private_key)
    while True:
        candidate = nonce if nonce is not None else secrets.randbelow(Q - 1) + 1
        if not 1 <= candidate < Q:
            raise ValueError(f"Nonce must be between 1 and {Q - 1}")
        r = pow(G, candidate, P) % Q
        s = (pow(candidate, -1, Q) * (hash_message(message) + private_key * r)) % Q
        if r and s:
            return Signature(r, s)
        if nonce is not None:
            raise ValueError("Fixed nonce produced an invalid signature; choose another nonce")


def verify(message: str, signature: Signature, signer_public_key: int) -> bool:
    if not (0 < signature.r < Q and 0 < signature.s < Q):
        return False
    try:
        w = pow(signature.s, -1, Q)
    except ValueError:
        return False
    u1 = (hash_message(message) * w) % Q
    u2 = (signature.r * w) % Q
    v = ((pow(G, u1, P) * pow(signer_public_key, u2, P)) % P) % Q
    return v == signature.r

