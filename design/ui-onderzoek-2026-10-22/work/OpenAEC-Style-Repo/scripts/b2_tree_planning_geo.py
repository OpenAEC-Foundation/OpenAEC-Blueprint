"""Reviewed tree, planning and geotechnical functions; explicit source mappings."""
from b2_second_series import box

DEFINITIONS=[
 ('tree.expand','Uitklappen','Lijsten en bomen','Een ingeklapte rij of tak openklappen. De aanwijzer wijst naar rechts in gesloten toestand; niet gebruiken voor vooruitnavigatie.'),
 ('tree.collapse','Inklappen','Lijsten en bomen','Een open rij of tak inklappen. De aanwijzer wijst omlaag in open toestand; geen lint-, paneel- of dropdownbediening.'),
 ('planning.gantt','Gantt-planning','Planning','Een Gantt-indeling herkennen. Bron: de Gantt-sleutel in de Planner-layoutregistry en de layoutknoppen; geen afzonderlijke hardgecodeerde Gantt-opdracht bewezen.'),
 ('planning.production','Productieplanning','Planning','De productieplanningswerkruimte openen in Frame; geen plattegrond of technische tekening.'),
 ('planning.cut-list','Zaagplan','Planning','De werkruimte met zaagoptimalisatie openen; geen tijdsplanning of klembordknipactie.'),
 ('planning.dependency-add','Taakrelatie toevoegen','Planning','Een afhankelijkheidsrelatie tussen taken toevoegen; geen hyperlink of willekeurig object toevoegen.'),
 ('planning.interruption-add','Taakonderbreking toevoegen','Planning','Een onderbreking in een taak invoegen; geen taak verwijderen of verwerking pauzeren.'),
 ('planning.driving','Bepalende relatie','Planning','Een sturende relatie aanduiden. Dit is een toestand bij de afhankelijkheid, geen opdracht en geen algemene succesmelding.'),
 ('planning.sync','Taken synchroniseren','Planning','Open Field-tickets als taken met KYP Project synchroniseren. De bron toont de knop; uitvoering van de koppeling is niet geverifieerd.'),
 ('geo.sondering','Sondering plaatsen','Geotechniek','Een sonderingslocatie in de tekening plaatsen; geen boring of algemene meetpin.'),
 ('geo.bore','Boring plaatsen','Geotechniek','Een boorlocatie in de tekening plaatsen; onderscheiden van een sondering.'),
 ('geo.sounding-grid','Sonderingsraster plaatsen','Geotechniek','Een raster met sonderingslocaties plaatsen; geen weergaveraster tonen.'),
 ('geo.coordinate-tag','RD-coördinaat plaatsen','Geotechniek','Een blijvend RD-coördinaatlabel in de tekening plaatsen; geen zoekopdracht of afstandsmeting.'),
]
KEYS={d[0] for d in DEFINITIONS}
SERIES={key:8 if group=='Lijsten en bomen' else 9 if group=='Planning' else 10 for key,_,group,_ in DEFINITIONS}
EXAMPLES={
 'tree.expand':'86dc30a1e1e261c9','tree.collapse':'d2638b377d86d685',
 'planning.gantt':'ae69b3e6ec027156','planning.production':'8318a35744e2e52d',
 'planning.cut-list':'72a4428c0cc71466','planning.dependency-add':'85023deea0637235',
 'planning.interruption-add':'878e74a91fdc7d16','planning.driving':'b0c83ea72510ac3b',
 'planning.sync':'850b8fb667b5d229','geo.sondering':'424135cc3fda0cff',
 'geo.bore':'b0e5fd9cfe7c9c71','geo.sounding-grid':'27ac02054351fb1b','geo.coordinate-tag':'163ce7fa69f89fe2',
}
SOURCE_FUNCTIONS={
 'planning.gantt':'review.ganttchartsquare','planning.production':'review.productieplan',
 'planning.cut-list':'review.zaagplan','planning.dependency-add':'review.relatietoevoegen',
 'planning.interruption-add':'review.onderbrekingtoevoegen','planning.driving':'review.bepalend',
 'planning.sync':'review.syncopenticketsalstakennaarkypprojectplanning',
 'geo.bore':'review.placebore','geo.sounding-grid':'review.placeraster','geo.coordinate-tag':'review.coordtag',
}
EVIDENCE={
 'planning.gantt':'icoonregistry en dynamische layoutknop gelezen; geen zelfstandige Gantt-opdracht bewezen',
 'planning.sync':'UI-knop en doellabel gelezen; werking externe KYP-koppeling niet geverifieerd',
 'planning.driving':'toestandsindicator bij item.driving gelezen; geen actieknop',
}
# Reuse only these inspected call sites, never every occurrence of a name.
REUSED={'b6551cbbcda32862':('draw.note','Taakaantekening toevoegen gebruikt het bestaande Opmerking-ontwerp.'),
        'ad083eb833a3b33f':('file.export','GeoJSON is een exportformaat; gebruikt het bestaande Exporteren-ontwerp.')}
