"""Second B2 series: original UI geometry and explicit function contracts."""
import math

DEFINITIONS=[
 ('draw.line','Lijn tekenen','Tekenen','Een recht lijnsegment plaatsen; geen afbeelding verwijderen.'),
 ('draw.polyline','Polylijn tekenen','Tekenen','Een open keten van verbonden lijnsegmenten tekenen.'),
 ('draw.polygon','Veelhoek tekenen','Tekenen','Een gesloten veelhoek tekenen; apart van een open polylijn.'),
 ('draw.rectangle','Rechthoek tekenen','Tekenen','Een rechthoekige geometrie of annotatie plaatsen; geen selectiekader.'),
 ('draw.circle','Cirkel tekenen','Tekenen','Een cirkelvormige geometrie of annotatie plaatsen.'),
 ('draw.arc','Boog tekenen','Tekenen','Een open cirkelboog tekenen; geen volledige cirkel of rotatieopdracht.'),
 ('draw.text','Tekst toevoegen','Tekenen','Vrije tekst plaatsen; geen bestaand tekstveld bewerken.'),
 ('draw.textbox','Tekstvak toevoegen','Tekenen','Tekst als omkaderde annotatie plaatsen; apart van vrije tekst.'),
 ('draw.leader','Leidlijn plaatsen','Tekenen','Een bijschrift met een verwijzende leidlijn plaatsen.'),
 ('draw.dimension','Maatlijn plaatsen','Tekenen','Een blijvende maatannotatie plaatsen; geen tijdelijke afstandsmeting.'),
 ('measure.area','Oppervlakte meten','Annoteren en meten','De oppervlakte van een begrensd vlak meten; geen afstand of omtrek.'),
 ('transform.move','Object verplaatsen','Transformeren','Geselecteerde objecten verplaatsen; geen camera-pan.'),
 ('transform.rotate','Object roteren','Transformeren','De geometrie van een object roteren; geen 3D-camera draaien.'),
 ('transform.mirror','Spiegelen','Transformeren','Objecten spiegelen ten opzichte van een as.'),
 ('transform.offset','Evenwijdige kopie','Transformeren','Een parallelle kopie op een afstand maken; geen gewone verplaatsing.'),
 ('transform.trim','Inkorten tot grens','Transformeren','Een object inkorten tot een snijgrens; geen klembord-knipopdracht.'),
 ('transform.extend','Verlengen tot grens','Transformeren','Een object verlengen tot een snijgrens; lengte wijzigen blijft apart te beoordelen.'),
 ('object.layers','Lagen','Objecten en lagen','Lagen voor documentobjecten beheren; geen constructiecatalogus, groepering of BIM-export.'),
 ('object.lock','Vergrendelen','Objecten en lagen','Objecten tegen wijziging vergrendelen; geen algemene alleen-lezen-veiligheidsmodus.'),
 ('object.unlock','Ontgrendelen','Objecten en lagen','Objectvergrendeling opheffen; de scope (selectie/alles) staat in het label.'),
 ('object.show','Zichtbaar maken','Objecten en lagen','Documentobjecten zichtbaar maken; geen paneel tonen, zoomreset of geheim token onthullen.'),
 ('object.hide','Verbergen','Objecten en lagen','Documentobjecten verbergen; geen paneel sluiten of geheim token verbergen.'),
 ('object.align-left','Links uitlijnen','Objecten en lagen','Objecten links uitlijnen; tekstuitlijning niet automatisch koppelen.'),
 ('object.align-center','Horizontaal centreren','Objecten en lagen','Objecten horizontaal op hun middellijn uitlijnen; geen tekstuitlijning of camera-fit.'),
 ('object.align-right','Rechts uitlijnen','Objecten en lagen','Objecten rechts uitlijnen; tekstuitlijning niet automatisch koppelen.'),
 ('view.grid','Raster tonen','Objecten en lagen','Het werkvlak-raster tonen of verbergen; geen venster tekenen of tegelweergave kiezen.'),
 ('status.info','Informatie','Status en meldingen','Een informatieve melding aanduiden; geen knop Over deze app. Nieuw contract voor componenten 2.4.'),
 ('status.warning','Waarschuwing','Status en meldingen','Een waarschuwing aanduiden; label en statuskleur benoemen de ernst.'),
 ('status.error','Fout','Status en meldingen','Een foutmelding aanduiden; geen opdracht sluiten of selectie verwijderen.'),
 ('status.success','Geslaagd','Status en meldingen','Een geslaagde of bevestigde toestand aanduiden; geen zelfstandige bevestigingsopdracht.'),
 ('status.busy','Bezig','Status en meldingen','Lopende verwerking aanduiden. Statische SVG; de host verzorgt eventuele animatie en toegankelijkheid.'),
 ('ui.settings','Instellingen','Instellingen en hulp','Algemene voorkeuren openen; geen hoeveelheden of prijspercentage instellen.'),
 ('ui.help','Hulp','Instellingen en hulp','Hulp openen; geen onbeschikbaarheid van een rekenkern aanduiden.'),
 ('ui.refresh','Vernieuwen','Instellingen en hulp','Een lijst of gegevens opnieuw laden; geen berekening opnieuw uitvoeren of object roteren.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={
 'draw.line':'2133612eced155e1','draw.polyline':'aa04624ea72e9ea5','draw.polygon':'af08bcabc2283f76',
 'draw.rectangle':'95ccf21cd554b245','draw.circle':'26ad61afad9b4040','draw.arc':'c27d69478528b782',
 'draw.text':'3268b58b6e58ac3f','draw.textbox':'d7d2e85b145344a6','draw.leader':'a5b3c5e14febc2ba',
 'measure.area':'0442472ef2b4b307','transform.move':'81436d845ad9caed','transform.rotate':'51ca1e5af4e7ff47',
 'transform.offset':'aa230d5a558eaaab','transform.trim':'f8992bbd2c7ecbf6','transform.extend':'7eadf1d67a20d341',
 'object.layers':'27316432f31205ea','object.lock':'67aac612a6709193','object.unlock':'fd8edd666479305a',
 'object.show':'39b39516536df9f2','object.hide':'a2e98429959e27de','object.align-left':'a35d9c41ff496c46',
 'view.grid':'dc9672b01fccfa68','status.warning':'d1cf142d3f09982c','status.error':'0cb2e9fb4a985e37',
 'status.success':'efe195ff39fd7e31','status.busy':'7069f4fe3e07499e',
 'ui.settings':'be6a0fcceef5deb8','ui.help':'d1bee27b9756bff7','ui.refresh':'d6f4ae10d7f17297',
}
ISSUES={
 '92144aca8d87de21':'Afbeelding verwijderen/bewerken; geen lijn tekenen.',
 '0cc80121d0b1fb17':'Hoeveelheden tonen; geen algemene instellingen.',
 'ba9379eeeeb59cce':'Prijspercentage wijzigen; geen algemene instellingen.',
 'cedd5304a944cc34':'Berekenen; geen gegevenslijst vernieuwen.',
 '99a5942975a19def':'Rotatievorm zonder bewezen vernieuw-opdracht; niet automatisch koppelen.',
 '340b258e362ba15e':'Vloertype/bouwdeel; geen documentlagen beheren.',
 '85027d5edbf3fff6':'Groeperen in planning; geen documentlagen beheren.',
 '62721a140f3d9750':'BCF-export; geen lagen beheren.',
 'ca9ea487822b769a':'Zoomreset; geen object zichtbaar maken.',
 'a5336be6274e59b3':'Geheim token verbergen; geen objectzichtbaarheid.',
 'fb3f86f1255aed40':'Venster tekenen; geen werkvlak-raster tonen.',
 '3a26991f069be001':'Lengte aanpassen is niet hetzelfde als verlengen tot een snijgrens.',
}
SEMANTIC={'status.info':'info','status.warning':'warning','status.error':'error',
          'status.success':'success','status.busy':'text-secondary'}
ACCENT_FRONT={k:'Het accent markeert een bedienbaar knooppunt boven de lijn.' for k in
              ('draw.line','draw.polyline','draw.polygon','draw.rectangle','draw.arc')}
ACCENT_FRONT.update({'draw.dimension':'Pijlpunten en hulplijnen staan vrij van elkaar.',
                    'draw.text':'De T heeft één hoofdkleur; geheel accent kan via de kleurrol.',
                    'transform.move':'Het centrale aangrijppunt blijft volledig zichtbaar.',
                    'object.hide':'De schuine streep blijft vóór het oog zichtbaar.',
                    'ui.settings':'De schuifknop ligt vóór de rail.'})


def arc(c,x,y,r,start,end,accent=False):
    steps=max(16,round(abs(end-start)/4))
    return c.line([(x+r*math.cos(math.radians(start+(end-start)*i/steps)),
                    y+r*math.sin(math.radians(start+(end-start)*i/steps))) for i in range(steps+1)],accent,radius=0)


def cubic(c,points,accent=False):
    a,b,d,e=points
    return c.line([tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*d[j]+t**3*e[j] for j in (0,1)) for t in [i/32 for i in range(33)]],accent,radius=0)


