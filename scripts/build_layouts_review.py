#!/usr/bin/env python3
"""Build the layouts review page (step 2.5) from the UI 0.4 tokens.

Writes design/ontwerp-0.4/layouts-review.html: full app screens for a ribbon app
(Open Calc Studio) and two workflow apps, switchable between the five themes.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import mix  # noqa: E402
from review_icons import SPRITE_MARK, icon, sprite, usage  # noqa: E402

TOKENS = json.loads((ROOT / "design/ontwerp-0.4/tokens-0.4.json").read_text(encoding="utf-8"))
OUT = ROOT / "design/ontwerp-0.4/layouts-review.html"
ICON_DIR = ROOT / "crates/openaec-ui/assets/icons"
R = TOKENS["radius"]
F = TOKENS["font"]["size"]
S = TOKENS["shell"]
THEMES = TOKENS["themes"]


def esc(s):
    return html.escape(str(s))


def theme_vars(th):
    c = th["color"]
    hc = th.get("high-contrast", False)
    v = {"--" + k: val for k, val in c.items()}
    v.update({
        "--tint": c["panel"] if hc else c["selected"],
        "--tintline": c["accent"] if hc else mix(c["accent"], 0.35, c["panel"]),
        "--hoverline": c["accent"] if hc else "transparent",
        "--gridline": mix(c["workspace-text"], 0.10, c["workspace"]),
        "--shpop": th["shadow"]["popup"],
        "--shdlg": th["shadow"]["dialog"],
        "--shpanel": th["shadow"]["panel"],
        "--overlay": th["overlay"],
        "--disline": "dashed" if th["disabled-style"] == "dashed" else "solid",
        "--selring": f"inset 0 0 0 2px {c['selected-bar']}" if hc else f"inset 3px 0 0 {c['selected-bar']}",
        "--seltd": f"inset 0 2px 0 {c['selected-bar']}, inset 0 -2px 0 {c['selected-bar']}" if hc else "none",
        "--selfirst": f"inset 2px 0 0 {c['selected-bar']}, inset 0 2px 0 {c['selected-bar']}, inset 0 -2px 0 {c['selected-bar']}" if hc else f"inset 3px 0 0 {c['selected-bar']}",
        "--sellast": f"inset -2px 0 0 {c['selected-bar']}, inset 0 2px 0 {c['selected-bar']}, inset 0 -2px 0 {c['selected-bar']}" if hc else "none",
    })
    return v


THEME_JSON = json.dumps({tid: theme_vars(th) for tid, th in THEMES.items()})


# ---------- shared building blocks ----------
def titlebar(app):
    return f"""<div class="tb"><span class="qa"><span class="logo"></span>{icon("save", 14)}{icon("undo", 14)}{icon("redo", 14)}</span>
<span class="ttl">{esc(app)}</span><span class="win">&#8212;&nbsp;&nbsp;&#9633;&nbsp;&nbsp;&#10005;</span></div>"""


def ribbon(disabled=False):
    d = " dis" if disabled else ""

    def big(n, label, cls=""):
        return f'<span class="big{cls}"><span class="ic">{icon(n, 22)}</span><span>{esc(label)}</span></span>'

    def small(n, label, cls=""):
        return f'<span class="sml{cls}">{icon(n, 16)}<span>{esc(label)}</span></span>'

    return f"""<div class="tabs"><span class="t file">Bestand</span><span class="t on">Start</span><span class="t">Invoegen</span><span class="t">Begroting</span><span class="t">Beeld</span></div>
<div class="rb">
  <div class="g"><div class="gb">{big("save", "Opslaan", d)}<div class="col3">{small("undo", "Ongedaan", d)}{small("redo", "Opnieuw", d)}{small("duplicate", "Dupliceren", d)}</div></div><div class="gl">Bestand</div></div>
  <div class="g"><div class="gb">{big("new", "Post", d)}{big("grid", "Hoofdstuk", d)}{big("import", "Importeren")}</div><div class="gl">Invoegen</div></div>
  <div class="g"><div class="gb">{big("measure.area", "Hoeveelheid", d)}{big("export", "Exporteren", d)}</div><div class="gl">Begroting</div></div>
  <div class="g"><div class="gb">{big("panelleft", "Verkenner", " on")}{big("panelright", "Eigenschappen", " on")}</div><div class="gl">Panelen</div></div>
</div>"""


def docs(tabs):
    out = []
    for i, (name, mod) in enumerate(tabs):
        cls = " on" if i == 0 else ""
        dot = '<i class="mod"></i>' if mod else ""
        out.append(f'<span class="d{cls}">{esc(name)}{dot}<span class="x">{icon("close", 12)}</span></span>')
    return f'<div class="docs">{"".join(out)}</div>'


def explorer(empty=False):
    if empty:
        return '<div class="pnl"><div class="ph"><span>Verkenner</span></div><div class="pempty">Geen project geopend</div></div>'
    rows = [("tree.collapse", "cube", "Kade 12", "", 0), ("tree.expand", "grid", "21 Fundering", "sel", 1),
            ("tree.expand", "grid", "22 Vloeren", "", 1), ("tree.expand", "grid", "23 Gevels", "", 1),
            ("tree.expand", "grid", "24 Daken", "", 1), ("tree.expand", "grid", "30 Installaties", "", 1)]
    items = "".join(f'<div class="tn {cls} l{lvl}">{icon(a, 12)}{icon(b, 14)}<span>{esc(t)}</span></div>' for a, b, t, cls, lvl in rows)
    return f'<div class="pnl"><div class="ph"><span>Verkenner</span><span class="ib">{icon("search", 14)}</span></div>{items}</div>'


