#!/usr/bin/env python3
"""Compare source-used drawing commands across Geotechniek, OpenCAD and Pointcloud."""

import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO_COMMIT = "8182b48afc3f662e8d78650c7a1f21a7780d7e5f"
CAD_COMMIT = "77f19dafd01776947934e71563dd3d92a77c4f94"
PC_COMMIT = "cf209fe7a265aea7d692d710d70709c35b5b2b2c"
COMMANDS = (
    ("tekening-move", "Verplaatsen", "assets/icons/move.svg", "move.svg", "adopted-domain", "Object verplaatsen; Geotechniek gebruikt slepen, Pointcloud een translatiebediening. De iconbetekenis is gedeeld."),
    ("tekening-copy", "Kopiëren", "assets/icons/copy.svg", None, "decision", "Geotechniek dupliceert een geselecteerd tekenobject; toets OpenCAD's kopie-plaatsing apart."),
    ("tekening-rotate", "Roteren", "assets/icons/rotate.svg", None, "adopted-domain", "Rotatie van een geselecteerd object met opgegeven hoek; de Rust-vorm toont ook het te roteren object."),
    ("tekening-trim", "Trim", "assets/icons/trim.svg", None, "adopted-domain", "Lijn inkorten tegen een referentie; de Rust-vorm vereenvoudigt de knipvorm van de bron."),
    ("tekening-extend", "Extend", "assets/icons/extend.svg", None, "adopted-domain", "Lijn verlengen tot een grens; de pijl wijst naar de grenslijn."),
    ("tekening-mirror", "Mirror", "assets/icons/mirror.svg", None, "adopted-domain", "Object spiegelen langs een getekende as; de as blijft ook op 16 px zichtbaar."),
    ("tekening-offset", "Offset", "assets/icons/offset.svg", None, "adopted-domain", "Parallelle kopie van een lijn op afstand; twee lijnen en een maatpijl."),
    ("tekening-line", "Lijn", "assets/icons/line.svg", "annotation_line.svg", "adopted-domain", "Nieuwe lijn tekenen; Pointcloud noemt dit een annotatielijn. De iconbetekenis is gedeeld."),
    ("tekening-select", "Selecteren", "assets/icons/blocks/select_objects.svg", "select_objects.svg", "decision", "Geotechniek activeert selectiemodus; Pointcloud selecteert met een venster. Vorm en gebaar vragen scheiding."),
)
RUST_TARGETS = {"tekening-move": ("transform.move", "transform-move.svg"),
                "tekening-line": ("drawing.line", "drawing-line.svg"),
                "tekening-rotate": ("transform.rotate", "transform-rotate.svg"),
                "tekening-trim": ("drawing.trim", "drawing-trim.svg"),
                "tekening-extend": ("drawing.extend", "drawing-extend.svg"),
                "tekening-mirror": ("transform.mirror", "transform-mirror.svg"),
                "tekening-offset": ("drawing.offset", "drawing-offset.svg")}


