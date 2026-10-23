"""Draw inspectable 24px concept glyphs for every proposed FEM/BIM action.

These are design drafts, deliberately kept outside the distributable Rust crate.
"""
from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
proposals = json.loads((DESIGN / "domain-icon-proposals.json").read_text())

# Each entry is a distinct visual metaphor on the same 24x24 grid.
# The library deliberately uses one color, a 1.75px stroke and round joins.
FEM = {
    "node": '<path d="M4 20V4M4 20h16"/><circle cx="12" cy="12" r="2.3" fill="currentColor" stroke="none"/>',
    "beam": '<path d="M4 14h16"/><circle cx="4" cy="14" r="2"/><circle cx="20" cy="14" r="2"/>',
    "column": '<path d="M12 3v18"/><circle cx="12" cy="3" r="2"/><circle cx="12" cy="21" r="2"/>',
    "plate": '<path d="m5 5 14 2-2 12-12-2Z"/><circle cx="5" cy="5" r="1"/><circle cx="19" cy="7" r="1"/><circle cx="17" cy="19" r="1"/><circle cx="5" cy="17" r="1"/>',
    "shell": '<path d="M3 17c6-13 12-13 18 0M3 17c6 4 12 4 18 0"/><circle cx="3" cy="17" r="1"/><circle cx="21" cy="17" r="1"/>',
    "solid": '<path d="m12 2 9 5v10l-9 5-9-5V7l9-5ZM3 7l9 5 9-5M12 12v10"/>',
    "truss": '<path d="M3 19 12 4l9 15H3ZM7 12h10M12 4v15"/><circle cx="3" cy="19" r="1"/><circle cx="21" cy="19" r="1"/>',
    "rigid-link": '<path d="M4 9h16M4 15h16M4 9v6M20 9v6"/><circle cx="4" cy="12" r="2"/><circle cx="20" cy="12" r="2"/>',
    "offset": '<path d="M3 7h9v9h9M12 7l3-3M12 16l-3 3"/><path d="M12 7v9" stroke-dasharray="2 2"/>',
    "local-axes": '<path d="M6 18V5m0 13h13M6 18l8-8M6 5l-2 3m2-3 2 3m11 10-3-2m3 2-3 2m-2-10-1 3m1-3-3 1"/>',
    "section": '<path d="M4 4h16M8 4v16m8-16v16M4 20h16"/>',
    "material": '<path d="M4 4h16v16H4zM5 12l7-7M5 19 19 5M12 19l7-7"/>',
    "fixed-support": '<path d="M5 4v16M5 12h15M2 6l3-3M2 12l3-3M2 18l3-3"/>',
    "pinned-support": '<path d="M12 5v6m-6 7 6-7 6 7H6Zm-2 2h16"/><circle cx="12" cy="5" r="2"/>',
    "roller-support": '<path d="M12 3v7m-6 6 6-6 6 6H6Zm-2 5h16"/><circle cx="9" cy="18" r="1.6"/><circle cx="15" cy="18" r="1.6"/>',
    "spring-support": '<path d="M12 3v4l-3 2 6 3-6 3 3 2v3M5 21h14"/>',
    "rotational-spring": '<path d="M7 12a5 5 0 1 1 5 5h-2m2-10a3 3 0 1 1-3 3M4 20h16"/>',
    "release": '<path d="M3 12h8m4 0h6"/><circle cx="13" cy="12" r="2"/><circle cx="3" cy="12" r="1"/><circle cx="21" cy="12" r="1"/>',
    "prescribed-displacement": '<path d="M4 19h16M12 6v10m-3-3 3 3 3-3"/><circle cx="12" cy="5" r="2"/>',
    "diaphragm": '<path d="M4 6h16v12H4zM4 6l16 12M20 6 4 18"/><circle cx="4" cy="6" r="1"/><circle cx="20" cy="18" r="1"/>',
    "contact": '<path d="M3 8h18M3 16h18M9 12V9m-2 2 2-2 2 2m4 1v3m-2-2 2 2 2-2"/>',
    "point-load": '<path d="M12 2v13m-3-3 3 3 3-3M5 20h14"/><circle cx="12" cy="18" r="2"/>',
    "line-load": '<path d="M4 19h16M6 3v12m-2-2 2 2 2-2m4-10v12m-2-2 2 2 2-2m4-10v12m-2-2 2 2 2-2"/>',
    "surface-load": '<path d="m4 15 12-3 4 7-12 3-4-7ZM7 3v8m-2-2 2 2 2-2m5-7v8m-2-2 2 2 2-2m5-9v8m-2-2 2 2 2-2"/>',
    "moment": '<path d="M18 8a7 7 0 1 0 1 8M18 4v4h-4"/><circle cx="12" cy="12" r="2"/>',
    "self-weight": '<path d="m5 5 6-3 6 3v7l-6 3-6-3V5Zm0 0 6 3 6-3m-6 3v7m7 0v7m-3-3 3 3 3-3"/>',
    "thermal-load": '<path d="M3 16h12M17 4v11a3 3 0 1 1-3 0V4a1.5 1.5 0 0 1 3 0ZM15.5 9v8"/>',
    "settlement": '<path d="M5 11h14m-12 5 5-5 5 5H7Zm-2 4h14M20 4v11m-2-3 2 3 2-3"/>',
    "load-case": '<path d="M4 3h11l4 4v14H4V3Zm11 0v4h4M11 9v7m-2-2 2 2 2-2"/>',
    "load-combination": '<path d="M6 3v11m-2-2 2 2 2-2m12-9v11m-2-2 2 2 2-2M6 19h12m-6-3v6"/>',
    "moving-load": '<path d="M4 20h16M6 4v10m-2-2 2 2 2-2M7 17h11m-3-2 3 2-3 2"/>',
    "wind-load": '<path d="M17 3v18M3 7h10m-3-3 3 3-3 3M3 13h10m-3-3 3 3-3 3M3 19h10m-3-3 3 3-3 3"/>',
    "mass": '<path d="M4 4h16v16H4z"/><circle cx="12" cy="12" r="3" fill="currentColor" stroke="none"/>',
    "mesh": '<path d="M3 4h18v16H3zM3 4l9 8 9-8M3 20l9-8 9 8M12 12V4m0 8v8"/>',
    "mesh-refine": '<path d="M3 20 12 3l9 17H3ZM7 12h10m-10 0 5 8 5-8M12 3v17"/>',
    "mesh-quality": '<path d="M3 20 12 3l9 17H3ZM8 14l3 3 5-6"/>',
    "solve-linear": '<path d="M4 4h11v11H4zM4 9h11M9 4v11m8-6 4 3-4 3M15 12h6"/>',
    "solve-nonlinear": '<path d="M3 20V4m0 16h18M6 16c3 0 3-8 7-8s3 7 8-3"/><path d="M16 5h5v5"/>',
    "buckling": '<path d="M8 3h8M8 21h8M12 3c-6 6 6 12 0 18M18 7l3 3-3 3"/>',
    "modal": '<path d="M3 12c3-10 6 10 9 0s6-10 9 0M3 19h18"/>',
    "convergence": '<path d="M3 4v16h18M5 7c4 11 8 11 15 5M5 17c4-7 8-7 15-5"/>',
    "stop-solver": '<circle cx="12" cy="12" r="9"/><path d="M9 9h6v6H9z" fill="currentColor" stroke="none"/>',
    "deformation": '<path d="M3 17h18" stroke-dasharray="2 2"/><path d="M3 17c5-1 7-11 11-11s5 10 7 11"/><circle cx="3" cy="17" r="1"/><circle cx="21" cy="17" r="1"/>',
    "reaction": '<path d="M4 20h16M7 17l5-6 5 6H7ZM12 11V3m-3 3 3-3 3 3"/>',
    "normal-force": '<path d="M7 12h10M2 12h5m-3-3-3 3 3 3m13-3h5m-3-3 3 3-3 3"/>',
    "shear-force": '<path d="M4 12h16M8 3v7m-2-2 2 2 2-2m6 6v7m-2-2 2 2 2-2"/>',
    "bending-moment": '<path d="M3 17c5-7 13-7 18 0M4 8c1 4 4 5 6 4m-6-4 1 4m15-4c-1 4-4 5-6 4m6-4-1 4"/>',
    "torsion": '<path d="M6 7h12v10H6zM6 7c-4 2-4 8 0 10m12-10c4 2 4 8 0 10M9 3c6-3 10 2 10 5m0 0-3-1m3 1 1-3"/>',
    "stress": '<path d="M8 8h8v8H8zM2 12h5m-2-2 2 2-2 2m17-2h-5m2-2-2 2 2 2M12 2v5m-2-2 2 2 2-2m-2 17v-5m-2 2 2-2 2 2"/>',
    "utilization": '<path d="M4 18a8 8 0 0 1 16 0M12 18l5-7M4 21h16"/><circle cx="12" cy="18" r="1.5"/>',
    "envelope": '<path d="M3 19V5m0 14h18M5 16c4-8 8-8 15-4M5 12c4-6 8-4 15-8"/>',
    "result-probe": '<path d="M12 2v20M2 12h20"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>',
}

