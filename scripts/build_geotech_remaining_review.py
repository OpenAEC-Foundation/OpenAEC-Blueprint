#!/usr/bin/env python3
"""Compare three source-pinned Geotechniek drawing meanings with reviewed Rust assets."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = json.loads((ROOT / "design/geotech-icon-crosswalk.json").read_text())
by_name = {item["name"]: item for item in index["icons"]}
cases = [
    ("tekening-tag", "geotech.coordinate-tag", "RD-coördinaat plaatsen",
     "Kruisdraad en centrum blijven bij 16 px apart leesbaar; coördinaatlabel is context, geen tekst in het pictogram.", "geotech-coordinate-tag.svg"),
    ("tekening-vlak", "drawing.polygon", "Gesloten vlak tekenen",
     "Gesloten, licht gevuld veelhoekprofiel; niet verwarren met OpenCAD Polyline, dat een open lijn tekent.", "drawing-polygon.svg"),
    ("tekening-frame", "drawing.svg-frame", "SVG-kader laden",
     "Binnenhoek onderscheidt deze invoeropdracht van OpenCAD Underlay Frames, een weergave-instelling.", "drawing-svg-frame.svg"),
]


def image(path: str, size: int) -> str:
    assert (ROOT / "design" / path).exists(), path
    return f'<img src="{escape(path)}" width="{size}" height="{size}" alt="">'


cards = []
for name, meaning, label, rationale, draft in cases:
    source = by_name[name]
    assert source["status"] == "adopted-domain" and source["usage_lines"]
    source_path = "../harmonization/" + source["source_svg"]
    large = "../crates/openaec-ui/assets/domain-icons/" + draft
    small = "../crates/openaec-ui/assets/domain-icons-small/" + draft
    ref = ("https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/"
           f"{index['commit']}/{source['source']}#L{source['usage_lines'][0]}")
    src_images = "".join(image(source_path, size) for size in (16, 24, 32))
    draft_images = image(small, 16) + image(large, 24) + image(large, 32)
    cards.append(f'''<article><div class="meta"><span class="tag">{escape(meaning)}</span><a href="{escape(ref)}">UI-aanroep ↗</a></div>
      <h2>{escape(label)}</h2><p>{escape(rationale)}</p><div class="pair"><div><h3>Bron · {escape(name)}</h3><div class="samples">{src_images}</div></div>
      <div><h3>Rust · 16/24/32 px</h3><div class="samples">{draft_images}</div></div></div></article>''')

out = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · resterende tekensymbolen</title>
<style>:root{font:14px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f3f3f2}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(22px,calc((100vw - 1320px)/2))}header a{color:#ffc17a}h1{font-size:28px;margin:12px 0 6px}header p{margin:0;max-width:900px;color:#d8d8df}main{max-width:1360px;margin:auto;padding:22px}.note{padding:12px 15px;background:#fff8ee;border-left:3px solid #d97706;margin-bottom:20px}.theme{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:22px}.theme h2{grid-column:1/-1;margin:4px 0 0;font-size:20px}article{background:#fff;border:1px solid #d5d5d9;padding:15px;min-width:0}.meta{display:flex;align-items:center;justify-content:space-between;gap:5px}.tag{font-size:11px;color:#ae5b00;background:#fff3e0;padding:3px 6px}.meta a,footer a{color:#a75600;font-size:12px}article h2{font-size:17px;margin:12px 0 5px}article p{color:#666670;min-height:62px;margin:0 0 15px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.pair>div{background:#f8f8f8;border:1px solid #e0e0e3;padding:8px;min-width:0}h3{font-size:11px;color:#6b6b73;font-weight:500;margin:0 0 9px;min-height:28px}.samples{display:flex;align-items:center;gap:11px;min-height:34px}.samples img{display:block}.dark{background:#303039;padding:14px}.dark>h2{color:white}.dark article{background:#414149;border-color:#64646e;color:white}.dark article p,.dark h3{color:#d1d1d8}.dark .pair>div{background:#4a4a53;border-color:#6a6a74}.dark img{filter:invert(1)}.dark .tag{background:#6b4a2d;color:#ffe0b7}.dark a{color:#ffbd6f}footer{padding:0 3px 18px;color:#666}@media(max-width:900px){.theme{grid-template-columns:1fr}.theme h2{grid-column:auto}article p{min-height:0}}</style>
<header><a href="review.html">← Hoofdreview</a><h1>Geotechniek · drie beoordeelde tekensymbolen</h1><p>Bronvorm en geharmoniseerde Rust-vorm op 16, 24 en 32 px, in lichte en donkere omgeving.</p></header>
<main><div class="note">Alle drie de knoppen hebben een concrete UI-aanroep in de gepinde Geotechniek-bron. De kleine vormen en de onderscheiden betekenissen zijn beoordeeld vóór opname als <code>DomainIcon</code>.</div><section class="theme"><h2>Light</h2>'''
out += "".join(cards) + '</section><section class="theme dark"><h2>Forge</h2>' + "".join(cards) + '</section>'
out += '<footer><a href="geotech-icon-crosswalk.html">Alle 54 bronvormen</a> · <a href="geotech-native-source-ribbon-review.html">Native Rust-ribbon</a></footer></main></html>'
(ROOT / "design/geotech-remaining-icon-review.html").write_text(out)
print("Reviewed drafts:", len(cases))
