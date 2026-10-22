"""Source-reviewed additions for the overnight completion of the B2 family.

Artwork is original vector construction. Source records describe behaviour only.
Keep explicit record decisions; never map all occurrences of a name automatically.
"""
import json
import math
from pathlib import Path
from b2_second_series import box, cubic, lightning
from b2_bulk_series import page
from b2_energy_pile_audio import arc_points, microphone
from b2_session_two import dimension_arrow

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {46: 'Taal en account', 47: 'Spraakapparaten en bronnen',
          48: 'Veldwerk en inspectie', 49: 'Camera en gegevenskoppeling'}
# Series, canonical contract, Dutch label, exact behaviour, reviewed record ID.
ROWS = [
    (46, 'ui.language', 'Taal kiezen', 'Het taalmenu openen; de taalknoppen wijzigen de interfacetaal.', 'd084a1bf22abab10'),
    (46, 'account.menu', 'Accountmenu openen', 'openMenu opent de accountkeuzes; de avatar is geen directe aanmeldopdracht.', '1352dd021291e310'),
    (47, 'audio.microphone', 'Microfooningang', 'Aanduiding bij de invoerapparaatkeuze; start zelf geen opname.', 'abbb17683d1c0d4d'),
    (47, 'audio.models', 'Spraakmodellen beheren', 'De models-werkruimte openen voor lokale spraakmodellen.', '79c4fc49ab182fc1'),
    (47, 'audio.dictionary', 'Woordenboek bewerken', 'De dictionary-werkruimte openen voor herkenningswoorden en correcties.', 'd875ebf829c5043e'),
    (47, 'audio.transcript-result', 'Transcriptieresultaat', 'Aanduiding bij het resultaat van de microfoontest; geen nieuwe transcriptie starten.', '5616a14f60d2ee06'),
    (48, 'field.project', 'Veldwerkproject', 'Het project-tabblad met projectformulier openen via switchTab.', 'ee057c2b24924d35'),
    (48, 'field.floorplans', 'Plattegronden', 'Het plattegrond-tabblad openen; geen bestand direct importeren.', '6ac59ecbcdb3521f'),
    (48, 'bim.workspace', 'BIM-werkruimte', 'Het IFC/3D BIM-tabblad openen; geen lagenbeheer of IFC-import starten.', '7dcc688ff8034884'),
    (48, 'field.survey', 'Opname ter plaatse', 'De opname-werkruimte voor veldgegevens openen; geen audio-opname.', '0b1110670625ab5e'),
    (48, 'field.inspections', 'Inspecties', 'Het inspectie-tabblad openen en de inspectielijst vernieuwen.', 'ae78b8209192b3ac'),
    (48, 'field.handovers', 'Opleveringen', 'Het opleverings-tabblad openen en de opleveringslijst vernieuwen.', '6a201b752b588ee5'),
    (48, 'field.dashboard', 'Projectdashboard', 'Het dashboard-tabblad openen en de projectstatistieken bijwerken.', 'be1af0c79a2d0d52'),
    (48, 'field.ticket-add', 'Ticket op plattegrond', 'toggleAddPointMode schakelt de plaatsingsmodus voor een veldwerkticket.', '5e6ef56d3606a993'),
    (49, 'integration.manage', 'Gegevenskoppelingen', 'Het koppelingen-tabblad openen en de connectorlijst tekenen.', '62185ad3ff22a6d4'),
    (49, 'energy.fetch-label', 'Energielabel ophalen', 'lookupEnergyLabel haalt de gekoppelde labelgegevens voor het project op.', 'db301c559138fdd7'),
    (49, 'camera.open', 'Camera openen', 'Het live cameravenster openen om een foto te maken; nog geen foto vastleggen.', '1a08728699c6faec'),
    (49, 'camera.switch', 'Camera wisselen', 'switchCamera wisselt facingMode tussen environment en user en opent de nieuwe stream.', '28f0b55660729171'),
    (49, 'camera.capture', 'Foto vastleggen', 'capturePhoto legt het videoframe vast en voegt het toe aan de huidige fotos.', 'df0e4bed272e9285'),
]
from b2_workspace_completion import (ROWS as WORKSPACE_ROWS, GROUPS as WORKSPACE_GROUPS,
    REUSED as WORKSPACE_REUSED, EXCLUDED as WORKSPACE_EXCLUDED,
    KEYS as WORKSPACE_KEYS, extend as extend_workspace)
ROWS += WORKSPACE_ROWS
GROUPS.update(WORKSPACE_GROUPS)

from b2_reports_completion import (ROWS as REPORTS_ROWS, GROUPS as REPORTS_GROUPS,
    REUSED as REPORTS_REUSED, EXCLUDED as REPORTS_EXCLUDED, DISPATCHERS,
    KEYS as REPORTS_KEYS, extend as extend_reports, TYPOGRAPHY,
    ACCENT_FRONT as REPORTS_ACCENT_FRONT)
ROWS += REPORTS_ROWS
GROUPS.update(REPORTS_GROUPS)

