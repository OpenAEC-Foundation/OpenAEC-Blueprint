#!/usr/bin/env python3
"""Inventory Lucide shapes used by the active Open Heatloss UI components."""
import base64
import hashlib
import json
import re
import subprocess
import tarfile
import urllib.request
from collections import Counter, defaultdict
from html import escape
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-heatloss-studio')
COMMIT = 'e233aec70e16771ecb42a57d6eab3ca6cb0e75a8'
FILES = '''frontend/src/components/import/ConstructionImportStep.tsx
frontend/src/components/import/FileUploadStep.tsx
frontend/src/components/import/ImportSummary.tsx
frontend/src/components/import/RoomImportStep.tsx
frontend/src/components/import/ThermalImportWizard.tsx
frontend/src/components/ribbon/ModellerTab.tsx
frontend/src/pages/Library.tsx
frontend/src/pages/ProjectConstructions.tsx'''.splitlines()
TARGET = ROOT / 'harmonization/ui-icons/open-heatloss-studio'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path):
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-heatloss-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


app = source('frontend/src/App.tsx')
ribbon = source('frontend/src/components/ribbon/Ribbon.tsx')
wizard = source('frontend/src/components/import/ThermalImportWizard.tsx')
assert '<Route path="/import/thermal" element={<ThermalImportWizard />}' in app
assert '<Route path="/library" element={<Library />}' in app
assert '<Route path="/constructies" element={<ProjectConstructions />}' in app
assert 'import ModellerTab from "./ModellerTab"' in ribbon and 'return <ModellerTab />' in ribbon
assert all(f'<{name}' in wizard for name in
           ('FileUploadStep', 'RoomImportStep', 'ConstructionImportStep', 'ImportSummary'))


lock = json.loads(source('frontend/package-lock.json'))['packages']['node_modules/lucide-react']
assert lock['version'] == '0.577.0'
archive = urllib.request.urlopen(lock['resolved'], timeout=45).read()
assert 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode() == lock['integrity']
package = tarfile.open(fileobj=BytesIO(archive), mode='r:gz')
(TARGET / 'LUCIDE-LICENSE.txt').write_bytes(package.extractfile('package/LICENSE').read())

uses = defaultdict(list)
kind_counts = Counter()
for path in FILES:
    code = source(path)
    imports = {}
    for block in re.findall(r'import\s*{([^}]*)}\s*from\s*[\'"]lucide-react[\'"]', code, re.S):
        for entry in block.split(','):
            original = entry.strip()
            if original:
                imports[original] = original
    assert imports, path
    patterns = {
        'jsx': r'<([A-Z][A-Za-z\d]*)\b',
        'icon-prop': r'\bicon=\{([A-Z][A-Za-z\d]*)\}',
        'icon-registry': r'\bicon:\s*([A-Z][A-Za-z\d]*)\b',
    }
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, code):
            name = match.group(1)
            if name not in imports:
                continue
            uses[name].append({'file': path, 'line': code.count('\n', 0, match.start()) + 1,
                               'kind': kind, 'area': ('Modeller-lint' if '/ribbon/' in path else
                                                      'Importwizard' if '/import/' in path else 'Projectschermen')})
            kind_counts[kind] += 1
    seen = {name for name, sites in uses.items() if any(site['file'] == path for site in sites)}
    assert set(imports) <= seen, (path, sorted(set(imports) - seen))

assert len(FILES) == 8 and len(uses) == 35, (len(FILES), len(uses))
records = []
for name in sorted(uses):
    slug = re.sub(r'(?<!^)(?=[A-Z0-9])', '-', name).lower()
    slug = re.sub(r'(?<=\d)x-(?=\d)', 'x', slug)
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
        attrs = dict(re.findall(r'([A-Za-z][A-Za-z0-9]*):\s*"([^"]*)"', attributes))
        assert not re.sub(r'[A-Za-z][A-Za-z0-9]*:\s*"[^"]*"', '', attributes).strip(' ,\n\t'), (name, attributes)
        attrs.pop('key', None)
        if tag == 'line':
            assert {'x1', 'x2', 'y1', 'y2'} <= attrs.keys(), (name, attrs)
        ET.SubElement(root, tag, attrs)
    payload = ET.tostring(root, encoding='unicode') + '\n'
    dest = TARGET / f'{slug}.svg'
    dest.write_text(payload)
    ET.parse(dest)
    records.append({'name': name, 'svg': f'ui-icons/open-heatloss-studio/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'source_module': member, 'uses': uses[name]})

manifest = {'repository': 'open-heatloss-studio', 'commit': COMMIT,
            'lucide_version': lock['version'], 'lucide_integrity': lock['integrity'],
            'scope': 'Direct JSX, icon props and icon registries in eight active UI files. Legacy components/modeller/Ribbon.tsx is excluded because the app ribbon renders components/ribbon/ModellerTab.tsx.',
            'reachability': {'routes': ['/import/thermal', '/library', '/constructies'],
                             'ribbon': 'frontend/src/components/ribbon/Ribbon.tsx → ModellerTab',
                             'wizard_steps': ['FileUploadStep', 'RoomImportStep', 'ConstructionImportStep', 'ImportSummary']},
            'files': len(FILES), 'count': len(records), 'kind_counts': dict(kind_counts),
            'icons': records}
(ROOT / 'harmonization/heatloss-lucide-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for record in records:
    use = record['uses'][0]
    link = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{use["file"]}#L{use["line"]}'
    areas = sorted({site['area'] for site in record['uses']})
    chips = ''.join(f'<span>{escape(area)}</span>' for area in areas)
    imgs = ''.join(f'<div><img src="../harmonization/{record["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16, 24, 32))
    cards.append(f'<article data-search="{escape((record["name"]+" "+" ".join(areas)).lower())}"><header><strong>{escape(record["name"])}</strong><small>{len(record["uses"])} {"aanroep" if len(record["uses"]) == 1 else "aanroepen"}</small></header><div class="chips">{chips}</div><div class="swatches"><div class="sample light">{imgs}</div><div class="sample dark">{imgs}</div></div><footer><a href="{escape(link)}">Bronaanroep ↗</a></footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · Lucide UI-iconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1060px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:224px}article header,article footer{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.chips{display:flex;gap:4px;flex-wrap:wrap;min-height:20px;margin-top:7px}.chips span{background:#fff1dc;color:#995100;font-size:9px;padding:2px 5px}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · Lucide-iconen in de UI</h1><p>35 bronvormen in acht actieve UI-bestanden: importwizard, Modeller-lint en projectschermen. Commit e233aec · lucide-react 0.577.0.</p></div><main class="content"><div class="note"><strong>Scope.</strong> Rechtstreekse JSX-aanroepen, iconprops en de dynamische Modeller-toolregistry zijn meegeteld. De oudere `components/modeller/Ribbon.tsx` is geen actieve app-ribbon. In het Modeller-lint betekent `Download` IFC import en `Upload` IFC export; `FileDown` betekent JSON import en `FileUp` JSON export. Elders in de importwizard betekent `Upload` juist een bestand kiezen. Hun namen zijn dus geen betrouwbare commandobetekenis. Dit zijn bronvormen voor review, geen goedgekeurde Rust-iconen.</div><input id="search" type="search" placeholder="Zoek icoon of UI-gebied" aria-label="Zoek icoon"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/heatloss-lucide-icon-review.html').write_text(page)
print(f'Open Heatloss active Lucide: {len(FILES)} UI files, {len(records)} icons, {dict(kind_counts)}')
