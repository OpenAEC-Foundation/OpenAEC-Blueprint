#!/usr/bin/env python3
"""Review Planner ribbon meanings against the shared Rust icon vocabulary."""
import json
import re
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
inventory = json.loads((ROOT / 'harmonization/planner-ribbon-ui-icons.json').read_text())
names = {icon['name'] for icon in inventory['icons']}

# The source label/action, rather than the Lucide name, determines the command.
meanings = dict(line.split('|', 1) for line in '''Activity|AI-activiteitenpaneel
AlertTriangle|Waarschuwingen, overallocatie en AI-waarschuwing
ArrowLeftToLine|Voorgangers traceren
ArrowRightToLine|Opvolgers traceren
ArrowUpDown|Tabel sorteren
BarChart3|Resourcehistogram aan/uit
Calendar|Projectkalender openen
CalendarClock|Project in tijd verschuiven en statusdatum
CalendarDays|Statusdatumlijn aan/uit
CalendarRange|Layout met periodeweergave
Check|AI-token gekopieerd / AI-actie bevestigd
ChevronDown|Lint uitklappen
ChevronLeft|Vorige resource
ChevronRight|Volgende resource
ChevronUp|Lint inklappen
ChevronsDownUp|Taken samenvouwen
ChevronsUpDown|Taken uitvouwen
Circle|AI-verbindingsstatus
Columns3|Tabelkolommen instellen
Copy|AI-token naar klembord kopiëren
DatabaseBackup|Automatische AI-backup
Diamond|Mijlpaal toevoegen
Download|Exportmenu openen
Eraser|Resourcevereffening wissen
Eye|Eigenschappenpaneel / zichtbare weergavelaag
EyeOff|Weergavelaag verbergen
FileDown|Voortgang exporteren
FileText|Nieuw project
FileUp|Voortgang importeren
Filter|Filtermenu of filterlayout
Flag|Baselinebediening of vlaglayout
FolderOpen|Project openen / AI-backupmap
GanttChartSquare|Gantt-layout
GitCompareArrows|Baselines beheren
HardHat|Ploegenlayout
Hash|WBS automatisch coderen
History|Recente projecten openen
IndentDecrease|Taak minder diep inspringen
IndentIncrease|Taak dieper inspringen
Info|Projectinformatie openen
Keyboard|Sneltoetsen tonen
Layers|Taken groeperen
LayoutGrid|Baseline-overlay tonen
LayoutTemplate|Projectsjabloon of layoutkeuze
Link|Taakrelatie tekenen
ListOrdered|WBS hernummeren
ListTree|Boomlayout
Lock|AI-verbinding alleen-lezen
Map|Minikaart tonen
Maximize2|Presentatiemodus aanzetten
Milestone|Mijlpaallayout
Minimize2|Presentatiemodus uitzetten
MoveHorizontal|Zwevende tijdsbalk tonen
Palette|Resourcekleuren tonen
PanelRight|Resourcepaneel rechts docken
Pause|AI-automatisering pauzeren
Play|Planning berekenen / AI hervatten of starten
Plug|AI-verbinding openen
Plus|Taak toevoegen
Printer|Afdrukvoorbeeld openen
Puzzle|Fallback-icoon voor extensieknop
Redo2|Bewerking opnieuw uitvoeren
RefreshCw|AI-verbinding vernieuwen
Route|Kritieke-padlayout
Save|Project opslaan / AI-veiligheidsactie
SaveAll|Project Opslaan als
Scale|Resources vereffenen
Scissors|Taak splitsen
Settings|Projectinstellingen openen
Spline|Taakrelatielijnen tonen
SplitSquareHorizontal|Gesplitste weergave aan/uit
Square|AI-server stoppen
Star|Favoriete layout
Tags|Codes en velden beheren
Trash2|Geselecteerde taak verwijderen
TrendingUp|Voortgangslijn tonen
Truck|Apparatuurlayout
Undo2|Bewerking ongedaan maken
Unlock|AI-verbinding bewerken toestaan
UserPlus|Resource aan taak toewijzen
Users|Resourcepaneel of personenlayout
Wrench|Gereedschappenlayout
X|Statusdatumveld sluiten
ZoomIn|Gantt-tijdas inzoomen
ZoomOut|Gantt-tijdas uitzoomen'''.splitlines())
assert set(meanings) == names

