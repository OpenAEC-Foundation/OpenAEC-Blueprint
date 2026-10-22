"""Export the B2 masters as deterministic, lossless gzip-compressed SVG assets."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import os

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'design/icon-set-b2'
OUT = SOURCE / 'library-lossless'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_if_changed(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(data)
    os.replace(temporary, path)


def compress(data):
    buffer = io.BytesIO()
    # No file name, timestamp or host-specific source path in the gzip header.
    with gzip.GzipFile(filename='', mode='wb', compresslevel=9, mtime=0, fileobj=buffer) as stream:
        stream.write(data)
    return buffer.getvalue()


def build():
    source_bytes = (SOURCE / 'manifest.json').read_bytes()
    source = json.loads(source_bytes)
    rows = []
    totals = {str(size): {'files': 0, 'original_bytes': 0, 'compressed_bytes': 0} for size in (16, 24)}
    for icon in source['icons']:
        assets = {}
        for size in ('16', '24'):
            original_path = SOURCE / icon['assets'][size]['path']
            original = original_path.read_bytes()
            assert sha256(original) == icon['assets'][size]['sha256'], original_path
            packed = compress(original)
            assert gzip.decompress(packed) == original, original_path
            relative = f'{size}/{icon["id"]}.svgz'
            write_if_changed(OUT / relative, packed)
            assets[size] = {
                'path': relative,
                'compressed_sha256': sha256(packed),
                'original_sha256': sha256(original),
                'compressed_bytes': len(packed),
                'original_bytes': len(original),
                'source_path': icon['assets'][size]['path'],
            }
            totals[size]['files'] += 1
            totals[size]['original_bytes'] += len(original)
            totals[size]['compressed_bytes'] += len(packed)
        rows.append({'id': icon['id'], 'label': icon['label'], 'assets': assets})
    # Catch concurrent changes before publishing a manifest for a mixed source set.
    assert (SOURCE / 'manifest.json').read_bytes() == source_bytes, 'B2 manifest changed during export'
    for total in totals.values():
        total['reduction_percent'] = round(100 * (1 - total['compressed_bytes'] / total['original_bytes']), 2)
    manifest = {
        'family': source['family'],
        'source_revision': source['revision'],
        'source_manifest_sha256': sha256(source_bytes),
        'format': 'gzip-compressed original SVG (SVGZ)',
        'compression': {'level': 9, 'mtime': 0, 'filename': ''},
        'geometry_changes': False,
        'icon_count': len(rows),
        'asset_count': sum(total['files'] for total in totals.values()),
        'totals': totals,
        'icons': rows,
    }
    write_if_changed(OUT / 'manifest.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
    print(json.dumps({'icons': len(rows), 'assets': manifest['asset_count'], 'totals': totals}, ensure_ascii=False))


if __name__ == '__main__':
    build()
