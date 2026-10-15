// Disconnected BCF state of the BIM Validator viewer ribbon at 8f837dd9a56e.
const beforeValidatorGroups = groups;
const validatorGroups = {
  'Start': [
    ['Project', ['Opslaan', 'Opslaan als', 'Openen']],
    ['Modellen', ['Toevoegen IFC', 'Verwijder']],
    ['Validatie', ['Valideer', 'IDS Standaard', 'Reset']],
    ['BCF', ['Export BCF', 'Sync', 'Inloggen']],
  ],
  'Beeld': [
    ['Panelen', ['Modellen', 'Validatie']],
    ['3D Beeld', ['Passend', 'Reset']],
    ['Doorsnede', ['Snijvlak X', 'Snijvlak Y', 'Snijvlak Z', 'Wis snijvlakken']],
  ],
};
groups = function (tab, app) {
  return app.id === 'validator' ? (validatorGroups[tab] || []) : beforeValidatorGroups(tab, app);
};
Object.assign(iconMap, {
  'Opslaan als': 'save', 'Toevoegen IFC': 'import',
  'Valideer': 'check', 'Export BCF': 'export',
  'Modellen': 'panelleft', 'Validatie': 'panelright',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'IDS Standaard': 'ListTree', 'Reset': 'RotateCcw',
  'Sync': 'RefreshCw', 'Inloggen': 'Lock',
  'Snijvlak X': 'Columns3', 'Snijvlak Y': 'Columns3',
  'Snijvlak Z': 'Columns3', 'Wis snijvlakken': 'Eraser',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
