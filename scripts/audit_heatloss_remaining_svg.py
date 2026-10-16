#!/usr/bin/env python3
"""Classify the remaining Heatloss JSX SVGs by actual UI role.

The titlebar, backstage and sidebar are inventoried separately. This audit is
intentionally source-pinned: charts and inactive components are not icons.
"""
import hashlib
import json
import re
import subprocess
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-heatloss-studio')
COMMIT = 'e233aec70e16771ecb42a57d6eab3ca6cb0e75a8'
PREFIX = 'frontend/src/'
OUT = ROOT / 'harmonization/inline-ui-icons/open-heatloss-remaining'
OUT.mkdir(parents=True, exist_ok=True)

# Every <svg> in the remaining TSX files has one reviewed role, in source order.
# A tuple is (kind, semantic label). Only "icon" entries become reusable assets.
SPECS = {
    'components/ThemedSelect.tsx': [('icon', 'SelectChevron')],
    'components/DocumentBar.tsx': [('inactive', 'DocumentClose')],
    'pages/HellingbaanCalculator.tsx': [('diagram', 'RampDiagram')],
    'pages/HoekenCalculator.tsx': [('diagram', 'AngleDiagram')],
    'pages/Rapport.tsx': [('icon', 'ReportOptionsToggle')],
    'pages/RcCalculator.tsx': [('icon', 'LayerMoveUp'), ('icon', 'LayerMoveDown'),
                               ('icon', 'StudToggle'), ('icon', 'LayerRemove')],
    'components/rooms/RoomHeaderRow.tsx': [('icon', 'RoomCollapse'),
                                           ('icon', 'RoomVentilation'), ('icon', 'RoomRemove')],
    'components/rooms/ConstructionRow.tsx': [('icon', 'BoundaryRemove')],
    'components/settings/SettingsDialog.tsx': [('icon', 'ThemeSelectChevron'),
                                               ('illustration', 'ShortcutsPlaceholder'),
                                               ('illustration', 'PluginsPlaceholder')],
    'components/charts/StackedBarChart.tsx': [('diagram', 'StackedBarChart')],
    'components/charts/SummaryDonut.tsx': [('diagram', 'SummaryDonut')],
    'components/charts/ConstructionLossChart.tsx': [('diagram', 'ConstructionLossChart')],
    'components/layout/AppShell.tsx': [('icon', 'ErrorDismiss')],
    'components/layout/Topbar.tsx': [('inactive', 'TopbarMenu'), ('inactive', 'TopbarBrandMark'),
                                    ('inactive', 'TopbarSearch'), ('inactive', 'TopbarSettings'),
                                    ('inactive', 'TopbarAccount')],
    'components/projectSetup/ZonesCard.tsx': [('icon', 'ZoneRemove')],
    'components/construction/MaterialPicker.tsx': [('pattern', 'MaterialHatch')],
    'components/construction/LayerEditor.tsx': [('icon', 'LayerDialogClose'),
                                                ('icon', 'LayerEditorMoveUp'),
                                                ('icon', 'LayerEditorMoveDown'),
                                                ('icon', 'LayerEditorRemove')],
    'components/construction/GlaserDiagram.tsx': [('diagram', 'GlaserDiagram')],
    'components/modeller/IfcWallTypeReview.tsx': [('icon', 'IfcReviewClose')],
    'components/modeller/ProjectLibraryPanel.tsx': [('icon', 'ProjectLibraryRemove')],
}


def source(path):
    return subprocess.check_output(['git', '-C', str(REPO), 'show',
                                    f'{COMMIT}:{PREFIX}{path}']).decode()


def payload(jsx):
    opening = jsx[:jsx.index('>') + 1]
    attrs = dict(re.findall(r'\b([\w:-]+)="([^"]*)"', opening))
    keep = ('viewBox', 'fill', 'stroke', 'strokeWidth', 'strokeLinecap', 'strokeLinejoin')
    head = '<svg xmlns="http://www.w3.org/2000/svg" ' + ' '.join(
        f'{key}="{attrs[key]}"' for key in keep if key in attrs) + '>'
    body = jsx[len(opening):]
    body = re.sub(r'\b(fillRule|clipRule|strokeWidth|strokeLinecap|strokeLinejoin)',
                  lambda m: re.sub(r'[A-Z]', lambda x: '-' + x.group().lower(), m.group()), body)
    body = re.sub(r'(stroke-width)=\{([0-9.]+)\}', r'\1="\2"', body)
    svg = re.sub(r'\s+', ' ', head + body).replace('> <', '><').strip()
    ET.fromstring(svg)
    return svg + '\n'


records = []
for file, specs in SPECS.items():
    code = source(file)
    matches = list(re.finditer(r'<svg\b', code))
    assert len(matches) == len(specs), (file, len(matches), len(specs))
    for match, (kind, name) in zip(matches, specs):
        line = code.count('\n', 0, match.start()) + 1
        item = {'name': name, 'kind': kind, 'source': {'file': PREFIX + file, 'line': line}}
        if kind == 'icon':
            end = code.find('</svg>', match.start())
            assert end >= 0, (file, line)
            svg = payload(code[match.start():end + len('</svg>')])
            slug = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
            dest = OUT / f'{slug}.svg'
            dest.write_text(svg)
            item.update(svg=f'inline-ui-icons/open-heatloss-remaining/{slug}.svg',
                        sha256=hashlib.sha256(svg.encode()).hexdigest())
        records.append(item)

