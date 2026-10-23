"""Run pinned Calc parser functions, preserving originals outside the repo."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'work/ui-research/upstream/calc-b470427'
PROBE = ROOT/'work/ui-research/probes/calc'
PROBE.mkdir(exist_ok=True)
for name in ['formatting.ts','numericInput.ts']:
    original = (SOURCE/'src/utils'/name).read_text()
    prepared = original.replace("from './formatting'", "from './formatting.ts'")
    (PROBE/name).write_text(prepared)
(PROBE/'package.json').write_text('{"type":"module"}\n')
cases = ['6,66','6.66','1.234','1.234,56','1 234,56','1\u00a0234,56','12abc','1,2,3','abc12','0','','Infinity','NaN','=1.234','=1,2,3','=2/0','=12,2*2,22','-15,5','0.001','=0.001']
script = '''import {parseNumericInput} from './numericInput.ts';
import {formatNumberForEdit,parseNlNumber} from './formatting.ts';
const safe=x=>typeof x==='number'&&!Number.isFinite(x)?String(x):x;
const cases=JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify({node:process.version,rows:cases.map(input=>({input,nl:safe(parseNlNumber(input)),numeric:safe(parseNumericInput(input))})),roundtrip:[6.66,60.5,1988.25,17.7,103.4,0.001,12345.67,42,0].map(value=>({value,editor:formatNumberForEdit(value),parsed:safe(parseNumericInput(formatNumberForEdit(value)))}))}));'''
(PROBE/'run.mjs').write_text(script)
node='/home/aia08/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
results=json.loads(subprocess.run([node,str(PROBE/'run.mjs'),json.dumps(cases,ensure_ascii=False)],check=True,capture_output=True,text=True).stdout)
rows={r['input']:r for r in results['rows']}
assert rows['6,66']['numeric']==6.66
assert rows['6.66']['numeric']==6.66
assert rows['12abc']['numeric']==12
assert rows['1 234,56']['numeric']==1
assert rows['1,2,3']['numeric']==1.2
assert rows['=1,2,3']['numeric'] is None
assert rows['1.234']['numeric']==1234
assert rows['=1.234']['numeric']==1.234
assert rows['Infinity']['numeric']=='Infinity'
assert rows['=2/0']['numeric'] is None
assert all(r['value']==r['parsed'] for r in results['roundtrip'] if r['value']!=0)
assert results['roundtrip'][-1]['parsed'] is None
results.update({
 'repo':'OpenAEC-Foundation/open-calc-studio',
 'commit':'b47042704efa388d95eb59ce77d23aeb5ee0e44c',
 'method':'Gepinde parserbestanden uitgevoerd met Node type stripping. Alleen de relatieve import kreeg .ts als extensie. Geen React-component, UI-event, storemutatie of productie-installatie uitgevoerd.',
 'source_hashes':{f:hashlib.sha256((SOURCE/'src/utils'/f).read_bytes()).hexdigest() for f in ['formatting.ts','numericInput.ts']},
 'checks':'12 gerichte assertions geslaagd; acht niet-nul round-tripvoorbeelden behouden hun waarde.',
 'limits':['Uitkomsten zijn parserresultaten, geen aangetoonde gevolgen voor opgeslagen begrotingen.','Bestaande tests zijn gelezen, niet als volledige Vitest-suite uitgevoerd.','Gedrag op huidige upstream-HEAD of een geïnstalleerde versie is niet vastgesteld.','Nul leeg formatteren is expliciet bestaande keuze in broncode/tests; beoordeling van de zichtbare betekenis blijft een ontwerpvoorstel.']
})
(PROBE/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
target=ROOT/'outputs/OpenAEC-UI-proeven.json'
all_results=json.loads(target.read_text())
all_results['calc_parser']=results
target.write_text(json.dumps(all_results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(results,ensure_ascii=False))
