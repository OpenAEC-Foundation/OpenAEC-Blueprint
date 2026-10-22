#!/usr/bin/env python3
"""Crop the installer screenshots to one card aspect for the UI 0.4 gallery.

Source: harmonization/references/openaec-installer/public/previews (openaec-installer
at 8b39bae, CC BY-SA 4.0). Output: design/ontwerp-0.4/installer-previews.

The cards show the top of each screenshot with 8 px rounded corners (16 px at
this source size, shown at about half), as the website does. The lowest third
fades out to transparent, so the picture flows into the tile in every theme. Cropping here
keeps the gallery free of image cropping at run time: in iced 0.13 a cropped
(`ContentFit::Cover`) image gets its own layer that ignores the scroll area.
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "harmonization/references/openaec-installer/public/previews"
OUT = ROOT / "design/ontwerp-0.4/installer-previews"
WIDTH, HEIGHT = 640, 304  # about the 2.1 : 1 of a card preview
RADIUS = 16
FADE = 0.34  # share of the height that fades out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SRC.glob("*.jpg")):
        image = Image.open(path).convert("RGB")
        scale = WIDTH / image.width
        resized = image.resize((WIDTH, max(HEIGHT, round(image.height * scale))), Image.LANCZOS)
        picture = resized.crop((0, 0, WIDTH, HEIGHT)).convert("RGBA")
        mask = Image.new("L", (WIDTH, HEIGHT), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), RADIUS, fill=255)
        start = round(HEIGHT * (1 - FADE))
        fade = Image.new("L", (WIDTH, HEIGHT), 255)
        draw = ImageDraw.Draw(fade)
        for y in range(start, HEIGHT):
            t = (y - start) / (HEIGHT - start)
            draw.line((0, y, WIDTH, y), fill=round(255 * (1 - t * t * (3 - 2 * t))))
        picture.putalpha(ImageChops.darker(mask, fade))
        picture.save(OUT / (path.stem + ".png"), optimize=True)
        count += 1
    print(f"{count} previews cropped to {WIDTH} x {HEIGHT} in {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