from b2_bim_completion import (ROWS as BIM_ROWS, GROUPS as BIM_GROUPS,
    REUSED as BIM_REUSED, EXCLUDED as BIM_EXCLUDED,
    KEYS as BIM_KEYS, extend as extend_bim, ACCENT_FRONT as BIM_ACCENT_FRONT)
ROWS += BIM_ROWS
GROUPS.update(BIM_GROUPS)

from b2_frame_completion import (ROWS as FRAME_ROWS, GROUPS as FRAME_GROUPS,
    REUSED as FRAME_REUSED, EXCLUDED as FRAME_EXCLUDED,
    KEYS as FRAME_KEYS, extend as extend_frame, ACCENT_FRONT as FRAME_ACCENT_FRONT)
ROWS += FRAME_ROWS
GROUPS.update(FRAME_GROUPS)

from b2_pointcloud_completion import (ROWS as POINTCLOUD_ROWS, GROUPS as POINTCLOUD_GROUPS,
    REUSED as POINTCLOUD_REUSED, EXCLUDED as POINTCLOUD_EXCLUDED, DISPATCHERS as POINTCLOUD_DISPATCHERS,
    DISPATCH_EVIDENCE as POINTCLOUD_DISPATCH_EVIDENCE, KEYS as POINTCLOUD_KEYS,
    EXAMPLE_OVERRIDES as POINTCLOUD_EXAMPLE_OVERRIDES, EXAMPLE_EVIDENCE as POINTCLOUD_EXAMPLE_EVIDENCE,
    extend as extend_pointcloud, ACCENT_FRONT as POINTCLOUD_ACCENT_FRONT)
ROWS += POINTCLOUD_ROWS
GROUPS.update(POINTCLOUD_GROUPS)
DISPATCH_EVIDENCE={rid:'De gelezen BlockIcon-dispatcher kiest het ontwerp voor het concrete BLOCK_OPTIONS-type.' for rid in DISPATCHERS}
DISPATCHERS.update(POINTCLOUD_DISPATCHERS)
DISPATCH_EVIDENCE.update(POINTCLOUD_DISPATCH_EVIDENCE)

from b2_energy_completion import (ROWS as ENERGY_ROWS, GROUPS as ENERGY_GROUPS,
    REUSED as ENERGY_REUSED, EXCLUDED as ENERGY_EXCLUDED, DISPATCHERS as ENERGY_DISPATCHERS,
    DISPATCH_EVIDENCE as ENERGY_DISPATCH_EVIDENCE, KEYS as ENERGY_KEYS, SEMANTIC,
    extend as extend_energy, ACCENT_FRONT as ENERGY_ACCENT_FRONT)
ROWS += ENERGY_ROWS
GROUPS.update(ENERGY_GROUPS)
DISPATCHERS.update(ENERGY_DISPATCHERS)
DISPATCH_EVIDENCE.update(ENERGY_DISPATCH_EVIDENCE)

from b2_heatloss_completion import (ROWS as HEATLOSS_ROWS, GROUPS as HEATLOSS_GROUPS,
    REUSED as HEATLOSS_REUSED, EXCLUDED as HEATLOSS_EXCLUDED, DISPATCHERS as HEATLOSS_DISPATCHERS,
    DISPATCH_EVIDENCE as HEATLOSS_DISPATCH_EVIDENCE, KEYS as HEATLOSS_KEYS,
    extend as extend_heatloss, ACCENT_FRONT as HEATLOSS_ACCENT_FRONT)
ROWS += HEATLOSS_ROWS
GROUPS.update(HEATLOSS_GROUPS)
DISPATCHERS.update(HEATLOSS_DISPATCHERS)
DISPATCH_EVIDENCE.update(HEATLOSS_DISPATCH_EVIDENCE)

from b2_pile_completion import (ROWS as PILE_ROWS, GROUPS as PILE_GROUPS,
    REUSED as PILE_REUSED, EXCLUDED as PILE_EXCLUDED, DISPATCHERS as PILE_DISPATCHERS,
    DISPATCH_EVIDENCE as PILE_DISPATCH_EVIDENCE, KEYS as PILE_KEYS, SEMANTIC as PILE_SEMANTIC,
    extend as extend_pile, ACCENT_FRONT as PILE_ACCENT_FRONT)
ROWS += PILE_ROWS
GROUPS.update(PILE_GROUPS)
DISPATCHERS.update(PILE_DISPATCHERS)
DISPATCH_EVIDENCE.update(PILE_DISPATCH_EVIDENCE)
SEMANTIC.update(PILE_SEMANTIC)

from b2_geotech_completion import (ROWS as GEOTECH_ROWS, GROUPS as GEOTECH_GROUPS,
    REUSED as GEOTECH_REUSED, EXCLUDED as GEOTECH_EXCLUDED, DISPATCHERS as GEOTECH_DISPATCHERS,
    DISPATCH_EVIDENCE as GEOTECH_DISPATCH_EVIDENCE, KEYS as GEOTECH_KEYS, EVIDENCE as GEOTECH_EVIDENCE,
    extend as extend_geotech, ACCENT_FRONT as GEOTECH_ACCENT_FRONT)
