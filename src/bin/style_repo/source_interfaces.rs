//! Source-backed non-studio UIs. Construction SVGs remain domain content,
//! never entries in the shared UI icon registry.
use super::*;
use openaec_ui::iced::widget::{checkbox, column, row};

pub(super) struct SourceRoute {
    pub label: &'static str,
    pub source: &'static str,
    pub sections: &'static [&'static str],
}

pub(super) const OCONDAT_ROUTES: [SourceRoute; 12] = [
    SourceRoute {
        label: "Component Library",
        source: "DXF Library/component-library/index.html",
        sections: &[
            "Fabrikanten",
            "IFC Klassen",
            "NL-SfB",
            "Zoeken",
            "Eigenschappen",
        ],
    },
    SourceRoute {
        label: "Fabrikanten",
        source: "DXF Library/component-library/fabrikanten.html",
        sections: &["Alle", "Actief", "Inactief", "Historisch"],
    },
    SourceRoute {
        label: "Nederlandse standaarden",
        source: "Libraries/Netherlands/index.html",
        sections: &["Bouwkundig", "Constructie", "Civiel", "Installatie"],
    },
    SourceRoute {
        label: "Open BIM Library",
        source: "Libraries/Netherlands/library/index.html",
        sections: &["Zoeken", "Familie", "Type", "Componentdetails"],
    },
    SourceRoute {
        label: "Bouwkundig",
        source: "Libraries/Netherlands/bouwkundig.html",
        sections: &[
            "Tekeningtypen",
            "Arceringen per Schaal",
            "Arceringen (NEN 47:1970)",
            "Materiaal Achtergrondkleuren",
            "Lijntypen",
        ],
    },
    SourceRoute {
        label: "Constructie",
        source: "Libraries/Netherlands/constructie.html",
        sections: &[
            "Constructietekeningen Overzicht",
            "Betonconstructies",
            "Staalconstructies",
            "Houtconstructies",
            "Funderingen",
        ],
    },
    SourceRoute {
        label: "Civiele Techniek",
        source: "Libraries/Netherlands/civiel.html",
        sections: &[
            "NLCS - Nederlandse CAD Standaard",
            "Grondsoorten & Arceringen",
            "Riolering",
            "Wegenbouw",
            "Waterbouw",
        ],
    },
    SourceRoute {
        label: "Installatie",
        source: "Libraries/Netherlands/installatie.html",
        sections: &[
            "E-Installatie (Elektra)",
            "W-Installatie (Water/Sanitair)",
            "Klimaatinstallaties",
            "Brandmeld & Beveiliging",
            "Relevante Normen",
        ],
    },
    SourceRoute {
        label: "Palenplannen",
        source: "Libraries/Netherlands/palenplan.html",
        sections: &[
            "Peilaanduidingen",
            "Paalsymbolen",
            "Palenplan Voorbeeld",
            "Paaltypen Overzicht",
        ],
    },
    SourceRoute {
        label: "Staalprofielen",
        source: "Libraries/Netherlands/staalprofielen.html",
        sections: &[
            "Profielvormen Overzicht",
            "I-Profielen (Breed Flens)",
            "U-Profielen (Kanaalprofielen)",
            "Kokerprofielen (Holle Doorsneden)",
            "Ronde Buizen",
        ],
    },
    SourceRoute {
        label: "Wapeningsstekeningen",
        source: "Libraries/Netherlands/wapening.html",
        sections: &[
            "Wapeningsstaalkwaliteit - Vlaggetjes",
            "Staafaanduiding",
            "Netaanduiding",
            "Wapeningslagen",
            "Balkdoorsnede",
        ],
    },
    SourceRoute {
        label: "Belastingen Calculator",
        source: "Libraries/Netherlands/belastingen-calculator.html",
        sections: &[
            "Veranderlijke Belasting",
            "Windbelasting",
            "Klimaatbelastingen - Combinatiefactoren",
            "Overzicht Gebruikscategorieën",
        ],
    },
];

