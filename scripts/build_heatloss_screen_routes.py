#!/usr/bin/env python3
"""Map every pinned Heatloss page route to its source screen and shell state."""
import json
import re
import subprocess
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-heatloss-studio')
COMMIT = 'e233aec70e16771ecb42a57d6eab3ca6cb0e75a8'
APP = 'frontend/src/App.tsx'
SIDEBAR = 'frontend/src/components/layout/Sidebar.tsx'
RIBBON = 'frontend/src/components/ribbon/Ribbon.tsx'
SHELL = 'frontend/src/components/layout/AppShell.tsx'


def source(path):
    if (REPO / '.git').exists():
        return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{path}']).decode()
    url = f'https://raw.githubusercontent.com/OpenAEC-Foundation/open-heatloss-studio/{COMMIT}/{path}'
    return urllib.request.urlopen(url, timeout=45).read().decode()


app, sidebar, ribbon, shell = map(source, (APP, SIDEBAR, RIBBON, SHELL))
sidebar_index = json.loads((ROOT / 'harmonization/heatloss-sidebar-ui-icons.json').read_text())
assert sidebar_index['commit'] == COMMIT and sidebar_index['sidebar_routes'] == 24
assert all(token in shell for token in ('<TitleBar', '<Ribbon', '<TabBar', '<Sidebar', '<main', '<StatusBar'))

import_paths = {}
for match in re.finditer(r'import\s*\{\s*(\w+)\s*}\s*from\s*"(\./[^\"]+)"', app):
    import_paths[match.group(1)] = 'frontend/src/' + match.group(2).removeprefix('./') + '.tsx'

nav = {}
for icon in sidebar_index['icons']:
    for use in icon['uses']:
        if use['route']:
            assert use['route'] not in nav
            nav[use['route']] = {'icon': icon['name'], 'svg': icon['svg'],
                                 'line': use['line'], 'mode': use['mode'],
                                 'label_key': use['label_key']}
groups = {}
block = sidebar[sidebar.index('const NAV_GROUPS'):sidebar.index('/* ─── Persistent')]
for match in re.finditer(r'to:\s*"([^\"]+)"', block):
    keys = list(re.finditer(r'^    key:\s*"([^\"]+)"', block[:match.start()], re.M))
    assert keys, match.group(1)
    groups[match.group(1)] = keys[-1].group(1)
groups['/projects'] = 'web-projecten'
assert len(groups) == 24 and set(groups) == set(nav)

route_to_tab_block = ribbon.split('const ROUTE_TO_TAB:', 1)[1].split('};', 1)[0]
tabs = dict(re.findall(r'"([^\"]+)":\s*"([^\"]+)"', route_to_tab_block))
assert len(tabs) == 10
tab_names = {'vertrekken': 'Vertrekken', 'constructies': 'Constructies',
             'modeller': 'Modeller', 'ifc': 'IFC', 'resultaten': 'Resultaten',
             'rapport': 'Rapport'}
assert set(tabs.values()) <= set(tab_names)
assert 'ROUTE_TO_TAB[location.pathname] ?? "vertrekken"' in ribbon
assert 'if (newTab && newTab !== activeTab)' in ribbon

routes = []
pattern = r'<Route path="([^\"]+)" element=\{<(\w+)([^>]*?)/>\} />'
for match in re.finditer(pattern, app):
    path, component, attrs = match.groups()
    if path == '/':
        assert component == 'Navigate' and 'to="/project"' in attrs
        continue
    assert component in import_paths, (path, component)
    assert Path(import_paths[component]).suffix == '.tsx'
    group = groups.get(path, 'buiten-zijbalk')
    ribbon_tab = tabs.get(path)
    routes.append({'path': path, 'component': component,
                   'component_file': import_paths[component],
                   'app_line': app.count('\n', 0, match.start()) + 1,
                   'sidebar_group': group, 'sidebar': nav.get(path),
                   'ribbon_tab': ribbon_tab,
                   'ribbon_tab_label': tab_names[ribbon_tab] if ribbon_tab else None,
                   'ribbon_mapping': 'expliciet' if path in tabs else 'niet gekoppeld',
                   'route_props': attrs.strip()})

