"""Large B2 review: explicit PDF and Calc actions, original vector artwork."""
import math
from b2_second_series import box
from b2_bulk_series import page
from b2_energy_pile_audio import arc_points, pencil
from b2_session_two import dimension_arrow, eraser, fill_rect
from b2_font_geometry import add_letter, font_sources

AVAILABLE_SERIES=(31,32,33,34,35,36,37,38)
GROUPS={31:'Markeringslagen',32:'Documentkoppelingen',33:'Annotatielijsten',
        34:'Tekst en stijlen',35:'Begrotingsregels',36:'Project en wijzigingsreview',
        37:'Documentuitvoer',38:'Objectstand'}
# Batch, contract, label, precise source action, record, original cluster.
ROWS=[
 (31,'layer.add','Markeringslaag toevoegen','Een benoemde annotatielaag toevoegen via addAnnotationLayer.','7e55971b72fa2d86','review.laagtoevoegen'),
 (31,'layer.raise','Laag omhoog','De geselecteerde markeringslaag één plaats omhoog in de laagvolgorde zetten.','78b78dd5326d1eb5','review.laagomhoog'),
 (31,'layer.lower','Laag omlaag','De geselecteerde markeringslaag één plaats omlaag in de laagvolgorde zetten.','b768f733819310f1','review.laagomlaag'),
 (31,'layer.assign-selection','Selectie naar laag','De geselecteerde annotaties naar de gekozen markeringslaag verplaatsen.','61c78bca4f4a3307','review.selectienaarlaag'),
 (32,'link.locate','Koppeling op pagina tonen','gotoSelectedLink gaat naar de bronpagina waarop de geselecteerde koppeling staat; niet naar de koppelingsbestemming.','60a96a7cc464a9d6','review.ganaarkoppeling'),
 (32,'link.open-external','Externe koppeling openen','De URL van de geselecteerde koppeling via openExternal openen.','29534f0dfac38a66','review.externeurlopenen'),
 (32,'link.export-list','Koppelingenlijst exporteren','De gevonden koppelingen met bronpagina en bestemming als CSV wegschrijven.','0f71baa83c3bd0f9','review.koppelingenexporteren'),
 (33,'list.group-by','Lijst groeperen','Een of meer groeperingscriteria voor een annotatie- of taaklijst kiezen; geen geometrische objecten groeperen.','6b37f45683cabf53','review.groeperenopsubmenu'),
 (33,'list.filter','Annotatielijst filteren','Via Tonen de lijst op pagina of reviewstatus filteren; documentobjecten blijven bestaan.','eb519e9bc9a45949','review.tonensubmenuopenen'),
 (33,'annotate.flatten','Annotatie vlak maken','De geselecteerde annotatie via commitAnnotationMutation als flattened markeren; geen nieuwe documentkopie maken.','8a47b0eacb68af61','review.flatten'),
 (34,'format.font-increase','Tekst groter','De tekstgrootte van de geselecteerde begrotingsregels één stap verhogen, binnen de bronlimieten.','0c16ebb6aa4ab45e','review.groter'),
 (34,'format.font-decrease','Tekst kleiner','De tekstgrootte van de geselecteerde begrotingsregels één stap verlagen, binnen de bronlimieten.','ee2f0016a652131a','review.kleiner'),
 (34,'format.clear','Tekstopmaak wissen','Vet, cursief, onderstrepen, uitlijning en grootte van begrotingsregels herstellen; tekst behouden.','3298d0533ab7f155','review.opmaakwissen'),
 (34,'format.fill-color','Vulkleur kiezen','Een vulkleur voor de selectie kiezen; bij invoegmodus en vergrendeling gelden de bronbeperkingen.','df0254789d032180','review.vulkleur'),
 (34,'format.stroke-color','Lijnkleur kiezen','De strokeColor en color van de selectie wijzigen via de lijnkleurkiezer.','334766e87fa2e7fb','review.lijnkleur'),
 (34,'style.gallery','Stijlgalerij openen','De popup met meer stijlen en opgeslagen stijlvoorinstellingen openen.','9b51020d107b1b51','review.meerstijlen'),
 (34,'style.tools','Stijlgereedschappen','Het menu met de beschikbare stijlhulpmiddelen en voorinstellingen openen; geen directe opmaakoverdracht.','f51887797d19f0bf','review.stijlgereedschappen'),
 (34,'symbol.edit-type','Symbooltype bewerken','Bij één geselecteerd symboolstempel de type-editor openen via openSymbolTypeEditor.','c6674be2fd9ca0c9','review.edittype'),
 (35,'budget.add-chapter','Hoofdstuk toevoegen','Een hoofdstuk als geschikte buur of op hoofdniveau aan de begroting toevoegen.','510e72b91f44b47b','review.hoofdstuk'),
 (35,'budget.add-item','Begrotingspost toevoegen','Een begrotingspost onder het actieve hoofdstuk of de geschikte ouder toevoegen.','c8af37557e3452f6','review.begrpost'),
 (35,'budget.add-monitor','Bewakingspost toevoegen','Een bewakingspost onder de dichtstbijzijnde begrotingspost toevoegen.','31b56ea0c97e3177','review.bewpost'),
 (35,'budget.add-formula','Rekenregel toevoegen','Via insertRegelBelow een rekenregel direct onder het actieve item invoegen.','102d083592c0f30c','review.rekenregel'),
 (35,'budget.add-text','Tekstregel toevoegen','Een tekstregel onder een geschikte begrotingscontainer toevoegen.','c9f28d6246d06dbb','review.tekstregel'),
 (35,'budget.add-blank','Witregel toevoegen','Een lege regel naast het actieve item invoegen; geen inhoud wissen.','560a3459a1ecb819','review.witregel'),
 (36,'project.properties','Projectgegevens','Een venster of pagina met projectgegevens openen; geen nieuw project maken.','da83438a351f800b','review.projectgegevens'),
 (36,'project.variants','Begrotingsvarianten','De variantenstructuur van de begroting in- of uitschakelen via toggleBranchesEnabled.','c5f6ea7e62611223','review.varianten'),
 (36,'project.option-set','Optieset maken','Een nieuwe optieset onder main met twee onderliggende opties A/B maken; varianten zo nodig inschakelen.','7a11e23fc62d3bad','review.optieset'),
 (36,'review.track-changes','Wijzigingen bijhouden','Wijzigingsregistratie van de begroting in- of uitschakelen.','5f0d04507348f2f3','review.bijhouden'),
 (36,'review.clear-marks','Wijzigingsmarkeringen wissen','De wijzigingsmarkeringen wissen via clearChangeMarks; begrotingsinhoud behouden.','947990d8cc0907e6','review.wismarkeringen'),
 (36,'review.highlight-row','Hele regel markeren','De weergave van bijgehouden wijzigingen op volledige regels instellen.','1d6402f7745fa3dd','review.heleregel'),
 (36,'review.highlight-cell','Alleen cel markeren','De weergave van bijgehouden wijzigingen beperken tot de gewijzigde cel.','dcf5b5f295e6a628','review.alleencel'),
 (37,'export.page-images','Pagina-afbeeldingen exporteren','De exportopties voor pagina-afbeeldingen openen; geen raster-PDF maken.','c6054e1c4d7831b7','review.afbeeldingenexporteren'),
 (37,'document.flatten-copy','Gevlakte kopie maken','Een afzonderlijke gevlakte PDF-kopie maken via maakGevlakteKopie; geen annotatieselectie muteren.','d74a4d328d53f0e3','review.gevlaktekopiemaken'),
 (37,'export.pdfx','PDF/X exporteren','De PDF/X-exportinstellingen met conformiteit en kleurprofiel openen; niet beschikbaar in de webvariant.','64d06550d1b6c0f9','review.pdfxexporteren'),
 (38,'object.rotate-left-90','Object 90° linksom','De geselecteerde annotatie 90 graden linksom roteren en de wijziging registreerbaar maken voor ongedaan.','3bbd87065b07bac3','review.90linksomdraaien'),
 (38,'object.rotate-right-90','Object 90° rechtsom','De geselecteerde annotatie 90 graden rechtsom roteren; geen camera of pagina draaien.','113312abf57dcb30','review.90rechtsomdraaien'),
 (38,'object.rotate-180','Object 180° draaien','De geselecteerde annotaties 180 graden roteren via rotateAnnotation.','1416fc04ca64126d','review.rotate180'),
]
ACTIVE_ROWS=[r for r in ROWS if r[0] in AVAILABLE_SERIES]
DEFINITIONS=[(key,label,GROUPS[b],meaning) for b,key,label,meaning,_,_ in ACTIVE_ROWS]
EXAMPLES={key:record for _,key,_,_,record,_ in ACTIVE_ROWS}
SOURCE_FUNCTIONS={key:source for _,key,_,_,_,source in ROWS}
SERIES={key:b for b,key,_,_,_,_ in ACTIVE_ROWS}
KEYS=set(SERIES)
REUSED={
 '0236bb54340e826b':('object.rename','beginHernoemen/renameAnnotationLayer wijzigt de laagnaam; bestaand hernoemicoon met laagscope.'),
 '6c42f916bd49df94':('edit.delete','requestDeleteAnnotationLayer verwijdert een laag en vraagt bij inhoud hoe die behandeld moet worden; scope blijft in het dialoog.'),
 '6b5b537fc04cfb5a':('edit.copy','copySelectedLink kopieert URL of bestemmingsbeschrijving naar het klembord.'),
 '7c0b0fbc125b1117':('tree.expand','expandAllGroups vouwt de annotatiegroepen uit.'),
 'd8e0f5e19bbdee4e':('tree.collapse','collapseAllGroups vouwt de annotatiegroepen in.'),
 '62c9bd6c0ed525c0':('tree.expand','De werkbalk roept dezelfde expandAll aan.'),
 '9260be4bb34facd0':('tree.collapse','De werkbalk roept dezelfde collapseAll aan.'),
 '69ac8bbccf2e3b9b':('export.raster-pdf','De backstagekaart selecteert de bestaande raster-PDF-exportroute.'),
 '746b7de9e51de6a1':('export.cad','De backstagekaart start dezelfde CAD-export; in de browser niet beschikbaar.'),
 '9d7f5c380ca6a261':('format.underline','De Calc-knop schakelt textUnderline van de geselecteerde regels om.'),
}
if 'budget.add-formula' in KEYS:
    REUSED['b01c8aa06317b201']=('budget.add-formula','De grote + Regel-knop roept dezelfde handleAddRegel/insertRegelBelow aan.')
