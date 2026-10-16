"""IFC actions: model exchange and validation, distinct from generic file actions."""

DEFINITIONS=[
 ('ifc.import','IFC importeren','IFC en BIM','Een IFC-model inlezen; label en modelvorm onderscheiden deze opdracht van algemene bestandsimport.'),
 ('ifc.export','IFC exporteren','IFC en BIM','Model- of begrotingsgegevens als IFC wegschrijven; het label benoemt IFC, geen algemeen exportformaat.'),
 ('ifc.validate','IFC valideren','IFC en BIM','De modelvalidatie starten; geen geslaagde status, rapportvalidatie of controle van een energierekenkern.'),
]
KEYS={d[0] for d in DEFINITIONS}
EXAMPLES={'ifc.import':'e56a571f2950e3fd','ifc.export':'0a20794c7d830f96','ifc.validate':'d2147f75536ab361'}
ISSUES={'1f0f0ba95c5bb04d':'Kerncontrole van Energy; geen IFC-modelvalidatie starten.',
        '07694e578e0da59b':'Rapport valideren; geen IFC-modelvalidatie.'}

def extend(c,key):
    if key not in KEYS:return False
    # Orthographic isometric projection of one unit cube. All three axes
    # have the same projected length; shared vertices are computed once.
    from math import sqrt
    edge=7.5
    def project(x,y,z):
        return (9+edge*sqrt(3)/2*(x-y),12+edge/2*(x+y)-edge*z)
    back=project(0,0,1)
    right=project(1,0,1)
    left=project(0,1,1)
    front=project(1,1,1)
    bottom=project(1,1,0)
    c.line([back,right,project(1,0,0),bottom,project(0,1,0),left],closed=True,radius=.45)
    c.line([left,front,right],radius=.45)
    c.line([front,bottom])
    if key=='ifc.validate':
        c.line([(17,15),(19,17),(22,12)],True,radius=.6)
    else:
        tip,tail=(17,5) if key=='ifc.import' else (5,17)
        c.line([(20,tail),(20,tip)],True)
        shoulder=tip-3 if key=='ifc.import' else tip+3
        c.line([(17.5,shoulder),(20,tip),(22.5,shoulder)],True,radius=.6)
    return True
