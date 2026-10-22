"""Curated revision 99 refinements; preserve width when freeing action marks."""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points

OFFSETS = {'document.from-clipboard-image': {'primary': [-1, 0], 'accent': [1, 0]}, 'file.list-add': {'primary': [0, 0], 'accent': [1, 0]}, 'resource.clear-level': {'primary': [0, 1], 'accent': [1, -3]}, 'planning.baselines': {'primary': [0, 0], 'accent': [1, 0]}, 'planning.bar-colors': {'primary': [0, 0], 'accent': [0, 1]}, 'resource.availability-step-add': {'primary': [0, 0], 'accent': [0, -1]}, 'planning.code-value-add': {'primary': [0, -1], 'accent': [0, 0]}, 'planning.custom-field-add': {'primary': [0, 0], 'accent': [-1, 0]}, 'ai.bridge-start': {'primary': [-1, 0], 'accent': [0, 0]}, 'ai.bridge-stop': {'primary': [-1, -1], 'accent': [0, 0]}, 'input.time-increase': {'primary': [0, 1], 'accent': [0, -1]}, 'input.time-decrease': {'primary': [0, -1], 'accent': [0, 1]}, 'diagnostics.run-benchmark': {'primary': [-1, -1], 'accent': [0, 1]}, 'guide.tutorial-start': {'primary': [0, 0], 'accent': [0, 1]}, 'calendar.work-band-add': {'primary': [0, 0], 'accent': [1, 0]}}

SETTINGS = {'preferences.annotations','preferences.page-display','printer.virtual-settings','symbol.library-settings'}
ACTIONS = {
 'data.excel-refresh':('table','refresh'), 'session.restore':('page','refresh'), 'extension.reinstall-file':('package','refresh'),
 'extension.uninstall':('package','minus'), 'planning.clear-status-date':('calendar','cross'),
 'company.new':('book','plus'), 'calendar.new':('calendar','plus'),
 'table.column-add-menu':('table','plus'), 'table.columns-reset':('table','refresh'),
 'table.column-hide':('table','minus'), 'activity.clear':('log','cross'),
 'capture.clear-annotations':('image','cross'), 'log.pause-view':('log','pause'),
 'log.resume-view':('log','play'), 'planning.profile-new':('profile','plus'),
 'software.launch':('window','play'), 'software.open-webtab':('tab','right'),
 'software.install':('package','down'), 'software.update':('package','refresh'),
 'view.web-reload':('window','refresh'),
}
ACCENT_ROLES = {'status.resource-overallocated','status.bridge-live','status.bridge-off','extension.runtime-desktop','extension.runtime-browser','status.column-present','help.context-hint','status.library-suggestion','status.install-size-smaller','status.install-size-larger','planning.dependency-draw-mode','status.recorded-dates','status.software-installed','status.version-upgrade'}
SCREENSHOT_KEYS = {'symbol.system-types','link.open-internal','update.previous-download','planning.move-date','resource.workspace','status.resource-overallocated','file.examples','ui.tour','layout.equipment','layout.tools','credential.regenerate','ai.connection-menu','ai.connection-details','status.bridge-live','status.bridge-off','extension.runtime-desktop','extension.runtime-browser','guide.compact','status.column-present','help.context-hint','status.library-suggestion','input.confirm-draft','status.install-size-smaller','status.install-size-larger','planning.dependency-draw-mode','status.recorded-dates','status.software-installed','status.version-upgrade'}
CUSTOM = SCREENSHOT_KEYS | {'assistant.detect-doors','product.no-vendor-lock','panel.links','symbol.category-site','backup.recover','tree.collapse-scope','tree.expand-scope','tools.category-geotechniek','tools.category-bim','tools.category-ai','tools.category-energie'}
FINAL_REFINEMENTS={'draw.schedule-table','view.zoom-tool','comments.import','comments.export','validation.select-specification','validation.reset','preferences.printing','panel.document-navigation','report.view-build'}
KEYS=set(OFFSETS)|SETTINGS|set(ACTIONS)|CUSTOM|FINAL_REFINEMENTS

def fill(c, points, accent=True):
 s=c.size/24
 c.fills.append({'tone':'accent' if accent else 'primary','rings':[[(x*s,y*s) for x,y in points]]})

