"""Convert the bundled OpenAEC heading font into deterministic icon contours."""
from pathlib import Path
import hashlib
import sys
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'harmonization/sources/b2-runtime'))
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

FONT_SPECS={'format.bold':('B','Bold',4,20,0),
            'format.italic':('I','Medium',4,20,.22),
            'format.underline':('U','Medium',3,17,0),
            'format.color':('A','Medium',3,17,0)}


class OutlinePen(BasePen):
    def __init__(self,glyph_set):
        super().__init__(glyph_set);self.contours=[];self.points=[]
    def _moveTo(self,p):self.points=[p]
    def _lineTo(self,p):self.points.append(p)
    def _qCurveToOne(self,b,d):
        a=self._getCurrentPoint()
        for i in range(1,25):
            t=i/24;self.points.append(tuple((1-t)**2*a[j]+2*(1-t)*t*b[j]+t*t*d[j] for j in (0,1)))
    def _curveToOne(self,b,d,e):
        a=self._getCurrentPoint()
        for i in range(1,33):
            t=i/32;self.points.append(tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*d[j]+t**3*e[j] for j in (0,1)))
    def _closePath(self):self.contours.append(self.points);self.points=[]
    def _endPath(self):self._closePath()


@lru_cache(maxsize=4)
def letter_contours(letter,weight):
    path=ROOT/'assets/fonts'/('SpaceGrotesk-'+weight+'.ttf')
    font=TTFont(path);glyphs=font.getGlyphSet();name=font.getBestCmap()[ord(letter)]
    pen=OutlinePen(glyphs);glyphs[name].draw(pen);font.close()
    return pen.contours


def add_letter(c,key):
    letter,weight,top,bottom,slant=FONT_SPECS[key]
    contours=letter_contours(letter,weight)
    all_points=[p for ring in contours for p in ring]
    low=min(y for x,y in all_points);high=max(y for x,y in all_points)
    scale=(bottom-top)/(high-low)
    rings=[[(x*scale+slant*(y-low)*scale,bottom-(y-low)*scale) for x,y in ring] for ring in contours]
    xs=[x for ring in rings for x,y in ring];center=(min(xs)+max(xs))/2
    c.fills.append({'tone':'primary','rings':[[( (x-center+12)*c.size/24,y*c.size/24) for x,y in ring] for ring in rings]})


def font_sources():
    return {key:{'family':'Space Grotesk','glyph':v[0],'weight':v[1],
                 'source':f'assets/fonts/SpaceGrotesk-{v[1]}.ttf',
                 'sha256':hashlib.sha256((ROOT/f'assets/fonts/SpaceGrotesk-{v[1]}.ttf').read_bytes()).hexdigest(),
                 'synthetic_slant':v[4],'license':'SIL OFL 1.1',
                 'sampling':'24 steps per quadratic segment; 32 per cubic segment'}
            for key,v in FONT_SPECS.items()}
