"""Download immutable UI source snapshots for the function icon inventory.

Only source text is downloaded; nothing from upstream repositories is executed.
The cache is ignored by Git. The manifest records every selected file and error.
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / 'harmonization'
CACHE = H / 'sources' / 'function-icon-audit'
APPS = {
    'open-calc-studio': 'Calc', 'Open-Calculations-Studio': 'Calculations',
    'open-planner-studio': 'Planner', 'open-geotechniek-studio': 'Geotechniek',
    'open-heatloss-studio': 'Heatloss', 'pile-plan-studio': 'Pile Plan',
    'openaec-reports': 'Reports', 'open-energy-studio': 'Energy',
    'Open-Field-Studio': 'Field', 'open-pdf-studio': 'PDF',
    'open-pdf-studio-v3': 'PDF', 'open-speech-studio': 'Speech',
    'OpenAEC-Workspace-Composer': 'Workspace Composer', 'open-frame-studio': 'Frame',
    'open-pointcloud-studio': 'Pointcloud', 'OpenAEC-BIM-validator': 'BIM Validator',
    'open-fem-studio': 'FEM',
    'open-calc-studio-extensions': 'Calc',
    'open-planner-studio-extensions': 'Planner',
}
SKIP = {'node_modules', 'target', 'vendor', 'third_party', 'dist', 'build',
        '.git', 'coverage', '__tests__', 'tests', 'test', 'docs', 'examples',
        '_archive', '.venv', 'venv', 'pdfjs', 'pdfium-worker','mockups','mockup','prototypes'}
EXT = {'.tsx', '.jsx', '.ts', '.js', '.svelte', '.vue', '.rs', '.slint', '.py', '.html', '.css'}


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'OpenAEC-function-icon-audit'})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def selected(path):
    p = Path(path)
    if path=='open-pdf-studio/public/pdfjs/web/viewer.css': return True
    if not SKIP.intersection(p.parts) and p.suffix.lower() in {'.svg', '.png', '.ico', '.webp'} and re.search(r'icons?(?:/|\.)',path,re.I):
        return True
    if not SKIP.intersection(p.parts) and (p.name in {'package.json', 'package-lock.json'} or
            p.name in {'extension.json','manifest.json','openaec-extension.json','catalog.json'} or
            (p.suffix == '.json' and any(x in p.parts for x in ('locales', 'translations', 'i18n')))):
        return True
    if SKIP.intersection(p.parts) or p.suffix not in EXT:
        return False
    if re.search(r'\.(test|spec|min)\.|(?:_tests|_test)\.rs$', path):
        return False
    # Scan whole client trees, including icon registries outside components.
    return (p.suffix in {'.svelte', '.vue', '.slint', '.html', '.css'}
            or any(x in p.parts for x in ('src', 'ui', 'frontend', 'js', 'components', 'app','extensions'))
            or bool(re.search(r'icon|ribbon|toolbar|menu|window', p.name, re.I)))


def collect_repo(repo, metadata):
    commit = metadata.get('commit')
    result = {'repository': repo, 'app': APPS[repo], 'commit': commit,
              'branch': metadata.get('branch'), 'files': [], 'errors': []}
    if not commit:
        result['status'] = 'bron ontbreekt'
        return result
    base = CACHE / repo / commit
    tree_cache = base / '_tree.json'
    try:
        if tree_cache.exists():
            tree = json.loads(tree_cache.read_text(encoding='utf-8'))
        else:
            tree = json.loads(fetch(f'https://api.github.com/repos/OpenAEC-Foundation/{repo}/git/trees/{commit}?recursive=1'))
            base.mkdir(parents=True, exist_ok=True)
            tree_cache.write_text(json.dumps(tree), encoding='utf-8')
        if tree.get('truncated'):
            raise ValueError('GitHub tree is truncated: source enumeration incomplete')
        paths = [x['path'] for x in tree['tree'] if x['type'] == 'blob' and selected(x['path'])]
        result['tree_files'] = sum(x['type'] == 'blob' for x in tree['tree'])
        def download(path):
            dest = base / path
            try:
                if not dest.exists():
                    data = fetch(f'https://raw.githubusercontent.com/OpenAEC-Foundation/{repo}/{commit}/{urllib.parse.quote(path)}')
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
                data = dest.read_bytes()
                return {'path': path, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
            except Exception as error:
                return {'path': path, 'error': str(error)}
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            for record in pool.map(download, paths):
                result['errors' if 'error' in record else 'files'].append(record)
        result['files'].sort(key=lambda x: x['path'])
        result['selected_files'] = len(paths)
        result['status'] = 'brontekst opgehaald' if not result['errors'] else 'onvolledige download'
    except Exception as error:
        result['status'] = 'bron niet opgehaald'
        result['errors'].append({'error': str(error)})
    print(repo, result['status'], len(result['files']), 'files', len(result['errors']), 'errors', flush=True)
    return result


def main():
    inventory = {x['name']: x for x in json.loads((H / 'inventory.json').read_text(encoding='utf-8'))}
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda repo: collect_repo(repo, inventory.get(repo, {})), APPS))
    output = {'basis': 'Vastgelegde broncommits uit inventory.json; geen claim over nieuwste productieversies.',
              'scope': '16 apps uit APP-OVERZICHT.md; inclusief PDF v3 als bronvariant en de bekende Calc/Planner-extensierepositories.',
              'selection': 'Alle clientbronbestanden volgens selected(); afhankelijkheden, tests, docs en gegenereerde builds uitgesloten. Geen bereikbaarheidsgarantie.',
              'repositories': results}
    (H / 'function-icon-sources.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
