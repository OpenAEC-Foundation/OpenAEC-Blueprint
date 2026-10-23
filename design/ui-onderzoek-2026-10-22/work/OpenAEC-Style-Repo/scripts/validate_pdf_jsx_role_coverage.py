#!/usr/bin/env python3
"""Require one source-role decision for each pinned PDF JSX <svg> opening."""
import json
from collections import Counter, defaultdict
from pathlib import Path

root=Path(__file__).resolve().parents[1]
coverage=json.loads((root/'harmonization/pdf-jsx-svg-coverage.json').read_text())
commit=coverage['commit']
expected={(row['file'],line) for row in coverage['files'] for line in row['lines']}
assert len(expected)==coverage['literal_svg_sites']==317
assert coverage['fully_reviewed_literal_sites']==317
assert coverage['sites_requiring_role_review_or_partial_followup']==0

# Catalog definitions from ribbonIcons.js, contextMenuIcons.js and symbol
# category sources are separate from this JSX source-site proof.
manifests=[
 'pdf-chrome-ui-icons.json',
 'pdf-open-panel-ui-icons.json',
 'pdf-transfer-panel-ui-icons.json',
 'pdf-context-literal-ui-icons.json',
 'pdf-drawing-ui-icons.json',
 'pdf-home-tab-ui-icons.json',
 'pdf-annotations-panel-ui-icons.json',
 'pdf-mobile-ui-icons.json',
 'pdf-symbol-palette-ui-icons.json',
 'pdf-tool-palette-ui-icons.json',
 'pdf-find-bar-ui-icons.json',
 'pdf-left-panel-content-ui-icons.json',
 'pdf-dialog-ui-visuals.json',
 'pdf-preferences-ui-icons.json',
 'pdf-ribbon-remaining-ui-icons.json',
 'pdf-last-jsx-svg-roles.json',
]
found=defaultdict(list)
counts=Counter()
for filename in manifests:
    data=json.loads((root/'harmonization'/filename).read_text())
    assert data['repository']=='open-pdf-studio' and data['commit']==commit,filename
    for kind in ('records','excluded'):
        for record in data.get(kind,[]):
            path=record.get('source_file') or record.get('file')
            line=record.get('source_line') or record.get('line')
            assert path and isinstance(line,int),(filename,record)
            key=(path,line)
            found[key].append({'manifest':filename,'kind':kind,
                               'role':record.get('role') or record.get('kind') or record.get('review')})
            counts[(filename,kind)]+=1
            svg=record.get('svg')
            if svg:
                assert (root/'harmonization'/svg).is_file(),(filename,svg)
            if kind=='excluded':
                assert record.get('reason'),(filename,record)

assert set(found)==expected,{
    'missing':sorted(expected-set(found)),
    'unexpected':sorted(set(found)-expected),
}
duplicates={key:entries for key,entries in found.items() if len(entries)!=1}
assert not duplicates,duplicates
assert counts[('pdf-symbol-palette-ui-icons.json','excluded')]==1
assert sum(counts.values())==317
print(f'PDF JSX source-role coverage: {len(expected)} of {len(expected)} sites; '
      f'{sum(n for (f,k),n in counts.items() if k=="excluded")} explicit non-icon exclusion; '
      f'{len(manifests)} pinned review manifests')
