#!/usr/bin/env python3
"""Audit ContextMenu.jsx inline SVG strings with their lexical JSX uses."""
import hashlib
import json
import re
import subprocess
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
path = 'open-pdf-studio/js/solid/components/ContextMenu.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/context-menu'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
app = source('open-pdf-studio/js/solid/App.jsx')
assert "import ContextMenu from './components/ContextMenu.jsx'" in app and '<ContextMenu />' in app
defs = list(re.finditer(r"const\s+(\w+)\s*=\s*'(<svg\b[^']*</svg>)';", code))
assert len(defs) == 14
labels = {
    'revealInFolderIcon': ('Bestand tonen in bestandsbeheerder', 'page', 'path-only'),
    'moveUpIcon': ('Miniatuurpagina omhoog', 'thumbnail', 'boundary-conditional'),
    'moveDownIcon': ('Miniatuurpagina omlaag', 'thumbnail', 'boundary-conditional'),
    'thumbnailCutIcon': ('Pagina knippen', 'thumbnail', 'last-page-disabled'),
    'thumbnailCopyIcon': ('Pagina kopiëren', 'thumbnail', 'available'),
    'thumbnailPasteIcon': ('Pagina plakken', 'thumbnail', 'available'),
    'thumbnailInsertIcon': ('Pagina invoegen / uit bestand invoegen', 'thumbnail', 'two-commands'),
    'thumbnailExtractIcon': ('Pagina extraheren', 'thumbnail', 'available'),
    'thumbnailReplaceIcon': ('Pagina vervangen', 'thumbnail', 'multi-selection-disabled'),
    'thumbnailDeleteIcon': ('Pagina verwijderen', 'thumbnail', 'last-page-disabled'),
    'thumbnailRotateLeftIcon': ('Pagina linksom draaien', 'thumbnail', 'available'),
    'thumbnailRotateRightIcon': ('Pagina rechtsom draaien', 'thumbnail', 'available'),
    'thumbnailPropertiesIcon': ('Pagina-eigenschappen', 'thumbnail', 'multi-selection-disabled'),
    'selectAllIcon': ('Alle pagina’s selecteren', 'thumbnail', 'available'),
}
assert set(labels) == {m.group(1) for m in defs}
records = []
for ordinal, match in enumerate(defs, 1):
    name, raw = match.group(1, 2)
    line = code.count('\n', 0, match.start()) + 1
    # This component also imports selectAllIcon. A use before this local declaration
    # belongs to the imported vector, not to this SVG string.
    end = code.find('function TextSelectionMenuContent()', match.end()) if name != 'revealInFolderIcon' else code.find('function BookmarkMenuContent()', match.end())
    assert end > match.end()
    uses = []
    for use_match in re.finditer(r'icon=\{' + name + r'\}', code[match.end():end]):
        offset = match.end() + use_match.start()
        menu_item = code.rfind('<MenuItem', 0, offset)
        submenu = code.rfind('<Submenu', 0, offset)
        uses.append({'line': code.count('\n', 0, offset) + 1,
                     'component': 'Submenu' if submenu > menu_item else 'MenuItem'})
    assert len(uses) == (2 if name == 'thumbnailInsertIcon' else 1), (name, uses)
    svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    ET.fromstring(svg)
    filename = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower() + '.svg'
    (out / filename).write_text(svg + '\n')
    label, menu, state = labels[name]
    records.append({'file': path, 'line': line, 'ordinal': ordinal, 'definition': name,
                    'label': label, 'menu': menu, 'state': state, 'uses': uses,
                    'svg': f'inline-ui-icons/open-pdf-studio/context-menu/{filename}',
                    'sha256': hashlib.sha256((svg + '\n').encode()).hexdigest()})
assert sum(len(item['uses']) for item in records) == 15
manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'All 14 literal SVG strings in source-reachable ContextMenu.jsx. The separate imported contextMenuIcons.js catalog and its call sites remain a separate inventory. Lexical scope excludes the imported selectAllIcon in the page menu.',
            'literal_svg_definitions': 14, 'ui_icon_uses': 15, 'records': records}
(root / 'harmonization/pdf-context-literal-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{item["line"]}'
    uses = ' · '.join(f'<a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{use["line"]}">{use["component"]} L{use["line"]}</a>' for use in item['uses'])
    cards.append(f'<article data-search="{escape((item["definition"]+" "+item["label"]+" "+item["menu"]).lower())}"><h2>{escape(item["label"])}</h2><small>{escape(item["definition"])} · {escape(item["menu"])} · {escape(item["state"])}</small><div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div><a href="{url}">Definitie L{item["line"]}</a> · {uses}</article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · Contextmenu-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}article{background:#fff;border:1px solid #d8d8dc;padding:14px}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d6d6da}.samples span{display:flex;flex-direction:column;gap:3px;align-items:center}.samples small{font-size:9px}.light{background:#fafaf9}.dark{background:#303039;border-color:#53535d!important}.light img{filter:brightness(0) saturate(100%) invert(20%)}.dark img{filter:brightness(0) invert(1)}article>a{font-size:11px;color:#a95200}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · Contextmenu</h1><p>Alle 14 letterlijke SVG-definities in de bereikbare desktopcomponent; samen 15 directe UI-aanroepen. Het grotere geïmporteerde iconencatalogusbestand is een aparte audit.</p></div><main><div class="note"><strong>Lexicale scope telt.</strong> De pagina-context gebruikt een geïmporteerde <code>selectAllIcon</code>; de miniatuur-context definieert later een lokale vorm met dezelfde naam. Alleen de lokale miniatuur-aanroep hoort bij de hier getoonde SVG. <code>thumbnailInsertIcon</code> bedient twee opdrachten. Een bladzijde kan niet geknipt of verwijderd worden als dat het laatste blad zou zijn.</div><input id="search" type="search" placeholder="Zoek pictogram of menu" aria-label="Zoek pictogram of menu"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.oninput=()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
(root / 'design/pdf-context-literal-icon-review.html').write_text(page)
print('PDF ContextMenu: 14 literal UI SVG definitions, 15 direct uses')
