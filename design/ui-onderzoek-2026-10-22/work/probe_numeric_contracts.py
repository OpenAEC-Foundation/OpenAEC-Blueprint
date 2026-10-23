"""Isolate two pinned review expressions; this is not a native application test."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT / 'work/OpenAEC-Style-Repo'
WORK = ROOT / 'work/ui-research/probes'
WORK.mkdir(parents=True, exist_ok=True)
app = (REPO / 'src/bin/style_repo.rs').read_text()
pdf = (REPO / 'src/bin/style_repo/pdf_split_native.rs').read_text()
predicate = re.search(r'Action::PdfFormatLineWidth\(value\) => \{\s*if (.*?)\{\s*self.pdf_format.line_width', app, re.S).group(1).strip()
step = re.search(r'let step = (.*?);', pdf, re.S).group(1)
step = re.sub(r'self\s*\.\s*pages', 'value', step)
cases = ['', '.', '0', '-3', '1', '1.6', '0,5', '0.5', '1,234', '1.234,56', '1 234,56', '3e1', 'NaN', 'Infinity', 'abc', '−2']
literals = ','.join(json.dumps(x, ensure_ascii=False) for x in cases)
rust = ('fn main() { for value in [' + literals + '] { let accepted = ' + predicate + '; let step = ' + step + '; println!("{:?}\\t{}\\t{}",value,accepted,step); } }')
(WORK / 'numeric_probe.rs').write_text(rust)
rustc = '/home/aia08/.cargo/bin/rustc'
subprocess.run([rustc, str(WORK/'numeric_probe.rs'), '-o', str(WORK/'numeric_probe')], check=True, capture_output=True, text=True)
raw = subprocess.run([str(WORK/'numeric_probe')], check=True, capture_output=True, text=True).stdout
observations = []
for line in raw.splitlines():
    inp, accepted, pages = line.split('\t')
    observations.append({'input':json.loads(inp),'line_width_draft_accepted':accepted=='true','pdf_sample_page_step':int(pages)})
by_input = {x['input']:x for x in observations}
assert by_input['0,5']['line_width_draft_accepted'] is False
assert by_input['0.5']['line_width_draft_accepted'] is True
assert by_input['abc']['pdf_sample_page_step'] == 1
assert by_input['-3']['pdf_sample_page_step'] == 1
assert by_input['1.6']['pdf_sample_page_step'] == 2
assert by_input['3e1']['pdf_sample_page_step'] == 30

js = '''const cases = JSON.parse(process.argv[1]);
const safe = x => Number.isNaN(x) ? 'NaN' : Number.isFinite(x) ? x : String(x);
process.stdout.write(JSON.stringify({node:process.version, rows:cases.map(input=>({input,parseFloat:safe(parseFloat(input)),Number:safe(Number(input))})), formatting:['nl-NL','en-US'].map(locale=>({locale,value:1234.56,display:new Intl.NumberFormat(locale).format(1234.56)}))}));'''
(WORK/'ecmascript_probe.js').write_text(js)
js_result = json.loads(subprocess.run(['node', '-e', js, json.dumps(cases,ensure_ascii=False)],check=True,capture_output=True,text=True).stdout)
assert next(r for r in js_result['rows'] if r['input']=='0,5')['parseFloat'] == 0
assert next(r for r in js_result['rows'] if r['input']=='')['Number'] == 0
result = {
 'checked_at':'2026-10-22',
 'repo_snapshot':'befcbff7790e8c593b2ec47ae18d43115a4f530c',
 'method':'Exacte expressies uit twee native reviewroutes geïsoleerd gecompileerd. Daarnaast standaard ECMAScript-functies in Node uitgevoerd. Geen GUI, productieapp, daadwerkelijke invoerevents of bestandsexport getest.',
 'rustc':subprocess.run([rustc,'--version'],check=True,capture_output=True,text=True).stdout.strip(),
 'source_hashes':{p:hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in ['src/bin/style_repo.rs','src/bin/style_repo/pdf_split_native.rs']},
 'expressions':{'line_width_draft_acceptance':predicate,'pdf_sample_step':step},
 'review_expression_results':observations,
 'ecmascript':js_result,
 'limitations':['De PDF-splitsroute schrijft expliciet geen bestanden; de uitkomst betreft alleen de voorbeeldpreview.', 'De lijndiktepredicate bewijst acceptatie van een complete string, niet elk teken-, plak- of IME-event in de renderer.', 'Het ECMAScript-voorbeeld is een taalproef; er is hiermee geen parseFloat-gebruik of fout in een specifieke OpenAEC-productieapp aangetoond.'],
 'checks':'8 gerichte assertions geslaagd; geen oordeel over alle getalinvoer.'
}
(WORK/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(ROOT/'outputs/OpenAEC-UI-proeven.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'rust':observations,'js_sample':js_result['rows'][:8]},ensure_ascii=False))
