//! Canonical controls for domain panels. Use these instead of restyling buttons per app.
use crate::{
    fonts,
    icons::Icon,
    model::{metrics, CommandIcon},
    Theme,
};
use iced::{
    widget::{
        button, checkbox, column, container, pick_list, progress_bar, row, scrollable, slider,
        text, text_input, tooltip,
    },
    Background, Border, Element, Fill,
};

pub fn slider_style(theme: Theme, status: slider::Status) -> slider::Style {
    let t = theme.tokens();
    slider::Style {
        rail: slider::Rail {
            backgrounds: (t.accent.into(), theme.border_strong().into()),
            width: 4.0,
            border: Border::default().rounded(2),
        },
        handle: slider::Handle {
            shape: slider::HandleShape::Circle { radius: 7.0 },
            background: if status == slider::Status::Dragged {
                t.accent
            } else {
                t.bg_lighter
            }
            .into(),
            border_width: 2.0,
            border_color: if status == slider::Status::Hovered {
                t.accent_hover
            } else {
                t.accent
            },
        },
    }
}

pub fn progress_style(theme: Theme) -> progress_bar::Style {
    progress_bar::Style {
        background: theme.border_strong().into(),
        bar: theme.tokens().accent.into(),
        border: Border::default().rounded(4),
    }
}

pub fn progress_line_style(theme: Theme) -> progress_bar::Style {
    progress_bar::Style {
        border: Border::default().rounded(1),
        ..progress_style(theme)
    }
}

pub fn checkbox_style(theme: Theme, status: checkbox::Status) -> checkbox::Style {
    let t = theme.tokens();
    let (checked, hovered, disabled) = match status {
        checkbox::Status::Active { is_checked } => (is_checked, false, false),
        checkbox::Status::Hovered { is_checked } => (is_checked, true, false),
        checkbox::Status::Disabled { is_checked } => (is_checked, false, true),
    };
    let (background, border) = if checked {
        (t.accent, t.accent)
    } else if hovered {
        (t.dialog_input_bg, t.dialog_content_secondary)
    } else {
        (t.dialog_input_bg, t.dialog_input_border)
    };
    let opacity = if disabled { 0.5 } else { 1.0 };
    checkbox::Style {
        background: background.scale_alpha(opacity).into(),
        icon_color: t.btn_primary_text,
        border: Border {
            color: border.scale_alpha(opacity),
            width: 1.0,
            radius: 2.0.into(),
        },
        text_color: Some(t.text.scale_alpha(opacity)),
    }
}

pub fn scrollable_style(theme: Theme, status: scrollable::Status) -> scrollable::Style {
    let t = theme.tokens();
    let (horizontal, vertical) = match status {
        scrollable::Status::Active => (false, false),
        scrollable::Status::Hovered {
            is_horizontal_scrollbar_hovered,
            is_vertical_scrollbar_hovered,
        } => (
            is_horizontal_scrollbar_hovered,
            is_vertical_scrollbar_hovered,
        ),
        scrollable::Status::Dragged {
            is_horizontal_scrollbar_dragged,
            is_vertical_scrollbar_dragged,
        } => (
            is_horizontal_scrollbar_dragged,
            is_vertical_scrollbar_dragged,
        ),
    };
    let rail = |strong: bool| scrollable::Rail {
        background: None,
        border: Border::default(),
        scroller: scrollable::Scroller {
            color: t.accent.scale_alpha(if strong { 0.40 } else { 0.25 }),
            border: Border::default().rounded(3),
        },
    };
    scrollable::Style {
        container: container::Style::default(),
        vertical_rail: rail(vertical),
        horizontal_rail: rail(horizontal),
        gap: None,
    }
}

pub fn tooltip_style(_theme: Theme) -> container::Style {
    container::Style::default()
        .background(iced::Color::from_rgb8(0x36, 0x36, 0x3E))
        .color(iced::Color::from_rgb8(0xFA, 0xFA, 0xF9))
        .border(Border::default().rounded(4))
}

