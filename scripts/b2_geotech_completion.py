"""Geotechniek controls: events followed to mounted views and store operations."""
from b2_second_series import box
from b2_bulk_series import page
from b2_session_two import dimension_arrow

GROUPS={97:'Kaart en geotechnische rapportuitvoer',98:'Tekeningkaders en hoekverbindingen'}
ROWS=[
(97,'map.export-image','Kaart als afbeelding','MapView.handleExportImage maakt een PNG van de actuele kaartcontainer met schaalstok; geen foto maken.','05002d30f115e71b'),
(97,'report.open-viewer','Rapport in systeemviewer','Het actuele rapport in de systeem-PDF-viewer of een nieuw browsertabblad tonen. De lintvariant genereert eerst preview_report; de previewknop gebruikt de al opgebouwde bytes.','94f2b92aade7deb6'),
(97,'geo.quote-request','Offerteaanvraag voorbereiden','setOffertesOpen opent de dialoog met sondeerbedrijven en aanvraaggegevens; nog geen aanvraag verzenden.','46f53f643826483a'),
(98,'drawing.frame-import','SVG-tekeningkader kiezen','Een SVG-bestand kiezen en als tekeningkader opslaan via handleFrameFile; geen kozijn plaatsen.','f1a4346a2ddd8a41'),
(98,'transform.corner-join','Lijnen tot hoek verbinden','Twee lijnen kiezen en van beide het dichtstbijzijnde eindpunt op hun berekende snijpunt zetten. De als Trim en Extend gelabelde gereedschappen voeren dezelfde geometrische bewerking uit.','7bbe3a32111a5f30'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De bepalende pijl of verbinding ligt volledig vóór de achterliggende contour.' for k in KEYS}
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}
EVIDENCE={
 'view.fit':'Geotechniek ogs:zoom-fit -> ChartCanvas zoom=1/panX=panY=0. chart-renderer.visibleDepthWindow gebruikt fullRange/zoom; 1 past dus werkelijk het volledige dieptebereik, geen ongecontroleerde labelkoppeling.',
 'edit.clear-all':'Geotechniek onClearAll leegt geplaatste sonderingen/rasters, lijnen en coördinaattags; polygonen, notities, onderlegger en kader vallen niet onder deze bronscope. Geen volledig leeg papier claimen.',
}


def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)

def exclude(ids,reason):
    for rid in ids.split():EXCLUDED[rid]=reason

