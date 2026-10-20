"""Complete the missing Installer scope and explicit planned UI designs."""
import math
from b2_source_catalog import supplemental_catalog
from b2_second_series import box
from b2_planner_safety_completion import turn
from b2_reports_completion import glyph
from b2_font_geometry import font_sources
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

SID={r['name']:r['id'] for r in supplemental_catalog()['records']}
GROUPS={158:'Toolcategorieën: techniek',159:'Toolcategorieën: werkvelden',160:'Apps kiezen en openen',161:'Installaties en versies',162:'Webtools en decimalen',163:'Geplande documentgereedschappen',164:'Geplande opmerkingenuitwisseling',165:'Geplande BIM-bediening',166:'Geplande documentpanelen en afdrukvoorkeuren'}
ROWS=[]
for series,code,label in [(158,'calculatie','Calculatie'),(158,'cad','CAD'),(158,'constructief','Constructief'),(158,'geotechniek','Geotechniek'),(158,'bim','BIM'),(159,'planning','Planning'),(159,'documenten','Documenten'),(159,'ai','AI en spraak'),(159,'energie','Energie'),(159,'veld','Veldwerk'),(159,'gis','GIS')]:
    ROWS.append((series,'tools.category-'+code,label+'-categorie','Vaste onderwerpidentiteit voor de toolcategorie '+label+' in de appcatalogus, previewfallback en webtooltab; geen ontwerp- of rekenopdracht.',SID['category-'+code]))
