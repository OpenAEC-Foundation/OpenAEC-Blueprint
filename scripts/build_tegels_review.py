#!/usr/bin/env python3
"""Build the tiles-and-cards review page (step 2.3) from the UI 0.4 tokens.

Writes design/ontwerp-0.4/tegels-review.html. Every colour, radius and size comes
from design/ontwerp-0.4/tokens-0.4.json; derived tile colours are mixes of tokens.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import contrast, mix  # noqa: E402

TOKENS = json.loads((ROOT / "design/ontwerp-0.4/tokens-0.4.json").read_text(encoding="utf-8"))
OUT = ROOT / "design/ontwerp-0.4/tegels-review.html"
ICON_DIR = ROOT / "crates/openaec-ui/assets/icons"
R = TOKENS["radius"]
F = TOKENS["font"]["size"]


def esc(s):
    return html.escape(str(s))


def fmt(r):
    return f"{r:.2f}".replace(".", ",")


def icon(name, size=20):
    svg = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    svg = svg.replace('stroke="#000"', 'stroke="currentColor"').replace('fill="#000"', 'fill="currentColor"')
    return re.sub(r"<svg ", f'<svg width="{size}" height="{size}" aria-hidden="true" ', svg, count=1)


# ---------- derived tile colours ----------
def tile_vars(th):
    c = th["color"]
    hc = th.get("high-contrast", False)
    v = {
        "frame": c["frame"], "panel": c["panel"], "raised": c["raised"], "text": c["text"], "text2": c["text-secondary"],
        "dis": c["text-disabled"], "border": c["border"], "bstrong": c["border-strong"], "accent": c["accent"],
        "acchover": c["accent-hover"], "acctext": c["accent-text"], "onacc": c["text-on-accent"], "focus": c["focus"],
        "sel": c["selected"], "selbar": c["selected-bar"], "statusbar": c["statusbar"], "statustext": c["statusbar-text"],
        "success": c["success"], "warning": c["warning"], "info": c["info"], "error": c["error"],
        "tilebg": c["panel"] if hc else c["selected"],
        "tileborder": c["accent"] if hc else mix(c["accent"], 0.35, c["raised"]),
        "hoverw": "2px" if hc else "1px",
        "pressring": f"inset 0 0 0 2px {c['accent']}" if hc else "none",
        "shadow": th["shadow"]["panel"],
        "disline": "dashed" if th["disabled-style"] == "dashed" else "solid",
        "selout": "outline" if th["selection-style"] == "outline" else "tint",
        "thumb": c["workspace"],
        "thumbline": mix(c["workspace-text"], 0.12, c["workspace"]),
    }
    return v


def style_vars(v):
    return ";".join(f"--{k}:{val}" for k, val in v.items())


# ---------- contrast checks for tiles ----------
CHECKS = [
    ("Titel van tegel", "text", "raised", 4.5),
    ("Omschrijving", "text2", "raised", 4.5),
    ("Icoon in icoontegel", "acctext", "tilebg", 3.0),
    ("Rand bij hover", "accent", "raised", 3.0),
    ("Titel bij ingedrukt", "text", "sel", 4.5),
    ("Omschrijving bij ingedrukt", "text2", "sel", 4.5),
    ("Rand van gekozen keuzetegel", "selbar", "raised", 3.0),
    ("Focusring", "focus", "frame", 3.0),
    ("Metadata op kaart (mono)", "text2", "raised", 4.5),
]
check_rows, problems = [], []
for tid, th in TOKENS["themes"].items():
    v = tile_vars(th)
    hc = th.get("high-contrast", False)
    for label, fg, bg, need in CHECKS:
        need_eff = 7.0 if hc and need == 4.5 else need
        r = contrast(v[fg], v[bg])
        check_rows.append((th["name"], label, v[fg], v[bg], r, need_eff))
        if r < need_eff:
            problems.append(f"{th['name']}: {label} {fmt(r)} < {fmt(need_eff)}")


# ---------- building blocks ----------
TASKS = [("new", "Nieuw", "Begin een nieuwe begroting"), ("open", "Openen", "Open een bestaand project"),
         ("saveas", "Opslaan als", "Sla een kopie op onder een andere naam"), ("export", "Exporteren", "Naar PDF, Excel of IFC"),
         ("print", "Afdrukken", "Druk de begroting af")]


def task_b(ic, title, desc, state=""):
    return f'<div class="task b {state}"><span class="ico">{icon(ic, 22)}</span><span class="tt"><b>{esc(title)}</b><small>{esc(desc)}</small></span></div>'


def task_a(title, desc, state=""):
    return f'<div class="task a {state}"><span class="tt"><b>{esc(title)}</b><small>{esc(desc)}</small></span></div>'


def task_c(ic, title, state=""):
    return f'<div class="task c {state}"><span class="ico">{icon(ic, 22)}</span><b>{esc(title)}</b></div>'


def backstage(tid):
    th = TOKENS["themes"][tid]
    v = tile_vars(th)
    nav = [("back", "Terug", ""), ("new", "Nieuw", ""), ("open", "Openen", "on"), ("save", "Opslaan", ""), ("saveas", "Opslaan als", ""),
           ("export", "Exporteren", ""), ("print", "Afdrukken", ""), ("settings", "Instellingen", ""), ("help", "Over", "")]
    items = "".join(f'<div class="nav {cls}">{icon(ic, 18)}<span>{esc(t)}</span></div>' for ic, t, cls in nav)
    tasks = "".join(task_b(*t) for t in TASKS[:2]) + task_b("import", "Importeren", "Lees een CSV- of IFC-bestand in", "dis")
    recent = "".join(
        f'<div class="rrow">{icon("grid", 18)}<span class="rn"><b>{n}</b><small>{p}</small></span><code>{d}</code></div>'
        for n, p, d in [("Begroting Kade 12.ocs", "D:/Projecten/Kade 12", "16-10-2026"),
                        ("Variant B.ocs", "D:/Projecten/Kade 12", "14-10-2026"),
                        ("Schoolgebouw.ocs", "D:/Projecten/School", "02-10-2026")])
    return f"""
