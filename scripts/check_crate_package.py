#!/usr/bin/env python3
"""Check that the reusable crate ships controls, not Style Repo research assets."""

import shutil
import subprocess
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
fonts = {f"assets/fonts/{p.name}" for p in (root / "crates/openaec-ui/assets/fonts").glob("*.ttf")}
assert len(icons) == 26 and len(fonts) == 6
assert icons <= files and fonts <= files
assert {f"licenses/{name}-OFL.txt" for name in ("Inter", "SpaceGrotesk", "JetBrainsMono")} <= files
assert {"NOTICE.md", "LICENSE", "README.md", "src/lib.rs"} <= files
print(f"Reusable crate package: {len(files)} files, 26 icons, 6 fonts, 3 font notices, no research assets")
