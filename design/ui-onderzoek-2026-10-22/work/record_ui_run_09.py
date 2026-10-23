"""Bounded source audit of actual 0.4 components, review host and web package."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'work/ui-research'
OUT=ROOT/'outputs'
now=datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(timespec='seconds')
sha='85a6aafc7d003ec8f61c9543b352a1f1b0f47346'
iced='9bfbd7cda79aceef2d115b8bb35e8f3257dcabf2'
sources=json.loads((W/'sources.json').read_text())
findings=json.loads((W/'findings.json').read_text())
assert 'R78' not in {s['id'] for s in sources}, 'Run once only'
def src(id,title,url,type,supports,limits,**extra):
    sources.append(dict(id=id,title=title,url=url,type=type,checked_at='2026-10-23',supports=supports,limits=limits,**extra))
for id,title,path,supports,limits in [
('R78','0.4-reviewhost: echte berichten, expliciet een reviewhulpmiddel','src/bin/ui04.rs','Escape/Enter, commandosneltoetsen, undo/rijbewerking en ID-mapping bestaan. De kop noemt de gallery expliciet een reviewhulp; Save/Export/Print-berichten zijn hier geen productie-I/O-bewijs.','Geen executable uitgevoerd; subscription en update statisch gelezen. Niet extrapoleren naar oorspronkelijke Calc of alle afnemers.'),
('R79','Webpakket: CSS, attributen en appverantwoordelijkheid','web/README.md','Bestaande token-/component-CSS en verwachte toestandattributen; apps laden zelf fonts. Klassen en attributen definiëren op zichzelf geen hele interactieroute.','Geen webapp gemigreerd of browser-/screenreaderproef; documentatiebelofte onderscheiden van semantische uitvoering.'),
('R80','0.4-chrome: menu, splitter en hostberichten','crates/openaec-ui/src/design/chrome.rs','Splitter geeft startbericht; host volgt cursor. Menu heeft plaatsingshelper en dismiss-berichten. Geen compleet toetsenbord-/overflowcontract in deze helper.','Broninspectie, geen aangetoonde clipping, foutieve platformactie of algehele ontbrekende keyboardbediening.'),
('R81','Actuele besloten0.4-componentafspraken','design/ontwerp-0.4/04-componenten.md','Visuele geometrie/tabelafspraken; Escape sluit en Enter kiest primaire dialoogknop. Basis blijft vertrekpunt voor aanvullend gedragscontract.','Geen nieuw besluit of wijziging; bron beschrijft geen volledig raster-/focus-/modalitycontract.'),
('R82','Webcomponentgallery als voorbeeld, niet appconformiteit','web/componenten.html','Dialogvoorbeeld is div met role/label. Laatste script wisselt alleen thema; geen showModal-route in dit bestand. Voorbeeld is visuele catalogus.','Geen volledige productieappaudit; geen conclusie dat alle webapps dezelfde voorbeeldmarkup gebruiken.')]:
    src(id,title,f'https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/blob/{sha}/{path}','Gepinde actuele OpenAEC-bron/besluitbron',supports,limits,local_file='work/ui-research/upstream/style-85a6aaf/'+path,commit=sha)
src('R83','iced0.13.1 on_key_press: alleen genegeerde events','https://github.com/iced-rs/iced/blob/'+iced+'/futures/src/keyboard.rs','Gepinde primaire frameworkbron','Callback ontvangt KeyPressed wanneer widgetstatus Ignored is; Captured levert geen bericht via deze route.','Geen volledige eventpropagatie-/IME-/OS-proef; aanwezigheid van globale mapping betekent niet dat elke toets altijd doorlekt.',local_file='work/ui-research/upstream/iced-0.13.1/futures/src/keyboard.rs',commit=iced)
src('A112','W3C APG Window Splitter: voorstel met eigen reviewvoorbehoud','https://www.w3.org/WAI/ARIA/apg/patterns/windowsplitter/','Primaire informatieve patroonbeschrijving','Pijltjes, grens-/herstelbediening en naam/waarde als aanknopingspunt voor paneelcontract.','Pagina meldt expliciet onvoltooide taskforcereview/voorbeeld; geen afgeronde norm, nativeplatformcertificering of verplicht toetsenrecept.')
src('A113','WHATWG HTML: dialog en modale lifecycle','https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element','Primaire HTML Living Standard','show/showModal, beginfocus en modaliteit hebben browseralgoritmen; een CSS-klasse of role-attribuut voert die algoritmen niet zelfstandig uit.','Webstandaard, geen iced-implementatie of automatisch bewijs voor appcommando’s en ondersteunde WebViews.')

byid={f['id']:f for f in findings}
for id in ['UI-002','UI-004','UI-008','UI-009','UI-038','UI-050']:
    byid[id]['source_ids'] += [s for s in {'UI-002':['R78','R83'],'UI-004':['R78'],'UI-008':['R71','R78'],'UI-009':['R71','R78','R81'],'UI-038':['R80','R78','A112'],'UI-050':['R79','R82','A113']}[id] if s not in byid[id]['source_ids']]
byid['UI-002']['limits'] += ' Actuele ui04-review heeft expliciete commandobindings en Escape/Enter; ontbreken van algemene focusroute is geen ontbreken van alle sneltoetsen.'
byid['UI-004']['limits'] += ' Positief tegenvoorbeeld: actuele ui04-host bindt onder meer bewaren, undo en panelen afzonderlijk.'
byid['UI-008']['claim']='Oudere native Calc-review en nieuwe0.4-tabelhelper bewijzen geen volledige bronrasterport; nieuwe ui04-host heeft wel rijacties, undo en stabiele ID-mapping.'
byid['UI-008']['limits'] += ' Nieuwe0.4-gallery is expliciet reviewhulp, geen volledige Calc-app. Geen bestaande functionaliteit als afwezig bestempelen alleen omdat zij buiten de helper zit.'
byid['UI-009']['limits'] += ' Nieuwe tabelhelper gebruikt één geselecteerde rijpositie; ui04-host vertaalt correct tussen positie en domein-ID. Geen bewezen ID-verwisselingsbug.'
findings.append(dict(id='UI-056',module='01',title='Leg modale opdrachtcontext naast de dialoogkaart vast',claim='Nieuwe0.4-dialoogkaart/overlay tekenen de context; ui04-host levert Escape/Enter en klikopvang. Volledige focus-/achtergrondopdrachtisolatie is niet aangetoond.',priority='P1',evidence_status='Actuele gepinde broninspectie met positieve tegenvoorbeelden; runtime open',source_ids=['R71','R78','R83','R81','A06','A113'],recommendation='Leg beginfocus, focusherstel, toetsvoorrang en toegestane opdrachten per modale toestand vast; test dit in de native host en webhost.',validation=['Open een gewijzigde-documentdialoog: Tab/Shift-Tab, Escape, Enter en logische terugkeerfocus.','Probeer Delete/Cmd+N/Cmd+Z en paneel-/documentopdrachten vanuit dialoog, tekstveld en menu; controleer dat alleen bedoelde context verandert.','Test gestapelde overlays, foutmelding, weggehaalde opener en schaal/scroll.'],limits='Geen native app gestart en geen doorgelekte toets of dataverlies gereproduceerd. iced on_key_press ontvangt alleen Ignored events; helpers/hosts en platformgedrag moeten samen worden getest. Prioriteit blijft voorstel.',code_locations=['design/widgets.rs:dialog/overlay','src/bin/ui04.rs:subscription/update/view','iced futures/src/keyboard.rs:on_key_press'],status='proposal'))

contracts=[
dict(component='Knoppen en opdrachten',provided='on_press/disabled/selected en styling; host-demo heeft echte commandobindings.',host='Context, naam/rol, focusroute, commandoprioriteit en platformbinding.',counterexample='Sneltoetsen ontbreken niet allemaal: ui04 bindt bewaren/undo en andere opdrachten.',sources=['R71','R78','R83']),
dict(component='Boom',provided='Eigen uitklapbericht en afzonderlijk selectiebericht; host bewaart domein-ID.',host='Pijltjes, logische boomstructuur, meervoudige selectie, afstammelingenscope en viewportkoppeling.',counterexample='Uitklappen en selecteren zijn in de huidige API al afzonderlijke handelingen.',sources=['R71','R78']),
dict(component='Tabel',provided='Kolommen/rijen, één geselecteerde positie en rij-/menuberichten; host remapt IDs.',host='Rasterbewerking, sorteren/filteren, multi-/bereikselectie, formule-/plak-/virtualisatiecontract voor gekozen taak.',counterexample='Een positionele presentatie-API is niet automatisch een ID-bug; huidige host vertaalt expliciet.',sources=['R71','R78','R81']),
dict(component='Dialoog',provided='Kaart/overlay; host-demo heeft Escape/Enter en muisopvang.',host='Beginfocus, terugkeerfocus, toets-/opdrachtisolatie, fouten, schaal en scroll.',counterexample='Escape/Enter zijn al ingevuld; een kaart bewijst de overige modale lifecycle niet.',sources=['R71','R78','R83','A06']),
dict(component='Menu',provided='Actie-/checked-/disabledweergave, popupplaatsing en klik-dismiss.',host='Toetsnavigatie, focusretour, typeahead indien gekozen, submenu’s en te groot menu.',counterexample='Plaatsinghelper bevat al randcorrectie; niet zonder runtime bewijs clipping claimen.',sources=['R80','R78']),
dict(component='Splitter',provided='5px sleepgebied/startbericht; host volgt cursor met180–480grenzen.',host='Alternatief voor slepen, naam/waarde, focus, reset/collapse en schaalafhankelijke grenzen.',counterexample='De host heeft bestaande begrenzing en paneelverbergopdrachten; geen totale afwezigheid van paneelbediening.',sources=['R80','R78','A112']),
dict(component='Webpakket',provided='CSS/verwachte state-attributen en visuele gallery; fonts door app geladen.',host='Juiste HTML/platformsemantiek, feitelijke events/lifecycle, labels/fouten en appintegratie.',counterexample='Browser-native dialog is een mogelijke implementatie voor web; dit vervangt geen native Rust-platformbewijs.',sources=['R79','R82','A113'])]
hashes={}
for cache in ['style-85a6aaf','iced-0.13.1']:
    hashes[cache]={e['path']:e['sha256'] for e in json.loads((W/'upstream'/cache/'manifest.json').read_text())}
audit=dict(checked_at=now,style_commit=sha,iced_commit=iced,method='Statische broninspectie en kruiscontrole met besluitbron; geen nieuwe app-/renderer-/gebruikersproef.',contracts=contracts,source_hashes=hashes,limits=['Geen runtime-eventpropagatie of vensterlayout gemeten.','Gallery zelf noemt zich reviewhulp; simulatie van bewaren/export/print is geen productie-I/O.','Web-CSS en native componentbron leveren verschillende delen van één productcontract.','APG-splitterpagina heeft eigen reviewvoorbehoud; patroon geen norm.'])
(OUT/'OpenAEC-UI-componentcontracten.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
(W/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
(W/'findings.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False)+'\n')
sp=ROOT/'work/ui-research-state.json';state=json.loads(sp.read_text())
state['last_updated']=now
state['completed_runs'].append(dict(date=now,modules=['01','02','03','12','13','14'],method='Actuele0.4-component-/reviewhost-/webpakketcontractaudit met primaire keyboard-/dialog-/splitterdocumentatie; positieve ID/sneltoets/expandtegenvoorbeelden.',findings_added=['UI-056'],findings_corrected=['UI-002','UI-004','UI-008','UI-009','UI-038','UI-050'],evidence=['outputs/OpenAEC-UI-componentcontracten.json'],checks=['Bron-/hostgrenzen herleidbaar vastgelegd voor zeven componentgroepen; geen nieuwe runtimetests.'],limitations=['Geen toetslekkage, clipping, beschadiging of platformconformiteit geclaimd.','Geen browsercontrole wegens eerdere URL-policyblokkade.'],qa='work/ui-research/report-qa-run09.json'))
for m in state['modules']:
    if m['id'] in ['01','02','03','12','13','14']:m['last_updated']=now;m['validation_open']=True
state['next_actions']=['Maak na de versie-/componentaudit het ochtendadvies concreet met voorgestelde taakfixtures en acceptatiebewijs per eerste doorsnede.','Werk alleen resterende verbindingen uit die besluitvorming verbeteren; geen herhaling of willekeurige nieuwe bronnen.','Geen nieuwe poging via alternatieve browsers/headlessroutes na URL-policyblokkade.','Laatste run: synthese en controles, uiterlijk08:00Europe/Amsterdam stoppen en automation beëindigen.']
sp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(sources=len(sources),findings=len(findings),contract_groups=len(contracts))))
