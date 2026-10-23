"""Project-library navigation and data views; insertion commands remain separate."""
from b2_second_series import box

DEFINITIONS=[
 ('project.folder','Projectmap','Projecten en gegevens','Een map binnen een projectbibliotheek of bestandslocatielijst bekijken; geen bestand openen of nieuwe map aanmaken.'),
 ('data.table','Tabelweergave','Projecten en gegevens','Gegevens als tabel bekijken of de tabelweergave omschakelen; een tabelblok invoegen is een andere opdracht.'),
 ('data.chart','Grafiekweergave','Projecten en gegevens','Een grafiek of histogram met gegevens tonen; geen specifieke statistiekendialoog of urenverdeling bewerken.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={'project.folder':'c6b28ec8feaa9033','data.table':'44c70dd34017ba8c','data.chart':'7962634bca4e037a'}
ISSUES={'6b13080726f40d5e':'Een tabelblok invoegen is geen bestaande gegevens als tabel bekijken.',
        'fd075b03be024a7d':'Een tabelblok invoegen is geen bestaande gegevens als tabel bekijken.',
        '9b7cc874353719e3':'Downloadstatistieken is een specifieke dialoog; geen algemene grafiekweergave omschakelen.',
        '71852e25a3b1082f':'Urenverdeling van een toewijzing bewerken is geen algemene grafiekweergave tonen.'}


def extend(c,key):
    if key not in KEYS:return False
    if key=='project.folder':
        box(c,3,8,18,12)
        c.line([(3,8),(3,4),(9,4),(13,8)],radius=1.5)
    elif key=='data.table':
        box(c,3,4,18,16)
        c.line([(3,9),(21,9)])
        inset=c.width*24/c.size
        c.line([(3+inset,9),(21-inset,9)],True)
        c.line([(3,14.5),(21,14.5)])
        for x in ([11] if c.size==16 else [9,15]):c.line([(x,9),(x,20)])
    elif key=='data.chart':
        c.line([(3,3),(3,21),(21,21)],radius=1.5)
        c.line([(8,17),(8,13)],True)
        c.line([(13,17),(13,9)],True)
        c.line([(18,17),(18,5)],True)
    return True
