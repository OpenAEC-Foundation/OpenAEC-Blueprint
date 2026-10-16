#!/usr/bin/env python3
"""Classify the final PDF JSX SVG sites without treating every SVG as an icon."""
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
prefix='open-pdf-studio/js/solid/'

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
app=source(prefix+'App.jsx')
assert "import MiniLog from './components/MiniLog.jsx'" in app and '<MiniLog />' not in app
assert '<ExtensionToolPalette />' not in app and '<DockedExtPalette ' in app
assert '<SymbolTypeEditor />' in app and '<SchedulePanel />' in app
assert "import StraightenOverlay from '../solid/components/StraightenOverlay.jsx'" in source('open-pdf-studio/js/tools/straighten-select.js')
assert "'compare': CompareDialog" in source(prefix+'components/DialogHost.jsx')
assert '<ColorPalettePicker' in source(prefix+'components/properties-panel/AppearanceSection.jsx')
assert '<ParagraphSection />' in source(prefix+'components/properties-panel/PropertiesPanel.jsx')
assert '<ScheduleWizard />' in source(prefix+'components/left-panel/panels/SchedulesPanel.jsx')
for component in ('DestinationsPanel','SchedulesPanel','ThumbnailsPanel'):
    assert f'<{component} />' in source(prefix+'components/left-panel/LeftPanel.jsx')

