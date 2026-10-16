"""Draw original, themeable vector concepts for the OpenAEC icon family.

Three visual directions, fourteen identical functions, two optical masters.
No upstream icon geometry is copied and no production theme or crate is edited.
"""
from pathlib import Path
import hashlib
import json
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
from icon_geometry import B_WIDTHS, build_b_model

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'design/icon-style-proposals'


def p(d, **attrs):
    return '<path d="'+d+'"'+''.join(f' {k.replace("_","-") }="{v}"' for k,v in attrs.items())+'/>'


def r(x,y,w,h,rx=0,**attrs):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"'+''.join(f' {k.replace("_","-") }="{v}"' for k,v in attrs.items())+'/>'


def c(x,y,rad,**attrs):
    return f'<circle cx="{x}" cy="{y}" r="{rad}"'+''.join(f' {k.replace("_","-") }="{v}"' for k,v in attrs.items())+'/>'


def accent(body):
    return '<g stroke="var(--icon-accent,currentColor)" data-part="accent">'+body+'</g>'


def surface(d):
    return p(d,fill='var(--icon-tint,none)',data_part='surface')


FUNCTIONS = [
 ('open','file.open','Openen','Bestand of project openen'),
 ('save','file.save','Opslaan','De huidige wijzigingen bewaren'),
 ('import','file.import','Importeren','Gegevens de app in brengen'),
 ('export','file.export','Exporteren','Gegevens de app uit brengen'),
 ('undo','edit.undo','Ongedaan','De laatste bewerking terugnemen'),
 ('search','view.search','Zoeken','Inhoud opzoeken'),
 ('select','edit.select','Selecteren','Een object aanwijzen of selecteren'),
 ('move','transform.move','Verplaatsen','Een object verplaatsen; geen beeldpan'),
 ('measure','measure.distance','Afstand meten','Afstand meten; geen maatlijn plaatsen'),
 ('layers','object.layers','Lagen','Lagen tonen of beheren'),
 ('note','draw.note','Opmerking','Een opmerking plaatsen'),
 ('cpt','geo.sondering','Sondering','Een sondering plaatsen; eigen domeinbetekenis'),
 ('cloud','cloud.points','Puntenwolk','Een puntenwolk herkennen of tonen'),
 ('delete','edit.delete','Verwijderen','De selectie verwijderen; niet alles wissen'),
]
STYLES = {
 'a':{'label':'Rustig','tag':'Eenvoudige lijn','detail':'Laag','stroke24':1.7,'stroke16':1.25,'cap':'round','join':'round',
      'description':'Open contouren, afgeronde uiteinden en weinig binnenlijnen. De stilste richting voor een dicht lint.',
      'tradeoff':'Rustig op 16 px; minder uitgesproken als eigen OpenAEC-familie.'},
 'b':{'label':'Constructief','tag':'Geometrie + accent','detail':'Middel','stroke24':B_WIDTHS[24],'stroke16':B_WIDTHS[16],'cap':'butt','join':'miter','rendering':'filled-outline-from-construction-model',
      'description':'Afgeschuinde hoeken, rechte verbindingen en één gericht accent. Geïnspireerd op de constructieve geometrie van het merk.',
      'tradeoff':'Gekozen richting. De accentdelen worden uit dezelfde ankerpunten berekend als de hoofdvorm.'},
 'c':{'label':'Gelaagd','tag':'Vlak + contour','detail':'Hoog','stroke24':1.5,'stroke16':1.3,'cap':'round','join':'round',
      'description':'Vlakken, overlappende onderdelen en extra binnenlijnen. Twee kleurlagen benadrukken de constructie of handeling.',
      'tradeoff':'Rijker op 24–32 px. Op 16 px verdwijnen bewust de kleine details; één kleur blijft mogelijk.'},
}

