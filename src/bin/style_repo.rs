//! Native Rust showcase for the shared OpenAEC desktop UI.
use openaec_ui::{
    fonts,
    iced::{
        self,
        widget::{
            button, column, container, image, row, scrollable, svg, text, text_input, Column, Row,
            Space,
        },
        Alignment, Element, Fill, Task,
    },
    icons::Icon,
    run, widgets, Application, Command, Document, DocumentEvent, Language, RibbonGroup, RibbonTab,
    Theme,
};
use serde::Deserialize;
use std::{path::PathBuf, sync::OnceLock};
#[path = "style_repo/source_icons.rs"]
mod source_icons;
#[path = "style_repo/domain_drafts.rs"]
mod domain_drafts;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Page {
    Overview,
    Components,
    Icons,
    Themes,
    Layouts,
    Studios,
    Fem,
    Bim,
}
impl Page {
    const ALL: [Self; 8] = [
        Self::Overview,
        Self::Components,
        Self::Icons,
        Self::Themes,
        Self::Layouts,
        Self::Studios,
        Self::Fem,
        Self::Bim,
    ];
    fn id(self) -> &'static str {
        match self {
            Self::Overview => "overview",
            Self::Components => "components",
            Self::Icons => "icons",
            Self::Themes => "themes",
            Self::Layouts => "layouts",
            Self::Studios => "studios",
            Self::Fem => "fem",
            Self::Bim => "bim",
        }
    }
    fn title(self, l: Language) -> &'static str {
        match self {
            Self::Overview => l.text("Overzicht", "Overview"),
            Self::Components => l.text("Componenten", "Components"),
            Self::Icons => l.text("Iconen", "Icons"),
            Self::Themes => l.text("Thema's", "Themes"),
            Self::Layouts => l.text("Layouts", "Layouts"),
            Self::Studios => l.text("Alle studio's", "All studios"),
            Self::Fem => "Open FEM Studio",
            Self::Bim => "Open BIM Studio",
        }
    }
    fn icon(self) -> Icon {
        match self {
            Self::Overview => Icon::Cube,
            Self::Components => Icon::Grid,
            Self::Icons => Icon::Search,
            Self::Themes => Icon::Settings,
            Self::Layouts => Icon::PanelLeft,
            Self::Studios => Icon::Cube,
            Self::Fem => Icon::Measure,
            Self::Bim => Icon::Fit,
        }
    }
    fn from_id(id: &str) -> Option<Self> {
        Self::ALL.into_iter().find(|page| page.id() == id)
    }
}

#[derive(Debug, Clone)]
enum Action {
    Show(Page),
    Search(String),
    Previous,
    Next,
    SelectIcon(usize),
    Input(String),
    Toggle,
    Slider(f32),
    Reset,
    SelectStudio(usize),
}

#[derive(Deserialize)]
struct Proposal {
    id: String,
    domain: String,
    group: String,
    label: String,
    visual_metaphor: String,
    name_match_count: usize,
}
#[derive(Deserialize)]
struct StudioLayout {
    name: String,
    tabs: Vec<String>,
    left_panel: String,
    right_panel: String,
    workspace: String,
    notes: String,
}
fn studios() -> &'static [StudioLayout] {
    static DATA: OnceLock<Vec<StudioLayout>> = OnceLock::new();
    DATA.get_or_init(|| {
        serde_json::from_str(include_str!("../../design/app-layouts.json"))
            .expect("valid studio layouts")
    })
}
fn proposals() -> &'static [Proposal] {
    static DATA: OnceLock<Vec<Proposal>> = OnceLock::new();
    DATA.get_or_init(|| {
        serde_json::from_str(include_str!("../../design/domain-icon-proposals.json"))
            .expect("valid design proposals")
    })
}

