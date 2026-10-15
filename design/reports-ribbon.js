// Actual Reports ribbon at 818e58118c0f; the atlas workspace is still a study.
const beforeReportsGroups = groups;
const reportsGroups = {
  'Start': [
    ['Klembord', ['Plakken', 'Kopieer sectie']],
    ['Blokken', ['Tekst', 'Berekening', 'Toets', 'Tabel', 'Spreadsheet', 'Afbeelding', 'Kaart', 'Opsomming', 'Subkop']],
    ['Pagina', ['Witruimte', 'Pagina-einde']],
    ['Controle', ['Valideren']],
    ['Uitvoer', ['PDF Genereren', 'Download PDF']],
  ],
  'Invoegen': [
    ['Secties', ['Nieuw hoofdstuk', 'Nieuwe bijlage']],
    ['Inhoud', ['Tekst', 'Berekening', 'Toets', 'Tabel', 'Afbeelding', 'Kaart', 'Opsomming', 'Subkop']],
  ],
  'Beeld': [
    ['Weergave', ['Editor', 'Gesplitst', 'JSON', 'Preview']],
    ['Panelen', ['Zijpaneel']],
  ],
};
groups = function (tab, app) {
  return app.id === 'reports' ? (reportsGroups[tab] || []) : beforeReportsGroups(tab, app);
};
Object.assign(iconMap, {
  'Valideren': 'check', 'PDF Genereren': 'export', 'Download PDF': 'export',
  'Nieuw hoofdstuk': 'new', 'Nieuwe bijlage': 'new',
  'Zijpaneel': 'panelleft',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Kopieer sectie': 'Copy', 'Tekst': 'FileText',
  'Berekening': 'Hash', 'Tabel': 'LayoutGrid',
  'Spreadsheet': 'LayoutGrid', 'Kaart': 'Map',
  'Opsomming': 'ListOrdered', 'Subkop': 'FileType',
  'Witruimte': 'Minus', 'Pagina-einde': 'FilePlus2',
  'Editor': 'Pen', 'Gesplitst': 'Columns3',
  'JSON': 'FileCode', 'Preview': 'Eye',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
