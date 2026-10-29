//! OpenAEC Blueprint: the empty standard application in Rust (issue #37, step 4).
//!
//! Every OpenAEC tool starts from this shell: title bar with quick actions and
//! window buttons, ribbon with Bestand, document tabs, side panels, status bar,
//! settings with themes and own shortcuts, and the shared behaviour of library
//! 0.4: keyboard focus, one command list, saving and closing through a close plan,
//! undo per document, the update notice of the installer and accessible names.
//! It has no functions of its own; an app adds its work in the workspace and
//! its commands to `commands()`.
//!
//! Run with `cargo run --bin blueprint`.
use openaec_icons::{Icon, Size as IconSize};
use openaec_ui::design::chrome::{self as ch, WindowActions, WindowIcons};
use openaec_ui::design::command::{self as cm, Command, Shortcut};
use openaec_ui::design::document::{self as dm, Choice, ClosePlan, DocumentState, Request, SaveKind, SaveTicket, Step};
use openaec_ui::design::focus;
use openaec_ui::design::history::{self as hist, History};
use openaec_ui::design::shortcuts::{self as sc, Keymap};
use openaec_ui::design::tiles as t;
use openaec_ui::design::update::{self as upd, Available};
use openaec_ui::design::widgets::{self as w, ButtonKind as K, Density as D, DocumentTab, Tone};
use openaec_ui::design::display::{self as dsp, Display};
use openaec_ui::design::{Look, StatusbarSetting, TextSize, ThemeId, WorkspaceSetting};
use openaec_ui::fonts;
use openaec_ui::iced::widget::{column, container, mouse_area, row};
use openaec_ui::iced::{self, Element, Length, Size, Subscription, Task};
use openaec_ui::keyboard::{KeyPress, Navigation};
use std::time::{Duration, Instant};

/// The id of this app in the installer's catalogue, for the update notice.
const APP_ID: &str = "openaec-blueprint";
const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Shortcut groups on the settings page, by command id prefix.
const COMMAND_GROUPS: [(&str, &str); 4] = [("file", "Bestand"), ("edit", "Bewerken"), ("view", "Weergave"), ("app", "Programma")];

/// A B2 icon from the `openaec-icons` crate, as every app loads them.
fn icon(id: &str, size: IconSize) -> &'static str {
    Icon::from_id(id).unwrap_or_else(|| panic!("icon {id} in openaec-icons")).svg(size)
}

fn small(id: &str) -> &'static str {
    icon(id, IconSize::S16)
}

fn large(id: &str) -> &'static str {
    icon(id, IconSize::S24)
}

fn window_icons() -> WindowIcons {
    WindowIcons { minimize: small("window.minimize"), maximize: small("window.maximize"), restore: small("window.restore"), close: small("window.close") }
}

/// The contents of one document. A real app keeps its model here.
#[derive(Debug, Clone, PartialEq)]
struct Content {
    name: String,
    description: String,
}

