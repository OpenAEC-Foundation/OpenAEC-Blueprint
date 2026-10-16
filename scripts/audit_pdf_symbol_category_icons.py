#!/usr/bin/env python3
"""Inventory category-header UI icons loaded into PDF Studio's symbol palette."""
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
prefix = 'open-pdf-studio/js/solid/'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/symbol-categories'
out.mkdir(parents=True, exist_ok=True)

def source(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{prefix}{path}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
palette = source('components/SymbolPalette.jsx')
store = source('stores/symbolStore.js')
assert 'innerHTML={cat.icon}' in palette
assert '...NL_CATEGORIES' in store and '...NEN1414_CATEGORIES' in store and '...custom' in store
assert 'export const BUILT_IN_CATEGORIES = []' in source('data/symbolLibrary.js')
assert 'export const INB_CATEGORIES = []' in source('data/inbSymbolLibrary.js')
nl = source('data/nlSymbolLibrary.js')
nen = source('data/nen1414Library.js')

records = []
def add(name, label, src_path, body, match, occurrence, state):
    svg = match.group(1).replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    assert '${' not in svg and '{' not in svg
    ET.fromstring(svg)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
    filename = name + '.svg'
    (out / filename).write_text(svg)
    records.append({'name': name, 'label': label, 'source_file': prefix + src_path,
                    'source_line': body.count('\n', 0, match.start()) + 1,
                    'category_instances': occurrence, 'availability': state,
                    'render_expression': 'cat.icon in SymbolPalette.jsx:290',
                    'svg': f'inline-ui-icons/open-pdf-studio/symbol-categories/{filename}',
                    'sha256': hashlib.sha256(svg.encode()).hexdigest(),
                    'native_preview_limitation': 'SVG <text> may disappear in the Iced software renderer; use vector paths before canonical adoption' if '<text' in svg else None})

nl_matches = list(re.finditer(r'\bicon:\s*`(<svg\b[\s\S]*?</svg>)`', nl))
assert len(nl_matches) == 5
for match in nl_matches:
    prior = nl[:match.start()]
    cat_id = re.findall(r"\bid:\s*'([^']+)'", prior)[-1]
    label = re.findall(r"\bname:\s*'([^']+)'", prior)[-1]
    assert cat_id.startswith('nl-')
    add(cat_id, label, 'data/nlSymbolLibrary.js', nl, match, 1, 'built-in-category; locale-filtered')

nen_matches = list(re.finditer(r'\bicon:\s*`(<svg\b[\s\S]*?</svg>)`', nen))
assert len(nen_matches) == 1
names_block = nen.split('const NAMES = {',1)[1].split('\n};',1)[0]
ids = re.findall(r"^\s*'([^']+)':", names_block, re.M)
def category_prefix(symbol_id):
    return next((p for p in ('Tbk','Tb','Td','Tn','Tr','Tv','Tw') if symbol_id.startswith(p)), 'Tb')
nen_prefixes = sorted({category_prefix(symbol_id) for symbol_id in ids})
assert nen_prefixes == ['Tb','Tbk','Td','Tn','Tr','Tv','Tw']
add('nen1414-category', 'NL NEN 1414 · categorieletter N', 'data/nen1414Library.js', nen,
    nen_matches[0], len(nen_prefixes), 'seven-built-in-locale-filtered-categories')

custom_matches = list(re.finditer(r'\bicon:\s*`(<svg\b[\s\S]*?</svg>)`', store))
assert len(custom_matches) == 1
add('custom-group', 'Eigen symboolgroep', 'stores/symbolStore.js', store,
    custom_matches[0], 'one per user-created group', 'only-when-custom-group-exists')
assert len(records) == 7
manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'Category-header SVGs passed as cat.icon to the source-reachable SymbolPalette.jsx. Five NL categories, one NEN1414 template instantiated for seven prefixes, and one optional custom-group template. Empty built-in/INB arrays have no rendered categories. Placeable sym.svg thumbnails are document content and excluded.',
            'svg_definition_sites': 7, 'built_in_category_instances': 12,
            'optional_custom_category_instances': 'one per created group',
            'non_icon_symbol_thumbnails_excluded': True,
            'records': records}
(root / 'harmonization/pdf-symbol-category-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for record in records:
    src = '../harmonization/' + record['svg']
    sizes = ''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{record["source_file"]}#L{record["source_line"]}'
    note = f'<p class="warning">{escape(record["native_preview_limitation"])}</p>' if record['native_preview_limitation'] else ''
    cards.append(f'<article data-search="{escape((record["name"]+" "+record["label"]+" "+record["availability"]).lower())}"><h2>{escape(record["label"])}</h2><p>{escape(record["name"])} · {escape(str(record["category_instances"]))} categorieplaats(en) · regel {record["source_line"]}</p><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div>{note}<a href="{url}">Broncode ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Symboolcategorie-iconen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.intro p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}h2{font-size:15px;margin:0 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}.warning{color:#aa5700}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Symboolcategorieën · iconenreview</h1><p>Dynamisch in het PDF-symboolpalet geladen categorie-iconen, gescheiden van plaatsbare tekeningsymbolen.</p></header><main><div class="intro"><strong>Brongebonden telling.</strong><p>Vijf NL-categorieën hebben een eigen pictogram. De zeven NEN 1414-categorieën delen één letter-N-template. Een eigen groep krijgt een plus-in-kader-template zodra de gebruiker haar aanmaakt. De ingebouwde en INB-arrays zijn momenteel leeg.</p><p>De <a href="pdf-symbol-palette-icon-review.html">paletbediening</a> is apart beoordeeld. Miniaturen uit <code>sym.svg</code> kunnen als annotatie op de PDF worden geplaatst en zijn daarom geen vaste UI-commando-iconen. De NEN-vorm gebruikt SVG-tekst; native Rust-rendering vraagt een vectorvariant.</p></div><div class="stats"><span><strong>7</strong> SVG-definities</span><span><strong>12</strong> ingebouwde categorieplaatsen</span><span>eigen groepen: <strong>variabel</strong></span></div><input id="q" type="search" placeholder="Zoek categorie" aria-label="Zoek categorie"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root / 'design/pdf-symbol-category-icon-review.html').write_text(page)
print('PDF symbol categories: 7 SVG definitions, 12 built-in category instances, optional custom instances')