# File, SVG sites in source order, pinned lines. A role describes the visible
# shape, not merely its XML container. The last three live SVG canvases are
# classified as generated content rather than icons; MiniLog is not mounted.
specs=[
 ('components/ExtensionToolPalette.jsx',[
  ('extension-grip','Extensiepalet-sleepgreep','drag-affordance'),('extension-close','Extensiepalet sluiten','command'),
  ('extension-undock','Palet losmaken','command'),('extension-dock-left','Links docken','drop-target'),
  ('extension-dock-right','Rechts docken','drop-target'),
 ],[394,405,478,504,512]),
 ('components/compare/CompareDialog.jsx',[
  ('compare-empty','Geen tweede document','empty-illustration'),('compare-swap','Documenten omwisselen','command'),
  ('compare-overlay','Over elkaar vergelijken','mode-preview'),('compare-side','Naast elkaar vergelijken','mode-preview'),
 ],[80,135,181,199]),
 ('components/properties-panel/ColorPalettePicker.jsx',[
  ('properties-color-chevron','Kleurmenu openen','command'),('properties-color-none','Geen kleur','command'),
  ('properties-color-more','Meer kleuren','command'),
 ],[56,68,116]),
 ('components/properties-panel/ParagraphSection.jsx',[
  ('paragraph-left','Links uitlijnen','command'),('paragraph-center','Centreren','command'),
  ('paragraph-right','Rechts uitlijnen','command'),
 ],[21,29,37]),
 ('components/symbol-edit/SymbolTypeEditor.jsx',[
  ('symbol-editor-close','Symbooleditor sluiten','command'),('symbol-editor-canvas','Symbooleditor tekenvlak','generated-editor-canvas'),
 ],[11,110]),
 ('App.jsx', [('empty-document','Leeg documentvenster','empty-illustration')],[101]),
 ('components/BeveiligdBar.jsx',[('bar-password','Beveiligd document','status-marker')],[24]),
 ('components/Dialog.jsx',[('dialog-close','Dialoog sluiten','command')],[155]),
 ('components/FormFieldsBar.jsx',[('bar-form-fields','Interactieve formuliervelden','status-marker')],[17]),
 ('components/HandtekeningBar.jsx',[('bar-signature','Handtekeningstatus','status-marker')],[46]),
 ('components/MiniLog.jsx',[('minilog-close','Historisch MiniLog sluiten','unmounted-source')],[165]),
 ('components/NotificationBar.jsx',[('bar-notification','Melding','status-marker')],[26]),
 ('components/PdfABar.jsx',[('bar-pdfa','PDF/A-melding','status-marker')],[16]),
 ('components/QuantitiesProperties.jsx',[('quantities-close','Hoeveelheden-eigenschappen sluiten','command')],[149]),
 ('components/SchedulePanel.jsx',[('schedule-close','Hoeveelhedenstaat sluiten','command')],[130]),
 ('components/ScheduleWizard.jsx',[('schedule-wizard-close','Hoeveelhedenwizard sluiten','command')],[149]),
 ('components/StraightenOverlay.jsx',[('straighten-guide','Rechtzet-richtlijn','generated-document-overlay')],[110]),
 ('components/left-panel/panels/DestinationsPanel.jsx',[('destination-item','Bestemming in lijst','list-marker')],[28]),
 ('components/left-panel/panels/SchedulesPanel.jsx',[('schedule-grip','Hoeveelhedenstaat-sleepgreep','drag-affordance')],[202]),
 ('components/left-panel/panels/ThumbnailsPanel.jsx',[('thumbnail-label','Paginalabels openen','command')],[66]),
 ('components/properties-panel/DimensionTypeSection.jsx',[('dimension-type-preview','Maatvoeringtype-voorbeeld','generated-type-preview')],[121]),
 ('components/properties-panel/PanelHeader.jsx',[('properties-collapse','Eigenschappenpaneel inklappen','command')],[12]),
]
assert len(specs)==22
out=root/'harmonization/inline-ui-icons/open-pdf-studio/last-jsx'
out.mkdir(parents=True,exist_ok=True)
records=[]
non_static={'unmounted-source','generated-editor-canvas','generated-document-overlay','generated-type-preview'}
for relative,items,expected in specs:
    code=source(prefix+relative)
    matches=list(re.finditer(r'<svg\b[\s\S]*?</svg>',code))
    lines=[code.count('\n',0,m.start())+1 for m in matches]
    assert lines==expected and len(items)==len(matches),(relative,lines)
    for match,(name,label,role),line in zip(matches,items,lines):
        raw=match.group()
        record={'name':name,'label':label,'role':role,'source_file':prefix+relative,'source_line':line,
                'mounted_in_current_ui':role!='unmounted-source'}
        if role in non_static:
            record['source_excerpt']=raw[:500]
            record['no_static_icon_reason']='unmounted component' if role=='unmounted-source' else 'runtime-generated SVG canvas/overlay; not a fixed icon'
        else:
            assert '{' not in raw,(relative,line)
            opening=raw[:raw.index('>')]
            if 'xmlns=' not in opening:
                raw=raw.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)
            saved=re.sub(r'\s+',' ',raw).replace('> <','><').strip()+'\n'
            ET.fromstring(saved)
            (out/f'{name}.svg').write_text(saved)
            record['svg']=f'inline-ui-icons/open-pdf-studio/last-jsx/{name}.svg'
            record['sha256']=hashlib.sha256(saved.encode()).hexdigest()
        records.append(record)
assert len(records)==34 and len([r for r in records if 'svg' in r])==30
role_counts={role:sum(r['role']==role for r in records) for role in sorted({r['role'] for r in records})}
manifest={'repository':'open-pdf-studio','commit':commit,
          'scope':'The final 34 literal SVG source sites in 22 PDF JSX files. Source-site audit is complete across all 317 literal sites. This is not a count of unique UI icons: three live SVGs are generated editor/overlay/type-preview surfaces, one is in an unmounted MiniLog component, and static empty-state illustrations and compare mode previews are UI visuals rather than generic commands. Imported JavaScript SVG catalogs and external assets remain separate inventories.',
          'literal_svg_sites':34,'static_reachable_svg_exports':30,
          'generated_non_icon_sites':3,'unmounted_source_sites':1,
          'role_counts':role_counts,'records':records}
