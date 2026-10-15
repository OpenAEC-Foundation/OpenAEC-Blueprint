//! Native rendition of the proposed ribbon groups in design/harmonized-template.html.
//! FEM/BIM SVGs are review drafts, supplied as application-owned vectors.
use super::*;

macro_rules! planner_source_icon {
    ($name:literal) => {
        CommandIcon::Svg(include_bytes!(concat!(
            "../../../harmonization/library-icons/lucide-static/0.575.0/",
            $name,
            ".svg"
        )))
    };
}

pub(super) fn studio_tabs(studio: &StudioLayout, selected: Option<&str>) -> Vec<RibbonTab<Action>> {
    studio
        .tabs
        .iter()
        .filter(|tab| tab.as_str() != "Bestand")
        .map(|tab| RibbonTab {
            id: tab.to_lowercase(),
            label: if studio.optional_tabs.contains(tab) {
                format!("{tab} · optioneel")
            } else {
                tab.clone()
            },
            groups: planner_groups(studio, tab, selected)
                .or_else(|| frame_groups(studio, tab, selected))
                .or_else(|| calc_groups(studio, tab, selected))
                .or_else(|| geotech_groups(studio, tab, selected))
                .or_else(|| heatloss_groups(studio, tab, selected))
                .or_else(|| calculations_groups(studio, tab, selected))
                .or_else(|| reports_groups(studio, tab, selected))
                .or_else(|| validator_groups(studio, tab, selected))
                .or_else(|| pile_groups(studio, tab, selected))
                .or_else(|| domain_groups(studio, tab, selected))
                .unwrap_or_else(|| base_groups(tab, selected)),
        })
        .collect()
}

