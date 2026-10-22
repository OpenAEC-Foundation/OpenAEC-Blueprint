"""Calc source contracts: quotation state, report modes, sheet actions and extensions."""
import math
from b2_second_series import box
from b2_workspace_completion import shield
from b2_bulk_series import page
from b2_reports_completion import glyph
from b2_font_geometry import font_sources
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS={99:'Offertetypen en secties',100:'Offertedocument en versies',101:'Begrotingsrapportages',
102:'Rapportpapier en huisstijl',103:'Begrotingsweergave',104:'Subbladen en Excel',105:'Uitbreidingen, docking en rekenwizard'}
ROWS=[
(99,'quotation.type-private','Particuliere offerte','setOfferteType particulier selecteert het particuliere offertetype; geen rapport genereren.','1819ba24a47eec10'),
(99,'quotation.type-raw','RAW-offerte','setOfferteType raw selecteert het RAW-offertetype.','5d689da8931a2467'),
(99,'quotation.type-simple','Eenvoudige offerte','setOfferteType eenvoudig selecteert het eenvoudige offertetype.','78f797952b505635'),
(99,'quotation.section-technical','Technische offertesectie','addSection technisch voegt een technische omschrijving toe en activeert die sectie.','dc412787414a6d3f'),
(99,'quotation.section-options','Optiesectie toevoegen','addSection opties voegt een offertesectie voor opties toe en activeert die sectie; geen begrotingsvariant maken.','78c25c928e6f93ce'),
(99,'quotation.section-free','Vrije offertesectie','addSection vrij voegt een vrije offertesectie toe.','a74ae7d74fdb2630'),
(99,'quotation.section-extra','Meerwerksectie toevoegen','addSection meerwerk voegt een meerwerksectie toe, selecteert die en opent het offertetabblad.','3423cd36006134ce'),
(100,'quotation.metadata','Offertegegevens','Het offerteonderdeel __meta selecteren met document- en geadresseerdegegevens.','23c1d50c782fe075'),
(100,'quotation.payment-terms','Betalingstermijnen','Het offerteonderdeel __termijnen met percentages, omschrijvingen en toelichting openen.','2623be96a2352308'),
(100,'quotation.warranties','Offertegaranties','Het offerteonderdeel __garanties met onderdelen en termijnen openen.','77cdc1c27eba119c'),
(100,'quotation.snapshot-sent','Versie als verstuurd vastleggen','createSnapshot bewaart een diepe kopie van begroting/items/offerte met type verstuurd; er wordt niets verzonden.','efdbce21039aa949'),
(100,'quotation.snapshot-draft','Conceptversie vastleggen','createSnapshot bewaart een diepe kopie met type concept; geen nieuwe lege offerte maken.','230129508fd580b3'),
(101,'report.view-specification','Werkbeschrijving','REPORT_VIEWS kiest werkbeschrijving en activeert de rapportweergave; nog geen uitvoerbestand maken.','fc3edde04dd8d211'),
(101,'report.view-main-contract','Hoofdaannemingsrapport','REPORT_VIEWS kiest hoofdaanneming voor de rapportpreview.','8604b1e54568c00c'),
(101,'report.view-subcontract','Onderaannemingsrapport','REPORT_VIEWS kiest onderaanneming voor de rapportpreview.','ab479d5c2fb50734'),
(101,'report.view-tender','Inschrijfstaatweergave','REPORT_VIEWS kiest inschrijfstaat; geen Excel-bestand exporteren.','31d750e4c3278179'),
(101,'report.view-actual-cost','Nacalculatierapport','REPORT_VIEWS kiest nacalculatie voor de rapportpreview.','485542c530830597'),
(101,'report.view-build','Bouw 1-rapport','REPORT_VIEWS kiest bouw1 voor de rapportpreview.','4368700f162b1647'),
(101,'report.view-ibis','IBIS-rapportweergave','De als Bouw 2 gelabelde keuze zet reportView ibis; preview/export gebruiken de IBIS-generator.','2330bfeea2a38fe2'),
(101,'report.view-estimate','Directiebegrotingsrapport','REPORT_VIEWS kiest directie voor de rapportpreview; geen offerteaanvraag verzenden.','e634aa83ac6cdf95'),
(102,'report.paper-size','Rapportpapierformaat','setPageSize kiest A4 of A3 voor preview en rapportuitvoer; geen bestaande PDF-pagina schalen.','e797419f7bc13da1'),
(102,'report.portrait','Rapport staand','setPageOrientation portrait kiest staand rapportpapier.','152b60149198ef78'),
(102,'report.landscape','Rapport liggend','setPageOrientation landscape kiest liggend rapportpapier.','3200ec78f1e38359'),
(102,'report.branding','Rapportlogo’s instellen','Het ReportLogoSettings-dialoog openen; het icoon is geen bedrijfsbeeldmerk.','2f41a76ad09abfb4'),
(103,'calc.quantities-visible','Hoeveelheden tonen','toggleHoeveelheid schakelt de hoeveelheidkolom/-weergave in begroting en rapporten.','0cc80121d0b1fb17'),
(103,'calc.price-percentage','Prijzen procentueel wijzigen','De prijzendialoog openen; Toepassen roept scaleAllPrices aan met factor 1 + percentage/100.','ba9379eeeeb59cce'),
(103,'calc.grid-standard','Standaard begrotingsweergave','setGridView st kiest GRID_COLUMN_DEFS; geen geheel nieuw document maken.','9ef187cdbc0fbd0e'),
(103,'calc.grid-wpcalc','WpCalc-begrotingsweergave','setGridView wpcalc kiest WPCALC_COLUMN_DEFS en de bijbehorende hiërarchische groepering.','e2c2f9a423ccb8ea'),
(103,'calc.grid-simple','Eenvoudige begrotingsweergave','setGridView simple kiest SIMPLE_COLUMN_DEFS.','8de859729fb99cf7'),
(103,'tree.collapse-level','Tot niveau inklappen','De niveaukeuze voor collapseToLevel openen; één keuze kan ook alles uitklappen. Geen individuele tak onmiddellijk invouwen.','26a62d2ab8e698fd'),
(103,'calc.chapter','Begrotingshoofdstuk','Hoofdstukindicator in SchedulePanel; de omringende rij selecteert de corresponderende begrotingsrij.','6754758a1a470b4a'),
(104,'spreadsheet.sheet-add','Subblad toevoegen','addSubSheet maakt een nieuw rekenblad binnen de begroting en openSheet activeert dat blad.','ed0e7a106bded527'),
(104,'format.decimals-decrease','Minder decimalen','spreadsheet-action decimals-down verlaagt de getoonde decimalen van de geselecteerde cellen, met ondergrens nul.','0a3515fb9640e34c'),
(104,'data.excel-refresh','Excel-koppelingen bijwerken','updateAllExcelLinks leest de gekoppelde werkboeken/cellen en werkt quantity bij; schrijft geen Excel-export.','f422a43648ca2b57'),
(104,'data.excel-link','Gekoppelde Excel-waarde','Vaste aanduiding bij een hoeveelheidcel met item.excelLink; geen nieuwe koppeling maken of exporteren.','b4a5cd3e7e0d7fba'),
(105,'extension.install-file','Extensie uit bestand installeren','Een lokaal extensiepakket kiezen en installeren; het pakketformaat volgt de appworkflow, geen projectgegevens importeren.','7de470d44e492eb8'),
(105,'extension.item','Uitbreidingspakket','Vaste aanduiding van een extensiepakket, ook als fallback zonder eigen icoon; geen plus- of verwijderactie.','64e10498d2f34ec3'),
(105,'extension.importer','Importuitbreiding','Typeaanduiding van een ingebouwde importadapter in Extensiebeheer/cataloog; de kaart voert niet direct de import uit.','7733ca7d97f4f949'),
(105,'extension.exporter','Exportuitbreiding','Typeaanduiding van de ingebouwde WpCalc-exportadapter; uitvoering zit in Bestand.','4df5a136f45aff7d'),
(105,'workspace.dock-back','Terug naar hoofdvenster','De losgemaakte begroting via BroadcastChannel als tab in het hoofdvenster openen/activeren en daarna het losse venster laten sluiten.','1f7657010f43067e'),
(105,'calc.hsb-wizard','HSB-wandrekenwizard','De geregistreerde HSB-wandwizard kiezen en de parameters openen; berekenen en begrotingsposten invoegen volgen afzonderlijk.','a187ebf3640483d6'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De bepalende pijl, markering of verbinding blijft vóór de document- of tabelcontour volledig zichtbaar.' for k in KEYS}
TYPOGRAPHY={'format.decimals-decrease':{**font_sources()['format.color'],'glyph':'0','purpose':'Cijfercontour voor decimale celopmaak; Space Grotesk Medium.'}}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}

def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)

