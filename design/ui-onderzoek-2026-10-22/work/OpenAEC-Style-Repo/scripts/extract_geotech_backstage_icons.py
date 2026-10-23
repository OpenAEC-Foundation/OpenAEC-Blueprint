#!/usr/bin/env python3
"""Extract only Geotechniek Backstage SVG strings passed to live menu items."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "apps/desktop/src/components/backstage/Backstage.tsx"
PINNED = ROOT / "harmonization/references/open-geotechniek-studio" / SOURCE
OUT = ROOT / "harmonization/inline-ui-icons/open-geotechniek-studio"
COMMIT = "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"


def main() -> None:
    source = PINNED.read_text()
    block = source.split("const ICONS = {", 1)[1].split("\n};", 1)[0]
    entries = re.findall(r"^\s*(\w+):\s*'(<svg.*?</svg>)',?", block, re.M)
    assert len(entries) == 11
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for key, original in entries:
        def_line = next(i for i, line in enumerate(source.splitlines(), 1)
                        if re.search(rf"^\s*{key}:\s*'<svg", line))
        uses = [i for i, line in enumerate(source.splitlines(), 1)
                if re.search(rf"\bicon=\{{ICONS\.{key}\}}", line)]
        assert uses, f"No UI menu use: {key}"
        svg = original.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        ET.fromstring(svg)
        name = "backstage-" + re.sub(r"(?<!^)(?=[A-Z])", "-", key).lower()
        target = OUT / (name + ".svg")
        target.write_text(svg + "\n")
        records.append({
            "name": name, "identifier": "ICONS." + key, "source": SOURCE,
            "source_line": def_line, "usage": SOURCE, "usage_lines": uses,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "svg": "inline-ui-icons/open-geotechniek-studio/" + target.name,
        })
    index = {
        "repository": "open-geotechniek-studio", "commit": COMMIT,
        "scope": "Backstage ICONS strings actually supplied to MenuItem",
        "count": len(records), "icons": records,
        "excluded_other_inline_svg": "JSX arrows, logo and other embedded vectors require separate usage classification",
    }
    (ROOT / "harmonization/geotech-backstage-ui-icons.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    cards = []
    for item in records:
        path = f"https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{COMMIT}/{SOURCE}"
        icon = "../harmonization/" + item["svg"]
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(item["name"])}</b><small>{escape(item["identifier"])}</small><p><a href="{path}#L{item["source_line"]}">Vorm</a> · <a href="{path}#L{item["usage_lines"][0]}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · Bestand-menu-iconen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:960px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>Open Geotechniek Studio · Bestand-menu</h1><p class="lead">Elf SVG-strings uit <code>Backstage.tsx</code> worden daadwerkelijk als icoon aan <code>MenuItem</code> doorgegeven. Deze review toont bronvormen op 16/24/32 px en lichte en donkere achtergrond. Overige SVG’s in dit bestand, waaronder een logo, zijn niet stilzwijgend als menu-iconen geteld. De vormen zijn nog geen canonieke Rust-iconen.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead"><a href="../harmonization/geotech-backstage-ui-icons.json">De index</a> legt definitie, menu-aanroep en hash vast.</p></main></html>'
    (ROOT / "design/geotech-backstage-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} used Geotechniek Backstage menu icons")


if __name__ == "__main__":
    main()
