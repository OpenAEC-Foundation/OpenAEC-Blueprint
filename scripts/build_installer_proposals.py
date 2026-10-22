#!/usr/bin/env python3
"""Build four from-scratch proposals for the OpenAEC Installer in one page.

Output: design/ontwerp-0.4/installer-voorstellen.html. The proposals use the
colours, radii, buttons, gradients and shadows of https://www.open-aec.com/,
the B2 icons by Codex (inlined, so the page also works from disk) and the tool
screenshots of the real installer (openaec-installer at 8b39bae). Disciplines,
statuses, versions and commit counts come from the website's ecosystem section
as read on 2026-10-22. One deliberate difference from the website: text on the
amber primary button stays dark (#1C1917), as decided for contrast.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design/ontwerp-0.4/installer-voorstellen.html"
ICONS = ROOT / "design/icon-set-b2/svg"
PREVIEWS = "../../harmonization/references/openaec-installer/public/previews/"

ICON_NAMES = {
    "16": ["software.install", "software.update", "software.launch", "software.open-webtab", "link.open-external",
           "git.repository", "ui.check-updates", "view.search", "status.info", "status.success", "ui.settings",
           "window.minimize", "window.maximize", "window.close", "tree.expand", "nav.home", "stats.downloads",
           "product.open-source", "status.update-available"],
    "24": ["data.table", "report.document", "planning.gantt", "draw.polyline", "frame.calculation", "geo.sondering",
           "ifc.validate", "audio.speech", "energy.fetch-label", "field.list", "geo.coordinate-tag", "software.install",
           "software.update", "software.launch", "nav.home", "project.folder"],
}

# Catalogue of the real installer; disciplines, website status, version and commits from open-aec.com.
TOOLS = [
    # id, name, kind, category, icon, preview, disciplines, site status, latest, commits, installed, description
    ("calc", "Open Calc Studio", "desktop", "Calculatie", "data.table", "open-calc-studio", "CI", "", "0.13", 96, "0.13", "Open source calculatie en begroting voor de bouwsector, met AI-assistent."),
    ("pdf", "Open PDF Studio", "desktop", "Documenten", "report.document", "open-pdf-studio", "AECI", "", "2026.43", 1459, "2026.40", "PDF's bekijken, bewerken en annoteren, gericht op bouwdocumentatie en tekeningen."),
    ("planner", "Open Planner Studio", "desktop", "Planning", "planning.gantt", "open-planner-studio", "ACI", "Beta", "2026.10", 4569, "2026.10", "Open source projectplanning en werkcoördinatie voor bouwprojecten."),
    ("2d", "Open 2D Studio", "desktop", "CAD", "draw.polyline", "open-2d-studio", "AEC", "", "0.6", 0, None, "2D tekeningen en documenten bekijken en bewerken."),
    ("cad", "Open CAD Studio", "desktop", "CAD", "draw.polyline", "open-cad-studio", "AEC", "Community", "2026.42", 5516, None, "Volwaardige 2D + 3D CAD-applicatie met DWG/DXF-ondersteuning."),
    ("calculations", "Open Calculations Studio", "desktop", "Constructief", "frame.calculation", "open-calculations-studio", "EI", "In ontwikkeling", "2026.39", 306, "2026.35", "Constructieve handberekeningen met CalcPAD-syntax, herleidbaar en deelbaar."),
    ("frame", "Open Frame Studio", "desktop", "Constructief", "frame.calculation", None, "AC", "Alpha", "0.6", 122, None, "Parametrisch kozijn- en raamwerkontwerp voor de bouw."),
    ("geotech", "Open Geotechniek Studio", "desktop", "Geotechniek", "geo.sondering", "open-geotechniek-studio", "EI", "Beta", "0.4", 218, "0.4", "Viewer voor sonderingen: CPT's in GEF- en BRO-XML-formaat."),
    ("monty", "Monty IFC Viewer", "desktop", "BIM", "ifc.validate", "monty-ifc-viewer", "C", "Beta", "1.0", 50, None, "Open source IFC-viewer voor BIM-modellen, ook op de bouwplaats."),
    ("speech", "Open Speech Studio", "desktop", "AI", "audio.speech", "open-speech-studio", "AECI", "Beta", "0.12", 93, "0.12", "Lokale spraak-naar-tekst en vergadernotities, 100% op je eigen machine."),
    ("field", "Open Field Studio", "desktop", "Veld", "field.list", "open-field-studio", "C", "Beta", "0.3", 35, None, "Inspecties, opleveringen en kwaliteitsborging met checklists."),
    ("pointcloud", "Open Pointcloud Studio", "desktop", "BIM", "ifc.validate", "open-pointcloud-studio", "ECI", "Beta", "0.9", 432, "0.9", "Pointcloud-viewer voor renovatie en analyse."),
    ("stl", "Open STL-3DMap Studio", "desktop", "GIS", "geo.coordinate-tag", None, "I", "", "0.2", 0, None, "3D-printbare meerkleuren stadskaarten van Nederland op basis van 3DBAG en BGT."),
    ("energy", "Open Energy Studio", "web", "Energie", "energy.fetch-label", "open-energy-studio", "E", "Beta", "", 0, None, "Energieprestatie volgens NTA 8800: BENG, energielabel en TOjuli."),
    ("heatloss", "Open Heatloss Studio", "web", "Energie", "energy.fetch-label", "open-heatloss-studio", "E", "Beta", "", 693, None, "Warmteverliesberekeningen volgens NEN-EN 12831 / ISSO 51."),
    ("books", "Open Books Studio", "web", "Documenten", "report.document", "open-books", "A", "In ontwikkeling", "", 113, None, "Digitalisering van historische bouwliteratuur."),
    ("validator", "Open BIM Validator Studio", "web", "BIM", "ifc.validate", "open-bim-validator", "", "", "", 75, None, "Valideer IFC-modellen tegen IDS, NL-BIM Basis ILS en de RVB BIM Norm."),
    ("pile", "Pile Plan Studio", "web", "Constructief", "frame.calculation", None, "EI", "Beta", "", 406, None, "Funderingspalenplannen opstellen en beheren, met technische uitvoer."),
]


# GitHub repository and web address per tool, from the installer catalogue (catalog.ts at 8b39bae).
REPOS = {
    "calc": "OpenAEC-Foundation/open-calc-studio", "pdf": "OpenAEC-Foundation/open-pdf-studio",
    "planner": "OpenAEC-Foundation/open-planner-studio", "2d": "OpenAEC-Foundation/open-2d-studio",
    "cad": "HakanSeven12/OpenCADStudio", "calculations": "OpenAEC-Foundation/Open-Calculations-Studio",
    "frame": "OpenAEC-Foundation/open-frame-studio", "geotech": "OpenAEC-Foundation/open-geotechniek-studio",
    "monty": "OpenAEC-Foundation/monty-ifc-viewer", "speech": "OpenAEC-Foundation/open-speech-studio",
    "field": "OpenAEC-Foundation/Open-Field-Studio", "pointcloud": "OpenAEC-Foundation/open-pointcloud-studio",
    "stl": "OpenAEC-Foundation/Open-STL-3DMap-Studio", "validator": "OpenAEC-Foundation/OpenAEC-BIM-validator",
    "pile": "OpenAEC-Foundation/pile-plan-studio",
}
WEB = {"calc", "pdf", "planner", "2d", "cad", "calculations", "geotech", "monty", "field", "pointcloud",
       "energy", "heatloss", "books", "validator", "pile"}
# The installer's own tool logos (public/logos); the other tools show their category icon.
LOGOS = {"energy": "../../harmonization/references/openaec-installer/public/logos/open-energy-studio.png"}
# GitHub mark as used by the real installer for its GitHub button (Octicons, MIT).
GITHUB = ('<symbol id="gh" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
          '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 '
          '2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 '
          '2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 '
          '1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></symbol>')


def symbol(master, name):
    svg = (ICONS / master / f"{name}.svg").read_text(encoding="utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    inner = inner.replace("var(--icon-accent,currentColor)", "var(--icon-accent, currentColor)")
    return f'<symbol id="i{master}-{name}" viewBox="0 0 {master} {master}">{inner}</symbol>'


def main():
    sprite = "".join(symbol(m, n) for m, names in ICON_NAMES.items() for n in names) + GITHUB
    tools = [
        dict(id=t[0], name=t[1], kind=t[2], cat=t[3], icon=t[4], preview=(PREVIEWS + t[5] + ".jpg") if t[5] else None,
             disc=t[6], site=t[7], latest=t[8], commits=t[9], installed=t[10], desc=t[11],
             repo=REPOS.get(t[0]), web=t[0] in WEB, logo=LOGOS.get(t[0]))
        for t in TOOLS
    ]
    page = TEMPLATE.replace("/*SPRITE*/", sprite).replace("/*TOOLS*/", json.dumps(tools, ensure_ascii=False))
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT).as_posix()}: 5 proposals, {len(tools)} tools, {sprite.count('<symbol')} icons")


TEMPLATE = r"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC Installer · voorstellen</title>
<style>
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf');font-weight:400}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Medium.ttf');font-weight:500}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-SemiBold.ttf');font-weight:600 800}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Medium.ttf');font-weight:500}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}
@font-face{font-family:'JetBrains Mono';src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
:root{
  --page:#F1EEEA;--ink:#2A2A32;--text:#36363E;--muted:#5F5F65;--faint:#8A8A90;
  --card1:#FFFFFF;--card2:#FAFAF9;--line:rgba(42,42,50,.10);--line2:rgba(42,42,50,.16);--chip:#F5F5F4;
  --night:#2A2A32;--forge:#33333C;--onnight:#EDEBE8;--onnight2:#B9B7B2;
  --amber:#D97706;--amber-hi:#E08A12;--amber-text:#B45309;--amber-tint:rgba(217,119,6,.15);--on-amber:#1C1917;
  --ok:#166534;--ok-tint:#E8F0EB;--up:#B45309;--up-tint:#FBF1E6;
  --shadow:0 1px 2px rgba(42,42,50,.06),0 12px 28px -14px rgba(42,42,50,.22);
  --panel-shadow:0 40px 80px -30px rgba(42,42,50,.55);
  --win:#FFFFFF;--title:#F1EEEA;--hover:#F2F2F3;
}
body.dark{
  --page:#26262D;--ink:#EDEBE8;--text:#EDEBE8;--muted:#B9B7B2;--faint:#8F8D89;
  --card1:#363640;--card2:#2F2F38;--line:rgba(255,255,255,.08);--line2:rgba(255,255,255,.14);--chip:rgba(255,255,255,.06);
  --amber-text:#FBBF24;--ok:#4ADE80;--ok-tint:rgba(74,222,128,.12);--up:#FBBF24;--up-tint:rgba(251,191,36,.12);
  --shadow:0 1px 2px rgba(0,0,0,.3),0 14px 30px -14px rgba(0,0,0,.6);--panel-shadow:0 40px 80px -30px rgba(0,0,0,.7);
  --win:#2A2A32;--title:#2A2A32;--hover:rgba(255,255,255,.06);
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:#DCD7D0;color:var(--text);font:14px/1.5 Inter,system-ui,sans-serif;transition:background .2s}
body.dark{background:#1A1A20}
svg.i{width:16px;height:16px;flex:none;--icon-accent:var(--amber)}
.mono{font-family:'JetBrains Mono',monospace}
.sg{font-family:'Space Grotesk',Inter,sans-serif;font-weight:700;letter-spacing:-.02em}

/* Page chrome around the proposals (not part of the design) */
.top{max-width:1320px;margin:0 auto;padding:22px 20px 10px;display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap}
.top h1{font:700 26px/1.2 'Space Grotesk';margin:0;color:#2A2A32;letter-spacing:-.02em}
body.dark .top h1{color:#EDEBE8}
.top p{margin:4px 0 0;color:#5F5F65;max-width:640px}body.dark .top p{color:#B9B7B2}
.switch{display:flex;gap:8px;flex-wrap:wrap;margin-left:auto}
.switch button{font:600 14px Inter;border-radius:9999px;padding:9px 16px;border:1px solid rgba(42,42,50,.12);background:#fff;color:#36363E;cursor:pointer;box-shadow:0 1px 2px rgba(42,42,50,.06)}
.switch button.on{background:linear-gradient(#E08A12,#D97706);color:#1C1917;border-color:#D97706;box-shadow:0 10px 24px -8px rgba(217,119,6,.65)}
.note{max-width:1320px;margin:0 auto;padding:0 20px 14px;color:#5F5F65;font-size:13px}body.dark .note{color:#B9B7B2}
.note b{color:#2A2A32}body.dark .note b{color:#EDEBE8}

/* The window */
.win{width:1280px;height:800px;margin:0 auto 40px;border-radius:10px;overflow:hidden;background:var(--page);box-shadow:0 30px 70px -20px rgba(0,0,0,.45),0 0 0 1px rgba(0,0,0,.08);display:flex;flex-direction:column}
.titlebar{height:32px;flex:none;display:flex;align-items:center;background:var(--title);border-bottom:1px solid var(--line);font:500 12px Inter;color:var(--text)}
.titlebar .name{flex:1;text-align:center}
.titlebar .wb{width:40px;height:32px;display:grid;place-items:center;color:var(--text)}
.titlebar .wb:hover{background:var(--hover)}.titlebar .wb.x:hover{background:#B91C1C;color:#fff}
.app{flex:1;min-height:0;display:flex}
.scroll{flex:1;overflow:auto}
.status{height:22px;flex:none;display:flex;align-items:center;gap:16px;padding:0 10px;font:11px Inter;color:var(--muted);background:var(--title);border-top:1px solid var(--line)}
.status .r{margin-left:auto;font-family:'JetBrains Mono'}

/* Website parts */
.btn{display:inline-flex;align-items:center;gap:8px;font:600 14px Inter;border-radius:8px;padding:10px 20px;border:0;cursor:pointer;white-space:nowrap;text-decoration:none}
.btn.sm{padding:7px 14px;font-size:13px}
.btn.primary{background:linear-gradient(#E08A12,#D97706);color:var(--on-amber);box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 10px 24px -8px rgba(217,119,6,.65)}
.btn.primary:hover{background:linear-gradient(#EA9A26,#E08A12)}
.btn.primary .i{--icon-accent:var(--on-amber)}
.btn.light{background:linear-gradient(var(--card1),var(--card2));color:var(--text);border:1px solid var(--line2);box-shadow:0 1px 2px rgba(42,42,50,.06)}
.btn.light:hover{border-color:var(--amber)}
.btn.glass{background:rgba(255,255,255,.06);color:#fff;border:1px solid rgba(255,255,255,.14);box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.btn.glass:hover{border-color:var(--amber)}
.ibtn{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--line2);background:var(--card1);color:var(--text);cursor:pointer;flex:none}
.ibtn:hover{border-color:var(--amber);color:var(--amber-text)}
.on-dark .ibtn{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14);color:#EDEBE8}
.label{align-self:flex-start;display:inline-flex;align-items:center;gap:8px;font:500 12px 'JetBrains Mono';letter-spacing:.1em;text-transform:uppercase;padding:7px 14px;border-radius:9999px;background:var(--amber-tint);color:var(--amber-text)}
.label:before{content:"";width:6px;height:6px;border-radius:3px;background:var(--amber)}
.on-dark .label{color:#F59E0B}
.chips{display:flex;gap:4px;flex-wrap:wrap}
.chip{font:600 10px 'JetBrains Mono';letter-spacing:.04em;padding:1px 7px;border-radius:4px;background:var(--chip);border:1px solid var(--line);color:var(--text)}
.on-dark .chip{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.1);color:#EDEBE8}
.pill{flex:none;font:500 10px 'JetBrains Mono';letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:9999px;border:1px solid var(--line2);color:var(--muted);white-space:nowrap}
.pill.beta,.pill.update{border-color:rgba(217,119,6,.45);background:var(--up-tint);color:var(--up)}
.pill.ok{border-color:rgba(22,101,52,.35);background:var(--ok-tint);color:var(--ok)}
.pill.web{border-color:rgba(29,78,216,.3);background:rgba(29,78,216,.08);color:#1D4ED8}
body.dark .pill.web,.on-dark .pill.web{color:#93C5FD;border-color:rgba(147,197,253,.35);background:rgba(147,197,253,.1)}
.on-dark .pill{color:#B9B7B2;border-color:rgba(255,255,255,.16)}
.on-dark .pill.ok{color:#4ADE80;border-color:rgba(74,222,128,.35);background:rgba(74,222,128,.1)}
.on-dark .pill.beta,.on-dark .pill.update{color:#FBBF24;border-color:rgba(251,191,36,.4);background:rgba(251,191,36,.1)}
.card{background:linear-gradient(var(--card1),var(--card2));border:1px solid var(--line);border-radius:12px;box-shadow:inset 0 1px 0 rgba(255,255,255,.6),var(--shadow)}
.card.feat{border:2px solid var(--amber)}
.glass{background:linear-gradient(rgba(255,255,255,.07),rgba(255,255,255,.024));border:1px solid rgba(255,255,255,.08);border-radius:12px;box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 20px 40px -20px rgba(0,0,0,.6);color:#EDEBE8}
.glass.feat{border:2px solid var(--amber)}
.dark-panel{background:linear-gradient(#33333C 0%,#2A2A32 70%);border-radius:16px;box-shadow:var(--panel-shadow),0 0 0 1px rgba(42,42,50,.04);color:#EDEBE8}
.tile.logo{background:linear-gradient(145deg,rgba(217,119,6,.12),rgba(217,119,6,.03))}
.ibtn.gh{color:var(--ink)}.on-dark .ibtn.gh{color:#EDEBE8}
.tile{display:grid;place-items:center;border-radius:12px;background:linear-gradient(145deg,rgba(217,119,6,.2),rgba(217,119,6,.05));border:1px solid rgba(217,119,6,.22);color:var(--amber-text);flex:none}
.on-dark .tile{color:#F59E0B}
.thumb{display:block;width:100%;border-radius:8px;background:var(--chip);object-fit:cover;object-position:top}
.thumb.empty{display:grid;place-items:center;background:linear-gradient(145deg,rgba(217,119,6,.14),rgba(217,119,6,.03))}
.muted{color:var(--muted)}.on-dark .muted{color:#B9B7B2}
.ver{font:12px 'JetBrains Mono';color:var(--muted);display:flex;gap:6px;align-items:center}
.ver .new{font:inherit;color:var(--amber-text)}.on-dark .ver{color:#B9B7B2}.on-dark .ver .new{color:#FBBF24}
.link{font:600 13px Inter;color:var(--amber-text);text-decoration:none;cursor:pointer}.link:hover{text-decoration:underline}
.on-dark .link{color:#F59E0B}
.fpill{display:inline-flex;align-items:center;gap:8px;font:600 14px Inter;border-radius:9999px;padding:8px 15px;border:1px solid var(--line2);background:linear-gradient(var(--card1),var(--card2));color:var(--text);cursor:pointer;box-shadow:0 1px 2px rgba(42,42,50,.06)}
.fpill .n{font:500 11px 'JetBrains Mono';padding:1px 7px;border-radius:9999px;background:var(--line)}
.fpill .d{font:600 10px 'JetBrains Mono';padding:0 5px;border-radius:4px;background:var(--chip);border:1px solid var(--line)}
.fpill.on{background:linear-gradient(#E08A12,#D97706);border-color:#D97706;color:var(--on-amber);box-shadow:0 10px 24px -8px rgba(217,119,6,.65)}
.fpill.on .n{background:rgba(28,25,23,.12)}.fpill.on .d{background:rgba(28,25,23,.1);border-color:transparent}
.search{display:flex;align-items:center;gap:8px;border:1px solid var(--line2);background:var(--card1);border-radius:9999px;padding:8px 14px;color:var(--muted);min-width:220px}
.search input{border:0;background:transparent;font:14px Inter;color:var(--text);outline:none;width:100%}
.progress{height:6px;border-radius:3px;background:var(--line);overflow:hidden}.progress i{display:block;height:100%;background:linear-gradient(90deg,#E08A12,#D97706);border-radius:3px}
.h2{font:700 26px/1.2 'Space Grotesk';letter-spacing:-.02em;margin:10px 0 6px;color:var(--ink)}
.on-dark .h2{color:#EDEBE8}
.acc{color:var(--amber-text)}.on-dark .acc,.hero .acc{color:#F59E0B}

/* A · Etalage */
.A .hero{position:relative;padding:54px 48px 46px;text-align:center;background:radial-gradient(60% 90% at 50% -10%,rgba(255,255,255,.07),rgba(0,0,0,0) 65%),linear-gradient(#33333C,#2A2A32);color:#EDEBE8;border-bottom:3px solid var(--amber)}
.A .hero h2{font:700 44px/1.1 'Space Grotesk';letter-spacing:-.025em;margin:16px 0 10px}
.A .hero p{color:#B9B7B2;font-size:17px;max-width:620px;margin:0 auto}
.A .hero .cta{display:flex;gap:12px;justify-content:center;margin-top:26px}
.A .stats{display:flex;justify-content:center;gap:26px;margin-top:22px;font:12px 'JetBrains Mono';color:#B9B7B2;letter-spacing:.06em;text-transform:uppercase}
.A .stats b{color:#EDEBE8;font-weight:400}
.A .body{padding:32px 40px 48px;display:flex;flex-direction:column;gap:30px}
.A .bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.A .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.A .tc{padding:18px;display:flex;flex-direction:column;gap:12px}
.A .tc .thumb{height:150px}
.A .tc h3{font:700 18px/1.2 'Space Grotesk';letter-spacing:-.02em;margin:0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.A .tc p{margin:0;color:var(--muted);font-size:14px;min-height:42px}
.A .tc .foot{display:flex;align-items:center;gap:8px;margin-top:auto}
.A .tc .foot .sp{flex:1}
.A .webp{padding:40px 32px;margin:0}
.A .webp .grid .tc p{color:#B9B7B2}

/* B · Bibliotheek */
.B .side{width:248px;flex:none;background:linear-gradient(#33333C,#2A2A32 70%);color:#EDEBE8;display:flex;flex-direction:column;padding:20px 14px;gap:4px}
.B .brand{font:700 20px 'Space Grotesk';letter-spacing:-.02em;padding:4px 10px 16px}.B .brand span{color:#F59E0B}
.B .nav{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:8px;color:#D4D1CC;cursor:pointer;font-weight:500}
.B .nav:hover{background:rgba(255,255,255,.05)}
.B .nav.on{background:linear-gradient(rgba(255,255,255,.09),rgba(255,255,255,.03));color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.08)}
.B .nav .n{margin-left:auto;font:11px 'JetBrains Mono';color:#B9B7B2}.B .nav .n.up{color:#1C1917;background:linear-gradient(#E08A12,#D97706);border-radius:9999px;padding:0 7px}
.B .grp{font:500 11px 'JetBrains Mono';letter-spacing:.1em;color:#8F8D89;padding:16px 10px 6px;text-transform:uppercase}
.B .self{margin-top:auto;padding:14px}
.B .main{flex:1;display:flex;min-width:0}
.B .list{flex:1;overflow:auto;padding:26px 28px}
.B .head{display:flex;align-items:flex-end;gap:12px;margin-bottom:18px}
.B .gh{font:500 11px 'JetBrains Mono';letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:22px 0 10px;display:flex;align-items:center;gap:10px}
.B .gh:after{content:"";flex:1;height:1px;background:var(--line)}
.B .row{display:flex;align-items:center;gap:14px;padding:10px 12px;margin-bottom:8px;cursor:pointer}
.B .row .thumb{width:112px;height:64px;border-radius:6px}
.B .row .t{flex:1;min-width:0}.B .row .t b{font:700 16px 'Space Grotesk';letter-spacing:-.01em;color:var(--ink);white-space:nowrap}
.B .row .t .desc{color:var(--muted);font-size:13px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.B .row.sel{border:2px solid var(--amber);padding:9px 11px}
.B .detail{width:380px;flex:none;border-left:1px solid var(--line);background:linear-gradient(var(--card1),var(--card2));overflow:auto;padding:24px;display:flex;flex-direction:column;gap:14px}
.B .detail .thumb{height:190px;box-shadow:var(--shadow)}
.B .detail h3{font:700 24px/1.15 'Space Grotesk';letter-spacing:-.02em;margin:0;color:var(--ink)}
.B .facts{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.B .fact{padding:12px 14px}.B .fact b{display:block;font:700 20px 'Space Grotesk';color:var(--ink)}.B .fact span{font:11px 'JetBrains Mono';letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}

/* C · Startpunt */
.C .top2{padding:30px 40px 26px;background:radial-gradient(70% 120% at 15% -20%,rgba(217,119,6,.18),rgba(0,0,0,0) 60%),linear-gradient(#33333C,#2A2A32);color:#EDEBE8;display:flex;align-items:center;gap:20px}
.C .top2 h2{font:700 30px/1.15 'Space Grotesk';letter-spacing:-.02em;margin:6px 0 0}
.C .top2 .search{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14);color:#B9B7B2;margin-left:auto;min-width:300px}
.C .top2 .search input{color:#fff}
.C .body{padding:28px 40px 44px;display:flex;flex-direction:column;gap:30px}
.C .apps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.C .app2{padding:20px;display:flex;flex-direction:column;gap:14px;position:relative}
.C .app2 .tile{width:56px;height:56px;border-radius:14px}
.C .app2 .nm{display:block;font:700 17px/1.2 'Space Grotesk';letter-spacing:-.02em;color:var(--ink)}
.C .app2 .row2{display:flex;align-items:center;gap:8px}
.C .app2 .row2 .sp{flex:1}
.C .ups{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.C .up{display:flex;gap:16px;align-items:center;padding:16px 18px}
.C .up .thumb{width:150px;height:84px}
.C .disc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.C .dc{overflow:hidden;display:flex;flex-direction:column}
.C .dc .thumb{height:118px;border-radius:12px 12px 0 0}
.C .dc .in{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.C .dc .nm{font:700 15px 'Space Grotesk';color:var(--ink)}
.C .web{padding:26px 28px;display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center}
.C .webs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.C .wt{padding:14px;display:flex;flex-direction:column;gap:10px;cursor:pointer}
.C .wt:hover{border-color:var(--amber)}

/* E · Mix: dark top (A hero + D feature), everything below follows the theme */
.E .top3{display:grid;grid-template-columns:minmax(0,1fr) 560px;gap:40px;align-items:center;padding:40px 44px 40px 48px;background:radial-gradient(60% 90% at 30% -10%,rgba(255,255,255,.07),rgba(0,0,0,0) 65%),linear-gradient(#33333C,#2A2A32);color:#EDEBE8;border-bottom:3px solid var(--amber)}
.E .top3 h2{font:700 40px/1.08 'Space Grotesk';letter-spacing:-.025em;margin:14px 0 10px}
.E .top3 p{color:#B9B7B2;font-size:16px;margin:0;max-width:440px}
.E .cta{display:flex;gap:12px;margin-top:22px}
.E .stats{display:flex;gap:22px;margin-top:20px;font:12px 'JetBrains Mono';color:#B9B7B2;letter-spacing:.06em;text-transform:uppercase}.E .stats b{color:#EDEBE8;font-weight:400}
.E .spot{padding:16px;display:flex;flex-direction:column;gap:12px}
.E .spot .shot{position:relative;border-radius:8px;overflow:hidden}
.E .spot .shot img{display:block;width:100%;height:220px;object-fit:cover;object-position:top left}
.E .spot .shot:after{content:"";position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(rgba(42,42,50,0),rgba(42,42,50,.85))}
.E .spot .shot .tag{position:absolute;left:12px;bottom:10px;z-index:1;background:rgba(42,42,50,.88);color:#F59E0B}
.E .spot .row3{display:flex;align-items:center;gap:12px}
.E .spot .nm{display:block;font:700 18px 'Space Grotesk';letter-spacing:-.02em}
.E .dots{display:flex;gap:6px}.E .dots i{width:22px;height:4px;border-radius:2px;background:rgba(255,255,255,.18);cursor:pointer}.E .dots i.on{background:var(--amber)}
.E .body{padding:28px 40px 48px;display:flex;flex-direction:column;gap:34px}
.E .tools{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.E .sect{display:flex;align-items:flex-end;gap:14px;margin-bottom:16px}
.E .sect .sp{flex:1}.E .sect .ico{margin-bottom:4px}
.E .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.E .tc{padding:18px;display:flex;flex-direction:column;gap:12px}
.E .tc .thumb{height:150px}
.E .tc .head{display:flex;gap:12px;align-items:center}
.E .tc .head .t{min-width:0;display:flex;flex-direction:column;gap:5px}
.E .tc h3{font:700 16px/1.2 'Space Grotesk';letter-spacing:-.01em;margin:0;color:var(--ink)}
.E .tc p{margin:0;color:var(--muted);font-size:13px;min-height:58px}
.E .tc .meta{font:11px 'JetBrains Mono';color:var(--faint);display:flex;gap:10px;align-items:center}
.E .tc .foot{display:flex;align-items:center;gap:6px;margin-top:auto;flex-wrap:nowrap}.E .tc .foot .sp{flex:1}
.E .tc .ibtn{width:32px;height:32px}
.E .divider{display:flex;align-items:center;gap:14px;font:500 11px 'JetBrains Mono';letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.E .divider:before,.E .divider:after{content:"";flex:1;height:1px;background:var(--line2)}
/* D · Uitgelicht */
.D .feature{margin:26px 32px 0;padding:0;overflow:hidden;display:grid;grid-template-columns:420px 1fr;min-height:330px}
.D .feature .txt{padding:38px 36px;display:flex;flex-direction:column;gap:14px;justify-content:center}
.D .feature h2{font:700 38px/1.1 'Space Grotesk';letter-spacing:-.025em;margin:0}
.D .feature p{color:#B9B7B2;margin:0;font-size:15px}
.D .feature .shot{position:relative;padding:34px 34px 0 0}
.D .feature .shot img{width:100%;height:100%;object-fit:cover;object-position:top left;border-radius:10px 10px 0 0;box-shadow:0 30px 60px -20px rgba(0,0,0,.7);display:block}
.D .feature .shot:after{content:"";position:absolute;left:0;right:0;bottom:0;height:90px;background:linear-gradient(rgba(42,42,50,0),#2A2A32)}
.D .dots{display:flex;gap:6px;margin-top:6px}.D .dots i{width:22px;height:4px;border-radius:2px;background:rgba(255,255,255,.18);cursor:pointer}.D .dots i.on{background:var(--amber)}
.D .body{padding:26px 32px 44px;display:flex;flex-direction:column;gap:22px}
.D .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.D .tc{padding:16px;display:flex;flex-direction:column;gap:10px}
.D .tc .thumb{height:120px}
.D .tc h3{font:700 16px/1.2 'Space Grotesk';letter-spacing:-.01em;margin:0;color:var(--ink)}
.D .tc p{margin:0;color:var(--muted);font-size:13px;min-height:58px}
.D .tc .meta{font:11px 'JetBrains Mono';color:var(--faint);display:flex;gap:10px}
.D .tc .foot{display:flex;align-items:center;gap:8px;margin-top:auto}.D .tc .foot .sp{flex:1}
.D .sect{display:flex;align-items:flex-end;gap:14px}
.D .sect .sp{flex:1}
</style>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">/*SPRITE*/</svg>
<div class="top">
  <div><h1>OpenAEC Installer · voorstellen</h1>
  <p>Vanaf nul ontworpen met de kleuren, rondingen, knoppen, verlopen en schaduwen van open-aec.com. Klik gerust overal op: filteren, selecteren, installeren en bijwerken werken.</p></div>
  <div class="switch" id="variants"></div>
  <div class="switch"><button id="themeL" class="on">Licht</button><button id="themeD">Donker</button></div>
</div>
<div class="note" id="note"></div>
<div class="win">
  <div class="titlebar"><div style="width:120px"></div><div class="name" id="wtitle">OpenAEC Installer</div>
    <div class="wb"><svg class="i"><use href="#i16-window.minimize"/></svg></div><div class="wb"><svg class="i"><use href="#i16-window.maximize"/></svg></div><div class="wb x"><svg class="i"><use href="#i16-window.close"/></svg></div></div>
  <div class="app" id="app"></div>
  <div class="status" id="status"></div>
</div>
<script>
const TOOLS=/*TOOLS*/;
const S={v:'E',filter:'all',disc:'',q:'',sel:'pdf',feat:0,progress:{}};
const ic=(n,s=16,m='16')=>`<svg class="i" style="width:${s}px;height:${s}px"><use href="#i${m}-${n}"/></svg>`;
const big=(n,s=24)=>ic(n,s,'24');
const isUpd=t=>t.kind==='desktop'&&t.installed&&t.installed!==t.latest;
const inst=t=>t.kind==='desktop'&&!!t.installed;
const DISC={A:'Architecture',E:'Engineering',C:'Construction',I:'Infra & GWW'};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function chips(t){return `<div class="chips">${[...t.disc].map(d=>`<span class="chip">${d}</span>`).join('')}</div>`}
function pills(t){let p='';if(S.progress[t.id]!==undefined)p+=`<span class="pill web">Bezig</span>`;else if(isUpd(t))p+=`<span class="pill update">Update</span>`;else if(inst(t))p+=`<span class="pill ok">Geïnstalleerd</span>`;
  if(t.kind==='web')p+=`<span class="pill web">Web</span>`;if(t.site)p+=`<span class="pill ${t.site==='Beta'?'beta':''}">${esc(t.site)}</span>`;return p}
function statusPill(t){if(S.progress[t.id]!==undefined)return `<span class="pill web">Bezig</span>`;if(isUpd(t))return `<span class="pill update">Update</span>`;if(t.kind==='web')return `<span class="pill web">Web</span>`;return inst(t)?`<span class="pill ok">Geïnstalleerd</span>`:''}
function thumb(t,h){return t.preview?`<img class="thumb" src="${t.preview}" alt="" style="height:${h}px">`:`<div class="thumb empty" style="height:${h}px"><div class="tile" style="width:64px;height:64px">${big(t.icon,34)}</div></div>`}
function ver(t){if(t.kind==='web')return `<div class="ver">${ic('link.open-external',12)} webtool</div>`;
  if(isUpd(t))return `<div class="ver">${ic('status.success',12)} v${t.installed} → <span class="new">v${t.latest}</span></div>`;
  if(inst(t))return `<div class="ver">${ic('status.success',12)} v${t.installed}</div>`;return `<div class="ver">v${t.latest} beschikbaar</div>`}
function action(t,size=''){const p=S.progress[t.id];if(p!==undefined)return `<div style="flex:1;max-width:190px"><div class="progress"><i style="width:${p}%"></i></div><div class="ver" style="margin-top:5px">Downloaden… ${p}%</div></div>`;
  if(t.kind==='web')return `<button class="btn primary ${size}" data-act="open" data-id="${t.id}">${ic('software.open-webtab')}Openen</button>`;
  if(isUpd(t))return `<button class="btn primary ${size}" data-act="install" data-id="${t.id}">${ic('software.update')}Bijwerken</button>`;
  if(inst(t))return `<button class="btn primary ${size}" data-act="launch" data-id="${t.id}">${ic('software.launch')}Starten</button>`;
  return `<button class="btn primary ${size}" data-act="install" data-id="${t.id}">${ic('software.install')}Installeren</button>`}
function icons(t){let s='';if(isUpd(t)&&S.progress[t.id]===undefined)s+=`<span class="ibtn" title="Huidige versie starten" data-act="launch" data-id="${t.id}">${ic('software.launch')}</span>`;
  if(t.repo)s+=`<span class="ibtn gh" title="Broncode op GitHub · ${esc(t.repo)}"><svg class="i"><use href="#gh"/></svg></span>`;
  if(t.kind==='desktop'&&t.web)s+=`<span class="ibtn" title="Webversie hier openen">${ic('software.open-webtab')}</span>`;
  if(t.web)s+=`<span class="ibtn" title="Openen in browser">${ic('link.open-external')}</span>`;return s}
function logo(t,size){return t.logo?`<span class="tile logo" style="width:${size}px;height:${size}px"><img src="${t.logo}" alt="" style="width:${Math.round(size*.72)}px;height:${Math.round(size*.72)}px"></span>`:`<span class="tile" style="width:${size}px;height:${size}px">${big(t.icon,Math.round(size*.55))}</span>`}
function visible(t){if(S.filter==='inst'&&!inst(t))return false;if(S.filter==='upd'&&!isUpd(t))return false;if(S.disc&&!t.disc.includes(S.disc))return false;
  const q=S.q.trim().toLowerCase();return !q||(t.name+' '+t.desc+' '+t.cat).toLowerCase().includes(q)}
const count=f=>TOOLS.filter(t=>f==='all'||(f==='inst'&&inst(t))||(f==='upd'&&isUpd(t))||(f==='web'&&t.kind==='web')).length;
const upd=()=>TOOLS.filter(isUpd).length;

const VARIANTS={
A:{name:'A · Etalage',note:'<b>Etalage</b>: de installer als de website zelf. Een donkere kop met amber lijn, de filters van het ecosysteem (A/E/C/I) en de websitetegels; webtools in een donker paneel. Goed om te ontdekken; voor dagelijks starten iets lang.',render(){
  const d=TOOLS.filter(t=>t.kind==='desktop'&&visible(t)),w=TOOLS.filter(t=>t.kind==='web'&&visible(t));
  const card=(t,glass)=>`<div class="${glass?'glass':'card'} tc ${isUpd(t)?'feat':''}">${thumb(t,150)}${chips(t)}<h3>${esc(t.name)} ${pills(t)}</h3><p>${esc(t.desc)}</p>${ver(t)}<div class="foot">${action(t)}<span class="sp"></span>${icons(t)}</div></div>`;
  return `<div class="scroll A"><div class="hero on-dark"><span class="label">OpenAEC Installer</span><h2>Alle bouwsoftware,<br><span class="acc">één plek.</span></h2><p>Ontdek, installeer, werk bij en start de open source tools van de OpenAEC Foundation.</p>
  <div class="cta"><button class="btn primary" data-act="all">${ic('software.update')}Alles bijwerken (${upd()})</button><button class="btn glass">${ic('ui.check-updates')}Controleren op updates</button></div>
  <div class="stats"><span><b>${TOOLS.length}</b> tools</span><span><b>${count('inst')}</b> geïnstalleerd</span><span><b>${upd()}</b> updates</span><span><b>${count('web')}</b> webtools</span></div></div>
  <div class="body"><div class="bar">${discPills()}</div>
  <div><div style="display:flex;align-items:flex-end;gap:12px"><div><span class="label">Desktop-apps · ${d.length}</span><div class="h2">Installeren en starten op je computer</div></div><span style="flex:1"></span><div style="margin-bottom:6px">${searchBox()}</div></div><div class="grid" style="margin-top:18px">${d.map(t=>card(t,false)).join('')||'<p class=muted>Geen desktop-apps voor dit filter.</p>'}</div></div>
  <div class="dark-panel webp on-dark"><span class="label">Webtools · ${w.length}</span><div class="h2">Direct in je browser</div><p class="muted" style="margin:0 0 18px">Geen installatie nodig. Ze openen in de installer of in je browser.</p><div class="grid">${w.map(t=>card(t,true)).join('')||'<p class=muted>Geen webtools voor dit filter.</p>'}</div></div></div></div>`}},
B:{name:'B · Bibliotheek',note:'<b>Bibliotheek</b>: een rustige beheerlijst, zoals een app-bibliotheek. Donkere zijbalk met tellers, rijen met kleine screenshot en status, en rechts alle details van de gekozen tool. Snel voor dagelijks gebruik en bijwerken.',render(){
  const groups=[['Updates beschikbaar',TOOLS.filter(t=>isUpd(t)&&visible(t))],['Geïnstalleerd',TOOLS.filter(t=>inst(t)&&!isUpd(t)&&visible(t))],['Niet geïnstalleerd',TOOLS.filter(t=>t.kind==='desktop'&&!inst(t)&&visible(t))],['Webtools',TOOLS.filter(t=>t.kind==='web'&&visible(t))]];
  const sel=TOOLS.find(t=>t.id===S.sel)||TOOLS[0];
  const nav=(f,label,icon,n,up)=>`<div class="nav ${S.filter===f&&!S.disc?'on':''}" data-filter="${f}">${ic(icon)}${label}<span class="n ${up?'up':''}">${n}</span></div>`;
  return `<div class="B" style="display:flex;flex:1;min-width:0"><div class="side on-dark"><div class="brand">Open<span>AEC</span> <span style="color:#B9B7B2;font-weight:500">Installer</span></div>
  ${nav('all','Alle tools','nav.home',TOOLS.length)}${nav('inst','Geïnstalleerd','status.success',count('inst'))}${nav('upd','Updates','software.update',upd(),true)}
  <div class="grp">Disciplines</div>${'AECI'.split('').map(d=>`<div class="nav ${S.disc===d?'on':''}" data-disc="${d}"><span class="chip">${d}</span>${DISC[d]}<span class="n">${TOOLS.filter(t=>t.disc.includes(d)).length}</span></div>`).join('')}
  <div class="self glass"><div style="font:600 13px Inter">Installer 1.6.0 is uit</div><div class="muted" style="font-size:12px;margin:2px 0 10px">Je hebt 1.5.0.</div><button class="btn primary sm">${ic('software.update')}Bijwerken</button></div></div>
  <div class="main"><div class="list"><div class="head"><div><span class="label">Bibliotheek</span><div class="h2" style="margin-bottom:0">${S.disc?DISC[S.disc]:({all:'Alle tools',inst:'Geïnstalleerd',upd:'Updates'}[S.filter])}</div></div><span style="flex:1"></span>${searchBox()}<button class="btn light" >${ic('ui.check-updates')}Controleren</button></div>
  ${groups.filter(g=>g[1].length).map(([h,ts])=>`<div class="gh">${h} · ${ts.length}${h==='Updates beschikbaar'?` <button class="btn primary sm" data-act="all" style="margin-left:8px">Alles bijwerken</button>`:''}</div>`+ts.map(t=>`<div class="card row ${t.id===S.sel?'sel':''}" data-sel="${t.id}">${thumb(t,64)}<div class="t"><div style="display:flex;gap:8px;align-items:center"><b>${esc(t.name)}</b>${statusPill(t)}</div><span class="desc">${esc(t.desc)}</span>${ver(t)}</div>${action(t,'sm')}</div>`).join('')).join('')}</div>
  <div class="detail">${thumb(sel,190)}<div style="display:flex;gap:8px;align-items:center">${chips(sel)}${pills(sel)}</div><h3>${esc(sel.name)}</h3><p class="muted" style="margin:0">${esc(sel.desc)}</p>
  <div style="display:flex;gap:8px;align-items:center">${action(sel)}<span style="flex:1"></span>${icons(sel)}</div>
  <div class="facts"><div class="card fact"><b>${sel.kind==='web'?'Web':(sel.installed?'v'+sel.installed:'—')}</b><span>Geïnstalleerd</span></div><div class="card fact"><b>${sel.latest?'v'+sel.latest:'Live'}</b><span>Nieuwste</span></div><div class="card fact"><b>${sel.commits||'—'}</b><span>Commits</span></div><div class="card fact"><b>${esc(sel.cat)}</b><span>Categorie</span></div></div>
  <div style="display:flex;gap:16px"><a class="link">Productpagina →</a><a class="link">GitHub →</a><a class="link">Releases →</a></div></div></div></div>`}},
C:{name:'C · Startpunt',note:'<b>Startpunt</b>: eerst jouw eigen apps, groot en direct te starten, daarna updates en daarna ontdekken. Voelt als een launcher; de installer wordt de plek waar je je werkdag begint.',render(){
  const mine=TOOLS.filter(t=>inst(t)&&visible(t)),ups=TOOLS.filter(t=>isUpd(t)&&visible(t)),disc=TOOLS.filter(t=>t.kind==='desktop'&&!inst(t)&&visible(t)),web=TOOLS.filter(t=>t.kind==='web'&&visible(t));
  return `<div class="scroll C"><div class="top2 on-dark"><div><span class="label">Goedemiddag</span><h2>Waar werk je vandaag aan?</h2></div>${searchBox()}</div><div class="body">
  <div><div style="display:flex;align-items:flex-end;gap:12px"><div><span class="label">Mijn apps · ${mine.length}</span></div></div><div class="apps" style="margin-top:16px">${mine.map(t=>`<div class="card app2 ${isUpd(t)?'feat':''}"><div class="tile">${big(t.icon,30)}</div><div><span class="nm">${esc(t.name)}</span>${ver(t)}</div><div class="row2">${action(t,'sm')}<span class="sp"></span>${isUpd(t)?'<span class="pill update">Update</span>':''}</div></div>`).join('')}</div></div>
  ${ups.length?`<div><span class="label">Updates · ${ups.length}</span><div class="ups" style="margin-top:16px">${ups.map(t=>`<div class="card up feat">${thumb(t,84)}<div style="flex:1"><b class="sg" style="font-size:17px;color:var(--ink)">${esc(t.name)}</b>${ver(t)}<div class="muted" style="font-size:13px">Nieuwe versie met verbeteringen en reparaties.</div></div>${action(t,'sm')}</div>`).join('')}</div></div>`:''}
  <div><span class="label">Ontdekken · ${disc.length}</span><div class="h2">Meer tools van de Foundation</div><div class="disc" style="margin-top:14px">${disc.map(t=>`<div class="card dc">${thumb(t,118).replace('class="thumb','class="thumb')}<div class="in"><div style="display:flex;gap:6px;align-items:center">${chips(t)}${pills(t)}</div><span class="nm">${esc(t.name)}</span><div class="muted" style="font-size:13px;min-height:40px">${esc(t.desc)}</div><div style="display:flex;align-items:center;margin-top:auto">${action(t,'sm')}<span style="flex:1"></span><a class="link">Meer →</a></div></div></div>`).join('')}</div></div>
  <div class="dark-panel web on-dark"><div><span class="label">Webtools</span><div class="h2" style="max-width:220px">Direct in je browser</div><p class="muted" style="margin:0;max-width:220px">Geen installatie nodig.</p></div><div class="webs">${web.map(t=>`<div class="glass wt" data-act="open" data-id="${t.id}"><div class="tile" style="width:40px;height:40px">${big(t.icon,22)}</div><b style="font:700 14px 'Space Grotesk'">${esc(t.name.replace(' Studio',''))}</b><span class="link">Openen →</span></div>`).join('')}</div></div>
  </div></div>`}},
D:{name:'D · Uitgelicht',note:'<b>Uitgelicht</b>: een groot uitgelicht blok met screenshot dat wisselt (zoals een productpagina), daaronder de websitetegels in vier kolommen met disciplines, status, versie en commits. Het meest "marketing", het dichtst bij de site.',render(){
  const feats=TOOLS.filter(t=>t.preview&&(isUpd(t)||t.id==='calc'||t.id==='planner'||t.id==='energy'));const f=feats[S.feat%feats.length];
  const list=TOOLS.filter(visible);
  return `<div class="scroll D"><div class="dark-panel feature on-dark"><div class="txt"><span class="label">${isUpd(f)?'Nieuwe versie':'Uitgelicht'}</span><h2>${esc(f.name)}</h2><p>${esc(f.desc)}</p>${chips(f)}${ver(f)}<div style="display:flex;gap:10px;margin-top:6px">${action(f)}<button class="btn glass">${ic('git.repository')}Broncode</button></div><div class="dots">${feats.map((x,i)=>`<i class="${i===S.feat%feats.length?'on':''}" data-feat="${i}"></i>`).join('')}</div></div><div class="shot"><img src="${f.preview}" alt=""></div></div>
  <div class="body"><div class="sect"><div><span class="label">Het OpenAEC-ecosysteem</span><div class="h2">Alle tools · ${list.length}</div></div><span class="sp"></span>${searchBox()}</div><div style="display:flex;gap:8px;flex-wrap:wrap">${discPills()}</div>
  <div class="grid">${list.map(t=>`<div class="card tc ${isUpd(t)?'feat':''}">${thumb(t,120)}<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">${chips(t)}${pills(t)}</div><h3>${esc(t.name)}</h3><p>${esc(t.desc)}</p><div class="meta">${t.commits?`<span>● ${t.commits} commits</span>`:''}${t.latest?`<span>v${t.latest}</span>`:'<span>webtool</span>'}</div><div class="foot">${action(t,'sm')}<span class="sp"></span><a class="link">GitHub →</a></div></div>`).join('')}</div></div></div>`}},
E:{name:'E · Mix A + D',note:'<b>Mix van A en D</b>: alleen het bovenste vlak is donker, met links de kop en de acties van A en rechts het wisselende uitgelichte blok van D. Daaronder volgt alles het thema: desktop-apps en webtools zijn twee secties met dezelfde websitetegels, gescheiden door een duidelijke kop.',render(){
  const feats=TOOLS.filter(t=>t.preview&&(isUpd(t)||['calc','planner','energy','pointcloud'].includes(t.id)));const f=feats[S.feat%feats.length];
  const d=TOOLS.filter(t=>t.kind==='desktop'&&visible(t)),w=TOOLS.filter(t=>t.kind==='web'&&visible(t));
  const card=t=>`<div class="card tc ${isUpd(t)?'feat':''}">${thumb(t,150)}<div class="head">${logo(t,44)}<div class="t"><h3>${esc(t.name)}</h3><div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">${chips(t)}${statusPill(t)}${t.site?`<span class="pill ${t.site==='Beta'?'beta':''}">${esc(t.site)}</span>`:''}</div></div></div><p>${esc(t.desc)}</p><div class="meta">${t.kind==='web'?`${ic('link.open-external',12)}<span>webtool</span>`:(isUpd(t)?`<span>v${t.installed} → <b style="font-weight:400;color:var(--amber-text)">v${t.latest}</b></span>`:`<span>v${t.installed||t.latest}</span>`)}${t.commits?`<span>● ${t.commits} commits</span>`:''}</div><div class="foot">${action(t,'sm')}<span class="sp"></span>${icons(t).replace(/class="ibtn"/g,'class="ibtn"')}</div></div>`;
  const section=(label,title,sub,list,empty,search)=>`<div><div class="sect"><div><span class="label">${label} · ${list.length}</span><div class="h2">${title}</div><div class="muted">${sub}</div></div><span class="sp"></span>${search?searchBox():''}</div><div class="grid">${list.map(card).join('')||`<p class="muted">${empty}</p>`}</div></div>`;
  return `<div class="scroll E"><div class="top3 on-dark"><div><span class="label">OpenAEC Installer</span><h2>Alle bouwsoftware,<br><span class="acc">één plek.</span></h2><p>Ontdek, installeer, werk bij en start de open source tools van de OpenAEC Foundation.</p>
  <div class="cta"><button class="btn primary" data-act="all">${ic('software.update')}Alles bijwerken (${upd()})</button><button class="btn glass">${ic('ui.check-updates')}Controleren op updates</button></div>
  <div class="stats"><span><b>${TOOLS.length}</b> tools</span><span><b>${count('inst')}</b> geïnstalleerd</span><span><b>${upd()}</b> updates</span><span><b>${count('web')}</b> webtools</span></div></div>
  <div class="glass spot"><div class="shot"><img src="${f.preview}" alt=""><span class="label tag">${isUpd(f)?'Nieuwe versie':'Uitgelicht'}</span></div><div class="row3">${logo(f,40)}<div style="flex:1;min-width:0"><span class="nm">${esc(f.name)}</span>${ver(f)}</div>${action(f,'sm')}</div><div class="dots">${feats.map((x,i)=>`<i class="${i===S.feat%feats.length?'on':''}" data-feat="${i}"></i>`).join('')}</div></div></div>
  <div class="body"><div class="tools">${discPills()}</div>
  ${section('Desktop-apps','Installeren en starten op je computer','Windows-installers en AppImages van GitHub Releases. De installer ziet welke versie je hebt.',d,'Geen desktop-apps voor dit filter.',true)}
  <div class="divider">${ic('software.open-webtab',14)} Webtools</div>
  ${section('Webtools','Direct in je browser','Geen installatie nodig. Ze openen in de installer of in je eigen browser.',w,'Geen webtools voor dit filter.')}
  </div></div>`}},
};
function discPills(){const all=`<span class="fpill ${!S.disc&&S.filter==='all'?'on':''}" data-filter="all">Alle <span class="n">${TOOLS.length}</span></span>`;
  return all+`<span class="fpill ${S.filter==='inst'?'on':''}" data-filter="inst">Geïnstalleerd <span class="n">${count('inst')}</span></span><span class="fpill ${S.filter==='upd'?'on':''}" data-filter="upd">Updates <span class="n">${upd()}</span></span>`+'AECI'.split('').map(d=>`<span class="fpill ${S.disc===d?'on':''}" data-disc="${d}"><span class="d">${d}</span>${DISC[d]} <span class="n">${TOOLS.filter(t=>t.disc.includes(d)).length}</span></span>`).join('')}
function searchBox(){return `<label class="search">${ic('view.search')}<input id="q" placeholder="Zoek een tool" value="${esc(S.q)}"></label>`}
function render(){const v=VARIANTS[S.v];document.getElementById('app').innerHTML=v.render();document.getElementById('note').innerHTML=v.note;
  document.getElementById('variants').innerHTML=Object.entries(VARIANTS).map(([k,x])=>`<button class="${k===S.v?'on':''}" data-v="${k}">${x.name}</button>`).join('');
  document.getElementById('status').innerHTML=`<span>${count('inst')} van ${TOOLS.filter(t=>t.kind==='desktop').length} desktop-apps geïnstalleerd</span><span>${upd()?upd()+' updates beschikbaar':'Alles is bijgewerkt'}</span><span class="r">installer 1.5.0</span>`;
  const q=document.getElementById('q');if(q){q.oninput=e=>{S.q=e.target.value;const pos=e.target.selectionStart;render();const n=document.getElementById('q');n.focus();n.setSelectionRange(pos,pos)}}}
function install(id){if(S.progress[id]!==undefined)return;S.progress[id]=0;const t=TOOLS.find(x=>x.id===id);const tick=()=>{S.progress[id]=Math.min(100,S.progress[id]+7);if(S.progress[id]>=100){delete S.progress[id];t.installed=t.latest}else setTimeout(tick,110);render()};setTimeout(tick,110);render()}
document.addEventListener('click',e=>{const el=e.target.closest('[data-v],[data-filter],[data-disc],[data-sel],[data-act],[data-feat],#themeL,#themeD');if(!el)return;
  if(el.id==='themeL'||el.id==='themeD'){document.body.classList.toggle('dark',el.id==='themeD');document.getElementById('themeL').classList.toggle('on',el.id==='themeL');document.getElementById('themeD').classList.toggle('on',el.id==='themeD');return}
  if(el.dataset.v){S.v=el.dataset.v;S.filter='all';S.disc='';}
  if(el.dataset.filter){S.filter=el.dataset.filter;S.disc=''}
  if(el.dataset.disc){S.disc=S.disc===el.dataset.disc?'':el.dataset.disc;S.filter='all'}
  if(el.dataset.sel)S.sel=el.dataset.sel;
  if(el.dataset.feat!==undefined)S.feat=+el.dataset.feat;
  if(el.dataset.act==='install')install(el.dataset.id);
  if(el.dataset.act==='all')TOOLS.filter(isUpd).forEach(t=>install(t.id));
  render()});
// #B, #C-donker: open a proposal and theme directly, for sharing and screenshots.
(()=>{const m=(location.hash||'').match(/^#([ABCDE])(-donker)?/);if(m){S.v=m[1];if(m[2])document.body.classList.add('dark'),document.getElementById('themeL').classList.remove('on'),document.getElementById('themeD').classList.add('on')}})();
// #E@1400 scrolls the window content, for screenshots further down.
(()=>{const m=(location.hash||'').match(/@(\d+)/);if(m)setTimeout(()=>{const el=document.querySelector('.scroll,.list');if(el)el.scrollTop=+m[1]},50)})();
setInterval(()=>{if((S.v==='D'||S.v==='E')&&!Object.keys(S.progress).length){S.feat++;render()}},6000);
render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
