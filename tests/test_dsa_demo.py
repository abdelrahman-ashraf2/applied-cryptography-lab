from crypto_lab.dsa_demo import public_key, sign, verify


def test_signature_validates_only_original_message():
    signature = sign("security matters", private_key=24, nonce=15)
    key = public_key(24)
    assert verify("security matters", signature, key)
    assert not verify("security matters!", signature, key)


def test_random_nonce_signature_validates():
    message = "fresh nonce"
    signature = sign(message, private_key=24)
    assert verify(message, signature, public_key(24))
