#!/usr/bin/env python3
"""Index UI SVGs from Pile Plan Backstage; omit the 1024 px OA brand mark."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / "harmonization/repositories/pile-plan-studio.json").read_text())["commit"]
SOURCE_REL = "apps/pile-plan-studio/src/components/template/backstage/Backstage.tsx"
SOURCE = ROOT / "harmonization/references/pile-plan-studio" / SOURCE_REL
ASSETS = ROOT / "harmonization/inline-ui-icons/pile-plan-studio-backstage"
ASSETS.mkdir(parents=True, exist_ok=True)

# Each row is an actual UI position. The OA logomark at line 270 is branding,
# and the identical arrow at 495 is captured as a second use of line 472.
CASES = [
    (19, "menu-open", "Bestand-menu", "Openen"),
    (20, "menu-save", "Bestand-menu", "Opslaan · alleen met save-commando"),
    (21, "menu-save-as", "Bestand-menu", "Opslaan als · alleen met save-commando"),
    (22, "menu-export", "Bestand-menu", "Exporteren"),
    (23, "menu-import", "Bestand-menu", "Importeren en Pile Plan importeren"),
    (24, "menu-preferences", "Bestand-menu", "Instellingen openen"),
    (25, "menu-about", "Bestand-menu", "Over deze app"),
    (26, "menu-exit", "Bestand-menu", "Afsluiten · alleen met save-commando"),
    (121, "menu-back", "Bestand-menu", "Terug naar werkruimte"),
    (312, "about-website", "Over", "Website-link"),
    (323, "about-github", "Over", "GitHub-link"),
    (362, "recent-ifc", "Recent", "IFC-bestandstype"),
    (364, "recent-report", "Recent", "Rapportbestandstype"),
    (366, "recent-project", "Recent", "Projectbestandstype"),
    (368, "recent-other", "Recent", "Overig bestandstype"),
    (442, "recent-remove", "Recent", "Verwijder één recent bestand"),
    (458, "open-choose-project", "Openen", "Kies lokaal project"),
    (472, "open-project-arrow", "Openen", "Pijl bij project kiezen en voorbeeld openen"),
    (484, "open-sample", "Openen", "Open voorbeeldproject"),
    (588, "export-project", "Export", "Projectexportkaart"),
    (593, "export-table", "Export", "Tabelexportkaart"),
    (598, "export-rows", "Export", "Rijexportkaart"),
    (611, "export-download", "Export", "Downloadactie op exportkaart"),
]
SHARED_CANDIDATES = {
    "menu-open": ("open", "open.svg"),
    "menu-save": ("save", "save.svg"),
    "menu-save-as": ("save-as", "saveas.svg"),
    "menu-export": ("export", "export.svg"),
    "menu-import": ("import", "import.svg"),
    "menu-preferences": ("settings", "settings.svg"),
    "menu-back": ("back", "back.svg"),
}

source = SOURCE.read_text()
occurrences = {}
for match in re.finditer(r"<svg\b[\s\S]*?</svg>", source):
    line = source.count("\n", 0, match.start()) + 1
    assert line not in occurrences, line
    occurrences[line] = match.group()
expected = {line for line, *_ in CASES} | {270, 495}
assert set(occurrences) == expected, (sorted(set(occurrences) - expected), sorted(expected - set(occurrences)))
assert occurrences[472] == occurrences[495]

def clean(svg: str) -> str:
    svg = re.sub(r"<svg(?=\s)", '<svg xmlns="http://www.w3.org/2000/svg"', svg, count=1)
    for react, standard in (("strokeWidth", "stroke-width"), ("strokeLinecap", "stroke-linecap"),
                            ("strokeLinejoin", "stroke-linejoin")):
        svg = svg.replace(react + "=", standard + "=")
    ET.fromstring(svg)
    return svg + "\n"


def usage(line: int, name: str) -> list[int]:
    if name.startswith("menu-") and name != "menu-back":
        key = name.removeprefix("menu-").replace("save-as", "saveAs").replace("preferences", "preferences")
        key = "import" if name == "menu-import" else key
        found = [source.count("\n", 0, m.start()) + 1
                 for m in re.finditer(r"icon=\{ICONS\." + re.escape(key) + r"\}", source)]
        assert found, name
        return found
    if name.startswith("recent-") and name != "recent-remove":
        assert "typeIcon(file.type)" in source
        return [source.count("\n", 0, source.index("typeIcon(file.type)")) + 1]
    if name == "open-project-arrow":
        return [472, 495]
    return [line]


records = []
for line, name, group, meaning in CASES:
    raw = occurrences[line]
    asset = ASSETS / f"{name}.svg"
    asset.write_text(clean(raw))
    records.append({
        "name": name, "group": group, "meaning": meaning,
        "definition": SOURCE_REL, "definition_line": line,
        "usage_lines": usage(line, name),
        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "svg": f"inline-ui-icons/pile-plan-studio-backstage/{name}.svg",
        "shared_candidate": SHARED_CANDIDATES.get(name, (None, None))[0],
        "candidate_svg": (f"../crates/openaec-ui/assets/icons/{SHARED_CANDIDATES[name][1]}"
                          if name in SHARED_CANDIDATES else None),
    })

index = {
    "repository": "pile-plan-studio", "commit": PIN,
    "scope": "visible or conditionally visible Backstage command, file-type, and link SVGs",
    "svg_occurrences": len(occurrences), "count": len(records),
    "excluded_branding": {"source": SOURCE_REL, "line": 270, "reason": "1024 px OA logomark"},
    "duplicate_usage": {"name": "open-project-arrow", "lines": [472, 495]},
    "icons": records,
}
(ROOT / "harmonization/pile-backstage-ui-icons.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

def samples(path: str) -> str:
    return "".join(f'<img src="{escape(path)}" width="{n}" height="{n}" alt="">' for n in (16, 24, 32))


cards = []
for item in records:
    ref = f"https://github.com/OpenAEC-Foundation/pile-plan-studio/blob/{PIN}/{SOURCE_REL}#L{item['usage_lines'][0]}"
    candidate = item["candidate_svg"]
    candidate_html = (f'<div class="candidate"><span>Rust-kandidaat · {escape(item["shared_candidate"])}</span>'
                      f'<img src="{escape(candidate)}" width="24" height="24" alt=""></div>') if candidate else ''
    cards.append(f'''<article data-group="{escape(item['group'])}"><div class="meta"><span>{escape(item['group'])}</span><code>{escape(item['name'])}</code></div>
      <div class="samples">{samples('../harmonization/' + item['svg'])}</div><p>{escape(item['meaning'])}</p>{candidate_html}<a href="{escape(ref)}">UI-aanroep ↗</a></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pile Plan · Bestand-iconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f1}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:23px max(22px,calc((100vw - 1370px)/2))}header a{color:#ffc184}h1{font-size:29px;margin:12px 0 6px}header p{margin:0;max-width:1030px;color:#dddde3}main{max-width:1410px;margin:auto;padding:22px}.note{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:19px}.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:13px 0}.controls select{font:inherit;padding:8px 10px;border:1px solid #b8b8c0;background:white}.controls output{color:#707078}.theme{margin:15px 0 22px}.theme h2{font-size:20px;margin:0 0 10px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:11px}article{background:#fff;border:1px solid #d9d9df;padding:14px;min-width:0}.meta{display:flex;justify-content:space-between;align-items:baseline;gap:6px;min-height:35px}.meta span{color:#ab5700;font-size:11px}.meta code{font-size:11px;color:#5a5a63}.samples{height:47px;display:flex;align-items:center;gap:18px}.samples img{display:block}article p{min-height:35px;margin:6px 0;color:#666672}.candidate{border-top:1px solid #e3e3e7;padding:6px 0;display:flex;align-items:center;justify-content:space-between;min-height:38px}.candidate span{font-size:10px;color:#9a560b}.candidate img{display:block;margin-right:12px}article a,footer a{color:#a55100}.dark{background:#303039;padding:15px}.dark h2{color:white}.dark article{background:#42424b;border-color:#686872;color:white}.dark .meta code,.dark article p{color:#d1d1d8}.dark .meta span,.dark a,.dark .candidate span{color:#ffbd71}.dark .candidate{border-color:#666670}.dark img{filter:invert(1)}article[hidden]{display:none}footer{color:#666;margin:22px 0}
</style><header><a href="review.html">← Hoofdreview</a><h1>Pile Plan · 23 Bestand-iconen</h1><p>Werkelijk gebruikte of toestand-afhankelijke SVG-vormen uit Backstage.tsx op de gepinde broncommit ffe979d. Bekijk elke vorm op 16, 24 en 32 px in Light en Forge.</p></header><main><div class="note"><strong>Afbakening.</strong> Van 25 SVG-voorkomens is het 1024 px OA-beeldmerk branding. Dezelfde pijl wordt op twee Openen-kaarten gebruikt en staat eenmaal in de index met beide aanroepregels. Opslaan en Afsluiten hangen af van de desktopcommando’s; recente bestandstypen hangen af van de bestandslijst. Zeven menuacties hebben een semantisch passende Rust-kandidaat. Over en Afsluiten betekenen iets anders dan Help en een document sluiten; bestandstypen blijven eigen pictogrammen. De voorstellen zijn nog niet in de Pile Plan-app ingebouwd.</div><div class="controls"><label for="group">Groep</label><select id="group"><option value="">Alle groepen</option>'''
for group in dict.fromkeys(item["group"] for item in records):
    page += f'<option>{escape(group)}</option>'
page += '</select><output id="count"></output></div><section class="theme"><h2>Light · 16 / 24 / 32 px</h2><div class="grid">' + "".join(cards) + '</div></section><section class="theme dark"><h2>Forge · 16 / 24 / 32 px</h2><div class="grid">' + "".join(cards) + '</div></section>'
page += '<footer><a href="../harmonization/pile-backstage-ui-icons.json">Gestructureerde index met SHA-256</a> · <a href="pile-inline-icon-review.html">Pile Plan-linticonen</a> · <a href="backstage-review.html">Gedeelde Bestand-layout</a></footer></main><script>const select=document.getElementById("group"),cards=[...document.querySelectorAll("article")],count=document.getElementById("count");function update(){let shown=0;for(const card of cards){card.hidden=!!select.value&&card.dataset.group!==select.value;shown+=!card.hidden}count.textContent=`${shown/2} / 23 vormen per thema`}select.onchange=update;update();</script></html>'
(ROOT / "design/pile-backstage-icon-review.html").write_text(page)
print(f"Pile Backstage: {len(occurrences)} SVG occurrences, {len(records)} UI forms, 1 logo excluded, 1 duplicate use")
