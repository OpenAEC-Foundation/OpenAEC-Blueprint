"""Original B2 designs for reviewed Workspace Composer controls and indicators."""
import math
from b2_second_series import box
from b2_bulk_series import page
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS = {50:'Algemene bediening',51:'Pakketten en werkstromen',
          52:'Toegang en machtigingen',53:'Koppelingen en servers',
          54:'Git en opdrachten',55:'Prompts en projectcontext'}
ROWS = [
 (50,'ui.close','Paneel of dialoog sluiten','Een dialoog, menu, paneel of lokale invoerronde sluiten; geen native appvenster sluiten.','1386a03b0c39b234'),
 (50,'search.clear','Zoektekst wissen','De pakketzoektekst leegmaken via onQueryChange; gevonden gegevens blijven bestaan.','1936a7e92865b93d'),
 (50,'ui.feedback','Feedbackformulier openen','Het feedbackformulier openen via setFeedbackOpen; nog niets verzenden.','5785ed1637f51fa3'),
 (50,'selection.mark','Geselecteerde optie','Aanduiding dat een pakket is geselecteerd; geen succesmelding over een proces.','9d6426786df7a951'),
 (51,'package.catalog','Pakkettencatalogus','Navigatie naar de werkruimte met beschikbare skillpakketten.','33a30a64efcf3782'),
 (51,'workspace.install','Werkruimte installeren','Navigatie naar de installatieconfiguratie; deze tegel start de installatie nog niet.','8bd317b788bdaa6c'),
 (51,'workflow.skills','Skillpakket-werkstroom','De werkstroom voor skillpakketten kiezen via onSelect.','576bb1390b474823'),
 (51,'workflow.upgrade','Versie-upgradewerkstroom','De upgrade-werkstroom kiezen; geen updatecontrole of installatie direct uitvoeren.','9eaccf873eb012da'),
 (51,'category.building','Bouw en BIM','Vaste categorieaanduiding voor Bouw en BIM in pakketkiezer of symboolbibliotheek; geen gebouw invoegen.','6efc76a8a7f3367c'),
 (51,'category.code','Webontwikkeling','Categorieaanduiding web-dev in de pakketkiezer; geen code uitvoeren.','63e85972ef96284a'),
 (51,'category.devops','DevOps','Categorieaanduiding devops in de pakketkiezer.','d95851d7c275ca09'),
 (51,'category.integration','Techniekintegratie','Categorieaanduiding cross-tech in de pakketkiezer.','18615ecdbfe590f3'),
 (52,'permission.manage','Machtigingen','Navigatie naar het overzicht van toelatingsmodi en regels; wijzigt zelf geen toegang.','a6a9fb6390d95d94'),
 (52,'permission.default','Toestemming per gereedschap','De modus default kiezen: vragen bij het eerste gebruik van een gereedschap.','9d0e456df29a17c0'),
 (52,'permission.edits','Bestandswijzigingen toestaan','De modus accept-edits kiezen; shellopdrachten blijven om toestemming vragen.','ce282cdf7715f279'),
 (52,'permission.plan','Alleen analyseren','De modus plan kiezen; bestandswijzigingen zijn daarbij niet toegestaan.','618bacea6f65c110'),
 (52,'permission.bypass','Toestemmingsvragen overslaan','De modus bypass kiezen; de waarschuwende tekst en gevaarstatus blijven bij de bediening.','23c40999c9eef489'),
 (52,'permission.allow','Toegestane regels','Kopaanduiding van de lijst met toegestane gereedschappen en opdrachten.','9bbc0f69526843c8'),
 (52,'permission.deny','Geblokkeerde regels','Kopaanduiding van de lijst met geblokkeerde patronen.','e76603d624afb539'),
 (52,'permission.add','Eigen toegangsregel','Kopaanduiding van het formulier voor een eigen allow- of deny-patroon.','adc78db675fd284d'),
 (52,'category.network','Netwerktoegang','Categorieaanduiding voor netwerkregels; geen netwerkverbinding openen.','a9e947f80dc9542f'),
 (52,'category.ai','AI-gereedschappen','Categorieaanduiding voor AI-regels; geen agent starten.','6b45bacba63ef1d5'),
 (53,'hooks.manage','Gebeurteniskoppelingen','Navigatie naar de hooks-instellingen; geen shellopdracht uitvoeren.','5581a3a729d1e13b'),
 (53,'mcp.manage','MCP-servers','Navigatie naar de MCP-serverconfiguratie; geen server toevoegen of starten.','438252482cd441a8'),
 (53,'server.gpu','GPU-server','Navigatie naar de GPU-serverpagina met verbindingsinstellingen.','30234f8dda086496'),
 (53,'server.metrics','Serverstatistieken','Kopaanduiding bij beschikbare server-, VRAM- en schijfgegevens.','98b19f93cb530555'),
 (53,'folder.sync','Mappen synchroniseren','Navigatie naar synchronisatiesessies; de tegel start geen overdracht.','f00917f172c01ac2'),
 (54,'git.repository','Git-repositorystatus','Kopaanduiding bij de gecontroleerde repository en huidige branch.','e01212f2e503917b'),
 (54,'git.init','Git-repository initialiseren','handleInit initialiseert een repository in de gekozen werkruimte.','f43883729ef883c9'),
 (54,'git.commit','Commitformulier','Het commitformulier tonen of verbergen; de knop maakt nog geen commit.','aaa295a3207c88b3'),
 (54,'git.push','Git-wijzigingen pushen','handlePush probeert de huidige repository naar de ingestelde remote te pushen.','39d44834b336b0f9'),
 (54,'git.issue','Issueformulier','Het formulier voor een repository-issue tonen of verbergen; nog niets publiceren.','d2152bead1d88ccf'),
 (54,'git.branches','Git-branches','Kopaanduiding bij de branchlijst; geen branch aanmaken.','8963a930cbaef811'),
 (54,'git.stage-all','Alle wijzigingen klaarzetten','handleStageAll zet alle repositorywijzigingen klaar voor een commit.','dbe5743370555d73'),
 (54,'terminal.log','Opdrachtenlogboek','Aanduiding bij het gelogde overzicht van uitgevoerde opdrachten.','32d3146a1b6b143b'),
 (55,'prompt.catalog','Promptsjablonen','Kopaanduiding bij de beschikbare promptsjablonen.','af8161dd30206ec6'),
 (55,'prompt.builder','Prompt samenstellen','Kopaanduiding bij het formulier voor eigen prompts; geen prompt uitvoeren.','f2cb3d7230af5b98'),
 (55,'command.catalog','Eigen opdrachten','Kopaanduiding bij eigen opdrachten in de werkruimte.','87ce4f848d42996c'),
 (55,'command.templates','Opdrachtsjablonen','Kopaanduiding bij voorgedefinieerde opdrachtteksten.','f07e8a3a466ba99c'),
 (55,'memory.manage','Projectgeheugen','Kopaanduiding bij de contextgeheugeninstellingen; geen geheugen automatisch schrijven.','e8e7d8880847e890'),
 (55,'memory.index','Geheugenindex','Aanduiding bij de inhoud van MEMORY.md.','3684ddd048af41e9'),
 (55,'memory.types','Geheugentypen','Aanduiding bij de vier contextcategorieen, met documentatielinks.','1c4708df13b2f939'),
 (55,'memory.entries','Geheugenitems','Aanduiding bij de gefilterde lijst met geheugenitems.','ca76783f2d1d3056'),
 (55,'file.structure','Mappenstructuur','Aanduiding bij de getoonde bestandsstructuur; geen map openen.','edb1530dd20cb99f'),
 (55,'template.workspace','Werkruimtesjabloon','Navigatie naar de CLAUDE.md-sjablonen voor projectinstructies.','744151384878bab0'),
 (55,'template.fields','Sjabloongegevens','Aanduiding bij de in te vullen projectvelden van een sjabloon.','6eb0d54f92db6abc'),
 (55,'template.preview','Sjabloonvoorbeeld','Aanduiding bij het live tekstvoorbeeld; geen objectzichtbaarheid schakelen.','9f286a15bb09ca22'),
 (55,'team.add','Team samenstellen','De New Team-kaart opent de teambouwer via setBuilding.','792b79dba5a01815'),
]
KEYS={k for _,k,_,_,_ in ROWS}
REUSED = {
 'bce68b183a6e9687':('theme.light','De zonvariant schakelt van donker naar licht.'),
 'f1d4afe40b371ea0':('theme.dark','De maanvariant schakelt van licht naar donker.'),
 'c60ce98ec35c14c4':('project.folder','De tegel verwijst naar de project-/werkruimtemapconfiguratie.'),
 'b8db9c87b0c12a58':('ui.settings','De tegel opent /configure.'),
 '845498c23d293402':('data.chart','De statistiekvorm duidt de zakelijke/ERP-pakketcategorie aan; geen nieuwe actie.'),
 '72a6a14844079f43':('tree.expand','De chevronklap opent of sluit de details van het gekozen promptitem.'),
 '55c7fe2d61772b63':('edit.copy','copyPrompt kopieert de gekozen prompt naar het klembord.'),
 '4a3e8eb05dc61281':('tree.expand','toggleExpand opent of sluit de onderliggende skilllijst.'),
 'b6e51475c30c66af':('view.search','De pakketzoeker filtert op naam, omschrijving of tag.'),
 '0a19f864e6f72f9a':('window.minimize','De native titelbalkknop minimaliseert het venster.'),
 '7144cbe5217413e4':('window.maximize','De native titelbalkknop maximaliseert het venster.'),
 '290e8647f9366265':('window.close','De titelbalkknop sluit het venster, niet een dialoog.'),
 '821b395394e39c85':('project.folder','Kopaanduiding voor de werkruimtemap en projectconfiguratie.'),
 '86b4f6f827c8f289':('server.gpu','Verbindingsinstellingen voor dezelfde GPU-server.'),
 '817c9641a3193918':('folder.sync','Kopaanduiding van de mappensynchronisatiesessies.'),
 '6cef9e02c345c1ee':('ui.help','De uitklapbare installatiehandleiding voor de serververbinding.'),
 'fa041c8d00704675':('hooks.manage','Kopaanduiding van dezelfde hooks-configuratie.'),
 '95b4223f8236d426':('hooks.manage','Subkop van actieve hooks, zonder extra uitvoeractie.'),
 '58a6a452afc6650a':('hooks.manage','Subkop van hooksjablonen; de lijstitems regelen toevoegen.'),
 '8f78cb64fbc1c8f6':('file.open','handleBrowse opent de mapkiezer; het label benoemt de map.'),
 'b2c828520aa8396c':('project.folder','Aanduiding van het installatiepad; geen openactie.'),
 '6caecbc710f93e40':('mcp.manage','Kopaanduiding van dezelfde MCP-configuratie; de bron-toevoegknop mist een callback.'),
 'd13dd485e0f32e39':('project.folder','Aanduiding naast het geheugenmappad.'),
 '5887e412a3c315ab':('link.open-external','De link opent de documentatie voor een geheugentype.'),
 '900bf3b5b91bfc07':('permission.manage','Kopaanduiding van dezelfde machtigingsinstellingen.'),
 'e7b13c3717403a4f':('selection.mark','Vinkje bij de geselecteerde toestemmingsmodus; geen procesresultaat.'),
 '4ecd852a9007ef76':('status.warning','Waarschuwingstekst bij bypass; de gevarenmelding blijft geel volgens de themarol.'),
 '2552ae9c8b735d6c':('command.catalog','Categorie voor shell-opdrachtregels; geen opdracht direct uitvoeren.'),
 '01e670bf11c646a6':('file.structure','Categorieaanduiding voor bestandsbewerkingsregels.'),
 'fa72ff59dd9911d0':('selection.mark','Actieve preset, geen afgeronde installatie.'),
 '9fc18e7697f92e6e':('template.workspace','Kopaanduiding van dezelfde CLAUDE.md-sjablonen.'),
 '69ede7d21d1f8e82':('file.save','saveToWorkspace schrijft de ingevulde sjabloontekst naar de werkruimte.'),
 '8f2beefca84bedc4':('edit.copy','copyToClipboard kopieert de sjabloontekst.'),
 '43b2ed738225614b':('review.track-changes','Aanduiding van gewijzigde Git-bestanden; alleen als lijstindicator, niet als registratieknop.'),
 '4392a57ce39c25db':('git.commit','Indicator bij recente commits; geen commitbewerking.'),
 'b433f8c9d0699600':('command.catalog','Subkop van de geinstalleerde opdrachten.'),
}
EXCLUDED = {
 '7eb2d833b986991a':'Grote lege-staatillustratie voor nog niet geladen Git-status.',
 'e801988d63adc6b7':'Decoratieve bliksem naast Quick Actions; geen afzonderlijke opdracht of betekenisdragende status.',
 'd126d1c3d5d704ee':'OpenAEC-beeldmerk in de titelbalk.',
 'dd08072e634ceb6e':'Decoratieve pijl tussen bron- en doelversie; geen knop of navigatieactie.',
 '555989cf80aa24b9':'Groot OpenAEC-beeldmerk in About.',
 'efbfc01b7eb3610c':'Grote lege-staatillustratie voor de opdrachtenlijst.',
 'a5090d14c78e7fcb':'Grote lege-staatillustratie voor synchronisatiesessies.',
 '22c9cccb1e2254d3':'Grote lege-staatillustratie voor hooks.',
 'e148e735c11eb16e':'Grote lege-staatillustratie voor MCP-servers.',
 '1ea0d2e143d8fab0':'Grote lege-staatillustratie bij een leeg geheugenfilter.',
 '8fedd89fc498fab3':'Geimporteerd productlogo voor pakketbranding.',
 'e4b81ad9ddfec77c':'Geimporteerd PDF-appbeeldmerk voor pakketbranding.',
}


