#!/usr/bin/env python3
"""Puts the web package of design 0.4 into the Tauri template.

The template in style-book/project-templates/Tauri+React is copied as a whole
when a new tool starts, so it carries its own copy of the web package instead
of a path into this repository. This script writes that copy from web/:

  src/openaec/openaec-tokens.css   the tokens, unchanged
  src/openaec/openaec-fonts.css    the fonts, WOFF2 only (a webview reads it)
  src/openaec/fonts/               the WOFF2 files and their licences
  public/icons/standard.svg        the B2 icons of the standard application

  python scripts/sync_tauri_template.py           write the copy
  python scripts/sync_tauri_template.py --check   compare only (for the checks)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
TEMPLATE = ROOT / "style-book/project-templates/Tauri+React"
NOTE = "/* Copied from web/ by scripts/sync_tauri_template.py; do not edit here. */\n"


def files():
    """{target path: bytes} for everything the template gets from web/."""
    out = {}
    out[TEMPLATE / "src/openaec/openaec-tokens.css"] = (NOTE + (WEB / "openaec-tokens.css").read_text(encoding="utf-8")).encode("utf-8")
    fonts = (WEB / "openaec-fonts.css").read_text(encoding="utf-8")
    fonts, count = re.subn(r', url\("fonts/[^"]+\.ttf"\) format\("truetype"\)', "", fonts)
    assert count, "openaec-fonts.css has no TTF fallbacks to leave out; check the format"
    out[TEMPLATE / "src/openaec/openaec-fonts.css"] = (NOTE + fonts).encode("utf-8")
    for font in sorted((WEB / "fonts").iterdir()):
        if font.suffix in (".woff2", ".txt"):
            out[TEMPLATE / "src/openaec/fonts" / font.name] = font.read_bytes()
    out[TEMPLATE / "public/icons/standard.svg"] = (WEB / "icons/standard.svg").read_bytes()
    return out


def main():
    check = "--check" in sys.argv[1:]
    want = files()
    managed = [TEMPLATE / "src/openaec/fonts", TEMPLATE / "public/icons"]
    present = {p for d in managed if d.exists() for p in d.iterdir()}
    stale = [p for p, data in want.items() if not p.exists() or p.read_bytes() != data]
    extra = sorted(present - set(want))
    if check:
        if stale or extra:
            first = (stale + extra)[0].relative_to(ROOT).as_posix()
            print(f"Tauri-sjabloon loopt achter op web/, draai scripts/sync_tauri_template.py: {len(stale) + len(extra)} bestanden, bijvoorbeeld {first}")
            return 1
        print(f"Tauri-sjabloon gelijk met web/: {len(want)} bestanden (tokens, fonts, B2-iconen)")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(want[path])
    for path in extra:
        path.unlink()
    print(f"Tauri-sjabloon bijgewerkt: {len(stale)} bestanden geschreven, {len(extra)} verwijderd, {len(want)} in totaal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
