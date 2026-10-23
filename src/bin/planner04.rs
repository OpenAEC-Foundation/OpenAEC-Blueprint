//! Open Planner Studio, test version in UI 0.4 (phase 5 of library 0.4).
//! Run it smoothly with `cargo run --release --features gpu --bin planner04`;
//! add `-- project` to skip the start screen or `-- donker` for the dark theme.
//!
//! The structure follows the real Open Planner Studio (OpenAEC-Foundation/
//! open-planner-studio, commit 001b9c67): the ribbon tabs Start, Planning,
//! Resources, Beeld, Instellingen, Tabel, IFC and Rapport with their groups and
//! Dutch labels from `src/i18n/locales/nl`, the properties panel, the status
//! bar and the example project `examples/01-grachtenpand-amsterdam.ifc`
//! (tasks, relations with SS/FF and lags, resources and the Dutch construction
//! calendar). Everything is drawn with `openaec_ui::design` and the B2 icons
//! from the `openaec-icons` crate. The planner works: WBS, Gantt, table,
//! resources, histogram, report, CPM with float, baseline, status date, undo,
//! dialogs, notifications and shortcuts all respond. It is a test version for
//! review, not the app: nothing is read from or written to disk, relations are
//! not drawn as lines and there is one calendar.
use openaec_icons::{Icon, Size as IconSize};
use openaec_ui::design::chrome::{self as ch, MenuItem, WindowActions, WindowIcons};
use openaec_ui::design::tiles::{self as t, RecentFile};
use openaec_ui::design::widgets::{self as w, ButtonKind as K, Density as D, DocumentTab, TableColumn, Tone};
use openaec_ui::design::workflow as wf;
use openaec_ui::design::{font, Look, StatusbarSetting, ThemeId, WorkspaceSetting};
use openaec_ui::fonts;
use openaec_ui::iced::alignment::{Horizontal, Vertical};
use openaec_ui::iced::widget::{column, container, mouse_area, row, scrollable, text, Space, Stack};
use openaec_ui::iced::{self, keyboard, mouse, Alignment, Background, Color, Element, Length, Point, Size, Subscription, Task};
use std::collections::{HashMap, HashSet};
use std::time::{Duration, Instant};

/// The 16 px master of a B2 icon, for buttons, menus and trees.
fn s(icon: Icon) -> &'static str {
    icon.svg(IconSize::S16)
}

/// The 24 px master of a B2 icon, for large ribbon buttons and tiles.
fn l(icon: Icon) -> &'static str {
    icon.svg(IconSize::S24)
}

fn window_icons() -> WindowIcons {
    WindowIcons { minimize: s(Icon::WindowMinimize), maximize: s(Icon::WindowMaximize), restore: s(Icon::WindowRestore), close: s(Icon::WindowClose) }
}

/// The ribbon tabs of Open Planner Studio, in the order and words of the app
/// (`menu:ribbon.*`). The optional AI tab is left out of this test version.
const TABS: [&str; 8] = ["Start", "Planning", "Resources", "Beeld", "Instellingen", "Tabel", "IFC", "Rapport"];
const TAB_START: usize = 0;
const TAB_PLANNING: usize = 1;
const TAB_RESOURCES: usize = 2;
const TAB_VIEW: usize = 3;
const TAB_SETTINGS: usize = 4;
const TAB_TABLE: usize = 5;
const TAB_IFC: usize = 6;
const TAB_REPORT: usize = 7;
const FORMATS: [&str; 4] = ["IFC 4.3 (eigen formaat)", "MS Project XML", "Primavera P6 XML", "CSV"];
const MONTHS: [&str; 12] = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"];
/// Work categories (`task:taskType.*`), in the order of the IFC predefined types used.
const CATEGORIES: [&str; 5] = ["Bouw", "Logistiek", "Installatie", "Sloop", "Keuring/Inspectie"];
const CONSTRAINTS: [&str; 4] = ["Zo vroeg mogelijk (ASAP)", "Zo laat mogelijk (ALAP)", "Start niet eerder dan (SNET)", "Moet starten op (MSO)"];
const CAPACITY_PER_WEEK: u32 = 5;
/// The example projects that ship with the app (`examples/`). Only the first
/// one is loaded in this test version.
const EXAMPLES: [(&str, &str, &str); 8] = [
    ("Grachtenpand Amsterdam", "Nieuwbouw · 44 taken", "01-grachtenpand-amsterdam.ifc"),
    ("Rijwoningen De Akkers", "Showcase · 89 taken", "showcase-rijwoningen-de-akkers.ifc"),
    ("Appartementencomplex De Vaart", "Showcase · 260 taken", "showcase-appartementencomplex.ifc"),
    ("Verbouwing eengezinswoning", "Showcase · 20 taken", "showcase-verbouwing-eengezinswoning.ifc"),
    ("Renovatie basisschool", "Renovatie · 37 taken", "02-renovatie-basisschool.ifc"),
    ("Kantoorgebouw Zuidas", "Utiliteitsbouw", "03-kantoorgebouw-zuidas.ifc"),
    ("Brugvervanging N279", "Infra", "05-brugvervanging-n279.ifc"),
    ("Dijkversterking Markermeerdijk", "Infra", "16-dijkversterking-markermeerdijk.ifc"),
];
const RESOURCES: [&str; 7] = ["Restauratieploeg", "Restauratiemetselaars", "Timmerlieden", "Stukadoors", "Mobiele kraan", "Heibedrijf", "Beton C20/25"];
/// Resource accents (Beeld · Resource-accent), readable on every workspace colour.
const RESOURCE_COLORS: [Color; 7] = [
    Color::from_rgb(0.85, 0.47, 0.02),
    Color::from_rgb(0.72, 0.31, 0.25),
    Color::from_rgb(0.49, 0.34, 0.22),
    Color::from_rgb(0.55, 0.40, 0.65),
    Color::from_rgb(0.33, 0.42, 0.56),
    Color::from_rgb(0.25, 0.45, 0.40),
    Color::from_rgb(0.45, 0.45, 0.50),
];
/// The project starts on Monday 1 March 2027, as in the example file.
const PROJECT_START: (i32, u32, u32) = (2027, 3, 1);
/// Non-working days of the construction calendar in the example (`IfcWorkTime`),
/// as (year, month, first day, last day); weekends are never working days.
const HOLIDAYS: [(i32, u32, u32, u32); 10] = [
    (2027, 3, 26, 26),
    (2027, 3, 29, 29),
    (2027, 4, 27, 27),
    (2027, 5, 5, 6),
    (2027, 5, 17, 17),
    (2027, 7, 26, 31),
    (2027, 8, 1, 15),
    (2027, 12, 27, 27),
    (2028, 4, 14, 14),
    (2028, 4, 17, 17),
];
const DEFAULT_STATUS_DATE: u32 = 32;
const ROW: f32 = 28.0;
const GRID_WIDTH: f32 = 300.0;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum RelKind {
    /// Finish-to-start (einde-start).
    FS,
    /// Start-to-start.
    SS,
    /// Finish-to-finish.
    FF,
}

impl RelKind {
    fn code(self) -> &'static str {
        match self {
            Self::FS => "FS",
            Self::SS => "SS",
            Self::FF => "FF",
        }
    }
}

/// A relation to a predecessor, with a lag in working days.
#[derive(Debug, Clone, PartialEq)]
struct Pred {
    id: u32,
    kind: RelKind,
    lag: i32,
}

#[derive(Debug, Clone, PartialEq)]
struct PlanTask {
    id: u32,
    name: String,
    level: u8,
    /// Start in working days from the project start.
    start: u32,
    /// Duration in working days; 0 is a milestone.
    duration: u32,
    /// 0 to 100.
    progress: u8,
    category: usize,
    resource: Option<usize>,
    predecessors: Vec<Pred>,
    /// Delay added by Nivelleren, in working days; kept through recalculation.
    leveling_delay: u32,
}

impl PlanTask {
    fn milestone(&self) -> bool {
        self.duration == 0
    }
    fn end(&self) -> u32 {
        self.start + self.duration
    }
}

/// The example project, translated from `examples/01-grachtenpand-amsterdam.ifc`:
/// (WBS, name, level, duration, category, resource, predecessors by WBS).
/// Starts follow from the relations; the overallocation of the carpenters on
/// 3.9 and 4.1 is added for the test so that levelling has something to do.
type Rel = (&'static str, RelKind, i32);
const EXAMPLE: [(&str, &str, u8, u32, usize, Option<usize>, &[Rel]); 52] = [
    ("", "Grachtenpand Amsterdam", 0, 0, 0, None, &[]),
    ("1", "1. Voorbereiding", 1, 0, 0, None, &[]),
    ("1.1", "Bouwplaats inrichten", 2, 5, 1, Some(0), &[]),
    ("1.2", "Damwand aanbrengen", 2, 10, 0, Some(5), &[("1.1", RelKind::FS, 0)]),
    ("1.3", "Bronbemaling aanbrengen", 2, 5, 2, None, &[("1.2", RelKind::FS, 0)]),
    ("1.4", "Grondonderzoek uitvoeren", 2, 3, 0, None, &[("1.3", RelKind::FS, 0)]),
    ("1.5", "Start bouw", 2, 0, 0, None, &[("1.4", RelKind::FS, 0)]),
    ("2", "2. Fundering en kelder", 1, 0, 0, None, &[]),
    ("2.1", "Bouwput ontgraven", 2, 10, 0, Some(0), &[("1.1", RelKind::SS, 12)]),
    ("2.2", "Funderingspalen heien", 2, 15, 0, Some(5), &[("2.1", RelKind::FS, 0)]),
    ("2.3", "Wapening kelder vlechten", 2, 8, 0, None, &[("2.2", RelKind::FS, 0)]),
    ("2.4", "Keldervloer storten", 2, 5, 0, Some(6), &[("2.3", RelKind::FS, 0)]),
    ("2.5", "Kelderwanden storten", 2, 10, 0, Some(6), &[("2.4", RelKind::FS, 0)]),
    ("2.6", "Kelder waterdicht maken", 2, 5, 0, None, &[("2.5", RelKind::FS, 0)]),
    ("2.7", "Bouwput aanvullen", 2, 5, 1, Some(0), &[("2.6", RelKind::FS, 0)]),
    ("3", "3. Ruwbouw", 1, 0, 0, None, &[]),
    ("3.1", "Metselwerk begane grond", 2, 12, 0, Some(1), &[("2.1", RelKind::SS, 4)]),
    ("3.2", "Verdiepingsvloer 1", 2, 5, 0, Some(4), &[("3.1", RelKind::FS, 0)]),
    ("3.3", "Metselwerk 1e verdieping", 2, 10, 0, Some(1), &[("3.2", RelKind::FS, 0)]),
    ("3.4", "Verdiepingsvloer 2", 2, 5, 0, Some(4), &[("3.3", RelKind::FS, 0)]),
    ("3.5", "Metselwerk 2e verdieping", 2, 10, 0, Some(1), &[("3.4", RelKind::FS, 0)]),
    ("3.6", "Verdiepingsvloer 3", 2, 5, 0, Some(4), &[("3.5", RelKind::FS, 0)]),
    ("3.7", "Metselwerk 3e verdieping", 2, 8, 0, Some(1), &[("3.6", RelKind::FS, 0)]),
    ("3.8", "Houten kapconstructie", 2, 10, 0, Some(2), &[("3.7", RelKind::FS, 0)]),
    ("3.9", "Dakbedekking", 2, 8, 0, Some(2), &[("3.8", RelKind::FS, 0)]),
    ("3.10", "Hoogste punt", 2, 0, 0, None, &[("3.9", RelKind::FS, 0)]),
    ("4", "4. Gevel en dak", 1, 0, 0, None, &[]),
    ("4.1", "Gevelisolatie", 2, 8, 2, Some(2), &[("3.9", RelKind::FS, -15)]),
    ("4.2", "Natuursteen gevelbekleding", 2, 15, 0, None, &[("4.1", RelKind::FS, 0)]),
    ("4.3", "Kozijnen plaatsen", 2, 10, 2, Some(2), &[("4.2", RelKind::FS, 0)]),
    ("4.4", "Beglazing", 2, 5, 2, None, &[("4.3", RelKind::FS, 0), ("3.9", RelKind::FF, 2)]),
    ("4.5", "Wind- en waterdicht", 2, 0, 0, None, &[("4.4", RelKind::FS, 0)]),
    ("5", "5. Installaties", 1, 0, 2, None, &[]),
    ("5.1", "Elektra eerste fase", 2, 10, 2, None, &[("4.4", RelKind::FS, 0)]),
    ("5.2", "Loodgieterswerk eerste fase", 2, 8, 2, None, &[("5.1", RelKind::FS, 0)]),
    ("5.3", "Verwarmingsinstallatie", 2, 10, 2, None, &[("5.2", RelKind::SS, 3)]),
    ("5.4", "Ventilatiesysteem", 2, 8, 2, None, &[("5.3", RelKind::FS, 0)]),
    ("5.5", "Domoticabekabeling", 2, 5, 2, None, &[("5.4", RelKind::FS, 0)]),
    ("6", "6. Afbouw", 1, 0, 0, None, &[]),
    ("6.1", "Binnenwanden", 2, 10, 0, None, &[("5.1", RelKind::SS, 21)]),
    ("6.2", "Stucwerk", 2, 12, 0, Some(3), &[("6.1", RelKind::FS, 0)]),
    ("6.3", "Tegelwerk badkamers", 2, 8, 0, None, &[("6.2", RelKind::FS, 0)]),
    ("6.4", "Dekvloeren", 2, 5, 0, None, &[("6.3", RelKind::FS, 0)]),
    ("6.5", "Schilderwerk", 2, 10, 0, None, &[("6.4", RelKind::FS, 0)]),
    ("6.6", "Keuken plaatsen", 2, 5, 2, None, &[("6.5", RelKind::FS, 0)]),
    ("6.7", "Sanitair afmonteren", 2, 5, 2, None, &[("6.6", RelKind::FS, 0)]),
    ("6.8", "Vloerafwerking", 2, 8, 0, None, &[("6.7", RelKind::FS, 0)]),
    ("7", "7. Oplevering", 1, 0, 0, None, &[]),
    ("7.1", "Buitenruimte aanleggen", 2, 5, 0, None, &[("6.8", RelKind::FS, 0)]),
    ("7.2", "Schoonmaak", 2, 3, 1, None, &[("7.1", RelKind::FS, 0)]),
    ("7.3", "Eindkeuring installaties", 2, 3, 4, None, &[("7.2", RelKind::FS, 0)]),
    ("7.4", "Oplevering", 2, 0, 0, None, &[("7.3", RelKind::FS, 0)]),
];

// ---------- Calendar ----------

fn days_in_month(year: i32, month: u32) -> u32 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        _ => {
            if (year % 4 == 0 && year % 100 != 0) || year % 400 == 0 {
                29
            } else {
                28
            }
        }
    }
}

fn is_holiday(year: i32, month: u32, day: u32) -> bool {
    HOLIDAYS.iter().any(|&(y, m, from, to)| y == year && m == month && (from..=to).contains(&day))
}

/// The calendar date of a working day: weekends (unless `weekend_work`) and
/// the holidays of the construction calendar are skipped.
fn date_of(working_day: u32, weekend_work: bool) -> (u32, u32, i32) {
    let (mut year, mut month, mut day) = PROJECT_START;
    let mut weekday = 0; // Monday
    let mut left = working_day;
    loop {
        let working = (weekend_work || weekday < 5) && !is_holiday(year, month, day);
        if working {
            if left == 0 {
                return (day, month, year);
            }
            left -= 1;
        }
        day += 1;
        weekday = (weekday + 1) % 7;
        if day > days_in_month(year, month) {
            day = 1;
            month += 1;
            if month > 12 {
                month = 1;
                year += 1;
            }
        }
    }
}

/// `dd-mm-jjjj`, as the app shows dates.
fn dmy(working_day: u32, weekend_work: bool) -> String {
    let (d, m, y) = date_of(working_day, weekend_work);
    format!("{d:02}-{m:02}-{y}")
}

