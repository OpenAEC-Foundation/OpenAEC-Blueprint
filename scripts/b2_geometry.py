"""Original B2 vector construction and deterministic filled-outline export.

Runtime: python -m pip install --target harmonization/sources/b2-runtime shapely==2.2.0
No upstream icon artwork is copied. Existing B2 geometry is the design source.
"""
from pathlib import Path
import sys
import math
import re
from dataclasses import dataclass, field

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'harmonization/sources/b2-runtime'))
try:
    from shapely.geometry import LineString, Point, Polygon
    from shapely.ops import unary_union
    from shapely import set_precision
except ImportError as error:
    raise SystemExit('Installeer eerst scripts/requirements-icon-b2.txt in harmonization/sources/b2-runtime') from error
from build_icon_rounding_review import proposal_model, rounded_edges
from b2_icon_placement_refinements import refine
from b2_second_series import ACCENT_FRONT, extend
from b2_window_series import extend as extend_windows
from b2_text_series import extend as extend_text
from b2_data_series import extend as extend_data
from b2_report_series import extend as extend_report
from b2_ifc_series import extend as extend_ifc
from b2_tree_planning_geo import extend as extend_next
from b2_energy_pile_audio import extend as extend_later
from b2_page_views import extend as extend_pages
from b2_bulk_series import extend as extend_bulk
from b2_session_two import extend as extend_session
from b2_document_navigation import extend as extend_document_navigation
from b2_session_three import extend as extend_third
from b2_session_four import extend as extend_fourth
from b2_completion import extend as extend_completion, ACCENT_FRONT as COMPLETION_ACCENT_FRONT

WHOLE_ACCENT={'planning.driving'}

# The foreground is a design decision for each icon, not a family-wide rule.
ACCENT_FOREGROUND={
    'edit.undo':'De gekleurde pijlpunt blijft één geheel bij de aansluiting op de steel.',
    'edit.redo':'Dezelfde ononderbroken pijlpunt als bij Ongedaan maken.',
    'nav.back':'De pijlpunt ligt vóór de steel, zodat de richting volledig zichtbaar blijft.',
    'nav.forward':'Dezelfde aansluiting als bij Terug, gespiegeld.',
    'edit.paste':'De invoegpijl loopt vanuit het klembord door in het voorste vel.',
    'file.print':'Het gekleurde papier ligt vóór de printeropening.',
}
ACCENT_FOREGROUND.update(ACCENT_FRONT)
ACCENT_FOREGROUND.update(COMPLETION_ACCENT_FRONT)
ACCENT_FOREGROUND['format.no-color']='De diagonale accentstreep loopt ononderbroken voor het lege kleurvlak.'
ACCENT_FOREGROUND.update({
    'page.extract':'De extractiepijl loopt ononderbroken vóór de paginarand.',
    'page.resize':'De formaatpijl loopt ononderbroken vóór de paginacontouren.',
    'draw.arrow':'De accentpijlpunt ligt ononderbroken vóór de steel.',
    'object.align-middle':'De accentas blijft ononderbroken vóór de objectcontouren.',
})
ACCENT_FOREGROUND.update({k:reason for k,reason in {
    'draw.spline-arrow':'De gebogen pijl heeft een volledige accentpunt vóór de curve.',
    'draw.coordinate':'De puntmarkering en leidlijn blijven volledig zichtbaar.',
    'measure.count':'De dwarsstrepen van het telteken blijven ononderbroken vóór de schuine staanders.',
    'transform.join':'De gekleurde verbinding en beide aansluitpunten liggen volledig vóór de twee lijndelen.',
    'transform.stretch':'De uitrekpijl loopt ononderbroken vóór de kadergrens.',
    'transform.break':'De twee breekpunten blijven volledig in accentkleur zichtbaar.',
    'transform.scale':'De schaalpijl blijft ononderbroken bij de kaderkruising.',
    'document.compress':'De twee compressiepijlen lopen ononderbroken vóór de paginarand.',
    'edit.paste-in-place':'De plaatsmarkering staat vrij naast het klembord.',
    'edit.deselect':'De accentstreep ligt vóór de selectiemarkeringen.',
    'document.compare':'De vergelijkingslijnen blijven vóór de paginaranden zichtbaar.',
    'view.remember-reading':'Het volledige accentbladwijzertje blijft vóór de boekcontour.',
    'panel.element-visibility':'De zichtbaarheidsschuine streep blijft ononderbroken vóór de oogcontour.',
    'object.reset-location':'De richtpijlen blijven volledig zichtbaar vóór het centrale object.',
    'view.rotate-left':'De weergavepijl blijft een ononderbroken accentvorm.',
    'view.rotate-right':'De gespiegelde weergavepijl behoudt de ononderbroken accentvorm.',
}.items()})
ACCENT_FOREGROUND['line.to-measure']='De oranje maatbegrenzingen liggen ononderbroken voor de horizontale maatlijn.'
ACCENT_FOREGROUND['data.table']='De bovenste binnenlijn loopt ononderbroken vóór de kolomverdelers; het accent blijft binnen de hoofdgekleurde buitenrand.'
ACCENT_FOREGROUND.update({
    'planning.cut-list':'De snijmarkeringen lopen ononderbroken over de materiaalregels.',
    'geo.bore':'De boorspiraal blijft ononderbroken vóór de schacht zichtbaar.',
    'geo.sounding-grid':'De sonderingspunten liggen vóór de rasterverbindingen en behouden hun volle accentkleur.',
})


