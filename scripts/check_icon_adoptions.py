#!/usr/bin/env python3
"""Check reviewed Pointcloud icon adoptions against the portable Rust crate."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
decisions = json.loads((root / "design/icon-adoptions.json").read_text())["decisions"]
assert len(decisions) == 6
for decision in decisions:
    shared = root / "assets/icons" / f'{decision["shared_icon"]}.svg'
    assert shared.is_file(), shared

pointcloud = root.parent / "open-pointcloud-studio"
if pointcloud.exists():
    desktop = (pointcloud / "native/desktop/src/main.rs").read_text()
    mapping = re.search(r"fn canonical_icon\([^)]*\).*?\n}\n", desktop, flags=re.S)
    assert mapping, "Pointcloud canonical_icon function missing"
    for decision in decisions:
        variant = decision["tool_icon"]
        semantic = decision["shared_icon"].title().replace("-", "")
        expected = rf"ToolIcon::{variant}\s*=>\s*Some\(Icon::{semantic}\)"
        assert re.search(expected, mapping.group(0)), f"Missing adoption: {variant} => {semantic}"
        portable = pointcloud / "native/ui/assets/icons" / f'{decision["shared_icon"]}.svg'
        assert portable.read_bytes() == (root / "assets/icons" / portable.name).read_bytes(), (
            f"Portable icon drift: {portable.name}"
        )
        assert (pointcloud / decision["legacy_asset"]).is_file()
    assert re.search(r"Message::LoadDetail\s*\|\s*Message::RefreshLod\s*=>\s*ToolIcon::Update", desktop)
    print("Six reviewed icons use identical SVGs in Pointcloud; LOD refresh stays distinct")
else:
    print("Six reviewed shared SVGs exist; local Pointcloud integration unavailable")
