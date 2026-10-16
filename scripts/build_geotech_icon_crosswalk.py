#!/usr/bin/env python3
"""Crosswalk every proven Geotechniek UI vector to a semantic decision."""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEXES = (
    "geotech-inline-ui-icons.json",
    "geotech-backstage-ui-icons.json",
    "geotech-chrome-ui-icons.json",
)
SHARED = {
    "start-zoom-out": "zoomout", "start-zoom-fit": "fit", "start-settings": "settings",
    "kaart-measure": "measure",
    "backstage-new": "new", "backstage-open": "open", "backstage-save": "save",
    "backstage-export": "export", "backstage-import": "import",
    "backstage-preferences": "settings", "backstage-extensions": "extensions",
    "title-save": "save", "title-undo": "undo", "title-redo": "redo",
    "title-settings": "settings", "window-minimize": "minimize",
    "window-maximize": "maximize", "window-close": "close", "document-close": "close",
}
NEW_SHARED = {
    "tekening-print": "print", "backstage-print": "print", "title-print": "print",
    "backstage-save-as": "save-as", "window-restore": "restore",
}
DECISION = {
    "rapport-open": ("report.open-system-viewer", "Genereert een tijdelijk PDF-rapport en opent dat in de systeemviewer; de gedeelde Open-map betekent een bestand kiezen."),
    "tekening-delete": ("geotech.delete-selection / geotech.clear-all", "Eén prullenbakvorm heeft twee knopaanroepen met verschillende reikwijdte; Wis alles vraagt een eigen betekenis en vorm."),
    "document-add": ("document.open", "De plusvorm opent Bestand; deze handeling moet tegen Nieuw document en Open document worden beoordeeld."),
    "rapport-download": ("report.export-pdf", "De pijl omlaag zegt downloaden; bepaal of PDF-export dezelfde generieke Export-betekenis krijgt."),
    "backstage-about": ("app.about", "Informatie over de app is niet dezelfde actie als de bestaande Help-vraagtekenknop."),
    "backstage-exit": ("app.exit", "De app afsluiten is niet hetzelfde als een document of dialoog sluiten."),
    "document-file": ("document.type-file", "Deze vorm duidt een documenttype aan, geen opdracht Nieuw document."),
    "document-folder": ("document.type-project", "Deze map duidt het projecttype aan, geen opdracht Open map."),
}
DOMAIN = {
    "kaart-export-image", "tekening-sondering", "tekening-bore", "tekening-overlay",
    "tekening-frame", "tekening-raster", "tekening-tag", "tekening-move",
    "tekening-quotes", "tekening-dwg", "tekening-export-pdf", "tekening-rotate",
    "tekening-copy", "tekening-select", "tekening-line", "tekening-vlak",
    "tekening-note", "tekening-dimension", "tekening-trim", "tekening-extend",
    "tekening-mirror", "tekening-offset",
}
LABELS = {
    "shared": "Gedeelde kernbetekenis",
    "new-shared": "Nieuw in de gedeelde Rust-kern",
    "decision": "Betekenisbesluit nodig",
    "domain": "Domein- of bestandstypevorm",
}


