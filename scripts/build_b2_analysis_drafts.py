"""Original visual proposals, kept separate from canonical B2 masters."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
from b2_geometry import Construction, export_svg
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_reports_completion import glyph
from b2_icon_placement_refinements import head, badge

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'design/icon-set-b2'


def fill(c, points, accent=True):
    s = c.size / 24
    c.fills.append({'tone': 'accent' if accent else 'primary', 'rings': [[(x*s, y*s) for x, y in points]]})


def magnifier(c):
    c.circle(19.5, 15, 2.8, True)
    c.line([(21.5,17),(23,19)], True, radius=0)


def document(c):
    box(c, 3, 2, 18, 20)


def hierarchy(c, lower=False):
    document(c)
    box(c,9,5,6,4,not lower)
    c.line([(12,9),(12,15)],radius=0)
    box(c,9,15,6,4,lower)


def proposal(key, size):
    c=Construction(key,size,1.25 if size==16 else 1.75)
    if key=='thermal.window':
        for y in (10,15):
            c.line([(2,y),(6,y)],radius=0);c.line([(18,y),(22,y)],radius=0)
        box(c,6,5,12,15);c.line([(12,5),(12,20)],radius=0)
        c.line([(8.5,12),(10,9)],True,radius=0);c.line([(14,16),(15.5,13)],True,radius=0)
    elif key=='thermal.room-split':
        box(c,2,4,20,16)
        for y in (7,13):c.line([(12,y),(12,y+4)],True,radius=0)
    elif key=='construction.studs-toggle':
        box(c,2,6,20,12)
        for x in (6,15):fill(c,[(x,9),(x+3,9),(x+3,15),(x,15)])
    elif key=='pile.load-points':
        c.line([(2,20),(12,20)],radius=0)
        for x in (4,10):
            c.line([(x,4),(x,11)],radius=0)
            c.line([(x-1.5,9),(x,11),(x+1.5,9)],radius=0)
            c.circle(x,16,.8,filled=True)
        magnifier(c)
    elif key=='pile.cpts':
        c.line([(2,3),(2,21),(12,21)],radius=0)
        c.line([(6,4),(10,7),(5,10),(9,13),(6,17)],radius=.5)
        magnifier(c)
    elif key=='pile.optimization':
        c.line([(2,3),(2,21),(22,21)],radius=0)
        for x,y in ((6,17),(10,12),(15,8)):c.circle(x,y,1,filled=True)
        c.circle(19,5,2,True,filled=True)
    elif key=='pile.tip-regions':
        c.line([(2,3),(13,3),(13,9),(22,9),(22,21),(2,21)],closed=True,radius=.6)
        fill(c,[(5,12),(11,12),(11,18),(5,18)])
    elif key=='pile.load-groups':
        for x in (1.5,14.5):box(c,x,4,8,16)
        for x,y in ((4.5,9),(6.5,15),(17.5,9),(19.5,15)):c.circle(x,y,.8,True,filled=True)
    elif key=='quotation.type-private':
        c.line([(21,7.5),(21,3),(3,3),(3,21),(9,21)],radius=1)
        c.line([(7,7),(15,7)],radius=0)
        c.circle(18,12,2,True)
        c.line(arc_points(18,22,4,180,360,24),True,radius=0)
    elif key=='quotation.type-raw':
        document(c)
        fill(c,[(7,6),(17,6),(17,9),(7,9)])
        for y in (13,18):c.line([(7,y),(17,y)],radius=0)
    elif key=='quotation.payment-terms':
        box(c,2,5,20,16)
        for x in (7,17):c.line([(x,2),(x,5)],radius=0)
        c.line([(2,9),(22,9)],radius=0)
        c.circle(8,12,.8,True,filled=True);c.circle(16,18,.8,True,filled=True)
        c.line([(8,18),(16,11)],True,radius=0)
    elif key in {'report.view-main-contract','report.view-subcontract'}:
        hierarchy(c,key.endswith('subcontract'))
    elif key=='report.view-tender':
        document(c)
        c.line([(12,5),(12,19)],radius=0)
        for y in (10,15):c.line([(7,y),(17,y)],radius=0)
        fill(c,[(7,6),(10,6),(10,8),(7,8)])
    elif key in {'report.view-build','report.view-ibis'}:
        document(c)
        glyph(c,'1' if key.endswith('build') else '2',8,6,8,13,True)
    elif key=='report.view-estimate':
        document(c)
        for y in (7,12):
            c.line([(6,y),(10,y)],radius=0);c.line([(15,y),(18,y)],radius=0)
        c.line([(6,18),(18,18)],True,radius=0)
    elif key=='calc.quantities-visible':
        box(c,2,3,20,18);c.line([(10,3),(10,21)],radius=0)
        c.line([(2,8),(22,8)],radius=0)
        for y in (12,17):c.line([(5,y),(7,y)],radius=0)
        glyph(c,'1',14,11,4,7,True)
    elif key in {'calc.grid-standard','calc.grid-wpcalc','calc.grid-simple'}:
        box(c,2,3,20,18)
        c.line([(2,8),(22,8)],radius=0)
        if key.endswith('standard'):
            for x in (9,15):c.line([(x,3),(x,21)],radius=0)
            fill(c,[(5,11),(7,11),(7,18),(5,18)])
        elif key.endswith('wpcalc'):
            c.line([(13,3),(13,21)],radius=0)
            c.line([(5,11),(5,17),(10,17)],True,radius=.4)
            c.line([(16,12),(19,12)],radius=0)
        else:
            c.line([(12,3),(12,21)],radius=0)
            for y in (12,17):c.line([(5,y),(9,y)],True,radius=0)
    elif key=='calc.chapter':
        document(c);fill(c,[(6,5),(18,5),(18,8),(6,8)])
        c.line([(7,13),(17,13)],radius=0);c.line([(10,18),(17,18)],radius=0)
    else:
        return next_proposal(key, size)
    return c



def pencil(c):
    # Full diagonal pencil: pointed wood end, parallel barrel and separate end cap.
    c.line([(12,22),(13,18),(20,11),(23,14),(16,21)],True,closed=True,radius=.25)
    c.line([(18.5,12.5),(21.5,15.5)],True,radius=0)



def lock(c,x,y,accent=True):
    # A rounded shackle above a properly proportioned, closed lock case.
    c.line(arc_points(x,y,2.7,180,360,32),accent,radius=0)
    box(c,x-4,y,8,6,accent)



def clock_mark(c,x,y,r):
    c.circle(x,y,r,True)
    s=r/4.2
    fill(c,[(x+dx*s,y+dy*s) for dx,dy in [(-.6,-2.1),(.6,-2.1),(.6,-.6),(2.1,-.6),(2.1,.6),(-.6,.6)]])


def feedback_proposal(key,size):
    keys={'image.embedded-edit','capture.annotate','calendar.edit','panel.attachments','file.place-add','backup.folder','panel.warnings',
          'planning.status-date','status.hour-data','ai.read-only-toggle',
          'status.schedule-preview','status.schedule-last-result',
          'status.library-item-missing','status.library-item-deviated','status.structure-locked'}
    if key not in keys:return None
    c=Construction(key,size,1.25 if size==16 else 1.75)
    if key in {'image.embedded-edit','capture.annotate','calendar.edit'}:
        c.line([(21,9),(21,4),(3,4),(3,21),(8,21)],radius=1)
        if key=='calendar.edit':
            c.line([(3,8),(21,8)],radius=0)
            for x in (8,16):c.line([(x,2),(x,6)],radius=0)
            for x in (7,11):c.circle(x,12,.7,filled=True)
        else:
            c.circle(8,8,1.1,filled=True)
            c.line([(6,16),(10,12),(12,14)],radius=.3)
        pencil(c)
    elif key=='panel.attachments':
        # A complete upper/left panel contour, with a large diagonal clip at its corner.
        c.line([(21,9),(21,3),(3,3),(3,21),(8,21)],radius=1)
        c.line([(3,7),(21,7)],radius=0)
        # Original capsule spiral, rotated 40 degrees to read as a paperclip.
        points=[(1,-3),(1,4),*arc_points(-1,4,2,0,180,24),(-3,-4),
                *arc_points(1,-4,4,180,360,32),(5,4),
                *arc_points(-1,4,6,0,180,40),(-7,-5)]
        angle=math.radians(40)
        c.line([(16+(x*math.cos(angle)-y*math.sin(angle))*.72,
                    14.5+(x*math.sin(angle)+y*math.cos(angle))*.72) for x,y in points],True,radius=0)
    elif key in {'file.place-add','backup.folder'}:
        # Preserve normal folder height; leave a corner clear for the independent mark.
        c.line([(20,11),(20,7),(11,7),(8,3),(2,3),(2,21),(12 if key=='file.place-add' else 9.5,21)],radius=1)
        if key=='file.place-add':c.plus(20,19,2.8)
        else:
            from b2_icon_placement_refinements import circular_mark
            circular_mark(c,19,18.5,3.7)
    elif key=='panel.warnings':
        box(c,3,2,18,20);c.line([(3,7),(21,7)],radius=0)
        rings=[[(12,10),(6.5,19),(17.5,19)],[(11.35,13),(12.65,13),(12.65,15.7),(11.35,15.7)],arc_points(12,17.5,.65,0,360,32)]
        scale=c.size/24
        c.fills.append({'tone':'accent','rings':[[(x*scale,y*scale) for x,y in ring] for ring in rings]})
    elif key in {'planning.status-date','status.hour-data'}:
        box(c,3,4,18,19);c.line([(3,8),(21,8)],radius=0)
        for x in (8,16):c.line([(x,2),(x,6)],radius=0)
        clock_mark(c,12,16,4.2)
    elif key=='ai.read-only-toggle':
        c.line([(21,10),(21,3),(3,3),(3,21),(8,21)],radius=1)
        c.line([(3,7),(21,7)],radius=0);c.line([(7,11),(12,11)],radius=0)
        lock(c,18,16)
    elif key in {'status.schedule-preview','status.schedule-last-result'}:
        c.line([(21,10),(21,3),(3,3),(3,21),(8,21)],radius=1)
        c.line([(7,7),(16,7)],radius=0)
        if key=='status.schedule-preview':
            from b2_icon_placement_refinements import circular_mark
            circular_mark(c,18,18,4.3)
        else:
            clock_mark(c,18,18,4.3)
    elif key in {'status.library-item-missing','status.library-item-deviated'}:
        c.line([(20,10),(20,3),(3,3),(3,21),(9,21)],radius=1)
        c.line([(8,3),(8,21)],radius=0)
        if key=='status.library-item-missing':
            c.circle(17.5,17.5,4.5,True);c.line([(15.4,17.5),(19.6,17.5)],True,radius=0)
        else:
            for y in (15,20):c.line([(13, y),(22,y)],True,radius=0)
            c.line([(20,12),(15,23)],True,radius=0)
    elif key=='status.structure-locked':
        box(c,8,2,12,5);box(c,8,10,5,5)
        c.line([(3,3),(3,21),(7,21)],radius=.5)
        for y,x in ((4.5,8),(12.5,8)):c.line([(3,y),(x,y)],radius=0)
        lock(c,19,17)
    return c


def next_proposal(key,size):
    revised=feedback_proposal(key,size)
    if revised is not None:return revised
    c=Construction(key,size,1.25 if size==16 else 1.75)
    if key in {'page.insert-file','bcf.import'}:
        c.line([(21,9),(21,3),(3,3),(3,21),(9,21)],radius=1)
        if key=='bcf.import':
            for y,end in ((7,15),(12,13)):
                c.circle(7,y,.65,filled=True);c.line([(11,y),(end,y)],radius=0)
        else:c.line([(7,7),(15,7)],radius=0)
        c.line([(23,17),(13,17)],True,radius=0)
        c.line([(16,14),(13,17),(16,20)],True,radius=.3)
        return c
    if key=='calendar.promote-menu':
        c.line([(21,9),(21,4),(3,4),(3,21),(8,21)],radius=1)
        c.line([(3,8),(21,8)],radius=0)
        for x in (8,16):c.line([(x,2),(x,6)],radius=0)
        for y in (15,20):c.line([(14,y),(22,y)],True,radius=0)
        return c
    if key=='library.link-recognized':
        c.line([(20,10),(20,3),(3,3),(3,21),(8,21)],radius=1)
        c.line([(8,3),(8,21)],radius=0)
        c.line([(15,15.5),*arc_points(14,18,2.5,270,90,24),(15,20.5)],True,radius=0)
        c.line([(19,15.5),*arc_points(20,18,2.5,270,450,24),(19,20.5)],True,radius=0)
        c.line([(14.5,18),(19.5,18)],True,radius=0)
        return c
    simple={
      'workspace.dock-back':('window','right'), 'file.place-add':('folder','plus'),
      'page.replace':('copies','swap'),
      'bcf.import':('issues','right'), 'layout.manage':('window','settings'),
      'backup.auto':('copies','refresh'), 'backup.create':('copies','plus'),
      'backup.folder':('folder','refresh'), 'update.install':('package','down'),
      'calendar.promote-menu':('calendar','list'), 'calendar.edit':('calendar','pencil'),
      'capture.annotate':('image','pencil'), 'image.embedded-edit':('image','pencil'), 'page.insert-file':('page','right'), 'ai.read-only-toggle':('log','lock'),
      'library.link-recognized':('book','link'), 'documents.new-or-open':('window','choices'),
      'status.library-item-missing':('book','minus'), 'status.library-item-deviated':('book','unequal'),
      'status.schedule-preview':('page','refresh'), 'status.schedule-last-result':('page','clock'),
      'planning.status-date':('calendar','clock'), 'status.hour-data':('calendar','clock'),
      'panel.warnings':('window','warning'), 'report.workspace':('report','none'),
    }
    if key in simple:
        main,action=simple[key]
        if key=='page.replace':
            box(c,2,2,8,11);box(c,14,2,8,11)
        elif main=='folder':
            c.line([(2,4),(9,4),(12,7),(22,7),(22,14),(2,14)],closed=True,radius=1)
        elif main=='copies':
            box(c,2,2,17,10);box(c,5,5,17,9)
        elif main=='issues':
            head(c,'page')
            for y in (6,10):c.circle(6,y,.6,filled=True)
        elif main=='report':
            box(c,2,2,20,20);c.line([(2,6),(22,6)],radius=0)
            box(c,7,9,10,10)
            for y in (12,16):c.line([(10,y),(14,y)],True,radius=0)
        else:head(c,main)
        if action in {'refresh','plus','minus','down','right','settings'}:
            badge(c,action)
            if key in {'workspace.dock-back','bcf.import','page.insert-file'}:
                for path in c.paths:
                    if path['tone']=='accent':path['points']=[(size-x,y) for x,y in path['points']]
        elif action=='swap':
            c.line([(6,17.5),(18,17.5),(16,16)],True,radius=.2)
            c.line([(18,21.5),(6,21.5),(8,23)],True,radius=.2)
        elif action=='pencil':pencil(c)
        elif action=='clock':
            c.circle(12,20,2.6,True);c.line([(12,18.3),(12,20),(13.5,20)],True,radius=0)
        elif action=='lock':
            c.line(arc_points(12,20,2.5,180,360,24),True,radius=0);box(c,8,20,8,3,True)
        elif action=='link':
            c.line([(10.5,17),*arc_points(7.5,20,3,270,90,24),(10.5,23)],True,radius=0)
            c.line([(13.5,17),*arc_points(16.5,20,3,270,450,24),(13.5,23)],True,radius=0)
            c.line([(9,20),(15,20)],True,radius=0)
        elif action=='unequal':
            for y in (18.5,21.5):c.line([(8,y),(16,y)],True,radius=0)
            c.line([(14,16.5),(10,23)],True,radius=0)
        elif action=='choices':
            c.plus(6,20,2.5);c.line([(13,20),(21,20),(18.5,17.5)],True,radius=.2)
            c.line([(18.5,22.5),(21,20)],True,radius=.2)
        elif action=='list':
            for y in (18.5,22):c.line([(8,y),(16,y)],True,radius=0)
        elif action=='warning':c.line([(12,17),(8,23),(16,23)],True,closed=True,radius=.2)
    elif key=='calc.hsb-wizard':
        box(c,2,3,20,18)
        for x in (6,15):fill(c,[(x,6),(x+3,6),(x+3,18),(x,18)])
    elif key=='symbol.category-electric':
        c.circle(12,12,9)
        for x in (8,16):c.circle(x,12,1.5,True,filled=True)
        for a,b in ((3.5,6),(18,20.5)):c.line([(12,a),(12,b)],radius=0)
    elif key=='symbol.category-custom':
        c.line([(2,4),(10,4),(13,7),(22,7),(22,21),(2,21)],closed=True,radius=1)
        c.line([(12,10),(13.5,13),(17,13.5),(14.5,16),(15,19),(12,17.5),(9,19),(9.5,16),(7,13.5),(10.5,13)],True,closed=True,radius=.3)
    elif key=='assistant.translate':
        glyph(c,'A',2,5,8,14);glyph(c,'B',14,5,8,14,True)
        c.line([(7,2),(17,2),(15,1)],True,radius=.2)
        c.line([(17,22),(7,22),(9,23)],True,radius=.2)
    elif key=='assistant.summarize':
        document(c)
        for y in (6,10):c.line([(7,y),(17,y)],radius=0)
        for y,w in ((15,7),(18,4)):c.line([(7,y),(7+w,y)],True,radius=0)
    elif key=='format.custom-color':
        c.line([*arc_points(12,12,9,60,360,48),(18,12),(16,14),(17,16)],closed=True,radius=.6)
        for x,y in ((8,7),(15,6),(6,13),(10,17)):c.circle(x,y,1.3,True,filled=True)
    elif key=='panel.attachments':
        # Four evenly spaced legs make a rounded clip, with no self-crossing.
        c.line([(19,7),(19,15),*arc_points(12,15,7,0,180,40),(5,7),
                *arc_points(10.5,7,5.5,180,360,40),(16,15),
                *arc_points(12,15,4,0,180,32),(8,7)],True,radius=0)
        c.line([(2,4),(2,22),(3,22)],radius=.5)
    elif key=='drawing.settings':
        c.line([(3,2),(3,14),(21,14)],closed=True,radius=.5)
        c.line([(6,8),(6,11),(9,11)],radius=.3);badge(c,'settings')
    elif key=='planning.calculate':
        box(c,3,2,18,20);box(c,6,5,12,4,True)
        for x,y in ((8,13),(16,13),(8,18),(16,18)):c.circle(x,y,1,filled=True)
    elif key=='wbs.auto-number':
        glyph(c,'1',3,2,3,5);glyph(c,'2',3,9,4,5)
        for y in (4.5,11.5):c.line([(10,y),(21,y)],radius=0)
        badge(c,'refresh')
    elif key=='table.columns':
        box(c,2,2,20,20);c.line([(2,7),(22,7)],radius=0)
        for x in (8,16):c.line([(x,2),(x,22)],radius=0)
        fill(c,[(10,10),(14,10),(14,19),(10,19)])
    elif key=='company.library':
        for x in (2,10,18):box(c,x,3,5,18,x==10)
        c.line([(2,7),(7,7)],radius=0);c.line([(18,7),(23,7)],radius=0)
    elif key=='resource.unlink-library':
        c.circle(12,4.5,2.3)
        c.line(arc_points(12,14.5,4.5,180,360,32),radius=0)
        c.line([(9,18),(7,18),(4.5,20.5),(7,23),(9,23)],True,radius=1)
        c.line([(15,18),(17,18),(19.5,20.5),(17,23),(15,23)],True,radius=1)
    elif key=='documents.overview':
        for y in (2,14):
            box(c,3,y,18,8);c.line([(6,y+3),(18,y+3)],True,radius=0)
    elif key=='status.structure-locked':
        box(c,3,2,7,4);box(c,14,9,7,4)
        c.line([(6.5,6),(6.5,11),(14,11)],radius=.3)
        c.line(arc_points(12,20,2.5,180,360,24),radius=0);box(c,8,20,8,3)
    elif key=='calendar.holiday-add':
        c.line([(21,9),(21,4),(3,4),(3,21),(8,21)],radius=1)
        c.line([(3,8),(21,8)],radius=0)
        for x in (8,16):c.line([(x,2),(x,6)],radius=0)
        c.line([(7,12),(11,16)],radius=0);c.line([(7,16),(11,12)],radius=0)
        c.plus(19,18,3)
    elif key=='calendar.copy-workdays':
        box(c,2,4,20,18);c.line([(2,8),(22,8)],radius=0)
        for x in (7,17):c.line([(x,2),(x,5)],radius=0)
        for x in (5,8.5,12,15.5,19):c.line([(x,16),(x,19)],True,radius=0)
        c.line([(5,12),(19,12),(17,10)],True,radius=.2)
    else:return None
    return c


def build(report_path, directory, icons=None):
    report=json.loads(report_path.read_text(encoding='utf-8'))
    made=[]
    for row in report['icons']:
        if row['decision']!='proposed' or icons and row['id'] not in icons:continue
        assets={}
        for size in (16,24):
            model=proposal(row['id'],size)
            if model is None:raise ValueError('Missing proposal: '+row['id'])
            for part in model.paths:
                points=[]
                for point in part['points']:
                    if not points or math.dist(points[-1],point)>1e-6:points.append(point)
                part['points']=points
            svg=export_svg(model)
            path=OUT/directory/'svg'/str(size)/(row['id']+'.svg')
            path.parent.mkdir(parents=True,exist_ok=True)
            temp=path.with_suffix('.draft.tmp');temp.write_text(svg,encoding='utf-8',newline='\n');os.replace(temp,path)
            assets[str(size)]={'path':path.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        row['proposal_assets']=assets
        row['proposal_status']='Getekend voorbeeld; niet toegepast op de canonieke icoonmasters.'
        made.append(row['id'])
    temp=report_path.with_suffix('.draft.tmp');temp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');os.replace(temp,report_path)
    print(f'{len(made)} concrete voorstellen / {len(made)*2} SVG-masters apart getekend.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,default=ROOT/'harmonization/icon-set-b2/analysis-review-97.json')
    parser.add_argument('--directory',default='review/analysis-97-drafts')
    parser.add_argument('--icons',nargs='+',help='Only redraw these proposal IDs.')
    args=parser.parse_args();build(args.report,args.directory,args.icons)
