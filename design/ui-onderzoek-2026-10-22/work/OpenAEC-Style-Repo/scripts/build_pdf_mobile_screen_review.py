#!/usr/bin/env python3
"""Build source-dimensioned mobile PDF screen states for layout assessment."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
css_path = 'open-pdf-studio/styles/mobile.css'
jsx_path = 'open-pdf-studio/js/solid/MobileApp.jsx'

def source(path):
    return subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'],text=True)

assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==commit
css = source(css_path)
jsx = source(jsx_path)
for marker in ('height: 48px;', 'min-height: 52px;', 'width: 280px;', 'max-width: 80vw;',
               'min-height: 24px;', 'width: 44px;', 'max-width: 480px;',
               'min-width: 32px;', 'max-width: 48px;'):
    assert marker in css, marker
for marker in ('mobile-placeholder', 'mobile-bottombar', 'mobile-drawer', 'mobile-prefs-page',
               'mobile-toolbar-collapse-handle', 'MOBIELE_GEREEDSCHAPPEN'):
    assert marker in jsx, marker

states = [
    {'id':'empty','label':'Leeg','trigger':'Geen document','regions':['48px topbar','werkgebied met illustratie','geen onderste werkbalk']},
    {'id':'document','label':'Document','trigger':'PDF geladen','regions':['48px topbar','PDF-canvas','minimaal 52px werkbalk']},
    {'id':'drawer','label':'Bestandmenu','trigger':'Menu geopend','regions':['280px drawer, maximaal 80vw','56px drawerheader','document achter 40% scrim']},
    {'id':'preferences','label':'Voorkeuren','trigger':'Voorkeuren geopend','regions':['schermvullende pagina','48px header','scrollende formuliersecties']},
]
manifest={'repository':'open-pdf-studio','commit':commit,'source_jsx':jsx_path,'source_css':css_path,
          'scope':'Four source-reachable mobile screen states. Dimensions are taken from mobile.css, with zero safe-area insets in the static study. PDF page artwork is schematic, not a screenshot. Theme/accent controls compare source blue against a harmonized amber proposal, not a finished product pixel match.',
          'source_dimensions_px':{'topbar_height':48,'bottom_toolbar_min_height':52,'collapsed_toolbar_min_height':24,
                                  'topbar_button':44,'toolbar_button_min_width':32,'toolbar_button_max_width':48,
                                  'toolbar_content_max_width':480,'drawer_width':280,'drawer_max_viewport_percent':80,
                                  'drawer_header_height':56},'states':states}
(root/'harmonization/pdf-mobile-screen-states.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

def icon(name,size=22):
    return f'<img src="../harmonization/inline-ui-icons/open-pdf-studio/mobile/{name}.svg" width="{size}" height="{size}" alt="">'

topbar=f'<div class="topbar"><span class="tap">{icon("topbar-menu")}</span><strong>Open PDF Studio</strong><span class="tap">{icon("theme-moon")}</span><span class="tap">{icon("topbar-open")}</span></div>'
toolbar=''.join([
    '<div class="bottombar"><div class="collapse">'+icon('toolbar-disclosure-expanded',16)+'</div><div class="toolbar">',
    '<span class="tool">'+icon('page-previous')+'</span><span class="page-no">1 / 12</span><span class="tool">'+icon('page-next')+'</span><i></i>',
    '<span class="tool">'+icon('zoom-out')+'</span><span class="tool">'+icon('zoom-in')+'</span><i></i>',
    '<span class="tool">'+icon('rotate-page')+'</span><span class="tool">'+icon('enter-fullscreen')+'</span><i></i>',
    '<span class="tool">'+icon('annotation-tools')+'</span></div></div>'])
empty=topbar+'<div class="viewport empty"><img src="../harmonization/ui-graphics/open-pdf-studio/mobile/empty-document.svg" width="64" height="64" alt=""><p>Open a PDF file to get started</p><button>Open PDF</button></div>'
document=topbar+'<div class="viewport document"><div class="paper"><div class="paper-title">PDF-DOCUMENT</div><div class="paper-line"></div><div class="paper-line short"></div><div class="paper-box"></div><div class="paper-line"></div><div class="paper-line med"></div></div><small>Schematische canvasplaceholder</small></div>'+toolbar
drawer=document+'<div class="scrim"></div><div class="drawer"><div class="drawer-head"><strong>Open PDF Studio</strong>'+icon('drawer-close')+'</div><div class="drawer-items">'+''.join([
    '<div>'+icon('drawer-open',20)+'<span>Openen</span></div>',
    '<div>'+icon('drawer-save',20)+'<span>Opslaan</span></div>',
    '<div>'+icon('drawer-save-as',20)+'<span>Opslaan als</span></div>',
    '<hr><label>RECENTE BESTANDEN</label>',
    '<div>'+icon('recent-document',18)+'<span>tekening.pdf</span></div>',
    '<hr><div>'+icon('drawer-settings',20)+'<span>Voorkeuren</span></div>',
    '<div>'+icon('drawer-feedback',20)+'<span>Feedback</span></div>',
    '<div>'+icon('drawer-about',20)+'<span>Over</span></div>'])+'</div></div>'
preferences='<div class="prefs-head">'+icon('preferences-back')+'<strong>Preferences</strong></div><div class="prefs-body">'+''.join([
    '<section><label>THEMA</label><div class="field">System <span>⌄</span></div></section>',
    '<section><label>TAAL</label><div class="field">Nederlands <span>⌄</span></div></section>',
    '<section><label>AUTEUR</label><div class="field">Naam auteur</div></section>',
    '<section><label>ANNOTATIES</label><div class="row">Standaardkleur <span class="swatch"></span></div><div class="row">Lijndikte <span class="number">3</span></div><div class="row">Dekking <span>30%</span></div></section>',
    '<section><label>OPSTARTEN</label><div class="row">Vorige sessie herstellen <span>☑</span></div></section>',
    '<section><label>VERWIJDEREN</label><div class="row">Eerst bevestigen <span>☑</span></div></section>'])+'</div>'
markup={'empty':empty,'document':document,'drawer':drawer,'preferences':preferences}
cards=''.join(f'<article><div class="card-head"><span>{index:02d}</span><h2>{s["label"]}</h2><small>{s["trigger"]}</small></div><div class="phone">{markup[s["id"]]}</div><p>{" · ".join(s["regions"])}</p></article>' for index,s in enumerate(states,1))
page='''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Mobiele schermstudie</title><style>
:root{font:13px/1.45 system-ui,sans-serif;color:#303039;background:#eff0f2;--phone-width:360px;--accent:#0078d4}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #e58a21;padding:28px max(20px,calc((100vw - 1460px)/2))}header a{color:#ffc580}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{max-width:1060px;color:#d8d8df;margin:0}main{max-width:1500px;margin:auto;padding:20px}.note{background:#fff;border-left:4px solid #e58a21;padding:12px 16px;margin-bottom:14px}.controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 20px}.controls label{font-weight:600}.controls button{border:1px solid #c6c7cd;background:#fff;padding:7px 12px;font:inherit;cursor:pointer}.controls button[aria-pressed=true]{background:#303039;color:#fff}.cards{display:flex;gap:18px;align-items:flex-start;overflow-x:auto;padding-bottom:12px}article{flex:0 0 calc(var(--phone-width) + 20px);background:#fff;border:1px solid #d6d7de;padding:10px}article p{color:#74747e;font-size:11px;margin:9px 2px 0;min-height:30px}.card-head{display:flex;align-items:baseline;gap:8px;padding:4px 2px 9px}.card-head>span{font-size:11px;color:#aaa}.card-head h2{font-size:16px;margin:0;flex:1}.card-head small{color:#777}.phone{position:relative;width:var(--phone-width);height:640px;background:#fff;color:#1a1a1a;overflow:hidden;border:1px solid #bebfc5;display:flex;flex-direction:column;--surface:#fff;--secondary:#f5f5f5;--line:#d4d4d4;--ink:#1a1a1a;--muted:#666}.topbar,.prefs-head{height:48px;min-height:48px;display:flex;align-items:center;gap:4px;padding:0 4px;background:var(--secondary);border-bottom:1px solid var(--line)}.topbar strong{font-size:15px;font-weight:500;flex:1;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.tap{width:44px;height:44px;min-width:44px;display:grid;place-items:center}.viewport{flex:1;min-height:0;position:relative}.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--muted);gap:16px;padding:32px}.empty>img{opacity:.4}.empty p{font-size:15px;margin:0}.empty button{background:var(--accent);color:#fff;border:0;border-radius:4px;padding:12px 32px;min-height:44px;font:500 16px system-ui}.document{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;overflow:hidden;background:#d9dadd;padding-top:22px}.document .paper{width:74%;height:510px;background:#fff;box-shadow:0 2px 9px #0002;padding:31px 22px}.paper-title{font-size:18px;font-weight:700;color:#4c4c56;margin-bottom:25px}.paper-line{height:8px;background:#e8e8ed;margin:14px 0}.paper-line.short{width:55%}.paper-line.med{width:72%}.paper-box{height:165px;border:1px solid #e3e3ea;margin:22px 0;background:linear-gradient(130deg,#f5f5f7,#e3e3e8)}.document small{position:absolute;bottom:7px;color:#4e4e55;background:#fffd;padding:2px 5px}.bottombar{position:relative;min-height:52px;background:var(--secondary);border-top:1px solid var(--line);padding:4px 4px 0}.collapse{position:absolute;left:50%;top:0;transform:translateX(-50%);width:48px;height:20px;display:grid;place-items:center;color:var(--muted)}.toolbar{display:flex;align-items:center;justify-content:space-between;max-width:480px;min-width:0;height:44px;margin:auto}.toolbar .tool{flex:1 1 0;min-width:32px;max-width:48px;height:44px;display:grid;place-items:center}.toolbar i{width:1px;height:28px;background:var(--line);margin:0 2px}.page-no{min-width:48px;text-align:center;font-size:13px;white-space:nowrap}.scrim{position:absolute;inset:0;background:#0006}.drawer{position:absolute;inset:0 auto 0 0;width:min(280px,80%);background:var(--surface);box-shadow:4px 0 16px #0003;display:flex;flex-direction:column}.drawer-head{height:56px;min-height:56px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 16px;font-size:16px}.drawer-items{padding:8px 0;overflow:auto}.drawer-items>div{min-height:48px;display:flex;align-items:center;gap:16px;padding:12px 20px;font-size:15px}.drawer-items>div img{flex:none}.drawer-items hr{border:0;border-top:1px solid var(--line);margin:8px 16px}.drawer-items label{display:block;padding:8px 20px 4px;color:var(--muted);font-size:11px;font-weight:600;letter-spacing:.5px}.prefs-head strong{font-size:16px;margin-left:13px}.prefs-body{overflow:auto;flex:1}.prefs-body section{padding:12px 16px;border-bottom:1px solid var(--line)}.prefs-body label{display:block;color:var(--muted);font-size:12px;font-weight:600;letter-spacing:.5px;margin-bottom:10px}.field{background:var(--secondary);border:1px solid var(--line);padding:10px 12px;font-size:16px;display:flex;justify-content:space-between}.row{min-height:42px;display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:14px}.swatch{background:#ff0000;width:44px;height:36px;border:3px solid #fff;outline:1px solid var(--line)}.number{border:1px solid var(--line);padding:8px 10px;min-width:64px;text-align:center}.phone img{display:block}.dark .phone{--surface:#303039;--secondary:#393940;--line:#565660;--ink:#f5f5f7;--muted:#bdbdc7;background:var(--surface);color:var(--ink)}.dark .phone img{filter:brightness(0) invert(1)}.dark .document{background:#24242a}.dark .paper{color:#303039}.dark .empty button{color:#fff}.dark .swatch{border-color:#393940}@media(max-width:700px){main{padding:10px}header{padding:20px 14px}.cards{gap:10px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Mobiele schermstudie · Open PDF Studio</h1><p>Vier toestanden uit de bereikbare mobiele route. De maten komen uit de gepinde bron-CSS; het PDF-canvas is schematisch. Wissel schermbreedte, thema en accent om de harmonisatie te beoordelen.</p></header><main><div class="note"><strong>Bronmaten:</strong> 48px topbar, minimaal 52px onderste werkbalk (ingeklapt 24px), 44px topbar-tapvlak, 32–48px werkbalkknoppen, drawer 280px of 80vw, drawerheader 56px. Safe-area-insets staan hier op 0. <a href="pdf-mobile-icon-review.html">Bekijk alle mobiele UI-iconen</a>.</div><div class="controls"><label>Breedte</label><button data-width="320">320px</button><button data-width="360" aria-pressed="true">360px</button><button data-width="412">412px</button><label>Thema</label><button id="theme">Light / Forge</button><label>Accent</label><button id="accent">Bronblauw / harmonisatie-amber</button></div><div class="cards">''' + cards + '''</div></main><script>for(const b of document.querySelectorAll('[data-width]'))b.onclick=()=>{document.documentElement.style.setProperty('--phone-width',b.dataset.width+'px');for(const x of document.querySelectorAll('[data-width]'))x.setAttribute('aria-pressed',x===b)};document.querySelector('#theme').onclick=()=>document.body.classList.toggle('dark');document.querySelector('#accent').onclick=()=>document.documentElement.style.setProperty('--accent',getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()==='#0078d4'?'#d97706':'#0078d4');</script></html>'''
(root/'design/pdf-mobile-screen-review.html').write_text(page)
print('PDF mobile screen study: four source-reachable states; 320/360/412 px, Light/Forge, source/harmonized accent')
