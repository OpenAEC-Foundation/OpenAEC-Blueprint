// Ribbon icons from the OpenAEC B2 set (design 0.4).
// public/icons/standard.svg holds every B2 icon of the standard application in
// 16 and 24 px; scripts/sync_tauri_template.py in the Blueprint repository keeps
// it up to date. A large button shows the 24 px design, a small one the 16 px
// design (see Ribbon.css). Add an icon: put its B2 id in STANDARD of
// scripts/build_web_icons.py, run that script and sync_tauri_template.py.

const SPRITE = `${import.meta.env.BASE_URL}icons/standard.svg`;

/** A B2 icon as markup for RibbonButton: both sizes, CSS shows the right one. */
export function b2(id: string): string {
  return (
    `<svg class="oa-icon oa-b2-24" aria-hidden="true"><use href="${SPRITE}#i24-${id}"/></svg>` +
    `<svg class="oa-icon oa-b2-16" aria-hidden="true"><use href="${SPRITE}#i16-${id}"/></svg>`
  );
}

export const settingsIcon = b2("ui.settings");
export const helpIcon = b2("ui.help");
export const infoIcon = b2("status.info");

// IFC tab
export const ifcImportIcon = b2("ifc.import");
export const ifcExportIcon = b2("ifc.export");
export const ifcTreeIcon = b2("panel.model-tree");
export const ifcValidateIcon = b2("ifc.validate");
export const ifcStatsIcon = b2("data.chart");

// 3D Viewer tab
export const viewerLoadIcon = b2("file.open");
export const viewerOrbitIcon = b2("view.orbit");
export const viewerSectionIcon = b2("section.box");
export const viewerMeasureIcon = b2("measure.distance");
export const viewerFitIcon = b2("view.fit");
export const viewerWireframeIcon = b2("mesh.closed");

// Report tab
export const reportNewIcon = b2("file.new");
export const reportTemplateIcon = b2("report.template");
export const reportGenerateIcon = b2("report.generate");
export const reportPreviewIcon = b2("view.report-preview");
export const reportCoverIcon = b2("report.cover");

// Extensions tab
export const extensionBrowseIcon = b2("software.catalog");
export const extensionInstallIcon = b2("extension.install-file");
export const extensionManageIcon = b2("extensions.manage");

// Home tab
export const projectIcon = b2("project.properties");
export const pasteIcon = b2("edit.paste");
export const cutIcon = b2("edit.cut");
export const copyIcon = b2("edit.copy");
export const undoIcon = b2("edit.undo");
export const redoIcon = b2("edit.redo");
export const boldIcon = b2("format.bold");
export const italicIcon = b2("format.italic");
export const underlineIcon = b2("format.underline");
export const alignLeftIcon = b2("format.align-left");
export const alignCenterIcon = b2("format.align-center");
export const alignRightIcon = b2("format.align-right");
export const pencilIcon = b2("draw.freehand");
export const lineIcon = b2("draw.line");
export const arrowIcon = b2("draw.arrow");
export const circleIcon = b2("draw.circle");
export const rectangleIcon = b2("draw.rectangle");
export const imageIcon = b2("draw.image");
export const tableIcon = b2("data.table");
export const linkIcon = b2("link.open-external");
