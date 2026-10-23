#!/usr/bin/env python3
"""Transfer unchanged PDF JSX source-role decisions to current public main."""
from __future__ import annotations

import difflib
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / 'harmonization'
REPO = Path('/tmp/openaec-inventory/open-pdf-studio')
old_coverage = json.loads((H / 'pdf-jsx-svg-coverage.json').read_text())
drift = json.loads((H / 'pdf-public-branch-drift.json').read_text())
delta = json.loads((H / 'pdf-main-icon-delta.json').read_text())
OLD = old_coverage['commit']
NEW = drift['current_public_main']
assert OLD == drift['pinned_pdf_commit'] and NEW == delta['current_commit']

review_files = [
    'pdf-chrome-ui-icons.json', 'pdf-open-panel-ui-icons.json', 'pdf-transfer-panel-ui-icons.json',
    'pdf-context-literal-ui-icons.json', 'pdf-drawing-ui-icons.json', 'pdf-home-tab-ui-icons.json',
    'pdf-annotations-panel-ui-icons.json', 'pdf-mobile-ui-icons.json', 'pdf-symbol-palette-ui-icons.json',
    'pdf-tool-palette-ui-icons.json', 'pdf-find-bar-ui-icons.json', 'pdf-left-panel-content-ui-icons.json',
    'pdf-dialog-ui-visuals.json', 'pdf-preferences-ui-icons.json', 'pdf-ribbon-remaining-ui-icons.json',
    'pdf-last-jsx-svg-roles.json',
]
old_roles = {}
for filename in review_files:
    data = json.loads((H / filename).read_text())
    assert data['commit'] == OLD
    for decision in ('records', 'excluded'):
        for record in data.get(decision, []):
            path = record.get('source_file') or record.get('file')
            line = record.get('source_line') or record.get('line')
            assert path and isinstance(line, int)
            key = (path, line)
            assert key not in old_roles, key
            old_roles[key] = {'decision': 'excluded' if decision == 'excluded' else 'reviewed-ui-source',
                              'role': record.get('role') or record.get('kind') or record.get('review') or
                                      ('context-menu-ui' if record.get('menu') else 'ui-role-reviewed'),
                              'label': record.get('label') or record.get('name') or record.get('definition'),
                              'review_manifest': filename,
                              'exclusion_reason': record.get('reason') if decision == 'excluded' else None}
assert len(old_roles) == 317
assert set(old_roles) == {(row['file'], line) for row in old_coverage['files'] for line in row['lines']}
new_roles = {(item['source_evidence']['file'], item['source_evidence']['line']): item for item in delta['entries']}
assert len(new_roles) == 4


def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True).strip()


def show(commit: str, path: str) -> str:
    try:
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{commit}:{path}'],
                                       text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ''


def sites(source: str) -> list[dict]:
    return [{'line': source.count('\n', 0, match.start()) + 1,
             'normalized': re.sub(r'\s+', ' ', match.group()).strip()}
            for match in re.finditer(r'<svg\b[\s\S]*?</svg>', source)]


scope = 'open-pdf-studio/js/solid'
paths = sorted({path for commit in (OLD, NEW)
                for path in git('ls-tree', '-r', '--name-only', commit, scope).splitlines()
                if path.endswith(('.jsx', '.tsx'))})
entries, files = [], []
for path in paths:
    prior = sites(show(OLD, path))
    current = sites(show(NEW, path))
    matcher = difflib.SequenceMatcher(
        None, [item['normalized'] for item in prior],
        [item['normalized'] for item in current], autojunk=False)
    file_entries = []
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        assert tag in ('equal', 'insert'), (path, tag)
        if tag == 'equal':
            for old_index, new_index in zip(range(old_start, old_end), range(new_start, new_end)):
                before, now = prior[old_index], current[new_index]
                previous = old_roles[(path, before['line'])]
                file_entries.append({'file': path, 'line': now['line'], 'origin': 'unchanged-from-pinned-review',
                                     'previous_line': before['line'], **previous,
                                     'source_sha256': hashlib.sha256(now['normalized'].encode()).hexdigest()})
        else:
            assert old_start == old_end
            for new_index in range(new_start, new_end):
                now = current[new_index]
                new_role = new_roles[(path, now['line'])]
                file_entries.append({'file': path, 'line': now['line'], 'origin': 'new-main-role-review',
                                     'decision': ('ui-choice-illustration' if new_role['role'] == 'mode-choice-illustration' else 'reviewed-ui-source'),
                                     'role': new_role['role'],
                                     'label': new_role['name'], 'review_manifest': 'pdf-main-icon-delta.json',
                                     'exclusion_reason': None,
                                     'source_sha256': hashlib.sha256(now['normalized'].encode()).hexdigest()})
    assert len(file_entries) == len(current)
    entries.extend(sorted(file_entries, key=lambda item: item['line']))
    if current:
        files.append({'file': path, 'old_sites': len(prior), 'current_sites': len(current),
                      'new_sites': sum(item['origin'] == 'new-main-role-review' for item in file_entries)})

