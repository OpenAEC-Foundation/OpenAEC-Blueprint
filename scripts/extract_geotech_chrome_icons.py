#!/usr/bin/env python3
"""Review actually rendered JSX SVG controls in Geotechniek's window chrome."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "harmonization/references/open-geotechniek-studio/apps/desktop/src/components"
OUT = ROOT / "harmonization/inline-ui-icons/open-geotechniek-studio"
COMMIT = "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"
NAMES = {
    "TitleBar.tsx": [
        "branding-mark", "title-save", "title-undo", "title-redo", "title-print",
        "title-settings", "window-minimize", "window-restore", "window-maximize", "window-close",
    ],
    "DocumentBar.tsx": ["document-close", "document-add", "document-file", "document-folder"],
}
JSX_ATTRIBUTES = {
    "strokeWidth": "stroke-width", "strokeLinecap": "stroke-linecap",
    "strokeLinejoin": "stroke-linejoin", "fillRule": "fill-rule", "clipRule": "clip-rule",
}


def line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def ui_uses(source: str, name: str, svg_line: int) -> list[int]:
    lines = source.splitlines()
    if name == "document-file":
        return [i for i, line in enumerate(lines, 1) if "<FileIcon />" in line]
    if name == "document-folder":
        return [i for i, line in enumerate(lines, 1) if "<FolderIcon />" in line]
    if name == "document-close":
        return [i for i, line in enumerate(lines, 1) if 'className="document-tab-close"' in line]
    if name == "document-add":
        return [i for i, line in enumerate(lines, 1) if 'className="document-tab document-tab-add"' in line]
    before = "\n".join(lines[:svg_line])
    buttons = [line_number(before, match.start()) for match in re.finditer(r"<button\b", before)]
    assert buttons, name
    return [buttons[-1]]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, names in NAMES.items():
        source = (BASE / filename).read_text()
        forms = list(re.finditer(r"<svg\b[\s\S]*?</svg>", source))
        assert len(forms) == len(names), (filename, len(forms))
        for name, match in zip(names, forms):
            if name == "branding-mark":
                continue
            svg = match.group()
            for jsx, xml in JSX_ATTRIBUTES.items():
                svg = re.sub(rf"\b{jsx}=", f"{xml}=", svg)
            if "xmlns=" not in svg.split(">", 1)[0]:
                svg = re.sub(r"<svg\b", '<svg xmlns="http://www.w3.org/2000/svg"', svg, count=1)
            ET.fromstring(svg)
            target = OUT / (name + ".svg")
            target.write_text(svg + "\n")
            definition = line_number(source, match.start())
            uses = ui_uses(source, name, definition)
            assert uses, name
            records.append({
                "name": name,
                "source": f"apps/desktop/src/components/{filename}",
                "source_line": definition,
                "usage_lines": uses,
                "source_size": re.search(r'width="(\d+)"', match.group()).group(1),
                "interactive": name not in {"title-save", "title-undo", "title-redo", "title-print"},
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "svg": "inline-ui-icons/open-geotechniek-studio/" + target.name,
            })
    assert len(records) == 13
    index = {
        "repository": "open-geotechniek-studio", "commit": COMMIT,
        "scope": "Rendered titlebar and document-tab JSX SVG controls, including both maximize states",
        "count": len(records), "icons": records,
        "excluded_branding_svg_count": 1,
        "note": "Save, undo, redo and print quick-access buttons are visible but have no onClick handler in the pinned source",
    }
    (ROOT / "harmonization/geotech-chrome-ui-icons.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    cards = []
    for record in records:
        path = f"https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{COMMIT}/{record['source']}"
        icon = "../harmonization/" + record["svg"]
        badge = "Zichtbaar, nog zonder klikactie" if not record["interactive"] else "Bediening of toestandsicoon"
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(record["name"])}</b><small>Bronmaat {record["source_size"]} px · {badge}</small><p><a href="{path}#L{record["source_line"]}">Vorm</a> · <a href="{path}#L{record["usage_lines"][0]}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · titel- en documenticonen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:1000px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>Open Geotechniek Studio · titel- en documenticonen</h1><p class="lead">Dertien zichtbare UI-vormen uit <code>TitleBar.tsx</code> en <code>DocumentBar.tsx</code>, inclusief beide venster-maximalisatiestaten. Het CPT-beeldmerk in dezelfde titelbalk is branding en telt niet mee. De knoppen Opslaan, Ongedaan, Opnieuw en Afdrukken tonen wel een icoon, maar hebben in deze bron geen <code>onClick</code>-afhandeling. De maat onder elke naam is de bronmaat; 16/24/32 px dienen voor vergelijking. Dit zijn nog geen canonieke Rust-iconen.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead"><a href="../harmonization/geotech-chrome-ui-icons.json">De index</a> bewaart bronregel, UI-gebruik, originele maat en SHA-256.</p></main></html>'
    (ROOT / "design/geotech-chrome-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} visible chrome forms; excluded one branding SVG")


if __name__ == "__main__":
    main()
