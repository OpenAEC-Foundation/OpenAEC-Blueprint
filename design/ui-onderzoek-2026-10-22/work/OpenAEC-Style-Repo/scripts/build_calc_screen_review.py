#!/usr/bin/env python3
"""Archive and classify every pinned Open Calc Studio UI screenshot."""
from __future__ import annotations

import hashlib
import html
import json
import subprocess
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-calc-studio')
COMMIT = 'b47042704efa388d95eb59ce77d23aeb5ee0e44c'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT
paths = subprocess.check_output(
    ['git', '-C', str(REPO), 'ls-tree', '-r', '--name-only', 'HEAD', 'docs/screenshots'], text=True
).splitlines()
assert len(paths) == 11 and all(path.endswith('.png') for path in paths)


def source_evidence(path: str, marker: str) -> dict:
    source = subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'], text=True)
    matches = [i for i, line in enumerate(source.splitlines(), 1) if marker in line]
    assert matches, (path, marker)
    return {'file': path, 'line': matches[0], 'marker': marker,
            'url': f'https://github.com/OpenAEC-Foundation/open-calc-studio/blob/{COMMIT}/{path}#L{matches[0]}'}

roles = {
    '1-leistungsverzeichnis.png': 'estimate-grid',
    '2-leistungsbuch-hochbau.png': 'construction-catalog',
    '1-estimate.png': 'estimate-grid',
    '2-grid.png': 'estimate-grid-detail',
    '3-report.png': 'report',
    '1-presupuesto.png': 'estimate-grid',
    '2-partidas.png': 'estimate-grid-detail',
    '3-informe.png': 'report',
    '4-idiomas.png': 'language-selection',
    '1-begroting.png': 'estimate-grid',
    '2-rapport.png': 'report',
}
assert {Path(path).name for path in paths} == set(roles)
items = []
for path in paths:
    raw = subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'])
    local = ROOT / 'harmonization/references/open-calc-studio' / path
    local.parent.mkdir(parents=True, exist_ok=True)
    if local.exists():
        assert local.read_bytes() == raw, f'Existing capture differs: {local}'
    else:
        local.write_bytes(raw)
    with Image.open(BytesIO(raw)) as image:
        dimensions = list(image.size)
    items.append({'source': path, 'local': str(local.relative_to(ROOT)),
                  'locale': path.split('/')[2], 'screen_role': roles[Path(path).name],
                  'dimensions': dimensions, 'sha256': hashlib.sha256(raw).hexdigest(),
                  'url': f'https://github.com/OpenAEC-Foundation/open-calc-studio/blob/{COMMIT}/{path}'})

sample_source = 'public/data/voorbeeld.ifcCalc'
sample_raw = subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{sample_source}'])
sample_local = ROOT / 'harmonization/references/open-calc-studio' / sample_source
sample_local.parent.mkdir(parents=True, exist_ok=True)
if sample_local.exists():
    assert sample_local.read_bytes() == sample_raw
else:
    sample_local.write_bytes(sample_raw)
sample = json.loads(sample_raw)
assert sample['schedule']['name'] == 'Voorbeeldbegroting'
assert len(sample['items']) >= 20

manifest = {'repository': 'open-calc-studio', 'commit': COMMIT,
            'classification': 'screen_role groups visual purposes; localization does not imply a distinct layout',
            'screens': items, 'count': len(items),
            'roles': sorted({item['screen_role'] for item in items}),
            'sample_data': {'source': sample_source, 'local': str(sample_local.relative_to(ROOT)),
                            'sha256': hashlib.sha256(sample_raw).hexdigest(),
                            'item_count': len(sample['items']),
                            'url': f'https://github.com/OpenAEC-Foundation/open-calc-studio/blob/{COMMIT}/{sample_source}'},
            'layout': {
                'title_height_px': 32,
                'title_evidence': source_evidence('src/components/layout/TitleBar.css', 'height: 32px;'),
                'tabs_height_px': 28,
                'tabs_evidence': source_evidence('src/components/ribbon/Ribbon.css', 'height: 28px;'),
                'ribbon_height_px': 94,
                'ribbon_evidence': source_evidence('src/components/ribbon/Ribbon.css', 'height: 94px;'),
                'status_height_px': 22,
                'status_evidence': source_evidence('src/components/layout/StatusBar.css', 'height: 22px;'),
                'left_panel_width_px': 220,
                'left_evidence': source_evidence('src/App.tsx', 'useState(220)'),
                'right_panel_width_px': 240,
                'right_evidence': source_evidence('src/App.tsx', 'useState(240)'),
            }}
(ROOT / 'harmonization/calc-screen-review.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = ''.join(
    '<article><div class="meta"><strong>' + html.escape(item['source'].split('/')[-1]) + '</strong>'
    '<span>' + html.escape(item['locale'].upper()) + ' · ' + html.escape(item['screen_role']) + '</span></div>'
    '<a href="../' + html.escape(item['local']) + '"><img loading="lazy" src="../' + html.escape(item['local']) + '" alt="' + html.escape(item['source']) + '"></a>'
    '<footer>' + str(item['dimensions'][0]) + ' × ' + str(item['dimensions'][1]) + ' px · '
    '<a href="' + html.escape(item['url']) + '">gepinde bron</a></footer></article>'
    for item in items)
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Open Calc Studio · schermreview</title><style>
:root{font:13px Inter,system-ui,sans-serif;color:#252a32;background:#f3f4f6}*{box-sizing:border-box}body{margin:0}
header{background:#fff;padding:22px 28px;border-bottom:1px solid #dadde2}h1{font-size:22px;margin:0 0 7px}p{margin:0;color:#5d6672;line-height:1.5;max-width:1100px}
main{padding:22px 28px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(370px,1fr));gap:15px}
article{background:white;border:1px solid #d9dde3;min-width:0}.meta{display:flex;justify-content:space-between;gap:10px;padding:12px 14px}.meta span{color:#a75b00}
article img{display:block;width:100%;height:260px;object-fit:contain;object-position:top;background:#e9ebef;border-top:1px solid #e1e3e7;border-bottom:1px solid #e1e3e7}
article footer{padding:10px 14px;color:#69727c;font-size:11px}a{color:#a75b00}details{background:white;border:1px solid #d9dde3;padding:14px;margin-top:20px}
</style><header><h1>Open Calc Studio · alle bronbeelden</h1>
<p>11 gepinde screenshots, 5 schermrollen. Nederlands, Engels, Duits en Spaans zijn hier bronvarianten; de raster- en rapportschermen zijn geen elf onafhankelijke routes. Vergelijk eerst de begrotingsgeometrie en de aparte rapportsurface voordat een Rust-pixelclaim wordt gedaan.</p></header>
<main><div class="grid">''' + cards + '''</div><details><summary>Bronmaten voor de gedeelde shell</summary>
<p>Titelbalk 32 px, linttabs 28 px, lintinhoud 94 px, status 22 px. De App.tsx-startmaten van de panelen zijn links 220 px en rechts 240 px. De 11 beelden tonen daarnaast eigen spreadsheet- en rapportinhoud.</p>
<p><a href="../harmonization/calc-screen-review.json">Manifest met hashes en bronpaden</a></p></details></main></html>'''
(ROOT / 'design/calc-screen-review.html').write_text(page)
print(f'Archived {len(items)} screenshots across {len(manifest["roles"])} screen roles')
