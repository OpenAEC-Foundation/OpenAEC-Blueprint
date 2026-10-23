#!/usr/bin/env python3
"""Extract only SVG constants called by the pinned Pile Plan Studio ribbon."""
import hashlib
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "pile-plan-studio"
PIN = json.loads((ROOT / "harmonization/repositories/pile-plan-studio.json").read_text())["commit"]
BASE = "apps/pile-plan-studio/src/components/template/ribbon/"
SOURCE = ROOT / "harmonization/references/pile-plan-studio" / BASE
DEFINITIONS = SOURCE / "icons.ts"
RIBBON = SOURCE / "Ribbon.tsx"
OUT = ROOT / "harmonization/inline-ui-icons/pile-plan-studio"
OUT.mkdir(parents=True, exist_ok=True)

# These names are ribbon groups and application states, not guessed from the
# SVG shapes. The JSX call sites below are the source of truth for inclusion.
CONTEXT = {
    "projectIcon": ("Plan · Project", "Opent projectinformatie"),
    "loadPointIcon": ("Plan · Inspecteren", "Opent rechterpaneel voor paallocaties"),
    "cptIcon": ("Plan · Inspecteren", "Opent rechterpaneel voor sonderingen"),
    "lassoIcon": ("Plan · Selectie", "Schakelt lasso-selectie in of uit"),
    "settingsIcon": ("Plan · Instellingen", "Drie knoppen voor afzonderlijke instellingenpanelen"),
    "lockIcon": ("Plan · Vergrendeling", "Zichtbaar vóór bewerken van vergrendelingen"),
    "applyIcon": ("Plan · Vergrendeling", "Alleen tijdens bewerken van vergrendelingen"),
    "removeIcon": ("Plan · Vergrendeling", "Alleen tijdens bewerken van vergrendelingen"),
    "unlockIcon": ("Plan · Vergrendeling", "Alleen tijdens bewerken van vergrendelingen"),
    "optimizeIcon": ("Plan · Optimalisatie", "Opent ILP-optimalisatiepaneel"),
    "gridIcon": ("Weergave · Raster", "Toont of verbergt het raster"),
    "tipLevelRegionsIcon": ("Weergave · Regio's", "Toont of verbergt puntniveauregio's"),
    "groupsIcon": ("Weergave · Regio's", "Toont of verbergt paalpuntgroepen"),
    "explorerPanelIcon": ("Weergave · Vensters", "Toont of verbergt de verkenner"),
    "propertiesPanelIcon": ("Weergave · Vensters", "Toont of verbergt eigenschappen"),
}

source = DEFINITIONS.read_text()
ribbon = RIBBON.read_text()
defined = {}
for match in re.finditer(r"export const (\w+)\s*=\s*`(<svg.*?</svg>)`", source):
    name, svg = match.groups()
    assert name not in defined
    defined[name] = {"svg": svg, "line": source.count("\n", 0, match.start()) + 1}
uses = {}
for match in re.finditer(r"\bicon=\{(\w+)\}", ribbon):
    name = match.group(1)
    uses.setdefault(name, []).append(ribbon.count("\n", 0, match.start()) + 1)
assert len(defined) == 20, len(defined)
assert set(uses) == set(CONTEXT) <= set(defined), (sorted(set(uses) - set(CONTEXT)), sorted(set(CONTEXT) - set(uses)))
assert len(uses) == 15

items = []
for name in CONTEXT:
    details = defined[name]
    svg = details["svg"]
    portable_svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    asset = OUT / f"{name}.svg"
    asset.write_text(portable_svg + "\n")
    group, behavior = CONTEXT[name]
    items.append({
        "name": name,
        "group": group,
        "behavior": behavior,
        "definition": BASE + "icons.ts",
        "definition_line": details["line"],
        "usage": BASE + "Ribbon.tsx",
        "usage_lines": uses[name],
        "source_sha256": hashlib.sha256(svg.encode()).hexdigest(),
        "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "svg": f"inline-ui-icons/{REPO}/{name}.svg",
    })

