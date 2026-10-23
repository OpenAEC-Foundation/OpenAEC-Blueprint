"""Record current-head correction without replacing original research snapshots."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent.parent
W = ROOT / 'work/ui-research'
OUT = ROOT / 'outputs'
now = datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(timespec='seconds')
style = '85a6aafc7d003ec8f61c9543b352a1f1b0f47346'
pdf = 'e9f599f66ac75c5cb7656789573f942ecb8db2d7'
sources = json.loads((W/'sources.json').read_text())
findings = json.loads((W/'findings.json').read_text())
assert 'R70' not in {s['id'] for s in sources}, 'Run once only'
def source(id, title, repo, sha, cache, path, supports, limits):
    sources.append(dict(id=id,title=title,url=f'https://github.com/OpenAEC-Foundation/{repo}/blob/{sha}/{path}',type='Gepinde actuele OpenAEC-broncode; versieaudit 23 oktober',checked_at='2026-10-23',supports=supports,limits=limits,local_file=f'work/ui-research/upstream/{cache}/{path}',commit=sha))
def s(id,title,path,supports,limits):
    source(id,title,'OpenAEC-Style-Repo',style,'style-85a6aaf',path,supports,limits)
def p(id,title,path,supports,limits):
    source(id,title,'open-pdf-studio',pdf,'pdf-e9f599f','open-pdf-studio/js/'+path,supports,limits)
s('R70','0.4-generator: dezelfde JSON naar Rust en CSS','scripts/generate_tokens_04.py','Bestaande 0.4-pipeline naar design/tokens.rs en web/openaec-tokens.css. --check uitgevoerd: vijf thema’s,31 kleurrollen actueel.','Tekst-/tokenafleiding en ingebouwde kleurpaarcontrole; geen renderer-, typografie-, platform- of apppariteit.')
s('R71','Bestaande 0.4-widgets en expliciete rendererafwijkingen','crates/openaec-ui/src/design/widgets.rs','Echte iced-knoppen, velden en andere gedeelde componenten. Bron documenteert focusrand binnen de control en solide HC-disabledrand als benadering.','Geen volledige native keyboard-/screenreaderproef of bewezen appadoptie; knop bouwt op gepinde iced0.13.1.')
s('R72','B2 als gedeelde Rust-iconenbibliotheek','crates/openaec-icons/README.md','Bestaande bibliotheek met945 iconen,16/24-masters,selectie per app en SVG-bronnen.','Catalogus en API gelezen; geen Cargo-build, complete assetcontrole of herkenningsonderzoek uitgevoerd.')
p('R73','PDF: volledige getalparser naast bewuste prefixparser','core/getal-invoer.js','leesGetal weigert trailingtekst; leesGetalBegin is expliciet prefix. Enkel punt/komma betekent decimaal; gekozen groepsregels en Unicodecijfers. Bestaande pure tests uitgevoerd.','Geen audit van ieder getalveld of AEC-eenheid. Ambigue getalnotatie blijft productkeuze; geen volledige UI-/saveproef.')
p('R74','PDF: getalvelden met zichtbare tekst en canonieke waarde','ui/getal-veld.js','DOM-adapter gebruikt gedeelde normalisatie; main.js importeert en installeert deze in init met app-taal. Bron houdt tekst tijdens bewerken en canonieke waarde uiteen.','Installatieroute statisch gelezen, geen browser/WebView/IME/toegankelijkheidsboom getest. Niet elk veld of fallback getoetst.')
p('R75','PDF: foutreden behouden bij Error/string/object','core/fout-bericht.js','Pure helper vermijdt lege reden, leest detail/code en string. Vier bestaande pure testgevallen geslaagd.','Geen volledige foutmeldingflow, lokalisatie, herstelactie of toegankelijkheidsaankondiging getest.')
s('R76','Nieuwste portable-check: bestaande beperkte bronselectie','scripts/check_portable_ui.py','Ontbrekende lokale snapshot blijft expliciete exit0; Rustvergelijking gebruikt src.glob("*.rs"), dus doorloopt niet de nieuwe design/-submap.','Nieuwste checker alleen gelezen, niet uitgevoerd op complete afnemer; geen aangetoonde kapotte Pointcloud-build of actuele pariteitsclaim.')
p('R77','Nieuwere hatchmetadata: ook vreemde PatternName/PatternColor','pdf/saver/hatch-meta.js','Naast OPS-metadata bestaan mappings en lezen van vreemde patroonvelden; onbekend patroon valt terug op none.','Alleen broncontrole, geen PDF-roundtrip of normconformiteit; eerdere pure geometrieproeven horen bij oudere snapshot.')

byid = {f['id']:f for f in findings}
byid['UI-049'].update(claim='Nieuwste Style HEAD bevat al een0.4-generator van besloten JSON naar Rust en CSS, naast de oudere prototypepipeline; de0.4 --check slaagt.',source_ids=['R63','R64','R65','R70','R71','A100'],recommendation='Documenteer en gebruik de bestaande0.4-pipeline; leg migratie/afnemers en de resterende rendererafwijkingen vast. Beoordeel uitwisselformaat alleen waar nuttig.',limits='Oudere prototypepipeline blijft bestaan; cratepakketversie0.1 zegt niet dat0.4-implementatie ontbreekt. Generator alleen met --check uitgevoerd; geen appmigratie of rendererpariteit getest.',code_locations=['scripts/generate_tokens_04.py:main','crates/openaec-ui/src/design/mod.rs','crates/openaec-ui/src/design/tokens.rs','web/openaec-tokens.css'])
byid['UI-050']['source_ids'] += ['R71','R72']
byid['UI-052']['source_ids'] += ['R76']
byid['UI-052']['claim']='Oudere portablecheck gaf exit0 met ontbrekende afnemer. Nieuwste checker behoudt die grens en vergelijkt Rust alleen direct in src, zonder design/-submap.'
byid['UI-052']['limits']='Oudere checker daadwerkelijk uitgevoerd; nieuwste alleen statisch gelezen. Geen volledige afnemerbuild of aangetoonde distributiefout.'
byid['UI-012']['source_ids'] += ['R73']
byid['UI-012']['limits']='Calc-HEAD bij deze versieaudit gelijk aan geproefde commit; geen beschadigde begroting of end-to-end incident aangetoond. Nieuwere PDF heeft al een aparte strikte parser; claim niet op alle apps toepassen.'
byid['UI-002']['source_ids'] += ['R71']
byid['UI-002']['limits'] += ' Nieuwste0.4-knop gebruikt dezelfde iced0.13.1-button; nieuwe widgets zijn geen volledige keyboard-/AT-proef.'
for obj in sources:
    if obj['id'] in ['A01','A02']:
        obj['checked_at']='2026-10-23'
        obj['limits'] += ' Issue opnieuw geraadpleegd tijdens versieaudit; open status op zichzelf bewijst geen concrete appbeperking.'
(W/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
(W/'findings.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False)+'\n')

probes = json.loads((OUT/'OpenAEC-UI-proeven.json').read_text())
hashes = lambda cache: {e['path']:e['sha256'] for e in json.loads((W/'upstream'/cache/'manifest.json').read_text())}
raw = W/'probes/current-head/pdf-numeric-error-tests.tap'
dest = raw.with_suffix('.txt')
if raw.exists():raw.rename(dest)
probes['current_head_tokens_04'] = dict(commit=style,command='python3 scripts/generate_tokens_04.py --check',exit_code=0,themes=5,colour_roles=31,output='work/ui-research/probes/current-head/tokens-04-check.txt',source_hashes=hashes('style-85a6aaf'),scope='Bestaande read-only afleidingscontrole; geen app, beeldvergelijking, Cargo-build of font-/platformvalidatie.')
probes['current_head_pdf_numeric_errors'] = dict(commit=pdf,command='Node24 --test core/getal-invoer.test.mjs core/fout-bericht.test.mjs',exit_code=0,tests=18,passed=18,failed=0,skipped=0,output=str(dest.relative_to(ROOT)),source_hashes=hashes('pdf-e9f599f'),scope='Bestaande14 pure getaltests en4 pure foutredentests. DOM-adapter/installatie alleen gelezen; geen volledige WebView/IME/eindgebruikersproef.')
(OUT/'OpenAEC-UI-proeven.json').write_text(json.dumps(probes,indent=2,ensure_ascii=False)+'\n')
heads = json.loads((W/'audits/upstream-heads-run08.json').read_text())
audit = dict(checked_at=now,heads=heads,original_style_snapshot='befcbff7790e8c593b2ec47ae18d43115a4f530c',original_pdf_snapshot='f754cb7c9d9adf654f6894cee15543413c24fcff',targeted_comparisons=[json.loads((W/'audits'/n).read_text()) for n in ['OpenAEC-Style-Repo-targeted-diff-run08.json','open-pdf-studio-targeted-diff-run08.json']],corrections=['0.4-implementatie en generator bestaan al; oude prototypepipeline is niet de hele huidige crate.','B2 is een gedeelde bibliotheek, geen uitsluitend visuele ontwerpcollectie.','PDF heeft expliciete strikte/prefix-getalhelpers; andere ambiguïteitsregel dan Calc.','Oudere PDF-viewer/snap/print/hatch-proeven niet zonder nieuwe integratie als nieuwste appvalidatie presenteren.'],limits=['Gerichte vergelijkingen, geen volledige audit van alle nieuwe bestanden. GitHub compare-fileslijst was begrensd op300; daarom volledige niet-afgekaptetrees en expliciete blobvergelijking gebruikt.','Gelijke functieblob bewijst geen gelijke totale app door afhankelijkheden/configuratie.','Calc en Validator HEAD gelijk aan eerdere onderzochte commits op controlemoment.','Geen checkout, commit/push of productiecodewijziging.'])
(OUT/'OpenAEC-UI-versieaudit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
sp=ROOT/'work/ui-research-state.json';state=json.loads(sp.read_text())
state['upstream_version_audit']=dict(checked_at=now,heads=heads,deliverable='outputs/OpenAEC-UI-versieaudit.json')
state['completed_runs'].append(dict(date=now,modules=['01','04','07','10','11','13','14','15'],method='Gerichte actuele upstream-HEAD-/blobcontrole, correctie verouderde generalisatie, bestaande read-only0.4-generatorcheck en18 pure PDF-tests; geen appintegratie.',findings_added=[],findings_corrected=['UI-002','UI-012','UI-049','UI-050','UI-052'],evidence=['outputs/OpenAEC-UI-versieaudit.json','outputs/OpenAEC-UI-proeven.json'],checks=['0.4 Rust/CSS-afleiding actueel:5thema’s31rollen.','18 bestaande pure PDF-getal-/fouttests geslaagd.'],limitations=['Oudere bronbewijzen blijven aan oorspronkelijke snapshot gekoppeld.','Geen volledige nieuwste app-, portable-, native- of gebruikersproef.'],qa='work/ui-research/report-qa-run08.json'))
for m in state['modules']:
    if m['id'] in ['01','04','07','10','11','13','14','15']:
        m['last_updated']=now;m['validation_open']=True
state['last_updated']=now
state['next_actions']=['Controleer de samenhang van actuele0.4-besluiten, echte componentimplementaties en nog niet bewezen taak-/hulptechnologiecontracten.','Controleer presentatie/rapportnavigatie waar beschikbaar en beperk resterende runs tot aantoonbare kennishiaten.','Houd versieaudit en oorspronkelijke proefgrenzen zichtbaar; geen generieke bugclaims uit oudere snapshots.','Maak de uiteindelijke ochtendagenda compact en stop uiterlijk08:00Europe/Amsterdam.']
sp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(sources=len(sources),findings=len(findings),new_tests=18,version_audit=True)))