if 'object.rotate-left-90' in KEYS:
    REUSED['ce2a4c43c1d07a4e']=('object.rotate-left-90','De lintknop roteert geselecteerde annotaties ook met -90 graden.')
ISSUES={
 '991333aa7e9a41aa':'Samenvatten in het annotatiemenu is permanent disabled en heeft geen callback; geen actieve implementatie bewezen.',
 'd2741f870c014d63':'Opmerkingen importeren in dit menu is disabled zonder callback; de afzonderlijke actieve XFDF-import is een andere bronplaats.',
 'ed6cd72ad90a9ea6':'Beide exportmenu-items zijn disabled zonder callback; dit bewijst geen actieve exportfunctie.',
}
TYPOGRAPHY={key:{**font_sources()['format.color'],
                 'icon_transform':'scale x by 0.70 about 12, move center to 8.5, translate y by +2'}
            for key in ('format.font-increase','format.font-decrease','format.clear') if key in KEYS}


def plus(c,x,y,r=2.5):
    c.line([(x-r,y),(x+r,y)],True,radius=0)
    c.line([(x,y-r),(x,y+r)],True,radius=0)


def stack(c,x=3,y=6,w=11):
    h=w/3
    c.line([(x,y),(x+w/2,y-h),(x+w,y),(x+w/2,y+h)],closed=True,radius=.3)
    c.line([(x,y+5),(x+w/2,y+5+h),(x+w,y+5)],radius=.3)


