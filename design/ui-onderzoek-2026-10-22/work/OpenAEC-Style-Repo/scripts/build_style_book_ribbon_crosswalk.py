#!/usr/bin/env python3
"""Record the semantic migration decisions for source-used Style Book commands."""
import json
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "harmonization/style-book-tauri-ribbon-ui-icons.json").read_text())

core = {"undoIcon": "Icon::Undo", "redoIcon": "Icon::Redo", "helpIcon": "Icon::Help", "settingsIcon": "Icon::Settings"}
existing_domain = {"lineIcon": "DomainIcon::DrawingLine"}
new_domain = {
    "projectIcon": "ProjectSettings", "pasteIcon": "ClipboardPaste",
    "cutIcon": "ClipboardCut", "copyIcon": "ClipboardCopy",
    "boldIcon": "TextBold", "italicIcon": "TextItalic", "underlineIcon": "TextUnderline",
    "alignLeftIcon": "TextAlignLeft", "alignCenterIcon": "TextAlignCenter", "alignRightIcon": "TextAlignRight",
    "pencilIcon": "DrawingPencil", "arrowIcon": "DrawingArrow", "circleIcon": "DrawingCircle",
    "rectangleIcon": "DrawingRectangle", "imageIcon": "InsertImage", "tableIcon": "InsertTable",
    "linkIcon": "InsertLink", "infoIcon": "ApplicationAbout",
    "ifcImportIcon": "IfcImport", "ifcExportIcon": "IfcExport", "ifcTreeIcon": "IfcStructure",
    "ifcStatsIcon": "IfcStatistics", "ifcValidateIcon": "IfcValidate",
    "reportNewIcon": "ReportNew", "reportTemplateIcon": "ReportTemplate",
    "reportGenerateIcon": "ReportGenerate", "downloadIcon": "ReportDownloadPdf",
    "a4Icon": "ReportPageA4", "a3Icon": "ReportPageA3",
    "portraitIcon": "ReportPortrait", "landscapeIcon": "ReportLandscape",
    "reportCoverIcon": "ReportCover",
}
special = {"reportPreviewIcon"}
assert (set(core) | set(existing_domain) | set(new_domain) | special) == {i["name"] for i in source["icons"]}

records = []
for icon in source["icons"]:
    name = icon["name"]
    if name in core:
        status, target, reason = "gedeelde kandidaat", core[name], "Zelfde handeling; behoud één Rust-variant na controle van kleine maat en context."
    elif name in existing_domain:
        status, target, reason = "bestaande domeinkandidaat", existing_domain[name], "De tekenhandeling bestaat al in de crate; vergelijk lijnhoek en knopmaat vóór overzetting."
    elif name in new_domain:
        status, target, reason = "nieuw domeincommando", f"RibbonIcon::{new_domain[name]}", "Eigen getypeerde Rust-lintvorm; de opdrachtlogica blijft bij de betreffende applicatie."
    else:
        status, target, reason = "bronfout vervangen", "Icon::SaveAs", "De knop voert Opslaan als uit maar toont een oog; gebruik de al beoordeelde SaveAs-vorm in de Rust-implementatie."
    if name == "copyIcon":
        reason = "Klembord-Kopiëren is geen document-Dupliceren; beide hebben overlappende bladen maar houden aparte semantische IDs."
    if name == "infoIcon":
        reason = "Over deze app is geen Hulp-actie; gebruik niet de bestaande Help-variant."
    if name in ("ifcImportIcon", "ifcExportIcon"):
        reason = "IFC-bestandsactie; houd het bestandstype in de commandosemantiek, ook als de pijl familiegelijkenis heeft met generieke import/export."
    ribbon_asset = None
    if name in new_domain:
        import re
        filename = re.sub(r"(?<!^)(?=[A-Z])", "-", new_domain[name]).lower() + ".svg"
        ribbon_asset = f"../crates/openaec-ui/assets/ribbon-icons/{filename}"
    records.append({"name": name, "tab": icon["tab"], "status": status, "target": target,
                    "rationale": reason, "source_svg": icon["svg"],
                    "source_file": icon["usage_file"], "source_line": icon["usage_line"],
                    "ribbon_asset": ribbon_asset,
                    "vector_implemented": bool(ribbon_asset and (ROOT / "design" / ribbon_asset).is_file()),
                    "app_command_integrated": False})

