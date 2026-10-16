#!/usr/bin/env python3
"""Review literal SVG roles in eight reachable PDF dialogs."""
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
prefix='open-pdf-studio/js/solid/components/dialogs/'

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
host=source('open-pdf-studio/js/solid/components/DialogHost.jsx')
specs=[
 ('AboutDialog.jsx','about','Over',[
  ('about-free','Gratis','feature-marker'),('about-open','Open broncode','feature-marker'),
  ('about-no-lock','Geen vergrendeling','feature-marker'),('about-website','Website','link-action'),
  ('about-github','GitHub','brand-mark'),('about-contact','Contact','link-action'),
 ],[44,48,52,66,73,79]),
 ('TextAnnotationDialog.jsx','text-annotation','Tekstannotatie',[
  ('text-bold','Vet','toolbar-action'),('text-italic','Cursief','toolbar-action'),
  ('text-underline','Onderstrepen','toolbar-action'),('text-align-left','Links uitlijnen','toolbar-action'),
  ('text-align-center','Centreren','toolbar-action'),('text-align-right','Rechts uitlijnen','toolbar-action'),
 ],[157,168,179,195,206,217]),
 ('MergePdfsDialog.jsx','merge-pdfs','PDF’s samenvoegen',[
  ('merge-add','Bestanden toevoegen','toolbar-action'),('merge-remove','Selectie verwijderen','toolbar-action'),
  ('merge-up','Omhoog','toolbar-action'),('merge-down','Omlaag','toolbar-action'),
  ('merge-file','Bestand in lijst','list-marker'),
 ],[141,144,147,150,165]),
 ('PrintDialog.jsx','print','Afdrukken',[
  ('print-first','Eerste voorbeeldpagina','navigation-action'),('print-prev','Vorige voorbeeldpagina','navigation-action'),
  ('print-next','Volgende voorbeeldpagina','navigation-action'),('print-last','Laatste voorbeeldpagina','navigation-action'),
 ],[1171,1177,1183,1189]),
 ('ConfirmDialog.jsx','confirm','Bevestiging',[
  ('confirm-warning','Waarschuwing','status-emblem'),
 ],[33]),
 ('FormValidationDialog.jsx','form-validation','Formuliervalidatie',[
  ('validation-error','Validatiefout','status-emblem'),
 ],[36]),
 ('PageLabelsDialog.jsx','page-labels','Paginalabels',[
  ('page-label-remove','OCR-gebied verwijderen','toolbar-action'),
 ],[178]),
 ('UpdateDialog.jsx','update','Update',[
  ('update-available','Update beschikbaar','status-emblem'),
 ],[126]),
]
out=root/'harmonization/inline-ui-icons/open-pdf-studio/dialog-ui'
out.mkdir(parents=True,exist_ok=True)
records=[]
for filename,dialog_id,area,items,expected in specs:
    component=filename.removesuffix('.jsx')
    assert f"import {component} from './dialogs/{filename}'" in host
    assert f"'{dialog_id}': {component}" in host
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
        records.append({'name':name,'label':label,'area':area,'dialog_id':dialog_id,'role':role,
                        'source_file':prefix+filename,'source_line':line,
                        'svg':f'inline-ui-icons/open-pdf-studio/dialog-ui/{name}.svg',
                        'sha256':hashlib.sha256(saved.encode()).hexdigest()})
assert len(records)==25
counts={role:sum(r['role']==role for r in records) for role in sorted({r['role'] for r in records})}
manifest={'repository':'open-pdf-studio','commit':commit,
          'scope':'All 25 literal SVGs in eight DialogHost-registered dialogs. Every shape is UI-bound, but feature badges, GitHub brand mark, file marker, and state emblems are not interchangeable command icons. The About app icon is a separate imported PNG asset and is not counted here. The print-page preview is document content, not an icon.',
          'literal_svg_sites':25,'ui_visual_sites':25,'generic_action_icon_sites':sum(counts.get(k,0) for k in ('toolbar-action','navigation-action','link-action')),'clickable_svg_sites':18,
          'role_counts':counts,
          'source_metrics':{'about_feature_svg_px':20,'text_toolbar_button_px':[28,26],
                            'text_toolbar_svg_px':16,'merge_toolbar_button_px':[26,24],
                            'print_preview_button_px':[28,22],'print_preview_svg_px':10,
                            'confirm_and_validation_emblem_px':32,'update_emblem_px':40},
          'decisions':[
              'Preserve the GitHub mark geometry as an external brand identity; do not redraw it as a generic OpenAEC icon.',
              'Map confirmation, validation and update emblems to semantic warning/error/info colors rather than globally tinting every source SVG.',
              'Keep About feature badges as informational markers, separate from reusable toolbar commands.',
          ],'records':records}