ISSUES={
 '58f36a32ca9f8eed':'Plattegrondblad in Pointcloud; geen tijdsplanning.',
 'c1676146271bbfe6':'Plattegrondblad in Pointcloud; geen tijdsplanning.',
 'de5f2f568326abf4':'Mesh omzetten naar tekeningen; geen tijdsplanning.',
 '724546f8c0a6e761':'Mesh omzetten naar tekeningen; geen tijdsplanning.',
 'a6ffb9712f3da69e':'App-favicon, geen geotechnisch gereedschap.',
 '1e2bcca63db6596f':'Informatief pakketicoon bij Snap-update; geen geotechnisch gereedschap.',
 '5d5f07c5010c72ad':'Recent geopende bestanden; geen geotechnisch gereedschap.',
 '154065ae8c7a8e92':'Lint compact maken; geen boomtak inklappen.',
 '2b3bca5f9fa0d8e7':'Keuzemenu openen; geen boomtak inklappen.',
 'd3f9b3f8517c5d87':'Tijdwaarde verlagen; geen boomtak inklappen.',
 'f6f49488c64cdbe3':'Volgende resource kiezen; geen boomtak uitklappen.',
 'd6b5b9d50fa23cf0':'Documenttabs scrollen; geen boomtak uitklappen.',
 'cf66a61dd9a43f5d':'Documenttabs scrollen; geen boomtak uitklappen.',
 '51b96ce273bb2749':'Zijpaneel openen; geen boomtak uitklappen.',
}

def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='tree.expand':c.line([(9,6),(15,12),(9,18)],radius=1)
    elif key=='tree.collapse':c.line([(6,9),(12,15),(18,9)],radius=1)
    elif key=='planning.gantt':
        box(c,3,3,18,18)
        for x,y,end in [(7,7,13),(11,12,17),(7,17,11)]:c.line([(x,y),(end,y)],True)
    elif key=='planning.production':
        box(c,3,5,18,16)
        for x in (7,17):c.line([(x,3),(x,7)])
        c.line([(3,10),(21,10)])
        c.line([(7,15),(10,18),(17,13)],True,radius=.8)
    elif key=='planning.cut-list':
        for y,end in [(5,21),(12,16),(19,19)]:
            c.line([(3,y),(end,y)])
            c.line([(8,y-1.5),(6,y+1.5)],True,radius=0)
    elif key=='planning.dependency-add':
        box(c,3,4,7,5);box(c,14,15,7,5)
        c.line([(6.5,9),(6.5,17.5),(11,17.5)],True,radius=1)
        c.line([(9,15.5),(11,17.5),(9,19.5)],True,radius=.5)
    elif key=='planning.interruption-add':
        box(c,3,8,6,8);box(c,15,8,6,8)
        c.line([(12,4),(12,20)],True,radius=0)
    elif key=='planning.driving':
        c.line([(13,3),(5,13),(11,13),(10,21),(19,10),(13,10)],closed=True,radius=.5)
    elif key=='planning.sync':
        c.line([(4,9),(4,5),(20,5)],True,radius=1)
        c.line([(17,2.5),(20,5),(17,7.5)],True,radius=.5)
        c.line([(20,15),(20,19),(4,19)],True,radius=1)
        c.line([(7,16.5),(4,19),(7,21.5)],True,radius=.5)
        c.line([(8,10),(14,10)])
        c.line([(10,14),(16,14)])
    elif key=='geo.sondering':
        c.line([(3,7),(8,7)]);c.line([(16,7),(21,7)])
        c.line([(12,3),(12,15)])
        c.line([(8,15),(16,15),(12,21)],True,closed=True,radius=.4)
    elif key=='geo.bore':
        c.line([(3,7),(8,7)]);c.line([(16,7),(21,7)])
        c.line([(12,3),(12,21)])
        for y in ([12,17] if small else [10,14,18]):c.line([(9,y+1),(15,y-1)],True,radius=0)
    elif key=='geo.sounding-grid':
        for v in (5,19):
            c.line([(v,5),(v,19)])
            c.line([(5,v),(19,v)])
        for x in (5,19):
            for y in (5,19):c.circle(x,y,1.7,True,True)
        if not small:c.circle(12,12,1.7,True,True)
    elif key=='geo.coordinate-tag':
        c.line([(3,21),(3,3)]);c.line([(3,21),(21,21)])
        c.circle(13,10,2.7,True)
        c.line([(13,4),(13,6)],True);c.line([(13,14),(13,16)],True)
        c.line([(7,10),(9,10)],True);c.line([(17,10),(19,10)],True)
    return True
