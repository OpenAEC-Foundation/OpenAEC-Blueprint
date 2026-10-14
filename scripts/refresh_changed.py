"""Refresh only repositories whose public default branch moved since inventory."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inventory", root / "scripts/inventory.py")
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)
audit = json.loads((root / "harmonization/head-audit.json").read_text())
catalog = {repo["name"]: repo for repo in json.loads((root / "harmonization/catalog.json").read_text())}
changed = [record for record in audit["repositories"] if record["status"] == "changed"]

def refresh(record):
    name = record["name"]
    checkout = inventory.CACHE / name
    head = record["current_head"]
    subprocess.run(["git", "-C", str(checkout), "fetch", "--depth=1", "origin", head], check=True, timeout=180, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fetched = inventory.git(checkout, "rev-parse", "FETCH_HEAD").strip()
    if fetched != head:
        raise RuntimeError(f"{name}: fetched {fetched}, expected {head}")
    subprocess.run(["git", "-C", str(checkout), "update-ref", "HEAD", head], check=True)
    return inventory.inspect(catalog[name])

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {pool.submit(refresh, record): record["name"] for record in changed}
    for future in as_completed(futures):
        future.result()

print(f"Refreshed {len(changed)} repositories at audited commits")