def foreground(key):return 'accent' if key in ACCENT_FOREGROUND else 'primary'


def layer_reason(key):
    return ACCENT_FOREGROUND.get(key,'De hoofdkleur bewaart de doorgaande contour; losliggende accenten blijven intact.')

SHAPE_REVISIONS={
    'file.new':'Het plusje staat halverwege de vorige middenpositie en de eerdere positie linksonder.',
    'file.save-as':'Volwaardige diskette met een diagonale pen; ruimte rond de pen houdt de vormen leesbaar.',
    'view.orbit':'Terug naar de bol met omloop: een zuivere cirkel en een vloeiende, licht gekantelde ellips.',
    'edit.paste':'Klembord achter een vel, met een invoegpijl; geen gekleurde clip meer.',
    'edit.undo':'De steel in de hoofdkleur loopt tot in de aanwijzer, met een afgerond aansluitvlak.',
    'edit.redo':'Dezelfde doorlopende steel en afgeronde aansluiting als bij Ongedaan maken, gespiegeld.',
    'nav.back':'De steel loopt tot in de aanwijzer; buitenvorm behouden en twee vaste kleuren.',
    'nav.forward':'Dezelfde doorlopende steel als bij Terug, met behoud van de buitenvorm.',
}

# Iconen die volgens docs/iconen.md opnieuw getekend zijn; zie scripts/b2_richtlijn.py.
from b2_richtlijn import REVISED as RICHTLIJN_REVISED
for _key in RICHTLIJN_REVISED:ACCENT_FOREGROUND.pop(_key,None)
SHAPE_REVISIONS.update(RICHTLIJN_REVISED)

ROUNDED_JOINTS={'nav.forward'}  # edit.undo, edit.redo en nav.back zijn volgens docs/iconen.md hertekend
CURRENT_CHANGES=ROUNDED_JOINTS


