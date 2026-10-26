// @generated GEGENEREERD door generators/ uit design/ — niet met de hand bewerken.

pub mod color {
    pub mod brand {
        /// Alias voor signal-orange — backwards compat voor bestaande apps
        pub const ACCENT: crate::Rgba = crate::Rgba::new(0xEA, 0x58, 0x0C, 0xFF);
        /// Primary brand — buttons, links, accents. Nooit als grote achtergrondvlak (DESIGN-SYSTEM.md §2.1)
        pub const AMBER: crate::Rgba = crate::Rgba::new(0xD9, 0x77, 0x06, 0xFF);
        /// Light background (warm, not clinical)
        pub const BLUEPRINT_WHITE: crate::Rgba = crate::Rgba::new(0xFA, 0xFA, 0xF9, 0xFF);
        /// Cards, code blocks, sections
        pub const CONCRETE: crate::Rgba = crate::Rgba::new(0xF5, 0xF5, 0xF4, 0xFF);
        /// Dark backgrounds, text on light
        pub const DEEP_FORGE: crate::Rgba = crate::Rgba::new(0x36, 0x36, 0x3E, 0xFF);
        /// Darkest background, hero sections
        pub const NIGHT_BUILD: crate::Rgba = crate::Rgba::new(0x2A, 0x2A, 0x32, 0xFF);
        /// Alias voor amber — makkelijk voor apps die primary-naming gewend zijn
        pub const PRIMARY: crate::Rgba = crate::Rgba::new(0xD9, 0x77, 0x06, 0xFF);
        /// Alias voor signal-orange — DESIGN-SYSTEM.md §3.1 schrijft bg → signal-orange op hover
        pub const PRIMARY_HOVER: crate::Rgba = crate::Rgba::new(0xEA, 0x58, 0x0C, 0xFF);
        /// Secondary text, borders, subtle UI
        pub const SCAFFOLD_GRAY: crate::Rgba = crate::Rgba::new(0xA1, 0xA1, 0xAA, 0xFF);
        /// Hover states, CTAs, warnings
        pub const SIGNAL_ORANGE: crate::Rgba = crate::Rgba::new(0xEA, 0x58, 0x0C, 0xFF);
        /// Highlights, badges, secondary accents
        pub const WARM_GOLD: crate::Rgba = crate::Rgba::new(0xF5, 0x9E, 0x0B, 0xFF);
    }
    pub mod neutral {
        pub const N0: crate::Rgba = crate::Rgba::new(0xFF, 0xFF, 0xFF, 0xFF);
        /// Concrete
        pub const N100: crate::Rgba = crate::Rgba::new(0xF5, 0xF5, 0xF4, 0xFF);
        /// Default border (DESIGN-SYSTEM.md §2.6)
        pub const N200: crate::Rgba = crate::Rgba::new(0xE7, 0xE5, 0xE4, 0xFF);
        /// Hover border
        pub const N300: crate::Rgba = crate::Rgba::new(0xD6, 0xD3, 0xD1, 0xFF);
        /// Scaffold gray
        pub const N400: crate::Rgba = crate::Rgba::new(0xA1, 0xA1, 0xAA, 0xFF);
        /// Blueprint white
        pub const N50: crate::Rgba = crate::Rgba::new(0xFA, 0xFA, 0xF9, 0xFF);
        pub const N500: crate::Rgba = crate::Rgba::new(0x71, 0x71, 0x7A, 0xFF);
        /// Secondary text / table headings
        pub const N600: crate::Rgba = crate::Rgba::new(0x57, 0x53, 0x4E, 0xFF);
        pub const N700: crate::Rgba = crate::Rgba::new(0x3F, 0x3F, 0x46, 0xFF);
        /// Dark separator / dark button hover
        pub const N800: crate::Rgba = crate::Rgba::new(0x27, 0x27, 0x2A, 0xFF);
        /// Night build
        pub const N900: crate::Rgba = crate::Rgba::new(0x2A, 0x2A, 0x32, 0xFF);
        /// Deep forge
        pub const N950: crate::Rgba = crate::Rgba::new(0x36, 0x36, 0x3E, 0xFF);
    }
}
pub mod font {
    pub mod family {
        /// Body + UI
        pub const BODY: &str = "Inter";
        /// H1-H6 (DESIGN-SYSTEM.md §2.2)
        pub const HEADING: &str = "Space Grotesk";
        /// Code + section labels
        pub const MONO: &str = "JetBrains Mono";
    }
    pub mod letter_spacing {
        pub const NORMAL: f32 = 0.0;
        /// H4-H6 (Space Grotesk medium)
        pub const SNUG: f32 = -0.01;
        /// H1-H3 (Space Grotesk bold)
        pub const TIGHT: f32 = -0.02;
        /// Table headers uppercase
        pub const WIDE: f32 = 0.05;
        /// Section labels uppercase
        pub const WIDER: f32 = 0.1;
    }
    pub mod line_height {
        /// A4 report body
        pub const LOOSE: f32 = 1.7;
        /// Code / mono
        pub const NORMAL: f32 = 1.5;
        /// Body text
        pub const RELAXED: f32 = 1.6;
        /// Subheadings H4-H6
        pub const SNUG: f32 = 1.3;
        /// Headings H1-H3
        pub const TIGHT: f32 = 1.2;
    }
    pub mod size {
        /// 24px — H3
        pub const S2XL: f32 = 24.0;
        /// 32px — H2
        pub const S3XL: f32 = 32.0;
        /// 40px — H1
        pub const S4XL: f32 = 40.0;
        /// 16px — body default, H6
        pub const BASE: f32 = 16.0;
        /// 18px — H5
        pub const LG: f32 = 18.0;
        /// 14px — body small, code
        pub const SM: f32 = 14.0;
        /// 20px — H4
        pub const XL: f32 = 20.0;
        /// 12px — captions, section labels
        pub const XS: f32 = 12.0;
    }
    pub mod weight {
        /// H1-H3
        pub const BOLD: u16 = 700;
        /// H4-H6
        pub const MEDIUM: u16 = 500;
        pub const REGULAR: u16 = 400;
        /// UI / buttons / labels
        pub const SEMIBOLD: u16 = 600;
    }
}
pub mod radius {
    /// Pills, avatars
    pub const FULL: f32 = 9999.0;
    /// Modals, large cards
    pub const LG: f32 = 12.0;
    /// Cards, panels, buttons
    pub const MD: f32 = 8.0;
    pub const NONE: f32 = 0.0;
    /// Inputs, small buttons
    pub const SM: f32 = 4.0;
}
pub mod spacing {
    pub const S0: f32 = 0.0;
    /// 4px
    pub const S1: f32 = 4.0;
    /// 40px
    pub const S10: f32 = 40.0;
    /// 48px
    pub const S12: f32 = 48.0;
    /// 64px
    pub const S16: f32 = 64.0;
    /// 8px
    pub const S2: f32 = 8.0;
    /// 80px
    pub const S20: f32 = 80.0;
    /// 96px
    pub const S24: f32 = 96.0;
    /// 12px
    pub const S3: f32 = 12.0;
    /// 16px
    pub const S4: f32 = 16.0;
    /// 20px
    pub const S5: f32 = 20.0;
    /// 24px
    pub const S6: f32 = 24.0;
    /// 32px
    pub const S8: f32 = 32.0;
    /// MS Office stijl command ribbon hoogte
    pub const RIBBON_HEIGHT: f32 = 96.0;
    /// Hoofdnavigatie sidebar breedte (app layout). DESIGN-SYSTEM website-sidebar = 260px, apps gebruiken 280px.
    pub const SIDEBAR_WIDTH: f32 = 280.0;
    /// Topbar hoogte (desktop app)
    pub const TOPBAR_HEIGHT: f32 = 48.0;
}

