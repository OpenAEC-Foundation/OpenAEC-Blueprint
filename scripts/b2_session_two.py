"""Second extended B2 review: original geometry, explicit pinned PDF actions."""
import math
from b2_second_series import box, extend as extend_base
from b2_energy_pile_audio import arc_points, pencil
from b2_bulk_series import page, arrow, curve, reset_ring

AVAILABLE_SERIES=(21,22,23,24,25,26,27,28)
GROUPS={21:'Technisch tekenen',22:'Vectorbewerkingen',23:'Selecties en verzamelingen',
        24:'Verdelen en objectgrootte',25:'Documentafwerking',26:'Vastleggen en uitvoer',
        27:'Weergave en panelen',28:'Lezen en inspecteren'}
# Series, canonical contract, label, precise action, inspected catalog record.
ROWS=[
 (21,'draw.spline-arrow','Gebogen pijl tekenen','Een spline met pijlpunt plaatsen; geen navigatiepijl.','3ecea67e2168a0b6'),
 (21,'draw.cloud','Revisiewolk tekenen','Het cloud-annotatiegereedschap activeren; geen cloudopslag.','0e079325c8531c75'),
 (21,'draw.l-shape','L-vorm tekenen','Een L-vormige geometrie plaatsen.','ecd8a2380ab0c57d'),
 (21,'draw.coordinate','Puntcoördinaat plaatsen','Via startSpotCoordTool een punt met X/Y-coördinaten annoteren.','943d3f299245deb8'),
 (21,'measure.radius','Straalmaat plaatsen','Een straalmaat plaatsen via het radius-gereedschap, van middelpunt naar rand.','16ea2c18ced5eb14'),
 (21,'measure.diameter','Diametermaat plaatsen','Een diametermaat plaatsen via het diameter-gereedschap, van rand naar rand.','881c668f471abfe8'),
 (21,'measure.count','Objecten tellen','Telmarkeringen plaatsen via setTool(count); de gedeelde bronvorm Circle bewijst geen cirkeltekengereedschap.','ffd773e7fa5151ce'),
 (21,'draw.vector-clip','Vectorknipsel maken','Een tekeninggebied als vectorknipsel selecteren; geen rasteropname of gewone klembordknip.','9360cc9d8602c11a'),
 (22,'transform.array','Objectreeks maken','Het array-gereedschap voor een herhaalde objectreeks activeren.','97c8acec90fe8d02'),
 (22,'transform.stretch','Geometrie uitrekken','Het stretch-gereedschap starten; geen uniforme schaalbewerking.','f76a719613a4a5da'),
 (22,'transform.explode','Geometrie ontleden','De samengestelde selectie via explodeSelection ontleden; apart van een verzameling opheffen.','867eafbaa8af231b'),
 (22,'transform.join','Geometrie samenvoegen','Geselecteerde geometrie via joinSelection verbinden; geen PDF-documenten samenvoegen.','4aa69754f65fce99'),
 (22,'transform.split','Geometrie splitsen','Het split-gereedschap voor geometrische segmenten activeren.','7736a0433b5d56bf'),
 (22,'transform.break','Geometrie onderbreken','Het break-gereedschap activeren voor een onderbreking; geen planningspauze.','07eeda23a38d13fb'),
 (22,'transform.scale','Objecten schalen','De selectie rond een basispunt vergroten of verkleinen via startEnlargeTool.','eb91da110aa5ba13'),
 (22,'edit.paste-in-place','Op dezelfde plaats plakken','Annotaties op hun oorspronkelijke coördinaten plakken via pasteAnnotationsInPlace.','fa75b006595b6a07'),
 (23,'object.collection-create','Verzameling maken','De selectie via createCollection als verzameling bewaren.','8b3d739f687ea651'),
 (23,'object.collection-explode','Verzameling opheffen','De verzameling via explodeCollection ontbinden; geen geometrische explode-opdracht.','736975b0c4960698'),
 (23,'edit.paste-vector-clip','Vectorknipsel plakken','Het vectorknipsel via plakKnipsel plaatsen met behoud van vectordata.','b93b0fe09fdd1cdb'),
 (23,'measure.scale-region','Schaalgebied tekenen','Een gebied met een eigen meetkalibratie tekenen via scaleRegion.','7c635882e9312293'),
 (23,'measure.scale-page','Schaalgebied over pagina','Een schaalgebied over de volledige pagina maken via createFullPageScaleRegion.','785e8b82ca2e2e4b'),
 (23,'edit.deselect','Selectie opheffen','De huidige annotatieselectie wissen; de objecten blijven bestaan.','c7452392df70c988'),
 (23,'annotate.clear-all','Alle annotaties wissen','Na bevestiging alle documentannotaties wissen; de PDF-pagina’s blijven bestaan.','713a0d876c5d5656'),
 (24,'object.distribute-left','Linkerranden verdelen','Geselecteerde objecten op gelijk verdeelde linkerranden plaatsen.','589d35904196effd'),
 (24,'object.distribute-center','Middens horizontaal verdelen','Objectmiddens op gelijke horizontale afstanden plaatsen; geen gelijke vrije tussenruimte.','63a205840fff9691'),
 (24,'object.distribute-right','Rechterranden verdelen','Geselecteerde objecten op gelijk verdeelde rechterranden plaatsen.','57f6df89b3f321c7'),
 (24,'object.distribute-top','Bovenranden verdelen','Geselecteerde objecten op gelijk verdeelde bovenranden plaatsen.','6c0afe04697196c9'),
 (24,'object.distribute-middle','Middens verticaal verdelen','Objectmiddens op gelijke verticale afstanden plaatsen.','a4e75d8e0d86d46e'),
 (24,'object.distribute-bottom','Onderranden verdelen','Geselecteerde objecten op gelijk verdeelde onderranden plaatsen.','7ed852d1ff6d2115'),
 (24,'object.same-size','Dezelfde grootte','De selectie dezelfde afmetingen geven via sameSize; het bronicoon hoort bij de groottegroep met daarnaast breedte/hoogte-opdrachten.','dc615ca7574697fe'),
 (24,'transform.flip-vertical','Verticaal spiegelen','De selectie verticaal spiegelen via flipVertical; geen camera- of paginarotatie.','5a67e282aa17b011'),
 (25,'document.watermark-add','Watermerk toevoegen','Het dialoog voor een documentwatermerk openen.','ac015e967207b80b'),
 (25,'document.watermarks','Watermerken beheren','Het beheer van bestaande documentwatermerken openen.','b8d5d291e48e76d0'),
 (25,'document.header-footer','Kop- en voettekst','Het dialoog voor kop- en voetteksten openen.','4a402f015615fe5b'),
 (25,'document.edit-text','Bestaande tekst bewerken','Het editText-gereedschap activeren; geen nieuwe tekst plaatsen.','1b1cfbeed8319b97'),
 (25,'document.ocr','Tekst herkennen met OCR','Het OCR-taaldialoog openen voor tekstherkenning.','68bca3af912abd78'),
 (25,'document.edit-scanned-text','Scantekst bewerken','Bestaande herkende woorden in een scan bewerkbaar maken via startScanTextTool; deze opdracht voert niet zelf OCR uit.','0e011c2ff421ed46'),
 (25,'document.compress','PDF comprimeren','Het compressiedialoog met de huidige documentgrootte openen.','c6e84fe5f41547f3'),
 (25,'page.reorder','Paginavolgorde wijzigen','Het miniaturenpaneel openen om pagina’s te verslepen; geen automatische sortering.','adff753b9493562c'),
 (26,'capture.page','Pagina vastleggen','De volledige huidige pagina vastleggen via screenshotFullPage.','e847748a1b52b5e2'),
 (26,'capture.region','Gebied vastleggen','Een rasteropnamegebied kiezen via startRegionScreenshot; geen vectorknipsel.','89ba1a6bb807afcf'),
 (26,'capture.overlay','Opname als overlay plaatsen','De vorige rasteropname via placeLastScreenshotAsOverlay plaatsen.','61a39e06b623745e'),
 (26,'export.cad','Naar CAD exporteren','Het CAD-exportdialoog openen; geen generieke bestandsdownload.','7c042a2567af363e'),
 (26,'export.raster-pdf','Raster-PDF exporteren','Alle pagina’s op 300 dpi als raster-PDF exporteren via exportAsRasterPdf.','da1a80514986e113'),
 (26,'export.ifc-report','IFC-report exporteren','Een .ifcreport JSON-container met PDF en IFC-geclassificeerde annotaties exporteren; geen regulier IFC-modelbestand.','59946f9d650c3d43'),
 (26,'document.email','PDF per e-mail voorbereiden','emailCurrentPdf aanroepen voor het actieve document; het icoon is geen bewijs dat een bericht al is verzonden.','49db8c61e75a252f'),
 (27,'view.actual-size','Werkelijke grootte','De documentweergave op werkelijke grootte zetten via actualSize.','e016247b2cc5a986'),
 (27,'view.rotate-left','Weergave linksom draaien','Alleen de weergave 90 graden linksom draaien via draaiWeergave; het document blijft ongewijzigd.','400ba6fdf5d8f79d'),
 (27,'view.rotate-right','Weergave rechtsom draaien','Alleen de weergave 90 graden rechtsom draaien; geen paginabewerking.','65ca05a817f56754'),
 (27,'object.properties','Objecteigenschappen openen','De eigenschappen van de selectie openen via showProperties/showMultiSelectionProperties.','b597f3c292344232'),
 (27,'panel.annotations','Annotatielijst','Het annotatielijstpaneel omschakelen.','1e1d51e7821b2372'),
 (27,'panel.element-visibility','Elementzichtbaarheid','Het paneel voor tonen/verbergen/dimmen van annotatiesoorten openen.','3fc25b23a458fa87'),
 (27,'panel.symbol-library','Symboolbibliotheek','De symboolbibliotheek/Toolpalette omschakelen; de plaatsbare symbolen zelf zijn geen vaste UI-iconen.','d5787dfb35a63447'),
 (28,'view.thin-lines','Dunne lijnen tonen','De thinLines-weergavevoorkeur schakelen en de pagina opnieuw tekenen; geen objectlijndikte wijzigen.','8e4edf1a8e45898c'),
 (28,'view.remember-reading','Leespositie onthouden','Leespositie, scroll en zoom per document bewaren/herstellen via setReaderTracking; geen afleidingsvrije leesweergave.','e9225d7ecd162f46'),
 (28,'document.compare','PDF’s vergelijken','Het documentvergelijkingsdialoog openen of de actieve vergelijking afsluiten.','4a8b3d89c1b9330f'),
 (28,'view.show-keystrokes','Toetsaanslagen tonen','De toetsaanslagen-overlay omschakelen; geen sneltoetsenoverzicht openen.','a5df12145ac6cff8'),
 (28,'measure.takeoff','Hoeveelhedenpaneel','Het meet-/hoeveelhedenpaneel omschakelen via toggleSchedule.','ecae040fbe0b11b6'),
 (28,'symbol.parametric-picker','Parametrisch symbool kiezen','De template-/parameterkiezer voor een nieuwe parametrische annotatie openen.','e7fe0752e9f32542'),
 (28,'object.reset-location','Objectpositie herstellen','Selectierotatie op nul zetten en objecten naar het paginamidden verplaatsen; geen ongedaan maken.','36dc2e8e3a5a888e'),
 (28,'ui.whats-new','Wat is er nieuw','Het venster met nieuwe functies openen via openWhatsNewManual; geen Over-venster.','10ff88c329f230cc'),
]
ACTIVE_ROWS=[r for r in ROWS if r[0] in AVAILABLE_SERIES]
DEFINITIONS=[(key,label,GROUPS[batch],meaning) for batch,key,label,meaning,_ in ACTIVE_ROWS]
EXAMPLES={key:record for _,key,_,_,record in ACTIVE_ROWS}
SERIES={key:batch for batch,key,_,_,_ in ACTIVE_ROWS}
KEYS=set(SERIES)
SOURCE_FUNCTIONS={'draw.spline-arrow': 'review.gebogenpijldubbelklikomtevoltooien', 'draw.cloud': 'review.wolk', 'draw.l-shape': 'review.lvorm', 'draw.coordinate': 'review.cordinaat', 'measure.radius': 'review.straal', 'measure.diameter': 'review.diameter', 'measure.count': 'draw.circle', 'draw.vector-clip': 'review.vectorknipsel', 'transform.array': 'review.reeks', 'transform.stretch': 'review.uitrekken', 'transform.explode': 'review.ontleden', 'transform.join': 'review.samenvoegen', 'transform.split': 'review.splitsen', 'transform.break': 'review.breken', 'transform.scale': 'review.vergroten', 'edit.paste-in-place': 'review.plakkenopplaats', 'object.collection-create': 'review.aanmaken', 'object.collection-explode': 'review.ontleden', 'edit.paste-vector-clip': 'review.plakknipsel', 'measure.scale-region': 'review.schaalgebied', 'measure.scale-page': 'review.schaalgebiedoppagina', 'edit.deselect': 'review.deselecteren', 'annotate.clear-all': 'edit.clear-all', 'object.distribute-left': 'review.linksverdelen', 'object.distribute-center': 'review.middenverdelen', 'object.distribute-right': 'review.rechtsverdelen', 'object.distribute-top': 'review.bovenverdelen', 'object.distribute-middle': 'review.middenverdelen', 'object.distribute-bottom': 'review.onderverdelen', 'object.same-size': 'review.samesize16', 'transform.flip-vertical': 'review.flipv', 'document.watermark-add': 'review.watermerktoevoegen', 'document.watermarks': 'review.watermerkenbeheren', 'document.header-footer': 'review.koptekstvoetteksttoevoegen', 'document.edit-text': 'review.tekstbewerken', 'document.ocr': 'review.tekstherkennenocr', 'document.edit-scanned-text': 'review.tekstherkennen', 'document.compress': 'review.pdfcomprimeren', 'page.reorder': 'review.paginasherschikken', 'capture.page': 'review.helepaginavastleggen', 'capture.region': 'review.gebiedvastleggen', 'capture.overlay': 'review.vorigeopnamealsoverlayplaatsen', 'export.cad': 'review.naarcadexporteren', 'export.raster-pdf': 'review.rasterpdfexporteren', 'export.ifc-report': 'review.ifcreportexporteren', 'document.email': 'review.pdfperemail', 'view.actual-size': 'review.werkelijkegroottectrl0', 'view.rotate-left': 'review.draaitdeweergave90linksomhetdocumentzelfverandertniet', 'view.rotate-right': 'review.draaitdeweergave90rechtsomhetdocumentzelfverandertniet', 'object.properties': 'review.openproperties', 'panel.annotations': 'review.annotatielijstf11', 'panel.element-visibility': 'review.zichtbaarheidelemententoonverbergendimannotatiesoorten', 'panel.symbol-library': 'review.toolpalette', 'view.thin-lines': 'review.dunnelijnen', 'view.remember-reading': 'review.leesmodus', 'document.compare': 'review.pdfsvergelijken', 'view.show-keystrokes': 'review.toetsaanslagentonen', 'measure.takeoff': 'review.hoeveelheden', 'symbol.parametric-picker': 'review.parametrischsymbool', 'object.reset-location': 'review.resetlocation', 'ui.whats-new': 'review.about'}
ALL_REUSED={'b89544d4ed52a503': ('draw.textbox', 'Label activeert hetzelfde textbox-gereedschap.'), 'a627ac6d73c02297': ('capture.page', 'De hoofdknop en de menukeuze roepen beide screenshotFullPage aan.'), '58e2e0906a68834b': ('panel.left', 'Navigatiepaneel roept toggleLeftPanel aan; bestaande zijpaneelbediening.'), '737be5f4c8d2e640': ('page.view-single', 'De lintknop roept setViewMode(single) aan.'), 'b1427133416e2d07': ('page.view-continuous', 'De concrete bronknop is actief en roept setViewMode(continuous) aan; het inventarislabel Binnenkort is verouderd.'), 'b281d8d67fdf729e': ('page.view-book', 'setViewMode(book) activeert dezelfde boekweergave als de statusbalk.'), '66cc73069b6606ab': ('page.view-facing', 'setViewMode(facing) activeert dezelfde spreadweergave als de statusbalk.'), '674340c12806396e': ('view.zoom-in', 'De lintknop roept zoomIn aan.'), 'ae02fec74493b5d8': ('view.zoom-out', 'De lintknop roept zoomOut aan.'), 'f1ad8e241c239f19': ('ui.settings', 'De lintknop opent showPreferencesDialog.'), '246fc0f34af9f349': ('edit.copy', 'De klembordknop roept copySelected aan.'), '326df1d22879ad6d': ('edit.duplicate', 'De andere Copy-knop roept duplicateAnnotation aan; kopiëren en dupliceren blijven verschillende contracten.'), '14ebc93c85e0057b': ('edit.cut', 'De klembordknop roept cutSelected aan.'), 'd21b039436fa7eeb': ('edit.delete', 'De klembordknop roept deleteSelected aan.'), 'e9b1febf179a0e3e': ('edit.paste', 'De knop roept pasteFromClipboard aan.'), '383008844b589079': ('draw.rectangle', 'De knop activeert het box-gereedschap.'), 'f4db354f6f26831d': ('draw.circle', 'Deze Circle-knop activeert daadwerkelijk circle; de Count-knop met hetzelfde icoon blijft apart.'), 'e434f32c98338bf2': ('edit.select', 'Ondanks de variabelenaam selectTextIcon activeert deze knop objectselectie met armedMarquee.'), 'bdba7ce20891d778': ('document.compare', 'De Beeld-knop opent hetzelfde compare-dialoog of sluit dezelfde vergelijking af.'), 'd5cb6058d9975216': ('measure.angle', 'De knop activeert hetzelfde measureAngle-gereedschap.'), '5557c95e7ad72c05': ('measure.perimeter', 'De broncluster noemt afstand, maar deze knop activeert measurePerimeter; expliciet aan omtrek gekoppeld.'), '0a52b9af343d80fd': ('draw.textbox', 'De knop activeert textbox.'), '979608069d91d01f': ('draw.note', 'De knop activeert comment.'), '706dfcdb907c7736': ('draw.leader', 'De knop activeert callout.'), '8b96aff6b2db7865': ('measure.distance', 'CommentTab activeert measureDistance.'), 'df8ec0d0d9766d3f': ('measure.distance', 'DrawingTab activeert measureDistance.'), 'c4b4846bd5f64bb2': ('measure.distance', 'De knop Maatlijn activeert hier measureDistance, niet een ander blijvend maatlijngereedschap.'), '1f9de18fb39c9679': ('measure.area', 'DrawingTab activeert measureArea.')}
ALL_KEYS={r[1] for r in ROWS}
REUSED={r:v for r,v in ALL_REUSED.items() if v[0] not in ALL_KEYS or v[0] in KEYS}


