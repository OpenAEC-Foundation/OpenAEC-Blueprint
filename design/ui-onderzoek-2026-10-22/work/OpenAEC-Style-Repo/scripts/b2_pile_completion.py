"""Pile Plan controls reviewed against the pinned AppSession and source callbacks."""
from b2_second_series import box
from b2_bulk_series import page
from b2_bim_completion import cube
from b2_session_two import dimension_arrow

GROUPS={93:'Paalplaninspectie en instellingen',94:'Paalplanbewerking',95:'Paalplanzweergave',96:'Bestandstypeaanduidingen'}
ROWS=[
(93,'pile.load-points','Belastinglocaties inspecteren','Het rechterpaneel load-point met de belastinglocaties openen; geen locatie plaatsen.','0c59a530634a23f9'),
(93,'pile.cpts','Sonderingen inspecteren','Het rechterpaneel cpts openen; geen sondering in de tekening plaatsen.','97f9f80540eb01f1'),
(93,'pile.cpt-settings','Sonderingsinstellingen','Het taakpaneel cpt-settings openen voor de toewijzingsinstellingen.','6f99f83bce25096f'),
(93,'pile.cost-settings','Paalkosten instellen','Het taakpaneel cost-settings met de paalkostentabel openen.','4a34f31ef2963441'),
(93,'pile.group-settings','Belastinggroepen instellen','Het taakpaneel grouping-settings openen; geen bestaande lijst automatisch groeperen.','4e3d4165e1025cb4'),
(94,'pile.lock-edit','Locatievergrendelingen bewerken','beginLoadPointLockEditing start een bewerkingsronde; toepassen en annuleren volgen apart.','142a53fc4bfbe7a9'),
(94,'pile.optimization','ILP-optimalisatiepaneel','Het taakpaneel ilp-optimization openen; de berekening start pas met de afzonderlijke opdracht in dat paneel.','878dcaefee22db8e'),
(94,'table.column-filter','Kolomwaarden filteren','Het filtermenu voor de gekozen bronkolom openen; de invoer werkt filterAndSortSourceRows bij.','e5313bf195206ed8'),
(95,'pile.tip-regions','Paalpuntniveaugebieden tonen of verbergen','showTipLevelRegions omschakelen; de actie en zichtbaarheid staan in het dynamische label.','2d68fd5c3f51d38e'),
(95,'pile.load-groups','Belastinggroepen tonen of verbergen','showLoadPointGroups omschakelen; geen groep maken of instellingen openen.','c66ad5ebba56d8cb'),
(95,'status.hidden','Verborgen','Een verborgen weergavelaag aanduiden; dit is geen verbergopdracht.','679ef74f5252a09c'),
(96,'file.type-ifc','IFC-bestandstype','Vaste typeaanduiding van een IFC-bestand; geen importopdracht of garantie dat het bestand geopend kan worden.','0a95aa106356c4df'),
(96,'file.type-project','Projectbestandstype','Vaste typeaanduiding van een projectbestand; geen projectmap openen.','0cf8155745344b34'),
(96,'file.type-other','Bestandsaanduiding','Vaste generieke aanduiding van een bestand of brongegevensdocument; het label noemt het formaat als dat bekend is.','fb4d5fdb2afb5877'),
]
KEYS={k for _,k,_,_,_ in ROWS}
SEMANTIC={'status.hidden':'text-secondary'}
ACCENT_FRONT={k:'De bepalende markering blijft ononderbroken vóór het achterliggende kader.' for k in KEYS if k not in SEMANTIC}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}

def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)

def exclude(ids,reason):
    for rid in ids.split():EXCLUDED[rid]=reason

