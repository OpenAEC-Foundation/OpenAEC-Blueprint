//! UI 0.4 gallery: the components of library 0.4 in the five themes, as a full
//! application screen and as a component sheet. Run it smoothly with
//! `cargo run --release --features gpu --bin ui04`.
//!
//! Everything is drawn with `openaec_ui::design`; the icons are Codex's B2 set
//! from `design/icon-set-b2`. The sample screen is a small working estimate so
//! the design can be judged by using it: tabs, ribbon, tree, editing, undo,
//! dialogs, notifications and shortcuts all respond. It is a review aid, not an app.
use openaec_ui::design::chrome::{self as ch, MenuItem, WindowActions, WindowIcons};
use openaec_ui::design::tiles::{self as t, RecentFile};
use openaec_ui::design::widgets::{self as w, ButtonKind as K, Density as D, DocumentTab, TableColumn, Tone};
use openaec_ui::design::workflow::{self as wf, Navigation, Section};
use openaec_ui::design::{font, Look, StatusbarSetting, ThemeId, WorkspaceSetting};
use openaec_ui::fonts;
use openaec_ui::iced::widget::{column, container, mouse_area, row, scrollable, text, Space};
use openaec_ui::iced::{self, keyboard, mouse, Alignment, Background, Element, Length, Point, Size, Subscription, Task};
use std::collections::HashSet;
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

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
enum View {
    #[default]
    Screen,
    Workflow,
    Components,
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
    // Component sheet
    Check(bool),
    Switch(bool),
    Radio(u8),
    Slider(f32),
    Name(String),
    Unit(&'static str),
    Noop,
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
            Msg::Dialog(d) => self.dialog = d,
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
                return iced::window::get_latest().and_then(iced::window::drag);
            }
            Msg::Minimize => return iced::window::get_latest().and_then(|id| iced::window::minimize(id, true)),
            Msg::Maximize => {
                self.maximized = !self.maximized;
                return iced::window::get_latest().and_then(iced::window::toggle_maximize);
            }
            Msg::CloseWindow => {
                if self.docs.iter().any(|d| d.dirty) {
                    self.dialog = Some(Dialog::Quit);
                } else {
                    return iced::window::get_latest().and_then(iced::window::close);
                }
            }
            Msg::QuitNow => return iced::window::get_latest().and_then(iced::window::close),
            Msg::SaveAndQuit => {
                for doc in &mut self.docs {
                    doc.dirty = false;
                }
                return iced::window::get_latest().and_then(iced::window::close);
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
        let keys = keyboard::on_key_press(|key, mods| {
            use keyboard::key::Named;
            use keyboard::Key;
            match (key.as_ref(), mods.command()) {
                (Key::Named(Named::Escape), _) => Some(Msg::Escape),
                (Key::Named(Named::Enter), false) => Some(Msg::Enter),
                (Key::Named(Named::Delete), false) => Some(Msg::Delete),
                (Key::Character("s"), true) => Some(Msg::Save),
                (Key::Character("n"), true) => Some(Msg::New),
                (Key::Character("z"), true) => Some(Msg::Undo),
                (Key::Character("y"), true) => Some(Msg::Redo),
                (Key::Character("x"), true) => Some(Msg::Cut),
                (Key::Character("c"), true) => Some(Msg::Copy),
                (Key::Character("v"), true) => Some(Msg::Paste),
                (Key::Character("p"), true) => Some(Msg::Dialog(Some(Dialog::Print))),
                (Key::Character("e"), true) => Some(Msg::Dialog(Some(Dialog::Export))),
                (Key::Character(","), true) => Some(Msg::Dialog(Some(Dialog::Settings))),
                (Key::Character("1"), true) => Some(Msg::ToggleLeft),
                (Key::Character("2"), true) => Some(Msg::ToggleRight),
                (Key::Character("+") | Key::Character("="), true) => Some(Msg::ZoomIn),
                (Key::Character("-"), true) => Some(Msg::ZoomOut),
                (Key::Character("0"), true) => Some(Msg::ZoomFit),
                (Key::Character("w"), true) => Some(Msg::CloseActive),
                _ => None,
            }
        });
        Subscription::batch([keys, iced::window::resize_events().map(|(_, size)| Msg::WindowResized(size))])
    }

