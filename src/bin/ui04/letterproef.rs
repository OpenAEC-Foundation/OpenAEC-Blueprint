//! Letterproef (issue #29): the same AEC screens in five candidate text fonts,
//! drawn by iced itself, so the team can judge them as a Rust app shows them
//! before the decision in #19.
//!
//! The candidates are Inter, Inter AEC (#28), IBM Plex Sans, Source Sans 3 and
//! Atkinson Hyperlegible Next. The three newcomers are unmodified variable fonts
//! from google/fonts in `design/letterproef/fonts` (OFL; Plex and Source have a
//! Reserved Font Name, so they are not changed), loaded with
//! `fonts::load_variable` for 400 and 600. They are only for this gallery.
use super::{ADD_ITEM, OPEN, PASTE, RECALC, REDO, REPORT, SAVE, UNDO};
use openaec_ui::design::widgets::{self as w, ButtonKind as K, Density as D};
use openaec_ui::design::{font, Look};
use openaec_ui::fonts;
use openaec_ui::iced::advanced::graphics::text::cosmic_text::skrifa::{self, MetadataProvider};
use openaec_ui::iced::font::Weight;
use openaec_ui::iced::widget::{column, container, row, scrollable, text, Space};
use openaec_ui::iced::{Alignment, Element, Font, Length};

macro_rules! candidate_file {
    ($file:literal) => {
        include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"), "/design/letterproef/fonts/", $file)) as &'static [u8]
    };
}

const PLEX: &[u8] = candidate_file!("IBMPlexSans[wdth,wght].ttf");
const SOURCE: &[u8] = candidate_file!("SourceSans3[wght].ttf");
const ATKINSON: &[u8] = candidate_file!("AtkinsonHyperlegibleNext[wght].ttf");

/// Loads the three variable candidates for 400 and 600. Call once at start.
pub fn load() {
    for bytes in [PLEX, SOURCE, ATKINSON] {
        fonts::load_variable(bytes, &[400, 600]);
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum Candidate {
    #[default]
    Inter,
    InterAec,
    Plex,
    SourceSans,
    Atkinson,
}

impl Candidate {
    pub const ALL: [Self; 5] = [Self::Inter, Self::InterAec, Self::Plex, Self::SourceSans, Self::Atkinson];

    pub fn family(self) -> &'static str {
        match self {
            Self::Inter => "Inter",
            Self::InterAec => "Inter AEC",
            Self::Plex => "IBM Plex Sans",
            Self::SourceSans => "Source Sans 3",
            Self::Atkinson => "Atkinson Hyperlegible Next",
        }
    }

    fn bytes(self) -> &'static [u8] {
        match self {
            Self::Inter => fonts::FILES[0],
            Self::InterAec => fonts::FILES[6],
            Self::Plex => PLEX,
            Self::SourceSans => SOURCE,
            Self::Atkinson => ATKINSON,
        }
    }

    fn regular(self) -> Font {
        Font::with_name(self.family())
    }

    fn strong(self) -> Font {
        Font { weight: Weight::Semibold, ..self.regular() }
    }

    /// x-height as a share of the em, from the font's own metrics.
    fn x_height(self) -> f32 {
        let data = skrifa::FontRef::new(self.bytes()).expect("candidate font");
        let metrics = data.metrics(skrifa::instance::Size::unscaled(), skrifa::instance::LocationRef::default());
        metrics.x_height.unwrap_or(0.5 * f32::from(metrics.units_per_em)) / f32::from(metrics.units_per_em)
    }
}

