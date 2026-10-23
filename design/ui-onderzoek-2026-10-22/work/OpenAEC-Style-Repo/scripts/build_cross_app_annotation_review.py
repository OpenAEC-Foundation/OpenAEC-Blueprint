#!/usr/bin/env python3
"""Review two annotation commands used in Geotechniek and Pointcloud."""

import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO_COMMIT = "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"
PC_COMMIT = "cf209fe7a265aea7d692d710d70709c35b5b2b2c"
PAIRS = (
    ("dimension", "Maatlijn / Dimension", "tekening-dimension", "annotation_dimension.svg", "drawing-dimension.svg"),
    ("note", "Opmerking / Note", "tekening-note", "annotation_note.svg", "drawing-note.svg"),
)


def main() -> None:
    geotech = {x["name"]: x for x in json.loads((ROOT / "harmonization/geotech-inline-ui-icons.json").read_text())["icons"]}
    pointcloud = {Path(x.get("path", "")).name: x for x in json.loads((ROOT / "harmonization/asset-index.json").read_text())
                  if x.get("repo") == "open-pointcloud-studio" and x.get("path", "").startswith("native/assets/opencad-icons/")}
    records = []
    for slug, label, geo_name, pc_name, rust_name in PAIRS:
        geo, pc = geotech[geo_name], pointcloud[pc_name]
        geo_path = ROOT / "harmonization" / geo["svg"]
        pc_path = ROOT / "harmonization/ui-icons/open-pointcloud-studio/native/assets/opencad-icons" / pc_name
        large = ROOT / "crates/openaec-ui/assets/domain-icons" / rust_name
        small = ROOT / "crates/openaec-ui/assets/domain-icons-small" / rust_name
        assert hashlib.sha256(geo_path.read_bytes()).hexdigest() == geo["sha256"]
        assert hashlib.sha256(pc_path.read_bytes()).hexdigest() == pc["sha256"]
        assert all(path.exists() for path in (large, small))
        records.append({
            "meaning": f"drawing.{slug}", "label": label,
            "geotechniek": {"commit": GEO_COMMIT, "source": geo["source"], "usage_lines": geo["usage_lines"],
                            "sha256": geo["sha256"], "svg": "../harmonization/" + geo["svg"]},
            "pointcloud": {"commit": PC_COMMIT, "source": pc["path"], "sha256": pc["sha256"],
                           "svg": "../harmonization/ui-icons/open-pointcloud-studio/" + pc["path"],
                           "usage": "native/desktop/src/main.rs · ToolIcon::" + slug.title()},
            "rust": {"large": "../crates/openaec-ui/assets/domain-icons/" + rust_name,
                     "small": "../crates/openaec-ui/assets/domain-icons-small/" + rust_name},
        })
    (ROOT / "design/cross-app-annotation-review.json").write_text(json.dumps({"icons": records}, ensure_ascii=False, indent=2) + "\n")

    def samples(paths: list[str]) -> str:
        return ''.join(f'<img src="{escape(path)}" width="{size}" height="{size}" alt="">'
                       for path, size in zip(paths, (16, 24, 32)))

    panels = []
    for dark in (False, True):
        cards = []
        for item in records:
            geo, pc, rust = item["geotechniek"], item["pointcloud"], item["rust"]
            geolink = f'https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{GEO_COMMIT}/{geo["source"]}#L{geo["usage_lines"][0]}'
            pclink = f'https://github.com/OpenAEC-Foundation/open-pointcloud-studio/blob/{PC_COMMIT}/{pc["source"]}'
            cards.append(f'''<article><h3>{escape(item["label"])} <code>{escape(item["meaning"])}</code></h3><div class="sources">
<div class="source geo"><b>Geotechniek · bron</b>{samples([geo["svg"]]*3)}<a href="{geolink}">RibbonButton-bron ↗</a></div>
<div class="source pointcloud"><b>Pointcloud · bron</b>{samples([pc["svg"]]*3)}<a href="{pclink}">Asset op vastgelegde commit ↗</a></div>
<div class="source rust"><b>Rust · gedeeld domeinicoon</b>{samples([rust["small"],rust["large"],rust["large"]])}<span>16 px eigen tekening · 24/32 px gedeelde vorm</span></div>
</div></article>''')
        panels.append(f'<section class="{"dark" if dark else "light"}"><h2>{"Donker" if dark else "Licht"}</h2>' + ''.join(cards) + '</section>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · gedeelde tekeniconen</title><style>
:root{font:14px/1.45 Inter,system-ui,sans-serif;color:#303039;background:#f2f2f3}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:white;border-bottom:3px solid #d97706;padding:24px max(24px,calc((100vw - 1300px)/2))}header a{color:#ffc17a}h1{font-size:28px;margin:10px 0 7px}header p{max-width:900px;color:#e4e4e7;margin:0}main{max-width:1400px;margin:auto;padding:24px}section{padding:20px;margin-bottom:20px;border:1px solid #d8d8dd}section.light{background:white}section.dark{background:#303039;color:#f6f6f7;border-color:#55555f}h2{font-size:20px;margin:0 0 15px}article{border:1px solid #d9d9dd;padding:15px;margin-bottom:13px}article:last-child{margin-bottom:0}.dark article{border-color:#63636c}h3{font-size:16px;margin:0 0 12px}h3 code{font-size:12px;color:#a45600;margin-left:8px}.dark h3 code{color:#ffc17a}.sources{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.source{border:1px solid #dddde1;padding:12px;min-width:0}.dark .source{border-color:#666670;background:#404049}.source b{display:block;font-size:12px;margin-bottom:10px}.source img{vertical-align:middle;margin-right:16px}.source a,.source span{display:block;font-size:11px;margin-top:12px;color:#a45600}.dark .source a,.dark .source span{color:#ffc17a}.dark .geo img,.dark .rust img{filter:invert(1)}.dark .pointcloud img{filter:none}main>p{line-height:1.6}@media(max-width:800px){.sources{grid-template-columns:1fr}}
</style><header><a href="review.html">← Hoofdreview</a><h1>Tekeniconen · twee tools, één betekenis</h1><p>Maatlijn en Opmerking zijn concrete UI-opdrachten in Geotechniek en Pointcloud. De bronvormen verschillen; de Rust-domeiniconen geven beide applicaties dezelfde vorm. Vergelijk de leesbaarheid op 16, 24 en 32 px in licht en donker.</p></header><main><p>De Pointcloud-bronvormen bevatten vaste amber/grijze kleuren en bij Opmerking een donker gevuld vlak. Die ruwe vormen verliezen op een donkere ondergrond contrast. De geharmoniseerde Rust-vormen worden in beide native apps thematisch getint. De punten hieronder beoordelen de vorm; daadwerkelijke klikacties blijven bij de applicatie.</p>'''
    html += ''.join(panels) + '<p><a href="cross-app-annotation-review.json">Provenance, SHA-256 en doelassets</a> · <a href="geotech-icon-crosswalk.html">Alle Geotechniek-betekenissen</a></p></main></html>'
    (ROOT / "design/cross-app-annotation-review.html").write_text(html)
    print("Cross-app annotation review:", len(records), "shared domain meanings")


if __name__ == "__main__":
    main()
