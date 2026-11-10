"""
Process the client-supplied app images into web-ready screenshots.

The 8 promotional posters (759x1440) have an English caption band and a solid
coloured background around a phone screenshot. We crop the actual app screen
and save it as WebP. The 4 raw device screenshots (720x1600) are converted
directly.

Usage:
    python tools/process_uploads.py
"""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "_uploads"
OUT = ROOT / "assets" / "img" / "screens"

# Poster crop: the screenshot occupies x 76..683, y 204..bottom in every poster.
POSTER_BOX = (77, 205, 682, 1440)

# Source file -> output name
POSTERS = {
    "01.png": "home",
    "02.png": "medicine-details",
    "03.png": "calculators",
    "04.png": "bmi",
    "05.png": "directory-home",
    "06.png": "symptoms-checker",
    "07.png": "doctors",
    "08.png": "doctor-details",
}

RAW = {
    "09.png": "my-medicine",
    "10.png": "medicine-reminder",
    "11.png": "medicine-cost",
    "12.png": "medicine-search",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for filename, name in POSTERS.items():
        source = SRC / filename
        with Image.open(source) as image:
            cropped = image.convert("RGB").crop(POSTER_BOX)
            target = OUT / f"{name}.webp"
            cropped.save(target, "WEBP", quality=90, method=6)
            print(f"{filename} -> {target.name}  {cropped.size}  {target.stat().st_size // 1024} KB")

    for filename, name in RAW.items():
        source = SRC / filename
        with Image.open(source) as image:
            converted = image.convert("RGB")
            target = OUT / f"{name}.webp"
            converted.save(target, "WEBP", quality=90, method=6)
            print(f"{filename} -> {target.name}  {converted.size}  {target.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
