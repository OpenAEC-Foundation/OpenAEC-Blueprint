#!/usr/bin/env python3
"""Check Rust and HTML band heights against the pinned Tauri layout source."""

import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "design/layout-spec.json").read_text())
model = (root / "src/model.rs").read_text()
prototype = (root / "design/harmonized-template.html").read_text()
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

source_root = root.parent / "OpenAEC-style-book" / spec["source_root"]
if source_root.exists():
    for region, entry in spec["regions"].items():
        source = (source_root / entry["source"]).read_text()
        selector = re.escape(entry["selector"])
        rule = re.search(rf"{selector}\s*\{{([^}}]*)\}}", source, flags=re.S)
        assert rule, f"Missing source selector for {region}"
        height = re.search(r"\bheight:\s*(\d+)px;", rule.group(1))
        assert height and int(height.group(1)) == entry["pixels"], f"Pinned source {region} changed"
    print("Rust, HTML and local Tauri source agree: 32 / 28 / 94 / 30 / 22 px")
else:
    print("Rust and HTML agree with the recorded Tauri source: 32 / 28 / 94 / 30 / 22 px")
