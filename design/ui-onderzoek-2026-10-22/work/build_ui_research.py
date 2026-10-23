"""Build the locally readable UI research supplement from durable research data."""
from pathlib import Path
import html
import json
import re
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'work/ui-research'
OUT = ROOT / 'outputs'
state = json.loads((ROOT / 'work/ui-research-state.json').read_text())
sources = json.loads((WORK / 'sources.json').read_text())
findings = json.loads((WORK / 'findings.json').read_text())
esc = lambda s: html.escape(str(s))
now = datetime.now(ZoneInfo('Europe/Amsterdam')).strftime('%d-%m-%Y %H:%M')
closed = state.get('status') == 'desk_research_complete'
labels = {'pending':'Nog te onderzoeken','in_progress':'In onderzoek','researched':'Bureauonderzoek uitgewerkt; validatie open','reviewed':'Bronnen en tegenspraak gecontroleerd'}
index = ''.join(f'<li><a href="#module-{m["id"]}">{esc(m["title"])}</a> <span class="meta">— {esc(labels.get(m["status"],m["status"]))}</span></li>' for m in state['modules'])
rows = ''.join('<tr><td><a href="#module-'+esc(f['module'])+'">'+esc(f['id'])+'</a></td><td>'+esc(f['priority'])+'</td><td><strong>'+esc(f['title'])+'</strong><br>'+esc(f['claim'])+'</td><td>'+esc(f['evidence_status'])+'</td></tr>' for f in findings)
modules = []
for module in state['modules']:
    fragment = WORK / 'modules' / (module['id']+'.html')
    if fragment.exists():
        body = fragment.read_text()
    else:
        body = '<p>Deze module staat op de onderzoeksagenda. Er is nog geen afgeronde conclusie. De voortzetting pakt eerst de onderwerpen met de grootste gevolgen voor harmonisatie en dagelijks gebruik op.</p>'
    modules.append('<section id="module-'+module['id']+'"><div class="eyebrow">Module '+module['id']+' · '+esc(labels.get(module['status'],module['status']))+'</div><h2>'+esc(module['title'])+'</h2>'+body+'</section>')
