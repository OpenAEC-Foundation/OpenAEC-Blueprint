//! UI 0.4 gallery: the components of library 0.4 in the five themes, as a full
//! application screen and as a component sheet. Run it smoothly with
//! `cargo run --release --features gpu --bin ui04`; add `-- installer`,
//! `-- werkstroom`, `-- componenten` or `-- iconen` to open another view first.
//!
//! Everything is drawn with `openaec_ui::design`; the icons are Codex's B2 set
//! from `design/icon-set-b2`. The sample screen is a small working estimate so
//! the design can be judged by using it: tabs, ribbon, tree, editing, undo,
//! dialogs, notifications and shortcuts all respond. It is a review aid, not an app.
use openaec_ui::design::chrome::{self as ch, MenuItem, WindowActions, WindowIcons};
use openaec_ui::design::command::{self as cm, Command, Shortcut};
use openaec_ui::design::focus;
use openaec_ui::design::shortcuts::{self as sc, Keymap};
use openaec_ui::design::tiles::{self as t, RecentFile};
use openaec_ui::design::widgets::{self as w, ButtonKind as K, Density as D, DocumentTab, TableColumn, Tone};
use openaec_ui::design::workflow::{self as wf, Navigation, Section};
use openaec_ui::design::{font, Look, StatusbarSetting, ThemeId, WorkspaceSetting};
use openaec_ui::fonts;
use openaec_ui::iced::widget::{column, container, mouse_area, row, scrollable, text, Space};
use openaec_ui::iced::{self, keyboard, mouse, Alignment, Background, Element, Length, Point, Size, Subscription, Task};
use openaec_icons::Icon;
use std::collections::HashSet;
use std::sync::OnceLock;
use std::time::{Duration, Instant};

macro_rules! b2 {
    ($size:literal, $name:literal) => {
        include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/design/icon-set-b2/svg/", $size, "/", $name, ".svg"))
    };
}

const NEW: &str = b2!("24", "file.new");
const OPEN: &str = b2!("24", "file.open");
const SAVE: &str = b2!("24", "file.save");
const UNDO: &str = b2!("24", "edit.undo");
const REDO: &str = b2!("24", "edit.redo");
const PASTE: &str = b2!("24", "edit.paste");
const CUT: &str = b2!("16", "edit.cut");
const COPY: &str = b2!("16", "edit.copy");
const DELETE: &str = b2!("16", "edit.delete");
const ZOOM_IN: &str = b2!("16", "view.zoom-in");
const ZOOM_OUT: &str = b2!("16", "view.zoom-out");
const FIT: &str = b2!("16", "view.fit");
const GRID: &str = b2!("24", "view.grid");
const LEFT_LARGE: &str = b2!("24", "panel.left");
const RIGHT_LARGE: &str = b2!("24", "panel.right");
const SETTINGS_LARGE: &str = b2!("24", "ui.settings");
const EXPORT: &str = b2!("24", "file.export");
const PRINT: &str = b2!("24", "file.print");
const TABLE: &str = b2!("24", "data.table");
const CHART: &str = b2!("24", "data.chart");
const ADD_ITEM: &str = b2!("24", "budget.add-item");
const ADD_CHAPTER: &str = b2!("24", "budget.add-chapter");
const RECALC: &str = b2!("24", "calculation.recalculate");
const AUDIT: &str = b2!("24", "calculation.audit");
const REPORT: &str = b2!("24", "report.generate");
const REPORT_DOC: &str = b2!("24", "report.document");
const FOLDER_NEW: &str = b2!("24", "project.folder-new");
const SETTINGS: &str = b2!("16", "ui.settings");
const HELP: &str = b2!("16", "ui.help");
const CLOSE: &str = b2!("16", "window.close");
const MINIMIZE: &str = b2!("16", "window.minimize");
const MAXIMIZE: &str = b2!("16", "window.maximize");
const EXPAND: &str = b2!("16", "tree.expand");
const COLLAPSE: &str = b2!("16", "tree.collapse");
const FOLDER: &str = b2!("16", "project.folder");
const FOLDER_LARGE: &str = b2!("24", "project.folder");
const ITEM: &str = b2!("16", "data.table");
const SEARCH: &str = b2!("16", "view.search");
const PANEL_LEFT: &str = b2!("16", "panel.left");
const PANEL_RIGHT: &str = b2!("16", "panel.right");
const SAVE_SMALL: &str = b2!("16", "file.save");
const UNDO_SMALL: &str = b2!("16", "edit.undo");
const BACK: &str = b2!("16", "nav.back");
const ERROR: &str = b2!("16", "status.error");
const WARNING: &str = b2!("16", "status.warning");
const SUCCESS: &str = b2!("16", "status.success");
const INFO: &str = b2!("16", "status.info");
const HOME: &str = b2!("16", "nav.home");
const INSTALL: &str = b2!("16", "software.install");
const UPDATE: &str = b2!("16", "software.update");
const LAUNCH: &str = b2!("16", "software.launch");
const WEBTAB: &str = b2!("16", "software.open-webtab");
const EXTERNAL: &str = b2!("16", "link.open-external");
const CHECK_UPDATES: &str = b2!("16", "ui.check-updates");
const WEB_RELOAD: &str = b2!("16", "view.web-reload");
const REDO_SMALL: &str = b2!("16", "edit.redo");
const TABLE_SMALL: &str = b2!("16", "data.table");
const RESTORE: &str = b2!("16", "window.restore");
const MENU: &str = b2!("16", "nav.page-menu");
const CHECK: &str = b2!("16", "status.success");
const WINDOW_ICONS: WindowIcons = WindowIcons { minimize: MINIMIZE, maximize: MAXIMIZE, restore: RESTORE, close: CLOSE };
const NEW_SMALL: &str = b2!("16", "file.new");
const OPEN_SMALL: &str = b2!("16", "file.open");
const OPEN_LARGE: &str = b2!("24", "file.open");
const EXPORT_SMALL: &str = b2!("16", "file.export");
const PRINT_SMALL: &str = b2!("16", "file.print");
const NEXT: &str = b2!("16", "nav.forward");
const DONE: &str = b2!("16", "status.success");
const HOUSING: &str = b2!("24", "building.housing");
const DETACHED: &str = b2!("24", "building.new-housing");
const APARTMENT: &str = b2!("24", "building.apartment");
const UTILITY: &str = b2!("24", "building.office");
const S_PROJECT: &str = b2!("16", "project.folder");
const S_BUILDING: &str = b2!("16", "building.housing");
const S_SHELL: &str = b2!("16", "thermal.window");
const S_SYSTEMS: &str = b2!("16", "energy.heat-pump");
const S_RESULT: &str = b2!("16", "thermal.results");

/// The groups of the shortcuts page, by command id prefix.
const COMMAND_GROUPS: [(&str, &str); 8] = [
    ("file", "Bestand"),
    ("doc", "Document"),
    ("edit", "Bewerken"),
    ("insert", "Invoegen"),
    ("view", "Weergave"),
    ("calc", "Berekenen"),
    ("report", "Rapport"),
    ("app", "Programma"),
];

const TABS: [&str; 5] = ["Start", "Invoegen", "Berekenen", "Weergave", "Rapport"];
const UNITS: [&str; 5] = ["st", "m", "m²", "m³", "kg"];
const FORMATS: [&str; 3] = ["PDF", "Excel", "IFC"];
const SECTIONS: [Section<'static>; 5] = [
    Section { icon: S_PROJECT, label: "Project" },
    Section { icon: S_BUILDING, label: "Gebouw" },
    Section { icon: S_SHELL, label: "Schil" },
    Section { icon: S_SYSTEMS, label: "Installaties" },
    Section { icon: S_RESULT, label: "Resultaat" },
];
const BUILDING_TYPES: [(&str, &str, &str); 4] = [
    (HOUSING, "Rijwoning", "Tussen- of hoekwoning in een rij"),
    (DETACHED, "Vrijstaand", "Woning met vier gevels"),
    (APARTMENT, "Appartement", "Woning in een gebouw met meer woningen"),
    (UTILITY, "Utiliteit", "Kantoor, school of winkel"),
];
const HEATING: [&str; 4] = ["Warmtepomp", "Hybride warmtepomp", "Cv-ketel", "Warmtenet"];
const VENTILATION: [&str; 3] = ["Natuurlijke toevoer, mechanische afvoer", "Gebalanceerd met warmteterugwinning", "Natuurlijk"];
macro_rules! preview {
    ($name:literal) => {
        // Cropped, rounded and faded by scripts/crop_installer_previews.py.
        Some(include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"), "/design/ontwerp-0.4/installer-previews/", $name, ".png")) as &'static [u8])
    };
}

/// A tool in the installer, as in proposal E (design/ontwerp-0.4/installer-voorstellen.html):
/// the catalogue of openaec-installer at 8b39bae with disciplines, website status,
/// versions and commit counts from open-aec.com (read 2026-10-22).
struct Tool {
    name: &'static str,
    category: &'static str,
    icon: &'static str,
    /// A web tool: no installation.
    web: bool,
    preview: Option<&'static [u8]>,
    /// The tool's own logo; otherwise the category icon, as in the real installer.
    logo: Option<&'static [u8]>,
    /// Has a web version that can open in the installer.
    web_url: Option<&'static str>,
    repo: Option<&'static str>,
    /// Disciplines of the website: Architecture, Engineering, Construction, Infra & GWW.
    disc: &'static str,
    /// Website status, such as Beta or In ontwikkeling.
    site: &'static str,
    latest: &'static str,
    commits: u32,
    description: &'static str,
}

const CAT_CALC: &str = b2!("24", "data.table");
const CAT_CAD: &str = b2!("24", "draw.polyline");
const CAT_STRUCT: &str = b2!("24", "frame.calculation");
const CAT_GEO: &str = b2!("24", "geo.sondering");
const CAT_BIM: &str = b2!("24", "ifc.validate");
const CAT_PLAN: &str = b2!("24", "planning.gantt");
const CAT_DOCS: &str = b2!("24", "report.document");
const CAT_AI: &str = b2!("24", "audio.speech");
const CAT_ENERGY: &str = b2!("24", "energy.fetch-label");
const CAT_FIELD: &str = b2!("24", "field.list");
const CAT_GIS: &str = b2!("24", "geo.coordinate-tag");
const ENERGY_LOGO: &[u8] = include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"), "/harmonization/references/openaec-installer/public/logos/open-energy-studio.png"));
/// The GitHub mark, as on the real installer's GitHub button (Octicons, MIT).
const GITHUB: &str = r#"<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>"#;

#[allow(clippy::too_many_arguments)]
const fn tool(
    name: &'static str,
    category: &'static str,
    icon: &'static str,
    web: bool,
    preview: Option<&'static [u8]>,
    web_url: Option<&'static str>,
    repo: Option<&'static str>,
    disc: &'static str,
    site: &'static str,
    latest: &'static str,
    commits: u32,
    description: &'static str,
) -> Tool {
    Tool { name, category, icon, web, preview, logo: None, web_url, repo, disc, site, latest, commits, description }
}

const TOOLS: [Tool; 18] = [
    tool("Open Calc Studio", "Calculatie", CAT_CALC, false, preview!("open-calc-studio"), Some("open-calc-studio.open-aec.com"), Some("OpenAEC-Foundation/open-calc-studio"), "CI", "", "0.13", 96, "Open source calculatie en begroting voor de bouwsector, met AI-assistent."),
    tool("Open PDF Studio", "Documenten", CAT_DOCS, false, preview!("open-pdf-studio"), Some("open-pdf-studio.open-aec.com"), Some("OpenAEC-Foundation/open-pdf-studio"), "AECI", "", "2026.43", 1459, "PDF's bekijken, bewerken en annoteren, gericht op bouwdocumentatie en tekeningen."),
    tool("Open Planner Studio", "Planning", CAT_PLAN, false, preview!("open-planner-studio"), Some("open-planner-studio.open-aec.com"), Some("OpenAEC-Foundation/open-planner-studio"), "ACI", "Beta", "2026.10", 4569, "Open source projectplanning en werkcoördinatie voor bouwprojecten."),
    tool("Open 2D Studio", "CAD", CAT_CAD, false, preview!("open-2d-studio"), Some("open-2d-studio.open-aec.com"), Some("OpenAEC-Foundation/open-2d-studio"), "AEC", "", "0.6", 0, "2D tekeningen en documenten bekijken en bewerken."),
    tool("Open CAD Studio", "CAD", CAT_CAD, false, preview!("open-cad-studio"), Some("hakanseven12.github.io/OpenCADStudio"), Some("HakanSeven12/OpenCADStudio"), "AEC", "Community", "2026.42", 5516, "Volwaardige 2D + 3D CAD-applicatie met DWG/DXF-ondersteuning."),
    tool("Open Calculations Studio", "Constructief", CAT_STRUCT, false, preview!("open-calculations-studio"), Some("open-calculations-studio.open-aec.com"), Some("OpenAEC-Foundation/Open-Calculations-Studio"), "EI", "In ontwikkeling", "2026.39", 306, "Constructieve handberekeningen met CalcPAD-syntax, herleidbaar en deelbaar."),
    tool("Open Frame Studio", "Constructief", CAT_STRUCT, false, None, None, Some("OpenAEC-Foundation/open-frame-studio"), "AC", "Alpha", "0.6", 122, "Parametrisch kozijn- en raamwerkontwerp voor de bouw."),
    tool("Open Geotechniek Studio", "Geotechniek", CAT_GEO, false, preview!("open-geotechniek-studio"), Some("open-geotechniek-studio.open-aec.com"), Some("OpenAEC-Foundation/open-geotechniek-studio"), "EI", "Beta", "0.4", 218, "Viewer voor sonderingen: CPT's in GEF- en BRO-XML-formaat."),
    tool("Monty IFC Viewer", "BIM", CAT_BIM, false, preview!("monty-ifc-viewer"), Some("monty-ifc-viewer.open-aec.com"), Some("OpenAEC-Foundation/monty-ifc-viewer"), "C", "Beta", "1.0", 50, "Open source IFC-viewer voor BIM-modellen, ook op de bouwplaats."),
    tool("Open Speech Studio", "AI", CAT_AI, false, preview!("open-speech-studio"), None, Some("OpenAEC-Foundation/open-speech-studio"), "AECI", "Beta", "0.12", 93, "Lokale spraak-naar-tekst en vergadernotities, 100% op je eigen machine."),
    tool("Open Field Studio", "Veld", CAT_FIELD, false, preview!("open-field-studio"), Some("open-field-studio.open-aec.com"), Some("OpenAEC-Foundation/Open-Field-Studio"), "C", "Beta", "0.3", 35, "Inspecties, opleveringen en kwaliteitsborging met checklists."),
    tool("Open Pointcloud Studio", "BIM", CAT_BIM, false, preview!("open-pointcloud-studio"), Some("open-pointcloud-studio.open-aec.com"), Some("OpenAEC-Foundation/open-pointcloud-studio"), "ECI", "Beta", "0.9", 432, "Pointcloud-viewer voor renovatie en analyse."),
    tool("Open STL-3DMap Studio", "GIS", CAT_GIS, false, None, None, Some("OpenAEC-Foundation/Open-STL-3DMap-Studio"), "I", "", "0.2", 0, "3D-printbare meerkleuren stadskaarten van Nederland op basis van 3DBAG en BGT."),
    Tool {
        logo: Some(ENERGY_LOGO),
        ..tool("Open Energy Studio", "Energie", CAT_ENERGY, true, preview!("open-energy-studio"), Some("open-energy-studio.open-aec.com"), None, "E", "Beta", "", 0, "Energieprestatie volgens NTA 8800: BENG, energielabel en TOjuli.")
    },
    tool("Open Heatloss Studio", "Energie", CAT_ENERGY, true, preview!("open-heatloss-studio"), Some("open-heatloss-studio.open-aec.com"), None, "E", "Beta", "", 693, "Warmteverliesberekeningen volgens NEN-EN 12831 / ISSO 51."),
    tool("Open Books Studio", "Documenten", CAT_DOCS, true, preview!("open-books"), Some("open-books.open-aec.com"), None, "A", "In ontwikkeling", "", 113, "Digitalisering van historische bouwliteratuur."),
    tool("Open BIM Validator Studio", "BIM", CAT_BIM, true, preview!("open-bim-validator"), Some("open-aec.com/bim-validator"), Some("OpenAEC-Foundation/OpenAEC-BIM-validator"), "", "", "", 75, "Valideer IFC-modellen tegen IDS, NL-BIM Basis ILS en de RVB BIM Norm."),
    tool("Pile Plan Studio", "Constructief", CAT_STRUCT, true, None, Some("pile-plan-studio.open-aec.com"), Some("OpenAEC-Foundation/pile-plan-studio"), "EI", "Beta", "", 406, "Funderingspalenplannen opstellen en beheren, met technische uitvoer."),
];

/// Disciplines of the website's ecosystem filter.
const DISCIPLINES: [(char, &str); 4] = [('A', "Architecture"), ('E', "Engineering"), ('C', "Construction"), ('I', "Infra & GWW")];

/// Decoded once: iced gives every new image handle a new id, which would decode
/// the picture again on every view.
fn preview_handle(i: usize) -> Option<iced::widget::image::Handle> {
    use std::sync::OnceLock;
    static HANDLES: OnceLock<Vec<Option<iced::widget::image::Handle>>> = OnceLock::new();
    HANDLES.get_or_init(|| TOOLS.iter().map(|t| t.preview.map(iced::widget::image::Handle::from_bytes)).collect())[i].clone()
}

fn logo_handle(i: usize) -> Option<iced::widget::image::Handle> {
    use std::sync::OnceLock;
    static HANDLES: OnceLock<Vec<Option<iced::widget::image::Handle>>> = OnceLock::new();
    HANDLES.get_or_init(|| TOOLS.iter().map(|t| t.logo.map(iced::widget::image::Handle::from_bytes)).collect())[i].clone()
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
enum Filter {
    #[default]
    All,
    Installed,
    Updates,
    Web,
}

#[derive(Debug, Clone, Default)]
struct ToolState {
    installed: Option<&'static str>,
    progress: Option<f32>,
}

/// A filter choice in the icon view: `None` is everything.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Choice {
    key: Option<&'static str>,
    label: &'static str,
}

impl std::fmt::Display for Choice {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.label)
    }
}

/// Display names of the app features of `openaec-icons`.
fn app_name(feature: &str) -> &'static str {
    match feature {
        "calc" => "Calc",
        "calculations" => "Calculations",
        "composer" => "Workspace Composer",
        "energy" => "Energy",
        "field" => "Field",
        "frame" => "Frame",
        "geotechniek" => "Geotechniek",
        "heatloss" => "Heatloss",
        "installer" => "Installer",
        "pdf" => "PDF",
        "pile-plan" => "Pile Plan",
        "planner" => "Planner",
        "pointcloud" => "Pointcloud",
        "reports" => "Reports",
        "speech" => "Speech",
        "validator" => "BIM Validator",
        _ => "Onbekend",
    }
}

/// The app choices, alphabetical by display name, after "Alle apps".
fn app_choices() -> &'static [Choice] {
    static LIST: OnceLock<Vec<Choice>> = OnceLock::new();
    LIST.get_or_init(|| {
        let mut list: Vec<Choice> = openaec_icons::APPS.iter().map(|&a| Choice { key: Some(a), label: app_name(a) }).collect();
        list.sort_by_key(|c| c.label);
        list.insert(0, Choice { key: None, label: "Alle apps" });
        list
    })
}

/// The group choices of the B2 set, alphabetical, after "Alle groepen".
fn group_choices() -> &'static [Choice] {
    static LIST: OnceLock<Vec<Choice>> = OnceLock::new();
    LIST.get_or_init(|| {
        let mut groups: Vec<&'static str> = Icon::all().iter().map(|i| i.group()).collect();
        groups.sort_unstable();
        groups.dedup();
        std::iter::once(Choice { key: None, label: "Alle groepen" }).chain(groups.into_iter().map(|g| Choice { key: Some(g), label: g })).collect()
    })
}

/// Icons per page, so a page lays out quickly even with all 945 icons.
const ICONS_PER_PAGE: usize = 120;

fn icon_grid_id() -> iced::widget::Id {
    iced::widget::Id::new("icon-grid")
}

fn icon_grid_to_top() -> Task<Msg> {
    iced::widget::operation::snap_to(icon_grid_id(), scrollable::RelativeOffset::START)
}

/// State of the icon view: every B2 icon from the `openaec-icons` crate.
struct Icons {
    search: String,
    app: Choice,
    group: Choice,
    large: bool,
    page: usize,
    selected: Option<Icon>,
}

impl Default for Icons {
    fn default() -> Self {
        Self { search: String::new(), app: app_choices()[0], group: group_choices()[0], large: true, page: 0, selected: None }
    }
}

impl Icons {
    /// The icons that match the search text, app and group.
    fn matches(&self) -> Vec<Icon> {
        let needle = self.search.trim().to_lowercase();
        Icon::all()
            .into_iter()
            .filter(|i| self.app.key.map_or(true, |a| i.apps().contains(&a)))
            .filter(|i| self.group.key.map_or(true, |g| i.group() == g))
            .filter(|i| needle.is_empty() || i.label().to_lowercase().contains(&needle) || i.id().contains(&needle) || i.group().to_lowercase().contains(&needle))
            .collect()
    }
}

/// State of the sample installer.
struct Installer {
    tools: Vec<ToolState>,
    tabs: Vec<usize>,
    active: Option<usize>,
    search: String,
    filter: Filter,
    disc: Option<char>,
    feature: usize,
    refreshing: bool,
    last_refresh: String,
    self_version: &'static str,
    self_update: Option<f32>,
    self_dismissed: bool,
}

impl Default for Installer {
    fn default() -> Self {
        // Calc, Planner, Geotechniek, Speech and Pointcloud are current; PDF and Calculations have an update.
        let mut installed: [Option<&'static str>; 18] = [None; 18];
        for (i, v) in [(0, "0.13"), (1, "2026.40"), (2, "2026.10"), (5, "2026.35"), (7, "0.4"), (9, "0.12"), (11, "0.9")] {
            installed[i] = Some(v);
        }
        Self {
            tools: installed.into_iter().map(|installed| ToolState { installed, progress: None }).collect(),
            tabs: Vec::new(),
            active: None,
            search: String::new(),
            filter: Filter::All,
            disc: None,
            feature: 0,
            refreshing: false,
            last_refresh: "10:42".into(),
            self_version: "1.5.0",
            self_update: None,
            self_dismissed: false,
        }
    }
}

impl Installer {
    fn has_update(&self, i: usize) -> bool {
        !TOOLS[i].web && self.tools[i].progress.is_none() && self.tools[i].installed.is_some_and(|v| v != TOOLS[i].latest)
    }

    fn passes(&self, i: usize, filter: Filter) -> bool {
        match filter {
            Filter::All => true,
            Filter::Installed => self.tools[i].installed.is_some(),
            Filter::Updates => self.has_update(i),
            Filter::Web => TOOLS[i].web,
        }
    }

    fn count(&self, filter: Filter) -> usize {
        (0..TOOLS.len()).filter(|&i| self.passes(i, filter)).count()
    }

