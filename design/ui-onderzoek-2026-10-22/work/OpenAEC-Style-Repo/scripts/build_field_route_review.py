"""Build a source-pinned screen review for Open Field Studio's ten routes."""
from __future__ import annotations

import json
import re
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "Open-Field-Studio"
meta = json.loads((ROOT / "harmonization/repositories" / f"{REPO}.json").read_text())
layout = next(item for item in json.loads((ROOT / "design/app-layouts.json").read_text()) if item["id"] == "field")
checkout = Path("/tmp/openaec-inventory") / REPO
commit = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
assert commit == meta["commit"]
source = subprocess.check_output(["git", "-C", str(checkout), "show", "HEAD:index.html"], text=True)
screenshots = {
    "project": "01-project.png",
    "koppelingen": "02-koppelingen.png",
    "inspectie": "03-inspectie.png",
    "oplevering": "04-oplevering.png",
    "dashboard": "05-dashboard.png",
    "export": "06-export.png",
}
routes = []
for i, match in enumerate(re.finditer(r'<button class="nav-btn[^>]*data-tab="([^"]+)"[^>]*>', source)):
    route = match.group(1)
    section = re.search(r'<section id="' + re.escape(route) + r'-tab"[^>]*>', source)
    assert section, route
    screenshot = screenshots.get(route)
    if screenshot:
        screenshot_path = ROOT / "harmonization/references" / REPO / "docs/screenshots" / screenshot
        assert screenshot_path.is_file(), screenshot_path
    routes.append({
        "id": route,
        "label": layout["tabs"][i],
        "nav_line": source.count("\n", 0, match.start()) + 1,
        "section_line": source.count("\n", 0, section.start()) + 1,
        "screenshot": screenshot,
        "evidence": "repository-screenshot" if screenshot else "source-only",
    })

assert [item["id"] for item in routes] == layout["screens"]
assert len(routes) == 10 and sum(bool(item["screenshot"]) for item in routes) == 6
payload = {"repository": REPO, "commit": commit, "routes": routes}
(ROOT / "design/field-route-review.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

cards = []
for route in routes:
    label = escape(route["label"])
    nav_url = f'{meta["url"]}/blob/{commit}/index.html#L{route["nav_line"]}'
    section_url = f'{meta["url"]}/blob/{commit}/index.html#L{route["section_line"]}'
    if route["screenshot"]:
        path = f'../harmonization/references/{REPO}/docs/screenshots/{route["screenshot"]}'
        visual = f'<a href="{path}"><img src="{path}" alt="Bronbeeld van {label}" loading="lazy"></a>'
        status = '<span class="badge captured">Bronbeeld aanwezig</span>'
    else:
        visual = '<div class="missing"><strong>Geen repositoryscreenshot</strong><span>Schermstructuur in UI-code aanwezig</span></div>'
        status = '<span class="badge code">Alleen codebewijs</span>'
    cards.append(f'''<article class="card">
      <div class="visual">{visual}</div><div class="details"><small>{len(cards)+1:02d} · {escape(route["id"])}</small>
      <h2>{label}</h2>{status}<p><a href="{nav_url}">Navigatie · regel {route["nav_line"]} ↗</a><br>
      <a href="{section_url}">Schermsectie · regel {route["section_line"]} ↗</a></p></div></article>''')

html = '''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Open Field Studio · schermroute-review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f6f7;color:#292e36;font:14px/1.5 Inter,"Segoe UI",Arial,sans-serif}
header{background:#292d35;color:white;border-bottom:4px solid #d97706;padding:28px max(24px,calc((100vw - 1360px)/2))}
header small{color:#efba6e;letter-spacing:.14em;font-size:11px;font-weight:700}h1{font-size:32px;letter-spacing:-.025em;margin:7px 0}header p{max-width:800px;color:#d3d5d9}
main{max-width:1408px;margin:auto;padding:24px}.note{border-left:3px solid #d97706;background:#fff6e9;padding:13px 16px;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}.card{background:white;border:1px solid #dde0e4;border-radius:7px;overflow:hidden;min-width:0}
.visual{aspect-ratio:16/9;background:#e9ebee;display:grid;place-items:center;overflow:hidden}.visual a{width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.visual img{width:100%;height:100%;object-fit:contain}.missing{text-align:center;color:#55606e;display:grid;gap:4px}.missing span{font-size:12px}
.details{padding:15px}.details small{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#66707b}.details h2{margin:4px 0 10px;font-size:19px}.badge{display:inline-block;border-radius:4px;padding:3px 7px;font-size:11px;font-weight:650}.captured{background:#e5f3e9;color:#23693d}.code{background:#fff0dc;color:#90590a}
.details p{margin:12px 0 0;font-size:12px;line-height:1.8}a{color:#92500b}footer{border-top:1px solid #d9dde1;margin-top:24px;padding:18px 0;font-size:12px;color:#64707c}
@media(max-width:600px){header{padding:22px 16px}main{padding:16px}.grid{grid-template-columns:1fr}}
</style></head><body><header><small>OPENAEC · SCHERMONDERZOEK</small><h1>Open Field Studio · 10 schermroutes</h1>
<p>Alle navigatieknoppen en doelgebieden zijn gecontroleerd in dezelfde vastgelegde UI-bron. Zes routes hebben een bestaand repositoryscreenshot; vier hebben alleen codebewijs.</p></header>
<main><div class="note">De bronbeelden kunnen een andere data- of thematoestand tonen. Een route in de code bewijst de aanwezigheid van de pagina, niet dat iedere functie in een gewone browsersessie werkt. De tien kaarten volgen de actuele navigatievolgorde.</div>
<div class="grid">''' + "\n".join(cards) + '''</div><footer><a href="review.html">Terug naar de ontwerpreview</a> · <a href="field-route-review.json">Gestructureerde routegegevens</a> · Broncommit: ''' + escape(commit[:12]) + '''</footer></main></body></html>'''
(ROOT / "design/field-route-review.html").write_text(html)
print(f"Field route review: {len(routes)} routes, {len(screenshots)} repository screenshots")
