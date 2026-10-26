//! Model en validatie van `ribbon.toml` (formaat 1) voor OpenAEC-applicaties.
//! Specificatie: `docs/superpowers/specs/2026-10-15-ui-fundament-design.md` §5.

mod generated;
mod model;
mod validate;

pub use generated::SHARED_TABS;
pub use model::*;
pub use validate::{validate_ribbon, validate_shared, AppLabels, Issue, STANDARD_COMMANDS};

pub fn parse_ribbon(src: &str) -> Result<RibbonFile, String> {
    toml::from_str(src).map_err(|e| e.to_string())
}

pub fn parse_shared(src: &str) -> Result<SharedTabFile, String> {
    toml::from_str(src).map_err(|e| e.to_string())
}

pub fn shared_tab_source(name: &str) -> Option<&'static str> {
    SHARED_TABS.iter().find(|(n, _)| *n == name).map(|(_, src)| *src)
}
