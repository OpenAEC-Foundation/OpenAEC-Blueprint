//! Shared vertical application frame; tools provide their domain content.
use crate::{model::metrics, Theme};
use iced::{widget::{column, container, Column, Space}, Alignment, Color, Element, Fill};

/// Tauri Style Book document band: 30 px, one-pixel rules and 4 px inset.
/// The caller owns document identity, content and activation behavior.
pub fn document_bar<'a, M: 'a>(theme: Theme, content: Element<'a, M>) -> Element<'a, M> {
    let tokens = theme.tokens();
    let blend = |overlay: Color| Color {
        r: tokens.docbar_bg.r * (1.0 - overlay.a) + overlay.r * overlay.a,
        g: tokens.docbar_bg.g * (1.0 - overlay.a) + overlay.g * overlay.a,
        b: tokens.docbar_bg.b * (1.0 - overlay.a) + overlay.b * overlay.a,
        a: 1.0,
    };
    let top = blend(Color::from_rgba8(217, 119, 6, 0.15));
    let bottom = blend(tokens.border);
    column![
        container(Space::new(Fill, 1))
            .width(Fill)
            .style(move |_| container::Style::default().background(top)),
        container(content)
            .width(Fill)
            .height(metrics::DOCUMENTS - 2)
            .padding([0, 4])
            .align_y(Alignment::End)
            .style(move |_| container::Style::default().background(tokens.docbar_bg)),
        container(Space::new(Fill, 1))
            .width(Fill)
            .style(move |_| container::Style::default().background(bottom)),
    ]
    .width(Fill)
    .height(metrics::DOCUMENTS)
    .into()
}

/// Common 22 px status band with a one-pixel top rule. Applications supply
/// their own status content while the crate owns its geometry and palette.
pub fn status_bar<'a, M: 'a>(
    theme: Theme,
    content: Element<'a, M>,
    horizontal_padding: u16,
) -> Element<'a, M> {
    let tokens = theme.tokens();
    column![
        container(Space::new(Fill, 1))
            .width(Fill)
            .style(move |_| container::Style::default().background(tokens.status_border)),
        container(content)
            .padding([0, horizontal_padding])
            .width(Fill)
            .height(metrics::STATUS - 1)
            .style(move |_| {
                container::Style::default()
                    .background(tokens.status_bg)
                    .color(tokens.status_text)
            }),
    ]
    .width(Fill)
    .height(metrics::STATUS)
    .into()
}

pub struct FrameSlots<'a, M> {
    pub titlebar: Element<'a, M>,
    pub tabs: Element<'a, M>,
    pub ribbon: Option<Element<'a, M>>,
    pub documents: Option<Element<'a, M>>,
    pub content: Element<'a, M>,
    pub status: Element<'a, M>,
}

pub fn frame<'a, M: 'a>(slots: FrameSlots<'a, M>) -> Element<'a, M> {
    let mut bands = Column::new()
        .push(container(slots.titlebar).height(metrics::TITLE).width(Fill))
        .push(container(slots.tabs).height(metrics::TABS).width(Fill));
    if let Some(ribbon) = slots.ribbon {
        bands = bands.push(container(ribbon).height(metrics::RIBBON).width(Fill));
    }
    if let Some(documents) = slots.documents {
        bands = bands.push(container(documents).height(metrics::DOCUMENTS).width(Fill));
    }
    bands
        .push(container(slots.content).height(Fill).width(Fill))
        .push(container(slots.status).height(metrics::STATUS).width(Fill))
        .height(Fill)
        .width(Fill)
        .into()
}

/// Compact outer frame for step-by-step applications such as Energy Studio.
/// The title, document and status bands keep their shared dimensions.
pub fn workflow_frame<'a, M: 'a>(
    titlebar: Element<'a, M>,
    documents: Option<Element<'a, M>>,
    content: Element<'a, M>,
    status: Element<'a, M>,
) -> Element<'a, M> {
    let mut bands = Column::new()
        .push(container(titlebar).height(metrics::TITLE).width(Fill));
    if let Some(documents) = documents {
        bands = bands.push(container(documents).height(metrics::DOCUMENTS).width(Fill));
    }
    bands
        .push(container(content).height(Fill).width(Fill))
        .push(container(status).height(metrics::STATUS).width(Fill))
        .height(Fill)
        .width(Fill)
        .into()
}
