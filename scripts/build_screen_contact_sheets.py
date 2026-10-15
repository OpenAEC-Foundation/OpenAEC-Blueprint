#!/usr/bin/env python3
"""Render every indexed screen candidate from its pinned Git blob for review."""
from collections import defaultdict
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'harmonization/screen-index.json'
OUT = ROOT / 'design/screen-contact-sheets'
OUT.mkdir(exist_ok=True)
records = json.loads(SOURCE.read_text())['screens']
font_path = ROOT / 'assets/fonts/Inter-Regular.ttf'
font = ImageFont.truetype(str(font_path), 14)
small = ImageFont.truetype(str(font_path), 11)
groups = defaultdict(list)
for record in records:
    groups[(record['kind'], record['repository'])].append(record)

SHEET_W = 1380
CELL_W, CELL_H = 340, 190
manifest, errors = [], []
for (kind, repo), items in sorted(groups.items()):
    checkout = Path('/tmp/openaec-inventory') / repo
    head = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip() if (checkout / '.git').exists() else None
    for page, offset in enumerate(range(0, len(items), 20), 1):
        chunk = items[offset:offset + 20]
        sheet_h = 40 + ((len(chunk) + 3) // 4) * CELL_H + 8
        sheet = Image.new('RGB', (SHEET_W, sheet_h), '#f0f2f4')
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 10), f'OPENAEC / {repo} / {kind} / {page}', font=font, fill='#252a30')
        for index, record in enumerate(chunk):
            col, row = index % 4, index // 4
            x, y = 12 + col * CELL_W, 40 + row * CELL_H
            draw.rounded_rectangle((x, y, x + CELL_W - 8, y + CELL_H - 8), radius=5, fill='#fff', outline='#d4d9df')
            target = (x + 8, y + 7, CELL_W - 24, 142)
            try:
                if head != record['commit']:
                    raise ValueError('checkout commit differs from pinned source')
                data = subprocess.check_output(['git', '-C', str(checkout), 'show', f'HEAD:{record["path"]}'], stderr=subprocess.DEVNULL)
                with Image.open(BytesIO(data)) as source:
                    record['dimensions'] = list(source.size)
                    source = ImageOps.exif_transpose(source)
                    thumb = ImageOps.contain(source.convert('RGB'), (target[2], target[3]), Image.Resampling.LANCZOS)
                px = target[0] + (target[2] - thumb.width) // 2
                py = target[1] + (target[3] - thumb.height) // 2
                sheet.paste(thumb, (px, py))
                record['visual_status'] = 'rendered'
            except (subprocess.CalledProcessError, UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
                record['visual_status'] = f'error: {error}'
                errors.append({'repository': repo, 'path': record['path'], 'error': str(error)})
                draw.text((x + 16, y + 62), 'Afbeelding niet te lezen', font=small, fill='#a03e3e')
            label = record['path'].split('/')[-1]
            while draw.textlength(label, font=small) > CELL_W - 36:
                label = label[:-5] + '…' if len(label) > 7 else label[:4]
            draw.text((x + 10, y + 151), f'{offset + index + 1:03d}  {label}', font=small, fill='#28313b')
            if record.get('dimensions'):
                draw.text((x + 10, y + 166), f'{record["dimensions"][0]} × {record["dimensions"][1]} px', font=small, fill='#7b8792')
        slug = ''.join(ch.lower() if ch.isalnum() else '-' for ch in f'{kind}-{repo}').strip('-')
        filename = f'{slug}-{page:02d}.jpg'
        sheet.save(OUT / filename, quality=84, optimize=True)
        manifest.append({'kind': kind, 'repository': repo, 'page': page, 'file': filename, 'count': len(chunk),
                         'paths': [record['path'] for record in chunk]})
        print(f'{filename}: {len(chunk)}', flush=True)

assert sum(item['count'] for item in manifest) == len(records)
(OUT / 'manifest.json').write_text(json.dumps({'total': len(records), 'sheets': manifest, 'errors': errors,
                                               'screens': records}, ensure_ascii=False, indent=2) + '\n')
print(f'Rendered {len(records)} candidates across {len(manifest)} sheets; {len(errors)} errors')
