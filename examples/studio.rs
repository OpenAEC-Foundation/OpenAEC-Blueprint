//! A consuming application: no copied shell code, CSS, JavaScript or Tauri.
use openaec_ui::{
    find_bar::{self, FindBarActions, FindBarState, ResultGroup},
    iced::{
        self,
        widget::{column, container, row, text, text_input, Space},
        Element, Fill, Task,
    },
    icons::Icon,
    *,
};

#[derive(Debug, Clone)]
enum Action {
    New,
    Rename(String),
    Save,
    SelectIcons,
    SelectWorkspace,
    SelectFind,
    Query(String),
    Previous,
    Next,
    MatchCase,
    WholeWord,
    HighlightAll,
    SearchText,
    SearchAnnotations,
    Results,
    Page(usize),
    CloseFind,
    NarrowFind,
}
struct Studio {
    documents: Vec<Document>,
    active: Option<String>,
    next_id: u64,
    show_icons: bool,
    show_find: bool,
    narrow_find: bool,
    find: FindBarState,
    pending_close: Option<String>,
}
impl Default for Studio {
    fn default() -> Self {
        Self {
            documents: Vec::new(),
            active: None,
            next_id: 0,
            show_icons: false,
            show_find: false,
            narrow_find: false,
            find: FindBarState {
                search_text: true,
                search_annotations: true,
                highlight_all: true,
                ..FindBarState::default()
            },
            pending_close: None,
        }
    }
}
impl Studio {
    fn active(&self) -> Option<&Document> {
        self.documents
            .iter()
            .find(|d| Some(&d.id) == self.active.as_ref())
    }
    fn refresh_find_results(&mut self) {
        self.find.groups.clear();
        let query = self.find.query.to_lowercase();
        if query.contains("construct") || query.contains("struct") {
            if self.find.search_text {
                self.find.groups.push(ResultGroup {
                    page: 2,
                    count: 4,
                    kinds: "Tekst".into(),
                    current: true,
                });
            }
            if self.find.search_annotations {
                self.find.groups.push(ResultGroup {
                    page: 5,
                    count: 3,
                    kinds: "Annotaties".into(),
                    current: !self.find.search_text,
                });
            }
        }
        self.find.total = self.find.groups.iter().map(|group| group.count).sum();
        self.find.current = usize::from(self.find.total > 0);
    }
}
impl Application for Studio {
    type Command = Action;
    fn title(&self) -> String {
        "OpenAEC Studio · UI Library".into()
    }
    fn ribbon(&self, l: Language) -> Vec<RibbonTab<Action>> {
        vec![RibbonTab {
            id: "home".into(),
            label: l.text("Start", "Home").into(),
            groups: vec![
                RibbonGroup {
                    label: l.text("Document", "Document").into(),
                    commands: vec![
                        Command::new(l.text("Nieuw", "New"), Icon::New, Action::New),
                        Command::new(
                            l.text("Opslaan (demo)", "Save (demo)"),
                            Icon::Save,
                            Action::Save,
                        )
                        .enabled(self.active().is_some_and(|d| d.dirty)),
                    ],
                },
                RibbonGroup {
                    label: l.text("Bibliotheek", "Library").into(),
                    commands: vec![
                        Command::new(
                            l.text("Werkruimte", "Workspace"),
                            Icon::Cube,
                            Action::SelectWorkspace,
                        )
                        .selected(!self.show_icons),
                        Command::new(l.text("Iconen", "Icons"), Icon::Grid, Action::SelectIcons)
                            .selected(self.show_icons),
                        Command::new(
                            l.text("Zoekbalk", "Find bar"),
                            Icon::Search,
                            Action::SelectFind,
                        )
                        .selected(self.show_find),
                    ],
                },
            ],
        }]
    }
    fn workspace(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        if self.show_find {
            let width = if self.narrow_find { 300.0 } else { 620.0 };
            let actions = FindBarActions {
                query_changed: Action::Query,
                previous: Action::Previous,
                next: Action::Next,
                toggle_match_case: Action::MatchCase,
                toggle_whole_word: Action::WholeWord,
                toggle_highlight_all: Action::HighlightAll,
                toggle_text: Action::SearchText,
                toggle_annotations: Action::SearchAnnotations,
                toggle_results: Action::Results,
                select_page: Action::Page,
                close: Action::CloseFind,
            };
            let bar = find_bar::view(&self.find, actions, theme, l, width);
            let toggle = iced::widget::button(text(if self.narrow_find {
                l.text("Breed vlak", "Wide canvas")
            } else {
                l.text("Smal vlak", "Narrow canvas")
            }))
            .on_press(Action::NarrowFind)
            .style(move |_, status| widgets::secondary_button_style(theme, status));
            let page = container(
                column![
                    row![Space::new().width(Fill).height(1), bar].width(Fill),
                    Space::new().width(Fill).height(24),
                    text(l.text("Voorbeeld document", "Sample document"))
                        .size(21)
                        .font(fonts::HEADING),
                    text(l.text(
                        "Zoek naar constructie om de resultatenlijst te bekijken.",
                        "Search for structure to inspect the results list."
                    ))
                    .size(12),
                ]
                .spacing(8),
            )
            .width(width)
            .height(350)
            .padding([4, 12])
            .style(move |_| container::Style::default().background(theme.tokens().content_bg));
            return container(column![
                text(l.text("PDF · native zoekbalk", "PDF · native find bar")).font(fonts::HEADING).size(24),
                text(l.text("Bronmaten en vijf gecontroleerde UI-iconen · smalle breedte apart te bekijken", "Source dimensions and five verified UI icons · inspect narrow width separately")).size(12),
                toggle, page,
            ].spacing(15)).padding(28).into();
        }
        if self.show_icons {
            let mut rows = column![text(l.text("Centrale iconen", "Canonical icons"))
                .font(fonts::HEADING)
                .size(28)]
            .spacing(16);
            for chunk in Icon::ALL.chunks(5) {
                let mut row = iced::widget::Row::new().spacing(24);
                for icon in chunk {
                    row = row.push(
                        column![
                            icon.view(24, theme.tokens().text),
                            text(format!("{icon:?}")).size(11)
                        ]
                        .spacing(8)
                        .width(100)
                        .align_x(iced::Alignment::Center),
                    );
                }
                rows = rows.push(row);
            }
            return iced::widget::scrollable(iced::widget::container(rows).padding(32)).into();
        }
        match self.active() {
            None => widgets::empty_state(
                l.text("Bouw samen. Bouw open.", "Build together. Build open."),
                l.text(
                    "Maak een document om de gedeelde UI te bekijken.",
                    "Create a document to explore the shared UI.",
                ),
                theme,
            ),
            Some(doc) => iced::widget::container(
                column![
                    text(l.text("Werkruimte", "Workspace"))
                        .font(fonts::HEADING)
                        .size(28),
                    text(l.text("Documentnaam", "Document name")).size(13),
                    text_input(l.text("Naam", "Name"), &doc.title).on_input(Action::Rename),
                    text(l.text(
                        "Deze demo bewaart documenten alleen in het geheugen.",
                        "This demo keeps documents in memory only."
                    ))
                    .size(12),
                    text(if self.pending_close.is_some() {
                        l.text(
                            "Sla het document op voordat je het sluit.",
                            "Save the document before closing it.",
                        )
                    } else {
                        ""
                    })
                    .color(theme.tokens().danger_color),
                ]
                .spacing(16)
                .max_width(600),
            )
            .padding(32)
            .into(),
        }
    }
    fn explorer(&self, theme: Theme, _l: Language) -> Element<'_, Action> {
        let mut list = column![].spacing(8);
        for doc in &self.documents {
            list = list.push(widgets::property(
                doc.title.clone(),
                if doc.dirty { "•" } else { "" },
                theme,
            ));
        }
        list.into()
    }
    fn properties(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        column![
            widgets::property(
                l.text("Documenten", "Documents"),
                self.documents.len().to_string(),
                theme
            ),
            widgets::property(l.text("Thema", "Theme"), theme.to_string(), theme)
        ]
        .spacing(12)
        .into()
    }
    fn update(&mut self, action: Action) -> Task<Action> {
        match action {
            Action::New => {
                self.next_id += 1;
                let id = self.next_id.to_string();
                self.documents.push(Document {
                    id: id.clone(),
                    title: format!("Document {}", self.next_id),
                    dirty: false,
                });
                self.active = Some(id);
                self.show_icons = false;
            }
            Action::Rename(title) => {
                if let Some(doc) = self
                    .documents
                    .iter_mut()
                    .find(|d| Some(&d.id) == self.active.as_ref())
                {
                    doc.title = title;
                    doc.dirty = true;
                }
            }
            Action::Save => {
                if let Some(doc) = self
                    .documents
                    .iter_mut()
                    .find(|d| Some(&d.id) == self.active.as_ref())
                {
                    doc.dirty = false;
                }
                self.pending_close = None;
            }
            Action::SelectIcons => {
                self.show_icons = true;
                self.show_find = false;
            }
            Action::SelectWorkspace => {
                self.show_icons = false;
                self.show_find = false;
            }
            Action::SelectFind => {
                self.show_find = true;
                self.show_icons = false;
            }
            Action::Query(query) => {
                self.find.query = query;
                self.refresh_find_results();
            }
            Action::Previous => {
                if self.find.total > 0 {
                    self.find.current = if self.find.current <= 1 {
                        self.find.total
                    } else {
                        self.find.current - 1
                    };
                }
            }
            Action::Next => {
                if self.find.total > 0 {
                    self.find.current = self.find.current % self.find.total + 1;
                }
            }
            Action::MatchCase => self.find.match_case = !self.find.match_case,
            Action::WholeWord => self.find.whole_word = !self.find.whole_word,
            Action::HighlightAll => self.find.highlight_all = !self.find.highlight_all,
            Action::SearchText => {
                self.find.search_text = !self.find.search_text;
                self.refresh_find_results();
            }
            Action::SearchAnnotations => {
                self.find.search_annotations = !self.find.search_annotations;
                self.refresh_find_results();
            }
            Action::Results => self.find.results_open = !self.find.results_open,
            Action::Page(page) => {
                for group in &mut self.find.groups {
                    group.current = group.page == page;
                }
            }
            Action::CloseFind => self.show_find = false,
            Action::NarrowFind => self.narrow_find = !self.narrow_find,
        }
        Task::none()
    }
    fn documents(&self) -> Vec<Document> {
        self.documents.clone()
    }
    fn active_document(&self) -> Option<String> {
        self.active.clone()
    }
    fn file_commands(&self, l: Language) -> Vec<Command<Action>> {
        self.ribbon(l).remove(0).groups.remove(0).commands
    }
    fn document_event(&mut self, event: DocumentEvent) -> Task<Action> {
        match event {
            DocumentEvent::Activate(id) => {
                self.active = Some(id);
                self.show_icons = false;
            }
            DocumentEvent::CloseRequested(id) => {
                if self.documents.iter().any(|d| d.id == id && d.dirty) {
                    self.pending_close = Some(id.clone());
                    self.active = Some(id);
                    self.show_icons = false;
                } else {
                    self.documents.retain(|d| d.id != id);
                    if self.active.as_ref() == Some(&id) {
                        self.active = self.documents.last().map(|d| d.id.clone());
                    }
                }
            }
        }
        Task::none()
    }
    fn close_requested(&mut self) -> bool {
        if let Some(doc) = self.documents.iter().find(|d| d.dirty) {
            self.active = Some(doc.id.clone());
            self.pending_close = Some(doc.id.clone());
            self.show_icons = false;
            false
        } else {
            true
        }
    }
}
fn main() -> iced::Result {
    run(Studio::default(), None)
}
