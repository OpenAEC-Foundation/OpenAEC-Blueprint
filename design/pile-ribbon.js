// Pile Plan ribbon at ffe979d3b859. Its View groups include true controls.
const beforePileGroups = groups;
const pileGroups = {
  'Plan': [
    ['Project', ['Projectinformatie']],
    ['Inspecteren', ['Belastinglocaties', 'Sonderingen']],
    ['Selecteren', ['Kaderselectie']],
    ['Instellingen', ['Sonderingsinstellingen', 'Kosteninstellingen', 'Groeperingsinstellingen']],
    ['Vergrendelen', ['Locaties vergrendelen']],
    ['Optimalisatie', ['Uitvoeren']],
  ],
  'Weergave': [
    ['Symbolen', ['@slider:Symboolgrootte']],
    ['Benutting', ['@range:Gewenst bereik']],
    ['Voorgrond', ['@segmented:Voorgrond']],
    ['Grid', ['Grid tonen']],
    ['Gebieden', ['Puntniveaugebieden tonen', 'Groepen tonen']],
    ['Vensters', ['Verkenner tonen', 'Eigenschappen tonen']],
  ],
};
groups = function (tab, app) {
  return app.id === 'pile' ? (pileGroups[tab] || []) : beforePileGroups(tab, app);
};
Object.assign(iconMap, {
  'Projectinformatie': 'open', 'Belastinglocaties': 'measure',
  'Sonderingen': 'measure', 'Kaderselectie': 'grid',
  'Sonderingsinstellingen': 'settings', 'Kosteninstellingen': 'settings',
  'Groeperingsinstellingen': 'settings', 'Uitvoeren': 'check',
  'Grid tonen': 'grid', 'Verkenner tonen': 'panelleft',
  'Eigenschappen tonen': 'panelright',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Locaties vergrendelen': 'Lock',
  'Puntniveaugebieden tonen': 'LayoutGrid', 'Groepen tonen': 'Boxes',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));

function renderRibbonCommand(c, group, app, index) {
  if (app.id === 'pile' && c === '@slider:Symboolgrootte') {
    return '<label class="ribbon-control"><span>Symboolgrootte</span><strong id="symbol-value">100%</strong><input type="range" min="10" max="200" value="100" aria-label="Symboolgrootte" oninput="document.getElementById(\'symbol-value\').textContent=this.value+\'%\'"></label>';
  }
  if (app.id === 'pile' && c === '@range:Gewenst bereik') {
    return '<div class="ribbon-control ribbon-range"><span>Gewenst bereik</span><strong>45–95%</strong><input type="range" min="0" max="100" value="45" aria-label="Minimale benuttingsgraad"><input type="range" min="0" max="100" value="95" aria-label="Maximale benuttingsgraad"></div>';
  }
  if (app.id === 'pile' && c === '@segmented:Voorgrond') {
    return '<div class="ribbon-control ribbon-segmented" role="group" aria-label="Voorgrond"><button class="active" type="button">Belastinglocaties</button><button type="button">Sonderingen</button></div>';
  }
  return '<button class="cmd '+(index===0&&group===activeTab?'selected':'')+'" title="'+esc(cmdLabel(c))+'">'+cmdIcon(c)+'<span>'+esc(cmdLabel(c))+'</span></button>';
}
