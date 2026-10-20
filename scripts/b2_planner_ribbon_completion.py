"""Planner ribbon contracts, traced through pinned store commands and renderers."""
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_reports_completion import glyph
from b2_font_geometry import font_sources

GROUPS = {126:'Taken en planningsberekening',127:'Taakstructuur en WBS',128:'Resources en werkruimtes',129:'Resourcebelasting en vereffening',130:'Planningslagen en volgrelaties'}
ROWS = [
 (126,'planning.calculate','Planning doorrekenen','runCPM berekent de taakdatums en resourcebelasting opnieuw via solveProject; een cyclusfout blijft als fout en verouderde planning zichtbaar.','d519b126b5a469ee'),
 (126,'task.add','Taak toevoegen','Een taak onder de selectie invoegen in boommodus; zonder bruikbaar anker achteraan toevoegen via addTaskNearSelection.','3319a280928e223e'),
 (126,'task.split-mode','Taakonderbreking tekenen','De splitsmodus voor een sleepgebaar op een Gantt-balk bedienen of de actieve modus aanduiden; het beeld alleen maakt nog geen onderbreking.','50c7c51f371bc7ac'),
 (126,'calendar.manage','Werkkalenders beheren','De kalenderdialoog openen voor werk- en niet-werktijden; geen datumkiezer voor één invoerveld.','a9ed3274ab2fab7b'),
 (126,'report.workspace','Rapportwerkruimte','Het Rapport-tabblad activeren met het gemonteerde ReportPanel; nog geen printopdracht of uitvoerbestand maken.','46fa102bb8e0aae2'),
 (126,'planning.move-date','Projectdatums verschuiven','De dialoog Project verplaatsen openen voor de projectstart; uitgeschakeld zonder projectstartdatum.','8f2ccbc37c36f78c'),
 (127,'planning.structure','Codes en velden beheren','Het structuurvenster openen voor de planningscodes en velden.','f56a341ecac7019f'),
 (127,'wbs.auto-number','Automatische WBS-nummering','Automatische taaknummering omschakelen; inschakelen past de WBS-nummering onmiddellijk toe.','b53cd197e52819b3'),
 (127,'wbs.renumber','WBS opnieuw nummeren','De taakstructuur opnieuw WBS-nummers geven via applyWbsNumbering; alleen beschikbaar als automatische nummering uit staat.','782680d722120f78'),
 (127,'task.indent','Taak inspringen','De geselecteerde taken in boommodus een niveau onderbrengen; geen tekstopmaak wijzigen.','d31cfea60ae57d82'),
 (127,'task.outdent','Taak uitspringen','De geselecteerde taken in boommodus een niveau hoger plaatsen; geen tekst uitlijnen.','eb565b6d73ceb451'),
 (127,'tree.collapse-scope','Taakstructuur inklappen','In gegroepeerde weergave alle groepen inklappen; anders de geselecteerde samenvattingstaken, of alle zonder selectie.','6282dc4e8ecf3855'),
 (127,'tree.expand-scope','Taakstructuur uitklappen','In gegroepeerde weergave alle groepen uitklappen; anders de geselecteerde samenvattingstaken, of alle zonder selectie.','05fb961f6f382630'),
 (128,'resource.workspace','Resourcewerkruimte','De resourcebeheerweergave over de volledige werkruimte openen via showResourcePanel=true en resourcePanelDocked=false.','9f0942b9c58b35e2'),
 (128,'resource.dock','Resourcepaneel naast planning','Het resourcebeheer als rechter zijpaneel tonen of sluiten; een verborgen rail wordt bij openen uitgeklapt.','ab0259d3f4fe2dea'),
 (128,'resource.new','Resource toevoegen','Een lokale resourceconcept-rij met naamfocus openen in project- of bibliotheekbeheer; de lintknop opent eerst de werkruimte. Pas bevestiging bewaart de resource.','510238f231980cd9'),
 (128,'panel.warnings','Waarschuwingenpaneel','Het rechter paneel met planningswaarschuwingen omschakelen; de icoonknop zelf is geen fout- of waarschuwingsstatus.','ccae8c3214625106'),
 (128,'table.columns','Tabelkolommen kiezen','Naar de Tabel-werkruimte schakelen en de gedeelde kolommenkiezer openen via useColumnsButtonBinding.','94ff0ed8451c1014'),
 (129,'resource.previous','Vorige histogramresource','In de histogramresourcekeuze achteruit door alle resources en de totaalkeuze stappen; geen vorige taak selecteren.','7e4d99a181b4158e'),
 (129,'resource.next','Volgende histogramresource','In de histogramresourcekeuze vooruit door alle resources en de totaalkeuze stappen.','f6f49488c64cdbe3'),
 (129,'resource.level','Resources vereffenen','De resourcevereffeningsdialoog openen; de knop alleen wijzigt nog geen taakdatums.','0a1a3d2345f613fb'),
 (129,'resource.clear-level','Vereffening wissen','Alle berekende vereffeningsvertragingen en -gaten wissen en de planning opnieuw doorrekenen; taakgegevens blijven behouden.','d316b8fd0c45514d'),
 (130,'planning.trace-predecessors','Voorgangers volgen','De voorgangerkant van traceMode omschakelen; combineren met opvolgers geeft both. Geen afhankelijkheid toevoegen.','ac429983ed375f2f'),
 (130,'planning.trace-successors','Opvolgers volgen','De opvolgerkant van traceMode omschakelen; combineren met voorgangers geeft both.','820270b1df8eae33'),
 (130,'planning.baseline-overlay','Referentieplanning tonen','De referentieplanningsbalken in de Gantt omschakelen via setOverlays baseline; geen referentie vastleggen.','c5742f4334cc8898'),
 (130,'planning.progress-line','Voortgangslijn tonen','De voortgangslijn op de Gantt omschakelen; geen voortgang importeren of taken verbinden.','56777ef0cf4f0c7f'),
 (130,'planning.status-date-line','Peildatumlijn tonen','De verticale peildatumlijn op de Gantt omschakelen; de peildatum zelf blijft gelijk.','9ddcb0b3c55ca017'),
 (130,'planning.resource-accent','Resourcekleuren tonen','Resourcekleuraccenten op de Gantt-balken omschakelen; geen kleur van een resource bewerken.','8c3f19a230ed0a8b'),
 (130,'planning.float-band','Spelingsband tonen','De beschikbare speling als band na niet-kritieke taken omschakelen.','701a9da750f34c86'),
 (130,'planning.relations-visible','Relatielijnen tonen','Bestaande afhankelijkheidslijnen op de Gantt tonen of verbergen; geen nieuwe relatie maken.','276352345f306f83'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De bepalende taakbalk, pijl of laagmarkering blijft voor de dragende contour zichtbaar.' for k in KEYS}
TYPOGRAPHY={k:{**font_sources()['format.color'],'glyph':'12','purpose':'WBS-cijfers in Space Grotesk Medium.'} for k in ('wbs.auto-number','wbs.renumber')}
REUSED={}
EXCLUDED={}
DISPATCHERS={}
DISPATCH_EVIDENCE={}
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)
reuse('c5bcf38e7b0d8248','file.new','showNewProjectDialog opent de concrete nieuwe-projectworkflow.')
reuse('08e2791e26101fa0','file.save','COMMANDS.save roept saveFile aan voor het actieve document.')
reuse('749e185416e5bde8','file.save-as','COMMANDS.saveAs roept saveFileAs aan; andere bestemming dan gewoon opslaan.')
reuse('1eb287092a4443d8','file.open','COMMANDS.open roept openFile aan met de vertaalde importlabels.')
reuse('a3a56fa3f14e6b57','edit.undo','COMMANDS.undo gebruikt de actieve documenthistorie en canUndo.')
reuse('0eb0fb1bc05418dc','edit.redo','COMMANDS.redo gebruikt de actieve documenthistorie en canRedo.')
reuse('222e3bd976395c25','edit.delete','deleteTasksBulk verwijdert de geselecteerde taken; de handler wordt alleen bij selectie ingeschakeld.')
reuse('6e8e178892078d62','view.zoom-in','COMMANDS.zoomIn verhoogt de Gantt-tijdschaal view.zoom met ZOOM_STEP.')
reuse('cc176c1b2a851e1a','view.zoom-out','COMMANDS.zoomOut verlaagt de Gantt-tijdschaal view.zoom met ZOOM_STEP.')
reuse('d2e5b379cc7276fc','file.import','showProgressImportDialog opent de concrete voortgangsimport; alleen met aanwezige taken.')
reuse('bce8d4fd5662f722','file.export','exportAs(progress-xlsx) exporteert de voortgangstabel als XLSX, niet het native projectbestand.')
reuse('91599c28aeded364','project.properties','showProjectInfoDialog opent het gemonteerde projectinformatieformulier.')
reuse('1beb69aa4ac6a9aa','ui.settings','showSettingsDialog opent de appinstellingen.')
reuse('eb724bff1cf8a629','ui.shortcuts','showShortcutsDialog opent het toetsencombinatieoverzicht.')
reuse('a994a35d5aff1e38 e0806d685ee9e4bc 3bba187535649f3c','panel.right','Alle drie zijn declaratie/toestandvarianten van dezelfde eigenschappenpaneelknop: de zichtbaarheid bepaalt Eye/EyeOff, klikken schakelt showPropertiesPanel. Gebruik het paneelcontract in plaats van objectzichtbaarheid.')


def bars(c,accent=False,baseline=False):
    c.line([(3,3),(3,21),(22,21)],radius=.2)
    c.line([(6,7),(14,7)],accent,radius=0)
    c.line([(10,13),(20,13)],accent,radius=0)
    if baseline:
        c.line([(5,10),(12,10)],True,radius=0)
        c.line([(9,16),(17,16)],True,radius=0)

def person(c,x=8,y=7):
    c.circle(x,y,2.4)
    c.line(arc_points(x,y+9,4.2,180,360,16),radius=0)

def arrow(c,x,y,right=True,accent=True):
    d=1 if right else -1
    c.line([(x-3*d,y),(x+3*d,y)],accent,radius=0)
    c.line([(x,y-3),(x+3*d,y),(x,y+3)],accent,radius=.3)

def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='planning.calculate':
        bars(c)
        c.line(arc_points(16,9,5,215,535,28),True,radius=0)
        c.line([(11,8),(11,12),(15,12)],True,radius=.3)
    elif key=='task.add':
        c.line([(3,5),(17,5),(17,11),(3,11)],closed=True,radius=.5)
        c.line([(3,16),(10,16)],radius=0);c.plus(18,18,3)
    elif key=='task.split-mode':
        c.line([(3,8),(9,8),(9,16),(3,16)],closed=True,radius=.4)
        c.line([(15,8),(21,8),(21,16),(15,16)],closed=True,radius=.4)
        c.line([(12,3),(12,7)],True,radius=0)
        c.line([(12,17),(12,21)],True,radius=0)
    elif key=='calendar.manage':
        box(c,3,5,18,16);c.line([(3,10),(21,10)],radius=0)
        for x in (8,16):c.line([(x,3),(x,7)],radius=0)
        for x in ((8,16) if small else (7,12,17)):c.circle(x,15,1,True,True)
    elif key=='report.workspace':
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        box(c,7,10,10,8);c.line([(10,13),(14,13)],True,radius=0)
        if not small:c.line([(10,16),(13,16)],True,radius=0)
    elif key=='planning.move-date':
        bars(c);arrow(c,17,6)
        c.line([(6,13),(6,17)],True,radius=0)
        c.line([(5,15),(9,15)],True,radius=0)
    elif key=='planning.structure':
        c.line([(5,4),(5,18),(11,18)],radius=.3)
        c.line([(5,9),(11,9)],radius=0)
        for y in (6,15):box(c,12,y,9,6,True)
    elif key in ('wbs.auto-number','wbs.renumber'):
        glyph(c,'1',3,3,4,6)
        glyph(c,'2',3,14,5,7)
        for y in (5,20):c.line([(12,y),(20,y)],radius=0)
        if key=='wbs.auto-number':
            c.line(arc_points(17,12,3.5,200,510,24),True,radius=0)
            c.line([(12.5,10),(13.5,14),(17,13)],True,radius=.3)
        else:
            c.line([(15,7),(15,17)],True,radius=0);c.line([(12,14),(15,17),(18,14)],True,radius=.3)
    elif key in ('task.indent','task.outdent'):
        c.line([(3,4),(21,4)],radius=0);c.line([(12,11),(21,11)],radius=0);c.line([(12,19),(21,19)],radius=0)
        arrow(c,6,13,key=='task.indent')
    elif key in ('tree.collapse-scope','tree.expand-scope'):
        for y in (4,20):c.line([(4,y),(20,y)],radius=0)
        down=key=='tree.expand-scope'
        c.line([(8,9 if down else 6),(12,5 if down else 10),(16,9 if down else 6)],True,radius=.3)
        c.line([(8,15 if down else 18),(12,19 if down else 14),(16,15 if down else 18)],True,radius=.3)
    elif key in ('resource.workspace','resource.dock'):
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        if key=='resource.workspace':person(c,12,12)
        else:
            c.line([(13,7),(13,21)],radius=0)
            c.circle(17.5,12,1.7,True)
            c.line(arc_points(17.5,19,2.5,180,360,16),True,radius=0)
    elif key=='resource.new':
        person(c,8,7);c.plus(18,17,3)
    elif key=='panel.warnings':
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        c.line([(12,10),(18,19),(6,19)],True,closed=True,radius=.4)
        c.line([(12,13),(12,15)],True,radius=0);c.circle(12,17,0.3,True,True)
    elif key=='table.columns':
        box(c,3,3,18,18)
        for x in (9,15):c.line([(x,3),(x,21)],True,radius=0)
        c.line([(3,8),(21,8)],radius=0)
    elif key in ('resource.previous','resource.next'):
        person(c,12,6);arrow(c,12,20,key=='resource.next')
    elif key=='resource.level':
        c.line([(3,21),(21,21)],radius=0)
        for x,h in [(5,6),(12,12),(19,17)]:c.line([(x,19),(x,h)],radius=0)
        c.line([(2,9),(22,9)],True,radius=0)
    elif key=='resource.clear-level':
        c.line([(3,20),(21,20)],radius=0)
        for x,h in [(5,9),(11,5),(17,12)]:c.line([(x,18),(x,h)],radius=0)
        c.line([(13,6),(21,14)],True,radius=0);c.line([(13,14),(21,6)],True,radius=0)
    elif key in ('planning.trace-predecessors','planning.trace-successors'):
        right=key=='planning.trace-successors'
        box(c,3,3,7,6);box(c,14,15,7,6)
        c.line([(6,10),(6,12),(18,12),(18,14)],radius=.3)
        arrow(c,16 if right else 8,12,right)
    elif key=='planning.baseline-overlay':bars(c,baseline=True)
    elif key=='planning.progress-line':
        bars(c);c.line([(12,3),(12,7),(17,10),(9,13),(12,17),(12,21)],True,radius=.3)
    elif key=='planning.status-date-line':
        bars(c);c.line([(13,3),(13,21)],True,radius=0)
        c.line([(10,3),(16,3)],True,radius=0)
    elif key=='planning.resource-accent':
        bars(c,True);c.circle(20,5,2)
    elif key=='planning.float-band':
        bars(c);c.line([(15,7),(21,7)],True,radius=0)
        for x in (16,21):c.line([(x,4),(x,10)],True,radius=0)
    elif key=='planning.relations-visible':
        box(c,3,3,8,6);box(c,13,15,8,6)
        c.line([(7,9),(7,12),(17,12),(17,15)],True,radius=.3)
        c.line([(14,12),(17,15),(20,12)],True,radius=.3)
    return True
