#!/usr/bin/env python3
"""Render 16/24/32 px vector drafts on light and dark review surfaces."""
from pathlib import Path
import io
import warnings

import cairo
import gi
from PIL import Image, ImageDraw, ImageFont

gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / 'design/icon-collision-drafts').glob('*.svg'))
assert len(files) == 12
font_path = ROOT / 'assets/fonts/Inter-Regular.ttf'
font = ImageFont.truetype(str(font_path), 15)
small = ImageFont.truetype(str(font_path), 11)
board = Image.new('RGB', (920, 1010), '#f0f2f4')
draw = ImageDraw.Draw(board)
draw.text((16, 8), 'OPENAEC · COLLISION ICON DRAFTS', font=font, fill='#272b32')
for col, label in enumerate(['16 LIGHT', '16 DARK', '24 LIGHT', '24 DARK', '32 LIGHT', '32 DARK']):
    draw.text((216 + col * 116, 45), label, font=small, fill='#565d67')
for index, path in enumerate(files):
    y = 67 + index * 78
    draw.text((16, y + 30), path.stem, font=small, fill='#30343b')
    source = path.read_text()
    for col, (size, dark) in enumerate([(16, False), (16, True), (24, False), (24, True), (32, False), (32, True)]):
        x = 211 + col * 116
        bg = '#292d34' if dark else '#ffffff'
        draw.rounded_rectangle((x, y, x + 105, y + 68), radius=3, fill=bg, outline='#d4d8dd')
        color = '#f1f2f3' if dark else '#22262c'
        small_path = ROOT / 'design/icon-collision-drafts-small' / path.name
        markup = (small_path.read_text() if size == 16 else source).replace('#000', color)
        handle = Rsvg.Handle.new_from_data(markup.encode())
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
        context = cairo.Context(surface)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            handle.render_cairo(context)
        png = io.BytesIO()
        surface.write_to_png(png)
        png.seek(0)
        icon = Image.open(png).convert('RGBA')
        board.paste(icon, (x + (105-size)//2, y + (68-size)//2), icon)
board.save(ROOT / 'design/icon-collision-drafts-review.png')
print(f'Rendered {len(files)} icon drafts at 16/24/32 px')
