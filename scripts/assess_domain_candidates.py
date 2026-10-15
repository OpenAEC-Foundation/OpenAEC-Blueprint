"""Record a source-context assessment for every FEM/BIM filename match."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
PROPOSALS = json.loads((DESIGN / "domain-icon-proposals.json").read_text())

# Ordered against candidate_assets; each filename is asserted below so a
# regenerated inventory cannot silently attach an assessment to a new icon.
# same = same user-facing meaning, related = same visual/domain family but a
# different action, different = a filename collision. These are semantic
# assessments, never a licensing or final visual-adoption decision.
ASSESSMENTS = {
    "fem.node": [
        ("node.svg", "related", "Object-snap naar een CAD-knooppunt; geen FEM-knoop aanmaken."),
        ("node_graph.svg", "different", "Node-editor/diagram, niet een constructieve knoop."),
    ],
    "fem.shell": [
        ("shell.svg", "related", "CAD-shell maakt een volume hol; het resultaat lijkt op een schaal, maar is geen FEM-schaalelement."),
    ],
    "fem.solid": [
        ("solid.svg", "related", "Pointcloud-solidweergave, niet een volume-element in een FEM-model."),
        ("hatch_solid.svg", "different", "Effen arcering is een vlakvulling, geen volume-element."),
        ("polysolid.svg", "related", "CAD-polysolid maakt een volume; een FEM-solid heeft knopen en elementtopologie."),
        ("solid.svg", "related", "CAD-solidstijl/volume, niet de FEM-elementdefinitie."),
    ],
    "fem.offset": [
        ("offset.svg", "related", "CAD-offset verplaatst geometrie; FEM-excentriciteit beschrijft een verschoven staafas."),
    ],
    "fem.section": [
        ("browser_section.svg", "different", "Documentboom voor een doorsnedetekening, geen profieltype."),
        ("section_box.svg", "different", "Snedebox van een 3D-scène, geen I-profiel."),
        ("section_drawing.svg", "different", "Een doorsnedetekening maken is geen staafdoorsnede kiezen."),
        ("intersection.svg", "different", "CAD-snap op een snijpunt, geen profieldoorsnede."),
    ],
    "fem.mesh": [
        ("closed_mesh.svg", "related", "Gesloten pointcloud-oppervlaktenet; geen FEM-discretisatie."),
        ("mesh_pointcloud.svg", "related", "Net uit puntenwolk; meshingprincipe verwant, invoer en resultaat anders."),
        ("mesh_surface.svg", "related", "Oppervlaktesmesh uit scan; mogelijk bruikbaar beeldmotief, ander commando."),
        ("mesh_terrain.svg", "related", "Terreinmesh uit punten; geen FEM-elementennet."),
        ("mesh_to_plans.svg", "different", "Workflow van mesh naar plattegronden, niet net genereren."),
    ],
    "bim.grid": [
        ("grid.svg", "different", "Object-snap op raster, geen BIM-stramien plaatsen."),
        ("grid.svg", "related", "Generiek CAD-raster; stramien heeft bouwkundige assen en labels."),
    ],
    "bim.window": [
        ("zoom_window.svg", "different", "Venster is hier een zoomrechthoek, geen bouwkundig raam."),
    ],
    "bim.space": [
        ("dim_space.svg", "different", "Maatvoering van tussenruimte, geen BIM-ruimteobject."),
        ("spacemouse.svg", "different", "3D-navigatieapparaat, geen gebouwruimte."),
    ],
    "bim.join": [
        ("modify_join.svg", "related", "CAD-geometrie verbinden; BIM-aansluiting heeft objectsemantiek."),
        ("vports_join.svg", "different", "Weergavevensters samenvoegen, geen bouwdelen."),
    ],
    "bim.trim": [
        ("trim.svg", "same", "Algemene trimactie op geometrie; betekenis sluit aan bij het BIM-bewerkcommando."),
    ],
    "bim.extend": [
        ("extend.svg", "same", "Algemene verlengactie tot begrenzing; dezelfde bewerkbetekenis."),
    ],
    "bim.align": [
        ("align_bottom.svg", "related", "Specifiek onder uitlijnen, niet de algemene referentie-uitlijning."),
        ("align_hcenter.svg", "related", "Specifiek horizontaal centreren, niet de algemene uitlijnactie."),
        ("align_left.svg", "related", "Specifiek links uitlijnen, niet de algemene uitlijnactie."),
        ("align_right.svg", "related", "Specifiek rechts uitlijnen, niet de algemene uitlijnactie."),
        ("align_top.svg", "related", "Specifiek boven uitlijnen, niet de algemene uitlijnactie."),
        ("align_vcenter.svg", "related", "Specifiek verticaal centreren, niet de algemene uitlijnactie."),
        ("dim_aligned.svg", "different", "Uitgelijnde maatlijn is annotatie, geen objectuitlijning."),
        ("mleader_align.svg", "different", "Tekstleiders uitlijnen is een annotatieactie."),
        ("modify_align.svg", "same", "Generieke CAD-objectuitlijning aan een referentie."),
    ],
    "bim.offset": [
        ("offset.svg", "related", "CAD-lijnen parallel verschuiven; BIM-variant werkt op wanden/bouwdelen."),
    ],
    "bim.array": [
        ("array_path.svg", "related", "Reeks langs een pad; specifieke variant van de algemene BIM-reeks."),
        ("array_polar.svg", "related", "Polaire reeks; specifieke variant van de algemene BIM-reeks."),
        ("array_rect.svg", "related", "Rechthoekige reeks; specifieke variant van de algemene BIM-reeks."),
    ],
    "bim.mirror": [
        ("mirror.svg", "same", "Objecten spiegelen om een as is dezelfde generieke bewerkactie."),
    ],
    "bim.plan": [
        ("browser_plan.svg", "same", "Boomicoon voor een plattegrondweergave."),
        ("mesh_to_plans.svg", "related", "Maakt plattegronden via een scanworkflow; geen plattegrondweergave op zich."),
    ],
    "bim.section": [
        ("browser_section.svg", "same", "Boomicoon voor een bouwkundige doorsnedetekening."),
        ("section_box.svg", "related", "3D-snedebox, geen 2D-doorsnedeweergave."),
        ("section_drawing.svg", "related", "Maakt een doorsnedetekening; het concept is een doorsnedeweergave."),
        ("intersection.svg", "different", "Object-snap op een snijpunt, geen doorsnede."),
    ],
    "bim.elevation": [
        ("browser_elevation.svg", "same", "Boomicoon voor een aanzichtweergave."),
    ],
    "bim.sheet": [
        ("browser_sheet.svg", "same", "Boomicoon voor een tekenblad."),
        ("layout_tabs.svg", "related", "Bediening van layouttabs, niet het bladobject zelf."),
        ("sheetset.svg", "related", "Een verzameling bladen, niet één tekenblad."),
    ],
    "bim.viewport": [
        ("viewport.svg", "same", "Modelvenster op een layoutblad is hetzelfde documentconcept."),
    ],
    "bim.dimension": [
        ("annotation_dimension.svg", "same", "Maatlijnannotatie met getuigenlijnen; dezelfde betekenis."),
    ],
    "bim.bcf-issue": [
        ("browser_bcf.svg", "related", "BCF-groep in de projectboom, geen individuele issue."),
    ],
    "bim.section-box": [
        ("section_box.svg", "same", "3D-snedebox voor het begrenzen van een modelweergave."),
    ],
}

matches = [proposal for proposal in PROPOSALS if proposal["candidate_assets"]]
assert set(ASSESSMENTS) == {proposal["id"] for proposal in matches}
records = []
for proposal in matches:
    decisions = ASSESSMENTS[proposal["id"]]
    candidates = proposal["candidate_assets"]
    assert len(decisions) == len(candidates), proposal["id"]
    for candidate, (name, decision, rationale) in zip(candidates, decisions):
        assert Path(candidate["path"]).name == name, (proposal["id"], candidate, name)
        assert decision in {"same", "related", "different"}
        records.append({
            "proposal": proposal["id"],
            "repo": candidate["repo"],
            "path": candidate["path"],
            "semantic_assessment": decision,
            "rationale": rationale,
            "status": "source-context-preliminary",
        })
assert len(records) == 54
(DESIGN / "domain-candidate-assessment.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
from collections import Counter
print(Counter(record["semantic_assessment"] for record in records))
