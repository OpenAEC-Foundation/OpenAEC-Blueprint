"""Thermal-import stages, pile-plan actions and speech workspace routes."""
from b2_second_series import box

DEFINITIONS=[
 ('thermal.openings','Openingen controleren','Energie en warmte','De stap Openingen in de thermische import aanduiden; geen deur tekenen. Het icoon is een stapindicator.'),
 ('thermal.summary','Importsamenvatting','Energie en warmte','De samenvattingsstap van de thermische import aanduiden; geen algemene succesmelding.'),
 ('thermal.door','Deur plaatsen','Energie en warmte','Het deurgereedschap in de Heatloss-modelleur activeren; apart van de importstap Openingen.'),
 ('pile.new','Nieuw paalplan','Paalplan','Een paalplan binnen het project toevoegen; geen nieuw projectbestand.'),
 ('object.rename','Object hernoemen','Naam en eigenschappen','De naam van een bestaand object, persoonlijk taaktype of lokaal objectconcept wijzigen; geen extra exemplaar maken of Opslaan als.'),
 ('pile.legend-edit','Legenda bewerken','Paalplan','De legenda-editor openen om codering van paaltypen te wijzigen.'),
 ('pile.legend-used','Gebruikte typen activeren','Paalplan','Alleen de gebruikte paaltypen in de legenda activeren; geen algemene filterweergave.'),
 ('pile.columns','Paalkolommen kiezen','Paalplan','Kiezen welke kolommen bij de paalopties worden getoond; geen tabelgegevens invoegen.'),
 ('pile.combined','Gecombineerd paneel','Paalplan','De gecombineerde weergave van het rechterpaneel kiezen; geen document dupliceren.'),
 ('pile.encoding-conflicts','Coderingsconflicten bekijken','Paalplan','De details van dubbel gebruikte symbolen en kleuren openen; geen automatische foutcorrectie.'),
 ('audio.speech','Spraakwerkruimte','Spraak en audio','De spraakwerkruimte openen; deze knop start geen opname.'),
 ('audio.transcribe','Transcriptiewerkruimte','Spraak en audio','De werkruimte voor bestandstranscriptie openen; deze knop start geen transcriptietaak.'),
 ('audio.meeting','Vergaderwerkruimte','Spraak en audio','De vergaderwerkruimte openen; geen afspraak plannen of opname direct starten.'),
 ('audio.mic-test','Microfoon testen','Spraak en audio','De microfoontest openen; geen algemene medische hartslagmeting.'),
 ('audio.tts','Tekst naar spraak','Spraak en audio','De tekst-naar-spraakwerkruimte openen; geen geluidsvolume instellen.'),
]
KEYS={d[0] for d in DEFINITIONS}
SERIES={key:11 if group=='Energie en warmte' else 12 if group=='Paalplan' else 13 for key,_,group,_ in DEFINITIONS}
EXAMPLES={
 'thermal.openings':'b55e8c56aa05fd5c','thermal.summary':'0ed7e30ccbd9afd2','thermal.door':'a00d326fccecda27',
 'pile.new':'dacd58c5f114c5ca','object.rename':'bf1978a13618af79',
 'pile.legend-edit':'d2a6e42779404bda','pile.legend-used':'4aa4c8deab0b363d',
 'pile.columns':'bdcda7ee65dfabba','pile.combined':'5acedfc9f2109ddc','pile.encoding-conflicts':'be1587471e1c4c80',
 'audio.speech':'302fa478c570babe','audio.transcribe':'60bcbb4ca7faf64f','audio.meeting':'1f31715621c0f8e8',
 'audio.mic-test':'d9d10bdd0f23c650','audio.tts':'4011647d30c78c84',
}
SOURCE_FUNCTIONS={
 'thermal.openings':'review.dooropen','thermal.summary':'review.clipboardcheck','thermal.door':'review.dooropen',
 'pile.new':'review.nieuwpaalplan','object.rename':'review.paalplanhernoemen',
 'pile.legend-edit':'review.legendabewerken','pile.legend-used':'review.alleengebruiktactiveren',
 'pile.columns':'review.kolommenvanpaalopties','pile.combined':'review.dubbeleweergave',
 'pile.encoding-conflicts':'review.dubbelecoderingofgebruikbuitenscope',
 'audio.speech':'review.speech','audio.transcribe':'review.transcribe','audio.meeting':'review.meeting',
 'audio.mic-test':'review.mictest','audio.tts':'review.tts',
}
EVIDENCE={key:'stapregistry en de renderer van ThermalImportWizard gelezen; stapindicator, geen zelfstandige actie' for key in ('thermal.openings','thermal.summary')}
REUSED={
 'eb82f4b0bb193982':('edit.duplicate','Een bestaand paalplan direct dupliceren; gebruikt Dupliceren.'),
 'f543c443dd46906c':('edit.delete','Een paalplan verwijderen; gebruikt Verwijderen, met scope in het label.'),
 '986e0a413c0b602f':('status.warning','Waarschuwingsvorm bij ontbrekende kosten; semantische warning-kleur en label behouden.'),
 'c2a5d7c5c9a5194a':('file.open','Een lokaal project kiezen en openen; gebruikt Openen.'),
 '3f261a3108f95e89':('file.open','Een voorbeeldproject openen; gebruikt Openen met expliciet voorbeeldlabel.'),
 '6c1a45414a209240':('edit.undo','Titelbalk roept onUndo aan; gebruikt Ongedaan maken.'),
 'f0eb4a5a90c1b2f2':('edit.redo','Titelbalk roept onRedo aan; gebruikt Opnieuw uitvoeren.'),
}
ISSUES={
 'd519b126b5a469ee':'CPM-berekening starten; geen audio afspelen.',
 '01c098d307083bbb':'AI hervatten; geen audio afspelen.',
 'b76e1c6b14f1e43a':'AI pauzeren; geen audio pauzeren.',
 '4a028395debd5a89':'AI starten/stoppen; geen audiospeler.',
 'eca82aec93a14104':'Logweergave pauzeren; geen audio pauzeren.',
 '570d2f4a4d5cc199':'Logweergave hervatten; geen audio afspelen.',
 '83f7f9a7079658d0':'App-favicon; geen paalplanopdracht.',
 '2118a839477a5f5b':'App-logo in titelbalk; geen paalplanopdracht.',
 'bc8b0175df442bb6':'Grote algoritme-illustratie van kwadranten; geen bedieningsicoon.',
 '584ba513983a94c3':'Grote algoritme-illustratie van maximumhoek; geen bedieningsicoon.',
 '551a0e5b4fb639d1':'Dynamische paalsymbolen in het model; geen vaste UI-icoonfunctie.',
}