core = {
    'Check': 'Check', 'Download': 'Export', 'FileText': 'New',
    'FolderOpen': 'Open', 'PanelRight': 'PanelRight', 'Puzzle': 'Extensions',
    'Redo2': 'Redo', 'Save': 'Save', 'SaveAll': 'SaveAs',
    'Settings': 'Settings', 'Undo2': 'Undo', 'X': 'Close', 'ZoomIn': 'ZoomIn', 'ZoomOut': 'ZoomOut',
}
collisions = {
    'Circle': ('RibbonIcon::DrawingCircle', 'AI-statusstip is geen tekencommando.'),
    'Copy': ('Icon::Duplicate / RibbonIcon::ClipboardCopy', 'Token naar klembord kopiëren is geen document dupliceren; de klembordvorm past semantisch beter.'),
    'Info': ('Icon::Help', 'Projectinformatie is geen hulpactie.'),
    'LayoutGrid': ('Icon::Grid', 'Baseline-overlay wisselen is geen rasterweergave wisselen.'),
    'Maximize2': ('Icon::Maximize', 'Presentatiemodus is geen OS-venster maximaliseren.'),
    'Minimize2': ('Icon::Minimize', 'Presentatiemodus verlaten is geen OS-venster minimaliseren.'),
    'Play': ('berekenen / AI-start / AI-hervat', 'Eén driehoek bedient verschillende opdrachten; de commandosemantiek moet per context afzonderlijk blijven.'),
    'Plus': ('Icon::New', 'Een taak toevoegen is geen nieuw document maken.'),
    'Printer': ('Icon::Print', 'De knop opent een afdrukvoorbeeld en drukt nog niets af.'),
    'Scale': ('Icon::Measure', 'Resourcevereffening is geen lengtemeting.'),
    'Scissors': ('RibbonIcon::ClipboardCut', 'Taak splitsen is geen selectie naar het klembord knippen.'),
}
assert not set(core) & set(collisions)

source = (ROOT / 'crates/openaec-ui/src/icons.rs').read_text()
asset_map = dict(re.findall(r'Self::(\w+) => include_bytes!\("\.\./assets/icons/([^\"]+)"\)', source))
assert set(core.values()) <= set(asset_map)
decisions = []
for icon in inventory['icons']:
    name = icon['name']
    if name in core:
        status = 'gedeelde kandidaat'
        target = f'Icon::{core[name]}'
        note = ('Vervang de bronvorm pas na controle van knopmaat en context.' if name != 'SaveAll'
                else 'Opslaan als heeft al een eigen Rust-vorm; de Lucide SaveAll-vorm toont meerdere diskettes.')
        candidate = f'../crates/openaec-ui/assets/icons/{asset_map[core[name]]}'
    elif name in collisions:
        status = 'betekenis scheiden'
        target, note = collisions[name]
        candidate_name = re.match(r'Icon::(\w+)$', target)
        candidate = f'../crates/openaec-ui/assets/icons/{asset_map[candidate_name.group(1)]}' if candidate_name else None
    else:
        status = 'eigen Planner-context'
        target = 'Nog geen gedeelde commandovariant'
        note = 'Eigen opdracht of toestand; native vorm volgt na schermreview.'
        candidate = None
    decisions.append({**icon, 'meaning': meanings[name], 'status': status,
                      'proposed_target': target, 'rationale': note,
                      'rust_candidate_svg': candidate, 'shared_core_candidate': name in core,
                      'planner_command_integrated': False})

raw_counts = Counter(item['status'] for item in decisions)
counts = {name: raw_counts[name] for name in
          ('betekenis scheiden', 'gedeelde kandidaat', 'eigen Planner-context')}
out = {'repository': inventory['repository'], 'commit': inventory['commit'],
       'source_index': '../harmonization/planner-ribbon-ui-icons.json',
       'count': len(decisions), 'status_counts': counts, 'decisions': decisions}