    /// Tools in the featured block: updates first, then a few with a screenshot.
    fn featured(&self) -> Vec<usize> {
        let mut list: Vec<usize> = (0..TOOLS.len()).filter(|&i| self.has_update(i) && TOOLS[i].preview.is_some()).collect();
        for i in [0, 2, 13, 11] {
            if !list.contains(&i) {
                list.push(i);
            }
        }
        list
    }
}

fn after<T: Send + 'static>(millis: u64, value: T) -> Task<T> {
    Task::perform(
        async move {
            std::thread::sleep(Duration::from_millis(millis));
            value
        },
        |v| v,
    )
}

const RECENT_FILES: [(&str, &str, &str); 4] = [
    ("Kade 12 begroting.oaec", "Projecten/Kade 12", "vandaag"),
    ("Brugweg 4 variant B.oaec", "Projecten/Brugweg 4", "gisteren"),
    ("Prijslijst 2026.xlsx", "Bibliotheek", "14 okt"),
    ("Havenkade fase 2.oaec", "Projecten/Havenkade", "12 okt"),
];
const CHAPTERS: [(&str, &str); 5] = [("21", "21 Fundering"), ("22", "22 Vloeren"), ("23", "23 Gevels"), ("24", "24 Daken"), ("30", "30 Installaties")];
const PROJECTS: [(&str, &str, &str); 4] = [
    ("Kade 12", "Woningbouw · 6 posten", "vandaag"),
    ("Brugweg 4", "Utiliteitsbouw · 48 posten", "gisteren"),
    ("Havenkade fase 2", "Woningbouw · 112 posten", "12 okt"),
    ("Schoolplein 1", "Renovatie · 31 posten", "3 okt"),
];
const BUDGET_COLUMNS: [TableColumn<'static>; 5] = [
    TableColumn { title: "Code", width: Length::Fixed(64.0), numeric: false },
    TableColumn { title: "Omschrijving", width: Length::Fill, numeric: false },
    TableColumn { title: "Hoeveelheid", width: Length::Fixed(110.0), numeric: true },
    TableColumn { title: "Prijs", width: Length::Fixed(100.0), numeric: true },
    TableColumn { title: "Bedrag", width: Length::Fixed(110.0), numeric: true },
];
const QUANTITY_COLUMNS: [TableColumn<'static>; 4] = [
    TableColumn { title: "Code", width: Length::Fixed(64.0), numeric: false },
    TableColumn { title: "Omschrijving", width: Length::Fill, numeric: false },
    TableColumn { title: "Hoeveelheid", width: Length::Fixed(110.0), numeric: true },
    TableColumn { title: "Eenheid", width: Length::Fixed(80.0), numeric: false },
];

/// Dutch number: thousands with a dot, decimals with a comma.
fn nl(value: f64, decimals: usize) -> String {
    let raw = format!("{:.*}", decimals, value.abs());
    let (int, frac) = raw.split_once('.').map_or((raw.as_str(), ""), |(a, b)| (a, b));
    let mut grouped = String::new();
    for (i, ch) in int.chars().enumerate() {
        if i > 0 && (int.len() - i) % 3 == 0 {
            grouped.push('.');
        }
        grouped.push(ch);
    }
    let sign = if value < 0.0 { "-" } else { "" };
    if frac.is_empty() { format!("{sign}{grouped}") } else { format!("{sign}{grouped},{frac}") }
}

fn euro(value: f64) -> String {
    format!("€ {}", nl(value, 2))
}

fn parse_nl(input: &str) -> Option<f64> {
    input.trim().replace('.', "").replace(',', ".").parse().ok()
}

#[derive(Debug, Clone, PartialEq)]
struct Item {
    id: u32,
    code: String,
    name: String,
    quantity: f64,
    unit: &'static str,
    price: f64,
    include: bool,
}

