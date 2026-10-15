#!/usr/bin/env python3
"""Show per-public-repository evidence without treating every SVG as a UI icon."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "harmonization"
D = ROOT / "design"

public = json.loads((H / "public-access-audit.json").read_text())
source = {
    p.stem: json.loads(p.read_text())
    for p in (H / "repositories").glob("*.json")
}
scans = {
    item["repository"]: item
    for item in json.loads((H / "ui-code-references.json").read_text())
}
assets = json.loads((H / "asset-index.json").read_text())
screens = json.loads((H / "screen-index.json").read_text())["screens"]
libraries = json.loads((H / "library-icon-index.json").read_text())["icons"]

ui_files = Counter(item["repo"] for item in assets if item["category"] == "ui-used")
possible_files = Counter(item["repo"] for item in assets if item["category"] == "possible-ui-icon")
app_screens = Counter(item["repository"] for item in screens if item["kind"] == "application-screen")
local_screens = Counter(item["repository"] for item in screens if item["kind"] == "application-screen" and item["local"])
library_ids: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
for icon in libraries:
    key = (icon["package"], icon["version"], icon["name"])
    for use in icon["sources"]:
        library_ids[use["repo"]].add(key)

rows = []
for repo in public["current_public_repositories"]:
    name = repo["name"]
    scan = scans.get(name)
    pin = source.get(name, {}).get("commit")
    rows.append({
        "name": name,
        "url": repo["url"],
        "pinned_commit": pin,
        "ui_source_status": ("empty-public-repository" if not pin and repo.get("commit_api_status") == 409
                             else scan["status"] if scan else "not-in-code-audit"),
        "ui_code_files": scan.get("code_files", 0) if scan else 0,
        "ui_reference_lines": len(scan["matches"]) if scan else 0,
        "ui_asset_files": ui_files[name],
        "possible_asset_files": possible_files[name],
        "library_icon_imports": len(library_ids[name]),
        "application_screen_candidates": app_screens[name],
        "locally_copied_screens": local_screens[name],
    })

assert len(rows) == public["current_public_count"]
assert len({item["name"] for item in rows}) == len(rows)
assert all(item["pinned_commit"] or item["ui_source_status"] == "empty-public-repository" for item in rows), \
    "Public repository without a pin needs an explicit empty-repository API check"

totals = {
    "public_repositories": len(rows),
    "ui_source_scanned": sum(row["ui_source_status"] == "source-scanned" for row in rows),
    "empty_public_repositories": sum(row["ui_source_status"] == "empty-public-repository" for row in rows),
    "ui_asset_files": sum(row["ui_asset_files"] for row in rows),
    "library_icon_imports_by_repository": sum(row["library_icon_imports"] for row in rows),
    "application_screen_candidates": sum(row["application_screen_candidates"] for row in rows),
    "locally_copied_screens": sum(row["locally_copied_screens"] for row in rows),
}
manifest = {
    "based_on_public_access_audit_utc": public["checked_at_utc"],
    "basis": "pinned source commits; screenshot candidates are not individually approved screen designs",
    "totals": totals,
    "repositories": rows,
}
(H / "coverage-matrix.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

def esc(value: object) -> str:
    return html.escape(str(value), quote=True)

trs = []
for row in rows:
    searchable = (row["name"] + " " + row["ui_source_status"]).lower()
    screen = row["application_screen_candidates"]
    copied = row["locally_copied_screens"]
    trs.append(
        f'<tr data-search="{esc(searchable)}" data-gap="{int(not(screen or row["ui_asset_files"] or row["library_icon_imports"]))}">'
        f'<td><a href="{esc(row["url"])}">{esc(row["name"])}</a><small>{esc((row["pinned_commit"] or "")[:10])}</small></td>'
        f'<td>{esc(row["ui_source_status"])}<small>{row["ui_code_files"]} codebestanden · {row["ui_reference_lines"]} trefregels</small></td>'
        f'<td class="number">{row["ui_asset_files"]}</td>'
        f'<td class="number">{row["library_icon_imports"]}</td>'
        f'<td class="number">{screen}<small>{copied} lokaal gekopieerd</small></td>'
        f'<td class="number">{row["possible_asset_files"]}</td></tr>'
    )

checked = datetime.fromisoformat(public["checked_at_utc"]).strftime("%d-%m-%Y %H:%M UTC")
page = f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · bewijsdekking per repository</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f4f5;color:#303039;font:13px/1.45 Inter,system-ui,sans-serif}}header{{background:#303039;color:white;border-bottom:3px solid #d97706;padding:25px max(20px,calc((100vw - 1320px)/2))}}header a{{color:#ffbf70}}h1{{font-size:27px;margin:6px 0}}header p{{margin:0;color:#dddde2;max-width:980px}}main{{max-width:1360px;margin:auto;padding:22px}}a{{color:#a34f00}}.counts{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}.counts span{{background:white;border:1px solid #dddde1;padding:8px 12px}}.counts b{{color:#ae5700;font-size:19px;margin-right:5px}}.note{{background:#fff;border-left:3px solid #d97706;padding:12px 15px;margin:15px 0}}.controls{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:14px 0}}input[type=search]{{font:inherit;padding:8px 10px;border:1px solid #babac0;min-width:min(330px,80vw)}}.controls label{{display:inline-flex;gap:6px;align-items:center;white-space:nowrap}}.controls output{{margin-left:auto}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:9px 11px;border-bottom:1px solid #e3e3e6;text-align:left;vertical-align:top}}th{{background:#e9e9ec;position:sticky;top:0;z-index:1}}td small{{display:block;color:#73737b;font-size:11px}}td.number{{font-variant-numeric:tabular-nums;text-align:right}}tr[hidden]{{display:none}}@media(max-width:800px){{table{{display:block;overflow-x:auto}}th,td{{min-width:110px}}}}
</style><header><a href="review.html">← Visuele review</a><h1>Bewijsdekking per OpenAEC-repository</h1><p>63 publieke organisatierepositories · gepinde broncommits · toegang opnieuw gecontroleerd op {esc(checked)}</p></header><main>
<div class="counts"><span><b>{totals["public_repositories"]}</b>publiek</span><span><b>{totals["ui_source_scanned"]}</b>repositories met codeaudit</span><span><b>{totals["empty_public_repositories"]}</b>publiek maar leeg</span><span><b>{totals["ui_asset_files"]}</b>UI-gebruikte assetbestanden</span><span><b>{totals["library_icon_imports_by_repository"]}</b>bibliotheekiconen per repo</span><span><b>{totals["application_screen_candidates"]}</b>applicatieschermkandidaten</span><span><b>{totals["locally_copied_screens"]}</b>lokaal gekopieerd</span></div>
<p class="note"><strong>Leeswijzer.</strong> Alleen direct in UI-code gebruikte assetbestanden tellen als UI-asset; SVG's in technische tekeningen en branding tellen niet mee. Bibliotheekimporten tellen apart en kunnen in meerdere repositories dezelfde vorm gebruiken. Een schermkandidaat is geen beoordeelde of actuele productstaat. Nul betekent dat deze gepinde audit geen bewijs vond, niet dat de tool geen iconen of schermen heeft. De drie lege publieke repositories geven een GitHub-commits-API-status 409 terug; ze hebben geen broncommit. De vier niet-publiek bereikbare historische namen staan in de <a href="public-access-audit.html">toegangsaudit</a>; OpenCADStudio is een externe referentie buiten deze 63.</p>
<div class="controls"><input id="search" type="search" placeholder="Zoek repository of scanstatus" aria-label="Zoek repositories"><label><input id="gaps" type="checkbox"> Alleen zonder icon- en schermbewijs</label><output id="shown"></output></div>
<table><thead><tr><th>Repository · broncommit</th><th>UI-codeaudit</th><th>Gebruikte assetbestanden</th><th>Bibliotheekiconen</th><th>Applicatieschermen</th><th>Mogelijke UI-assets</th></tr></thead><tbody>{''.join(trs)}</tbody></table>
<p class="note">Detailbronnen: <a href="../harmonization/coverage-matrix.json">deze matrix als JSON</a> · <a href="screen-inventory.html">alle 666 beeldkandidaten met type</a> · <a href="icon-review-board.html">UI-assetreview</a> · <a href="library-icons.html">gebruikte bibliotheekiconen</a>.</p></main>
<script>const rows=[...document.querySelectorAll('tbody tr')];const search=document.querySelector('#search');const gaps=document.querySelector('#gaps');function update(){{const q=search.value.toLocaleLowerCase();let shown=0;for(const row of rows){{row.hidden=!(row.dataset.search.includes(q)&&(!gaps.checked||row.dataset.gap==='1'));shown+=!row.hidden}}document.querySelector('#shown').textContent=shown+' / '+rows.length}}search.oninput=update;gaps.onchange=update;update();</script></html>'''
(D / "coverage-matrix.html").write_text(page)
print(totals)
