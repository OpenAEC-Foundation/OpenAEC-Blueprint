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
                .or_else(|| domain_groups(studio, tab, selected))
                .unwrap_or_else(|| base_groups(tab, selected)),
        })
        .collect()
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
