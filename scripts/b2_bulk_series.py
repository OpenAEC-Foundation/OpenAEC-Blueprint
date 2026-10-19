"""Original B2 drawings for six consecutive, source-reviewed batches.

PDF actions refer to the pinned Solid implementation, not the v3 placeholders.
Only the individual source records listed here are assessed.
"""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points

AVAILABLE_SERIES = (15,16,17,18,19,20)
GROUPS = {15:'Paginabewerkingen',16:'Annoteren en meten',17:'Extra tekengereedschappen',
          18:'Rangschikken en verdelen',19:'Beeldbewerking',20:'Extensies en hulpfuncties'}
# batch, contract, Dutch label, precise meaning, inspected catalog record
ROWS = [
 (15,'page.insert','Pagina invoegen','Het invoegdialoog voor documentpagina’s openen.','03611e7c3191bc2e'),
 (15,'page.delete','Pagina verwijderen','Het dialoog voor pagina’s verwijderen openen; geen annotaties wissen.','c5f8b57fecad63ae'),
 (15,'page.extract','Pagina’s extraheren','Gekozen documentpagina’s via het extractiedialoog afzonderen.','ee8e8fae89c7e4d9'),
 (15,'document.merge','PDF’s samenvoegen','Het dialoog voor meerdere PDF-documenten samenvoegen openen.','109d3a5be24fe213'),
 (15,'page.rotate-left','Pagina linksom draaien','Documentpagina’s 90 graden linksom draaien; opgeslagen, ongedaan te maken paginabewerking.','4b2c5fedc628eaf8'),
 (15,'page.rotate-right','Pagina rechtsom draaien','Documentpagina’s 90 graden rechtsom draaien; geen tijdelijke weergavedraaiing.','f52faadbb61c63ba'),
 (15,'page.crop','Paginamarges bijsnijden','Het dialoog voor bijsnijden van documentpaginamarges openen; geen afbeelding bijsnijden.','25c6791aa8b4ea2a'),
 (15,'page.resize','Paginaformaat wijzigen','Het dialoog voor documentpagina-afmetingen openen; geen object schalen.','78c1dfa140d9e3f8'),
 (15,'page.straighten','Pagina rechtzetten','Het gereedschap voor rechtzetten van een documentpagina starten.','d5ffa750e085ff47'),
 (15,'page.shift','Pagina-inhoud verschuiven','Het dialoog voor verschuiven binnen documentpagina’s openen.','0e280e01d1ef531b'),
 (16,'annotate.highlight','Tekst markeren','Het markeergereedschap voor tekstannotaties activeren.','0bf70d643f6fbe20'),
 (16,'annotate.stamp','Stempel plaatsen','Het annotatiestempelgereedschap activeren; geen parametrisch bouwsymbool.','060984fea64a1271'),
 (16,'annotate.signature','Handtekening plaatsen','Het handtekeninggereedschap activeren; dit icoon bewijst geen juridische of cryptografische ondertekening.','594905f3e32dc771'),
 (16,'annotate.redact','Redactie markeren','Een gebied voor redactie markeren; nog niet toepassen.','e43b5acb39895fec'),
 (16,'annotate.apply-redactions','Redacties toepassen','Gemarkeerde redacties toepassen via applyRedactions; andere opdracht dan een redactiegebied tekenen.','baae463757e61700'),
 (16,'annotate.clear-page','Pagina-annotaties wissen','Na bevestiging annotaties van de huidige pagina wissen; de documentpagina blijft bestaan.','5da23da2be4ccd13'),
 (16,'measure.perimeter','Omtrek meten','Het omtrekmeetinstrument activeren; geen oppervlak of enkele afstand.','0b56945e9a4cf444'),
 (16,'measure.angle','Hoek meten','Het hoekmeetinstrument activeren.','7fbb1fa727be8473'),
 (17,'draw.freehand','Vrije hand tekenen','Vrije handlijn tekenen met het draw-gereedschap.','1108117107122048'),
 (17,'draw.eraser','Vrije hand uitgummen','Het gumgereedschap activeren voor vrije handlijnen.','080fc764237511a1'),
 (17,'draw.ellipse','Ellips tekenen','Een ellips plaatsen; apart van cirkel tekenen en objecten tellen.','24d5787030b9561d'),
 (17,'draw.arrow','Pijl tekenen','Een rechte pijlannotatie plaatsen; geen navigatieopdracht.','9c775b7c80813ae0'),
 (17,'draw.spline','Spline tekenen','Een vloeiende spline tekenen; geen gebogen pijl.','8591dee76e5c7bf1'),
 (17,'transform.fillet','Hoek afronden','Het fillet-gereedschap activeren voor een ronde geometrische hoek.','d7ec2df09b3cc12b'),
 (17,'transform.chamfer','Hoek afkanten','Het chamfer-gereedschap activeren voor een rechte afschuining.','d7425a71fcb7e9ff'),
 (17,'draw.image','Afbeelding plaatsen','Het gereedschap voor plaatsen van een afbeelding activeren.','5561a98d6bd82fe4'),
 (18,'object.align-top','Boven uitlijnen','Geselecteerde objecten langs hun bovenkant uitlijnen; geen tekstuitlijning.','78262e2573df1722'),
 (18,'object.align-middle','Verticaal centreren','Geselecteerde objecten op dezelfde verticale middenhoogte uitlijnen.','aa281f534267e5be'),
 (18,'object.align-bottom','Onder uitlijnen','Geselecteerde objecten langs hun onderkant uitlijnen.','7987a085babcd841'),
 (18,'object.distribute-horizontal','Horizontaal verdelen','Gelijke horizontale tussenruimte tussen geselecteerde objecten maken.','31d83910128c564f'),
 (18,'object.distribute-vertical','Verticaal verdelen','Gelijke verticale tussenruimte tussen geselecteerde objecten maken.','f4cedc7173dc846c'),
 (18,'object.bring-forward','Eén stap naar voren','De selectie één stap naar voren in de tekenvolgorde brengen.','50e33f5ab1e8bcff'),
 (18,'object.bring-front','Helemaal naar voren','De selectie voor alle andere annotaties plaatsen.','3451c6ceb360bae0'),
 (18,'object.send-backward','Eén stap naar achteren','De selectie één stap naar achteren in de tekenvolgorde brengen.','7df32960de53034f'),
 (18,'object.send-back','Helemaal naar achteren','De selectie achter alle andere annotaties plaatsen.','069a7ee47a60c889'),
 (19,'image.crop','Afbeelding bijsnijden','De bijsnijdmodus voor de geselecteerde afbeelding schakelen; geen documentpaginamarges.','b340b27f01089144'),
 (19,'image.grayscale','Grijswaarden','De grijswaardebewerking voor een afbeelding schakelen.','a11b03f363a92ab4'),
 (19,'image.brightness','Helderheid','De helderheidsregeling van een afbeelding aanduiden.','c02d64668f891930'),
 (19,'image.contrast','Contrast','De contrastregeling van een afbeelding aanduiden.','3d61c30c98965747'),
 (19,'image.reset','Beeldcorrecties herstellen','De beeldcorrecties terugzetten via resetImageAdjustments; geen pagina- of objectrotatie.','6eeb56efc8f8ce8a'),
 (20,'extensions.manage','Extensies beheren','Het venster voor extensies openen; geen uitvoering van een specifieke extensie.','e6b024f6ba1a48a0'),
 (20,'ui.about','Over deze app','Het informatievenster over de toepassing openen; geen informatiemelding.','492b54d0123dd6dd'),
 (20,'ui.shortcuts','Sneltoetsen','Het overzicht van toetsencombinaties openen.','dc3b5589f685173b'),
 (20,'ui.check-updates','Updates controleren','Handmatig op appupdates controleren; geen startupdiagnostiek.','e7f468df7094a54b'),
 (20,'ui.file-associations','Bestandskoppelingen','Voorkeuren voor bestandsassociaties openen.','2e432b6f83171c60'),
]
ACTIVE_ROWS=[r for r in ROWS if r[0] in AVAILABLE_SERIES]
DEFINITIONS=[(key,label,GROUPS[batch],meaning) for batch,key,label,meaning,_ in ACTIVE_ROWS]
EXAMPLES={key:record for _,key,_,_,record in ACTIVE_ROWS}
SERIES={key:batch for batch,key,_,_,_ in ACTIVE_ROWS}
KEYS=set(SERIES)
# Filled below from the already inspected, pinned catalog; never blanket aliases.
SOURCE_FUNCTIONS = {'page.insert': 'review.paginainvoegen', 'page.delete': 'page.delete', 'page.extract': 'review.paginasextraheren', 'document.merge': 'review.pdfssamenvoegen', 'page.rotate-left': 'review.linksomdraaien', 'page.rotate-right': 'review.rechtsomdraaien', 'page.crop': 'review.margesbijsnijden', 'page.resize': 'review.paginaformaat', 'page.straighten': 'review.paginarechtzetten', 'page.shift': 'review.paginaverschuiven', 'annotate.highlight': 'review.markeren', 'annotate.stamp': 'review.stempel', 'annotate.signature': 'review.handtekening', 'annotate.redact': 'review.markerenvoorredactie', 'annotate.apply-redactions': 'review.redactiestoepassenophuidigepagina', 'annotate.clear-page': 'review.annotatiesoppaginawissen', 'measure.perimeter': 'review.omtrekmeten', 'measure.angle': 'review.hoekmeten', 'draw.freehand': 'review.vrijehand', 'draw.eraser': 'review.gumverwijdertvrijehandlijnen', 'draw.ellipse': 'review.ellips', 'draw.arrow': 'review.pijl', 'draw.spline': 'review.splinedubbelklikomtevoltooien', 'transform.fillet': 'review.afronden', 'transform.chamfer': 'review.afkanten', 'draw.image': 'review.afbeelding', 'object.align-top': 'review.aligntop', 'object.align-middle': 'review.alignmiddle', 'object.align-bottom': 'review.alignbottom', 'object.distribute-horizontal': 'review.horizontaalverdelen', 'object.distribute-vertical': 'review.verticaalverdelen', 'object.bring-forward': 'review.bringforward', 'object.bring-front': 'review.bringtofront', 'object.send-backward': 'review.sendbackward', 'object.send-back': 'review.sendtoback', 'image.crop': 'review.crop', 'image.grayscale': 'review.grayscale', 'image.brightness': 'review.brightness', 'image.contrast': 'review.contrast', 'image.reset': 'review.resetadjust', 'extensions.manage': 'extensions.manage', 'ui.about': 'review.about', 'ui.shortcuts': 'review.shortcuts', 'ui.check-updates': 'review.updates', 'ui.file-associations': 'review.fileassoc'}
REUSED = {
 '97a470c60f596657':('page.first','PDF-lintknop roept goToPage(1) aan; zelfde functie als de statusbalk.'),
 '312c6f877999a075':('page.previous','PDF-lintknop gaat naar currentPage - 1; hergebruik van Vorige pagina.'),
 '8c631742a67394c5':('page.next','PDF-lintknop gaat naar currentPage + 1; hergebruik van Volgende pagina.'),
 'e2b36d51e4ceeb28':('page.last','PDF-lintknop gaat naar numPages; hergebruik van Laatste pagina.'),
 '03e29bb7dc2153e4':('draw.note','CommentTab activeert comment; dezelfde annotatiefunctie als Opmerking.'),
 'eec143c4ceed249e':('draw.line','DrawingTab activeert line; hergebruik van Lijn tekenen.'),
}


