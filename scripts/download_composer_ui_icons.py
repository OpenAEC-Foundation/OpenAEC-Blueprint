#!/usr/bin/env python3
"""Extract only used Composer UI vectors from its lockfile-pinned Solid icon package."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
import tarfile
import urllib.request
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'harmonization/composer-ui-icons.json').read_text())
VERSION = '1.2.0'
URL = f'https://registry.npmjs.org/solid-icons/-/solid-icons-{VERSION}.tgz'
# package-lock.json at the pinned Composer source commit.
INTEGRITY = 'yjQxWQMi9l19P5Af9vjsvalTMDFPDL4XD6etrUdNxNVhFp1bMYF0SFwUa5VYDfJ7u0SF3Qkz/F7BZxqcLUwklw=='
raw = urllib.request.urlopen(URL, timeout=30).read()
assert hashlib.sha512(raw).digest() == base64.b64decode(INTEGRITY), 'npm integrity mismatch'
with tarfile.open(fileobj=BytesIO(raw), mode='r:gz') as package:
    source = package.extractfile('package/tb/index.js').read().decode()
    solid_license = package.extractfile('package/LICENSE').read()

target = ROOT / 'harmonization/ui-icons/open-aec-workspace-composer'
target.mkdir(parents=True, exist_ok=True)
(target / 'SOLID-ICONS-LICENSE.txt').write_bytes(solid_license)
tabler_license = urllib.request.urlopen(
    'https://raw.githubusercontent.com/tabler/tabler-icons/main/LICENSE', timeout=30).read()
(target / 'TABLER-ICONS-LICENSE.txt').write_bytes(tabler_license)

assets = []
for symbol in manifest['unique_used_symbols']:
    pattern = r'export function ' + re.escape(symbol) + r"\(props\)\{return IconTemplate\(\{a:(\{[^}]+\}),c:'([^']*)'\},props\)\}"
    matches = re.findall(pattern, source)
    assert len(matches) == 1, (symbol, len(matches))
    attrs = json.loads(matches[0][0])
    assert attrs['viewBox'] == '0 0 24 24'
    inner = html.unescape(matches[0][1])
    attr_text = ' '.join(f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items())
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" {attr_text}>{inner}</svg>\n'
    ET.fromstring(svg)
    name = re.sub(r'(?<!^)(?=[A-Z])', '-', symbol.removeprefix('TbOutline')).lower()
    path = target / f'{name}.svg'
    path.write_text(svg)
    assets.append({'symbol': symbol, 'path': str(path.relative_to(ROOT)),
                   'sha256': hashlib.sha256(svg.encode()).hexdigest(),
                   'placements': sum(u['symbol'] == symbol for u in manifest['usages'])})

index = {'source_repository': manifest['repository'], 'source_commit': manifest['commit'],
         'source_package': f'solid-icons@{VERSION}', 'package_url': URL,
         'package_integrity_sha512': INTEGRITY, 'assets': assets,
         'role': 'source UI-library vectors for review; not approved shared Rust icons',
         'licenses': [str((target / name).relative_to(ROOT)) for name in
                      ('SOLID-ICONS-LICENSE.txt', 'TABLER-ICONS-LICENSE.txt')]}
(ROOT / 'harmonization/composer-ui-icon-assets.json').write_text(json.dumps(index, indent=2) + '\n')

cards = ''.join(
    '<article><div class="sizes"><span class="s16"><img src="../' + a['path'] + '"></span>'
    '<span class="s24"><img src="../' + a['path'] + '"></span>'
    '<span class="s32"><img src="../' + a['path'] + '"></span></div>'
    '<b>' + html.escape(a['symbol']) + '</b><small>' + str(a['placements']) + ' UI-plaatsen</small></article>'
    for a in assets)
page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Workspace Composer · gebruikte UI-iconen</title><style>
:root{font:13px system-ui,sans-serif;color:#252a32;background:#f3f4f6}*{box-sizing:border-box}body{margin:0}
header{padding:22px 28px;background:#fff;border-bottom:1px solid #d7d9de}h1{font-size:22px;margin:0 0 7px}p{line-height:1.5;color:#59616b;margin:0}
main{padding:24px 28px}h2{font-size:16px;margin:0 0 14px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
article{background:#fff;border:1px solid #d7d9de;padding:14px;min-height:112px}article b,article small{display:block;overflow-wrap:anywhere}
article small{color:#59616b;margin-top:4px}.sizes{display:flex;gap:15px;align-items:center;height:44px;margin-bottom:7px}
.sizes span{display:grid;place-items:center;width:38px;height:38px}.s16 img{width:16px}.s24 img{width:24px}.s32 img{width:32px}
.dark{background:#242830;color:#f4f5f6;margin-top:24px;padding:22px}.dark article{background:#333840;border-color:#565d68}.dark small{color:#b8c0c8}
.dark img{filter:invert(1)}.dark p{color:#b8c0c8}a{color:#a76000}.dark a{color:#ffaf45}
</style><header><h1>Workspace Composer · daadwerkelijk gebruikte UI-iconen</h1>
<p>26 vormen · 51 JSX-plaatsen · broncommit 33327e0 · solid-icons 1.2.0. OpenAEC-symbool en pakketlogo’s zijn merkbeelden. Deze bronvormen zijn nog geen goedgekeurde Rust-iconen.</p></header>
<main><h2>Licht · 16 / 24 / 32 px</h2><div class="grid">''' + cards + '''</div></main>
<section class="dark"><h2>Donker · 16 / 24 / 32 px</h2><div class="grid">''' + cards + '''</div>
<p style="margin-top:20px">Bron- en licentiebewijs: <a href="../harmonization/composer-ui-icons.json">UI-aanroepen</a> · <a href="../harmonization/composer-ui-icon-assets.json">assetindex</a></p></section></html>'''
(ROOT / 'design/composer-ui-icon-review.html').write_text(page)
print(f'{len(assets)} pinned SVGs → {target}')