<figure class="win" style="{style_vars(v)}">
  <div class="bs">
    <div class="bsnav">{items}</div>
    <div class="bscontent">
      <h4 class="ph">Openen</h4>
      <div class="mono">Taken</div>
      <div class="col">{tasks}</div>
      <div class="mono">Recent</div>
      <div class="list">{recent}</div>
    </div>
  </div>
  <figcaption><b>Bestand-menu · {esc(th['name'])}</b>Navigatie links, taaktegels en recente bestanden rechts.</figcaption>
</figure>"""


def variant_block(tid, kind):
    th = TOKENS["themes"][tid]
    v = tile_vars(th)
    if kind == "a":
        inner = "".join(task_a(t, d) for _, t, d in TASKS[:3])
        cap = "A · Zonder icoon, getinte achtergrond. Zoals het prototype nu."
    elif kind == "b":
        inner = "".join(task_b(*t) for t in TASKS[:3])
        cap = "B · Icoontegel links, rand. Zoals de Tauri-template en de website."
    else:
        inner = '<div class="grid3">' + "".join(task_c(i, t) for i, t, _ in TASKS) + "</div>"
        cap = "C · Grote tegels in een raster, icoon boven."
    return f'<figure class="pane" style="{style_vars(v)}"><div class="col">{inner}</div><figcaption><b>{esc(th["name"])}</b>{esc(cap)}</figcaption></figure>'


def states_block(tid):
    th = TOKENS["themes"][tid]
    v = tile_vars(th)
    rows = [("", "Normaal"), ("hover", "Hover"), ("press", "Ingedrukt"), ("focus", "Focus met toetsenbord"), ("dis", "Uitgeschakeld")]
    inner = "".join(f'<div class="srow"><span class="sl">{esc(lbl)}</span>{task_b("open", "Openen", "Open een bestaand project", st)}</div>' for st, lbl in rows)
    return f'<figure class="pane" style="{style_vars(v)}"><div class="col">{inner}</div><figcaption><b>{esc(th["name"])}</b></figcaption></figure>'


def project_card(name, meta, status, kind, state=""):
    pill = {"succes": "success", "let op": "warning", "concept": "info"}[kind]
    return f"""<div class="pcard {state}">
  <div class="thumb"><i></i></div>
  <div class="pbody"><b>{esc(name)}</b><code>{esc(meta)}</code><span class="pill" style="--pc:var(--{pill})">{esc(status)}</span></div>
