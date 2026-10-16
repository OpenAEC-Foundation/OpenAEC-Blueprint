#!/usr/bin/env python3
"""Build the components review page (step 2.4) from the UI 0.4 tokens.

Writes design/ontwerp-0.4/componenten-review.html. Colours come from
design/ontwerp-0.4/tokens-0.4.json; derived colours are mixes of tokens.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import contrast, luminance, mix  # noqa: E402
from review_icons import SPRITE_MARK, icon, sprite, usage  # noqa: E402

TOKENS = json.loads((ROOT / "design/ontwerp-0.4/tokens-0.4.json").read_text(encoding="utf-8"))
OUT = ROOT / "design/ontwerp-0.4/componenten-review.html"
ICON_DIR = ROOT / "crates/openaec-ui/assets/icons"
R = TOKENS["radius"]
F = TOKENS["font"]["size"]
THEMES = TOKENS["themes"]


def esc(s):
    return html.escape(str(s))


def fmt(r):
    return f"{r:.2f}".replace(".", ",")


def tvars(th):
    c = th["color"]
    hc = th.get("high-contrast", False)
    v = {k.replace("-", ""): val for k, val in c.items()}
    v.update({
        "hoverbg": c["hover"],
        "pressedbg": c["pressed"],
        "dangerhover": c["panel"] if hc else mix(c["error"], 0.08 if th["kind"] == "light" else 0.06, c["raised"]),
        "dangerpressed": c["panel"] if hc else mix(c["error"], 0.16 if th["kind"] == "light" else 0.10, c["raised"]),
        "hoverline": c["accent"] if hc else "transparent",
        "tint": c["panel"] if hc else c["selected"],
        "tintline": c["accent"] if hc else mix(c["accent"], 0.35, c["panel"]),
        "track": c["border-strong"],
        "knob": "#FFFFFF" if th["kind"] == "dark" and not hc else c["raised"],
        "tipbg": c["raised"],
        "shpop": th["shadow"]["popup"],
        "shdlg": th["shadow"]["dialog"],
        "overlay": th["overlay"],
        "disline": "dashed" if th["disabled-style"] == "dashed" else "solid",
        "band": "#2A2A32",
        "bandtext": "#EDEBE8",
        "bandmuted": "#BDBAB5",
        "bandaccent": "#FBBF24",
        "bandhover": "#3A3A44",
        "worksecondary": mix(c["workspace-text"], 0.72, c["workspace"]),
        "workaccent": c["accent-text"] if (luminance(c["workspace"]) > 0.5) == (th["kind"] == "light") else (THEMES["light"]["color"]["accent-text"] if luminance(c["workspace"]) > 0.5 else THEMES["dark"]["color"]["accent-text"]),
    })
    for k in ("error", "success", "warning", "info"):
        v[k + "tint"] = c[k + "-tint"]
    return v


def svars(v):
    return ";".join(f"--{k}:{val}" for k, val in v.items())


# ---------- contrast checks ----------
CHECKS = [
    ("Primaire knop", "textonaccent", "accent", "t"),
    ("Primaire knop bij hover", "textonaccent", "accenthover", "t"),
    ("Secundaire knop", "text", "raised", "t"),
    ("Gevaarlijke knop", "error", "raised", "t"),
    ("Tekst op hover-vlak", "text", "hoverbg", "t"),
    ("Tekst op ingedrukt-vlak", "text", "pressedbg", "t"),
    ("Primaire knop ingedrukt", "textonaccent", "accentpressed", "t"),
    ("Gevaarlijke knop bij hover", "error", "dangerhover", "t"),
    ("Gevaarlijke knop ingedrukt", "error", "dangerpressed", "t"),
    ("Invoerveld: tekst", "text", "raised", "t"),
    ("Invoerveld: hulptekst", "textsecondary", "raised", "t"),
    ("Invoerveld: rand", "borderstrong", "raised", "u"),
    ("Invoerveld: rand op paneel", "borderstrong", "panel", "u"),
    ("Checkbox: rand", "borderstrong", "panel", "u"),
    ("Checkbox: vinkje op amber", "textonaccent", "accent", "u"),
    ("Schakelaar aan: spoor", "accent", "panel", "u"),
    ("Schakelaar uit: spoor", "track", "panel", "u"),
    ("Voortgang: gevulde balk", "accent", "panel", "u"),
    ("Tooltip", "text", "tipbg", "t"),
    ("Linttab, niet actief", "textsecondary", "panel", "t"),
    ("Linttab, actief", "accenttext", "panel", "t"),
    ("Lintgroeplabel (mono)", "textsecondary", "panel", "t"),
    ("Lintknop actief", "text", "tint", "t"),
    ("Documenttab, niet actief", "textsecondary", "docbar", "t"),
    ("Documenttab, actief", "workspacetext", "workspace", "t"),
    ("Tabelkop (mono)", "textsecondary", "panel", "t"),
    ("Geselecteerde rij", "text", "tint", "t"),
    ("Melding: tekst op fout-tint", "text", "errortint", "t"),
    ("Melding: tekst op waarschuwing-tint", "text", "warningtint", "t"),
    ("Melding: foutkleur op eigen tint", "error", "errortint", "u"),
    ("Dialoogtitel", "text", "raised", "t"),
    ("Lege staat: titel", "text", "panel", "t"),
    ("Lint C: tab in kopbalk", "bandmuted", "band", "t"),
    ("Lint C: actieve tab in kopbalk", "bandaccent", "band", "t"),
    ("Lint C: titel in kopbalk", "bandtext", "band", "t"),
    ("Lint B en C: actieve tab", "text", "panel", "t"),
    ("Lege staat: icoon", "accenttext", "panel", "u"),
    ("Lege staat: uitleg", "textsecondary", "panel", "t"),
]
rows, problems = [], []
for tid, th in THEMES.items():
    v = tvars(th)
    hc = th.get("high-contrast", False)
    for label, fg, bg, kind in CHECKS:
        need = 3.0 if kind == "u" else (7.0 if hc else 4.5)
        r = contrast(v[fg], v[bg])
        rows.append((th["name"], label, v[fg], v[bg], r, need))
        if r < need:
            problems.append(f"{th['name']}: {label} {fmt(r)} < {fmt(need)}")


# ---------- component builders ----------
STATES = [("", "Normaal"), ("hov", "Hover"), ("prs", "Ingedrukt"), ("foc", "Focus"), ("dis", "Uitgeschakeld")]


def state_table(render):
    head = "".join(f"<th>{esc(n)}</th>" for _, n in STATES)
    return lambda rows_: f'<table class="st"><tr><th></th>{head}</tr>' + "".join(
        f"<tr><th>{esc(lbl)}</th>" + "".join(f"<td>{render(kind, s)}</td>" for s, _ in STATES) + "</tr>" for kind, lbl in rows_) + "</table>"


def btn(kind, s):
    ic = icon("save", 16) if kind == "p" else ""
    txt = {"p": "Opslaan", "s": "Annuleren", "g": "Meer opties", "d": "Verwijderen"}[kind]
    return f'<span class="btn {kind} {s}">{ic}{txt}</span>'


def field(kind, s):
    if kind == "in":
        return f'<span class="fld {s}"><span>Kade 12</span></span>'
    if kind == "ph":
        return f'<span class="fld {s}"><span class="ph">Typ een naam</span></span>'
    if kind == "sel":
        return f'<span class="fld sel {s}"><span>Woningbouw</span>{icon("disclosure-expanded", 14)}</span>'
    return f'<span class="fld {s}">{icon("search", 14)}<span class="ph">Zoeken</span></span>'


def choice(kind, s):
    if kind == "cb":
        return f'<span class="cbx {s}"><i class="box on">{icon("check", 12)}</i>Aan</span>'
    if kind == "cb0":
        return f'<span class="cbx {s}"><i class="box"></i>Uit</span>'
    if kind == "rd":
        return f'<span class="cbx {s}"><i class="rad on"></i>Gekozen</span>'
    if kind == "sw":
        return f'<span class="cbx {s}"><i class="sw on"><b></b></i>Aan</span>'
    return f'<span class="cbx {s}"><i class="sw"><b></b></i>Uit</span>'


btn_table = state_table(btn)([("p", "Primair"), ("s", "Secundair"), ("g", "Stil"), ("d", "Gevaarlijk")])
fld_table = state_table(field)([("in", "Invoerveld"), ("ph", "Met hulptekst"), ("sel", "Keuzelijst"), ("sr", "Zoekveld")])
cho_table = state_table(choice)([("cb", "Checkbox aan"), ("cb0", "Checkbox uit"), ("rd", "Keuzerondje"), ("sw", "Schakelaar aan"), ("sw0", "Schakelaar uit")])


def pane(tid, inner, cap="", cls=""):
    th = THEMES[tid]
    return f'<figure class="pane {cls}" style="{svars(tvars(th))}">{inner}<figcaption><b>{esc(th["name"])}</b>{esc(cap)}</figcaption></figure>'


def pair(inner, cap="", cls="", stacked=False):
    wrap = "pair stacked" if stacked else "pair"
    return f'<div class="{wrap}">{pane("light", inner, cap, cls)}{pane("dark", inner, cap, cls)}</div>'


iconbtns = ('<div class="row">'
            + "".join(f'<span class="ib {s}">{icon(n, 16)}</span>' for n, s in [("undo", ""), ("redo", "hov"), ("panelleft", "on"), ("zoomin", "foc"), ("settings", "dis")])
            + '<span class="note">Normaal · hover · aan · focus · uitgeschakeld</span></div>')

extra = f"""
<div class="stack">
  <div class="lbl">Slider</div>
  <div class="slider"><i style="width:62%"></i><b style="left:62%"></b></div><code class="val">62%</code>
  <div class="lbl">Voortgang</div>
  <div class="prog"><i style="width:40%"></i></div><div class="row sm"><span>Exporteren naar PDF</span><code class="val">40%</code></div>
  <div class="prog busy"><i></i></div><div class="row sm"><span>Bezig, duur onbekend</span></div>
  <div class="lbl">Scrollbalk</div>
  <div class="scrollbox"><div class="lines">{'<p></p>' * 6}</div><div class="sbar"><i></i></div></div>