def main() -> None:
    sources = []
    for index in INDEXES:
        data = json.loads((ROOT / "harmonization" / index).read_text())
        assert data["commit"] == "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"
        sources.extend(data["icons"])
    names = {item["name"] for item in sources}
    assert len(sources) == len(names) == 54
    decisions = set(SHARED) | set(NEW_SHARED) | set(DECISION) | DOMAIN
    assert names == decisions, (sorted(names - decisions), sorted(decisions - names))
    assert sum(map(len, (SHARED, NEW_SHARED, DECISION, DOMAIN))) == len(names)
    records = []
    for item in sources:
        name = item["name"]
        if name in SHARED:
            status, meaning, why = "shared", SHARED[name], "Gedeelde handeling; canonieke vorm bestaat al."
            target = f"../crates/openaec-ui/assets/icons/{meaning.replace('-', '')}.svg"
        elif name in NEW_SHARED:
            status, meaning, why = "new-shared", NEW_SHARED[name], "Na licht/donker-review opgenomen als algemene Rust-kernvorm."
            target = f"../crates/openaec-ui/assets/icons/{meaning.replace('-', '')}.svg"
        elif name in DECISION:
            status, (meaning, why) = "decision", DECISION[name]
            target = None
        else:
            status, meaning, why = "domain", "geotech." + name, "Behoud eigen betekenis; harmoniseer raster en lijnvoering vóór opname."
            target = None
        if target:
            assert (ROOT / "design" / target).exists(), target
        records.append({
            "name": name, "status": status, "meaning": meaning,
            "decision": why, "source": item["source"],
            "source_line": item["source_line"], "usage_lines": item["usage_lines"],
            "source_sha256": item["sha256"], "source_svg": item["svg"],
            "candidate_svg": target,
        })
    output = {"repository": "open-geotechniek-studio", "commit": "8182b48afc3f662e8d78650c7a1f21a7780d7e5f",
              "count": len(records), "counts": {key: sum(r["status"] == key for r in records) for key in LABELS},
              "icons": records}
    (ROOT / "design/geotech-icon-crosswalk.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    sections = []
    for status, label in LABELS.items():
        cards = []
        for item in (record for record in records if record["status"] == status):
            source = "../harmonization/" + item["source_svg"]
            target = item["candidate_svg"]
            ref = f"https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{output['commit']}/{item['source']}#L{item['usage_lines'][0]}"
            sample = lambda path: ''.join(f'<img src="{escape(path)}" width="{size}" height="{size}" alt="">' for size in (16, 24, 32))
            comparison = f'<div class="candidate"><span>Canoniek · {escape(item["meaning"])}</span><div class="samples">{sample(target)}</div></div>' if target else f'<div class="candidate text"><span>Betekenis · {escape(item["meaning"])}</span><p>{escape(item["decision"])}</p></div>'
            note = f'<p>{escape(item["decision"])}</p>' if target else ''
            cards.append(f'<article data-search="{escape((item["name"] + " " + item["meaning"]).lower())}"><h3>{escape(item["name"])}</h3><div class="pair"><div><span>Bron</span><div class="samples">{sample(source)}</div></div>{comparison}</div>{note}<a href="{ref}">UI-gebruik ↗</a></article>')
        sections.append(f'<section id="{status}"><h2>{label} <small>{sum(r["status"] == status for r in records)}</small></h2><div class="grid">' + ''.join(cards) + '</div></section>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · icoonharmonisatie</title><style>
:root{font:13px/1.45 Inter,system-ui,sans-serif;color:#33343b;background:#f3f3f2}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;padding:22px max(22px,calc((100vw - 1450px)/2));border-bottom:3px solid #d97706}header a{color:#ffc17a}h1{font-size:28px;margin:11px 0 7px}header p{max-width:1000px;color:#e0e0e4;margin:0}nav{display:flex;gap:9px;flex-wrap:wrap;margin:0 0 19px}nav a{background:white;padding:6px 9px;border:1px solid #d5d5d9;color:#9a5100;text-decoration:none}main{max-width:1490px;margin:auto;padding:22px}input{padding:8px 10px;border:1px solid #a9a9b0;width:270px;max-width:100%;font:inherit;margin-bottom:15px}h2{font-size:19px;border-bottom:1px solid #d4d4d8;padding-bottom:6px;margin:29px 0 12px}h2 small{font-size:12px;color:#777;margin-left:5px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(325px,1fr));gap:12px}article{background:#fff;border:1px solid #d6d6db;padding:12px;min-width:0}article h3{font-size:14px;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair>div{min-width:0;border:1px solid #e0e0e4;background:#fafafa;padding:7px}.pair span{display:block;font-size:11px;color:#717179;min-height:31px}.samples{display:flex;align-items:center;gap:12px;height:39px}.samples img{display:block}.candidate.text p{font-size:11px;margin:3px 0 0}.pair>div.candidate.text{background:#fff7ed}article>p{color:#686873;min-height:39px;margin:10px 0 6px}article a{color:#a45600}.dark{background:#303039;padding:15px;margin-top:15px}.dark h2{color:#f4f4f5;border-color:#676772}.dark h2 small{color:#c2c2ca}.dark article{background:#3d3d45;border-color:#676772;color:#fff}.dark .pair>div{background:#46464f;border-color:#676772}.dark .pair span,.dark article>p{color:#c6c6cc}.dark img{filter:invert(1)}.dark article a{color:#ffbb6d}.hidden{display:none!important}
</style><header><a href="review.html">← Hoofdreview</a><h1>Geotechniek · icoonharmonisatie</h1><p>Alle 54 bronbewezen UI-vormen uit lint, Bestand, titelbalk en documenttabs krijgen een expliciete betekenis. De Rust-kern is de doelvorm voor gedeelde handelingen; Print, Opslaan als en Herstellen zijn na visuele review toegevoegd. Domeinvormen blijven gescheiden van algemene bediening.</p></header><main><nav><a href="#shared">Gedeeld</a><a href="#new-shared">Nieuw in Rust</a><a href="#decision">Besluit nodig</a><a href="#domain">Domein</a></nav><label for="search">Zoek op bronvorm of betekenis</label><br><input id="search" type="search" placeholder="Bijv. delete, print, boring"><p>Elke bronvorm en eventuele doelvorm staat op 16, 24 en 32 px. De onderste donkere ronde maakt contrastproblemen zichtbaar. Alleen de expliciet aangeduide algemene kernvormen staan in de crate; de rest blijft bron- of ontwerpmateriaal.</p><h2>Licht</h2>'''
    dark_sections = [section.replace(f'id="{status}"', f'id="dark-{status}"', 1) for status, section in zip(LABELS, sections)]
    html += ''.join(sections) + '<h2>Donker</h2><div class="dark">' + ''.join(dark_sections) + '</div><p><a href="geotech-icon-crosswalk.json">Gestructureerde beslisdata</a> · <a href="geotech-inline-icon-review.html">Lintbronvormen</a> · <a href="geotech-backstage-icon-review.html">Bestandbronvormen</a> · <a href="geotech-chrome-icon-review.html">Titel- en documentbronvormen</a></p></main><script>const q=document.getElementById("search");function filter(){let v=q.value.trim().toLowerCase();for(let card of document.querySelectorAll("article"))card.classList.toggle("hidden",!!v&&!card.dataset.search.includes(v));for(let section of document.querySelectorAll("section"))section.classList.toggle("hidden",!!v&&!section.querySelector("article:not(.hidden)"))}q.addEventListener("input",filter);q.value=new URLSearchParams(location.search).get("q")||"";filter();</script></html>'
    (ROOT / "design/geotech-icon-crosswalk.html").write_text(html)
    print("Crosswalk:", output["counts"])


if __name__ == "__main__":
    main()
