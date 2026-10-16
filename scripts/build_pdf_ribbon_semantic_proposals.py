#!/usr/bin/env python3
"""Review semantically distinct 24px candidates for reused PDF ribbon shapes."""
import json
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
audit = json.loads((root / 'harmonization/pdf-ribbon-imported-ui-icons.json').read_text())
assert audit['commit'] == 'f754cb7c9d9adf654f6894cee15543413c24fcff'
records = {item['name']: item for item in audit['records']}
out = root / 'harmonization/proposals/pdf-ribbon-semantic'
out.mkdir(parents=True, exist_ok=True)

# Plain black source geometry matches the crate's current tintable icon format.
# No text element: Iced drops SVG text in the actual native rendering path.
shapes = {
    'fit-width': '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M2 12h6m-6 0 2-2m-2 2 2 2m18-2h-6m6 0-2-2m2 2-2 2"/>',
    'actual-size': '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M7.5 10.5 9 9v6m-1.5 0h3m4-4.5 1.5-1.5v6m-1.5 0h3" stroke-width="1.3"/><circle cx="12.1" cy="10.5" r=".5" fill="#000" stroke="none"/><circle cx="12.1" cy="13.5" r=".5" fill="#000" stroke="none"/>',
    'edit-text': '<path d="M13.5 4H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-8"/><path d="M7 9h6M10 9v8M7 17h6"/><path d="m14 13 6.5-6.5a1.5 1.5 0 0 0-2.1-2.1L12 10.8l-.5 3z"/>',
    'clear-page': '<path d="M5 3h10l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M15 3v4h4M7 10h7M7 13h5"/><path d="m9 19 8-8" stroke-width="2.2"/>',
    'delete-page': '<path d="M6 3h9l3 3v5M15 3v3h3M6 3v7"/><path d="M7 12h13M10 12v8a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1v-8M12 9h3M12 15v3M15 15v3"/>',
    'single-page': '<rect x="5" y="2.5" width="14" height="19" rx="1"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    'continuous-pages': '<path d="M5 2.5h14v8H5zM5 13.5h14v8H5z"/><path d="M8 6h8M8 17h8"/>',
    'file-association': '<path d="M4 3h10l4 4v14H4zM14 3v4h4"/><path d="M9.5 15.5a2.5 2.5 0 0 1 0-5h2m1 0h2a2.5 2.5 0 0 1 0 5h-2m-3-2.5h5"/>',
    'book-view': '<path d="M12 5c-2.2-1.6-5.3-1.8-9-1v14c3.7-.8 6.8-.6 9 1 2.2-1.6 5.3-1.8 9-1V4c-3.7-.8-6.8-.6-9 1zM12 5v14"/><path d="M5.5 8h4M14.5 8h4M5.5 11h4M14.5 11h4" stroke-width="1.2"/>',
    'shortcuts': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M5 9h2m3 0h2m3 0h2m-12 4h2m3 0h2m3 0h2M6 16h12"/>',
    'navigation': '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/><circle cx="12" cy="12" r="1" fill="#000" stroke="none"/>',
    'manage-watermarks': '<path d="M5 3h10l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM15 3v4h4"/><path d="m7 11 2 6 3-4 3 4 2-6" stroke-width="1.45"/><path d="M7 18h10" stroke-dasharray="1 2" stroke-width="1"/>',
}
for name, body in shapes.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}</svg>\n'
    ET.fromstring(svg)
    assert '<text' not in svg
    (out / f'{name}.svg').write_text(svg)

small_shapes = {
    'fit-width': '<rect x="6" y="3" width="12" height="18" rx="1"/><path d="M3 12h18m-18 0 3-3m-3 3 3 3m15-3-3-3m3 3-3 3"/>',
    'actual-size': '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M7 10.5 9 9v6m-2 0h4m3-4.5 2-1.5v6m-2 0h4" stroke-width="2"/><circle cx="12.4" cy="10.7" r=".7" fill="#000" stroke="none"/><circle cx="12.4" cy="14" r=".7" fill="#000" stroke="none"/>',
    'delete-page': '<path d="M5 3h10l4 4v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zM15 3v4h4"/><path d="M8 14h8" stroke-width="2.6"/>',
    'manage-watermarks': '<path d="M5 3h10l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM15 3v4h4"/><path d="m6.5 11 2 6 3.5-4 3.5 4 2-6" stroke-width="2.3"/>',
}
for name, body in small_shapes.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>\n'
    ET.fromstring(svg)
    (out / f'{name}-small.svg').write_text(svg)

