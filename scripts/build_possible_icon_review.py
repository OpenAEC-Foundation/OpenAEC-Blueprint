#!/usr/bin/env python3
"""Render unverified icon-like assets separately from source-proven UI icons."""
from collections import Counter
from html import escape
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "design"
H = ROOT / "harmonization"
assets = [a for a in json.loads((H / "asset-index.json").read_text())
          if a["category"] == "possible-ui-icon"]
assert len(assets) == 53
counts = Counter(a["repo"] for a in assets)
notes = {
    "OpenCADStudio": "Archief-icoon zonder directe verwijzing in de gescande UI-bron; zichtbaarheid niet bewezen.",
    "open-pdf-studio": "Meegeleverd met PDF.js; geen directe bestandsverwijzing in viewer.html, viewer.css of viewer.mjs. Dynamisch laden blijft mogelijk.",
    "open-pointcloud-studio": "Bronbestand in de native iconmap; in de gepinde UI-code geen directe bestandsverwijzing gevonden.",
    "open-geotechniek-studio": "Bestandstype-illustratie in public/file-icons; geen directe bestandsverwijzing in de gescande UI-code.",
}
cards = []
for asset in sorted(assets, key=lambda a: (a["repo"].lower(), a["path"].lower())):
    path = Path(asset["repo"]) / asset["path"]
    preview = "../harmonization/possible-icons/" + quote(path.as_posix())
    assert (H / "possible-icons" / path).is_file(), path
    source = asset["url"]
    repo = asset["repo"]
    cards.append(
        f'<article data-repo="{escape(repo, quote=True)}" data-search="{escape((repo + " " + asset["path"]).lower(), quote=True)}">'
        f'<header><b>{escape(path.stem)}</b><small>{escape(repo)}</small></header>'
        '<div class="samples">'
        + ''.join(f'<span class="sample"><img src="{preview}" width="{size}" height="{size}" alt="">{size} px</span>' for size in (16, 24, 32))
        + f'<span class="sample dark"><img src="{preview}" width="24" height="24" alt="">donker</span></div>'
        f'<p>{escape(notes[repo])}</p><a href="{escape(source, quote=True)}">Bronbestand ↗</a>'
        f'<code>{escape(asset["path"])}</code></article>'
    )
options = ''.join(f'<option value="{escape(repo, quote=True)}">{escape(repo)} · {n}</option>'
                  for repo, n in sorted(counts.items()))
page = f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · onzekere iconassets</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f4f5;color:#303039;font:13px/1.45 Inter,system-ui,sans-serif}}.top{{background:#303039;color:white;padding:24px max(22px,calc((100vw - 1350px)/2));border-bottom:3px solid #d97706}}.top a{{color:#ffc278}}h1{{font-size:28px;margin:6px 0}}.top p{{color:#dddde2;margin:0;max-width:950px}}main{{max-width:1390px;margin:auto;padding:22px}}.note{{background:white;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:18px}}.filters{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:15px}}input,select{{font:inherit;border:1px solid #bebec5;background:white;padding:8px}}input{{min-width:280px}}.filters output{{margin-left:auto}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:10px}}article{{background:white;border:1px solid #d8d8de;padding:11px;min-width:0}}article[hidden]{{display:none}}article header{{display:flex;justify-content:space-between;gap:8px}}article b{{overflow-wrap:anywhere}}article small{{color:#797983}}.samples{{display:flex;gap:4px;margin:9px 0}}.sample{{width:54px;height:60px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;background:#f3f4f6;font-size:10px}}.sample.dark{{background:#303039;color:white}}article p{{color:#5d5d66;min-height:52px;margin:8px 0}}article a{{color:#a85000}}article code{{display:block;color:#7b7b83;font-size:10px;overflow-wrap:anywhere;margin-top:8px}}
</style><div class="top"><a href="review.html">← Hoofdreview</a><h1>53 onzekere iconassets</h1><p>Deze bestanden lijken door hun pad of vorm op iconen, maar de gepinde codeaudit bewijst geen direct gebruik in de UI. Ze zijn apart van de 577 bewezen bestanden beschikbaar voor visuele en runtimebeoordeling.</p></div><main><div class="note"><strong>Bewijsgrens.</strong> Een bestand in <code>assets/icons</code> of een meegeleverde PDF.js-beeldmap is niet automatisch een gebruikte knop. De lichte en donkere proef toont de originele SVG zonder thematische correctie. De OpenCADStudio-referentie is extern aan de OpenAEC-organisatie. <a href="icon-review-board.html">Open de bewezen UI-iconenreview</a>.</div><div class="filters"><input id="search" type="search" placeholder="Zoek naam of pad" aria-label="Zoek kandidaten"><select id="repo" aria-label="Filter repository"><option value="">Alle repositories</option>{options}</select><output id="count"></output></div><div class="grid">{''.join(cards)}</div></main><script>const cards=[...document.querySelectorAll('article')];const search=document.querySelector('#search');const repo=document.querySelector('#repo');function update(){{const q=search.value.toLowerCase();let visible=0;for(const card of cards){{card.hidden=!(card.dataset.search.includes(q)&&(!repo.value||card.dataset.repo===repo.value));visible+=!card.hidden}}document.querySelector('#count').textContent=visible+' / '+cards.length}}search.oninput=update;repo.onchange=update;update();</script></html>'''
(D / "possible-icon-review.html").write_text(page)
print("Built review for", len(assets), "unverified icon-like assets", dict(counts))
