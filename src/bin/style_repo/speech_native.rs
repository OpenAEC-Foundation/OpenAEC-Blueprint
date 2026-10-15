//! Native sidebar-screen reviews for Open Speech Studio.
use super::*;
use openaec_ui::iced::widget::{column, row};

impl StyleRepo {
    pub(super) fn speech_native_page(
        &self,
        theme: Theme,
        _l: Language,
        screen: &str,
    ) -> Element<'_, Action> {
        let t = theme.tokens();
        let content: Element<'_, Action> = match screen {
            "speech" => self.speech_home(theme),
            "transcribe" => self.speech_transcribe(theme),
            "dictionary" => self.speech_dictionary_page(theme),
            _ => unreachable!("routed Speech screen"),
        };
        let capture = match screen {
            "speech" => "Speech.png",
            "transcribe" => "Transcribe.png",
            "dictionary" => "Dictionary.png",
            _ => unreachable!("routed Speech capture"),
        };
        let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("harmonization/references/open-speech-studio/Socials")
            .join(capture);
        column![
            text("OPEN SPEECH STUDIO · NATIVE RUST SCHERMREVIEW")
                .font(fonts::STRONG)
                .size(11)
                .color(t.accent),
            content,
            text("Broncapture ter vergelijking · commit 4e8aa61")
                .font(fonts::MEDIUM)
                .size(12)
                .color(t.text_secondary),
            image(image::Handle::from_path(path)).width(900),
        ]
        .spacing(16)
        .into()
    }

    fn speech_home(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let banner = container(text("Open Speech Studio is actief — houd Ctrl + Win / Ctrl + Shift + Space ingedrukt om te spreken")
            .font(fonts::STRONG).size(12).color(iced::Color::WHITE))
            .padding([11, 16]).width(900)
            .style(move |_| container::Style::default().background(t.accent));
        let microphone = container(Icon::Microphone.view(42, t.accent))
            .width(74)
            .height(74)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
            .style(move |_| {
                container::Style::default()
                    .background(t.accent_soft)
                    .border(iced::Border::default().rounded(37))
            });
        let start = button(text("Ctrl + Win / Ctrl + Shift + Space").size(12))
            .padding([10, 16])
            .on_press(Action::SpeechPreview("Spraakopname"))
            .style(move |_, status| widgets::button_style(theme, false, status));
        let mut center = Column::new()
            .spacing(19)
            .align_x(Alignment::Center)
            .push(microphone)
            .push(
                text("Klaar om te spreken")
                    .font(fonts::HEADING)
                    .size(24)
                    .color(t.text),
            )
            .push(
                text("Druk op de sneltoets om te starten. Uw stem wordt lokaal verwerkt.")
                    .size(13)
                    .color(t.text_secondary),
            )
            .push(start);
        if let Some(notice) = self.speech_notice {
            center = center.push(
                text(format!(
                    "{notice}: opname vereist de Speech-backend en is hier niet gekoppeld."
                ))
                .size(12)
                .color(t.accent),
            );
        }
        let body = container(center)
            .width(900)
            .height(460)
            .align_x(Alignment::Center)
            .align_y(Alignment::Center)
            .style(move |_| {
                container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border {
                        color: t.border,
                        width: 1.0,
                        radius: 8.0.into(),
                    })
            });
        column![banner, body].spacing(0).into()
    }

    fn speech_transcribe(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let drop = button(
            column![
                Icon::Import.view(36, t.accent),
                text("Sleep audio- of videobestanden hierheen of klik om te kiezen")
                    .size(13)
                    .color(t.text),
                text("WAV, MP3, FLAC, OGG, M4A, MP4, MKV, AVI, MOV en meer")
                    .size(11)
                    .color(t.text_secondary),
            ]
            .spacing(16)
            .width(Fill)
            .align_x(Alignment::Center),
        )
        .width(800)
        .height(175)
        .padding(22)
        .on_press(Action::SpeechPreview("Bestandsselectie"))
        .style(move |_, status| {
            let mut style = widgets::button_style(theme, false, status);
            style.border = iced::Border {
                color: t.accent,
                width: 1.0,
                radius: 7.0.into(),
            };
            style
        });
        let mut body = Column::new().spacing(17)
            .push(text("Bestanden transcriberen").font(fonts::HEADING).size(25).color(t.text))
            .push(text("Transcribeer audio- of videobestanden. Meerdere bestanden worden parallel verwerkt; de verwerking blijft lokaal.")
                .size(13).color(t.text_secondary))
            .push(drop);
        if let Some(notice) = self.speech_notice {
            body = body.push(
                text(format!(
                    "{notice}: deze schermreview opent nog geen lokale bestanden."
                ))
                .size(12)
                .color(t.accent),
            );
        }
        container(body)
            .padding(32)
            .width(900)
            .height(430)
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

    fn speech_dictionary_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let word = text_input("Woord (bijv. OpenAEC)", &self.speech_word)
            .on_input(|value| Action::SpeechDictionaryEdit(true, value))
            .padding([10, 12])
            .width(310)
            .style(move |_, status| widgets::text_input_style(theme, status));
        let replacement = text_input("Vervanging (optioneel)", &self.speech_replacement)
            .on_input(|value| Action::SpeechDictionaryEdit(false, value))
            .padding([10, 12])
            .width(310)
            .style(move |_, status| widgets::text_input_style(theme, status));
        let add = button(text("Toevoegen").size(12))
            .padding([10, 15])
            .on_press(Action::SpeechDictionaryAdd)
            .style(move |_, status| widgets::primary_button_style(theme, status));
        let mut entries = Column::new().spacing(10).push(
            row![
                container(
                    text("WOORD")
                        .font(fonts::STRONG)
                        .size(10)
                        .color(t.text_secondary)
                )
                .width(300),
                text("VERVANGING")
                    .font(fonts::STRONG)
                    .size(10)
                    .color(t.text_secondary),
            ]
            .spacing(10),
        );
        if self.speech_dictionary.is_empty() {
            entries = entries.push(
                container(
                    text("Nog geen woorden toegevoegd")
                        .size(12)
                        .color(t.text_secondary),
                )
                .height(80)
                .width(Fill)
                .align_x(Alignment::Center)
                .align_y(Alignment::Center),
            );
        } else {
            for (word, replacement) in &self.speech_dictionary {
                entries = entries.push(
                    row![
                        container(text(word.clone()).size(12).color(t.text)).width(300),
                        text(replacement.clone()).size(12).color(t.text),
                    ]
                    .spacing(10),
                );
            }
        }
        let table = container(entries).padding(16).width(800).style(move |_| {
            container::Style::default()
                .background(t.bg)
                .border(iced::Border {
                    color: t.border,
                    width: 1.0,
                    radius: 7.0.into(),
                })
        });
        let body = column![
            text("Woordenboek").font(fonts::HEADING).size(25).color(t.text),
            text("Voeg woorden toe die het spraakmodel moet herkennen, zoals namen, afkortingen of vaktaal.")
                .size(13).color(t.text_secondary),
            row![word, replacement, add].spacing(10).align_y(Alignment::Center),
            table,
            text("Dit woordenboek is alleen een sessievoorbeeld in de Style Repo.")
                .size(11).color(t.text_secondary),
        ].spacing(20);
        container(body)
            .padding(32)
            .width(900)
            .height(430)
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
}