impl Item {
    fn amount(&self) -> f64 {
        if self.include { self.quantity * self.price } else { 0.0 }
    }
    fn chapter(&self) -> &str {
        self.code.split('.').next().unwrap_or("")
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DocKind {
    Budget,
    Quantities,
    Chart,
    Report,
    Item(u32),
    Blank(u32),
}

#[derive(Debug, Clone)]
struct Doc {
    kind: DocKind,
    title: String,
    dirty: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum TreeSel {
    Root,
    Chapter(&'static str),
    Item(u32),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Dialog {
    Settings,
    Export,
    Print,
    CloseDirty(usize),
    Quit,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum MenuKind {
    Row(u32),
    Tree(TreeSel),
    Tab(usize),
    App,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Side {
    Left,
    Right,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
enum FilePage {
    #[default]
    Open,
    New,
}

/// The tabs of the settings dialog.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SettingsPage {
    General,
    Shortcuts,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
enum View {
    #[default]
    Screen,
    Workflow,
    Installer,
    Components,
    Icons,
}

#[derive(Debug, Clone)]
enum Msg {
    Theme(ThemeId),
    Workspace(WorkspaceSetting),
    Statusbar(StatusbarSetting),
    View(View),
    RibbonTab(usize),
    Backstage(bool),
    OpenProject(usize),
    SelectDoc(usize),
    CloseDoc(usize),
    OpenDoc(DocKind),
    Tree(TreeSel),
    ToggleRoot,
    ToggleChapter(&'static str),
    SelectRow(u32),
    New,
    Save,
    Undo,
    Redo,
    Cut,
    Copy,
    Paste,
    Delete,
    AddItem,
    AddChapter,
    Recalculate,
    Audit,
    CloseBanner,
    ZoomIn,
    ZoomOut,
    ZoomFit,
    ToggleGrid,
    ToggleLeft,
    ToggleRight,
    GenerateReport,
    Dialog(Option<Dialog>),
    Format(&'static str),
    Landscape(bool),
    ConfirmExport,
    ConfirmPrint,
    DiscardAndClose(usize),
    SaveAndClose(usize),
    EditName(String),
    EditUnit(&'static str),
    EditQuantity(String),
    EditPrice(String),
    EditInclude(bool),
    CloseToast,
    ToastExpired(u32),
    Escape,
    Enter,
    Restart,
    SkipStart(bool),
    Cursor(Point),
    WindowResized(Size),
    TitlePress,
    Minimize,
    Maximize,
    CloseWindow,
    QuitNow,
    SaveAndQuit,
    DragSplit(Side),
    EndDrag,
    Menu(Option<MenuKind>),
    OpenItem(u32),
    CloseOthers(usize),
    CloseAll,
    CloseActive,
    FilePage(FilePage),
    // Workflow app
    WfSection(usize),
    WfNavigation(Navigation),
    WfNext,
    WfPrevious,
    WfProject(String),
    WfAddress(String),
    WfType(usize),
    WfYear(String),
    WfArea(String),
    WfRcWall(String),
    WfRcRoof(String),
    WfRcFloor(String),
    WfWindowU(String),
    WfHeating(&'static str),
    WfVentilation(&'static str),
    WfSolar(bool),
    WfPanels(f32),
    WfCalculate,
    // Installer
    InstTab(Option<usize>),
    InstOpenWeb(usize),
    InstInstall(usize),
    InstTick(usize),
    InstLaunch(usize),
    InstSearch(String),
    InstFilter(Filter),
    InstGitHub(usize),
    InstUpdateAll,
    InstDisc(Option<char>),
    InstFeature(usize),
    InstFeatureTick,
    IconSearch(String),
    IconApp(Choice),
    IconGroup(Choice),
    IconLarge(bool),
    IconPage(usize),
    IconSelect(Icon),
    InstRefresh,
    InstRefreshDone,
    InstSelfUpdate,
    InstSelfTick,
    InstDismissSelf,
    // Component sheet
    Check(bool),
    Switch(bool),
    Radio(u8),
    Slider(f32),
    Name(String),
    Unit(&'static str),
    Noop,
    Navigate(openaec_ui::keyboard::Navigation),
    Key(openaec_ui::keyboard::KeyPress),
    Shortcuts(sc::Message),
    SettingsPage(SettingsPage),
}

/// State of the sample workflow app: an energy label in five sections.
struct Workflow {
    section: usize,
    navigation: Navigation,
    visited: [bool; 5],
    project: String,
    address: String,
    kind: usize,
    year: String,
    area: String,
    rc_wall: String,
    rc_roof: String,
    rc_floor: String,
    window_u: String,
    heating: &'static str,
    ventilation: &'static str,
    solar: bool,
    panels: f32,
    calculated: bool,
}

impl Default for Workflow {
    fn default() -> Self {
        Self {
            section: 0,
            navigation: Navigation::Sidebar,
            visited: [true, false, false, false, false],
            project: "Kade 12".into(),
            address: "Kade 12, 3011 AA Rotterdam".into(),
            kind: 0,
            year: "1978".into(),
            area: "124".into(),
            rc_wall: "2,5".into(),
            rc_roof: "3,5".into(),
            rc_floor: "2,0".into(),
            window_u: "1,4".into(),
            heating: "Hybride warmtepomp",
            ventilation: "Natuurlijke toevoer, mechanische afvoer",
            solar: true,
            panels: 8.0,
            calculated: false,
        }
    }
}

impl Workflow {
    /// A rough primary energy use in kWh/m² per year, for the review only.
    fn energy(&self) -> f64 {
        let rc = |s: &str| parse_nl(s).unwrap_or(1.0).max(0.3);
        let shell = 40.0 / rc(&self.rc_wall) + 30.0 / rc(&self.rc_roof) + 20.0 / rc(&self.rc_floor) + 25.0 * parse_nl(&self.window_u).unwrap_or(2.0);
        let heating = match self.heating {
            "Warmtepomp" => 0.45,
            "Hybride warmtepomp" => 0.7,
            "Warmtenet" => 0.8,
            _ => 1.0,
        };
        let ventilation = if self.ventilation.starts_with("Gebalanceerd") { 0.85 } else { 1.0 };
        let kind = [1.0, 1.15, 0.85, 1.1][self.kind];
        let solar = if self.solar { f64::from(self.panels) * 6.0 } else { 0.0 };
        (shell * heating * ventilation * kind - solar).max(0.0)
    }

    fn label(&self) -> &'static str {
        match self.energy() {
            e if e < 50.0 => "A+++",
            e if e < 75.0 => "A++",
            e if e < 105.0 => "A+",
            e if e < 160.0 => "A",
            e if e < 190.0 => "B",
            e if e < 250.0 => "C",
            _ => "D",
        }
    }
}

struct Toast {
    id: u32,
    tone: Tone,
    title: String,
    message: String,
}

struct Gallery {
    theme: ThemeId,
    workspace: WorkspaceSetting,
    statusbar: StatusbarSetting,
    view: View,
    ribbon_tab: usize,
    backstage: bool,
    project: usize,
    docs: Vec<Doc>,
    active: usize,
    blank_count: u32,
    items: Vec<Item>,
    next_id: u32,
    history: Vec<Vec<Item>>,
    future: Vec<Vec<Item>>,
    clipboard: Option<Item>,
    tree: TreeSel,
    root_open: bool,
    open_chapters: HashSet<&'static str>,
    selected: Option<u32>,
    quantity_text: String,
    price_text: String,
    banner: Option<(Tone, String)>,
    toast: Option<Toast>,
    toast_count: u32,
    dialog: Option<Dialog>,
    format: &'static str,
    landscape: bool,
    zoom: u16,
    grid: bool,
    show_left: bool,
    show_right: bool,
    report_ready: bool,
    started: bool,
    skip_start: bool,
    cursor: Point,
    window: Size,
    maximized: bool,
    last_title_press: Option<Instant>,
    left_width: f32,
    right_width: f32,
    drag: Option<(Side, f32, f32)>,
    menu: Option<(MenuKind, Point)>,
    file_page: FilePage,
    wf: Workflow,
    inst: Installer,
    icons: Icons,
    /// The shortcuts someone set (issue #22), and the page that changes them.
    keymap: Keymap,
    shortcuts: sc::Editor,
    /// Where the keymap is saved; `None` in tests, so they never write a file.
    keymap_path: Option<std::path::PathBuf>,
    settings_page: SettingsPage,
    // Component sheet
    check: bool,
    switch: bool,
    radio: Option<u8>,
    slider: f32,
    name: String,
    unit: Option<&'static str>,
}

impl Default for Gallery {
    fn default() -> Self {
        let rows: [(&str, &str, f64, &'static str, f64); 6] = [
            ("21.10", "Funderingsbalken", 38.4, "m³", 240.0),
            ("21.20", "Poeren", 12.0, "st", 245.0),
            ("22.10", "Breedplaatvloer", 164.0, "m²", 70.0),
            ("22.20", "Druklaag", 164.0, "m²", 0.0),
            ("23.10", "Kalkzandsteen", 212.5, "m²", 70.0),
            ("23.20", "Spouwisolatie", 212.5, "m²", 0.0),
        ];
        let items: Vec<Item> = rows
            .iter()
            .enumerate()
            .map(|(i, (code, name, quantity, unit, price))| Item { id: i as u32 + 1, code: code.to_string(), name: name.to_string(), quantity: *quantity, unit, price: *price, include: true })
            .collect();
        let mut gallery = Self {
            theme: ThemeId::Light,
            workspace: WorkspaceSetting::Theme,
            statusbar: StatusbarSetting::Theme,
            view: View::Screen,
            ribbon_tab: 0,
            backstage: false,
            project: 0,
            docs: vec![
                Doc { kind: DocKind::Budget, title: "Begroting".into(), dirty: false },
                Doc { kind: DocKind::Quantities, title: "Hoeveelheden".into(), dirty: false },
                Doc { kind: DocKind::Report, title: "Rapport".into(), dirty: false },
            ],
            active: 0,
            blank_count: 0,
            next_id: items.len() as u32 + 1,
            items,
            history: Vec::new(),
            future: Vec::new(),
            clipboard: None,
            tree: TreeSel::Item(3),
            root_open: true,
            open_chapters: ["21", "22"].into_iter().collect(),
            selected: None,
            quantity_text: String::new(),
            price_text: String::new(),
            banner: None,
            toast: None,
            toast_count: 0,
            dialog: None,
            format: "PDF",
            landscape: false,
            zoom: 100,
            grid: true,
            show_left: true,
            show_right: true,
            report_ready: false,
            started: false,
            skip_start: false,
            cursor: Point::ORIGIN,
            window: Size::new(1280.0, 800.0),
            maximized: false,
            last_title_press: None,
            left_width: 240.0,
            right_width: 240.0,
            drag: None,
            menu: None,
            file_page: FilePage::Open,
            wf: Workflow::default(),
            inst: Installer::default(),
            icons: Icons::default(),
            keymap: Keymap::default(),
            shortcuts: sc::Editor::default(),
            keymap_path: None,
            settings_page: SettingsPage::General,
            check: true,
            switch: true,
            radio: Some(1),
            slider: 0.6,
            name: "Kade 12".into(),
            unit: Some("m³"),
        };
        gallery.select(Some(3));
        gallery.banner = gallery.missing_prices();
        gallery
    }
}

impl Gallery {
    fn look(&self) -> Look {
        Look::new(self.theme, self.workspace, self.statusbar)
    }

    fn item(&self, id: u32) -> Option<&Item> {
        self.items.iter().find(|i| i.id == id)
    }

    fn select(&mut self, id: Option<u32>) {
        self.selected = id;
        if let Some((quantity, price, item_id)) = id.and_then(|id| self.item(id)).map(|i| (i.quantity, i.price, i.id)) {
            self.quantity_text = nl(quantity, 1);
            self.price_text = nl(price, 2);
            self.tree = TreeSel::Item(item_id);
        }
    }

    fn total(&self) -> f64 {
        self.items.iter().map(Item::amount).sum()
    }

    fn missing_prices(&self) -> Option<(Tone, String)> {
        let n = self.items.iter().filter(|i| i.include && i.price == 0.0).count();
        match n {
            0 => None,
            1 => Some((Tone::Warning, "Eén post heeft nog geen prijs.".into())),
            n => Some((Tone::Warning, format!("{n} posten hebben nog geen prijs."))),
        }
    }

    /// Record the current posts before a change, for undo.
    fn remember(&mut self) {
        self.history.push(self.items.clone());
        if self.history.len() > 200 {
            self.history.remove(0);
        }
        self.future.clear();
        for doc in &mut self.docs {
            if matches!(doc.kind, DocKind::Budget | DocKind::Quantities | DocKind::Item(_)) {
                doc.dirty = true;
            }
        }
    }

    fn toast(&mut self, tone: Tone, title: &str, message: impl Into<String>) -> Task<Msg> {
        self.toast_count += 1;
        let id = self.toast_count;
        self.toast = Some(Toast { id, tone, title: title.into(), message: message.into() });
        if tone == Tone::Error {
            // An error stays until it is closed (besluit 3).
            return Task::none();
        }
        Task::perform(
            async move {
                std::thread::sleep(Duration::from_secs(5));
                id
            },
            Msg::ToastExpired,
        )
    }

    fn open_doc(&mut self, kind: DocKind) {
        if let Some(i) = self.docs.iter().position(|d| d.kind == kind) {
            self.active = i;
            return;
        }
        let title = match kind {
            DocKind::Budget => "Begroting".to_string(),
            DocKind::Quantities => "Hoeveelheden".to_string(),
            DocKind::Chart => "Grafiek".to_string(),
            DocKind::Report => "Rapport".to_string(),
            DocKind::Item(id) => self.item(id).map_or("Post".into(), |i| format!("{} {}", i.code, i.name)),
            DocKind::Blank(n) => format!("Naamloos {n}"),
        };
        self.docs.push(Doc { kind, title, dirty: false });
        self.active = self.docs.len() - 1;
    }

    fn close_doc(&mut self, i: usize) {
        if i < self.docs.len() {
            self.docs.remove(i);
            if self.active >= self.docs.len() {
                self.active = self.docs.len().saturating_sub(1);
            } else if self.active > i {
                self.active -= 1;
            }
        }
    }

    fn next_code(&self, chapter: &str) -> String {
        let last = self
            .items
            .iter()
            .filter(|i| i.chapter() == chapter)
            .filter_map(|i| i.code.split('.').nth(1).and_then(|n| n.parse::<u32>().ok()))
            .max()
            .unwrap_or(0);
        format!("{chapter}.{}", last + 10)
    }

    fn insert_item(&mut self, mut item: Item) -> u32 {
        item.id = self.next_id;
        self.next_id += 1;
        let at = self.selected.and_then(|id| self.items.iter().position(|i| i.id == id)).map_or(self.items.len(), |p| p + 1);
        let id = item.id;
        self.open_chapters.insert(CHAPTERS.iter().find(|(k, _)| *k == item.chapter()).map_or("21", |(k, _)| k));
        self.items.insert(at.min(self.items.len()), item);
        self.items.sort_by(|a, b| a.code.cmp(&b.code));
        self.select(Some(id));
        id
    }

    fn update(&mut self, message: Msg) -> Task<Msg> {
        if !matches!(message, Msg::Cursor(_) | Msg::Menu(_) | Msg::WindowResized(_) | Msg::Noop) {
            self.menu = None;
        }
        match message {
            Msg::Theme(t) => self.theme = t,
            Msg::Workspace(s) => self.workspace = s,
            Msg::Statusbar(s) => self.statusbar = s,
            Msg::View(v) => self.view = v,
            Msg::RibbonTab(i) => self.ribbon_tab = i,
            Msg::Backstage(open) => self.backstage = open,
            Msg::OpenProject(i) => {
                self.backstage = false;
                self.started = true;
                self.project = i;
                return self.toast(Tone::Info, "Project geopend", format!("{} is geopend.", PROJECTS[i].0));
            }
            Msg::SelectDoc(i) => self.active = i,
            Msg::CloseDoc(i) => {
                if self.docs.get(i).is_some_and(|d| d.dirty) {
                    self.dialog = Some(Dialog::CloseDirty(i));
                } else {
                    self.close_doc(i);
                }
            }
            Msg::OpenDoc(kind) => self.open_doc(kind),
            Msg::Tree(sel) => {
                self.tree = sel;
                match sel {
                    TreeSel::Item(id) => {
                        self.select(Some(id));
                        self.open_doc(DocKind::Item(id));
                    }
                    _ => self.open_doc(DocKind::Budget),
                }
            }
            Msg::ToggleRoot => self.root_open = !self.root_open,
            Msg::ToggleChapter(k) => {
                if !self.open_chapters.remove(k) {
                    self.open_chapters.insert(k);
                }
            }
            Msg::SelectRow(id) => self.select(Some(id)),
            Msg::New => {
                self.blank_count += 1;
                self.open_doc(DocKind::Blank(self.blank_count));
            }
            Msg::Save => {
                for doc in &mut self.docs {
                    doc.dirty = false;
                }
                return self.toast(Tone::Success, "Opgeslagen", format!("{} is opgeslagen.", PROJECTS[self.project].0));
            }
            Msg::Undo => {
                if let Some(previous) = self.history.pop() {
                    self.future.push(std::mem::replace(&mut self.items, previous));
                    self.select(self.selected.filter(|id| self.items.iter().any(|i| i.id == *id)));
                }
            }
            Msg::Redo => {
                if let Some(next) = self.future.pop() {
                    self.history.push(std::mem::replace(&mut self.items, next));
                    self.select(self.selected.filter(|id| self.items.iter().any(|i| i.id == *id)));
                }
            }
            Msg::Copy | Msg::Cut => {
                let Some(item) = self.selected.and_then(|id| self.item(id)).cloned() else {
                    return self.toast(Tone::Info, "Niets gekozen", "Kies eerst een post.");
                };
                self.clipboard = Some(item.clone());
                if matches!(message, Msg::Cut) {
                    self.remember();
                    self.items.retain(|i| i.id != item.id);
                    self.selected = None;
                    return self.toast(Tone::Info, "Geknipt", format!("{} staat op het klembord.", item.name));
                }
                return self.toast(Tone::Info, "Gekopieerd", format!("{} staat op het klembord.", item.name));
            }
            Msg::Paste => {
                if let Some(mut item) = self.clipboard.clone() {
                    self.remember();
                    item.code = self.next_code(item.chapter().to_string().as_str());
                    self.insert_item(item);
                    self.banner = self.missing_prices();
                }
            }
            Msg::Delete => {
                if let Some(id) = self.selected {
                    let name = self.item(id).map(|i| i.name.clone()).unwrap_or_default();
                    self.remember();
                    self.items.retain(|i| i.id != id);
                    self.selected = None;
                    if let Some(i) = self.docs.iter().position(|d| d.kind == DocKind::Item(id)) {
                        self.close_doc(i);
                    }
                    self.banner = self.missing_prices();
                    return self.toast(Tone::Info, "Verwijderd", format!("{name} is verwijderd. Ongedaan maken met Ctrl+Z."));
                }
            }
            Msg::AddItem => {
                let chapter = self.selected.and_then(|id| self.item(id)).map_or("21".to_string(), |i| i.chapter().to_string());
                self.remember();
                let code = self.next_code(&chapter);
                self.insert_item(Item { id: 0, code, name: "Nieuwe post".into(), quantity: 1.0, unit: "st", price: 0.0, include: true });
                self.open_doc(DocKind::Budget);
                self.banner = self.missing_prices();
            }
            Msg::AddChapter => {
                let used: HashSet<String> = self.items.iter().map(|i| i.chapter().to_string()).collect();
                if let Some((key, name)) = CHAPTERS.iter().find(|(k, _)| !used.contains(*k)) {
                    self.remember();
                    let code = format!("{key}.10");
                    self.insert_item(Item { id: 0, code, name: "Nieuwe post".into(), quantity: 1.0, unit: "st", price: 0.0, include: true });
                    self.open_doc(DocKind::Budget);
                    self.banner = self.missing_prices();
                    return self.toast(Tone::Success, "Hoofdstuk toegevoegd", format!("{name} is toegevoegd."));
                }
                return self.toast(Tone::Info, "Alle hoofdstukken bestaan al", "Deze voorbeeldbegroting heeft vijf hoofdstukken.");
            }
            Msg::Recalculate => {
                let total = euro(self.total());
                return self.toast(Tone::Success, "Berekening bijgewerkt", format!("Het totaal is {total}."));
            }
            Msg::Audit => {
                self.banner = self.missing_prices();
                self.open_doc(DocKind::Budget);
                if self.banner.is_none() {
                    return self.toast(Tone::Success, "Gecontroleerd", "Alle posten hebben een prijs.");
                }
            }
            Msg::CloseBanner => self.banner = None,
            Msg::ZoomIn => self.zoom = (self.zoom + 25).min(400),
            Msg::ZoomOut => self.zoom = self.zoom.saturating_sub(25).max(25),
            Msg::ZoomFit => self.zoom = 100,
            Msg::ToggleGrid => self.grid = !self.grid,
            Msg::ToggleLeft => self.show_left = !self.show_left,
            Msg::ToggleRight => self.show_right = !self.show_right,
            Msg::GenerateReport => {
                self.report_ready = true;
                self.open_doc(DocKind::Report);
                return self.toast(Tone::Success, "Rapport gemaakt", "Het rapport staat in de tab Rapport.");
            }
            Msg::Dialog(d) => {
                let opening = d.is_some() && self.dialog.is_none();
                self.dialog = d;
                if d.is_none() {
                    // Closing the dialog stops any recording on the shortcuts page.
                    self.shortcuts = sc::Editor::default();
                }
                // The screen behind is inert, so the first step lands in the dialog.
                if opening {
                    return openaec_ui::keyboard::navigate(openaec_ui::keyboard::Navigation::Next);
                }
            }
            Msg::Navigate(step) => return openaec_ui::keyboard::navigate(step),
            Msg::Key(press) if self.shortcuts.recording() => return self.update(Msg::Shortcuts(sc::Message::Key(press))),
            Msg::Shortcuts(message) => {
                let defaults = self.default_commands();
                if self.shortcuts.update(message, &mut self.keymap, &defaults) {
                    if let Some(path) = &self.keymap_path {
                        if let Err(error) = self.keymap.save(path) {
                            return self.toast(Tone::Error, "Sneltoetsen niet opgeslagen", &error.to_string());
                        }
                    }
                }
            }
            Msg::SettingsPage(page) => {
                self.settings_page = page;
                self.shortcuts = sc::Editor::default();
            }
            Msg::Key(press) => {
                use keyboard::key::Named;
                // Escape and Enter belong to dialogs and menus; every other key is a command.
                let message = match &press.key {
                    keyboard::Key::Named(Named::Escape) => Some(Msg::Escape),
                    keyboard::Key::Named(Named::Enter) if press.modifiers.is_empty() => Some(Msg::Enter),
                    key => cm::find(&self.commands(), key, press.modifiers),
                };
                if let Some(message) = message {
                    return self.update(message);
                }
            }
            Msg::Format(f) => self.format = f,
            Msg::Landscape(b) => self.landscape = b,
            Msg::ConfirmExport => {
                self.dialog = None;
                return self.toast(Tone::Success, "Geëxporteerd", format!("De begroting is geëxporteerd als {}.", self.format));
            }
            Msg::ConfirmPrint => {
                self.dialog = None;
                let orientation = if self.landscape { "liggend" } else { "staand" };
                return self.toast(Tone::Success, "Naar de printer", format!("De begroting wordt {orientation} afgedrukt."));
            }
            Msg::DiscardAndClose(i) => {
                self.dialog = None;
                self.close_doc(i);
            }
            Msg::SaveAndClose(i) => {
                self.dialog = None;
                for doc in &mut self.docs {
                    doc.dirty = false;
                }
                self.close_doc(i);
                return self.toast(Tone::Success, "Opgeslagen", "De wijzigingen zijn opgeslagen.");
            }
            Msg::EditName(name) => self.edit(|i| i.name = name),
            Msg::EditUnit(unit) => self.edit(|i| i.unit = unit),
            Msg::EditQuantity(value) => {
                if let Some(q) = parse_nl(&value) {
                    self.edit(|i| i.quantity = q);
                }
                self.quantity_text = value;
            }
            Msg::EditPrice(value) => {
                if let Some(p) = parse_nl(&value) {
                    self.edit(|i| i.price = p);
                    if self.banner.is_some() {
                        self.banner = self.missing_prices();
                    }
                }
                self.price_text = value;
            }
            Msg::EditInclude(b) => self.edit(|i| i.include = b),
            Msg::CloseToast => self.toast = None,
            Msg::ToastExpired(id) => {
                if self.toast.as_ref().is_some_and(|t| t.id == id) {
                    self.toast = None;
                }
            }
            Msg::Escape => {
                if self.menu.is_some() {
                    self.menu = None;
                } else if self.dialog.is_some() {
                    self.dialog = None;
                } else if self.backstage {
                    self.backstage = false;
                } else {
                    self.toast = None;
                }
            }
            Msg::Enter => {
                let next = match self.dialog {
                    Some(Dialog::Export) => Some(Msg::ConfirmExport),
                    Some(Dialog::Print) => Some(Msg::ConfirmPrint),
                    Some(Dialog::CloseDirty(i)) => Some(Msg::SaveAndClose(i)),
                    Some(Dialog::Quit) => Some(Msg::SaveAndQuit),
                    Some(Dialog::Settings) => Some(Msg::Dialog(None)),
                    None => None,
                };
                if let Some(msg) = next {
                    return self.update(msg);
                }
            }
            Msg::Restart => {
                // As at launch: the start screen, unless the setting opens the last project.
                self.started = self.skip_start;
                self.backstage = false;
                self.dialog = None;
                self.view = View::Screen;
                if self.skip_start {
                    return self.toast(Tone::Info, "Laatste project geopend", format!("{} is direct geopend, zonder startscherm.", PROJECTS[self.project].0));
                }
            }
            Msg::SkipStart(b) => self.skip_start = b,
            Msg::Cursor(p) => {
                self.cursor = p;
                if let Some((side, start_x, start_width)) = self.drag {
                    let dx = p.x - start_x;
                    let width = match side {
                        Side::Left => start_width + dx,
                        Side::Right => start_width - dx,
                    }
                    .clamp(180.0, 480.0);
                    match side {
                        Side::Left => self.left_width = width,
                        Side::Right => self.right_width = width,
                    }
                }
            }
            Msg::WindowResized(size) => self.window = size,
            Msg::TitlePress => {
                // A second press within 400 ms is a double click: maximise or restore.
                let now = Instant::now();
                let double = self.last_title_press.is_some_and(|t| now.duration_since(t) < Duration::from_millis(400));
                self.last_title_press = Some(now);
                if double {
                    self.last_title_press = None;
                    return self.update(Msg::Maximize);
                }
                return iced::window::latest().and_then(iced::window::drag);
            }
            Msg::Minimize => return iced::window::latest().and_then(|id| iced::window::minimize(id, true)),
            Msg::Maximize => {
                self.maximized = !self.maximized;
                return iced::window::latest().and_then(iced::window::toggle_maximize);
            }
            Msg::CloseWindow => {
                if self.docs.iter().any(|d| d.dirty) {
                    self.dialog = Some(Dialog::Quit);
                } else {
                    return iced::window::latest().and_then(iced::window::close);
                }
            }
            Msg::QuitNow => return iced::window::latest().and_then(iced::window::close),
            Msg::SaveAndQuit => {
                for doc in &mut self.docs {
                    doc.dirty = false;
                }
                return iced::window::latest().and_then(iced::window::close);
            }
            Msg::DragSplit(side) => {
                let width = match side {
                    Side::Left => self.left_width,
                    Side::Right => self.right_width,
                };
                self.drag = Some((side, self.cursor.x, width));
            }
            Msg::EndDrag => self.drag = None,
            Msg::Menu(kind) => {
                let opening = kind.is_some() && self.menu.is_none();
                self.menu = kind.map(|k| (k, self.cursor));
                match kind {
                    Some(MenuKind::Row(id)) => self.select(Some(id)),
                    Some(MenuKind::Tree(sel)) => {
                        self.tree = sel;
                        if let TreeSel::Item(id) = sel {
                            self.select(Some(id));
                        }
                    }
                    _ => {}
                }
                if opening {
                    return openaec_ui::keyboard::navigate(openaec_ui::keyboard::Navigation::Next);
                }
            }
            Msg::OpenItem(id) => {
                self.menu = None;
                self.select(Some(id));
                self.open_doc(DocKind::Item(id));
            }
            Msg::CloseOthers(keep) => {
                self.menu = None;
                let kept = self.docs.get(keep).map(|d| d.kind);
                let before = self.docs.len();
                self.docs.retain(|d| Some(d.kind) == kept || d.dirty);
                self.active = self.docs.iter().position(|d| Some(d.kind) == kept).unwrap_or(0);
                if self.docs.len() > 1 {
                    return self.toast(Tone::Info, "Niet alles gesloten", format!("{} tab(s) met wijzigingen blijven open.", self.docs.len() - 1));
                }
                let _ = before;
            }
            Msg::CloseAll => {
                self.menu = None;
                self.docs.retain(|d| d.dirty);
                self.active = 0;
                if !self.docs.is_empty() {
                    return self.toast(Tone::Info, "Niet alles gesloten", "Tabs met wijzigingen blijven open. Sla eerst op.");
                }
            }
            Msg::CloseActive => {
                if !self.docs.is_empty() {
                    return self.update(Msg::CloseDoc(self.active));
                }
            }
            Msg::FilePage(p) => self.file_page = p,
            Msg::WfSection(i) => {
                self.wf.section = i;
                self.wf.visited[i] = true;
            }
            Msg::WfNavigation(n) => self.wf.navigation = n,
            Msg::WfNext => {
                let i = (self.wf.section + 1).min(SECTIONS.len() - 1);
                return self.update(Msg::WfSection(i));
            }
            Msg::WfPrevious => {
                let i = self.wf.section.saturating_sub(1);
                return self.update(Msg::WfSection(i));
            }
            Msg::WfProject(s) => self.wf.project = s,
            Msg::WfAddress(s) => self.wf.address = s,
            Msg::WfType(k) => self.wf.kind = k,
            Msg::WfYear(s) => self.wf.year = s,
            Msg::WfArea(s) => self.wf.area = s,
            Msg::WfRcWall(s) => self.wf.rc_wall = s,
            Msg::WfRcRoof(s) => self.wf.rc_roof = s,
            Msg::WfRcFloor(s) => self.wf.rc_floor = s,
            Msg::WfWindowU(s) => self.wf.window_u = s,
            Msg::WfHeating(h) => self.wf.heating = h,
            Msg::WfVentilation(v) => self.wf.ventilation = v,
            Msg::WfSolar(b) => self.wf.solar = b,
            Msg::WfPanels(p) => self.wf.panels = p.round(),
            Msg::WfCalculate => {
                self.wf.calculated = true;
                self.wf.section = SECTIONS.len() - 1;
                self.wf.visited = [true; 5];
                let label = self.wf.label();
                return self.toast(Tone::Success, "Berekend", format!("Het voorlopige energielabel is {label}."));
            }
            Msg::InstTab(t) => self.inst.active = t,
            Msg::InstOpenWeb(i) => {
                self.inst.tabs = vec![i];
                self.inst.active = Some(0);
            }
            Msg::InstInstall(i) => {
                self.inst.tools[i].progress = Some(0.0);
                return after(120, Msg::InstTick(i));
            }
            Msg::InstTick(i) => {
                let p = self.inst.tools[i].progress.unwrap_or(0.0) + 0.06;
                if p >= 1.0 {
                    let updated = self.inst.tools[i].installed.is_some();
                    self.inst.tools[i] = ToolState { installed: Some(TOOLS[i].latest), progress: None };
                    let title = if updated { "Bijgewerkt" } else { "Geïnstalleerd" };
                    return self.toast(Tone::Success, title, format!("{} v{} is klaar om te starten.", TOOLS[i].name, TOOLS[i].latest));
                }
                self.inst.tools[i].progress = Some(p);
                return after(120, Msg::InstTick(i));
            }
            Msg::InstLaunch(i) => {
                let what = if TOOLS[i].web { "wordt in de browser geopend" } else { "wordt gestart" };
                return self.toast(Tone::Info, TOOLS[i].name, format!("{} {what}.", TOOLS[i].name));
            }
            Msg::InstSearch(q) => self.inst.search = q,
            Msg::InstFilter(f) => {
                self.inst.filter = f;
                self.inst.disc = None;
            }
            Msg::InstDisc(d) => {
                self.inst.disc = if self.inst.disc == d { None } else { d };
                self.inst.filter = Filter::All;
            }
            Msg::InstFeature(n) => self.inst.feature = n,
            Msg::IconSearch(s) => {
                self.icons.search = s;
                self.icons.page = 0;
                return icon_grid_to_top();
            }
            Msg::IconApp(c) => {
                self.icons.app = c;
                self.icons.page = 0;
                return icon_grid_to_top();
            }
            Msg::IconGroup(c) => {
                self.icons.group = c;
                self.icons.page = 0;
                return icon_grid_to_top();
            }
            Msg::IconLarge(on) => self.icons.large = on,
            Msg::IconPage(n) => {
                self.icons.page = n;
                return icon_grid_to_top();
            }
            Msg::IconSelect(i) => self.icons.selected = if self.icons.selected == Some(i) { None } else { Some(i) },
            Msg::InstFeatureTick => {
                // The featured block changes every six seconds, but not while something installs.
                if self.inst.tools.iter().all(|t| t.progress.is_none()) {
                    self.inst.feature += 1;
                }
                return after(6000, Msg::InstFeatureTick);
            }
            Msg::InstGitHub(i) => return self.toast(Tone::Info, TOOLS[i].name, "De GitHub-pagina wordt in de browser geopend."),
            Msg::InstUpdateAll => {
                let ids: Vec<usize> = (0..TOOLS.len()).filter(|&i| self.inst.has_update(i)).collect();
                let tasks: Vec<Task<Msg>> = ids
                    .into_iter()
                    .map(|i| {
                        self.inst.tools[i].progress = Some(0.0);
                        after(120, Msg::InstTick(i))
                    })
                    .collect();
                return Task::batch(tasks);
            }
            Msg::InstRefresh => {
                self.inst.refreshing = true;
                return after(1200, Msg::InstRefreshDone);
            }
            Msg::InstRefreshDone => {
                self.inst.refreshing = false;
                self.inst.last_refresh = "zojuist".into();
                let n = (0..TOOLS.len()).filter(|&i| self.inst.has_update(i)).count();
                return self.toast(Tone::Info, "Vernieuwd", if n == 0 { "Alle geïnstalleerde tools zijn bij.".to_string() } else { format!("{n} update(s) beschikbaar.") });
            }
            Msg::InstSelfUpdate => {
                self.inst.self_update = Some(0.0);
                return after(120, Msg::InstSelfTick);
            }
            Msg::InstSelfTick => {
                let p = self.inst.self_update.unwrap_or(0.0) + 0.08;
                if p >= 1.0 {
                    self.inst.self_update = None;
                    self.inst.self_version = "1.6.0";
                    return self.toast(Tone::Success, "Installer bijgewerkt", "De installer start opnieuw met versie 1.6.0.");
                }
                self.inst.self_update = Some(p);
                return after(120, Msg::InstSelfTick);
            }
            Msg::InstDismissSelf => self.inst.self_dismissed = true,
            Msg::Check(b) => self.check = b,
            Msg::Switch(b) => self.switch = b,
            Msg::Radio(r) => self.radio = Some(r),
            Msg::Slider(v) => self.slider = v,
            Msg::Name(s) => self.name = s,
            Msg::Unit(u) => self.unit = Some(u),
            Msg::Noop => {}
        }
        Task::none()
    }

    fn edit(&mut self, change: impl FnOnce(&mut Item)) {
        let Some(id) = self.selected else { return };
        self.remember();
        if let Some(item) = self.items.iter_mut().find(|i| i.id == id) {
            change(item);
        }
        let title = self.item(id).map(|i| format!("{} {}", i.code, i.name));
        if let (Some(title), Some(doc)) = (title, self.docs.iter_mut().find(|d| d.kind == DocKind::Item(id))) {
            doc.title = title;
        }
    }

    fn subscription(&self) -> Subscription<Msg> {
        // Shortcuts come from the same command list as the ribbon and the menus.
        let keys = openaec_ui::keyboard::presses().map(Msg::Key);
        Subscription::batch([keys, openaec_ui::keyboard::navigation().map(Msg::Navigate), iced::window::resize_events().map(|(_, size)| Msg::WindowResized(size))])
    }

    fn view(&self) -> Element<'_, Msg> {
        let look = self.look();
        let body = match self.view {
            View::Screen => self.screen(look),
            View::Workflow => self.workflow(look),
            View::Installer => self.installer(look),
            View::Components => self.components(look),
            View::Icons => self.icons(look),
        };
        // An open menu or dialog takes the screen behind out of the Tab route and the keys.
        let screen = column![self.toolbar(look), container(body).height(Length::Fill)].height(Length::Fill);
        let mut layers = vec![focus::inert(screen, self.menu.is_some() || self.dialog.is_some())];
        if let Some(toast) = &self.toast {
            let card = w::toast(look, toast.tone, tone_icon(toast.tone), &toast.title, &toast.message, CLOSE, Some(Msg::CloseToast));
            layers.push(container(card).width(Length::Fill).height(Length::Fill).align_right(Length::Fill).align_bottom(Length::Fill).padding([36, 16]).into());
        }
        if let Some((kind, at)) = self.menu {
            let items = self.menu_items(kind);
            let height = ch::menu_height(&items);
            let menu = ch::menu(look, items, CHECK);
            layers.push(ch::menu_layer(menu, at, Size::new(ch::MENU_WIDTH, height), self.window, Msg::Menu(None)));
        }
        if let Some(dialog) = self.dialog {
            // The overlay takes the clicks, so the screen behind it stays still.
            layers.push(mouse_area(w::overlay(look, self.dialog_card(look, dialog))).on_press(Msg::Noop).into());
        }
        // The root follows the cursor for menus and panel dragging.
        let root = mouse_area(iced::widget::Stack::with_children(layers)).on_move(Msg::Cursor).on_release(Msg::EndDrag);
        if self.drag.is_some() {
            root.interaction(mouse::Interaction::ResizingHorizontally).into()
        } else {
            root.into()
        }
    }

    /// The gallery's own controls: theme, settings and view. Not part of the design.
    fn toolbar(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let views = [(View::Screen, "Lint-app"), (View::Workflow, "Werkstroom-app"), (View::Installer, "Installer"), (View::Components, "Componenten"), (View::Icons, "Iconen")];
        let mut bar = row![
            text("UI 0.4").size(font::SIZE_PANEL_HEADING).font(fonts::HEADING).color(c.text),
            Space::new().width(12),
            w::mono_label(look, "Thema"),
            container(w::select(look, &ThemeId::ALL, Some(self.theme), Msg::Theme, D::Compact)).width(160),
            w::mono_label(look, "Werkruimte"),
            container(w::select(look, &WorkspaceSetting::ALL, Some(self.workspace), Msg::Workspace, D::Compact)).width(122),
            w::mono_label(look, "Statusbalk"),
            container(w::select(look, &StatusbarSetting::ALL, Some(self.statusbar), Msg::Statusbar, D::Compact)).width(122),
        ]
        .spacing(8)
        .align_y(Alignment::Center);
        if self.view == View::Workflow {
            bar = bar.push(w::mono_label(look, "Navigatie"));
            bar = bar.push(container(w::select(look, &Navigation::ALL, Some(self.wf.navigation), Msg::WfNavigation, D::Compact)).width(144));
        }
        bar = bar.push(Space::new().width(Length::Fill));
        bar = bar.push(w::with_tooltip(look, w::icon_button(look, HOME, 24.0, false, Some(Msg::Restart)), "Herstart: doe alsof de app opnieuw opent", None));
        for (v, label) in views {
            let kind = if self.view == v { K::Secondary } else { K::Quiet };
            bar = bar.push(w::button(look, label, kind, D::Compact, None, Some(Msg::View(v))));
        }
        // The window has no system frame, so the gallery bar also moves the window.
        mouse_area(
            container(bar)
                .padding([6, 12])
                .width(Length::Fill)
                .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() }),
        )
        .on_press(Msg::TitlePress)
        .into()
    }

    /// A complete application screen in the 0.4 design.
    fn screen(&self, look: Look) -> Element<'_, Msg> {
        let dirty = self.docs.iter().any(|d| d.dirty);
        let title = self.title_bar(look, format!("{}{} · Voorbeeldstudio · OpenAEC", PROJECTS[self.project].0, if dirty { " •" } else { "" }), true);
        if !self.started {
            return column![self.title_bar(look, "Voorbeeldstudio · OpenAEC".into(), false), self.start_screen(look), self.plain_status(look, "Kies een project om te beginnen")].into();
        }

        let tabs = w::ribbon_tabs(look, "Bestand", Some(Msg::Backstage(!self.backstage)), &TABS, if self.backstage { usize::MAX } else { self.ribbon_tab }, |i| Msg::RibbonTab(i));
        if self.backstage {
            return column![title, tabs, w::divider(look), self.backstage_view(look)].into();
        }

        let mut main = row![].height(Length::Fill);
        let dragging = |side| self.drag.is_some_and(|(s, _, _)| s == side);
        if self.show_left {
            main = main.push(self.tree_panel(look));
            main = main.push(ch::splitter(look, dragging(Side::Left), Msg::DragSplit(Side::Left)));
        }
        main = main.push(column![self.document_tabs(look), self.workspace_view(look)].width(Length::Fill));
        if self.show_right {
            main = main.push(ch::splitter(look, dragging(Side::Right), Msg::DragSplit(Side::Right)));
            main = main.push(self.properties_panel(look));
        }
        let open = self.items.iter().filter(|i| i.include).count();
        column![
            title,
            tabs,
            self.ribbon(look),
            w::divider(look),
            main,
            w::status_bar(
                look,
                vec![
                    if dirty { "Niet opgeslagen wijzigingen".into() } else { "Gereed".into() },
                    format!("{open} posten"),
                    format!("Raster {}", if self.grid { "aan" } else { "uit" }),
                ],
                vec![euro(self.total()), format!("{}%", self.zoom)],
            ),
        ]
        .into()
    }

    fn ribbon(&self, look: Look) -> Element<'_, Msg> {
        // Every button comes from the command list, so it shows the same label,
        // state and shortcut as the menus and the keyboard.
        let large = |id| cm::ribbon_large(look, &self.command(id));
        let small = |id| cm::ribbon_small(look, &self.command(id));
        let groups = match self.ribbon_tab {
            0 => vec![
                w::ribbon_group(look, "Project", vec![large("file.new"), large("file.open"), large("file.save")]),
                w::ribbon_group(look, "Klembord", vec![large("edit.paste"), column![small("edit.cut"), small("edit.copy"), small("edit.delete")].spacing(2).into()]),
                w::ribbon_group(look, "Geschiedenis", vec![large("edit.undo"), large("edit.redo")]),
            ],
            1 => vec![
                w::ribbon_group(look, "Posten", vec![large("insert.item"), large("insert.chapter")]),
                w::ribbon_group(look, "Weergaven", vec![large("view.table"), large("view.chart")]),
            ],
            2 => vec![
                w::ribbon_group(look, "Berekening", vec![large("calc.recalculate")]),
                w::ribbon_group(look, "Controle", vec![large("calc.audit")]),
            ],
            3 => vec![
                w::ribbon_group(look, "Zoomen", vec![column![small("view.zoom-in"), small("view.zoom-out"), small("view.zoom-fit")].spacing(2).into()]),
                w::ribbon_group(look, "Tonen", vec![large("view.grid"), large("view.left"), large("view.right")]),
                w::ribbon_group(look, "Venster", vec![large("app.settings")]),
            ],
            _ => vec![
                w::ribbon_group(look, "Rapport", vec![large("report.generate")]),
                w::ribbon_group(look, "Uitvoer", vec![large("file.export"), large("file.print")]),
            ],
        };
        w::ribbon(look, groups)
    }

    fn tree_panel(&self, look: Look) -> Element<'_, Msg> {
        // Right and Left open and close a branch while its row has the focus.
        let root = w::tree_row(
            look,
            0,
            Some(if self.root_open { COLLAPSE } else { EXPAND }),
            Some(Msg::ToggleRoot),
            Some(FOLDER),
            PROJECTS[self.project].0,
            self.tree == TreeSel::Root,
            Some(Msg::Tree(TreeSel::Root)),
            Some(Msg::Menu(Some(MenuKind::Tree(TreeSel::Root)))),
        );
        let mut tree = column![focus::expander(root, self.root_open, Msg::ToggleRoot)];
        if self.root_open {
            for (key, name) in CHAPTERS {
                let children: Vec<&Item> = self.items.iter().filter(|i| i.chapter() == key).collect();
                if children.is_empty() {
                    continue;
                }
                let open = self.open_chapters.contains(key);
                let row = w::tree_row(look, 1, Some(if open { COLLAPSE } else { EXPAND }), Some(Msg::ToggleChapter(key)), Some(FOLDER), name, self.tree == TreeSel::Chapter(key), Some(Msg::Tree(TreeSel::Chapter(key))), Some(Msg::Menu(Some(MenuKind::Tree(TreeSel::Chapter(key))))));
                tree = tree.push(focus::expander(row, open, Msg::ToggleChapter(key)));
                if open {
                    for item in children {
                        tree = tree.push(w::tree_row(look, 2, None, None, Some(ITEM), &item.name, self.tree == TreeSel::Item(item.id), Some(Msg::Tree(TreeSel::Item(item.id))), Some(Msg::Menu(Some(MenuKind::Tree(TreeSel::Item(item.id)))))));
                    }
                }
            }
        }
        w::panel(
            look,
            "Structuur",
            self.left_width,
            vec![
                w::with_tooltip(look, w::icon_button(look, SEARCH, 20.0, false, Some(Msg::Noop)), "Zoeken", Some("Ctrl+F")),
                w::with_tooltip(look, w::icon_button(look, PANEL_LEFT, 20.0, true, Some(Msg::ToggleLeft)), "Paneel verbergen", Some("Ctrl+1")),
            ],
            scrollable(focus::group(tree, focus::Axis::Vertical)).height(Length::Fill).into(),
        )
    }

    fn properties_panel(&self, look: Look) -> Element<'_, Msg> {
        let content: Element<'_, Msg> = match self.selected.and_then(|id| self.item(id)) {
            Some(item) => column![
                w::section_header(look, COLLAPSE, "Algemeen"),
                w::property_row(look, "Code", w::number(look, item.code.as_str()).into()),
                w::property_row(look, "Naam", w::text_field(look, "Naam", &item.name, Some(Msg::EditName), D::Compact, None)),
                w::property_row(look, "Eenheid", w::select(look, &UNITS, Some(item.unit), Msg::EditUnit, D::Compact)),
                w::property_row(look, "Meenemen", w::checkbox(look, "", item.include, Some(Msg::EditInclude))),
                w::section_header(look, COLLAPSE, "Berekening"),
                w::property_row(
                    look,
                    "Hoeveelheid",
                    w::text_field(look, "0", &self.quantity_text, Some(Msg::EditQuantity), D::Compact, parse_nl(&self.quantity_text).is_none().then_some("Geen getal")),
                ),
                w::property_row(look, "Prijs", w::text_field(look, "0,00", &self.price_text, Some(Msg::EditPrice), D::Compact, parse_nl(&self.price_text).is_none().then_some("Geen getal"))),
                w::property_row(look, "Bedrag", w::number(look, euro(item.amount())).into()),
            ]
            .into(),
            None => container(w::secondary(look, "Kies een post in de boom of de tabel om de eigenschappen te zien.")).padding(12).into(),
        };
        w::panel(look, "Eigenschappen", self.right_width, vec![w::with_tooltip(look, w::icon_button(look, PANEL_RIGHT, 20.0, true, Some(Msg::ToggleRight)), "Paneel verbergen", Some("Ctrl+2"))], content)
    }

    fn document_tabs(&self, look: Look) -> Element<'_, Msg> {
        let tabs: Vec<DocumentTab<'_>> = self.docs.iter().map(|d| DocumentTab::new(&d.title, d.dirty)).collect();
        w::document_tabs(look, &tabs, self.active, CLOSE, Msg::SelectDoc, Msg::CloseDoc, |i| Msg::Menu(Some(MenuKind::Tab(i))))
    }

    fn workspace_view(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let Some(doc) = self.docs.get(self.active) else {
            return w::empty_state(
                look,
                FOLDER_LARGE,
                "Geen document geopend",
                "Open de begroting of maak een nieuw document.",
                Some(row![w::button(look, "Begroting openen", K::Secondary, D::Regular, None, Some(Msg::OpenDoc(DocKind::Budget))), w::button(look, "Nieuw", K::Primary, D::Regular, None, Some(Msg::New))].spacing(8).into()),
            );
        };
        let page = |content| page(look, content);
        let card = |content| card(look, content);
        let selected_row = |ids: &[u32]| self.selected.and_then(|s| ids.iter().position(|id| *id == s));
        match doc.kind {
            DocKind::Budget => {
                let ids: Vec<u32> = self.items.iter().map(|i| i.id).collect();
                let rows = self
                    .items
                    .iter()
                    .map(|i| vec![i.code.clone(), i.name.clone(), format!("{} {}", nl(i.quantity, 1), i.unit), if i.price == 0.0 { "–".into() } else { euro(i.price) }, euro(i.amount())])
                    .collect();
                let mut content = column![].spacing(12);
                if let Some((tone, message)) = &self.banner {
                    content = content.push(w::banner(look, *tone, tone_icon(*tone), message, CLOSE, Some(Msg::CloseBanner)));
                }
                let menu_ids = ids.clone();
                let table = w::table(look, &BUDGET_COLUMNS, rows, selected_row(&ids), Some(move |i: usize| Msg::SelectRow(ids[i])), Some(move |i: usize| Msg::Menu(Some(MenuKind::Row(menu_ids[i])))));
                let total = row![w::mono_label(look, "Totaal"), Space::new().width(Length::Fill), text(euro(self.total())).size(font::SIZE_PANEL_HEADING).font(fonts::MONO).color(c.text)].padding([8, 8]).align_y(Alignment::Center);
                content = content.push(card(column![table, total].into()));
                content = content.push(row![
                    w::button(look, "Nieuwe post", K::Secondary, D::Regular, Some(b2!("16", "budget.add-item")), Some(Msg::AddItem)),
                    w::button(look, "Verwijderen", K::Danger, D::Regular, Some(DELETE), self.selected.map(|_| Msg::Delete)),
                ]
                .spacing(8));
                page(content.into())
            }
            DocKind::Quantities => {
                let ids: Vec<u32> = self.items.iter().map(|i| i.id).collect();
                let rows = self.items.iter().map(|i| vec![i.code.clone(), i.name.clone(), nl(i.quantity, 1), i.unit.to_string()]).collect();
                let menu_ids = ids.clone();
                page(card(w::table(look, &QUANTITY_COLUMNS, rows, selected_row(&ids), Some(move |i: usize| Msg::SelectRow(ids[i])), Some(move |i: usize| Msg::Menu(Some(MenuKind::Row(menu_ids[i])))))))
            }
            DocKind::Chart => {
                let totals: Vec<(&str, f64)> = CHAPTERS
                    .iter()
                    .map(|(key, name)| (*name, self.items.iter().filter(|i| i.chapter() == *key).map(Item::amount).sum::<f64>()))
                    .filter(|(_, v)| *v > 0.0)
                    .collect();
                let max = totals.iter().map(|(_, v)| *v).fold(1.0, f64::max);
                let mut bars = column![text("Bedrag per hoofdstuk").size(font::SIZE_DIALOG_HEADING).font(fonts::HEADING).color(c.text)].spacing(14);
                for (name, value) in totals {
                    let share = ((value / max) * 1000.0).round().max(1.0) as u16;
                    let accent = c.accent;
                    bars = bars.push(
                        row![
                            text(name).size(font::SIZE_BODY).color(c.text).width(120),
                            row![
                                container(Space::new().width(Length::Fill).height(18)).width(Length::FillPortion(share)).style(move |_| container::Style {
                                    background: Some(Background::Color(accent)),
                                    border: iced::Border { radius: 3.0.into(), ..Default::default() },
                                    ..Default::default()
                                }),
                                Space::new().width(Length::FillPortion(1000 - share.min(999))),
                            ]
                            .width(Length::Fill),
                            text(euro(value)).size(font::SIZE_BODY).font(fonts::MONO).color(c.text).width(120).align_x(iced::alignment::Horizontal::Right),
                        ]
                        .spacing(12)
                        .align_y(Alignment::Center),
                    );
                }
                page(card(container(bars).padding(16).into()))
            }
            DocKind::Report if !self.report_ready => w::empty_state(
                look,
                REPORT_DOC,
                "Nog geen rapport",
                "Maak het rapport van deze begroting. Je vindt de knop ook in de linttab Rapport.",
                Some(w::button(look, "Rapport maken", K::Primary, D::Regular, None, Some(Msg::GenerateReport))),
            ),
            DocKind::Report => {
                let mut lines = column![
                    text(format!("Begroting {}", PROJECTS[self.project].0)).size(font::SIZE_PAGE_HEADING).font(fonts::HEADING).color(c.text),
                    w::secondary(look, "Opdrachtgever: Gemeente Voorbeeld · Prijspeil oktober 2026"),
                    w::divider(look),
                ]
                .spacing(10);
                for (key, name) in CHAPTERS {
                    let sum: f64 = self.items.iter().filter(|i| i.chapter() == key).map(Item::amount).sum();
                    if sum > 0.0 {
                        lines = lines.push(row![w::body(look, name).width(Length::Fill), w::number(look, euro(sum)).width(140)]);
                    }
                }
                lines = lines.push(w::divider(look));
                lines = lines.push(row![text("Totaal").size(font::SIZE_PANEL_HEADING).font(fonts::STRONG).color(c.text).width(Length::Fill), w::number(look, euro(self.total())).width(140)]);
                page(container(card(container(lines).padding(24).into())).max_width(640).into())
            }
            DocKind::Item(id) => match self.item(id) {
                Some(item) => {
                    let facts = column![
                        text(format!("{} {}", item.code, item.name)).size(font::SIZE_DIALOG_HEADING).font(fonts::HEADING).color(c.text),
                        w::property_row(look, "Hoeveelheid", w::number(look, format!("{} {}", nl(item.quantity, 1), item.unit)).into()),
                        w::property_row(look, "Prijs per eenheid", w::number(look, euro(item.price)).into()),
                        w::property_row(look, "Bedrag", w::number(look, euro(item.amount())).into()),
                        w::property_row(look, "Meenemen", w::body(look, if item.include { "Ja" } else { "Nee" }).into()),
                        w::secondary(look, "Wijzig de waarden in het paneel Eigenschappen rechts."),
                    ]
                    .spacing(6);
                    page(container(card(container(facts).padding(16).into())).max_width(520).into())
                }
                None => w::empty_state(look, ITEM, "Deze post bestaat niet meer", "Sluit de tab of maak het verwijderen ongedaan.", None),
            },
            DocKind::Blank(_) => w::empty_state(
                look,
                FOLDER_NEW,
                "Leeg document",
                "Voeg een post toe om de begroting te vullen.",
                Some(w::button(look, "Post toevoegen", K::Primary, D::Regular, None, Some(Msg::AddItem))),
            ),
        }
    }

    /// The Bestand screen: a 260 px navigation and the tasks or recent work.
    fn backstage_view(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let nav = column![
            t::file_nav_row(look, BACK, "Terug", false, Some(Msg::Backstage(false))),
            w::divider(look),
            t::file_nav_row(look, NEW_SMALL, "Nieuw", self.file_page == FilePage::New, Some(Msg::FilePage(FilePage::New))),
            t::file_nav_row(look, OPEN_SMALL, "Openen", self.file_page == FilePage::Open, Some(Msg::FilePage(FilePage::Open))),
            t::file_nav_row(look, SAVE_SMALL, "Opslaan", false, Some(Msg::Save)),
            t::file_nav_row(look, EXPORT_SMALL, "Exporteren", false, Some(Msg::Dialog(Some(Dialog::Export)))),
            t::file_nav_row(look, PRINT_SMALL, "Afdrukken", false, Some(Msg::Dialog(Some(Dialog::Print)))),
            w::divider(look),
            t::file_nav_row(look, HOME, "Startscherm", false, Some(Msg::Restart)),
            t::file_nav_row(look, SETTINGS, "Instellingen", false, Some(Msg::Dialog(Some(Dialog::Settings)))),
            t::file_nav_row(look, HELP, "Hulp", false, None),
        ]
        .width(260);
        let content: Element<'_, Msg> = match self.file_page {
            FilePage::New => column![
                wf::page_heading(look, "Nieuw", Some("Begin met een lege begroting of een sjabloon.")),
                column![
                    t::task_tile(look, NEW, "Lege begroting", "Een begroting zonder posten.", Some(Msg::New)),
                    t::task_tile(look, ADD_CHAPTER, "Vanaf sjabloon woningbouw", "Hoofdstukken en posten voor een woning.", Some(Msg::AddChapter)),
                    t::task_tile(look, FOLDER_NEW, "Nieuw project", "Een projectmap met begroting en rapport.", Some(Msg::New)),
                    t::task_tile(look, OPEN_LARGE, "Importeren uit Excel", "Volgt later in deze voorbeeldstudio.", None),
                ]
                .spacing(8)
                .max_width(620),
            ]
            .spacing(16)
            .into(),
            FilePage::Open => column![
                wf::page_heading(look, "Openen", Some("Recente projecten en bestanden.")),
                self.project_grid(look),
                w::mono_label(look, "Recente bestanden"),
                self.recent_list(look),
            ]
            .spacing(16)
            .max_width(860)
            .into(),
        };
        row![
            container(nav).height(Length::Fill).style(move |_| w::panel_style(look)),
            container(scrollable(container(content).padding(32)).height(Length::Fill))
                .width(Length::Fill)
                .height(Length::Fill)
                .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() }),
        ]
        .height(Length::Fill)
        .into()
    }

    /// The title bar (32 px) from the library, with working window buttons.
    fn title_bar(&self, look: Look, name: String, quick: bool) -> Element<'_, Msg> {
        let quick_buttons = if quick {
            vec![
                cm::icon_button(look, &self.command("file.save"), 28.0),
                cm::icon_button(look, &self.command("edit.undo"), 28.0),
                cm::icon_button(look, &self.command("edit.redo"), 28.0),
            ]
        } else {
            vec![Space::new().width(86).into()]
        };
        let extra = vec![
            w::with_tooltip(look, ch::title_button(look, MENU, self.menu.is_some_and(|(k, _)| k == MenuKind::App), Some(Msg::Menu(Some(MenuKind::App)))), "Menu", None),
            w::with_tooltip(look, ch::title_button(look, SETTINGS, self.dialog == Some(Dialog::Settings), Some(Msg::Dialog(Some(Dialog::Settings)))), "Instellingen", Some("Ctrl+,")),
        ];
        let window = WindowActions { drag: Msg::TitlePress, minimize: Msg::Minimize, maximize: Msg::Maximize, close: Msg::CloseWindow, maximized: self.maximized };
        ch::title_bar(look, name, quick_buttons, extra, window, WINDOW_ICONS)
    }

    /// Lines of the open menu.
    /// Every command of the sample app, in one place (issue #9). The ribbon, the
    /// context menus, the title bar and the shortcuts all read from this list, so
    /// a label, state or key never differs between them.
    fn commands(&self) -> Vec<Command<Msg>> {
        let mut list = self.default_commands();
        self.keymap.apply(&mut list);
        list
    }

    /// The commands with the app's own shortcuts, before the keymap.
    fn default_commands(&self) -> Vec<Command<Msg>> {
        let selection = self.selected.is_some();
        let doc = self.docs.get(self.active).map(|d| d.kind);
        vec![
            Command::new("file.new", "Nieuw", Msg::New).icon(NEW_SMALL, NEW).shortcut(Shortcut::ctrl('n')),
            Command::new("file.open", "Openen", Msg::Backstage(true)).icon(OPEN_SMALL, OPEN).shortcut(Shortcut::ctrl('o')),
            Command::new("file.save", "Opslaan", Msg::Save).icon(SAVE_SMALL, SAVE).shortcut(Shortcut::ctrl('s')),
            Command::new("file.export", "Exporteren…", Msg::Dialog(Some(Dialog::Export))).icon(EXPORT_SMALL, EXPORT).shortcut(Shortcut::ctrl('e')).dialog(),
            Command::new("file.print", "Afdrukken…", Msg::Dialog(Some(Dialog::Print))).icon(PRINT_SMALL, PRINT).shortcut(Shortcut::ctrl('p')).dialog(),
            Command::new("doc.close", "Sluiten", Msg::CloseActive).icon_small(CLOSE).shortcut(Shortcut::ctrl('w')),
            Command::new("edit.undo", "Ongedaan", Msg::Undo).icon(UNDO_SMALL, UNDO).shortcut(Shortcut::ctrl('z')).enabled(!self.history.is_empty()),
            Command::new("edit.redo", "Opnieuw", Msg::Redo).icon(REDO_SMALL, REDO).shortcut(Shortcut::ctrl('y')).enabled(!self.future.is_empty()),
            Command::new("edit.cut", "Knippen", Msg::Cut).icon_small(CUT).shortcut(Shortcut::ctrl('x')).enabled(selection),
            Command::new("edit.copy", "Kopiëren", Msg::Copy).icon_small(COPY).shortcut(Shortcut::ctrl('c')).enabled(selection),
            Command::new("edit.paste", "Plakken", Msg::Paste).icon(b2!("16", "edit.paste"), PASTE).shortcut(Shortcut::ctrl('v')).enabled(self.clipboard.is_some()),
            Command::new("edit.delete", "Verwijderen", Msg::Delete).icon_small(DELETE).shortcut(Shortcut::named(keyboard::key::Named::Delete)).danger().enabled(selection),
            Command::new("insert.item", "Nieuwe post", Msg::AddItem).icon(b2!("16", "budget.add-item"), ADD_ITEM),
            Command::new("insert.chapter", "Nieuw hoofdstuk", Msg::AddChapter).icon(b2!("16", "budget.add-chapter"), ADD_CHAPTER),
            Command::new("view.table", "Tabel", Msg::OpenDoc(DocKind::Budget)).icon(TABLE_SMALL, TABLE).mode(doc == Some(DocKind::Budget)),
            Command::new("view.chart", "Grafiek", Msg::OpenDoc(DocKind::Chart)).icon(b2!("16", "data.chart"), CHART).mode(doc == Some(DocKind::Chart)),
            Command::new("calc.recalculate", "Herberekenen", Msg::Recalculate).icon(b2!("16", "calculation.recalculate"), RECALC),
            Command::new("calc.audit", "Controleren", Msg::Audit).icon(b2!("16", "calculation.audit"), AUDIT).toggle(self.banner.is_some()),
            Command::new("view.zoom-in", "Inzoomen", Msg::ZoomIn).icon_small(ZOOM_IN).shortcut(Shortcut::ctrl('+')),
            Command::new("view.zoom-out", "Uitzoomen", Msg::ZoomOut).icon_small(ZOOM_OUT).shortcut(Shortcut::ctrl('-')),
            Command::new("view.zoom-fit", "100%", Msg::ZoomFit).icon_small(FIT).shortcut(Shortcut::ctrl('0')).mode(self.zoom == 100),
            Command::new("view.grid", "Raster", Msg::ToggleGrid).icon(b2!("16", "view.grid"), GRID).toggle(self.grid),
            Command::new("view.left", "Structuur", Msg::ToggleLeft).icon(PANEL_LEFT, LEFT_LARGE).shortcut(Shortcut::ctrl('1')).toggle(self.show_left),
            Command::new("view.right", "Eigenschappen", Msg::ToggleRight).icon(PANEL_RIGHT, RIGHT_LARGE).shortcut(Shortcut::ctrl('2')).toggle(self.show_right),
            Command::new("app.settings", "Instellingen…", Msg::Dialog(Some(Dialog::Settings))).icon(SETTINGS, SETTINGS_LARGE).shortcut(Shortcut::ctrl(',')).dialog(),
            Command::new("report.generate", "Rapport maken", Msg::GenerateReport).icon(b2!("16", "report.generate"), REPORT),
        ]
    }

    /// One command from [`Self::commands`].
    fn command(&self, id: &str) -> Command<Msg> {
        self.commands().into_iter().find(|c| c.id == id).unwrap_or_else(|| panic!("unknown command {id}"))
    }

    fn menu_items(&self, kind: MenuKind) -> Vec<MenuItem<'static, Msg>> {
        let item_menu = |id: u32| {
            vec![
                MenuItem::action(Some(ITEM), "Openen in tab", None, Some(Msg::OpenItem(id))),
                MenuItem::Separator,
                cm::menu_item(&self.command("edit.cut")),
                cm::menu_item(&self.command("edit.copy")),
                cm::menu_item(&self.command("edit.paste")),
                MenuItem::Separator,
                cm::menu_item(&self.command("insert.item")),
                MenuItem::Separator,
                cm::menu_item(&self.command("edit.delete")),
            ]
        };
        match kind {
            MenuKind::Row(id) | MenuKind::Tree(TreeSel::Item(id)) => item_menu(id),
            MenuKind::Tree(TreeSel::Chapter(key)) => {
                let open = self.open_chapters.contains(key);
                vec![
                    MenuItem::Heading(CHAPTERS.iter().find(|(k, _)| *k == key).map_or("Hoofdstuk", |(_, n)| n)),
                    MenuItem::action(Some(if open { COLLAPSE } else { EXPAND }), if open { "Inklappen" } else { "Uitklappen" }, None, Some(Msg::ToggleChapter(key))),
                    MenuItem::action(Some(TABLE_SMALL), "Begroting openen", None, Some(Msg::OpenDoc(DocKind::Budget))),
                    MenuItem::Separator,
                    cm::menu_item(&self.command("insert.chapter")),
                ]
            }
            MenuKind::Tree(TreeSel::Root) => vec![
                MenuItem::Heading(PROJECTS[self.project].0),
                MenuItem::action(Some(if self.root_open { COLLAPSE } else { EXPAND }), if self.root_open { "Inklappen" } else { "Uitklappen" }, None, Some(Msg::ToggleRoot)),
                MenuItem::action(Some(TABLE_SMALL), "Begroting openen", None, Some(Msg::OpenDoc(DocKind::Budget))),
                MenuItem::action(Some(b2!("16", "data.chart")), "Grafiek openen", None, Some(Msg::OpenDoc(DocKind::Chart))),
                MenuItem::Separator,
                cm::menu_item(&self.command("file.save")),
            ],
            MenuKind::Tab(i) => vec![
                // The tab menu closes this tab: the same command with its own message.
                cm::menu_item(&Command { message: Msg::CloseDoc(i), ..self.command("doc.close") }),
                MenuItem::action(None, "Andere tabs sluiten", None, (self.docs.len() > 1).then_some(Msg::CloseOthers(i))),
                MenuItem::action(None, "Alle tabs sluiten", None, Some(Msg::CloseAll)),
                MenuItem::Separator,
                cm::menu_item(&self.command("file.save")),
            ],
            MenuKind::App => vec![
                MenuItem::Heading("Weergave"),
                MenuItem::check("Structuur", Some("Ctrl+1"), self.show_left, Msg::ToggleLeft),
                MenuItem::check("Eigenschappen", Some("Ctrl+2"), self.show_right, Msg::ToggleRight),
                MenuItem::check("Raster", None, self.grid, Msg::ToggleGrid),
                MenuItem::Separator,
                MenuItem::action(Some(SETTINGS), "Instellingen", Some("Ctrl+,"), Some(Msg::Dialog(Some(Dialog::Settings)))),
                MenuItem::action(Some(HOME), "Startscherm", None, Some(Msg::Restart)),
                MenuItem::Separator,
                MenuItem::action(Some(CLOSE), "Afsluiten", Some("Alt+F4"), Some(Msg::CloseWindow)),
            ],
        }
    }

