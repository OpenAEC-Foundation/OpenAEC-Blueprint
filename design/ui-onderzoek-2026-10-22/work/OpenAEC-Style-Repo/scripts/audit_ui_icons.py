"""Find direct UI references to archived assets without treating SVG as an icon."""
from __future__ import annotations
import concurrent.futures as cf
import json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'harmonization'
REPOS=H/'repositories'
ARCHIVED={p.stem:json.loads(p.read_text()) for p in REPOS.glob('*.json')}
CODE={'.rs','.slint','.ts','.tsx','.js','.jsx','.mjs','.html','.css','.vue','.svelte','.py','.cpp','.h','.hpp','.dl'}
SKIP={'target','node_modules','vendor','third_party','test','tests','docs','examples','__tests__','benches','.worktrees','_archive','open-pdf-render','pdfium-worker','build','dist','public','coverage','.next','storybook-static'}
UI_SEGMENTS={'ui','frontend','renderer','classic','viewer','components','ribbon','toolbar','widgets','panels','pages','views','webpagina'}
PATTERN=r'(icon|\.svg|\.png|\.ico|\.webp|logo|favicon|toolbar|ribbon|sprite|lucide|phosphor|heroicon|assets/|resource_path|include_bytes!)'

def ocondat_ui_source(path):
 """Audit the two web UIs, not their generated component data or drawing CSS."""
 if path.startswith('DXF Library/component-library/'):
  return Path(path).suffix.lower() in {'.html','.css'} or path in {
   'DXF Library/component-library/js/app.js',
   'DXF Library/component-library/js/fabrikanten.js',
  }
 if path.startswith('Libraries/Netherlands/'):
  if path.startswith('Libraries/Netherlands/css/'):return False
  return Path(path).suffix.lower()=='.html' or path in {
   'Libraries/Netherlands/library/css/style.css',
   'Libraries/Netherlands/library/js/app.js',
   'Libraries/Netherlands/library/js/renderer.js',
  }
 return False

def is_ui_code_source(name,path):
 if name=='project-ocondat':return ocondat_ui_source(path)
 if name=='building-py':return path=='apps/GIS2BIM/GIS2BIM_location.py'
 # These repositories contain training media, drawing styles, or index/validation
 # scripts. None of those files implement a studio UI.
 if name in {'blender-bonsai-training','inb-template','open-pdf-studio-library'}:return False
 part=Path(path)
 if part.suffix.lower() not in CODE or any(x in path for x in ('.test.','.spec.','.min.')):return False
 pdfjs_viewer=name=='open-pdf-studio' and path in {
  'open-pdf-studio/public/pdfjs/web/viewer.css',
  'open-pdf-studio/public/pdfjs/web/viewer.html',
  'open-pdf-studio/public/pdfjs/web/viewer.mjs',
 }
 if SKIP.intersection(part.parts) and not pdfjs_viewer:return False
 return bool(
  UI_SEGMENTS.intersection(part.parts) or part.suffix.lower()=='.slint'
  or path.count('/')<=1
  or re.search(r'icon|ribbon|toolbar|menu|titlebar|backstage',part.name,re.I)
  or re.search(r'(?:^|/)src/(?:main|app|ui)\.rs$',path)
  or (name=='open-pointcloud-studio' and path.startswith('native/desktop/src/') and part.suffix.lower()=='.rs')
  or (name=='OpenCADStudio' and (path.startswith('src/modules/') or path.startswith('src/app/view/')))
  or (name=='open-pdf-studio' and '/pdfjs/web/' in path)
 )

def scan(item):
 name,r=item
 repo=Path('/tmp/openaec-inventory')/name
 if not (repo/'.git').exists() or not r.get('commit'):return {'repository':name,'status':'no-checkout','matches':[],'lines_scanned':0}
 files=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only','HEAD'],timeout=60).decode(errors='replace').splitlines()
 code=[p for p in files if is_ui_code_source(name,p)]
 # Read actual UI source paths. Core libraries without a UI source are left out.
 if not code:return {'repository':name,'status':'no-ui-source','matches':[],'lines_scanned':0}
 code.sort(key=lambda p:(0 if re.search(r'icon|ribbon|toolbar|menu|titlebar',p,re.I) else 1, 0 if p.endswith(('.tsx','.slint','.rs')) else 1,p))
 try:
  matches=[]
  for offset in range(0,len(code),80):
   pattern=PATTERN+(r'|QDialog|QWebEngineView|QPushButton|QCheckBox|QComboBox|QLineEdit|QGroupBox|QMessageBox|setWindowTitle' if name=='building-py' else '')
   cp=subprocess.run(['git','-C',str(repo),'grep','-I','-i','-n','-E',pattern,'HEAD','--',*code[offset:offset+80]],capture_output=True,text=True,timeout=180)
   if cp.returncode not in (0,1):raise RuntimeError(cp.stderr[:200])
   for line in cp.stdout.splitlines():
    m=re.match(r'HEAD:(.*?):(\d+):(.*)',line)
    if m:matches.append({'source':m.group(1),'line':int(m.group(2)),'text':m.group(3)[:800]})
  return {'repository':name,'status':'source-scanned','code_files':len(code),'matches':matches}
 except Exception as e:return {'repository':name,'status':'scan-failed','code_files':len(code),'error':str(e),'matches':[]}

if __name__=='__main__':
 # Scan every accessible UI repository, including code-only icon systems.
 selection=[(n,r) for n,r in ARCHIVED.items() if r.get('commit') and n!='llvm-project']
 previous_path=H/'ui-code-references.json'
 previous_order={record['repository']:index for index,record in enumerate(json.loads(previous_path.read_text()))} if previous_path.exists() else {}
 with cf.ThreadPoolExecutor(max_workers=4) as pool:
  results=[]
  for future in cf.as_completed([pool.submit(scan,item) for item in selection]):
   result=future.result();results.append(result)
   print(result['repository'],result['status'],len(result['matches']),flush=True)
 # Completion order depends on network/cache timings. Preserve the established
 # record order to keep source-audit diffs readable and reproducible.
 results.sort(key=lambda result: (previous_order.get(result['repository'],len(previous_order)),result['repository'].lower()))
 (H/'ui-code-references.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