ROWS += GEOTECH_ROWS
GROUPS.update(GEOTECH_GROUPS)
DISPATCHERS.update(GEOTECH_DISPATCHERS)
DISPATCH_EVIDENCE.update(GEOTECH_DISPATCH_EVIDENCE)

from b2_calc_completion import (ROWS as CALC_ROWS, GROUPS as CALC_GROUPS,
    REUSED as CALC_REUSED, EXCLUDED as CALC_EXCLUDED, DISPATCHERS as CALC_DISPATCHERS,
    DISPATCH_EVIDENCE as CALC_DISPATCH_EVIDENCE, KEYS as CALC_KEYS, TYPOGRAPHY as CALC_TYPOGRAPHY,
    extend as extend_calc, ACCENT_FRONT as CALC_ACCENT_FRONT)
ROWS += CALC_ROWS
GROUPS.update(CALC_GROUPS)
DISPATCHERS.update(CALC_DISPATCHERS)
DISPATCH_EVIDENCE.update(CALC_DISPATCH_EVIDENCE)
TYPOGRAPHY.update(CALC_TYPOGRAPHY)

from b2_calculations_completion import (ROWS as CALCULATIONS_ROWS, GROUPS as CALCULATIONS_GROUPS,
    REUSED as CALCULATIONS_REUSED, EXCLUDED as CALCULATIONS_EXCLUDED,
    DISPATCHERS as CALCULATIONS_DISPATCHERS, DISPATCH_EVIDENCE as CALCULATIONS_DISPATCH_EVIDENCE,
    KEYS as CALCULATIONS_KEYS, extend as extend_calculations, ACCENT_FRONT as CALCULATIONS_ACCENT_FRONT)
ROWS += CALCULATIONS_ROWS
GROUPS.update(CALCULATIONS_GROUPS)
DISPATCHERS.update(CALCULATIONS_DISPATCHERS)
DISPATCH_EVIDENCE.update(CALCULATIONS_DISPATCH_EVIDENCE)

from b2_pdf_catalog_completion import (ROWS as PDF_CATALOG_ROWS, GROUPS as PDF_CATALOG_GROUPS,
    REUSED as PDF_CATALOG_REUSED, EXCLUDED as PDF_CATALOG_EXCLUDED,
    KEYS as PDF_CATALOG_KEYS, extend as extend_pdf_catalog,
    TYPOGRAPHY as PDF_CATALOG_TYPOGRAPHY, ACCENT_FRONT as PDF_CATALOG_ACCENT_FRONT)
ROWS += PDF_CATALOG_ROWS
GROUPS.update(PDF_CATALOG_GROUPS)
TYPOGRAPHY.update(PDF_CATALOG_TYPOGRAPHY)

from b2_pdf_controls_completion import (ROWS as PDF_CONTROLS_ROWS, GROUPS as PDF_CONTROLS_GROUPS,
    REUSED as PDF_CONTROLS_REUSED, EXCLUDED as PDF_CONTROLS_EXCLUDED,
    DISPATCHERS as PDF_CONTROLS_DISPATCHERS, DISPATCH_EVIDENCE as PDF_CONTROLS_DISPATCH_EVIDENCE,
    KEYS as PDF_CONTROLS_KEYS, extend as extend_pdf_controls,
    TYPOGRAPHY as PDF_CONTROLS_TYPOGRAPHY, ACCENT_FRONT as PDF_CONTROLS_ACCENT_FRONT)
ROWS += PDF_CONTROLS_ROWS
GROUPS.update(PDF_CONTROLS_GROUPS)
DISPATCHERS.update(PDF_CONTROLS_DISPATCHERS)
DISPATCH_EVIDENCE.update(PDF_CONTROLS_DISPATCH_EVIDENCE)
TYPOGRAPHY.update(PDF_CONTROLS_TYPOGRAPHY)

from b2_pdf_editing_completion import (ROWS as PDF_EDITING_ROWS, GROUPS as PDF_EDITING_GROUPS,
    REUSED as PDF_EDITING_REUSED, EXCLUDED as PDF_EDITING_EXCLUDED,
    DISPATCHERS as PDF_EDITING_DISPATCHERS, DISPATCH_EVIDENCE as PDF_EDITING_DISPATCH_EVIDENCE,
    KEYS as PDF_EDITING_KEYS, extend as extend_pdf_editing, ACCENT_FRONT as PDF_EDITING_ACCENT_FRONT)
ROWS += PDF_EDITING_ROWS
GROUPS.update(PDF_EDITING_GROUPS)
DISPATCHERS.update(PDF_EDITING_DISPATCHERS)
DISPATCH_EVIDENCE.update(PDF_EDITING_DISPATCH_EVIDENCE)

from b2_pdf_final_completion import (ROWS as PDF_FINAL_ROWS, GROUPS as PDF_FINAL_GROUPS,
    REUSED as PDF_FINAL_REUSED, EXCLUDED as PDF_FINAL_EXCLUDED,
    DISPATCHERS as PDF_FINAL_DISPATCHERS, DISPATCH_EVIDENCE as PDF_FINAL_DISPATCH_EVIDENCE,
    KEYS as PDF_FINAL_KEYS, extend as extend_pdf_final, ACCENT_FRONT as PDF_FINAL_ACCENT_FRONT,
    TYPOGRAPHY as PDF_FINAL_TYPOGRAPHY, SEMANTIC as PDF_FINAL_SEMANTIC)
