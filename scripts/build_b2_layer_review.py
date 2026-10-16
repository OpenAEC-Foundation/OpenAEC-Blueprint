"""Compare both occlusion orders without changing an icon's silhouette."""
import hashlib
import json
from b2_geometry import construction, export_svg, foreground, layer_reason, SHAPE_REVISIONS, CURRENT_CHANGES


def render_layer_review(out,entries,themes):
    records=[];manifest=[]
    for entry in entries:
        if entry['series']!=1:continue
        key=entry['id'];variants={tone:{} for tone in ('primary','accent')};assets={tone:{} for tone in variants}
        difference=0
        for size in (16,24):
            model=construction(key,size)
            for tone in variants:
                content=export_svg(model,tone)
                variants[tone][str(size)]=content
                path=out/'review/layers'/tone/str(size)/(key+'.svg')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
                assets[tone][str(size)]={'path':path.relative_to(out).as_posix(),
                                        'sha256':hashlib.sha256(content.encode()).hexdigest()}
            if size==24:
                difference=model.geometry('primary')['primary'].symmetric_difference(model.geometry('accent')['primary']).area
        records.append({'id':key,'label':entry['label'],'front':foreground(key),'reason':layer_reason(key),
                        'difference':difference,'variants':variants})
        manifest.append({'id':key,'foreground':foreground(key),'difference':difference,'variants':assets})
    records.sort(key=lambda r:(r['front']!='accent',r['label']))
    (out/'layer-comparison.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'layers.html').write_text(PAGE.replace('/* DATA */',json.dumps({'icons':records,'themes':themes},ensure_ascii=False)),encoding='utf-8')
    render_shape_review(out,entries,themes)


def render_shape_review(out,entries,themes):
    records=[]
    for e in entries:
        if e['id'] not in CURRENT_CHANGES:continue
        records.append({'label':e['label'],'reason':SHAPE_REVISIONS[e['id']],
                        'before':{str(s):(out/'review/stem-before'/str(s)/(e['id']+'.svg')).read_text(encoding='utf-8') for s in (16,24)},
                        'after':{str(s):(out/e['assets'][str(s)]['path']).read_text(encoding='utf-8') for s in (16,24)}})
    css=PAGE.split('<style>')[1].split('</style>')[0]
    html='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2 · drie vormen herzien</title><style>CSS .head,.row{grid-template-columns:1.1fr 1fr 1fr}.big{height:86px}</style><main><small>OPENAEC / B2 / VORMCORRECTIES</small><h1>Drie iconen opnieuw uitgewerkt</h1><p>Nieuw document, Opslaan als en 3D-beeld draaien. Links de vorige vorm, rechts de bijgewerkte vorm op 16, 24 en 32 px.</p><a href="index.html">Naar de iconenfamilie</a> · <a href="layers.html">De zes accentcorrecties bekijken</a><div class="controls"><label>Thema <select id="theme"></select></label><label><input id="mono" type="checkbox"> Eén kleur</label></div><div class="head"><div>Wat is aangepast</div><div>Vorige vorm</div><div>Nieuwe vorm</div></div><div id="rows"></div></main><script id="data" type="application/json">DATA</script><script>const d=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);$('#theme').innerHTML=Object.entries(d.themes).map(([k,t])=>`<option value="${k}">${t.name}</option>`).join('');$('#theme').value='dark';function theme(){let t=d.themes[$('#theme').value],c=t.color;document.documentElement.style.colorScheme=t.kind;for(let [k,v] of Object.entries({bg:c.frame,panel:c.panel,ink:c.text,muted:c['text-secondary'],line:c['border-strong'],'icon-accent':c.accent}))document.documentElement.style.setProperty('--'+k,v)}function resize(s,n){return s.replace(/width="\\d+"/,`width="${n}"`).replace(/height="\\d+"/,`height="${n}"`)}$('#rows').innerHTML=d.icons.map(r=>`<section class="row"><div class="info"><h2>${r.label}</h2><p>${r.reason}</p></div>${['before','after'].map(side=>`<div class="cell ${side==='after'?'selected':''}"><div class="big">${r[side][24]}</div><div class="native">${[16,24,32].map(n=>`<div>${resize(r[side][n===16?16:24],n)}<span>${n} px</span></div>`).join('')}</div></div>`).join('')}</section>`).join('');$('#theme').onchange=theme;$('#mono').onchange=()=>document.body.classList.toggle('mono',$('#mono').checked);theme();</script></html>'''
    html=html.replace('CSS',css).replace('DATA',json.dumps({'icons':records,'themes':themes},ensure_ascii=False))
    html=html.replace('B2 · drie vormen herzien','B2 · vormen en overgangen').replace('Drie iconen opnieuw uitgewerkt','Vormen en overgangen verfijnd').replace(
        'Nieuw document, Opslaan als en 3D-beeld draaien. Links de vorige vorm, rechts de bijgewerkte vorm op 16, 24 en 32 px.',
        'Vier pijlen: de steel in de hoofdkleur loopt nu tot in de aanwijzer. De afgeronde aansluiting, vaste kleuren en buitenvorm blijven behouden. Links de vorige uitvoering, rechts de nieuwe.').replace(
        'function resize(s,n){','let svgInstance=0;function resize(s,n){s=s.replaceAll("b2-blend-","b2-blend-"+(++svgInstance)+"-");').replace('${r[side][24]}','${resize(r[side][24],74)}')
    (out/'shapes.html').write_text(html,encoding='utf-8')


PAGE=r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2 · laagvolgorde per icoon</title><style>
*{box-sizing:border-box}body{margin:0;font:14px/1.5 system-ui;background:var(--bg);color:var(--ink)}:root{--bg:#2a2a32;--panel:#33333c;--ink:#edebe8;--muted:#bebdbd;--line:#878689;--icon-accent:#d97706;color-scheme:dark}main{max-width:1350px;margin:auto;padding:32px}h1{font-size:30px;margin:12px 0}h2{font-size:16px;margin:0}p{color:var(--muted);max-width:940px}a{color:inherit}.controls{display:flex;flex-wrap:wrap;gap:20px;align-items:center;position:sticky;top:0;background:var(--bg);padding:18px 0;z-index:2}select,input{font:inherit}select,input[type=search]{padding:7px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink)}.head,.row{display:grid;grid-template-columns:1.05fr repeat(3,1fr);gap:12px}.head{font-size:13px;margin:18px 0}.head>div{padding:10px}.row{padding:18px 0;border-top:1px solid var(--line)}.info{padding:14px 4px}.info p{font-size:12px}.info small{font-size:11px;color:var(--muted)}.cell{border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--panel)}.selected{border:2px solid var(--icon-accent)}.big{display:flex;align-items:center;justify-content:center;height:100px}.big svg{width:74px;height:74px}.native{height:68px;display:flex;justify-content:center;align-items:flex-end;gap:22px}.native>div{display:flex;flex-direction:column;gap:8px;align-items:center;font-size:10px;color:var(--muted)}.native svg{color:var(--ink)}.status{text-align:center;font-size:11px;color:var(--muted);margin-top:8px}.mono{--icon-accent:currentColor!important}footer{border-top:1px solid var(--line);margin-top:24px;padding:20px 0;color:var(--muted);font-size:12px}@media(max-width:700px){main{padding:18px 10px}.head,.row{grid-template-columns:repeat(3,1fr);gap:6px}.head>div:first-child{display:none}.info{grid-column:1/-1}.native{gap:8px}.big svg{width:52px;height:52px}.head>div{padding:3px}}
</style><main><small>OPENAEC / B2 / LAAGVOLGORDE</small><h1>De aansluiting bepaalt de voorgrond</h1><p>Accent vóór bij de zes iconen die je aanwees: Afdrukken, Ongedaan maken, Opnieuw uitvoeren, Plakken, Terug en Vooruit. De rest behoudt de vorige aansluiting. Links en midden tonen beide mogelijkheden; rechts staat de bijgewerkte uitvoering.</p><a href="index.html">Naar de iconenfamilie en SVG-download</a><div class="controls"><label>Thema <select id="theme"></select></label><input id="search" type="search" aria-label="Zoek icoon" placeholder="Zoek icoon…"><label><input id="changed" type="checkbox" checked> Alleen de zes aangepaste iconen</label><label><input id="mono" type="checkbox"> Eén kleur</label></div><div class="head"><div>Functie en aansluiting</div><div><b>Hoofdkleur vóór</b><br>Vorige uitvoering</div><div><b>Accent vóór</b><br>Volledige pijl / clip / papier</div><div><b>Bijgewerkt</b><br>Per icoon vastgelegd</div></div><div id="rows"></div><footer>Beide uitvoeringen zijn gevulde vectorcontouren uit hetzelfde constructiemodel. De achterste kleur wordt geometrisch uitgesneden onder de voorste kleur; de vorm en lijndikte veranderen niet. De uitvoer en SVG-download in het hoofdoverzicht volgen dezelfde keuze. 16px heeft een eigen master; 32px gebruikt de 24px-master. Thema’s komen uit tokens-0.4.json.</footer></main><script id="data" type="application/json">/* DATA */</script><script>
const d=JSON.parse(document.querySelector('#data').textContent),$=s=>document.querySelector(s);$('#theme').innerHTML=Object.entries(d.themes).map(([k,t])=>`<option value="${k}">${t.name}</option>`).join('');$('#theme').value='dark';function theme(){const t=d.themes[$('#theme').value],c=t.color;document.documentElement.style.colorScheme=t.kind;for(const [k,v] of Object.entries({bg:c.frame,panel:c.panel,ink:c.text,muted:c['text-secondary'],line:c['border-strong'],'icon-accent':c.accent}))document.documentElement.style.setProperty('--'+k,v)}function resize(s,n){return s.replace(/width="d+"/,`width="${n}"`).replace(/height="d+"/,`height="${n}"`)}function cell(r,tone,selected){return `<div class="cell ${selected?'selected':''}"><div class="big">${r.variants[tone][24]}</div><div class="native">${[16,24,32].map(n=>`<div>${resize(r.variants[tone][n===16?16:24],n)}<span>${n} px</span></div>`).join('')}</div><div class="status">${tone==='accent'?'Accent vóór':'Hoofdkleur vóór'}</div></div>`}function render(){const q=$('#search').value.toLowerCase();$('#rows').innerHTML=d.icons.filter(r=>(!$('#changed').checked||r.front==='accent')&&(r.label+' '+r.id).toLowerCase().includes(q)).map(r=>`<section class="row"><div class="info"><h2>${r.label}</h2><small>${r.id}</small><p>${r.reason}</p>${r.difference<.0001?'<small>Hier raken beide kleuren elkaar niet: de volgorde maakt visueel geen verschil.</small>':''}</div>${cell(r,'primary',false)}${cell(r,'accent',false)}${cell(r,r.front,true)}</section>`).join('')}$('#theme').onchange=theme;$('#search').oninput=render;$('#changed').onchange=render;$('#mono').onchange=()=>document.body.classList.toggle('mono',$('#mono').checked);theme();render();
</script></html>'''

PAGE=PAGE.replace('function resize(s,n){','let svgInstance=0;function resize(s,n){s=s.replaceAll("b2-blend-","b2-blend-"+(++svgInstance)+"-");').replace('${r.variants[tone][24]}','${resize(r.variants[tone][24],74)}').replace('Volledige pijl / clip / papier','Volledige pijl / invoegpijl / papier')
PAGE=PAGE.replace('width="d+"',r'width="\d+"').replace('height="d+"',r'height="\d+"')
PAGE=PAGE.replace('Hier raken beide kleuren elkaar niet: de volgorde maakt visueel geen verschil.',
                  'Bij deze geometrie verandert de laagvolgorde het beeld niet.')
