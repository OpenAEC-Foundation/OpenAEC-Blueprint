//! Keyboard focus for every control (issue #2).
//!
//! iced 0.14 only lets text fields take focus. [`focusable`] gives any control a
//! place in the Tab route: Enter and Space then send it the same press and release
//! as a mouse click, so buttons, tiles, checkboxes and pick lists work without
//! knowing about the keyboard. The focus ring only shows when the focus came from
//! the keyboard, like `:focus-visible` on the web.
//!
//! [`inert`] takes everything behind an open dialog or menu out of the Tab route and
//! out of the key handling. The control that had the focus keeps it, so closing the
//! dialog returns the focus there without remembering anything.
//!
//! Tab and Shift+Tab come from [`crate::keyboard::navigation`].
use iced::advanced::layout::{self, Layout};
use iced::advanced::renderer::{self, Renderer as _};
use iced::advanced::widget::operation::{Focusable, Operation};
use iced::advanced::widget::tree::{self, Tree};
use iced::advanced::{overlay, Clipboard, Shell, Widget};
use iced::keyboard::{self, key::Named, Key};
use iced::{mouse, Background, Border, Color, Element, Event, Length, Rectangle, Renderer, Size, Theme, Vector};

use super::Look;

thread_local! {
    /// Set while an inert screen draws: the control that keeps the focus behind
    /// an open dialog shows no ring, so only the dialog's focus is visible.
    static BEHIND_DIALOG: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}

/// The focus state of one control.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct State {
    focused: bool,
    /// Whether the ring shows: the focus came from the keyboard, not a click.
    visible: bool,
}

impl Focusable for State {
    fn is_focused(&self) -> bool {
        self.focused
    }
    fn focus(&mut self) {
        // Only focus operations (Tab, Shift+Tab, `focus(id)`) call this.
        self.focused = true;
        self.visible = true;
    }
    fn unfocus(&mut self) {
        self.focused = false;
        self.visible = false;
    }
}

/// Puts `content` in the Tab route. `enabled: false` leaves it out, as for a
/// disabled button. `radius` is the corner of the focus ring, the same as the
/// control's own corner.
pub fn focusable<'a, M: 'a>(look: Look, content: impl Into<Element<'a, M>>, enabled: bool, radius: f32) -> Element<'a, M> {
    let content = content.into();
    if !enabled {
        return content;
    }
    Element::new(Focus { content, ring: look.color.focus, radius, id: None })
}

/// Like [`focusable`], with an id so `iced::widget::operation::focus(id)` can move
/// the focus here, for example to the first field of a form.
pub fn focusable_with_id<'a, M: 'a>(look: Look, content: impl Into<Element<'a, M>>, id: iced::widget::Id, radius: f32) -> Element<'a, M> {
    Element::new(Focus { content: content.into(), ring: look.color.focus, radius, id: Some(id) })
}

struct Focus<'a, M> {
    content: Element<'a, M>,
    ring: Color,
    radius: f32,
    id: Option<iced::widget::Id>,
}

/// The press and release of a mouse click, as Enter and Space send them.
fn click_events() -> [Event; 2] {
    [
        Event::Mouse(mouse::Event::ButtonPressed(mouse::Button::Left)),
        Event::Mouse(mouse::Event::ButtonReleased(mouse::Button::Left)),
    ]
}

/// Moves the focus to the next control of the Tab route, wrapping from the last
/// to the first. iced's own `focus_next` passes through "no focus" at the end.
pub fn next<T: Send + 'static>() -> impl Operation<T> {
    iced::advanced::widget::operation::then(iced::advanced::widget::operation::focusable::count(), |count| Step { target: step_target(count, true), current: 0 })
}

/// Moves the focus to the previous control, wrapping from the first to the last.
pub fn previous<T: Send + 'static>() -> impl Operation<T> {
    iced::advanced::widget::operation::then(iced::advanced::widget::operation::focusable::count(), |count| Step { target: step_target(count, false), current: 0 })
}

fn step_target(count: iced::advanced::widget::operation::focusable::Count, forward: bool) -> Option<usize> {
    let total = count.total;
    if total == 0 {
        return None;
    }
    Some(match (count.focused, forward) {
        (None, true) => 0,
        (None, false) => total - 1,
        (Some(i), true) => (i + 1) % total,
        (Some(i), false) => (i + total - 1) % total,
    })
}

