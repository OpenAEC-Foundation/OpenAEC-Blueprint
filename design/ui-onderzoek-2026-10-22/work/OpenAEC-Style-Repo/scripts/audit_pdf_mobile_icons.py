#!/usr/bin/env python3
"""Audit every literal SVG site in PDF Studio's reachable mobile route."""
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
path = 'open-pdf-studio/js/solid/MobileApp.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/mobile'
out.mkdir(parents=True, exist_ok=True)
graphics = root / 'harmonization/ui-graphics/open-pdf-studio/mobile'
graphics.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
app = source('open-pdf-studio/js/solid/App.jsx')
tools = source('open-pdf-studio/js/mobile/mobiele-gereedschappen.js')
assert "import MobileApp from './MobileApp.jsx'" in app
assert 'if (isMobile())' in app and 'return <MobileApp />;' in app
tool_names = re.findall(r"\btool: '([^']+)'", tools)
assert tool_names == ['select','highlight','draw','textbox','comment']
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
lines = [code.count('\n',0,m.start())+1 for m in matches]
assert lines == [326,335,339,353,363,391,402,412,420,427,438,447,454,466,521,535,543,550,558,574,588,601,607,640,669]
roles = [
    ('topbar-menu','Navigatiemenu openen','topbar','ui-icon','always'),
    ('theme-moon','Donkere modus inschakelen','topbar','ui-icon','when-light'),
    ('theme-sun','Lichte modus inschakelen','topbar','ui-icon','when-dark'),
    ('topbar-open','Bestand openen','topbar','ui-icon','always'),
    ('empty-document','Lege staat: document','empty-state','illustration','no-document'),
    ('toolbar-disclosure','Onderste werkbalk in-/uitklappen','toolbar','ui-icon','document-open'),
    ('page-previous','Vorige pagina','toolbar','ui-icon','document-open; RTL-swaps-action'),
    ('page-next','Volgende pagina','toolbar','ui-icon','document-open; RTL-swaps-action'),
    ('zoom-out','Uitzoomen','toolbar','ui-icon','document-open'),
    ('zoom-in','Inzoomen','toolbar','ui-icon','document-open'),
    ('rotate-page','Pagina draaien','toolbar','ui-icon','document-open'),
    ('enter-fullscreen','Volledig scherm','toolbar','ui-icon','not-fullscreen'),
    ('exit-fullscreen','Volledig scherm verlaten','toolbar','ui-icon','fullscreen'),
    ('annotation-tools','Annotatiegereedschappen openen','toolbar','ui-icon','document-open'),
    ('copy-selection','Geselecteerde tekst kopiëren','floating-action','ui-icon','text-selected'),
    ('drawer-close','Menu sluiten','drawer','ui-icon','drawer-open'),
    ('drawer-open','Bestand openen','drawer','ui-icon','drawer-open'),
    ('drawer-save','Opslaan','drawer','ui-icon','document-open'),
    ('drawer-save-as','Opslaan als','drawer','ui-icon','document-open'),
    ('recent-document','Recent bestand','drawer','ui-icon','recent-entry-exists; re-pick-prompt'),
    ('drawer-settings','Voorkeuren','drawer','ui-icon','drawer-open'),
    ('drawer-feedback','Feedback','drawer','ui-icon','drawer-open; guest-disabled'),
    ('drawer-about','Over','drawer','ui-icon','drawer-open'),
    ('annotation-tool','Gereedschap in keuzemenu','tool-menu','ui-icon','tool-menu-open'),
    ('preferences-back','Terug uit voorkeuren','preferences','ui-icon','preferences-open'),
]
assert len(roles) == len(matches) == 25
pad_block = code.split('const pad = {',1)[1].split('}[props.tool];',1)[0]
tool_shapes = {}
for tool in tool_names:
    value = re.search(r'^\s*' + tool + r':\s*(.*),\s*$', pad_block, re.M)
    assert value, tool
    tool_shapes[tool] = value.group(1).replace('<>','').replace('</>','')
toggle_match = re.compile(r'<Show when=\{toolbarCollapsed\(\)\} fallback=\{\s*(<polyline[^>]+/>)\s*\}>\s*(<polyline[^>]+/>)\s*</Show>')
records = []
for ordinal, (m, (name,label,area,kind,state)) in enumerate(zip(matches,roles),1):
    raw = m.group()
    variants = {'default': raw}
    if name == 'toolbar-disclosure':
        toggle = toggle_match.search(raw)
        assert toggle
        variants = {'expanded': raw[:toggle.start()] + toggle.group(1) + raw[toggle.end():],
                    'collapsed': raw[:toggle.start()] + toggle.group(2) + raw[toggle.end():]}
    elif name == 'annotation-tool':
        assert '{pad}' in raw
        variants = {tool: raw.replace('{pad}', shape) for tool,shape in tool_shapes.items()}
    exports = {}
    for variant,svg in variants.items():
        assert '{' not in svg, (name,variant)
        if 'xmlns=' not in svg:
            svg = svg.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)
        ET.fromstring(svg)
        svg = re.sub(r'\s+', ' ', svg).replace('> <','><').strip() + '\n'
        filename = name + (('-'+variant) if variant != 'default' else '') + '.svg'
        directory = graphics if kind == 'illustration' else out
        (directory/filename).write_text(svg)
        relative = (directory/filename).relative_to(root/'harmonization')
        exports[variant] = {'path': str(relative), 'sha256': hashlib.sha256(svg.encode()).hexdigest()}
    records.append({'ordinal':ordinal,'source_file':path,'source_line':lines[ordinal-1],
                    'name':name,'label':label,'area':area,'kind':kind,'availability':state,
                    'variants':exports})
