"""Build the first B2 family and a traceable function assessment queue."""
from pathlib import Path
import csv
import hashlib
import json
import zipfile
import shutil
from b2_font_geometry import font_sources
from b2_source_catalog import load_catalog, source_hashes, SUPPLEMENT
from b2_completion import PLANNED_KEYS, PLANNED
from b2_scope_audit import audit_hash, validate_scope_audit, render_scope_review
from build_b2_feedback_review import WARNING_PREVIEW, render_feedback_review
from b2_geometry import ROOT, construction, export_svg, foreground, layer_reason, SHAPE_REVISIONS, ROUNDED_JOINTS, WHOLE_ACCENT
from b2_second_series import DEFINITIONS as SECOND_DEFINITIONS, EXAMPLES as SECOND_EXAMPLES, ISSUES as SECOND_ISSUES, KEYS as SECOND_KEYS, SEMANTIC

from b2_window_series import DEFINITIONS as WINDOW_DEFINITIONS, EXAMPLES as WINDOW_EXAMPLES, KEYS as WINDOW_KEYS

from b2_text_series import DEFINITIONS as TEXT_DEFINITIONS, EXAMPLES as TEXT_EXAMPLES, ISSUES as TEXT_ISSUES, KEYS as TEXT_KEYS

from b2_data_series import DEFINITIONS as DATA_DEFINITIONS, EXAMPLES as DATA_EXAMPLES, ISSUES as DATA_ISSUES, KEYS as DATA_KEYS

from b2_report_series import DEFINITIONS as REPORT_DEFINITIONS, EXAMPLES as REPORT_EXAMPLES, ISSUES as REPORT_ISSUES, KEYS as REPORT_KEYS

from b2_ifc_series import DEFINITIONS as IFC_DEFINITIONS, EXAMPLES as IFC_EXAMPLES, ISSUES as IFC_ISSUES, KEYS as IFC_KEYS

from b2_tree_planning_geo import (DEFINITIONS as NEXT_DEFINITIONS, EXAMPLES as NEXT_EXAMPLES,
    ISSUES as NEXT_ISSUES, SERIES as NEXT_SERIES, SOURCE_FUNCTIONS, EVIDENCE, REUSED)

from b2_energy_pile_audio import (DEFINITIONS as LATER_DEFINITIONS, EXAMPLES as LATER_EXAMPLES,
    ISSUES as LATER_ISSUES, SERIES as LATER_SERIES, SOURCE_FUNCTIONS as LATER_SOURCES,
    EVIDENCE as LATER_EVIDENCE, REUSED as LATER_REUSED)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**LATER_SOURCES}
EVIDENCE={**EVIDENCE,**LATER_EVIDENCE}
REUSED={**REUSED,**LATER_REUSED}

from b2_page_views import (DEFINITIONS as PAGE_DEFINITIONS, EXAMPLES as PAGE_EXAMPLES,
    SOURCE_FUNCTIONS as PAGE_SOURCES, REUSED as PAGE_REUSED, KEYS as PAGE_KEYS)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**PAGE_SOURCES}
REUSED={**REUSED,**PAGE_REUSED}

from b2_bulk_series import (DEFINITIONS as BULK_DEFINITIONS, EXAMPLES as BULK_EXAMPLES,
    SOURCE_FUNCTIONS as BULK_SOURCES, SERIES as BULK_SERIES, REUSED as BULK_REUSED, GROUPS as BULK_GROUPS, AVAILABLE_SERIES)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**BULK_SOURCES}
REUSED={**REUSED,**BULK_REUSED}

from b2_session_two import (DEFINITIONS as SESSION_DEFINITIONS, EXAMPLES as SESSION_EXAMPLES,
    SOURCE_FUNCTIONS as SESSION_SOURCES, SERIES as SESSION_SERIES, REUSED as SESSION_REUSED,
    GROUPS as SESSION_GROUPS, AVAILABLE_SERIES as SESSION_AVAILABLE)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**SESSION_SOURCES}
REUSED={**REUSED,**SESSION_REUSED}
from b2_document_navigation import (DEFINITIONS as NAV_DEFINITIONS, EXAMPLES as NAV_EXAMPLES,
    SOURCE_FUNCTIONS as NAV_SOURCES, SERIES as NAV_SERIES, REUSED as NAV_REUSED,
    GROUPS as NAV_GROUPS, AVAILABLE_SERIES as NAV_AVAILABLE)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**NAV_SOURCES}
REUSED={**REUSED,**NAV_REUSED}
from b2_session_three import (DEFINITIONS as THIRD_DEFINITIONS, EXAMPLES as THIRD_EXAMPLES,
    SOURCE_FUNCTIONS as THIRD_SOURCES, SERIES as THIRD_SERIES, REUSED as THIRD_REUSED,
    GROUPS as THIRD_GROUPS, AVAILABLE_SERIES as THIRD_AVAILABLE, ISSUES as THIRD_ISSUES, TYPOGRAPHY as THIRD_TYPOGRAPHY)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**THIRD_SOURCES}
REUSED={**REUSED,**THIRD_REUSED}
from b2_session_four import (DEFINITIONS as FOURTH_DEFINITIONS, EXAMPLES as FOURTH_EXAMPLES,
    SOURCE_FUNCTIONS as FOURTH_SOURCES, SERIES as FOURTH_SERIES, REUSED as FOURTH_REUSED,
    GROUPS as FOURTH_GROUPS, AVAILABLE_SERIES as FOURTH_AVAILABLE, EVIDENCE as FOURTH_EVIDENCE, ISSUES as FOURTH_ISSUES)
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**FOURTH_SOURCES}
REUSED={**REUSED,**FOURTH_REUSED}
EVIDENCE={**EVIDENCE,**FOURTH_EVIDENCE}
from b2_completion import (DEFINITIONS as COMPLETION_DEFINITIONS, EXAMPLES as COMPLETION_EXAMPLES,
    SOURCE_FUNCTIONS as COMPLETION_SOURCES, SERIES as COMPLETION_SERIES,
    REUSED as COMPLETION_REUSED, EXCLUDED as COMPLETION_EXCLUDED,
    GROUPS as COMPLETION_GROUPS, AVAILABLE_SERIES as COMPLETION_AVAILABLE,
    EVIDENCE as COMPLETION_EVIDENCE, TYPOGRAPHY as COMPLETION_TYPOGRAPHY, DISPATCHERS as COMPLETION_DISPATCHERS,
    SEMANTIC as COMPLETION_SEMANTIC, DISPATCH_EVIDENCE as COMPLETION_DISPATCH_EVIDENCE)
SEMANTIC={**SEMANTIC,**COMPLETION_SEMANTIC}
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**COMPLETION_SOURCES}
REUSED={**REUSED,**COMPLETION_REUSED}
EVIDENCE={**EVIDENCE,**COMPLETION_EVIDENCE}
FONT_METADATA={**font_sources(),**THIRD_TYPOGRAPHY,**COMPLETION_TYPOGRAPHY}
ALL_AVAILABLE=(*AVAILABLE_SERIES,*SESSION_AVAILABLE,*NAV_AVAILABLE,*THIRD_AVAILABLE,*FOURTH_AVAILABLE,*COMPLETION_AVAILABLE)

OUT=ROOT/'design/icon-set-b2'
AUDIT=ROOT/'harmonization/icon-set-b2'
CATALOG=ROOT/'harmonization/function-icon-catalog.json'
BASIS_PATH=ROOT/'harmonization/icon-set-b2/basis-sources.json'
BASIS_SOURCES=json.loads(BASIS_PATH.read_text(encoding='utf-8'))
TOKENS=ROOT/'design/ontwerp-0.4/tokens-0.4.json'