index = {
    "repository": REPO,
    "commit": PIN,
    "scope": "currently called RibbonButton SVG constants in Plan and Weergave tabs",
    "count": len(items),
    "defined_count": len(defined),
    "unused_in_ribbon": sorted(set(defined) - set(uses)),
    "icons": items,
}
(ROOT / "harmonization/pile-inline-ui-icons.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

def samples(path: str) -> str:
    return "".join(f'<img src="{escape(path)}" width="{size}" height="{size}" alt="">' for size in (16, 24, 32))

cards = []
for item in items:
    definition_url = f"https://github.com/OpenAEC-Foundation/{REPO}/blob/{PIN}/{item['definition']}#L{item['definition_line']}"
    use_url = f"https://github.com/OpenAEC-Foundation/{REPO}/blob/{PIN}/{item['usage']}#L{item['usage_lines'][0]}"
    asset = "../harmonization/" + item["svg"]
    cards.append(f'''<article data-group="{escape(item['group'])}"><div class="meta"><span>{escape(item['group'])}</span><code>{escape(item['name'])}</code></div>
      <div class="samples">{samples(asset)}</div><p>{escape(item['behavior'])}</p><div class="links"><a href="{escape(definition_url)}">Definitie ↗</a><a href="{escape(use_url)}">UI-aanroep ↗</a></div></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pile Plan · werkelijk gebruikte linticonen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f1}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:23px max(22px,calc((100vw - 1370px)/2))}header a{color:#ffc184}h1{font-size:29px;margin:12px 0 6px}header p{margin:0;max-width:1030px;color:#dddde3}main{max-width:1410px;margin:auto;padding:22px}.note{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:19px}.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:13px 0}.controls select{font:inherit;padding:8px 10px;border:1px solid #b8b8c0;background:white}.controls output{color:#707078}.theme{margin:15px 0 22px}.theme h2{font-size:20px;margin:0 0 10px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:11px}article{background:#fff;border:1px solid #d9d9df;padding:14px;min-width:0}.meta{display:flex;justify-content:space-between;align-items:baseline;gap:6px;min-height:35px}.meta span{color:#ab5700;font-size:11px}.meta code{font-size:11px;color:#5a5a63}.samples{height:47px;display:flex;align-items:center;gap:18px}.samples img{display:block}article p{min-height:35px;margin:6px 0;color:#666672}.links{display:flex;gap:14px}.links a,footer a{color:#a55100}.dark{background:#303039;padding:15px}.dark h2{color:white}.dark article{background:#42424b;border-color:#686872;color:white}.dark .meta code,.dark article p{color:#d1d1d8}.dark .meta span,.dark a{color:#ffbd71}.dark img{filter:invert(1)}article[hidden]{display:none}footer{color:#666;margin:22px 0}
</style><header><a href="review.html">← Hoofdreview</a><h1>Pile Plan · vijftien echte linticonen</h1><p>De bron op commit ffe979d bevat twintig SVG-constanten in icons.ts. Alleen vijftien worden door de actieve Plan- en Weergave-ribbon als knopicoon aangeroepen. Definitie en concrete UI-aanroep zijn afzonderlijk gelinkt.</p></header><main><div class="note"><strong>Bronselectie.</strong> infoIcon, ifcImportIcon, pencilIcon, filterCheckIcon en searchIcon hebben in deze ribbon geen knopaanroep en tellen hier niet mee. Vergrendelingsiconen zijn voorwaardelijke toestanden; settingsIcon bedient drie afzonderlijke instellingenknoppen. De bronvormen zijn nog geen geharmoniseerde Rust-iconen.</div><div class="controls"><label for="group">Groep</label><select id="group"><option value="">Alle groepen</option>'''
for group in dict.fromkeys(item["group"] for item in items):
    page += f'<option>{escape(group)}</option>'
page += '</select><output id="count"></output></div><section class="theme"><h2>Light · 16 / 24 / 32 px</h2><div class="grid">' + "".join(cards) + '</div></section><section class="theme dark"><h2>Forge · 16 / 24 / 32 px</h2><div class="grid">' + "".join(cards) + '</div></section><p class="note"><strong>Betekenisbesluiten.</strong> Projectinformatie gebruikt in de bron een mapvorm, maar opent geen bestand. Het raster is een weergaveschakelaar en lijkt semantisch op het gedeelde Grid-icoon. De CPT-knop opent een paneel; de Geotechniek-sonderingknop plaatst een symbool. Deze opdrachten worden eerst naast elkaar beoordeeld voordat één Rust-vorm wordt gekozen.</p>'
page += '<footer><a href="../harmonization/pile-inline-ui-icons.json">Gestructureerde index met SHA-256</a> · <a href="style-repo-pile-ribbon-wide-forge.png">Complete native Plan-ribbon</a> · <a href="style-repo-pile-view-forge.png">Native Weergave-ribbon</a></footer></main><script>const select=document.getElementById("group"),cards=[...document.querySelectorAll("article")],count=document.getElementById("count");function update(){let shown=0;for(const card of cards){card.hidden=!!select.value&&card.dataset.group!==select.value;shown+=!card.hidden}count.textContent=`${shown/2} / 15 vormen per thema`}select.onchange=update;update();</script></html>'
(ROOT / "design/pile-inline-icon-review.html").write_text(page)
print(f"Pile ribbon: {len(items)} used SVG definitions, {len(index['unused_in_ribbon'])} unused in ribbon")