/// ISO week number of a date.
fn iso_week(year: i32, month: u32, day: u32) -> u32 {
    let ordinal: u32 = (1..month).map(|m| days_in_month(year, m)).sum::<u32>() + day;
    // 1 March 2027 is a Monday; count weekdays from there (Monday = 1).
    let days_from_start = i64::from(ordinal) - 60 + if year == 2027 { 0 } else { 365 * i64::from(year - 2027) };
    let weekday = ((days_from_start % 7 + 7) % 7) as u32 + 1;
    let week = (ordinal + 10 - weekday) / 7;
    if week == 0 {
        52
    } else if week == 53 {
        1
    } else {
        week
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

// ---------- State ----------

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Workspace {
    Gantt,
    Table,
    Resources,
    Report,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Zoom {
    Day,
    Week,
    Month,
}

impl Zoom {
    const ALL: [Self; 3] = [Self::Day, Self::Week, Self::Month];
    /// Pixels per working day.
    fn px(self) -> f32 {
        match self {
            Self::Day => 28.0,
            Self::Week => 14.0,
            Self::Month => 7.0,
        }
    }
    fn name(self) -> &'static str {
        match self {
            Self::Day => "Dag",
            Self::Week => "Week",
            Self::Month => "Maand",
        }
    }
    fn closer(self) -> Self {
        match self {
            Self::Month => Self::Week,
            _ => Self::Day,
        }
    }
    fn further(self) -> Self {
        match self {
            Self::Day => Self::Week,
            _ => Self::Month,
        }
    }
}

impl std::fmt::Display for Zoom {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.name())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Dialog {
    Settings,
    Export,
    Print,
    Quit,
    CloseDirty(usize),
    ProjectInfo,
    Calendar,
    Shortcuts,
    Relation,
    MoveProject,
    NewResource,
    Baselines,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum MenuKind {
    App,
    Task(u32),
    Tab(usize),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Side {
    Left,
    Right,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum FilePage {
    New,
    Open,
    Examples,
    Info,
    Export,
}

/// A task in a select list.
#[derive(Debug, Clone, PartialEq)]
struct TaskChoice {
    id: u32,
    label: String,
}

impl std::fmt::Display for TaskChoice {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.label)
    }
}

struct Toast {
    id: u32,
    tone: Tone,
    title: String,
    message: String,
}

/// One open project: a document tab.
#[derive(Debug, Clone)]
struct Project {
    name: String,
    file: String,
    tasks: Vec<PlanTask>,
    next_id: u32,
    history: Vec<Vec<PlanTask>>,
    future: Vec<Vec<PlanTask>>,
    baseline: Option<HashMap<u32, (u32, u32)>>,
    selected: Option<u32>,
    collapsed: HashSet<u32>,
    dirty: bool,
    scheduled: bool,
    status_date: Option<u32>,
    resources: Vec<String>,
    weekend_work: bool,
}

#[derive(Debug, Clone)]
enum Msg {
    Theme(ThemeId),
    Workspace(WorkspaceSetting),
    Statusbar(StatusbarSetting),
    RibbonTab(usize),
    Backstage(bool),
    FilePage(FilePage),
    OpenExample(usize),
    Restart,
    SkipStart(bool),
    SelectDoc(usize),
    CloseDoc(usize),
    CloseOthers(usize),
    CloseAll,
    CloseActive,
    ShowWorkspace(Workspace),
    ToggleHistogram,
    Select(Option<u32>),
    ToggleCollapse(u32),
    CollapseAll(bool),
    AddTask,
    AddMilestone,
    Indent,
    Outdent,
    Delete,
    Renumber,
    EditName(String),
    EditDuration(String),
    EditProgress(f32),
    EditCategory(&'static str),
    EditResource(String),
    SetMilestone(bool),
    ShiftStart(i32),
    RemovePredecessor(u32),
    RelationPick(TaskChoice),
    RelationKind(RelKind),
    ConfirmRelation,
    MoveDays(String),
    ConfirmMove,
    ResourceName(String),
    ConfirmResource,
    Schedule,
    Level,
    ClearLevel,
    SetBaseline,
    ToggleBaseline,
    ToggleCritical,
    ToggleProgressLine,
    ToggleStatusLine,
    ToggleResourceColors,
    ToggleFloatBand,
    ToggleRelations,
    ToggleExtraColumns,
    ToggleOverallocation,
    SetStatusDate(Option<u32>),
    Zoom(Zoom),
    ZoomIn,
    ZoomOut,
    HistResource(usize),
    HistStep(isize),
    TracePredecessors,
    TraceSuccessors,
    WeekendWork(bool),
    AutoSave(bool),
    Save,
    SaveAs,
    New,
    Undo,
    Redo,
    Format(&'static str),
    Landscape(bool),
    ConfirmExport,
    ConfirmPrint,
    Dialog(Option<Dialog>),
    SaveAndClose(usize),
    DiscardAndClose(usize),
    SaveAndQuit,
    QuitNow,
    CloseBanner,
    CloseToast,
    ToastExpired(u32),
    Feedback,
    Escape,
    Enter,
    ToggleLeft,
    ToggleRight,
    DragSplit(Side),
    EndDrag,
    Cursor(Point),
    WindowResized(Size),
    TitlePress,
    Minimize,
    Maximize,
    CloseWindow,
    Menu(Option<MenuKind>),
    Navigate(openaec_ui::keyboard::Navigation),
    Noop,
}

struct Planner {
    theme: ThemeId,
    workspace_setting: WorkspaceSetting,
    statusbar: StatusbarSetting,
    started: bool,
    skip_start: bool,
    backstage: bool,
    file_page: FilePage,
    ribbon_tab: usize,
    projects: Vec<Project>,
    active: usize,
    workspace: Workspace,
    show_histogram: bool,
    hist_resource: usize,
    zoom: Zoom,
    show_critical: bool,
    show_baseline: bool,
    show_progress_line: bool,
    show_status_line: bool,
    resource_colors: bool,
    show_float: bool,
    show_relations: bool,
    extra_columns: bool,
    overallocation_indicator: bool,
    autosave: bool,
    duration_text: String,
    relation_pick: Option<TaskChoice>,
    relation_kind: RelKind,
    move_text: String,
    resource_text: String,
    format: &'static str,
    landscape: bool,
    banner: Option<(Tone, String)>,
    toast: Option<Toast>,
    toast_count: u32,
    dialog: Option<Dialog>,
    menu: Option<(MenuKind, Point)>,
    show_left: bool,
    show_right: bool,
    left_width: f32,
    right_width: f32,
    drag: Option<(Side, f32, f32)>,
    cursor: Point,
    window: Size,
    maximized: bool,
    last_title_press: Option<Instant>,
}

// ---------- Project logic ----------

impl Project {
    fn example() -> Self {
        let wbs_ids: HashMap<&str, u32> = EXAMPLE.iter().enumerate().map(|(i, row)| (row.0, i as u32 + 1)).collect();
        let tasks = EXAMPLE
            .iter()
            .enumerate()
            .map(|(i, (_, name, level, duration, category, resource, preds))| PlanTask {
                id: i as u32 + 1,
                name: name.to_string(),
                level: *level,
                start: 0,
                duration: *duration,
                progress: 0,
                category: *category,
                resource: *resource,
                predecessors: preds.iter().map(|(wbs, kind, lag)| Pred { id: wbs_ids[wbs], kind: *kind, lag: *lag }).collect(),
                leveling_delay: 0,
            })
            .collect();
        let mut project = Self::new("Grachtenpand Amsterdam", "01-grachtenpand-amsterdam.ifc", tasks);
        project.schedule();
        // Progress as on the status date: finished before it, under way across it.
        let sd = DEFAULT_STATUS_DATE;
        for i in 0..project.tasks.len() {
            if project.is_summary(i) {
                continue;
            }
            let t = &mut project.tasks[i];
            t.progress = if t.end() <= sd {
                100
            } else if t.start < sd && t.duration > 0 {
                (((sd - t.start) as f32 / t.duration as f32 * 20.0).round() * 5.0) as u8
            } else {
                0
            };
        }
        project.selected = Some(wbs_ids["3.3"]);
        project
    }

    fn new(name: &str, file: &str, tasks: Vec<PlanTask>) -> Self {
        Self {
            name: name.into(),
            file: file.into(),
            next_id: tasks.iter().map(|t| t.id).max().unwrap_or(0) + 1,
            tasks,
            history: Vec::new(),
            future: Vec::new(),
            baseline: None,
            selected: None,
            collapsed: HashSet::new(),
            dirty: false,
            scheduled: true,
            status_date: Some(DEFAULT_STATUS_DATE),
            resources: RESOURCES.iter().map(|r| r.to_string()).collect(),
            weekend_work: false,
        }
    }

    fn empty(name: &str) -> Self {
        let root = PlanTask { id: 1, name: name.into(), level: 0, start: 0, duration: 0, progress: 0, category: 0, resource: None, predecessors: Vec::new(), leveling_delay: 0 };
        let mut p = Self::new(name, "", vec![root]);
        p.status_date = None;
        p.selected = Some(1);
        p
    }

    fn index(&self, id: u32) -> Option<usize> {
        self.tasks.iter().position(|t| t.id == id)
    }

    fn task(&self, id: u32) -> Option<&PlanTask> {
        self.tasks.iter().find(|t| t.id == id)
    }

    fn selected_task(&self) -> Option<&PlanTask> {
        self.selected.and_then(|id| self.task(id))
    }

    /// A summary task has children: the next row is deeper.
    fn is_summary(&self, i: usize) -> bool {
        self.tasks.get(i + 1).is_some_and(|next| next.level > self.tasks[i].level)
    }

    fn descendants(&self, i: usize) -> Vec<usize> {
        let level = self.tasks[i].level;
        self.tasks.iter().enumerate().skip(i + 1).take_while(|(_, t)| t.level > level).map(|(j, _)| j).collect()
    }

    fn leaves(&self) -> impl Iterator<Item = (usize, &PlanTask)> {
        self.tasks.iter().enumerate().filter(|(i, _)| !self.is_summary(*i))
    }

    /// Start and end of a row; a summary spans its leaf descendants.
    fn span(&self, i: usize) -> (u32, u32) {
        if self.is_summary(i) {
            let leaves: Vec<&PlanTask> = self.descendants(i).into_iter().filter(|j| !self.is_summary(*j)).map(|j| &self.tasks[j]).collect();
            let start = leaves.iter().map(|t| t.start).min().unwrap_or(0);
            let end = leaves.iter().map(|t| t.end()).max().unwrap_or(start);
            (start, end)
        } else {
            (self.tasks[i].start, self.tasks[i].end())
        }
    }

    fn project_end(&self) -> u32 {
        self.leaves().map(|(_, t)| t.end()).max().unwrap_or(0)
    }

    /// Summary progress: duration-weighted over the leaves.
    fn progress_of(&self, i: usize) -> u8 {
        if !self.is_summary(i) {
            return self.tasks[i].progress;
        }
        let leaves: Vec<&PlanTask> = self.descendants(i).into_iter().filter(|j| !self.is_summary(*j)).map(|j| &self.tasks[j]).collect();
        let total: u32 = leaves.iter().map(|t| t.duration.max(1)).sum();
        if total == 0 {
            return 0;
        }
        (leaves.iter().map(|t| t.duration.max(1) * u32::from(t.progress)).sum::<u32>() / total) as u8
    }

    /// WBS codes from the levels: 1, 1.1, 1.1.1; the project row has none.
    fn wbs(&self) -> Vec<String> {
        let mut counters = [0u32; 8];
        self.tasks
            .iter()
            .map(|t| {
                let level = usize::from(t.level);
                if level == 0 {
                    return String::new();
                }
                counters[level] += 1;
                for c in counters.iter_mut().skip(level + 1) {
                    *c = 0;
                }
                counters[1..=level].iter().map(u32::to_string).collect::<Vec<_>>().join(".")
            })
            .collect()
    }

    /// Rows that are not inside a collapsed summary.
    fn visible(&self) -> Vec<usize> {
        let mut hidden_below: Option<u8> = None;
        let mut rows = Vec::new();
        for (i, t) in self.tasks.iter().enumerate() {
            if let Some(level) = hidden_below {
                if t.level > level {
                    continue;
                }
                hidden_below = None;
            }
            rows.push(i);
            if self.collapsed.contains(&t.id) && self.is_summary(i) {
                hidden_below = Some(t.level);
            }
        }
        rows
    }

    /// Forward pass (CPM): a task starts as early as its relations allow; tasks
    /// without predecessors keep their own start.
    fn schedule(&mut self) {
        // Relations may point forward in the list, so repeat until nothing moves.
        for _ in 0..64 {
            let mut changed = false;
            for i in 0..self.tasks.len() {
                if self.is_summary(i) {
                    continue;
                }
                let t = &self.tasks[i];
                let earliest = t
                    .predecessors
                    .iter()
                    .filter_map(|p| self.tasks.iter().find(|x| x.id == p.id).map(|x| (p, x)))
                    .map(|(p, x)| match p.kind {
                        RelKind::FS => x.end() as i32 + p.lag,
                        RelKind::SS => x.start as i32 + p.lag,
                        RelKind::FF => x.end() as i32 + p.lag - t.duration as i32,
                    })
                    .max();
                if let Some(e) = earliest {
                    let start = e.max(0) as u32 + t.leveling_delay;
                    if self.tasks[i].start != start {
                        self.tasks[i].start = start;
                        changed = true;
                    }
                }
            }
            if !changed {
                break;
            }
        }
        self.scheduled = true;
    }

    /// Backward pass: total float per leaf task in working days.
    fn floats(&self) -> HashMap<u32, i32> {
        let end = self.project_end() as i32;
        let mut late_finish: HashMap<u32, i32> = HashMap::new();
        let mut floats = HashMap::new();
        for i in (0..self.tasks.len()).rev() {
            if self.is_summary(i) {
                continue;
            }
            let t = &self.tasks[i];
            let lf = self
                .leaves()
                .flat_map(|(_, s)| s.predecessors.iter().filter(|p| p.id == t.id).map(move |p| (s, p)))
                .filter_map(|(s, p)| {
                    let s_lf = *late_finish.get(&s.id)?;
                    let s_ls = s_lf - s.duration as i32;
                    Some(match p.kind {
                        RelKind::FS => s_ls - p.lag,
                        RelKind::SS => s_ls - p.lag + t.duration as i32,
                        RelKind::FF => s_lf - p.lag,
                    })
                })
                .min()
                .unwrap_or(end);
            late_finish.insert(t.id, lf);
            floats.insert(t.id, lf - t.end() as i32);
        }
        floats
    }

    fn critical(&self) -> HashSet<u32> {
        self.floats().into_iter().filter(|(_, f)| *f <= 0).map(|(id, _)| id).collect()
    }

    /// Days on which a resource has more than one task: (resource, days).
    fn overallocations(&self) -> Vec<(usize, u32)> {
        (0..self.resources.len())
            .filter_map(|r| {
                let tasks: Vec<&PlanTask> = self.leaves().filter(|(_, t)| t.resource == Some(r) && t.duration > 0).map(|(_, t)| t).collect();
                let end = tasks.iter().map(|t| t.end()).max().unwrap_or(0);
                let days = (0..end).filter(|d| tasks.iter().filter(|t| t.start <= *d && *d < t.end()).count() > 1).count() as u32;
                (days > 0).then_some((r, days))
            })
            .collect()
    }

    /// Tasks of a resource per week (`None`: all resources).
    fn histogram(&self, resource: Option<usize>) -> Vec<u32> {
        let tasks: Vec<&PlanTask> = self.leaves().filter(|(_, t)| t.resource.is_some() && resource.is_none_or(|r| t.resource == Some(r))).map(|(_, t)| t).collect();
        (0..self.weeks()).map(|wk| (wk * 5..wk * 5 + 5).map(|d| tasks.iter().filter(|t| t.start <= d && d < t.end()).count() as u32).sum()).collect()
    }

    fn weeks(&self) -> u32 {
        ((self.project_end() + 10) / 5 + 1).max(16)
    }

    fn remember(&mut self) {
        self.history.push(self.tasks.clone());
        if self.history.len() > 60 {
            self.history.remove(0);
        }
        self.future.clear();
        self.dirty = true;
        self.scheduled = false;
    }

    fn task_choices(&self) -> Vec<TaskChoice> {
        let wbs = self.wbs();
        let sel = self.selected_task();
        self.leaves()
            .filter(|(_, t)| sel.is_none_or(|s| s.id != t.id && !s.predecessors.iter().any(|p| p.id == t.id)))
            .map(|(i, t)| TaskChoice { id: t.id, label: format!("{} {}", wbs[i], t.name) })
            .collect()
    }
}

// ---------- Application ----------

impl Default for Planner {
    fn default() -> Self {
        let mut planner = Self {
            theme: ThemeId::Light,
            workspace_setting: WorkspaceSetting::Theme,
            statusbar: StatusbarSetting::Theme,
            started: false,
            skip_start: false,
            backstage: false,
            file_page: FilePage::Open,
            ribbon_tab: TAB_START,
            projects: vec![Project::example()],
            active: 0,
            workspace: Workspace::Gantt,
            show_histogram: false,
            hist_resource: 3,
            zoom: Zoom::Week,
            show_critical: true,
            show_baseline: false,
            show_progress_line: false,
            show_status_line: true,
            resource_colors: false,
            show_float: false,
            show_relations: true,
            extra_columns: false,
            overallocation_indicator: true,
            autosave: false,
            duration_text: String::new(),
            relation_pick: None,
            relation_kind: RelKind::FS,
            move_text: "5".into(),
            resource_text: String::new(),
            format: FORMATS[0],
            landscape: true,
            banner: None,
            toast: None,
            toast_count: 0,
            dialog: None,
            menu: None,
            show_left: false,
            show_right: true,
            left_width: 240.0,
            right_width: 260.0,
            drag: None,
            cursor: Point::ORIGIN,
            window: Size::new(1280.0, 800.0),
            maximized: false,
            last_title_press: None,
        };
        planner.after_change();
        planner
    }
}

impl Planner {
    fn look(&self) -> Look {
        Look::new(self.theme, self.workspace_setting, self.statusbar)
    }

    fn project(&self) -> Option<&Project> {
        self.projects.get(self.active)
    }

    fn project_mut(&mut self) -> Option<&mut Project> {
        self.projects.get_mut(self.active)
    }

    fn dirty(&self) -> bool {
        self.projects.iter().any(|p| p.dirty)
    }

    fn overallocation_banner(&self) -> Option<(Tone, String)> {
        let p = self.project()?;
        if !self.overallocation_indicator {
            return None;
        }
        let over = p.overallocations();
        match over.as_slice() {
            [] => None,
            [(r, days)] => Some((Tone::Warning, format!("{} is op {days} dagen overbezet. Nivelleer via Resources › Nivelleren.", p.resources[*r]))),
            many => Some((Tone::Warning, format!("{} resources zijn overbezet. Nivelleer via Resources › Nivelleren.", many.len()))),
        }
    }

    fn after_change(&mut self) {
        self.banner = self.overallocation_banner();
        self.duration_text = self.project().and_then(Project::selected_task).map(|t| t.duration.to_string()).unwrap_or_default();
    }

    fn select(&mut self, id: Option<u32>) {
        if let Some(p) = self.project_mut() {
            p.selected = id.filter(|id| p.task(*id).is_some());
        }
        self.after_change();
    }

    fn toast(&mut self, tone: Tone, title: &str, message: impl Into<String>) -> Task<Msg> {
        self.toast_count += 1;
        let id = self.toast_count;
        self.toast = Some(Toast { id, tone, title: title.into(), message: message.into() });
        after(4000, Msg::ToastExpired(id))
    }

    fn close_doc(&mut self, i: usize) {
        if i < self.projects.len() {
            self.projects.remove(i);
            self.active = self.active.min(self.projects.len().saturating_sub(1));
        }
        self.after_change();
    }

    /// Change the selected task, with undo.
    fn edit(&mut self, change: impl FnOnce(&mut PlanTask)) {
        if let Some(p) = self.project_mut() {
            if let Some(i) = p.selected.and_then(|id| p.index(id)) {
                p.remember();
                change(&mut p.tasks[i]);
            }
        }
        self.after_change();
    }

    fn insert_after_selected(&mut self, mut task: PlanTask) {
        let Some(p) = self.project_mut() else { return };
        p.remember();
        task.id = p.next_id;
        p.next_id += 1;
        let at = match p.selected.and_then(|id| p.index(id)) {
            Some(i) => {
                let summary = p.is_summary(i);
                let sel = &p.tasks[i];
                task.level = if summary { sel.level + 1 } else { sel.level.max(1) };
                if !summary {
                    task.start = sel.end();
                    task.resource = sel.resource;
                    task.category = sel.category;
                }
                i + 1
            }
            None => {
                task.level = 1;
                p.tasks.len()
            }
        };
        let id = task.id;
        p.tasks.insert(at, task);
        p.selected = Some(id);
        self.after_change();
    }

    fn update(&mut self, message: Msg) -> Task<Msg> {
        if !matches!(message, Msg::Cursor(_) | Msg::Menu(_) | Msg::WindowResized(_) | Msg::Noop) {
            self.menu = None;
        }
        match message {
            Msg::Theme(t) => self.theme = t,
            Msg::Workspace(s) => self.workspace_setting = s,
            Msg::Statusbar(s) => self.statusbar = s,
            Msg::RibbonTab(i) => {
                self.ribbon_tab = i;
                // As in the app: the Tabel and Rapport tabs show their own workspace.
                self.workspace = match i {
                    TAB_TABLE => Workspace::Table,
                    TAB_REPORT => Workspace::Report,
                    _ if matches!(self.workspace, Workspace::Table | Workspace::Report) => Workspace::Gantt,
                    _ => self.workspace,
                };
            }
            Msg::Backstage(open) => self.backstage = open,
            Msg::FilePage(p) => self.file_page = p,
            Msg::OpenExample(i) => {
                if i != 0 {
                    return self.toast(Tone::Info, "Niet in de testversie", format!("Alleen {} is ingeladen; de andere voorbeelden volgen met de echte IFC-lezer.", EXAMPLES[0].0));
                }
                self.backstage = false;
                self.started = true;
                match self.projects.iter().position(|p| p.file == EXAMPLES[0].2) {
                    Some(at) => self.active = at,
                    None => {
                        self.projects.push(Project::example());
                        self.active = self.projects.len() - 1;
                    }
                }
                self.after_change();
                return self.toast(Tone::Info, "Project geopend", format!("{} is geopend.", EXAMPLES[0].0));
            }
            Msg::Restart => {
                self.started = self.skip_start;
                self.backstage = false;
                self.dialog = None;
                if self.skip_start {
                    return self.toast(Tone::Info, "Laatste project geopend", "Direct geopend, zonder startscherm.");
                }
            }
            Msg::SkipStart(b) => self.skip_start = b,
            Msg::SelectDoc(i) => {
                self.active = i.min(self.projects.len().saturating_sub(1));
                self.after_change();
            }
            Msg::CloseDoc(i) => {
                if self.projects.get(i).is_some_and(|p| p.dirty) {
                    self.dialog = Some(Dialog::CloseDirty(i));
                } else {
                    self.close_doc(i);
                }
            }
            Msg::CloseOthers(keep) => {
                let name = self.projects.get(keep).map(|p| p.name.clone());
                self.projects.retain(|p| Some(&p.name) == name.as_ref() || p.dirty);
                self.active = self.projects.iter().position(|p| Some(&p.name) == name.as_ref()).unwrap_or(0);
                self.after_change();
                if self.projects.len() > 1 {
                    return self.toast(Tone::Info, "Niet alles gesloten", "Projecten met wijzigingen blijven open. Sla eerst op.");
                }
            }
            Msg::CloseAll => {
                self.projects.retain(|p| p.dirty);
                self.active = 0;
                self.after_change();
                if !self.projects.is_empty() {
                    return self.toast(Tone::Info, "Niet alles gesloten", "Projecten met wijzigingen blijven open. Sla eerst op.");
                }
            }
            Msg::CloseActive => {
                if !self.projects.is_empty() {
                    return self.update(Msg::CloseDoc(self.active));
                }
            }
            Msg::ShowWorkspace(ws) => {
                self.workspace = if self.workspace == ws && ws == Workspace::Resources { Workspace::Gantt } else { ws };
                if ws == Workspace::Table {
                    self.ribbon_tab = TAB_TABLE;
                } else if ws == Workspace::Report {
                    self.ribbon_tab = TAB_REPORT;
                } else if matches!(self.ribbon_tab, TAB_TABLE | TAB_REPORT) {
                    self.ribbon_tab = TAB_START;
                }
            }
            Msg::ToggleHistogram => self.show_histogram = !self.show_histogram,
            Msg::Select(id) => self.select(id),
            Msg::ToggleCollapse(id) => {
                if let Some(p) = self.project_mut() {
                    if !p.collapsed.remove(&id) {
                        p.collapsed.insert(id);
                    }
                }
            }
            Msg::CollapseAll(collapse) => {
                if let Some(p) = self.project_mut() {
                    p.collapsed.clear();
                    if collapse {
                        let phases: Vec<u32> = (0..p.tasks.len()).filter(|i| p.tasks[*i].level == 1 && p.is_summary(*i)).map(|i| p.tasks[i].id).collect();
                        p.collapsed.extend(phases);
                    }
                }
            }
            Msg::AddTask => self.insert_after_selected(PlanTask { id: 0, name: "Nieuwe taak".into(), level: 1, start: 0, duration: 5, progress: 0, category: 0, resource: None, predecessors: Vec::new(), leveling_delay: 0 }),
            Msg::AddMilestone => self.insert_after_selected(PlanTask { id: 0, name: "Nieuwe mijlpaal".into(), level: 1, start: 0, duration: 0, progress: 0, category: 0, resource: None, predecessors: Vec::new(), leveling_delay: 0 }),
            Msg::Indent | Msg::Outdent => {
                let indent = matches!(message, Msg::Indent);
                let Some(p) = self.project_mut() else { return Task::none() };
                let Some(i) = p.selected.and_then(|id| p.index(id)) else { return Task::none() };
                let level = p.tasks[i].level;
                let allowed = if indent { i > 0 && p.tasks[i - 1].level >= level && level < 4 && level > 0 } else { level > 1 };
                if !allowed {
                    return self.toast(Tone::Info, if indent { "Kan niet inspringen" } else { "Kan niet uitspringen" }, if indent { "Een taak springt in onder de taak erboven." } else { "Deze taak staat al op het hoogste niveau." });
                }
                p.remember();
                let rows = p.descendants(i);
                for j in std::iter::once(i).chain(rows) {
                    p.tasks[j].level = if indent { p.tasks[j].level + 1 } else { p.tasks[j].level - 1 };
                }
                self.after_change();
            }
            Msg::Delete => {
                let Some(p) = self.project_mut() else { return Task::none() };
                let Some(i) = p.selected.and_then(|id| p.index(id)) else { return Task::none() };
                if p.tasks[i].level == 0 {
                    return self.toast(Tone::Info, "Projectregel", "De projectregel kun je niet verwijderen.");
                }
                p.remember();
                let mut gone: Vec<u32> = p.descendants(i).into_iter().map(|j| p.tasks[j].id).collect();
                gone.push(p.tasks[i].id);
                let name = p.tasks[i].name.clone();
                p.tasks.retain(|t| !gone.contains(&t.id));
                for t in &mut p.tasks {
                    t.predecessors.retain(|x| !gone.contains(&x.id));
                }
                p.selected = None;
                p.schedule();
                p.scheduled = false;
                self.after_change();
                let extra = gone.len() - 1;
                let message = if extra > 0 { format!("{name} en {extra} onderliggende taken zijn verwijderd. Ongedaan maken met Ctrl+Z.") } else { format!("{name} is verwijderd. Ongedaan maken met Ctrl+Z.") };
                return self.toast(Tone::Info, "Verwijderd", message);
            }
            Msg::Renumber => return self.toast(Tone::Success, "WBS hernummerd", "De codes volgen weer de volgorde en de niveaus."),
            Msg::EditName(name) => self.edit(|t| t.name = name),
            Msg::EditDuration(text) => {
                self.duration_text = text.clone();
                if let Ok(days) = text.trim().parse::<u32>() {
                    if days <= 500 {
                        self.edit(|t| t.duration = days);
                        self.duration_text = text;
                    }
                }
            }
            Msg::EditProgress(v) => {
                let v = ((v / 5.0).round() * 5.0).clamp(0.0, 100.0) as u8;
                if self.project().and_then(Project::selected_task).is_some_and(|t| t.progress != v) {
                    self.edit(|t| t.progress = v);
                }
            }
            Msg::EditCategory(name) => {
                let c = CATEGORIES.iter().position(|x| *x == name).unwrap_or(0);
                self.edit(|t| t.category = c);
            }
            Msg::EditResource(name) => {
                let r = self.project().and_then(|p| p.resources.iter().position(|x| *x == name));
                self.edit(|t| t.resource = r);
            }
            Msg::SetMilestone(on) => self.edit(|t| t.duration = if on { 0 } else { 1 }),
            Msg::ShiftStart(days) => {
                if self.project().and_then(Project::selected_task).is_some_and(|t| !t.predecessors.is_empty()) {
                    return self.toast(Tone::Info, "Start volgt uit de relaties", "Verwijder eerst de voorgangers om de start zelf te kiezen.");
                }
                self.edit(|t| t.start = (t.start as i32 + days).max(0) as u32);
            }
            Msg::RemovePredecessor(id) => self.edit(|t| t.predecessors.retain(|p| p.id != id)),
            Msg::RelationPick(choice) => self.relation_pick = Some(choice),
            Msg::RelationKind(kind) => self.relation_kind = kind,
            Msg::ConfirmRelation => {
                if let Some(choice) = self.relation_pick.take() {
                    let kind = self.relation_kind;
                    self.edit(|t| t.predecessors.push(Pred { id: choice.id, kind, lag: 0 }));
                    self.dialog = None;
                    return self.toast(Tone::Success, "Relatie toegevoegd", format!("{} is nu een {}-voorganger. Bereken de planning met F5.", choice.label, kind.code()));
                }
            }
            Msg::MoveDays(text) => self.move_text = text,
            Msg::ConfirmMove => {
                let Ok(days) = self.move_text.trim().parse::<i32>() else {
                    return self.toast(Tone::Error, "Geen getal", "Vul een aantal werkdagen in, bijvoorbeeld 5 of -3.");
                };
                if let Some(p) = self.project_mut() {
                    p.remember();
                    for t in &mut p.tasks {
                        t.start = (t.start as i32 + days).max(0) as u32;
                    }
                    p.schedule();
                }
                self.dialog = None;
                self.after_change();
                return self.toast(Tone::Success, "Project verplaatst", format!("Alle taken zijn {} werkdagen verschoven.", days.abs()));
            }
            Msg::ResourceName(text) => self.resource_text = text,
            Msg::ConfirmResource => {
                let name = self.resource_text.trim().to_string();
                if name.is_empty() {
                    return self.toast(Tone::Error, "Geen naam", "Geef de resource een naam.");
                }
                if let Some(p) = self.project_mut() {
                    p.resources.push(name.clone());
                    p.dirty = true;
                }
                self.resource_text.clear();
                self.dialog = None;
                self.workspace = Workspace::Resources;
                return self.toast(Tone::Success, "Resource toegevoegd", format!("{name} staat in de lijst en kun je aan taken toewijzen."));
            }
            Msg::Schedule => {
                let Some(p) = self.project_mut() else { return Task::none() };
                let before: Vec<u32> = p.tasks.iter().map(|t| t.start).collect();
                p.schedule();
                let moved = p.tasks.iter().zip(before).filter(|(t, b)| t.start != *b).count();
                let end = dmy(p.project_end(), p.weekend_work);
                self.after_change();
                let message = if moved == 0 { format!("Niets verschoven. Einde blijft {end}.") } else { format!("{moved} taken verschoven. Einde {end}.") };
                return self.toast(Tone::Success, "Planning berekend", message);
            }
            Msg::Level => {
                let Some(p) = self.project_mut() else { return Task::none() };
                if p.overallocations().is_empty() {
                    return self.toast(Tone::Info, "Niets te nivelleren", "Geen resource is overbezet.");
                }
                p.remember();
                let mut shifted = 0;
                // Delay the later task of each overlap and recalculate, until no
                // resource is overbooked (successors move along, so repeat).
                for _ in 0..40 {
                    let mut changed = false;
                    for r in 0..p.resources.len() {
                        let mut order: Vec<usize> = (0..p.tasks.len()).filter(|i| !p.is_summary(*i) && p.tasks[*i].resource == Some(r) && p.tasks[*i].duration > 0).collect();
                        order.sort_by_key(|i| (p.tasks[*i].start, *i));
                        let mut free = 0;
                        for i in order {
                            if p.tasks[i].start < free {
                                p.tasks[i].leveling_delay += free - p.tasks[i].start;
                                p.tasks[i].start = free;
                                shifted += 1;
                                changed = true;
                            }
                            free = p.tasks[i].end();
                        }
                    }
                    p.schedule();
                    if !changed {
                        break;
                    }
                }
                let end = dmy(p.project_end(), p.weekend_work);
                self.after_change();
                return self.toast(Tone::Success, "Genivelleerd", format!("{shifted} taken verschoven; einde {end}."));
            }
            Msg::ClearLevel => {
                let Some(p) = self.project_mut() else { return Task::none() };
                if p.tasks.iter().all(|t| t.leveling_delay == 0) {
                    return self.toast(Tone::Info, "Geen nivellering", "Er is geen nivelleringsvertraging om te wissen.");
                }
                p.remember();
                for t in &mut p.tasks {
                    t.leveling_delay = 0;
                }
                p.schedule();
                self.after_change();
                return self.toast(Tone::Info, "Nivellering gewist", "Alle nivelleringsvertragingen zijn verwijderd en de planning is herberekend.");
            }
            Msg::Undo => {
                if let Some(p) = self.project_mut() {
                    if let Some(previous) = p.history.pop() {
                        p.future.push(std::mem::replace(&mut p.tasks, previous));
                        p.selected = p.selected.filter(|id| p.task(*id).is_some());
                    }
                }
                self.after_change();
            }
            Msg::Redo => {
                if let Some(p) = self.project_mut() {
                    if let Some(next) = p.future.pop() {
                        p.history.push(std::mem::replace(&mut p.tasks, next));
                        p.selected = p.selected.filter(|id| p.task(*id).is_some());
                    }
                }
                self.after_change();
            }
            Msg::SetBaseline => {
                if let Some(p) = self.project_mut() {
                    p.baseline = Some(p.tasks.iter().map(|t| (t.id, (t.start, t.duration))).collect());
                }
                self.show_baseline = true;
                self.dialog = None;
                return self.toast(Tone::Success, "Baseline vastgelegd", "De huidige planning is de baseline. Verschillen zie je onder de balken.");
            }
            Msg::ToggleBaseline => {
                if self.project().is_some_and(|p| p.baseline.is_none()) {
                    return self.toast(Tone::Info, "Geen baseline", "Leg eerst een baseline vast via Planning › Baselines beheren.");
                }
                self.show_baseline = !self.show_baseline;
            }
            Msg::ToggleCritical => self.show_critical = !self.show_critical,
            Msg::ToggleProgressLine => self.show_progress_line = !self.show_progress_line,
            Msg::ToggleStatusLine => self.show_status_line = !self.show_status_line,
            Msg::ToggleResourceColors => self.resource_colors = !self.resource_colors,
            Msg::ToggleFloatBand => self.show_float = !self.show_float,
            Msg::ToggleRelations => self.show_relations = !self.show_relations,
            Msg::ToggleExtraColumns => self.extra_columns = !self.extra_columns,
            Msg::ToggleOverallocation => {
                self.overallocation_indicator = !self.overallocation_indicator;
                self.banner = self.overallocation_banner();
            }
            Msg::SetStatusDate(date) => {
                let weekend = self.project().is_some_and(|p| p.weekend_work);
                if let Some(p) = self.project_mut() {
                    p.status_date = date;
                }
                return match date {
                    Some(d) => self.toast(Tone::Info, "Statusdatum", format!("De statusdatum staat op {}.", dmy(d, weekend))),
                    None => self.toast(Tone::Info, "Statusdatum leeggemaakt", "De statusdatumlijn is verborgen."),
                };
            }
            Msg::Zoom(z) => self.zoom = z,
            Msg::ZoomIn => self.zoom = self.zoom.closer(),
            Msg::ZoomOut => self.zoom = self.zoom.further(),
            Msg::HistResource(r) => {
                self.hist_resource = r;
                self.show_histogram = true;
            }
            Msg::HistStep(step) => {
                let n = self.project().map_or(1, |p| p.resources.len() + 1) as isize;
                self.hist_resource = ((self.hist_resource as isize + step).rem_euclid(n)) as usize;
                self.show_histogram = true;
            }
            Msg::TracePredecessors | Msg::TraceSuccessors => {
                let Some(p) = self.project() else { return Task::none() };
                let Some(t) = p.selected_task() else {
                    return self.toast(Tone::Info, "Niets gekozen", "Kies eerst een taak.");
                };
                let preds = matches!(message, Msg::TracePredecessors);
                let names: Vec<String> = if preds {
                    t.predecessors.iter().filter_map(|x| p.task(x.id)).map(|x| x.name.clone()).collect()
                } else {
                    p.tasks.iter().filter(|x| x.predecessors.iter().any(|y| y.id == t.id)).map(|x| x.name.clone()).collect()
                };
                let title = if preds { "Voorgangers" } else { "Opvolgers" };
                let message = if names.is_empty() { format!("Deze taak heeft geen {}.", title.to_lowercase()) } else { names.join(", ") };
                return self.toast(Tone::Info, title, message);
            }
            Msg::WeekendWork(b) => {
                if let Some(p) = self.project_mut() {
                    p.weekend_work = b;
                    p.dirty = true;
                }
            }
            Msg::AutoSave(b) => self.autosave = b,
            Msg::Save | Msg::SaveAs => {
                let save_as = matches!(message, Msg::SaveAs);
                let Some(p) = self.project_mut() else { return Task::none() };
                p.dirty = false;
                let name = p.name.clone();
                return if save_as { self.toast(Tone::Success, "Opgeslagen als", format!("{name} kopie.ifc is opgeslagen (IFC 4.3).")) } else { self.toast(Tone::Success, "Opgeslagen", format!("{name}.ifc is opgeslagen (IFC 4.3).")) };
            }
            Msg::New => {
                self.projects.push(Project::empty("Nieuwe planning"));
                self.active = self.projects.len() - 1;
                self.started = true;
                self.backstage = false;
                self.workspace = Workspace::Gantt;
                self.after_change();
                return self.toast(Tone::Info, "Nieuwe planning", "Voeg taken toe met Ctrl+N of de linttab Start.");
            }
            Msg::Format(f) => self.format = f,
            Msg::Landscape(b) => self.landscape = b,
            Msg::ConfirmExport => {
                self.dialog = None;
                let name = self.project().map(|p| p.name.clone()).unwrap_or_default();
                return self.toast(Tone::Success, "Geëxporteerd", format!("{name} is als {} opgeslagen in Projecten/{name}.", self.format));
            }
            Msg::ConfirmPrint => {
                self.dialog = None;
                return self.toast(Tone::Success, "Afgedrukt", format!("De Gantt is {} naar de standaardprinter gestuurd.", if self.landscape { "liggend" } else { "staand" }));
            }
            Msg::Dialog(d) => {
                if d == Some(Dialog::Relation) {
                    let Some(p) = self.project() else { return Task::none() };
                    if p.selected_task().is_none_or(|t| p.index(t.id).is_some_and(|i| p.is_summary(i))) {
                        return self.toast(Tone::Info, "Kies een taak", "Relaties leg je tussen gewone taken en mijlpalen, niet op samenvattingen.");
                    }
                    self.relation_pick = p.task_choices().into_iter().next();
                }
                self.dialog = d;
                if d.is_some() {
                    // The focus moves into the dialog; the screen behind it is inert.
                    return openaec_ui::keyboard::navigate(openaec_ui::keyboard::Navigation::Next);
                }
            }
            Msg::SaveAndClose(i) => {
                if let Some(p) = self.projects.get_mut(i) {
                    p.dirty = false;
                }
                self.dialog = None;
                self.close_doc(i);
            }
            Msg::DiscardAndClose(i) => {
                self.dialog = None;
                self.close_doc(i);
            }
            Msg::SaveAndQuit => {
                for p in &mut self.projects {
                    p.dirty = false;
                }
                return iced::window::latest().and_then(iced::window::close);
            }
            Msg::QuitNow => return iced::window::latest().and_then(iced::window::close),
            Msg::CloseBanner => self.banner = None,
            Msg::CloseToast => self.toast = None,
            Msg::ToastExpired(id) => {
                if self.toast.as_ref().is_some_and(|t| t.id == id) {
                    self.toast = None;
                }
            }
            Msg::Feedback => return self.toast(Tone::Info, "Feedback geven", "In de app opent hier het feedbackvenster naar GitHub."),
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
                    Some(Dialog::Relation) => Some(Msg::ConfirmRelation),
                    Some(Dialog::MoveProject) => Some(Msg::ConfirmMove),
                    Some(Dialog::NewResource) => Some(Msg::ConfirmResource),
                    Some(Dialog::Baselines) => Some(Msg::SetBaseline),
                    Some(_) => Some(Msg::Dialog(None)),
                    None => None,
                };
                if let Some(msg) = next {
                    return self.update(msg);
                }
            }
            Msg::ToggleLeft => self.show_left = !self.show_left,
            Msg::ToggleRight => self.show_right = !self.show_right,
            Msg::DragSplit(side) => {
                let width = match side {
                    Side::Left => self.left_width,
                    Side::Right => self.right_width,
                };
                self.drag = Some((side, self.cursor.x, width));
            }
            Msg::EndDrag => self.drag = None,
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
                if self.dirty() {
                    self.dialog = Some(Dialog::Quit);
                } else {
                    return iced::window::latest().and_then(iced::window::close);
                }
            }
            Msg::Menu(kind) => {
                self.menu = kind.map(|k| (k, self.cursor));
                if let Some(MenuKind::Task(id)) = kind {
                    self.select(Some(id));
                }
                if kind.is_some() {
                    return openaec_ui::keyboard::navigate(openaec_ui::keyboard::Navigation::Next);
                }
            }
            Msg::Navigate(step) => return openaec_ui::keyboard::navigate(step),
            Msg::Noop => {}
        }
        Task::none()
    }

    fn subscription(&self) -> Subscription<Msg> {
        let keys = openaec_ui::keyboard::on_key_press(|key, mods| {
            use keyboard::key::Named;
            use keyboard::Key;
            match (key.as_ref(), mods.command(), mods.alt()) {
                (Key::Named(Named::Escape), _, _) => Some(Msg::Escape),
                (Key::Named(Named::Enter), false, false) => Some(Msg::Enter),
                (Key::Named(Named::Delete), false, false) => Some(Msg::Delete),
                (Key::Named(Named::F5), _, _) => Some(Msg::Schedule),
                (Key::Named(Named::ArrowRight), false, true) => Some(Msg::Indent),
                (Key::Named(Named::ArrowLeft), false, true) => Some(Msg::Outdent),
                (Key::Character("s"), true, _) => Some(Msg::Save),
                (Key::Character("n"), true, _) => Some(Msg::AddTask),
                (Key::Character("m"), true, _) => Some(Msg::AddMilestone),
                (Key::Character("z"), true, _) => Some(Msg::Undo),
                (Key::Character("y"), true, _) => Some(Msg::Redo),
                (Key::Character("p"), true, _) => Some(Msg::Dialog(Some(Dialog::Print))),
                (Key::Character("e"), true, _) => Some(Msg::Dialog(Some(Dialog::Export))),
                (Key::Character(","), true, _) => Some(Msg::Dialog(Some(Dialog::Settings))),
                (Key::Character("1"), true, _) => Some(Msg::ToggleLeft),
                (Key::Character("2"), true, _) => Some(Msg::ToggleRight),
                (Key::Character("+") | Key::Character("="), true, _) => Some(Msg::ZoomIn),
                (Key::Character("-"), true, _) => Some(Msg::ZoomOut),
                (Key::Character("0"), true, _) => Some(Msg::Zoom(Zoom::Week)),
                (Key::Character("w"), true, _) => Some(Msg::CloseActive),
                _ => None,
            }
        });
        Subscription::batch([keys, openaec_ui::keyboard::navigation().map(Msg::Navigate), iced::window::resize_events().map(|(_, size)| Msg::WindowResized(size))])
    }

    // ---------- Views ----------

    fn view(&self) -> Element<'_, Msg> {
        let look = self.look();
        let screen = container(self.screen(look)).height(Length::Fill);
        let mut layers = vec![openaec_ui::design::focus::inert(screen, self.menu.is_some() || self.dialog.is_some())];
        if let Some(toast) = &self.toast {
            let card = w::toast(look, toast.tone, tone_icon(toast.tone), &toast.title, &toast.message, s(Icon::WindowClose), Some(Msg::CloseToast));
            layers.push(container(card).width(Length::Fill).height(Length::Fill).align_right(Length::Fill).align_bottom(Length::Fill).padding([36, 16]).into());
        }
        if let Some((kind, at)) = self.menu {
            let items = self.menu_items(kind);
            let height = ch::menu_height(&items);
            let menu = ch::menu(look, items, s(Icon::StatusSuccess));
            layers.push(ch::menu_layer(menu, at, Size::new(ch::MENU_WIDTH, height), self.window, Msg::Menu(None)));
        }
        if let Some(dialog) = self.dialog {
            layers.push(mouse_area(w::overlay(look, self.dialog_card(look, dialog))).on_press(Msg::Noop).into());
        }
        let root = mouse_area(Stack::with_children(layers)).on_move(Msg::Cursor).on_release(Msg::EndDrag);
        if self.drag.is_some() {
            root.interaction(mouse::Interaction::ResizingHorizontally).into()
        } else {
            root.into()
        }
    }

    fn screen(&self, look: Look) -> Element<'_, Msg> {
        if !self.started {
            return column![self.title_bar(look, "Open Planner Studio · testversie UI 0.4".into(), false), self.start_screen(look), w::status_bar(look, vec!["Kies een project om te beginnen".into()], vec!["UI 0.4".into()])].into();
        }
        let name = self.project().map_or("Open Planner Studio".to_string(), |p| format!("Open Planner Studio · {}{}", if p.dirty { "* " } else { "" }, p.name));
        let title = self.title_bar(look, name, true);
        let tabs = w::ribbon_tabs(look, "Bestand", Some(Msg::Backstage(!self.backstage)), &TABS, if self.backstage { usize::MAX } else { self.ribbon_tab }, Msg::RibbonTab);
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
        column![title, tabs, self.ribbon(look), w::divider(look), main, self.status_bar(look)].into()
    }

    /// The status bar as in the app: tasks, milestones, critical path, end,
    /// overallocation and selection on the left; scale, zoom and unsaved on the right.
    fn status_bar(&self, look: Look) -> Element<'_, Msg> {
        let Some(p) = self.project() else {
            return w::status_bar(look, vec!["Geen project geopend".into()], vec![format!("Schaal: {}", self.zoom.name())]);
        };
        let leaves = p.leaves().filter(|(_, t)| t.level > 0).count();
        let milestones = p.tasks.iter().filter(|t| t.milestone() && t.level > 0).count();
        let critical = p.critical().len();
        let mut left = vec![format!("Taken: {leaves}"), format!("Mijlpalen: {milestones}"), format!("Kritiek pad: {critical} taken, {} werkdagen", p.project_end()), format!("Einde: {}", dmy(p.project_end(), p.weekend_work))];
        let over = p.overallocations().len();
        if over > 0 {
            left.push(format!("⚠ {over} resource(s) overbezet"));
        }
        if !p.scheduled {
            left.push("Verouderd — herbereken (F5)".into());
        }
        left.push(format!("Selectie: {} taak", usize::from(p.selected_task().is_some())));
        let mut right = vec![format!("Schaal: {}", self.zoom.name()), format!("Zoom: {}px/dag", self.zoom.px() as u32)];
        if p.dirty {
            right.push("Niet opgeslagen".into());
        }
        w::status_bar(look, left, right)
    }

    fn ribbon(&self, look: Look) -> Element<'_, Msg> {
        let p = self.project();
        let has_project = p.is_some();
        let sel = p.and_then(Project::selected_task).is_some();
        let on_sel = |m: Msg| sel.then_some(m);
        let on_project = |m: Msg| has_project.then_some(m);
        let can_undo = p.is_some_and(|p| !p.history.is_empty());
        let can_redo = p.is_some_and(|p| !p.future.is_empty());
        let stale = p.is_some_and(|p| !p.scheduled);
        let over = p.map_or(0, |p| p.overallocations().len());
        let ws = |w: Workspace| self.workspace == w;

        let file_group = || {
            w::ribbon_group(look, "Bestand", vec![
                stack(vec![
                    w::ribbon_small(look, s(Icon::FileNew), "Nieuw", false, Some(Msg::New)),
                    w::ribbon_small(look, s(Icon::FileSave), "Opslaan", false, on_project(Msg::Save)),
                    w::ribbon_small(look, s(Icon::FileOpen), "Openen", false, Some(Msg::Backstage(true))),
                ]),
                stack(vec![
                    w::ribbon_small(look, s(Icon::FileSaveAs), "Opslaan als", false, on_project(Msg::SaveAs)),
                    w::ribbon_small(look, s(Icon::ProjectRecent), "Recent", false, Some(Msg::FilePage(FilePage::Open))),
                    w::ribbon_small(look, s(Icon::FileExport), "Exporteren", false, on_project(Msg::Dialog(Some(Dialog::Export)))),
                ]),
            ])
        };
        let edit_group = || {
            w::ribbon_group(look, "Bewerken", vec![stack(vec![
                w::ribbon_small(look, s(Icon::EditUndo), "Ongedaan", false, can_undo.then_some(Msg::Undo)),
                w::ribbon_small(look, s(Icon::EditRedo), "Opnieuw", false, can_redo.then_some(Msg::Redo)),
                w::ribbon_small(look, s(Icon::EditDelete), "Verwijder", false, on_sel(Msg::Delete)),
            ])])
        };
        let tasks_group = || {
            w::ribbon_group(look, "Taken", vec![
                w::ribbon_large(look, l(Icon::TaskAdd), "Taak", false, on_project(Msg::AddTask)),
                w::ribbon_large(look, l(Icon::TaskMilestoneMenu), "Mijlpaal", false, on_project(Msg::AddMilestone)),
                w::ribbon_large(look, l(Icon::PlanningDependencyAdd), "Relatie", false, on_sel(Msg::Dialog(Some(Dialog::Relation)))),
                w::ribbon_large(look, l(Icon::TaskSplitMode), "Taak splitsen", false, None),
            ])
        };
        let schedule_group = || w::ribbon_group(look, "Planning", vec![w::ribbon_large(look, l(Icon::PlanningCalculate), "Bereken", stale, on_project(Msg::Schedule))]);
        let progress_group = || {
            w::ribbon_group(look, "Voortgang", vec![stack(vec![
                w::ribbon_small(look, s(Icon::FileExport), "Voortgangsblad exporteren", false, on_project(Msg::Dialog(Some(Dialog::Export)))),
                w::ribbon_small(look, s(Icon::FileImport), "Voortgang bijwerken uit een blad", false, None),
            ])])
        };
        let trace_group = || {
            w::ribbon_group(look, "Pad traceren", vec![
                w::ribbon_large(look, l(Icon::PlanningTracePredecessors), "Voorgangers", false, on_sel(Msg::TracePredecessors)),
                w::ribbon_large(look, l(Icon::PlanningTraceSuccessors), "Opvolgers", false, on_sel(Msg::TraceSuccessors)),
            ])
        };
        let baselines_group = || {
            w::ribbon_group(look, "Baselines & voortgang", vec![
                w::ribbon_large(look, l(Icon::PlanningBaselines), "Baselines beheren…", false, on_project(Msg::Dialog(Some(Dialog::Baselines)))),
                w::ribbon_large(look, l(Icon::PlanningStatusDate), "Statusdatum", p.is_some_and(|p| p.status_date.is_some()), on_project(Msg::SetStatusDate(Some(DEFAULT_STATUS_DATE)))),
                stack(vec![
                    w::ribbon_small(look, s(Icon::PlanningBaselineOverlay), "Baseline-overlay", self.show_baseline, Some(Msg::ToggleBaseline)),
                    w::ribbon_small(look, s(Icon::PlanningProgressLine), "Voortgangslijn", self.show_progress_line, Some(Msg::ToggleProgressLine)),
                    w::ribbon_small(look, s(Icon::PlanningStatusDateLine), "Statusdatumlijn", self.show_status_line, Some(Msg::ToggleStatusLine)),
                ]),
            ])
        };
        let zoom_stack = || {
            stack(vec![
                w::ribbon_small(look, s(Icon::ViewZoomIn), "Zoomen +", false, (self.zoom != Zoom::Day).then_some(Msg::ZoomIn)),
                w::ribbon_small(look, s(Icon::ViewZoomOut), "Zoomen -", false, (self.zoom != Zoom::Month).then_some(Msg::ZoomOut)),
            ])
        };

        let groups = match self.ribbon_tab {
            TAB_START => vec![file_group(), edit_group(), tasks_group(), schedule_group(), w::ribbon_group(look, "Zoomen", vec![zoom_stack()])],
            TAB_PLANNING => vec![
                w::ribbon_group(look, "Planning", vec![
                    w::ribbon_large(look, l(Icon::PlanningCalculate), "Bereken", stale, on_project(Msg::Schedule)),
                    w::ribbon_large(look, l(Icon::PlanningMoveDate), "Project verplaatsen…", false, on_project(Msg::Dialog(Some(Dialog::MoveProject)))),
                    w::ribbon_large(look, l(Icon::PanelWarnings), "Waarschuwingen", self.banner.is_some(), on_project(Msg::ToggleOverallocation)),
                ]),
                w::ribbon_group(look, "Relaties", vec![
                    w::ribbon_large(look, l(Icon::PlanningDependencyAdd), "Relatie", false, on_sel(Msg::Dialog(Some(Dialog::Relation)))),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::PlanningDependencyDrawMode), "Relatie tekenen", false, None),
                        w::ribbon_small(look, s(Icon::PlanningExternalRelation), "Externe relatie toevoegen…", false, None),
                        w::ribbon_small(look, s(Icon::PlanningRelationsVisible), "Relatielijnen", self.show_relations, Some(Msg::ToggleRelations)),
                    ]),
                ]),
                w::ribbon_group(look, "Kalender", vec![w::ribbon_large(look, l(Icon::CalendarManage), "Kalender", false, on_project(Msg::Dialog(Some(Dialog::Calendar))))]),
                w::ribbon_group(look, "Structuur", vec![
                    w::ribbon_large(look, l(Icon::PlanningStructure), "Codes & velden", false, None),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::WbsAutoNumber), "WBS auto", true, Some(Msg::Noop)),
                        w::ribbon_small(look, s(Icon::WbsRenumber), "Hernummer WBS", false, on_project(Msg::Renumber)),
                        w::ribbon_small(look, s(Icon::WbsTemplates), "Sjablonen", false, None),
                    ]),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::TaskIndent), "Inspringen", false, on_sel(Msg::Indent)),
                        w::ribbon_small(look, s(Icon::TaskOutdent), "Uitspringen", false, on_sel(Msg::Outdent)),
                    ]),
                ]),
                baselines_group(),
                progress_group(),
            ],
            TAB_RESOURCES => vec![
                w::ribbon_group(look, "Beheer", vec![
                    w::ribbon_large(look, l(Icon::ResourceWorkspace), "Resources", ws(Workspace::Resources), on_project(Msg::ShowWorkspace(Workspace::Resources))),
                    w::ribbon_large(look, l(Icon::ResourceDock), "Resourcedock", false, None),
                    w::ribbon_large(look, l(Icon::ResourceNew), "Nieuwe resource", false, on_project(Msg::Dialog(Some(Dialog::NewResource)))),
                ]),
                w::ribbon_group(look, "Toewijzing", vec![w::ribbon_large(look, l(Icon::ResourceAssign), "Toewijzen", false, on_sel(Msg::ToggleRight))]),
                w::ribbon_group(look, "Histogram", vec![
                    w::ribbon_large(look, l(Icon::DataChart), "Histogram", self.show_histogram, on_project(Msg::ToggleHistogram)),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::ResourcePrevious), "Vorige", false, on_project(Msg::HistStep(-1))),
                        w::ribbon_small(look, s(Icon::ResourceNext), "Volgende", false, on_project(Msg::HistStep(1))),
                    ]),
                ]),
                w::ribbon_group(look, "Nivellering", vec![
                    w::ribbon_large(look, l(Icon::ResourceLevel), "Nivelleren…", false, on_project(Msg::Level)),
                    w::ribbon_large(look, l(Icon::ResourceClearLevel), "Nivellering wissen", false, p.is_some_and(|p| p.tasks.iter().any(|t| t.leveling_delay > 0)).then_some(Msg::ClearLevel)),
                ]),
                w::ribbon_group(look, "Overallocatie", vec![w::ribbon_large(
                    look,
                    l(Icon::StatusResourceOverallocated),
                    if over == 0 { "Geen" } else if over == 1 { "1 resource" } else { "resources" },
                    self.overallocation_indicator && over > 0,
                    on_project(Msg::ToggleOverallocation),
                )]),
            ],
            TAB_VIEW => vec![
                w::ribbon_group(look, "Tijdschaal", vec![
                    zoom_stack(),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::UiRefresh), "Herstellen", false, (self.zoom != Zoom::Week).then_some(Msg::Zoom(Zoom::Week))),
                        w::ribbon_small(look, s(Icon::ViewFit), "Passend maken op project", self.zoom == Zoom::Month, Some(Msg::Zoom(Zoom::Month))),
                    ]),
                    column![
                        container(w::select(look, &Zoom::ALL, Some(self.zoom), Msg::Zoom, D::Compact)).width(110),
                        w::secondary(look, format!("Zoom: {} px/dag", self.zoom.px() as u32)),
                    ]
                    .spacing(6)
                    .into(),
                ]),
                w::ribbon_group(look, "Overzicht", vec![stack(vec![
                    w::ribbon_small(look, s(Icon::TreeCollapseScope), "Inklappen", false, on_project(Msg::CollapseAll(true))),
                    w::ribbon_small(look, s(Icon::TreeExpandScope), "Uitklappen", false, on_project(Msg::CollapseAll(false))),
                ])]),
                w::ribbon_group(look, "Layout", vec![
                    w::ribbon_large(look, l(Icon::LayoutResources), "Resourcediagram", self.show_histogram, on_project(Msg::ToggleHistogram)),
                    w::ribbon_large(look, l(Icon::LayoutManage), "Nieuwe layout", false, None),
                ]),
                w::ribbon_group(look, "Presentatie", vec![stack(vec![
                    w::ribbon_small(look, s(Icon::ViewFullscreen), "Presentatie", false, None),
                    w::ribbon_small(look, s(Icon::ViewGanttSplit), "Split view", false, None),
                    w::ribbon_small(look, s(Icon::ViewMinimap), "Mini-map", false, None),
                ])]),
                w::ribbon_group(look, "Panelen", vec![
                    w::ribbon_large(look, l(Icon::PanelRight), "Eigensch.", self.show_right, Some(Msg::ToggleRight)),
                    w::ribbon_large(look, l(Icon::ResourceWorkspace), "Resources", ws(Workspace::Resources), on_project(Msg::ShowWorkspace(Workspace::Resources))),
                    w::ribbon_large(look, l(Icon::DataChart), "Histogram", self.show_histogram, on_project(Msg::ToggleHistogram)),
                    w::ribbon_large(look, l(Icon::PanelWarnings), "Waarschuwingen", self.banner.is_some(), on_project(Msg::ToggleOverallocation)),
                ]),
                w::ribbon_group(look, "Baselines & voortgang", vec![
                    stack(vec![
                        w::ribbon_small(look, s(Icon::PlanningBaselineOverlay), "Baseline-overlay", self.show_baseline, Some(Msg::ToggleBaseline)),
                        w::ribbon_small(look, s(Icon::PlanningProgressLine), "Voortgangslijn", self.show_progress_line, Some(Msg::ToggleProgressLine)),
                        w::ribbon_small(look, s(Icon::PlanningStatusDateLine), "Statusdatumlijn", self.show_status_line, Some(Msg::ToggleStatusLine)),
                    ]),
                    stack(vec![
                        w::ribbon_small(look, s(Icon::PlanningBarColors), "Kritiek pad", self.show_critical, Some(Msg::ToggleCritical)),
                        w::ribbon_small(look, s(Icon::PlanningResourceAccent), "Resource-accent", self.resource_colors, Some(Msg::ToggleResourceColors)),
                        w::ribbon_small(look, s(Icon::PlanningFloatBand), "Spelingsband", self.show_float, Some(Msg::ToggleFloatBand)),
                    ]),
                    stack(vec![w::ribbon_small(look, s(Icon::PlanningRelationsVisible), "Relatielijnen", self.show_relations, Some(Msg::ToggleRelations))]),
                ]),
            ],
            TAB_SETTINGS => vec![
                w::ribbon_group(look, "Project", vec![
                    w::ribbon_large(look, l(Icon::ProjectProperties), "Projectinstellingen", false, on_project(Msg::Dialog(Some(Dialog::ProjectInfo)))),
                    w::ribbon_large(look, l(Icon::UiSettings), "App-instellingen", false, Some(Msg::Dialog(Some(Dialog::Settings)))),
                ]),
                w::ribbon_group(look, "Kalender", vec![w::ribbon_large(look, l(Icon::CalendarManage), "Kalender", false, on_project(Msg::Dialog(Some(Dialog::Calendar))))]),
                w::ribbon_group(look, "Sneltoetsen", vec![stack(vec![w::ribbon_small(look, s(Icon::UiShortcuts), "Sneltoetsen", false, Some(Msg::Dialog(Some(Dialog::Shortcuts))))])]),
            ],
            TAB_TABLE => vec![
                file_group(),
                edit_group(),
                tasks_group(),
                schedule_group(),
                trace_group(),
                w::ribbon_group(look, "Kolommen", vec![w::ribbon_large(look, l(Icon::TableColumns), "Kolommen…", self.extra_columns, Some(Msg::ToggleExtraColumns))]),
                progress_group(),
            ],
            TAB_IFC => vec![w::ribbon_group(look, "IFC", vec![container(column![
                w::body(look, "IFC — Industry Foundation Classes, in het schema van het project"),
                w::secondary(look, "Standaard IFC 4.3 ADD2. Het projectbestand is schemageldige IFC; andere formaten zijn adapters."),
            ]
            .spacing(4))
            .padding([8, 4])
            .into()])],
            _ => vec![
                w::ribbon_group(look, "Rapportage", vec![
                    w::ribbon_large(look, l(Icon::ReportPrintEntry), "Afdruk", ws(Workspace::Report), on_project(Msg::ShowWorkspace(Workspace::Report))),
                    w::ribbon_large(look, l(Icon::FilePrint), "Afdrukken", false, on_project(Msg::Dialog(Some(Dialog::Print)))),
                ]),
                progress_group(),
            ],
        };
        w::ribbon(look, groups)
    }

    fn tree_panel(&self, look: Look) -> Element<'_, Msg> {
        let mut tree = column![];
        if let Some(p) = self.project() {
            for i in p.visible() {
                let task = &p.tasks[i];
                let summary = p.is_summary(i);
                let open = !p.collapsed.contains(&task.id);
                let arrow = summary.then_some(if open { s(Icon::TreeCollapse) } else { s(Icon::TreeExpand) });
                let icon = if task.level == 0 {
                    s(Icon::ProjectFolder)
                } else if summary {
                    s(Icon::PlanningGantt)
                } else if task.milestone() {
                    s(Icon::TaskMilestoneMenu)
                } else {
                    s(Icon::TaskAdd)
                };
                tree = tree.push(w::tree_row(
                    look,
                    u16::from(task.level),
                    arrow,
                    summary.then_some(Msg::ToggleCollapse(task.id)),
                    Some(icon),
                    &task.name,
                    p.selected == Some(task.id),
                    Some(Msg::Select(Some(task.id))),
                    Some(Msg::Menu(Some(MenuKind::Task(task.id)))),
                ));
            }
        } else {
            tree = tree.push(container(w::secondary(look, "Geen project geopend")).padding(12));
        }
        w::panel(
            look,
            "Structuur",
            self.left_width,
            vec![
                w::with_tooltip(look, w::icon_button(look, s(Icon::ViewSearch), 20.0, false, Some(Msg::Noop)), "Zoeken", Some("Ctrl+F")),
                w::with_tooltip(look, w::icon_button(look, s(Icon::PanelLeft), 20.0, true, Some(Msg::ToggleLeft)), "Paneel verbergen", Some("Ctrl+1")),
            ],
            scrollable(tree).height(Length::Fill).into(),
        )
    }

    /// The properties panel of the app: Taak, Tijd, CPM-resultaat,
    /// Afhankelijkheden and Toewijzingen.
    fn properties_panel(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let section = |title: &str| w::section_header(look, s(Icon::TreeCollapse), title);
        let content: Element<'_, Msg> = match self.project().and_then(|p| p.selected.and_then(|id| p.index(id)).map(|i| (p, i))) {
            Some((p, i)) => {
                let task = &p.tasks[i];
                let summary = p.is_summary(i);
                let (start, end) = p.span(i);
                let wbs = p.wbs();
                let floats = p.floats();
                let mut rows = column![
                    row![
                        container(w::mono_label(look, "Taak")).width(Length::Fill),
                        w::with_tooltip(look, w::icon_button(look, s(Icon::EditDelete), 20.0, false, (task.level > 0).then_some(Msg::Delete)), "Verwijder taak", Some("Del")),
                    ]
                    .padding([0, 8])
                    .align_y(Alignment::Center),
                    w::property_row(look, "Naam", w::text_field(look, "Naam", &task.name, Some(Msg::EditName), D::Compact, None)),
                    w::property_row(look, "WBS Code", w::number(look, if wbs[i].is_empty() { "–".to_string() } else { wbs[i].clone() }).into()),
                    w::property_row(look, "Werksoort", w::select(look, &CATEGORIES, Some(CATEGORIES[task.category.min(CATEGORIES.len() - 1)]), Msg::EditCategory, D::Compact)),
                    w::property_row(look, "Kalender", w::body(look, "Projectkalender").into()),
                ];
                if summary {
                    rows = rows
                        .push(section("Tijd"))
                        .push(w::property_row(look, "Start", w::number(look, dmy(start, p.weekend_work)).into()))
                        .push(w::property_row(look, "Einde", w::number(look, dmy(end, p.weekend_work)).into()))
                        .push(w::property_row(look, "Duur (dagen)", w::number(look, format!("{}", end - start)).into()))
                        .push(w::property_row(look, "Voortgang (%)", w::number(look, format!("{}%", p.progress_of(i))).into()))
                        .push(container(w::secondary(look, "Een samenvattingstaak volgt uit de taken eronder.")).padding([4, 8]));
                } else {
                    let fixed = task.predecessors.is_empty();
                    rows = rows.push(container(w::checkbox(look, "Mijlpaal", task.milestone(), Some(Msg::SetMilestone))).padding([4, 8]));
                    rows = rows.push(section("Tijd"));
                    let shift: Element<'_, Msg> = row![
                        w::number(look, dmy(task.start, p.weekend_work)),
                        w::button(look, "−", K::Quiet, D::Compact, None, (fixed && task.start > 0).then_some(Msg::ShiftStart(-1))),
                        w::button(look, "+", K::Quiet, D::Compact, None, fixed.then_some(Msg::ShiftStart(1))),
                    ]
                    .spacing(2)
                    .align_y(Alignment::Center)
                    .into();
                    rows = rows.push(w::property_row(look, "Start", shift));
                    if !fixed {
                        rows = rows.push(container(w::secondary(look, "Geplande ankerdatum — de berekende start volgt uit de planninglogica.")).padding([0, 8]));
                    }
                    rows = rows
                        .push(w::property_row(look, "Duur (dagen)", w::text_field(look, "0", &self.duration_text, Some(Msg::EditDuration), D::Compact, self.duration_text.trim().parse::<u32>().is_err().then_some("Geen getal"))))
                        .push(w::property_row(look, "Constraint", w::select(look, &CONSTRAINTS, Some(CONSTRAINTS[0]), |_| Msg::Noop, D::Compact)))
                        .push(w::property_row(look, "Deadline", w::text_field(look, "dd-mm-jjjj", "", Some(|_| Msg::Noop), D::Compact, None)))
                        .push(w::property_row(look, "Voortgang (%)", w::slider(look, 0.0..=100.0, f32::from(task.progress), Msg::EditProgress, format!("{}%", task.progress))));
                    let float = floats.get(&task.id).copied().unwrap_or(0);
                    rows = rows
                        .push(section("CPM Resultaat"))
                        .push(w::property_row(look, "Vroegste start", w::number(look, dmy(task.start, p.weekend_work)).into()))
                        .push(w::property_row(look, "Vroegste einde", w::number(look, dmy(task.end(), p.weekend_work)).into()))
                        .push(w::property_row(look, "Totale speling", w::number(look, format!("{float}d")).into()))
                        .push(w::property_row(look, "Kritiek pad", t::status_label(look, if float <= 0 { Tone::Error } else { Tone::Success }, if float <= 0 { "Ja" } else { "Nee" })));
                    rows = rows.push(section("Afhankelijkheden"));
                    if task.predecessors.is_empty() {
                        rows = rows.push(container(w::secondary(look, "Geen voorgangers.")).padding([2, 8]));
                    }
                    for pred in &task.predecessors {
                        if let Some(pt) = p.task(pred.id) {
                            let code = p.index(pred.id).map(|j| wbs[j].clone()).unwrap_or_default();
                            let lag = if pred.lag == 0 { String::new() } else { format!(" {:+}d", pred.lag) };
                            rows = rows.push(
                                row![
                                    column![w::body(look, format!("{code} {}", pt.name)), text(format!("{}{lag}", pred.kind.code())).size(font::SIZE_LABEL).font(fonts::MONO).color(c.text_secondary)].spacing(1).width(Length::Fill),
                                    w::with_tooltip(look, w::icon_button(look, s(Icon::WindowClose), 20.0, false, Some(Msg::RemovePredecessor(pred.id))), "Relatie verwijderen", None),
                                ]
                                .padding([2, 8])
                                .align_y(Alignment::Center),
                            );
                        }
                    }
                    rows = rows.push(container(w::button(look, "Relatie toevoegen", K::Secondary, D::Compact, Some(s(Icon::PlanningDependencyAdd)), Some(Msg::Dialog(Some(Dialog::Relation))))).padding([6, 8]));
                    rows = rows.push(section("Toewijzingen"));
                    if task.milestone() {
                        rows = rows.push(container(w::secondary(look, "Toewijzingen zijn niet mogelijk op mijlpalen.")).padding([2, 8]));
                    } else {
                        let mut options: Vec<String> = vec!["Niet toegekend".to_string()];
                        options.extend(p.resources.iter().cloned());
                        let current = task.resource.and_then(|r| p.resources.get(r)).cloned().unwrap_or_else(|| "Niet toegekend".to_string());
                        rows = rows.push(w::property_row(look, "Resource", w::select(look, Box::leak(options.into_boxed_slice()), Some(current), Msg::EditResource, D::Compact)));
                        rows = rows.push(w::property_row(look, "Werk (u)", w::number(look, format!("{}", task.duration * 8)).into()));
                    }
                }
                rows = rows.push(container(w::button(look, "Bereken", K::Primary, D::Compact, Some(s(Icon::PlanningCalculate)), Some(Msg::Schedule))).padding([10, 8]));
                scrollable(rows).height(Length::Fill).into()
            }
            None => container(w::secondary(look, "Selecteer een taak om eigenschappen te bekijken.")).padding(12).into(),
        };
        w::panel(
            look,
            "Eigenschappen",
            self.right_width,
            vec![
                w::with_tooltip(look, w::icon_button(look, s(Icon::UiHelp), 20.0, false, None), "Help", None),
                w::with_tooltip(look, w::icon_button(look, s(Icon::PanelRight), 20.0, true, Some(Msg::ToggleRight)), "Paneel verbergen", Some("Ctrl+2")),
            ],
            content,
        )
    }

    fn document_tabs(&self, look: Look) -> Element<'_, Msg> {
        let tabs: Vec<DocumentTab<'_>> = self.projects.iter().map(|p| DocumentTab::new(&p.name, p.dirty)).collect();
        let strip = w::document_tabs(look, &tabs, self.active, s(Icon::WindowClose), Msg::SelectDoc, Msg::CloseDoc, |i| Msg::Menu(Some(MenuKind::Tab(i))));
        let c = look.color;
        let add = container(w::with_tooltip(look, w::icon_button(look, s(Icon::DocumentsNewOrOpen), 24.0, false, Some(Msg::Backstage(true))), "Project starten", None))
            .height(Length::Fill)
            .align_y(Vertical::Center)
            .padding([0, 4])
            .style(move |_| container::Style { background: Some(Background::Color(c.docbar)), ..Default::default() });
        row![strip, add].height(30).into()
    }

    fn workspace_view(&self, look: Look) -> Element<'_, Msg> {
        let Some(p) = self.project() else {
            return w::empty_state(
                look,
                l(Icon::PlanningGantt),
                "Geen project geopend",
                "Start een nieuwe planning of open een voorbeeldproject.",
                Some(row![w::button(look, "Nieuw project", K::Primary, D::Regular, None, Some(Msg::New)), w::button(look, "Bestaand project openen", K::Secondary, D::Regular, None, Some(Msg::Backstage(true)))].spacing(8).into()),
            );
        };
        let mut content = column![].spacing(12);
        if let Some((tone, message)) = &self.banner {
            content = content.push(w::banner(look, *tone, tone_icon(*tone), message, s(Icon::WindowClose), Some(Msg::CloseBanner)));
        }
        let body: Element<'_, Msg> = match self.workspace {
            Workspace::Gantt => self.gantt(look, p),
            Workspace::Table => self.table(look, p),
            Workspace::Resources => self.resources_doc(look, p),
            Workspace::Report => self.report(look, p),
        };
        content = content.push(body);
        if self.show_histogram && self.workspace != Workspace::Report {
            content = content.push(self.histogram_dock(look, p));
        }
        page(look, content.into())
    }

    /// The Gantt chart: the task grid (WBS, Taaknaam, Duur) on the left and the
    /// time scale on the right, both with 28 px rows, so they stay aligned.
    fn gantt<'a>(&'a self, look: Look, p: &'a Project) -> Element<'a, Msg> {
        let c = look.color;
        let px = self.zoom.px();
        let weeks = p.weeks();
        let total = weeks as f32 * 5.0 * px;
        let week_cell = 5.0 * px;
        let wbs = p.wbs();
        let floats = p.floats();
        let critical: HashSet<u32> = floats.iter().filter(|(_, f)| **f <= 0).map(|(id, _)| *id).collect();
        let weekend = p.weekend_work;

        // Month row and week row of the time scale.
        let mut months = row![];
        let mut run: Option<(u32, i32, u32)> = None;
        for wk in 0..=weeks {
            let (_, m, y) = date_of(wk * 5, weekend);
            match run {
                Some((rm, ry, n)) if wk < weeks && rm == m && ry == y => run = Some((rm, ry, n + 1)),
                _ => {
                    if let Some((rm, ry, n)) = run {
                        let label = if n as f32 * week_cell >= 60.0 { format!("{} {ry}", MONTHS[(rm - 1) as usize]) } else { String::new() };
                        months = months.push(container(text(label).size(font::SIZE_LABEL).font(fonts::STRONG).color(c.text)).width(n as f32 * week_cell).height(ROW / 2.0 + 4.0).padding([0, 4]).align_y(Vertical::Center).clip(true));
                    }
                    run = Some((m, y, 1));
                }
            }
        }
        let mut week_row = row![];
        for wk in 0..weeks {
            let (d, m, y) = date_of(wk * 5, weekend);
            let label = if week_cell >= 90.0 { format!("W{} · {d:02}-{m:02}", iso_week(y, m, d)) } else { format!("W{}", iso_week(y, m, d)) };
            week_row = week_row.push(
                container(text(label).size(font::SIZE_LABEL).font(fonts::MONO).color(c.text_secondary))
                    .width(week_cell)
                    .height(ROW / 2.0 - 4.0)
                    .padding([0, 4])
                    .align_y(Vertical::Center)
                    .clip(true)
                    .style(move |_| container::Style { border: iced::Border { color: c.border, width: 1.0, radius: 0.0.into() }, ..Default::default() }),
            );
        }
        let mut header_layers: Vec<Element<'_, Msg>> = vec![column![months, week_row].width(total).height(ROW).into()];
        if let Some(d) = p.status_date.filter(|_| self.show_status_line) {
            let chip = container(text(dmy(d, weekend)).size(font::SIZE_LABEL).font(fonts::MONO).color(c.text_on_accent))
                .padding([2, 6])
                .style(move |_| container::Style { background: Some(Background::Color(c.warning)), border: iced::Border { radius: 3.0.into(), ..Default::default() }, ..Default::default() });
            header_layers.push(container(row![Space::new().width((d as f32 * px - 36.0).max(0.0)), chip]).height(ROW).align_y(Vertical::Bottom).into());
        }
        let grid_header = row![
            container(w::mono_label(look, "WBS")).width(44),
            container(w::mono_label(look, "Taaknaam")).width(Length::Fill),
            container(w::mono_label(look, "Duur").width(Length::Fill).align_x(Horizontal::Right)).width(40),
        ]
        .spacing(8)
        .padding([0, 8])
        .align_y(Alignment::Center);

        let mut grid = column![container(grid_header).height(ROW).align_y(Vertical::Center), hbar(c.border_strong)];
        let mut chart = column![Stack::with_children(header_layers).width(total).height(ROW), hbar(c.border_strong)];
        for i in p.visible() {
            let task = &p.tasks[i];
            let summary = p.is_summary(i);
            let milestone = task.milestone() && !summary;
            let (start, end) = p.span(i);
            let on = p.selected == Some(task.id);
            let is_critical = self.show_critical && critical.contains(&task.id);
            let bold = summary || task.level == 0;
            let name_color = if milestone { c.accent_text } else { c.text };
            // Grid row.
            let indent = 4.0 + 14.0 * f32::from(task.level);
            let name = text(&task.name).size(font::SIZE_BODY).font(if bold { fonts::STRONG } else { fonts::BODY }).color(name_color);
            let arrow: Element<'_, Msg> = if summary {
                w::icon_button(look, if p.collapsed.contains(&task.id) { s(Icon::TreeExpand) } else { s(Icon::TreeCollapse) }, 16.0, false, Some(Msg::ToggleCollapse(task.id)))
            } else {
                Space::new().width(16).into()
            };
            let line = row![
                container(text(wbs[i].clone()).size(font::SIZE_BODY).font(fonts::MONO).color(c.text_secondary)).width(44),
                container(row![Space::new().width(indent), arrow, name].spacing(2).align_y(Alignment::Center)).width(Length::Fill).clip(true),
                container(w::number(look, if milestone { "0d".to_string() } else { format!("{}d", end - start) })).width(40),
            ]
            .spacing(8)
            .padding([0, 8])
            .align_y(Alignment::Center);
            grid = grid.push(selectable_row(look, line.into(), on, Msg::Select(Some(task.id)), Msg::Menu(Some(MenuKind::Task(task.id)))));
            grid = grid.push(w::divider(look));

            // Chart row.
            let x = start as f32 * px;
            let width = ((end - start) as f32 * px).max(2.0);
            let progress = f32::from(p.progress_of(i)) / 100.0;
            let label = |t: &'a str| text(t).size(font::SIZE_LABEL).font(fonts::MEDIUM).color(c.text_secondary);
            let bar: Element<'_, Msg> = if milestone {
                let fill = if is_critical { c.error } else { c.accent_text };
                row![Space::new().width((x - 7.0).max(0.0)), text("◆").size(14).color(fill), Space::new().width(6), label(&task.name)].align_y(Alignment::Center).into()
            } else if summary {
                row![Space::new().width(x), block(c.text, width, 6.0, 1.0), Space::new().width(6), label(&task.name)].align_y(Alignment::Center).into()
            } else {
                let fill = if is_critical {
                    c.error
                } else if self.resource_colors {
                    task.resource.map_or(c.accent, |r| RESOURCE_COLORS[r % RESOURCE_COLORS.len()])
                } else {
                    c.accent
                };
                let back = mix(fill, 0.4, c.panel);
                let done = (width * progress).round();
                let layers: Vec<Element<'_, Msg>> = vec![block(back, width, 14.0, 3.0), block(fill, done.max(if progress > 0.0 { 3.0 } else { 0.0 }), 14.0, 3.0)];
                let mut parts: Vec<Element<'_, Msg>> = vec![Stack::with_children(layers).width(width).height(14).into()];
                if self.show_baseline {
                    if let Some((b_start, b_dur)) = p.baseline.as_ref().and_then(|b| b.get(&task.id)) {
                        let dx = (*b_start as f32 - start as f32) * px;
                        parts.push(row![Space::new().width(dx.max(-x)), block(c.text_secondary, (*b_dur as f32 * px).max(2.0), 4.0, 2.0)].into());
                    }
                }
                let mut line = row![Space::new().width(x), column(parts).spacing(2)].align_y(Alignment::Center);
                let float = floats.get(&task.id).copied().unwrap_or(0);
                if self.show_float && float > 0 {
                    line = line.push(block(c.success, float as f32 * px, 4.0, 2.0));
                }
                line = line.push(Space::new().width(6)).push(label(&task.name));
                if self.zoom == Zoom::Day {
                    if let Some(r) = task.resource {
                        line = line.push(Space::new().width(6)).push(text(&p.resources[r]).size(font::SIZE_LABEL).color(c.text_secondary));
                    }
                }
                line.into()
            };
            let mut layers: Vec<Element<'_, Msg>> = vec![container(bar).width(total).height(ROW).align_y(Vertical::Center).into()];
            if self.show_status_line {
                if let Some(d) = p.status_date {
                    layers.push(vline(c.warning, d as f32 * px, ROW));
                }
            }
            if self.show_progress_line && !summary && !milestone {
                if let Some(d) = p.status_date {
                    if task.start <= d {
                        layers.push(vline(c.warning, (x + width * f32::from(task.progress) / 100.0).round(), ROW));
                    }
                }
            }
            let chart_row: Element<'_, Msg> = container(Stack::with_children(layers).width(total).height(ROW))
                .style(move |_| container::Style { background: if on && !look.high_contrast() { Some(Background::Color(c.selected)) } else { None }, ..Default::default() })
                .into();
            chart = chart.push(mouse_area(chart_row).on_press(Msg::Select(Some(task.id))).on_right_press(Msg::Menu(Some(MenuKind::Task(task.id)))));
            chart = chart.push(w::divider(look));
        }
        if p.tasks.len() <= 1 {
            grid = grid.push(container(w::secondary(look, "Nog geen taken. Voeg er een toe met Ctrl+N.")).padding(12));
        }
        let sheet = row![
            container(grid).width(GRID_WIDTH),
            vbar(c.border_strong),
            scrollable(container(chart).width(total).padding(iced::Padding { bottom: 12.0, ..iced::Padding::ZERO }))
                .direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new()))
                .width(Length::Fill),
        ];
        let legend = row![
            legend_item(look, c.accent, "Taak"),
            legend_item(look, mix(c.accent, 0.4, c.panel), "Resterend"),
            legend_item(look, c.error, "Kritiek pad"),
            legend_item(look, c.text, "Samenvatting"),
            legend_item(look, c.warning, "Statusdatum"),
            legend_item(look, c.success, "Speling"),
            Space::new().width(Length::Fill),
            w::secondary(look, "Relatielijnen worden in deze testversie niet getekend"),
        ]
        .spacing(16)
        .padding([8, 12])
        .align_y(Alignment::Center);
        card(look, column![sheet, w::divider(look), legend].into())
    }

    /// The resource histogram under the Gantt: a resource list on the left and
    /// the load per week on the right (as the app's bottom dock).
    fn histogram_dock<'a>(&'a self, look: Look, p: &'a Project) -> Element<'a, Msg> {
        let c = look.color;
        let current = if self.hist_resource == 0 { None } else { Some(self.hist_resource - 1) };
        let usage = p.histogram(current);
        let max = usage.iter().copied().max().unwrap_or(0).max(CAPACITY_PER_WEEK);
        let scale = 96.0 / max as f32;
        let mut list = column![w::tree_row(look, 0, None, None, Some(s(Icon::ResourceWorkspace)), "Alle resources", current.is_none(), Some(Msg::HistResource(0)), None)];
        for (r, name) in p.resources.iter().enumerate() {
            list = list.push(w::tree_row(look, 1, None, None, None, name, current == Some(r), Some(Msg::HistResource(r + 1)), None));
        }
        let mut bars = row![].spacing(3).align_y(Alignment::End);
        for (wk, used) in usage.iter().enumerate() {
            let over = *used > CAPACITY_PER_WEEK && current.is_some();
            let fill = if over { c.error } else { c.accent };
            let height = (*used as f32 * scale).max(if *used > 0 { 2.0 } else { 0.0 });
            let (d, m, y) = date_of(wk as u32 * 5, p.weekend_work);
            bars = bars.push(column![container(block(fill, 18.0, height, 2.0)).height(96).align_y(Vertical::Bottom), text(format!("W{}", iso_week(y, m, d))).size(9).font(fonts::MONO).color(c.text_secondary)].spacing(3).align_x(Alignment::Center));
        }
        let title = current.map_or("Alle resources", |r| p.resources[r].as_str());
        let head = row![
            w::mono_label(look, title),
            w::secondary(look, format!("taakdagen per week · capaciteit {CAPACITY_PER_WEEK}")),
            Space::new().width(Length::Fill),
            w::with_tooltip(look, w::icon_button(look, s(Icon::ResourcePrevious), 20.0, false, Some(Msg::HistStep(-1))), "Vorige", None),
            w::with_tooltip(look, w::icon_button(look, s(Icon::ResourceNext), 20.0, false, Some(Msg::HistStep(1))), "Volgende", None),
            w::with_tooltip(look, w::icon_button(look, s(Icon::WindowClose), 20.0, false, Some(Msg::ToggleHistogram)), "Histogram sluiten", None),
        ]
        .spacing(8)
        .align_y(Alignment::Center);
        let chart = column![head, scrollable(container(bars).padding([0, 4])).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new()))].spacing(8);
        card(look, row![container(scrollable(list).height(150)).width(200), vbar(c.border_strong), container(chart).padding(10).width(Length::Fill)].into())
    }

    fn table<'a>(&'a self, look: Look, p: &'a Project) -> Element<'a, Msg> {
        let wbs = p.wbs();
        let floats = p.floats();
        let visible = p.visible();
        let ids: Vec<u32> = visible.iter().map(|i| p.tasks[*i].id).collect();
        let mut columns = vec![
            TableColumn { title: "WBS", width: Length::Fixed(56.0), numeric: false },
            TableColumn { title: "Taaknaam", width: Length::Fill, numeric: false },
            TableColumn { title: "Duur", width: Length::Fixed(50.0), numeric: true },
            TableColumn { title: "Start", width: Length::Fixed(84.0), numeric: true },
            TableColumn { title: "Einde", width: Length::Fixed(84.0), numeric: true },
            TableColumn { title: "Kritiek", width: Length::Fixed(56.0), numeric: false },
            TableColumn { title: "Tot. speling", width: Length::Fixed(80.0), numeric: true },
            TableColumn { title: "Voortg.", width: Length::Fixed(60.0), numeric: true },
        ];
        if self.extra_columns {
            columns.push(TableColumn { title: "Werksoort", width: Length::Fixed(90.0), numeric: false });
            columns.push(TableColumn { title: "Resource", width: Length::Fixed(120.0), numeric: false });
            columns.push(TableColumn { title: "Voorgangers", width: Length::Fixed(120.0), numeric: false });
        }
        let rows: Vec<Vec<String>> = visible
            .iter()
            .map(|&i| {
                let t = &p.tasks[i];
                let summary = p.is_summary(i);
                let (start, end) = p.span(i);
                let indent = "   ".repeat(usize::from(t.level.saturating_sub(1)));
                let float = floats.get(&t.id).copied();
                let mut cells = vec![
                    wbs[i].clone(),
                    format!("{indent}{}", t.name),
                    format!("{}d", end - start),
                    dmy(start, p.weekend_work),
                    dmy(end, p.weekend_work),
                    if summary { String::new() } else if float.is_some_and(|f| f <= 0) { "Ja".into() } else { "Nee".into() },
                    float.map_or(String::new(), |f| format!("{f}d")),
                    format!("{}%", p.progress_of(i)),
                ];
                if self.extra_columns {
                    cells.push(CATEGORIES[t.category.min(CATEGORIES.len() - 1)].to_string());
                    cells.push(t.resource.and_then(|r| p.resources.get(r)).cloned().unwrap_or_default());
                    cells.push(t.predecessors.iter().filter_map(|x| p.index(x.id).map(|j| format!("{}{}", wbs[j], if x.kind == RelKind::FS && x.lag == 0 { String::new() } else { format!("{}{:+}", x.kind.code(), x.lag) }))).collect::<Vec<_>>().join(", "));
                }
                cells
            })
            .collect();
        let selected = p.selected.and_then(|s| ids.iter().position(|id| *id == s));
        let menu_ids = ids.clone();
        let table = w::table(look, &columns, rows, selected, Some(move |i: usize| Msg::Select(Some(ids[i]))), Some(move |i: usize| Msg::Menu(Some(MenuKind::Task(menu_ids[i])))));
        let actions = row![
            w::button(look, "Taak", K::Secondary, D::Regular, Some(s(Icon::TaskAdd)), Some(Msg::AddTask)),
            w::button(look, "Mijlpaal", K::Secondary, D::Regular, Some(s(Icon::TaskMilestoneMenu)), Some(Msg::AddMilestone)),
            w::button(look, "Verwijder", K::Danger, D::Regular, Some(s(Icon::EditDelete)), p.selected.map(|_| Msg::Delete)),
        ]
        .spacing(8);
        column![card(look, table), actions].spacing(12).into()
    }

    fn resources_doc<'a>(&'a self, look: Look, p: &'a Project) -> Element<'a, Msg> {
        let over: HashMap<usize, u32> = p.overallocations().into_iter().collect();
        let columns = [
            TableColumn { title: "Resource", width: Length::Fill, numeric: false },
            TableColumn { title: "Taken", width: Length::Fixed(64.0), numeric: true },
            TableColumn { title: "Dagen", width: Length::Fixed(64.0), numeric: true },
            TableColumn { title: "Werk (u)", width: Length::Fixed(72.0), numeric: true },
            TableColumn { title: "Bezetting", width: Length::Fixed(170.0), numeric: false },
        ];
        let rows: Vec<Vec<String>> = p
            .resources
            .iter()
            .enumerate()
            .map(|(r, name)| {
                let tasks: Vec<&PlanTask> = p.leaves().filter(|(_, t)| t.resource == Some(r)).map(|(_, t)| t).collect();
                let days: u32 = tasks.iter().map(|t| t.duration).sum();
                let status = match over.get(&r) {
                    Some(d) => format!("Overbezet op {d} dag(en)"),
                    None if tasks.is_empty() => "Niet ingezet".to_string(),
                    None => "In balans".to_string(),
                };
                vec![name.clone(), tasks.len().to_string(), days.to_string(), (days * 8).to_string(), status]
            })
            .collect();
        let selected = if self.hist_resource == 0 { None } else { Some(self.hist_resource - 1) };
        let table = w::table(look, &columns, rows, selected, Some(|i: usize| Msg::HistResource(i + 1)), None::<fn(usize) -> Msg>);
        let actions = row![
            w::button(look, "Nieuwe resource", K::Secondary, D::Regular, Some(s(Icon::ResourceNew)), Some(Msg::Dialog(Some(Dialog::NewResource)))),
            w::button(look, "Histogram", K::Secondary, D::Regular, Some(s(Icon::DataChart)), Some(Msg::ToggleHistogram)),
            w::button(look, "Nivelleren…", K::Primary, D::Regular, Some(s(Icon::ResourceLevel)), (!over.is_empty()).then_some(Msg::Level)),
            Space::new().width(Length::Fill),
            w::button(look, "Terug naar Gantt", K::Quiet, D::Regular, Some(s(Icon::PlanningGantt)), Some(Msg::ShowWorkspace(Workspace::Gantt))),
        ]
        .spacing(8)
        .align_y(Alignment::Center);
        column![card(look, table), actions].spacing(12).into()
    }

    /// The report (Rapport tab): project figures, the phases and the milestones.
    fn report<'a>(&'a self, look: Look, p: &'a Project) -> Element<'a, Msg> {
        let c = look.color;
        let critical = p.critical();
        let leaves = p.leaves().filter(|(_, t)| t.level > 0).count();
        let figures = row![
            t::figure_tile(look, format!("{} wd", p.project_end()), "Doorlooptijd", true),
            t::figure_tile(look, leaves.to_string(), "Taken", false),
            t::figure_tile(look, critical.len().to_string(), "Kritieke taken", false),
            t::figure_tile(look, format!("{}%", p.progress_of(0)), "Voortgang", false),
        ]
        .spacing(12);
        let mut lines = column![
            text(format!("Planning {}", p.name)).size(font::SIZE_PAGE_HEADING).font(fonts::HEADING).color(c.text),
            w::secondary(look, format!("Start {} · einde {} · statusdatum {}", dmy(0, p.weekend_work), dmy(p.project_end(), p.weekend_work), p.status_date.map_or("geen".to_string(), |d| dmy(d, p.weekend_work)))),
            figures,
            w::divider(look),
            w::mono_label(look, "Fasen"),
        ]
        .spacing(12);
        let wbs = p.wbs();
        for (i, t) in p.tasks.iter().enumerate() {
            if t.level != 1 {
                continue;
            }
            let (start, end) = p.span(i);
            lines = lines.push(
                row![
                    w::number(look, wbs[i].clone()).width(32).align_x(Horizontal::Left),
                    w::body(look, &t.name).width(Length::Fill),
                    w::number(look, dmy(start, p.weekend_work)).width(90),
                    w::number(look, dmy(end, p.weekend_work)).width(90),
                    w::number(look, format!("{}%", p.progress_of(i))).width(60),
                ]
                .spacing(8),
            );
        }
        lines = lines.push(w::divider(look)).push(w::mono_label(look, "Mijlpalen"));
        for (i, t) in p.tasks.iter().enumerate() {
            if t.milestone() && t.level > 0 && !p.is_summary(i) {
                lines = lines.push(row![w::number(look, wbs[i].clone()).width(32).align_x(Horizontal::Left), w::body(look, format!("◆ {}", t.name)).width(Length::Fill), w::number(look, dmy(t.start, p.weekend_work)).width(90)].spacing(8));
            }
        }
        container(card(look, container(lines).padding(24).into())).max_width(760).into()
    }

    /// The Bestand screen of the app: Terug, Nieuw, Openen, Voorbeelden,
    /// Opslaan, Opslaan als, Exporteren, Afdruk, Projectinstellingen,
    /// App-instellingen, Help and Sluit project.
    fn backstage_view(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let has_project = self.project().is_some();
        let on_project = |m: Msg| has_project.then_some(m);
        let nav = column![
            t::file_nav_row(look, s(Icon::NavBack), "Terug", false, Some(Msg::Backstage(false))),
            w::divider(look),
            t::file_nav_row(look, s(Icon::FileNew), "Nieuw", self.file_page == FilePage::New, Some(Msg::FilePage(FilePage::New))),
            t::file_nav_row(look, s(Icon::FileOpen), "Openen", self.file_page == FilePage::Open, Some(Msg::FilePage(FilePage::Open))),
            t::file_nav_row(look, s(Icon::FileExamples), "Voorbeelden", self.file_page == FilePage::Examples, Some(Msg::FilePage(FilePage::Examples))),
            t::file_nav_row(look, s(Icon::FileSave), "Opslaan", false, on_project(Msg::Save)),
            t::file_nav_row(look, s(Icon::FileSaveAs), "Opslaan als", false, on_project(Msg::SaveAs)),
            t::file_nav_row(look, s(Icon::FileExport), "Exporteren", self.file_page == FilePage::Export, on_project(Msg::FilePage(FilePage::Export))),
            t::file_nav_row(look, s(Icon::FilePrint), "Afdruk", false, on_project(Msg::ShowWorkspace(Workspace::Report)).map(|_| Msg::Dialog(Some(Dialog::Print)))),
            w::divider(look),
            t::file_nav_row(look, s(Icon::ProjectProperties), "Projectinstellingen", self.file_page == FilePage::Info, on_project(Msg::FilePage(FilePage::Info))),
            t::file_nav_row(look, s(Icon::UiSettings), "App-instellingen", false, Some(Msg::Dialog(Some(Dialog::Settings)))),
            t::file_nav_row(look, s(Icon::UiHelp), "Help", false, None),
            w::divider(look),
            t::file_nav_row(look, s(Icon::NavHome), "Startscherm", false, Some(Msg::Restart)),
            t::file_nav_row(look, s(Icon::DocumentClose), "Sluit project", false, on_project(Msg::CloseActive)),
        ]
        .width(260);
        let content: Element<'_, Msg> = match self.file_page {
            FilePage::New => column![
                wf::page_heading(look, "Nieuw", Some("Begin met een lege planning of een voorbeeldproject.")),
                column![
                    t::task_tile(look, l(Icon::FileNew), "Nieuw project", "Alleen een projectregel; je voegt zelf taken toe.", Some(Msg::New)),
                    t::task_tile(look, l(Icon::FileExamples), "Voorbeeldproject", "Meegeleverde bouwplanning met alle functies.", Some(Msg::OpenExample(0))),
                    t::task_tile(look, l(Icon::FileImport), "MS Project of Primavera P6 openen", "Volgt in deze testversie nog niet.", None),
                ]
                .spacing(8)
                .max_width(620),
            ]
            .spacing(16)
            .into(),
            FilePage::Open => column![wf::page_heading(look, "Recente projecten", Some("Klik om te openen.")), self.project_grid(look), w::mono_label(look, "Recente bestanden"), self.recent_list(look)]
                .spacing(16)
                .max_width(860)
                .into(),
            FilePage::Examples => {
                let mut list = column![].spacing(8);
                for (i, (name, meta, file)) in EXAMPLES.iter().enumerate() {
                    list = list.push(t::task_tile(look, l(if i < 4 { Icon::PlanningGantt } else { Icon::FileTypeProject }), name, if i == 0 { meta } else { file }, Some(Msg::OpenExample(i))));
                }
                column![wf::page_heading(look, "Voorbeeldprojecten", Some("Meegeleverde bouwplanningen. Klik om te openen in een nieuw tabblad.")), list.max_width(620)].spacing(16).into()
            }
            FilePage::Export => column![
                wf::page_heading(look, "Exporteren", Some("Kies een formaat. Het project wordt geconverteerd en opgeslagen.")),
                column![
                    t::task_tile(look, l(Icon::FileTypeIfc), "IFC 4.3", "Het eigen formaat, schemageldig.", Some(Msg::Dialog(Some(Dialog::Export)))),
                    t::task_tile(look, l(Icon::FileExport), "MS Project XML", "Voor Microsoft Project.", Some(Msg::Dialog(Some(Dialog::Export)))),
                    t::task_tile(look, l(Icon::FileExport), "Primavera P6 XML", "Voor Primavera P6.", Some(Msg::Dialog(Some(Dialog::Export)))),
                    t::task_tile(look, l(Icon::FileExportOptions), "Voortgangsblad (CSV/XLSX)", "Lees een teruggestuurd blad later weer in.", Some(Msg::Dialog(Some(Dialog::Export)))),
                ]
                .spacing(8)
                .max_width(620),
            ]
            .spacing(16)
            .into(),
            FilePage::Info => column![
                wf::page_heading(look, "Projectinstellingen", Some("Gegevens en instellingen van dit project.")),
                t::info_card(look, "Project", self.info_rows()),
                t::info_card(look, "Rekenprofiel", vec![("Profiel", "Open Planner Studio".into()), ("Bijna-kritiek drempel", "2 dagen".into()), ("Voortgangsmodus", "Retained Logic".into())]),
            ]
            .spacing(16)
            .max_width(620)
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

    fn info_rows(&self) -> Vec<(&'static str, String)> {
        let Some(p) = self.project() else { return vec![("Project", "Geen project geopend".into())] };
        let leaves = p.leaves().filter(|(_, t)| t.level > 0).count();
        vec![
            ("Naam", p.name.clone()),
            ("Bestand", if p.file.is_empty() { "Nog niet opgeslagen".into() } else { p.file.clone() }),
            ("Formaat", "IFC 4.3 ADD2".into()),
            ("Start", dmy(0, p.weekend_work)),
            ("Einde", dmy(p.project_end(), p.weekend_work)),
            ("Taken", format!("{leaves} taken, {} mijlpalen", p.tasks.iter().filter(|t| t.milestone() && t.level > 0).count())),
            ("Resources", p.resources.len().to_string()),
            ("Kalender", if p.weekend_work { "Bouwkalender NL, 7 dagen".into() } else { "Bouwkalender NL, ma–vr 07:00–16:00".into() }),
        ]
    }

    fn title_bar(&self, look: Look, name: String, quick: bool) -> Element<'_, Msg> {
        let has_project = self.project().is_some();
        let p = self.project();
        let quick_buttons = if quick {
            vec![
                w::with_tooltip(look, ch::title_button(look, s(Icon::FileNew), false, Some(Msg::New)), "Nieuw", None),
                w::with_tooltip(look, ch::title_button(look, s(Icon::FileOpen), false, Some(Msg::Backstage(true))), "Openen", None),
                w::with_tooltip(look, ch::title_button(look, s(Icon::FileSave), false, has_project.then_some(Msg::Save)), "Opslaan", Some("Ctrl+S")),
                container(w::switch(look, "Automatisch opslaan", self.autosave, Some(Msg::AutoSave))).padding([0, 8]).into(),
                w::with_tooltip(look, ch::title_button(look, s(Icon::EditUndo), false, p.is_some_and(|p| !p.history.is_empty()).then_some(Msg::Undo)), "Ongedaan maken", Some("Ctrl+Z")),
                w::with_tooltip(look, ch::title_button(look, s(Icon::EditRedo), false, p.is_some_and(|p| !p.future.is_empty()).then_some(Msg::Redo)), "Opnieuw", Some("Ctrl+Y")),
            ]
        } else {
            vec![Space::new().width(86).into()]
        };
        let extra = vec![
            w::with_tooltip(look, ch::title_button(look, s(Icon::UiFeedback), false, Some(Msg::Feedback)), "Feedback geven", None),
            w::with_tooltip(look, ch::title_button(look, s(Icon::NavPageMenu), self.menu.is_some_and(|(k, _)| k == MenuKind::App), Some(Msg::Menu(Some(MenuKind::App)))), "Menu", None),
            w::with_tooltip(look, ch::title_button(look, s(Icon::UiSettings), self.dialog == Some(Dialog::Settings), Some(Msg::Dialog(Some(Dialog::Settings)))), "App-instellingen", Some("Ctrl+,")),
        ];
        let window = WindowActions { drag: Msg::TitlePress, minimize: Msg::Minimize, maximize: Msg::Maximize, close: Msg::CloseWindow, maximized: self.maximized };
        ch::title_bar(look, name, quick_buttons, extra, window, window_icons())
    }

    fn menu_items(&self, kind: MenuKind) -> Vec<MenuItem<'static, Msg>> {
        match kind {
            MenuKind::Task(id) => {
                let p = self.project();
                let i = p.and_then(|p| p.index(id));
                let summary = p.zip(i).is_some_and(|(p, i)| p.is_summary(i));
                let open = p.is_some_and(|p| !p.collapsed.contains(&id));
                let mut items = Vec::new();
                if summary {
                    items.push(MenuItem::action(Some(if open { s(Icon::TreeCollapse) } else { s(Icon::TreeExpand) }), if open { "Inklappen" } else { "Uitklappen" }, None, Some(Msg::ToggleCollapse(id))));
                    items.push(MenuItem::Separator);
                }
                items.extend([
                    MenuItem::action(Some(s(Icon::TaskAdd)), "Taak toevoegen", Some("Ctrl+N"), Some(Msg::AddTask)),
                    MenuItem::action(Some(s(Icon::TaskMilestoneMenu)), "Mijlpaal toevoegen", Some("Ctrl+M"), Some(Msg::AddMilestone)),
                    MenuItem::action(Some(s(Icon::PlanningDependencyAdd)), "Relatie toevoegen…", None, (!summary).then_some(Msg::Dialog(Some(Dialog::Relation)))),
                    MenuItem::Separator,
                    MenuItem::action(Some(s(Icon::TaskIndent)), "Inspringen", Some("Alt+→"), Some(Msg::Indent)),
                    MenuItem::action(Some(s(Icon::TaskOutdent)), "Uitspringen", Some("Alt+←"), Some(Msg::Outdent)),
                    MenuItem::action(Some(s(Icon::PlanningTracePredecessors)), "Voorgangers", None, Some(Msg::TracePredecessors)),
                    MenuItem::action(Some(s(Icon::PlanningTraceSuccessors)), "Opvolgers", None, Some(Msg::TraceSuccessors)),
                    MenuItem::Separator,
                    MenuItem::danger(Some(s(Icon::EditDelete)), "Verwijder", Some("Del"), Some(Msg::Delete)),
                ]);
                items
            }
            MenuKind::Tab(i) => vec![
                MenuItem::action(Some(s(Icon::DocumentClose)), "Sluit project", Some("Ctrl+W"), Some(Msg::CloseDoc(i))),
                MenuItem::action(None, "Andere projecten sluiten", None, (self.projects.len() > 1).then_some(Msg::CloseOthers(i))),
                MenuItem::action(None, "Alle projecten sluiten", None, Some(Msg::CloseAll)),
                MenuItem::Separator,
                MenuItem::action(Some(s(Icon::FileSave)), "Opslaan", Some("Ctrl+S"), Some(Msg::Save)),
            ],
            MenuKind::App => vec![
                MenuItem::Heading("Beeld"),
                MenuItem::check("Eigenschappen", Some("Ctrl+2"), self.show_right, Msg::ToggleRight),
                MenuItem::check("Structuur", Some("Ctrl+1"), self.show_left, Msg::ToggleLeft),
                MenuItem::check("Histogram", None, self.show_histogram, Msg::ToggleHistogram),
                MenuItem::check("Kritiek pad", None, self.show_critical, Msg::ToggleCritical),
                MenuItem::check("Resource-accent", None, self.resource_colors, Msg::ToggleResourceColors),
                MenuItem::Separator,
                MenuItem::action(Some(s(Icon::PlanningCalculate)), "Bereken", Some("F5"), Some(Msg::Schedule)),
                MenuItem::action(Some(s(Icon::UiSettings)), "App-instellingen", Some("Ctrl+,"), Some(Msg::Dialog(Some(Dialog::Settings)))),
                MenuItem::action(Some(s(Icon::UiShortcuts)), "Sneltoetsen", None, Some(Msg::Dialog(Some(Dialog::Shortcuts)))),
                MenuItem::action(Some(s(Icon::NavHome)), "Startscherm", None, Some(Msg::Restart)),
                MenuItem::Separator,
                MenuItem::action(Some(s(Icon::WindowClose)), "Afsluiten", Some("Alt+F4"), Some(Msg::CloseWindow)),
            ],
        }
    }

    /// A small Gantt in the workspace colours: the preview on a project card.
    fn mini_preview(look: Look, seed: usize) -> Element<'static, Msg> {
        let c = look.color;
        let bars: [(u16, u16); 4] = [[(0, 3), (2, 4), (5, 3), (7, 3)], [(0, 4), (3, 3), (5, 4), (8, 2)], [(1, 2), (2, 5), (6, 2), (7, 3)], [(0, 2), (1, 4), (4, 4), (7, 3)]][seed % 4];
        let mut sheet = column![].spacing(5).width(150);
        for (i, (offset, len)) in bars.into_iter().enumerate() {
            let color = if i == 0 { look.workspace_accent_text } else { Color { a: 0.45, ..c.workspace_text } };
            sheet = sheet.push(row![
                Space::new().width(Length::FillPortion(offset.max(1))),
                container(Space::new().width(Length::Fill).height(5)).width(Length::FillPortion(len)).style(move |_| container::Style {
                    background: Some(Background::Color(color)),
                    border: iced::Border { radius: 2.0.into(), ..Default::default() },
                    ..Default::default()
                }),
                Space::new().width(Length::FillPortion((10 - offset - len).max(1))),
            ]);
        }
        sheet.into()
    }

    fn project_grid(&self, look: Look) -> Element<'_, Msg> {
        let statuses = [Some((Tone::Warning, "1 resource overbezet")), Some((Tone::Info, "Showcase")), None, Some((Tone::Info, "Showcase"))];
        let mut grid = column![].spacing(12);
        for pair in [0usize, 2] {
            let mut line = row![].spacing(12);
            for (i, status) in statuses.iter().enumerate().skip(pair).take(2) {
                let (name, meta, _) = EXAMPLES[i];
                let preview = (i != 2).then(|| Self::mini_preview(look, i));
                line = line.push(container(t::project_card(look, preview, l(Icon::PlanningGantt), name, meta, *status, Some(Msg::OpenExample(i)))).width(Length::FillPortion(1)));
            }
            grid = grid.push(line);
        }
        grid.into()
    }

    fn recent_list(&self, look: Look) -> Element<'_, Msg> {
        let files = EXAMPLES.iter().take(4).enumerate().map(|(i, (_, _, file))| RecentFile { icon: s(Icon::FileTypeIfc), name: file, path: "examples", date: if i == 0 { "vandaag" } else { "12 okt" }, on_press: Some(Msg::OpenExample(i)) }).collect();
        t::recent_files(look, files)
    }

    fn start_screen(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let left = column![
            wf::page_heading(look, "Open Planner Studio", Some("Open-source bouwplanning: kritiek pad, MS Project- en P6-bestanden, IFC 4.3")),
            Space::new().height(4),
            w::mono_label(look, "Nieuw"),
            t::task_tile(look, l(Icon::FileNew), "Nieuw project", "Begin met alleen een projectregel.", Some(Msg::New)),
            t::task_tile(look, l(Icon::FileExamples), "Voorbeeldproject", "Grachtenpand Amsterdam: 44 taken, 7 fasen, resources.", Some(Msg::OpenExample(0))),
            t::task_tile(look, l(Icon::FileOpen), "Bestaand project openen", "IFC 4.3, MS Project (.mpp, .xml) of Primavera P6 (.xer, .xml).", Some(Msg::OpenExample(0))),
            Space::new().height(8),
            t::info_card(look, "Over", vec![("Versie", "UI 0.4 · testversie".into()), ("Thema", self.theme.name().into()), ("Iconen", format!("B2 revisie {}", openaec_icons::REVISION)), ("Licentie", "LGPL-3.0".into())]),
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

    fn dialog_card(&self, look: Look, dialog: Dialog) -> Element<'_, Msg> {
        let close = Some(Msg::Dialog(None));
        let close_icon = s(Icon::WindowClose);
        let cancel = || w::button(look, "Annuleren", K::Secondary, D::Regular, None, Some(Msg::Dialog(None)));
        let ok = || w::button(look, "Sluiten", K::Primary, D::Regular, None, Some(Msg::Dialog(None)));
        let p = self.project();
        match dialog {
            Dialog::Settings => {
                let hc = look.high_contrast();
                let workspace: Element<'_, Msg> = if hc { w::secondary(look, "Bepaald door High contrast").into() } else { w::select(look, &WorkspaceSetting::ALL, Some(self.workspace_setting), Msg::Workspace, D::Regular) };
                let statusbar: Element<'_, Msg> = if hc { w::secondary(look, "Bepaald door High contrast").into() } else { w::select(look, &StatusbarSetting::ALL, Some(self.statusbar), Msg::Statusbar, D::Regular) };
                let content = column![
                    w::mono_label(look, "Weergave"),
                    w::property_row(look, "Thema", w::select(look, &ThemeId::ALL, Some(self.theme), Msg::Theme, D::Regular)),
                    w::property_row(look, "Werkruimte", workspace),
                    container(w::secondary(look, "Kleur van het vlak waarin je planning staat.")).padding([0, 8]),
                    w::property_row(look, "Statusbalk", statusbar),
                    w::property_row(look, "Tijdschaal", w::select(look, &Zoom::ALL, Some(self.zoom), Msg::Zoom, D::Regular)),
                    w::property_row(look, "Taal", w::select(look, &["Nederlands", "English"], Some("Nederlands"), |_| Msg::Noop, D::Regular)),
                    Space::new().height(6),
                    w::mono_label(look, "Opstarten"),
                    container(w::checkbox(look, "Laatste project direct openen", self.skip_start, Some(Msg::SkipStart))).padding([4, 8]),
                    container(w::checkbox(look, "Automatisch opslaan", self.autosave, Some(Msg::AutoSave))).padding([4, 8]),
                    container(w::secondary(look, "Sla het startscherm over. Kies Startscherm in het menu om het te zien werken.")).padding([0, 8]),
                ]
                .spacing(6);
                w::dialog(look, "App-instellingen", close_icon, close, content.into(), None, vec![ok()], true)
            }
            Dialog::Export => {
                let mut formats = column![w::secondary(look, "Kies een formaat. Het project wordt geconverteerd en opgeslagen.")].spacing(10);
                for f in FORMATS {
                    formats = formats.push(w::radio(look, f, f, Some(self.format), Msg::Format));
                }
                w::dialog(look, "Exporteren", close_icon, close, formats.into(), None, vec![cancel(), w::button(look, "Exporteren", K::Primary, D::Regular, None, Some(Msg::ConfirmExport))], false)
            }
            Dialog::Print => {
                let content = column![
                    w::secondary(look, "De Gantt wordt op de standaardprinter afgedrukt. Het rapportscherm toont het afdrukvoorbeeld."),
                    w::radio(look, "Liggend", true, Some(self.landscape), Msg::Landscape),
                    w::radio(look, "Staand", false, Some(self.landscape), Msg::Landscape),
                ]
                .spacing(10);
                w::dialog(look, "Afdrukken", close_icon, close, content.into(), None, vec![cancel(), w::button(look, "Afdrukken", K::Primary, D::Regular, None, Some(Msg::ConfirmPrint))], false)
            }
            Dialog::Quit => w::dialog(
                look,
                "Niet-opgeslagen wijzigingen",
                close_icon,
                close,
                w::secondary(look, "Er zijn wijzigingen die nog niet zijn opgeslagen. Wil je ze opslaan voordat je afsluit?").into(),
                Some(w::button(look, "Niet opslaan", K::Quiet, D::Regular, None, Some(Msg::QuitNow))),
                vec![cancel(), w::button(look, "Opslaan en afsluiten", K::Primary, D::Regular, None, Some(Msg::SaveAndQuit))],
                false,
            ),
            Dialog::CloseDirty(i) => {
                let name = self.projects.get(i).map_or("dit project", |p| p.name.as_str());
                w::dialog(
                    look,
                    "Niet-opgeslagen wijzigingen",
                    close_icon,
                    close,
                    w::secondary(look, format!("'{name}' heeft wijzigingen die nog niet zijn opgeslagen.")).into(),
                    Some(w::button(look, "Niet opslaan", K::Quiet, D::Regular, None, Some(Msg::DiscardAndClose(i)))),
                    vec![cancel(), w::button(look, "Opslaan", K::Primary, D::Regular, None, Some(Msg::SaveAndClose(i)))],
                    false,
                )
            }
            Dialog::ProjectInfo => w::dialog(look, "Projectinstellingen", close_icon, close, t::info_card(look, "Project", self.info_rows()), None, vec![ok()], false),
            Dialog::Calendar => {
                let weekend = p.is_some_and(|p| p.weekend_work);
                let mut days = row![].spacing(6);
                for (d, on) in [("Ma", true), ("Di", true), ("Wo", true), ("Do", true), ("Vr", true), ("Za", weekend), ("Zo", weekend)] {
                    days = days.push(t::status_label(look, if on { Tone::Success } else { Tone::Info }, d));
                }
                let content = column![
                    w::property_row(look, "Naam", w::body(look, "Bouwkalender NL").into()),
                    w::property_row(look, "Werktijden", w::body(look, "07:00 – 16:00 · 8 uur per dag").into()),
                    w::property_row(look, "Werkdagen", days.into()),
                    w::switch(look, "Weekend als werkdagen", weekend, Some(Msg::WeekendWork)),
                    w::mono_label(look, "Feestdagen"),
                    w::secondary(look, "Goede Vrijdag, Pasen, Koningsdag, Bevrijdingsdag, Hemelvaart, Pinksteren, bouwvak (26 juli – 15 augustus 2027) en Kerst."),
                ]
                .spacing(10);
                w::dialog(look, "Kalender", close_icon, close, content.into(), None, vec![ok()], false)
            }
            Dialog::Shortcuts => {
                let keys = [
                    ("Ctrl+N", "Nieuwe taak"),
                    ("Ctrl+M", "Nieuwe mijlpaal"),
                    ("Alt+→ / Alt+←", "Inspringen / uitspringen"),
                    ("Delete", "Verwijder selectie"),
                    ("F5", "CPM berekenen"),
                    ("Ctrl+Z / Ctrl+Y", "Ongedaan maken / opnieuw"),
                    ("Ctrl+S", "Opslaan"),
                    ("Ctrl+1 / Ctrl+2", "Structuur / eigenschappen"),
                    ("Ctrl+= / Ctrl+-", "Inzoomen / uitzoomen"),
                    ("Ctrl+0", "Standaard zoom"),
                    ("Ctrl+W", "Sluit project"),
                    ("Ctrl+P / Ctrl+E", "Afdrukken / exporteren"),
                    ("Esc", "Menu, dialoog of melding sluiten"),
                ];
                let mut list = column![].spacing(4);
                for (key, what) in keys {
                    list = list.push(row![container(w::mono_label(look, key)).width(150), w::body(look, what)].spacing(12).align_y(Alignment::Center));
                }
                w::dialog(look, "Sneltoetsen", close_icon, close, list.into(), None, vec![ok()], false)
            }
            Dialog::Relation => {
                let choices = p.map(Project::task_choices).unwrap_or_default();
                let name = p.and_then(Project::selected_task).map(|t| t.name.clone()).unwrap_or_default();
                let content: Element<'_, Msg> = if choices.is_empty() {
                    w::secondary(look, "Alle andere taken zijn al voorganger van deze taak.").into()
                } else {
                    column![
                        w::secondary(look, format!("Kies de voorganger van {name}.")),
                        w::property_row(look, "Kies een taak", w::select(look, Box::leak(choices.into_boxed_slice()), self.relation_pick.clone(), Msg::RelationPick, D::Regular)),
                        w::property_row(
                            look,
                            "Type relatie",
                            row![
                                w::radio(look, "FS", RelKind::FS, Some(self.relation_kind), Msg::RelationKind),
                                w::radio(look, "SS", RelKind::SS, Some(self.relation_kind), Msg::RelationKind),
                                w::radio(look, "FF", RelKind::FF, Some(self.relation_kind), Msg::RelationKind),
                            ]
                            .spacing(12)
                            .into(),
                        ),
                    ]
                    .spacing(12)
                    .into()
                };
                w::dialog(look, "Relatie toevoegen", close_icon, close, content, None, vec![cancel(), w::button(look, "Relatie vastleggen", K::Primary, D::Regular, None, self.relation_pick.as_ref().map(|_| Msg::ConfirmRelation))], false)
            }
            Dialog::MoveProject => {
                let content = column![
                    w::secondary(look, "Verschuif alle taken een aantal werkdagen. Een negatief getal schuift naar voren."),
                    w::property_row(look, "Werkdagen", w::text_field(look, "5", &self.move_text, Some(Msg::MoveDays), D::Regular, self.move_text.trim().parse::<i32>().is_err().then_some("Geen getal"))),
                ]
                .spacing(12);
                w::dialog(look, "Project verplaatsen", close_icon, close, content.into(), None, vec![cancel(), w::button(look, "Verplaatsen", K::Primary, D::Regular, None, Some(Msg::ConfirmMove))], false)
            }
            Dialog::NewResource => {
                let content = column![
                    w::secondary(look, "Een ploeg, persoon, machine of materiaal dat je aan taken toewijst."),
                    w::property_row(look, "Naam", w::text_field(look, "Bijvoorbeeld Steigerbouwers", &self.resource_text, Some(Msg::ResourceName), D::Regular, None)),
                ]
                .spacing(12);
                w::dialog(look, "Nieuwe resource", close_icon, close, content.into(), None, vec![cancel(), w::button(look, "Toevoegen", K::Primary, D::Regular, None, Some(Msg::ConfirmResource))], false)
            }
            Dialog::Baselines => {
                let has = p.is_some_and(|p| p.baseline.is_some());
                let content = column![
                    w::secondary(look, if has { "Er is een baseline vastgelegd. Een nieuwe baseline vervangt die." } else { "Nog geen baseline. Leg de huidige planning vast om later verschillen te zien." }),
                    w::checkbox(look, "Baseline-overlay tonen", self.show_baseline, has.then_some(|_| Msg::ToggleBaseline)),
                ]
                .spacing(12);
                w::dialog(look, "Baselines beheren", close_icon, close, content.into(), None, vec![cancel(), w::button(look, "Baseline vastleggen", K::Primary, D::Regular, None, Some(Msg::SetBaseline))], false)
            }
        }
    }
}

