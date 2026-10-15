#!/usr/bin/env python3
"""Build a source-traceable review of exact UI icon duplicates."""
from collections import defaultdict
from html import escape as e
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design'
records = json.loads((DESIGN / 'icon-review-data.json').read_text())['records']
groups = defaultdict(list)
for item in records:
    groups[item['sha256']].append(item)

DISTINCT = {
    ('actual-size.svg', 'area.svg'): ('PDF · werkelijke grootte / oppervlaktemeting', ('pdf-actual-size', 'pdf-area')),
    ('fit-page.svg', 'fullscreen.svg'): ('PDF · passend zoomen / schermvullend tonen', ('pdf-fit-page', 'pdf-fullscreen')),
    ('BAG3D.pushbutton', 'CityJSON.pushbutton'): ('GIS · BAG 3D / CityJSON', ('gis-bag3d', 'gis-cityjson')),
    ('BGT.pushbutton', 'BGT3D.pushbutton'): ('GIS · BGT / BGT 3D', ('gis-bgt', 'gis-bgt3d')),
    ('LuchtfotoTijdreis.pushbutton', 'StreetView.pushbutton'): ('GIS · historische luchtfoto / straatbeeld', ('gis-aerial-history', 'gis-street-view')),
    ('Locatie.pushbutton', 'Opschonen.pushbutton'): ('GIS · locatie / opschonen', ('gis-location', 'gis-cleanup')),
    ('opencad-icons/solid.svg', 'assets/icons/solid.svg'): ('CAD / Pointcloud · gebouwpaneel / shaded weergave', ('pointcloud-bag-panel', 'cad-shaded')),
    ('opencad-icons/sphere.svg', 'assets/icons/model/sphere.svg'): ('CAD / Pointcloud · EDL-weergave / bolprimitief', ('pointcloud-edl', 'cad-sphere')),
}

DISTINCT_REASONS = {
    'GIS · BAG 3D / CityJSON': 'BAG 3D haalt gebouwgeometrie op; CityJSON bedient een ander gegevensformaat. De identieke knopafbeelding verbergt het bronverschil.',
    'GIS · BGT / BGT 3D': 'De ene knop vraagt BGT-kaartgegevens, de andere een 3D-variant. De dimensie hoort in de vorm herkenbaar te zijn.',
    'GIS · historische luchtfoto / straatbeeld': 'Een historische luchtfotoreeks en een straatbeeld openen verschillende kaartbronnen en navigatiecontexten.',
    'GIS · locatie / opschonen': 'Locatie stelt plaatsinformatie in; Opschonen verwijdert of herstelt ongewenste gegevens. Dezelfde vorm suggereert ten onrechte dezelfde opdracht.',
    'PDF · passend zoomen / schermvullend tonen': 'Fit Page wijzigt de documentzoom; Fullscreen wijzigt de venstermodus. De bediening en terugweg verschillen.',
    'PDF · werkelijke grootte / oppervlaktemeting': 'Actual Size kiest een 1:1-weergave; Area start een meetgereedschap. Dit zijn aparte opdrachten in verschillende lintgroepen.',
    'CAD / Pointcloud · gebouwpaneel / shaded weergave': 'Pointcloud opent het 3D BAG-gebouwpaneel; CAD kiest Shaded als visuele stijl. Het gedeelde kubusbeeld staat voor andere acties.',
    'CAD / Pointcloud · EDL-weergave / bolprimitief': 'Pointcloud schakelt Eye Dome Lighting in; CAD maakt een bolprimitief. Een gedeelde bolvorm maakt renderinstelling en modelgeometrie onduidelijk.',
}

RELATED = {
    'Aantallen': 'Beide tellen family-instances per type; de deurstaat telt deuren, de kozijnstaat kozijnen en schrijft daarbij ook family-typewaarden.',
    'Config': 'Beide openen de configuratie van een staat met dezelfde profielgestuurde formulierbasis; deur- en kozijnvelden verschillen.',
    'Create': 'Beide plaatsen unieke typen op een geselecteerde wand: deuren respectievelijk kozijnen.',
    'Maatvoering': 'Beide plaatsen maatlijnen bij instances in de actieve view; de gebruikte referenties en aantallen verschillen.',
    'Rename': 'Beide hernoemen family types; de deurstaat volgt de 3BM-conventie, de kozijnstaat breedte- en hoogteparameters.',
    'Tag': 'Beide plaatsen tags onder instances; de bron kiest afzonderlijke deur- en kozijnfamilies en offsets.',
}

ADOPTED = {'pointcloud-bag-panel', 'pointcloud-edl', 'cad-shaded', 'cad-sphere'}
for stem in ADOPTED:
    for review_folder, crate_folder in (
        ('icon-collision-drafts', 'domain-icons'),
        ('icon-collision-drafts-small', 'domain-icons-small'),
    ):
        reviewed = DESIGN / review_folder / f'{stem}.svg'
        packaged = ROOT / 'crates/openaec-ui/assets' / crate_folder / f'{stem}.svg'
        assert reviewed.read_bytes() == packaged.read_bytes(), f'Review and Rust asset differ: {stem}'