/// Open Frame Studio shell ribbon at eb77f9e4c5d3. Template/theme selects are
/// represented as commands until typed ribbon controls are available.
fn frame_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "frame" { return None; }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Home" => vec![
            ("Sjabloon", vec![("Sjabloon kiezen", Grid.into()), ("Opslaan als sjabloon", Save.into()), ("Sjabloon verwijderen", Close.into())]),
            ("Nieuw kozijn", vec![("Leeg", New.into()), ("Draaikiep", planner_source_icon!("Square")), ("Dubbel", planner_source_icon!("LayoutGrid")), ("Schuifpui", planner_source_icon!("Square")), ("Voordeur", planner_source_icon!("Square"))]),
            ("Bewerken", vec![("Kolom toevoegen", planner_source_icon!("Columns3")), ("Rij toevoegen", planner_source_icon!("LayoutGrid")), ("Dupliceren", planner_source_icon!("Copy")), ("Verwijderen", planner_source_icon!("Trash2"))]),
            ("Importeren", vec![("Nieuw profiel", New.into()), ("Profiel DXF", Import.into()), ("Catalogus", Open.into())]),
        ],
        "Invoegen" => vec![
            ("Onderverdeling", vec![("Kolom", planner_source_icon!("Columns3")), ("Rij", planner_source_icon!("LayoutGrid"))]),
            ("Paneel type", vec![("Vast glas", planner_source_icon!("Square")), ("Draaikiep", planner_source_icon!("Square")), ("Paneel", planner_source_icon!("Square"))]),
            ("Vliesgevel", vec![("Leeg", New.into()), ("Stijl-regel", Grid.into()), ("Element", Cube.into())]),
        ],
        "IFC / Export" => vec![
            ("Kozijn exporteren", vec![("IFC (LOD-keuze)", Export.into()), ("DXF", Export.into())]),
            ("IFC Import", vec![("IFC Import", Import.into()), ("IFC Roundtrip", planner_source_icon!("GitCompareArrows")), ("IFC vergelijken", planner_source_icon!("GitCompareArrows"))]),
            ("Validatie", vec![("IDS Validatie", Check.into()), ("Certificering", Check.into())]),
            ("Project exporteren", vec![("Kozijnstaat PDF", Export.into()), ("Kozijnstaat Excel", Export.into())]),
            ("Werkplaats", vec![("Tekening PDF", Export.into())]),
            ("3D Export", vec![("glTF/GLB", Export.into())]),
            ("Blender / Bonsai", vec![("Naar Blender", Export.into()), ("Verbinding testen", Check.into())]),
        ],
        "Productie" => vec![
            ("Productiestaten exporteren", vec![("PDF", Export.into()), ("Excel", Export.into()), ("CSV", Export.into())]),
            ("CNC / Labels", vec![("CNC G-code", Export.into()), ("Labels PDF", Export.into())]),
            ("Planning / Optimalisatie", vec![("Zaagplan", planner_source_icon!("BarChart3")), ("Planning", planner_source_icon!("CalendarDays")), ("CNC", Export.into()), ("Inkoop", Open.into())]),
        ],
        "Beeld" => vec![
            ("Ongedaan maken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())]),
            ("Zoom", vec![("Inzoomen", planner_source_icon!("ZoomIn")), ("Uitzoomen", planner_source_icon!("ZoomOut"))]),
            ("Thema", vec![("Thema kiezen", Settings.into())]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup { label: label.into(), commands: items.into_iter().map(|(name, icon)| {
        let id = format!("frame:{tab}:{name}");
        Command::new(name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect())
}

/// Pile Plan ribbon on ffe979d3b859. View controls are labeled review
/// placeholders until the shared ribbon supports sliders and segmented picks.
fn pile_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "pile" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Plan" => vec![
            ("Project", vec![("Projectinformatie", planner_source_icon!("FolderOpen"))]),
            ("Inspecteren", vec![("Belastinglocaties", planner_source_icon!("Map")), ("Sonderingen", planner_source_icon!("Compass"))]),
            ("Selecteren", vec![("Kaderselectie", planner_source_icon!("Square"))]),
            ("Instellingen", vec![("Sonderingsinstellingen", Settings.into()), ("Kosteninstellingen", Settings.into()), ("Groeperingsinstellingen", Settings.into())]),
            ("Vergrendelen", vec![("Locaties vergrendelen", planner_source_icon!("Lock"))]),
            ("Optimalisatie", vec![("Uitvoeren", planner_source_icon!("Play"))]),
        ],
        "Weergave" => vec![
            ("Symbolen", vec![("Symboolgrootte · slider", planner_source_icon!("Gauge"))]),
            ("Benutting", vec![("Gewenst bereik · schuifregelaars", planner_source_icon!("Gauge"))]),
            ("Voorgrond", vec![("Belastinglocaties / sonderingen", planner_source_icon!("Layers"))]),
            ("Grid", vec![("Grid tonen", Grid.into())]),
            ("Gebieden", vec![("Puntniveaugebieden tonen", planner_source_icon!("LayoutGrid")), ("Groepen tonen", planner_source_icon!("Boxes"))]),
            ("Vensters", vec![("Verkenner tonen", PanelLeft.into()), ("Eigenschappen tonen", PanelRight.into())]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("pile:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// BIM Validator viewer ribbon on 8f837dd9a56e; disconnected BCF state shown.
fn validator_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "validator" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Project", vec![("Opslaan", Save.into()), ("Opslaan als", planner_source_icon!("SaveAll")), ("Openen", Open.into())]),
            ("Modellen", vec![("Toevoegen IFC", Import.into()), ("Verwijder", planner_source_icon!("Trash2"))]),
            ("Validatie", vec![("Valideer", Check.into()), ("IDS Standaard", planner_source_icon!("ListTree")), ("Reset", planner_source_icon!("RotateCcw"))]),
            ("BCF", vec![("Export BCF", Export.into()), ("Sync", planner_source_icon!("RefreshCw")), ("Inloggen", planner_source_icon!("Lock"))]),
        ],
        "Beeld" => vec![
            ("Panelen", vec![("Modellen", PanelLeft.into()), ("Validatie", PanelRight.into())]),
            ("3D Beeld", vec![("Passend", Fit.into()), ("Reset", planner_source_icon!("RotateCcw"))]),
            ("Doorsnede", vec![("Snijvlak X", planner_source_icon!("Columns3")), ("Snijvlak Y", planner_source_icon!("Columns3")), ("Snijvlak Z", planner_source_icon!("Columns3")), ("Wis snijvlakken", planner_source_icon!("Eraser"))]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("validator:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Reports Studio ribbon at 818e58118c0f: Start, Invoegen and Beeld.
fn reports_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "reports" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Klembord", vec![("Plakken", planner_source_icon!("ClipboardCheck")), ("Kopieer sectie", planner_source_icon!("Copy"))]),
            ("Blokken", vec![("Tekst", planner_source_icon!("FileText")), ("Berekening", planner_source_icon!("Hash")), ("Toets", Check.into()), ("Tabel", Grid.into()), ("Spreadsheet", Grid.into()), ("Afbeelding", planner_source_icon!("FilePlus2")), ("Kaart", planner_source_icon!("Map"))]),
            ("Pagina", vec![("Witruimte", planner_source_icon!("Minus")), ("Pagina-einde", planner_source_icon!("FilePlus2"))]),
            ("Controle", vec![("Valideren", Check.into())]),
            ("Uitvoer", vec![("PDF Genereren", Export.into()), ("Download PDF", Export.into())]),
        ],
        "Invoegen" => vec![
            ("Secties", vec![("Nieuw hoofdstuk", New.into()), ("Nieuwe bijlage", New.into())]),
            ("Inhoud", vec![("Tekst", planner_source_icon!("FileText")), ("Berekening", planner_source_icon!("Hash")), ("Toets", Check.into()), ("Tabel", Grid.into()), ("Afbeelding", planner_source_icon!("FilePlus2")), ("Kaart", planner_source_icon!("Map"))]),
        ],
        "Beeld" => vec![
            ("Weergave", vec![("Editor", planner_source_icon!("Pen")), ("Gesplitst", planner_source_icon!("Columns3")), ("JSON", planner_source_icon!("FileCode")), ("Preview", planner_source_icon!("Eye"))]),
            ("Panelen", vec![("Zijpaneel", PanelLeft.into())]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("reports:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Calculations has only Start and an intentionally empty IFC tab.
fn calculations_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "calculations" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Bestand", vec![("Nieuw", New.into()), ("Bladeren…", Open.into()), ("Opslaan", Save.into())]),
            ("Bewerken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())]),
            ("Invoegen", vec![("Module", planner_source_icon!("Puzzle")), ("Afbeelding", planner_source_icon!("FilePlus2"))]),
            ("Exporteren", vec![("Voorbeeld", planner_source_icon!("Eye")), ("PDF blad", Export.into()), ("Rapport (PDF)", Export.into())]),
        ],
        "IFC" => vec![],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("calculations:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Heatloss uses route-linked tabs; the IFC ribbon is intentionally empty.
fn heatloss_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "heatloss" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Vertrekken" => vec![
            ("Vertrekken", vec![("Nieuw vertrek", New.into())]),
            ("Zones", vec![("Zones beheren", planner_source_icon!("Building2"))]),
            ("Berekening", vec![("Bereken", planner_source_icon!("Play"))]),
        ],
        "Constructies" => vec![("Constructies", vec![("Nieuwe constructie", New.into()), ("Catalogus", planner_source_icon!("BookOpen"))])],
        "Modeller" => vec![
            ("Bewerken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into()), ("Leeg", planner_source_icon!("Trash2"))]),
            ("Selectie", vec![("Selecteer", planner_source_icon!("CircleDot"))]),
            ("Vormen", vec![("Rechthoek", planner_source_icon!("Square")), ("Polygoon", planner_source_icon!("Diamond")), ("Cirkel", planner_source_icon!("Circle"))]),
            ("Bouwelementen", vec![("Raam", planner_source_icon!("Columns3")), ("Deur", planner_source_icon!("PanelRight"))]),
        ],
        "IFC" => vec![],
        "Resultaten" => vec![("Rapport", vec![("Genereer rapport", planner_source_icon!("FileText"))]), ("Export", vec![("Export JSON", Export.into())])],
        "Rapport" => vec![("Rapport", vec![("Genereren", planner_source_icon!("FileText")), ("Download PDF", Export.into())])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("heatloss:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Source-aligned Geotechniek ribbon samples at 8182b48afc3f. IFC and
/// Berekeningen are dynamic status/list surfaces, represented as placeholders.
fn geotech_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "geotech" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Home" => vec![
            ("Project", vec![("Projectinfo", Settings.into())]),
            ("Weergave", vec![("Zoom -", planner_source_icon!("ZoomOut")), ("Passend", Fit.into())]),
        ],
        "Kaart" => vec![("Kaart", vec![("Meten", Measure.into()), ("Exporteer als afbeelding", Export.into())])],
        "Rapport" => vec![("Output", vec![("Genereer PDF", Export.into()), ("Open PDF", Open.into())])],
        "Situatietekening" => vec![
            ("Selecteer", vec![("Selecteren", planner_source_icon!("CircleDot"))]),
            ("Bewerken", vec![("Verplaatsen", planner_source_icon!("MoveHorizontal")), ("Kopiëren", planner_source_icon!("Copy")), ("Roteren", planner_source_icon!("RotateCw")), ("Verwijderen", planner_source_icon!("Trash2")), ("Trim", planner_source_icon!("Scissors")), ("Mirror", planner_source_icon!("GitCompareArrows"))]),
            ("Plaatsen", vec![("Sondering", planner_source_icon!("Compass")), ("Boring", planner_source_icon!("Compass")), ("Lijn", planner_source_icon!("Minus")), ("Maatlijn", Measure.into()), ("Vlak", planner_source_icon!("Square")), ("Opmerking", planner_source_icon!("Pen"))]),
            ("Overlay", vec![("Image/PDF import", Import.into()), ("Kader (SVG)", planner_source_icon!("Square")), ("Wis alles", planner_source_icon!("Eraser"))]),
            ("Export", vec![("Exporteer DWG", Export.into()), ("Exporteer PDF", Export.into()), ("Print", planner_source_icon!("Printer"))]),
        ],
        "Berekeningen" => vec![("Projectberekeningen", vec![("Dynamische berekeningenlijst", Grid.into())])],
        "IFC" => vec![("Automatisch gegenereerd", vec![("Live IFC4x3 + IFCX", Cube.into())])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("geotech:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Source-aligned command samples from Calc's ribbon components at b47042704efa.
/// Experimental and contextual tab visibility is recorded in app-layouts.json.
fn calc_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "calc" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Begroting" => vec![
            (
                "Regels",
                vec![
                    ("Hoofdstuk", planner_source_icon!("FilePlus2")),
                    ("Begr.post", planner_source_icon!("FileText")),
                    ("Bew.post", planner_source_icon!("ClipboardCheck")),
                    ("Rekenregel", planner_source_icon!("ListOrdered")),
                    ("Tekstregel", planner_source_icon!("FileType")),
                    ("Witregel", planner_source_icon!("ListTree")),
                    ("Verwijder", planner_source_icon!("Trash2")),
                ],
            ),
            (
                "Klembord",
                vec![
                    ("Plakken", planner_source_icon!("ClipboardCheck")),
                    ("Knippen", planner_source_icon!("Scissors")),
                    ("Kopiëren", planner_source_icon!("Copy")),
                ],
            ),
            (
                "Geschiedenis",
                vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())],
            ),
            ("Panelen", vec![("Hoeveelheid", Settings.into())]),
            (
                "Weergave",
                vec![
                    ("UI-1", Grid.into()),
                    ("UI-2", Grid.into()),
                    ("Simple", Grid.into()),
                    ("Inklappen", planner_source_icon!("ChevronsDownUp")),
                ],
            ),
            ("Prijzen", vec![("Prijzen %", Settings.into())]),
            (
                "Wijzigingen",
                vec![
                    ("Bijhouden", planner_source_icon!("ListOrdered")),
                    ("Wis markeringen", planner_source_icon!("Eraser")),
                    ("Hele regel", Grid.into()),
                    ("Alleen cel", Grid.into()),
                ],
            ),
            ("Project", vec![("Projectgegevens", Settings.into())]),
            (
                "Varianten",
                vec![
                    ("Varianten", planner_source_icon!("GitBranch")),
                    ("Optieset", planner_source_icon!("Layers")),
                ],
            ),
        ],
        "Rapportage" => vec![
            (
                "Rapportage",
                vec![
                    ("Opdrachtgever", planner_source_icon!("FileText")),
                    ("Intern", planner_source_icon!("FileText")),
                    ("Nacalculatie", planner_source_icon!("FileText")),
                ],
            ),
            (
                "Weergave",
                vec![
                    ("Hoeveelheden", Grid.into()),
                    ("Staand", planner_source_icon!("FileText")),
                    ("Liggend", planner_source_icon!("FileText")),
                ],
            ),
            (
                "Afdrukken",
                vec![("Afdrukken", planner_source_icon!("Printer"))],
            ),
            (
                "Export",
                vec![
                    ("PDF Export", Export.into()),
                    ("Excel Export", Export.into()),
                    ("IFC Export", Export.into()),
                ],
            ),
        ],
        "Spreadsheet" => vec![
            (
                "Werkbladen",
                vec![
                    ("Nieuw blad", New.into()),
                    ("Verwijder", planner_source_icon!("Trash2")),
                ],
            ),
            (
                "Opmaak",
                vec![
                    ("Vet", planner_source_icon!("FileType")),
                    ("Cursief", planner_source_icon!("FileType")),
                    ("Links", planner_source_icon!("IndentDecrease")),
                    ("Midden", planner_source_icon!("Columns3")),
                    ("Rechts", planner_source_icon!("IndentIncrease")),
                ],
            ),
            (
                "Getal",
                vec![
                    ("Valuta (€)", planner_source_icon!("Gauge")),
                    ("Percentage (%)", planner_source_icon!("Gauge")),
                    ("+Decimaal", planner_source_icon!("Plus")),
                    ("-Decimaal", planner_source_icon!("Minus")),
                ],
            ),
            (
                "Tekstgrootte",
                vec![
                    ("Groter", planner_source_icon!("ZoomIn")),
                    ("Kleiner", planner_source_icon!("ZoomOut")),
                ],
            ),
        ],
        "IFC" => vec![(
            "Rapport",
            vec![("Genereer", planner_source_icon!("FileText"))],
        )],
        "Offerte" => vec![
            (
                "Secties",
                vec![
                    ("Technisch", New.into()),
                    ("Opties", New.into()),
                    ("Vrij", New.into()),
                    ("Meerwerk", New.into()),
                ],
            ),
            (
                "Document",
                vec![
                    ("Gegevens", Settings.into()),
                    ("Termijnen", Settings.into()),
                    ("Garanties", Settings.into()),
                ],
            ),
            ("Export", vec![("PDF offerte", Export.into())]),
        ],
        "Tekstopmaak" => vec![
            (
                "Tekststijl",
                vec![
                    ("Vet", planner_source_icon!("FileType")),
                    ("Cursief", planner_source_icon!("FileType")),
                    ("Onderstr.", planner_source_icon!("FileType")),
                ],
            ),
            (
                "Grootte",
                vec![
                    ("Groter", planner_source_icon!("ZoomIn")),
                    ("Kleiner", planner_source_icon!("ZoomOut")),
                ],
            ),
            (
                "Uitlijning",
                vec![
                    ("Links", planner_source_icon!("IndentDecrease")),
                    ("Midden", planner_source_icon!("Columns3")),
                    ("Rechts", planner_source_icon!("IndentIncrease")),
                ],
            ),
        ],
        "3D" | "PDF" => vec![("Experimenteel", vec![("Nog niet beschikbaar", Help.into())])],
        _ => return None,
    };
    Some(
        spec.into_iter()
            .map(|(label, items)| RibbonGroup {
                label: label.into(),
                commands: items
                    .into_iter()
                    .map(|(name, icon)| {
                        let id = format!("calc:{tab}:{name}");
                        Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                            .selected(selected == Some(id.as_str()))
                    })
                    .collect(),
            })
            .collect(),
    )
}

/// The Planner groups follow its source ribbon registry at commit 5a65f6b865a7.
/// Only shared action meanings are canonical; domain vectors remain review assets.
fn planner_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "planner" {
        return None;
    }
    use Icon::*;
    let file: (&str, &[(&str, CommandIcon)]) = (
        "Bestand",
        &[
            ("Nieuw", New.into()),
            ("Openen", Open.into()),
            ("Opslaan", Save.into()),
            ("Opslaan als", planner_source_icon!("SaveAll")),
            ("Recent", planner_source_icon!("Clock")),
            ("Exporteren", Export.into()),
        ],
    );
    let edit: (&str, &[(&str, CommandIcon)]) = (
        "Bewerken",
        &[
            ("Ongedaan", Undo.into()),
            ("Opnieuw", Redo.into()),
            ("Verwijderen", planner_source_icon!("Trash2")),
        ],
    );
    let tasks: (&str, &[(&str, CommandIcon)]) = (
        "Taken",
        &[
            ("Taak", planner_source_icon!("Plus")),
            ("Mijlpaal", planner_source_icon!("Milestone")),
            ("Relatie", planner_source_icon!("Link")),
            ("Splitsen", planner_source_icon!("Scissors")),
        ],
    );
    let schedule: (&str, &[(&str, CommandIcon)]) =
        ("Planning", &[("Berekenen", planner_source_icon!("Play"))]);
    let progress: (&str, &[(&str, CommandIcon)]) = (
        "Voortgang",
        &[
            ("Voortgang importeren", planner_source_icon!("FileUp")),
            ("Voortgang exporteren", planner_source_icon!("FileDown")),
        ],
    );
    let spec: Vec<(&str, &[(&str, CommandIcon)])> = match tab {
        "Start" => vec![
            file,
            edit,
            tasks,
            schedule,
            (
                "Zoom",
                &[
                    ("Inzoomen", planner_source_icon!("ZoomIn")),
                    ("Uitzoomen", planner_source_icon!("ZoomOut")),
                ],
            ),
        ],
        "Planning" => vec![
            (
                "Planning",
                &[
                    ("Berekenen", planner_source_icon!("Play")),
                    ("Project verplaatsen", planner_source_icon!("CalendarClock")),
                    ("Waarschuwingen", planner_source_icon!("AlertTriangle")),
                ],
            ),
            (
                "Relaties",
                &[
                    ("Relatie", planner_source_icon!("Link")),
                    ("Splitsen", planner_source_icon!("Scissors")),
                ],
            ),
            (
                "Traceren",
                &[
                    ("Voorgangers", planner_source_icon!("MoveHorizontal")),
                    ("Opvolgers", planner_source_icon!("MoveHorizontal")),
                ],
            ),
            (
                "Kalender",
                &[("Kalender", planner_source_icon!("Calendar"))],
            ),
            (
                "Structuur",
                &[
                    ("Codevelden", planner_source_icon!("Tags")),
                    ("WBS automatisch", planner_source_icon!("Hash")),
                    ("WBS hernummeren", planner_source_icon!("ListOrdered")),
                    ("Inspringen", planner_source_icon!("IndentIncrease")),
                    ("Uitspringen", planner_source_icon!("IndentDecrease")),
                ],
            ),
            (
                "Basislijnen",
                &[("Basislijnen", planner_source_icon!("LayoutGrid"))],
            ),
            progress,
        ],
        "Resources" => vec![
            (
                "Resourcebeheer",
                &[
                    ("Resources", planner_source_icon!("Users")),
                    ("Resourcedock", CommandIcon::Canonical(PanelRight)),
                    ("Nieuwe resource", planner_source_icon!("Plus")),
                ],
            ),
            (
                "Toewijzing",
                &[("Toewijzen", planner_source_icon!("Users"))],
            ),
            (
                "Histogram",
                &[("Histogram", planner_source_icon!("BarChart3"))],
            ),
            (
                "Nivelleren",
                &[
                    ("Nivelleren", planner_source_icon!("Scale")),
                    ("Wissen", planner_source_icon!("Eraser")),
                ],
            ),
            (
                "Overbezetting",
                &[("Indicator", planner_source_icon!("AlertTriangle"))],
            ),
        ],
        "Weergave" => vec![
            (
                "Tijdschaal",
                &[("Tijdschaal", planner_source_icon!("CalendarDays"))],
            ),
            (
                "Overzicht",
                &[
                    ("Inklappen", planner_source_icon!("ChevronsDownUp")),
                    ("Uitklappen", planner_source_icon!("ChevronsUpDown")),
                ],
            ),
            ("Layout", &[("Layout", planner_source_icon!("LayoutGrid"))]),
            (
                "Presentatie",
                &[("Presentatie", planner_source_icon!("Eye"))],
            ),
            (
                "Panelen",
                &[
                    ("Eigenschappen", CommandIcon::Canonical(PanelRight)),
                    ("Resources", planner_source_icon!("Users")),
                ],
            ),
            (
                "Overlays",
                &[
                    ("Basislijn", planner_source_icon!("LayoutGrid")),
                    ("Voortgangslijn", planner_source_icon!("TrendingUp")),
                ],
            ),
        ],
        "Instellingen" => vec![
            (
                "Project",
                &[
                    ("Projectinformatie", planner_source_icon!("Info")),
                    ("Projectinstellingen", CommandIcon::Canonical(Settings)),
                ],
            ),
            (
                "Kalender",
                &[("Kalender", planner_source_icon!("Calendar"))],
            ),
            (
                "Sneltoetsen",
                &[("Sneltoetsen", planner_source_icon!("Keyboard"))],
            ),
        ],
        "Tabel" => vec![
            file,
            edit,
            tasks,
            schedule,
            (
                "Traceren",
                &[
                    ("Voorgangers", planner_source_icon!("MoveHorizontal")),
                    ("Opvolgers", planner_source_icon!("MoveHorizontal")),
                ],
            ),
            (
                "Kolommen",
                &[("Kolommen", planner_source_icon!("Columns3"))],
            ),
            progress,
        ],
        "IFC" => vec![("IFC", &[("IFC-informatie", planner_source_icon!("Info"))])],
        "Rapport" => vec![
            (
                "Rapportage",
                &[("Afdrukvoorbeeld", planner_source_icon!("Printer"))],
            ),
            progress,
        ],
        "AI" => vec![
            ("Server", &[("Server", planner_source_icon!("Settings"))]),
            ("Verbinding", &[("Verbinden", planner_source_icon!("Plug"))]),
            (
                "Veiligheid",
                &[("Veiligheid", planner_source_icon!("AlertTriangle"))],
            ),
            (
                "Activiteit",
                &[("Activiteit", planner_source_icon!("Activity"))],
            ),
        ],
        _ => return None,
    };
    Some(
        spec.into_iter()
            .map(|(label, items)| RibbonGroup {
                label: label.into(),
                commands: items
                    .iter()
                    .map(|(name, icon)| {
                        let id = format!("planner:{tab}:{name}");
                        Command::new(*name, *icon, Action::SelectPreviewCommand(id.clone()))
                            .selected(selected == Some(id.as_str()))
                    })
                    .collect(),
            })
            .collect(),
    )
}

fn base_groups(tab: &str, selected: Option<&str>) -> Vec<RibbonGroup<Action>> {
    use Icon::*;
    let spec: &[(&str, &[(&str, Icon)])] = match tab {
        "Start" => &[
            (
                "Project",
                &[("Nieuw", New), ("Openen", Open), ("Opslaan", Save)],
            ),
            (
                "Gegevens",
                &[("Importeren", Import), ("Exporteren", Export)],
            ),
            ("Navigatie", &[("Zoeken", Search), ("Passend", Fit)]),
            (
                "Schermen",
                &[("Weergave", Cube), ("Eigenschappen", PanelRight)],
            ),
        ],
        "Weergave" => &[
            (
                "Navigatie",
                &[("Passend", Fit), ("Weergave", Cube), ("Lagen", PanelLeft)],
            ),
            (
                "Vensters",
                &[("Eigenschappen", PanelRight), ("Instellingen", Settings)],
            ),
        ],
        "Help" => &[(
            "Ondersteuning",
            &[("Help", Help), ("Instellingen", Settings)],
        )],
        _ => &[
            (tab, &[("Nieuw", New), ("Openen", Open), ("Maat", Measure)]),
            (
                "Bewerken",
                &[("Zoeken", Search), ("Eigenschappen", PanelRight)],
            ),
            ("Uitvoer", &[("Exporteren", Export), ("Passend", Fit)]),
        ],
    };
    spec.iter()
        .map(|(label, items)| RibbonGroup {
            label: (*label).into(),
            commands: items
                .iter()
                .map(|(name, icon)| {
                    let id = format!("{tab}:{name}");
                    Command::new(*name, *icon, Action::SelectPreviewCommand(id.clone()))
                        .selected(selected == Some(id.as_str()))
                })
                .collect(),
        })
        .collect()
}

fn domain_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    let wanted: &[&str] = match (studio.id.as_str(), tab) {
        ("fem", "Geometrie") => &["Geometrie"],
        ("fem", "Randvoorwaarden") => &["Randvoorwaarden"],
        ("fem", "Belastingen") => &["Belastingen"],
        ("fem", "Net" | "Berekenen") => &["Net & berekening"],
        ("fem", "Resultaten") => &["Resultaten"],
        ("bim", "Modelleren") => &[
            "Project & referenties",
            "Bouwdelen",
            "Bewerken & informatie",
        ],
        ("bim", "Documenteren" | "Coördineren") => &["Documentatie & coördinatie"],
        _ => return None,
    };
    let mut groups: Vec<RibbonGroup<Action>> = Vec::new();
    for proposal in proposals()
        .iter()
        .filter(|item| item.domain == studio.id && wanted.contains(&item.group.as_str()))
    {
        let short = proposal.id.rsplit('.').next().unwrap_or_default();
        if studio.id == "fem"
            && tab == "Net"
            && !["mesh", "mesh-refine", "mesh-quality"].contains(&short)
        {
            continue;
        }
        if studio.id == "fem"
            && tab == "Berekenen"
            && ["mesh", "mesh-refine", "mesh-quality"].contains(&short)
        {
            continue;
        }
        let coordination = [
            "clash",
            "clearance",
            "bcf-issue",
            "ids-check",
            "ifc-export",
            "revision",
            "section-box",
        ]
        .contains(&short);
        if studio.id == "bim"
            && ((tab == "Documenteren" && coordination) || (tab == "Coördineren" && !coordination))
        {
            continue;
        }
        let bytes = domain_drafts::ALL
            .iter()
            .find(|(id, _)| *id == proposal.id)
            .expect("every proposal has a review SVG")
            .1;
        let command = Command::new(
            proposal.label.clone(),
            CommandIcon::Svg(bytes),
            Action::SelectPreviewCommand(proposal.id.clone()),
        )
        .selected(selected == Some(proposal.id.as_str()));
        match groups
            .iter_mut()
            .find(|group| group.label == proposal.group)
        {
            Some(group) => group.commands.push(command),
            None => groups.push(RibbonGroup {
                label: proposal.group.clone(),
                commands: vec![command],
            }),
        }
    }
    Some(groups)
}