@dataclass
class Construction:
    key:str
    size:int
    width:float
    paths:list=field(default_factory=list)
    circles:list=field(default_factory=list)
    fills:list=field(default_factory=list)
    clear_primary:bool=False

    def line(self,points,accent=False,closed=False,radius=3.6):
        scale=self.size/24
        self.paths.append({'points':[(x*scale,y*scale) for x,y in points],
                           'closed':closed,'radius':radius*scale,'tone':'accent' if accent else 'primary'})
        return self

    def circle(self,x,y,r,accent=False,filled=False):
        scale=self.size/24
        self.circles.append({'x':x*scale,'y':y*scale,'r':r*scale,
                             'tone':'accent' if accent else 'primary','filled':filled})
        return self

    def box(self,x,y,w,h,accent=False):
        return self.line([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],accent,True)

    def plus(self,x,y,r=2,accent=True):
        self.line([(x-r,y),(x+r,y)],accent)
        self.line([(x,y-r),(x,y+r)],accent)
        return self

    def mirror(self):
        for p in self.paths:p['points']=[(self.size-x,y) for x,y in p['points']]
        for c in self.circles:c['x']=self.size-c['x']
        return self

    def geometry(self,front=None):
        front=front or foreground(self.key)
        assert front in ('primary','accent')
        cache=getattr(self,'_geometry',{})
        if front in cache:return cache[front]
        if hasattr(self,'_raw_geometry'):
            raw=self._raw_geometry
            if self.key in ROUNDED_JOINTS:
                # A single silhouette, partitioned at a rounded seam. Neither
                # colour has an overlapping cap painted over the other colour.
                y=10 if self.key.startswith('edit.') else 12
                start=5.2 if self.key.startswith('edit.') else 5.5
                end=12
                if self.key in {'edit.redo','nav.forward'}:start,end=24-start,24-end
                scale=self.size/24
                neck=LineString([(start*scale,y*scale),(end*scale,y*scale)]).buffer(self.width/2,quad_segs=32,cap_style='round')
                silhouette=unary_union(list(raw.values()))
                primary=set_precision(raw['primary'].union(neck).intersection(silhouette).buffer(0),.000001)
                cache[front]={'primary':primary,'accent':silhouette.difference(primary)}
                self._geometry=cache
                return cache[front]
            back='primary' if front=='accent' else 'accent'
            cache[front]={front:raw[front],back:raw[back].difference(raw[front])}
            self._geometry=cache
            return cache[front]
        parts={'accent':[],'primary':[]}
        for p in self.paths:
            sampled=[]
            for d in rounded_edges(p['points'],p['closed'],p['radius']):
                values=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',d)))
                a=values[:2];control=values[2:4];end=values[4:6]
                if not sampled:sampled.append(tuple(a))
                for i in range(1,13):
                    t=i/12
                    sampled.append(tuple((1-t)**2*x+2*(1-t)*t*c+t*t*y for x,c,y in zip(a,control,end)))
                a=values[6:8];sampled.append(tuple(a));control=values[8:10];end=values[10:12]
                for i in range(1,13):
                    t=i/12
                    sampled.append(tuple((1-t)**2*x+2*(1-t)*t*c+t*t*y for x,c,y in zip(a,control,end)))
            parts[p['tone']].append(LineString(sampled).buffer(self.width/2,quad_segs=20,cap_style='round',join_style='round'))
        for c in self.circles:
            disk=Point(c['x'],c['y']).buffer(c['r']+(0 if c['filled'] else self.width/2),quad_segs=64)
            if not c['filled']:disk=disk.difference(Point(c['x'],c['y']).buffer(c['r']-self.width/2,quad_segs=64))
            parts[c['tone']].append(disk)
        for fill in self.fills:
            shape=Polygon()
            for ring in fill['rings']:shape=shape.symmetric_difference(Polygon(ring))
            parts[fill['tone']].append(shape)
        self._raw_geometry={tone:set_precision(unary_union(items),.000001) for tone,items in parts.items()}
        if self.clear_primary:
            self._raw_geometry['primary']=self._raw_geometry['primary'].difference(
                self._raw_geometry['accent'].buffer(.5*self.size/24,quad_segs=16))
        return self.geometry(front)