    fn plain_status(&self, look: Look, status: &str) -> Element<'_, Msg> {
        w::status_bar(look, vec![status.to_string()], vec!["UI 0.4".into()])
    }

    /// A small picture of an estimate in the workspace colours: the preview on a
    /// project card (besluit 2.3-3).
    fn mini_preview(look: Look, seed: usize) -> Element<'static, Msg> {
        let c = look.color;
        let lines: [u16; 4] = [[9, 6, 8, 4], [7, 9, 5, 8], [8, 4, 9, 6], [6, 8, 7, 9]][seed % 4];
        let mut sheet = column![].spacing(5).width(150);
        for (i, len) in lines.into_iter().enumerate() {
            let color = if i == 0 { look.workspace_accent_text } else { iced::Color { a: 0.45, ..c.workspace_text } };
            sheet = sheet.push(row![
                container(Space::new().width(Length::Fill).height(5)).width(Length::FillPortion(len)).style(move |_| container::Style {
                    background: Some(Background::Color(color)),
                    border: iced::Border { radius: 2.0.into(), ..Default::default() },
                    ..Default::default()
                }),
                Space::new().width(Length::FillPortion(10 - len)),
            ]);
        }
        sheet.into()
    }

    fn project_grid(&self, look: Look) -> Element<'_, Msg> {
        let statuses = [Some((Tone::Warning, "2 posten zonder prijs")), Some((Tone::Success, "Gereed")), None, Some((Tone::Info, "Concept"))];
        let mut grid = column![].spacing(12);
        for pair in [0usize, 2] {
            let mut line = row![].spacing(12);
            for (i, status) in statuses.iter().enumerate().skip(pair).take(2) {
                let (name, kind, when) = PROJECTS[i];
                // Havenkade has no preview, so its card shows the app icon.
                let preview = (i != 2).then(|| Self::mini_preview(look, i));
                line = line.push(container(t::project_card(look, preview, TABLE, name, card_meta(kind, when), *status, Some(Msg::OpenProject(i)))).width(Length::FillPortion(1)));
            }
            grid = grid.push(line);
        }
        grid.into()
    }

    fn recent_list(&self, look: Look) -> Element<'_, Msg> {
        let files = RECENT_FILES.iter().enumerate().map(|(i, (name, path, date))| RecentFile { icon: ITEM, name, path, date, on_press: Some(Msg::OpenProject(i.min(3))) }).collect();
        t::recent_files(look, files)
    }

    /// The start screen (besluit 2.5-1): no ribbon or panels. New on the left with
    /// task tiles; recent projects as cards and recent files on the right.
    fn start_screen(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let left = column![
            wf::page_heading(look, "Voorbeeldstudio", Some("Begrotingen voor bouwprojecten")),
            Space::new().height(4),
            w::mono_label(look, "Nieuw"),
            t::task_tile(look, NEW, "Lege begroting", "Begin zonder posten.", Some(Msg::OpenProject(0))),
            t::task_tile(look, ADD_CHAPTER, "Vanaf sjabloon", "Woningbouw, utiliteit of renovatie.", Some(Msg::OpenProject(0))),
            t::task_tile(look, OPEN_LARGE, "Bestand openen", "Kies een begroting op deze computer.", Some(Msg::OpenProject(1))),
            Space::new().height(8),
            t::info_card(look, "Over", vec![("Versie", "UI 0.4 · voorbeeld".into()), ("Thema", self.theme.name().into()), ("Licentie", "nog te bepalen".into())]),
        ]
        .spacing(8)
        .width(340);
        let right = column![w::mono_label(look, "Recente projecten"), self.project_grid(look), Space::new().height(4), w::mono_label(look, "Recente bestanden"), self.recent_list(look)]
            .spacing(12)
            .width(Length::Fill);
        container(scrollable(container(row![left, right].spacing(40)).padding(32).max_width(1180)).height(Length::Fill))
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() })
            .into()
    }

    /// The workflow app: no ribbon; a sidebar or steps, a 22 px heading, cards and an action bar.
    fn workflow(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let s = &self.wf;
        let number_error = |value: &str| parse_nl(value).is_none().then_some("Geen getal");
        let content: Element<'_, Msg> = match s.section {
            0 => column![
                wf::page_heading(look, "Project", Some("Gegevens van de woning die je beoordeelt.")),
                wf::form_card(
                    look,
                    "Projectgegevens",
                    column![
                        w::property_row(look, "Projectnaam", w::text_field(look, "Naam", &s.project, Some(Msg::WfProject), D::Regular, None)),
                        w::property_row(look, "Adres", w::text_field(look, "Straat, postcode en plaats", &s.address, Some(Msg::WfAddress), D::Regular, None)),
                        w::property_row(look, "Bouwjaar", w::text_field(look, "1978", &s.year, Some(Msg::WfYear), D::Regular, s.year.parse::<u32>().is_err().then_some("Vul een jaartal in."))),
                    ]
                    .spacing(4)
                    .into()
                ),
                t::info_card(look, "Opname", vec![("Adviseur", "N. de Vries".into()), ("Datum opname", "22 oktober 2026".into()), ("Methode", "NTA 8800, basisopname".into())]),
            ]
            .spacing(16)
            .into(),
            1 => {
                let mut tiles = row![].spacing(12);
                for (i, (icon, name, note)) in BUILDING_TYPES.iter().enumerate() {
                    tiles = tiles.push(container(t::choice_tile(look, icon, name, note, s.kind == i, Msg::WfType(i))).width(Length::FillPortion(1)));
                }
                column![
                    wf::page_heading(look, "Gebouw", Some("Kies het type gebouw en vul de oppervlakte in.")),
                    tiles,
                    wf::form_card(look, "Afmetingen", w::property_row(look, "Gebruiksoppervlakte (m²)", w::text_field(look, "124", &s.area, Some(Msg::WfArea), D::Regular, number_error(&s.area)))),
                ]
                .spacing(16)
                .into()
            }
            2 => column![
                wf::page_heading(look, "Schil", Some("Isolatiewaarden van de gebouwschil.")),
                wf::form_card(
                    look,
                    "Isolatie",
                    column![
                        w::property_row(look, "Rc gevel (m²K/W)", w::text_field(look, "2,5", &s.rc_wall, Some(Msg::WfRcWall), D::Regular, number_error(&s.rc_wall))),
                        w::property_row(look, "Rc dak (m²K/W)", w::text_field(look, "3,5", &s.rc_roof, Some(Msg::WfRcRoof), D::Regular, number_error(&s.rc_roof))),
                        w::property_row(look, "Rc vloer (m²K/W)", w::text_field(look, "2,0", &s.rc_floor, Some(Msg::WfRcFloor), D::Regular, number_error(&s.rc_floor))),
                        w::property_row(look, "U-waarde ramen (W/m²K)", w::text_field(look, "1,4", &s.window_u, Some(Msg::WfWindowU), D::Regular, number_error(&s.window_u))),
                    ]
                    .spacing(4)
                    .into()
                ),
                w::banner(look, Tone::Info, INFO, "Een hogere Rc-waarde betekent beter isoleren.", CLOSE, None),
            ]
            .spacing(16)
            .into(),
            3 => column![
                wf::page_heading(look, "Installaties", Some("Verwarming, ventilatie en zonnepanelen.")),
                wf::form_card(
                    look,
                    "Verwarming en ventilatie",
                    column![
                        w::property_row(look, "Verwarming", w::select(look, &HEATING, Some(s.heating), Msg::WfHeating, D::Regular)),
                        w::property_row(look, "Ventilatie", w::select(look, &VENTILATION, Some(s.ventilation), Msg::WfVentilation, D::Regular)),
                    ]
                    .spacing(4)
                    .into()
                ),
                wf::form_card(
                    look,
                    "Zonnepanelen",
                    column![
                        w::switch(look, "Zonnepanelen aanwezig", s.solar, Some(Msg::WfSolar)),
                        w::property_row(
                            look,
                            "Aantal panelen",
                            if s.solar { w::slider(look, 0.0..=24.0, s.panels, Msg::WfPanels, format!("{}", s.panels as u32)) } else { w::secondary(look, "Geen zonnepanelen").into() }
                        ),
                    ]
                    .spacing(8)
                    .into()
                ),
            ]
            .spacing(16)
            .into(),
            _ => {
                let figures = row![
                    t::figure_tile(look, if s.calculated { s.label() } else { "–" }, "Energielabel", true),
                    t::figure_tile(look, if s.calculated { nl(s.energy(), 0) } else { "–".into() }, "kWh/m² per jaar", false),
                    t::figure_tile(look, if s.solar { format!("{}", s.panels as u32) } else { "0".into() }, "Zonnepanelen", false),
                ]
                .spacing(12);
                let mut col = column![wf::page_heading(look, "Resultaat", Some("Bereken het label met de knop rechtsonder.")), figures].spacing(16);
                if s.calculated {
                    col = col.push(t::info_card(
                        look,
                        "Uitgangspunten",
                        vec![
                            ("Gebouw", BUILDING_TYPES[s.kind].1.into()),
                            ("Oppervlakte", format!("{} m²", s.area)),
                            ("Verwarming", s.heating.into()),
                            ("Ventilatie", s.ventilation.into()),
                        ],
                    ));
                } else {
                    col = col.push(w::banner(look, Tone::Warning, WARNING, "Nog niet berekend. De waarden kunnen nog veranderen.", CLOSE, None));
                }
                col.into()
            }
        };
        let last = s.section == SECTIONS.len() - 1;
        let actions = wf::action_bar(
            look,
            vec![w::button(look, "Opslaan", K::Quiet, D::Regular, Some(SAVE_SMALL), Some(Msg::Save))],
            vec![
                w::button(look, "Vorige", K::Secondary, D::Regular, Some(BACK), (s.section > 0).then_some(Msg::WfPrevious)),
                if last {
                    w::button(look, "Berekenen", K::Primary, D::Regular, None, Some(Msg::WfCalculate))
                } else {
                    w::button(look, "Volgende", K::Primary, D::Regular, Some(NEXT), Some(Msg::WfNext))
                },
            ],
        );
        let page = container(scrollable(container(container(content).max_width(860)).padding(28).center_x(Length::Fill)).height(Length::Fill))
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() });
        let done: Vec<bool> = (0..SECTIONS.len()).map(|i| (s.visited[i] && i < s.section) || (s.calculated && i != s.section)).collect();
        let body: Element<'_, Msg> = match s.navigation {
            Navigation::Sidebar => row![wf::sidebar(look, "Energielabel", &SECTIONS, s.section, Msg::WfSection), column![page, actions].width(Length::Fill)].height(Length::Fill).into(),
            Navigation::Steps => column![wf::step_bar(look, &SECTIONS, s.section, &done, DONE, Msg::WfSection), page, actions].height(Length::Fill).into(),
        };
        column![
            self.title_bar(look, format!("{} · Energielabel · OpenAEC", s.project), false),
            w::divider(look),
            body,
            w::status_bar(
                look,
                vec![format!("Stap {} van {}", s.section + 1, SECTIONS.len()), s.address.clone()],
                vec![if s.calculated { format!("Label {}", s.label()) } else { "Niet berekend".into() }],
            ),
        ]
        .into()
    }

    /// The OpenAEC Installer, proposal E (design/ontwerp-0.4/installer-voorstellen.html#E):
    /// only the top band is dark, everything below follows the theme. Desktop apps and
    /// web tools are two sections with the same website tiles.
    /// Source: harmonization/references/openaec-installer at 8b39bae.
    fn installer(&self, look: Look) -> Element<'_, Msg> {
        let s = &self.inst;
        let content: Element<'_, Msg> = match s.active.and_then(|t| s.tabs.get(t)) {
            Some(&tool) => self.web_tool_view(look, tool),
            None => self.installer_catalog(look),
        };
        let desktop = TOOLS.iter().filter(|t| !t.web).count();
        let installed = (0..TOOLS.len()).filter(|&i| !TOOLS[i].web && s.tools[i].installed.is_some()).count();
        let updates = s.count(Filter::Updates);
        column![
            self.title_bar(look, "OpenAEC Installer".into(), false),
            w::divider(look),
            content,
            w::status_bar(
                look,
                vec![
                    format!("{installed} van {desktop} desktop-apps geïnstalleerd"),
                    match updates {
                        0 => "Alles is bijgewerkt".into(),
                        1 => "1 update beschikbaar".into(),
                        n => format!("{n} updates beschikbaar"),
                    },
                ],
                vec![if s.refreshing { "Controleren…".into() } else { format!("installer {} · gecontroleerd {}", s.self_version, s.last_refresh) }],
            ),
        ]
        .height(Length::Fill)
        .into()
    }

    /// A web tool inside the installer, with a bar back to all tools. The real
    /// installer shows a web view here; the gallery shows the screenshot.
    fn web_tool_view(&self, look: Look, i: usize) -> Element<'_, Msg> {
        let c = look.color;
        let tool = &TOOLS[i];
        let bar = row![
            site_button(look, "Alle tools", SiteKind::Light, Some(BACK), Some(Msg::InstTab(None))),
            tool_logo(look, i, 32.0),
            column![text(tool.name).size(14).font(fonts::STRONG).color(c.text), text(format!("https://{}", tool.web_url.unwrap_or(""))).size(11).font(fonts::MONO).color(c.text_secondary)].spacing(1).width(Length::Fill),
            round_icon(look, WEB_RELOAD, "Opnieuw laden", Msg::Noop),
            round_icon(look, EXTERNAL, "Openen in browser", Msg::InstLaunch(i)),
        ]
        .spacing(12)
        .align_y(Alignment::Center)
        .padding([0, 16]);
        let view: Element<'_, Msg> = match preview_handle(i) {
            Some(handle) => container(iced::widget::image(handle).content_fit(iced::ContentFit::Contain).width(Length::Fill).height(Length::Fill)).padding(32).center(Length::Fill).into(),
            None => container(icon_tile_amber(look, tool.icon, 64.0)).center(Length::Fill).into(),
        };
        column![
            container(bar).height(52).width(Length::Fill).align_y(iced::alignment::Vertical::Center).style(move |_| container::Style { background: Some(Background::Color(c.panel)), ..Default::default() }),
            w::divider(look),
            container(view).width(Length::Fill).height(Length::Fill).style(move |_| container::Style { background: Some(Background::Color(c.workspace)), ..Default::default() }),
        ]
        .height(Length::Fill)
        .into()
    }

    fn installer_catalog(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let s = &self.inst;
        // The top band is the website's dark band in every theme except High contrast.
        let dark = if look.tokens.dark || look.high_contrast() { look } else { Look::from(ThemeId::Dark) };
        let d = dark.color;
        let query = s.search.trim().to_lowercase();
        let visible = |i: usize| {
            s.passes(i, s.filter)
                && s.disc.map_or(true, |x| TOOLS[i].disc.contains(x))
                && (query.is_empty() || format!("{} {} {}", TOOLS[i].name, TOOLS[i].description, TOOLS[i].category).to_lowercase().contains(&query))
        };
        let desktop: Vec<usize> = (0..TOOLS.len()).filter(|&i| !TOOLS[i].web && visible(i)).collect();
        let web: Vec<usize> = (0..TOOLS.len()).filter(|&i| TOOLS[i].web && visible(i)).collect();
        let updates = s.count(Filter::Updates);

        // Left of the band: label, heading with an accent part, actions and figures (proposal A).
        let stat = |value: usize, label: &'static str| -> Element<'_, Msg> {
            row![text(value.to_string()).size(12).font(fonts::MONO).color(d.text), text(label).size(12).font(fonts::MONO).color(d.text_secondary)].spacing(6).into()
        };
        let update_all = if updates == 0 { "Alles is bijgewerkt".to_string() } else { format!("Alles bijwerken ({updates})") };
        let left = column![
            section_label(dark, "OpenAEC Installer"),
            column![
                text("Alle bouwsoftware,").size(40).font(BOLD_HEADING).color(d.text),
                text("één plek.").size(40).font(BOLD_HEADING).color(d.accent_text),
            ],
            text("Ontdek, installeer, werk bij en start de open source tools van de OpenAEC Foundation.").size(16).font(fonts::BODY).color(d.text_secondary),
            Space::new().height(6),
            row![
                site_button_owned(dark, update_all, SiteKind::Primary, Some(UPDATE), (updates > 0).then_some(Msg::InstUpdateAll), false),
                site_button(dark, if s.refreshing { "Controleren…" } else { "Controleren op updates" }, SiteKind::Glass, Some(CHECK_UPDATES), (!s.refreshing).then_some(Msg::InstRefresh)),
            ]
            .spacing(12),
            Space::new().height(4),
            row![
                stat(TOOLS.len(), "TOOLS"),
                stat(s.count(Filter::Installed), "GEÏNSTALLEERD"),
                stat(updates, "UPDATES"),
                stat(s.count(Filter::Web), "WEBTOOLS"),
            ]
            .spacing(22),
        ]
        .spacing(12)
        .width(Length::Fill);

        // Right of the band: the featured tool that changes every six seconds (proposal D).
        let featured = s.featured();
        let f = featured[s.feature % featured.len()];
        let mut dots = row![].spacing(6);
        for (n, _) in featured.iter().enumerate() {
            let on = n == s.feature % featured.len();
            dots = dots.push(
                iced::widget::button(Space::new().width(22).height(4))
                    .padding(0)
                    .on_press(Msg::InstFeature(n))
                    .style(move |_, _| iced::widget::button::Style { background: Some(Background::Color(if on { d.accent } else { alpha(iced::Color::WHITE, 0.18) })), border: iced::Border { radius: 2.0.into(), ..Default::default() }, ..Default::default() }),
            );
        }
        let shot: Element<'_, Msg> = match preview_handle(f) {
            Some(handle) => iced::widget::image(handle).content_fit(iced::ContentFit::Contain).width(Length::Fill).into(),
            None => container(icon_tile_amber(dark, TOOLS[f].icon, 64.0)).center_x(Length::Fill).height(200).align_y(iced::alignment::Vertical::Center).into(),
        };
        let spot = container(
            column![
                row![section_label(dark, if s.has_update(f) { "Nieuwe versie" } else { "Uitgelicht" }), Space::new().width(Length::Fill), dots].align_y(Alignment::Center),
                shot,
                row![
                    tool_logo(dark, f, 40.0),
                    column![text(TOOLS[f].name).size(18).font(BOLD_HEADING).color(d.text), version_line(dark, s, f)].spacing(2).width(Length::Fill),
                    self.tool_action(dark, f),
                ]
                .spacing(12)
                .align_y(Alignment::Center),
            ]
            .spacing(14),
        )
        .padding(16)
        .width(540)
        .style(move |_| glass_style(dark));

        let band = column![
            container(row![left, spot].spacing(40).align_y(Alignment::Center))
                .padding(iced::Padding { top: 40.0, right: 44.0, bottom: 40.0, left: 48.0 })
                .width(Length::Fill)
                .style(move |_| dark_band_style(dark)),
            container(Space::new().width(Length::Fill).height(3)).height(3).style(move |_| container::Style { background: Some(Background::Color(d.accent)), ..Default::default() }),
        ];

        // Below the band everything follows the theme.
        let mut pills = row![].spacing(8).align_y(Alignment::Center);
        for (filter, name) in [(Filter::All, "Alle"), (Filter::Installed, "Geïnstalleerd"), (Filter::Updates, "Updates")] {
            pills = pills.push(pill(look, None, name, s.count(filter), s.filter == filter && (filter != Filter::All || s.disc.is_none()), Msg::InstFilter(filter)));
        }
        for (letter, name) in DISCIPLINES {
            let n = TOOLS.iter().filter(|t| t.disc.contains(letter)).count();
            pills = pills.push(pill(look, Some(letter), name, n, s.disc == Some(letter), Msg::InstDisc(Some(letter))));
        }
        let grid = |ids: &[usize]| -> Element<'_, Msg> {
            let mut rows = column![].spacing(22);
            for chunk in ids.chunks(3) {
                let mut line = row![].spacing(22);
                for &i in chunk {
                    line = line.push(container(self.tool_card(look, i)).width(Length::FillPortion(1)));
                }
                for _ in chunk.len()..3 {
                    line = line.push(Space::new().width(Length::FillPortion(1)));
                }
                rows = rows.push(line);
            }
            rows.into()
        };
        let empty = |what: &'static str| -> Element<'_, Msg> { text(what).size(14).font(fonts::BODY).color(c.text_secondary).into() };

        let mut body = column![].spacing(30);
        if s.self_version == "1.5.0" && (!s.self_dismissed || s.self_update.is_some()) {
            let action: Element<'_, Msg> = match s.self_update {
                Some(p) => container(w::progress(look, p)).width(120).into(),
                None => w::button(look, "Bijwerken naar 1.6.0", K::Primary, D::Compact, None, Some(Msg::InstSelfUpdate)),
            };
            body = body.push(w::banner_with_action(look, Tone::Info, INFO, "Er is een nieuwe versie van de installer: 1.6.0. Je hebt 1.5.0.", Some(action), CLOSE, Some(Msg::InstDismissSelf)));
        }
        body = body.push(pills.wrap());
        body = body.push(
            column![
                row![
                    section_head(look, &format!("Desktop-apps · {}", desktop.len()), "Installeren en starten op je computer", "Windows-installers en AppImages van GitHub Releases. De installer ziet welke versie je hebt."),
                    Space::new().width(Length::Fill),
                    container(w::text_field(look, "Zoek een tool", &s.search, Some(Msg::InstSearch), D::Regular, None)).width(260),
                ]
                .align_y(Alignment::End),
                if desktop.is_empty() { empty("Geen desktop-apps voor dit filter.") } else { grid(&desktop) },
            ]
            .spacing(18),
        );
        let line = || container(Space::new().width(Length::Fill).height(1)).height(1).width(Length::Fill).style(move |_| container::Style { background: Some(Background::Color(c.border_strong)), ..Default::default() });
        body = body.push(
            row![line(), row![w::glyph(WEBTAB, 14.0, c.text_secondary, c.accent_text), text("WEBTOOLS").size(11).font(fonts::MONO).color(c.text_secondary)].spacing(8).align_y(Alignment::Center), line()]
                .spacing(14)
                .align_y(Alignment::Center),
        );
        body = body.push(
            column![
                section_head(look, &format!("Webtools · {}", web.len()), "Direct in je browser", "Geen installatie nodig. Ze openen in de installer of in je eigen browser."),
                if web.is_empty() { empty("Geen webtools voor dit filter.") } else { grid(&web) },
            ]
            .spacing(18),
        );

        container(scrollable(column![band, container(container(body).max_width(1200)).padding([28, 40]).center_x(Length::Fill)]).height(Length::Fill))
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() })
            .into()
    }

    /// The main action of a tool: open, install, update or start; while installing, the progress.
    fn tool_action(&self, look: Look, i: usize) -> Element<'_, Msg> {
        let c = look.color;
        let tool = &TOOLS[i];
        let state = &self.inst.tools[i];
        if let Some(p) = state.progress {
            return column![w::progress(look, p), text(format!("Downloaden… {:.0}%", p * 100.0)).size(11).font(fonts::BODY).color(c.text_secondary)].spacing(5).width(160).into();
        }
        if tool.web {
            site_button_owned(look, "Openen".into(), SiteKind::Primary, Some(WEBTAB), Some(Msg::InstOpenWeb(i)), true)
        } else if state.installed.is_none() {
            site_button_owned(look, "Installeren".into(), SiteKind::Primary, Some(INSTALL), Some(Msg::InstInstall(i)), true)
        } else if self.inst.has_update(i) {
            site_button_owned(look, "Bijwerken".into(), SiteKind::Primary, Some(UPDATE), Some(Msg::InstInstall(i)), true)
        } else {
            site_button_owned(look, "Starten".into(), SiteKind::Primary, Some(LAUNCH), Some(Msg::InstLaunch(i)), true)
        }
    }

    /// A website tile of proposal E: screenshot fading into the tile, logo or category
    /// icon next to the name, discipline and status chips, description, version and
    /// commits in mono, the main button and round buttons that always fit.
    fn tool_card(&self, look: Look, i: usize) -> Element<'_, Msg> {
        let c = look.color;
        let tool = &TOOLS[i];
        let state = &self.inst.tools[i];
        let update = self.inst.has_update(i);
        let launchable = !tool.web && state.installed.is_some();
        let shortcut = if launchable { Some(Msg::InstLaunch(i)) } else if tool.web_url.is_some() { Some(Msg::InstOpenWeb(i)) } else { None };

        let picture: Element<'_, Msg> = match preview_handle(i) {
            // The PNG has rounded corners and fades out at the bottom; Contain keeps it inside the scroll area.
            Some(handle) => iced::widget::image(handle).content_fit(iced::ContentFit::Contain).width(Length::Fill).into(),
            None => container(icon_tile_amber(look, tool.icon, 64.0))
                .center_x(Length::Fill)
                .height(150)
                .align_y(iced::alignment::Vertical::Center)
                .style(move |_| container::Style {
                    background: Some(if look.high_contrast() { Background::Color(c.panel) } else { gradient(&[(0.0, alpha(c.accent, 0.12)), (1.0, alpha(c.accent, 0.03))]) }),
                    border: iced::Border { radius: 8.0.into(), ..Default::default() },
                    ..Default::default()
                })
                .into(),
        };
        let preview = iced::widget::button(picture).padding(0).width(Length::Fill).on_press_maybe(shortcut).style(move |_, _| iced::widget::button::Style { snap: false,
            background: None,
            text_color: c.text,
            border: iced::Border::default(),
            shadow: iced::Shadow::default(),
        });
        let preview = w::with_tooltip(look, preview.into(), if launchable { "Starten" } else if tool.web_url.is_some() { "Openen" } else { "Geen voorbeeld" }, None);

        let mut chips = row![].spacing(5).align_y(Alignment::Center);
        for letter in tool.disc.chars() {
            chips = chips.push(chip(look, &letter.to_string(), None));
        }
        if state.progress.is_some() {
            chips = chips.push(chip(look, "Bezig", Some(Tone::Info)));
        } else if update {
            chips = chips.push(chip(look, "Update", Some(Tone::Warning)));
        } else if tool.web {
            chips = chips.push(chip(look, "Web", Some(Tone::Info)));
        } else if state.installed.is_some() {
            chips = chips.push(chip(look, "Geïnstalleerd", Some(Tone::Success)));
        }
        if !tool.site.is_empty() {
            chips = chips.push(chip(look, tool.site, (tool.site == "Beta").then_some(Tone::Warning)));
        }
        let head = row![tool_logo(look, i, 44.0), column![text(tool.name).size(16).font(BOLD_HEADING).color(c.text), chips.wrap()].spacing(6).width(Length::Fill)]
            .spacing(12)
            .align_y(Alignment::Center);

        let mut meta = row![version_line(look, &self.inst, i)].spacing(10).align_y(Alignment::Center);
        if tool.commits > 0 {
            meta = meta.push(text(format!("● {} commits", tool.commits)).size(11).font(fonts::MONO).color(c.text_secondary));
        }

        let mut icons = row![].spacing(6).align_y(Alignment::Center);
        if update && state.progress.is_none() {
            icons = icons.push(round_icon(look, LAUNCH, "Huidige versie starten", Msg::InstLaunch(i)));
        }
        if let Some(repo) = tool.repo {
            icons = icons.push(round_icon_owned(look, GITHUB, format!("Broncode op GitHub · {repo}"), Msg::InstGitHub(i)));
        }
        if !tool.web && tool.web_url.is_some() {
            icons = icons.push(round_icon(look, WEBTAB, "Webversie hier openen", Msg::InstOpenWeb(i)));
        }
        if tool.web_url.is_some() {
            icons = icons.push(round_icon(look, EXTERNAL, "Openen in browser", Msg::InstLaunch(i)));
        }

        let card = column![
            preview,
            head,
            text(tool.description).size(13).font(fonts::BODY).color(c.text_secondary).height(58),
            meta,
            container(row![self.tool_action(look, i), Space::new().width(Length::Fill), icons].spacing(8).align_y(Alignment::Center)).height(40).align_y(iced::alignment::Vertical::Center),
        ]
        .spacing(12);
        container(card).padding(18).width(Length::Fill).style(move |_| site_card_style(look, update)).into()
    }

    fn dialog_card(&self, look: Look, dialog: Dialog) -> Element<'_, Msg> {
        let close = Some(Msg::Dialog(None));
        match dialog {
            Dialog::Settings => {
                let hc = look.high_contrast();
                let workspace: Element<'_, Msg> = if hc { w::secondary(look, "Bepaald door High contrast").into() } else { w::select(look, &WorkspaceSetting::ALL, Some(self.workspace), Msg::Workspace, D::Regular) };
                let statusbar: Element<'_, Msg> = if hc { w::secondary(look, "Bepaald door High contrast").into() } else { w::select(look, &StatusbarSetting::ALL, Some(self.statusbar), Msg::Statusbar, D::Regular) };
                let content = column![
                    w::mono_label(look, "Weergave"),
                    w::property_row(look, "Thema", w::select(look, &ThemeId::ALL, Some(self.theme), Msg::Theme, D::Regular)),
                    w::property_row(look, "Werkruimte", workspace),
                    container(w::secondary(look, "Kleur van het vlak waarin je document staat.")).padding([0, 8]),
                    w::property_row(look, "Statusbalk", statusbar),
                    w::property_row(look, "Taal", w::select(look, &["Nederlands"], Some("Nederlands"), |_| Msg::Noop, D::Regular)),
                    Space::new().height(6),
                    w::mono_label(look, if self.view == View::Workflow { "Werkstroom" } else { "Opstarten" }),
                ]
                .spacing(6);
                let content = if self.view == View::Workflow {
                    content.push(w::property_row(look, "Navigatie", w::select(look, &Navigation::ALL, Some(self.wf.navigation), Msg::WfNavigation, D::Regular)))
                } else {
                    content
                        .push(container(w::checkbox(look, "Laatste project direct openen", self.skip_start, Some(Msg::SkipStart))).padding([4, 8]))
                        .push(container(w::secondary(look, "Sla het startscherm over. Kies Herstart bovenaan om het te zien werken.")).padding([0, 8]))
                };
                let tab = |page, label| w::button(look, label, if self.settings_page == page { K::Secondary } else { K::Quiet }, D::Compact, None, Some(Msg::SettingsPage(page)));
                let tabs = row![tab(SettingsPage::General, "Algemeen"), tab(SettingsPage::Shortcuts, "Sneltoetsen")].spacing(4);
                let body: Element<'_, Msg> = match self.settings_page {
                    SettingsPage::General => content.into(),
                    SettingsPage::Shortcuts => sc::page(look, &self.shortcuts, &self.commands(), &self.keymap, &COMMAND_GROUPS, Msg::Shortcuts),
                };
                w::dialog(look, "Instellingen", CLOSE, close, column![tabs, body].spacing(14).into(), None, vec![w::button(look, "Sluiten", K::Primary, D::Regular, None, Some(Msg::Dialog(None)))], true)
            }
            Dialog::Export => {
                let mut formats = column![w::secondary(look, "Kies het formaat van het bestand.")].spacing(10);
                for f in FORMATS {
                    formats = formats.push(w::radio(look, f, f, Some(self.format), Msg::Format));
                }
                w::dialog(
                    look,
                    "Begroting exporteren",
                    CLOSE,
                    close,
                    formats.into(),
                    None,
                    vec![w::button(look, "Annuleren", K::Secondary, D::Regular, None, Some(Msg::Dialog(None))), w::button(look, "Exporteren", K::Primary, D::Regular, None, Some(Msg::ConfirmExport))],
                    false,
                )
            }
            Dialog::Print => {
                let content = column![
                    w::secondary(look, "De begroting wordt op de standaardprinter afgedrukt."),
                    w::radio(look, "Staand", false, Some(self.landscape), Msg::Landscape),
                    w::radio(look, "Liggend", true, Some(self.landscape), Msg::Landscape),
                ]
                .spacing(10);
                w::dialog(
                    look,
                    "Afdrukken",
                    CLOSE,
                    close,
                    content.into(),
                    None,
                    vec![w::button(look, "Annuleren", K::Secondary, D::Regular, None, Some(Msg::Dialog(None))), w::button(look, "Afdrukken", K::Primary, D::Regular, None, Some(Msg::ConfirmPrint))],
                    false,
                )
            }
            Dialog::Quit => w::dialog(
                look,
                "Wijzigingen opslaan?",
                CLOSE,
                close,
                w::secondary(look, "Er zijn wijzigingen die nog niet zijn opgeslagen. Wil je ze opslaan voordat je afsluit?").into(),
                Some(w::button(look, "Niet opslaan", K::Quiet, D::Regular, None, Some(Msg::QuitNow))),
                vec![w::button(look, "Annuleren", K::Secondary, D::Regular, None, Some(Msg::Dialog(None))), w::button(look, "Opslaan en afsluiten", K::Primary, D::Regular, None, Some(Msg::SaveAndQuit))],
                false,
            ),
            Dialog::CloseDirty(i) => {
                let name = self.docs.get(i).map_or("dit document", |d| d.title.as_str());
                w::dialog(
                    look,
                    "Wijzigingen opslaan?",
                    CLOSE,
                    close,
                    w::secondary(look, format!("Er zijn wijzigingen in {name} die nog niet zijn opgeslagen.")).into(),
                    Some(w::button(look, "Niet opslaan", K::Quiet, D::Regular, None, Some(Msg::DiscardAndClose(i)))),
                    vec![w::button(look, "Annuleren", K::Secondary, D::Regular, None, Some(Msg::Dialog(None))), w::button(look, "Opslaan", K::Primary, D::Regular, None, Some(Msg::SaveAndClose(i)))],
                    false,
                )
            }
        }
    }

    /// Every component in its states.
    /// Every B2 icon, loaded from the `openaec-icons` crate as an app would load
    /// them: search, filter by app or group, and a panel with the icon in use.
    fn icons(&self, look: Look) -> Element<'_, Msg> {
        use openaec_icons::Size as IconSize;
        let c = look.color;
        let st = &self.icons;
        let found = st.matches();
        let pages = found.len().div_ceil(ICONS_PER_PAGE).max(1);
        let page = st.page.min(pages - 1);
        let (size, px) = if st.large { (IconSize::S24, 24.0) } else { (IconSize::S16, 16.0) };

        let size_button = |large: bool, label: &'static str| w::button(look, label, if st.large == large { K::Secondary } else { K::Quiet }, D::Compact, None, Some(Msg::IconLarge(large)));
        let controls = row![
            container(w::text_field(look, "Zoek op naam, id of groep", &st.search, Some(Msg::IconSearch), D::Compact, None)).width(280),
            container(w::select(look, app_choices(), Some(st.app), Msg::IconApp, D::Compact)).width(190),
            container(w::select(look, group_choices(), Some(st.group), Msg::IconGroup, D::Compact)).width(230),
            row![size_button(false, "16 px"), size_button(true, "24 px")].spacing(4),
        ]
        .spacing(8)
        .align_y(Alignment::Center);

        let grid: Element<'_, Msg> = if found.is_empty() {
            w::empty_state(look, SEARCH, "Geen iconen gevonden", "Pas de zoekterm of de filters aan.", None)
        } else {
            let mut tiles = row![].spacing(8);
            for &icon in found.iter().skip(page * ICONS_PER_PAGE).take(ICONS_PER_PAGE) {
                let chosen = st.selected == Some(icon);
                let label = text(icon.label()).size(font::SIZE_LABEL).font(fonts::BODY).color(c.text).width(Length::Fill).align_x(iced::alignment::Horizontal::Center);
                let tile = column![
                    container(w::glyph(icon.svg(size), px, c.text, c.accent_text)).center_x(Length::Fill).center_y(30),
                    container(label).height(30).width(Length::Fill).clip(true),
                ]
                .spacing(4);
                tiles = tiles.push(
                    focus::focusable(look, iced::widget::button(tile)
                        .width(140)
                        .height(84)
                        .padding([8, 6])
                        .on_press(Msg::IconSelect(icon))
                        .style(move |_, status| t::tile_style(look, status, chosen, openaec_ui::design::radius::MEDIUM)), true, 6.0),
                );
            }
            scrollable(container(tiles.wrap()).padding(iced::Padding { right: 12.0, ..Default::default() })).id(icon_grid_id()).height(Length::Fill).into()
        };
        let pager = row![
            w::button(look, "Vorige", K::Secondary, D::Compact, Some(BACK), (page > 0).then(|| Msg::IconPage(page - 1))),
            w::secondary(look, format!("Pagina {} van {} · {} van {} iconen", page + 1, pages, found.len(), Icon::all().len())),
            w::button(look, "Volgende", K::Secondary, D::Compact, Some(NEXT), (page + 1 < pages).then(|| Msg::IconPage(page + 1))),
        ]
        .spacing(8)
        .align_y(Alignment::Center);
        let left = column![
            column![
                w::heading(look, "Iconen B2", font::SIZE_PAGE_HEADING),
                w::secondary(look, format!("Alle iconen van Codex uit de crate openaec-icons, B2-revisie {}. Klik op een icoon voor de details.", openaec_icons::REVISION)),
            ]
            .spacing(4),
            controls,
            container(grid).height(Length::Fill),
            pager,
        ]
        .spacing(12)
        .padding(20)
        .width(Length::Fill)
        .height(Length::Fill);

        let detail: Element<'_, Msg> = match st.selected {
            Some(icon) => {
                let s16 = icon.svg(IconSize::S16);
                let s24 = icon.svg(IconSize::S24);
                // Each sample on the workspace colour, at its native size or enlarged.
                let sample = |source: &'static str, px: f32, accent: iced::Color, caption: &'static str| -> Element<'_, Msg> {
                    column![
                        container(w::glyph(source, px, c.workspace_text, accent)).center(64).style(move |_| container::Style {
                            background: Some(Background::Color(c.workspace)),
                            border: iced::Border { color: c.border, width: 1.0, radius: openaec_ui::design::radius::MEDIUM.into() },
                            ..Default::default()
                        }),
                        w::mono_label(look, caption),
                    ]
                    .spacing(4)
                    .align_x(Alignment::Center)
                    .into()
                };
                let accent = look.workspace_accent_text;
                let apps = icon.apps().iter().map(|a| app_name(a)).collect::<Vec<_>>().join(", ");
                column![
                    w::heading(look, icon.label(), font::SIZE_DIALOG_HEADING),
                    text(icon.id()).size(font::SIZE_LABEL).font(fonts::MONO).color(c.text_secondary),
                    row![sample(s16, 16.0, accent, "16 px"), sample(s24, 24.0, accent, "24 px"), sample(s24, 48.0, accent, "48 px"), sample(s24, 24.0, c.workspace_text, "Eén kleur")].spacing(8),
                    w::mono_label(look, "In gebruik"),
                    row![w::button(look, "Opslaan", K::Primary, D::Regular, Some(s16), Some(Msg::Noop)), w::button(look, "Knop", K::Secondary, D::Regular, Some(s16), Some(Msg::Noop))].spacing(8),
                    row![
                        w::icon_button(look, s16, 28.0, false, Some(Msg::Noop)),
                        w::icon_button(look, s16, 28.0, true, Some(Msg::Noop)),
                        w::icon_button(look, s16, 28.0, false, None),
                        t::icon_tile(look, s24, 40.0, false),
                        w::ribbon_large(look, s24, "Lint", false, Some(Msg::Noop)),
                    ]
                    .spacing(8)
                    .align_y(Alignment::Center),
                    t::info_card(
                        look,
                        "Gegevens",
                        vec![("Groep", icon.group().to_string()), ("Apps", apps), ("In Rust", format!("Icon::{icon:?}")), ("Bron", format!("openaec-icons, revisie {}", openaec_icons::REVISION))],
                    ),
                ]
                .spacing(12)
                .into()
            }
            None => column![
                w::mono_label(look, "Details"),
                w::secondary(look, "Kies een icoon. Hier zie je het op 16 en 24 px, vergroot en in één kleur, en in knoppen, het lint en een icoontegel."),
            ]
            .spacing(8)
            .into(),
        };
        let panel = container(scrollable(container(detail).padding(16)).height(Length::Fill)).width(340).height(Length::Fill).style(move |_| w::panel_style(look));
        container(row![left, panel].height(Length::Fill))
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_| container::Style { background: Some(Background::Color(c.frame)), ..Default::default() })
            .into()
    }

    fn components(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let buttons = column![
            row![
                w::button(look, "Opslaan", K::Primary, D::Regular, Some(SAVE_SMALL), Some(Msg::Noop)),
                w::button(look, "Exporteren", K::Secondary, D::Regular, None, Some(Msg::Noop)),
                w::button(look, "Niet opslaan", K::Quiet, D::Regular, None, Some(Msg::Noop)),
                w::button(look, "Verwijderen", K::Danger, D::Regular, Some(DELETE), Some(Msg::Noop)),
            ]
            .spacing(8),
            row![
                w::button(look, "Opslaan", K::Primary, D::Compact, None, Some(Msg::Noop)),
                w::button(look, "Exporteren", K::Secondary, D::Compact, None, Some(Msg::Noop)),
                w::button(look, "Niet opslaan", K::Quiet, D::Compact, None, Some(Msg::Noop)),
                w::button(look, "Verwijderen", K::Danger, D::Compact, None, Some(Msg::Noop)),
            ]
            .spacing(8),
            row![
                w::button(look, "Opslaan", K::Primary, D::Regular, None, None),
                w::button(look, "Exporteren", K::Secondary, D::Regular, None, None),
                w::button(look, "Verwijderen", K::Danger, D::Regular, None, None),
                secondary_note(look, "uitgeschakeld"),
            ]
            .spacing(8)
            .align_y(Alignment::Center),
        ]
        .spacing(8);
        let icon_buttons = row![
            w::with_tooltip(look, w::icon_button(look, PANEL_LEFT, 28.0, false, Some(Msg::Noop)), "Linkerpaneel", Some("Ctrl+1")),
            w::with_tooltip(look, w::icon_button(look, PANEL_RIGHT, 28.0, true, Some(Msg::Noop)), "Rechterpaneel", Some("Ctrl+2")),
            w::icon_button(look, HELP, 28.0, false, None),
            w::icon_button(look, SEARCH, 20.0, false, Some(Msg::Noop)),
            secondary_note(look, "normaal, aan, uitgeschakeld, 20 px"),
        ]
        .spacing(8)
        .align_y(Alignment::Center);
        let fields = column![
            row![
                container(w::text_field(look, "Projectnaam", &self.name, Some(Msg::Name), D::Regular, None)).width(220),
                container(w::text_field(look, "Hoeveelheid", "abc", Some(|_| Msg::Noop), D::Regular, Some("Vul een getal in."))).width(220),
                container(w::text_field(look, "Uitgeschakeld", "", None::<fn(String) -> Msg>, D::Regular, None)).width(220),
            ]
            .spacing(12),
            row![container(w::select(look, &UNITS, self.unit, Msg::Unit, D::Regular)).width(220), container(w::select(look, &UNITS, self.unit, Msg::Unit, D::Compact)).width(220)].spacing(12),
        ]
        .spacing(12);
        let choices = row![
            column![
                w::checkbox(look, "Meenemen in totaal", self.check, Some(Msg::Check)),
                w::checkbox(look, "Uit", false, Some(|_| Msg::Noop)),
                w::checkbox(look, "Uitgeschakeld", true, None::<fn(bool) -> Msg>),
            ]
            .spacing(10),
            column![w::radio(look, "Zijbalk", 1u8, self.radio, Msg::Radio), w::radio(look, "Stappen bovenaan", 2u8, self.radio, Msg::Radio)].spacing(10),
            column![
                w::switch(look, "Raster tonen", self.switch, Some(Msg::Switch)),
                container(w::slider(look, 0.0..=1.0, self.slider, Msg::Slider, format!("{:.2}", self.slider))).width(220),
                container(w::progress(look, 0.62)).width(220),
            ]
            .spacing(12),
        ]
        .spacing(40);
        let notes = column![
            w::banner(look, Tone::Error, ERROR, "Het bestand kan niet worden geopend.", CLOSE, Some(Msg::Noop)),
            w::banner(look, Tone::Warning, WARNING, "Twee posten hebben nog geen prijs.", CLOSE, Some(Msg::Noop)),
            w::banner(look, Tone::Success, SUCCESS, "De begroting is opgeslagen.", CLOSE, Some(Msg::Noop)),
            w::banner(look, Tone::Info, INFO, "Er is een nieuwe versie van de prijslijst.", CLOSE, Some(Msg::Noop)),
            w::toast(look, Tone::Success, SUCCESS, "Opgeslagen", "Kade 12 is opgeslagen.", CLOSE, Some(Msg::Noop)),
        ]
        .spacing(8);
        let rows: Vec<Vec<String>> = self.items.iter().take(4).map(|i| vec![i.code.clone(), i.name.clone(), format!("{} {}", nl(i.quantity, 1), i.unit), euro(i.price), euro(i.amount())]).collect();
        let sheet = column![
            section(look, "Knoppen", buttons.into()),
            section(look, "Icoonknoppen", icon_buttons.into()),
            section(look, "Velden", fields.into()),
            section(look, "Keuzes", choices.into()),
            section(look, "Tabel", container(w::table(look, &BUDGET_COLUMNS, rows, Some(1), None::<fn(usize) -> Msg>, None::<fn(usize) -> Msg>)).style(move |_| w::panel_style(look)).into()),
            section(look, "Meldingen", notes.into()),
            section(look, "Dialoog", self.dialog_card(look, Dialog::CloseDirty(0))),
            section(
                look,
                "Lege staat",
                container(w::empty_state(look, FOLDER_LARGE, "Geen document geopend", "Open of maak een project om te beginnen.", Some(w::button(look, "Nieuw project", K::Primary, D::Regular, None, Some(Msg::Noop)))))
                    .height(220)
                    .into()
            ),
        ]
        .spacing(28)
        .padding(24)
        .max_width(980);
        container(scrollable(container(sheet).center_x(Length::Fill)))
            .width(Length::Fill)
            .height(Length::Fill)
            .style(move |_| container::Style { background: Some(Background::Color(c.panel)), ..Default::default() })
            .into()
    }
}

