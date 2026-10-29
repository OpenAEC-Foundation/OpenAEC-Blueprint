#!/usr/bin/env python3
"""The images of the README, made from renders that are already in design/.

  python scripts/build_readme_images.py           write docs/images/readme/*.png
  python scripts/build_readme_images.py --check   images present, small enough and
                                                  all used in README.md and README.nl.md

Sources: the renders of the Rust standard application (cargo test --bin blueprint
-- --ignored, in design/blueprint/), of the ui04 gallery (design/ontwerp-0.4/native/)
and of the online application (node web/online/screenshots.mjs, in design/online/).
An image larger than MAX_BYTES is reduced to 256 colours without dithering, which
keeps interface text sharp. Writing needs Pillow; --check does not.
"""

import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images" / "readme"
READMES = ["README.md", "README.nl.md"]
MAX_BYTES = 150 * 1024
WIDTH = 1280

# Output name -> one source, or four sources for a 2x2 mosaic.
IMAGES = {
    "hero-3d.png": "design/online/online-3d-dark.png",
    "rust-app.png": "design/blueprint/blueprint-light.png",
    "themes.png": [
        "design/blueprint/blueprint-light.png",
        "design/blueprint/blueprint-dark.png",
        "design/blueprint/blueprint-blueprint.png",
        "design/blueprint/blueprint-high-contrast-dark.png",
    ],
    "tauri-app.png": "design/online/online-light.png",
    "settings.png": "design/online/online-settings-blueprint.png",
    "icons.png": "design/ontwerp-0.4/native/iconen-dark.png",
    "workflow-app.png": "design/ontwerp-0.4/native/werkstroom-zijbalk-light.png",
    "installer.png": "design/ontwerp-0.4/native/installer-light.png",
    "rust-file.png": "design/blueprint/blueprint-bestand.png",
    "rust-settings.png": "design/blueprint/blueprint-instellingen.png",
    "start-screen.png": "design/ontwerp-0.4/native/start-light.png",
    "workflow-steps.png": "design/ontwerp-0.4/native/werkstroom-stappen-light.png",
}


def build():
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    for name, source in IMAGES.items():
        if isinstance(source, list):
            tiles = [Image.open(ROOT / s).convert("RGB") for s in source]
            w, h = tiles[0].size
            image = Image.new("RGB", (w, h), "white")
            gap = 8
            half = ((w - gap) // 2, (h - gap) // 2)
            for i, tile in enumerate(tiles):
                x = (i % 2) * (half[0] + gap)
                y = (i // 2) * (half[1] + gap)
                image.paste(tile.resize(half, Image.LANCZOS), (x, y))
        else:
            image = Image.open(ROOT / source).convert("RGB")
        if image.width > WIDTH:
            image = image.resize((WIDTH, round(image.height * WIDTH / image.width)), Image.LANCZOS)
        path = OUT / name
        image.save(path, optimize=True)
        if path.stat().st_size > MAX_BYTES:
            image.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)
        print(f"{path.relative_to(ROOT).as_posix()}  {path.stat().st_size // 1024} kB")


def png_size(path):
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def check():
    errors = []
    for name in IMAGES:
        path = OUT / name
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT).as_posix()}; run this script without --check")
            continue
        if not png_size(path):
            errors.append(f"{name} is not a PNG")
        if path.stat().st_size > MAX_BYTES:
            errors.append(f"{name} is {path.stat().st_size // 1024} kB, more than {MAX_BYTES // 1024} kB")
    on_disk = {p.name for p in OUT.glob("*")} if OUT.exists() else set()
    for extra in sorted(on_disk - set(IMAGES)):
        errors.append(f"docs/images/readme/{extra} is not made by this script")
    for readme in READMES:
        text = (ROOT / readme).read_text(encoding="utf-8")
        used = set(re.findall(r"docs/images/readme/([\w.-]+)", text))
        for name in sorted(used - set(IMAGES)):
            errors.append(f"{readme} uses docs/images/readme/{name}, which does not exist")
        for name in sorted(set(IMAGES) - used):
            errors.append(f"{readme} does not use docs/images/readme/{name}")
    for error in errors:
        print(error)
    if not errors:
        print(f"{len(IMAGES)} README images present and used in {', '.join(READMES)}")
    return not errors


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        sys.exit(0 if check() else 1)
    build()
