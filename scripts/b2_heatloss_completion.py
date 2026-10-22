"""Heatloss source audit: mounted routes, tools, import and construction controls."""
import math
from b2_second_series import box, lightning
from b2_energy_completion import droplet, calculator
from b2_bim_completion import cube
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS={88:'Vertrekken en constructieoverzichten',89:'IFC en warmteverliesresultaten',
        90:'Bouwfysische rekenhulpen',91:'Model- en constructiebewerking',92:'Importbron en stappen'}
ROWS=[
(88,'thermal.rooms','Vertrekken','De vertrekkenlijst of het importonderdeel Ruimtes aanduiden/openen; geen startpagina.','2407c86db3b4ea05'),
(88,'thermal.modeller','Thermische modelbewerker','De gemonteerde modellerwerkruimte met 2D/3D-model en eigenschappen openen.','b4d9855e13de1cc1'),
(88,'construction.types','Projectconstructietypen','Het overzicht van project- of importconstructietypen aanduiden/openen; geen annotatielagenbeheer.','8c0b8cf43453ac93'),
(88,'construction.library','Constructiebibliotheek','De catalogusbibliotheek met beschikbare constructieopbouwen openen.','7fe56362526ba4dd'),
(88,'material.library','Materiaalbibliotheek','De materiaalafdeling van de catalogusbibliotheek openen.','8d4db57ec4308b4c'),
(88,'project.recent','Recente projecten','Het paneel met recent geopende project- of documentbestanden tonen.','5d5f07c5010c72ad'),
(89,'ifc.workspace','IFC-werkruimte','Naar de IFC-werkruimte navigeren; nog geen specifiek bestand inlezen.','e8626f52f0d480db'),
(89,'ifc.reconstruction-workspace','IFC-reconstructiewerkruimte','De route ifc-reconstructie openen; nog geen reconstructie uitvoeren.','cc743dbfe82c9295'),
(89,'thermal.results','Warmteverliesresultaten','De warmteverliesresultaten openen; geen nieuwe berekening starten.','256a5f4a64e8fe3b'),
(89,'thermal.overheating','Volledige TOjuli-werkruimte','De als volledig gelabelde TOjuli-route openen.','09c6734ae8ebf961'),
(89,'thermal.overheating-quick','Snelle TOjuli-werkruimte','De afzonderlijke quick-route voor TOjuli openen.','e899701055a971e8'),
(90,'tool.ventilation-balance','Ventilatiebalans','De werkruimte ventilation openen; geen ventilatiemaatregel toevoegen.','5e8f0136d50ee99f'),
(90,'tool.door-gap','Deurspleetrekenhulp','De rekenhulp tools/deurspleet openen; geen deur plaatsen.','63a42688dfd28926'),
(90,'tool.uw-window','Uw-rekenhulp','De rekenhulp voor de volledige raamwaarde openen.','444d55ed0764f251'),
(90,'construction.compare','Constructieopbouwen vergelijken','De werkruimte rc-compare voor constructievergelijking openen.','9ee5b00a30bc8ad4'),
(90,'tool.rainwater','HWA-rekenhulp','De hemelwaterafvoerrekenhulp openen.','95ce10e627008113'),
(90,'tool.ramp','Hellingbaanrekenhulp','De rekenhulp voor een hellingbaan openen.','c562a8d596e847c7'),
(90,'tool.angle','Hoekenrekenhulp','De hoekenrekenhulp openen; geen meetgereedschap op een tekening activeren.','f8c606572877fdbe'),
(90,'tool.thermal-expansion','Uitzettingsrekenhulp','De werkruimte tools/uitzetting openen.','19e5a7c55ddf9a05'),
(91,'thermal.window','Raamopening plaatsen','draw_window activeren; FloorCanvas plaatst op de gekozen wand een raamopening.','fb3f86f1255aed40'),
(91,'thermal.room-split','Vertrek splitsen','split_room activeren en via splitPolygon een vertrek in nieuwe polygonen verdelen; geen klembordknipactie.','32aa70772556335b'),
(91,'construction.studs-toggle','Stijlen in constructielaag','handleToggleStud voegt de heterogene stijlgegevens aan een materiaallaag toe of verwijdert ze.','beab9b650adec10d'),
(91,'thermal.room-ventilation','Ventilatiegegevens van vertrek','onToggleVent toont of verbergt de ventilatie-invoer van dit vertrek.','43ac8f5226446f2a'),
(92,'thermal.import-source','Thermisch importbronbestand','Het onderdeel Bestand of het Thermal Import JSON-bronformaat aanduiden; geen generieke upload naar een dienst.','47e1f4c62d6c32d2'),
(92,'nav.next-step','Volgende stap','handleNext gaat naar de volgende wizardstap; geen browsergeschiedenis of toepassen-en-volgende.','9b22095f989738d2'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De bepalende richting of markering blijft ononderbroken voor de achterliggende contour.' for k in KEYS if k.startswith(('thermal.','tool.','construction.','ifc.','nav.'))}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}


def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)


def exclude(ids,reason):
    for rid in ids.split():EXCLUDED[rid]=reason


def dispatch(ids,targets,reason):
    for rid in ids.split():DISPATCHERS[rid]=targets;DISPATCH_EVIDENCE[rid]=reason


reuse('4c8fc1f9a6a84558 3b6edbad3290b272','file.save','TitleBar onSave is door AppShell aan performSave gebonden; Backstage handleSave bewaart het actieve project.')
reuse('15d8eef8aa61c263 2a43bcc59fc1ad4e','ui.settings','De appvoorkeuren openen via de werkelijk doorgegeven callback.')
reuse('f70155ef51f18554','window.minimize','De native titelbalk minimaliseert het Tauri-venster.')
reuse('e655995c6added0c','window.restore','Herstelvariant wanneer het venster gemaximaliseerd is.')
reuse('092f04d1024b4f67','window.maximize','De andere isMaximized-tak maximaliseert; het oude cataloguslabel Herstellen is hiervoor onjuist.')
reuse('8517a14cbbffadc9 5fa0ccb4f25121f8','window.close','De native titelbalk of Afsluiten sluit het Tauri-venster; webmode heeft geen native vensterbediening.')
reuse('f68bb544a52ec078','ui.about','Het Over-paneel van de app openen.')
reuse('4d63dcc7e1bd9895','document.close','handleClose reset het huidige project en sluit Backstage; het appvenster blijft bestaan.')
reuse('30145ffe388936b1','extensions.manage','Het paneel extensions openen; geen specifieke extensie uitvoeren.')
reuse('6966968d3d1e80e7','file.new','De normkeuze openen en na bevestiging newTab/resetToExample/setNorm uitvoeren.')
reuse('01cbb5c91e1f1b76 92c5a41ed5dc33fd','file.open','Openen toont de bestemmingskeuze; de lokale tak opent en leest een bestaand ifcenergy-project.')
reuse('6d7dee80256f95b8 7a64faff04e8c0c5','file.save-as','Een nieuwe lokale bestemming voor het huidige project kiezen; daarna currentLocalPath bijwerken.')
reuse('2d59176499d09124','file.save-as','handleSaveAsServer vraagt een nieuwe projectnaam en schrijft via saveNewServerProject een nieuw serverproject.')
reuse('059a2d99eebfba06 ebf106f99ee16577 06ce6501e556f997','project.library','De route projects toont de serverprojectlijst; geen projectbestand reeds geopend. IconFolder hoort bij ProjectsNavLink, niet bij de navgroepchevron.')
reuse('a6728c476ef45cd0','ui.close','De terugknop Bestand sluit de Backstage-overlay; geen geschiedenis terug.')
reuse('034293a1225eae09 c8e1e9b743e2cb7a','link.open-external','De Foundation-website of GitHub-repository extern openen.')
reuse('bf59ebeec790ce23','status.error','Parsefout van het gekozen thermische importbestand.')
reuse('3018ca31d70744cd 831f4e85660b0632 093942a1fdb56595 21a382a94ab043c8','status.warning','Waarschuwing over ontbrekende verwarmde ruimtes, constructielagen of importgegevens; bronconditie en tekst gelezen.')
reuse('d5178fb78570f647 d92da45024d383ef 79d18e0643e5cd2c','status.success','Berekende U-waarde, gelezen geldig importbestand of import zonder waarschuwingen: toestand, geen nieuwe opdracht.')
reuse('d57a30840a469a81','file.import','onImport past de gecontroleerde thermische importgegevens op het project/model toe; geen stapnavigatie.')
reuse('bdb9e137e4ae9e0a','tree.collapse','Uitgeklapte constructie-entree invouwen.')
reuse('6f14a35d57a5245a','tree.expand','Ingeklapte constructie-entree uitvouwen.')
reuse('0a866c9fe62e408c','nav.back','handlePrev gaat naar de vorige importstap, geen undo.')
reuse('f06cb4736e0508b4','thermal.openings','De statistiek Openingen in ImportSummary duidt dezelfde verzameling raam/deuropeningen aan als de importstap.')
reuse('afe48aff9ded5c49','ifc.import','Het actieve modeller:import-ifc-event wordt in Modeller aan de native of web-IFC-import gebonden.')
reuse('ed920be58c643a7e','file.import','De PDF-knop accepteert PDF/afbeeldingen en rendert de eerste PDF-pagina als onderlegger in het huidige model.')
reuse('27bd95751cdca460','file.export','Het als IFC gelabelde export-event schrijft werkelijk modelToIfcx-JSON met extensie .ifcx; geen reguliere STEP-IFC-export claimen.')
reuse('6f6e3ea4cce84ccd','file.open','De als projectimport gelabelde knop leest ifcenergy/JSON via openProjectFile en vervangt het project via setProject; thermische JSON gaat naar de wizard.')
reuse('2506e90c2148267d d654d8a029612ac5','file.export','Een projectsnapshot via exportIfcEnergy wegschrijven als .ifcenergy; geen regulier IFC-model of alleen resultaat-JSON.')
reuse('bbdfc78cf6b7ecab caedf11e11e1368a','thermal.rooms','Rooms/Ruimtes is de dataset of importstap met vertrekken; geen startpagina.')
reuse('6a6dddf90c2701a4 2dedf02c41bf40f2','construction.types','Constructietypen in de importstatistiek of importstap aanduiden; geen tekenlagen.')
reuse('8cc76c3a3d0dbdd5','edit.select','Het actieve select-gereedschap van FloorCanvas kiezen.')
reuse('d0827b2b48029bb1','draw.polygon','draw_polygon verzamelt punten en maakt een gesloten vertrekpolygoon.')
reuse('2f4c2d501871e0ad','edit.redo','Het gemonteerde lint roept modellerStore.redo aan.')
reuse('cec440e735ac3284','edit.undo','Het gemonteerde lint roept modellerStore.undo aan.')
reuse('4adcc6a636431f7d','edit.clear-all','modeller:clear-view leegt via importModel([],[],[]) de modelgeometrie en selectie; niet alle projectinstellingen.')
reuse('baf3dc94b6d5df5d a863e311203c7a9e eb56747327d5839c','object.edit','Legenda en daadwerkelijke laag-/U-waarde-editor voor de gekozen constructie; geen vrije-handtekenen.')
reuse('1c3f287efd0d15c4 22ddc73b1d9b4710 84641740b70c9cb0','object.rename','De naam van de gekozen constructie/catalogus-entree bewerken, geen nieuw exemplaar opslaan.')
reuse('9f7502af2418f8b2 9d93f4b72d0e2496','ui.dropdown','De eigen selectiecomponent of themakeuze uitklappen.')
reuse('1094c5802d2cdacb','report.options','Het rapportoptiepaneel in- of uitklappen.')
reuse('a52a39c451768772 dbee487ba9bc4873','construction.layer-up','De fysieke materiaallaag met de vorige laag verwisselen in RcCalculator of LayerEditor.')
reuse('63e8b0c9cc72d4ae 3f250ffd3dc553f1','construction.layer-down','De fysieke materiaallaag met de volgende laag verwisselen.')
reuse('30548524df375cb2 87a30a3b30d80150 fbd89e3313795755 60c212c6d900001a 34255fa95078d840 06ff0004a35b447f','edit.delete','De benoemde materiaallaag, het vertrek, grensvlak, de zone of projectconstructie verwijderen; scope staat bij de bediening.')
reuse('05555d5bb3f2f606 cefcb7c554ec4629 809a7e0e92d4a5ab','ui.close','Foutmelding, laagdialoog of IFC-typecontrole sluiten.')
reuse('d69f278f4eea7e0e cb92de9a3d2a3547 ca1e3a06af026594','project.properties','De projectgegevenspagina openen; de snelkoppeling Zones beheren komt op dezelfde pagina met ZonesCard.')
reuse('e01afbf24611b047','calculation.recalculate','useRunCalculation voert de projectberekening uit en opent bij succes de resultaten; geen rekenhulp alleen openen.')
reuse('29d3f22fd7e251cf','file.download','Download PDF haalt het reeds gegenereerde rapport uit de bestaande object-URL; genereert niets opnieuw.')
reuse('a72ae4ff34dc567f','object.add','addRoom(createRoom(...)) voegt een vertrek toe en opent rooms.')
reuse('79c18d3b3002dbdf a7468bc6f4e039f5','tool.uvalue','Nieuwe constructie navigeert uitsluitend naar rc; hetzelfde Rc/U-rekenwerkvlak als de zijbalkkeuze.')
reuse('6e032566b5943a9a 00864330cdc29288','report.generate','Rapportdata opbouwen volgens de gekozen norm en PDF laten genereren; los van Download PDF.')
reuse('cf808a43fee7f0e4','calculation.performance','De BENG-werkruimte voor energieprestatie openen; geen directe berekenknop.')
reuse('fec60a61857800bd','calculation.settings','De werkruimte warmteverlies/instellingen openen voor rekenvoorkeuren.')
reuse('1b0b505964d67e2f caf675ac7d0e1518','ui.help','De gemonteerde help-route openen.')
# A definition asset is assessed through every concrete NAV_GROUPS use above.
reuse('11e58ad28e8bedea','thermal.rooms','IconGrid is alleen aan de route rooms gekoppeld.')
reuse('4720ef7a386a87be','thermal.modeller','IconCube is gekoppeld aan de modeller-route, niet een importopdracht.')
reuse('11549391ebccb028','construction.library','IconBook duidt de construction library-route aan.')
reuse('0a6777060bf788f0','material.library','IconSwatches duidt de material library-route aan.')
reuse('0431956b0c866caf','ifc.workspace','IconIfc duidt de IFC-werkruimte aan.')
reuse('4d7220f5f1eda0b5','ifc.reconstruction-workspace','IconIfcReconstruction duidt de reconstructiewerkruimte aan.')
reuse('aac56b595ab0d32d','tool.ventilation-balance','IconWind is gekoppeld aan de ventilatiebalansroute.')
reuse('5ad47255eb67b07f','tool.door-gap','IconDoor is gekoppeld aan de deurspleetrekenhulp, geen deurplaatsing.')
reuse('d0baea76e1af6a13','tool.rainwater','IconDroplet is gekoppeld aan de HWA-rekenhulp.')
reuse('856cd5025ea985da','tool.ramp','IconRamp is gekoppeld aan de hellingbaanrekenhulp.')
reuse('bda35d4032a0e787','tool.angle','IconAngle is gekoppeld aan de hoekenrekenhulp.')
reuse('16c16a19a7dcdc73','tool.thermal-expansion','IconThermometer is gekoppeld aan de uitzettingsrekenhulp.')
reuse('bae88116f5af0184 d6fb848102e9e22b','construction.types','De projectconstructietypenroute gebruikt IconClipboardList; geen willekeurige notitie-opdracht.')
reuse('8ea9ad112c5cd8ef','thermal.import-source','Vaste kleine aanduiding van het verwachte Thermal Import JSON-bronformaat.')

dispatch('050dab13af903f63 893f50f68dfa3213 0b27df6882c05d45',('tree.expand','tree.collapse'),'De collapsed/expanded-waarde bepaalt uit- of invouwen van vertrekgrensvlakken of navigatiegroepen; de pijlvorm draait met dezelfde toestand.')
dispatch('1b709d76cad84599',('thermal.results','thermal.overheating','thermal.overheating-quick','calculation.performance'),'IconBarChart wordt in NAV_GROUPS voor results, tojuli, tojuli/quick en beng gebruikt; de route bepaalt de afzonderlijke werkruimte.')
dispatch('7239179a14fa9073',('calculation.settings','tool.uvalue','tool.uw-window','construction.compare'),'IconLayers wordt in NAV_GROUPS gebruikt voor rekenvoorkeuren, rc, uw en rc-compare; dit zijn geen annotatielagen.')
exclude('e4fcf0e3e7b4e580 6b9117258c379e0d bbea865e564891a2','TitleBar Undo, Redo en Print hebben geen onClick en worden door AppShell ook niet als callback doorgegeven; het werkende modellerlint/rapport is afzonderlijk beoordeeld.')
exclude('95da62ac3c51f91e e1ab12a0785e0ffe','Vabi-onderdelen zijn expliciet disabled en hebben slechts een in-ontwikkeling-toast; geen werkende importfunctie.')
exclude('49f33a4d441b830e','Deze importmenutak klapt alleen het expliciet uitgeschakelde Vabi-onderdeel uit. Werkende model-/thermische importbedieningen zijn apart beoordeeld.')
exclude('3fc0d4e81f663367','handleImportDwg meldt uitsluitend dat DWG later komt; er wordt geen DWG gelezen.')
exclude('5f654ab46818f382 73623509a48f8a53 f29f990b7e23c09f','De annotatieknoppen zetten alleen annotate_leader/dimension/text in de store. De gemonteerde FloorCanvas behandelt deze tools niet en Modeller heeft geen annotatiecallbacks; geen werkende plaatsing aangetoond.')
exclude('83d3b3a546cfeea0 cd818894e56d6f1f','Grote illustratie in bestands-dropzone of lege constructielijst; de kleine werkende stap-/typiconen zijn afzonderlijk beoordeeld.')
exclude('1ecb706e57f79731 6c3a7916b448f708 f72a87916a99e08a 5b8918482f71f9ce','Applicatiebeeldmerk, marketingillustratie of favicon; geen vast bedieningsicoon.')
# Full pinned-source search for Ribbon imports/JSX shows this old component is
# only exported from the barrel; AppShell mounts components/ribbon/Ribbon.
exclude('d6eb0a92c9c481db e804d380c2c8b7a7 b39850e22029b75f 9db7e93cffd26b19 6077fd068833ef1d 787842559005b1ee ee7f74cb6daed277 3c97244bf252903b 105b0cf916bbcb04 f3b4f50296c1fab1 1b2d80d67c2f0651 665ad782f2393314 812a518075c0c03f 537a5986e78c3791 227a5dd6182eaf0b 3e03f0e6b214dde5 5da4ba3cb0951f7c 3da4ddb359fb7df9 bd07eb8507ede8ad 03fa82011cf536d9 8eb0bff9f1c6f16e','Oude components/modeller/Ribbon is niet gemonteerd: volledige zoekactie op de gepinde frontend toont alleen de definitie en barrel-export, terwijl AppShell de hoofdribbon met ModellerTab gebruikt. Actieve equivalente functies zijn afzonderlijk beoordeeld.')


def slabs(c,x=3,y=3,w=18):
    for dy in (0,6,12):box(c,x,y+dy,w,4)


def room(c):
    box(c,3,3,18,18)
    c.line([(10,3),(10,21)],radius=0);c.line([(10,12),(21,12)],radius=0)


def house(c):c.line([(3,10),(11,3),(19,10),(19,21),(3,21)],closed=True,radius=.4)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='thermal.rooms':
        box(c,2,3,11,18)
        c.line([(7,3),(7,21)],radius=0);c.line([(7,12),(13,12)],radius=0)
        c.line([(20.5,5),(20.5,17)],True,radius=0);c.circle(20.5,19,2,True)
    elif key=='thermal.modeller':
        c.line([(2,21),(2,3),(8,3),(8,9),(12,9),(12,21)],closed=True,radius=.6)
        c.line([(16,20),(16.5,16),(20.5,10),(23,12),(19,18)],True,closed=True,radius=.5)
    elif key=='construction.types':
        slabs(c,3,3,12)
        for y in (5,11,17):c.circle(20,y,1,True,True)
    elif key=='construction.library':
        c.line([(3,21),(3,4),(11,2),(21,4),(21,21),(11,19)],closed=True,radius=.4)
        c.line([(11,2),(11,19)],radius=0)
        for y in (7,11,15):c.line([(14,y),(18,y+.8)],True,radius=0)
    elif key=='material.library':
        box(c,2,4,6,16);box(c,9,4,6,16);box(c,16,4,6,16)
        for x in (5,12,19):c.line([(x-1,9),(x+1,9)],True,radius=0)
        for x,y in ((4,15),(11,17),(19,14)):c.circle(x,y,.6,False,True)
    elif key=='project.recent':
        c.circle(9,9,6);c.line([(9,5),(9,9),(12,11)],radius=.3)
        for y,w in ((18,21),(22,17)):c.line([(3,y),(w,y)],True,radius=0)
    elif key=='ifc.workspace':
        c.line([(12,2),(20,6),(20,18),(12,22),(4,18),(4,6)],closed=True,radius=.3)
        c.line([(4,6),(12,10),(20,6)],radius=0)
        c.line([(12,10),(12,22)],radius=0)
        c.line([(4,12),(12,16),(20,12)],radius=0)
        scale=c.size/24
        c.fills.append({'tone':'accent','rings':[[(px*scale,py*scale) for px,py in ((12,2),(20,6),(12,10),(4,6))]]})
    elif key=='ifc.reconstruction-workspace':
        cube(c);x=5*math.sqrt(3);scale=c.size/24
        c.fills.append({'tone':'accent','rings':[[(px*scale,py*scale) for px,py in ((12,2),(12+x,7),(12,12),(12-x,7))]]})
    elif key=='thermal.results':
        box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0)
        for x,h in ((7,5),(12,9),(17,7)):c.line([(x,19),(x,19-h)],True,radius=0)
    elif key in {'thermal.overheating','thermal.overheating-quick'}:
        c.line([(2,10),(7,5),(12,10),(12,21),(2,21)],closed=True,radius=.6)
        if key=='thermal.overheating':
            c.line([(20.5,5),(20.5,17)],True,radius=0);c.circle(20.5,19,2,True)
        else:lightning(c,19.5,12,7,16)
    elif key=='tool.ventilation-balance':
        box(c,4,3,16,18)
        dimension_arrow(c,(2,8),(16,8),2)
        dimension_arrow(c,(22,16),(8,16),2)
    elif key=='tool.door-gap':
        c.line([(2,18),(2,2),(12,2),(12,18)],radius=.7)
        c.line([(5,18),(5,5),(10,5),(10,18)],radius=.5)
        c.circle(8,11,.6,filled=True)
        c.line([(1,23),(13,23)],radius=0)
        c.line([(17,18),(21,18),(21,23),(17,23)],True,radius=.4)
    elif key=='tool.uw-window':
        box(c,2,3,10,18);c.line([(7,3),(7,21)],radius=0)
        calculator(c,16,7,7,14,True)
    elif key=='construction.compare':
        slabs(c,2,3,7);slabs(c,15,3,7)
        dimension_arrow(c,(10,8),(14,8),1.5)
        dimension_arrow(c,(14,16),(10,16),1.5)
    elif key=='tool.rainwater':
        c.line([(2,9),(8,4),(14,9)],radius=.6)
        c.line([(2,12),(13,12),(13,20),(19,20)],radius=1.4)
        droplet(c,5,18.5,5,6)
    elif key=='tool.ramp':
        c.line([(2,21),(12,21),(12,6)],closed=True,radius=.5)
        calculator(c,16,7,7,14,True)
    elif key=='tool.angle':
        c.line([(2,4),(2,21),(12,21)],radius=.5)
        c.line(arc_points(2,21,5,-90,0,24),radius=0)
        calculator(c,16,7,7,14,True)
    elif key=='tool.thermal-expansion':
        box(c,3,8,18,8)
        dimension_arrow(c,(3,3),(21,3),1.4)
        dimension_arrow(c,(21,21),(3,21),1.4)
    elif key=='thermal.window':
        for x1,x2 in ((2,8),(16,22)):
            c.line([(x1,11),(x2,11)],radius=0);c.line([(x1,15),(x2,15)],radius=0)
        box(c,8,9,8,8,True);c.line([(8,13),(16,13)],True,radius=0);c.plus(20,21,2,True)
    elif key=='thermal.room-split':
        box(c,3,3,18,18);c.line([(12,3),(12,21)],True,radius=0)
        c.line([(6,8),(8,8)],radius=0);c.line([(16,16),(18,16)],radius=0)
    elif key=='construction.studs-toggle':
        box(c,3,4,18,16)
        for y in (9,15):c.line([(3,y),(21,y)],radius=0)
        for x in (9,15):c.line([(x,4),(x,20)],True,radius=0)
    elif key=='thermal.room-ventilation':
        box(c,2,4,10,17)
        for y in (7,12,17):dimension_arrow(c,(17,y),(23,y),1.4)
    elif key=='thermal.import-source':
        box(c,3,2,18,20)
        c.line([(9,7),(7,7),(7,11),(6,12),(7,13),(7,17),(9,17)],True,radius=.4)
        c.line([(15,7),(17,7),(17,11),(18,12),(17,13),(17,17),(15,17)],True,radius=.4)
    elif key=='nav.next-step':
        dimension_arrow(c,(3,10),(21,10),3)
        for x in (5,12,19):c.circle(x,20,.8,x==19,True)
    return True
