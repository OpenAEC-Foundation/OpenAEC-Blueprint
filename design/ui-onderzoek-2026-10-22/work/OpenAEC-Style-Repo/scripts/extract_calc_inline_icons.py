#!/usr/bin/env python3
"""Preserve Open Calc Studio's actually rendered inline ribbon SVGs."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "harmonization/references/open-calc-studio/src/components/ribbon"
OUT = ROOT / "harmonization/inline-ui-icons/open-calc-studio"
COMMIT = "b47042704efa388d95eb59ce77d23aeb5ee0e44c"
PREFIX = "src/components/ribbon/"
USAGE = ["HomeTab.tsx", "OfferteTab.tsx", "RapportageTab.tsx", "TekstopmaakTab.tsx"]


def kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def main() -> None:
    source = (BASE / "icons.ts").read_text()
    pattern = re.compile(r"^export const (\w+)\s*=\s*`(<svg[^\n]*?</svg>)`;?\s*$", re.M)
    definitions = list(pattern.finditer(source))
    assert len(definitions) == 47, "Pinned icon definition count changed"
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for match in definitions:
        identifier, svg = match.groups()
        source_line = source.count("\n", 0, match.start()) + 1
        uses = []
        for filename in USAGE:
            for line_number, line in enumerate((BASE / filename).read_text().splitlines(), 1):
                if (re.search(rf"\b{identifier}\b", line)
                    and not re.fullmatch(rf"\s*{identifier},?\s*", line)
                    and not line.lstrip().startswith("import ")):
                    uses.append({"path": PREFIX + filename, "line": line_number})
        assert uses, f"No rendered-use evidence for {identifier}"
        if "xmlns=" not in svg.split(">", 1)[0]:
            svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        ET.fromstring(svg)
        filename = kebab(identifier.removesuffix("Icon")) + ".svg"
        target = OUT / filename
        assert not target.exists() or target.read_text() == svg + "\n"
        target.write_text(svg + "\n")
        records.append({
            "name": filename.removesuffix(".svg"),
            "identifier": identifier,
            "source": PREFIX + "icons.ts", "source_line": source_line,
            "usage": uses,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "svg": "inline-ui-icons/open-calc-studio/" + filename,
        })
    assert len({record["name"] for record in records}) == 47
    index = {"repository": "open-calc-studio", "commit": COMMIT,
             "scope": "47 UI-rendered ribbon SVG definitions, excluding other code or technical SVGs",
             "count": len(records), "icons": records}
    (ROOT / "harmonization/calc-inline-ui-icons.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    cards = []
    for record in records:
        shape = f"https://github.com/OpenAEC-Foundation/open-calc-studio/blob/{COMMIT}/{record['source']}#L{record['source_line']}"
        first_use = record["usage"][0]
        used = f"https://github.com/OpenAEC-Foundation/open-calc-studio/blob/{COMMIT}/{first_use['path']}#L{first_use['line']}"
        icon = "../harmonization/" + record["svg"]
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(record["name"])}</b><small>{escape(record["identifier"])}</small><p><a href="{shape}">Vorm</a> · <a href="{used}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Calc · inline UI-iconen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:960px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>Open Calc Studio · inline UI-iconen</h1><p class="lead">47 SVG-vormen uit de brongepinde <code>icons.ts</code> hebben elk minstens één concrete aanroep in Home, Offerte, Rapportage of Tekstopmaak. De review vergelijkt hun originele vorm op 16/24/32 px in licht en donker. Dit is nog geen goedkeuring voor de Rust-crate; vormfamilies en betekenis moeten vóór canonisering worden geharmoniseerd.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead">Alleen een ontbrekende SVG-namespace is aan de losse reviewbestanden toegevoegd. <a href="../harmonization/calc-inline-ui-icons.json">De index</a> legt vorm, UI-gebruik en hash vast.</p></main></html>'
    (ROOT / "design/calc-inline-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} source-proven Open Calc inline UI icons")


if __name__ == "__main__":
    main()
