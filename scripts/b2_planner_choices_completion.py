"""Planner ribbon menus, Backstage and layout identity glyphs on the pinned source."""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_planner_ribbon_completion import bars,person,arrow

GROUPS={131:'Referenties, peildatum en relaties',132:'Resourcekeuzes en Gantt-weergave',133:'Bestandmenu en projectbibliotheek',134:'Indelingsiconen voor taken',135:'Indelingsiconen voor resources',136:'Indelingsiconen voor kenmerken'}
ROWS=[
 (131,'planning.baselines','Referentieplanningen beheren','De gemonteerde referentieplanningsdialoog openen; geen referentie onmiddellijk opslaan of overlay omschakelen.','ff4f8d6c5b8d84d7'),
 (131,'planning.status-date','Peildatum','Vaste aanduiding bij het peildatumveld; DateTextInput commit de datum via setStatusDate. Het icoon is geen kalenderknop.','83eb7897510d5055'),
 (131,'planning.clear-status-date','Peildatum wissen','De projectpeildatum verwijderen via setStatusDate(undefined); geen datum op vandaag zetten of invoervenster sluiten.','718f564998ef2db2'),
 (131,'planning.progress-menu','Referenties en voortgang','Het compacte lintmenu met referentiebeheer, peildatum en voortgangsmodus openen; geen mijlpaal invoegen.','8c176c4b1efc1949'),
 (131,'task.milestone-menu','Mijlpaal toevoegen','Het menu openen voor een start-, eind- of verplichte inspectiemijlpaal; de keuze voegt pas daarna de passende taak toe.','098fea350a1d889c'),
 (131,'planning.relations-menu','Taakrelaties kiezen','Het menu openen voor relatie-tekenmodus, twee geselecteerde taken koppelen, een externe relatie of externe ankers vernieuwen.','376bf5f9f84c52f8'),
 (131,'wbs.templates','WBS-sjablonen kiezen','Het menu met opgeslagen taakstructuren openen; keuze gebruikt insertWbsTemplate onder de geselecteerde taak of projectwortel.','7731669e788edf87'),
 (132,'resource.assign','Resource toewijzen','Het toewijzingsmenu voor één niet-mijlpaalbladtaak openen; de resourcekeuze bewaart de eenheden per dag en belastingscurve via assignResource.','187c5d4303dc8c30'),
 (132,'planning.bar-colors','Planningskleuren kiezen','Het menu voor balkkleuren volgens kritisch pad, automatisch of categorieveld openen; keuze werkt setOverlays barColors bij.','aba618d721e22e4c'),
 (132,'list.sort-fields','Sorteervelden kiezen','Het menu openen voor meerdere sorteervelden met richting; wijzigen gebruikt setSort voor de taakweergave.','93d208e2371b5c7b'),
 (132,'layout.manage','Indelingen beheren','Het dialoog voor een nieuwe of bestaande bewaarde weergave-indeling openen; nieuwe-indelingsknop wist eerst layoutDialogTargetId.','fcd476adddffe0d2'),
 (132,'view.gantt-split','Twee tijdschalen tonen','De tweede Gantt-weergave omschakelen met een eigen zoom en horizontale scrollpositie; geen tabelcel of taak splitsen.','654bfc09b1a288e2'),
 (132,'view.minimap','Planningsoverzicht tonen','De kleine navigatiekaart van de Gantt omschakelen en de voorkeur bewaren; geen geografische kaart openen.','4396fcf679e77427'),
 (132,'status.resource-overallocated','Resourceoverbelasting','Alleen bij overbelaste resources naast hun aantal tonen; dit is een foutgekleurde overbelastingsstatus, geen opdracht of waarschuwingenpaneel.','1ad22a16a4c8ca66'),
 (133,'file.examples','Voorbeeldprojecten','Het paneel met meegeleverde voorbeeldprojecten tonen; pas een voorbeeldkaart haalt het bestand op en opent het als voorbeeld.','30ce5906f2aa1ed2'),
 (133,'ui.tour','Rondleiding starten','Backstage sluiten en de begeleide rondleiding vanaf stap nul tonen via showTourOverlay en tourStepIndex.','973e9ab120076663'),
 (133,'company.library','Bedrijfsbibliotheek','De bedrijfsbibliotheek in Backstage tonen of een bibliotheek uit de lijst selecteren; geen gebouw in een model invoegen.','c64d4907849c0cfb'),
 (133,'report.print-entry','Naar afdrukvoorbereiding','Het PrintSection-paneel met de ingang naar afdrukvoorbeeld tonen; de navigatieknop drukt niets af. De vervolgrouting wordt hiermee niet als werkende print bewezen.','c30722810efc2e68'),
 (134,'layout.identity','Algemene indeling','Herkenningsteken layout in de indelingsicoonkiezer; legt alleen de icon-sleutel bij de opgeslagen indeling vast.','835627b22da03b01'),
 (134,'layout.task-tree','Boomindeling herkennen','Herkenningsteken tree voor een eigen indeling; icoonkeuze wijzigt geen taakhiërarchie.','a0b22af901da4abb'),
 (134,'layout.filter','Filterindeling herkennen','Herkenningsteken filter voor een opgeslagen indeling; icoonkeuze stelt zelf geen filtercriteria in.','b1a25eafedda8a4a'),
 (134,'layout.critical','Kritiekpadindeling herkennen','Herkenningsteken critical voor een indeling; de icoonkeuze berekent of filtert geen kritisch pad.','04e0c1b328946ccb'),
 (134,'layout.milestone','Mijlpaalindeling herkennen','Herkenningsteken milestone voor een indeling; geen mijlpaaltaak toevoegen.','bd63aec6fb2efea1'),
 (135,'layout.resources','Resource-indeling herkennen','Herkenningsteken users voor indelingen, ook de meegeleverde resourcegroepering; het beeld zelf wijst geen resources toe.','81423903cd9c00df'),
 (135,'layout.crew','Ploegindeling herkennen','Herkenningsteken crew voor een eigen opgeslagen indeling; icoonkeuze maakt geen ploeg of taak aan.','560b16086d037090'),
 (135,'layout.equipment','Materieelindeling herkennen','Herkenningsteken equipment voor een eigen opgeslagen indeling; icoonkeuze beheert geen materieel.','5d4057bd24b918fa'),
 (135,'layout.tools','Gereedschapsindeling herkennen','Herkenningsteken tools voor een eigen opgeslagen indeling; icoonkeuze voert geen gereedschap uit.','6eedad8e3e95fab0'),
 (136,'layout.flag','Gemarkeerde indeling herkennen','Herkenningsteken flag voor een opgeslagen indeling; geen taak markeren of voortgangsmenu openen.','fff9861e74124fbf'),
 (136,'layout.period','Periode-indeling herkennen','Herkenningsteken period voor een opgeslagen indeling; icoonkeuze wijzigt geen tijdschaal of kalender.','83c53d77b9521056'),
 (136,'layout.star','Sterindeling herkennen','Herkenningsteken star voor een opgeslagen indeling; alleen een visuele keuze, geen favorietstatus omschakelen.','db3e899106aed8bf'),
]
GROUPS[137]='Bibliotheekstandaard en kalenders'
ROWS += [
 (137,'company.new','Resourcebibliotheek toevoegen','Een nieuwe bedrijfsresourcebibliotheek met een lege pool maken en selecteren via addCompany.','e6f839d4a560f61a'),
 (137,'company.default','Standaardbibliotheek instellen','De geselecteerde bibliotheek als standaard bewaren via setDefaultCompany; verandert geen projecttoewijzing.','ef1ab403d03e494b'),
 (137,'company.default-status','Standaardbibliotheek','Vaste aanduiding naast de standaardbibliotheek in de lijst; geen actieknop en geen favorietstatus.','f8a565b9eb0bd029'),
 (137,'calendar.promote-menu','Projectkalender kiezen voor bibliotheek','De lijst met projectkalenders openen of sluiten om er één naar de geselecteerde bibliotheek over te nemen; nog geen kalender kopiëren.','850c3d2b45dbf223'),
 (137,'calendar.promote','Kalender in bibliotheek opnemen','De gekozen projectkalender kopiëren naar de bedrijfsbibliotheek met nieuwe pool-identiteit en een bijgewerkte poolversie.','4998a138a2973703'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De bepalende markering blijft ononderbroken zichtbaar voor de dragende lijn.' for k in KEYS}
SEMANTIC={'status.resource-overallocated':'error','company.default-status':'text-secondary'}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}
EVIDENCE={k:'LayoutIcon-registry, alle radio-opties en setIcon in LayoutsDialog gelezen: dit beeld identificeert de opgeslagen indeling, geen autonome planningsopdracht.' for k in KEYS if k.startswith('layout.') and k!='layout.manage'}
EVIDENCE['report.print-entry']='Backstage goTo(print) toont PrintSection. De vervolgbinding zet report maar roept daarna onClose/closeBackstage aan, dat start zet; die vervolgroute bewijst dus geen blijvende rapportpreview. Alleen de werkelijk werkende paneelnavigatie is beoordeeld.'
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)
reuse('ca344ec4b2609133','planning.baselines','De compacte variant roept dezelfde onManageBaselines/showBaselineDialog aan en sluit het compacte menu.')
reuse('37f04d7c7e13805e','resource.assign','Disabled-variant van dezelfde toewijzingsknop wanneer de selectie geen geldige bladtaak is; geen afzonderlijke functie.')
reuse('d96e936d65731df7 63d6cb57e14a4554','project.recent','Lint toont recent-bestandenmenu; Backstage toont RecentSection. De afzonderlijke bestandsrij roept openRecentFile aan.')
reuse('9f8ee25e85821b19 252adfc2f67a4580','file.export-options','Lint opent de EXPORT_FORMATS-keuzelijst; Backstage opent ExportSection met formaatkaarten. Nog geen bestand exporteren op de trigger.')
reuse('3e3c614c467a7688','extension.item','Fallback voor een dynamische extensieknop in ExtensionIcon; de extensie levert eigen label en onClick. Geen nieuwe vaste functie voor onbekende runtimeknoppen.')
reuse('bf8f9b68b38e0411','edit.delete','deleteWbsTemplate verwijdert het gekozen opgeslagen taakstructuursjabloon uit de lokale opslag; geen projecttaken wissen.')
reuse('7dff0d454f687648 678071bd08abb307','list.filter','Opent de werkende filtereditor of opgeslagen filterpresets; keuzes gebruiken setFilter/applyLayout en de bestaande dialoog.')
reuse('6b9fc5171723a8bb','table.columns','DisplayGroupContent gebruikt dezelfde useColumnsButtonBinding: activeRibbonTab table en showColumnsDialog true.')
reuse('85027d5edbf3fff6','list.group-by','LevelListEditor kiest maximaal twee groeperingsvelden met richting via setGroup. Dit is taaklijstgroepering; het oude objectgroeperingsconflict is opgelost.')
reuse('4b7ce424f249ce27','view.zoom-in','Verhoogt Gantt zoom met ZOOM_STEP.')
reuse('e5339d8c3ac7384d','view.zoom-out','Verlaagt Gantt zoom met ZOOM_STEP.')
reuse('ca9ea487822b769a','view.zoom-default','Zet alleen Gantt zoom op DEFAULT_ZOOM=30 (dagbreedte). Geen object zichtbaar maken of fysieke 1:1-maat claimen.')
reuse('c795049a0794ffee','view.fit','requestFitToProject zet pendingFit; de viewportcoördinator past computeFitToProject toe op alle taken en past zoom, startdatum en scroll aan.')
reuse('49adee11e7ec6aab','view.fullscreen','Presentatiemodus verbergt appchrome en vraagt browserfullscreen. Bij geweigerde fullscreen blijft de presentatie-indeling actief.')
reuse('ef3c38058334c481','view.fullscreen-exit','De actieve presentatiemodus uitschakelen en eventueel document.exitFullscreen aanroepen; geen zoom-fit.')
reuse('bf36f2053531d29b','ui.close','Backstage-terug sluit alleen het bestandmenu via activeRibbonTab start, met controle op niet-toegepaste projectgegevens.')
reuse('5c4d5ed61d33915e','file.new','handleNewProject opent showNewProjectDialog; bestandmenu sluiten staat los van projectaanmaak.')
reuse('1d01dc961f8b5420','file.open','handleOpen roept openFile aan met vertaalde labels, na de guard voor niet-toegepaste gegevens.')
reuse('f2ed79a414b9bba1','file.save','handleSave roept saveFile aan voor het actieve project.')
reuse('069e1819a4e4d3bc','file.save-as','handleSaveAs roept saveFileAs aan voor een andere identiteit/bestemming.')
reuse('df84020ae55f7194','project.properties','goTo(project-info) toont ProjectInfoPanelContent; wijzigingen hebben Toepassen/Verwerpen en een vertrekguard.')
reuse('cbc28e7474970e53','ui.settings','goTo(settings) toont SettingsPanelContent.')
reuse('0fd95561b6e94b6f','document.close','closeWithGuard ontvangt het actieve document-ID en isDirty; sluit dit project met wijzigingscontrole, niet de applicatie.')
reuse('2076583c78711ed0','file.type-other','Generieke bestandsaanduiding bij een recente bestandsrij; de rij opent via openRecentFile.')
reuse('8ccd2332536732b5','extensions.manage','Toont de gemonteerde ExtensionManagerPanel binnen Backstage als extensies zijn ingeschakeld.')
reuse('42388a08ef23c87c','file.import','Opent het invoerpaneel met voortgangsimport en beschikbare extensie-importers; nog geen bestand onmiddellijk verwerken.')
reuse('9e6dcadc8964bce3','file.import','Fallback voor een extensie-importkaart: handleImport vraagt een bestand van het ondersteunde formaat en roept importWithExtension aan.')
reuse('acf389eb0155b191','file.open','De voorbeeldkaart haalt het meegeleverde bestand op en opent het via openExampleFromString; een showcase krijgt daarna demobibliotheekgegevens.')
reuse('6a7f172ff11ca354','ui.help','goTo(help) toont het gemonteerde HelpPanel.')
reuse('f9a00ea83f3c04e5','file.import','Concrete voortgangsimportkaart zet showProgressImportDialog true en gaat naar Start; uitgeschakeld zonder taken.')


