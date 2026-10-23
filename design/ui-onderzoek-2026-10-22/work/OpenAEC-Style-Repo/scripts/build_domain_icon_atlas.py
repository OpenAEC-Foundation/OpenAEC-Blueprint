#!/usr/bin/env python3
"""Build a self-contained review page for the proposed FEM/BIM vector icons."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
drafts = json.loads((DESIGN / "domain-icon-drafts.json").read_text())
proposals = {p["id"]: p for p in json.loads((DESIGN / "domain-icon-proposals.json").read_text())}

cards = []
for draft in drafts:
    proposal = proposals[draft["id"]]
    candidate_count = len(proposal["candidate_assets"])
    candidate_text = " · ".join(
        f'{asset["repo"]}: {asset["path"]}' for asset in proposal["candidate_assets"]
    )
    img = html.escape(draft["file"], quote=True)
    small_img = html.escape(draft.get("small_file", draft["file"]), quote=True)
    cards.append(
        f'<article class="card" data-domain="{draft["domain"]}" '
        f'data-group="{html.escape(draft["group"], quote=True)}" '
        f'data-search="{html.escape(" ".join([draft["id"], draft["label"], draft["group"], draft["visual_metaphor"], candidate_text]).lower(), quote=True)}">'
        f'<div class="iconrow"><span class="sample small"><img src="{small_img}" alt=""></span>'
        f'<span class="sample medium"><img src="{img}" alt=""></span>'
        f'<span class="sample large"><img src="{img}" alt=""></span></div>'
        f'<div class="identity"><strong>{html.escape(draft["label"])}</strong>'
        f'<code>{html.escape(draft["id"])}</code></div>'
        f'<p>{html.escape(draft["visual_metaphor"])}</p>'
        f'<div class="meta">{html.escape(draft["group"])}'
        + (f'<span class="match" title="{html.escape(candidate_text, quote=True)}">{candidate_count} {"bronkandidaat" if candidate_count == 1 else "bronkandidaten"}</span>' if candidate_count else '<span>nieuw voorstel</span>')
        + '</div></article>'
    )

page = '''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · FEM/BIM iconconcepten</title>
<style>
@font-face{font-family:Inter;src:url("../assets/fonts/Inter-Regular.ttf");font-weight:400}@font-face{font-family:Inter;src:url("../assets/fonts/Inter-SemiBold.ttf");font-weight:600 900}
*{box-sizing:border-box}body{margin:0;background:#f2f3f5;color:#36363e;font:13px/1.4 Inter,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:13px 24px;background:#272b32;color:#fff;border-bottom:3px solid #d97706}
header strong{font-size:15px;letter-spacing:.02em;margin-right:16px}header .count{color:#cbd0d6;margin-left:auto}
button,input{font:inherit}button{background:#3a414b;color:#fff;border:1px solid #626a75;border-radius:4px;padding:7px 12px;cursor:pointer}button.active{background:#d97706;border-color:#d97706;color:#fff}input{width:220px;padding:7px 9px;border:1px solid #8e949d;border-radius:4px}
main{max-width:1600px;margin:auto;padding:22px 24px 50px}.intro{background:#fff;border:1px solid #d9dce0;border-left:4px solid #d97706;padding:13px 17px;margin-bottom:22px}.intro p{margin:4px 0;color:#61656d}
.section{margin:26px 0 13px;display:flex;align-items:baseline;gap:10px}.section h2{font-size:18px;margin:0}.section span{color:#777}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:10px}.card{background:#fff;border:1px solid #d9dce0;border-radius:5px;min-height:180px;padding:12px;display:flex;flex-direction:column}.card:hover{border-color:#d97706;box-shadow:0 2px 10px #292d3412}
.iconrow{height:65px;display:flex;align-items:center;gap:16px;border-bottom:1px solid #eceef0;padding-bottom:11px}.sample{width:48px;height:46px;display:grid;place-items:center;background:#f5f6f7;border:1px solid #e8eaec;border-radius:4px}.small img{width:16px;height:16px}.medium img{width:24px;height:24px}.large img{width:32px;height:32px}
.identity{display:flex;justify-content:space-between;gap:8px;align-items:baseline;margin-top:10px}.identity strong{font-size:13px}.identity code{font-size:10px;color:#7b8089}.card p{margin:5px 0 13px;font-size:11px;color:#61656d}.meta{display:flex;justify-content:space-between;gap:6px;margin-top:auto;font-size:10px;color:#747981}.match{color:#97530a;text-decoration:underline dotted;cursor:help}
body.dark{background:#20252c;color:#e2e5e8}body.dark .intro,body.dark .card{background:#30363e;border-color:#535a63}body.dark .intro p,body.dark .card p,body.dark .meta,body.dark .identity code{color:#b8bec6}body.dark .sample{background:#242a31;border-color:#58616b}body.dark .sample img{filter:invert(1)}body.dark .iconrow{border-color:#4b535d}body.dark .match{color:#e9a75f}
.hidden{display:none!important}@media(max-width:600px){header{padding:12px}header .count{width:100%;margin-left:0}main{padding:12px}.grid{grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}}
</style></head><body><header><strong>OPENAEC · FEM/BIM ICONCONCEPTEN</strong><button class="active" data-filter="all">Alle 109</button><button data-filter="fem">FEM 52</button><button data-filter="bim">BIM 57</button><button id="theme">Donkere omgeving</button><input id="search" placeholder="Zoek betekenis of bron…" aria-label="Zoek iconen"><span class="count" id="count"></span></header>
<main><div class="intro"><b>Visuele ontwerpronde · 24 × 24 grid · 1,75 px lijn</b><p>Iedere kaart toont het icoon op 16, 24 en 32 px. SMALL_COUNT betekenissen hebben een aparte vereenvoudigde 16 px-variant. Dit zijn 109 unieke vectorconcepten, nog geen goedgekeurde definitieve set. Een bronkandidaat betekent alleen een naamovereenkomst; de betekenis moet visueel worden beoordeeld.</p></div><div id="sections"></div></main>
<script>const cards=Array.from(document.querySelectorAll('.card'));let domain='all';function update(){const q=document.getElementById('search').value.trim().toLowerCase();let shown=0;for(const c of cards){const ok=(domain==='all'||c.dataset.domain===domain)&&c.dataset.search.includes(q);c.classList.toggle('hidden',!ok);shown+=ok}for(const section of document.querySelectorAll('.section-wrap'))section.classList.toggle('hidden',!section.querySelector('.card:not(.hidden)'));document.getElementById('count').textContent=shown+' concepten zichtbaar'}document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{domain=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('active',x===b));update()});document.getElementById('search').oninput=update;document.getElementById('theme').onclick=()=>{document.body.classList.toggle('dark');document.getElementById('theme').textContent=document.body.classList.contains('dark')?'Lichte omgeving':'Donkere omgeving'};
</script></body></html>'''

from collections import defaultdict
grouped = defaultdict(list)
for draft, card in zip(drafts, cards):
    grouped[(draft["domain"], draft["group"])].append(card)
sections = []
for (domain, group), group_cards in grouped.items():
    sections.append(
        f'<section class="section-wrap"><div class="section"><h2>{domain.upper()} · {html.escape(group)}</h2><span>{len(group_cards)} iconen</span></div>'
        f'<div class="grid">{"".join(group_cards)}</div></section>'
    )
page = page.replace('SMALL_COUNT', str(sum('small_file' in draft for draft in drafts)))
page = page.replace('<div id="sections"></div>', f'<div id="sections">{"".join(sections)}</div>')
(DESIGN / "domain-icon-atlas.html").write_text(page)
print(f"Built atlas with {len(cards)} icons in {len(grouped)} groups")