const MANUFACTURERS: [(&str, usize); 5] = [
    ("ArcelorMittal", 359),
    ("Community/DXF-library", 2256),
    ("Community/dxfBlocks", 305),
    ("Generic", 1307),
    ("Halfen", 18606),
];
const COMPONENTS: [(&str, &str, &str); 8] = [
    ("As500-11.0_2025", "ArcelorMittal", "IfcPile"),
    ("As500-12.0_2025", "ArcelorMittal", "IfcPile"),
    ("Ag_eletr", "Community/DXF-library", "IfcElectricAppliance"),
    ("Armoire", "Community/dxfBlocks", "IfcFurniture"),
    (
        "Aansluitprofiel-droogbouw-1138-type-1313",
        "Generic",
        "IfcMember",
    ),
    ("Hgb-40-25", "Halfen", "IfcMechanicalFastener"),
    ("Au14-d_2025", "ArcelorMittal", "IfcPile"),
    ("Hgb-38-17", "Halfen", "IfcMechanicalFastener"),
];
const DUTCH_COMPONENTS: [(&str, &str); 6] = [
    (
        "00 Kingspan_Detail_KS1000_Evolution_dikte 88",
        "Kingspan paneeldetail",
    ),
    ("16 anker-recht", "Wandanker"),
    ("17 paal_aanzicht", "Paal"),
    ("20 kz_anker", "Kozijnanker"),
    ("22 metalstud profiel", "Metalstud"),
    ("23 VBI kanaalplaat", "Kanaalplaat"),
];

impl StyleRepo {
    pub(super) fn source_interfaces_page(&self, theme: Theme, l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let selector = row![
            button(text("Project OconDat").size(12))
                .on_press(Action::SelectSourceApp(0))
                .style(move |_, status| widgets::button_style(theme, self.source_app == 0, status)),
            button(text("BuildingPy · GIS2BIM").size(12))
                .on_press(Action::SelectSourceApp(1))
                .style(move |_, status| widgets::button_style(theme, self.source_app == 1, status)),
        ]
        .spacing(8);
        let body = if self.source_app == 0 {
            self.ocondat_page(theme, l)
        } else {
            self.buildingpy_page(theme, l)
        };
        column![
            self.heading("SOURCE UI · PINNED", l.text("Broninterfaces", "Source interfaces"),
                l.text("Niet elke OpenAEC-bron is een ribbonstudio. Deze twee interfaces gebruiken dezelfde Rust-typografie, velden en panelen, met hun eigen navigatie.",
                       "Not every OpenAEC source is a ribbon studio. These two interfaces use the same Rust typography, fields and panels with their own navigation."), theme),
            selector,
            text("Onderzoek op vastgelegde commits · OconDat 85a78eef · BuildingPy 291cc79d")
                .size(11).color(t.text_secondary),
            body,
        ].spacing(16).into()
    }

