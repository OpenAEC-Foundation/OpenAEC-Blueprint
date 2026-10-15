// Current OpenCADStudio core registry at 77f19dafd017; Layout is a side-toolbar module.
const beforeCadGroups = groups;
const cadGroups = {
  'Tekenen': [
    ['Draw', ['Line', 'Polyline', 'Circle', 'Arc']],
    ['Modify', ['Move', 'Copy', 'Rotate']],
    ['Annotation', ['Text', 'Dimension']],
    ['Layers', ['Layers']], ['Block', ['Create Block', 'Insert Block']],
    ['Properties', ['Match Properties']], ['Groups', ['Group', 'Ungroup']],
    ['Clipboard', ['Paste']], ['Measure', ['Measure']],
  ],
  'Parametrisch': [['Geometric', ['Constraints']], ['Dimensional', ['Linear']], ['Manage', ['Parameters']]],
  'Model': [['Create', ['Box']], ['Boolean', ['Union']], ['Edges', ['Fillet Edge']]],
  'Invoegen': [['Reference', ['Attach Underlay']], ['Block', ['Insert Block']], ['Block Definition', ['Create Block']], ['Import', ['Import']], ['Content', ['Content']]],
  'Annoteren': [['Text', ['Multiline Text']], ['Dimensions', ['Dimension']], ['Centerlines', ['Centerline']], ['Leaders', ['Multileader']], ['Tables', ['Table']], ['Markup', ['Revision Cloud']], ['Annotation Scaling', ['Add Current Scale']]],
  'Beeld': [['Viewport Tools', ['Viewport']], ['Navigate', ['Zoom']], ['Model Viewports', ['Model Viewport']], ['Preset', ['Views']], ['Palettes', ['Properties']], ['Interface', ['File Tabs']], ['Plot', ['Page Setup']]],
  'Beheren': [['Customization', ['Tool Palettes']], ['Cleanup', ['Purge']], ['Application', ['Options']]],
};
groups = function (tab, app) {
  return app.id === 'cad' ? (cadGroups[tab] || []) : beforeCadGroups(tab, app);
};
Object.assign(iconMap, {
  'Insert Block': 'import', 'Attach Underlay': 'import', 'Import': 'import',
  'Content': 'open', 'Properties': 'panelleft', 'Options': 'settings',
  'Parameters': 'settings', 'Page Setup': 'settings', 'Measure': 'measure',
});
Object.assign(calcIconFiles, Object.fromEntries(Object.entries({
  'Line': 'Pen', 'Polyline': 'GitBranch', 'Circle': 'Circle', 'Arc': 'Compass',
  'Move': 'MoveHorizontal', 'Copy': 'Copy', 'Rotate': 'RotateCw',
  'Text': 'FileText', 'Dimension': 'Gauge', 'Layers': 'Layers',
  'Create Block': 'Boxes', 'Match Properties': 'Pencil',
  'Group': 'Boxes', 'Ungroup': 'Boxes', 'Paste': 'ClipboardCheck',
  'Constraints': 'GitBranch', 'Linear': 'Gauge', 'Box': 'Boxes',
  'Union': 'Boxes', 'Fillet Edge': 'RotateCw', 'Multiline Text': 'FileText',
  'Centerline': 'Minus', 'Multileader': 'GitBranch', 'Table': 'LayoutGrid',
  'Revision Cloud': 'Circle', 'Tool Palettes': 'LayoutGrid', 'Purge': 'Eraser',
}).map(([label, file]) => [label, calcIconRoot + file + '.svg'])));
