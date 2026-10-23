//! Source-aligned borehole review, based on the pinned 02-bhr-boring capture.
//! The bands are UI examples; they are not a geotechnical interpretation engine.
use super::*;
use openaec_ui::iced::widget::{column, row};

pub(super) struct Layer {
    pub top: f32,
    pub bottom: f32,
    pub name: &'static str,
    pub color: &'static str,
    pub detail: &'static str,
}

pub(super) const LAYERS: [Layer; 13] = [
    Layer {
        top: 0.30,
        bottom: 0.92,
        name: "sterkSiltigZand",
        color: "#efc66b",
        detail: "Zand · sterk siltig",
    },
    Layer {
        top: 0.92,
        bottom: 1.36,
        name: "matigSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · matig siltig",
    },
    Layer {
        top: 1.36,
        bottom: 1.48,
        name: "veenNietGespecificeerd",
        color: "#85513a",
        detail: "Veen · niet gespecificeerd",
    },
    Layer {
        top: 1.48,
        bottom: 1.92,
        name: "matigSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · matig siltig",
    },
    Layer {
        top: 1.92,
        bottom: 5.99,
        name: "mineraalarmVeen",
        color: "#85513a",
        detail: "Veen · mineraalarm",
    },
    Layer {
        top: 5.99,
        bottom: 6.40,
        name: "zwakSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · zwak siltig",
    },
    Layer {
        top: 6.40,
        bottom: 6.73,
        name: "zwakSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · zwak siltig",
    },
    Layer {
        top: 6.73,
        bottom: 7.20,
        name: "matigSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · matig siltig",
    },
    Layer {
        top: 7.20,
        bottom: 7.55,
        name: "matigSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · matig siltig",
    },
    Layer {
        top: 7.55,
        bottom: 7.68,
        name: "zwakSiltigZand",
        color: "#efc66b",
        detail: "Zand · zwak siltig",
    },
    Layer {
        top: 7.68,
        bottom: 7.85,
        name: "zwakSiltigZand",
        color: "#efc66b",
        detail: "Zand · zwak siltig",
    },
    Layer {
        top: 7.85,
        bottom: 8.20,
        name: "zwakSiltigZand",
        color: "#efc66b",
        detail: "Zand · zwak siltig",
    },
    Layer {
        top: 8.20,
        bottom: 8.40,
        name: "matigSiltigeKlei",
        color: "#8bb36f",
        detail: "Klei · matig siltig",
    },
];

