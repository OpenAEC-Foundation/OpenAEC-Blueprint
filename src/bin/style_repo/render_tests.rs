//! Reproducible software renders of the actual native Style Repo shell.
use super::*;
use iced::advanced::layout::{self, Layout};
use iced::advanced::renderer;
use iced::advanced::widget::Tree;
use iced::{mouse, Color, Rectangle, Size, Vector};
use openaec_ui::{Message, Preferences, Region, ShellState, Slots};
use std::sync::Once;

fn load_fonts() {
    static LOADED: Once = Once::new();
    LOADED.call_once(|| {
        fonts::install_fallback();
        let mut system = iced_tiny_skia::graphics::text::font_system()
            .write()
            .expect("font system");
        for bytes in fonts::FILES {
            system.load_font(std::borrow::Cow::Borrowed(bytes));
        }
    });
}

#[test]
#[ignore = "regenerate native PDF split-dialog review on demand"]
fn export_pdf_split_native_screen_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::PdfSplitOpen(true));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    render_sized(&app, Theme::Light, false, Some("pdf bewerken & samenvoegen"), Size::new(1280.0, 800.0))
        .save_png(&design.join("style-repo-pdf-split-light.png"))
        .expect("save native PDF split dialog");
    let _ = app.update(Action::PdfSplitOpen(false));
    let _ = app.update(Action::PdfSplitBookmarks(true));
    let _ = app.update(Action::PdfSplitModified(true));
    let _ = app.update(Action::PdfSplitOpen(true));
    render_sized(&app, Theme::Forge, false, Some("pdf bewerken & samenvoegen"), Size::new(1280.0, 800.0))
        .save_png(&design.join("style-repo-pdf-split-forge.png"))
        .expect("save native PDF split dialog with bookmarks");
}

#[test]
#[ignore = "regenerate native Reports screen review on demand"]
fn export_reports_native_screen_review() {
    let mut app = StyleRepo::default();
    let reports = studios().iter().position(|studio| studio.id == "reports").unwrap();
    let _ = app.update(Action::SelectStudio(reports));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (route, theme, hide_sidebar, name) in [
        (4, Theme::Light, false, "metadata-light"),
        (2, Theme::Light, false, "projects-light"),
        (3, Theme::Forge, false, "admin-forge"),
        (12, Theme::Light, true, "split-light"),
        (13, Theme::Forge, true, "preview-forge"),
    ] {
        let _ = app.update(Action::SelectReportsRoute(route));
        app.reports_sidebar_visible = !hide_sidebar;
        render_sized(&app, theme, false, None, Size::new(1280.0, 800.0))
            .save_png(&design.join(format!("style-repo-reports-{name}.png")))
            .expect("save native Reports screen");
    }
}

#[test]
#[ignore = "regenerate native BIM Validator screen review on demand"]
fn export_validator_native_screen_review() {
    let mut app = StyleRepo::default();
    let validator = studios().iter().position(|studio| studio.id == "validator").unwrap();
    let _ = app.update(Action::SelectStudio(validator));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (route, theme, name) in [
        (0, Theme::Light, "empty-light"),
        (1, Theme::Forge, "model-forge"),
        (4, Theme::Light, "results-light"),
        (6, Theme::Forge, "clashes-forge"),
        (7, Theme::Light, "bcf-light"),
        (8, Theme::Light, "legacy-input-light"),
        (11, Theme::Forge, "legacy-results-forge"),
    ] {
        let _ = app.update(Action::SelectValidatorRoute(route));
        render_sized(&app, theme, false, None, Size::new(1280.0, 800.0))
            .save_png(&design.join(format!("style-repo-validator-{name}.png")))
            .expect("save native BIM Validator screen");
    }
}

#[test]
#[ignore = "regenerate native Workspace Composer screen review on demand"]
fn export_composer_native_screen_review() {
    let mut app = StyleRepo::default();
    let studio = studios().iter().position(|s| s.id == "composer").unwrap();
    let _ = app.update(Action::SelectStudio(studio));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (path, advanced, theme, name) in [
        ("/workspace", false, Theme::Forge, "workspace-forge"),
        ("/presets", false, Theme::Forge, "presets-forge"),
        ("/install", false, Theme::Light, "install-light"),
        ("/dashboard", true, Theme::Forge, "dashboard-evidence-gap"),
    ] {
        let _ = app.update(Action::ComposerAdvanced(advanced));
        let index = composer_native::data().routes.iter().position(|r| r.path == path).unwrap();
        let _ = app.update(Action::ComposerRoute(index));
        render_sized(&app, theme, false, None, Size::new(1280.0, 800.0))
            .save_png(&design.join(format!("style-repo-composer-{name}.png")))
            .expect("save native Composer screen");
    }
}

#[test]
#[ignore = "regenerate native Open Calc Studio budget grid review on demand"]
fn export_calc_native_screen_review() {
    let mut app = StyleRepo::default();
    let calc = studios().iter().position(|studio| studio.id == "calc").unwrap();
    let _ = app.update(Action::SelectStudio(calc));
    let _ = app.update(Action::SelectScreen(1));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized(&app, theme, false, Some("begroting"), Size::new(1800.0, 1000.0))
            .save_png(&design.join(format!("style-repo-calc-budget-{name}.png")))
            .expect("save native Calc budget review");
    }
}

#[test]
fn validator_three_pane_shell_keeps_quarter_half_quarter_geometry() {
    let mut app = StyleRepo::default();
    let validator = studios().iter().position(|studio| studio.id == "validator").unwrap();
    let _ = app.update(Action::SelectStudio(validator));
    let picture = render_sized(&app, Theme::Light, false, None, Size::new(1280.0, 800.0));
    let pixel = |x: usize| {
        let at = ((500 * picture.width() as usize + x) * 4) as usize;
        &picture.data()[at..at + 3]
    };
    assert_ne!(pixel(200), &[30, 35, 43]);
    assert_eq!(pixel(600), &[30, 35, 43]);
    assert_ne!(pixel(1100), &[30, 35, 43]);
    assert_eq!(pixel(321), &[33, 37, 45]);
    assert_eq!(pixel(958), &[33, 37, 45]);
    let _ = app.update(Action::ToggleValidatorLeft);
    let _ = app.update(Action::ToggleValidatorRight);
    let full = render_sized(&app, Theme::Light, false, None, Size::new(1280.0, 800.0));
    for x in [200usize, 600, 1100] {
        let at = ((500 * full.width() as usize + x) * 4) as usize;
        assert_eq!(&full.data()[at..at + 3], &[30, 35, 43]);
    }
}

#[test]
#[ignore = "regenerate native PDF find-bar review on demand"]
fn export_pdf_native_find_bar_review() {
    use openaec_ui::find_bar::{self, FindBarActions, FindBarState, ResultGroup};
    load_fonts();
    let state = FindBarState {
        query: "constructie".into(),
        current: 1,
        total: 7,
        search_text: true,
        search_annotations: true,
        highlight_all: true,
        results_open: true,
        groups: vec![
            ResultGroup {
                page: 2,
                count: 4,
                kinds: "Tekst".into(),
                current: true,
            },
            ResultGroup {
                page: 5,
                count: 3,
                kinds: "Annotaties".into(),
                current: false,
            },
        ],
        ..FindBarState::default()
    };
    let actions = || FindBarActions {
        query_changed: |_| (),
        previous: (),
        next: (),
        toggle_match_case: (),
        toggle_whole_word: (),
        toggle_highlight_all: (),
        toggle_text: (),
        toggle_annotations: (),
        toggle_results: (),
        select_page: |_| (),
        close: (),
    };
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        for (width, size_name) in [(620.0, "wide"), (300.0, "narrow")] {
            let bar = find_bar::view(&state, actions(), theme, Language::Dutch, width)
                .map(|_| Message::Command(Action::SelectScreen(0)));
            let element = iced::widget::container(
                iced::widget::column![
                    iced::widget::row![iced::widget::Space::new().width(iced::Fill).height(1), bar],
                    iced::widget::Space::new().width(iced::Fill).height(24),
                    iced::widget::text("Voorbeeld document").size(20),
                ]
                .spacing(8),
            )
            .width(width)
            .height(330)
            .padding([4, 12])
            .style(move |_| {
                iced::widget::container::Style::default().background(theme.tokens().content_bg)
            })
            .into();
            render_element(element, theme, Size::new(width, 330.0))
                .save_png(&design.join(format!("pdf-find-bar-native-{name}-{size_name}.png")))
                .expect("save native find bar");
        }
    }
}

#[test]
#[ignore = "regenerate shared Rust icon catalogue on demand"]
fn export_canonical_icon_reviews() {
    let mut app = StyleRepo::default();
    app.show(Page::Icons);
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        save_render(&app, theme, &design.join(format!("style-repo-icons-{name}.png")));
    }
}

