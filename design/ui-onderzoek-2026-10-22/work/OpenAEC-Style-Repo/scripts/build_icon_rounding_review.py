"""Separate B shape/accent proposals; keep approved source masters untouched."""
from pathlib import Path
from copy import deepcopy
import json
import math
import xml.etree.ElementTree as ET
from icon_geometry import build_b_model

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'design/icon-style-proposals/rounding'
LABELS = {'open':'Openen', 'note':'Opmerking', 'undo':'Ongedaan',
          'search':'Zoeken', 'measure':'Afstand meten'}
REASONS = {
 'open':'Voorstel: de opening van de map krijgt kleur; het schuine tabje wordt rustig.',
 'note':'Voorstel: de eerste tekstregel krijgt kleur; het hoekje is alleen onderdeel van de vorm.',
 'undo':'Voorstel: alleen de pijlpunt krijgt kleur; de hals en teruggaande lijn blijven één hoofdkleur.',
 'search':'Voorstel: de steel krijgt kleur; geen los kleurstuk boven in de lens.',
 'measure':'Voorstel: de maatstreepjes krijgen kleur; de buitencontour blijft één geheel.'}


def number(v):
    return f'{v:.5f}'.rstrip('0').rstrip('.') or '0'


def xy(p):
    return ' '.join(number(v) for v in p)


def mix(a,b,t):
    return tuple(x+(y-x)*t for x,y in zip(a,b))


def rounded_edges(points, closed, radius):
    """Split each quadratic corner at its midpoint for exact colour seams."""
    n=len(points); corners=[]
    for i,v in enumerate(points):
        if not closed and i in (0,n-1):
            corners.append((v,v,v,v,v));continue
        prev,nxt=points[(i-1)%n],points[(i+1)%n]
        before=math.dist(prev,v);after=math.dist(v,nxt)
        trim=min(radius,before*.32,after*.32)
        incoming=mix(v,prev,trim/before);outgoing=mix(v,nxt,trim/after)
        c1=mix(incoming,v,.5);c2=mix(v,outgoing,.5)
        midpoint=mix(c1,c2,.5)
        corners.append((incoming,outgoing,c1,c2,midpoint))
    result=[]
    for i in range(n if closed else n-1):
        a,b=corners[i],corners[(i+1)%n]
        result.append(f'M{xy(a[4])}Q{xy(a[3])} {xy(a[1])}L{xy(b[0])}Q{xy(b[2])} {xy(b[4])}')
    return result


def proposal_model(key,size,style,logical):
    m=deepcopy(build_b_model(key,size))
    scale=size/24
    def pts(big):return [(x*scale,y*scale) for x,y in big]
    if style=='round':
        if key=='search':
            m.strokes[0].points=[(8.5*scale+7.5*scale*math.cos(t*math.tau/40),
                                 10.5*scale+7.5*scale*math.sin(t*math.tau/40)) for t in range(40)]
            m.strokes[0].accent_edges=tuple(range(29,34))
            m.strokes[1].points=pts([(13.8,15.8),(21,23)])
        elif key=='open':
            m.strokes[0].points=pts([(3,8),(3,4),(9,4),(12,7),(21,7),(21,21),(3,21)])
            # Meet the rounded top-right contour, not its removed sharp corner.
            m.strokes[1].points=pts([(3,10),(17,10),(20.28,7.72)])
        elif key=='note':
            m.strokes[0].points=pts([(3,3),(21,3),(21,17),(9,17),(3,21)])
            m.strokes[0].accent_edges=(1,)
        elif key=='measure':
            m.strokes[0].points=pts([(3,16),(16,3),(21,8),(8,21)])
            m.strokes[0].accent_edges=(1,)
        elif key=='undo':
            m.strokes[2].points=pts([(10,10),(20,10),(20,21)])
    if logical:
        chosen={'open':{'lip'},'note':{'text-0'},'undo':{'return-head'},
                'search':{'handle'},'measure':{'tick-0','tick-1'}}[key]
        for s in m.strokes:
            count=len(s.points) if s.closed else len(s.points)-1
            s.accent_edges=tuple(range(count)) if s.name in chosen else ()
        if key=='undo':
            # Join the white shaft to the inside of the coloured arrowhead.
            m.strokes[1].points[0]=(3*scale+m.width/2,10*scale) if size==24 else (2+m.width/2,6)
    return m


