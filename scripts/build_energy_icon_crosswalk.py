#!/usr/bin/env python3
"""Review source-used Energy icon meanings against the shared Rust vocabulary."""
import json
import re
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
inventory = json.loads((ROOT / 'harmonization/energy-ui-icons.json').read_text())
names = {icon['name'] for icon in inventory['icons']}

# The command or state in the component, not the Lucide name, decides reuse.
meanings = dict(line.split('|', 1) for line in '''AlertCircle|Validatiefout, ontbrekende invoer of waarschuwing
AlertTriangle|Waarschuwing bij project of controle
Archive|Project archiveren of uit archief herstellen; archiefbak openen
ArrowLeft|Vorige invoerstap
ArrowRight|Volgende stap, openen of naar onderdeel gaan
Ban|Afwezig installatietype
BookOpen|Handleiding of hoofdstuk openen
Box|IFC-model exporteren of modelgerelateerd onderdeel
Building|Utiliteit of appartement
Building2|Kantoor, appartement of collectieve installatie
Calculator|Berekening, prestatie of rekentool
Camera|Fotobewijs
Caravan|Woonwagen als gebouwtype
Check|Voltooid, akkoord of gekopieerd
CheckCircle2|Geslaagde controle of voltooide registratiestatus
ChevronDown|Bestandsmenu of sectie uitklappen
ChevronRight|Navigatiestap of gereedschappen openen
ChevronUp|Sectie inklappen
CircleAlert|Registratie vraagt aandacht
CircleHelp|Onbekende keuze of uitleg
CircleX|Openstaande registratie of onvolledig bewijs
ClipboardList|Maatwerkadvies en maatregelenlijst
Clock|Wachtende registratiestatus
Copy|Tekst kopiëren, project dupliceren of venster herstellen
Download|Gegevensuitwisseling of export
Droplet|Warm tapwater
Factory|Industrie of warmtekrachtkoppeling
Fan|Mechanische ventilatie
FileArchive|Projectdossier exporteren
FileDown|Rapport of PDF exporteren
FileInput|Extern projectbestand importeren
FilePlus|Nieuw project
FileText|Rapport, berekening of bestandsnamen
Flame|Verwarming of gasgestookt systeem
Folder|Bibliotheekmap of mapkeuze
FolderOpen|Projectbestand openen of gekozen map
FolderPlus|Nieuwe bibliotheekmap
GraduationCap|Onderwijsgebouw
GripVertical|Sleepgreep voor volgorde
HeartPulse|Zorggebouw
History|Historie of terugblikmelding
Home|Woning, dak of woningtype
HousePlus|Nieuw woonproject
Info|Informatie, toelichting of Over
Layers|Vloerconstructie
LayoutGrid|Gevel, alle mappen of rasterweergave
List|Lijstweergave
MessageSquare|Feedback geven
Minus|Venster minimaliseren
MoreHorizontal|Overig gebouwtype of contextmenu
MoreVertical|Map- of bibliotheekmenu
Network|Warmtenet of collectieve installatie
PanelRight|Inspectiepaneel tonen of verbergen
PanelRightClose|Rechterpaneel inklappen
PanelTop|Raamconstructie
Paperclip|Bewijsbijlage of verwijzing
Pencil|Item bewerken of projectinformatie openen
Plug|Elektrische warmwatervoorziening
Plus|Wisselende entiteit toevoegen
Printer|Rapport daadwerkelijk afdrukken
RefreshCw|Berekening opnieuw uitvoeren
RotateCcw|Item uit prullenbak herstellen
Save|Project opslaan én Opslaan als
Search|Zoeken in projecten of opdrachten
Settings|Instellingen openen
ShieldCheck|Geslaagde kerncontrole
ShieldQuestion|Niet-geverifieerde toestand
Ship|Woonboot als gebouwtype
ShoppingBag|Winkelgebouw
SlidersHorizontal|Instellingen openen of algemene instellingensectie
Square|Venster maximaliseren
Sun|Zonnepanelen
Table2|Resultatentabel tonen
Thermometer|Warmtepomp of temperatuur
Trash2|Entiteit verwijderen of prullenbak
TreePine|Biomassasysteem
Undo2|Bewerking terugdraaien
Upload|Extern formaat importeren
Wind|Natuurlijke ventilatie of luchtverwarming
Wrench|Gereedschappen openen
X|Paneel sluiten, recent item vergeten of negatieve status
XCircle|Fout of mislukte controle
XSquare|Actief tabblad sluiten
Zap|Elektrische verwarming'''.splitlines())
assert set(meanings) == names, (sorted(names - set(meanings)), sorted(set(meanings) - names))