source_list = ''.join('<li id="source-'+esc(s['id'])+'"><a href="'+esc(s['url'])+'">'+esc(s['id']+' · '+s['title'])+'</a><div class="meta">'+esc(s['type'])+' · geraadpleegd '+esc(s['checked_at'])+'</div><p>'+esc(s['supports'])+'</p><p class="meta">Beperking: '+esc(s['limits'])+'</p></li>' for s in sources)
css = '''*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#f1eeea;color:#2a2a32;font:17px/1.65 system-ui,sans-serif}header,main,footer{max-width:1100px;margin:auto;padding:38px 42px}header{background:#2a2a32;color:#edebe8}header a{color:#fbbf24}h1{font-size:clamp(2rem,4vw,3.2rem);line-height:1.15;max-width:24ch}h2{font-size:1.7rem;line-height:1.3}h3{font-size:1.2rem;margin-top:30px}section{background:white;border-radius:10px;padding:32px;margin:24px 0;scroll-margin-top:20px}p,li{max-width:83ch}a{color:#92400e;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #b45309;outline-offset:3px}.meta{font-size:.87rem;color:#5f5f65}.eyebrow{font-size:.8rem;text-transform:uppercase;letter-spacing:.07em}.notice{border-left:4px solid #b45309;padding:12px 18px;background:#fbf1e6}li{margin:9px 0}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:.91rem}td,th{padding:12px 9px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd9d3}th{background:#f7f5f2}code{background:#f5f5f4;font-size:.9em;padding:2px 4px;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#f5f5f4;padding:16px;overflow-wrap:anywhere}.source-list li{margin:24px 0}.source-list p{margin:6px 0}summary{cursor:pointer;font-weight:600}.coverage li{padding:3px 0}.priority{font-weight:600}@media(max-width:680px){header,main,footer{padding:24px 16px}section{padding:22px 16px}table{font-size:.85rem}}@media print{body{background:white;font-size:10.5pt}header{background:white;color:#2a2a32}header,main,footer{padding:0}section{border-radius:0;padding:12px 0;margin:0}h2,h3{break-after:avoid}tr{break-inside:avoid}a{color:inherit}nav{display:none}.meta{font-size:9pt}}'''
doc = '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC — verdiepend UI-onderzoek</title><style>'+css+'</style></head><body><header><div class="eyebrow">Onderzoek in uitvoering · '+esc(now)+' · Europe/Amsterdam</div><h1>Hoe de OpenAEC-interface moet werken</h1><p>Verdieping van het typografie- en vormonderzoek naar dagelijks gebruik, invoer, herstel, prestaties, toegankelijkheid en de technische harmonisatie.</p><p><a href="OpenAEC-ontwerponderzoek.html">Open het oorspronkelijke onderzoek naar typografie en vorm</a></p></header><main>'
doc += '<section><h2>Leeswijzer en onderzoeksstatus</h2><p>De gebruiker heeft op 22 oktober gevraagd om gedurende de nacht verder te onderzoeken wat UI-technisch belangrijk en relevant is. Dit document groeit per onderzoeksronde. Het doet geen uitspraken dat ongeteste apps al aan alle eisen voldoen of dat alle onderdelen al volledig onderzocht zijn.</p><p class="notice"><strong>Vroeg te bewijzen:</strong> een volledige toetsenbord-/hulptechnologieroute en betrouwbare interpretatie van technische invoer. De gepinde Calc-proeven laten gedeeltelijk gelezen getallen en controlepunten rond opslagrevisies en meerdere tabbladen zien. De end-to-end gevolgen zijn nog te toetsen.</p><p>De eerdere identiteit, B2-iconen en vastgelegde 0.4-afspraken blijven het vertrekpunt. Voorstellen om ze te herzien worden als voorstel behandeld. Er is geen productiecode gewijzigd.</p><p><a href="OpenAEC-UI-ochtendoverzicht.html">Open het groeiende ochtendoverzicht</a> · <a href="OpenAEC-UI-dekkingsmatrix.json">Dekkingsmatrix als JSON</a></p><nav aria-label="Onderzoeksmodules"><ol class="coverage">'+index+'</ol><p><a href="#findings">Bevindingen en voorgestelde prioriteiten</a> · <a href="#sources">Bronregister</a></p></nav></section>'
doc += '<section id="findings"><h2>Bevindingen en voorgestelde prioriteiten</h2><p>P0 betekent hier: eerst een haalbaarheids- of databetrouwbaarheidsproef uitvoeren omdat een probleem brede harmonisatie kan blokkeren. Het is geen automatische claim van een productie-incident. P1 is belangrijk voor de eerste gedeelde componenten; P2 kan volgen wanneer de basis werkt. Prioriteiten blijven voorstellen.</p><div class="table-wrap"><table><thead><tr><th>ID</th><th>Prioriteit</th><th>Bevinding</th><th>Bewijskracht</th></tr></thead><tbody>'+rows+'</tbody></table></div><p><a href="OpenAEC-UI-bevindingen.json">Download het volledige bevindingregister</a> · <a href="OpenAEC-UI-bronnen.json">Download het bronregister</a> · <a href="OpenAEC-UI-proeven.json">Uitgevoerde geïsoleerde proeven</a></p></section>'
if state.get('upstream_version_audit'):
    doc += '<section id="versieaudit"><h2>Actuele bronversies en correcties</h2><p>De versieaudit van 23 oktober onderscheidt eerdere snapshots van nieuwere broncode. Style HEAD 85a6aaf bevat al een echte 0.4-module, JSON→Rust/CSS-generator en B2-bibliotheek. De0.4-afleidingscheck slaagt. PDF HEAD e9f599f heeft aparte strikte/prefix-getalhelpers; 18 bestaande pure getal-/fouttests slagen. Calc en BIM-validator staan bij controle op de eerder onderzochte commits.</p><p>Oudere proeven blijven aan hun oorspronkelijke commit gekoppeld. De gerichte blobvergelijking is geen volledige audit van alle nieuwe bestanden. <a href="#module-13">Gecorrigeerde implementatieanalyse</a> · <a href="#module-15">Beoordeling per snapshot</a> · <a href="OpenAEC-UI-versieaudit.json">Machineleesbare versieaudit</a>.</p></section>'