(root/'harmonization/pdf-dialog-ui-visuals.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    src='../harmonization/'+r['svg']
    sizes=''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt=""><small>{n}px</small></span>' for n in (16,24,32))
    href=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    cards.append(f'<article data-area="{escape(r["area"])}" data-role="{escape(r["role"])}"><div class="head"><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em></div><div class="sizes"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{href}">{escape(r["area"])} · bronregel {r["source_line"]} ↗</a></article>')

def img(name,n=16):
    return f'<img src="../harmonization/inline-ui-icons/open-pdf-studio/dialog-ui/{name}.svg" width="{n}" height="{n}" alt="">'
text_toolbar='<div class="toolbar"><select><option>Segoe UI</option></select><select><option>12</option></select><i></i>'+''.join(f'<button title="{escape(label)}">{img(name)}</button>' for name,label in [('text-bold','Vet'),('text-italic','Cursief'),('text-underline','Onderstrepen')])+'<i></i>'+''.join(f'<button title="{escape(label)}">{img(name)}</button>' for name,label in [('text-align-left','Links'),('text-align-center','Midden'),('text-align-right','Rechts')])+'</div>'
merge_toolbar='<div class="toolbar merge"><span>Bestanden</span>'+''.join(f'<button title="{escape(label)}">{img(name,14)}</button>' for name,label in [('merge-add','Toevoegen'),('merge-remove','Verwijderen'),('merge-up','Omhoog'),('merge-down','Omlaag')])+'</div>'
print_toolbar='<div class="toolbar print">'+''.join(f'<button title="{escape(label)}">{img(name,10)}</button>' for name,label in [('print-first','Eerste'),('print-prev','Vorige'),('print-next','Volgende'),('print-last','Laatste')])+'</div>'
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Dialoog-UI-beeldreview</title><style>
:root{font:13px/1.5 system-ui,sans-serif;background:#f2f2f4;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:28px max(18px,calc((100vw - 1300px)/2))}header a{color:#ffcb89;font-size:12px}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{max-width:950px;color:#d7d7de;margin:0}main{max-width:1340px;margin:auto;padding:20px}.note{background:#fff;border:1px solid #dcdce2;border-left:4px solid #df8421;padding:14px 17px}.note p{margin:5px 0}.stats{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}.stats span{background:#fff;border:1px solid #dedee3;padding:6px 10px}.stats b{color:#a95700}.toolbars{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:10px;margin-bottom:16px}.sample{background:#fff;border:1px solid #d8d8df;padding:12px;overflow:auto}.sample h2{font-size:13px;margin:0 0 9px}.toolbar{display:flex;align-items:center;gap:2px;white-space:nowrap}.toolbar select{font:11px system-ui;height:26px;border:1px solid #ccc;background:#fff}.toolbar select:first-child{width:160px}.toolbar select:nth-child(2){width:52px}.toolbar i{height:22px;width:1px;background:#ccc;margin:0 4px}.toolbar button{width:28px;height:26px;border:1px solid transparent;background:#f3f3f5;padding:4px;display:flex;align-items:center;justify-content:center}.toolbar button img{width:16px;height:16px}.toolbar.merge button{width:26px;height:24px}.toolbar.merge span{flex:1;font-size:11px}.toolbar.merge button img{width:14px;height:14px}.toolbar.print button{width:28px;height:22px;border-color:#ccc}.toolbar.print button img{width:10px;height:10px}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}.icons article{background:#fff;border:1px solid #dadade;padding:12px}.head{display:flex;justify-content:space-between;gap:5px}.head b{font-size:12px}.head em{font-style:normal;color:#777781;font-size:10px}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #dcdce1}.sizes .light{background:#fafafa}.sizes .forge{background:#303039}.sizes .forge img{filter:brightness(0) invert(1)}.icons article[data-role="status-emblem"] .forge img{filter:none}.sizes span{display:flex;flex-direction:column;align-items:center}.sizes small{font-size:9px;color:#777781}.sizes .forge small{color:#ddd}.icons a{font-size:10px;color:#a85b00}.key{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}.key span{background:#fff;border-left:3px solid #df8421;padding:9px 12px;border-top:1px solid #ddd;border-right:1px solid #ddd;border-bottom:1px solid #ddd;flex:1;min-width:220px}@media(max-width:740px){main{padding:10px}.toolbars{grid-template-columns:1fr}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · dialoogvormen</h1><p>Alle 25 letterlijke SVG-plaatsen in acht bereikbare dialoogcomponenten, met functie, bronniveau en maatstudies voor werkbalken.</p></header><main><div class="note"><strong>Niet elke SVG is een opdrachticoon.</strong><p>Zeventien vormen zijn generieke actie- of navigatie-iconen. De overige acht zijn drie kenmerken in Over, het klikbare GitHub-merkbeeld, één lijstbestand en drie toestandsemblemen. De PNG-appidentiteit in Over valt buiten deze SVG-telling; een afdrukvoorbeeld is documentinhoud.</p><p>De bron gebruikt 16 px SVG’s in Tekstannotatie, 14 px in Samenvoegen en 10 px in de afdruknavigatie. De onderstaande werkbalken volgen deze maten; ze zijn geïsoleerde studies, geen volledige dialoog-runtimescreenshot. De rode, amber en blauwe statusvormen zijn semantisch en mogen niet met een universele thematint worden overschreven.</p></div><div class="stats"><span><b>25</b> UI-beeldplaatsen</span><span><b>17</b> generieke actieiconen</span><span><b>3</b> kenmerkbadges</span><span><b>3</b> toestandsemblemen</span><span><b>1</b> merkbeeld</span><span><b>1</b> lijstmarkering</span></div><div class="key"><span><b>Merkbeeld</b><br>GitHub-geometrie behouden als externe identiteit.</span><span><b>Status</b><br>Waarschuwing, fout en update houden een betekenisvolle kleurrol.</span><span><b>Bediening</b><br>Tekst, samenvoegen en afdrukken delen maatregels, zonder betekenisverlies.</span></div><div class="toolbars"><div class="sample"><h2>Tekstannotatie · knoppen 28 × 26 px</h2>''' + text_toolbar + '''</div><div class="sample"><h2>Samenvoegen · knoppen 26 × 24 px</h2>''' + merge_toolbar + '''</div><div class="sample"><h2>Afdrukvoorbeeld · knoppen 28 × 22 px</h2>''' + print_toolbar + '''</div></div><div class="icons">''' + ''.join(cards) + '''</div></main></html>'''
(root/'design/pdf-dialog-ui-visual-review.html').write_text(page)
print('PDF dialogs: 25 UI SVG sites,',manifest['generic_action_icon_sites'],'generic action icons',counts)
