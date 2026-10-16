#!/usr/bin/env python3
"""Check that the reusable crate ships controls, not Style Repo research assets."""

import shutil
import subprocess
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
cargo = shutil.which("cargo") or str(Path.home() / ".cargo/bin/cargo")
result = subprocess.run(
    [cargo, "package", "-p", "openaec-ui", "--allow-dirty", "--list"],
    cwd=root, check=True, capture_output=True, text=True,
)
files = set(result.stdout.splitlines())
assert all(not name.startswith(("design/", "harmonization/", "src/bin/")) for name in files)
icons = {f"assets/icons/{p.name}" for p in (root / "crates/openaec-ui/assets/icons").glob("*.svg")}
domain_icons = {f"assets/{group}/{p.name}" for group in ("domain-icons", "domain-icons-small") for p in (root / "crates/openaec-ui/assets" / group).glob("*.svg")}
ribbon_icons = {f"assets/ribbon-icons/{p.name}" for p in (root / "crates/openaec-ui/assets/ribbon-icons").glob("*.svg")}
fonts = {f"assets/fonts/{p.name}" for p in (root / "crates/openaec-ui/assets/fonts").glob("*.ttf")}
icon_source = (root / "crates/openaec-ui/src/icons.rs").read_text()
core_count, domain_count = map(int, re.findall(r"pub const ALL: \[Self; (\d+)\]", icon_source))
assert len(icons) == core_count and len(domain_icons) == 2 * domain_count and len(fonts) == 6
ribbon_source = (root / "crates/openaec-ui/src/ribbon_icons.rs").read_text()
ribbon_count = int(re.search(r"pub const ALL: \[Self; (\d+)\]", ribbon_source).group(1))
assert len(ribbon_icons) == ribbon_count
assert icons <= files and domain_icons <= files and ribbon_icons <= files and fonts <= files
assert {f"licenses/{name}-OFL.txt" for name in ("Inter", "SpaceGrotesk", "JetBrainsMono")} <= files
assert {"NOTICE.md", "LICENSE", "README.md", "src/lib.rs"} <= files
print(f"Reusable crate package: {len(files)} files, {core_count} core icons, {len(domain_icons)} domain SVGs, {ribbon_count} typed ribbon icons, 6 fonts, 3 font notices, no research assets")
