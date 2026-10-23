//! Source-pinned Speech screens beyond the first three sidebar routes.
use super::*;
use openaec_ui::iced::widget::{column, row};

fn speech_surface<'a>(
    theme: Theme,
    content: impl Into<Element<'a, Action>>,
) -> Element<'a, Action> {
    let t = theme.tokens();
    container(content)
        .padding(32)
        .width(900)
        .style(move |_| {
            container::Style::default()
                .background(t.bg_lighter)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 8.0.into(),
                })
        })
        .into()
}

impl StyleRepo {
    fn speech_review_notice(&self, theme: Theme) -> Option<Element<'_, Action>> {
        self.speech_notice.map(|notice| {
            text(format!(
                "{notice}: dit is een schermreview zonder gekoppelde Speech-backend."
            ))
            .size(12)
            .color(theme.tokens().accent)
            .into()
        })
    }

    pub(super) fn speech_meeting_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let select = |label: &'static str, value: &'static str, width: f32| {
            column![
                text(label)
                    .font(fonts::STRONG)
                    .size(10)
                    .color(t.text_secondary),
                container(text(value).size(12).color(t.text))
                    .width(width)
                    .padding([9, 12])
                    .style(
                        move |_| container::Style::default().background(t.bg).border(
                            iced::Border {
                                color: t.border,
                                width: 1.0,
                                radius: 3.0.into()
                            }
                        )
                    ),
            ]
            .spacing(6)
        };
        let controls = row![
            select("MODEL", "base", 98.0),
            select("TAAL", "Dutch (Nederlands)", 213.0),
            select("AUTOMATISCH ELKE", "5 min", 150.0),
            select("BACKEND", "Browser fallback", 145.0),
        ]
        .spacing(12)
        .align_y(Alignment::End);
        let record = button(text("Opname starten").font(fonts::STRONG).size(12))
            .padding([10, 16])
            .on_press(Action::SpeechPreview("Vergaderopname"))
            .style(move |_, status| widgets::primary_button_style(theme, status));
        let transport = container(
            row![
                record,
                Space::new().width(Fill).height(1),
                text("base   00:00:00")
                    .font(fonts::MONO)
                    .size(14)
                    .color(t.text)
            ]
            .align_y(Alignment::Center),
        )
        .padding(14)
        .width(545)
        .style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let transcript = container(
            column![
                Icon::Microphone.view(38, t.text_secondary),
                text("Start een opname om het transcript hier te zien.")
                    .size(12)
                    .color(t.text_secondary),
                text("Tip: sla tijdens de opname een segment op om tussentijds te transcriberen.")
                    .size(11)
                    .color(t.text_secondary),
            ]
            .spacing(18)
            .align_x(Alignment::Center),
        )
        .width(545)
        .height(240)
        .align_x(Alignment::Center)
        .align_y(Alignment::Center)
        .style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let microphone = container(
            column![
                text("MICROFOON")
                    .font(fonts::STRONG)
                    .size(10)
                    .color(t.text_secondary),
                text("································")
                    .size(16)
                    .color(t.accent),
                text("Niveau  0%\n\nPiek 0%     Gemiddeld 0%\n\nClipping Nee   Status Uit")
                    .size(11)
                    .color(t.text_secondary),
            ]
            .spacing(18),
        )
        .padding(16)
        .width(230)
        .height(307)
        .style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let mut body = Column::new().spacing(16)
            .push(text("Opnemen & transcriberen").font(fonts::HEADING).size(25).color(t.text))
            .push(text("Neem een vergadering of gesprek op. Audio wordt tijdens de opname in segmenten getranscribeerd.")
                .size(13).color(t.text_secondary))
            .push(controls)
            .push(row![column![transport, text("Klaar om op te nemen").size(12).color(t.text_secondary), transcript]
                .spacing(12), microphone].spacing(20));
        if let Some(notice) = self.speech_review_notice(theme) {
            body = body.push(notice);
        }
        speech_surface(theme, body)
    }

    pub(super) fn speech_mic_test_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let test = button(text("Microfoontest starten").font(fonts::STRONG).size(12))
            .padding([10, 16])
            .on_press(Action::SpeechPreview("Microfoontest"))
            .style(move |_, status| widgets::primary_button_style(theme, status));
        let card = container(
            column![
                row![
                    Icon::Microphone.view(17, t.text),
                    text("Invoerapparaat")
                        .font(fonts::STRONG)
                        .size(13)
                        .color(t.text)
                ]
                .spacing(8)
                .align_y(Alignment::Center),
                container(text("Standaardmicrofoon").size(12).color(t.text))
                    .width(760)
                    .padding(10)
                    .style(
                        move |_| container::Style::default().background(t.bg).border(
                            iced::Border {
                                color: t.border,
                                width: 1.0,
                                radius: 3.0.into()
                            }
                        )
                    ),
                text("Niveau                                                        0%")
                    .size(11)
                    .color(t.text_secondary),
                progress_bar(0.0..=100.0, 0.0)
                    .girth(6)
                    .length(760)
                    .style(move |_| widgets::progress_style(theme)),
                container(
                    text("··········································")
                        .size(18)
                        .color(t.accent)
                )
                .width(760)
                .height(56)
                .align_x(Alignment::Center)
                .align_y(Alignment::Center)
                .style(move |_| container::Style::default().background(t.bg)),
                test,
            ]
            .spacing(16),
        )
        .padding(20)
        .width(800)
        .style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let mut body = Column::new().spacing(18)
            .push(text("Microfoontest").font(fonts::HEADING).size(25).color(t.text))
            .push(text("Controleer of uw microfoon en spraakherkenning werken. Spreek een zin in en bekijk het resultaat.")
                .size(13).color(t.text_secondary))
            .push(card);
        if let Some(notice) = self.speech_review_notice(theme) {
            body = body.push(notice);
        }
        speech_surface(theme, body)
    }

    pub(super) fn speech_models_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let model = |name: &'static str,
                     size: &'static str,
                     description: &'static str,
                     speed: &'static str,
                     accuracy: &'static str,
                     active: bool| {
            let label = if active { "ACTIEF" } else { "Downloaden" };
            container(
                column![
                    row![
                        text(name).font(fonts::STRONG).size(15).color(t.text),
                        text(size).size(11).color(t.text_secondary),
                        text(if active { "ACTIEF" } else { "" })
                            .size(10)
                            .color(t.accent)
                    ]
                    .spacing(10),
                    text(description).size(12).color(t.text_secondary),
                    row![
                        text(format!("SNELHEID  {speed}")).size(10),
                        text(format!("NAUWKEURIGHEID  {accuracy}")).size(10)
                    ]
                    .spacing(20),
                    button(text(label).size(11))
                        .padding([7, 13])
                        .on_press(Action::SpeechPreview(name))
                        .style(move |_, status| {
                            let mut style = widgets::button_style(theme, false, status);
                            style.text_color = t.accent;
                            style.border = iced::Border {
                                color: t.accent,
                                width: 1.0,
                                radius: 4.0.into(),
                            };
                            style
                        }),
                ]
                .spacing(12),
            )
            .padding(16)
            .width(389)
            .height(180)
            .style(move |_| {
                container::Style::default()
                    .background(t.bg)
                    .border(iced::Border {
                        color: if active { t.accent } else { t.border },
                        width: 1.0,
                        radius: 7.0.into(),
                    })
            })
        };
        let mut body = Column::new().spacing(17)
            .push(text("Spraakmodellen").font(fonts::HEADING).size(25).color(t.text))
            .push(text("Download en laad een Whisper-spraakherkenningsmodel. Alle modellen draaien lokaal op uw computer.")
                .size(13).color(t.text_secondary))
            .push(text("Herkenningstaal · Dutch (Nederlands)").size(12).color(t.text))
            .push(row![
                model("tiny", "~75 MB", "Snelste model voor korte spraakopdrachten.", "~10× realtime", "Basis", false),
                model("base", "~142 MB", "Balans tussen snelheid en nauwkeurigheid.", "~7× realtime", "Goed", true),
            ].spacing(14))
            .push(row![
                model("small", "~466 MB", "Betere herkenning van accenten en vaktaal.", "~4× realtime", "Hoog", false),
                model("medium", "~1,5 GB", "Hoge nauwkeurigheid voor professionele transcriptie.", "~2× realtime", "Zeer hoog", false),
            ].spacing(14));
        if let Some(notice) = self.speech_review_notice(theme) {
            body = body.push(notice);
        }
        speech_surface(theme, body)
    }

    pub(super) fn speech_settings_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let tabs = ["Algemeen", "Spraak", "Bediening", "Audio", "Bestanden"];
        let mut tab_row = Row::new().spacing(4);
        for (index, label) in tabs.into_iter().enumerate() {
            tab_row = tab_row.push(
                button(text(label).size(12))
                    .padding([9, 14])
                    .on_press(Action::SpeechSettingsTab(index))
                    .style(move |_, status| {
                        widgets::button_style(theme, self.speech_settings_tab == index, status)
                    }),
            );
        }
        let descriptions = [
            (
                "Interfacetaal",
                "English",
                "Kies de taal van de gebruikersinterface.",
            ),
            (
                "Spraakmodel",
                "base",
                "Kies herkenningstaal, model en transcriptie-instellingen.",
            ),
            (
                "Sneltoetsen",
                "Ctrl + Win / Ctrl + Shift + Space",
                "Configureer opname- en bedieningssneltoetsen.",
            ),
            (
                "Invoerapparaat",
                "Standaardmicrofoon",
                "Kies microfoon en audiofeedback voor opnamen.",
            ),
            (
                "Bestandsverwerking",
                "Lokale bestanden",
                "Configureer opslag en bestandsverwerking.",
            ),
        ];
        let (heading, value, help) = descriptions[self.speech_settings_tab];
        let mut body = Column::new()
            .spacing(20)
            .push(
                text("Instellingen")
                    .font(fonts::HEADING)
                    .size(25)
                    .color(t.text),
            )
            .push(tab_row)
            .push(text(heading).font(fonts::STRONG).size(13).color(t.text))
            .push(
                container(text(value).size(12).color(t.text))
                    .width(560)
                    .padding(11)
                    .style(move |_| {
                        container::Style::default()
                            .background(t.bg)
                            .border(iced::Border {
                                color: t.border,
                                width: 1.0,
                                radius: 3.0.into(),
                            })
                    }),
            )
            .push(text(help).size(12).color(t.text_secondary));
        if let Some(notice) = self.speech_review_notice(theme) {
            body = body.push(notice);
        }
        speech_surface(theme, body)
    }

    pub(super) fn speech_about_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let info = [
            ("Licentie", "Apache-2.0"),
            ("Ontwikkelaar", "OpenAEC Foundation"),
            ("Broncode", "GitHub"),
        ];
        let mut rows = Column::new().spacing(0);
        for (label, value) in info {
            rows = rows.push(
                container(row![
                    container(text(label).size(12).color(t.text_secondary)).width(300),
                    text(value).size(12).color(t.accent),
                ])
                .padding([11, 16])
                .width(520)
                .style(move |_| {
                    container::Style::default()
                        .background(t.bg)
                        .border(iced::Border {
                            color: t.border,
                            width: 1.0,
                            radius: 2.0.into(),
                        })
                }),
            );
        }
        speech_surface(theme, column![
            row![Icon::Microphone.view(48, t.accent),
                column![text("Open Speech Studio").font(fonts::HEADING).size(25).color(t.text),
                    text("v0.5.0 · broncapture").size(12).color(t.text_secondary)]
                    .spacing(5)].spacing(18).align_y(Alignment::Center),
            text("Open-source spraak-naar-tekstapplicatie. De bronapp verwerkt audio lokaal op uw computer.")
                .size(13).color(t.text_secondary),
            rows,
            text("© 2025 OpenAEC Foundation").size(11).color(t.text_secondary),
        ].spacing(24))
    }

    pub(super) fn speech_tts_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let input = text_input("Typ tekst om uit te spreken…", &self.speech_tts_text)
            .on_input(Action::SpeechTtsInput)
            .padding([12, 14])
            .width(760)
            .style(move |_, status| widgets::text_input_style(theme, status));
        let speed = iced::widget::slider(0.5..=2.0, self.speech_tts_speed, Action::SpeechTtsSpeed)
            .width(280)
            .style(move |_, status| widgets::slider_style(theme, status));
        let speak = button(text("Spreek tekst uit").font(fonts::STRONG).size(12))
            .padding([10, 16])
            .on_press(Action::SpeechPreview("Tekst naar spraak"))
            .style(move |_, status| widgets::primary_button_style(theme, status));
        let library = container(
            column![
                text("Stemmenbibliotheek")
                    .font(fonts::STRONG)
                    .size(16)
                    .color(t.text),
                text("De bronapp toont hier lokaal beschikbare Piper-stemmen en downloadopties.")
                    .size(12)
                    .color(t.text_secondary),
                text("Geen stem geladen in deze schermreview.")
                    .size(12)
                    .color(t.text_secondary),
            ]
            .spacing(14),
        )
        .padding(18)
        .width(800)
        .style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let mut body = Column::new()
            .spacing(21)
            .push(
                text("Tekst naar spraak")
                    .font(fonts::HEADING)
                    .size(25)
                    .color(t.text),
            )
            .push(
                text(
                    "Piper maakt spraak lokaal. Kies een stem, stel het tempo in en voer tekst in.",
                )
                .size(13)
                .color(t.text_secondary),
            )
            .push(
                text("Stem · geen gedownloade stem beschikbaar")
                    .size(12)
                    .color(t.text),
            )
            .push(
                row![
                    text("Snelheid").size(12).color(t.text),
                    speed,
                    text(format!("{:.2}×", self.speech_tts_speed))
                        .size(12)
                        .color(t.text)
                ]
                .spacing(16)
                .align_y(Alignment::Center),
            )
            .push(input)
            .push(speak)
            .push(library);
        if let Some(notice) = self.speech_review_notice(theme) {
            body = body.push(notice);
        }
        speech_surface(theme, body)
    }
}
