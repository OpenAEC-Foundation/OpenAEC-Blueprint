#!/usr/bin/env python3
"""Audit literal SVGs in the pinned Open PDF Studio window chrome."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
base = 'open-pdf-studio/js/solid/components/'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/chrome'
out.mkdir(parents=True, exist_ok=True)

labels = {
    'TitleBar.jsx': [
        'Openen', 'Opslaan', 'Opslaan als', 'Afdrukken', 'Raster-PDF exporteren',
        'Voorkeuren', 'Ongedaan', 'Opnieuw', 'Vorige weergave', 'Volgende weergave',
        'Minimaliseren', 'Herstellen', 'Maximaliseren', 'Sluiten',
    ],
    'StatusBar.jsx': [
        'Eerste pagina', 'Vorige pagina', 'Volgende pagina', 'Laatste pagina',
        'Enkele pagina', 'Doorlopend', 'Boekweergave', 'Tegenover elkaar',
        'Uitzoomen', 'Inzoomen', 'Draaiing herstellen',
    ],
    'DocumentTabs.jsx': ['Vergelijken-tab'],
    'ribbon/Ribbon.jsx': ['Ribbon inklappen / uitklappen'],
}
app_menu_names = {
    'new': 'Nieuw', 'open': 'Openen', 'save': 'Opslaan', 'saveAs': 'Opslaan als',
    'print': 'Afdrukken', 'import': 'Importeren', 'export': 'Exporteren',
    'docProperties': 'Documenteigenschappen', 'preferences': 'Voorkeuren',
    'about': 'Over / Wat is nieuw', 'exit': 'Afsluiten',
    'extensions': 'Extensies', 'annotateScreenshot': 'Screenshot annoteren',
}
title_targets = [
    'Icon::Open', 'Icon::Save', 'Icon::SaveAs', 'Icon::Print',
    'pdf.raster-export', 'Icon::Settings', 'Icon::Undo', 'Icon::Redo',
    'pdf.previous-view', 'pdf.next-view', 'Icon::Minimize', 'Icon::Restore',
    'Icon::Maximize', 'Icon::Close',
]
status_targets = [
    'pdf.page.first', 'pdf.page.previous', 'pdf.page.next', 'pdf.page.last',
    'pdf.view.single', 'pdf.view.continuous', 'pdf.view.book', 'pdf.view.facing',
    'Icon::ZoomOut', 'Icon::ZoomIn', 'pdf.view.reset-rotation',
]
menu_targets = {
    'new': 'Icon::New', 'open': 'Icon::Open', 'save': 'Icon::Save',
    'saveAs': 'Icon::SaveAs', 'print': 'Icon::Print',
    'import': 'Icon::Import', 'export': 'Icon::Export',
    'docProperties': 'pdf.document-properties', 'preferences': 'Icon::Settings',
    'about': 'pdf.about + pdf.whats-new', 'exit': 'app.exit',
    'extensions': 'Icon::Extensions', 'annotateScreenshot': 'pdf.annotate-screenshot',
}

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True)

assert git('rev-parse', 'HEAD').strip() == commit
app = git('show', f'{commit}:open-pdf-studio/js/solid/App.jsx')
for component in ('TitleBar', 'Ribbon', 'DocumentTabs', 'StatusBar', 'AppMenu'):
    assert f'<{component} ' in app or f'<{component}/>' in app, component
records = []
for relative in (*labels, 'app-menu/AppMenu.jsx'):
    path = base + relative
    code = git('show', f'{commit}:{path}')
    matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
    expected = 14 if relative in ('TitleBar.jsx', 'app-menu/AppMenu.jsx') else 11 if relative == 'StatusBar.jsx' else 1
    assert len(matches) == expected, (relative, len(matches))
    for ordinal, match in enumerate(matches, 1):
        line = code.count('\n', 0, match.start()) + 1
        raw = match.group()
        variants = [('default', raw)]
        if relative == 'ribbon/Ribbon.jsx':
            assert "d={ribbonCollapsed() ? 'M2 4 L6 8 L10 4' : 'M2 8 L6 4 L10 8'}" in raw
            variants = [
                ('expand', raw.replace("d={ribbonCollapsed() ? 'M2 4 L6 8 L10 4' : 'M2 8 L6 4 L10 8'}", 'd="M2 4 L6 8 L10 4"')),
                ('collapse', raw.replace("d={ribbonCollapsed() ? 'M2 4 L6 8 L10 4' : 'M2 8 L6 4 L10 8'}", 'd="M2 8 L6 4 L10 8"')),
            ]
        if relative == 'app-menu/AppMenu.jsx' and ordinal <= 13:
            prefix = code[max(0, match.start() - 45):match.start()]
            key = re.search(r'(\w+):\s*\'$' , prefix)
            assert key and key.group(1) in app_menu_names, (relative, ordinal, prefix)
            name = key.group(1)
            use_lines = [i for i, row in enumerate(code.splitlines(), 1) if f'ICONS.{name}' in row]
            assert use_lines, name
            label = app_menu_names[name]
            target = menu_targets[name]
            usage = [{'file': path, 'line': use} for use in use_lines]
        else:
            label = ('Bestand: terug' if relative == 'app-menu/AppMenu.jsx' else labels[relative][ordinal - 1])
            target = ('Icon::Back' if relative == 'app-menu/AppMenu.jsx' else
                      title_targets[ordinal - 1] if relative == 'TitleBar.jsx' else
                      status_targets[ordinal - 1] if relative == 'StatusBar.jsx' else
                      'pdf.compare-tab' if relative == 'DocumentTabs.jsx' else
                      'chrome.ribbon-toggle')
            usage = [{'file': path, 'line': line}]
        if relative == 'TitleBar.jsx' and ordinal in (9, 10):
            state = 'zichtbaar-maar-uitgeschakeld'
        elif relative == 'TitleBar.jsx' and ordinal >= 11:
            state = 'tauri-venstercontrole'
        elif relative == 'DocumentTabs.jsx':
            state = 'alleen-vergelijken'
        elif relative == 'ribbon/Ribbon.jsx':
            state = 'twee-dynamische-standen'
        elif relative == 'app-menu/AppMenu.jsx':
            state = 'bestand-menu-open'
        else:
            state = 'actieve-ui-aanroep'
        group = ('titelbalk' if relative == 'TitleBar.jsx' else
                 'status' if relative == 'StatusBar.jsx' else
                 'bestand' if relative == 'app-menu/AppMenu.jsx' else
                 'document' if relative == 'DocumentTabs.jsx' else 'ribbon')
        item = {'file': path, 'line': line, 'ordinal': ordinal, 'label': label,
                'group': group, 'state': state, 'uses': usage, 'variants': [],
                'review': {'semantic_target': target,
                           'decision': ('split-two-commands' if target == 'pdf.about + pdf.whats-new' else
                                        'shared-meaning-candidate' if target.startswith('Icon::') else
                                        'requires-domain-design')}}
        for variant, svg in variants:
            svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            ET.fromstring(svg)
            svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
            stem = relative.replace('/', '-').replace('.jsx', '').lower()
            filename = f'{stem}-{ordinal:02}' + (f'-{variant}' if variant != 'default' else '') + '.svg'
            (out / filename).write_text(svg)
            item['variants'].append({'state': variant,
                                     'svg': 'inline-ui-icons/open-pdf-studio/chrome/' + filename,
                                     'sha256': hashlib.sha256(svg.encode()).hexdigest()})
        records.append(item)

assert len(records) == 41
assert sum(len(item['variants']) for item in records) == 42
assert Counter(item['group'] for item in records) == {'titelbalk': 14, 'bestand': 14, 'status': 11, 'document': 1, 'ribbon': 1}
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'All literal SVG sites in TitleBar, StatusBar, AppMenu, DocumentTabs and Ribbon on the pinned desktop Solid route; each is a UI icon, with disabled, Tauri-only and conditional states kept explicit.',
    'ui_icon_sites': len(records), 'rendered_variants': sum(len(item['variants']) for item in records),
    'records': records,
}
(root / 'harmonization/pdf-chrome-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{item["file"]}#L{item["line"]}'
    use_links = ' · '.join(
        f'<a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{use["file"]}#L{use["line"]}">UI L{use["line"]} ↗</a>'
        for use in item['uses'] if use['line'] != item['line']
    )
    samples = ''.join('<div class="variant"><span>' + escape(v['state']) + '</span><div class="samples">' + ''.join(
        f'<div><img src="../harmonization/{escape(v["svg"])}" width="{size}" height="{size}" alt=""><small>{size}</small></div>' for size in (16, 24, 32)) + '</div></div>' for v in item['variants'])
    review = item['review']
    cards.append(f'<article data-group="{escape(item["group"])}" data-search="{escape((item["label"]+" "+item["state"]+" "+item["file"]).lower())}"><h2>{escape(item["label"])}</h2><small>{escape(item["group"])} · {escape(item["state"])} · {escape(item["file"])}:{item["line"]}</small><div class="pair"><div class="light">{samples}</div><div class="dark">{samples}</div></div><p><strong>Doel:</strong> <code>{escape(review["semantic_target"])}</code><br><strong>Besluit:</strong> {escape(review["decision"])}</p><a href="{escape(url)}">Bron ↗</a> {use_links}</article>')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · chrome-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}.controls{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.controls button{padding:7px 10px;border:1px solid #c7c7cd;background:white;cursor:pointer}.controls button.active{background:#303039;color:white;border-color:#303039}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:white;border:1px solid #d8d8dc;padding:14px}article[hidden]{display:none}article h2{font-size:14px;margin:0 0 4px}article>small{display:block;color:#6c6c74;font-size:10px;overflow-wrap:anywhere}.pair{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.pair>div{padding:7px;border:1px solid #d6d6da;min-width:0}.light{background:#fafaf9}.dark{background:#303039;color:#fafaf9;border-color:#53535d!important}.samples{display:flex;justify-content:space-around;align-items:center;min-height:55px;gap:4px}.samples>div{display:flex;flex-direction:column;align-items:center;gap:3px}.samples small{font-size:9px}.variant>span{font-size:9px}.light img{filter:brightness(0) saturate(100%) invert(20%)}.dark img{filter:brightness(0) invert(1)}article>a{color:#9f5200;font-size:11px}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · vensterchrome-iconen</h1><p>41 daadwerkelijk aangeroepen JSX-SVG-plaatsen op gepinde commit f754cb7. De dynamische ribbonchevron levert twee standen, dus 42 te beoordelen vectoren. Titelbalk, Bestand-menu, status, vergelijkingstab en ribbon.</p></div><main><div class="note"><strong>Afgrenzing.</strong> De bron gebruikt hier directe UI-iconen. Het app-beeldmerk is een geïmporteerde PNG en telt niet mee. Vorige/Volgende weergave staan zichtbaar maar uitgeschakeld; vensterknoppen bestaan alleen onder Tauri; de Vergelijken-tab is conditioneel. Identieke naam betekent niet automatisch identiek commando: de twee Over/Wat-is-nieuw-rijen delen één bronvorm. Deze bronvormen zijn nog geen geharmoniseerde Rust-iconen.</div><input id="search" type="search" aria-label="Zoek icoon" placeholder="Zoek icoon of bronbestand"><div class="controls"><button class="active" data-filter="all">Alles</button><button data-filter="titelbalk">Titelbalk</button><button data-filter="bestand">Bestand</button><button data-filter="status">Status</button><button data-filter="document">Document</button><button data-filter="ribbon">Ribbon</button></div><div class="grid">''' + ''.join(cards) + '''</div></main><script>let filter='all';const search=document.querySelector('#search');function update(){for(const card of document.querySelectorAll('article'))card.hidden=!(card.dataset.search.includes(search.value.toLowerCase().trim())&&(filter==='all'||card.dataset.group===filter))}search.oninput=update;document.querySelectorAll('[data-filter]').forEach(button=>button.onclick=()=>{document.querySelectorAll('[data-filter]').forEach(other=>other.classList.toggle('active',other===button));filter=button.dataset.filter;update()});</script></html>'''
page = page.replace(
    '</div><input id="search"',
    '<p>Semantische review: 23 plaatsen passen qua opdracht bij een bestaande gedeelde <code>Icon</code>-betekenis; 17 vragen een apart PDF- of chrome-icoon; één bronvorm bedient zowel Over als Wat is nieuw en moet voor twee opdrachten worden gesplitst. De titelbalk en Bestand tonen verschillende bronvormen voor Openen, Opslaan als en Afdrukken. De bron tekent Extensies als moersleutel, terwijl de gedeelde kern een puzzelstuk gebruikt; dit blijft een visueel harmonisatiebesluit.</p></div><input id="search"',
    1,
)
page = page.replace(
    '</div></main><script>',
    '</div><section style="margin-top:24px"><h2>Native Rust-contactbladen</h2><p>Dezelfde 42 bronvarianten op 24 px, met de software-renderer van de Style Repo getekend. Dit controleert zichtbaarheid op licht en Forge, nog geen volledige PDF-schermmigratie.</p><img src="pdf-chrome-icons-light.png" alt="PDF-chrome-iconen in Light" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #d6d6da"><img src="pdf-chrome-icons-forge.png" alt="PDF-chrome-iconen in Forge" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #53535d"></section></main><script>',
    1,
)
(root / 'design/pdf-chrome-icon-review.html').write_text(page)
print(f'Open PDF chrome: {len(records)} UI SVG sites; 42 state vectors; all five chrome components covered')
