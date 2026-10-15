#!/usr/bin/env python3
"""Verify that the Pointcloud vendor snapshot matches the shared Rust crate."""

import subprocess
import shutil
import tomllib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
canonical = root / "crates/openaec-ui"
portable = root.parent / "open-pointcloud-studio/native/ui"
rustfmt = shutil.which("rustfmt") or str(Path.home() / ".cargo/bin/rustfmt")

for group in ("fonts", "icons", "domain-icons", "domain-icons-small"):
    canonical_assets = {p.name: p for p in (canonical / "assets" / group).iterdir() if p.is_file()}
    review_assets = {p.name: p for p in (root / "assets" / group).iterdir() if p.is_file()}
    assert canonical_assets.keys() == review_assets.keys(), f"Review {group} set differs"
    for name, source in canonical_assets.items():
        assert source.read_bytes() == review_assets[name].read_bytes(), f"Review {group} differs: {name}"

if not portable.is_dir():
    print("Canonical and review assets agree; local Pointcloud snapshot unavailable")
    raise SystemExit(0)

for name in ("README.md", "NOTICE.md", "LICENSE"):
    assert (canonical / name).read_bytes() == (portable / name).read_bytes(), f"Portable {name} differs"
canonical_licenses = {p.name: p for p in (canonical / "licenses").iterdir() if p.is_file()}
portable_licenses = {p.name: p for p in (portable / "licenses").iterdir() if p.is_file()}
assert canonical_licenses.keys() == portable_licenses.keys(), "Portable license set differs"
for name, source in canonical_licenses.items():
    assert source.read_bytes() == portable_licenses[name].read_bytes(), f"Portable license differs: {name}"


def formatted(path: Path) -> str:
    result = subprocess.run(
        [rustfmt, "--edition", "2021", "--config",
         "skip_children=true", "--emit", "stdout", str(path)],
        check=True, capture_output=True, text=True,
    )
    lines = result.stdout.splitlines(keepends=True)
    assert len(lines) >= 2 and lines[0].rstrip().endswith(":") and not lines[1].strip()
    return "".join(lines[2:])


canonical_sources = {p.name: p for p in (canonical / "src").glob("*.rs")}
portable_sources = {p.name: p for p in (portable / "src").glob("*.rs")}
assert canonical_sources.keys() == portable_sources.keys(), "Portable Rust file set differs"
for name, source in canonical_sources.items():
    assert formatted(source) == formatted(portable_sources[name]), f"Portable Rust source differs: {name}"

asset_count = 0
for group in ("fonts", "icons", "domain-icons", "domain-icons-small"):
    canonical_assets = {p.name: p for p in (canonical / "assets" / group).iterdir() if p.is_file()}
    portable_assets = {p.name: p for p in (portable / "assets" / group).iterdir() if p.is_file()}
    assert canonical_assets.keys() == portable_assets.keys(), f"Portable {group} set differs"
    for name, source in canonical_assets.items():
        assert source.read_bytes() == portable_assets[name].read_bytes(), f"Portable {group} differs: {name}"
        asset_count += 1

canonical_manifest = tomllib.loads((canonical / "Cargo.toml").read_text())
portable_manifest = tomllib.loads((portable / "Cargo.toml").read_text())
for key in ("name", "version", "edition", "description", "license"):
    assert canonical_manifest["package"][key] == portable_manifest["package"][key], f"Package {key} differs"
assert canonical_manifest["dependencies"] == portable_manifest["dependencies"], "Portable dependencies differ"
print(f"Portable crate matches {len(canonical_sources)} Rust files, {asset_count} assets and package dependencies")