def clear(c):
 c.paths.clear();c.circles.clear();c.fills.clear()

def head(c, kind):
 if kind=='printer':
  box(c,7,2,10,5);box(c,2,7,20,7);box(c,7,11,10,5)
 else:
  box(c,3,2,18,12)
  if kind in {'window','tab','package','calendar','table','profile'}:c.line([(3,6),(21,6)],radius=0)
  if kind in {'book','tab','table'}:c.line([(9,2),(9,14 if kind!='tab' else 6)],radius=0)
  if kind=='table':c.line([(3,10),(21,10)],radius=0)
  if kind=='package':c.line([(8,2),(8,6)],radius=0)
  if kind=='calendar':
   for x in (8,16):c.line([(x,1.5),(x,4)],radius=0)
  if kind in {'page','log'}:
   for y in ((6,) if kind=='page' else (6,10)):c.line([(7,y),(17,y)],radius=0)
  if kind=='profile':
   c.circle(7,10,.7,filled=True);c.line([(11,10),(17,10)],radius=0)
  if kind=='image':
   c.circle(8,6,.8,filled=True);c.line([(6,11),(10,8),(13,11),(16,8),(19,11)],radius=.3)

def circular_mark(c,x,y,r):
 # End with a straight tangent before the arrowhead. The inner wing ends in
 # the empty centre, rather than merging into the circular stroke below it.
 c.line(arc_points(x,y,r,270,540,48),True,radius=0)
 wing=min(r,3)
 rise=min(r*.75,2.5)
 tip=(x-r,y-rise)
 c.line([(x-r,y),tip],True,radius=0)
 c.line([(x-r-wing,y),tip,(x-r+wing,y)],True,radius=0)


def badge(c,kind):
 if kind=='plus':c.plus(12,20,2.5)
 elif kind=='minus':c.line([(9.5,20),(14.5,20)],True,radius=0)
 elif kind=='cross':
  c.line([(10,18),(14,22)],True,radius=0);c.line([(10,22),(14,18)],True,radius=0)
 elif kind=='refresh':
  circular_mark(c,12,20,3)
 elif kind=='play':c.line([(9.5,17),(15,20),(9.5,23)],True,closed=True,radius=.3)
 elif kind=='pause':
  for x in (10,14):c.line([(x,17.5),(x,22.5)],True,radius=0)
 elif kind=='right':
  c.line([(7,20),(17,20)],True,radius=0);c.line([(14.5,17.5),(17,20),(14.5,22.5)],True,radius=.2)
 elif kind=='down':
  c.line([(12,17),(12,23)],True,radius=0);c.line([(9.5,20.5),(12,23),(14.5,20.5)],True,radius=.2)
 elif kind=='settings':
  for a,b,tick in ((3,10,6),(14,21,18)):
   c.line([(a,20),(b,20)],True,radius=0);c.line([(tick,18.5),(tick,21.5)],True,radius=0)

def shift(c, offsets):
 s=c.size/24
 for path in c.paths:
  dx,dy=offsets[path['tone']];path['points']=[(x+dx*s,y+dy*s) for x,y in path['points']]
 for circle in c.circles:
  dx,dy=offsets[circle['tone']];circle['x']+=dx*s;circle['y']+=dy*s
 for part in c.fills:
  dx,dy=offsets[part['tone']];part['rings']=[[(x+dx*s,y+dy*s) for x,y in ring] for ring in part['rings']]