fn profile_svg(selected: usize, theme: Theme) -> Vec<u8> {
    let guide = if theme == Theme::Forge {
        "#56565d"
    } else {
        "#dddddf"
    };
    let mut drawing = String::from(
        r##"<svg xmlns="http://www.w3.org/2000/svg" width="160" height="560" viewBox="0 0 160 560"><defs><pattern id="sand" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".6" fill="#8d632d"/></pattern><pattern id="peat" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 2h5" stroke="#42271c" stroke-width=".5"/></pattern><pattern id="clay" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M-2 7L7-2" stroke="#42683e" stroke-width=".6"/></pattern></defs>"##,
    );
    let y_of = |depth: f32| 22.0 + (depth - 0.30) * 62.0;
    for meter in 0..=8 {
        let y = y_of(meter as f32).max(22.0);
        if y <= 525.0 {
            drawing.push_str(&format!(
                r##"<path d="M0 {y:.1}H160" stroke="{guide}" stroke-width=".7"/>"##
            ));
        }
    }
    for (index, layer) in LAYERS.iter().enumerate() {
        let y = y_of(layer.top);
        let height = ((layer.bottom - layer.top) * 62.0).max(1.0);
        let pattern = if layer.name.contains("Zand") {
            "sand"
        } else if layer.name.contains("Veen") {
            "peat"
        } else {
            "clay"
        };
        drawing.push_str(&format!(r##"<rect x="2" y="{y:.1}" width="150" height="{height:.1}" fill="{}" stroke="{}" stroke-width="{}"/><rect x="2" y="{y:.1}" width="150" height="{height:.1}" fill="url(#{pattern})" opacity=".7"/>"##, layer.color, if index == selected { "#d97706" } else { guide }, if index == selected { 2 } else { 1 }));
    }
    drawing.push_str("</svg>");
    drawing.into_bytes()
}

pub(super) fn workspace(selected: usize, theme: Theme, l: Language) -> Element<'static, Action> {
    let t = theme.tokens();
    let chart = svg(svg::Handle::from_memory(profile_svg(selected, theme)))
        .width(160)
        .height(560);
    let mut scale = Column::new()
        .width(46)
        .push(text("NAP (m)").size(10).color(t.text_secondary));
    scale = scale.push(Space::new().width(0).height(48));
    for meter in 1..=8 {
        scale = scale.push(
            container(
                text(format!("-{meter:.2}"))
                    .size(10)
                    .color(t.text_secondary),
            )
            .height(62),
        );
    }
    let mut rows = Column::new().spacing(2);
    for (index, layer) in LAYERS.iter().enumerate() {
        let label = format!("{:.2}–{:.2} m  ·  {}", layer.top, layer.bottom, layer.name);
        rows = rows.push(
            button(
                column![
                    text(label).font(fonts::STRONG).size(11),
                    text(layer.detail).size(10).color(t.text_secondary),
                ]
                .spacing(2),
            )
            .padding([6, 9])
            .width(Fill)
            .on_press(Action::GeotechLayer(index))
            .style(move |_, state| widgets::button_style(theme, selected == index, state)),
        );
    }
    column![
        text("BHR000000391794")
            .font(fonts::HEADING)
            .size(21)
            .color(t.text),
        text(l.text(
            "Boorprofiel · brongetrouwe lagen en dieptes, native Rust-weergave",
            "Borehole profile · source-aligned layers and depths, native Rust view"
        ))
        .size(11)
        .color(t.text_secondary),
        row![scale, chart, scrollable(rows).height(560).width(Fill)]
            .spacing(10)
            .height(560),
        text(l.text(
            "Visuele review van de broncapture; geen bodemkundige berekening.",
            "Visual review of the source capture; no soil calculation."
        ))
        .size(10)
        .color(t.text_secondary),
    ]
    .spacing(10)
    .width(Fill)
    .into()
}

pub(super) fn explorer(theme: Theme) -> Element<'static, Action> {
    let t = theme.tokens();
    column![
        text("BHR000000391794")
            .font(fonts::STRONG)
            .size(12)
            .color(t.accent),
        text("BHR000000391794.xml").size(10).color(t.text_secondary),
        widgets::property("Startdatum", "2002-10-25", theme),
        widgets::property("Bronhouder", "archief overdracht", theme),
        widgets::property("Kwaliteit", "IMBRO/A", theme),
        widgets::property("Maaiveld NAP", "-1.40 m", theme),
        widgets::property("Einddiepte", "8.40 m", theme),
        widgets::property("Lagen", "13", theme),
    ]
    .spacing(7)
    .into()
}

pub(super) fn properties(selected: usize, theme: Theme) -> Element<'static, Action> {
    let t = theme.tokens();
    let layer = &LAYERS[selected.min(LAYERS.len() - 1)];
    column![
        text("GESELECTEERDE LAAG")
            .font(fonts::STRONG)
            .size(11)
            .color(t.accent),
        widgets::property("Grondsoort", layer.detail, theme),
        widgets::property("Van", format!("{:.2} m", layer.top), theme),
        widgets::property("Tot", format!("{:.2} m", layer.bottom), theme),
        text("ROBERTSON SBT")
            .font(fonts::STRONG)
            .size(11)
            .color(t.accent),
        widgets::property("1", "Gevoelig fijnkorrelig", theme),
        widgets::property("2", "Organisch / veen", theme),
        widgets::property("3", "Klei", theme),
        widgets::property("6", "Zand", theme),
    ]
    .spacing(8)
    .into()
}
