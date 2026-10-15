// AEC extension at fd22965ed28a. IFC is a built-in host tab receiving two buttons.
const before2dExtensionGroups = groups;
const extension2dGroups = {
  'AEC': [
    ['Elements', ['IfcBeam', 'IfcWall', 'IfcSlab', 'IfcPile', 'IfcColumn', 'CPT', 'IfcSpace']],
    ['Annotations', ['Slab Label', 'IfcGrid', '2DLevel', 'Section/Detail']],
    ['Connections', ['Join']],
    ['Reference', ['PDF Underlay']],
    ['Properties', ['Materials', 'IfcTypes', 'Wall Systems', 'Project']],
  ],
  'Pile Plan': [
    ['Place', ['IfcPile', 'CPT', 'Puntniveau', 'Pile Symbols']],
    ['CPT Data', ['Parse CPT']],
  ],
  'IFC': [['IFCX · in host-IFC', ['Export IFCX', 'Copy IFCX']]],
};
groups = function (tab, app) {
  return app.id === '2d' ? (extension2dGroups[tab] || []) : before2dExtensionGroups(tab, app);
};
Object.assign(iconMap, {
  'PDF Underlay': 'import', 'Materials': 'settings', 'IfcTypes': 'settings',
  'Wall Systems': 'settings', 'Project': 'open', 'Parse CPT': 'import',
  'Export IFCX': 'export', 'IfcGrid': 'grid', 'Puntniveau': 'measure',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'IfcBeam': 'Columns3', 'IfcWall': 'Square', 'IfcSlab': 'LayoutGrid',
  'IfcPile': 'Compass', 'IfcColumn': 'Columns3', 'CPT': 'Activity',
  'IfcSpace': 'Square', 'Slab Label': 'FileText', '2DLevel': 'Gauge',
  'Section/Detail': 'FileText', 'Join': 'GitBranch',
  'Pile Symbols': 'Map', 'Copy IFCX': 'Copy',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