assert len(entries) == 321 and sum(x['origin'] == 'new-main-role-review' for x in entries) == 4
assert len({(x['file'], x['line']) for x in entries}) == len(entries)
manifest = {'repository': 'open-pdf-studio', 'previous_commit': OLD, 'current_commit': NEW,
            'scope': 'literal <svg> openings in Solid JSX/TSX only; unchanged markup inherits its pinned source-role decision, new markup is reviewed separately. Reachability and imported JS catalogs are separate.',
            'jsx_tsx_files_current': len([path for path in paths if show(NEW, path)]),
            'svg_bearing_files_current': len(files), 'literal_svg_sites_current': len(entries),
            'inherited_unchanged_sites': 317, 'new_role_reviewed_sites': 4,
            'files': files, 'sites': entries}
(H / 'pdf-main-jsx-svg-role-coverage.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

rows = ''.join('<tr data-file="' + html.escape(row['file'].lower()) + '"><td><a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/' +
               NEW + '/' + html.escape(row['file']) + '">' + html.escape(row['file'].removeprefix(scope + '/')) +
               '</a></td><td>' + str(row['old_sites']) + '</td><td>' + str(row['current_sites']) +
               '</td><td>' + ('<span class="new">+' + str(row['new_sites']) + '</span>' if row['new_sites'] else '—') + '</td></tr>'
               for row in files)
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PDF Studio · actuele JSX-SVG-bronrollen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#2b2d33;background:#f6f5f3}*{box-sizing:border-box}body{margin:0}
header{background:#36363e;color:#fafaf9;padding:32px max(24px,calc((100vw - 1160px)/2))}header small{color:#f5b85c;letter-spacing:.13em;font-size:11px}h1{font-size:30px;font-weight:550;margin:7px 0 10px}header p{color:#e5e3e1}
p{max-width:930px;margin:0;line-height:1.6}main{max-width:1208px;margin:auto;padding:24px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:0 0 18px}
.metric{background:white;border:1px solid #dedde1;border-radius:5px;padding:14px 16px}.metric strong{display:block;font-size:25px;font-weight:550;line-height:1.2}.metric span{font-size:12px;color:#73737a}
.note{background:#fff2de;border-left:3px solid #d97706;padding:14px 18px;margin-bottom:18px}.actions{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-bottom:12px}
input{font:inherit;border:1px solid #ceccd1;border-radius:4px;padding:9px 11px;background:white;width:min(100%,340px)}.tablewrap{overflow:auto;border:1px solid #dedde1;border-radius:5px;background:white}
table{width:100%;border-collapse:collapse}th,td{padding:10px 14px;text-align:left;border-bottom:1px solid #ecebee}th{background:#efedf0;color:#52525c;font-size:12px;position:sticky;top:0}
tr:last-child td{border-bottom:0}tbody tr:hover{background:#fffaf3}td:first-child{font:12px/1.45 ui-monospace,SFMono-Regular,monospace;overflow-wrap:anywhere;min-width:300px}
a{color:#925509}a:hover{text-decoration:none}.new{color:#9b5700;font-weight:650}#result{font-size:12px;color:#73737a}@media(max-width:680px){h1{font-size:24px}.metrics{grid-template-columns:repeat(2,1fr)}main{padding:16px}header{padding:24px 16px}}
</style><header><small>OPENAEC · BRONROLREVIEW</small><h1>PDF Studio · actuele JSX-SVG-bronrollen</h1>
<p>Publieke main ae1d787 · vergelijking met de eerder beoordeelde f754cb7. Iedere letterlijke SVG-bronplaats krijgt een rol; dit is geen telling van unieke UI-iconen.</p></header>
<main><div class="metrics"><div class="metric"><strong>176</strong><span>JSX/TSX-bestanden</span></div><div class="metric"><strong>69</strong><span>met letterlijke SVG</span></div><div class="metric"><strong>321</strong><span>SVG-bronplaatsen</span></div><div class="metric"><strong>4</strong><span>nieuwe rollen beoordeeld</span></div></div>
<div class="note">317 ongewijzigde SVG-markups behouden hun gepinde bronrol. De vier nieuwe plaatsen zijn afzonderlijk beoordeeld, inclusief een keuzeillustratie. Deze kaart toetst geen schermbereikbaarheid, importcatalogi of gewijzigde bediening rond een ongewijzigde vector.</div>
<div class="actions"><p><a href="pdf-main-icon-delta-review.html">Bekijk de vier nieuwe vormen</a> · <a href="../harmonization/pdf-main-jsx-svg-role-coverage.json">Machineleesbare rolkaart</a></p><input id="filter" type="search" aria-label="Filter bronbestanden" placeholder="Zoek bronbestand…"><span id="result"></span></div>
<div class="tablewrap"><table><thead><tr><th>Solid-bronbestand</th><th>Vorige audit</th><th>Huidige main</th><th>Nieuw beoordeeld</th></tr></thead><tbody>''' + rows + '''</tbody></table></div></main>
<script>const field=document.getElementById('filter'),rows=[...document.querySelectorAll('tbody tr')],result=document.getElementById('result');function update(){let n=0;for(const row of rows){const show=row.dataset.file.includes(field.value.toLowerCase());row.hidden=!show;if(show)n++}result.textContent=n+' / '+rows.length+' bestanden'}field.addEventListener('input',update);update()</script></html>'''
(ROOT / 'design/pdf-main-jsx-svg-coverage.html').write_text(page)
print(f'Current PDF JSX: {len(entries)} sites in {len(files)} files; 317 inherited roles, 4 new roles')