# Every master is drawn separately: the sixteen-pixel master uses a sixteen
# unit coordinate grid and has fewer marks, not just a resized 24px drawing.
A24 = {
 'open':p('M3 8V5h6l3 3h9v3 M3 8h6l2 3h10l-3 9H3Z'),
 'save':p('M4 3h13l3 3v15H4Z M8 3v6h8V3')+r(8,14,8,7,1),
 'import':p('M4 15v5h16v-5')+accent(p('M12 3v12 M8 11l4 4 4-4')),
 'export':p('M4 15v5h16v-5')+accent(p('M12 15V3 M8 7l4-4 4 4')),
 'undo':p('M8 5 3 10l5 5 M3 10h10a7 7 0 0 1 7 7v2'),
 'search':c(10,10,6.5)+p('m15 15 5.5 5.5'),
 'select':p('M5 3v17l5-5 4 6 3-2-4-6 7-1Z'),
 'move':p('M12 3v18 M3 12h18 M9 6l3-3 3 3 M9 18l3 3 3-3 M6 9l-3 3 3 3 M18 9l3 3-3 3'),
 'measure':p('m3 16 13-13 5 5L8 21Z M8 11l2 2 M11 8l2 2 M14 5l2 2'),
 'layers':p('m3 8 9-5 9 5-9 5Z M3 12l9 5 9-5 M3 16l9 5 9-5'),
 'note':p('M4 4h16v13H9l-5 4Z M8 8h8 M8 12h5'),
 'cpt':p('M5 4h14l-7 13Z M8 21h8'),
 'cloud':''.join(c(x,y,1.25,fill='currentColor',stroke='none') for x,y in [(5,9),(10,6),(15,4),(4,14),(9,11),(14,9),(19,6),(8,17),(13,14),(18,12),(12,20),(17,18)]),
 'delete':p('M3 6h18 M9 6V3h6v3 M6 6l1 15h10l1-15 M10 10v7 M14 10v7'),
}
A16 = {
 'open':p('M2 5V3h4l2 2h6v3 M2 5h4l2 2h6l-2 6H2Z'),
 'save':p('M2.5 2h8l3 3v9h-11Z M5 2v4h5V2')+r(5,9,6,5,.5),
 'import':p('M2.5 10v4h11v-4')+accent(p('M8 2v8 M5.5 7.5 8 10l2.5-2.5')),
 'export':p('M2.5 10v4h11v-4')+accent(p('M8 10V2 M5.5 4.5 8 2l2.5 2.5')),
 'undo':p('m5 3-3 3 3 3 M2 6h7a4 4 0 0 1 4 4v3'),
 'search':c(6.5,6.5,4.25)+p('m10 10 3.5 3.5'),
 'select':p('M3 2v12l3.5-3.5L9 14l2-1.5L8.5 9l5-1Z'),
 'move':p('M8 2v12 M2 8h12 M6 4l2-2 2 2 M6 12l2 2 2-2 M4 6 2 8l2 2 M12 6l2 2-2 2'),
 'measure':p('m2 10 8-8 4 4-8 8Z M6 6l2 2 M9 3l2 2'),
 'layers':p('m2 5 6-3 6 3-6 3Z M2 9l6 3 6-3'),
 'note':p('M2 2.5h12V11H6l-4 3Z M5 6h6'),
 'cpt':p('M3 2.5h10L8 11Z M5 14h6'),
 'cloud':''.join(c(x,y,.95,fill='currentColor',stroke='none') for x,y in [(3,6),(7,3),(11,2),(3,10),(7,7),(11,6),(7,12),(11,10),(13,13)]),
 'delete':p('M2 4h12 M6 4V2h4v2 M4 4l1 10h6l1-10 M8 7v4'),
}
# Selected direction B is generated from the checked construction model.
# Coordinates and colour ownership are defined once, in icon_geometry.py.
B_MODELS={(key,size):build_b_model(key,size) for key,*_ in FUNCTIONS for size in (16,24)}
B24={key:B_MODELS[key,24].markup() for key,*_ in FUNCTIONS}
B16={key:B_MODELS[key,16].markup() for key,*_ in FUNCTIONS}
C24 = {
 'open':surface('M3 4h6l3 3h8v12H3Z')+p('M3 10h7l2 2h9l-3 9H3Z')+accent(p('M7 7h6 M7 10h7')),
 'save':surface('M3 3h14l4 4v14H3Z')+r(7,3,10,7,1)+r(7,14,10,7,1)+accent(p('M10 17h4 M14 5v3')),
 'import':surface('M3 13h5v3h8v-3h5v8H3Z')+p('M3 16h5l1 2h6l1-2h5')+accent(p('M12 3v11 M8 10l4 4 4-4')),
 'export':surface('M3 13h5v3h8v-3h5v8H3Z')+p('M3 16h5l1 2h6l1-2h5')+accent(p('M12 14V3 M8 7l4-4 4 4')),
 'undo':surface('M3 10 9 4v4h5l7 7v6h-4v-5l-4-4H9v4Z')+accent(p('M9 4 3 10l6 6')),
 'search':surface('M3 10a7 7 0 1 0 14 0 7 7 0 1 0-14 0')+p('m15 15 6 6')+accent(p('M6 10h8 M10 6v8')),
 'select':surface('M4 3v18l6-6 5 6 3-3-5-6 8-2Z')+accent(p('m7 8 5 3-3 1Z',fill='var(--icon-accent,currentColor)',stroke='none')),
 'move':surface('M9 9h6v6H9Z')+p('M12 3v6 M12 15v6 M3 12h6 M15 12h6 M9 6l3-3 3 3 M9 18l3 3 3-3 M6 9l-3 3 3 3 M18 9l3 3-3 3')+accent(p('M10 10h4v4h-4Z',fill='var(--icon-accent,currentColor)',stroke='none')),
 'measure':surface('m3 16 13-13 5 5L8 21Z')+p('M7 12l3 3 M10 9l2 2 M13 6l3 3')+accent(p('M16 3l5 5')),
 'layers':surface('m3 15 9-5 9 5v3l-9 5-9-5Z')+surface('m3 9 9-5 9 5v3l-9 5-9-5Z')+accent(surface('m3 6 9-5 9 5v3l-9 5-9-5Z'))+p('m3 6 9 5 9-5 M12 11v3 M12 17v3'),
 'note':surface('M3 3h18v15H9l-6 4Z')+p('M7 8h10 M7 12h6')+accent(c(18,17,3,fill='var(--icon-accent,currentColor)',stroke='none')),
 'cpt':surface('M6 3h12l-6 13Z')+p('M12 16v5 M7 21h10 M3 5v12 M2 7h2 M2 12h2 M2 17h2')+accent(p('M6 3h12l-6 13Z')),
 'cloud':surface('M3 8 14 2l7 4v12l-11 5-7-4Z')+''.join(c(x,y,1.1,fill='currentColor',stroke='none') for x,y in [(6,9),(10,7),(14,5),(6,14),(10,12),(14,10),(10,17),(14,15),(18,8),(18,13),(14,20)])+accent(c(18,18,1.5,fill='var(--icon-accent,currentColor)',stroke='none')),
 'delete':surface('M5 6h14v12l-3 3H8l-3-3Z')+p('M3 6h18 M9 6V3h6v3 M9 10v7 M15 10v7')+accent(p('M8 3h8')),
}
C16 = {
 'open':surface('M2 2h4l3 3h5v8H2Z')+p('M2 6h5l2 2h5l-2 6H2Z'),
 'save':surface('M2 2h9l3 3v9H2Z')+r(5,2,5,4,.5)+accent(r(5,9,6,5,.5)),
 'import':surface('M2 9h4v2h4V9h4v5H2Z')+accent(p('M8 2v7 M5.5 6.5 8 9l2.5-2.5')),
 'export':surface('M2 9h4v2h4V9h4v5H2Z')+accent(p('M8 9V2 M5.5 4.5 8 2l2.5 2.5')),
 'undo':surface('M2 6 6 2v3h4l4 4v5h-3v-4L9 8H6v3Z')+accent(p('m6 2-4 4 4 5')),
 'search':c(6.5,6.5,4.5,fill='var(--icon-tint,none)')+p('m10 10 4 4')+accent(p('M4.5 6.5h4')),
 'select':surface('M2 2v12l4-4 3 4 3-2-4-4 6-2Z'),
 'move':surface('M6 6h4v4H6Z')+p('M8 2v4 M8 10v4 M2 8h4 M10 8h4 M6 4l2-2 2 2 M6 12l2 2 2-2 M4 6 2 8l2 2 M12 6l2 2-2 2'),
 'measure':surface('m2 10 8-8 4 4-8 8Z')+p('m6 6 2 2')+accent(p('m9 3 3 3')),
 'layers':surface('m2 8 6-3 6 3v3l-6 3-6-3Z')+accent(surface('m2 4 6-3 6 3v3l-6 3-6-3Z'))+p('m2 4 6 3 6-3'),
 'note':surface('M2 2h12v9H6l-4 3Z')+p('M5 6h6')+accent(c(12,11,2,fill='var(--icon-accent,currentColor)',stroke='none')),
 'cpt':surface('M4 2h8l-4 9Z')+p('M8 11v3 M5 14h6')+accent(p('M4 2h8l-4 9Z')),
 'cloud':surface('M2 6 9 2l5 3v7l-7 3-5-3Z')+''.join(c(x,y,.85,fill='currentColor',stroke='none') for x,y in [(5,7),(8,5),(5,11),(8,9),(11,7)])+accent(c(11,12,1.1,fill='var(--icon-accent,currentColor)',stroke='none')),
 'delete':surface('M3 4h10v8l-2 2H5l-2-2Z')+p('M2 4h12 M6 4V2h4v2 M8 7v4'),
}
MASTERS={'a':{24:A24,16:A16},'b':{24:B24,16:B16},'c':{24:C24,16:C16}}


