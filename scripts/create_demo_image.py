"""Create an original geometric image for the public demo."""

from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    destination = Path(__file__).resolve().parents[1] / "assets" / "demo-input.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    width, height = 960, 600
    image = Image.new("RGB", (width, height), "#07111f")
    draw = ImageDraw.Draw(image)
    for y in range(height):
        blue = 24 + int(42 * y / height)
        draw.line((0, y, width, y), fill=(5, blue, 52 + int(40 * y / height)))
    for index in range(13):
        x = 65 + index * 70
        color = (34 + index * 8, 211 - index * 5, 238)
        draw.rounded_rectangle((x, 105, x + 42, 490), radius=18, outline=color, width=4)
        draw.ellipse((x - 10, 65 + (index % 3) * 14, x + 52, 127 + (index % 3) * 14), fill=color)
    draw.rounded_rectangle((180, 210, 780, 390), radius=28, fill="#0d1b2e", outline="#6ee7ff", width=5)
    draw.text((275, 260), "APPLIED CRYPTOGRAPHY", fill="#f8fafc", stroke_width=1)
    draw.text((345, 320), "ABDELRAHMAN ASHRAF", fill="#6ee7ff")
    image.save(destination)
    print(destination)


if __name__ == "__main__":
    main()
