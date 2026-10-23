#!/usr/bin/env python3
"""Check reviewed Pointcloud icon adoptions against the portable Rust crate."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ledger = json.loads((root / "design/icon-adoptions.json").read_text())
explorer = json.loads((root / "design/pile-pointcloud-explorer-decisions.json").read_text())["pairs"]
decisions = ledger["decisions"]
domain_decisions = ledger["domain_decisions"]
chrome_decisions = ledger["chrome_decisions"]
assert len(decisions) == 10
assert len(domain_decisions) == 6
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
    explorer_mapping = {
        "duplicate": ("Duplicate", "Duplicate"),
        "rename": ("Rename", "Rename"),
        "disclosure-expanded": ("ChevronOpen", "DisclosureExpanded"),
        "disclosure-collapsed": ("ChevronClosed", "DisclosureCollapsed"),
    }
    assert {item["id"] for item in explorer} == set(explorer_mapping)
    for decision in explorer:
        tool, semantic = explorer_mapping[decision["id"]]
        expected = rf"ToolIcon::{tool}\s*=>\s*Some\(Icon::{semantic}\)"
        assert re.search(expected, mapping.group(0)), f"Missing explorer adoption: {expected}"
        filename = decision["id"] + ".svg"
        shared = root / "crates/openaec-ui/assets/icons" / filename
        portable = pointcloud / "native/ui/assets/icons" / filename
        assert shared.read_bytes() == portable.read_bytes() == (root / decision["pile_svg"]).read_bytes(), filename
        assert (root / decision["pointcloud_svg"]).is_file()
    domain_mapping = re.search(r"fn domain_icon\([^)]*\).*?\n}\n", desktop, flags=re.S)
    assert domain_mapping, "Pointcloud domain_icon function missing"
    for decision in domain_decisions:
        expected = rf"ToolIcon::{decision['tool_icon']}\s*=>\s*Some\(DomainIcon::{decision['shared_icon']}\)"
        assert re.search(expected, domain_mapping.group(0)), f"Missing domain adoption: {expected}"
        for folder in ("domain-icons", "domain-icons-small"):
            shared = root / "crates/openaec-ui/assets" / folder / decision["asset"]
            portable = pointcloud / "native/ui/assets" / folder / decision["asset"]
            assert shared.read_bytes() == portable.read_bytes(), f"Portable domain icon drift: {folder}/{decision['asset']}"
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
    print("Fourteen core and six domain tool icons plus the Extensions page use shared SVGs in Pointcloud; LOD refresh stays distinct")
else:
    print("Reviewed shared SVGs exist; local Pointcloud integration unavailable")
