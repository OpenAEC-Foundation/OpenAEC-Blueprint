"""Build a local design-review report; never modifies any consuming application."""
from pathlib import Path
import json,re,hashlib,html,collections,urllib.parse,posixpath,subprocess
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'harmonization';D=ROOT/'design'
repos=sorted([json.load(open(p)) for p in (H/'repositories').glob('*.json')],key=lambda r:r['name'].lower())
meta={x['name']:x for x in json.load(open(H/'catalog.json'))}
for r in repos:
 if r['name'] in ['nextcloud-sharelink','open-aec-master-builder-I-OAMBI','master-builder-library'] and meta.get(r['name'],{}).get('size')==0:
  r['status']='empty-repository';r['errors']=[]
 else:r['status']='unavailable' if any(e.get('stage')=='access' for e in r['errors']) else 'downloaded'
(H/'inventory.json').write_text(json.dumps(repos,indent=2))
# File type alone says nothing about icon use. Keep the broad source archive and
# derive an evidence-backed UI icon set from actual UI code references.
references_path=H/'ui-code-references.json'
source_scans=json.loads(references_path.read_text()) if references_path.exists() else []
source_lines={s['repository']:s.get('matches',[]) for s in source_scans if s.get('status') in ('source-scanned','partial-source-limit')}
code_icon_sources=[]
def code_icon_names(repo,src,kind):
    checkout=Path('/tmp/openaec-inventory')/repo
    try:
        body=subprocess.check_output(['git','-C',str(checkout),'show','HEAD:'+src],stderr=subprocess.DEVNULL,timeout=15).decode(errors='replace')
    except Exception:return []
    if kind=='icon-library':
        found=[]
        for m in re.finditer(r'''import\s*\{([^}]+)\}\s*from\s*["'](?:lucide-react|@phosphor-icons[^"']*|@heroicons[^"']*|@fortawesome[^"']*|solid-icons[^"']*|@tabler/icons-react|react-icons[^"']*|@radix-ui/react-icons)["']''',body,re.S):
            found.extend(re.findall(r'\b([A-Z][A-Za-z0-9]+)(?:\s+as\s+[A-Za-z0-9]+)?\b',m.group(1)))
        return list(dict.fromkeys(found))[:100]
    if kind=='icon-component':
        return list(dict.fromkeys(re.findall(r'\b(?:function|const|export\s+const)\s+([A-Za-z][A-Za-z0-9]*Icon)\b',body)))[:100]
    names=[]
    for m in re.finditer(r'\b(?:export\s+)?(?:const|let)\s+((?:[A-Za-z][A-Za-z0-9]*Icon[A-Za-z0-9]*|icon[A-Z][A-Za-z0-9]*))\s*=',body):
        if '<svg' in body[m.end():m.end()+250]:names.append(m.group(1))
    for m in re.finditer(r'<svg\b[^>]{0,300}>',body,re.I):
        tag=m.group(0);named=re.search(r"\b(?:id|class|className)=[\"']([^\"']+)[\"']",tag)
        if named and 'icon' in named.group(1).lower():names.append(named.group(1))
    return list(dict.fromkeys(names))[:100]
for repo,lines in source_lines.items():
    if repo in ('website','Y-app-ERPNext'):continue
    grouped={}
    for line in lines:
        src=line['source']; body=line['text'].strip()
        if repo=='dynlex' and src.startswith('web/'):continue
        if any(x in src.lower().split('/') for x in ('test','tests','bench','benches','examples','docs','public','scripts','utils')) or '.test.' in src or '.spec.' in src or src.endswith(('build.rs','overview.html','create-icon.js')):continue
        if '<svg' in body.lower() and ('icon' in src.lower() or 'icon' in body.lower()):kind='inline-svg'
        elif re.search(r'''from\s*["'](?:lucide-react|@phosphor-icons|@heroicons|@fortawesome|solid-icons|@tabler/icons-react|react-icons|@radix-ui/react-icons)''',body,re.I):kind='icon-library'
        elif re.search(r'\b(?:function|const|export)\s+\w*Icon\b',body) and ('components' in src.lower().split('/') or '<svg' in body.lower()):kind='icon-component'
        else:continue
        grouped.setdefault((src,kind),[]).append(line['line'])
    for (src,kind),nums in grouped.items():
        r=next((x for x in repos if x['name']==repo),None)
        if r and r.get('commit'):
            code_icon_sources.append({'repo':repo,'source':src,'kind':kind,'lines':nums[:8],'names':code_icon_names(repo,src,kind),'url':r['url'].rstrip('/')+'/blob/'+r['commit']+'/'+urllib.parse.quote(src)})