/// Card metadata such as "Woningbouw · 6 posten · vandaag", built once per project.
fn card_meta(kind: &'static str, when: &'static str) -> &'static str {
    use std::collections::HashMap;
    use std::sync::{Mutex, OnceLock};
    static META: OnceLock<Mutex<HashMap<(&'static str, &'static str), &'static str>>> = OnceLock::new();
    let mut map = META.get_or_init(Default::default).lock().unwrap_or_else(|e| e.into_inner());
    map.entry((kind, when)).or_insert_with(|| Box::leak(format!("{kind} · {when}").into_boxed_str()))
}

fn tone_icon(tone: Tone) -> &'static str {
    match tone {
        Tone::Error => ERROR,
        Tone::Warning => WARNING,
        Tone::Success => SUCCESS,
        Tone::Info => INFO,
    }
}

/// The workspace surface around a document, scrollable, in the workspace colour.
fn page<'a>(look: Look, content: Element<'a, Msg>) -> Element<'a, Msg> {
    let c = look.color;
    container(scrollable(container(content).padding(16).width(Length::Fill)).height(Length::Fill))
        .width(Length::Fill)
        .height(Length::Fill)
        .style(move |_| container::Style { background: Some(Background::Color(c.workspace)), text_color: Some(c.workspace_text), ..Default::default() })
        .into()
}