#[test]
#[ignore = "regenerate source-icon Geotechniek ribbon previews on demand"]
fn export_geotech_source_ribbon_reviews() {
    let mut app = StyleRepo::default();
    let geotech = studios().iter().position(|studio| studio.id == "geotech").unwrap();
    let _ = app.update(Action::SelectStudio(geotech));
    let _ = app.update(Action::SelectScreen(1));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (tab, theme, suffix) in [
        ("home", Theme::Light, "home-light"),
        ("situatietekening", Theme::Light, "drawing-light"),
        ("situatietekening", Theme::Forge, "drawing-forge"),
    ] {
        render_with_options(&app, theme, false, Some(tab))
            .save_png(&design.join(format!("style-repo-geotech-source-{suffix}.png")))
            .expect("save Geotechniek source-icon ribbon");
    }
    for (theme, suffix) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized(
            &app,
            theme,
            false,
            Some("situatietekening"),
            Size::new(2200.0, 800.0),
        )
        .save_png(&design.join(format!("style-repo-geotech-drawing-wide-{suffix}.png")))
        .expect("save complete Geotechniek drawing ribbon");
    }
}

fn render(app: &StyleRepo, theme: Theme) -> tiny_skia::Pixmap {
    render_with_options(app, theme, false, None)
}

fn render_with_settings(app: &StyleRepo, theme: Theme, show_settings: bool) -> tiny_skia::Pixmap {
    render_with_options(app, theme, show_settings, None)
}

fn render_with_options(
    app: &StyleRepo,
    theme: Theme,
    show_settings: bool,
    active_tab: Option<&str>,
) -> tiny_skia::Pixmap {
    render_sized(app, theme, show_settings, active_tab, Size::new(1280.0, 800.0))
}

fn render_sized(
    app: &StyleRepo,
    theme: Theme,
    show_settings: bool,
    active_tab: Option<&str>,
    size: Size,
) -> tiny_skia::Pixmap {
    render_sized_with_reset(app, theme, show_settings, active_tab, size, false, false)
}

fn render_sized_with_reset(
    app: &StyleRepo,
    theme: Theme,
    show_settings: bool,
    active_tab: Option<&str>,
    size: Size,
    reset_confirm: bool,
    backstage: bool,
) -> tiny_skia::Pixmap {
    load_fonts();
    let mut preferences = Preferences::default();
    preferences.theme = theme;
    let mut state = ShellState::new(preferences);
    state.set_window_width(size.width);
    state.settings = show_settings;
    state.settings_reset_confirm = reset_confirm;
    state.backstage = backstage;
    if show_settings {
        state.settings_page = openaec_ui::SettingsPage::Appearance;
        state.settings_theme_open = !reset_confirm;
    }
    if let Some(tab) = active_tab {
        state.active_tab = tab.into();
    }
    let language = Language::Dutch;
    let element = openaec_ui::shell(
        &state,
        Slots {
            title: app.title(),
            mode: app.chrome_mode(),
            tabs: app.ribbon(language),
            documents: app.documents(),
            active_document: app.active_document(),
            file_commands: app.file_commands(language),
            file_active_label: app.file_active_label(language),
            quick_commands: app.quick_commands(language),
            status: app.status(language),
            overlay: app.overlay(theme, language).map(|element| element.map(Message::Command)),
            content: Box::new(|region| match region {
                Region::Workspace => app.workspace(theme, language).map(Message::Command),
                Region::Explorer if app.chrome_mode() == ChromeMode::SidebarCompact => app.explorer(theme, language).map(Message::Command),
                Region::Explorer if matches!(app.chrome_mode(), ChromeMode::ThreePaneRibbon { .. } | ChromeMode::ThreePaneFixed { .. }) => app.explorer(theme, language).map(Message::Command),
                Region::Explorer => widgets::panel(
                    if app.chrome_mode() == ChromeMode::Workflow { language.text("Werkstroom", "Workflow") } else if app.chrome_mode() == ChromeMode::Sidebar { language.text("Navigatie", "Navigation") } else if app.chrome_mode() == ChromeMode::CanvasRibbon { language.text("Eigenschappen", "Properties") } else { language.text("Verkenner", "Explorer") },
                    app.explorer(theme, language).map(Message::Command),
                    theme,
                ),
                Region::Properties if matches!(app.chrome_mode(), ChromeMode::ThreePaneRibbon { .. } | ChromeMode::ThreePaneFixed { .. }) => app.properties(theme, language).map(Message::Command),
                Region::Properties => widgets::panel(
                    language.text("Eigenschappen", "Properties"),
                    app.properties(theme, language).map(Message::Command),
                    theme,
                ),
            }),
        },
    );
    render_element(element, theme, size)
}

fn render_element(
    mut element: iced::Element<'_, Message<Action>>,
    theme: Theme,
    size: Size,
) -> tiny_skia::Pixmap {
    let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let node =
        element
            .as_widget_mut()
            .layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, size));
    let iced_theme = theme.iced();
    element.as_widget().draw(
        &tree,
        &mut renderer,
        &iced_theme,
        &renderer::Style {
            text_color: iced_theme.palette().text,
        },
        Layout::new(&node),
        mouse::Cursor::Unavailable,
        &Rectangle::with_size(size),
    );
    if let Some(mut overlay) =
        element
            .as_widget_mut()
            .overlay(&mut tree, Layout::new(&node), &renderer, &Rectangle::with_size(size), Vector::ZERO)
    {
        let popup_node = overlay.as_overlay_mut().layout(&renderer, size);
        overlay.as_overlay().draw(
            &mut renderer,
            &iced_theme,
            &renderer::Style {
                text_color: iced_theme.palette().text,
            },
            Layout::new(&popup_node),
            mouse::Cursor::Unavailable,
        );
    }
    let mut software = renderer;
    let (width, height) = (size.width as u32, size.height as u32);
    let mut bytes = vec![0u8; (width * height * 4) as usize];
    let mut pixels =
        tiny_skia::PixmapMut::from_bytes(&mut bytes, width, height).expect("valid pixmap");
    let mut mask = tiny_skia::Mask::new(width, height).expect("valid mask");
    software.draw(
        &mut pixels,
        &mut mask,
        &iced_tiny_skia::graphics::Viewport::with_physical_size(Size::new(width, height), 1.0),
        &[Rectangle::with_size(size)],
        Color::from_rgb(1.0, 0.0, 1.0),
        );
    for pixel in bytes.chunks_exact_mut(4) {
        pixel.swap(0, 2);
    }
    tiny_skia::Pixmap::from_vec(
        bytes,
        tiny_skia::IntSize::from_wh(width, height).expect("valid size"),
    )
    .expect("valid rendered pixels")
}

fn save_render(app: &StyleRepo, theme: Theme, path: &std::path::Path) {
    render(app, theme)
        .save_png(path)
        .expect("save native review image");
}

fn source_band<'a>(
    label: &'static str,
    height: u16,
    background: Color,
    foreground: Color,
) -> iced::Element<'a, Message<Action>> {
    iced::widget::container(iced::widget::text(label).size(12))
        .width(iced::Fill)
        .height(u32::from(height))
        .padding([0, 12])
        .align_y(iced::Alignment::Center)
        .style(move |_| {
            iced::widget::container::Style::default()
                .background(background)
                .color(foreground)
        })
        .into()
}

fn source_pane<'a>(
    label: &'static str,
    background: Color,
    foreground: Color,
) -> iced::Element<'a, Message<Action>> {
    iced::widget::container(iced::widget::text(label).size(12))
        .width(iced::Fill)
        .height(iced::Fill)
        .padding(12)
        .style(move |_| {
            iced::widget::container::Style::default()
                .background(background)
                .color(foreground)
        })
        .into()
}

#[test]
#[ignore = "regenerate native Open Frame shell geometry review on demand"]
fn export_frame_shell_geometry_review() {
    load_fonts();
    let profile = openaec_ui::frame::WorkspaceFrameProfile::OPEN_FRAME;
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (width, height, tabs_height, suffix) in
        [(1200.0, 800.0, 73, "wide"), (720.0, 600.0, 145, "narrow")]
    {
        let ink = Color::from_rgb8(236, 236, 239);
        let body = Color::from_rgb8(40, 40, 47);
        let panels = openaec_ui::frame::workspace_panes(
            profile,
            Some(source_pane(
                "Explorer · 220 px",
                Color::from_rgb8(48, 48, 56),
                ink,
            )),
            source_pane("Werkgebied", body, ink),
            Some(source_pane(
                "Properties · 290 px",
                Color::from_rgb8(48, 48, 56),
                ink,
            )),
        );
        let shell = openaec_ui::frame::workspace_frame(
            openaec_ui::frame::WorkspaceFrameSlots {
                titlebar: source_band("Title · 36 px", 36, Color::from_rgb8(54, 54, 62), ink),
                ribbon: source_band(
                    "Ribbon · inhoudshoogte 132 px",
                    132,
                    Color::from_rgb8(68, 68, 76),
                    ink,
                ),
                workspace_tabs: source_band(
                    "Workspace tabs · omvouwende hoogte",
                    tabs_height,
                    Color::from_rgb8(58, 58, 66),
                    ink,
                ),
                content: panels,
                status: source_band("Status · 28 px", 28, Color::from_rgb8(54, 54, 62), ink),
            },
            profile,
        );
        render_element(shell, Theme::Forge, Size::new(width, height))
            .save_png(&design.join(format!("frame-native-shell-{suffix}.png")))
            .expect("save native frame geometry");
    }
}