reuse('78cc877fa881e9fc 670306608b15294e b37e3902096c0b66','file.open','Backstage Openen toont de IFCPP-keuze; de kaartpijlen kiezen een desktopproject of laden het voorbeeld via de door AppSession doorgegeven callbacks. Geen vooruitnavigatie.')
reuse('e4e793c1ba9b7996 7b29fd89625edfac','file.save','De desktopvariant roept saveProject aan; bestaand pad overschrijven, anders saveProjectAs.')
reuse('c46845eb54df089b','file.save-as','saveProjectAs kiest een nieuwe IFCPP-bestemming, schrijft de projectsnapshot en bewaart projectPath.')
reuse('7264384f092f719e','file.export-options','Het exportpaneel tonen; er wordt bij deze menukeuze nog geen bestand geschreven.')
reuse('5fb08d7c135056aa d94cc597791e2b14','file.import','Het project- of paalplanimportpaneel openen. Werkelijke broninvoer is CSV/XLSX, geen IFC ondanks de oude assetnaam.')
reuse('b9243b5f5204a5d2 36e155100c4c7b23','ui.settings','De gebonden callback opent de appvoorkeuren.')
reuse('fb45ddce51e3ee91','ui.about','Het Over-paneel in Backstage openen.')
reuse('a81ce94151730796','window.close','Deze alleen op desktop aanwezige knop sluit getCurrentWindow; geen document-close.')
reuse('54b466a59d39517c de3a04bda3d79e60','ui.close','De Bestand-overlay of brongegevenstabel sluiten; geen browsergeschiedenis terug.')
reuse('c656930a7790cbbf 8d37a23c55128748','link.open-external','De Foundation-site of GitHub-organisatie extern openen.')
reuse('f6cbf77cd3a07e37','report.document','De report-arm is een documenttypeaanduiding in de opgeslagen recentelijst; geen rapport genereren. useRecentFiles leest persistent opgeslagen records, inferType classificeert JSON/OAEC als report.')
reuse('d8d5b1279812abed','project.forget-recent','removeRecentFile filtert alleen het pad uit de recentelijst en bewaart de lijst; wist geen bestand.')
reuse('29ebfa61cc282aea 2c061a8b32312919 d5bfe77abdf32c82 b9af4713b6b7ddee 86f688ed13c6c8d6','file.export','Exportkaart of web-titelbalk schrijft een nieuwe IFCPP-projectsnapshot, XLSX- of CSV-paalplantabel. AppSession serialiseert/bouwt de bytes tijdens de opdracht; geen bestaand bestand uitsluitend downloaden. Formaat blijft expliciet in het label.')
reuse('28d95720e3960f86','project.properties','setProjectInformationOpen toont de projectgegevensdialoog met naam, paalkopniveau en munteenheid.')
reuse('80157e65661d4566','selection.box','De als lasso gelabelde modus gebruikt LassoRectangle en rechthoekgrenzen; geen vrije selectielus.')
reuse('0fdb20ac34c0145e','data.apply','finishLoadPointLockEditing legt de in de bewerkingsronde gekozen locatievergrendelingen vast via commitProjectState.')
reuse('48b04473781e9662','data.discard','cancelLoadPointLockEditing verwerpt de huidige vergrendelingsdraft; geen object verwijderen.')
reuse('6c5901ed748a0e10','panel.left','workspaceLayout.explorerVisible omschakelen; toont of verbergt de linker verkenner.')
reuse('1fd778e420999571','panel.right','workspaceLayout.propertiesVisible omschakelen; toont of verbergt het rechter eigenschappenpaneel.')
reuse('968cd92e85a0a98d 6c9fa9548ca0e842 e7c5c8c351594a3e 90828e7205c41b17','tree.expand','Ingeklapte invoerbronnen- of paalplangroep uitklappen. De dubbele catalogusrecords beschrijven dezelfde GroupHeading-aanroep/false-arm.')
reuse('1af5ceabde809e42 35a0cbedad7572b6 eae9b114f155db40 13e968b012cd799f','tree.collapse','Uitgeklapte invoerbronnen- of paalplangroep invouwen. De dubbele catalogusrecords beschrijven dezelfde GroupHeading-aanroep/true-arm.')
reuse('fea932258ffa5ef3 3ebc535c10548fff','object.rename','startRename opent het plan-naamveld; finishRename roept de gebonden planhernoeming aan.')
reuse('1bb989a860773872 eb8130a126565b74','edit.duplicate','De concrete copy-variant roept onDuplicate(plan.id) aan; geen klembordkopie.')
reuse('2ecbf54d95b4f6cb ad19c868ae73026b','edit.delete','De delete-variant verwijdert het gekozen paalplan; laatste plan is beschermd door disabled.')
reuse('eea14f7f9fae9c14 366ba01f089ac560','status.warning','De warning-arm van Icon wordt alleen gerenderd wanneer costSummary.missingCount groter dan nul is; geen verwijderopdracht.')
reuse('44a74da17be88a03 a015b8037a805c77','pile.new','De concrete plus-arm bij onCreate maakt via de bestaande callback een paalplan in het project.')
reuse('8f05c236a6c5d3b3 687720a2acb6e089 1c6fa4e20a316e76 ce9f6f1611d3214b 71d2f37b4ba4c21a 418145bc9eb21aaf','file.import','FileActionIcon/ifcImportIcon staat bij native CSV/XLSX-keuze. assignFiles/assignRoleFile/changeFile leest importbronnen; de assetnaam bewijst geen IFC-functie.')
reuse('638eeb05bf99dc64 124bc0e364ba937a bae4abf733bfca10 58c8ddccb28ad998','status.info','Vaste tekstuele hulp over paalkopniveau of numerieke invoer; rol img met title, geen apart hulpvenster.')
reuse('016f4628af82638c','status.warning','De unavailable-arm van LegendRegionStatus meldt dat niveaugebieden niet beschikbaar zijn; geen waarschuwingsactie.')
reuse('f368c1ab9724fb9c','pile.encoding-conflicts','LegendConflictNotice klapt de details van dubbele legenda-encoderingen open; hetzelfde contract als het bestaande serie-12-voorbeeld.')
reuse('0d861c175324a52f','status.info','Het informatiebadge meldt gebruik buiten de huidige scope. De omringende knop opent plan-gebruikdetails; dit is geen dubbelcoderingswaarschuwing.')
reuse('c6c1f49e47317153','content.drag','Sleephandvat voor de volgorde van paaloptiekolommen, ook via pijltoetsen; verplaatst layout-items, geen tabelgegevens.')
reuse('5e7a11de6a581bd8 3fddcf40c10325cc','ui.dropdown','De selectie- of themakeuze open- en dichtklappen; geen boomtak.')
reuse('978b2d2a7a8b7202','feedback.attach-images','De feedbackknop opent de afbeeldingsbestandskeuze voor bijlagen; deze klik verzendt nog geen feedbackbericht.')
exclude('9c0b11c01aa9905a','Sonderingsteken in de hoverlegenda van het model met geselecteerde-CPT-klasse en dynamisch locatielabel; geen vaste bedieningsknop. Het CPT-inspectiepaneel krijgt een eigen functiecontract.')
exclude('ff4ea1d4ae463cf7','Modelmarkering voor een belastinglocatie zonder gekozen paaloptie; betekenis en omvang horen bij de modelrenderer, geen UI-sluitknop.')
exclude('1cb20d274e6fc85e','Vraagtekenmarker op een niet door de optimizer toegewezen belastinglocatie. Map/inline placement, halo en schaal volgen optimizerMarkerGeometry/loadPointMarker; onderdeel van het model, geen vaste knop of algemene helpvraag.')
exclude('bc8b0175df442bb6 584ba513983a94c3','Groot 120×80 algoritmediagram binnen AlgorithmOption (kwadranten of maximumhoek). De knop wijzigt het algoritme; de schematische meetpunten en boog blijven een inhoudelijk diagram buiten de 16/24px UI-icoonfamilie.')
exclude('551a0e5b4fb639d1','Dynamische paalsymbolen met baseShape/fillPattern, kleur, clipmaskers en modelschaal; geen eindige set vaste bedieningsfuncties.')
exclude('83f7f9a7079658d0 2118a839477a5f5b','Appbeeldmerk als favicon of titelbalklogo; geen bedieningsicoon.')


