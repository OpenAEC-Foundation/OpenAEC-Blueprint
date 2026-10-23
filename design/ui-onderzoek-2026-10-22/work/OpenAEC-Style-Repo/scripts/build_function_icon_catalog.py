"""Merge all scoped icon evidence and audit downloaded source by function.

Generate a standalone, searchable HTML comparison, JSON and CSV. A name match
is always a candidate; reviewed command mappings and visual hashes are separate.
No source icon or canonical library is changed by this script.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote
from xml.etree import ElementTree as ET

from collect_app_icon_sources import APPS, CACHE, H, ROOT

DESIGN = ROOT / 'design'
OUT = H / 'function-icon-assets'
ROWS = []
EXCLUDED = []
WARNINGS = []
SOURCE = {}
AUDITED_SITES = set()
LIBRARIES = {}
TRANSLATIONS = {}
ASSESSMENTS = {}
SOURCE_PATHS = {}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def norm(value):
    return re.sub(r'[^a-z0-9]', '', str(value).lower())


def words(value):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', str(value)).replace('-', ' ').replace('_', ' ')


# A controlled list of functional candidates, never an artwork approval.
# Keep document/page/object, fit-width/fit-page and import/export distinct.
FUNCTIONS = {}
ALIASES = {}


def function(key, category, label, aliases):
    FUNCTIONS[key] = {'id': key, 'category': category, 'label': label}
    for alias in [key, label, *aliases.split('|')]:
        ALIASES[norm(alias)] = key


for args in [
 ('file.new','Bestanden','Nieuw document','new|fileplus|fileplus2|filenew|newproject|nieuw|nieuw project|newfile'),
 ('file.open','Bestanden','Bestand openen','open|folderopen|openfile|openen|toolbarbuttonopenfile'),
 ('file.save','Bestanden','Opslaan','save|opslaan'),
 ('file.save-as','Bestanden','Opslaan als','saveas|save_as'),
 ('file.save-all','Bestanden','Alles opslaan','saveall'),
 ('file.print','Bestanden','Afdrukken','print|printer|afdrukken|toolbarbuttonprint'),
 ('file.import','Bestanden','Importeren','import|fileinput|importeren|cuiimport'),
 ('file.export','Bestanden','Exporteren','export|fileoutput|exporteren|cuiexport'),
 ('edit.undo','Bewerken','Ongedaan maken','undo|undo2|ongedaan'),
 ('edit.redo','Bewerken','Opnieuw uitvoeren','redo|redo2|opnieuw'),
 ('edit.cut','Bewerken','Knippen','cut|scissors'),
 ('edit.copy','Bewerken','Kopiëren naar klembord','copy|kopieren'),
 ('edit.paste','Bewerken','Plakken','paste|clipboardpaste'),
 ('edit.duplicate','Bewerken','Object dupliceren','duplicate|duplicates|files|objectduplicate'),
 ('page.duplicate','Pagina’s','Pagina dupliceren','pagecopy|pageduplicate'),
 ('page.delete','Pagina’s','Pagina verwijderen','pagedelete'),
 ('page.paste','Pagina’s','Pagina plakken','pagepaste'),
 ('edit.delete','Bewerken','Selectie verwijderen','delete|trash|trash2|verwijderen'),
 ('edit.clear-all','Bewerken','Alles wissen','clearall|wisalles|deleteall'),
 ('edit.rename','Bewerken','Hernoemen','rename|hernoemen'),
 ('edit.select-all','Selecteren','Alles selecteren','selectall|alles selecteren'),
 ('edit.select','Selecteren','Selecteren','select|mousepointer|mousepointer2|cursor|selecteren'),
 ('view.search','Navigatie en zoeken','Zoeken','search|find|zoeken|toolbarbuttonsearch'),
 ('view.zoom-in','Navigatie en zoeken','Inzoomen','zoomin|zoom_in|inzoomen'),
 ('view.zoom-out','Navigatie en zoeken','Uitzoomen','zoomout|zoom_out|uitzoomen'),
 ('view.fit','Navigatie en zoeken','Alles passend in beeld','fit|zoomext|zoomextents|zoomfit|zoom fit'),
 ('view.fit-page','Navigatie en zoeken','Pagina passend','fitpage|pagefit|pagina passend'),
 ('view.fit-width','Navigatie en zoeken','Breedte passend','fitwidth|widthfit'),
 ('view.fit-selection','Navigatie en zoeken','Selectie passend','fitselection|frameselection|zoomselection'),
 ('view.pan','Navigatie en zoeken','Beeld verschuiven','pan|hand|pannen'),
 ('view.orbit','Navigatie en zoeken','3D-beeld draaien','orbit|rotate3d'),
 ('view.fullscreen','Venster en panelen','Volledig scherm','fullscreen|volledig scherm'),
 ('view.fullscreen-exit','Venster en panelen','Volledig scherm verlaten','fullscreenexit'),
 ('window.minimize','Venster en panelen','Venster minimaliseren','minimize|windowminimize'),
 ('window.maximize','Venster en panelen','Venster maximaliseren','maximize|windowmaximize'),
 ('window.restore','Venster en panelen','Venster herstellen','restore|restorewindow|windowrestore'),
 ('window.close','Venster en panelen','Venster sluiten','windowclose|venster sluiten'),
 ('ui.close','Venster en panelen','Sluiten (context controleren)','close|x|sluiten'),
 ('panel.left','Venster en panelen','Linkerpaneel tonen of verbergen','panelleft|panelleftclose|panelleftopen|sidebartoggle'),
 ('panel.right','Venster en panelen','Rechterpaneel tonen of verbergen','panelright|panelrightclose|panelrightopen'),
 ('tree.expand','Lijsten en bomen','Uitklappen','chevronright|disclosurecollapsed'),
 ('tree.collapse','Lijsten en bomen','Inklappen','chevrondown|disclosureexpanded'),
 ('nav.back','Navigatie en zoeken','Terug','back|arrowleft|chevronleft|terug'),
 ('nav.forward','Navigatie en zoeken','Vooruit','forward|arrowright|vooruit'),
 ('nav.home','Navigatie en zoeken','Startpagina','home|house|startpagina'),
 ('ui.settings','Instellingen en hulp','Instellingen','settings|settings2|preferences|voorkeuren|instellingen'),
 ('ui.help','Instellingen en hulp','Hulp','help|circlehelp|helpcircle|hulp'),
 ('ui.info','Instellingen en hulp','Informatie','info|information|circleinfo|informatie'),
 ('ui.refresh','Instellingen en hulp','Vernieuwen','refresh|refreshcw|rotatecw|update|vernieuwen'),
 ('extensions.manage','Extensies','Extensies beheren','extensions|extension|plugin|puzzle'),
 ('draw.line','Tekenen en annoteren','Lijn tekenen','line|drawingline|lijn'),
 ('draw.polyline','Tekenen en annoteren','Polylijn tekenen','polyline|polylijn'),
 ('draw.rectangle','Tekenen en annoteren','Rechthoek tekenen','rectangle|rect|square|rechthoek'),
 ('draw.circle','Tekenen en annoteren','Cirkel tekenen','circle|cirkel'),
 ('draw.arc','Tekenen en annoteren','Boog tekenen','arc|boog'),
 ('draw.polygon','Tekenen en annoteren','Gesloten veelhoek tekenen','polygon|drawingpolygon|veelhoek'),
 ('draw.text','Tekenen en annoteren','Tekst toevoegen','text|drawingtext|addtext|textadd|type'),
 ('draw.textbox','Tekenen en annoteren','Tekstvak toevoegen','textbox|textsquare'),
 ('draw.note','Tekenen en annoteren','Opmerking plaatsen','note|drawingnote|stickynote|sticky|message square'),
 ('draw.leader','Tekenen en annoteren','Leidlijn tekenen','leader|drawingleader|callout'),
 ('draw.dimension','Meten en maatvoering','Maatlijn plaatsen','dimension|drawingdimension|dimensionline'),
 ('measure.distance','Meten en maatvoering','Afstand meten','measure|ruler|distance|meten'),
 ('measure.area','Meten en maatvoering','Oppervlakte meten','measurearea|area'),
 ('transform.move','Transformeren','Object verplaatsen','move|transformmove|verplaatsen'),
 ('transform.rotate','Transformeren','Object roteren','rotate|transformrotate|roteren'),
 ('transform.mirror','Transformeren','Spiegelen','mirror|transformmirror|flip|spiegelen'),
 ('transform.trim','Transformeren','Trimmen','trim|drawingtrim'),
 ('transform.extend','Transformeren','Verlengen','extend|drawingextend'),
 ('transform.offset','Transformeren','Evenwijdige kopie','offset|drawingoffset'),
 ('format.bold','Tekstopmaak','Vet','bold'), ('format.italic','Tekstopmaak','Cursief','italic'),
 ('format.underline','Tekstopmaak','Onderstrepen','underline'),
 ('format.align-left','Tekstopmaak','Links uitlijnen','alignleft|textalignleft'),
 ('format.align-center','Tekstopmaak','Centreren','aligncenter|textaligncenter'),
 ('format.align-right','Tekstopmaak','Rechts uitlijnen','alignright|textalignright'),
 ('format.color','Tekstopmaak','Kleur kiezen','color|palette|paintbucket|colorpicker'),
 ('object.lock','Objecten en lagen','Vergrendelen','lock|locked|lockclosed'),
 ('object.unlock','Objecten en lagen','Ontgrendelen','unlock|lockopen'),
 ('object.show','Objecten en lagen','Zichtbaar maken','eye|show|visible'),
 ('object.hide','Objecten en lagen','Verbergen','eyeoff|hide|invisible'),
 ('object.layers','Objecten en lagen','Lagen','layers|layers2|lagen'),
 ('object.group','Objecten en lagen','Groeperen','group|groupobjects'),
 ('object.ungroup','Objecten en lagen','Groep opheffen','ungroup'),
 ('status.success','Status en meldingen','Geslaagd of bevestigd','check|checkcircle|circlecheck|checkcircle2'),
 ('status.warning','Status en meldingen','Waarschuwing','alerttriangle|trianglealert|warning'),
 ('status.error','Status en meldingen','Foutmelding','alertcircle|circlealert|xcircle|circlex'),
 ('status.busy','Status en meldingen','Bezig','loader|loader2|loadercircle|spinner'),
 ('audio.microphone','Spraak en audio','Microfoon','microphone|mic'),
 ('audio.microphone-off','Spraak en audio','Microfoon uit','micoff|microphoneoff'),
 ('audio.play','Spraak en audio','Afspelen','play|playerplay'),
 ('audio.pause','Spraak en audio','Pauzeren','pause|playerpause'),
 ('audio.stop','Spraak en audio','Stoppen','stop|playerstop'),
 ('audio.volume','Spraak en audio','Volume','volume|volume2'),
 ('project.folder','Project en gegevens','Projectmap','folder|folders'),
 ('data.table','Project en gegevens','Tabel','table|table2'),
 ('data.database','Project en gegevens','Database','database'),
 ('data.chart','Project en gegevens','Grafiek','chart|barchart|chartcolumn|barchart3'),
 ('report.generate','Rapporten','Rapport genereren','reportgenerate|generatereport|generatepdf'),
 ('report.preview','Rapporten','Rapportvoorbeeld','reportpreview'),
 ('report.template','Rapporten','Rapportsjabloon','reporttemplate|template|layouttemplate'),
 ('ifc.import','IFC en BIM','IFC importeren','ifcimport'),
 ('ifc.export','IFC en BIM','IFC exporteren','ifcexport'),
 ('ifc.validate','IFC en BIM','IFC valideren','ifcvalidate|validate|shieldcheck'),
 ('geo.boring','Geotechniek','Boring plaatsen','boring|geotechboring'),
 ('geo.sondering','Geotechniek','Sondering plaatsen','sondering|geotechsondering|cpt'),
 ('geo.coordinate','Geotechniek','Coördinaat plaatsen','coordinatetag|geotechcoordinatetag'),
 ('view.grid','Objecten en lagen','Raster tonen','grid|grid2x2|grid3x3'),
]:
    function(*args)


def source_url(repo, commit, path, line):
    return f'https://github.com/OpenAEC-Foundation/{repo}/blob/{commit}/{quote(path)}#L{line}' if path and commit else ''


def resolve_path(repo,commit,path):
    paths=SOURCE_PATHS.get((repo,commit),set())
    if path and path not in paths:
        choices=[p for p in paths if p.endswith('/'+path)]
        if len(choices)==1: return choices[0]
    return path


def get_source(repo, commit, path):
    key = (repo, commit, path)
    if key not in SOURCE:
        p = CACHE / repo / str(commit) / path
        SOURCE[key] = p.read_text(encoding='utf-8', errors='replace') if p.is_file() else ''
    return SOURCE[key]


def excerpt(repo, commit, path, line):
    lines = get_source(repo, commit, path).splitlines()
    return '\n'.join(lines[max(0, line - 3):line + 4])[:1600] if line else ''


def source_context(repo,commit,path,line):
    """Prefer the actual enclosing control over neighbouring toolbar buttons."""
    code=get_source(repo,commit,path)
    lines=code.splitlines(keepends=True)
    offset=sum(len(s) for s in lines[:max(0,line-1)])
    current=lines[line-1] if 0<line<=len(lines) else ''
    marker=re.search(r'<svg\b|\bicon\s*[:=]',current)
    if marker: offset+=marker.start()
    before=code[max(0,offset-1200):offset]
    starts=list(re.finditer(r'<(?:button|RibbonButton|MenuItem|IconButton|ToolButton|SplitButton)\b',before))
    if starts:
        start=max(0,offset-1200)+starts[-1].start()
        # Do not borrow a control that closed before this SVG/component.
        if not re.search(r'</(?:button|RibbonButton|MenuItem|IconButton|ToolButton|SplitButton)>',code[start:offset]):
            after=code[offset:offset+1300]
            end=re.search(r'</(?:button|RibbonButton|MenuItem|IconButton|ToolButton|SplitButton)>|\n\s*<(?:button|RibbonButton|MenuItem|IconButton)',after)
            return code[start:offset+(end.end() if end else 800)][:2000]
    # With no enclosing control, do not infer a label from adjacent buttons.
    return ''.join(lines[max(0,line-1):line+2])[:1600]


def normalize_svg(raw):
    """Convert only harmless JSX attributes; preserve uncertain geometry as a gap."""
    if re.search(r'<(?:script|foreignObject|image)\b|\bon\w+\s*=|(?:href)\s*=', raw, re.I):
        raise ValueError('actieve of externe SVG-inhoud')
    raw=re.sub(r'''[`"']\s*\+\s*[`"']''','',raw)
    raw=raw.replace('\\"','"')
    raw=re.sub(r'\b(fill|stroke|color)="\$\{[^{}]+\}"',r'\1="currentColor"',raw)
    raw=re.sub(r'\bstroke-width="\$\{[^{}]+\}"','stroke-width="1.6"',raw)
    raw=re.sub(r'\baria-hidden(?=\s|>)','aria-hidden="true"',raw)
    # JSX class/style expressions can contain nested template substitutions.
    for match in reversed(list(re.finditer(r'\b(?:className|class|ref|style)=\{',raw))):
        depth=1; i=match.end(); quotechar=None; escaped=False
        while i<len(raw) and depth:
            char=raw[i]
            if escaped: escaped=False
            elif char=='\\': escaped=True
            elif quotechar:
                if char==quotechar: quotechar=None
            elif char in "'\"`": quotechar=char
            elif char=='{': depth+=1
            elif char=='}': depth-=1
            i+=1
        if not depth: raw=raw[:match.start()]+raw[i:]
    raw = re.sub(r'\{\s*/\*.*?\*/\s*\}', '', raw, flags=re.S)
    raw = re.sub(r'\bstyle=\{\{[\s\S]*?\}\}', '', raw)
    raw = re.sub(r'\b(className|class|ref|style|aria-hidden|focusable)=\{[^{}]*\}', '', raw)
    raw = re.sub(r'\b(width|height)=\{[^{}]*\}', r'\1="24"', raw)
    raw = re.sub(r'\b(stroke|fill)=\{[^{}]*\}', r'\1="currentColor"', raw)
    raw = re.sub(r'=\{([\d.]+)\}', r'="\1"', raw)
    raw = re.sub(r"=\{(['\"])(.*?)\1\}", lambda m: '="' + html.escape(m[2], quote=True) + '"', raw)
    for key in ('strokeWidth', 'strokeLinecap', 'strokeLinejoin', 'fillRule', 'clipRule', 'strokeDasharray', 'strokeDashoffset', 'fillOpacity', 'strokeOpacity'):
        replacement = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
        raw = raw.replace(key, replacement)
    raw = re.sub(r'\s+(?:className|class|aria-label|role)="[^"]*"', '', raw)
    if '{' in raw or '}' in raw:
        raise ValueError('dynamische SVG-geometrie of expressie; handmatige extractie nodig')
    if 'xmlns=' not in raw.split('>', 1)[0]:
        raw = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    ET.fromstring(raw)
    return raw


def visual_hash(path):
    if not path or not path.exists():
        return None, None, None
    data = path.read_bytes()
    exact = hashlib.sha256(data).hexdigest()
    geometry = None
    try:
        tree = ET.fromstring(data)
        allowed = {'svg','g','path','circle','rect','line','polyline','polygon','ellipse','defs','clipPath','text','tspan','use'}
        def node(element):
            tag = element.tag.split('}')[-1]
            if tag not in allowed:
                raise ValueError('nongeometry')
            attrs = {k.split('}')[-1]: re.sub(r'\s+', ' ', v.strip()) for k,v in element.attrib.items()
                     if k.split('}')[-1] not in {'width','height','class','id','style','fill','stroke','color','opacity','fill-opacity','stroke-opacity','stroke-width','stroke-linecap','stroke-linejoin','xmlns','aria-hidden','role'}
                     or (tag != 'svg' and k in {'width','height'})}
            return [tag, sorted(attrs.items()), (element.text or '').strip(), [node(child) for child in element]]
        geometry = hashlib.sha256(json.dumps(node(tree), ensure_ascii=False).encode()).hexdigest()
    except (ET.ParseError, ValueError):
        pass
    suffix = path.suffix.lower()
    mime = 'image/svg+xml' if suffix == '.svg' else 'image/png' if suffix == '.png' else 'image/x-icon' if suffix == '.ico' else 'image/webp'
    source_data=f'data:{mime};base64,' + base64.b64encode(data).decode()
    samples={'light':source_data,'dark':source_data}
    if suffix=='.svg' and b'currentColor' in data:
        for theme,color in [('light','#182432'),('dark','#edf2f6')]:
            # currentColor inherits the host UI colour in the apps; an IMG does
            # not inherit it, so set only that inherited colour for the samples.
            tinted=re.sub(rb'<svg\b',b'<svg color="'+color.encode()+b'"',data,count=1)
            if b'<svg color=' in data: tinted=data
            samples[theme]='data:image/svg+xml;base64,'+base64.b64encode(tinted).decode()
    return exact, geometry, samples


VISUALS = {}


def add(repo, commit, name, path='', line=0, preview=None, evidence='', label='', role='', review=None, context='', state='', origin=''):
    if repo not in APPS:
        return
    if isinstance(path, dict):
        line = path.get('line', line); path = path.get('file', path.get('path', ''))
    path=resolve_path(repo,commit,path)
    line = int(line or 0)
    preview = Path(preview) if preview else None
    if preview and preview not in VISUALS:
        VISUALS[preview] = visual_hash(preview)
    exact, geometry, data = VISUALS.get(preview, (None, None, None))
    if preview and not exact:
        WARNINGS.append({'repo': repo, 'missing_preview': str(preview), 'origin': origin})
    assessment=ASSESSMENTS.get((repo,str(preview.resolve()) if preview else ''),{})
    if assessment.get('semantic_target') and not review:
        review={'semantic_target':assessment['semantic_target']}
    ROWS.append({'app': APPS[repo], 'repository': repo, 'commit': commit, 'name': name or label or 'SVG',
                 'label': label or name or 'SVG', 'path': path, 'line': line, 'role': role,
                 'evidence': evidence, 'review': review, 'assessment':assessment,'state': state, 'origin': origin,
                 'context': context or source_context(repo, commit, path, line),
                 'source_url': source_url(repo, commit, path, line),
                 'asset': str(preview.relative_to(ROOT)).replace('\\','/') if preview and preview.is_relative_to(ROOT) else None,
                 'exact_hash': exact, 'geometry_hash': geometry, 'visual': data})


def use_path(use, record):
    path = use.get('file', use.get('path', use.get('source', '')))
    if isinstance(path, dict):
        return path.get('file',''), path.get('line',0)
    return path, use.get('line', 0)


def audit_records(inventory):
    # Structured reviews are authoritative about exclusions and usage context.
    for f in sorted(H.glob('*.json')):
        if not (any(x in f.name for x in ('-ui-icons', '-svg-audit', '-jsx-svg-roles', '-dialog-ui-visuals'))):
            continue
        if f.name == 'imported-ui-icons.json':
            continue
        d = read(f)
        if not isinstance(d, dict) or d.get('repository') not in APPS:
            continue
        repo = d['repository']; commit = d.get('commit', inventory[repo].get('commit'))
        for r in d.get('icons', d.get('records', [])):
            role = r.get('role', r.get('kind', r.get('classification', '')))
            variants = r.get('variants', [r])
            if isinstance(variants,dict):
                variants = [{**value,'state':state,'svg':value.get('svg',value.get('path'))} for state,value in variants.items()]
            path = r.get('file', r.get('source_file', r.get('source', r.get('catalog_file', r.get('definition', '')))))
            line = r.get('line', r.get('source_line', r.get('definition_line', 0)))
            if isinstance(path,dict):
                line = path.get('line',line); path = path.get('file','')
            if isinstance(path,str) and path:
                AUDITED_SITES.add((repo,commit,path,int(line or 0)))
            if role in {'inactive','excluded','illustration','diagram','pattern','content-graphic','non-ui','unmounted-source', 'generated-editor-canvas','generated-document-overlay','generated-type-preview','empty-illustration','mode-preview','extension-only-export','extension-addressable-only','unused-placeholder','editable-geometry','empty-state-illustration','technical-profile','technical-preview','technical-layout'} or r.get('mounted_in_current_ui') is False:
                EXCLUDED.append({'repository':repo,'origin':f.name,'record':r})
                continue
            uses = r.get('uses',r.get('usage',[]))
            if isinstance(uses,str):
                uses = [{'file':uses,'line':n} for n in r.get('usage_lines',[])]
            if not uses:
                uses = [{'file':r.get('usage_file',path),'line':n} for n in r.get('usage_lines',[]) ] or [{'file':path,'line':line}]
            for v in variants:
                svg = v.get('svg',r.get('svg'))
                preview = H / svg if svg else None
                if not preview and r.get('template'):
                    try:
                        sample=normalize_svg(r['template'])
                        preview=OUT/(hashlib.sha256(sample.encode()).hexdigest()+'.svg')
                        preview.parent.mkdir(parents=True,exist_ok=True); preview.write_text(sample,encoding='utf-8')
                    except (ValueError,ET.ParseError): pass
                for u in uses:
                    p,l = use_path(u,r)
                    if not p: p,l = path,line
                    add(repo,commit,r.get('name',r.get('identifier',r.get('definition',''))),p,l,preview,
                        'bronreview',u.get('label',r.get('label',r.get('meaning',''))),role,r.get('review') if isinstance(r.get('review'),dict) else None,
                        u.get('source_excerpt',''),v.get('state',r.get('state',r.get('availability',''))) + ('; neutrale kleurproef uit dynamische template' if r.get('template') else ''),f.name)
                    if p: AUDITED_SITES.add((repo,commit,p,int(l or 0)))

    for r in read(H/'asset-index.json'):
        if r['repo'] not in APPS or r['category'] not in {'ui-used','possible-icon'}:
            continue
        if r['category'] == 'possible-icon':
            EXCLUDED.append({'repository':r['repo'],'origin':'asset-index.json','record':r})
            continue
        repo=r['repo']; commit=inventory[repo].get('commit')
        preview=(DESIGN/unquote(r['file'])).resolve()
        # Tracked UI copies are preferred to the ignored source archive.
        copy=H/'ui-icons'/repo/r['path']
        if copy.is_file(): preview=copy
        for u in r.get('ui_references',[]):
            add(repo,commit,Path(r['path']).stem,u.get('source',''),u.get('line',0),preview,
                r.get('evidence_type','asset'),origin='asset-index.json')


def libraries():
    for r in read(H/'library-icon-index.json')['icons']:
        for s in r['sources']:
            LIBRARIES[(s['repo'],r['name'])]=(H/r['file'], r['version'])
    for f in ('energy-ui-icons.json','planner-ribbon-ui-icons.json','heatloss-lucide-ui-icons.json'):
        d=read(H/f)
        for r in d['icons']: LIBRARIES[(d['repository'],r['name'])]=(H/r['svg'],d.get('lucide_version','bronreview'))
    assets=read(H/'composer-ui-icon-assets.json')
    for r in assets['assets']:
        LIBRARIES[(assets['source_repository'],r['symbol'])]=(ROOT/r['path'],assets['source_package'])


def assessments():
    for filename in ('geotech-icon-crosswalk.json','energy-icon-crosswalk.json','planner-ribbon-crosswalk.json'):
        data=read(DESIGN/filename); repo=data['repository']
        for row in data.get('icons',data.get('decisions',[])):
            asset=row.get('source_svg',row.get('svg'))
            if not asset: continue
            record={'meaning':row.get('meaning',''),'status':row.get('status',''),
                    'rationale':row.get('rationale',row.get('decision','')),'source':filename}
            target=row.get('proposed_target','')
            if re.fullmatch(r'Icon::\w+',target) and row.get('status')=='gedeelde kandidaat':
                record['semantic_target']=target
            elif filename=='geotech-icon-crosswalk.json' and row.get('status') in {'shared','new-shared'}:
                meaning=row.get('meaning','')
                if norm(meaning) in ALIASES: record['semantic_target']='Icon::'+meaning
            ASSESSMENTS[(repo,str((H/asset).resolve()))]=record


def translations(manifest):
    def flatten(data,prefix=''):
        if isinstance(data,dict):
            for k,v in data.items(): yield from flatten(v,prefix+'.'+k if prefix else k)
        elif isinstance(data,str): yield prefix,data
    for repo in manifest['repositories']:
        table={}
        files=sorted((f['path'] for f in repo['files'] if re.search(r'(?:^|[/._-])(?:nl|en)(?:[-_](?:NL|US|GB))?(?:/|\.json$)',f['path'])),key=lambda p:('nl' in Path(p).stem,p))
        for path in files:
            try: table.update(dict(flatten(json.loads(get_source(repo['repository'],repo['commit'],path)))))
            except (ValueError,TypeError): pass
        TRANSLATIONS[repo['repository']]=table


def collect_imports(manifest):
    imports = re.compile(r'import\s+(?:type\s+)?\{([^}]+)\}\s+from\s*[\'"]((?:lucide|solid-icons|@tabler|react-icons|@heroicons|@phosphor)[^\'"]*)[\'"]',re.S)
    for repo in manifest['repositories']:
        name=repo['repository']; commit=repo['commit']
        for file in repo['files']:
            path=file['path']
            if Path(path).suffix not in {'.tsx','.jsx','.ts','.js','.svelte','.vue'}: continue
            code=get_source(name,commit,path)
            for m in imports.finditer(code):
                for token in m[1].split(','):
                    token=token.strip()
                    if not token or token.startswith('type '): continue
                    names=re.split(r'\s+as\s+',token)
                    symbol=names[0].strip(); local=names[-1].strip()
                    if not re.fullmatch(r'\w+',symbol): continue
                    if symbol in {'LucideIcon','IconNode','IconType','IconWeight','IconProps','LucideProps'} or symbol.endswith('Props'): continue
                    use_pattern=re.compile(r'<'+re.escape(local)+r'\b|\b(?:icon|Icon|component)\s*[:=]\s*\{?\s*'+re.escape(local)+r'\b')
                    for use in use_pattern.finditer(code,m.end()):
                        line=code.count('\n',0,use.start())+1
                        preview,version=LIBRARIES.get((name,symbol),(None,None))
                        add(name,commit,symbol,path,line,preview,'bibliotheek-aanroep',
                            role='component',origin=m[2]+('@'+version if version else ''))


def source_sites(manifest):
    """Keep unreviewed SVGs explicit rather than silently dropping difficult sites."""
    OUT.mkdir(parents=True,exist_ok=True)
    for repo in manifest['repositories']:
        name=repo['repository']; commit=repo['commit']
        texts={f['path']:get_source(name,commit,f['path']) for f in repo['files'] if Path(f['path']).suffix.lower() in {'.tsx','.jsx','.ts','.js','.svelte','.vue','.rs','.slint','.py','.html','.css'} and '/public/pdfjs/' not in f['path']}
        consumers=defaultdict(list)
        for p,text in texts.items():
            # Retain line offsets while removing imports and SVG literals.
            def blank(m): return re.sub(r'[^\n]',' ',m.group())
            clean=re.sub(r'import\b[\s\S]*?\bfrom\s*[\'"][^\'"]+[\'"]\s*;?',blank,text)
            clean=re.sub(r'<svg\b[\s\S]*?</svg>',blank,clean)
            for use in re.finditer(r'\b(?:\w*Icon\w*|Icon\w+)\b',clean):
                prefix=clean[max(0,use.start()-30):use.start()]
                if re.search(r'\b(?:const|let|function|fn|type|interface|class)\s*$',prefix): continue
                if re.search(r'//[^\n]*$',prefix): continue
                consumers[use.group()].append((p,clean.count('\n',0,use.start())+1))
        for file in repo['files']:
            path=file['path']; code=get_source(name,commit,path)
            if '/public/pdfjs/' in path: continue
            if Path(path).suffix.lower() not in {'.tsx','.jsx','.ts','.js','.svelte','.vue','.rs','.slint','.py','.html','.css'}: continue
            for m in re.finditer(r'<svg(?=[\s>])[\s\S]*?</svg>',code):
                line=code.count('\n',0,m.start())+1
                if (name,commit,path,line) in AUDITED_SITES: continue
                prefix=code[max(0,m.start()-220):m.start()]
                identifiers=list(re.finditer(r'(?:const|let|function|fn)\s+(\w+)',prefix))
                keymatch=re.search(r"(?:[\"']?)(\w+)(?:[\"']?)\s*:\s*['\"`]?\s*\(?\s*$",prefix)
                symbol=keymatch[1] if keymatch else identifiers[-1][1] if identifiers else f'{Path(path).stem}:svg-{line}'
                raw=m.group(); preview=None; state='bronplaats; rol en bereikbaarheid controleren'
                if len(re.findall(r'<svg(?=[\s>])',raw))>1:
                    EXCLUDED.append({'repository':name,'origin':'volledige clientbronscan','record':{'file':path,'line':line,'role':'SVG-tekst in commentaar of bronteksttest; geen afzonderlijke vorm'}})
                    continue
                if path.endswith('/ui/cursors/annotation-cursors.js'):
                    constants=dict(re.findall(r'const\s+(\w+)\s*=\s*`([^`]+)`',code,re.S))
                    for match in re.finditer(r'\b(\w+)\s*:\s*(\w+_BADGE)\b',code):
                        badge=constants.get(match[2]); arrow=constants.get('ARROW')
                        if not badge or not arrow:continue
                        svg=normalize_svg(raw.replace('${ARROW}',arrow).replace('${badgeSvg}',badge))
                        dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                        if not dest.exists():dest.write_text(svg,encoding='utf-8')
                        add(name,commit,'cursor-'+match[1],path,code.count('\n',0,match.start())+1,dest,'SVG-bronplaats',
                            label='Annotatiecursor: '+match[1],role='cursor',state='Vaste cursorbadge uit BADGE_MAP',origin='volledige clientbronscan')
                    continue
                category_path=re.search(r'\bd=\{(\w+)\[[^]]+\][^}]*\}',raw)
                if category_path:
                    definition=re.search(r'const\s+'+re.escape(category_path[1])+r'[^=]*=\s*\{([\s\S]*?)\};',code)
                    expanded=0
                    if definition:
                        for choice in re.finditer(r'''(?:["']?)([\w-]+)(?:["']?)\s*:\s*(["'])(M.*?)\2''',definition[1]):
                            svg=normalize_svg(raw.replace(category_path.group(),'d="'+choice[3]+'"'))
                            dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                            if not dest.exists():dest.write_text(svg,encoding='utf-8')
                            add(name,commit,'category-'+choice[1],path,line,dest,'SVG-bronplaats',label='Categorie: '+choice[1],state='Vaste categorie uit '+category_path[1],origin='volledige clientbronscan')
                            expanded+=1
                    if expanded:continue
                constant_path=re.search(r'\bd=\{([A-Z_]+)\}',raw)
                if constant_path:
                    pattern=re.compile(r'const\s+'+re.escape(constant_path[1])+r'''\s*=\s*(["'])([^"']+)\1''')
                    definition=next((match for text in texts.values() if (match:=pattern.search(text))),None)
                    if definition:raw=raw.replace(constant_path.group(),'d="'+definition[2]+'"')
                optional=re.search(r'''\$\{\s*([^?{}]+)\?\s*`([^`]*)`\s*:\s*["']{2}\s*\}''',raw,re.S)
                if optional:
                    expanded=0
                    for body,label in [(optional[2],'met kleefmeting'),('','zonder kleefmeting')]:
                        try:
                            svg=normalize_svg(raw.replace(optional.group(),body))
                            dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                            if not dest.exists():dest.write_text(svg,encoding='utf-8')
                            add(name,commit,'sondering-marker-'+label,path,line,dest,'SVG-bronplaats',label='Sonderingmarkering '+label,
                                role='kaartmarkering',state='Vaste geometrie; selectieafhankelijke verf als neutrale kleurproef',origin='volledige clientbronscan')
                            expanded+=1
                        except (ValueError,ET.ParseError): pass
                    if expanded==2:continue
                # Expand simple, static SVG factory calls without executing JS.
                helper=re.search(r'\$\{(\w+)\}',raw)
                factory=re.search(r'const\s+(\w+)\s*=\s*\([^)]*\)[^=]*=>\s*[`\'"]\s*$',prefix)
                if helper and factory:
                    call_pattern=re.compile(r'\b'+re.escape(factory[1])+r'''\(\s*([`'"])([\s\S]*?)\1\s*,?\s*\)''')
                    expanded=0
                    for call in call_pattern.finditer(code):
                        declaration=re.search(r'(?:const|let)\s+(\w+)\s*=\s*$',code[max(0,call.start()-100):call.start()])
                        if not declaration: continue
                        icon_name=declaration[1]
                        try:
                            svg=normalize_svg(raw.replace('${'+helper[1]+'}',call[2]))
                            dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                            if not dest.exists():dest.write_text(svg,encoding='utf-8')
                            refs=consumers.get(icon_name,[]) or [(path,code.count('\n',0,call.start())+1)]
                            for p,l in refs:
                                add(name,commit,icon_name,p,l,dest,'SVG-bronplaats',state='Statische SVG-fabriek; functie controleren',origin='clientbronscan: '+path)
                            expanded+=1
                        except (ValueError,ET.ParseError): pass
                    if expanded:
                        EXCLUDED.append({'repository':name,'origin':'volledige clientbronscan','record':{'file':path,'line':line,'role':'SVG-fabriekswrapper; afzonderlijke vaste aanroepen verzameld','expanded':expanded}})
                        continue
                catalog_definition=bool(re.search(r'(?:icons|RibbonIcons)\.(?:ts|js|tsx)$',path,re.I)) and 'Icon' in symbol
                if catalog_definition and not consumers.get(symbol):
                    EXCLUDED.append({'repository':name,'origin':'volledige clientbronscan','record':{'file':path,'line':line,'name':symbol,'role':'catalogusdefinitie zonder gevonden bronconsument; dynamisch gebruik niet bewezen'}})
                    continue
                # Generated engineering diagrams are not fixed UI pictograms.
                opening=raw.split('>',1)[0]
                box=re.search(r'viewBox=["\']\s*0[ ,]+0[ ,]+([\d.]+)[ ,]+([\d.]+)',opening)
                if (re.search(r'viewBox=[`"{][^>]*(?:\$\{|\b(?:V_W|ZK_W|SIZE|VB_W|svgWidth|viewWidth)\b)',opening,re.I)
                    or re.search(r'class(?:Name)?=["\'][^"\']*(?:chart|plot|diagram|cross-section|visual-svg|vd-svg)',opening)
                    or (box and max(float(box[1]),float(box[2]))>64 and re.search(r'calc|wizard|diagram|template|chart|drawing|plot|preview|canvas|visual',path,re.I))):
                    EXCLUDED.append({'repository':name,'origin':'volledige clientbronscan','record':{'file':path,'line':line,'role':'gegenereerd diagram of tekenvlak','excerpt':raw[:250]}})
                    continue
                if (('/templates/' in path and re.search(r'#(?:show|for|if)\b',raw))
                    or any(p in path for p in ('/js/solid/data/elektraSymbols','/js/solid/data/nen1414Library','/js/symbols/steel-catalog','/js/solid/components/SymbolPalette')) and ('<image' in raw or path.endswith(('elektraSymbols.js','steel-catalog.js')))):
                    EXCLUDED.append({'repository':name,'origin':'volledige clientbronscan','record':{'file':path,'line':line,'role':'document- of plaatsbare symboolinhoud; geen UI-bediening'}})
                    continue
                non_icons={
                    ('Open-Calculations-Studio','packages/desktop/src/components/calc/ModuleAfbeelding.tsx',92):'Module-illustratie met dynamische inhoud',
                    ('Open-Calculations-Studio','packages/desktop/src/components/calc/VoetplaatDesigner.tsx',318):'Technische doorsnedetekening',
                    ('Open-Calculations-Studio','packages/desktop/src/components/calc/designerKit.tsx',470):'Technische modulevoorbeelden met dynamische inhoud',
                    ('Open-Calculations-Studio','packages/web/src/main.ts',238):'Technische voorbeeldtekening in documentinhoud',
                    ('Open-Calculations-Studio','packages/web/src/main.ts',388):'Technische voorbeeldtekening in documentinhoud',
                    ('open-pdf-studio','open-pdf-studio/js/solid/data/symbolLibraryOnline.js',123):'SVG-validatiecode; geen vaste UI-vorm',
                }
                reason=non_icons.get((name,path,line))
                if reason:
                    EXCLUDED.append({'repository':name,'origin':'bronrolcontrole 2026-10-16','record':{'file':path,'line':line,'role':reason}})
                    continue
                # Source-only expansion of conditional shapes. No application
                # code is evaluated; both literal branches remain separate.
                attr_choice=re.search(r'''\bd=\{([^{}?]+)\?\s*(["'])(.*?)\2\s*:\s*(["'])(.*?)\4\s*\}''',raw,re.S)
                body_choice=re.search(r'\{\s*([^{}?]+)\?\s*\(?\s*(<[^{}]*?)\s*\)?\s*:\s*\(?\s*(<[^{}]*?)\s*\)?\s*\}',raw,re.S)
                variants=[]
                if attr_choice:
                    variants=[(raw.replace(attr_choice.group(),'d="'+attr_choice[n]+'"'),attr_choice[1].strip()+'='+value) for n,value in [(3,'true'),(5,'false')]]
                elif body_choice:
                    variants=[(raw.replace(body_choice.group(),body_choice[n].replace('<>','').replace('</>','')),body_choice[1].strip()+'='+value) for n,value in [(2,'true'),(3,'false')]]
                if variants:
                    expanded=0
                    for variant,condition in variants:
                        try:
                            svg=normalize_svg(variant)
                            dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                            if not dest.exists():dest.write_text(svg,encoding='utf-8')
                            add(name,commit,symbol+':'+condition,path,line,dest,'SVG-bronplaats',state='Vaste toestand '+condition,origin='volledige clientbronscan')
                            expanded+=1
                        except (ValueError,ET.ParseError): pass
                    if expanded==len(variants): continue
                try:
                    clean=normalize_svg(raw)
                    digest=hashlib.sha256(clean.encode()).hexdigest()
                    preview=OUT/(digest+'.svg')
                    if not preview.exists(): preview.write_text(clean,encoding='utf-8')
                    if clean != raw: state+='; JSX-weergave genormaliseerd'
                except (ValueError,ET.ParseError) as error:
                    state+='; '+str(error)
                    # Recover fixed choices in dynamic path catalogues (for
                    # example permission options), preserving every alternative.
                    dynamic=re.search(r'\bd=\{([\w.]+)\}',raw)
                    if dynamic:
                        prop=dynamic[1].split('.')[-1]
                        choices=list(re.finditer(r'\b'+re.escape(prop)+r'''\s*:\s*(["'])(M[^"']+)\1''',code))
                        variants=[]
                        for choice in choices:
                            try:
                                svg=normalize_svg(raw.replace(dynamic.group(),'d="'+choice[2]+'"'))
                                dest=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                                if not dest.exists():dest.write_text(svg,encoding='utf-8')
                                context=code[max(0,code.rfind('{',0,choice.start())):choice.end()+120]
                                labelmatch=re.search(r'''(?:label|name|id)\s*:\s*["']([^"']+)["']''',context)
                                choice_line=code.count('\n',0,choice.start())+1
                                label=labelmatch[1] if labelmatch else prop+' '+str(choice_line)
                                variants.append((dest,label,choice_line))
                            except (ValueError,ET.ParseError): pass
                        if variants:
                            for dest,label,choice_line in variants:
                                add(name,commit,symbol+':'+label,path,line,dest,'SVG-bronplaats',label=label,
                                    state='Dynamische padkeuze uit '+str(choice_line)+'; functie controleren',origin='volledige clientbronscan')
                            continue
                if catalog_definition and consumers.get(symbol):
                    for p,l in consumers[symbol]:
                        add(name,commit,symbol,p,l,preview,'SVG-bronplaats',state=state+'; symboolreferentie buiten import/definitie',origin='clientbronscan: '+path+':'+str(line))
                else:
                    add(name,commit,symbol,path,line,preview,'SVG-bronplaats',state=state,origin='volledige clientbronscan')
            # Glyph icons are kept as evidence, separate from SVG artwork.
            for m in re.finditer(r'\bicon\s*[:=]\s*\{?\s*[\'"]([^\'"\n]{1,8})[\'"]',code):
                glyph=m[1]
                if not any(ord(c)>255 for c in glyph): continue
                line=code.count('\n',0,m.start())+1
                add(name,commit,'Glyph '+glyph,path,line,evidence='teksticoon-kandidaat',label=glyph,
                    state='Lettertype-/OS-afhankelijke vorm; functie controleren',origin='volledige clientbronscan')


def asset_sites(manifest):
    """Collect file references and typed native icon calls omitted by JSX scans."""
    for repo in manifest['repositories']:
        name=repo['repository']; commit=repo['commit']
        assets=[f['path'] for f in repo['files'] if Path(f['path']).suffix.lower() in {'.svg','.png','.ico','.webp'}]
        codefiles=[f['path'] for f in repo['files'] if Path(f['path']).suffix.lower() in {'.tsx','.jsx','.ts','.js','.svelte','.vue','.rs','.slint','.py','.html','.css'}]
        basenames=defaultdict(list)
        for path in assets: basenames[Path(path).name].append(path)
        native={}
        for path in assets:
            if '/ui/assets/' in path or '/ui/src/' in path or '/assets/opencad-icons/' in path:
                native.setdefault(norm(Path(path).stem),path)
        for path in codefiles:
            code=get_source(name,commit,path)
            for basename,paths in basenames.items():
                if basename not in code: continue
                # Require unique basename or a literal path suffix to resolve it.
                for m in re.finditer(r'''['"`]([^'"`\n]*?'''+re.escape(basename)+r''')\s*['"`]''',code):
                    if not re.search(r'icon|image|asset|include|\.slint',path+' '+code[max(0,m.start()-100):m.start()],re.I): continue
                    choices=[p for p in paths if p.endswith(m[1].lstrip('./'))] or paths
                    if len(choices)!=1: continue
                    asset=choices[0]; data=(CACHE/name/commit/asset).read_bytes()
                    dest=OUT/(hashlib.sha256(data).hexdigest()+Path(asset).suffix.lower())
                    if not dest.exists(): dest.write_bytes(data)
                    line=code.count('\n',0,m.start())+1
                    add(name,commit,Path(asset).stem,path,line,dest,'bestandsverwijzing',origin='clientbronscan: '+asset)
            if Path(path).suffix=='.rs':
                for m in re.finditer(r'\b(Icon|DomainIcon|RibbonIcon)::(\w+)',code):
                    # Ignore enum implementation matches and tests; preserve typed call evidence.
                    if re.search(r'/ui/(?:src|tests)/',path): continue
                    asset=native.get(norm(m[2])); preview=None
                    if asset:
                        data=(CACHE/name/commit/asset).read_bytes()
                        preview=OUT/(hashlib.sha256(data).hexdigest()+Path(asset).suffix.lower())
                        if not preview.exists(): preview.write_bytes(data)
                    add(name,commit,m[2],path,code.count('\n',0,m.start())+1,preview,'getypeerde Rust-aanroep',
                        state='Bronvariant '+m[1],origin='clientbronscan')


def manifest_icons(manifest):
    for repo in manifest['repositories']:
        name=repo['repository']; commit=repo['commit']
        for file in repo['files']:
            path=file['path']
            if Path(path).name not in {'manifest.json','catalog.json','extension.json','openaec-extension.json'}:continue
            code=get_source(name,commit,path)
            try:data=json.loads(code)
            except ValueError:continue
            def walk(value):
                if isinstance(value,list):
                    for v in value:yield from walk(v)
                if isinstance(value,dict):
                    icon=value.get('icon',value.get('iconSvg'))
                    if isinstance(icon,str) and icon:
                        label=value.get('name',value.get('title',value.get('id',icon)))
                        if isinstance(label,dict):label=label.get('nl',label.get('en',icon))
                        yield icon,str(label)
                    for v in value.values():
                        if isinstance(v,(dict,list)):yield from walk(v)
            for icon,label in walk(data):
                offset=code.find(json.dumps(icon,ensure_ascii=False))
                if offset<0:offset=code.find('"icon"')
                line=code.count('\n',0,max(0,offset))+1;preview=None
                if '<svg ' in icon:
                    try:
                        svg=normalize_svg(icon)
                        preview=OUT/(hashlib.sha256(svg.encode()).hexdigest()+'.svg')
                        if not preview.exists():preview.write_text(svg,encoding='utf-8')
                    except (ValueError,ET.ParseError): pass
                add(name,commit,icon if len(icon)<80 else label,path,line,preview,
                    'manifest-icoon',label=label,state='Extensiemetadata; runtime-plaatsing controleren',origin='extensiecatalogus')


def categorize(row):
    """Use reviewed meanings first; automatic aliases remain visibly provisional."""
    review=row.get('review')
    if isinstance(review,dict):
        target=review.get('semantic_target','')
        if target.startswith('Icon::'):
            key=ALIASES.get(norm(target.split('::')[-1]))
            if key: return key,'bronreview van functie'
    label=row['label']; name=row['name']
    # An explicit label outranks a library glyph name (Download may mean Import).
    context=row['context']
    if re.search(r'(?:TitleBar|WindowControls)',row['path'],re.I):
        if re.search(r'\b(?:close|exit|sluiten)\b',name+' '+label,re.I): return 'window.close','functie uit venstercontext; controleren'
    labels=re.findall(r'(?:title|label|aria-label|tooltip)\s*=\s*[\'"]([^\'"]+)',context)
    labels+=re.findall(r'(?:title|label|aria-label|tooltip)\s*=\s*\{\s*[\'"]([^\'"]+)',context)
    translations=re.findall(r"(?:label|title|tooltip)\s*=\s*\{[^}]*?t\(['\"]([^'\"]+)",context)
    if not translations and re.match(r'<(?:button|RibbonButton|MenuItem|IconButton|ToolButton|SplitButton)\b',context):
        translations=re.findall(r"\bt\(['\"]([^'\"]+)",context)
        tail=re.search(r'</svg>\s*(?:<span[^>]*>\s*)?([^<>{\n][^<>{}]{1,70})',context)
        if tail and re.match(r'[A-Za-zÀ-ž0-9+]',tail[1].strip()) and not re.search(r'//|=>|\breturn\b|`',tail[1]): labels.append(tail[1].strip())
    translated=[TRANSLATIONS.get(row['repository'],{}).get(x,x.split('.')[-1]) for x in translations]
    candidates=([label] if label != name else [])+labels+translated
    if label==name and (labels or translated):
        row['label']=(labels+translated)[0]
        label=row['label']
    for candidate in candidates:
        key=ALIASES.get(norm(candidate))
        if key:
            if key.startswith('format.align-') and (re.search(r'ArrangeTab',row['path']) or 'arrange.align' in context):
                target=key.replace('format.','object.')
                FUNCTIONS.setdefault(target,{'id':target,'category':'Objecten en lagen','label':{'object.align-left':'Objecten links uitlijnen','object.align-center':'Objecten centreren','object.align-right':'Objecten rechts uitlijnen'}[target]})
                return target,'functie uit schikcontext; controleren'
            return key,'functie uit label; controleren'
    value=re.sub(r'^(?:TbOutline|Tb|Lu|Fa|Icon)', '', name)
    value=re.sub(r'(?:Icon|_icon)$','',value)
    key=ALIASES.get(norm(value))
    if not key:
        stripped=re.sub(r'^(?:start|home|map|drawing|titlebar|chrome|toolbar|menu|backstage|nav|ribbon)[-_]', '',value,flags=re.I)
        key=ALIASES.get(norm(stripped))
    if key:
        if key.startswith('format.align-') and (re.search(r'ArrangeTab',row['path']) or 'arrange.align' in context):
            target=key.replace('format.','object.')
            FUNCTIONS.setdefault(target,{'id':target,'category':'Objecten en lagen','label':{'object.align-left':'Objecten links uitlijnen','object.align-center':'Objecten centreren','object.align-right':'Objecten rechts uitlijnen'}[target]})
            return target,'functie uit schikcontext; controleren'
        return key,'naamkandidaat; functie controleren'
    # Keep ambiguous downloads, pluses, crosses and arrows outside specific actions.
    ambiguous={'download':'Download-vorm: import of export controleren','upload':'Upload-vorm: functie controleren',
               'plus':'Plus-vorm: toevoegen of menu controleren','minus':'Min-vorm: functie controleren',
               'layoutgrid':'Tegelraster: navigatie of indeling controleren','cube':'Kubus: object of paneel controleren'}
    n=norm(label) if label!=name and len(label)<100 else norm(value)
    if n in {'icon','icons','svg','render','component','default','geticon','iconmap'}:
        n=norm(row['app']+' '+row['path']+' '+str(row['line']))
    key='review.'+ (n or 'unknown')
    if key not in FUNCTIONS:
        haystack=(value+' '+label+' '+row['path']).lower()
        category='Overige functies — broncontrole nodig'
        for pattern,cat in [(r'ribbon|toolbar','Appspecifieke opdrachten'),(r'report','Rapporten'),(r'pdf|page','Pagina’s'),(r'heat|energy|thermal','Energie en warmte'),(r'geo|cpt|boring','Geotechniek'),(r'pile','Paalplan'),(r'speech|audio|transcri','Spraak en audio'),(r'plan|gantt|task','Planning'),(r'ifc|bim','IFC en BIM')]:
            if re.search(pattern,haystack): category=cat; break
        FUNCTIONS[key]={'id':key,'category':'Betekenisconflicten' if n in ambiguous else category,
                        'label':ambiguous.get(n,words(label or value))}
    return key,'nog functioneel te beoordelen'


def deduplicate():
    output={}
    for r in ROWS:
        # Keep states with distinct artwork and definitions with distinct symbols.
        key=(r['repository'],r['commit'],r['path'],r['line'],r['exact_hash'],norm(r['name']))
        if key in output:
            other=output[key]
            other['origins']=sorted(set(other['origins']+[r['origin']]))
            if other['evidence']!='bronreview' and r['evidence']=='bronreview':
                r['origins']=other['origins']; output[key]=r
        else:
            r['origins']=[r['origin']]; output[key]=r
    return list(output.values())


def main():
    manifest=read(H/'function-icon-sources.json')
    SOURCE_PATHS.update({(r['repository'],r['commit']):{f['path'] for f in r['files']} for r in manifest['repositories']})
    inventory={r['name']:r for r in read(H/'inventory.json')}
    libraries(); assessments(); translations(manifest); audit_records(inventory); collect_imports(manifest); source_sites(manifest); asset_sites(manifest); manifest_icons(manifest)
    rows=deduplicate()
    groups=defaultdict(list)
    for i,row in enumerate(rows):
        key,status=categorize(row); row['function_id']=key; row['function_status']=status
        row['id']=hashlib.sha256(json.dumps([row[k] for k in ('repository','commit','path','line','name','exact_hash')]).encode()).hexdigest()[:16]
        groups[key].append(row)
    # Unnamed SVGs can join a *candidate* function only when the geometry has one
    # unambiguous named function. Reused artwork with conflicting functions stays apart.
    meanings=defaultdict(set)
    for r in rows:
        if r['geometry_hash'] and not r['function_id'].startswith('review.'):
            meanings[r['geometry_hash']].add(r['function_id'])
    for row in rows:
        if ':svg-' in row['name'] and row['function_id'].startswith('review.'):
            targets=meanings[row['geometry_hash']]
            if len(targets)==1:
                old=row['function_id']; target=next(iter(targets))
                groups[old].remove(row); row['function_id']=target
                row['function_status']='vormkandidaat; functie controleren'; groups[target].append(row)
    groups={k:v for k,v in groups.items() if v}
    for row in rows:
        row['function_label']=FUNCTIONS[row['function_id']]['label']
        row['category']=FUNCTIONS[row['function_id']]['category']
    functions=[]
    for key,items in groups.items():
        known=[r for r in items if r['geometry_hash']]
        hashes={r['geometry_hash'] for r in known}
        apps=sorted({r['app'] for r in items})
        compare='Vorm ontbreekt of is niet geometrisch vergelijkbaar'
        if len(hashes)>1: compare='Verschillende geometrie binnen deze functiekandidaten'
        elif len(hashes)==1: compare='Eén geometrie in de vergelijkbare bronnen'
        functions.append({**FUNCTIONS[key], 'apps':apps,'occurrences':len(items),
                          'shape_count':len(hashes),'comparison':compare,
                          'requires_review':any(r['function_status']!='bronreview van functie' for r in items),
                          'record_ids':[r['id'] for r in items]})
    order=['Bestanden','Bewerken','Selecteren','Navigatie en zoeken','Venster en panelen','Lijsten en bomen','Instellingen en hulp','Tekenen en annoteren','Meten en maatvoering','Transformeren','Tekstopmaak','Objecten en lagen','Project en gegevens','Rapporten','IFC en BIM','Geotechniek','Energie en warmte','Paalplan','Planning','Pagina’s','Spraak en audio','Extensies','Status en meldingen','Appspecifieke opdrachten','Betekenisconflicten','Overige functies — broncontrole nodig']
    functions.sort(key=lambda r:(order.index(r['category']) if r['category'] in order else 99,r['label'].lower()))
    shapes=defaultdict(list)
    for row in rows:
        if row['geometry_hash']: shapes[row['geometry_hash']].append(row)
    collisions=[]
    for shape,items in shapes.items():
        keys={r['function_id'] for r in items if not r['function_id'].startswith('review.')}
        if len(keys)>1:
            collisions.append({'geometry_hash':shape,'function_ids':sorted(keys),'record_ids':[r['id'] for r in items],
                               'status':'Gelijke geometrie bij verschillende functiekandidaten; broncontext controleren'})
    coverage=[]
    for app in dict.fromkeys(APPS.values()):
        sources=[{**{k:v for k,v in r.items() if k!='files'},'license':inventory.get(r['repository'],{}).get('license','UNKNOWN')} for r in manifest['repositories'] if r['app']==app]
        app_rows=[r for r in rows if r['app']==app]
        coverage.append({'app':app,'sources':sources,'occurrences':len(app_rows),
                         'reviewed_occurrences':sum(r['evidence']=='bronreview' for r in app_rows),
                         'source_candidates':sum(r['evidence']=='SVG-bronplaats' for r in app_rows),
                         'missing_visuals':sum(not r['visual'] for r in app_rows),
                         'status':'Bron ontbreekt' if not app_rows else 'Verzameld; aanvullende bronrollen en functies te controleren'})
    result={'scope':manifest['scope'],'basis':manifest['basis'],
            'rules':['Een record is een bronvoorkomen, geen uniek icoon of unieke opdracht.',
                     'Naam- en labelgroepen zijn functiekandidaten, tenzij de bronreview expliciet een functie koppelt.',
                     'Gelijke geometrie bewijst geen gelijke betekenis. Verschillende geometrie kan dezelfde functie bedienen.',
                     'Geometriehash vergelijkt XML-geometrie zonder verf en afmetingen van de SVG-wrapper; visueel gelijke herschreven paden kunnen verschillende hashes hebben.',
                     'Onbeoordeelde SVG-bronplaatsen omvatten mogelijk diagrammen, logo’s of ongebruikte code; deze zijn apart filterbaar.',
                     'Runtime-extensies, dynamische iconen en ontbrekende bronnen verhinderen een claim van volledige productdekking.'],
            'summary':{'apps':len(coverage),'occurrences':len(rows),'functions':len(functions),
                       'cross_app_functions':sum(len(f['apps'])>1 for f in functions),
                       'different_shape_functions':sum(f['shape_count']>1 for f in functions),
                       'same_shape_different_function_candidates':len(collisions),
                       'missing_visuals':sum(not r['visual'] for r in rows)},
            'coverage':coverage,'functions':functions,'shape_collisions':collisions,
            'records':[{k:v for k,v in r.items() if k!='visual'} for r in rows],
            'excluded':EXCLUDED,'warnings':WARNINGS}
    (H/'function-icon-catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Remove only orphaned hash-named files created by this generator, inside
    # this task's dedicated output folder. Never touch the upstream archives.
    expected={str((ROOT/r['asset']).resolve()) for r in rows if r['asset']}
    output_root=OUT.resolve()
    assert output_root.is_relative_to((ROOT/'harmonization').resolve())
    for path in OUT.iterdir():
        if path.is_file() and re.fullmatch(r'[0-9a-f]{64}\.(svg|png|ico|webp)',path.name) and str(path.resolve()) not in expected:
            assert path.resolve().parent==output_root
            path.unlink()
    with (H/'function-icon-catalog.csv').open('w',newline='',encoding='utf-8-sig') as file:
        keys=['app','category','function_id','function_label','function_status','name','label','evidence','path','line','commit','exact_hash','geometry_hash','asset','source_url','state']
        writer=csv.DictWriter(file,fieldnames=keys,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)
    # Embed images once, then refer to IDs, so the page works directly from disk.
    images={r['exact_hash']:r['visual'] for r in rows if r['visual']}
    render(result,images)
    print(json.dumps(result['summary'],ensure_ascii=False))


def render(result,images):
    payload=json.dumps({'catalog':result,'images':images},ensure_ascii=False).replace('</','<\\/')
    page=PAGE.replace('/* DATA */',payload).replace('src="${image}"','src="${image[d?\'dark\':\'light\']}"')
    page=page.replace('bronvoorkomens','bronrecords').replace('voorkomens','bronrecords')
    page=page.replace('Bronbronrecords','Bronrecords')
    (DESIGN/'function-icon-catalog.html').write_text(page,encoding='utf-8')


PAGE=r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · Iconen per functie</title><style>
:root{color-scheme:light;--bg:#f4f5f7;--card:#fff;--text:#182432;--muted:#5a6877;--line:#d8dee6;--accent:#087d75}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,sans-serif}body.dark{color-scheme:dark;--bg:#161c24;--card:#222b36;--text:#edf2f6;--muted:#a8b8c8;--line:#3c4a5b;--accent:#70d6cb}header{background:#142c3c;color:#fff;padding:36px max(24px,calc((100vw - 1420px)/2));border-top:5px solid #11a599}header p{max-width:950px;color:#cbd8e0}h1{margin:0;font-size:32px}h2{font-size:22px;margin:0}h3{margin:0;font-size:17px}main{max-width:1468px;margin:auto;padding:24px}button,select,input{font:inherit;border:1px solid var(--line);border-radius:6px;padding:9px 12px;background:var(--card);color:var(--text)}button{cursor:pointer}button.active{background:var(--accent);color:var(--bg)}a{color:var(--accent)}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}.stat{padding:12px 18px;background:var(--card);border:1px solid var(--line);border-radius:8px}.stat b{display:block;font-size:24px}.controls{position:sticky;top:0;background:var(--bg);padding:14px 0;z-index:4;display:flex;gap:8px;flex-wrap:wrap;border-bottom:1px solid var(--line)}input{flex:1;min-width:240px}.notice{padding:16px;border-left:4px solid #d29421;background:var(--card);margin:16px 0}.muted,small{color:var(--muted)}.function{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:16px 0;overflow:hidden}.function>summary{cursor:pointer;padding:18px;display:flex;justify-content:space-between;gap:20px}.function>summary:hover{background:var(--bg)}.groupmeta{color:var(--muted);font-size:13px}.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;padding:0 18px 18px}.card{border:1px solid var(--line);border-radius:8px;padding:14px;min-width:0;overflow:hidden}.card b{display:block}.samples{display:flex;gap:8px;margin:12px 0}.sample{height:66px;flex:1;display:flex;align-items:center;justify-content:center;border:1px solid #596879;border-radius:5px;background:#f6f7fa;color:#152335}.sample.night{background:#202831;color:#edf2f6}.sample img{width:var(--size,24px);height:var(--size,24px);object-fit:contain}.missing{font-size:11px;text-align:center;color:#9c5a0a}.badge{display:inline-block;border:1px solid var(--line);font-size:11px;border-radius:4px;padding:2px 5px;margin-top:5px}.card details{margin-top:10px;font-size:12px}pre{white-space:pre-wrap;word-break:break-word;max-height:220px;overflow:auto}code{overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--line);vertical-align:top}th{position:sticky;top:135px;background:var(--card)}.scroll{overflow:auto}.section{margin-top:24px}.hidden{display:none}#count{margin:14px 0}.category{font-size:13px;color:var(--accent);font-weight:700;margin-bottom:4px}.more{margin:10px 18px 18px}footer{padding:24px 0;color:var(--muted)}@media(max-width:650px){header{padding:24px}.function>summary{display:block}.cards{grid-template-columns:1fr}h1{font-size:26px}}
</style><header><h1>Iconen per functie</h1><p>OpenAEC · bronverzameling en vergelijking voor de gezamenlijke iconenset. Vergelijk de oorspronkelijke vormen, bekijk welke apps ze gebruiken en scheid gelijke vormen met verschillende opdrachten.</p><button id="theme">Licht / donker</button> <button id="download">Download JSON</button> <a style="color:#a4e6df" href="../harmonization/function-icon-catalog.csv">CSV openen</a></header><main>
<div class="stats" id="stats"></div><div class="notice"><b>Verzameling ≠ afgeronde functiebeoordeling.</b> Functies uit bronreviews, labelkandidaten en onbeoordeelde SVG-bronplaatsen blijven herkenbaar. FEM heeft geen toegankelijke bron. De oorspronkelijke broncommits staan bij elk voorkomen. Gelijke geometrie bewijst geen gelijke betekenis; kleuren en lijndiktes kunnen verschillen.</div>
<div class="controls"><input id="search" type="search" placeholder="Zoek functie, icoon, bronbestand of app…" aria-label="Zoeken"><select id="app" aria-label="App"><option value="">Alle apps</option></select><select id="category" aria-label="Functiegroep"><option value="">Alle functiegroepen</option></select><select id="mode" aria-label="Vergelijking"><option value="all">Alle functiekandidaten</option><option value="cross">In meerdere apps</option><option value="different">Verschillende vormen</option><option value="same">Eén geometrie, meerdere apps</option><option value="collision">Gelijke vorm, andere functie</option><option value="missing">Vorm ontbreekt</option></select><select id="evidence" aria-label="Bronzekerheid"><option value="">Alle bewijsklassen</option><option value="bronreview">Bestaande bronreviews</option><option value="bibliotheek-aanroep">Bibliotheek-aanroepen</option><option value="SVG-bronplaats">Onbeoordeelde SVG-bronplaatsen</option><option value="teksticoon-kandidaat">Teksticonen</option><option value="bestandsverwijzing">Bestandsverwijzingen</option><option value="getypeerde Rust-aanroep">Getypeerde Rust-aanroepen</option><option value="manifest-icoon">Extensiecatalogi</option></select><select id="size" aria-label="Icoongrootte"><option>24</option><option>16</option><option>32</option></select><button id="catalogTab" class="active">Per functie</button><button id="matrixTab">App × functie</button><button id="coverageTab">Dekking en open werk</button></div>
<div id="count" class="muted" aria-live="polite"></div><section id="catalog"></section><section id="matrix" class="hidden scroll"></section><section id="coverage" class="hidden"></section><footer>Reviewmateriaal voor versie 0.4. De gezamenlijke iconenset wordt in een volgende stap ontworpen. Broniconen en de Rust-crate zijn niet gewijzigd.</footer></main>
<script type="application/json" id="data">/* DATA */</script><script>
const {catalog:c,images}=JSON.parse(document.querySelector('#data').textContent);const $=s=>document.querySelector(s);const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));const byId=Object.fromEntries(c.records.map(r=>[r.id,r]));const collisionIds=new Set(c.shape_collisions.flatMap(x=>x.record_ids));let tab='catalog';
$('#stats').innerHTML=[['apps',c.summary.apps],['bronvoorkomens',c.summary.occurrences],['functie- en bronclusters',c.summary.functions],['functies in meerdere apps',c.summary.cross_app_functions],['groepen met verschillende vormen',c.summary.different_shape_functions]].map(([a,b])=>`<div class="stat"><b>${b}</b>${a}</div>`).join('');
for(const a of c.coverage)$('#app').insertAdjacentHTML('beforeend',`<option>${esc(a.app)}</option>`);for(const cat of [...new Set(c.functions.map(f=>f.category))].sort())$('#category').insertAdjacentHTML('beforeend',`<option>${esc(cat)}</option>`);
function card(r){const image=images[r.exact_hash];return `<article class="card"><b>${esc(r.app)}</b><span>${esc(r.label)}</span><div class="samples">${[false,true].map(d=>`<div class="sample ${d?'night':''}">${image?`<img loading="lazy" src="${image}" alt="${esc(r.name)}">`:`<span class="missing">${r.evidence==='teksticoon-kandidaat'?esc(r.label):'Geen vaste vorm beschikbaar'}</span>`}</div>`).join('')}</div><small>${esc(r.name)} · ${esc(r.repository==='open-pdf-studio-v3'?'PDF v3':r.role||r.evidence)}</small><br><span class="badge">${esc(r.evidence)}</span> <span class="badge">${esc(r.function_status)}</span><div><small>Geometrie ${esc((r.geometry_hash||'onbekend').slice(0,10))}</small></div><details><summary>Bron, context en toestand</summary><p>${r.source_url?`<a href="${esc(r.source_url)}" target="_blank" rel="noopener">${esc(r.path)}:${r.line}</a>`:esc(r.path)}</p><code>${esc((r.commit||'').slice(0,12))}</code><p>${esc(r.state)}</p>${r.assessment?.meaning?`<p><b>Bestaande functiebeoordeling:</b> ${esc(r.assessment.meaning)}<br>${esc(r.assessment.rationale)}</p>`:""}<pre>${esc(r.context)}</pre><p>${esc(r.origins.join(', '))}</p></details></article>`}
function matches(){const q=$('#search').value.toLowerCase(),app=$('#app').value,cat=$('#category').value,mode=$('#mode').value,evidence=$('#evidence').value;return c.functions.map(f=>{let rows=f.record_ids.map(id=>byId[id]);rows=rows.filter(r=>(!app||r.app===app)&&(!evidence||r.evidence===evidence)&&(!q||[f.label,f.id,r.label,r.name,r.app,r.path].join(' ').toLowerCase().includes(q)));if(mode==='missing')rows=rows.filter(r=>!images[r.exact_hash]);if(mode==='collision')rows=rows.filter(r=>collisionIds.has(r.id));return {f,rows}}).filter(({f,rows})=>rows.length&&(!cat||f.category===cat)&&(mode!=='cross'||f.apps.length>1)&&(mode!=='different'||f.shape_count>1)&&(mode!=='same'||f.shape_count===1&&f.apps.length>1))}
function render(){for(const name of ['catalog','matrix','coverage'])$('#'+name).classList.toggle('hidden',name!==tab);const found=matches();$('#count').textContent=`${found.length} functiegroepen · ${found.reduce((a,x)=>a+x.rows.length,0)} bronvoorkomens in deze selectie`;if(tab==='catalog'){const el=$('#catalog');el.innerHTML='';for(const {f,rows} of found){rows.sort((a,b)=>a.app.localeCompare(b.app)||a.path.localeCompare(b.path)||a.line-b.line);const detail=document.createElement('details');detail.className='function';detail.innerHTML=`<summary><div><div class="category">${esc(f.category)}</div><h3>${esc(f.label)}</h3><small>${esc(f.id)}</small></div><div class="groupmeta">${f.apps.length} apps · ${rows.length} voorkomens · ${f.shape_count} geometrieën<br>${esc(f.comparison)}${f.requires_review?'<br>Functiebeoordeling open':''}</div></summary><div class="cards"></div>`;detail.addEventListener('toggle',()=>{if(detail.open&&!detail.dataset.loaded){detail.dataset.loaded='1';const container=detail.querySelector('.cards');let n=0;const more=document.createElement('button');more.className='more';function next(){container.insertAdjacentHTML('beforeend',rows.slice(n,n+60).map(card).join(''));n+=60;more.textContent=`Meer voorkomens (${Math.max(0,rows.length-n)})`;more.hidden=n>=rows.length}more.onclick=next;detail.append(more);next()}});el.append(detail)}if(found.length&&found.length<=5)el.querySelector('details').open=true}
if(tab==='matrix'){const apps=c.coverage.map(a=>a.app);$('#matrix').innerHTML=`<table><thead><tr><th>Functie / voorkomens</th>${apps.map(a=>`<th>${esc(a)}</th>`).join('')}</tr></thead><tbody>${found.map(({f,rows})=>`<tr><td><b>${esc(f.label)}</b><br><small>${esc(f.category)}</small></td>${apps.map(a=>{const rs=rows.filter(r=>r.app===a),shapes=new Set(rs.map(r=>r.geometry_hash).filter(Boolean));return `<td>${rs.length?`${rs.length} plaatsen<br><small>${shapes.size} geometrieën</small>`:'<span class="muted">—</span>'}</td>`}).join('')}</tr>`).join('')}</tbody></table>`}
if(tab==='coverage'){$('#coverage').innerHTML=`<h2>Dekking per app</h2><p>Een streep of nul betekent geen verzameld bewijs, en bewijst niet dat een app geen icoon heeft. De bronscan selecteert clientbestanden, maar bewijst geen runtime-bereikbaarheid. Externe extensiecatalogi en dynamische vormen vragen aanvullende controle.</p><div class="scroll"><table><tr><th>App</th><th>Bronvoorkomens</th><th>Bestaande review</th><th>Onbeoordeelde SVG’s</th><th>Zonder vorm</th><th>Bronstatus</th></tr>${c.coverage.map(a=>`<tr><td><b>${esc(a.app)}</b></td><td>${a.occurrences}</td><td>${a.reviewed_occurrences}</td><td>${a.source_candidates}</td><td>${a.missing_visuals}</td><td>${a.sources.map(s=>`${esc(s.repository)} · <code>${esc((s.commit||'geen commit').slice(0,12))}</code><br>${esc(s.status)} · ${(s.files||[]).length||s.selected_files||0} bestanden${s.errors.length?' · '+s.errors.length+' fouten':''}`).join('<br>')}</td></tr>`).join('')}</table></div><h2 class="section">Wat moet nog beoordeeld worden?</h2><ol><li>Bronrollen van automatisch gevonden SVG’s: opdracht, status, branding, illustratie, diagram of ongebruikte definitie.</li><li>Functie van naam- en labelkandidaten controleren tegen de werkelijke handler. Download, plus, kruis, hand en raster kunnen per context iets anders doen.</li><li>Dynamische SVG’s en bibliotheekvormen zonder vaste preview exporteren met de juiste bronversie.</li><li>Extern aangeleverde extensie-iconen en ontbrekende FEM-bron aanvullen.</li><li>Daarna per vastgestelde functie één ontwerp kiezen en 16/24/32 px plus toestanden beoordelen.</li></ol><details><summary>${c.excluded.length} bewaarde uitsluitingen en onzekere assets · ${c.warnings.length} ontbrekende bestandsverwijzingen</summary><p>De volledige redenen en records staan in de JSON-export.</p><pre>${esc(JSON.stringify(c.warnings,null,2))}</pre></details><h2 class="section">Vergelijkingsregels</h2><ul>${c.rules.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`}}
for(const id of ['search','app','category','mode','evidence'])$('#'+id).addEventListener(id==='search'?'input':'change',render);$('#size').onchange=()=>document.documentElement.style.setProperty('--size',$('#size').value+'px');$('#theme').onclick=()=>document.body.classList.toggle('dark');for(const t of ['catalog','matrix','coverage'])$('#'+t+'Tab').onclick=()=>{tab=t;for(const n of ['catalog','matrix','coverage'])$('#'+n+'Tab').classList.toggle('active',n===t);render()};$('#download').onclick=()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(c,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='function-icon-catalog.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};render();
</script></html>'''


if __name__ == '__main__':
    main()
