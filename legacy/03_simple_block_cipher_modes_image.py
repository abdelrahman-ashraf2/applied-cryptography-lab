# Project 3: Block Cipher Modes on an Image
# Hint: Install libraries first: pip install pillow pycryptodome
# Hint: Put a JPG image named input.jpg in the same folder.

from pathlib import Path
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

image_path = Path("input.jpg")

# Hint: If input.jpg is missing, this creates a simple test image.
if not image_path.exists():
    img = Image.new("RGB", (160, 160), "white")
    pixels = img.load()
    for x in range(160):
        for y in range(160):
            if (x // 20) % 2 == (y // 20) % 2:
                pixels[x, y] = (0, 0, 0)
    img.save(image_path)

# Hint: Open image and convert it to raw RGB bytes.
img = Image.open(image_path).convert("RGB")
data = img.tobytes()
size = img.size

# Hint: AES key must be 16 bytes.
key = b"Sixteen byte key"
iv = b"1234567890abcdef"

out = Path("mode_results")
out.mkdir(exist_ok=True)
img.save(out / "original.png")

# Hint: ECB shows repeated patterns more clearly.
ecb = AES.new(key, AES.MODE_ECB).encrypt(pad(data, 16))[:len(data)]

# Hint: CBC uses an IV and hides patterns better than ECB.
cbc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data, 16))[:len(data)]

# Hint: CFB, OFB, and CTR work like stream modes.
cfb = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128).encrypt(data)
ofb = AES.new(key, AES.MODE_OFB, iv=iv).encrypt(data)
ctr = AES.new(key, AES.MODE_CTR, nonce=b"12345678").encrypt(data)

# Hint: Save encrypted bytes as images to compare visually.
Image.frombytes("RGB", size, ecb).save(out / "ECB.png")
Image.frombytes("RGB", size, cbc).save(out / "CBC.png")
Image.frombytes("RGB", size, cfb).save(out / "CFB.png")
Image.frombytes("RGB", size, ofb).save(out / "OFB.png")
Image.frombytes("RGB", size, ctr).save(out / "CTR.png")

print("Images saved in folder:", out)
print("ECB: patterns may appear")
print("CBC: hides patterns better")
print("CFB/OFB/CTR: stream-like modes")