(root/'harmonization/pdf-last-jsx-svg-roles.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    href=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    if 'svg' in r:
        src='../harmonization/'+r['svg']
        sizes=''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt=""><small>{n}px</small></span>' for n in (16,24,32))
        visual=f'<div class="sizes"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div>'
    else:
        visual=f'<div class="no-asset">{escape(r["no_static_icon_reason"])}</div>'
    cards.append(f'<article data-role="{escape(r["role"])}" data-name="{escape(r["name"])}"><div class="head"><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em></div>{visual}<a href="{href}">{escape(r["source_file"].rsplit("/",1)[-1])} · bronregel {r["source_line"]} ↗</a></article>')
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · laatste JSX-SVG-rollen</title><style>
:root{font:13px/1.5 system-ui,sans-serif;background:#f2f2f4;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:28px max(18px,calc((100vw - 1290px)/2))}header a{font-size:12px;color:#ffcb89}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{margin:0;max-width:970px;color:#d7d7de}main{max-width:1330px;margin:auto;padding:20px}.note{background:#fff;border:1px solid #dcdce2;border-left:4px solid #df8421;padding:14px 17px}.note p{margin:5px 0}.stats{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}.stats span{background:#fff;border:1px solid #dedee3;padding:6px 10px}.stats b{color:#a95700}.findings{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:9px;margin:16px 0}.findings div{border:1px solid #e9c399;background:#fff7ee;padding:10px}.findings b{display:block;color:#9f5200}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}.icons article{background:#fff;border:1px solid #dadade;padding:12px}.head{display:flex;justify-content:space-between;gap:5px}.head b{font-size:12px}.head em{font-style:normal;color:#777781;font-size:10px}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #dcdce1}.sizes .light{background:#fafafa}.sizes .forge{background:#303039}.sizes .forge img{filter:brightness(0) invert(1)}.icons article[data-name="compare-overlay"] .forge img,.icons article[data-name="bar-form-fields"] .forge img{filter:none}.sizes span{display:flex;flex-direction:column;align-items:center}.sizes small{font-size:9px;color:#777781}.sizes .forge small{color:#ddd}.no-asset{background:#fff7eb;border:1px solid #e9c399;padding:17px 12px;margin:9px 0;min-height:65px;font-size:11px}.icons a{font-size:10px;color:#a85b00}@media(max-width:740px){main{padding:10px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · laatste JSX-SVG-rollen</h1><p>34 laatste bronplaatsen uit 22 bestanden, met expliciete scheiding tussen vaste UI-vormen, gegenereerde tekenvlakken en niet-gemonteerde code.</p></header><main><div class="note"><strong>De JSX-bronplaatsaudit is volledig; de migratie nog niet.</strong><p>Alle 317 letterlijke SVG-openingen in 68 Solid-bestanden hebben nu een rolreview. Dat zijn geen 317 unieke iconen. In deze laatste groep zijn drie live SVG’s dynamische teken- of voorbeeldvlakken en staat één sluiticoon alleen in een niet-gemonteerde MiniLog-component. Lege-staatillustraties en vergelijkingsopties zijn UI-beelden, geen generieke werkbalkopdrachten.</p><p>De dertig hieronder geëxporteerde vormen zijn statische, bereikbare UI-beelden. De geïmporteerde JavaScript-SVG-catalogi en externe assets hebben aparte reviews. De contactkaart beoordeelt kleur en maat, maar is geen pixelvergelijking met de native Rust-app.</p></div><div class="stats"><span><b>34</b> bronplaatsen</span><span><b>30</b> vaste bereikbare SVG-beelden</span><span><b>3</b> gegenereerde niet-iconen</span><span><b>1</b> niet gemonteerd</span></div><div class="findings"><div><b>Symbooleditor</b>Het SVG-tekenvlak toont bewerkbare symboolgeometrie, geen vast pictogram.</div><div><b>Rechtzetten</b>De blauwe lijn en eindpunten zijn een tijdelijke documentoverlay.</div><div><b>Maatvoering</b>Het SVG-vlak rendert een typeafhankelijk voorbeeld.</div><div><b>MiniLog</b>De component wordt geïmporteerd maar niet meer in `App.jsx` gemonteerd.</div></div><div class="icons">''' + ''.join(cards) + '''</div></main></html>'''
(root/'design/pdf-last-jsx-svg-role-review.html').write_text(page)
print('PDF last JSX: 34 sites, 30 static reachable UI visuals, 3 generated non-icons, 1 unmounted')
