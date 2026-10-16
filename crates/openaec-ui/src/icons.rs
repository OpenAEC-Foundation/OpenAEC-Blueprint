//! Canonical semantic icons. Source SVG geometry is embedded, never fetched at runtime.
use iced::{widget::svg, Color};
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Icon {
    New,
    Open,
    Save,
    SaveAs,
    Print,
    Import,
    Export,
    Undo,
    Redo,
    Settings,
    Close,
    Minimize,
    Maximize,
    Restore,
    PanelLeft,
    PanelRight,
    Search,
    Measure,
    Fit,
    FitSelection,
    ZoomIn,
    ZoomOut,
    Pan,
    Cube,
    Extensions,
    Help,
    Back,
    Check,
    Grid,
    Microphone,
}
impl Icon {
    pub const ALL: [Self; 30] = [
        Self::New,
        Self::Open,
        Self::Save,
        Self::SaveAs,
        Self::Print,
        Self::Import,
        Self::Export,
        Self::Undo,
        Self::Redo,
        Self::Settings,
        Self::Close,
        Self::Minimize,
        Self::Maximize,
        Self::Restore,
        Self::PanelLeft,
        Self::PanelRight,
        Self::Search,
        Self::Measure,
        Self::Fit,
        Self::FitSelection,
        Self::ZoomIn,
        Self::ZoomOut,
        Self::Pan,
        Self::Cube,
        Self::Extensions,
        Self::Help,
        Self::Back,
        Self::Check,
        Self::Grid,
        Self::Microphone,
    ];
    pub fn id(self) -> &'static str {
        match self {
            Self::New => "new",
            Self::Open => "open",
            Self::Save => "save",
            Self::SaveAs => "save-as",
            Self::Print => "print",
            Self::Import => "import",
            Self::Export => "export",
            Self::Undo => "undo",
            Self::Redo => "redo",
            Self::Settings => "settings",
            Self::Close => "close",
            Self::Minimize => "minimize",
            Self::Maximize => "maximize",
            Self::Restore => "restore",
            Self::PanelLeft => "panel-left",
            Self::PanelRight => "panel-right",
            Self::Search => "search",
            Self::Measure => "measure",
            Self::Fit => "fit",
            Self::FitSelection => "fit-selection",
            Self::ZoomIn => "zoom-in",
            Self::ZoomOut => "zoom-out",
            Self::Pan => "pan",
            Self::Cube => "cube",
            Self::Extensions => "extensions",
            Self::Help => "help",
            Self::Back => "back",
            Self::Check => "check",
            Self::Grid => "grid",
            Self::Microphone => "microphone",
        }
    }
    pub fn bytes(self) -> &'static [u8] {
        match self {
            Self::New => include_bytes!("../assets/icons/new.svg"),
            Self::Open => include_bytes!("../assets/icons/open.svg"),
            Self::Save => include_bytes!("../assets/icons/save.svg"),
            Self::SaveAs => include_bytes!("../assets/icons/saveas.svg"),
            Self::Print => include_bytes!("../assets/icons/print.svg"),
            Self::Import => include_bytes!("../assets/icons/import.svg"),
            Self::Export => include_bytes!("../assets/icons/export.svg"),
            Self::Undo => include_bytes!("../assets/icons/undo.svg"),
            Self::Redo => include_bytes!("../assets/icons/redo.svg"),
            Self::Settings => include_bytes!("../assets/icons/settings.svg"),
            Self::Close => include_bytes!("../assets/icons/close.svg"),
            Self::Minimize => include_bytes!("../assets/icons/minimize.svg"),
            Self::Maximize => include_bytes!("../assets/icons/maximize.svg"),
            Self::Restore => include_bytes!("../assets/icons/restore.svg"),
            Self::PanelLeft => include_bytes!("../assets/icons/panelleft.svg"),
            Self::PanelRight => include_bytes!("../assets/icons/panelright.svg"),
            Self::Search => include_bytes!("../assets/icons/search.svg"),
            Self::Measure => include_bytes!("../assets/icons/measure.svg"),
            Self::Fit => include_bytes!("../assets/icons/fit.svg"),
            Self::FitSelection => include_bytes!("../assets/icons/fitselection.svg"),
            Self::ZoomIn => include_bytes!("../assets/icons/zoomin.svg"),
            Self::ZoomOut => include_bytes!("../assets/icons/zoomout.svg"),
            Self::Pan => include_bytes!("../assets/icons/pan.svg"),
            Self::Cube => include_bytes!("../assets/icons/cube.svg"),
            Self::Extensions => include_bytes!("../assets/icons/extensions.svg"),
            Self::Help => include_bytes!("../assets/icons/help.svg"),
            Self::Back => include_bytes!("../assets/icons/back.svg"),
            Self::Check => include_bytes!("../assets/icons/check.svg"),
            Self::Grid => include_bytes!("../assets/icons/grid.svg"),
            Self::Microphone => include_bytes!("../assets/icons/microphone.svg"),
        }
    }
    pub fn view<'a>(self, size: u16, color: Color) -> svg::Svg<'a> {
        svg(svg::Handle::from_memory(self.bytes()))
            .width(size)
            .height(size)
            .style(move |_, _| svg::Style { color: Some(color) })
    }
}

