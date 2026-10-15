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
        let mut system = iced_tiny_skia::graphics::text::font_system()
            .write()
            .expect("font system");
        for bytes in fonts::FILES {
            system.load_font(std::borrow::Cow::Borrowed(bytes));
        }
    });
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
    render_sized_with_reset(app, theme, show_settings, active_tab, size, false)
}

fn render_sized_with_reset(
    app: &StyleRepo,
    theme: Theme,
    show_settings: bool,
    active_tab: Option<&str>,
    size: Size,
    reset_confirm: bool,
) -> tiny_skia::Pixmap {
    load_fonts();
    let mut preferences = Preferences::default();
    preferences.theme = theme;
    let mut state = ShellState::new(preferences);
    state.settings = show_settings;
    state.settings_reset_confirm = reset_confirm;
    if show_settings {
        state.settings_page = openaec_ui::SettingsPage::Appearance;
        state.settings_theme_open = !reset_confirm;
    }
    if let Some(tab) = active_tab {
        state.active_tab = tab.into();
    }
    let language = Language::Dutch;
    let mut element = openaec_ui::shell(
        &state,
        Slots {
            title: app.title(),
            mode: app.chrome_mode(),
            tabs: app.ribbon(language),
            documents: app.documents(),
            active_document: app.active_document(),
            file_commands: app.file_commands(language),
            quick_commands: app.quick_commands(language),
            status: app.status(language),
            content: Box::new(|region| match region {
                Region::Workspace => app.workspace(theme, language).map(Message::Command),
                Region::Explorer => widgets::panel(
                    if app.chrome_mode() == ChromeMode::Workflow { language.text("Werkstroom", "Workflow") } else if app.chrome_mode() == ChromeMode::Sidebar { language.text("Navigatie", "Navigation") } else if app.chrome_mode() == ChromeMode::CanvasRibbon { language.text("Eigenschappen", "Properties") } else { language.text("Verkenner", "Explorer") },
                    app.explorer(theme, language).map(Message::Command),
                    theme,
                ),
                Region::Properties => widgets::panel(
                    language.text("Eigenschappen", "Properties"),
                    app.properties(theme, language).map(Message::Command),
                    theme,
                ),
            }),
        },
    );
    let mut renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let node =
        element
            .as_widget()
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
    if let Some(mut overlay) = element.as_widget_mut().overlay(
        &mut tree, Layout::new(&node), &renderer, Vector::ZERO,
    ) {
        let popup_node = overlay.layout(&renderer, size);
        overlay.draw(
            &mut renderer,
            &iced_theme,
            &renderer::Style { text_color: iced_theme.palette().text },
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
    software.draw::<&str>(
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
    render_sized_with_reset(&app, Theme::Forge, true, None, Size::new(1280.0, 800.0), true)
        .save_png(&design.join("style-repo-settings-reset-forge.png"))
        .expect("save reset confirmation review");
}

#[test]
fn expanded_theme_menu_keeps_the_trigger_height_in_form_layout() {
    load_fonts();
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    for open in [false, true] {
        let element = widgets::settings_theme_picker(
            vec![(Theme::Light, "Light".to_owned(), ())],
            Theme::Light, Theme::Light, open, (),
        );
        let mut tree = Tree::new(&element);
        let node = element.as_widget().layout(
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
        quick_commands: app.quick_commands(Language::Dutch),
        status: app.status(Language::Dutch),
        content: Box::new(|_| text("test").into()),
    });
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let size = Size::new(1280.0, 800.0);
    let node = element.as_widget().layout(&mut tree, &renderer,
        &layout::Limits::new(Size::ZERO, size));
    let mut overlay = element.as_widget_mut().overlay(&mut tree, Layout::new(&node),
        &renderer, Vector::ZERO).expect("open color palette overlay");
    let popup_node = overlay.layout(&renderer, size);
    let mut clipboard = iced::advanced::clipboard::Null;
    let click = iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left));
    let mut messages = Vec::new();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.on_event(click.clone(), Layout::new(&popup_node),
        mouse::Cursor::Available(iced::Point::new(516.0, 192.0)),
        &renderer, &mut clipboard, &mut shell);
    overlay.on_event(iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), mouse::Cursor::Available(iced::Point::new(516.0, 192.0)),
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatFill(9)))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let no_fill_cursor = mouse::Cursor::Available(iced::Point::new(510.0, 260.0));
    overlay.on_event(click.clone(), Layout::new(&popup_node), no_fill_cursor,
        &renderer, &mut clipboard, &mut shell);
    overlay.on_event(iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), no_fill_cursor,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatNoFill))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let custom_cursor = mouse::Cursor::Available(iced::Point::new(595.0, 260.0));
    overlay.on_event(click.clone(), Layout::new(&popup_node), custom_cursor,
        &renderer, &mut clipboard, &mut shell);
    overlay.on_event(iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left)),
        Layout::new(&popup_node), custom_cursor,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatCustomToggle))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.on_event(click, Layout::new(&popup_node),
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
        quick_commands: app.quick_commands(Language::Dutch),
        status: app.status(Language::Dutch),
        content: Box::new(|_| text("test").into()),
    });
    let renderer = iced_tiny_skia::Renderer::new(fonts::BODY, iced::Pixels(12.0));
    let mut tree = Tree::new(&element);
    let size = Size::new(1280.0, 800.0);
    let node = element.as_widget().layout(&mut tree, &renderer,
        &layout::Limits::new(Size::ZERO, size));
    let mut overlay = element.as_widget_mut().overlay(&mut tree, Layout::new(&node),
        &renderer, Vector::ZERO).expect("open style gallery overlay");
    let popup_node = overlay.layout(&renderer, size);
    let mut clipboard = iced::advanced::clipboard::Null;
    let click = iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left));
    let release = iced::Event::Mouse(iced::mouse::Event::ButtonReleased(iced::mouse::Button::Left));
    let mut messages = Vec::new();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    let hidden_style = mouse::Cursor::Available(iced::Point::new(415.0, 218.0));
    overlay.on_event(click.clone(), Layout::new(&popup_node), hidden_style,
        &renderer, &mut clipboard, &mut shell);
    overlay.on_event(release, Layout::new(&popup_node), hidden_style,
        &renderer, &mut clipboard, &mut shell);
    assert!(messages.iter().any(|message| matches!(message,
        Message::Command(Action::PdfFormatStyle(9)))), "messages: {messages:?}");
    messages.clear();
    let mut shell = iced::advanced::Shell::new(&mut messages);
    overlay.on_event(click, Layout::new(&popup_node),
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