def sliders(c,x=17):
    for y,dx in ((6,-1),(12,2),(18,-1)):
        c.line([(x-3,y),(x+3,y)],True,radius=0)
        c.circle(x+dx,y,1.4,True,filled=True)


def panel(c):
    box(c,2,3,20,18)
    c.line([(15,3),(15,21)],radius=0)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='pile.load-points':
        panel(c)
        dimension_arrow(c,(8.5,6),(8.5,13),2)
        c.line([(5,17),(12,17)],True,radius=0)
    elif key=='pile.cpts':
        panel(c)
        c.line([(8.5,6),(8.5,12)],True,radius=0)
        c.line([(5.5,12),(11.5,12),(8.5,18)],True,closed=True,radius=.2)
    elif key=='pile.cpt-settings':
        c.line([(7,3),(7,12)],radius=0)
        c.line([(3,12),(11,12),(7,20)],closed=True,radius=.3)
        sliders(c,18)
    elif key=='pile.cost-settings':
        box(c,2,4,11,16)
        c.line([(2,9),(13,9)],radius=0)
        c.line([(6,13),(10,13)],radius=0)
        if not small:c.line([(6,17),(10,17)],radius=0)
        sliders(c,19)
    elif key=='pile.group-settings':
        for x,y in ((4,5),(11,5),(7.5,15)):c.circle(x,y,2)
        c.line([(4,7),(7.5,13),(11,7)],radius=0)
        sliders(c,19)
    elif key=='pile.lock-edit':
        box(c,3,10,12,11)
        c.line([(6,10),(6,5),(12,5),(12,10)],radius=3)
        c.line([(19,5),(19,19)],True,radius=0)
        c.circle(19,12,2.5,True)
    elif key=='pile.optimization':
        panel(c)
        for x,y in ((5,17),(8,11),(12,7)):
            c.circle(x,y,1.4,True,filled=True)
        c.line([(5,17),(8,11),(12,7)],True,radius=0)
    elif key=='table.column-filter':
        box(c,2,3,20,7)
        c.line([(8,3),(8,10)],radius=0)
        c.line([(15,3),(15,10)],radius=0)
        c.line([(5,14),(19,14),(14,19),(14,22),(10,22),(10,19)],True,closed=True,radius=.3)
    elif key=='pile.tip-regions':
        c.line([(3,3),(13,3),(13,8),(21,8),(21,21),(3,21)],closed=True,radius=.3)
        c.line([(3,10),(13,10),(13,21)],True,radius=.3)
        c.line([(13,15),(21,15)],True,radius=0)
    elif key=='pile.load-groups':
        box(c,2,3,12,12);box(c,10,11,12,10)
        for x,y in ((6,7),(10,11),(14,15),(18,17)):c.circle(x,y,1,True,filled=True)
    elif key=='status.hidden':
        c.line([(2,12),(7,7),(12,5),(17,7),(22,12),(17,17),(12,19),(7,17)],closed=True,radius=2)
        c.circle(12,12,3)
        c.line([(3,3),(21,21)],radius=0)
    elif key=='file.type-ifc':
        cube(c)
        c.line([(12,2),(12+5*3**.5,7)],True,radius=0)
    elif key=='file.type-project':
        page(c,4,2,16,20)
        box(c,7,12,10,7,True)
        c.line([(7,12),(7,10),(11,10),(13,12)],True,radius=.3)
    elif key=='file.type-other':
        c.line([(4,2),(14,2),(20,8),(20,22),(4,22)],closed=True,radius=.6)
        c.line([(14,2),(14,8),(20,8)],True,radius=.3)
    return True