def properties(empty=False):
    if empty:
        return '<div class="pnl right"><div class="ph"><span>Eigenschappen</span></div><div class="pempty">Geen selectie</div></div>'
    return f"""<div class="pnl right"><div class="ph"><span>Eigenschappen</span></div>
<div class="sec">{icon("tree.collapse", 12)}<span>Post</span></div>
<div class="pr"><span>Code</span><code>21.20</code></div>
<div class="pr"><span>Omschrijving</span><span class="fld">Poeren</span></div>
<div class="pr"><span>Eenheid</span><span class="fld sel">st{icon("disclosure-expanded", 12)}</span></div>
<div class="pr"><span>Hoeveelheid</span><code>12</code></div>
<div class="pr"><span>Eenheidsprijs</span><code>€ 290,00</code></div>
<div class="sec">{icon("tree.collapse", 12)}<span>Berekening</span></div>
<div class="pr"><span>Meenemen</span><span class="box on">{icon("check", 12)}</span></div>
<div class="pr"><span>Totaal</span><code>€ 3.480</code></div>
</div>"""


TABLE_ROWS = [("21.10", "Funderingsbalken", "48,50 m³", "€ 12.610", ""), ("21.20", "Poeren", "12 st", "€ 3.480", "sel"),
              ("21.30", "Werkvloer", "96,00 m²", "€ 2.304", ""), ("22.10", "Kanaalplaatvloer", "210,00 m²", "€ 18.900", ""),
              ("22.20", "Afwerkvloer", "198,00 m²", "€ 5.940", ""), ("23.10", "Kalkzandsteen", "340,00 m²", "€ 27.200", ""),
              ("23.20", "Gevelsteen", "312,00 m²", "€ 34.320", ""), ("24.10", "Dakplaten", "120,00 m²", "€ 9.600", "")]


def table():
    rows = "".join(f'<tr class="{cls}"><td><code>{a}</code></td><td>{esc(b)}</td><td class="r"><code>{c}</code></td><td class="r"><code>{d}</code></td></tr>'
                   for a, b, c, d, cls in TABLE_ROWS)
    return f'<table class="tbl"><tr><th>Code</th><th>Omschrijving</th><th class="r">Hoeveelheid</th><th class="r">Bedrag</th></tr>{rows}</table>'


def status(text, right="", progress=None):
    prog = (f'<span class="sprog"><span>{esc(progress[0])}</span><i><b style="width:{progress[1]}%"></b></i><code>{progress[1]}%</code></span>'
            if progress else "")
    return f'<div class="sb"><span>{esc(text)}</span>{prog}<span class="sr">{esc(right)}</span></div>'


def frame(content, label, note, cls=""):
    return f'<figure class="shot"><div class="app {cls}">{content}</div><figcaption><b>{esc(label)}</b>{esc(note)}</figcaption></figure>'


# ---------- ribbon app screens ----------
def scr_workspace():
    body = f'<div class="body">{explorer()}<div class="ws"><div class="doc">{table()}</div></div>{properties()}</div>'
    return frame(titlebar("Open Calc Studio") + ribbon() + docs([("Kade 12.ocs", True), ("Variant B.ocs", False)]) + body
                 + status("Gereed", "91 posten · totaal € 1.214.560"),
                 "1 · Werkruimte", "Titelbalk 32, linttabs 28, lint 94, documenttabs 30, panelen 240 en statusbalk 22 px.")


def scr_start():
    cards = "".join(f"""<div class="pcard"><div class="thumb"><i></i></div><div class="pbody"><b>{esc(n)}</b><code>{esc(m)}</code><span class="pill" style="--pc:var(--{k})">{esc(st)}</span></div></div>"""
                    for n, m, k, st in [("Kade 12", "16-10-2026 · 91 posten", "success", "Gereed"),
                                        ("Schoolgebouw", "02-10-2026 · 240 posten", "warning", "Controle"),
                                        ("Brug Noord", "28-09-2026 · 12 posten", "info", "Concept")])
    tiles = "".join(f'<div class="task"><span class="ico">{icon(i, 22)}</span><span class="tt"><b>{esc(t)}</b><small>{esc(dsc)}</small></span></div>'
                    for i, t, dsc in [("new", "Leeg project", "Begin zonder posten"), ("grid", "Woningbouw", "Sjabloon voor een woning"),
                                      ("open", "Openen", "Open een bestaand project")])
    recent = "".join(f'<div class="rrow">{icon("grid", 16)}<span class="rn"><b>{esc(n)}</b><small>{esc(pth)}</small></span><code>{d}</code></div>'
                     for n, pth, d in [("Kade 12.ocs", "D:/Projecten/Kade 12", "16-10-2026"), ("Variant B.ocs", "D:/Projecten/Kade 12", "14-10-2026"),
                                       ("Schoolgebouw.ocs", "D:/Projecten/School", "02-10-2026")])
    content = f"""<div class="start"><div class="sh"><h3>Welkom bij Open Calc Studio</h3><span class="mono">Versie 0.4.0</span></div>
<div class="scols"><div><div class="mono">Nieuw</div><div class="tasks">{tiles}</div></div>
<div><div class="mono">Recente projecten</div><div class="cards">{cards}</div><div class="mono">Recente bestanden</div><div class="list">{recent}</div></div></div></div>"""
    return frame(titlebar("Open Calc Studio") + content + status("Gereed", "Laatste project: Kade 12"),
                 "2 · Startscherm", "Bij het openen. Nieuw links, recente projecten en bestanden rechts. Geen lint, omdat er nog geen document is.")


