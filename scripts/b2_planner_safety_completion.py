"""Pinned Planner resource, AI control, updater and document chrome contracts."""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_planner_ribbon_completion import person
from b2_planner_choices_completion import calendar

GROUPS={138:'Resourcecapaciteit en herkomst',139:'AI-mutaties bedienen',140:'Herstelkopieën',141:'Verbindingsgegevens en tokens',142:'Updates, tabbladen en activiteit'}
ROWS=[
 (138,'resource.availability-step-add','Capaciteitsstap toevoegen','Een nieuwe beschikbaarheidsstap met ingangsdatum vandaag en capaciteit één aan de resource toevoegen; project- of poolrij bepaalt de opslagbestemming.','298e86f1dc6de0a8'),
 (138,'calendar.edit','Resourcekalender bewerken','De ResourceCalendarDialog voor de gekozen bestaande project- of poolkalender openen; de bewerkte kopie wordt pas bij Toepassen vastgelegd.','a330d3eee827ba9e'),
 (138,'resource.unlink-library','Resource van bibliotheek losmaken','De herkomststempel van de resource verwijderen; ook de kalenderkopie losmaken als geen andere gekoppelde resource die nog volgt. De resourcegegevens blijven behouden.','de01ca52647cd05e'),
 (138,'status.library-linked','Uit bibliotheek afkomstig','Vaste herkomstaanduiding bij een resource met libraryOrigin; geen bibliotheek openen of gegevens direct synchroniseren.','4e117afddfe58549'),
 (139,'ai.pause','AI-mutaties pauzeren','aiPaused inschakelen zodat muterende AI-tools tijdelijk PAUSED terugkrijgen; de bridgeverbinding blijft bestaan.','b76e1c6b14f1e43a'),
 (139,'ai.resume','AI-mutaties hervatten','aiPaused uitschakelen; de overige controles zoals alleen-lezen blijven mutaties zo nodig blokkeren.','01c098d307083bbb'),
 (139,'ai.read-only-toggle','AI alleen-lezen','De alleen-lezenmodus voor muterende AI-tools omschakelen via aiReadOnly; de actieve knoptoestand benoemt of deze beperking aan staat.','41e7e4127856cace'),
 (140,'backup.auto','Automatische AI-back-up','De voorkeur voor een herstelsnapshot vóór de eerste muterende AI-aanroep per document en serversessie omschakelen; geen periodieke bestandsautosave.','49ef7231249a4bfd'),
 (140,'backup.create','Nu herstelkopie maken','Op desktop een IFC-snapshot van het actieve document naar de AI-back-upmap schrijven en de automatische back-upteller voor dit document resetten.','d3bf1c6e1061e1cf'),
 (140,'backup.folder','Back-upmap openen','De AI-back-upmap zo nodig aanmaken en in de desktopbestandsbeheerder openen; geen projectbestand inladen.','92c9fb031590a014'),
 (141,'credential.show','Token tonen','Het gemaskeerde verbindingstoken zichtbaar maken in een invoerveld of configuratiefragment; geen object of paneel tonen.','14371da2a299aef2'),
 (141,'credential.hide','Token verbergen','Het weergegeven verbindingstoken in velden en configuratiefragmenten opnieuw maskeren; het token blijft gelijk.','a5336be6274e59b3'),
 (141,'credential.regenerate','Nieuw verbindingstoken','De bevestiging voor tokenvernieuwing openen; na bevestiging wordt het token vervangen en een actieve desktopbridge herstart om het oude token in te trekken.','24eb6e894d43d89f'),
 (141,'ai.connection-menu','Verbindingsinstellingen','Het compacte menu met poort, token en de ingang naar verbindingsgegevens openen; start zelf geen verbinding.','65be4b6089c98832'),
 (141,'ai.connection-details','Verbindingsgegevens','De dialoog met endpoint, token, configuratiefragment en koppelprompt openen; de Plug-knop start zelf geen server of cliënt.','452fdf10697a94e5'),
 (142,'update.install','Appupdate installeren','Een beschikbare desktopupdate downloaden, een herstelkopie flushen, installeren en de app herstarten; ontbreekt voor door Snap beheerde installatie.','2523ec219f1f330c'),
 (142,'documents.overview','Geopende projecten','Het overzicht van geopende documentkaarten tonen via showProjectOverview; geen recent-bestandenlijst of bedrijfsbibliotheek.','fc6bd09ae5173585'),
 (142,'documents.new-or-open','Project starten of openen','Het gemonteerde keuzedialoog voor een nieuw of bestaand project tonen; nog geen project direct maken of bestand kiezen.','25231043fc8d8e2a'),
 (142,'tabs.scroll-start','Tabstrook naar begin','De tabstrook naar eerdere verborgen tabgroepen schuiven zonder het actieve document te wijzigen; de host spiegelt de richting bij RTL.','e52144d9b66255eb'),
 (142,'tabs.scroll-end','Tabstrook naar eind','De tabstrook naar latere verborgen tabgroepen schuiven zonder het actieve document te wijzigen; de host spiegelt de richting bij RTL.','cf66a61dd9a43f5d'),
 (142,'activity.clear','Activiteitenlog wissen','De huidige AI-activiteitenbuffer of appdebuglogbuffer legen en de abonnees bijwerken; geen projectdocumenten, taken of back-upbestanden wissen.','6b049106c883a5bb'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De bepalende markering blijft zichtbaar voor de dragende lijn; geen kleurverloop.' for k in KEYS}
SEMANTIC={'status.library-linked':'text-secondary'}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)
reuse('a9b9dfba09525e45','resource.new','onAddClick opent een lokale resourceconcept-rij en focust de naam; project/pool-weergave bepaalt het soort, bezettingsweergave biedt de knop niet aan.')
reuse('23180fd38b4179ab 64c72275f2eb8f66','edit.delete','Trash vraagt resourceverwijdering; Check bevestigt diezelfde verwijdering. Projectresources met toewijzingen vragen bevestiging, poolresources altijd; geen geslaagd-status op de bevestigingsknop.')
reuse('89ab4900bee7dbf4','edit.delete','Verwijdert de gekozen capaciteitsstap via filter op de index en schrijft de gewijzigde availabilitySteps terug; de resource blijft bestaan.')
reuse('3e9989b5d1857a69','tree.collapse','De geopende detailrij met AvailabilityStepsEditor sluiten; ChevronDown is de huidige geopende-rijvariant.')
reuse('a0b45374db3d31a8','tree.expand','De resource-detailrij met beschikbaarheidsstappen openen; ChevronRight is de gesloten-rijvariant.')
reuse('79fb6e9664d150c0','ui.close','Sluit resourcebeheer via showResourcePanel false.')
reuse('6e6416aa9859efdc','ui.close','Verlaat alleen de inline verwijderbevestiging via onCancelRemove; verwijdert de resource niet.')
reuse('bfee1b7bfa988162 89bb8e7fcbf64a91','status.success','De afzonderlijke poolNotice/projectNotice bevestigt een geslaagde overname of koppeling in resourcebeheer.')
reuse('a48964a8baa6f522','ai.read-only-toggle','Unlock is alleen de niet-actieve toestandvariant van dezelfde aiReadOnly-schakelaar; geen object ontgrendelen. Het vervangende icoon blijft gelijk met expliciete active-toestand.')
reuse('8c8d62d5e1a74ec2','status.success','AiSafety-feedback met kind ok na een geslaagde handmatige herstelkopie.')
reuse('da4371bfbb0d3e2c','status.error','Deze bron heeft ondanks het overgenomen label Backup-map openen werkelijk AlertTriangle in feedback.kind err, voor back-up-/mapfouten; geen waarschuwing of mapactie.')
reuse('d0f2d85ee4e3dc80','edit.copy','Kopieert het bestaande verbindingstoken naar het klembord via useCopyFeedback; geen token vernieuwen.')
reuse('4280a3a34181d1de','status.success','Check verschijnt alleen als copiedKey token is; tijdelijk bevestigingsbeeld van een geslaagde tokenkopie.')
reuse('a895435660053164','ai.connection-details','De volledige lintvariant opent dezelfde AiConnectionDetailsDialog; geen server direct starten.')
reuse('d3a4f281aa993ea4','status.update-available','De available-status met versienummer en releasetekst; geen downloadactie op dit vaste beeld.')
reuse('ffee37dfe7ce879a 7062f1ffa6d340cb','status.busy','Status van updatecontrole of de readyToInstall/herstartfase; de host kan het teken laten draaien.')
reuse('eab0b820d0b05a06','status.error','Toont status.kind error met fouttekst; de oorspronkelijke driehoek staat hier in de foutrol.')
reuse('45c6ad617419f68c','status.success','Toont de door de updater gerapporteerde upToDate-status als de controle niet bezig is; web-no-op meldt dezelfde status, dus geen onafhankelijke versiegarantie.')
reuse('f427f7b6939a6ac9','ui.check-updates','Opnieuw proberen roept runCheck/checkForUpdates(false,setStatus) aan; geen download of installatie direct starten.')
reuse('81cebf7d82418e11','edit.copy','Kopieert alleen de vaste handmatige DEB-installatie-instructie; voert die opdracht niet uit.')
reuse('e82f9f8935f8caf9','status.success','Check is de tijdelijke copied-feedback na geslaagde klembordkopie van de instructie.')
reuse('f70e3effe31d8ecf','link.open-external','Opent uitsluitend de releases/downloadpagina in de browser via shell-open of window.open.')
reuse('1e2bcca63db6596f','status.info','Vaste Snap-notitie meldt dat Snap Store/snapd updates verzorgt; dit PackageOpen-beeld voert geen installatie uit.')
reuse('d050a6a913790e44','status.success','ActivityRow entry.ok is true; de vaste markering bevestigt het gelogde toolresultaat.')
reuse('642b3c25548d6680','status.error','ActivityRow entry.ok is false en de rij toont foutinformatie; oorspronkelijke rode driehoek wordt door de foutrol vervangen.')
reuse('4fc2045c463b1eae','tree.expand','Opent details van de activiteitenrij (argsJson/resultJson/substappen); geen tijdnavigatie.')
reuse('e159066d6d8721b5','tree.collapse','Sluit de geopende activiteitendetails.')
reuse('cfdc9fce95283f1c','ui.close','Sluit alleen AIActivityPanel via aiActivityOpen false.')
reuse('51b96ce273bb2749 a5df3b127f8651c8','panel.right','De railstrip zet rightPanelCollapsed false; de paneelkopknop zet die true. Beide bedienen dezelfde rechterkolom, geen boomrij.')
reuse('88d18fe380562c4f','resource.workspace','De dockkop zet resourcePanelDocked false terwijl het resourcepaneel al zichtbaar is; opent daardoor het volledige resourcebeheer.')
reuse('94e182e7df53ec12 8ae7f21cb050826e 0f6da78398a128be','ui.close','De drie railkoppen sluiten respectievelijk eigenschappen, resource-dock en waarschuwingen via hun eigen show-vlag; geen native venster.')
reuse('291a769dab739767','edit.undo','Titelbalk roept undo aan met canUndo-beschikbaarheid van het actieve document.')
reuse('9872f67988a4ff11','edit.redo','Titelbalk roept redo aan met canRedo-beschikbaarheid van het actieve document.')
reuse('8bc4fb239d4f1e7e','ui.settings','Titelbalk opent showSettingsDialog.')
reuse('519cf4c25f2c1dd8','window.minimize','Desktop withAppWindow roept het native w.minimize aan.')
reuse('8946ad2b9ff86de0','window.maximize','Square is de niet-gemaximaliseerde titelbalkvariant; handleMaximize roept dan native maximize aan.')
reuse('ce0925bc20c20f29','window.restore','Copy is hier uitsluitend de gemaximaliseerde herstelvariant; handleMaximize roept unmaximize aan, geen kopie maken.')
reuse('4269c36cba31ff4e','window.close','Desktoptitelbalk roept native w.close aan; de app verzorgt de eigen afsluitafhandeling.')
reuse('d6b5b9d50fa23cf0','tabs.scroll-start','RTL-tegenvorm van dezelfde scrollTabs(start)-knop. documentTabScrollTarget schuift naar verborgen tabgroepen, geen documentselectie.')
reuse('548cc404345abe61','tabs.scroll-end','RTL-tegenvorm van dezelfde scrollTabs(end)-knop; activeId blijft gelijk.')


def frame(c):
    box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
def copies(c):
    c.line([(3,17),(3,3),(16,3)],radius=.3)
    box(c,6,6,15,15)
def field(c):
    box(c,2,3,20,8)
    for x in (6,12,18):c.circle(x,7,.7,False,True)
def eye(c):
    for pts in [((4,18),(8,12),(16,12),(20,18)),((20,18),(16,24),(8,24),(4,18))]:
        a,b,d,e=pts
        c.line([tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*d[j]+t**3*e[j] for j in (0,1)) for t in [i/32 for i in range(33)]],radius=0)