def refine(c,key):
 if key not in KEYS:return
 if key in FINAL_REFINEMENTS:
  final_refine(c,key);return
 if key in OFFSETS:shift(c,OFFSETS[key]);return
 if key in SCREENSHOT_KEYS:
  screenshot_refine(c,key);return
 clear(c)
 if key in SETTINGS:
  kind={'preferences.annotations':'page','preferences.page-display':'window','printer.virtual-settings':'printer','symbol.library-settings':'book'}[key]
  head(c,kind)
  if key=='preferences.annotations':c.line([(8,11),(14,5)],radius=0)
  badge(c,'settings')
 elif key in ACTIONS:
  main,action=ACTIONS[key];head(c,main);badge(c,action)
 elif key in {'tree.collapse-scope','tree.expand-scope'}:
  for y in (3,21):c.line([(4,y),(20,y)],radius=0)
  if key=='tree.collapse-scope':pairs=[[(8,6),(12,10),(16,6)],[(8,18),(12,14),(16,18)]]
  else:pairs=[[(8,10),(12,6),(16,10)],[(8,14),(12,18),(16,14)]]
  for points in pairs:c.line(points,True,radius=.3)
 elif key=='tools.category-geotechniek':
  face=[(3,7),(12,3),(21,7),(12,11)]
  fill(c,face);c.line(face,True,closed=True,radius=.3)
  for y in (12,17):c.line([(3,y),(12,y+4),(21,y)],radius=.3)
 elif key=='assistant.detect-doors':
  box(c,7,3,10,18)
  c.circle(13.5,13,.75,filled=True)
  c.line([(5,22),(19,22)],radius=0)
  for x,dx in ((3,1.5),(21,-1.5)):
   c.line([(x+dx,3),(x,3),(x,7)],True,radius=.6)
   c.line([(x,17),(x,21),(x+dx,21)],True,radius=.6)
 elif key=='product.no-vendor-lock':
  c.line([(14,10),(14,3),(3,3),(3,21),(9,21)],radius=1)
  box(c,14,16,8,6,True)
  c.line([(15.3,16),(15.3,14)],True,radius=0)
  c.line(arc_points(18,14,2.7,180,330,32),True,radius=0)
 elif key=='panel.links':
  box(c,2,2,20,20);c.line([(2,6),(22,6)],radius=0)
  c.line([(10.5,11.5),*arc_points(7.5,14.5,3,270,90,24),(10.5,17.5)],True,radius=0)
  c.line([(13.5,11.5),*arc_points(16.5,14.5,3,270,450,24),(13.5,17.5)],True,radius=0)
  c.line([(9,14.5),(15,14.5)],True,radius=0)
 elif key=='symbol.category-site':
  c.line([(7,3),(7,22)],radius=0)
  c.line([(2,7),(22,7)],radius=0)
  c.line([(7,3),(20,7)],radius=0)
  c.line([(3,22),(11,22)],radius=0)
  fill(c,[(2,6),(5,6),(5,9),(2,9)],False)
  c.line([(18,10),(18,17)],True,radius=0)
  c.line(arc_points(19.5,17,1.5,180,0,24),True,radius=0)
  c.line([(21,17),(21,16)],True,radius=0)
 elif key=='backup.recover':
  c.line([(18,9),(18,6),(14,2),(3,2),(3,21),(8,21)],radius=.7)
  c.line([(14,2),(14,6),(18,6)],radius=.3)
  circular_mark(c,17.5,17.5,4.5)
 elif key=='tools.category-bim':
  # Complete upper face, with a neutral vertical front edge.
  back=(12,4);right=(12+4*math.sqrt(3),8);left=(12-4*math.sqrt(3),8);front=(12,12)
  c.line([back,right,(right[0],16),(12,20),(left[0],16),left],closed=True,radius=.4)
  c.line([front,(12,20)],radius=0)
  fill(c,[back,right,front,left])
 elif key=='tools.category-ai':
  points=[(6,6),(18,6),(6,18),(18,18)]
  # Stop neutral edges at the circular outlines instead of crossing their interiors.
  for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3)):
   a,b=points[i],points[j];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);trim=4
   c.line([(a[0]+dx*trim/length,a[1]+dy*trim/length),(b[0]-dx*trim/length,b[1]-dy*trim/length)],radius=0)
  for x,y in points:c.circle(x,y,3,True)
 elif key=='tools.category-energie':
  c.line([(2,11),(12,3),(22,11)],radius=.3)
  c.line([(5,10),(5,21),(19,21),(19,10)],radius=.4)
  # A single filled bolt stays clear of the roof and floor, including at 16 px.
  fill(c,[(12.5,8.5),(8.5,14.5),(12,14.5),(11,18),(15.5,11.5),(12,11.5)])