def main() -> None:
    geo = {x["name"]: x for x in json.loads((ROOT / "harmonization/geotech-inline-ui-icons.json").read_text())["icons"]}
    cad = {x.get("path"): x for x in json.loads((ROOT / "harmonization/asset-index.json").read_text())
           if x.get("repo") == "OpenCADStudio" and x.get("category") == "ui-used"}
    pc = {x.get("path"): x for x in json.loads((ROOT / "harmonization/asset-index.json").read_text())
          if x.get("repo") == "open-pointcloud-studio" and x.get("category") == "ui-used"}
    records = []
    for name, label, cad_path, pc_file, status, decision in COMMANDS:
        item, cad_item = geo[name], cad[cad_path]
        geo_file = ROOT / "harmonization" / item["svg"]
        cad_file = ROOT / "harmonization/ui-icons/OpenCADStudio" / cad_path
        assert hashlib.sha256(geo_file.read_bytes()).hexdigest() == item["sha256"]
        assert hashlib.sha256(cad_file.read_bytes()).hexdigest() == cad_item["sha256"]
        assert cad_item["ui_references"], cad_path
        pointcloud = None
        if pc_file:
            pc_path = "native/assets/opencad-icons/" + pc_file
            pc_item = pc[pc_path]
            pc_file_path = ROOT / "harmonization/ui-icons/open-pointcloud-studio" / pc_path
            assert hashlib.sha256(pc_file_path.read_bytes()).hexdigest() == pc_item["sha256"]
            pointcloud = {"path": pc_path, "svg": "../harmonization/ui-icons/open-pointcloud-studio/" + pc_path,
                          "sha256": pc_item["sha256"], "usage": pc_item["ui_references"], "commit": PC_COMMIT}
        target = None
        if name in RUST_TARGETS:
            meaning, filename = RUST_TARGETS[name]
            large = ROOT / "crates/openaec-ui/assets/domain-icons" / filename
            small = ROOT / "crates/openaec-ui/assets/domain-icons-small" / filename
            assert large.exists() and small.exists()
            target = {"meaning": meaning, "large": "../crates/openaec-ui/assets/domain-icons/" + filename,
                      "small": "../crates/openaec-ui/assets/domain-icons-small/" + filename}
        records.append({"name": name, "label": label, "status": status, "decision": decision,
                        "geotechniek": {"source": item["source"], "line": item["usage_lines"][0], "commit": GEO_COMMIT,
                                         "svg": "../harmonization/" + item["svg"], "sha256": item["sha256"]},
                        "opencad": {"path": cad_path, "svg": "../harmonization/ui-icons/OpenCADStudio/" + cad_path,
                                    "sha256": cad_item["sha256"], "usage": cad_item["ui_references"], "commit": CAD_COMMIT},
                        "pointcloud": pointcloud, "rust": target})
    (ROOT / "design/geotech-cad-command-review.json").write_text(json.dumps({"commands": records}, ensure_ascii=False, indent=2) + "\n")

    def sample(src: str) -> str:
        return ''.join(f'<img src="{escape(src)}" width="{n}" height="{n}" alt="">' for n in (16, 24, 32))

    sections = []
    for dark in (False, True):
        cards = []
        for r in records:
            geo, cad, pc = r["geotechniek"], r["opencad"], r["pointcloud"]
            geolink = f'https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/{GEO_COMMIT}/{geo["source"]}#L{geo["line"]}'
            cadline = cad["usage"][0]
            cadlink = f'https://github.com/HakanSeven12/OpenCADStudio/blob/{CAD_COMMIT}/{cadline["source"]}#L{cadline["line"]}'
            panels = [f'<div class="source geo"><b>Geotechniek</b><div>{sample(geo["svg"])}</div><a href="{geolink}">UI-gebruik ↗</a></div>',
                      f'<div class="source"><b>OpenCAD</b><div>{sample(cad["svg"])}</div><a href="{cadlink}">UI-gebruik ↗</a></div>']
            if pc:
                pcline = pc["usage"][0]
                pclink = f'https://github.com/OpenAEC-Foundation/open-pointcloud-studio/blob/{PC_COMMIT}/{pcline["source"]}#L{pcline["line"]}'
                panels.append(f'<div class="source"><b>Pointcloud</b><div>{sample(pc["svg"])}</div><a href="{pclink}">UI-asset ↗</a></div>')
            if r["rust"]:
                target = r["rust"]
                target_images = f'<img src="{escape(target["small"])}" width="16" height="16" alt=""><img src="{escape(target["large"])}" width="24" height="24" alt=""><img src="{escape(target["large"])}" width="32" height="32" alt="">'
                label = "Rust" if r["status"] == "adopted-domain" else "Voorstel"
                panels.append(f'<div class="source rust"><b>{label} · {escape(target["meaning"])}</b><div>{target_images}</div><span>16 px eigen vorm · 24/32 px gedeeld</span></div>')
            cards.append(f'<article><h3>{escape(r["label"])} <small>{escape(r["status"])}</small></h3><p>{escape(r["decision"])}</p><div class="sources">' + ''.join(panels) + '</div></article>')
        sections.append(f'<section class="{"dark" if dark else "light"}"><h2>{"Donker" if dark else "Licht"}</h2><div class="grid">' + ''.join(cards) + '</div></section>')
    html = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geotechniek · CAD-tekenacties</title><style>
:root{font:13px/1.4 Inter,system-ui,sans-serif;color:#303039;background:#f3f3f2}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(24px,calc((100vw - 1400px)/2))}h1{font-size:28px;margin:10px 0 7px}header p{color:#e2e2e7;max-width:950px;margin:0}header a{color:#ffc17a}main{max-width:1500px;margin:auto;padding:22px}section{padding:18px;margin:0 0 20px;border:1px solid #d6d6db}section.light{background:#fff}section.dark{background:#303039;color:#fafafa;border-color:#66666e}h2{font-size:20px;margin:0 0 12px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:12px}article{border:1px solid #d6d6db;padding:12px;min-width:0}.dark article{border-color:#66666f}h3{font-size:15px;margin:0 0 7px}h3 small{font-size:10px;color:#945000;font-weight:500;margin-left:8px}.dark h3 small{color:#ffc17a}article>p{margin:0 0 10px;min-height:36px;color:#686873}.dark article>p{color:#ceced6}.sources{display:flex;gap:8px}.source{flex:1;min-width:0;border:1px solid #dedee2;padding:8px}.dark .source{border-color:#66666f;background:#414149}.source b{display:block;font-size:11px;margin-bottom:7px}.source img{vertical-align:middle;margin-right:8px}.source a,.source span{display:block;margin-top:9px;color:#a65500;font-size:11px}.dark .source a,.dark .source span{color:#ffc17a}.dark .geo img,.dark .rust img{filter:invert(1)}.dark .source:not(.geo):not(.rust) img{filter:grayscale(1) brightness(1.8)}@media(max-width:700px){.grid{grid-template-columns:1fr}.sources{flex-wrap:wrap}.source{min-width:130px}}
</style><header><a href="review.html">← Hoofdreview</a><h1>Geotechniek · CAD-tekenacties</h1><p>Negen werkelijk aangesloten tekencommando’s naast UI-gebruikte OpenCAD-vectoren; waar aanwezig ook de Pointcloud-vorm. Zeven bewerkingen hebben na beoordeling een Rust-domeinvorm. Kopiëren en Selecteren vragen een betekenisbesluit.</p></header><main><p>Alle bronbestanden zijn tegen SHA-256 op vastgelegde commits gecontroleerd. De bronvormen staan op 16, 24 en 32 px in licht en donker. Ruwe OpenCAD-assets zijn geen canonieke Rust-vormen; de apart gemarkeerde Rust-tekeningen zijn brongeïnformeerde harmonisaties.</p>'''
    html += ''.join(sections) + '<p><a href="geotech-cad-command-review.json">Gestructureerde bron- en beslisdata</a> · <a href="geotech-icon-crosswalk.html">Geotechniek-kruisverwijzing</a></p></main></html>'
    (ROOT / "design/geotech-cad-command-review.html").write_text(html)
    print("Geotechniek/CAD command review:", len(records), "commands")


if __name__ == "__main__":
    main()