// ---------- Small drawing helpers ----------

/// A column of small ribbon buttons.
fn stack<'a>(buttons: Vec<Element<'a, Msg>>) -> Element<'a, Msg> {
    column(buttons).spacing(2).into()
}

fn tone_icon(tone: Tone) -> &'static str {
    match tone {
        Tone::Error => s(Icon::StatusError),
        Tone::Warning => s(Icon::StatusWarning),
        Tone::Success => s(Icon::StatusSuccess),
        Tone::Info => s(Icon::StatusInfo),
    }
}

fn mix(top: Color, amount: f32, bottom: Color) -> Color {
    openaec_ui::design::mix(top, amount, bottom)
}

/// A filled rectangle with rounded corners.
fn block<'a>(color: Color, width: f32, height: f32, radius: f32) -> Element<'a, Msg> {
    container(Space::new().width(width).height(height))
        .style(move |_| container::Style { background: Some(Background::Color(color)), border: iced::Border { radius: radius.into(), ..Default::default() }, ..Default::default() })
        .into()
}

fn hbar<'a>(color: Color) -> Element<'a, Msg> {
    container(Space::new().width(Length::Fill).height(1)).style(move |_| container::Style { background: Some(Background::Color(color)), ..Default::default() }).into()
}

fn vbar<'a>(color: Color) -> Element<'a, Msg> {
    container(Space::new().width(1).height(Length::Fill)).style(move |_| container::Style { background: Some(Background::Color(color)), ..Default::default() }).into()
}

