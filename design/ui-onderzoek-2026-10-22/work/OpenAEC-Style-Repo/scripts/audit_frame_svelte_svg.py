#!/usr/bin/env python3
"""Pin and review Open Frame Studio's Svelte SVGs by rendered UI role."""
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/open-frame-studio')
COMMIT = 'eb77f9e4c5d3f5b9b081aef5dd3dcf07dbdaf43f'
OUT = ROOT / 'harmonization/inline-ui-icons/open-frame-studio'
OUT.mkdir(parents=True, exist_ok=True)

# 1-based SVG ordinal within each Svelte source; these are content graphics,
# not reusable command icons. Every other literal SVG is a UI control glyph.
EXCLUDED = {
    'ui/src/components/editor/KozijnEditor.svelte': {1: 'editable-geometry', 2: 'empty-state-illustration'},
    'ui/src/components/editor/VliesgevelEditor.svelte': {1: 'editable-geometry'},
    'ui/src/components/panels/AiAssistant.svelte': {4: 'empty-state-illustration'},
    'ui/src/components/panels/ProfileCrossSection.svelte': {1: 'technical-profile'},
    'ui/src/components/panels/ProfilePreview.svelte': {1: 'technical-profile'},
    'ui/src/components/panels/ShapeManager.svelte': {2: 'technical-preview'},
    'ui/src/components/profile-editor/ProfileCanvas.svelte': {1: 'editable-geometry'},
    'ui/src/components/project/LayoutProtoView.svelte': {1: 'technical-layout'},
}

LABELS = {
    'ui/src/App.svelte': {21: 'Linkerpaneel inklappen', 22: 'AI-paneel',
                          23: 'Rechterpaneel inklappen', 24: 'Linkerpaneel inklappen (3D)',
                          25: 'Rechterpaneel inklappen (3D)'},
    'ui/src/components/panels/AiAssistant.svelte': {2: 'Chat wissen',
                                                     3: 'AI-instellingen', 5: 'Bericht versturen'},
    'ui/src/components/panels/ShapeManager.svelte': {1: 'Vormbeheer sluiten'},
    'ui/src/components/profile-editor/ProfileLibrary.svelte': {1: 'Nieuw profiel',
                                                                4: 'Categorie uitklappen'},
    'ui/src/components/profile-editor/ProfileToolbar.svelte': {
        1: 'Selecteren', 2: 'Punt verwijderen', 3: 'Spiegel horizontaal',
        4: 'Spiegel verticaal', 5: 'Snap aan raster', 6: 'Ongedaan', 7: 'Opnieuw'},
    'ui/src/components/shell/Settings.svelte': {1: 'Instellingen sluiten'},
    'ui/src/components/shell/StatusBar.svelte': {1: 'Ontbrekende hardware'},
    'ui/src/components/shell/TitleBar.svelte': {
        1: 'Instellingen', 2: 'Ongedaan', 3: 'Opnieuw', 4: 'Minimaliseren',
        5: 'Herstellen', 6: 'Maximaliseren', 7: 'Sluiten'},
    'ui/src/components/shell/Toast.svelte': {1: 'Melding sluiten'},
}


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True)


def source(path):
    return git('show', f'{COMMIT}:{path}')


paths = [p for p in git('ls-tree', '-r', '--name-only', COMMIT).splitlines()
         if p.startswith('ui/src/') and p.endswith('.svelte')]
