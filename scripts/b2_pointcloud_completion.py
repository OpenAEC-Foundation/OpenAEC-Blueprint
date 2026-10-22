"""Pointcloud semantics traced through Rust messages and classic React callbacks.

Asset-index and client scan duplicates are paired explicitly by record ID.
Unused match arms and misidentified include sites remain explicit exclusions.
"""
import math
from b2_second_series import box
from b2_bim_completion import cube
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS={71:'Punten en verwerking',72:'Doorsneden en meshes',73:'Meshmethoden',
        74:'Model- en tekeningenbrowser',75:'Opgeslagen weergaven',76:'Camerarichtingen',77:'Puntkleuren en gebouwen'}
ROWS=[
(71,'selection.box','Rechthoekselectie','ToggleBoxSelect of setEditMode activeert het slepen van een rechthoekig selectiekader.','afef7195f7486240'),
(71,'process.cancel','Verwerking annuleren','Een lopende schaal- of reconstructietaak om annulering vragen; geen resultaat verwijderen.','9ebdb566d5fc7c57'),
(71,'pointcloud.thin','Punten uitdunnen','Thin en handleThin behouden het gekozen percentage punten; geen weergavefilter.','c12d0425b9adbb84'),
(71,'pointcloud.index-build','Puntenindex bouwen','BuildIndex vraagt een octree-index voor de actieve puntenwolk; geen revisiewolk tekenen.','c02fe1b3618264aa'),
(72,'section.box','Doorsnedebox','SetSectionEnabled schakelt de begrenzende 3D-box; dezelfde vorm duidt een opgeslagen box aan.','6af26897d56fd216'),
(72,'section.fit-selection','Doorsnedebox om selectie','FitSectionToSelection past de boxgrenzen aan de geselecteerde punten aan; geen camera-fit.','9265e41e28f7a97a'),
(72,'section.reset-box','Doorsnedebox herstellen','ResetSectionBox herstelt de boxgrenzen; laat de camerarichting ongemoeid.','c69f9d1e645f0d5a'),
(72,'pointcloud.lod-refresh','Detailpunten vernieuwen','RefreshLod wist de detailcache en vraagt LoadDetail voor de huidige weergave.','de77dbd47144940c'),
(72,'pointcloud.section-drawing','2D-doorsnede','DrawingAction Toggle toont het paneel voor een 2D-doorsnedetekening.','b3b35e5fa5e5e33c'),
(72,'pointcloud.to-drawing','Puntenwolk naar tekening','WizardAction Open opent de wizard voor projectie naar tekeningen; nog niet uitvoeren.','de5f2f568326abf4'),
(73,'mesh.wizard','Meshwizard openen','MeshWizardAction Open toont de methodekiezer; start nog geen reconstructie.','1f25076b66d392c3'),
(73,'mesh.closed','Gesloten mesh kiezen','OpenMethod Closed kiest de gesloten-meshroute binnen de wizard.','a0c0260755ce2fda'),
(73,'mesh.terrain','Terreinmesh kiezen','OpenMethod Terrain kiest de terreinmeshroute binnen de wizard.','1ae839fe79d98c49'),
(73,'mesh.surface','3D-oppervlak kiezen','OpenMethod Surface kiest de 3D-oppervlakroute binnen de wizard.','85608b5276b467aa'),
(73,'mesh.faces','Vlakken detecteren kiezen','OpenMethod Faces kiest de vlakdetectieroute binnen de wizard.','3889be367a67e74e'),
(73,'mesh.reconstruct','Mesh reconstrueren','De klassieke handleReconstruct voert reconstructSurface uit op geladen punten.','b724bace116df6ad'),
(74,'pointcloud.scans','Scans in browser','Groeps- en rijindicator voor geopende scanbestanden; geen indexeeropdracht.','06b796a111700c2d'),
(74,'pointcloud.classes','Puntklassen in browser','Indicator bij ASPRS-klassen en hun zichtbaarheidskeuze; geen klassekleurenmodus.','9d5c99f373918d01'),
(74,'drawing.plan','Plattegrondblad','Een opgeslagen 2D-plattegrond aanduiden en tonen; geen tijdsplanning.','58f36a32ca9f8eed'),
(74,'drawing.elevation','Aanzichtblad','Een opgeslagen 2D-aanzicht aanduiden en tonen.','21e66dcde11fd3a9'),
(74,'drawing.section','Doorsnedeblad','Een opgeslagen 2D-doorsnede aanduiden en tonen; geen doorsnede genereren.','2c78ba9189baa92a'),
(74,'drawing.file','Geimporteerd tekenblad','Een reeds ingelezen tekenbestand in de browser kiezen en tonen.','e745a3d456a60aa2'),
(74,'drawing.sheet-new','Nieuw tekenblad voorbereiden','SheetAction Open opent de keuze voor een nieuw plan, aanzicht of doorsnede.','a8df314a252274b7'),
(75,'view.saved-list','Opgeslagen weergaven','Groepsindicator bij model, bewaarde cameraweergaven en 2D-tekeningen.','5da4fd680a3a2606'),
(75,'view.saved','Opgeslagen weergave herstellen','ViewAction Restore haalt de bewaarde camera- en doorsnedetoestand terug.','eefb78404e38a3df'),
(75,'view.update-saved','Weergave overschrijven','ViewAction Update vervangt een bestaande bewaarde weergave door de huidige toestand.','30589813d4a4057e'),
(76,'view.top','Bovenaanzicht','CameraPreset Top kiest yaw -pi/2, pitch pi/2.','be15545e5612ac58'),
(76,'view.bottom','Onderaanzicht','CameraPreset Bottom kiest yaw -pi/2, pitch -pi/2.','038a8c5d41032054'),
(76,'view.front','Vooraanzicht','CameraPreset Front kiest yaw -pi/2, pitch 0.','cac04e68f0760d3b'),
(76,'view.back','Achteraanzicht','CameraPreset Back kiest yaw pi/2, pitch 0.','5525491b8521c17a'),
(76,'view.right','Rechteraanzicht','CameraPreset Right kiest yaw 0, pitch 0.','537ad28ce24ef6ad'),
(76,'view.left','Linkeraanzicht','CameraPreset Left kiest yaw pi, pitch 0.','7ab7f2cba4b046ee'),
(76,'view.isometric','Isometrisch beeld','CameraPreset Isometric kiest de diagonale modelweergave.','1e940412b47d248d'),
(77,'pointcloud.color-elevation','Kleur naar hoogte','setPointcloudColorMode elevation kleurt punten naar hun hoogte.','4e8e9587332eaa45'),
(77,'pointcloud.color-class','Kleur naar puntklasse','setPointcloudColorMode classification kleurt punten naar ASPRS-klasse.','493f5b697c76efa5'),
(77,'pointcloud.color-intensity','Kleur naar intensiteit','setPointcloudColorMode intensity kleurt punten naar reflectie-intensiteit.','8389f4ae9e7f8370'),
(77,'geo.bag-buildings','3D-BAG-gebouwen','Het 3D-BAG-paneel tonen voor een gebieds- en LoD-keuze; nog niets ophalen.','a232cb9fd442dc20'),
(77,'geo.fetch-buildings','Gebouwen ophalen','handleDownload haalt het gekozen gebied op, leest CityJSON en voegt gebouwen toe.','d0938cf7b0f01167'),
]
EXAMPLE_OVERRIDES={'object.show':'a2e98429959e27de','object.hide':'39b39516536df9f2'}
EXAMPLE_EVIDENCE={k:'PointcloudPanel toont het oude oog als toestand; de gelezen tooltip en !pc.visible-callback bepalen de tegengestelde actie. Bronvoorbeeld gekozen op de actie, bestaande B2-geometrie behouden.' for k in EXAMPLE_OVERRIDES}
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De bepaling, richting of wijzigingsmarkering blijft zichtbaar voor de modelcontour.' for k in KEYS if k.startswith(('view.','pointcloud.','section.','geo.','drawing.'))}
REUSED={}
EXCLUDED={}
DISPATCHERS={}
DISPATCH_EVIDENCE={}


