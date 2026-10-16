#!/usr/bin/env python3
"""Compare pinned Open Frame CSS geometry with the shared Rust shell."""
import json
import re
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-frame-studio')
COMMIT = 'eb77f9e4c5d3f5b9b081aef5dd3dcf07dbdaf43f'


def source(path):
    return subprocess.check_output(['git', '-C', str(REPO), 'show',
                                    f'{COMMIT}:{path}'], text=True)


def rule(code, selector, declaration):
    match = re.search(r'(?m)^\s*' + re.escape(selector) + r'\s*\{([^}]+)\}', code)
    assert match and declaration in match.group(1), (selector, declaration)
    return code.count('\n', 0, match.start()) + 1


def contrast(foreground, background):
    def luminance(color):
        rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return round((high + .05) / (low + .05), 2)


title = source('ui/src/components/shell/TitleBar.svelte')
ribbon = source('ui/src/components/shell/Ribbon.svelte')
status = source('ui/src/components/shell/StatusBar.svelte')
app = source('ui/src/App.svelte')
tokens = source('ui/src/styles/tokens.css')
global_css = source('ui/src/styles/app.css')
settings = source('ui/src/lib/settings.js')
rust = (ROOT / 'crates/openaec-ui/src/model.rs').read_text()
assert '*, *::before, *::after {' in global_css and 'box-sizing: border-box;' in global_css

facts = [
    ('Titelbalk', '36 px', '32 px', 'ui/src/components/shell/TitleBar.svelte',
     rule(title, '.titlebar', 'height: 36px;'), 'metrics::TITLE',
     'Profielmaat per app; vensterknoppen blijven 36 × 36 px.'),
    ('Lintinhoud', 'min. 72 px + tabrij', '94 px vast', 'ui/src/components/shell/Ribbon.svelte',
     rule(ribbon, '.ribbon-content', 'min-height: 72px;'), 'metrics::RIBBON',
     'De inhoudshoogte en de vijf tabbladen afzonderlijk modelleren.'),
    ('Werkruimtetabs', 'flex-wrap; hoogte variabel', '30 px documentbalk', 'ui/src/App.svelte',
     rule(app, '.workspace-tabs', 'flex-wrap: wrap;'), 'metrics::DOCUMENTS',
     'Een eigen omvouwende workspace-navigatie; geen documenttab-nabootsing.'),
    ('Statusbalk', '28 px', '22 px', 'ui/src/components/shell/StatusBar.svelte',
     rule(status, '.statusbar', 'height: 28px;'), 'metrics::STATUS',
     'App-profielhoogte met behoud van gedeelde statussemantiek.'),
    ('Paneelkop', '26 px', '24 px gedeelde paneeltoolbar', 'ui/src/App.svelte',
     rule(app, '.panel-header', 'height: 26px;'), 'metrics::PANEL_TOOLBAR',
     'Kophoogte apart van de herbruikbare eigenschapsrij.'),
    ('Paneelbreedtes', 'links 220 / rechts 290 px', '240 px standaard', 'ui/src/lib/settings.js',
     settings.count('\n', 0, settings.index('left_panel_width: 220')) + 1, 'metrics::PANEL_DEFAULT',
     'Linker en rechter standaardwaarde onafhankelijk bewaren.'),
]
for _, _, rust_value, _, _, metric, _ in facts:
    assert metric.removeprefix('metrics::') in rust and rust_value
assert 'left_panel_width: 220' in settings and 'right_panel_width: 290' in settings
assert 'Math.max(140, Math.min(400, leftWidth + delta))' in app
assert 'Math.max(200, Math.min(500, rightWidth - delta))' in app
assert 'padding: var(--sp-2) var(--sp-4);' in ribbon
assert 'min-width: 56px;' in ribbon
assert '--sp-2: 0.5rem;' in tokens and '--sp-4: 1rem;' in tokens
assert '--bg-titlebar: #36363E;' in tokens and '--bg-ribbon: #44444C;' in tokens
assert '--bg-titlebar: #d4d1cc;' in tokens and '--bg-ribbon: #e8e6e3;' in tokens
assert '--text-muted: #9ca3af;' in tokens and '--text-secondary: #57534E;' in tokens
assert '--bg-surface-alt: #f0f0f0;' in tokens
for metric, number in [('TITLE', 32), ('RIBBON', 94), ('DOCUMENTS', 30),
                       ('STATUS', 22), ('PANEL_DEFAULT', 240), ('PANEL_TOOLBAR', 24)]:
    assert re.search(rf'pub const {metric}: u16 = {number};', rust), metric

