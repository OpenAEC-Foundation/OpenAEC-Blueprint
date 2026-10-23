#!/usr/bin/env python3
"""Build the design-foundation review page for UI version 0.4.

Reads the five theme token sets and the pinned Style Book token snapshot,
computes WCAG contrast for key colour pairs and writes
design/ontwerp-0.4/fundament-review.html.
"""

import html
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
themes = json.loads((root / "assets/tokens.json").read_text(encoding="utf-8"))
sb_dir = root / "harmonization/references/OpenAEC-style-book/packages/tokens"
sb = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (sb_dir / "tokens").glob("*.json")}
sb_commit = (sb_dir / "SOURCE_COMMIT").read_text(encoding="utf-8").strip()[:7]
out_path = root / "design/ontwerp-0.4/fundament-review.html"
tokens04 = json.loads((root / "design/ontwerp-0.4/tokens-0.4.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import evaluate  # noqa: E402

THEME_NAMES = {"light": "Light", "forge": "Forge", "openaec": "OpenAEC", "blueprint": "Blueprint", "contrast": "High contrast"}

PAIRS = [
    ("Tekst op achtergrond", "text", "bg", 4.5),
    ("Secundaire tekst", "text-secondary", "bg", 4.5),
    ("Gedempte tekst", "text-muted", "bg", 4.5),
    ("Vage tekst", "text-faint", "bg", 4.5),
    ("Accent als tekst", "accent", "surface", 4.5),
    ("Tekst op primaire knop", "btn-primary-text", "btn-primary-bg", 4.5),
    ("Tekst op Bestand-tab", "file-tab-text", "file-tab-bg", 4.5),
    ("Lintgroeplabel", "ribbon-group-label", "surface", 4.5),
    ("Statusbalktekst", "status-text", "status-bg", 4.5),
    ("Dialoogkop", "dialog-header-text", "dialog-header-bg", 4.5),
    ("Focuskleur", "focus-color", "surface", 3.0),
    ("Rand", "border", "surface", 3.0),
    ("Foutkleur als tekst", "danger-color", "surface", 4.5),
]


def parse(value):
    value = value.strip()
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)] + [1.0]
    m = re.match(r"rgba?\(([^)]+)\)", value)
    parts = [x.strip() for x in m.group(1).split(",")]
    return [float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) if len(parts) > 3 else 1.0]


def over(fg, bg):
    a = fg[3]
    return [fg[i] * a + bg[i] * (1 - a) for i in range(3)] + [1.0]


def luminance(c):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(x) for x in c[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_value, bg_value, base=None):
    bg = parse(bg_value)
    if bg[3] < 1 and base:
        bg = over(bg, parse(base))
    fg = over(parse(fg_value), bg)
    la, lb = luminance(fg), luminance(bg)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def fmt(r):
    return f"{r:.2f}".replace(".", ",")


def esc(s):
    return html.escape(str(s))


# ---------- contrast table ----------
results = {t: [(label, round(ratio(tok[f], tok[b], tok["bg"]), 2), need) for label, f, b, need in PAIRS] for t, tok in themes.items()}
head = "".join(f"<th>{esc(THEME_NAMES[t])}</th>" for t in themes)
rows = []
for i, (label, f, b, need) in enumerate(PAIRS):
    cells = []
    for t in themes:
        r = results[t][i][1]
        ok = r >= need
        cells.append(f'<td class="{"ok" if ok else "bad"}"><b>{fmt(r)}</b> {"gehaald" if ok else "te laag"}</td>')
    rows.append(f"<tr><th>{esc(label)}<small>{esc(f)} op {esc(b)} · minimaal {fmt(need)}</small></th>{''.join(cells)}</tr>")
totals = "".join(
    f"<td><b>{sum(1 for _, r, n in results[t] if r >= n)}</b> van {len(PAIRS)}</td>" for t in themes
)
contrast_table = f"<div class=\"tablewrap\"><table class=\"contrast\"><tr><th>Kleurpaar</th>{head}</tr>{''.join(rows)}<tr class=\"total\"><th>Gehaald</th>{totals}</tr></table></div>"


