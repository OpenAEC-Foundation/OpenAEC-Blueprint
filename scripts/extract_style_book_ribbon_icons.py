#!/usr/bin/env python3
"""Index SVGs actually rendered by the pinned Tauri Style Book ribbon route."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / "harmonization/repositories/OpenAEC-style-book.json").read_text())["commit"]
BASE = "project-templates/Tauri+React/src/components/ribbon"
REF = ROOT / "harmonization/references/OpenAEC-style-book"
SRC = REF / BASE
ASSETS = ROOT / "harmonization/inline-ui-icons/style-book-tauri-ribbon"
ASSETS.mkdir(parents=True, exist_ok=True)
CATALOG = f"{BASE}/icons.ts"
CATALOG_COPY = "packages/ribbon/src/icons.ts"
catalog = (REF / CATALOG).read_text()
assert catalog == (REF / CATALOG_COPY).read_text(), "template/package icon catalogue drift"
definitions = {}
for match in re.finditer(r"export const (\w+Icon)\s*=\s*`(<svg.*?</svg>)`;", catalog):
    definitions[match.group(1)] = (match.group(2), CATALOG, catalog.count("\n", 0, match.start()) + 1)
assert len(definitions) == 42

ribbon = (SRC / "Ribbon.tsx").read_text()
assert 'const TABS = ["home", "ifc", "viewer", "report"]' in ribbon
assert 'case "viewer": return null' in ribbon
assert "<ExtensionsTab" not in ribbon
active_tabs = {"Home": "HomeTab.tsx", "IFC": "IfcTab.tsx", "Report": "ReportTab.tsx"}
usage = []
for group, filename in active_tabs.items():
    body = (SRC / filename).read_text()
    for match in re.finditer(r"\bicon=\{(\w+Icon)\}", body):
        usage.append((match.group(1), group, f"{BASE}/{filename}", body.count("\n", 0, match.start()) + 1))
assert len(usage) == 38 and len({item[0] for item in usage}) == 38

report = (SRC / "ReportTab.tsx").read_text()
local = {}
for match in re.finditer(r"const (\w+Icon)\s*=\s*`(<svg.*?</svg>)`;", report):
    local[match.group(1)] = (match.group(2), f"{BASE}/ReportTab.tsx", report.count("\n", 0, match.start()) + 1)
assert len(local) == 5
assert set(name for name, *_ in usage) == (set(definitions) - {
    "viewerLoadIcon", "viewerOrbitIcon", "viewerSectionIcon", "viewerMeasureIcon", "viewerFitIcon", "viewerWireframeIcon",
    "extensionBrowseIcon", "extensionInstallIcon", "extensionManageIcon",
}) | set(local)
unused = sorted(set(definitions) - {name for name, *_ in usage})
assert len(unused) == 9

candidates = {
    "settingsIcon": ("settings.svg", "Dezelfde instellingenroute; de Rust-kern gebruikt nu ook een tandwiel. Beeldregelaars behouden een eigen Controls-vorm."),
    "helpIcon": ("help.svg", "Zelfde hulpfunctie; lijnvorm en kleine maat nog vergelijken."),
    "undoIcon": ("undo.svg", "Dezelfde terugdraai-opdracht; pijlbaan verschilt."),
    "redoIcon": ("redo.svg", "Dezelfde herhaal-opdracht; pijlbaan verschilt."),
    "ifcImportIcon": ("import.svg", "IFC-bestandsimport tegenover generieke import; context behouden."),
    "ifcExportIcon": ("export.svg", "IFC-bestandsexport tegenover generieke export; context behouden."),
}


def normalize(svg: str) -> str:
    result = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1) + "\n"
    ET.fromstring(result)
    return result


records = []
for name, group, usage_file, usage_line in usage:
    raw, definition, definition_line = (definitions | local)[name]
    asset = ASSETS / f"{name.removesuffix('Icon')}.svg"
    asset.write_text(normalize(raw))
    candidate = candidates.get(name)
    records.append({
        "name": name, "tab": group, "definition": definition, "definition_line": definition_line,
        "usage_file": usage_file, "usage_line": usage_line,
        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "svg": f"inline-ui-icons/style-book-tauri-ribbon/{asset.name}",
        "shared_candidate": f"../crates/openaec-ui/assets/icons/{candidate[0]}" if candidate else None,
        "candidate_assessment": candidate[1] if candidate else None,
        "replacement_candidate": "../crates/openaec-ui/assets/icons/saveas.svg" if name == "reportPreviewIcon" else None,
        "review_note": ("Bron gebruikt het oogpictogram voor Opslaan als; dit is geen passende SaveAs-kandidaat."
                        if name == "reportPreviewIcon" else
                        "Klembord-kopie; niet dezelfde opdracht als document dupliceren." if name == "copyIcon" else
                        "De knop heet Over; niet dezelfde opdracht als Hulp." if name == "infoIcon" else None),
    })

index = {
    "repository": "OpenAEC-style-book", "commit": PIN,
    "scope": "Tauri+React ribbon route: Home, IFC and Report buttons; Viewer returns null; Extensions not registered",
    "catalogue_definitions": len(definitions), "local_report_definitions": len(local),
    "count": len(records), "unused_catalogue_definitions": unused,
    "catalogue_duplicate": CATALOG_COPY, "icons": records,
}
(ROOT / "harmonization/style-book-tauri-ribbon-ui-icons.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")


def sample(path: str) -> str:
    return "".join(f'<img src="{escape(path)}" width="{n}" height="{n}" alt="">' for n in (16, 24, 32))


cards = []
for item in records:
    url = f"https://github.com/OpenAEC-Foundation/OpenAEC-style-book/blob/{PIN}/{item['usage_file']}#L{item['usage_line']}"
    candidate = item["shared_candidate"]
    candidate_html = (f'<div class="candidate">Rust-vergelijking {sample(candidate)}</div><p class="assessment">{escape(item["candidate_assessment"])}</p>' if candidate else "")
    if item["replacement_candidate"]:
        candidate_html = f'<div class="candidate">Vervangvoorstel SaveAs {sample(item["replacement_candidate"])}</div>'
    note = f'<p class="warning">{escape(item["review_note"])}</p>' if item["review_note"] else ""
    cards.append(f'''<article data-tab="{escape(item['tab'])}"><div class="meta"><span>{escape(item['tab'])}</span><code>{escape(item['name'])}</code></div>
<div class="samples">{sample('../harmonization/' + item['svg'])}</div><div class="hash" title="SHA-256: {item['asset_sha256']}">SHA-256 · {item['asset_sha256'][:12]}</div>{candidate_html}{note}<a href="{escape(url)}">UI-aanroep ↗</a></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Style Book Tauri · linticonen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f1}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(22px,calc((100vw - 1370px)/2))}header a{color:#ffc184}h1{font-size:29px;margin:10px 0 5px}header p{max-width:1000px;color:#dddde3;margin:0}main{max-width:1410px;margin:auto;padding:22px}.note{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:17px}.controls{display:flex;align-items:center;gap:10px;margin:12px 0 20px}.controls button{border:1px solid #b8b8c0;background:white;padding:7px 12px;font:inherit;cursor:pointer}.controls button.active{background:#d97706;border-color:#d97706;color:white}.controls output{color:#74747c;margin-left:auto}.theme{margin-bottom:22px}.theme h2{font-size:20px;margin:0 0 10px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:11px}article{background:white;border:1px solid #d9d9df;padding:13px;min-height:145px}.meta{display:flex;align-items:baseline;justify-content:space-between;gap:6px;color:#a85706;font-size:11px}.meta code{color:#595962}.samples{height:55px;display:flex;align-items:center;gap:17px}.samples img{display:block}.hash{font:10px ui-monospace,monospace;color:#9a9aa1;margin:-3px 0 8px}article a,footer a{color:#a55100}.candidate{border-top:1px solid #e2e2e6;display:flex;align-items:center;justify-content:space-between;color:#99620f;font-size:10px;padding:5px 0}.candidate img{margin-right:4px}.assessment{font-size:10px;color:#666672;margin:0 0 8px}.warning{font-size:11px;color:#9d4215;margin:0 0 8px}.dark{background:#303039;padding:16px}.dark h2{color:white}.dark article{background:#42424b;border-color:#686872;color:white}.dark .meta,.dark article a,.dark .candidate{color:#ffbd71}.dark .meta code,.dark .hash,.dark .assessment{color:#d1d1d8}.dark .candidate{border-color:#666670}.dark img{filter:invert(1)}article[hidden]{display:none}footer{color:#777;margin:22px 0}
</style><header><a href="review.html">← Hoofdreview</a><h1>Style Book Tauri · 38 echte lintvormen</h1><p>Brongecontroleerde knoppen uit Home, IFC en Report op commit dfdcd41. Voor elke vorm de aanroep, SVG-hash en Light/Forge-voorbeelden op 16, 24 en 32 px.</p></header><main><div class="note"><strong>Routebewijs.</strong> De catalogus bevat 42 definities; daarvan worden er 33 door actieve linttabbladen aangeroepen. Report definieert vijf extra vormen. Viewer retourneert in Ribbon.tsx <code>null</code> en Extensions is niet geregistreerd, zodat hun negen catalogusiconen buiten deze UI-telling blijven. Het package en Tauri-sjabloon bevatten byte-identieke iconcatalogi. Het oogicoon bij Report ‘Opslaan als’ is een betekenisfout; de gedeelde SaveAs-vorm staat ernaast als vervangvoorstel. Klembord-Kopiëren en document-Dupliceren blijven afzonderlijke handelingen.</div><div class="controls"><button class="active" data-tab="">Alle</button><button data-tab="Home">Home</button><button data-tab="IFC">IFC</button><button data-tab="Report">Report</button><output id="count"></output></div>
'''
cards_html = "".join(cards)
page += f'<section class="theme"><h2>Light</h2><div class="grid">{cards_html}</div></section><section class="theme dark"><h2>Forge</h2><div class="grid">{cards_html}</div></section>'
page += '<footer><a href="../harmonization/style-book-tauri-ribbon-ui-icons.json">Gestructureerde bronindex</a> · <a href="pile-pointcloud-explorer-review.html">Gedeelde verkennerbesluiten</a></footer></main><script>const controls=[...document.querySelectorAll("[data-tab]:is(button)")],cards=[...document.querySelectorAll("article")],out=document.getElementById("count");function choose(tab){controls.forEach(b=>b.classList.toggle("active",b.dataset.tab===tab));let n=0;cards.forEach(c=>{c.hidden=!!tab&&c.dataset.tab!==tab;n+=!c.hidden});out.textContent=`${n/2} / 38 vormen per thema`}controls.forEach(b=>b.onclick=()=>choose(b.dataset.tab));choose("");</script></html>'
(ROOT / "design/style-book-tauri-ribbon-icon-review.html").write_text(page)
print("Style Book Tauri ribbon: 42 catalogue + 5 local definitions, 38 active UI forms, 9 catalogue definitions excluded")