def page(c,x=5,y=3,w=12,h=18,accent=False):
    return box(c,x,y,w,h,accent)


def arrow(c,a,b,accent=True,head=2.5):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    ux,uy=dx/length,dy/length
    c.line([a,b],accent)
    c.line([(b[0]-head*ux-head*uy,b[1]-head*uy+head*ux),b,
            (b[0]-head*ux+head*uy,b[1]-head*uy-head*ux)],accent,radius=.6)


def crop(c,accent=False):
    c.line([(3,7),(17,7),(17,21)],accent,radius=1)
    c.line([(7,3),(7,17),(21,17)],accent,radius=1)


def curve(c,points,accent=False):
    # Cubic Bezier sampled at a fixed resolution; smooth even at small sizes.
    a,b,d,e=points
    samples=[]
    for i in range(49):
        t=i/48;u=1-t
        samples.append((u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*d[0]+t**3*e[0],
                        u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*d[1]+t**3*e[1]))
    c.line(samples,accent,radius=0)


def reset_ring(c,accent=False):
    # Extend the tangent beyond the circle before adding a symmetric head.
    # This keeps both arms clear of the curved shaft and the inner symbol.
    c.line(arc_points(12,12,8,0,270)+[(15,4)],accent,radius=0)
    c.line([(12,1.5),(15,4),(12,6.5)],accent,radius=.35)


