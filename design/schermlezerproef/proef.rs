//! The trial screen, shared by both forks: the controls an OpenAEC app needs
//! most, built from plain iced widgets without extra accessibility code. It
//! measures what each fork exposes to a screen reader by itself.
use iced::widget::{button, center, checkbox, column, container, opaque, pick_list, row, stack, text, text_input, toggler};
use iced::{Element, Length};

const DISCIPLINES: [&str; 4] = ["Architectuur", "Constructie", "Installaties", "Infra"];
const ROWS: [(&str, &str, &str); 3] = [("Ligger 1", "HEA 200", "0,64"), ("Ligger 2", "HEA 180", "0,97"), ("Kolom 3", "HEB 160", "1,12")];

#[derive(Default)]
struct Proef {
    name: String,
    saved: u32,
    report: bool,
    auto_update: bool,
    discipline: Option<&'static str>,
    dialog: bool,
    deleted: bool,
}

#[derive(Debug, Clone)]
enum Msg {
    Name(String),
    Save,
    Report(bool),
    AutoUpdate(bool),
    Discipline(&'static str),
    Dialog(bool),
    Delete,
}

impl Proef {
    fn update(&mut self, message: Msg) {
        match message {
            Msg::Name(name) => self.name = name,
            Msg::Save => self.saved += 1,
            Msg::Report(on) => self.report = on,
            Msg::AutoUpdate(on) => self.auto_update = on,
            Msg::Discipline(d) => self.discipline = Some(d),
            Msg::Dialog(open) => self.dialog = open,
            Msg::Delete => {
                self.deleted = true;
                self.dialog = false;
            }
        }
    }

    fn view(&self) -> Element<'_, Msg> {
        let table = ROWS.iter().fold(
            column![row![text("Element").width(140), text("Profiel").width(120), text("Unity check")]].spacing(6),
            |table, (element, profile, check)| table.push(row![text(*element).width(140), text(*profile).width(120), text(*check)]),
        );
        let screen = column![
            text("Schermlezerproef").size(22),
            text_input("Projectnaam", &self.name).on_input(Msg::Name).width(320),
            row![
                button("Opslaan").on_press(Msg::Save),
                text(format!("Opgeslagen: {} keer", self.saved)),
            ]
            .spacing(12),
            checkbox(self.report).label("Rapport meesturen").on_toggle(Msg::Report),
            toggler(self.auto_update).label("Automatisch bijwerken").on_toggle(Msg::AutoUpdate),
            discipline_list(self.discipline),
            table,
            button("Verwijderen…").on_press(Msg::Dialog(true)),
            text(if self.deleted { "Verwijderd" } else { "" }),
        ]
        .spacing(16)
        .padding(24);
        if !self.dialog {
            return screen.into();
        }
        let dialog = container(
            column![
                text("Ligger 2 verwijderen?").size(16),
                text("Dit kun je ongedaan maken met Ctrl+Z."),
                row![button("Annuleren").on_press(Msg::Dialog(false)), button("Verwijderen").on_press(Msg::Delete)].spacing(8),
            ]
            .spacing(12),
        )
        .padding(20)
        .width(360)
        .style(container::rounded_box);
        stack![screen, opaque(center(dialog).width(Length::Fill).height(Length::Fill))].into()
    }
}

/// The pick list: plushie-iced (iced master) takes the selection first and a
/// label function, the COSMIC fork keeps the iced 0.14 order.
#[cfg(feature = "plushie")]
fn discipline_list<'a>(selected: Option<&'static str>) -> Element<'a, Msg> {
    pick_list(selected, &DISCIPLINES[..], |d: &&str| d.to_string()).on_select(Msg::Discipline).placeholder("Kies een discipline").into()
}

#[cfg(not(feature = "plushie"))]
fn discipline_list<'a>(selected: Option<&'static str>) -> Element<'a, Msg> {
    pick_list(&DISCIPLINES[..], selected, Msg::Discipline).placeholder("Kies een discipline").into()
}

pub fn main() -> iced::Result {
    iced::application(Proef::default, Proef::update, Proef::view).title("Schermlezerproef").run()
}
