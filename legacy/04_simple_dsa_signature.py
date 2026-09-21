# Project 4: DSS / DSA Digital Signature
# Given: p=283, q=47, h=2, x=24, k=15, H(M)=41
# Hint: This is a small educational example, not real security.

p = 283
q = 47
h = 2
x = 24       # private key
k = 15       # random number
H = 41       # message hash H(M)

# Hint: Calculate generator g.
g = pow(h, (p - 1) // q, p)

# Hint: Public key y = g^x mod p.
y = pow(g, x, p)

# Hint: r = (g^k mod p) mod q.
r = pow(g, k, p) % q

# Hint: s = k^-1 * (H + x*r) mod q.
k_inverse = pow(k, -1, q)
s = (k_inverse * (H + x * r)) % q

print("g =", g)
print("Public key y =", y)
print("Signature r =", r)
print("Signature s =", s)

# Hint: Simple verification.
w = pow(s, -1, q)
u1 = (H * w) % q
u2 = (r * w) % q
v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

print("Verification v =", v)
print("Valid signature?", v == r)
