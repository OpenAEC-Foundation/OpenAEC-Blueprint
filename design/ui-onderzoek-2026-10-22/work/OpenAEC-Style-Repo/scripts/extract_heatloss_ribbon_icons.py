#!/usr/bin/env python3
"""Extract only inline SVG definitions used by the active Heatloss ribbon tabs."""
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
DEF_PATH = 'frontend/src/components/ribbon/icons.ts'
TABS = ('VertrekkenTab', 'ConstructiesTab', 'ResultatenTab', 'RapportTab')
TARGET = ROOT / 'harmonization/inline-ui-icons/open-heatloss-ribbon'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path):
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-heatloss-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


definitions = {}
code = source(DEF_PATH)
for match in re.finditer(r'export const (\w+Icon) = `(<svg[^`]+</svg>)`;', code):
    definitions[match.group(1)] = {'svg': match.group(2),
                                  'definition_line': code.count('\n', 0, match.start()) + 1}
assert len(definitions) == 10, len(definitions)
uses = defaultdict(list)
for tab in TABS:
    path = f'frontend/src/components/ribbon/{tab}.tsx'
    code = source(path)
    imports = re.findall(r'import\s*{([^}]+)}\s*from\s*["\']\./icons["\']', code)
    assert len(imports) == 1, path
    symbols = [name.strip() for name in imports[0].split(',')]
    assert set(symbols) <= set(definitions), path
    for name in symbols:
        occurrences = list(re.finditer(r'\bicon=\{' + re.escape(name) + r'\}', code))
        assert occurrences, (path, name)
        for match in occurrences:
            uses[name].append({'file': path, 'line': code.count('\n', 0, match.start()) + 1,
                               'tab': tab.removesuffix('Tab')})
assert len(uses) == 6 and sum(map(len, uses.values())) == 9, (len(uses), sum(map(len, uses.values())))
assert set(definitions) - set(uses) == {'thermometerIcon', 'cubeIcon', 'chartIcon', 'navigateIcon'}

records = []
for name in sorted(uses):
    svg = definitions[name]['svg'].replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    ET.fromstring(svg)
    slug = name.removesuffix('Icon')
    payload = svg + '\n'
    dest = TARGET / f'{slug}.svg'
    dest.write_text(payload)
    records.append({'name': name, 'svg': f'inline-ui-icons/open-heatloss-ribbon/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'definition': {'file': DEF_PATH, 'line': definitions[name]['definition_line']},
                    'uses': uses[name]})

manifest = {'repository': 'open-heatloss-studio', 'commit': COMMIT,
            'scope': 'Inline SVG strings passed to icon props in four active ribbon tabs; unused definitions and legacy modeller/Ribbon.tsx excluded.',
            'definition_count': len(definitions), 'count': len(records),
            'ui_uses': sum(len(x['uses']) for x in records),
            'excluded_definitions': sorted(set(definitions) - set(uses)), 'icons': records}
(ROOT / 'harmonization/heatloss-ribbon-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for record in records:
    links = ''.join(f'<a href="https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{use["file"]}#L{use["line"]}">{escape(use["tab"])} · L{use["line"]}</a>' for use in record['uses'])
    samples = ''.join(f'<div><img src="../harmonization/{record["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16,24,32))
    cards.append(f'<article><header><strong>{escape(record["name"])}</strong><small>{len(record["uses"])} {"knop" if len(record["uses"]) == 1 else "knoppen"}</small></header><div class="swatches"><div class="sample light">{samples}</div><div class="sample dark">{samples}</div></div><footer>{links}</footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · inline linticonen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1060px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:210px}article header{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:15px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer{display:flex;gap:6px;flex-wrap:wrap}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · inline linticonen</h1><p>Zes bronvormen op negen actieve lintknoppen in Vertrekken, Constructies, Resultaten en Rapport. Commit e233aec.</p></div><main class="content"><div class="note"><strong>Scope.</strong> `icons.ts` definieert tien SVG-strings; thermometer, kubus, staafdiagram en navigatiepijl worden door de actieve linttabs niet aangeroepen. De oudere `components/modeller/Ribbon.tsx` is geen getoonde app-ribbon. Dit zijn bronvormen ter beoordeling, geen goedgekeurde Rust-iconen.</div><div class="grid">''' + ''.join(cards) + '''</div></main></html>'''
(ROOT / 'design/heatloss-ribbon-icon-review.html').write_text(page)
print(f'Open Heatloss active ribbon: {len(records)} inline SVGs, {manifest["ui_uses"]} buttons; {len(manifest["excluded_definitions"])} definitions excluded')
