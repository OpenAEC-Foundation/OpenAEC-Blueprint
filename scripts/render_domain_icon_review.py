#!/usr/bin/env python3
"""Render FEM/BIM icon drafts at their actual small sizes for visual review."""

import io
import json
import warnings
from pathlib import Path

import cairo
import gi
from PIL import Image, ImageDraw, ImageFont, ImageOps

gi.require_version("Rsvg", "2.0")
from gi.repository import Rsvg

ROOT = Path(__file__).resolve().parents[1]
ICON_SIZE = 24
CELL_WIDTH = 180
CELL_HEIGHT = 100
COLUMNS = 6
FONT = ImageFont.truetype("DejaVuSans.ttf", 11)


def svg_image(path: Path, pixels: int) -> Image.Image:
    handle = Rsvg.Handle.new_from_file(str(path))
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pixels, pixels)
    context = cairo.Context(surface)
    context.scale(pixels / ICON_SIZE, pixels / ICON_SIZE)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        handle.render_cairo(context)
    stream = io.BytesIO()
    surface.write_to_png(stream)
    stream.seek(0)
    return Image.open(stream).convert("RGBA")


def sheet(domain: str, records: list[dict]) -> None:
    count = len(records)
    rows = (count + COLUMNS - 1) // COLUMNS
    canvas = Image.new("RGB", (COLUMNS * CELL_WIDTH, rows * CELL_HEIGHT), "#e9ecf0")
    draw = ImageDraw.Draw(canvas)
    for index, record in enumerate(records):
        x = index % COLUMNS * CELL_WIDTH
        y = index // COLUMNS * CELL_HEIGHT
        draw.rounded_rectangle((x + 3, y + 3, x + CELL_WIDTH - 4, y + CELL_HEIGHT - 4),
                               radius=5, fill="#ffffff", outline="#c7cbd1")
        path = ROOT / "design" / record["file"]
        small = svg_image(ROOT / "design" / record.get("small_file", record["file"]), 16)
        regular = svg_image(path, 24)
        dark = ImageOps.invert(small.convert("RGB")).convert("RGBA")
        dark.putalpha(small.getchannel("A"))
        for left, icon, background in [(x + 8, small, "#f6f7f9"),
                                        (x + 66, regular, "#f6f7f9"),
                                        (x + 124, dark, "#242a31")]:
            draw.rectangle((left, y + 8, left + 48, y + 56), fill=background)
            enlarged = icon.resize((48, 48), Image.Resampling.NEAREST)
            canvas.paste(enlarged, (left, y + 8), enlarged)
        draw.text((x + 8, y + 62), record["id"], font=FONT, fill="#262a30")
        draw.text((x + 8, y + 79), record["group"], font=FONT, fill="#717780")
    output = ROOT / "design" / f"{domain}-icon-small-review.png"
    canvas.save(output)
    print(f"{output}: {count} icons")


def main() -> None:
    records = json.loads((ROOT / "design/domain-icon-drafts.json").read_text())
    for domain in ("fem", "bim"):
        sheet(domain, [record for record in records if record["domain"] == domain])


if __name__ == "__main__":
    main()
