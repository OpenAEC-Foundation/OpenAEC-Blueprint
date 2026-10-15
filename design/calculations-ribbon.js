// Current ribbon from Open-Calculations-Studio at 21d218c996d0.
const beforeCalculationsGroups = groups;
const calculationsGroups = {
  'Start': [
    ['Bestand', ['Nieuw', 'Bladeren…', 'Opslaan']],
    ['Bewerken', ['Ongedaan', 'Opnieuw']],
    ['Invoegen', ['Module', 'Afbeelding']],
    ['Exporteren', ['Voorbeeld', 'PDF blad', 'Rapport (PDF)']],
  ],
  'IFC': [],
};
groups = function (tab, app) {
  return app.id === 'calculations' ? (calculationsGroups[tab] || []) : beforeCalculationsGroups(tab, app);
};
Object.assign(iconMap, {
  'Bladeren…': 'open', 'Module': 'extensions',
  'Afbeelding': 'new', 'Voorbeeld': 'fit',
  'PDF blad': 'export', 'Rapport (PDF)': 'export',
});
