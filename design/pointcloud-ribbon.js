// Current native Pointcloud branch: one Start ribbon with ten panels.
const beforePointcloudGroups = groups;
const pointcloudGroups = {
  'Start': [
    ['Bestand', ['Openen', 'Scanmap openen']],
    ['Navigatie', ['Alles passend', 'Inzoomen', 'Uitzoomen', 'Selectie passend', 'Pannen']],
    ['Selectie', ['Punt kiezen', 'Kaderselectie', 'Selectie wissen', 'Punten verwijderen', 'Selectie exporteren']],
    ['Snedebox', ['Snedebox', 'Passend op selectie', 'Box resetten']],
    ['Oppervlak', ['Mesh', 'Gesloten mesh', 'Terrein', 'Vlakken']],
    ['Tekening', ['Mesh naar plan', 'Doorsnedetekening', 'Blad']],
    ['Meten', ['Afstand', 'Oppervlakte']],
    ['Annotatie', ['Notitie', 'Lijn tekenen']],
    ['Index', ['Index bouwen', 'LOD verversen']],
    ['Export', ['Puntenwolk exporteren']],
  ],
};
groups = function (tab, app) {
  return app.id === 'pointcloud' ? (pointcloudGroups[tab] || []) : beforePointcloudGroups(tab, app);
};
Object.assign(iconMap, {
  'Alles passend': 'fit', 'Selectie passend': 'fit', 'Passend op selectie': 'fit',
  'Punt kiezen': 'search', 'Kaderselectie': 'grid', 'Selectie wissen': 'close',
  'Selectie exporteren': 'export', 'Gesloten mesh': 'cube', 'Vlakken': 'grid',
  'Afstand': 'measure', 'Oppervlakte': 'measure', 'Puntenwolk exporteren': 'export',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Scanmap openen': 'FolderOpen', 'Inzoomen': 'ZoomIn', 'Uitzoomen': 'ZoomOut',
  'Pannen': 'MoveHorizontal', 'Punten verwijderen': 'Trash2', 'Snedebox': 'Square',
  'Box resetten': 'RotateCcw', 'Mesh': 'Boxes', 'Terrein': 'Map',
  'Mesh naar plan': 'FileText', 'Doorsnedetekening': 'FileText', 'Blad': 'FileText',
  'Notitie': 'FileText', 'Lijn tekenen': 'Pen', 'Index bouwen': 'DatabaseBackup',
  'LOD verversen': 'RefreshCw',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
