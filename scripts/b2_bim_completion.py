"""BIM Validator controls verified through Ribbon -> AppShell -> event/store wiring."""
import math
from b2_second_series import box
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS={62:'BCF en cloudbestanden',63:'Snijvlakken',64:'Validatieweergave'}
ROWS=[
 (62,'bcf.export','BCF exporteren','De huidige issues of PDF-markeringen als BCF-pakket uitvoeren; geen issues naar een server pushen.','b84ade848ad77378'),
 (62,'bcf.push','BCF-issues verzenden','bcfPushIssues verstuurt de klaarstaande issues naar het geselecteerde verbonden BCF-project.','46817b2402a9a42c'),
 (62,'cloud.save','Cloudbestand opslaan','Een BCF-bestand voorbereiden en het cloudvenster in save-modus openen; nog een bestemming kiezen.','b4b2e0d81788b2d8'),
 (62,'cloud.open','Cloudbestand kiezen','Het cloudbestandspaneel of cloudvenster in open-modus tonen; nog geen bestand downloaden of lokaal project openen.','15fc3480ed94a030'),
 (62,'ui.file-menu','Bestandmenu openen','De als Inloggen gelabelde knop roept hier alleen setBackstageOpen(true) aan; geen aanmelding bewezen.','2bf5ec0ccc60408e'),
 (62,'feedback.attach-images','Feedbackafbeeldingen kiezen','De verborgen afbeeldingsbestandskeuze openen; geen exportopdracht.','6a16c60a264db1da'),
 (63,'section.plane-x','Snijvlak X','add-section-plane versturen met axis x; het snijvlak staat loodrecht op X.','14980082f2387cbe'),
 (63,'section.plane-y','Snijvlak Y','add-section-plane versturen met axis y; het snijvlak staat loodrecht op Y.','2dc3a6ed5dad3dd5'),
 (63,'section.plane-z','Snijvlak Z','add-section-plane versturen met axis z; het snijvlak staat loodrecht op Z.','e6433ae2a060d8cc'),
 (63,'section.clear','Snijvlakken wissen','remove-section-planes wist alle actieve snijvlakken; modelgeometrie blijft bestaan.','6ec142048f3ff593'),
 (64,'view.reset-camera','Modelweergave herstellen','De 3D-camera naar het standaardbeeld herstellen; de BIM-bron heft daarbij ook de elementselectie op.','6998b8d32a5c2501'),
 (64,'validation.highlight-failures','Afgekeurde elementen markeren','GlobalIds uit gefaalde validatieregels verzamelen en als een highlightgroep tonen.','a91fb3b2995cdaee'),
 (64,'validation.clear-highlights','Validatiemarkeringen wissen','clearHighlights verwijdert de 3D-kleurmarkeringen; validatieresultaten blijven bestaan.','a81ae086eceb71f1'),
 (64,'image.placeholder','Geen voorbeeldafbeelding','Vaste fallback voor een BCF-miniatuur zonder screenshot; geen afbeelding invoegen.','fd4b86ab381d47ed'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De markering of richting blijft ononderbroken voor de achterliggende contour.' for k in ('cloud.save','cloud.open','bcf.export','bcf.push','section.plane-x','section.plane-y','section.plane-z','section.clear','validation.clear-highlights')}
REUSED={
 '62721a140f3d9750':('bcf.export','Field exportBCF schrijft de veldwerktickets als BCF 2.1 ZIP; geen lagenbeheer. Klikbinding en ZIP-opbouw in public/app.js gelezen.'),
 '2889c1e0f757d3a0':('tree.expand','De issuechevron toont of verbergt de issuegegevens.'),
 'b048539a6a5dafd0':('ui.dropdown','De keuzeveldknop schakelt open.'),
 '96ba0d6b2e67e469':('ifc.import','TitleBar -> handleUploadClick -> .ifc/.ifcx-bestandskeuze -> addModel; dit is modelinvoer.'),
 '3ed478d67e15cb79':('ui.help','De hulpknop opent de bronprojectpagina.'),
 'b0009f8d90430cd8':('file.open','Bestand Openen biedt de lokale .wefc-keuze en de serverprojectkiezer; volledige hydratatie staat in deze bron nog open.'),
 '788e866df0350c7b':('file.save','Bestand Opslaan bewaart de project-envelop lokaal of in de cloud.'),
 '6a0f5418d6c1c0e2':('file.save-as','Opslaan als kiest een nieuwe lokale naam of serverprojectidentiteit.'),
 '66e38e0780d30efe':('ui.close','handleClose sluit hier alleen Bestand; reset van het model is een TODO.'),
 '956ea1027e6b8212':('ui.settings','De voorkeurenactie opent de instellingen.'),
 '312848128cd112c7':('ui.about','De About-menuactie opent het appinformatiepaneel.'),
 '7e79e18c6d0327a4':('ui.close','De Exit-handler doet in de webversie alleen onClose.'),
 '56ab700f294bb054':('server.storage','Bestemmingsindicator voor de serverprojecten.'),
 'f43c295feb69951e':('file.local','Bestemmingsindicator voor lokale bestanden.'),
 '8414feb6e32d41f0':('nav.back','De Bestand-terugknop keert terug naar de werkruimte.'),
 'c5b6490549268b3d':('ui.close','De Afsluiten-menuplaats sluit in de webvariant alleen Bestand.'),
 'cafafd09bfcb7fc2':('link.open-external','De website-link opent open-aec.com.'),
 '561c88b93f2b0e8f':('link.open-external','De bronproject-link opent de GitHub-pagina; geen nieuwe Git-bewerking.'),
 '0dbf2ee9ecbb3407':('ifc.import','De lintknop gebruikt dezelfde IFC-bestandskiezer en addModel-route.'),
 '8394d2f52cb7f9d9':('panel.right','onToggleRightPanel schakelt het validatiezijpaneel.'),
 '8e33d5dec6474b41':('view.fit','zoom-fit-all past de geladen modelgeometrie in de weergave.'),
 '85da12bbef4e675f':('file.save','De lintknop roept handleSave aan voor het huidige project.'),
 '0712f8b77ac40ee6':('file.save-as','De lintknop opent de SaveAs-keuze.'),
 '568aeb95f1e7a269':('file.open','De lintknop opent het project-openvenster.'),
 '5f10f4e17e7c2508':('ui.dropdown','De themakiezer schakelt zijn keuzemenu.'),
 '67e185eb2fcee6cc':('ui.refresh','cloudLoadProjects vernieuwt de cloudprojectlijst.'),
 '5c6229c289c26535':('file.open','handleLocalOpen start de lokale projectbestandkeuze.'),
 '4c07dcc8fb703250':('cloud.open','De optie kiest target cloud binnen hetzelfde openvenster.'),
 '4687ed651fc78b50':('ui.refresh','De open-projectenlijst wordt opnieuw opgehaald.'),
 '7749107ef45411f3':('project.folder','Projectmapindicator bij een klikbare projectnaam.'),
 '3de4bd540f8d8d9a':('file.save-as','De optie kiest de lokale bestemming van Opslaan als; geen importactie.'),
 '43c2b2b6c5663ecd':('cloud.save','De optie kiest de cloudbestemming van Opslaan als.'),
 '6d86db161a678e37':('ui.refresh','De cloudprojectlijst in Opslaan als wordt opnieuw opgehaald.'),
 '60be2d9926d8b386':('file.download','handleDownloadJson serialiseert en downloadt bestaande validatieresultaten als JSON.'),
}
EXCLUDED={
 'a2337d23cb8b9fc3':'Appbeeldmerk in de titelbalk.',
 '184969243a79cffc':'handleNew vraagt onNavigate(/), maar de gemonteerde AppShell-callback logt dit alleen. Het menu sluit; navigatie en projectreset zijn niet aangesloten. Nieuw document en Home blijven ontwerpcontracten.',
 'aa5e16bc4b81b412':'onSyncPlatform wordt doorgegeven maar nergens door de gemonteerde AppShell ingevuld; geen actieve synchronisatie aangetoond.',
 'dc22983cc947382e':'onRemoveModel wordt door Ribbon/HomeTab doorgegeven maar niet door AppShell ingevuld; deze lintplaats is een placeholder.',
 '4d5ed0c958d22668':'IDS Standaard heeft geen callback op deze lintplaats; de werkende IDS-selectie in het validatiepaneel is een andere bediening.',
 '5ea99a4a22dd643f':'onResetValidation is niet door de gemonteerde AppShell ingevuld; geen resetimplementatie voor deze knop.',
}
# All of these records belong to marketing HTML or a disconnected static mockup.
for _record in ('21c0f7dee2708446','f98be2296710e02d','6be8c99340ee1c11','f5ac9cf6d705faae',
                'ed5aabd4b9c771ab','a7c654d72684da3e','d0befa0bf383ecd6','e6b3525d409f3421',
                'fa4b9add1f8091a2','a886b8997afbba34','26aab008bf863920','4ef6e913eda9bde0',
                'a5d8b23eece7f3c3','837f6b60fa415181','1336e670e208d440','1b6635ee2806d28e',
                '1a21522a89df1f92','b4bdc7bfe575aa31','30a4ade0b2d59558','4a7b6bafb68c0d12','da822c920e5a2d22'):
    EXCLUDED[_record]='Statische webpagina of niet-gemonteerde 3bm-viewer-mockup; geen bewijs van een actieve applicatiebediening.'


def cube(c):
    x=5*math.sqrt(3)
    c.line([(12,2),(12+x,7),(12+x,17),(12,22),(12-x,17),(12-x,7)],closed=True,radius=.3)
    c.line([(12-x,7),(12,12),(12+x,7)],radius=.3)
    c.line([(12,12),(12,22)],radius=0)


def cloud(c):
    # Original cloud silhouette: union of circular lobes and a flat base.
    # Buffer its boundary into a filled outline; preserve the interior hole.
    from shapely.geometry import Point as GeoPoint, box as geo_box
    from shapely.ops import unary_union
    scale=c.size/24
    shape=unary_union([GeoPoint(x*scale,y*scale).buffer(r*scale,quad_segs=32)
                       for x,y,r in ((7,11,4),(12,8,6),(17,11,4))]+[geo_box(3*scale,11*scale,21*scale,16*scale)])
    outline=shape.boundary.buffer(c.width/2,quad_segs=20)
    parts=[outline] if outline.geom_type=='Polygon' else list(outline.geoms)
    for part in parts:
        c.fills.append({'tone':'primary','rings':[list(part.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in part.interiors]})


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key in {'bcf.export','bcf.push'}:
        c.line([(2,20),(2,4),(15,4),(15,16),(8,16),(4,20)],closed=True,radius=.6)
        for y,w in ((8,11),(12,9)):c.line([(6,y),(w,y)],radius=0)
        if key=='bcf.export':dimension_arrow(c,(14,17),(22,17),2.5)
        else:dimension_arrow(c,(20,21),(20,8),2.5)
    elif key in {'cloud.save','cloud.open'}:
        cloud(c)
        if key=='cloud.save':dimension_arrow(c,(12,22),(12,11),2.8)
        else:dimension_arrow(c,(12,11),(12,22),2.8)
    elif key=='ui.file-menu':
        c.line([(3,20),(3,7),(8,7),(11,10),(21,10),(21,20)],closed=True,radius=.6)
        c.line([(6,3),(18,3)],True,radius=0)
    elif key=='feedback.attach-images':
        box(c,2,3,15,15);c.circle(6,7,1.5)
        c.line([(2,15),(6,11),(10,14),(14,9),(17,12)],radius=.5)
        c.plus(19,20,2.8,True)
    elif key.startswith('section.plane-'):
        cube(c)
        axis=key[-1]
        def project(x,y,z):return (12+5*math.sqrt(3)*(x-y),12+5*(x+y)-10*z)
        if axis=='x':points=[project(.5,y,z) for y,z in ((0,1),(1,1),(1,0),(0,0))]
        elif axis=='y':points=[project(x,.5,z) for x,z in ((0,1),(1,1),(1,0),(0,0))]
        else:points=[project(x,y,.5) for x,y in ((0,0),(1,0),(1,1),(0,1))]
        c.line(points,True,closed=True,radius=.3)
    elif key=='section.clear':
        c.line([(3,7),(12,2),(21,7),(12,12)],closed=True,radius=.4)
        c.line([(3,13),(12,18),(21,13)],radius=.4)
        c.line([(16,17),(22,23)],True,radius=0);c.line([(16,23),(22,17)],True,radius=0)
    elif key=='view.reset-camera':
        cube(c)
        scale=c.size/24
        for path in c.paths:path['points']=[(.6*x+4.8*scale,.6*y+4.8*scale) for x,y in path['points']]
        c.line(arc_points(12,12,10,220,490,64),True,radius=0)
        t=math.radians(490);tip=(12+10*math.cos(t),12+10*math.sin(t))
        ux,uy=-math.sin(t),math.cos(t)
        c.line([(tip[0]-2*ux-2*uy,tip[1]-2*uy+2*ux),tip,(tip[0]-2*ux+2*uy,tip[1]-2*uy-2*ux)],True,radius=0)
    elif key=='validation.highlight-failures':
        cube(c)
        # Reserve a clear lane for the exclamation mark beside the model.
        scale=c.size/24
        for path in c.paths:
            path['points']=[(.7*x+scale,.7*y+3*scale) for x,y in path['points']]
        c.line([(20,7),(20,14)],True,radius=0);c.circle(20,18.5,.9,True,True)
    elif key=='validation.clear-highlights':
        cube(c)
        c.line([(4,20),(20,4)],True,radius=0)
    elif key=='image.placeholder':
        box(c,3,3,18,18)
        c.line([(7,12),(17,12)],True,radius=0)
    return True