ROWS += PDF_FINAL_ROWS
GROUPS.update(PDF_FINAL_GROUPS)
DISPATCHERS.update(PDF_FINAL_DISPATCHERS)
DISPATCH_EVIDENCE.update(PDF_FINAL_DISPATCH_EVIDENCE)
TYPOGRAPHY.update(PDF_FINAL_TYPOGRAPHY)
SEMANTIC.update(PDF_FINAL_SEMANTIC)

from b2_planner_ribbon_completion import (ROWS as PLANNER_RIBBON_ROWS, GROUPS as PLANNER_RIBBON_GROUPS,
    REUSED as PLANNER_RIBBON_REUSED, EXCLUDED as PLANNER_RIBBON_EXCLUDED,
    KEYS as PLANNER_RIBBON_KEYS, extend as extend_planner_ribbon, ACCENT_FRONT as PLANNER_RIBBON_ACCENT_FRONT,
    TYPOGRAPHY as PLANNER_RIBBON_TYPOGRAPHY)
ROWS += PLANNER_RIBBON_ROWS
GROUPS.update(PLANNER_RIBBON_GROUPS)
TYPOGRAPHY.update(PLANNER_RIBBON_TYPOGRAPHY)

from b2_planner_choices_completion import (ROWS as PLANNER_CHOICES_ROWS, GROUPS as PLANNER_CHOICES_GROUPS,
    REUSED as PLANNER_CHOICES_REUSED, EXCLUDED as PLANNER_CHOICES_EXCLUDED,
    KEYS as PLANNER_CHOICES_KEYS, extend as extend_planner_choices, ACCENT_FRONT as PLANNER_CHOICES_ACCENT_FRONT,
    SEMANTIC as PLANNER_CHOICES_SEMANTIC, EVIDENCE as PLANNER_CHOICES_EVIDENCE)
ROWS += PLANNER_CHOICES_ROWS
GROUPS.update(PLANNER_CHOICES_GROUPS)
SEMANTIC.update(PLANNER_CHOICES_SEMANTIC)

from b2_planner_safety_completion import (ROWS as PLANNER_SAFETY_ROWS, GROUPS as PLANNER_SAFETY_GROUPS,
    REUSED as PLANNER_SAFETY_REUSED, EXCLUDED as PLANNER_SAFETY_EXCLUDED,
    KEYS as PLANNER_SAFETY_KEYS, extend as extend_planner_safety, ACCENT_FRONT as PLANNER_SAFETY_ACCENT_FRONT,
    SEMANTIC as PLANNER_SAFETY_SEMANTIC)
ROWS += PLANNER_SAFETY_ROWS
GROUPS.update(PLANNER_SAFETY_GROUPS)
SEMANTIC.update(PLANNER_SAFETY_SEMANTIC)

from b2_planner_dialogs_completion import (ROWS as PLANNER_DIALOGS_ROWS, GROUPS as PLANNER_DIALOGS_GROUPS,
    REUSED as PLANNER_DIALOGS_REUSED, EXCLUDED as PLANNER_DIALOGS_EXCLUDED,
    KEYS as PLANNER_DIALOGS_KEYS, extend as extend_planner_dialogs, ACCENT_FRONT as PLANNER_DIALOGS_ACCENT_FRONT,
    SEMANTIC as PLANNER_DIALOGS_SEMANTIC, EVIDENCE as PLANNER_DIALOGS_EVIDENCE,
    DISPATCHERS as PLANNER_DIALOGS_DISPATCHERS, DISPATCH_EVIDENCE as PLANNER_DIALOGS_DISPATCH_EVIDENCE)
ROWS += PLANNER_DIALOGS_ROWS
GROUPS.update(PLANNER_DIALOGS_GROUPS)
SEMANTIC.update(PLANNER_DIALOGS_SEMANTIC)
DISPATCHERS.update(PLANNER_DIALOGS_DISPATCHERS)
DISPATCH_EVIDENCE.update(PLANNER_DIALOGS_DISPATCH_EVIDENCE)

from b2_planner_panels_completion import (ROWS as PLANNER_PANELS_ROWS, GROUPS as PLANNER_PANELS_GROUPS,
    REUSED as PLANNER_PANELS_REUSED, EXCLUDED as PLANNER_PANELS_EXCLUDED,
    KEYS as PLANNER_PANELS_KEYS, extend as extend_planner_panels, ACCENT_FRONT as PLANNER_PANELS_ACCENT_FRONT,
    SEMANTIC as PLANNER_PANELS_SEMANTIC, EVIDENCE as PLANNER_PANELS_EVIDENCE,
    DISPATCHERS as PLANNER_PANELS_DISPATCHERS, DISPATCH_EVIDENCE as PLANNER_PANELS_DISPATCH_EVIDENCE)
