"""Render pinned library icons with evidence of post-import UI references."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "harmonization/library-icon-index.json").read_text())
imports = json.loads((root / "harmonization/imported-ui-icons.json").read_text())
repo_meta = {
    path.stem: json.loads(path.read_text())
    for path in (root / "harmonization/repositories").glob("*.json")
}
uses = {(item["repo"], item["source"], item["line"], item["name"]): item for item in imports["records"]}
counts = Counter()
for icon in data["icons"]:
    references = []
    for source in icon["sources"]:
        key = (source["repo"], source["source"], source["line"], icon["name"])
        use = uses[key]
        line = (use["jsx_lines"] or use["reference_lines"])[0]
        repo = repo_meta[source["repo"]]
        url = f'{repo["url"].rstrip("/")}/blob/{source["commit"]}/{quote(source["source"])}#L{line}'
        references.append({"repo": source["repo"], "source": source["source"], "line": line,
                           "evidence": use["evidence"], "url": url})
    icon["uses"] = references
    icon["evidence"] = "jsx-render" if any(ref["evidence"] == "jsx-render" for ref in references) else "identifier-reference"
    counts[icon["evidence"]] += 1
assert sum(counts.values()) == data["downloaded"] == 312
data["use_counts"] = dict(counts)
data["import_counts"] = imports["evidence"]
template = (root / "design/library-icons-template.html").read_text()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
(root / "design/library-icons.html").write_text(template.replace("/*ICON_DATA*/", payload))
print(f"Built imported icon atlas: {data['downloaded']} SVGs, {dict(counts)}")