# A function contract is independent of the artwork used by existing apps.
DEFINITIONS=[
 ('file.new','Nieuw document','Bestanden','Een nieuw document of project maken; geen nieuw object binnen een tekening.'),
 ('file.open','Openen','Bestanden','Een bestand of project openen; geen paneel openen of naar een processtap gaan.'),
 ('file.save','Opslaan','Bestanden','Het huidige document opslaan onder de bestaande identiteit.'),
 ('file.save-as','Opslaan als','Bestanden','Opslaan onder een andere naam of locatie; apart van gewoon opslaan.'),
 ('file.import','Importeren','Bestanden','Een gegevensinvoerworkflow voor de actieve werkomgeving starten. Formaatvarianten delen het icoon; het label benoemt het formaat.'),
 ('file.export','Exporteren','Bestanden','Gegevens uit het project wegschrijven. Geen algemene download of synchronisatie zonder verdere beoordeling.'),
 ('file.print','Afdrukken','Bestanden','Een document of rapport afdrukken; geen logo-instellingen of paginaformaat.'),
 ('edit.undo','Ongedaan maken','Bewerken','De laatste bewerking terugdraaien; geen terugnavigatie.'),
 ('edit.redo','Opnieuw uitvoeren','Bewerken','Een teruggedraaide bewerking opnieuw uitvoeren.'),
 ('edit.cut','Knippen','Bewerken','Selectie naar het klembord verplaatsen; geen kamer of taak splitsen.'),
 ('edit.copy','Kopiëren','Bewerken','Selectie of resultaat naar het klembord kopiëren; geen direct dupliceren.'),
 ('edit.paste','Plakken','Bewerken','Inhoud van het klembord invoegen.'),
 ('edit.duplicate','Dupliceren','Bewerken','Een extra exemplaar direct aanmaken; geen klembordstap.'),
 ('edit.delete','Verwijderen','Bewerken','Geselecteerde objecten verwijderen. Herstelbaarheid en omvang blijven in label/dialoog expliciet.'),
 ('edit.clear-all','Alles wissen','Bewerken','Alle inhoud binnen een expliciet benoemde scope wissen; apart van selectie verwijderen.'),
 ('edit.select','Selecteren','Selecteren','Objectselectie activeren. Tekstselectie en sonderingenpaneel niet automatisch koppelen.'),
 ('edit.select-all','Alles selecteren','Selecteren','Alles binnen de huidige scope selecteren; geen selectiegereedschap activeren.'),
 ('view.search','Zoeken','Navigeren','Een zoekopdracht of zoekinvoer; geen 100%-zoom of alleen filteren.'),
 ('view.zoom-in','Inzoomen','Navigeren','De weergaveschaal vergroten; geen object vergroten.'),
 ('view.zoom-out','Uitzoomen','Navigeren','De weergaveschaal verkleinen; geen object verkleinen.'),
 ('view.fit','Alles passend','Navigeren','Alle inhoud in beeld brengen; apart van pagina, selectie en breedte.'),
 ('view.fit-selection','Selectie passend','Navigeren','Alleen de geselecteerde inhoud passend in beeld brengen.'),
 ('view.fit-page','Pagina passend','Navigeren','Een volledige pagina binnen de weergave tonen.'),
 ('view.fit-width','Breedte passend','Navigeren','De documentbreedte passend in de weergave tonen.'),
 ('view.pan','Beeld verschuiven','Navigeren','De camera of weergave verschuiven; geen objecten verplaatsen.'),
 ('view.orbit','3D-beeld draaien','Navigeren','De camera om het model draaien; geen modelrotatie. De native Pointcloud-sleeproute en turn_orbit ondersteunen deze functie; de bron gebruikt daarvoor een invoergebaar.'),
 ('nav.back','Terug','Navigeren','Teruggaan in navigatie; vorige pagina/resource en ongedaan maken niet automatisch samenvoegen.'),
 ('nav.forward','Vooruit','Navigeren','Vooruitgaan in navigatiegeschiedenis. Algemene ga-naar-knoppen blijven te beoordelen.'),
 ('nav.home','Startpagina','Navigeren','Naar de startpagina gaan. Woningtype, dak en ruimtes blijven eigen betekenissen.'),
 ('draw.note','Opmerking','Annoteren en meten','Een notitie/annotatie aan het document toevoegen; geen feedback naar de ontwikkelaar of chatbericht.'),
 ('measure.distance','Afstand meten','Annoteren en meten','Een afstand opmeten; geen schaal, liniaalweergave of oppervlaktemeting.'),
]

# Explicitly inspected representative source call sites, not approval of a cluster.
EXAMPLES={
 'file.new':'18965242f5d73b74','file.open':'933a9427b0384941','file.save':'d43a61afd637ffe2',
 'file.save-as':'660dabcaa19abdda','file.import':'4e53633009e16e77','file.export':'5cab79042d178cfd',
 'file.print':'fab9bf743af167c4','edit.undo':'92310a61b3fcfa0c','edit.redo':'378f63c41b7b6fa4',
 'edit.cut':'b1f5537ca9fcd8d3','edit.copy':'41771a668b68a382','edit.paste':'24df098d9c7e5865',
 'edit.duplicate':'df18e86cfe4f6e89','edit.delete':'13a87dbaf9a4ea07','edit.clear-all':'131846172049210a',
 'edit.select':'3fd55ee9cc6267ac','edit.select-all':'2fc26c88f2265f9b','view.search':'75e07c0e0323b83d',
 'view.zoom-in':'8715f0e9c1418594','view.zoom-out':'e29e432f247f20c0','view.fit':'c730a43430ffe194',
 'view.fit-selection':'acf2d93966f6c796','view.fit-page':'f01a1916c36006c4',
 'view.fit-width':'b3f80dd044b20e08','view.pan':'ec0aeac49d30d1cc',
 'nav.back':'409b86c979f9874e','draw.note':'f0e801cdc5ba894f','measure.distance':'55133dfb800ace87',
}
ISSUES={
 '2f41a76ad09abfb4':'Logo-instellingen zijn geen afdrukopdracht.',
 '730c4023dee18e42':'Navigatie naar een processtap; geen bestand openen.',
 'f422a43648ca2b57':'Update Excel/synchronisatie vraagt een eigen functiebeoordeling.',
 'c41861a0d009e1bd':'Afbeelding invoegen; geen exportopdracht.',
 '30e196bc32898f9c':'Feedback openen; verkeerd bij opslaan gegroepeerd.',
 '32aa70772556335b':'Een kamer splitsen is geen klembord-knipopdracht.',
 '1d6fc1ce6b1ce7c5':'Direct dupliceren; apart van kopiëren naar het klembord.',
 '2441ef471ee21567':'Venster herstellen/maximaliseren; geen kopieeropdracht.',
 '208026e879fb81ea':'Selectiegereedschap activeren; geen alles-selecteren-opdracht.',
 '97f9f80540eb01f1':'Sonderingenpaneel openen; geen selectiegereedschap.',
 '557ba88b42e736a9':'Woningtype; geen startpagina.',
 '078822babeb8756d':'Dak/bouwdelen; geen startpagina.',
 'bbdfc78cf6b7ecab':'Ruimtes; geen startpagina.',
 'cb92de9a3d2a3547':'Projectroute; niet zonder beoordeling naar startpagina omzetten.',
 '7ba47aad8fc33b84':'Feedback naar ontwikkelaar; geen documentannotatie.',
}
DEFINITIONS+=SECOND_DEFINITIONS+WINDOW_DEFINITIONS+TEXT_DEFINITIONS+DATA_DEFINITIONS+REPORT_DEFINITIONS+IFC_DEFINITIONS+NEXT_DEFINITIONS+LATER_DEFINITIONS+PAGE_DEFINITIONS+BULK_DEFINITIONS+SESSION_DEFINITIONS+NAV_DEFINITIONS+THIRD_DEFINITIONS+FOURTH_DEFINITIONS+COMPLETION_DEFINITIONS
EXAMPLES.update(SECOND_EXAMPLES)
EXAMPLES.update(WINDOW_EXAMPLES)
EXAMPLES.update(TEXT_EXAMPLES)
EXAMPLES.update(DATA_EXAMPLES)
EXAMPLES.update(REPORT_EXAMPLES)
EXAMPLES.update(IFC_EXAMPLES)
EXAMPLES.update(NEXT_EXAMPLES)
EXAMPLES.update(LATER_EXAMPLES)
EXAMPLES.update(PAGE_EXAMPLES)
EXAMPLES.update(BULK_EXAMPLES)
EXAMPLES.update(SESSION_EXAMPLES)
EXAMPLES.update(NAV_EXAMPLES)
EXAMPLES.update(THIRD_EXAMPLES)
EXAMPLES.update(FOURTH_EXAMPLES)
EXAMPLES.update(COMPLETION_EXAMPLES)
ISSUES.update(SECOND_ISSUES)
ISSUES.update(TEXT_ISSUES)
ISSUES.update(DATA_ISSUES)
ISSUES.update(REPORT_ISSUES)
ISSUES.update(IFC_ISSUES)
ISSUES.update(NEXT_ISSUES)
ISSUES.update(LATER_ISSUES)
ISSUES.update(THIRD_ISSUES)
ISSUES.update(FOURTH_ISSUES)
RESOLVED_ISSUES={k:v for k,v in ISSUES.items() if k in set(COMPLETION_EXAMPLES.values())|set(COMPLETION_REUSED)|set(COMPLETION_DISPATCHERS)|set(COMPLETION_EXCLUDED)}
ISSUES={k:v for k,v in ISSUES.items() if k not in RESOLVED_ISSUES}


