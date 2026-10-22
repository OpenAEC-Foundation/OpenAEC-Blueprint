//! The B2 icons of OpenAEC UI 0.4, drawn by Codex, as a typed list.
//!
//! Each icon has a 16 px and a 24 px master, stored as gzip-compressed SVG
//! (byte copies of `design/icon-set-b2/library-lossless`). Turn on the feature of
//! your app, such as `features = ["pdf"]`, and only the icons of that app are
//! compiled in; using an icon of another app is a compile error.
//!
//! [`Icon::svg`] unpacks an icon once and returns the SVG text, which fits
//! `openaec_ui::design::widgets::glyph` directly: the main colour is
//! `currentColor` and the accent `var(--icon-accent, currentColor)`.
mod generated;

pub use generated::{Icon, APPS, REVISION};

use std::collections::HashMap;
use std::io::Read;
use std::sync::{Mutex, OnceLock};

/// The two masters. Use 16 for sizes up to 18 px and 24 above.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Size {
    S16,
    S24,
}

impl Size {
    /// The master that suits a size in pixels.
    pub fn for_pixels(pixels: f32) -> Self {
        if pixels <= 18.0 {
            Self::S16
        } else {
            Self::S24
        }
    }
}

impl Icon {
    /// The SVG text of the master, unpacked on first use and kept for the life
    /// of the program, so it can be passed on as `&'static str`.
    pub fn svg(self, size: Size) -> &'static str {
        static CACHE: OnceLock<Mutex<HashMap<(Icon, Size), &'static str>>> = OnceLock::new();
        let mut cache = CACHE.get_or_init(Default::default).lock().unwrap_or_else(|e| e.into_inner());
        cache.entry((self, size)).or_insert_with(|| {
            let mut text = String::new();
            flate2::read::GzDecoder::new(self.svgz(size)).read_to_string(&mut text).expect("valid gzip-compressed SVG");
            Box::leak(text.into_boxed_str())
        })
    }

    /// The SVG text for a size in pixels.
    pub fn svg_for(self, pixels: f32) -> &'static str {
        self.svg(Size::for_pixels(pixels))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_included_icon_unpacks_to_its_svg_master() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../design/icon-set-b2/svg");
        for icon in Icon::all() {
            assert_eq!(Icon::from_id(icon.id()), Some(icon));
            assert!(!icon.label().is_empty(), "{}", icon.id());
            assert!(!icon.apps().is_empty() && icon.apps().iter().all(|a| APPS.contains(a)), "{}", icon.id());
            for (size, folder) in [(Size::S16, "16"), (Size::S24, "24")] {
                let svg = icon.svg(size);
                assert!(svg.starts_with("<svg"), "{} {folder}", icon.id());
                // In the Style Repo the design masters are present: the bytes must match exactly.
                if let Ok(master) = std::fs::read_to_string(root.join(folder).join(format!("{}.svg", icon.id()))) {
                    assert_eq!(svg, master, "{} {folder}", icon.id());
                }
            }
        }
    }

    #[test]
    fn sizes_follow_pixels() {
        assert_eq!(Size::for_pixels(16.0), Size::S16);
        assert_eq!(Size::for_pixels(22.0), Size::S24);
    }
}
