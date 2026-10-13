//! Canonical semantic icons. Source SVG geometry is embedded, never fetched at runtime.
use iced::{widget::svg, Color};
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Icon { New, Open, Save, Import, Export, Undo, Redo, Settings, Close, Minimize, Maximize, PanelLeft, PanelRight, Search, Measure, Fit, Cube, Help, Back, Check, Grid }
impl Icon {
pub const ALL: [Self; 21] = [Self::New, Self::Open, Self::Save, Self::Import, Self::Export, Self::Undo, Self::Redo, Self::Settings, Self::Close, Self::Minimize, Self::Maximize, Self::PanelLeft, Self::PanelRight, Self::Search, Self::Measure, Self::Fit, Self::Cube, Self::Help, Self::Back, Self::Check, Self::Grid];
pub fn bytes(self) -> &'static [u8] { match self {
Self::New => include_bytes!("../assets/icons/new.svg"),
Self::Open => include_bytes!("../assets/icons/open.svg"),
Self::Save => include_bytes!("../assets/icons/save.svg"),
Self::Import => include_bytes!("../assets/icons/import.svg"),
Self::Export => include_bytes!("../assets/icons/export.svg"),
Self::Undo => include_bytes!("../assets/icons/undo.svg"),
Self::Redo => include_bytes!("../assets/icons/redo.svg"),
Self::Settings => include_bytes!("../assets/icons/settings.svg"),
Self::Close => include_bytes!("../assets/icons/close.svg"),
Self::Minimize => include_bytes!("../assets/icons/minimize.svg"),
Self::Maximize => include_bytes!("../assets/icons/maximize.svg"),
Self::PanelLeft => include_bytes!("../assets/icons/panelleft.svg"),
Self::PanelRight => include_bytes!("../assets/icons/panelright.svg"),
Self::Search => include_bytes!("../assets/icons/search.svg"),
Self::Measure => include_bytes!("../assets/icons/measure.svg"),
Self::Fit => include_bytes!("../assets/icons/fit.svg"),
Self::Cube => include_bytes!("../assets/icons/cube.svg"),
Self::Help => include_bytes!("../assets/icons/help.svg"),
Self::Back => include_bytes!("../assets/icons/back.svg"),
Self::Check => include_bytes!("../assets/icons/check.svg"),
Self::Grid => include_bytes!("../assets/icons/grid.svg"),
}}
pub fn view<'a>(self, size: u16, color: Color) -> svg::Svg<'a> {
svg(svg::Handle::from_memory(self.bytes())).width(size).height(size).style(move |_,_| svg::Style { color: Some(color) })
}
}
