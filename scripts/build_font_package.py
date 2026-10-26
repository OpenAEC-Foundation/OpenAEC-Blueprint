#!/usr/bin/env python3
"""One font package for Rust, web and reports (issues #24, #25 and #28).

Source: the TTF files in crates/openaec-ui/assets/fonts and their OFL licences
in crates/openaec-ui/licenses. Writes:
  crates/openaec-ui/assets/fonts/manifest.json  family, weight, version, SHA-256, licence
  assets/fonts/<file>.ttf and manifest.json     the same, for the review copy
  web/fonts/<file>.ttf and <licence>.txt        byte copies for the web package
  web/fonts/<file>.woff2                        compressed copies for browsers
  web/openaec-fonts.css                         @font-face rules for those files
Building needs fontTools and brotli (scripts/requirements-fonts.txt in
harmonization/sources/font-runtime): it first rebuilds Inter AEC
(scripts/build_inter_aec.py) and then the WOFF2 files. --check verifies the
package against the manifest without fontTools.
"""

import hashlib
import io
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "harmonization/sources/font-runtime"
FONTS = ROOT / "crates/openaec-ui/assets/fonts"
LICENCES = ROOT / "crates/openaec-ui/licenses"
WEB = ROOT / "web"

# file -> (CSS family, weight, licence file). The family names match the tokens
# (`--oa-font-*`) and `openaec_ui::fonts`.
PACKAGE = {
    "Inter-Regular.ttf": ("Inter", 400, "Inter-OFL.txt"),
    "Inter-Medium.ttf": ("Inter", 500, "Inter-OFL.txt"),
    "Inter-SemiBold.ttf": ("Inter", 600, "Inter-OFL.txt"),
    "SpaceGrotesk-Medium.ttf": ("Space Grotesk", 500, "SpaceGrotesk-OFL.txt"),
    "SpaceGrotesk-Bold.ttf": ("Space Grotesk", 700, "SpaceGrotesk-OFL.txt"),
    "JetBrainsMono-Regular.ttf": ("JetBrains Mono", 400, "JetBrainsMono-OFL.txt"),
    # Inter with tabular figures and I/l disambiguation frozen (issue #28), for
    # numbers in tables, number fields and reports.
    "InterAEC-Regular.ttf": ("Inter AEC", 400, "Inter-OFL.txt"),
    "InterAEC-Medium.ttf": ("Inter AEC", 500, "Inter-OFL.txt"),
    "InterAEC-SemiBold.ttf": ("Inter AEC", 600, "Inter-OFL.txt"),
}

# Fonts made from another file in the package, by scripts/build_inter_aec.py.
DERIVED = {
    "InterAEC-Regular.ttf": "Inter-Regular.ttf",
    "InterAEC-Medium.ttf": "Inter-Medium.ttf",
    "InterAEC-SemiBold.ttf": "Inter-SemiBold.ttf",
}

# Fallback fonts for characters the fonts above lack (issue #25): Greek and
# Ĳ from Noto Sans, the diameter sign ⌀ from Noto Sans Symbols. Rust and CSS
# put them after every family, so no computer falls back to its own fonts.
FALLBACK = {
    "NotoSans-Regular.ttf": ("Noto Sans", 400, "NotoSans-OFL.txt"),
    "NotoSansSymbols-Regular.ttf": ("Noto Sans Symbols", 400, "NotoSansSymbols-OFL.txt"),
}

# Weights the tokens use (400, 500, 600, 700) that no file has yet: the browser
# then picks the nearest file. Listed so the gap stays visible.
MISSING = ["Inter 700", "Space Grotesk 400", "Space Grotesk 600", "JetBrains Mono 500"]


def name_table(data):
    """Reads nameID 1 (family), 2 (style) and 5 (version) from a TTF."""
    num_tables = struct.unpack(">H", data[4:6])[0]
    for i in range(num_tables):
        tag, _, offset, _ = struct.unpack(">4sIII", data[12 + 16 * i: 28 + 16 * i])
        if tag != b"name":
            continue
        _, count, strings = struct.unpack(">HHH", data[offset: offset + 6])
        names = {}
        for j in range(count):
            platform, encoding, _, name_id, length, at = struct.unpack(">HHHHHH", data[offset + 6 + 12 * j: offset + 18 + 12 * j])
            raw = data[offset + strings + at: offset + strings + at + length]
            # Windows Unicode names are UTF-16BE; keep the first one per id.
            if platform == 3 and encoding in (0, 1) and name_id not in names:
                names[name_id] = raw.decode("utf-16-be")
        return names
    return {}


def woff2(data):
    """Compresses a TTF to WOFF2 with fontTools and brotli (deterministic)."""
    from fontTools.ttLib import TTFont

    font = TTFont(io.BytesIO(data), recalcTimestamp=False)
    font.flavor = "woff2"
    out = io.BytesIO()
    font.save(out)
    return out.getvalue()