/// Thema-afhankelijke kleuren (licht en donker).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Theme {
    pub border_default: crate::Rgba,
    pub border_focus: crate::Rgba,
    pub border_strong: crate::Rgba,
    pub semantic_danger: crate::Rgba,
    pub semantic_danger_bg: crate::Rgba,
    pub semantic_error: crate::Rgba,
    pub semantic_error_bg: crate::Rgba,
    pub semantic_info: crate::Rgba,
    pub semantic_info_bg: crate::Rgba,
    pub semantic_success: crate::Rgba,
    pub semantic_success_bg: crate::Rgba,
    pub semantic_warning: crate::Rgba,
    pub semantic_warning_bg: crate::Rgba,
    pub surface_bg: crate::Rgba,
    pub surface_elevated: crate::Rgba,
    pub surface_muted: crate::Rgba,
    pub surface_panel: crate::Rgba,
    pub text_inverse: crate::Rgba,
    pub text_muted: crate::Rgba,
    pub text_primary: crate::Rgba,
    pub text_secondary: crate::Rgba,
}

pub const LIGHT: Theme = Theme {
    border_default: crate::Rgba::new(0xE7, 0xE5, 0xE4, 0xFF),
    border_focus: crate::Rgba::new(0xD9, 0x77, 0x06, 0xFF),
    border_strong: crate::Rgba::new(0xD6, 0xD3, 0xD1, 0xFF),
    semantic_danger: crate::Rgba::new(0xDC, 0x26, 0x26, 0xFF),
    semantic_danger_bg: crate::Rgba::new(0xFE, 0xF2, 0xF2, 0xFF),
    semantic_error: crate::Rgba::new(0xDC, 0x26, 0x26, 0xFF),
    semantic_error_bg: crate::Rgba::new(0xFE, 0xF2, 0xF2, 0xFF),
    semantic_info: crate::Rgba::new(0x25, 0x63, 0xEB, 0xFF),
    semantic_info_bg: crate::Rgba::new(0xEF, 0xF6, 0xFF, 0xFF),
    semantic_success: crate::Rgba::new(0x16, 0xA3, 0x4A, 0xFF),
    semantic_success_bg: crate::Rgba::new(0xF0, 0xFD, 0xF4, 0xFF),
    semantic_warning: crate::Rgba::new(0xF5, 0x9E, 0x0B, 0xFF),
    semantic_warning_bg: crate::Rgba::new(0xFF, 0xFB, 0xEB, 0xFF),
    surface_bg: crate::Rgba::new(0xFA, 0xFA, 0xF9, 0xFF),
    surface_elevated: crate::Rgba::new(0xFF, 0xFF, 0xFF, 0xFF),
    surface_muted: crate::Rgba::new(0xF5, 0xF5, 0xF4, 0xFF),
    surface_panel: crate::Rgba::new(0xFF, 0xFF, 0xFF, 0xFF),
    text_inverse: crate::Rgba::new(0xFA, 0xFA, 0xF9, 0xFF),
    text_muted: crate::Rgba::new(0xA1, 0xA1, 0xAA, 0xFF),
    text_primary: crate::Rgba::new(0x36, 0x36, 0x3E, 0xFF),
    text_secondary: crate::Rgba::new(0x57, 0x53, 0x4E, 0xFF),
};

