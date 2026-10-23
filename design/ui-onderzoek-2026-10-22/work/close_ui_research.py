"""Finalize research artifacts; scheduler shutdown is a separate app tool action."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'work/ui-research';OUT=ROOT/'outputs'
now=datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(timespec='seconds')
sp=ROOT/'work/ui-research-state.json';state=json.loads(sp.read_text())
assert state['status']=='active', 'Finalization runs once'
assert datetime.fromisoformat(now) < datetime.fromisoformat(state['stop_at'])
heads=json.loads((W/'audits/upstream-heads-final.json').read_text())
diff=json.loads((W/'audits/pdf-final-targeted-diff.json').read_text())
assert diff['compared']==38 and diff['unchanged']==37 and diff['changed']==['open-pdf-studio/js/main.js']
sources=json.loads((W/'sources.json').read_text());assert 'R85' not in {s['id'] for s in sources}
sources.append(dict(id='R85',title='Afsluitcontrole PDF2026.43.7: hosted web bundle en bronversiegrens',url='https://github.com/OpenAEC-Foundation/open-pdf-studio/commit/1c57e8ee2f00665d7e90321b0030deec3c4ce4f5',type='Primaire repositorymetadata en gerichte Git-blobvergelijking',checked_at='2026-10-23',supports='Nieuwere HEAD bevat hosted-web-integratie. Volledige niet-afgekapte tree vergeleken op38 eerder gecachte paden:37 gelijk aan ronde8,main.js gewijzigd.',local_file='work/ui-research/audits/pdf-final-targeted-diff.json',limits='Geen volledige review van91 gewijzigde bestanden, nieuwe hoststorage-/iframe-integratie of nieuwste appbuild. Oude proeven behouden hun eigen commit.',commit='1c57e8ee2f00665d7e90321b0030deec3c4ce4f5'))
final=dict(checked_at=heads['checked_at'],heads=heads['heads'],pdf_targeted_comparison=diff,source_id='R85',limits=['37 gelijke bronblobs bewijzen geen complete gelijkheid van de app/hostintegratie.','Eerdere tests zijn niet als volledige nieuwe-HEAD-test herbenoemd.'])
version=json.loads((OUT/'OpenAEC-UI-versieaudit.json').read_text());version['final_check']=final
(OUT/'OpenAEC-UI-versieaudit.json').write_text(json.dumps(version,indent=2,ensure_ascii=False)+'\n')
state['upstream_version_audit']['final_check']=final
state['status']='desk_research_complete'
state['completed_at']=now;state['last_updated']=now
state['research_phase']='Nachtelijk bureauonderzoek en afsluitcontrole afgerond. Gezamenlijke ontwerpbesluiten en volledige taak-/platform-/gebruikersvalidatie blijven open.'
state['closure_reason']='Vijftien onderwerpen en gerichte bron-/versie-/component-/voorkeur-/tekstcontractaudits zijn uitgewerkt. Resterend werk vraagt gekozen scope/criteria en echte app-/platform-/gebruikersproeven; extra algemene bronnen zouden nu vooral herhaling zijn. Afsluiting vóór08:00 is toegestaan in de voortzettingsinstructie.'
state['automation_shutdown']='pending_app_tool'
state['completed_runs'].append(dict(date=now,modules=['13','14','15'],method='Eindredactie ochtendadvies, laatste upstream-HEAD-/blobcontrole, artifact-/bron-/fonthash-QA en afsluiting van nachtelijk bureauonderzoek.',findings_added=[],evidence=['outputs/OpenAEC-UI-versieaudit.json','outputs/OpenAEC-UI-ochtendoverzicht.html','outputs/OpenAEC-UI-taakproeven.html'],checks=['Laatste HEADs:Style/Calc/Validator gelijk; PDF nieuwe hosted-release.','PDF38 gericht vergeleken paden:37 gelijk,main.js gewijzigd; geen nieuwe appvalidatie.'],limitations=['Geen nieuwe native-/browser-/apparaat-/gebruikers-/printer-/crash-/offlineproef.','Ontwerpkeuzes en zes volledige taakproeven zijn voorstellen.'],qa='work/ui-research/report-qa-final.json'))
state['next_actions']=['Geen verdere automatische onderzoeksruns; tijdelijke automation beëindigen.','Volgende menselijke bespreking: scope/platformen, font/leesruimte en invoer/selectie/revisiecontract kiezen.','Daarna de gekozen voorgestelde taakproeven in echte apps uitvoeren met bronbaseline en vooraf afgesproken criteria.']
(W/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n');sp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
module=W/'modules/15.html'
module.write_text(module.read_text()+'''\n<h3>Afsluitcontrole23oktober: nieuwe PDF-hostversie apart begrensd</h3><p>Bij de afsluitcontrole om06:53 Amsterdam staan Style,Calc en BIM-validator nog op de eerder vastgelegde HEADs. PDF staat op<code>1c57e8e</code>, een nieuwe hosted-web-integratie na de onderzochte<code>e9f599f</code>. Van38 gecachte relevante bronpaden zijn37 blobs gelijk aan ronde8; alleen<code>main.js</code> is gewijzigd. De getal-/zoek-/geometriehelpers blijven bronmatig hetzelfde binnen die vergelijking. Dat is geen volledige app- of hoststorage-/iframevalidatie. Alle proefresultaten blijven gekoppeld aan hun oorspronkelijke commit. <a href="#source-R85">Versiebron</a>, <a href="OpenAEC-UI-versieaudit.json">audit met exacte paden</a>.</p><p>Het nachtelijke bureauonderzoek is afgesloten. Verdere algemene bronverzameling levert nu minder op dan het samen kiezen van scope/criteria en het uitvoeren van de voorgestelde echte taakproeven. De15 onderwerpen zijn inhoudelijk behandeld; platformconformiteit, volledige apppariteit en gebruikersresultaten zijn hiermee niet afgerond.</p>\n''')
print(json.dumps(dict(status=state['status'],completed_at=now,sources=len(sources))))