</div>"""

popups = f"""
<div class="poprow">
  <div>
    <div class="lbl">Tooltip</div>
    <div class="tipwrap"><span class="ib">{icon("save", 16)}</span><div class="tip">Opslaan <code>Ctrl+S</code></div></div>
  </div>
  <div>
    <div class="lbl">Menu</div>
    <div class="menu">
      <div class="mi">{icon("duplicate", 14)}<span>Dupliceren</span><code>Ctrl+D</code></div>
      <div class="mi hov">{icon("rename", 14)}<span>Hernoemen</span><code>F2</code></div>
      <div class="mi chk">{icon("check", 14)}<span>Raster tonen</span><code></code></div>
      <div class="sep"></div>
      <div class="mi dis">{icon("export", 14)}<span>Exporteren</span><code></code></div>
      <div class="mi">{icon("disclosure-collapsed", 14)}<span>Meer</span><code>▸</code></div>
    </div>
  </div>
  <div>
    <div class="lbl">Keuzelijst, open</div>
    <span class="fld sel foc" style="width:180px"><span>Woningbouw</span>{icon("disclosure-expanded", 14)}</span>
    <div class="menu" style="width:180px;margin-top:4px">
      <div class="mi"><span class="sp"></span><span>Leeg project</span></div>
      <div class="mi chk sel"><span class="cm">{icon("check", 14)}</span><span>Woningbouw</span></div>
      <div class="mi hov"><span class="sp"></span><span>Utiliteitsbouw</span></div>
    </div>
  </div>
</div>"""


def rbtn(n, label, cls=""):
    return f'<span class="rbtn {cls}">{icon(n, 24)}<span>{esc(label)}</span></span>'


def rsm(n, label, cls=""):
    return f'<span class="rsm {cls}">{icon(n, 16)}<span>{esc(label)}</span></span>'


ribbon = f"""
<div class="rtabs"><span class="rt file">Bestand</span><span class="rt on">Start</span><span class="rt">Invoegen</span><span class="rt hov">Beeld</span></div>
<div class="ribbon">
  <div class="rgrp"><div class="rbody">{rbtn("save", "Opslaan", "on")}{rbtn("open", "Openen", "hov")}<div class="rstack">{rsm("undo", "Ongedaan")}{rsm("redo", "Opnieuw")}{rsm("duplicate", "Dupliceren", "dis")}</div></div><div class="rlbl">Bestand</div></div>
  <div class="rgrp"><div class="rbody">{rbtn("view.grid", "Raster", "foc")}{rbtn("measure.distance", "Meten")}{rbtn("export", "Export", "dis")}</div><div class="rlbl">Beeld</div></div>
</div>
<div class="doc"><span class="dt on">{esc("Begroting.ocs")}<i class="mod"></i><span class="x">{icon("close", 12)}</span></span><span class="dt hov">Variant B<span class="x">{icon("close", 12)}</span></span><span class="dt">Schoolgebouw<span class="x">{icon("close", 12)}</span></span></div>
"""

panels = f"""
<div class="panels">
  <div class="pnl">
    <div class="ph"><span>Verkenner</span><span class="ib sm">{icon("panelleft", 14)}</span></div>
    <div class="tree">
      <div class="tn">{icon("tree.collapse", 12)}{icon("cube", 14)}<span>Kade 12</span></div>
      <div class="tn l1 sel">{icon("tree.expand", 12)}{icon("grid", 14)}<span>Fundering</span></div>
      <div class="tn l1 hov">{icon("tree.expand", 12)}{icon("grid", 14)}<span>Ruwbouw</span></div>
      <div class="tn l1">{icon("tree.expand", 12)}{icon("grid", 14)}<span>Afbouw</span></div>
    </div>
  </div>
  <div class="pnl">
    <div class="ph"><span>Eigenschappen</span></div>
    <div class="sec">{icon("tree.collapse", 12)}<span>Algemeen</span></div>
    <div class="pr"><span>Naam</span><span class="fld sm"><span>Fundering</span></span></div>
    <div class="pr"><span>Eenheid</span><span class="fld sm sel"><span>m³</span>{icon("disclosure-expanded", 12)}</span></div>
    <div class="pr"><span>Hoeveelheid</span><code class="num">48,50</code></div>
    <div class="pr"><span>Meenemen</span><span class="cbx"><i class="box on">{icon("check", 12)}</i></span></div>
  </div>
</div>"""

table = """
<table class="tbl">
  <tr><th>Code</th><th>Omschrijving</th><th class="r">Hoeveelheid</th><th class="r">Bedrag</th></tr>
  <tr><td><code>21.10</code></td><td>Funderingsbalken</td><td class="r"><code>48,50 m³</code></td><td class="r"><code>€ 12.610</code></td></tr>
  <tr class="sel"><td><code>21.20</code></td><td>Poeren</td><td class="r"><code>12 st</code></td><td class="r"><code>€ 3.480</code></td></tr>
  <tr class="hov"><td><code>22.10</code></td><td>Kanaalplaatvloer</td><td class="r"><code>210,00 m²</code></td><td class="r"><code>€ 18.900</code></td></tr>
  <tr><td><code>23.10</code></td><td>Kalkzandsteen</td><td class="r"><code>340,00 m²</code></td><td class="r"><code>€ 27.200</code></td></tr>
</table>"""


def banner(k, ic, title, text):
    return f'<div class="ban" style="--sc:var(--{k});--st:var(--{k}tint)"><span class="bi">{icon(ic, 16)}</span><span><b>{esc(title)}</b> {esc(text)}</span><span class="ib sm">{icon("close", 12)}</span></div>'


messages = f"""
<div class="stack">
  {banner("error", "status.error", "Fout.", "Het bestand kan niet worden geopend.")}
  {banner("success", "status.success", "Gelukt.", "De begroting is opgeslagen.")}
  {banner("warning", "status.warning", "Let op.", "Twee posten hebben geen eenheid.")}
  {banner("info", "status.info", "Info.", "Er is een nieuwe versie beschikbaar.")}
  <div class="lbl">Melding rechtsonder</div>
  <div class="toast"><span class="bi" style="color:var(--success)">{icon("status.success", 16)}</span><span><b>Opgeslagen</b><br><small>Begroting.ocs · 16:42</small></span><span class="lnk">Openen</span><span class="ib sm">{icon("close", 12)}</span></div>