def scr_backstage():
    nav = "".join(f'<div class="nav {cls}">{icon(i, 18)}<span>{esc(t)}</span></div>' for i, t, cls in [
        ("back", "Terug", ""), ("new", "Nieuw", ""), ("open", "Openen", "on"), ("save", "Opslaan", ""), ("saveas", "Opslaan als", ""),
        ("export", "Exporteren", ""), ("print", "Afdrukken", ""), ("settings", "Instellingen", ""), ("help", "Over", "")])
    tiles = "".join(f'<div class="task"><span class="ico">{icon(i, 22)}</span><span class="tt"><b>{esc(t)}</b><small>{esc(dsc)}</small></span></div>'
                    for i, t, dsc in [("open", "Bladeren", "Kies een bestand op deze computer"), ("import", "Importeren", "Lees een CSV- of IFC-bestand in")])
    recent = "".join(f'<div class="rrow">{icon("grid", 16)}<span class="rn"><b>{esc(n)}</b><small>{esc(pth)}</small></span><code>{d}</code></div>'
                     for n, pth, d in [("Kade 12.ocs", "D:/Projecten/Kade 12", "16-10-2026"), ("Variant B.ocs", "D:/Projecten/Kade 12", "14-10-2026"),
                                       ("Schoolgebouw.ocs", "D:/Projecten/School", "02-10-2026"), ("Brug Noord.ocs", "D:/Projecten/Brug", "28-09-2026")])
    content = f"""<div class="bs"><div class="bsnav">{nav}</div><div class="bsc"><h3>Openen</h3><div class="mono">Taken</div><div class="tasks">{tiles}</div>
<div class="mono">Recent</div><div class="list">{recent}</div></div></div>"""
    return frame(titlebar("Open Calc Studio") + content + status("Bestand-menu", ""),
                 "3 · Bestand-menu", "Navigatie van 260 px links, taaktegels en recente bestanden rechts. Lint en documenttabs zijn verborgen.")


def scr_empty():
    body = f"""<div class="body">{explorer(True)}<div class="ws theme"><div class="empty"><span class="eicon">{icon("open", 32)}</span><b>Geen document geopend</b><span>Open een project of begin een nieuwe begroting.</span><span class="btn p">{icon("new", 16)}Nieuw project</span></div></div>{properties(True)}</div>"""
    return frame(titlebar("Open Calc Studio") + ribbon(disabled=True) + '<div class="docs"></div>' + body + status("Geen document", ""),
                 "4 · Lege staat", "Lintknoppen die een document nodig hebben, zijn uitgeschakeld. De lege staat volgt het thema.")


def scr_progress():
    banner = f'<div class="ban">{icon("status.error", 16)}<span><b>Fout.</b> Export naar IFC mislukt: 3 posten hebben geen classificatie.</span><span class="lnk">Toon posten</span><span class="ib">{icon("close", 12)}</span></div>'
    body = f'<div class="body">{explorer()}<div class="ws"><div class="doc">{banner}{table()}</div></div>{properties()}</div>'
    toast = f'<div class="toast"><span class="ti">{icon("status.success", 16)}</span><span><b>PDF opgeslagen</b><br><small>Kade 12.pdf · 16:42</small></span><span class="lnk">Openen</span></div>'
    return frame(titlebar("Open Calc Studio") + ribbon() + docs([("Kade 12.ocs", True), ("Variant B.ocs", False)]) + body
                 + status("Exporteren", "91 posten", ("Excel", 64)) + toast,
                 "5 · Voortgang, fout en melding", "Voortgang in de statusbalk, een fout bovenaan het document en een melding rechtsonder.", "rel")


def scr_dialog():
    body = f'<div class="body">{explorer()}<div class="ws"><div class="doc">{table()}</div></div>{properties()}</div>'
    dialog = f"""<div class="dim"></div><div class="dlgl"><div class="dlg"><div class="dh"><b>Wijzigingen opslaan?</b><span class="ib">{icon("close", 12)}</span></div>
<div class="db">Het project <b>Kade 12</b> heeft wijzigingen die nog niet zijn opgeslagen. Wil je ze opslaan voordat je afsluit?</div>
<div class="df"><span class="btn g">Niet opslaan</span><span class="btn s">Annuleren</span><span class="btn p">{icon("save", 16)}Opslaan</span></div></div></div>"""
    return frame(titlebar("Open Calc Studio") + ribbon() + docs([("Kade 12.ocs", True), ("Variant B.ocs", False)]) + body
                 + status("Gereed", "91 posten") + dialog,
                 "6 · Onopgeslagen wijzigingen", "Dialoog van 420 px boven de gedimde app. Escape annuleert, Enter slaat op.", "rel")


