//! Native Rust review of the source-pinned Workspace Composer sidebar and routes.
use super::*;
use openaec_ui::iced::widget::{column, row};

#[derive(Deserialize)]
pub(super) struct ComposerData {
    pub routes: Vec<ComposerRoute>,
    pub screenshots: Vec<ComposerScreenshot>,
    pub presets: Vec<ComposerPreset>,
    pub packages: Vec<ComposerPackage>,
}
#[derive(Deserialize)]
pub(super) struct ComposerRoute {
    pub path: String,
    pub component: String,
    pub mode: String,
    pub page_evidence: ComposerEvidence,
}
#[derive(Deserialize)]
pub(super) struct ComposerEvidence {
    pub file: String,
    pub line: usize,
}
#[derive(Deserialize)]
pub(super) struct ComposerScreenshot {
    pub route: String,
    pub local: String,
    pub state: String,
}
#[derive(Deserialize)]
pub(super) struct ComposerPreset {
    pub id: String,
    pub name: String,
    pub description: String,
    pub packages: Vec<String>,
}
#[derive(Deserialize)]
pub(super) struct ComposerPackage {
    pub id: String,
    pub name: String,
    pub description: String,
    pub category: String,
    pub skill_count: usize,
}

pub(super) fn data() -> &'static ComposerData {
    static DATA: OnceLock<ComposerData> = OnceLock::new();
    DATA.get_or_init(|| serde_json::from_str(include_str!("../../../harmonization/composer-screen-routes.json"))
        .expect("valid source-pinned Workspace Composer inventory"))
}

fn route_label(path: &str) -> &'static str {
    match path {
        "/workspace" => "Workspace", "/presets" => "Presets", "/install" => "Install",
        "/about" => "About", "/dashboard" => "Dashboard", "/configure" => "Settings",
        "/permissions" => "Permissions", "/hooks" => "Hooks", "/mcp" => "MCP Servers",
        "/templates" => "CLAUDE.md", "/commands" => "Commands", "/memory" => "Memory",
        "/prompts" => "Prompts", "/core-files" => "CORE Files", "/teams" => "Team Factory",
        "/gpu-server" => "GPU Server", "/auth" => "Authentication", "/git" => "Git",
        _ => "Unknown route",
    }
}
const SIMPLE: [&str; 4] = ["/workspace", "/presets", "/install", "/about"];
const ADVANCED: [&str; 18] = [
    "/dashboard", "/workspace", "/presets", "/install", "/configure", "/permissions",
    "/hooks", "/mcp", "/commands", "/memory", "/templates", "/core-files",
    "/prompts", "/teams", "/gpu-server", "/auth", "/git", "/about",
];

fn surface<'a>(theme: Theme, content: impl Into<Element<'a, Action>>, padding: u16) -> Element<'a, Action> {
    let t = theme.tokens();
    container(content).padding(padding).width(Fill)
        .style(move |_| container::Style::default().background(t.bg_lighter)
            .border(iced::Border::default().color(t.border).width(1))).into()
}

fn selectable_card<'a>(theme: Theme, selected: bool, content: impl Into<Element<'a, Action>>) -> Element<'a, Action> {
    let t = theme.tokens();
    container(content).padding(13).width(Fill).height(148)
        .style(move |_| container::Style::default().background(t.bg_lighter)
            .border(iced::Border::default().color(if selected { t.accent } else { t.border }).width(if selected { 2 } else { 1 })))
        .into()
}

