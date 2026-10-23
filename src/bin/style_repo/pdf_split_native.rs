//! Native review of PDF Studio's source-backed Split Document dialog.
//! The twelve-page document is sample data; no PDF files are written here.
use super::Action;
use openaec_ui::{
    iced::{
        self,
        widget::{button, column, container, radio, row, text, text_input, Space},
        Alignment, Element, Fill,
    },
    widgets, Theme,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum SplitMode {
    Pages,
    Bookmarks,
    Size,
}

pub(super) struct SplitReview {
    pub open: bool,
    pub mode: SplitMode,
    pub pages: String,
    pub max_mb: String,
    pub folder: String,
    pub pattern: String,
    pub custom_pattern: bool,
    pub bookmarks: bool,
    pub modified: bool,
    pub notice: Option<&'static str>,
}

impl Default for SplitReview {
    fn default() -> Self {
        Self {
            open: false,
            mode: SplitMode::Pages,
            pages: "1".into(),
            max_mb: "10".into(),
            folder: "/Documenten/Project".into(),
            pattern: "{name}-{n}".into(),
            custom_pattern: false,
            bookmarks: false,
            modified: false,
            notice: None,
        }
    }
}

impl SplitReview {
    pub fn choose_mode(&mut self, mode: SplitMode) {
        if mode == SplitMode::Bookmarks && !self.bookmarks {
            return;
        }
        self.mode = mode;
        if !self.custom_pattern {
            self.pattern = if mode == SplitMode::Bookmarks {
                "{bookmark}"
            } else {
                "{name}-{n}"
            }
            .into();
        }
    }

    pub fn toggle_bookmarks(&mut self, available: bool) {
        self.bookmarks = available;
        if !available && self.mode == SplitMode::Bookmarks {
            self.choose_mode(SplitMode::Pages);
        }
        if available && !self.open && self.mode == SplitMode::Pages {
            self.choose_mode(SplitMode::Bookmarks);
        }
    }

    fn sample_parts(&self) -> Vec<(usize, usize, &'static str)> {
        match self.mode {
            SplitMode::Pages => {
                let step = self
                    .pages
                    .trim()
                    .replace(',', ".")
                    .parse::<f64>()
                    .ok()
                    .filter(|value| value.is_finite())
                    .map(|value| value.round().max(1.0) as usize)
                    .unwrap_or(1);
                (1usize..=12)
                    .step_by(step)
                    .map(|start| {
                        (
                            start,
                            start.saturating_add(step).saturating_sub(1).min(12),
                            "",
                        )
                    })
                    .collect()
            }
            SplitMode::Bookmarks if self.bookmarks => vec![
                (1, 3, "Inleiding"),
                (4, 8, "Constructie"),
                (9, 12, "Bijlagen"),
            ],
            _ => Vec::new(),
        }
    }

    pub fn preview_names(&self) -> Vec<String> {
        let parts = self.sample_parts();
        let digits = parts.len().to_string().len();
        parts
            .iter()
            .enumerate()
            .take(4)
            .map(|(index, (start, end, bookmark))| {
                let mut name = if self.pattern.trim().is_empty() {
                    "{name}-{n}"
                } else {
                    &self.pattern
                }
                .to_owned();
                for (key, value) in [
                    ("{name}", "Project".to_owned()),
                    ("{n}", format!("{:0digits$}", index + 1)),
                    (
                        "{bookmark}",
                        if bookmark.is_empty() {
                            "Project"
                        } else {
                            bookmark
                        }
                        .to_owned(),
                    ),
                    ("{start}", start.to_string()),
                    ("{end}", end.to_string()),
                ] {
                    name = name.replace(key, &value);
                }
                format!("{}.pdf", name.trim())
            })
            .collect()
    }

    pub fn view(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let label = |value: &'static str| text(value).size(11).color(t.dialog_content_text);
        let field = |value: &str, action: fn(String) -> Action, width: f32, enabled: bool| {
            let input = text_input("", value)
                .size(11)
                .padding([3, 6])
                .width(width)
                .style(move |_, status| widgets::text_input_style(theme, status));
            if enabled {
                input.on_input(action)
            } else {
                input
            }
        };
        let choice = |title: &'static str, mode: SplitMode| {
            radio(title, mode, Some(self.mode), Action::PdfSplitMode)
                .size(13)
                .text_size(11)
                .spacing(6)
        };
        let page_choice = row![
            choice("Elke", SplitMode::Pages),
            field(
                &self.pages,
                Action::PdfSplitPages,
                56.0,
                self.mode == SplitMode::Pages
            ),
            label("pagina's")
        ]
        .spacing(6)
        .align_y(Alignment::Center);
        let bookmark_choice = if self.bookmarks {
            row![
                choice("Per bladwijzer op het hoogste niveau", SplitMode::Bookmarks),
                label("(3)")
            ]
        } else {
            row![
                text("○  Per bladwijzer op het hoogste niveau")
                    .size(11)
                    .color(t.text_secondary),
                text("(geen)").size(11).color(t.text_secondary)
            ]
        }
        .spacing(6)
        .align_y(Alignment::Center);
        let size_choice = row![
            choice("Per maximale bestandsgrootte", SplitMode::Size),
            field(
                &self.max_mb,
                Action::PdfSplitSize,
                56.0,
                self.mode == SplitMode::Size
            ),
            label("MB")
        ]
        .spacing(6)
        .align_y(Alignment::Center);
        let group_style = move |_: &iced::Theme| {
            container::Style::default().border(iced::Border {
                color: t.dialog_border,
                width: 1.0,
                radius: 0.0.into(),
            })
        };
        let methods = container(
            column![
                text("Manier van splitsen")
                    .size(11)
                    .color(t.dialog_content_text),
                page_choice,
                bookmark_choice,
                size_choice,
            ]
            .spacing(6),
        )
        .padding([6, 8])
        .width(Fill)
        .style(group_style);
        let output = container(column![
            text("Uitvoer").size(11).color(t.dialog_content_text),
            row![container(label("Map:")).width(90),
                field(&self.folder, Action::PdfSplitFolder, 228.0, true),
                button(label("Bladeren…")).padding([5, 8]).on_press(Action::PdfSplitBrowse)
                    .style(move |_, status| widgets::secondary_button_style(theme, status))]
                .spacing(6).align_y(Alignment::Center),
            row![container(label("Bestandsnamen:")).width(90),
                field(&self.pattern, Action::PdfSplitPattern, 304.0, true)]
                .spacing(6).align_y(Alignment::Center),
            container(text("{name} = documentnaam, {n} = volgnummer, {bookmark} = titel van de bladwijzer, {start} en {end} = paginanummers")
                .size(10).color(t.text_secondary)).padding(iced::Padding { left: 96.0, ..Default::default() }),
        ].spacing(6)).padding([6, 8]).width(Fill).style(group_style);
        let parts = self.sample_parts();
        let mut summary = column![text(if self.mode == SplitMode::Size {
            "Het aantal bestanden hangt af van de grootte en wordt tijdens het splitsen bepaald."
                .to_owned()
        } else {
            format!("Aantal bestanden: {}", parts.len())
        })
        .size(11)
        .color(t.dialog_content_text)]
        .spacing(3);
        for name in self.preview_names() {
            summary = summary.push(text(format!("•  {name}")).size(11).color(t.text_secondary));
        }
        if parts.len() > 4 {
            summary = summary.push(
                text(format!("… en nog {}", parts.len() - 4))
                    .size(11)
                    .color(t.text_secondary),
            );
        }
        let summary = container(summary)
            .padding([6, 8])
            .width(Fill)
            .style(move |_| {
                container::Style::default()
                    .background(t.dialog_sidebar_bg)
                    .border(iced::Border {
                        color: t.dialog_border,
                        width: 1.0,
                        radius: 0.0.into(),
                    })
            });
        let mut body = column![
            methods,
            output,
            summary,
            text("Elk deel houdt zijn annotaties, bladwijzers, paginalabels en paginadraaiing.")
                .size(10)
                .color(t.text_secondary)
        ]
        .spacing(8);
        if self.modified {
            body = body.push(text("Dit document heeft niet-opgeslagen wijzigingen. Gewijzigde annotaties gaan pas mee als het document is opgeslagen; paginadraaiing, paginalabels en bladwijzers gaan altijd mee.")
            .size(11).color(if theme == Theme::Light { iced::Color::from_rgb8(164, 38, 44) }
                else { iced::Color::from_rgb8(255, 156, 162) }));
        }
        if let Some(notice) = self.notice {
            body = body.push(text(notice).size(11).color(t.accent));
        }
        let body = container(body).padding(15).width(Fill).into();
        let footer = row![
            Space::new().width(Fill),
            widgets::dialog_button("Splitsen", move |_, status| widgets::primary_button_style(
                theme, status
            ))
            .on_press(Action::PdfSplitPreview),
            widgets::dialog_button("Annuleren", move |_, status| {
                widgets::secondary_button_style(theme, status)
            })
            .on_press(Action::PdfSplitOpen(false))
        ]
        .spacing(6)
        .align_y(Alignment::Center)
        .into();
        widgets::dialog_modal(
            "Document splitsen",
            body,
            footer,
            Action::PdfSplitOpen(false),
            460.0,
            theme,
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn preview_follows_the_three_source_modes() {
        let mut state = SplitReview::default();
        assert_eq!(state.preview_names().len(), 4);
        state.pages = "5".into();
        assert_eq!(
            state.preview_names(),
            ["Project-1.pdf", "Project-2.pdf", "Project-3.pdf"]
        );
        state.pages = usize::MAX.to_string();
        assert_eq!(state.preview_names(), ["Project-1.pdf"]);
        state.pages = "1,5".into();
        assert_eq!(state.sample_parts().len(), 6);
        state.toggle_bookmarks(true);
        assert_eq!(state.mode, SplitMode::Bookmarks);
        assert_eq!(
            state.preview_names(),
            ["Inleiding.pdf", "Constructie.pdf", "Bijlagen.pdf"]
        );
        state.choose_mode(SplitMode::Size);
        assert!(state.preview_names().is_empty());
        state.toggle_bookmarks(false);
        state.choose_mode(SplitMode::Bookmarks);
        assert_eq!(state.mode, SplitMode::Size);
    }
}