ROWS += PLANNER_PANELS_ROWS
GROUPS.update(PLANNER_PANELS_GROUPS)
SEMANTIC.update(PLANNER_PANELS_SEMANTIC)
DISPATCHERS.update(PLANNER_PANELS_DISPATCHERS)
DISPATCH_EVIDENCE.update(PLANNER_PANELS_DISPATCH_EVIDENCE)

from b2_planner_final_completion import (ROWS as PLANNER_FINAL_ROWS, GROUPS as PLANNER_FINAL_GROUPS,
    REUSED as PLANNER_FINAL_REUSED, EXCLUDED as PLANNER_FINAL_EXCLUDED,
    KEYS as PLANNER_FINAL_KEYS, extend as extend_planner_final, ACCENT_FRONT as PLANNER_FINAL_ACCENT_FRONT,
    SEMANTIC as PLANNER_FINAL_SEMANTIC, EVIDENCE as PLANNER_FINAL_EVIDENCE, TYPOGRAPHY as PLANNER_FINAL_TYPOGRAPHY,
    DISPATCHERS as PLANNER_FINAL_DISPATCHERS, DISPATCH_EVIDENCE as PLANNER_FINAL_DISPATCH_EVIDENCE)
ROWS += PLANNER_FINAL_ROWS
GROUPS.update(PLANNER_FINAL_GROUPS)
SEMANTIC.update(PLANNER_FINAL_SEMANTIC)
TYPOGRAPHY.update(PLANNER_FINAL_TYPOGRAPHY)
DISPATCHERS.update(PLANNER_FINAL_DISPATCHERS)
DISPATCH_EVIDENCE.update(PLANNER_FINAL_DISPATCH_EVIDENCE)

from b2_scope_completion import (ROWS as SCOPE_ROWS, GROUPS as SCOPE_GROUPS,
    REUSED as SCOPE_REUSED, EXCLUDED as SCOPE_EXCLUDED,
    KEYS as SCOPE_KEYS, extend as extend_scope, ACCENT_FRONT as SCOPE_ACCENT_FRONT,
    SEMANTIC as SCOPE_SEMANTIC, EVIDENCE as SCOPE_EVIDENCE, TYPOGRAPHY as SCOPE_TYPOGRAPHY,
    DISPATCHERS as SCOPE_DISPATCHERS, DISPATCH_EVIDENCE as SCOPE_DISPATCH_EVIDENCE,
    PLANNED_KEYS, PLANNED)
ROWS += SCOPE_ROWS
GROUPS.update(SCOPE_GROUPS)
SEMANTIC.update(SCOPE_SEMANTIC)
TYPOGRAPHY.update(SCOPE_TYPOGRAPHY)
DISPATCHERS.update(SCOPE_DISPATCHERS)
DISPATCH_EVIDENCE.update(SCOPE_DISPATCH_EVIDENCE)
from b2_source_catalog import load_catalog

