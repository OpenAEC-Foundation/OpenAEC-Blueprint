#!/usr/bin/env python3
"""Expose unreviewed literal JSX SVG sites without calling them UI icons."""
import json
import re
import subprocess
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repo = Path('/tmp/openaec-inventory/open-pdf-studio')
commit = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
prefix = 'open-pdf-studio/js/solid/'
fully_audited = {
    'components/TitleBar.jsx', 'components/StatusBar.jsx',
    'components/DocumentTabs.jsx', 'components/ribbon/Ribbon.jsx',
    'components/app-menu/AppMenu.jsx', 'components/app-menu/OpenPanel.jsx',
    'components/ribbon/DrawingTab.jsx', 'components/ContextMenu.jsx',
}

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True)

assert git('rev-parse', 'HEAD').strip() == commit
paths = [p for p in git('ls-tree', '-r', '--name-only', commit, prefix).splitlines()
         if p.endswith(('.jsx', '.tsx'))]
rows = []
for path in paths:
    code = git('show', f'{commit}:{path}')
    matches = list(re.finditer(r'<svg\b', code))
    if not matches:
        continue
    relative = path.removeprefix(prefix)
    if relative in fully_audited:
        state = 'fully-reviewed-literal-sites'
    elif relative in ('components/ribbon/ArrangeTab.jsx', 'components/ribbon/FormatTab.jsx'):
        state = 'partial-command-review'
    else:
        state = 'requires-ui-role-review'
    group = ('mobile' if relative == 'MobileApp.jsx' else
             'ribbon' if '/ribbon/' in relative else
             'app-menu' if '/app-menu/' in relative else
             'left-panel' if '/left-panel/' in relative else
             'preferences' if '/preferences/' in relative else
             'dialogs' if '/dialogs/' in relative else 'other')
    rows.append({'file': path, 'group': group, 'literal_svg_sites': len(matches),
                 'lines': [code.count('\n', 0, m.start()) + 1 for m in matches],
                 'review_state': state})

assert len(paths) == 172 and len(rows) == 68
assert sum(row['literal_svg_sites'] for row in rows) == 317
audited_sites = sum(row['literal_svg_sites'] for row in rows if row['review_state'] == 'fully-reviewed-literal-sites')
assert audited_sites == 112
manifest = {
    'repository': 'open-pdf-studio', 'commit': commit,
    'scope': 'Literal <svg> openings in pinned open-pdf-studio/js/solid JSX/TSX; counts are source sites, not UI icon counts. Component reachability and graphic role remain to be checked for non-audited rows.',
    'jsx_tsx_files': len(paths), 'svg_bearing_files': len(rows),
    'literal_svg_sites': 317, 'fully_reviewed_literal_sites': audited_sites,
    'sites_requiring_role_review_or_partial_followup': 317 - audited_sites,
    'files': sorted(rows, key=lambda row: (-row['literal_svg_sites'], row['file'])),
}
(root / 'harmonization/pdf-jsx-svg-coverage.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

trs = []
for row in manifest['files']:
    url = f'https://github.com/OpenAEC-Foundation/open-pdf-studio/blob/{commit}/{row["file"]}#L{row["lines"][0]}'
    trs.append(f'<tr data-search="{escape((row["file"]+" "+row["group"]+" "+row["review_state"]).lower())}" data-state="{escape(row["review_state"])}"><td><a href="{escape(url)}">{escape(row["file"].removeprefix(prefix))}</a></td><td>{escape(row["group"])}</td><td>{row["literal_svg_sites"]}</td><td>{escape(row["review_state"])}</td></tr>')
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open PDF Studio · JSX-SVG-dekking</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:13px/1.5 system-ui,sans-serif}header{background:#303039;color:#fff;border-bottom:3px solid #d97706;padding:24px max(20px,calc((100vw - 1150px)/2))}header a{color:#ffc47e}header h1{font-size:27px;margin:8px 0 4px}header p{max-width:1050px;color:#d6d6dd;margin:0}main{max-width:1190px;margin:auto;padding:20px}.note{background:#fff7eb;border-left:3px solid #d97706;padding:12px 16px;margin-bottom:16px}.stats{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.stats span{background:#fff;padding:8px 12px;border:1px solid #d8d8dc}.stats b{color:#ad5b00}input{font:inherit;border:1px solid #c7c7cd;padding:9px 12px;width:min(420px,100%);margin-bottom:16px}table{border-collapse:collapse;background:#fff;width:100%}th,td{border-bottom:1px solid #e1e1e5;text-align:left;padding:8px 10px}th{background:#e9e9ec;position:sticky;top:0}tr[hidden]{display:none}a{color:#9f5200}@media(max-width:700px){main{padding:10px}table{display:block;overflow-x:auto}td{min-width:100px}}
 </style><header><a href="review.html">← Ontwerpreview</a><h1>PDF · JSX-SVG-dekking</h1><p>Gepinde codekaart voor alle 172 Solid JSX/TSX-bestanden. Een letterlijke SVG is pas een UI-icoon na controle van de aanroep en visuele rol.</p></header><main><div class="note"><strong>Huidige grens.</strong> Titelbalk, status, Bestand inclusief Openen, contextmenu’s, documenttabs, ribbonchevron en Tekenen zijn per bronplaats beoordeeld. Arrangement en Opmaak hebben gerichte commandoreviews, maar geen volledige bestandsaudit in deze kaart. Alle andere rijen blijven zonder icoonclaim totdat hun bereikbaarheid en grafische rol zijn vastgesteld. Mobiele UI is een aparte route.</div><div class="stats"><span><b>172</b> JSX/TSX-bestanden</span><span><b>68</b> met letterlijke SVG</span><span><b>317</b> SVG-bronplaatsen</span><span><b>112</b> volledig bronplaats-beoordeeld</span><span><b>205</b> nog te classificeren of aanvullen</span></div><input id="q" type="search" placeholder="Zoek bestand of status" aria-label="Zoek bestand of status"><table><thead><tr><th>Bronbestand</th><th>Gebied</th><th>SVG-plaatsen</th><th>Reviewstatus</th></tr></thead><tbody>''' + ''.join(trs) + '''</tbody></table></main><script>const q=document.querySelector('#q');q.oninput=()=>{for(const row of document.querySelectorAll('tbody tr'))row.hidden=!row.dataset.search.includes(q.value.toLowerCase().trim())};</script></html>'''
(root / 'design/pdf-jsx-svg-coverage.html').write_text(page)
print('PDF JSX: 317 literal SVG sites in 68 files; 112 fully audited, 205 remaining/partial')
