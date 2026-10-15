import { writeFileSync } from "node:fs";
import { repoPath } from "../lib/paths.mjs";
import { importIcons, manifestToml, readTsIconModule } from "./import.mjs";

// exportnaam → [id, nl, en, tags]
const MAP = {
  settingsIcon: ["ui/settings", "Instellingen", "Settings", ["ui"]],
  helpIcon: ["ui/help", "Help", "Help", ["ui"]],
  infoIcon: ["ui/info", "Informatie", "Information", ["ui"]],
  extensionBrowseIcon: ["ui/extension-browse", "Extensies zoeken", "Browse extensions", ["ui", "extension"]],
  extensionInstallIcon: ["ui/extension-install", "Extensie installeren", "Install extension", ["ui", "extension"]],
  extensionManageIcon: ["ui/extension-manage", "Extensies beheren", "Manage extensions", ["ui", "extension"]],
  projectIcon: ["file/project", "Project", "Project", ["file"]],
  pasteIcon: ["edit/paste", "Plakken", "Paste", ["edit", "clipboard"]],
  cutIcon: ["edit/cut", "Knippen", "Cut", ["edit", "clipboard"]],
  copyIcon: ["edit/copy", "Kopiëren", "Copy", ["edit", "clipboard"]],
  undoIcon: ["edit/undo", "Ongedaan maken", "Undo", ["edit", "history"]],
  redoIcon: ["edit/redo", "Opnieuw", "Redo", ["edit", "history"]],
  boldIcon: ["text/bold", "Vet", "Bold", ["text"]],
  italicIcon: ["text/italic", "Cursief", "Italic", ["text"]],
  underlineIcon: ["text/underline", "Onderstrepen", "Underline", ["text"]],
  alignLeftIcon: ["text/align-left", "Links uitlijnen", "Align left", ["text", "align"]],
  alignCenterIcon: ["text/align-center", "Centreren", "Center", ["text", "align"]],
  alignRightIcon: ["text/align-right", "Rechts uitlijnen", "Align right", ["text", "align"]],
  pencilIcon: ["draw/pencil", "Potlood", "Pencil", ["draw"]],
  lineIcon: ["draw/line", "Lijn", "Line", ["draw"]],
  arrowIcon: ["draw/arrow", "Pijl", "Arrow", ["draw"]],
  circleIcon: ["draw/circle", "Cirkel", "Circle", ["draw"]],
  rectangleIcon: ["draw/rectangle", "Rechthoek", "Rectangle", ["draw"]],
  imageIcon: ["insert/image", "Afbeelding", "Image", ["insert"]],
  tableIcon: ["insert/table", "Tabel", "Table", ["insert"]],
  linkIcon: ["insert/link", "Koppeling", "Link", ["insert"]],
  viewerLoadIcon: ["view/load-model", "Model laden", "Load model", ["view", "3d"]],
  viewerOrbitIcon: ["view/orbit", "Roteren", "Orbit", ["view", "3d", "navigation"]],
  viewerFitIcon: ["view/fit-all", "Passend", "Fit all", ["view", "3d", "navigation"]],
  viewerSectionIcon: ["view/section", "Doorsnede", "Section", ["view", "3d", "analysis"]],
  viewerMeasureIcon: ["view/measure", "Meten", "Measure", ["view", "3d", "analysis"]],
  viewerWireframeIcon: ["view/wireframe", "Draadmodel", "Wireframe", ["view", "3d", "display"]],
  ifcImportIcon: ["ifc/import", "IFC importeren", "Import IFC", ["ifc"]],
  ifcExportIcon: ["ifc/export", "IFC exporteren", "Export IFC", ["ifc"]],
  ifcTreeIcon: ["ifc/tree", "IFC-structuur", "IFC tree", ["ifc"]],
  ifcValidateIcon: ["ifc/validate", "IFC valideren", "Validate IFC", ["ifc"]],
  ifcStatsIcon: ["ifc/stats", "IFC-statistieken", "IFC statistics", ["ifc"]],
  reportNewIcon: ["report/new", "Nieuw rapport", "New report", ["report"]],
  reportTemplateIcon: ["report/template", "Rapportsjabloon", "Report template", ["report"]],
  reportGenerateIcon: ["report/generate", "Rapport genereren", "Generate report", ["report"]],
  reportPreviewIcon: ["report/preview", "Voorbeeld", "Preview", ["report"]],
  reportCoverIcon: ["report/cover", "Voorblad", "Cover page", ["report"]],
};

const template = readTsIconModule(repoPath("project-templates", "Tauri+React", "src", "components", "ribbon", "icons.ts"));
const pkg = readTsIconModule(repoPath("packages", "ribbon", "src", "icons.ts"));

for (const [name, svg] of pkg) {
  if (template.has(name) && template.get(name) !== svg) throw new Error(`${name} verschilt tussen template en packages/ribbon`);
}
const unknown = [...template.keys()].filter((n) => !MAP[n]);
if (unknown.length) throw new Error(`Geen id voor: ${unknown.join(", ")}`);

const entries = [...template].map(([name, svg]) => {
  const [id, nl, en, tags] = MAP[name];
  return { id, svg, label: { nl, en }, tags, source: "openaec" };
});
const iconsDir = repoPath("design", "icons");
const { written, duplicates } = importIcons(entries, iconsDir);
writeFileSync(repoPath("design", "icons", "icons.toml"), manifestToml(written), "utf8");
console.log(`${written.length} iconen geschreven`);
for (const [a, b] of duplicates) console.log(`dubbel: ${a} = ${b} (overgeslagen)`);
