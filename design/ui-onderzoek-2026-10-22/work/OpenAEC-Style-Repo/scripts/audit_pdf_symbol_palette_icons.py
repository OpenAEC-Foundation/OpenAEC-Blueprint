#!/usr/bin/env python3
"""Separate UI affordances from imported symbol content in PDF SymbolPalette."""
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
path = 'open-pdf-studio/js/solid/components/SymbolPalette.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/symbol-palette'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
app = source('open-pdf-studio/js/solid/App.jsx')
view = source('open-pdf-studio/js/solid/components/ribbon/ViewTab.jsx')
assert "from './components/SymbolPalette.jsx'" in app
for component in ('DockedSymbolPalette', 'FloatingSymbolPalette', 'SymbolSettingsDialog'):
    assert f'<{component} ' in app or f'<{component} />' in app
assert 'onClick={toggleSymbolPalette}' in view
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
assert len(matches) == 8
assert [code.count('\n', 0, m.start()) + 1 for m in matches] == [173,175,177,179,181,236,309,441]
roles = [
    ('drag-grip', 'Palet verslepen', 'control-affordance', 'docked'),
    ('search', 'Symbolen zoeken', 'search', 'docked-or-floating'),
    ('settings', 'Instellingen openen', 'control', 'docked-or-floating-or-category'),
    ('close', 'Palet of bibliotheekdialoog sluiten', 'control', 'docked-or-floating-or-dialog'),
    ('category-disclosure', 'Symboolcategorie in-/uitklappen', 'disclosure', 'category'),
    ('scale-combo-arrow', 'Plaatsingsschaalkeuze openen', 'disclosure', 'docked-or-floating'),
    ('system-types', 'Systeemtypen beheren', 'control', 'nl-ifc-bouw-category'),
]
defs = ('gripSvg', 'searchSvg', 'settingsSvg', 'closeSvg', 'arrowSvg')
records = []
for ordinal, (match, (name, label, role, condition)) in enumerate(zip(matches[:7], roles), 1):
    line = code.count('\n', 0, match.start()) + 1
    raw = match.group()
    assert '${' not in raw and '{' not in raw
    svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    ET.fromstring(svg)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
    filename = name + '.svg'
    (out / filename).write_text(svg)
    if ordinal <= 5:
        definition = defs[ordinal-1]
        uses = [code.count('\n',0,m.start())+1 for m in re.finditer(r'innerHTML=\{' + definition + r'\}',code)]
        assert len(uses) == (3 if definition in ('settingsSvg', 'closeSvg') else 1), (name,uses)
    else:
        uses = [line]
    records.append({'ordinal': ordinal, 'source_file': path, 'source_line': line,
                    'name': name, 'label': label, 'role': role, 'availability': condition,
                    'render_lines': uses, 'svg': f'inline-ui-icons/open-pdf-studio/symbol-palette/{filename}',
                    'sha256': hashlib.sha256(svg.encode()).hexdigest()})
assert sum(len(record['render_lines']) for record in records) == 11
excluded = matches[7]
assert '${dataUrl}' in excluded.group() and '<image href=' in excluded.group()
assert 'addSymbolToGroup(groupId, name, svg)' in code[excluded.end():excluded.end()+150]
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'All eight literal SVG source sites in App.jsx-reachable SymbolPalette.jsx. Seven draw UI affordances at eleven placements. The eighth wraps a user-uploaded raster image as annotation symbol content and is not a UI icon. Dynamic sym.svg and cat.icon catalog content are outside the literal-SVG count and require separate catalog inspection.',
    'literal_svg_sites': 8, 'ui_icon_or_affordance_sites': 7,
    'ui_placements': 11, 'non_icon_svg_sites': 1,
    'excluded': [{'source_file': path, 'source_line': 441, 'role': 'uploaded-raster-to-svg-content-wrapper',
                  'reason': 'The SVG contains an <image> href bound to uploaded data and is passed to addSymbolToGroup as document/symbol content, not to a UI control.'}],
    'dynamic_content_not_counted_as_literal_svg': [
        {'source_line': 290, 'expression': 'cat.icon', 'role': 'category artwork, separately catalog-driven'},
        {'source_line': 323, 'expression': 'colorizeSvg(sym.svg, cat.color)', 'role': 'placeable symbol thumbnail/content, not a fixed UI control icon'}],
    'records': records,
}
(root / 'harmonization/pdf-symbol-palette-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for r in records:
    src = '../harmonization/' + r['svg']
    sizes = ''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{r["source_line"]}'
    uses = ', '.join(map(str,r['render_lines']))
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+r["role"]+" "+r["availability"]).lower())}"><div class="top"><b>{r["ordinal"]:02d}</b><em>{escape(r["availability"])}</em></div><h2>{escape(r["label"])}</h2><p>{escape(r["role"])} · bron {r["source_line"]} · render {uses}</p><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{url}">Broncode ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Symboolpalet-iconen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.intro p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}.top{display:flex;align-items:center;justify-content:space-between}.top b{font-size:11px;color:#a4a4ae}.top em{font-size:10px;font-style:normal;background:#eeeef1;color:#565663;padding:3px 7px}h2{font-size:15px;margin:10px 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Symboolpalet · iconenreview</h1><p>Bedieningsvormen uit het bereikbare gedockte en zwevende PDF-symboolpalet, met expliciete scheiding van tekeningsymbolen.</p></header><main><div class="intro"><strong>Niet elke SVG is een UI-icoon.</strong><p>Van acht letterlijke SVG-bronplaatsen zijn er zeven UI-bedieningsvormen op elf renderplaatsen. De achtste is een SVG-container rond een geüploade rasterafbeelding en wordt als tekeningsymbool opgeslagen; die hoort niet in de iconenset.</p><p><code>cat.icon</code> en <code>sym.svg</code> laden dynamische categorie- en plaatsbare symboolafbeeldingen. De <a href="pdf-symbol-category-icon-review.html">categorie-iconen zijn apart beoordeeld</a>; de plaatsbare symboolminiaturen blijven tekeningsinhoud. Het tandwiel opent zowel de paletinstellingen als Tekeninstellingen; de betekenis volgt uit de knopcontext.</p></div><div class="stats"><span><strong>8</strong> SVG-bronplaatsen</span><span><strong>7</strong> UI-vormen</span><span><strong>11</strong> UI-plaatsingen</span><span><strong>1</strong> inhoudswrapper</span></div><input id="q" type="search" placeholder="Zoek icoon of rol" aria-label="Zoek icoon of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root / 'design/pdf-symbol-palette-icon-review.html').write_text(page)
print('PDF SymbolPalette: 8 literal SVG sites; 7 UI forms at 11 placements, 1 content wrapper')
