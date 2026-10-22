#!/usr/bin/env python3
"""Build the meeting summary for step 2.6 from the decision tables in the specs.

Reads the "## Besluiten" table of each specification in design/ontwerp-0.4 and
writes design/ontwerp-0.4/samenvatting.html.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "design/ontwerp-0.4"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import evaluate  # noqa: E402

SPECS = [
    ("01-fundament.md", "Fundament", "fundament-review.html", "Thema's, kleuren, contrast, letters, maten en toestanden"),
    ("03-tegels.md", "Tegels en kaarten", "tegels-review.html", "Taaktegels, projectkaarten, keuzetegels en infokaarten"),
    ("04-componenten.md", "Componenten", "componenten-review.html", "Knoppen, velden, lint, panelen, tabellen, meldingen en dialogen"),
    ("05-layouts.md", "Layouts", "layouts-review.html", "Volledige schermen voor lint-apps en werkstroom-apps"),
]


def inline(text):
    t = html.escape(text)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def decisions(md_path):
    s = md_path.read_text(encoding="utf-8")
    m = re.search(r"^## Besluiten\s*$(.*?)(?=^## |\Z)", s, re.S | re.M)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].isdigit():
            rows.append((cells[0], " | ".join(cells[1:])))
    return rows


tokens = json.loads((DIR / "tokens-0.4.json").read_text(encoding="utf-8"))
problems, rows = evaluate(tokens)

sections, total = [], 0
for fname, title, review, sub in SPECS:
    dec = decisions(DIR / fname)
    total += len(dec)
    items = "".join(f"<li><span class=\"n\">{n}</span><span>{inline(t)}</span></li>" for n, t in dec)
    sections.append(f"""<section class="card"><div class="ch"><h3>{html.escape(title)}</h3><span class="cnt">{len(dec)} besluiten</span></div>
