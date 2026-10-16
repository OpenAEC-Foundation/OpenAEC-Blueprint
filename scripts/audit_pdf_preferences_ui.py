#!/usr/bin/env python3
"""Review PDF preferences tab and selector SVGs plus source layout."""
import ast
import hashlib
import json
import re
import subprocess
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root=Path(__file__).resolve().parents[1]
repo=Path('/tmp/openaec-inventory/open-pdf-studio')
commit='f754cb7c9d9adf654f6894cee15543413c24fcff'
prefix='open-pdf-studio/js/solid/components/preferences/'

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
host=source('open-pdf-studio/js/solid/components/DialogHost.jsx')
app=source('open-pdf-studio/js/solid/App.jsx')
menu=source('open-pdf-studio/js/solid/components/app-menu/AppMenu.jsx')
assert "import PreferencesDialog from './preferences/PreferencesDialog.jsx'" in host
assert "'preferences': PreferencesDialog" in host
assert 'showPreferencesDialog' in menu and 'onClick={() => actionAndClose(showPreferencesDialog)}' in menu
assert 'if (isMobile())' in app and 'return <MobileApp />' in app and '<DialogHost />' in app
specs=[
 ('PreferencesDialog.jsx','Tabs',[
  ('pref-general','Algemeen','tab-icon'),('pref-annotations','Annotaties','tab-icon'),
  ('pref-behavior','Gedrag','tab-icon'),('pref-fileassoc','Bestandskoppeling','tab-icon'),
  ('pref-page-display','Paginaweergave','tab-icon'),('pref-vprinter','Virtuele printer','tab-icon'),
 ],[30,35,40,45,50,55]),
 ('PrefColorPicker.jsx','Kleurkiezer',[
  ('color-dropdown','Kleurkeuze openen','selector-chevron'),('color-none','Geen kleur','picker-action'),
  ('color-more','Meer kleuren','picker-action'),
 ],[79,86,117]),
 ('LanguageSelect.jsx','Taalkeuze',[
  ('language-dropdown','Taalkeuze openen','selector-chevron'),
 ],[82]),
 ('PrefComboBox.jsx','Numerieke keuze',[
  ('combo-dropdown','Waardenlijst openen','selector-chevron'),
 ],[75]),
 ('PrefSelect.jsx','Lijstkeuze',[
  ('select-dropdown','Opties openen','selector-chevron'),
 ],[26]),
]
dialog=source(prefix+'PreferencesDialog.jsx')
assert "import GeneralTab from './GeneralTab.jsx'" in dialog
assert "import AnnotationsTab from './AnnotationsTab.jsx'" in dialog
assert "isMobile() ? TAB_IDS.filter(t => !DESKTOP_ONLY_TABS.includes(t.id)) : TAB_IDS" in dialog
assert "const DESKTOP_ONLY_TABS = ['fileassoc', 'vprinter']" in dialog
for name in ('PrefColorPicker','PrefComboBox','PrefSelect'):
    assert f"import {name} from './{name}.jsx'" in source(prefix+'AnnotationsTab.jsx')
assert "import LanguageSelect from './LanguageSelect.jsx'" in source(prefix+'GeneralTab.jsx')

out=root/'harmonization/inline-ui-icons/open-pdf-studio/preferences'
out.mkdir(parents=True,exist_ok=True)
records=[]
for filename,area,items,expected in specs:
    code=source(prefix+filename)
    matches=list(re.finditer(r'<svg\b[\s\S]*?</svg>',code))
    lines=[code.count('\n',0,m.start())+1 for m in matches]
    assert lines==expected and len(items)==len(matches),(filename,lines)
    for match,(name,label,role),line in zip(matches,items,lines):
        svg=match.group()
        assert '{' not in svg
        saved=re.sub(r'\s+',' ',svg.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)).replace('> <','><').strip()+'\n'
        ET.fromstring(saved)
        (out/f'{name}.svg').write_text(saved)
        records.append({'name':name,'label':label,'area':area,'role':role,
                        'source_file':prefix+filename,'source_line':line,
                        'svg':f'inline-ui-icons/open-pdf-studio/preferences/{name}.svg',
                        'sha256':hashlib.sha256(saved.encode()).hexdigest()})
