import {parseNumericInput} from './numericInput.ts';
import {formatNumberForEdit,parseNlNumber} from './formatting.ts';
const safe=x=>typeof x==='number'&&!Number.isFinite(x)?String(x):x;
const cases=JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify({node:process.version,rows:cases.map(input=>({input,nl:safe(parseNlNumber(input)),numeric:safe(parseNumericInput(input))})),roundtrip:[6.66,60.5,1988.25,17.7,103.4,0.001,12345.67,42,0].map(value=>({value,editor:formatNumberForEdit(value),parsed:safe(parseNumericInput(formatNumberForEdit(value)))}))}));