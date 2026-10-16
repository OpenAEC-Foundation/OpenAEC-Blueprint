#!/usr/bin/env python3
"""Distinguish built-in PDF ribbon UI icons from merely exported SVG strings."""
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
catalog_path = 'open-pdf-studio/js/solid/data/ribbonIcons.js'
consumer_prefix = 'open-pdf-studio/js/solid/components/'
consumers = ['ToolPalette.jsx'] + [f'ribbon/{name}Tab.jsx' for name in
             ('Arrange', 'Comment', 'Drawing', 'Format', 'Help', 'Home', 'Image', 'Organize', 'View')]
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/ribbon-imported'
out.mkdir(parents=True, exist_ok=True)

def source(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{path}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
catalog = source(catalog_path)
app = source('open-pdf-studio/js/solid/App.jsx')
ribbon = source(consumer_prefix + 'ribbon/Ribbon.jsx')
assert "import Ribbon from './components/ribbon/Ribbon.jsx'" in app and '<Ribbon />' in app
assert 'DockedToolPalette' in app and '<FloatingToolPalette />' in app
for path in consumers[1:]:
    component = Path(path).name
    assert f"import {component.removesuffix('.jsx')} from './{component}'" in ribbon

export_matches = list(re.finditer(r'export const (\w+) = `(<svg[\s\S]*?</svg>)`;', catalog))
assert len(export_matches) == len(re.findall(r'<svg\b', catalog)) == 122
exported_names = [match.group(1) for match in export_matches]
assert len(set(exported_names)) == 122
uses = defaultdict(list)
imports_by_file = {}
for relative in consumers:
    path = consumer_prefix + relative
    code = source(path)
    imported = re.search(r'import\s*\{([^}]+)\}\s*from\s*[\'\"](?:\.\./)+data/ribbonIcons\.js[\'\"]', code)
    assert imported, path
    names = {name.strip() for name in imported.group(1).split(',') if name.strip()}
    assert names <= set(exported_names), (path, names - set(exported_names))
    imports_by_file[path] = sorted(names)
    for name in names:
        for use_match in re.finditer(r'\b' + name + r'\b', code[imported.end():]):
            offset = imported.end() + use_match.start()
            line = code.count('\n', 0, offset) + 1
            source_line = code.splitlines()[line - 1].strip()
            assert any(key in source_line for key in ('icon=', 'icon:', 'innerHTML', 'svg=', 'Icon', 'icon}', 'icon,')), (path, name, line)
            uses[name].append({'file': path, 'line': line, 'source_excerpt': source_line[:180]})

records = []
same = defaultdict(list)
for ordinal, match in enumerate(export_matches, 1):
    name, raw = match.group(1, 2)
    line = catalog.count('\n', 0, match.start()) + 1
    svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    ET.fromstring(svg)
    digest = hashlib.sha256((svg + '\n').encode()).hexdigest()
    same[digest].append(name)
    call_sites = sorted(uses[name], key=lambda use: (use['file'], use['line']))
    record = {'catalog_file': catalog_path, 'definition_line': line, 'ordinal': ordinal,
              'name': name, 'classification': 'built-in-ui-icon' if call_sites else 'extension-addressable-only',
              'uses': call_sites, 'sha256': digest}
    if call_sites:
        filename = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower() + '.svg'
        (out / filename).write_text(svg + '\n')
        record['svg'] = f'inline-ui-icons/open-pdf-studio/ribbon-imported/{filename}'
        if '<text' in svg:
            record['native_preview_limitation'] = 'Iced omits source SVG <text> glyph'
    records.append(record)

built_in = [record for record in records if record['classification'] == 'built-in-ui-icon']
assert len(built_in) == 109 and len(records) - len(built_in) == 13
assert sum(len(record['uses']) for record in records) == 146
assert {record['name'] for record in records if record['classification'] != 'built-in-ui-icon'} == {
    'screenshotDropdownArrow', 'screenshotPageMenuIcon', 'screenshotRegionMenuIcon',
    'textAnnotIcon', 'northArrowIcon', 'calibrateIcon', 'snapToDrawingIcon',
    'undoIcon', 'thinLinesIcon', 'themeDropdownArrow', 'styleMoreArrow',
    'colorDropdownArrow', 'dropdownArrowSmall',
}
collision_review = {
    ('fitWidthIcon', 'fitPageIcon'): 'Splits aanpassen aan breedte en volledige pagina: dezelfde hoeken zeggen niet welke maat leidend is.',
    ('actualSizeIcon', 'findIcon'): 'Ware grootte en zoeken moeten verschillende tekens krijgen; het huidige vergrootglas verbergt het verschil.',
    ('editTextIcon', 'textAnnotIcon'): 'Tekst bewerken is ingebouwd; textAnnotIcon heeft hier geen ingebouwde aanroep. Bewaar de betekenissen apart.',
    ('clearPageIcon', 'deletePageIcon'): 'Pagina-inhoud wissen en pagina verwijderen hebben verschillende destructieve reikwijdte.',
    ('singlePageIcon', 'continuousIcon', 'fileAssocIcon'): 'Enkele pagina, doorlopend lezen en bestandsassociatie mogen niet hetzelfde documentblad blijven.',
    ('bookViewIcon', 'shortcutsIcon'): 'Boekweergave en sneltoetsen verwijzen naar verschillende objecten.',
    ('navigationIcon', 'manageWatermarksIcon'): 'Navigatie en watermerkbeheer vragen om onderscheidende objecten.',
}
assert {tuple(names) for names in same.values() if len(names) > 1} == set(collision_review)
collision_groups = [{'names': list(names), 'assessment': collision_review[tuple(names)]}
                    for names in same.values() if len(names) > 1]
manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'Every SVG export in ribbonIcons.js, checked against the ten source-reachable built-in Solid consumers. A plugin registry also exposes this entire catalog by name, but that alone is not evidence of an icon on a built-in screen. Source token uses after import are checked to be icon/SVG contexts.',
            'catalog_svg_exports': len(records), 'built_in_ui_icons': len(built_in),
            'extension_addressable_only': len(records) - len(built_in),
            'built_in_symbol_references': sum(len(record['uses']) for record in records),
            'consumer_files': consumers, 'imports_by_file': imports_by_file,
            'identical_source_shapes': collision_groups,
            'records': records}
