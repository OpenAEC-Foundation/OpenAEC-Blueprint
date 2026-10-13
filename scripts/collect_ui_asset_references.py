"""Archive raster UI icon files found by exact paths after the source audit.

The initial broad asset pass saves every SVG but only icon-named raster files.
This pass catches neutral PNG/WebP filenames referenced by icon-bearing UI code.
"""
from __future__ import annotations
import hashlib,json,posixpath,re,subprocess,urllib.parse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'harmonization'
scans=json.loads((H/'ui-code-references.json').read_text())
EXT=('png','webp','bmp','xpm')
quoted=re.compile(r'''["']([^"']+\.(?:png|webp|bmp|xpm))["']''',re.I)
css_url=re.compile(r'''url\(\s*["']?([^"')\s]+\.(?:png|webp|bmp|xpm))["']?\s*\)''',re.I)
skip_source=('test','tests','bench','benches','docs','examples','public','scripts','utils')

def candidate_paths(src,raw):
    value=raw.split('?',1)[0].replace('\\','/')
    paths={posixpath.normpath(posixpath.join(posixpath.dirname(src),value))}
    if value.startswith('/'):paths.add(value.lstrip('/'))
    if value.startswith('@/'):paths.add('src/'+value[2:])
    if value.startswith('assets/'):paths.add(value)
    return paths

added=[]
for scan in scans:
    repo=scan['repository'];meta_path=H/'repositories'/f'{repo}.json'
    if not meta_path.exists() or scan['status']!='source-scanned':continue
    meta=json.loads(meta_path.read_text());checkout=Path('/tmp/openaec-inventory')/repo
    if not (checkout/'.git').exists():continue
    files=set(subprocess.check_output(['git','-C',str(checkout),'ls-tree','-r','--name-only','HEAD'],text=True).splitlines())
    present={a['path'] for a in meta['icons']}
    found={}
    for line in scan['matches']:
        src=line['source'];body=line['text'].strip();parts=src.lower().split('/')
        if set(parts)&set(skip_source) or '.test.' in src or '.spec.' in src or body.startswith(('//','/*','*','#')):continue
        if not re.search(r'icon|toolbar|ribbon|button|<img|image-url|background-image',src+' '+body,re.I):continue
        for raw in set(quoted.findall(body)+css_url.findall(body)):
            for p in candidate_paths(src,raw):
                if p in files and p not in present and p.startswith(('src/','frontend/','apps/','app/','packages/','classic/','native/','assets/','viewer/','open-pdf-studio/')):
                    if any(x in p.lower() for x in ('screenshot','logo','favicon','src-tauri/icons/','hero','banner')):continue
                    found.setdefault(p,[]).append((src,line['line']))
    for p,refs in sorted(found.items()):
        try:data=subprocess.check_output(['git','-C',str(checkout),'show','HEAD:'+p],timeout=20)
        except Exception:continue
        if len(data)>1024*1024:continue
        dest=H/'sources'/repo/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        record={'path':p,'kind':'icon','source_url':meta['url'].rstrip('/')+'/raw/'+meta['commit']+'/'+urllib.parse.quote(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        meta['icons'].append(record);present.add(p);added.append({'repo':repo,'path':p,'references':refs[:8]})
    if found:meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2))
(H/'additional-ui-assets.json').write_text(json.dumps(added,ensure_ascii=False,indent=2))
print('New source-linked raster assets:',len(added))