assert sum(r['kind']=='ui-icon' for r in records)==24
assert sum(len(r['variants']) for r in records if r['kind']=='ui-icon')==29

def geometry(record,variant='default'):
    svg = (root/'harmonization'/record['variants'][variant]['path']).read_text()
    element = ET.fromstring(svg)
    return [(child.tag.split('}')[-1],tuple(sorted(child.attrib.items())))
            for child in element.iter() if child is not element]

assert geometry(records[3]) == geometry(records[16])  # open: topbar and drawer
assert geometry(records[17]) == geometry(records[18]) # save / save as collision
assert geometry(records[6]) == geometry(records[24]) # previous page / back
manifest = {'repository':'open-pdf-studio','commit':commit,
            'scope':'All 25 literal SVG sites in isMobile()-reachable MobileApp.jsx. Twenty-four sites are UI symbols, one large empty-state document is an illustration. Toolbar disclosure and ToolIcon produce conditional variants. Mobile tool list contains exactly five reachable tools.',
            'literal_svg_sites':25,'ui_icon_sites':24,'empty_state_illustrations':1,
            'exported_ui_state_svgs':29,'tool_menu_variants':5,
            'semantic_collisions':[
                {'sites':['drawer-save','drawer-save-as'],'issue':'identical geometry for Save and Save As'},
                {'sites':['page-previous','preferences-back'],'issue':'identical geometry for page navigation and leaving settings'}],
            'source_repetitions':[['topbar-open','drawer-open']],
            'records':records}
(root/'harmonization/pdf-mobile-ui-icons.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    if r['kind']!='ui-icon':continue
    samples=[]
    for variant,item in r['variants'].items():
        src='../harmonization/'+item['path']
        sizes=''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
        samples.append(f'<div class="variant"><b>{escape(variant)}</b><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div></div>')
    url=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{r["source_line"]}'
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+r["area"]+" "+r["availability"]).lower())}"><div class="top"><b>{r["ordinal"]:02d}</b><em>{escape(r["area"])}</em></div><h2>{escape(r["label"])}</h2><p>{escape(r["availability"])} · bronregel {r["source_line"]}</p>{"".join(samples)}<a href="{url}">Broncode ↗</a></article>')
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Mobiele UI-iconen</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.intro p{margin:5px 0}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}.top{display:flex;align-items:center;justify-content:space-between}.top b{font-size:11px;color:#a4a4ae}.top em{font-size:10px;font-style:normal;background:#eeeef1;color:#565663;padding:3px 7px}h2{font-size:15px;margin:10px 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.variant{margin:8px 0}.variant>b{display:block;font-size:10px;text-transform:uppercase;color:#777780;margin-bottom:4px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Mobiele PDF-route · iconenreview</h1><p>Alle zichtbare bedieningstekens uit de mobiele route op 16, 24 en 32 px, met toestands- en gereedschapsvarianten.</p></header><main><div class="intro"><strong>Brongebonden telling.</strong><p>Van 25 letterlijke SVG-plaatsen zijn er 24 UI-symbolen. De grote lege-staatdocumentvorm is een <a href="../harmonization/ui-graphics/open-pdf-studio/mobile/empty-document.svg">illustratie</a>, geen commando-icoon. De werkbalkpijl heeft twee staten; één ToolIcon-bronplaats levert vijf gereedschapsvormen.</p><p>Opslaan en Opslaan als gebruiken exact dezelfde bronvorm. De pijl voor vorige pagina is ook de terugknop van Voorkeuren. Deze betekenissen moeten bij de Rust-migratie bewust worden gescheiden. Het topbar- en drawericoon voor Openen is dezelfde vorm op twee plaatsen. De mobiele route wordt via <code>isMobile()</code> gekozen; dit is geen variant van de desktop-ribbon.</p></div><div class="stats"><span><strong>25</strong> SVG-bronplaatsen</span><span><strong>24</strong> UI-plaatsen</span><span><strong>29</strong> UI-toestandsvormen</span><span><strong>1</strong> illustratie</span></div><input id="q" type="search" placeholder="Zoek icoon of rol" aria-label="Zoek icoon of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root/'design/pdf-mobile-icon-review.html').write_text(page)
print('PDF MobileApp: 25 SVG sites; 24 UI sites, 29 state SVGs, 1 illustration')
