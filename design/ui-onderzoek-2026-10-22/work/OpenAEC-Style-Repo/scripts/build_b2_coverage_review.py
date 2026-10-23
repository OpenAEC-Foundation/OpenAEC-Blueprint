"""Build a source-record coverage report without treating name clusters as functions."""
from collections import Counter, defaultdict
from b2_source_catalog import supplemental_catalog
import json


def render_coverage(out, manifest, catalog, audit):
    assessments = {r['record_id']:r for r in audit['record_assessments']}
    rows = []
    apps = defaultdict(Counter)
    for record in catalog['records']:
        a=assessments[record['id']]
        status=a['assessment']
        apps[record['app']][status]+=1
        rows.append({'id':record['id'],'app':record['app'],
                     'label':record['label'] or record['name'],
                     'path':record['path'],'line':record['line'],
                     'commit':record['commit'],'url':record['source_url'],
                     'status':status,'reason':a['reason'],
                     'planned':status=='gepland ontwerp; bronbediening ontbreekt',
                     'canonical':', '.join(a.get('canonical_functions',[])) or a.get('canonical_function')})
    payload={'revision':manifest['revision'],'icons':manifest['function_count'],
             'masters':manifest['svg_count'],'apps':dict(apps),'records':rows,
             'assessed':sum(r['status']!='nog te beoordelen' for r in rows),
             'planned_sources':sum(r['planned'] for r in rows),
             'supplemental_records':len(supplemental_catalog()['records']),
             'unresolved_conflicts':sum(r['status']=='niet samenvoegen' for r in rows),
             'remaining':sum(r['status'] in {'nog te beoordelen','niet samenvoegen'} for r in rows),
             'limits':['Installer is aanvullend op 40 gepinde bronplaatsen beoordeeld (39 Installer, 1 ontbrekende Calc-bron); de oorspronkelijke inventaris blijft behouden.',
                       'Geplande ontwerpen hebben zichtbaar nog geen aangesloten bronbediening; ontwerpdekking is geen claim van werkende appfuncties.',
                       'FEM-bron was niet toegankelijk en blijft de expliciete dekkingsgrens uit de overdracht.',
                       'Dynamische symbolen, logo’s, illustraties en runtime-extensies worden niet stilzwijgend als vaste UI-iconen geteld.']}
    (out/'coverage.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'coverage-review.html').write_text(PAGE,encoding='utf-8')


PAGE='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>B2 · brondekking</title>
<style>body{margin:0;background:#26262d;color:#edebe8;font:15px/1.5 system-ui}main{max-width:1400px;margin:auto;padding:32px}a{color:#fbbf24}h1{font-size:32px}nav{display:flex;gap:24px}.stats{display:flex;flex-wrap:wrap;gap:16px;margin:24px 0}.stat{padding:20px;background:#33333c;border:1px solid #878689;border-radius:8px}.stat strong{font-size:26px;display:block}.controls{display:flex;gap:12px;position:sticky;top:0;background:#26262d;padding:16px 0}input,select{padding:10px;background:#33333c;color:#edebe8;border:1px solid #878689;border-radius:5px}input{min-width:260px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:12px;border-bottom:1px solid #555560;vertical-align:top}th{color:#fbbf24}small{color:#bebdbd}code{font-size:11px}li{margin:7px 0}.good{color:#86efac}.open{color:#fde047}</style>
<main><nav><a href="completion-review.html">Nieuwe ontwerpen</a><a href="index.html">Alle iconen</a><a href="coverage.json">Bronbesluiten (JSON)</a><a href="scope-review.html">Controle op ontbrekende ontwerpen</a></nav><h1>B2 · functies en brondekking</h1><p>Elke bronplaats krijgt een afzonderlijk besluit. De aantallen hieronder zijn geen telling van unieke iconen. De gepinde bronplaatsen binnen de afgesproken scope zijn afgehandeld. De afzonderlijke scopecontrole dekt ook zichtbare placeholders; nog niet aangesloten bediening blijft expliciet herkenbaar.</p><div id="stats" class="stats"></div><h2>Per app</h2><table><thead><tr><th>App</th><th>Bronplaatsen</th><th>Afgehandeld</th><th>Open</th><th>Status</th></tr></thead><tbody id="apps"></tbody></table><h2>Bronbesluiten</h2><div class="controls"><input id="search" placeholder="Zoek functie, pad of besluit"><select id="app"><option value="">Alle apps</option></select><select id="status"><option value="">Alle besluiten</option></select></div><table><thead><tr><th>Bron</th><th>Besluit</th><th>Motivering</th></tr></thead><tbody id="records"></tbody></table><h2>Dekkingsgrenzen</h2><ul id="limits"></ul></main>
<script>let data=null;const $=s=>document.querySelector(s),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function render(){const q=$('#search').value.toLowerCase(),app=$('#app').value,status=$('#status').value;const rs=data.records.filter(r=>(!app||r.app===app)&&(!status||r.status===status)&&JSON.stringify(r).toLowerCase().includes(q));$('#records').innerHTML=rs.map(r=>`<tr><td><strong>${esc(r.app)} · ${esc(r.label)}</strong><br><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.path)}:${r.line}</a><br><code>${esc(r.commit)}</code></td><td>${esc(r.status)}<br><code>${esc(r.canonical||'')}</code></td><td>${esc(r.reason)}</td></tr>`).join('')}
async function load(){const r=await fetch('coverage.json',{cache:'no-store'});if(!r.ok)return;const d=await r.json();if(data?.revision===d.revision)return;data=d;const app=$('#app').value,status=$('#status').value;$('#app').innerHTML='<option value="">Alle apps</option>'+Object.keys(d.apps).sort().map(a=>`<option>${esc(a)}</option>`).join('');$('#status').innerHTML='<option value="">Alle besluiten</option>'+[...new Set(d.records.map(r=>r.status))].sort().map(a=>`<option>${esc(a)}</option>`).join('');$('#app').value=app;$('#status').value=status;$('#stats').innerHTML=[[d.icons,'ontwerpen'],[d.masters,'SVG-masters'],[d.assessed,'beoordeelde bronplaatsen'],[d.remaining,'nog af te handelen'],[d.revision,'revisie']].map(([n,label])=>`<div class="stat"><strong>${n}</strong>${label}</div>`).join('');$('#apps').innerHTML=Object.entries(d.apps).sort().map(([app,counts])=>{const total=Object.values(counts).reduce((a,b)=>a+b,0),open=(counts['nog te beoordelen']||0)+(counts['niet samenvoegen']||0);return `<tr><td>${esc(app)}</td><td>${total}</td><td>${total-open}</td><td>${open}</td><td class="${open?'open':'good'}">${open?'In behandeling':'Catalogusbronplaatsen afgehandeld'}</td></tr>`}).join('');$('#limits').innerHTML=d.limits.map(l=>`<li>${esc(l)}</li>`).join('');render()}
for(const id of ['search','app','status'])$('#'+id).addEventListener(id==='search'?'input':'change',render);load();setInterval(load,15000);</script></html>'''