/// Square text field shared by panel forms and dialogs.
pub fn text_input_style(theme: Theme, status: text_input::Status) -> text_input::Style {
    let t = theme.tokens();
    let mut style = text_input::Style {
        background: t.dialog_input_bg.into(),
        border: Border {
            color: if status == text_input::Status::Focused {
                t.focus_color
            } else {
                t.dialog_input_border
            },
            width: 1.0,
            radius: 0.0.into(),
        },
        icon: t.text_muted,
        placeholder: t.text_faint,
        value: t.dialog_input_text,
        selection: t.accent_soft,
    };
    if status == text_input::Status::Disabled {
        style.background = style.background.scale_alpha(0.5);
        style.border.color = style.border.color.scale_alpha(0.5);
        style.value = style.value.scale_alpha(0.5);
    }
    style
}

/// Choice field and its popup use the same tokens as text fields.
pub fn pick_list_style(theme: Theme, status: pick_list::Status) -> pick_list::Style {
    let t = theme.tokens();
    pick_list::Style {
        text_color: t.dialog_input_text,
        placeholder_color: t.text_faint,
        handle_color: t.dialog_input_text.scale_alpha(0.6),
        background: t.dialog_input_bg.into(),
        border: Border {
            color: match status {
                pick_list::Status::Active => t.dialog_input_border,
                pick_list::Status::Hovered => t.dialog_content_secondary,
                pick_list::Status::Opened => t.focus_color,
            },
            width: 1.0,
            radius: 0.0.into(),
        },
    }
}

pub fn pick_list_menu_style(theme: Theme) -> iced::overlay::menu::Style {
    let t = theme.tokens();
    iced::overlay::menu::Style {
        background: Background::Color(t.bg),
        border: Border {
            color: t.dialog_input_border,
            width: 1.0,
            radius: 0.0.into(),
        },
        text_color: t.dialog_input_text,
        selected_text_color: t.accent,
        selected_background: Background::Color(t.ribbon_btn_hover),
    }
}

/// Filled confirmation button used by dialogs and forms in every studio.
pub fn primary_button_style(theme: Theme, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    let style = button::Style {
        background: Some(
            if hovered {
                t.btn_primary_hover_bg
            } else {
                t.btn_primary_bg
            }
            .into(),
        ),
        text_color: if hovered {
            t.btn_primary_hover_text
        } else {
            t.btn_primary_text
        },
        border: Border {
            color: t.btn_primary_border,
            width: 1.0,
            radius: 2.0.into(),
        },
        ..Default::default()
    };
    if status == button::Status::Disabled {
        faded_button(style, 0.5)
    } else {
        style
    }
}

/// Neutral companion button used by dialogs and forms in every studio.
pub fn secondary_button_style(theme: Theme, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    let style = button::Style {
        background: Some(
            if hovered {
                t.btn_secondary_hover_bg
            } else {
                t.btn_secondary_bg
            }
            .into(),
        ),
        text_color: t.btn_secondary_text,
        border: Border {
            color: if hovered {
                t.btn_secondary_hover_border
            } else {
                t.dialog_input_border
            },
            width: 1.0,
            radius: 2.0.into(),
        },
        ..Default::default()
    };
    if status == button::Status::Disabled {
        faded_button(style, 0.5)
    } else {
        style
    }
}

/// Text link used for source references and secondary navigation.
pub fn link_button_style(theme: Theme, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    let style = button::Style {
        text_color: if hovered { t.accent_hover } else { t.accent },
        ..Default::default()
    };
    if status == button::Status::Disabled {
        faded_button(style, 0.5)
    } else {
        style
    }
}

/// Flat action on the common status bar.
pub fn status_button_style(theme: Theme, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    button::Style {
        background: hovered.then_some(t.status_hover.into()),
        text_color: if status == button::Status::Disabled {
            t.status_text_label
        } else {
            t.status_text
        },
        ..Default::default()
    }
}