struct Step {
    target: Option<usize>,
    current: usize,
}

impl<T> Operation<T> for Step {
    fn traverse(&mut self, operate: &mut dyn FnMut(&mut dyn Operation<T>)) {
        operate(self);
    }
    fn focusable(&mut self, _id: Option<&iced::widget::Id>, _bounds: Rectangle, state: &mut dyn Focusable) {
        if Some(self.current) == self.target {
            state.focus();
        } else {
            state.unfocus();
        }
        self.current += 1;
    }
}

impl<M> Widget<M, Theme, Renderer> for Focus<'_, M> {
    fn tag(&self) -> tree::Tag {
        tree::Tag::of::<State>()
    }
    fn state(&self) -> tree::State {
        tree::State::new(State::default())
    }
    fn children(&self) -> Vec<Tree> {
        vec![Tree::new(&self.content)]
    }
    fn diff(&self, tree: &mut Tree) {
        tree.diff_children(std::slice::from_ref(&self.content));
    }
    fn size(&self) -> Size<Length> {
        self.content.as_widget().size()
    }
    fn size_hint(&self) -> Size<Length> {
        self.content.as_widget().size_hint()
    }
    fn layout(&mut self, tree: &mut Tree, renderer: &Renderer, limits: &layout::Limits) -> layout::Node {
        self.content.as_widget_mut().layout(&mut tree.children[0], renderer, limits)
    }

    fn operate(&mut self, tree: &mut Tree, layout: Layout<'_>, renderer: &Renderer, operation: &mut dyn Operation) {
        operation.focusable(self.id.as_ref(), layout.bounds(), tree.state.downcast_mut::<State>());
        operation.traverse(&mut |operation| {
            self.content.as_widget_mut().operate(&mut tree.children[0], layout, renderer, operation);
        });
    }

    fn update(
        &mut self,
        tree: &mut Tree,
        event: &Event,
        layout: Layout<'_>,
        cursor: mouse::Cursor,
        renderer: &Renderer,
        clipboard: &mut dyn Clipboard,
        shell: &mut Shell<'_, M>,
        viewport: &Rectangle,
    ) {
        let bounds = layout.bounds();
        let state = *tree.state.downcast_ref::<State>();
        match event {
            Event::Keyboard(keyboard::Event::KeyPressed { key: Key::Named(Named::Enter | Named::Space), repeat: false, modifiers, .. })
                if state.focused && !modifiers.command() && !modifiers.alt() =>
            {
                // The same press and release a mouse click in the middle would give.
                // Each half gets its own shell: a button ignores the release once
                // the press counts as captured in the same shell.
                let centre = mouse::Cursor::Available(bounds.center());
                for click in click_events() {
                    let mut messages = Vec::new();
                    let mut own = Shell::new(&mut messages);
                    self.content.as_widget_mut().update(&mut tree.children[0], &click, layout, centre, renderer, clipboard, &mut own, viewport);
                    shell.merge(own, |message| message);
                }
                shell.capture_event();
                shell.request_redraw();
                return;
            }
            Event::Mouse(mouse::Event::ButtonPressed(_)) | Event::Touch(iced::touch::Event::FingerPressed { .. }) => {
                // A click moves the focus here without showing the ring, and away elsewhere.
                let own = tree.state.downcast_mut::<State>();
                let inside = cursor.is_over(bounds);
                if own.focused != inside || own.visible {
                    *own = State { focused: inside, visible: false };
                    shell.request_redraw();
                }
            }
            _ => {}
        }
        self.content.as_widget_mut().update(&mut tree.children[0], event, layout, cursor, renderer, clipboard, shell, viewport);
    }

    fn mouse_interaction(&self, tree: &Tree, layout: Layout<'_>, cursor: mouse::Cursor, viewport: &Rectangle, renderer: &Renderer) -> mouse::Interaction {
        self.content.as_widget().mouse_interaction(&tree.children[0], layout, cursor, viewport, renderer)
    }

    fn draw(&self, tree: &Tree, renderer: &mut Renderer, theme: &Theme, style: &renderer::Style, layout: Layout<'_>, cursor: mouse::Cursor, viewport: &Rectangle) {
        self.content.as_widget().draw(&tree.children[0], renderer, theme, style, layout, cursor, viewport);
        let state = tree.state.downcast_ref::<State>();
        if state.focused && state.visible && !BEHIND_DIALOG.with(|b| b.get()) {
            // A 2 px ring inside the control: iced cannot draw outside it (see widgets.rs).
            renderer.fill_quad(
                renderer::Quad { bounds: layout.bounds(), border: Border { color: self.ring, width: 2.0, radius: self.radius.into() }, ..Default::default() },
                Background::Color(Color::TRANSPARENT),
            );
        }
    }

    fn overlay<'b>(&'b mut self, tree: &'b mut Tree, layout: Layout<'b>, renderer: &Renderer, viewport: &Rectangle, translation: Vector) -> Option<overlay::Element<'b, M, Theme, Renderer>> {
        self.content.as_widget_mut().overlay(&mut tree.children[0], layout, renderer, viewport, translation)
    }
}

