//! Native Rust screen study for the current viewer and /validate branches.
use super::*;
use openaec_ui::iced::widget::{column, row};

#[derive(Deserialize)]
pub(super) struct ValidatorData {
    pub routes: Vec<ValidatorRoute>,
    pub right_tabs: Vec<ValidatorRoute>,
}
#[derive(Deserialize)]
pub(super) struct ValidatorRoute {
    pub id: String,
    pub label: String,
    pub branch: String,
    pub note: String,
    pub evidence: ValidatorEvidence,
}
#[derive(Deserialize)]
pub(super) struct ValidatorEvidence {
    pub file: String,
    pub line: usize,
}
pub(super) fn data() -> &'static ValidatorData {
    static DATA: OnceLock<ValidatorData> = OnceLock::new();
    DATA.get_or_init(|| serde_json::from_str(include_str!("../../../harmonization/validator-screen-routes.json"))
        .expect("valid source-pinned BIM Validator inventory"))
}

fn surface<'a>(theme: Theme, content: impl Into<Element<'a, Action>>, padding: u16) -> Element<'a, Action> {
    let t = theme.tokens();
    container(content).padding(padding).width(Fill)
        .style(move |_| container::Style::default().background(t.bg_lighter)
            .border(iced::Border::default().color(t.border).width(1))).into()
}
fn line<'a>(theme: Theme, label: impl Into<String>, value: impl Into<String>) -> Element<'a, Action> {
    let t = theme.tokens();
    container(row![text(label.into()).size(11).width(Fill), text(value.into()).size(11).color(t.text_secondary)]
        .spacing(7)).padding([8, 9]).width(Fill)
        .style(move |_| container::Style::default().border(iced::Border::default().color(t.border).width(1))).into()
}

