//! Canonical controls for domain panels. Use these instead of restyling buttons per app.
use crate::{fonts, icons::Icon, model::metrics, Theme};
use iced::{widget::{button, column, container, row, text, tooltip}, Border, Element, Fill};

pub fn button_style(theme: Theme, selected: bool, status: button::Status) -> button::Style {
    let t = theme.tokens();
    let disabled = matches!(status, button::Status::Disabled);
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    button::Style {
        background: Some(if selected { t.ribbon_btn_active_bg } else if hovered { t.ribbon_btn_hover } else { t.bg }.into()),
        text_color: if disabled { t.text_faint } else if selected { t.ribbon_btn_active_text } else { t.text },
        border: Border { color: if selected { t.ribbon_btn_active_border } else if hovered { t.ribbon_btn_hover_border } else { iced::Color::TRANSPARENT }, width: 1.0, radius: 4.0.into() },
        ..Default::default()
    }
}
pub fn surface(theme: Theme) -> container::Style {
    let t = theme.tokens(); container::Style::default().background(t.bg).color(t.text)
}
pub fn panel<'a,M:'a>(title: impl Into<String>, content: Element<'a,M>, theme: Theme) -> Element<'a,M> {
    let t = theme.tokens();
    container(column![
        container(text(title.into()).font(fonts::STRONG).size(12)).padding(10).width(Fill).style(move |_| container::Style::default().background(t.bg_lighter).color(t.text)),
        iced::widget::scrollable(container(content).padding(12).width(Fill)).height(Fill),
    ]).width(Fill).height(Fill).style(move |_| surface(theme)).into()
}
pub fn action<'a, M: Clone + 'a>(label: impl Into<String>, icon: Icon, message: Option<M>, theme: Theme) -> Element<'a,M> {
    let color = if message.is_some() { theme.tokens().text } else { theme.tokens().text_faint };
    button(row![icon.view(metrics::ICON,color), text(label.into()).font(fonts::BODY).size(13)].spacing(8).align_y(iced::Alignment::Center))
        .padding([5,10]).height(metrics::CONTROL).on_press_maybe(message)
        .style(move |_, status| button_style(theme,false,status)).into()
}
pub fn icon_button<'a, M: Clone + 'a>(label: &'a str, icon: Icon, message:M, theme:Theme) -> Element<'a,M> {
    tooltip(button(icon.view(16,theme.tokens().text)).padding(7).on_press(message).style(move |_,s|button_style(theme,false,s)), text(label).size(12), tooltip::Position::Bottom).into()
}
pub fn empty_state<'a, M:'a>(title: impl Into<String>, description: impl Into<String>, theme: Theme) -> Element<'a,M> {
    container(column![Icon::Cube.view(48,theme.tokens().accent),text(title.into()).font(fonts::HEADING).size(28),text(description.into()).font(fonts::BODY).size(14)].spacing(16).align_x(iced::Alignment::Center)).center(Fill).into()
}
pub fn property<'a,M:'a>(label:impl Into<String>, value:impl Into<String>, theme:Theme)->Element<'a,M> {
    row![text(label.into()).size(12).color(theme.tokens().text_secondary).width(Fill),text(value.into()).size(12).font(fonts::MEDIUM)].spacing(12).into()
}
