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


def executable_text(source: str) -> str:
    """Mask strings/comments while preserving offsets and line breaks."""
    out = list(source)
    i = 0
    while i < len(source):
        quote = source[i]
        if source.startswith("//", i):
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
        elif source.startswith("/*", i):
            stop = source.find("*/", i + 2)
            end = len(source) if stop < 0 else stop + 2
        elif quote in "'\"`":
            end = i + 1
            while end < len(source):
                if source[end] == "\\":
                    end += 2
                elif source[end] == quote:
                    end += 1
                    break
                else:
                    end += 1
        else:
            i += 1
            continue
        for pos in range(i, min(end, len(source))):
            if source[pos] != "\n":
                out[pos] = " "
        i = end
    return "".join(out)


def usage_lines(source: str, imports: list[re.Match[str]], local_name: str) -> tuple[list[int], list[int]]:
    masked = list(executable_text(source))
    for imp in imports:
        for pos in range(imp.start(), imp.end()):
            if source[pos] != "\n":
                masked[pos] = " "
    code = "".join(masked)
    identifier = re.compile(r"\b" + re.escape(local_name) + r"\b")
    uses = [source.count("\n", 0, match.start()) + 1 for match in identifier.finditer(code)]
    jsx = [source.count("\n", 0, match.start()) + 1 for match in re.finditer(r"<\s*" + re.escape(local_name) + r"\b", code)]
    return sorted(set(uses)), sorted(set(jsx))

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
    if subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip() != repos[repo]["commit"]:
        errors.append({"repo": repo, "source": source, "reason": "checkout commit differs from inventory"})
        continue
    imports = list(pattern.finditer(result.stdout))
    for match in imports:
        package = match.group(2)
        if not is_icon_package.search(package):
            continue
        line = result.stdout.count("\n", 0, match.start()) + 1
        for raw in match.group(1).split(","):
            raw = raw.strip()
            if not raw or raw.startswith("type "):
                continue
            names = re.split(r"\s+as\s+", raw, maxsplit=1)
            name = names[0].strip()
            local_name = names[-1].strip()
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name) or name.endswith("Icon") and name == "LucideIcon":
                continue
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", local_name):
                continue
            references, jsx_uses = usage_lines(result.stdout, imports, local_name)
            records.append({
                "package": package,
                "name": name,
                "local_name": local_name,
                "repo": repo,
                "source": source,
                "line": line,
                "commit": repos.get(repo, {}).get("commit"),
                "reference_lines": references,
                "jsx_lines": jsx_uses,
                "evidence": "jsx-render" if jsx_uses else "identifier-reference" if references else "import-only",
            })

payload = {
    "import_occurrences": len(records),
    "unique_package_names": len({(r["package"], r["name"]) for r in records}),
    "packages": dict(Counter(r["package"] for r in records)),
    "evidence": dict(Counter(r["evidence"] for r in records)),
    "records": records,
    "errors": errors,
}
(H / "imported-ui-icons.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(payload["import_occurrences"], "imports,", payload["unique_package_names"], "distinct package/name pairs,", len(errors), "errors")