struct Doc {
    id: u32,
    title: String,
    content: Content,
    state: DocumentState,
    history: History<Content>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Dialog {
    Settings,
    Close,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SettingsPage {
    General,
    Shortcuts,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum CloseTarget {
    Documents,
    Window,
    Update,
}

#[derive(Debug, Clone)]
enum Msg {
    Theme(ThemeId),
    Workspace(WorkspaceSetting),
    Statusbar(StatusbarSetting),
    TextSize(TextSize),
    RibbonTab(usize),
    Backstage(bool),
    New,
    Save,
    Written(u32, SaveTicket),
    Undo,
    Redo,
    SelectDoc(usize),
    CloseDoc(usize),
    CloseWindow,
    Update,
    CloseChoose(Choice),
    CloseChooseAll(Choice),
    Dialog(Option<Dialog>),
    SettingsPage(SettingsPage),
    Shortcuts(sc::Message),
    Key(KeyPress),
    Navigate(Navigation),
    EditName(String),
    EditDescription(String),
    ToggleLeft,
    ToggleRight,
    TitlePress,
    Minimize,
    Maximize,
    CloseToast,
}

struct Toast {
    tone: Tone,
    title: String,
    message: String,
}

struct App {
    theme: ThemeId,
    workspace: WorkspaceSetting,
    statusbar: StatusbarSetting,
    text_size: TextSize,
    /// Where the display settings are stored; `None` in tests, so they never write.
    display_path: Option<std::path::PathBuf>,
    docs: Vec<Doc>,
    active: usize,
    next_number: u32,
    ribbon_tab: usize,
    backstage: bool,
    left: bool,
    right: bool,
    dialog: Option<Dialog>,
    settings_page: SettingsPage,
    closing: Option<(ClosePlan<u32>, CloseTarget)>,
    keymap: Keymap,
    /// Where own shortcuts are stored; `None` in tests, so they never write.
    keymap_path: Option<std::path::PathBuf>,
    shortcuts: sc::Editor,
    update: Option<Available>,
    toast: Option<Toast>,
    maximized: bool,
    last_title_press: Option<Instant>,
}

impl Default for App {
    fn default() -> Self {
        let mut app = Self {
            theme: ThemeId::Light,
            workspace: WorkspaceSetting::Theme,
            statusbar: StatusbarSetting::Theme,
            text_size: TextSize::Standard,
            display_path: None,
            docs: Vec::new(),
            active: 0,
            next_number: 1,
            ribbon_tab: 0,
            backstage: false,
            left: true,
            right: true,
            dialog: None,
            settings_page: SettingsPage::General,
            closing: None,
            keymap: Keymap::default(),
            keymap_path: None,
            shortcuts: sc::Editor::default(),
            update: None,
            toast: None,
            maximized: false,
            last_title_press: None,
        };
        app.new_doc();
        app
    }
}

impl App {
    fn look(&self) -> Look {
        self.display().look()
    }

    fn display(&self) -> Display {
        Display { theme: self.theme, workspace: self.workspace, statusbar: self.statusbar, text_size: self.text_size }
    }

    /// Keeps the display settings for the next start (issue #27).
    fn save_display(&self) {
        if let Some(path) = &self.display_path {
            let _ = self.display().save(path);
        }
    }

    fn doc(&self) -> Option<&Doc> {
        self.docs.get(self.active)
    }

    fn doc_mut(&mut self) -> Option<&mut Doc> {
        self.docs.get_mut(self.active)
    }

    fn new_doc(&mut self) {
        let id = self.next_number;
        self.next_number += 1;
        let title = format!("Naamloos {id}");
        let content = Content { name: title.clone(), description: String::new() };
        self.docs.push(Doc { id, title, content, state: DocumentState::new_file(), history: History::new() });
        self.active = self.docs.len() - 1;
    }

    /// Every command, in one place (issue #9): the ribbon, the title bar and the
    /// shortcuts read from this list. Own shortcuts are applied on top.
    fn default_commands(&self) -> Vec<Command<Msg>> {
        let history = self.doc().map(|d| &d.history);
        vec![
            Command::new("file.new", "Nieuw", Msg::New).icon(small("file.new"), large("file.new")).shortcut(Shortcut::ctrl('n')),
            Command::new("file.save", "Opslaan", Msg::Save).icon(small("file.save"), large("file.save")).shortcut(Shortcut::ctrl('s')).enabled(self.doc().is_some()),
            Command::new("edit.undo", "Ongedaan", Msg::Undo)
                .icon(small("edit.undo"), large("edit.undo"))
                .shortcut(Shortcut::ctrl('z'))
                .enabled(history.is_some_and(History::can_undo))
                .detail(&hist::undo_text(history.and_then(History::undo_label))),
            Command::new("edit.redo", "Opnieuw", Msg::Redo)
                .icon(small("edit.redo"), large("edit.redo"))
                .shortcut(Shortcut::ctrl('y'))
                .enabled(history.is_some_and(History::can_redo))
                .detail(&hist::redo_text(history.and_then(History::redo_label))),
            Command::new("view.left", "Verkenner", Msg::ToggleLeft).icon_small(small("panel.left")).shortcut(Shortcut::ctrl('1')).toggle(self.left),
            Command::new("view.right", "Eigenschappen", Msg::ToggleRight).icon_small(small("panel.right")).shortcut(Shortcut::ctrl('2')).toggle(self.right),
            Command::new("app.settings", "Instellingen…", Msg::Dialog(Some(Dialog::Settings))).icon(small("ui.settings"), large("ui.settings")).shortcut(Shortcut::ctrl(',')).dialog(),
        ]
    }

    fn commands(&self) -> Vec<Command<Msg>> {
        let mut list = self.default_commands();
        self.keymap.apply(&mut list);
        list
    }

    fn command(&self, id: &str) -> Command<Msg> {
        self.commands().into_iter().find(|c| c.id == id).expect("command")
    }

    fn toast(&mut self, tone: Tone, title: &str, message: impl Into<String>) {
        self.toast = Some(Toast { tone, title: title.into(), message: message.into() });
    }

    /// One change to the active document, typed in a field: one undo step per
    /// run of typing in that field (issue #34).
    fn edit(&mut self, label: &str, field: &str, change: impl FnOnce(&mut Content)) {
        let Some(doc) = self.doc_mut() else { return };
        doc.history.record_merged(label, field, doc.content.clone());
        change(&mut doc.content);
        doc.state.edit();
    }

    /// Start writing a document. This is where a real app serialises its
    /// content and writes the file; a new document first asks for a name.
    fn write(&mut self, id: u32) -> Task<Msg> {
        let Some(doc) = self.docs.iter_mut().find(|d| d.id == id) else { return Task::none() };
        let mut request = doc.state.request(SaveKind::Save);
        if request == Request::NeedsPath {
            // A real app asks for a file name here (Opslaan als).
            doc.state.set_path();
            request = doc.state.request(SaveKind::Save);
        }
        match request {
            Request::Start(ticket) => Task::done(Msg::Written(id, ticket)),
            Request::Queued | Request::NotNeeded | Request::NeedsPath => Task::none(),
        }
    }

    /// Close documents, the window or for an update through one close plan (issue #10).
    fn start_close(&mut self, target: CloseTarget, ids: Vec<u32>) -> Task<Msg> {
        let documents = ids.into_iter().filter_map(|id| self.docs.iter().find(|d| d.id == id).map(|d| (id, d.state.is_dirty()))).collect::<Vec<_>>();
        self.closing = Some((ClosePlan::new(documents), target));
        self.advance_close()
    }

    fn advance_close(&mut self) -> Task<Msg> {
        let Some((plan, target)) = &self.closing else { return Task::none() };
        match plan.step() {
            Step::Ask { .. } => self.dialog = Some(Dialog::Close),
            Step::Wait => self.dialog = None,
            Step::Close(ids) => {
                let target = *target;
                self.closing = None;
                self.dialog = None;
                match target {
                    CloseTarget::Window => return iced::window::latest().and_then(iced::window::close),
                    CloseTarget::Update => {
                        if let Some(available) = self.update.take() {
                            if let Err(reason) = upd::open_installer(&available) {
                                self.toast(Tone::Error, "Bijwerken mislukt", reason);
                                return Task::none();
                            }
                        }
                        return iced::window::latest().and_then(iced::window::close);
                    }
                    CloseTarget::Documents => {
                        self.docs.retain(|d| !ids.contains(&d.id));
                        self.active = self.active.min(self.docs.len().saturating_sub(1));
                    }
                }
            }
        }
        Task::none()
    }

    fn close_choose(&mut self, choice: Choice, all: bool) -> Task<Msg> {
        let Some((plan, _)) = self.closing.as_mut() else { return Task::none() };
        let to_save = if all { plan.choose_all(choice) } else { plan.choose(choice) };
        let mut tasks: Vec<Task<Msg>> = to_save.into_iter().map(|id| self.write(id)).collect();
        tasks.push(self.advance_close());
        Task::batch(tasks)
    }

    fn update(&mut self, message: Msg) -> Task<Msg> {
        match message {
            Msg::Theme(theme) => {
                self.theme = theme;
                self.save_display();
            }
            Msg::Workspace(setting) => {
                self.workspace = setting;
                self.save_display();
            }
            Msg::Statusbar(setting) => {
                self.statusbar = setting;
                self.save_display();
            }
            Msg::TextSize(size) => {
                self.text_size = size;
                self.save_display();
            }
            Msg::RibbonTab(i) => self.ribbon_tab = i,
            Msg::Backstage(open) => self.backstage = open,
            Msg::New => {
                self.backstage = false;
                self.new_doc();
            }
            Msg::Save => {
                self.backstage = false;
                if let Some(id) = self.doc().map(|d| d.id) {
                    return self.write(id);
                }
            }
            Msg::Written(id, ticket) => {
                let Some(doc) = self.docs.iter_mut().find(|d| d.id == id) else { return Task::none() };
                let next = doc.state.finish(ticket, Ok(()));
                let (done, clean, title) = (!doc.state.is_saving(), !doc.state.is_dirty(), doc.title.clone());
                if let Some(next) = next {
                    return Task::done(Msg::Written(id, next));
                }
                if done && self.closing.as_ref().is_some_and(|(plan, _)| plan.is_waiting_for(id)) {
                    let ok = self.closing.as_mut().is_some_and(|(plan, _)| plan.saved(id, clean));
                    if !ok {
                        self.closing = None;
                        self.toast(Tone::Error, "Niet gesloten", format!("{title} is niet opgeslagen, dus er is niets gesloten."));
                        return Task::none();
                    }
                    return self.advance_close();
                }
                if done {
                    self.toast(Tone::Success, "Opgeslagen", format!("{title} is opgeslagen."));
                }
            }
            Msg::Undo => {
                if let Some(doc) = self.doc_mut() {
                    if let Some(previous) = doc.history.undo(doc.content.clone()) {
                        doc.content = previous;
                        doc.state.edit();
                    }
                }
            }
            Msg::Redo => {
                if let Some(doc) = self.doc_mut() {
                    if let Some(next) = doc.history.redo(doc.content.clone()) {
                        doc.content = next;
                        doc.state.edit();
                    }
                }
            }
            Msg::SelectDoc(i) => {
                self.active = i;
                if let Some(doc) = self.doc_mut() {
                    doc.history.seal();
                }
            }
            Msg::CloseDoc(i) => {
                if let Some(id) = self.docs.get(i).map(|d| d.id) {
                    return self.start_close(CloseTarget::Documents, vec![id]);
                }
            }
            Msg::CloseWindow => {
                let ids = self.docs.iter().map(|d| d.id).collect();
                return self.start_close(CloseTarget::Window, ids);
            }
            Msg::Update => {
                let ids = self.docs.iter().map(|d| d.id).collect();
                return self.start_close(CloseTarget::Update, ids);
            }
            Msg::CloseChoose(choice) => return self.close_choose(choice, false),
            Msg::CloseChooseAll(choice) => return self.close_choose(choice, true),
            Msg::Dialog(dialog) => {
                let opening = dialog.is_some() && self.dialog.is_none();
                self.dialog = dialog;
                if dialog.is_none() {
                    self.closing = None;
                    self.shortcuts = sc::Editor::default();
                }
                if opening {
                    return openaec_ui::keyboard::navigate(Navigation::Next);
                }
            }
            Msg::SettingsPage(page) => self.settings_page = page,
            Msg::Shortcuts(message) => {
                let defaults = self.default_commands();
                if self.shortcuts.update(message, &mut self.keymap, &defaults) {
                    if let Some(path) = &self.keymap_path {
                        if let Err(error) = self.keymap.save(path) {
                            self.toast(Tone::Error, "Sneltoetsen niet opgeslagen", error.to_string());
                        }
                    }
                }
            }
            Msg::Key(press) if self.shortcuts.recording() => return self.update(Msg::Shortcuts(sc::Message::Key(press))),
            Msg::Key(press) => {
                use iced::keyboard::{key::Named, Key};
                if press.key == Key::Named(Named::Escape) {
                    if self.dialog.is_some() {
                        return self.update(Msg::Dialog(None));
                    }
                    self.backstage = false;
                    return Task::none();
                }
                if self.dialog.is_none() {
                    if let Some(message) = cm::find(&self.commands(), &press.key, press.modifiers) {
                        return self.update(message);
                    }
                }
            }
            Msg::Navigate(step) => return openaec_ui::keyboard::navigate(step),
            Msg::EditName(name) => {
                self.edit("Naam wijzigen", "name", |c| c.name = name);
                if let Some(doc) = self.doc_mut() {
                    doc.title = if doc.content.name.trim().is_empty() { format!("Naamloos {}", doc.id) } else { doc.content.name.clone() };
                }
            }
            Msg::EditDescription(text) => self.edit("Omschrijving wijzigen", "description", |c| c.description = text),
            Msg::ToggleLeft => self.left = !self.left,
            Msg::ToggleRight => self.right = !self.right,
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
            Msg::CloseToast => self.toast = None,
        }
        Task::none()
    }

    fn subscription(&self) -> Subscription<Msg> {
        Subscription::batch([
            openaec_ui::keyboard::presses().map(Msg::Key),
            openaec_ui::keyboard::navigation().map(Msg::Navigate),
            // The window's own close (Alt+F4, taskbar) also goes through the close plan.
            iced::window::close_requests().map(|_| Msg::CloseWindow),
        ])
    }

    /// The save status for the status bar.
    fn save_status(&self) -> String {
        match self.doc().map(|d| d.state.status()) {
            Some(dm::Status::Saved) | None => "Gereed".into(),
            Some(status) => status.label(),
        }
    }

    fn view(&self) -> Element<'_, Msg> {
        let look = self.look();
        let c = look.color;
        let screen = column![
            self.title_bar(look),
            w::ribbon_tabs(look, "Bestand", Some(Msg::Backstage(!self.backstage)), &["Start"], self.ribbon_tab, Msg::RibbonTab),
            if self.backstage { self.backstage_view(look) } else { self.ribbon(look) },
            self.document_area(look),
            w::status_bar(look, vec![self.save_status(), format!("{} document(en)", self.docs.len())], vec![format!("OpenAEC Blueprint {VERSION}")]),
        ]
        .height(Length::Fill);
        let mut layers = vec![focus::inert(container(screen).style(move |_| container::Style { background: Some(c.frame.into()), ..Default::default() }), self.dialog.is_some())];
        if let Some(toast) = &self.toast {
            let card = w::toast(look, toast.tone, small("status.success"), &toast.title, &toast.message, small("window.close"), Some(Msg::CloseToast));
            layers.push(container(card).width(Length::Fill).height(Length::Fill).align_right(Length::Fill).align_bottom(Length::Fill).padding([36, 16]).into());
        }
        if let Some(dialog) = self.dialog {
            layers.push(mouse_area(w::overlay(look, self.dialog_card(look, dialog))).into());
        }
        iced::widget::Stack::with_children(layers).into()
    }

    fn title_bar(&self, look: Look) -> Element<'_, Msg> {
        let quick = vec![
            cm::icon_button(look, &self.command("file.save"), 28.0),
            cm::icon_button(look, &self.command("edit.undo"), 28.0),
            cm::icon_button(look, &self.command("edit.redo"), 28.0),
        ];
        let mut extra = Vec::new();
        if let Some(available) = &self.update {
            extra.push(container(upd::notice(look, available, Msg::Update)).padding([0, 8]).into());
        }
        extra.push(cm::icon_button(look, &self.command("app.settings"), 28.0));
        let name = match self.doc() {
            Some(doc) => format!("{}{} · OpenAEC Blueprint", doc.title, if doc.state.is_dirty() { " •" } else { "" }),
            None => "OpenAEC Blueprint".into(),
        };
        let window = WindowActions { drag: Msg::TitlePress, minimize: Msg::Minimize, maximize: Msg::Maximize, close: Msg::CloseWindow, maximized: self.maximized };
        ch::title_bar(look, name, quick, extra, window, window_icons())
    }

    fn ribbon(&self, look: Look) -> Element<'_, Msg> {
        w::ribbon(
            look,
            vec![
                w::ribbon_group(look, "Project", vec![cm::ribbon_large(look, &self.command("file.new")), cm::ribbon_large(look, &self.command("file.save"))]),
                w::ribbon_group(look, "Geschiedenis", vec![cm::ribbon_large(look, &self.command("edit.undo")), cm::ribbon_large(look, &self.command("edit.redo"))]),
                w::ribbon_group(look, "Weergave", vec![column![cm::ribbon_small(look, &self.command("view.left")), cm::ribbon_small(look, &self.command("view.right"))].spacing(2).into()]),
            ],
        )
    }