def capsule(c,a,b,r):
    angle=math.atan2(b[1]-a[1],b[0]-a[0]);points=[]
    for (x,y),start in ((b,angle-math.pi/2),(a,angle+math.pi/2)):
        for i in range(17):
            t=start+i*math.pi/16;points.append((x+r*math.cos(t),y+r*math.sin(t)))
    c.line(points,closed=True,radius=0)


def chain(c):
    # Open ends and one connecting bar avoid crossed capsule outlines.
    v=math.sqrt(2)
    for outer,inner,start in (((4.5,15.5),(7.3,12.7),45),((12.5,7.5),(9.7,10.3),225)):
        sign=1 if start==45 else -1
        points=[(inner[0]+sign*v,inner[1]+sign*v)]
        points+=arc_points(*outer,2,start,start+180)
        points.append((inner[0]-sign*v,inner[1]-sign*v))
        c.line(points,radius=0)
    c.line([(6.2,13.8),(10.8,9.2)],radius=0)


def letter(c,key):
    add_letter(c,'format.color')
    scale=c.size/24
    for fill in c.fills:
        fill['rings']=[[( (8.5+.7*(x/scale-12))*scale,y+2*scale) for x,y in ring] for ring in fill['rings']]


def miniature_eraser(c,x=19,y=17):
    c.line([(x-3,y),(x+1,y-4),(x+4,y-1),(x,y+3),(x-2,y+3)],True,closed=True,radius=.35)
    if c.size==24:c.line([(x-1,y-2),(x+2,y+1)],True,radius=0)


