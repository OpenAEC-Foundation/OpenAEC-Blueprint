#!/usr/bin/env python3
"""Audit source-reachable SVG symbols in PDF Studio's annotation panel."""
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
path = 'open-pdf-studio/js/solid/components/left-panel/panels/AnnotationsPanel.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/annotations-panel'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
parent = source('open-pdf-studio/js/solid/components/left-panel/LeftPanel.jsx')
assert "import AnnotationsPanel from './panels/AnnotationsPanel.jsx'" in parent
assert '<AnnotationsPanel />' in parent
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
assert len(matches) == 14
roles = [
    ('menu-expand-all', 'Alles uitklappen · menu', 'command', 'menu', 'enabled'),
    ('menu-collapse-all', 'Alles inklappen · menu', 'command', 'menu', 'enabled'),
    ('menu-summarize', 'Samenvatten · menu', 'command', 'menu', 'always-disabled'),
    ('menu-import-comments', 'Opmerkingen importeren · menu', 'command', 'menu', 'always-disabled'),
    ('menu-export-comments', 'Opmerkingen exporteren · twee menuacties', 'command', 'menu', 'always-disabled'),
    ('menu-group-by', 'Groeperen op · submenu', 'command', 'menu', 'enabled'),
    ('menu-show', 'Tonen · submenu', 'command', 'menu', 'enabled'),
    ('toolbar-menu', 'Annotatiemenu openen', 'command', 'toolbar', 'enabled'),
    ('group-submenu-chevron', 'Groeperen op · submenu openen', 'disclosure', 'menu', 'menu-open'),
    ('show-submenu-chevron', 'Tonen · submenu openen', 'disclosure', 'menu', 'menu-open'),
    ('toolbar-expand-all', 'Alles uitklappen · werkbalk', 'command', 'toolbar', 'enabled'),
    ('toolbar-collapse-all', 'Alles inklappen · werkbalk', 'command', 'toolbar', 'enabled'),
    ('color-group-chevron', 'Kleurgroep in-/uitklappen', 'disclosure', 'group-header', 'color-sort'),
    ('other-group-chevron', 'Andere groep in-/uitklappen', 'disclosure', 'group-header', 'other-sort'),
]
assert [code.count('\n', 0, m.start()) + 1 for m in matches] == [13,14,15,16,17,18,19,203,285,305,369,378,430,442]
records = []
for ordinal, (match, (name, label, role, placement, state)) in enumerate(zip(matches, roles), 1):
    line = code.count('\n', 0, match.start()) + 1
    raw = match.group()
    variants = {'default': raw}
    if 'points={collapsedGroups().has(item.groupKey)' in raw:
        variants = {
            'expanded': re.sub(r'points=\{collapsedGroups\(\)\.has\(item\.groupKey\) \? "[^"]+" : "([^"]+)"\}', r'points="\1"', raw),
            'collapsed': re.sub(r'points=\{collapsedGroups\(\)\.has\(item\.groupKey\) \? "([^"]+)" : "[^"]+"\}', r'points="\1"', raw),
        }
    svg_files = {}
    for variant, svg in variants.items():
        assert '{' not in svg, (name, variant)
        svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        element = ET.fromstring(svg)
        assert element.tag.endswith('svg')
        svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
        filename = f'{name}{"-" + variant if variant != "default" else ""}.svg'
        (out / filename).write_text(svg)
        svg_files[variant] = {'path': f'inline-ui-icons/open-pdf-studio/annotations-panel/{filename}',
                              'sha256': hashlib.sha256(svg.encode()).hexdigest()}
    uses = []
    if ordinal <= 7:
        symbol = ['expandAllIcon', 'collapseAllIcon', 'summarizeIcon', 'importIcon',
                  'exportCommentsIcon', 'groupByIcon', 'showIcon'][ordinal - 1]
        uses = [code.count('\n', 0, m.start()) + 1 for m in re.finditer(r'innerHTML=\{' + symbol + r'\}', code)]
        assert len(uses) == (2 if symbol == 'exportCommentsIcon' else 1)
    else:
        uses = [line]
    records.append({'ordinal': ordinal, 'source_file': path, 'source_line': line,
                    'name': name, 'label': label, 'role': role, 'placement': placement,
                    'availability': state, 'render_lines': uses, 'variants': svg_files})

assert sum(len(r['render_lines']) for r in records) == 15
# Compare path/polygon geometry, ignoring whitespace and JSX-only CSS classes.
def geometry(record, variant='default'):
    svg = (root / 'harmonization' / record['variants'][variant]['path']).read_text()
    element = ET.fromstring(svg)
    return [(child.tag.split('}')[-1], tuple(sorted((k, v) for k, v in child.attrib.items()
            if k in ('d', 'points')))) for child in element.iter() if child is not element and child.tag.split('}')[-1] in ('path','polyline')]