def extend(c,key):
    if key not in KEYS:return False
    if key in {'page.insert','page.delete','page.extract'}:
        page(c,3 if key!='page.extract' else 4,3,9 if key!='page.extract' else 11,18)
        if key=='page.insert':c.plus(19,12,2.5)
        elif key=='page.delete':c.line([(17,9.5),(21,13.5)],True);c.line([(21,9.5),(17,13.5)],True)
        else:arrow(c,(10,12),(21,12),head=2.5)
    elif key=='document.merge':
        page(c,3,3,7,11);page(c,14,3,7,11)
        c.line([(6.5,17),(6.5,20),(17.5,20),(17.5,17)],True,radius=1)
        c.line([(12,15),(12,20)],True)
    elif key in {'page.rotate-left','page.rotate-right'}:
        page(c,8,11,8,10)
        c.line(arc_points(12,10,7,180,360),True,radius=0)
        c.line([(2.5,7.5),(5,10),(7.5,7.5)],True,radius=.5)
        if key=='page.rotate-right':c.mirror()
    elif key=='page.crop':
        page(c,4,3,16,18)
        c.line([(7,8),(15,8),(15,18)],True,radius=.6)
        c.line([(9,6),(9,16),(17,16)],True,radius=.6)
    elif key=='page.resize':
        page(c,4,3,12,16)
        arrow(c,(10,13),(20,3),head=2)
        c.line([(8,22),(20,22),(20,10)],radius=1)
    elif key=='page.straighten':
        c.line([(5,7),(15,3),(20,16),(10,20)],closed=True,radius=1)
        c.line([(3,22),(21,22)],True)
        c.line([(8,12),(16,9)],True)
    elif key=='page.shift':
        page(c,3,3,18,18)
        arrow(c,(7,12),(17,12),head=2)
    elif key=='annotate.highlight':
        c.line([(5,14),(14,4),(20,9),(11,19)],closed=True,radius=.6)
        c.line([(5,14),(11,19)],True)
        c.line([(3,22),(19,22)],True)
    elif key=='annotate.stamp':
        box(c,4,15,16,5)
        c.line([(8,15),(8,11),(10,8),(10,4),(14,4),(14,8),(16,11),(16,15)],radius=1)
        c.line([(5,22),(19,22)],True)
    elif key=='annotate.signature':
        curve(c,[(3,16),(8,13),(12,2),(9,6)],True)
        curve(c,[(9,6),(3,17),(13,20),(15,12)],True)
        curve(c,[(15,12),(14,19),(18,15),(21,16)],True)
        c.line([(3,21),(21,21)])
    elif key in {'annotate.redact','annotate.apply-redactions'}:
        applying=key=='annotate.apply-redactions'
        box(c,3,4 if applying else 5,14 if applying else 18,13 if applying else 14)
        c.line([(7,9 if applying else 10),(13 if applying else 17,9 if applying else 10)])
        c.line([(7,13 if applying else 14),(13 if applying else 17,13 if applying else 14)],True)
        if applying:
            c.line([(14,18.5),(17,21.5),(22,15.5)],True,radius=.4)
    elif key=='annotate.clear-page':
        page(c,3,3,11,17)
        c.line([(7,8),(10,8)])
        c.line([(11,16),(17,10),(22,15),(16,21),(15,21)],True,closed=True,radius=.5)
        c.line([(14,13),(19,18)],True,radius=0)
        c.line([(17,22),(22,22)],True)
        c.clear_primary=True
    elif key=='measure.perimeter':
        c.line([(19,19),(5,19),(5,5)],radius=.7)
        c.line([(5,5),(19,5),(19,19)],True,radius=.7)
        for x,y in [(5,5),(19,5),(19,19),(5,19)]:c.circle(x,y,1.25,filled=True)
    elif key=='measure.angle':
        c.line([(4,4),(4,20),(21,20)],radius=.3)
        c.line(arc_points(4,20,10,-90,0),True,radius=0)
    elif key=='draw.freehand':
        curve(c,[(3,17),(8,2),(16,3),(11,12)])
        curve(c,[(11,12),(5,22),(15,21),(21,7)])
    elif key=='draw.eraser':
        c.line([(3,15),(14,4),(21,11),(11,21),(9,21)],closed=True,radius=.6)
        c.line([(8,10),(15,17)],True)
        c.line([(13,21),(22,21)])
    elif key=='draw.ellipse':
        c.line([(12+9*math.cos(i*math.tau/96),12+6*math.sin(i*math.tau/96)) for i in range(96)],closed=True,radius=0)
        c.line([(12,12),(21,12)],True)
    elif key=='draw.arrow':
        c.line([(4,20),(20,4)])
        c.line([(14,4),(20,4),(20,10)],True,radius=.6)
    elif key=='draw.spline':
        curve(c,[(3,18),(5,-2),(19,26),(21,6)])
        for x,y in [(3,18),(21,6)]:c.circle(x,y,1.5,True,True)
    elif key in {'transform.fillet','transform.chamfer'}:
        c.line([(4,21),(4,4),(21,4)],radius=.2)
        if key=='transform.fillet':
            c.line([(9,21),(9,16)],True)
            c.line(arc_points(16,16,7,180,270),True,radius=0)
            c.line([(16,9),(21,9)],True)
        else:c.line([(9,21),(9,15),(15,9),(21,9)],True,radius=.3)
    elif key=='draw.image':
        box(c,3,4,18,16)
        c.circle(8,9,1.4,True,True)
        c.line([(4,18),(10,12),(14,16),(17,13),(20,16)],True,radius=.6)
    elif key.startswith('object.align-'):
        if key=='object.align-top':a,b,y=(8,20),(8,16),4
        elif key=='object.align-middle':a,b,y=(4,20),(7,17),12
        else:a,b,y=(4,16),(8,16),20
        box(c,5,a[0],4,a[1]-a[0]);box(c,15,b[0],4,b[1]-b[0])
        c.line([(3,y),(21,y)],True)
    elif key in {'object.distribute-horizontal','object.distribute-vertical'}:
        for x,h in [(3,8),(10,12),(17,10)]:
            y=11-h/2
            c.line([(x,y),(x+4,y),(x+4,y+h),(x,y+h)],closed=True,radius=.45)
        c.line([(5,21),(19,21)],True)
        for x in (5,12,19):c.line([(x,19),(x,23)],True)
        if key.endswith('vertical'):
            for p in c.paths:p['points']=[(y,x) for x,y in p['points']]
    elif key in {'object.bring-forward','object.bring-front','object.send-backward','object.send-back'}:
        front=key in {'object.bring-forward','object.bring-front'}
        # Full vs one-step has a different number of depth markers.
        box(c,3,10,8,10);box(c,7,5,8,10,True)
        c.clear_primary=True
        x=21
        arrow(c,(x,18 if front else 6),(x,6 if front else 18),head=1.7)
        if key in {'object.bring-front','object.send-back'}:
            y=2 if front else 22;c.line([(19,y),(23,y)],True)
    elif key=='image.crop':
        c.line([(3,7),(17,7),(17,21)],radius=1)
        c.line([(7,3),(7,17)],radius=1)
        c.line([(7,17),(21,17)],True)
    elif key in {'image.grayscale','image.contrast'}:
        c.circle(12,12,8)
        c.line([(12,4),(12,20)],True)
        if key=='image.grayscale':
            for y in (9,12,15):c.line([(13,y),(18,y)],True)
        else:
            for x in (14,16,18):
                h=math.sqrt(7**2-(x-12)**2);c.line([(x,12-h),(x,12+h)],True)
    elif key=='image.brightness':
        c.circle(12,12,4,True)
        for i in range(8):
            angle=i*math.tau/8
            c.line([(12+7*math.cos(angle),12+7*math.sin(angle)),
                    (12+10*math.cos(angle),12+10*math.sin(angle))])
    elif key=='image.reset':
        box(c,8,10,8,5)
        reset_ring(c,True)
    elif key=='extensions.manage':
        # Four modules with a detached accent module: remains clear at 16 px.
        for x,y,tone in [(3,3,False),(3,14,False),(14,14,False),(14,3,True)]:box(c,x,y,7,7,tone)
    elif key=='ui.about':
        c.circle(12,12,9)
        c.circle(12,7,1,True,True);c.line([(10,11),(12,11),(12,17)],True,radius=.5)
        c.line([(10,17),(14,17)],True)
    elif key=='ui.shortcuts':
        box(c,2,5,20,14)
        for y in (9,13):
            for x in (6,10,14,18):c.circle(x,y,.6,filled=True)
        c.line([(8,17),(16,17)],True)
    elif key=='ui.check-updates':
        reset_ring(c)
        arrow(c,(12,17),(12,9),head=2.5)
    elif key=='ui.file-associations':
        page(c,3,3,9,18)
        arrow(c,(16,12),(22,12),head=2.5)
    return True