/// A 1 px vertical line at `x` in a row of `height`.
fn vline<'a>(color: Color, x: f32, height: f32) -> Element<'a, Msg> {
    row![Space::new().width(x.max(0.0)), block(color, 1.0, height, 0.0)].into()
}

fn legend_item<'a>(look: Look, color: Color, label: &'a str) -> Element<'a, Msg> {
    row![block(color, 14.0, 8.0, 2.0), w::secondary(look, label)].spacing(6).align_y(Alignment::Center).into()
}

/// A 28 px row that selects on click, as the table rows of the library.
fn selectable_row<'a>(look: Look, content: Element<'a, Msg>, selected: bool, on_press: Msg, on_menu: Msg) -> Element<'a, Msg> {
    let c = look.color;
    let hc = look.high_contrast();
    let lead: Element<'a, Msg> = if selected && !hc { block(c.selected_bar, 3.0, ROW, 0.0) } else { Space::new().width(3).into() };
    let body = iced::widget::button(container(content).height(Length::Fill).align_y(Vertical::Center))
        .padding(0)
        .width(Length::Fill)
        .height(Length::Fill)
        .on_press(on_press)
        .style(move |_, status| iced::widget::button::Style {
            background: if status == iced::widget::button::Status::Hovered && !selected && !hc { Some(Background::Color(c.hover)) } else { None },
            text_color: c.text,
            border: iced::Border { color: if status == iced::widget::button::Status::Hovered && hc { c.accent } else { Color::TRANSPARENT }, width: 1.0, radius: 0.0.into() },
            shadow: iced::Shadow::default(),
            snap: false,
        });
    container(row![lead, mouse_area(body).on_right_press(on_menu)].height(Length::Fill).align_y(Alignment::Center))
        .height(ROW)
        .width(Length::Fill)
        .style(move |_| container::Style {
            background: if selected && !hc { Some(Background::Color(c.selected)) } else { None },
            border: if selected && hc { iced::Border { color: c.selected_bar, width: 2.0, radius: 0.0.into() } } else { iced::Border::default() },
            ..Default::default()
        })
        .into()
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
    container(content).width(Length::Fill).style(move |_| w::panel_style(look)).into()
}

