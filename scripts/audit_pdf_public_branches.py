#!/usr/bin/env python3
"""Check public PDF refs and report source drift without changing pinned reviews."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = 'f754cb7c9d9adf654f6894cee15543413c24fcff'
REPOS = ['open-pdf-studio', 'open-pdf-studio-v3']
requested = ['dynlex', 'feat/rust-native']


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(['git', *(('-C', str(cwd)) if cwd else ()), *args], text=True).strip()


records = []
for name in REPOS:
    url = f'https://github.com/OpenAEC-Foundation/{name}.git'
    heads = {}
    for line in git('ls-remote', '--heads', url).splitlines():
        sha, ref = line.split('\t')
        heads[ref.removeprefix('refs/heads/')] = sha
    records.append({'repository': name, 'url': url.removesuffix('.git'),
                    'main': heads.get('main'), 'public_branch_count': len(heads),
                    'requested_branches': {branch: heads.get(branch) for branch in requested}})

cache = Path('/tmp/openaec-inventory/open-pdf-studio')
assert cache.joinpath('.git').is_dir()
assert git('rev-parse', 'HEAD', cwd=cache) == OLD
new = records[0]['main']
assert new
subprocess.check_call(['git', '-C', str(cache), 'fetch', '--quiet', 'origin', 'main'])
assert git('rev-parse', 'FETCH_HEAD', cwd=cache) == new

changed = []
jsx_deltas = []
for line in git('diff', '--name-status', OLD, new, cwd=cache).splitlines():
    parts = line.split('\t')
    path = parts[-1]
    ui_code = bool(re.search(r'\.(jsx|tsx|css|scss|slint)$', path, re.I))
    changed.append({'status': parts[0], 'path': path,
                    'ui_code_candidate': ui_code,
                    'icon_or_chrome_candidate': ui_code and bool(re.search(r'(icon|ribbon|panel|dialog|titlebar|toolbar|backstage)', path, re.I))})
    if path.endswith(('.jsx', '.tsx')):
        old_source = '' if parts[0].startswith('A') else git('show', f'{OLD}:{path}', cwd=cache)
        new_source = '' if parts[0].startswith('D') else git('show', f'{new}:{path}', cwd=cache)
        jsx_deltas.append({'path': path, 'old_literal_svg_tags': len(re.findall(r'<svg\b', old_source)),
                           'new_literal_svg_tags': len(re.findall(r'<svg\b', new_source))})

manifest = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
            'repositories': records, 'pinned_pdf_commit': OLD,
            'current_public_main': new, 'changed_file_count': len(changed),
            'ui_code_candidate_count': sum(item['ui_code_candidate'] for item in changed),
            'icon_or_chrome_candidate_count': sum(item['icon_or_chrome_candidate'] for item in changed),
            'changed_files': changed, 'jsx_literal_svg_counts': jsx_deltas,
            'conclusion': 'Prior PDF inventories remain pinned evidence; changed main files require a new UI-role audit before current-state claims.'}
(ROOT / 'harmonization/pdf-public-branch-drift.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(f'{len(changed)} changed files; {manifest["ui_code_candidate_count"]} UI-code candidates; '
      f'{manifest["icon_or_chrome_candidate_count"]} icon/chrome name candidates')