groups = [
    ('Schaal en zoeken', [
        ('fitWidthIcon', 'Aan breedte aanpassen', 'fit-width', None),
        ('fitPageIcon', 'Volledige pagina', None, 'Icon::Fit'),
        ('actualSizeIcon', 'Ware grootte', 'actual-size', None),
        ('findIcon', 'Zoeken', None, 'Icon::Search'),
    ]),
    ('Tekstbewerking', [
        ('editTextIcon', 'Bestaande tekst bewerken', 'edit-text', None),
        ('textAnnotIcon', 'Tekstannotatie (extensie)', None, 'DomainIcon::DrawingText'),
    ]),
    ('Pagina-inhoud en pagina', [
        ('clearPageIcon', 'Pagina-inhoud wissen', 'clear-page', None),
        ('deletePageIcon', 'Pagina verwijderen', 'delete-page', None),
    ]),
    ('Weergave en associatie', [
        ('singlePageIcon', 'Eén pagina', 'single-page', None),
        ('continuousIcon', 'Doorlopende pagina’s', 'continuous-pages', None),
        ('fileAssocIcon', 'Bestandsassociatie', 'file-association', None),
    ]),
    ('Boek en hulp', [
        ('bookViewIcon', 'Boekweergave', 'book-view', None),
        ('shortcutsIcon', 'Sneltoetsen', 'shortcuts', None),
    ]),
    ('Navigatie en watermerk', [
        ('navigationIcon', 'Navigatie', 'navigation', None),
        ('manageWatermarksIcon', 'Watermerken beheren', 'manage-watermarks', None),
    ]),
]
reuse = {
    'Icon::Fit': 'crates/openaec-ui/assets/icons/fit.svg',
    'Icon::Search': 'crates/openaec-ui/assets/icons/search.svg',
    'DomainIcon::DrawingText': 'crates/openaec-ui/assets/domain-icons/drawing-text.svg',
}
rows = []
for group, items in groups:
    for source_name, label, new_name, existing in items:
        item = records[source_name]
        proposed = f'harmonization/proposals/pdf-ribbon-semantic/{new_name}.svg' if new_name else reuse[existing]
        assert (root / proposed).exists()
        small = f'harmonization/proposals/pdf-ribbon-semantic/{new_name}-small.svg' if new_name in small_shapes else None
        rows.append({'group': group, 'source_name': source_name, 'label': label,
                     'source_svg': 'harmonization/' + item['svg'] if item.get('svg') else None,
                     'built_in_used': bool(item['uses']), 'proposal_svg': proposed,
                     'proposal_small_svg': small,
                     'proposal_kind': 'new-draft' if new_name else 'reuse-existing-crate-icon',
                     'reuse_icon': existing, 'source_uses': item['uses']})
assert len(rows) == 15 and len(shapes) == 12
manifest = {'source_audit': 'harmonization/pdf-ribbon-imported-ui-icons.json',
            'status': 'visual proposal, not approved or installed in the shared crate',
            'grid': '24×24, 1.75px round stroke for new candidates; reused crate assets keep their established geometry',
            'collision_groups': 7, 'semantic_rows': 15, 'new_candidate_svgs': 12,
            'optical_16px_variants': len(small_shapes),
            'reused_crate_icons': 3, 'rows': rows}