/// A panel-coloured card on the workspace.
fn card<'a>(look: Look, content: Element<'a, Msg>) -> Element<'a, Msg> {
    container(content).style(move |_| w::panel_style(look)).into()
}

/// Space Grotesk bold, as the headings and tile names on open-aec.com.
const BOLD_HEADING: iced::Font = iced::Font { weight: iced::font::Weight::Bold, ..fonts::HEADING };

/// A linear gradient with stops, top to bottom.
fn gradient(stops: &[(f32, iced::Color)]) -> Background {
    let mut g = iced::gradient::Linear::new(iced::Degrees(180.0));
    for &(offset, color) in stops {
        g = g.add_stop(offset, color);
    }
    Background::Gradient(iced::Gradient::Linear(g))
}

fn vertical(top: iced::Color, bottom: iced::Color) -> Background {
    gradient(&[(0.0, top), (1.0, bottom)])
}

fn alpha(color: iced::Color, a: f32) -> iced::Color {
    iced::Color { a, ..color }
}

/// Shadow colour of the website's deep soft shadows.
fn soft_shadow(look: Look, a: f32) -> iced::Color {
    if look.tokens.dark { iced::Color::from_rgba(0.0, 0.0, 0.0, (a * 2.2).min(0.8)) } else { iced::Color::from_rgba8(42, 42, 50, a) }
}