BIM = {
    "site": '<path d="M2 17c4-5 6 3 10-2s7-1 10-5M2 21h20M5 8l3-4 3 4H5Zm3 0v6"/>',
    "building": '<path d="M4 21V6l8-4 8 4v15H4ZM4 10h16M8 6h2m4 0h2M8 14h2m4 0h2M10 21v-5h4v5"/>',
    "storey": '<path d="M3 5h18M3 12h18M3 19h18M6 5v14m12-14v14"/>',
    "grid": '<path d="M6 2v20M18 2v20M2 7h20M2 17h20"/><circle cx="6" cy="7" r="1"/><circle cx="18" cy="17" r="1"/>',
    "level": '<path d="M3 12h12"/><circle cx="18" cy="12" r="3"/><path d="M17 12h2"/>',
    "survey-point": '<path d="M12 22s-7-7-7-12a7 7 0 1 1 14 0c0 5-7 12-7 12Z"/><circle cx="12" cy="10" r="2"/>',
    "project-origin": '<path d="M12 21V3M3 12h18m-9-9-3 3m3-3 3 3m6 6-3-3m3 3-3 3"/><circle cx="12" cy="12" r="2"/>',
    "link-model": '<path d="m3 7 5-3 5 3v6l-5 3-5-3V7Zm8 5 5-3 5 3v6l-5 3-5-3v-6M8 16l3-4"/>',
    "federate": '<path d="m3 8 6-4 6 4v8l-6 4-6-4V8Zm6 0 6-4 6 4v8l-6 4-6-4M3 8l6 4 6-4m0 4 6-4"/>',
    "wall": '<path d="M3 5h18v5H3zM3 14h18v5H3zM9 5v5m6 4v5"/>',
    "curtain-wall": '<path d="M3 3h18v18H3zM9 3v18m6-18v18M3 9h18M3 15h18"/>',
    "slab": '<path d="m3 10 14-6 4 4-14 6-4-4Zm0 0v5l4 4 14-6V8M7 14v5"/>',
    "roof": '<path d="m2 12 10-9 10 9M5 10v10h14V10M9 20v-6h6v6"/>',
    "door": '<path d="M4 3h16v18H4V3Zm4 18V7l10 14M8 7a14 14 0 0 1 10 14"/>',
    "window": '<path d="M3 4h18v16H3zM12 4v16M3 12h18M6 7l3-3m6 16 3-3"/>',
    "beam": '<path d="M2 7h20v4H2zM5 11v5h14v-5M3 20h18"/>',
    "column": '<path d="M8 2h8v20H8zM5 2h14M5 22h14"/>',
    "footing": '<path d="M9 3h6v10H9zM5 13h14v5H5zM2 21h20"/>',
    "pile": '<path d="M3 8h18M10 3h4v17l-2 3-2-3V3ZM5 8v5m14-5v5"/>',
    "stair": '<path d="M3 20h5v-5h5v-5h5V5h3M3 15v5m5-5v5m5-10v5m5-10v5"/>',
    "ramp": '<path d="M3 20 20 5v15H3ZM6 16l9-8m-2 0h2v2"/>',
    "railing": '<path d="M3 5h18M3 19h18M5 5v14m5-14v14m5-14v14m5-14v14"/>',
    "opening": '<path d="M3 3h18v18H3zM8 8h8v8H8zM3 8h3m12 0h3M3 16h3m12 0h3"/>',
    "space": '<path d="M3 3h18v18H3V3Zm9 0v8h9M3 15h7v6"/><circle cx="14" cy="15" r="2"/>',
    "zone": '<path d="M3 3h18v18H3zM12 3v18M3 12h18"/><path d="m6 8 2 2 2-2m4 7 2 2 2-2"/>',
    "site-element": '<path d="M2 20c5-4 9 1 20-5M12 17V6m-5 6 5-9 5 9H7Z"/>',
    "join": '<path d="M3 5h8v8H3zM13 11h8v8h-8zM9 11l6 2"/>',
    "unjoin": '<path d="M2 5h8v8H2zM14 11h8v8h-8zM9 15l6-6"/><path d="M7 19h3m4 0h3"/>',
    "trim": '<path d="M3 4v16M3 12h18M16 4l5 5m0-5-5 5"/>',
    "extend": '<path d="M4 5v15M4 13h11"/><path d="M15 13h6" stroke-dasharray="2 2"/><path d="M18 4v16"/>',
    "align": '<path d="M4 4v16M8 7h12M8 12h8M8 17h12"/><path d="M4 7h3m-3 5h3m-3 5h3"/>',
    "offset": '<path d="M4 5v14M12 5v14M20 5v14M5 12h6m-3-3-3 3 3 3m5-3h6m-3-3 3 3-3 3"/>',
    "array": '<path d="M2 7h5v5H2zM9 7h5v5H9zM16 7h5v5h-5zM2 16h5v5H2zM9 16h5v5H9zM16 16h5v5h-5z"/>',
    "mirror": '<path d="M12 2v20" stroke-dasharray="2 2"/><path d="M3 18 9 5v13H3Zm18 0L15 5v13h6Z"/>',
    "type": '<path d="M3 5h12v13H3zM7 2h12v13M5 9h8M5 13h6"/>',
    "instance": '<path d="M5 4h14v16H5zM9 8h6v8H9z"/><circle cx="18" cy="5" r="2" fill="currentColor" stroke="none"/>',
    "property-set": '<path d="M4 3h16v18H4zM4 8h16M9 8v13M6 12h1m4 0h6M6 17h1m4 0h6"/>',
    "classification": '<path d="M4 4h7v5H4zM13 4h7v5h-7zM8 15h12v5H8zM8 9v6m8-6v6"/>',
    "material-layers": '<path d="M3 5h18v3H3zM3 11h18v3H3zM3 17h18v3H3z"/>',
    "quantity": '<path d="M4 20V4m0 16h17M7 13h3v7H7zM12 9h3v11h-3zM17 5h3v15h-3z"/>',
    "phasing": '<path d="M3 5h18M3 12h18M3 19h18M7 3v18M15 3v18"/><circle cx="7" cy="12" r="2"/>',
    "plan": '<path d="M3 3h18v18H3zM3 10h12m0-7v12M9 10v11M15 15h6"/>',
    "section": '<path d="M4 3h16v18H4zM4 9h16M7 9v12m6-12v12m7-6-6 6"/>',
    "elevation": '<path d="M3 20h18M5 20V6l7-4 7 4v14M9 9h2v3H9zm5 0h2v3h-2zM10 20v-5h4v5"/>',
    "sheet": '<path d="M4 2h16v20H4zM7 5h10v11H7zM7 19h6m2 0h2"/>',
    "viewport": '<path d="M3 2h18v20H3zM6 5h12v11H6zM6 18h7"/><path d="m9 13 3-5 3 5"/>',
    "dimension": '<path d="M5 5v14m14-14v14M5 13h14m-11-2-3 2 3 2m8-4 3 2-3 2"/>',
    "tag": '<path d="M3 4h13l5 8-5 8H3V4ZM6 9h8M6 14h6"/><circle cx="17" cy="12" r="1"/>',
    "schedule": '<path d="M3 3h18v18H3zM3 8h18M3 13h18M3 18h18M10 3v18"/>',
    "detail": '<circle cx="10" cy="10" r="6"/><path d="m14 14 7 7M7 10h6m-3-3v6"/>',
    "clash": '<path d="m3 7 7-4 7 4v8l-7 4-7-4V7Zm7 0 7-4 4 3v8l-4 3M3 7l7 4 7-4"/><path d="m15 15 5 5m0-5-5 5"/>',
    "clearance": '<path d="M3 5h5v14H3zM16 5h5v14h-5zM8 12h8m-5-2-3 2 3 2m2-4 3 2-3 2"/>',
    "bcf-issue": '<path d="M3 4h18v13H8l-5 4V4ZM12 7v5m0 2h.01"/>',
    "ids-check": '<path d="M12 2 20 5v6c0 5-3 8-8 11-5-3-8-6-8-11V5l8-3ZM8 12l3 3 5-6"/>',
    "ifc-export": '<path d="m3 6 7-4 7 4v10l-7 4-7-4V6Zm0 0 7 4 7-4m-7 4v10M17 12h5m-2-2 2 2-2 2"/>',
    "revision": '<path d="M3 4h10v15H3zM11 6h10v15H11zM5 8h6m-6 4h4m5 0h5m-5 4h5"/>',
    "section-box": '<path d="m12 2 9 5v10l-9 5-9-5V7l9-5ZM3 7l9 5 9-5M12 12v10"/><path d="M7 5v14m10-14v14" stroke-dasharray="2 2"/>',
}

