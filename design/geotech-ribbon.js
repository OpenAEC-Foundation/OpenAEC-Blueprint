// Review taxonomy from open-geotechniek-studio ribbon components at 8182b48afc3f.
const beforeGeotechGroups = groups;
const geotechGroups = {
  'Home': [['Project', ['Projectinfo']], ['Weergave', ['Zoom -', 'Passend']]],
  'Kaart': [['Kaart', ['Meten', 'Exporteer als afbeelding']]],
  'Rapport': [['Output', ['Genereer PDF', 'Open PDF']]],
  'Situatietekening': [
    ['Selecteer', ['Selecteren']],
    ['Bewerken', ['Verplaatsen', 'Kopiëren', 'Roteren', 'Verwijderen', 'Trim', 'Mirror']],
    ['Plaatsen', ['Sondering', 'Boring', 'Lijn', 'Maatlijn', 'Vlak', 'Opmerking']],
    ['Overlay', ['Image/PDF import', 'Kader (SVG)', 'Wis alles']],
    ['Export', ['Exporteer DWG', 'Exporteer PDF', 'Print']],
  ],
  'Berekeningen': [['Projectberekeningen', ['Dynamische berekeningenlijst']]],
  'IFC': [['Automatisch gegenereerd', ['Live IFC4x3 + IFCX']]],
};
groups = function (tab, app) {
  return app.id === 'geotech' ? (geotechGroups[tab] || []) : beforeGeotechGroups(tab, app);
};
Object.assign(iconMap, {
  'Projectinfo': 'settings', 'Passend': 'fit', 'Meten': 'measure',
  'Exporteer als afbeelding': 'export', 'Genereer PDF': 'export',
  'Open PDF': 'open', 'Maatlijn': 'measure',
  'Image/PDF import': 'import', 'Exporteer DWG': 'export',
  'Exporteer PDF': 'export', 'Print': 'export',
  'Dynamische berekeningenlijst': 'grid', 'Live IFC4x3 + IFCX': 'cube',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Verplaatsen': 'MoveHorizontal', 'Roteren': 'RotateCw',
  'Trim': 'Scissors', 'Mirror': 'GitCompareArrows',
  'Sondering': 'Compass', 'Boring': 'Compass',
  'Lijn': 'Minus', 'Vlak': 'Square', 'Opmerking': 'Pen',
  'Kader (SVG)': 'Square', 'Wis alles': 'Eraser',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
