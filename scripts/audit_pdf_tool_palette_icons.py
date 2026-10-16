#!/usr/bin/env python3
"""Classify all literal SVGs in the reachable PDF tool palette."""
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
path = 'open-pdf-studio/js/solid/components/ToolPalette.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/tool-palette'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
app = source('open-pdf-studio/js/solid/App.jsx')
assert "from './components/ToolPalette.jsx'" in app
for component in ('DockedToolPalette', 'FloatingToolPalette', 'DockTargets'):
    assert f'<{component} ' in app or f'<{component} />' in app
assert 'icon: handIcon' in code and 'icon: selectIcon' in code and 'innerHTML={props.icon}' in code
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
roles = [
    ('hand', 'Pan/handgereedschap', 'tool', 'docked-or-floating'),
    ('select', 'Selectiegereedschap', 'tool', 'docked-or-floating'),
    ('dock-grip', 'Sleepgreep van gedockt palet', 'control-affordance', 'docked'),
    ('dock-settings', 'Instellingen / icoongrootte', 'control', 'docked'),
    ('dock-close', 'Gedockt palet sluiten', 'control', 'docked'),
    ('floating-close', 'Zwevend palet sluiten', 'control', 'floating'),
    ('dock-target-left', 'Links docken · sleepdoel', 'drag-target', 'dragging'),
    ('dock-target-right', 'Rechts docken · sleepdoel', 'drag-target', 'dragging'),
]
assert len(matches) == len(roles) == 8
assert [code.count('\n', 0, m.start()) + 1 for m in matches] == [17,18,311,323,328,358,378,386]
records = []
for ordinal, (m, (name, label, role, condition)) in enumerate(zip(matches, roles), 1):
    line = code.count('\n', 0, m.start()) + 1
    svg = m.group().replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    assert '{' not in svg
    ET.fromstring(svg)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
    filename = name + '.svg'
    (out / filename).write_text(svg)
    records.append({'ordinal': ordinal, 'name': name, 'label': label, 'role': role,
                    'availability': condition, 'source_file': path, 'source_line': line,
                    'svg': f'inline-ui-icons/open-pdf-studio/tool-palette/{filename}',
                    'sha256': hashlib.sha256(svg.encode()).hexdigest()})

manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'All eight literal SVGs in the App.jsx-reachable ToolPalette.jsx. The grip and dock targets are visual UI affordances, not ribbon commands. The 18 imported ribbonIcons.js shapes used by the tool list are covered by the imported ribbon catalog.',
            'literal_svg_sites': 8, 'ui_symbol_sites': 8,
            'tool_commands': 2, 'control_affordances': 1, 'controls': 3, 'drag_targets': 2,
            'records': records}
(root / 'harmonization/pdf-tool-palette-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for r in records:
    src = '../harmonization/' + r['svg']
    sizes = ''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{r["source_line"]}'
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+r["role"]+" "+r["availability"]).lower())}"><div class="top"><b>{r["ordinal"]:02d}</b><em>{escape(r["availability"])}</em></div><h2>{escape(r["label"])}</h2><p>{escape(r["role"])} · bronregel {r["source_line"]}</p><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{url}">Broncode ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Toolpalet-iconen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.note{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.note p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}.top{display:flex;align-items:center;justify-content:space-between}.top b{font-size:11px;color:#a4a4ae}.top em{font-size:10px;font-style:normal;background:#eeeef1;color:#565663;padding:3px 7px}h2{font-size:15px;margin:10px 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Toolpalet · iconenreview</h1><p>Alle letterlijke SVG-vormen in het bereikbare gedockte en zwevende toolpalet van Open PDF Studio.</p></header><main><div class="note"><strong>Brongebonden rol.</strong><p>De acht SVG’s zijn UI-symbolen: twee gereedschappen, vier paletbedieningen en twee dockdoelen. De sleepgreep is een bedieningsaffordance, geen commando. Dockdoelen worden alleen tijdens slepen getoond. De 18 uit <code>ribbonIcons.js</code> geïmporteerde overige gereedschapsvormen horen bij de <a href="pdf-ribbon-imported-icon-review.html">aparte ribboncatalogus</a>.</p></div><div class="stats"><span><strong>8</strong> SVG-bronplaatsen</span><span><strong>2</strong> gereedschappen</span><span><strong>2</strong> sleepdoelen</span></div><input id="q" type="search" placeholder="Zoek symbool of rol" aria-label="Zoek symbool of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root / 'design/pdf-tool-palette-icon-review.html').write_text(page)
print('PDF ToolPalette: 8 literal UI SVG sites; 2 tools, 4 controls/affordances, 2 drag targets')