def exclude(ids,reason):
    for rid in ids.split():EXCLUDED[rid]=reason

def dispatch(ids,targets,reason):
    for rid in ids.split():DISPATCHERS[rid]=targets;DISPATCH_EVIDENCE[rid]=reason

reuse('56847522844879f5','edit.delete','removeSection verwijdert alleen de actieve gewone offertesectie; speciale __-onderdelen zijn beschermd.')
reuse('941a722a9150c01b c385c6321439c5e4','report.generate','De offerte- of begrotingsrapportgegevens naar de gekozen PDF-bestemming laten genereren. Begrotingspreview/export volgen de geselecteerde rapportmodus; browserfallback gebruikt de HTML-printservice.')
reuse('8b985125a67bae3e ca820325a7a92684','file.export','Inschrijfstaat naar Excel of begroting naar WpCalc wegschrijven; formaatlabel en bestaand native/web-bereik blijven expliciet.')
reuse('dcb41be6ec33141d','report.options','Het rapportoptiepaneel voor hoeveelheden en wijzigingsmarkeringen openen; geen algemene appvoorkeuren.')
reuse('9a15dd5397c34adf','report.paper-size','setPageSize A3 is de tweede formaatkeuze van hetzelfde rapportpapiercontract.')
reuse('2b58aa571a17e352 2d094e55c2248b15','panel.left','De linker verkenner of StartSidebar dichtzetten via zijn eigen state; geen boomtak invouwen.')
reuse('a99970add230693f','panel.right','Het rechter eigenschappenpaneel dichtzetten.')
reuse('3b890568ba9d5a7b f65389c94c7ec102 a07bdac28f5ca973','file.new','newFile voegt een nieuw leeg begrotingsdocument toe via addDocument.')
reuse('706c39e5af4d4e3e 97438eadca5869f9 07978a71f7435235 c5bbc436f3ddc058','file.open','Bestand openen toont de bestandskeuze of recente lijst. StartSidebar gebruikt werkelijk openFile/openRecentFile; onLoadVoorbeeld in App laadt het ingesloten voorbeeldproject.')
reuse('1903a8ecc71b2f02','cloud.open','Het cloudbestandspaneel met bladeren/openen/uploaden openen, alleen als OPENAEC_ENABLED; nog geen bestand downloaden.')
reuse('d66f023db644112b','file.save','saveFile schrijft het native actieve pad; bij nieuw/geïmporteerd document kiest het een ifcCalc-bestemming. Webvariant downloadt de projectsnapshot.')
reuse('9e58f990ca55a330','file.import','Dezelfde importmenuvorm opent het importpaneel en staat bij meerdere echte bestandsimporters. De concrete IFC/IFCX-kostenimport en overige XML/tabulaire adapters zijn in de callbacks onderscheiden; formaat blijft in label.')
dispatch('a21636a72c9ae0f3',('file.save','file.save-as'),'Dezelfde save-definitie staat bij gewone saveFile én saveFileAs. De eerste schrijft een bestaand native pad, de tweede vraagt altijd een nieuwe bestemming.')
dispatch('15618f785a51afef',('file.export-options','file.export','ifc.export'),'De exportdefinitie opent het exportpaneel en staat bij XLSX/XML/native exports én echte STEP-IFC-kostenexport. Concrete callback en formaat bepalen de keuze; geen onjuiste algemene IFCX-toewijzing.')
reuse('82b3e4bc16adad01','file.print','Bestand Print roept printBudget voor hoofdaanneming aan; werkende printservice.')
reuse('d2a5d26b46d3fc44 ff2c088dd72f58f1','ui.settings','De gebonden instellingenhandler opent de appvoorkeuren.')
reuse('f36d9c568f7150d8','ui.about','Het Over-paneel in Bestand openen.')
reuse('d9cae6452d7a3f67 7d9d78c1dfa8630d','window.close','De appvenster-sluitactie aanroepen, met eigen afhandeling van niet-opgeslagen begroting; geen object verwijderen.')
reuse('2e1d988af4d34c92','extensions.manage','Het werkende ExtensionManagerPanel openen.')
reuse('7346a5f2c660d9b2 70aa869737cb7938 631aecc44beb0ee4','ui.close','Bestand-overlay, gesplitste grid of middelenkiezer sluiten; dit sluit het appvenster niet.')
reuse('15f035565ba7bf13 810eff95d542f25b','file.type-project','Het documenticoon staat bij een begrotingsbestand in de recente of cloudlijst; geen Nieuw-opdracht. De omringende rij opent het bestand.')
reuse('6698f73b2a3fcbc3','project.folder','De cloudmaprij toont een map en kiest path naar die map; geen bibliotheekmap aanmaken.')
reuse('3f80817756b9cbd9','extension.install-file','De JS-variant van dezelfde lokale extensie-installatieworkflow; service kiest/leest het bestand en registreert de uitbreiding.')
reuse('3fefaf11c36ff117','extension.item','De fallback bij een catalogusitem zonder icoon is een pakketaanduiding; de aparte installatieknop voert de actie uit.')
reuse('1cfcf1907e34a08c 9a8c2c6b7c22b5e9','status.warning','Waarschuwing over gecontroleerde importproblemen of niet-opgeslagen wijzigingen; geen zelfstandige delete/close-actie.')
dispatch('003c6ce2b2be9e75',('tree.expand','tree.collapse'),'GridCell toont één chevron met isCollapsed/CSS-toestand. De knop roept onToggleCollapse voor die concrete containerrij aan; beide taktoestanden afzonderlijk kiezen.')
reuse('915ec1a512dec731','spreadsheet.sheet-add','SubSheetTabBar.handleAdd maakt en activeert hetzelfde subblad als de lintknop.')
reuse('c4a516da450ddbba','edit.undo','De werkende titelbalkhandler herstelt undo en past de items toe.')
reuse('f1714406adaba285','edit.redo','De werkende titelbalkhandler herstelt redo en past de items toe.')
reuse('92f81ca4bdf2fb20','window.minimize','De native titelbalk minimaliseert het appvenster.')
reuse('80de6944047bcd8b','window.restore','De isMaximized-arm herstelt de vorige vensterafmetingen.')
reuse('7eaf7389cbfc82d9','window.maximize','De andere arm maximaliseert; het cataloguslabel Herstellen beschrijft deze arm onjuist.')
reuse('9ed0cc34360ab174','tree.expand','Een ingeklapt begrotingshoofdstuk uitklappen (chapter.isCollapsed true).')
reuse('f43f21d825baafe4','tree.collapse','Een open begrotingshoofdstuk invouwen (chapter.isCollapsed false).')
reuse('c6261a6dd2ca66b3 fb9505ede7a4f608','edit.delete','Een niet-standaard projectkengetal of het gekozen subblad verwijderen; expliciete scope in het bedieningslabel.')
reuse('74d8af79cca94090','format.bold','De spreadsheet-action bold wordt in SubSheetEditor ontvangen en schakelt toggleBold voor alle geselecteerde cellen.')
reuse('b3753d3c6fe1ae2f','format.italic','De spreadsheet-action italic schakelt toggleItalic voor de geselecteerde cellen.')
reuse('2e336a21b47011bd','format.align-left','De spreadsheetactie zet cellAlign op left; geen vorige-pagina-opdracht.')
reuse('c1c058447b88cda3','format.align-center','De spreadsheetactie zet cellAlign op center; geen horizontaal objectverdelen.')
reuse('32e3282bb7d50bc3','format.align-right','De spreadsheetactie zet cellAlign op right; geen volgende-pagina-opdracht.')
reuse('8b47bfdf310714a2 89dc358ef9a8efcf 1de4e9d2da0ed6f4 8174866f70ac1498 28770a5aceef7289 b934fe4ffa2bef00 e576a74f16cb3eb7 ed848bd2f3ee8ce8 866e5fd5b8c4e521 350fa7a807596653 4e6ddc6a17b6732c','extension.importer','De expliciet benoemde ONLV/BasCalc/WpCalc/Inschrijfstaat/IBIS/DNC/RSX-importadapter wordt in Extensiebeheer of de gepinde catalogus als pakket aangeduid. registerBuiltinExtensions bindt concrete importers; de kaart voert ze niet automatisch uit. Catalogus en ingebouwde manifests apart gelezen; geen naamregel voor onbekende runtime-extensies.')
exclude('28c7b470c7e548a6','De offerte-printknop is disabled en heeft alleen een lege onClick. Begrotingsprint en PDF-generatie zijn wel afzonderlijk bereikbaar.')
exclude('026d5029976a6a28','Het appbeeldmerk in Over; branding, geen bedieningsicoon.')


