//! Shared vertical application frame; tools provide their domain content.
use crate::model::metrics;
use iced::{widget::{container, Column}, Element, Fill};

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