/// Reviewed tool-specific commands. Their names include the domain so a
/// visually similar shape cannot silently acquire another command meaning.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DomainIcon {
    PointcloudBagPanel,
    PointcloudEyeDome,
    CadShadedView,
    CadSpherePrimitive,
    GeotechSondering,
    GeotechBoring,
    GeotechSonderingGrid,
}

impl DomainIcon {
    pub const ALL: [Self; 7] = [
        Self::PointcloudBagPanel,
        Self::PointcloudEyeDome,
        Self::CadShadedView,
        Self::CadSpherePrimitive,
        Self::GeotechSondering,
        Self::GeotechBoring,
        Self::GeotechSonderingGrid,
    ];

    pub fn id(self) -> &'static str {
        match self {
            Self::PointcloudBagPanel => "pointcloud.bag-panel",
            Self::PointcloudEyeDome => "pointcloud.eye-dome",
            Self::CadShadedView => "cad.shaded-view",
            Self::CadSpherePrimitive => "cad.sphere-primitive",
            Self::GeotechSondering => "geotech.sondering",
            Self::GeotechBoring => "geotech.boring",
            Self::GeotechSonderingGrid => "geotech.sondering-grid",
        }
    }

    pub fn bytes(self, size: u16) -> &'static [u8] {
        match (self, size <= 16) {
            (Self::PointcloudBagPanel, true) => {
                include_bytes!("../assets/domain-icons-small/pointcloud-bag-panel.svg")
            }
            (Self::PointcloudBagPanel, false) => {
                include_bytes!("../assets/domain-icons/pointcloud-bag-panel.svg")
            }
            (Self::PointcloudEyeDome, true) => {
                include_bytes!("../assets/domain-icons-small/pointcloud-edl.svg")
            }
            (Self::PointcloudEyeDome, false) => {
                include_bytes!("../assets/domain-icons/pointcloud-edl.svg")
            }
            (Self::CadShadedView, true) => {
                include_bytes!("../assets/domain-icons-small/cad-shaded.svg")
            }
            (Self::CadShadedView, false) => {
                include_bytes!("../assets/domain-icons/cad-shaded.svg")
            }
            (Self::CadSpherePrimitive, true) => {
                include_bytes!("../assets/domain-icons-small/cad-sphere.svg")
            }
            (Self::CadSpherePrimitive, false) => {
                include_bytes!("../assets/domain-icons/cad-sphere.svg")
            }
            (Self::GeotechSondering, true) => {
                include_bytes!("../assets/domain-icons-small/geotech-sondering.svg")
            }
            (Self::GeotechSondering, false) => {
                include_bytes!("../assets/domain-icons/geotech-sondering.svg")
            }
            (Self::GeotechBoring, true) => {
                include_bytes!("../assets/domain-icons-small/geotech-boring.svg")
            }
            (Self::GeotechBoring, false) => {
                include_bytes!("../assets/domain-icons/geotech-boring.svg")
            }
            (Self::GeotechSonderingGrid, true) => {
                include_bytes!("../assets/domain-icons-small/geotech-sondering-grid.svg")
            }
            (Self::GeotechSonderingGrid, false) => {
                include_bytes!("../assets/domain-icons/geotech-sondering-grid.svg")
            }
        }
    }

    pub fn view<'a>(self, size: u16, color: Color) -> svg::Svg<'a> {
        svg(svg::Handle::from_memory(self.bytes(size)))
            .width(size)
            .height(size)
            .style(move |_, _| svg::Style { color: Some(color) })
    }
}