def construction(key,size):
    from b2_richtlijn import DRAWINGS, revised_construction
    if key in DRAWINGS:return revised_construction(Construction(key,size,1.25 if size==16 else 1.75))
    from b2_approved_proposals import APPROVED, approved_construction
    if key in APPROVED:return approved_construction(key,size)
    c=Construction(key,size,1.25 if size==16 else 1.75)
    if key in {'file.open','draw.note','view.search','measure.distance'}:
        original={'file.open':'open','draw.note':'note',
                  'view.search':'search','measure.distance':'measure'}[key]
        m=proposal_model(original,size,'round',True)
        for s in m.strokes:
            assert not s.accent_edges or len(s.accent_edges)==(len(s.points) if s.closed else len(s.points)-1)
            c.paths.append({'points':s.points,'closed':s.closed,'radius':3.6*size/24,
                            'tone':'accent' if s.accent_edges else 'primary'})
        if key=='edit.redo':c.mirror()
        return c
    if key=='file.new':
        c.line([(5,3),(14,3),(20,9),(20,21),(5,21)],closed=True,radius=1.5)
        c.line([(14.25,3.4),(14.25,8.75),(19.6,8.75)],radius=.5)
        c.plus(12,13.5,2.5)
    elif key in {'file.save','file.save-as'}:
        if key=='file.save-as':
            c.line([(3,3),(15,3),(20,8),(20,21),(3,21)],closed=True,radius=2)
            c.line([(7,3),(7,9),(14,9),(14,3)])
            c.line([(7,21),(7,15),(15,15),(15,21)],radius=1.4)
            c.line([(12,18),(19,11),(22,14),(15,21),(11,22)],True,True,radius=.5)
            if size==24:c.line([(17.5,12.5),(20.5,15.5)],True,radius=0)
            c.clear_primary=True
        else:
            c.line([(3,3),(16,3),(21,7),(21,21),(3,21)],closed=True)
            c.line([(7,3),(7,10),(15,10),(15,3)],True)
            c.line([(7,21),(7,15),(15,15),(15,21)])
    elif key in {'file.import','file.export'}:
        c.line([(3,15),(3,21),(21,21),(21,15)])
        if key=='file.import':
            c.line([(12,3),(12,15)],True);c.line([(8,11),(12,15),(16,11)],True)
        else:
            c.line([(12,15),(12,3)],True);c.line([(8,7),(12,3),(16,7)],True)
    elif key=='file.print':
        c.line([(7,8),(7,3),(17,3),(17,8)])
        c.line([(7,18),(3,18),(3,8),(21,8),(21,18),(17,18)])
        c.box(7,14,10,7,True)
        if size==24:c.circle(17.5,11,0.65,filled=True)
    elif key in {'edit.copy','edit.duplicate'}:
        c.line([(7,17),(3,17),(3,3),(15,3),(15,7)])
        c.box(8,8,13,13)
        if key=='edit.duplicate':c.plus(14.5,14.5,2.5)
        else:c.line([(11,12),(18,12)],True)
    elif key=='edit.paste':
        c.line([(7,5),(3,5),(3,20),(7,20)],radius=1.4)
        c.line([(12,5),(16,5),(16,8)],radius=1.4)
        c.box(7,3,5,4)
        c.box(10,10,11,11)
        c.line([(5,10),(5,15),(15,15)],True,radius=2)
        c.line([(12,12),(15,15),(12,18)],True,radius=1)
    elif key in {'edit.undo','edit.redo'}:
        c.line([(5.5,10),(20,10),(20,21)],radius=6)
        c.line([(9,4),(3,10),(9,16)],True,radius=3.6)
        if key=='edit.redo':c.mirror()
    elif key=='edit.cut':
        c.circle(6,6,3);c.circle(6,18,3)
        c.line([(8.2,8.2),(21,21)],True,radius=0)
        c.line([(8.2,15.8),(21,3)],radius=0)
    elif key in {'edit.delete','edit.clear-all'}:
        c.line([(8,6),(8,3),(16,3),(16,6)],True)
        c.line([(3,6),(21,6)])
        c.line([(5,6),(5,21),(19,21),(19,6)])
        if key=='edit.delete':
            for x in ([9,15] if size==24 else [12]):c.line([(x,10),(x,17)])
        else:
            c.line([(9,11),(15,17)],True);c.line([(15,11),(9,17)],True)
    elif key=='edit.select':
        c.line([(4,3),(4,21),(10,15),(15,21),(18,18),(12,12),(21,10)],closed=True,radius=1.6)
    elif key=='edit.select-all':
        for p in [[(3,8),(3,3),(8,3)],[(16,3),(21,3),(21,8)],[(21,16),(21,21),(16,21)],[(8,21),(3,21),(3,16)]]:c.line(p)
        c.line([(7,12),(10,15),(17,8)],True,radius=1.2)
    elif key in {'view.zoom-in','view.zoom-out'}:
        c.circle(9,9,6.5);c.line([(13.6,13.6),(21,21)])
        c.line([(6,9),(12,9)],True)
        if key=='view.zoom-in':c.line([(9,6),(9,12)],True)
    elif key in {'view.fit','view.fit-selection','view.fit-page','view.fit-width'}:
        for p in [[(3,8),(3,3),(8,3)],[(16,3),(21,3),(21,8)],[(21,16),(21,21),(16,21)],[(8,21),(3,21),(3,16)]]:c.line(p)
        if key=='view.fit':
            c.line([(7,12),(12,7),(17,12),(12,17)],True,True,radius=1)
        elif key=='view.fit-selection':
            c.box(8,8,8,8,True)
        elif key=='view.fit-page':
            c.box(8,6,8,12,True)
        else:
            c.line([(6,12),(18,12)],True)
            c.line([(8.5,9.5),(6,12),(8.5,14.5)],True)
            c.line([(15.5,9.5),(18,12),(15.5,14.5)],True)
    elif key=='view.pan':
        c.line([(8,11),(8,5),(11,5),(11,3),(14,3),(14,5),(17,5),(17,7),(20,7),(20,16),(16,21),(10,21),(4,15),(4,12),(7,12),(9,15)],closed=False,radius=1.8)
        c.line([(11,5),(11,10)]);c.line([(14,5),(14,10)])
        c.line([(17,7),(17,11)],True)
    elif key=='view.orbit':
        c.circle(12,12,6.5)
        tilt=math.radians(-15)
        points=[(12+9.5*math.cos(i*math.tau/96)*math.cos(tilt)-3.6*math.sin(i*math.tau/96)*math.sin(tilt),
                 12+9.5*math.cos(i*math.tau/96)*math.sin(tilt)+3.6*math.sin(i*math.tau/96)*math.cos(tilt)) for i in range(96)]
        c.line(points,True,True,radius=0)
    elif key=='nav.home':
        c.line([(3,10),(12,3),(21,10)])
        c.line([(5,9),(5,21),(19,21),(19,9)])
        c.line([(10,21),(10,14),(14,14),(14,21)],True)
    elif key in {'nav.back','nav.forward'}:
        c.line([(20,12),(6,12)])
        c.line([(10,6),(4,12),(10,18)],True,radius=2)
        if key=='nav.forward':c.mirror()
    elif not extend(c,key) and not extend_windows(c,key) and not extend_text(c,key) and not extend_data(c,key) and not extend_report(c,key) and not extend_ifc(c,key) and not extend_next(c,key) and not extend_later(c,key) and not extend_pages(c,key) and not extend_bulk(c,key) and not extend_session(c,key) and not extend_document_navigation(c,key) and not extend_third(c,key) and not extend_fourth(c,key) and not extend_completion(c,key):raise ValueError(key)
    refine(c,key)
    return c