</div>"""


def start_block(tid):
    th = TOKENS["themes"][tid]
    v = tile_vars(th)
    cards = (project_card("Kade 12", "16-10-2026 · 91 posten", "Gereed", "succes")
             + project_card("Schoolgebouw", "02-10-2026 · 240 posten", "Controle", "let op", "hover")
             + project_card("Brug Noord", "28-09-2026 · 12 posten", "Concept", "concept"))
    choices = "".join(
        f'<div class="choice {cls}"><span class="radio"></span><span class="ico">{icon(ic, 22)}</span><b>{esc(t)}</b><small>{esc(d)}</small></div>'
        for ic, t, d, cls in [("new", "Leeg project", "Begin zonder posten", ""),
                              ("grid", "Woningbouw", "Standaard begroting voor een woning", "chosen"),
                              ("cube", "Utiliteitsbouw", "Kantoor, school of zorg", "")])
    return f"""
<figure class="pane wide" style="{style_vars(v)}">
  <h4 class="ph">Welkom bij Open Calc Studio</h4>
  <div class="mono">Recente projecten</div>
  <div class="cards">{cards}</div>
  <div class="mono">Nieuw project vanaf sjabloon</div>
  <div class="cards">{choices}</div>
  <figcaption><b>Startscherm · {esc(th['name'])}</b>Projectkaarten en keuzetegels. De middelste projectkaart toont de hover, de middelste keuzetegel is gekozen.</figcaption>
</figure>"""


def info_block(tid):
    th = TOKENS["themes"][tid]
    v = tile_vars(th)
    stats = "".join(f'<div class="stat"><b>{n}</b><span class="mono">{esc(l)}</span></div>'
                    for n, l in [("91", "Posten"), ("€ 1,2 mln", "Totaal"), ("3", "Waarschuwingen")])
    return f"""
<figure class="pane wide" style="{style_vars(v)}">
  <div class="infowrap">
    <div class="icard"><div class="mono ih">Over deze app</div>
      <div class="irow"><span>Versie</span><code>0.4.0</code></div>
      <div class="irow"><span>Licentie</span><span>LGPL-3.0</span></div>
      <div class="irow"><span>Uitgever</span><span>OpenAEC Foundation</span></div>
    </div>
    <div class="stats">{stats}</div>
  </div>
  <figcaption><b>Infokaart en cijfertegels · {esc(th['name'])}</b>Geen hover, want ze zijn niet klikbaar.</figcaption>
