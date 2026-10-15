// Review copy of the command taxonomy in open-calc-studio/src/components/ribbon
// at b47042704efa; command execution remains in the source application.
const sharedGroups = groups;
const calcIconRoot = '../harmonization/library-icons/lucide-static/0.575.0/';
const calcIconFiles = Object.fromEntries(Object.entries({
  'Hoofdstuk': 'FilePlus2', 'Begr.post': 'FileText',
  'Bew.post': 'ClipboardCheck', 'Rekenregel': 'ListOrdered',
  'Tekstregel': 'FileType', 'Witregel': 'ListTree',
  'Verwijder': 'Trash2', 'Plakken': 'ClipboardCheck',
  'Knippen': 'Scissors', 'Kopiëren': 'Copy',
  'Varianten': 'GitBranch', 'Optieset': 'Layers',
  'Bijhouden': 'ListOrdered', 'Wis markeringen': 'Eraser',
  'Afdrukken': 'Printer',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg']));
const calcGroups = {
  'Begroting': [
    ['Regels', ['Hoofdstuk', 'Begr.post', 'Bew.post', 'Rekenregel', 'Tekstregel', 'Witregel', 'Verwijder']],
    ['Klembord', ['Plakken', 'Knippen', 'Kopiëren']],
    ['Geschiedenis', ['Ongedaan', 'Opnieuw']],
    ['Panelen', ['Hoeveelheid']],
    ['Weergave', ['UI-1', 'UI-2', 'Simple', 'Inklappen']],
    ['Prijzen', ['Prijzen %']],
    ['Wijzigingen', ['Bijhouden', 'Wis markeringen', 'Hele regel', 'Alleen cel']],
    ['Project', ['Projectgegevens']],
    ['Varianten', ['Varianten', 'Optieset']],
  ],
  'Rapportage': [
    ['Rapportage', ['Opdrachtgever', 'Intern', 'Nacalculatie']],
    ['Weergave', ['Hoeveelheden', 'Staand', 'Liggend']],
    ['Afdrukken', ['Afdrukken']],
    ['Export', ['PDF Export', 'Excel Export', 'IFC Export']],
  ],
  'Spreadsheet': [
    ['Werkbladen', ['Nieuw blad', 'Verwijder']],
    ['Opmaak', ['Vet', 'Cursief', 'Links', 'Midden', 'Rechts']],
    ['Getal', ['Valuta (€)', 'Percentage (%)', '+Decimaal', '-Decimaal']],
    ['Tekstgrootte', ['Groter', 'Kleiner']],
  ],
  'IFC': [['Rapport', ['Genereer']]],
  'Offerte': [
    ['Secties', ['Technisch', 'Opties', 'Vrij', 'Meerwerk']],
    ['Document', ['Gegevens', 'Termijnen', 'Garanties']],
    ['Export', ['PDF offerte']],
  ],
  'Tekstopmaak': [
    ['Tekststijl', ['Vet', 'Cursief', 'Onderstr.']],
    ['Grootte', ['Groter', 'Kleiner']],
    ['Uitlijning', ['Links', 'Midden', 'Rechts']],
  ],
  '3D': [['Experimenteel', ['Nog niet beschikbaar']]],
  'PDF': [['Experimenteel', ['Nog niet beschikbaar']]],
};
groups = function (tab, app) {
  return app.id === 'calc' ? (calcGroups[tab] || []) : sharedGroups(tab, app);
};
Object.assign(iconMap, {
  'Hoofdstuk': 'new', 'Begr.post': 'new', 'Bew.post': 'new',
  'Rekenregel': 'new', 'Tekstregel': 'new', 'Witregel': 'new',
  'Verwijder': 'close', 'Ongedaan': 'undo', 'Opnieuw': 'redo',
  'Hoeveelheid': 'settings', 'Projectgegevens': 'settings',
  'Prijzen %': 'settings', 'Genereer': 'export',
  'PDF Export': 'export', 'Excel Export': 'export', 'IFC Export': 'export',
  'Nieuw blad': 'new', 'Afdrukken': 'export', 'PDF offerte': 'export',
  'Nog niet beschikbaar': 'help',
});