    fn ocondat_page(&self, theme: Theme, _l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let route = &OCONDAT_ROUTES[self.source_route];
        let mut routes = Column::new().spacing(5).width(200);
        for (index, item) in OCONDAT_ROUTES.iter().enumerate() {
            routes = routes.push(
                button(text(item.label).size(11))
                    .width(Fill)
                    .padding([7, 10])
                    .on_press(Action::SelectSourceRoute(index))
                    .style(move |_, status| {
                        widgets::button_style(theme, index == self.source_route, status)
                    }),
            );
        }
        let body: Element<'_, Action> = match self.source_route {
            0 => self.ocondat_components(theme),
            1 => self.ocondat_manufacturers(theme),
            2 => self.ocondat_standards(theme),
            3 => self.ocondat_bim_library(theme),
            11 => self.ocondat_loads(theme),
            _ => self.ocondat_technical_route(theme),
        };
        let content = column![
            text(route.label).font(fonts::HEADING).size(26).color(t.text),
            text(format!("Bron: {}", route.source)).font(fonts::MONO).size(11).color(t.text_secondary),
            body,
            self.card(text("Technische SVG's zijn componentgeometrie of tekenpatronen, geen UI-iconen. Deze review laadt ze daarom niet als bediening.")
                .size(11).color(t.text_secondary), theme),
        ].spacing(14).width(850);
        row![routes, content].spacing(23).into()
    }

    fn ocondat_components(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let manufacturer = self.source_manufacturer;
        let filters = row![
            text_input("Zoek op naam, IFC class, tag...", &self.source_search)
                .on_input(Action::SourceSearch)
                .padding([8, 10])
                .width(320)
                .style(move |_, status| widgets::text_input_style(theme, status)),
            pick_list(
                (0..=5)
                    .map(|index| if index == 0 {
                        "Alle fabrikanten".to_string()
                    } else {
                        MANUFACTURERS[index - 1].0.to_string()
                    })
                    .collect::<Vec<_>>(),
                Some(if manufacturer == 0 {
                    "Alle fabrikanten".to_string()
                } else {
                    MANUFACTURERS[manufacturer - 1].0.to_string()
                }),
                |name| Action::SourceManufacturer(
                    MANUFACTURERS
                        .iter()
                        .position(|item| item.0 == name)
                        .map_or(0, |index| index + 1)
                )
            )
            .width(220)
            .style(move |_, status| widgets::pick_list_style(theme, status))
            .menu_style(move |_| widgets::pick_list_menu_style(theme)),
        ]
        .spacing(10)
        .align_y(Alignment::Center);
        let query = self.source_search.to_lowercase();
        let mut cards = Column::new().spacing(7);
        let mut shown = 0;
        for (index, (name, maker, ifc)) in COMPONENTS.iter().enumerate() {
            if manufacturer != 0 && MANUFACTURERS[manufacturer - 1].0 != *maker {
                continue;
            }
            if !query.is_empty()
                && !format!("{name} {maker} {ifc}")
                    .to_lowercase()
                    .contains(&query)
            {
                continue;
            }
            shown += 1;
            cards = cards.push(
                button(
                    row![
                        container(text("DXF").font(fonts::MONO).size(11).color(t.accent))
                            .width(52)
                            .height(40)
                            .align_x(Alignment::Center)
                            .align_y(Alignment::Center)
                            .style(move |_| container::Style::default().background(t.accent_soft)),
                        column![
                            text(*name).font(fonts::MEDIUM).size(12),
                            text(format!("{maker} · {ifc}"))
                                .size(11)
                                .color(t.text_secondary)
                        ]
                        .spacing(4)
                        .width(Fill),
                        text("Details").size(11).color(t.accent),
                    ]
                    .spacing(11)
                    .align_y(Alignment::Center),
                )
                .padding(7)
                .width(Fill)
                .on_press(Action::SourceDetails(Some(index)))
                .style(move |_, status| widgets::button_style(theme, false, status)),
            );
        }
        column![
            filters,
            text(format!(
                "{shown} van 8 bronvoorbeelden · oorspronkelijke catalogus: 22.833 componenten"
            ))
            .size(11)
            .color(t.text_secondary),
            cards
        ]
        .spacing(12)
        .into()
    }

    fn ocondat_manufacturers(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut filters = Row::new().spacing(6);
        for (index, label) in ["Alle", "Actief", "Inactief", "Historisch"]
            .iter()
            .enumerate()
        {
            filters = filters.push(
                button(text(*label).size(11))
                    .padding([6, 9])
                    .on_press(Action::SourceStatus(index))
                    .style(move |_, status| {
                        widgets::button_style(theme, self.source_status_filter == index, status)
                    }),
            );
        }
        let mut list = Column::new().spacing(8);
        if self.source_status_filter <= 1 {
            for (index, (name, count)) in MANUFACTURERS.iter().enumerate() {
                list = list.push(
                    button(
                        row![
                            text(*name).font(fonts::STRONG).size(13).width(Fill),
                            text(format!("{count} componenten · Actief"))
                                .size(11)
                                .color(t.text_secondary),
                            text("Bekijk").size(11).color(t.accent),
                        ]
                        .spacing(12)
                        .align_y(Alignment::Center),
                    )
                    .padding(14)
                    .width(Fill)
                    .on_press(Action::SourceManufacturerCatalog(index + 1))
                    .style(move |_, status| {
                        widgets::button_style(theme, self.source_manufacturer == index + 1, status)
                    }),
                );
            }
        } else {
            list = list.push(
                self.card(
                    text("Geen fabrikanten in deze bronstatus.")
                        .size(12)
                        .color(t.text_secondary),
                    theme,
                ),
            );
        }
        column![
            text("Fabrikanten uit de broncatalogus")
                .font(fonts::STRONG)
                .size(14),
            filters,
            list
        ]
        .spacing(11)
        .into()
    }

    fn ocondat_standards(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut list = Column::new().spacing(8);
        for index in 4..=7 {
            let route = &OCONDAT_ROUTES[index];
            list = list.push(
                button(
                    row![
                        text(route.label).font(fonts::STRONG).size(14).width(Fill),
                        text(format!("{} secties", route.sections.len()))
                            .size(11)
                            .color(t.text_secondary),
                        text("Open").size(11).color(t.accent),
                    ]
                    .spacing(12)
                    .align_y(Alignment::Center),
                )
                .padding(16)
                .width(Fill)
                .on_press(Action::SelectSourceRoute(index))
                .style(move |_, status| widgets::button_style(theme, false, status)),
            );
        }
        column![
            text("Nederlandse tekenstandaarden · disciplineoverzicht")
                .font(fonts::STRONG)
                .size(14),
            list
        ]
        .spacing(11)
        .into()
    }

    fn ocondat_bim_library(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let query = self.source_search.to_lowercase();
        let mut list = Column::new().spacing(7);
        for (family, kind) in DUTCH_COMPONENTS {
            if !query.is_empty() && !format!("{family} {kind}").to_lowercase().contains(&query) {
                continue;
            }
            list = list.push(
                self.card(
                    row![
                        container(text("DXF").font(fonts::MONO).size(11).color(t.accent))
                            .width(52)
                            .height(40)
                            .align_x(Alignment::Center)
                            .align_y(Alignment::Center)
                            .style(move |_| container::Style::default().background(t.accent_soft)),
                        column![
                            text(family).font(fonts::MEDIUM).size(12),
                            text(kind).size(11).color(t.text_secondary)
                        ]
                        .spacing(4),
                    ]
                    .spacing(11)
                    .align_y(Alignment::Center),
                    theme,
                ),
            );
        }
        column![
            text_input("Zoek op naam, familie of type...", &self.source_search)
                .on_input(Action::SourceSearch)
                .padding([8, 10])
                .width(360)
                .style(move |_, status| widgets::text_input_style(theme, status)),
            text("6 van 30 broncomponenten als routevoorbeeld")
                .size(11)
                .color(t.text_secondary),
            list,
        ]
        .spacing(12)
        .into()
    }

    fn ocondat_loads(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        column![
            self.card(
                column![
                text("Veranderlijke Belasting").font(fonts::STRONG).size(15),
                widgets::property("Gebruikscategorie", "-- Selecteer categorie --", theme),
                row![widgets::property("ψ₀", "-", theme), widgets::property("ψ₁", "-", theme),
                    widgets::property("ψ₂", "-", theme)].spacing(18),
                text("Bronvelden en bronsecties; rekenlogica is niet in de Style Repo overgenomen.")
                    .size(11).color(t.text_secondary),
            ]
                .spacing(12),
                theme
            ),
            self.ocondat_technical_route(theme),
        ]
        .spacing(12)
        .into()
    }

    fn ocondat_technical_route(&self, theme: Theme) -> Element<'_, Action> {
        let t = theme.tokens();
        let mut list = Column::new().spacing(8);
        for section in OCONDAT_ROUTES[self.source_route].sections {
            list = list.push(
                self.card(
                    column![
                text(*section).font(fonts::STRONG).size(13).color(t.text),
                text("Bronsectie · technische tekenvoorbeelden blijven in de domeinassetlaag")
                    .size(11).color(t.text_secondary),
            ]
                    .spacing(6),
                    theme,
                ),
            );
        }
        list.into()
    }

    fn buildingpy_page(&self, theme: Theme, _l: Language) -> Element<'_, Action> {
        let t = theme.tokens();
        let field = |index: usize, label: &'static str| {
            widgets::form_field(
                theme,
                label,
                self.source_location[index].clone(),
                move |value| Action::SourceLocationEdit(index, value),
                iced::Length::Fixed(315.0),
            )
        };
        let map = container(column![
            text("KAART").font(fonts::MONO).size(11).color(t.accent),
            text("GIS2BIM · WebEngine-kaartvak").font(fonts::STRONG).size(14),
            text("De bron laadt kaart-HTML en GIS-scripts extern; hier staat alleen de native kadermaat en positie.")
                .size(11).color(t.text_secondary),
        ].spacing(9).align_x(Alignment::Center)).width(760).height(225).align_x(Alignment::Center).align_y(Alignment::Center)
            .style(move |_| container::Style::default().background(t.bg_lighter)
                .border(iced::Border { color: t.border, width: 1.0, radius: 4.0.into() }));
        let form = self.card(column![
            text("Location").font(fonts::STRONG).size(15),
            row![field(0, "Search Place/Address"),
                button(text("Search").size(12)).on_press(Action::SourceNotice("Zoeken is een bronbediening; Nominatim en FreeCAD zijn hier niet gekoppeld."))
                    .style(move |_, status| widgets::primary_button_style(theme, status))].spacing(10).align_y(Alignment::End),
            field(1, "Coordinate Reference System · bronkeuzelijst"),
            row![field(2, "Boundingbox Width [m]"), field(3, "Boundingbox Height [m]")].spacing(14),
            checkbox(self.source_geo_origin).label("Create/Update GeoOrigin Object")
                .on_toggle(Action::SourceGeoOrigin).style(move |_, status| widgets::checkbox_style(theme, status)),
            checkbox(self.source_aerial).label("Import Aerialphoto")
                .on_toggle(Action::SourceAerial).style(move |_, status| widgets::checkbox_style(theme, status)),
        ].spacing(14), theme);
        let notice: Element<'_, Action> = self.source_notice.map_or_else(
            || Space::new().width(0).height(0).into(),
            |message| text(message).size(11).color(t.accent).into(),
        );
        container(
            column![
                text("Set Geographic Location")
                    .font(fonts::HEADING)
                    .size(26)
                    .color(t.text),
                text("Bron: apps/GIS2BIM/GIS2BIM_location.py · PySide2 QDialog · 920 × 900 px")
                    .font(fonts::MONO)
                    .size(11)
                    .color(t.text_secondary),
                map,
                form,
                row![
                    button(text("Cancel").size(12))
                        .on_press(Action::SourceNotice(
                            "Locatiedialoog geannuleerd in deze review."
                        ))
                        .style(move |_, status| widgets::secondary_button_style(theme, status)),
                    button(text("OK").size(12))
                        .on_press(Action::SourceNotice(
                            "FreeCAD-projectmutatie is in deze review niet gekoppeld."
                        ))
                        .style(move |_, status| widgets::primary_button_style(theme, status)),
                ]
                .spacing(8),
                notice,
            ]
            .spacing(15),
        )
        .width(920)
        .into()
    }

    pub(super) fn source_details_modal(&self, theme: Theme) -> Option<Element<'_, Action>> {
        if self.page != Page::Sources || self.source_app != 0 || self.source_route != 0 {
            return None;
        }
        let (name, manufacturer, ifc) = *COMPONENTS.get(self.source_details?)?;
        let body = column![
            widgets::property("Naam", name, theme),
            widgets::property("Fabrikant", manufacturer, theme),
            widgets::property("IFC-klasse", ifc, theme),
            text("De technische SVG/DXF-preview is niet als UI-icoon overgenomen.").size(11),
        ]
        .spacing(12)
        .into();
        let footer = row![
            Space::new().width(Fill),
            widgets::dialog_button("Sluiten", move |_, status| widgets::primary_button_style(
                theme, status
            ))
            .on_press(Action::SourceDetails(None))
        ]
        .into();
        Some(widgets::dialog_modal(
            name,
            body,
            footer,
            Action::SourceDetails(None),
            520.0,
            theme,
        ))
    }
}
