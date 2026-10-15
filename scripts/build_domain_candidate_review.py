"""Build a visual, evidence-linked review of FEM/BIM filename matches."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
ASSETS = {
    (record["repo"], record["path"]): record
    for record in json.loads((ROOT / "harmonization/asset-index.json").read_text())
}
REPOS = {record["name"]: record for record in json.loads((ROOT / "harmonization/inventory.json").read_text())}
PROPOSALS = json.loads((DESIGN / "domain-icon-proposals.json").read_text())
MATCHES = [proposal for proposal in PROPOSALS if proposal["candidate_assets"]]
ASSESSMENTS = {
    (record["proposal"], record["repo"], record["path"]): record
    for record in json.loads((DESIGN / "domain-candidate-assessment.json").read_text())
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def candidate(proposal_id: str, item: dict[str, str]) -> str:
    record = ASSETS[(item["repo"], item["path"])]
    if record["category"] != "ui-used":
        raise ValueError(f"Candidate lacks UI-use evidence: {item}")
    path = f'{item["repo"]}/{item["path"]}'
    image = "../harmonization/ui-icons/" + quote(path, safe="/")
    source = record["url"]
    first_use = record["ui_references"][0]
    use = f'{item["repo"]}/{first_use["source"]}'
    repo = REPOS[item["repo"]]
    use_url = f'{repo["url"].rstrip("/")}/blob/{repo["commit"]}/{quote(first_use["source"])}'
    if first_use["line"]:
        use_url += f'#L{first_use["line"]}'
    key = f"{proposal_id}|{path}"
    assessment = ASSESSMENTS[(proposal_id, item["repo"], item["path"])]
    names = {"same": "Dezelfde betekenis", "related": "Verwant commando", "different": "Naamtoeval"}
    return (
        f'<article class="candidate" data-key="{esc(key)}" data-search="{esc(path.lower())}">'
        f'<div class="swatches"><div class="swatch light"><img src="{esc(image)}" alt=""></div>'
        f'<div class="swatch dark"><img src="{esc(image)}" alt=""></div></div>'
        f'<div class="candidate-body"><strong>{esc(Path(path).stem)}</strong>'
        f'<small>{esc(path)}</small><div class="links">'
        f'<a href="{esc(source)}" target="_blank" rel="noopener">Origineel ↗</a>'
        f'<a href="{esc(use_url)}" target="_blank" rel="noopener">UI-gebruik ↗</a>'
        f'</div><small class="evidence">{esc(use)}</small>'
        f'<div class="judgment"><b class="{esc(assessment["semantic_assessment"])}">{names[assessment["semantic_assessment"]]}</b>'
        f'<span>{esc(assessment["rationale"])}</span></div></div>'
        f'<select aria-label="Beoordeling {esc(key)}"><option value="">Te beoordelen</option>'
        f'<option value="same">Dezelfde betekenis</option><option value="related">Verwant, ander commando</option>'
        f'<option value="different">Naamtoeval</option><option value="unclear">Onzeker</option></select>'
        f'</article>'
    )


assert len(ASSESSMENTS) == sum(len(proposal["candidate_assets"]) for proposal in MATCHES)
cards = []
for proposal in MATCHES:
    draft = f'icon-drafts/{proposal["domain"]}/{proposal["id"].split(".", 1)[1]}.svg'
    candidates = "".join(candidate(proposal["id"], item) for item in proposal["candidate_assets"])
    search = " ".join([proposal["id"], proposal["label"], proposal["visual_metaphor"]]).lower()
    cards.append(
        f'<section class="proposal" data-domain="{esc(proposal["domain"])}" data-search="{esc(search)}">'
        f'<header class="proposal-head"><div class="draft"><img src="{esc(draft)}" alt="Ontwerpvoorstel {esc(proposal["label"])}"></div>'
        f'<div><span class="eyebrow">{esc(proposal["domain"].upper())} · {esc(proposal["group"])} · {len(proposal["candidate_assets"])} {"bronkandidaat" if len(proposal["candidate_assets"]) == 1 else "bronkandidaten"}</span>'
        f'<h2>{esc(proposal["label"])} <code>{esc(proposal["id"])}</code></h2>'
        f'<p>{esc(proposal["visual_metaphor"])}</p></div></header>'
        f'<div class="candidates">{candidates}</div></section>'
    )

page = r'''<!doctype html>
<html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · FEM/BIM bronkandidaten</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f4f4f2;color:#303037;font:13px/1.45 Inter,system-ui,sans-serif}
header.top{background:#303039;color:white;padding:26px max(20px,calc((100vw - 1300px)/2));border-bottom:3px solid #d97706}
header.top a{color:#f3b861}h1{font-size:27px;font-weight:600;margin:8px 0}header.top p{max-width:900px;color:#d7d7db;margin:0}
main{max-width:1340px;margin:auto;padding:20px}.summary{display:flex;gap:8px;flex-wrap:wrap;align-items:center;background:white;border:1px solid #dedee2;padding:10px 14px;position:sticky;top:0;z-index:2}
button,input,select{font:inherit}button{border:1px solid #c9c9cf;background:#fff;padding:7px 12px;border-radius:3px;cursor:pointer}button.active{background:#d97706;border-color:#d97706;color:white}input{border:1px solid #c9c9cf;border-radius:3px;padding:7px 10px;min-width:220px}.summary output{margin-left:auto;color:#71717a}
.note{background:#fff6e8;border-left:3px solid #d97706;padding:12px 16px;margin:18px 0;max-width:950px}.proposal{margin:22px 0;border:1px solid #dedee2;background:white}.proposal[hidden],.candidate[hidden]{display:none!important}
.proposal-head{display:flex;gap:18px;align-items:center;padding:16px 18px;background:#fafaf9;border-bottom:1px solid #e5e5e8}.draft{width:64px;height:64px;flex:none;display:grid;place-items:center;border:1px solid #e2e2e5;background:white}.draft img{width:32px;height:32px}.eyebrow{font-size:10px;letter-spacing:.1em;color:#a15c05;font-weight:600}h2{font-size:17px;margin:4px 0}h2 code{font-size:11px;color:#797981;font-weight:400;margin-left:8px}.proposal-head p{margin:0;color:#696971}
.candidates{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:1px;background:#e5e5e8}.candidate{background:white;min-width:0;display:flex;align-items:flex-start;gap:11px;padding:12px}.swatches{display:flex;gap:4px;flex:none}.swatch{width:42px;height:42px;display:grid;place-items:center;border:1px solid #ddd}.swatch img{width:28px;height:28px}.swatch.light{background:#fafaf9}.swatch.dark{background:#303039}.candidate-body{min-width:0;flex:1}.candidate-body strong{font-size:12px}.candidate-body small{display:block;color:#777;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.links{display:flex;gap:12px}.links a{color:#9a5708;font-size:11px}.candidate select{max-width:110px;min-width:0;font-size:11px;padding:5px 2px;border:1px solid #d5d5d9;background:#fff}
.judgment{display:flex;gap:6px;align-items:baseline;flex-wrap:wrap;font-size:11px;margin-top:4px}.judgment b{white-space:nowrap;font-size:10px;padding:1px 5px;border-radius:2px}.judgment .same{background:#e4f4e8;color:#176c39}.judgment .related{background:#fff0da;color:#8a5708}.judgment .different{background:#f2e9ed;color:#90425e}.judgment span{color:#62626a}
body.dark{background:#222228;color:#f1f1f2}body.dark .summary,body.dark .proposal,body.dark .candidate{background:#34343c;color:#f1f1f2;border-color:#55555c}body.dark .proposal-head{background:#3e3e47;border-color:#55555c}body.dark .draft{background:#fafaf9}body.dark .candidates{background:#55555c}body.dark .note{background:#42392c}body.dark .candidate select{background:#3e3e47;color:white;border-color:#666}body.dark .proposal-head p,body.dark .candidate-body small{color:#c3c3c9}
body.dark .judgment span{color:#d0d0d3}
@media(max-width:750px){.candidate{flex-wrap:wrap}.candidate select{max-width:none;flex:1}.summary output{margin-left:0;width:100%}}
</style>
<header class="top"><a href="review.html">← Hoofdreview</a> · <a href="domain-icon-atlas.html">Alle 109 concepten</a><h1>FEM/BIM: bronkandidaten toetsen</h1><p>24 ontwerpbetekenissen hebben samen 54 naamkandidaten met een UI-broncodeverwijzing. De eerste broncontextbeoordeling onderscheidt 11 gelijke betekenissen, 28 verwante commando’s en 15 naamtoevallen. Vergelijk ook de vorm voordat een bestaand symbool in de gedeelde Rust-set komt.</p></header>
<main><div class="summary"><button class="active" data-filter="all">Alle 24</button><button data-filter="fem">FEM 6</button><button data-filter="bim">BIM 18</button><button id="theme">Donker</button><input id="search" placeholder="Zoek betekenis of bron" aria-label="Zoeken"><button id="export">Exporteer beoordeling</button><output id="count"></output></div>
<div class="note"><strong>Bewijsgrens</strong> · Iedere bronkandidaat heeft een direct UI-codepad; een iconregistry bewijst niet dat iedere variant in een huidig scherm zichtbaar is. De gekleurde labels zijn een voorlopige beoordeling op basis van bestandsnaam en broncontext. Ook “dezelfde betekenis” is geen hergebruikbesluit. De keuzen rechts zijn voor een afzonderlijke visuele beoordeling en worden lokaal in deze browser bewaard.</div>
<!--CARDS-->
</main><script>
const key='openaec-domain-candidate-review-v1';let saved={};try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch{}
document.querySelectorAll('.candidate').forEach(card=>{const select=card.querySelector('select');select.value=saved[card.dataset.key]||'';select.onchange=()=>{if(select.value)saved[card.dataset.key]=select.value;else delete saved[card.dataset.key];localStorage.setItem(key,JSON.stringify(saved));refresh()}});
let domain='all';function refresh(){const q=document.querySelector('#search').value.toLocaleLowerCase();let shown=0,choices=0;document.querySelectorAll('.proposal').forEach(section=>{const match=domain==='all'||section.dataset.domain===domain;const own=section.dataset.search.includes(q);let children=0;section.querySelectorAll('.candidate').forEach(card=>{const visible=match&&(!q||own||card.dataset.search.includes(q));card.hidden=!visible;if(visible){children++;if(card.querySelector('select').value)choices++}});section.hidden=children===0;if(children)shown++});document.querySelector('#count').textContent=shown+' '+(shown===1?'betekenis':'betekenissen')+' · '+choices+' beoordeeld'}
document.querySelectorAll('[data-filter]').forEach(button=>button.onclick=()=>{domain=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('active',x===button));refresh()});document.querySelector('#search').oninput=refresh;document.querySelector('#theme').onclick=()=>{document.body.classList.toggle('dark');document.querySelector('#theme').textContent=document.body.classList.contains('dark')?'Licht':'Donker'};
document.querySelector('#export').onclick=()=>{const blob=new Blob([JSON.stringify({schema:1,decisions:saved},null,2)],{type:'application/json'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='openaec-domain-candidate-review.json';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),5000)};refresh();
</script></html>'''
(DESIGN / "domain-candidate-review.html").write_text(page.replace("<!--CARDS-->", "\n".join(cards)))
print(f"Built {len(MATCHES)} meaning cards with {sum(len(p['candidate_assets']) for p in MATCHES)} UI-used candidates")