reuse('a879e47ef01d90df','company.library','De bibliotheekrij selecteert selectedId en toont de bijbehorende pool; geen gebouwmodel plaatsen.')
reuse('adf656c269386c12 b210d03d3a6f116c','edit.delete','Bibliotheek verwijderen vraagt bevestiging en bewaart minstens één bibliotheek; kalender verwijderen gebruikt removePoolCalendar voor de gekozen pool.')
reuse('386a8b971ab86288','file.export','exportPoolIFC maakt bibliotheek-IFC en saveFileDialog bewaart die bytes; geen actieve projectplanning exporteren.')
reuse('fc90833de8feb0fc','file.import','Opent het gemonteerde PoolImportDialog met de gekozen doelbibliotheek-ID; nog geen pool direct overschrijven.')
reuse('62697f47d954dc3b','calendar.promote','Hetzelfde opneemteken als vaste uitleg bij de kalenderlijst; dit gebruik heeft zelf geen klikhandler.')
reuse('24c8db84f6e08d28','object.rename','Opent de inline naameditie van de bibliotheekkalender; geen datumrooster wijzigen.')
reuse('07ba9181dc7fe29a','status.success','Alleen bij een geslaagde kalenderovername staat notice met Check naast de bevestigingstekst.')
reuse('3ec677ea282a1b84','data.apply','saveEditCalendar commit de niet-lege kalendernaam via updatePoolCalendar en sluit de inline editor.')
reuse('2f73b6ad9106a238','data.discard','Verlaat de inline naameditie zonder updatePoolCalendar; bij opnieuw openen wordt calDraft uit de opgeslagen kalendernaam gevuld.')