nl = json.loads(source('ui/src/locales/nl.json'))
records = []
for path in paths:
    code = source(path)
    starts = list(re.finditer(r'<svg\b', code))
    for ordinal, match in enumerate(starts, 1):
        line = code.count('\n', 0, match.start()) + 1
        end = code.find('</svg>', match.start())
        assert end >= 0, (path, ordinal)
        raw = code[match.start():end + len('</svg>')]
        kind = EXCLUDED.get(path, {}).get(ordinal, 'ui-icon')
        before = code[max(0, code.rfind('<button', 0, match.start())):match.start()]
        after = code[end + len('</svg>'):code.find('</button>', end) if '</button>' in code[end:] else end + 200]
        keys = re.findall(r"\$_\(['\"]([^'\"]+)['\"]\)", after[:400])
        labels = [nl.get(key, key) for key in keys]
        title = re.findall(r'\btitle="([^"]+)"', before[-350:])
        literal = re.search(r'<span\b[^>]*>\s*([^<{][^<]*?)\s*</span>', after[:400])
        label = (labels[0] if labels else literal.group(1).strip() if literal else
                 title[-1] if title else f'{Path(path).stem} {ordinal:02}')
        label = LABELS.get(path, {}).get(ordinal, label)
        if path == 'ui/src/App.svelte' and ordinal <= 20:
            assert keys and keys[0].startswith('tabs.'), (path, ordinal, keys)
        entry = {'file': path, 'line': line, 'ordinal': ordinal,
                 'kind': kind, 'label': label,
                 'translation_keys': keys[:2]}
        if kind == 'ui-icon':
            # The source uses a theme variable for two quickstart card icons.
            # currentColor preserves the same geometry in both atlas themes.
            normalized = raw.replace('var(--amber)', 'currentColor')
            normalized = normalized.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            ET.fromstring(normalized)
            normalized = re.sub(r'\s+', ' ', normalized).replace('> <', '><').strip() + '\n'
            group = ('workspace' if path == 'ui/src/App.svelte' and ordinal <= 20 else
                     'ribbon' if path.endswith('/Ribbon.svelte') else
                     'shell' if path == 'ui/src/App.svelte' or '/shell/' in path else
                     'editor')
            entry['group'] = group
            slug = re.sub(r'[^a-z0-9-]+', '-', Path(path).stem.lower()).strip('-')
            filename = f'{slug}-{ordinal:02}.svg'
            (OUT / filename).write_text(normalized)
            entry['svg'] = f'inline-ui-icons/open-frame-studio/{filename}'
            entry['sha256'] = hashlib.sha256(normalized.encode()).hexdigest()
        records.append(entry)

assert len(records) == 127
icons = [r for r in records if r['kind'] == 'ui-icon']
excluded = [r for r in records if r['kind'] != 'ui-icon']
assert len(icons) == 118 and len(excluded) == 9
assert len({r['svg'] for r in icons}) == len(icons), 'Filename collision across Svelte components'
assert sum(r['group'] == 'workspace' for r in icons) == 20
assert sum(r['file'].endswith('/Ribbon.svelte') for r in icons) == 52

shapes = defaultdict(list)
for item in icons:
    shapes[item['sha256']].append({'label': item['label'], 'file': item['file'],
                                   'line': item['line']})
reused_shapes = [{'sha256': digest, 'uses': uses} for digest, uses in shapes.items()
                 if len(uses) > 1]
assert len(reused_shapes) == 8

# Prove the shell and workspaces reach the major icon-bearing components.
app = source('ui/src/App.svelte')
for component in ('Ribbon', 'TitleBar', 'AppMenu', 'Settings', 'StatusBar',
                  'AiAssistant', 'KozijnEditor', 'VliesgevelEditor',
                  'ProfileEditorView', 'LayoutProtoView'):
    assert f'<{component}' in app, component
assert '<ProfileToolbar' in source('ui/src/components/profile-editor/ProfileEditorView.svelte')
assert '<ProfileLibrary' in source('ui/src/components/profile-editor/ProfileEditorView.svelte')

