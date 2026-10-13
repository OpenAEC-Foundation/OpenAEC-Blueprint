use crate::*;
use iced::{Element, Task, Subscription};
use std::path::PathBuf;

/// Implement only domain behavior; the shared runtime owns all window chrome.
pub trait Application: 'static {
    type Command: Clone + std::fmt::Debug + Send + 'static;
    fn title(&self) -> String;
    fn ribbon(&self, language: Language) -> Vec<RibbonTab<Self::Command>>;
    fn workspace(&self, theme: Theme, language: Language) -> Element<'_, Self::Command>;
    fn update(&mut self, command: Self::Command) -> Task<Self::Command>;
    fn explorer(&self, theme: Theme, language: Language) -> Element<'_, Self::Command> {
        widgets::empty_state(language.text("Verkenner","Explorer"), "", theme)
    }
    fn properties(&self, theme: Theme, language: Language) -> Element<'_, Self::Command> {
        widgets::empty_state(language.text("Eigenschappen","Properties"), "", theme)
    }
    fn file_commands(&self, _language: Language) -> Vec<Command<Self::Command>> { Vec::new() }
    fn documents(&self) -> Vec<Document> { Vec::new() }
    fn active_document(&self) -> Option<String> { None }
    fn document_event(&mut self, _event: DocumentEvent) -> Task<Self::Command> { Task::none() }
    fn status(&self, language: Language) -> String { language.text("Gereed","Ready").into() }
    fn subscription(&self) -> Subscription<Self::Command> { Subscription::none() }
    /// Return false to keep the window open while the application asks to save.
    fn close_requested(&mut self) -> bool { true }
}
struct Runtime<A:Application> { app:A, shell:ShellState, preferences_path:Option<PathBuf>, error:Option<String> }
impl<A:Application> Runtime<A> {
    fn update(&mut self, message: Message<A::Command>) -> Task<Message<A::Command>> {
        match message {
            Message::Command(command) => self.app.update(command).map(Message::Command),
            Message::Document(event) => self.app.document_event(event).map(Message::Command),
            Message::Ui(event) => {
                let window_task:Option<Task<Message<A::Command>>> = match &event {
                    UiEvent::DragWindow => Some(iced::window::get_latest().and_then(iced::window::drag)),
                    UiEvent::Minimize => Some(iced::window::get_latest().and_then(|id|iced::window::minimize(id,true))),
                    UiEvent::Maximize => Some(iced::window::get_latest().and_then(iced::window::toggle_maximize)),
                    UiEvent::CloseWindow if self.app.close_requested() => Some(iced::window::get_latest().and_then(iced::window::close)),
                    _ => None,
                };
                self.shell.update(&event);
                if matches!(event, UiEvent::Theme(_) | UiEvent::Language(_) | UiEvent::Scale(_) | UiEvent::ToggleLeft | UiEvent::ToggleRight | UiEvent::Resize(_)) {
                    if let Some(path)=&self.preferences_path {
                        self.error=self.shell.preferences.save(path).err().map(|e|format!("Settings: {e}"));
                    }
                }
                window_task.unwrap_or_else(Task::none)
            }
        }
    }
    fn view(&self) -> Element<'_,Message<A::Command>> {
        let theme=self.shell.preferences.theme; let language=self.shell.preferences.language;
        shell(&self.shell, Slots {
            title:self.app.title(), tabs:self.app.ribbon(language), documents:self.app.documents(),
            active_document:self.app.active_document(), file_commands:self.app.file_commands(language),
            status:self.error.clone().unwrap_or_else(||self.app.status(language)),
            content:Box::new(move |region| match region {
                Region::Workspace => self.app.workspace(theme,language).map(Message::Command),
                Region::Explorer => widgets::panel(language.text("Verkenner","Explorer"),self.app.explorer(theme,language).map(Message::Command),theme),
                Region::Properties => widgets::panel(language.text("Eigenschappen","Properties"),self.app.properties(theme,language).map(Message::Command),theme),
            }),
        })
    }
    fn subscription(&self)->Subscription<Message<A::Command>> {
        Subscription::batch([
            self.app.subscription().map(Message::Command),
            iced::window::close_requests().map(|_|Message::Ui(UiEvent::CloseWindow)),
            iced::keyboard::on_key_press(|key,mods| {
                use iced::keyboard::{Key,key::Named};
                match key {
                    Key::Named(Named::Escape) => Some(Message::Ui(UiEvent::Settings(false))),
                    Key::Character(c) if mods.command() && c.as_str()=="," => Some(Message::Ui(UiEvent::Settings(true))),
                    _ => None,
                }
            }),
        ])
    }
}
/// Start the same shell in every tool. Pass a per-application preferences path,
/// or `None` for an ephemeral showcase. All fonts are embedded in this crate.
pub fn run<A:Application>(app:A, preferences_path:Option<PathBuf>) -> iced::Result {
    let (preferences,error)= match preferences_path.as_deref().filter(|p|p.exists()) {
        Some(path)=>match Preferences::load(path) { Ok(p)=>(p,None),Err(e)=>(Preferences::default(),Some(format!("Settings: {e}"))) },
        None=>(Preferences::default(),None),
    };
    iced::application(|state:&Runtime<A>|state.app.title(),Runtime::update,Runtime::view)
        .subscription(Runtime::subscription)
        .theme(|state:&Runtime<A>|state.shell.preferences.theme.iced())
        .scale_factor(|state:&Runtime<A>|state.shell.preferences.scale)
        .default_font(fonts::BODY).font(fonts::FILES[0]).font(fonts::FILES[1]).font(fonts::FILES[2])
        .font(fonts::FILES[3]).font(fonts::FILES[4]).font(fonts::FILES[5])
        .window(iced::window::Settings { size:iced::Size::new(1280.0,800.0), min_size:Some(iced::Size::new(720.0,480.0)), decorations:false, exit_on_close_request:false,..Default::default() })
        .run_with(||(Runtime{app,shell:ShellState::new(preferences),preferences_path,error},Task::none()))
}
