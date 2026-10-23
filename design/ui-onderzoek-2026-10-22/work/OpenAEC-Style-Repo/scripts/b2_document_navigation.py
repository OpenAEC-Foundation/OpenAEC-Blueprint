"""Original B2 document navigation designs, backed by pinned PDF callbacks."""
from b2_energy_pile_audio import pencil
import math
from b2_session_two import dimension_arrow

AVAILABLE_SERIES=(29,30)
GROUPS={29:'Bladwijzers',30:'Bijlagen'}
ROWS=[
 (29,'bookmark.navigate','Naar bladwijzer','Een documentbladwijzer selecteren en naar de opgeslagen bestemming navigeren.','53366c4288a590aa','review.bladwijzerinlijst'),
 (29,'bookmark.add','Bladwijzer toevoegen','Een bladwijzer met titel en paginabestemming toevoegen.','a96bbe8de026f8b2','review.bladwijzertoevoegen'),
 (29,'bookmark.add-child','Onderliggende bladwijzer','Een bladwijzer onder de geselecteerde ouder toevoegen.','8c8f77919f549b8e','review.onderliggendebladwijzer'),
 (29,'bookmark.edit','Bladwijzer bewerken','Titel en paginabestemming van de geselecteerde bladwijzer wijzigen.','88827c1ff02e2c3b','review.bladwijzerbewerken'),
 (30,'attachment.add','Bijlage toevoegen','Een of meer bestanden in het actieve PDF-document insluiten.','e949501ca30f6eea','review.bijlagetoevoegen'),
 (30,'attachment.open','Bijlage openen','Een ingesloten bijlage buiten het document openen; geen PDF openen in het huidige werkvlak.','7e549f62fd462e1f','review.bijlageopenen'),
 (30,'attachment.save','Bijlage opslaan','De geselecteerde ingesloten bijlage als afzonderlijk bestand wegschrijven.','7407f648cb9790b2','review.bijlageopslaan'),
 (30,'attachment.save-all','Alle bijlagen opslaan','Alle ingesloten bijlagen afzonderlijk wegschrijven; geen ZIP of document opslaan.','6c1504f63d04134f','review.allebijlagenopslaan'),
]
DEFINITIONS=[(key,label,GROUPS[batch],meaning) for batch,key,label,meaning,_,_ in ROWS]
EXAMPLES={key:record for _,key,_,_,record,_ in ROWS}
SOURCE_FUNCTIONS={key:source for _,key,_,_,_,source in ROWS}
SERIES={key:batch for batch,key,_,_,_,_ in ROWS}
KEYS=set(SERIES)
REUSED={
 '8f611ae377ad1c3a':('edit.delete','deleteBookmark verwijdert de geselecteerde bladwijzer; bij kinderen vraagt de bron bevestiging. Bestaand verwijdericoon, expliciete scope in het label.'),
 '089ef08478613625':('edit.delete','deleteSelectedAttachment verwijdert de geselecteerde ingesloten bijlage; bestaand verwijdericoon met bijlage als scope.'),
}


def bookmark(c,x,y,w,h,accent=False):
    c.line([(x,y),(x+w,y),(x+w,y+h),(x+w/2,y+h-3),(x,y+h)],
           accent,closed=True,radius=.5)


def paperclip(c):
    # One continuous wire: concentric lower bends and a round upper return.
    # Rotate the construction before fitting it beside the action badge.
    points=[(3,5.5),(3,12)]
    for cx,cy,r,start,stop,end in [
            (5,12,2,180,0,(7,3.5)),
            (3.5,3.5,3.5,0,-180,(0,12)),
            (5,12,5,180,0,(10,5.5))]:
        for step in range(1,25):
            angle=math.radians(start+(stop-start)*step/24)
            points.append((cx+r*math.cos(angle),cy+r*math.sin(angle)))
        points.append(end)
    cosine,sine=math.cos(math.pi/6),math.sin(math.pi/6)
    points=[(cosine*x-sine*y,sine*x+cosine*y) for x,y in points]
    xs,ys=zip(*points)
    scale=min(12/(max(xs)-min(xs)),18/(max(ys)-min(ys)))
    cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2
    c.line([(8.5+(x-cx)*scale,12+(y-cy)*scale) for x,y in points],radius=0)


def extend(c,key):
    if key not in KEYS:return False
    if key=='bookmark.navigate':bookmark(c,6,3,12,18)
    elif key=='bookmark.add':
        bookmark(c,3,3,10,18)
        c.line([(20,10),(20,16)],True,radius=0)
        c.line([(17,13),(23,13)],True,radius=0)
    elif key=='bookmark.add-child':
        bookmark(c,3,3,8,10)
        bookmark(c,13,11,8,10,True)
        c.line([(6,15),(6,18),(10,18)],radius=.5)
    elif key=='bookmark.edit':
        bookmark(c,3,3,9,18)
        pencil(c)
    else:
        paperclip(c)
        if key=='attachment.add':
            c.line([(20,10),(20,16)],True,radius=0)
            c.line([(17,13),(23,13)],True,radius=0)
        elif key=='attachment.open':dimension_arrow(c,(17,16),(22,11),1.8)
        else:
            dimension_arrow(c,(20,5),(20,15),1.8)
            c.line([(16.5,18),(16.5,21),(23,21),(23,18)],True,radius=.5)
            if key=='attachment.save-all':c.line([(16.5,23),(23,23)],True,radius=0)
    return True