assert geometry(records[0]) == geometry(records[10])
assert geometry(records[1]) == geometry(records[11])
assert geometry(records[8]) == geometry(records[9])
assert geometry(records[12], 'expanded') == geometry(records[13], 'expanded')
assert geometry(records[12], 'collapsed') == geometry(records[13], 'collapsed')
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'All 14 literal SVG source sites in source-reachable desktop AnnotationsPanel.jsx; all are UI symbols, including always-disabled commands. Imported contextMenuIcons.js SVGs are counted in their separate catalog.',
    'literal_svg_sites': 14, 'ui_placements': 15, 'exported_state_svgs': 16,
    'always_disabled_placements': 4,
    'shared_geometry': [['menu-expand-all','toolbar-expand-all'], ['menu-collapse-all','toolbar-collapse-all'],
                        ['group-submenu-chevron','show-submenu-chevron'],
                        ['color-group-chevron','other-group-chevron']],
    'records': records,
}
(root / 'harmonization/pdf-annotations-panel-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for r in records:
    samples = []
    for variant, value in r['variants'].items():
        src = '../harmonization/' + value['path']
        sizes = ''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
        samples.append(f'<div class="variant"><b>{escape(variant)}</b><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div></div>')
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{r["source_line"]}'
    subtitle = f'{r["placement"]} · {r["availability"]} · bron {r["source_line"]} · render {", ".join(map(str,r["render_lines"]))}'
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+subtitle).lower())}"><div class="card-top"><span class="index">{r["ordinal"]:02d}</span><span class="badge {"disabled" if r["availability"] == "always-disabled" else ""}">{escape(r["availability"])}</span></div><h2>{escape(r["label"])}</h2><p>{escape(subtitle)}</p>{"".join(samples)}<a href="{url}">Broncode ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Annotatiepaneel-iconen</title><style>
:root{font:14px/1.5 system-ui,-apple-system,sans-serif;color:#2d2e36;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1440px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:900px;color:#d5d5dd;margin:0}main{max-width:1480px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:20px}.intro p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 18px}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{width:min(420px,100%);padding:10px 12px;border:1px solid #c8c8d0;font:inherit;margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px;min-width:0}.card-top{display:flex;justify-content:space-between;align-items:center}.index{color:#a4a4ae;font-size:11px;font-weight:700}.badge{background:#e9f4ea;color:#2c6934;font-size:10px;text-transform:uppercase;letter-spacing:.04em;padding:3px 6px}.badge.disabled{background:#f9eae7;color:#a24633}h2{font-size:15px;line-height:1.3;margin:9px 0 4px}article p{font-size:11px;color:#70707a;margin:0 0 9px}.variant{margin:7px 0}.variant>b{display:block;text-transform:uppercase;font-size:10px;letter-spacing:.08em;color:#6b6b76;margin-bottom:4px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;border:1px solid #dadbe0;min-height:65px}.light{color:#303039;background:#fafafa}.forge{color:#f5f5f5;background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}article>a{display:inline-block;margin-top:7px;color:#a85500;font-size:11px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Annotatiepaneel · iconenreview</h1><p>Brongebonden inventaris van de zichtbare SVG-symbolen in het linker annotatiepaneel van Open PDF Studio, op drie groottes en twee themabackgrounds.</p></header><main><div class="intro"><strong>Wat telt mee?</strong><p>Alle 14 letterlijke SVG-bronplaatsen zijn UI-symbolen. Eén exportvorm wordt op twee menuregels gebruikt: 15 plaatsingen. Vier menuregels zijn permanent uitgeschakeld, maar hun iconen zijn zichtbaar. Twee groepchevrons hebben elk een open en gesloten variant.</p><p>De zeven geïmporteerde contextmenu-iconen staan in de <a href="pdf-context-imported-icon-review.html">aparte catalogusreview</a>. Gekleurde annotatieswatches en de statusstip zijn CSS/tekst, geen SVG-iconen. Herhaalde geometrie blijft apart op de bronplaats beoordeeld.</p></div><div class="stats"><span><strong>14</strong> SVG-bronplaatsen</span><span><strong>15</strong> UI-plaatsingen</span><span><strong>16</strong> toestands-SVG’s</span><span><strong>4</strong> permanent uitgeschakelde plaatsingen</span></div><input type="search" id="q" placeholder="Zoek icoon of rol" aria-label="Zoek icoon of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{let q=e.target.value.toLowerCase().trim();for(let card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root / 'design/pdf-annotations-panel-icon-review.html').write_text(page)
print('PDF AnnotationsPanel: 14 literal UI SVG sites, 15 placements, 16 state SVGs')