def svg(key,size,style,logical):
    if style=='original' and not logical:
        return (ROOT/f'design/icon-style-proposals/b/{size}/{key}.svg').read_text(encoding='utf-8')
    m=proposal_model(key,size,style,logical)
    if style=='original':
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" stroke="none">'+m.markup()+'</svg>'
    radius={'original':0,'soft':1.15,'round':3.6}[style]*size/24
    parts={'primary':[],'accent':[]}
    for s in m.strokes:
        runs=[]
        for i,d in enumerate(rounded_edges(s.points,s.closed,radius)):
            tone='accent' if i in s.accent_edges else 'primary'
            if runs and runs[-1][0]==tone:
                runs[-1][1]+=d[d.index('Q'):]
            else:runs.append([tone,d])
        for tone,d in runs:
            if s.closed and len(runs)==1:d+='Z'
            parts[tone].append(f'<path fill="none" d="{d}"/>')
        if style!='original' and not s.closed:
            for index,edge in [(0,0),(-1,len(s.points)-2)]:
                tone='accent' if edge in s.accent_edges else 'primary'
                x,y=s.points[index]
                parts[tone].append(f'<circle cx="{number(x)}" cy="{number(y)}" r="{number(m.width/2)}" stroke="none"/>')
    result=[]
    # Paint the structural outline last: accent endpoints disappear beneath it.
    for tone in ('accent','primary'):
        paths=parts[tone]
        colour='currentColor' if tone=='primary' else 'var(--icon-accent,currentColor)'
        # Circles use the same paint as their owning edge; paths remain unfilled.
        result.append(f'<g data-part="{tone}" stroke="{colour}" fill="{colour}">'+''.join(paths)+'</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" stroke-width="{m.width}" stroke-linecap="butt" stroke-linejoin="round">'+''.join(result)+'</svg>'


PAGE='''<!doctype html><html lang="nl" data-theme="dark"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B · ronding en accentplaatsing</title><style>
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui}html{--bg:#2a2a32;--panel:#34343e;--ink:#edebe8;--muted:#bab7b2;--line:#55555f;--icon-accent:#f59e0b;color-scheme:dark}html[data-theme=light]{--bg:#f1eeea;--panel:#fff;--ink:#292931;--muted:#62616b;--line:#c9c5be;--icon-accent:#a65b00;color-scheme:light}main{max-width:1280px;margin:auto;padding:36px 30px}h1{font-size:32px;margin:8px 0}h2{font-size:18px;margin:0}a{color:inherit}p{max-width:880px;color:var(--muted)}.eyebrow{font-size:12px;letter-spacing:.15em;color:var(--icon-accent)}.controls{display:flex;flex-wrap:wrap;gap:22px;align-items:center;background:var(--bg);position:sticky;top:0;padding:18px 0;z-index:1}select,input{font:inherit}select{padding:7px;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px}.head,.row{display:grid;grid-template-columns:1.1fr repeat(3,1fr);gap:14px}.head{margin-top:18px}.head>div{padding:12px}.row{border-top:1px solid var(--line);padding:18px 0}.info{padding:18px 10px}.info p{font-size:13px}.cell{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;align-items:center}.big{height:104px;display:flex;align-items:center}.big svg{width:74px;height:74px}.native{display:flex;gap:23px;height:68px;align-items:flex-end}.native>div{display:flex;flex-direction:column;gap:8px;align-items:center;font-size:10px;color:var(--muted)}.native svg{color:var(--ink)}.mono{--icon-accent:currentColor!important}.badge{font-size:11px;color:var(--icon-accent)}footer{border-top:1px solid var(--line);padding:20px 0;font-size:13px;color:var(--muted)}@media(max-width:760px){main{padding:20px 12px}.head,.row{grid-template-columns:repeat(3,1fr);gap:6px}.head>div:first-child{display:none}.info{grid-column:1/-1;padding:4px}.info p{margin:4px 0}.native{gap:8px}.cell{padding:8px}.big svg{width:58px;height:58px}.head>div{padding:4px;font-size:12px}}
</style><main><div class="eyebrow">OPENAEC / ICONEN / ONTWERPVERGELIJKING</div><h1>B, met ruimte voor rondere vormen</h1><p>Vijf iconen die je aanwees. Vergelijk de vorm en de betekenis van het accent apart. Dit zijn voorstellen; de bestaande B-masters blijven bewaard.</p><div class="controls"><label>Thema <select id="theme"><option value="dark">Donker</option><option value="light">Licht</option></select></label><label>Accentplaatsing <select id="placement"><option value="logical">Nieuw voorstel — betekenisvol onderdeel</option><option value="old">Huidige plaatsing</option></select></label><label><input type="checkbox" id="mono"> Eén kleur</label><label>Accentkleur <input type="color" id="accent" value="#f59e0b"></label></div><div class="head"><div><b>Functie / accentvoorstel</b></div><div><b>B0 · hoekig</b><br><small>Huidige vorm als referentie</small></div><div><b>B1 · verzacht</b><br><small>Kleine rondingen, karakter van B</small></div><div><b>B2 · ronder</b><br><small>Grotere rondingen en een ronde lens</small></div></div><div id="rows"></div><footer>Bron: B-constructiemodel, afzonderlijke 16/24px-masters. 32px gebruikt de 24px-master. Nieuwe rondingen zijn kwadratische vectorcurven met gedeelde eindpunten tussen kleursegmenten. Deze voorstellen gebruiken SVG-strokes; omzetting naar definitieve gevulde contouren en de bijbehorende geometriecontrole volgen na de vormkeuze. Voorbeeldkleuren staan los van de productiethema’s.<br><a href="../b-review.html">Terug naar eerdere accentcorrecties</a> · <a href="manifest.json">Bron en varianten</a></footer></main><script id="data" type="application/json">DATA</script><script>const data=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);function sized(s,n){return s.replace(/width="\\d+"/,`width="${n}"`).replace(/height="\\d+"/,`height="${n}"`)}function render(){let mode=$('#placement').value;$('#rows').innerHTML=data.map(r=>`<section class="row"><div class="info"><h2>${r.label}</h2><p>${r.reason}</p><span class="badge">${mode==='logical'?'NIEUWE ACCENTPLAATSING':'HUIDIGE ACCENTPLAATSING'}</span></div>${['original','soft','round'].map(v=>`<div class="cell"><div class="big">${r.variants[v][mode][24]}</div><div class="native">${[16,24,32].map(n=>`<div>${sized(r.variants[v][mode][n===16?16:24],n)}<span>${n} px</span></div>`).join('')}</div></div>`).join('')}</section>`).join('')}$('#placement').onchange=render;$('#theme').onchange=()=>{document.documentElement.dataset.theme=$('#theme').value;document.documentElement.style.removeProperty('--icon-accent');$('#accent').value=$('#theme').value==='light'?'#a65b00':'#f59e0b'};$('#mono').onchange=()=>document.body.classList.toggle('mono',$('#mono').checked);$('#accent').oninput=()=>document.documentElement.style.setProperty('--icon-accent',$('#accent').value);render();</script></html>'''


PAGE=PAGE.replace('B, met ruimte voor rondere vormen','B2 gekozen · rond en zacht').replace(
    'Vijf iconen die je aanwees. Vergelijk de vorm en de betekenis van het accent apart. Dit zijn voorstellen; de bestaande B-masters blijven bewaard.',
    'B2 is gekozen als basis voor de iconenfamilie. De accentkleur wordt eerst getekend; de hoofdkleur ligt erboven bij aansluitingen. B0 en B1 blijven vergelijkingsmateriaal.').replace(
    '<b>B2 · ronder</b>','<b>B2 · gekozen</b>').replace(
    'omzetting naar definitieve gevulde contouren en de bijbehorende geometriecontrole volgen na de vormkeuze.',
    'omzetting naar definitieve gevulde contouren en de bijbehorende geometriecontrole zijn de volgende uitwerking. Accent wordt onder de hoofdkleur getekend; die volgorde geldt ook in andere thema’s.')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[];count=0
    for key,label in LABELS.items():
        variants={}
        for style in ('original','soft','round'):
            variants[style]={}
            for placement,logical in [('old',False),('logical',True)]:
                variants[style][placement]={}
                for size in (16,24):
                    content=svg(key,size,style,logical)
                    node=ET.fromstring(content)
                    if style!='original':
                        assert [g.attrib.get('data-part') for g in node]==['accent','primary'], (key,size,style,placement)
                    path=OUT/style/placement/str(size)/(key+'.svg')
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_text(content,encoding='utf-8')
                    variants[style][placement][size]=content;count+=1
        records.append({'key':key,'label':label,'reason':REASONS[key],'variants':variants})
    manifest={'status':'B2 gekozen; nog geen definitieve masters', 'selected_style':'round',
              'paint_order':['accent','primary'], 'source':'scripts/icon_geometry.py',
              'generator':'scripts/build_icon_rounding_review.py','functions':list(LABELS),
              'styles':['original','soft','round'],'accent_modes':['old','logical'],'svg_files':count,
              'masters':[16,24],'renderer':'SVG quadratic curves with shared tangent seams; strokes, not production filled outlines'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'index.html').write_text(PAGE.replace('DATA',json.dumps(records,ensure_ascii=False)),encoding='utf-8')
    print(json.dumps({'status':'gegenereerd','svg_files':count,'functions':len(records)}))


if __name__=='__main__':main()