assert len(records)==12
by_name={r['name']:r for r in records}
def child_geometry(name):
    el=ET.fromstring((root/'harmonization'/by_name[name]['svg']).read_text())
    return [(node.tag.split('}')[-1],tuple(sorted(node.attrib.items()))) for node in el.iter() if node is not el]
assert len({str(child_geometry(n)) for n in ('color-dropdown','language-dropdown','combo-dropdown','select-dropdown')})==1
color_code=source(prefix+'PrefColorPicker.jsx')
palette=ast.literal_eval(re.search(r'const PALETTE_COLUMNS = (\[[\s\S]*?\]);',color_code).group(1))
assert len(palette)==7 and all(len(col)==6 for col in palette)
css=source('open-pdf-studio/styles/dialogs.css')
for needle in ('.preferences-dialog { width: 600px; height: 520px; }','width: 140px;','padding: 8px 0;','gap: 2px;','width: 14px;','width: 12px;'):
    assert needle in css
manifest={'repository':'open-pdf-studio','commit':commit,
          'scope':'Twelve literal UI SVGs across five source-reachable preferences components. Six are tab icons; four are instances of one selector-chevron geometry; two are color-picker actions. The 42 palette color swatches are CSS blocks, not SVG icons. The current App.jsx mobile branch renders MobileApp instead of DialogHost, so the isMobile tab filter inside PreferencesDialog is not evidence that this desktop dialog appears on mobile.',
          'literal_svg_sites':12,'ui_symbol_sites':12,'tab_icons':6,'identical_chevron_sites':4,
          'palette_columns':palette,'palette_color_cells':42,
          'layout':{'desktop_dialog_px':[600,520],'tab_sidebar_px':140,'tab_icon_px':14,
                    'selector_chevron_px':12,'language_dropdown_width_px':260,
                    'language_dropdown_max_height_px':280,'color_picker_width_px':140,
                    'color_dropdown_width_px':200,'color_swatch_px':20},
          'route_note':'App.jsx chooses MobileApp when isMobile() is true; this desktop PreferencesDialog is shown through DialogHost and AppMenu.',
          'records':records}
