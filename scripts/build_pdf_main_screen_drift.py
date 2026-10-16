#!/usr/bin/env python3
"""Map changed PDF Solid UI files to their current import chains and surfaces."""
from __future__ import annotations

import collections
import hashlib
import html
import json
import posixpath
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-pdf-studio')
DRIFT = json.loads((ROOT / 'harmonization/pdf-public-branch-drift.json').read_text())
SVG_ROLES = json.loads((ROOT / 'harmonization/pdf-main-jsx-svg-role-coverage.json').read_text())
OLD, NEW = DRIFT['pinned_pdf_commit'], DRIFT['current_public_main']
SCOPE = 'open-pdf-studio/js/solid/'
assert SVG_ROLES['current_commit'] == NEW


def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True)


def show(path: str) -> str:
    return git('show', f'{NEW}:{path}')


ROLES = {
    'App.jsx': ('root', 'Desktop-documentvenster'),
    'MobileApp.jsx': ('root', 'Mobiel documentvenster'),
    'components/AssistantPanel.jsx': ('panel', 'Assistentpaneel'),
    'components/DialogHost.jsx': ('dialog-host', 'Dialoogdispatcher'),
    'components/KeystrokeOverlay.jsx': ('overlay', 'Toetsenbordoverlay'),
    'components/ThreeDLazy.jsx': ('conditional-loader', '3D-lazy gate'),
    'components/ThreeDView.jsx': ('document-viewport', '3D-model en snapshotbalk'),
    'components/TypeLengthHUD.jsx': ('overlay', 'Tekenlengte-HUD'),
    'components/compare/CompareDialog.jsx': ('dialog', 'Vergelijkingskeuze'),
    'components/compare/CompareView.jsx': ('document-viewport', 'Vergelijkingswerkgebied'),
    'components/dialogs/ParametricSymbolPicker.jsx': ('dialog', 'Parametrische-symboolkiezer'),
    'components/dialogs/PrintDialog.jsx': ('dialog', 'Afdrukdialoog'),
    'components/dialogs/SplitDocumentDialog.jsx': ('dialog', 'Document splitsen'),
    'components/left-panel/panels/AnnotationsPanel.jsx': ('left-panel', 'Annotaties'),
    'components/preferences/AnnotationsTab.jsx': ('settings-page', 'Annotatievoorkeuren'),
    'components/preferences/PreferencesDialog.jsx': ('dialog', 'Voorkeuren'),
    'components/properties-panel/GeneralSection.jsx': ('properties', 'Algemene eigenschappen'),
    'components/properties-panel/ImageSection.jsx': ('properties', 'Afbeeldingseigenschappen'),
    'components/properties-panel/PapierMaat.jsx': ('properties-control', 'Papiermaat-eenheid'),
    'components/properties-panel/PropertiesPanel.jsx': ('properties', 'Eigenschappenpaneel'),
    'components/ribbon/CommentTab.jsx': ('ribbon', 'Annotatielint'),
    'components/ribbon/OrganizeTab.jsx': ('ribbon', 'Organiserenlint'),
    'components/ribbon/ViewTab.jsx': ('ribbon', 'Beeldlint'),
}
SPECIAL = {
    'components/ThreeDLazy.jsx': 'Rendert alleen bij een actief document met 3D-model of 3D-snapshot; laadt ThreeDView dynamisch.',
    'components/ThreeDView.jsx': 'App monteert de gate; model en snapshotbalk verschijnen alleen met passende PDF-inhoud.',
    'components/dialogs/SplitDocumentDialog.jsx': 'DialogHost registreert split-document; OrganizeTab opent die dialoog via het lint.',
    'components/compare/CompareDialog.jsx': 'DialogHost registreert compare; de nieuwe split-kaart is een modusillustratie.',
    'components/properties-panel/PapierMaat.jsx': 'ImageSection en PropertiesPanel gebruiken dit invoer- en eenheidscomponent.',
}

changed = [item for item in DRIFT['changed_files'] if item['ui_code_candidate']]
jsx_changed = [item for item in changed if item['path'].startswith(SCOPE) and item['path'].endswith(('.jsx', '.tsx'))]
css_changed = [item for item in changed if item['path'].endswith('.css')]
assert len(changed) == 34 and len(jsx_changed) == len(ROLES) == 23 and len(css_changed) == 11
assert {item['path'].removeprefix(SCOPE) for item in jsx_changed} == set(ROLES)
assert {item['path'] for item in jsx_changed} == {
    path for path in git('diff', '--name-only', OLD, NEW, '--', SCOPE).splitlines()
    if path.endswith(('.jsx', '.tsx'))
}
assert {item['path'] for item in css_changed} == {
    path for path in git('diff', '--name-only', OLD, NEW, '--', 'open-pdf-studio/styles').splitlines()
    if path.endswith('.css')
}

