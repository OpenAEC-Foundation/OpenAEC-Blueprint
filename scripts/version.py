#!/usr/bin/env python3
"""One version number for everything in this repository (issue #1).

The scheme is JJJJ.W.N: year, ISO week without a leading zero, and a sequence
number within that week that starts at 0, such as 2026.44.0. Releases are
tagged vJJJJ.W.N. The root Cargo.toml holds the version; every other version
field follows it.

  python scripts/version.py            show the version and where it is set
  python scripts/version.py --check    every field equal and valid (for the checks)
  python scripts/version.py --set 2026.44.0
  python scripts/version.py --next     the next number for today: N + 1 in the
                                       same ISO week, otherwise <year>.<week>.0;
                                       prints it, for a release workflow

After --set or --next, run scripts/generate_icon_crate.py: it writes the
version of openaec-icons from the root Cargo.toml.
"""

import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEME = re.compile(r"^(?P<year>\d{4})\.(?P<week>[1-9]\d?)\.(?P<n>0|[1-9]\d*)$")
# Cargo manifests whose [package] version follows the root.
MANIFESTS = ["Cargo.toml", "crates/openaec-ui/Cargo.toml", "crates/openaec-icons/Cargo.toml"]
PACKAGE_VERSION = re.compile(r'(\[package\][^\[]*?\nversion = ")([^"]+)(")', re.S)


def valid(version):
    match = SCHEME.match(version)
    return bool(match) and 1 <= int(match["week"]) <= 53


def read(path):
    match = PACKAGE_VERSION.search((ROOT / path).read_text(encoding="utf-8"))
    return match.group(2) if match else None


def current():
    """The version of the repository: the one in the root Cargo.toml."""
    return read("Cargo.toml")


def next_version(today=None, now=None):
    """The next release number for `today`, given the current version `now`."""
    today = today or datetime.date.today()
    year, week, _ = today.isocalendar()
    match = SCHEME.match(now or "")
    if match and int(match["year"]) == year and int(match["week"]) == week:
        return f"{year}.{week}.{int(match['n']) + 1}"
    return f"{year}.{week}.0"


def write(version):
    for path in MANIFESTS:
        file = ROOT / path
        text = file.read_text(encoding="utf-8")
        new, count = PACKAGE_VERSION.subn(lambda m: m.group(1) + version + m.group(3), text, count=1)
        assert count == 1, f"no [package] version in {path}"
        file.write_text(new, encoding="utf-8", newline="")


def main():
    args = sys.argv[1:]
    if args[:1] == ["--set"] and len(args) == 2 or args == ["--next"]:
        version = args[1] if args[0] == "--set" else next_version(now=current())
        if not valid(version):
            print(f"Ongeldige versie {version}: gebruik JJJJ.W.N, zonder voorloopnul in de week")
            return 1
        write(version)
        print(version)
        return 0
    versions = {path: read(path) for path in MANIFESTS}
    wrong = {p: v for p, v in versions.items() if v != current() or not valid(v or "")}
    if args == ["--check"]:
        if wrong:
            print(f"Versies niet gelijk of niet JJJJ.W.N: {wrong}")
            return 1
        print(f"Versie {current()} in alle {len(versions)} versievelden")
        return 0
    for path, version in versions.items():
        print(f"{version}  {path}")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
