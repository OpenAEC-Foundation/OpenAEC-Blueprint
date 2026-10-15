// Open Frame Studio ribbon at eb77f9e4c5d3; workspace views are a separate band.
const beforeFrameGroups = groups;
const frameGroups = {
  'Home': [
    ['Sjabloon', ['Sjabloon kiezen', 'Opslaan als sjabloon', 'Sjabloon verwijderen']],
    ['Nieuw kozijn', ['Leeg', 'Draaikiep', 'Dubbel', 'Schuifpui', 'Voordeur']],
    ['Bewerken', ['Kolom toevoegen', 'Rij toevoegen', 'Dupliceren', 'Verwijderen']],
    ['Importeren', ['Nieuw profiel', 'Profiel DXF', 'Catalogus']],
  ],
  'Invoegen': [
    ['Onderverdeling', ['Kolom', 'Rij']],
    ['Paneel type', ['Vast glas', 'Draaikiep', 'Paneel']],
    ['Vliesgevel', ['Leeg', 'Stijl-regel', 'Element']],
  ],
  'IFC / Export': [
    ['Kozijn exporteren', ['IFC (LOD-keuze)', 'DXF']],
    ['IFC Import', ['IFC Import', 'IFC Roundtrip', 'IFC vergelijken']],
    ['Validatie', ['IDS Validatie', 'Certificering']],
    ['Project exporteren', ['Kozijnstaat PDF', 'Kozijnstaat Excel']],
    ['Werkplaats', ['Tekening PDF']],
    ['3D Export', ['glTF/GLB']],
    ['Blender / Bonsai', ['Naar Blender', 'Verbinding testen']],
  ],
  'Productie': [
    ['Productiestaten exporteren', ['PDF', 'Excel', 'CSV']],
    ['CNC / Labels', ['CNC G-code', 'Labels PDF']],
    ['Planning / Optimalisatie', ['Zaagplan', 'Planning', 'CNC', 'Inkoop']],
  ],
  'Beeld': [
    ['Ongedaan maken', ['Ongedaan', 'Opnieuw']],
    ['Zoom', ['Inzoomen', 'Uitzoomen']],
    ['Thema', ['Thema kiezen']],
  ],
};
groups = function (tab, app) {
  return app.id === 'frame' ? (frameGroups[tab] || []) : beforeFrameGroups(tab, app);
};
Object.assign(iconMap, {
  'Sjabloon kiezen': 'grid', 'Opslaan als sjabloon': 'save', 'Sjabloon verwijderen': 'close',
  'Leeg': 'new', 'Nieuw profiel': 'new', 'Catalogus': 'open', 'Profiel DXF': 'import',
  'IFC (LOD-keuze)': 'export', 'DXF': 'export', 'IFC Import': 'import', 'IDS Validatie': 'check', 'Certificering': 'check',
  'Kozijnstaat PDF': 'export', 'Kozijnstaat Excel': 'export', 'Tekening PDF': 'export',
  'glTF/GLB': 'export', 'Naar Blender': 'export', 'Verbinding testen': 'check',
  'PDF': 'export', 'Excel': 'export', 'CSV': 'export', 'CNC G-code': 'export', 'Labels PDF': 'export',
  'Ongedaan': 'undo', 'Opnieuw': 'redo', 'Thema kiezen': 'settings',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Draaikiep': 'Square', 'Dubbel': 'LayoutGrid', 'Schuifpui': 'Square', 'Voordeur': 'Square',
  'Kolom toevoegen': 'Columns3', 'Rij toevoegen': 'LayoutGrid', 'Dupliceren': 'Copy',
  'Verwijderen': 'Trash2', 'Kolom': 'Columns3', 'Rij': 'LayoutGrid',
  'Vast glas': 'Square', 'Paneel': 'Square', 'Stijl-regel': 'LayoutGrid',
  'Element': 'Boxes', 'IFC vergelijken': 'GitCompareArrows', 'Planning': 'CalendarDays',
  'Zaagplan': 'BarChart3', 'IFC Roundtrip': 'GitCompareArrows', 'Inzoomen': 'ZoomIn', 'Uitzoomen': 'ZoomOut',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
const beforeFrameCommand = renderRibbonCommand;
renderRibbonCommand = function (command, group, app, index) {
  if (app.id === 'frame' && command === 'Sjabloon kiezen') {
    return '<label class="ribbon-control"><span>Sjabloon</span><select aria-label="Kozijnsjabloon"><option>Standaard 67mm Meranti</option><option>Standaard 67mm Accoya</option><option>Zwaar 78mm Meranti</option><option>Passief 90mm Accoya</option></select></label>';
  }
  if (app.id === 'frame' && command === 'IFC (LOD-keuze)') {
    return '<label class="ribbon-control"><span>IFC LOD</span><select aria-label="IFC detailniveau"><option>300</option><option>200</option><option>400</option></select><button type="button" class="cmd">IFC export</button></label>';
  }
  if (app.id === 'frame' && command === 'Thema kiezen') {
    return '<label class="ribbon-control"><span>Thema</span><select aria-label="Frame thema"><option>Donker</option><option>Licht</option></select></label>';
  }
  return beforeFrameCommand(command, group, app, index);
};