assert len(routes) == 26 and len({r['path'] for r in routes}) == 26
assert len([r for r in routes if r['sidebar']]) == 24
assert {r['path'] for r in routes if not r['sidebar']} == {'/rapport', '/import/thermal'}
assert Counter(r['ribbon_mapping'] for r in routes) == {'expliciet': 10, 'niet gekoppeld': 16}
manifest = {'repository': 'open-heatloss-studio', 'commit': COMMIT,
            'scope': 'All App.tsx page routes; source-backed shell, sidebar and ribbon mapping. No source screenshots were found for this repository.',
            'redirect': {'from': '/', 'to': '/project'}, 'page_routes': len(routes),
            'sidebar_routes': 24, 'explicit_ribbon_routes': 10,
            'unmapped_ribbon_routes': 16, 'source_screenshots': 0,
            'unmapped_ribbon_behavior': 'Vertrekken on direct entry; previous active tab persists on in-app navigation.',
            'shell_order': ['TitleBar', 'Ribbon', 'TabBar', 'Sidebar + main', 'StatusBar'],
            'routes': routes}
(ROOT / 'harmonization/heatloss-screen-routes.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

group_labels = {'project': 'Project', 'warmteverlies': 'Warmteverlies',
                'ventilatie': 'Ventilatie', 'tojuli': 'Tojuli', 'beng': 'BENG',
                'rcwaarde': 'Rc/Uw', 'rekentools': 'Rekentools', 'library': 'Bibliotheek',
                'help': 'Help', 'web-projecten': 'Projecten (web)',
                'buiten-zijbalk': 'Zonder zijbalkitem'}
cards = []
for route in routes:
    icon = (f'<img src="../harmonization/{escape(route["sidebar"]["svg"])}" width="22" height="22" alt="">'
            if route['sidebar'] else '<span class="no-icon">↗</span>')
    link = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{APP}#L{route["app_line"]}'
    comp = f'https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/{COMMIT}/{route["component_file"]}'
    badge = 'geen vaste ribbonkoppeling' if route['ribbon_mapping'] == 'niet gekoppeld' else f'ribbon · {route["ribbon_tab_label"]}'
    cards.append(f'''<article class="route-card" data-route="{escape(route['path'])}"><button class="route-main" type="button"><span class="route-icon">{icon}</span><span class="route-content"><strong>{escape(route['path'])}</strong><small>{escape(group_labels[route['sidebar_group']])} · {escape(route['component'])}</small><em class="{'fallback' if route['ribbon_mapping']=='niet gekoppeld' else 'mapped'}">{escape(badge)}</em></span></button><span class="route-links"><a href="{escape(link)}" title="Route in App.tsx">route ↗</a><a href="{escape(comp)}" title="Paginasource">pagina ↗</a></span></article>''')
data = json.dumps([{k: r[k] for k in ('path', 'component', 'sidebar_group', 'ribbon_tab_label', 'ribbon_mapping')}
                   for r in routes], ensure_ascii=False).replace('</', '<\\/')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Heatloss · schermroutes</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:white;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}.content{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:18px}.summary{display:flex;gap:9px;flex-wrap:wrap;margin:16px 0}.summary span{background:white;border:1px solid #d8d8de;padding:8px 11px}.summary b{color:#a85400}.layout{display:grid;grid-template-columns:minmax(360px,580px) 1fr;gap:18px;align-items:start}.frame{background:white;border:1px solid #bcbcc5;box-shadow:0 8px 22px #20202a12;min-height:430px}.chrome{height:38px;background:#303039;color:white;padding:9px 13px}.ribbon{height:75px;background:#ebebee;border-bottom:1px solid #c7c7cd;padding:10px 13px}.ribbon strong{display:inline-block;border-bottom:2px solid #e58200;padding-bottom:4px}.ribbon p{font-size:11px;color:#7b5a29;margin:6px 0}.tabbar{height:29px;background:#f9f9fa;border-bottom:1px solid #d9d9df;padding:5px 13px;color:#6d6d75}.frame-body{display:grid;grid-template-columns:134px 1fr;min-height:260px}.sidebar{background:#f0f0f2;border-right:1px solid #d9d9df;padding:16px 10px;font-size:11px}.sidebar b{display:block;margin-bottom:7px}.sidebar span{display:block;background:#fff;padding:6px 7px;border-left:2px solid #e58200;overflow-wrap:anywhere}.screen{padding:19px 17px}.screen small{display:block;color:#787881;margin:8px 0}.screen h2{font-size:17px;margin:5px 0}.screen .placeholder{height:135px;background:linear-gradient(135deg,#fbfbfc,#f1f1f4);border:1px dashed #bfc0c8;display:grid;place-items:center;color:#898992;font-size:11px;text-align:center;padding:12px}.status{height:25px;background:#303039;color:#d8d8de;padding:4px 12px;font-size:10px}.routes{display:grid;grid-template-columns:repeat(auto-fill,minmax(265px,1fr));gap:8px}.route-card{display:grid;grid-template-columns:28px 1fr;gap:7px;text-align:left;background:white;border:1px solid #d8d8de;padding:10px;min-height:88px}.route-main{grid-column:1/-1;display:grid;grid-template-columns:28px 1fr;gap:7px;border:0;background:transparent;padding:0;color:inherit;text-align:left;font:inherit;cursor:pointer}.route-card:hover,.route-card.selected{border-color:#e58200;box-shadow:0 0 0 1px #e58200}.route-icon{color:#bc6400;display:grid;place-items:start center}.route-icon img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.no-icon{font-size:20px}.route-content{min-width:0}.route-content strong,.route-content small,.route-content em{display:block}.route-content strong{font:11px ui-monospace,monospace;overflow-wrap:anywhere}.route-content small{font-size:10px;color:#73737d}.route-content em{font-size:9px;font-style:normal;padding-top:3px}.route-content em.fallback{color:#aa5c08}.route-content em.mapped{color:#39806b}.route-links{grid-column:2;display:flex;gap:8px}.route-links a{color:#a85400;font-size:10px}h2.list-title{font-size:16px;margin:0 0 10px}@media(max-width:950px){.layout{grid-template-columns:1fr}}@media(max-width:620px){.content{padding:12px}.hero{padding:20px}.routes{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Heatloss · scherm- en routekaart</h1><p>26 pagina-routes uit de gepinde App, met brongebonden zijbalk en ribbonstatus. Dit is een structurele ontwerpbeoordeling; de repository bevat geen bron-screenshots voor pixelvergelijking.</p></div><main class="content"><div class="note"><strong>Afwijking in de huidige bron.</strong> Tien routes hebben een expliciete ribbonkoppeling; zestien andere pagina’s hebben geen routekoppeling. Bij een directe start kiest de ribbon Vertrekken; bij navigatie binnen de app blijft de vorige tab actief. Rapport en de thermische importwizard hebben geen eigen zijbalkitem. Een geharmoniseerde Rust-shell moet deze routes eerst inhoudelijk toewijzen voordat schermen als identiek worden beoordeeld.</div><div class="summary"><span><b>26</b> pagina-routes</span><span><b>24</b> zijbalkitems</span><span><b>10</b> expliciete ribbontoewijzingen</span><span><b>16</b> routes zonder tabkoppeling</span><span><b>0</b> bron-screenshots</span></div><div class="layout"><div class="frame" aria-label="Structurele shell-preview"><div class="chrome">Open Heatloss · titelbalk</div><div class="ribbon"><strong id="preview-tab">Vertrekken</strong><p id="preview-mapping">Expliciete bronkoppeling</p></div><div class="tabbar">Documenttabbalk</div><div class="frame-body"><div class="sidebar"><b id="preview-group">Project</b><span id="preview-nav">/project</span></div><div class="screen"><small id="preview-path">/project</small><h2 id="preview-component">ProjectSetup</h2><div class="placeholder">Brongebonden schermstructuur<br>Geen pixelclaim zonder screenshot</div></div></div><div class="status">Statusbalk</div></div><div><h2 class="list-title">Kies een bronroute</h2><div class="routes">''' + ''.join(cards) + '''</div></div></div></main><script>const rows=''' + data + ''';const labels=''' + json.dumps(group_labels, ensure_ascii=False) + ''';const cards=[...document.querySelectorAll('.route-card')];let activeTab='Vertrekken';function select(route){const row=rows.find(x=>x.path===route);if(!row)return;for(const c of cards)c.classList.toggle('selected',c.dataset.route===route);if(row.ribbon_mapping==='expliciet')activeTab=row.ribbon_tab_label;document.querySelector('#preview-tab').textContent=activeTab;document.querySelector('#preview-mapping').textContent=row.ribbon_mapping==='niet gekoppeld'?'Geen routekoppeling · vorige tab blijft actief (directe start: Vertrekken)':'Expliciete bronkoppeling';document.querySelector('#preview-group').textContent=labels[row.sidebar_group];document.querySelector('#preview-nav').textContent=row.sidebar_group==='buiten-zijbalk'?'Geen eigen zijbalkitem':row.path;document.querySelector('#preview-path').textContent=row.path;document.querySelector('#preview-component').textContent=row.component}for(const c of cards)c.querySelector('.route-main').addEventListener('click',()=>select(c.dataset.route));select('/project')</script></html>'''
(ROOT / 'design/heatloss-screen-route-review.html').write_text(page)
print(f'Open Heatloss: {len(routes)} page routes, 24 sidebar routes, 10 mapped ribbon routes, 16 unmapped ribbon routes')
