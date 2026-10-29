"""Check exported B2 contours independently of construction-model geometry."""
from build_b2_feedback_review import WARNING_PREVIEW
from copy import deepcopy
from b2_icon_placement_refinements import ACCENT_ROLES
from b2_approved_proposals import APPROVED
import json
import re
import hashlib
import xml.etree.ElementTree as ET
import zipfile
from b2_source_catalog import load_catalog, source_hashes, supplemental_catalog
from b2_completion import PLANNED_KEYS, PLANNED, EXCLUDED as SCOPE_EXCLUDED
from b2_scope_audit import audit_hash, validate_scope_audit
from b2_geometry import ROOT, Polygon, Point, unary_union, foreground, ROUNDED_JOINTS, CURRENT_CHANGES, WHOLE_ACCENT
from b2_second_series import KEYS as SECOND_KEYS, SEMANTIC
from b2_window_series import KEYS as WINDOW_KEYS
from b2_text_series import KEYS as TEXT_KEYS
from b2_data_series import KEYS as DATA_KEYS
from b2_report_series import KEYS as REPORT_KEYS
from b2_ifc_series import KEYS as IFC_KEYS
from b2_tree_planning_geo import SOURCE_FUNCTIONS, SERIES as NEXT_SERIES, REUSED

from b2_energy_pile_audio import SOURCE_FUNCTIONS as LATER_SOURCES, SERIES as LATER_SERIES, REUSED as LATER_REUSED
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**LATER_SOURCES}
REUSED={**REUSED,**LATER_REUSED}

from b2_page_views import SOURCE_FUNCTIONS as PAGE_SOURCES, REUSED as PAGE_REUSED, KEYS as PAGE_KEYS
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**PAGE_SOURCES}
REUSED={**REUSED,**PAGE_REUSED}

from b2_bulk_series import SOURCE_FUNCTIONS as BULK_SOURCES, SERIES as BULK_SERIES, REUSED as BULK_REUSED, AVAILABLE_SERIES
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**BULK_SOURCES}
REUSED={**REUSED,**BULK_REUSED}

from b2_session_two import SOURCE_FUNCTIONS as SESSION_SOURCES, SERIES as SESSION_SERIES, REUSED as SESSION_REUSED, AVAILABLE_SERIES as SESSION_AVAILABLE
from b2_document_navigation import SOURCE_FUNCTIONS as NAV_SOURCES, SERIES as NAV_SERIES, REUSED as NAV_REUSED, AVAILABLE_SERIES as NAV_AVAILABLE
from b2_session_three import SOURCE_FUNCTIONS as THIRD_SOURCES, SERIES as THIRD_SERIES, REUSED as THIRD_REUSED, AVAILABLE_SERIES as THIRD_AVAILABLE
from b2_session_four import SOURCE_FUNCTIONS as FOURTH_SOURCES, SERIES as FOURTH_SERIES, REUSED as FOURTH_REUSED, AVAILABLE_SERIES as FOURTH_AVAILABLE
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**SESSION_SOURCES,**NAV_SOURCES,**THIRD_SOURCES,**FOURTH_SOURCES}
REUSED={**REUSED,**SESSION_REUSED,**NAV_REUSED,**THIRD_REUSED,**FOURTH_REUSED}

from b2_completion import SOURCE_FUNCTIONS as COMPLETION_SOURCES, REUSED as COMPLETION_REUSED, DISPATCHERS as COMPLETION_DISPATCHERS, SEMANTIC as COMPLETION_SEMANTIC
SOURCE_FUNCTIONS={**SOURCE_FUNCTIONS,**COMPLETION_SOURCES}
REUSED={**REUSED,**COMPLETION_REUSED}
SEMANTIC={**SEMANTIC,**COMPLETION_SEMANTIC}

OUT=ROOT/'design/icon-set-b2'


def sha(data):return hashlib.sha256(data).hexdigest()