    /// Bestand: the file page.
    fn backstage_view(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let nav = column![
            t::file_nav_row(look, small("file.new"), "Nieuw", false, Some(Msg::New)),
            t::file_nav_row(look, small("file.save"), "Opslaan", false, self.doc().map(|_| Msg::Save)),
            t::file_nav_row(look, small("ui.settings"), "Instellingen", false, Some(Msg::Dialog(Some(Dialog::Settings)))),
        ]
        .width(260);
        let recent = column![w::heading(look, "Recente bestanden", 16.0), w::secondary(look, "Nog geen bestanden. Een app toont hier de laatst geopende projecten.")].spacing(8).padding(24);
        container(row![container(nav).height(Length::Fill).style(move |_| w::panel_style(look)), recent]).height(Length::Fill).style(move |_| container::Style { background: Some(c.panel.into()), ..Default::default() }).into()
    }

    fn document_area(&self, look: Look) -> Element<'_, Msg> {
        let c = look.color;
        let tabs: Vec<DocumentTab<'_>> = self.docs.iter().map(|d| DocumentTab::new(&d.title, d.state.is_dirty())).collect();
        let workspace: Element<'_, Msg> = container(w::empty_state(
            look,
            large("project.folder"),
            "Lege werkruimte",
            "Hier komt het werk van de app. De schil eromheen is de standaard van OpenAEC.",
            None,
        ))
        .width(Length::Fill)
        .height(Length::Fill)
        .style(move |_| container::Style { background: Some(c.workspace.into()), ..Default::default() })
        .into();
        let mut body = row![].height(Length::Fill);
        if self.left {
            let mut tree = column![];
            for (i, doc) in self.docs.iter().enumerate() {
                tree = tree.push(w::tree_row(look, 0, None, None, Some(small("data.table")), &doc.title, i == self.active, Some(Msg::SelectDoc(i)), None));
            }
            let actions = vec![w::with_tooltip(look, w::icon_button(look, small("panel.left"), 20.0, true, "Verkenner verbergen", Some(Msg::ToggleLeft)), "Verkenner verbergen", Some("Ctrl+1"))];
            body = body.push(w::panel(look, "Verkenner", 240.0, actions, focus::group(tree, focus::Axis::Vertical)));
        }
        body = body.push(column![w::document_tabs(look, &tabs, self.active, small("window.close"), Msg::SelectDoc, Msg::CloseDoc, Msg::SelectDoc), workspace].width(Length::Fill));
        if self.right {
            let actions = vec![w::with_tooltip(look, w::icon_button(look, small("panel.right"), 20.0, true, "Eigenschappen verbergen", Some(Msg::ToggleRight)), "Eigenschappen verbergen", Some("Ctrl+2"))];
            let content: Element<'_, Msg> = match self.doc() {
                Some(doc) => column![
                    w::property_row(look, "Naam", w::text_field(look, "Naam", &doc.content.name, Some(Msg::EditName), D::Compact, None)),
                    w::property_row(look, "Omschrijving", w::text_field(look, "Omschrijving", &doc.content.description, Some(Msg::EditDescription), D::Compact, None)),
                    w::property_row(look, "Status", w::body(look, doc.state.status().label()).into()),
                ]
                .spacing(4)
                .padding([8, 0])
                .into(),
                None => container(w::secondary(look, "Geen document geopend.")).padding(12).into(),
            };
            body = body.push(w::panel(look, "Eigenschappen", 240.0, actions, content));
        }
        body.into()
    }

    fn dialog_card(&self, look: Look, dialog: Dialog) -> Element<'_, Msg> {
        let close_icon = small("window.close");
        match dialog {
            Dialog::Settings => {
                let tab = |page, label| w::button(look, label, if self.settings_page == page { K::Secondary } else { K::Quiet }, D::Compact, None, Some(Msg::SettingsPage(page)));
                let tabs = row![tab(SettingsPage::General, "Algemeen"), tab(SettingsPage::Shortcuts, "Sneltoetsen")].spacing(4);
                let body: Element<'_, Msg> = match self.settings_page {
                    SettingsPage::General => column![
                        w::mono_label(look, "Weergave"),
                        w::property_row(look, "Thema", w::select(look, &ThemeId::ALL, Some(self.theme), Msg::Theme, D::Regular)),
                        w::property_row(look, "Werkruimte", w::select(look, &WorkspaceSetting::ALL, Some(self.workspace), Msg::Workspace, D::Regular)),
                        w::property_row(look, "Statusbalk", w::select(look, &StatusbarSetting::ALL, Some(self.statusbar), Msg::Statusbar, D::Regular)),
                        w::property_row(look, "Tekstgrootte", w::select(look, &TextSize::ALL, Some(self.text_size), Msg::TextSize, D::Regular)),
                    ]
                    .spacing(6)
                    .into(),
                    SettingsPage::Shortcuts => sc::page(look, &self.shortcuts, &self.commands(), &self.keymap, &COMMAND_GROUPS, Msg::Shortcuts),
                };
                w::dialog(look, "Instellingen", close_icon, Some(Msg::Dialog(None)), column![tabs, body].spacing(14).into(), None, vec![w::button(look, "Sluiten", K::Primary, D::Regular, None, Some(Msg::Dialog(None)))], true)
            }
            Dialog::Close => {
                let (id, number, of) = match self.closing.as_ref().map(|(plan, _)| plan.step()) {
                    Some(Step::Ask { id, number, of }) => (Some(id), number, of),
                    _ => (None, 1, 1),
                };
                let name = id.and_then(|id| self.docs.iter().find(|d| d.id == id)).map_or("dit document", |d| d.title.as_str());
                dm::close_dialog(look, name, number, of, close_icon, Msg::Dialog(None), Msg::CloseChoose(Choice::Discard), Msg::CloseChoose(Choice::Save), Msg::CloseChooseAll(Choice::Save))
            }
        }
    }
}

