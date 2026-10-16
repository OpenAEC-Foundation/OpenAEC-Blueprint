// Source-pinned Geotechniek ribbon taxonomy (8182b48afc3f). Keep this HTML
// review aligned with the native Rust preview in ribbon_preview.rs.
const beforeGeotechGroups = groups;
const geotechGroups = {
  'Home': [['Project', ['Projectinfo']], ['Weergave', ['Zoom -', 'Passend']]],
  'Kaart': [['Kaart', ['Meten', 'Exporteer als afbeelding']]],
  'Rapport': [['Output', ['Genereer PDF', 'Open PDF']]],
  'Situatietekening': [
    ['Selecteer', ['Selecteren']],
    ['Bewerken', ['Verplaatsen', 'Kopiëren', 'Roteren…', 'Verwijderen', 'Trim', 'Extend', 'Mirror', 'Offset']],
    ['Plaatsen', ['Sondering', 'Boring', 'Sonderingsraster', 'Lijn', 'Maatlijn', 'RD-coördinaat', 'Vlak', 'Opmerking']],
    ['Overlay', ['Image/PDF import', 'Kader (SVG)', 'Wis alles']],
    ['Export', ['Exporteer DWG', 'Exporteer PDF', 'Print']],
  ],
  'Berekeningen': [['Projectberekeningen', ['Dynamische berekeningenlijst']]],
  'IFC': [['Automatisch gegenereerd', ['Live IFC4x3 + IFCX']]],
};
groups = function (tab, app) {
  return app.id === 'geotech' ? (geotechGroups[tab] || []) : beforeGeotechGroups(tab, app);
};
// Every active Geotechniek button has an explicit, source-provenanced icon.
// Reviewed DomainIcon SVGs come from the Rust crate; unresolved domain
// meanings keep their actual UI source SVG for comparison at small sizes.
const geotechSource = '../harmonization/inline-ui-icons/open-geotechniek-studio/';
const geotechDomain = '../crates/openaec-ui/assets/domain-icons/';
const geotechIcons = {
  'Projectinfo': '../crates/openaec-ui/assets/icons/settings.svg',
  'Zoom -': '../crates/openaec-ui/assets/icons/zoomout.svg',
  'Passend': '../crates/openaec-ui/assets/icons/fit.svg',
  'Meten': '../crates/openaec-ui/assets/icons/measure.svg',
  'Exporteer als afbeelding': geotechSource + 'kaart-export-image.svg',
  'Genereer PDF': geotechSource + 'rapport-download.svg',
  'Open PDF': geotechSource + 'rapport-open.svg',
  'Selecteren': geotechSource + 'tekening-select.svg',
  'Verplaatsen': geotechDomain + 'transform-move.svg',
  'Kopiëren': geotechSource + 'tekening-copy.svg',
  'Roteren…': geotechDomain + 'transform-rotate.svg',
  'Verwijderen': geotechSource + 'tekening-delete.svg',
  'Trim': geotechDomain + 'drawing-trim.svg',
  'Extend': geotechDomain + 'drawing-extend.svg',
  'Mirror': geotechDomain + 'transform-mirror.svg',
  'Offset': geotechDomain + 'drawing-offset.svg',
  'Sondering': geotechDomain + 'geotech-sondering.svg',
  'Boring': geotechDomain + 'geotech-boring.svg',
  'Sonderingsraster': geotechDomain + 'geotech-sondering-grid.svg',
  'Lijn': geotechDomain + 'drawing-line.svg',
  'Maatlijn': geotechDomain + 'drawing-dimension.svg',
  'RD-coördinaat': geotechDomain + 'geotech-coordinate-tag.svg',
  'Vlak': geotechDomain + 'drawing-polygon.svg',
  'Opmerking': geotechDomain + 'drawing-note.svg',
  'Image/PDF import': geotechSource + 'tekening-overlay.svg',
  'Kader (SVG)': geotechDomain + 'drawing-svg-frame.svg',
  'Wis alles': geotechSource + 'tekening-delete.svg',
  'Exporteer DWG': geotechSource + 'tekening-dwg.svg',
  'Exporteer PDF': geotechSource + 'tekening-export-pdf.svg',
  'Print': '../crates/openaec-ui/assets/icons/print.svg',
  'Dynamische berekeningenlijst': '../crates/openaec-ui/assets/icons/grid.svg',
  'Live IFC4x3 + IFCX': '../crates/openaec-ui/assets/icons/cube.svg',
};
const beforeGeotechCommand = renderRibbonCommand;
renderRibbonCommand = function (command, group, app, index) {
  if (app.id !== 'geotech' || !geotechIcons[command]) {
    return beforeGeotechCommand(command, group, app, index);
  }
  const label = cmdLabel(command);
  return '<button class="cmd" title="' + esc(label) + '"><img src="' + geotechIcons[command] + '" alt=""><span>' + esc(label) + '</span></button>';
};
