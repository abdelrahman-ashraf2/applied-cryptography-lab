import pytest

from crypto_lab.diffie_hellman import simulate_mitm


def test_mitm_establishes_two_attacker_controlled_channels():
    result = simulate_mitm()
    assert result.attack_succeeded
    assert result.alice_mallory_key == result.mallory_alice_key
    assert result.bob_mallory_key == result.mallory_bob_key


def test_rejects_composite_modulus():
    with pytest.raises(ValueError, match="prime"):
        simulate_mitm(p=21)