def arc_points(x,y,r,start,end,steps=48):
    from math import cos,sin,radians
    return [(x+r*cos(radians(start+(end-start)*i/steps)),y+r*sin(radians(start+(end-start)*i/steps))) for i in range(steps+1)]


def microphone(c,x=12):
    c.line([(x-3,3),(x+3,3),(x+3,13),(x-3,13)],closed=True,radius=3)
    c.line(arc_points(x,11,6,0,180),True,radius=0)
    c.line([(x,17),(x,21)]);c.line([(x-3,21),(x+3,21)])


def pencil(c):
    # Parallel sides from one axis; the wood tip follows that same axis.
    from math import hypot
    top=(20.5,6);neck=(17,16.5)
    dx,dy=neck[0]-top[0],neck[1]-top[1]
    length=hypot(dx,dy);ux,uy=dx/length,dy/length
    nx,ny=uy*1.7,-ux*1.7
    a=(top[0]-nx,top[1]-ny);b=(top[0]+nx,top[1]+ny)
    d=(neck[0]-nx,neck[1]-ny);e=(neck[0]+nx,neck[1]+ny)
    tip=(neck[0]+ux*3.2,neck[1]+uy*3.2)
    c.line([a,b,e,tip,d],True,closed=True,radius=.2)
    if c.size==24:c.line([d,e],True,radius=0)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='thermal.openings':
        box(c,3,4,18,16)
        c.line([(7,8),(17,8),(17,16),(7,16)],True,closed=True,radius=.8)
        if not small:c.line([(12,8),(12,16)],True)
    elif key=='thermal.door':
        c.line([(2,21),(2,3),(16,3),(16,21)],radius=.8)
        c.line([(5,6),(13,6),(13,21),(5,21)],True,closed=True,radius=.6)
        c.circle(10.5,13,.85,filled=True)
        c.plus(20,17,2.5)
    elif key=='thermal.summary':
        box(c,5,4,14,17);box(c,9,2,6,4)
        c.line([(8,13),(11,16),(16,10)],True,radius=.8)
    elif key=='pile.new':
        c.line([(8,3),(14,3),(14,17),(11,21),(8,17)],closed=True,radius=.5)
        c.line([(3,9),(6,9)]);c.line([(16,9),(21,9)])
        c.plus(20,18,2.5)
    elif key=='object.rename':
        box(c,3,5,10,14)
        c.line([(6,10),(11,10)])
        if not small:c.line([(6,14),(9,14)])
        pencil(c)
    elif key=='pile.legend-edit':
        box(c,3,3,10,18)
        for y in (7,12,17):c.line([(6,y),(9,y)])
        pencil(c)
    elif key=='pile.legend-used':
        c.line([(3,4),(20,4),(14,11),(14,19),(9,21),(9,11)],closed=True,radius=.7)
        c.line([(16,16),(18,18),(22,13)],True,radius=.7)
    elif key=='pile.columns':
        box(c,3,4,11,16)
        c.line([(3,9),(14,9)])
        for x in ([8.5] if small else [7,10.5]):c.line([(x,4),(x,20)])
        c.line([(17,16),(19,18),(22,12)],True,radius=.6)
    elif key=='pile.combined':
        box(c,3,3,18,18)
        c.line([(3,12),(21,12)])
        c.line([(7,7),(17,7)],True);c.line([(7,17),(17,17)],True)
    elif key=='pile.encoding-conflicts':
        c.circle(6,11,3.3);c.circle(18,11,3.3)
        c.line([(12,4),(12,13)],True)
        c.circle(12,18,.9,True,True)
    elif key=='audio.speech':microphone(c)
    elif key=='audio.transcribe':
        box(c,4,3,16,18)
        c.line([(8,8),(10,5),(12,11),(14,7),(16,8)],True,radius=.4)
        for y,end in [(15,16),(18,13)]:c.line([(8,y),(end,y)])
    elif key=='audio.meeting':
        c.circle(7,7,3);c.circle(18,7,2.7,True)
        c.line([(2.5,21)]+arc_points(7,20,4.5,180,360)+[(11.5,21)],radius=0)
        c.line([(14.5,21)]+arc_points(18,20,3.5,180,360)+[(21.5,21)],True,radius=0)
    elif key=='audio.mic-test':
        c.line([(3,20),(3,4)])
        c.line([(6,12),(9,12),(11,6),(14,18),(17,9),(19,12),(21,12)],True,radius=.5)
    elif key=='audio.tts':
        c.line([(3,9),(7,9),(12,5),(12,19),(7,15),(3,15)],closed=True,radius=.6)
        c.line(arc_points(11,12,6,-50,50),True,radius=0)
        if not small:c.line(arc_points(11,12,10,-50,50),True,radius=0)
    return True