# ---------- workflow app screens ----------
ENERGY_NAV = [("cube", "Project"), ("grid", "Gebouw"), ("controls", "Installaties"), ("measure", "Resultaat")]
FIELD_NAV = [("cube", "Project"), ("grid", "Plattegronden"), ("measure", "Inspectie"), ("open", "Foto's"), ("export", "Rapport")]


def nav_side(items, active, extra=True):
    rows = [(i, t, "on" if t == active else "") for i, t in items]
    if extra:
        rows.append(("settings", "Instellingen", ""))
    return '<div class="side">' + "".join(f'<div class="snav {cls}">{icon(i, 18)}<span>{esc(t)}</span></div>' for i, t, cls in rows) + "</div>"


def nav_top(items, active):
    names = [t for _, t in items]
    idx = names.index(active)
    out = []
    for n, t in enumerate(names):
        cls = "done" if n < idx else ("on" if n == idx else "")
        mark = icon("check", 12) if n < idx else str(n + 1)
        out.append(f'<span class="step {cls}"><code>{mark}</code>{esc(t)}</span>')
    return f'<div class="steps">{"".join(out)}</div>'


def energy_content():
    return f"""<div class="fh"><h3>Gebouw</h3><span class="pill" style="--pc:var(--warning)">1 veld ontbreekt</span></div>
<div class="fgrid"><div class="fcard"><div class="mono">Gebouwgegevens</div>
<div class="frow"><label>Gebruiksoppervlakte</label><span class="fld"><code>100,0</code><small>m²</small></span></div>
<div class="frow"><label>Bouwjaar</label><span class="fld"><code>2026</code></span></div>
<div class="frow"><label>Type woning</label><span class="fld sel">Tussenwoning{icon("disclosure-expanded", 12)}</span></div>
<div class="frow"><label>Aantal bouwlagen</label><span class="fld"><code>3</code></span></div></div>
<div class="fcard"><div class="mono">Schil</div>
<div class="frow"><label>Rc gevel</label><span class="fld"><code>4,70</code><small>m²K/W</small></span></div>
<div class="frow"><label>Rc dak</label><span class="fld err"><code>-</code><small>m²K/W</small></span></div>
<div class="ferr">Vul de Rc-waarde van het dak in.</div></div></div>"""


def field_content():
    rows = "".join(f'<div class="rrow">{icon(i, 16)}<span class="rn"><b>{esc(t)}</b><small>{esc(sub)}</small></span><span class="pill" style="--pc:var(--{k})">{esc(st)}</span></div>'
                   for i, t, sub, k, st in [("grid", "Gevel noord", "Conditie 3 · 4 gebreken", "warning", "Matig"),
                                            ("grid", "Dakbedekking", "Conditie 2 · 1 gebrek", "success", "Goed"),
                                            ("grid", "Kozijnen begane grond", "Conditie 5 · 7 gebreken", "error", "Slecht"),
                                            ("grid", "Fundering", "Nog niet geïnspecteerd", "info", "Open")])
    return f'<div class="fh"><h3>Inspectie</h3><span class="btn p">{icon("new", 16)}Bouwdeel</span></div><div class="list wide">{rows}</div>'


def flow_screen(app, kind, content, nav_items, active, label, note, stat):
    bar = '<div class="fbar"><span class="btn s">Vorige</span><span class="btn p">Volgende</span></div>'
    if kind == "side":
        body = f'<div class="flow">{nav_side(nav_items, active)}<div class="fmain">{content}{bar}</div></div>'
    else:
        body = f'<div class="topflow">{nav_top(nav_items, active)}<div class="fmain">{content}{bar}</div></div>'
    return frame(titlebar(app) + body + status(*stat), label, note)


def scr_flow_side():
    return flow_screen("Open Energy Studio", "side", energy_content(), ENERGY_NAV, "Gebouw",
                       "7 · Werkstroom met zijbalk", "Zoals Energy, Speech en Composer. Zijbalk van 220 px, formulier in kaarten en een actiebalk onderaan.",
                       ("Niet berekend", "NTA 8800"))


def scr_flow_top():
    return flow_screen("Open Field Studio", "top", field_content(), FIELD_NAV, "Inspectie",
                       "8 · Werkstroom met stappen bovenaan", "Zoals Field. Genummerde stappen in mono, afgeronde stappen met een vinkje, de actieve met een amberkleurige streep.",
                       ("Opgeslagen", "4 bouwdelen"))


def flow_compare():
    return "".join([
        '<div class="cmp"><div class="mono">Energy: secties die je in elke volgorde invult</div>',
        flow_screen("Open Energy Studio", "side", energy_content(), ENERGY_NAV, "Gebouw",
                    "Energy met zijbalk", "Je springt vrij tussen Project, Gebouw en Installaties. Resultaat kun je altijd openen.", ("Niet berekend", "NTA 8800")),
        flow_screen("Open Energy Studio", "top", energy_content(), ENERGY_NAV, "Gebouw",
                    "Energy met stappen", "Suggereert dat je eerst Project moet afronden. Dat klopt niet voor Energy.", ("Niet berekend", "NTA 8800")),
        "</div>",
        '<div class="cmp"><div class="mono">Field: een vaste volgorde op locatie</div>',
        flow_screen("Open Field Studio", "top", field_content(), FIELD_NAV, "Inspectie",
                    "Field met stappen", "Je ziet waar je bent in het proces en wat nog komt.", ("Opgeslagen", "4 bouwdelen")),
        flow_screen("Open Field Studio", "side", field_content(), FIELD_NAV, "Inspectie",
                    "Field met zijbalk", "Werkt ook, maar je ziet niet meer welke stappen al klaar zijn.", ("Opgeslagen", "4 bouwdelen")),
        "</div>",
    ])