def screenshot_refine(c,key):
 # Explicitly requested accents preserve the existing status meaning and role.
 if key in {'extension.runtime-desktop','extension.runtime-browser','help.context-hint','status.recorded-dates'}:
  paths={'extension.runtime-desktop':[-1],'extension.runtime-browser':[-2,-1],'help.context-hint':[-1],'status.recorded-dates':[]}[key]
  for i in paths:c.paths[i]['tone']='accent'
  if key in {'extension.runtime-browser','help.context-hint','status.recorded-dates'}:
   for circle in c.circles:circle['tone']='accent'
  return
 if key in {'status.install-size-smaller','status.install-size-larger'}:
  # A taller free arrow beside the package, with no grazing contact.
  clear(c);box(c,2,3,11,18);c.line([(2,8),(13,8)],radius=0)
  c.line([(20,4),(20,20)],True,radius=0)
  c.line([(17,17),(20,20),(23,17)] if key.endswith('smaller') else [(17,7),(20,4),(23,7)],True,radius=.3)
  return
 clear(c)
 if key=='symbol.system-types':
  for x,y in ((3,3),(14,3),(3,14),(14,14)):box(c,x,y,7,7,x==14 and y==14)
 elif key=='link.open-internal':
  box(c,2,2,20,20)
  c.line([(6.5,8),(15,8),(15,16.5)],True,radius=.5)
  c.line([(11.5,13),(15,16.5),(18.5,13)],True,radius=.3)
 elif key=='update.previous-download':
  box(c,2,3,10,18)
  c.line([(22,7),(19,7),(19,18)],True,radius=.5)
  c.line([(16,15),(19,18),(22,15)],True,radius=.3)
 elif key=='planning.move-date':
  c.line([(3,3),(3,21),(22,21)],radius=.3)
  for y in (12,16.5):c.line([(7,y),(17,y)],radius=0)
  c.line([(8,5.5),(21,5.5)],True,radius=0)
  c.line([(18,2.5),(21,5.5),(18,8.5)],True,radius=.3)
 elif key=='planning.dependency-draw-mode':
  # Two separate tasks and one free orthogonal relation arrow, without a cursor.
  box(c,2,3,8,5);box(c,14,16,8,5)
  c.line([(13.5,5.5),(18,5.5),(18,12.5)],True,radius=.6)
  c.line([(15.5,10),(18,12.5),(20.5,10)],True,radius=.3)
 elif key=='resource.workspace':
  box(c,2,2,20,20);c.line([(2,6),(22,6)],radius=0)
  c.circle(12,11,2,True)
  c.line(arc_points(12,18.5,3.5,180,360,24),True,radius=0)
 elif key=='status.resource-overallocated':
  c.line([(12,2),(23,21),(1,21)],closed=True,radius=.5)
  c.circle(12,10,2,True);c.line(arc_points(12,18,3.3,180,360,24),True,radius=0)
 elif key=='file.examples':
  c.line([(2,4),(7,4),(12,6),(17,4),(22,4),(22,20),(17,20),(12,22),(7,20),(2,20)],closed=True,radius=.4)
  c.line([(12,6),(12,22)],radius=0)
  # Text follows the two page planes, including their equal slopes.
  c.line([(5,9),(8,9.4)],True,radius=0);c.line([(5,14),(8,14.4)],True,radius=0)
  c.line([(16,9.4),(19,9)],True,radius=0)
 elif key=='ui.tour':
  box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
  for x in (6,12,18):c.circle(x,12,1,True,True)
  c.line([(6,17),(18,17)],True,radius=0)
  c.line([(15.5,14.5),(18,17),(15.5,19.5)],True,radius=.3)
 elif key=='layout.equipment':
  box(c,2,4,12,11,True)
  c.line([(17,8),(19,8),(22,12),(22,16),(17,16)],radius=.3)
  for x in (6,19):c.circle(x,20,2)
 elif key=='layout.tools':
  # A single spanner silhouette: open jaws and a long, attached handle.
  # Colour transitions meet at the two shoulders; they are not separate parts.
  c.line([*arc_points(7,7,5,0,-90,24),(7,5),(5,7),(2,7),
          *arc_points(7,7,5,180,90,24)[1:]],True,radius=0)
  c.line([(7,12),*arc_points(19,19,math.sqrt(8),135,-45,32),(12,7)],radius=0)
 elif key=='credential.regenerate':
  box(c,2,3,20,7)
  for x in (6,12,18):c.circle(x,6.5,.65,filled=True)
  circular_mark(c,12,18.5,3.5)
 elif key in {'ai.connection-menu','ai.connection-details'}:
  box(c,2,2,20,20);c.line([(2,6),(22,6)],radius=0)
  c.line([(7,9.5),(7,12),(14,12),(14,9.5)],True,radius=.3)
  c.line(arc_points(10.5,12,3.5,0,180,24),True,radius=0)
  c.line([(10.5,15.5),(10.5,18.5)],True,radius=0)
  if key=='ai.connection-menu':c.line([(17,16),(18.5,17.5),(20,16)],True,radius=.2)
  else:
   c.circle(18.5,10,.6,False,True);c.line([(18.5,13),(18.5,16)],radius=0)
 elif key in {'status.bridge-live','status.bridge-off'}:
  c.line([(5,5),(5,10),(14,10),(14,5)],True,radius=.3)
  c.line(arc_points(9.5,10,4.5,0,180,24),True,radius=0)
  c.line([(9.5,14.5),(9.5,19)],True,radius=0)
  if key.endswith('live'):c.line([(15,19),(18,22),(23,15)],radius=.3)
  else:c.line([(18,5),(22,9)],radius=0);c.line([(22,5),(18,9)],radius=0)
 elif key=='guide.compact':
  box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
  for y in (12,17):c.line([(6,y),(10,y)],radius=0)
  c.line([(14,16),(17,13),(20,16)],True,radius=.3)
 elif key in {'status.column-present','input.confirm-draft','status.software-installed'}:
  box(c,2,2,20,20)
  if key in {'status.column-present','status.software-installed'}:c.line([(2,7),(22,7)],radius=0)
  if key=='status.column-present':c.line([(7,2),(7,22)],radius=0)
  if key=='input.confirm-draft':c.line([(6,7),(16,7)],radius=0)
  c.line([(10,15),(13,18),(18.5,11.5)],True,radius=.3)
 elif key in {'status.library-suggestion','status.version-upgrade'}:
  box(c,1.5,5,5,14);box(c,17.5,5,5,14)
  c.line([(10,12),(14,12)],True,radius=0)
  c.line([(12,10),(14,12),(12,14)],True,radius=.2)