def classify(items):
    paths = [item['path'] for item in items]
    for keys, (title, drafts) in DISTINCT.items():
        if all(any(key in path for path in paths) for key in keys):
            return 'distinct-action', title, drafts, DISTINCT_REASONS[title]
    if all('Deurstaat.panel' in path or 'Kozijnstaat.panel' in path for path in paths):
        action = Path(paths[0]).parent.name.replace('Deurstaat', '')
        key = action.replace('WindowTag.pushbutton', 'Tag').replace('Tag.pushbutton', 'Tag').replace('.pushbutton', '')
        return 'related-action', f'Bouwkunde · deurstaat / kozijnstaat · {action}', (), RELATED[key]
    raise ValueError(paths)

pairs = []
for sha, items in groups.items():
    if len(items) == 1:
        continue
    assert len(items) == 2
    kind, title, drafts, assessment = classify(items)
    for item in items:
        source = (DESIGN / item['preview']).resolve()
        assert source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == sha
    for stem in drafts:
        for folder in ('icon-collision-drafts', 'icon-collision-drafts-small'):
            ET.parse(DESIGN / folder / f'{stem}.svg')
    pairs.append(dict(sha256=sha, kind=kind, title=title, assessment=assessment, originals=items, drafts=list(drafts), adopted_drafts=[stem for stem in drafts if stem in ADOPTED]))
pairs.sort(key=lambda pair: (pair['kind'] != 'distinct-action', pair['title']))
assert len(pairs) == 14 and sum(pair['kind'] == 'distinct-action' for pair in pairs) == 8
(DESIGN / 'icon-collision-audit.json').write_text(json.dumps({
    'scope': 'SHA-256 collisions within 565 verified UI icon assets',
    'pair_count': 14, 'distinct_action_pairs': 8, 'related_action_pairs': 6, 'context_review_pairs': 0,
    'pairs': pairs,
}, indent=2, ensure_ascii=False) + '\n')

def tile(path, alt, size=24, dark=False):
    tone = 'dark' if dark else 'light'
    proposal = ' proposal' if path.startswith('icon-collision-drafts') else ''
    return f'<span class="tile s{size} {tone}{proposal}" title="{size} px · {tone}"><img src="{e(path, quote=True)}" alt="{e(alt, quote=True)}"></span>'

cards = []
for index, pair in enumerate(pairs, 1):
    sources = []
    for item in pair['originals']:
        name = Path(item['path']).parent.name if item['path'].endswith('icon.png') else Path(item['path']).name
        original_samples = ''.join(tile(item['preview'], name, size, dark) for size in (16, 24, 32) for dark in (False, True))
        sources.append(f'<article class="candidate"><div class="name"><strong>{e(name)}</strong><small>{e(item["repo"])}</small></div><div class="samples">{original_samples}</div><a href="{e(item["source"], quote=True)}">Broncode ↗</a><code>{e(item["path"])}</code></article>')
    drafts = []
    for stem in pair['drafts']:
        examples = ''.join(tile(f'icon-collision-drafts-small/{stem}.svg' if size == 16 else f'icon-collision-drafts/{stem}.svg', stem, size, dark) for size in (16, 24, 32) for dark in (False, True))
        phase = 'Rust-crate · domeinicoon' if stem in ADOPTED else 'vectorconcept'
        drafts.append(f'<article class="candidate"><div class="name"><strong>{e(stem.replace("-", " "))}</strong><small>{phase}</small></div><div class="samples">{examples}</div></article>')
    proposal = f'<div class="label">Nieuwe voorstellen · 16 / 24 / 32 px</div><div class="grid">{"".join(drafts)}</div>' if drafts else '<p class="hold">De handeling is verwant; behoud de context in de commandonaam en beoordeel de vorm in de uiteindelijke ribbon.</p>'
    caption = 'verschillende handelingen' if pair['kind'] == 'distinct-action' else 'verwante handelingen'
    cards.append(f'<section class="pair {pair["kind"]}"><div class="heading"><div><small>{index:02d} / 14</small><h2>{e(pair["title"])}</h2></div><span class="badge">{caption}</span></div><p class="hash">Exact dezelfde bronbytes · SHA-256 {pair["sha256"][:16]}…</p><p class="decision">{e(pair["assessment"])}</p><div class="label">Huidige UI-iconen · identieke geometrie</div><div class="grid">{"".join(sources)}</div>{proposal}</section>')