def parse_layer(path):
    # Even-odd SVG rings; subtraction preserves holes without ring-orientation assumptions.
    result=Polygon()
    for ring in re.findall(r'M([^M]+?)Z',path):
        points=[tuple(map(float,p.strip().split())) for p in ring.split('L')]
        polygon=Polygon(points)
        assert polygon.is_valid,'invalid exported ring'
        result=result.symmetric_difference(polygon)
    return result


def check_svg(content,size,front='primary'):
    root=ET.fromstring(content)
    assert root.attrib['viewBox']==f'0 0 {size} {size}','wrong master'
    assert root.attrib.get('stroke')=='none','active stroke'
    order=['primary','accent'] if front=='accent' else ['accent','primary']
    paths=[n for n in root if n.tag.endswith('}path')]
    defs=[n for n in root if n.tag.endswith('}defs')]
    assert len(paths)==2 and [p.attrib['data-part'] for p in paths]==order,'paint order'
    assert not defs and len(root)==2,'unexpected gradient or definition'
    layers={}
    for node in paths:
        tone=node.attrib['data-part']
        fill='currentColor' if tone=='primary' else 'var(--icon-accent,currentColor)'
        assert node.attrib['fill']==fill,'theme token'
        assert node.attrib['fill-rule']=='evenodd'
        g=parse_layer(node.attrib['d']);layers[tone]=g
        assert g.is_valid,'invalid export'
        if not g.is_empty:
            a,b,c,d=g.bounds
            assert min(a,b)>=0 and max(c,d)<=size,'clipped export'
    assert layers['primary'].area>0,'missing primary'
    overlap=layers['primary'].intersection(layers['accent']).area
    assert overlap<0.00005,'colour overlap'
    return overlap,layers


def luminance(colour):
    rgb=[int(colour[i:i+2],16)/255 for i in (1,3,5)]
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722)))