def svg(style,key,size):
    meta=STYLES[style]; width=meta['stroke'+str(size)]
    stroke='none' if style=='b' else 'currentColor'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
            f'fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="{meta["cap"]}" '
            f'stroke-linejoin="{meta["join"]}" stroke-miterlimit="3" aria-hidden="true">'
            +MASTERS[style][size][key]+'</svg>')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]; drawings={}
    geometry_checks=[model.validate() for model in B_MODELS.values()]
    model_data={'revision':2,'format':'OpenAEC 2D construction model','icons':[model.as_dict() for model in B_MODELS.values()]}
    (OUT/'model-b.json').write_text(json.dumps(model_data,indent=2)+'\n',encoding='utf-8')
    (OUT/'geometry-validation.json').write_text(json.dumps({'revision':2,'checked_models':len(geometry_checks),'checks':geometry_checks,'errors':[]},indent=2)+'\n',encoding='utf-8')
    for style in STYLES:
        drawings[style]={}
        for key,function_id,label,meaning in FUNCTIONS:
            drawings[style][key]={}
            for size in (16,24):
                markup=svg(style,key,size);ET.fromstring(markup)
                path=OUT/style/str(size)/(key+'.svg');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(markup+'\n',encoding='utf-8',newline='\n')
                drawings[style][key][str(size)]=markup
                records.append({'style':style,'function_id':function_id,'label':label,'meaning':meaning,'master_px':size,
                                'path':str(path.relative_to(OUT)).replace('\\','/'),'sha256':hashlib.sha256((markup+'\n').encode()).hexdigest()})
    reference=ROOT/'harmonization/sources/icon-style-reference/website-style.css'
    manifest={'status':'B gekozen; accentgeometrie revisie 2; nog geen volledige of geharmoniseerde set','selected_style':'b','geometry_revision':2,'construction_model':'model-b.json','date':'2026-10-16',
              'reference':{'url':'https://www.open-aec.com/','stylesheet':'https://www.open-aec.com/shared/style.css?v=20261015',
                           'stylesheet_sha256':hashlib.sha256(reference.read_bytes()).hexdigest() if reference.exists() else None},
              'authorship':'Nieuwe SVG-geometrie voor deze stijlproef; geen overgenomen bibliotheekpaden.',
              'rules':['Eén functie-ID voor dezelfde vastgestelde handeling, ongeacht app.',
                       'Kopiëren/dupliceren, import/export, afstand meten/maatlijn en verplaatsen/pannen blijven afzonderlijk.',
                       '16px heeft eigen geometrie en minder details; 32px gebruikt de 24px-master.',
                       'currentColor is de hoofdkleur; --icon-accent en --icon-tint zijn optionele CSS-tokens.',
                       'Themapaletten op de proefpagina zijn voorbeelden; Claude beheert de echte thema’s.',
                       'Geen kleur is nodig om de functie te onderscheiden; monochroom blijft beschikbaar.',
                       'B gebruikt één constructiemodel: gedeelde hoekpunten, exclusieve kleursegmenten en gevulde contouren.',
                       'Alle 28 B-masters blijven binnen hun kader en hebben geen geometrische overlap tussen hoofd- en accentkleur.'],
              'styles':STYLES,'records':records}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    data=json.dumps({'styles':STYLES,'functions':[{'key':k,'id':i,'label':l,'meaning':m} for k,i,l,m in FUNCTIONS],'drawings':drawings},ensure_ascii=False).replace('</','<\\/')
    (OUT/'index.html').write_text(PAGE.replace('/* DATA */',data),encoding='utf-8')
    with ZipFile(OUT/'openaec-icon-style-samples.zip','w',ZIP_DEFLATED) as archive:
        archive.write(OUT/'manifest.json','manifest.json')
        archive.write(OUT/'model-b.json','model-b.json')
        archive.write(OUT/'geometry-validation.json','geometry-validation.json')
        for record in records:archive.write(OUT/record['path'],record['path'])
    # Structural checks for all new drawings and the intended family coverage.
    assert len(records)==84
    assert all(set(m)=={f[0] for f in FUNCTIONS} for masters in MASTERS.values() for m in masters.values())
    assert all(MASTERS[s][16][key]!=MASTERS[s][24][key] for s in STYLES for key,*_ in FUNCTIONS)
    assert all(not re.search(r'#[0-9a-fA-F]{3,8}|\b(?:opacity|filter|image|script)\b',svg(s,k,z)) for s in STYLES for k,*_ in FUNCTIONS for z in (16,24))
    from build_icon_style_review import render_review
    render_review(OUT,FUNCTIONS,B_MODELS)
    print('84 originele SVG-proeven: 3 stijlen × 14 functies × 2 optische masters; XML en thematokens gecontroleerd.')