# ---------- theme previews ----------
def preview(t, tok):
    v = lambda k: esc(tok[k])
    return f"""
<figure class="theme" style="background:{v('bg')};color:{v('text')};border-color:{v('border')}">
  <figcaption style="background:{v('status-bg')};color:{v('status-text')}">{esc(THEME_NAMES[t])}</figcaption>
  <div class="tabs" style="background:{v('docbar-bg')};border-bottom:2px solid {v('accent')}">
    <span style="background:{v('file-tab-bg')};color:{v('file-tab-text')}">Bestand</span>
    <span class="active" style="color:{v('ribbon-btn-active-text')};background:{v('surface')};border-color:{v('accent')}">Start</span>
    <span style="color:{v('text-secondary')}">Beeld</span>
  </div>
  <div class="group" style="background:{v('surface')};border-right:1px solid {v('ribbon-group-separator')}">
    <div class="btns"><span class="rb" style="background:{v('ribbon-btn-active-bg')};color:{v('ribbon-btn-active-text')}">Actief</span><span class="rb" style="color:{v('text')}">Knop</span></div>
    <div class="glabel" style="color:{v('ribbon-group-label')}">Lintgroep</div>
  </div>
  <div class="body" style="background:{v('surface')}">
    <p style="color:{v('text')}">Tekst · {fmt(results[t][0][1])}</p>
    <p style="color:{v('text-secondary')}">Secundair · {fmt(results[t][1][1])}</p>
    <p style="color:{v('text-muted')}">Gedempt · {fmt(results[t][2][1])}</p>
    <p style="color:{v('text-faint')}">Vaag · {fmt(results[t][3][1])}</p>
    <p style="color:{v('accent')}">Accent als tekst · {fmt(results[t][4][1])}</p>
    <div class="field" style="background:{v('dialog-input-bg')};border-color:{v('dialog-input-border')};color:{v('text')}">Invoerveld</div>
    <div class="row">
      <span class="btn" style="background:{v('btn-primary-bg')};color:{v('btn-primary-text')}">Primair · {fmt(results[t][5][1])}</span>
      <span class="btn" style="background:{v('btn-secondary-bg')};color:{v('btn-secondary-text')};border:1px solid {v('border')}">Secundair</span>
    </div>
    <div class="dlg" style="background:{v('dialog-header-bg')};color:{v('dialog-header-text')}">Dialoogkop · {fmt(results[t][9][1])}</div>
    <p style="color:{v('danger-color')}">Foutmelding · {fmt(results[t][12][1])}</p>
  </div>
  <div class="status" style="background:{v('status-bg')};color:{v('status-text')}">Statusbalk · {fmt(results[t][8][1])}</div>
</figure>"""


previews = "".join(preview(t, tok) for t, tok in themes.items())


# ---------- proposals ----------
def swatch_pair(label, fg, bg, note=""):
    r = ratio(fg, bg)
    ok = r >= 4.5
    return f"""<div class="prop"><div class="sample" style="background:{esc(bg)};color:{esc(fg)}">{esc(label)}</div>
<div class="meta"><b class="{"ok" if ok else "bad"}">{fmt(r)}</b> {esc(fg)} op {esc(bg)}{(" · " + esc(note)) if note else ""}</div></div>"""


proposals = f"""
<div class="props">
  <section><h3>Light · primaire knop</h3>
    {swatch_pair("Nu: wit op amber", "#FFFFFF", "#D97706")}
    {swatch_pair("Optie A: donkere tekst", "#1C1917", "#D97706", "merkkleur blijft exact")}
    {swatch_pair("Optie B: donkerder amber", "#FFFFFF", "#B45309", "witte tekst blijft")}
  </section>
  <section><h3>Forge · primaire knop</h3>
    {swatch_pair("Nu: Deep Forge op amber", themes["forge"]["btn-primary-text"], themes["forge"]["btn-primary-bg"])}
    {swatch_pair("Optie A: donkere tekst", "#1C1917", "#D97706")}
    {swatch_pair("Optie B: donkerder amber", "#FFFFFF", "#B45309")}
  </section>
  <section><h3>Accent als tekst</h3>
    {swatch_pair("Light nu", "#D97706", "#FFFFFF")}
    {swatch_pair("Light voorstel", "#B45309", "#FFFFFF")}
    {swatch_pair("Forge nu", "#D97706", "#36363E")}
    {swatch_pair("Forge voorstel: Warm Gold", "#F59E0B", "#36363E")}
  </section>
</div>"""