def asset_family(repo,path):
    low=path.lower(); parts=low.split('/'); name=parts[-1]
    if repo=='dynlex' and low.startswith('web/'):
        return 'branding' if 'dynlex-icon' in name else 'illustration'
    if repo in ('project-ocondat','open-pdf-studio-library'):return 'technical-symbol'
    if 'drawings' in parts or 'sheets' in parts or any(x in name for x in ('-linework.svg','-underlay.svg','-annotation.svg')):return 'technical-drawing'
    if '/text/svg/' in low or '/fonts/' in low:return 'font'
    if ('src-tauri' in parts and 'icons' in parts) or 'logos' in parts or 'brandbook/assets/logo/' in low or 'social/' in parts or any(x in name for x in ('favicon','logo','app-icon','app_icon','storelogo','ic_launcher','wordmark','openaec-symbol','apple-touch-icon')) or name in ('icon.png','icon.ico','icon.icns','icon.svg') or re.match(r'(?:icon[-_]?\d+|128x128|32x32)',name):return 'branding'
    if any(x in parts for x in ('screenshots','screenshot','promo','illustrations')) or any(x in name for x in ('hero','banner','preview','background-pattern','color-palette')):return 'illustration'
    if 'assets/icons/' in low or 'ui/icons/' in low or '/opencad-icons/' in low or '/file-icons/' in low or '/pdfjs/web/images/' in low or '.pushbutton/icon' in low or '.pulldown/icon' in low:return 'possible-ui-icon'
    if any(x in parts for x in ('symbols','patterns','markers','component-library')):return 'technical-symbol'
    return 'unclassified'
def references_for(repo,path):
    # Resolve quoted asset paths from the referencing source file. A matching
    # basename alone is ambiguous when several directories contain save.svg.
    result=[]
    for line in source_lines.get(repo,[]):
        src=line['source']; body=line['text'].strip()
        if any(x in src.lower().split('/') for x in ('test','tests','bench','benches','examples','docs','screenshots')) or src.endswith(('build.rs','overview.html')) or body.startswith(('//','/*','*','#')):continue
        quoted_paths=re.findall(r'''["']([^"']+\.(?:svg|png|ico|icns|bmp|webp|xpm))["']''',body,re.I)
        css_urls=re.findall(r'''url\(\s*["']?([^"')\s]+\.(?:svg|png|ico|icns|bmp|webp|xpm))["']?\s*\)''',body,re.I)
        for quoted in dict.fromkeys(quoted_paths+css_urls):
            clean=quoted.split('?',1)[0].replace('\\','/')
            candidates={posixpath.normpath(posixpath.join(posixpath.dirname(src),clean))}
            if clean.startswith('/'):candidates.add(clean.lstrip('/'))
            if clean.startswith('@/'):candidates.add('src/'+clean[2:])
            if clean.startswith('assets/'):candidates.add(clean)
            if path in candidates:
                result.append({'source':src,'line':line['line'],'reference':quoted})
                break
    return result[:12]
pyrevit_files=set(subprocess.check_output(['git','-C','/tmp/openaec-inventory/pyrevit-gis2bim','ls-tree','-r','--name-only','HEAD'],text=True).splitlines())
def bundle_reference(repo,path):
    if repo!='pyrevit-gis2bim' or not path.endswith('.pushbutton/icon.png') or '/_archived/' in path:return []
    parent=posixpath.dirname(path)
    for name in ('script.py','script.cs','script.dyn','bundle.yaml'):
        sibling=parent+'/'+name
        if sibling in pyrevit_files:return [{'source':sibling,'line':0,'reference':'pyRevit pushbutton/icon.png bundle convention'}]
    return []
assets=[];hashes=collections.defaultdict(list)
for r in repos:
 for a in r['icons']:
  path=a['path'];family=asset_family(r['name'],path);refs=references_for(r['name'],path);bundle_refs=bundle_reference(r['name'],path)
  if not refs:refs=bundle_refs
  # An explicit UI-code reference is necessary to mark a file as used.
  status='ui-used' if (refs and family in ('possible-ui-icon','unclassified')) or bundle_refs else family
  preview_root='ui-icons' if status=='ui-used' else 'sources'
  record={'repo':r['name'],'path':path,'category':status,'family':family,'ui_references':refs,'evidence_type':'framework-convention' if bundle_refs and refs==bundle_refs else 'direct-path' if refs else None,'sha256':a['sha256'],'url':a['source_url'],'file':'../harmonization/'+preview_root+'/'+urllib.parse.quote(r['name']+'/'+path),'bytes':a['bytes']}
  assets.append(record);hashes[a['sha256']].append(r['name']+'/'+path)
