//! Source-data-backed budget grid review for Open Calc Studio.
use super::*;
use openaec_ui::iced::widget::{column, mouse_area};
use serde_json::Value;

fn sample() -> &'static Value {
    static SAMPLE: OnceLock<Value> = OnceLock::new();
    SAMPLE.get_or_init(|| {
        serde_json::from_str(include_str!(
            "../../../harmonization/references/open-calc-studio/public/data/voorbeeld.ifcCalc"
        ))
        .expect("valid pinned Calc sample")
    })
}

pub(super) fn items() -> &'static Vec<Value> {
    sample()["items"].as_array().expect("sample items")
}

fn field<'a>(item: &'a Value, key: &str) -> &'a str {
    item[key].as_str().unwrap_or("")
}

fn number(item: &Value, key: &str) -> String {
    item[key]
        .as_f64()
        .map(|value| format!("{value:.2}").replace('.', ","))
        .unwrap_or_default()
}

fn calc_cell<'a>(
    label: impl Into<String>,
    width: u16,
    theme: Theme,
    prominent: bool,
) -> Element<'a, Action> {
    let t = theme.tokens();
    container(
        text(label.into())
            .size(10)
            .color(if prominent { t.text } else { t.text_secondary }),
    )
    .width(u32::from(width))
    .height(29)
    .padding([7, 6])
    .into()
}

