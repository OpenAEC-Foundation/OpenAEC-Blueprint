#!/usr/bin/env python3
"""Compare current public OpenAEC repositories with the pinned research archive.

This read-only GitHub check preserves historical inventory records and their SHAs.
"""
from datetime import datetime, timezone
from pathlib import Path
import html
import json
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ORG = "OpenAEC-Foundation"
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "OpenAEC-UI-access-audit"}


def request_json(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


org = request_json(f"{API}/orgs/{ORG}")
current = []
page = 1
while True:
    batch = request_json(f"{API}/orgs/{ORG}/repos?per_page=100&type=public&page={page}")
    current.extend(batch)
    if len(batch) < 100:
        break
    page += 1

assert len(current) == org["public_repos"], "Org count and paginated public listing differ"
names = {repo["name"] for repo in current}
assert len(names) == len(current), "Duplicate public repository name"
historical = {path.stem: json.loads(path.read_text()) for path in
              (ROOT / "harmonization/repositories").glob("*.json")}
historical_org = {name: repo for name, repo in historical.items()
                  if repo.get("url", "").startswith(f"https://github.com/{ORG}/")}
external = sorted(historical.keys() - historical_org.keys(), key=str.lower)

missing = []
for name in sorted(historical_org.keys() - names, key=str.lower):
    url = f"{API}/repos/{ORG}/{urllib.parse.quote(name)}"
    try:
        request_json(url)
        status = 200
    except urllib.error.HTTPError as error:
        status = error.code
    missing.append({
        "name": name,
        "api_status": status,
        "last_inventory_commit": historical_org[name].get("commit"),
        "last_inventory_errors": historical_org[name].get("errors", []),
    })

audit = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "organization": ORG,
    "current_public_count": len(current),
    "pinned_inventory_count": len(historical),
    "pinned_org_inventory_count": len(historical_org),
    "external_reference_names": external,
    "new_since_inventory": sorted(names - historical_org.keys(), key=str.lower),
    "historical_not_publicly_listed": missing,
    "current_public_repositories": sorted([
        {"name": repo["name"], "url": repo["html_url"],
         "default_branch": repo["default_branch"], "archived": repo["archived"],
         "pushed_at": repo["pushed_at"]}
        for repo in current
    ], key=lambda repo: repo["name"].lower()),
}
out = ROOT / "harmonization/public-access-audit.json"
out.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")

current_rows = []
for repo in audit["current_public_repositories"]:
    name = html.escape(repo["name"])
    url = html.escape(repo["url"], quote=True)
    pinned = historical_org.get(repo["name"], {}).get("commit")
    current_rows.append(f'<tr><td><a href="{url}">{name}</a></td>'
                        f'<td>{html.escape((pinned or "—")[:12])}</td>'
                        f'<td>{"ja" if repo["archived"] else "nee"}</td></tr>')
missing_rows = []
for repo in missing:
    missing_rows.append(f'<tr><td>{html.escape(repo["name"])}</td>'
                        f'<td>{repo["api_status"]}</td>'
                        f'<td>{html.escape((repo["last_inventory_commit"] or "—")[:12])}</td></tr>')
checked = html.escape(audit["checked_at_utc"])
page = f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · actuele publieke toegang</title><style>
body{{margin:0;background:#f6f6f7;color:#303039;font:14px/1.5 Inter,system-ui,sans-serif}}
header{{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(24px,calc((100vw - 1100px)/2))}}
main{{max-width:1100px;margin:auto;padding:24px}}h1{{margin:0;font-size:28px}}h2{{margin-top:30px}}p{{max-width:880px}}
.note{{background:white;border-left:3px solid #d97706;padding:12px 16px}}
table{{border-collapse:collapse;width:100%;background:white}}th,td{{padding:9px 12px;text-align:left;border-bottom:1px solid #e2e2e5}}
th{{background:#ececee}}a{{color:#ac5b00}}.count{{font-size:20px;font-weight:700;color:#ac5b00}}
</style><header><h1>Publieke OpenAEC-toegang</h1><p>GitHub API-controle · {checked}</p></header><main>
<p class="note">Het brongepinde onderzoeksarchief blijft bewaard. Een 404 betekent dat de naam nu niet publiek via de API toegankelijk is; het bewijst niet of de repository is verwijderd, hernoemd of privé gemaakt.</p>
<p><span class="count">{len(current)}</span> nu openbaar · <span class="count">{len(historical_org)}</span> historische OpenAEC-records · <span class="count">{len(missing)}</span> historische OpenAEC-namen niet in de openbare lijst · {len(audit['new_since_inventory'])} nieuw. Daarnaast {len(external)} externe referentie: {', '.join(map(html.escape, external))}.</p>
<h2>Historische namen zonder publieke API-toegang</h2><table><tr><th>Repository</th><th>API-status</th><th>Laatst vastgelegde commit</th></tr>{''.join(missing_rows)}</table>
<h2>Huidige openbare repositories</h2><table><tr><th>Repository</th><th>Gepinde onderzoekscommit</th><th>Gearchiveerd</th></tr>{''.join(current_rows)}</table>
<p><a href="review.html">Terug naar de ontwerpreview</a> · <a href="../harmonization/public-access-audit.json">Gestructureerde audit</a></p></main></html>'''
(ROOT / "design/public-access-audit.html").write_text(page)
print(f"Public now: {len(current)}; new: {len(audit['new_since_inventory'])}; "
      f"historical not listed: {len(missing)}")
for record in missing:
    print(f"  {record['name']}: GitHub API {record['api_status']}")