</div>"""

dialog = f"""
<div class="dlgwrap">
  <div class="dlg">
    <div class="dh"><b>Wijzigingen opslaan?</b><span class="ib sm">{icon("close", 12)}</span></div>
    <div class="db">De begroting <b>Kade 12</b> heeft wijzigingen die nog niet zijn opgeslagen.</div>
    <div class="df"><span class="btn g">Niet opslaan</span><span class="btn s">Annuleren</span><span class="btn p">{icon("save", 16)}Opslaan</span></div>
  </div>
</div>
<div class="empty"><span class="eicon">{icon("open", 32)}</span><b>Geen document geopend</b><span>Open een project of begin een nieuwe begroting.</span><span class="btn p">{icon("new", 16)}Nieuw project</span></div>
"""

# ---------- hover / pressed alternatives (section 1b) ----------
OLD_HOVER = {"light": "#EA580C", "dark": "#EA580C", "blueprint": "#93C5FD"}
PRIMARY_A = {t: (THEMES[t]["color"]["accent-hover"], THEMES[t]["color"]["accent-pressed"]) for t in ("light", "dark", "blueprint")}


def alt_rows(tid):
    th = THEMES[tid]
    c = th["color"]
    v = tvars(th)
    nh, np_ = mix(c["text"], 0.06, c["panel"]), mix(c["text"], 0.12, c["panel"])
    ah, ap = PRIMARY_A[tid]
    eh, ep = mix(c["error"], 0.08, c["raised"]), mix(c["error"], 0.16, c["raised"])
    ring = mix(c["accent"], 0.35, c["panel"])
    inset = "inset 0 2px 0 rgba(0,0,0,.22)"
    base = "display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 12px;border-radius:var(--rm);font-weight:600;border:1px solid transparent;white-space:nowrap"
    P = f"{base};color:{c['text-on-accent']}"
    S = f"{base};color:{c['text']};border-color:{c['border-strong']}"
    G = f"{base};color:{c['text']}"
    D = f"{base};color:{c['error']};border-color:{c['error']}"

    def b(style, txt):
        return f'<span style="{style}">{txt}</span>'

    variants = {
        "Voorheen": [
            (b(f"{P};background:{c['accent']}", "Opslaan"), b(f"{P};background:{OLD_HOVER[tid]}", "Opslaan"), b(f"{P};background:{OLD_HOVER[tid]};box-shadow:{inset}", "Opslaan")),
            (b(f"{S};background:{c['raised']}", "Annuleren"), b(f"{S};background:{c['raised']};border-color:{c['accent']}", "Annuleren"), b(f"{S};background:{v['tint']};border-color:{c['accent']}", "Annuleren")),
            (b(G, "Meer opties"), b(f"{G};background:{nh}", "Meer opties"), b(f"{G};background:{v['tint']}", "Meer opties")),
            (b(f"{D};background:{c['raised']}", "Verwijderen"), b(f"{D};background:{v['errortint']}", "Verwijderen"), b(f"{D};background:{v['errortint']};border-width:2px", "Verwijderen")),
        ],
        "A · Besloten: zelfde kleur, lichter en donkerder": [
            (b(f"{P};background:{c['accent']}", "Opslaan"), b(f"{P};background:{ah}", "Opslaan"), b(f"{P};background:{ap}", "Opslaan")),
            (b(f"{S};background:{c['raised']}", "Annuleren"), b(f"{S};background:{nh}", "Annuleren"), b(f"{S};background:{np_}", "Annuleren")),
            (b(G, "Meer opties"), b(f"{G};background:{nh}", "Meer opties"), b(f"{G};background:{np_}", "Meer opties")),
            (b(f"{D};background:{c['raised']}", "Verwijderen"), b(f"{D};background:{eh}", "Verwijderen"), b(f"{D};background:{ep}", "Verwijderen")),
        ],
        "B · Zelfde vulling, alleen rand of schaduw": [
            (b(f"{P};background:{c['accent']}", "Opslaan"), b(f"{P};background:{c['accent']};box-shadow:0 0 0 3px {ring}", "Opslaan"), b(f"{P};background:{c['accent']};box-shadow:{inset}", "Opslaan")),
            (b(f"{S};background:{c['raised']}", "Annuleren"), b(f"{S};background:{c['raised']};border-color:{c['text']}", "Annuleren"), b(f"{S};background:{c['raised']};border-color:{c['text']};box-shadow:{inset}", "Annuleren")),
            (b(G, "Meer opties"), b(f"{G};background:{nh}", "Meer opties"), b(f"{G};background:{nh};box-shadow:{inset}", "Meer opties")),
            (b(f"{D};background:{c['raised']}", "Verwijderen"), b(f"{D};background:{c['raised']};border-width:2px", "Verwijderen"), b(f"{D};background:{c['raised']};border-width:2px;box-shadow:{inset}", "Verwijderen")),
        ],
    }
    out = []
    for name, rows_ in variants.items():
        body = "".join(f"<tr><th>{esc(k)}</th>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>"
                       for k, r in zip(["Primair", "Secundair", "Stil", "Gevaarlijk"], rows_))
        out.append(f'<div class="alt"><div class="lbl">{esc(name)}</div><table class="st"><tr><th></th><th>Normaal</th><th>Hover</th><th>Ingedrukt</th></tr>{body}</table></div>')
    return f'<figure class="pane" style="{svars(v)}"><div class="alts">{"".join(out)}</div><figcaption><b>{esc(th["name"])}</b></figcaption></figure>'


alt_checks = []
for tid, (ah, ap) in PRIMARY_A.items():
    c = THEMES[tid]["color"]
    alt_checks.append((THEMES[tid]["name"], contrast(c["text-on-accent"], ah), contrast(c["text-on-accent"], ap)))
alt_note = " · ".join(f"{n}: hover {fmt(h)}, ingedrukt {fmt(pr)}" for n, h, pr in alt_checks)
alt_html = "".join(alt_rows(t) for t in ("light", "dark", "blueprint"))


# ---------- ribbon variants (section 7) ----------
def lint(tid, variant, focus=False):
    th = THEMES[tid]
    v = tvars(th)

    def big(n, label, cls=""):
        return f'<span class="big {cls}"><span class="ic">{icon(n, 22)}</span><span>{esc(label)}</span></span>'

    def small(n, label, cls=""):
        return f'<span class="sml {cls}">{icon(n, 16)}<span>{esc(label)}</span></span>'

    return f"""
<figure class="pane lintfig" style="{svars(v)}">
  <div class="lint {variant}">
    <div class="tb"><span class="logo"></span><span class="ttl">Open Calc Studio</span><span class="win">&#8212;&nbsp;&#9633;&nbsp;&#10005;</span></div>
    <div class="tabs"><span class="t file">Bestand</span><span class="t on">Start</span><span class="t">Invoegen</span><span class="t">Beeld</span></div>
    <div class="rb">
      <div class="g"><div class="gb">{big("save", "Opslaan", "on")}{big("open", "Openen", "hov")}<div class="col3">{small("undo", "Ongedaan")}{small("redo", "Opnieuw")}{small("duplicate", "Dupliceren", "dis")}</div></div><div class="gl">Bestand</div></div>
      <div class="g"><div class="gb">{big("view.grid", "Raster", "foc" if focus else "")}{big("measure.distance", "Meten")}{big("export", "Export", "dis")}</div><div class="gl">Beeld</div></div>
    </div>
    <div class="docs"><span class="d on">Begroting.ocs<i class="mod"></i><span class="x">{icon("close", 12)}</span></span><span class="d">Variant B<span class="x">{icon("close", 12)}</span></span><span class="d">Schoolgebouw<span class="x">{icon("close", 12)}</span></span></div>
    <div class="ws"></div>
  </div>
  <figcaption><b>{esc(th["name"])}</b></figcaption>