impl StyleRepo {
    pub(super) fn calc_native_page(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let headings = [
            ("ID", 35),
            ("Type", 75),
            ("Hst", 45),
            ("Nr", 72),
            ("Omschrijving", 310),
            ("Aantal", 72),
            ("Eenheid", 60),
            ("Prijs", 75),
            ("Norm", 72),
            ("Uren", 65),
            ("Loon", 82),
            ("Materiaal", 92),
            ("Totaal", 92),
        ];
        let mut heading_row = Row::new().spacing(0);
        for (label, width) in headings {
            heading_row = heading_row.push(calc_cell(label, width, theme, true));
        }
        let mut rows = Column::new()
            .spacing(0)
            .push(container(heading_row).width(1147).style(move |_| {
                container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border::default().color(t.border).width(1))
            }));
        for (index, item) in items().iter().enumerate() {
            let kind = field(item, "rowType");
            let depth = item["depth"].as_u64().unwrap_or(0);
            let mut row = Row::new().spacing(0);
            let values = [
                ((index + 1).to_string(), 35),
                (
                    match kind {
                        "chapter" => "HOOFD",
                        "begrotingspost" => "BGRPS",
                        "regel" => "REGEL",
                        _ => kind,
                    }
                    .to_string(),
                    75,
                ),
                (
                    if kind == "chapter" {
                        field(item, "code")
                    } else {
                        ""
                    }
                    .to_string(),
                    45,
                ),
                (field(item, "code").to_string(), 72),
                (
                    format!(
                        "{}{}{}",
                        "  ".repeat(depth as usize),
                        if kind == "chapter" { "▾ " } else { "" },
                        field(item, "description")
                    ),
                    310,
                ),
                (number(item, "quantity"), 72),
                (field(item, "unit").to_string(), 60),
                (number(item, "unitPrice"), 75),
                (String::new(), 72),
                (
                    if field(item, "resourceType") == "arbeid" {
                        number(item, "quantity")
                    } else {
                        String::new()
                    },
                    65,
                ),
                (
                    if field(item, "resourceType") == "arbeid" {
                        number(item, "total")
                    } else {
                        String::new()
                    },
                    82,
                ),
                (
                    if field(item, "resourceType") == "materiaal" {
                        number(item, "total")
                    } else {
                        String::new()
                    },
                    92,
                ),
                (number(item, "total"), 92),
            ];
            for (value, width) in values {
                row = row.push(calc_cell(value, width, theme, kind == "chapter"));
            }
            let selected = self.calc_selected_row == index;
            let background = if selected {
                t.accent_soft
            } else if kind == "chapter" {
                t.bg_lighter
            } else {
                t.bg
            };
            rows = rows.push(
                mouse_area(container(row).width(1147).style(move |_| {
                    container::Style::default()
                        .background(background)
                        .border(iced::Border::default().color(t.border).width(0.5))
                }))
                .on_press(Action::CalcSelectRow(index)),
            );
        }
        let table = scrollable::Scrollable::with_direction(
            rows,
            scrollable::Direction::Both {
                vertical: scrollable::Scrollbar::new(),
                horizontal: scrollable::Scrollbar::new(),
            },
        )
        .height(Fill)
        .width(Fill);
        let footer = row![
            text("Data").font(fonts::STRONG).size(11).color(t.accent),
            text("Uren & Staat").size(11),
            text("Rapport").size(11),
            text("Spreadsheet").size(11),
            text("＋").size(11),
            text("IFC").size(11),
        ]
        .spacing(22)
        .padding([6, 12]);
        column![
            container(
                text("Voorbeeldbegroting  ×     ＋")
                    .size(11)
                    .color(t.accent)
            )
            .padding([6, 10])
            .width(Fill)
            .style(move |_| container::Style::default().background(t.bg_lighter)),
            table,
            container(footer)
                .width(Fill)
                .style(move |_| container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border::default().color(t.border).width(1))),
        ]
        .spacing(0)
        .width(Fill)
        .height(Fill)
        .into()
    }

    pub(super) fn calc_explorer(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let content = column![
            text("START").font(fonts::STRONG).size(11),
            Space::new().height(12),
            text("Open Calc Studio").font(fonts::HEADING).size(16),
            text("Open of maak een nieuw document om te beginnen.")
                .size(11)
                .color(t.text_secondary),
            Space::new().height(12),
            text("＋  Nieuwe begroting").size(12),
            text("▢  Openen").size(12),
            text("↗  Voorbeeldbegroting").size(12).color(t.accent),
            Space::new().height(18),
            text("OpenAEC").font(fonts::STRONG).size(13),
            text("WAT IS ER NIEUW")
                .font(fonts::STRONG)
                .size(10)
                .color(t.text_secondary),
            text("v0.12.1 · broncapture").size(10).color(t.accent),
            text("Getallen en datums in PDF-rapporten in de rapporttaal").size(11),
        ]
        .spacing(9)
        .width(Fill);
        container(content)
            .padding(12)
            .width(Fill)
            .height(Fill)
            .style(move |_| {
                container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border::default().color(t.border).width(1))
            })
            .into()
    }

    pub(super) fn calc_properties(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let item = &items()[self.calc_selected_row];
        let content = column![
            text("EIGENSCHAPPEN").font(fonts::STRONG).size(11),
            text("GESELECTEERD ITEM")
                .font(fonts::STRONG)
                .size(10)
                .color(t.accent),
            text(field(item, "description"))
                .font(fonts::STRONG)
                .size(12),
            widgets::property("Type", field(item, "rowType"), theme),
            widgets::property("Code", field(item, "code"), theme),
            widgets::property("Aantal", number(item, "quantity"), theme),
            widgets::property("Eenheid", field(item, "unit"), theme),
            widgets::property("Eenheidsprijs", number(item, "unitPrice"), theme),
            widgets::property("Totaal · brondata", number(item, "total"), theme),
            Space::new().height(10),
            text("WIJZIGINGSHISTORIE")
                .font(fonts::STRONG)
                .size(10)
                .color(t.accent),
            text("Review van gepinde voorbeelddata; geen bewerking of herberekening.")
                .size(10)
                .color(t.text_secondary),
        ]
        .spacing(10)
        .width(Fill);
        container(content)
            .padding(12)
            .width(Fill)
            .height(Fill)
            .style(move |_| {
                container::Style::default()
                    .background(t.bg_lighter)
                    .border(iced::Border::default().color(t.border).width(1))
            })
            .into()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pinned_sample_drives_the_native_grid_and_item_selection() {
        assert_eq!(items().len(), 21);
        assert_eq!(field(&items()[5], "description"), "Funderingsbalken C25/30");
        let mut app = StyleRepo::default();
        let calc = studios()
            .iter()
            .position(|studio| studio.id == "calc")
            .unwrap();
        let _ = app.update(Action::SelectStudio(calc));
        let _ = app.update(Action::SelectScreen(1));
        assert_eq!(app.chrome_mode(), ChromeMode::ThreePaneFixed { left_width: 320, right_width: 240 });
        assert_eq!(app.documents()[0].title, "Voorbeeldbegroting");
        let _ = app.update(Action::CalcSelectRow(7));
        assert_eq!(
            field(&items()[app.calc_selected_row], "description"),
            "Wapeningsstaal FeB500"
        );
    }
}
