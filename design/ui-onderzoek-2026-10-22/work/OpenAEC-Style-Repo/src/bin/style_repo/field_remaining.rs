//! Field routes without repository screenshots, reconstructed from pinned HTML and app code.
use super::*;
use openaec_ui::iced::widget::{column, row};

impl StyleRepo {
    pub(super) fn field_upload_page(
        &self,
        theme: Theme,
        l: Language,
        ifc: bool,
    ) -> Element<'_, Action> {
        let t = theme.tokens();
        let title = if ifc {
            "3D BIM (IFC-viewer)"
        } else {
            "Plattegronden"
        };
        let prompt = if ifc {
            "Sleep een .ifc-bestand hierheen of klik om te uploaden"
        } else {
            "Sleep plattegronden hierheen of klik om te uploaden"
        };
        let hint = if ifc {
            "IFC 2x3 / IFC4"
        } else {
            "JPG, PNG, PDF"
        };
        let upload = button(
            column![
                Icon::Import.view(44, t.accent),
                text(prompt).size(14).color(t.text),
                text(hint).size(12).color(t.text_secondary),
            ]
            .spacing(12)
            .width(Fill)
            .align_x(Alignment::Center),
        )
        .width(1104)
        .height(190)
        .padding(20)
        .on_press(Action::FieldReviewPreview(if ifc {
            "IFC-import"
        } else {
            "Plattegrond-import"
        }))
        .style(move |_, status| {
            let mut style = widgets::button_style(theme, false, status);
            style.border = iced::Border {
                color: t.border,
                width: 1.0,
                radius: 8.0.into(),
            };
            style
        });
        let mut body = Column::new()
            .spacing(20)
            .push(text(title).font(fonts::HEADING).size(29).color(t.text))
            .push(upload);
        if ifc {
            let canvas_ink = iced::Color::from_rgb8(0xb9, 0xbb, 0xc5);
            body = body.push(container(column![
                Icon::Cube.view(52, canvas_ink),
                text("Nog geen IFC-model geladen").size(14).color(canvas_ink),
            ].spacing(14).align_x(Alignment::Center))
                .width(1104).height(350).center_x(Fill).center_y(iced::Length::Fixed(350.0))
                .style(|_| container::Style::default()
                    .background(iced::Color::from_rgb8(0x1a, 0x1a, 0x20))
                    .border(iced::Border::default().rounded(8))))
                .push(text("Muis: linksklik+sleep = draaien · scroll = zoomen · rechtsklik+sleep = pannen. Ticket-koppeling op 3D-model volgt later.")
                    .size(12).color(t.text_secondary));
        } else {
            body = body.push(
                text("Er zijn nog geen plattegronden geladen.")
                    .size(13)
                    .color(t.text_secondary),
            );
        }
        if let Some(notice) = self.field_review_notice {
            body = body.push(
                text(format!(
                    "{notice}: bestand kiezen is in deze schermreview nog niet gekoppeld."
                ))
                .size(12)
                .color(t.accent),
            );
        }
        let panel = container(body).padding(32).width(1168).style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 10.0.into(),
                })
        });
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            panel,
            text(l.text("Indeling afgeleid uit index.html op commit 8a4f104; geen repositoryscreenshot beschikbaar.",
                "Layout derived from index.html at commit 8a4f104; no repository screenshot available."))
                .size(12).color(t.text_secondary),
        ].spacing(16).into()
    }

    pub(super) fn field_capture_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let filter = |group: usize, choices: Vec<&'static str>| {
            let current = self.field_capture_filter[group].min(choices.len() - 1);
            let selected = Some(choices[current].to_string());
            let names: Vec<String> = choices.iter().map(|choice| (*choice).to_string()).collect();
            let selected_names = names.clone();
            pick_list(names, selected, move |name| {
                Action::FieldCaptureFilter(
                    group,
                    selected_names
                        .iter()
                        .position(|choice| choice == &name)
                        .unwrap_or(0),
                )
            })
            .width(180)
            .style(move |_, status| widgets::pick_list_style(theme, status))
            .menu_style(move |_| widgets::pick_list_menu_style(theme))
        };
        let selectors = row![
            text("Plattegrond:")
                .font(fonts::MEDIUM)
                .size(12)
                .color(t.text),
            container(
                text("— Kies een plattegrond —")
                    .size(12)
                    .color(t.text_secondary)
            )
            .width(230)
            .padding(9)
            .style(move |_| container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 2.0.into()
                })),
            filter(
                0,
                vec![
                    "Alle statussen",
                    "Open",
                    "Toegewezen",
                    "Afgerond",
                    "Geverifieerd"
                ]
            ),
            filter(1, vec!["Alle categorieën"]),
            filter(2, vec!["Alle prioriteiten", "Hoog", "Midden", "Laag"]),
        ]
        .spacing(10)
        .align_y(Alignment::Center);
        let canvas = container(
            column![
                Icon::Grid.view(60, t.text_secondary),
                text("Selecteer een plattegrond om tickets toe te voegen")
                    .size(14)
                    .color(t.text_secondary),
            ]
            .spacing(14)
            .align_x(Alignment::Center),
        )
        .width(820)
        .height(408)
        .center_x(Fill)
        .center_y(iced::Length::Fixed(408.0))
        .style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 8.0.into(),
                })
        });
        let mut toolbar = Row::new().spacing(8);
        for (label, icon) in [
            ("Ticket toevoegen", Icon::New),
            ("Inzoomen", Icon::ZoomIn),
            ("Uitzoomen", Icon::ZoomOut),
            ("Passend maken", Icon::Fit),
        ] {
            toolbar = toolbar.push(
                button(
                    row![icon.view(16, t.text), text(label).size(11)]
                        .spacing(6)
                        .align_y(Alignment::Center),
                )
                .padding([8, 10])
                .on_press(Action::FieldReviewPreview(label))
                .style(move |_, state| widgets::button_style(theme, false, state)),
            );
        }
        let canvas_area = column![canvas, toolbar].spacing(10);
        let points = container(
            column![
                text("Tickets  0")
                    .font(fonts::STRONG)
                    .size(16)
                    .color(t.text),
                container(
                    text("Nog geen tickets toegevoegd")
                        .size(12)
                        .color(t.text_secondary)
                )
                .width(Fill)
                .height(240)
                .center_x(Fill)
                .align_y(Alignment::Center),
            ]
            .spacing(20),
        )
        .padding(20)
        .width(260)
        .height(460)
        .style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 8.0.into(),
                })
        });
        let mut content = Column::new()
            .spacing(18)
            .push(selectors)
            .push(row![canvas_area, points].spacing(24));
        if let Some(notice) = self.field_review_notice {
            content = content.push(text(format!("{notice}: voeg eerst een plattegrond toe; deze schermreview bevat geen projectdata."))
                .size(12).color(t.accent));
        }
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            content,
            text(l.text("Opname-indeling afgeleid uit index.html op commit 8a4f104; geen repositoryscreenshot beschikbaar.",
                "Capture layout derived from index.html at commit 8a4f104; no repository screenshot available."))
                .size(12).color(t.text_secondary),
        ].spacing(18).into()
    }

    pub(super) fn field_manual_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        // Condensed from src/locales/nl.json:manual_html on the pinned Field commit.
        let sections = [
            ("1. Project & Contacten", "Projectgegevens en contacten vastleggen; gegevens worden automatisch opgeslagen."),
            ("2. Plattegronden", "JPG, PNG en PDF toevoegen; PDF-pagina’s worden afzonderlijk verwerkt."),
            ("3. Opname & Tickets", "Gebreken op de plattegrond plaatsen en filteren op status, categorie en prioriteit."),
            ("4. Inspectie", "Checklists uitvoeren met algemene of NEN 2767-templates en digitaal ondertekenen."),
            ("5. Oplevering", "Open tickets beoordelen, documenten toevoegen en het proces-verbaal ondertekenen."),
            ("6. Dashboard", "Tickets, deadlines, inspecties en activiteit in één overzicht volgen."),
            ("7. Export & Opslag", "Rapporten exporteren en projecten als JSON opslaan of laden."),
            ("8. Sneltoetsen", "Ctrl+S opslaan · Ctrl+E export · Ctrl+O laden · Ctrl+D thema · Escape sluiten."),
        ];
        let mut body = Column::new().spacing(22)
            .push(text(l.text("Handleiding", "Manual")).font(fonts::HEADING).size(29).color(t.text))
            .push(text("Welkom bij Open Field Studio — uw tool voor inspectie, oplevering en kwaliteitsborging bij bouwprojecten.")
                .size(13).color(t.text_secondary));
        for (heading, description) in sections {
            body = body.push(
                column![
                    text(heading).font(fonts::STRONG).size(16).color(t.text),
                    text(description).size(13).color(t.text_secondary),
                ]
                .spacing(7),
            );
        }
        let panel = container(body).padding(32).width(1168).style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 10.0.into(),
                })
        });
        column![
            text("OPEN FIELD STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG).size(11).color(t.accent),
            panel,
            text("Inhoud samengevat uit src/locales/nl.json:manual_html · commit 8a4f104; geen repositoryscreenshot beschikbaar.")
                .size(12).color(t.text_secondary),
        ].spacing(16).into()
    }
}
