#!/usr/bin/env python3
"""Audit remaining literal PDF ribbon SVG sites, including dynamic templates."""
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
prefix='open-pdf-studio/js/solid/components/ribbon/'

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
ribbon=source(prefix+'Ribbon.jsx')
specs=[
 ('FormatTab.jsx','Opmaak',[
  ('format-fill-template','Vulkleur','dynamic-color-template'),('format-stroke-template','Lijnkleur','dynamic-color-template'),
  ('format-gallery-more','Meer stijlen','disclosure'),('format-tools-chevron','Stijlgereedschappen','disclosure'),
 ],[76,81,168,374]),
 ('OrganizeTab.jsx','Organiseren',[
  ('organize-reorder','Pagina’s herschikken','command'),('organize-compress','PDF comprimeren','command'),
  ('organize-scan-text','Tekst herkennen','command'),('organize-compare','PDF’s vergelijken','command'),
 ],[17,18,20,116]),
 ('ViewTab.jsx','Beeld',[
  ('view-thin-lines','Dunne lijnen','command'),('view-reader','Leesmodus','command'),
  ('view-compare','PDF’s vergelijken','command'),('view-keystrokes','Toetsaanslagen tonen','command'),
 ],[75,89,140,159]),
 ('AdaptiveGroups.jsx','Ribbon-overloop',[
  ('overflow-more','Meer groepen','disclosure'),('overflow-chevron','Overloop openen','disclosure'),
 ],[232,240]),
 ('ArrangeTab.jsx','Schikken',[
  ('arrange-align-chevron','Uitlijnmenu openen','disclosure'),
 ],[78]),
 ('ColorPickerButton.jsx','Ribbon-kleurkiezer',[
  ('color-picker-chevron','Kleurenpalet openen','disclosure'),
 ],[80]),
 ('CommentTab.jsx','Annoteren',[
  ('comment-schedule','Hoeveelheden','command'),
 ],[31]),
 ('ExtensionRibbonTab.jsx','Extensietabs',[
  ('extension-more-tabs','Verborgen extensietabs','disclosure'),
 ],[154]),
 ('SplitButton.jsx','Gesplitste knop',[
  ('split-chevron','Actiemenu openen','disclosure'),
 ],[30]),
 ('ThemePicker.jsx','Themakeuze',[
  ('theme-chevron','Themamenu openen','disclosure'),
 ],[66]),
]
for filename in ('FormatTab.jsx','OrganizeTab.jsx','ViewTab.jsx','ArrangeTab.jsx','CommentTab.jsx'):
    component=filename.removesuffix('.jsx')
    assert f"import {component} from './{filename}'" in ribbon
assert "import ExtensionRibbonTab, { ExtensionTabStrip" in ribbon
for component,used_in in [('AdaptiveGroups','OrganizeTab.jsx'),('ColorPickerButton','FormatTab.jsx'),('SplitButton','HomeTab.jsx'),('ThemePicker','ViewTab.jsx')]:
    code=source(prefix+used_in)
    assert f"import {component} from './{component}.jsx'" in code
    assert f'<{component}' in code

out=root/'harmonization/inline-ui-icons/open-pdf-studio/ribbon-remaining'
out.mkdir(parents=True,exist_ok=True)
records=[]
for filename,area,items,expected in specs:
    code=source(prefix+filename)
    matches=list(re.finditer(r'<svg\b[\s\S]*?</svg>',code))
    lines=[code.count('\n',0,m.start())+1 for m in matches]
    assert lines==expected and len(items)==len(matches),(filename,lines)
    for match,(name,label,role),line in zip(matches,items,lines):
        raw=match.group()
        record={'name':name,'label':label,'area':area,'role':role,
                'source_file':prefix+filename,'source_line':line}
        if role=='dynamic-color-template':
            assert '${' in raw
            record['template']=raw
            record['reason_no_static_svg']='The rendered fill/stroke and indicator colors come from the active format store.'
        else:
            assert '${' not in raw
            saved=re.sub(r'\s+',' ',raw.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)).replace('> <','><').strip()+'\n'
            ET.fromstring(saved)
            (out/f'{name}.svg').write_text(saved)
            record['svg']=f'inline-ui-icons/open-pdf-studio/ribbon-remaining/{name}.svg'
            record['sha256']=hashlib.sha256(saved.encode()).hexdigest()
        records.append(record)
assert len(records)==20, len(records)
by_name={r['name']:r for r in records}
def geometry(name):
    e=ET.fromstring((root/'harmonization'/by_name[name]['svg']).read_text())
    return [(x.tag.split('}')[-1],tuple(sorted(x.attrib.items()))) for x in e.iter() if x is not e]
for group in [
    ('organize-compare','view-compare'),
    ('format-tools-chevron','arrange-align-chevron','color-picker-chevron'),
    ('split-chevron','theme-chevron'),
]:
    assert len({str(geometry(name)) for name in group})==1,group