def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)


def dispatch(ids,targets,reason):
    for rid in ids.split():DISPATCHERS[rid]=targets;DISPATCH_EVIDENCE[rid]=reason


def exclude(ids,reason):
    for rid in ids.split():EXCLUDED[rid]=reason


reuse('7d35fa94977e929d 09a9426b3d1d9a9b','draw.dimension','Drawing Notes Tool Dimension plaatst een blijvende maatannotatie; maatgereedschap en bronrenderer gelezen.')
reuse('6c4458b16f94ae37 60e7a1561c9714d3','draw.leader','Drawing Notes Tool Leader plaatst een verwijzend bijschrift.')
reuse('39b00d128cc5e22e e40b88e9814d10ae','draw.line','ViewAction Tool Line en NoteKind Line tekenen een rechte annotatielijn.')
reuse('09057d59a25aa997 d7a97cd43b8008dd','draw.note','ViewAction Tool Note activeert het plaatsen van een weergavenotitie.')
reuse('1cdb3b8a1f6e01d5 9b1126a6e32aad25','draw.text','NoteKind Text activeert vrije tekst op de tekening.')
reuse('aa47fcde1a6bc4a6 59b55e1fece65f68','bcf.workspace','BCF-browsergroep met de beschikbare weergaven en exportbediening; geen directe export.')
reuse('9c1ee25b2a710233 9a37d46427c580bc','edit.duplicate','BrowserAction Duplicate maakt een kopie van modelweergave, bewaarde weergave of tekening; layouts gebruiken eveneens Duplicate.')
reuse('113c4e38f88545b7 ed9e222833b0dae0','object.rename','StartRename bewerkt de naam van een bewaarde weergave; hetzelfde naamwijzigingscontract als een plan.')
reuse('3ce485d82029775c 2b55506f11c5eb07','tree.expand','Ingeklapte browser- of fotogroep uitvouwen.')
reuse('0c331ee9d985ee40 82adaf468a3bd75a','tree.collapse','Uitgeklapte browser- of fotogroep invouwen.')
reuse('4a76027920d47092 073a606bfb7ea67d','edit.delete','DeleteSelection verwijdert geselecteerde punten uit de actieve bewerking; geen selectie alleen opheffen.')
reuse('99b1e2199ca2f0c7 45fe229eca086e05','measure.area','MeasureAction Toggle Area activeert oppervlakte meten.')
reuse('2f30aed14c812fa0 dad90c9e5f3f95e1','measure.distance','MeasureAction Toggle Distance activeert afstand meten.')
reuse('26ed31322de86812 8f40b540a6cacd85 68537317940cb06f','transform.move','ApplyTranslation en handleTranslate verplaatsen de actieve puntenwolk volgens X/Y/Z.')
reuse('800ade59367efead 382fba2b86d60598 0abd96612176e56d','transform.scale','ApplyScale en handleScale schalen de actieve puntenwolk rond zijn centrum.')
reuse('841821c9c20a03cb b8315d78d65e5391','view.pan','TogglePanTool activeert cameraverschuiving; geen punten verplaatsen.')
reuse('459ddd9e3d9180f3 8adff6ce2e50f5e7','edit.redo','RedoDelete voert de ongedaan gemaakte puntverwijdering opnieuw uit.')
reuse('e760695f90889789 fb559b0ef1be7117','edit.undo','UndoDelete herstelt een eerdere puntverwijdering.')
reuse('3a0bb830132ab9ac 396c1b4ad7849199','view.zoom-in','Message Zoom met positief zoomcommando vergroot het beeld rond het midden.')
reuse('9d147d098ddbf048 eb2cfda38a81f0da','view.zoom-out','Message Zoom met negatief zoomcommando verkleint het beeld rond het midden.')
reuse('b58755bfc2dc582d aa14a1ce22f7f15b','file.export','ExportSelection schrijft alleen de geselecteerde punten; selectie-scope in het label.')
reuse('afef7195f7486240 8c80e933267222f6 d567b971a4f9fad7 78e99f50db39e01d 8f7c5361032a27bc','selection.box','ToggleBoxSelect en de klassieke setEditMode schakelen rechthoekselectie.')
reuse('499820fc04a43e35 4d4b7e9349e4010b','edit.select','De grote Select-knop gebruikt TogglePickSelect: individuele punten aanklikken. Het paneelsymbool duidt dezelfde selectiegroep aan.')
reuse('2c86dc38b5598f11 37e2afa2b00975a3 9a6bce3060aa3e1e','view.fit','De klassieke zoomToFit kadert alle geometrie in het beeld.')
reuse('21452259f5a54511 90f389ef1b790f6c','panel.right','De klassieke rechterzijbalk in- of uitvouwen.')
reuse('38d5495ccd11819e f04089b795c4269a','ui.settings','Instellingen openen, respectievelijk vaste aanduiding bij het enige tabblad met algemene voorkeuren.')
reuse('2bd263a096cb9aba ec135d98acae2602 6898821e79011e02','file.import','handleImport kiest of sleept LAS/LAZ-bestanden en voegt de gelezen puntenwolken toe.')
reuse('8ee3cce5b5870e59','file.export','handleExportOBJ schrijft het gereconstrueerde mesh als Wavefront OBJ.')
reuse('513d8e547541b4c9','selection.mark','Vinkje bij het momenteel geselecteerde thema, geen procesresultaat.')
reuse('1decc8013f512d5f 277279a36b788b36','ui.dropdown','Chevron opent de export- of themakeuzelijst; keuze bepaalt de concrete actie.')
reuse('0b7a0fa5bf6092ea','ui.close','Het 3D-BAG-paneel sluiten.')
reuse('2e5e9f78c758edf2','geo.bag-buildings','Kopaanduiding van hetzelfde BAG-gebiedspaneel.')
reuse('d51e7cf12ee6876e','edit.delete','removePointcloud verwijdert de gekozen puntenwolk uit de projectlijst.')
reuse('2eda3ccfe5b401e6 2c7b803f6c507d5e','window.minimize','Native Tauri-appWindow.minimize via de Windows- of Linux-titelbalk.')
reuse('28cfa4646c5cdbca 86927bb55988a609','window.restore','Herstelvariant van de native titelbalkknop, zichtbaar als isMaximized waar is.')
reuse('4797b8777d48c09c e10d98deb1c6bfc8','window.maximize','Maximaliseervariant van de native titelbalkknop, zichtbaar als isMaximized onwaar is.')
reuse('fd4f2652dffba594 f4803c126c31d358','window.close','De titelbalk roept appWindow.close aan; geen dialoog of tab sluiten.')
reuse('6e218fd51edf3c9f 7cc4071ea08a93ff','pointcloud.thin','Dezelfde percentage-uitdunning via Thin of handleThin, geen kleurfilter.')
reuse('969582748fe56b0b','mesh.closed','Dezelfde Closed-wizardroute; tweede bronregistratie.')
reuse('074f80244b55dce7','mesh.faces','Dezelfde Faces-wizardroute; tweede bronregistratie.')
reuse('8f070a0f12c7af80','mesh.wizard','Dezelfde MeshWizardAction Open; tweede bronregistratie.')
reuse('b6c93f1d7f367a28','mesh.surface','Dezelfde Surface-wizardroute; tweede bronregistratie.')
reuse('b4e0a621ec4e282a','mesh.terrain','Dezelfde Terrain-wizardroute; tweede bronregistratie.')
reuse('724546f8c0a6e761','pointcloud.to-drawing','Dezelfde WizardAction Open voor tekeningen; lost de eerdere planningsverwarring op.')
reuse('a403fad54b374e9a','pointcloud.section-drawing','Dezelfde DrawingAction Toggle; tweede bronregistratie.')
reuse('4a67bc473c0ce8de','pointcloud.scans','Dezelfde scanbrowsergroep en scanrijen.')
reuse('8dc0861c42d0fbc7','pointcloud.classes','Dezelfde ASPRS-klassegroep en klasseaanduiding.')
reuse('7a37155a512a6863','drawing.elevation','ViewKind Elevations en ShowDrawing van een aanzicht.')
reuse('c3a075b9253eab5f','drawing.section','ViewKind Sections en ShowDrawing van een doorsnede.')
reuse('d18b6ae6baf5890c','drawing.file','ViewKind Files en ShowSheet van een ingelezen tekenblad.')
reuse('e93c5aec2b2ca8b5','view.saved-list','Dezelfde VIEWS-groepsindicator.')
reuse('fe607ef3b3f84e2b','view.saved','Dezelfde Restore-guid en bewaarde-weergavetab.')
reuse('7b0685cc6e93e1d3','view.update-saved','Dezelfde Update-guid, uitgeschakeld zolang de weergave is vergrendeld.')
reuse('141341de4a8ca6b0','drawing.sheet-new','Dezelfde SheetAction Open; layouttab gebruikt de bladindicator.')
reuse('b8f4a212125b4f87','view.isometric','Dezelfde isometrische camerakeuze.')