def path_data(geometry):
    if geometry.is_empty:return ''
    # A precise contour difference may leave zero-area line fragments at tangencies.
    # SVG fills contain polygon areas only; preserve every polygon and its holes.
    def polygon_parts(g):
        if g.geom_type=='Polygon':yield g
        elif hasattr(g,'geoms'):
            for part in g.geoms:yield from polygon_parts(part)
    polygons=list(polygon_parts(geometry))
    def ring(coords):return 'M'+'L'.join(f'{x:.6f} {y:.6f}' for x,y in list(coords)[:-1])+'Z'
    return ''.join(ring(p.exterior.coords)+''.join(ring(i.coords) for i in p.interiors) for p in polygons)


def export_svg(model,front=None):
    front=front or foreground(model.key)
    geometry=model.geometry(front)
    for tone,g in geometry.items():
        assert g.is_valid,(model.key,model.size,tone,'invalid geometry')
        if not g.is_empty:
            a,b,c,d=g.bounds
            assert min(a,b)>=0 and max(c,d)<=model.size,(model.key,model.size,tone,g.bounds)
    assert geometry['primary'].area>0
    assert geometry['primary'].intersection(geometry['accent']).area<0.00005,(model.key,model.size,'colour overlap',geometry['primary'].intersection(geometry['accent']).area)
    result=[]
    for tone in (('primary','accent') if front=='accent' else ('accent','primary')):
        fill='currentColor' if tone=='primary' else 'var(--icon-accent,currentColor)'
        result.append(f'<path data-part="{tone}" fill="{fill}" fill-rule="evenodd" d="{path_data(geometry[tone])}"/>')
    colour_style=' style="color:var(--icon-accent,currentColor)"' if model.key in WHOLE_ACCENT else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{model.size}" height="{model.size}" viewBox="0 0 {model.size} {model.size}" stroke="none"{colour_style}>'+''.join(result)+'</svg>'