#[test]
#[ignore = "regenerate Pointcloud annotation icon comparison on demand"]
fn export_pointcloud_annotation_icon_review() {
    use iced::widget::{column, container, row, svg, text};
    use openaec_ui::icons::DomainIcon;

    fn swatch<'a>(glyph: iced::Element<'a, Message<Action>>, background: Color) -> iced::Element<'a, Message<Action>> {
        container(glyph)
            .width(120)
            .height(72)
            .center_x(iced::Fill)
            .center_y(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into()
    }

    load_fonts();
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(54, 54, 62)),
    ] {
        let foreground = theme.tokens().text;
        let mut rows = column![] .spacing(12).padding(18);
        for (label, icon, source) in [
            ("Tekst", DomainIcon::DrawingText, include_bytes!("../../../harmonization/ui-icons/open-pointcloud-studio/native/assets/opencad-icons/annotation_text.svg").as_slice()),
            ("Leidlijn", DomainIcon::DrawingLeader, include_bytes!("../../../harmonization/ui-icons/open-pointcloud-studio/native/assets/opencad-icons/annotation_leader.svg").as_slice()),
        ] {
            let source_icon: iced::Element<'_, Message<Action>> = svg(svg::Handle::from_memory(source))
                .width(24)
                .height(24)
                .style(move |_, _| svg::Style { color: (theme == Theme::Forge).then_some(foreground) })
                .into();
            rows = rows.push(
                column![
                    text(label).size(15).color(foreground),
                    row![
                        swatch(source_icon, background),
                        swatch(icon.view(16, foreground).into(), background),
                        swatch(icon.view(24, foreground).into(), background),
                        swatch(icon.view(32, foreground).into(), background),
                    ].spacing(12),
                ].spacing(7),
            );
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(560.0, 230.0))
            .save_png(&design.join(format!("pointcloud-annotation-icons-{suffix}.png")))
            .expect("save annotation comparison");
    }
}

#[test]
#[ignore = "regenerate native PDF chrome icon contact sheets on demand"]
fn export_pdf_chrome_icon_contact_sheets() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/pdf-chrome-ui-icons.json")).expect("PDF chrome manifest"),
    ).expect("valid PDF chrome manifest");
    let records = manifest["records"].as_array().expect("PDF chrome records");
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut cells: Vec<iced::Element<'_, Message<Action>>> = Vec::new();
        for item in records {
            let label = item["label"].as_str().expect("PDF icon label");
            for variant in item["variants"].as_array().expect("PDF icon variants") {
                let path = variant["svg"].as_str().expect("PDF icon path");
                let bytes = std::fs::read(root.join("harmonization").join(path)).expect("PDF icon SVG");
                let glyph = svg(svg::Handle::from_memory(bytes))
                    .width(24)
                    .height(24)
                    .style(move |_, _| svg::Style { color: Some(foreground) });
                cells.push(
                    container(column![text(label).size(11).color(foreground), glyph].spacing(9))
                        .width(150)
                        .height(88)
                        .padding(8)
                        .style(move |_| container::Style::default().background(background))
                        .into(),
                );
            }
        }
        assert_eq!(cells.len(), 42);
        let mut rows = column![].spacing(5).padding(10);
        let mut cells = cells.into_iter();
        for _ in 0..6 {
            let mut line = row![].spacing(5);
            for _ in 0..7 {
                line = line.push(cells.next().expect("complete PDF icon row"));
            }
            rows = rows.push(line);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(1100.0, 580.0))
            .save_png(&root.join(format!("design/pdf-chrome-icons-{suffix}.png")))
            .expect("save PDF chrome icon sheet");
    }
}

#[test]
#[ignore = "regenerate native PDF Drawing icon contact sheets on demand"]
fn export_pdf_drawing_icon_contact_sheets() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/pdf-drawing-ui-icons.json")).expect("PDF Drawing manifest"),
    ).expect("valid PDF Drawing manifest");
    let records = manifest["records"].as_array().expect("PDF Drawing records");
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut cells: Vec<iced::Element<'_, Message<Action>>> = Vec::new();
        for item in records.iter().filter(|item| item["kind"] == "ui-icon") {
            let label = item["uses"][0]["label"].as_str().expect("PDF Drawing label");
            let path = item["svg"].as_str().expect("PDF Drawing icon path");
            let bytes = std::fs::read(root.join("harmonization").join(path)).expect("PDF Drawing SVG");
            let glyph = svg(svg::Handle::from_memory(bytes))
                .width(24)
                .height(24)
                .style(move |_, _| svg::Style { color: Some(foreground) });
            cells.push(
                container(column![text(label).size(11).color(foreground), glyph].spacing(9))
                    .width(170)
                    .height(84)
                    .padding(8)
                    .style(move |_| container::Style::default().background(background))
                    .into(),
            );
        }
        assert_eq!(cells.len(), 37);
        let mut cells = cells.into_iter();
        let mut rows = column![].spacing(5).padding(10);
        for _ in 0..7 {
            let mut line = row![].spacing(5);
            for _ in 0..6 {
                if let Some(cell) = cells.next() {
                    line = line.push(cell);
                }
            }
            rows = rows.push(line);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(1100.0, 660.0))
            .save_png(&root.join(format!("design/pdf-drawing-icons-{suffix}.png")))
            .expect("save PDF Drawing icon sheet");
    }
}

#[test]
#[ignore = "regenerate native PDF SVG-text fallback comparison on demand"]
fn export_pdf_drawing_text_fallback_review() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/pdf-drawing-ui-icons.json")).expect("PDF Drawing manifest"),
    ).expect("valid PDF Drawing manifest");
    let records = manifest["records"].as_array().expect("PDF Drawing records");
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut rows = column![].spacing(12).padding(12);
        for item in records.iter().filter(|item| item.get("vector_fallback").is_some()) {
            let name = item["uses"][0]["label"].as_str().expect("PDF fallback label");
            let source = item["svg"].as_str().expect("PDF source SVG");
            let candidate = item["vector_fallback"].as_str().expect("PDF fallback SVG");
            let candidate_small = item["vector_fallback_small"].as_str().expect("PDF small fallback SVG");
            let mut icons = row![text(name).size(12).color(foreground).width(170)].spacing(14);
            for (path, size) in [(source, 24), (candidate_small, 16), (candidate, 24), (candidate, 32)] {
                let bytes = std::fs::read(root.join("harmonization").join(path)).expect("PDF SVG bytes");
                let glyph = svg(svg::Handle::from_memory(bytes))
                    .width(size)
                    .height(size)
                    .style(move |_, _| svg::Style { color: Some(foreground) });
                icons = icons.push(
                    container(glyph).width(100).height(64)
                        .center_x(iced::Fill).center_y(iced::Fill)
                        .style(move |_| container::Style::default().background(background)),
                );
            }
            rows = rows.push(icons);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill).height(iced::Fill)
            .style(move |_| container::Style::default().background(background)).into();
        render_element(page, theme, Size::new(680.0, 250.0))
            .save_png(&root.join(format!("design/pdf-drawing-text-fallback-{suffix}.png")))
            .expect("save PDF SVG-text fallback comparison");
    }
}

#[test]
#[ignore = "regenerate native PDF imported context-menu icon sheets on demand"]
fn export_pdf_context_imported_icon_contact_sheets() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/pdf-context-imported-ui-icons.json"))
            .expect("PDF context import manifest"),
    )
    .expect("valid PDF context import manifest");
    let records = manifest["records"].as_array().expect("PDF context records");
    assert_eq!(records.len(), 52);
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut cells: Vec<iced::Element<'_, Message<Action>>> = Vec::new();
        for item in records {
            let name = item["name"].as_str().expect("PDF icon name");
            let path = item["svg"].as_str().expect("PDF icon path");
            let bytes = std::fs::read(root.join("harmonization").join(path))
                .expect("PDF context imported SVG");
            let glyph = svg(svg::Handle::from_memory(bytes))
                .width(24)
                .height(24)
                .style(move |_, _| svg::Style {
                    color: if name.ends_with("Svg") { None } else { Some(foreground) },
                });
            cells.push(
                container(column![text(name).size(10).color(foreground), glyph].spacing(7))
                    .width(170)
                    .height(72)
                    .padding(7)
                    .style(move |_| container::Style::default().background(background))
                    .into(),
            );
        }
        let mut cells = cells.into_iter();
        let mut rows = column![].spacing(5).padding(10);
        for _ in 0..8 {
            let mut line = row![].spacing(5);
            for _ in 0..7 {
                if let Some(cell) = cells.next() {
                    line = line.push(cell);
                }
            }
            rows = rows.push(line);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(1250.0, 650.0))
            .save_png(&root.join(format!("design/pdf-context-imported-icons-{suffix}.png")))
            .expect("save PDF context imported icon sheet");
    }
}

