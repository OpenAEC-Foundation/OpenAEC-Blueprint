"""Screenshot feedback review; alternatives remain outside the canonical exports."""
import json
from b2_geometry import Construction, export_svg
from b2_second_series import box

# Local review proposal: shared theme tokens still specify yellow warnings.
WARNING_PREVIEW={'light':'#9A3412','dark':'#FDBA74','blueprint':'#FDBA74',
                 'high-contrast-dark':'#FDBA74','high-contrast-light':'#7C2D12'}
FEEDBACK={
 'measure.area':'Arcering sluit op de binnenrand aan.',
 'draw.circle':'Gekozen: B, constructiestraal in accentkleur.',
 'draw.text':'Gekozen: de gehele T in accentkleur.',
 'draw.textbox':'De gehele T in accentkleur.',
 'draw.dimension':'Hulplijnen staan vrij van de pijlpunten.',
 'object.show':'Vloeiende oogcontour met ronde boven- en onderboog.',
 'object.hide':'Dezelfde oogcontour, met de zichtbaarheidstreep ervoor.',
 'object.align-left':'Verticale uitlijnlijn als accent.',
 'object.align-right':'Verticale uitlijnlijn als accent.',
 'view.grid':'Gekozen: alle binnenlijnen accent, buitenrand in hoofdkleur.',
 'ui.settings':'Alle drie de schuifknoppen als accent, ook op 16 px.',
 'status.warning':'Oranje voorstel; gedeelde warning-token staat nog geel.',
 'status.busy':'Draaiende ring in deze review; klokje als alternatief.',
 'ui.help':'Vraagteken 20% kleiner; meer ruimte tot de ongewijzigde cirkel.',
 'draw.polygon':'Zeshoek die duidelijk verschilt van een rechthoek.',
 'draw.rectangle':'Vier accentpunten op de hoeken.',
}


ROUND_TWO={'draw.circle','draw.text','view.grid','ui.help'}