</figure>"""


# ---------- page ----------
themes = list(TOKENS["themes"])
check_table = "".join(
    f"<tr><td>{esc(t)}</td><td>{esc(l)}</td><td><span class=\"sw\" style=\"background:{fg}\"></span><code>{fg}</code></td>"
    f"<td><span class=\"sw\" style=\"background:{bg}\"></span><code>{bg}</code></td><td class=\"{'ok' if r >= n else 'bad'}\"><b>{fmt(r)}</b> / {fmt(n)}</td></tr>"
    for t, l, fg, bg, r, n in check_rows)

CSS = f"""
@font-face{{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf');font-weight:400}}
@font-face{{font-family:Inter;src:url('../../assets/fonts/Inter-Medium.ttf');font-weight:500}}
@font-face{{font-family:Inter;src:url('../../assets/fonts/Inter-SemiBold.ttf');font-weight:600 800}}
@font-face{{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Medium.ttf');font-weight:500}}
@font-face{{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}}
@font-face{{font-family:'JetBrains Mono';src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}}
*{{box-sizing:border-box}}
body{{margin:0;background:#f3f3f2;color:#303039;font:14px/1.5 Inter,system-ui,sans-serif}}
header{{background:#303039;color:#fff;padding:26px max(22px,calc((100vw - 1420px)/2));border-bottom:3px solid #dc7900}}
header a{{color:#ffc180}}header p{{margin:0;color:#dddde3;max-width:1000px}}
h1{{font:700 29px/1.2 'Space Grotesk',Inter,system-ui,sans-serif;margin:8px 0}}
h2{{font:500 22px/1.3 'Space Grotesk',Inter,system-ui,sans-serif;margin:40px 0 6px}}
main{{max-width:1460px;margin:auto;padding:23px 22px 46px}}p{{max-width:980px}}
.q{{background:#fff;border-left:3px solid #dc7900;padding:12px 16px;max-width:1000px;margin:12px 0 16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(380px,100%),1fr));gap:16px}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(560px,100%),1fr));gap:16px}}
figure{{margin:0;min-width:0}}
figcaption{{margin-top:8px;font-size:13px;color:#55555f}}figcaption b{{display:block;color:#303039;font-size:14px}}
code{{font-family:'JetBrains Mono',monospace;font-size:11px}}
table{{border-collapse:collapse;background:#fff;width:100%;min-width:640px}}th,td{{border:1px solid #dedee2;padding:6px 9px;text-align:left}}th{{background:#f5f5f4}}
td.ok{{background:#f0fdf4}}td.bad{{background:#fef2f2}}.tablewrap{{overflow-x:auto}}
.sw{{display:inline-block;width:12px;height:12px;border:1px solid #bbb;vertical-align:-2px;margin-right:6px}}
.facts{{display:flex;gap:9px;flex-wrap:wrap}}.facts span{{background:#fff;border:1px solid #d8d8dd;padding:8px 11px}}
footer{{color:#6b6b75;font-size:12px;margin-top:34px}}

/* themed panes */
.pane,.win{{background:var(--frame);color:var(--text);padding:16px;border:1px solid var(--border);font-size:{F['body']}px;line-height:1.4}}
.pane figcaption,.win figcaption{{color:var(--text2)}}.pane figcaption b,.win figcaption b{{color:var(--text)}}
.mono{{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:{F['label']}px;color:var(--text2);margin:16px 0 8px}}
.ph{{font:700 {F['page-heading']}px/1.2 'Space Grotesk',Inter,sans-serif;letter-spacing:-.02em;margin:0 0 4px;color:var(--text)}}
.col{{display:flex;flex-direction:column;gap:8px;max-width:620px}}

/* icon tile */
.ico{{flex:0 0 40px;width:40px;height:40px;border-radius:{R['medium']}px;background:var(--tilebg);border:1px solid var(--tileborder);color:var(--acctext);display:grid;place-items:center}}

/* task tiles */
.task{{border-radius:{R['large']}px;cursor:default}}
.task .tt{{display:flex;flex-direction:column;gap:2px;min-width:0}}
.task .tt b{{font-size:{F['panel-heading']}px;font-weight:600;color:var(--text)}}
.task .tt small{{font-size:{F['body']}px;color:var(--text2)}}
.task.b{{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--raised);border:1px solid var(--border)}}
.task.a{{padding:12px 16px;background:var(--tilebg);border:1px solid var(--tileborder)}}
.task.c{{display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 8px;background:var(--raised);border:1px solid var(--border);text-align:center}}
.task.c b{{font-size:{F['body']}px;font-weight:600}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:8px}}
.task.hover{{border:var(--hoverw) solid var(--accent)}}
.task.press{{background:var(--sel);border-color:var(--accent);box-shadow:var(--pressring)}}
.task.focus{{box-shadow:0 0 0 2px var(--frame),0 0 0 4px var(--focus)}}
.task.dis .tt b,.task.dis .tt small{{color:var(--dis)}}
.task.dis{{border-style:var(--disline)}}
.task.dis .ico{{background:transparent;border:1px var(--disline) var(--border);color:var(--dis)}}
.srow{{display:grid;grid-template-columns:120px 1fr;gap:10px;align-items:center}}
.srow .sl{{font-size:{F['label']}px;color:var(--text2);font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.06em}}

/* backstage */
.win{{padding:0}}.win figcaption{{padding:8px 12px;margin:0;border-top:1px solid var(--border);background:var(--panel)}}
.bs{{display:flex;min-height:430px}}
.bsnav{{flex:0 0 200px;background:var(--panel);border-right:1px solid var(--border);padding:8px 0}}
.nav{{display:flex;align-items:center;gap:12px;height:40px;padding:0 20px;font-size:{F['panel-heading']}px;color:var(--text)}}
.nav svg{{color:var(--text2)}}
.nav.on{{background:var(--sel);box-shadow:inset 3px 0 0 var(--selbar);color:var(--acctext);font-weight:600}}.nav.on svg{{color:var(--acctext)}}
.bscontent{{flex:1;padding:24px 32px;min-width:0}}
.list{{max-width:620px;background:var(--raised);border:1px solid var(--border);border-radius:{R['large']}px;overflow:hidden}}
.rrow{{display:flex;align-items:center;gap:12px;height:40px;padding:0 12px;border-bottom:1px solid var(--border)}}.rrow:last-child{{border-bottom:none}}
.rrow svg{{color:var(--text2);flex:0 0 auto}}.rrow .rn{{flex:1;display:flex;flex-direction:column;min-width:0}}
.rrow .rn b{{font-weight:500;font-size:{F['body']}px}}.rrow .rn small{{font-size:{F['label']}px;color:var(--text2)}}.rrow code{{color:var(--text2)}}

/* start screen */
.wide{{grid-column:1/-1}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(200px,100%),1fr));gap:12px;max-width:900px}}
.pcard{{background:var(--raised);border:1px solid var(--border);border-radius:{R['large']}px;overflow:hidden;box-shadow:var(--shadow)}}
.pcard.hover{{border:var(--hoverw) solid var(--accent)}}
.thumb{{height:96px;background:var(--thumb);background-image:linear-gradient(var(--thumbline) 1px,transparent 1px),linear-gradient(90deg,var(--thumbline) 1px,transparent 1px);background-size:12px 12px;position:relative;border-bottom:1px solid var(--border)}}
.thumb i{{position:absolute;left:28%;top:24%;width:44%;height:50%;border:2px solid var(--accent);border-radius:2px}}
.pbody{{padding:10px 12px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}}
.pbody b{{font-size:{F['panel-heading']}px;font-weight:600}}.pbody code{{color:var(--text2)}}
.pill{{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.06em;font-size:{F['label']}px;padding:1px 8px;border-radius:9999px;color:var(--pc);border:1px solid var(--pc)}}
.choice{{position:relative;display:flex;flex-direction:column;gap:6px;padding:14px;background:var(--raised);border:1px solid var(--border);border-radius:{R['large']}px}}
.choice b{{font-size:{F['panel-heading']}px;font-weight:600}}.choice small{{color:var(--text2)}}
.choice .radio{{position:absolute;right:12px;top:12px;width:16px;height:16px;border-radius:50%;border:1.5px solid var(--bstrong)}}
.choice.chosen{{border:2px solid var(--selbar);padding:13px}}
.choice.chosen .radio{{border-color:var(--selbar);background:radial-gradient(var(--selbar) 0 4px,transparent 4.5px)}}

/* info cards */
.icard{{background:var(--raised);border:1px solid var(--border);border-radius:{R['large']}px;padding:4px 14px 10px}}
.icard .ih{{margin:10px 0 6px}}
.irow{{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px solid var(--border)}}.irow:last-child{{border-bottom:none}}
.irow span:first-child{{color:var(--text2)}}
.infowrap{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(320px,100%),1fr));gap:12px;max-width:900px;align-items:start}}
.stats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}}
.stat{{background:var(--raised);border:1px solid var(--border);border-radius:{R['large']}px;padding:12px;display:flex;flex-direction:column;gap:2px}}
.stat b{{font:700 {F['page-heading']}px/1.1 'Space Grotesk',Inter,sans-serif;white-space:nowrap}}.stat .mono{{margin:0}}
@media (max-width:640px){{.bsnav{{flex-basis:56px}}.nav span{{display:none}}.srow{{grid-template-columns:1fr}}.stats{{grid-template-columns:1fr}}}}
"""

page = f"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · tegels en kaarten 0.4</title>
<style>{CSS}</style>
<header>
  <a href="README.md">Fase 2: ontwerp 0.4</a>
  <h1>Tegels en kaarten · besloten</h1>
  <p>Stap 2.3. Alle kleuren, hoeken en maten komen uit <code>tokens-0.4.json</code>. De onderbouwing staat in <a href="03-tegels.md">03-tegels.md</a>.</p>
</header>
<main>
  <div class="facts"><span>5 soorten tegels en kaarten</span><span>{len(themes)} thema's</span><span>{len(check_rows)} contrastparen</span><span>{'Alle paren halen hun minimum' if not problems else str(len(problems)) + ' paren te laag'}</span></div>

  <h2>1. Zo ziet het Bestand-menu eruit</h2>
  <div class="q">Een voorbeeld met de voorgestelde taaktegels, variant B. Links staat de navigatie, rechts staan de taken en de recente bestanden. De tegel Importeren is uitgeschakeld.</div>
  <div class="grid2">{backstage('light')}{backstage('dark')}</div>

  <h2>2. Taaktegel: drie varianten</h2>
  <div class="q">De belangrijkste keuze. <b>A</b> is hoe het prototype het nu doet: alleen tekst op een getinte achtergrond. <b>B</b> volgt de Tauri-template en de website: een icoontegel links en een rand. <b>C</b> is een raster van grote tegels met het icoon boven, zoals het Nieuw-scherm in Office. <b>Besloten: B.</b> Het icoon maakt de taak snel herkenbaar, en de vorm is gelijk aan de website.</div>
  <div class="grid">{variant_block('light', 'a')}{variant_block('light', 'b')}{variant_block('light', 'c')}</div>
  <div class="grid" style="margin-top:16px">{variant_block('dark', 'a')}{variant_block('dark', 'b')}{variant_block('dark', 'c')}</div>

  <h2>3. Toestanden van een taaktegel</h2>
  <div class="q">Bij <b>hover</b> wordt de rand amber. <b>Ingedrukt</b> geeft de lichte accenttint, in High contrast een dikke amberkleurige rand. <b>Focus</b> geeft de focusring. <b>Uitgeschakeld</b> is vervaagd, in High contrast met een stippellijn. De tegel komt niet omhoog bij hover. Dat doet de website wel, maar het past niet bij een rustige app.</div>
  <div class="grid2">{''.join(states_block(t) for t in themes)}</div>

  <h2>4. Startscherm: projectkaarten en keuzetegels</h2>
  <div class="q"><b>Besloten:</b> apps die met projecten werken krijgen een startscherm met projectkaarten, met een voorbeeldbeeld waar de app dat kan maken en anders het app-icoon. Een <b>projectkaart</b> heeft een voorbeeldbeeld, een naam, mono-metadata en een statuslabel. Een <b>keuzetegel</b> kies je uit een groep, bijvoorbeeld een sjabloon. De gekozen tegel krijgt een rand van 2 px en een gevuld rondje.</div>
  <div class="grid">{start_block('light')}{start_block('dark')}</div>

  <h2>5. Infokaarten en cijfertegels</h2>
  <div class="q">Voor informatie die je leest maar niet aanklikt, zoals het Over-scherm, instellingen en overzichten. Ze hebben dezelfde vorm als de andere kaarten, maar geen hover.</div>
  <div class="grid">{info_block('light')}{info_block('dark')}</div>

  <h2>6. Contrast van de tegels</h2>
  <p>Gemeten per thema. Tekst moet 4,5:1 halen, in High contrast 7:1. Iconen, randen en de focusring moeten 3:1 halen.</p>
  <div class="tablewrap"><table><tr><th>Thema</th><th>Onderdeel</th><th>Kleur</th><th>Op</th><th>Verhouding / minimum</th></tr>{check_table}</table></div>

  <footer>Gegenereerd door <code>scripts/build_tegels_review.py</code> uit <code>design/ontwerp-0.4/tokens-0.4.json</code>. Iconen uit <code>crates/openaec-ui/assets/icons</code>.</footer>
</main>
</html>
"""

OUT.write_text(page, encoding="utf-8")
for p in problems:
    print("TE LAAG  " + p)
print(f"Wrote {OUT.relative_to(ROOT)}: {len(check_rows)} tile contrast pairs, {len(problems)} too low")
