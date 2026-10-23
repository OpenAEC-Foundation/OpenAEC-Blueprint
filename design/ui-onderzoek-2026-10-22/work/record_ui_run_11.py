"""Last bounded content addition: technical labels, tooltips and copy meaning."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'work/ui-research'
OUT=ROOT/'outputs'
now=datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(timespec='seconds')
sources=json.loads((W/'sources.json').read_text());findings=json.loads((W/'findings.json').read_text())
assert 'A120' not in {s['id'] for s in sources}, 'Run once only'
sources.append(dict(id='A120',title='WCAG1.4.13 Content on Hover or Focus, niveauAA',url='https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html',type='Primaire informatieve WCAG-uitleg',checked_at='2026-10-23',supports='Auteursgestuurde aanvullende hover-/focusinhoud: onder toepasselijke voorwaarden dismissible, hoverable en persistent; eigen uitzonderingen expliciet.',limits='Webcriterium met uitzonderingen, waaronder ongewijzigde browsertooltip. Geen uitvoerbare OpenAEC-browser-/nativeproef en geen algemene eis iedere tooltip een dialoog te maken.'))
for s in sources:
    if s['id'] in ['A71','A75','A80']:s['checked_at']='2026-10-23'
byid={f['id']:f for f in findings}
byid['UI-005']['claim']='Oudere shell schat tab-/lintbreedte met tekentelling; nieuwere0.4-tabs bouwen hun titel met tekstlayout. Font-/taalwijziging blijft per route te toetsen.'
byid['UI-005']['source_ids']+=['R71','R78']
byid['UI-005']['limits']+=' Positief tegenvoorbeeld in nieuwe0.4: document_tabs geeft tab.title direct aan tekstlayout, geen vaste tekentelfactor in die functie. Geen clipping of afgekapt Unicodecluster gereproduceerd.'
byid['UI-035']['source_ids'] += ['A120','R84']
byid['UI-035']['limits'] += ' Aanvullende voorgestelde lange-/gemengde-tekstfixtures zijn geen gemeten rendererdefect.'
findings.append(dict(id='UI-058',module='11',title='Maak tooltip en volledige tekst ook zonder hover bruikbaar',claim='Web0.4-tooltip verschijnt op hover én focus-visible, met white-space:pre en pointer-events:none. Leesbaarheid, sluiten en bereikbaarheid bij vergroting blijven te toetsen.',priority='P1',evidence_status='Gepinde CSS-/widgetbron en primaire patroonvereisten; runtime open',source_ids=['R84','R71','A120','A75','A80'],recommendation='Gebruik tooltips voor aanvullende uitleg; borg naam/volledige waarde via passende blijvende of opvraagbare route en test hover/focus/Escape/vergroting.',validation=['Beweeg pointer naar extra inhoud en toets dismiss/persistentie waar van toepassing.','Lees lange waarde zonder hover op keyboard/touch; kopieer de volledige bedoelde waarde.','Controleer vensterrand,200%schaal,tekstspacing en bijna gelijke bestandsnamen.'],limits='Geen browser-/native tooltip uitgevoerd en geen automatische WCAG-overtreding vastgesteld; uitzonderingen en eventuele hostlogica moeten per gebruik worden beoordeeld. CSSfocus-trigger is positief bestaand gedrag.',code_locations=['web/openaec-components.css:[data-oa-tip]','design/widgets.rs:with_tooltip/document_tabs'],status='proposal'))
(W/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n');(W/'findings.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False)+'\n')

p=OUT/'OpenAEC-UI-taakproeven.json';plan=json.loads(p.read_text())
tp=next(t for t in plan['fixtures'] if t['id']=='TP-06')
tp['text_fixture_examples']=[
  'Project Zeekade – constructief model – fase02 – revisie03.ifc',
  'Project Zeekade – constructief model – fase02 – revisie04.ifc',
  'ProjectA/Constructie/model.ifc en ProjectB/Installatie/model.ifc',
  'Café – Cafe\u0301 – kolom A\u0301 – doorsnede ⌀20',
  'مرحلة02 – gevel-A03.ifc',
  '−0,001 kN/mm² · 12\u202f345,67 m²',
  'Bestand niet opgeslagen: Project Zeekade/Constructie/revisie03/model.ifc — schrijven geweigerd.'
]
tp['actions'].append('Vergelijk bijna gelijke namen/revisies en gelijke basenames in verschillende projecten; vraag volledige tekst op en kopieer de afgesproken waarde.')
tp['expected'].append('Een eventuele verkorting bewaart onderscheidende informatie; volledige waarde blijft zonder hover beschikbaar. Visuele afbreking/ellipsis verandert de gekopieerde identifier niet stil.')
tp['source_ids'] += ['A71','A75','A80','A120','R71']
tp['finding_ids'] += ['UI-005','UI-035','UI-058']
plan['updated_at']=now
p.write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')

sp=ROOT/'work/ui-research-state.json';state=json.loads(sp.read_text());state['last_updated']=now
state['completed_runs'].append(dict(date=now,modules=['02','09','11','12','14','15'],method='Gerichte tekstlayout-/tooltip-/Unicodecontractaudit met primaire documentatie; bestaande0.4-natuurlijke tekstlayout als tegenvoorbeeld; bestaande taakfixture uitgebreid.',findings_added=['UI-058'],findings_corrected=['UI-005','UI-035'],evidence=['outputs/OpenAEC-UI-taakproeven.json','outputs/OpenAEC-UI-taakproeven.html'],checks=['Geen nieuwe uitgevoerde runtimeproeven. Bron- en artifactcontrole uitgevoerd.'],limitations=['Geen clipping, tooltipfout, Unicodecorruptie of volledige platformconformiteit geclaimd.','Voorgestelde lange-/gemengde-tekstcases niet in een echte app uitgevoerd.'],qa='work/ui-research/report-qa-run11.json'))
for m in state['modules']:
    if m['id'] in ['02','09','11','12','14','15']:m.update(last_updated=now,validation_open=True)
state['research_phase']='Inhoudelijke bureaudekking en gerichte versie-/component-/voorkeur-/tekstcontractaudits afgerond; eindredactie en afsluitcontrole volgen. Native/web/gebruikerstoetsen blijven open.'
state['next_actions']=['Laatste ronde: eindredactie van ochtendadvies en leesroute; controleer prioriteiten/besluiten/voorstellen en bronversiegrenzen.','Controleer verse upstreamHEAD alleen voor materiaal dat als actueel wordt samengevat; neem geen nieuwe uitgebreide scope op.','Bouw/valideer alle lokale deliverables, controleer repo ongewijzigd en sluit tijdelijke automation af zodra resterend werk alleen herhaling is.','Uiterlijk08:00Europe/Amsterdam stoppen. Latere run alleen automation beëindigen, geen nieuw onderzoek.']
sp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(sources=len(sources),findings=len(findings),proposed_fixtures=len(plan['fixtures']),new_executed_tests=0)))
