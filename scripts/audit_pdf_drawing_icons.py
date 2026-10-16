#!/usr/bin/env python3
"""Extract only source-reachable literal Drawing ribbon icons from PDF Studio."""
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
path = 'open-pdf-studio/js/solid/components/ribbon/DrawingTab.jsx'
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/drawing'
out.mkdir(parents=True, exist_ok=True)
native_fallbacks = {
    'scaleRegionIcon': 'scale-region.svg',
    'scaleRegionFullPageInline': 'scale-region-full-page.svg',
    'radiusIcon': 'radius.svg',
}

def source(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{name}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
code = source(path)
ribbon = source('open-pdf-studio/js/solid/components/ribbon/Ribbon.jsx')
assert "import DrawingTab from './DrawingTab.jsx'" in ribbon
assert "<Match when={activeTab() === 'drawing'}><DrawingTab /></Match>" in ribbon
locale = json.loads(source('open-pdf-studio/js/i18n/locales/nl/ribbon.json'))

def translated(key):
    node = locale
    for part in key.split('.'):
        node = node.get(part) if isinstance(node, dict) else None
    return node if isinstance(node, str) else key

buttons = list(re.finditer(r'<RibbonButton\b[\s\S]*?/>', code))
svg_sites = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
assert len(svg_sites) == 38
records = []
for ordinal, match in enumerate(svg_sites, 1):
    line = code.count('\n', 0, match.start()) + 1
    before = code[max(0, match.start() - 90):match.start()]
    definition = re.search(r'const\s+(\w+)\s*=\s*`\s*$', before)
    name = definition.group(1) if definition else 'scaleRegionFullPageInline'
    if ordinal <= 37:
        assert definition, (ordinal, line)
    else:
        assert name == 'scaleRegionFullPageInline' and line == 313
    uses = []
    if name != 'scaleRegionFullPageInline':
        for button in buttons:
            if f'icon={{{name}}}' not in button.group():
                continue
            tag = button.group()
            id_match = re.search(r'\bid="([^"]+)"', tag)
            assert id_match, (name, tag[:80])
            key = re.search(r'\blabel=\{t\(\'([^\']+)\'\)', tag)
            title_key = re.search(r'\btitle=[^>]*?t\(\'([^\']+)\'\)', tag)
            literal_title = re.search(r'\btitle="([^"]+)"', tag)
            selected_key = key or title_key
            label = (translated(selected_key.group(1)) if selected_key else
                     literal_title.group(1) if literal_title else id_match.group(1))
            uses.append({'file': path, 'line': code.count('\n', 0, button.start()) + 1,
                         'button_id': id_match.group(1), 'label': label,
                         'translation_key': selected_key.group(1) if selected_key else None})
    else:
        assert 'id="btn-create-scale-region-full-page"' in code[match.start() - 260:match.start()]
        uses.append({'file': path, 'line': 310, 'button_id': 'btn-create-scale-region-full-page',
                     'label': translated('comment.scaleRegionFullPage'),
                     'translation_key': 'comment.scaleRegionFullPage'})
    kind = 'unused-placeholder' if not uses else 'ui-icon'
    state = ('not-rendered' if not uses else
             'always-disabled' if name == 'tableIcon' else
             'selection-conditional' if all(408 <= use['line'] <= 445 for use in uses) else
             'document-readonly-conditional')
    entry = {'file': path, 'line': line, 'ordinal': ordinal,
             'definition': name, 'kind': kind, 'state': state, 'uses': uses}
    if uses:
        raw = match.group()
        assert '{' not in raw, (name, raw)
        svg = raw.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        ET.fromstring(svg)
        svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip() + '\n'
        filename = f'drawing-{ordinal:02}.svg'
        (out / filename).write_text(svg)
        entry['svg'] = f'inline-ui-icons/open-pdf-studio/drawing/{filename}'
        entry['sha256'] = hashlib.sha256(svg.encode()).hexdigest()
        entry['review'] = ('compare-with-DomainIcon::TransformMove' if name == 'moveIcon' else
                           'compare-with-DomainIcon::DrawingTrim' if name in ('trimIcon', 'cutIcon') else
                           'compare-with-DomainIcon::DrawingExtend' if name == 'extendIcon' else
                           'compare-with-DomainIcon::DrawingOffset' if name == 'offsetIcon' else
                           'split-duplicate-and-clipboard-copy' if name == 'copyAnnIcon' else
                           'keep-disabled-until-command-exists' if name == 'tableIcon' else
                           'design-PDF-drawing-command')
        if name in native_fallbacks:
            candidate = root / 'harmonization/proposals/pdf-drawing-native' / native_fallbacks[name]
            candidate_text = candidate.read_text()
            assert '<text' not in candidate_text
            ET.fromstring(candidate_text)
            small = candidate.with_name(candidate.stem + '-small.svg')
            small_text = small.read_text()
            assert '<text' not in small_text
            ET.fromstring(small_text)
            entry['native_preview_limitation'] = 'Iced software SVG render omits source <text> glyph'
            entry['vector_fallback'] = str(candidate.relative_to(root / 'harmonization'))
            entry['vector_fallback_small'] = str(small.relative_to(root / 'harmonization'))
    records.append(entry)

icons = [entry for entry in records if entry['kind'] == 'ui-icon']
assert len(icons) == 37 and len(records) == 38
assert sum(len(entry['uses']) for entry in icons) == 38
assert len({entry['svg'] for entry in icons}) == 37
assert next(entry for entry in records if entry['definition'] == 'placeholderIcon')['kind'] == 'unused-placeholder'
assert next(entry for entry in records if entry['definition'] == 'tableIcon')['state'] == 'always-disabled'
assert len([entry for entry in records if entry['state'] == 'selection-conditional']) >= 10
duplicates = defaultdict(list)
for entry in icons:
    duplicates[entry['sha256']].append(entry['definition'])
same_shape = [{'sha256': digest, 'definitions': definitions}
              for digest, definitions in duplicates.items() if len(definitions) > 1]
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'Every literal SVG in the source-reachable desktop DrawingTab.jsx; imported ribbonIcons.js vectors are a separate category. One defined placeholder has no button use.',
    'svg_sites': len(records), 'ui_icon_definitions': len(icons),
    'ui_button_uses': sum(len(entry['uses']) for entry in icons),
    'excluded_unused_definitions': 1, 'identical_source_shapes': same_shape,
    'records': records,
}
(root / 'harmonization/pdf-drawing-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for item in records:
    label = ' / '.join(use['label'] for use in item['uses']) if item['uses'] else 'Ongebruikte placeholder'
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{item["line"]}'
    if item['kind'] == 'ui-icon':
        samples = ''.join(f'<span><img src="../harmonization/{item["svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
        body = f'<div class="samples"><div class="light">{samples}</div><div class="dark">{samples}</div></div><p class="decision">{escape(item["review"])}</p>'
        if 'vector_fallback' in item:
            candidate = item['vector_fallback']
            fallback = ''.join(f'<span><img src="../harmonization/{item["vector_fallback_small"] if size == 16 else candidate}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32))
            body += f'<p class="decision">Native aandachtspunt: {escape(item["native_preview_limitation"])}. Path-gebaseerde ontwerpvariant:</p><div class="samples"><div class="light">{fallback}</div><div class="dark">{fallback}</div></div>'
        links = ' · '.join(f'<a href="https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{path}#L{use["line"]}">{escape(use["button_id"])} ↗</a>' for use in item['uses'])
    else:
        body = '<p class="excluded">Geen UI-aanroep gevonden. Deze placeholder is geen geteld UI-icoon.</p>'
        links = ''
    cards.append(f'<article data-kind="{escape(item["kind"])}" data-search="{escape((label+" "+item["definition"]+" "+item["state"]).lower())}"><h2>{escape(label)}</h2><small>{escape(item["definition"])} · {escape(item["state"])} · L{item["line"]}</small>{body}<a href="{escape(url)}">Definitie ↗</a> {links}</article>')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · Tekenen-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}.hero{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}.hero a{color:#ffc47e}.hero h1{font-size:27px;margin:8px 0 4px}.hero p{max-width:1050px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}.stats span{background:white;border:1px solid #d6d6da;padding:7px 10px}.stats b{color:#a95200}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(400px,100%);margin-bottom:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}article{background:white;border:1px solid #d8d8dc;padding:14px}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.samples{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.samples>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d6d6da}.samples span{display:flex;flex-direction:column;gap:3px;align-items:center}.samples small{font-size:9px}.light{background:#fafaf9}.dark{background:#303039;border-color:#53535d!important}.light img{filter:brightness(0) saturate(100%) invert(20%)}.dark img{filter:brightness(0) invert(1)}.decision{font-size:11px;color:#57534e}.excluded{min-height:75px;color:#696972}article>a{font-size:11px;color:#a95200}article[data-kind=unused-placeholder]{background:#fafafa}@media(max-width:650px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><div class="hero"><a href="review.html">← Ontwerpreview</a><h1>Open PDF Studio · Tekenen-ribbon</h1><p>38 letterlijke SVG-plaatsen uit de actuele Solid-bron op commit f754cb7; 37 staan op echte knoppen. Geïmporteerde vectoren uit ribbonIcons.js zijn een aparte broncategorie.</p></div><main><div class="note"><strong>Brongebonden selectie.</strong> De generieke placeholder wordt nergens aangeroepen. De Tabel-knop is zichtbaar maar permanent uitgeschakeld; de bewerkingsgroep verschijnt pas bij geselecteerde annotaties. Eén kopieervorm bedient dupliceren én klembordkopiëren, en Trim/Knippen delen een vorm terwijl het andere opdrachten zijn. Naam- of bytegelijkheid leidt daarom niet automatisch tot één Rust-commando.</div><div class="stats"><span><b>37</b> gebruikte SVG-definities</span><span><b>38</b> knopplaatsen</span><span><b>1</b> ongebruikte placeholder</span><span><b>1</b> uitgeschakelde knop</span></div><input id="search" type="search" placeholder="Zoek knop of definitie" aria-label="Zoek knop of definitie"><div class="grid">''' + ''.join(cards) + '''</div></main><script>const q=document.querySelector('#search');q.oninput=()=>{for(const card of document.querySelectorAll('article'))card.hidden=!card.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
page = page.replace(
    '</div></main><script>',
    '</div><section style="margin-top:24px"><h2>Native Rust-renders</h2><p>Deze contactbladen tonen alle 37 gebruikte bron-SVG’s op 24 px. Bij Straal en beide Schaalgebied-knoppen ontbreekt de SVG-tekst in deze renderer; de path-gebaseerde varianten boven zijn een voorstel, geen bronkopie.</p><img src="pdf-drawing-icons-light.png" alt="PDF Tekenen-broniconen in Light" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #d6d6da"><img src="pdf-drawing-icons-forge.png" alt="PDF Tekenen-broniconen in Forge" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #53535d"></section></main><script>',
    1,
)
page = page.replace(
    '</section></main><script>',
    '<h2>SVG-tekst als paden</h2><p>Per rij: oorspronkelijke 24px-bronrender, ontwerpvariant op 16, 24 en 32 px. De 16px-versie heeft een eigen vereenvoudigde geometrie.</p><img src="pdf-drawing-text-fallback-light.png" alt="Path-gebaseerde schaal- en straaliconen in Light" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #d6d6da"><img src="pdf-drawing-text-fallback-forge.png" alt="Path-gebaseerde schaal- en straaliconen in Forge" style="display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #53535d"></section></main><script>',
    1,
)
(root / 'design/pdf-drawing-icon-review.html').write_text(page)
print(f'PDF Drawing: {len(records)} literal SVG sites; {len(icons)} used forms, 38 button uses; placeholder excluded')
