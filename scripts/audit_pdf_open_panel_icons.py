#!/usr/bin/env python3
"""Inventory SVGs rendered by PDF Studio's desktop Open panel."""
import hashlib
import json
import re
import subprocess
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
path = 'open-pdf-studio/js/solid/components/app-menu/OpenPanel.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/open-panel'
out.mkdir(parents=True, exist_ok=True)

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
menu = source('open-pdf-studio/js/solid/components/app-menu/AppMenu.jsx')
assert "import OpenPanel from './OpenPanel.jsx'" in menu
assert '<OpenPanel />' in menu

# The role is determined at each JSX call site, not from its SVG filename or shape.
roles = [
    ('recent-document', 'Bestand in recentlijst', 'document', 'recent'),
    ('pin-recent', 'Recent bestand vastzetten/losmaken', 'action', 'recent'),
    ('remove-recent', 'Recent bestand verwijderen', 'action', 'recent'),
    ('search-recent', 'Recente bestanden zoeken', 'search', 'recent'),
    ('pinned-chevron', 'Vastgezette lijst in-/uitklappen', 'disclosure', 'recent'),
    ('unpinned-chevron', 'Andere lijst in-/uitklappen', 'disclosure', 'recent'),
    ('session-tile', 'Opgeslagen sessie', 'object', 'sessions'),
    ('remove-session', 'Sessie verwijderen', 'action', 'sessions'),
    ('site-document', 'Site-document', 'document', 'site'),
    ('add-place', 'Maplocatie toevoegen', 'action', 'places'),
    ('place-folder', 'Maplocatie', 'object', 'places'),
    ('remove-place', 'Maplocatie verwijderen', 'action', 'places'),
    ('place-document', 'PDF in maplocatie', 'document', 'places'),
    ('nav-site', 'Navigatie: site', 'navigation', 'site'),
    ('nav-recent', 'Navigatie: recent', 'navigation', 'recent'),
    ('nav-sessions', 'Navigatie: sessies', 'navigation', 'sessions'),
    ('nav-url', 'Navigatie: openen van URL', 'navigation', 'url'),
    ('nav-places', 'Navigatie: locaties', 'navigation', 'places'),
    ('nav-browse', 'Navigatie: bladeren', 'navigation', 'browse'),
]
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
assert len(matches) == len(roles) == 19
records = []
for ordinal, (match, (name, label, role, panel)) in enumerate(zip(matches, roles), 1):
    line = code.count('\n', 0, match.start()) + 1
    raw = match.group()
    dynamic = []
    if 'fill={props.file.pinned ?' in raw:
        dynamic.append('fill=none/filled according to pinned state')
        raw = raw.replace("fill={props.file.pinned ? 'currentColor' : 'none'}", 'fill="none"')
    if 'class={`open-panel-chevron${' in raw:
        dynamic.append('chevron rotation according to collapsed state')
        raw = re.sub(r'class=\{`open-panel-chevron\$\{[^}]+\}[^`]*`\}\s*', '', raw, count=1)
    assert '{' not in raw, (name, raw)
    svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1) if 'xmlns=' not in raw else raw
    ET.fromstring(svg)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
    filename = f'{name}.svg'
    (out / filename).write_text(svg)
    record = {'file': path, 'line': line, 'ordinal': ordinal, 'name': name,
              'label': label, 'role': role, 'subpanel': panel,
              'state': 'conditional' if panel in ('site', 'recent', 'sessions', 'places') else 'always-available',
              'svg': f'inline-ui-icons/open-pdf-studio/open-panel/{filename}',
              'sha256': hashlib.sha256(svg.encode()).hexdigest()}
    if dynamic:
        record['source_dynamic_state'] = dynamic
    if '<text' in svg:
        record['native_preview_limitation'] = 'Iced SVG render omits PDF lettering from source <text>'
    records.append(record)

hashes = {}
for item in records:
    hashes.setdefault(item['sha256'], []).append(item['name'])
duplicates = [names for names in hashes.values() if len(names) > 1]
manifest = {'repository': 'open-pdf-studio', 'commit': commit,
            'scope': 'All 19 literal SVG call sites in source-reachable desktop OpenPanel.jsx. Every site renders a visible UI symbol when its panel/data state is active; repetitions are preserved as separate placements.',
            'literal_svg_sites': 19, 'ui_icon_placements': 19,
            'distinct_source_shapes': len(hashes), 'duplicate_shapes': duplicates,
            'records': records}
(root / 'harmonization/pdf-open-panel-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
    warning = f'<p class="warning">{escape(item["native_preview_limitation"])}</p>' if 'native_preview_limitation' in item else ''
    dynamic = f'<p class="dynamic">Bronstatus: {escape("; ".join(item["source_dynamic_state"]))}</p>' if 'source_dynamic_state' in item else ''
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{item["line"]}'
    cards.append(f'<article data-search="{escape((item["name"]+" "+item["label"]+" "+item["role"]+" "+item["subpanel"]).lower())}"><h2>{escape(item["label"])}</h2><small>{escape(item["name"])} · {escape(item["role"])} · {escape(item["subpanel"])}</small><div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div>{dynamic}{warning}<a href="{url}">Bronregel {item["line"]} ↗</a></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · Openen-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}article{background:#fff;border:1px solid #d8d8dc;padding:14px}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d6d6da}.samples span{display:flex;flex-direction:column;gap:3px;align-items:center}.samples small{font-size:9px}.light{background:#fafaf9}.dark{background:#303039;border-color:#53535d!important}.light img{filter:brightness(0) saturate(100%) invert(20%)}.dark img{filter:brightness(0) invert(1)}article>a{font-size:11px;color:#a95200}.dynamic,.warning{font-size:11px;margin:6px 0}.dynamic{color:#57534e}.warning{color:#b45309}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · Bestand openen</h1><p>Alle 19 letterlijke SVG-plaatsen uit het bereikbare desktop-openpaneel. De plaatsen zijn UI-gebonden, maar subpanelen, data en status bepalen wanneer ze zichtbaar zijn.</p></div><main><div class="note"><strong>Brongebonden telling.</strong> Herhaalde vormen blijven afzonderlijke UI-plaatsen: een PDF-document staat in recent, site en map; sluiten komt bij bestand, sessie en locatie voor. De bron heeft dynamische pin- en chevronstatus. De PDF-letter in het documentpictogram is SVG-tekst en moet voor native Rust-rendering als paden worden getekend.</div><input id="search" type="search" placeholder="Zoek pictogram of paneel" aria-label="Zoek pictogram of paneel"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.oninput=()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
(root / 'design/pdf-open-panel-icon-review.html').write_text(page)
print(f'PDF OpenPanel: {len(records)} UI SVG placements; {len(hashes)} distinct exact SVG shapes')
