"""Record named UI-library icons separately from archived icon files."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "harmonization"
code_sources = json.loads((H / "ui-icon-code-sources.json").read_text())
repos = {p.stem: json.loads(p.read_text()) for p in (H / "repositories").glob("*.json")}
source_paths = {(x["repo"], x["source"]) for x in code_sources if x["kind"] == "icon-library"}
pattern = re.compile(r"import\s+(?:type\s+)?\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]", re.S)
is_icon_package = re.compile(r"(?:lucide-react|solid-icons/|@tabler/icons|@phosphor-icons|@heroicons|@fortawesome|react-icons/|@radix-ui/react-icons)")
records = []
errors = []
for repo, source in sorted(source_paths):
    checkout = Path("/tmp/openaec-inventory") / repo
    if not (checkout / ".git").exists():
        errors.append({"repo": repo, "source": source, "reason": "checkout unavailable"})
        continue
    result = subprocess.run(
        ["git", "-C", str(checkout), "show", f"HEAD:{source}"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        errors.append({"repo": repo, "source": source, "reason": result.stderr[:160]})
        continue
    for match in pattern.finditer(result.stdout):
        package = match.group(2)
        if not is_icon_package.search(package):
            continue
        line = result.stdout.count("\n", 0, match.start()) + 1
        for raw in match.group(1).split(","):
            raw = raw.strip()
            if not raw or raw.startswith("type "):
                continue
            name = raw.split(" as ", 1)[0].strip()
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name) or name.endswith("Icon") and name == "LucideIcon":
                continue
            records.append({
                "package": package,
                "name": name,
                "repo": repo,
                "source": source,
                "line": line,
                "commit": repos.get(repo, {}).get("commit"),
            })

payload = {
    "import_occurrences": len(records),
    "unique_package_names": len({(r["package"], r["name"]) for r in records}),
    "packages": dict(Counter(r["package"] for r in records)),
    "records": records,
    "errors": errors,
}
(H / "imported-ui-icons.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(payload["import_occurrences"], "imports,", payload["unique_package_names"], "distinct package/name pairs,", len(errors), "errors")