/// The light tile of open-aec.com: a white-to-warm gradient with a light line on
/// top, 12 px corners, a fine border (2 px amber when featured) and a deep soft shadow.
fn site_card_style(look: Look, featured: bool) -> container::Style {
    let c = look.color;
    let hc = look.high_contrast();
    let top = c.raised;
    let bottom = openaec_ui::design::mix(c.frame, 0.3, c.raised);
    let shine = openaec_ui::design::mix(iced::Color::WHITE, 0.5, c.raised);
    container::Style { snap: false,
        text_color: Some(c.text),
        background: Some(if hc { Background::Color(c.raised) } else { gradient(&[(0.0, shine), (0.006, top), (1.0, bottom)]) }),
        border: iced::Border { color: if featured { c.accent } else { c.border }, width: if featured { 2.0 } else { 1.0 }, radius: 12.0.into() },
        shadow: if hc { iced::Shadow::default() } else { iced::Shadow { color: soft_shadow(look, 0.2), offset: iced::Vector::new(0.0, 14.0), blur_radius: 30.0 } },
    }
}

/// The glass tile in the website's dark panels: white 7% to 2.4% with a light
/// line on top, a white 8% border and a deep shadow.
fn glass_card_style(look: Look, featured: bool) -> container::Style {
    let c = look.color;
    if look.high_contrast() {
        return container::Style { text_color: Some(c.text), background: Some(Background::Color(c.raised)), border: iced::Border { color: if featured { c.accent } else { c.border }, width: 2.0, radius: 12.0.into() }, ..Default::default() };
    }
    container::Style { snap: false,
        text_color: Some(c.text),
        background: Some(gradient(&[(0.0, alpha(iced::Color::WHITE, 0.16)), (0.006, alpha(iced::Color::WHITE, 0.07)), (1.0, alpha(iced::Color::WHITE, 0.024))])),
        border: iced::Border { color: if featured { c.accent } else { alpha(iced::Color::WHITE, 0.09) }, width: if featured { 2.0 } else { 1.0 }, radius: 12.0.into() },
        shadow: iced::Shadow { color: iced::Color::from_rgba(0.0, 0.0, 0.0, 0.5), offset: iced::Vector::new(0.0, 16.0), blur_radius: 34.0 },
    }
}

/// A smaller glass surface, such as the figures and the update strip in the hero.
fn glass_style(look: Look) -> container::Style {
    let mut s = glass_card_style(look, false);
    s.shadow = iced::Shadow { color: iced::Color::from_rgba(0.0, 0.0, 0.0, 0.3), offset: iced::Vector::new(0.0, 8.0), blur_radius: 20.0 };
    s
}

/// The website's dark top band: #33333C to #2A2A32 at 70%, with a soft light at the top.
fn dark_band_style(dark: Look) -> container::Style {
    let c = dark.color;
    if dark.high_contrast() {
        return container::Style { text_color: Some(c.text), background: Some(Background::Color(c.panel)), ..Default::default() };
    }
    container::Style {
        text_color: Some(c.text),
        background: Some(gradient(&[(0.0, openaec_ui::design::mix(iced::Color::WHITE, 0.06, c.panel)), (0.7, c.frame), (1.0, c.frame)])),
        ..Default::default()
    }
}

/// A round button with a tooltip text that is built at run time.
fn round_icon_owned<'a>(look: Look, icon: &'static str, tip: String, on_press: Msg) -> Element<'a, Msg> {
    let c = look.color;
    let button = focus::focusable(look, iced::widget::button(container(w::glyph(icon, 16.0, c.text, c.accent_text)).center(Length::Fill))
        .width(34)
        .height(34)
        .padding(0)
        .on_press(on_press)
        .style(move |_, status| {
            let hovered = status == iced::widget::button::Status::Hovered;
            iced::widget::button::Style { snap: false,
                background: Some(Background::Color(if hovered && !look.high_contrast() { c.hover } else { alpha(c.raised, if look.tokens.dark { 0.5 } else { 1.0 }) })),
                text_color: c.text,
                border: iced::Border { color: if hovered { c.accent } else { c.border }, width: if look.high_contrast() && hovered { 2.0 } else { 1.0 }, radius: 17.0.into() },
                shadow: iced::Shadow::default(),
            }
        }), true, 17.0);
    let tip = container(text(tip).size(font::SIZE_LABEL).font(fonts::BODY).color(c.text)).padding([4, 8]).style(move |_| w::surface(look, look.tokens.shadow.popup, 3.0));
    iced::widget::tooltip(button, tip, iced::widget::tooltip::Position::Bottom).gap(4).into()
}

/// The tool's own logo in an amber tile, or its category icon, as in the real installer.
fn tool_logo<'a>(look: Look, i: usize, size: f32) -> Element<'a, Msg> {
    let c = look.color;
    match logo_handle(i) {
        Some(handle) => container(iced::widget::image(handle).width(size * 0.72).height(size * 0.72))
            .center(size)
            .style(move |_| container::Style {
                background: Some(if look.high_contrast() { Background::Color(c.panel) } else { Background::Gradient(iced::Gradient::Linear(iced::gradient::Linear::new(iced::Degrees(145.0)).add_stop(0.0, alpha(c.accent, 0.14)).add_stop(1.0, alpha(c.accent, 0.03)))) }),
                border: iced::Border { color: alpha(c.accent, 0.25), width: 1.0, radius: (size * 0.25).round().into() },
                ..Default::default()
            })
            .into(),
        None => icon_tile_amber(look, TOOLS[i].icon, size),
    }
}

/// Version in mono, one size: installed, an arrow and the new version in the accent.
fn version_line<'a>(look: Look, inst: &Installer, i: usize) -> Element<'a, Msg> {
    let c = look.color;
    let tool = &TOOLS[i];
    let mono = |s: String, color: iced::Color| text(s).size(11).font(fonts::MONO).color(color);
    let mut line = row![].spacing(5).align_y(Alignment::Center);
    if tool.web {
        line = line.push(w::glyph(EXTERNAL, 11.0, c.text_secondary, c.text_secondary)).push(mono("webtool".into(), c.text_secondary));
    } else if let Some(v) = inst.tools[i].installed {
        line = line.push(w::glyph(CHECK, 11.0, c.success, c.success)).push(mono(format!("v{v}"), c.text_secondary));
        if inst.has_update(i) {
            line = line.push(mono("→".into(), c.text_secondary)).push(mono(format!("v{}", tool.latest), c.accent_text));
        }
    } else {
        line = line.push(mono(format!("v{} beschikbaar", tool.latest), c.text_secondary));
    }
    line.into()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SiteKind {
    /// Amber gradient with a light line and an amber glow.
    Primary,
    /// The light button: raised, fine border, small shadow.
    Light,
    /// The glass button on dark panels: white 6%, a white 14% border.
    Glass,
}

/// A button as on open-aec.com: 8 px corners, 14 px semibold, an icon on the left.
/// The primary text stays dark, as decided for contrast; the website's white text
/// on amber does not reach 4.5 : 1.
fn site_button<'a>(look: Look, label: &'a str, kind: SiteKind, icon: Option<&'static str>, on_press: Option<Msg>) -> Element<'a, Msg> {
    site_button_owned(look, label.to_string(), kind, icon, on_press, false)
}

/// `small` is the tile size: 7 × 14 px padding and 13 px text.
fn site_button_owned<'a>(look: Look, label: String, kind: SiteKind, icon: Option<&'static str>, on_press: Option<Msg>, small: bool) -> Element<'a, Msg> {
    let c = look.color;
    let hc = look.high_contrast();
    let disabled = on_press.is_none();
    let fg = if disabled { c.text_disabled } else if kind == SiteKind::Primary { c.text_on_accent } else { c.text };
    let mut content = row![].spacing(8).align_y(Alignment::Center);
    if let Some(source) = icon {
        content = content.push(w::glyph(source, 16.0, fg, if kind == SiteKind::Primary || disabled { fg } else { c.accent_text }));
    }
    content = content.push(text(label).size(if small { 13 } else { 14 }).font(fonts::STRONG).color(fg));
    focus::focusable(look, iced::widget::button(content)
        .padding(if small { [7, 14] } else { [10, 20] })
        .on_press_maybe(on_press)
        .style(move |_, status| {
            use iced::widget::button::Status as S;
            let hovered = status == S::Hovered;
            let pressed = status == S::Pressed;
            let radius: iced::border::Radius = 8.0.into();
            match kind {
                SiteKind::Primary if !disabled => {
                    let shine = openaec_ui::design::mix(iced::Color::WHITE, 0.35, c.accent_hover);
                    let (top, bottom) = if pressed { (c.accent_pressed, c.accent_pressed) } else if hovered { (c.accent_hover, c.accent) } else { (openaec_ui::design::mix(c.accent_hover, 0.6, c.accent), c.accent) };
                    iced::widget::button::Style { snap: false,
                        background: Some(if hc { Background::Color(c.accent) } else { gradient(&[(0.0, shine), (0.04, top), (1.0, bottom)]) }),
                        text_color: fg,
                        border: iced::Border { color: if hc && hovered { c.text } else { iced::Color::TRANSPARENT }, width: if hc { 2.0 } else { 0.0 }, radius },
                        shadow: if hc || pressed { iced::Shadow::default() } else { iced::Shadow { color: alpha(c.accent, if hovered { 0.6 } else { 0.45 }), offset: iced::Vector::new(0.0, 7.0), blur_radius: 20.0 } },
                    }
                }
                SiteKind::Glass if !hc => iced::widget::button::Style { snap: false,
                    background: Some(Background::Color(alpha(iced::Color::WHITE, if pressed { 0.03 } else if hovered { 0.11 } else { 0.06 }))),
                    text_color: fg,
                    border: iced::Border { color: if hovered { c.accent } else { alpha(iced::Color::WHITE, 0.14) }, width: 1.0, radius },
                    shadow: iced::Shadow::default(),
                },
                _ => iced::widget::button::Style { snap: false,
                    background: Some(if disabled { Background::Color(c.panel) } else if pressed { Background::Color(c.pressed) } else if hovered && !hc { Background::Color(c.hover) } else { vertical(c.raised, openaec_ui::design::mix(c.frame, 0.25, c.raised)) }),
                    text_color: fg,
                    border: iced::Border { color: if hovered { c.accent } else { c.border }, width: if hc && hovered { 2.0 } else { 1.0 }, radius },
                    shadow: if hc || disabled { iced::Shadow::default() } else { iced::Shadow { color: soft_shadow(look, 0.08), offset: iced::Vector::new(0.0, 2.0), blur_radius: 4.0 } },
                },
            }
        }), !disabled, 8.0)
        .into()
}

/// A round icon button with a tooltip, as the source and browser buttons of the real installer.
fn round_icon<'a>(look: Look, icon: &'static str, tip: &'a str, on_press: Msg) -> Element<'a, Msg> {
    let c = look.color;
    let button = focus::focusable(look, iced::widget::button(container(w::glyph(icon, 16.0, c.text, c.accent_text)).center(Length::Fill))
        .width(34)
        .height(34)
        .padding(0)
        .on_press(on_press)
        .style(move |_, status| {
            let hovered = status == iced::widget::button::Status::Hovered;
            iced::widget::button::Style { snap: false,
                background: Some(Background::Color(if hovered && !look.high_contrast() { c.hover } else { alpha(c.raised, if look.tokens.dark { 0.5 } else { 1.0 }) })),
                text_color: c.text,
                border: iced::Border { color: if hovered { c.accent } else { c.border }, width: if look.high_contrast() && hovered { 2.0 } else { 1.0 }, radius: 17.0.into() },
                shadow: iced::Shadow::default(),
            }
        }), true, 17.0);
    w::with_tooltip(look, button.into(), tip, None)
}

/// The website's icon tile: an amber gradient at 145°, from 18% to 5%.
fn icon_tile_amber<'a>(look: Look, icon: &'static str, size: f32) -> Element<'a, Msg> {
    let c = look.color;
    let hc = look.high_contrast();
    container(w::glyph(icon, (size * 0.55).round(), c.accent_text, c.accent_text))
        .center(size)
        .style(move |_| container::Style {
            background: Some(if hc {
                Background::Color(c.panel)
            } else {
                Background::Gradient(iced::Gradient::Linear(iced::gradient::Linear::new(iced::Degrees(145.0)).add_stop(0.0, alpha(c.accent, 0.22)).add_stop(1.0, alpha(c.accent, 0.06))))
            }),
            border: iced::Border { color: if hc { c.accent } else { alpha(c.accent, 0.25) }, width: 1.0, radius: (size * 0.25).round().into() },
            ..Default::default()
        })
        .into()
}

/// The section label of open-aec.com: mono uppercase on a 15% amber tint, round,
/// with an amber dot.
fn section_label<'a>(look: Look, label: &str) -> Element<'a, Msg> {
    let c = look.color;
    let dot = container(Space::new().width(6).height(6)).style(move |_| container::Style { background: Some(Background::Color(c.accent)), border: iced::Border { radius: 3.0.into(), ..Default::default() }, ..Default::default() });
    container(row![dot, text(label.to_uppercase()).size(12).font(fonts::MONO).color(c.accent_text)].spacing(8).align_y(Alignment::Center))
        .padding([7, 14])
        .style(move |_| container::Style {
            background: Some(Background::Color(if look.high_contrast() { c.panel } else { alpha(c.accent, 0.15) })),
            border: iced::Border { color: if look.high_contrast() { c.accent } else { iced::Color::TRANSPARENT }, width: 1.0, radius: 9999.0.into() },
            ..Default::default()
        })
        .into()
}

/// A section head: label, a 26 px Space Grotesk heading and an explanation.
fn section_head<'a>(look: Look, label: &str, heading: &'a str, explanation: &'a str) -> Element<'a, Msg> {
    let c = look.color;
    column![section_label(look, label), text(heading).size(26).font(BOLD_HEADING).color(c.text), text(explanation).size(15).font(fonts::BODY).color(c.text_secondary)].spacing(10).into()
}

/// A small mono chip as the discipline letters on the website tiles: 4 px corners,
/// a fine border. With a tone it becomes a status chip in the status colours.
fn chip<'a>(look: Look, label: &str, tone: Option<Tone>) -> Element<'a, Msg> {
    let c = look.color;
    let (fg, bg, edge) = match tone {
        Some(t) => (t.color(look), if look.high_contrast() { c.panel } else { t.tint(look) }, t.color(look)),
        None => (c.text_secondary, if look.tokens.dark { alpha(iced::Color::WHITE, 0.06) } else { c.hover }, c.border),
    };
    container(text(label.to_uppercase()).size(11).font(fonts::MONO).color(fg))
        .padding([1, 7])
        .style(move |_| container::Style { background: Some(Background::Color(bg)), border: iced::Border { color: edge, width: 1.0, radius: 4.0.into() }, ..Default::default() })
        .into()
}

/// A filter pill with a count, as on open-aec.com: round, 14 px semibold, a small
/// shadow; the active one in the amber gradient with a glow.
fn pill<'a>(look: Look, letter: Option<char>, name: &'a str, count: usize, active: bool, on_press: Msg) -> Element<'a, Msg> {
    let c = look.color;
    let hc = look.high_contrast();
    let fg = if active { c.text_on_accent } else { c.text };
    let badge_bg = if active { alpha(c.text_on_accent, 0.12) } else { c.hover };
    let mut content = row![].spacing(8).align_y(Alignment::Center);
    if let Some(l) = letter {
        let edge = if active { alpha(c.text_on_accent, 0.2) } else { c.border };
        content = content.push(
            container(text(l.to_string()).size(10).font(fonts::MONO).color(fg))
                .padding([0, 5])
                .style(move |_| container::Style { background: Some(Background::Color(alpha(fg, 0.06))), border: iced::Border { color: edge, width: 1.0, radius: 4.0.into() }, ..Default::default() }),
        );
    }
    focus::focusable(look, iced::widget::button(
        content.push(row![
            text(name).size(14).font(fonts::STRONG).color(fg),
            container(text(count.to_string()).size(11).font(fonts::MONO).color(fg))
                .padding([1, 7])
                .style(move |_| container::Style { background: Some(Background::Color(badge_bg)), border: iced::Border { radius: 9999.0.into(), ..Default::default() }, ..Default::default() }),
        ]
        .spacing(8)
        .align_y(Alignment::Center)),
    )
    .padding([9, 16])
    .on_press(on_press)
    .style(move |_, status| {
        let hovered = status == iced::widget::button::Status::Hovered;
        iced::widget::button::Style { snap: false,
            background: Some(if active && !hc {
                gradient(&[(0.0, openaec_ui::design::mix(iced::Color::WHITE, 0.35, c.accent_hover)), (0.05, openaec_ui::design::mix(c.accent_hover, 0.6, c.accent)), (1.0, c.accent)])
            } else if active {
                Background::Color(c.accent)
            } else if hovered && !hc {
                Background::Color(c.hover)
            } else {
                vertical(c.raised, openaec_ui::design::mix(c.frame, 0.25, c.raised))
            }),
            text_color: fg,
            border: iced::Border { color: if active || hovered { c.accent } else { c.border }, width: if hc && hovered { 2.0 } else { 1.0 }, radius: 9999.0.into() },
            shadow: if hc {
                iced::Shadow::default()
            } else if active {
                iced::Shadow { color: alpha(c.accent, 0.5), offset: iced::Vector::new(0.0, 7.0), blur_radius: 20.0 }
            } else {
                iced::Shadow { color: soft_shadow(look, 0.08), offset: iced::Vector::new(0.0, 2.0), blur_radius: 4.0 }
            },
        }
    }), true, 9999.0)
    .into()
}