core = {
    'ArrowLeft': 'Back', 'Check': 'Check', 'Download': 'Export',
    'FileDown': 'Export', 'FileInput': 'Import', 'FilePlus': 'New',
    'FolderOpen': 'Open', 'Minus': 'Minimize', 'PanelRight': 'PanelRight',
    'Printer': 'Print', 'Search': 'Search', 'Settings': 'Settings',
    'Square': 'Maximize', 'Undo2': 'Undo', 'Upload': 'Import',
    'XSquare': 'Close',
}
collisions = {
    'Archive': ('archiveren / herstellen', 'Dezelfde archiefbak bedient tegengestelde opdrachten; een herstelaanduiding moet apart zichtbaar worden.'),
    'ArrowRight': ('stap / openen / doorlopen', 'Dezelfde pijl geeft verschillende navigatiedoelen aan; doeltekst en context bepalen de actie.'),
    'Building2': ('gebouwtype / collectieve installatie', 'Eén gebouwvorm codeert een kantoorgebouw, appartement en onbekend collectief systeem.'),
    'ChevronRight': ('navigatie / uitklappen', 'Een volgende stap is niet dezelfde handeling als het tonen van een subgroep.'),
    'Copy': ('kopiëren / dupliceren / venster herstellen', 'Klembordactie, projectkopie en OS-vensterherstel vragen verschillende semantische doelen.'),
    'FolderOpen': ('project openen / geselecteerde map', 'Dezelfde vorm is een opdracht én een maptoestand; `Icon::Open` geldt alleen voor de opdracht.'),
    'LayoutGrid': ('gevel / alle mappen / rasterweergave', 'Bouwdeel, bibliotheekfilter en weergaveknop zijn drie betekenissen van hetzelfde raster.'),
    'MoreHorizontal': ('overig type / contextmenu', 'Een typekeuze is geen meer-optiesknop.'),
    'Pencil': ('bewerken / projectinformatie', 'Een projectinformatiedialoog openen vraagt een eigen contextbesluit naast item bewerken.'),
    'Plus': ('project / maatregel / inventarisitem toevoegen', 'Een generieke plus is niet automatisch `Icon::New` voor een document; houd de entiteit in de knoptekst.'),
    'Save': ('opslaan / opslaan als', 'De bron gebruikt één diskette voor twee commando’s; `Icon::SaveAs` heeft een eigen vorm.'),
    'SlidersHorizontal': ('algemene instellingen / regelaars', 'De schuiven dienen zowel als navigatie naar Instellingen als als markering van de algemene instellingensectie; `Settings` en `Controls` zijn gescheiden.'),
    'X': ('sluiten / vergeten / afgekeurd', 'Een kruis voor een mislukte toets is geen venster- of paneelactie.'),
}
# A source shape can still have one safe shared use amid other, distinct uses.
assert set(core) & set(collisions) == {'FolderOpen'}
collision_candidates = {
    'Copy': ('Duplicate', 'Restore'),
    'FolderOpen': ('Open',),
    'LayoutGrid': ('Grid',),
    'Plus': ('New',),
    'Save': ('Save', 'SaveAs'),
    'SlidersHorizontal': ('Settings', 'Controls'),
    'X': ('Close',),
}
source = (ROOT / 'crates/openaec-ui/src/icons.rs').read_text()
asset_map = dict(re.findall(r'Self::(\w+) => include_bytes!\("\.\./assets/icons/([^\"]+)"\)', source))
assert set(core.values()) | {x for values in collision_candidates.values() for x in values} <= set(asset_map)

decisions = []
for icon in inventory['icons']:
    name = icon['name']
    if name in collisions:
        status = 'betekenis scheiden'
        target, note = collisions[name]
        candidates = collision_candidates.get(name, ())
    elif name in core:
        status = 'gedeelde kandidaat'
        target = f'Icon::{core[name]}'
        note = 'Vergelijk knopmaat en toestand in de native Energy-schermreview vóór vervanging.'
        candidates = (core[name],)
    else:
        status = 'Energy- of toestandsspecifiek'
        target = 'Nog geen gedeelde commandovariant'
        note = 'Domeinobject, informatiestatus of bediening zonder vastgesteld algemeen commandodoel.'
        candidates = ()
    decisions.append({**icon, 'meaning': meanings[name], 'status': status,
                      'proposed_target': target, 'rationale': note,
                      'rust_candidates': [{'icon': f'Icon::{variant}',
                                           'svg': f'../crates/openaec-ui/assets/icons/{asset_map[variant]}'}
                                          for variant in candidates],
                      'energy_command_integrated': False})

raw_counts = Counter(item['status'] for item in decisions)
status_order = ('betekenis scheiden', 'gedeelde kandidaat', 'Energy- of toestandsspecifiek')
counts = {status: raw_counts[status] for status in status_order}
out = {'repository': inventory['repository'], 'commit': inventory['commit'],
       'source_index': '../harmonization/energy-ui-icons.json', 'count': len(decisions),
       'status_counts': counts, 'decisions': decisions}