/// Takes `content` out of the Tab route and the key handling while `inert` is
/// true, for the screen behind an open dialog or menu. Its focus stays where it
/// was, so it comes back when the dialog closes.
pub fn inert<'a, M: 'a>(content: impl Into<Element<'a, M>>, inert: bool) -> Element<'a, M> {
    Element::new(Inert { content: content.into(), inert })
}

struct Inert<'a, M> {
    content: Element<'a, M>,
    inert: bool,
}

impl<M> Widget<M, Theme, Renderer> for Inert<'_, M> {
    fn children(&self) -> Vec<Tree> {
        vec![Tree::new(&self.content)]
    }
    fn diff(&self, tree: &mut Tree) {
        tree.diff_children(std::slice::from_ref(&self.content));
    }
    fn size(&self) -> Size<Length> {
        self.content.as_widget().size()
    }
    fn size_hint(&self) -> Size<Length> {
        self.content.as_widget().size_hint()
    }
    fn layout(&mut self, tree: &mut Tree, renderer: &Renderer, limits: &layout::Limits) -> layout::Node {
        self.content.as_widget_mut().layout(&mut tree.children[0], renderer, limits)
    }
    fn operate(&mut self, tree: &mut Tree, layout: Layout<'_>, renderer: &Renderer, operation: &mut dyn Operation) {
        if !self.inert {
            self.content.as_widget_mut().operate(&mut tree.children[0], layout, renderer, operation);
        }
    }
    fn update(
        &mut self,
        tree: &mut Tree,
        event: &Event,
        layout: Layout<'_>,
        cursor: mouse::Cursor,
        renderer: &Renderer,
        clipboard: &mut dyn Clipboard,
        shell: &mut Shell<'_, M>,
        viewport: &Rectangle,
    ) {
        // Keys and clicks belong to the dialog; window events still pass.
        if self.inert && matches!(event, Event::Keyboard(_) | Event::Mouse(_) | Event::Touch(_)) {
            return;
        }
        self.content.as_widget_mut().update(&mut tree.children[0], event, layout, cursor, renderer, clipboard, shell, viewport);
    }
    fn mouse_interaction(&self, tree: &Tree, layout: Layout<'_>, cursor: mouse::Cursor, viewport: &Rectangle, renderer: &Renderer) -> mouse::Interaction {
        if self.inert {
            return mouse::Interaction::None;
        }
        self.content.as_widget().mouse_interaction(&tree.children[0], layout, cursor, viewport, renderer)
    }
    fn draw(&self, tree: &Tree, renderer: &mut Renderer, theme: &Theme, style: &renderer::Style, layout: Layout<'_>, cursor: mouse::Cursor, viewport: &Rectangle) {
        let cursor = if self.inert { mouse::Cursor::Unavailable } else { cursor };
        let outer = BEHIND_DIALOG.with(|b| b.replace(b.get() || self.inert));
        self.content.as_widget().draw(&tree.children[0], renderer, theme, style, layout, cursor, viewport);
        BEHIND_DIALOG.with(|b| b.set(outer));
    }
    fn overlay<'b>(&'b mut self, tree: &'b mut Tree, layout: Layout<'b>, renderer: &Renderer, viewport: &Rectangle, translation: Vector) -> Option<overlay::Element<'b, M, Theme, Renderer>> {
        if self.inert {
            return None;
        }
        self.content.as_widget_mut().overlay(&mut tree.children[0], layout, renderer, viewport, translation)
    }
}

#[cfg(test)]
#[path = "focus_tests.rs"]
mod tests;
