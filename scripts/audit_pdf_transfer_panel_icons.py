#!/usr/bin/env python3
"""Review UI SVGs in PDF Import, Export and Extensions panels."""
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
prefix='open-pdf-studio/js/solid/components/'
out=root/'harmonization/inline-ui-icons/open-pdf-studio/transfer-panels'
out.mkdir(parents=True,exist_ok=True)

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{prefix}{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
menu=source('app-menu/AppMenu.jsx')
host=source('DialogHost.jsx')
dialog=source('dialogs/ExtensionsDialog.jsx')
for name in ('ImportPanel','ExportPanel'):
    assert f"import {name} from './{name}.jsx'" in menu
    assert f'<{name} />' in menu
assert "import ExtensionsDialog from './dialogs/ExtensionsDialog.jsx'" in host
assert "'extensions': ExtensionsDialog" in host
assert "import ExtensionsPanel from '../app-menu/ExtensionsPanel.jsx'" in dialog
assert '<ExtensionsPanel />' in dialog

specs=[
 ('app-menu/ExportPanel.jsx',[
  ('export-images','Afbeeldingen exporteren','export','export-card','document-required'),
  ('export-raster-pdf','Raster-PDF exporteren','export','export-card','document-required'),
  ('export-flat-copy','Gevlakte kopie maken','export','export-card','document-required'),
  ('export-pdfx','PDF/X exporteren','export','export-card','tauri-only; visible-disabled-in-web'),
  ('export-cad','CAD exporteren','export','export-card','tauri-only; visible-disabled-in-web'),
  ('export-xfdf','XFDF exporteren','export','export-card','document-required'),
  ('export-bcf','BCF exporteren','export','export-card','document-required'),
 ],[207,221,235,251,269,283,298]),
 ('app-menu/ImportPanel.jsx',[
  ('import-cad','CAD importeren','import','import-card','tauri-only; visible-disabled-in-web'),
  ('import-xfdf','XFDF importeren','import','import-card','available'),
  ('import-bcf','BCF importeren','import','import-card','available'),
 ],[39,53,68]),
 ('app-menu/ExtensionsPanel.jsx',[
  ('extension-install','Extensie uit bestand installeren','extension-action','extension-panel','tauri-only-handler; disabled-only-while-installing'),
  ('extension-package','Geïnstalleerde extensie','extension-object','extension-card','only-when-extension-exists'),
  ('extension-reload','Extensie herladen','extension-action','extension-card','only-when-installed'),
  ('extension-uninstall','Extensie verwijderen','extension-action','extension-card','only-when-installed'),
 ],[113,136,165,171]),
]
records=[]
for relative,roles,expected in specs:
    code=source(relative)
    matches=list(re.finditer(r'<svg\b[\s\S]*?</svg>',code))
    lines=[code.count('\n',0,m.start())+1 for m in matches]
    assert lines==expected and len(roles)==len(matches), (relative,lines)
    for match,(name,label,role,panel,state),line in zip(matches,roles,lines):
        svg=match.group()
        assert '{' not in svg
        svg=svg.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)
        ET.fromstring(svg)
        svg=re.sub(r'\s+',' ',svg).replace('> <','><').strip()+'\n'
        filename=name+'.svg'
        (out/filename).write_text(svg)
        records.append({'name':name,'label':label,'role':role,'area':panel,
                        'availability':state,'source_file':prefix+relative,'source_line':line,
                        'svg':f'inline-ui-icons/open-pdf-studio/transfer-panels/{filename}',
                        'sha256':hashlib.sha256(svg.encode()).hexdigest()})
assert len(records)==14
by_name={r['name']:r for r in records}
def geometry(record):
    element=ET.fromstring((root/'harmonization'/record['svg']).read_text())
    return [(child.tag.split('}')[-1],tuple(sorted(child.attrib.items()))) for child in element.iter() if child is not element]
direction_collisions=[]
for kind in ('cad','xfdf','bcf'):
    outgoing=by_name['export-'+kind]
    incoming=by_name['import-'+kind]
    assert geometry(outgoing)==geometry(incoming)
    direction_collisions.append({'format':kind.upper(),'export':outgoing['name'],'import':incoming['name'],
                                 'finding':'same source geometry for opposite transfer directions'})
manifest={'repository':'open-pdf-studio','commit':commit,
          'scope':'All 14 literal SVGs in source-reachable ImportPanel.jsx, ExportPanel.jsx and ExtensionsPanel.jsx. The first two render through AppMenu; ExtensionsPanel renders through ExtensionsDialog and DialogHost. All are UI icon/object markers, including conditional and visible-disabled states. Office cards show text format badges, not SVGs.',
          'literal_svg_sites':14,'ui_symbol_sites':14,'direction_collisions':direction_collisions,
          'records':records}
