#!/usr/bin/env python3
"""Pin reachable Workspace Composer pages, shell modes and source captures."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/OpenAEC-Workspace-Composer')
COMMIT = '33327e001d6ad917356920060b8c7016fcbd6de5'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT


def show(path: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'])


def evidence(path: str, marker: str) -> dict:
    lines = show(path).decode().splitlines()
    matches = [i for i, line in enumerate(lines, 1) if marker in line]
    assert matches, (path, marker)
    line = matches[0]
    return {'file': path, 'line': line, 'marker': marker,
            'url': f'https://github.com/OpenAEC-Foundation/OpenAEC-Workspace-Composer/blob/{COMMIT}/{path}#L{line}'}


index = show('src/index.tsx').decode()
route_matches = re.findall(r'<Route path="([^"]+)" component=\{([A-Za-z]+)', index)
assert len(route_matches) == 18 and len({path for path, _ in route_matches}) == 18
simple = {'/workspace', '/presets', '/install', '/about'}
all_pages = {name for name in subprocess.check_output(
    ['git', '-C', str(REPO), 'ls-tree', '-r', '--name-only', 'HEAD', 'src/pages'], text=True
).splitlines() if name.endswith('.tsx')}
routes = []
for path, component in route_matches:
    page = f'src/pages/{component}.tsx'
    assert page in all_pages, page
    assert f'export function {component}(' in show(page).decode(), page
    nav_marker = f'href="{path}"'
    route = {
        'path': path, 'component': component,
        'mode': 'both' if path in simple else 'advanced',
        'route_evidence': evidence('src/index.tsx', f'<Route path="{path}"'),
        'page_evidence': evidence(page, f'export function {component}('),
        'nav_evidence': evidence('src/layouts/AppLayout.tsx', nav_marker),
    }
    routes.append(route)
assert {r['path'] for r in routes if r['mode'] == 'both'} == simple
assert len(routes) == 18

redirects = [
    {'path': path, 'target': '/workspace', 'evidence': evidence('src/index.tsx', f'<Route path="{path}"')}
    for path in ('/', '/packages')
]
orphan_pages = sorted(all_pages - {f'src/pages/{name}.tsx' for _, name in route_matches})
assert orphan_pages == ['src/pages/PackagesPage.tsx', 'src/pages/SyncPage.tsx'], orphan_pages
unmatched_link = {
    'path': '/sync', 'evidence': evidence('src/pages/DashboardPage.tsx', '<A href="/sync"'),
    'component': 'src/pages/SyncPage.tsx',
    'component_evidence': evidence('src/pages/SyncPage.tsx', 'export function SyncPage('),
    'reason': 'Dashboard tile points to /sync, but src/index.tsx registers no /sync route.',
}
assert '<Route path="/sync"' not in index

screenshots = []
for path, route, state in [
    ('workspace-packages.png', '/workspace', 'Simple mode; selected package grid'),
    ('workspace-presets.png', '/presets', 'Simple mode; preset grid'),
    ('install-complete.png', '/install', 'Simple mode; completed installation and prerequisites'),
]:
    source = f'docs/screenshots/{path}'
    local = ROOT / 'harmonization/references/OpenAEC-Workspace-Composer' / source
    raw = show(source)
    assert local.read_bytes() == raw, f'local capture differs: {source}'
    screenshots.append({'source': source, 'local': str(local.relative_to(ROOT)),
                        'route': route, 'state': state, 'sha256': hashlib.sha256(raw).hexdigest(),
                        'url': f'https://github.com/OpenAEC-Foundation/OpenAEC-Workspace-Composer/blob/{COMMIT}/{source}'})

manifest = {
    'repository': 'OpenAEC-Workspace-Composer', 'commit': COMMIT,
    'routes': routes, 'redirects': redirects, 'orphan_pages': orphan_pages,
    'unmatched_link': unmatched_link, 'screenshots': screenshots,
    'modes': {
        'default': 'simple', 'default_evidence': evidence('src/stores/app.store.ts', 'createSignal<AppMode>("simple")'),
        'simple_evidence': evidence('src/layouts/AppLayout.tsx', '<Show when={!advanced()}>'),
        'advanced_evidence': evidence('src/layouts/AppLayout.tsx', '<Show when={advanced()}>'),
        'toggle_evidence': evidence('src/layouts/AppLayout.tsx', 'onClick={() => appStore.toggleMode()}'),
    },
    'layout': {
        'sidebar_width_px': 220, 'titlebar_height_px': 32, 'statusbar_height_px': 22,
        'sidebar_evidence': evidence('src/styles/tokens.css', '--sidebar-w:   220px;'),
        'title_evidence': evidence('src/styles/tokens.css', '--titlebar-h:  32px;'),
        'status_evidence': evidence('src/styles/tokens.css', '--statusbar-h: 22px;'),
        'shell_evidence': evidence('src/layouts/AppLayout.tsx', '<div class="app-main">'),
    },
    'asset_roles': {
        'brand_symbol': evidence('src/layouts/AppLayout.tsx', '<img src={openaecSymbol} alt="OpenAEC"'),
        'package_logos': evidence('src/lib/package-logos.ts', 'import '),
        'nav_icon_factory': evidence('src/layouts/AppLayout.tsx', 'function NavIcon('),
        'classification': 'OpenAEC symbol and package logos are branding; Tabler components in NavIcon are UI icons.',
    },
    'limits': ['Three captured screens cover two simple-mode pages and the completed install state, not all 18 routes.',
               'The captured UI is dark and may predate current source; layout evidence is pinned to the source commit.',
               'Package and skill data are not reproduced by the review mock.'],
}
(ROOT / 'harmonization/composer-screen-routes.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
template = (ROOT / 'design/composer-screen-route-template.html').read_text()
(ROOT / 'design/composer-screen-route-review.html').write_text(
    template.replace('/*COMPOSER_DATA*/', json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')))
print(f'Composer: {len(routes)} reachable routes, {len(redirects)} redirects, {len(orphan_pages)} orphan page modules, {len(screenshots)} captures')