def row(c,y=5,accent=False):
    box(c,3,y,13,12,accent)
    c.line([(3,y+4),(16,y+4)],accent,radius=0)
    c.line([(7,y+4),(7,y+12)],accent,radius=0)


def extend(c,key):
    if key not in KEYS:return False
    if key.startswith('layer.'):
        if key=='layer.assign-selection':
            box(c,3,3,5,5);stack(c,14,14,8)
            c.line([(5.5,11),(5.5,15),(11,15)],True,radius=.8)
            c.line([(9,13),(11,15),(9,17)],True,radius=.3)
        else:
            stack(c,2,7,11)
            if key=='layer.add':plus(c,20,13)
            elif key=='layer.raise':dimension_arrow(c,(20,14),(20,5),1.5)
            else:dimension_arrow(c,(20,5),(20,14),1.5)
    elif key.startswith('link.'):
        chain(c)
        if key=='link.locate':c.line([(18,9),(21,12),(18,15)],True,radius=.3)
        elif key=='link.open-external':dimension_arrow(c,(17,16),(22,11),1.8)
        else:
            dimension_arrow(c,(20,5),(20,15),1.8)
            c.line([(16.5,18),(16.5,21),(23,21),(23,18)],True,radius=.5)
    elif key=='list.group-by':
        c.line([(4,5),(4,19)],radius=.5)
        for y in (6,17):
            c.line([(4,y),(9,y)],radius=0);box(c,10,y-3,11,6,y==17)
    elif key=='list.filter':
        c.line([(3,4),(21,4),(14,12),(14,19),(10,21),(10,12)],closed=True,radius=.6)
        c.line([(5,8),(19,8)],True,radius=0);c.clear_primary=True
    elif key=='annotate.flatten':
        c.line([(3,3),(15,3),(15,10),(9,10),(6,13),(6,10),(3,10)],closed=True,radius=.6)
        dimension_arrow(c,(20,6),(20,16),1.6)
        c.line([(3,20),(21,20)],True,radius=0)
    elif key in {'format.font-increase','format.font-decrease','format.clear'}:
        letter(c,key)
        if key=='format.font-increase':plus(c,20,10)
        elif key=='format.font-decrease':c.line([(17.5,10),(22.5,10)],True,radius=0)
        else:miniature_eraser(c)
    elif key=='format.fill-color':
        box(c,3,3,18,14);fill_rect(c,6,6,12,8,True)
        c.line([(5,22),(19,22)],True,radius=0)
    elif key=='format.stroke-color':
        box(c,4,3,16,14,True);c.line([(5,22),(19,22)],radius=0)
    elif key=='style.gallery':
        for x,y in ((3,3),(14,3),(3,14),(14,14)):
            box(c,x,y,7,7,x==14 and y==14)
        c.line([(5,7),(8,7)],radius=0)
        c.line([(16,5),(19,8)],radius=0)
    elif key=='style.tools':
        box(c,3,3,14,6)
        c.line([(17,6),(21,6),(21,13),(11,13),(11,16)],radius=.8)
        box(c,9,18,4,4,True)
        fill_rect(c,9.5,18.5,3,3,True)
    elif key=='symbol.edit-type':
        # Equal projected edges, shared vertices and a true isometric top face.
        c.line([(2,6),(7,3.113),(12,6),(12,11.774),(7,14.66),(2,11.774)],closed=True,radius=.2)
        c.line([(2,6),(7,8.887),(12,6)],radius=0)
        c.line([(7,8.887),(7,14.66)],radius=0)
        pencil(c)
    elif key.startswith('budget.'):
        row(c)
        plus(c,21,12,2)
        if key=='budget.add-chapter':
            fill_rect(c,4.4,6.4,10.2,1.2,True)
        elif key=='budget.add-item':
            c.line([(8,13),(14,13)],True,radius=0)
        elif key=='budget.add-monitor':
            c.line([(9,13),(10.5,14.5),(14,11)],True,radius=0)
        elif key=='budget.add-formula':
            c.line([(9,11),(14,11)],True,radius=0);c.line([(9,14),(14,14)],True,radius=0)
        elif key=='budget.add-text':
            c.line([(9,11),(14,11)],True,radius=0);c.line([(11.5,11),(11.5,15)],True,radius=0)
        else:
            c.line([(8,21),(14,21)],True,radius=0)
    elif key=='project.properties':
        # Project folder with an information badge.
        c.line([(3,19),(3,5),(9,5),(11,8),(21,8),(21,11)],radius=.7)
        c.line([(3,19),(10,19)],radius=0)
        c.circle(17,17,5,True)
        c.circle(17,14.7,.55,True,True)
        c.line([(17,17),(17,19.5)],True,radius=0)
    elif key in {'project.variants','project.option-set'}:
        c.line([(4,3),(4,20),(16,20)],radius=.7)
        c.line([(4,7),(16,7)],radius=.7)
        for y in (7,20):c.circle(19,y,2.2,True)
        c.circle(4,3,1.2,filled=True)
        if key=='project.option-set':
            plus(c,11,13,2.3)
    elif key=='review.track-changes':
        page(c,3,3,12,18)
        for y in (8,13,18):c.line([(6,y),(11,y)],radius=0)
        # Margin marks identify changed rows without suggesting navigation.
        for y in (8,18):c.line([(20,y-1.5),(20,y+1.5)],True,radius=0)
    elif key=='review.clear-marks':
        page(c,3,3,12,18)
        for y in (7,11,15):c.line([(6,y),(11,y)],radius=0)
        miniature_eraser(c,19,17)
    elif key in {'review.highlight-row','review.highlight-cell'}:
        box(c,3,3,18,18)
        for y in (9,15):c.line([(3,y),(21,y)],radius=0)
        for x in (9,15):c.line([(x,3),(x,21)],radius=0)
        fill_rect(c,4,10,16 if key.endswith('row') else 4,4,True)
        c.clear_primary=True
    elif key=='export.page-images':
        box(c,2,4,13,16);c.circle(6,8,1,filled=True)
        c.line([(4,17),(8,11),(13,17)],radius=.4)
        dimension_arrow(c,(18,12),(23,12),1.8)
    elif key=='document.flatten-copy':
        stack(c,3,7,13)
        c.line([(3,21),(16,21)],True,radius=0)
        dimension_arrow(c,(21,7),(21,17),1.8)
    elif key=='export.pdfx':
        page(c,3,3,11,18)
        c.line([(6,10),(11,16)],radius=0);c.line([(6,16),(11,10)],radius=0)
        dimension_arrow(c,(17,12),(22,12),1.8)
    elif key in {'object.rotate-left-90','object.rotate-right-90','object.rotate-180'}:
        box(c,8,12,8,9)
        if key=='object.rotate-180':
            c.line(arc_points(12,11,8,180,360),True,radius=0)
            dimension_arrow(c,(20,11),(20,16),1.6)
        else:
            c.line(arc_points(12,12,8,180,270)+[(15,4)],True,radius=0)
            c.line([(12,1.5),(15,4),(12,6.5)],True,radius=.35)
            if key=='object.rotate-left-90':c.mirror()
    return True