</figure>"""


lint_sections = "".join(
    f'<div class="lbl" style="margin-top:20px">{esc(title)}</div><div class="pair">{lint("light", key)}{lint("dark", key)}</div>'
    for key, title in [("va", "A · Zoals de Tauri-template, nu"),
                       ("vb", "B · Licht en vlak, naar de website"),
                       ("vc", "C · Donkere kopbalk, zoals de navigatie van de website")])


# ---------- dark banner comparison (section 10b) ----------
DEEP_BG = {"error": "#7F1D1D", "success": "#14532D", "warning": "#78350F", "info": "#1E3A8A"}
MID = {"error": "#DC2626", "success": "#16A34A", "warning": "#CA8A04", "info": "#2563EB"}
BANNERS = [("error", "status.error", "Fout.", "Het bestand kan niet worden geopend."),
           ("success", "status.success", "Gelukt.", "De begroting is opgeslagen."),
           ("warning", "status.warning", "Let op.", "Twee posten hebben geen eenheid."),
           ("info", "status.info", "Info.", "Er is een nieuwe versie beschikbaar.")]


def dark_banners(kind):
    th = THEMES["dark"]
    c = th["color"]
    v = tvars(th)
    rows_ = []
    for k, ic, title, text in BANNERS:
        bg = {"now": mix({"error": "#FCA5A5", "success": "#4ADE80", "warning": "#FACC15", "info": "#93C5FD"}[k], 0.18, c["panel"]),
              "z1": mix(MID[k], 0.20, c["panel"]),
              "z2": mix(MID[k], 0.28, c["panel"]),
              "z3": mix(DEEP_BG[k], 0.50, c["panel"]),
              "deep": DEEP_BG[k]}[kind]
        rows_.append(
            f'<div class="ban" style="--sc:{c[k]};--st:{bg}"><span class="bi">{icon(ic, 16)}</span>'
            f'<span><b>{esc(title)}</b> {esc(text)}</span><span class="ib sm">{icon("close", 12)}</span></div>'
            f'<code class="bm">vlak {bg} · tekst {fmt(contrast(c["text"], bg))}:1 · statuskleur {fmt(contrast(c[k], bg))}:1</code>')
    cap = {"now": "Voorheen · lichte pastelkleur, 18% over het paneel",
           "z1": "Z1 · volle statuskleur, 20% over het paneel",
           "z2": "Z2, besloten · volle statuskleur, 28% over het paneel",
           "z3": "Z3 · diepe Style Book-kleur, 50% met het paneel",
           "deep": "Diep · de donkere achtergronden uit het Style Book"}[kind]
    return f'<figure class="pane" style="{svars(v)}"><div class="stack">{"".join(rows_)}</div><figcaption><b>Donker</b>{esc(cap)}</figcaption></figure>'


dark_banner_html = "".join(dark_banners(k) for k in ("now", "z1", "z2", "z3"))


# ---------- workspace example in Donker (section 11b) ----------
WS_OPTIONS = TOKENS["workspace-setting"]["options"]
DARK_WS = WS_OPTIONS["dark"]["workspace"]


def ws_vars(mode):
    """CSS variables for content inside the workspace."""
    if mode == "light":
        v = tvars(THEMES["light"])
        v["wsbg"] = WS_OPTIONS["light"]["workspace"]
    else:
        v = tvars(THEMES["dark"])
        v["wsbg"] = DARK_WS
        v["raised"] = THEMES["dark"]["color"]["panel"]
    v["gridline"] = mix(v["text"], 0.10, v["wsbg"])
    return v


def doc_table():
    return """<table class="tbl wsdoc">
  <tr><th>Code</th><th>Omschrijving</th><th class="r">Hoeveelheid</th><th class="r">Bedrag</th></tr>
  <tr><td><code>21.10</code></td><td>Funderingsbalken</td><td class="r"><code>48,50 m³</code></td><td class="r"><code>€ 12.610</code></td></tr>
  <tr class="sel"><td><code>21.20</code></td><td>Poeren</td><td class="r"><code>12 st</code></td><td class="r"><code>€ 3.480</code></td></tr>
  <tr><td><code>22.10</code></td><td>Kanaalplaatvloer</td><td class="r"><code>210,00 m²</code></td><td class="r"><code>€ 18.900</code></td></tr>
  <tr><td><code>23.10</code></td><td>Kalkzandsteen</td><td class="r"><code>340,00 m²</code></td><td class="r"><code>€ 27.200</code></td></tr>
</table>"""


def doc_drawing():
    return """<svg class="wsdraw" viewBox="0 0 320 150" aria-hidden="true">
  <rect x="30" y="20" width="200" height="110" fill="none" stroke="var(--text)" stroke-width="2"/>
  <line x1="130" y1="20" x2="130" y2="130" stroke="var(--text)" stroke-width="1.2"/>
  <line x1="30" y1="80" x2="130" y2="80" stroke="var(--text)" stroke-width="1.2"/>
  <rect x="150" y="40" width="60" height="40" fill="var(--tint)" stroke="var(--accent)" stroke-width="2"/>
  <line x1="30" y1="142" x2="230" y2="142" stroke="var(--textsecondary)" stroke-width="1"/>
  <text x="130" y="140" text-anchor="middle" font-size="9" fill="var(--textsecondary)" font-family="JetBrains Mono">8000</text>
  <circle cx="270" cy="60" r="22" fill="none" stroke="var(--info)" stroke-width="1.5" stroke-dasharray="4 3"/>
</svg>"""


def app_dark(mode, doc):
    th = THEMES["dark"]
    v = tvars(th)
    wv = ws_vars(mode)
    title = "Begroting.ocs" if doc == "table" else "Plattegrond.ofs"
    content = doc_table() if doc == "table" else doc_drawing()
    tab_bg = wv["wsbg"]
    tab_fg = wv["text"]
    return f"""
<figure class="pane" style="{svars(v)}">
  <div class="lint vb wsapp">
    <div class="tb"><span class="logo"></span><span class="ttl">Open Calc Studio</span><span class="win">&#8212;&nbsp;&#9633;&nbsp;&#10005;</span></div>
    <div class="tabs"><span class="t file">Bestand</span><span class="t on">Start</span><span class="t">Invoegen</span><span class="t">Beeld</span></div>
    <div class="body">
      <div class="side"><div class="ph"><span>Verkenner</span></div>
        <div class="tn sel">{icon("grid", 14)}<span>Fundering</span></div><div class="tn">{icon("grid", 14)}<span>Ruwbouw</span></div><div class="tn">{icon("grid", 14)}<span>Afbouw</span></div></div>
      <div class="main">
        <div class="docs"><span class="d on" style="background:{tab_bg};color:{tab_fg}">{esc(title)}<span class="x">{icon("close", 12)}</span></span><span class="d">Variant B<span class="x">{icon("close", 12)}</span></span></div>
        <div class="wsarea" style="{svars(wv)};background:var(--wsbg);color:var(--text)">{content}</div>
      </div>
    </div>
  </div>
  <figcaption><b>{"Instelling: Altijd licht" if mode == "light" else "Standaard: volgt het thema"}</b>{"Tabel" if doc == "table" else "Tekening"} in het thema Donker.</figcaption>
</figure>"""



def setting_example(tid):
    th = THEMES[tid]
    v = tvars(th)
    hc = th.get("high-contrast", False)
    return f"""
<figure class="pane" style="{svars(v)}">
  <div class="setcard">
    <div class="sethd">Instellingen</div>
    <div class="setbody">
      <div class="setnav"><div class="tn sel"><span>Weergave</span></div><div class="tn"><span>Taal</span></div><div class="tn"><span>Bestanden</span></div></div>
      <div class="setmain">
        <div class="lbl">Weergave</div>
        <div class="setrow"><span>Thema</span><span class="fld sel"><span>{esc(th["name"])}</span>{icon("disclosure-expanded", 14)}</span></div>
        <div class="setrow" style="position:relative"><span>Werkruimte</span><span class="fld sel {"dis" if hc else "foc"}"><span>Volgt thema</span>{icon("disclosure-expanded", 14)}</span>
        {"" if hc else '<div class="menu" style="position:absolute;left:128px;top:30px;width:200px;z-index:2"><div class="mi chk sel"><span class="cm">' + icon("check", 14) + '</span><span>Volgt thema</span></div><div class="mi hov"><span class="sp"></span><span>Altijd licht</span></div><div class="mi"><span class="sp"></span><span>Altijd donker</span></div></div>'}
        </div>
        <div class="sethelp">Kleur van het vlak waarin je document staat.{" In High contrast bepaalt het thema dit zelf." if hc else ""}</div>
        <div class="setrow"><span>Statusbalk</span><span class="fld sel {"dis" if hc else ""}"><span>Volgt thema</span>{icon("disclosure-expanded", 14)}</span></div>
        <div class="setrow"><span>Navigatie</span><span class="fld sel"><span>Zijbalk</span>{icon("disclosure-expanded", 14)}</span></div>
        <div class="sethelp">Alleen in werkstroom-apps: zijbalk of stappen bovenaan.</div>
      </div>
    </div>
  </div>
  <figcaption><b>{esc(th["name"])}</b></figcaption>
