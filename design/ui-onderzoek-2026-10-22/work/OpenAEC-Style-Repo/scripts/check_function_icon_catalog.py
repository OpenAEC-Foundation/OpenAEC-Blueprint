"""Validate the deliverable against its independent source and asset evidence."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / 'harmonization'


def main():
    manifest = json.loads((H / 'function-icon-sources.json').read_text(encoding='utf-8'))
    catalog = json.loads((H / 'function-icon-catalog.json').read_text(encoding='utf-8'))
    errors = []
    def check(condition, message):
        if not condition: errors.append(message)
    app_scope = {'Calc','Calculations','Planner','Geotechniek','Heatloss','Pile Plan','Reports',
                 'Energy','Field','PDF','Speech','Workspace Composer','Frame','Pointcloud','BIM Validator','FEM'}
    check({r['app'] for r in catalog['coverage']} == app_scope, 'App scope differs from the 16 agreed apps')
    snapshots = {}
    files_checked = 0
    for repo in manifest['repositories']:
        key = (repo['repository'],repo['commit'])
        snapshots[key] = {f['path']:f for f in repo['files']}
        if repo['app'] == 'FEM':
            check(repo['status']=='bron ontbreekt' and not repo['files'], 'FEM must remain an explicit source gap')
            continue
        check(not repo['errors'], f"Source download errors: {repo['repository']}")
        check(len(repo['files'])==repo['selected_files'],f"Incomplete source selection: {repo['repository']}")
        for file in repo['files']:
            path = H/'sources/function-icon-audit'/repo['repository']/repo['commit']/file['path']
            check(path.is_file(),f'Missing source cache: {path}')
            if path.is_file():
                check(hashlib.sha256(path.read_bytes()).hexdigest()==file['sha256'],f'Source digest mismatch: {path}')
            files_checked += 1
    rows = catalog['records']
    ids = [r['id'] for r in rows]
    check(len(ids)==len(set(ids)), 'Duplicate record IDs')
    references = [rid for f in catalog['functions'] for rid in f['record_ids']]
    check(Counter(ids)==Counter(references), 'Function groups lose or duplicate records')
    check(catalog['summary']['occurrences']==len(rows), 'Summary count differs from records')
    with (H/'function-icon-catalog.csv').open(encoding='utf-8-sig',newline='') as file:
        check(sum(1 for _ in csv.DictReader(file))==len(rows),'CSV count differs from JSON')
    assets = set()
    for row in rows:
        check(row['app'] in app_scope, f"Out-of-scope app: {row['app']}")
        paths = snapshots.get((row['repository'],row['commit']),{})
        check(row['path'] in paths,f"Unresolved source path: {row['repository']}:{row['path']}")
        check(row['line']>0,f"Missing source line: {row['id']}")
        check(bool(row['context'].strip()),f"Empty source context: {row['id']}")
        check(row['commit'] in row['source_url'],f"Source link is not immutable: {row['id']}")
        if row['asset']:
            path = ROOT/row['asset']; assets.add(path)
            check(path.is_file(),f'Missing preview: {path}')
            if path.is_file():
                check(hashlib.sha256(path.read_bytes()).hexdigest()==row['exact_hash'],f'Preview digest mismatch: {path}')
    page = (ROOT/'design/function-icon-catalog.html').read_text(encoding='utf-8')
    payload = re.search(r'<script type="application/json" id="data">([\s\S]*?)</script>',page)
    check(bool(payload),'HTML lacks embedded catalog')
    if payload:
        embedded = json.loads(payload[1])
        check(embedded['catalog']==catalog,'Standalone HTML is stale')
        for row in rows:
            if row['asset']:
                check(row['exact_hash'] in embedded['images'],f"HTML image missing: {row['id']}")
    check(not catalog['warnings'],'Generator reported missing preview files')
    result = {'status':'geslaagd' if not errors else 'mislukt','source_files_checked':files_checked,
              'records_checked':len(rows),'preview_files_checked':len(assets),
              'function_groups_checked':len(catalog['functions']),'errors':errors}
    (H/'function-icon-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