impl std::fmt::Display for Candidate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.family())
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Message {
    Font(Candidate),
    Size(u8),
    EqualXHeight(bool),
    Scale(f32),
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct State {
    pub font: Candidate,
    pub size: u8,
    /// Scale every font so its x-height matches Inter's at the chosen size.
    pub equal_x_height: bool,
    /// Window scale: 1.0, 1.25 or 1.5.
    pub scale: f32,
}

impl Default for State {
    fn default() -> Self {
        Self { font: Candidate::Inter, size: 13, equal_x_height: false, scale: 1.0 }
    }
}

const SIZES: [u8; 3] = [12, 13, 14];
const SCALES: [(f32, &str); 3] = [(1.0, "100%"), (1.25, "125%"), (1.5, "150%")];

impl State {
    pub fn update(&mut self, message: Message) {
        match message {
            Message::Font(font) => self.font = font,
            Message::Size(size) => self.size = size,
            Message::EqualXHeight(on) => self.equal_x_height = on,
            Message::Scale(scale) => self.scale = scale,
        }
    }

    /// The text size for `candidate`: the chosen size, or with equal x-height
    /// the size at which its x-height matches Inter's.
    pub fn size_of(&self, candidate: Candidate) -> f32 {
        let size = f32::from(self.size);
        if self.equal_x_height {
            (size * Candidate::Inter.x_height() / candidate.x_height() * 2.0).round() / 2.0
        } else {
            size
        }
    }

    pub fn view(&self, look: Look) -> Element<'_, Message> {
        let c = look.color;
        let choice = |label: &'static str, on: bool, message: Message| w::button(look, label, if on { K::Secondary } else { K::Quiet }, D::Compact, None, Some(message));
        let mut sizes = row![w::mono_label(look, "Grootte")].spacing(4).align_y(Alignment::Center);
        for size in SIZES {
            sizes = sizes.push(choice(["12 px", "13 px", "14 px"][usize::from(size - 12)], self.size == size, Message::Size(size)));
        }
        let mut scales = row![w::mono_label(look, "Schaal")].spacing(4).align_y(Alignment::Center);
        for (scale, label) in SCALES {
            scales = scales.push(choice(label, self.scale == scale, Message::Scale(scale)));
        }
        let controls = row![
            w::mono_label(look, "Tekstfont"),
            openaec_ui::design::a11y::named(container(w::select(look, &Candidate::ALL, Some(self.font), Message::Font, D::Compact)).width(230), openaec_ui::design::a11y::Role::Label, "Tekstfont"),
            sizes,
            w::checkbox(look, "Gelijke x-hoogte", self.equal_x_height, Some(Message::EqualXHeight)),
            scales,
        ]
        .spacing(16)
        .align_y(Alignment::Center);

        let font = self.font;
        let size = self.size_of(font);
        let note = format!(
            "{} op {} px{}. Thema en hoog contrast kies je rechtsboven. Getallen staan in de tekstfont, zodat je ook de cijfers vergelijkt.",
            font.family(),
            fmt_size(size),
            if self.equal_x_height { format!(" (x-hoogte gelijk aan Inter op {} px)", self.size) } else { String::new() }
        );
        let sheet = column![
            controls,
            text(note).size(font::SIZE_LABEL).font(fonts::BODY).color(c.text_secondary),
            block(look, "Lint", ribbon(look, font, size)),
            row![block(look, "Tabel met codes en getallen", table(look, font, size)), block(look, "Formulier met eenheden", form(look, font, size))].spacing(16),
            block(look, "Rapporttekst", report(look, font, size)),
            block(look, "Alle kandidaten", self.all(look)),
        ]
        .spacing(16)
        .padding(24)
        .max_width(1180);
        container(scrollable(container(sheet).center_x(Length::Fill))).height(Length::Fill).style(move |_| container::Style { background: Some(c.frame.into()), ..Default::default() }).into()
    }

    /// The same line in every candidate, at the current settings.
    fn all(&self, look: Look) -> Element<'_, Message> {
        let c = look.color;
        let mut list = column![].spacing(6);
        for candidate in Candidate::ALL {
            let size = self.size_of(candidate);
            let on = candidate == self.font;
            list = list.push(
                row![
                    text(format!("{} · {} px", candidate.family(), fmt_size(size))).size(font::SIZE_LABEL).font(if on { fonts::STRONG } else { fonts::BODY }).color(if on { c.accent_text } else { c.text_secondary }).width(230),
                    text("Il1 O0 rn m 5S 2Z · 21.10 IPE 300 · € 11.480,00 · 38,4 m³ · Ĳsselmeer ⌀ 16 σ").size(size).font(candidate.regular()).color(c.text),
                ]
                .spacing(12)
                .align_y(Alignment::Center),
            );
        }
        list.into()
    }
}

fn fmt_size(size: f32) -> String {
    if size.fract() == 0.0 { format!("{size:.0}") } else { format!("{size:.1}").replace('.', ",") }
}

fn block<'a>(look: Look, title: &'static str, content: Element<'a, Message>) -> Element<'a, Message> {
    container(column![w::mono_label(look, title), content].spacing(10)).padding(14).width(Length::Fill).style(move |_| w::panel_style(look)).into()
}

fn ribbon<'a>(look: Look, font: Candidate, size: f32) -> Element<'a, Message> {
    let c = look.color;
    let label_size = (size - 1.0).max(11.0);
    let button = |icon: &'static str, label: &'static str| -> Element<'a, Message> {
        column![w::glyph(icon, 24.0, c.text, c.accent), text(label).size(label_size).font(font.regular()).color(c.text)].spacing(4).align_x(Alignment::Center).width(78).into()
    };
    let group = |title: &'static str, buttons: Vec<Element<'a, Message>>| -> Element<'a, Message> {
        column![row(buttons).spacing(2), text(title.to_uppercase()).size(11).font(fonts::MONO).color(c.text_secondary)].spacing(6).align_x(Alignment::Center).into()
    };
    let divider = || container(Space::new().width(1).height(64)).style(move |_| container::Style { background: Some(c.border.into()), ..Default::default() });
    row![
        group("Project", vec![button(OPEN, "Openen"), button(SAVE, "Opslaan")]),
        divider(),
        group("Bewerken", vec![button(PASTE, "Plakken"), button(UNDO, "Ongedaan"), button(REDO, "Opnieuw")]),
        divider(),
        group("Begroting", vec![button(ADD_ITEM, "Nieuwe post"), button(RECALC, "Herberekenen"), button(REPORT, "Rapport")]),
    ]
    .spacing(10)
    .align_y(Alignment::Center)
    .into()
}