</figure>"""


setting_html = setting_example("dark") + setting_example("high-contrast-dark")

ws_example_html = (
    '<div class="lbl">Begroting als tabel</div><div class="pair">' + app_dark("light", "table") + app_dark("dark", "table") + "</div>"
    + '<div class="lbl" style="margin-top:16px">Tekening</div><div class="pair">' + app_dark("light", "drawing") + app_dark("dark", "drawing") + "</div>")

ws_rows = []
for mode in ("light", "dark"):
    wv = ws_vars(mode)
    for label, fg, bg, need in [("Tekst in werkruimte", "text", "wsbg", 4.5), ("Tabelkop", "textsecondary", "panel", 4.5),
                                ("Lijnen van tekening", "text", "wsbg", 3.0), ("Maatvoering", "textsecondary", "wsbg", 4.5)]:
        r = contrast(wv[fg], wv[bg])
        ws_rows.append(r >= need)
ws_ok = all(ws_rows)


strip = "".join(
    f'<figure class="pane mini" style="{svars(tvars(th))}"><div class="row">{btn("p", "")}{btn("s", "")}</div>'
    f'<div class="row">{field("in", "")}{choice("cb", "")}{choice("sw", "")}</div>'
    f'<div class="lint vb" style="border:0"><div class="tabs" style="padding:0"><span class="t file">Bestand</span><span class="t on">Start</span><span class="t">Beeld</span></div></div>'
    f'<figcaption><b>{esc(th["name"])}</b></figcaption></figure>'
    for th in THEMES.values())

check_table = "".join(
    f"<tr><td>{esc(t)}</td><td>{esc(l)}</td><td><span class=\"sw2\" style=\"background:{fg}\"></span><code>{fg}</code></td>"
    f"<td><span class=\"sw2\" style=\"background:{bg}\"></span><code>{bg}</code></td><td class=\"{'ok' if r >= n else 'bad'}\"><b>{fmt(r)}</b> / {fmt(n)}</td></tr>"
    for t, l, fg, bg, r, n in rows)

ROOTVARS = (f":root{{--rs:{R['small']}px;--rm:{R['medium']}px;--rl:{R['large']}px;--fl:{F['label']}px;--fb:{F['body']}px;"
            f"--fp:{F['panel-heading']}px;--fd:{F['dialog-heading']}px;--fpg:{F['page-heading']}px}}")

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
.facts{display:flex;gap:9px;flex-wrap:wrap}.facts span{background:#fff;border:1px solid #d8d8dd;padding:8px 11px}
figure{margin:0;min-width:0}figcaption{margin-top:10px;font-size:13px;color:var(--textsecondary)}figcaption b{display:block;color:var(--text);font-size:14px}
code{font-family:'JetBrains Mono',monospace;font-size:var(--fl)}
.pair{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(600px,100%),1fr));gap:16px}.pair.stacked{grid-template-columns:minmax(0,1fr)}
.strip{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(260px,100%),1fr));gap:12px}
.tablewrap{overflow-x:auto;overflow-y:hidden;max-width:100%}
.ctab{border-collapse:collapse;background:#fff;width:100%;min-width:640px}.ctab th,.ctab td{border:1px solid #dedee2;padding:6px 9px;text-align:left}.ctab th{background:#f5f5f4}
.ctab td.ok{background:#f0fdf4}.ctab td.bad{background:#fef2f2}.sw2{display:inline-block;width:12px;height:12px;border:1px solid #bbb;vertical-align:-2px;margin-right:6px}
footer{color:#6b6b75;font-size:12px;margin-top:34px}
/* B2 icons: primary part follows currentColor, accent part follows the theme accent */
.pane,.win,.app{--icon-accent:var(--accent)}
.dis .b2,.b2.dis,.dis.b2{--icon-accent:currentColor}
.ban .b2,.bi .b2,.ti .b2,.ban>.b2{--icon-accent:currentColor}


.pane{background:var(--panel);color:var(--text);border:1px solid var(--border);padding:16px;font-size:var(--fb);line-height:1.4;overflow-x:auto}
.pane svg{flex:0 0 auto}
.lbl,.ph span:first-child,.rlbl,.sec span,.tbl th,.st th{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:var(--fl);color:var(--textsecondary);font-weight:400}
.lbl{margin:12px 0 6px}.lbl:first-child{margin-top:0}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px}.row.sm{font-size:var(--fl);color:var(--textsecondary);justify-content:space-between;margin:4px 0 10px}
.note{font-size:var(--fl);color:var(--textsecondary)}
.stack{display:flex;flex-direction:column;gap:8px;max-width:520px}
table.st{border-collapse:separate;border-spacing:8px 6px;margin:0}table.st th{text-align:left;padding:0;white-space:nowrap}table.st td{padding:0}

/* focus + disabled shared */
.foc{box-shadow:0 0 0 2px var(--panel),0 0 0 4px var(--focus)!important}
/* dense areas: focus ring inside the element so it never touches neighbours */
.lint .foc,.rbtn.foc,.rsm.foc,.mi.foc,.tn.foc,.dt.foc,.tbl tr.foc td{box-shadow:inset 0 0 0 2px var(--focus),inset 0 0 0 3px var(--panel)!important}
.dis{color:var(--textdisabled)!important;cursor:default}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 12px;border-radius:var(--rm);font-weight:600;font-size:var(--fb);border:1px solid transparent;white-space:nowrap}
.btn.p{background:var(--accent);color:var(--textonaccent)}.btn.p.hov{background:var(--accenthover)}.btn.p.prs{background:var(--accentpressed)}
.btn.s{background:var(--raised);color:var(--text);border-color:var(--borderstrong)}.btn.s.hov{background:var(--hoverbg);border-color:var(--hoverline,var(--borderstrong))}.btn.s.prs{background:var(--pressedbg)}
.btn.g{background:transparent;color:var(--text)}.btn.g.hov{background:var(--hoverbg);border-color:var(--hoverline)}.btn.g.prs{background:var(--pressedbg);border-color:var(--hoverline)}
.btn.d{background:var(--raised);color:var(--error);border-color:var(--error)}.btn.d.hov{background:var(--dangerhover)}.btn.d.prs{background:var(--dangerpressed)}
.btn.dis{background:transparent;border:1px var(--disline) var(--border)}

/* icon buttons */
.ib{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:var(--rs);color:var(--text);border:1px solid transparent}
.ib.sm{width:20px;height:20px}
.ib.hov{background:var(--hoverbg);border-color:var(--hoverline)}.ib.on{background:var(--tint);border-color:var(--selectedbar);color:var(--accenttext)}

/* fields */
.fld{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 8px;min-width:150px;background:var(--raised);color:var(--text);border:1px solid var(--borderstrong);border-radius:var(--rm)}
.fld.sm{height:24px;min-width:0;width:100%}
.fld .ph{color:var(--textsecondary)}.fld.sel{justify-content:space-between}.fld svg{color:var(--textsecondary)}
.fld.hov{border-color:var(--text)}.fld.prs{border-color:var(--accent)}
.fld.dis{background:var(--panel);border:1px var(--disline) var(--border)}.fld.dis .ph{color:var(--textdisabled)}
.fld.err{border-color:var(--error);border-width:2px}

/* choices */
.cbx{display:inline-flex;align-items:center;gap:8px;padding:2px 4px;border-radius:var(--rs);white-space:nowrap}
.cbx.hov{background:var(--hoverbg)}
.box{width:16px;height:16px;border-radius:var(--rs);border:1.5px solid var(--borderstrong);display:grid;place-items:center;font-style:normal}
.box.on{background:var(--accent);border-color:var(--accent);color:var(--textonaccent)}
.rad{width:16px;height:16px;border-radius:50%;border:1.5px solid var(--borderstrong)}.rad.on{border-color:var(--selectedbar);background:radial-gradient(var(--selectedbar) 0 4px,transparent 4.5px)}
.sw{position:relative;width:32px;height:18px;border-radius:9999px;border:1.5px solid var(--track);font-style:normal}
.sw b{position:absolute;left:2px;top:2px;width:11px;height:11px;border-radius:50%;background:var(--track)}
.sw.on{background:var(--accent);border-color:var(--accent)}.sw.on b{left:16px;background:var(--knob)}
.cbx.dis .box,.cbx.dis .rad,.cbx.dis .sw{border-style:var(--disline);border-color:var(--textdisabled);background:transparent;color:var(--textdisabled)}.cbx.dis .sw b{background:var(--textdisabled)}
.cbx.prs .box,.cbx.prs .rad,.cbx.prs .sw{box-shadow:0 0 0 3px var(--tint)}

/* slider, progress, scroll */
.slider{position:relative;height:4px;border-radius:9999px;background:var(--track);margin:10px 8px 4px}
.slider i{position:absolute;left:0;top:0;bottom:0;border-radius:9999px;background:var(--accent)}
.slider b{position:absolute;top:50%;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--raised);border:2px solid var(--accent)}
.val{color:var(--textsecondary)}
.prog{height:6px;border-radius:9999px;background:var(--border);overflow:hidden;outline:1px solid var(--track);outline-offset:-1px}
.prog i{display:block;height:100%;background:var(--accent);border-radius:9999px}
.prog.busy i{width:30%;margin-left:35%}
.scrollbox{display:flex;height:84px;border:1px solid var(--border);border-radius:var(--rs);background:var(--raised)}
.lines{flex:1;padding:6px 8px;overflow:hidden}.lines p{height:6px;margin:0 0 7px;border-radius:3px;background:var(--border)}
.sbar{width:10px;padding:2px;border-left:1px solid var(--border)}.sbar i{display:block;height:40%;border-radius:9999px;background:var(--track)}

/* popups */
.poprow{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start}
.tipwrap{display:flex;flex-direction:column;align-items:flex-start;gap:4px}
.tip{background:var(--tipbg);color:var(--text);border:1px solid var(--border);box-shadow:var(--shpop);border-radius:var(--rs);padding:4px 8px;font-size:var(--fl);white-space:nowrap}.tip code{color:var(--textsecondary);margin-left:8px}
.menu{background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);box-shadow:var(--shpop);padding:4px;width:220px}
.mi{display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:var(--rs)}.mi span{flex:1}.mi code{color:var(--textsecondary)}
.mi svg{color:var(--textsecondary)}.mi.hov{background:var(--hoverbg);outline:1px solid var(--hoverline)}
.mi.chk svg,.mi.sel{color:var(--accenttext)}.mi.sel{background:var(--tint);font-weight:600}.mi.dis svg{color:var(--textdisabled)}
.mi .sp{flex:0 0 14px}.mi .cm{flex:0 0 14px;display:grid}
.sep{height:1px;background:var(--border);margin:4px 0}

/* ribbon */
.rtabs{display:flex;gap:2px;height:28px;align-items:flex-end;padding:0 8px;border-bottom:1px solid var(--accent)}
.rt{padding:0 16px;height:24px;display:flex;align-items:center;color:var(--textsecondary);font-weight:500;border:1px solid transparent;border-bottom:none;border-radius:var(--rs) var(--rs) 0 0}
.rt.file{background:var(--accent);color:var(--textonaccent);font-weight:600}
.rt.on{color:var(--accenttext);border-color:var(--accent);background:var(--panel);margin-bottom:-1px;height:25px}
.rt.hov{color:var(--text);background:var(--hoverbg)}
.ribbon{display:flex;height:94px;border-bottom:1px solid var(--border);background:var(--panel)}
.rgrp{display:flex;flex-direction:column;padding:4px 8px 0;border-right:1px solid var(--border)}
.rbody{display:flex;gap:2px;flex:1}
.rbtn{display:flex;flex-direction:column;align-items:center;gap:2px;width:56px;height:66px;padding:6px 2px 2px;border-radius:var(--rs);border:1px solid transparent;font-size:var(--fl);text-align:center;line-height:1.2}
.rbtn.hov{background:var(--hoverbg);border-color:var(--hoverline)}.rbtn.on{background:var(--tint);border-color:var(--selectedbar);color:var(--text)}.rbtn.on svg{color:var(--accenttext)}
.rstack{display:flex;flex-direction:column;gap:1px}
.rsm{display:flex;align-items:center;gap:6px;height:22px;padding:0 6px;border-radius:var(--rs);font-size:var(--fl);white-space:nowrap}
.rbtn.dis svg,.rsm.dis svg{color:var(--textdisabled)}
.rlbl{text-align:center;height:18px;line-height:18px}
.doc{display:flex;gap:1px;height:30px;align-items:flex-end;padding:0 4px;background:var(--docbar);border-bottom:1px solid var(--border)}
.dt{display:flex;align-items:center;gap:6px;height:24px;padding:0 4px 0 10px;color:var(--textsecondary);border:1px solid var(--border);border-bottom:none;border-radius:var(--rs) var(--rs) 0 0;font-size:var(--fb)}
.dt.on{background:var(--workspace);color:var(--workspacetext);border-top:2px solid var(--accent)}
.dt.hov{background:var(--hoverbg);color:var(--text)}
.dt .x{display:grid;place-items:center;width:16px;height:16px;border-radius:var(--rs)}
.mod{width:6px;height:6px;border-radius:50%;background:var(--accent)}

/* panels, tree, property grid */
.panels{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(260px,100%),1fr));gap:12px}
.pnl{border:1px solid var(--border);background:var(--panel)}
.ph{display:flex;justify-content:space-between;align-items:center;height:24px;padding:0 4px 0 8px;border-bottom:1px solid var(--border)}
.tn{display:flex;align-items:center;gap:6px;height:24px;padding:0 8px}.tn svg{color:var(--textsecondary)}.tn.l1{padding-left:24px}
.tn.sel{background:var(--tint);box-shadow:inset 3px 0 0 var(--selectedbar)}.tn.sel span{color:var(--text);font-weight:600}.tn.hov{background:var(--hoverbg)}
.sec{display:flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-bottom:1px solid var(--border)}.sec svg{color:var(--textsecondary)}
.pr{display:grid;grid-template-columns:40% 1fr;align-items:center;gap:8px;height:28px;padding:0 8px;border-bottom:1px solid var(--border)}
.pr>span:first-child{color:var(--textsecondary)}.num{text-align:right;color:var(--text)}

/* table */
.tbl{border-collapse:collapse;width:100%;min-width:480px;background:var(--raised);border:1px solid var(--border)}
.tbl th{height:28px;padding:0 10px;text-align:left;border-bottom:1px solid var(--borderstrong);background:var(--panel)}
.tbl td{height:28px;padding:0 10px;border-bottom:1px solid var(--border)}
.tbl .r{text-align:right}.tbl tr.sel td{background:var(--tint)}.tbl tr.sel td:first-child{box-shadow:inset 3px 0 0 var(--selectedbar)}
.tbl tr.hov td{background:var(--hoverbg)}.tbl code{font-size:var(--fb)}

/* messages */
.ban{display:flex;align-items:center;gap:10px;padding:8px 8px 8px 12px;background:var(--st);border-left:3px solid var(--sc);border-radius:var(--rs);outline:1px solid var(--st)}
.ban .bi{color:var(--sc);display:grid}.ban span:nth-child(2){flex:1}
.toast{display:flex;align-items:center;gap:10px;padding:10px 10px 10px 12px;background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);box-shadow:var(--shpop);max-width:360px}
.bm{display:block;margin:-4px 0 4px 3px;color:var(--textsecondary)}
.toast span:nth-child(2){flex:1}.toast small{color:var(--textsecondary)}.toast .bi{display:grid}
.lnk{color:var(--accenttext);font-weight:600;text-decoration:underline}

/* dialog + empty */
.dlgwrap{background:var(--overlay);padding:24px;display:flex;justify-content:center;margin-bottom:16px}
.dlg{width:420px;max-width:100%;background:var(--raised);border:1px solid var(--border);border-radius:var(--rl);box-shadow:var(--shdlg);overflow:hidden}
.dh{display:flex;justify-content:space-between;align-items:center;padding:12px 12px 8px 20px}.dh b{font:700 var(--fd)/1.2 'Space Grotesk',Inter,sans-serif}
.db{padding:4px 20px 16px}
.df{display:flex;justify-content:flex-end;gap:8px;padding:12px 20px;border-top:1px solid var(--border)}
.df .btn.g{margin-right:auto}
.empty{display:flex;flex-direction:column;align-items:center;gap:6px;padding:28px;background:var(--panel);color:var(--text);border:1px dashed var(--border);text-align:center}
.empty span:not(.btn):not(.eicon){color:var(--textsecondary)}
.empty .eicon{color:var(--accenttext);margin-bottom:4px}.empty b{font-size:var(--fp)}.empty span:not(.btn):not(.eicon){font-size:var(--fb)}
.empty .btn{margin-top:8px}
.mini .row{margin-bottom:10px}
.setcard{border:1px solid var(--border);border-radius:var(--rl);background:var(--raised);overflow:hidden;box-shadow:var(--shdlg)}
.sethd{padding:10px 16px;font:700 var(--fd)/1.2 'Space Grotesk',Inter,sans-serif;border-bottom:1px solid var(--border)}
.setbody{display:flex;min-height:200px}
.setnav{width:120px;border-right:1px solid var(--border);padding:6px 0;background:var(--panel)}
.setmain{flex:1;padding:6px 16px 14px;min-width:0}
.setrow{display:grid;grid-template-columns:120px 1fr;align-items:center;gap:8px;margin:6px 0}
.setrow .fld{min-width:0}
.sethelp{margin-left:128px;font-size:var(--fl);color:var(--textsecondary)}
@media (max-width:640px){.setnav{display:none}.setrow{grid-template-columns:1fr}.sethelp,.setmain .menu{margin-left:0!important}}

.wsapp .body{display:flex;height:210px}
.wsapp .side{width:26%;background:var(--panel);border-right:1px solid var(--border)}
.wsapp .main{flex:1;display:flex;flex-direction:column;min-width:0}
.wsapp .docs{flex:0 0 30px}
.wsapp .d.on{font-weight:600}
.wsarea{flex:1;padding:12px;overflow:hidden}
.wsarea .tbl{min-width:0}
.wsdraw{width:100%;height:100%;display:block;background-image:linear-gradient(var(--gridline) 1px,transparent 1px),linear-gradient(90deg,var(--gridline) 1px,transparent 1px);background-size:16px 16px}

/* ribbon variants */
.lintfig{padding:12px}
.lint{font-size:var(--fb);border:1px solid var(--border);overflow:hidden;color:var(--text)}
.lint .tb{height:32px;display:flex;align-items:center;gap:8px;padding:0 10px;background:var(--panel);border-bottom:1px solid var(--border)}
.lint .logo{width:14px;height:14px;border-radius:3px;background:var(--accent)}
.lint .ttl{flex:1;text-align:center;font-weight:600;color:var(--accenttext)}
.lint .win{color:var(--textsecondary);font-size:11px}
.lint .tabs{height:28px;display:flex;align-items:flex-end;gap:2px;padding:0 8px;background:var(--panel)}
.lint .rb{height:94px;display:flex;background:var(--panel);border-bottom:1px solid var(--border)}
.lint .g{display:flex;flex-direction:column;padding:4px 8px 0;border-right:1px solid var(--border)}
.lint .gb{display:flex;gap:2px;flex:1}
.lint .gl{height:18px;line-height:18px;text-align:center;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:var(--fl);color:var(--textsecondary)}
.lint .big{display:flex;flex-direction:column;align-items:center;gap:3px;width:56px;height:66px;padding-top:5px;font-size:var(--fl);border:1px solid transparent}
.lint .ic{display:grid;place-items:center;width:32px;height:32px}
.lint .col3{display:flex;flex-direction:column;gap:1px}
.lint .sml{display:flex;align-items:center;gap:6px;height:22px;padding:0 6px;font-size:var(--fl);white-space:nowrap;border-radius:var(--rs)}
.lint .dis,.lint .dis svg{color:var(--textdisabled)}
.lint .docs{height:30px;display:flex;align-items:flex-end;gap:2px;padding:0 4px;background:var(--docbar);border-bottom:1px solid var(--border)}
.lint .d{display:flex;align-items:center;gap:6px;height:24px;padding:0 4px 0 10px;color:var(--textsecondary);white-space:nowrap}
.lint .d .x{display:grid;place-items:center;width:16px;height:16px}
.lint .ws{height:40px;background:var(--workspace)}

/* A: template */
.va .tabs{border-bottom:1px solid var(--accent)}
.va .t{display:flex;align-items:center;height:24px;padding:0 14px;color:var(--textsecondary);font-weight:500;border:1px solid transparent;border-bottom:none;border-radius:var(--rs) var(--rs) 0 0}
.va .t.file{background:var(--accent);color:var(--textonaccent);font-weight:600}
.va .t.on{color:var(--accenttext);border-color:var(--accent);background:var(--panel);height:25px;margin-bottom:-1px}
.va .big{border-radius:var(--rs)}.va .big.on{background:var(--tint);border-color:var(--selectedbar)}.va .big.on svg{color:var(--accenttext)}.va .big.hov{background:var(--hoverbg)}
.va .d{border:1px solid var(--border);border-bottom:none;border-radius:var(--rs) var(--rs) 0 0}.va .d.on{background:var(--workspace);color:var(--workspacetext);border-top:2px solid var(--accent)}

/* B: light and flat */
.vb .tabs,.vc .tabs{align-items:stretch;border-bottom:1px solid var(--border)}
.vb .t,.vc .t{display:flex;align-items:center;padding:0 12px;color:var(--textsecondary);font-weight:500;border-bottom:2px solid transparent}
.vb .t.on{color:var(--text);font-weight:600;border-bottom-color:var(--accent)}
.vb .t.file,.vc .t.file{align-self:center;height:22px;margin-right:8px;border-radius:var(--rm);background:var(--accent);color:var(--textonaccent);font-weight:600;border:0}
.vb .g,.vc .g{border-right:0;position:relative}
.vb .g:after,.vc .g:after{content:"";position:absolute;right:0;top:10px;bottom:10px;width:1px;background:var(--border)}
.vb .big,.vc .big{border-radius:var(--rm)}
.vb .big .ic,.vc .big .ic{border-radius:var(--rm);border:1px solid transparent}
.vb .big.on .ic,.vc .big.on .ic{background:var(--tint);border-color:var(--tintline);color:var(--accenttext)}
.vb .big.hov,.vc .big.hov{background:var(--hoverbg)}
.vb .docs,.vc .docs{gap:4px}
.vb .d,.vc .d{border-radius:var(--rm) var(--rm) 0 0}
.vb .d.on,.vc .d.on{background:var(--workspace);color:var(--workspacetext);font-weight:600}

/* C: dark header band */
.vc .tb,.vc .tabs{background:var(--band);border-color:transparent}
.vc .ttl{color:var(--bandtext)}.vc .win{color:var(--bandmuted)}
.vc .t{color:var(--bandmuted)}
.vc .t.on{color:var(--bandaccent);font-weight:600;border-bottom-color:var(--accent)}
.vc .tabs{border-bottom:0}

.alts{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(360px,100%),1fr));gap:16px}
@media (max-width:640px){table.st{font-size:11px}}
"""

