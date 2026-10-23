//! Tests of the keyboard focus in `focus.rs`: the Tab route, Enter and Space, a
//! dialog that keeps the focus, and a click that gives focus without the ring.
use super::*;
use crate::design::widgets::{button, ButtonKind, Density};
use crate::design::{StatusbarSetting, ThemeId, WorkspaceSetting};
use iced::advanced::clipboard;
use iced::advanced::widget::operation::Outcome;
use iced::widget::column;

const SIZE: Size = Size::new(800.0, 600.0);

fn look() -> Look {
    Look::new(ThemeId::Light, WorkspaceSetting::Theme, StatusbarSetting::Theme)
}

fn renderer() -> Renderer {
    let software = iced_tiny_skia::Renderer::new(crate::fonts::BODY, iced::Pixels(12.0));
    #[cfg(feature = "gpu-renderer")]
    {
        Renderer::Secondary(software)
    }
    #[cfg(not(feature = "gpu-renderer"))]
    {
        software
    }
}

/// Three buttons (one disabled) behind a "dialog" with two more.
fn screen(dialog: bool) -> Element<'static, &'static str> {
    let look = look();
    let behind = column![
        button(look, "Nieuw", ButtonKind::Secondary, Density::Regular, None, Some("nieuw")),
        button(look, "Uitgeschakeld", ButtonKind::Secondary, Density::Regular, None, None),
        button(look, "Opslaan", ButtonKind::Primary, Density::Regular, None, Some("opslaan")),
    ];
    let mut layers = column![inert(behind, dialog)];
    if dialog {
        layers = layers.push(column![
            button(look, "Annuleren", ButtonKind::Quiet, Density::Regular, None, Some("annuleren")),
            button(look, "Exporteren", ButtonKind::Primary, Density::Regular, None, Some("exporteren")),
        ]);
    }
    layers.into()
}

struct Ui {
    element: Element<'static, &'static str>,
    tree: Tree,
    node: layout::Node,
    renderer: Renderer,
}

impl Ui {
    fn new(dialog: bool) -> Self {
        let mut element = screen(dialog);
        let mut tree = Tree::new(&element);
        let renderer = renderer();
        let node = element.as_widget_mut().layout(&mut tree, &renderer, &layout::Limits::new(Size::ZERO, SIZE));
        Self { element, tree, node, renderer }
    }

    /// Rebuilds the view with or without the dialog, keeping the widget state.
    fn show(&mut self, dialog: bool) {
        self.element = screen(dialog);
        self.tree.diff(&self.element);
        self.node = self.element.as_widget_mut().layout(&mut self.tree, &self.renderer, &layout::Limits::new(Size::ZERO, SIZE));
    }

    /// Runs an operation to the end, as the runtime does for `focus_next`.
    fn operate(&mut self, operation: impl Operation<()> + 'static) {
        let mut operation: Box<dyn Operation<()>> = Box::new(operation);
        loop {
            self.element.as_widget_mut().operate(&mut self.tree, Layout::new(&self.node), &self.renderer, operation.as_mut());
            match operation.finish() {
                Outcome::Chain(next) => operation = next,
                _ => break,
            }
        }
    }

    fn send(&mut self, event: Event, cursor: mouse::Cursor) -> Vec<&'static str> {
        let mut messages = Vec::new();
        let mut shell = Shell::new(&mut messages);
        let viewport = Rectangle::with_size(SIZE);
        self.element.as_widget_mut().update(&mut self.tree, &event, Layout::new(&self.node), cursor, &self.renderer, &mut clipboard::Null, &mut shell, &viewport);
        messages
    }

    fn key(&mut self, named: Named) -> Vec<&'static str> {
        let key = Key::Named(named);
        self.send(
            Event::Keyboard(keyboard::Event::KeyPressed {
                key: key.clone(),
                modified_key: key,
                physical_key: keyboard::key::Physical::Unidentified(keyboard::key::NativeCode::Unidentified),
                location: keyboard::Location::Standard,
                modifiers: keyboard::Modifiers::empty(),
                text: None,
                repeat: false,
            }),
            mouse::Cursor::Unavailable,
        )
    }

    /// Whether each control in the Tab route has the focus, in route order.
    fn route(&mut self) -> Vec<bool> {
        struct Collect(Vec<bool>);
        impl Operation<()> for Collect {
            fn traverse(&mut self, operate: &mut dyn FnMut(&mut dyn Operation<()>)) {
                operate(self);
            }
            fn focusable(&mut self, _id: Option<&iced::widget::Id>, _bounds: Rectangle, state: &mut dyn Focusable) {
                self.0.push(state.is_focused());
            }
        }
        let mut collect = Collect(Vec::new());
        self.element.as_widget_mut().operate(&mut self.tree, Layout::new(&self.node), &self.renderer, &mut collect);
        collect.0
    }

    fn focused(&mut self) -> Option<usize> {
        self.route().iter().position(|&f| f)
    }
}

#[test]
fn tab_walks_the_enabled_controls_and_enter_presses_the_focused_one() {
    let mut ui = Ui::new(false);
    assert_eq!(ui.route().len(), 2, "a disabled button stays out of the Tab route");
    assert_eq!(ui.focused(), None);
    ui.operate(next());
    assert_eq!(ui.focused(), Some(0));
    assert_eq!(ui.key(Named::Enter), vec!["nieuw"]);
    ui.operate(next());
    assert_eq!(ui.focused(), Some(1));
    assert_eq!(ui.key(Named::Space), vec!["opslaan"]);
    ui.operate(next());
    assert_eq!(ui.focused(), Some(0), "Tab wraps around at the end");
    ui.operate(previous());
    assert_eq!(ui.focused(), Some(1), "Shift+Tab goes back");
    assert!(ui.key(Named::Escape).is_empty(), "other keys do not press the control");
}

#[test]
fn a_dialog_keeps_the_focus_and_returns_it_when_closed() {
    let mut ui = Ui::new(false);
    ui.operate(next());
    ui.operate(next());
    assert_eq!(ui.focused(), Some(1), "Opslaan has the focus");
    ui.show(true);
    assert_eq!(ui.route().len(), 2, "only the dialog's buttons are in the route");
    ui.operate(next());
    assert_eq!(ui.focused(), Some(0));
    ui.operate(next());
    ui.operate(next());
    assert_eq!(ui.focused(), Some(0), "Tab stays inside the dialog");
    assert_eq!(ui.key(Named::Enter), vec!["annuleren"], "Enter does not reach the screen behind");
    ui.show(false);
    assert_eq!(ui.focused(), Some(1), "closing the dialog returns the focus to Opslaan");
    assert_eq!(ui.key(Named::Enter), vec!["opslaan"]);
}

#[test]
fn a_click_moves_the_focus_without_the_ring() {
    let mut ui = Ui::new(false);
    let first = Layout::new(&ui.node).children().next().unwrap().children().next().unwrap().bounds();
    let _ = ui.send(Event::Mouse(mouse::Event::ButtonPressed(mouse::Button::Left)), mouse::Cursor::Available(first.center()));
    assert_eq!(ui.focused(), Some(0));
    let state = *ui.tree.children[0].children[0].children[0].state.downcast_ref::<State>();
    assert!(state.focused && !state.visible, "a click shows no focus ring");
    ui.operate(next());
    assert_eq!(ui.focused(), Some(1));
}
