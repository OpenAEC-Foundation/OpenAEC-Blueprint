//! Native rendition of the proposed ribbon groups in design/harmonized-template.html.
//! FEM/BIM SVGs are review drafts, supplied as application-owned vectors.
use super::*;

pub(super) fn studio_tabs(studio: &StudioLayout, selected: Option<&str>) -> Vec<RibbonTab<Action>> {
    studio
        .tabs
        .iter()
        .filter(|tab| tab.as_str() != "Bestand")
        .map(|tab| RibbonTab {
            id: tab.to_lowercase(),
            label: tab.clone(),
            groups: domain_groups(studio, tab, selected)
                .unwrap_or_else(|| base_groups(tab, selected)),
        })
        .collect()
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
