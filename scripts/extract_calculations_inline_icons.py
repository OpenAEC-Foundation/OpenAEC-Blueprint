#!/usr/bin/env python3
"""Extract the eight calcIcons.ts vectors wired into the current Calc ribbon."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "harmonization/references/Open-Calculations-Studio/packages/desktop/src/components/ribbon"
OUT = ROOT / "harmonization/inline-ui-icons/Open-Calculations-Studio"
COMMIT = "21d218c996d09b92018ad21b730c883c665dc035"
PREFIX = "packages/desktop/src/components/ribbon/"


def kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def main() -> None:
    source = (BASE / "calcIcons.ts").read_text()
    calc_tab = (BASE / "CalcTab.tsx").read_text()
    ifc_tab = (BASE / "IfcTab.tsx").read_text()
    legacy = (BASE / "icons.ts").read_text()
    assert 'from "./calcIcons"' in calc_tab
    assert "./icons" not in calc_tab
    assert "ribbon-groups" in ifc_tab and "<RibbonButton" not in ifc_tab
    pattern = re.compile(r"export const (\w+)\s*=\s*svg\(\s*`([\s\S]*?)`,\s*\);")
    definitions = list(pattern.finditer(source))
    assert len(definitions) == 28, "Pinned calcIcons definitions changed"
    legacy_names = re.findall(r"export const (\w+)\s*=\s*`<svg", legacy)
    assert len(legacy_names) == 42, "Pinned legacy definitions changed"
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    excluded = []
    for match in definitions:
        identifier, body = match.groups()
        button_pattern = re.compile(rf"\bicon\s*=\s*\{{\s*{re.escape(identifier)}\s*\}}")
        use_lines = [i for i, line in enumerate(calc_tab.splitlines(), 1)
                     if button_pattern.search(line)]
        if not use_lines:
            excluded.append(identifier)
            continue
        # calcIcons.ts constructs every icon through this fixed wrapper.
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
               'fill="none" stroke="currentColor" stroke-width="1.6" '
               'stroke-linecap="round" stroke-linejoin="round">' + body + '</svg>')
        ET.fromstring(svg)
        filename = kebab(identifier.removesuffix("Icon")) + ".svg"
        target = OUT / filename
        target.write_text(svg + "\n")
        records.append({
            "name": filename.removesuffix(".svg"), "identifier": identifier,
            "source": PREFIX + "calcIcons.ts",
            "source_line": source.count("\n", 0, match.start()) + 1,
            "usage": PREFIX + "CalcTab.tsx", "usage_lines": use_lines,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "svg": "inline-ui-icons/Open-Calculations-Studio/" + filename,
        })
    assert len(records) == 8 and len(excluded) == 20
    index = {
        "repository": "Open-Calculations-Studio", "commit": COMMIT,
        "scope": "SVGs constructed by calcIcons.ts and passed to visible CalcTab RibbonButton controls",
        "count": len(records), "icons": records,
        "excluded_unwired_calc_icons": excluded,
        "excluded_legacy_icons_ts_count": len(legacy_names),
        "excluded_legacy_reason": "CalcTab imports ./calcIcons and IfcTab renders an empty ribbon; legacy icons.ts is not imported by these active ribbon tabs",
    }
    (ROOT / "harmonization/calculations-inline-ui-icons.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    cards = []
    for record in records:
        shape = f"https://github.com/OpenAEC-Foundation/Open-Calculations-Studio/blob/{COMMIT}/{record['source']}#L{record['source_line']}"
        used = f"https://github.com/OpenAEC-Foundation/Open-Calculations-Studio/blob/{COMMIT}/{record['usage']}#L{record['usage_lines'][0]}"
        icon = "../harmonization/" + record["svg"]
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(record["name"])}</b><small>{escape(record["identifier"])}</small><p><a href="{shape}">Vorm</a> · <a href="{used}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Calculations · inline UI-iconen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:960px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>Open Calculations Studio · inline UI-iconen</h1><p class="lead">De huidige Calc-ribbon gebruikt acht vectoren uit <code>calcIcons.ts</code> als knopicoon. Twintig andere definities in dat bestand zijn niet aan de huidige knoppen gekoppeld. De oudere <code>icons.ts</code> heeft 42 definities, maar wordt door deze linttabs niet geïmporteerd; IFC toont bewust geen lintacties. Daarom worden die definities niet als gebruikte UI-iconen geteld. De acht bronvormen zijn op 16/24/32 px in licht en donker te beoordelen, nog zonder canonieke goedkeuring.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead">De SVG-wrapper uit <code>calcIcons.ts</code> is letterlijk toegepast, met alleen een namespace voor de zelfstandige bestanden. <a href="../harmonization/calculations-inline-ui-icons.json">De index</a> bewaart alle uitgesloten namen, bronregels, gebruiksregels en hashes.</p></main></html>'
    (ROOT / "design/calculations-inline-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} used vectors; excluded {len(excluded)} staged and {len(legacy_names)} legacy definitions")


if __name__ == "__main__":
    main()
