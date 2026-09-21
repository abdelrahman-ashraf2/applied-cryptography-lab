"""Small-number Diffie-Hellman and man-in-the-middle demonstrations."""

from __future__ import annotations

from dataclasses import asdict, dataclass


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def _validate(p: int, g: int, *private_values: int) -> None:
    if not _is_prime(p):
        raise ValueError("p must be prime")
    if not 1 < g < p:
        raise ValueError("g must be between 2 and p - 1")
    if any(not 1 < value < p - 1 for value in private_values):
        raise ValueError("Private values must be between 2 and p - 2")


@dataclass(frozen=True)
class MitmResult:
    p: int
    g: int
    alice_public: int
    bob_public: int
    direct_shared_key: int
    mallory_public_to_alice: int
    mallory_public_to_bob: int
    alice_mallory_key: int
    mallory_alice_key: int
    bob_mallory_key: int
    mallory_bob_key: int

    @property
    def attack_succeeded(self) -> bool:
        return (
            self.alice_mallory_key == self.mallory_alice_key
            and self.bob_mallory_key == self.mallory_bob_key
            and self.alice_mallory_key != self.direct_shared_key
        )

    def to_dict(self) -> dict[str, int | bool]:
        return {**asdict(self), "attack_succeeded": self.attack_succeeded}


def simulate_mitm(
    p: int = 23,
    g: int = 5,
    alice_private: int = 6,
    bob_private: int = 15,
    mallory_for_alice: int = 9,
    mallory_for_bob: int = 7,
) -> MitmResult:
    """Return the keys from a normal exchange and an unauthenticated MITM exchange."""
    _validate(p, g, alice_private, bob_private, mallory_for_alice, mallory_for_bob)
    alice_public = pow(g, alice_private, p)
    bob_public = pow(g, bob_private, p)
    direct_shared_key = pow(bob_public, alice_private, p)
    if direct_shared_key != pow(alice_public, bob_private, p):
        raise AssertionError("Diffie-Hellman invariant failed")

    mallory_public_to_alice = pow(g, mallory_for_alice, p)
    mallory_public_to_bob = pow(g, mallory_for_bob, p)
    return MitmResult(
        p=p,
        g=g,
        alice_public=alice_public,
        bob_public=bob_public,
        direct_shared_key=direct_shared_key,
        mallory_public_to_alice=mallory_public_to_alice,
        mallory_public_to_bob=mallory_public_to_bob,
        alice_mallory_key=pow(mallory_public_to_alice, alice_private, p),
        mallory_alice_key=pow(alice_public, mallory_for_alice, p),
        bob_mallory_key=pow(mallory_public_to_bob, bob_private, p),
        mallory_bob_key=pow(bob_public, mallory_for_bob, p),
    )
