#!/usr/bin/env python3
"""Check every packaged font against the AEC test set (issue #25).

The test set is `AEC_TEST_SET` in crates/openaec-ui/src/fonts.rs; the fonts are
the ones in crates/openaec-ui/assets/fonts/manifest.json. A character a font
lacks must be in the fallback font, otherwise the renderer picks whatever
system font the computer has. Reads the cmap table itself, no fontTools needed.
"""

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "crates/openaec-ui/assets/fonts"
SOURCE = ROOT / "crates/openaec-ui/src/fonts.rs"


def test_set():
    block = SOURCE.read_text(encoding="utf-8").split("pub const AEC_TEST_SET", 1)[1].split("];", 1)[0]
    groups = re.findall(r'\("([^"]+)",\s*"([^"]+)"\)', block)
    assert groups, "AEC_TEST_SET not found in fonts.rs"
    return [(name, [c for c in chars if not c.isspace()]) for name, chars in groups]


def cmap(data):
    """Returns the set of code points a TTF maps (cmap formats 4 and 12)."""
    num_tables = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        tag, _, offset, _ = struct.unpack(">4sIII", data[12 + 16 * i: 28 + 16 * i])
        tables[tag] = offset
    base = tables[b"cmap"]
    count = struct.unpack(">H", data[base + 2: base + 4])[0]
    points = set()
    for i in range(count):
        platform, encoding, offset = struct.unpack(">HHI", data[base + 4 + 8 * i: base + 12 + 8 * i])
        if (platform, encoding) not in ((3, 1), (3, 10), (0, 3), (0, 4)):
            continue
        at = base + offset
        fmt = struct.unpack(">H", data[at: at + 2])[0]
        if fmt == 4:
            segs = struct.unpack(">H", data[at + 6: at + 8])[0] // 2
            ends = struct.unpack(f">{segs}H", data[at + 14: at + 14 + 2 * segs])
            start_at = at + 16 + 2 * segs
            starts = struct.unpack(f">{segs}H", data[start_at: start_at + 2 * segs])
            deltas = struct.unpack(f">{segs}h", data[start_at + 2 * segs: start_at + 4 * segs])
            range_at = start_at + 4 * segs
            ranges = struct.unpack(f">{segs}H", data[range_at: range_at + 2 * segs])
            for s in range(segs):
                for c in range(starts[s], ends[s] + 1):
                    if c == 0xFFFF:
                        continue
                    if ranges[s] == 0:
                        glyph = (c + deltas[s]) & 0xFFFF
                    else:
                        g_at = range_at + 2 * s + ranges[s] + 2 * (c - starts[s])
                        glyph = struct.unpack(">H", data[g_at: g_at + 2])[0]
                        if glyph:
                            glyph = (glyph + deltas[s]) & 0xFFFF
                    if glyph:
                        points.add(c)
        elif fmt == 12:
            groups = struct.unpack(">I", data[at + 12: at + 16])[0]
            for g in range(groups):
                start, end, glyph = struct.unpack(">III", data[at + 16 + 12 * g: at + 28 + 12 * g])
                for c in range(start, end + 1):
                    if glyph + (c - start):
                        points.add(c)
    return points


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console defaults to cp1252
    manifest = json.loads((FONTS / "manifest.json").read_text(encoding="utf-8"))
    groups = test_set()
    chars = [c for _, group in groups for c in group]
    fallback = manifest.get("fallback", [])
    fallback_points = set()
    for font in fallback:
        fallback_points |= cmap((FONTS / font["file"]).read_bytes())

    uncovered = {}
    for font in manifest["fonts"]:
        points = cmap((FONTS / font["file"]).read_bytes())
        missing = [c for c in chars if ord(c) not in points]
        label = f"{font['family']} {font['weight']}"
        if missing:
            print(f"  {label}: mist {' '.join(missing)}")
        else:
            print(f"  {label}: compleet")
        lost = [c for c in missing if ord(c) not in fallback_points]
        if lost:
            uncovered[label] = lost

    if uncovered:
        where = "; ".join(f"{label}: {' '.join(lost)}" for label, lost in uncovered.items())
        fallback_name = ", ".join(f["family"] for f in fallback) or "geen terugvalfont"
        print(f"Tekenset niet gedekt ({fallback_name}): {where}")
        return 1
    print(f"Tekenset gedekt: {len(chars)} tekens in {len(manifest['fonts'])} fonts, ontbrekende tekens komen uit {', '.join(f['family'] for f in fallback)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