def main():
    check = "--check" in sys.argv[1:]
    if not check:
        sys.path.insert(0, str(RUNTIME))
        try:
            import brotli  # noqa: F401
            import fontTools  # noqa: F401
        except ImportError:
            print("fontTools en brotli ontbreken: python -m pip install --target harmonization/sources/font-runtime -r scripts/requirements-fonts.txt")
            return 1
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_inter_aec

        if build_inter_aec.main() != 0:
            return 1
    on_disk = sorted(p.name for p in FONTS.glob("*.ttf"))
    if on_disk != sorted({**PACKAGE, **FALLBACK}):
        print(f"Fontbestanden en PACKAGE verschillen: op schijf {on_disk}")
        return 1

    writes = {}

    def entries(files):
        out = []
        for file, (family, weight, licence) in files.items():
            data = (FONTS / file).read_bytes()
            names = name_table(data)
            assert (LICENCES / licence).exists(), f"Licentie ontbreekt: {licence}"
            compressed = WEB / "fonts" / (Path(file).stem + ".woff2")
            if check:
                packed = compressed.read_bytes() if compressed.exists() else b""
            else:
                packed = woff2(data)
            writes[compressed] = packed
            entry = {
                "file": file,
                "family": family,
                "weight": weight,
                "style": "normal",
                "name": f"{names.get(1, '?')} {names.get(2, '')}".strip(),
                "version": names.get(5, "?"),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "licence": f"licenses/{licence}",
                "woff2": {"file": compressed.name, "bytes": len(packed), "sha256": hashlib.sha256(packed).hexdigest()},
            }
            if file in DERIVED:
                source = (FONTS / DERIVED[file]).read_bytes()
                entry["derived_from"] = {
                    "file": DERIVED[file],
                    "sha256": hashlib.sha256(source).hexdigest(),
                    "features": ["ss04", "tnum"],
                    "script": "scripts/build_inter_aec.py",
                }
            out.append(entry)
            writes[WEB / "fonts" / file] = data
            # The review copy in assets/fonts mirrors the crate (scripts/check_portable_ui.py).
            writes[ROOT / "assets/fonts" / file] = data
            writes[WEB / "fonts" / licence] = (LICENCES / licence).read_bytes()
        return out

    fonts = entries(PACKAGE)
    fallback = entries(FALLBACK)

    manifest = {
        "about": "Fontpakket van OpenAEC UI 0.4 (issues #24, #25 en #28). Gemaakt door scripts/build_font_package.py; niet met de hand aanpassen.",
        "licence": "SIL Open Font License 1.1 voor alle fonts",
        "fonts": fonts,
        "fallback": fallback,
        "missing_weights": MISSING,
    }
    manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    writes[FONTS / "manifest.json"] = manifest_bytes
    # The review copy in assets/fonts mirrors the crate (scripts/check_portable_ui.py).
    writes[ROOT / "assets/fonts/manifest.json"] = manifest_bytes

    css = [
        "/* OpenAEC UI 0.4 fonts for web apps (issues #24 and #28).",
        " * Generated by scripts/build_font_package.py from crates/openaec-ui/assets/fonts.",
        " * Do not edit by hand. The same files as the Rust library; no Google Fonts, works offline.",
        " * WOFF2 first, the TTF for browsers without it. Inter AEC is Inter with tabular figures",
        " * and a distinct I and l. Licences: web/fonts/*-OFL.txt (SIL Open Font License 1.1). */",
    ]
    for font in fonts + fallback:
        css.append(
            f"@font-face {{ font-family: \"{font['family']}\"; font-style: normal; font-weight: {font['weight']}; "
            f"font-display: swap; src: url(\"fonts/{font['woff2']['file']}\") format(\"woff2\"), url(\"fonts/{font['file']}\") format(\"truetype\"); }}"
        )
    writes[WEB / "openaec-fonts.css"] = ("\n".join(css) + "\n").encode("utf-8")

    stale = [p for p, data in writes.items() if not p.exists() or p.read_bytes() != data]
    extra = [p for p in (WEB / "fonts").glob("*") if p not in writes] if (WEB / "fonts").exists() else []
    if check:
        if stale or extra:
            first = (stale + extra)[0].relative_to(ROOT).as_posix()
            print(f"Fontpakket verouderd, draai scripts/build_font_package.py: {len(stale) + len(extra)} bestanden, bijvoorbeeld {first}")
            return 1
        print(f"Fontpakket actueel: {len(fonts)} fonts en {len(fallback)} terugvalfonts, {sum(f['bytes'] for f in fonts + fallback) // 1024} kB TTF, {sum(f['woff2']['bytes'] for f in fonts + fallback) // 1024} kB WOFF2, gelijk in crate en web")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(writes[path])
    for path in extra:
        path.unlink()
    print(f"Fontpakket: {len(fonts)} fonts en {len(fallback)} terugvalfonts, {len(stale)} bestanden bijgewerkt, {len(extra)} verwijderd")
    for f in fonts + fallback:
        print(f"  {f['file']}: {f['name']}, {f['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