(H/'asset-index.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2))
(H/'duplicates.json').write_text(json.dumps({k:v for k,v in hashes.items() if len(v)>1},indent=2))
proposals=json.load(open(D/'domain-icon-proposals.json'))
synonyms={'node':['node','knoop'],'beam':['beam','balk','staaf'],'column':['column','kolom'],'slab':['slab','vloer'],'wall':['wall','wand','muur'],'door':['door','deur'],'window':['window','raam','kozijn'],'mesh':['mesh','net'],'section':['section','doorsnede'],'point-load':['point_load','point-load','puntlast'],'line-load':['line_load','line-load','lijnlast'],'fixed-support':['fixed_support','inklemming'],'pinned-support':['pin_support','scharnier'],'roller-support':['roller','roloplegging'],'spring-support':['spring','veer'],'stress':['stress','spanning'],'deformation':['deform','vervorming'],'clash':['clash'],'bcf-issue':['bcf','issue'],'ids-check':['ids','validation'],'storey':['storey','verdieping','bouwlaag'],'stair':['stair','trap'],'roof':['roof','dak'],'footing':['footing','fundering'],'pile':['pile','paal'],'material':['material','materiaal'],'dimension':['dimension','maat'],'sheet':['sheet','layout'],'export':['export'],'grid':['grid','stramien']}
for p in proposals:
 key=p['id'].split('.',1)[1];terms=synonyms.get(key,[key,key.replace('-','_')]);matches=[a for a in assets if a['category']=='ui-used' and any(t in Path(a['path']).stem.lower() for t in terms)]
 p['name_match_count']=len(matches);p['candidate_assets']=[{'repo':a['repo'],'path':a['path']} for a in matches[:12]]
 p['existing_match']='candidates-found-requires-visual-review' if matches else 'no-filename-match-not-proof-of-absence'
(D/'domain-icon-proposals.json').write_text(json.dumps(proposals,ensure_ascii=False,indent=2))
refs=json.load(open(H/'visual-references.json'))
screen_kinds={(s['repository'],s['path']):s['kind'] for s in json.load(open(H/'screen-index.json'))['screens']}
# Exclude non-UI promotional artwork after visual inspection of contact sheets.
excluded=['social-preview','ifccad-prototype','open-books.jpg']
shots=[{'repo':r['name'],**s,'kind':screen_kinds.get((r['name'],s['path']),'unclassified')} for r in refs for s in r['screenshots'] if not any(x in r['name']+'/'+s['path'] for x in excluded)]
counts=collections.Counter(a['category'] for a in assets)
summary={'repositories':len(repos),'accessible':sum(r['status']=='downloaded' for r in repos),'empty':sum(r['status']=='empty-repository' for r in repos),'unavailable':sum(r['status']=='unavailable' for r in repos),'assets':len(assets),'unique_hashes':len(hashes),'duplicate_occurrences':len(assets)-len(hashes),'categories':counts,'screen_images_archived':len(shots),'screen_candidates':json.load(open(H/'screen-index.json'))['total'],'usable_ui_references':len(shots),'ui_reference_repositories':len(set(s['repo'] for s in shots)),'domain_proposals':len(proposals),'name_matches':sum(bool(p['name_match_count']) for p in proposals),'verified_ui_icon_files':sum(a['category']=='ui-used' for a in assets),'direct_ui_icon_files':sum(a['category']=='ui-used' and a['evidence_type']=='direct-path' for a in assets),'convention_ui_icon_files':sum(a['category']=='ui-used' and a['evidence_type']=='framework-convention' for a in assets),'code_icon_source_files':len(set((a['repo'],a['source']) for a in code_icon_sources)),'source_audit_repositories':sum(s.get('status') in ('source-scanned','partial-source-limit') for s in source_scans),'errors':sum(len(r['errors']) for r in repos)}
(D/'summary.json').write_text(json.dumps(summary,indent=2))
(H/'ui-icon-code-sources.json').write_text(json.dumps(code_icon_sources,ensure_ascii=False,indent=2))
# Inline compact data; render thumbnails only for the current page.
repo_by_name={r['name']:r for r in repos}
def evidence_url(a):
    if not a['ui_references']:return ''
    r=repo_by_name[a['repo']];ref=a['ui_references'][0]
    return r['url'].rstrip('/')+'/blob/'+r['commit']+'/'+urllib.parse.quote(ref['source'])+('#L'+str(ref['line']) if ref['line'] else '')
data={'summary':summary,'repos':[{k:r.get(k) for k in ['name','url','status','ui_stack','license','commit','errors']}|{'archived_assets':len(r['icons']),'sources':len(r['icon_sources']),'direct_ui_icons':sum(a['category']=='ui-used' for a in assets if a['repo']==r['name'])} for r in repos],'assets':[[a[k] for k in ['repo','path','category','file','sha256']]+[evidence_url(a),a['evidence_type']] for a in assets],'code_icon_sources':code_icon_sources,'proposals':proposals,'screens':shots,'apps':json.load(open(D/'app-layouts.json'))}
page=(D/'review-template.html').read_text().replace('/*DATA*/',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
(D/'review.html').write_text(page)
print(json.dumps(summary,indent=2))
