#!/usr/bin/env python3
"""Review the four newly added literal JSX SVGs on public PDF main."""
from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-pdf-studio')
drift = json.loads((ROOT / 'harmonization/pdf-public-branch-drift.json').read_text())
COMMIT = drift['current_public_main']
OLD = drift['pinned_pdf_commit']


def show(path: str, commit: str = COMMIT) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{commit}:{path}'], text=True)


def evidence(path: str, marker: str) -> dict:
    lines = show(path).splitlines()
    matches = [i for i, line in enumerate(lines, 1) if marker in line]
    assert matches, (path, marker)
    return {'file': path, 'line': matches[0], 'marker': marker,
            'url': f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{COMMIT}/{path}#L{matches[0]}'}


BASE = 'open-pdf-studio/js/solid/components/'
specs = [
    ('three-d-snapshot', BASE + 'ThreeDView.jsx', 'snapshot-status-icon',
     r'(<svg width="16" height="16".*?</svg>)', '<ThreeDSnapshotBar />',
     'open-pdf-studio/js/solid/App.jsx'),
    ('compare-split-choice', BASE + 'compare/CompareDialog.jsx', 'mode-choice-illustration',
     r'(<svg viewBox="0 0 32 32" width="32" height="32" fill="none" stroke-width="2">\s*<rect x="4" y="5".*?</svg>)',
     "value=\"split\"", BASE + 'compare/CompareDialog.jsx'),
    ('proofread', BASE + 'ribbon/CommentTab.jsx', 'ribbon-command-icon',
     r'const proofreadIcon = `(<svg.*?</svg>)`;', 'id="tool-proofread"',
     BASE + 'ribbon/CommentTab.jsx'),
    ('split-document', BASE + 'ribbon/OrganizeTab.jsx', 'ribbon-command-icon',
     r'const splitDocumentIcon = `(<svg.*?</svg>)`;', 'id="split-document"',
     BASE + 'ribbon/OrganizeTab.jsx'),
]

out = ROOT / 'harmonization/inline-ui-icons/open-pdf-studio-main-delta'
out.mkdir(parents=True, exist_ok=True)
entries = []
for name, path, role, pattern, use_marker, use_path in specs:
    source = show(path)
    matches = list(re.finditer(pattern, source, re.S))
    assert len(matches) == 1, (name, len(matches))
    source_svg = matches[0].group(1)
    svg = source_svg.strip().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1) + '\n'
    ET.fromstring(svg)
    target = out / f'{name}.svg'
    target.write_text(svg)
    source_line = source.count('\n', 0, matches[0].start(1)) + 1
    entries.append({'name': name, 'role': role,
                    'source_evidence': {'file': path, 'line': source_line,
                                        'marker': source_svg.splitlines()[0].strip(),
                                        'url': f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{COMMIT}/{path}#L{source_line}'},
                    'ui_usage_evidence': evidence(use_path, use_marker),
                    'local': str(target.relative_to(ROOT)),
                    'sha256': hashlib.sha256(svg.encode()).hexdigest()})

assert sum(x['new_literal_svg_tags'] - x['old_literal_svg_tags'] for x in drift['jsx_literal_svg_counts']) == 4
manifest = {'repository': 'open-pdf-studio', 'previous_commit': OLD, 'current_commit': COMMIT,
            'scope': 'four added literal JSX SVG source places in changed files; unchanged shapes and imported icon catalogs require separate delta review',
            'entries': entries, 'count': len(entries),
            'role_counts': {role: sum(e['role'] == role for e in entries) for role in sorted({e['role'] for e in entries})}}
(ROOT / 'harmonization/pdf-main-icon-delta.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = ''.join('<article><div class="sizes"><span class="s16">' + (ROOT / e['local']).read_text() + '</span>'
                '<span class="s24">' + (ROOT / e['local']).read_text() + '</span>'
                '<span class="s32">' + (ROOT / e['local']).read_text() + '</span></div><b>' + html.escape(e['name']) + '</b>'
                '<small>' + html.escape(e['role']) + '</small><a href="' + e['ui_usage_evidence']['url'] + '">UI-aanroep</a></article>'
                for e in entries)
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Open PDF Studio · main-icoondelta</title><style>
:root{font:13px Inter,system-ui,sans-serif;color:#262a31;background:#f2f3f5}*{box-sizing:border-box}body{margin:0}
header{padding:22px 28px;background:white;border-bottom:1px solid #dadddf}h1{font-size:22px;margin:0 0 7px}p{max-width:1000px;line-height:1.5;color:#56606b;margin:0}
section{padding:22px 28px}h2{font-size:16px;margin:0 0 12px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
article{background:white;border:1px solid #dadddf;padding:18px;min-height:145px}article b,article small,article a{display:block}article small{color:#6b7580;margin:5px 0 12px}
.sizes{display:flex;align-items:center;gap:20px;height:42px;margin-bottom:10px}.sizes span{display:grid;place-items:center;width:38px;height:38px}.sizes svg{color:#262a31}.s16 svg{width:16px;height:16px}.s24 svg{width:24px;height:24px}.s32 svg{width:32px;height:32px}
.dark{background:#252a32;color:#f4f5f6}.dark article{background:#333942;border-color:#59616b}.dark small{color:#c5cad0}.dark svg{color:#f4f5f6}
a{color:#ac6500}.dark a{color:#ffb454}@media(max-width:780px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style><header><h1>PDF Studio · vier nieuwe JSX-SVG-plaatsen</h1>
<p>Publieke main ae1d787 vergeleken met gepinde audit f754cb7. Drie vormen zijn status/commando-iconen; het Vergelijken-beeld is een keuzeillustratie. Vaste rode/blauwe kleur in twee vormen vraagt een thema- en betekenisoordeel voordat ze gedeelde Rust-iconen worden.</p></header>
<section><h2>Light · 16 / 24 / 32 px</h2><div class="grid">''' + cards + '''</div></section>
<section class="dark"><h2>Forge · 16 / 24 / 32 px</h2><div class="grid">''' + cards + '''</div>
<p style="margin-top:18px"><a href="../harmonization/pdf-main-icon-delta.json">Bronrollen en hashes</a> · <a href="../harmonization/pdf-public-branch-drift.json">404 gewijzigde bestanden</a></p></section></html>'''
(ROOT / 'design/pdf-main-icon-delta-review.html').write_text(page)
print(f'Classified {len(entries)} added JSX SVGs at {COMMIT[:8]}')