def turn(c,x=17,y=17,r=4):
    c.line(arc_points(x,y,r,200,520,28),True,radius=0)
    c.line([(x-r-1,y-1),(x-r,y+2),(x-r+3,y+1)],True,radius=.3)
def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='resource.availability-step-add':
        c.line([(3,3),(3,21),(21,21)],radius=.2)
        c.line([(6,17),(6,12),(13,12),(13,6),(20,6)],radius=.3);c.plus(18,16,3)
    elif key=='calendar.edit':
        calendar(c)
        c.line([(11,20),(18,13),(21,16),(14,23),(10,23)],True,closed=True,radius=.3)
    elif key=='resource.unlink-library':
        person(c,7,6)
        c.line([(14,11),(17,8),(21,12),(18,15)],True,radius=.5)
        c.line([(13,14),(10,17),(14,21),(17,18)],True,radius=.5)
        c.line([(18,5),(19,3)],True,radius=0)
        c.line([(21,8),(23,7)],True,radius=0)
    elif key=='status.library-linked':
        box(c,3,3,18,18);c.line([(8,3),(8,21)],radius=0)
        c.line([(12,10),(15,13),(20,8)],radius=.3)
    elif key in ('ai.pause','ai.resume'):
        frame(c)
        if key=='ai.pause':
            for x in (9,15):c.line([(x,11),(x,18)],True,radius=0)
        else:c.line([(9,10),(17,14),(9,19)],True,closed=True,radius=.3)
    elif key=='ai.read-only-toggle':
        frame(c)
        c.line([(6,11),(10,11)],radius=0);c.line([(6,16),(9,16)],radius=0)
        box(c,12,14,8,6,True)
        c.line(arc_points(16,14,3,180,360,20),True,radius=0)
    elif key=='backup.auto':
        copies(c);turn(c)
    elif key=='backup.create':
        copies(c);c.plus(14,14,3.5)
    elif key=='backup.folder':
        c.line([(2,7),(2,21),(22,21),(22,7),(11,7),(9,4),(2,4)],closed=True,radius=.4)
        turn(c,15,15,4)
    elif key in ('credential.show','credential.hide'):
        field(c);eye(c)
        if key=='credential.show':c.circle(12,18,2,True)
        else:c.line([(7,13),(17,23)],True,radius=0)
    elif key=='credential.regenerate':
        field(c);turn(c,12,18,4)
    elif key in ('ai.connection-menu','ai.connection-details'):
        frame(c)
        c.line([(7,10),(7,13),(15,13),(15,10)],True,radius=.3)
        c.line(arc_points(11,13,4,0,180,18),True,radius=0)
        c.line([(11,17),(11,20)],True,radius=0)
        if key=='ai.connection-menu':c.line([(17,17),(19,19),(21,17)],True,radius=.3)
        else:
            c.circle(19,10,.6,False,True);c.line([(19,13),(19,16)],radius=0)
    elif key=='update.install':
        c.line([(3,8),(12,3),(21,8),(21,21),(3,21)],closed=True,radius=.5)
        c.line([(3,8),(12,12),(21,8)],radius=.3)
        c.line([(12,12),(12,19)],True,radius=0)
        c.line([(8,15),(12,19),(16,15)],True,radius=.3)
    elif key=='documents.overview':
        for x,y in ((2,3),(9,3),(2,13),(9,13)):box(c,x,y,5,8)
        c.line([(18,5),(22,5),(22,20),(18,20)],True,radius=.3)
    elif key=='documents.new-or-open':
        frame(c);c.plus(8,14,3)
        c.line([(14,14),(21,14)],True,radius=0)
        c.line([(18,11),(21,14),(18,17)],True,radius=.3)
    elif key in ('tabs.scroll-start','tabs.scroll-end'):
        box(c,2,3,20,8)
        for x in (8,15):c.line([(x,3),(x,11)],radius=0)
        left=key=='tabs.scroll-start'
        c.line([(15 if left else 9,14),(9 if left else 15,18),(15 if left else 9,22)],True,radius=.3)
    elif key=='activity.clear':
        box(c,3,3,18,18)
        for y in (7,12,17):c.line([(7,y),(13,y)],radius=0)
        c.line([(15,14),(22,21)],True,radius=0);c.line([(15,21),(22,14)],True,radius=0)
    return True