(out / 'review.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

cards = []
for row in rows:
    original = row['source_svg'] if row['built_in_used'] else None
    samples = ''
    if original:
        samples += '<div class="sample source">' + ''.join(f'<span><img src="../{original}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32)) + '</div>'
    else:
        samples += '<div class="sample missing">Geen ingebouwde UI-aanroep</div>'
    samples += '<div class="sample proposal">' + ''.join(f'<span><img src="../{row["proposal_small_svg"] if size == 16 and row["proposal_small_svg"] else row["proposal_svg"]}" width="{size}" height="{size}" alt=""><small>{size}</small></span>' for size in (16, 24, 32)) + '</div>'
    cards.append(f'<article data-search="{escape((row["group"]+" "+row["label"]+" "+row["source_name"]).lower())}"><h2>{escape(row["label"])}</h2><small>{escape(row["group"])} · {escape(row["source_name"])}</small><div class="comparison">{samples}</div><p>{escape(row["proposal_kind"])}{(" · " + escape(row["reuse_icon"])) if row["reuse_icon"] else ""}</p></article>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PDF-ribbon · betekenisvolle icoonvarianten</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}header{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1380px)/2))}header a{color:#ffc47e}header h1{font-size:27px;margin:8px 0 4px}header p{max-width:1000px;color:#d6d6dd;margin:0}main{max-width:1420px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}.legend{display:flex;gap:15px;margin:0 0 12px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}article{background:#fff;border:1px solid #d8d8dc;padding:14px}article h2{font-size:14px;margin:0 0 3px}article>small{font-size:10px;color:#6c6c74}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:12px 0}.sample{display:flex;justify-content:space-around;align-items:center;min-height:70px;border:1px solid #d6d6da;background:#fafaf9;color:#303039}.sample span{display:flex;align-items:center;flex-direction:column;gap:3px}.sample small{font-size:9px}.sample.proposal img{filter:brightness(0)}.missing{font-size:11px;color:#777}article p{font-size:11px;color:#6a5541;margin:0}.dark .sample{background:#303039;color:white;border-color:#53535d}.dark .proposal img{filter:brightness(0) invert(1)}.dark article{background:#383840;color:white;border-color:#55555e}.dark article p,.dark article small{color:#ddd}.themes{display:flex;gap:8px;margin-bottom:14px}button{font:inherit;border:1px solid #bbb;background:white;padding:7px 12px;cursor:pointer}button[aria-pressed=true]{background:#303039;color:white;border-color:#303039}.native{margin-top:25px;background:white;border:1px solid #d8d8dc;padding:16px}.native img{display:block;max-width:100%;height:auto;margin:10px 0;border:1px solid #d8d8dc}@media(max-width:700px){main{padding:10px}.grid{grid-template-columns:1fr}}
</style><header><a href="pdf-ribbon-imported-icon-review.html">← Ribbonbroniconen</a><h1>PDF-ribbon · onderscheid per betekenis</h1><p>Ontwerpvergelijking voor zeven groepen waarin de bron dezelfde vorm voor verschillende opdrachten gebruikt. Twaalf nieuwe path-SVG’s, vier compacte 16px-optische varianten en drie bestaande Rust-iconen vormen een voorstel, nog geen crate-migratie.</p></header><main><div class="note"><strong>Beoordelingskader.</strong> Links staat de bestaande bronvorm, rechts het semantische voorstel. Controleer herkenning, onderlinge afstand en leesbaarheid op 16, 24 en 32 px. Tekstannotatie heeft in de ingebouwde ribbon geen aanroep; de bronexport blijft wel via extensies aanspreekbaar. De native contactbladen hieronder toetsen de voorstellen in de echte Iced-renderer.</div><div class="themes"><button id="light" aria-pressed="true">Light</button><button id="dark" aria-pressed="false">Forge</button></div><div class="legend"><span>Links: bestaande bron</span><span>Rechts: voorstel / hergebruik</span></div><div id="cards" class="grid">''' + ''.join(cards) + '''</div><section class="native"><h2>Native Rust-vergelijking</h2><p>Per betekenis: bron op 24 px, voorstel op 16/24/32 px. De vier compacte 16px-versies hebben eigen geometrie. Dit is visuele beoordeling; de voorgestelde SVG’s zijn nog niet in de publieke crate opgenomen.</p><img src="pdf-ribbon-semantic-light.png" alt="PDF-ribbon semantische voorstellen in Light"><img src="pdf-ribbon-semantic-forge.png" alt="PDF-ribbon semantische voorstellen in Forge"></section></main><script>const cards=document.querySelector('#cards');for(const [id,dark] of [['light',false],['dark',true]])document.querySelector('#'+id).onclick=()=>{cards.classList.toggle('dark',dark);document.querySelector('#light').setAttribute('aria-pressed',String(!dark));document.querySelector('#dark').setAttribute('aria-pressed',String(dark))};</script></html>'''
(root / 'design/pdf-ribbon-semantic-review.html').write_text(page)
print('PDF ribbon semantic review: 15 meanings, 12 new proposals, 3 existing crate icons')
