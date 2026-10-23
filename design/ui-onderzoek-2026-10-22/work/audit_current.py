import hashlib
import importlib.util
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'OpenAEC-Style-Repo'
u16 = lambda b, o: struct.unpack_from('>H', b, o)[0]
u32 = lambda b, o: struct.unpack_from('>I', b, o)[0]

def inspect_font(path):
    b = path.read_bytes()
    tables = {}
    for i in range(u16(b, 4)):
        tag, checksum, offset, length = struct.unpack_from('>4sIII', b, 12 + i * 16)
        tables[tag.decode()] = b[offset:offset + length]
    names = []
    n = tables['name']
    for i in range(u16(n, 2)):
        platform, encoding, language, name_id, length, offset = struct.unpack_from('>6H', n, 6 + 12 * i)
        if name_id == 5:
            raw = n[u16(n, 4) + offset:u16(n, 4) + offset + length]
            names.append(raw.decode('utf-16-be' if platform in (0, 3) else 'mac_roman', errors='replace'))
    features = set()
    for tag in ('GSUB', 'GPOS'):
        if tag in tables:
            t = tables[tag]
            start = u16(t, 6)
            if start:
                for i in range(u16(t, start)):
                    features.add(t[start + 2 + i * 6:start + 6 + i * 6].decode())
    # Unicode cmap formats 4 and 12, sufficient for this deliberately small probe.
    cmap = tables['cmap']
    subtables = []
    for i in range(u16(cmap, 2)):
        platform, encoding, offset = struct.unpack_from('>HHI', cmap, 4 + 8 * i)
        if platform == 0 or (platform == 3 and encoding in (1, 10)):
            subtables.append(cmap[offset:])
    def has(cp):
        for t in subtables:
            fmt = u16(t, 0)
            if fmt == 12:
                for i in range(u32(t, 12)):
                    first, last, glyph = struct.unpack_from('>III', t, 16 + i * 12)
                    if first <= cp <= last and glyph + cp - first:
                        return True
            elif fmt == 4 and cp <= 65535:
                count = u16(t, 6) // 2
                for i in range(count):
                    last = u16(t, 14 + i * 2)
                    first = u16(t, 16 + count * 2 + i * 2)
                    if first <= cp <= last:
                        delta = u16(t, 16 + count * 4 + i * 2)
                        ro_pos = 16 + count * 6 + i * 2
                        ro = u16(t, ro_pos)
                        glyph = (cp + delta) % 65536 if not ro else u16(t, ro_pos + ro + (cp - first) * 2)
                        if glyph:
                            return True
        return False
    probe = 'ĲĳéëçİıĞğŞş±−×Øø⌀²³≤≥αβσλ°€'
    return {'file': path.name, 'version': sorted(set(names)), 'features': sorted(features), 'missing_probe': ''.join(c for c in probe if not has(ord(c))), 'probe': probe, 'sha256': hashlib.sha256(b).hexdigest()}

spec = importlib.util.spec_from_file_location('tokens_check', REPO / 'scripts/check_tokens_04.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
tokens = json.loads((REPO / 'design/ontwerp-0.4/tokens-0.4.json').read_text())
problems, rows = check.evaluate(tokens)
pairs = [('white_on_amber', '#FFFFFF', '#D97706'), ('white_on_gradient_top', '#FFFFFF', '#E08A12'), ('dark_on_amber', '#1C1917', '#D97706'), ('amber_on_white', '#D97706', '#FFFFFF'), ('accent_text_on_white', '#92400E', '#FFFFFF'), ('body_on_white', '#2A2A32', '#FFFFFF'), ('body_on_dark', '#EDEBE8', '#2A2A32')]
evidence = {
    'date': '2026-10-22',
    'repo_commit': subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip(),
    'repo_status': subprocess.check_output(['git', '-C', str(REPO), 'status', '--short'], text=True).strip(),
    'token_check': {'themes': len(tokens['themes']), 'pairs': len(rows), 'problems': problems},
    'contrast_pairs': [{'name': name, 'fg': fg, 'bg': bg, 'ratio': round(check.contrast(fg, bg), 4)} for name, fg, bg in pairs],
    'fonts': [inspect_font(p) for p in sorted((REPO / 'crates/openaec-ui/assets/fonts').glob('*.ttf'))],
    'website_snapshots': [{'file': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (ROOT / 'open-aec-home.html', ROOT / 'open-aec-style.css')],
    'limits': 'Static source inspection and existing token checker only. No native app execution, user test, complete glyph coverage audit or conformance certification.'
}
(ROOT.parent / 'outputs/OpenAEC-onderzoeksbewijs.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'commit': evidence['repo_commit'], 'tokens': evidence['token_check'], 'contrasts': evidence['contrast_pairs'], 'fonts': [{'file': f['file'], 'version': f['version'], 'features': [v for v in f['features'] if v in ('ss02', 'ss04', 'cv05', 'cv08', 'tnum', 'zero')], 'missing_probe': f['missing_probe']} for f in evidence['fonts']]}, ensure_ascii=False, indent=2))
