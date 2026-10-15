use crate::{fonts, icons::Icon, model::*, widgets, Language, Theme};
use iced::{widget::{button, column, container, mouse_area, pane_grid, pick_list, row, scrollable, slider, stack, text, tooltip, Column, Row, Space}, Element, Fill, Padding};

/// Application-owned contents. Shell layout and styling stay inside the crate.
pub struct Slots<'a, M> {
    pub title: String,
    pub mode: ChromeMode,
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
        quick=quick.push(widgets::title_action(
            command.icon.view(16,if command.enabled {t.accent} else {t.text_faint}).into(),
            hint,
            command.enabled.then(||Message::Command(command.message.clone())),
            theme,
        ));
    }
    let titlebar = container(row![
        container(Icon::Cube.view(18,t.accent)).padding([0,8]), quick, title,
        widgets::title_action(Icon::Settings.view(16,t.text).into(),l.text("Instellingen","Settings"),Some(Message::Ui(UiEvent::Settings(true))),theme),
        widgets::title_action(Icon::Minimize.view(16,t.text).into(),l.text("Minimaliseren","Minimize"),Some(Message::Ui(UiEvent::Minimize)),theme),
        widgets::title_action(Icon::Maximize.view(16,t.text).into(),l.text("Maximaliseren","Maximize"),Some(Message::Ui(UiEvent::Maximize)),theme),
        widgets::title_action(Icon::Close.view(16,t.text).into(),l.text("Sluiten","Close"),Some(Message::Ui(UiEvent::CloseWindow)),theme),
    ].align_y(iced::Alignment::Center)).height(metrics::TITLE).style(move |_| container::Style::default().background(t.bg_lighter).color(t.text));
    let mut tabs = Row::new().spacing(if slots.mode == ChromeMode::CanvasRibbon { 6 } else { 2 });
    if !matches!(slots.mode, ChromeMode::TopNav | ChromeMode::CanvasRibbon) {
        tabs = tabs.push(button(text(l.text("Bestand","File")).font(fonts::STRONG).size(13)).padding([4,16]).on_press(Message::Ui(UiEvent::Backstage(true))).style(move |_,s| {
            let mut style=widgets::button_style(theme,true,s); style.background=Some(t.file_tab_bg.into());style.text_color=t.file_tab_text;style
        }));
    }
    let active = slots.tabs.iter().find(|tab| tab.id == state.active_tab).or(slots.tabs.first());
    for tab in &slots.tabs {
        let selected = active.is_some_and(|a| a.id == tab.id);
        tabs = tabs.push(button(text(tab.label.clone()).font(fonts::MEDIUM).size(13)).padding([4,16]).on_press(Message::Ui(UiEvent::Tab(tab.id.clone()))).style(move |_,s| widgets::ribbon_tab_style(theme,selected,s)));
    }
    let tabs = container(horizontal(tabs)).height(metrics::TABS).width(Fill);
    let mut groups = Row::new().spacing(0);
    if let Some(active) = active {
        for group in &active.groups {
            let mut commands = Row::new().spacing(1);
            let mut tools_width = 0.0_f32;
            for command in &group.commands {
                if let Some(control) = &command.control {
                    tools_width += control.width();
                    commands = commands.push(widgets::ribbon_control(theme, command.label.clone(), control.clone()).map(Message::Command));
                    continue;
                }
                let selected = command.selected;
                let color = if !command.enabled {t.text_faint} else if selected {t.accent} else {t.text};
                let label = command.label.clone();
                let control_width = (label.chars().count() as f32 * 7.0 + 20.0).clamp(66.0, 160.0);
                tools_width += control_width;
                let hint = format!("{}{}", label, command.shortcut.as_ref().map(|s|format!(" ({s})")).unwrap_or_default());
                let control = button(column![command.icon.view(24,color),text(label).font(fonts::BODY).size(12)].spacing(6).align_x(iced::Alignment::Center))
                    .padding([3,10]).width(control_width).height(52).on_press_maybe(command.enabled.then(|| Message::Command(command.message.clone())))
                    .style(move |_,s| widgets::ribbon_button_style(theme,selected,s));
                commands=commands.push(tooltip(control,text(hint).size(12),tooltip::Position::Bottom));
            }
            tools_width += group.commands.len().saturating_sub(1) as f32;
            let caption_width = (group.label.chars().count() as f32 * 6.0 + 8.0).max(50.0);
            let group_width = tools_width.max(caption_width) + 17.0;
            groups=groups.push(widgets::ribbon_group(theme, group.label.clone(), commands.into(), group_width));
        }
    }
    let ribbon = container(
        scrollable(groups)
            .direction(scrollable::Direction::Horizontal(
                scrollable::Scrollbar::new().width(3).scroller_width(3).margin(0),
            ))
            .height(Fill),
    ).height(metrics::RIBBON).padding(Padding { top: 0.0, right: 8.0, bottom: 0.0, left: 2.0 });
    let mut documents = Row::new().spacing(1).align_y(iced::Alignment::End);
    for doc in slots.documents {
        let selected=slots.active_document.as_ref() == Some(&doc.id);
        let label=format!("{}{}",doc.title,if doc.dirty {" •"} else {""});
        let close = button(text("×").size(12))
            .on_press(Message::Document(DocumentEvent::CloseRequested(doc.id.clone())))
            .style(move |_, status| widgets::document_close_style(theme, selected, status))
            .padding([0, 4]);
        let content = row![text(label).size(11), close]
            .spacing(6)
            .align_y(iced::Alignment::Center);
        let tab = button(content)
            .on_press(Message::Document(DocumentEvent::Activate(doc.id)))
            .height(24)
            .padding(Padding { top: 0.0, bottom: 0.0, left: 10.0, right: 4.0 })
            .style(move |_, status| widgets::document_tab_style(theme, selected, status));
        documents = documents.push(widgets::document_tab_bottom_gap(theme, tab.into()));
    }
    let document_bar=crate::frame::document_bar(theme, horizontal(documents));
    let body: Element<'a,Message<M>> = if state.backstage {
        let mut commands=Column::new().spacing(8).push(widgets::action(l.text("Terug","Back"),Icon::Back,Some(Message::Ui(UiEvent::Backstage(false))),theme));
        for command in slots.file_commands { commands=commands.push(widgets::action(command.label,command.icon,command.enabled.then_some(Message::Command(command.message)),theme)); }
        commands=commands.push(widgets::action(l.text("Instellingen","Settings"),Icon::Settings,Some(Message::Ui(UiEvent::Settings(true))),theme));
        container(column![text(l.text("Bestand","File")).font(fonts::HEADING).size(28),commands].spacing(24)).padding(32).width(Fill).height(Fill).into()
    } else if slots.mode == ChromeMode::TopNav {
        (slots.content)(Region::Workspace)
    } else if slots.mode == ChromeMode::CanvasRibbon {
        row![
            container((slots.content)(Region::Explorer)).width(255).height(Fill),
            container((slots.content)(Region::Workspace)).width(Fill).height(Fill),
        ].height(Fill).width(Fill).into()
    } else if matches!(slots.mode, ChromeMode::Workflow | ChromeMode::Sidebar) {
        row![
            container((slots.content)(Region::Explorer)).width(260).height(Fill),
            container((slots.content)(Region::Workspace)).width(Fill).height(Fill),
        ].height(Fill).width(Fill).into()
    } else {
        pane_grid::PaneGrid::new(&state.panes, move |_, region, _| pane_grid::Content::new((slots.content)(*region)))
            .spacing(2).on_resize(6,|e|Message::Ui(UiEvent::Resize(e))).height(Fill).into()
    };
    let mut status_row = Row::new().push(text(slots.status).size(11).width(Fill));
    if slots.mode == ChromeMode::Ribbon {
        status_row = status_row
            .push(widgets::status_icon_button(l.text("Verkenner","Explorer"),Icon::PanelLeft,Message::Ui(UiEvent::ToggleLeft),theme))
            .push(widgets::status_icon_button(l.text("Eigenschappen","Properties"),Icon::PanelRight,Message::Ui(UiEvent::ToggleRight),theme));
    }
    let status = crate::frame::status_bar(
        theme,
        status_row.align_y(iced::Alignment::Center).height(Fill).into(),
        8,
    );
    let bands = if slots.mode == ChromeMode::TopNav {
        crate::frame::frame(crate::frame::FrameSlots {
            titlebar: titlebar.into(), tabs: tabs.into(), ribbon: None,
            documents: None, content: body, status: status.into(),
        })
    } else if matches!(slots.mode, ChromeMode::Workflow | ChromeMode::Sidebar) {
        crate::frame::workflow_frame(titlebar.into(), (slots.mode == ChromeMode::Workflow).then_some(document_bar.into()), body, status.into())
    } else {
        crate::frame::frame(crate::frame::FrameSlots {
            titlebar: titlebar.into(),
            tabs: tabs.into(),
            ribbon: Some(ribbon.into()),
            documents: Some(document_bar.into()),
            content: body,
            status: status.into(),
        })
    };
    let base: Element<'a,Message<M>>=container(bands).height(Fill).width(Fill).style(move |_| widgets::surface(theme)).into();
    if state.settings {
        stack([base,settings(state)]).width(Fill).height(Fill).into()
    } else {base}
}
fn settings<'a,M:Clone+'a>(state:&'a ShellState) -> Element<'a,Message<M>> {
    let p=&state.preferences; let l=p.language; let t=p.theme.tokens();
    let form=column![
        text(l.text("Uiterlijk","Appearance")).font(fonts::HEADING).size(20),
        text(l.text("Thema","Theme")).font(fonts::STRONG).size(12),
        pick_list(Theme::ALL,Some(p.theme),|theme|Message::Ui(UiEvent::Theme(theme)))
            .style(move |_,status|widgets::pick_list_style(p.theme,status))
            .menu_style(move |_|widgets::pick_list_menu_style(p.theme)).width(Fill),
        text(l.text("Taal","Language")).font(fonts::STRONG).size(12),
        pick_list(Language::ALL,Some(p.language),|language|Message::Ui(UiEvent::Language(language)))
            .style(move |_,status|widgets::pick_list_style(p.theme,status))
            .menu_style(move |_|widgets::pick_list_menu_style(p.theme)).width(Fill),
        text(format!("{}: {:.0}%",l.text("Schaal","Scale"),p.scale*100.0)).font(fonts::STRONG).size(12),
        slider(0.75..=2.0,p.scale,|scale|Message::Ui(UiEvent::Scale(scale)))
            .step(0.05).style(move |_,status|widgets::slider_style(p.theme,status)),
    ].spacing(12);
    let sidebar=container(column![text(l.text("Algemeen","General")).size(12),text(l.text("Uiterlijk","Appearance")).font(fonts::STRONG).size(12).color(t.accent)].spacing(20))
        .padding([4,12]);
    let footer=row![Space::with_width(Fill),widgets::action(l.text("Sluiten","Close"),Icon::Check,Some(Message::Ui(UiEvent::Settings(false))),p.theme)];
    widgets::settings_modal(
        l.text("Instellingen","Settings"), sidebar.into(), form.into(), footer.into(),
        Message::Ui(UiEvent::Settings(false)), p.theme,
    )
}
