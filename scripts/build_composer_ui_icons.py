#!/usr/bin/env python3
"""Inventory source-reachable Solid icon components, not arbitrary SVG assets."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/OpenAEC-Workspace-Composer')
COMMIT = '33327e001d6ad917356920060b8c7016fcbd6de5'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT


def show(path: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'], text=True)


def evidence(path: str, line: int) -> dict:
    return {'file': path, 'line': line,
            'url': f'https://github.com/OpenAEC-Foundation/OpenAEC-Workspace-Composer/blob/{COMMIT}/{path}#L{line}'}


paths = subprocess.check_output(
    ['git', '-C', str(REPO), 'ls-tree', '-r', '--name-only', 'HEAD', 'src'], text=True
).splitlines()
files = {path: show(path) for path in paths if path.endswith(('.tsx', '.jsx'))}
imports = []
usages = []
for path, source in files.items():
    for match in re.finditer(r'import\s*\{([^}]*)\}\s*from\s*["\'](solid-icons/[^"\']+)["\']', source, re.S):
        package = match.group(2)
        import_line = source.count('\n', 0, match.start()) + 1
        for item in match.group(1).split(','):
            item = item.strip()
            if not item:
                continue
            parts = re.split(r'\s+as\s+', item)
            symbol, local = parts[0], parts[-1]
            imports.append({'package': package, 'symbol': symbol, 'local': local,
                            'evidence': evidence(path, import_line)})
            for use in re.finditer(r'<\s*' + re.escape(local) + r'(?=[\s/>])', source):
                usages.append({'package': package, 'symbol': symbol, 'local': local,
                               'kind': 'direct_jsx',
                               'evidence': evidence(path, source.count('\n', 0, use.start()) + 1)})

layout = files['src/layouts/AppLayout.tsx']
nav_block = re.search(r'const iconMap:.*?=\s*\{(.*?)\};', layout, re.S)
assert nav_block
nav_map = dict(re.findall(r'["\']?([\w-]+)["\']?:\s*(TbOutline\w+)', nav_block.group(1)))
assert len(nav_map) == 13
for match in re.finditer(r'<NavIcon icon="([^"]+)"', layout):
    icon = match.group(1)
    assert icon in nav_map
    usages.append({'package': 'solid-icons/tb', 'symbol': nav_map[icon], 'local': 'NavIcon',
                   'kind': 'dynamic_nav', 'nav_key': icon,
                   'evidence': evidence('src/layouts/AppLayout.tsx', layout.count('\n', 0, match.start()) + 1)})

used = {(u['evidence']['file'], u['symbol']) for u in usages}
unused = [item for item in imports if (item['evidence']['file'], item['symbol']) not in used]
manifest = {
    'repository': 'OpenAEC-Workspace-Composer', 'commit': COMMIT,
    'scope': 'Solid icon components actually instantiated in JSX, including NavIcon factory calls; brand and package logos excluded.',
    'source_files_scanned': len(files), 'imports': imports, 'usages': usages,
    'unused_imports': unused,
    'unique_used_symbols': sorted({u['symbol'] for u in usages}),
    'nav_map': nav_map,
    'excluded_asset_roles': ['OpenAEC sidebar symbol is branding.', 'Package logos represent product identity.'],
}
target = ROOT / 'harmonization/composer-ui-icons.json'
target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(f'{len(files)} TSX/JSX files; {len(usages)} icon placements; '
      f'{len(manifest["unique_used_symbols"])} used component symbols; {len(unused)} unused imports → {target}')
