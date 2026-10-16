"""Inject the reviewed studio taxonomy into the shared shell design study."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
apps = json.loads((root / "design/app-layouts.json").read_text())
domain_icons = json.loads((root / "design/domain-icon-drafts.json").read_text())
template = (root / "design/harmonized-template.html").read_text()
payload = json.dumps(apps, ensure_ascii=False).replace("</", "<\\/")
icons_payload = json.dumps(domain_icons, ensure_ascii=False).replace("</", "<\\/")
(root / "design/harmonized.html").write_text(
    template.replace("/*APP_DATA*/", payload).replace("/*DOMAIN_ICON_DATA*/", icons_payload).replace("/*CALC_RIBBON*/", (root / "design/calc-ribbon.js").read_text()).replace("/*GEOTECH_RIBBON*/", (root / "design/geotech-ribbon.js").read_text()).replace("/*HEATLOSS_RIBBON*/", (root / "design/heatloss-ribbon.js").read_text()).replace("/*CALCULATIONS_RIBBON*/", (root / "design/calculations-ribbon.js").read_text()).replace("/*REPORTS_RIBBON*/", (root / "design/reports-ribbon.js").read_text()).replace("/*VALIDATOR_RIBBON*/", (root / "design/validator-ribbon.js").read_text()).replace("/*PILE_RIBBON*/", (root / "design/pile-ribbon.js").read_text()).replace("/*FRAME_RIBBON*/", (root / "design/frame-ribbon.js").read_text()).replace("/*2D_EXTENSION_RIBBON*/", (root / "design/2d-extension-ribbon.js").read_text()).replace("/*CAD_RIBBON*/", (root / "design/cad-ribbon.js").read_text()).replace("/*POINTCLOUD_RIBBON*/", (root / "design/pointcloud-ribbon.js").read_text()).replace("/*PDF_RIBBON*/", (root / "design/pdf-ribbon.js").read_text())
)
print(f"Generated shared shell for {len(apps)} tool interfaces")