fn start_view() -> Planner {
    let mut planner = Planner::default();
    if let Some(arg) = std::env::args().nth(1) {
        match arg.as_str() {
            "project" => planner.started = true,
            "donker" => {
                planner.theme = ThemeId::Dark;
                planner.started = true;
            }
            _ => {}
        }
    }
    planner
}

fn main() -> iced::Result {
    iced::application(|| (start_view(), Task::none()), Planner::update, Planner::view)
        .title("Open Planner Studio · UI 0.4")
        .subscription(Planner::subscription)
        .theme(|p: &Planner| p.theme.iced())
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
    use iced::Rectangle;
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

    fn render(planner: &Planner, size: Size) -> tiny_skia::Pixmap {
        load_fonts();
        let mut element = planner.view();
        let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let mut tree = Tree::new(&element);
        let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
        let theme = planner.theme.iced();
        let style = renderer::Style { text_color: theme.palette().text };
        element.as_widget().draw(&tree, &mut renderer, &theme, &style, Layout::new(&node), mouse::Cursor::Unavailable, &Rectangle::with_size(size));
        let (width, height) = (size.width as u32, size.height as u32);
        let mut bytes = vec![0u8; (width * height * 4) as usize];
        let mut pixels = tiny_skia::PixmapMut::from_bytes(&mut bytes, width, height).expect("valid pixmap");
        let mut mask = tiny_skia::Mask::new(width, height).expect("valid mask");
        renderer.draw(&mut pixels, &mut mask, &iced_tiny_skia::graphics::Viewport::with_physical_size(Size::new(width, height), 1.0), &[Rectangle::with_size(size)], Color::from_rgb(1.0, 0.0, 1.0));
        for pixel in bytes.chunks_exact_mut(4) {
            pixel.swap(0, 2);
        }
        tiny_skia::Pixmap::from_vec(bytes, tiny_skia::IntSize::from_wh(width, height).expect("size")).expect("pixels")
    }

    fn save(pixmap: tiny_skia::Pixmap, path: std::path::PathBuf) {
        if let Err(error) = pixmap.save_png(&path) {
            eprintln!("Niet opgeslagen, bestand is in gebruik: {} ({error})", path.display());
        }
    }

    #[test]
    #[ignore = "regenerate the Planner review renders on demand"]
    fn export_review_renders() {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/ontwerp-0.4/native");
        std::fs::create_dir_all(&dir).expect("render folder");
        let size = Size::new(1280.0, 800.0);
        let mut planner = Planner::default();
        let task = id_of(planner.project().unwrap(), "3.3");
        for theme in ThemeId::ALL {
            planner.theme = theme;
            planner.started = false;
            save(render(&planner, size), dir.join(format!("planner-start-{}.png", theme.key())));
            planner.started = true;
            let _ = planner.update(Msg::Select(Some(task)));
            let _ = planner.update(Msg::RibbonTab(TAB_START));
            save(render(&planner, size), dir.join(format!("planner-gantt-{}.png", theme.key())));
        }
        planner.theme = ThemeId::Light;
        let _ = planner.update(Msg::RibbonTab(TAB_VIEW));
        let _ = planner.update(Msg::ToggleHistogram);
        save(render(&planner, size), dir.join("planner-beeld-histogram-light.png"));
        let _ = planner.update(Msg::ToggleHistogram);
        let _ = planner.update(Msg::RibbonTab(TAB_TABLE));
        let _ = planner.update(Msg::ToggleExtraColumns);
        save(render(&planner, Size::new(1400.0, 800.0)), dir.join("planner-tabel-light.png"));
        let _ = planner.update(Msg::ToggleExtraColumns);
        let _ = planner.update(Msg::RibbonTab(TAB_RESOURCES));
        let _ = planner.update(Msg::ShowWorkspace(Workspace::Resources));
        save(render(&planner, size), dir.join("planner-resources-light.png"));
        let _ = planner.update(Msg::RibbonTab(TAB_REPORT));
        save(render(&planner, size), dir.join("planner-rapport-light.png"));
        let _ = planner.update(Msg::RibbonTab(TAB_PLANNING));
        let _ = planner.update(Msg::Dialog(Some(Dialog::Relation)));
        save(render(&planner, size), dir.join("planner-relatie-light.png"));
        let _ = planner.update(Msg::Dialog(None));
        let _ = planner.update(Msg::Backstage(true));
        let _ = planner.update(Msg::FilePage(FilePage::Examples));
        save(render(&planner, size), dir.join("planner-bestand-light.png"));
        let _ = planner.update(Msg::Backstage(false));
        planner.theme = ThemeId::Dark;
        let _ = planner.update(Msg::RibbonTab(TAB_START));
        let _ = planner.update(Msg::Zoom(Zoom::Day));
        let _ = planner.update(Msg::ToggleResourceColors);
        let _ = planner.update(Msg::ToggleFloatBand);
        save(render(&planner, size), dir.join("planner-gantt-dag-dark.png"));
    }

    fn id_of(p: &Project, wbs: &str) -> u32 {
        let codes = p.wbs();
        p.tasks.iter().zip(codes).find(|(_, c)| c == wbs).map(|(t, _)| t.id).expect(wbs)
    }

    #[test]
    fn calendar_skips_weekends_and_holidays() {
        assert_eq!(dmy(0, false), "01-03-2027");
        assert_eq!(dmy(5, false), "08-03-2027");
        assert_eq!(dmy(5, true), "06-03-2027");
        // Good Friday 26 March and Easter Monday 29 March are skipped.
        assert_eq!(dmy(19, false), "26-03-2027".replace("26-03", "30-03"));
        assert_eq!(iso_week(2027, 3, 1), 9);
        assert_eq!(iso_week(2027, 7, 5), 27);
    }

    #[test]
    fn schedule_follows_relations_with_lags() {
        let p = Project::example();
        let t = |wbs: &str| p.task(id_of(&p, wbs)).unwrap();
        assert_eq!(t("1.2").start, t("1.1").end());
        assert_eq!(t("2.1").start, t("1.1").start + 12, "start-start with lag");
        assert_eq!(t("3.1").start, t("2.1").start + 4);
        assert_eq!(t("4.1").start, t("3.9").end() - 15, "negative lag");
        assert!(t("4.4").end() >= t("3.9").end() + 2, "finish-finish");
        assert_eq!(t("7.4").start, t("7.3").end());
        assert!(p.project_end() > 150);
        assert_eq!(p.wbs()[2], "1.1");
    }

    #[test]
    fn critical_path_and_float() {
        let p = Project::example();
        let floats = p.floats();
        let critical = p.critical();
        assert!(critical.contains(&id_of(&p, "7.4")), "oplevering is kritiek");
        assert!(critical.contains(&id_of(&p, "6.2")));
        assert!(floats[&id_of(&p, "1.5")] > 0, "start bouw has float");
        assert!(floats.values().all(|f| *f >= 0));
    }

    #[test]
    fn overallocation_is_found_and_levelled() {
        let mut planner = Planner::default();
        let p = planner.project().unwrap();
        let over = p.overallocations();
        assert_eq!(over.len(), 1, "{over:?}");
        assert_eq!(p.resources[over[0].0], "Timmerlieden");
        assert!(planner.banner.is_some());
        let _ = planner.update(Msg::Level);
        assert!(planner.project().unwrap().overallocations().is_empty());
        assert!(planner.banner.is_none());
        let _ = planner.update(Msg::Undo);
        assert_eq!(planner.project().unwrap().overallocations().len(), 1);
    }

    #[test]
    fn editing_marks_dirty_and_undo_restores() {
        let mut planner = Planner::default();
        planner.started = true;
        let id = id_of(planner.project().unwrap(), "3.2");
        let next = id_of(planner.project().unwrap(), "3.3");
        let _ = planner.update(Msg::Select(Some(id)));
        let _ = planner.update(Msg::EditDuration("12".into()));
        let p = planner.project().unwrap();
        assert_eq!(p.task(id).unwrap().duration, 12);
        assert!(p.dirty && !p.scheduled);
        let _ = planner.update(Msg::Schedule);
        let p = planner.project().unwrap();
        assert_eq!(p.task(next).unwrap().start, p.task(id).unwrap().end());
        let _ = planner.update(Msg::Undo);
        assert_eq!(planner.project().unwrap().task(id).unwrap().duration, 5);
    }

    #[test]
    fn tasks_indent_outdent_add_and_delete() {
        let mut planner = Planner::default();
        planner.started = true;
        let before = planner.project().unwrap().tasks.len();
        let leaf = id_of(planner.project().unwrap(), "1.5");
        let _ = planner.update(Msg::Select(Some(leaf)));
        let _ = planner.update(Msg::AddTask);
        assert_eq!(planner.project().unwrap().tasks.len(), before + 1);
        let new_id = planner.project().unwrap().selected.unwrap();
        assert_eq!(planner.project().unwrap().task(new_id).unwrap().level, 2);
        let _ = planner.update(Msg::Outdent);
        assert_eq!(planner.project().unwrap().task(new_id).unwrap().level, 1);
        let _ = planner.update(Msg::Indent);
        assert_eq!(planner.project().unwrap().task(new_id).unwrap().level, 2);
        let _ = planner.update(Msg::Delete);
        assert_eq!(planner.project().unwrap().tasks.len(), before);
        // Deleting a phase removes its children and the relations to them.
        let phase = id_of(planner.project().unwrap(), "1");
        let _ = planner.update(Msg::Select(Some(phase)));
        let _ = planner.update(Msg::Delete);
        let p = planner.project().unwrap();
        assert_eq!(p.tasks.len(), before - 6);
        assert!(p.task(id_of(p, "1.1")).unwrap().predecessors.is_empty(), "2.1 lost its predecessor 1.1");
    }

    #[test]
    fn projects_open_and_close_as_tabs() {
        let mut planner = Planner::default();
        planner.started = true;
        let _ = planner.update(Msg::New);
        assert_eq!(planner.projects.len(), 2);
        assert_eq!(planner.active, 1);
        let _ = planner.update(Msg::AddTask);
        let _ = planner.update(Msg::CloseDoc(1));
        assert_eq!(planner.dialog, Some(Dialog::CloseDirty(1)));
        let _ = planner.update(Msg::DiscardAndClose(1));
        assert_eq!(planner.projects.len(), 1);
        let _ = planner.update(Msg::OpenExample(0));
        assert_eq!(planner.projects.len(), 1, "the example is already open");
    }

    #[test]
    fn every_theme_tab_workspace_and_dialog_builds() {
        let mut planner = Planner::default();
        let _ = planner.view();
        planner.started = true;
        let task = id_of(planner.project().unwrap(), "3.2");
        for theme in ThemeId::ALL {
            planner.theme = theme;
            for tab in 0..TABS.len() {
                let _ = planner.update(Msg::RibbonTab(tab));
                let _ = planner.view();
            }
            for ws in [Workspace::Gantt, Workspace::Table, Workspace::Resources, Workspace::Report] {
                let _ = planner.update(Msg::ShowWorkspace(ws));
                let _ = planner.view();
            }
            let _ = planner.update(Msg::ToggleHistogram);
            let _ = planner.update(Msg::ShowWorkspace(Workspace::Gantt));
            let _ = planner.view();
            let _ = planner.update(Msg::ToggleHistogram);
            for d in [Dialog::Settings, Dialog::Export, Dialog::Print, Dialog::Quit, Dialog::CloseDirty(0), Dialog::ProjectInfo, Dialog::Calendar, Dialog::Shortcuts, Dialog::Relation, Dialog::MoveProject, Dialog::NewResource, Dialog::Baselines] {
                let _ = planner.update(Msg::Select(Some(task)));
                let _ = planner.update(Msg::Dialog(Some(d)));
                let _ = planner.view();
            }
            let _ = planner.update(Msg::Dialog(None));
            for z in Zoom::ALL {
                let _ = planner.update(Msg::Zoom(z));
                let _ = planner.view();
            }
            let _ = planner.update(Msg::Backstage(true));
            for page in [FilePage::New, FilePage::Open, FilePage::Examples, FilePage::Export, FilePage::Info] {
                let _ = planner.update(Msg::FilePage(page));
                let _ = planner.view();
            }
            let _ = planner.update(Msg::Backstage(false));
            let _ = planner.update(Msg::SetBaseline);
            let _ = planner.update(Msg::ToggleProgressLine);
            let _ = planner.update(Msg::ToggleResourceColors);
            let _ = planner.update(Msg::ToggleFloatBand);
            let _ = planner.update(Msg::ToggleLeft);
            let _ = planner.update(Msg::Menu(Some(MenuKind::Task(task))));
            let _ = planner.view();
            let _ = planner.update(Msg::Menu(Some(MenuKind::App)));
            let _ = planner.view();
            let _ = planner.update(Msg::Menu(None));
            let _ = planner.update(Msg::CloseAll);
            let _ = planner.view();
            let _ = planner.update(Msg::OpenExample(0));
        }
    }
}
