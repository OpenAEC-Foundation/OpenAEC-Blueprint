// Route-linked tabs from open-heatloss-studio Ribbon.tsx at e233aec70e16.
// IFC is intentionally empty; its page owns copy/download actions.
const beforeHeatlossGroups = groups;
const heatlossGroups = {
  'Vertrekken': [
    ['Vertrekken', ['Nieuw vertrek']],
    ['Zones', ['Zones beheren']],
    ['Berekening', ['Bereken']],
  ],
  'Constructies': [['Constructies', ['Nieuwe constructie', 'Catalogus']]],
  'Modeller': [
    ['Bewerken', ['Ongedaan', 'Opnieuw', 'Leeg']],
    ['Selectie', ['Selecteer']],
    ['Vormen', ['Rechthoek', 'Polygoon', 'Cirkel']],
    ['Bouwelementen', ['Raam', 'Deur']],
  ],
  'IFC': [],
  'Resultaten': [
    ['Rapport', ['Genereer rapport']],
    ['Export', ['Export JSON']],
  ],
  'Rapport': [['Rapport', ['Genereren', 'Download PDF']]],
};
groups = function (tab, app) {
  return app.id === 'heatloss' ? (heatlossGroups[tab] || []) : beforeHeatlossGroups(tab, app);
};
Object.assign(iconMap, {
  'Nieuw vertrek': 'new', 'Nieuwe constructie': 'new',
  'Bereken': 'grid', 'Catalogus': 'open',
  'Ongedaan': 'undo', 'Opnieuw': 'redo',
  'Genereer rapport': 'export', 'Export JSON': 'export',
  'Genereren': 'export', 'Download PDF': 'export',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Zones beheren': 'Building2', 'Leeg': 'Trash2',
  'Rechthoek': 'Square', 'Polygoon': 'Diamond', 'Cirkel': 'Circle',
  'Raam': 'Columns3', 'Deur': 'PanelRight',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
