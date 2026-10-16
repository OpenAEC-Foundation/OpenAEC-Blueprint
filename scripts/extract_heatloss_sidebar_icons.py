#!/usr/bin/env python3
"""Inventory SVG icon components actually selected by Heatloss sidebar navigation."""
import hashlib
import json
import re
import subprocess
import urllib.request
from collections import defaultdict
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-heatloss-studio')
COMMIT = 'e233aec70e16771ecb42a57d6eab3ca6cb0e75a8'
PATH = 'frontend/src/components/layout/Sidebar.tsx'
TARGET = ROOT / 'harmonization/inline-ui-icons/open-heatloss-sidebar'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path):
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-heatloss-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


code = source(PATH)
app = source('frontend/src/App.tsx')
shell = source('frontend/src/components/layout/AppShell.tsx')
assert '<Sidebar />' in shell
app_routes = set(re.findall(r'<Route path="([^"]+)"', app))
definitions = {}
for match in re.finditer(r'function (Icon\w+)\([\s\S]*?return \(\s*(<svg\b[\s\S]*?</svg>)', code):
    definitions[match.group(1)] = {'svg': match.group(2),
                                   'line': code.count('\n', 0, match.start()) + 1}
assert len(definitions) == 19

uses = defaultdict(list)
item_pattern = r'\{\s*to:\s*"([^"]+)",\s*labelKey:\s*"([^"]+)",\s*Icon:\s*(Icon\w+),?\s*\}'
for match in re.finditer(item_pattern, code, re.S):
    route, label, name = match.groups()
    assert route in app_routes and name in definitions, (route, name)
    uses[name].append({'file': PATH, 'line': code.count('\n', 0, match.start()) + 1,
                       'route': route, 'label_key': label, 'mode': 'web en Tauri'})
assert sum(len(v) for v in uses.values()) == 23
assert '/projects' in app_routes
uses['IconFolder'].append({'file': PATH, 'line': code.count('\n', 0, code.index('<NavItem to="/projects"')) + 1,
                           'route': '/projects', 'label_key': 'sidebar.projects', 'mode': 'alleen web'})
chevron_pos = code.index('<IconChevron expanded={expanded}')
uses['IconChevron'].append({'file': PATH, 'line': code.count('\n', 0, chevron_pos) + 1,
                            'route': None, 'label_key': 'group.expand/collapse',
                            'mode': 'negen navigatiegroepen'})
assert set(definitions) == set(uses) and sum(len(v) for v in uses.values()) == 25

records = []
for name in sorted(definitions):
    svg = definitions[name]['svg']
    # React-only className expressions include a dynamic rotation on IconChevron.
    svg = re.sub(r'\s+className=\{[\s\S]*?\}\s*(?=width=)', ' ', svg, count=1)
    svg = re.sub(r'\b(strokeWidth|strokeLinecap|strokeLinejoin)\b',
                 lambda m: re.sub(r'[A-Z]', lambda x: '-' + x.group(0).lower(), m.group(0)), svg)
    svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
    root = ET.fromstring(svg)
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    payload = svg + '\n'
    slug = re.sub(r'(?<!^)(?=[A-Z])', '-', name.removeprefix('Icon')).lower()
    dest = TARGET / f'{slug}.svg'
    dest.write_text(payload)
    records.append({'name': name, 'svg': f'inline-ui-icons/open-heatloss-sidebar/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'definition': {'file': PATH, 'line': definitions[name]['line']},
                    'uses': uses[name],
                    'semantic_collision': name in {'IconBarChart', 'IconLayers'}})

routes = [use for item in records for use in item['uses'] if use['route']]
assert len(routes) == 24 and len({use['route'] for use in routes}) == 24
assert app_routes - {use['route'] for use in routes} == {'/', '/rapport', '/import/thermal'}
manifest = {'repository': 'open-heatloss-studio', 'commit': COMMIT,
            'scope': 'SVG components selected by NAV_GROUPS, web Projects link and group disclosure in the rendered AppShell Sidebar.',
            'count': len(records), 'source_use_sites': sum(len(x['uses']) for x in records),
            'sidebar_routes': 24, 'nav_groups': 9,
            'routes_without_sidebar_item': ['/rapport', '/import/thermal'],
            'icons': records}
(ROOT / 'harmonization/heatloss-sidebar-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for item in records:
    samples = ''.join(f'<div><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16,24,32))
    route_text = ', '.join(use['route'] or 'groepspijl' for use in item['uses'])
    link = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{PATH}#L{item["uses"][0]["line"]}'
    collision = '<span class="collision">meerdere bestemmingen</span>' if item['semantic_collision'] else ''
    cards.append(f'<article data-search="{escape((item["name"]+" "+route_text).lower())}"><header><strong>{escape(item["name"])}</strong><small>{len(item["uses"])} {"gebruik" if len(item["uses"]) == 1 else "gebruiken"}</small></header><div class="routes">{escape(route_text)}</div>{collision}<div class="swatches"><div class="sample light">{samples}</div><div class="sample dark">{samples}</div></div><footer><a href="{escape(link)}">Bronaanroep ↗</a></footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · zijbalkiconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1060px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:246px}article header,article footer{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.routes{font:10px/1.4 ui-monospace,monospace;min-height:30px;overflow-wrap:anywhere;margin-top:6px;color:#6d6d75}.collision{display:inline-block;background:#fff1dc;color:#995100;font-size:9px;padding:2px 5px;margin-top:3px}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · gebruikte zijbalkiconen</h1><p>Negentien SVG-componenten op 24 navigatieroutes en de pijl van negen groepen. Broncommit e233aec.</p></div><main class="content"><div class="note"><strong>Scope.</strong> Alle negentien vormen zijn aan de gerenderde `Sidebar` gekoppeld. De web-only Projecten-route gebruikt de mapvorm. Rapport en de thermische importwizard zijn wel App-routes maar hebben geen eigen zijbalkitem. Eén staafdiagramvorm staat bij Resultaten, Tojuli en BENG; één lagenvorm bij Warmteverlies-instellingen en drie Rc/Uw-pagina’s. Die bestemmingen krijgen niet automatisch hetzelfde Rust-commando.</div><input id="search" type="search" placeholder="Zoek icoon of route" aria-label="Zoek icoon"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/heatloss-sidebar-icon-review.html').write_text(page)
print(f'Open Heatloss Sidebar: {len(records)} icon components, {manifest["source_use_sites"]} source sites, {len(routes)} routes')