ROWS += [
 (160,'software.catalog','Appcatalogus tonen','Naar de vaste catalogustab met beschikbare desktopapps en webtools gaan; reeds geopende webtooltabs blijven behouden.',SID['catalog']),
 (160,'software.launch','Geïnstalleerde app starten','De bekende lokale executable via launchTool starten; geen bestand openen, opname beginnen of installatie downloaden.',SID['launch']),
 (160,'software.open-webtab','Webtool in tab openen','De webversie via openTab in een interne iframe-tab openen of activeren; een bestaande tab behoudt haar sessie.',SID['webtab']),
 (161,'software.install','App installeren','Het gekozen releasepakket downloaden en de platforminstallatie uitvoeren of starten: Linux beheerde AppImage, Windows setup. Geen extensiepakket of projectbestand importeren.',SID['install-or-update']),
 (161,'software.update','App met releasepakket bijwerken','Het beschikbare opvolgpakket downloaden en het bestaande platforminstallatiepad volgen. Bij eigen AppImage-vervanging volgt een herstartinstructie; geen automatische herstart of backupflush beloven.',SID['self-update']),
 (161,'status.software-installed','Appversie geïnstalleerd','De lokaal aangetroffen versie aanduiden; deze vaste toestand zegt niet dat de versie actueel is.',SID['installed-version']),
 (161,'status.version-upgrade','Beschikbare opvolgversie','Vaste richting van geïnstalleerde naar beschikbare nieuwere versie in de versievergelijking; geen updateactie op dit beeld.',SID['version-upgrade']),
 (162,'view.web-reload','Webtool herladen','Het iframe van de huidige webtool opnieuw aanmaken via reloadKey; hierdoor wordt de pagina opnieuw geladen. Geen andere tab of release-inventaris vernieuwen.',SID['web-reload']),
 (162,'format.decimals-increase','Meer decimalen','spreadsheet-action decimals-up verhoogt de getoonde decimalen van iedere geselecteerde cel met één, vanaf de standaardwaarde twee; de celwaarde zelf blijft gelijk.',SID['decimals-up']),
 (163,'draw.qr-code','QR-code plaatsen — gepland','Ontwerp voor het plaatsen van een QR-code op het document. De onderzochte oude setTool(qrCode)-route heeft geen geregistreerde handler; de functie is nog niet aangesloten.','2a8ef385de25c748'),
 (163,'draw.schedule-table','Tekeningtabel plaatsen — gepland','Ontwerp voor het plaatsen van een tabel op het tekenblad. Drawing Table is permanent disabled omdat scheduleTable niet geregistreerd is; geen werkende uitvoering claimen.','f3883c39a1b2785f'),
 (163,'view.zoom-tool','Zoomgereedschap — gepland','Ontwerp voor het interactieve in-/uitzoomgereedschap in het paginacontextmenu. De onderzochte setTool(zoom)-route heeft geen handler; de werkende losse zoomknoppen blijven afzonderlijk.','bc51cb10ad02cc5e'),
 (164,'comments.summarize','Opmerkingen samenvatten — gepland','Ontwerp voor een overzicht/samenvatting van documentopmerkingen; geen AI-documentsamenvatting. De bronmenuactie is disabled en heeft geen callback.','991333aa7e9a41aa'),
 (164,'comments.import','Opmerkingen importeren — gepland','Ontwerp voor invoer van documentopmerkingen. De bronmenuactie is disabled en heeft geen callback; bestandsformaat en invoerroute zijn nog niet vastgelegd.','d2741f870c014d63'),
 (164,'comments.export','Opmerkingen exporteren — gepland','Ontwerp voor uitvoer van alle of de geselecteerde documentopmerkingen. Beide bronmenuacties zijn disabled zonder callback; de scope hoort in het label.','ed6cd72ad90a9ea6'),
 (165,'integration.platform-sync','Platform synchroniseren — gepland','Ontwerp voor de benoemde platform-synchronisatie in het BIM-lint. onSyncPlatform is niet door AppShell ingevuld; overdrachtsinhoud en protocol zijn nog niet vastgelegd.','aa5e16bc4b81b412'),
 (165,'validation.select-specification','IDS-specificatie kiezen — gepland','Ontwerp voor het kiezen van de IDS-specificatie bij de modeltoetsing. Deze IDS Standaard-lintknop heeft geen callback; de bestaande IDS-werkruimte is een afzonderlijke functie.','4d5ed0c958d22668'),
 (165,'validation.reset','Validatietoestand herstellen — gepland','Ontwerp voor Reset bij de modelvalidatie. De bron geeft onResetValidation niet door; de precieze resetinhoud is nog niet aangesloten. Dit is geen bewezen opdracht om alleen 3D-markeringen te wissen.','5ea99a4a22dd643f'),
 (166,'panel.document-navigation','Documentnavigatie — gepland','Ontwerp voor het Navigation-paneel in PDF v3; de knop meldt uitsluitend een nog niet geïmplementeerde actie. De precieze paneelinhoud wordt niet als werkend voorgesteld.','5dd7e03fb2f5d16e'),
 (166,'panel.tool-palette','Gereedschapspalet — gepland','Ontwerp voor het apart benoemde Tool Palette in PDF v3; de knop heeft alleen de action-todo-route. Geen symboolbibliotheek of kleurkiezer.','5266ce44bd01a4e8'),
 (166,'preferences.printing','Afdrukvoorkeuren — gepland','Ontwerp voor de Print-categorie in de voorkeurendialoog van PDF v3; de inhoud toont Coming soon. Dit start geen afdruktaak.','3d72b875fda7bc5f'),
 (166,'panel.model-tree','Modelstructuur — gepland','Ontwerp voor het IFC Tree-paneel in de oude Calculations-webinterface. De knop heeft geen handler in main.ts; dit is geen boomindeling van planningstaken.','54ae530559493bfb'),
 (166,'edit.select-text','Documenttekst selecteren — gepland','Ontwerp voor het afzonderlijk benoemde tekstselectiegereedschap in het oude PDF-paginamenu. De selectText-route heeft geen geregistreerde handler; objectselectie blijft een ander contract.','bcba3c77347357aa'),
]
KEYS={r[1] for r in ROWS}
PLANNED_KEYS={r[1] for r in ROWS if r[0]>=163}|{'nav.forward','nav.home'}
PLANNED={r[4]:r[3] for r in ROWS if r[1] in PLANNED_KEYS}
PLANNED['68098cc741a51f9f']='GEPLAND BASISONTWERP: het behouden Vooruit-icoon heeft hier alleen een permanent disabled bronknop zonder callback.'
ACCENT_FRONT={k:'De bepalende markering blijft vóór de dragende contour volledig zichtbaar.' for k in KEYS}
SEMANTIC={'status.software-installed':'text-secondary','status.version-upgrade':'text-secondary'}
TYPOGRAPHY={'format.decimals-increase':{**font_sources()['format.color'],'glyph':'0','purpose':'Cijfer voor decimale celopmaak; Space Grotesk Medium, passend bij Minder decimalen.'}}
REUSED={};EXCLUDED={SID['brand']:'OpenAEC-merkbeeld, geen functieicoon. Bronlogo en vectorpaden worden niet in de B2-functiefamilie overgenomen.'}
DISPATCHERS={SID['category-dispatch']:tuple('tools.category-'+k for k in ('calculatie','cad','constructief','geotechniek','bim','planning','documenten','ai','energie','veld','gis')),
             SID['preview-open']:('software.open-webtab','link.open-external'),
             SID['install-or-update']:('software.install','software.update')}
