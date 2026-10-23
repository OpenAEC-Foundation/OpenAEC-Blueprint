#!/usr/bin/env python3
"""Extract rendered Heatloss titlebar and backstage SVG controls, excluding branding."""
import hashlib
import json
import re
import subprocess
import urllib.request
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-heatloss-studio')
COMMIT = 'e233aec70e16771ecb42a57d6eab3ca6cb0e75a8'
TITLE = 'frontend/src/components/TitleBar.tsx'
BACKSTAGE = 'frontend/src/components/backstage/Backstage.tsx'
TARGET = ROOT / 'harmonization/inline-ui-icons/open-heatloss-chrome'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path):
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-heatloss-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


def svg_payload(svg):
    svg = re.sub(r'\b(strokeWidth|strokeLinecap|strokeLinejoin|fillRule|clipRule)\b',
                 lambda m: re.sub(r'[A-Z]', lambda x: '-' + x.group(0).lower(), m.group(0)), svg)
    svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
    root = ET.fromstring(svg)
    assert root.tag == '{http://www.w3.org/2000/svg}svg'
    return svg + '\n'


records = []


def record(name, group, svg, definition_line, uses, state):
    payload = svg_payload(svg)
    slug = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    dest = TARGET / f'{slug}.svg'
    assert not dest.exists() or dest.read_text() == payload, dest
    dest.write_text(payload)
    records.append({'name': name, 'group': group,
                    'svg': f'inline-ui-icons/open-heatloss-chrome/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'definition': {'file': TITLE if group == 'Titelbalk' else BACKSTAGE,
                                   'line': definition_line},
                    'uses': uses, 'state': state})


title_code = source(TITLE)
title_svgs = list(re.finditer(r'<svg\b[\s\S]*?</svg>', title_code))
assert len(title_svgs) == 10
title_names = ('Branding', 'Save', 'Undo', 'Redo', 'Print', 'Settings',
               'Minimize', 'Restore', 'Maximize', 'Close')
assert title_code.count('<div className="titlebar-icon">') == 1
for name, match in zip(title_names, title_svgs):
    line = title_code.count('\n', 0, match.start()) + 1
    if name == 'Branding':
        assert line == 78
        continue
    button = title_code[title_code.rfind('<button', 0, match.start()):match.start()]
    has_click = 'onClick=' in button
    assert has_click == (name not in {'Undo', 'Redo', 'Print'}), (name, line, has_click)
    state = ('zichtbaar, nog geen klikactie' if not has_click else
             'alleen Tauri; bij gemaximaliseerd venster' if name == 'Restore' else
             'alleen Tauri' if name in {'Minimize', 'Maximize', 'Close'} else
             'klikactie aangesloten')
    record(f'Title{name}', 'Titelbalk', match.group(), line,
           [{'file': TITLE, 'line': line, 'kind': 'jsx'}], state)

backstage_code = source(BACKSTAGE)
table, rest = backstage_code.split('};', 1)
definitions = {}
for match in re.finditer(r"^  (\w+): '(<svg.+?</svg>)',", table, re.M):
    definitions[match.group(1)] = (match.group(2), table.count('\n', 0, match.start()) + 1)
assert len(definitions) == 14
for name in sorted(definitions):
    sites = [{'file': BACKSTAGE, 'line': backstage_code.count('\n', 0, match.start()) + 1,
              'kind': 'menu-prop'} for match in re.finditer(r'\bicon=\{ICONS\.' + re.escape(name) + r'\}', backstage_code)]
    assert sites, name
    svg, line = definitions[name]
    record(f'Menu{name[0].upper()}{name[1:]}', 'Bestand-menu', svg, line, sites,
           'menu-item of submenu-item')

extra_svgs = list(re.finditer(r'<svg\b[\s\S]*?</svg>', rest))
assert len(extra_svgs) == 4
extra_names = ('Back', 'Branding', 'Website', 'GitHub')
offset = len(table) + 2
for name, match in zip(extra_names, extra_svgs):
    line = backstage_code.count('\n', 0, offset + match.start()) + 1
    if name == 'Branding':
        assert line == 817
        continue
    record(f'Backstage{name}', 'Bestand-menu', match.group(), line,
           [{'file': BACKSTAGE, 'line': line, 'kind': 'jsx'}],
           'terugnavigatie' if name == 'Back' else 'externe link in Over')

assert len(records) == 26 and sum(len(x['uses']) for x in records) == 29
manifest = {'repository': 'open-heatloss-studio', 'commit': COMMIT,
            'scope': 'Rendered titlebar and backstage control SVGs; two app-branding building marks excluded. Three quick-access buttons have no onClick in source.',
            'count': len(records), 'ui_uses': sum(len(x['uses']) for x in records),
            'excluded_branding': [{'file': TITLE, 'line': 78}, {'file': BACKSTAGE, 'line': 817}],
            'icons': records}
(ROOT / 'harmonization/heatloss-chrome-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for item in records:
    samples = ''.join(f'<div><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16,24,32))
    link = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{item["uses"][0]["file"]}#L{item["uses"][0]["line"]}'
    cards.append(f'<article data-search="{escape((item["name"]+" "+item["group"]+" "+item["state"]).lower())}"><header><strong>{escape(item["name"])}</strong><small>{escape(item["group"])}</small></header><p class="state">{escape(item["state"])}</p><div class="swatches"><div class="sample light">{samples}</div><div class="sample dark">{samples}</div></div><footer><a href="{escape(link)}">Bronaanroep ↗</a><small>{len(item["uses"])} {"plaats" if len(item["uses"]) == 1 else "plaatsen"}</small></footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · titelbalk en Bestand</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1060px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:235px}article header,article footer{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.state{font-size:11px;min-height:18px;color:#995100;margin:7px 0 0}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · titelbalk en Bestand</h1><p>26 gebruikte SVG-bedieningsvormen uit de titelbalk en het Bestand-menu, met 29 concrete UI-plaatsen op commit e233aec.</p></div><main class="content"><div class="note"><strong>Scope.</strong> Het titelbalkbeeldmerk en het grotere gebouwlogo in Over zijn branding en uitgesloten. Ongedaan, Opnieuw en Print zijn zichtbaar als snelknop, maar hebben in de gepinde bron nog geen klikactie. Vensterbediening verschijnt alleen in Tauri; maximaliseren en herstellen zijn alternatieve toestanden.</div><input id="search" type="search" placeholder="Zoek icoon of UI-gebied" aria-label="Zoek icoon"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/heatloss-chrome-icon-review.html').write_text(page)
print(f'Open Heatloss chrome: {len(records)} UI icons, {manifest["ui_uses"]} source uses; 2 branding marks excluded')