fn section<'a>(look: Look, title: &str, content: Element<'a, Msg>) -> Element<'a, Msg> {
    column![w::mono_label(look, title), content].spacing(10).into()
}

fn secondary_note(look: Look, s: &'static str) -> Element<'static, Msg> {
    text(s).size(font::SIZE_LABEL).font(fonts::BODY).color(look.color.text_secondary).into()
}

/// The first argument chooses the opening view: `lint` (default), `werkstroom`,
/// `installer`, `componenten` or `iconen`, so a demo can start where it is needed.
fn start_view() -> Gallery {
    let mut gallery = Gallery::default();
    gallery.keymap_path = sc::keymap_path("ui04");
    if let Some(path) = &gallery.keymap_path {
        gallery.keymap = Keymap::load(path);
    }
    match std::env::args().nth(1).as_deref() {
        Some("werkstroom") => gallery.view = View::Workflow,
        Some("installer") => gallery.view = View::Installer,
        Some("componenten") => gallery.view = View::Components,
        Some("iconen") => gallery.view = View::Icons,
        _ => {}
    }
    gallery
}

fn main() -> iced::Result {
    iced::application(|| (start_view(), after(6000, Msg::InstFeatureTick)), Gallery::update, Gallery::view)
        .title("OpenAEC UI 0.4")
        .subscription(Gallery::subscription)
        .theme(|g: &Gallery| g.theme.iced())
        .default_font(fonts::BODY)
        .font(fonts::FILES[0])
        .font(fonts::FILES[1])
        .font(fonts::FILES[2])
        .font(fonts::FILES[3])
        .font(fonts::FILES[4])
        .font(fonts::FILES[5])
        .window(iced::window::Settings {
            size: Size::new(1280.0, 800.0),
            min_size: Some(Size::new(960.0, 600.0)),
            // The library draws the title bar; Windows keeps the shadow and the resize border.
            decorations: false,
            platform_specific: iced::window::settings::PlatformSpecific { undecorated_shadow: true, ..Default::default() },
            ..Default::default()
        })
        .run()
}

#[cfg(test)]
mod tests {
    use super::*;
    use iced::advanced::layout::{self, Layout};
    use iced::advanced::renderer;
    use iced::advanced::widget::Tree;
    use iced::{mouse, Color, Rectangle, Size};

    /// Issue #2: a whole task without the mouse. From the start screen, Tab to the
    /// tile "Lege begroting" and press Enter: the project opens.
    #[test]
    fn a_project_opens_with_the_keyboard_alone() {
        use iced::advanced::widget::operation::{Focusable, Operation, Outcome};
        use iced::advanced::{clipboard, Shell};
        use iced::keyboard;

        struct Find {
            route: Vec<Rectangle>,
            target: Option<Rectangle>,
        }
        impl Operation<()> for Find {
            fn traverse(&mut self, operate: &mut dyn FnMut(&mut dyn Operation<()>)) {
                operate(self);
            }
            fn focusable(&mut self, _id: Option<&iced::widget::Id>, bounds: Rectangle, _state: &mut dyn Focusable) {
                self.route.push(bounds);
            }
            fn text(&mut self, _id: Option<&iced::widget::Id>, bounds: Rectangle, text: &str) {
                if text == "Lege begroting" {
                    self.target = Some(bounds);
                }
            }
        }

        let mut g = Gallery::default();
        assert!(!g.started, "the gallery opens on the start screen");
        let size = Size::new(1280.0, 800.0);
        let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let messages = {
            let mut element = g.view();
            let mut tree = Tree::new(&element);
            let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
            let mut find = Find { route: Vec::new(), target: None };
            element.as_widget_mut().operate(&mut tree, Layout::new(&node), &renderer, &mut find);
            let target = find.target.expect("the start screen shows Lege begroting");
            let steps = find.route.iter().position(|b| b.contains(target.center())).expect("the tile is in the Tab route") + 1;
            for _ in 0..steps {
                let mut step: Box<dyn Operation<()>> = Box::new(openaec_ui::design::focus::next());
                loop {
                    element.as_widget_mut().operate(&mut tree, Layout::new(&node), &renderer, step.as_mut());
                    match step.finish() {
                        Outcome::Chain(next) => step = next,
                        _ => break,
                    }
                }
            }
            let enter = keyboard::Key::Named(keyboard::key::Named::Enter);
            let event = iced::Event::Keyboard(keyboard::Event::KeyPressed {
                key: enter.clone(),
                modified_key: enter,
                physical_key: keyboard::key::Physical::Unidentified(keyboard::key::NativeCode::Unidentified),
                location: keyboard::Location::Standard,
                modifiers: keyboard::Modifiers::empty(),
                text: None,
                repeat: false,
            });
            let mut messages = Vec::new();
            let mut shell = Shell::new(&mut messages);
            element.as_widget_mut().update(&mut tree, &event, Layout::new(&node), mouse::Cursor::Unavailable, &renderer, &mut clipboard::Null, &mut shell, &Rectangle::with_size(size));
            messages
        };
        assert!(messages.iter().any(|m| matches!(m, Msg::OpenProject(0))), "Enter on the tile opens the project: {messages:?}");
        for message in messages {
            let _ = g.update(message);
        }
        assert!(g.started, "the project is open");
    }
    use std::sync::Once;

    fn load_fonts() {
        static LOADED: Once = Once::new();
        LOADED.call_once(|| {
            let mut system = iced_tiny_skia::graphics::text::font_system().write().expect("font system");
            for bytes in fonts::FILES {
                system.load_font(std::borrow::Cow::Borrowed(bytes));
            }
        });
    }

    fn render(gallery: &Gallery, size: Size) -> tiny_skia::Pixmap {
        load_fonts();
        let mut element = gallery.view();
        let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let mut tree = Tree::new(&element);
        let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
        let theme = gallery.theme.iced();
        let style = renderer::Style { text_color: theme.palette().text };
        element.as_widget().draw(&tree, &mut renderer, &theme, &style, Layout::new(&node), mouse::Cursor::Unavailable, &Rectangle::with_size(size));
        let (width, height) = (size.width as u32, size.height as u32);
        let mut bytes = vec![0u8; (width * height * 4) as usize];
        let mut pixels = tiny_skia::PixmapMut::from_bytes(&mut bytes, width, height).expect("valid pixmap");
        let mut mask = tiny_skia::Mask::new(width, height).expect("valid mask");
        renderer.draw(
            &mut pixels,
            &mut mask,
            &iced_tiny_skia::graphics::Viewport::with_physical_size(Size::new(width, height), 1.0),
            &[Rectangle::with_size(size)],
            Color::from_rgb(1.0, 0.0, 1.0),
        );
        for pixel in bytes.chunks_exact_mut(4) {
            pixel.swap(0, 2);
        }
        tiny_skia::Pixmap::from_vec(bytes, tiny_skia::IntSize::from_wh(width, height).expect("size")).expect("pixels")
    }

    #[test]
    fn every_theme_tab_and_document_builds() {
        let mut g = Gallery::default();
        for theme in ThemeId::ALL {
            g.theme = theme;
            for tab in 0..TABS.len() {
                let _ = g.update(Msg::RibbonTab(tab));
                let _ = g.view();
            }
            for kind in [DocKind::Budget, DocKind::Quantities, DocKind::Chart, DocKind::Report, DocKind::Item(1), DocKind::Blank(1)] {
                let _ = g.update(Msg::OpenDoc(kind));
                let _ = g.view();
            }
            for d in [Dialog::Settings, Dialog::Export, Dialog::Print, Dialog::CloseDirty(0)] {
                let _ = g.update(Msg::Dialog(Some(d)));
                let _ = g.view();
            }
            let _ = g.update(Msg::Dialog(None));
            let _ = g.update(Msg::Backstage(true));
            let _ = g.view();
            let _ = g.update(Msg::FilePage(FilePage::New));
            let _ = g.view();
            let _ = g.update(Msg::Backstage(false));
            let _ = g.update(Msg::Restart);
            let _ = g.view();
            let _ = g.update(Msg::OpenProject(0));
            g.view = View::Workflow;
            for nav in Navigation::ALL {
                let _ = g.update(Msg::WfNavigation(nav));
                for i in 0..SECTIONS.len() {
                    let _ = g.update(Msg::WfSection(i));
                    let _ = g.view();
                }
            }
            let _ = g.update(Msg::WfCalculate);
            let _ = g.view();
            g.view = View::Installer;
            let _ = g.view();
            for f in [Filter::Installed, Filter::Updates, Filter::Web, Filter::All] {
                let _ = g.update(Msg::InstFilter(f));
                let _ = g.view();
            }
            for (letter, _) in DISCIPLINES {
                let _ = g.update(Msg::InstDisc(Some(letter)));
                let _ = g.view();
            }
            let _ = g.update(Msg::InstFeature(2));
            let _ = g.view();
            let _ = g.update(Msg::InstOpenWeb(14));
            let _ = g.view();
            let _ = g.update(Msg::InstTab(None));
            g.view = View::Components;
            let _ = g.view();
            g.view = View::Icons;
            let _ = g.view();
            g.view = View::Screen;
        }
    }

    #[test]
    fn icon_view_filters_pages_and_selects() {
        let mut g = Gallery::default();
        assert_eq!(g.icons.matches().len(), Icon::all().len());
        let pdf = *app_choices().iter().find(|c| c.key == Some("pdf")).unwrap();
        let _ = g.update(Msg::IconApp(pdf));
        let pdf_count = g.icons.matches().len();
        assert!(pdf_count > 0 && pdf_count < Icon::all().len());
        assert!(g.icons.matches().iter().all(|i| i.apps().contains(&"pdf")));
        let _ = g.update(Msg::IconPage(2));
        let _ = g.update(Msg::IconSearch("opslaan".into()));
        assert_eq!(g.icons.page, 0);
        assert!(g.icons.matches().contains(&Icon::FileSave));
        let _ = g.update(Msg::IconSelect(Icon::FileSave));
        assert_eq!(g.icons.selected, Some(Icon::FileSave));
        let _ = g.update(Msg::IconLarge(false));
        g.view = View::Icons;
        let _ = g.view();
        let _ = g.update(Msg::IconSearch("geen icoon heet zo".into()));
        assert!(g.icons.matches().is_empty());
        let _ = g.view();
    }

    #[test]
    fn one_command_list_drives_keys_ribbon_and_menus() {
        use iced::keyboard::{Key, Modifiers};
        use openaec_ui::keyboard::KeyPress;
        let mut g = Gallery::default();
        g.started = true;
        assert!(cm::conflicts(&g.commands()).is_empty(), "no key does two things: {:?}", cm::conflicts(&g.commands()));
        let left = g.show_left;
        let _ = g.update(Msg::Key(KeyPress { key: Key::Character("1".into()), modifiers: Modifiers::COMMAND }));
        assert_ne!(g.show_left, left, "Ctrl+1 is the Structuur command");
        assert!(!g.command("view.left").kind.is_on() || g.show_left, "the command shows the panel state");
        g.selected = None;
        g.clipboard = None;
        assert!(!g.command("edit.cut").enabled, "Knippen is greyed out without a selection");
        let _ = g.update(Msg::Key(KeyPress { key: Key::Character("x".into()), modifiers: Modifiers::COMMAND }));
        assert!(g.clipboard.is_none(), "and then Ctrl+X does nothing either");
        // The tab menu shows the same label and shortcut as the command.
        let items = g.menu_items(MenuKind::Tab(0));
        let close = Shortcut::ctrl('w').label();
        assert!(items.iter().any(|i| matches!(i, MenuItem::Action { label: "Sluiten", shortcut: Some(s), .. } if std::ptr::eq(*s, close))));
        g.view = View::Screen;
        for tab in 0..5 {
            let _ = g.update(Msg::RibbonTab(tab));
            let _ = g.view();
        }
    }

    #[test]
    fn an_own_shortcut_changes_keys_menus_and_ribbon() {
        use iced::keyboard::{Key, Modifiers};
        use openaec_ui::keyboard::KeyPress;
        let mut g = Gallery::default();
        g.started = true;
        assert!(g.keymap_path.is_none(), "tests never write a keymap file");
        let _ = g.update(Msg::Dialog(Some(Dialog::Settings)));
        let _ = g.update(Msg::SettingsPage(SettingsPage::Shortcuts));
        g.view = View::Screen;
        let _ = g.view();
        // Raster gets Ctrl+G, through the page.
        let _ = g.update(Msg::Shortcuts(sc::Message::Record("view.grid")));
        let _ = g.update(Msg::Key(KeyPress { key: Key::Character("g".into()), modifiers: Modifiers::COMMAND }));
        assert_eq!(g.command("view.grid").shortcut, Some(Shortcut::ctrl('g')));
        assert!(cm::conflicts(&g.commands()).is_empty());
        let _ = g.update(Msg::Dialog(None));
        let grid = g.grid;
        let _ = g.update(Msg::Key(KeyPress { key: Key::Character("g".into()), modifiers: Modifiers::COMMAND }));
        assert_ne!(g.grid, grid, "Ctrl+G now switches the grid");
        // Opslaan moves to Ctrl+Shift+S; plain Ctrl+S then does nothing.
        let _ = g.update(Msg::Shortcuts(sc::Message::Record("file.save")));
        let _ = g.update(Msg::Key(KeyPress { key: Key::Character("S".into()), modifiers: Modifiers::COMMAND | Modifiers::SHIFT }));
        let save = Shortcut::ctrl_shift('s').label();
        assert!(g.menu_items(MenuKind::Tree(TreeSel::Root)).iter().any(|i| matches!(i, MenuItem::Action { label: "Opslaan", shortcut: Some(s), .. } if std::ptr::eq(*s, save))), "the menu shows the new shortcut");
        assert!(cm::find(&g.commands(), &Key::Character("s".into()), Modifiers::COMMAND).is_none());
        let _ = g.update(Msg::Shortcuts(sc::Message::ResetAll));
        assert_eq!(g.command("file.save").shortcut, Some(Shortcut::ctrl('s')));
        let _ = g.view();
    }

    #[test]
    fn editing_marks_dirty_and_undo_restores() {
        let mut g = Gallery::default();
        let _ = g.update(Msg::SelectRow(1));
        let _ = g.update(Msg::EditPrice("250,00".into()));
        assert_eq!(g.item(1).unwrap().price, 250.0);
        assert!(g.docs[0].dirty);
        let _ = g.update(Msg::Undo);
        assert_eq!(g.item(1).unwrap().price, 240.0);
        let _ = g.update(Msg::Redo);
        assert_eq!(g.item(1).unwrap().price, 250.0);
        let _ = g.update(Msg::Save);
        assert!(!g.docs.iter().any(|d| d.dirty));
    }

    #[test]
    fn closing_a_dirty_tab_asks_first() {
        let mut g = Gallery::default();
        let _ = g.update(Msg::SelectRow(2));
        let _ = g.update(Msg::EditName("Poeren groot".into()));
        let _ = g.update(Msg::CloseDoc(0));
        assert_eq!(g.dialog, Some(Dialog::CloseDirty(0)));
        let _ = g.update(Msg::DiscardAndClose(0));
        assert_eq!(g.docs.len(), 2);
        assert!(g.dialog.is_none());
    }

    #[test]
    fn copy_paste_delete_and_tree_tabs() {
        let mut g = Gallery::default();
        let before = g.items.len();
        let _ = g.update(Msg::SelectRow(1));
        let _ = g.update(Msg::Copy);
        let _ = g.update(Msg::Paste);
        assert_eq!(g.items.len(), before + 1);
        assert!(g.items.iter().any(|i| i.code == "21.30"));
        let _ = g.update(Msg::Delete);
        assert_eq!(g.items.len(), before);
        let _ = g.update(Msg::Tree(TreeSel::Item(5)));
        assert_eq!(g.docs[g.active].kind, DocKind::Item(5));
        let _ = g.update(Msg::ToggleChapter("21"));
        assert!(!g.open_chapters.contains("21"));
        assert_eq!(nl(11480.0, 2), "11.480,00");
        assert_eq!(parse_nl("1.234,5"), Some(1234.5));
    }

    #[test]
    fn menus_and_splitters_respond() {
        let mut g = Gallery::default();
        let _ = g.update(Msg::OpenProject(0));
        let _ = g.update(Msg::Cursor(Point::new(300.0, 400.0)));
        let _ = g.update(Msg::Menu(Some(MenuKind::Row(5))));
        assert_eq!(g.selected, Some(5));
        assert!(g.menu.is_some());
        let _ = g.view();
        let _ = g.update(Msg::OpenItem(5));
        assert!(g.menu.is_none());
        assert_eq!(g.docs[g.active].kind, DocKind::Item(5));
        for kind in [MenuKind::Tree(TreeSel::Root), MenuKind::Tree(TreeSel::Chapter("22")), MenuKind::Tab(0), MenuKind::App] {
            let _ = g.update(Msg::Menu(Some(kind)));
            let _ = g.view();
        }
        let _ = g.update(Msg::Escape);
        assert!(g.menu.is_none());
        let _ = g.update(Msg::Cursor(Point::new(240.0, 300.0)));
        let _ = g.update(Msg::DragSplit(Side::Left));
        let _ = g.update(Msg::Cursor(Point::new(320.0, 300.0)));
        assert_eq!(g.left_width, 320.0);
        let _ = g.update(Msg::Cursor(Point::new(900.0, 300.0)));
        assert_eq!(g.left_width, 480.0);
        let _ = g.update(Msg::EndDrag);
        let _ = g.update(Msg::Cursor(Point::new(200.0, 300.0)));
        assert_eq!(g.left_width, 480.0);
        let _ = g.update(Msg::CloseOthers(0));
        assert_eq!(g.docs.len(), 1);
    }

    #[test]
    fn installer_installs_updates_and_opens_web_tools() {
        let mut g = Gallery::default();
        assert_eq!(g.inst.count(Filter::Updates), 2);
        assert!(g.inst.has_update(1));
        let _ = g.update(Msg::InstInstall(1));
        for _ in 0..20 {
            let _ = g.update(Msg::InstTick(1));
        }
        assert_eq!(g.inst.tools[1].installed, Some("2026.43"));
        assert!(!g.inst.has_update(1));
        assert_eq!(g.inst.count(Filter::Updates), 1);
        assert_eq!(g.inst.count(Filter::Web), 5);
        let _ = g.update(Msg::InstOpenWeb(13));
        let _ = g.update(Msg::InstOpenWeb(15));
        assert_eq!((g.inst.tabs.clone(), g.inst.active), (vec![15], Some(0)));
        let _ = g.update(Msg::InstTab(None));
        assert_eq!(g.inst.active, None);
        let _ = g.update(Msg::InstUpdateAll);
        assert!(g.inst.tools[5].progress.is_some());
        let _ = g.update(Msg::InstDisc(Some('A')));
        assert_eq!(g.inst.disc, Some('A'));
        let _ = g.update(Msg::InstFilter(Filter::Installed));
        assert_eq!(g.inst.disc, None);
        let _ = g.update(Msg::InstSearch("plan".into()));
        g.view = View::Installer;
        let _ = g.view();
    }

    #[test]
    fn screen_uses_theme_colours() {
        let mut gallery = Gallery::default();
        gallery.theme = ThemeId::Dark;
        let pixmap = render(&gallery, Size::new(1280.0, 800.0));
        // The title bar is the frame colour of Donker.
        let frame = ThemeId::Dark.tokens().color.frame;
        let p = pixmap.pixel(300, 50).expect("pixel");
        let [r, g, b, _] = frame.into_rgba8();
        assert_eq!((p.red(), p.green(), p.blue()), (r, g, b));
    }

    /// Save a render; a file that is open elsewhere is skipped with a warning.
    fn save(pixmap: tiny_skia::Pixmap, path: std::path::PathBuf) {
        if let Err(error) = pixmap.save_png(&path) {
            eprintln!("Niet opgeslagen, bestand is in gebruik: {} ({error})", path.display());
        }
    }

    #[test]
    #[ignore = "regenerate the UI 0.4 review renders on demand"]
    fn export_review_renders() {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/ontwerp-0.4/native");
        std::fs::create_dir_all(&dir).expect("render folder");
        let mut gallery = Gallery::default();
        for theme in ThemeId::ALL {
            gallery.theme = theme;
            gallery.view = View::Screen;
            gallery.started = false;
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("start-{}.png", theme.key())));
            gallery.started = true;
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("scherm-{}.png", theme.key())));
            gallery.view = View::Workflow;
            gallery.wf.navigation = Navigation::Sidebar;
            gallery.wf.section = 1;
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("werkstroom-zijbalk-{}.png", theme.key())));
            gallery.wf.navigation = Navigation::Steps;
            gallery.wf.section = 3;
            gallery.wf.visited = [true, true, true, true, false];
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("werkstroom-stappen-{}.png", theme.key())));
            gallery.view = View::Screen;
            gallery.view = View::Components;
            save(render(&gallery, Size::new(1100.0, 1700.0)), dir.join(format!("componenten-{}.png", theme.key())));
            gallery.view = View::Icons;
            gallery.icons.selected = Icon::from_id("file.save");
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("iconen-{}.png", theme.key())));
            gallery.icons.selected = None;
        }
        gallery.theme = ThemeId::Light;
        gallery.workspace = WorkspaceSetting::Dark;
        gallery.view = View::Screen;
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("scherm-light-werkruimte-donker.png"));
        gallery.workspace = WorkspaceSetting::Theme;
        let _ = gallery.update(Msg::Backstage(true));
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("bestand-light.png"));
        let _ = gallery.update(Msg::Backstage(false));
        let _ = gallery.update(Msg::Dialog(Some(Dialog::Settings)));
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("instellingen-light.png"));
        let _ = gallery.update(Msg::Dialog(None));
        let _ = gallery.update(Msg::OpenDoc(DocKind::Chart));
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("grafiek-light.png"));
        let _ = gallery.update(Msg::OpenDoc(DocKind::Budget));
        let _ = gallery.update(Msg::Cursor(Point::new(520.0, 440.0)));
        let _ = gallery.update(Msg::Menu(Some(MenuKind::Row(5))));
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("menu-light.png"));
        gallery.theme = ThemeId::Dark;
        let _ = gallery.update(Msg::Cursor(Point::new(1100.0, 66.0)));
        let _ = gallery.update(Msg::Menu(Some(MenuKind::App)));
        save(render(&gallery, Size::new(1280.0, 800.0)), dir.join("menu-dark.png"));
        let _ = gallery.update(Msg::Menu(None));
        gallery.view = View::Installer;
        let _ = gallery.update(Msg::InstInstall(3));
        for _ in 0..7 {
            let _ = gallery.update(Msg::InstTick(3));
        }
        for theme in [ThemeId::Light, ThemeId::Dark] {
            gallery.theme = theme;
            save(render(&gallery, Size::new(1280.0, 800.0)), dir.join(format!("installer-{}.png", theme.key())));
            save(render(&gallery, Size::new(1280.0, 4300.0)), dir.join(format!("installer-volledig-{}.png", theme.key())));
        }
    }
}