jsx_paths = [p for p in git('ls-tree', '-r', '--name-only', NEW, SCOPE).splitlines() if p.endswith(('.jsx', '.tsx'))]
assert len(jsx_paths) == 176
sources = {path: show(path) for path in jsx_paths}
graph = {}
for path, source in sources.items():
    imports = re.findall(r'(?:\bfrom\s+|\bimport\s*\(\s*|\bimport\s+)[\'\"]([^\'\"]+)[\'\"]', source)
    edges = []
    for spec in imports:
        if not spec.startswith('.'): continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
        for candidate in (target, target + '.jsx', target + '.tsx', target + '/index.jsx', target + '/index.tsx'):
            if candidate in sources:
                edges.append(candidate)
                break
    graph[path] = sorted(set(edges))

chains = {}
for root_name in ('App.jsx', 'MobileApp.jsx'):
    start = SCOPE + root_name
    queue = collections.deque([[start]])
    seen = {start}
    while queue:
        chain = queue.popleft()
        current = chain[-1]
        chains.setdefault(current, chain)
        for child in graph[current]:
            if child not in seen:
                seen.add(child)
                queue.append(chain + [child])

changed_lines = {}
for raw in git('diff', '--numstat', OLD, NEW, '--', SCOPE).splitlines():
    added, removed, path = raw.split('\t', 2)
    changed_lines[path] = {'added': None if added == '-' else int(added),
                           'removed': None if removed == '-' else int(removed)}
svg_counts = collections.Counter(item['file'] for item in SVG_ROLES['sites'])
rows = []
for item in jsx_changed:
    path = item['path']
    short = path.removeprefix(SCOPE)
    role, title = ROLES[short]
    source = sources[path]
    chain = chains.get(path, [])
    rows.append({
        'path': path, 'status': item['status'], 'role': role, 'surface': title,
        'source_lines': len(source.splitlines()), 'delta_lines': changed_lines.get(path),
        'literal_svg_sites': svg_counts[path],
        'import_chain': [p.removeprefix(SCOPE) for p in chain],
        'route_evidence': 'static JSX import chain only; conditional render and UI state require separate verification',
        'review_note': SPECIAL.get(short, ''),
        'sha256': hashlib.sha256(source.encode()).hexdigest(),
        'url': f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{NEW}/{path}',
    })
rows.sort(key=lambda row: (row['status'] != 'A', row['role'], row['path']))
assert all(row['import_chain'] for row in rows), [row['path'] for row in rows if not row['import_chain']]

styles = [{'path': item['path'], 'status': item['status'],
           'url': f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{NEW}/{item["path"]}',
           'sha256': hashlib.sha256(show(item['path']).encode()).hexdigest()}
          for item in css_changed]
manifest = {'repository': 'open-pdf-studio', 'previous_commit': OLD, 'current_commit': NEW,
            'scope': '34 changed UI candidates from pinned drift: 23 Solid JSX components and 11 CSS files. Import chains show structural connections, not runtime reachability or pixel equivalence.',
            'changed_ui_candidates': len(changed), 'changed_jsx_components': len(rows),
            'changed_css_files': len(styles), 'new_jsx_components': sum(row['status'] == 'A' for row in rows),
            'current_jsx_total': len(jsx_paths), 'components': rows, 'styles': styles}
