//! Reproducible software renders of the actual native Style Repo shell.
use super::*;
use iced::advanced::layout::{self, Layout};
use iced::advanced::renderer;
use iced::advanced::widget::Tree;
use iced::{mouse, Color, Rectangle, Size};
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
    load_fonts();
    let size = Size::new(1280.0, 800.0);
    let mut preferences = Preferences::default();
    preferences.theme = theme;
    let mut state = ShellState::new(preferences);
    state.settings = show_settings;
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
            quick_commands: app.quick_commands(language),
            status: app.status(language),
            content: Box::new(|region| match region {
                Region::Workspace => app.workspace(theme, language).map(Message::Command),
                Region::Explorer => widgets::panel(
                    if app.chrome_mode() == ChromeMode::Workflow { language.text("Werkstroom", "Workflow") } else if app.chrome_mode() == ChromeMode::Sidebar { language.text("Navigatie", "Navigation") } else { language.text("Verkenner", "Explorer") },
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
#[ignore = "regenerate native Speech review on demand"]
fn export_speech_sidebar_review() {
    let mut app = StyleRepo::default();
    let speech = studios().iter().position(|studio| studio.id == "speech").unwrap();
    let _ = app.update(Action::SelectStudio(speech));
    render(&app, Theme::Forge)
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-speech-sidebar-forge.png"))
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
#[ignore = "regenerate native Field review on demand"]
fn export_field_topnav_review() {
    let mut app = StyleRepo::default();
    let field = studios().iter().position(|studio| studio.id == "field").unwrap();
    let _ = app.update(Action::SelectStudio(field));
    render(&app, Theme::Light)
        .save_png(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design/style-repo-field-topnav-light.png"))
        .expect("save Field top navigation review");
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
fn long_ribbon_keeps_group_caption_above_horizontal_scrollbar() {
    let mut app = StyleRepo::default();
    let _ = app.update(Action::SelectStudio(4));
    let picture = render_with_options(&app, Theme::Light, false, Some("start"));
    let orange_ink = (210..270)
        .flat_map(|x| (128..136).map(move |y| (x, y)))
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