dispatch('15fc035425a0a733 005de3091d66b6e9',('file.import','file.open'),'ToolIcon Open duidt zowel Message Open (puntenwolk toevoegen) als DrawingView OpenFile (bestaande tekening openen) aan; vervangen per concrete callback.')
dispatch('65086f4b8df54db7 912f9467f555b912',('file.import',),'OpenFolder kiest een scanmap en voegt de gevonden scanbestanden toe; bestandstype/scope in het label.')
reuse('5df1b1c107cf9f8e a51a9ec9e91ed851','file.export','De actieve Export-lintknop schrijft de puntenwolk. De ExportBcf-variant van ViewAction::icon is niet aangeroepen door een actieve icoonknop; de BCF-bediening is tekst.')
dispatch('c02fe1b3618264aa 7f072b512fb0ee49',('bim.workspace','pointcloud.index-build','process.cancel'),'Model-icoon opent het 3D-model in browser/tab; de Index-lintknop wisselt BuildIndex en CancelIndex. Geen automatische gelijkstelling op assetnaam.')
dispatch('acf2d93966f6c796 9265e41e28f7a97a',('view.fit-selection','section.fit-selection'),'FitSelection staat bij ZoomToSelection en FitSectionToSelection; de eerste kadert de camera, de tweede past alleen de box aan.')
dispatch('c69f9d1e645f0d5a de77dbd47144940c',('view.reset-camera','section.reset-box','pointcloud.lod-refresh'),'ToolIcon Fit staat bij ResetCamera, ResetSectionBox en RefreshLod in het actieve lint. De detailcache herladen is geen camera-fit.')
dispatch('6af26897d56fd216 b179d4524396f10f',('section.box',),'SetSectionEnabled toggelt de box; indicator bij bewaarde weergave betekent dat een box aanwezig is.')
dispatch('58f36a32ca9f8eed c1676146271bbfe6',('drawing.plan','drawing.sheet-new'),'PlanSheet is typeaanduiding bij plattegronden en opent op de browserband SheetAction Open; geen tijdsplanning.')
dispatch('be15545e5612ac58 038a8c5d41032054',('view.top','view.bottom'),'CameraPreset Top en Bottom delen het oude asset; yaw/pitch bepalen de tegenovergestelde richting.')
dispatch('cac04e68f0760d3b 5525491b8521c17a',('view.front','view.back'),'CameraPreset Front en Back delen het oude asset; de yaw verschilt pi.')
dispatch('537ad28ce24ef6ad 7ab7f2cba4b046ee',('view.right','view.left'),'CameraPreset Right en Left delen het oude asset; de yaw verschilt pi.')
dispatch('124a4b314b30448b cff3d89e4b96eaa6',('object.lock','object.unlock'),'Gesloten slot is de vergrendelde toestand van weergave/tekening; klikken roept Lock(target) aan en ontgrendelt. Toestand en tegenactie niet verwisselen.')
dispatch('696206417b062694 c04ee7db2856f3ea',('object.unlock','object.lock'),'Open slot is de onvergrendelde toestand; klikken op Lock(target) vergrendelt de weergave of tekening.')
dispatch('2014526e77276608 48110f0049cb2b1b',('process.cancel','edit.deselect'),'Clear wordt actief in transform_properties gebruikt voor CancelScale. Hetzelfde match-arm beschrijft ook selectie opheffen/annuleren; geen revisiewolk- of move-opdracht.')
dispatch('39b39516536df9f2 a2e98429959e27de',('object.show','object.hide'),'PointcloudPanel toont de huidige zichtbaarheid met Eye/EyeOff, terwijl de tooltip Hide/Show en de klik !pc.visible de tegengestelde actie uitvoeren. De toekomstige bediening moet expliciet kiezen tussen toestand en actie; de actiebronvoorbeelden zijn gecorrigeerd zonder geometriewijziging.')
exclude('93f8f36bf3308129 908077f1765ce3bc f896ca46a7f30de2 e3ad2adafbf9f1fe','Favicon of applicatiebeeldmerk, geen vast bedieningsicoon.')
exclude('5f57ceb397b2eb27 0749c48532114dac','Clientbronscan kent de assetnaam aan een verkeerde include-regel toe: de getoonde bronplaats bevat respectievelijk xclip_remove en pick_point; geen zelfstandige move/point-bronplaats.')
exclude('438f16d2a42a6b39 707138febbaa1f8d a866d15437f98cc5 23e27b6d554a24ff 0a638ab7bb0bb2d8 d11273aa99a60c8f 0d24876f9d48ba6e f946df51f86bee21 6d53b3096f79c0f1 ade06f166ac17adb 2dd5e68f990ed965 69c9d9e96849382b','Alleen icon_svg-matcharm en ongebruikte tool_icon/ViewAction::icon-route; alle echte aanroepen van icon_tool_button_when zijn Move, Scale, CancelScale en Thin. Scan van alle gemounte native modules toont voor deze ToolIcon-variant geen actieve icoonbediening. De functies kunnen elders als tekstbediening bestaan.')