/// Shared dialog-button geometry: 11 px text, a 27 px line and a 75 px
/// minimum width. The caller supplies its theme adapter to the style hook.
pub fn dialog_button<'a, M: 'a>(
    label: impl text::IntoFragment<'a>,
    style: impl Fn(&iced::Theme, button::Status) -> button::Style + 'a,
) -> button::Button<'a, M> {
    const PADDING: [u16; 2] = [5, 20];
    const MIN_WIDTH: f32 = 75.0;
    const LINE_HEIGHT: f32 = 17.0;
    button(
        column![
            text(label)
                .size(11)
                .font(fonts::BODY)
                .line_height(text::LineHeight::Absolute(LINE_HEIGHT.into())),
            iced::widget::Space::with_width(MIN_WIDTH - 2.0 * f32::from(PADDING[1])),
        ]
        .align_x(iced::Alignment::Center),
    )
    .padding(PADDING)
    .style(style)
}

fn faded_button(style: button::Style, alpha: f32) -> button::Style {
    button::Style {
        background: style.background.map(|color| color.scale_alpha(alpha)),
        text_color: style.text_color.scale_alpha(alpha),
        border: Border {
            color: style.border.color.scale_alpha(alpha),
            ..style.border
        },
        ..style
    }
}

pub fn button_style(theme: Theme, selected: bool, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let disabled = matches!(status, button::Status::Disabled);
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    button::Style {
        background: Some(
            if selected {
                t.ribbon_btn_active_bg
            } else if hovered {
                t.ribbon_btn_hover
            } else {
                t.bg
            }
            .into(),
        ),
        text_color: if disabled {
            t.text_faint
        } else if selected {
            t.ribbon_btn_active_text
        } else {
            t.text
        },
        border: Border {
            color: if selected {
                t.ribbon_btn_active_border
            } else if hovered {
                t.ribbon_btn_hover_border
            } else {
                iced::Color::TRANSPARENT
            },
            width: 1.0,
            radius: 4.0.into(),
        },
        ..Default::default()
    }
}
/// Canonical ribbon control colors, including hover, selection, and disabled contrast.
pub fn ribbon_button_style(theme: Theme, selected: bool, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    let (background, text_color, border) = if selected {
        (
            Some(t.ribbon_btn_active_bg),
            t.ribbon_btn_active_text,
            t.ribbon_btn_active_border,
        )
    } else if hovered {
        (
            Some(t.ribbon_btn_hover),
            t.ribbon_text_hover,
            t.ribbon_btn_hover_border,
        )
    } else {
        (None, t.text, iced::Color::TRANSPARENT)
    };
    let style = button::Style {
        background: background.map(Into::into),
        text_color,
        border: Border {
            color: border,
            width: 1.0,
            radius: 2.0.into(),
        },
        ..Default::default()
    };
    if status == button::Status::Disabled {
        button::Style {
            background: style.background.map(|color| color.scale_alpha(0.72)),
            text_color: style.text_color.scale_alpha(0.72),
            border: Border {
                color: style.border.color.scale_alpha(0.72),
                ..style.border
            },
            ..style
        }
    } else {
        style
    }
}

