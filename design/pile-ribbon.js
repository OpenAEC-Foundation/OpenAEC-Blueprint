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
const pileIconRoot = '../harmonization/inline-ui-icons/pile-plan-studio/';
const pileIcons = {
  'Projectinformatie': 'projectIcon',
  'Belastinglocaties': 'loadPointIcon',
  'Sonderingen': 'cptIcon',
  'Kaderselectie': 'lassoIcon',
  'Sonderingsinstellingen': 'settingsIcon',
  'Kosteninstellingen': 'settingsIcon',
  'Groeperingsinstellingen': 'settingsIcon',
  'Locaties vergrendelen': 'lockIcon',
  'Uitvoeren': 'optimizeIcon',
  'Grid tonen': 'gridIcon',
  'Puntniveaugebieden tonen': 'tipLevelRegionsIcon',
  'Groepen tonen': 'groupsIcon',
  'Verkenner tonen': 'explorerPanelIcon',
  'Eigenschappen tonen': 'propertiesPanelIcon',
};

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
  const artwork = app.id === 'pile' && pileIcons[c]
    ? '<img src="'+pileIconRoot+pileIcons[c]+'.svg" alt="">'
    : cmdIcon(c);
  const label = cmdLabel(c);
  if (app.id !== 'pile') return '<button class="cmd '+(index===0&&group===activeTab?'selected':'')+'" title="'+esc(label)+'">'+artwork+'<span>'+esc(label)+'</span></button>';
  const width = Math.max(86, Math.min(160, Math.ceil(label.length * 6.2 + 20)));
  return '<button class="cmd" style="width:'+width+'px" title="'+esc(label)+'">'+artwork+'<span style="max-width:'+(width-8)+'px">'+esc(label)+'</span></button>';
}
