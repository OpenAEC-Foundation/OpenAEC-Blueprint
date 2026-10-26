//! OpenAEC-iconen. Bron: `design/icons/` in OpenAEC-style-book;
//! `generated.rs` wordt door `npm run generate` gemaakt.

mod generated;
pub use generated::Icon;

impl Icon {
    /// SVG met `currentColor` vervangen door een vaste kleur (bijv. `"#36363E"`).
    /// Nodig voor renderers die geen `currentColor` kennen.
    pub fn svg_colored(self, hex: &str) -> String {
        self.svg().replace("currentColor", hex)
    }
}
