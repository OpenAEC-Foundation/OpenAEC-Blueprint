#!/usr/bin/env python3
"""Extract only source-proven UI icons embedded in BCF Platform components."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "harmonization/references/openaec-bcf-platform/frontend/src/components/shell"
OUT = ROOT / "harmonization/inline-ui-icons/openaec-bcf-platform"
COMMIT = "e98fb97f5f23bc9c9f3b80de18acd721440f7597"
PREFIX = "frontend/src/components/shell/"

# An icon definition is counted only when the pinned UI component renders it.
GROUPS = [
    ("icons.ts", "Ribbon.tsx", "icon", {
        "iconNewProject": "ribbon-new-project", "iconImportBcf": "ribbon-import-bcf",
        "iconExportBcf": "ribbon-export-bcf", "iconNewIssue": "ribbon-new-issue",
    }),
    ("icons.ts", "CloudPanel.tsx", "icon", {
        "iconCloudUpload": "cloud-upload", "iconCloudDownload": "cloud-download",
    }),
    ("AppBar.tsx", "AppBar.tsx", "icon", {
        "iconSave": "title-save", "iconSettingsSmall": "title-settings",
    }),
    ("Backstage.tsx", "Backstage.tsx", "ICONS", {
        "new": "file-new", "open": "file-open", "save": "file-save",
        "saveAs": "file-save-as", "close": "file-close", "preferences": "file-preferences",
        "about": "file-about", "exit": "file-exit", "server": "file-server",
        "file": "file-document",
    }),
]


def definition(source: str, name: str, kind: str) -> tuple[int, str]:
    if kind == "ICONS":
        pattern = rf"^\s*{re.escape(name)}: '(<svg[^\n]*?</svg>)',?\s*$"
    else:
        pattern = rf"^(?:export )?const {re.escape(name)} = [`'](<svg[^\n]*?</svg>)[`'];?\s*$"
    matches = list(re.finditer(pattern, source, re.M))
    assert len(matches) == 1, f"Expected one definition for {name}"
    match = matches[0]
    return source.count("\n", 0, match.start()) + 1, match.group(1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for source_name, usage_name, kind, names in GROUPS:
        source = (BASE / source_name).read_text()
        usage = (BASE / usage_name).read_text()
        for name, filename in names.items():
            line, svg = definition(source, name, kind)
            reference = f"ICONS.{name}" if kind == "ICONS" else name
            usage_lines = [i for i, text in enumerate(usage.splitlines(), 1)
                           if reference in text and not text.lstrip().startswith("import ")
                           and (source_name != usage_name or i != line)]
            assert usage_lines, f"No UI use for {name}"
            assert svg.count("<svg") == 1 and svg.count("</svg>") == 1
            if "xmlns=" not in svg.split(">", 1)[0]:
                svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
            ET.fromstring(svg)
            (OUT / f"{filename}.svg").write_text(svg + "\n")
            records.append({
                "name": filename,
                "identifier": name,
                "source": PREFIX + source_name,
                "source_line": line,
                "usage": PREFIX + usage_name,
                "usage_lines": usage_lines,
                "sha256": hashlib.sha256((svg + "\n").encode()).hexdigest(),
                "svg": f"inline-ui-icons/openaec-bcf-platform/{filename}.svg",
            })
    assert len(records) == 18
    index = {"repository": "openaec-bcf-platform", "commit": COMMIT,
             "scope": "UI-rendered inline SVG definitions only; not standalone assets or all SVG occurrences",
             "count": len(records), "icons": records,
             "excluded_unused_definitions": ["iconSettings", "iconAbout", "iconClose", "iconCloud"]}
    (ROOT / "harmonization/bcf-inline-ui-icons.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    cards = []
    for record in records:
        source_url = f"https://github.com/OpenAEC-Foundation/openaec-bcf-platform/blob/{COMMIT}/{record['source']}#L{record['source_line']}"
        use_url = f"https://github.com/OpenAEC-Foundation/openaec-bcf-platform/blob/{COMMIT}/{record['usage']}#L{record['usage_lines'][0]}"
        icon = "../harmonization/" + record["svg"]
        cards.append(f'<article><div class="samples"><span><img src="{icon}" width="16" height="16">16</span><span><img src="{icon}" width="24" height="24">24</span><span><img src="{icon}" width="32" height="32">32</span></div><b>{escape(record["name"])}</b><small>{escape(record["identifier"])}</small><p><a href="{source_url}">Vorm</a> · <a href="{use_url}">UI-gebruik</a></p></article>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BCF · inline UI-iconen</title><style>
:root{font:14px Inter,system-ui,sans-serif;color:#34343e;background:#f9f9f8}*{box-sizing:border-box}body{margin:0;padding:32px;max-width:1480px;margin:auto}h1{font-size:30px;margin:0 0 8px}p{line-height:1.55}a{color:#b35b00}.lead{max-width:960px;color:#666670}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:26px}article{background:white;border:1px solid #dddddf;border-radius:5px;padding:16px}article b,article small{display:block}article small{color:#73737b;margin-top:4px}.samples{display:flex;align-items:center;gap:15px;height:72px}.samples span{display:inline-flex;align-items:center;gap:5px;color:#888;font-size:11px}.samples img{color:#32323a}.grid.dark{background:#303036;border-radius:5px;padding:14px}.dark article{background:#3e3e46;border-color:#64646d;color:#f1f1f2}.dark small,.dark .samples span{color:#bdbdc5}.dark .samples img{filter:invert(1)}.dark a{color:#ffac43}
</style><main><p><a href="review.html">← Overzicht</a></p><h1>BCF Platform · inline UI-iconen</h1><p class="lead">Deze 18 vectoren staan als SVG-string of JSX in de vastgelegde broncode en worden aantoonbaar door ribbon, bestandsweergave, titelbalk of cloudpaneel gebruikt. Vier gedefinieerde maar niet aangeroepen iconen blijven buiten de telling. Dit is een bronreview; de vormen zijn nog niet vrijgegeven als canonieke Rust-iconen.</p><h2>Licht · 16, 24 en 32 px</h2><div class="grid">'''
    html += "".join(cards) + '</div><h2>Donker · dezelfde bronvormen</h2><div class="grid dark">' + "".join(cards) + '</div><p class="lead">De bron gebruikt <code>currentColor</code>; alleen een ontbrekende SVG-namespace is aan de losse reviewbestanden toegevoegd. Provenance en hashes staan in <a href="../harmonization/bcf-inline-ui-icons.json">de index</a>.</p></main></html>'
    (ROOT / "design/bcf-inline-icon-review.html").write_text(html)
    print(f"Extracted {len(records)} source-proven inline UI icons")


if __name__ == "__main__":
    main()
