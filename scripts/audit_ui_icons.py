"""Find direct UI references to archived assets without treating SVG as an icon."""
from __future__ import annotations
import concurrent.futures as cf
import json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'harmonization'
REPOS=H/'repositories'
ARCHIVED={p.stem:json.loads(p.read_text()) for p in REPOS.glob('*.json')}
CODE={'.rs','.slint','.ts','.tsx','.js','.jsx','.html','.css','.vue','.svelte','.py','.cpp','.h','.hpp','.dl'}
SKIP={'target','node_modules','vendor','third_party','test','tests','docs','examples','__tests__','benches','.worktrees','_archive','open-pdf-render','pdfium-worker','build','dist','public','coverage','.next','storybook-static'}
UI_SEGMENTS={'ui','frontend','renderer','classic','viewer','components','ribbon','toolbar','widgets','panels','pages','views','webpagina'}
PATTERN=r'(icon|\.svg|\.png|\.ico|\.webp|logo|favicon|toolbar|ribbon|sprite|lucide|phosphor|heroicon|assets/|resource_path|include_bytes!)'

def scan(item):
 name,r=item
 repo=Path('/tmp/openaec-inventory')/name
 if not (repo/'.git').exists() or not r.get('commit'):return {'repository':name,'status':'no-checkout','matches':[],'lines_scanned':0}
 files=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only','HEAD'],timeout=60).decode(errors='replace').splitlines()
 code=[p for p in files if Path(p).suffix.lower() in CODE and (not SKIP.intersection(Path(p).parts) or (name=='open-pdf-studio' and p in ('open-pdf-studio/public/pdfjs/web/viewer.css','open-pdf-studio/public/pdfjs/web/viewer.html'))) and (UI_SEGMENTS.intersection(Path(p).parts) or p.endswith('.slint') or p.count('/')<=1 or re.search(r'icon|ribbon|toolbar|menu|titlebar|backstage',Path(p).name,re.I) or (name=='OpenCADStudio' and p.startswith('src/modules/')) or (name=='open-pdf-studio' and '/pdfjs/web/' in p)) and '.test.' not in p and '.spec.' not in p and '.min.' not in p]
 # Read actual UI source paths. Core libraries without a UI source are left out.
 if not code:return {'repository':name,'status':'no-ui-source','matches':[],'lines_scanned':0}
 code.sort(key=lambda p:(0 if re.search(r'icon|ribbon|toolbar|menu|titlebar',p,re.I) else 1, 0 if p.endswith(('.tsx','.slint','.rs')) else 1,p))
 try:
  matches=[]
  for offset in range(0,len(code),80):
   cp=subprocess.run(['git','-C',str(repo),'grep','-I','-i','-n','-E',PATTERN,'HEAD','--',*code[offset:offset+80]],capture_output=True,text=True,timeout=180)
   if cp.returncode not in (0,1):raise RuntimeError(cp.stderr[:200])
   for line in cp.stdout.splitlines():
    m=re.match(r'HEAD:(.*?):(\d+):(.*)',line)
    if m:matches.append({'source':m.group(1),'line':int(m.group(2)),'text':m.group(3)[:800]})
  return {'repository':name,'status':'source-scanned','code_files':len(code),'matches':matches}
 except Exception as e:return {'repository':name,'status':'scan-failed','code_files':len(code),'error':str(e),'matches':[]}

if __name__=='__main__':
 # Scan every accessible UI repository, including code-only icon systems.
 selection=[(n,r) for n,r in ARCHIVED.items() if r.get('commit') and n not in {'project-ocondat','open-pdf-studio-library','blender-bonsai-training','inb-template','building-py','llvm-project'}]
 with cf.ThreadPoolExecutor(max_workers=4) as pool:
  results=[]
  for future in cf.as_completed([pool.submit(scan,item) for item in selection]):
   result=future.result();results.append(result)
   print(result['repository'],result['status'],len(result['matches']),flush=True)
   (H/'ui-code-references.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 (H/'ui-code-references.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