role_counts={role:sum(r['role']==role for r in records) for role in sorted({r['role'] for r in records})}
manifest={'repository':'open-pdf-studio','commit':commit,
          'scope':'All 20 literal SVG openings in ten remaining ribbon JSX files. Two FormatTab sites are dynamic color-dependent SVG templates and deliberately have no static SVG export. The 18 other sites are UI controls, including conditional overflow and extension-tab controls. Imported ribbonIcons.js assets are audited separately.',
          'literal_svg_sites':20,'static_svg_exports':18,'dynamic_color_templates':2,
          'role_counts':role_counts,
          'identical_geometry_groups':[
              ['organize-compare','view-compare'],
              ['format-tools-chevron','arrange-align-chevron','color-picker-chevron'],
              ['split-chevron','theme-chevron'],
          ],'records':records}
(root/'harmonization/pdf-ribbon-remaining-ui-icons.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

cards=[]
for r in records:
    href=f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    if 'svg' in r:
        src='../harmonization/'+r['svg']
        imgs=''.join(f'<span><img src="{src}" width="{n}" height="{n}" alt=""><small>{n}px</small></span>' for n in (16,24,32))
        preview=f'<div class="sizes"><div class="light">{imgs}</div><div class="forge">{imgs}</div></div>'
    else:
        preview='<div class="dynamic"><div><i style="background:#e87136"></i><span>Voorbeeld vulling</span></div><div><i style="background:#287bb7"></i><span>Voorbeeld lijn</span></div></div><p class="dynamic-note">Dynamische SVG-template: kleur komt uit de actuele opmaak; geen vast SVG-bestand.</p>'
    cards.append(f'<article><div class="head"><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em></div>{preview}<a href="{href}">{escape(r["area"])} · bronregel {r["source_line"]} ↗</a></article>')
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · resterende ribbonvormen</title><style>
:root{font:13px/1.5 system-ui,sans-serif;background:#f2f2f4;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:28px max(18px,calc((100vw - 1290px)/2))}header a{font-size:12px;color:#ffcb89}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{margin:0;max-width:980px;color:#d7d7de}main{max-width:1330px;margin:auto;padding:20px}.note{background:#fff;border:1px solid #dcdce2;border-left:4px solid #df8421;padding:14px 17px}.note p{margin:5px 0}.stats{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}.stats span{background:#fff;border:1px solid #dedee3;padding:6px 10px}.stats b{color:#a95700}.duplicate{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:9px;margin:16px 0}.duplicate div{border:1px solid #e9c399;background:#fff7ee;padding:10px}.duplicate b{display:block;color:#9f5200}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}.icons article{background:#fff;border:1px solid #dadade;padding:12px}.head{display:flex;justify-content:space-between;gap:5px}.head b{font-size:12px}.head em{font-style:normal;color:#777781;font-size:10px}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #dcdce1}.sizes .light{background:#fafafa}.sizes .forge{background:#303039}.sizes .forge img{filter:brightness(0) invert(1)}.sizes span{display:flex;flex-direction:column;align-items:center}.sizes small{font-size:9px;color:#777781}.sizes .forge small{color:#ddd}.dynamic{display:flex;gap:8px;margin:12px 0}.dynamic>div{display:flex;align-items:center;gap:6px;font-size:11px}.dynamic i{display:inline-block;width:20px;height:20px;border:1px solid #aaa}.dynamic-note{font-size:10px;color:#777;margin:6px 0}.icons a{font-size:10px;color:#a85b00}@media(max-width:740px){main{padding:10px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · ribbonbronnen</h1><p>De laatste letterlijke SVG-plaatsen in tien ribbonbestanden: vaste bedieningsvormen, voorwaardelijke overloop en twee dynamische kleurtemplates.</p></header><main><div class="note"><strong>Bronrol.</strong><p>Deze 20 bronplaatsen zijn aan UI-bediening gekoppeld. Achttien leveren vaste SVG-vormen; de twee Opmaak-iconen voor vulling en lijn tekenen hun actieve kleur in een SVG-template en hebben daarom geen statisch downloadbaar icoon. De bestaande geïmporteerde `ribbonIcons.js`-vormen staan in hun aparte catalogus.</p><p>Vergelijken gebruikt dezelfde brongeometrie in Beeld en Organiseren. Drie kleine menu’s delen één pijl; SplitButton en Themakeuze delen een tweede. De extensietab- en groeps-overloopvormen verschijnen alleen onder hun bronvoorwaarden. De kleurblokjes hieronder zijn illustratieve staten, geen bronpixels.</p></div><div class="stats"><span><b>20</b> SVG-bronplaatsen</span><span><b>18</b> vaste UI-vormen</span><span><b>2</b> dynamische kleurtemplates</span><span><b>3</b> exacte hergebruiksgroepen</span></div><div class="duplicate"><div><b>Vergelijken</b>Beeld ↔ Organiseren: dezelfde geometrie.</div><div><b>Menuchevron</b>Opmaak · Schikken · Kleurkiezer: dezelfde geometrie.</div><div><b>Gesplitste knop</b>SplitButton ↔ Themakeuze: dezelfde geometrie.</div></div><div class="icons">''' + ''.join(cards) + '''</div></main></html>'''
(root/'design/pdf-ribbon-remaining-icon-review.html').write_text(page)
print('PDF ribbon: 20 literal sites; 18 static UI SVGs; 2 dynamic color templates')