def box(c,x,y,w,h,accent=False):
    # Keep straight, aligned sides; only the corner itself is softened.
    return c.line([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],accent,True,radius=1.5)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='draw.line':
        c.line([(4,19),(20,5)],radius=0)
        for x,y in [(4,19),(20,5)]:c.circle(x,y,1.5,True,True)
    elif key in {'draw.polyline','draw.polygon'}:
        pts=([(5,19),(5,5),(19,5),(19,19)] if key=='draw.polyline' else
             [(4,12),(8,5),(16,5),(20,12),(16,19),(8,19)])
        c.line(pts,closed=key=='draw.polygon',radius=1)
        for x,y in (pts[1:3] if small else pts):c.circle(x,y,1.35,True,True)
    elif key=='draw.rectangle':
        box(c,4,4,16,16)
        for x,y in [(4,4),(20,4),(20,20),(4,20)]:c.circle(x,y,1.35,True,True)
    elif key=='draw.circle':
        c.circle(12,12,7.5);c.line([(12,12),(17.3033,6.6967)],True)
    elif key=='draw.arc':
        arc(c,5,5,14,0,90)
        c.circle(19,5,1.4,True,True);c.circle(5,19,1.4,True,True)
        if not small:c.plus(5,5,1.4,False)
    elif key=='draw.text':
        c.line([(5,5),(19,5)]);c.line([(12,5),(12,20)])
    elif key=='draw.textbox':
        box(c,3,4,18,16);c.line([(8,8),(16,8)],True);c.line([(12,8),(12,17)],True)
    elif key=='draw.leader':
        box(c,12,3,9,7)
        c.line([(16,10),(16,15),(4,20)],True)
        c.line([(5,16),(4,20),(8,20)],True,radius=1)
    elif key=='draw.dimension':
        for x in (2,22):c.line([(x,4),(x,21)])
        c.line([(5,12),(19,12)],True)
        c.line([(8,9),(5,12),(8,15)],True,radius=1)
        c.line([(16,9),(19,12),(16,15)],True,radius=1)
    elif key=='measure.area':
        box(c,4,4,16,16)
        for a,b in [((4,12),(12,4)),((5.5,18.5),(18.5,5.5)),((12,20),(20,12))]:c.line([a,b],True,radius=0)
    elif key=='transform.move':
        c.line([(12,3),(12,21)]);c.line([(3,12),(21,12)])
        for p in [[(9,6),(12,3),(15,6)],[(9,18),(12,21),(15,18)],[(6,9),(3,12),(6,15)],[(18,9),(21,12),(18,15)]]:c.line(p,radius=1)
        c.circle(12,12,1.6,True,True)
    elif key=='transform.rotate':
        box(c,7,11,9,9)
        arc(c,12,12,9,210,330,True)
        c.line([(16.5,7.5),(19.79,7.5),(20.3,4.3)],True,radius=1)
    elif key=='transform.mirror':
        for a,b in [(3,7),(10,14),(17,21)]:c.line([(12,a),(12,b)],True)
        c.line([(3,18),(3,7),(9,18)],closed=True,radius=.7)
        c.line([(21,18),(21,7),(15,18)],closed=True,radius=.7)
    elif key=='transform.offset':
        c.line([(4,17),(4,6),(17,6)],radius=1.3)
        c.line([(8,21),(8,10),(21,10)],True,radius=1.3)
    elif key=='transform.trim':
        c.line([(15,3),(15,21)])
        c.line([(3,12),(15,12)],True)
    elif key=='transform.extend':
        c.line([(20,3),(20,21)]);c.line([(3,12),(10,12)])
        c.line([(10,12),(20,12)],True)
        c.line([(17,9),(20,12),(17,15)],True,radius=1)
    elif key=='object.layers':
        c.line([(3,7),(12,3),(21,7),(12,11)],True,True,radius=1.2)
        for y in ([17] if small else [12,17]):c.line([(3,y),(12,y+4),(21,y)],radius=1.2)
    elif key in {'object.lock','object.unlock'}:
        box(c,5,10,14,11)
        if key=='object.lock':c.line([(8,10),(8,4),(16,4),(16,10)],radius=3)
        else:c.line([(8,10),(8,4),(16,4),(16,7)],radius=3)
        c.circle(12,14,1.2,True,True);c.line([(12,14),(12,17)],True)
    elif key in {'object.show','object.hide'}:
        top=[(3,12),(7,4),(17,4),(21,12)]
        bottom=[(21,12),(17,20),(7,20),(3,12)]
        cubic(c,top);cubic(c,bottom)
        c.circle(12,12,2.7,key=='object.show',key=='object.show')
        if key=='object.hide':c.line([(3,3),(21,21)],True,radius=0)
    elif key.startswith('object.align-'):
        if key=='object.align-left':
            c.line([(4,3),(4,21)],True);c.line([(8,7),(20,7)]);c.line([(8,16),(15,16)])
        elif key=='object.align-right':
            c.line([(20,3),(20,21)],True);c.line([(4,7),(16,7)]);c.line([(9,16),(16,16)])
        else:
            for a,b in [(3,5),(9,14),(18,21)]:c.line([(12,a),(12,b)])
            c.line([(5,7),(19,7)],True);c.line([(8,16),(16,16)])
    elif key=='view.grid':
        box(c,4,4,16,16)
        nodes=[12] if small else [9.3333,14.6667]
        for p in nodes:c.line([(p,4),(p,20)],True);c.line([(4,p),(20,p)],True)
    elif key=='ui.settings':
        specs=[(6,9),(12,15),(18,8)]
        for i,(x,y) in enumerate(specs):
            c.line([(x,3),(x,y-3)]);c.line([(x,y+3),(x,21)])
            c.circle(x,y,2.2 if small else 2.5,True)
    elif key=='ui.help':
        c.circle(12,12,9)
        cubic(c,[(8.5,8.5),(8.5,4),(17,4),(16,8.5)],True)
        cubic(c,[(16,8.5),(15.5,10.5),(12,10.5),(12,14)],True)
        c.circle(12,18,.85,True,True)
        # Scale only the question mark; keep its stroke weight and outer ring.
        center=c.size/2
        for path in c.paths:
            path['points']=[(center+(x-center)*.8,center+(y-center)*.8) for x,y in path['points']]
        dot=c.circles[-1]
        dot['x']=center+(dot['x']-center)*.8
        dot['y']=center+(dot['y']-center)*.8
        dot['r']*=.8
    elif key=='ui.refresh':
        arc(c,12,12,7,210,330,True);arc(c,12,12,7,30,150)
        c.line([(14.7,8.5),(18.06,8.5),(18.06,5.2)],True,radius=1)
        c.line([(9.3,15.5),(5.94,15.5),(5.94,18.8)],radius=1)
    elif key=='status.busy':arc(c,12,12,8.5,-90,180)
    elif key=='status.warning':
        c.line([(12,3),(22,21),(2,21)],closed=True,radius=2)
        c.line([(12,9),(12,14)]);c.circle(12,17.5,.8,filled=True)
    elif key in {'status.info','status.error','status.success'}:
        c.circle(12,12,9)
        if key=='status.info':
            c.circle(12,7,.9,filled=True);c.line([(12,10),(12,17)]);c.line([(10,17),(14,17)])
        elif key=='status.error':
            c.line([(8,8),(16,16)]);c.line([(16,8),(8,16)])
        else:c.line([(7,12),(10.5,15.5),(17,8.5)],radius=1)
    return True


def lightning(c,x=12.5,y=12.5,w=8,h=15,accent=True):
    points=[(.65,0),(0,.57),(.42,.57),(.32,1),(1,.38),(.58,.38)]
    scale=c.size/24
    c.fills.append({'tone':'accent' if accent else 'primary','rings':[[((x-w/2+u*w)*scale,(y-h/2+v*h)*scale) for u,v in points]]})