# ---------- status bar comparison (always Licht) ----------
def statusbar_compare():
    light = ";".join(f"{k}:{v}" for k, v in theme_vars(THEMES["light"]).items())
    a = scr_workspace().replace("1 · Werkruimte", "Instelling: Altijd donker").replace('<div class="app ', '<div class="app darksb ', 1).replace(
        "Titelbalk 32, linttabs 28, lint 94, documenttabs 30, panelen 240 en statusbalk 22 px.",
        "Night Build, zoals de voettekst van de website.")
    b = scr_workspace().replace("1 · Werkruimte", "Standaard: volgt het thema").replace(
        "Titelbalk 32, linttabs 28, lint 94, documenttabs 30, panelen 240 en statusbalk 22 px.",
        "In Licht in de kleur van de panelen, met een lijn erboven.")
    return f'<div class="fixedlight" style="{light}">{a}{b}</div>'


ribbon_screens = scr_workspace() + scr_start() + scr_backstage() + scr_empty() + scr_progress() + scr_dialog()
flow_screens = scr_flow_side() + scr_flow_top()
flow_cmp = flow_compare()
sb_cmp = statusbar_compare()
theme_buttons = "".join(f'<button data-t="{tid}"{" class=on" if tid == "light" else ""}>{esc(th["name"])}</button>' for tid, th in THEMES.items())

