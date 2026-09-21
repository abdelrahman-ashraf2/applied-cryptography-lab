# Project 2: Diffie-Hellman MITM Attack
# Hint: Darth makes two keys: one with Alice and one with Bob.

# Hint: Press Enter to use the test values from the slide.
p = int(input("Prime p [11]: ") or 11)
g = int(input("Generator g [15]: ") or 15)
a = int(input("Alice private key a [7]: ") or 7)
b = int(input("Bob private key b [9]: ") or 9)
a1 = int(input("Darth private key with Bob a1 [5]: ") or 5)
b1 = int(input("Darth private key with Alice b1 [3]: ") or 3)

# Hint: Public key = g^private mod p
A = pow(g, a, p)      # Alice public key
B = pow(g, b, p)      # Bob public key

# Hint: Darth sends fake public keys instead of real ones.
D_to_Bob = pow(g, a1, p)
D_to_Alice = pow(g, b1, p)

# Alice and Bob calculate keys using Darth's fake public keys.
alice_key = pow(D_to_Alice, a, p)
bob_key = pow(D_to_Bob, b, p)

# Darth calculates the same two keys.
darth_with_alice = pow(A, b1, p)
darth_with_bob = pow(B, a1, p)

print("\nPublic keys:")
print("Alice public =", A)
print("Bob public   =", B)
print("Darth to Alice =", D_to_Alice)
print("Darth to Bob   =", D_to_Bob)

print("\nShared keys:")
print("Alice key        =", alice_key)
print("Darth with Alice =", darth_with_alice)
print("Bob key          =", bob_key)
print("Darth with Bob   =", darth_with_bob)

print("\nResult:")
print("Darth can read Alice messages using key", darth_with_alice)
print("Darth can send to Bob using key", darth_with_bob)