counts = dict(Counter(i["status"] for i in records))
(ROOT / "design/style-book-tauri-ribbon-crosswalk.json").write_text(json.dumps({
    "source_index": "../harmonization/style-book-tauri-ribbon-ui-icons.json",
    "commit": source["commit"], "count": len(records), "status_counts": counts, "decisions": records,
}, ensure_ascii=False, indent=2) + "\n")

cards = []
for x in records:
    url = f"https://github.com/OpenAEC-Foundation/OpenAEC-style-book/blob/{source['commit']}/{x['source_file']}#L{x['source_line']}"
    built = " · Rust-vector gereed" if x["vector_implemented"] else ""
    cards.append(f'''<article data-status="{escape(x['status'])}" data-tab="{escape(x['tab'])}"><div class="top"><img src="../harmonization/{escape(x['source_svg'])}" width="28" height="28" alt=""><div><small>{escape(x['tab'])}</small><h3>{escape(x['name'])}</h3></div></div><span class="badge">{escape(x['status'] + built)}</span><p><strong>{escape(x['target'])}</strong><br>{escape(x['rationale'])}</p><a href="{escape(url)}">Bronaanroep ↗</a></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Style Book Tauri · Rust-kruisverwijzing</title><style>
:root{font:13px/1.5 Inter,system-ui,sans-serif;background:#f2f2f1;color:#303039}*{box-sizing:border-box}body{margin:0}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(22px,calc((100vw - 1370px)/2))}header a{color:#ffc184}h1{font-size:29px;margin:10px 0 5px}header p{max-width:970px;color:#dddde3;margin:0}main{max-width:1410px;margin:auto;padding:22px}.note{background:#fff8ee;border-left:3px solid #d97706;padding:12px 15px;margin-bottom:20px}.summary{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}.summary span{background:white;border:1px solid #dadadf;padding:8px 12px}.summary strong{color:#a55200}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}article{background:white;border:1px solid #d9d9df;padding:15px;display:flex;flex-direction:column;min-height:230px}.top{display:flex;align-items:center;gap:11px;min-height:44px}.top img{flex:0 0 28px}.top small{color:#aa620f}.top h3{font-size:14px;margin:1px 0}.badge{align-self:flex-start;background:#fff2e1;border:1px solid #e9c391;color:#91500b;font-size:10px;padding:3px 7px;margin:10px 0 0}article p{color:#686873;font-size:12px;flex:1}article p strong{color:#303039;font:11px ui-monospace,monospace}article a,footer a{color:#a55100;font-size:11px}footer{margin:22px 0;color:#777}
</style><header><a href="style-book-tauri-ribbon-icon-review.html">← Bronvormen</a><h1>38 Tauri-lintopdrachten → Rust-semantiek</h1><p>Per daadwerkelijk aangeroepen knop staat vast of een bestaande gedeelde vorm past, een eigen getypeerd domeinicoon nodig is, of de bronbetekenis eerst gecorrigeerd moet worden.</p></header><main><div class="note"><strong>Ontwerpbesluit.</strong> Klembord-Kopiëren blijft gescheiden van document-Dupliceren; Over van Hulp; IFC-import/export van generieke bestandsacties. Instellingen gebruikt nu een tandwiel, Beeldregelaars een eigen Controls-vorm. Report ‘Opslaan als’ krijgt in Rust de bestaande SaveAs-vorm in plaats van het bron-oog. De 32 eigen vectoren staan nu in de getypeerde Rust-crate; de opdrachtlogica en schermen zijn nog niet allemaal naar Rust overgezet.</div>
'''
page += '<div class="summary">' + "".join(f'<span><strong>{n}</strong> {escape(k)}</span>' for k,n in counts.items()) + '</div>'
page += '<div class="grid">' + "".join(cards) + '</div><footer><a href="style-book-tauri-ribbon-icon-review.html">Bronvormen op 16/24/32 px</a> · <a href="style-book-tauri-ribbon-crosswalk.json">Beslisdata</a></footer></main></html>'
(ROOT / "design/style-book-tauri-ribbon-crosswalk.html").write_text(page)
print(f"38 source-used Style Book commands classified: {counts}")
