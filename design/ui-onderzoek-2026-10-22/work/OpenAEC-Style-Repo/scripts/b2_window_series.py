"""B2 group: window chrome and side panels, backed by explicit call sites."""
DEFINITIONS=[
 ('window.minimize','Venster minimaliseren','Vensters en panelen','Het appvenster naar de taakbalk minimaliseren; geen zoom verkleinen.'),
 ('window.maximize','Venster maximaliseren','Vensters en panelen','Het appvenster maximaliseren met behoud van de vensterbediening; geen volledig-schermmodus.'),
 ('window.restore','Venster herstellen','Vensters en panelen','Een gemaximaliseerd venster herstellen naar zijn vorige afmetingen; geen document kopiëren.'),
 ('window.close','Venster sluiten','Vensters en panelen','Het appvenster sluiten, met de eigen afhandeling van niet-opgeslagen werk; geen document verwijderen of melding sluiten.'),
 ('view.fullscreen','Volledig scherm','Vensters en panelen','De weergave naar volledig-schermmodus omschakelen; geen zoom-fit of venster maximaliseren.'),
 ('view.fullscreen-exit','Volledig scherm verlaten','Vensters en panelen','Volledig-schermmodus verlaten; geen camera uitzoomen.'),
 ('panel.left','Linkerpaneel tonen of verbergen','Vensters en panelen','Het linkerzijpaneel omschakelen; actieve toestand en toegankelijk label geven de zichtbaarheid aan.'),
 ('panel.right','Rechterpaneel tonen of verbergen','Vensters en panelen','Het rechterzijpaneel omschakelen; geen documentobject verbergen.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={
 'window.minimize':'fbc558915b0a17c1','window.maximize':'65598584d714c664',
 'window.restore':'593eea7da5657819','window.close':'04dc93d8d3baf337',
 'view.fullscreen':'86a16b5135be2803','view.fullscreen-exit':'2b0b4b1f770ffb20',
 'panel.left':'ab4f9af82f3f7a8c','panel.right':'4b38be570b161300',
}


def extend(c,key):
    if key not in KEYS:return False
    if key=='window.minimize':c.line([(5,17),(19,17)])
    elif key=='window.maximize':c.line([(5,5),(19,5),(19,19),(5,19)],closed=True,radius=1.5)
    elif key=='window.restore':
        c.line([(8,7),(8,3),(21,3),(21,16),(17,16)],True,radius=1.5)
        c.line([(3,8),(16,8),(16,21),(3,21)],closed=True,radius=1.5)
    elif key=='window.close':
        c.line([(6,6),(18,18)]);c.line([(18,6),(6,18)])
    elif key=='view.fullscreen':
        c.line([(13,11),(21,3)],True)
        c.line([(15,3),(21,3),(21,9)],True,radius=1.5)
        c.line([(11,13),(3,21)])
        c.line([(3,15),(3,21),(9,21)],radius=1.5)
    elif key=='view.fullscreen-exit':
        c.line([(21,3),(13,11)],True)
        c.line([(13,5),(13,11),(19,11)],True,radius=1.5)
        c.line([(3,21),(11,13)])
        c.line([(5,13),(11,13),(11,19)],radius=1.5)
    elif key in {'panel.left','panel.right'}:
        c.line([(3,4),(21,4),(21,20),(3,20)],closed=True,radius=1.5)
        c.line([(9,4),(9,20)],True)
        if key=='panel.right':c.mirror()
    return True