manifest = {
    'repository': 'open-frame-studio', 'commit': COMMIT,
    'scope': 'Every literal SVG in pinned ui/src/**/*.svelte, including source-reachable ribbon and workspace controls; technical geometry and empty-state illustrations excluded from icon count.',
    'svg_sites': 127, 'ui_icon_sites': 118, 'excluded_content_graphics': 9,
    'workspace_tabs': 20, 'ribbon_icon_sites': 52,
    'unique_source_shapes': len({r['sha256'] for r in icons}),
    'reused_source_shapes': reused_shapes,
    'records': records,
}
(ROOT / 'harmonization/frame-svelte-svg-audit.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    url = f'https://github.com/OpenAEC-Foundation/open-frame-studio/blob/{COMMIT}/{item["file"]}#L{item["line"]}'
    if item['kind'] == 'ui-icon':
        sample = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
        body = f'<div class="samples"><div class="light">{sample}</div><div class="dark">{sample}</div></div>'
    else:
        body = f'<p class="reason">{escape(item["kind"].replace("-", " "))}: bron-SVG is een tekening of illustratie en geen actieicoon.</p>'
    search = (item['label'] + ' ' + item['file'] + ' ' + item['kind']).lower()
    cards.append(f'<article class="{escape(item["kind"])}" data-search="{escape(search)}"><header><strong>{escape(item["label"])}</strong><small>{escape(item.get("group", item["kind"]))}</small></header><p class="source">{escape(item["file"])}:{item["line"]}</p>{body}<a href="{escape(url)}">Bron ↗</a></article>')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Frame Studio · Svelte-UI-iconen</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f1f1f2}*{box-sizing:border-box}body{margin:0}.hero{background:#303039;color:#fff;border-bottom:3px solid #e58200;padding:25px max(24px,calc((100vw - 1370px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:29px;margin:12px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1410px;margin:auto;padding:24px}.note{background:#fff8ee;border-left:3px solid #e58200;padding:13px 16px;margin-bottom:16px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.stats span{background:#fff;border:1px solid #d8d8de;padding:7px 10px}.stats b{color:#ae5b00}input{font:inherit;padding:10px 13px;border:1px solid #c7c7cf;width:min(100%,420px);margin-bottom:18px}.filters{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}.filters button{font:inherit;border:1px solid #d2d2d8;background:#fff;padding:6px 10px;cursor:pointer}.filters button.active{background:#303039;border-color:#303039;color:white}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:1px solid #d8d8de;padding:14px;min-height:190px}article header{display:flex;justify-content:space-between;gap:8px}article header strong{font-size:12px}article header small{font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#9b5200}.source{font:10px/1.4 ui-monospace,monospace;color:#6d6d75;overflow-wrap:anywhere;margin:7px 0 10px}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:80px;border:1px solid #dadade}.samples span{display:flex;flex-direction:column;align-items:center;gap:4px}.samples small{font-size:9px}.light{background:#fafafa}.dark{background:#303039;border-color:#53535d!important}.light img{filter:brightness(0) saturate(100%) invert(38%) sepia(89%) saturate(1193%) hue-rotate(358deg) brightness(91%)}.dark img{filter:brightness(0) saturate(100%) invert(65%) sepia(70%) saturate(2526%) hue-rotate(357deg) brightness(102%)}.reason{min-height:80px;color:#666671;font-size:12px}article>a{display:inline-block;color:#ac5600;font-size:11px;margin-top:10px}article:not(.ui-icon){background:#fafafa}article[hidden]{display:none}@media(max-width:620px){.hero{padding:20px}main{padding:12px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open Frame Studio · Svelte-SVG-audit</h1><p>127 bron-SVG-plaatsen op commit eb77f9e: werkruimte, lint, Bestand, editor en instellingen.</p></div><main><div class="note"><strong>Brongebonden.</strong> De algemene bestandsiconindex miste deze in Svelte ingebedde vormen. Hier tellen alleen 118 UI-icoonplaatsen mee. Zeven bewerkbare of technische tekeningen en twee lege-staatillustraties blijven buiten de iconset. Acht bronvormen worden dubbel gebruikt; Opslaan/Opslaan als en CNC-export/CNC-werkruimte zijn voorbeelden waarbij dezelfde tekening geen gedeelde Rust-commando-ID mag afdwingen.</div><div class="stats"><span><b>118</b> UI-icoonplaatsen</span><span><b>110</b> bronvormen</span><span><b>20</b> werkruimtetabs</span><span><b>52</b> linticoonplaatsen</span><span><b>9</b> inhoudsgraphics uitgesloten</span></div><input id="search" type="search" aria-label="Zoek icoon of bronbestand" placeholder="Zoek icoon of bronbestand"><div class="filters"><button class="active" data-filter="all">Alles</button><button data-filter="workspace">Werkruimtes</button><button data-filter="ribbon">Lint</button><button data-filter="shell">Shell</button><button data-filter="editor">Editor</button><button data-filter="excluded">Uitgesloten</button></div><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search'),buttons=[...document.querySelectorAll('.filters button')];let filter='all';function update(){for(const card of document.querySelectorAll('article'))card.hidden=!(card.dataset.search.includes(q.value.toLowerCase().trim())&&(filter==='all'||filter==='excluded'&&!card.classList.contains('ui-icon')||card.querySelector('header small').textContent===filter))}q.addEventListener('input',update);for(const b of buttons)b.onclick=()=>{buttons.forEach(x=>x.classList.toggle('active',x===b));filter=b.dataset.filter;update()};</script></html>'''
(ROOT / 'design/frame-svelte-icon-review.html').write_text(page)
print(f'Open Frame: {len(records)} SVG sites; {len(icons)} UI icons, {len(excluded)} content graphics excluded')
