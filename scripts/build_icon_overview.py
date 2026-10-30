"""Maak het overzichtsblad van een tab en de voorbeeldbeelden van docs/iconen.md.

Overzichtsblad: per knop de betekenis, het nieuwe icoon en het icoon van Open Planner Studio op main,
op 16 en 24 px, in licht en donker, en in welke andere programma's een gedeeld icoon nog meer zit.
  - <map>/overzicht.html: ware grootte in de browser (inline SVG), met de betekenis uit het manifest.
  - <map>/overzicht-<n>.png: per pagina licht en donker, ware grootte en elke pixel 4 x vergroot.
Voorbeeldbeelden: docs/images/iconen/*.png (goed en fout per principe).

Rastert met rsvg-convert (librsvg) en Pillow; dit draait op Linux, niet in de CI.
Gebruik:
  python3 scripts/build_icon_overview.py design/iconen/planning
  python3 scripts/build_icon_overview.py --voorbeelden
"""
from __future__ import annotations

import argparse
import html
import io
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from b2_richtlijn import NEW_APPS  # noqa: E402
from b2_source_catalog import load_catalog  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / 'design/icon-set-b2/svg'
MAIN = ROOT / 'design/iconen/referentie/ops-main'
WRONG = ROOT / 'design/iconen/voorbeelden/fout'
DOCS = ROOT / 'docs/images/iconen'
TOKENS = json.loads((ROOT / 'design/ontwerp-0.4/tokens-0.4.json').read_text(encoding='utf-8'))['themes']
THEMES = [(name, TOKENS[name]['color']['panel'], TOKENS[name]['color']['text'], TOKENS[name]['color']['accent'])
          for name in ('light', 'dark')]
THEME_NL = {'light': 'licht', 'dark': 'donker'}
FONT = ROOT / 'assets/fonts/Inter-Regular.ttf'
FONT_BOLD = ROOT / 'assets/fonts/Inter-SemiBold.ttf'
ZOOM = 4


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def paint(svg: str, ink: str, accent: str) -> str:
    for token in ('var(--icon-accent,currentColor)', 'var(--icon-accent, currentColor)'):
        svg = svg.replace(token, accent)
    return svg.replace('currentColor', ink)


def raster(svg: str, px: int, bg: str, ink: str, accent: str) -> Image.Image:
    data = subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px)], input=paint(svg, ink, accent).encode(),
                          capture_output=True, check=True).stdout
    icon = Image.open(io.BytesIO(data)).convert('RGBA')
    base = Image.new('RGBA', icon.size, bg)
    base.alpha_composite(icon)
    return base.convert('RGB')


def source(kind: str, key: str, size: int) -> str:
    """kind: nieuw (B2-master), main (Lucide-referentie), fout (oude B2-tekening), allaccent (nieuw, alles oranje)."""
    if kind == 'main':
        # 'x@12': het icoon staat in main op 12 px in plaats van 16; teken het in het vak even klein als in het lint.
        name, _, px = key.partition('@')
        svg = (MAIN / f'{name}.svg').read_text(encoding='utf-8')
        if px and int(px) != 16:
            a = (24 * 16 / int(px) - 24) / 2
            svg = svg.replace('viewBox="0 0 24 24"', f'viewBox="{-a:g} {-a:g} {24 + 2 * a:g} {24 + 2 * a:g}"', 1)
        return svg
    if kind == 'fout':
        return (WRONG / str(size) / f'{key}.svg').read_text(encoding='utf-8')
    svg = (SVG / str(size) / f'{key}.svg').read_text(encoding='utf-8')
    if kind == 'allaccent':
        svg = svg.replace('fill="currentColor"', 'fill="var(--icon-accent,currentColor)"')
    return svg


