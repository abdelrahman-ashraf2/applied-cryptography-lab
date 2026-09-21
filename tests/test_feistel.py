import pytest

from crypto_lab.feistel import decrypt_bytes, decrypt_text, encrypt_bytes, encrypt_text


@pytest.mark.parametrize("message", ["", "Hello", "أمن المعلومات", "odd length!"])
def test_text_round_trip(message):
    assert decrypt_text(encrypt_text(message)) == message


def test_binary_round_trip():
    payload = bytes(range(256))
    assert decrypt_bytes(encrypt_bytes(payload)) == payload


def test_rejects_incomplete_ciphertext():
    with pytest.raises(ValueError):
        decrypt_bytes(b"x")