const ROWS: [(&str, &str, &str, &str); 6] = [
    ("21.10", "Funderingsbalk 400×600", "38,4 m³", "€ 9.216,00"),
    ("21.20", "Prefab betonpaal 290×290, l=18,5 m", "12 st", "€ 11.480,00"),
    ("22.11", "Kanaalplaatvloer C30/37", "164,0 m²", "€ 14.875,00"),
    ("31.01", "Ligger IPE 300 S235", "1,2 t", "€ 1.111,10"),
    ("31.17", "Kolom HEB 160, K1 tot en met K11", "11 st", "€ 7.701,00"),
    ("41.10", "Wapening Ø 12-150, Il1-lI1", "850 kg", "€ 0,00"),
];

fn table<'a>(look: Look, font: Candidate, size: f32) -> Element<'a, Message> {
    let c = look.color;
    let head = |label: &'static str, width: Length, right: bool| {
        let t = w::mono_label(look, label).width(width);
        if right { t.align_x(Alignment::End) } else { t }
    };
    let mut sheet = column![row![head("Code", Length::Fixed(56.0), false), head("Omschrijving", Length::Fill, false), head("Hoeveelheid", Length::Fixed(90.0), true), head("Bedrag", Length::Fixed(100.0), true)].spacing(10)].spacing(8);
    for (code, name, quantity, amount) in ROWS {
        let cell = |value: &'static str, width: Length, right: bool| {
            let t = text(value).size(size).font(font.regular()).color(c.text).width(width);
            if right { t.align_x(Alignment::End) } else { t }
        };
        sheet = sheet.push(row![cell(code, Length::Fixed(56.0), false), cell(name, Length::Fill, false), cell(quantity, Length::Fixed(90.0), true), cell(amount, Length::Fixed(100.0), true)].spacing(10));
    }
    sheet = sheet.push(row![text("Totaal").size(size).font(font.strong()).color(c.text).width(Length::Fill), text("€ 44.383,10").size(size).font(font.strong()).color(c.text)].spacing(10));
    sheet.into()
}

const FIELDS: [(&str, &str, &str); 6] = [
    ("Rc-waarde gevel", "4,70", "m²K/W"),
    ("U-waarde kozijn", "1,40", "W/m²K"),
    ("Wapening", "Ø 12-150", "mm"),
    ("Betonkwaliteit", "C30/37", ""),
    ("Spanning σ", "235", "N/mm²"),
    ("Paaldiameter ⌀", "400", "mm"),
];

fn form<'a>(look: Look, font: Candidate, size: f32) -> Element<'a, Message> {
    let c = look.color;
    let mut list = column![].spacing(8);
    for (label, value, unit) in FIELDS {
        let field = container(text(value).size(size).font(font.regular()).color(c.text)).padding([4, 8]).width(110).style(move |_| container::Style {
            background: Some(c.raised.into()),
            border: openaec_ui::iced::Border { color: c.border_strong, width: 1.0, radius: 4.0.into() },
            ..Default::default()
        });
        list = list.push(row![text(label).size(size).font(font.regular()).color(c.text_secondary).width(Length::Fill), field, text(unit).size(size).font(font.regular()).color(c.text_secondary).width(60)].spacing(8).align_y(Alignment::Center));
    }
    list.width(380).into()
}

fn report<'a>(look: Look, font: Candidate, size: f32) -> Element<'a, Message> {
    let c = look.color;
    column![
        text("3.2 Fundering en hoofddraagconstructie").size(size + 3.0).font(font.strong()).color(c.text),
        text("De fundering bestaat uit prefab betonpalen 290×290 mm met een lengte van 18,5 m en een draagvermogen van 950 kN per paal. De ligger IPE 300 (S235) heeft een unity check van 0,81; de kolom HEB 160 voldoet met 0,97. In as 1 tot en met 11 komen Ĳzeren ankers ⌀ 16 mm h.o.h. 600 mm; de spanning σ blijft onder 235 N/mm². Ill. 4 en tabel 3.1 geven de maten; let op het verschil tussen l (lengte), I (traagheidsmoment) en 1.")
            .size(size)
            .font(font.regular())
            .color(c.text),
    ]
    .spacing(8)
    .max_width(820)
    .into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn equal_x_height_scales_each_font_to_inter() {
        let state = State { equal_x_height: true, ..State::default() };
        assert_eq!(state.size_of(Candidate::Inter), 13.0);
        for candidate in Candidate::ALL {
            let shown = state.size_of(candidate) * candidate.x_height();
            assert!((shown - 13.0 * Candidate::Inter.x_height()).abs() < 0.3, "{candidate}: {shown}");
        }
        // Inter AEC has Inter's metrics, so the same size.
        assert_eq!(state.size_of(Candidate::InterAec), 13.0);
    }
}