def tile(kind: str, key: str, bg: str, ink: str, accent: str) -> Image.Image:
    """[16][24] op ware grootte, daarna [16 x4][24 x4]."""
    pad = 6
    w = pad + 16 + pad + 24 + pad + 16 * ZOOM + pad + 24 * ZOOM + pad
    h = 24 * ZOOM + 2 * pad
    out = Image.new('RGB', (w, h), bg)
    ims = {px: raster(source(kind, key, px), px, bg, ink, accent) for px in (16, 24)}
    base = pad + 24 * ZOOM
    x = pad
    out.paste(ims[16], (x, base - 16)); x += 16 + pad
    out.paste(ims[24], (x, base - 24)); x += 24 + pad
    out.paste(ims[16].resize((16 * ZOOM, 16 * ZOOM), Image.NEAREST), (x, base - 16 * ZOOM)); x += 16 * ZOOM + pad
    out.paste(ims[24].resize((24 * ZOOM, 24 * ZOOM), Image.NEAREST), (x, base - 24 * ZOOM))
    return out


def sheet(rows, heads, out: Path, label_width=300, title=None):
    """rows: [{'label','sub','cells':[(kind,key), ...]}]; licht links, donker rechts."""
    tiles = [[[tile(k, key, bg, ink, acc) for k, key in r['cells']] for _, bg, ink, acc in THEMES] for r in rows]
    tw, th = tiles[0][0][0].size
    gap, top = 4, 58 if title else 34
    ncell = len(rows[0]['cells'])
    width = label_width + len(THEMES) * (ncell * (tw + gap) + 18)
    height = top + len(rows) * (th + gap) + 8
    img = Image.new('RGB', (width, height), '#C9C9CC')
    d = ImageDraw.Draw(img)
    if title:
        d.text((10, 8), title, fill='#1C1917', font=font(17, True))
    x = label_width
    for name, *_ in THEMES:
        for head in heads:
            d.text((x + 4, top - 22), f'{THEME_NL[name]}: {head}', fill='#1C1917', font=font(13, True))
            x += tw + gap
        x += 18
    y = top
    for r, row_tiles in zip(rows, tiles):
        d.text((10, y + 18), r['label'], fill='#1C1917', font=font(14, True))
        for i, line in enumerate(r.get('sub', [])):
            d.text((10, y + 40 + 17 * i), line, fill='#3F3F46', font=font(12))
        x = label_width
        for theme_tiles in row_tiles:
            for t in theme_tiles:
                img.paste(t, (x, y)); x += tw + gap
            x += 18
        y += th + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    return out


def used_in() -> dict[str, set[str]]:
    """Programma's waar een id echt aan een bronplaats gekoppeld is (function-plan.json), plus de bedoelde
    programma's van een nieuw id. Ruimer dan dit is candidate_apps: dat volgt de naamcluster, niet de betekenis."""
    plan = json.loads((ROOT / 'harmonization/icon-set-b2/function-plan.json').read_text(encoding='utf-8'))
    apps = {r['id']: r['app'] for r in load_catalog()['records']}
    result: dict[str, set[str]] = {k: set(v) for k, v in NEW_APPS.items()}
    for row in plan['record_assessments']:
        for key in row.get('canonical_functions') or []:
            result.setdefault(key, set()).add(apps[row['record_id']])
    return result


def inline(svg: str, px: int) -> str:
    return svg.replace('<svg ', f'<svg class="i" width="{px}" height="{px}" ', 1)