pub const DARK: Theme = Theme {
    border_default: crate::Rgba::new(0x27, 0x27, 0x2A, 0xFF),
    border_focus: crate::Rgba::new(0xF5, 0x9E, 0x0B, 0xFF),
    border_strong: crate::Rgba::new(0x3F, 0x3F, 0x46, 0xFF),
    semantic_danger: crate::Rgba::new(0xF8, 0x71, 0x71, 0xFF),
    semantic_danger_bg: crate::Rgba::new(0x7F, 0x1D, 0x1D, 0xFF),
    semantic_error: crate::Rgba::new(0xF8, 0x71, 0x71, 0xFF),
    semantic_error_bg: crate::Rgba::new(0x7F, 0x1D, 0x1D, 0xFF),
    semantic_info: crate::Rgba::new(0x60, 0xA5, 0xFA, 0xFF),
    semantic_info_bg: crate::Rgba::new(0x1E, 0x3A, 0x8A, 0xFF),
    semantic_success: crate::Rgba::new(0x4A, 0xDE, 0x80, 0xFF),
    semantic_success_bg: crate::Rgba::new(0x14, 0x53, 0x2D, 0xFF),
    semantic_warning: crate::Rgba::new(0xFB, 0xBF, 0x24, 0xFF),
    semantic_warning_bg: crate::Rgba::new(0x78, 0x35, 0x0F, 0xFF),
    surface_bg: crate::Rgba::new(0x36, 0x36, 0x3E, 0xFF),
    surface_elevated: crate::Rgba::new(0x3F, 0x3F, 0x46, 0xFF),
    surface_muted: crate::Rgba::new(0x27, 0x27, 0x2A, 0xFF),
    surface_panel: crate::Rgba::new(0x2A, 0x2A, 0x32, 0xFF),
    text_inverse: crate::Rgba::new(0x36, 0x36, 0x3E, 0xFF),
    text_muted: crate::Rgba::new(0xA1, 0xA1, 0xAA, 0xFF),
    text_primary: crate::Rgba::new(0xFA, 0xFA, 0xF9, 0xFF),
    text_secondary: crate::Rgba::new(0xD6, 0xD3, 0xD1, 0xFF),
};
