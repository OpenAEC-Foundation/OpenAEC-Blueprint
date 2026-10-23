#!/usr/bin/env python3
"""Source-pinned BCF Platform route, ribbon, and actually referenced icon review."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/openaec-bcf-platform')
COMMIT = 'e98fb97f5f23bc9c9f3b80de18acd721440f7597'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT


def show(path: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}']).decode()


def evidence(path: str, marker: str) -> dict:
    lines = show(path).splitlines()
    matches = [i for i, line in enumerate(lines, 1) if marker in line]
    assert matches, (path, marker)
    line = matches[0]
    return {'file': path, 'line': line,
            'url': f'https://github.com/OpenAEC-Foundation/openaec-bcf-platform/blob/{COMMIT}/{path}#L{line}'}


app_path = 'frontend/src/App.tsx'
app = show(app_path)
routes = []
for path, component in re.findall(r'<Route path="([^"]+)" element=\{<AppShellWrapper><(\w+)\s*/>', app):
    file = f'frontend/src/pages/{component}.tsx'
    assert f'export default function {component}(' in show(file)
    routes.append({'path': path, 'component': component,
                   'route_evidence': evidence(app_path, f'<Route path="{path}"'),
                   'page_evidence': evidence(file, f'export default function {component}(')})
assert len(routes) == 3 and {r['path'] for r in routes} == {'/', '/projects/:projectId', '/projects/:projectId/topics/:topicId'}

ribbon_path = 'frontend/src/components/shell/Ribbon.tsx'
ribbon = show(ribbon_path)
css_path = 'frontend/src/components/shell/Ribbon.css'
css = show(css_path)
assert 'height: 28px;' in css and 'height: 94px;' in css
assert "type TabId = 'home' | 'view'" in ribbon
tabs = [{'id': 'file', 'label': 'Bestand', 'role': 'backstage', 'evidence': evidence(ribbon_path, '>\n          Bestand') if False else evidence(ribbon_path, '          Bestand')},
        {'id': 'home', 'label': 'Start', 'role': 'ribbon', 'evidence': evidence(ribbon_path, '          Start')},
        {'id': 'view', 'label': 'Beeld', 'role': 'ribbon', 'evidence': evidence(ribbon_path, '          Beeld')}]

sprite_path = 'frontend/src/components/shell/icons.ts'
sprite_source = show(sprite_path)
sprites = re.findall(r'export const (\w+) = `(<svg[^`]+</svg>)`;', sprite_source)
assert len(sprites) == 10
sprite_uses = {
    'iconNewProject': [(ribbon_path, 'icon={iconNewProject}')],
    'iconImportBcf': [(ribbon_path, 'icon={iconImportBcf}')],
    'iconExportBcf': [(ribbon_path, 'icon={iconExportBcf}')],
    'iconNewIssue': [(ribbon_path, 'icon={iconNewIssue}')],
    'iconCloudUpload': [('frontend/src/components/shell/CloudPanel.tsx', '__html: iconCloudUpload')],
    'iconCloudDownload': [('frontend/src/components/shell/CloudPanel.tsx', '__html: iconCloudDownload')],
}
assert len(sprite_uses) == 6
icons = []
for name, svg in sprites:
    uses = [evidence(p, marker) for p, marker in sprite_uses.get(name, [])]
    icons.append({'id': name, 'source': 'shared-svg-string', 'svg': svg, 'sha256': hashlib.sha256(svg.encode()).hexdigest(),
                  'definition': evidence(sprite_path, f'export const {name} ='), 'uses': uses,
                  'active_ui': bool(uses)})

backstage_path = 'frontend/src/components/shell/Backstage.tsx'
backstage = show(backstage_path)
backstage_icons = re.findall(r"^  (\w+): '(<svg[^']+</svg>)',?$", backstage, re.M)
assert len(backstage_icons) == 10
for name, svg in backstage_icons:
    marker = f'icon={{ICONS.{name}}}'
    assert marker in backstage, name
    icons.append({'id': f'backstage.{name}', 'source': 'backstage-svg-string', 'svg': svg,
                  'sha256': hashlib.sha256(svg.encode()).hexdigest(),
                  'definition': evidence(backstage_path, f'  {name}: '),
                  'uses': [evidence(backstage_path, marker)], 'active_ui': True})

appbar_path = 'frontend/src/components/shell/AppBar.tsx'
appbar = show(appbar_path)
appbar_icons = re.findall(r'const (icon\w+) = `(<svg[^`]+</svg>)`;', appbar)
assert len(appbar_icons) == 2
for name, svg in appbar_icons:
    icons.append({'id': f'appbar.{name}', 'source': 'appbar-svg-string', 'svg': svg,
                  'sha256': hashlib.sha256(svg.encode()).hexdigest(),
                  'definition': evidence(appbar_path, f'const {name} ='),
                  'uses': [evidence(appbar_path, f'__html: {name}')], 'active_ui': True})

# Four JSX SVGs are present in Backstage: three controls/links and one brand illustration.
inline = list(re.finditer(r'(?m)^[ \t]*<svg\b[^>]*>.*?</svg>', backstage, re.S))
assert len(inline) == 4
inline_roles = [('backstage.back', 'ui-icon', 'className="backstage-back"'),
                ('backstage.brand', 'brand-illustration', 'className="bs-about-logo"'),
                ('backstage.website', 'ui-icon', 'href="https://open-aec.com"'),
                ('backstage.github', 'ui-icon', 'href="https://github.com/OpenAEC-Foundation"')]
brand_illustration = None
for match, (name, role, preceding) in zip(inline, inline_roles):
    before = backstage[:match.start()].splitlines()[-12:]
    assert any(preceding in line for line in before), name
    svg = match.group().replace('strokeWidth=', 'stroke-width=').replace('strokeLinecap=', 'stroke-linecap=').replace('strokeLinejoin=', 'stroke-linejoin=')
    line = backstage[:match.start()].count('\n') + 1
    record = {'id': name, 'role': role, 'source': 'inline-jsx-svg', 'svg': svg,
              'sha256': hashlib.sha256(svg.encode()).hexdigest(),
              'definition': {'file': backstage_path, 'line': line,
                             'url': f'https://github.com/OpenAEC-Foundation/openaec-bcf-platform/blob/{COMMIT}/{backstage_path}#L{line}'},
              'uses': [], 'active_ui': role == 'ui-icon'}
    if role == 'ui-icon':
        record['uses'] = [record['definition']]
        icons.append(record)
    else:
        brand_illustration = record
assert brand_illustration is not None

lucide = []
paths = subprocess.check_output(['git', '-C', str(REPO), 'ls-tree', '-r', '--name-only', 'HEAD', 'frontend/src'], text=True).splitlines()
for path in paths:
    if not path.endswith('.tsx'):
        continue
    source = show(path)
    for names in re.findall(r'import\s*\{([^}]+)\}\s*from\s*[\'\"]lucide-react[\'\"]', source, re.S):
        for imported in [s.strip() for s in names.split(',') if s.strip()]:
            name = imported.split(' as ')[-1]
            assert re.search(rf'<{name}(?:\s|/|>)', source), (path, name)
            lucide.append({'name': name, 'file': path, 'import_evidence': evidence(path, 'lucide-react'),
                           'use_evidence': evidence(path, f'<{name}')})
assert len(lucide) == 38 and len({x['name'] for x in lucide}) == 30

findings = [
    {'id': 'new-project-route', 'summary': 'Backstage Nieuw navigeert naar /projects; deze route is niet geregistreerd.',
     'evidence': evidence(backstage_path, 'onNavigate?.("/projects")')},
    {'id': 'topics-route', 'summary': 'Backstage Open navigeert naar /topics; deze route is niet geregistreerd.',
     'evidence': evidence(backstage_path, 'onNavigate?.("/topics")')},
    {'id': 'new-issue-handler', 'summary': 'De lintknop Nieuw issue krijgt vanuit AppShell geen onNewIssue-handler.',
     'evidence': evidence(ribbon_path, 'onClick={onNewIssue}'),
     'shell_evidence': evidence('frontend/src/components/shell/AppShell.tsx', '<Ribbon')},
    {'id': 'view-placeholder', 'summary': 'De tab Beeld bevat een placeholder in plaats van opdrachten.',
     'evidence': evidence(ribbon_path, 'Weergave-opties komen hier')},
    {'id': 'import-export-arrows', 'summary': 'Import toont een pijl omhoog en Export een pijl omlaag; beoordeel de betekenis vóór canonisering.',
     'evidence': evidence(sprite_path, 'export const iconImportBcf ='),
     'other_evidence': evidence(sprite_path, 'export const iconExportBcf =')},
]
assert '<Route path="/projects"' not in app and '<Route path="/topics"' not in app
assert 'onNewIssue=' not in show('frontend/src/components/shell/AppShell.tsx')

manifest = {'repository': 'openaec-bcf-platform', 'commit': COMMIT,
            'routes': routes, 'tabs': tabs,
            'ribbon': {'tab_strip_height_px': 28, 'content_height_px': 94,
                       'tab_evidence': evidence(css_path, 'height: 28px;'),
                       'content_evidence': evidence(css_path, 'height: 94px;')},
            'appbar': {'height_px': 40, 'evidence': evidence('frontend/src/components/shell/AppBar.css', 'height: 40px;')},
            'statusbar': {'height_px': 22, 'evidence': evidence('frontend/src/components/shell/StatusBar.css', 'height: 22px;')},
            'icons': icons, 'brand_illustration': brand_illustration,
            'lucide_uses': lucide, 'findings': findings,
            'capture_count': 0,
            'limits': ['No source screenshots are present in this pinned repository; the HTML is a code-derived layout review, not a pixel match.',
                       'The 38 Lucide rows are import/use sites for 30 distinct component names, not necessarily 30 unique vector designs.',
                       'Unused exported icon SVGs are retained as source definitions but excluded from the active-UI count.',
                       'The Backstage About illustration is branding and excluded from the icon count.']}
out = ROOT / 'harmonization/bcf-platform-ui-audit.json'
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
template = (ROOT / 'design/bcf-platform-review-template.html').read_text()
(ROOT / 'design/bcf-platform-review.html').write_text(template.replace('/*BCF_DATA*/', json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')))
print(f'BCF Platform: {len(routes)} routes, {len(icons)} UI SVG definitions, {sum(i["active_ui"] for i in icons)} active UI SVGs, {len(lucide)} Lucide use sites')
