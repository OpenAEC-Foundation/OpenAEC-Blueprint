use crate::tokens::{self, Tokens};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Theme {
    #[default]
    Light,
    Forge,
    OpenAec,
    Blueprint,
    Contrast,
}
impl Theme {
    pub const ALL: [Self; 5] = [Self::Light, Self::Forge, Self::OpenAec, Self::Blueprint, Self::Contrast];
    pub fn tokens(self) -> Tokens {
        match self { Self::Light => tokens::LIGHT, Self::Forge => tokens::FORGE, Self::OpenAec => tokens::OPENAEC, Self::Blueprint => tokens::BLUEPRINT, Self::Contrast => tokens::CONTRAST }
    }
    pub fn iced(self) -> iced::Theme {
        let t = self.tokens();
        iced::Theme::custom(self.to_string(), iced::theme::Palette {
            background: t.bg, text: t.text, primary: t.accent,
            success: iced::Color::from_rgb8(22, 163, 74), danger: t.danger_color,
        })
    }
}
impl std::fmt::Display for Theme {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(match self { Self::Light => "Light", Self::Forge => "Forge", Self::OpenAec => "OpenAEC", Self::Blueprint => "Blueprint", Self::Contrast => "High contrast" })
    }
}