impl StyleRepo {
    pub(super) fn composer_sidebar(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut nav = Column::new().spacing(5)
            .push(text("OpenAEC").font(fonts::HEADING).size(18).color(t.accent))
            .push(text("Workspace Composer").size(10).color(t.text_secondary))
            .push(Space::with_height(8))
            .push(row![
                button(text("Simple").size(11)).padding([6, 8]).width(Fill)
                    .on_press(Action::ComposerAdvanced(false))
                    .style(move |_, s| widgets::button_style(theme, !self.composer_advanced, s)),
                button(text("Advanced").size(11)).padding([6, 8]).width(Fill)
                    .on_press(Action::ComposerAdvanced(true))
                    .style(move |_, s| widgets::button_style(theme, self.composer_advanced, s)),
            ].spacing(3));
        let order: &[&str] = if self.composer_advanced { &ADVANCED } else { &SIMPLE };
        for path in order {
            let index = data().routes.iter().position(|route| route.path == *path)
                .expect("navigation path registered");
            nav = nav.push(button(text(route_label(path)).size(11)).padding([8, 10]).width(Fill)
                .on_press(Action::ComposerRoute(index))
                .style(move |_, s| widgets::button_style(theme, self.composer_route == index, s)));
        }
        let sidebar = column![
            scrollable(container(nav).padding(12)).height(Fill),
            container(text("v3.0.0 · OpenAEC Foundation").size(10).color(t.text_secondary)).padding(10),
        ].width(Fill).height(Fill);
        container(sidebar).width(Fill).height(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border::default().color(t.border).width(1))).into()
    }

    pub(super) fn composer_native_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let d = data();
        let route = &d.routes[self.composer_route];
        let choices: Vec<String> = studios().iter().map(|s| s.name.clone()).collect();
        let picker = pick_list(choices, Some("OpenAEC Workspace Composer".to_string()), |name| {
            Action::SelectStudio(studios().iter().position(|s| s.name == name).unwrap_or(0))
        }).width(255).style(move |_, s| widgets::pick_list_style(theme, s))
            .menu_style(move |_| widgets::pick_list_menu_style(theme));
        let heading = row![
            column![
                text("OPENAEC WORKSPACE COMPOSER · NATIVE RUST REVIEW")
                    .font(fonts::STRONG).size(10).color(t.accent),
                text(route_label(&route.path)).font(fonts::HEADING).size(24).color(t.text),
                text(format!("{} · {}", route.path, route.component)).size(11).color(t.text_secondary),
            ].spacing(5).width(Fill), picker,
        ].spacing(12).align_y(Alignment::Center);
        let body = match route.path.as_str() {
            "/workspace" => self.composer_package_page(theme),
            "/presets" => self.composer_presets_page(theme),
            "/install" => self.composer_install_page(theme),
            _ => surface(theme, column![
                text(route_label(&route.path)).font(fonts::HEADING).size(18),
                text("De route en component zijn uit de broncode bevestigd. Voor dit scherm ontbreekt een broncapture; pixelgelijkheid kan hier nog niet worden beoordeeld.")
                    .size(12).color(t.text_secondary),
            ].spacing(10), 22),
        };
        let mut page = Column::new().spacing(14).push(heading).push(body)
            .push(text(format!("BRON · {}:{} · commit 33327e0 · {}",
                route.page_evidence.file, route.page_evidence.line, route.mode))
                .size(10).color(t.text_secondary));
        if let Some(capture) = d.screenshots.iter().find(|s| s.route == route.path) {
            page = page.push(text(format!("BRONCAPTURE · {} · native layout hierboven ter vergelijking", capture.state))
                .font(fonts::STRONG).size(10).color(t.accent));
            let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(&capture.local);
            page = page.push(image(image::Handle::from_path(path)).width(Fill));
        } else {
            page = page.push(text("GEEN BRONCAPTURE · geen pixelgelijke claim")
                .font(fonts::STRONG).size(10).color(t.text_secondary));
        }
        container(scrollable(container(page).padding(18).width(Fill)).height(Fill))
            .width(Fill).height(Fill)
            .style(move |_| container::Style::default().background(t.bg)).into()
    }

    fn composer_package_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let d = data();
        let mut cards = Column::new().spacing(8);
        for chunk in d.packages.iter().collect::<Vec<_>>().chunks(3) {
            let mut line = Row::new().spacing(8);
            for pkg in chunk {
                let selected = self.composer_packages.contains(&pkg.id);
                line = line.push(button(selectable_card(theme, selected, column![
                    text(&pkg.name).font(fonts::STRONG).size(12),
                    text(&pkg.description).size(10).color(t.text_secondary),
                    text(format!("{} skills · {}", pkg.skill_count, pkg.category))
                        .size(10).color(t.accent),
                ].spacing(8))).padding(0).width(Fill)
                    .on_press(Action::ComposerPackage(pkg.id.clone()))
                    .style(move |_, s| widgets::button_style(theme, selected, s)));
            }
            cards = cards.push(line.width(Fill));
        }
        column![
            surface(theme, row![
                text(format!("{} packages · {} selected", d.packages.len(), self.composer_packages.len()))
                    .font(fonts::STRONG).size(12).width(Fill),
                text("Refresh  ·  + Add repo").size(11).color(t.text_secondary),
            ].align_y(Alignment::Center), 12),
            text("Pakketselectie · klik een kaart om de reviewselectie te wijzigen")
                .size(11).color(t.text_secondary),
            cards,
        ].spacing(11).into()
    }

    fn composer_presets_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let d = data();
        let mut rows = Column::new().spacing(8);
        for chunk in d.presets.iter().collect::<Vec<_>>().chunks(3) {
            let mut line = Row::new().spacing(8);
            for preset in chunk {
                let selected = self.composer_preset.as_deref() == Some(&preset.id);
                line = line.push(button(selectable_card(theme, selected, column![
                    text(&preset.name).font(fonts::HEADING).size(15),
                    text(&preset.description).size(10).color(t.text_secondary),
                    text(format!("{} packages", preset.packages.len())).size(10).color(t.accent),
                ].spacing(8))).padding(0).width(Fill)
                    .on_press(Action::ComposerPreset(preset.id.clone()))
                    .style(move |_, s| widgets::button_style(theme, selected, s)));
            }
            rows = rows.push(line.width(Fill));
        }
        column![
            surface(theme, row![
                text("Skill Package Presets").font(fonts::STRONG).size(14).width(Fill),
                text(format!("{} presets", d.presets.len())).size(11).color(t.accent),
            ], 12),
            text("De gepinde code bevat 24 presets; de oudere broncapture toont 20.")
                .size(10).color(t.text_secondary),
            rows,
        ].spacing(11).into()
    }

    fn composer_install_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        column![
            surface(theme, column![
                text("Install").font(fonts::HEADING).size(19),
                text("Geselecteerde packages, workspacepad en vereisten worden in de bronapp hier gecontroleerd.")
                    .size(11).color(t.text_secondary),
                text(format!("{} packages in deze native review geselecteerd", self.composer_packages.len()))
                    .font(fonts::STRONG).size(12).color(t.accent),
            ].spacing(10), 20),
            surface(theme, column![
                text("Voltooide installatie · broncapture hieronder").font(fonts::STRONG).size(12),
                text("Deze Rust-review voert geen package-installatie uit.")
                    .size(11).color(t.text_secondary),
            ].spacing(8), 16),
        ].spacing(11).into()
    }
}
