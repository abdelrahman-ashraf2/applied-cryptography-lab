from PIL import Image

from crypto_lab.image_modes import MODES, process_image


def test_all_image_modes_round_trip(tmp_path):
    image_path = tmp_path / "source.png"
    image = Image.new("RGB", (13, 11))
    image.putdata([((x * 19) % 256, (x * 43) % 256, (x * 71) % 256) for x in range(13 * 11)])
    image.save(image_path)

    result = process_image(image_path, tmp_path / "results", key=bytes(range(16)))

    assert result["all_round_trips_verified"]
    assert [record["mode"] for record in result["modes"]] == list(MODES)
    assert (tmp_path / "results" / "comparison.png").is_file()
    assert (tmp_path / "results" / "manifest.json").is_file()
