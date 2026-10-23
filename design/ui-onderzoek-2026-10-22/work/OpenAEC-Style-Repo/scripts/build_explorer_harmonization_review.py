#!/usr/bin/env python3
"""Compare source-used Pile and Pointcloud explorer commands before Rust adoption."""
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINT = Path("harmonization/ui-icons/open-pointcloud-studio/native/assets/opencad-icons")
PILE = Path("harmonization/inline-ui-icons/pile-plan-studio-workarea")
PAIRS = [
    ("duplicate", "Dupliceren", "explorer-copy.svg", "browser_duplicate.svg", "Pile Plan gebruikt twee overlappende bladen; Pointcloud voegt blauw en een plus toe. De handeling is dezelfde."),
    ("rename", "Hernoemen", "explorer-edit.svg", "browser_rename.svg", "Beide bronnen gebruiken een potlood. Eén monochrome lijnvorm maakt de bediening in Light en Forge gelijk."),
    ("disclosure-expanded", "Groep uitgeklapt", "explorer-collapse.svg", "chevron_open.svg", "De pijl omlaag duidt in beide verkenners de huidige open toestand aan."),
    ("disclosure-collapsed", "Groep ingeklapt", "explorer-expand.svg", "chevron_closed.svg", "De pijl naar rechts duidt in beide verkenners de huidige gesloten toestand aan."),
]

entries = []
for key, label, pile_file, point_file, assessment in PAIRS:
    pile = ROOT / PILE / pile_file
    point = ROOT / POINT / point_file
    assert pile.is_file() and point.is_file()
    entries.append({
        "id": key, "label": label, "pile_svg": str(PILE / pile_file),
        "pointcloud_svg": str(POINT / point_file),
        "pile_sha256": hashlib.sha256(pile.read_bytes()).hexdigest(),
        "pointcloud_sha256": hashlib.sha256(point.read_bytes()).hexdigest(),
        "assessment": assessment,
        "candidate": "Pile Plan source geometry with CSS stroke captured in extracted SVG",
        "decision": "adopted-in-shared-rust-crate-and-pointcloud",
    })

(ROOT / "design/pile-pointcloud-explorer-decisions.json").write_text(json.dumps({"pairs": entries}, ensure_ascii=False, indent=2) + "\n")


def imgs(path: str) -> str:
    return "".join(f'<img src="../{escape(path)}" width="{n}" height="{n}" alt="">' for n in (16, 24, 32))


cards = []
for item in entries:
    cards.append(f'''<article><div class="eyebrow">VERKENNER · {escape(item['id'])}</div><h3>{escape(item['label'])}</h3>
<div class="compare"><div><span>Pile Plan · CSS + SVG</span><div class="samples">{imgs(item['pile_svg'])}</div></div>
<div><span>Pointcloud · lokale SVG</span><div class="samples">{imgs(item['pointcloud_svg'])}</div></div></div>
<p>{escape(item['assessment'])}</p><div class="choice">Rust-keuze <strong>Pile Plan-vorm · ingebouwd</strong></div></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Verkenneracties · Pile Plan × Pointcloud</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f1}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(22px,calc((100vw - 1370px)/2))}header a{color:#ffc184}h1{font-size:29px;margin:12px 0 6px}header p{max-width:950px;color:#dddde3;margin:0}main{max-width:1410px;margin:auto;padding:22px}.note{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:22px}h2{font-size:20px;margin:0 0 12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(410px,1fr));gap:12px}article{background:white;border:1px solid #d9d9df;padding:17px}.eyebrow{font-size:11px;color:#a85706;letter-spacing:.06em}h3{margin:5px 0 14px;font-size:17px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:10px}.compare>div{border:1px solid #e0e0e4;background:#fafafa;padding:9px;min-width:0}.compare span{font-size:11px;color:#707078}.samples{display:flex;align-items:center;gap:13px;height:47px}.samples img{display:block}article p{min-height:38px;color:#676771}.choice{border-top:1px solid #e3e3e7;padding-top:8px;color:#767680;font-size:11px}.choice strong{float:right;color:#9d5304}.dark{background:#303039;margin-top:22px;padding:18px}.dark h2{color:white}.dark article{background:#42424b;border-color:#686872;color:white}.dark .compare>div{background:#393943;border-color:#60606a}.dark .compare span,.dark article p,.dark .choice{color:#c9c9d1}.dark .eyebrow,.dark .choice strong{color:#ffbd71}.dark .choice{border-color:#666670}.dark .compare img{filter:invert(1)}.dark .compare>div:nth-child(2) img{filter:grayscale(1) brightness(2.7)}footer{margin:24px 0;color:#777}footer a{color:#a55100}@media(max-width:550px){.grid{grid-template-columns:1fr}.compare{grid-template-columns:1fr}}
</style><header><a href="review.html">← Hoofdreview</a><h1>Vier verkenneracties · Pile Plan × Pointcloud</h1><p>Dezelfde opdrachten hadden verschillende SVG’s. Bronvormen op 16 / 24 / 32 px in Light en Forge; de gedeelde Rust-crate gebruikt nu de CSS-getrouwe Pile Plan-geometrie.</p></header><main><div class="note"><strong>Beoordeling.</strong> Dupliceren en Hernoemen zijn semantisch gelijk. Open en dicht zijn toestanden van dezelfde disclosure-knop; de naam van de pijl beschrijft de huidige toestand. De Pointcloud-bron heeft vaste blauwe/grijze kleuren; de gekozen monochrome vorm volgt de themakleur. Pointcloud tekent alle vier via de gedeelde Rust-crate. De knopmaat en hover/disabled-staten blijven in de betreffende app.</div>
'''
card_html = "".join(cards)
page += f'<section><h2>Light</h2><div class="grid">{card_html}</div></section><section class="dark"><h2>Forge</h2><div class="grid">{card_html}</div></section>'
page += '<footer><a href="pile-workarea-icon-review.html">Pile Plan-brongebruik</a> · <a href="pile-pointcloud-explorer-decisions.json">Beslisdata</a></footer></main></html>'
(ROOT / "design/pile-pointcloud-explorer-review.html").write_text(page)
print("4 cross-app explorer meanings reviewed at 16/24/32 px")