# ---------- conflicts ----------
brand = {k: v["value"] for k, v in sb["colors"]["color"]["brand"].items()}
neutral = {k: v["value"] for k, v in sb["colors"]["color"]["neutral"].items()}
neutral_strip = "".join(
    f'<div class="chip{" flag" if k in ("900", "950") else ""}"><span style="background:{esc(c)}"></span><b>{esc(k)}</b><small>{esc(c)}</small></div>'
    for k, c in neutral.items()
)
conflicts = f"""
<div class="conflicts">
  <section><h3>Night Build</h3>
    <div class="row">
      <div class="chip big"><span style="background:#1C1917"></span><b>#1C1917</b><small>thema's, gebruikt in OpenAEC</small></div>
      <div class="chip big"><span style="background:{esc(brand['night-build'])}"></span><b>{esc(brand['night-build'])}</b><small>Style Book-tokens</small></div>
    </div>
  </section>
  <section><h3>Betekenis van "accent"</h3>
    <div class="row">
      <div class="chip big"><span style="background:{esc(themes['light']['accent'])}"></span><b>{esc(themes['light']['accent'])}</b><small>accent in de thema's</small></div>
      <div class="chip big"><span style="background:{esc(brand['accent'])}"></span><b>{esc(brand['accent'])}</b><small>accent-alias in het Style Book</small></div>
    </div>
  </section>
  <section class="wide"><h3>Grijsschaal van het Style Book</h3>
    <p>Stap 900 is donkerder dan stap 950. In een gewone schaal is 950 het donkerst.</p>
    <div class="strip">{neutral_strip}</div>
  </section>
</div>"""


# ---------- typography ----------
desktop_scale = [("Klein", 11, "Statusbalk, lintgroeplabel, sneltoetsen"), ("Standaard", 12, "Knoppen, velden, lijsten, panelen"),
                 ("Paneelkop", 13, "Paneel- en sectiekoppen"), ("Dialoogkop", 16, "Kop van een dialoog"), ("Paginakop", 22, "Bestand-menu en startscherm")]
sb_sizes = sb["typography"]["font"]["size"]
type_desktop = "".join(
    f'<div class="ty"><span class="lbl">{esc(n)} · {s} px</span><span style="font-size:{s}px;font-family:{"'Space Grotesk',Inter" if s >= 16 else "Inter"},system-ui,sans-serif;font-weight:{500 if s >= 13 else 400}">{esc(use)}</span></div>'
    for n, s, use in desktop_scale
)
type_sb = "".join(
    f'<div class="ty"><span class="lbl">{esc(k)} · {esc(v.get("comment", v["value"]).split(" ")[0])}</span><span style="font-size:{esc(v["value"])}">OpenAEC</span></div>'
    for k, v in sb_sizes.items()
)


# ---------- sizes ----------
def bar(label, a, b, scale=1.0):
    return f"""<div class="bar"><span class="lbl">{esc(label)}</span>
<div class="b"><i style="width:{a * scale}px"></i><em>{a} px · Tauri en Rust</em></div>
<div class="b sb"><i style="width:{b * scale}px"></i><em>{b} px · Style Book</em></div></div>"""


sizes = (bar("Titelbalk", 32, 48, 3) + bar("Lint", 94, 96, 3) + bar("Zijpaneel", 240, 280, 1.2))

# ---------- version 0.4 themes ----------
problems04, rows04 = evaluate(tokens04)
R = tokens04["radius"]


def hexa(h, a):
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{a})"