def main():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    payload_script=(OUT/'review-data.js').read_text(encoding='utf-8').strip()
    prefix='document.getElementById("data").textContent = '
    assert payload_script.startswith(prefix) and payload_script.endswith(';')
    review=json.loads(json.loads(payload_script[len(prefix):-1]))
    review_icons={icon['id']:icon for icon in review['icons']}
    assert set(review_icons)=={icon['id'] for icon in manifest['icons']}
    for name in ('index.html','completion-review.html'):
        page=(OUT/name).read_text(encoding='utf-8')
        assert f'review-data.js?revision={manifest["revision"]}' in page
        assert page.index('review-data.js')<page.index('const d=JSON.parse')

    for name,expected in manifest['completion_modules_sha256'].items():assert sha((ROOT/'scripts'/name).read_bytes())==expected
    assert sha((ROOT/'scripts/b2_completion.py').read_bytes())==manifest['completion_generator_sha256']
    assert sha((ROOT/'scripts/build_icon_set_b2.py').read_bytes())==manifest['generator_sha256']
    assert sha((ROOT/'scripts/b2_geometry.py').read_bytes())==manifest['geometry_generator_sha256']
    assert sha((ROOT/'scripts/b2_second_series.py').read_bytes())==manifest['extension_generator_sha256']
    assert sha((ROOT/'scripts/build_b2_feedback_review.py').read_bytes())==manifest['feedback_generator_sha256']
    assert manifest['warning_preview']['colors']==WARNING_PREVIEW
    assert sha((ROOT/'scripts/b2_window_series.py').read_bytes())==manifest['window_generator_sha256']
    assert sha((ROOT/'scripts/b2_text_series.py').read_bytes())==manifest['text_generator_sha256']
    assert sha((ROOT/'scripts/b2_font_geometry.py').read_bytes())==manifest['font_generator_sha256']
    for font in manifest['font_sources'].values():assert sha((ROOT/font['source']).read_bytes())==font['sha256']
    assert sha((ROOT/'scripts/b2_data_series.py').read_bytes())==manifest['data_generator_sha256']
    assert sha((ROOT/'scripts/b2_session_three.py').read_bytes())==manifest['session_three_generator_sha256']
    assert sha((ROOT/'scripts/b2_session_four.py').read_bytes())==manifest['session_four_generator_sha256']
    assert sha((ROOT/'scripts/b2_document_navigation.py').read_bytes())==manifest['document_navigation_generator_sha256']
    assert sha((ROOT/'scripts/b2_session_two.py').read_bytes())==manifest['session_two_generator_sha256']
    assert sha((ROOT/'scripts/b2_bulk_series.py').read_bytes())==manifest['bulk_generator_sha256']
    assert sha((ROOT/'scripts/b2_page_views.py').read_bytes())==manifest['page_views_generator_sha256']
    assert sha((ROOT/'scripts/b2_energy_pile_audio.py').read_bytes())==manifest['later_groups_generator_sha256']
    assert sha((ROOT/'scripts/b2_tree_planning_geo.py').read_bytes())==manifest['next_groups_generator_sha256']
    assert sha((ROOT/'scripts/b2_ifc_series.py').read_bytes())==manifest['ifc_generator_sha256']
    assert sha((ROOT/'scripts/b2_report_series.py').read_bytes())==manifest['report_generator_sha256']
    source=ROOT/'harmonization/function-icon-catalog.json'
    assert sha(source.read_bytes())==manifest['source_catalog_sha256']
    assert sha((ROOT/'design/ontwerp-0.4/tokens-0.4.json').read_bytes())==manifest['theme_tokens_sha256']
    audit=json.loads((ROOT/'harmonization/icon-set-b2/function-plan.json').read_text(encoding='utf-8'))
    catalog=load_catalog()
    assert manifest['source_catalogs_sha256']==source_hashes()
    assert audit['source_catalogs_sha256']==source_hashes()
    assert {r['id'] for r in supplemental_catalog()['records']}<={r['record_id'] for r in audit['record_assessments']}
    for rid,reason in PLANNED.items():
        a=next(r for r in audit['record_assessments'] if r['record_id']==rid)
        assert a['assessment']=='gepland ontwerp; bronbediening ontbreekt' and reason in a['reason']
    assert {r['record_id'] for r in audit['record_assessments']}=={r['id'] for r in catalog['records']}
    assert len(audit['record_assessments'])==len(catalog['records'])
    assert {f['id'] for f in audit['clusters']}=={f['id'] for f in catalog['functions']}
    by_id={r['id']:r for r in catalog['records']}
    icon_keys={i['id'] for i in manifest['icons']}
    assert manifest['scope_audit_sha256']==audit_hash()
    basis_path=ROOT/'harmonization/icon-set-b2/basis-sources.json'
    assert manifest['basis_sources_sha256']==sha(basis_path.read_bytes())
    basis=json.loads(basis_path.read_text(encoding='utf-8'))
    for row in audit['record_assessments']:assert set(row['canonical_functions'])<=icon_keys
    validate_scope_audit(SCOPE_EXCLUDED,icon_keys,PLANNED,PLANNED_KEYS)
    for record,targets in COMPLETION_DISPATCHERS.items():
        a=next(r for r in audit['record_assessments'] if r['record_id']==record)
        assert a['assessment']=='typeafhankelijk hergebruik'
        assert a['canonical_functions']==list(targets) and set(targets)<=icon_keys
    maximum=0;count=0;sample=None
    for icon in manifest['icons']:
        assert icon['source_support']==basis.get(icon['id'])
        assert icon['source_example'] or icon['source_support'],'missing functional evidence'
        if icon['source_support']:
            assert icon['planned']==icon['source_support']['planned']
            for s in icon['source_support']['sources']:
                assert len(s['commit'])==40 and len(s['sha256'])==64 and s['url'].endswith('#L'+str(s['line']))
        assert icon['planned']==(icon['id'] in PLANNED_KEYS)
        if icon['planned']:assert 'GEPLAND ONTWERP' in icon['evidence_status'] and 'nog niet aangesloten' in icon['status']
        assert icon['rounded_joint']==(icon['id'] in ROUNDED_JOINTS)
        assert icon['foreground']==foreground(icon['id'])
        example=icon['source_example']
        if example:assert example==by_id[example['id']] and example['function_id']==SOURCE_FUNCTIONS.get(icon['id'],icon['id'])
        for size in (16,24):
            asset=icon['assets'][str(size)];content=(OUT/asset['path']).read_text(encoding='utf-8')
            # Revision 107 (issue #35) only fitted the 16 px masters to the pixel grid; the
            # reviewed designs are kept as revision 106 in review/raster-before/16.
            reviewed=(OUT/'review/raster-before/16'/(icon['id']+'.svg')).read_text(encoding='utf-8') if size==16 else content
            assert sha(content.encode())==asset['sha256'],'hash mismatch'
            assert review_icons[icon['id']]['svg'][str(size)]==content,'shared review/export mismatch'
            style=ET.fromstring(content).attrib.get('style')
            assert style==('color:var(--icon-accent,currentColor)' if icon['id'] in WHOLE_ACCENT else None),'unexpected whole-icon colour'
            assert icon['whole_icon_accent']==(icon['id'] in WHOLE_ACCENT)
            overlap,layers=check_svg(content,size,icon['foreground']);maximum=max(maximum,overlap);count+=1
            if icon['id'] in {'page.insert','page.delete'}:
                assert layers['primary'].distance(layers['accent'])>=size/16,'page badge too close'
            crossing={'page.extract':(15,12),'page.resize':(16,7),'draw.arrow':(20,4),'object.align-middle':(5,12)}
            if icon['id'] in crossing:
                x,y=crossing[icon['id']]
                assert layers['accent'].covers(Point(x*size/24,y*size/24)),'accent interrupted at crossing'
            if icon['id']=='draw.freehand':assert layers['accent'].is_empty,'freehand must use one colour'
            if icon['id'] in {'image.reset','ui.check-updates'}:
                ring=layers['accent' if icon['id']=='image.reset' else 'primary']
                for x,y in ((13.5,2.75),(13.5,5.25),(15,4),(12.75,4)):
                    assert ring.covers(Point(x*size/24,y*size/24)),'incomplete symmetric ring arrowhead'

            if icon['id'] in ROUNDED_JOINTS:
                x=18 if icon['id'] in {'edit.redo','nav.forward'} else 6
                y=10 if icon['id'].startswith('edit.') else 12
                assert layers['primary'].covers(Point(x*size/24,y*size/24)),'shaft stops before pointer'
            if icon['id'] in SEMANTIC:
                # Approved alternatives explicitly use an identifying status mark in accent.
                if icon['id'] in ACCENT_ROLES or icon['id'] in APPROVED:
                    assert layers['accent'].area>0,'requested identifying accent missing'
                else:
                    assert layers['accent'].is_empty,'status contains decorative accent'
                assert icon['semantic_color']==SEMANTIC[icon['id']]
            if icon['series']==1:
                assert (OUT/'review/approved-core'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'approved core changed'
            if icon['series']<11 and icon['id']!='planning.driving':
                assert (OUT/'review/retained-series-1-10'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'accepted series changed'
            if icon['id']=='planning.driving':
                before=(OUT/'review/retained-series-1-10'/str(size)/(icon['id']+'.svg')).read_text(encoding='utf-8')
                assert reviewed.replace(' style="color:var(--icon-accent,currentColor)"','')==before,'driving shape changed'
            if icon['series']<14 and icon['id'] not in {'thermal.openings','thermal.door','pile.new','object.rename','pile.columns','pile.encoding-conflicts','audio.speech','audio.tts','audio.meeting','pile.legend-edit'}:
                assert (OUT/'review/before-round-11-13'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'unrequested icon changed'
            if icon['series']<14 and icon['id'] not in {'object.rename','pile.legend-edit'}:
                assert (OUT/'review/before-pencil-fix'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'unrequested pencil-round change'
            if icon['series']<14:
                assert (OUT/'review/retained-series-1-13'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'previous family changed'
            if icon['series']<=14:
                assert (OUT/'review/retained-series-1-14'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'previous 125 designs changed'
            if icon['series']<=20:
                assert (OUT/'review/retained-series-1-20'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'accepted 170 changed'
            if icon['series']<=28:
                assert (OUT/'review/retained-series-1-28'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'previous 231 designs changed'
            if icon['series']<=30:
                assert (OUT/'review/retained-series-1-30'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'previous 239 designs changed'
            if icon['series']<=45:
                assert (OUT/'review/retained-series-1-45'/str(size)/(icon['id']+'.svg')).read_bytes()==reviewed.encode(),'nightly work changed existing master'
            if icon['id']=='file.open' and size==24:sample=content
    # Failure controls make sure layering, overshoot and overlap are actually rejected.
    controls=0
    for failure in ('paint order','clipped export','colour overlap'):
        root=ET.fromstring(sample)
        if failure=='paint order':root[:]=list(reversed(list(root)))
        elif failure=='clipped export':root[0].attrib['d']='M0 0L25 0L25 1L0 1Z'
        else:root[0].attrib['d']=root[1].attrib['d']
        try:check_svg(ET.tostring(root,encoding='unicode'),24)
        except AssertionError as error:
            assert str(error)==failure,(failure,str(error));controls+=1
        else:raise AssertionError('negative control not rejected: '+failure)
    contrasts=[]
    tokens=json.loads((ROOT/'design/ontwerp-0.4/tokens-0.4.json').read_text(encoding='utf-8'))
    for name,t in tokens['themes'].items():
        for role in ('text','accent','info','warning','error','success','text-secondary'):
            a,b=sorted((luminance(t['color'][role]),luminance(t['color']['panel'])))
            contrast=(b+.05)/(a+.05)
            assert contrast>=3,(name,role,contrast)
            contrasts.append({'theme':name,'role':role,'on':'panel','contrast':round(contrast,3),'minimum':3})
    for name,t in tokens['themes'].items():
        a,b=sorted((luminance(WARNING_PREVIEW[name]),luminance(t['color']['panel'])))
        contrast=(b+.05)/(a+.05);assert contrast>=3,(name,'warning-review',contrast)
        contrasts.append({'theme':name,'role':'warning-review','on':'panel','contrast':round(contrast,3),'minimum':3})
    for key in ('grid-inner','busy-clock','circle-radius','circle-center'):
        for size in (16,24):check_svg((OUT/'review/feedback-options'/str(size)/(key+'.svg')).read_text(encoding='utf-8'),size)
    with zipfile.ZipFile(OUT/'openaec-b2-first-family.zip') as z:
        assert len(z.namelist())==count+2+len(manifest['license_files']) and z.testzip() is None
        for path in manifest['license_files']:assert z.read(path)==(OUT/path).read_bytes()
        for i in manifest['icons']:
            for a in i['assets'].values():assert z.read(a['path'])==(OUT/a['path']).read_bytes()
    comparisons=json.loads((OUT/'layer-comparison.json').read_text(encoding='utf-8'))
    comparison_count=0
    assert {c['id'] for c in comparisons}=={i['id'] for i in manifest['icons'] if i['series']==1}
    for record in comparisons:
        for size in (16,24):
            silhouettes=[]
            for front in ('primary','accent'):
                asset=record['variants'][front][str(size)]
                content=(OUT/asset['path']).read_text(encoding='utf-8')
                assert sha(content.encode())==asset['sha256']
                _,layers=check_svg(content,size,front);comparison_count+=1
                silhouettes.append(unary_union(list(layers.values())))
            assert silhouettes[0].symmetric_difference(silhouettes[1]).area<.0001,'changed silhouette'
            current=(OUT/'svg'/str(size)/(record['id']+'.svg')).read_bytes()
            selected=record['variants'][record['foreground']][str(size)]
            assert current==(OUT/selected['path']).read_bytes(),'review/export mismatch'
            before=OUT/'review/stem-before'/str(size)/(record['id']+'.svg')
            # Revision 107 fitted 16 px to the pixel grid; compare the reviewed revision 106 master.
            reviewed=(OUT/'review/raster-before/16'/(record['id']+'.svg')).read_bytes() if size==16 else current
            if record['id'] not in CURRENT_CHANGES:
                assert before.read_bytes()==reviewed,'unrequested change'
            elif record['id'] in ROUNDED_JOINTS:
                old=ET.fromstring(before.read_text(encoding='utf-8'))
                old_shape=unary_union([parse_layer(n.attrib['d']) for n in old if n.tag.endswith('}path')])
                shown=unary_union([parse_layer(n.attrib['d']) for n in ET.fromstring(reviewed.decode('utf-8')) if n.tag.endswith('}path')]) if size==16 else silhouettes[0]
                assert old_shape.symmetric_difference(shown).area<.0001,'approved arrow shape changed'
    result={'status':'geslaagd','functions':len(manifest['icons']),'exported_masters':count,
            'max_exported_overlap_area':maximum,'rejected_failure_controls':controls,
            'source_clusters':len(audit['clusters']),'source_records':len(audit['record_assessments']),
            'theme_contrasts':contrasts,'zip_entries':count+2+len(manifest['license_files']),'layer_comparison_masters':comparison_count,
            'accent_foreground_icons':sum(i['foreground']=='accent' for i in manifest['icons'])}
    assert {i['id'] for i in manifest['icons'] if i['series']==2}==SECOND_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==3}==WINDOW_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==4}==TEXT_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==5}==DATA_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==6}==REPORT_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==7}==IFC_KEYS
    assert {i['id'] for i in manifest['icons'] if i['series']==14}==PAGE_KEYS
    nav_review=(OUT/'bulk-review-3.html').read_text(encoding='utf-8')
    assert '<option value="29,30">' in nav_review,'missing combined review filter'
    assert '.value="29,30";render();' in nav_review,'wrong default review filter'
    fourth_review=(OUT/'bulk-review-5.html').read_text(encoding='utf-8')
    combined=','.join(map(str,FOURTH_AVAILABLE))
    assert f'<option value="{combined}">' in fourth_review,'missing next review filter'
    assert f'.value="{combined}";render();' in fourth_review,'wrong next review default'
    assert len(FOURTH_SERIES)==40
    for batch in FOURTH_AVAILABLE:
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in FOURTH_SERIES.items() if v==batch}
    third_review=(OUT/'bulk-review-4.html').read_text(encoding='utf-8')
    combined=','.join(map(str,THIRD_AVAILABLE))
    assert f'<option value="{combined}">' in third_review,'missing large review filter'
    for batch in THIRD_AVAILABLE:
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in THIRD_SERIES.items() if v==batch}
    for batch in NAV_AVAILABLE:
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in NAV_SERIES.items() if v==batch}
    for batch in SESSION_AVAILABLE:
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in SESSION_SERIES.items() if v==batch}
    for batch in AVAILABLE_SERIES:
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in BULK_SERIES.items() if v==batch}
    for batch in (11,12,13):
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in LATER_SERIES.items() if v==batch}
    for batch in (8,9,10):
        assert {i['id'] for i in manifest['icons'] if i['series']==batch}=={k for k,v in NEXT_SERIES.items() if v==batch}
    assert {f['id'] for f in audit['new_contracts']}=={i['id'] for i in manifest['icons'] if SOURCE_FUNCTIONS.get(i['id'],i['id']) not in {f['id'] for f in catalog['functions']}}
    for record,(target,_) in REUSED.items():
        a=next(r for r in audit['record_assessments'] if r['record_id']==record)
        assert a['canonical_function']==target and a['assessment']=='bestaand B2-ontwerp hergebruiken'
    (OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='theme_contrasts'}))


if __name__=='__main__':main()
