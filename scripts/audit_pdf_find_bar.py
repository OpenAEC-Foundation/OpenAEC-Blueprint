#!/usr/bin/env python3
"""Pin PDF FindBar UI icons and make a CSS-faithful, interactive layout review."""
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
prefix = 'open-pdf-studio/'

def source(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{prefix}{path}'], text=True)

assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == commit
app = source('js/solid/App.jsx')
code = source('js/solid/components/FindBar.jsx')
css = source('styles/find-bar.css')
store = source('js/solid/stores/findBarStore.js')
locale = json.loads(source('js/i18n/locales/nl/statusbar.json'))
assert "import FindBar from './components/FindBar.jsx'" in app and '<FindBar />' in app
assert '<div class="main-view">' in app and app.index('<FindBar />') > app.index('<div class="main-view">')
assert 'searchInText, setSearchInText] = createSignal(true)' in store
assert 'searchInAnnotations, setSearchInAnnotations] = createSignal(true)' in store
assert 'resultsOpen, setResultsOpen] = createSignal(true)' in store

specs = [
    ('previous', 'Vorige treffer', 'navigation', 119),
    ('next', 'Volgende treffer', 'navigation', 124),
    ('whole-word', 'Hele woorden', 'toggle', 145),
    ('highlight-all', 'Alles markeren', 'toggle', 156),
    ('close', 'Zoekbalk sluiten', 'action', 163),
]
matches = list(re.finditer(r'<svg\b[\s\S]*?</svg>', code))
lines = [code.count('\n', 0, m.start()) + 1 for m in matches]
assert lines == [s[3] for s in specs]
out = root / 'harmonization/inline-ui-icons/open-pdf-studio/find-bar'
out.mkdir(parents=True, exist_ok=True)
records = []
inline = {}
for match, (name, label, role, line) in zip(matches, specs):
    svg = match.group()
    assert '{' not in svg
    ET.fromstring(svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1))
    inline[name] = svg
    saved = re.sub(r'\s+', ' ', svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)).replace('> <', '><').strip() + '\n'
    (out / f'{name}.svg').write_text(saved)
    records.append({'name': name, 'label': label, 'role': role,
                    'source_file': prefix + 'js/solid/components/FindBar.jsx',
                    'source_line': line,
                    'svg': f'inline-ui-icons/open-pdf-studio/find-bar/{name}.svg',
                    'sha256': hashlib.sha256(saved.encode()).hexdigest()})

