"""Build a source-pinned inventory of every discovered screenshot candidate."""
from __future__ import annotations

import json
import subprocess
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "harmonization"
refs = json.loads((H / "visual-references.json").read_text())
catalog = {
    p.stem: json.loads(p.read_text())
    for p in (H / "repositories").glob("*.json")
}
items = []

for ref in refs:
    repo = ref["name"]
    meta = catalog.get(repo, {})
    selected = {x["path"]: x for x in ref.get("screenshots", [])}
    checkout = Path("/tmp/openaec-inventory") / repo
    blobs = {}
    if ref.get("available_screenshots") and (checkout / ".git").exists():
        head = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        if head == ref["commit"]:
            tree = subprocess.check_output(["git", "-C", str(checkout), "ls-tree", "-r", "-z", "HEAD"])
            for entry in tree.split(b"\0"):
                if b"\t" in entry:
                    metadata, path_bytes = entry.split(b"\t", 1)
                    blobs[path_bytes.decode()] = metadata.split()[2].decode()
    for path in ref.get("available_screenshots", []):
        lower = path.lower()
        if "social-preview" in lower or "social_preview" in lower:
            kind = "social-preview"
        elif repo == "openaec-installer" and lower.startswith("public/previews/"):
            kind = "catalog-preview"
        elif repo == "website":
            kind = "website-reference"
        elif "samples/preview" in lower:
            kind = "sample-preview"
        else:
            kind = "application-screen"
        url = (
            f"https://raw.githubusercontent.com/"
            f"{meta.get('url', '').removeprefix('https://github.com/')}/"
            f"{ref['commit']}/{urllib.parse.quote(path)}"
        )
        record = {
            "repository": repo,
            "path": path,
            "kind": kind,
            "commit": ref["commit"],
            "git_blob": blobs.get(path),
            "url": url,
            "local": selected.get(path, {}).get("local"),
            "assessment": "candidate; visual review pending",
        }
        items.append(record)

items.sort(key=lambda x: (x["repository"].lower(), x["path"].lower()))
counts = dict(Counter(x["kind"] for x in items))
manifest = {
    "total": len(items),
    "unique_known_blobs": len({x["git_blob"] for x in items if x["git_blob"]}),
    "counts": counts,
    "screens": items,
}
(H / "screen-index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

template = (ROOT / "design/screen-inventory-template.html").read_text()
payload = json.dumps(manifest, ensure_ascii=False).replace("</", "<\\/")
(ROOT / "design/screen-inventory.html").write_text(template.replace("/*SCREEN_DATA*/", payload))
print(f"Indexed {len(items)} candidates: {counts}")
