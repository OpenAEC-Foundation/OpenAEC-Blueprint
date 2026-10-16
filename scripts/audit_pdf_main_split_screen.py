#!/usr/bin/env python3
"""Pin the source evidence behind the current PDF split-dialog screen review."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-pdf-studio')
DRIFT = json.loads((ROOT / 'harmonization/pdf-public-branch-drift.json').read_text())
COMMIT = DRIFT['current_public_main']
BASE = 'open-pdf-studio/'


def show(path: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{BASE}{path}'], text=True)


def evidence(path: str, marker: str) -> dict:
    source = show(path)
    assert source.count(marker) == 1, (path, marker)
    line = source.count('\n', 0, source.index(marker)) + 1
    return {'file': BASE + path, 'line': line,
            'url': f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{COMMIT}/{BASE}{path}#L{line}',
            'sha256': hashlib.sha256(source.encode()).hexdigest()}


jsx_path = 'js/solid/components/dialogs/SplitDocumentDialog.jsx'
jsx = show(jsx_path)
css = show('styles/dialogs.css')
locale = json.loads(show('js/i18n/locales/nl/dialogs.json'))['splitDocument']
assert "'split-document': SplitDocumentDialog" in show('js/solid/components/DialogHost.jsx')
assert 'id="split-document"' in show('js/solid/components/ribbon/OrganizeTab.jsx')
assert 'onClick={() => openDialog(\'split-document\', {})}' in show('js/solid/components/ribbon/OrganizeTab.jsx')
assert 'const MAX_VOORBEELD = 4;' in jsx
assert "aantalBoven > 0 ? 'bookmarks' : 'pages'" in jsx
assert "const [aantal, setAantal] = createSignal('1')" in jsx
assert "const [maxMb, setMaxMb] = createSignal('10')" in jsx
assert "const [modus, setModus]" in jsx
assert 'dialogClass="split-doc-dialog"' in jsx
assert re.search(r'\.split-doc-dialog\s*\{\s*width:\s*460px;', css)
assert re.search(r'\.modal-header\s*\{[^}]*height:\s*30px;', css, re.S)
assert re.search(r'\.modal-body\s*\{\s*padding:\s*15px;', css)
assert re.search(r'\.split-doc-form\s*\{[^}]*gap:\s*8px;', css, re.S)
assert re.search(r'\.split-doc-label\s*\{[^}]*width:\s*90px;', css, re.S)
assert re.search(r'\.split-doc-number\s*\{[^}]*width:\s*56px;', css, re.S)

page = (ROOT / 'design/pdf-main-split-document-screen-review.html').read_text()
for needle in ('460 px', '30 px', '15 px', '3 modi', '4 namen', 'Manier van splitsen',
               'Uitvoer', 'Per bladwijzer op het hoogste niveau', 'Bestandsnamen:',
               'Elk deel houdt zijn annotaties', 'Dit document heeft niet-opgeslagen wijzigingen'):
    assert needle in page, needle
for key in ('title', 'method', 'everyN', 'byBookmarks', 'bySize', 'output', 'fileNames', 'keeps', 'unsaved'):
    assert locale[key] in page, (key, locale[key])

manifest = {
    'repository': 'open-pdf-studio', 'commit': COMMIT,
    'scope': 'source-backed interactive HTML review, not a captured application screenshot or PDF split implementation',
    'route': {'ribbon_command': evidence('js/solid/components/ribbon/OrganizeTab.jsx', 'id="split-document"'),
              'dialog_host': evidence('js/solid/components/DialogHost.jsx', "'split-document': SplitDocumentDialog"),
              'screen': evidence(jsx_path, 'export default function SplitDocumentDialog()')},
    'layout': {'dialog_width_px': 460, 'header_height_px': 30, 'body_padding_px': 15,
               'form_gap_px': 8, 'label_width_px': 90, 'number_input_width_px': 56,
               'source': evidence('styles/dialogs.css', '/* Split Document Dialog (#381) */')},
    'states': {'methods': ['pages', 'bookmarks', 'size'],
               'initial_without_bookmarks': 'pages', 'initial_with_bookmarks': 'bookmarks',
               'bookmarks_disabled_without_top_level': True, 'max_preview_names': 4,
               'warning_on_modified_document': True,
               'native_folder_picker_only_on_tauri': True},
    'locale': {'language': 'nl', 'source': evidence('js/i18n/locales/nl/dialogs.json', '"splitDocument": {'),
               'title': locale['title'], 'split': locale['split']},
    'prototype': 'design/pdf-main-split-document-screen-review.html',
}
(ROOT / 'harmonization/pdf-main-split-document-screen.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('PDF split dialog: route, 460/30/15 px layout, three modes and Dutch labels verified')