struct StyleRepo {
    page: Page,
    open_pages: Vec<Page>,
    search: String,
    icon_page: usize,
    selected_icon: Option<usize>,
    sample_input: String,
    sample_toggle: bool,
    sample_value: f32,
    selected_studio: usize,
}
impl Default for StyleRepo {
    fn default() -> Self {
        Self {
            page: Page::Overview,
            open_pages: vec![Page::Overview, Page::Components, Page::Icons],
            search: String::new(),
            icon_page: 0,
            selected_icon: None,
            sample_input: String::new(),
            sample_toggle: false,
            sample_value: 35.0,
            selected_studio: 0,
        }
    }
}
impl StyleRepo {
    fn show(&mut self, page: Page) {
        self.page = page;
        if !self.open_pages.contains(&page) {
            self.open_pages.push(page);
        }
    }
    fn matches(&self) -> Vec<usize> {
        let query = self.search.trim().to_lowercase();
        source_icons::ALL
            .iter()
            .enumerate()
            .filter(|(_, icon)| {
                query.is_empty()
                    || format!("{} {}", icon.repo, icon.path)
                        .to_lowercase()
                        .contains(&query)
            })
            .map(|(i, _)| i)
            .collect()
    }
    fn heading<'a>(
        &self,
        eyebrow: &'static str,
        title: &'static str,
        detail: &'static str,
        theme: Theme,
    ) -> Element<'a, Action> {
        let t = theme.tokens();
        column![
            text(eyebrow).font(fonts::STRONG).size(11).color(t.accent),
            text(title).font(fonts::HEADING).size(31).color(t.text),
            text(detail).size(13).color(t.text_secondary),
        ]
        .spacing(7)
        .into()
    }
    fn card<'a>(&self, body: impl Into<Element<'a, Action>>, theme: Theme) -> Element<'a, Action> {
        let t = theme.tokens();
        container(body)
            .padding(18)
            .width(Fill)
            .style(move |_| container::Style {
                background: Some(t.bg_lighter.into()),
                border: iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 6.0.into(),
                },
                text_color: Some(t.text),
                ..Default::default()
            })
            .into()
    }
    fn nav_card<'a>(
        &self,
        page: Page,
        description: &'static str,
        theme: Theme,
        l: Language,
    ) -> Element<'a, Action> {
        let t = theme.tokens();
        button(
            column![
                page.icon().view(24, t.accent),
                text(page.title(l)).font(fonts::STRONG).size(15),
                text(description).size(12).color(t.text_secondary)
            ]
            .spacing(9),
        )
        .padding(18)
        .width(Fill)
        .on_press(Action::Show(page))
        .style(move |_, s| widgets::button_style(theme, false, s))
        .into()
    }
    fn overview(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let hero = container(column![
            text("OPENAEC  /  STYLE REPO").font(fonts::STRONG).size(11).color(t.accent),
            text(l.text("Eén interface voor elke studio", "One interface for every studio")).font(fonts::HEADING).size(36),
            text(l.text("Een native Rust-bibliotheek voor dezelfde ribbon, panelen, thema's, typografie en iconbetekenis in alle OpenAEC-tools.", "A native Rust library for the same ribbon, panels, themes, typography and icon semantics in every OpenAEC tool.")).size(15),
            row![widgets::action(l.text("Bekijk componenten", "View components"), Icon::Grid, Some(Action::Show(Page::Components)), theme), widgets::action(l.text("Onderzoek iconen", "Explore icons"), Icon::Search, Some(Action::Show(Page::Icons)), theme)].spacing(8),
        ].spacing(16)).padding(28).width(Fill).style(move |_| container::Style::default().background(t.bg_lighter).color(t.text));
        column![
            hero,
            text(l.text("Ontwerpsysteem", "Design system")).font(fonts::HEADING).size(22),
            row![
                self.nav_card(Page::Components, l.text("Native bediening en formulieren", "Native controls and forms"), theme, l),
                self.nav_card(Page::Icons, l.text("Broniconen met UI-bewijs", "Source icons with UI evidence"), theme, l),
                self.nav_card(Page::Themes, l.text("Vijf gedeelde kleurthema's", "Five shared colour themes"), theme, l),
            ].spacing(12),
            row![
                self.nav_card(Page::Layouts, l.text("Vaste regio's en ribbon", "Fixed regions and ribbon"), theme, l),
                self.nav_card(Page::Studios, l.text("18 studio-indelingen", "18 studio layouts"), theme, l),
                self.nav_card(Page::Fem, l.text("Constructieve pictogrammen", "Structural icon proposals"), theme, l),
            ].spacing(12),
            self.card(column![text(l.text("Stand van het ontwerp", "Design status")).font(fonts::STRONG).size(14), text(format!("{} {}", source_icons::ALL.len(), l.text("iconen met UI-bewijs zijn onderzoeksbronnen. Definitieve semantische iconen volgen na beoordeling.", "icons with UI evidence are research sources. Final semantic icons follow review."))).size(12)].spacing(7), theme),
        ].spacing(18).into()
    }
    fn components(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        column![
            self.heading(
                "UI PRIMITIVES",
                l.text("Componenten", "Components"),
                l.text(
                    "Dezelfde bediening in iedere OpenAEC-app.",
                    "The same controls in every OpenAEC app."
                ),
                theme
            ),
            self.card(
                column![
                    text(l.text("Acties", "Actions"))
                        .font(fonts::STRONG)
                        .size(16),
                    row![
                        widgets::action(
                            l.text("Primair", "Primary"),
                            Icon::Check,
                            Some(Action::Toggle),
                            theme
                        ),
                        widgets::action(
                            l.text("Secundair", "Secondary"),
                            Icon::Open,
                            Some(Action::Show(Page::Layouts)),
                            theme
                        ),
                        widgets::action(
                            l.text("Uitgeschakeld", "Disabled"),
                            Icon::Save,
                            None::<Action>,
                            theme
                        )
                    ]
                    .spacing(10),
                    text(l.text(
                        "Primair wijzigt de voorbeeldschakelaar; secundair opent Layouts.",
                        "Primary toggles the sample switch; secondary opens Layouts."
                    ))
                    .size(12)
                    .color(t.text_secondary),
                ]
                .spacing(13),
                theme
            ),
            self.card(
                column![
                    text(l.text("Formulier", "Form"))
                        .font(fonts::STRONG)
                        .size(16),
                    text(l.text("Projectnaam", "Project name")).size(12),
                    text_input(l.text("Typ een naam", "Type a name"), &self.sample_input)
                        .on_input(Action::Input)
                        .width(360),
                    row![
                        widgets::action(
                            if self.sample_toggle {
                                l.text("Aan", "On")
                            } else {
                                l.text("Uit", "Off")
                            },
                            Icon::Check,
                            Some(Action::Toggle),
                            theme
                        ),
                        text(format!(
                            "{}: {:.0}%",
                            l.text("Waarde", "Value"),
                            self.sample_value
                        ))
                        .size(12)
                    ]
                    .spacing(14)
                    .align_y(Alignment::Center),
                    iced::widget::slider(0.0..=100.0, self.sample_value, Action::Slider).width(360),
                    widgets::action(
                        l.text("Voorbeeld resetten", "Reset sample"),
                        Icon::Undo,
                        Some(Action::Reset),
                        theme
                    ),
                ]
                .spacing(12),
                theme
            ),
            self.card(
                column![
                    text(l.text("Eigenschappen", "Properties"))
                        .font(fonts::STRONG)
                        .size(16),
                    widgets::property(
                        l.text("Naam", "Name"),
                        if self.sample_input.is_empty() {
                            "—"
                        } else {
                            &self.sample_input
                        },
                        theme
                    ),
                    widgets::property(
                        l.text("Status", "Status"),
                        if self.sample_toggle {
                            l.text("Actief", "Active")
                        } else {
                            l.text("Inactief", "Inactive")
                        },
                        theme
                    ),
                    widgets::property(
                        l.text("Schaal", "Scale"),
                        format!("{:.0}%", self.sample_value),
                        theme
                    ),
                ]
                .spacing(12),
                theme
            ),
        ]
        .spacing(18)
        .into()
    }
    fn icons(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let matches = self.matches();
        let pages = matches.len().max(1).div_ceil(48);
        let page = self.icon_page.min(pages - 1);
        let mut grid = Column::new().spacing(10);
        for chunk in matches[page * 48..(page * 48 + 48).min(matches.len())].chunks(3) {
            let mut row = Row::new().spacing(10);
            for &index in chunk {
                let icon = &source_icons::ALL[index];
                let preview: Element<'_, Action> = if icon.is_svg {
                    svg(svg::Handle::from_memory(icon.bytes))
                        .width(34)
                        .height(34)
                        .into()
                } else {
                    image(image::Handle::from_bytes(icon.bytes))
                        .width(34)
                        .height(34)
                        .into()
                };
                let selected = self.selected_icon == Some(index);
                let name = icon.name.to_string();
                row = row.push(
                    button(
                        column![
                            container(preview).height(48).center_x(Fill),
                            text(name).size(11)
                        ]
                        .spacing(6)
                        .align_x(Alignment::Center),
                    )
                    .padding(10)
                    .width(100)
                    .on_press(Action::SelectIcon(index))
                    .style(move |_, s| widgets::button_style(theme, selected, s)),
                );
            }
            grid = grid.push(row);
        }
        let details: Element<'_, Action> = if let Some(i) = self.selected_icon {
            let icon = &source_icons::ALL[i];
            self.card(
                column![
                    text(icon.name).font(fonts::HEADING).size(19),
                    widgets::property("Repository", icon.repo, theme),
                    widgets::property("Pad", icon.path, theme),
                    text(l.text(
                        "Onderzoeksbron; nog niet gekozen als canoniek icoon.",
                        "Research source; not yet selected as a canonical icon."
                    ))
                    .size(12)
                    .color(t.text_secondary)
                ]
                .spacing(10),
                theme,
            )
        } else {
            self.card(
                text(l.text(
                    "Selecteer een icoon voor brongegevens.",
                    "Select an icon for source details.",
                ))
                .size(12),
                theme,
            )
        };
        column![
            self.heading(
                "ICON RESEARCH",
                l.text("UI-iconen met bronbewijs", "UI icons with source evidence"),
                l.text(
                    "Alle onderzochte bronbestanden zijn ingebed in deze native app.",
                    "All researched source files are embedded in this native app."
                ),
                theme
            ),
            row![
                text_input(
                    l.text(
                        "Zoek op naam, pad of repository",
                        "Search name, path or repository"
                    ),
                    &self.search
                )
                .on_input(Action::Search)
                .width(360),
                text(format!(
                    "{} {}",
                    matches.len(),
                    l.text("resultaten", "results")
                ))
                .size(12)
                .color(t.text_secondary)
            ]
            .spacing(14)
            .align_y(Alignment::Center),
            row![
                widgets::action(
                    l.text("Vorige", "Previous"),
                    Icon::Back,
                    (page > 0).then_some(Action::Previous),
                    theme
                ),
                text(format!("{} / {}", page + 1, pages)).size(12),
                widgets::action(
                    l.text("Volgende", "Next"),
                    Icon::Redo,
                    (page + 1 < pages).then_some(Action::Next),
                    theme
                )
            ]
            .spacing(12)
            .align_y(Alignment::Center),
            grid,
            details,
        ]
        .spacing(16)
        .into()
    }
    fn themes(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let mut items = Column::new().spacing(12);
        for candidate in Theme::ALL {
            let t = candidate.tokens();
            let swatch = container(
                row![
                    container(Space::new(30, 30))
                        .style(move |_| container::Style::default().background(t.bg)),
                    container(Space::new(30, 30))
                        .style(move |_| container::Style::default().background(t.bg_lighter)),
                    container(Space::new(30, 30))
                        .style(move |_| container::Style::default().background(t.accent)),
                    container(Space::new(30, 30))
                        .style(move |_| container::Style::default().background(t.status_bg)),
                ]
                .spacing(6),
            );
            items = items.push(
                self.card(
                    row![
                        column![
                            text(candidate.to_string()).font(fonts::STRONG).size(16),
                            text(if candidate == theme {
                                l.text("Actief thema", "Active theme")
                            } else {
                                l.text("Beschikbaar in Instellingen", "Available in Settings")
                            })
                            .size(12)
                        ]
                        .spacing(6)
                        .width(Fill),
                        swatch
                    ]
                    .align_y(Alignment::Center),
                    theme,
                ),
            );
        }
        column![
            self.heading(
                "DESIGN TOKENS",
                l.text("Thema's", "Themes"),
                l.text(
                    "Open Instellingen in de titelbalk om live van thema te wisselen.",
                    "Open Settings in the title bar to switch themes live."
                ),
                theme
            ),
            items
        ]
        .spacing(18)
        .into()
    }
    fn layouts(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let regions = [
            (
                "01",
                l.text("Titel & snelle acties", "Title & quick actions"),
                "32 px",
            ),
            ("02", l.text("Ribbon-tabs", "Ribbon tabs"), "34 px"),
            ("03", "Ribbon", "100 px"),
            ("04", l.text("Documenttabs", "Document tabs"), "32 px"),
            (
                "05",
                l.text(
                    "Verkenner · Werkgebied · Eigenschappen",
                    "Explorer · Workspace · Properties",
                ),
                l.text("Schaalbaar", "Resizable"),
            ),
            ("06", l.text("Status", "Status"), "26 px"),
        ];
        let mut list = Column::new().spacing(10);
        for (number, name, size) in regions {
            list = list.push(
                self.card(
                    row![
                        text(number)
                            .font(fonts::MONO)
                            .size(12)
                            .color(theme.tokens().accent),
                        text(name).font(fonts::STRONG).size(13).width(Fill),
                        text(size).size(12).color(theme.tokens().text_secondary)
                    ]
                    .spacing(16),
                    theme,
                ),
            );
        }
        column![self.heading("APPLICATION SHELL", l.text("Gedeelde layout", "Shared layout"), l.text("Deze regio's worden door de crate bepaald. Applicaties leveren hun eigen commando's en inhoud.", "The crate defines these regions. Applications supply their commands and content."),theme),list].spacing(18).into()
    }
    fn studios_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let selected = &studios()[self.selected_studio];
        let mut list = Column::new().spacing(5).width(220);
        for (index, studio) in studios().iter().enumerate() {
            list = list.push(
                button(text(&studio.name).size(12))
                    .padding(9)
                    .width(Fill)
                    .on_press(Action::SelectStudio(index))
                    .style(move |_, state| {
                        widgets::button_style(theme, index == self.selected_studio, state)
                    }),
            );
        }
        let mut tabs = Row::new().spacing(5);
        for tab in &selected.tabs {
            tabs = tabs.push(
                container(text(tab).size(11).color(t.text))
                    .padding(8)
                    .style(move |_| container::Style::default().background(t.bg_lighter)),
            );
        }
        let detail = column![
            text(&selected.name)
                .font(fonts::HEADING)
                .size(27)
                .color(t.text),
            text(l.text("Voorgestelde ribbon-tabs", "Proposed ribbon tabs"))
                .font(fonts::STRONG)
                .size(11)
                .color(t.accent),
            tabs,
            self.card(
                column![
                    text(l.text("Gedeelde schermindeling", "Shared screen layout"))
                        .font(fonts::STRONG)
                        .size(14),
                    widgets::property(l.text("Links", "Left"), &selected.left_panel, theme),
                    widgets::property(
                        l.text("Werkgebied", "Workspace"),
                        &selected.workspace,
                        theme
                    ),
                    widgets::property(l.text("Rechts", "Right"), &selected.right_panel, theme),
                ]
                .spacing(14),
                theme
            ),
            text(&selected.notes).size(12).color(t.text_secondary),
        ]
        .spacing(16)
        .width(Fill);
        column![
            self.heading("STUDIO ATLAS", l.text("Alle studio's", "All studios"),
                l.text("Achttien applicatie-indelingen op dezelfde shell. Selecteer een studio om de ribbon en panelen te vergelijken.",
                       "Eighteen application layouts on one shell. Select a studio to compare its ribbon and panels."), theme),
            row![list, detail].spacing(24).width(Fill),
        ].spacing(22).into()
    }
    fn domains(&self, theme: Theme, l: Language, domain: &'static str) -> Element<'_, Action> {
        let title = if domain == "fem" {
            "Open FEM Studio"
        } else {
            "Open BIM Studio"
        };
        let count = proposals().iter().filter(|p| p.domain == domain).count();
        let mut list = Column::new().spacing(10);
        for proposal in proposals().iter().filter(|p| p.domain == domain) {
            let preview = svg(svg::Handle::from_memory(
                domain_drafts::get(&proposal.id).expect("draft for every proposal"),
            ))
            .width(32)
            .height(32)
            .style(move |_, _| svg::Style {
                color: Some(theme.tokens().text),
            });
            list = list.push(
                self.card(
                    row![
                        container(preview).width(46).center_x(Fill),
                        column![
                            text(&proposal.label).font(fonts::STRONG).size(14),
                            text(&proposal.visual_metaphor)
                                .size(12)
                                .color(theme.tokens().text_secondary)
                        ]
                        .spacing(4)
                        .width(Fill),
                        column![
                            text(&proposal.group).size(11).color(theme.tokens().accent),
                            text(format!(
                                "{} {}",
                                proposal.name_match_count,
                                l.text("naamkandidaten", "name candidates")
                            ))
                            .size(11)
                        ]
                        .spacing(4),
                    ]
                    .spacing(18),
                    theme,
                ),
            );
        }
        column![self.heading("DOMAIN ICONS",title,l.text("Vectorconcepten voor visuele beoordeling; nog niet vrijgegeven voor de gedeelde crate.", "Vector concepts for visual review; not yet released in the shared crate."),theme),text(format!("{} {}",count,l.text("iconconcepten", "icon concepts"))).size(12).color(theme.tokens().text_secondary),list].spacing(16).into()
    }
}