doc += ''.join(modules)
doc += '<section id="sources"><h2>Bronregister</h2><p>Normatieve eisen, informatieve patronen, leveranciersdocumentatie, broncode en forumervaringen zijn apart herkenbaar. Een forumervaring is geen representatief onderzoek. Broncode-inspectie vervangt geen proef met hulptechnologie of echte gebruikers.</p><ol class="source-list">'+source_list+'</ol></section></main><footer><p>Lokale onderzoeksversie. Laatst samengesteld '+esc(now)+'. Gepland vervolg tot 23 oktober 2026 08:00 Europe/Amsterdam. De onderzoeksvragen en dekkingsstatus blijven expliciet zichtbaar.</p></footer></body></html>'
path = OUT / 'OpenAEC-UI-verdiepingsonderzoek.html'
if closed:
    doc = doc.replace('Onderzoek in uitvoering', 'Bureauonderzoek afgerond')
    doc = doc.replace('Dit document groeit per onderzoeksronde.', 'Deze lokale eindversie bundelt het nachtelijke bureauonderzoek; echte taak-/platformvalidatie blijft open.')
    doc = doc.replace('Open het groeiende ochtendoverzicht', 'Open het ochtendadvies en gezamenlijke plan')
    doc = doc.replace('Gepland vervolg tot 23 oktober 2026 08:00 Europe/Amsterdam.', 'Nachtelijk bureauonderzoek afgesloten vóór de afgesproken grens van 23 oktober 2026 08:00 Europe/Amsterdam.')
    final_check = state.get('upstream_version_audit',{}).get('final_check',{})
    if final_check:
        note='<p class="notice"><strong>Afsluitcontrole:</strong> PDF HEAD is intussen <code>1c57e8e</code> (hosted web bundle). Van 38 eerder gecachte relevante bronpaden zijn 37 gelijk aan de ronde 8-HEAD; <code>main.js</code> is gewijzigd. De nieuwe hostintegratie is niet gevalideerd. Eerdere proeven blijven op hun originele commit staan. <a href="#source-R85">Versiebron</a> · <a href="OpenAEC-UI-versieaudit.json">volledige afgrenzing</a>.</p>'
        doc=doc.replace('<section id="versieaudit"><h2>Actuele bronversies en correcties</h2>','<section id="versieaudit"><h2>Actuele bronversies en correcties</h2>'+note,1)