fn main() -> iced::Result {
    fonts::install_fallback();
    let mut app = App::default();
    app.keymap_path = sc::keymap_path("blueprint");
    app.display_path = dsp::settings_path("blueprint");
    if let Some(path) = &app.display_path {
        let saved = Display::load(path);
        (app.theme, app.workspace, app.statusbar, app.text_size) = (saved.theme, saved.workspace, saved.statusbar, saved.text_size);
    }
    if let Some(path) = &app.keymap_path {
        app.keymap = Keymap::load(path);
    }
    // The installer reports updates; the app only shows them (issue #33).
    app.update = upd::check_installed(APP_ID, VERSION);
    let initial = std::sync::Mutex::new(Some(app));
    let builder = iced::application(move || (initial.lock().unwrap_or_else(|e| e.into_inner()).take().expect("the application boots once"), Task::none()), App::update, App::view)
        .title(|app: &App| match app.doc() {
            Some(doc) => format!("{} · OpenAEC Blueprint", doc.title),
            None => "OpenAEC Blueprint".into(),
        })
        .subscription(App::subscription)
        .theme(|app: &App| app.theme.iced())
        .default_font(fonts::BODY);
    fonts::FILES
        .iter()
        .fold(builder, |builder, file| builder.font(*file))
        .window(iced::window::Settings {
            size: Size::new(1280.0, 800.0),
            min_size: Some(Size::new(960.0, 600.0)),
            decorations: false,
            exit_on_close_request: false,
            ..Default::default()
        })
        .run()
}

