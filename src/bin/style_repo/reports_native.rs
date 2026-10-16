//! Source-pinned native layout review of OpenAEC Reports screen destinations.
use super::*;
use openaec_ui::iced::widget::{column, row};

#[derive(Deserialize)]
pub(super) struct ReportsData {
    pub routes: Vec<ReportEntry>,
    pub admin_tabs: Vec<ReportEntry>,
    pub preview_states: Vec<ReportEntry>,
    pub sample: ReportSample,
}
#[derive(Deserialize)]
pub(super) struct ReportEntry {
    pub id: String,
    pub label: String,
    #[serde(default)]
    pub category: String,
    #[serde(default)]
    pub note: String,
    pub evidence: ReportEvidence,
}
#[derive(Deserialize)]
pub(super) struct ReportEvidence {
    pub file: String,
    pub line: usize,
}
#[derive(Deserialize)]
pub(super) struct ReportSample {
    pub project: String,
    pub number: String,
    pub status: String,
    pub sections: Vec<String>,
}
pub(super) fn data() -> &'static ReportsData {
    static DATA: OnceLock<ReportsData> = OnceLock::new();
    DATA.get_or_init(|| serde_json::from_str(include_str!("../../../harmonization/reports-screen-routes.json"))
        .expect("valid source-pinned Reports inventory"))
}