def brackets(c,x=3,y=3,w=18,h=18,accent=False):
    d=3
    for sx,sy,dx,dy in [(x,y,1,1),(x+w,y,-1,1),(x+w,y+h,-1,-1),(x,y+h,1,-1)]:
        c.line([(sx+dx*d,sy),(sx,sy),(sx,sy+dy*d)],accent,radius=.4)


def text_t(c,x=7,y=7,w=10,h=10,accent=False):
    c.line([(x,y),(x+w,y)],accent)
    c.line([(x+w/2,y),(x+w/2,y+h)],accent)


def dashed_box(c,x,y,w,h,accent=False):
    for points in [[(x,y+3),(x,y),(x+3,y)],[(x+w-3,y),(x+w,y),(x+w,y+3)],
                   [(x+w,y+h-3),(x+w,y+h),(x+w-3,y+h)],[(x+3,y+h),(x,y+h),(x,y+h-3)]]:
        c.line(points,accent,radius=.35)


def eraser(c):
    c.line([(11,16),(17,10),(22,15),(16,21),(15,21)],True,True,radius=.5)
    c.line([(14,13),(19,18)],True,radius=0)
    c.line([(17,22),(22,22)],True)
    c.clear_primary=True


def slider(c,x,ys,top=4,bottom=20):
    begin=top
    for y in ys:
        if y-2.5>begin:c.line([(x,begin),(x,y-2.5)],True)
        c.circle(x,y,1.4,True)
        begin=y+2.5
    if bottom>begin:c.line([(x,begin),(x,bottom)],True)