DISPATCH_EVIDENCE={
 SID['category-dispatch']:'CategoryIcon kiest paths[category]; alle elf typed varianten hebben een eigen onderwerpontwerp. Dezelfde renderer staat in kaartkop, previewfallback en tooltab.',
 SID['preview-open']:'ToolCard.shortcut: bij webUrl onOpenTab; anders open(externalTarget) via openUrl. De omringende preview voert de actie uit. De aparte launch-tak staat op een eigen bronplaats.',
 SID['install-or-update']:'Dezelfde tekstknop en handleInstall kiezen een eerste installatie of opvolgversie op basis van status. downloadAndRunInstaller heeft platformspecifieke uitkomsten; geen appherstart beloven.'}
EVIDENCE={k:'Concrete aanvullende bronplaats, callback en gegevensroute op de vastgelegde commit gelezen; eigen B2-geometrie.' for k in KEYS}
for _,k,_,meaning,_ in ROWS:
    if k in PLANNED_KEYS:EVIDENCE[k]='GEPLAND ONTWERP; de onderzochte bronbediening werkt nog niet. '+meaning
def reuse(name,key,reason):REUSED[SID[name]]=(key,reason)
reuse('search','view.search','App.matches filtert de toolnaam, vertaalde omschrijving en categorie; het vaste zoekbeeld staat naast de invoer.')
reuse('refresh','ui.refresh','refresh(true) scant geïnstalleerde tools en haalt releasegegevens. Terwijl refreshing waar is draait hetzelfde beeld en is de knop disabled; geen CPM-berekening.')
reuse('modal-close','ui.close','Het times-teken sluit de lokale Modal via de doorgegeven onClose.')
reuse('update-available','status.update-available','Vaste melding bij compareVersions(current,latest)<0; het downloadbeeld zelf start de update niet.')
reuse('update-dismiss','ui.close','De X zet selfUpdateDismissed voor deze sessie; geen update verwijderen of installeren.')
reuse('tab-close','ui.close','De X sluit de geselecteerde webtooltab via closeTab, zonder het appvenster te sluiten.')
reuse('select','ui.dropdown','De trigger opent de keuzelijst; de optie bepaalt de waarde via onChange.')
reuse('theme-menu','ui.dropdown','De trigger opent de themakeuze; de aparte optie kiest het thema.')
reuse('settings','ui.settings','TitleBar.onSettingsClick zet settingsOpen in App.')
reuse('minimize','window.minimize','De native minimize-handler is gekoppeld.')
reuse('restore','window.restore','isMaximized toont de herstelvariant van toggleMaximize.')
reuse('maximize','window.maximize','De normale venstertoestand toont de maximaliseervariant van toggleMaximize.')
reuse('window-close','window.close','De titelbalkknop roept native close aan; geen lokale tab of dialoog.')
for name in ('repository-link','web-external','website','webtool-external'):
    reuse(name,'link.open-external','De concrete URL wordt via openUrl extern geopend. De oorspronkelijke merk- of webvorm wordt niet gekopieerd; geen repositorybewerking of bestandsoverdracht.')