_catalog = load_catalog()
_records = {r['id']: r for r in _catalog['records']}
AVAILABLE_SERIES = tuple(GROUPS)
DEFINITIONS = [(k, label, GROUPS[b], meaning) for b, k, label, meaning, _ in ROWS]
EXAMPLES = {k: record for _, k, _, _, record in ROWS}
EXAMPLES.update(POINTCLOUD_EXAMPLE_OVERRIDES)
EXAMPLES['status.info']='4cb1901dd8a3a052'
SOURCE_FUNCTIONS = {k: _records[record]['function_id'] for k, record in EXAMPLES.items()}
SERIES = {k: b for b, k, _, _, _ in ROWS}
KEYS = set(SERIES)
ACCENT_FRONT={k:'Het accent blijft volledig zichtbaar voor de kruisende verbindingslijnen.' for k in ('category.devops','category.integration','category.network','category.ai','git.stage-all')}
ACCENT_FRONT.update(REPORTS_ACCENT_FRONT)
ACCENT_FRONT.update(BIM_ACCENT_FRONT)
ACCENT_FRONT.update(FRAME_ACCENT_FRONT)
ACCENT_FRONT.update(POINTCLOUD_ACCENT_FRONT)
ACCENT_FRONT.update(ENERGY_ACCENT_FRONT)
ACCENT_FRONT.update(HEATLOSS_ACCENT_FRONT)
ACCENT_FRONT.update(PILE_ACCENT_FRONT)
ACCENT_FRONT.update(GEOTECH_ACCENT_FRONT)
ACCENT_FRONT.update(CALC_ACCENT_FRONT)
ACCENT_FRONT.update(CALCULATIONS_ACCENT_FRONT)
ACCENT_FRONT.update(PDF_CATALOG_ACCENT_FRONT)
ACCENT_FRONT.update(PDF_CONTROLS_ACCENT_FRONT)
ACCENT_FRONT.update(PDF_EDITING_ACCENT_FRONT)
ACCENT_FRONT.update(PDF_FINAL_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_RIBBON_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_CHOICES_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_SAFETY_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_DIALOGS_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_PANELS_ACCENT_FRONT)
ACCENT_FRONT.update(PLANNER_FINAL_ACCENT_FRONT)
ACCENT_FRONT.update(SCOPE_ACCENT_FRONT)
ACCENT_FRONT['package.catalog']='Alleen de verpakkingstape is accent; de doosribben blijven hoofdkleur.'
ACCENT_FRONT['report.properties']='De ronde schuifknoppen blijven ononderbroken voor de rails.'
EVIDENCE = {k: 'Concrete UI-aanroep en omliggende implementatie gelezen op de vastgelegde broncommit.' for k in KEYS}
EVIDENCE.update(POINTCLOUD_EXAMPLE_EVIDENCE)
EVIDENCE.update(GEOTECH_EVIDENCE)
EVIDENCE.update(PLANNER_CHOICES_EVIDENCE)
EVIDENCE.update(PLANNER_DIALOGS_EVIDENCE)
EVIDENCE.update(PLANNER_PANELS_EVIDENCE)
EVIDENCE.update(PLANNER_FINAL_EVIDENCE)
EVIDENCE.update(SCOPE_EVIDENCE)
EVIDENCE['status.info']='Speech MicTest toont deze melding uitsluitend bij type info; de conditionele tak op de gepinde bron is gelezen.'
REUSED = {
    'b71a80566acd1ac0': ('status.busy', 'DictationOverlay toont de transcribing-toestand met voortgang en resterende tijd.'),
    'b44b2a57254cc154': ('status.success', 'DictationOverlay toont done met het herkende resultaat.'),
    '51ecaabd8e60ca8c': ('status.error', 'DictationOverlay toont error met de fouttekst.'),
    'fb85eb68cfcd1893': ('audio.microphone', 'In DictationOverlay geeft de microfoon de actieve recording-toestand aan; de niveaubalk blijft dynamisch.'),
    'f358917ddb33467c': ('audio.microphone', 'MeetingIndicator toont de opname- of pauzetoestand; dit pictogram start geen opname.'),
    '6da085ce24a4b409': ('status.success', 'MicTest-resultaat met type success.'),
    '296a12618ef46b77': ('status.error', 'MicTest-resultaat met type error.'),
    '4cb1901dd8a3a052': ('status.info', 'MicTest-resultaat met type info.'),
    '1f13157fb00a2f31': ('file.open', 'De klikbare audiobestandszone roept pickFiles aan; bestandkeuze, geen upload naar een externe dienst.'),
    '284ad4872f3ac90f': ('ui.settings', 'Sidebar onViewChange(settings) opent de instellingen.'),
    '17166ae276ac3a98': ('ui.about', 'Sidebar onViewChange(about) opent appinformatie.'),
    '5213f2b68a9b7336': ('window.minimize', 'TitleBar-knop roept minimize aan.'),
    '8801788875e220c5': ('window.close', 'TitleBar-knop roept close aan; dit betreft het venster.'),
    '3b573a404923df25': ('window.minimize', 'Field-titelbalk tb-minimize bedient het native venster.'),
    '8b0598585a9d8e35': ('window.maximize', 'Field-titelbalk tb-maximize schakelt de venstergrootte.'),
    '844b94e7a43ab2d7': ('window.close', 'Field-titelbalk tb-close sluit het native venster.'),
    '45affac1089f48e7': ('theme.light', 'De zichtbare zon staat voor omschakelen naar de lichte themavariant.'),
    'e01ea6294cde38e7': ('theme.dark', 'De maanvariant van dezelfde themaknop schakelt naar donker.'),
    '860ce34d1404d906': ('ui.language', 'De menuchevron staat in dezelfde taalknop; geen afzonderlijke actie.'),
    '4cfb9f09bc763923': ('ui.help', 'Het handleiding-tabblad openen via switchTab(handleiding).'),
    'bc0ddab197c18880': ('view.search', 'openBagModal opent de BAG-adreszoeker; de context benoemt de zoekbron.'),
    '6a0f6d44abb7e525': ('status.success', 'De conditionele bag-verified-badge bevestigt de BAG-verificatie.'),
    '7012e1a6ce4f82ed': ('file.import', 'openProjectImport opent de selectie voor projectimport uit een koppeling.'),
    'dbe59f3042d4ec35': ('file.save', 'saveProject bewaart het actieve Field-project.'),
    '419b9a3e861d0765': ('view.zoom-in', 'De knop vergroot de plattegrond via zoom.'),
    '174580a2b2a27f96': ('view.zoom-out', 'De knop verkleint de plattegrond via zoom.'),
    'ef4508c9baf699a6': ('view.actual-size', 'zoomFit zet in deze bron alleen zoomLevel op 1; geen berekende passend-in-vensterfunctie.'),
    '158018bdc3ff1cb4': ('file.export', 'exportPDF maakt een PDF-export van de veldgegevens; geen rapportgenerator van een andere app.'),
    'ac1bad0383b39683': ('file.export', 'De HTML-export bewaart veldgegevens als HTML; formaat staat in het label.'),
    '3e071d63c443a65e': ('file.export', 'Navigatie naar het exporttabblad; alleen als routeaanduiding, niet als directe exportactie.'),
}
EXCLUDED = {
    '52ebfad677597c94': 'Appbeeldmerk in About, geen vast bedieningsicoon.',
    'fe4c2e121a784a91': 'Appbeeldmerk in TitleBar, geen vast bedieningsicoon.',
    '14c60ae0fb9107f3': 'Grote decoratieve microfoon in de lege vergaderweergave; geen afzonderlijke bediening.',
    'fdbbfa70ea0acd38': 'Grote lege-staatillustratie in de transcriptieweergave; geen afzonderlijke bediening.',
    'fd63623a808b1d6b': 'Field-beeldmerk in titelbalk.',
    '8fc3022bb567d1b4': 'Field-beeldmerk bij de appkop.',
    '1f4f953cd640eb2a': 'Native vensterbeeldmerk geladen uit icon.png.',
    '3ba43d2d8cca4711': 'Grote cloudillustratie in een bestands-dropzone; invoerbediening en inhoud blijven van de component.',
    'ab49e668797a2014': 'Grote cloudillustratie in de tweede bestands-dropzone.',
    '4e4de3f67fd57006': 'Grote plattegrondillustratie in de lege werkruimte.',
    '8517e0d8e6e7c479': 'Grote afbeeldingsillustratie bij de foto-invoer; geen foto vastleggen.',
}

