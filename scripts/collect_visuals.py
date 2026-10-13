"""Collect existing UI screenshots and implementation references for visual review."""
import concurrent.futures as futures
import importlib.util
import json,re,subprocess
from pathlib import Path
spec=importlib.util.spec_from_file_location('inventory',Path(__file__).with_name('inventory.py'));inv=importlib.util.module_from_spec(spec);spec.loader.exec_module(inv)
OUT=inv.OUT

def collect(r):
 name=r['name']; repo=inv.CACHE/name
 out={'name':name,'commit':r.get('commit'),'screenshots':[],'ui_sources':[],'errors':[]}
 if not r.get('commit'):return out
 paths=inv.git(repo,'ls-tree','-r','--name-only','HEAD').splitlines()
 ui=[];screens=[]
 for p in paths:
  low=p.lower();base=Path(p).name.lower()
  if any(x in low for x in ['node_modules/','vendor/','tests/fixtures/']):continue
  if base in ['readme.md','readme.rst'] and p.count('/')<2: ui.append(p)
  elif re.search(r'\.(tsx?|css|rs|slint)$',low) and re.search(r'(ribbon|backstage|theme|titlebar|documentbar|app\.tsx$|app\.slint$)',base) and p.count('/')<7:ui.append(p)
  if re.search(r'\.(png|jpe?g|webp)$',low) and re.search(r'screenshot|screens/|preview|ribbon-approved|ui-reference',low) and not re.search(r'icon|logo',low):screens.append(p)
 def score(p):
  low=p.lower();return sum(v for word,v in [('native',8),('approved',10),('light',8),('ribbon',5),('home',4),('main',4),('overview',4),('backstage',3),('settings',2),('dark',2),('error',-15),('debug',-10),('broken',-10)] if word in low)
 chosen=sorted(screens,key=lambda p:(-score(p),len(p)))[:3]
 for p in sorted(set(ui))[:35]+chosen:
  kind='screenshots' if p in chosen else 'ui_sources'
  url=f'https://raw.githubusercontent.com/{r["url"].removeprefix("https://github.com/")}/{r["commit"]}/{inv.urllib.parse.quote(p)}'
  dest=OUT/'references'/name/p
  try:
   if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(inv.fetch(url))
   out[kind].append({'path':p,'url':url,'local':str(dest.relative_to(OUT))})
  except Exception as e:out['errors'].append({'path':p,'error':str(e)})
 out['available_screenshots']=screens
 print(name,len(screens),'screenshots,',len(out['screenshots']),'selected',flush=True)
 return out
results=[json.load(open(p)) for p in (OUT/'repositories').glob('*.json')]
with futures.ThreadPoolExecutor(max_workers=8) as pool:references=list(pool.map(collect,results))
(OUT/'visual-references.json').write_text(json.dumps(references,indent=2))