#[test]
#[ignore = "regenerate native PDF built-in ribbon icon sheets on demand"]
fn export_pdf_ribbon_imported_icon_contact_sheets() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/pdf-ribbon-imported-ui-icons.json"))
            .expect("PDF ribbon import manifest"),
    )
    .expect("valid PDF ribbon import manifest");
    let records = manifest["records"].as_array().expect("PDF ribbon records");
    assert_eq!(records.len(), 122);
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut cells: Vec<iced::Element<'_, Message<Action>>> = Vec::new();
        for item in records.iter().filter(|item| item["classification"] == "built-in-ui-icon") {
            let name = item["name"].as_str().expect("PDF ribbon name");
            let path = item["svg"].as_str().expect("PDF ribbon path");
            let bytes = std::fs::read(root.join("harmonization").join(path))
                .expect("PDF ribbon imported SVG");
            let glyph = svg(svg::Handle::from_memory(bytes))
                .width(24)
                .height(24)
                .style(move |_, _| svg::Style {
                    color: Some(foreground),
                });
            cells.push(
                container(column![text(name).size(10).color(foreground), glyph].spacing(7))
                    .width(170)
                    .height(70)
                    .padding(7)
                    .style(move |_| container::Style::default().background(background))
                    .into(),
            );
        }
        assert_eq!(cells.len(), 109);
        let mut cells = cells.into_iter();
        let mut rows = column![].spacing(5).padding(10);
        for _ in 0..11 {
            let mut line = row![].spacing(5);
            for _ in 0..10 {
                if let Some(cell) = cells.next() {
                    line = line.push(cell);
                }
            }
            rows = rows.push(line);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(1780.0, 840.0))
            .save_png(&root.join(format!("design/pdf-ribbon-imported-icons-{suffix}.png")))
            .expect("save PDF ribbon imported icon sheet");
    }
}

fn pdf_semantic_icon_bytes(variant: &str, size: u16) -> &'static [u8] {
    use openaec_ui::icons::{DomainIcon, Icon};
    match variant {
        "Icon::Fit" => Icon::Fit.bytes(),
        "Icon::Search" => Icon::Search.bytes(),
        "DomainIcon::DrawingText" => DomainIcon::DrawingText.bytes(size),
        "DomainIcon::PdfFitWidth" => DomainIcon::PdfFitWidth.bytes(size),
        "DomainIcon::PdfActualSize" => DomainIcon::PdfActualSize.bytes(size),
        "DomainIcon::PdfEditText" => DomainIcon::PdfEditText.bytes(size),
        "DomainIcon::PdfClearPage" => DomainIcon::PdfClearPage.bytes(size),
        "DomainIcon::PdfDeletePage" => DomainIcon::PdfDeletePage.bytes(size),
        "DomainIcon::PdfSinglePage" => DomainIcon::PdfSinglePage.bytes(size),
        "DomainIcon::PdfContinuousPages" => DomainIcon::PdfContinuousPages.bytes(size),
        "DomainIcon::PdfFileAssociation" => DomainIcon::PdfFileAssociation.bytes(size),
        "DomainIcon::PdfBookView" => DomainIcon::PdfBookView.bytes(size),
        "DomainIcon::PdfShortcuts" => DomainIcon::PdfShortcuts.bytes(size),
        "DomainIcon::PdfNavigation" => DomainIcon::PdfNavigation.bytes(size),
        "DomainIcon::PdfManageWatermarks" => DomainIcon::PdfManageWatermarks.bytes(size),
        _ => panic!("unmapped PDF semantic: {variant}"),
    }
}

#[test]
fn shared_pdf_ribbon_icons_match_reviewed_artwork() {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/proposals/pdf-ribbon-semantic/review.json"))
            .expect("PDF ribbon semantic review"),
    )
    .expect("valid PDF ribbon semantic review");
    let records = manifest["rows"].as_array().expect("PDF semantic rows");
    assert_eq!(records.len(), 15);
    assert_eq!(records.iter().filter(|item| item["proposal_kind"] == "shared-domain-icon").count(), 12);
    for item in records {
        let variant = item["crate_variant"].as_str().expect("typed Rust icon");
        for size in [16, 24] {
            let path = if size == 16 {
                item["proposal_small_svg"].as_str().or(item["proposal_svg"].as_str())
            } else {
                item["proposal_svg"].as_str()
            }
            .expect("review SVG path");
            assert_eq!(pdf_semantic_icon_bytes(variant, size), std::fs::read(root.join(path)).expect("reviewed SVG"),
                "{variant} at {size} px diverged from visual review");
        }
    }
}

#[test]
#[ignore = "regenerate native PDF ribbon semantic Rust icon comparisons on demand"]
fn export_pdf_ribbon_semantic_review() {
    use iced::widget::{column, container, row, svg, text};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let manifest: serde_json::Value = serde_json::from_slice(
        &std::fs::read(root.join("harmonization/proposals/pdf-ribbon-semantic/review.json"))
            .expect("PDF ribbon semantic proposal manifest"),
    )
    .expect("valid PDF ribbon proposal manifest");
    let records = manifest["rows"].as_array().expect("PDF ribbon proposal rows");
    assert_eq!(records.len(), 15);
    load_fonts();
    for (theme, suffix, background) in [
        (Theme::Light, "light", Color::from_rgb8(250, 250, 249)),
        (Theme::Forge, "forge", Color::from_rgb8(48, 48, 57)),
    ] {
        let foreground = theme.tokens().text;
        let mut rows = column![].spacing(6).padding(12);
        for item in records {
            let label = item["label"].as_str().expect("PDF semantic label");
            let variant = item["crate_variant"].as_str().expect("typed PDF semantic icon");
            let candidate = item["proposal_svg"].as_str().expect("PDF semantic proposal path");
            let candidate_small = item["proposal_small_svg"].as_str().unwrap_or(candidate);
            let mut icons = row![text(label).size(11).color(foreground).width(190)].spacing(8);
            for (path, size, shared) in [
                (item["source_svg"].as_str(), 24, false),
                (Some(candidate_small), 16, true),
                (Some(candidate), 24, true),
                (Some(candidate), 32, true),
            ] {
                let content: iced::Element<'_, Message<Action>> = if let Some(path) = path {
                    let bytes = if shared {
                        pdf_semantic_icon_bytes(variant, size).to_vec()
                    } else {
                        std::fs::read(root.join(path)).expect("PDF source SVG")
                    };
                    svg(svg::Handle::from_memory(bytes))
                        .width(u32::from(size))
                        .height(u32::from(size))
                        .style(move |_, _| svg::Style {
                            color: Some(foreground),
                        })
                        .into()
                } else {
                    text("—").size(18).color(foreground).into()
                };
                icons = icons.push(
                    container(content).width(100).height(42)
                        .center_x(iced::Fill)
                        .center_y(iced::Fill)
                        .style(move |_| container::Style::default().background(background)),
                );
            }
            rows = rows.push(icons);
        }
        let page: iced::Element<'_, Message<Action>> = container(rows)
            .width(iced::Fill)
            .height(iced::Fill)
            .style(move |_| container::Style::default().background(background))
            .into();
        render_element(page, theme, Size::new(660.0, 740.0))
            .save_png(&root.join(format!("design/pdf-ribbon-semantic-{suffix}.png")))
            .expect("save PDF ribbon semantic review");
    }
}

#[test]
fn source_interfaces_keep_their_non_ribbon_routes_and_modal() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::Show(Page::Sources));
    assert_eq!(app.chrome_mode(), ChromeMode::TopNav);
    assert_eq!(source_interfaces::OCONDAT_ROUTES.len(), 12);
    let _ = app.update(Action::SourceManufacturerCatalog(1));
    assert_eq!(app.source_manufacturer, 1);
    assert_eq!(app.source_route, 0);
    let _ = app.update(Action::SourceDetails(Some(0)));
    assert!(app.overlay(Theme::Light, Language::Dutch).is_some());
    let _ = app.update(app.escape().expect("details modal closes on Escape"));
    assert!(app.source_details.is_none());
    let _ = app.update(Action::SelectSourceApp(1));
    assert_eq!(app.source_app, 1);
    assert_eq!(app.chrome_mode(), ChromeMode::TopNav);
    let _ = app.source_interfaces_page(Theme::Forge, Language::Dutch);
}

#[test]
#[ignore = "regenerate native source-interface reviews on demand"]
fn export_source_interface_reviews() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    let _ = app.update(Action::Show(Page::Sources));
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        save_render(&app, theme, &design.join(format!("style-repo-ocondat-catalog-{name}.png")));
        let _ = app.update(Action::SelectSourceRoute(2));
        save_render(&app, theme, &design.join(format!("style-repo-ocondat-standards-{name}.png")));
        let _ = app.update(Action::SelectSourceApp(0));
        let _ = app.update(Action::SelectSourceApp(1));
        render_sized(&app, theme, false, None, Size::new(1280.0, 1100.0))
            .save_png(&design.join(format!("style-repo-buildingpy-location-{name}.png")))
            .expect("save full BuildingPy location review");
        let _ = app.update(Action::SelectSourceApp(0));
    }
}

