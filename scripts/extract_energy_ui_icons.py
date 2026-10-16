#!/usr/bin/env python3
"""Inventory source-used Open Energy UI icons from its locked Lucide release."""
from __future__ import annotations

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
REPO = Path('/tmp/openaec-inventory/open-energy-studio')
COMMIT = 'e9a485db4ac695ff502a48cd2ded50dec5b5a1a6'
FILES = '''src/components/BuildFlow/BuildFlow.tsx
src/components/CalculationNotice/CalculationNotice.tsx
src/components/EvidenceLink/EvidenceLink.tsx
src/components/HeatPumpInventoryPanel/HeatPumpInventoryPanel.tsx
src/components/ItemActions/ItemActions.tsx
src/components/KernelAuditPanel/KernelAuditPanel.tsx
src/components/MaatwerkadviesPanel/MaatwerkadviesPanel.tsx
src/components/MaatwerkadviesPanel/RelabelPanel.tsx
src/components/NtaPerformancePanel/NtaPerformancePanel.tsx
src/components/PreviewPanel/PreviewPanel.tsx
src/components/PropertiesPanel/PropertiesPanel.tsx
src/components/SettingsDialog/SettingsDialog.tsx
src/components/StatusBar/StatusBar.tsx
src/components/SurveyWizard/SurveyMwa.tsx
src/components/SurveyWizard/SurveyRegistration.tsx
src/components/SurveyWizard/SurveyRelabel.tsx
src/components/SurveyWizard/SurveyReport.tsx
src/components/SurveyWizard/SurveyWizard.tsx
src/components/UValueCalculator/UValueCalculator.tsx
src/components/WelcomeScreen/NewProjectDialog.tsx
src/components/WelcomeScreen/WelcomeScreen.tsx
src/components/shell/CommandPalette.tsx
src/components/shell/Inspector.tsx
src/components/shell/NtaStepPage.tsx
src/components/shell/PageHeader.tsx
src/components/shell/StepRouter.tsx
src/components/shell/TopBar.tsx
src/components/shell/WorkflowNav.tsx
src/components/shell/pages/BuildingPages.tsx
src/components/shell/pages/DeliveryPages.tsx
src/components/shell/pages/InstallationsPage.tsx
src/components/shell/pages/ProjectOverview.tsx
src/components/shell/pages/RegistrationForm.tsx
src/components/shell/pages/RegistrationPage.tsx
src/components/shell/pages/existing/MwaViews.tsx
src/components/shell/pages/results/MonthlyChart.tsx
src/components/shell/pages/results/ResultsDashboard.tsx
src/components/ui/DataTable.tsx
src/components/ui/Display.tsx
src/components/ui/Navigation.tsx
src/components/ui/Toast.tsx'''.splitlines()
TARGET = ROOT / 'harmonization/ui-icons/open-energy-studio'
TARGET.mkdir(parents=True, exist_ok=True)


def source(path: str) -> str:
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-C', str(REPO),
                                        'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-energy-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


if (REPO / '.git').exists():
    assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD']).decode().strip() == COMMIT
lock = json.loads(source('package-lock.json'))['packages']['node_modules/lucide-react']
assert lock['version'] == '0.577.0'
assert lock['resolved'].startswith('https://registry.npmjs.org/lucide-react/-/')
archive = urllib.request.urlopen(lock['resolved'], timeout=45).read()
assert 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode() == lock['integrity']
package = tarfile.open(fileobj=BytesIO(archive), mode='r:gz')
(TARGET / 'LUCIDE-LICENSE.txt').write_bytes(package.extractfile('package/LICENSE').read())


def section(path: str) -> str:
    if '/shell/pages/results/' in path or '/NtaPerformancePanel/' in path:
        return 'Resultaten'
    if '/shell/pages/' in path:
        return 'Schermroutes'
    if '/shell/' in path:
        return 'Shell en navigatie'
    if '/WelcomeScreen/' in path or '/BuildFlow/' in path:
        return 'Start en project'
    if '/SurveyWizard/' in path or '/MaatwerkadviesPanel/' in path:
        return 'Opname en advies'
    return 'Panelen en bediening'