def points(c,accent=False,sparse=False):
    coords=[(4,6),(10,4),(17,5),(6,12),(13,11),(20,12),(4,19),(11,18),(18,20)]
    for i,(x,y) in enumerate(coords):
        if sparse and i%2:continue
        c.circle(x,y,.8,accent and i%2==0,True)


def sheet(c):
    box(c,3,3,18,18)
    c.line([(3,7),(21,7)],radius=0)


def lattice(c,kind):
    if kind=='terrain':p=[(3,16),(8,8),(15,12),(21,6),(20,20),(10,20)]
    elif kind=='surface':p=[(3,16),(7,6),(16,4),(21,13),(16,21),(8,19)]
    else:p=[(3,7),(12,2),(21,7),(21,17),(12,22),(3,17)]
    c.line(p,closed=True,radius=.3)
    center=(12,16) if kind=='terrain' else (12,13)
    for vertex in p:c.line([vertex,center],True,radius=0)


def clip_frame(c):
    for points in ([(2,7),(2,2),(7,2)],[(17,2),(22,2),(22,7)],[(22,17),(22,22),(17,22)],[(7,22),(2,22),(2,17)]):c.line(points,radius=.4)


def mini_cube(c,k=.45,x=12,y=12,accent=False):
    start=len(c.paths);cube(c);scale=c.size/24
    for p in c.paths[start:]:
        p['points']=[(k*px+(x-12*k)*scale,k*py+(y-12*k)*scale) for px,py in p['points']]
        if accent:p['tone']='accent'