all_code = {path: source(path) for path in SPECS}
all_tsx = subprocess.check_output(['git', '-C', str(REPO), 'ls-tree', '-r', '--name-only',
                                   COMMIT, PREFIX]).decode().splitlines()
tsx = [p for p in all_tsx if p.endswith('.tsx')]
excluded = {'components/TitleBar.tsx', 'components/backstage/Backstage.tsx',
            'components/layout/Sidebar.tsx'}
svg_files = {}
for path in tsx:
    short = path.removeprefix(PREFIX)
    if short in excluded:
        continue
    count = len(re.findall(r'<svg\b', source(short)))
    if count:
        svg_files[short] = count
assert svg_files == {name: len(specs) for name, specs in SPECS.items()}
assert len(records) == 34
assert {kind: sum(r['kind'] == kind for r in records) for kind in
        ('icon', 'inactive', 'diagram', 'illustration', 'pattern')} == {
            'icon': 19, 'inactive': 6, 'diagram': 6, 'illustration': 2, 'pattern': 1}

# These controls are reached from AppShell, page routes or an imported component.
app = source('App.tsx')
shell = all_code['components/layout/AppShell.tsx']
assert '<AppShell>' in app and '<SettingsDialog' in shell
assert 'DocumentBar' not in app + shell and 'Topbar' not in app + shell
assert '<IfcWallTypeReview' in source('pages/Modeller.tsx')
assert '<ProjectLibraryPanel' in source('pages/Modeller.tsx')
assert '<RoomHeaderCells' in source('components/rooms/RoomTable.tsx')
assert '<ConstructionCells' in source('components/rooms/RoomTable.tsx')

manifest = {
    'repository': 'open-heatloss-studio', 'commit': COMMIT,
    'scope': 'All remaining literal JSX <svg> elements outside separately audited TitleBar, Backstage and Sidebar; package icons and string-defined ribbon icons have their own audits.',
    'tsx_svg_sites': 34, 'ui_icon_sites': 19, 'inactive_sites': 6,
    'diagram_sites': 6, 'illustration_sites': 2, 'pattern_sites': 1,
    'unique_icon_shapes': len({r['sha256'] for r in records if r['kind'] == 'icon'}),
    'records': records,
}
(ROOT / 'harmonization/heatloss-remaining-svg-audit.json').write_text(
    json.dumps(manifest, indent=2) + '\n')

cards = []
for item in records:
    src = item['source']
    url = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{src["file"]}#L{src["line"]}'
    if item['kind'] == 'icon':
        samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
        body = f'<div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div>'
    else:
        reason = {'inactive': 'Geen gevonden renderaanroep in de app',
                  'diagram': 'Data- of rekenkundige visualisatie',
                  'illustration': 'Lege-staatbeeld op instellingenpagina',
                  'pattern': 'Materiaal-arcering, geen commando'}[item['kind']]
        body = f'<p class="reason">{reason}</p>'
    cards.append(f'<article class="{item["kind"]}" data-search="{escape((item["name"]+" "+src["file"]+" "+item["kind"]).lower())}"><header><strong>{escape(item["name"])}</strong><span>{item["kind"]}</span></header><p class="source">{escape(src["file"])}:{src["line"]}</p>{body}<a href="{escape(url)}">Bron ↗</a></article>')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · overige SVG-audit</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:#fff;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:16px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.stats span{background:#fff;border:1px solid #d8d8de;padding:7px 10px}.stats b{color:#ae5b00}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:190px}article header{display:flex;justify-content:space-between;gap:8px}article header span{font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#9b5200}.source{font:10px/1.4 ui-monospace,monospace;color:#6d6d75;overflow-wrap:anywhere;margin:7px 0 10px}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:80px;border:1px solid #dadade}.samples span{display:flex;flex-direction:column;align-items:center;gap:4px}.samples small{font-size:9px}.light{background:#fafafa}.dark{background:#303039;border-color:#53535d!important}.light img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}.reason{min-height:80px;color:#666671;font-size:12px}article>a{display:inline-block;color:#ac5600;font-size:11px;margin-top:10px}.inactive,.diagram,.illustration,.pattern{background:#fafafa}@media(max-width:620px){.hero{padding:20px}main{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · overige SVG-audit</h1><p>Alle 34 overige JSX-SVG-plaatsen op broncommit e233aec; alleen echte, bereikbare bedieningsiconen komen in de icoonset.</p></div><main><div class="note"><strong>Afgrenzing.</strong> Titelbalk, Bestand, zijbalk, lint-strings en gebruikte Lucide-vormen hebben eigen bronreviews. De oude Topbar en DocumentBar hebben geen gevonden renderaanroep. Grafieken, hoek- en hellingbaandiagrammen, materiaalpatroon en grote lege-staatbeelden zijn bewust geen Rust-actieiconen. De negentien icoonplaatsen bevatten slechts negen unieke vormen; dezelfde kruisvorm sluit dialogen en verwijdert ook lagen of objecten. Die handelingen blijven semantisch gescheiden.</div><div class="stats"><span><b>19</b> iconenplaatsen</span><span><b>9</b> unieke vormen</span><span><b>6</b> inactief</span><span><b>6</b> diagrammen</span><span><b>2</b> illustraties</span><span><b>1</b> patroon</span></div><input id="search" type="search" aria-label="Zoek SVG of bronbestand" placeholder="Zoek SVG of bronbestand"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/heatloss-remaining-svg-review.html').write_text(page)
print('Open Heatloss remaining SVG: 34 sites; 19 UI icons, 15 excluded with reasons')