REUSED.update(WORKSPACE_REUSED)
REUSED.update(REPORTS_REUSED)
REUSED.update(BIM_REUSED)
REUSED.update(FRAME_REUSED)
REUSED.update(POINTCLOUD_REUSED)
REUSED.update(ENERGY_REUSED)
REUSED.update(HEATLOSS_REUSED)
REUSED.update(PILE_REUSED)
REUSED.update(GEOTECH_REUSED)
REUSED.update(CALC_REUSED)
REUSED.update(CALCULATIONS_REUSED)
REUSED.update(PDF_CATALOG_REUSED)
REUSED.update(PDF_CONTROLS_REUSED)
REUSED.update(PDF_EDITING_REUSED)
REUSED.update(PDF_FINAL_REUSED)
REUSED.update(PLANNER_RIBBON_REUSED)
REUSED.update(PLANNER_CHOICES_REUSED)
REUSED.update(PLANNER_SAFETY_REUSED)
REUSED.update(PLANNER_DIALOGS_REUSED)
REUSED.update(PLANNER_PANELS_REUSED)
REUSED.update(PLANNER_FINAL_REUSED)
REUSED.update(SCOPE_REUSED)
EXCLUDED.update(WORKSPACE_EXCLUDED)
EXCLUDED.update(REPORTS_EXCLUDED)
EXCLUDED.update(BIM_EXCLUDED)
EXCLUDED.update(FRAME_EXCLUDED)
EXCLUDED.update(POINTCLOUD_EXCLUDED)
EXCLUDED.update(ENERGY_EXCLUDED)
EXCLUDED.update(HEATLOSS_EXCLUDED)
EXCLUDED.update(PILE_EXCLUDED)
EXCLUDED.update(GEOTECH_EXCLUDED)
EXCLUDED.update(CALC_EXCLUDED)
EXCLUDED.update(CALCULATIONS_EXCLUDED)
EXCLUDED.update(PDF_CATALOG_EXCLUDED)
EXCLUDED.update(PDF_CONTROLS_EXCLUDED)
EXCLUDED.update(PDF_EDITING_EXCLUDED)
EXCLUDED.update(PDF_FINAL_EXCLUDED)
EXCLUDED.update(PLANNER_RIBBON_EXCLUDED)
EXCLUDED.update(PLANNER_CHOICES_EXCLUDED)
EXCLUDED.update(PLANNER_SAFETY_EXCLUDED)
EXCLUDED.update(PLANNER_DIALOGS_EXCLUDED)
EXCLUDED.update(PLANNER_PANELS_EXCLUDED)
EXCLUDED.update(PLANNER_FINAL_EXCLUDED)
EXCLUDED.update(SCOPE_EXCLUDED)


def pin(c, x=10, y=9, r=5, accent=False):
    points = arc_points(x, y, r, 150, 390, 32)
    c.line(points + [(x, y + r + 6)], accent, closed=True, radius=.5)
    c.circle(x, y, 1.5, accent)


def camera(c):
    c.line([(3,8),(7,8),(9,5),(15,5),(17,8),(21,8),(21,20),(3,20)], closed=True, radius=.7)
    c.circle(12,14,3.5,True)