def drop(c,x=12,y=12.5,r=3.5,accent=True):
    # Mirrored cubic sides, rounded bowl, and one clear upper tip.
    scale=r/3.5
    segments=[[(0,-5),(-1.5,-2.8),(-3.5,-.5),(-3.5,1.2)],
              [(-3.5,1.2),(-3.5,3),(-1.8,4),(0,4)],
              [(0,4),(1.8,4),(3.5,3),(3.5,1.2)],
              [(3.5,1.2),(3.5,-.5),(1.5,-2.8),(0,-5)]]
    for points in segments:curve(c,[(x+px*scale,y+py*scale) for px,py in points],accent)


def cloud(c):
    # Eight regular outward scallops form a revision contour.
    points=[]
    for i in range(8):
        a=i*math.tau/8;b=(i+1)*math.tau/8;m=(a+b)/2
        start=(12+7.5*math.cos(a),12+6.5*math.sin(a))
        end=(12+7.5*math.cos(b),12+6.5*math.sin(b))
        control=(12+11*math.cos(m),12+10*math.sin(m))
        for j in range(24):
            t=j/24;u=1-t
            points.append((u*u*start[0]+2*u*t*control[0]+t*t*end[0],
                           u*u*start[1]+2*u*t*control[1]+t*t*end[1]))
    c.line(points,closed=True,radius=0)