(root / 'harmonization/pdf-ribbon-imported-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    source_url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{catalog_path}#L{item["definition_line"]}'
    if item['uses']:
        samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
        body = f'<div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div>'
        if 'native_preview_limitation' in item:
            body += f'<p class="warning">{escape(item["native_preview_limitation"])}</p>'
        body += '<div class="uses">' + ' · '.join(f'<a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{use["file"]}#L{use["line"]}">{escape(Path(use["file"]).name)} L{use["line"]}</a>' for use in item['uses']) + '</div>'
    else:
        body = '<p class="excluded">Geen aanroep in de ingebouwde UI gevonden. De export blijft via het extensieregister op naam beschikbaar.</p>'
    cards.append(f'<article data-kind="{escape(item["classification"])}" data-search="{escape((item["name"]+" "+" ".join(use["file"] for use in item["uses"])).lower())}"><h2>{escape(item["name"])}</h2><small>{escape(item["classification"])} · {len(item["uses"])} aanroep(en)</small>{body}<a href="{source_url}">Definitie L{item["definition_line"]} ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · Geïmporteerde ribboniconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1400px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}main{max-width:1440px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.stats span{background:#fff;border:1px solid #d8d8dc;padding:7px 10px}.stats b{color:#a95200}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}article{background:#fff;border:1px solid #d8d8dc;padding:14px}article[data-kind=extension-addressable-only]{background:#f9f9fa}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d6d6da}.samples span{display:flex;flex-direction:column;gap:3px;align-items:center}.samples small{font-size:9px}.light{background:#fafaf9;color:#303039}.dark{background:#303039;color:#fff;border-color:#53535d!important}.uses{font-size:11px;line-height:1.7;margin:8px 0}.warning{font-size:11px;color:#a95200}.excluded{font-size:11px;color:#696972;min-height:75px}article a{font-size:11px;color:#a95200}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · gedeelde ribboniconen</h1><p>Alle 122 SVG-exports uit ribbonIcons.js zijn tegen de tien bereikbare Solid-consumenten gecontroleerd. Alleen aantoonbare ingebouwde UI-aanroepen tellen als huidige iconen.</p></div><main><div class="note"><strong>Bron en bereikbaarheid.</strong> 109 vormen hebben samen 146 referenties in de ingebouwde UI. Dertien exports hebben daar geen aanroep, maar blijven op naam beschikbaar voor extensies. Deze 122 zijn dus geen 122 bewezen zichtbare iconen. Bronvormen in de HTML worden niet globaal monochroom gefilterd; eventuele bronkleuren blijven zichtbaar. Twee gebruikte vormen bevatten SVG-tekst die de huidige native renderer niet tekent.</div><div class="stats"><span><b>109</b> ingebouwd gebruikt</span><span><b>13</b> alleen extensie-adresseerbaar</span><span><b>146</b> bronreferenties</span><span><b>10</b> ingebouwde consumenten</span></div><input id="search" type="search" placeholder="Zoek icoon of bronbestand" aria-label="Zoek icoon of bronbestand"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.oninput=()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
collisions = ''.join(f'<li><strong>{escape(" / ".join(group["names"]))}</strong><br>{escape(group["assessment"])}</li>' for group in collision_groups)
page = page.replace('</div></main><script>', '''</div><section class="assessment"><h2>Identieke bronvorm, andere betekenis</h2><p>Zeven vormgroepen zijn byte-identiek. Hun semantiek mag in de Rust-crate niet worden samengevoegd op basis van de SVG-hash.</p><ul>''' + collisions + '''</ul><h2>Native Rust-contactbladen</h2><p>Alle 109 ingebouwd gebruikte bronvormen op 24 px. De T in Tekst toevoegen en Tekstvak ontbreekt in deze Iced-renderer, omdat beide bron-SVG’s een <code>&lt;text&gt;</code>-element gebruiken. Daarvoor zijn nog vectorvarianten nodig.</p><img src="pdf-ribbon-imported-icons-light.png" alt="PDF-ribbonbronvormen in Light"><img src="pdf-ribbon-imported-icons-forge.png" alt="PDF-ribbonbronvormen in Forge"></section></main><script>''', 1)
page = page.replace('.excluded{font-size:11px;color:#696972;min-height:75px}', '.excluded{font-size:11px;color:#696972;min-height:75px}.assessment{margin-top:24px;background:#fff;padding:18px;border:1px solid #d8d8dc}.assessment ul{columns:2;padding-left:20px}.assessment li{break-inside:avoid;margin:0 0 10px}.assessment img{display:block;max-width:100%;height:auto;margin:12px 0;border:1px solid #d6d6da}')
(root / 'design/pdf-ribbon-imported-icon-review.html').write_text(page)
print('PDF ribbonIcons: 122 exports; 109 built-in-used, 13 extension-addressable only; 146 references')
