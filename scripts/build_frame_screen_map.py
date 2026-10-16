#!/usr/bin/env python3
"""Map Open Frame Studio's workspace tabs to their pinned Svelte screens."""
import json
import re
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-frame-studio')
COMMIT = 'eb77f9e4c5d3f5b9b081aef5dd3dcf07dbdaf43f'
APP_PATH = 'ui/src/App.svelte'
app = subprocess.check_output(['git', '-C', str(REPO), 'show', f'{COMMIT}:{APP_PATH}'], text=True)
nl = json.loads(subprocess.check_output(['git', '-C', str(REPO), 'show',
                                         f'{COMMIT}:ui/src/locales/nl.json'], text=True))
ribbon = subprocess.check_output(['git', '-C', str(REPO), 'show',
                                  f'{COMMIT}:ui/src/components/shell/Ribbon.svelte'], text=True)
ribbon_tabs = re.findall(r'\{ id: "([^"]+)", key: "ribbon\.[^"]+" \}', ribbon)
assert ribbon_tabs == ['home', 'insert', 'ifc', 'production', 'view']
icons = json.loads((ROOT / 'harmonization/frame-svelte-svg-audit.json').read_text())
assert icons['commit'] == COMMIT
tab_icons = [r for r in icons['records'] if r['kind'] == 'ui-icon' and r['file'] == APP_PATH and r['ordinal'] <= 20]
assert len(tab_icons) == 20

imports = dict(re.findall(r'import\s+(\w+)\s+from\s+"([^"]+\.svelte)"', app))
tab_clicks = list(re.finditer(r'activeWorkspaceView\.set\("([^"]+)"\)', app))
assert len(tab_clicks) == 20
branch_start = list(re.finditer(r'\{(?:#if|:else if) workspaceView === "([^"]+)"\}', app))
assert len(branch_start) == 20
branches = {}
for i, match in enumerate(branch_start):
    end = branch_start[i + 1].start() if i + 1 < len(branch_start) else app.index('\n  {/if}\n</div>', match.end())
    branches[match.group(1)] = app[match.end():end]

records = []
for icon, click in zip(tab_icons, tab_clicks):
    key = click.group(1)
    assert key in branches and f'"tabs.{key}"' in json.dumps(nl), key
    tab_line = app.count('\n', 0, click.start()) + 1
    assert icon['line'] >= tab_line and icon['line'] <= tab_line + 8, (key, tab_line, icon['line'])
    branch = branches[key]
    components = list(dict.fromkeys(re.findall(r'<([A-Z][A-Za-z0-9]*)\b', branch)))
    screens = []
    for component in components:
        if component in ('ResizeHandle',):
            continue
        source = imports.get(component)
        assert source, (key, component)
        full = 'ui/src/' + source.removeprefix('./')
        assert subprocess.run(['git', '-C', str(REPO), 'cat-file', '-e', f'{COMMIT}:{full}'],
                              capture_output=True).returncode == 0, full
        screens.append({'component': component, 'file': full})
    shell_panels = (['ProjectOverview', 'PropertiesPanel', 'AiAssistant'] if key == 'editor' else
                    ['ProjectOverview', 'PropertiesPanel'] if key == 'viewer3d' else [])
    primary = [s for s in screens if s['component'] not in shell_panels]
    assert primary, key
    records.append({'id': key, 'label': nl[f'tabs.{key}'], 'tab_line': tab_line,
                    'icon': icon['svg'], 'icon_line': icon['line'],
                    'primary_screens': primary, 'shared_panels': shell_panels,
                    'conditional_editor_variants': key == 'editor'})

assert len(records) == 20
assert set(r['id'] for r in records) == set(branches)
assert {s['component'] for s in records[0]['primary_screens']} == {'KozijnEditor', 'VliesgevelEditor'}
manifest = {'repository': 'open-frame-studio', 'commit': COMMIT,
            'scope': 'App.svelte workspace tab destinations and conditional Svelte components; structural source review, not screenshots.',
            'workspace_tabs': 20, 'default_workspace': 'editor',
            'ribbon_tabs': ribbon_tabs, 'default_ribbon_tab': 'home', 'editor_canvas_variants': 2,
            'source_screenshots': 0, 'shell': ['TitleBar', 'Ribbon', 'AppMenu', 'Settings',
                                            'WorkspaceTabs', 'Workspace', 'StatusBar', 'Toast'],
            'screens': records}
