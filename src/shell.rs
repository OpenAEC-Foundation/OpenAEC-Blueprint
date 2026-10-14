use crate::{fonts, icons::Icon, model::*, widgets, Language, Theme};
use iced::{widget::{button, column, container, mouse_area, opaque, pane_grid, pick_list, row, scrollable, slider, stack, text, tooltip, Column, Row, Space}, Element, Fill};

/// Application-owned contents. Shell layout and styling stay inside the crate.
pub struct Slots<'a, M> {
    pub title: String,
    pub tabs: Vec<RibbonTab<M>>,
    pub documents: Vec<Document>,
    pub active_document: Option<String>,
    pub file_commands: Vec<Command<M>>,
    pub quick_commands: Vec<Command<M>>,
    pub status: String,
    pub content: Box<dyn Fn(Region) -> Element<'a, Message<M>> + 'a>,
}
fn horizontal<'a,M:'a>(content: impl Into<Element<'a,M>>) -> Element<'a,M> {
    scrollable(content).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())).into()
}
pub fn shell<'a, M: Clone + 'a>(state: &'a ShellState, slots: Slots<'a,M>) -> Element<'a,Message<M>> {
    let theme = state.preferences.theme;
    let t = theme.tokens(); let l = state.preferences.language;
    let title = mouse_area(container(text(slots.title).font(fonts::MEDIUM).size(12).color(t.accent)).width(Fill).height(metrics::TITLE).center(Fill))
        .on_press(Message::Ui(UiEvent::DragWindow));
    let mut quick = Row::new().spacing(1);
    for command in &slots.quick_commands {
        let hint=format!("{}{}",command.label,command.shortcut.as_ref().map(|s|format!(" ({s})")).unwrap_or_default());
        let control=button(command.icon.view(16,if command.enabled {t.accent} else {t.text_faint}))
            .padding([4,7]).on_press_maybe(command.enabled.then(||Message::Command(command.message.clone())))
            .style(move |_,s|widgets::button_style(theme,false,s));
        quick=quick.push(tooltip(control,text(hint).size(12),tooltip::Position::Bottom));
    }
    let titlebar = container(row![
        container(Icon::Cube.view(18,t.accent)).padding([0,8]), quick, title,
        widgets::icon_button(l.text("Instellingen","Settings"),Icon::Settings,Message::Ui(UiEvent::Settings(true)),theme),
        widgets::icon_button(l.text("Minimaliseren","Minimize"),Icon::Minimize,Message::Ui(UiEvent::Minimize),theme),
        widgets::icon_button(l.text("Maximaliseren","Maximize"),Icon::Maximize,Message::Ui(UiEvent::Maximize),theme),
        widgets::icon_button(l.text("Sluiten","Close"),Icon::Close,Message::Ui(UiEvent::CloseWindow),theme),
    ].align_y(iced::Alignment::Center)).height(metrics::TITLE).style(move |_| container::Style::default().background(t.bg_lighter).color(t.text));
    let mut tabs = Row::new().spacing(2).push(button(text(l.text("Bestand","File")).font(fonts::STRONG).size(13)).padding([4,16]).on_press(Message::Ui(UiEvent::Backstage(true))).style(move |_,s| {
        let mut style=widgets::button_style(theme,true,s); style.background=Some(t.file_tab_bg.into());style.text_color=t.file_tab_text;style
    }));
    let active = slots.tabs.iter().find(|tab| tab.id == state.active_tab).or(slots.tabs.first());
    for tab in &slots.tabs {
        let selected = active.is_some_and(|a| a.id == tab.id);
        tabs = tabs.push(button(text(tab.label.clone()).font(fonts::MEDIUM).size(13)).padding([4,16]).on_press(Message::Ui(UiEvent::Tab(tab.id.clone()))).style(move |_,s| widgets::button_style(theme,selected,s)));
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
                    .padding([5,10]).height(58).on_press_maybe(command.enabled.then(|| Message::Command(command.message.clone())))
                    .style(move |_,s| widgets::ribbon_button_style(theme,selected,s));
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
    let body: Element<'a,Message<M>> = if state.backstage {
        let mut commands=Column::new().spacing(8).push(widgets::action(l.text("Terug","Back"),Icon::Back,Some(Message::Ui(UiEvent::Backstage(false))),theme));
        for command in slots.file_commands { commands=commands.push(widgets::action(command.label,command.icon,command.enabled.then_some(Message::Command(command.message)),theme)); }
        commands=commands.push(widgets::action(l.text("Instellingen","Settings"),Icon::Settings,Some(Message::Ui(UiEvent::Settings(true))),theme));
        container(column![text(l.text("Bestand","File")).font(fonts::HEADING).size(28),commands].spacing(24)).padding(32).width(Fill).height(Fill).into()
    } else {
        pane_grid::PaneGrid::new(&state.panes, move |_, region, _| pane_grid::Content::new((slots.content)(*region)))
            .spacing(2).on_resize(6,|e|Message::Ui(UiEvent::Resize(e))).height(Fill).into()
    };
    let status = container(row![text(slots.status).size(11).width(Fill),
        widgets::status_icon_button(l.text("Verkenner","Explorer"),Icon::PanelLeft,Message::Ui(UiEvent::ToggleLeft),theme),
        widgets::status_icon_button(l.text("Eigenschappen","Properties"),Icon::PanelRight,Message::Ui(UiEvent::ToggleRight),theme),
    ].align_y(iced::Alignment::Center)).padding([0,8]).height(metrics::STATUS).style(move |_|container::Style::default().background(t.status_bg).color(t.status_text));
    let base: Element<'a,Message<M>>=container(column![titlebar,tabs,ribbon,document_bar,body,status]).height(Fill).width(Fill).style(move |_| widgets::surface(theme)).into();
    if state.settings {
        let overlay=container(settings(state)).center(Fill).style(move |_|container::Style::default().background(t.dialog_overlay));
        stack([base,opaque(overlay)]).width(Fill).height(Fill).into()
    } else {base}
}
fn settings<'a,M:Clone+'a>(state:&'a ShellState) -> Element<'a,Message<M>> {
    let p=&state.preferences; let l=p.language; let t=p.theme.tokens();
    let header=container(row![text(l.text("Instellingen","Settings")).font(fonts::STRONG).size(15).color(t.dialog_header_text).width(Fill),widgets::icon_button(l.text("Sluiten","Close"),Icon::Close,Message::Ui(UiEvent::Settings(false)),p.theme)]
        .align_y(iced::Alignment::Center)).padding([7,12]).width(Fill).style(move |_|container::Style::default().background(t.dialog_header_bg));
    let form=column![
        text(l.text("Uiterlijk","Appearance")).font(fonts::HEADING).size(20),
        text(l.text("Thema","Theme")).font(fonts::STRONG).size(12),
        pick_list(Theme::ALL,Some(p.theme),|theme|Message::Ui(UiEvent::Theme(theme))).width(Fill),
        text(l.text("Taal","Language")).font(fonts::STRONG).size(12),
        pick_list(Language::ALL,Some(p.language),|language|Message::Ui(UiEvent::Language(language))).width(Fill),
        text(format!("{}: {:.0}%",l.text("Schaal","Scale"),p.scale*100.0)).font(fonts::STRONG).size(12),
        slider(0.75..=2.0,p.scale,|scale|Message::Ui(UiEvent::Scale(scale))).step(0.05),
    ].spacing(12);
    let sidebar=container(column![text(l.text("Algemeen","General")).size(12),text(l.text("Uiterlijk","Appearance")).font(fonts::STRONG).size(12).color(t.accent)].spacing(20))
        .padding(16).width(140).height(Fill).style(move |_|container::Style::default().background(t.dialog_sidebar_bg));
    let body=row![sidebar,container(form).padding(22).width(Fill)].height(Fill);
    let footer=container(row![Space::with_width(Fill),widgets::action(l.text("Sluiten","Close"),Icon::Check,Some(Message::Ui(UiEvent::Settings(false))),p.theme)])
        .padding([9,12]).width(Fill).style(move |_|container::Style::default().background(t.dialog_header_bg));
    container(column![header,body,footer].height(460).width(560)).style(move |_|container::Style {
        background:Some(t.dialog_bg.into()),border:iced::Border{color:t.dialog_border,width:1.0,radius:4.0.into()},..Default::default()
    }).into()
}