def vector_fragment(c,x=7,y=8,scale=1):
    # A Bezier segment with square anchor nodes, shared by both clip tools.
    points=[(x,y+7*scale),(x,y-2*scale),
            (x+9*scale,y-2*scale),(x+9*scale,y+7*scale)]
    curve(c,points,True)
    for px,py in (points[0],points[-1]):
        fill_rect(c,px-1.1*scale,py-1.1*scale,2.2*scale,2.2*scale,True)


def dimension_arrow(c,a,b,head=2):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    ux,uy=dx/length,dy/length
    c.line([a,b],True,radius=0)
    c.line([(b[0]-head*ux-head*uy,b[1]-head*uy+head*ux),b,
            (b[0]-head*ux+head*uy,b[1]-head*uy-head*ux)],True,radius=0)


def fill_rect(c,x,y,w,h,accent=False):
    scale=c.size/24
    c.fills.append({'tone':'accent' if accent else 'primary',
                    'rings':[[(a*scale,b*scale) for a,b in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]]]})


def ruler(c,x=3,y=16,w=18,h=5):
    box(c,x,y,w,h)
    for px in (x+4,x+8,x+12):
        if px<x+w-1:c.line([(px,y),(px,y+2)],True)


def detail_line(c,points):
    # The tiny report cube needs a lighter optical weight inside the page.
    # Export it as ordinary filled contours, without SVG strokes.
    from shapely.geometry import LineString
    scale=c.size/24
    shape=LineString([(x*scale,y*scale) for x,y in points]).buffer((.75 if c.size==16 else 1)/2,quad_segs=12,cap_style='round',join_style='round')
    polygons=list(shape.geoms) if hasattr(shape,'geoms') else [shape]
    for polygon in polygons:
        c.fills.append({'tone':'primary','rings':[list(polygon.exterior.coords)]+[list(r.coords) for r in polygon.interiors]})