impl StyleRepo {
    pub(super) fn validator_native_page(&self, theme: Theme) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        let route = &d.routes[self.validator_route];
        let mut selectors = Column::new().spacing(4);
        for branch in ["viewer", "legacy"] {
            let mut choices = Row::new().spacing(4);
            for (index, item) in d.routes.iter().enumerate().filter(|(_, item)| item.branch == branch) {
                choices = choices.push(button(text(&item.label).size(10)).padding([5, 7])
                    .on_press(Action::SelectValidatorRoute(index))
                    .style(move |_, status| widgets::button_style(theme, self.validator_route == index, status)));
            }
            selectors = selectors.push(scrollable(choices).height(30)
                .direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())));
        }
        let mut header = Column::new().spacing(5)
            .push(text("OPEN BIM VALIDATOR · NATIVE RUST SCHERMREVIEW").font(fonts::STRONG).size(10).color(t.accent))
            .push(text(&route.label).font(fonts::HEADING).size(19).color(t.text))
            .push(text(&route.note).size(10).color(t.text_secondary));
        if route.branch == "viewer" {
            header = header.push(row![
                button(text(if self.validator_left_visible { "Modellen verbergen" } else { "Modellen tonen" }).size(10))
                    .padding([5, 8]).on_press(Action::ToggleValidatorLeft)
                    .style(move |_, status| widgets::button_style(theme, self.validator_left_visible, status)),
                button(text(if self.validator_right_visible { "Rechterpaneel verbergen" } else { "Rechterpaneel tonen" }).size(10))
                    .padding([5, 8]).on_press(Action::ToggleValidatorRight)
                    .style(move |_, status| widgets::button_style(theme, self.validator_right_visible, status)),
            ].spacing(5));
        }
        let top = container(column![header, selectors].spacing(8)).padding(11).width(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border::default().color(t.border).width(1)));
        let evidence = text(format!("{}:{} · commit 8f837dd · voorbeeldinhoud, geen broncapture",
            route.evidence.file, route.evidence.line)).size(9).color(t.text_secondary);
        if route.branch == "legacy" {
            return container(scrollable(column![top, self.validator_legacy(theme, &route.id), evidence]
                .spacing(12).padding(12))).width(Fill).height(Fill).into();
        }
        let loaded = route.id != "viewer-empty";
        let canvas = self.validator_canvas(theme, loaded, route.id == "viewer-results");
        column![top, canvas, container(evidence).padding([5, 9])]
            .spacing(2).width(Fill).height(Fill).into()
    }

    pub(super) fn validator_left_panel(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let loaded = data().routes[self.validator_route].id != "viewer-empty";
        let model_list: Element<'_, Action> = if loaded {
            column![
                line(theme, "▾  Project", "1 model"),
                line(theme, "  ◉  Gebouw.ifc", "zichtbaar"),
                line(theme, "     Verdieping 01", "IfcBuildingStorey"),
            ].spacing(2).into()
        } else {
            text("Upload een IFC bestand").size(11).color(t.text_secondary).into()
        };
        let models = container(column![
            text("MODELLEN").font(fonts::STRONG).size(10).color(t.accent),
            model_list,
        ].spacing(10)).padding(12).width(Fill).height(175)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border::default().color(t.border).width(1)));
        let properties = container(column![
            text("EIGENSCHAPPEN").font(fonts::STRONG).size(10).color(t.accent),
            text(if self.validator_route == 4 { "IfcWall · geselecteerd in resultaatboom" } else { "Selecteer een element in de 3D-viewer" })
                .size(11).color(t.text_secondary),
            if self.validator_route == 4 { line(theme, "GlobalId", "voorbeeld") } else { Space::new().width(0).height(0).into() },
        ].spacing(13)).padding(12).width(Fill).height(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border::default().color(t.border).width(1)));
        column![models, properties].spacing(2).height(Fill).width(Fill).into()
    }

    pub(super) fn validator_right_panel(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let id = data().routes[self.validator_route].id.as_str();
        let tab = if id == "viewer-clashes" { "clashes" } else if id == "viewer-bcf" { "bcf" } else { "validation" };
        let mut tabs = Row::new().spacing(2);
        for entry in &data().right_tabs {
            let target = match entry.id.as_str() { "clashes" => 6, "bcf" => 7, _ => 0 };
            tabs = tabs.push(button(text(&entry.label).size(11)).padding([8, 7])
                .on_press(Action::SelectValidatorRoute(target))
                .style(move |_, status| widgets::button_style(theme, tab == entry.id, status)));
        }
        let body: Element<'_, Action> = match id {
            "viewer-clashes" => surface(theme, column![
                text("Clashes").font(fonts::STRONG).size(13),
                text("Clash detection — binnenkort beschikbaar").size(11).color(t.text_secondary),
            ].spacing(10), 14),
            "viewer-bcf" => surface(theme, column![
                text("Issue Queue").font(fonts::STRONG).size(13),
                line(theme, "Deurhoogte controleren", "lokaal"),
                text("Local Export").font(fonts::STRONG).size(12),
                text("BCF ZIP downloaden · voorbeeldactie").size(11).color(t.accent),
            ].spacing(12), 14),
            _ => self.validator_validation(theme, id),
        };
        container(column![tabs, scrollable(body).height(Fill)].spacing(8)).padding(8).height(Fill).width(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border::default().color(t.border).width(1))).into()
    }

    fn validator_validation(&self, theme: Theme, id: &str) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut content = Column::new().spacing(10)
            .push(text("IDS STANDAARD").font(fonts::STRONG).size(10).color(t.accent))
            .push(line(theme, "◉  NL BIM Basis ILS", ""))
            .push(line(theme, "○  RVB BIM Norm", ""))
            .push(line(theme, "○  Custom IDS", ""))
            .push(button(text("Valideer").size(11)).padding([7, 12])
                .style(move |_, status| widgets::button_style(theme, true, status)));
        match id {
            "viewer-submitting" => content = content.push(text("Bestanden uploaden…").size(11).color(t.accent)),
            "viewer-polling" => content = content.push(column![
                text("Validatie wordt uitgevoerd").font(fonts::STRONG).size(11),
                progress_bar(0.0..=100.0, 63.0).girth(7),
                text("Annuleren").size(10).color(t.text_secondary),
            ].spacing(9)),
            "viewer-error" => content = content.push(column![
                text("Validatie mislukt").font(fonts::STRONG).size(12).color(iced::Color::from_rgb8(194, 71, 62)),
                text("Controleer verbinding of invoerbestand.").size(10),
                text("Opnieuw proberen").size(10).color(t.accent),
            ].spacing(7)),
            "viewer-results" => content = content
                .push(text("RESULTATEN · 2 geslaagd / 2 fouten").font(fonts::STRONG).size(10).color(t.accent))
                .push(line(theme, "▾  Constructieve eisen", "2 / 2"))
                .push(line(theme, "  ✕  Wandhoogte", "1 fout"))
                .push(line(theme, "  ✓  Materiaalclassificatie", "goed"))
                .push(text("DETAIL · IfcWall").font(fonts::STRONG).size(10))
                .push(text("Geselecteerd element krijgt een highlight in 3D.").size(10).color(t.text_secondary)),
            _ => {}
        }
        surface(theme, content, 12)
    }

    fn validator_canvas(&self, theme: Theme, loaded: bool, selected: bool) -> Element<'_, Action> {
        let t = theme.tokens();
        let drawing: Element<'_, Action> = if loaded {
            let stroke = if selected { "#d77260" } else { "#82a8b0" };
            let svg_text = format!("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 360'><g fill='none' stroke='{stroke}' stroke-width='2' opacity='.9'><path d='M90 200 250 100 465 170 308 270Z M90 200V270L308 341V270 M308 270V341L465 240V170 M250 100V170 M150 178V287 M205 145V305 M358 153V306 M410 168V274'/><path d='M91 235 308 305 465 205 M150 178 359 244 M205 145 411 211 M250 100 465 170'/></g></svg>");
            column![
                svg(svg::Handle::from_memory(svg_text.into_bytes())).width(Fill).height(350),
                text(if selected { "IfcWall · resultaat geselecteerd" } else { "Gebouw.ifc · illustratief wireframe" })
                    .size(10).color(iced::Color::WHITE),
            ].spacing(3).align_x(Alignment::Center).into()
        } else {
            text("3D Viewer laden… / IFC openen").size(13).color(iced::Color::WHITE).into()
        };
        container(drawing).center(Fill).width(Fill).height(Fill)
            .style(move |_| container::Style::default().background(iced::Color::from_rgb8(30, 35, 43))
                .border(iced::Border::default().color(t.border).width(1))).into()
    }

    fn validator_legacy(&self, theme: Theme, id: &str) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut cards = Column::new().spacing(12).width(760)
            .push(text("3BM IFC Validator").font(fonts::HEADING).size(23).color(t.text))
            .push(text("Validate IFC files against IDS standards").size(11).color(t.text_secondary))
            .push(surface(theme, column![
                text("IFC File").font(fonts::STRONG).size(13),
                line(theme, if id == "legacy-idle" { "Select IFC file…" } else { "Gebouw.ifc · voorbeeldbestand" }, ""),
                text("IDS Standard").font(fonts::STRONG).size(13),
                line(theme, "◉  NL BIM Basis ILS", ""),
                line(theme, "○  RVB BIM Norm", ""),
                line(theme, "○  Custom IDS", ""),
                text("Validate").size(11).color(t.accent),
            ].spacing(9), 17));
        match id {
            "legacy-submitting" => cards = cards.push(surface(theme, text("Uploading files and starting validation…").size(12), 17)),
            "legacy-polling" => cards = cards.push(surface(theme, column![
                text("Validation progress").font(fonts::STRONG).size(13),
                progress_bar(0.0..=100.0, 63.0).girth(7),
                text("Cancel").size(11).color(t.accent),
            ].spacing(10), 17)),
            "legacy-completed" => cards = cards.push(surface(theme, column![
                text("Results Summary").font(fonts::STRONG).size(15),
                line(theme, "Passed", "2"), line(theme, "Failed", "2"),
                text("Specifications").font(fonts::STRONG).size(13),
                line(theme, "Constructieve eisen", "voorbeeld"),
                text("Download JSON　 New Validation").size(11).color(t.accent),
            ].spacing(9), 17)),
            "legacy-error" => cards = cards.push(surface(theme, column![
                text("Validation failed").font(fonts::STRONG).size(15).color(iced::Color::from_rgb8(194, 71, 62)),
                text("Controleer bestand of verbinding.").size(11),
                text("Retry　 Dismiss").size(11).color(t.accent),
            ].spacing(9), 17)),
            _ => {}
        }
        container(cards).width(Fill).center_x(Fill).into()
    }
}