uses: dict[str, list[dict]] = defaultdict(list)
direct = dynamic = 0
for path in FILES:
    code = source(path)
    imports = {}
    for block in re.findall(r'import\s*{([^}]*)}\s*from\s*[\'"]lucide-react[\'"]', code, re.S):
        for entry in block.split(','):
            entry = entry.strip()
            if entry:
                original, _, alias = entry.partition(' as ')
                imports[alias or original] = original
    assert imports, path
    for match in re.finditer(r'<([A-Z][A-Za-z\d]*)\b', code):
        if match.group(1) not in imports:
            continue
        uses[imports[match.group(1)]].append({'file': path,
            'line': code.count('\n', 0, match.start()) + 1,
            'kind': 'jsx', 'section': section(path)})
        direct += 1
    for table in re.finditer(r'const ICON = \{([^}]+)\}', code):
        for match in re.finditer(r'\b(done|open|waiting):\s*([A-Z][A-Za-z\d]+)', table.group(1)):
            assert match.group(2) in imports, (path, match.group(2))
            offset = table.start(1) + match.start()
            uses[imports[match.group(2)]].append({'file': path,
                'line': code.count('\n', 0, offset) + 1,
                'kind': 'dynamic-status', 'status': match.group(1), 'section': section(path)})
            dynamic += 1
    used = {name for name, entries in uses.items() if any(u['file'] == path for u in entries)}
    assert set(imports.values()) <= used, (path, set(imports.values()) - used)

assert len(FILES) == 41 and len(uses) == 84 and direct == 251 and dynamic == 6
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
    records.append({'name': name, 'svg': f'ui-icons/open-energy-studio/{slug}.svg',
                    'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                    'source_module': member, 'sections': sorted({u['section'] for u in uses[name]}),
                    'uses': uses[name]})

manifest = {'repository': 'open-energy-studio', 'commit': COMMIT,
            'lucide_version': lock['version'], 'lucide_integrity': lock['integrity'],
            'scope': 'Actual Lucide JSX tags and status-table choices in 41 UI component files; direct imports without UI use are excluded.',
            'files': len(FILES), 'count': len(records), 'jsx_uses': direct,
            'dynamic_status_uses': dynamic, 'sections': dict(Counter(u['section'] for r in records for u in r['uses'])),
            'icons': records}
(ROOT / 'harmonization/energy-ui-icons.json').write_text(json.dumps(manifest, indent=2) + '\n')

cards = []
for record in records:
    use = record['uses'][0]
    link = f'https://github.com/OpenAEC-Foundation/open-energy-studio/blob/{COMMIT}/{use["file"]}#L{use["line"]}'
    chips = ''.join(f'<span>{escape(label)}</span>' for label in record['sections'])
    imgs = ''.join(f'<div><img src="../harmonization/{record["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16, 24, 32))
    cards.append(f'<article data-search="{escape((record["name"]+" "+" ".join(record["sections"])).lower())}"><header><strong>{escape(record["name"])}</strong><small>{len(record["uses"])} bronplaatsen</small></header><div class="chips">{chips}</div><div class="swatches"><div class="sample light">{imgs}</div><div class="sample dark">{imgs}</div></div><footer><a href="{escape(link)}">Bronaanroep ↗</a></footer></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Energy · UI-iconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1060px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:224px}article header,article footer{display:flex;justify-content:space-between;gap:8px;align-items:baseline}article header small,article footer{font-size:11px;color:#74747d}.chips{display:flex;gap:4px;flex-wrap:wrap;min-height:20px;margin-top:7px}.chips span{background:#fff1dc;color:#995100;font-size:9px;padding:2px 5px}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:94px;border:1px solid #dadade}.sample div{display:flex;flex-direction:column;align-items:center;justify-content:end;height:64px;gap:8px}.sample img{display:block}.sample small{font-size:9px}.light{color:#b45b00;background:#fafafa}.dark{color:#ff980e;background:#303039;border-color:#53535d}img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}article footer a{color:#ac5600;white-space:nowrap}@media(max-width:620px){.hero{padding:20px}.content{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Energy · iconen in de echte UI</h1><p>84 Lucide-vormen in 41 UI-bestanden, met 251 concrete JSX-aanroepen en zes statuskeuzes via een dynamische tabel. Broncommit e9a485d · lucide-react 0.577.0.</p></div><main class="content"><div class="note"><strong>Scope.</strong> De atlas toont gebruikte bibliotheekvectoren uit shell, routes, resultaten, opname, projectstart en panelen. De drie statusvormen van de Survey Wizard zijn via `ICON`-tabellen gekozen en expliciet meegeteld. Handleidingbeelden, bouwsymbolen en niet-aangeroepen imports blijven buiten de telling. Dit zijn bronvormen op 16/24/32 px, nog geen goedgekeurde Rust-iconen.</div><input id="search" type="search" placeholder="Zoek icoon of UI-gebied" aria-label="Zoek icoon"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.addEventListener('input',()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())})</script></html>'''
(ROOT / 'design/energy-ui-icon-review.html').write_text(page)
print(f'Open Energy: {len(FILES)} UI files, {len(records)} Lucide icons, {direct} JSX + {dynamic} status-table uses')