PAGE=r'''<!doctype html><html lang="nl" data-theme="dark"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · Stijl B — gecorrigeerde accentgeometrie</title>
<style>
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf')}@font-face{font-family:Space;src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}@font-face{font-family:Mono;src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
:root{--bg:#f1eeea;--surface:#fafaf9;--panel:#fff;--ink:#2a2a32;--muted:#655f59;--border:#d7d1ca;--icon-accent:#b45309;--icon-tint:#f7e7cc;--icon-fg:#36363e;--focus:#b45309;--danger:#b91c1c;--tile:#f5f2ee;color-scheme:light}
[data-theme=dark]{--bg:#2a2a32;--surface:#33333c;--panel:#383840;--ink:#edebe8;--muted:#bcb8b2;--border:#55555f;--icon-accent:#f59e0b;--icon-tint:#57432c;--icon-fg:#edebe8;--focus:#f59e0b;--danger:#fca5a5;--tile:#2e2e36;color-scheme:dark}
[data-theme=blueprint]{--bg:#0f1b2d;--surface:#17273d;--panel:#1c3049;--ink:#e0e7ff;--muted:#aebfda;--border:#496482;--icon-accent:#83bdff;--icon-tint:#28496e;--icon-fg:#e0e7ff;--focus:#83bdff;--danger:#fda4af;--tile:#14243a;color-scheme:dark}
[data-theme=contrast]{--bg:#000;--surface:#000;--panel:#000;--ink:#fff;--muted:#fff;--border:#fff;--icon-accent:#f59e0b;--icon-tint:#000;--icon-fg:#fff;--focus:#f59e0b;--danger:#fff;--tile:#000;color-scheme:dark}
[data-theme=contrast-light]{--bg:#fff;--surface:#fff;--panel:#fff;--ink:#000;--muted:#000;--border:#000;--icon-accent:#92400e;--icon-tint:#fff;--icon-fg:#000;--focus:#92400e;--danger:#000;--tile:#fff;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 Inter,system-ui,sans-serif}h1,h2,h3{font-family:Space,system-ui;line-height:1.12;letter-spacing:-.025em}h1{font-size:clamp(30px,3.5vw,50px);margin:14px 0}h2{font-size:28px;margin:0 0 12px}h3{font-size:23px;margin:10px 0}.mono,.eyebrow{font:11px/1.6 Mono,monospace;text-transform:uppercase;letter-spacing:.07em}.eyebrow{color:var(--icon-accent)}a{color:var(--icon-accent)}button,select,input{font:inherit}button,select{border:1px solid var(--border);border-radius:6px;padding:9px 12px;background:var(--surface);color:var(--ink)}button{cursor:pointer}button:hover{border-color:var(--icon-accent)}button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--focus);outline-offset:3px}button.chosen{border-color:var(--focus);box-shadow:inset 0 0 0 1px var(--focus)}header{max-width:1440px;margin:auto;padding:34px 28px 22px;display:flex;justify-content:space-between;gap:32px}header p{max-width:740px;color:var(--muted);margin-bottom:8px}.brandmark{width:52px;height:52px;flex:none;color:var(--icon-accent)}.hero-right{align-self:flex-end;max-width:220px;text-align:right;color:var(--muted)}main{max-width:1440px;margin:auto;padding:0 28px 48px}.controls{position:sticky;top:0;z-index:9;background:var(--bg);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:13px 0;display:flex;align-items:center;gap:14px;flex-wrap:wrap}.control{display:flex;gap:7px;align-items:center}.control>span{font:11px Mono;text-transform:uppercase;color:var(--muted)}input[type=color]{width:34px;height:32px;padding:2px;border:1px solid var(--border);background:var(--surface);border-radius:4px}.hint{color:var(--muted);font-size:12px;margin:14px 0 24px}.directions{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.direction{border:1px solid var(--border);border-radius:12px;background:var(--surface);padding:24px;min-width:0;display:flex;flex-direction:column;scroll-margin-top:150px}.direction.preferred{border-color:var(--icon-accent)}.labelrow{display:flex;justify-content:space-between;align-items:center;gap:8px}.letter{font:26px Space;color:var(--icon-accent)}.pill{font:10px Mono;border:1px solid var(--border);border-radius:30px;padding:4px 8px;text-transform:uppercase}.direction p{color:var(--muted);font-size:13px;min-height:64px;margin:0 0 12px}.signature{display:flex;justify-content:space-around;padding:22px 8px;margin:5px 0 14px;background:var(--tile);border:1px solid var(--border);border-radius:8px;color:var(--icon-fg)}.signature svg{width:54px;height:54px}.icongrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:9px 3px;padding:14px 0}.iconcell{display:flex;justify-content:center;align-items:center;min-height:38px;color:var(--icon-fg)}.glyph{width:var(--preview-size,24px);height:var(--preview-size,24px);display:block;flex:none}.mini-caption{font:10px Mono;color:var(--muted);text-align:center}.direction .trade{font-size:12px;min-height:50px;margin-top:12px}.direction button{width:100%;margin-top:auto}.section{padding-top:38px}.sectionhead{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;flex-wrap:wrap;margin-bottom:20px}.sectionhead p{color:var(--muted);max-width:740px;margin:0}.comparison{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.inspect{padding:20px;border:1px solid var(--border);border-radius:10px;background:var(--surface)}.large{height:116px;display:flex;align-items:center;justify-content:center;color:var(--icon-fg);background:var(--tile);border-radius:6px}.large svg{width:80px;height:80px}.real-sizes{display:flex;gap:28px;justify-content:center;align-items:flex-end;padding:20px 0 0;color:var(--icon-fg)}.actual{display:flex;flex-direction:column;align-items:center;gap:10px}.actual svg{display:block}.actual span{font:11px Mono;color:var(--muted)}.callout{margin-top:20px;background:var(--surface);border-left:3px solid var(--icon-accent);padding:16px 20px;display:flex;gap:22px;align-items:center}.callout b{white-space:nowrap}.callout p{margin:0;color:var(--muted);font-size:13px}.toolbar-panel{border:1px solid var(--border);border-radius:10px;background:var(--surface);overflow:hidden}.window-title{padding:10px 18px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;gap:20px;font:11px Mono}.toolbar{display:flex;align-items:stretch;gap:8px;padding:14px 18px;flex-wrap:wrap}.toolgroup{display:flex;gap:4px;border-right:1px solid var(--border);padding-right:12px;margin-right:4px}.tool{display:flex;align-items:center;justify-content:center;flex-direction:column;gap:7px;min-width:62px;border:1px solid transparent;background:transparent;padding:9px 6px;color:var(--icon-fg);border-radius:4px;font-size:11px}.tool.selected{border:1px solid var(--icon-accent);background:var(--icon-tint)}.tool.danger{color:var(--danger);--icon-accent:currentColor}.tool:disabled{opacity:.4;cursor:default}.toolbar-footer{padding:10px 18px;border-top:1px solid var(--border);font:11px Mono;color:var(--muted)}.theme-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.theme-swatch{background:var(--surface);padding:18px;border:1px solid var(--border);border-radius:8px;color:var(--ink)}.theme-icons{display:flex;justify-content:space-between;gap:7px;margin:14px 0 0;color:var(--icon-fg)}.swatchlabel{font:11px Mono}.rules{display:grid;grid-template-columns:1fr 1fr;gap:30px;border-top:1px solid var(--border);margin-top:38px;padding-top:28px}.rules p,.rules li{color:var(--muted);font-size:13px}code,pre{font-family:Mono;font-size:11px}pre{padding:18px;border:1px solid var(--border);border-radius:8px;background:var(--surface);overflow:auto}footer{color:var(--muted);border-top:1px solid var(--border);padding:20px 0 0;margin-top:25px;font-size:12px}.mono-mode{--icon-accent:var(--icon-fg)!important;--icon-tint:none!important}.mono-mode [data-part=surface]{fill:none}.mono-mode .tool.selected{background:var(--tile)}
[data-theme^=contrast] .tool:disabled{opacity:1;border:1px dashed var(--border)}
@media(max-width:1050px){.directions,.comparison{gap:12px}.direction{padding:17px}.icongrid{grid-template-columns:repeat(7,1fr)}.signature svg{width:42px;height:42px}.theme-strip{grid-template-columns:repeat(3,1fr)}}@media(max-width:760px){header{padding:24px 18px}.hero-right{display:none}main{padding:0 18px 30px}.directions,.comparison{grid-template-columns:1fr}.direction p,.direction .trade{min-height:0}.signature{padding:18px}.signature svg{width:52px;height:52px}.theme-strip{grid-template-columns:1fr 1fr}.rules{grid-template-columns:1fr}.callout{display:block}.controls{position:static}h2{font-size:24px}}
</style>
<header><div><div class="eyebrow">OpenAEC / iconen / B revisie 02</div><h1>Stijl B: constructief,<br>met gecorrigeerde accenten.</h1><p>B is gekozen. De veertien B-iconen hebben nu één gecontroleerd vectormodel. Accentlijnen sluiten aan op dezelfde ankerpunten; A en C blijven staan als eerdere referenties.</p></div><div class="hero-right"><svg class="brandmark" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m24 3 20 11v21L24 46 4 35V14Z M4 14l20 11 20-11 M24 25v21 M14 8l20 11"/></svg><div class="mono">Warm · technisch · open</div></div></header>
<main><div class="controls"><label class="control"><span>Thema</span><select id="theme" aria-label="Voorbeeldthema"><option value="dark">Donker / website</option><option value="light">Licht / website</option><option value="blueprint">Blueprint</option><option value="contrast">Hoog contrast donker</option><option value="contrast-light">Hoog contrast licht</option></select></label><label class="control"><span>Maat</span><select id="size" aria-label="Icoonmaat"><option>16</option><option selected>24</option><option>32</option></select></label><label class="control"><span>Lijn</span><input id="fg" type="color" aria-label="Hoofdkleur"></label><label class="control"><span>Accent</span><input id="accent" type="color" aria-label="Accentkleur"></label><label class="control"><span>Vlak</span><input id="tint" type="color" aria-label="Vlakkleur"></label><label class="control"><input id="mono" type="checkbox"> Eén kleur</label><button id="reset">Herstel kleuren</button></div>
<p class="hint"><a href="b-review.html"><b>Bekijk B vóór en na de correctie, met ankerpunten →</b></a></p><p class="hint">De themapaletten zijn losse voorbeelden. Claude kan de echte thema’s verder aanpassen; de icoonvormen hoeven daarvoor niet opnieuw getekend te worden.</p>
<section class="directions" id="directions" aria-label="Drie icoonstijlen"></section>
<section class="section"><div class="sectionhead"><div><div class="eyebrow">Detail onder de loep</div><h2>Dezelfde functie, drie uitwerkingen.</h2><p>De grote voorbeelden tonen de vorm. De kleine iconen hieronder staan op hun echte pixelmaat.</p></div><label>Functie <select id="function" aria-label="Vergelijkingsfunctie"></select></label></div><div id="comparison" class="comparison"></div><div class="callout"><b>16 px is apart getekend.</b><p id="opticalNote">Minder lagen, minder markeringen en meer ruimte tussen lijnen. Op 32 px gebruiken we de ruimere 24px-master.</p></div></section>
<section class="section"><div class="sectionhead"><div><div class="eyebrow">In gebruik</div><h2>Zo leest het in een lint.</h2><p id="selectedDescription">Proef met stijl B. Een selectie en een uitgeschakelde knop laten zien hoe de iconen zich in de interface gedragen.</p></div><a href="openaec-icon-style-samples.zip" download>Download alle SVG-proeven</a></div><div class="toolbar-panel"><div class="window-title"><span>OpenAEC · voorbeeldproject</span><span id="toolbarStyle">STIJL B / CONSTRUCTIEF</span></div><div id="toolbar" class="toolbar"></div><div class="toolbar-footer">ZELFDE FUNCTIE = ZELFDE ICOON-ID · APP EN THEMA VERANDEREN DE VORM NIET</div></div></section>
<section class="section"><div class="sectionhead"><div><div class="eyebrow">Eén tekening, vijf paletten</div><h2>De kleur staat los van de vorm.</h2><p>Deze rij gebruikt overal de gekozen proefstijl. Twee lichte en drie donkere vlakken maken de themakoppeling zichtbaar.</p></div></div><div class="theme-strip" id="themeStrip"></div></section>
<section class="rules"><div><div class="eyebrow">Voor de hele set</div><h2>Functies verbinden de apps.</h2><p>Openen, opslaan en zoeken krijgen ieder één vaste betekenis en vorm in alle apps. Vakfuncties zoals sondering blijven afzonderlijk herkenbaar.</p><p>Kopiëren en dupliceren, importeren en exporteren, afstand meten en een maatlijn plaatsen blijven verschillende opdrachten. De inventaris van de bronapps bepaalt welke functies werkelijk samengevoegd kunnen worden.</p><p><a href="../function-icon-catalog.html">Naar de broninventaris per functie →</a></p></div><div><div class="eyebrow">Themakoppeling</div><h2>Geen vaste kleur in de paden.</h2><pre>.toolbar-icon {
  color: var(--theme-text);
  --icon-accent: var(--theme-accent);
  --icon-tint: var(--theme-accent-soft);
}
/* SVG gebruikt currentColor + deze twee tokens.
   Bij extern IMG-gebruik kleuren apart meegeven. */</pre><p>SVG’s werken direct in webinterfaces. Dezelfde geometrie kan later naar de Rust-renderer. De proeven zijn nog niet in de gedeelde crate opgenomen.</p></div></section>
<footer>Stijl B is gekozen. De accentgeometrie is herzien; A en C blijven eerdere stijlproeven. Vorm- en kleurreferentie: <a href="https://www.open-aec.com/" target="_blank" rel="noopener">OpenAEC-website</a>. De website en de thema’s van Claude zijn niet aangepast.</footer></main>
<script type="application/json" id="data">/* DATA */</script><script>
const {styles,functions,drawings}=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);let chosen='b';const names={dark:'Donker',light:'Licht',blueprint:'Blueprint',contrast:'Contrast donker','contrast-light':'Contrast licht'};const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function icon(style,key,size){let master=size===16?16:24;return drawings[style][key][master].replace('<svg ',`<svg class="glyph" style="width:${size}px;height:${size}px" `)}
function directions(){ $('#directions').innerHTML=Object.entries(styles).map(([id,s])=>`<article class="direction ${chosen===id?'preferred':''}"><div class="labelrow"><span class="letter">${id.toUpperCase()}</span><span class="pill">${s.detail} detail</span></div><h3>${s.label}</h3><div class="eyebrow">${s.tag}</div><p style="margin-top:12px">${s.description}</p><div class="signature">${['open','layers','cpt'].map(k=>icon(id,k,48)).join('')}</div><div class="icongrid">${functions.map(f=>`<div class="iconcell" title="${f.label}" aria-label="${f.label}">${icon(id,f.key,+$('#size').value)}</div>`).join('')}</div><div class="mini-caption">14 functies · ${$('#size').value} px · master ${$('#size').value==='16'?'16':'24'} px</div><p class="trade">${s.tradeoff}</p><button data-choose="${id}" class="${chosen===id?'chosen':''}" aria-pressed="${chosen===id}">Bekijk stijl ${id.toUpperCase()} in het lint</button></article>`).join('');for(const b of document.querySelectorAll('[data-choose]'))b.onclick=()=>{chosen=b.dataset.choose;render()}}
function comparison(){const key=$('#function').value;$('#comparison').innerHTML=Object.entries(styles).map(([id,s])=>`<article class="inspect"><div class="eyebrow">${id.toUpperCase()} / ${s.label}</div><div class="large">${icon(id,key,80)}</div><div class="real-sizes">${[16,24,32].map(n=>`<div class="actual">${icon(id,key,n)}<span>${n} px</span></div>`).join('')}</div></article>`).join('')}
function toolbar(){const groups=[['open','save','import','export'],['undo','search','select','move'],['measure','layers','note','cpt','cloud','delete']];$('#toolbar').innerHTML=groups.map(group=>`<div class="toolgroup">${group.map(key=>{let f=functions.find(f=>f.key===key);return `<button class="tool ${key==='select'?'selected':''} ${key==='delete'?'danger':''}" ${key==='undo'?'disabled':''} aria-label="${f.label}" title="${f.meaning}">${icon(chosen,key,+$('#size').value)}<span>${f.label}</span></button>`}).join('')}</div>`).join('');$('#toolbarStyle').textContent='STIJL '+chosen.toUpperCase()+' / '+styles[chosen].label.toUpperCase();$('#selectedDescription').textContent='Proef met stijl '+chosen.toUpperCase()+' — '+styles[chosen].label+'. Selecteren is actief; Ongedaan is uitgeschakeld.';$('#themeStrip').innerHTML=Object.entries(names).map(([id,label])=>`<div class="theme-swatch ${$('#mono').checked?'mono-mode':''}" data-theme="${id}"><div class="swatchlabel">${label}</div><div class="theme-icons">${['save','layers','cpt','cloud'].map(k=>icon(chosen,k,24)).join('')}</div></div>`).join('')}
function render(){directions();comparison();toolbar()}
function syncColors(){for(const [id,token] of [['fg','--icon-fg'],['accent','--icon-accent'],['tint','--icon-tint']]){$('#'+id).value=getComputedStyle(document.documentElement).getPropertyValue(token).trim()}}
function reset(){for(const token of ['--icon-fg','--icon-accent','--icon-tint'])document.documentElement.style.removeProperty(token);syncColors()}
for(const f of functions)$('#function').insertAdjacentHTML('beforeend',`<option value="${f.key}">${f.label}</option>`);$('#function').value='layers';$('#function').onchange=comparison;$('#size').onchange=render;$('#theme').onchange=()=>{document.documentElement.dataset.theme=$('#theme').value;reset()};$('#reset').onclick=reset;for(const [id,token] of [['fg','--icon-fg'],['accent','--icon-accent'],['tint','--icon-tint']])$('#'+id).oninput=e=>document.documentElement.style.setProperty(token,e.target.value);$('#mono').onchange=()=>{document.body.classList.toggle('mono-mode',$('#mono').checked);toolbar()};syncColors();render();
</script></html>'''


if __name__=='__main__':main()
