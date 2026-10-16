#!/usr/bin/env python3
"""Extract Geotechniek's live ribbon-button SVGs, including concatenated strings."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "harmonization/references/open-geotechniek-studio/apps/desktop/src/components/ribbon"
OUT = ROOT / "harmonization/inline-ui-icons/open-geotechniek-studio"
COMMIT = "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"
PREFIX = "apps/desktop/src/components/ribbon/"
TABS = [
    ("StartTab.tsx", "start"),
    ("KaartTab.tsx", "kaart"),
    ("RapportTab.tsx", "rapport"),
    ("SonderingstekeningTab.tsx", "tekening"),
]


def kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    legacy = (BASE / "icons.ts").read_text()
    legacy_names = re.findall(r"export const (\w+)\s*=\s*`<svg", legacy)
    assert len(legacy_names) == 42
    records = []
    for filename, group in TABS:
        source = (BASE / filename).read_text()
        assert 'from "./icons"' not in source and "from './icons'" not in source
        pattern = re.compile(r"^const (\w+Icon)\s*=\s*([\s\S]*?);(?=\n)", re.M)
        for match in pattern.finditer(source):
            identifier, expression = match.groups()
            parts = re.findall(r"`([^`]*)`", expression)
            assert parts and all("${" not in part for part in parts), identifier
            svg = "".join(parts)
            assert svg.startswith("<svg ") and svg.endswith("</svg>")
            if "xmlns=" not in svg.split(">", 1)[0]:
                svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
            ET.fromstring(svg)
            uses = [i for i, line in enumerate(source.splitlines(), 1)
                    if re.search(rf"\bicon\s*=\s*\{{\s*{re.escape(identifier)}\s*\}}", line)]
            assert uses, f"Unwired definition in {filename}: {identifier}"
            name = group + "-" + kebab(identifier.removesuffix("Icon"))
            target = OUT / (name + ".svg")
            target.write_text(svg + "\n")
            records.append({
                "name": name, "identifier": identifier,
                "source": PREFIX + filename,
                "source_line": source.count("\n", 0, match.start()) + 1,
                "usage": PREFIX + filename, "usage_lines": uses,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "svg": "inline-ui-icons/open-geotechniek-studio/" + name + ".svg",
            })
    assert len(records) == 30, "Pinned UI icon count changed"
    assert len({r["name"] for r in records}) == 30
    index = {
        "repository": "open-geotechniek-studio", "commit": COMMIT,
        "scope": "Inline SVG definitions actually passed to RibbonButton in Start, Kaart, Rapport and Sonderingstekening tabs",
        "count": 30, "icons": records,
        "excluded_legacy_icons_ts_count": 42,
        "excluded_legacy_reason": "The four audited ribbon tabs define their own SVGs and do not import ./icons",
    }
    (ROOT / "harmonization/geotech-inline-ui-icons.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    cards = []
    for record in records:
        shape = f"https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{COMMIT}/{record['source']}#L{record['source_line']}"
        used = f"https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{COMMIT}/{record['usage']}#L{record['usage_lines'][0]}"
        icon = "../harmonization/" + record["svg"]
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(record["name"])}</b><small>{escape(record["identifier"])}</small><p><a href="{shape}">Vorm</a> · <a href="{used}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · inline UI-iconen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:960px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>Open Geotechniek Studio · inline UI-iconen</h1><p class="lead">Dertig bronvormen worden in de actieve tabs Start, Kaart, Rapport en Sonderingstekening als <code>RibbonButton</code>-icoon gebruikt. De 42 definities uit het oude generieke <code>icons.ts</code> worden door deze tabs niet geïmporteerd. Op 16/24/32 px en beide achtergronden zijn vooral de kleine geotechnische markeringen, PDF-tekst en CAD-bewerkglyfen ter beoordeling. Deze bronvormen zijn nog geen canonieke Rust-iconen.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead">De oorspronkelijke SVG-strings zijn exact samengevoegd; alleen de namespace is toegevoegd voor zelfstandige reviewbestanden. <a href="../harmonization/geotech-inline-ui-icons.json">De index</a> koppelt elke definitie aan een knop en bewaart de hash.</p></main></html>'
    (ROOT / "design/geotech-inline-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} live ribbon icons; excluded {len(legacy_names)} legacy definitions")


if __name__ == "__main__":
    main()