(ROOT / 'harmonization/frame-screen-map.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    link = f'https://github.com/OpenAEC-Foundation/open-frame-studio/blob/{COMMIT}/{APP_PATH}#L{item["tab_line"]}'
    comp = ', '.join(s['component'] for s in item['primary_screens'])
    primary_links = ' · '.join(f'<a href="https://github.com/OpenAEC-Foundation/open-frame-studio/blob/{COMMIT}/{s["file"]}">{escape(s["component"])} ↗</a>' for s in item['primary_screens'])
    panels = ' · '.join(item['shared_panels']) or 'geen vaste zijpanelen'
    cards.append(f'<article data-id="{escape(item["id"])}"><button class="select" type="button" aria-label="Toon {escape(item["label"])}"><img src="../harmonization/{item["icon"]}" width="22" height="22" alt=""><span><strong>{escape(item["label"])}</strong><small>{escape(item["id"])}</small></span></button><p>{escape(comp)}</p><p class="panels">{escape(panels)}</p><footer><a href="{escape(link)}">Tabbron ↗</a> · {primary_links}</footer></article>')

data = json.dumps(records, ensure_ascii=False).replace('</', '<\\/')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Frame Studio · schermkaart</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:#fff;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:16px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.stats span{background:#fff;border:1px solid #d8d8de;padding:7px 10px}.stats b{color:#ae5b00}.layout{display:grid;grid-template-columns:minmax(340px,560px) minmax(400px,1fr);gap:16px}.preview{position:sticky;top:12px;align-self:start;background:white;border:1px solid #bcbcc4;min-height:440px}.titlebar{background:#303039;color:#fff;padding:10px 13px}.ribbon{height:74px;background:#e8e8ea;border-bottom:1px solid #c8c8d0;padding:10px 12px}.ribbon strong{border-bottom:2px solid #e58200;padding-bottom:5px}.tabs{display:flex;flex-wrap:wrap;gap:4px;background:#f3f3f4;border-bottom:1px solid #ddd;padding:8px}.tab{border:1px solid #c7c7cd;padding:3px 6px;font-size:10px}.tab.active{color:#a65500;border-bottom:2px solid #e58200}.work{display:flex;min-height:240px}.side{width:22%;padding:12px 8px;background:#f6f6f7;border-right:1px solid #ddd;font-size:11px}.side.right{border-left:1px solid #ddd;border-right:0}.canvas{flex:1;padding:20px 14px;min-width:0}.canvas h2{margin:0 0 10px;font-size:20px}.canvas p{color:#73737b}.canvas .placeholder{border:1px dashed #c6c6ce;height:115px;display:grid;place-items:center;color:#9a9aa3;text-align:center}.status{height:24px;background:#e8e8ea;border-top:1px solid #ccc;padding:4px 10px;font-size:10px;color:#6d6d76}.list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}article{background:white;border:1px solid #d8d8de;padding:10px}article.active{outline:2px solid #e58200;outline-offset:-2px}.select{border:0;background:transparent;width:100%;text-align:left;display:flex;gap:10px;align-items:center;cursor:pointer;color:inherit}.select img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.select span{display:flex;flex-direction:column}.select small{color:#7a7a83;font:10px ui-monospace,monospace}article p{font-size:11px;margin:8px 0 0}article .panels{color:#777781}article footer{font-size:10px;margin-top:9px}a{color:#ac5600}@media(max-width:900px){.layout{grid-template-columns:1fr}.preview{position:static}.list{grid-template-columns:1fr}}@media(max-width:620px){.hero{padding:20px}main{padding:12px}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Frame Studio · schermkaart</h1><p>Twintig echte werkruimtetabs uit de gepinde Svelte-app, gekoppeld aan hun schermcomponenten en gedeelde shell.</p></div><main><div class="note"><strong>Structurele review.</strong> De standaardstart is de 2D-editor met Home-lint. Die editor wisselt conditioneel tussen KozijnEditor en VliesgevelEditor; 3D Viewer en 2D Editor hebben inklapbare zijpanelen. Deze kaart claimt geen pixelgelijkheid: er zijn geen bron-screenshots in de repository aangetroffen.</div><div class="stats"><span><b>20</b> werkruimtetabs</span><span><b>2</b> editor-canvasvarianten</span><span><b>5</b> linttabs</span><span><b>0</b> bron-screenshots</span></div><div class="layout"><section class="preview"><div class="titlebar">Open Frame Studio · titelbalk</div><div class="ribbon"><strong>Home</strong><p>Gedeelde lintindeling</p></div><div class="tabs"><span class="tab active" id="active-tab">2D Editor</span><span class="tab">3D Viewer</span><span class="tab">Kozijnstaat</span><span class="tab">…</span></div><div class="work"><div class="side" id="left-panel">ProjectOverview</div><div class="canvas"><h2 id="screen-title">2D Editor</h2><p id="screen-components">KozijnEditor / VliesgevelEditor</p><div class="placeholder">Brongebonden schermstructuur<br>Geen pixelclaim zonder screenshot</div></div><div class="side right" id="right-panel">PropertiesPanel / AiAssistant</div></div><div class="status">StatusBar · Toast</div></section><div class="list">''' + ''.join(cards) + '''</div></div></main><script>const data=''' + data + ''';const cards=[...document.querySelectorAll('article')];function show(id){const item=data.find(x=>x.id===id);if(!item)return;cards.forEach(c=>c.classList.toggle('active',c.dataset.id===id));document.querySelector('#active-tab').textContent=item.label;document.querySelector('#screen-title').textContent=item.label;document.querySelector('#screen-components').textContent=item.primary_screens.map(x=>x.component).join(' / ');document.querySelector('#left-panel').hidden=!item.shared_panels.includes('ProjectOverview');document.querySelector('#right-panel').hidden=!item.shared_panels.includes('PropertiesPanel');document.querySelector('#right-panel').textContent=item.shared_panels.filter(x=>x!=='ProjectOverview').join(' / ')}cards.forEach(c=>c.querySelector('button').onclick=()=>show(c.dataset.id));show('editor');</script></html>'''
(ROOT / 'design/frame-screen-review.html').write_text(page)
print('Open Frame: 20 workspace tabs, editor has two conditional canvas components')
