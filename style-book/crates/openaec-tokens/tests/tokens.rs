use openaec_tokens::{color, font, spacing, Rgba, DARK, LIGHT};

#[test]
fn merkkleuren() {
    assert_eq!(color::brand::AMBER.to_hex(), "#D97706");
    assert_eq!(color::brand::DEEP_FORGE.to_hex(), "#36363E");
}

#[test]
fn themas() {
    assert_eq!(LIGHT.surface_bg.to_hex(), "#FAFAF9");
    assert_eq!(DARK.surface_bg.to_hex(), "#36363E");
    assert_eq!(DARK.border_focus.to_hex(), "#F59E0B");
    assert_ne!(LIGHT, DARK);
}

#[test]
fn maten_en_fonts() {
    assert_eq!(spacing::S4, 16.0);
    assert_eq!(spacing::RIBBON_HEIGHT, 96.0);
    assert_eq!(font::size::S2XL, 24.0);
    assert_eq!(font::family::HEADING, "Space Grotesk");
    assert_eq!(font::weight::BOLD, 700);
}

#[test]
fn rgba_hulpfuncties() {
    assert_eq!(Rgba::new(255, 0, 0, 128).to_hex(), "#FF000080");
    assert_eq!(Rgba::new(255, 0, 0, 255).to_f32(), [1.0, 0.0, 0.0, 1.0]);
}