(ROOT / 'design/energy-icon-crosswalk.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in sorted(decisions, key=lambda x: (status_order.index(x['status']), x['name'])):
    use = item['uses'][0]
    link = f'https://github.com/OpenAEC-Foundation/open-energy-studio/blob/{inventory["commit"]}/{use["file"]}#L{use["line"]}'
    candidate = ''.join(f'<div class="icon"><img src="{escape(c["svg"])}" width="24" height="24" alt=""><small>{escape(c["icon"])}</small></div>' for c in item['rust_candidates'])
    cards.append(f'''<article data-status="{escape(item['status'])}" data-search="{escape((item['name']+' '+item['meaning']).lower())}"><div class="symbols"><div class="icon"><img src="../harmonization/{escape(item['svg'])}" width="24" height="24" alt=""><small>Energy-bron</small></div>{candidate}</div><h3>{escape(item['name'])}</h3><p class="meaning">{escape(item['meaning'])}</p><span class="badge">{escape(item['status'])}</span><p class="target">{escape(item['proposed_target'])}</p><p class="note">{escape(item['rationale'])}</p><a href="{escape(link)}">Bronaanroep ↗ · {len(item['uses'])} {'plaats' if len(item['uses']) == 1 else 'plaatsen'}</a></article>''')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Energy · Rust-betekenissen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;background:#f1f1f2;color:#303039}*{box-sizing:border-box}[hidden]{display:none!important}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:10px 0 4px}.hero p{max-width:1000px;color:#dadade;margin:0}.main{max-width:1410px;margin:auto;padding:23px}.note-top{background:#fff8eb;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}.filters{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:17px}.filters button,.filters input{font:inherit;border:1px solid #c9c9d0;background:white;padding:8px 11px}.filters button.active{background:#303039;color:white}.filters input{width:min(100%,300px)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;border-top:3px solid #d9d9df;padding:13px 15px 15px;min-height:290px;display:flex;flex-direction:column}article[data-status="betekenis scheiden"]{border-top-color:#c96847}article[data-status="gedeelde kandidaat"]{border-top-color:#59997e}.symbols{display:flex;gap:7px}.icon{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;width:70px;min-width:0;height:62px;background:#fafafa;border:1px solid #e3e3e6;color:#a55200}.icon small{font-size:9px;color:#777781;text-align:center;overflow-wrap:anywhere}.icon img{filter:brightness(0) saturate(100%) invert(39%) sepia(84%) saturate(1526%) hue-rotate(355deg) brightness(93%)}article h3{font-size:14px;margin:11px 0 2px}.meaning{font-size:12px;margin:0 0 8px}.badge{align-self:start;background:#fff0d8;color:#88510d;border:1px solid #e7c798;padding:3px 7px;font-size:10px}.target{font:11px ui-monospace,monospace;margin:9px 0 4px;overflow-wrap:anywhere}.note{font-size:11px;color:#676773;flex:1;margin:0 0 10px}article a{font-size:11px;color:#a55200}@media(max-width:620px){.main{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="energy-ui-icon-review.html">← Bronvormen</a><h1>Open Energy · commandobetekenissen</h1><p>84 bronvormen beoordeeld tegen de gedeelde Rust-kern en het Energy-domein. De voorgestelde koppelingen zijn nog geen Energy-inbouw.</p></div><main class="main"><div class="note-top"><strong>Betekenisbotsingen.</strong> Save bedient Opslaan én Opslaan als; Copy bedient kopiëren, dupliceren én vensterherstel. Hetzelfde raster duidt een gevel, bibliotheekfilter en rasterweergave aan. Een gedeelde Rust-vorm wordt alleen per passende UI-actie gekozen.</div><div class="filters"><button class="active" data-filter="all">Alles · 84</button>''' + ''.join(f'<button data-filter="{escape(k)}">{escape(k)} · {v}</button>' for k,v in counts.items()) + '''<input id="search" type="search" placeholder="Zoek icoon of handeling" aria-label="Zoek icoon"></div><div class="grid">''' + ''.join(cards) + '''</div></main><script>let filter='all';const q=document.querySelector('#search');function update(){for(const card of document.querySelectorAll('article'))card.hidden=!(filter==='all'||card.dataset.status===filter)||!card.dataset.search.includes(q.value.toLowerCase().trim())}for(const b of document.querySelectorAll('[data-filter]'))b.addEventListener('click',()=>{filter=b.dataset.filter;for(const x of document.querySelectorAll('[data-filter]'))x.classList.toggle('active',x===b);update()});q.addEventListener('input',update)</script></html>'''
(ROOT / 'design/energy-icon-crosswalk.html').write_text(page)
print(f'{len(decisions)} Energy icons classified: {counts}')