page = f"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · componenten 0.4</title>
<style>{ROOTVARS}{CSS}</style>
<header>
  <a href="README.md">Fase 2: ontwerp 0.4</a>
  <h1>Componenten · besloten</h1>
  <p>Stap 2.4. Alle bedieningselementen in hun toestanden, gemaakt uit <code>tokens-0.4.json</code>. De maten en regels staan in <a href="04-componenten.md">04-componenten.md</a>.</p>
</header>
<main>{SPRITE_MARK}
  <div class="facts"><span>23 componenten</span><span>{len(THEMES)} thema's</span><span>{len(rows)} contrastparen</span><span>{'Alle paren halen hun minimum' if not problems else str(len(problems)) + ' paren te laag'}</span></div>

  <h2>1. Knoppen</h2>
  <div class="q">Vier soorten. <b>Primair</b> voor de hoofdactie, maximaal één per scherm of dialoog. Hover maakt de kleur iets lichter, ingedrukt iets donkerder. <b>Secundair</b> voor andere acties. <b>Stil</b> voor minder belangrijke acties. <b>Gevaarlijk</b> voor verwijderen en andere onomkeerbare acties. Hoogte 28 px, hoek 6 px, tekst 12 px halfvet.</div>
  {pair(f'<div class="tablewrap">{btn_table}</div>', stacked=True)}

  <h2>1b. Hover en ingedrukt: besloten variant A</h2>
  <div class="q"><b>Besloten: variant A.</b> De knoppen in sectie 1 gebruiken deze kleuren al. Ter vergelijking staan hieronder de vorige versie en variant B. De vorige versie sprong bij hover naar Signal Orange en gebruikt bij ingedrukt een perzikkleurige tint. Dat past niet bij de rustige thema's. <b>A</b> houdt dezelfde kleur aan, iets lichter bij hover en iets donkerder bij ingedrukt. Neutrale knoppen worden grijs in plaats van perzik. De website doet dit al bij de Feedback-knop. <b>B</b> laat de vulling gelijk en verandert alleen de rand of een schaduw. Contrast van de tekst op de primaire knop in A: {alt_note}.</div>
  <div class="pair stacked">{alt_html}</div>

  <h2>2. Icoonknoppen</h2>
  <div class="q">Voor werkbalken en paneelkoppen. 28 × 28 px, of 20 × 20 px in een paneelkop. Een icoonknop die aan of uit staat, zoals een paneel tonen, krijgt in de aan-stand de accenttint en een rand. Elke icoonknop heeft een tooltip.</div>
  {pair(iconbtns)}

  <h2>3. Invoervelden en keuzelijsten</h2>
  <div class="q">Hoogte 28 px, of 24 px in het eigenschappenraster. Rand in <code>border-strong</code>, zodat het veld goed te zien is. Hulptekst in <code>text-secondary</code>. Een fout geeft een rode rand van 2 px en een melding onder het veld.</div>
  {pair(f'<div class="tablewrap">{fld_table}</div><div class="row" style="margin-top:12px"><span class="fld err"><span>-12</span></span><span style="color:var(--error);font-size:var(--fl)">Hoeveelheid moet positief zijn</span></div>', stacked=True)}

  <h2>4. Checkbox, keuzerondje en schakelaar</h2>
  <div class="q">Checkbox en keuzerondje zijn 16 px. Aan is amber met een vinkje of een gevulde stip. De schakelaar is 32 × 18 px en gebruik je voor iets dat direct werkt, zoals een raster tonen. Een checkbox gebruik je in formulieren die je nog bevestigt.</div>
  {pair(f'<div class="tablewrap">{state_table(choice)([("cb", "Checkbox aan"), ("cb0", "Checkbox uit"), ("rd", "Keuzerondje"), ("sw", "Schakelaar aan"), ("sw0", "Schakelaar uit")])}</div>', stacked=True)}

  <h2>5. Slider, voortgang en scrollbalk</h2>
  <div class="q">De slider heeft een spoor van 4 px en een knop van 14 px, met de waarde in mono ernaast. De voortgangsbalk is 6 px. Bij onbekende duur loopt een blokje heen en weer. De scrollbalk is 10 px breed met een ronde greep.</div>
  {pair(extra)}

  <h2>6. Tooltip en menu</h2>
  <div class="q">Een tooltip verschijnt na een halve seconde, met de sneltoets in mono. Menu's en open keuzelijsten hebben de pop-upschaduw en een hoek van 10 px, met regels van 28 px. Een vinkje toont wat aan staat.</div>
  {pair(popups)}

  <h2>7. Lint en documenttabs: besloten variant B</h2>
  <div class="q"><b>Besloten: variant B</b>, licht en vlak, naar de website. Ter vergelijking staan A en C er nog bij. De maten blijven gelijk aan de Tauri-template: titelbalk 32 px, linttabs 28 px, lint 94 px en documenttabs 30 px. Alleen de vormgeving verschilt.
  <ul style="margin:6px 0 0;padding-left:18px">
  <li><b>A</b> is de template: tabs en knoppen met kaders.</li>
  <li><b>B, besloten</b>, volgt de website: tabs als tekst met een amberkleurige streep, Bestand als afgeronde knop zoals de Feedback-knop, een actieve knop als icoontegel en documenttabs zonder kaders.</li>
  <li><b>C</b> is B met een donkere kopbalk, zoals de navigatiebalk van de website.</li>
  </ul>
  In elk voorbeeld staat Opslaan aan, staat de muis op Openen en zijn Export en Dupliceren uitgeschakeld.</div>
  {lint_sections}
  <div class="lbl" style="margin-top:24px">Variant B met focus</div>
  <div class="pair">{lint("light", "vb", True)}{lint("dark", "vb", True)}</div>
  <div class="row sm" style="margin-top:6px">De knop Raster toont de focusring, voor wie met het toetsenbord werkt. In het lint staat de ring binnen de knop, zodat hij nergens tegenaan komt.</div>

  <h2>8. Panelen, boomstructuur en eigenschappenraster</h2>
  <div class="q">Paneelkop 24 px met een mono-label. De boomstructuur heeft regels van 24 px en 16 px inspringing per niveau. Het eigenschappenraster heeft regels van 28 px, met labels in 40% van de breedte en compacte velden van 24 px. Getallen staan in mono, rechts uitgelijnd.</div>
  {pair(panels)}

  <h2>9. Tabel</h2>
  <div class="q">Kop van 28 px in mono hoofdletters, met een sterkere lijn eronder. Regels van 28 px. Codes en getallen in mono, bedragen rechts uitgelijnd. Een geselecteerde regel krijgt de tint en een streep links. Geen zebrastrepen.</div>
  {pair('<div class="tablewrap">' + table + '</div>')}

  <h2>10. Meldingen</h2>
  <div class="q">Een <b>melding in de pagina</b> heeft de lichte tint van de statuskleur, een streep links en een icoon. Een <b>melding rechtsonder</b> verdwijnt na vijf seconden, behalve bij een fout. Kleur is nooit het enige signaal: er staat altijd een icoon en een woord bij.</div>
  {pair(messages)}

  <h2>10b. Meldingen in Donker: besloten Z2</h2>
  <div class="q"><b>Besloten: Z2.</b> De meldingen in sectie 10 gebruiken deze tint al, ook in Blueprint. De vorige tint was te licht. Dat komt doordat een lichte pastelkleur, zoals <code>#FCA5A5</code>, met het grijze paneel wordt gemengd. Dat geeft een lichte, grauwe waas. De drie varianten mengen een vollere, donkerdere kleur. Daardoor worden de vlakken donkerder en duidelijker gekleurd, zonder fel te worden. Tekst en statuskleur halen in alle varianten de norm.</div>
  <div class="pair">{dark_banner_html}</div>

  <h2>11. Dialoog en lege staat</h2>
  <div class="q">Een dialoog is 420 of 560 px breed, met de dialoogschaduw en een gedimde achtergrond. De titel staat in Space Grotesk 16 px. De primaire knop staat rechts, een stille knop als "Niet opslaan" links. Escape sluit de dialoog. Een lege staat legt uit wat er ontbreekt en biedt één actie. Hij volgt de kleuren van het thema, dus in Donker een donker vlak in plaats van wit.</div>
  {pair(dialog)}

  <h2>11b. Werkruimte: volgt het thema, met een instelling</h2>
  <div class="q"><b>Besloten.</b> De werkruimte volgt standaard het gekozen thema. In Donker is hij dus donker, <code>#26262D</code>, iets dieper dan de panelen. Wie liever een lichte werkruimte heeft, kiest in de instellingen bij Werkruimte voor Altijd licht. Andersom kan ook. Hieronder links de instelling Altijd licht en rechts de standaard. {"Alle tekst en lijnen halen de norm." if ws_ok else "Niet alle tekst haalt de norm."}</div>
  {ws_example_html}
  <div class="lbl" style="margin-top:16px">De instelling in het instellingenvenster</div>
  <div class="pair">{setting_html}</div>

  <h2>12. Alle thema's</h2>
  <p>De belangrijkste componenten naast elkaar in de vijf thema's.</p>
  <div class="strip">{strip}</div>

  <h2>13. Contrast van de componenten</h2>
  <p>Gemeten per thema. Tekst moet 4,5:1 halen, in High contrast 7:1. Randen, sporen en vulling moeten 3:1 halen.</p>
  <div class="tablewrap"><table class="ctab"><tr><th>Thema</th><th>Onderdeel</th><th>Kleur</th><th>Op</th><th>Verhouding / minimum</th></tr>{check_table}</table></div>

  <footer>Gegenereerd door <code>scripts/build_componenten_review.py</code> uit <code>design/ontwerp-0.4/tokens-0.4.json</code>. Iconen uit <code>crates/openaec-ui/assets/icons</code>.</footer>
</main>
</html>
"""

page = page.replace(SPRITE_MARK, sprite(), 1)
OUT.write_text(page, encoding="utf-8")
for p in problems:
    print("TE LAAG  " + p)
print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} component contrast pairs, {len(problems)} too low; {usage()}")