(root/'harmonization/pdf-transfer-panel-ui-icons.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    src='../harmonization/'+r['svg']
    sizes=''.join(f'<span><img src="{src}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16,24,32))
    url=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    cards.append(f'<article data-search="{escape((r["name"]+" "+r["label"]+" "+r["role"]+" "+r["area"]).lower())}"><div class="top"><b>{escape(r["area"])}</b><em>{escape(r["availability"])}</em></div><h2>{escape(r["label"])}</h2><p>{escape(r["role"])} · bronregel {r["source_line"]}</p><div class="pair"><div class="light">{sizes}</div><div class="forge">{sizes}</div></div><a href="{url}">Broncode ↗</a></article>')
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Import, export en extensies</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f1f1f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:30px max(20px,calc((100vw - 1360px)/2))}header a{color:#ffc580;font-size:12px}h1{font-size:30px;letter-spacing:-.03em;margin:8px 0}header p{max-width:920px;color:#d6d6de;margin:0}main{max-width:1400px;margin:auto;padding:22px}.intro{background:#fff;border:1px solid #dedee4;border-left:4px solid #e58a21;padding:15px 18px;margin-bottom:18px}.intro p{margin:5px 0}.collisions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:16px 0}.collisions div{border:1px solid #efc99f;background:#fff8ef;padding:10px}.collisions b{display:block;color:#995000}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.stats span{background:#f8f8f9;border:1px solid #dedee4;padding:7px 12px}.stats strong{color:#b35b00}input{font:inherit;padding:10px 12px;border:1px solid #c8c8d0;width:min(420px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;padding:15px}.top{display:flex;align-items:center;justify-content:space-between}.top b{font-size:11px;color:#8b5a27}.top em{font-size:10px;font-style:normal;background:#eeeef1;color:#565663;padding:3px 7px}h2{font-size:15px;margin:10px 0 4px;line-height:1.3}article p{font-size:11px;color:#70707a;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}.light,.forge{display:flex;align-items:center;justify-content:space-around;min-height:68px;border:1px solid #dadbe0}.light{background:#fafafa}.forge{background:#303039;border-color:#565660}.forge img{filter:brightness(0) invert(1)}.pair span{display:flex;flex-direction:column;align-items:center;gap:3px}.pair small{font-size:9px;opacity:.7}.forge small{color:#fff}article>a{display:inline-block;color:#a85500;font-size:11px;margin-top:9px}@media(max-width:700px){main{padding:10px}.grid,.collisions{grid-template-columns:1fr}header{padding:22px 15px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Bestand · import, export en extensies</h1><p>Alle 14 letterlijke SVG-bedieningsvormen in de bereikbare panelen, inclusief uitgeschakelde of data-afhankelijke plaatsen.</p></header><main><div class="intro"><strong>Semantische bevinding.</strong><p>CAD, XFDF en BCF gebruiken telkens exact dezelfde documentvorm voor Importeren en Exporteren. In een gedeelde Rust-taal moeten de tegengestelde richtingen zichtbaar worden, bijvoorbeeld met in- en uitgaande pijlen. De kantoorformaten ODT, DOCX en XLSX zijn tekstbadges, geen SVG-iconen.</p><p>Importeren en Exporteren staan in Bestand; Extensies opent via een apart dialoogvenster. CAD-import/-export en PDF/X-export zijn in de webversie zichtbaar maar uitgeschakeld. Het extensie-installatieproces werkt alleen onder Tauri; de knop wordt alleen tijdens installatie uitgeschakeld, niet op basis van het webplatform.</p></div><div class="collisions"><div><b>CAD</b> Importeren ↔ Exporteren: identieke vorm</div><div><b>XFDF</b> Importeren ↔ Exporteren: identieke vorm</div><div><b>BCF</b> Importeren ↔ Exporteren: identieke vorm</div></div><div class="stats"><span><strong>7</strong> exportvormen</span><span><strong>3</strong> importvormen</span><span><strong>4</strong> extensievormen</span></div><input id="q" type="search" placeholder="Zoek vorm of rol" aria-label="Zoek vorm of rol"><div class="grid">''' + ''.join(cards) + '''</div></main><script>document.querySelector('#q').oninput=e=>{const q=e.target.value.toLowerCase().trim();for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q)}</script></html>'''
(root/'design/pdf-transfer-panel-icon-review.html').write_text(page)
print('PDF transfer panels: 14 UI SVG sites, three import/export geometry collisions')
