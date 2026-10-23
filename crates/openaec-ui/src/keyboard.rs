//! Shortcuts outside text fields.
//!
//! iced 0.14 removed `keyboard::on_key_press`; this keeps the same contract on
//! top of `keyboard::listen`: only key presses that no widget captured arrive.
use iced::keyboard::{Event, Key, Modifiers};
use iced::Subscription;

/// Key presses that no widget captured, mapped by `f`. Like every iced
/// subscription mapper, `f` must be a non-capturing closure or a function.
pub fn on_key_press<M, F>(f: F) -> Subscription<M>
where
    M: Send + 'static,
    F: Fn(Key, Modifiers) -> Option<M> + Send + Clone + 'static,
{
    iced::keyboard::listen().filter_map(move |event| match event {
        Event::KeyPressed { key, modifiers, .. } => f(key, modifiers),
        _ => None,
    })
}
