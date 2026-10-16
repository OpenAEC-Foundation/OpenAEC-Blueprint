#!/usr/bin/env python3
"""Extract only source-used Open Planner ribbon icons from its locked Lucide build."""
from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
import tarfile
import urllib.request
from collections import defaultdict
from html import escape
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-planner-studio')
COMMIT = '5a65f6b865a7f4bedca11e05bc51ad7004fb019d'
FILES = [
    'src/components/layout/Ribbon/Ribbon.tsx',
    'src/components/layout/Ribbon/ribbonConfig.tsx',
    'src/components/layout/Ribbon/ribbonWidgets.tsx',
    *[f'src/components/ribbon/ai/Ai{name}Group.tsx' for name in
      ('Activity', 'Connection', 'Safety', 'Server')],
    'src/components/viewControls/layoutIcons.tsx',
]
TARGET = ROOT / 'harmonization/ui-icons/open-planner-ribbon'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path: str) -> str:
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-planner-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


if (REPO / '.git').exists():
    assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD']).decode().strip() == COMMIT
lock = json.loads(source('package-lock.json'))['packages']['node_modules/lucide-react']
assert lock['version'] == '0.575.0'
assert lock['resolved'].startswith('https://registry.npmjs.org/lucide-react/-/')
archive = urllib.request.urlopen(lock['resolved'], timeout=45).read()
assert 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode() == lock['integrity']
package = tarfile.open(fileobj=BytesIO(archive), mode='r:gz')
(TARGET / 'LUCIDE-LICENSE.txt').write_bytes(package.extractfile('package/LICENSE').read())

uses: dict[str, list[dict]] = defaultdict(list)
for path in FILES:
    code = source(path)
    imports = {}
    for block in re.findall(r'import\s*{([^}]*)}\s*from\s*[\'"]lucide-react[\'"]', code, re.S):
        for item in block.split(','):
            item = item.strip()
            if item:
                original, _, alias = item.partition(' as ')
                imports[alias or original] = original
    tags = list(re.finditer(r'<([A-Z][A-Za-z\d]*)\b', code))
    for match in tags:
        alias = match.group(1)
        if alias not in imports:
            continue
        name = imports[alias]
        uses[name].append({'file': path, 'line': code.count('\n', 0, match.start()) + 1,
                           'kind': 'conditional-ai' if '/ai/' in path else 'ribbon-jsx'})
    if path.endswith('/layoutIcons.tsx'):
        body = code.split('const LAYOUT_ICONS = {', 1)[1].split('} as const', 1)[0]
        for match in re.finditer(r'^\s*([a-z]+):\s*([A-Z][A-Za-z\d]+),', body, re.M):
            key, alias = match.groups()
            assert alias in imports
            offset = code.index('const LAYOUT_ICONS = {') + len('const LAYOUT_ICONS = {') + match.start()
            uses[imports[alias]].append({'file': path, 'line': code.count('\n', 0, offset) + 1,
                                         'kind': 'dynamic-layout', 'layout_key': key})

assert len(uses) == 85 and sum(map(len, uses.values())) == 114
records = []
for name in sorted(uses):
    slug = re.sub(r'(?<!^)(?=[A-Z0-9])', '-', name).lower()
    member = f'package/dist/esm/icons/{slug}.js'
    js = package.extractfile(member).read().decode()
    while 'const __iconNode =' not in js:
        alias = re.search(r"from './([^']+)\.js'", js)
        assert alias, (name, member)
        member = f'package/dist/esm/icons/{alias.group(1)}.js'
        js = package.extractfile(member).read().decode()
    block = js.split('const __iconNode =', 1)[1].split(';', 1)[0]
    nodes = re.findall(r'\[\s*"([a-z]+)",\s*\{([^}]*)\}\s*\]', block)
    assert nodes and len(nodes) == block.count('key:'), (name, member)
    root = ET.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg', 'viewBox': '0 0 24 24',
                              'fill': 'none', 'stroke': 'currentColor', 'stroke-width': '2',
                              'stroke-linecap': 'round', 'stroke-linejoin': 'round'})
    for tag, attributes in nodes:
        attrs = dict(re.findall(r'([A-Za-z]+):\s*"([^"]*)"', attributes))
        attrs.pop('key', None)
        ET.SubElement(root, tag, attrs)
    payload = ET.tostring(root, encoding='unicode') + '\n'
    dest = TARGET / f'{slug}.svg'
    dest.write_text(payload)
    ET.parse(dest)
    records.append({'name': name, 'svg': f'ui-icons/open-planner-ribbon/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'source_module': member, 'uses': uses[name]})

manifest = {'repository': 'open-planner-studio', 'commit': COMMIT,
            'lucide_version': lock['version'], 'lucide_integrity': lock['integrity'],
            'scope': 'Core ribbon JSX, its widget components, conditional AI groups and dynamic layout-icon registry; extension-provided SVGs remain runtime data.',
            'count': len(records), 'jsx_calls': sum(len(r['uses']) for r in records),
            'icons': records}
(ROOT / 'harmonization/planner-ribbon-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for record in records:
    first = record['uses'][0]
    link = f'https://github.com/OpenAEC-Foundation/open-planner-studio/blob/{COMMIT}/{first["file"]}#L{first["line"]}'
    refs = ' · '.join(sorted({u['kind'] for u in record['uses']}))
    imgs = ''.join(f'<div><img src="../harmonization/{record["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16, 24, 32))
    cards.append(f'<article data-search="{escape((record["name"] + " " + refs).lower())}"><header><strong>{escape(record["name"])}</strong><small>{len(record["uses"])} bronaanroep(en)</small></header><div class="swatches"><div class="sample light">{imgs}</div><div class="sample dark">{imgs}</div></div><footer><span>{escape(refs)}</span><a href="{escape(link)}">Bronaanroep ↗</a></footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Planner · brongebruikte ribbon-iconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:204px}article header,article footer{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:13px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Planner · echte ribbon-iconen</h1><p>85 vectoren met 114 concrete aanroepplaatsen in de actieve ribbonbron, dynamische layoutset en conditionele AI-groepen. Vastgezet op commit 5a65f6b en lucide-react 0.575.0.</p></div><main class="content"><div class="note"><strong>Scope.</strong> De Bestand-tab opent Backstage. De AI-tab verschijnt alleen bij AI-modus in niet-platformbouw. Extensies kunnen eigen SVG’s leveren; hun vorm is runtime-data en niet uit de broncatalogus af te leiden. Deze pagina toont de bronvormen op 16/24/32 px in licht en donker; harmonisatiebesluiten volgen apart.</div><input id="search" type="search" placeholder="Zoek icoonnaam of type" aria-label="Zoek icoon"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/planner-ribbon-icon-review.html').write_text(page)
print(f'Open Planner ribbon: {len(records)} locked Lucide SVGs, {manifest["jsx_calls"]} source uses')