def preview04(tid, th):
    c = th["color"]
    hc = th.get("high-contrast", False)
    sel = (f"outline:2px solid {c['selected-bar']};outline-offset:-2px" if th["selection-style"] == "outline"
           else f"background:{c['selected']};box-shadow:inset 3px 0 0 {c['selected-bar']}")
    dis = (f"border:1px dashed {c['text-disabled']};color:{c['text-disabled']}" if th["disabled-style"] == "dashed"
           else f"border:1px solid {c['border']};color:{c['text-disabled']}")
    chips = "".join(
        f'<span class="v4chip" style="color:{c[k]};{"border:1px solid " + c[k] if hc else "background:" + c[k + "-tint"]}">{lbl}</span>'
        for k, lbl in (("error", "Fout"), ("success", "Gelukt"), ("warning", "Let op"), ("info", "Info")))
    return f"""
<figure class="v4" style="background:{c['frame']};color:{c['text']};border-color:{c['border']}">
  <div class="v4title" style="background:{c['panel']};color:{c['accent-text']};border-bottom:1px solid {c['border']}">Open Calc Studio</div>
  <div class="v4tabs" style="background:{c['panel']};border-bottom:2px solid {c['accent']}">
    <span style="background:{c['accent']};color:{c['text-on-accent']}">Bestand</span>
    <span style="color:{c['accent-text']};border:1px solid {c['accent']};border-bottom:none">Start</span>
    <span style="color:{c['text-secondary']}">Beeld</span>
  </div>
  <div class="v4ribbon" style="background:{c['panel']};border-bottom:1px solid {c['border']}">
    <div class="v4grp" style="border-right:1px solid {c['border']}"><div class="v4btns"><i style="border-color:{c['selected-bar']};background:{c['selected']}"></i><i style="border-color:{c['border-strong']}"></i><i style="border-color:{c['border-strong']}"></i></div><div class="v4mono" style="color:{c['text-secondary']}">Klembord</div></div>
    <div class="v4grp" style="border-right:1px solid {c['border']}"><div class="v4btns"><i style="border-color:{c['border-strong']}"></i><i style="border-color:{c['border-strong']}"></i></div><div class="v4mono" style="color:{c['text-secondary']}">Begroting</div></div>
  </div>
  <div class="v4doc" style="background:{c['docbar']};border-bottom:1px solid {c['border']}"><span style="background:{c['workspace']};color:{c['workspace-text']};border-top:2px solid {c['accent']}">Begroting.ocs</span><span style="color:{c['text-secondary']}">Variant B</span></div>
  <div class="v4body">
    <div class="v4panel" style="background:{c['panel']};border-right:1px solid {c['border']}">
      <div class="v4mono v4ph" style="color:{c['text-secondary']};border-bottom:1px solid {c['border']}">Verkenner</div>
      <div class="v4row" style="{sel}">Fundering</div><div class="v4row">Ruwbouw</div><div class="v4row" style="color:{c['text-secondary']}">Afbouw</div>
    </div>
    <div class="v4work" style="background:{c['workspace']};color:{c['workspace-text']}">Werkruimte</div>
    <div class="v4panel v4props" style="background:{c['panel']};border-left:1px solid {c['border']}">
      <div class="v4mono v4ph" style="color:{c['text-secondary']};border-bottom:1px solid {c['border']}">Eigenschappen</div>
      <div class="v4field" style="border:1px solid {c['border-strong']};border-radius:{R['medium']}px;background:{c['raised']}">Hoeveelheid</div>
      <div class="v4act"><span style="background:{c['accent']};color:{c['text-on-accent']};border-radius:{R['medium']}px;box-shadow:0 0 0 2px {c['panel']},0 0 0 4px {c['focus']}">Opslaan</span><span style="{dis};border-radius:{R['medium']}px">Export</span></div>
      <div class="v4chips">{chips}</div>
    </div>
  </div>
  <div class="v4status" style="background:{c['statusbar']};color:{c['statusbar-text']};border-top:1px solid {c['border']}">Gereed · 91 posten</div>
  <figcaption style="background:{c['panel']};color:{c['text']};border-top:1px solid {c['border']}"><b>{esc(th['name'])}</b></figcaption>
</figure>"""


previews04 = "".join(preview04(t, th) for t, th in tokens04["themes"].items())

