#!/usr/bin/env python3
"""Inventory public OpenAEC repositories and archive visual assets at immutable SHAs.
No downloaded code is executed. Run again to resume failed downloads.
"""
import concurrent.futures as futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'harmonization'
CACHE = Path('/tmp/openaec-inventory')
EXT = {'.svg', '.png', '.ico', '.icns', '.bmp', '.webp', '.xpm'}

def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'OpenAEC-UI-inventory'}), timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == 2: raise
            time.sleep(attempt + 1)

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE, timeout=180).decode()

def inspect(meta):
    name = meta['name']
    repo = CACHE / name
    result = {'name': name, 'url': meta['html_url'], 'branch': meta['default_branch'],
              'description': meta.get('description'), 'archived': meta['archived'],
              'license': (meta.get('license') or {}).get('spdx_id', 'UNKNOWN'),
              'icons': [], 'icon_sources': [], 'manifests': [], 'errors': []}
    try:
        if not (repo / '.git').exists():
            subprocess.run(['git', 'clone', '--depth=1', '--filter=blob:none', '--no-checkout', '--single-branch', meta['clone_url'], str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=240)
        sha = git(repo, 'rev-parse', 'HEAD').strip()
        result['commit'] = sha
        paths = git(repo, 'ls-tree', '-r', '--name-only', 'HEAD').splitlines()
        result['files_scanned'] = len(paths)
        selected = []
        for path in paths:
            p = Path(path); low = path.lower()
            if any(x in p.parts for x in ['node_modules', 'target', '.venv', 'vendor']): continue
            kind = None
            if p.name in ('package.json', 'Cargo.toml', 'pyproject.toml'): kind = 'manifest'
            elif p.name.lower().startswith(('license', 'copying', 'ofl')): kind = 'license'
            elif p.suffix.lower() in EXT and (p.suffix.lower() in {'.svg', '.ico', '.icns', '.xpm'} or re.search(r'icon|logo|favicon|pictogram|toolbar|ribbon', low)): kind = 'icon'
            elif p.suffix.lower() in {'.ts', '.tsx', '.js', '.jsx', '.rs', '.py', '.json', '.css', '.slint'} and re.search(r'icon', p.name.lower()): kind = 'icon-source'
            if kind: selected.append((path, kind))
        base = OUT / 'sources' / name
        def download(item):
            path, kind = item
            dest = base / path
            url = f'https://raw.githubusercontent.com/{meta["full_name"]}/{sha}/{urllib.parse.quote(path)}'
            try:
                data = dest.read_bytes() if dest.exists() else fetch(url)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists(): dest.write_bytes(data)
                return {'path': path, 'kind': kind, 'source_url': url, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes':len(data)}
            except Exception as e: return {'path': path, 'error': str(e)}
        with futures.ThreadPoolExecutor(max_workers=6) as pool:
            for entry in pool.map(download, selected):
                if 'error' in entry: result['errors'].append(entry)
                elif entry['kind'] == 'icon': result['icons'].append(entry)
                elif entry['kind'] == 'icon-source': result['icon_sources'].append(entry)
                elif entry['kind'] == 'manifest': result['manifests'].append(entry)
        stack = set(); packages = set()
        for m in result['manifests']:
            text = (base / m['path']).read_text(errors='replace')
            for token, label in [('"react"','React'), ('"vue"','Vue'), ('"svelte"','Svelte'), ('tauri','Tauri'), ('iced','iced'), ('egui','egui'), ('eframe','egui'), ('slint','Slint'), ('PySide','Qt'), ('PyQt','Qt'), ('winit','winit'), ('dynlex','Dynlex')]:
                if token in text: stack.add(label)
            for match in re.findall(r'"([^"\n]*(?:lucide|icon|phosphor|heroicons)[^"\n]*)"\s*:', text): packages.add(match)
        result['ui_stack'] = sorted(stack)
        result['icon_packages'] = sorted(packages)
    except Exception as e: result['errors'].append({'stage':'tree', 'error':str(e)})
    (OUT / 'repositories').mkdir(parents=True,exist_ok=True)
    (OUT / 'repositories' / f'{name}.json').write_text(json.dumps(result, indent=2))
    print(f"{name}: {len(result['icons'])} visual assets, {len(result['icon_sources'])} icon-related source files, {len(result['errors'])} errors", flush=True)
    return result

def main():
    OUT.mkdir(exist_ok=True); CACHE.mkdir(exist_ok=True)
    repos = []; page = 1
    while True:
        batch = json.loads(fetch(f'https://api.github.com/orgs/OpenAEC-Foundation/repos?per_page=100&type=all&page={page}'))
        repos.extend(batch)
        if len(batch)<100: break
        page += 1
    (OUT / 'catalog.json').write_text(json.dumps(repos,indent=2))
    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = sorted(pool.map(inspect, repos),key=lambda x:x['name'].lower())
    (OUT / 'inventory.json').write_text(json.dumps(results,indent=2))
    hashes = {}
    for repo in results:
        for icon in repo['icons']:
            hashes.setdefault(icon['sha256'],[]).append(f"{repo['name']}/{icon['path']}")
    (OUT / 'duplicates.json').write_text(json.dumps({h:p for h,p in hashes.items() if len(p)>1},indent=2))
    lines = ['# OpenAEC UI-inventarisatie', '', 'Publiek beschikbare repositories in de OpenAEC-Foundation-organisatie. Elke bron is vastgelegd op een commit. Geen code uit de bronrepositories is uitgevoerd.', '',
             'Dit is een breed archief van visuele bronbestanden, geen telling van gebruikte UI-iconen: alle SVG/ICO/ICNS/XPM-bestanden en rasterbestanden met icon/logo/favicon/pictogram/toolbar/ribbon in het pad. Het omvat ook technische symbolen, tekeningen en branding. Inline iconen zijn als bronbestanden bewaard; externe iconpackages zijn geregistreerd, niet volledig gespiegeld. Voor UI-gebruik zie `asset-index.json`, `ui-code-references.json` en `../design/review.html`. Privérepositories en externe repositories vallen buiten deze inventarisatie.', '',
             'Gedownloade bronbestanden staan in `sources/` en worden **niet** meegeleverd in de Rust-crate. De repositorylicentie is een aanwijzing; afwijkende assetlicenties moeten bij selectie worden gecontroleerd.', '',
             '| Repository | UI-techniek (manifest) | Visuele bronbestanden | Icon-gerelateerde bronbestanden | Fouten |', '|---|---|---:|---:|---:|']
    for r in results:
        lines.append(f"| [{r['name']}]({r['url']}) | {', '.join(r.get('ui_stack',[])) or 'Niet vastgesteld'} | {len(r['icons'])} | {len(r['icon_sources'])} | {len(r['errors'])} |")
    lines += ['', f"Totaal: {len(results)} repositories, {sum(len(r['icons']) for r in results)} visuele bronbestanden, {len(hashes)} unieke bestandshashes."]
    (OUT / 'README.md').write_text('\n'.join(lines)+'\n')

if __name__ == '__main__': main()
