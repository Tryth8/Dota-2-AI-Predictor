import shutil
from pathlib import Path

from PIL import Image


def crop_hero_icons_percent(image_path, output_dir):
    output_dir = Path(output_dir)

    hero_positions_percent = [
        (0.11, 0.007, 0.055, 0.06),
        (0.174, 0.007, 0.055, 0.06),
        (0.24, 0.007, 0.055, 0.06),
        (0.30, 0.007, 0.055, 0.06),
        (0.37, 0.007, 0.055, 0.06),
        (0.572, 0.007, 0.055, 0.06),
        (0.64, 0.007, 0.055, 0.06),
        (0.70, 0.007, 0.055, 0.06),
        (0.765, 0.007, 0.055, 0.06),
        (0.831, 0.007, 0.055, 0.06),
    ]

    img = Image.open(image_path)
    img_width, img_height = img.size

    output_dir.mkdir(parents=True, exist_ok=True)

    for file in output_dir.iterdir():
        if file.is_file():
            file.unlink()
        elif file.is_dir():
            shutil.rmtree(file)

    for i, (x_pct, y_pct, width_pct, height_pct) in enumerate(hero_positions_percent):
        x = img_width * x_pct
        y = img_height * y_pct
        width = img_width * width_pct
        height = img_height * height_pct

        area = tuple(int(i) for i in (x, y, x + width, y + height))
        cropped_img = img.crop(area)

        cropped_img.save(f"{output_dir}/hero_{i + 1}.jpg")