/// Flat 28 px ribbon-tab strip, shared by the showcase and desktop tools.
/// The active tab takes the work-surface colour; hover uses the theme's
/// ribbon hover token. Geometry belongs to the caller's tab button.
pub fn ribbon_tab_style(theme: Theme, active: bool, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let hovered = matches!(status, button::Status::Hovered);
    button::Style {
        background: if active {
            Some(t.bg.into())
        } else if hovered {
            Some(t.ribbon_btn_hover.into())
        } else {
            None
        },
        text_color: if active || hovered { t.accent } else { t.text },
        ..Default::default()
    }
}
pub fn surface(theme: Theme) -> container::Style {
    let t = theme.tokens();
    container::Style::default().background(t.bg).color(t.text)
}
pub fn panel_header<'a, M: 'a>(title: impl Into<String>, theme: Theme) -> Element<'a, M> {
    let t = theme.tokens();
    let title = container(
        text(title.into().to_uppercase())
            .font(fonts::STRONG)
            .size(11),
    )
    .padding([0, 6])
    .height(metrics::PANEL_TOOLBAR - 1)
    .width(Fill)
    .align_y(iced::Alignment::Center)
    .style(move |_| {
        container::Style::default()
            .background(t.bg_lighter)
            .color(t.accent)
    });
    let divider = container(iced::widget::Space::new(Fill, 1))
        .height(1)
        .width(Fill)
        .style(move |_| container::Style::default().background(t.border));
    column![title, divider]
        .height(metrics::PANEL_TOOLBAR)
        .width(Fill)
        .into()
}
pub fn panel<'a, M: 'a>(
    title: impl Into<String>,
    content: Element<'a, M>,
    theme: Theme,
) -> Element<'a, M> {
    container(column![
        panel_header(title, theme),
        iced::widget::scrollable(container(content).padding(12).width(Fill))
            .height(Fill)
            .style(move |_, status| scrollable_style(theme, status)),
    ])
    .width(Fill)
    .height(Fill)
    .style(move |_| surface(theme))
    .into()
}
pub fn action<'a, M: Clone + 'a>(
    label: impl Into<String>,
    icon: impl Into<CommandIcon>,
    message: Option<M>,
    theme: Theme,
) -> Element<'a, M> {
    let icon = icon.into();
    let color = if message.is_some() {
        theme.tokens().text
    } else {
        theme.tokens().text_faint
    };
    button(
        row![
            icon.view(metrics::ICON, color),
            text(label.into()).font(fonts::BODY).size(13)
        ]
        .spacing(8)
        .align_y(iced::Alignment::Center),
    )
    .padding([5, 10])
    .height(metrics::CONTROL)
    .on_press_maybe(message)
    .style(move |_, status| button_style(theme, false, status))
    .into()
}
pub fn icon_button<'a, M: Clone + 'a>(
    label: &'a str,
    icon: Icon,
    message: M,
    theme: Theme,
) -> Element<'a, M> {
    tooltip(
        button(icon.view(16, theme.tokens().text))
            .padding(7)
            .on_press(message)
            .style(move |_, s| button_style(theme, false, s)),
        container(text(label).size(12))
            .padding([8, 12])
            .max_width(340)
            .style(move |_| tooltip_style(theme)),
        tooltip::Position::Bottom,
    )
    .into()
}
pub fn status_icon_button<'a, M: Clone + 'a>(
    label: &'a str,
    icon: Icon,
    message: M,
    theme: Theme,
) -> Element<'a, M> {
    let t = theme.tokens();
    tooltip(
        button(icon.view(14, t.status_text))
            .padding([3, 7])
            .on_press(message)
            .style(move |_, status| status_button_style(theme, status)),
        text(label).size(12),
        tooltip::Position::Top,
    )
    .into()
}
pub fn empty_state<'a, M: 'a>(
    title: impl Into<String>,
    description: impl Into<String>,
    theme: Theme,
) -> Element<'a, M> {
    container(
        column![
            Icon::Cube.view(48, theme.tokens().accent),
            text(title.into()).font(fonts::HEADING).size(28),
            text(description.into()).font(fonts::BODY).size(14)
        ]
        .spacing(16)
        .align_x(iced::Alignment::Center),
    )
    .center(Fill)
    .into()
}
pub fn property<'a, M: 'a>(
    label: impl Into<String>,
    value: impl Into<String>,
    theme: Theme,
) -> Element<'a, M> {
    row![
        text(label.into())
            .size(12)
            .color(theme.tokens().text_secondary)
            .width(Fill),
        text(value.into()).size(12).font(fonts::MEDIUM)
    ]
    .spacing(12)
    .into()
}