CSS = r"""
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf');font-weight:400}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Medium.ttf');font-weight:500}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-SemiBold.ttf');font-weight:600 800}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Medium.ttf');font-weight:500}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}
@font-face{font-family:'JetBrains Mono';src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
*{box-sizing:border-box}
body{margin:0;background:#f3f3f2;color:#303039;font:14px/1.5 Inter,system-ui,sans-serif}
header{background:#303039;color:#fff;padding:26px max(22px,calc((100vw - 1420px)/2));border-bottom:3px solid #dc7900}
header a{color:#ffc180}header p{margin:0;color:#dddde3;max-width:1000px}
h1{font:700 29px/1.2 'Space Grotesk',Inter,system-ui,sans-serif;margin:8px 0}
h2{font:500 22px/1.3 'Space Grotesk',Inter,system-ui,sans-serif;margin:40px 0 6px}
main{max-width:1460px;margin:auto;padding:23px 22px 46px}p{max-width:980px}
.q{background:#fff;border-left:3px solid #dc7900;padding:12px 16px;max-width:1000px;margin:12px 0 16px}
.switch{position:sticky;top:0;z-index:20;display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:10px 0;background:#f3f3f2}
.switch span{font:11px 'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;color:#55555f;margin-right:6px}
.switch button{font:600 13px Inter,sans-serif;padding:6px 12px;border:1px solid #c9c9cf;background:#fff;border-radius:6px;cursor:pointer}
.switch button.on{background:#D97706;border-color:#D97706;color:#1C1917}
.shots{display:flex;flex-direction:column;gap:28px}
.shot{margin:0;overflow-x:auto;scroll-margin-top:60px}
.shot figcaption{margin-top:8px;font-size:13px;color:#55555f;max-width:1000px}.shot figcaption b{display:block;color:#303039;font-size:15px}
code{font-family:'JetBrains Mono',monospace;font-size:var(--fl)}
footer{color:#6b6b75;font-size:12px;margin-top:34px}
/* B2 icons: primary part follows currentColor, accent part follows the theme accent */
.pane,.win,.app{--icon-accent:var(--accent)}
.dis .b2,.b2.dis,.dis.b2{--icon-accent:currentColor}
.ban .b2,.bi .b2,.ti .b2,.ban>.b2{--icon-accent:currentColor}


/* app frame */
.app{width:1180px;height:700px;display:flex;flex-direction:column;background:var(--frame);color:var(--text);font-size:var(--fb);line-height:1.35;border:1px solid var(--border);box-shadow:0 10px 30px rgba(0,0,0,.12);overflow:hidden}
.app.rel{position:relative}
.app svg{flex:0 0 auto}
.mono,.ph span:first-child,.gl,.sec span,.tbl th{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:var(--fl);color:var(--text-secondary);font-weight:400}
.tb{height:32px;flex:0 0 32px;display:flex;align-items:center;padding:0 10px;background:var(--panel);border-bottom:1px solid var(--border)}
.qa{display:flex;gap:10px;align-items:center;color:var(--text-secondary);width:200px}
.logo{width:14px;height:14px;border-radius:3px;background:var(--accent)}
.ttl{flex:1;text-align:center;font-weight:600;color:var(--accent-text)}
.win{width:200px;text-align:right;color:var(--text-secondary);font-size:12px}
.tabs{height:28px;flex:0 0 28px;display:flex;align-items:stretch;gap:2px;padding:0 8px;background:var(--panel);border-bottom:1px solid var(--border)}
.t{display:flex;align-items:center;padding:0 12px;color:var(--text-secondary);font-weight:500;border-bottom:2px solid transparent}
.t.on{color:var(--text);font-weight:600;border-bottom-color:var(--accent)}
.t.file{align-self:center;height:22px;margin-right:8px;border-radius:var(--rm);background:var(--accent);color:var(--text-on-accent);font-weight:600;border:0}
.rb{height:94px;flex:0 0 94px;display:flex;background:var(--panel);border-bottom:1px solid var(--border)}
.g{display:flex;flex-direction:column;padding:4px 8px 0;position:relative}
.g:after{content:"";position:absolute;right:0;top:10px;bottom:10px;width:1px;background:var(--border)}
.gb{display:flex;gap:2px;flex:1}.gl{height:18px;line-height:18px;text-align:center}
.big{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:56px;height:66px;padding:5px 4px 0;font-size:var(--fl);border-radius:var(--rm)}
.big .ic{display:grid;place-items:center;width:32px;height:32px;border-radius:var(--rm);border:1px solid transparent}
.big.on .ic{background:var(--tint);border-color:var(--tintline);color:var(--accent-text)}
.col3{display:flex;flex-direction:column;gap:1px}
.sml{display:flex;align-items:center;gap:6px;height:22px;padding:0 6px;font-size:var(--fl);white-space:nowrap}
.dis,.dis svg{color:var(--text-disabled)}
.docs{height:30px;flex:0 0 30px;display:flex;align-items:flex-end;gap:4px;padding:0 4px;background:var(--docbar);border-bottom:1px solid var(--border)}
.d{display:flex;align-items:center;gap:6px;height:24px;padding:0 4px 0 10px;color:var(--text-secondary);border-radius:var(--rm) var(--rm) 0 0}
.d.on{background:var(--workspace);color:var(--workspace-text);font-weight:600}
.d .x{display:grid;place-items:center;width:16px;height:16px}
.mod{width:6px;height:6px;border-radius:50%;background:var(--accent)}
.body{flex:1;display:flex;min-height:0}
.pnl{width:240px;flex:0 0 240px;background:var(--panel);border-right:1px solid var(--border);overflow:hidden}
.pnl.right{border-right:0;border-left:1px solid var(--border)}
.ph{display:flex;justify-content:space-between;align-items:center;height:24px;padding:0 4px 0 8px;border-bottom:1px solid var(--border)}
.pempty{padding:24px 12px;text-align:center;color:var(--text-secondary)}
.ib{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:var(--rs);color:var(--text-secondary)}
.tn{display:flex;align-items:center;gap:6px;height:24px;padding:0 8px}.tn svg{color:var(--text-secondary)}.tn.l1{padding-left:24px}
.tn.sel{background:var(--tint);box-shadow:var(--selring);font-weight:600}
.sec{display:flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-bottom:1px solid var(--border)}.sec svg{color:var(--text-secondary)}
.pr{display:grid;grid-template-columns:40% 1fr;align-items:center;gap:8px;height:28px;padding:0 8px;border-bottom:1px solid var(--border)}
.pr>span:first-child{color:var(--text-secondary)}.pr code{text-align:right;font-size:var(--fb)}
.fld{display:inline-flex;align-items:center;justify-content:space-between;gap:6px;height:24px;padding:0 8px;background:var(--raised);border:1px solid var(--border-strong);border-radius:var(--rm);color:var(--text)}
.fld small{color:var(--text-secondary)}.fld svg{color:var(--text-secondary)}.fld.err{border:2px solid var(--error)}
.box{width:16px;height:16px;border-radius:var(--rs);display:grid;place-items:center;background:var(--accent);color:var(--text-on-accent)}
.ws{flex:1;min-width:0;background:var(--workspace);color:var(--workspace-text);overflow:hidden}
.doc{padding:16px}
.tbl{width:100%;border-collapse:collapse;background:var(--workspace);color:var(--workspace-text)}
.tbl th{height:28px;padding:0 10px;text-align:left;border-bottom:1px solid var(--border-strong)}
.tbl td{height:28px;padding:0 10px;border-bottom:1px solid var(--gridline)}
.tbl .r{text-align:right}.tbl code{font-size:var(--fb)}
.tbl tr.sel td{background:var(--tint);box-shadow:var(--seltd)}.tbl tr.sel td:first-child{box-shadow:var(--selfirst)}.tbl tr.sel td:last-child{box-shadow:var(--sellast)}
.sb{height:22px;flex:0 0 22px;display:flex;align-items:center;gap:16px;padding:0 10px;background:var(--statusbar);color:var(--statusbar-text);font-size:var(--fl);border-top:1px solid var(--border)}
.sb .sr{margin-left:auto}
.sprog{display:flex;align-items:center;gap:8px}.sprog i{display:block;width:140px;height:6px;border-radius:9999px;background:rgba(127,127,127,.35);overflow:hidden}
.sprog b{display:block;height:100%;background:var(--accent)}
/* start, backstage */
.start{flex:1;padding:28px 40px;overflow:hidden}
.sh{display:flex;justify-content:space-between;align-items:baseline}
h3{font:700 var(--fpg)/1.2 'Space Grotesk',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 6px}
.scols{display:grid;grid-template-columns:320px 1fr;gap:32px}
.mono{margin:18px 0 8px}
.tasks{display:flex;flex-direction:column;gap:8px;max-width:620px}
.task{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--raised);border:1px solid var(--border);border-radius:var(--rl)}
.ico{flex:0 0 40px;width:40px;height:40px;border-radius:var(--rm);background:var(--tint);border:1px solid var(--tintline);color:var(--accent-text);display:grid;place-items:center}
.tt{display:flex;flex-direction:column}.tt b{font-size:var(--fp)}.tt small{color:var(--text-secondary);font-size:var(--fb)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.pcard{background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden;box-shadow:var(--shpanel)}
.thumb{height:84px;background:var(--workspace);background-image:linear-gradient(var(--gridline) 1px,transparent 1px),linear-gradient(90deg,var(--gridline) 1px,transparent 1px);background-size:12px 12px;position:relative;border-bottom:1px solid var(--border)}
.thumb i{position:absolute;left:28%;top:22%;width:44%;height:54%;border:2px solid var(--accent);border-radius:2px}
.pbody{padding:10px 12px;display:flex;flex-direction:column;gap:3px;align-items:flex-start}.pbody b{font-size:var(--fp)}.pbody code{color:var(--text-secondary)}
.pill{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.06em;font-size:var(--fl);padding:1px 8px;border-radius:9999px;color:var(--pc);border:1px solid var(--pc)}
.list{background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden;max-width:620px}
.list.wide{max-width:none}
.rrow{display:flex;align-items:center;gap:12px;height:40px;padding:0 12px;border-bottom:1px solid var(--border)}.rrow:last-child{border-bottom:0}
.rrow svg{color:var(--text-secondary)}.rn{flex:1;display:flex;flex-direction:column}.rn b{font-weight:500}.rn small{font-size:var(--fl);color:var(--text-secondary)}.rrow code{color:var(--text-secondary)}
.bs{flex:1;display:flex;min-height:0}
.bsnav{width:260px;background:var(--panel);border-right:1px solid var(--border);padding:8px 0}
.nav{display:flex;align-items:center;gap:12px;height:40px;padding:0 20px;font-size:var(--fp)}.nav svg{color:var(--text-secondary)}
.nav.on{background:var(--tint);box-shadow:var(--selring);color:var(--accent-text);font-weight:600}.nav.on svg{color:var(--accent-text)}
.bsc{flex:1;padding:28px 40px;overflow:hidden}
/* empty, banner, toast, dialog */
.ws.theme{background:var(--panel);color:var(--text);display:grid;place-items:center}
.empty{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}
.empty .eicon{color:var(--accent-text)}.empty b{font-size:var(--fp)}.empty>span:not(.btn):not(.eicon){color:var(--text-secondary)}
.btn{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 12px;border-radius:var(--rm);font-weight:600;border:1px solid transparent;white-space:nowrap}
.btn.p{background:var(--accent);color:var(--text-on-accent)}.btn.s{background:var(--raised);color:var(--text);border-color:var(--border-strong)}.btn.g{color:var(--text)}
.ban{display:flex;align-items:center;gap:10px;padding:8px 8px 8px 12px;margin-bottom:12px;background:var(--error-tint);border-left:3px solid var(--error);border-radius:var(--rs);color:var(--text)}
.ban>svg{color:var(--error)}.ban>span:nth-child(2){flex:1}
.lnk{color:var(--accent-text);font-weight:600;text-decoration:underline}
.toast{position:absolute;right:16px;bottom:34px;display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--raised);color:var(--text);border:1px solid var(--border);border-radius:var(--rl);box-shadow:var(--shpop);z-index:3}
.toast .ti{color:var(--success);display:grid}.toast small{color:var(--text-secondary)}
.dim{position:absolute;inset:0;background:var(--overlay);z-index:3}
.dlgl{position:absolute;inset:0;display:grid;place-items:center;z-index:4}
.dlg{width:420px;background:var(--raised);color:var(--text);border:1px solid var(--border);border-radius:var(--rl);box-shadow:var(--shdlg);overflow:hidden}
.dh{display:flex;justify-content:space-between;align-items:center;padding:12px 12px 8px 20px}.dh b{font:700 var(--fd)/1.2 'Space Grotesk',Inter,sans-serif}
.db{padding:4px 20px 16px}.df{display:flex;justify-content:flex-end;gap:8px;padding:12px 20px;border-top:1px solid var(--border)}.df .btn.g{margin-right:auto}
/* workflow */
.flow{flex:1;display:flex;min-height:0}
.side{width:220px;background:var(--panel);border-right:1px solid var(--border);padding:8px}
.snav{display:flex;align-items:center;gap:10px;height:36px;padding:0 12px;border-radius:var(--rm);font-size:var(--fp)}.snav svg{color:var(--text-secondary)}
.snav.on{background:var(--tint);color:var(--accent-text);font-weight:600;box-shadow:var(--selring)}.snav.on svg{color:var(--accent-text)}
.fmain{flex:1;display:flex;flex-direction:column;min-width:0;padding:24px 32px 0}
.fh{display:flex;align-items:center;justify-content:space-between;gap:12px}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px;align-items:start}
.fcard{background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);padding:4px 16px 14px}
.fcard .mono{margin:12px 0 8px}
.frow{display:grid;grid-template-columns:160px 1fr;align-items:center;gap:8px;height:36px}
.frow label{color:var(--text-secondary)}.frow .fld{height:28px}
.ferr{margin-left:168px;color:var(--error);font-size:var(--fl)}
.fbar{margin-top:auto;display:flex;justify-content:flex-end;gap:8px;padding:12px 0;border-top:1px solid var(--border)}
.topflow{flex:1;display:flex;flex-direction:column;min-height:0}
.steps{height:44px;flex:0 0 44px;display:flex;align-items:stretch;gap:4px;padding:0 16px;background:var(--panel);border-bottom:1px solid var(--border)}
.step{display:flex;align-items:center;gap:8px;padding:0 14px;color:var(--text-secondary);font-weight:500;border-bottom:2px solid transparent}
.step code{display:grid;place-items:center;width:20px;height:20px;border-radius:50%;border:1px solid var(--border-strong);font-size:var(--fl)}
.step.done code{background:var(--tint);border-color:var(--tintline);color:var(--accent-text)}
.step.on{color:var(--text);font-weight:600;border-bottom-color:var(--accent)}.step.on code{background:var(--accent);border-color:var(--accent);color:var(--text-on-accent)}
.topflow .list{margin-top:12px}
.flow .list{margin-top:12px}
.cmp{display:flex;flex-direction:column;gap:20px}
.cmp>.mono{margin:6px 0 -8px;color:#55555f}
.app.darksb .sb{background:#2A2A32;color:#D4D1CC;border-top-color:#2A2A32}
"""