def refresh_badge(c,x=18,y=18,r=4):
    c.line([(x+r,y+r),(x+r,y-1),(x-r,y-1)],True,radius=1.4)
    c.line([(x-r+1.8,y-2.8),(x-r,y-1),(x-r+1.8,y+.8)],True,radius=0)


def inset_face(c,points,k=.5):
    x=sum(p[0] for p in points)/len(points);y=sum(p[1] for p in points)/len(points);s=c.size/24
    c.fills.append({'tone':'accent','rings':[[(s*(x+k*(px-x)),s*(y+k*(py-y))) for px,py in points]]})


def terrain_mesh(c):
    c.line([(2,20),(9,5),(14,13),(18,8),(22,20)],closed=True,radius=.35)
    c.line([(14,13),(16,20)],radius=0)
    scale=c.size/24
    c.fills.append({'tone':'accent','rings':[[(x*scale,y*scale) for x,y in ((6.5,17.5),(9,11),(12.5,17.5))]]})


def surface_patch(c):
    c.line([(2,8),(14,3),(22,16),(10,21)],closed=True,radius=.35)
    c.line([(8,5.5),(16,18.5)],radius=0)
    c.line([(6,14.5),(18,9.5)],radius=0)
    inset_face(c,[(8,5.5),(14,3),(18,9.5),(12,12)],.35)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='selection.box':
        for pts in ([(2,8),(2,2),(8,2)],[(16,2),(22,2),(22,8)],[(2,16),(2,22),(8,22)],[(16,22),(22,22),(22,16)]):c.line(pts,radius=.3)
        for x,y in ((8,8),(16,8),(8,16),(16,16)):c.circle(x,y,.9,True,True)
    elif key=='process.cancel':
        box(c,3,3,18,18)
        c.line([(8,8),(16,16)],True,radius=0);c.line([(8,16),(16,8)],True,radius=0)
    elif key=='pointcloud.thin':
        # A dense sample becomes a sparse sample; no deletion slash.
        for x in (3,6,9):
            for y in (5,12,19):c.circle(x,y,.7,False,True)
        for y in (6,18):c.circle(20,y,1,False,True)
        dimension_arrow(c,(12,12),(22,12),2)
    elif key=='pointcloud.index-build':
        box(c,3,3,18,18);c.line([(12,3),(12,21)],radius=0)
        c.line([(3,12),(21,12)],radius=0);c.line([(12,7),(21,7)],True,radius=0)
        c.line([(17,3),(17,12)],True,radius=0)
        for x,y in ((6,7),(7,17),(17,17)):c.circle(x,y,.7,False,True)
    elif key in {'section.box','section.fit-selection','section.reset-box'}:
        clip_frame(c)
        if key=='section.box':mini_cube(c,accent=True)
        elif key=='section.fit-selection':
            box(c,8,8,8,8,True)
        else:
            for p in c.paths:p['points']=[(.6*x,.6*y) for x,y in p['points']]
            refresh_badge(c)
    elif key=='pointcloud.lod-refresh':
        for x in (3,8,13):
            for y in (3,8):c.circle(x,y,.85,filled=True)
        refresh_badge(c,17,17,5)
    elif key in {'pointcloud.section-drawing','pointcloud.to-drawing'}:
        sheet(c)
        c.line([(6,17),(10,11),(14,15),(18,9)],radius=.3)
        if key=='pointcloud.section-drawing':c.line([(5,13),(19,13)],True,radius=0)
        else:
            scale=c.size/24
            for p in c.paths:p['points']=[(.65*x,.8*y+1.8*scale) for x,y in p['points']]
            dimension_arrow(c,(20,4),(20,20),2)
    elif key.startswith('mesh.'):
        kind=key.split('.')[1]
        if kind=='closed':
            c.line([(12,3),(22,20),(2,20)],closed=True,radius=.35)
            c.line([(12,9),(12,14),(7,17)],True,radius=.25)
            c.line([(12,14),(17,17)],True,radius=0)
        elif kind=='terrain':terrain_mesh(c)
        elif kind=='surface':surface_patch(c)
        elif kind=='faces':
            c.line([(2,7),(13,3),(20,7),(9,12)],closed=True,radius=.35)
            c.line([(13,16),(21,12),(21,20),(13,23)],True,closed=True,radius=.35)
        elif kind=='wizard':
            box(c,2,2,12,12);c.line([(2,14),(14,2)],radius=0)
            c.line([(15,22),(22,15)],True,radius=0)
            c.line([(19.5,17.5),(21,19)],True,radius=0)
            c.plus(20,7,2,True)
        else:
            surface_patch(c)
            for p in c.paths:p['points']=[(.55*x,.55*y) for x,y in p['points']]
            c.fills.pop()
            refresh_badge(c)
    elif key=='pointcloud.scans':
        box(c,4,3,12,8);c.circle(10,7,2)
        c.line([(12,11),(12,15)],radius=0)
        c.line([(7,22),(12,15),(17,22)],radius=.3)
        c.line([(19,5),(22,3)],True,radius=0)
        c.line([(19,9),(22,11)],True,radius=0)
    elif key=='pointcloud.classes':
        for x,y in ((5,5),(5,12),(5,19)):c.circle(x,y,1.5,True,True)
        for y,w in ((5,17),(12,21),(19,15)):c.line([(10,y),(w,y)],radius=0)
    elif key.startswith('drawing.'):
        kind=key.split('.')[1];sheet(c)
        if kind=='plan':
            c.line([(7,11),(17,11),(17,18),(7,18)],True,closed=True,radius=.3);c.line([(12,11),(12,18)],True,radius=0)
        elif kind=='elevation':
            c.line([(7,18),(7,13),(12,9),(17,13),(17,18)],True,radius=.3)
            c.line([(10,18),(10,15),(14,15),(14,18)],True,radius=.2)
        elif kind=='section':
            c.line([(7,11),(7,17),(17,17),(17,11)],radius=.3)
            c.line([(5,14),(19,14)],True,radius=0)
        elif kind=='file':c.line([(7,17),(10,11),(14,16),(18,11)],True,radius=.3)
        else:c.plus(12,14,3,True)
    elif key in {'view.saved-list','view.saved','view.update-saved'}:
        box(c,3,3,18,15)
        if key=='view.saved-list':
            c.line([(6,21),(18,21)],radius=0)
            for x in (7,12,17):c.circle(x,10,.8,True,True)
        elif key=='view.saved':
            c.line([(14,3),(14,12),(17,10),(20,12),(20,3)],True,radius=.2)
        else:
            for p in c.paths:p['points']=[(.6*x,.6*y) for x,y in p['points']]
            refresh_badge(c)
    elif key.startswith('view.'):
        name=key.split('.')[1]
        if name=='isometric':
            cube(c);del c.paths[-2:]
            c.line([(6.25,8.5),(12,12),(17.75,8.5)],True,radius=.3)
            c.line([(12,12),(12,18.5)],True,radius=0)
        else:
            centers={'top':(12,15),'bottom':(12,9),'front':(14,9),'back':(10,15),'right':(9,12),'left':(15,12)}
            mini_cube(c,.5,*centers[name])
            dirs={'top':((12,1.5),(12,6.5)),'bottom':((12,22.5),(12,17.5)),
                  'front':((2,22),(7.5,16.5)),'back':((22,2),(16.5,7.5)),
                  'right':((22.5,12),(17.5,12)),'left':((1.5,12),(6.5,12))}
            dimension_arrow(c,*dirs[name],1.6)
    elif key.startswith('pointcloud.color-'):
        kind=key.removeprefix('pointcloud.color-')
        if kind=='elevation':
            for x,y in ((4,19),(9,14),(14,9),(19,4)):c.line([(x,y),(x+2,y)],True,radius=0)
            c.line([(3,3),(3,21),(21,21)],radius=0)
        elif kind=='class':
            c.circle(6,6,2.5,True);box(c,15,3,6,6)
            c.line([(3,21),(6,14),(9,21)],True,closed=True,radius=.3);c.circle(18,18,3)
        else:
            for x,r in ((5,1),(12,2),(20,3)):c.circle(x,12,r,True,True)
            c.line([(3,21),(21,21)],radius=0)
    elif key.startswith('geo.'):
        c.line([(3,21),(3,8),(10,8),(10,3),(17,3),(17,12),(21,12),(21,21)],closed=True,radius=.3)
        if key=='geo.bag-buildings':
            for x,y in ((6,12),(6,17),(13,7),(13,12),(17,17)):c.circle(x,y,.6,True,True)
        else:
            scale=c.size/24
            for p in c.paths:p['points']=[(.65*x,.85*y+scale) for x,y in p['points']]
            dimension_arrow(c,(20,4),(20,21),2)
    return True