def render_feedback_review(out,entries,themes):
    alternatives={}
    for key in ('grid-inner','busy-clock','circle-radius','circle-center'):
        assets={}
        for size in (16,24):
            c=Construction(key,size,1.25 if size==16 else 1.75)
            if key=='grid-inner':
                box(c,4,4,16,16)
                for p in ([12] if size==16 else [9.3333,14.6667]):
                    c.line([(p,4),(p,20)],True);c.line([(4,p),(20,p)],True)
            elif key.startswith('circle-'):
                c.circle(12,12,7.5)
                if key=='circle-radius':c.line([(12,12),(17.3033,6.6967)],True)
                else:c.circle(12,12,1.4,True,True)
            else:
                c.circle(12,12,8.5);c.line([(12,7),(12,12),(16,14)],radius=1)
            content=export_svg(c)
            path=out/'review/feedback-options'/str(size)/(key+'.svg')
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
            assets[str(size)]=content
        alternatives[key]=assets
    records=[]
    for e in entries:
        if e['id'] not in FEEDBACK:continue
        records.append({'id':e['id'],'label':e['label'],'note':FEEDBACK[e['id']],
                        'semantic':e['semantic_color'],
                        'before':{str(s):(out/('review/selected-before' if e['id'] in {'draw.text','draw.circle'} else 'review/feedback-round-2-before' if e['id'] in ROUND_TWO else 'review/feedback-before')/str(s)/(e['id']+'.svg')).read_text(encoding='utf-8') for s in (16,24)},
                        'after':{str(s):(out/e['assets'][str(s)]['path']).read_text(encoding='utf-8') for s in (16,24)}})
    data={'icons':records,'themes':themes,'warning_preview':WARNING_PREVIEW,'alternatives':alternatives}
    (out/'feedback.html').write_text(PAGE.replace('/* DATA */',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')


PAGE=r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2 · screenshotfeedback</title><style>
*{box-sizing:border-box}body{font:14px/1.5 system-ui;margin:0;background:var(--bg);color:var(--ink)}main{max-width:1400px;margin:auto;padding:30px}h1{font-size:30px}p{max-width:850px;color:var(--muted)}a{color:inherit}.controls{display:flex;gap:18px;flex-wrap:wrap;align-items:center;position:sticky;top:0;background:var(--bg);padding:16px 0;z-index:2}select,button{background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:8px;border-radius:6px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:18px}.card{padding:20px;background:var(--panel);border:1px solid var(--line);border-radius:10px}.card h2{font-size:17px;margin:0}.card p{font-size:12px;min-height:36px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}.version{text-align:center;border-top:1px solid var(--line);padding-top:12px}.version b{font-size:12px}.hero{height:85px;display:grid;place-items:center}.hero svg{width:58px;height:58px}.native{display:flex;align-items:end;justify-content:center;gap:20px}.native>div{display:grid;justify-items:center;gap:6px}.native span{font-size:10px;color:var(--muted)}.mono{--icon-accent:currentColor!important}.motion .spin svg{animation:spin 1.4s linear infinite;transform-origin:center;transform-box:fill-box}.paused .spin svg{animation:none}@keyframes spin{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.motion .spin svg{animation:none!important}}.circle-options{display:grid;grid-template-columns:1fr 1fr;gap:12px}.alternative{margin-top:20px;padding-top:15px;border-top:1px solid var(--line)}code{font-size:11px;color:var(--muted)}
</style><main><a href="series-2.html">← Tweede serie</a><h1>Jouw screenshotfeedback verwerkt</h1><p>Voor en na op 16, 24 en 32 px. Tweede ronde: kleiner vraagteken, gekozen rasterbinnenlijnen, Tekst geheel in accent en Cirkel B gekozen. Bezig behoudt de ring en het klok-alternatief. De draaiende ring is een demonstratie in de review; de losse SVG blijft statisch. Systeemvoorkeur voor minder beweging wordt gerespecteerd.</p><p>Waarschuwing: oranje is hier een kleurvoorstel. Het gedeelde tokenbestand bevat nog geel; Claude’s themabestanden zijn niet gewijzigd.</p><div class="controls"><label>Thema <select id="theme"></select></label><label><input id="mono" type="checkbox"> Eén kleur per icoon</label><label><input id="motion" type="checkbox" checked> Animatie Bezig</label></div><div class="grid" id="cards"></div></main><script id="data" type="application/json">/* DATA */</script><script>
const d=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);$('#theme').innerHTML=Object.entries(d.themes).map(([k,v])=>`<option value="${k}">${v.name}</option>`).join('');$('#theme').value='dark';
function resized(s,n){return s.replace(/width="\d+"/,`width="${n}"`).replace(/height="\d+"/,`height="${n}"`)}
function version(svg,label,spin=false){return `<div class="version"><b>${label}</b><div class="hero ${spin?'spin':''}">${svg[24]}</div><div class="native ${spin?'spin':''}">${[16,24,32].map(n=>`<div>${resized(svg[n===16?16:24],n)}<span>${n} px</span></div>`).join('')}</div></div>`}
function render(){let c=d.themes[$('#theme').value].color;for(let [k,v] of Object.entries({bg:c.frame,panel:c.panel,ink:c.text,muted:c['text-secondary'],line:c['border-strong'],'icon-accent':c.accent}))document.documentElement.style.setProperty('--'+k,v);document.body.classList.toggle('mono',$('#mono').checked);document.body.classList.toggle('motion',$('#motion').checked);$('#cards').innerHTML=d.icons.map(i=>`<article class="card" data-icon="${i.id}"><h2>${i.label}</h2><code>${i.id}</code><p>${i.note}</p><div class="pair"><div style="color:${i.semantic?c[i.semantic]:'var(--ink)'}">${version(i.before,'Vorige')}</div><div style="color:${i.semantic?(i.semantic==='warning'?d.warning_preview[$('#theme').value]:c[i.semantic]):'var(--ink)'}">${version(i.after,i.id==='draw.circle'?'Gekozen · B':i.id==='draw.text'?'Gekozen · geheel accent':'Herzien',i.id==='status.busy')}</div></div>${i.id==='status.busy'?'<div class="alternative" style="color:'+c['text-secondary']+'">'+version(d.alternatives['busy-clock'],'Alternatief · klokje (wachten / tijdsduur)')+'</div>':''}</article>`).join('')}
$('#theme').onchange=render;$('#mono').onchange=render;$('#motion').onchange=render;render();
</script></html>'''
