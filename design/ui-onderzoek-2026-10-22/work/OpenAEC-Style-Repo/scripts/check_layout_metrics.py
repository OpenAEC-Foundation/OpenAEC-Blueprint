#!/usr/bin/env python3
"""Check Rust and HTML band heights against the pinned Tauri layout source."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "design/layout-spec.json").read_text())
model = (root / "crates/openaec-ui/src/model.rs").read_text()
prototype = (root / "design/harmonized-template.html").read_text()
panel_title = re.search(r"\.paneltitle\{([^}]*)\}", prototype)
assert panel_title and "padding:0 4px 0 6px" in panel_title.group(1), "HTML panel title padding differs from Tauri"
assert "font-weight:600" in panel_title.group(1) and "letter-spacing:.5px" in panel_title.group(1), "HTML panel title typography differs from Tauri"
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
    "panel_toolbar": "paneltitle",
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
    app_css = (source_root / "../App.css").read_text()
    right = re.search(r"\.right-panel-toolbar\s*\{([^}]*)\}", app_css, flags=re.S)
    assert right and re.search(r"\bheight:\s*24px;", right.group(1)), "Pinned right panel toolbar changed"
    for side in ("left", "right"):
        toolbar = re.search(rf"\.{side}-panel-toolbar\s*\{{([^}}]*)\}}", app_css, flags=re.S)
        title = re.search(rf"\.{side}-panel-title\s*\{{([^}}]*)\}}", app_css, flags=re.S)
        assert toolbar and re.search(r"\bpadding:\s*0 4px 0 6px;", toolbar.group(1)), f"Pinned {side} panel padding changed"
        assert title and re.search(r"\bfont-weight:\s*600;", title.group(1)), f"Pinned {side} panel title changed"
        assert re.search(r"\bletter-spacing:\s*0\.5px;", title.group(1)), f"Pinned {side} panel tracking changed"
    print("Rust, HTML and local Tauri source agree: 32 / 28 / 94 / 30 / 22 px bands, 24 px panel toolbars, 240 px panels")
else:
    print("Rust and HTML agree with the recorded Tauri source: 32 / 28 / 94 / 30 / 22 px bands, 24 px panel toolbars, 240 px panels")
