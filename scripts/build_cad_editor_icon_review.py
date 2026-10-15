#!/usr/bin/env python3
"""Review newly source-proven OpenCAD text-editor and start-page SVG icons."""
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "design"
A = ROOT / "harmonization"
commit = json.loads((A / "repositories/OpenCADStudio.json").read_text())["commit"]

labels = {
    "mt_bold": "Vet", "mt_italic": "Cursief", "mt_underline": "Onderstrepen",
    "mt_overline": "Bovenstrepen", "mt_strike": "Doorhalen", "mt_upper": "Hoofdletters",
    "mt_lower": "Kleine letters", "mt_align_left": "Tekst links",
    "mt_align_center": "Tekst centreren", "mt_align_right": "Tekst rechts",
    "mt_align_justify": "Tekst uitvullen", "reddit": "Communitylink",
}
items = [x for x in json.loads((A / "asset-index.json").read_text())
         if x["repo"] == "OpenCADStudio" and Path(x["path"]).stem in labels]
assert len(items) == 12
assert all(x["category"] == "ui-used" and x["evidence_type"] == "direct-path" for x in items)
assert all(x["ui_references"][0]["source"] in ("src/app/view/overlay.rs", "src/app/view/mod.rs") for x in items)
assert {Path(x["path"]).stem for x in items} == set(labels)
cards = []
for item in sorted(items, key=lambda x: x["path"]):
    stem = Path(item["path"]).stem
    ref = item["ui_references"][0]
    asset = "../harmonization/ui-icons/OpenCADStudio/" + quote(item["path"])
    assert (A / "ui-icons/OpenCADStudio" / item["path"]).is_file()
    source = "https://github.com/HakanSeven12/OpenCADStudio/blob/" + commit + "/" + quote(ref["source"]) + f'#L{ref["line"]}'
    samples = "".join(
        f'<span class="sample"><img src="{asset}" width="{size}" height="{size}" alt="">{size} px</span>'
        for size in (16, 24, 32)
    ) + f'<span class="sample dark{" colored" if stem == "reddit" else ""}"><img src="{asset}" width="16" height="16" alt="">donker</span>'
    cards.append(f'<article><h2>{html.escape(labels[stem])}</h2><code>{html.escape(stem)}</code>'
                 f'<div class="samples">{samples}</div><a href="{html.escape(source, quote=True)}">UI-bronregel ↗</a>'
                 f'<p>{"Startpagina: communitylink" if stem == "reddit" else "MText-editor: opmaakopdracht"}</p></article>')

page = f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · aanvullende OpenCAD UI-iconen</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f2f3f5;color:#303039;font:13px/1.45 Inter,system-ui,sans-serif}}header{{background:#303039;color:white;padding:25px max(22px,calc((100vw - 1200px)/2));border-bottom:3px solid #d97706}}header a{{color:#ffc278}}h1{{font-size:27px;margin:5px 0}}header p{{max-width:920px;color:#dedee2;margin:0}}main{{max-width:1240px;margin:auto;padding:22px}}.note{{background:white;border-left:3px solid #d97706;padding:13px 16px;margin-bottom:18px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(275px,1fr));gap:12px}}article{{background:white;border:1px solid #d8d8de;padding:14px}}h2{{font-size:16px;margin:0}}code{{color:#63636d}}.samples{{display:flex;gap:5px;margin:13px 0;flex-wrap:wrap}}.sample{{width:57px;height:62px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;background:#f4f5f7;font-size:10px}}.sample.dark{{background:#303039;color:white}}.sample.dark:not(.colored) img{{filter:brightness(0) invert(1)}}article a,main a{{color:#a85000}}article p{{font-size:11px;color:#65656e;margin:9px 0 0}}
</style><header><a href="review.html">← Hoofdreview</a><h1>Twaalf herontdekte OpenCAD UI-iconen</h1><p>De gepinde bron bevat elf knoppen van de MText-editor en één communityknop op de startpagina. Een eerdere codeaudit sloeg <code>src/app/view/</code> over; de hernieuwde audit bewijst hun UI-gebruik.</p></header><main><div class="note">Alle twaalf SVG's blijven onderzoeksassets en worden niet automatisch canonieke Rust-iconen. <code>mt_align_*</code> bestuurt alinea-uitlijning; de naam is geen bewijs voor dezelfde BIM-uitlijnactie. De oorspronkelijke MText-lijnkleur #B4B6B9 haalt op deze lichte proefachtergrond slechts circa 1,86:1 contrast; de vorm moet bij migratie thematisch worden gekleurd. In de donkere proef krijgen alleen de monochrome pictogrammen een witte tint; de Reddit-merkleur blijft origineel.</div><div class="grid">{''.join(cards)}</div><p class="note"><a href="icon-review-board.html">Alle 577 bronbewezen UI-bestanden</a> · <a href="domain-candidate-review.html">FEM/BIM-betekenisvergelijking</a></p></main></html>'''
(D / "cad-editor-icon-review.html").write_text(page)
print("Reviewed", len(items), "source-linked OpenCAD UI SVGs")