css = '''*{box-sizing:border-box}body{margin:0;background:#15191e;color:#e8ecf1;font:14px/1.5 Inter,system-ui,sans-serif}main{max-width:1150px;margin:auto;padding:40px 28px 90px}a{color:#98c6fb}header>small{color:#9cacbe;text-transform:uppercase;letter-spacing:.13em;font-weight:750}h1{font-size:38px;letter-spacing:-.035em;line-height:1.1;margin:8px 0 12px}header p{max-width:780px;color:#abb6c1;font-size:15px}.metrics{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}.metric{background:#21272e;border:1px solid #343e48;border-radius:7px;min-width:160px;padding:12px 16px}.metric b{display:block;font-size:25px;line-height:1}.metric span{color:#aab5c0;font-size:12px}.filters{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:24px 0}.filters button{background:#232a32;border:1px solid #46515d;border-radius:5px;color:#d6dee7;padding:8px 12px;cursor:pointer}.filters button.active{background:#2b4664;border-color:#5792c8;color:white}.filters a{margin-left:auto}.pair{background:#1e242b;border:1px solid #343d47;border-radius:9px;padding:20px 22px;margin:14px 0}.heading{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.heading small{color:#84a9cc;font-size:10px;font-weight:800;letter-spacing:.1em}h2{font-size:18px;line-height:1.25;margin:4px 0}.badge{border:1px solid #5c6876;border-radius:99px;padding:4px 9px;white-space:nowrap;font-size:11px;color:#ced7df}.distinct-action .badge{background:#463d2b;border-color:#847149;color:#f3d28a}.related-action .badge{background:#283f45;border-color:#4a7379;color:#addce2}.decision{font-size:13px;color:#c7d0d9;margin:0 0 14px}.hash{font:11px ui-monospace,monospace;color:#8e9ba9;margin:3px 0 16px}.label{text-transform:uppercase;font-size:10px;font-weight:800;letter-spacing:.08em;color:#aab7c4;margin:17px 0 9px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.candidate{min-width:0;background:#171c22;border:1px solid #303943;border-radius:6px;padding:12px 14px}.name{display:flex;justify-content:space-between;gap:8px}.name strong{font-size:13px}.name small{font-size:11px;color:#91a2b3}.samples{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.tile{width:64px;height:56px;background:#fafafa;border-radius:4px;display:flex;align-items:center;justify-content:center}.tile.dark{background:#2b3037}.tile img{width:24px;height:24px;object-fit:contain}.tile.dark.proposal img{filter:invert(1)}.tile.s16 img{width:16px;height:16px}.tile.s32 img{width:32px;height:32px}.candidate a{font-size:11px;text-decoration:none}.candidate code{display:block;color:#8493a1;font:10px/1.4 ui-monospace,monospace;word-break:break-all;margin-top:4px}.hold{font-size:12px;color:#adb8c3;margin:8px 0}.hidden{display:none}@media(max-width:700px){main{padding:24px 15px}h1{font-size:29px}.grid{grid-template-columns:1fr}.pair{padding:15px}.heading{display:block}.badge{display:inline-block;margin:6px 0}.filters a{margin-left:0}}'''
js = "document.querySelectorAll('[data-kind]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-kind]').forEach(item=>item.classList.toggle('active',item===button));document.querySelectorAll('.pair').forEach(pair=>pair.classList.toggle('hidden',button.dataset.kind!=='all'&&!pair.classList.contains(button.dataset.kind)));}));"
html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · Icoonbotsingen</title><style>{css}</style></head><body><main><header><small>OpenAEC / ontwerpbeoordeling / bronbewijs</small><h1>Identieke iconen, verschillende contexten</h1><p>Van 565 aantoonbaar in de UI gebruikte iconbestanden hebben 14 paren exact dezelfde bytes. Acht paren vertegenwoordigen verschillende handelingen en hebben hier onderscheidende vectorconcepten. Zes paren hergebruiken een vorm voor verwante handelingen bij deuren en kozijnen. Vier CAD/Pointcloud-vormen zijn na beoordeling in de Rust-crate opgenomen en twee worden in Pointcloud gebruikt; de overige twaalf blijven reviewmateriaal.</p><div class="metrics"><div class="metric"><b>565</b><span>geverifieerde UI-iconen</span></div><div class="metric"><b>14</b><span>identieke paren</span></div><div class="metric"><b>8</b><span>verschillende handelingen</span></div><div class="metric"><b>16</b><span>getekende vectoren · 4 in Rust</span></div></div><nav class="filters" aria-label="Filter paren"><button data-kind="all" class="active">Alle 14</button><button data-kind="distinct-action">Verschillende handelingen · 8</button><button data-kind="related-action">Verwante handelingen · 6</button><a href="icon-review-board.html">Volledige iconenreview ↗</a></nav></header>{''.join(cards)}<footer><a href="review.html">← Terug naar ontwerpbeoordeling</a></footer></main><script>{js}</script></body></html>'''
(DESIGN / 'icon-collision-review.html').write_text(html)
print('Built 14 assessed collision pairs and 16 vector drafts')