#[test]
#[ignore = "regenerate shared settings dialog review on demand"]
fn export_shared_settings_review() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let app = StyleRepo::default();
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_with_settings(&app, theme, true)
            .save_png(&design.join(format!("style-repo-settings-{name}.png")))
            .expect("save shared settings review");
    }
    render_sized_with_reset(&app, Theme::Forge, true, None, Size::new(1280.0, 800.0), true, false)
        .save_png(&design.join("style-repo-settings-reset-forge.png"))
        .expect("save reset confirmation review");
    render_sized(&app, Theme::Light, true, None, Size::new(1280.0, 480.0))
        .save_png(&design.join("style-repo-settings-short-light.png"))
        .expect("save short-window settings review");
}

#[test]
fn expanded_theme_menu_keeps_the_trigger_height_in_form_layout() {
    load_fonts();
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    for open in [false, true] {
        let mut element = widgets::settings_theme_picker(
            vec![(Theme::Light, "Light".to_owned(), ())],
            Theme::Light, Theme::Light, open, (),
        );
        let mut tree = Tree::new(&element);
        let node = element.as_widget_mut().layout(
            &mut tree, &renderer,
            &layout::Limits::new(Size::ZERO, Size::new(500.0, 500.0)),
        );
        assert_eq!(node.size(), Size::new(200.0, 27.0));
    }
}

#[test]
#[ignore = "regenerate native Geotechniek borehole review on demand"]
fn export_geotech_borehole_review() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    let geotech = studios().iter().position(|studio| studio.id == "geotech").unwrap();
    let _ = app.update(Action::SelectStudio(geotech));
    let _ = app.update(Action::SelectScreen(1));
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_with_options(&app, theme, false, Some("home"))
            .save_png(&design.join(format!("style-repo-geotech-borehole-{name}.png")))
            .expect("save native borehole review");
    }
}

#[test]
#[ignore = "regenerate native Speech review on demand"]
fn export_speech_sidebar_review() {
    let mut app = StyleRepo::default();
    let speech = studios().iter().position(|studio| studio.id == "speech").unwrap();
    let _ = app.update(Action::SelectStudio(speech));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (index, name) in [
        (0, "speech"), (1, "transcribe"), (2, "meeting"),
        (3, "mic-test"), (4, "models"), (5, "dictionary"),
        (6, "tts"), (7, "settings"), (8, "about"),
    ] {
        let _ = app.update(Action::SelectScreen(index));
        render(&app, Theme::Light)
            .save_png(&design.join(format!("style-repo-speech-{name}-light.png")))
            .expect("save native Speech Light review");
        render(&app, Theme::Forge)
            .save_png(&design.join(format!("style-repo-speech-{name}-forge.png")))
            .expect("save native Speech Forge review");
    }
    let _ = app.update(Action::SelectScreen(0));
    render(&app, Theme::Forge)
        .save_png(&design.join("style-repo-speech-sidebar-forge.png"))
        .expect("save Speech sidebar review");
}