ART = {"fem": FEM, "bim": BIM}
# At 16 px these concepts lose their distinctive interior lines. The small
# glyphs retain the same metaphor with fewer strokes; all others use the 24 px
# drawing at smaller scale until they have been individually reviewed.
SMALL = {
    "fem.local-axes": '<path d="M5 19V5m0 14h14M5 19l8-8M3 8l2-3 2 3m9 9 3 2-3 2"/>',
    "fem.wind-load": '<path d="M19 3v18M3 8h11m-3-3 3 3-3 3M3 16h11m-3-3 3 3-3 3"/>',
    "fem.diaphragm": '<path d="M4 5h16v14H4zM4 5l16 14"/><circle cx="4" cy="5" r="1.3" fill="currentColor" stroke="none"/><circle cx="20" cy="19" r="1.3" fill="currentColor" stroke="none"/>',
    "fem.mesh": '<path d="M3 4h18v16H3zM3 4l18 16M3 20l9-8"/>',
    "fem.mesh-refine": '<path d="M3 20 12 4l9 16H3ZM8 20l4-8 4 8"/>',
    "fem.surface-load": '<path d="m4 15 12-3 4 7-12 3-4-7ZM8 3v9m-2-2 2 2 2-2m8-9v7m-2-2 2 2 2-2"/>',
    "bim.federate": '<path d="M3 4h12v12H3zM9 10h12v12H9z"/>',
    "bim.curtain-wall": '<path d="M3 3h18v18H3zM12 3v18M3 12h18"/>',
    "bim.opening": '<path d="M3 3h18v18H3zM8 8h8v13H8z"/>',
    "bim.space": '<path d="M3 3h18v18H3V3Zm9 0v8M3 15h8"/><circle cx="15" cy="15" r="2" fill="currentColor" stroke="none"/>',
    "bim.zone": '<path d="M3 3h18v18H3zM12 3v18"/><circle cx="8" cy="12" r="1.2" fill="currentColor" stroke="none"/><circle cx="16" cy="12" r="1.2" fill="currentColor" stroke="none"/>',
    "bim.array": '<path d="M3 5h8v9H3zM13 10h8v9h-8z"/>',
    "bim.revision": '<path d="M3 4h12v15H3zM9 7h12v15H9zM12 12h6"/>',
    "bim.section-box": '<path d="M12 2 21 7v10l-9 5-9-5V7l9-5ZM3 7l9 5 9-5M12 12v10"/><path d="M4 15h16" stroke-dasharray="2 2"/>',
    "bim.level": '<path d="M3 12h12"/><circle cx="18" cy="12" r="3"/>',
    "bim.survey-point": '<path d="M12 21s-7-7-7-12a7 7 0 1 1 14 0c0 5-7 12-7 12Z"/><circle cx="12" cy="9" r="2"/>',
    "bim.project-origin": '<path d="M12 3v18M3 12h18"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
}
drafts = []
for proposal in proposals:
    domain, name = proposal["id"].split(".", 1)
    if name not in ART[domain]:
        raise KeyError(f"Missing icon drawing: {proposal['id']}")
    body = ART[domain][name]
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        'viewBox="0 0 24 24" fill="none" stroke="#36363E" '
        'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
        + body + '</svg>\n'
    )
    ET.fromstring(svg)
    path = DESIGN / "icon-drafts" / domain / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    draft = {
        "id": proposal["id"], "domain": domain, "group": proposal["group"],
        "label": proposal["label"], "visual_metaphor": proposal["visual_metaphor"],
        "file": str(path.relative_to(DESIGN)),
        "sha256": hashlib.sha256(svg.encode()).hexdigest(),
        "status": "visual-draft",
    }
    if proposal["id"] in SMALL:
        small_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" '
            'viewBox="0 0 24 24" fill="none" stroke="#36363E" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            + SMALL[proposal["id"]] + '</svg>'
        )
        small_path = DESIGN / "icon-drafts-small" / domain / f"{name}.svg"
        small_path.parent.mkdir(parents=True, exist_ok=True)
        ET.fromstring(small_svg)
        small_path.write_text(small_svg)
        draft["small_file"] = str(small_path.relative_to(DESIGN))
        draft["small_sha256"] = hashlib.sha256(small_svg.encode()).hexdigest()
    drafts.append(draft)
for domain, drawings in ART.items():
    unused = set(drawings) - {p["id"].split(".", 1)[1] for p in proposals if p["domain"] == domain}
    if unused:
        raise ValueError(f"Unused {domain} drawings: {unused}")
(DESIGN / "domain-icon-drafts.json").write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + "\n")
print(f"Generated {len(drafts)} vector concept icons")