    fn view(&self) -> Element<'_, Msg> {
        let look = self.look();
        let body = match self.view {
            View::Screen => self.screen(look),
            View::Workflow => self.workflow(look),
            View::Components => self.components(look),
        };
        let mut layers = vec![column![self.toolbar(look), body].into()];
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
        let views = [(View::Screen, "Lint-app"), (View::Workflow, "Werkstroom-app"), (View::Components, "Componenten")];
        let mut bar = row![
            text("UI 0.4").size(font::SIZE_PANEL_HEADING).font(fonts::HEADING).color(c.text),
            Space::with_width(12),
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
        bar = bar.push(Space::with_width(Length::Fill));
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
        let has_selection = self.selected.is_some();
        let sel = |m: Msg| has_selection.then_some(m);
        let groups = match self.ribbon_tab {
            0 => vec![
                w::ribbon_group(look, "Project", vec![w::ribbon_large(look, NEW, "Nieuw", false, Some(Msg::New)), w::ribbon_large(look, OPEN, "Openen", false, Some(Msg::Backstage(true))), w::ribbon_large(look, SAVE, "Opslaan", false, Some(Msg::Save))]),
                w::ribbon_group(look, "Klembord", vec![
                    w::ribbon_large(look, PASTE, "Plakken", false, self.clipboard.as_ref().map(|_| Msg::Paste)),
                    column![w::ribbon_small(look, CUT, "Knippen", false, sel(Msg::Cut)), w::ribbon_small(look, COPY, "Kopiëren", false, sel(Msg::Copy)), w::ribbon_small(look, DELETE, "Verwijderen", false, sel(Msg::Delete))].spacing(2).into(),
                ]),
                w::ribbon_group(look, "Geschiedenis", vec![
                    w::ribbon_large(look, UNDO, "Ongedaan", false, (!self.history.is_empty()).then_some(Msg::Undo)),
                    w::ribbon_large(look, REDO, "Opnieuw", false, (!self.future.is_empty()).then_some(Msg::Redo)),
                ]),
            ],
            1 => vec![
                w::ribbon_group(look, "Posten", vec![w::ribbon_large(look, ADD_ITEM, "Nieuwe post", false, Some(Msg::AddItem)), w::ribbon_large(look, ADD_CHAPTER, "Hoofdstuk", false, Some(Msg::AddChapter))]),
                w::ribbon_group(look, "Weergaven", vec![
                    w::ribbon_large(look, TABLE, "Tabel", self.docs.get(self.active).is_some_and(|d| d.kind == DocKind::Budget), Some(Msg::OpenDoc(DocKind::Budget))),
                    w::ribbon_large(look, CHART, "Grafiek", self.docs.get(self.active).is_some_and(|d| d.kind == DocKind::Chart), Some(Msg::OpenDoc(DocKind::Chart))),
                ]),
            ],
            2 => vec![
                w::ribbon_group(look, "Berekening", vec![w::ribbon_large(look, RECALC, "Herberekenen", false, Some(Msg::Recalculate))]),
                w::ribbon_group(look, "Controle", vec![w::ribbon_large(look, AUDIT, "Controleren", self.banner.is_some(), Some(Msg::Audit))]),
            ],
            3 => vec![
                w::ribbon_group(look, "Zoomen", vec![
                    column![w::ribbon_small(look, ZOOM_IN, "Inzoomen", false, Some(Msg::ZoomIn)), w::ribbon_small(look, ZOOM_OUT, "Uitzoomen", false, Some(Msg::ZoomOut)), w::ribbon_small(look, FIT, "100%", self.zoom == 100, Some(Msg::ZoomFit))].spacing(2).into(),
                ]),
                w::ribbon_group(look, "Tonen", vec![
                    w::ribbon_large(look, GRID, "Raster", self.grid, Some(Msg::ToggleGrid)),
                    w::ribbon_large(look, LEFT_LARGE, "Structuur", self.show_left, Some(Msg::ToggleLeft)),
                    w::ribbon_large(look, RIGHT_LARGE, "Eigenschappen", self.show_right, Some(Msg::ToggleRight)),
                ]),
                w::ribbon_group(look, "Venster", vec![w::ribbon_large(look, SETTINGS_LARGE, "Instellingen", false, Some(Msg::Dialog(Some(Dialog::Settings))))]),
            ],
            _ => vec![
                w::ribbon_group(look, "Rapport", vec![w::ribbon_large(look, REPORT, "Rapport maken", self.report_ready, Some(Msg::GenerateReport))]),
                w::ribbon_group(look, "Uitvoer", vec![w::ribbon_large(look, EXPORT, "Exporteren", false, Some(Msg::Dialog(Some(Dialog::Export)))), w::ribbon_large(look, PRINT, "Afdrukken", false, Some(Msg::Dialog(Some(Dialog::Print))))]),
            ],
        };
        w::ribbon(look, groups)
    }

