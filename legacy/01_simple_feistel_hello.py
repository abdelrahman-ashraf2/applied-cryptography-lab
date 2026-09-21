# Project 1: Feistel Cipher
# Hint: This is a very simple educational cipher, not real security.

message = "Hello"
data = message.encode()

# Hint: Feistel uses 2 halves, so we make the length even.
if len(data) % 2 == 1:
    data += b" "

# Hint: These are small round keys for the example.
keys = [12, 34, 56, 78]

cipher = b""

# Hint: Encrypt 2 bytes at a time: left byte and right byte.
for i in range(0, len(data), 2):
    left = data[i]
    right = data[i + 1]

    # Hint: Repeat Feistel rounds.
    for key in keys:
        f = (right + key) % 256       # simple round function F(R, K)
        left, right = right, left ^ f # swap and XOR

    cipher += bytes([left, right])

print("Plain text :", message)
print("Cipher hex :", cipher.hex())
print("Cipher bytes:", cipher)