def doc(c):page(c,4,2,16,20)


def rows(c,ys=(7,12,17),accent=False):
    for i,y in enumerate(ys):c.line([(8,y),(16-(2 if i==len(ys)-1 else 0),y)],accent,radius=0)


def small_pencil(c):
    c.line([(14,17),(20,11),(23,14),(17,20),(13,21)],True,closed=True,radius=.2)


def extension_box(c):
    box(c,3,3,18,18)
    c.line([(3,8),(9,8),(9,3)],radius=.4)
    c.line([(15,21),(15,16),(21,16)],radius=.4)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key.startswith('quotation.type-'):
        doc(c);kind=key.removeprefix('quotation.type-')
        if kind=='private':
            c.line([(7,12),(12,7),(17,12),(17,18),(7,18)],True,closed=True,radius=.4)
            c.line([(11,18),(11,14),(14,14),(14,18)],True,radius=.3)
        elif kind=='raw':
            for y in (7,12,17):
                c.circle(8,y,.8,True,filled=True);c.line([(11,y),(17,y)],radius=0)
        else:
            c.line([(8,8),(16,8)],True,radius=0)
            c.line([(8,15),(14,15)],radius=0)
    elif key.startswith('quotation.section-'):
        page(c,2,3,10,18);c.plus(20,17,3,True)
        kind=key.removeprefix('quotation.section-')
        if kind=='technical':
            for y in ((8,12,16) if not small else (8,13)):c.line([(5,y),(9,y)],radius=0)
        elif kind=='options':
            c.line([(5,7),(5,16),(9,16)],radius=.4)
            c.line([(8.5,8),(8.5,12.5)],True,radius=0)
        elif kind=='extra':
            box(c,5,7,4,5,True)
            c.line([(5,17),(9,17)],radius=0)
    elif key=='quotation.metadata':
        doc(c);c.circle(12,7,1.8,True)
        c.line(arc_points(12,15.5,4,180,360,24),True,radius=0)
        c.line([(8,19),(16,19)],radius=0)
    elif key=='quotation.payment-terms':
        box(c,2,4,20,16)
        c.line([(5,13),(19,13)],radius=0)
        for x in (6,12,18):
            c.circle(x,13,1.2,True,filled=True)
            c.line([(x,8),(x,10)],True,radius=0)
        if not small:c.line([(8,17),(16,17)],radius=0)
    elif key=='quotation.warranties':
        page(c,2,3,10,18)
        c.line([(5,7),(9,7)],radius=0)
        start=len(c.paths);shield(c);scale=c.size/24
        for path in c.paths[start:]:
            path['points']=[(.38*x+14.94*scale,.46*y+9.94*scale) for x,y in path['points']]
            path['tone']='accent'
    elif key in {'quotation.snapshot-sent','quotation.snapshot-draft'}:
        page(c,2,5,10,16)
        c.line([(5,2),(14,2),(14,8)],radius=.5)
        c.line([(5,10),(9,10)],radius=0)
        if key.endswith('sent'):
            c.line([(16,16),(18.5,19),(23,12)],True,radius=.5)
        else:
            c.line([(16,20),(16.5,16),(20.5,10),(23,12),(19,18)],True,closed=True,radius=.5)
    elif key.startswith('report.view-'):
        doc(c);kind=key.removeprefix('report.view-')
        if kind=='specification':
            for y in ((7,12,17) if not small else (8,16)):
                c.circle(7,y,.7,True,filled=True);c.line([(10,y),(17,y)],radius=0)
        elif kind in {'main-contract','subcontract'}:
            if kind=='main-contract':
                box(c,9,5,6,4,True)
                c.line([(12,9),(12,13),(7.5,13),(7.5,16)],radius=.4)
                c.line([(12,13),(16.5,13),(16.5,16)],radius=.4)
                box(c,6,16,3,3);box(c,15,16,3,3)
            else:
                box(c,6,5,6,4)
                c.line([(9,9),(9,16),(13,16)],radius=.4)
                box(c,13,13,5,6,True)
        elif kind=='tender':
            box(c,7,6,10,12)
            for y in (10,14):c.line([(7,y),(17,y)],radius=0)
            c.line([(13,6),(13,18)],True,radius=0)
        elif kind=='actual-cost':
            c.line([(7,18),(17,18)],radius=0)
            for x,y in ((8,12),(12,8),(16,14)):c.line([(x,17),(x,y)],True,radius=0)
        elif kind=='build':
            c.line([(7,18),(7,10),(12,6),(17,10),(17,18)],radius=.3)
            c.line([(7,13),(17,13)],True,radius=0)
            c.line([(12,13),(12,18)],radius=0)
        elif kind=='ibis':
            for y in (7,12,17):
                c.line([(7,y),(12,y)],radius=0)
                c.line([(15,y),(17,y)],True,radius=0)
        else:
            c.line([(7,9),(12,5),(17,9)],True,radius=.3)
            c.line([(8,10),(8,17),(16,17),(16,10)],radius=.3)
            c.line([(11,10),(11,17)],radius=0)
            c.line([(7,20),(17,20)],True,radius=0)
    elif key=='report.paper-size':
        box(c,5,6,14,16)
        c.line([(3,4),(3,1),(21,1),(21,4)],True,radius=.3)
        c.line([(9,11),(15,11)],radius=0)
    elif key in {'report.portrait','report.landscape'}:
        if key.endswith('portrait'):
            box(c,6,2,12,20)
            c.line([(9,8),(15,8)],True,radius=0)
            c.line([(9,13),(15,13)],radius=0)
        else:
            box(c,2,6,20,12)
            c.line([(6,10),(18,10)],True,radius=0)
            c.line([(6,14),(15,14)],radius=0)
    elif key=='report.branding':
        box(c,2,3,20,18)
        box(c,6,7,12,10,True)
        c.circle(14.5,10,1,True,filled=True)
        c.line([(6,15),(10,11),(15,17)],True,radius=.3)
    elif key=='calc.quantities-visible':
        box(c,2,3,20,18)
        c.line([(2,8),(22,8)],radius=0)
        for x in (8,16):c.line([(x,3),(x,21)],radius=0)
        for y in (12,17):c.line([(11,y),(13,y)],True,radius=0)
    elif key=='calc.price-percentage':
        c.circle(7,7,3);c.circle(17,17,3)
        c.line([(5,21),(19,3)],True,radius=0)
    elif key.startswith('calc.grid-'):
        box(c,2,3,20,18);kind=key.removeprefix('calc.grid-')
        if kind=='simple':
            c.line([(2,9),(22,9)],True,radius=0)
            c.line([(15,3),(15,21)],radius=0)
            c.line([(5,15),(11,15)],radius=0)
        else:
            c.line([(2,8),(22,8)],radius=0)
            xs=(7,15) if kind=='standard' else (6,13,18)
            for x in xs:c.line([(x,3),(x,21)],radius=0)
            if kind=='standard':c.line([(2,14),(22,14)],True,radius=0)
            else:
                c.line([(2,11),(22,11)],True,radius=0)
                c.line([(8,17),(11,17)],radius=0)
    elif key=='tree.collapse-level':
        for x,y in ((3,5),(7,12),(11,19)):
            c.line([(x,y),(14,y)],radius=0)
            c.circle(x,y,.7,filled=True)
        dimension_arrow(c,(20,4),(20,20),2.3)
    elif key=='calc.chapter':
        box(c,3,3,18,18)
        c.line([(3,8),(21,8)],True,radius=0)
        for x,y in ((7,12),(10,17)):c.line([(x,y),(17,y)],radius=0)
    elif key=='spreadsheet.sheet-add':
        box(c,3,2,18,12)
        c.line([(3,6),(21,6)],radius=0)
        c.line([(9,2),(9,14)],radius=0)
        c.line([(3,10),(21,10)],radius=0)
        c.plus(12,20,2.5,True)
    elif key=='format.decimals-decrease':
        c.circle(3,14,.9,filled=True)
        glyph(c,'0',7,3,8,11)
        dimension_arrow(c,(21,20),(3,20),2.5)
    elif key in {'data.excel-refresh','data.excel-link'}:
        box(c,3,2,18,12)
        c.line([(3,6),(21,6)],radius=0)
        c.line([(9,2),(9,14)],radius=0)
        c.line([(3,10),(21,10)],radius=0)
        if key=='data.excel-refresh':
            from b2_frame_completion import circular_arrow
            circular_arrow(c,12,20,2.7,135,405,1.3)
            c.paths.pop()
            scale=c.size/24
            c.fills.append({'tone':'accent','rings':[[(x*scale,y*scale) for x,y in ((12.3,23),(12.3,19.4),(15.9,23))]]})
        else:
            c.line([(10.5,17),*arc_points(7.5,20,3,270,90,24),(10.5,23)],True,radius=0)
            c.line([(13.5,17),*arc_points(16.5,20,3,270,450,24),(13.5,23)],True,radius=0)
            c.line([(9,20),(15,20)],True,radius=0)
    elif key.startswith('extension.'):
        extension_box(c)
        if key=='extension.item':
            box(c,8,8,8,8,True)
        elif key=='extension.importer':
            dimension_arrow(c,(12,6),(12,17),3)
        elif key=='extension.exporter':
            dimension_arrow(c,(12,17),(12,6),3)
        else:
            c.line([(8,1),(8,7),(16,7),(16,1)],radius=.3)
            dimension_arrow(c,(12,10),(12,18),2.5)
    elif key=='workspace.dock-back':
        box(c,2,3,17,18)
        c.line([(2,8),(19,8)],radius=0)
        box(c,14,11,8,8,True)
        dimension_arrow(c,(16,15),(8,15),2.5)
    elif key=='calc.hsb-wizard':
        box(c,3,3,18,18)
        for x in (7,12,17):c.line([(x,3),(x,21)],radius=0)
        c.line([(3,9),(21,9)],True,radius=0)
        c.line([(3,15),(21,15)],True,radius=0)
    return True