def camera(c,small=False):
    c.line([(3,9),(7,9),(9,5),(15,5),(17,9),(21,9),(21,20),(3,20)],closed=True,radius=1.2)
    c.circle(12,14.5,2.75,True)


def extend(c,key):
    if key not in KEYS:return False
    if key=='draw.spline-arrow':
        curve(c,[(3,18),(3,3),(13,21),(19,7)])
        dx,dy=6/math.sqrt(232),-14/math.sqrt(232)
        tip=(19+2*dx,7+2*dy);base=(tip[0]-2.8*dx,tip[1]-2.8*dy)
        c.line([(19,7),tip],True)
        c.line([(base[0]-2.2*dy,base[1]+2.2*dx),tip,(base[0]+2.2*dy,base[1]-2.2*dx)],True,radius=.35)
    elif key=='draw.cloud':cloud(c)
    elif key=='draw.l-shape':
        c.line([(11,3),(4,3),(4,21),(21,21),(21,14)],radius=.5)
        c.line([(11,3),(11,14),(21,14)],True,radius=.5)
        c.clear_primary=True
    elif key=='draw.coordinate':
        c.line([(3,17),(11,17)],True,radius=0)
        c.line([(7,13),(7,21)],True,radius=0)
        c.line([(9.5,14.5),(13,11)],radius=0)
        box(c,11,3,10,7)
        c.line([(14,6.5),(18,6.5)],radius=0)
    elif key in {'measure.radius','measure.diameter'}:
        c.circle(12,12,8)
        a=(12,12) if key=='measure.radius' else (6.343,17.657)
        b=(17.657,6.343)
        dimension_arrow(c,a,b,1.65)
        if key=='measure.radius':c.circle(12,12,.8,True,True)
        else:
            dimension_arrow(c,b,a,1.65)
        c.clear_primary=True
    elif key=='measure.count':
        # Number sign: two clean slanted uprights and two foreground crossbars.
        c.line([(10,3),(6,21)],radius=0)
        c.line([(18,3),(14,21)],radius=0)
        c.line([(4,9),(21,9)],True,radius=0)
        c.line([(3,15),(20,15)],True,radius=0)
    elif key=='draw.vector-clip':
        dashed_box(c,2,2,20,20)
        vector_fragment(c)
    elif key=='transform.array':
        for x in (3,10,17):
            for y in (3,15):box(c,x,y,4,6,x==17)
    elif key=='transform.stretch':
        box(c,3,4,9,16)
        c.line([(17,4),(21,4),(21,20),(17,20)],radius=.5)
        arrow(c,(8,12),(21,12),head=2.5)
    elif key=='transform.explode':
        for pts in [[(3,9),(3,3),(9,3)],[(15,3),(21,3),(21,9)],
                    [(21,15),(21,21),(15,21)],[(9,21),(3,21),(3,15)]]:c.line(pts,radius=.5)
        for a,b in [((10,10),(7,7)),((14,10),(17,7)),((14,14),(17,17)),((10,14),(7,17))]:c.line([a,b],True)
    elif key=='transform.join':
        c.line([(3,6),(8,6),(8,12)],radius=.5)
        c.line([(16,12),(16,18),(21,18)],radius=.5)
        c.line([(8,12),(16,12)],True,radius=0)
        c.circle(8,12,1.2,True,True);c.circle(16,12,1.2,True,True)
    elif key=='transform.split':
        c.line([(3,12),(9,12)]);c.line([(15,12),(21,12)])
        c.line([(9,4),(15,20)],True)
    elif key=='transform.break':
        c.line([(3,3),(9,9)],radius=0);c.line([(15,15),(21,21)],radius=0)
        c.circle(9,9,1.1,True,True);c.circle(15,15,1.1,True,True)
    elif key=='transform.scale':
        box(c,3,13,8,8)
        c.line([(3,8),(3,3),(21,3),(21,21),(16,21)],radius=.5)
        arrow(c,(11,13),(21,3),head=3)
    elif key=='edit.paste-in-place':
        # The clip bridges an open top edge instead of stacking two rectangles.
        c.line([(6,5),(3,5),(3,21),(15,21),(15,5),(12,5)],radius=.7)
        c.line([(6,2),(12,2),(12,7),(6,7)],closed=True,radius=.7)
        c.line([(20,13),(20,20)],True,radius=0)
        c.line([(17.5,16.5),(22.5,16.5)],True,radius=0)
    elif key in {'object.collection-create','object.collection-explode'}:
        box(c,5,6,6,7);box(c,14,12,5,6,True)
        if key.endswith('create'):box(c,2,2,20,20)
        else:brackets(c,2,2,20,20)
    elif key=='edit.paste-vector-clip':
        page(c,2,3,13,18)
        vector_fragment(c,5.575,9.75,.65)
        dimension_arrow(c,(21,6),(21,18),1.8)
    elif key in {'measure.scale-region','measure.scale-page'}:
        if key.endswith('page'):page(c,2,2,20,20)
        else:dashed_box(c,2,2,20,20)
        # A bounded measuring rule with perpendicular end marks.
        c.line([(7,15),(17,9)],True,radius=0)
        c.line([(6,13.3),(8,16.7)],True,radius=0)
        c.line([(16,7.3),(18,10.7)],True,radius=0)
    elif key=='edit.deselect':
        brackets(c,3,3,18,18)
        c.line([(9,9),(15,15)],True,radius=0)
        c.line([(9,15),(15,9)],True,radius=0)
    elif key=='annotate.clear-all':
        page(c,3,3,10,15);page(c,7,6,10,15)
        before=len(c.paths);eraser(c)
        for path in c.paths[before:]:
            scale=c.size/24
            path['points']=[((16+(x/scale-16)*.72)*scale,
                             (17+(y/scale-17)*.72)*scale) for x,y in path['points']]
    elif key.startswith('object.distribute-'):
        vertical=key.rsplit('-',1)[1] in {'top','middle','bottom'}
        variant=key.rsplit('-',1)[1]
        widths=[3,5,4]
        marks=[4,11,18] if variant in {'left','top'} else [6,13,20] if variant in {'right','bottom'} else [5,12,19]
        for mark,w in zip(marks,widths):
            x=mark if variant in {'left','top'} else mark-w if variant in {'right','bottom'} else mark-w/2
            c.line([(x,7),(x+w,7),(x+w,15),(x,15)],closed=True,radius=.4)
        c.line([(marks[0],21),(marks[-1],21)],True)
        for x in marks:c.line([(x,19),(x,23)],True)
        if vertical:
            for p in c.paths:p['points']=[(y,x) for x,y in p['points']]
    elif key=='object.same-size':
        box(c,3,5,7,9);box(c,14,5,7,9)
        arrow(c,(6,20),(18,20),head=2)
        c.line([(6,20),(8,18)],True);c.line([(6,20),(8,22)],True)
    elif key=='transform.flip-vertical':
        c.line([(5,3),(18,3),(18,8)],closed=True,radius=.5)
        c.line([(5,21),(18,21),(18,16)],closed=True,radius=.5)
        c.line([(3,12),(21,12)],True)
    elif key in {'document.watermark-add','document.watermarks'}:
        managing=key=='document.watermarks'
        page(c,2 if managing else 4,3,14 if managing else 16,18)
        drop(c,9 if managing else 12,12.5,2.8 if managing else 3.5)
        if managing:slider(c,21,[10])
    elif key=='document.header-footer':
        page(c,4,2,16,20)
        for y in (6,18):c.line([(8,y),(16,y)],True,radius=0)
        c.line([(9,12),(15,12)],radius=0)
    elif key=='document.edit-text':
        text_t(c,3,5,10,15);pencil(c)
    elif key=='document.ocr':
        brackets(c,3,3,18,18,True);text_t(c,7,8,10,9)
    elif key=='document.edit-scanned-text':
        dashed_box(c,2,3,10,18)
        text_t(c,4,8,6,8);pencil(c)
        for path in c.paths:
            if path['tone']=='accent':
                path['points']=[(x+.7*c.size/24,y) for x,y in path['points']]
    elif key=='document.compress':
        page(c,3,3,18,18)
        dimension_arrow(c,(7,6),(7,11),1.8)
        dimension_arrow(c,(17,18),(17,13),1.8)
    elif key=='page.reorder':
        for y in (3,10,17):box(c,3,y,7,4)
        arrow(c,(15.5,20),(15.5,4),head=1.5)
        arrow(c,(21.5,4),(21.5,20),head=1.5)
    elif key=='capture.page':camera(c)
    elif key=='capture.region':
        brackets(c,3,3,18,18)
        box(c,8,8,8,8,True)
    elif key=='capture.overlay':
        box(c,3,3,12,12);box(c,10,10,11,11,True)
        c.clear_primary=True
    elif key in {'export.cad','export.raster-pdf','export.ifc-report'}:
        page(c,3,3,11,18)
        if key=='export.cad':c.line([(5,16),(8.5,8),(12,16)],radius=.4)
        elif key=='export.raster-pdf':
            c.circle(6.5,8,1,filled=True)
            c.line([(5,17),(8.5,12),(12,17)],radius=.4)
        else:
            dx=3*math.sqrt(3)/2
            detail_line(c,[(8.5,9),(8.5+dx,10.5),(8.5+dx,13.5),(8.5,15),(8.5-dx,13.5),(8.5-dx,10.5),(8.5,9)])
            detail_line(c,[(8.5-dx,10.5),(8.5,12),(8.5+dx,10.5)]);detail_line(c,[(8.5,12),(8.5,15)])
        dimension_arrow(c,(17,12),(22,12),1.8)
    elif key=='document.email':
        box(c,3,5,18,14)
        c.line([(3,6),(12,13),(21,6)],True,radius=.7)
    elif key=='view.actual-size':
        brackets(c,3,3,18,18)
        # A geometric 1:1; no runtime text/font dependency.
        for x in (7,17):c.line([(x-1.5,9),(x,7),(x,17)],True,radius=.3)
        for y in (10,14):c.circle(12,y,.65,filled=True)
    elif key in {'view.rotate-left','view.rotate-right'}:
        box(c,3,13,18,8)
        c.line([(4,16),(20,16)])
        c.line(arc_points(12,10,7,180,360),True,radius=0)
        c.line([(2.5,7.5),(5,10),(7.5,7.5)],True,radius=.5)
        if key.endswith('right'):c.mirror()
    elif key=='object.properties':
        box(c,3,3,12,18)
        for y in (7,11,15):c.line([(6,y),(11,y)])
        slider(c,20,[11],5,19)
    elif key=='panel.annotations':
        for y in (5,11,17):
            c.circle(4,y,1,True,True);c.line([(8,y),(21,y)])
    elif key=='panel.element-visibility':
        extend_base(c,'object.hide')
    elif key=='panel.symbol-library':
        box(c,3,3,7,7);c.circle(17,6.5,3.5)
        c.line([(3,21),(6.5,14),(10,21)],closed=True,radius=.4)
        c.plus(17,17,3.5)
    elif key=='view.thin-lines':
        fill_rect(c,3,5,18,1,True);fill_rect(c,3,17.5,18,1,True)
        c.line([(3,12),(21,12)])
    elif key=='view.remember-reading':
        c.line([(3,5),(8,5),(12,7),(16,5),(21,5),(21,21),(16,21),(12,23),(8,21),(3,21)],closed=True,radius=.6)
        c.line([(12,7),(12,23)],radius=0)
        c.line([(15,3),(20,3),(20,13),(17.5,11),(15,13)],True,closed=True,radius=.25)
        c.clear_primary=True
    elif key=='document.compare':
        page(c,2,3,8,18);page(c,14,3,8,18)
        for x in (4.5,16.5):
            for y in (8,12,16):
                accent=(x==4.5 and y==8) or (x==16.5 and y==12)
                c.line([(x,y),(x+3,y)],accent,radius=0)
    elif key=='view.show-keystrokes':
        box(c,2,5,20,14)
        for x in (6,10,14,18):c.circle(x,9,.6,filled=True)
        c.line([(8,15),(14,15),(14,12)],True,radius=.4)
        c.line([(8,15),(10,13)],True);c.line([(8,15),(10,17)],True)
    elif key=='measure.takeoff':
        for y in (4,9,14):
            c.circle(4,y,.7,True,True);c.line([(8,y),(21,y)])
        c.line([(3,19),(21,19)],radius=0)
        for x in (7,12,17):c.line([(x,19),(x,22)],True,radius=0)
    elif key=='symbol.parametric-picker':
        box(c,3,4,10,16)
        c.line([(6,8),(10,8)]);c.line([(6,12),(10,12)])
        slider(c,19,[8,16])
    elif key=='object.reset-location':
        box(c,3,13,9,9)
        c.line([(21,19),(21,5),(7.5,5),(7.5,10)],True,radius=2)
        c.line([(5,7.5),(7.5,10),(10,7.5)],True,radius=0)
    elif key=='ui.whats-new':
        page(c,3,7,11,14)
        for y in (12,16):c.line([(6,y),(11,y)])
        c.line([(20,1.5),(20,6.5)],True,radius=0)
        c.line([(17.5,4),(22.5,4)],True,radius=0)
        c.line([(18.2,2.2),(21.8,5.8)],True,radius=0)
        c.line([(18.2,5.8),(21.8,2.2)],True,radius=0)

    return True
