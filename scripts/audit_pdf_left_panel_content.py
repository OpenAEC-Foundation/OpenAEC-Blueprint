#!/usr/bin/env python3
"""Pin UI-bound SVGs in six PDF left-side panel components."""
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
prefix = 'open-pdf-studio/js/solid/components/left-panel/'

def source(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{path}'], text=True)

assert source('open-pdf-studio/js/solid/App.jsx').count('<AnnotationLayersPanel />') == 1
view = source('open-pdf-studio/js/solid/components/ribbon/ViewTab.jsx')
assert 'toggleAnnotationLayersPanel' in view and 'onClick={toggleAnnotationLayersPanel}' in view
left = source(prefix + 'LeftPanel.jsx')
specs = [
    ('AnnotationLayersPanel.jsx', 'Markeringslagen', [
        ('layer-add','Laag toevoegen','toolbar-action'), ('layer-rename','Laag hernoemen','toolbar-action'),
        ('layer-up','Laag omhoog','toolbar-action'), ('layer-down','Laag omlaag','toolbar-action'),
        ('layer-delete','Laag verwijderen','toolbar-action'), ('layer-move-selection','Selectie naar laag','toolbar-action'),
    ], [21,22,23,24,25,26], 'standalone-docked-panel'),
    ('panels/AttachmentsPanel.jsx', 'Bijlagen', [
        ('attachment-add','Bijlage toevoegen','toolbar-action'), ('attachment-open','Bijlage openen','toolbar-action'),
        ('attachment-save','Bijlage opslaan','toolbar-action'), ('attachment-save-all','Alle bijlagen opslaan','toolbar-action'),
        ('attachment-delete','Bijlage verwijderen','toolbar-action'), ('attachment-file','Bijlagebestand','list-marker'),
    ], [23,31,39,47,55,79], 'left-panel-tab'),
    ('panels/FormFieldsPanel.jsx', 'Formuliervelden', [
        ('field-text','Tekstveld','field-type-marker'), ('field-checkbox','Selectievak','field-type-marker'),
        ('field-radio','Keuzerondje','field-type-marker'), ('field-combo','Keuzelijst','field-type-marker'),
        ('field-list','Lijstveld','field-type-marker'), ('field-button','Formulierknop','field-type-marker'),
    ], [7,8,9,10,11,12], 'left-panel-tab'),
    ('panels/LinksPanel.jsx', 'Koppelingen', [
        ('link-goto','Ga naar koppeling','toolbar-action'), ('link-open','Externe URL openen','toolbar-action'),
        ('link-copy','URL kopiëren','toolbar-action'), ('link-export','Koppelingen exporteren','toolbar-action'),
        ('link-internal','Interne koppeling','list-marker'), ('link-external','Externe koppeling','list-marker'),
    ], [34,42,50,58,99,104], 'left-panel-tab'),
    ('panels/BookmarksPanel.jsx', 'Bladwijzers', [
        ('bookmark-item','Bladwijzer in lijst','list-marker'), ('bookmark-add','Bladwijzer toevoegen','toolbar-action'),
        ('bookmark-add-child','Onderliggende bladwijzer','toolbar-action'), ('bookmark-edit','Bladwijzer bewerken','toolbar-action'),
        ('bookmark-delete','Bladwijzer verwijderen','toolbar-action'),
    ], [46,179,187,195,203], 'left-panel-tab'),
    ('panels/SignaturesPanel.jsx', 'Handtekeningen', [
        ('signature-unknown','Status onbekend','status-marker'), ('signature-invalid','Ongeldige handtekening','status-marker'),
        ('signature-valid','Geldige handtekening','status-marker'),
    ], [10,16,23], 'left-panel-tab'),
]
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip() == commit
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/left-panel-content'
out.mkdir(parents=True, exist_ok=True)
records = []
for relative, area, items, expected, route in specs:
    if route == 'left-panel-tab':
        component = Path(relative).stem
        assert f'import {component} from \'./{relative}\'' in left
        assert f'<{component} />' in left
    code = source(prefix + relative)
    matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
    lines = [code.count('\n',0,m.start()) + 1 for m in matches]
    assert lines == expected and len(items) == len(matches), (relative, lines)
    for match,(name,label,role),line in zip(matches,items,lines):
        svg = match.group()
        assert '{' not in svg
        saved = re.sub(r'\s+',' ',svg.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)).replace('> <','><').strip()+'\n'
        ET.fromstring(saved)
        (out/f'{name}.svg').write_text(saved)
        records.append({'name':name,'label':label,'area':area,'role':role,'route':route,
                        'source_file':prefix+relative,'source_line':line,
                        'svg':f'inline-ui-icons/open-pdf-studio/left-panel-content/{name}.svg',
                        'sha256':hashlib.sha256(saved.encode()).hexdigest()})