def extend(c, key):
    if key not in KEYS:
        return False
    if key in WORKSPACE_KEYS:return extend_workspace(c,key)
    if key in REPORTS_KEYS:return extend_reports(c,key)
    if key in BIM_KEYS:return extend_bim(c,key)
    if key in FRAME_KEYS:return extend_frame(c,key)
    if key in POINTCLOUD_KEYS:return extend_pointcloud(c,key)
    if key in ENERGY_KEYS:return extend_energy(c,key)
    if key in HEATLOSS_KEYS:return extend_heatloss(c,key)
    if key in PILE_KEYS:return extend_pile(c,key)
    if key in GEOTECH_KEYS:return extend_geotech(c,key)
    if key in CALC_KEYS:return extend_calc(c,key)
    if key in CALCULATIONS_KEYS:return extend_calculations(c,key)
    if key in PDF_CATALOG_KEYS:return extend_pdf_catalog(c,key)
    if key in PDF_CONTROLS_KEYS:return extend_pdf_controls(c,key)
    if key in PDF_EDITING_KEYS:return extend_pdf_editing(c,key)
    if key in PDF_FINAL_KEYS:return extend_pdf_final(c,key)
    if key in PLANNER_RIBBON_KEYS:return extend_planner_ribbon(c,key)
    if key in PLANNER_CHOICES_KEYS:return extend_planner_choices(c,key)
    if key in PLANNER_SAFETY_KEYS:return extend_planner_safety(c,key)
    if key in PLANNER_DIALOGS_KEYS:return extend_planner_dialogs(c,key)
    if key in PLANNER_PANELS_KEYS:return extend_planner_panels(c,key)
    if key in PLANNER_FINAL_KEYS:return extend_planner_final(c,key)
    if key in SCOPE_KEYS:return extend_scope(c,key)
    small = c.size == 16
    if key == 'ui.language':
        c.circle(12,12,9)
        c.line([(12+4.5*math.cos(2*math.pi*i/64),12+9*math.sin(2*math.pi*i/64)) for i in range(64)],True,closed=True,radius=0)
        c.line([(3,12),(21,12)],radius=0)
    elif key == 'account.menu':
        c.circle(10,7,3.5)
        c.line(arc_points(10,20,7,180,360,24),radius=0)
        c.line([(17,10),(20,13),(23,10)],True,radius=.5)
    elif key == 'audio.microphone':
        microphone(c,12)
    elif key == 'audio.models':
        box(c,4,4,16,16)
        for x,h in ((8,4),(12,8),(16,5)):
            c.line([(x,12-h/2),(x,12+h/2)],True,radius=0)
        for x in (7,12,17):
            c.line([(x,1.5),(x,4)],radius=0);c.line([(x,20),(x,22.5)],radius=0)
    elif key == 'audio.dictionary':
        box(c,4,3,16,18);c.line([(8,3),(8,21)],radius=0)
        c.line([(11,8),(17,8)],True,radius=0)
        c.line([(11,12),(17,12)],radius=0)
        if not small:c.line([(11,16),(15,16)],radius=0)
    elif key == 'audio.transcript-result':
        page(c,4,2,16,20)
        for y,x in ((8,15),(12,17),(16,13)):c.line([(8,y),(x,y)],True,radius=0)
    elif key == 'field.project':
        c.line([(3,21),(3,9),(12,2),(21,9),(21,21)],closed=True,radius=.5)
        box(c,7,11,10,10,True)
        c.line([(12,11),(12,21)],True,radius=0)
    elif key == 'field.floorplans':
        box(c,3,3,18,18)
        c.line([(3,11),(12,11),(12,21)],True,radius=0)
        c.line([(12,3),(12,7)],radius=0)
        c.line([(16,11),(21,11)],True,radius=0)
    elif key == 'bim.workspace':
        x=5*math.sqrt(3)
        c.line([(12,2),(12+x,7),(12+x,17),(12,22),(12-x,17),(12-x,7)],closed=True,radius=.4)
        c.line([(12-x,7),(12,12),(12+x,7)],radius=.4)
        c.line([(12,12),(12,22)],True,radius=0)
    elif key == 'field.survey':
        pin(c,12,8,5,True)
        cubic(c,[(3,23),(8,20.5),(16,20.5),(21,23)])
    elif key == 'field.inspections':
        box(c,4,4,16,18);box(c,8,2,8,4)
        c.line([(7,13),(10,16),(17,9)],True,radius=.4)
    elif key == 'field.handovers':
        c.line([(3,10),(12,3),(21,10),(21,21),(3,21)],closed=True,radius=.6)
        c.line([(7,14),(11,18),(18,11)],True,radius=.5)
    elif key == 'field.dashboard':
        box(c,3,3,18,18);c.line([(3,9),(21,9)],radius=0)
        c.line([(9,9),(9,21)],radius=0)
        for x,y in ((13,17),(17,13)):c.line([(x,19),(x,y)],True,radius=0)
    elif key == 'field.ticket-add':
        pin(c,9,8,5)
        c.plus(19,18,3,True)
    elif key == 'integration.manage':
        box(c,2,6,7,12);box(c,15,6,7,12)
        c.line([(9,10),(15,10)],True,radius=0)
        c.line([(9,14),(15,14)],True,radius=0)
    elif key == 'energy.fetch-label':
        c.line([(3,5),(14,5),(21,12),(14,19),(3,19)],closed=True,radius=.5)
        c.circle(6,9,.8,filled=True)
        lightning(c,12.5,12,6.5,10)
    elif key in {'camera.open','camera.capture'}:
        camera(c)
        if key == 'camera.open':
            c.line([(2,3),(6,3)],True,radius=0)
            c.line([(4,1),(4,5)],True,radius=0)
        else:c.circle(12,14,1.1,True,True)
    elif key == 'camera.switch':
        box(c,4,7,16,10);c.circle(12,12,2.8)
        dimension_arrow(c,(5,3),(19,3),1.8)
        dimension_arrow(c,(19,21),(5,21),1.8)
    return True