summary_rows = []
details = []
for tid, th in tokens04["themes"].items():
    mine = [r for r in rows04 if r[0] == tid]
    low = min(mine, key=lambda r: r[5] / r[6])
    ok = all(r[5] >= r[6] for r in mine)
    summary_rows.append(
        f"<tr><th>{esc(th['name'])}</th><td>{len(mine)}</td><td>{fmt(low[5])} · {esc(low[1])} op {esc(low[3])}</td>"
        f"<td class=\"{'ok' if ok else 'bad'}\">{'alle gehaald' if ok else 'niet alles gehaald'}</td></tr>")
    body = "".join(
        f"<tr><td>{esc(r[1])}</td><td><span class=\"sw\" style=\"background:{th['color'].get(r[2], r[2])}\"></span><code>{esc(th['color'].get(r[2], r[2]))}</code></td>"
        f"<td><span class=\"sw\" style=\"background:{r[4]}\"></span>{esc(r[3])}</td><td class=\"{'ok' if r[5] >= r[6] else 'bad'}\"><b>{fmt(r[5])}</b> / {fmt(r[6])}</td></tr>"
        for r in mine)
    details.append(f"<details><summary>{esc(th['name'])}: alle {len(mine)} paren</summary><div class=\"tablewrap\"><table><tr><th>Paar</th><th>Kleur</th><th>Op</th><th>Verhouding / minimum</th></tr>{body}</table></div></details>")
summary04 = ("<div class=\"tablewrap\"><table class=\"contrast\"><tr><th>Thema</th><th>Getoetste paren</th><th>Krapste paar</th><th>Resultaat</th></tr>"
             + "".join(summary_rows) + "</table></div>" + "".join(details))