impl Application for StyleRepo {
    type Command = Action;
    fn title(&self) -> String {
        "OpenAEC Style Repo  ·  Rust".into()
    }
    fn ribbon(&self, l: Language) -> Vec<RibbonTab<Action>> {
        vec![
            RibbonTab {
                id: "start".into(),
                label: l.text("Start", "Home").into(),
                groups: vec![
                    RibbonGroup {
                        label: l.text("Bibliotheek", "Library").into(),
                        commands: vec![
                            Command::new(
                                l.text("Overzicht", "Overview"),
                                Icon::Cube,
                                Action::Show(Page::Overview),
                            )
                            .selected(self.page == Page::Overview),
                            Command::new(
                                l.text("Componenten", "Components"),
                                Icon::Grid,
                                Action::Show(Page::Components),
                            )
                            .selected(self.page == Page::Components),
                            Command::new(
                                l.text("Iconen", "Icons"),
                                Icon::Search,
                                Action::Show(Page::Icons),
                            )
                            .selected(self.page == Page::Icons),
                        ],
                    },
                    RibbonGroup {
                        label: l.text("Vormgeving", "Appearance").into(),
                        commands: vec![
                            Command::new(
                                l.text("Thema's", "Themes"),
                                Icon::Settings,
                                Action::Show(Page::Themes),
                            )
                            .selected(self.page == Page::Themes),
                            Command::new("Layouts", Icon::PanelLeft, Action::Show(Page::Layouts))
                                .selected(self.page == Page::Layouts),
                            Command::new(
                                l.text("Studio's", "Studios"),
                                Icon::Cube,
                                Action::Show(Page::Studios),
                            )
                            .selected(self.page == Page::Studios),
                        ],
                    },
                ],
            },
            RibbonTab {
                id: "domains".into(),
                label: l.text("Domeinen", "Domains").into(),
                groups: vec![
                    RibbonGroup {
                        label: l.text("Studio's", "Studios").into(),
                        commands: vec![
                            Command::new("Open FEM", Icon::Measure, Action::Show(Page::Fem))
                                .selected(self.page == Page::Fem),
                            Command::new("Open BIM", Icon::Fit, Action::Show(Page::Bim))
                                .selected(self.page == Page::Bim),
                        ],
                    },
                    RibbonGroup {
                        label: l.text("Onderzoek", "Research").into(),
                        commands: vec![Command::new(
                            l.text("UI-iconen", "UI icons"),
                            Icon::Grid,
                            Action::Show(Page::Icons),
                        )],
                    },
                ],
            },
        ]
    }
    fn quick_commands(&self, l: Language) -> Vec<Command<Action>> {
        vec![
            Command::new(
                l.text("Overzicht", "Overview"),
                Icon::Cube,
                Action::Show(Page::Overview),
            ),
            Command::new(
                l.text("Componenten", "Components"),
                Icon::Grid,
                Action::Show(Page::Components),
            ),
            Command::new(
                l.text("Iconen", "Icons"),
                Icon::Search,
                Action::Show(Page::Icons),
            ),
        ]
    }
    fn file_commands(&self, l: Language) -> Vec<Command<Action>> {
        Page::ALL
            .iter()
            .map(|&page| Command::new(page.title(l), page.icon(), Action::Show(page)))
            .collect()
    }
    fn workspace(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let content = match self.page {
            Page::Overview => self.overview(theme, l),
            Page::Components => self.components(theme, l),
            Page::Icons => self.icons(theme, l),
            Page::Themes => self.themes(theme, l),
            Page::Layouts => self.layouts(theme, l),
            Page::Studios => self.studios_page(theme, l),
            Page::Fem => self.domains(theme, l, "fem"),
            Page::Bim => self.domains(theme, l, "bim"),
        };
        let bg = theme.tokens().content_bg;
        container(scrollable(container(content).padding(28).width(Fill)).height(Fill))
            .width(Fill)
            .height(Fill)
            .style(move |_| container::Style::default().background(bg))
            .into()
    }
    fn explorer(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let mut nav = Column::new().spacing(5);
        for page in Page::ALL {
            let selected = self.page == page;
            nav = nav.push(
                button(
                    row![
                        page.icon().view(16, theme.tokens().accent),
                        text(page.title(l)).size(12)
                    ]
                    .spacing(9)
                    .align_y(Alignment::Center),
                )
                .padding(8)
                .width(Fill)
                .on_press(Action::Show(page))
                .style(move |_, s| widgets::button_style(theme, selected, s)),
            );
        }
        nav.into()
    }
    fn properties(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        column![
            widgets::property(l.text("Pagina", "Page"), self.page.title(l), theme),
            widgets::property(l.text("Thema", "Theme"), theme.to_string(), theme),
            widgets::property(
                l.text("Canonieke iconen", "Canonical icons"),
                Icon::ALL.len().to_string(),
                theme
            ),
            widgets::property(
                l.text("UI-broniconen", "UI source icons"),
                source_icons::ALL.len().to_string(),
                theme
            ),
            widgets::property(
                l.text("FEM/BIM-voorstellen", "FEM/BIM proposals"),
                proposals().len().to_string(),
                theme
            ),
        ]
        .spacing(14)
        .into()
    }
    fn update(&mut self, action: Action) -> Task<Action> {
        match action {
            Action::Show(page) => self.show(page),
            Action::Search(query) => {
                self.search = query;
                self.icon_page = 0;
                self.selected_icon = None
            }
            Action::Previous => self.icon_page = self.icon_page.saturating_sub(1),
            Action::Next => self.icon_page += 1,
            Action::SelectIcon(index) => self.selected_icon = Some(index),
            Action::Input(value) => self.sample_input = value,
            Action::Toggle => self.sample_toggle = !self.sample_toggle,
            Action::Slider(value) => self.sample_value = value,
            Action::Reset => {
                self.sample_input.clear();
                self.sample_toggle = false;
                self.sample_value = 35.0;
            }
            Action::SelectStudio(index) => {
                self.selected_studio = index.min(studios().len().saturating_sub(1));
                self.show(Page::Studios);
            }
        }
        Task::none()
    }
    fn documents(&self) -> Vec<Document> {
        self.open_pages
            .iter()
            .map(|p| Document {
                id: p.id().into(),
                title: p.title(Language::Dutch).into(),
                dirty: false,
            })
            .collect()
    }
    fn active_document(&self) -> Option<String> {
        Some(self.page.id().into())
    }
    fn document_event(&mut self, event: DocumentEvent) -> Task<Action> {
        match event {
            DocumentEvent::Activate(id) => {
                if let Some(page) = Page::from_id(&id) {
                    self.show(page)
                }
            }
            DocumentEvent::CloseRequested(id) => {
                self.open_pages.retain(|p| p.id() != id);
                if self.page.id() == id {
                    self.page = self.open_pages.last().copied().unwrap_or(Page::Overview)
                }
            }
        }
        Task::none()
    }
    fn status(&self, l: Language) -> String {
        format!(
            "{}  ·  {} UI-iconen  ·  109 FEM/BIM-voorstellen",
            self.page.title(l),
            source_icons::ALL.len()
        )
    }
}

fn preferences_path() -> Option<PathBuf> {
    let base = std::env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .or_else(|| std::env::var_os("HOME").map(|home| PathBuf::from(home).join(".config")))?;
    Some(base.join("openaec").join("style-repo.json"))
}
fn main() -> iced::Result {
    run(StyleRepo::default(), preferences_path())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;

    #[test]
    fn research_catalog_is_complete_and_unique() {
        assert!(source_icons::ALL.len() >= 565);
        assert!(source_icons::ALL.iter().all(|icon| !icon.bytes.is_empty()));
        let keys: HashSet<_> = source_icons::ALL
            .iter()
            .map(|icon| (icon.repo, icon.path))
            .collect();
        assert_eq!(keys.len(), source_icons::ALL.len());
        assert_eq!(proposals().len(), 109);
        assert!(proposals().iter().any(|proposal| proposal.domain == "fem"));
        assert!(proposals().iter().any(|proposal| proposal.domain == "bim"));
        assert_eq!(domain_drafts::ALL.len(), proposals().len());
        assert!(proposals()
            .iter()
            .all(|proposal| domain_drafts::get(&proposal.id).is_some()));
    }
}
