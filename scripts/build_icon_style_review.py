"""Render the before/after review of B using preserved originals and new SVGs."""
import json
from pathlib import Path


FIXES={
 'open':'Het accent volgt nu de echte schuine map-tab. De verschoven tweede tab is weg.',
 'save':'De bodem van de opslaguitsparing is één exclusief accentsegment; geen kort streepje tegen de buitenrand.',
 'import':'Pijl en bak blijven apart. De pijl wordt als één kleurvlak getekend, zonder stapeling bij de pijlpunt.',
 'export':'Dezelfde constructie als Importeren, met de tegengestelde richting. Geen losse eindkapjes.',
 'undo':'De terugkeerpunt en hals vormen samen het accent. De witte staart begint exact aan het kleurscheidingsvlak.',
 'search':'Het accent is de echte bovenzijde van de lens. Het losse binnenhoekje is weg; de steel raakt de lens.',
 'select':'Het accentpunt ligt exact op de schuine buitenrand. De scherpe tip heeft een gecontroleerde afschuining.',
 'move':'De vier armen stoppen aan het middenblok. Het accent ligt niet langer over een doorlopend kruis.',
 'measure':'Het accent is het afgeschuinde uiteinde van de liniaal, geen tick die over de buitenrand steekt.',
 'layers':'Beide voorste randen komen uit dezelfde ruit. Geen tweede, iets afwijkende schuine lijn.',
 'note':'Alleen de echte afschuining is gekleurd. Het onjuiste extra L-hoekje is verwijderd.',
 'cpt':'Het losse registratiestreepjespaar is verwijderd. De onderste markering is alleen accent, niet dubbel getekend.',
 'cloud':'Eén bestaande meetpuntvorm is accent. Het extra grote blok en de botsende kaderlijn zijn weg.',
 'delete':'Het accent is de bovenrand van het handvat. De kleurvlakken delen dezelfde berekende hoekpunten.',
}


def render_review(root,functions,models):
    labels={k:label for k,_,label,_ in functions}
    order=['open','select','layers','note','undo','save','move','search','measure','cloud','cpt','delete','import','export']
    records=[]
    for key in order:
        before={str(s):(root/'review/before'/str(s)/(key+'.svg')).read_text(encoding='utf-8') for s in (16,24)}
        after={str(s):(root/'b'/str(s)/(key+'.svg')).read_text(encoding='utf-8') for s in (16,24)}
        records.append({'key':key,'label':labels[key],'fix':FIXES[key],'before':before,'after':after,
                        'construction':{str(s):models[key,s].wireframe() for s in (16,24)}})
    payload=json.dumps(records,ensure_ascii=False).replace('</','<\\/')
    (root/'b-review.html').write_text(PAGE.replace('/* DATA */',payload),encoding='utf-8')