<p class="sub">{html.escape(sub)}. <a href="{fname}">Specificatie</a> · <a href="{review}">Voorbeelden</a></p><ol class="dec">{items}</ol></section>""")

OPEN = [
    ("Iconen (2.2)", "De iconen van Codex, stijl B Constructief, worden de definitieve set. De voorbeeldpagina's gebruiken al de iconen die er zijn. Alleen voor functies die nog ontbreken, staat tijdelijk een oud icoon uit het prototype.",
     '<a href="../icon-set-b2/index.html">Eerste serie</a> · <a href="../icon-set-b2/series-2.html">Tweede serie</a>'),
    ("Licentie van de iconen", "De bibliotheek valt onder LGPL-3.0-only (besloten 2026-10-22). Voor de iconen van Codex volgt de keuze nog: LGPL of een aparte iconenlicentie.", ""),
    ("Field op tablet of telefoon", "Energy en Field gaan naar de Rust-UI, net als PDF, Speech, Composer en Frame. Blijkt Field op locatie op een tablet of telefoon nodig, dan kijken we opnieuw naar het webpakket.", ""),
]
open_html = "".join(f'<li><b>{html.escape(t)}</b><span>{d}</span>{(" <span class=\"lk\">" + lk + "</span>") if lk else ""}</li>' for t, d, lk in OPEN)

FREEZE = [
    ("De gebruiker heeft de besluiten vastgesteld", True),
    ("Iconen van Codex zijn beoordeeld en compleet, zodat er geen tijdelijke iconen meer in de voorbeelden staan", False),
    ("Tokenbestand heeft versie 0.4.0", True),
    (f"Alle {len(rows)} kleurparen halen hun minimum", not problems),
    ("Specificaties en reviewpagina's zijn bijgewerkt", True),
]
freeze_html = "".join(f'<li class="{"ok" if ok else "todo"}"><span class="chk">{"✓" if ok else ""}</span>{html.escape(t)}</li>' for t, ok in FREEZE)


def esc_t(x):
    return html.escape(x)


CSS = r"""
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-Regular.ttf');font-weight:400}
@font-face{font-family:Inter;src:url('../../assets/fonts/Inter-SemiBold.ttf');font-weight:600 800}
@font-face{font-family:'Space Grotesk';src:url('../../assets/fonts/SpaceGrotesk-Bold.ttf');font-weight:700}
@font-face{font-family:'JetBrains Mono';src:url('../../assets/fonts/JetBrainsMono-Regular.ttf')}
*{box-sizing:border-box}
body{margin:0;background:#F1EEEA;color:#2A2A32;font:14px/1.55 Inter,system-ui,sans-serif}
header{background:#2A2A32;color:#EDEBE8;padding:28px max(22px,calc((100vw - 1100px)/2));border-bottom:3px solid #D97706}
header a{color:#FBBF24}header p{margin:0;max-width:820px;color:#D4D1CC}
h1{font:700 30px/1.2 'Space Grotesk',Inter,sans-serif;letter-spacing:-.02em;margin:8px 0}
h2{font:700 22px/1.3 'Space Grotesk',Inter,sans-serif;letter-spacing:-.02em;margin:36px 0 10px}
h3{font:700 17px/1.3 'Space Grotesk',Inter,sans-serif;margin:0}
main{max-width:1100px;margin:auto;padding:24px 22px 48px}
a{color:#92400E}code{font-family:'JetBrains Mono',monospace;font-size:12px}
.facts{display:flex;gap:10px;flex-wrap:wrap}
.fact{background:#fff;border:1px solid rgba(42,42,50,.09);border-radius:10px;padding:10px 14px}
.fact b{display:block;font:700 22px/1.1 'Space Grotesk',Inter,sans-serif}
.fact span{font:11px 'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;color:#5F5F65}
.card{background:#fff;border:1px solid rgba(42,42,50,.09);border-radius:10px;padding:16px 20px;margin-bottom:14px}
.ch{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.cnt{font:11px 'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;color:#92400E;background:#FBF1E6;border-radius:9999px;padding:2px 10px}
.sub{margin:4px 0 10px;color:#5F5F65}
.dec{list-style:none;margin:0;padding:0}
.dec li{display:flex;gap:12px;padding:7px 0;border-top:1px solid #EAEAEA}
.dec .n{flex:0 0 28px;font:12px 'JetBrains Mono',monospace;color:#5F5F65;padding-top:2px}
.open{list-style:none;margin:0;padding:0}
.open li{background:#fff;border:1px solid rgba(42,42,50,.09);border-left:3px solid #D97706;border-radius:6px;padding:10px 14px;margin-bottom:8px;display:flex;flex-direction:column;gap:2px}
.open .lk{font-size:13px}
.freeze{list-style:none;margin:0;padding:0;background:#fff;border:1px solid rgba(42,42,50,.09);border-radius:10px;overflow:hidden}
.freeze li{display:flex;gap:12px;align-items:center;padding:10px 14px;border-top:1px solid #EAEAEA}.freeze li:first-child{border-top:0}
.chk{width:18px;height:18px;border-radius:3px;border:1.5px solid #7F7F84;display:grid;place-items:center;font-size:12px;font-weight:700}
.freeze li.ok .chk{background:#D97706;border-color:#D97706;color:#1C1917}
footer{color:#5F5F65;font-size:12px;margin-top:32px}
@media (max-width:640px){.dec li{flex-direction:column;gap:2px}}
"""

page = f"""<!doctype html>
<html lang="nl">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · ontwerp 0.4 · samenvatting</title>
<style>{CSS}</style>
<header>
  <a href="README.md">Fase 2: ontwerp 0.4</a>
  <h1>Ontwerp 0.4 · vastgesteld</h1>
  <p>Alle besluiten van fase 2 op één pagina, met links naar de voorbeelden. Vastgesteld op 2026-10-16 en bevroren als versie 0.4. De iconen lopen nog door.</p>
</header>
<main>
  <div class="facts">
    <div class="fact"><b>{total}</b><span>Besluiten</span></div>
    <div class="fact"><b>5</b><span>Thema's</span></div>
    <div class="fact"><b>17</b><span>Apps in scope</span></div>
    <div class="fact"><b>{len(rows)}</b><span>Kleurparen getoetst</span></div>
    <div class="fact"><b>{"Alle" if not problems else len(problems)}</b><span>{"Halen de norm" if not problems else "Te laag"}</span></div>
  </div>

  <h2>Besluiten per onderdeel</h2>
  {''.join(sections)}

  <h2>Nog open</h2>
  <ul class="open">{open_html}</ul>

  <h2>Voorwaarden om te bevriezen als 0.4</h2>
  <ul class="freeze">{freeze_html}</ul>

  <footer>Gegenereerd door <code>scripts/build_samenvatting_04.py</code> uit de besluittabellen in <code>design/ontwerp-0.4/*.md</code> en <code>tokens-0.4.json</code>. Draai het script opnieuw na een nieuw besluit.</footer>
</main>
</html>
"""
(DIR / "samenvatting.html").write_text(page, encoding="utf-8")
print(f"Wrote design/ontwerp-0.4/samenvatting.html: {total} decisions, {len(rows)} colour pairs, {len(problems)} problems")
