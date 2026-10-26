//! OpenAEC design tokens voor Rust-applicaties.
//!
//! Bron: `design/tokens/` in OpenAEC-style-book. De constanten in `generated.rs`
//! worden door `npm run generate` gemaakt; pas de bron aan, niet die code.
//! Lengtes zijn in pixels (1rem = 16px); letterafstand in em.

mod generated;
pub use generated::*;

/// Kleur als 8-bit RGBA.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Rgba {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}

impl Rgba {
    pub const fn new(r: u8, g: u8, b: u8, a: u8) -> Self {
        Self { r, g, b, a }
    }

    /// `#RRGGBB`, of `#RRGGBBAA` als de kleur niet volledig dekkend is.
    pub fn to_hex(self) -> String {
        if self.a == 255 {
            format!("#{:02X}{:02X}{:02X}", self.r, self.g, self.b)
        } else {
            format!("#{:02X}{:02X}{:02X}{:02X}", self.r, self.g, self.b, self.a)
        }
    }

    /// Kanalen als 0.0–1.0, in de volgorde r, g, b, a.
    pub fn to_f32(self) -> [f32; 4] {
        [self.r, self.g, self.b, self.a].map(|c| c as f32 / 255.0)
    }
}
