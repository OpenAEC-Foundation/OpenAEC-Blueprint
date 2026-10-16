"""B2 text formatting; no automatic mapping of object or screen colours."""
from b2_font_geometry import add_letter

DEFINITIONS=[
 ('format.bold','Vet','Tekstopmaak','Vette tekstopmaak aan- of uitzetten; de actieve knoptoestand toont de huidige opmaak.'),
 ('format.italic','Cursief','Tekstopmaak','Cursieve tekstopmaak aan- of uitzetten; geen object schuin trekken.'),
 ('format.underline','Onderstrepen','Tekstopmaak','Tekst onderstrepen; geen losse lijn in een tekening plaatsen.'),
 ('format.color','Tekstkleur','Tekstopmaak','Tekstkleur kiezen; schermkleuren en resourceaccenten blijven apart. Ontwerpcontract zonder passend bronvoorbeeld in dit cluster.'),
 ('format.align-left','Tekst links uitlijnen','Tekstopmaak','Tekst links uitlijnen; geen objecten langs een verticale as uitlijnen.'),
 ('format.align-center','Tekst centreren','Tekstopmaak','Tekst horizontaal centreren; geen camerabeweging of objectuitlijning.'),
 ('format.align-right','Tekst rechts uitlijnen','Tekstopmaak','Tekst rechts uitlijnen; geen objecten langs een verticale as uitlijnen.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={'format.bold':'485d005b0655b83e','format.italic':'d2dfb4f78372196e',
          'format.underline':'1b6102e6763b8da3','format.align-left':'5f6da723e9649ea1',
          'format.align-center':'b866cd644d76b02e','format.align-right':'d57800951d0f5fc6'}
ISSUES={'8c3f19a230ed0a8b':'Resourceaccenten tonen/verbergen is geen tekstkleur kiezen.',
        'aba618d721e22e4c':'Schermkleuren instellen is geen tekstkleur kiezen.'}


def extend(c,key):
    if key not in KEYS:return False
    if key in {'format.bold','format.italic','format.underline','format.color'}:
        add_letter(c,key)
        if key=='format.underline':c.line([(5,21),(19,21)],True)
        if key=='format.color':c.line([(4,21),(20,21)],True)
    elif key.startswith('format.align-'):
        short={'format.align-left':(4,14),'format.align-center':(7,17),'format.align-right':(10,20)}[key]
        c.line([(4,5),(20,5)]);c.line([(short[0],10),(short[1],10)],True)
        c.line([(4,15),(20,15)]);c.line([(short[0],20),(short[1],20)],True)
    return True