#[test]
#[ignore = "regenerate native Frame review on demand"]
fn export_frame_ribbon_review() {
    let mut app = StyleRepo::default();
    let frame = studios().iter().position(|studio| studio.id == "frame").unwrap();
    let _ = app.update(Action::SelectStudio(frame));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("home"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-frame-ribbon-light.png"))
        .expect("save Frame ribbon review");
}

#[test]
#[ignore = "regenerate native Frame selection reviews on demand"]
fn export_frame_select_reviews() {
    let mut app = StyleRepo::default();
    let frame = studios().iter().position(|studio| studio.id == "frame").unwrap();
    let _ = app.update(Action::SelectStudio(frame));
    let _ = app.update(Action::SelectScreen(1));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (tab, file) in [("home", "style-repo-frame-ribbon-light.png"),
        ("ifc / export", "style-repo-frame-ifc-light.png"),
        ("beeld", "style-repo-frame-view-light.png")] {
        render_with_options(&app, Theme::Light, false, Some(tab))
            .save_png(&design.join(file)).expect("save Frame select review");
    }
}

#[test]
#[ignore = "regenerate native Field review on demand"]
fn export_field_topnav_review() {
    let mut app = StyleRepo::default();
    let field = studios().iter().position(|studio| studio.id == "field").unwrap();
    let _ = app.update(Action::SelectStudio(field));
    render(&app, Theme::Light)
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-topnav-light.png"))
        .expect("save Field top navigation review");
    render(&app, Theme::Forge)
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-topnav-forge.png"))
        .expect("save Field Forge project form review");
    let _ = app.update(Action::SelectScreen(6));
    render_with_options(&app, Theme::Light, false, Some("dashboard"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-dashboard-light.png"))
        .expect("save Field dashboard review");
    render_with_options(&app, Theme::Forge, false, Some("dashboard"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-dashboard-forge.png"))
        .expect("save Field Forge dashboard review");
    let _ = app.update(Action::SelectScreen(8));
    render_with_options(&app, Theme::Light, false, Some("koppelingen"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-connectors-light.png"))
        .expect("save Field connectors review");
    render_with_options(&app, Theme::Forge, false, Some("koppelingen"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-connectors-forge.png"))
        .expect("save Field Forge connectors review");
    let _ = app.update(Action::SelectScreen(7));
    render_with_options(&app, Theme::Light, false, Some("export"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-export-light.png"))
        .expect("save Field export review");
    render_with_options(&app, Theme::Forge, false, Some("export"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-export-forge.png"))
        .expect("save Field Forge export review");
    let _ = app.update(Action::SelectScreen(4));
    render_with_options(&app, Theme::Light, false, Some("inspectie"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-inspection-light.png"))
        .expect("save Field inspection overview");
    let _ = app.update(Action::FieldFlowSetup("inspectie"));
    render_with_options(&app, Theme::Forge, false, Some("inspectie"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-inspection-setup-forge.png"))
        .expect("save Field inspection setup");
    let _ = app.update(Action::SelectScreen(5));
    render_with_options(&app, Theme::Light, false, Some("oplevering"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-handover-light.png"))
        .expect("save Field handover overview");
    let _ = app.update(Action::FieldFlowSetup("oplevering"));
    render_with_options(&app, Theme::Forge, false, Some("oplevering"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-handover-setup-forge.png"))
        .expect("save Field handover setup");
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (index, tab, light, forge) in [
        (1, "plattegronden", "style-repo-field-floorplans-light.png", "style-repo-field-floorplans-forge.png"),
        (2, "3d bim", "style-repo-field-ifc-light.png", "style-repo-field-ifc-forge.png"),
        (3, "opname", "style-repo-field-capture-light.png", "style-repo-field-capture-forge.png"),
        (9, "handleiding", "style-repo-field-manual-light.png", "style-repo-field-manual-forge.png"),
    ] {
        let _ = app.update(Action::SelectScreen(index));
        render_with_options(&app, Theme::Light, false, Some(tab))
            .save_png(&design.join(light)).expect("save Field code-derived Light route");
        render_with_options(&app, Theme::Forge, false, Some(tab))
            .save_png(&design.join(forge)).expect("save Field code-derived Forge route");
    }
}

#[test]
#[ignore = "regenerate native AEC extension review on demand"]
fn export_aec_extension_review() {
    let mut app = StyleRepo::default();
    let aec = studios().iter().position(|studio| studio.id == "2d").unwrap();
    let _ = app.update(Action::SelectStudio(aec));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("aec"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-2d-extension-forge.png"))
        .expect("save AEC extension review");
}

#[test]
#[ignore = "regenerate native CAD review on demand"]
fn export_cad_canvas_review() {
    let mut app = StyleRepo::default();
    let cad = studios().iter().position(|studio| studio.id == "cad").unwrap();
    let _ = app.update(Action::SelectStudio(cad));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("tekenen"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-cad-canvas-forge.png"))
        .expect("save CAD canvas review");
}

#[test]
#[ignore = "regenerate native Pointcloud review on demand"]
fn export_pointcloud_ribbon_review() {
    let mut app = StyleRepo::default();
    let pointcloud = studios().iter().position(|studio| studio.id == "pointcloud").unwrap();
    let _ = app.update(Action::SelectStudio(pointcloud));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("start"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pointcloud-ribbon-forge.png"))
        .expect("save Pointcloud ribbon review");
}

#[test]
#[ignore = "regenerate native PDF ribbon review on demand"]
fn export_pdf_ribbon_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("tekenen"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-ribbon-forge.png"))
        .expect("save PDF ribbon review");
}

#[test]
#[ignore = "regenerate native PDF Home ribbon review on demand"]
fn export_pdf_home_ribbon_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_with_options(&app, theme, false, Some("start"))
            .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join(format!("design/style-repo-pdf-home-{name}.png")))
            .expect("save PDF Home ribbon review");
    }
}

#[test]
#[ignore = "regenerate native PDF image-tab review on demand"]
fn export_pdf_image_ribbon_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("afbeelding"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-image-forge.png"))
        .expect("save PDF image-tab review");
}

#[test]
#[ignore = "regenerate native PDF Arrange-tab review on demand"]
fn export_pdf_arrange_ribbon_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    render_sized(&app, Theme::Forge, false, Some("schikken"), Size::new(3200.0, 800.0))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-arrange-forge.png"))
        .expect("save PDF Arrange-tab review");
}

#[test]
#[ignore = "regenerate native PDF Format-tab review on demand"]
fn export_pdf_format_ribbon_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    for (theme, name) in [(Theme::Forge, "forge"), (Theme::Light, "light")] {
        render_sized(&app, theme, false, Some("opmaak"), Size::new(2800.0, 800.0))
            .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("design/style-repo-pdf-format-{name}.png")))
            .expect("save PDF Format-tab review");
    }
    let _ = app.update(Action::PdfFormatSymbolStamp);
    render_sized(&app, Theme::Forge, false, Some("opmaak"), Size::new(2800.0, 800.0))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-symbol-forge.png"))
        .expect("save PDF symbol-stamp Format review");
    let _ = app.update(Action::PdfFormatSymbolStamp);
    let _ = app.update(Action::PdfFormatStyle(7));
    render_sized(&app, Theme::Forge, false, Some("opmaak"), Size::new(2800.0, 800.0))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-preset-forge.png"))
        .expect("save PDF cloudy style Format review");
}

#[test]
#[ignore = "regenerate native PDF Format palette review on demand"]
fn export_pdf_format_palette_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    render_sized(&app, Theme::Forge, false, Some("opmaak"), Size::new(1280.0, 1100.0))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-palette-forge.png"))
        .expect("save PDF Format palette review");
}

#[test]
#[ignore = "regenerate PDF Format ribbon palette popup on demand"]
fn export_pdf_format_palette_popup_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    let _ = app.update(Action::PdfFormatTogglePalette(0));
    render_with_options(&app, Theme::Forge, false, Some("opmaak"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-popup-forge.png"))
        .expect("save PDF Format palette popup review");
}

#[test]
#[ignore = "regenerate PDF Format custom color editor on demand"]
fn export_pdf_format_custom_color_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    let _ = app.update(Action::PdfFormatTogglePalette(0));
    let _ = app.update(Action::PdfFormatCustomToggle);
    render_with_options(&app, Theme::Forge, false, Some("opmaak"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-custom-forge.png"))
        .expect("save PDF Format custom color editor review");
}

#[test]
#[ignore = "regenerate PDF Format style gallery popup on demand"]
fn export_pdf_format_gallery_popup_review() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    let _ = app.update(Action::PdfFormatToggleGallery);
    render_with_options(&app, Theme::Forge, false, Some("opmaak"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pdf-format-gallery-forge.png"))
        .expect("save PDF Format style gallery popup review");
}

#[test]
fn pdf_format_popup_dispatches_source_color_and_closes_outside() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::PdfFormatTogglePalette(0));
    let mut state = ShellState::new(Preferences::default());
    state.active_tab = "opmaak".into();
    let mut element = openaec_ui::shell(&state, Slots {
        title: app.title(), mode: app.chrome_mode(), tabs: app.ribbon(Language::Dutch),
        documents: app.documents(), active_document: app.active_document(),
        file_commands: app.file_commands(Language::Dutch),
        file_active_label: app.file_active_label(Language::Dutch),
        quick_commands: app.quick_commands(Language::Dutch),
        status: app.status(Language::Dutch),
        overlay: None,
        content: Box::new(|_| text("test").into()),
    });
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let size = Size::new(1280.0, 800.0);
    let node = element.as_widget_mut().layout(&mut tree, &renderer,
        &layout::Limits::new(Size::ZERO, size));
    let mut overlay = element.as_widget_mut().overlay(&mut tree, Layout::new(&node),
        &renderer, &Rectangle::with_size(size), Vector::ZERO).expect("open color palette overlay");
    let popup_node = overlay.as_overlay_mut().layout(&renderer, size);
    let mut clipboard = iced::advanced::clipboard::Null;
    let click = iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left));
    let mut messages = Vec::new();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.as_overlay_mut().update(&click.clone(), Layout::new(&popup_node),
        mouse::Cursor::Available(iced::Point::new(516.0, 192.0)),
        &renderer, &mut clipboard, &mut shell);
    overlay.as_overlay_mut().update(&iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), mouse::Cursor::Available(iced::Point::new(516.0, 192.0)),
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatFill(9)))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let no_fill_cursor = mouse::Cursor::Available(iced::Point::new(510.0, 260.0));
    overlay.as_overlay_mut().update(&click.clone(), Layout::new(&popup_node), no_fill_cursor,
        &renderer, &mut clipboard, &mut shell);
    overlay.as_overlay_mut().update(&iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), no_fill_cursor,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatNoFill))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let custom_cursor = mouse::Cursor::Available(iced::Point::new(595.0, 260.0));
    overlay.as_overlay_mut().update(&click.clone(), Layout::new(&popup_node), custom_cursor,
        &renderer, &mut clipboard, &mut shell);
    overlay.as_overlay_mut().update(&iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), custom_cursor,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatCustomToggle))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.as_overlay_mut().update(&click, Layout::new(&popup_node),
        mouse::Cursor::Available(iced::Point::new(100.0, 300.0)),
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatClosePalette))));
}

#[test]
fn pdf_format_gallery_popup_selects_hidden_style_and_closes_outside() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::PdfFormatToggleGallery);
    let mut state = ShellState::new(Preferences::default());
    state.active_tab = "opmaak".into();
    let mut element = openaec_ui::shell(&state, Slots {
        title: app.title(), mode: app.chrome_mode(), tabs: app.ribbon(Language::Dutch),
        documents: app.documents(), active_document: app.active_document(),
        file_commands: app.file_commands(Language::Dutch),
        file_active_label: app.file_active_label(Language::Dutch),
        quick_commands: app.quick_commands(Language::Dutch),
        status: app.status(Language::Dutch),
        overlay: None,
        content: Box::new(|_| text("test").into()),
    });
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let size = Size::new(1280.0, 800.0);
    let node = element.as_widget_mut().layout(&mut tree, &renderer,
        &layout::Limits::new(Size::ZERO, size));
    let mut overlay = element.as_widget_mut().overlay(&mut tree, Layout::new(&node),
        &renderer, &Rectangle::with_size(size), Vector::ZERO).expect("open style gallery overlay");
    let popup_node = overlay.as_overlay_mut().layout(&renderer, size);
    let mut clipboard = iced::advanced::clipboard::Null;
    let click = iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left));
    let release = iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left));
    let mut messages = Vec::new();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let hidden_style = mouse::Cursor::Available(iced::Point::new(415.0, 218.0));
    overlay.as_overlay_mut().update(&click.clone(), Layout::new(&popup_node), hidden_style,
        &renderer, &mut clipboard, &mut shell);
    overlay.as_overlay_mut().update(&release, Layout::new(&popup_node), hidden_style,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatStyle(9)))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.as_overlay_mut().update(&click, Layout::new(&popup_node),
        mouse::Cursor::Available(iced::Point::new(700.0, 300.0)),
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatCloseGallery))));
}

#[test]
fn pdf_format_palette_renders_all_source_colors_in_seven_columns() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    let picture = render_sized(&app, Theme::Forge, false, Some("opmaak"), Size::new(1280.0, 1100.0));
    for column in 0..7 {
        for row in 0..6 {
            let index = column * 6 + row;
            let expected = ribbon_preview::pdf_color(ribbon_preview::PDF_FORMAT_PALETTE[index]);
            let expected = [expected.r, expected.g, expected.b].map(|value| (value * 255.0).round() as u8);
            let x = 541 + 20 * column;
            let y = 750 + 19 * row;
            let at = ((y * picture.width() as usize + x) * 4) as usize;
            let actual = &picture.data()[at..at + 3];
            assert!(actual.iter().zip(expected).all(|(a, e)| a.abs_diff(e) <= 1),
                "source palette color {index} at ({x},{y}): {actual:?} != {expected:?}");
        }
    }
}

#[test]
fn atlas_workspace_respects_each_theme_background() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::SelectStudio(1));
    let _ = app.update(Action::SelectScreen(1));
    for theme in Theme::ALL {
        let picture = render(&app, theme);
        let at = ((400 * picture.width() + 1000) * 4) as usize;
        let actual = &picture.data()[at..at + 3];
        let [red, green, blue, _] = theme.tokens().bg.into_rgba8();
        assert!(
            actual
                .iter()
                .zip([red, green, blue])
                .all(|(a, e)| a.abs_diff(e) <= 1),
            "{theme} atlas background: {actual:?}"
        );
    }
}