def digest(data):return hashlib.sha256(data).hexdigest()


def stable_model(value):
    if isinstance(value,float):return round(value,11)
    if isinstance(value,(list,tuple)):return [stable_model(v) for v in value]
    if isinstance(value,dict):return {k:stable_model(v) for k,v in value.items()}
    return value


def main():
    OUT.mkdir(parents=True,exist_ok=True);AUDIT.mkdir(parents=True,exist_ok=True)
    catalog=load_catalog()
    tokens=json.loads(TOKENS.read_text(encoding='utf-8'))
    by_id={r['id']:r for r in catalog['records']}
    scope_audit=validate_scope_audit(COMPLETION_EXCLUDED,{r[0] for r in DEFINITIONS},PLANNED,PLANNED_KEYS)
    clusters={f['id']:f for f in catalog['functions']}
    previous=json.loads((OUT/'manifest.json').read_text(encoding='utf-8')) if (OUT/'manifest.json').exists() else {'icons':[]}
    retained={i['id']:i for i in previous['icons'] }
    previous_geometry={(i['id'],i['master']):i for i in json.loads((OUT/'geometry-validation.json').read_text())} if (OUT/'geometry-validation.json').exists() else {}
    records=[];entries=[];geometry=[]
    for key,label,group,meaning in DEFINITIONS:
        example=by_id[EXAMPLES[key]] if key in EXAMPLES else None
        source_key=SOURCE_FUNCTIONS.get(key,key)
        if example:assert example['function_id']==source_key
        entry={'id':key,'label':label,'group':group,'meaning':meaning,
               'status':'gepland ontwerp; bronbediening nog niet aangesloten' if key in PLANNED_KEYS else 'B2-ontwerp beschikbaar; nog geen app-integratie',
               'planned':key in PLANNED_KEYS,
               'source_support':BASIS_SOURCES.get(key),
               'evidence_status':BASIS_SOURCES[key]['description'] if key in BASIS_SOURCES else EVIDENCE.get(key,'bronaanroep beoordeeld als voorbeeld' if example else 'ontwerpcontract; geen bevestigde bronaanroep'),
               'source_function_id':source_key,
               'candidate_apps':clusters.get(source_key,{}).get('apps',[]),
               'candidate_records':clusters.get(source_key,{}).get('occurrences',0),
               'source_example':example,'assets':{},'construction':{},
               'foreground':foreground(key),'layer_reason':layer_reason(key),
               'paint_order':['primary','accent'] if foreground(key)=='accent' else ['accent','primary'],
               'shape_revision':SHAPE_REVISIONS.get(key),'rounded_joint':key in ROUNDED_JOINTS,
               'series':COMPLETION_SERIES[key] if key in COMPLETION_SERIES else FOURTH_SERIES[key] if key in FOURTH_SERIES else THIRD_SERIES[key] if key in THIRD_SERIES else NAV_SERIES[key] if key in NAV_SERIES else SESSION_SERIES[key] if key in SESSION_SERIES else BULK_SERIES[key] if key in BULK_SERIES else 14 if key in PAGE_KEYS else LATER_SERIES[key] if key in LATER_SERIES else NEXT_SERIES[key] if key in NEXT_SERIES else 7 if key in IFC_KEYS else 6 if key in REPORT_KEYS else 5 if key in DATA_KEYS else 4 if key in TEXT_KEYS else 3 if key in WINDOW_KEYS else 2 if key in SECOND_KEYS else 1,'semantic_color':SEMANTIC.get(key),
               'whole_icon_accent':key in WHOLE_ACCENT,'typography':FONT_METADATA.get(key)}
        for size in (16,24):
            model=construction(key,size)
            model_data={'width':model.width,'paths':model.paths,'circles':model.circles,'fills':model.fills,'clear_primary':model.clear_primary}
            old=retained.get(key)
            cached_path=OUT/old['assets'][str(size)]['path'] if old else None
            # Retain the reviewed batches only when both model and verified bytes agree.
            reusable=(old and old['foreground']==entry['foreground'] and old.get('whole_icon_accent',False)==entry['whole_icon_accent'] and
                stable_model(model_data)==stable_model(old['construction'][str(size)]) and
                (key,size) in previous_geometry and cached_path.exists() and
                digest(cached_path.read_bytes())==old['assets'][str(size)]['sha256'])
            content=cached_path.read_text(encoding='utf-8') if reusable else export_svg(model)
            path=OUT/'svg'/str(size)/(key+'.svg');path.parent.mkdir(parents=True,exist_ok=True)
            before=OUT/'review/layers-before'/str(size)/(key+'.svg')
            if path.exists() and not before.exists():
                before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(path.read_bytes())
            path.write_text(content,encoding='utf-8')
            entry['assets'][str(size)]={'path':path.relative_to(OUT).as_posix(),'sha256':digest(content.encode())}
            entry['construction'][str(size)]=old['construction'][str(size)] if reusable else model_data
            if reusable:
                geometry.append(previous_geometry[(key,size)])
                continue
            g=model.geometry()
            geometry.append({'id':key,'master':size,'bounds':g['primary'].union(g['accent']).bounds,
                             'overlap_area':g['primary'].intersection(g['accent']).area,
                             'accent_area':g['accent'].area})
        entries.append(entry)
    keys={e['id'] for e in entries}
    canonical={SOURCE_FUNCTIONS.get(k,k):k for k in sorted(keys)}
    canonical.update({by_id[r]['function_id']:target for r,(target,_) in REUSED.items()})
    canonical_lists={source:sorted(k for k in keys if SOURCE_FUNCTIONS.get(k,k)==source) for source in canonical}
    for record,(target,_) in REUSED.items():
        source=by_id[record]['function_id']
        canonical_lists[source]=sorted(set(canonical_lists.get(source,[])+[target]))
    for record,targets in COMPLETION_DISPATCHERS.items():
        source=by_id[record]['function_id']
        canonical_lists[source]=sorted(set(canonical_lists.get(source,[]))|set(targets))
    example_targets={record:key for key,record in EXAMPLES.items()}
    for r in catalog['records']:
        assessment='nog te beoordelen';reason='Naam-/labelcluster is geen definitieve functietoewijzing.'
        if r['id'] in COMPLETION_DISPATCHERS:assessment='typeafhankelijk hergebruik';reason=COMPLETION_DISPATCH_EVIDENCE[r['id']]
        elif r['id'] in PLANNED:assessment='gepland ontwerp; bronbediening ontbreekt';reason=PLANNED[r['id']]+' Oorspronkelijk runtimebesluit: '+COMPLETION_EXCLUDED.get(r['id'],'geen uitvoering bewezen')
        elif r['id'] in COMPLETION_EXCLUDED:assessment='buiten vaste UI-set';reason=COMPLETION_EXCLUDED[r['id']]
        elif r['id'] in ISSUES:assessment='niet samenvoegen';reason=ISSUES[r['id']]
        elif r['id'] in REUSED:
            assessment='bestaand B2-ontwerp hergebruiken';reason=REUSED[r['id']][1]
        elif r['id'] in EXAMPLES.values():
            assessment='bronvoorbeeld beoordeeld';reason='Concrete aanroep gelezen; ondersteunt het beschreven functiecontract, geen bewijs van runtime-adoptie.'
        records.append({'record_id':r['id'],'candidate_function':r['function_id'],
                        'assessment':assessment,'reason':reason,'source_url':r['source_url'],
                        'resolved_prior_conflict':RESOLVED_ISSUES.get(r['id']),
                        'canonical_function':REUSED[r['id']][0] if r['id'] in REUSED else example_targets.get(r['id']),
                        'canonical_functions':list(COMPLETION_DISPATCHERS[r['id']]) if r['id'] in COMPLETION_DISPATCHERS else [REUSED[r['id']][0]] if r['id'] in REUSED else sorted(k for k,v in EXAMPLES.items() if v==r['id'])})
    assessed_records={r['record_id']:r for r in records}
    queue=[]
    for f in catalog['functions']:
        targets=canonical_lists.get(f['id'],[])
        pending=sum(assessed_records[rid]['assessment'] in {'nog te beoordelen','niet samenvoegen'} for rid in f['record_ids'])
        if pending:status=f"{pending} bronplaatsen nog af te handelen"+('; ontwerp beschikbaar' if targets else '')
        elif targets:status='alle bronplaatsen afgehandeld; B2-ontwerp beschikbaar'
        else:status='alle bronplaatsen afgehandeld; buiten vaste UI-set'
        queue.append({**f,'canonical_function':canonical.get(f['id']),
                      'canonical_functions':targets,'design_status':status,
                      'mapping_status':'afzonderlijke bronbesluiten; geen automatische naamskoppeling',
                      'remaining_source_records':pending})
    manifest={'family':'OpenAEC B2','revision':86,'status':'ontwerpuitwerking; niet in Rust-crate of apps ingebouwd',
              'function_count':len(entries),'svg_count':2*len(entries),'masters':[16,24],
              'paint_order':'per icoon vastgelegd','export':'gevulde contouren; achterste kleur minus voorste kleur',
              'curve_sampling':'12 stappen per halve kwadratische hoek; buffer 20 segmenten per kwadrant; cirkels 64',
              'scope_audit_sha256':audit_hash(),'basis_sources_sha256':digest(BASIS_PATH.read_bytes()),'source_catalog_sha256':digest(CATALOG.read_bytes()),'source_catalogs_sha256':source_hashes(),'theme_tokens_sha256':digest(TOKENS.read_bytes()),
              'generator_sha256':digest(Path(__file__).read_bytes()),
              'geometry_generator_sha256':digest((ROOT/'scripts/b2_geometry.py').read_bytes()),
              'font_generator_sha256':digest((ROOT/'scripts/b2_font_geometry.py').read_bytes()),
              'font_sources':FONT_METADATA,'license_files':['licenses/SpaceGrotesk-OFL.txt'],
              'completion_generator_sha256':digest((ROOT/'scripts/b2_completion.py').read_bytes()),
              'completion_modules_sha256':{name:digest((ROOT/'scripts'/name).read_bytes()) for name in ['b2_completion.py','b2_workspace_completion.py','b2_reports_completion.py','b2_bim_completion.py','b2_frame_completion.py','b2_pointcloud_completion.py','b2_energy_completion.py','b2_heatloss_completion.py','b2_pile_completion.py','b2_geotech_completion.py','b2_calc_completion.py','b2_calculations_completion.py','b2_pdf_catalog_completion.py','b2_pdf_controls_completion.py','b2_pdf_editing_completion.py','b2_pdf_final_completion.py','b2_planner_ribbon_completion.py','b2_planner_choices_completion.py','b2_planner_safety_completion.py','b2_planner_dialogs_completion.py','b2_planner_panels_completion.py','b2_planner_final_completion.py','b2_scope_completion.py','b2_scope_audit.py','b2_source_catalog.py','build_b2_supplemental_sources.py','build_b2_coverage_review.py']},
              'session_four_generator_sha256':digest((ROOT/'scripts/b2_session_four.py').read_bytes()),
              'session_three_generator_sha256':digest((ROOT/'scripts/b2_session_three.py').read_bytes()),
              'document_navigation_generator_sha256':digest((ROOT/'scripts/b2_document_navigation.py').read_bytes()),
              'session_two_generator_sha256':digest((ROOT/'scripts/b2_session_two.py').read_bytes()),
              'bulk_generator_sha256':digest((ROOT/'scripts/b2_bulk_series.py').read_bytes()),
              'page_views_generator_sha256':digest((ROOT/'scripts/b2_page_views.py').read_bytes()),
              'later_groups_generator_sha256':digest((ROOT/'scripts/b2_energy_pile_audio.py').read_bytes()),
              'next_groups_generator_sha256':digest((ROOT/'scripts/b2_tree_planning_geo.py').read_bytes()),
              'ifc_generator_sha256':digest((ROOT/'scripts/b2_ifc_series.py').read_bytes()),
              'report_generator_sha256':digest((ROOT/'scripts/b2_report_series.py').read_bytes()),
              'data_generator_sha256':digest((ROOT/'scripts/b2_data_series.py').read_bytes()),
              'text_generator_sha256':digest((ROOT/'scripts/b2_text_series.py').read_bytes()),
              'window_generator_sha256':digest((ROOT/'scripts/b2_window_series.py').read_bytes()),
              'extension_generator_sha256':digest((ROOT/'scripts/b2_second_series.py').read_bytes()),
              'feedback_generator_sha256':digest((ROOT/'scripts/build_b2_feedback_review.py').read_bytes()),
              'warning_preview':{'status':'gele warning-rol uit tokens-0.4.json','colors':WARNING_PREVIEW},
              'limits':['Bronplaatsen afzonderlijk beoordeeld op de gepinde versies; kandidaat-apps zijn geen runtime-adopties.',
                        'FEM-bron ontbreekt; runtime-extensies blijven buiten volledige dekking.',
                        'Bronillustraties en symbolen worden niet automatisch onderdeel van de UI-iconenset.',
                        '16px gebruikt eigen lijndikte en waar nodig minder details; verdere optische verfijning blijft mogelijk.'],
              'icons':entries}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'geometry-validation.json').write_text(json.dumps(geometry,indent=2),encoding='utf-8')
    new_contracts=[{'id':e['id'],'label':e['label'],'category':e['group'],'apps':[],
                    'occurrences':0,'design_status':'nieuw ontwerpcontract; geen broncluster',
                    'mapping_status':'toegevoegd voor componenten 2.4'} for e in entries if e['source_function_id'] not in clusters]
    audit={'source':CATALOG.relative_to(ROOT).as_posix(),'source_sha256':manifest['source_catalog_sha256'],
           'source_catalogs_sha256':manifest['source_catalogs_sha256'],'supplemental_source':SUPPLEMENT.relative_to(ROOT).as_posix(),
           'new_contracts':new_contracts,
           'clusters':queue,'record_assessments':records,'scope':catalog['scope'],'limits':manifest['limits']}
    from build_b2_coverage_review import render_coverage
    render_coverage(OUT,manifest,catalog,audit)
    render_scope_review(OUT)
    (AUDIT/'function-plan.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    with (AUDIT/'function-list.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['functie','label','groep','status','bronrecords','kandidaat_apps'])
        for q in queue:writer.writerow([q['id'],q['label'],q['category'],q['design_status'],q['occurrences'],'; '.join(q['apps'])])
        for q in new_contracts:writer.writerow([q['id'],q['label'],q['category'],q['design_status'],0,''])
    payload=[]
    for e in entries:
        payload.append({**{k:v for k,v in e.items() if k!='construction'},
                        'svg':{str(s):(OUT/e['assets'][str(s)]['path']).read_text(encoding='utf-8') for s in (16,24)}})
    data={'icons':payload,'queue':queue+new_contracts,'issues':[{**by_id[k],'finding':v} for k,v in ISSUES.items() if k in by_id],
          'themes':tokens['themes'],'warning_preview':WARNING_PREVIEW,'total_records':len(records),
          'assessed':sum(r['assessment']!='nog te beoordelen' for r in records)}
    page=PAGE.replace('/* DATA */',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (OUT/'index.html').write_text(page,encoding='utf-8')
    bulk_batches=','.join(str(b) for b in AVAILABLE_SERIES)
    bulk_count=len(BULK_DEFINITIONS)
    bulk=page.replace('theme();render();',f'theme();$("#batch").value="{bulk_batches}";render();')
    links=' · '.join(f'<a href="series-{b}.html">{BULK_GROUPS[b]} ({sum(v==b for v in BULK_SERIES.values())})</a>' for b in AVAILABLE_SERIES)
    bulk=bulk.replace('</h1>',f'</h1><div class="note"><b>Nieuwe reviewronde: {bulk_count} iconen klaar.</b><p>{links}</p><label><input type="checkbox" id="live-update" checked> Nieuwe groepen automatisch laden</label><p>Controle op aanvullingen elke 15 seconden. Filters en leespositie blijven bewaard. Serie 14 is goedgekeurd.</p></div>',1)
    live="""<script>
const reviewRevision=__REVISION__;
const savedReview=sessionStorage.getItem('b2-bulk-view');
if(savedReview){try{const q=JSON.parse(savedReview);for(const id of ['theme','group','search','batch']){const el=document.getElementById(id);if(el&&q[id]!==undefined&&(el.tagName!=='SELECT'||[...el.options].some(o=>o.value===q[id])))el.value=q[id]}theme();render();document.getElementById('mono').checked=q.mono;document.body.classList.toggle('mono',q.mono);requestAnimationFrame(()=>scrollTo(0,q.scroll||0));}catch(e){}sessionStorage.removeItem('b2-bulk-view');}
setInterval(async()=>{if(!document.getElementById('live-update').checked)return;try{const r=await fetch('manifest.json',{cache:'no-store'});if(!r.ok)return;const m=await r.json();if(m.revision!==reviewRevision){const q={scroll:scrollY,mono:document.getElementById('mono').checked};for(const id of ['theme','group','search','batch'])q[id]=document.getElementById(id).value;if(q.batch===__BATCHES__)delete q.batch;sessionStorage.setItem('b2-bulk-view',JSON.stringify(q));location.reload();}}catch(e){}},15000);
</script>""".replace('__REVISION__',str(manifest['revision'])).replace('__BATCHES__',json.dumps(bulk_batches))
    intro_start=bulk.index('<p>Ronde vormen,')
    intro_end=bulk.index('<div class="stats">',intro_start)
    bulk=bulk[:intro_start]+'<p>Nieuwe B2-ontwerpen ter beoordeling op 16, 24 en 32 px. Kies hieronder een serie of bekijk alles samen.</p>'+bulk[intro_end:]
    bulk=bulk.replace('const groups=[...new Set(d.icons.map(i=>i.group))];','const groups=[...new Set([...d.icons.filter(i=>i.series>=15),...d.icons].map(i=>i.group))];')
    bulk=bulk.replace('</html>',live+'</html>')
    next_batches=','.join(map(str,SESSION_AVAILABLE))
    next_links=' · '.join(f'<a href="series-{b}.html">{SESSION_GROUPS[b]} ({sum(v==b for v in SESSION_SERIES.values())})</a>' for b in SESSION_AVAILABLE)
    next_bulk=bulk.replace(f'.value="{bulk_batches}";render();',f'.value="{next_batches}";render();').replace('q.batch==='+json.dumps(bulk_batches),'q.batch==='+json.dumps(next_batches)).replace('b2-bulk-view','b2-session-two-view')
    next_bulk=next_bulk.replace(f'Nieuwe reviewronde: {bulk_count} iconen klaar.',f'Tweede grote reviewronde: {len(SESSION_DEFINITIONS)} iconen klaar.')
    next_bulk=next_bulk.replace(links,next_links).replace('Serie 14 is goedgekeurd.','Series 15–20 zijn goedgekeurd.')
    next_bulk=next_bulk.replace('filter(i=>i.series>=15)','filter(i=>i.series>=21)')
    (OUT/'bulk-review-2.html').write_text(next_bulk,encoding='utf-8')
    nav_batches=','.join(map(str,NAV_AVAILABLE))
    nav_links=' · '.join(f'<a href="series-{b}.html">{NAV_GROUPS[b]} ({sum(v==b for v in NAV_SERIES.values())})</a>' for b in NAV_AVAILABLE)
    nav_bulk=bulk.replace(f'.value="{bulk_batches}";render();',f'.value="{nav_batches}";render();').replace('q.batch==='+json.dumps(bulk_batches),'q.batch==='+json.dumps(nav_batches)).replace('b2-bulk-view','b2-document-navigation-view')
    nav_bulk=nav_bulk.replace(f'Nieuwe reviewronde: {bulk_count} iconen klaar.',f'Bladwijzers en bijlagen: {len(NAV_DEFINITIONS)} nieuwe iconen klaar.')
    nav_bulk=nav_bulk.replace(links,nav_links).replace('Serie 14 is goedgekeurd.','De eerdere 231 ontwerpen blijven behouden.')
    nav_bulk=nav_bulk.replace('filter(i=>i.series>=15)','filter(i=>i.series>=29)')
    (OUT/'bulk-review-3.html').write_text(nav_bulk,encoding='utf-8')
    third_batches=','.join(map(str,THIRD_AVAILABLE))
    third_links=' · '.join(f'<a href="series-{b}.html">{THIRD_GROUPS[b]} ({sum(v==b for v in THIRD_SERIES.values())})</a>' for b in THIRD_AVAILABLE)
    third_bulk=bulk.replace(f'.value="{bulk_batches}";render();',f'.value="{third_batches}";render();').replace('q.batch==='+json.dumps(bulk_batches),'q.batch==='+json.dumps(third_batches)).replace('b2-bulk-view','b2-session-three-view')
    third_bulk=third_bulk.replace(f'Nieuwe reviewronde: {bulk_count} iconen klaar.',f'Grote vervolglijst: {len(THIRD_DEFINITIONS)} nieuwe iconen klaar.')
    third_bulk=third_bulk.replace(links,third_links).replace('Serie 14 is goedgekeurd.','De eerdere 239 ontwerpen blijven behouden.')
    third_bulk=third_bulk.replace('filter(i=>i.series>=15)','filter(i=>i.series>=31)')
    (OUT/'bulk-review-4.html').write_text(third_bulk,encoding='utf-8')
    fourth_batches=','.join(map(str,FOURTH_AVAILABLE))
    fourth_links=' · '.join(f'<a href="series-{b}.html">{FOURTH_GROUPS[b]} ({sum(v==b for v in FOURTH_SERIES.values())})</a>' for b in FOURTH_AVAILABLE)
    fourth_bulk=bulk.replace(f'.value="{bulk_batches}";render();',f'.value="{fourth_batches}";render();').replace('q.batch==='+json.dumps(bulk_batches),'q.batch==='+json.dumps(fourth_batches)).replace('b2-bulk-view','b2-session-four-view')
    fourth_bulk=fourth_bulk.replace(f'Nieuwe reviewronde: {bulk_count} iconen klaar.',f'Volgende reeks: {len(FOURTH_DEFINITIONS)} nieuwe iconen klaar.')
    fourth_bulk=fourth_bulk.replace(links,fourth_links).replace('Serie 14 is goedgekeurd.','De eerdere 276 ontwerpen blijven behouden. Formuliersymbolen zijn typeaanduidingen; dockingsymbolen zijn sleepdoelen.')
    fourth_bulk=fourth_bulk.replace('filter(i=>i.series>=15)','filter(i=>i.series>=39)')
    (OUT/'bulk-review-5.html').write_text(fourth_bulk,encoding='utf-8')
    completion_batches=','.join(map(str,COMPLETION_AVAILABLE))
    completion=bulk.replace(f'.value="{bulk_batches}";render();',f'.value="{completion_batches}";render();').replace('q.batch==='+json.dumps(bulk_batches),'q.batch==='+json.dumps(completion_batches)).replace('b2-bulk-view','b2-completion-view')
    completion=completion.replace(f'Nieuwe reviewronde: {bulk_count} iconen klaar.',f'Nachtelijke uitbreiding: {len(COMPLETION_DEFINITIONS)} ontwerpen klaar voor beoordeling.')
    completion_links=' · '.join(f'<a href="series-{b}.html">{COMPLETION_GROUPS[b]} ({sum(v==b for v in COMPLETION_SERIES.values())})</a>' for b in COMPLETION_AVAILABLE)
    completion=completion.replace(links,completion_links).replace('Serie 14 is goedgekeurd.','De oorspronkelijke 316 ontwerpen blijven bytegelijk behouden; alle aanvullingen wachten op beoordeling.')
    completion=completion.replace('filter(i=>i.series>=15)','filter(i=>i.series>=46)')
    (OUT/'completion-review.html').write_text(completion,encoding='utf-8')



    bulk=bulk.replace('Serie 14 is goedgekeurd.','Deze ronde is goedgekeurd. <a href="bulk-review-2.html">Open de volgende grote reviewronde</a>.')
    (OUT/'bulk-review.html').write_text(bulk,encoding='utf-8')

    (OUT/'series-2.html').write_text(page.replace('theme();render();','theme();$("#batch").value="2";render();'),encoding='utf-8')
    (OUT/'series-3.html').write_text(page.replace('theme();render();','theme();$("#batch").value="3";render();'),encoding='utf-8')
    (OUT/'series-4.html').write_text(page.replace('theme();render();','theme();$("#batch").value="4";render();'),encoding='utf-8')
    (OUT/'series-5.html').write_text(page.replace('theme();render();','theme();$("#batch").value="5";render();'),encoding='utf-8')
    for batch in (8,9,10,11,12,13,14,*ALL_AVAILABLE):
        (OUT/f'series-{batch}.html').write_text(page.replace('theme();render();',f'theme();$("#batch").value="{batch}";render();'),encoding='utf-8')
    combined=page.replace('theme();render();','theme();$("#batch").value="8,9,10";render();')
    combined=combined.replace('</h1>','</h1><p><b>Drie nieuwe groepen: 13 ontwerpen.</b> <a href="series-8.html">Lijsten en bomen (2)</a> · <a href="series-9.html">Planning (7)</a> · <a href="series-10.html">Geotechniek (4)</a>. Taakaantekeningen gebruiken Opmerking; GeoJSON-export gebruikt Exporteren. Verkeerd ingedeelde plattegrond-/meshfuncties en appillustraties zijn apart gezet.</p>',1)
    (OUT/'next-three.html').write_text(combined,encoding='utf-8')
    later=page.replace('theme();render();','theme();$("#batch").value="11,12,13";render();')
    later=later.replace('</h1>','</h1><p><b>Drie volgende groepen: 15 ontwerpen.</b> <a href="series-11.html">Energie en warmte (3)</a> · <a href="series-12.html">Paalplan (7)</a> · <a href="series-13.html">Spraak en audio (5)</a>. Bepalende relatie is nu geheel in accentkleur. Bestaande iconen voor dupliceren, verwijderen, openen, waarschuwing en ongedaan/opnieuw zijn hergebruikt.</p>',1)
    (OUT/'next-three-2.html').write_text(later,encoding='utf-8')
    (OUT/'series-7.html').write_text(page.replace('theme();render();','theme();$("#batch").value="7";render();'),encoding='utf-8')
    (OUT/'series-6.html').write_text(page.replace('theme();render();','theme();$("#batch").value="6";render();'),encoding='utf-8')
    render_feedback_review(OUT,entries,tokens['themes'])
    from build_b2_layer_review import render_layer_review
    render_layer_review(OUT,entries,tokens['themes'])
    (OUT/'licenses').mkdir(exist_ok=True)
    license_source=ROOT/'crates/openaec-ui/licenses/SpaceGrotesk-OFL.txt'
    license_target=OUT/'licenses/SpaceGrotesk-OFL.txt'
    if not license_target.exists() or license_target.read_text()!=license_source.read_text():
        shutil.copyfile(license_source,license_target)
    with zipfile.ZipFile(OUT/'openaec-b2-first-family.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted((OUT/'svg').rglob('*.svg')):z.write(path,path.relative_to(OUT))
        for license_path in manifest['license_files']:z.write(OUT/license_path,license_path)
        z.write(OUT/'manifest.json','manifest.json');z.write(OUT/'geometry-validation.json','geometry-validation.json')
    print(json.dumps({'functions':len(entries),'svg_files':2*len(entries),'source_clusters':len(queue),
                      'assessed_source_records':data['assessed'],'issues':len(ISSUES)}))


PAGE=r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC B2 · eerste iconenfamilie</title><style>
@font-face{font-family:Inter;src:url('../assets/fonts/Inter-Regular.ttf')}*{box-sizing:border-box}body{margin:0;font:14px/1.5 Inter,system-ui;background:var(--bg);color:var(--ink)}:root{--bg:#2a2a32;--panel:#33333c;--ink:#edebe8;--muted:#bebdbd;--line:#878689;--icon-accent:#d97706;color-scheme:dark}main{max-width:1500px;padding:32px;margin:auto}h1{font-size:32px;letter-spacing:-.04em;margin:12px 0}h2{font-size:20px;margin:30px 0 16px}h3{font-size:14px;margin:0}p{color:var(--muted);max-width:930px}a{color:var(--ink)}.eyebrow{font-size:11px;letter-spacing:.13em;color:var(--icon-accent)}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}.stats span{border:1px solid var(--line);padding:6px 12px;border-radius:20px;font-size:12px}.controls{position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 0;display:flex;gap:14px;flex-wrap:wrap;align-items:center}select,input,button{font:inherit}select,input[type=search]{padding:8px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink)}input[type=search]{width:230px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}.card{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:18px;min-width:0}.hero{height:84px;display:flex;align-items:center;justify-content:center}.hero svg{width:58px;height:58px}.native{display:flex;justify-content:center;align-items:flex-end;gap:25px;height:70px;margin-bottom:16px}.native>div{display:flex;flex-direction:column;align-items:center;gap:7px;color:var(--muted);font-size:10px}.native svg{color:var(--ink)}code{font-size:11px;color:var(--muted)}details{font-size:12px;margin-top:12px}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:11px/1.4 monospace;max-height:180px;overflow:auto}details p{font-size:12px}table{width:100%;border-collapse:collapse;font-size:12px}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}th{position:sticky;top:70px;background:var(--bg)}.tablewrap{overflow:auto}.note{padding:16px;border:1px solid var(--line);border-radius:10px;margin:20px 0}.mono{--icon-accent:currentColor!important}.hidden{display:none!important}.tabs{display:flex;gap:20px;border-bottom:1px solid var(--line);padding:12px 0}.tabs button{border:0;background:none;color:var(--muted);padding:8px;cursor:pointer}.tabs button.active{color:var(--ink);border-bottom:3px solid var(--icon-accent)}.issue{border-left:3px solid var(--icon-accent);padding:12px 18px;margin:12px 0;background:var(--panel)}.empty{padding:30px}footer{margin-top:30px;border-top:1px solid var(--line);padding-top:20px;color:var(--muted);font-size:12px}.hint{font-size:12px}@media(max-width:650px){main{padding:18px}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:12px}.native{gap:12px}h1{font-size:26px}.controls{gap:8px}}
</style><main><div class="eyebrow">OPENAEC / B2 / EERSTE FAMILIE</div><h1>Een vaste vorm voor dezelfde functie</h1><p>Ronde vormen, betekenisvolle accenten en de hoofdkleur bovenop. De eerste serie bevat 31 functies. Dit is ontwerpwerk voor de nieuwe familie; de bestaande apps gebruiken deze iconen nog niet.</p><div class="stats"><span>31 functies · 62 SVG-masters</span><span>16 / 24 / 32 px</span><span>5 productiethema’s</span><span>1.487 bronclusters in de werklijst</span></div><div class="controls"><label>Thema <select id="theme"></select></label><label>Groep <select id="group"><option value="">Alle groepen</option></select></label><input id="search" type="search" aria-label="Zoek functie" placeholder="Zoek functie, app of naam…"><label><input type="checkbox" id="mono"> Eén kleur</label><label>Eigen accent <input type="color" id="accent" value="#d97706"></label></div><div class="tabs"><button class="active" data-tab="icons">Iconen</button><button data-tab="queue">Functielijst & dekking</button><button data-tab="issues">Betekenisconflicten</button></div><section id="icons"><div id="icon-content"></div></section><section id="queue" class="hidden"><div class="note"><b>Een werklijst, nog geen definitieve telling van iconen.</b><p id="coverage"></p><p>Voor elk broncluster blijven de oorspronkelijke bronnen en kandidaat-apps behouden. Alleen benoemde bronvoorbeelden zijn beoordeeld. Gelijke namen, vormen of bibliotheekiconen geven geen automatische goedkeuring.</p><a href="../../harmonization/icon-set-b2/function-list.csv">CSV-functielijst</a> · <a href="../../harmonization/icon-set-b2/function-plan.json">Alle bronbeoordelingen (JSON)</a></div><p id="queue-count"></p><div class="tablewrap"><table><thead><tr><th>Functiekandidaat</th><th>Groep</th><th>Kandidaat-apps</th><th>Bronnen</th><th>Ontwerpstatus</th></tr></thead><tbody id="queue-rows"></tbody></table></div></section><section id="issues" class="hidden"><h2>Deze betekenissen voegen we niet automatisch samen</h2><p>Concrete afwijkingen uit de broncontext. Het oorspronkelijke icoon en de huidige apps zijn niet gewijzigd.</p><div id="issue-content"></div></section><footer><a href="openaec-b2-first-family.zip">Download 62 SVG’s + manifest</a> · <a href="manifest.json">Constructiemodellen, bronvoorbeelden en hashes</a> · <a href="geometry-validation.json">Geometriecontrole</a> · <a href="../function-icon-catalog.html">Volledige broninventaris</a><p>SVG-gebruik: hoofdkleur via <code>color</code>, accent via <code>--icon-accent</code>. Zonder accentvariabele valt het icoon terug op één kleur. 32 px gebruikt de 24px-master. Geef bediening een vertaalbaar label; markeer decoratieve SVG’s met <code>aria-hidden="true"</code>. Status en gevaar worden door label/toestand bepaald, niet door het amber accent. Eigen kleuren zijn vrij instelbaar; de contrastcontrole betreft alleen de vijf vaste paletten.</p><p>Eigen iconengeometrie; B/I/U/A bij Tekstopmaak zijn vectorcontouren uit de gebundelde Space Grotesk-fonts (SIL OFL 1.1), met bronhashes in het manifest en licentie in de ZIP. Externe appiconen dienen alleen als functionele bron. Veelhoekbenadering van de curven heeft een vaste resolutie. FEM-bron en dynamische extensies blijven dekkingsgrenzen. Geen Rust- of app-integratie in deze uitwerking.</p></footer></main><script id="data" type="application/json">/* DATA */</script><script>
const d=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));$('#theme').innerHTML=Object.entries(d.themes).map(([k,v])=>`<option value="${k}">${esc(v.name)}</option>`).join('');$('#theme').value='dark';const groups=[...new Set(d.icons.map(i=>i.group))];$('#group').innerHTML+=groups.map(g=>`<option>${g}</option>`).join('');function theme(){let t=d.themes[$('#theme').value],c=t.color,r=document.documentElement;r.style.colorScheme=t.kind;for(let [k,v] of Object.entries({bg:c.frame,panel:c.panel,ink:c.text,muted:c['text-secondary'],line:c['border-strong'],'icon-accent':c.accent}))r.style.setProperty('--'+k,v);$('#accent').value=c.accent}function resized(s,n){return s.replace(/width="\d+"/,`width="${n}"`).replace(/height="\d+"/,`height="${n}"`)}function matches(s){return s.toLowerCase().includes($('#search').value.toLowerCase())}function render(){const g=$('#group').value;let icons=d.icons.filter(i=>(!g||i.group===g)&&matches(i.id+' '+i.label+' '+i.meaning+' '+i.candidate_apps.join(' ')));$('#icon-content').innerHTML=groups.filter(a=>icons.some(i=>i.group===a)).map(a=>`<h2>${a}</h2><div class="grid">${icons.filter(i=>i.group===a).map(i=>`<article class="card"><h3>${esc(i.label)}</h3>${i.planned?'<small>GEPLAND · bronbediening niet aangesloten</small>':''}<code>${i.id}</code><div class="hero">${i.svg[24]}</div><div class="native">${[16,24,32].map(n=>`<div>${resized(i.svg[n===16?16:24],n)}<span>${n} px</span></div>`).join('')}</div><details><summary>Functie en bron</summary><p>${esc(i.meaning)}</p><p>${esc(i.evidence_status)}</p>${i.source_example?`<a href="${esc(i.source_example.source_url)}" target="_blank" rel="noopener">${esc(i.source_example.app)} · ${esc(i.source_example.path)}:${i.source_example.line}</a><pre>${esc(i.source_example.context)}</pre>`:(i.source_support?'<p>'+esc(i.source_support.description)+'</p>'+i.source_support.sources.map(s=>'<p><a href="'+esc(s.url)+'" target="_blank" rel="noopener">'+esc(s.repository)+' · '+esc(s.path)+':'+s.line+'</a><br>'+esc(s.description)+'</p>').join(''):'<p>Bewust ontwerpcontract; de bestaande cluster levert nog geen overtuigend bronvoorbeeld.</p>')}<a href="${i.assets[16].path}" download>16px SVG</a> · <a href="${i.assets[24].path}" download>24px SVG</a></details></article>`).join('')}</div>`).join('')||'<p class="empty">Geen iconen met dit filter.</p>';let queue=d.queue.filter(f=>matches(f.id+' '+f.label+' '+f.category+' '+f.apps.join(' '))&&(!g||d.icons.some(i=>(f.canonical_functions?.length?f.canonical_functions:[f.canonical_function||f.id]).includes(i.id)&&i.group===g)));$('#queue-count').textContent=queue.length+' bronclusters met dit filter';$('#queue-rows').innerHTML=queue.map(f=>`<tr><td>${esc(f.label)}<br><code>${esc(f.id)}</code></td><td>${esc(f.category)}</td><td>${esc(f.apps.join(', '))}</td><td>${f.occurrences}</td><td>${esc(f.design_status)}</td></tr>`).join('');$('#issue-content').innerHTML=d.issues.filter(r=>matches(r.finding+' '+r.app+' '+r.label)).map(r=>`<div class="issue"><h3>${esc(r.finding)}</h3><p>${esc(r.app)} · broncluster <code>${esc(r.function_id)}</code> · ${esc(r.label)}</p><a href="${esc(r.source_url)}" target="_blank" rel="noopener">Bronaanroep</a><details><summary>Broncontext</summary><pre>${esc(r.context)}</pre></details></div>`).join('')}$('#coverage').textContent=`${d.total_records} bronrecords; ${d.assessed} expliciete beoordelingen, overige bronplaatsen staan open. ${d.icons.length} functiecontracten getekend; ${d.icons.filter(i=>i.source_example).length} hebben een gelezen bronvoorbeeld. Dit is geen claim dat de overige bronclusters unieke functies zijn.`;$('#theme').onchange=theme;$('#group').onchange=render;$('#search').oninput=render;$('#mono').onchange=()=>document.body.classList.toggle('mono',$('#mono').checked);$('#accent').oninput=()=>document.documentElement.style.setProperty('--icon-accent',$('#accent').value);document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-tab]').forEach(t=>t.classList.toggle('active',t===b));['icons','queue','issues'].forEach(id=>$('#'+id).classList.toggle('hidden',id!==b.dataset.tab))});theme();render();
</script></html>'''


PAGE=PAGE.replace('Ronde vormen, betekenisvolle accenten en de hoofdkleur bovenop.',
                  'Ronde vormen, betekenisvolle accenten en een laagvolgorde per icoon.').replace(
    '<div class="stats">',
    '<p><a href="layers.html">Zes iconen met accent vóór</a> · <a href="shapes.html">Drie vormen herzien: Nieuw document, Opslaan als en 3D-beeld draaien</a>.</p><div class="stats">')


PAGE=PAGE.replace('function resized(s,n){','let svgInstance=0;function resized(s,n){s=s.replaceAll("b2-blend-","b2-blend-"+(++svgInstance)+"-");').replace('${i.svg[24]}','${resized(i.svg[24],58)}').replace(
    'Drie vormen herzien: Nieuw document, Opslaan als en 3D-beeld draaien','Vormen en kleurovergangen verfijnd')


PAGE=PAGE.replace('De eerste serie bevat 31 functies.',f'De {14+len(ALL_AVAILABLE)} series bevatten {len(DEFINITIONS)} functies.').replace(
    '31 functies · 62 SVG-masters',f'{len(DEFINITIONS)} functies · {len(DEFINITIONS)*2} SVG-masters').replace(
    'Download 62 SVG’s',f'Download {len(DEFINITIONS)*2} SVG’s').replace(
     '1.487 bronclusters in de werklijst',f"{len(load_catalog()['functions']):,} bronclusters in de werklijst".replace(',', '.')).replace(
    '<label>Groep <select',
    '<label>Serie <select id="batch"><option value="">Alles</option><option value="1">1 · Basis (31)</option><option value="2">2 · Tekenen en objecten (34)</option><option value="3">3 · Vensters en panelen (8)</option><option value="4">4 · Tekstopmaak (7)</option><option value="5">5 · Projecten en gegevens (3)</option><option value="6">6 · Rapporten (2)</option><option value="7">7 · IFC en BIM (3)</option><option value="8,9,10">8–10 · Drie nieuwe groepen (13)</option><option value="8">8 · Lijsten en bomen (2)</option><option value="9">9 · Planning (7)</option><option value="10">10 · Geotechniek (4)</option><option value="11,12,13">11–13 · Drie volgende groepen (15)</option><option value="11">11 · Energie en warmte (3)</option><option value="12">12 · Paalplan (7)</option><option value="13">13 · Spraak en audio (5)</option><option value="14">14 · Paginanavigatie en weergaven (9)</option></select></label><label>Groep <select').replace(
    'let icons=d.icons.filter(i=>','let icons=d.icons.filter(i=>(!$("#batch").value||$("#batch").value.split(",").includes(String(i.series)))&&').replace(
    "$('#group').onchange=render;","$('#group').onchange=render;$('#batch').onchange=render;").replace(
    '<article class="card">','<article class="card" data-series="${i.series}" ${i.semantic_color?`data-semantic="${i.semantic_color}" style="--semantic-color:var(--status-${i.semantic_color})"`:""}>').replace(
    '<code>${i.id}</code>','<code>${i.id}</code>${i.series>=21?"<span class=new-badge>NIEUW</span>":""}').replace(
    'r.style.colorScheme=t.kind;',
    'r.style.colorScheme=t.kind;for(const role of ["info","warning","error","success","text-secondary"])r.style.setProperty("--status-"+role,c[role]);').replace(
    "let queue=d.queue.filter(f=>","let queue=d.queue.filter(f=>(!$('#batch').value||d.icons.some(i=>(f.canonical_functions?.length?f.canonical_functions:[f.canonical_function||f.id]).includes(i.id)&&$('#batch').value.split(',').includes(String(i.series))))&&").replace(
    'bronclusters met dit filter','functierijen met dit filter').replace(
    ' Eén kleur</label>',' Eén kleur per icoon</label>').replace(
    '</style>',' .card[data-semantic] .hero svg,.card[data-semantic] .native svg{color:var(--semantic-color)}.new-badge{display:inline-block;font-size:9px;letter-spacing:.08em;margin-left:8px;color:var(--icon-accent)}.tablewrap th{position:static}</style>').replace(
    'Status en gevaar worden door label/toestand bepaald, niet door het amber accent.',
    'Statusiconen gebruiken één meldingskleur uit het thema via color; hun accentpad is leeg. Eigen accentkleur geldt voor actieiconen. Een status krijgt daarnaast altijd een label; kleur is niet het enige onderscheid.')


PAGE=PAGE.replace('data-series="${i.series}"','data-icon="${i.id}" data-series="${i.series}"').replace(
    'c[role]);','(role==="warning"?d.warning_preview[$("#theme").value]:c[role]));').replace(
    '<div class="stats">','<p><a href="feedback.html">Screenshotfeedback · voor/na, rastervarianten en bewegende laadindicator</a>. Waarschuwing volgt de afgesproken gele themarol uit tokens 0.4.</p><div class="stats">').replace(
    '<label>Eigen accent', '<label><input type="checkbox" id="motion" checked> Animatie Bezig</label><label>Eigen accent').replace(
    "$('#theme').onchange=theme;", "$('#motion').onchange=()=>document.body.classList.toggle('paused',!$('#motion').checked);$('#theme').onchange=theme;").replace(
    '</style>', '.card[data-icon="status.busy"] .hero svg,.card[data-icon="status.busy"] .native svg{animation:b2spin 1.4s linear infinite;transform-origin:center;transform-box:fill-box}.paused .card[data-icon="status.busy"] svg{animation:none}@keyframes b2spin{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.card[data-icon="status.busy"] svg{animation:none!important}}</style>').replace(
    'Eigen accentkleur geldt voor actieiconen.', 'Eigen accentkleur geldt voor actieiconen. De ring Bezig draait alleen in deze review; de SVG zelf is statisch. Waarschuwing gebruikt de gele warning-rol uit tokens 0.4.')


PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {BULK_GROUPS[batch]} ({sum(v==batch for v in BULK_SERIES.values())})</option>' for batch in AVAILABLE_SERIES) + f'<option value="{",".join(map(str,AVAILABLE_SERIES))}">Nieuwe reviewronde ({len(BULK_DEFINITIONS)})</option></select></label><label>Groep',1)
PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {SESSION_GROUPS[batch]} ({sum(v==batch for v in SESSION_SERIES.values())})</option>' for batch in SESSION_AVAILABLE) + f'<option value="{",".join(map(str,SESSION_AVAILABLE))}">Tweede grote reviewronde ({len(SESSION_DEFINITIONS)})</option></select></label><label>Groep',1)
PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {NAV_GROUPS[batch]} ({sum(v==batch for v in NAV_SERIES.values())})</option>' for batch in NAV_AVAILABLE) + f'<option value="{",".join(map(str,NAV_AVAILABLE))}">Bladwijzers en bijlagen ({len(NAV_DEFINITIONS)})</option></select></label><label>Groep',1)
PAGE=PAGE.replace('<div class="stats">','<p><a href="bulk-review-5.html">Volgende reeks · 40 iconen</a> · <a href="bulk-review-4.html">Vorige grote vervolglijst</a> · <a href="bulk-review-3.html">Bladwijzers en bijlagen</a> · <a href="bulk-review-2.html">Tweede grote reviewronde</a> · <a href="bulk-review.html">Vorige ronde (goedgekeurd)</a></p><div class="stats">',1)

PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {THIRD_GROUPS[batch]} ({sum(v==batch for v in THIRD_SERIES.values())})</option>' for batch in THIRD_AVAILABLE) + f'<option value="{",".join(map(str,THIRD_AVAILABLE))}">Grote vervolglijst ({len(THIRD_DEFINITIONS)})</option></select></label><label>Groep',1)

PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {FOURTH_GROUPS[batch]} ({sum(v==batch for v in FOURTH_SERIES.values())})</option>' for batch in FOURTH_AVAILABLE) + f'<option value="{",".join(map(str,FOURTH_AVAILABLE))}">Volgende reeks ({len(FOURTH_DEFINITIONS)})</option></select></label><label>Groep',1)



PAGE=PAGE.replace('</select></label><label>Groep', ''.join(f'<option value="{batch}">{batch} · {COMPLETION_GROUPS[batch]} ({sum(v==batch for v in COMPLETION_SERIES.values())})</option>' for batch in COMPLETION_AVAILABLE) + f'<option value="{",".join(map(str,COMPLETION_AVAILABLE))}">Nachtelijke uitbreiding ({len(COMPLETION_DEFINITIONS)})</option></select></label><label>Groep',1)
PAGE=PAGE.replace('<div class="stats">','<p><a href="completion-review.html">Nachtelijke uitbreiding · alle nieuwe ontwerpen</a> · <a href="coverage-review.html">Brondekking en resterend werk</a> · <a href="scope-review.html">Controle op ontbrekende ontwerpen</a></p><div class="stats">',1)

if __name__=='__main__':main()