source_base = f'https://github.com/OpenAEC-Foundation/open-frame-studio/blob/{COMMIT}/'
measurements = [{'region': name, 'frame_source': frame, 'shared_rust': shared,
                 'source': {'file': path, 'line': line,
                            'url': source_base + path + f'#L{line}'},
                 'rust_metric': metric, 'decision': decision}
                for name, frame, shared, path, line, metric, decision in facts]
manifest = {
    'repository': 'open-frame-studio', 'commit': COMMIT,
    'basis': 'Pinned Svelte CSS declarations and app settings versus current crate model.rs constants. This is a source-measured comparison; no original runtime screenshot or pixel equivalence is claimed.',
    'source_css_box_sizing': 'border-box',
    'source_spacing_unit': '4 px at a 16 px rem root',
    'frame_panel_width_constraints': {'left': [140, 400], 'right': [200, 500]},
    'light_theme_contrast': {
        'workspace_inactive_source': contrast('#9ca3af', '#f0f0f0'),
        'workspace_using_text_secondary': contrast('#57534E', '#f0f0f0'),
        'ribbon_inactive_source': contrast('#A1A1AA', '#e8e6e3'),
        'ribbon_using_text_secondary': contrast('#57534E', '#e8e6e3'),
        'source_tokens': source_base + 'ui/src/styles/tokens.css',
    },
    'measurements': measurements,
    'recommendation': 'Represent Open Frame as a shell profile with its own band metrics, wrapped workspace tabs and independent pane widths; retain the 32/94/30/22 base metrics for tools that match the existing crate shell.',
}
(ROOT / 'harmonization/frame-layout-evidence.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

screens = json.loads((ROOT / 'harmonization/frame-screen-map.json').read_text())['screens']
tabs = ''.join(f'<button class="ws-tab{" active" if i==0 else ""}" type="button"><img src="../harmonization/{s["icon"]}" width="14" height="14" alt="">{escape(s["label"])}</button>' for i, s in enumerate(screens))
rows = ''.join(f'<tr><th>{escape(m["region"])}</th><td>{escape(m["frame_source"])} <a href="{escape(m["source"]["url"])}">bron ↗</a></td><td>{escape(m["shared_rust"])} <a href="../crates/openaec-ui/src/model.rs">Rust ↗</a></td><td>{escape(m["decision"])}</td></tr>' for m in measurements)

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Frame · layoutmaten</title><style>
@font-face{font-family:Inter;src:url('../crates/openaec-ui/assets/fonts/Inter-Regular.ttf')}@font-face{font-family:Inter;src:url('../crates/openaec-ui/assets/fonts/Inter-SemiBold.ttf');font-weight:600}@font-face{font-family:Space;src:url('../crates/openaec-ui/assets/fonts/SpaceGrotesk-Medium.ttf')}*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.45 Inter,system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}main{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:16px}.toolbar{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:18px 0}.toolbar label{display:flex;gap:10px;align-items:center}.toolbar input[type=range]{width:240px}.toolbar output{font:600 13px Inter}.viewport{overflow-x:auto;border:1px solid #c8c8ce;background:#e6e6e9;padding:14px}.frame{width:var(--preview-width,1200px);background:var(--bg-app);color:var(--text-primary);font:14px/1.5 Inter,system-ui,sans-serif;box-shadow:0 2px 12px #0002}.frame button{font:inherit;border:0;background:none;color:inherit}.frame[data-theme=default]{--amber:#D97706;--night-build:#2A2A32;--warm-gold:#F59E0B;--scaffold-gray:#A1A1AA;--bg-app:#36363E;--bg-surface:#44444C;--bg-surface-alt:#3E3E46;--bg-ribbon:#44444C;--bg-titlebar:#36363E;--bg-statusbar:#36363E;--text-primary:#FAFAF9;--text-muted:rgba(250,250,249,.5);--text-on-dark:#FAFAF9;--border-default:1px solid #E7E5E4}.frame[data-theme=light]{--amber:#D97706;--night-build:#2A2A32;--warm-gold:#F59E0B;--scaffold-gray:#A1A1AA;--bg-app:#f5f5f5;--bg-surface:#fff;--bg-surface-alt:#f0f0f0;--bg-ribbon:#e8e6e3;--bg-titlebar:#d4d1cc;--bg-statusbar:#e8e6e3;--text-primary:#1f2937;--text-muted:#9ca3af;--text-on-dark:#1f2937;--border-default:1px solid #E7E5E4}.source-title{height:36px;background:var(--bg-titlebar);color:var(--text-on-dark);display:flex;align-items:center;justify-content:space-between;padding:0 8px;font-family:Space,Inter,sans-serif}.source-title strong{color:var(--amber);font-size:13px}.window-actions{display:flex}.window-actions span{width:36px;height:36px;display:grid;place-items:center;font:15px Inter}.source-ribbon{background:var(--bg-ribbon);border-bottom:2px solid var(--amber);color:var(--text-on-dark)}.source-ribbon-tabs{display:flex;padding:0 8px;border-bottom:1px solid rgba(255,255,255,.08)}.source-ribbon-tabs button{padding:8px 16px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:var(--scaffold-gray);border-bottom:2px solid transparent}.source-ribbon-tabs button.active{color:var(--amber);border-bottom-color:var(--amber)}.source-ribbon-tabs button.file{background:var(--amber);color:var(--night-build);margin-right:4px}.source-ribbon-content{display:flex;align-items:flex-start;padding:8px 12px;min-height:72px;gap:12px}.group{display:flex;flex-direction:column;gap:4px}.group-label{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--scaffold-gray);padding:0 4px}.commands{display:flex;gap:4px}.command{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 12px;font-size:11px;font-weight:500;min-width:56px}.command img{filter:brightness(0) saturate(100%) invert(59%) sepia(90%) saturate(390%) hue-rotate(354deg)}.source-workspace-tabs{display:flex;flex-wrap:wrap;background:var(--bg-surface-alt);border-bottom:var(--border-default);padding:0 12px}.ws-tab{display:flex;align-items:center;gap:8px;padding:8px 16px!important;font-size:12px!important;font-weight:500!important;color:var(--text-muted)!important;border-bottom:2px solid transparent!important;white-space:nowrap}.ws-tab.active{color:var(--amber)!important;border-bottom-color:var(--amber)!important}.ws-tab img{filter:brightness(0) saturate(100%) invert(64%) sepia(10%) saturate(136%) hue-rotate(201deg)}.source-work{display:flex;height:215px}.panel{flex-shrink:0;background:var(--bg-surface);width:220px;min-width:0}.panel.right{width:290px}.panel-head{height:26px;background:var(--bg-surface-alt);padding:0 8px;font-size:11px;font-weight:600;display:flex;align-items:center}.canvas{flex:1;padding:20px;background:var(--bg-app);min-width:0}.canvas h2{font:18px Space,Inter;margin:0 0 8px}.canvas p{color:var(--text-muted);margin:0}.source-status{height:28px;background:var(--bg-statusbar);color:var(--text-on-dark);padding:0 12px;display:flex;align-items:center;font-size:12px}.measure{margin-top:22px;overflow-x:auto}table{width:100%;border-collapse:collapse;background:white}th,td{text-align:left;border-bottom:1px solid #e1e1e5;padding:9px 11px;vertical-align:top}thead th{background:#e8e8eb}tbody th{width:140px}td{min-width:180px}td:last-child{min-width:280px}a{color:#a95200}small{color:#74747d}.readout{font:11px/1.5 ui-monospace,monospace;color:#595961;margin:8px 0 0}@media(max-width:650px){.hero{padding:20px}main{padding:12px}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Frame Studio · maat- en shellreview</h1><p>Bron-CSS op commit eb77f9e naast de huidige Rust-crate. De replica hieronder gebruikt de bronmaten en -kleurrollen; een originele runtimecapture ontbreekt.</p></div><main><div class="note"><strong>Ontwerpbesluit.</strong> Open Frame vraagt een eigen shellprofiel: 36 px titelbalk, flexibele ribbon, omvouwende werkruimtetabs, 220/290 px zijpanelen en 28 px status. De huidige 32/94/30/22 px Rust-maten blijven passend voor de bestaande gedeelde basis. De tabrij mag niet worden platgedrukt tot een documentbalk. In het lichte bronthema is het contrast van inactieve werkruimtetabs 2,23:1 en van linttabs 2,06:1; met de bestaande secundaire tekstkleur wordt dat respectievelijk 6,69:1 en 6,12:1. Dat is een gericht harmonisatievoorstel, geen kopie van de bron.</div><div class="toolbar"><label>Vensterbreedte <input id="width" type="range" min="720" max="1600" step="20" value="1200"><output id="width-value">1200 px</output></label><label><input id="light" type="checkbox"> Licht thema</label></div><div class="viewport"><div class="frame" id="frame" data-theme="default"><div class="source-title"><span><strong>Open Frame Studio</strong> · Bestand · Instellingen</span><span class="window-actions"><span>−</span><span>□</span><span>×</span></span></div><div class="source-ribbon"><div class="source-ribbon-tabs"><button class="file">Bestand</button><button class="active">Home</button><button>Invoegen</button><button>IFC / Export</button><button>Productie</button><button>Beeld</button></div><div class="source-ribbon-content"><div class="group"><span class="group-label">Nieuw kozijn</span><div class="commands"><span class="command"><img src="../harmonization/inline-ui-icons/open-frame-studio/ribbon-01.svg" width="24" height="24" alt="">Leeg</span><span class="command"><img src="../harmonization/inline-ui-icons/open-frame-studio/ribbon-02.svg" width="24" height="24" alt="">Draaikiep</span><span class="command"><img src="../harmonization/inline-ui-icons/open-frame-studio/ribbon-03.svg" width="24" height="24" alt="">Dubbel</span></div></div><div class="group"><span class="group-label">Bewerken</span><div class="commands"><span class="command"><img src="../harmonization/inline-ui-icons/open-frame-studio/ribbon-10.svg" width="24" height="24" alt="">Kolom</span><span class="command"><img src="../harmonization/inline-ui-icons/open-frame-studio/ribbon-11.svg" width="24" height="24" alt="">Rij</span></div></div></div></div><div class="source-workspace-tabs">''' + tabs + '''</div><div class="source-work"><div class="panel"><div class="panel-head">Kozijnen</div></div><div class="canvas"><h2>2D Editor</h2><p>Werkgebied met brongebonden paneelmaten</p></div><div class="panel right"><div class="panel-head">Eigenschappen · AI</div></div></div><div class="source-status">Open Frame Studio · zoom 35%</div></div></div><p class="readout" id="readout">Maten worden in de browser op deze replica gemeten.</p><div class="measure"><table><thead><tr><th>Gebied</th><th>Open Frame-bron</th><th>Gedeelde Rust nu</th><th>Harmonisatieregel</th></tr></thead><tbody>''' + rows + '''</tbody></table></div></main><script>const slider=document.querySelector('#width'),frame=document.querySelector('#frame'),light=document.querySelector('#light');function update(){frame.style.setProperty('--preview-width',slider.value+'px');frame.dataset.theme=light.checked?'light':'default';document.querySelector('#width-value').textContent=slider.value+' px';const h=x=>Math.round(frame.querySelector(x).getBoundingClientRect().height);document.querySelector('#readout').textContent='Replica in browser · titel '+h('.source-title')+' px · ribbon '+h('.source-ribbon')+' px · werkruimtetabs '+h('.source-workspace-tabs')+' px · status '+h('.source-status')+' px';}slider.oninput=update;light.onchange=update;update();</script></html>'''
(ROOT / 'design/frame-layout-review.html').write_text(page)
print('Open Frame source geometry compared with six shared Rust shell metrics')
