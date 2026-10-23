"""Small, deterministic 2D construction model for the selected B icon family.

Accents own edges of a common polyline, never approximate duplicate strokes.
Expand centre lines to filled polygons once. Shared miter vertices are calculated
once per joint and reused by both colours. No renderer-dependent stroke caps.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot

Point = tuple[float, float]
B_WIDTHS = {16: 1.25, 24: 1.75}


def signed_area(poly):
    return sum(x*y2-x2*y for (x,y),(x2,y2) in zip(poly,poly[1:]+poly[:1]))/2


def intersection_area(subject, clip):
    """Sutherland-Hodgman intersection for two convex, CCW polygons."""
    output = list(subject)
    def side(a,b,p): return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
    for a,b in zip(clip,clip[1:]+clip[:1]):
        incoming=output; output=[]
        if not incoming: break
        start=incoming[-1]; ds=side(a,b,start)
        for end in incoming:
            de=side(a,b,end)
            if (ds>=-1e-10)!=(de>=-1e-10):
                t=ds/(ds-de)
                output.append((start[0]+t*(end[0]-start[0]),start[1]+t*(end[1]-start[1])))
            if de>=-1e-10: output.append(end)
            start,ds=end,de
    return abs(signed_area(output)) if len(output)>2 else 0.0


def polygon_path(poly):
    def number(v): return f'{v:.7f}'.rstrip('0').rstrip('.') or '0'
    return 'M'+'L'.join(number(x)+' '+number(y) for x,y in poly)+'Z'


@dataclass
class Stroke:
    name: str
    points: list[Point]
    closed: bool = False
    accent_edges: tuple[int,...] = ()


@dataclass
class Model:
    key: str
    size: int
    width: float
    strokes: list[Stroke] = field(default_factory=list)
    faces: list[tuple[str,list[Point],str]] = field(default_factory=list)

    def line(self,name,points,accent=False):
        return self.path(name,points,accent_edges=tuple(range(len(points)-1)) if accent else ())

    def path(self,name,points,closed=False,accent_edges=()):
        points=[tuple(map(float,p)) for p in points]
        count=len(points) if closed else len(points)-1
        assert count>0 and all(0<=n<count for n in accent_edges)
        self.strokes.append(Stroke(name,points,closed,tuple(accent_edges)))
        return self

    def face(self,name,points,accent=False):
        points=[tuple(map(float,p)) for p in points]
        if signed_area(points)<0:points.reverse()
        self.faces.append((name,points,'accent' if accent else 'primary'))
        return self

    def square(self,name,x,y,w,accent=False):
        return self.face(name,[(x,y),(x+w,y),(x+w,y+w),(x,y+w)],accent)

    def pieces(self):
        result=[]
        for stroke in self.strokes:
            points=stroke.points; n=len(points); count=n if stroke.closed else n-1
            directions=[]; normals=[]
            for a,b in zip(points,points[1:]+points[:1] if stroke.closed else points[1:]):
                dx,dy=b[0]-a[0],b[1]-a[1];length=hypot(dx,dy)
                assert length>1e-9,(self.key,stroke.name,'zero-length edge')
                directions.append((dx/length,dy/length));normals.append((-dy/length,dx/length))
            left=[];right=[]
            for i,(x,y) in enumerate(points):
                if not stroke.closed and i in (0,n-1):
                    normal=normals[0 if i==0 else -1]
                    ox,oy=normal[0]*self.width/2,normal[1]*self.width/2
                else:
                    before=(i-1)%count;after=i%count
                    denominator=1+sum(a*b for a,b in zip(directions[before],directions[after]))
                    assert denominator>1e-8,(self.key,stroke.name,'reversing edge')
                    ox=(normals[before][0]+normals[after][0])*self.width/2/denominator
                    oy=(normals[before][1]+normals[after][1])*self.width/2/denominator
                    assert hypot(ox,oy)<=3*self.width/2+1e-8,(self.key,stroke.name,'miter too long')
                left.append((x+ox,y+oy));right.append((x-ox,y-oy))
            for i in range(count):
                j=(i+1)%n
                poly=[left[i],right[i],right[j],left[j]]
                if signed_area(poly)<0:poly.reverse()
                assert signed_area(poly)>1e-9,(self.key,stroke.name,'collapsed polygon')
                result.append((stroke.name+':'+str(i),poly,'accent' if i in stroke.accent_edges else 'primary'))
        return result+self.faces

    def validate(self):
        pieces=self.pieces();maximum=0.0
        for name,poly,tone in pieces:
            for x,y in poly:
                assert 0<=x<=self.size and 0<=y<=self.size,(self.key,self.size,name,'clipped',x,y)
            turns=[]
            for i,a in enumerate(poly):
                b,c=poly[(i+1)%len(poly)],poly[(i+2)%len(poly)]
                turns.append((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))
            assert min(turns)>=-1e-8,(self.key,self.size,name,'non-convex stroke piece')
        primary=[p for p in pieces if p[2]=='primary']; accents=[p for p in pieces if p[2]=='accent']
        assert primary and accents,(self.key,'missing colour part')
        for aname,a,_ in accents:
            for bname,b,_ in primary:
                area=intersection_area(a,b);maximum=max(maximum,area)
                assert area<1e-7,(self.key,self.size,'overlapping colours',aname,bname,area)
        return {'key':self.key,'master_px':self.size,'pieces':len(pieces),
                'max_colour_overlap_area':round(maximum,10),'bounds':'inside viewBox'}

    def markup(self):
        pieces=self.pieces(); result=[]
        for tone in ('primary','accent'):
            data=''.join(polygon_path(poly) for _,poly,t in pieces if t==tone)
            colour='currentColor' if tone=='primary' else 'var(--icon-accent,currentColor)'
            result.append(f'<path data-part="{tone}" fill="{colour}" stroke="none" fill-rule="nonzero" d="{data}"/>')
        return ''.join(result)

    def as_dict(self):
        return {'function_key':self.key,'master_px':self.size,'line_width':self.width,
                'strokes':[{'name':s.name,'anchors':s.points,'closed':s.closed,'accent_edges':s.accent_edges} for s in self.strokes],
                'faces':[{'name':n,'anchors':p,'tone':t} for n,p,t in self.faces]}

    def wireframe(self):
        result=[]
        for stroke in self.strokes:
            d='M'+'L'.join(f'{x:g} {y:g}' for x,y in stroke.points)+('Z' if stroke.closed else '')
            result.append(f'<path d="{d}"/>')
            result.extend(f'<circle cx="{x:g}" cy="{y:g}" r=".18"/>' for x,y in stroke.points)
        return '<g fill="none" stroke="var(--construction,#22d3ee)" stroke-width=".12">'+''.join(result)+'</g>'


def build_b_model(key,size):
    m=Model(key,size,B_WIDTHS[size])
    small=size==16
    def coords(big,little):return little if small else big
    if key=='open':
        m.path('folder',coords([(3,8),(3,4),(9,4),(12,7),(19,7),(21,9),(21,18),(18,21),(3,21)],
                              [(2,6),(2,2),(6,2),(9,5),(12,5),(14,7),(14,12),(12,14),(2,14)]),True,(2,))
        m.line('lip',coords([(3,10),(18,10),(21,9)],[(2,7.5),(12,7.5),(14,7)]))
    elif key=='save':
        m.path('case',coords([(3,3),(17,3),(21,7),(21,21),(3,21)],[(2,2),(11,2),(14,5),(14,14),(2,14)]),True)
        m.path('storage-slot',coords([(7,3),(7,10),(17,10),(17,3)],[(5,2),(5,6),(10,6),(10,2)]),accent_edges=(1,))
        m.line('label',coords([(7,21),(7,14),(17,14),(17,21)],[(5,14),(5,9),(11,9),(11,14)]))
    elif key in {'import','export'}:
        m.line('tray',coords([(3,15),(3,19),(5,21),(19,21),(21,19),(21,15)],[(2,10),(2,12),(4,14),(12,14),(14,12),(14,10)]))
        if key=='import':
            m.line('shaft',coords([(12,3),(12,15)],[(8,2),(8,9)]),True)
            m.line('arrowhead',coords([(8,11),(12,15),(16,11)],[(5,6),(8,9),(11,6)]),True)
        else:
            m.line('shaft',coords([(12,15),(12,3)],[(8,10),(8,2)]),True)
            m.line('arrowhead',coords([(8,7),(12,3),(16,7)],[(5,5),(8,2),(11,5)]),True)
    elif key=='undo':
        m.line('return-head',coords([(9,4),(3,10),(9,16)],[(6,2),(2,6),(6,10)]),True)
        m.line('return-neck',coords([(3,10),(10,10)],[(2,6),(7,6)]),True)
        m.line('return-body',coords([(10,10),(14,10),(20,16),(20,21)],[(7,6),(9,6),(13,10),(13,14)]))
    elif key=='search':
        m.path('lens',coords([(6,3),(13,3),(17,7),(17,14),(13,18),(6,18),(2,14),(2,7)],
                            [(5,2),(9,2),(12,5),(12,9),(9,12),(5,12),(2,9),(2,5)]),True,(0,))
        m.line('handle',coords([(15.5,15.5),(21,21)],[(10.5,10.5),(14,14)]))
    elif key=='select':
        # The intermediate anchor is exactly collinear with the outer edge.
        a,b=coords(((4,3),(19,9)),((2,2),(12,5.5)))
        join=tuple(x+.4*(y-x) for x,y in zip(a,b))
        rest=coords([(19,11),(13,12),(18,18),(15,21),(10,15),(4,21)],[(12,7),(8,8),(12,12),(9,14),(6,10),(2,14)])
        m.path('pointer',[a,join,b,*rest],True,(0,))
    elif key=='move':
        low,high,centre=(7,9,8) if small else (10,14,12)
        start,end=(2,14) if small else (3,21)
        for name,points in [('north',[(centre,start),(centre,low)]),('south',[(centre,high),(centre,end)]),
                            ('west',[(start,centre),(low,centre)]),('east',[(high,centre),(end,centre)])]:m.line(name,points)
        arms=coords([[(9,6),(12,3),(15,6)],[(9,18),(12,21),(15,18)],[(6,9),(3,12),(6,15)],[(18,9),(21,12),(18,15)]],
                    [[(6,4),(8,2),(10,4)],[(6,12),(8,14),(10,12)],[(4,6),(2,8),(4,10)],[(12,6),(14,8),(12,10)]])
        for i,points in enumerate(arms):m.line('head-'+str(i),points)
        m.square('joint',low,low,high-low,True)
    elif key=='measure':
        m.path('ruler',coords([(3,16),(16,3),(18,3),(21,6),(21,8),(8,21),(6,21),(3,18)],
                             [(2,10),(10,2),(12,2),(14,4),(14,6),(6,14),(4,14),(2,12)]),True,(1,2,3))
        ticks=coords([[(8,11),(10,13)],[(11,8),(13,10)]],[[(6,6),(8,8)]])
        for i,points in enumerate(ticks):m.line('tick-'+str(i),points)
    elif key=='layers':
        m.path('top-layer',coords([(3,7),(12,3),(21,7),(12,11)],[(2,5),(8,2),(14,5),(8,8)]),True,(2,3))
        rows=coords([[(3,12),(12,16),(21,12)],[(3,17),(12,21),(21,17)]],[[(2,10),(8,13),(14,10)]])
        for i,points in enumerate(rows):m.line('layer-'+str(i),points)
    elif key=='note':
        m.path('note',coords([(3,3),(18,3),(21,6),(21,17),(9,17),(3,21)],[(2,2),(12,2),(14,4),(14,11),(6,11),(2,14)]),True,(1,))
        rows=coords([[(7,8),(17,8)],[(7,12),(13,12)]],[[(5,6),(11,6)]])
        for i,points in enumerate(rows):m.line('text-'+str(i),points)
    elif key=='cpt':
        m.path('cone',coords([(5,4),(19,4),(12,17)],[(3,3),(13,3),(8,11)]),True)
        m.line('friction-mark',coords([(8,21),(16,21)],[(5,14),(11,14)]),True)
    elif key=='cloud':
        points=coords([(5,8),(10,5),(15,3),(5,13),(10,10),(15,8),(20,6),(10,16),(15,13),(20,11),(15,19),(20,16)],
                      [(3,6),(7,3),(11,2),(3,10),(7,7),(11,6),(7,12),(11,10),(13,13)])
        width=1.5 if small else 2
        selected=len(points)-1 if small else 10
        for i,(x,y) in enumerate(points):m.square('point-'+str(i),x-width/2,y-width/2,width,i==selected)
    elif key=='delete':
        m.path('handle',coords([(9,6),(9,3),(15,3),(15,6)],[(6,4),(6,2),(10,2),(10,4)]),accent_edges=(1,))
        m.line('lid',coords([(3,6),(21,6)],[(2,4),(14,4)]))
        m.line('bin',coords([(5,6),(5,18),(8,21),(16,21),(19,18),(19,6)],[(3,4),(3,12),(5,14),(11,14),(13,12),(13,4)]))
        ticks=coords([[(9,10),(9,17)],[(15,10),(15,17)]],[[(8,7),(8,11)]])
        for i,points in enumerate(ticks):m.line('rib-'+str(i),points)
    else:raise ValueError(key)
    return m