css = """

.v4{margin:0;border:1px solid;overflow:hidden;font-size:11px;line-height:1.35}
.v4title{height:24px;display:flex;align-items:center;justify-content:center;font-weight:600}
.v4tabs{display:flex;gap:2px;padding:3px 6px 0}.v4tabs span{padding:2px 9px}
.v4ribbon{display:flex;height:56px}.v4grp{padding:5px 8px 3px;display:flex;flex-direction:column;justify-content:space-between;align-items:center;min-width:80px}
.v4btns{display:flex;gap:4px}.v4btns i{display:block;width:22px;height:22px;border:1.5px solid;border-radius:3px}
.v4mono{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;font-size:9.5px}
.v4doc{display:flex;gap:2px;padding:3px 4px 0}.v4doc span{padding:2px 8px}
.v4body{display:flex;height:150px}.v4panel{width:30%;display:flex;flex-direction:column}.v4props{width:36%;padding-bottom:6px}
.v4ph{height:20px;display:flex;align-items:center;padding:0 7px}.v4row{padding:3px 7px}
.v4work{flex:1;display:grid;place-items:center;font-size:10px}
.v4field{margin:6px 7px 0;padding:3px 6px}.v4act{display:flex;gap:6px;margin:8px 7px 0}.v4act span{padding:3px 8px;font-weight:600}
.v4chips{display:flex;gap:4px;flex-wrap:wrap;margin:8px 7px 0}.v4chip{font-family:'JetBrains Mono',monospace;text-transform:uppercase;font-size:9px;letter-spacing:.05em;padding:1px 6px;border-radius:9999px}
.v4status{height:18px;display:flex;align-items:center;padding:0 7px;font-size:10px}
.v4 figcaption{padding:6px 9px;font-size:12px}
.themes04{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(360px,100%),1fr));gap:14px}
.sw{display:inline-block;width:12px;height:12px;border:1px solid #bbb;vertical-align:-2px;margin-right:6px}
details{margin:8px 0;background:#fff;border:1px solid #d8d8dd;padding:8px 12px}summary{cursor:pointer;font-weight:600}
.old{border-top:3px solid #d8d8dd;margin-top:44px;padding-top:4px}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf');font-weight:400}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Medium.ttf');font-weight:500}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-SemiBold.ttf');font-weight:600 800}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Medium.ttf');font-weight:500}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}
@font-face{font-family:'JetBrains Mono';src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
*{box-sizing:border-box}body{margin:0;background:#f3f3f2;color:#303039;font:14px/1.5 Inter,system-ui,sans-serif}
header{background:#303039;color:#fff;padding:26px max(22px,calc((100vw - 1420px)/2));border-bottom:3px solid #dc7900}
header a{color:#ffc180}h1{font:700 29px/1.2 'Space Grotesk',Inter,sans-serif;margin:8px 0}header p{margin:0;color:#dddde3;max-width:1000px}
main{max-width:1460px;margin:auto;padding:23px 22px 46px}h2{font:500 21px/1.3 'Space Grotesk',Inter,sans-serif;margin:34px 0 8px}h3{font-size:15px;margin:0 0 10px}
p{max-width:1000px}.facts{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:8px}.facts span{background:#fff;border:1px solid #d8d8dd;padding:8px 11px}
.note{background:#fffaf2;border-left:3px solid #dc7900;padding:12px 16px;max-width:1040px;margin:14px 0}
.themes{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr));gap:14px}
.theme{margin:0;border:1px solid;overflow:hidden;font-size:12px}.theme figcaption{padding:6px 10px;font-weight:600}
.tabs{display:flex;gap:2px;padding:4px 6px 0;height:28px}.tabs span{padding:3px 10px;border:1px solid transparent;border-bottom:none}
.group{padding:6px 8px}.btns{display:flex;gap:6px}.rb{padding:4px 8px;border-radius:2px}.glabel{font-size:11px;text-align:center;margin-top:4px}
.body{padding:8px 10px}.body p{margin:3px 0}.field{border:1px solid;padding:4px 8px;margin:8px 0;border-radius:2px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start}.btn{padding:5px 10px;border-radius:4px;font-weight:600}
.dlg{padding:6px 8px;margin:8px 0;font-weight:600}.status{padding:3px 10px;font-size:11px}
.tablewrap{overflow-x:auto;max-width:100%}table{border-collapse:collapse;background:#fff;width:100%;min-width:640px}th,td{text-align:left;vertical-align:top;border:1px solid #dedee2;padding:8px 10px}
th small{display:block;font-weight:400;color:#6b6b75;font-size:11px}.contrast td.ok{background:#f0fdf4}.contrast td.bad{background:#fef2f2}
.contrast .total td,.contrast .total th{background:#f5f5f4}b.ok{color:#15803d}b.bad{color:#b91c1c}
.props,.conflicts{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:14px}.props section,.conflicts section{background:#fff;border:1px solid #d8d8dd;padding:14px}
.conflicts .wide{grid-column:1/-1}.prop{margin-bottom:10px}.sample{padding:9px 12px;font-weight:600;border:1px solid #e5e5e5}.meta{font-size:12px;color:#55555f;margin-top:3px}
.chip{display:flex;flex-direction:column;align-items:flex-start;font-size:12px}.chip span{width:56px;height:36px;border:1px solid #ccc}.chip.big span{width:110px;height:56px}
.chip small{color:#6b6b75}.strip{display:flex;gap:6px;flex-wrap:wrap}.chip.flag span{outline:3px solid #dc2626;outline-offset:2px}
.types{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(420px,100%),1fr));gap:14px}.types section{min-width:0}.types section{background:#fff;border:1px solid #d8d8dd;padding:14px}
.ty{display:flex;gap:14px;align-items:baseline;border-bottom:1px solid #eee;padding:6px 0;overflow:hidden;white-space:nowrap}.ty .lbl{flex:0 0 170px;font-size:12px;color:#6b6b75}
.bars{background:#fff;border:1px solid #d8d8dd;padding:14px;max-width:1040px}.bar{margin:8px 0}.bar .lbl{font-weight:600;display:block}
.b{display:flex;align-items:center;gap:8px;margin:3px 0}.b i{display:block;height:14px;background:#36363e;max-width:70%}.b.sb i{background:#d97706}.b em{font-style:normal;font-size:12px;color:#55555f}
footer{color:#6b6b75;font-size:12px;margin-top:30px}code{font-family:'JetBrains Mono',monospace;font-size:12px}
@media (max-width:640px){.ty .lbl{flex-basis:110px}.types{grid-template-columns:minmax(0,1fr)}}
"""

