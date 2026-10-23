"""Keep the distributable UI-only icon research set in sync with source hashes."""
import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "harmonization"
assets = json.loads((root / "asset-index.json").read_text())
count = 0
for asset in assets:
    if asset["category"] != "ui-used":
        continue
    relative = Path(asset["repo"]) / asset["path"]
    source = root / "sources" / relative
    target = root / "ui-icons" / relative
    if not source.is_file():
        raise FileNotFoundError(source)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != asset["sha256"]:
        raise ValueError(f"Source hash differs from inventory: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        shutil.copy2(source, target)
    count += 1
print(f"Verified {count} source-backed UI icons")