def overview(folder: Path):
    spec = json.loads((folder / 'knoppen.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'design/icon-set-b2/manifest.json').read_text(encoding='utf-8'))
    icons = {i['id']: i for i in manifest['icons']}
    rows, html_rows = [], []
    usage = used_in()
    for k in spec['knoppen']:
        icon = icons[k['id']]
        others = sorted(usage.get(k['id'], set()) - {'Planner'})
        status = 'nieuw id' if icon['series'] == 167 else 'herzien' if icon.get('guideline') else 'ongewijzigd (B2)'
        main = f"{k['main']}@{k['main_px']}" if 'main_px' in k else k['main']
        sub = [f"{k['tab']} › {k['groep']}", f"{k['id']} · {status}"]
        if 'main_px' in k:
            sub.append(f"main: {k['main_px']} px, zoals in het lint")
        if others:
            sub.append('ook in: ' + ', '.join(others[:4]))
            if others[4:]:
                sub.append('         ' + ', '.join(others[4:]))
        rows.append({'label': k['knop'], 'sub': sub,
                     'cells': [('nieuw', k['id']), ('main', main)]})
        cells = []
        for kind, key in (('nieuw', k['id']), ('main', main)):
            parts = []
            for name, bg, ink, acc in THEMES:
                svgs = ''.join(inline(source(kind, key, px), px) for px in (16, 24))
                big = inline(source(kind, key, 24), 48)
                parts.append(f'<span class="t" style="background:{bg};color:{ink};--icon-accent:{acc}">{svgs}{big}</span>')
            cells.append(''.join(parts))
        html_rows.append(
            f"<tr><td><b>{html.escape(k['knop'])}</b><br><small>{html.escape(k['tab'])} › {html.escape(k['groep'])}</small></td>"
            f"<td>{html.escape(icon['meaning'])}<br><code>{k['id']}</code> · {status}</td>"
            f"<td>{cells[0]}</td><td>{cells[1]}<br><small>Lucide <code>{k['main']}</code></small></td>"
            f"<td>{html.escape(', '.join(others)) or '—'}</td></tr>")
    pages = [rows[i:i + 11] for i in range(0, len(rows), 11)]
    for old in folder.glob('overzicht-*.png'):
        old.unlink()
    for n, page in enumerate(pages, 1):
        sheet(page, ['nieuw', 'main'], folder / f'overzicht-{n}.png', label_width=340,
              title=f"{spec['titel']} — blad {n} van {len(pages)} (ware grootte, daarna elke pixel 4 x)")
    (folder / 'overzicht.html').write_text(f"""<!doctype html><html lang="nl"><meta charset="utf-8">
<title>{html.escape(spec['titel'])} · overzichtsblad iconen</title>
<style>body{{font:14px/1.45 Inter,system-ui,sans-serif;margin:24px;color:#1C1917;background:#F4F4F5}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #D4D4D8;padding:8px;vertical-align:top;text-align:left}}
.t{{display:inline-flex;gap:10px;align-items:flex-end;padding:8px 10px;margin:0 6px 6px 0;border-radius:6px}}
.i{{display:block}}small{{color:#52525B}}code{{font-size:12px}}</style>
<h1>{html.escape(spec['titel'])}</h1><p>{html.escape(spec['uitleg'])}</p>
<p>Elk vak toont 16 px en 24 px op ware grootte, en 24 px op dubbele grootte. Links licht, rechts donker.
Richtlijn: <a href="../../../docs/iconen.md">docs/iconen.md</a>.</p>
<table><thead><tr><th>Knop</th><th>Betekenis</th><th>Nieuw</th><th>Main</th><th>Ook in</th></tr></thead>
<tbody>{''.join(html_rows)}</tbody></table></html>
""", encoding='utf-8')
    print(folder / 'overzicht.html', len(pages), 'bladen')


# Voorbeelden in docs/iconen.md: per beeld rijen met (label, regels eronder, [(soort, id), ...]).
FIGURES = {
    'principe-1-inklapknop': (['goed', 'fout'], [
        ('Inklapknop van het lint', ['goed: klein pijltje aan de rand', 'fout: tekening van een lint (B2, #56 c)'],
         [('nieuw', 'workspace.ribbon-collapse'), ('fout', 'workspace.ribbon-compact')]),
    ]),
    'principe-2-bereken': (['Planner en FEM', 'Calc'], [
        ('Bereken', ['links: rekenkern laat doorrekenen (solver.run)', 'rechts: bedrag uitrekenen (planning.calculate)'],
         [('nieuw', 'solver.run'), ('nieuw', 'planning.calculate')]),
    ]),
    'principe-3-detail': (['goed', 'fout'], [
        ('Hernummer WBS', ['fout: kleine cijfers 1 en 2'], [('nieuw', 'wbs.renumber'), ('fout', 'wbs.renumber')]),
        ('Waarschuwingen', ['fout: paneelkader met driehoekje (#56 a)'], [('nieuw', 'panel.warnings'), ('fout', 'panel.warnings')]),
    ]),
    'principe-4-groep-fout': (['oud (B2)'], [
        (lbl, [], [('fout', key)]) for lbl, key in (
            ('Baseline-overlay', 'planning.baseline-overlay'), ('Voortgangslijn', 'planning.progress-line'),
            ('Statusdatumlijn', 'planning.status-date-line'), ('Balkkleuren', 'planning.bar-colors'),
            ('Resource-accent', 'planning.resource-accent'), ('Spelingsband', 'planning.float-band'),
            ('Relatielijnen', 'planning.relations-visible'))
    ]),
    'principe-4-groep-goed': (['nieuw'], [
        (lbl, [], [('nieuw', key)]) for lbl, key in (
            ('Baseline-overlay', 'planning.baseline-overlay'), ('Voortgangslijn', 'planning.progress-line'),
            ('Statusdatumlijn', 'planning.status-date-line'), ('Balkkleuren', 'planning.bar-colors'),
            ('Resource-accent', 'planning.resource-accent'), ('Spelingsband', 'planning.float-band'),
            ('Relatielijnen', 'planning.relations-visible'))
    ]),
    'principe-5-zoom': (['nieuw', 'main (Lucide)'], [
        ('Zoomen +', [], [('nieuw', 'view.zoom-in'), ('main', 'zoom-in')]),
        ('Zoomen −', [], [('nieuw', 'view.zoom-out'), ('main', 'zoom-out')]),
        ('Standaardzoom', ['main gebruikte hier een oog'], [('nieuw', 'view.zoom-default'), ('main', 'eye')]),
    ]),
    'regel-accent': (['goed', 'fout'], [
        ('Project verplaatsen', ['goed: alleen het klokje oranje', 'fout: alles oranje'],
         [('nieuw', 'planning.move-date'), ('allaccent', 'planning.move-date')]),
    ]),
}


def toggle_states(out: Path):
    """Principe 6: een actieve schakelaar toont de knop zelf, zoals elke lintknop; geen eigen tint."""
    light = TOKENS['light']['color']
    svg = source('nieuw', 'planning.progress-line', 16)
    cases = [('uit', light['panel'], None, light['text']),
             ('goed: aan, zoals\nelke lintknop', light['accent'], None, light['text-on-accent']),
             ('fout: eigen\noranje tint', '#FBEBD5', light['accent'], light['text'])]
    w, h, gap = 28, 28, 72
    img = Image.new('RGB', (len(cases) * (w * ZOOM + gap) + 24, h * ZOOM + 80), '#C9C9CC')
    d = ImageDraw.Draw(img)
    x = 24
    for label, bg, border, ink in cases:
        btn = Image.new('RGB', (w, h), light['panel'])
        bd = ImageDraw.Draw(btn)
        bd.rounded_rectangle([0, 0, w - 1, h - 1], radius=4, fill=bg, outline=border)
        icon = raster(svg, 16, bg, ink, ink if bg == light['accent'] else light['accent'])
        btn.paste(icon, (6, 6))
        img.paste(btn.resize((w * ZOOM, h * ZOOM), Image.NEAREST), (x, 16))
        d.multiline_text((x, h * ZOOM + 26), label, fill='#1C1917', font=font(13, True), spacing=3)
        x += w * ZOOM + gap
    img.save(out, optimize=True)


def examples():
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, (heads, rows) in FIGURES.items():
        sheet([{'label': lbl, 'sub': sub, 'cells': cells} for lbl, sub, cells in rows], heads, DOCS / f'{name}.png',
              label_width=320)
    toggle_states(DOCS / 'principe-6-schakelaar.png')
    print(DOCS, len(FIGURES) + 1, 'beelden')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('map', nargs='?', type=Path, help='map met knoppen.json, bijv. design/iconen/planning')
    parser.add_argument('--voorbeelden', action='store_true', help='maak de beelden voor docs/iconen.md')
    args = parser.parse_args()
    if args.map:
        overview(ROOT / args.map if not args.map.is_absolute() else args.map)
    if args.voorbeelden:
        examples()


if __name__ == '__main__':
    main()
