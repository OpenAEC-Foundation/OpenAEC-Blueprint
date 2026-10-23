"""Check exported B geometry, plus failure controls for the original bug class."""
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import hashlib
import json
import re

from icon_geometry import Model, build_b_model, intersection_area, signed_area

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'design/icon-style-proposals'


def exported_polygons(path):
    svg=ET.parse(path).getroot()
    assert svg.attrib['stroke']=='none','B must export filled contours, not renderer-dependent strokes'
    polygons={'primary':[],'accent':[]}
    for node in svg:
        tone=node.attrib['data-part']
        assert tone in polygons and node.attrib['stroke']=='none'
        assert node.attrib['fill']==('currentColor' if tone=='primary' else 'var(--icon-accent,currentColor)')
        for match in re.finditer(r'M([^M]+?)Z',node.attrib['d']):
            coords=[tuple(map(float,p)) for p in re.findall(r'([\d.-]+) ([\d.-]+)',match[1])]
            assert len(coords)>=3 and signed_area(coords)>0
            polygons[tone].append(coords)
    assert len(svg)==2 and all(polygons.values())
    return polygons


def main():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['selected_style']=='b' and manifest['geometry_revision']==2
    records=manifest['records']
    assert len(records)==84
    checked=0;maximum=0
    for record in records:
        path=OUT/record['path']
        ET.parse(path)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],record['path']
        if record['style']!='b':continue
        size=record['master_px'];key=path.stem
        assert size in (16,24)
        build_b_model(key,size).validate()
        colours=exported_polygons(path)
        for polys in colours.values():
            for poly in polys:
                assert all(0<=x<=size and 0<=y<=size for x,y in poly),(key,size,'export clipping')
        for a in colours['primary']:
            for b in colours['accent']:
                area=intersection_area(a,b);maximum=max(maximum,area)
                assert area<1e-6,(key,size,'exported colours overlap',area)
        ET.parse(OUT/'review/before'/str(size)/(key+'.svg'))
        checked+=1
    assert checked==28
    # Positive failure controls: detect a duplicate accent and an off-canvas end.
    broken=Model('old-overlay-pattern',24,1.75)
    broken.line('base',[(3,7),(12,11),(21,7)])
    broken.line('painted-again',[(3,7),(12,11),(17,8.8)],True)
    clipped=Model('out-of-frame',16,1.25)
    clipped.line('base',[(2,2),(12,2)])
    clipped.line('accent',[(15,8),(17,8)],True)
    for fixture,reason in ((broken,'overlapping colours'),(clipped,'clipped')):
        try:fixture.validate()
        except AssertionError as error:assert reason in str(error),(fixture.key,'unexpected rejection',str(error))
        else:raise AssertionError('Invalid fixture was accepted: '+fixture.key)
    with ZipFile(OUT/'openaec-icon-style-samples.zip') as archive:
        assert len(archive.namelist())==len(records)+3 and archive.testzip() is None
        for record in records:
            assert archive.read(record['path'])==(OUT/record['path']).read_bytes()
    print(json.dumps({'status':'geslaagd','svg_hashes':84,'exported_B_masters':checked,
                      'max_exported_colour_overlap_area':round(maximum,10),'rejected_failure_controls':2,
                      'zip_entries':len(records)+3},ensure_ascii=False))


if __name__=='__main__':main()