page = f"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · fundament 0.4</title>
<style>{css}</style>
<header>
  <a href="README.md">Fase 2: ontwerp 0.4</a>
  <h1>Fundament · besloten</h1>
  <p>De vijf thema's voor versie 0.4, gemaakt uit <code>tokens-0.4.json</code>, met het gemeten contrast. Daaronder de analyse van de huidige thema's waar de besluiten op steunen. De besluiten staan in <a href="01-fundament.md">01-fundament.md</a>.</p>
</header>
<main>
  <div class="facts"><span>Tokens {esc(tokens04['meta']['version'])}</span><span>{len(tokens04['themes'])} nieuwe thema's</span><span>{len(rows04)} kleurparen getoetst</span><span>{'Alle paren halen hun minimum' if not problems04 else str(len(problems04)) + ' paren te laag'}</span></div>

  <h2>Thema's voor versie 0.4</h2>
  <p>Elk voorbeeld gebruikt alleen waarden uit <code>tokens-0.4.json</code>. Hoeken, mono-labels, selectie, focusring en statuslabels volgen de besluiten. De knop Opslaan toont de focusring.</p>
  <div class="themes04">{previews04}</div>

  <h2>Contrast van de nieuwe thema's</h2>
  <p>Gemeten met <code>scripts/check_tokens_04.py</code>. Tekst moet 4,5:1 halen, in High contrast 7:1. Randen van velden, de focusring en de selectiestreep moeten 3:1 halen. Statuskleuren zijn ook getoetst op hun eigen lichte tint.</p>
  {summary04}

  <div class="old"><h2>Uitgangssituatie: de huidige thema's</h2><p>Hieronder de analyse van de vijf huidige thema's uit <code>assets/tokens.json</code>, waarop de besluiten zijn gebaseerd.</p></div>
  <div class="facts"><span>{len(themes)} huidige thema's</span><span>{len(themes['light'])} kleurvelden per thema</span><span>{len(PAIRS)} kleurparen getoetst</span><span>Style Book-tokens op commit <code>{esc(sb_commit)}</code></span></div>

  <h3>Huidige thema's naast elkaar</h3>
  <p>Elk voorbeeld gebruikt de echte waarden uit <code>assets/tokens.json</code>. De getallen zijn contrastverhoudingen.</p>
  <div class="themes">{previews}</div>

  <h2>Contrast volgens WCAG 2.2 AA</h2>
  <p>Tekst moet 4,5:1 halen. De focuskleur en de randen van bedieningselementen moeten 3:1 halen. Halfdoorzichtige kleuren zijn eerst met de achtergrond gemengd.</p>
  <div class="note">Een rand die alleen decoratief scheidt, hoeft niet 3:1 te halen. De rand van een invoerveld wel, omdat die laat zien waar het veld is.</div>
  {contrast_table}

  <h2>Voorstellen voor Light en Forge</h2>
  <p>Kleine aanpassingen die de norm halen. Optie A houdt de merkkleur exact, optie B houdt de witte tekst.</p>
  {proposals}

  <h2>Tegenstrijdigheden tussen de bronnen</h2>
  {conflicts}

  <h2>Typografie</h2>
  <div class="types">
    <section><h3>Voorstel: desktopschaal</h3>{type_desktop}</section>
    <section><h3>Style Book: webschaal</h3>{type_sb}</section>
  </div>

  <h2>Maten van de schil</h2>
  <p>De desktopmaten komen uit de Tauri-template en worden bewaakt door <code>scripts/check_layout_metrics.py</code>. De Style Book-maten zijn bedoeld voor webapps.</p>
  <div class="bars">{sizes}</div>

  <footer>Gegenereerd door <code>scripts/build_fundament_review.py</code> uit <code>design/ontwerp-0.4/tokens-0.4.json</code> en <code>assets/tokens.json</code>. Draai dat script opnieuw na een wijziging in de tokens.</footer>
</main>
</html>
"""

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(page, encoding="utf-8")
failed = {THEME_NAMES[t]: sum(1 for _, r, n in results[t] if r < n) for t in themes}
print(f"Wrote {out_path.relative_to(root)}: 0.4 tokens {len(tokens04['themes'])} themes, {len(rows04)} pairs, {len(problems04)} failures; current themes failures {failed}")
