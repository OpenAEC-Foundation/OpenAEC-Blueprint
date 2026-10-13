use crate::{fonts, icons::Icon, model::*, widgets, Language, Theme};
use iced::{widget::{button, column, container, mouse_area, pane_grid, pick_list, row, scrollable, slider, text, tooltip, Column, Row, Space}, Element, Fill};

/// Application-owned contents. Shell layout and styling stay inside the crate.
pub struct Slots<'a, M> {
    pub title: String,
    pub tabs: Vec<RibbonTab<M>>,
    pub documents: Vec<Document>,
    pub active_document: Option<String>,
    pub file_commands: Vec<Command<M>>,
    pub status: String,
    pub content: Box<dyn Fn(Region) -> Element<'a, Message<M>> + 'a>,
}
fn horizontal<'a,M:'a>(content: impl Into<Element<'a,M>>) -> Element<'a,M> {
    scrollable(content).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())).into()
}
pub fn shell<'a, M: Clone + 'a>(state: &'a ShellState, slots: Slots<'a,M>) -> Element<'a,Message<M>> {
    let theme = state.preferences.theme;
    let t = theme.tokens(); let l = state.preferences.language;
    let title = mouse_area(container(text(slots.title).font(fonts::MEDIUM).size(13)).width(Fill).height(metrics::TITLE).center_y(Fill))
        .on_press(Message::Ui(UiEvent::DragWindow));
    let titlebar = container(row![
        container(Icon::Cube.view(18,t.accent)).padding([0,8]), title,
        widgets::icon_button(l.text("Instellingen","Settings"),Icon::Settings,Message::Ui(UiEvent::Settings(true)),theme),
        widgets::icon_button(l.text("Minimaliseren","Minimize"),Icon::Minimize,Message::Ui(UiEvent::Minimize),theme),
        widgets::icon_button(l.text("Maximaliseren","Maximize"),Icon::Maximize,Message::Ui(UiEvent::Maximize),theme),
        widgets::icon_button(l.text("Sluiten","Close"),Icon::Close,Message::Ui(UiEvent::CloseWindow),theme),
    ].align_y(iced::Alignment::Center)).height(metrics::TITLE).style(move |_| container::Style::default().background(t.bg_lighter).color(t.text));
    let mut tabs = Row::new().spacing(2).push(button(text(l.text("Bestand","File")).font(fonts::STRONG).size(13)).padding([8,16]).on_press(Message::Ui(UiEvent::Backstage(true))).style(move |_,s| {
        let mut style=widgets::button_style(theme,true,s); style.background=Some(t.file_tab_bg.into());style.text_color=t.file_tab_text;style
    }));
    let active = slots.tabs.iter().find(|tab| tab.id == state.active_tab).or(slots.tabs.first());
    for tab in &slots.tabs {
        let selected = active.is_some_and(|a| a.id == tab.id);
        tabs = tabs.push(button(text(tab.label.clone()).font(fonts::MEDIUM).size(13)).padding([8,16]).on_press(Message::Ui(UiEvent::Tab(tab.id.clone()))).style(move |_,s| widgets::button_style(theme,selected,s)));
    }
    let tabs = container(horizontal(tabs)).height(metrics::TABS).width(Fill);
    let mut groups = Row::new().spacing(8);
    if let Some(active) = active {
        for group in &active.groups {
            let mut commands = Row::new().spacing(4);
            for command in &group.commands {
                let selected = command.selected;
                let color = if !command.enabled {t.text_faint} else if selected {t.accent} else {t.text};
                let label = command.label.clone();
                let hint = format!("{}{}", label, command.shortcut.as_ref().map(|s|format!(" ({s})")).unwrap_or_default());
                let control = button(column![command.icon.view(24,color),text(label).font(fonts::BODY).size(12)].spacing(6).align_x(iced::Alignment::Center))
                    .padding([8,12]).height(64).on_press_maybe(command.enabled.then(|| Message::Command(command.message.clone())))
                    .style(move |_,s| widgets::button_style(theme,selected,s));
                commands=commands.push(tooltip(control,text(hint).size(12),tooltip::Position::Bottom));
            }
            groups=groups.push(container(column![commands,text(group.label.clone()).font(fonts::MEDIUM).size(11).color(t.ribbon_group_label)].spacing(4).align_x(iced::Alignment::Center)).padding([4,8]).style(move |_| container::Style { border:iced::Border {color:t.ribbon_group_separator,width:1.0,radius:0.0.into()},..Default::default() }));
        }
    }
    let ribbon = container(horizontal(groups)).height(metrics::RIBBON).padding([4,8]);
    let mut documents = Row::new().spacing(2);
    for doc in slots.documents {
        let selected=slots.active_document.as_ref() == Some(&doc.id);
        let label=format!("{}{}",doc.title,if doc.dirty {" •"} else {""});
        documents=documents.push(row![
            button(text(label).size(12)).padding([6,12]).on_press(Message::Document(DocumentEvent::Activate(doc.id.clone()))).style(move |_,s|widgets::button_style(theme,selected,s)),
            widgets::icon_button(l.text("Document sluiten","Close document"),Icon::Close,Message::Document(DocumentEvent::CloseRequested(doc.id)),theme),
        ]);
    }
    let document_bar=container(horizontal(documents)).height(metrics::DOCUMENTS).width(Fill).style(move |_|container::Style::default().background(t.docbar_bg));
    let body: Element<'a,Message<M>> = if state.settings {
        settings(state)
    } else if state.backstage {
        let mut commands=Column::new().spacing(8).push(widgets::action(l.text("Terug","Back"),Icon::Back,Some(Message::Ui(UiEvent::Backstage(false))),theme));
        for command in slots.file_commands { commands=commands.push(widgets::action(command.label,command.icon,command.enabled.then_some(Message::Command(command.message)),theme)); }
        commands=commands.push(widgets::action(l.text("Instellingen","Settings"),Icon::Settings,Some(Message::Ui(UiEvent::Settings(true))),theme));
        container(column![text(l.text("Bestand","File")).font(fonts::HEADING).size(28),commands].spacing(24)).padding(32).width(Fill).height(Fill).into()
    } else {
        pane_grid::PaneGrid::new(&state.panes, move |_, region, _| pane_grid::Content::new((slots.content)(*region)))
            .spacing(2).on_resize(6,|e|Message::Ui(UiEvent::Resize(e))).height(Fill).into()
    };
    let status = container(row![text(slots.status).size(11).width(Fill),
        widgets::icon_button(l.text("Verkenner","Explorer"),Icon::PanelLeft,Message::Ui(UiEvent::ToggleLeft),theme),
        widgets::icon_button(l.text("Eigenschappen","Properties"),Icon::PanelRight,Message::Ui(UiEvent::ToggleRight),theme),
    ].align_y(iced::Alignment::Center)).padding([0,8]).height(metrics::STATUS).style(move |_|container::Style::default().background(t.status_bg).color(t.status_text));
    container(column![titlebar,tabs,ribbon,document_bar,body,status]).height(Fill).width(Fill).style(move |_| widgets::surface(theme)).into()
}
fn settings<'a,M:Clone+'a>(state:&'a ShellState) -> Element<'a,Message<M>> {
    let p=&state.preferences; let l=p.language;
    container(column![
        row![text(l.text("Instellingen","Settings")).font(fonts::HEADING).size(28),Space::with_width(Fill),widgets::action(l.text("Sluiten","Close"),Icon::Close,Some(Message::Ui(UiEvent::Settings(false))),p.theme)],
        text(l.text("Uiterlijk","Appearance")).font(fonts::STRONG),
        pick_list(Theme::ALL,Some(p.theme),|t|Message::Ui(UiEvent::Theme(t))),
        text(l.text("Taal","Language")).font(fonts::STRONG),
        pick_list(Language::ALL,Some(p.language),|l|Message::Ui(UiEvent::Language(l))),
        text(format!("{}: {:.0}%",l.text("Schaal","Scale"),p.scale*100.0)),
        slider(0.75..=2.0,p.scale,|s|Message::Ui(UiEvent::Scale(s))).step(0.05),
    ].spacing(16).max_width(640)).padding(32).width(Fill).height(Fill).into()
}