def calendar(c):
    box(c,3,5,18,16);c.line([(3,10),(21,10)],radius=0)
    for x in (8,16):c.line([(x,3),(x,7)],radius=0)
def page(c,x=3,y=3,w=18,h=18):box(c,x,y,w,h)
def flag(c,x=6,y=3):
    c.line([(x,21),(x,y)],radius=0)
    c.line([(x,y),(20,y),(17,y+4),(20,y+8),(x,y+8)],True,closed=True,radius=.3)
def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='planning.baselines':
        bars(c,baseline=True);c.circle(19,5,3,True)
    elif key in ('planning.status-date','planning.clear-status-date'):
        calendar(c)
        if key=='planning.status-date':
            c.circle(12,16,3,True);c.line([(12,13),(12,16),(14,16)],True,radius=.2)
        else:
            c.line([(9,13),(15,19)],True,radius=0);c.line([(9,19),(15,13)],True,radius=0)
    elif key=='planning.progress-menu':
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        c.line([(6,12),(14,12)],True,radius=0);c.line([(6,17),(12,17)],True,radius=0)
        c.line([(16,15),(18,17),(20,15)],True,radius=.3)
    elif key=='task.milestone-menu':
        c.line([(10,3),(18,11),(10,19),(2,11)],closed=True,radius=.4)
        c.plus(19,19,3)
    elif key=='planning.relations-menu':
        box(c,2,4,7,6);box(c,14,14,7,6)
        c.line([(6,10),(6,12),(17,12),(17,14)],radius=.3)
        c.line([(15,3),(18,6),(21,3)],True,radius=.3)
    elif key=='wbs.templates':
        box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0)
        c.line([(7,11),(7,17),(12,17)],True,radius=.3);box(c,13,14,5,5,True)
    elif key=='resource.assign':
        person(c,7,6);box(c,14,14,8,7);arrow(c,15,7,True)
    elif key=='planning.bar-colors':
        bars(c,True)
        c.circle(18,5,2);c.circle(21,9,1.5)
    elif key=='list.sort-fields':
        for y,w in ((4,7),(11,11),(19,14)):c.line([(2,y),(2+w,y)],radius=0)
        c.line([(20,3),(20,19)],True,radius=0);c.line([(17,16),(20,19),(23,16)],True,radius=.3)
    elif key=='layout.manage':
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0);c.line([(10,7),(10,21)],radius=0)
        c.plus(16,15,3)
    elif key=='view.gantt-split':
        box(c,2,3,20,18);c.line([(2,12),(22,12)],True,radius=0)
        c.line([(6,7),(15,7)],radius=0);c.line([(10,17),(18,17)],radius=0)
    elif key=='view.minimap':
        box(c,2,3,20,18)
        c.line([(5,7),(16,7)],radius=0);c.line([(9,11),(19,11)],radius=0)
        box(c,12,14,8,5,True)
    elif key=='status.resource-overallocated':
        c.line([(12,2),(23,21),(1,21)],closed=True,radius=.5)
        c.circle(12,10,2)
        c.line(arc_points(12,18,3.3,180,360,16),radius=0)
    elif key=='file.examples':
        c.line([(2,5),(7,3),(12,5),(17,3),(22,5),(22,21),(17,19),(12,21),(7,19),(2,21)],closed=True,radius=.4)
        c.line([(12,5),(12,21)],radius=0)
        for y in (9,14):c.line([(5,y),(9,y)],True,radius=0)
        c.line([(15,9),(19,9)],True,radius=0)
    elif key=='ui.tour':
        c.line([(3,20),(8,20),(8,6),(19,6)],radius=.4)
        for x,y in ((3,20),(19,6)):c.circle(x,y,2)
        c.line([(8,8),(15,11),(8,14)],True,closed=True,radius=.3)
    elif key=='company.library':
        box(c,3,3,18,18);c.line([(8,3),(8,21)],radius=0)
        for x in (12,17):
            for y in (7,12):c.circle(x,y,.7,True,True)
        c.line([(12,21),(12,17),(17,17),(17,21)],True,radius=.3)
    elif key=='report.print-entry':
        box(c,2,8,20,10);box(c,6,3,12,5)
        c.line([(7,18),(7,22),(17,22),(17,18)],radius=.3)
        c.line([(9,12),(12,15),(15,12)],True,radius=.3)
    elif key=='layout.identity':
        box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0);c.line([(9,8),(9,21)],radius=0)
        box(c,12,11,6,7,True)
    elif key=='layout.task-tree':
        c.line([(4,3),(4,17),(10,17)],radius=.3);c.line([(4,8),(10,8)],radius=0)
        for y in (5,14):box(c,11,y,10,6,True)
        c.circle(4,3,1.2,False,True)
    elif key=='layout.filter':
        box(c,3,3,18,18)
        c.line([(6,7),(18,7),(14,12),(14,17),(10,18),(10,12)],True,closed=True,radius=.3)
    elif key=='layout.critical':
        for x,y in ((4,4),(4,20),(20,4),(20,20)):c.circle(x,y,1.7)
        c.line([(4,4),(4,12),(20,12),(20,20)],True,radius=.4)
        c.line([(20,4),(20,8)],radius=0);c.line([(4,16),(4,20)],radius=0)
    elif key=='layout.milestone':
        c.line([(3,18),(21,18)],radius=0);c.line([(12,3),(19,10),(12,17),(5,10)],True,closed=True,radius=.4)
        for x in (3,21):c.line([(x,15),(x,21)],radius=0)
    elif key=='layout.resources':
        person(c,8,6);person(c,17,8)
        c.line([(3,21),(21,21)],True,radius=0)
    elif key=='layout.crew':
        c.line(arc_points(12,15,8,180,360,24),radius=0)
        c.line([(2,15),(22,15),(22,18),(2,18)],closed=True,radius=.3)
        c.line([(9,11),(9,5),(15,5),(15,11)],True,radius=.4)
    elif key=='layout.equipment':
        box(c,2,5,12,12);c.line([(14,9),(19,9),(22,13),(22,17),(14,17)],closed=True,radius=.3)
        for x in (6,18):c.circle(x,18,2.5,True)
        c.line([(17,10),(17,13),(21,13)],radius=.2)
    elif key=='layout.tools':
        c.line([(8,6)]+arc_points(7,7,4,315,585,36)+[(6,6)],radius=.2)
        c.line([(10,10),(17.2,17.2)],radius=0)
        c.circle(19,19,2.5,True)
    elif key=='layout.flag':flag(c)
    elif key=='layout.period':
        calendar(c);c.line([(7,16),(17,16)],True,radius=0)
        for x in (7,17):c.line([(x,13),(x,19)],True,radius=0)
    elif key=='layout.star':
        pts=[]
        for i in range(10):
            a=math.radians(-90+36*i);r=10 if i%2==0 else 4.5
            pts.append((12+r*math.cos(a),12+r*math.sin(a)))
        c.line(pts,True,closed=True,radius=.35)
        c.circle(12,12,1.2)
    elif key=='company.new':
        box(c,3,3,16,18);c.line([(8,3),(8,21)],radius=0);c.plus(18,17,4)
    elif key in ('company.default','company.default-status'):
        if key=='company.default':
            box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0)
            c.line([(7,15),(10,18),(17,11)],True,radius=.3)
        else:
            pts=[]
            for i in range(10):
                a=math.radians(-90+36*i);r=9 if i%2==0 else 4
                pts.append((12+r*math.cos(a),12+r*math.sin(a)))
            c.line(pts,closed=True,radius=.35)
    elif key=='calendar.promote-menu':
        calendar(c);c.plus(12,16,3)
    elif key=='calendar.promote':
        box(c,2,4,12,10);c.line([(2,8),(14,8)],radius=0)
        c.line([(4,19),(14,19)],radius=0)
        c.line([(20,20),(20,4)],True,radius=0)
        c.line([(17,7),(20,4),(23,7)],True,radius=.3)
    return True