def shield(c):
    c.line([(12,2),(21,6),(20,14),(17,19),(12,22),(7,19),(4,14),(3,6)],closed=True,radius=.7)


def folder(c):
    c.line([(3,21),(3,5),(9,5),(12,8),(21,8),(21,21)],closed=True,radius=.7)


def terminal(c):
    box(c,2,4,20,16)
    c.line([(6,9),(9,12),(6,15)],True,radius=.4)
    c.line([(13,15),(18,15)],radius=0)


def cube(c,accent=False):
    x=5*math.sqrt(3)
    c.line([(12,2),(12+x,7),(12+x,17),(12,22),(12-x,17),(12-x,7)],closed=True,radius=.3)
    c.line([(12-x,7),(12,12),(12+x,7)],accent,radius=.3)
    c.line([(12,12),(12,22)],accent,radius=0)


def document_lines(c,accent=True):
    page(c,4,2,16,20)
    for y in (8,12,16):c.line([(8,y),(16 if y!=16 else 13,y)],accent,radius=0)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='ui.close':
        c.line([(6,6),(18,18)],radius=0);c.line([(6,18),(18,6)],radius=0)
    elif key=='search.clear':
        c.line([(3,12),(8,5),(21,5),(21,19),(8,19)],closed=True,radius=.7)
        c.line([(11,9),(17,15)],True,radius=0);c.line([(11,15),(17,9)],True,radius=0)
    elif key=='ui.feedback':
        c.line([(3,3),(21,3),(21,16),(10,16),(5,21),(5,16),(3,16)],closed=True,radius=.8)
        for y,w in ((7,14),(11,11)):c.line([(7,y),(w,y)],True,radius=0)
    elif key=='selection.mark':
        box(c,3,3,18,18);c.line([(7,12),(10.5,16),(18,8)],True,radius=.4)
    elif key in {'package.catalog','workflow.skills'}:
        cube(c,True)
        if key=='package.catalog':
            c.line([(8,4.3),(16.5,9.5),(16.5,14)],True,radius=.3)
        else:c.circle(12,7,1.3,True,True)
    elif key=='workspace.install':
        box(c,3,3,18,18)
        c.line([(3,8),(21,8)],radius=0)
        dimension_arrow(c,(12,10),(12,18),2.5)
    elif key=='workflow.upgrade':
        box(c,3,10,8,11);box(c,13,3,8,18)
        dimension_arrow(c,(4,6),(11,6),1.8)
    elif key=='category.building':
        box(c,5,3,14,18)
        for x in (9,15):
            for y in (7,12):c.circle(x,y,.75,True,True)
        c.line([(10,21),(10,17),(14,17),(14,21)],radius=.3)
    elif key=='category.code':
        box(c,2,3,20,18);c.line([(2,8),(22,8)],radius=0)
        c.line([(9,11),(6,14),(9,17)],True,radius=.3)
        c.line([(15,11),(18,14),(15,17)],True,radius=.3)
    elif key=='category.devops':
        # One analytic figure-eight, with a continuous accented right lobe.
        c.line([(12+9*math.sin(2*math.pi*i/128),12+4*math.sin(4*math.pi*i/128)) for i in range(128)],closed=True,radius=0)
        c.line([(12+9*math.sin(math.pi*i/64),12+4*math.sin(2*math.pi*i/64)) for i in range(65)],True,radius=0)
    elif key in {'category.integration','category.network'}:
        if key=='category.integration':points=[(5,5),(19,5),(12,19)]
        else:points=[(12,4),(4,19),(20,19)]
        for a,b in ((0,1),(1,2),(2,0)):c.line([points[a],points[b]],radius=0)
        for idx,(x,y) in enumerate(points):c.circle(x,y,2.5,idx==2,filled=True)
    elif key.startswith('permission.'):
        shield(c)
        suffix=key.split('.')[1]
        if suffix in {'manage','default'}:
            if suffix=='manage':
                c.line([(8,10),(16,10)],True,radius=0);c.circle(12,10,1.7,True)
                c.line([(8,15),(16,15)],radius=0)
            else:
                c.circle(12,10,2.5,True);c.line([(12,12.5),(12,17)],True,radius=0)
        elif suffix in {'allow','edits'}:
            c.line([(8,12),(11,15),(17,8)],True,radius=.4)
            if suffix=='edits':c.line([(9,18),(15,18)],True,radius=0)
        elif suffix=='plan':
            c.line([(7,10),(17,10)],True,radius=0);c.line([(7,14),(14,14)],True,radius=0)
        elif suffix=='bypass':
            c.line([(16,6),(10,12),(14,12),(9,18)],True,radius=.2)
        elif suffix=='deny':
            c.line([(8,8),(16,16)],True,radius=0);c.line([(8,16),(16,8)],True,radius=0)
        elif suffix=='add':c.plus(12,12,4,True)
    elif key=='category.ai':
        for a,b in (((6,6),(12,12)),((18,6),(12,12)),((6,18),(12,12)),((18,18),(12,12))):c.line([a,b],radius=0)
        for x,y in ((6,6),(18,6),(6,18),(18,18)):c.circle(x,y,2.5)
        c.circle(12,12,3,True,True)
    elif key=='hooks.manage':
        c.circle(5,5,2);c.circle(19,19,2,True)
        c.line([(5,7),(5,12),(19,12),(19,17)],True,radius=2)
        c.line([(12,3),(12,12)],radius=0)
        c.circle(12,3,1.4,filled=True)
    elif key in {'mcp.manage','server.gpu','server.metrics'}:
        for y in (3,10):box(c,3,y,18,7)
        for y in (6.5,13.5):c.circle(6.5,y,.7,True,True)
        if key=='mcp.manage':
            c.line([(12,17),(12,21),(5,21),(19,21)],True,radius=.4)
        elif key=='server.gpu':
            box(c,8,18,8,4,True)
        else:
            c.line([(7,21),(10,18),(13,21),(18,18)],True,radius=.3)
    elif key=='folder.sync':
        folder(c)
        dimension_arrow(c,(7,12),(18,12),1.7)
        dimension_arrow(c,(18,17),(7,17),1.7)
    elif key.startswith('git.'):
        suffix=key.split('.')[1]
        if suffix in {'repository','init','branches'}:
            c.line([(6,6),(6,20)],radius=0);c.circle(6,4,2);c.circle(6,20,2)
            c.line([(6,13),(17,9),(17,5)],True,radius=1)
            c.circle(17,4,2,True)
            if suffix=='init':c.plus(18,18,3,True)
            elif suffix=='branches':
                c.line([(6,13),(18,18)],True,radius=0);c.circle(19,19,2,True)
        elif suffix=='commit':
            c.line([(2,12),(8,12)],radius=0);c.line([(16,12),(22,12)],radius=0);c.circle(12,12,4,True)
        elif suffix=='push':
            c.line([(3,6),(3,3),(21,3),(21,6)],radius=.5)
            dimension_arrow(c,(12,21),(12,7),3)
        elif suffix=='issue':
            page(c,4,2,16,20);c.line([(12,7),(12,13)],True,radius=0);c.circle(12,17,.8,True,True)
        elif suffix=='stage-all':
            page(c,2,5,12,16);page(c,7,2,14,16)
            c.line([(10,10),(13,13),(18,7)],True,radius=.4)
    elif key in {'terminal.log','command.catalog','command.templates'}:
        terminal(c)
        if key=='command.catalog':c.line([(15,1.5),(20,1.5)],True,radius=0)
        elif key=='command.templates':c.line([(5,22.5),(19,22.5)],True,radius=0)
    elif key in {'prompt.catalog','prompt.builder'}:
        c.line([(3,3),(21,3),(21,17),(11,17),(5,22),(5,17),(3,17)],closed=True,radius=.6)
        if key=='prompt.catalog':
            for y,w in ((7,17),(12,13)):c.line([(7,y),(w,y)],True,radius=0)
        else:c.line([(8,13),(9,9),(15,5),(18,8),(12,13)],True,closed=True,radius=.2)
    elif key.startswith('memory.'):
        suffix=key.split('.')[1]
        if suffix=='manage':
            box(c,4,3,16,18)
            c.line([(8,7),(16,7),(16,12),(8,12),(8,17),(16,17)],True,radius=.8)
        elif suffix=='index':
            document_lines(c);c.line([(2,5),(4,5)],radius=0);c.line([(2,10),(4,10)],radius=0)
        elif suffix=='types':
            for x,y in ((3,3),(14,3),(3,14),(14,14)):box(c,x,y,7,7,x==14 and y==14)
        else:
            for y in (5,12,19):
                c.circle(4,y,1.3,True,True);c.line([(8,y),(21,y)],radius=0)
    elif key=='file.structure':
        c.line([(5,4),(5,20),(12,20)],radius=.7)
        c.line([(5,11),(12,11)],radius=0)
        for x,y in ((3,2),(12,8),(12,17)):box(c,x,y,8 if x==12 else 6,5,x==12)
    elif key in {'template.workspace','template.fields','template.preview'}:
        page(c,3,2,18,20)
        if key=='template.workspace':
            c.line([(7,7),(17,7),(17,12),(7,12)],True,closed=True,radius=.5)
            c.line([(7,16),(14,16)],radius=0)
        elif key=='template.fields':
            for y in (8,15):box(c,7,y,10,4,True)
        else:
            c.line([(6,13),(9,9),(15,9),(18,13),(15,17),(9,17)],True,closed=True,radius=1.8)
            c.circle(12,13,1.5,True)
    elif key=='team.add':
        c.circle(8,6,3);c.circle(17,7,2.5)
        c.line(arc_points(8,21,6,180,360,24),radius=0)
        c.plus(19,18,3,True)
    return True