#[cfg(test)]
mod tests {
    use super::*;
    use openaec_ui::design::a11y::Collect;
    use openaec_ui::iced::advanced::layout::{self, Layout};
    use openaec_ui::iced::advanced::widget::Tree;

    fn accessibility(app: &App) -> Collect {
        let mut element = app.view();
        let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let mut tree = Tree::new(&element);
        let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, Size::new(1280.0, 800.0)));
        let mut found = Collect::default();
        element.as_widget_mut().operate(&mut tree, Layout::new(&node), &renderer, &mut found);
        found
    }

    fn load_fonts() {
        static LOADED: std::sync::Once = std::sync::Once::new();
        LOADED.call_once(|| {
            fonts::install_fallback();
            let mut system = iced_tiny_skia::graphics::text::font_system().write().expect("font system");
            for bytes in fonts::FILES {
                system.load_font(std::borrow::Cow::Borrowed(bytes));
            }
        });
    }

    fn render(app: &App, size: Size) -> tiny_skia::Pixmap {
        use openaec_ui::iced::advanced::renderer;
        use openaec_ui::iced::{mouse, Color, Rectangle};
        load_fonts();
        let mut element = app.view();
        let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
        let mut tree = Tree::new(&element);
        let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
        // A button learns its state from its first event, as the window sends a redraw first.
        let redraw = iced::Event::Window(iced::window::Event::RedrawRequested(Instant::now()));
        let mut messages = Vec::new();
        let mut shell = iced::advanced::Shell::new(&mut messages);
        element.as_widget_mut().update(&mut tree, &redraw, Layout::new(&node), mouse::Cursor::Unavailable, &renderer, &mut iced::advanced::clipboard::Null, &mut shell, &Rectangle::with_size(size));
        let theme = app.theme.iced();
        let style = renderer::Style { text_color: theme.palette().text };
        element.as_widget().draw(&tree, &mut renderer, &theme, &style, Layout::new(&node), mouse::Cursor::Unavailable, &Rectangle::with_size(size));
        let (width, height) = (size.width as u32, size.height as u32);
        let mut bytes = vec![0u8; (width * height * 4) as usize];
        let mut pixels = tiny_skia::PixmapMut::from_bytes(&mut bytes, width, height).expect("pixmap");
        let mut mask = tiny_skia::Mask::new(width, height).expect("mask");
        renderer.draw(&mut pixels, &mut mask, &iced_tiny_skia::graphics::Viewport::with_physical_size(Size::new(width, height), 1.0), &[Rectangle::with_size(size)], Color::from_rgb(1.0, 0.0, 1.0));
        for pixel in bytes.chunks_exact_mut(4) {
            pixel.swap(0, 2);
        }
        tiny_skia::Pixmap::from_vec(bytes, tiny_skia::IntSize::from_wh(width, height).expect("size")).expect("pixels")
    }

    #[test]
    #[ignore = "regenerate the renders in design/blueprint on demand"]
    fn export_renders() {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/blueprint");
        std::fs::create_dir_all(&dir).expect("folder");
        let mut app = App::default();
        let _ = app.update(Msg::EditName("Kade 12".into()));
        app.update = Some(Available { app: APP_ID.into(), current: VERSION.into(), latest: "2026.45.0".into(), page_url: None, installer: None });
        for theme in [ThemeId::Light, ThemeId::Dark, ThemeId::Blueprint, ThemeId::HighContrastDark] {
            app.theme = theme;
            render(&app, Size::new(1280.0, 800.0)).save_png(dir.join(format!("blueprint-{}.png", theme.key()))).expect("png");
        }
        app.theme = ThemeId::Light;
        let _ = app.update(Msg::Backstage(true));
        render(&app, Size::new(1280.0, 800.0)).save_png(dir.join("blueprint-bestand.png")).expect("png");
        let _ = app.update(Msg::Backstage(false));
        let _ = app.update(Msg::Dialog(Some(Dialog::Settings)));
        render(&app, Size::new(1280.0, 800.0)).save_png(dir.join("blueprint-instellingen.png")).expect("png");
        for size in [TextSize::Compact, TextSize::Large] {
            app.text_size = size;
            render(&app, Size::new(1280.0, 800.0)).save_png(dir.join(format!("blueprint-instellingen-{}.png", size.name().to_lowercase()))).expect("png");
        }
    }

    #[test]
    fn no_two_commands_share_a_shortcut() {
        assert!(cm::conflicts(&App::default().commands()).is_empty());
    }

    #[test]
    fn every_control_has_a_name_in_every_view() {
        let mut app = App::default();
        app.update = Some(Available { app: APP_ID.into(), current: VERSION.into(), latest: "2099.1.0".into(), page_url: None, installer: None });
        assert!(accessibility(&app).unnamed.is_empty(), "main screen");
        let _ = app.update(Msg::Backstage(true));
        assert!(accessibility(&app).unnamed.is_empty(), "Bestand");
        let _ = app.update(Msg::Backstage(false));
        let _ = app.update(Msg::Dialog(Some(Dialog::Settings)));
        assert!(accessibility(&app).unnamed.is_empty(), "settings");
        let _ = app.update(Msg::SettingsPage(SettingsPage::Shortcuts));
        assert!(accessibility(&app).unnamed.is_empty(), "shortcuts");
    }

    #[test]
    fn edits_are_undone_per_document_and_closing_asks_first() {
        let mut app = App::default();
        for typed in ["K", "Ka", "Kade 12"] {
            let _ = app.update(Msg::EditName(typed.into()));
        }
        assert_eq!(app.docs[0].title, "Kade 12");
        assert!(app.docs[0].state.is_dirty());
        let _ = app.update(Msg::New);
        let _ = app.update(Msg::Undo);
        assert_eq!(app.docs[0].content.name, "Kade 12", "undo works on the active document only");
        let _ = app.update(Msg::SelectDoc(0));
        assert_eq!(app.command("edit.undo").description(), "Ongedaan maken: Naam wijzigen");
        let _ = app.update(Msg::Undo);
        assert_eq!(app.docs[0].content.name, "Naamloos 1", "typing in one field is one step");
        // Closing the changed document asks; saving it lets the plan finish.
        let _ = app.update(Msg::EditDescription("Woningbouw".into()));
        let _ = app.update(Msg::CloseDoc(0));
        assert_eq!(app.dialog, Some(Dialog::Close));
        let _ = app.update(Msg::CloseChoose(Choice::Save));
        let ticket = app.docs[0].state.writing().expect("a write runs");
        let _ = app.update(Msg::Written(app.docs[0].id, ticket));
        assert_eq!(app.docs.len(), 1, "the saved document closed, the other stays");
        assert!(app.closing.is_none());
    }
}