#[test]
fn pdf_image_source_icons_render_as_standalone_svg() {
    let mut app = StyleRepo::default();
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let picture = render_with_options(&app, Theme::Forge, false, Some("afbeelding"));
    for (name, left, right, top, bottom) in [
        ("crop", 29, 51, 70, 100),
        ("brightness", 296, 314, 78, 96),
        ("contrast", 296, 314, 101, 119),
    ] {
        let bright = (left..right).flat_map(|x| (top..bottom).map(move |y| (x, y)))
            .filter(|&(x, y)| {
                let at = ((y * picture.width() + x) * 4) as usize;
                picture.data()[at..at + 3].iter().all(|channel| *channel >= 150)
            }).count();
        assert!(bright > 5, "PDF {name} icon missing from native render: {bright} light pixels");
    }
}

#[test]
fn pile_utilization_range_renders_two_thumbs_and_one_selected_band() {
    let mut app = StyleRepo::default();
    let pile = studios().iter().position(|studio| studio.id == "pile").unwrap();
    let _ = app.update(Action::SelectStudio(pile));
    for theme in [Theme::Light, Theme::Forge] {
        let picture = render_with_options(&app, theme, false, Some("weergave"));
        let [red, green, blue, _] = theme.tokens().accent.into_rgba8();
        for x in [239, 280, 325] {
            let at = ((106 * picture.width() + x) * 4) as usize;
            assert!(picture.data()[at..at + 3].iter().zip([red, green, blue])
                .all(|(actual, expected)| actual.abs_diff(expected) <= 1),
                "{theme} Pile range missing selected band or thumb at x={x}");
        }
        for x in [210, 350] {
            let at = ((106 * picture.width() + x) * 4) as usize;
            assert_ne!(&picture.data()[at..at + 3], &[red, green, blue],
                "{theme} Pile range leaked selection outside handles at x={x}");
        }
    }
}

#[test]
fn long_ribbon_keeps_group_caption_above_horizontal_scrollbar() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::SelectStudio(4));
    let picture = render_with_options(&app, Theme::Light, false, Some("start"));
    let orange_ink = (210..270)
        .flat_map(|x| (138..150).map(move |y| (x, y)))
        .filter(|&(x, y)| {
            let at = ((y * picture.width() + x) * 4) as usize;
            let (r, g, b) = (
                u16::from(picture.data()[at]),
                u16::from(picture.data()[at + 1]),
                u16::from(picture.data()[at + 2]),
            );
            r > 160 && r > g + 40 && g > b + 35
        })
        .count();
    assert!(
        orange_ink > 12,
        "Planner group caption hidden by scrollbar: {orange_ink} pixels"
    );
}

#[test]
fn energy_workflow_uses_document_band_without_ribbon_or_properties_panel() {
    let mut app = StyleRepo::default();
    let energy = studios().iter().position(|studio| studio.id == "energy").unwrap();
    let _ = app.update(Action::SelectStudio(energy));
    let _ = app.update(Action::SelectScreen(1));
    assert_eq!(app.chrome_mode(), ChromeMode::Workflow);
    for mode in EnergyMode::ALL {
        let _ = app.update(Action::SelectEnergyMode(mode));
        for theme in [Theme::Light, Theme::Forge] {
            let picture = render(&app, theme);
            let [red, green, blue, _] = theme.tokens().docbar_bg.into_rgba8();
            let at = ((45 * picture.width() + 1000) * 4) as usize;
            assert!(picture.data()[at..at + 3].iter().zip([red, green, blue])
                .all(|(actual, expected)| actual.abs_diff(expected) <= 1),
                "{mode:?} {theme} document band at y=45");
        }
    }
}

#[test]
#[ignore = "regenerate native Pile Weergave review on demand"]
fn export_pile_view_ribbon_review() {
    let mut app = StyleRepo::default();
    let pile = studios().iter().position(|studio| studio.id == "pile").unwrap();
    let _ = app.update(Action::SelectStudio(pile));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("weergave"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pile-view-forge.png"))
        .expect("save Pile Weergave ribbon review");
}

#[test]
#[ignore = "regenerate source-icon Pile Plan ribbon on demand"]
fn export_pile_plan_source_icon_review() {
    let mut app = StyleRepo::default();
    let pile = studios().iter().position(|studio| studio.id == "pile").unwrap();
    let _ = app.update(Action::SelectStudio(pile));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("plan"))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pile-ribbon-forge.png"))
        .expect("save Pile Plan source-icon ribbon review");
    render_sized(&app, Theme::Forge, false, Some("plan"), Size::new(1600.0, 800.0))
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-pile-ribbon-wide-forge.png"))
        .expect("save complete Pile Plan source-icon ribbon review");
}

#[test]
#[ignore = "regenerate shared File navigation review on demand"]
fn export_shared_backstage_review() {
    let app = StyleRepo::default();
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized_with_reset(
            &app, theme, false, None, Size::new(1280.0, 800.0), false, true,
        )
        .save_png(&design.join(format!("style-repo-backstage-{name}.png")))
        .expect("save shared File navigation review");
    }
}

#[test]
#[ignore = "regenerate shared File task tiles on demand"]
fn export_backstage_task_tiles_review() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::Show(Page::Components));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized(&app, theme, false, None, Size::new(1280.0, 1000.0))
            .save_png(&design.join(format!("style-repo-backstage-tiles-{name}.png")))
            .expect("save File task tile review");
    }
}

#[test]
#[ignore = "regenerate minimum-size File view on demand"]
fn export_backstage_minimum_window_review() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::Show(Page::Components));
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized_with_reset(
            &app, theme, false, None, Size::new(720.0, 480.0), false, true,
        )
        .save_png(&design.join(format!("style-repo-backstage-small-{name}.png")))
        .expect("save minimum-size File view");
        render_sized(&app, theme, false, None, Size::new(720.0, 480.0))
            .save_png(&design.join(format!("style-repo-components-small-{name}.png")))
            .expect("save minimum-size components view");
    }
}

#[test]
fn minimum_window_renders_file_and_component_states() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::Show(Page::Components));
    for theme in [Theme::Light, Theme::Forge] {
        let file = render_sized_with_reset(
            &app, theme, false, None, Size::new(720.0, 480.0), false, true,
        );
        let workspace = render_sized(&app, theme, false, None, Size::new(720.0, 480.0));
        assert_eq!((file.width(), file.height()), (720, 480));
        assert_eq!((workspace.width(), workspace.height()), (720, 480));
    }
}

#[test]
fn ribbon_tabs_keep_the_source_outline_and_continuous_rule() {
    let app = StyleRepo::default();
    for theme in [Theme::Light, Theme::Forge] {
        let picture = render_with_options(&app, theme, false, None);
        let rgb = |x: u32, y: u32| {
            let at = ((y * picture.width() + x) * 4) as usize;
            &picture.data()[at..at + 3]
        };
        let tokens = theme.tokens();
        let [ar, ag, ab, _] = tokens.accent.into_rgba8();
        let [br, bg, bb, _] = tokens.bg.into_rgba8();
        assert_eq!(rgb(40, 50), &[ar, ag, ab], "{theme} File tab");
        assert_eq!(rgb(110, 32), &[ar, ag, ab], "{theme} active top border");
        assert_eq!(rgb(110, 59), &[br, bg, bb], "{theme} active bottom gap");
        assert_eq!(rgb(500, 59), &[ar, ag, ab], "{theme} continuous rule");
        let file = render_sized_with_reset(
            &app, theme, false, None, Size::new(1280.0, 800.0), false, true,
        );
        let at = ((32 * file.width() + 110) * 4) as usize;
        assert_ne!(&file.data()[at..at + 3], &[ar, ag, ab],
            "{theme} workspace tab must not remain active in File view");
    }
}

