#!/usr/bin/env python3
"""Check Rust and HTML band heights against the pinned Tauri layout source."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "design/layout-spec.json").read_text())
model = (root / "src/model.rs").read_text()
prototype = (root / "design/harmonized-template.html").read_text()
panel = spec["panel_default"]["pixels"]
rust_panel = re.search(r"pub const PANEL_DEFAULT: u16 = (\d+);", model)
html_panels = re.search(r"\.body\{[^}]*grid-template-columns:(\d+)px minmax\(320px,1fr\) (\d+)px", prototype)
assert rust_panel and int(rust_panel.group(1)) == panel, f"Rust panel differs from {panel}px"
assert html_panels and all(int(value) == panel for value in html_panels.groups()), f"HTML panels differ from {panel}px"
selectors = {
    "title": "titlebar",
    "tabs": "tabs",
    "ribbon": "ribbon",
    "documents": "docbar",
    "status": "status",
}
for region, entry in spec["regions"].items():
    expected = entry["pixels"]
    rust = re.search(rf"pub const {region.upper()}: u16 = (\d+);", model)
    html = re.search(rf"\.{selectors[region]}\{{height:(\d+)px;", prototype)
    assert rust and int(rust.group(1)) == expected, f"Rust {region} differs from {expected}px"
    assert html and int(html.group(1)) == expected, f"HTML {region} differs from {expected}px"

portable = root.parent / "open-pointcloud-studio/native/ui/src/model.rs"
if portable.exists():
    portable_model = portable.read_text()
    portable_metrics = [
        (region.upper(), entry["pixels"]) for region, entry in spec["regions"].items()
    ] + [("PANEL_DEFAULT", panel)]
    for name, expected in portable_metrics:
        value = re.search(rf"pub const {name}: u16 = (\d+);", portable_model)
        assert value and int(value.group(1)) == expected, (
            f"Pointcloud portable crate {name} differs from {expected}px"
        )
    print("Pointcloud portable crate agrees with the shared layout metrics")

source_root = root.parent / "OpenAEC-style-book" / spec["source_root"]
if source_root.exists():
    app = (root.parent / "OpenAEC-style-book" / spec["panel_default"]["source"]).read_text()
    for side in ("left", "right"):
        match = re.search(rf"\[{side}PanelWidth, set{side.capitalize()}PanelWidth\] = useState\((\d+)\)", app)
        assert match and int(match.group(1)) == panel, f"Pinned Tauri {side} panel changed"
    for region, entry in spec["regions"].items():
        source = (source_root / entry["source"]).read_text()
        selector = re.escape(entry["selector"])
        rule = re.search(rf"{selector}\s*\{{([^}}]*)\}}", source, flags=re.S)
        assert rule, f"Missing source selector for {region}"
        height = re.search(r"\bheight:\s*(\d+)px;", rule.group(1))
        assert height and int(height.group(1)) == entry["pixels"], f"Pinned source {region} changed"
    print("Rust, HTML and local Tauri source agree: 32 / 28 / 94 / 30 / 22 px bands, 240 px panels")
else:
    print("Rust and HTML agree with the recorded Tauri source: 32 / 28 / 94 / 30 / 22 px bands, 240 px panels")
