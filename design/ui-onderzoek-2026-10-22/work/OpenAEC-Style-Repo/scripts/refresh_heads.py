"""Compare the inventory's immutable commits with current public GitHub heads."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "harmonization"
URL = "https://api.github.com/orgs/OpenAEC-Foundation/repos?per_page=100&type=all"
request = urllib.request.Request(URL, headers={"Accept": "application/vnd.github+json", "User-Agent": "OpenAEC-UI-harmonization"})
with urllib.request.urlopen(request, timeout=30) as response:
    repos = json.load(response)
assert len(repos) < 100, "Implement API pagination before auditing 100+ repositories"

def inspect(repo):
    name = repo["name"]
    branch = repo["default_branch"]
    previous_file = OUT / "repositories" / f"{name}.json"
    previous = json.loads(previous_file.read_text()) if previous_file.exists() else {}
    try:
        output = subprocess.check_output(
            ["git", "ls-remote", "--heads", repo["clone_url"], f"refs/heads/{branch}"],
            timeout=40, stderr=subprocess.PIPE, text=True,
        ).strip()
        head = output.split()[0] if output else None
        status = "unchanged" if head == previous.get("commit") else "changed" if head else "empty"
    except Exception as error:
        head = None
        status = "unavailable"
        return {"name": name, "default_branch": branch, "inventory_commit": previous.get("commit"), "current_head": head, "status": status, "error": str(error)}
    return {"name": name, "default_branch": branch, "inventory_commit": previous.get("commit"), "current_head": head, "status": status}

with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(inspect, repo) for repo in repos]
    results = sorted((future.result() for future in as_completed(futures)), key=lambda item: item["name"].lower())

payload = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "public_repositories": len(repos), "repositories": results}
(OUT / "head-audit.json").write_text(json.dumps(payload, indent=2) + "\n")
(OUT / "catalog.json").write_text(json.dumps(repos, indent=2) + "\n")
from collections import Counter
print(Counter(item["status"] for item in results))