def browser(c):
    box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0)
def package(c):
    box(c,3,5,16,16);c.line([(3,10),(19,10)],radius=0)
    c.line([(7,5),(7,10)],radius=0)
def comment(c):
    c.line([(3,3),(20,3),(20,16),(11,16),(5,21),(5,16),(3,16)],closed=True,radius=.6)
def arrow(c,a,b):
    dimension_arrow(c,a,b,2.5)
def extend(c,key):
    if key not in KEYS:return False
    if key.startswith('tools.category-'):
        kind=key.removeprefix('tools.category-')
        if kind=='calculatie':
            box(c,4,2,16,20);box(c,7,5,10,4)
            for x,y in ((8,13),(12,13),(8,18),(12,18)):c.circle(x,y,.8,False,True)
            c.line([(17,13),(17,18)],True,radius=0)
        elif kind=='cad':
            c.circle(12,4,2);c.line([(11,6),(4,22)],radius=0);c.line([(13,6),(20,22)],radius=0)
            c.line(arc_points(12,11,8,35,145,28),True,radius=0)
        elif kind=='constructief':
            box(c,3,3,18,4);box(c,3,17,18,4)
            c.line([(10,7),(10,17)],radius=0);c.line([(14,7),(14,17)],radius=0)
            c.line([(4,5),(20,5)],True,radius=0)
        elif kind=='geotechniek':
            c.line([(3,7),(12,3),(21,7),(12,11)],True,closed=True,radius=.3)
            for y in (12,18):c.line([(3,y),(12,y+4),(21,y)],radius=.3)
        elif kind=='bim':
            e=8
            def p(x,y,z):return (12+e*math.sqrt(3)/2*(x-y),12+e/2*(x+y)-e*z)
            back,right,left,front,bottom=p(0,0,1),p(1,0,1),p(0,1,1),p(1,1,1),p(1,1,0)
            c.line([back,right,p(1,0,0),bottom,p(0,1,0),left],closed=True,radius=.45)
            c.line([left,front,right],True,radius=.45);c.line([front,bottom],True)
        elif kind=='planning':
            browser(c)
            for x,y,w in ((6,11,7),(11,15,7),(6,19,4)):c.line([(x,y),(x+w,y)],y==15,radius=0)
        elif kind=='documenten':
            c.line([(3,18),(3,3),(14,3),(19,8),(19,21),(7,21)],closed=True,radius=.5)
            c.line([(14,3),(14,8),(19,8)],radius=.3)
            for y,w in ((12,7),(16,5)):c.line([(7,y),(7+w,y)],True,radius=0)
        elif kind=='ai':
            c.line([(6,6),(18,6),(12,18),(6,6)],radius=0)
            c.line([(6,6),(18,18),(18,6),(6,18),(6,6)],radius=0)
            for x,y in ((6,6),(18,6),(6,18),(18,18)):c.circle(x,y,3,True)
        elif kind=='energie':
            c.line([(2,11),(12,3),(22,11)],radius=.3)
            c.line([(5,10),(5,21),(19,21),(19,10)],radius=.4)
            c.line([(13,8),(8,15),(13,15),(11,20),(17,12),(12,12)],True,closed=True,radius=.1)
        elif kind=='veld':
            box(c,4,4,16,18);box(c,8,2,8,4)
            c.line([(8,13),(11,16),(17,10)],True,radius=.3)
        elif kind=='gis':
            c.line([(2,5),(8,2),(16,6),(22,3),(22,19),(16,22),(8,18),(2,21)],closed=True,radius=.4)
            c.line([(8,2),(8,18)],radius=0);c.line([(16,6),(16,22)],radius=0)
            c.line([(3,13),(9,10),(15,14),(21,11)],True,radius=.4)
    elif key=='software.catalog':
        for x,y in ((3,3),(14,3),(3,14),(14,14)):box(c,x,y,7,7,accent=x==14 and y==3)
    elif key=='software.launch':
        browser(c);c.line([(14,12),(22,17),(14,22)],True,closed=True,radius=.3)
    elif key=='software.open-webtab':
        browser(c);c.line([(9,3),(9,8)],radius=0)
        arrow(c,(5,15),(16,15))
    elif key=='software.install':
        package(c);arrow(c,(19,3),(19,19))
    elif key=='software.update':
        package(c);turn(c,18,17,5)
    elif key=='status.software-installed':
        browser(c);c.line([(10,16),(14,20),(22,11)],radius=.3)
    elif key=='status.version-upgrade':
        box(c,2,7,6,10);box(c,17,7,5,10)
        c.line([(9,12),(16,12)],radius=0);c.line([(13,9),(16,12),(13,15)],radius=.3)
    elif key=='view.web-reload':
        browser(c);turn(c,17,17,5)
    elif key=='format.decimals-increase':
        c.circle(3,14,.9,filled=True);glyph(c,'0',7,3,8,11)
        arrow(c,(3,20),(21,20))
    elif key=='draw.qr-code':
        for x,y in ((3,3),(15,3),(3,15)):box(c,x,y,6,6)
        c.line([(15,15),(18,15),(18,21),(21,21)],True,radius=0)
        c.line([(21,15),(21,17)],True,radius=0);c.line([(15,20),(15,21)],True,radius=0)
    elif key=='draw.schedule-table':
        c.line([(2,5),(2,21),(22,21)],radius=.3)
        box(c,6,3,15,14);c.line([(6,8),(21,8)],True,radius=0)
        c.line([(6,12),(21,12)],radius=0);c.line([(12,3),(12,17)],radius=0)
    elif key=='view.zoom-tool':
        c.circle(9,9,6);c.line([(13.5,13.5),(21,21)],radius=0)
        c.line([(6,9),(12,9)],True,radius=0);c.line([(9,6),(9,12)],True,radius=0)
        c.line([(16,6),(22,6)],True,radius=0)
    elif key=='comments.summarize':
        comment(c)
        for y,w in ((7,10),(11,6)):c.line([(7,y),(7+w,y)],True,radius=0)
    elif key in ('comments.import','comments.export'):
        comment(c)
        if key=='comments.import':arrow(c,(22,10),(11,10))
        else:arrow(c,(11,10),(22,10))
    elif key=='integration.platform-sync':
        box(c,2,13,7,8)
        c.line([(14,9),(14,5),(17,3),(21,5),(22,9)],radius=1)
        c.line([(14,9),(22,9)],radius=0)
        arrow(c,(4,8),(11,8));arrow(c,(21,17),(13,17))
    elif key in ('validation.select-specification','validation.reset'):
        box(c,3,3,15,18)
        for y in (7,12):
            c.circle(7,y,.65,False,True);c.line([(11,y),(14,y)],radius=0)
        if key=='validation.reset':turn(c,17,17,5)
        else:c.line([(12,16),(17,21),(22,16)],True,radius=.3)
    elif key=='panel.document-navigation':
        browser(c);c.line([(11,8),(11,21)],True,radius=0)
        c.line([(6,11),(6,17),(9,17)],radius=.3)
        c.line([(6,12),(9,12)],radius=0)
    elif key=='panel.tool-palette':
        browser(c);box(c,6,11,4,4);c.circle(16,13,2)
        c.line([(7,19),(18,19)],True,radius=0)
    elif key=='preferences.printing':
        box(c,3,8,15,10);box(c,6,3,9,5);box(c,6,14,9,7)
        c.line([(21,9),(21,21)],True,radius=0);c.circle(21,15,1.5,True)
    elif key=='panel.model-tree':
        box(c,3,3,8,5);box(c,12,11,9,4);box(c,12,19,9,3)
        c.line([(7,8),(7,20.5),(12,20.5)],True,radius=.3)
        c.line([(7,13),(12,13)],True,radius=0)
    elif key=='edit.select-text':
        for y in (5,19):c.line([(7,y),(10,y),(13,y)],radius=.3)
        c.line([(10,5),(10,19)],radius=0)
        box(c,3,9,18,6,accent=True)
    return True
