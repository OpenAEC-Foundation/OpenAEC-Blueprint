"""Combine preserved baseline evidence with explicit pinned supplemental call sites."""
from pathlib import Path
import json
import hashlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'harmonization/function-icon-catalog.json'
SUPPLEMENT=ROOT/'harmonization/icon-set-b2/supplemental-sources.json'

def supplemental_catalog():
    return json.loads(SUPPLEMENT.read_text(encoding='utf-8'))

def source_hashes():
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE,SUPPLEMENT)}

def load_catalog():
    catalog=json.loads(BASE.read_text(encoding='utf-8'))
    supplement=supplemental_catalog()
    records=supplement['records']
    assert len({r['id'] for r in catalog['records']+records})==len(catalog['records'])+len(records),'duplicate source ID'
    catalog['records']+=records
    for r in records:
        catalog['functions'].append({'id':r['function_id'],'category':r['category'],'label':r['function_label'],
            'apps':[r['app']],'occurrences':1,'shape_count':0,'comparison':'Afzonderlijk gelezen bronplaats; geen bronvorm overgenomen.',
            'requires_review':False,'record_ids':[r['id']]})
    catalog['scope']+=' Aanvulling: Installer en ontbrekende Calc-bronplaats op afzonderlijk vastgelegde commits.'
    catalog['supplemental_source']=SUPPLEMENT.relative_to(ROOT).as_posix()
    catalog['summary'].update({'apps':len({r['app'] for r in catalog['records']}),'occurrences':len(catalog['records']),
                               'functions':len(catalog['functions'])})
    return catalog