tmp = path.with_suffix('.tmp')
tmp.write_text(doc)
tmp.replace(path)
shutil.copyfile(WORK/'findings.json',OUT/'OpenAEC-UI-bevindingen.json')
shutil.copyfile(WORK/'sources.json',OUT/'OpenAEC-UI-bronnen.json')
coverage = {'updated_at':now,'timezone':'Europe/Amsterdam','stop_at':state['stop_at'],'scope':'Onderzoeksdekking, geen productconformiteit of percentage gereedheid. Bureauonderzoek is geen runtime-/gebruikerstoets.','repo_snapshot':state['repo_snapshot'],'upstream_version_audit':state.get('upstream_version_audit'),'modules':state['modules'],'completed_runs':state['completed_runs']}
coverage.update(status=state.get('status'),completed_at=state.get('completed_at'),automation_shutdown=state.get('automation_shutdown'))
(OUT/'OpenAEC-UI-dekkingsmatrix.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
covered = sum(m['status'] in ('researched','reviewed') for m in state['modules'])
p0 = [f for f in findings if f['priority']=='P0']
critical = ''.join('<li><strong>'+esc(f['id']+' · '+f['title'])+'</strong><p>'+esc(f['claim'])+'</p><p>Voorstel: '+esc(f['recommendation'])+' <a href="OpenAEC-UI-verdiepingsonderzoek.html#module-'+esc(f['module'])+'">Bronnen, context en beperkingen</a>.</p></li>' for f in p0)
coverage_rows = ''.join('<tr><td><a href="OpenAEC-UI-verdiepingsonderzoek.html#module-'+m['id']+'">'+esc(m['id']+' · '+m['title'])+'</a></td><td>'+esc(labels.get(m['status'],m['status']))+'</td></tr>' for m in state['modules'])
intro_path = WORK/'morning-intro.html'
intro = intro_path.read_text() if intro_path.exists() else '<section><h2>Voorlopige balans</h2><p>Lees de nieuwe bevindingen en de expliciete dekkingsstatus hieronder.</p></section>'
morning = '<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC — ochtendoverzicht UI-onderzoek</title><style>'+css+'</style></head><body><header><div class="eyebrow">Groeiend overlegdocument · '+esc(now)+' · Europe/Amsterdam</div><h1>OpenAEC: de keuzes voor harmonisatie</h1><p>Voorbereiding voor de gezamenlijke bespreking. Onderzoek loopt uiterlijk tot 23 oktober 2026 om 08:00.</p><p><a href="OpenAEC-UI-verdiepingsonderzoek.html">Volledige UI-verdieping</a> · <a href="OpenAEC-ontwerponderzoek.html">Typografie en vorm</a></p></header><main>'
morning += '<section><h2>Eerlijke tussenstand</h2><p>'+str(covered)+' van '+str(len(state['modules']))+' modules hebben nu uitgewerkt bureauonderzoek. Dit is een dekkingsaanduiding, geen kwaliteitspercentage. Het bronregister bevat '+str(len(sources))+' bronnen en bronplaatsen; '+str(len(findings))+' bevindingen zijn vastgelegd. Voorstellen zijn niet goedgekeurd en apps zijn niet volledig doorgetest.</p><p><a href="OpenAEC-UI-proeven.json">De daadwerkelijk uitgevoerde proeven</a> zijn begrensde parser-, taal-, controlflow- en bestaande pure rotatie-unitproeven, geen gebruikers- of end-to-endtests.</p></section>'
morning += intro + '<section><h2>Voorgestelde P0-controlepunten</h2><p>Deze punten eerst toetsen vóór brede uitrol. De prioriteit zegt niets over een vastgesteld productie-incident.</p><ol>'+critical+'</ol></section>'
morning += '<section><h2>Dekking en resterend onderzoek</h2><div class="table-wrap"><table><thead><tr><th>Onderwerp</th><th>Status</th></tr></thead><tbody>'+coverage_rows+'</tbody></table></div><p>Bij uitgewerkt bureauonderzoek blijven platformproeven, taakvalidatie en terugkoppeling van echte gebruikers open, tenzij uitdrukkelijk anders vermeld.</p></section></main><footer><p>Lokale versie, samengesteld '+esc(now)+'. Geen productiecode, goedgekeurde besluiten of GitHub-issues gewijzigd; geen commit/push.</p></footer></body></html>'
morning_path = OUT/'OpenAEC-UI-ochtendoverzicht.html'
if closed:
    morning=morning.replace('Groeiend overlegdocument','Ochtendadvies na het nachtelijke onderzoek')
    morning=morning.replace('Onderzoek loopt uiterlijk tot 23 oktober 2026 om 08:00.','Het bureauonderzoek is afgesloten. De voorgestelde taak-/platformproeven en ontwerpkeuzes bespreken we samen.')
    morning=morning.replace('Eerlijke tussenstand','Onderzoeksstatus bij afsluiting')
    morning=morning.replace('Dekking en resterend onderzoek','Dekking en resterende validatie')
morning_tmp = morning_path.with_suffix('.tmp')
morning_tmp.write_text(morning)
morning_tmp.replace(morning_path)
base = OUT/'OpenAEC-ontwerponderzoek.html'
original = base.read_text()
if 'id="ui-vervolgonderzoek"' not in original:
    original = original.replace('<main>', '<main><section id="ui-vervolgonderzoek"><h2>Verdiepend UI-onderzoek</h2><p>Het onderzoek is op verzoek uitgebreid naar gedrag, toegankelijkheid, navigatie, herstel, prestaties en harmonisatie. <a href="OpenAEC-UI-verdiepingsonderzoek.html">Open het actuele verdiepingsonderzoek en de dekkingsmatrix</a>.</p></section>', 1)
    base.write_text(original)
print(json.dumps({'report':str(path),'modules_with_content':sum((WORK/'modules'/(m['id']+'.html')).exists() for m in state['modules']),'sources':len(sources),'findings':len(findings),'bytes':path.stat().st_size},ensure_ascii=False))