PAGE=r'''<!doctype html><html lang="nl" data-theme="dark"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · B — accentcorrecties vóór en na</title><style>
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf')}@font-face{font-family:Space;src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf')}@font-face{font-family:Mono;src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
:root{--bg:#2a2a32;--surface:#33333c;--ink:#edebe8;--muted:#bcb8b2;--border:#55555f;--icon-accent:#f59e0b;--construction:#67e8f9;--zoom:88px;color-scheme:dark}
[data-theme=light]{--bg:#f1eeea;--surface:#fafaf9;--ink:#36363e;--muted:#655f59;--border:#d7d1ca;--icon-accent:#b45309;--construction:#0369a1;color-scheme:light}
[data-theme=blueprint]{--bg:#0f1b2d;--surface:#17273d;--ink:#e0e7ff;--muted:#aebfda;--border:#496482;--icon-accent:#83bdff}
[data-theme=contrast]{--bg:#000;--surface:#000;--ink:#fff;--muted:#fff;--border:#fff;--icon-accent:#f59e0b}
[data-theme=contrast-light]{--bg:#fff;--surface:#fff;--ink:#000;--muted:#000;--border:#000;--icon-accent:#92400e;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 Inter,system-ui}header,main{max-width:1440px;margin:auto;padding:28px}header{padding-bottom:8px}h1,h2{font-family:Space;line-height:1.15;letter-spacing:-.02em}h1{font-size:36px;margin:10px 0}h2{font-size:21px;margin:0}.eyebrow{font:11px Mono;color:var(--icon-accent);text-transform:uppercase;letter-spacing:.08em}p{color:var(--muted)}header p{max-width:900px}a{color:var(--icon-accent)}.controls{position:sticky;top:0;z-index:3;display:flex;gap:18px;align-items:center;flex-wrap:wrap;background:var(--bg);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:14px 0;margin-bottom:20px}label{display:flex;gap:7px;align-items:center}select,input{font:inherit;background:var(--surface);color:var(--ink);border:1px solid var(--border);padding:7px;border-radius:4px}input[type=checkbox]{accent-color:var(--icon-accent)}input[type=search]{max-width:200px}select:focus-visible,input:focus-visible{outline:2px solid var(--icon-accent);outline-offset:2px}.facts{display:flex;gap:24px;flex-wrap:wrap;padding:15px 20px;border-left:3px solid var(--icon-accent);background:var(--surface);margin-bottom:22px;font:12px Mono}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.card{border:1px solid var(--border);border-radius:10px;background:var(--surface);padding:20px;min-width:0}.card p{font-size:13px;min-height:65px}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:10px}.sample{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:12px;min-width:0}.label{font:11px Mono;color:var(--muted);margin-bottom:14px}.after .label{color:var(--icon-accent)}.big{display:flex;justify-content:center;align-items:center;height:120px}.big svg{width:var(--zoom);height:var(--zoom)}.native{display:flex;justify-content:space-around;align-items:flex-end;gap:8px;margin-top:16px;min-height:53px}.native>div{display:flex;align-items:center;flex-direction:column;gap:8px}.native small{font:10px Mono;color:var(--muted)}.construction-layer{display:none}.construction .construction-layer{display:inline}.mono{--icon-accent:var(--ink)}.foot{border-top:1px solid var(--border);margin-top:24px;padding-top:20px;color:var(--muted);font-size:12px}.hidden{display:none}@media(max-width:1100px){.grid{grid-template-columns:1fr 1fr}}@media(max-width:700px){.grid{grid-template-columns:1fr}.controls{position:static}.card p{min-height:0}header,main{padding:18px}h1{font-size:29px}}
</style><header><div class="eyebrow">OpenAEC / gekozen stijl B / revisie 02</div><h1>Gecorrigeerde accentlijnen.</h1><p>De oude versie staat links, de hertekende versie rechts. Het accent is nu een exact onderdeel van de constructie. Geen benaderde lijnen over een andere contour; iedere kleur krijgt zijn eigen vlak.</p><a href="index.html">Terug naar de stijlproef en het lint →</a></header><main>
<div class="controls"><label>Thema <select id="theme" aria-label="Reviewthema"><option value="dark">Donker</option><option value="light">Licht</option><option value="blueprint">Blueprint</option><option value="contrast">Contrast donker</option><option value="contrast-light">Contrast licht</option></select></label><label>Uitvergroting <select id="zoom" aria-label="Uitvergroting"><option value="88">88 px</option><option value="128">128 px</option></select></label><label><input id="wire" type="checkbox"> Toon ankerpunten</label><label><input id="mono" type="checkbox"> Eén kleur</label><input id="search" type="search" aria-label="Zoek icoon" placeholder="Zoek icoon…"></div>
<div class="facts"><span>14 functies</span><span>28 gecontroleerde masters</span><span>0 geometrische overlap tussen kleuren</span><span>16 / 24 / 32 px op ware grootte</span></div><section class="grid" id="grid"></section><div class="foot"><b>Het model is een 2D-vectormodel.</b> Ankerpunten en lijnbreedte bepalen de contour; gekleurde segmenten delen exact dezelfde hoekpunten. Voor export worden de lijnen één keer omgezet naar gevulde SVG-paden, zodat uiteinden en hoeken niet per renderer anders worden opgebouwd. De 16px-versies hebben hun eigen constructie. <a href="model-b.json">Constructiemodel</a> · <a href="geometry-validation.json">Geometriecontrole</a> · <a href="openaec-icon-style-samples.zip">SVG-download</a><p>De mathematische controle toetst overlap en begrenzing. Leesbaarheid en rasterweergave zijn daarnaast in de browser op echte pixelmaten beoordeeld. De voorbeeldkleuren staan los van de thema’s die Claude beheert.</p></div></main>
<script id="data" type="application/json">/* DATA */</script><script>
const records=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function resize(svg,size){return svg.replace(/\bwidth="\d+"/,`width="${size}"`).replace(/\bheight="\d+"/,`height="${size}"`)}function sample(r,side){return `<div class="sample ${side}"><div class="label">${side==='before'?'VOOR':'B / HERSTELD'}</div><div class="big">${side==='after'?r.after[24].replace('</svg>',`<g class="construction-layer">${r.construction[24]}</g></svg>`):r.before[24]}</div><div class="native">${[16,24,32].map(s=>`<div>${resize(r[side][s===16?16:24],s)}<small>${s} px</small></div>`).join('')}</div></div>`}function render(){const q=$('#search').value.toLowerCase();$('#grid').innerHTML=records.filter(r=>(r.label+' '+r.key).toLowerCase().includes(q)).map(r=>`<article class="card"><h2>${esc(r.label)}</h2><p>${esc(r.fix)}</p><div class="comparison">${sample(r,'before')}${sample(r,'after')}</div></article>`).join('')}$('#theme').onchange=()=>document.documentElement.dataset.theme=$('#theme').value;$('#zoom').onchange=()=>document.documentElement.style.setProperty('--zoom',$('#zoom').value+'px');$('#wire').onchange=()=>document.body.classList.toggle('construction',$('#wire').checked);$('#mono').onchange=()=>document.body.classList.toggle('mono',$('#mono').checked);$('#search').oninput=render;render();
</script></html>'''
