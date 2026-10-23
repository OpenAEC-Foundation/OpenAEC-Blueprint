"""Report output and scaffolds; planning/layout templates stay separate."""
from b2_second_series import box

DEFINITIONS=[
 ('report.generate','Rapport genereren','Rapporten','Een rapportuitvoer opbouwen uit documentgegevens, zoals PDF genereren; geen bestaand bestand exporteren of projectinformatie openen.'),
 ('report.template','Rapportsjabloon','Rapporten','Een opzet voor een rapport kiezen; geen WBS-planningssjabloon of schermindeling. Functiebron: Reports TemplateSelector.tsx, handleChange/loadScaffold; geen bevestigde icoonaanroep in dit cluster.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={'report.generate':'bdb2323e10ee76f2'}
ISSUES={'7731669e788edf87':'WBS-planningssjabloon invoegen; geen rapportsjabloon kiezen.',
        '835627b22da03b01':'Registry voor weergave-indelingen; geen rapportsjabloon kiezen.'}


def extend(c,key):
    if key not in KEYS:return False
    box(c,4,3,16,18)
    if key=='report.generate':
        c.line([(7,7),(16,7)])
        if c.size==24:c.line([(7,10),(13,10)])
        for x,top in [(8,15),(12,13),(16,11)]:c.line([(x,17),(x,top)],True)
    else:
        c.line([(7,7),(17,7)],True)
        if c.size==16:box(c,7,11,10,7)
        else:
            box(c,7,11,4,7);box(c,14,11,3,7)
    return True
