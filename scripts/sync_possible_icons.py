"""Keep unverified icon-like artwork available for offline review, outside the crate."""
import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "harmonization"
assets = json.loads((root / "asset-index.json").read_text())
possible = [asset for asset in assets if asset["category"] == "possible-ui-icon"]
for asset in possible:
    relative = Path(asset["repo"]) / asset["path"]
    source = root / "sources" / relative
    target = root / "possible-icons" / relative
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == asset["sha256"], relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_bytes() != data:
        shutil.copy2(source, target)
assert len(possible) == 53
print(f"Verified {len(possible)} unverified icon-like assets for offline review")
