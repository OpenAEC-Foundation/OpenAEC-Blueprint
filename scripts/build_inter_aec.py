#!/usr/bin/env python3
"""Inter AEC: Inter with its tabular figures and disambiguation frozen (issue #28).

iced 0.14 and most PDF writers apply no OpenType features, so Inter's `tnum`
(digits of one width) and `ss04` (I with serif, l with tail, zero without a
slash) are frozen into the character map: each character points straight at
the alternate glyph. The result gets its own family name, "Inter AEC", so it
never stands in for the original. Inter has no Reserved Font Name; the OFL text
and copyright stay the same (licenses/Inter-OFL.txt).

Needs fontTools: python -m pip install --target harmonization/sources/font-runtime
-r scripts/requirements-fonts.txt. Then run this script and
scripts/build_font_package.py, which records the source hashes and checks them
without fontTools.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harmonization/sources/font-runtime"))
FONTS = ROOT / "crates/openaec-ui/assets/fonts"

FAMILY = "Inter AEC"
# Applied in this order; both are single substitutions in Inter 4.001.
FEATURES = ("ss04", "tnum")
SOURCES = {
    "Inter-Regular.ttf": "InterAEC-Regular.ttf",
    "Inter-Medium.ttf": "InterAEC-Medium.ttf",
    "Inter-SemiBold.ttf": "InterAEC-SemiBold.ttf",
}


def feature_map(font, tag):
    gsub = font["GSUB"].table
    mapping = {}
    for record in gsub.FeatureList.FeatureRecord:
        if record.FeatureTag != tag:
            continue
        for index in record.Feature.LookupListIndex:
            lookup = gsub.LookupList.Lookup[index]
            assert lookup.LookupType == 1, f"{tag} is not a single substitution"
            for sub in lookup.SubTable:
                mapping.update(sub.mapping)
    assert mapping, f"{tag} not found"
    return mapping


def build(source):
    from fontTools.ttLib import TTFont

    font = TTFont(source, recalcTimestamp=False)
    maps = [feature_map(font, tag) for tag in FEATURES]
    for table in font["cmap"].tables:
        for code, glyph in list(table.cmap.items()):
            for mapping in maps:
                glyph = mapping.get(glyph, glyph)
            table.cmap[code] = glyph

    names = font["name"]
    for record in names.names:
        text = record.toUnicode()
        if record.nameID in (1, 3, 4, 16):
            record.string = text.replace("Inter", FAMILY, 1)
        elif record.nameID == 6:
            record.string = text.replace("Inter-", "InterAEC-", 1)
        elif record.nameID == 5:
            record.string = f"{text}; OpenAEC {' '.join(FEATURES)}"
    names.setName(f"Inter with {', '.join(FEATURES)} frozen into the character map by OpenAEC (scripts/build_inter_aec.py). Same OFL as Inter.", 10, 3, 1, 0x409)
    return font


def main():
    try:
        import fontTools  # noqa: F401
    except ImportError:
        print("fontTools ontbreekt: python -m pip install --target harmonization/sources/font-runtime -r scripts/requirements-fonts.txt")
        return 1
    import io

    changed = 0
    for source, target in SOURCES.items():
        buffer = io.BytesIO()
        build(FONTS / source).save(buffer)
        data = buffer.getvalue()
        path = FONTS / target
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            changed += 1
    print(f"{FAMILY}: {len(SOURCES)} gewichten, {' + '.join(FEATURES)} vastgezet, {changed} bestanden bijgewerkt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
