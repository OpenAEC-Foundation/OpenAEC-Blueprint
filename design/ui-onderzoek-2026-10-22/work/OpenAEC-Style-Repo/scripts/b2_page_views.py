"""Page navigation and display modes from PDF's inspected status bar."""
from b2_second_series import box
from b2_energy_pile_audio import arc_points

DEFINITIONS=[
 ('page.first','Eerste pagina','Paginanavigatie en weergaven','Naar de eerste pagina of het eerste vel in de document- of afdrukvoorbeeldweergave gaan; geen startpagina van de app.'),
 ('page.previous','Vorige pagina','Paginanavigatie en weergaven','Eén pagina of afdrukvoorbeeldvel teruggaan; geen navigatiegeschiedenis of ongedaan maken. Spiegelen bij rechts-naar-links lezen gebeurt in de app.'),
 ('page.next','Volgende pagina','Paginanavigatie en weergaven','Eén pagina of afdrukvoorbeeldvel vooruitgaan; geen navigatiegeschiedenis of opnieuw uitvoeren. Spiegelen bij rechts-naar-links lezen gebeurt in de app.'),
 ('page.last','Laatste pagina','Paginanavigatie en weergaven','Naar de laatste pagina of het laatste vel in de document- of afdrukvoorbeeldweergave gaan; geen export of download.'),
 ('page.view-single','Enkele pagina','Paginanavigatie en weergaven','Eén pagina tegelijk tonen; geen nieuwe pagina toevoegen.'),
 ('page.view-continuous','Doorlopende pagina’s','Paginanavigatie en weergaven','Pagina’s onder elkaar in een doorlopende documentweergave tonen.'),
 ('page.view-book','Boekweergave','Paginanavigatie en weergaven','Een doorlopende boekweergave met bookSpread activeren. Dit is een andere modus dan één dubbele pagina tegelijk.'),
 ('page.view-facing','Dubbele pagina','Paginanavigatie en weergaven','Eén spread tegelijk tonen en per spread bladeren met facingSpread; niet de doorlopende boekweergave.'),
 ('page.reset-view-rotation','Weergavedraaiing herstellen','Paginanavigatie en weergaven','De tijdelijke weergaverotatie op nul zetten via zetWeergaveRotatie(0); de documentpagina zelf wordt niet gedraaid.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={
 'page.first':'15c06fa62fa81ede','page.previous':'c5bb624c9a81d757',
 'page.next':'5459720ea86e2b16','page.last':'93ad43a8dc62d06a',
 'page.view-single':'6e11f7a8bdd0c036','page.view-continuous':'9706adeb60881248',
 'page.view-book':'0e25d25d9df0674a','page.view-facing':'1ff23532c124ca93',
 'page.reset-view-rotation':'dc4927e3d65bd320',
}
SOURCE_FUNCTIONS={
 'page.first':'review.eerstepagina','page.previous':'review.vorigepagina',
 'page.next':'review.volgendepagina','page.last':'review.laatstepagina',
 'page.view-single':'review.enkelepagina','page.view-continuous':'review.doorlopend',
 'page.view-book':'review.tweepaginas','page.view-facing':'review.tweepaginasnaastelkaar',
 'page.reset-view-rotation':'review.draaiingherstellen',
}
REUSED={
 'bd962e179ffaae69':('view.zoom-out','PDF-statusbalk roept handleZoomOut aan; gebruikt het bestaande Uitzoomen-ontwerp.'),
 '8c6f5325bb242e63':('view.zoom-in','PDF-statusbalk roept handleZoomIn aan; gebruikt het bestaande Inzoomen-ontwerp.'),
}

def extend(c,key):
    if key not in KEYS:return False
    if key in {'page.first','page.last'}:
        c.line([(5,5),(5,19)],True)
        c.line([(16,6),(10,12),(16,18)],radius=1)
        if key=='page.last':c.mirror()
    elif key in {'page.previous','page.next'}:
        c.line([(15,6),(9,12),(15,18)],radius=1)
        if key=='page.next':c.mirror()
    elif key=='page.view-single':
        box(c,6,3,12,18)
        for y in (9,15):c.line([(10,y),(14,y)],True)
    elif key=='page.view-continuous':
        box(c,6,2,12,8.5);box(c,6,13.5,12,8.5,True)
    elif key=='page.view-book':
        box(c,3,4,7,16);box(c,14,4,7,16,True)
    elif key=='page.view-facing':
        box(c,3,4,18,16)
        c.line([(12,5),(12,19)],True)
    elif key=='page.reset-view-rotation':
        box(c,9,8,6,8)
        c.line(arc_points(12,12,8,90,360),True,radius=0)
        c.line([(17.5,9),(20,12),(22.5,9)],True,radius=.6)
    return True
