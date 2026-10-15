"""Collect existing UI screenshots and implementation references for visual review."""
import concurrent.futures as futures
import importlib.util
import json,re,subprocess
from pathlib import Path
spec=importlib.util.spec_from_file_location('inventory',Path(__file__).with_name('inventory.py'));inv=importlib.util.module_from_spec(spec);spec.loader.exec_module(inv)
OUT=inv.OUT
previous_path=OUT/'visual-references.json'
previous={r['name']:r for r in json.loads(previous_path.read_text())} if previous_path.exists() else {}

def collect(r):
 name=r['name']; repo=inv.CACHE/name
 changed=previous.get(name,{}).get('commit')!=r.get('commit')
 out={'name':name,'commit':r.get('commit'),'screenshots':[],'ui_sources':[],'errors':[]}
 if not r.get('commit'):return out
 paths=inv.git(repo,'ls-tree','-r','--name-only','HEAD').splitlines()
 ui=[];screens=[]
 for p in paths:
  low=p.lower();base=Path(p).name.lower()
  if any(x in low for x in ['node_modules/','vendor/','tests/fixtures/']):continue
  if base in ['readme.md','readme.rst'] and p.count('/')<2: ui.append(p)
  elif re.search(r'\.(tsx?|css|rs|slint)$',low) and re.search(r'(ribbon|backstage|theme|titlebar|documentbar|app\.tsx$|app\.slint$)',base) and p.count('/')<7:ui.append(p)
  # Planner keeps its actual light/dark UI captures under artifacts/ rather
  # than screenshots/. Include those as screen candidates, not as icons.
  planner_capture = name == 'open-planner-studio' and low.startswith('artifacts/')
  energy_reference = name == 'open-energy-studio' and (low.startswith('docs/handleiding-nta8800/img/') or low.startswith('docs/ui-redesign/mockups/'))
  planner_tutorial = name == 'open-planner-studio-extensions' and low.startswith('extensions/tutorials/img/')
  cad_workspace = name == 'OpenCADStudio' and low == 'site/workspace.png'
  if re.search(r'\.(png|jpe?g|webp)$',low) and (re.search(r'screenshot|screens/|preview|ribbon-approved|ui-reference',low) or planner_capture or energy_reference or planner_tutorial or cad_workspace) and not re.search(r'icon|logo',low):screens.append(p)
 def score(p):
  low=p.lower();return sum(v for word,v in [('native',8),('approved',10),('light',8),('ribbon',5),('home',4),('main',4),('overview',4),('backstage',3),('settings',2),('dark',2),('error',-15),('debug',-10),('broken',-10)] if word in low)
 if name == 'open-planner-studio':
  # Sample distinct real UI states for layout review; all remaining artifact
  # captures still appear in the source-pinned screen inventory.
  highlights=[
   'artifacts/tabel-overhaul/22-gantt-wide-1280-en-dark.jpg',
   'artifacts/gantt-voortgang/gantt-licht.png',
   'artifacts/profielblok/eigen-profiel-bewerken-licht.png',
   'artifacts/kalender-optie2/eenvoudige-kalender-urenplanning-uit-licht.png',
   'artifacts/formaat-uitleg-popup/xer-donker.png',
   'artifacts/rapport-kolombreedtes/nl-na.png',
   'artifacts/resourcediagram/01-resourcediagram-preview-en-dark.png',
   'artifacts/balkkleuren/bars-light.png',
  ]
  chosen=[p for p in highlights if p in screens]
 elif name == 'open-energy-studio':
  highlights=[
   'docs/handleiding-nta8800/img/welkom.png',
   'docs/handleiding-nta8800/img/projectoverzicht.png',
   'docs/handleiding-nta8800/img/verwarming.png',
   'docs/handleiding-nta8800/img/resultaten.png',
   'docs/handleiding-nta8800/img/rapport.png',
   'docs/ui-redesign/mockups/00-designsystem.png',
   'docs/ui-redesign/mockups/01-projectoverzicht.png',
   'docs/ui-redesign/mockups/05b-resultaten-licht.png',
  ]
  chosen=[p for p in highlights if p in screens]
 elif name == 'open-planner-studio-extensions':
  chosen=[p for p in screens if p.endswith(('nl/tut-6-afwijking-gantt.webp','nl/tut-7-voortgangsrapport.webp'))]
 elif name == 'OpenCADStudio':
  chosen=['site/workspace.png']+[p for p in sorted(screens,key=lambda p:(-score(p),len(p))) if p!='site/workspace.png'][:2]
 else:
  chosen=sorted(screens,key=lambda p:(-score(p),len(p)))[:3]
 for p in sorted(set(ui))[:35]+chosen:
  kind='screenshots' if p in chosen else 'ui_sources'
  url=f'https://raw.githubusercontent.com/{r["url"].removeprefix("https://github.com/")}/{r["commit"]}/{inv.urllib.parse.quote(p)}'
  dest=OUT/'references'/name/p
  try:
   if not dest.exists() or changed:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(inv.fetch(url))
   out[kind].append({'path':p,'url':url,'local':str(dest.relative_to(OUT))})
  except Exception as e:out['errors'].append({'path':p,'error':str(e)})
 out['available_screenshots']=screens
 print(name,len(screens),'screenshots,',len(out['screenshots']),'selected',flush=True)
 return out
results=[json.load(open(p)) for p in (OUT/'repositories').glob('*.json')]
with futures.ThreadPoolExecutor(max_workers=8) as pool:references=list(pool.map(collect,results))
(OUT/'visual-references.json').write_text(json.dumps(references,indent=2))