(ROOT / 'harmonization/pdf-main-screen-drift-map.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

def link(row: dict) -> str:
    return f'<a href="{html.escape(row["url"])}">{html.escape(row["path"].removeprefix(SCOPE))}</a>'

table_rows = ''.join(
    f'<tr data-search="{html.escape((row["path"]+" "+row["surface"]+" "+row["role"]).lower())}">'
    f'<td>{link(row)}<small>{"Nieuw" if row["status"] == "A" else "Gewijzigd"}</small></td>'
    f'<td>{html.escape(row["surface"])}<small>{html.escape(row["role"])}</small></td>'
    f'<td>{" → ".join(html.escape(part) for part in row["import_chain"])}'
    f'{"<small>" + html.escape(row["review_note"]) + "</small>" if row["review_note"] else ""}</td>'
    f'<td>{row["literal_svg_sites"]}</td></tr>' for row in rows)
css_rows = ''.join(f'<li><a href="{html.escape(row["url"])}">{html.escape(row["path"].removeprefix("open-pdf-studio/"))}</a></li>' for row in styles)
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF-main · schermdriftkaart</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f5f3;color:#29292f;font:14px/1.5 system-ui,sans-serif}header{background:#36363e;color:white;padding:30px max(24px,calc((100vw - 1160px)/2))}header small{color:#f5b85c;letter-spacing:.13em}h1{font-size:28px;font-weight:550;margin:7px 0}header p{max-width:940px;color:#e1e1e6;margin:0}main{max-width:1208px;padding:24px;margin:auto}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}.metrics div{background:white;border:1px solid #dedde1;padding:12px 15px}.metrics strong{display:block;font-size:24px;font-weight:550}.metrics span{color:#686872;font-size:12px}.note{background:#fff2de;border-left:3px solid #d97706;padding:14px 18px;margin-bottom:18px}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px}.card{background:white;border:1px solid #dedde1;padding:15px;min-height:140px}.card h2{font-size:15px;margin:0 0 7px}.card p{font-size:12px;color:#63636c}.toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:14px 0}.toolbar input{font:inherit;padding:9px 11px;border:1px solid #ccc9cf;border-radius:4px;width:min(100%,360px)}.tablewrap{overflow:auto;border:1px solid #dedde1;background:white}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #ecebee;text-align:left;vertical-align:top;padding:12px 14px}th{background:#efedf0;font-size:12px;color:#565660}td small{display:block;font-size:11px;color:#777781;margin-top:3px}td:first-child{font:12px/1.45 ui-monospace,monospace;min-width:285px}td:nth-child(3){min-width:350px;font-size:12px}a{color:#925509}ul{columns:2;font:12px/1.7 ui-monospace,monospace;padding-left:18px}@media(max-width:850px){.metrics,.cards{grid-template-columns:repeat(2,1fr)}main{padding:16px}ul{columns:1}}</style><header><small>OPENAEC · PUBLIEKE PDF-MAIN</small><h1>Schermdrift sinds de gepinde audit</h1><p>Van f754cb7 naar ae1d787: alle gewijzigde Solid-componenten en stylesheetbestanden in één bronkaart. De importketen is structureel bewijs; voor zichtbare schermtoestanden is afzonderlijke review nodig.</p></header><main><div class="metrics"><div><strong>34</strong><span>UI-codekandidaten</span></div><div><strong>23</strong><span>Solid JSX-componenten</span></div><div><strong>4</strong><span>nieuwe componenten</span></div><div><strong>11</strong><span>CSS-bestanden</span></div></div><div class="note">Deze kaart vervangt geen runtimecapture. Een statische import kan conditioneel, verborgen of alleen via een dialoogroute worden gerenderd. De 321 JSX-SVG-bronplaatsen hebben een aparte rolkaart; hun aantal is geen icoontelling.</div><div class="cards"><article class="card"><h2>3D-model en snapshot</h2><p>App → ThreeDLazy → ThreeDView. De lazy gate laadt pas bij PDF-inhoud met 3D-model of snapshot.</p><a href="pdf-main-icon-delta-review.html">Snapshotstatus</a></article><article class="card"><h2>Document splitsen</h2><p>Organiseren → DialogHost → nieuwe 460px-dialoog. HTML en native Rust-modale proef zijn beoordeeld.</p><a href="pdf-main-split-document-screen-review.html">Schermreview</a></article><article class="card"><h2>Vergelijken</h2><p>Een nieuwe split-modus verschijnt als keuzekaart in de dialoog. De vorm is een illustratie, geen opdrachticoon.</p><a href="pdf-main-icon-delta-review.html">Modusvorm</a></article><article class="card"><h2>Papiermaat</h2><p>Nieuwe eenheidsinvoer in afbeeldings- en schaalbalkeigenschappen. De schermmaten vragen nog visuele review.</p><a href="../harmonization/pdf-main-screen-drift-map.json">Bronkaart</a></article></div><div class="toolbar"><h2>Gewijzigde componenten</h2><input id="filter" type="search" placeholder="Zoek component of schermrol…" aria-label="Filter componenten"><span id="count"></span></div><div class="tablewrap"><table><thead><tr><th>Solid-bron</th><th>Schermrol</th><th>Kortste importketen / beoordeling</th><th>SVG-plaatsen</th></tr></thead><tbody>''' + table_rows + '''</tbody></table></div><h2>Gewijzigde stijlen</h2><p>Deze elf bestanden kunnen de bestaande schermen visueel veranderen zonder nieuwe SVG-bronplaats. Hun exacte selector- en pixelverschillen zijn nog niet allemaal beoordeeld.</p><ul>''' + css_rows + '''</ul><p><a href="../harmonization/pdf-main-screen-drift-map.json">Machineleesbaar manifest</a> · <a href="pdf-main-jsx-svg-coverage.html">JSX-SVG-bronrollen</a></p></main><script>const field=document.getElementById('filter'),rows=[...document.querySelectorAll('tbody tr')],count=document.getElementById('count');function update(){let n=0;for(const row of rows){row.hidden=!row.dataset.search.includes(field.value.toLowerCase());if(!row.hidden)n++}count.textContent=n+' / '+rows.length}field.addEventListener('input',update);update()</script></html>'''
(ROOT / 'design/pdf-main-screen-drift-review.html').write_text(page)
print(f'PDF screen drift: {len(rows)} changed JSX components, {len(styles)} CSS files, {sum(row["status"] == "A" for row in rows)} new components')