assert len(records) == 32
role_counts = {role:sum(r['role']==role for r in records) for role in sorted({r['role'] for r in records})}
manifest = {'repository':'open-pdf-studio','commit':commit,
            'scope':'All 32 literal SVG sites in five LeftPanel tabs and the separately docked AnnotationLayersPanel. Every site is UI-bound: toolbar action, list marker, form-field type marker, or signature status marker. No PDF document drawing content is included. The twelve vertical tab icons are imported from leftPanelIcons.js and are outside this JSX audit.',
            'literal_svg_sites':32,'ui_symbol_sites':32,'role_counts':role_counts,
            'source_layout':{'left_panel_width_px':200,'left_panel_collapsed_width_px':32,'tab_strip_width_px':32,
                             'left_panel_toolbar_button_px':26,'toolbar_svg_px':14,
                             'annotation_layers_panel_width_px':250,'annotation_layers_toolbar_button_px':22},
            'records':records}
(root/'harmonization/pdf-left-panel-content-ui-icons.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    href=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    src='../harmonization/'+r['svg']
    sizes=''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt=""><small>{n}px</small></span>' for n in (16,24,32))
    cards.append(f'<article data-area="{escape(r["area"])}"><div class="card-head"><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em></div><div class="sizes"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{href}">{escape(r["area"])} · bronregel {r["source_line"]} ↗</a></article>')

tabs=[('Bijlagen','attachment-'),('Formuliervelden','field-'),('Koppelingen','link-'),('Bladwijzers','bookmark-'),('Handtekeningen','signature-')]
def img(name):
    return '<img src="../harmonization/inline-ui-icons/open-pdf-studio/left-panel-content/'+name+'.svg" alt="">'
screens=[]
for label,stem in tabs:
    subset=[r for r in records if r['area']==label]
    tools=[r for r in subset if r['role']=='toolbar-action']
    markers=[r for r in subset if r['role']!='toolbar-action']
    toolbar='<div class="mock-toolbar">'+''.join(f'<button title="{escape(r["label"])}">{img(r["name"])}</button>' for r in tools)+'</div>' if tools else ''
    rows='<div class="mock-rows">'+''.join(f'<div class="mock-row">{img(r["name"])}<span>{escape(r["label"])}</span></div>' for r in markers)+'</div>'
    screens.append(f'<section class="mock-panel" data-panel="{escape(label)}"><div class="mock-header">{escape(label)}</div>{toolbar}{rows}<div class="mock-count">{len(markers)} voorbeeldregels</div></section>')
layer_tools=[r for r in records if r['area']=='Markeringslagen']
layer_screen='<section class="layer-panel" data-panel="Markeringslagen"><div class="mock-header">Markeringslagen <span>×</span></div><div class="mock-toolbar">'+''.join(f'<button title="{escape(r["label"])}">{img(r["name"])}</button>' for r in layer_tools)+'</div><div class="layer-columns"><span>●</span><span>NAAM</span><span>AANTAL</span><span>Z</span><span>A</span><span>S</span></div><div class="layer-row"><span>◉</span><span><i></i>Standaard</span><span>3</span><span>✓</span><span>✓</span><span>·</span></div></section>'
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Linkerpanelen</title><style>
:root{font:13px/1.5 system-ui,sans-serif;background:#f2f2f4;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:28px max(18px,calc((100vw - 1300px)/2))}header a{color:#ffcc90;font-size:12px}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{max-width:980px;color:#d7d7de;margin:0}main{max-width:1340px;margin:auto;padding:20px}.note{background:#fff;border-left:4px solid #df8421;border-top:1px solid #dcdce2;border-right:1px solid #dcdce2;border-bottom:1px solid #dcdce2;padding:14px 17px}.note p{margin:5px 0}.stats{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}.stats span{background:#fff;border:1px solid #dedee3;padding:6px 10px}.stats b{color:#a95700}.review-layout{display:grid;grid-template-columns:250px 1fr;gap:17px;margin:16px 0}.controls{background:#fff;border:1px solid #dcdce2;padding:14px}.controls label{display:block;font-weight:600;font-size:12px;margin:7px 0 5px}.controls select{font:inherit;width:100%;padding:8px}.controls p{font-size:11px;color:#777781}.stage{background:#dedee4;border:1px solid #cacad3;min-height:460px;padding:18px;display:flex;gap:0;overflow:auto}.stage.forge{background:#23232a;color:#ececf0}.vertical-tabs{width:32px;flex:0 0 32px;background:#e7e7eb;border:1px solid #cfcfd6;display:flex;flex-direction:column;align-items:center}.vertical-tabs span{width:31px;height:32px;display:flex;align-items:center;justify-content:center;border-bottom:1px solid #d6d6dc;color:#707079}.vertical-tabs span.active{border-left:2px solid #df8421;background:#fff;color:#303039}.body-mock{width:168px;min-width:168px;min-height:420px;background:#fff;border:1px solid #cfcfd6;position:relative}.stage.forge .vertical-tabs{background:#303039;border-color:#555561}.stage.forge .vertical-tabs span{border-color:#555561;color:#c8c8d1}.stage.forge .vertical-tabs span.active,.stage.forge .body-mock,.stage.forge .layer-panel{background:#34343d;color:#f1f1f4}.stage.forge .body-mock,.stage.forge .layer-panel{border-color:#5a5a65}.mock-panel{display:none;height:100%}.mock-panel.active{display:block}.mock-header{padding:6px 3px;border-bottom:1px solid #dddde2;font-size:11px;font-weight:600;display:flex;justify-content:space-between}.mock-toolbar{display:flex;gap:2px;padding:4px 8px;border-bottom:1px solid #dddde2;background:#f3f3f5}.mock-toolbar button{border:1px solid transparent;background:none;width:26px;height:26px;padding:5px;flex:0 0 26px}.mock-toolbar img{width:14px;height:14px}.mock-rows{padding:4px 8px}.mock-row{display:flex;align-items:center;gap:8px;border:1px solid #dddde2;margin-bottom:4px;padding:6px 8px;min-height:32px;font-size:11px}.mock-row img{width:16px;height:16px;flex:0 0 16px}.mock-count{position:absolute;bottom:0;width:100%;padding:6px 12px;font-size:11px;background:#f3f3f5;border-top:1px solid #dddde2}.stage.forge .mock-toolbar,.stage.forge .mock-count{background:#303039;border-color:#555561}.stage.forge .mock-header,.stage.forge .mock-row{border-color:#555561}.stage.forge img{filter:brightness(0) invert(1)}.layer-panel{display:none;margin-left:12px;width:250px;min-width:250px;min-height:420px;background:#fff;border:1px solid #cfcfd6}.layer-panel.active{display:block}.layer-panel .mock-toolbar{padding:3px 4px}.layer-panel .mock-toolbar button{width:22px;height:22px;flex-basis:22px;padding:4px}.layer-columns,.layer-row{display:grid;grid-template-columns:22px 1fr 34px 24px 24px 24px;gap:2px;align-items:center;padding:3px 4px;border-bottom:1px solid #dddde2;font-size:9px}.layer-row{font-size:10px}.layer-row i{display:inline-block;background:#d97706;width:9px;height:9px;margin-right:4px}.stage.forge .layer-columns,.stage.forge .layer-row{border-color:#555561}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}.icons article{background:#fff;border:1px solid #dadade;padding:12px}.card-head{display:flex;justify-content:space-between;gap:5px}.card-head b{font-size:12px}.card-head em{font-style:normal;color:#777781;font-size:10px}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #dcdce1}.sizes .light{background:#fafafa}.sizes .forge{background:#303039}.sizes .forge img{filter:brightness(0) invert(1)}.sizes span{display:flex;flex-direction:column;align-items:center}.sizes small{font-size:9px;color:#777781}.sizes .forge small{color:#ddd}.icons a{font-size:10px;color:#a85b00}@media(max-width:740px){main{padding:10px}.review-layout{grid-template-columns:1fr}.stage{padding:10px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · linkerpanelen en markeringslagen</h1><p>32 brongepinde UI-SVG-plaatsen in zes componenten, met 16/24/32 px-vergelijking en een schaalvaste schematische panelreview.</p></header><main><div class="note"><strong>Rolgrens.</strong><p>Werkbalkknoppen voeren opdrachten uit. Bijlage-, bladwijzer- en koppelingvormen markeren lijstitems. De zes formuliervormen benoemen veldtypen; drie handtekeningvormen geven status aan. Het gaat om vaste applicatie-UI, niet om de te tekenen PDF-inhoud.</p><p>De vijf tabpanelen zijn via `LeftPanel.jsx` bereikbaar; Markeringslagen is een afzonderlijk gedockt paneel in `App.jsx`. De verticale tabiconen komen uit `leftPanelIcons.js` en tellen niet mee in de 32 JSX-bronplaatsen. De voorbeeldregels zijn schematisch; zonder bronruntimebeelden is dit maat- en betekenisbeoordeling, geen pixelverschiltest.</p></div><div class="stats"><span><b>32</b> SVG-bronplaatsen</span><span><b>''' + str(role_counts['toolbar-action']) + '''</b> werkbalkknoppen</span><span><b>''' + str(role_counts['list-marker']) + '''</b> lijstmarkeringen</span><span><b>6</b> veldtypen</span><span><b>3</b> handtekeningstaten</span></div><div class="review-layout"><div class="controls"><label for="panel">Paneel</label><select id="panel">''' + ''.join(f'<option>{escape(name)}</option>' for name in ['Bijlagen','Bladwijzers','Formuliervelden','Koppelingen','Handtekeningen','Markeringslagen']) + '''</select><label for="theme">Thema</label><select id="theme"><option value="light">Light</option><option value="forge">Forge</option></select><p>Linkerpaneel 200 px inclusief 32 px tabstrook. Markeringslagen 250 px apart gedockt. Werkbalkknoppen 26 px; Markeringslagen 22 px. De formulier- en statusiconen zijn lijstbetekenis, geen opdracht.</p></div><div id="stage" class="stage"><div class="vertical-tabs"><span>▤</span><span>♧</span><span>✎</span><span class="active">▣</span><span>◇</span><span>▥</span><span>☷</span><span>⌁</span><span>▦</span><span>⌘</span><span>▧</span><span>▤</span></div><div class="body-mock">''' + ''.join(screens) + '''</div>''' + layer_screen + '''</div></div><div class="icons">''' + ''.join(cards) + '''</div></main><script>const panel=document.querySelector('#panel'),theme=document.querySelector('#theme'),stage=document.querySelector('#stage');function render(){const name=panel.value;stage.classList.toggle('forge',theme.value==='forge');stage.querySelector('.vertical-tabs').style.display=name==='Markeringslagen'?'none':'';stage.querySelector('.body-mock').style.display=name==='Markeringslagen'?'none':'';for(const p of stage.querySelectorAll('[data-panel]'))p.classList.toggle('active',p.dataset.panel===name)}panel.addEventListener('change',render);theme.addEventListener('change',render);render();</script></html>'''
(root/'design/pdf-left-panel-content-review.html').write_text(page)
print('PDF left panels: 32 UI SVG sites in six components; role counts', role_counts)