ROOTVARS = (f":root{{--rs:{R['small']}px;--rm:{R['medium']}px;--rl:{R['large']}px;--fl:{F['label']}px;--fb:{F['body']}px;"
            f"--fp:{F['panel-heading']}px;--fd:{F['dialog-heading']}px;--fpg:{F['page-heading']}px}}")

page = f"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · layouts 0.4</title>
<style>{ROOTVARS}{CSS}</style>
<header>
  <a href="README.md">Fase 2: ontwerp 0.4</a>
  <h1>Layouts · concept</h1>
  <p>Stap 2.5. Volledige schermen met alle besloten onderdelen uit het fundament, de tegels en de componenten. Kies hieronder een thema. De regels staan in <a href="05-layouts.md">05-layouts.md</a>.</p>
</header>
<main>{SPRITE_MARK}
  <div class="switch"><span>Thema</span>{theme_buttons}</div>
  <div class="screens" id="screens">
  <h2>Lint-app: Open Calc Studio</h2>
  <div class="q">Zes kernschermen van een app met een lint. Maten volgens de Tauri-template, vormgeving volgens de besluiten. Calc is het eerste proefproject.</div>
  <div class="shots">{ribbon_screens}</div>
  <h2>Werkstroom-apps</h2>
  <div class="q">Apps die je stap voor stap doorloopt, zonder lint. Twee vormen: een zijbalk met secties, zoals Energy, Speech en Composer, of genummerde stappen bovenaan, zoals Field. Beide gebruiken dezelfde titelbalk, statusbalk en componenten.</div>
  <div class="shots">{flow_screens}</div>

  <h2>Besloten: werkstroom met zijbalk of stappen</h2>
  <div class="q"><b>Besloten:</b> beide vormen kunnen. Gebruikers kiezen in de instellingen bij Navigatie, en de zijbalk is standaard. Dezelfde app in beide vormen. <b>Hulpregel voor ontwerpers:</b> een zijbalk als je de onderdelen in elke volgorde kunt bewerken, stappen bovenaan als de volgorde vastligt. Energy past daardoor bij de zijbalk, Field bij de stappen.</div>
  <div class="shots">{flow_cmp}</div>
  </div>

  <h2>Besloten: statusbalk volgt het thema</h2>
  <div class="q"><b>Besloten:</b> de statusbalk volgt het thema, in Licht dus licht. Met de instelling Statusbalk kan hij altijd donker. Dit voorbeeld staat altijd in Licht, ook als je bovenaan een ander thema kiest.</div>
  <div class="shots">{sb_cmp}</div>
  <footer>Gegenereerd door <code>scripts/build_layouts_review.py</code> uit <code>design/ontwerp-0.4/tokens-0.4.json</code>. Iconen uit <code>crates/openaec-ui/assets/icons</code>. Voorbeelddata is verzonnen.</footer>
</main>
<script>
const THEMES = {THEME_JSON};
const root = document.getElementById('screens');
function apply(t) {{
  for (const [k, v] of Object.entries(THEMES[t])) root.style.setProperty(k, v);
  document.querySelectorAll('.switch button').forEach(b => b.classList.toggle('on', b.dataset.t === t));
  try {{ localStorage.setItem('layouts-theme', t); }} catch (e) {{}}
}}
document.querySelectorAll('.switch button').forEach(b => b.addEventListener('click', () => apply(b.dataset.t)));
let start = 'light';
try {{ start = localStorage.getItem('layouts-theme') || 'light'; }} catch (e) {{}}
apply(THEMES[start] ? start : 'light');
</script>
</html>
"""

page = page.replace(SPRITE_MARK, sprite(), 1)
OUT.write_text(page, encoding="utf-8")
print(f"Wrote {OUT.relative_to(ROOT)}: 8 screens, {len(THEMES)} themes; {usage()}")
