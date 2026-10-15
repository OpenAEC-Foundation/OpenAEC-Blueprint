#!/usr/bin/env python3
"""Check reviewed Pointcloud icon adoptions against the portable Rust crate."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ledger = json.loads((root / "design/icon-adoptions.json").read_text())
decisions = ledger["decisions"]
chrome_decisions = ledger["chrome_decisions"]
assert len(decisions) == 10
assert len(chrome_decisions) == 1
for decision in decisions:
    shared = root / "assets/icons" / f'{decision["shared_icon"].replace("-", "")}.svg'
    assert shared.is_file(), shared

pointcloud = root.parent / "open-pointcloud-studio"
if pointcloud.exists():
    desktop = (pointcloud / "native/desktop/src/main.rs").read_text()
    mapping = re.search(r"fn canonical_icon\([^)]*\).*?\n}\n", desktop, flags=re.S)
    assert mapping, "Pointcloud canonical_icon function missing"
    for decision in decisions:
        variant = decision["tool_icon"]
        semantic = variant
        expected = rf"ToolIcon::{variant}\s*=>\s*Some\(Icon::{semantic}\)"
        assert re.search(expected, mapping.group(0)), f"Missing adoption: {variant} => {semantic}"
        portable = pointcloud / "native/ui/assets/icons" / f'{decision["shared_icon"].replace("-", "")}.svg'
        assert portable.read_bytes() == (root / "assets/icons" / portable.name).read_bytes(), (
            f"Portable icon drift: {portable.name}"
        )
        assert (pointcloud / decision["legacy_asset"]).is_file()
    assert re.search(r"Message::LoadDetail\s*\|\s*Message::RefreshLod\s*=>\s*ToolIcon::Update", desktop)
    for decision in chrome_decisions:
        semantic = decision["shared_icon"].title().replace("-", "")
        expected = rf"TitleIcon::{decision['title_icon']}\s*=>\s*Icon::{semantic}"
        assert re.search(expected, desktop), f"Missing title icon adoption: {expected}"
        shared = root / "assets/icons" / f'{decision["shared_icon"]}.svg'
        portable = pointcloud / "native/ui/assets/icons" / shared.name
        assert shared.read_bytes() == portable.read_bytes(), f"Portable title icon drift: {shared.name}"
    extensions_page = (pointcloud / "native/desktop/src/extensions/page.rs").read_text()
    assert re.search(r"Icon::Extensions\.view\(22, colors\.accent\)", extensions_page), "Extensions page heading does not use the shared icon"
    print("Ten reviewed tool icons and the visible Extensions page use shared SVGs in Pointcloud; LOD refresh stays distinct")
else:
    print("Eleven reviewed shared SVGs exist; local Pointcloud integration unavailable")