(root/'harmonization/pdf-preferences-ui-icons.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

def img(name,n=14):
    return f'<img src="../harmonization/inline-ui-icons/open-pdf-studio/preferences/{name}.svg" width="{n}" height="{n}" alt="">'
tabs=[('pref-general','Algemeen'),('pref-annotations','Annotaties'),('pref-behavior','Gedrag'),
      ('pref-page-display','Paginaweergave'),('pref-fileassoc','Bestandskoppeling'),('pref-vprinter','Virtuele printer')]
tab_html=''.join(f'<button class="tab" data-tab="{name}">{img(name)}<span>{escape(label)}</span></button>' for name,label in tabs)
swatches=''.join('<div class="swatch-column">'+''.join(f'<button style="background:{color}" title="{color}" data-color="{color}" aria-label="{color}"></button>' for color in col)+'</div>' for col in palette)
cards=[]
for r in records:
    src='../harmonization/'+r['svg']
    sizes=''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt=""><small>{n}px</small></span>' for n in (16,24,32))
    href=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    cards.append(f'<article><div class="card-head"><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em></div><div class="sizes"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{href}">{escape(r["area"])} · bronregel {r["source_line"]} ↗</a></article>')

page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Voorkeurenreview</title><style>
:root{font:13px/1.5 system-ui,sans-serif;background:#f2f2f4;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:28px max(18px,calc((100vw - 1280px)/2))}header a{font-size:12px;color:#ffcb89}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{margin:0;max-width:940px;color:#d7d7de}main{max-width:1320px;margin:auto;padding:20px}.note{background:#fff;border:1px solid #dcdce2;border-left:4px solid #df8421;padding:14px 17px}.note p{margin:5px 0}.metrics{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}.metrics span{background:#fff;border:1px solid #dedee3;padding:6px 10px}.metrics b{color:#a95700}.controls{display:flex;gap:10px;align-items:center;margin:15px 0}.controls select{font:inherit;padding:7px}.stage{background:#dddddf;border:1px solid #c8c8cf;padding:20px;overflow:auto}.stage.forge{background:#202026}.dialog{width:600px;height:520px;background:#fff;border:1px solid #d4d4d4;box-shadow:0 2px 10px #0004;display:flex;flex-direction:column}.stage.forge .dialog{background:#303039;color:#f0f0f4;border-color:#5a5a62}.dialog-header{height:30px;min-height:30px;display:flex;align-items:center;justify-content:space-between;padding-left:10px;background:linear-gradient(#fff,#f5f5f5);border-bottom:1px solid #d4d4d4;font-size:12px;font-weight:600}.dialog-header span{width:30px;text-align:center}.stage.forge .dialog-header{background:linear-gradient(#373740,#303039);border-color:#5a5a62}.dialog-body{flex:1;min-height:0;display:flex}.sidebar{width:140px;min-width:140px;background:#f5f5f5;border-right:1px solid #d4d4d4;padding:8px 0;display:flex;flex-direction:column;gap:2px}.stage.forge .sidebar{background:#292930;border-color:#5a5a62}.tab{height:32px;padding:8px 12px;border:0;border-right:3px solid transparent;background:none;display:flex;align-items:center;gap:6px;font:500 11px system-ui;text-align:left;color:#666}.tab img{width:14px;height:14px}.tab.active{background:#fff;border-right-color:#0078d7;color:#0078d7}.stage.forge .tab{color:#bcbcc5}.stage.forge .tab img,.stage.forge .select img{filter:brightness(0) invert(1)}.stage.forge .tab.active{background:#35353e;border-right-color:#df8421;color:#ffb765}.content{flex:1;padding:16px;overflow:auto;position:relative}.content h2{font-size:14px;margin:0 0 10px}.fieldset{border:1px solid #d9d9de;padding:9px 10px;margin-bottom:12px}.fieldset legend{font-size:11px;font-weight:600;padding:0 4px}.row{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:11px}.select{height:25px;display:flex;align-items:center;justify-content:space-between;border:1px solid #babac2;background:#fff;min-width:140px;padding:0 6px;color:#333}.select.language{width:220px}.select img{width:12px;height:12px}.stage.forge .select{background:#2a2a31;color:#f0f0f4;border-color:#666}.palette-trigger{width:140px;height:25px;border:1px solid #bcbcc3;background:#fff;display:flex;align-items:center;gap:5px;padding:4px}.palette-trigger i{width:18px;height:15px;background:#ff0000;border:1px solid #999}.palette-trigger img{margin-left:auto}.palette{display:none;position:absolute;top:156px;right:16px;z-index:2;background:#fff;border:1px solid #aaa;padding:4px;width:200px;box-shadow:0 3px 8px #0003}.palette.open{display:block}.fieldset[hidden],.other-note[hidden]{display:none}.other-note{font-size:11px;color:#777}.stage.forge .palette{background:#303039;color:#f0f0f4;border-color:#666}.palette-grid{display:flex;gap:2px}.swatch-column{display:flex;flex-direction:column;gap:1px}.swatch-column button{width:20px;height:20px;border:1px solid #0002;border-radius:2px;padding:0}.palette button{text-align:left;font:11px system-ui}.dialog-footer{padding:8px 12px;border-top:1px solid #d4d4d4;background:#f5f5f5;display:flex;justify-content:space-between}.dialog-footer button{font:11px system-ui;padding:5px 20px;border:1px solid #aaa;background:#eee;min-width:75px}.stage.forge .dialog-footer{background:#292930;border-color:#5a5a62}.stage.forge .dialog-footer button{background:#3c3c45;color:#fff;border-color:#666}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;margin-top:16px}.icons article{background:#fff;border:1px solid #dadade;padding:12px}.card-head{display:flex;justify-content:space-between;gap:5px}.card-head b{font-size:12px}.card-head em{font-style:normal;color:#777781;font-size:10px}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #dcdce1}.sizes .light{background:#fafafa}.sizes .forge{background:#303039}.sizes .forge img{filter:brightness(0) invert(1)}.sizes span{display:flex;flex-direction:column;align-items:center}.sizes small{font-size:9px;color:#777781}.sizes .forge small{color:#ddd}.icons a{font-size:10px;color:#a85b00}@media(max-width:740px){main{padding:10px}.stage{padding:8px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · voorkeuren en keuzecomponenten</h1><p>Brongepinde tabiconen, selectors en kleurkiezer in een 600 × 520 px-schermstudie met originele 7 × 6-kleurcellen.</p></header><main><div class="note"><strong>Bereikbare route.</strong><p>Het desktopvenster opent via Bestand → Voorkeuren en `DialogHost`. De code definieert zes tabs. De twee systeemfuncties Bestandskoppeling en Virtuele printer worden in `PreferencesDialog` voor `isMobile()` weggefilterd; in de huidige `App.jsx` krijgt mobiel echter `MobileApp` in plaats van `DialogHost`. Die filter is dus geen bewijs dat dit dialoogvenster op mobiel verschijnt.</p><p>De 42 kleuren zijn CSS-vlakjes, geen SVG-iconen. Vier selectorpijlen hebben exact dezelfde padgeometrie. De scherminhoud hieronder is een compacte maatstudie, geen bronruntime-screenshot of bewijs van pixelgelijkheid met Rust.</p></div><div class="metrics"><span><b>12</b> UI-SVG-plaatsen</span><span><b>6</b> tabiconen</span><span><b>4</b> dezelfde keuzepijl</span><span><b>2</b> kleuracties</span><span><b>42</b> CSS-kleurcellen</span><span><b>600 × 520</b> dialoog</span></div><div class="controls"><label for="theme">Thema</label><select id="theme"><option value="light">Light</option><option value="forge">Forge</option></select></div><div class="stage" id="stage"><div class="dialog"><div class="dialog-header">Voorkeuren <span>×</span></div><div class="dialog-body"><div class="sidebar">''' + tab_html + '''</div><div class="content"><h2 id="content-title">Algemeen</h2><fieldset class="fieldset general-field"><legend>Taal</legend><div class="row"><span>Interfacetaal</span><button class="select language">Nederlands ''' + img('language-dropdown',12) + '''</button></div></fieldset><fieldset class="fieldset general-field"><legend>Thema</legend><div class="row"><span>Toepassingsthema</span><button class="select">Light ''' + img('select-dropdown',12) + '''</button></div></fieldset><fieldset class="fieldset annotations-field" hidden><legend>Annotatiekleur</legend><div class="row"><span>Standaardkleur</span><button class="palette-trigger" id="palette-trigger"><i></i><span>#FF0000</span>''' + img('color-dropdown',12) + '''</button></div></fieldset><p class="other-note" hidden>De inhoud van deze tab staat in de bron; deze studie toont alleen de tabstructuur en gemeenschappelijke keuzecomponenten.</p><div class="palette" id="palette"><button id="none">''' + img('color-none',14) + ''' Geen</button><div class="palette-grid">''' + swatches + '''</div><button id="more">''' + img('color-more',14) + ''' Meer kleuren…</button></div></div></div><div class="dialog-footer"><button>Standaardwaarden herstellen</button><div><button>Annuleren</button><button>Opslaan</button></div></div></div></div><div class="icons">''' + ''.join(cards) + '''</div></main><script>const stage=document.querySelector('#stage'),theme=document.querySelector('#theme'),trigger=document.querySelector('#palette-trigger'),palette=document.querySelector('#palette');theme.onchange=()=>stage.classList.toggle('forge',theme.value==='forge');for(const tab of document.querySelectorAll('.tab'))tab.onclick=()=>{for(const x of document.querySelectorAll('.tab'))x.classList.remove('active');tab.classList.add('active');document.querySelector('#content-title').textContent=tab.textContent;const isGeneral=tab.dataset.tab==='pref-general',isAnnotations=tab.dataset.tab==='pref-annotations';for(const el of document.querySelectorAll('.general-field'))el.hidden=!isGeneral;for(const el of document.querySelectorAll('.annotations-field'))el.hidden=!isAnnotations;document.querySelector('.other-note').hidden=isGeneral||isAnnotations;palette.classList.remove('open')};document.querySelector('.tab').classList.add('active');trigger.onclick=()=>palette.classList.toggle('open');for(const s of palette.querySelectorAll('[data-color]'))s.onclick=()=>{trigger.querySelector('i').style.background=s.dataset.color;trigger.querySelector('span').textContent=s.dataset.color.toUpperCase();palette.classList.remove('open')};document.querySelector('#none').onclick=()=>{trigger.querySelector('span').textContent='Geen';palette.classList.remove('open')};document.querySelector('#more').onclick=()=>palette.classList.remove('open');</script></html>'''
(root/'design/pdf-preferences-screen-review.html').write_text(page)
print('PDF preferences: 12 UI SVG sites; 4 identical selector chevrons; 42 CSS palette cells')