metrics = {
    'anchor_top_px': 4, 'anchor_right_px': 12,
    'max_width': 'calc(100% - 24px)', 'bar_padding_px': 4,
    'row_gap_px': 2, 'stack_gap_px': 4,
    'input_height_px': 24, 'input_text_width_px': 180, 'input_wrapper_min_width_px': 90,
    'count_min_width_px': 50, 'navigation_button_px': [22, 22],
    'toggle_button_px': [24, 22], 'close_button_px': [22, 22],
    'source_checkbox_px': 13, 'results_list_max_height_px': 150,
    'source_css': prefix + 'styles/find-bar.css',
}
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'Five literal UI SVG sites in source-reachable FindBar.jsx, rendered inside App.jsx main-view. Aa case sensitivity, checkboxes, and Unicode disclosure carets are UI controls but not SVGs. Search-highlight rectangles are document overlays, not icons.',
    'literal_svg_sites': 5, 'ui_symbol_sites': 5,
    'non_svg_controls': ['Aa case-sensitivity text button', 'Text and Annotations checkboxes', 'results disclosure ▾/▸'],
    'source_state_defaults': {'visible': False, 'text': True, 'annotations': True, 'results_open': True, 'highlight_all': True, 'match_case': False, 'whole_word': False},
    'metrics': metrics,
    'states_reviewed': ['open-no-query', 'results-expanded', 'not-found', 'both-sources-off', 'narrow-viewer'],
    'limitations': ['No source runtime screenshot is available for a pixel-difference comparison.', 'Result text and document page in the HTML are illustrative data.', 'The HTML uses the pinned source CSS and original inline SVG geometry for the find bar.'],
    'records': records,
}
(root / 'harmonization/pdf-find-bar-ui-icons.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

def icon(name):
    return inline[name]

bar = f'''<div class="find-bar visible"><div class="find-rows"><div class="find-row"><div class="find-input-wrapper"><input class="find-input" placeholder="{escape(locale['findPlaceholder'])}" aria-label="{escape(locale['findPlaceholder'])}"><span class="find-count-inline"></span></div><button class="find-btn" title="{escape(locale['previousShiftEnter'])}" disabled>{icon('previous')}</button><button class="find-btn" title="{escape(locale['nextEnter'])}" disabled>{icon('next')}</button><div class="find-separator"></div><button class="find-toggle-btn" title="{escape(locale['matchCase'])}">Aa</button><button class="find-toggle-btn" title="{escape(locale['wholeWords'])}">{icon('whole-word')}</button><button class="find-toggle-btn active" title="{escape(locale['highlightAll'])}">{icon('highlight-all')}</button><button class="find-close-btn" title="{escape(locale['closeEsc'])}">{icon('close')}</button></div><div class="find-row find-sources"><label class="find-check"><input type="checkbox" checked> {escape(locale['searchInText'])}</label><label class="find-check"><input type="checkbox" checked> {escape(locale['searchInAnnotations'])}</label><span class="find-sources-hint" hidden>{escape(locale['searchNoSources'])}</span></div><div class="find-results" hidden><button class="find-results-header"><span class="find-results-caret">▾</span><span class="results-title">Resultaten (7)</span></button><div class="find-results-list"><button class="find-results-row current"><span class="find-results-page">Pagina 2</span><span class="find-results-count">4 treffers</span><span class="find-results-kinds">Tekst</span></button><button class="find-results-row"><span class="find-results-page">Pagina 5</span><span class="find-results-count">3 treffers</span><span class="find-results-kinds">Annotaties</span></button></div></div></div><span class="find-message" hidden>Geen resultaten gevonden</span></div>'''

cards = []
for r in records:
    href = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{r["source_file"]}#L{r["source_line"]}'
    imgs = ''.join(f'<span><img src="../harmonization/{r["svg"]}" width="{size}" height="{size}" alt=""><small>{size}px</small></span>' for size in (16, 24, 32))
    cards.append(f'<article><b>{escape(r["label"])}</b><em>{escape(r["role"])}</em><div class="sizes"><div class="light">{imgs}</div><div class="dark">{imgs}</div></div><a href="{href}">Bronregel {r["source_line"]} ↗</a></article>')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF · Zoekbalk-schermreview</title><style>
:root{font:14px/1.5 system-ui,sans-serif;color:#303039;background:#f2f2f4}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:4px solid #df8421;padding:27px max(18px,calc((100vw - 1250px)/2))}header a{font-size:12px;color:#ffcb8b}h1{font-size:29px;letter-spacing:-.03em;margin:7px 0}header p{max-width:900px;margin:0;color:#d7d7df}main{max-width:1290px;margin:auto;padding:20px}.intro{background:#fff;border-left:4px solid #df8421;border-top:1px solid #dedee4;border-right:1px solid #dedee4;border-bottom:1px solid #dedee4;padding:13px 16px}.intro p{margin:5px 0}.layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:16px;margin-top:18px}.controls,.preview,.evidence{background:#fff;border:1px solid #d9d9e0;padding:16px}.controls label{display:block;margin:12px 0 5px;font-weight:600;font-size:12px}.controls select,.controls input[type=range]{width:100%;font:inherit}.controls output{display:block;color:#6f6f79;font-size:12px}.preview{min-width:0;overflow:hidden}.viewer{position:relative;width:500px;max-width:100%;height:240px;background:#dedee4;border:1px solid #bebec8;overflow:visible;--theme-surface:#fff;--theme-border:#d4d4d4;--theme-bg:#fff;--theme-text:#333;--theme-text-secondary:#888;--theme-hover:#e5e5e5;--theme-active:#d5d5d5;--theme-accent:#0078d4}.viewer.forge{background:#24242b;--theme-surface:#303039;--theme-border:#555560;--theme-bg:#27272e;--theme-text:#f2f2f4;--theme-text-secondary:#b0b0bc;--theme-hover:#45454e;--theme-active:#555560;--theme-accent:#df8421}.page-mock{position:absolute;left:24px;top:42px;width:190px;height:184px;background:#fff;border:1px solid #cacad2;box-shadow:0 2px 8px #0002;padding:25px;color:#9a9aa5;font:11px system-ui}.page-mock i{display:block;height:5px;background:#dddde3;margin:10px 0}.viewer.forge .page-mock{background:#dddde1}.ruler{display:flex;gap:8px;flex-wrap:wrap;color:#777783;font-size:11px;margin-top:12px}.ruler span{background:#f2f2f4;padding:3px 7px}.evidence{margin-top:16px}.evidence h2{font-size:17px;margin:0 0 7px}.evidence p{margin:4px 0}.icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-top:16px}.icons article{background:#fff;border:1px solid #d9d9e0;padding:12px}.icons b{display:block}.icons em{font-size:11px;color:#777783;font-style:normal}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:9px 0}.sizes>div{display:flex;justify-content:space-around;align-items:center;min-height:65px;border:1px solid #d9d9e0}.sizes .light{background:#fff}.sizes .dark{background:#303039}.sizes .dark img{filter:brightness(0) invert(1)}.sizes span{display:flex;flex-direction:column;align-items:center;gap:3px}.sizes small{font-size:9px;color:#777783}.sizes .dark small{color:#ddd}.icons a{color:#a45b08;font-size:11px}footer{font-size:11px;color:#777783;margin:18px 0}@media(max-width:740px){.layout{grid-template-columns:1fr}main{padding:10px}.preview{overflow:auto}}
''' + css + '''
</style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · Zoekbalk</h1><p>Interactieve indelingsstudie uit de gepinde FindBar-structuur, Nederlandse labels en originele CSS. Selecteer een toestand, breedte en thema om het brongedrag te beoordelen.</p></header><main><div class="intro"><strong>Bron en grens.</strong><p>De zoekbalk staat rechtsboven in de documentweergave: 4 px van boven, 12 px van rechts. De eerste rij bevat het zoekveld, twee pijlen, Aa en twee SVG-opties; de tweede rij bevat Tekst en Annotaties. Bij treffers volgt een uitklapbare lijst met maximaal 150 px hoogte. Alle vijf SVG’s zijn echte UI-knoppen. Aa, vinkjes en ▾/▸ zijn ook bediening, maar geen SVG’s.</p><p>De documentpagina en trefferaantallen hieronder zijn voorbeelddata. Er is geen bronruntime-screenshot voor een verschilbeeld; deze studie gebruikt de originele CSS en SVG-geometrie, maar claimt geen pixelgelijke native Rust-weergave.</p></div><div class="layout"><div class="controls"><label for="theme">Thema</label><select id="theme"><option value="light">Light</option><option value="forge">Forge</option></select><label for="state">Toestand</label><select id="state"><option value="idle">Open · lege zoekopdracht</option><option value="results">Treffers · lijst open</option><option value="closed">Treffers · lijst dicht</option><option value="notfound">Geen treffer</option><option value="sourcesoff">Beide bronnen uit</option></select><label for="width">Documentvlakbreedte</label><input id="width" type="range" min="260" max="700" value="500" step="10"><output id="widthout">500 px</output></div><div class="preview"><div id="viewer" class="viewer"><div class="page-mock" aria-hidden="true">Voorbeeldpagina<i></i><i></i><i></i><i></i></div>''' + bar + '''</div><div class="ruler"><span>anker: 4 px boven · 12 px rechts</span><span>veld: 24 px hoog</span><span>navigatie: 22 × 22 px</span><span>opties: 24 × 22 px</span><span>lijst: maximaal 150 px hoog</span></div></div></div><div class="evidence"><h2>Layoutbeoordeling</h2><p>De CSS begrenst de balk op <code>calc(100% - 24px)</code>, maar de knoppen blijven op vaste breedte en de eerste rij breekt niet om. Bij een documentvlak rond 260–280 px kan de rij intern buiten de begrensde balk lopen. Voor de Rust-component is een expliciete compacte toestand of overflow-keuze nodig.</p><p>De bron gebruikt een blauw accent voor de actieve zoekoptie; Forge in deze studie zet dat thematisch naar amber. Dat is een harmonisatievoorstel en geen eigenschap van de gepinde PDF-bron. De bronhighlight in de PDF-pagina blijft apart van deze zoekbalkiconen.</p></div><div class="icons">''' + ''.join(cards) + '''</div><footer>Bron: open-pdf-studio @ ''' + commit + ''' · FindBar.jsx · find-bar.css · Nederlandse statusbar-locale</footer></main><script>
const state=document.querySelector('#state'),theme=document.querySelector('#theme'),width=document.querySelector('#width'),viewer=document.querySelector('#viewer'),bar=document.querySelector('.find-bar');function render(){viewer.style.width=width.value+'px';document.querySelector('#widthout').textContent=width.value+' px';viewer.classList.toggle('forge',theme.value==='forge');const value=state.value;const found=value==='results'||value==='closed';const none=value==='notfound';const off=value==='sourcesoff';bar.querySelector('.find-input').value=found?'constructie':none?'nietsgevonden':'';bar.querySelector('.find-count-inline').textContent=found?'1 van 7':'';bar.querySelector('.find-input-wrapper').classList.toggle('not-found',none);bar.querySelector('.find-message').hidden=!none;bar.querySelector('.find-results').hidden=!found;bar.querySelector('.find-results-list').hidden=value==='closed';bar.querySelector('.find-results-caret').textContent=value==='closed'?'▸':'▾';for(const b of bar.querySelectorAll('.find-btn'))b.disabled=!found;for(const c of bar.querySelectorAll('.find-check input'))c.checked=!off;bar.querySelector('.find-sources-hint').hidden=!off}for(const el of [state,theme,width])el.addEventListener('input',render);bar.querySelector('.find-results-header').addEventListener('click',()=>{state.value=state.value==='closed'?'results':'closed';render()});render();
</script></html>'''
(root / 'design/pdf-find-bar-screen-review.html').write_text(page)
print('PDF FindBar: 5 UI SVG sites; CSS layout and five states reviewed')
