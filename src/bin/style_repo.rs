//! Native Rust showcase for the shared OpenAEC desktop UI.
use openaec_ui::{
    fonts,
    iced::{
        self,
        widget::{
            button, column, container, image, pick_list, progress_bar, row, scrollable, svg, text, text_input,
            Column, Row, Space,
        },
        Alignment, Element, Fill, Task,
    },
    icons::{DomainIcon, Icon},
    model::metrics,
    run, widgets, Application, ChromeMode, Command, CommandIcon, Document, DocumentEvent, Language, RibbonControl, RibbonGroup, RibbonSlider, RibbonTab,
    Theme,
};
use serde::Deserialize;
use std::{path::PathBuf, sync::OnceLock};
#[path = "style_repo/domain_drafts.rs"]
mod domain_drafts;
#[path = "style_repo/energy_workflow.rs"]
mod energy_workflow;
#[path = "style_repo/field_remaining.rs"]
mod field_remaining;
#[path = "style_repo/geotech_native.rs"]
mod geotech_native;
#[path = "style_repo/speech_native.rs"]
mod speech_native;
#[path = "style_repo/speech_more.rs"]
mod speech_more;
#[path = "style_repo/ribbon_preview.rs"]
mod ribbon_preview;
#[cfg(test)]
#[path = "style_repo/render_tests.rs"]
mod render_tests;
#[path = "style_repo/source_icons.rs"]
mod source_icons;
use energy_workflow::EnergyMode;

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
    SampleDialog(bool),
    SampleDialogInput(String),
    SampleDialogSave,
    SelectStudio(usize),
    SelectScreen(usize),
    GeotechLayer(usize),
    FieldProjectEdit(usize, String),
    FieldProjectPreview(&'static str),
    FieldConnectorPreview(&'static str),
    FieldExportType(usize),
    FieldExportPhotos(bool),
    FieldExportMap(bool),
    FieldExportPreview(&'static str),
    FieldFlowSetup(&'static str),
    FieldFlowCancel,
    FieldFlowEdit(bool, usize, String),
    FieldFlowType(bool, usize),
    FieldFlowPreview(&'static str),
    FieldReviewPreview(&'static str),
    FieldCaptureFilter(usize, usize),
    SpeechPreview(&'static str),
    SpeechDictionaryEdit(bool, String),
    SpeechDictionaryAdd,
    SpeechSettingsTab(usize),
    SpeechTtsInput(String),
    SpeechTtsSpeed(f32),
    SelectPreviewCommand(String),
    PileSymbolScale(f32),
    PileUtilizationMinimum(f32),
    PileUtilizationMaximum(f32),
    PileForeground(usize),
    FrameTemplate(usize),
    FrameLod(usize),
    FrameTheme(usize),
    PdfCrop,
    PdfGrayscale,
    PdfBrightness(f32),
    PdfContrast(f32),
    PdfResetImage,
    PdfAlignTarget(usize),
    PdfFormatStyle(usize),
    PdfFormatToggleGallery,
    PdfFormatCloseGallery,
    PdfFormatFill(usize),
    PdfFormatNoFill,
    PdfFormatStroke(usize),
    PdfFormatCustomToggle,
    PdfFormatCustomHex(String),
    PdfFormatCustomApply,
    PdfFormatLineWidth(String),
    PdfFormatBorder(usize),
    PdfFormatBlend(usize),
    PdfFormatOpacity(f32),
    PdfFormatOpacityText(String),
    PdfFormatArrowStart(usize),
    PdfFormatArrowEnd(usize),
    PdfFormatLayer(usize),
    PdfFormatSymbolStamp,
    PdfFormatTogglePalette(usize),
    PdfFormatClosePalette,
    SelectEnergyStep(usize),
    SelectEnergySub(usize),
    SelectEnergyMode(EnergyMode),
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
    id: String,
    name: String,
    tabs: Vec<String>,
    #[serde(default)]
    optional_tabs: Vec<String>,
    left_panel: String,
    right_panel: String,
    workspace: String,
    screens: Vec<String>,
    notes: String,
}
struct FieldProjectState {
    values: [String; 11],
    notice: Option<&'static str>,
}
impl Default for FieldProjectState {
    fn default() -> Self {
        Self { values: ["Renovatie Damrak 1", "DAM-2026-001", "BouwCo BV", "Jan Jansen",
            "Damrak 1", "1012LG", "Amsterdam", "30-07-2026", "Martijn de Vries", "", ""]
            .map(str::to_owned), notice: None }
    }
}
fn screen_label(id: &str, l: Language) -> &'static str {
    match id {
        "start" => l.text("Start", "Start"),
        "workspace" => l.text("Werkgebied", "Workspace"),
        "backstage" => l.text("Bestand", "File"),
        "settings" => l.text("Instellingen", "Settings"),
        "import-export" => l.text("Import / export", "Import / export"),
        "long-running-operation" => l.text("Voortgang", "Progress"),
        "unsaved-changes" => l.text("Niet opgeslagen", "Unsaved"),
        "empty" => l.text("Leeg", "Empty"),
        "error" => l.text("Fout", "Error"),
        "speech" => "Speech",
        "transcribe" => "Transcribe",
        "meeting" => "Meeting",
        "mic-test" => "Mic Test",
        "models" => "Models",
        "dictionary" => "Dictionary",
        "tts" => "Text To Speech",
        "about" => "About",
        "project" => "Project",
        "plattegrond" => "Plattegronden",
        "ifc" => "3D BIM",
        "opname" => "Opname",
        "inspectie" => "Inspectie",
        "oplevering" => "Oplevering",
        "dashboard" => "Dashboard",
        "export" => "Export",
        "koppelingen" => "Koppelingen",
        "handleiding" => "Handleiding",
        _ => "?",
    }
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
    sample_dialog: bool,
    sample_dialog_input: String,
    selected_studio: usize,
    selected_screen: usize,
    geotech_layer: usize,
    field_project: FieldProjectState,
    field_connector_notice: Option<&'static str>,
    field_export_type: usize,
    field_export_photos: bool,
    field_export_map: bool,
    field_export_notice: Option<&'static str>,
    field_flow_mode: Option<&'static str>,
    field_inspection_values: [String; 3],
    field_handover_values: [String; 2],
    field_inspection_type: usize,
    field_handover_type: usize,
    field_flow_notice: Option<&'static str>,
    field_review_notice: Option<&'static str>,
    field_capture_filter: [usize; 3],
    speech_notice: Option<&'static str>,
    speech_word: String,
    speech_replacement: String,
    speech_dictionary: Vec<(String, String)>,
    speech_settings_tab: usize,
    speech_tts_text: String,
    speech_tts_speed: f32,
    selected_preview_command: Option<String>,
    pile_view: ribbon_preview::PileViewState,
    frame_view: ribbon_preview::FrameViewState,
    pdf_image: ribbon_preview::PdfImageState,
    pdf_arrange: ribbon_preview::PdfArrangeState,
    pdf_format: ribbon_preview::PdfFormatState,
    selected_energy_step: usize,
    selected_energy_sub: Option<usize>,
    energy_mode: EnergyMode,
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
            sample_dialog: false,
            sample_dialog_input: String::new(),
            selected_studio: 0,
            selected_screen: 0,
            geotech_layer: 4,
            field_project: FieldProjectState::default(),
            field_connector_notice: None,
            field_export_type: 0,
            field_export_photos: true,
            field_export_map: true,
            field_export_notice: None,
            field_flow_mode: None,
            field_inspection_values: [String::new(), String::new(), String::new()],
            field_handover_values: [String::new(), String::new()],
            field_inspection_type: 0,
            field_handover_type: 0,
            field_flow_notice: None,
            field_review_notice: None,
            field_capture_filter: [0; 3],
            speech_notice: None,
            speech_word: String::new(),
            speech_replacement: String::new(),
            speech_dictionary: Vec::new(),
            speech_settings_tab: 0,
            speech_tts_text: String::new(),
            speech_tts_speed: 1.0,
            selected_preview_command: None,
            pile_view: ribbon_preview::PileViewState::default(),
            frame_view: ribbon_preview::FrameViewState::default(),
            pdf_image: ribbon_preview::PdfImageState::default(),
            pdf_arrange: ribbon_preview::PdfArrangeState::default(),
            pdf_format: ribbon_preview::PdfFormatState::default(),
            selected_energy_step: 0,
            selected_energy_sub: None,
            energy_mode: EnergyMode::NewBuildResidential,
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
                        widgets::dialog_button(
                            l.text("Primair", "Primary"),
                            move |_, status| widgets::primary_button_style(theme, status),
                        )
                        .width(110)
                        .height(27)
                        .on_press(Action::Toggle),
                        widgets::dialog_button(
                            l.text("Secundair", "Secondary"),
                            move |_, status| widgets::secondary_button_style(theme, status),
                        )
                        .width(110)
                        .height(27)
                        .on_press(Action::Show(Page::Layouts)),
                        widgets::dialog_button(
                            l.text("Uitgeschakeld", "Disabled"),
                            move |_, status| widgets::secondary_button_style(theme, status),
                        )
                        .width(140)
                        .height(27),
                        widgets::dialog_button(
                            l.text("Dialoog", "Dialog"),
                            move |_, status| widgets::secondary_button_style(theme, status),
                        )
                        .width(110)
                        .height(27)
                        .on_press(Action::SampleDialog(true)),
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
                    text(l.text("Bestandstaken", "File tasks"))
                        .font(fonts::STRONG)
                        .size(16),
                    widgets::backstage_page_heading(
                        l.text("Openen", "Open"),
                        l.text("Gedeelde opmaak voor Bestand-pagina's.", "Shared layout for File pages."),
                        theme,
                    ),
                    widgets::backstage_group_caption(l.text("BRONNEN", "SOURCES"), theme),
                    widgets::backstage_tile_column([
                        widgets::backstage_task_tile_with(
                            l.text("UI-iconen…", "UI icons…"),
                            l.text("Open de bronbewezen iconenbibliotheek.", "Open the source-proven icon library."),
                            Some(Action::Show(Page::Icons)),
                            move |_| theme,
                        ),
                        widgets::backstage_task_tile_with(
                            l.text("Nog niet beschikbaar", "Not yet available"),
                            l.text("De gedeelde uitgeschakelde toestand.", "The shared disabled state."),
                            None,
                            move |_| theme,
                        ),
                    ]),
                ]
                .spacing(9),
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
                        .style(move |_, status| widgets::text_input_style(theme, status))
                        .width(360),
                    iced::widget::checkbox(l.text("Voorbeeld actief", "Sample active"), self.sample_toggle)
                        .on_toggle(|_| Action::Toggle)
                        .size(13)
                        .text_size(11)
                        .spacing(6)
                        .style(move |_, status| widgets::checkbox_style(theme, status)),
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
                    iced::widget::slider(0.0..=100.0, self.sample_value, Action::Slider)
                        .style(move |_, status| widgets::slider_style(theme, status))
                        .width(360),
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
                    widgets::property_section(
                        l.text("Voorbeeld", "Sample"),
                        theme
                    ),
                    widgets::property_grid_row(
                        l.text("Naam", "Name"),
                        if self.sample_input.is_empty() {
                            "—"
                        } else {
                            &self.sample_input
                        },
                        theme
                    ),
                    widgets::property_grid_row(
                        l.text("Status", "Status"),
                        if self.sample_toggle {
                            l.text("Actief", "Active")
                        } else {
                            l.text("Inactief", "Inactive")
                        },
                        theme
                    ),
                    widgets::property_grid_control_with(
                        format!("{} {:.0}%", l.text("Schaal", "Scale"), self.sample_value),
                        iced::widget::slider(0.0..=100.0, self.sample_value, Action::Slider)
                            .style(move |_, status| widgets::slider_style(theme, status))
                            .width(Fill)
                            .into(),
                        move |_| theme,
                    ),
                ]
                .spacing(0),
                theme
            ),
        ]
        .spacing(18)
        .into()
    }
    fn icons(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut canonical = Column::new().spacing(5);
        for chunk in Icon::ALL.chunks(8) {
            let mut icons_row = Row::new().spacing(5);
            for &icon in chunk {
                icons_row = icons_row.push(
                    container(
                        column![icon.view(24, t.accent), text(icon.id()).size(10)]
                            .spacing(6)
                            .align_x(Alignment::Center),
                    )
                    .padding(8)
                    .width(84)
                    .height(64)
                    .align_x(Alignment::Center)
                    .style(move |_| container::Style {
                        background: Some(t.bg.into()),
                        border: iced::Border {
                            color: t.border,
                            width: 1.0,
                            radius: 4.0.into(),
                        },
                        ..Default::default()
                    }),
                );
            }
            canonical = canonical.push(icons_row);
        }
        let mut domain = Row::new().spacing(7);
        for icon in DomainIcon::ALL {
            domain = domain.push(
                container(
                    column![
                        row![icon.view(16, t.accent), icon.view(24, t.accent)]
                            .spacing(12)
                            .align_y(Alignment::Center),
                        text(icon.id()).size(10),
                    ]
                    .spacing(7)
                    .align_x(Alignment::Center),
                )
                .padding(8)
                .width(155)
                .height(74)
                .align_x(Alignment::Center)
                .style(move |_| container::Style {
                    background: Some(t.bg.into()),
                    border: iced::Border {
                        color: t.border,
                        width: 1.0,
                        radius: 4.0.into(),
                    },
                    ..Default::default()
                }),
            );
        }
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
            self.card(
                column![
                    text(format!(
                        "{} · {}",
                        l.text("Canonieke Rust-kern", "Canonical Rust core"),
                        Icon::ALL.len()
                    ))
                    .font(fonts::STRONG)
                    .size(14),
                    canonical,
                ]
                .spacing(10),
                theme,
            ),
            self.card(
                column![
                    text(l.text(
                        "Beoordeelde domeiniconen · 16 / 24 px",
                        "Reviewed domain icons · 16 / 24 px"
                    ))
                    .font(fonts::STRONG)
                    .size(14),
                    domain,
                ]
                .spacing(10),
                theme,
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
                .style(move |_, status| widgets::text_input_style(theme, status))
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
                format!("{} px", metrics::TITLE),
            ),
            (
                "02",
                l.text("Ribbon-tabs", "Ribbon tabs"),
                format!("{} px", metrics::TABS),
            ),
            ("03", "Ribbon", format!("{} px", metrics::RIBBON)),
            (
                "04",
                l.text("Documenttabs", "Document tabs"),
                format!("{} px", metrics::DOCUMENTS),
            ),
            (
                "05",
                l.text(
                    "Zijpanelen · standaardbreedte",
                    "Side panels · default width",
                ),
                format!("{} px", metrics::PANEL_DEFAULT),
            ),
            (
                "06",
                l.text("Paneelwerkbalken", "Panel toolbars"),
                format!("{} px", metrics::PANEL_TOOLBAR),
            ),
            (
                "07",
                l.text("Werkgebied", "Workspace"),
                l.text("Schaalbaar", "Resizable").to_owned(),
            ),
            (
                "08",
                l.text("Status", "Status"),
                format!("{} px", metrics::STATUS),
            ),
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
        if selected.id == "energy" {
            return self.energy_page(theme, l);
        }
        if selected.id == "speech" {
            return self.speech_page(theme, l);
        }
        if selected.id == "field" {
            return self.field_page(theme, l);
        }
        if selected.id == "geotech" && self.selected_screen == 1 {
            return geotech_native::workspace(self.geotech_layer, theme, l);
        }
        if selected.id == "cad" {
            return self.cad_page(theme, l);
        }
        let screen = selected
            .screens
            .get(self.selected_screen)
            .map(String::as_str)
            .unwrap_or("workspace");
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
        let mut tabs = Column::new().spacing(5);
        for chunk in selected.tabs.chunks(5) {
            let mut tab_row = Row::new().spacing(5);
            for tab in chunk {
                tab_row = tab_row.push(
                    container(text(if selected.optional_tabs.contains(tab) { format!("{tab} · optioneel") } else { tab.clone() }).size(11).color(t.text))
                        .padding(8)
                        .style(move |_| container::Style::default().background(t.bg_lighter)),
                );
            }
            tabs = tabs.push(tab_row);
        }
        let tab_review: Element<'_, Action> = if selected.id == "energy" {
            self.card(
                column![
                    text(l.text("Werkstroomnavigatie", "Workflow navigation"))
                        .font(fonts::STRONG).size(13).color(t.accent),
                    text(l.text("Project → Gebouw → Installaties → Controle → Resultaten en rapport → Registratie. De historische screenshot en de actuele bronroutes worden apart beoordeeld.",
                                "Project → Building → Installations → Check → Results and report → Registration. The historical screenshot and current source routes are reviewed separately."))
                        .size(11).color(t.text_secondary),
                ].spacing(8), theme)
        } else {
            let context: Element<'_, Action> = if selected.id == "pdf" {
                button(text(if self.pdf_format.symbol_stamp {
                    "Opmaaktoestand: één symboolstempel geselecteerd"
                } else {
                    "Opmaaktoestand: gewone annotatieselectie"
                }).size(11))
                    .padding([6, 9])
                    .on_press(Action::PdfFormatSymbolStamp)
                    .style(move |_, status| widgets::button_style(theme, self.pdf_format.symbol_stamp, status))
                    .into()
            } else { Space::new(0, 0).into() };
            column![
                text(l.text("Ribbon-tabs · bron / concept", "Ribbon tabs · source / concept"))
                    .font(fonts::STRONG).size(11).color(t.accent),
                tabs,
                context,
                self.preview_command_review(theme, l),
            ].spacing(10).into()
        };
        let mut screen_choices = Column::new().spacing(5);
        for (group, chunk) in selected.screens.chunks(5).enumerate() {
            let mut choices = Row::new().spacing(5);
            for (offset, id) in chunk.iter().enumerate() {
                let index = group * 5 + offset;
                choices = choices.push(
                    button(text(screen_label(id, l)).size(11))
                        .padding([6, 9])
                        .on_press(Action::SelectScreen(index))
                        .style(move |_, status| {
                            widgets::button_style(theme, index == self.selected_screen, status)
                        }),
                );
            }
            screen_choices = screen_choices.push(choices);
        }
        let format_palette: Element<'_, Action> = if selected.id == "pdf" {
            let colors = ribbon_preview::PDF_FORMAT_PALETTE.iter().enumerate()
                .map(|(index, hex)| (hex.to_string(), ribbon_preview::pdf_color(hex), Action::PdfFormatFill(index)))
                .collect();
            self.card(column![
                text("Opmaak · bronpalet 7 × 6").font(fonts::STRONG).size(13).color(t.accent),
                text("Kies een vulkleur; de lijnkleur gebruikt hetzelfde palet.").size(11).color(t.text_secondary),
                widgets::color_grid(theme, colors, 6, (self.pdf_format.fill < 42).then_some(self.pdf_format.fill)),
            ].spacing(8), theme)
        } else { Space::new(0, 0).into() };
        let detail = column![
            text(&selected.name)
                .font(fonts::HEADING)
                .size(27)
                .color(t.text),
            text(l.text("Schermtoestand", "Screen state"))
                .font(fonts::STRONG)
                .size(11)
                .color(t.accent),
            screen_choices,
            self.screen_preview(selected, screen, theme, l),
            format_palette,
            tab_review,
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
        .width(500);
        column![
            self.heading("STUDIO ATLAS", l.text("Alle studio's", "All studios"),
                l.text("Achttien applicatie-indelingen op dezelfde shell. Vergelijk schermtoestanden, ribbon-tabs en panelen.",
                       "Eighteen application layouts on one shell. Compare screen states, ribbon tabs and panels."), theme),
            scrollable(row![list, detail].spacing(24).width(744))
                .direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new()))
                .width(Fill),
        ].spacing(22).into()
    }
    fn cad_page(&self, theme: Theme, _l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let studio = &studios()[self.selected_studio];
        let image_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/OpenCADStudio/site/workspace.png");
        column![
            self.heading("SOURCE REVIEW · CAD CANVAS", "Open CAD Studio", "Huidige Rust-registry: zeven zichtbare kernmodules; bronbeeld kan een oudere UI-toestand tonen.", theme),
            text(&studio.notes).size(12).color(t.text_secondary),
            image(image::Handle::from_path(image_path)).width(1000),
        ].spacing(14).into()
    }
    fn field_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let studio = &studios()[self.selected_studio];
        let screen = studio.screens.get(self.selected_screen).map(String::as_str).unwrap_or("project");
        if screen == "project" {
            return self.field_project_page(theme, l);
        }
        if screen == "dashboard" {
            return self.field_dashboard_page(theme, l);
        }
        if screen == "koppelingen" {
            return self.field_connectors_page(theme, l);
        }
        if screen == "export" {
            return self.field_export_page(theme, l);
        }
        if screen == "inspectie" || screen == "oplevering" {
            return self.field_workflow_page(theme, l, screen == "inspectie");
        }
        if screen == "plattegrond" || screen == "ifc" {
            return self.field_upload_page(theme, l, screen == "ifc");
        }
        if screen == "opname" {
            return self.field_capture_page(theme, l);
        }
        if screen == "handleiding" {
            return self.field_manual_page(theme, l);
        }
        let capture = match screen {
            "project" => Some("01-project.png"),
            "koppelingen" => Some("02-koppelingen.png"),
            "inspectie" => Some("03-inspectie.png"),
            "oplevering" => Some("04-oplevering.png"),
            "dashboard" => Some("05-dashboard.png"),
            "export" => Some("06-export.png"),
            _ => None,
        };
        let t = theme.tokens();
        let mut content = Column::new().spacing(14)
            .push(self.heading("SOURCE REVIEW · TOP NAV", "Open Field Studio", "Tien pagina’s in de bovenste navigatie; zes brongepinde captures.", theme))
            .push(text(format!("{} · {}", screen_label(screen, l), studio.notes)).size(12).color(t.text_secondary));
        if let Some(name) = capture {
            let source = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("harmonization/references/Open-Field-Studio/docs/screenshots").join(name);
            content = content.push(image(image::Handle::from_path(source)).width(1200));
        } else {
            content = content.push(self.card(text("Deze pagina is in index.html geverifieerd; een broncapture ontbreekt.").size(12), theme));
        }
        content.into()
    }
    fn field_project_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let field = |index: usize, label: &'static str, width: f32| {
            widgets::form_field(theme, label, self.field_project.values[index].clone(),
                move |value| Action::FieldProjectEdit(index, value), iced::Length::Fixed(width))
        };
        let bag = button(text(l.text("Zoek adres (BAG)", "Find address (BAG)")).size(12))
            .padding([9, 16]).on_press(Action::FieldProjectPreview(
                "BAG is in deze schermreview niet gekoppeld; de badge komt uit de broncapture."))
            .style(move |_, status| widgets::button_style(theme, false, status));
        let energy = button(text(l.text("Energielabel ophalen", "Fetch energy label")).size(12))
            .padding([9, 16]).on_press(Action::FieldProjectPreview(
                "Energielabel is in deze schermreview niet gekoppeld; Label B is bronvoorbeelddata."))
            .style(move |_, status| widgets::button_style(theme, false, status));
        let verified_ink = if theme == Theme::Light {
            iced::Color::from_rgb8(0x05, 0x96, 0x69)
        } else {
            iced::Color::from_rgb8(0x86, 0xef, 0xac)
        };
        let mut sample_actions = column![
            bag,
            text("✓ Bronvoorbeeld: BAG-geverifieerd · 036320000481734")
                .size(11).color(verified_ink),
            energy,
            container(text("Label B").size(11).color(iced::Color::WHITE))
                .padding([4, 9]).style(|_| container::Style::default()
                    .background(iced::Color::from_rgb8(0x70, 0xbc, 0x31))
                    .border(iced::Border::default().rounded(3))),
        ].spacing(10).align_x(Alignment::Center);
        if let Some(notice) = self.field_project.notice {
            sample_actions = sample_actions.push(text(notice).size(11).color(t.text_secondary));
        }
        let mut form = Column::new().spacing(24)
            .push(text(l.text("Projectgegevens", "Project details"))
                .font(fonts::HEADING).size(29).color(t.text))
            .push(row![
                field(0, l.text("Projectnaam *", "Project name *"), 540.0),
                field(1, l.text("Projectnummer", "Project number"), 540.0)].spacing(24))
            .push(row![
                field(2, l.text("Opdrachtgever", "Client"), 540.0),
                field(3, l.text("Contactpersoon", "Contact person"), 540.0)].spacing(24))
            .push(field(4, l.text("Straat en huisnummer *", "Street and number *"), 1104.0))
            .push(row![
                field(5, l.text("Postcode *", "Postal code *"), 540.0),
                field(6, l.text("Plaats *", "City *"), 540.0)].spacing(24))
            .push(container(sample_actions).width(1104).center_x(iced::Fill))
            .push(row![
                field(7, l.text("Opnamedatum", "Survey date"), 540.0),
                field(8, l.text("Opgenomen door", "Surveyor"), 540.0)].spacing(24))
            .push(field(9, l.text("Projectbeschrijving", "Project description"), 1104.0))
            .push(field(10, l.text("Notities", "Notes"), 1104.0));
        form = form.push(button(text(l.text("Project opslaan · preview", "Save project · preview")).size(12))
            .padding([10, 16]).on_press(Action::FieldProjectPreview(
                "De Style Repo bewaart dit voorbeeld alleen in de huidige sessie."))
            .style(move |_, status| widgets::button_style(theme, false, status)));
        let panel = container(form).padding(32).width(1168)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border { color: t.border, width: 1.0, radius: 10.0.into() }));
        let capture = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/Open-Field-Studio/docs/screenshots/01-project.png");
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            panel,
            text("Broncapture ter vergelijking · commit 8a4f104")
                .font(fonts::MEDIUM).size(12).color(t.text_secondary),
            image(image::Handle::from_path(capture)).width(1168),
        ].spacing(16).into()
    }
    fn field_dashboard_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let tile = |label: &'static str, value: &'static str, color: iced::Color| {
            container(
                column![
                    text(label)
                        .font(fonts::STRONG)
                        .size(11)
                        .color(t.text_secondary),
                    text(value).font(fonts::HEADING).size(35).color(color),
                ]
                .spacing(18)
                .align_x(Alignment::Center),
            )
            .width(174)
            .height(126)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
            .style(move |_| {
                container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border {
                        color: t.border,
                        width: 1.0,
                        radius: 10.0.into(),
                    })
            })
        };
        let orange = iced::Color::from_rgb8(0xdc, 0x79, 0x00);
        let blue = iced::Color::from_rgb8(0x2c, 0x61, 0xe8);
        let green = iced::Color::from_rgb8(0x13, 0xa0, 0x50);
        let red = iced::Color::from_rgb8(0xdb, 0x24, 0x2b);
        let chart =
            |title: &'static str, entries: &[(&'static str, &'static str, iced::Color, f32)]| {
                let mut rows = Column::new().spacing(10);
                for &(label, count, color, fraction) in entries {
                    rows = rows.push(
                        row![
                            container(text(label).size(11).color(t.text)).width(90),
                            container(
                                container(Space::new((185.0 * fraction).max(6.0), 22))
                                    .width((185.0 * fraction).max(6.0))
                                    .style(move |_| container::Style::default()
                                        .background(color)
                                        .border(iced::Border::default().rounded(4)))
                            )
                            .width(185)
                            .height(22)
                            .style(move |_| container::Style::default().background(t.bg)),
                            container(text(count).size(11).color(t.text)).width(20),
                        ]
                        .spacing(8)
                        .align_y(Alignment::Center),
                    );
                }
                container(
                    column![text(title).font(fonts::STRONG).size(15).color(t.text), rows]
                        .spacing(22),
                )
                .padding(24)
                .width(368)
                .height(202)
                .style(move |_| {
                    container::Style::default()
                        .background(t.bg_lighter)
                        .border(iced::Border {
                            color: t.border,
                            width: 1.0,
                            radius: 10.0.into(),
                        })
                })
            };
        let stats = row![
            tile("TOTAAL TICKETS", "3", t.text),
            tile("OPEN", "1", orange),
            tile("TOEGEWEZEN", "1", blue),
            tile("AFGEROND", "1", green),
            tile("VERLOPEN DEADLINE", "0", red),
            tile("INSPECTIES", "0", t.text),
        ]
        .spacing(16);
        let charts = row![
            chart(
                "Tickets per status",
                &[
                    ("Open", "1", orange, 1.0),
                    ("Toegewezen", "1", blue, 1.0),
                    ("Afgerond", "1", green, 1.0),
                    ("Verlopen", "0", red, 0.03)
                ]
            ),
            chart(
                "Tickets per categorie",
                &[
                    ("Kozijnen", "1", orange, 1.0),
                    ("Sanitair", "1", orange, 1.0),
                    ("Elektra", "1", orange, 1.0)
                ]
            ),
            chart(
                "Tickets per verantwoordelijke",
                &[
                    ("De Wit Bouw", "1", blue, 1.0),
                    ("Slager Loodgieters", "1", blue, 1.0)
                ]
            ),
        ]
        .spacing(24);
        let activity = container(
            column![
                text(l.text("Recente activiteit", "Recent activity"))
                    .font(fonts::STRONG)
                    .size(15)
                    .color(t.text),
                container(
                    text(l.text("Nog geen activiteit", "No activity yet"))
                        .size(13)
                        .color(t.text_secondary)
                )
                .height(94)
                .width(Fill)
                .align_x(Alignment::Center)
                .align_y(Alignment::Center),
            ]
            .spacing(20),
        )
        .padding(24)
        .width(360)
        .height(150)
        .style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 10.0.into(),
                })
        });
        let capture = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/Open-Field-Studio/docs/screenshots/05-dashboard.png");
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG)
                .size(11)
                .color(t.accent),
            text("Voorbeelddata uit broncapture · Renovatie Damrak 1 · 3 tickets")
                .size(12)
                .color(t.text_secondary),
            stats,
            charts,
            activity,
            text("Broncapture ter vergelijking · commit 8a4f104")
                .font(fonts::MEDIUM)
                .size(12)
                .color(t.text_secondary),
            image(image::Handle::from_path(capture)).width(1168),
        ]
        .spacing(24)
        .into()
    }
    fn field_connectors_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        // Endpoint defaults from Open Field Studio's _connectorDefs(); status is screenshot example data.
        let definitions = [
            ("Woningborg WKI", "https://api.woningborg.nl/pvo/v1/dossiers", false, false),
            ("SWK (Stichting Waarborgfonds Koopwoningen)", "https://api.swk.nl/pvo/v1/dossiers", false, false),
            ("AFAS Profit", "https://<klant>.rest.afas.online/profitrestservices/connectors/KnSubject", true, false),
            ("Exact Online", "https://start.exactonline.nl/api/v1/<division>/documents/Documents", false, false),
            ("ERPNext (Frappe)", "https://<klant>.frappe.cloud/api/resource/Project", true, true),
            ("Bouw7", "https://api.bouw7.nl/v1/projects/<project-id>/documents", false, false),
            ("n8n / webhook", "https://n8n.example.nl/webhook/ofs-dossier", false, true),
            ("KYP Project (planning)", "https://kyp.nl/api/v1/projects/<project-id>/tasks", false, false),
        ];
        let mut list = Column::new().spacing(14);
        for (name, endpoint, configured, can_import) in definitions {
            let status = if configured { "INGESTELD" } else { "NIET INGESTELD" };
            let status_color = if configured { t.text_secondary } else { t.accent };
            let configure = button(text(l.text("Configureren", "Configure")).size(12))
                .padding([7, 12]).on_press(Action::FieldConnectorPreview(name))
                .style(move |_, state| {
                    let mut style = widgets::button_style(theme, false, state);
                    style.border = iced::Border { color: t.text, width: 1.0, radius: 5.0.into() };
                    style
                });
            let mut actions = Row::new().spacing(8).align_y(Alignment::Center)
                .push(text(status).font(fonts::STRONG).size(10).color(status_color));
            if can_import {
                actions = actions.push(button(text(l.text("Importeren", "Import")).size(12))
                    .padding([7, 12]).on_press(Action::FieldConnectorPreview(name))
                    .style(move |_, state| {
                        let mut style = widgets::button_style(theme, false, state);
                        style.border = iced::Border { color: t.text, width: 1.0, radius: 5.0.into() };
                        style
                    }));
            }
            actions = actions.push(configure);
            let details = column![
                text(name).font(fonts::STRONG).size(14).color(t.text),
                text(endpoint).size(11).color(t.text_secondary),
            ].spacing(8).width(Fill);
            list = list.push(container(row![details, actions].spacing(12).align_y(Alignment::Center))
                .width(1104).padding([20, 24])
                .style(move |_| container::Style::default().background(t.bg)
                    .border(iced::Border { color: t.border, width: 1.0, radius: 8.0.into() })));
        }
        let mut panel = Column::new().spacing(20)
            .push(text(l.text("Koppelingen", "Connectors")).font(fonts::HEADING).size(29).color(t.text))
            .push(text(l.text(
                "Configureer externe systemen voor opleveringen, dossiers en taken. Sleutels blijven lokaal op deze computer.",
                "Configure external systems for handovers, dossiers and tasks. Keys remain local to this computer.",
            )).size(13).color(t.text_secondary));
        if let Some(name) = self.field_connector_notice {
            panel = panel.push(text(format!("{name}: configuratie en import zijn in deze schermreview niet gekoppeld."))
                .size(12).color(t.accent));
        }
        panel = panel.push(list);
        let panel = container(panel).padding(32).width(1168)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border { color: t.border, width: 1.0, radius: 10.0.into() }));
        let capture = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/Open-Field-Studio/docs/screenshots/02-koppelingen.png");
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            text("Connectorstatussen zijn bronvoorbeelddata; geen lokale sleutels worden gelezen.")
                .size(12).color(t.text_secondary),
            panel,
            text("Broncapture ter vergelijking · commit 8a4f104")
                .font(fonts::MEDIUM).size(12).color(t.text_secondary),
            image(image::Handle::from_path(capture)).width(1168),
        ].spacing(16).into()
    }
    fn field_export_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let summary_tile = |label: &'static str, value: String| {
            container(column![
                text(label).font(fonts::STRONG).size(11).color(t.text_secondary),
                text(value).size(15).color(t.text),
            ].spacing(10))
                .padding(16).width(208).height(78)
                .style(move |_| container::Style::default().background(t.bg_lighter)
                    .border(iced::Border { color: t.border, width: 1.0, radius: 7.0.into() }))
        };
        let summary = container(column![
            text(l.text("Overzicht", "Overview")).font(fonts::STRONG).size(16).color(t.text),
            row![
                summary_tile("Project", self.field_project.values[0].clone()),
                summary_tile("Adres", self.field_project.values[4].clone()),
                summary_tile("Plattegronden", "0".into()),
                summary_tile("Tickets", "3".into()),
                summary_tile("Foto's", "0".into()),
            ].spacing(16),
            row![
                summary_tile("Inspecties", "0".into()),
                summary_tile("Opleveringen", "0".into()),
            ].spacing(16),
        ].spacing(18)).padding(24).width(1104)
            .style(move |_| container::Style::default().background(t.bg)
                .border(iced::Border::default().rounded(8)));
        let mut report_types = Column::new().spacing(12);
        for (index, label) in [
            "Volledig projectrapport", "Puntenlijst (open tickets)",
            "Inspectie-rapport", "Proces-verbaal van oplevering",
        ].into_iter().enumerate() {
            report_types = report_types.push(iced::widget::radio(
                label, index, Some(self.field_export_type), Action::FieldExportType,
            ).size(16).text_size(13).spacing(12));
        }
        if self.field_export_type == 2 || self.field_export_type == 3 {
            report_types = report_types.push(text(if self.field_export_type == 2 {
                "Geen inspecties in dit bronvoorbeeld beschikbaar."
            } else {
                "Geen opleveringen in dit bronvoorbeeld beschikbaar."
            }).size(12).color(t.text_secondary));
        }
        let options = column![
            iced::widget::checkbox(l.text("Foto's insluiten", "Include photos"), self.field_export_photos)
                .on_toggle(Action::FieldExportPhotos).size(15).text_size(13).spacing(12)
                .style(move |_, status| widgets::checkbox_style(theme, status)),
            iced::widget::checkbox(l.text("Plattegrond met markeringen", "Floor plan with markers"), self.field_export_map)
                .on_toggle(Action::FieldExportMap).size(15).text_size(13).spacing(12)
                .style(move |_, status| widgets::checkbox_style(theme, status)),
        ].spacing(12);
        let mut actions = Row::new().spacing(10);
        for (label, format) in [
            ("Exporteer als PDF", "PDF"), ("Exporteer als HTML", "HTML"),
            ("Exporteer als BCF (BIM)", "BCF"), ("Sync met KYP Project", "KYP"),
            ("Project Opslaan (JSON)", "JSON"),
        ] {
            actions = actions.push(button(text(label).size(12)).padding([10, 13])
                .on_press(Action::FieldExportPreview(format))
                .style(move |_, status| if format == "PDF" {
                    widgets::primary_button_style(theme, status)
                } else { widgets::button_style(theme, false, status) }));
        }
        let mut panel = Column::new().spacing(24)
            .push(text(l.text("Project Exporteren", "Export project"))
                .font(fonts::HEADING).size(29).color(t.text))
            .push(summary)
            .push(text(l.text("Rapport type", "Report type")).font(fonts::STRONG).size(16).color(t.text))
            .push(report_types)
            .push(text(l.text("Opties", "Options")).font(fonts::STRONG).size(16).color(t.text))
            .push(options)
            .push(actions);
        if let Some(format) = self.field_export_notice {
            panel = panel.push(text(format!("{format}: in deze schermreview wordt geen bestand gemaakt of synchronisatie uitgevoerd."))
                .size(12).color(t.accent));
        }
        let panel = container(panel).padding(32).width(1168)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border { color: t.border, width: 1.0, radius: 10.0.into() }));
        let capture = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/Open-Field-Studio/docs/screenshots/06-export.png");
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            text("Projectsamenvatting uit bronvoorbeeld; rapportkeuze en opties zijn interactief.")
                .size(12).color(t.text_secondary),
            panel,
            text("Broncapture ter vergelijking · commit 8a4f104")
                .font(fonts::MEDIUM).size(12).color(t.text_secondary),
            image(image::Handle::from_path(capture)).width(1168),
        ].spacing(16).into()
    }
    fn field_workflow_page(&self, theme: Theme, l: Language, inspection: bool) -> Element<'_, Action> {
        let t = theme.tokens();
        let mode = if inspection { "inspectie" } else { "oplevering" };
        let title = if inspection { "Inspecties" } else { "Opleveringen" };
        let capture = if inspection { "03-inspectie.png" } else { "04-oplevering.png" };
        let content: Element<'_, Action> = if self.field_flow_mode == Some(mode) {
            let edit = |index: usize, label: &'static str, value: String| {
                widgets::form_field(theme, label, value,
                    move |value| Action::FieldFlowEdit(inspection, index, value),
                    iced::Length::Fixed(532.0))
            };
            let choices: Vec<String> = if inspection {
                vec!["Vrije inspectie".into(), "Checklist-inspectie".into()]
            } else {
                vec!["Vooroplevering".into(), "Eerste oplevering".into(),
                    "Tweede oplevering / Naschouw".into()]
            };
            let selected_index = if inspection { self.field_inspection_type } else { self.field_handover_type };
            let selected = choices.get(selected_index).cloned();
            let type_picker = pick_list(choices.clone(), selected, move |value| {
                Action::FieldFlowType(inspection,
                    choices.iter().position(|choice| choice == &value).unwrap_or(0))
            }).width(532).style(move |_, status| widgets::pick_list_style(theme, status))
                .menu_style(move |_| widgets::pick_list_menu_style(theme));
            let picker = column![
                text(if inspection { "Type" } else { "Type oplevering" })
                    .font(fonts::MEDIUM).size(12).color(t.text_secondary),
                type_picker,
            ].spacing(7);
            let mut form = Column::new().spacing(22)
                .push(text(if inspection { "Nieuwe Inspectie" } else { "Nieuwe Oplevering" })
                    .font(fonts::HEADING).size(29).color(t.text));
            if inspection {
                form = form.push(row![
                    edit(0, "Naam inspectie *", self.field_inspection_values[0].clone()),
                    picker,
                ].spacing(24))
                .push(row![
                    container(column![
                        text("Checklist template").font(fonts::MEDIUM).size(12).color(t.text_secondary),
                        text("— Kies template —").size(13).color(t.text_secondary),
                    ].spacing(12)).width(532),
                    container(column![
                        text("Plattegrond").font(fonts::MEDIUM).size(12).color(t.text_secondary),
                        text("— Optioneel —").size(13).color(t.text_secondary),
                    ].spacing(12)).width(532),
                ].spacing(24))
                .push(row![
                    edit(1, "Inspecteur", self.field_inspection_values[1].clone()),
                    edit(2, "Datum", self.field_inspection_values[2].clone()),
                ].spacing(24));
            } else {
                form = form.push(row![
                    picker,
                    edit(0, "Datum", self.field_handover_values[0].clone()),
                ].spacing(24))
                .push(edit(1, "Opmerkingen", self.field_handover_values[1].clone()))
                .push(text("Deelnemers").font(fonts::STRONG).size(16).color(t.text))
                .push(button(text("+ Deelnemer").size(12)).padding([9, 14])
                    .on_press(Action::FieldFlowPreview("Deelnemers"))
                    .style(move |_, status| widgets::button_style(theme, false, status)));
            }
            form = form.push(row![
                button(text(l.text("Annuleren", "Cancel")).size(12)).padding([10, 16])
                    .on_press(Action::FieldFlowCancel)
                    .style(move |_, status| widgets::button_style(theme, false, status)),
                button(text(if inspection { "Inspectie Starten" } else { "Oplevering Starten" }).size(12))
                    .padding([10, 16]).on_press(Action::FieldFlowPreview(mode))
                    .style(move |_, status| widgets::primary_button_style(theme, status)),
            ].spacing(10));
            if let Some(message) = self.field_flow_notice {
                form = form.push(text(format!("{message}: deze schermreview maakt nog geen projectrecord aan."))
                    .size(12).color(t.accent));
            }
            container(form).padding(32).width(1168)
                .style(move |_| container::Style::default().background(t.bg_lighter)
                    .border(iced::Border { color: t.border, width: 1.0, radius: 10.0.into() })).into()
        } else {
            widgets::empty_collection(theme, title,
                if inspection { "+ Nieuwe inspectie" } else { "+ Nieuwe oplevering" },
                if inspection { "Nog geen inspecties uitgevoerd" } else { "Nog geen opleveringen" },
                Action::FieldFlowSetup(mode), iced::Length::Fixed(1168.0))
        };
        let source = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/Open-Field-Studio/docs/screenshots").join(capture);
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            content,
            text("Broncapture van leeg overzicht ter vergelijking · commit 8a4f104")
                .font(fonts::MEDIUM).size(12).color(t.text_secondary),
            image(image::Handle::from_path(source)).width(1168),
        ].spacing(16).into()
    }
    fn speech_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let studio = &studios()[self.selected_studio];
        let screen = studio.screens.get(self.selected_screen).map(String::as_str).unwrap_or("speech");
        self.speech_native_page(theme, l, screen)
    }
    fn energy_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let selected = &studios()[self.selected_studio];
        let screen = selected.screens.get(self.selected_screen).map(String::as_str).unwrap_or("workspace");
        let choices: Vec<String> = studios().iter().map(|studio| studio.name.clone()).collect();
        let studio_picker = pick_list(choices, Some(selected.name.clone()), |name| {
            Action::SelectStudio(studios().iter().position(|studio| studio.name == name).unwrap_or(0))
        }).width(235).style(move |_, status| widgets::pick_list_style(theme, status))
            .menu_style(move |_| widgets::pick_list_menu_style(theme));
        let mode = self.energy_mode;
        let mode_choices: Vec<String> = EnergyMode::ALL.iter().map(|mode| mode.label(l).to_string()).collect();
        let mode_picker = pick_list(mode_choices, Some(mode.label(l).to_string()), move |name| {
            Action::SelectEnergyMode(EnergyMode::ALL.into_iter()
                .find(|candidate| candidate.label(l) == name).unwrap_or(EnergyMode::NewBuildResidential))
        }).width(235).style(move |_, status| widgets::pick_list_style(theme, status))
            .menu_style(move |_| widgets::pick_list_menu_style(theme));
        let mut states = Row::new().spacing(5);
        for (index, id) in selected.screens.iter().enumerate() {
            states = states.push(button(text(screen_label(id, l)).size(11))
                .padding([6, 9]).on_press(Action::SelectScreen(index))
                .style(move |_, status| widgets::button_style(theme, index == self.selected_screen, status)));
        }
        let main: Element<'_, Action> = if screen == "workspace" {
            let steps = mode.steps(l);
            let active = &steps[self.selected_energy_step.min(steps.len() - 1)];
            let active_label = self.selected_energy_sub
                .and_then(|index| active.subs.get(index).copied()).unwrap_or(active.label);
            let progress_labels: &[&str] = if mode.existing() {
                &["Opname", "Controle", "Label en rapport", "Registratie"]
            } else {
                &["Project", "Gebouw", "Installaties", "Controle"]
            };
            let mut progress = Column::new().spacing(13).push(
                text(l.text("Voortgang · ontwerpvoorbeeld", "Progress · design example"))
                    .font(fonts::STRONG).size(14));
            for (index, label) in progress_labels.iter().enumerate() {
                let status = if index < self.selected_energy_step {
                    l.text("✓  compleet", "✓  complete")
                } else if index == self.selected_energy_step {
                    l.text("actief", "active")
                } else {
                    l.text("open", "pending")
                };
                progress = progress.push(widgets::property(*label, status, theme));
            }
            let outcome = if mode.existing() {
                self.card(column![
                    text(l.text("Indicatieve labelklasse", "Indicative energy label"))
                        .font(fonts::STRONG).size(14),
                    text("A+").font(fonts::HEADING).size(35).color(t.accent),
                    widgets::property(l.text("Opname", "Survey"), l.text("In behandeling", "In progress"), theme),
                    widgets::property(l.text("Bewijs", "Evidence"), l.text("Concept", "Draft"), theme),
                    widgets::property(l.text("Controle", "Check"), l.text("Nog te beoordelen", "Review pending"), theme),
                ].spacing(11), theme)
            } else {
                self.card(column![
                    text(l.text("Voorlopige uitkomst", "Provisional outcome"))
                        .font(fonts::STRONG).size(14),
                    text("A+").font(fonts::HEADING).size(35).color(t.accent),
                    widgets::property("BENG 1", "51,4 kWh/m²", theme),
                    widgets::property("BENG 2", "80,6 kWh/m²", theme),
                    widgets::property("BENG 3", "22,3 %", theme),
                ].spacing(11), theme)
            };
            let form = if mode.existing() {
                self.card(column![
                    text(l.text("Basisopname · overzicht", "Basic survey · overview"))
                        .font(fonts::STRONG).size(14),
                    row![
                        column![
                            widgets::property(l.text("Opnametype", "Survey type"),
                                if mode.utility() { "Utiliteit" } else { "Woning" }, theme),
                            widgets::property(l.text("Onderdeel", "Section"), active_label, theme),
                        ].spacing(10).width(Fill),
                        column![
                            widgets::property(l.text("Bron en bewijs", "Source and evidence"), "Voorbeeldproject", theme),
                            widgets::property(l.text("Labelstatus", "Label status"), "Concept", theme),
                        ].spacing(10).width(Fill),
                    ].spacing(20),
                ].spacing(14), theme)
            } else {
                self.card(column![
                    text(l.text("NTA 8800-invoer", "NTA 8800 input")).font(fonts::STRONG).size(14),
                    row![
                        column![
                            widgets::property(l.text("Uitgave", "Edition"), "NTA 8800:2025+C1:2026", theme),
                            widgets::property(l.text("Gebruiksfunctie", "Use"),
                                if mode.utility() { "Overige gebruiksfunctie" } else { "Woonfunctie" }, theme),
                        ].spacing(10).width(Fill),
                        column![
                            widgets::property(l.text("Rekenscope", "Calculation scope"),
                                if mode.utility() { "Utiliteitsbouw" } else { "Woningbouw" }, theme),
                            widgets::property(l.text("Bron en bewijs", "Source and evidence"), "Voorbeeldproject", theme),
                        ].spacing(10).width(Fill),
                    ].spacing(20),
                ].spacing(14), theme)
            };
            column![
                text(if mode.existing() {
                    l.text("Voorbeeld bestaande bouw", "Existing-building example")
                } else {
                    l.text("Voorbeeld nieuwbouw", "New-build example")
                }).font(fonts::HEADING).size(27),
                text(format!("{}: {active_label}", l.text("Actieve stap", "Active step")))
                    .size(12).color(t.text_secondary),
                row![self.card(progress, theme), outcome].spacing(16).width(Fill),
                form,
                text(l.text("Stijlproef op basis van bronroutes; berekening en veldgedrag blijven eigendom van Energy Studio.",
                            "Style study based on source routes; calculation and field behavior remain with Energy Studio."))
                    .size(11).color(t.text_secondary),
            ].spacing(17).into()
        } else {
            self.screen_preview(selected, screen, theme, l)
        };
        column![
            row![
                column![
                    text("ENERGY WORKFLOW · SOURCE REVIEW").font(fonts::STRONG).size(11).color(t.accent),
                    text(&selected.name).font(fonts::HEADING).size(29),
                ].spacing(5).width(Fill),
                studio_picker,
            ].align_y(Alignment::Center).spacing(20),
            mode_picker,
            scrollable(states).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())),
            main,
            text(&selected.notes).size(11).color(t.text_secondary),
        ].spacing(18).into()
    }
    fn preview_command_review(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let detail: Element<'_, Action> = match self.selected_preview_command.as_deref() {
            Some(id) => match proposals().iter().find(|proposal| proposal.id == id) {
                Some(proposal) => column![
                    text(&proposal.label).font(fonts::STRONG).size(14),
                    text(&proposal.visual_metaphor).size(12),
                    text(format!("{} {}", proposal.name_match_count, l.text("naamkandidaten · nog niet goedgekeurd", "name candidates · not approved"))).size(11).color(t.text_secondary),
                ].spacing(5).into(),
                None if id.starts_with("planner:") => column![
                    text(id.rsplit(':').next().unwrap_or(id)).font(fonts::STRONG).size(14),
                    text(l.text("Groep en commando uit de actuele Planner-ribbonregistry. Domeiniconen zijn vastgepinde bronvormen ter beoordeling; gedeelde acties gebruiken de canonieke kern.", "Group and command from the current Planner ribbon registry. Domain icons are pinned source vectors for review; shared actions use the canonical core.")).size(11).color(t.text_secondary),
                ].spacing(5).into(),
                None => column![
                    text(id.rsplit(':').next().unwrap_or(id)).font(fonts::STRONG).size(14),
                    text(l.text("Gedeeld conceptcommando voor de ribbonvergelijking.", "Shared concept command for ribbon comparison.")).size(11).color(t.text_secondary),
                ].spacing(5).into(),
            },
            None => text(l.text("Kies een ribboncommando om de betekenis te beoordelen.", "Select a ribbon command to review its meaning.")).size(12).color(t.text_secondary).into(),
        };
        self.card(column![
            text(l.text("Ribbonreview · concept", "Ribbon review · concept")).font(fonts::STRONG).size(13).color(t.accent),
            detail,
        ].spacing(8), theme)
    }
    fn screen_preview<'a>(
        &'a self,
        studio: &'a StudioLayout,
        screen: &str,
        theme: Theme,
        l: Language,
    ) -> Element<'a, Action> {
        let t = theme.tokens();
        let title = screen_label(screen, l);
        let body: Element<'a, Action> = match screen {
            "start" => column![
                Icon::Cube.view(34, t.accent),
                text(&studio.name).font(fonts::HEADING).size(23),
                text(l.text("Begin met een nieuw project of open een bestaand bestand.", "Start a new project or open an existing file.")).size(12),
            ].spacing(9).into(),
            "workspace" if studio.id == "energy" => column![
                text(l.text("Voorbeeld tussenwoning", "Example terraced home"))
                    .font(fonts::HEADING).size(20),
                text(l.text("Brongepinde Energy-werkstroom · nieuwbouw woning", "Source-pinned Energy workflow · residential new build"))
                    .size(11).color(t.text_secondary),
                widgets::property(l.text("Actieve stap", "Active step"),
                    ["Project", "Gebouw", "Installaties", "Controle", "Resultaten en rapport", "Registratie"]
                        [self.selected_energy_step.min(5)], theme),
                widgets::property(l.text("Voortgang", "Progress"), "Project ✓ · Gebouw ✓ · Installaties ✓", theme),
                widgets::property(l.text("Indicatieve labelklasse", "Indicative label class"), "A+", theme),
                text(l.text("De inhoudskaarten zijn een stijlproef; de NTA-berekening blijft in Energy Studio.",
                            "The content cards are a style study; the NTA calculation remains in Energy Studio."))
                    .size(11).color(t.text_secondary),
            ].spacing(11).into(),
            "workspace" => column![
                text(&studio.workspace).font(fonts::HEADING).size(20),
                text(l.text("Domeinwerkruimte binnen de gedeelde titel, ribbon, panelen en status.", "Domain workspace inside the shared title, ribbon, panels and status.")).size(12).color(t.text_secondary),
                widgets::property(l.text("Verkenner", "Explorer"), &studio.left_panel, theme),
                widgets::property(l.text("Eigenschappen", "Properties"), &studio.right_panel, theme),
            ].spacing(12).into(),
            "backstage" => column![
                text(l.text("Bestand", "File")).font(fonts::HEADING).size(23),
                text(l.text("Nieuw  ·  Openen  ·  Opslaan  ·  Exporteren  ·  Instellingen", "New  ·  Open  ·  Save  ·  Export  ·  Settings")).size(12).color(t.accent),
                text(l.text("Recente projecten verschijnen in dezelfde gedeelde bestandsweergave.", "Recent projects appear in the same shared file view.")).size(12),
            ].spacing(12).into(),
            "settings" => column![
                text(l.text("Instellingen", "Settings")).font(fonts::HEADING).size(23),
                widgets::property(l.text("Thema", "Theme"), theme.to_string(), theme),
                widgets::property(l.text("Taal", "Language"), l.text("Nederlands", "English"), theme),
                text(l.text("De titelbalk opent de werkende instellingen van deze Rust-app.", "The title bar opens this Rust app's working settings.")).size(12).color(t.text_secondary),
            ].spacing(12).into(),
            "import-export" => column![
                text(title).font(fonts::HEADING).size(23),
                text(l.text("Actie en bestandsformaat zijn studiospecifiek; veldmaten en knoppen volgen de gedeelde stijl.", "Action and file format are studio-specific; field sizes and buttons follow the shared style.")).size(12),
                text_input(l.text("Projectnaam", "Project name"), "Project_01")
                    .style(move |_, status| widgets::text_input_style(theme, status))
                    .width(300),
            ].spacing(12).into(),
            "long-running-operation" => column![
                text(l.text("Bezig met verwerken", "Processing")).font(fonts::HEADING).size(23),
                text(format!("{} · 62%", studio.workspace)).size(12),
                progress_bar(0.0..=100.0, 62.0)
                    .style(move |_| widgets::progress_style(theme))
                    .height(8)
                    .width(300),
                text(l.text("Stap 3 van 5 · Annuleren blijft beschikbaar.", "Step 3 of 5 · Cancel remains available.")).size(12).color(t.text_secondary),
            ].spacing(12).into(),
            "unsaved-changes" => column![
                text(l.text("Wijzigingen opslaan?", "Save changes?")).font(fonts::HEADING).size(23).color(t.accent),
                text(format!("{} {}", studio.workspace, l.text("heeft niet-opgeslagen wijzigingen.", "has unsaved changes."))).size(12),
                text(l.text("Annuleren  ·  Niet opslaan  ·  Opslaan", "Cancel  ·  Discard  ·  Save")).size(12).color(t.text_secondary),
            ].spacing(12).into(),
            "empty" => column![
                Icon::New.view(34, t.text_faint),
                text(l.text("Geen document geopend", "No document open")).font(fonts::HEADING).size(23),
                text(l.text("Open of maak een project om te beginnen.", "Open or create a project to begin.")).size(12),
            ].spacing(9).into(),
            "error" => column![
                text(l.text("Bestand kan niet worden geopend", "Cannot open file")).font(fonts::HEADING).size(23).color(t.danger_color),
                text(l.text("Een foutmelding noemt de oorzaak en biedt een herstelactie.", "An error message names the cause and offers a recovery action.")).size(12),
                text(l.text("Details bekijken  ·  Opnieuw proberen", "View details  ·  Try again")).size(12).color(t.text_secondary),
            ].spacing(12).into(),
            _ => text(l.text("Schermtoestand niet beschikbaar", "Screen state unavailable")).size(12).into(),
        };
        self.card(container(body).height(150), theme)
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
            let small_preview = svg(svg::Handle::from_memory(
                domain_drafts::get_small(&proposal.id).expect("small draft for every proposal"),
            ))
            .width(16)
            .height(16)
            .style(move |_, _| svg::Style {
                color: Some(theme.tokens().text),
            });
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
                        container(
                            row![small_preview, preview]
                                .spacing(8)
                                .align_y(Alignment::Center)
                        )
                        .width(66)
                        .center_x(Fill),
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
    fn chrome_mode(&self) -> ChromeMode {
        if self.page == Page::Studios && studios()[self.selected_studio].id == "energy" {
            ChromeMode::Workflow
        } else if self.page == Page::Studios && studios()[self.selected_studio].id == "speech" {
            ChromeMode::Sidebar
        } else if self.page == Page::Studios && studios()[self.selected_studio].id == "field" {
            ChromeMode::TopNav
        } else if self.page == Page::Studios && studios()[self.selected_studio].id == "cad" {
            ChromeMode::CanvasRibbon
        } else {
            ChromeMode::Ribbon
        }
    }
    fn tab_event(&mut self, id: &str) -> Task<Action> {
        if self.chrome_mode() == ChromeMode::TopNav {
            if let Some(index) = studios()[self.selected_studio].tabs.iter()
                .position(|tab| tab.to_lowercase() == id) {
                self.selected_screen = index;
                self.field_review_notice = None;
            }
        }
        Task::none()
    }
    fn ribbon(&self, l: Language) -> Vec<RibbonTab<Action>> {
        if self.page == Page::Studios {
            if matches!(self.chrome_mode(), ChromeMode::Workflow | ChromeMode::Sidebar) {
                return Vec::new();
            }
            return ribbon_preview::studio_tabs_with_controls(
                &studios()[self.selected_studio],
                self.selected_preview_command.as_deref(),
                self.pile_view,
                self.frame_view,
                self.pdf_image,
                self.pdf_arrange,
                self.pdf_format.clone(),
            );
        }
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
    fn file_active_label(&self, l: Language) -> Option<String> {
        Some(self.page.title(l).into())
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
        let bg = theme.tokens().bg;
        container(scrollable(container(content).padding(28).width(Fill)).height(Fill))
            .width(Fill)
            .height(Fill)
            .style(move |_| container::Style::default().background(bg))
            .into()
    }
    fn overlay(&self, theme: Theme, l: Language) -> Option<Element<'_, Action>> {
        if !self.sample_dialog { return None; }
        let body = container(column![
            text(l.text("Projectnaam", "Project name")).size(12),
            text_input(l.text("Typ een naam", "Type a name"), &self.sample_dialog_input)
                .on_input(Action::SampleDialogInput)
                .style(move |_, status| widgets::text_input_style(theme, status))
                .width(Fill),
            text(l.text("Deze dialoog gebruikt de algemene OpenAEC-modal.",
                "This dialog uses the general OpenAEC modal.")).size(12),
        ].spacing(10)).padding(18).width(Fill).into();
        let footer = row![
            Space::with_width(Fill),
            widgets::dialog_button(l.text("Annuleren", "Cancel"),
                move |_, status| widgets::secondary_button_style(theme, status))
                .on_press(Action::SampleDialog(false)),
            widgets::dialog_button(l.text("Opslaan", "Save"),
                move |_, status| widgets::primary_button_style(theme, status))
                .on_press(Action::SampleDialogSave),
        ].spacing(6).align_y(Alignment::Center).into();
        Some(widgets::dialog_modal(l.text("Voorbeelddialoog", "Sample dialog"),
            body, footer, Action::SampleDialog(false), 480.0, theme))
    }
    fn escape(&self) -> Option<Action> {
        self.sample_dialog.then_some(Action::SampleDialog(false))
    }
    fn explorer(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        if self.page == Page::Studios && studios()[self.selected_studio].id == "geotech" && self.selected_screen == 1 {
            return geotech_native::explorer(theme);
        }
        if self.chrome_mode() == ChromeMode::CanvasRibbon {
            return column![
                widgets::property("Object", "Polyline", theme),
                widgets::property("Kleur", "ByLayer", theme),
                widgets::property("Laag", "Defpoints", theme),
                widgets::property("Lijntype", "ByLayer", theme),
                widgets::property("Lijngewicht", "ByLayer", theme),
            ].spacing(2).into();
        }
        if self.chrome_mode() == ChromeMode::Sidebar {
            let studio = &studios()[self.selected_studio];
            let mut nav = Column::new().spacing(4);
            for (index, screen) in studio.screens.iter().enumerate() {
                nav = nav.push(button(text(screen_label(screen, l)).size(12))
                    .padding([10, 12]).width(Fill).on_press(Action::SelectScreen(index))
                    .style(move |_, status| widgets::button_style(theme, index == self.selected_screen, status)));
            }
            return nav.into();
        }
        if self.chrome_mode() == ChromeMode::Workflow {
            let t = theme.tokens();
            let steps = self.energy_mode.steps(l);
            let mut nav = Column::new().spacing(4).push(
                self.card(column![
                    text(if self.energy_mode.existing() {
                        l.text("Voorbeeld bestaande bouw", "Existing-building example")
                    } else {
                        l.text("Voorbeeld nieuwbouw", "New-build example")
                    })
                        .font(fonts::STRONG).size(13),
                    text(self.energy_mode.label(l))
                        .size(11).color(t.text_secondary),
                ].spacing(4), theme),
            );
            for (index, step) in steps.iter().enumerate() {
                if step.more {
                    nav = nav.push(text(l.text("MEER", "MORE")).font(fonts::STRONG).size(10).color(t.text_secondary));
                }
                let number = if step.more { format!("›  {}", step.label) } else { format!("{:02}  {}", index + 1, step.label) };
                nav = nav.push(button(text(number).size(12))
                    .padding([9, 10]).width(Fill)
                    .on_press(Action::SelectEnergyStep(index))
                    .style(move |_, status| widgets::button_style(theme, index == self.selected_energy_step, status)));
                if index == self.selected_energy_step {
                    for (sub_index, sub) in step.subs.iter().enumerate() {
                        nav = nav.push(button(text(format!("    {sub}")).size(11))
                            .padding([5, 9]).width(Fill)
                            .on_press(Action::SelectEnergySub(sub_index))
                            .style(move |_, status| widgets::button_style(theme, self.selected_energy_sub == Some(sub_index), status)));
                    }
                }
            }
            nav = nav.push(text(l.text("Gereedschap · Instellingen", "Tools · Settings"))
                .size(11).color(t.text_secondary));
            return nav.into();
        }
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
        if self.page == Page::Studios && studios()[self.selected_studio].id == "geotech" && self.selected_screen == 1 {
            return geotech_native::properties(self.geotech_layer, theme);
        }
        column![
            widgets::property_grid_row(l.text("Pagina", "Page"), self.page.title(l), theme),
            widgets::property_grid_row(l.text("Thema", "Theme"), theme.to_string(), theme),
            widgets::property_grid_row(
                l.text("Canonieke iconen", "Canonical icons"),
                Icon::ALL.len().to_string(),
                theme
            ),
            widgets::property_grid_row(
                l.text("UI-broniconen", "UI source icons"),
                source_icons::ALL.len().to_string(),
                theme
            ),
            widgets::property_grid_row(
                l.text("FEM/BIM-voorstellen", "FEM/BIM proposals"),
                proposals().len().to_string(),
                theme
            ),
        ]
        .spacing(0)
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
            Action::SampleDialog(open) => {
                if open { self.sample_dialog_input = self.sample_input.clone(); }
                self.sample_dialog = open;
            }
            Action::SampleDialogInput(value) => self.sample_dialog_input = value,
            Action::SampleDialogSave => {
                self.sample_input.clone_from(&self.sample_dialog_input);
                self.sample_dialog = false;
            }
            Action::Reset => {
                self.sample_input.clear();
                self.sample_toggle = false;
                self.sample_value = 35.0;
            }
            Action::SelectStudio(index) => {
                self.selected_studio = index.min(studios().len().saturating_sub(1));
                self.selected_screen = 0;
                self.speech_notice = None;
                self.selected_preview_command = None;
                self.selected_energy_step = 0;
                self.selected_energy_sub = self.energy_mode.existing().then_some(0);
                self.show(Page::Studios);
            }
            Action::SelectScreen(index) => {
                self.selected_screen = index.min(
                    studios()[self.selected_studio]
                        .screens
                        .len()
                        .saturating_sub(1),
                );
                self.field_review_notice = None;
                self.speech_notice = None;
            }
            Action::GeotechLayer(index) => self.geotech_layer = index.min(geotech_native::LAYERS.len() - 1),
            Action::FieldProjectEdit(index, value) => {
                if let Some(field) = self.field_project.values.get_mut(index) { *field = value; }
            }
            Action::FieldProjectPreview(message) => self.field_project.notice = Some(message),
            Action::FieldConnectorPreview(name) => self.field_connector_notice = Some(name),
            Action::FieldExportType(index) => self.field_export_type = index.min(3),
            Action::FieldExportPhotos(value) => self.field_export_photos = value,
            Action::FieldExportMap(value) => self.field_export_map = value,
            Action::FieldExportPreview(format) => self.field_export_notice = Some(format),
            Action::FieldFlowSetup(mode) => { self.field_flow_mode = Some(mode); self.field_flow_notice = None; }
            Action::FieldFlowCancel => { self.field_flow_mode = None; self.field_flow_notice = None; }
            Action::FieldFlowEdit(inspection, index, value) => {
                if inspection {
                    if let Some(field) = self.field_inspection_values.get_mut(index) { *field = value; }
                } else if let Some(field) = self.field_handover_values.get_mut(index) { *field = value; }
            }
            Action::FieldFlowType(inspection, index) => {
                if inspection { self.field_inspection_type = index.min(1); }
                else { self.field_handover_type = index.min(2); }
            }
            Action::FieldFlowPreview(message) => self.field_flow_notice = Some(message),
            Action::FieldReviewPreview(message) => self.field_review_notice = Some(message),
            Action::FieldCaptureFilter(group, index) => {
                if let Some(filter) = self.field_capture_filter.get_mut(group) { *filter = index; }
            }
            Action::SpeechPreview(message) => self.speech_notice = Some(message),
            Action::SpeechDictionaryEdit(word, value) => {
                if word { self.speech_word = value; } else { self.speech_replacement = value; }
            }
            Action::SpeechDictionaryAdd => {
                let word = self.speech_word.trim().to_owned();
                if !word.is_empty() {
                    self.speech_dictionary.push((word, self.speech_replacement.trim().to_owned()));
                    self.speech_word.clear();
                    self.speech_replacement.clear();
                }
            }
            Action::SpeechSettingsTab(index) => self.speech_settings_tab = index.min(4),
            Action::SpeechTtsInput(value) => self.speech_tts_text = value,
            Action::SpeechTtsSpeed(value) => self.speech_tts_speed = value.clamp(0.5, 2.0),
            Action::SelectPreviewCommand(id) => self.selected_preview_command = Some(id),
            Action::PileSymbolScale(value) => self.pile_view.symbol_scale = value.clamp(10.0, 200.0),
            Action::PileUtilizationMinimum(value) => {
                self.pile_view.utilization_minimum = value.clamp(0.0, self.pile_view.utilization_maximum);
            }
            Action::PileUtilizationMaximum(value) => {
                self.pile_view.utilization_maximum = value.clamp(self.pile_view.utilization_minimum, 100.0);
            }
            Action::PileForeground(index) => self.pile_view.foreground = index.min(1),
            Action::FrameTemplate(index) => self.frame_view.template = index.min(7),
            Action::FrameLod(index) => self.frame_view.lod = index.min(2),
            Action::FrameTheme(index) => self.frame_view.theme = index.min(6),
            Action::PdfCrop => self.pdf_image.crop = !self.pdf_image.crop,
            Action::PdfGrayscale => self.pdf_image.grayscale = !self.pdf_image.grayscale,
            Action::PdfBrightness(value) => self.pdf_image.brightness = value.round().clamp(0.0, 200.0),
            Action::PdfContrast(value) => self.pdf_image.contrast = value.round().clamp(0.0, 200.0),
            Action::PdfResetImage => {
                self.pdf_image.grayscale = false;
                self.pdf_image.brightness = 100.0;
                self.pdf_image.contrast = 100.0;
            }
            Action::PdfAlignTarget(index) => self.pdf_arrange.align_target = index.min(1),
            Action::PdfFormatStyle(index) => self.pdf_format.select_style(index),
            Action::PdfFormatToggleGallery => {
                self.pdf_format.style_gallery_open = !self.pdf_format.style_gallery_open;
                self.pdf_format.open_palette = None;
                self.pdf_format.custom_open = false;
            }
            Action::PdfFormatCloseGallery => self.pdf_format.style_gallery_open = false,
            Action::PdfFormatFill(index) => self.pdf_format.select_fill(index),
            Action::PdfFormatNoFill => self.pdf_format.clear_fill(),
            Action::PdfFormatStroke(index) => self.pdf_format.select_stroke(index),
            Action::PdfFormatCustomToggle => {
                if let Some(palette) = self.pdf_format.open_palette {
                    self.pdf_format.custom_open = !self.pdf_format.custom_open;
                    let color = if palette == 0 { self.pdf_format.fill_color } else { self.pdf_format.stroke_color };
                    self.pdf_format.custom_draft = format!("#{:02x}{:02x}{:02x}",
                        (color.r * 255.0).round() as u8, (color.g * 255.0).round() as u8,
                        (color.b * 255.0).round() as u8);
                }
            }
            Action::PdfFormatCustomHex(value) => {
                if value.len() <= 7 && (value.is_empty() ||
                    (value.starts_with('#') && value[1..].bytes().all(|byte| byte.is_ascii_hexdigit()))) {
                    self.pdf_format.custom_draft = value;
                }
            }
            Action::PdfFormatCustomApply => self.pdf_format.apply_custom(),
            Action::PdfFormatLineWidth(value) => {
                if value.is_empty() || value == "." ||
                    value.parse::<f32>().is_ok_and(|number| (0.0..=50.0).contains(&number)) {
                    self.pdf_format.line_width = value;
                }
            }
            Action::PdfFormatBorder(index) => self.pdf_format.border = index.min(2),
            Action::PdfFormatBlend(index) => self.pdf_format.blend = index.min(1),
            Action::PdfFormatOpacity(value) => self.pdf_format.set_opacity(value),
            Action::PdfFormatOpacityText(value) => self.pdf_format.edit_opacity(value),
            Action::PdfFormatArrowStart(index) => self.pdf_format.arrow_start = index.min(7),
            Action::PdfFormatArrowEnd(index) => self.pdf_format.arrow_end = index.min(7),
            Action::PdfFormatLayer(index) => {
                if index == 0 { self.pdf_format.layer = index; }
            }
            Action::PdfFormatSymbolStamp => self.pdf_format.symbol_stamp = !self.pdf_format.symbol_stamp,
            Action::PdfFormatTogglePalette(index) => {
                let index = index.min(1);
                self.pdf_format.open_palette = (self.pdf_format.open_palette != Some(index)).then_some(index);
                self.pdf_format.custom_open = false;
                self.pdf_format.style_gallery_open = false;
            }
            Action::PdfFormatClosePalette => {
                self.pdf_format.open_palette = None;
                self.pdf_format.custom_open = false;
            }
            Action::SelectEnergyStep(index) => {
                let steps = self.energy_mode.steps(Language::Dutch);
                self.selected_energy_step = index.min(steps.len().saturating_sub(1));
                self.selected_energy_sub = (!steps[self.selected_energy_step].subs.is_empty()).then_some(0);
            }
            Action::SelectEnergySub(index) => {
                let steps = self.energy_mode.steps(Language::Dutch);
                let subs = &steps[self.selected_energy_step.min(steps.len() - 1)].subs;
                self.selected_energy_sub = (index < subs.len()).then_some(index);
            }
            Action::SelectEnergyMode(mode) => {
                self.energy_mode = mode;
                self.selected_energy_step = 0;
                self.selected_energy_sub = mode.existing().then_some(0);
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
        let canonical: HashSet<_> = Icon::ALL.iter().map(|icon| icon.id()).collect();
        assert_eq!(canonical.len(), Icon::ALL.len());
        assert!(source_icons::ALL.len() >= 577);
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
        assert_eq!(domain_drafts::SMALL.len(), 13);
        assert!(domain_drafts::SMALL
            .iter()
            .all(|(id, bytes)| domain_drafts::get(id).is_some()
                && domain_drafts::get_small(id) == Some(*bytes)));
        assert_eq!(studios().len(), 18);
        let required_screens = [
            "start",
            "workspace",
            "backstage",
            "settings",
            "import-export",
            "long-running-operation",
            "unsaved-changes",
            "empty",
            "error",
        ];
        assert!(studios()
            .iter()
            .filter(|studio| !matches!(studio.id.as_str(), "speech" | "field"))
            .all(|studio| studio.screens.len() == required_screens.len()
                && required_screens
                    .iter()
                    .all(|screen| studio.screens.iter().any(|id| id == screen))));
        assert_eq!(studios().iter().find(|studio| studio.id == "speech").unwrap().screens,
            ["speech", "transcribe", "meeting", "mic-test", "models", "dictionary", "tts", "settings", "about"]);
        assert_eq!(studios().iter().find(|studio| studio.id == "field").unwrap().screens,
            ["project", "plattegrond", "ifc", "opname", "inspectie", "oplevering", "dashboard", "export", "koppelingen", "handleiding"]);
    }

    #[test]
    fn native_atlas_opens_every_studio_and_screen() {
        let mut app = StyleRepo::default();
        for studio in 0..studios().len() {
            let _ = app.update(Action::SelectStudio(studio));
            assert_eq!(app.selected_studio, studio);
            for screen in 0..studios()[studio].screens.len() {
                let _ = app.update(Action::SelectScreen(screen));
                assert_eq!(app.selected_screen, screen);
                let _ = app.studios_page(Theme::Light, Language::Dutch);
            }
        }
    }

    #[test]
    fn native_ribbon_uses_proposed_tabs_except_workflow_studios() {
        let mut app = StyleRepo::default();
        app.show(Page::Studios);
        for (index, studio) in studios().iter().enumerate() {
            let _ = app.update(Action::SelectStudio(index));
            let tabs = app.ribbon(Language::Dutch);
            if studio.id == "energy" || studio.id == "speech" {
                assert_eq!(app.chrome_mode(), if studio.id == "energy" { ChromeMode::Workflow } else { ChromeMode::Sidebar });
                assert!(tabs.is_empty());
                continue;
            }
            if studio.id == "field" {
                assert_eq!(app.chrome_mode(), ChromeMode::TopNav);
                assert_eq!(tabs.len(), 10);
                assert!(tabs.iter().all(|tab| tab.groups.is_empty()));
                continue;
            }
            assert_eq!(app.chrome_mode(), if studio.id == "cad" { ChromeMode::CanvasRibbon } else { ChromeMode::Ribbon });
            let expected: Vec<_> = studio.tabs.iter().filter(|tab| *tab != "Bestand").collect();
            assert_eq!(tabs.len(), expected.len(), "{}", studio.name);
            for (actual, label) in tabs.iter().zip(expected) {
                let expected_label = if studio.optional_tabs.contains(label) { format!("{label} · optioneel") } else { (*label).clone() };
                assert_eq!(actual.label, expected_label, "{}", studio.name);
                if matches!(studio.id.as_str(), "heatloss" | "calculations") && label == "IFC" {
                    assert!(actual.groups.is_empty(), "source IFC ribbon is intentionally empty");
                    continue;
                }
                assert!(!actual.groups.is_empty(), "{} / {}", studio.name, label);
                assert!(actual.groups.iter().all(|group| !group.commands.is_empty()));
            }
        }
    }

    #[test]
    fn calc_ribbon_tracks_source_tabs_and_command_groups() {
        let calc = studios().iter().find(|studio| studio.id == "calc").unwrap();
        assert_eq!(
            calc.tabs,
            [
                "Bestand",
                "Begroting",
                "Offerte",
                "Rapportage",
                "Spreadsheet",
                "3D",
                "PDF",
                "IFC",
                "Tekstopmaak"
            ]
        );
        assert_eq!(calc.optional_tabs, ["Offerte", "3D", "PDF", "Tekstopmaak"]);
        let tabs = ribbon_preview::studio_tabs(calc, None);
        let budget = tabs.iter().find(|tab| tab.id == "begroting").unwrap();
        let groups: Vec<_> = budget
            .groups
            .iter()
            .map(|group| group.label.as_str())
            .collect();
        assert!(groups.starts_with(&["Regels", "Klembord", "Geschiedenis", "Panelen", "Weergave"]));
        assert!(groups.contains(&"Varianten"));
        assert_eq!(
            tabs.iter().find(|tab| tab.id == "ifc").unwrap().groups[0].label,
            "Rapport"
        );
    }

    #[test]
    fn geotech_ribbon_tracks_core_and_extension_tabs() {
        let studio = studios().iter().find(|studio| studio.id == "geotech").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Home", "Kaart", "Rapport", "Situatietekening", "Berekeningen", "IFC"]);
        assert_eq!(studio.optional_tabs, ["Situatietekening", "Berekeningen"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        let map = tabs.iter().find(|tab| tab.id == "kaart").unwrap();
        assert_eq!(map.groups[0].label, "Kaart");
        assert_eq!(map.groups[0].commands.len(), 2);
        let drawing = tabs.iter().find(|tab| tab.id == "situatietekening").unwrap();
        assert_eq!(drawing.groups.len(), 5);
    }

    #[test]
    fn geotech_borehole_layers_follow_pinned_capture_and_select() {
        let layers = &geotech_native::LAYERS;
        assert_eq!(layers.len(), 13);
        assert_eq!((layers[0].top, layers[0].bottom), (0.30, 0.92));
        assert_eq!((layers[12].top, layers[12].bottom), (8.20, 8.40));
        for pair in layers.windows(2) {
            assert!((pair[0].bottom - pair[1].top).abs() < 0.001);
        }
        let mut app = StyleRepo::default();
        let geo = studios().iter().position(|studio| studio.id == "geotech").unwrap();
        let _ = app.update(Action::SelectStudio(geo));
        let _ = app.update(Action::SelectScreen(1));
        let _ = app.update(Action::GeotechLayer(12));
        assert_eq!(app.geotech_layer, 12);
        let _ = app.update(Action::GeotechLayer(100));
        assert_eq!(app.geotech_layer, 12);
    }

    #[test]
    fn heatloss_ribbon_tracks_route_tabs_and_empty_ifc() {
        let studio = studios().iter().find(|studio| studio.id == "heatloss").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Vertrekken", "Constructies", "Modeller", "IFC", "Resultaten", "Rapport"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs.iter().find(|tab| tab.id == "ifc").unwrap().groups.len(), 0);
        assert_eq!(tabs.iter().find(|tab| tab.id == "vertrekken").unwrap().groups.len(), 3);
    }

    #[test]
    fn calculations_ribbon_has_only_start_and_empty_ifc() {
        let studio = studios().iter().find(|studio| studio.id == "calculations").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Start", "IFC"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs.len(), 2);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Bestand", "Bewerken", "Invoegen", "Exporteren"]);
        assert!(tabs[1].groups.is_empty());
    }

    #[test]
    fn reports_ribbon_uses_three_source_tabs() {
        let studio = studios().iter().find(|studio| studio.id == "reports").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Start", "Invoegen", "Beeld"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs.len(), 3);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Klembord", "Blokken", "Pagina", "Controle", "Uitvoer"]);
        assert_eq!(tabs[2].groups[1].label, "Panelen");
    }

    #[test]
    fn validator_ribbon_uses_viewer_source_tabs() {
        let studio = studios().iter().find(|studio| studio.id == "validator").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Start", "Beeld"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Project", "Modellen", "Validatie", "BCF"]);
        assert_eq!(tabs[1].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Panelen", "3D Beeld", "Doorsnede"]);
    }

    #[test]
    fn pile_ribbon_uses_plan_and_control_groups() {
        let studio = studios().iter().find(|studio| studio.id == "pile").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Plan", "Weergave"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Project", "Inspecteren", "Selecteren", "Instellingen", "Vergrendelen", "Optimalisatie"]);
        assert_eq!(tabs[1].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Symbolen", "Benutting", "Voorgrond", "Grid", "Gebieden", "Vensters"]);
        assert!(matches!(tabs[1].groups[0].commands[0].control,
            Some(RibbonControl::Slider { minimum: 10.0, maximum: 200.0, .. })));
        assert!(matches!(tabs[1].groups[1].commands[0].control,
            Some(RibbonControl::Range { minimum: 0.0, maximum: 100.0, .. })));
        assert!(matches!(tabs[1].groups[2].commands[0].control,
            Some(RibbonControl::Segmented { selected: 0, .. })));
    }

    #[test]
    fn pile_ribbon_control_updates_keep_a_valid_range() {
        let mut app = StyleRepo::default();
        let pile = studios().iter().position(|studio| studio.id == "pile").unwrap();
        let _ = app.update(Action::SelectStudio(pile));
        let _ = app.update(Action::PileSymbolScale(250.0));
        let _ = app.update(Action::PileUtilizationMinimum(95.0));
        let _ = app.update(Action::PileUtilizationMaximum(5.0));
        let _ = app.update(Action::PileForeground(1));
        assert_eq!(app.pile_view.symbol_scale, 200.0);
        assert_eq!(app.pile_view.utilization_minimum, 80.0);
        assert_eq!(app.pile_view.utilization_maximum, 80.0);
        let tabs = app.ribbon(Language::Dutch);
        assert!(matches!(tabs[1].groups[1].commands[0].control,
            Some(RibbonControl::Range { lower: 80.0, upper: 80.0, .. })));
        assert!(matches!(tabs[1].groups[2].commands[0].control,
            Some(RibbonControl::Segmented { selected: 1, .. })));
    }

    #[test]
    fn frame_ribbon_uses_source_tabs_and_groups() {
        let studio = studios().iter().find(|studio| studio.id == "frame").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Home", "Invoegen", "IFC / Export", "Productie", "Beeld"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Sjabloon", "Nieuw kozijn", "Bewerken", "Importeren"]);
        assert_eq!(tabs[1].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Onderverdeling", "Paneel type", "Vliesgevel"]);
        assert_eq!(tabs[2].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Kozijn exporteren", "IFC Import", "Validatie", "Project exporteren", "Werkplaats", "3D Export", "Blender / Bonsai"]);
        assert_eq!(tabs[4].groups[1].label, "Zoom");
        assert!(matches!(tabs[0].groups[0].commands[0].control,
            Some(RibbonControl::Select { selected: 0, width: 192.0, .. })));
        assert!(matches!(tabs[2].groups[0].commands[2].control,
            Some(RibbonControl::Select { selected: 1, width: 112.0, .. })));
        assert!(matches!(tabs[4].groups[2].commands[0].control,
            Some(RibbonControl::Select { selected: 0, width: 192.0, .. })));
    }

    #[test]
    fn frame_ribbon_keeps_source_select_values() {
        let mut app = StyleRepo::default();
        let frame = studios().iter().position(|studio| studio.id == "frame").unwrap();
        let _ = app.update(Action::SelectStudio(frame));
        let _ = app.update(Action::FrameTemplate(6));
        let _ = app.update(Action::FrameLod(2));
        let _ = app.update(Action::FrameTheme(5));
        let tabs = app.ribbon(Language::Dutch);
        assert!(matches!(tabs[0].groups[0].commands[0].control,
            Some(RibbonControl::Select { selected: 6, .. })));
        assert!(matches!(tabs[2].groups[0].commands[2].control,
            Some(RibbonControl::Select { selected: 2, .. })));
        assert!(matches!(tabs[4].groups[2].commands[0].control,
            Some(RibbonControl::Select { selected: 5, .. })));
    }

    #[test]
    fn field_top_navigation_tracks_source_pages() {
        let mut app = StyleRepo::default();
        let field = studios().iter().position(|studio| studio.id == "field").unwrap();
        let _ = app.update(Action::SelectStudio(field));
        assert_eq!(app.chrome_mode(), ChromeMode::TopNav);
        let tabs = app.ribbon(Language::Dutch);
        assert_eq!(tabs.len(), 10);
        assert!(tabs.iter().all(|tab| tab.groups.is_empty()));
        assert_eq!(app.field_project.values[0], "Renovatie Damrak 1");
        let _ = app.update(Action::FieldProjectEdit(0, "Nieuwe opname".into()));
        assert_eq!(app.field_project.values[0], "Nieuwe opname");
        let _ = app.update(Action::FieldProjectEdit(usize::MAX, "genegeerd".into()));
        assert_eq!(app.field_project.values[0], "Nieuwe opname");
        let _ = app.update(Action::FieldProjectPreview("BAG-review"));
        assert_eq!(app.field_project.notice, Some("BAG-review"));
        let _ = app.tab_event("koppelingen");
        assert_eq!(app.selected_screen, 8);
        let _ = app.update(Action::FieldConnectorPreview("ERPNext (Frappe)"));
        assert_eq!(app.field_connector_notice, Some("ERPNext (Frappe)"));
        let _ = app.tab_event("export");
        assert_eq!(app.selected_screen, 7);
        let _ = app.update(Action::FieldExportType(2));
        let _ = app.update(Action::FieldExportPhotos(false));
        let _ = app.update(Action::FieldExportMap(false));
        let _ = app.update(Action::FieldExportPreview("PDF"));
        assert_eq!(app.field_export_type, 2);
        assert!(!app.field_export_photos && !app.field_export_map);
        assert_eq!(app.field_export_notice, Some("PDF"));
        let _ = app.tab_event("inspectie");
        let _ = app.update(Action::FieldFlowSetup("inspectie"));
        let _ = app.update(Action::FieldFlowEdit(true, 0, "Gevelinspectie".into()));
        let _ = app.update(Action::FieldFlowType(true, 1));
        assert_eq!(app.field_flow_mode, Some("inspectie"));
        assert_eq!(app.field_inspection_values[0], "Gevelinspectie");
        assert_eq!(app.field_inspection_type, 1);
        let _ = app.update(Action::FieldFlowCancel);
        assert_eq!(app.field_flow_mode, None);
        let _ = app.tab_event("oplevering");
        let _ = app.update(Action::FieldFlowSetup("oplevering"));
        let _ = app.update(Action::FieldFlowEdit(false, 1, "Controlepunten".into()));
        let _ = app.update(Action::FieldFlowType(false, 2));
        assert_eq!(app.field_handover_values[1], "Controlepunten");
        assert_eq!(app.field_handover_type, 2);
        let _ = app.tab_event("plattegronden");
        assert_eq!(app.selected_screen, 1);
        let _ = app.tab_event("3d bim");
        assert_eq!(app.selected_screen, 2);
        let _ = app.tab_event("opname");
        assert_eq!(app.selected_screen, 3);
        let _ = app.update(Action::FieldCaptureFilter(0, 2));
        let _ = app.update(Action::FieldCaptureFilter(usize::MAX, 1));
        assert_eq!(app.field_capture_filter, [2, 0, 0]);
        let _ = app.update(Action::FieldReviewPreview("Ticket toevoegen"));
        assert_eq!(app.field_review_notice, Some("Ticket toevoegen"));
        let _ = app.tab_event("handleiding");
        assert_eq!(app.selected_screen, 9);
        let _ = app.tab_event("project");
        assert_eq!(app.field_project.values[0], "Nieuwe opname");
    }

    #[test]
    fn speech_dictionary_is_a_local_native_review() {
        let mut app = StyleRepo::default();
        let speech = studios().iter().position(|studio| studio.id == "speech").unwrap();
        let _ = app.update(Action::SelectStudio(speech));
        let _ = app.update(Action::SelectScreen(5));
        let _ = app.update(Action::SpeechDictionaryEdit(true, "OpenAEC".into()));
        let _ = app.update(Action::SpeechDictionaryEdit(false, "Open A E C".into()));
        let _ = app.update(Action::SpeechDictionaryAdd);
        assert_eq!(app.speech_dictionary, [("OpenAEC".into(), "Open A E C".into())]);
        assert!(app.speech_word.is_empty() && app.speech_replacement.is_empty());
        let _ = app.update(Action::SpeechDictionaryAdd);
        assert_eq!(app.speech_dictionary.len(), 1);
        let _ = app.update(Action::SpeechPreview("Bestandsselectie"));
        assert_eq!(app.speech_notice, Some("Bestandsselectie"));
        let _ = app.update(Action::SelectScreen(7));
        assert_eq!(app.speech_notice, None);
        let _ = app.update(Action::SpeechSettingsTab(4));
        assert_eq!(app.speech_settings_tab, 4);
        let _ = app.update(Action::SelectScreen(6));
        let _ = app.update(Action::SpeechTtsInput("OpenAEC".into()));
        let _ = app.update(Action::SpeechTtsSpeed(5.0));
        assert_eq!(app.speech_tts_text, "OpenAEC");
        assert_eq!(app.speech_tts_speed, 2.0);
    }

    #[test]
    fn aec_extension_adds_only_its_two_tabs_and_ifcx_commands() {
        let studio = studios().iter().find(|studio| studio.id == "2d").unwrap();
        assert_eq!(studio.tabs, ["AEC", "Pile Plan", "IFC"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Elements", "Annotations", "Connections", "Reference", "Properties"]);
        assert_eq!(tabs[1].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Place", "CPT Data"]);
        assert_eq!(tabs[2].groups[0].commands.iter().map(|command| command.label.as_str()).collect::<Vec<_>>(),
            ["Export IFCX", "Copy IFCX"]);
    }

    #[test]
    fn cad_ribbon_tracks_visible_core_modules_without_layout_tab() {
        let studio = studios().iter().find(|studio| studio.id == "cad").unwrap();
        assert_eq!(studio.tabs, ["Tekenen", "Parametrisch", "Model", "Invoegen", "Annoteren", "Beeld", "Beheren"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Draw", "Modify", "Annotation", "Layers", "Block", "Properties", "Groups", "Clipboard", "Measure"]);
        assert_eq!(tabs[6].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Customization", "Cleanup", "Application"]);
    }

    #[test]
    fn pointcloud_ribbon_matches_current_single_tab_and_ten_panels() {
        let studio = studios().iter().find(|studio| studio.id == "pointcloud").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Start"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs.len(), 1);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Bestand", "Navigatie", "Selectie", "Snedebox", "Oppervlak", "Tekening", "Meten", "Annotatie", "Index", "Export"]);
    }

    #[test]
    fn pdf_ribbon_separates_core_and_contextual_tabs() {
        let studio = studios().iter().find(|studio| studio.id == "pdf").unwrap();
        assert_eq!(studio.tabs, ["Bestand", "Start", "Beeld", "Tekenen", "Annotatie", "PDF bewerken & samenvoegen", "Help", "Opmaak", "Schikken", "Afbeelding"]);
        assert_eq!(studio.optional_tabs, ["Opmaak", "Schikken", "Afbeelding"]);
        let tabs = ribbon_preview::studio_tabs(studio, None);
        assert_eq!(tabs.len(), 9);
        assert_eq!(tabs[0].groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Document", "Hulpmiddelen", "Beeld", "Navigeren", "Zoeken", "Instellingen"]);
        assert!(tabs[3].groups.iter().any(|group| group.label == "METEN"));
        let format = &tabs[6].groups;
        assert_eq!(format.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Stijlen", "Kleur", "Lijn & dekking", "Pijlen", "Gereedschap", "Eigenschappen"]);
        assert!(matches!(&format[0].commands[0].control,
            Some(RibbonControl::StyleGallery { items, visible: 8, .. })
                if items.len() == 10 && items.iter().enumerate()
                    .all(|(index, item)| item.dashed_border == (index >= 7))));
        assert!(matches!(&format[1].commands[0].control,
            Some(RibbonControl::ColorSelect { options, selected: 0, .. }) if options.len() == 42));
        assert!(matches!(&format[1].commands[1].control,
            Some(RibbonControl::ColorSelect { options, selected: 5, .. }) if options.len() == 42));
        assert!(matches!(&format[2].commands[0].control,
            Some(RibbonControl::FormStack { fields, .. }) if fields.len() == 4 &&
                matches!(&fields[0], openaec_ui::RibbonFormField::Number { value, .. } if value == "1") &&
                matches!(&fields[3], openaec_ui::RibbonFormField::Slider { value: 100.0, .. })));
        assert!(matches!(&format[3].commands[0].control,
            Some(RibbonControl::FormStack { fields, .. }) if fields.len() == 2));
        let arrange = &tabs[7].groups;
        assert_eq!(arrange.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Uitlijning", "Verdelen", "Grootte", "Draaien", "Spiegelen", "Z-volgorde"]);
        assert_eq!(arrange.iter().map(|group| group.commands.len()).collect::<Vec<_>>(),
            [7, 8, 3, 3, 2, 4]);
        assert_eq!(arrange[0].commands[0].label, "Links");
        assert_eq!(arrange[5].commands[3].label, "Naar achtergrond");
        assert!(arrange.iter().flat_map(|group| &group.commands)
            .filter(|command| command.control.is_none())
            .all(|command| matches!(command.icon, CommandIcon::Svg(bytes) if !bytes.is_empty())));
        assert!(matches!(&arrange[0].commands[6].control,
            Some(RibbonControl::Select { options, selected: 0, .. }) if options.len() == 2));
        let image = &tabs[8].groups;
        assert_eq!(image.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(), ["Bijsnijden", "Beeldbewerking"]);
        assert_eq!(image[0].commands[0].label, "Croppen");
        assert_eq!(image[1].commands[0].label, "Grijswaarden");
        assert_eq!(image[1].commands[1].label, "Herstellen");
        assert!(matches!(&image[1].commands[2].control,
            Some(RibbonControl::Sliders { minimum: 0.0, maximum: 200.0, items, .. })
                if items.len() == 2 && items[0].value == 100.0 && items[1].value == 100.0));
    }

    #[test]
    fn pdf_image_controls_update_and_reset_to_source_defaults() {
        let mut app = StyleRepo::default();
        let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
        let _ = app.update(Action::SelectStudio(pdf));
        let _ = app.update(Action::PdfCrop);
        let _ = app.update(Action::PdfGrayscale);
        let _ = app.update(Action::PdfBrightness(220.0));
        let _ = app.update(Action::PdfContrast(48.6));
        assert!(app.pdf_image.crop && app.pdf_image.grayscale);
        assert_eq!((app.pdf_image.brightness, app.pdf_image.contrast), (200.0, 49.0));
        let _ = app.update(Action::PdfResetImage);
        assert!(app.pdf_image.crop);
        assert!(!app.pdf_image.grayscale);
        assert_eq!((app.pdf_image.brightness, app.pdf_image.contrast), (100.0, 100.0));
    }

    #[test]
    fn pdf_arrange_align_target_updates_native_selection() {
        let mut app = StyleRepo::default();
        let _ = app.update(Action::PdfAlignTarget(1));
        assert_eq!(app.pdf_arrange.align_target, 1);
        let studio = studios().iter().find(|studio| studio.id == "pdf").unwrap();
        let tabs = ribbon_preview::studio_tabs_with_controls(studio, None, app.pile_view, app.frame_view,
            app.pdf_image, app.pdf_arrange, app.pdf_format.clone());
        assert!(matches!(&tabs[7].groups[0].commands[6].control,
            Some(RibbonControl::Select { selected: 1, .. })));
        let _ = app.update(Action::PdfAlignTarget(9));
        assert_eq!(app.pdf_arrange.align_target, 1);
    }

    #[test]
    fn pdf_format_gallery_colors_and_symbol_context_follow_source_defaults() {
        let mut app = StyleRepo::default();
        let _ = app.update(Action::PdfFormatToggleGallery);
        assert!(app.pdf_format.style_gallery_open);
        let _ = app.update(Action::PdfFormatStyle(9));
        assert!(!app.pdf_format.style_gallery_open);
        let _ = app.update(Action::PdfFormatToggleGallery);
        let _ = app.update(Action::PdfFormatCloseGallery);
        assert!(!app.pdf_format.style_gallery_open);
        let _ = app.update(Action::PdfFormatTogglePalette(0));
        assert_eq!(app.pdf_format.open_palette, Some(0));
        let _ = app.update(Action::PdfFormatFill(9));
        assert_eq!(app.pdf_format.open_palette, None);
        assert!(app.pdf_format.has_fill);
        let _ = app.update(Action::PdfFormatTogglePalette(0));
        let _ = app.update(Action::PdfFormatNoFill);
        assert!(!app.pdf_format.has_fill);
        assert_eq!(app.pdf_format.open_palette, None);
        let _ = app.update(Action::PdfFormatTogglePalette(0));
        let _ = app.update(Action::PdfFormatCustomToggle);
        assert!(app.pdf_format.custom_open);
        let _ = app.update(Action::PdfFormatCustomHex("#12ab34".into()));
        let _ = app.update(Action::PdfFormatCustomApply);
        assert_eq!(app.pdf_format.fill_color, ribbon_preview::pdf_color("#12ab34"));
        assert!(app.pdf_format.has_fill);
        assert_eq!(app.pdf_format.fill, usize::MAX);
        assert_eq!(app.pdf_format.open_palette, None);
        let _ = app.update(Action::PdfFormatTogglePalette(1));
        assert_eq!(app.pdf_format.open_palette, Some(1));
        let _ = app.update(Action::PdfFormatCustomToggle);
        let _ = app.update(Action::PdfFormatCustomHex("#123".into()));
        let _ = app.update(Action::PdfFormatCustomApply);
        assert_eq!(app.pdf_format.open_palette, Some(1));
        let _ = app.update(Action::PdfFormatCustomHex("#badc0d".into()));
        let _ = app.update(Action::PdfFormatCustomApply);
        assert_eq!(app.pdf_format.stroke_color, ribbon_preview::pdf_color("#badc0d"));
        assert_eq!(app.pdf_format.open_palette, None);
        let _ = app.update(Action::PdfFormatTogglePalette(1));
        let _ = app.update(Action::PdfFormatClosePalette);
        assert_eq!(app.pdf_format.open_palette, None);
        let _ = app.update(Action::PdfFormatStyle(7));
        assert_eq!(app.pdf_format.style, 7);
        assert_eq!(app.pdf_format.stroke_color, ribbon_preview::pdf_color("#ff0000"));
        assert!((app.pdf_format.fill_color.a - 0.08).abs() < 0.001);
        let _ = app.update(Action::PdfFormatStroke(32));
        assert_eq!(app.pdf_format.stroke_color, ribbon_preview::pdf_color("#4a86e8"));
        assert_eq!(app.pdf_format.style, usize::MAX);
        let _ = app.update(Action::PdfFormatLineWidth("50.1".into()));
        assert_eq!(app.pdf_format.line_width, "1");
        let _ = app.update(Action::PdfFormatLineWidth("0.".into()));
        assert_eq!(app.pdf_format.line_width, "0.");
        let _ = app.update(Action::PdfFormatLineWidth("0.1".into()));
        assert_eq!(app.pdf_format.line_width, "0.1");
        let _ = app.update(Action::PdfFormatOpacity(72.6));
        assert_eq!((app.pdf_format.opacity, app.pdf_format.opacity_text.as_str()), (73.0, "73"));
        let _ = app.update(Action::PdfFormatOpacityText("".into()));
        assert_eq!((app.pdf_format.opacity, app.pdf_format.opacity_text.as_str()), (73.0, ""));
        let _ = app.update(Action::PdfFormatOpacityText("42".into()));
        assert_eq!((app.pdf_format.opacity, app.pdf_format.opacity_text.as_str()), (42.0, "42"));
        let _ = app.update(Action::PdfFormatOpacityText("101".into()));
        assert_eq!(app.pdf_format.opacity, 42.0);
        let _ = app.update(Action::PdfFormatSymbolStamp);
        let studio = studios().iter().find(|studio| studio.id == "pdf").unwrap();
        let tabs = ribbon_preview::studio_tabs_with_controls(studio, None, app.pile_view,
            app.frame_view, app.pdf_image, app.pdf_arrange, app.pdf_format.clone());
        assert_eq!(tabs[6].groups[0].label, "Symbooltype");
        assert!(matches!(tabs[6].groups[0].commands[0].icon, CommandIcon::Svg(_)));
    }

    #[test]
    fn fem_and_bim_ribbons_render_review_vectors_without_promoting_them() {
        let fem = ribbon_preview::studio_tabs(&studios()[2], None);
        let bim = ribbon_preview::studio_tabs(&studios()[3], None);
        for (tabs, label) in [(&fem, "Geometrie"), (&bim, "Modelleren")] {
            let tab = tabs.iter().find(|tab| tab.label == label).unwrap();
            let commands: Vec<_> = tab.groups.iter().flat_map(|g| &g.commands).collect();
            assert!(!commands.is_empty());
            assert!(commands.iter().all(|command| matches!(command.icon, CommandIcon::Svg(bytes) if !bytes.is_empty())));
        }
        let fem_net = fem.iter().find(|tab| tab.label == "Net").unwrap();
        let fem_compute = fem.iter().find(|tab| tab.label == "Berekenen").unwrap();
        assert_eq!(fem_net.groups[0].commands.len(), 3);
        assert!(fem_compute.groups[0].commands.len() > 3);
        assert!(Icon::ALL.len() < domain_drafts::ALL.len());
    }

    #[test]
    fn selected_draft_command_is_highlighted_for_review() {
        let mut app = StyleRepo::default();
        app.show(Page::Studios);
        let _ = app.update(Action::SelectStudio(2));
        let proposal = proposals().iter().find(|p| p.domain == "fem").unwrap();
        let _ = app.update(Action::SelectPreviewCommand(proposal.id.clone()));
        assert_eq!(app.selected_preview_command.as_deref(), Some(proposal.id.as_str()));
        let tabs = app.ribbon(Language::Dutch);
        assert!(tabs.iter().flat_map(|tab| &tab.groups).flat_map(|group| &group.commands)
            .any(|command| command.selected && command.label == proposal.label));
        let _ = app.preview_command_review(Theme::Light, Language::Dutch);
    }

    #[test]
    fn planner_preview_tracks_source_ribbon_groups_and_optional_ai() {
        let planner = studios().iter().find(|studio| studio.id == "planner").unwrap();
        let tabs = ribbon_preview::studio_tabs(planner, None);
        let start = tabs.iter().find(|tab| tab.id == "start").unwrap();
        assert_eq!(start.groups.iter().map(|group| group.label.as_str()).collect::<Vec<_>>(),
            ["Bestand", "Bewerken", "Taken", "Planning", "Zoom"]);
        assert!(start.groups[0].commands.iter().any(|command| matches!(command.icon, CommandIcon::Canonical(Icon::Save))));
        let planning = tabs.iter().find(|tab| tab.id == "planning").unwrap();
        assert_eq!(planning.groups.len(), 7);
        assert!(planning.groups[0].commands.iter().any(|command| matches!(command.icon, CommandIcon::Svg(bytes) if !bytes.is_empty())));
        assert_eq!(tabs.iter().find(|tab| tab.id == "ai").unwrap().label, "AI · optioneel");
    }
}