    fn tree_panel(&self, look: Look) -> Element<'_, Msg> {
        let mut tree = column![w::tree_row(
            look,
            0,
            Some(if self.root_open { COLLAPSE } else { EXPAND }),
            Some(Msg::ToggleRoot),
            Some(FOLDER),
            PROJECTS[self.project].0,
            self.tree == TreeSel::Root,
            Some(Msg::Tree(TreeSel::Root)),
            Some(Msg::Menu(Some(MenuKind::Tree(TreeSel::Root)))),
        )];
        if self.root_open {
            for (key, name) in CHAPTERS {
                let children: Vec<&Item> = self.items.iter().filter(|i| i.chapter() == key).collect();
                if children.is_empty() {
                    continue;
                }
                let open = self.open_chapters.contains(key);
                tree = tree.push(w::tree_row(look, 1, Some(if open { COLLAPSE } else { EXPAND }), Some(Msg::ToggleChapter(key)), Some(FOLDER), name, self.tree == TreeSel::Chapter(key), Some(Msg::Tree(TreeSel::Chapter(key))), Some(Msg::Menu(Some(MenuKind::Tree(TreeSel::Chapter(key)))))));
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
            scrollable(tree).height(Length::Fill).into(),
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
        let tabs: Vec<DocumentTab<'_>> = self.docs.iter().map(|d| DocumentTab { title: &d.title, dirty: d.dirty }).collect();
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
                let total = row![w::mono_label(look, "Totaal"), Space::with_width(Length::Fill), text(euro(self.total())).size(font::SIZE_PANEL_HEADING).font(fonts::MONO).color(c.text)].padding([8, 8]).align_y(Alignment::Center);
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
                                container(Space::new(Length::Fill, 18)).width(Length::FillPortion(share)).style(move |_| container::Style {
                                    background: Some(Background::Color(accent)),
                                    border: iced::Border { radius: 3.0.into(), ..Default::default() },
                                    ..Default::default()
                                }),
                                Space::with_width(Length::FillPortion(1000 - share.min(999))),
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
                w::with_tooltip(look, ch::title_button(look, SAVE_SMALL, false, Some(Msg::Save)), "Opslaan", Some("Ctrl+S")),
                w::with_tooltip(look, ch::title_button(look, UNDO_SMALL, false, (!self.history.is_empty()).then_some(Msg::Undo)), "Ongedaan maken", Some("Ctrl+Z")),
                w::with_tooltip(look, ch::title_button(look, REDO_SMALL, false, (!self.future.is_empty()).then_some(Msg::Redo)), "Opnieuw", Some("Ctrl+Y")),
            ]
        } else {
            vec![Space::with_width(86).into()]
        };
        let extra = vec![
            w::with_tooltip(look, ch::title_button(look, MENU, self.menu.is_some_and(|(k, _)| k == MenuKind::App), Some(Msg::Menu(Some(MenuKind::App)))), "Menu", None),
            w::with_tooltip(look, ch::title_button(look, SETTINGS, self.dialog == Some(Dialog::Settings), Some(Msg::Dialog(Some(Dialog::Settings)))), "Instellingen", Some("Ctrl+,")),
        ];
        let window = WindowActions { drag: Msg::TitlePress, minimize: Msg::Minimize, maximize: Msg::Maximize, close: Msg::CloseWindow, maximized: self.maximized };
        ch::title_bar(look, name, quick_buttons, extra, window, WINDOW_ICONS)
    }

    /// Lines of the open menu.
    fn menu_items(&self, kind: MenuKind) -> Vec<MenuItem<'static, Msg>> {
        let paste = self.clipboard.as_ref().map(|_| Msg::Paste);
        let item_menu = |id: u32| {
            vec![
                MenuItem::action(Some(ITEM), "Openen in tab", None, Some(Msg::OpenItem(id))),
                MenuItem::Separator,
                MenuItem::action(Some(CUT), "Knippen", Some("Ctrl+X"), Some(Msg::Cut)),
                MenuItem::action(Some(COPY), "Kopiëren", Some("Ctrl+C"), Some(Msg::Copy)),
                MenuItem::action(Some(b2!("16", "edit.paste")), "Plakken", Some("Ctrl+V"), paste.clone()),
                MenuItem::Separator,
                MenuItem::action(Some(b2!("16", "budget.add-item")), "Nieuwe post hieronder", None, Some(Msg::AddItem)),
                MenuItem::Separator,
                MenuItem::danger(Some(DELETE), "Verwijderen", Some("Del"), Some(Msg::Delete)),
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
                    MenuItem::action(Some(b2!("16", "budget.add-chapter")), "Nieuw hoofdstuk", None, Some(Msg::AddChapter)),
                ]
            }
            MenuKind::Tree(TreeSel::Root) => vec![
                MenuItem::Heading(PROJECTS[self.project].0),
                MenuItem::action(Some(if self.root_open { COLLAPSE } else { EXPAND }), if self.root_open { "Inklappen" } else { "Uitklappen" }, None, Some(Msg::ToggleRoot)),
                MenuItem::action(Some(TABLE_SMALL), "Begroting openen", None, Some(Msg::OpenDoc(DocKind::Budget))),
                MenuItem::action(Some(b2!("16", "data.chart")), "Grafiek openen", None, Some(Msg::OpenDoc(DocKind::Chart))),
                MenuItem::Separator,
                MenuItem::action(Some(SAVE_SMALL), "Opslaan", Some("Ctrl+S"), Some(Msg::Save)),
            ],
            MenuKind::Tab(i) => vec![
                MenuItem::action(Some(CLOSE), "Sluiten", Some("Ctrl+W"), Some(Msg::CloseDoc(i))),
                MenuItem::action(None, "Andere tabs sluiten", None, (self.docs.len() > 1).then_some(Msg::CloseOthers(i))),
                MenuItem::action(None, "Alle tabs sluiten", None, Some(Msg::CloseAll)),
                MenuItem::Separator,
                MenuItem::action(Some(SAVE_SMALL), "Opslaan", Some("Ctrl+S"), Some(Msg::Save)),
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
                container(Space::new(Length::Fill, 5)).width(Length::FillPortion(len)).style(move |_| container::Style {
                    background: Some(Background::Color(color)),
                    border: iced::Border { radius: 2.0.into(), ..Default::default() },
                    ..Default::default()
                }),
                Space::with_width(Length::FillPortion(10 - len)),
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
            Space::with_height(4),
            w::mono_label(look, "Nieuw"),
            t::task_tile(look, NEW, "Lege begroting", "Begin zonder posten.", Some(Msg::OpenProject(0))),
            t::task_tile(look, ADD_CHAPTER, "Vanaf sjabloon", "Woningbouw, utiliteit of renovatie.", Some(Msg::OpenProject(0))),
            t::task_tile(look, OPEN_LARGE, "Bestand openen", "Kies een begroting op deze computer.", Some(Msg::OpenProject(1))),
            Space::with_height(8),
            t::info_card(look, "Over", vec![("Versie", "UI 0.4 · voorbeeld".into()), ("Thema", self.theme.name().into()), ("Licentie", "nog te bepalen".into())]),
        ]
        .spacing(8)
        .width(340);
        let right = column![w::mono_label(look, "Recente projecten"), self.project_grid(look), Space::with_height(4), w::mono_label(look, "Recente bestanden"), self.recent_list(look)]
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
                    Space::with_height(6),
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
                w::dialog(look, "Instellingen", CLOSE, close, content.into(), None, vec![w::button(look, "Sluiten", K::Primary, D::Regular, None, Some(Msg::Dialog(None)))], true)
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