reuse('4d5ae212327c617d','file.new','newProjectDocument maakt een nieuw projectdocument, met eigen tab en metadata.')
reuse('799e2a727798758b a85593274babda6a 5b87af32f7bb29ab 179d94e9268631b3','file.open','Openen kiest/leest via pickAndRead en de extension-routed loader een bestaand bestand; de tabplus/startknoppen openen hiervoor eerst Bestand.')
reuse('8cb8e1273dca90c5 e519204451e30b12','file.save-as','Ook de als Opslaan gelabelde projectknop vraagt altijd een nieuwe bestemming via saveProject/save-dialog. Opslaan als opent voor CPT een formaatkeuze met save_cpt_as; voor project dezelfde saveProject-route. Geen bestaande-padoverschrijving claimen.')
reuse('378a8c99317f3f47','file.export-options','Het Bestand-exportpaneel openen; de CSV/GeoJSON-knoppen schrijven pas daarna.')
reuse('f2b1f0c6970db6e7 7ab492d56f2e3b0b','ui.settings','De door App doorgegeven callback opent SettingsDialog.')
reuse('0f1df500078ff1ca','ui.about','Het Over-paneel openen.')
reuse('f21bbc73db49d8f0 012bacfdd1bfd6cb','window.close','getCurrentWindow().close sluit het appvenster; niet alleen een documenttab.')
reuse('6931cc7fafe75a21','extensions.manage','Het gemonteerde ExtensionManagerPanel openen.')
reuse('82b57081efc4c28c','window.minimize','handleMinimize minimaliseert het Tauri-appvenster.')
reuse('a94b330877a77914','window.restore','De isMaximized-arm van toggleMaximize herstelt de vorige vensterafmetingen.')
reuse('5a91d2b0cfcbd3cc','window.maximize','De andere toggleMaximize-arm maximaliseert het appvenster.')
reuse('bcaae3a021b8521e','document.close','closeDoc verwijdert alleen de gekozen geopende documenttab en de bijbehorende cache, en activeert een resterende tab. Geen bestand wissen.')
reuse('9cb708be878d8df3 bc4fcfcb48aa8d75','file.type-other','FileIcon duidt een CPT/boring/grondwaterput-document in tab of gegevenskop aan; het cataloguslabel Sluiten hoort bij de naastgelegen knop en is hier onjuist.')
reuse('080581cfa587ec0c 0ecf48455df6c712','file.type-project','FolderIcon duidt het geopende projectdocument aan, ook in de projectkop. Geen tab sluiten of mapkeuze starten.')
reuse('93ceae4d339b93bf','view.zoom-out','ogs:zoom-out wordt in ChartCanvas ontvangen en vermenigvuldigt de grafiekzoom met 0.8, met ondergrens.')
reuse('5cfccb966eeda3dc 27a8faaf90880f8a 1550ee9aadd5e9b1 5721f2dd95f5a769 77515fc958162dcf','project.properties','Projectinfo en de als Nieuw project gelabelde startacties openen ProjectSettingsDialog. Pas de afzonderlijke NoProjectHint-knop maakt een project aan. ReportPreview gebruikt hetzelfde door App ontvangen ogs:open-project-settings-event.')
reuse('2c8000ce08017d3b','measure.distance','ogs:measure-toggle activeert MapView-meetmodus; handleMeasurePoint verwerkt twee kaart- of CPT-punten en toont de afstand.')
reuse('8826ffb159b1670a','report.generate','generatePdf bouwt het rapport uit cptIds/project en actuele sectiekeuzes via generate_report en schrijft de gekozen PDF-bestemming.')
reuse('7ce29de29a1f89a2 ae90a01a4cdaece7','file.print','De tekening-printbridge zet papierformaat/styles, laadt de kaarttegels en roept window.print aan. Anders dan de losstaande niet-werkende titelbalk-/Backstage-printknoppen.')
reuse('60e16a8947cf8612 50876a5a3e3afa42','file.import','overlayInputRef opent de bestandskeuze; handleFile zet een afbeelding/PDF als tekeningonderlegger. Geen gewone afbeeldingsplaatsing in een PDF-document.')
reuse('9b0f5e5e9a34ead2 949d19e4869a568c a9c5f20ac8720284','transform.move','De lintbridge bewapent/start verplaatsen; de rastergrip wijzigt het centrum in RD op drag en houdt kaart-pan uit.')
reuse('ecd077283361d2c6 7d921f6e7a1cd0c1','export.cad','doExportDwg vraagt RD/lokale oorsprong en DWG/DXF-bestemming, bouwt entities/layer_colors/images en roept export_dwg aan. Desktopfunctie; webvariant meldt dat deze daar niet beschikbaar is.')
reuse('e14b273637d541a4 ea518202b3d5d9f8','file.export','Het actuele tekeningpapier rasteriseren en met jsPDF als PDF wegschrijven. Geen printerdialoog en geen 300dpi-export van alle pagina’s uit de PDF-app.')
reuse('38070bcb4e7d2998 8c6ec3746052e83f 37788abc960f9507','edit.duplicate','copySelection voegt een nieuwe raster/lijn/markerkopie met nieuwe id en verschoven positie toe; geen klembordkopie.')
reuse('ee631d4521daa133','edit.delete','deleteSelection verwijdert het geselecteerde tekenobject; de gedeelde deleteIcon-definitie heeft daarnaast Wis alles en wordt apart beoordeeld.')
reuse('cda052252d8c9807 bacd1233d7e4e3e9','selection.box','onSelectMode schakelt een rechthoekselectie op het papier en annuleert actieve plaats-/tekengereedschappen.')
reuse('1b1c4bc59766e2ac 04ae596c43fdafe7','draw.polygon','Vlakmodus verzamelt hoekpunten in vlakDraft; Enter/dubbelklik sluit de polygoon.')
reuse('9ac2b721560d1273 ab548c29a2962eb8','draw.note','onAddNote activeert plaatsing; volgende kaartklik vraagt tekst en bewaart de tekstnotitie.')
reuse('6b5b63834e62552e 993c5f60f33645a8','draw.dimension','onDrawDim activeert twee puntklikken en maakt een DrawnLine met kind dimension.')
reuse('e2f72ca9d5d63e8d 5fd0b507f3557495 b4f7a82f32402d07','transform.corner-join','De als Trim/Extend gelabelde varianten komen allebei in handleCadLineClickRef: lineIntersectionRd berekenen en beide nabije eindpunten op hetzelfde snijpunt zetten. Geen conventionele eenzijdige trim/extend claimen.')
reuse('87f228e1974b8e03 25f19fb7f8bd1959','transform.mirror','handleCadMapClick spiegelt beide eindpunten van de geselecteerde lijn over een gekozen tweepuntsas via mirrorPointRd.')
reuse('452b9eb8ff3f4488 4a6c9f025df7db4f','transform.offset','Bronlijn/afstand/zijde kiezen; offsetLineRd maakt een nieuwe parallelle lijn met nieuwe id.')
reuse('0715f2542ef5cb04 b52f1aea0a18f73a','panel.left','De linker verkenner dichtzetten of de StartSidebar via dismissStartSidebar sluiten; geen boomtak inklappen.')
reuse('dab5310757a2838d','panel.right','Het rechter eigenschappenpaneel dichtzetten.')
reuse('2968ee81d0e1c2bb 0fccbd9d69afc867','ui.dropdown','De ThemedSelect- of themakeuze open-/dichtklappen.')
reuse('3d48df8238af919b','ui.close','De Bestand-overlay via onClose sluiten; geen navigatiegeschiedenis terug.')
reuse('5dce879360d918da 4e89bf544cbabddc','link.open-external','De Foundation-site of GitHub-organisatie extern openen via openExternal.')
reuse('2a9ed397ba1ed5ee','file.export','exportCsv schrijft de actieve sondering via export_csv naar een gekozen CSV-bestand.')
reuse('08b4305ef7ad5024','object.layers','Vaste kopaanduiding bij GisLayerPanel met onder-, overlay- en datalagen; geen kaartobject plaatsen.')
reuse('ac2c58bae738627a 696fdce7e19b4a9e ba1a0a1dcd7ebb59','file.import','Bestandskeuze en addCptToActiveProject/addBoreToActiveProject voegen GEF/BRO-XML-brongegevens aan het project toe; geen locatie op de kaart tekenen.')
reuse('652c3cfbcbc66f14','object.hide','Het zichtbare oog toont de huidige toestand; onClick toggleHidden maakt de CPT onzichtbaar. B2-keuze volgt de actie, niet het oude toestandsglyf.')
reuse('342bc3514ab12269','object.show','Het doorgestreepte oog toont huidige verborgen toestand; toggleHidden maakt de CPT zichtbaar. Tegengestelde actie expliciet behouden.')
reuse('a47ee640a97d1c46','view.search','Vaste zoekveldmarkering voor adres/plaats/RD/WGS84; de invoer en Enter/selectie sturen de kaart naar de gevonden locatie.')
reuse('332f0e2d57d3714a','report.open-viewer','De previewknop opent de reeds opgebouwde pdfBytes via open_report_pdf of pdfUrl in een browsertab; dezelfde rapportbekijkfunctie als het lint, geen rapport genereren-en-opslaan.')
reuse('d98e3175f05d8c76','geo.sondering','De gebruikte definitie staat bij ogs:tekening-toggle-place en activeert sonderingplaatsing; niet de modelmarker zelf.')
reuse('065d15be0c8ae16a','geo.bore','De gebruikte definitie activeert boringplaatsing via de bijbehorende eventbridge.')
reuse('752825c05c7e6f59','drawing.frame-import','frameIcon is uitsluitend bij de SVG-kaderkeuze gebruikt; handleFrameFile bewaart het SVG als frame.')
reuse('a22bacb1096abc50','geo.sounding-grid','De gebruikte rasterdefinitie activeert placeRaster, dat één parameterraster met rijen/kolommen/afstand/rotatie maakt.')
reuse('dded80a2868bf018','geo.coordinate-tag','De gebruikte definitie activeert het plaatsen van een blijvende RD-coördinaattag.')
reuse('742822aafcaa56c0','geo.quote-request','De offertes-extensie koppelt quotesIcon aan het openen van de aanvraagdialoog; geen mail reeds verstuurd.')
reuse('6135fb6c298e1ade dfe5b78e80ade50a','transform.rotate','De lintvariant vraagt een hoek; de rastergrip berekent de hoek uit drag rond het centrum en wijzigt raster.rotation. Objectrotatie, geen kaartcamerarotatie.')
reuse('d733d8a4813bfe37 f06210ecb21e1225','draw.line','De gebruikte definitie en concrete lintplaats activeren DrawnLine-kind line met twee puntklikken.')
DISPATCHERS['09470ff35057aa15']=('edit.delete','edit.clear-all')
DISPATCH_EVIDENCE['09470ff35057aa15']='Dezelfde deleteIcon-definitie wordt gebruikt voor geselecteerd object verwijderen en voor Wis alles. onDelete verwijdert de selectie, onClearAll leegt plaatsingen/rasters/lijnen/coördinaattags.'
exclude('7e5770680c27e73e','De Backstage-printknop roept alleen actionAndClose zonder functie aan en sluit de overlay; print is niet aangesloten. De werkende tekening-printplaats is afzonderlijk hergebruikt.')
exclude('4e8ea19f0c0f0caf 4b8439afc32fa827 cb3a221953c5cea9','Het importpaneel en de twee kaarten tonen alleen beschrijvende divs zonder bestandskeuze/klikactie. Geen werkende importfunctie claimen; Openen en projectgegevensimport bestaan afzonderlijk.')
exclude('cdca90b676d89128 5f3f4f7684e7651e 6ef05f209f36cfcc ef78c1d83e86be24','Titelbalk-snelknoppen hebben geen onClick en krijgen geen actieprops; louter weergave van nog niet aangesloten bediening.')
exclude('04dc486c4361c7cb','Dock back zendt via requestDockBack alleen openaec:dock-request. Volledige gepinde frontendzoekactie vindt geen ontvanger; confirmDock is nergens aangeroepen. Geen werkende terugplaatsfunctie bewezen.')
exclude('72e22852d0462177','Grote cloudillustratie in de sleepbestands-overlay; geen afzonderlijk bedieningsicoon.')
exclude('b1f9719bb794d961 3b7171e21a1167ed c5718d5c5ef0b6ba 55bebadfb110fcde 10ab468bc9f3d168 bff4aa93ff1a9941 1714a19920f0f493','CalcModule.icon is metadata zonder renderer: NewCalculationDialog en ProjectTreePanel tonen alleen modulenamen/statusbadges. Volledige gepinde frontendzoekactie vindt geen module/mod/m.icon-gebruik. Publieke webregistry is leeg; desktop/dev-modules blijven concept/experimental, geen berekeningsicoon op basis van alleen metadata verzinnen.')
exclude('2af703c5e544ef91 9268076b022ce1f8 28434fa69d92b8dc cc664d36f8c06eb2 a6ffb9712f3da69e','Appbeeldmerk in titel, Over, Start, welkom of favicon; geen vaste bedieningsfunctie.')
exclude('80b463722f7d4ed1 d7925aa3e0906731 14b93af6c8f97b90 1f63084210fb16a7 ee9508b60d5fbed4 33525ca865cebd26','OpenPanel is een onbereikbare oude Backstage-tak: activePanel wordt nergens op open gezet; de actuele Openen-knop voert openAny rechtstreeks uit en gebruikt de aparte recente-snelkeuzelijst zonder deze iconen.')
exclude('a5f8dca851f36a61','De oude FeedbackDialog blijft dicht: feedbackOpen start false, nergens setFeedbackOpen(true); de titelbalk opent inmiddels GitHub-issues extern. Deze afbeeldingsbijlageknop wordt niet bereikt.')
exclude('feb0f778a33d180e','Grote grafiekillustratie bij geen geopende sondering; geen grafiekweergaveknop.')
exclude('774f3cc8d2052828 d7532c9c6121671e ab05b35f72a6c198 67ce3fe5bb88c003','Geografische CPT/boringmarkeringen met locatie, toestand en label in Leaflet; modelsymbolen, geen vaste UI-bedieningsiconen.')
exclude('7b69d66dd2df9fc0 ddca9cdaf7e0a68d 897f547ce7a765c2 3c8e186ff964f81a afdd0553b60c122a d6ebbb7fe69dafbb 1ae3a6dadfd01aa8 6608175a43a44884','Sondering-/boringmarkeringen en kleefmetingvarianten in geplaatste tekenelementen/BRO-laag; modelinhoud met eigen schaal en conventie, geen plaatsingsknop.')
exclude('a1bcaf8ba3ccb58b','Het weergegeven eigen/OpenAEC-beeldmerk is titelblokinhoud. De omringende knop kiest een logobestand; het beeldmerk blijft branding buiten de UI-icoonfamilie.')
exclude('60ace08122d98a1d','Noordpijl als 120×180 tekeningelement met N, achtergrond en mm-schaal; onderdeel van het papier, geen UI-noord- of cameraknop.')
exclude('7c794c5017f2a68c','De Voorbeeldproject-knop wordt alleen met onLoadExample gerenderd; App geeft die prop niet door aan StartSidebar.')
exclude('2f9f64aa35198914 3679c283769b68c9','Recente-itemknoppen in StartSidebar/Welcome roepen de door App gebonden console.log op en sluiten de overlay; er wordt geen bestand geladen. Werkelijke recente-bestandskeuze staat in Backstage zonder deze iconen.')
exclude('61e03ad53bd4bd37 bcff54834351241a 95976b2d62c8dcf6 d13aff62e59f7b2c 4393727c46dd682a 2c57a7cfe75a5a8d','Tegelbare klei-/zand-/silt-/veen-/grind-/humuspatronen voor boorprofielinhoud, met materiaalkleur en schaal; geen vaste bedieningsiconen.')


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='map.export-image':
        c.line([(2,6),(8,3),(14,6),(19,3),(19,12)],radius=.4)
        c.line([(2,6),(2,21),(8,18),(12,20)],radius=.4)
        c.line([(8,3),(8,18)],radius=0)
        c.line([(14,6),(14,11)],radius=0)
        dimension_arrow(c,(16,21),(22,15),2.5)
        c.line([(17,15),(22,15),(22,20)],True,radius=.3)
    elif key=='report.open-viewer':
        page(c,2,3,10,18)
        c.line([(5,8),(9,8)],radius=0)
        if not small:c.line([(5,12),(9,12)],radius=0)
        c.line([(17,17),(23,11)],True,radius=0)
        c.line([(17,11),(23,11),(23,17)],True,radius=.5)
    elif key=='geo.quote-request':
        box(c,2,11,20,11)
        c.line([(2,12),(12,18),(22,12)],radius=.5)
        c.line([(4,4),(20,4)],True,radius=0)
        c.line([(17,1),(20,4),(17,7)],True,radius=.3)
    elif key=='drawing.frame-import':
        box(c,2,3,11,18)
        c.line([(2,16),(13,16)],radius=0)
        c.line([(8,16),(8,21)],radius=0)
        dimension_arrow(c,(20,4),(20,17),2.3)
    elif key=='transform.corner-join':
        c.line([(4,21),(4,4),(21,4)],radius=.5)
        c.line([(4,12),(4,4),(12,4)],True,radius=.5)
    return True
