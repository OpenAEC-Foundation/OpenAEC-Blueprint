"""Planner calendar/field dialogs, remaining conflicts and explicit runtime indicators."""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_planner_choices_completion import calendar

GROUPS={143:'Kalenderconcepten en planningsvelden',144:'Schermannotaties en logweergave',145:'Bridge en lintdichtheid',146:'Tijdinvoer en toewijzingsinformatie',147:'Uitvoeromgeving van extensies'}
ROWS=[
 (143,'calendar.new','Kalenderconcept toevoegen','Een nieuwe werkkalender aan de lokale bibliotheek in CalendarDialog toevoegen; pas Toepassen/OK commit de kalenderbibliotheek.','0f4f8ff26aa1a546'),
 (143,'calendar.duplicate','Kalenderconcept dupliceren','Een lokale kopie van de geselecteerde werkkalender met nieuw ID en aangepaste naam maken; geen klembordactie. Pas toepassen bewaart de bibliotheek.','ab9ab07f8ba44f2e'),
 (143,'status.project-calendar','Projectkalender','De lokaal gekozen projectstandaard bij de kalenderlijst en -details aanduiden; de ster zelf is geen instelknop.','208dc204ccf06658'),
 (143,'planning.code-type-add','Codetype toevoegen','Een benoemd activiteitencodetype met een lege waardenlijst toevoegen via addActivityCodeType; geen codewaarde of vrij veld maken.','7cdcc010313e9389'),
 (143,'planning.code-value-add','Codewaarde toevoegen','Een nieuwe waarde binnen het gekozen activiteitencodetype maken via addActivityCodeValue met de volgende voorgestelde code.','419d7e7839155358'),
 (143,'planning.custom-field-add','Vrij veld toevoegen','Een vrij planningsveld met naam en gekozen gegevenstype toevoegen via addCustomField.','4a297e05a9336aaa'),
 (144,'capture.annotate','Schermopname annoteren','De editor voor de bestaande schermafbeelding openen; bij sluiten worden de zichtbare annotaties naar een PNG samengevoegd en via onChange teruggegeven.','4bf22288928451e0'),
 (144,'capture.clear-annotations','Schermannotaties wissen','Alle toegevoegde vormen uit de screenshot-overlay verwijderen; de oorspronkelijke schermafbeelding blijft behouden.','1cea710ed3f51c80'),
 (144,'log.pause-view','Logweergave pauzeren','De zichtbare debugloglijst op de huidige momentopname houden; de onderliggende appLog blijft nieuwe gebeurtenissen verzamelen.','eca82aec93a14104'),
 (144,'log.resume-view','Logweergave hervatten','De bevroren momentopname loslaten en de actuele debuglogbuffer weer tonen; geen AI-mutaties of audio hervatten.','570d2f4a4d5cc199'),
 (145,'ai.bridge-start','Bridge starten','De desktop-MCP-bridge starten via de gedeelde controller, met token en listeners; geen audio afspelen of alleen een dialoog openen.','4a028395debd5a89'),
 (145,'ai.bridge-stop','Bridge stoppen','De desktop-MCP-bridge stoppen, listeners afmelden en de status op off zetten; geen tijdelijke schrijfblokkade of audiostop.','cdce8607f570d082'),
 (145,'status.bridge-live','Bridge actief','De door de bridge gerapporteerde live-toestand aanduiden; bewijst niet dat een externe cliënt al verbonden is.','018088f9b6c21732'),
 (145,'status.bridge-off','Bridge uit','De gerapporteerde off-toestand van de bridge aanduiden; geen verbindingsfout suggereren.','018088f9b6c21732'),
 (145,'workspace.ribbon-compact','Compact lint omschakelen','De persistente lintdichtheid tussen full en compact omschakelen via ribbonCompact; de lintinhoud blijft zichtbaar.','154065ae8c7a8e92'),
 (146,'input.time-increase','Tijd met kwartier verhogen','De tijdstapper roept onStep(+15 minuten) aan; de ontvangende klok- of duurinvoer bepaalt toegestane grenzen.','bab21b1a4061cfc1'),
 (146,'input.time-decrease','Tijd met kwartier verlagen','De tijdstapper roept onStep(-15 minuten) aan; geen boomtak of lint invouwen.','d3f9b3f8517c5d87'),
 (146,'assignment.hours-distribution','Urenverdeling bewerken','Het gemonteerde ContourDialog voor deze toewijzing openen; het dialoog bewerkt tijdgefaseerde werkperiodes via setAssignmentContour, geen algemeen grafiekbeeld.','71852e25a3b1082f'),
 (146,'status.assignment-protected','Grootheid beschermd door werkregel','Vaste aanduiding bij duur, inzet of werk wanneer de effectieve werkregel die grootheid beschermt; geen klikbare vergrendeling of garantie dat het invoerveld disabled is.','b8fc3b0b8ebd2d55'),
 (146,'stats.downloads','Downloadstatistieken','Kopaanduiding bij het dialoog met appdownloadstatistieken per besturingssysteem en release; de tabel kan laatst bekende cachewaarden tonen. Geen bestand downloaden.','9b7cc874353719e3'),
 (147,'extension.runtime-desktop','Extensiecontext desktop','Vaste aanduiding bij de desktop-risicotekst in extensietoestemming; dit beeld verleent geen bestandsrechten en belooft geen sandbox.','e3663ce3c7bbf208'),
 (147,'extension.runtime-browser','Extensiecontext browser','Vaste aanduiding bij de browser-risicotekst in extensietoestemming; geen internetverbinding openen of specifieke netwerktoestemming verlenen.','eb044b8887a9c8bb'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De bepalende pijl, pen of markering blijft zichtbaar voor de dragende contour.' for k in KEYS}
SEMANTIC={'status.project-calendar':'text-secondary','status.bridge-live':'success','status.bridge-off':'text-secondary',
          'status.assignment-protected':'text-secondary','extension.runtime-desktop':'text-secondary','extension.runtime-browser':'text-secondary'}
REUSED={};EXCLUDED={}
DISPATCHERS={'018088f9b6c21732':('status.bridge-off','status.bridge-live','status.warning','status.error')}
DISPATCH_EVIDENCE={'018088f9b6c21732':'De vaste Circle in AiServerGroup krijgt AI_STATUS_COLOR[status.state]: off neutraal, live success, port-busy warning, error fout. Het titel/label Bridge stoppen is een omgevingslabel, geen klikhandler op deze indicator.'}
EVIDENCE={'planning.code-value-add':'De catalogus noemt dit W, maar de gepinde StructureDialog-regel101 bevat Plus bij addActivityCodeValue. Het bronpad en de werkende store-actie zijn gelezen; de catalogusnaam is niet als lettervorm overgenomen.',
          'status.bridge-live':'Circle is de gerapporteerde live-tak van AI_STATUS_COLOR, met poorttekst; geen bewijs van een verbonden cliënt.',
          'status.bridge-off':'Circle is de off-tak van AI_STATUS_COLOR; stopMcpServer/controller zet die toestand, niet het indicatorbeeld zelf.'}
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)
reuse('3e3d99f65dfda77f','edit.delete','handleRemove verwijdert het gekozen lokale kalenderconcept, behoudt minstens één kalender en kiest zo nodig een andere projectstandaard; pas commit bewaart de wijzigingen.')
reuse('23b085ac73ac1dda','status.project-calendar','De tweede Star staat in de detailtekst wanneer localProjectId gelijk is aan selected.id. De naastliggende instelknop heeft uitsluitend tekst, geen Star.')
reuse('e11db35d7c471285','status.error','De kalenderlijst toont de rode AlertTriangle alleen wanneer calendarInvalid waar is; dit is ongeldige invoer, geen gewone waarschuwing.')
reuse('e874ab15c9111325 f715841d5f411e7a 2623ee07e2592e38','edit.delete','De individuele knoppen verwijderen respectievelijk een activiteitencodetype, codewaarde of vrij veld via de specifieke structureSlice-actie; geen projectbestand wissen.')
reuse('fefc74b2840ede1a','draw.arrow','setActiveTool(arrow) kiest de rechte screenshot-pijl; slepen legt from/to vast en de tekenfunctie maakt een pijlpunt.')
reuse('82b4b2fafdea163c','draw.rectangle','setActiveTool(rectangle) kiest een rechthoekoverlay op de schermafbeelding; de muisactie legt beide hoeken vast.')
reuse('0a900860cb88cf5c','draw.freehand','setActiveTool(pen) verzamelt de muisposities als vrije lijnpunten in de screenshot-overlay.')
reuse('f4927826a0c815a2','draw.text','setActiveTool(text) plaatst gewone tekst op een gekozen canvaspositie; Enter commit de tekst in shapes.')
reuse('75badce81f8f89d3','edit.undo','handleUndo verwijdert uitsluitend de laatst toegevoegde overlayvorm; dit icoon bedient niet de projecthistorie.')
reuse('e6da22676e7fd5b9','workspace.ribbon-compact','ChevronUp is de andere toestandvariant van dezelfde persistente full/compact-dichtheidsknop; er blijft een compact lint zichtbaar.')
reuse('2b3bca5f9fa0d8e7','ui.dropdown','Select-trigger schakelt open, toont de lijst als portal en selectAt geeft de gekozen option door; de ChevronDown is geen boomtak.')
reuse('199fa964a2eb9fdd','activity.clear','De als Sluiten gelabelde cataloguswaarneming staat werkelijk op Trash2 bij appLog.clear; leegt de debuglogbuffer en notificeert de abonnees, sluit geen paneel.')
reuse('e5cc28b4d2e8811e','ui.close','X zet debugTerminalOpen false en sluit alleen het debugpaneel.')
reuse('339b4884d4bfe7cd','status.warning','Toont alleen een waarschuwing wanneer opgeslagen resterend werk afwijkt van de afgeleide waarde buiten de tolerantie; geen algemene rekenfout.')
reuse('4abfde6611df75aa','status.assignment-protected','De tweede Lock is dezelfde readonly werkregelaanduiding bij de andere beschermde grootheid; geen toggelknop.')
reuse('8205925e7206c712','edit.delete','unassignResource verwijdert de geselecteerde resourcetoewijzing; de resource en taak blijven bestaan.')
reuse('259049469bae8b70','edit.copy','copyButton kopieert werkelijk endpoint, authReal, snippetReal of promptReal volgens de concrete aanroeper; geen configuratie automatisch toepassen.')
reuse('d19bed29411b3678','status.success','De Check verschijnt uitsluitend als de bijbehorende kopieersleutel overeenkomt met copiedKey; tijdelijk kopieersucces.')
reuse('3564a6fc8344275f','credential.show','De Eye-tak toont het echte token in Authorization, configuratiefragment en koppelprompt door showToken true te zetten.')
reuse('1c3e6db7400453d2','credential.hide','De EyeOff-tak maskeert de weergegeven tokenwaarden opnieuw met MASK, zonder het token te wijzigen.')
reuse('7540879047618f02','status.warning','Vaste waarschuwing bij de verbindingsgegevens om zorgvuldig met het token om te gaan; geen verbindingstest.')
reuse('3bd666ffead05722 d7f2ca56e2a46638','status.warning','De ShieldAlert-plaatsen zijn risicowaarschuwingen bij externe extensiecode in de toestemmingsdialoog. Ze geven geen toestemming; de afzonderlijke knoppen beantwoorden resolveExtensionConsent.')


def page(c,x=3,y=3,w=18,h=18):box(c,x,y,w,h)
def log(c):
    page(c)
    for y,w in ((7,7),(12,10),(17,6)):c.line([(6,y),(6+w,y)],radius=0)
def plug(c,off=False):
    c.line([(5,7),(5,12),(15,12),(15,7)],radius=.3)
    c.line(arc_points(10,12,5,0,180,20),radius=0)
    c.line([(10,17),(10,21)],radius=0)
    if off:c.line([(3,3),(21,21)],radius=0)
def clock(c):
    c.circle(9,12,7);c.line([(9,8),(9,12),(12,14)],radius=.3)
def star(c,x,y,r=3):
    pts=[]
    for i in range(10):
        a=math.radians(-90+36*i);rad=r if i%2==0 else r*.45
        pts.append((x+rad*math.cos(a),y+rad*math.sin(a)))
    c.line(pts,closed=True,radius=.2)
def extend(c,key):
    if key not in KEYS:return False
    if key=='calendar.new':
        box(c,3,5,15,16);c.line([(3,10),(18,10)],radius=0)
        for x in (7,14):c.line([(x,3),(x,7)],radius=0)
        c.plus(20,19,3)
    elif key=='calendar.duplicate':
        c.line([(2,16),(2,3),(16,3)],radius=.3)
        box(c,6,6,15,15);c.line([(6,11),(21,11)],radius=0)
        c.line([(10,15),(17,15)],True,radius=0)
        if c.size==24:c.line([(10,18),(14,18)],True,radius=0)
    elif key=='status.project-calendar':
        calendar(c);star(c,12,16,3)
    elif key=='planning.code-type-add':
        c.line([(3,4),(12,4),(17,9),(12,14),(3,14)],closed=True,radius=.4)
        c.circle(7,9,1);c.plus(18,19,3)
    elif key=='planning.code-value-add':
        c.line([(4,3),(4,12),(10,12)],radius=.3)
        box(c,11,8,9,7);c.plus(16,20,3)
    elif key=='planning.custom-field-add':
        page(c);c.line([(3,8),(21,8)],radius=0)
        c.line([(7,12),(7,18)],radius=0);c.plus(16,15,3)
    elif key=='capture.annotate':
        page(c,2,3,20,16);c.circle(7,8,1)
        c.line([(4,15),(8,11),(12,15)],radius=.3)
        c.line([(13,18),(19,12),(22,15),(16,21),(12,22)],True,closed=True,radius=.3)
    elif key=='capture.clear-annotations':
        page(c,2,3,20,16);c.line([(5,14),(9,9),(13,14)],radius=.3)
        c.line([(15,15),(22,22)],True,radius=0);c.line([(15,22),(22,15)],True,radius=0)
    elif key in ('log.pause-view','log.resume-view'):
        log(c)
        if key=='log.pause-view':
            for x in (16,21):c.line([(x,13),(x,22)],True,radius=0)
        else:c.line([(15,12),(22,17),(15,22)],True,closed=True,radius=.3)
    elif key in ('ai.bridge-start','ai.bridge-stop'):
        plug(c)
        if key=='ai.bridge-start':c.line([(17,14),(23,18),(17,22)],True,closed=True,radius=.3)
        else:box(c,16,15,7,7,True)
    elif key=='status.bridge-live':
        plug(c);c.line([(15,19),(18,22),(23,15)],radius=.3)
    elif key=='status.bridge-off':plug(c,True)
    elif key=='workspace.ribbon-compact':
        page(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        for x in (6,11):c.line([(x,11),(x,17)],radius=0)
        c.line([(15,15),(18,12),(21,15)],True,radius=.3)
    elif key in ('input.time-increase','input.time-decrease'):
        clock(c);c.line([(20,5),(20,19)],True,radius=0)
        if key=='input.time-increase':c.line([(17,8),(20,5),(23,8)],True,radius=.3)
        else:c.line([(17,16),(20,19),(23,16)],True,radius=.3)
    elif key=='assignment.hours-distribution':
        c.line([(3,3),(3,21),(22,21)],radius=.2)
        c.line([(6,19),(6,14),(11,14),(11,6),(16,6),(16,11),(21,11),(21,19)],True,radius=.3)
    elif key=='status.assignment-protected':
        box(c,4,10,16,11);c.line(arc_points(12,10,5,180,360,24),radius=0)
        c.circle(12,15,1);c.line([(12,16),(12,18)],radius=0)
    elif key=='stats.downloads':
        c.line([(3,3),(3,21),(21,21)],radius=.3)
        for x,h in ((7,14),(12,10),(17,15)):c.line([(x,19),(x,h)],radius=0)
        c.line([(18,3),(18,10)],True,radius=0);c.line([(15,7),(18,10),(21,7)],True,radius=.3)
    elif key=='extension.runtime-desktop':
        page(c,2,3,20,14);c.line([(12,17),(12,21)],radius=0);c.line([(7,21),(17,21)],radius=0)
        c.line([(6,7),(18,7)],radius=0)
    elif key=='extension.runtime-browser':
        page(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        c.circle(12,14,5);c.line([(7,14),(17,14)],radius=0)
        c.line([(12,9),(12,19)],radius=0)
    return True
