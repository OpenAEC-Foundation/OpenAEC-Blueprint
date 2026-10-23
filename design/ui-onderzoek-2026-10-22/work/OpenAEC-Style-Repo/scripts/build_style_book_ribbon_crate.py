#!/usr/bin/env python3
"""Build typed Rust ribbon-icon assets from the reviewed Tauri crosswalk."""
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decisions = json.loads((ROOT / "design/style-book-tauri-ribbon-crosswalk.json").read_text())
chosen = [x for x in decisions["decisions"] if x["status"] == "nieuw domeincommando"]
assert len(chosen) == 32
crate = ROOT / "crates/openaec-ui"
assets = crate / "assets/ribbon-icons"
assets.mkdir(parents=True, exist_ok=True)


def kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


rows = []
for item in chosen:
    variant = item["target"].removeprefix("RibbonIcon::")
    assert variant != item["target"]
    source = ROOT / "harmonization" / item["source_svg"]
    ET.parse(source)
    dest = assets / f"{kebab(variant)}.svg"
    shutil.copyfile(source, dest)
    rows.append((variant, kebab(variant), dest.name))

assert len({variant for variant, *_ in rows}) == 32
variants = "\n".join(f"    {variant}," for variant, *_ in rows)
all_rows = "\n".join(f"        Self::{variant}," for variant, *_ in rows)
ids = "\n".join(f'            Self::{variant} => "{identifier}",' for variant, identifier, _ in rows)
bytes_rows = "\n".join(f'            Self::{variant} => include_bytes!("../assets/ribbon-icons/{filename}"),' for variant, _, filename in rows)
body = f'''//! Typed Tauri Style Book ribbon commands, reviewed against active UI routes.
//! Source: OpenAEC-style-book @ {decisions['commit']} (CC-BY-SA-4.0).
use iced::{{widget::svg, Color}};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RibbonIcon {{
{variants}
}}

impl RibbonIcon {{
    pub const ALL: [Self; 32] = [
{all_rows}
    ];

    pub const fn id(self) -> &'static str {{
        match self {{
{ids}
        }}
    }}

    pub fn bytes(self) -> &'static [u8] {{
        match self {{
{bytes_rows}
        }}
    }}

    pub fn view<'a>(self, size: u16, color: Color) -> svg::Svg<'a> {{
        svg(svg::Handle::from_memory(self.bytes()))
            .width(size)
            .height(size)
            .style(move |_, _| svg::Style {{ color: Some(color) }})
    }}
}}
'''
(crate / "src/ribbon_icons.rs").write_text(body)
print(f"Built {len(rows)} typed Style Book ribbon icons")
