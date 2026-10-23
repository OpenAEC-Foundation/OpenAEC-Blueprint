"""Structural/provenance QA of research artifacts; no production UI test."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import sys
import base64
import re

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'outputs'
WORK=ROOT/'work/ui-research'
state=json.loads((ROOT/'work/ui-research-state.json').read_text())
sources=json.loads((OUT/'OpenAEC-UI-bronnen.json').read_text())
findings=json.loads((OUT/'OpenAEC-UI-bevindingen.json').read_text())
assert len({s['id'] for s in sources})==len(sources)
assert len({f['id'] for f in findings})==len(findings)
assert all(set(f['source_ids'])<={s['id'] for s in sources} for f in findings)
assert all(f['module'] in {m['id'] for m in state['modules']} for f in findings)
assert sources==json.loads((WORK/'sources.json').read_text())
assert findings==json.loads((WORK/'findings.json').read_text())
for source in sources:
    if source.get('local_file'):assert (ROOT/source['local_file']).is_file(),source['id']
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
parsers={}
def parse(path):
    if path not in parsers:
        p=Parser();p.feed(path.read_text());assert len(set(p.ids))==len(p.ids),str(path);parsers[path]=p
    return parsers[path]
for name in ['OpenAEC-ontwerponderzoek.html','OpenAEC-UI-verdiepingsonderzoek.html','OpenAEC-UI-ochtendoverzicht.html','OpenAEC-UI-taakproeven.html']:
    path=OUT/name
    for href in parse(path).links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=path.parent/unquote(u.path) if u.path else path
        assert target.exists(),(name,href)
        if u.fragment:assert unquote(u.fragment) in parse(target).ids,(name,href)
supplement=parse(OUT/'OpenAEC-UI-verdiepingsonderzoek.html')
font_evidence=json.loads((OUT/'OpenAEC-onderzoeksbewijs.json').read_text())['report_fonts']
embedded_fonts=re.findall(r'data:font/[^;]+;base64,([A-Za-z0-9+/=]+)',(OUT/'OpenAEC-ontwerponderzoek.html').read_text())
assert len(embedded_fonts)==len(font_evidence)==11
assert [hashlib.sha256(base64.b64decode(b,validate=True)).hexdigest() for b in embedded_fonts]==[f['sha256'] for f in font_evidence]
assert all('source-'+s['id'] in supplement.ids for s in sources)
assert all('module-'+m['id'] in supplement.ids for m in state['modules'])
for m in state['modules']:
    if m['status'] in ['researched','reviewed']:assert (WORK/'modules'/(m['id']+'.html')).exists()
manifest_files=0
for p in [WORK/'upstream/calc-b470427/manifest.json',WORK/'upstream/iced-0.13.1/manifest.json',WORK/'upstream/pdf-f754cb7/manifest.json',WORK/'upstream/validator-8f837dd/manifest.json',WORK/'upstream/style-85a6aaf/manifest.json',WORK/'upstream/pdf-e9f599f/manifest.json']:
    for entry in json.loads(p.read_text()):
        assert hashlib.sha256((p.parent/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
        manifest_files+=1
probes=json.loads((OUT/'OpenAEC-UI-proeven.json').read_text())
for p,h in probes['source_hashes'].items():assert hashlib.sha256((ROOT/'work/OpenAEC-Style-Repo'/p).read_bytes()).hexdigest()==h
for p,h in probes['calc_parser']['source_hashes'].items():assert hashlib.sha256((WORK/'upstream/calc-b470427/src/utils'/p).read_bytes()).hexdigest()==h
if 'save_controlflow' in probes:
    for p,h in probes['save_controlflow']['source_hashes'].items():assert hashlib.sha256((WORK/'upstream/calc-b470427'/p).read_bytes()).hexdigest()==h
if 'pdf_rotation' in probes:
    for p,h in probes['pdf_rotation']['source_hashes'].items():assert hashlib.sha256((WORK/'upstream/pdf-f754cb7'/p).read_bytes()).hexdigest()==h
for name in ['calc_i18n_source_locales','calc_locale_load_controlflow']:
    if name in probes:
        for p,h in probes[name]['source_hashes'].items():assert hashlib.sha256((WORK/'upstream/calc-b470427'/p).read_bytes()).hexdigest()==h
if 'calc_locale_load_controlflow' in probes:
    exact=(WORK/'probes/locale/loadLocale-exact.ts.txt').read_text()
    assert hashlib.sha256(exact.encode()).hexdigest()==probes['calc_locale_load_controlflow']['source_function_sha256']
    assert exact in (WORK/'upstream/calc-b470427/src/i18n/config.ts').read_text()
    assert exact.replace('export async function','async function',1) in (ROOT/probes['calc_locale_load_controlflow']['harness']).read_text()
for name,base in [('pdf_word_boundary',WORK/'upstream/pdf-f754cb7'),('calc_print_colour_static',WORK/'upstream/calc-b470427')]:
    if name in probes:
        for p,h in probes[name]['source_hashes'].items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h
if 'migration_check_scope' in probes:
    for p,h in probes['migration_check_scope']['source_hashes'].items():assert hashlib.sha256((ROOT/'work/OpenAEC-Style-Repo'/p).read_bytes()).hexdigest()==h
for key,cache in [('current_head_tokens_04','style-85a6aaf'),('current_head_pdf_numeric_errors','pdf-e9f599f')]:
    if key in probes:
        for p,h in probes[key]['source_hashes'].items():assert hashlib.sha256((WORK/'upstream'/cache/p).read_bytes()).hexdigest()==h
        assert (ROOT/probes[key]['output']).is_file()
for item in probes.get('pdf_graphics_search_existing_tests',{}).values():
    for p,h in item['source_hashes'].items():assert hashlib.sha256((WORK/'upstream/pdf-f754cb7'/p).read_bytes()).hexdigest()==h
if 'pdf_word_boundary' in probes:
    exact=(WORK/'probes/graphics-search/buildPattern-exact.js.txt').read_text()
    assert hashlib.sha256(exact.encode()).hexdigest()==probes['pdf_word_boundary']['source_function_sha256']
    assert exact in (WORK/'upstream/pdf-f754cb7/open-pdf-studio/js/search/find-controller.js').read_text()
    assert exact in (ROOT/probes['pdf_word_boundary']['harness']).read_text()
coverage=json.loads((OUT/'OpenAEC-UI-dekkingsmatrix.json').read_text());assert coverage['modules']==state['modules']
contract_path=OUT/'OpenAEC-UI-componentcontracten.json'
if contract_path.exists():
    for cache,entries in json.loads(contract_path.read_text())['source_hashes'].items():
        for p,h in entries.items():assert hashlib.sha256((WORK/'upstream'/cache/p).read_bytes()).hexdigest()==h
preference_path=OUT/'OpenAEC-UI-voorkeurenaudit.json'
if preference_path.exists():
    for p,h in json.loads(preference_path.read_text())['source_hashes'].items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
task_path=OUT/'OpenAEC-UI-taakproeven.json'
if task_path.exists():
    tasks=json.loads(task_path.read_text())['fixtures']
    assert len({t['id'] for t in tasks})==len(tasks)
    for task in tasks:
        assert set(task['source_ids'])<={s['id'] for s in sources}
        assert set(task['finding_ids'])<={f['id'] for f in findings}
        assert task['id'] in parse(OUT/'OpenAEC-UI-taakproeven.html').ids
result={'checked_at':datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(timespec='seconds'),'sources':len(sources),'findings':len(findings),'researched_modules':sum(m['status'] in ('researched','reviewed') for m in state['modules']),'duplicate_ids':0,'broken_internal_or_local_links':0,'manifest_files_hash_verified':manifest_files,'review_probe_cases':len(probes['review_expression_results']),'calc_probe_cases':len(probes['calc_parser']['rows']),'save_controlflow_scenarios':len(probes.get('save_controlflow',{}).get('scenarios',[])),'existing_pdf_rotation_tests_passed':probes.get('pdf_rotation',{}).get('passed_tests'),'scope':'Artifactstructuur en bronhashes gecontroleerd. Dit script test geen browserlayout, productieapp, opslag, crash, annulering of performance.'}
result['calc_i18n_source_locales_exit_code']=probes.get('calc_i18n_source_locales',{}).get('exit_code')
result['calc_locale_load_scenarios']=len(probes.get('calc_locale_load_controlflow',{}).get('scenarios',[]))
result['calc_locale_load_assertions']=probes.get('calc_locale_load_controlflow',{}).get('assertions')
result['pdf_graphics_search_existing_tests']={k:v['counts'] for k,v in probes.get('pdf_graphics_search_existing_tests',{}).items()}
result['pdf_word_boundary_cases']=len(probes.get('pdf_word_boundary',{}).get('cases',[]))
result['migration_read_only_check_exit_codes']=[c['exit_code'] for c in probes.get('migration_check_scope',{}).get('checks',[])]
result['current_head_tokens_04_exit_code']=probes.get('current_head_tokens_04',{}).get('exit_code')
result['current_head_pdf_numeric_errors_passed']=probes.get('current_head_pdf_numeric_errors',{}).get('passed')
result['original_embedded_font_hashes_verified']=len(embedded_fonts)
if '--no-write' not in sys.argv:
    (WORK/'report-qa-latest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False))
