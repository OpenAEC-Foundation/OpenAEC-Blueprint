"""Independently verify every compressed library asset against its original master."""
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'design/icon-set-b2'
LIBRARY = SOURCE / 'library-lossless'
REPORT = ROOT / 'harmonization/icon-set-b2/lossless-library-validation.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check():
    source_bytes = (SOURCE / 'manifest.json').read_bytes()
    source = json.loads(source_bytes)
    manifest_bytes = (LIBRARY / 'manifest.json').read_bytes()
    library = json.loads(manifest_bytes)
    assert library['source_revision'] == source['revision']
    assert library['source_manifest_sha256'] == digest(source_bytes)
    source_icons = {icon['id']: icon for icon in source['icons']}
    assert len(source_icons) == len(library['icons']) == library['icon_count']
    assert set(source_icons) == {icon['id'] for icon in library['icons']}
    expected = set()
    checked = 0
    totals = {str(size): {'files': 0, 'original_bytes': 0, 'compressed_bytes': 0} for size in (16, 24)}
    for row in library['icons']:
        icon = source_icons[row['id']]
        for size in ('16', '24'):
            asset = row['assets'][size]
            assert asset['path'] == f'{size}/{row["id"]}.svgz'
            path = LIBRARY / asset['path']
            expected.add(path.relative_to(LIBRARY).as_posix())
            packed = path.read_bytes()
            assert packed[:3] == b'\x1f\x8b\x08', path
            assert packed[3:8] == b'\0' * 5, 'gzip has optional fields or a nonzero timestamp'
            original = (SOURCE / icon['assets'][size]['path']).read_bytes()
            restored = gzip.decompress(packed)
            assert restored == original, f'Roundtrip changed the original SVG: {path}'
            assert digest(original) == icon['assets'][size]['sha256'] == asset['original_sha256'], path
            assert digest(packed) == asset['compressed_sha256'], path
            assert len(packed) == asset['compressed_bytes'] < len(original) == asset['original_bytes'], path
            assert asset['source_path'] == icon['assets'][size]['path']
            totals[size]['files'] += 1
            totals[size]['original_bytes'] += len(original)
            totals[size]['compressed_bytes'] += len(packed)
            checked += 1
    assert {p.relative_to(LIBRARY).as_posix() for p in LIBRARY.rglob('*.svgz')} == expected
    assert {p.relative_to(SOURCE).as_posix() for p in (SOURCE / 'svg').rglob('*.svg')} == {
        icon['assets'][size]['path'] for icon in source_icons.values() for size in ('16', '24')
    }
    for size, total in totals.items():
        total['reduction_percent'] = round(100 * (1 - total['compressed_bytes'] / total['original_bytes']), 2)
        assert total == library['totals'][size]
    assert checked == library['asset_count'] == 2 * len(source_icons)
    assert (SOURCE / 'manifest.json').read_bytes() == source_bytes
    report = {
        'status': 'geslaagd',
        'source_revision': source['revision'],
        'icons': len(source_icons),
        'assets_checked': checked,
        'all_roundtrips_byte_identical': True,
        'source_manifest_sha256': digest(source_bytes),
        'library_manifest_sha256': digest(manifest_bytes),
        'generator_sha256': digest((ROOT / 'scripts/build_b2_lossless_library.py').read_bytes()),
        'checker_sha256': digest(Path(__file__).read_bytes()),
        'totals': totals,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    check()
