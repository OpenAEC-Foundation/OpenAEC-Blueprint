#!/usr/bin/env python3
"""Link the PDF context-menu SVG catalog to live Solid menu call sites."""
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
catalog_path = 'open-pdf-studio/js/solid/data/contextMenuIcons.js'
component_path = 'open-pdf-studio/js/solid/components/ContextMenu.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/context-imported'
out.mkdir(parents=True, exist_ok=True)

def source(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{path}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
catalog, component = source(catalog_path), source(component_path)
app = source('open-pdf-studio/js/solid/App.jsx')
assert "import ContextMenu from './components/ContextMenu.jsx'" in app and '<ContextMenu />' in app
assert "from '../data/contextMenuIcons.js'" in component
export_matches = list(re.finditer(r'export const (\w+) = `(<svg[\s\S]*?</svg>)`;', catalog))
assert len(export_matches) == 52
names = [match.group(1) for match in export_matches]
assert len(set(names)) == 52
import_block = re.search(r'import\s*\{([^}]+)\}\s*from\s*[\'\"]\.\./data/contextMenuIcons\.js[\'\"]', component)
assert import_block
imports = {name.strip() for name in import_block.group(1).split(',') if name.strip()}
assert imports == set(names)
start = component.index('function LayerSubmenu')
shadow = component.index('  const selectAllIcon =', start)
menus = ['LayerSubmenu', 'AnnotationMenuContent', 'MultiAnnotationMenuContent',
         'PageMenuContent', 'ThumbnailMenuContent', 'TextSelectionMenuContent']
menu_starts = [(component.index('function ' + name + '('), name) for name in menus]

records = []
for ordinal, match in enumerate(export_matches, 1):
    name, raw = match.group(1, 2)
    definition_line = catalog.count('\n', 0, match.start()) + 1
    end = shadow if name == 'selectAllIcon' else len(component)
    uses = []
    for use_match in re.finditer(r'\b' + name + r'\b', component[start:end]):
        offset = start + use_match.start()
        line = component.count('\n', 0, offset) + 1
        menu = max((entry for entry in menu_starts if entry[0] <= offset), default=None)
        assert menu, (name, line)
        before_line = component.rfind('\n', 0, offset) + 1
        after_line = component.find('\n', offset)
        source_line = component[before_line:after_line].strip()
        uses.append({'file': component_path, 'line': line, 'menu': menu[1],
                     'source_excerpt': source_line[:180]})
    assert uses, f'unused catalog export: {name}'
    assert '<svg' in raw and '</svg>' in raw
    svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    ET.fromstring(svg)
    filename = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower() + '.svg'
    (out / filename).write_text(svg + '\n')
    records.append({'catalog_file': catalog_path, 'definition_line': definition_line,
                    'ordinal': ordinal, 'name': name, 'uses': uses,
                    'condition': ('always-disabled-page-action' if name in ('pageCutIcon', 'pageCopyIcon', 'pageDeleteIcon') else
                                  'dynamic-alternative' if name in ('lockedIcon', 'unlockedIcon') else
                                  'conditional-menu-or-selection'),
                    'svg': f'inline-ui-icons/open-pdf-studio/context-imported/{filename}',
                    'sha256': hashlib.sha256((svg + '\n').encode()).hexdigest()})

assert len(records) == 52
assert sum(len(record['uses']) for record in records) == 69
unique_sites = {(use['file'], use['line']) for record in records for use in record['uses']}
assert len(unique_sites) == 67
assert len(next(record for record in records if record['name'] == 'selectAllIcon')['uses']) == 1
same = defaultdict(list)
for record in records:
    same[record['sha256']].append(record['name'])
manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'All exports of contextMenuIcons.js are imported by source-reachable ContextMenu.jsx. Uses are token occurrences in its menu functions after imports. The later local selectAllIcon shadows the imported name in ThumbnailMenuContent and is excluded here. Two dynamic lock/unlock alternatives share JSX sites.',
            'catalog_exports': 52, 'used_exports': 52, 'symbol_references': 69,
            'distinct_source_lines_with_use': len(unique_sites),
            'same_exact_svg_groups': [names for names in same.values() if len(names) > 1],
            'records': records}
(root / 'harmonization/pdf-context-imported-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
    source_url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{catalog_path}#L{item["definition_line"]}'
    use_links = ' · '.join(f'<a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{component_path}#L{use["line"]}">{escape(use["menu"])} L{use["line"]}</a>' for use in item['uses'])
    cards.append(f'<article data-search="{escape((item["name"]+" "+" ".join(use["menu"] for use in item["uses"])).lower())}"><h2>{escape(item["name"])}</h2><small>{len(item["uses"])} aanroep(en) · {escape(item["condition"])}</small><div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div><a href="{source_url}">Brondefinitie L{item["definition_line"]}</a><div class="uses">{use_links}</div></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · Geïmporteerde contextmenu-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}article{background:#fff;border:1px solid #d8d8dc;padding:14px}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d6d6da}.samples span{display:flex;flex-direction:column;gap:3px;align-items:center}.samples small{font-size:9px}.light{background:#fafaf9;color:#303039}.dark{background:#303039;color:#fff;border-color:#53535d!important}article a{font-size:11px;color:#a95200}.uses{margin-top:7px;font-size:11px}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · geïmporteerd contextmenu</h1><p>52 SVG-exports uit het broncatalogusbestand zijn daadwerkelijk aanroepbaar in ContextMenu.jsx. Elke vorm is op 16, 24 en 32 px in Light en Forge te beoordelen.</p></div><main><div class="note"><strong>Scope van deze audit.</strong> De 52 exports leveren 69 symboolreferenties op 67 bronregels. Twee lock/unlock-alternatieven delen telkens een menuplaats. De geïmporteerde <code>selectAllIcon</code> hoort bij de pagina; de lokale vorm met dezelfde naam hoort bij de miniaturen en staat in de <a href="pdf-context-literal-icon-review.html">letterlijke-SVG-review</a>. Knippen, kopiëren en verwijderen in het pagina-contextmenu zijn zichtbaar maar permanent uitgeschakeld. Kleuren in de acht schikiconen zijn bronkleuren en blijven daarom behouden.</div><input id="search" type="search" placeholder="Zoek icoon of menu" aria-label="Zoek icoon of menu"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.oninput=()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
page = page.replace('</div></main><script>', '''</div><section class="native"><h2>Native Rust-renders</h2><p>Bronvormen op 24 px in de Iced-renderer. De acht meerkleurige schikiconen zijn zonder globale SVG-tint gerenderd; bij de overige vormen is de thematekstkleur toegepast. Dit onderscheid moet in de gedeelde Rust-component expliciet blijven.</p><img src="pdf-context-imported-icons-light.png" alt="Geïmporteerde PDF-contextmenu-iconen in Light"><img src="pdf-context-imported-icons-forge.png" alt="Geïmporteerde PDF-contextmenu-iconen in Forge"></section></main><script>''', 1)
page = page.replace('.uses{margin-top:7px;font-size:11px}', '.uses{margin-top:7px;font-size:11px}.native{margin-top:24px}.native img{display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #d6d6da}')
(root / 'design/pdf-context-imported-icon-review.html').write_text(page)
print('PDF ContextMenu imports: 52 used SVG exports; 69 references on 67 source lines')