#[test]
#[ignore = "regenerate native review images on demand"]
fn export_native_style_repo_previews() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    save_render(&app, Theme::Light, &design.join("style-repo-native.png"));
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_with_settings(&app, theme, true)
            .save_png(&design.join(format!("style-repo-settings-{name}.png")))
            .expect("save native settings review image");
    }
    app.show(Page::Components);
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        save_render(
            &app,
            theme,
            &design.join(format!("style-repo-components-{name}.png")),
        );
    }
    app.show(Page::Icons);
    save_render(
        &app,
        Theme::Light,
        &design.join("style-repo-icons-light.png"),
    );
    save_render(
        &app,
        Theme::Forge,
        &design.join("style-repo-icons-forge.png"),
    );
    app.show(Page::Studios);
    let _ = app.update(Action::SelectStudio(1));
    let _ = app.update(Action::SelectScreen(1));
    for (theme, name) in [
        (Theme::Light, "light"),
        (Theme::Forge, "forge"),
        (Theme::OpenAec, "openaec"),
        (Theme::Blueprint, "blueprint"),
        (Theme::Contrast, "contrast"),
    ] {
        save_render(
            &app,
            theme,
            &design.join(format!("style-repo-atlas-{name}.png")),
        );
    }
    let _ = app.update(Action::SelectStudio(2));
    render_with_options(&app, Theme::Light, false, Some("geometrie"))
        .save_png(&design.join("style-repo-fem-ribbon-light.png"))
        .expect("save FEM concept ribbon");
    let _ = app.update(Action::SelectStudio(3));
    render_with_options(&app, Theme::Forge, false, Some("modelleren"))
        .save_png(&design.join("style-repo-bim-ribbon-forge.png"))
        .expect("save BIM concept ribbon");
    let _ = app.update(Action::SelectStudio(4));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("start"))
        .save_png(&design.join("style-repo-planner-ribbon-light.png"))
        .expect("save Planner ribbon review");
    let calc = studios().iter().position(|studio| studio.id == "calc").unwrap();
    let _ = app.update(Action::SelectStudio(calc));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("begroting"))
        .save_png(&design.join("style-repo-calc-ribbon-light.png"))
        .expect("save Calc ribbon review");
    let geotech = studios().iter().position(|studio| studio.id == "geotech").unwrap();
    let _ = app.update(Action::SelectStudio(geotech));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("home"))
        .save_png(&design.join("style-repo-geotech-ribbon-light.png"))
        .expect("save Geotechniek ribbon review");
    let heatloss = studios().iter().position(|studio| studio.id == "heatloss").unwrap();
    let _ = app.update(Action::SelectStudio(heatloss));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("vertrekken"))
        .save_png(&design.join("style-repo-heatloss-ribbon-light.png"))
        .expect("save Heatloss ribbon review");
    let calculations = studios().iter().position(|studio| studio.id == "calculations").unwrap();
    let _ = app.update(Action::SelectStudio(calculations));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("start"))
        .save_png(&design.join("style-repo-calculations-ribbon-light.png"))
        .expect("save Calculations ribbon review");
    let reports = studios().iter().position(|studio| studio.id == "reports").unwrap();
    let _ = app.update(Action::SelectStudio(reports));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("start"))
        .save_png(&design.join("style-repo-reports-ribbon-light.png"))
        .expect("save Reports ribbon review");
    let validator = studios().iter().position(|studio| studio.id == "validator").unwrap();
    let _ = app.update(Action::SelectStudio(validator));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("start"))
        .save_png(&design.join("style-repo-validator-ribbon-light.png"))
        .expect("save BIM Validator ribbon review");
    let pile = studios().iter().position(|studio| studio.id == "pile").unwrap();
    let _ = app.update(Action::SelectStudio(pile));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("plan"))
        .save_png(&design.join("style-repo-pile-ribbon-forge.png"))
        .expect("save Pile Plan ribbon review");
    let speech = studios().iter().position(|studio| studio.id == "speech").unwrap();
    let _ = app.update(Action::SelectStudio(speech));
    render(&app, Theme::Forge)
        .save_png(&design.join("style-repo-speech-sidebar-forge.png"))
        .expect("save Speech sidebar review");
    let frame = studios().iter().position(|studio| studio.id == "frame").unwrap();
    let _ = app.update(Action::SelectStudio(frame));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Light, false, Some("home"))
        .save_png(&design.join("style-repo-frame-ribbon-light.png"))
        .expect("save Frame ribbon review");
    let field = studios().iter().position(|studio| studio.id == "field").unwrap();
    let _ = app.update(Action::SelectStudio(field));
    render(&app, Theme::Light)
        .save_png(&design.join("style-repo-field-topnav-light.png"))
        .expect("save Field top navigation review");
    let aec = studios().iter().position(|studio| studio.id == "2d").unwrap();
    let _ = app.update(Action::SelectStudio(aec));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("aec"))
        .save_png(&design.join("style-repo-2d-extension-forge.png"))
        .expect("save AEC extension review");
    let cad = studios().iter().position(|studio| studio.id == "cad").unwrap();
    let _ = app.update(Action::SelectStudio(cad));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("tekenen"))
        .save_png(&design.join("style-repo-cad-canvas-forge.png"))
        .expect("save CAD canvas review");
    let pointcloud = studios().iter().position(|studio| studio.id == "pointcloud").unwrap();
    let _ = app.update(Action::SelectStudio(pointcloud));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("start"))
        .save_png(&design.join("style-repo-pointcloud-ribbon-forge.png"))
        .expect("save Pointcloud ribbon review");
    let pdf = studios().iter().position(|studio| studio.id == "pdf").unwrap();
    let _ = app.update(Action::SelectStudio(pdf));
    let _ = app.update(Action::SelectScreen(1));
    render_with_options(&app, Theme::Forge, false, Some("tekenen"))
        .save_png(&design.join("style-repo-pdf-ribbon-forge.png"))
        .expect("save PDF ribbon review");
    let energy = studios().iter().position(|studio| studio.id == "energy").unwrap();
    let _ = app.update(Action::SelectStudio(energy));
    let _ = app.update(Action::SelectScreen(1));
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render(&app, theme)
            .save_png(&design.join(format!("style-repo-energy-workflow-{name}.png")))
            .expect("save Energy workflow review");
    }
    for (mode, theme, name) in [
        (EnergyMode::NewBuildUtility, Theme::Light, "utility-light"),
        (EnergyMode::ExistingResidential, Theme::Light, "existing-light"),
        (EnergyMode::ExistingUtility, Theme::Forge, "existing-utility-forge"),
    ] {
        let _ = app.update(Action::SelectEnergyMode(mode));
        render(&app, theme)
            .save_png(&design.join(format!("style-repo-energy-workflow-{name}.png")))
            .expect("save Energy workflow variant");
    }
}

#[test]
#[ignore = "regenerate native icon atlas after shared icon changes"]
fn export_native_icon_atlas() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    app.show(Page::Icons);
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        save_render(&app, theme, &design.join(format!("style-repo-icons-{name}.png")));
        render_sized(&app, theme, false, None, Size::new(1280.0, 2400.0))
            .save_png(&design.join(format!("style-repo-ribbon-icons-{name}.png")))
            .expect("save typed ribbon-icon review");
    }
}

#[test]
#[ignore = "regenerate shared property-grid component images on demand"]
fn export_shared_property_grid_review() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    app.show(Page::Components);
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        save_render(&app, theme, &design.join(format!("style-repo-components-{name}.png")));
        render_sized(&app, theme, false, None, Size::new(1280.0, 1000.0))
            .save_png(&design.join(format!("style-repo-property-grid-{name}.png")))
            .expect("save full property-grid review");
    }
}

#[test]
#[ignore = "regenerate general modal review images on demand"]
fn export_general_dialog_review() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    app.show(Page::Components);
    app.sample_dialog = true;
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized(&app, theme, false, None, Size::new(1280.0, 800.0))
            .save_png(&design.join(format!("style-repo-dialog-{name}.png")))
            .expect("save shared general modal review");
    }
    render_sized(&app, Theme::Light, false, None, Size::new(1280.0, 480.0))
        .save_png(&design.join("style-repo-dialog-short-light.png"))
        .expect("save short-window general modal review");
}

#[test]
#[ignore = "regenerate BIM reference icon review images on demand"]
fn export_bim_reference_review() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    app.show(Page::Bim);
    for (theme, name) in [(Theme::Light, "light"), (Theme::Forge, "forge")] {
        render_sized(&app, theme, false, None, Size::new(1280.0, 800.0))
            .save_png(&design.join(format!("style-repo-bim-references-{name}.png")))
            .expect("save native BIM reference icon review");
    }
}

#[test]
fn sample_dialog_saves_only_after_confirmation() {
    let mut app = StyleRepo::default();
    app.sample_input = "Original".into();
    let _ = app.update(Action::SampleDialog(true));
    let _ = app.update(Action::SampleDialogInput("Preview".into()));
    let _ = app.update(Action::SampleDialog(false));
    assert_eq!(app.sample_input, "Original");
    let _ = app.update(Action::SampleDialog(true));
    let _ = app.update(Action::SampleDialogInput("Saved".into()));
    let _ = app.update(Action::SampleDialogSave);
    assert_eq!(app.sample_input, "Saved");
    assert!(!app.sample_dialog);
}

#[test]
fn general_modal_renders_vertical_gradient_and_shadow() {
    let mut app = StyleRepo::default();
    app.show(Page::Components);
    app.sample_dialog = true;
    let picture = render_sized(&app, Theme::Light, false, None, Size::new(1280.0, 800.0));
    let red = |x: usize, y: usize| picture.data()[(y * picture.width() as usize + x) * 4];
    assert!(red(640, 308) < red(640, 330), "header must fade down toward dialog white");
    assert!(red(399, 350) < red(380, 350), "shadow must darken overlay beside the card");
    let forge = render_sized(&app, Theme::Forge, false, None, Size::new(1280.0, 800.0));
    let red = |x: usize, y: usize| forge.data()[(y * forge.width() as usize + x) * 4];
    assert!(red(640, 308) > red(640, 330), "Forge header must fade toward dark dialog bg");
}
