// Public Tauri/Solid ribbon at f754cb7c9d9a; optional tabs require selected objects.
const beforePdfGroups = groups;
const pdfGroups = {
  'Start': [
    ['Document', ['Nieuw', 'Naar CAD', 'IFC-report', 'E-mail', 'Raster-PDF']],
    ['Hulpmiddelen', ['Hand', 'Selecteren']],
    ['Beeld', ['Inzoomen', 'Uitzoomen', 'Breedte passend', 'Pagina passend']],
    ['Navigeren', ['Eerste', 'Vorige', 'Volgende', 'Laatste']],
    ['Zoeken', ['Zoeken']], ['Instellingen', ['Voorkeuren', 'Vorige versie']],
  ],
  'Beeld': [
    ['Paginaweergave', ['Enkel', 'Doorlopend', 'Boek', 'Naast elkaar']],
    ['Weergave', ['Dunne lijnen', 'Leesmodus']],
    ['Panelen', ['Navigatie', 'Eigenschappen', 'Annotaties', 'Lagen']],
    ['Weergave', ['@pdfcontrol:Weergavekeuzes']],
    ['Vergelijken', ["PDF's vergelijken"]],
    ['Venster', ['Volledig scherm', 'Toetsaanslagen']],
  ],
  'Tekenen': [
    ['Selectie', ['Selecteren', 'Hand', 'Alles selecteren', 'Deselecteren']],
    ['Tekenen', ['@pdfcontrol:Vormkiezer']], ['Lijn', ['@pdfcontrol:Lijnkeuzes']],
    ['Knipsel', ['Vectorknipsel', 'Plak knipsel']],
    ['Schaal', ['Schaalgebied', 'Schaalgebied op pagina']],
    ['Annoteren', ['Oppervlakte', 'Lengte', 'Maatlijn', 'Hoek', 'Coördinaat']],
    ['Wijzigen', ['Verplaatsen', 'Kopiëren', 'Spiegelen H', 'Spiegelen V', 'Reeks']],
    ['Bewerken', ['Inkorten', 'Verlengen', 'Verschuiven', 'Afronden', 'Afkanten']],
    ['Klembord', ['Plakken', 'Plakken op plaats', 'Knippen', 'Kopiëren', 'Verwijderen']],
    ['Verzameling', ['Aanmaken', 'Ontleden']],
  ],
  'Annotatie': [
    ['Tekening', ['Markeren']], ['Tekst', ['Tekstvak', 'Bijschrift', 'Notitie']],
    ['Stempel', ['Stempel', 'Handtekening', 'Parametrisch symbool']],
    ['Redactie', ['Redigeren', 'Toepassen']],
    ['Eigenschappen', ['@pdfcontrol:Annotatie-eigenschappen']],
    ['Bewerken', ['Pagina wissen', 'Alles wissen']],
    ['METEN', ['Afstand', 'Oppervlakte', 'Omtrek', 'Hoek']],
    ['HOEVEELHEDEN', ['Hoeveelheden']],
  ],
  'PDF bewerken & samenvoegen': [
    ['Bewerken', ['Tekst bewerken', 'Tekst toevoegen', 'Tekst herkennen (OCR)', 'Bijsnijden']],
    ["Pagina's", ['Invoegen', 'Verwijderen', 'Extraheren', 'Volgorde']],
    ['Combineren', ['Samenvoegen', "PDF's vergelijken"]],
    ['Watermerk', ['Watermerk', 'Koptekst/voettekst', 'Beheren']],
  ],
  'Help': [
    ['Instellingen', ['Extensies', 'Bestandskoppelingen']],
    ['Help', ['Sneltoetsen', 'Over', 'Wat is nieuw', 'Updates', 'Diagnose']],
  ],
  'Opmaak': [['Symbooltype', ['@pdfcontrol:Typekiezer']], ['Eigenschappen', ['@pdfcontrol:Eigenschappenvelden']]],
  'Schikken': [
    ['Uitlijning', ['@pdfcontrol:Uitlijnkeuzes']],
    ['Verdelen', ['Horiz. verd.', 'Vert. verd.', 'Links', 'Boven', 'Midden']],
    ['Grootte', ['@pdfcontrol:Groottevelden']], ['Draaien', ['@pdfcontrol:Rotatievelden']],
    ['Spiegelen', ['@pdfcontrol:Spiegelkeuzes']], ['Z-volgorde', ['@pdfcontrol:Laagvolgorde']],
  ],
  'Afbeelding': [['Bijsnijden', ['@pdfcontrol:Bijsnijdopties']], ['Beeldbewerking', ['@pdfcontrol:Beeldopties']]],
};
groups = function (tab, app) {
  return app.id === 'pdf' ? (pdfGroups[tab] || []) : beforePdfGroups(tab, app);
};
Object.assign(iconMap, {
  'Nieuw': 'new', 'Naar CAD': 'export', 'IFC-report': 'export',
  'Inzoomen': 'search', 'Uitzoomen': 'search', 'Breedte passend': 'fit',
  'Pagina passend': 'fit', 'Zoeken': 'search', 'Voorkeuren': 'settings',
  'Selecteren': 'search', 'Annotaties': 'panelright', 'Eigenschappen': 'panelright',
  'Lagen': 'panelleft', 'Schaalgebied': 'measure', 'Oppervlakte': 'measure',
  'Lengte': 'measure', 'Maatlijn': 'measure', 'Hoek': 'measure',
  'Afstand': 'measure', 'Hoeveelheden': 'measure', 'Extensies': 'settings',
});
const beforePdfCommand = renderRibbonCommand;
renderRibbonCommand = function (command, group, app, index) {
  if (app.id === 'pdf' && command.startsWith('@pdfcontrol:')) {
    const label = command.split(':')[1];
    return '<label class="ribbon-control"><span>'+esc(label)+'</span><select aria-label="'+esc(label)+'"><option>Standaard</option><option>Meer opties</option></select></label>';
  }
  return beforePdfCommand(command, group, app, index);
};
