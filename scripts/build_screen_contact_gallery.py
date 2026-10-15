#!/usr/bin/env python3
"""Build a navigable page for all pinned screen contact sheets."""
from collections import defaultdict
from html import escape as e
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design'
manifest = json.loads((DESIGN / 'screen-contact-sheets/manifest.json').read_text())
records = {(item['repository'], item['path']): item for item in manifest['screens']}
groups = defaultdict(list)
for sheet in manifest['sheets']:
    groups[sheet['kind']].append(sheet)

labels = {
    'application-screen': 'Applicatieschermen',
    'documentation-image': 'Handleidingbeelden',
    'design-mockup': 'Ontwerpmockups',
    'tutorial-capture': 'Tutorialuitsneden',
    'website-reference': 'Websitebeelden',
    'catalog-preview': 'Cataloguspreviews',
    'social-preview': 'Social previews',
    'sample-preview': 'Voorbeeldbestanden',
}
sections = []
for kind, sheets in sorted(groups.items(), key=lambda entry: entry[0] != 'application-screen'):
    cards = []
    for sheet in sheets:
        entries = []
        for number, path in enumerate(sheet['paths'], (sheet['page'] - 1) * 20 + 1):
            record = records[(sheet['repository'], path)]
            dims = record.get('dimensions', [])
            dims_text = f'{dims[0]} × {dims[1]}' if len(dims) == 2 else 'onbekend'
            entries.append(f'<li><span>{number:03d}</span><a href="{e(record["url"], quote=True)}" target="_blank" rel="noopener">{e(path)}</a><small>{e(dims_text)} px</small></li>')
        file = f'screen-contact-sheets/{sheet["file"]}'
        image_word = 'beeld' if sheet['count'] == 1 else 'beelden'
        cards.append(f'<article class="sheet"><div class="sheet-head"><strong>{e(sheet["repository"])}</strong><span>Blad {sheet["page"]} · {sheet["count"]} {image_word}</span></div><a class="sheet-image" href="{e(file, quote=True)}" target="_blank"><img loading="lazy" src="{e(file, quote=True)}" alt="Contactblad {e(sheet["repository"])} {sheet["page"]}"></a><details><summary>Bronbestanden en afmetingen</summary><ol>{"".join(entries)}</ol></details></article>')
    count = sum(s['count'] for s in sheets)
    sections.append(f'<section id="{e(kind)}"><div class="section-head"><h2>{labels[kind]}</h2><span>{count} {"beeld" if count == 1 else "beelden"} · {len(sheets)} {"blad" if len(sheets) == 1 else "bladen"}</span></div><div class="sheets">{"".join(cards)}</div></section>')

nav = ''.join(f'<a href="#{e(kind)}">{labels[kind]} <span>{sum(s["count"] for s in sheets)}</span></a>' for kind, sheets in sorted(groups.items(), key=lambda entry: entry[0] != 'application-screen'))
css = '''*{box-sizing:border-box}body{margin:0;background:#15191e;color:#e8ecf1;font:14px/1.5 Inter,system-ui,sans-serif}a{color:#9cc8ff}main{max-width:1440px;margin:auto;padding:38px 25px 100px}header>small{color:#9baab9;text-transform:uppercase;letter-spacing:.14em;font-weight:750}h1{font-size:38px;letter-spacing:-.035em;line-height:1.1;margin:9px 0 15px}header p{max-width:850px;color:#aeb9c4;font-size:15px}.stats{display:flex;gap:9px;flex-wrap:wrap;margin:22px 0 27px}.stats span{border:1px solid #39434e;background:#222830;border-radius:5px;padding:9px 13px;color:#cbd5df}.stats strong{color:white;font-size:17px;margin-right:5px}.nav{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0 35px}.nav a{text-decoration:none;color:#d5dee7;background:#28313a;border:1px solid #40505e;border-radius:5px;padding:7px 10px;font-size:12px}.nav a span{color:#91acc5;margin-left:4px}section{margin:35px 0}.section-head{display:flex;align-items:baseline;gap:15px;border-bottom:1px solid #39434e;margin-bottom:16px}.section-head h2{font-size:22px;letter-spacing:-.02em;margin:0 0 10px}.section-head span{color:#98a6b3;font-size:12px}.sheets{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start}.sheet{border:1px solid #3a444f;background:#20262d;border-radius:8px;overflow:hidden;min-width:0}.sheet-head{display:flex;justify-content:space-between;gap:10px;padding:10px 14px;font-size:13px}.sheet-head span{color:#96a6b5;font-size:11px}.sheet-image{display:block;background:#f0f2f4}.sheet img{display:block;width:100%;height:auto}.sheet details{padding:0 14px}.sheet summary{cursor:pointer;color:#adbed0;font-size:12px;padding:10px 0}.sheet ol{list-style:none;margin:0 0 12px;padding:0;border-top:1px solid #39434e}.sheet li{display:grid;grid-template-columns:35px minmax(0,1fr) 90px;gap:8px;border-bottom:1px solid #303943;padding:5px 0;font-size:11px}.sheet li span,.sheet li small{color:#8294a5}.sheet li a{overflow-wrap:anywhere;text-decoration:none}.sheet li small{text-align:right}footer{padding-top:25px;color:#a1adba}@media(max-width:850px){.sheets{grid-template-columns:1fr}main{padding:23px 15px}h1{font-size:29px}.section-head{display:block}}'''
html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · Schermcontactbladen</title><style>{css}</style></head><body><main><header><small>OpenAEC / ontwerpbeoordeling / bronbeelden</small><h1>Alle gevonden schermbeelden naast elkaar</h1><p>666 screenshotkandidaten zijn rechtstreeks uit hun vastgelegde Git-commit gerenderd, verdeeld over 47 contactbladen. De 472 beelden onder ‘Applicatieschermen’ bevatten ook historische states en uitsneden; een contactblad bewijst op zichzelf niet dat het scherm in de huidige build bestaat. Open een blad voor een grotere weergave of een bronbestand onder het blad voor de exacte afbeelding.</p><div class="stats"><span><strong>666</strong> gelezen afbeeldingen</span><span><strong>47</strong> contactbladen</span><span><strong>0</strong> leesfouten</span><span><strong>472</strong> kandidaat-appschermen</span></div><nav class="nav" aria-label="Schermsoorten">{nav}</nav></header>{''.join(sections)}<footer><a href="screen-inventory.html">Alle bronmetadata en filters ↗</a> · <a href="review.html">Terug naar ontwerpreview ↗</a></footer></main></body></html>'''
(DESIGN / 'screen-contact-sheets.html').write_text(html)
print(f'Built contact gallery with {len(manifest["sheets"])} sheets and {manifest["total"]} source links')
