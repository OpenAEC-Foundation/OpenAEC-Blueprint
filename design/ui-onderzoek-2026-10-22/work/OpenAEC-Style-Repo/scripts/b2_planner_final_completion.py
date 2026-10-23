"""Final Planner controls, pinned source bindings and explicit shared-icon dispatch."""
from b2_second_series import box
from b2_planner_safety_completion import turn
from b2_reports_completion import glyph
from b2_font_geometry import font_sources

GROUPS={153:'Activiteiten en begeleiding',154:'Planningsmodi en informatie',155:'Werkrooster bewerken',156:'Relaties, herstel en tabelweergave',157:'Onderbrekingen en fontpakketten'}
ROWS=[
 (153,'panel.ai-activity','AI-activiteitenpaneel','Het activiteitenpaneel van de AI openen of sluiten via ui.aiActivityOpen; start geen agent of opdracht.','213b25256f4dd1e0'),
 (153,'panel.debug-terminal','Debugterminal tonen','De ingeschakelde debugterminal openen of sluiten via ui.debugTerminalOpen; geen terminalopdracht uitvoeren.','528a461551a25305'),
 (153,'guide.tutorials','Tutorials','Vaste aanduiding van begeleide oefenprojecten in het tutorialaanbod en het uitbreidingspakket; dit beeld start zelf niets.','40753b7a8f777000'),
 (153,'guide.tutorial-start','Tutorial starten','De gekozen tutorial via startTutorial en de begeleidingsruntime starten; geen gewone rondleiding of mediaplayer.','aa49ec6ee50e99d6'),
 (154,'planning.dependency-draw-mode','Relaties tekenen actief','Vaste aanduiding van de actieve afhankelijkheidstekenmodus; het aparte Stoppen beëindigt de modus. Het beeld maakt zelf geen relatie.','a437cc141d15ac12'),
 (154,'status.hour-data','Uurgegevens aanwezig','De melding aanduiden dat het document uurgegevens bevat terwijl uurplanning uitstaat; de aparte actie schakelt uurplanning in.','19296a9a99e055e8'),
 (154,'status.recorded-dates','Vastgelegde datums tonen','Vaste toestand datesAsRecorded: toon de uit het bestand overgenomen datums. De afzonderlijke herberekenactie kiest opnieuw CPM.','9fa1d41a7f11b2c7'),
 (154,'status.structure-locked','Structuurwijziging beperkt','Melden dat structuurwijzigingen in de huidige filter-, groeps- of sorteermodus niet beschikbaar zijn; de aparte actie herstelt de boomweergave. Geen documentvergrendeling.','bf992898cc9a4486'),
 (155,'calendar.holiday-add','Niet-werkdag toevoegen','Een nieuwe lokale uitzonderingsregel in draft.holidays toevoegen; naam en datum zijn daarna bewerkbaar. Geen nieuwe kalender maken.','cd7dc3ccc22b784d'),
 (155,'calendar.work-band-add','Werktijdvak toevoegen','Een extra 08:00–16:00-interval voor de gekozen weekdag aan het roosterconcept toevoegen; pas de omringende kalenderworkflow legt het vast.','1bb0bece330420db'),
 (155,'calendar.copy-workdays','Werktijden naar werkdagen','De tijdvakken van de gekozen weekdag als afzonderlijke kopieën op maandag tot en met vrijdag zetten; geen klembordactie.','c3999485c7ac3ba2'),
 (156,'planning.external-relation','Externe taakrelatie','Kopaanduiding voor het bewerken van een relatie met een taakanker uit een ander projectbestand; geen webadres openen of bestand downloaden.','c74db5796c433c8c'),
 (156,'backup.recover','Projecten herstellen','De aangeboden projectherstel-snapshots via restoreDocuments terugzetten. Opruimen volgt pas na herstel; onbruikbare snapshots blijven bewaard. Geen PDF-lezersessie herstellen.','f08c872839f1823f'),
 (156,'table.column-hide','Kolom uit weergave halen','De gekozen zichtbare kolom via onRemoveColumn uit de tabelweergave halen; cel- en projectgegevens blijven bestaan.','f89fd18c7dc4d14f'),
 (157,'planning.interruption-remove','Taakonderbreking opheffen','Een gekozen onderbreking of alle onderbrekingen van een taak opheffen via removeGap/setTaskSplits; de taak en haar werk blijven bestaan.','147d69f8414db2ae'),
 (157,'extension.font','PDF-fontpakket','Vaste pakketaanduiding voor een uitbreiding die PDF-lettertypen registreert; taal en schrift blijven in de pakketnaam. Geen tekst opmaken of pakket direct installeren.','bc31d24afcbbe026'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De functiemarkering blijft vóór de dragende paneel-, kalender- of documentcontour volledig zichtbaar.' for k in KEYS}
SEMANTIC={k:'text-secondary' for k in ('status.hour-data','status.recorded-dates','status.structure-locked','planning.dependency-draw-mode')}
TYPOGRAPHY={'extension.font':{**font_sources()['format.color'],'glyph':'A','purpose':'Neutrale fontpakketaanduiding; de taal staat in het label. Space Grotesk Medium, geen overgenomen CJK-fontasset.'}}
REUSED={};EXCLUDED={}
DISPATCHERS={
 '7ec7ecd3f23a534d':('status.warning','status.info'),
 'e795f0800acfd18f':('status.bridge-off','status.bridge-live','status.warning','status.error'),
}
DISPATCH_EVIDENCE={
 '7ec7ecd3f23a534d':'StatusBanner.TONES heeft exact warning (alert, waarschuwing) en dim (status, neutrale informatie). De gedeelde AlertTriangle wordt per tone vervangen; geen fouttak afleiden uit de naam.',
 'e795f0800acfd18f':'StatusBar gebruikt dezelfde AI_STATUS_COLOR als AiServerGroup: off, live, port-busy, error. Het omringende knopje opent de AI-linttab; het statusbeeld start of stopt de bridge niet.',
}
EVIDENCE={k:'De concrete gepinde component, handler en gekoppelde state/gegevensroute zijn gelezen; geen functietoewijzing op alleen de oude pictogramnaam.' for k in KEYS}
EVIDENCE['backup.recover']='RecoveryDialog.onRestore volgt useRecoveryRestore: restoreDocuments, daarna clearRecovery alleen zonder skippedIds, anders holdRecoveryForLater. Bron en foutpad gelezen.'
EVIDENCE['guide.tutorial-start']='extensions/tutorials/main.js registreert per TUTORIALS-definitie een ribbonbutton met startTutorial(api,def); het pakket en het aanbod hebben een apart vast onderwerpbeeld.'
EVIDENCE['calendar.copy-workdays']='copyToAllWorkdays kopieert elk interval en doorloopt d=1 tot en met 5; zaterdag/zondag en het klembord worden niet aangeraakt.'
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)

reuse('9d6dcac02f57f483','view.search','HelpPanel zet de query om naar helpArticleMatches op de helpindex; Search is de vaste aanduiding bij de zoekinvoer.')
reuse('339606785a979634 b8668e0ba6ea34fd 3ddc274fe173909b b1b6d24085659e0d f0cea90504d78861','ui.close','De concrete onClose/close-callback sluit de dialoog of het formulier; de knop volgt de eventuele closeDisabled/sending-bewaking.')
reuse('b818526b3dd3adca','ui.help','HelpButton opent het meegegeven articleId via de bewaakte interne helproute.')
reuse('8952d5c5a5d352e7','edit.delete','BaselineDialog.remove verwijdert alleen de gekozen baseline-ID, met bevestiging wanneer nodig; geen taak verwijderen.')
reuse('a29cca2c46363a6b 4b2bac7303bbcf4a','help.context-hint','Layouts toont een titlehint; TaskDurationField toont/verbergt de korte HoverTooltip op pointer/focus. Dit opent geen algemeen helpartikel.')
reuse('3d0f787e646b8344','status.warning','calendarIntervened is endShifted of durationShifted in een geldige verplaatsingspreview zonder preview.error. Waarschuwt voor kalenderinvloed; geen mislukte berekening ondanks de oude rode kleur.')
reuse('e24eaac4590546cb','ui.shortcuts','Vaste kopidentiteit van het toetsencombinatieoverzicht; dit Keyboard-beeld voert zelf geen opdracht uit.')
reuse('8e91a12e7223163d','ui.close','TaskDialog.handleClose verlaat de taakeditie en draait de lokale historiesessie terug; geen succesvolle opslag claimen.')
reuse('7ee295f692cbe92c','status.resource-overallocated','De vaste foutrol-waarschuwing benoemt de overbezette resource; geen algemene verwijder- of stopknop.')
reuse('fe54040f67aa77e1','edit.delete','deleteTask verwijdert de gekozen taak; geen paneel sluiten.')
reuse('2b70bfebe1986ff7','status.info','Vaste ops-note over de zichtbaarheid van taaktypen; geen klikbare toelichting.')
reuse('8456e62216ae615d','edit.delete','removeNote filtert uitsluitend de gekozen notitie-ID uit task.notes.')
reuse('67c7972c92fa717b','status.assignment-protected','Het vaste slot benoemt de door effectiveWorkRule beschermde duur, werk of inzet. Het icoon zelf vergrendelt geen invoerveld.')
reuse('06a3ffa0f1188a72 5f62dad85d08d788','ui.close','De X sluit alleen de desbetreffende NoticeStrip of notificatie via onDismiss/dismissNotification.')
reuse('e8b1ab4f28f5c770','status.warning','Het aanbod meldt verschillen met de vastgelegde bestandsdatums; de aparte actie showRecordedDates kiest die weergave. Het teken rekent niets door.')
reuse('6d3c266b5a78bac5','task.split-mode','Vaste aanduiding dat de Gantt-splitsmodus actief is; de aparte Stoppen-knop beëindigt de modus.')
reuse('0aa188c0fa973f21','edit.delete','removeHoliday verwijdert alleen de geselecteerde kalenderuitzonderingsregel uit het formulierconcept.')
reuse('c4bce9acc939a1bd','edit.delete','Deze X verwijdert een eigen kalenderpreset via deleteOwnPreset en persistOwnPresets; het is geen dialoogsluitknop.')
reuse('881b80b45dcafc8e','tree.collapse','De geopende gegenereerde uitzonderingslijst weer invouwen via expanded.')
reuse('52d7d01ab19f1a0b','tree.expand','De ingeklapte gegenereerde uitzonderingslijst uitvouwen; pas zichtbaar als er uitzonderingen zijn.')
reuse('b763d8f020da1261','status.info','FileDown is hier een vaste bronbestandsnotitie in ExternalLinkDialog; geen download- of importhandler op het beeld.')
reuse('07790dce77cf4d40 6dfdbb2c9d4c50dc 4fcd81ab99f88efc','edit.delete','De concrete knoppen verwijderen respectievelijk een AND/OR-filtergroep, filterregel of bewaard filter; geen venster sluiten.')
reuse('2a9170c5e99255f1','file.new','create sluit de keuze en opent de nieuwe-projectdialoog; het project wordt pas via dat formulier gemaakt.')
reuse('5416f3a2a93def6c','file.open','open sluit de keuze en roept de echte openFile-bestandkeuze aan.')
reuse('375d60e295ae6090','status.warning','De replace-tak waarschuwt als de geïmporteerde poolversie nieuwer is; geen importfout of onmiddellijke vervanging.')
reuse('bc7e0369574dfe6d 97c9b77391706160','status.warning','ProgressImportDialog meldt respectievelijk onzekere dag/maandinterpretatie en genegeerde override-rijen; geen berekening of verwijderactie.')
reuse('9f1528b292d4779d','file.type-project','Vaste typeaanduiding bij een aangeboden projectherstel-snapshot, naast naam, pad en taakcount; geen nieuw bestand maken.')
reuse('0393ecf45a771ac9','file.save-as','answerSiteSave local kiest de lokale bestemmingsroute. fileSlice valt daarna door naar saveFileDialog; opslaan is pas voltooid na een geslaagde bestemming.')
reuse('aa92bfe8a2471849','edit.delete','removeBand verwijdert alleen het gekozen tijdvak van de gekozen weekdag uit het roosterconcept.')
reuse('9e9c88fe4dd1a4c6 c5867e7669e8dbde','documents.new-or-open','Beide Plus-knoppen roepen chooseNewOrOpenProject aan; eerst kiest de gebruiker nieuw of bestaand project.')
reuse('fb67c297205658e1','document.close','De X op een projectkaart roept closeWithGuard voor dat document aan; het is geen sluitknop van het hele overzicht.')
reuse('f9b0a19084283ced e282fb2166cab852','documents.overview','ProjectRail en de hele SwitcherPill openen het overzicht van geopende projectdocumenten; de chevron is geen algemene invoerdropdown.')
reuse('d53284aeee71598f','status.warning','Vaste waarschuwing bij concrete relatieproblemen met een toelichtende tooltip; geen nieuwe relatie maken.')
reuse('22a1222dce758fe0','planning.interruption-remove','apply(removeGap(pieces,g.index)) heft de ene onderbreking op; de andere knop zet alle splitGaps op null.')
reuse('3c6503ac0b9c6328','object.rename','Pencil opent de lokale naameditie van een persoonlijk taaktype; geen taak of nieuw type maken.')
reuse('ac1084471974df9a','edit.delete','Trash2 verwijdert het gekozen persoonlijke taaktype via deleteType; het is geen taakverwijdering.')
reuse('083e9ec578f7eefc','edit.delete','De X verwijdert de gekozen groepeer-/sorteerniveauregel met onChange(levels.filter(...)); geen dialoog sluiten.')
reuse('8442ff973798f174 1774b18e7c78a827 fdc22b922a45a393 8d69158bd3b0c299 6d5c3e3e534a0462','extension.font','Catalogus en manifest tonen een PDF-fontpakket. De taal/het schrift blijft expliciet in de pakketnaam; geen los onbekend letterteken als bediening.')
reuse('3fd9ac23aa42f56f c1265b7c83a6722c','guide.tutorials','Vaste pakketidentiteit voor de begeleide oefenprojecten; alleen de aparte lintknoppen starten een gekozen tutorial.')
reuse('5c902d19ee9860f5 876621de77bdf4e7','extension.importer','Catalogus/manifest benoemen het takenlijst-importerpakket. De vaste lijstvorm voert geen import uit; de daadwerkelijke import zit in de geregistreerde lintactie.')

def panel(c):
    box(c,2,3,20,18);c.line([(2,8),(22,8)],radius=0)
def calendar(c):
    box(c,3,5,18,16);c.line([(3,9),(21,9)],radius=0)
    for x in (7,17):c.line([(x,3),(x,6)],radius=0)
def cap(c,small=False):
    if small:
        c.line([(3,6),(10,3),(17,6),(10,9)],closed=True,radius=.3)
        c.line([(6,9),(6,12),(10,14),(14,12),(14,9)],radius=.3)
    else:
        c.line([(2,8),(12,3),(22,8),(12,13)],closed=True,radius=.3)
        c.line([(6,12),(6,17),(12,20),(18,17),(18,12)],radius=.3)
        c.line([(22,8),(22,15)],True,radius=0)
def extend(c,key):
    if key not in KEYS:return False
    if key=='panel.ai-activity':
        panel(c)
        c.line([(5,15),(8,15),(10,11),(13,19),(16,13),(19,13)],True,radius=.4)
    elif key=='panel.debug-terminal':
        panel(c);c.line([(6,12),(9,15),(6,18)],True,radius=.3)
        c.line([(13,18),(18,18)],radius=0)
    elif key=='guide.tutorials':cap(c)
    elif key=='guide.tutorial-start':
        cap(c,True)
        c.line([(15,14),(22,18),(15,22)],True,closed=True,radius=.3)
        c.line([(3,19),(10,19)],radius=0)
    elif key=='planning.dependency-draw-mode':
        box(c,2,3,9,4);box(c,13,17,9,4)
        c.line([(8,7),(8,13),(17,13),(17,17)],radius=.3)
        c.line([(14,14),(17,17),(20,14)],radius=.3)
        c.line([(15,3),(22,7),(18,8),(17,12)],closed=True,radius=.3)
    elif key=='status.hour-data':
        calendar(c);c.circle(16,16,6)
        c.line([(16,12),(16,16),(19,16)],radius=.3)
    elif key=='status.recorded-dates':
        calendar(c);c.circle(12,15,3);c.circle(12,15,.65,False,True)
    elif key=='status.structure-locked':
        c.line([(4,3),(4,19),(10,19)],radius=.3)
        for y in (5,11):c.line([(4,y),(10,y)],radius=0)
        box(c,10,3,10,4);box(c,10,9,5,4)
        box(c,15,17,7,5);c.line([(16,17),(16,14),(21,14),(21,17)],radius=.8)
    elif key=='calendar.holiday-add':
        calendar(c)
        c.line([(7,13),(11,17)],radius=0);c.line([(11,13),(7,17)],radius=0)
        c.plus(19,19,4)
    elif key=='calendar.work-band-add':
        for y in (5,11,19):c.line([(3,y),(7,y)],radius=0)
        box(c,10,3,11,4);box(c,10,9,7,4);c.plus(18,19,4)
    elif key=='calendar.copy-workdays':
        box(c,2,3,7,6);c.line([(2,6),(9,6)],radius=0)
        c.line([(6,11),(6,16),(13,16)],True,radius=.3)
        c.line([(10,13),(13,16),(10,19)],True,radius=.3)
        for y in (4,8,12,16,20):c.line([(17,y),(22,y)],radius=0)
    elif key=='planning.external-relation':
        box(c,2,4,7,6);box(c,15,14,7,6)
        c.line([(6,10),(6,17),(14,17)],True,radius=.5)
        c.line([(11,14),(14,17),(11,20)],True,radius=.3)
        for y in (3,8):c.line([(12,y),(12,y+2)],radius=0)
    elif key=='backup.recover':
        c.line([(3,22),(3,3),(14,3),(19,8),(19,11)],radius=.5)
        c.line([(14,3),(14,8),(19,8)],radius=.3)
        c.line([(3,22),(9,22)],radius=0);turn(c,17,17,5)
    elif key=='table.column-hide':
        box(c,3,3,18,18)
        for x in (9,15):c.line([(x,3),(x,21)],radius=0)
        c.line([(3,8),(21,8)],radius=0);c.line([(12,16),(22,16)],True,radius=0)
    elif key=='planning.interruption-remove':
        box(c,2,11,6,7);box(c,16,11,6,7)
        c.line([(8,14.5),(16,14.5)],True,radius=0)
        c.line([(11,11.5),(14,14.5),(11,17.5)],True,radius=.3)
        c.line([(9,5),(15,5)],True,radius=0)
    elif key=='extension.font':
        box(c,3,3,18,18);c.line([(3,8),(21,8)],True,radius=0)
        glyph(c,'A',8,11,8,8)
    return True
