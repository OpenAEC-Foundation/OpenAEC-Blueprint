#!/usr/bin/env python3
"""Classify the eight literal UI SVGs in PDF Studio's source-reachable Home ribbon."""
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
path = 'open-pdf-studio/js/solid/components/ribbon/HomeTab.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/home-tab'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
ribbon = source('open-pdf-studio/js/solid/components/ribbon/Ribbon.jsx')
assert "import HomeTab from './HomeTab.jsx'" in ribbon
assert "<Match when={activeTab() === 'home'}><HomeTab /></Match>" in ribbon
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
roles = [
    ('new-document', 'Nieuw document', 'document', 'btn-home-new', 'always-enabled', 'Bestandsblad met plus'),
    ('ifc-report', 'IFC-report exporteren', 'export', 'btn-home-ifc-export', 'no-pdf-disabled', 'Broncomment noemt uitgaande pijl, maar SVG toont alleen een kubus; betekenis moet in harmonisatie expliciet worden ontworpen.'),
    ('cad-export', 'Naar CAD exporteren', 'export', 'btn-home-cad-export', 'no-pdf-disabled', 'Blad met polyline en uitgaande pijl'),
    ('email-pdf', 'PDF per e-mail', 'share', 'btn-home-email', 'no-pdf-disabled', 'Envelop'),
    ('raster-pdf', 'Raster-PDF exporteren', 'export', 'btn-home-raster-pdf', 'no-pdf-disabled', 'Document met afbeeldingsglyph'),
    ('screenshot-page', 'Hele pagina vastleggen', 'screenshot', 'screenshot-menu-page', 'split-menu-open', 'Camera in gedeeld screenshotmenu'),
    ('screenshot-region', 'Gebied vastleggen', 'screenshot', 'screenshot-menu-region', 'split-menu-open', 'Hoekmarkeringen en gestippeld gebied'),
    ('screenshot-overlay', 'Vorige opname als overlay plaatsen', 'screenshot', 'screenshot-menu-overlay', 'split-menu-and-capture-available', 'Twee overlappende vlakken; knop uitgeschakeld zonder eerdere opname'),
]
assert len(matches) == len(roles) == 8
assert [code.count('\n', 0, m.start()) + 1 for m in matches] == [23,25,27,29,31,99,110,123]
records = []
for ordinal, (match, (name, label, role, button_id, state, note)) in enumerate(zip(matches, roles), 1):
    line = code.count('\n', 0, match.start()) + 1
    before = code[max(0, match.start()-120):match.start()]
    if ordinal <= 5:
        symbol = re.search(r'const\s+(\w+)\s*=\s*`\s*$', before)
        assert symbol, (name, line)
        assert f'icon={{{symbol.group(1)}}}' in code
    else:
        assert f'id="{button_id}"' in code[max(0,match.start()-650):match.start()]
    svg = match.group().replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    assert '{' not in svg
    ET.fromstring(svg)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
    filename = name + '.svg'
    (out / filename).write_text(svg)
    records.append({'ordinal': ordinal, 'name': name, 'label': label, 'role': role,
                    'button_id': button_id, 'availability': state, 'source_file': path,
                    'source_line': line, 'review_note': note,
                    'svg': f'inline-ui-icons/open-pdf-studio/home-tab/{filename}',
                    'sha256': hashlib.sha256(svg.encode()).hexdigest()})

manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'All eight literal SVGs in Ribbon.jsx-reachable HomeTab.jsx. All eight are actual UI icons; three live inside the screenshot split menu. Imported ribbonIcons.js icons are in the separate imported catalog.',
            'literal_svg_sites': 8, 'ui_icon_sites': 8, 'screenshot_split_menu_icons': 3,
            'semantic_findings': ['ifc-report source comment describes outgoing arrow but path has no arrow'],
            'records': records}
(root / 'harmonization/pdf-home-tab-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for r in records:
    src = '../harmonization/' + r['svg']
    sizes = ''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{r["source_line"]}'
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+r["role"]+" "+r["availability"]).lower())}"><div class="top"><b>{r["ordinal"]:02d}</b><em>{escape(r["availability"])}</em></div><h2>{escape(r["label"])}</h2><p>{escape(r["role"])} · {escape(r["button_id"])} · bronregel {r["source_line"]}</p><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><p class="note">{escape(r["review_note"])}</p><a href="{url}">Broncode ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Start-ribbon-iconen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.intro p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}.top{display:flex;align-items:center;justify-content:space-between}.top b{font-size:11px;color:#a4a4ae}.top em{font-size:10px;font-style:normal;background:#eeeef1;color:#565663;padding:3px 7px}h2{font-size:15px;margin:10px 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}article .note{font-size:11px;margin:10px 0 0;min-height:34px}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Start-ribbon · iconenreview</h1><p>Alle letterlijke SVG-vormen in de bereikbare Start-tab van Open PDF Studio, inclusief het screenshotmenu.</p></header><main><div class="intro"><strong>Brongebonden rol.</strong><p>Vijf iconen staan op directe ribbonknoppen; drie staan in het screenshot-splitmenu. De overige Start-iconen komen uit <code>ribbonIcons.js</code> en zijn apart geïnventariseerd. De IFC-report-knop toont momenteel alleen een kubus, hoewel het broncommentaar een uitgaande pijl beschrijft: dat wordt een expliciete ontwerpbeslissing.</p></div><div class="stats"><span><strong>8</strong> SVG-bronplaatsen</span><span><strong>5</strong> hoofdknoppen</span><span><strong>3</strong> menuiconen</span></div><input id="q" type="search" placeholder="Zoek icoon of rol" aria-label="Zoek icoon of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root / 'design/pdf-home-tab-icon-review.html').write_text(page)
print('PDF HomeTab: 8 literal UI SVG sites; 5 ribbon buttons, 3 screenshot-menu items')