impl StyleRepo {
    pub(super) fn reports_sidebar(&self, theme: Theme) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        let mut nav = Column::new().spacing(4)
            .push(text(&d.sample.project).font(fonts::STRONG).size(14).color(t.text))
            .push(text(format!("{} · {}", d.sample.number, d.sample.status)).size(11).color(t.text_secondary))
            .push(Space::with_height(10));
        for (heading, ids) in [
            ("Document", &["rapport", "voorblad", "colofon", "opties"][..]),
            ("Template", &["field-group"][..]),
            ("Hoofdstukken", &["section"][..]),
            ("Bijlagen", &["appendix"][..]),
        ] {
            nav = nav.push(text(heading.to_uppercase()).font(fonts::STRONG).size(10).color(t.text_secondary));
            for id in ids {
                let (index, route) = d.routes.iter().enumerate().find(|(_, route)| route.id == *id).unwrap();
                nav = nav.push(button(text(&route.label).size(11)).padding([7, 9]).width(Fill)
                    .on_press(Action::SelectReportsRoute(index))
                    .style(move |_, status| widgets::button_style(theme, self.reports_route == index, status)));
            }
            if heading == "Hoofdstukken" {
                for (number, section) in d.sample.sections.iter().enumerate() {
                    let index = d.routes.iter().position(|route| route.id == "section").unwrap();
                    nav = nav.push(button(text(format!("  {}. {}", number + 1, section)).size(10))
                        .padding([5, 9]).width(Fill).on_press(Action::SelectReportsRoute(index))
                        .style(move |_, status| widgets::button_style(theme, self.reports_route == index && number == 0, status)));
                }
            }
            nav = nav.push(Space::with_height(8));
        }
        container(nav).padding(12).width(Fill).into()
    }

    pub(super) fn reports_native_page(&self, theme: Theme, _l: Language) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        let route = &d.routes[self.reports_route];
        let mut route_groups = Column::new().spacing(5);
        for category in ["access", "primary", "editor", "mode"] {
            let mut buttons = Row::new().spacing(4);
            for (index, item) in d.routes.iter().enumerate().filter(|(_, item)| item.category == category) {
                buttons = buttons.push(button(text(&item.label).size(10)).padding([5, 7])
                    .on_press(Action::SelectReportsRoute(index))
                    .style(move |_, status| widgets::button_style(theme, self.reports_route == index, status)));
            }
            route_groups = route_groups.push(scrollable(buttons).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())));
        }
        let sidebar: Element<'_, Action> = if matches!(route.id.as_str(), "loading" | "sso" | "projects" | "admin") {
            Space::new(0, 0).into()
        } else {
            button(text(if self.reports_sidebar_visible { "Zijbalk verbergen" } else { "Zijbalk tonen" }).size(11))
                .padding([6, 9]).on_press(Action::ToggleReportsSidebar)
                .style(move |_, status| widgets::button_style(theme, self.reports_sidebar_visible, status)).into()
        };
        let header = row![
            column![
                text("OPENAEC REPORTS · NATIVE RUST SCHERMREVIEW").font(fonts::STRONG).size(10).color(t.accent),
                text(&route.label).font(fonts::HEADING).size(23).color(t.text),
                text(&route.note).size(11).color(t.text_secondary),
            ].spacing(4).width(Fill),
            sidebar,
        ].spacing(12).align_y(Alignment::Center);
        let body = self.reports_body(theme, &route.id);
        column![
            header,
            self.reports_surface(theme, route_groups, 8),
            body,
            text(format!("BRON · {}:{} · commit 818e581", route.evidence.file, route.evidence.line))
                .size(10).color(t.text_secondary),
            text("Stijlproef met voorbeelddata. Geen live SSO, API of PDF-renderer; geen broncapture voor pixelvergelijking.")
                .size(10).color(t.text_secondary),
        ].spacing(12).width(Fill).into()
    }

    fn reports_body(&self, theme: Theme, id: &str) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        match id {
            "loading" | "sso" => self.reports_surface(theme, column![
                text(if id == "loading" { "Sessie laden…" } else { "Doorsturen naar SSO…" })
                    .font(fonts::HEADING).size(21).color(t.text),
                text(if id == "loading" { "De sessiestatus wordt gecontroleerd." } else { "Lokale fallback voor authenticatie." })
                    .size(12).color(t.text_secondary),
            ].spacing(12), 28),
            "projects" => {
                let left = self.reports_surface(theme, column![
                    text("PROJECTEN").font(fonts::STRONG).size(11).color(t.accent),
                    text("Alle rapporten").size(12),
                    text(&d.sample.project).size(12),
                ].spacing(16), 16);
                let right = self.reports_surface(theme, column![
                    text("Alle rapporten").font(fonts::HEADING).size(17),
                    text("TITEL                                  TEMPLATE             STATUS").size(10).color(t.text_secondary),
                    text(format!("{}            structural              {}", d.sample.project, d.sample.status)).size(11),
                ].spacing(17), 16);
                row![container(left).width(288), container(right).width(Fill)].spacing(2).into()
            }
            "admin" => {
                let mut tabs = Row::new().spacing(4);
                for (index, tab) in d.admin_tabs.iter().enumerate() {
                    tabs = tabs.push(button(text(&tab.label).size(11)).padding([7, 8])
                        .on_press(Action::SelectReportsAdminTab(index))
                        .style(move |_, status| widgets::button_style(theme, self.reports_admin_tab == index, status)));
                }
                let active = &d.admin_tabs[self.reports_admin_tab];
                self.reports_surface(theme, column![
                    text("Beheer").font(fonts::HEADING).size(18),
                    scrollable(tabs).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())),
                    text(&active.label).font(fonts::STRONG).size(14).color(t.accent),
                    text("Account- en servergegevens zijn in deze bronreview niet beschikbaar.").size(11).color(t.text_secondary),
                    text(format!("{}:{}", active.evidence.file, active.evidence.line)).size(10).color(t.text_secondary),
                ].spacing(14), 18)
            }
            "json" => self.reports_surface(theme, column![
                text("JSON-editor").font(fonts::HEADING).size(18),
                text("Toepassen    Formatteren").size(11).color(t.accent),
                text(format!("{{\n  \"project\": \"{}\",\n  \"template\": \"structural\",\n  \"sections\": [ … ]\n}}", d.sample.project))
                    .font(fonts::MONO).size(12),
            ].spacing(13), 18),
            "split" => row![
                container(self.reports_editor(theme, "section")).width(iced::FillPortion(1)),
                container(self.reports_pdf(theme)).width(iced::FillPortion(1)),
            ].spacing(2).width(Fill).into(),
            "preview" => self.reports_pdf(theme),
            _ => self.reports_editor(theme, id),
        }
    }

    fn reports_editor(&self, theme: Theme, id: &str) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        let title = d.routes.iter().find(|route| route.id == id).map(|route| route.label.as_str()).unwrap_or("Editor");
        let mut content = Column::new().spacing(12)
            .push(text(title).font(fonts::HEADING).size(18).color(t.text));
        if id == "section" {
            content = content
                .push(self.reports_line(theme, &format!("1. {}", d.sample.sections[0]), "Hoofdstuk met versleepbare inhoudsblokken"))
                .push(self.reports_line(theme, "Tekstblok", "Beschrijving van de constructieve uitgangspunten"))
                .push(self.reports_line(theme, "Berekening", "Bloktype uit de broneditor · voorbeeldinhoud"))
                .push(button(text("+ Voeg tekst, berekening of tabel toe").size(11))
                    .padding([8, 10]).style(move |_, status| widgets::button_style(theme, false, status)));
        } else if id == "appendix" {
            content = content.push(self.reports_line(theme, "Bijlage A", "Bijlage-editor met eigen inhoudsblokken"));
        } else {
            let fields: &[(&str, &str)] = match id {
                "rapport" => &[("Project", &d.sample.project), ("Projectnummer", &d.sample.number), ("Template", "structural"), ("Status", &d.sample.status), ("Versie", "1.0")],
                "voorblad" => &[("Titel", &d.sample.project), ("Subtitel", "Constructieve berekening hoofddraagconstructie"), ("Afbeelding", "renders/…")],
                "colofon" => &[("Ingeschakeld", "Ja"), ("Revisie", "0.1"), ("Opsteller", "Default Author")],
                "opties" => &[("Inhoudsopgave", "Aan"), ("Maximaal niveau", "3"), ("Papierformaat", "A4")],
                _ => &[("Formuliergroep", "Projectgegevens"), ("Veldtype", "Template-afhankelijk")],
            };
            for (label, value) in fields {
                content = content.push(column![
                    text(*label).size(10).color(t.text_secondary),
                    container(text(*value).size(12)).padding([7, 9]).width(Fill)
                        .style(move |_| container::Style::default().background(t.content_bg).border(iced::Border::default().color(t.border).width(1))),
                ].spacing(4));
            }
        }
        self.reports_surface(theme, content, 18)
    }

    fn reports_pdf(&self, theme: Theme) -> Element<'_, Action> {
        let d = data();
        let t = theme.tokens();
        let mut states = Row::new().spacing(4);
        for (index, entry) in d.preview_states.iter().enumerate() {
            states = states.push(button(text(&entry.label).size(10)).padding([5, 7])
                .on_press(Action::SelectReportsPdfState(index))
                .style(move |_, status| widgets::button_style(theme, self.reports_pdf_state == index, status)));
        }
        let page: Element<'_, Action> = if self.reports_pdf_state == 2 {
            container(container(column![
                text(format!("{} · {}", d.sample.number, d.sample.status)).size(9).color(iced::Color::from_rgb8(111, 117, 127)),
                Space::with_height(52),
                text(&d.sample.project).font(fonts::HEADING).size(18).color(iced::Color::from_rgb8(52, 56, 64)),
                text("Constructieve berekening hoofddraagconstructie").size(11).color(iced::Color::from_rgb8(111, 117, 127)),
                Space::with_height(160),
            ].spacing(15)).padding(20).width(360)
                .style(move |_| container::Style::default().background(iced::Color::WHITE).border(iced::Border::default().color(iced::Color::from_rgb8(210, 213, 218)).width(1))))
                .width(Fill).align_x(Alignment::Center).into()
        } else {
            container(text(if self.reports_pdf_state == 0 { "Geen verbinding met API server" } else { "Nog geen PDF gegenereerd" })
                .size(12).color(t.text_secondary)).padding(24).into()
        };
        self.reports_surface(theme, column![
            row![text("Auto-preview · Pagina 1").size(11).color(t.text), Space::with_width(Fill), text("Regenereer").size(11).color(t.accent)],
            scrollable(states).direction(scrollable::Direction::Horizontal(scrollable::Scrollbar::new())),
            page,
        ].spacing(12), 14)
    }

    fn reports_line<'a>(&self, theme: Theme, title: &str, detail: &str) -> Element<'a, Action> {
        let t = theme.tokens();
        container(column![
            text(title.to_owned()).font(fonts::STRONG).size(12),
            text(detail.to_owned()).size(11).color(t.text_secondary),
        ].spacing(6)).padding(12).width(Fill)
            .style(move |_| container::Style::default().background(t.content_bg).border(iced::Border::default().color(t.border).width(1))).into()
    }

    fn reports_surface<'a>(&self, theme: Theme, content: impl Into<Element<'a, Action>>, padding: u16) -> Element<'a, Action> {
        let t = theme.tokens();
        container(content).padding(padding).width(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter).border(iced::Border::default().color(t.border).width(1))).into()
    }
}