fn section<'a>(look: Look, title: &str, content: Element<'a, Msg>) -> Element<'a, Msg> {
    column![w::mono_label(look, title), content].spacing(10).into()
}

fn secondary_note(look: Look, s: &'static str) -> Element<'static, Msg> {
    text(s).size(font::SIZE_LABEL).font(fonts::BODY).color(look.color.text_secondary).into()
}

fn main() -> iced::Result {
    iced::application("OpenAEC UI 0.4", Gallery::update, Gallery::view)
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
        let element = gallery.view();
        let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let mut tree = Tree::new(&element);
        let node = element.as_widget().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
        let theme = gallery.theme.iced();
        let style = renderer::Style { text_color: theme.palette().text };
        element.as_widget().draw(&tree, &mut renderer, &theme, &style, Layout::new(&node), mouse::Cursor::Unavailable, &Rectangle::with_size(size));
        let (width, height) = (size.width as u32, size.height as u32);
        let mut bytes = vec![0u8; (width * height * 4) as usize];
        let mut pixels = tiny_skia::PixmapMut::from_bytes(&mut bytes, width, height).expect("valid pixmap");
        let mut mask = tiny_skia::Mask::new(width, height).expect("valid mask");
        renderer.draw::<&str>(
            &mut pixels,
            &mut mask,
            &iced_tiny_skia::graphics::Viewport::with_physical_size(Size::new(width, height), 1.0),
            &[Rectangle::with_size(size)],
            Color::from_rgb(1.0, 0.0, 1.0),
            &[],
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
            g.view = View::Components;
            let _ = g.view();
            g.view = View::Screen;
        }
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
            render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join(format!("start-{}.png", theme.key()))).expect("save");
            gallery.started = true;
            render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join(format!("scherm-{}.png", theme.key()))).expect("save");
            gallery.view = View::Workflow;
            gallery.wf.navigation = Navigation::Sidebar;
            gallery.wf.section = 1;
            render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join(format!("werkstroom-zijbalk-{}.png", theme.key()))).expect("save");
            gallery.wf.navigation = Navigation::Steps;
            gallery.wf.section = 3;
            gallery.wf.visited = [true, true, true, true, false];
            render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join(format!("werkstroom-stappen-{}.png", theme.key()))).expect("save");
            gallery.view = View::Screen;
            gallery.view = View::Components;
            render(&gallery, Size::new(1100.0, 1700.0)).save_png(dir.join(format!("componenten-{}.png", theme.key()))).expect("save");
        }
        gallery.theme = ThemeId::Light;
        gallery.workspace = WorkspaceSetting::Dark;
        gallery.view = View::Screen;
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("scherm-light-werkruimte-donker.png")).expect("save");
        gallery.workspace = WorkspaceSetting::Theme;
        let _ = gallery.update(Msg::Backstage(true));
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("bestand-light.png")).expect("save");
        let _ = gallery.update(Msg::Backstage(false));
        let _ = gallery.update(Msg::Dialog(Some(Dialog::Settings)));
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("instellingen-light.png")).expect("save");
        let _ = gallery.update(Msg::Dialog(None));
        let _ = gallery.update(Msg::OpenDoc(DocKind::Chart));
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("grafiek-light.png")).expect("save");
        let _ = gallery.update(Msg::OpenDoc(DocKind::Budget));
        let _ = gallery.update(Msg::Cursor(Point::new(520.0, 440.0)));
        let _ = gallery.update(Msg::Menu(Some(MenuKind::Row(5))));
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("menu-light.png")).expect("save");
        gallery.theme = ThemeId::Dark;
        let _ = gallery.update(Msg::Cursor(Point::new(1100.0, 66.0)));
        let _ = gallery.update(Msg::Menu(Some(MenuKind::App)));
        render(&gallery, Size::new(1280.0, 800.0)).save_png(dir.join("menu-dark.png")).expect("save");
    }
}