def final_refine(c,key):
 if key=='draw.schedule-table':
  c.paths[2]['points']=[(9.5*c.size/24,8*c.size/24),(17.5*c.size/24,8*c.size/24)];return
 if key=='view.zoom-tool':
  c.paths[-1]['points']=[(17*c.size/24,3*c.size/24),(22*c.size/24,3*c.size/24)];return
 if key=='preferences.printing':
  c.paths[-1]['points']=[(22*c.size/24,9*c.size/24),(22*c.size/24,21*c.size/24)]
  c.circles=[part for part in c.circles if part['tone']!='accent']
  c.line([(21,15),(23,15)],True,radius=0);return
 clear(c)
 if key=='report.view-build':
  box(c,4,2,16,20)
  c.line([(7,10),(12,6),(17,10)],True,radius=.3)
  c.line([(7,10),(7,18),(17,18),(17,10)],radius=.3)
  c.line([(10.5,18),(10.5,14),(13.5,14),(13.5,18)],radius=.3)
 elif key in {'comments.import','comments.export'}:
  c.line([(19,6.5),(19,3),(3,3),(3,16),(6,16),(6,21),(11,16),(13,16)],radius=.6)
  left=key.endswith('import');tip=14 if left else 23;back=17 if left else 20
  c.line([(23 if left else 14,12.5),(tip,12.5)],True,radius=0)
  c.line([(back,9.5),(tip,12.5),(back,15.5)],True,radius=.3)
 elif key in {'validation.select-specification','validation.reset'}:
  c.line([(19,9),(19,3),(3,3),(3,21),(9,21)],radius=1)
  for y,end in ((7,15),(12,13)):
   c.circle(7,y,.65,filled=True);c.line([(11,y),(end,y)],radius=0)
  if key.endswith('reset'):circular_mark(c,18,18,4.3)
  else:c.line([(14,15),(18,19),(22,15)],True,radius=.3)
 elif key=='panel.document-navigation':
  box(c,2,3,20,18);c.line([(2,8),(22,8)],radius=0);c.line([(11,8),(11,21)],radius=0)
  fill(c,[(5,11),(8,11),(8,18),(5,18)])
