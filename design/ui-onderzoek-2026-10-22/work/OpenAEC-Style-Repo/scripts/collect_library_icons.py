"""Archive imported Lucide and Solid/Tabler SVGs at the source package versions."""
from __future__ import annotations

import base64
import hashlib
import html
import io
import json
import re
import subprocess
import tarfile
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "harmonization"
OUT = H / "library-icons"
imports = json.loads((H / "imported-ui-icons.json").read_text())["records"]


def git(repo: str, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", f"/tmp/openaec-inventory/{repo}", *args], text=True, timeout=40
    )


@lru_cache(maxsize=None)
def repo_paths(repo: str) -> set[str]:
    return set(git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines())


@lru_cache(maxsize=None)
def package_version(repo: str, source: str, package: str) -> str:
    paths = repo_paths(repo)
    candidates = ["package.json"]
    parts = Path(source).parts[:-1]
    candidates += ["/".join(parts[:i]) + "/package.json" for i in range(1, len(parts) + 1)]
    for path in reversed(candidates):
        if path not in paths:
            continue
        data = json.loads(git(repo, "show", f"HEAD:{path}"))
        value = (data.get("dependencies") or {}).get(package) or (data.get("devDependencies") or {}).get(package)
        if value:
            match = re.search(r"\d+\.\d+\.\d+", value)
            if match:
                return match.group()
    raise ValueError(f"Cannot pin {package} for {repo}:{source}")


def npm_tarball(package: str, version: str) -> tarfile.TarFile:
    encoded = package.replace("/", "%2f")
    with urllib.request.urlopen(f"https://registry.npmjs.org/{encoded}/{version}", timeout=30) as response:
        metadata = json.load(response)
    with urllib.request.urlopen(metadata["dist"]["tarball"], timeout=90) as response:
        data = response.read()
    integrity = metadata["dist"].get("integrity", "")
    if integrity.startswith("sha512-"):
        expected = base64.b64decode(integrity[7:])
        if hashlib.sha512(data).digest() != expected:
            raise ValueError(f"npm tarball integrity mismatch: {package}@{version}")
    return tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")


def kebab(name: str) -> str:
    value = re.sub(r"([A-Z])([A-Z][a-z])", r"\1-\2", name)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"([A-Za-z])(\d+(?:x\d+)?)", r"\1-\2", value)
    return value.lower()


def checked_svg(data: bytes) -> bytes:
    root = ET.fromstring(data)
    if not root.tag.endswith("svg"):
        raise ValueError("Not an SVG")
    for node in root.iter():
        if node.tag.split("}")[-1] not in {"svg", "g", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse"}:
            raise ValueError(f"Unexpected SVG element: {node.tag}")
        if any(k.lower().startswith("on") or "href" in k.lower() for k in node.attrib):
            raise ValueError("SVG contains an active attribute")
    return data


grouped = defaultdict(list)
for item in imports:
    package = item["package"]
    if package not in {"lucide-react", "solid-icons/tb"}:
        continue
    npm_package = "lucide-static" if package == "lucide-react" else "solid-icons"
    version = package_version(item["repo"], item["source"], "lucide-react" if package == "lucide-react" else "solid-icons")
    grouped[(npm_package, version)].append(item)

records = []
missing = []
for (package, version), users in sorted(grouped.items()):
    archive = npm_tarball(package, version)
    names = set(archive.getnames())
    license_path = next((n for n in ("package/LICENSE", "package/LICENSE.md", "package/LICENSE.txt") if n in names), None)
    if license_path:
        dest = OUT / package / version / "LICENSE"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(archive.extractfile(license_path).read())
    source = None
    if package == "solid-icons":
        source = archive.extractfile("package/tb/index.js").read().decode()
    by_name = defaultdict(list)
    for user in users:
        by_name[user["name"]].append(user)
    for name, refs in sorted(by_name.items()):
        if package == "lucide-static":
            member = f"package/icons/{kebab(name)}.svg"
            if member not in names:
                missing.append({"package": package, "version": version, "name": name, "reason": "SVG absent in package"})
                continue
            data = archive.extractfile(member).read()
        else:
            pattern = re.compile(r"export function " + re.escape(name) + r"\(props\)\{return IconTemplate\(\{a:(\{.*?\}),c:'(.*?)'\},props\)\}", re.S)
            match = pattern.search(source)
            if not match:
                missing.append({"package": package, "version": version, "name": name, "reason": "Component absent in package"})
                continue
            attrs = json.loads(match.group(1))
            attr_text = " ".join(f'{key}="{html.escape(str(value), quote=True)}"' for key, value in attrs.items())
            data = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" {attr_text}>{match.group(2)}</svg>'.encode()
        data = checked_svg(data)
        dest = OUT / package / version / f"{name}.svg"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        records.append({
            "package": package, "version": version, "name": name,
            "file": str(dest.relative_to(H)),
            "sha256": hashlib.sha256(data).hexdigest(),
            "sources": [{k: ref[k] for k in ("repo", "source", "line", "commit")} for ref in refs],
        })
    archive.close()

payload = {"downloaded": len(records), "missing": missing, "icons": records}
(H / "library-icon-index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(f"Downloaded {len(records)} package-version SVGs; missing {len(missing)}")
