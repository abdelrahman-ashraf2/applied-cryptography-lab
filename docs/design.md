# Design notes

## Why the image tool keeps two representations

ECB and CBC pad plaintext to a complete AES block, so their ciphertext may be longer than the RGB pixel buffer. The lab keeps the complete ciphertext for correct decryption and uses only the first `width × height × 3` bytes to produce the visualization. This avoids the data-loss bug caused by truncating ciphertext and then trying to decrypt the truncated result.

## What each demonstration teaches

- **Feistel network:** encryption and decryption use the same round structure with reversed keys.
- **Diffie-Hellman MITM:** key exchange without authentication cannot prove who owns a public value.
- **AES image modes:** ECB exposes repeated visual structure; randomized modes obscure it. Confidentiality modes alone do not provide integrity.
- **DSA:** verification binds a signature to a message. Reusing or exposing the nonce can reveal the private key.

## Security boundaries

The Feistel cipher, small Diffie-Hellman group, and small DSA parameters exist for education and are insecure for real data. The image tool uses AES correctly enough to demonstrate confidentiality modes and round trips, but a production design should use an authenticated mode such as AES-GCM or ChaCha20-Poly1305 and a proper key-management system.