(ROOT / 'design/planner-ribbon-crosswalk.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in sorted(decisions, key=lambda x: ({'betekenis scheiden': 0, 'gedeelde kandidaat': 1}.get(x['status'], 2), x['name'])):
    use = item['uses'][0]
    link = f'https://github.com/OpenAEC-Foundation/open-planner-studio/blob/{inventory["commit"]}/{use["file"]}#L{use["line"]}'
    candidate = (f'<div class="icon"><img src="{escape(item["rust_candidate_svg"])}" width="24" height="24" alt=""><small>Rust-kandidaat</small></div>'
                 if item['rust_candidate_svg'] else '')
    cards.append(f'''<article data-status="{escape(item['status'])}" data-search="{escape((item['name']+' '+item['meaning']).lower())}"><div class="symbols"><div class="icon"><img src="../harmonization/{escape(item['svg'])}" width="24" height="24" alt=""><small>Planner-bron</small></div>{candidate}</div><h3>{escape(item['name'])}</h3><p class="meaning">{escape(item['meaning'])}</p><span class="badge">{escape(item['status'])}</span><p class="target">{escape(item['proposed_target'])}</p><p class="note">{escape(item['rationale'])}</p><a href="{escape(link)}">Bronaanroep ↗</a></article>''')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Planner · Rust-betekenissen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;background:#f1f1f2;color:#303039}*{box-sizing:border-box}[hidden]{display:none!important}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:10px 0 4px}.hero p{max-width:1000px;color:#dadade;margin:0}.main{max-width:1410px;margin:auto;padding:23px}.note-top{background:#fff8eb;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}.filters{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:17px}.filters button,.filters input{font:inherit;border:1px solid #c9c9d0;background:white;padding:8px 11px}.filters button.active{background:#303039;color:white}.filters input{width:min(100%,300px)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}article{background:#fff;border:1px solid #d9d9df;border-top:3px solid #d9d9df;padding:13px 15px 15px;min-height:280px;display:flex;flex-direction:column}article[data-status="betekenis scheiden"]{border-top-color:#c96847}article[data-status="gedeelde kandidaat"]{border-top-color:#59997e}.symbols{display:flex;gap:7px}.icon{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;width:92px;height:62px;background:#fafafa;border:1px solid #e3e3e6;color:#a55200}.icon small{font-size:9px;color:#777781}.icon img{filter:brightness(0) saturate(100%) invert(39%) sepia(84%) saturate(1526%) hue-rotate(355deg) brightness(93%)}article h3{font-size:14px;margin:11px 0 2px}.meaning{font-size:12px;margin:0 0 8px}.badge{align-self:start;background:#fff0d8;color:#88510d;border:1px solid #e7c798;padding:3px 7px;font-size:10px}.target{font:11px ui-monospace,monospace;margin:9px 0 4px;overflow-wrap:anywhere}.note{font-size:11px;color:#676773;flex:1;margin:0 0 10px}article a{font-size:11px;color:#a55200}@media(max-width:620px){.main{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="planner-ribbon-icon-review.html">← Bronvormen</a><h1>Open Planner · commandobetekenissen</h1><p>85 bronvormen gekoppeld aan de gedeelde Rust-kern of bewust apart gehouden. Dit is een semantische beoordeling; de voorgestelde Planner-koppelingen zijn nog niet ingebouwd.</p></div><main class="main"><div class="note-top"><strong>Belangrijkste botsingen.</strong> Afdrukvoorbeeld ≠ Afdrukken; Taak toevoegen ≠ Nieuw document; Taak splitsen ≠ Klembord knippen; Presentatiemodus ≠ venster maximaliseren. Instellingen gebruikt nu een tandwiel, beeldregelaars een eigen Controls-vorm. De AI-tab is conditioneel en extensie-SVG’s zijn runtime-data.</div><div class="filters"><button class="active" data-filter="all">Alles · 85</button>''' + ''.join(f'<button data-filter="{escape(k)}">{escape(k)} · {v}</button>' for k,v in counts.items()) + '''<input id="search" type="search" placeholder="Zoek icoon of handeling" aria-label="Zoek icoon"></div><div class="grid">''' + ''.join(cards) + '''</div></main><script>let filter='all';const q=document.querySelector('#search');function update(){for(const card of document.querySelectorAll('article'))card.hidden=!(filter==='all'||card.dataset.status===filter)||!card.dataset.search.includes(q.value.toLowerCase().trim())}for(const b of document.querySelectorAll('[data-filter]'))b.addEventListener('click',()=>{filter=b.dataset.filter;for(const x of document.querySelectorAll('[data-filter]'))x.classList.toggle('active',x===b);update()});q.addEventListener('input',update)</script></html>'''
(ROOT / 'design/planner-ribbon-crosswalk.html').write_text(page)
print(f'{len(decisions)} Planner icons classified: {counts}')
