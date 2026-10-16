#!/usr/bin/env python3
"""Review source-used Pile Plan explorer, import and legend UI icon forms."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / "harmonization/repositories/pile-plan-studio.json").read_text())["commit"]
REF = ROOT / "harmonization/references/pile-plan-studio/apps/pile-plan-studio/src"
OUT = ROOT / "harmonization/inline-ui-icons/pile-plan-studio-workarea"
OUT.mkdir(parents=True, exist_ok=True)
EXPLORER = "components/domain/pile-plans/PilePlanExplorer.tsx"
NOTICE = "components/domain/pile-plans/legend-editor/LegendConflictNotice.tsx"
ROW = "components/domain/pile-plans/legend-editor/LegendEditorItemRow.tsx"
IMPORT = "components/domain/imports/ProjectImportPanel.tsx"
RIBBON_ICONS = "components/template/ribbon/icons.ts"


def at(path: str, line: int) -> str:
    source = (REF / path).read_text().splitlines()
    assert "<svg" in source[line - 1], (path, line)
    chunk = "\n".join(source[line - 1:])
    chunk = chunk[chunk.index("<svg"):]
    return chunk[:chunk.index("</svg>") + len("</svg>")]


def clean(svg: str) -> str:
    svg = re.sub(r"<svg(?=\s)", '<svg xmlns="http://www.w3.org/2000/svg"', svg, count=1)
    svg = re.sub(r'\s+(?:aria-hidden|className)="[^"]*"', "", svg)
    svg = svg.replace("strokeWidth=", "stroke-width=").replace("strokeLinecap=", "stroke-linecap=")
    svg = svg.replace("strokeLinejoin=", "stroke-linejoin=")
    if 'stroke="' not in svg:
        svg = svg.replace("<svg ", '<svg fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ', 1)
    ET.fromstring(svg)
    return svg + "\n"


cases = [
    ("explorer-expand", "Verkenner", "Uitklappen", EXPLORER, 200, [94, 113, 200]),
    ("explorer-collapse", "Verkenner", "Inklappen", EXPLORER, 200, [94, 113, 200]),
    ("explorer-edit", "Verkenner", "Paalplan hernoemen", EXPLORER, 231, [160, 231]),
    ("explorer-copy", "Verkenner", "Paalplan dupliceren", EXPLORER, 232, [161, 232]),
    ("explorer-delete", "Verkenner", "Paalplan verwijderen", EXPLORER, 233, [165, 233]),
    ("explorer-warning", "Verkenner", "Ontbrekende kosten", EXPLORER, 234, [150, 234]),
    ("explorer-plus", "Verkenner", "Nieuw paalplan", EXPLORER, 235, [174, 235]),
    ("legend-info", "Legenda", "Dubbele codering of gebruik buiten scope", NOTICE, 78, [78]),
]

records = []
for name, group, meaning, path, line, uses in cases:
    raw = at(path, line)
    source_hash = hashlib.sha256(raw.encode()).hexdigest()
    if name.startswith("explorer-") and name.endswith(("expand", "collapse")):
        assert 'd={expanded ? "m4 6 4 4 4-4" : "m6 4 4 4-4 4"}' in raw
        raw = raw.replace('d={expanded ? "m4 6 4 4 4-4" : "m6 4 4 4-4 4"}',
                          'd="m6 4 4 4-4 4"' if name.endswith("expand") else 'd="m4 6 4 4 4-4"')
    if name == "legend-info":
        assert re.sub(r'\s+', '', raw) == re.sub(r'\s+', '', at(ROW, 188))
    asset = OUT / f"{name}.svg"
    asset.write_text(clean(raw))
    records.append({"name": name, "group": group, "meaning": meaning,
                    "definition": path, "definition_line": line,
                    "usage_lines": uses, "source_sha256": source_hash,
                    "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
                    "svg": f"inline-ui-icons/pile-plan-studio-workarea/{name}.svg"})
    if name == "legend-info":
        records[-1]["other_usage_sites"] = [{"file": ROW, "line": 188}]

ribbon = (REF / RIBBON_ICONS).read_text()
panel = (REF / IMPORT).read_text()
for name, symbol, meaning, uses in (
    ("import-ifc", "ifcImportIcon", "Bestanden kiezen of vervangen", [198, 240, 415, 420]),
    ("import-help", "infoIcon", "Hulp bij paalkopniveau", [171]),
):
    match = re.search(r"export const " + symbol + r" = `(<svg.*?</svg>)`;", ribbon)
    assert match and symbol in panel
    line = ribbon.count("\n", 0, match.start()) + 1
    asset = OUT / f"{name}.svg"
    asset.write_text(clean(match.group(1)))
    records.append({"name": name, "group": "Import", "meaning": meaning,
                    "definition": RIBBON_ICONS, "definition_line": line,
                    "usage_file": IMPORT, "usage_lines": uses,
                    "source_sha256": hashlib.sha256(match.group(1).encode()).hexdigest(),
                    "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
                    "svg": f"inline-ui-icons/pile-plan-studio-workarea/{name}.svg"})

assert len(re.findall(r"<svg\b", (REF / EXPLORER).read_text())) == 6
assert len(re.findall(r"<svg\b", (REF / NOTICE).read_text())) == 1
assert len(re.findall(r"<svg\b", (REF / ROW).read_text())) == 1
index = {"repository": "pile-plan-studio", "commit": PIN, "count": len(records),
         "scope": "actual explorer, legend and import UI positions; chevron states separate, duplicate legend info merged",
         "source_svg_occurrences": 8, "imported_ribbon_constants_newly_ui_used": 2,
         "icons": records}
(ROOT / "harmonization/pile-workarea-ui-icons.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

cards = []
for item in records:
    usage_file = item.get("usage_file", item["definition"])
    url = f"https://github.com/OpenAEC-Foundation/pile-plan-studio/blob/{PIN}/apps/pile-plan-studio/src/{usage_file}#L{item['usage_lines'][0]}"
    imgs = "".join(f'<img src="../harmonization/{escape(item["svg"])}" width="{n}" height="{n}" alt="">' for n in (16, 24, 32))
    cards.append(f'<article><div class="eyebrow">{escape(item["group"])} · <code>{escape(item["name"])}</code></div><div class="samples">{imgs}</div><p>{escape(item["meaning"])}</p><a href="{escape(url)}">UI-bron ↗</a></article>')
cards_html = "".join(cards)
page = f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pile Plan · werkgebiediconen</title><style>
:root{{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f1}}*{{box-sizing:border-box}}body{{margin:0}}header{{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(22px,calc((100vw - 1370px)/2))}}header a{{color:#ffc184}}h1{{font-size:29px;margin:11px 0 5px}}header p{{max-width:930px;color:#dddde3;margin:0}}main{{max-width:1410px;margin:auto;padding:22px}}.note{{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:23px}}h2{{font-size:20px;margin:0 0 12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}}article{{background:white;border:1px solid #d9d9df;padding:15px}}.eyebrow{{color:#ab5700;font-size:11px;min-height:27px;display:flex;justify-content:space-between;gap:6px}}.eyebrow code{{color:#62626b}}.samples{{height:50px;display:flex;align-items:center;gap:19px}}.samples img{{display:block}}article p{{min-height:38px;color:#666672;margin:6px 0}}article a,footer a{{color:#a55100}}.dark{{background:#303039;margin-top:23px;padding:18px}}.dark h2{{color:white}}.dark article{{background:#42424b;border-color:#686872;color:white}}.dark .eyebrow,.dark a{{color:#ffbd71}}.dark .eyebrow code,.dark article p{{color:#d1d1d8}}.dark img{{filter:invert(1)}}footer{{color:#666;margin:22px 0}}
</style><header><a href="review.html">← Hoofdreview</a><h1>Pile Plan · 10 werkgebiediconen</h1><p>Verkenner, legenda en importpaneel · brongebruik op commit {PIN[:7]} · 16 / 24 / 32 px in Light en Forge.</p></header><main><div class="note"><strong>Afbakening.</strong> Zes SVG-definities in de verkenner leveren zeven zichtbare toestandsvormen op: de groepschevron staat open of dicht. De twee identieke legenda-informatieiconen tellen eenmaal. Het importpaneel gebruikt twee bestaande SVG-constanten uit icons.ts die niet door het lint werden aangeroepen; deze staan hier wel omdat het paneel ze toont. Het zijn tien unieke vormen, geen tien losse bestanden uit de bron.</div><section><h2>Light</h2><div class="grid">{cards_html}</div></section><section class="dark"><h2>Forge</h2><div class="grid">{cards_html}</div></section><footer><a href="../harmonization/pile-workarea-ui-icons.json">Gestructureerde index met SHA-256</a> · <a href="pile-inline-icon-review.html">Lint</a> · <a href="pile-backstage-icon-review.html">Bestand</a></footer></main></html>'''
(ROOT / "design/pile-workarea-icon-review.html").write_text(page)
print("Pile work area: 8 inline SVG occurrences + 2 imported constants => 10 unique UI forms")
