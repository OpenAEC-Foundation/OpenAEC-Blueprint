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
    load_fonts();
    let size = Size::new(1280.0, 800.0);
    let mut preferences = Preferences::default();
    preferences.theme = theme;
    let state = ShellState::new(preferences);
    let language = Language::Dutch;
    let element = openaec_ui::shell(
        &state,
        Slots {
            title: app.title(),
            tabs: app.ribbon(language),
            documents: app.documents(),
            active_document: app.active_document(),
            file_commands: app.file_commands(language),
            quick_commands: app.quick_commands(language),
            status: app.status(language),
            content: Box::new(|region| match region {
                Region::Workspace => app.workspace(theme, language).map(Message::Command),
                Region::Explorer => widgets::panel(
                    language.text("Verkenner", "Explorer"),
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
#[ignore = "regenerate native review images on demand"]
fn export_native_style_repo_previews() {
    let design = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("design");
    let mut app = StyleRepo::default();
    save_render(&app, Theme::Light, &design.join("style-repo-native.png"));
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
}
