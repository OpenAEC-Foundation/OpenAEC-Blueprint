"""Toets iconen aan de richtlijn in docs/iconen.md: leesbaarheid op 16 px, niet te veel losse delen,
en genoeg verschil binnen een groep knoppen die naast elkaar staan.

De check meet de 16 px-master zoals hij op het scherm komt: de gevulde contouren uit
design/icon-set-b2/svg/16/ worden per pixel gerasterd (dekking 0..1). Alle maten zijn in pixels van die master.

Wat streng getoetst wordt (exit 1 bij een fout):
- elk icoon dat volgens de richtlijn getekend is (REVISED en de nieuwe ids in scripts/b2_richtlijn.py), ook op
  de regel dat één doorlopende lijn één kleur heeft: hoofdkleur en accent raken elkaar niet, op 16 en op 24 px;
- elke groep in design/iconen/groepen.json.
Met --alle meet de check daarnaast de hele B2-set en drukt hij af hoeveel iconen de regels nu al halen.
Dat deel is informatie, geen fout: de rest van de set wordt per tab herzien.

Negatieve controle: de oude B2-tekeningen in design/iconen/voorbeelden/fout/16/ moeten op de bedoelde regel
falen, met de regels van hun echte groep. Daarnaast moet per familie een verschoven kopie van het eerste icoon
falen: binnen een familie telt alleen vormverschil na uitlijnen, geen verschil in plaats of maat, ook niet
van één los deel.

Runtime: shapely (scripts/requirements-icon-b2.txt, in harmonization/sources/b2-runtime).
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'harmonization/sources/b2-runtime'))
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    import numpy as np
    import shapely
    from shapely import affinity
    from shapely.geometry import Polygon, box
except ImportError as error:
    raise SystemExit('Installeer eerst scripts/requirements-icon-b2.txt in harmonization/sources/b2-runtime') from error

from b2_richtlijn import NEW_DEFINITIONS, REVISED  # noqa: E402

SVG16 = ROOT / 'design/icon-set-b2/svg/16'
SVG24 = ROOT / 'design/icon-set-b2/svg/24'
GROUPS = ROOT / 'design/iconen/groepen.json'
WRONG = ROOT / 'design/iconen/voorbeelden/fout/16'

# Grenzen voor de 16 px-master. Onderbouwing en voorbeelden: docs/iconen.md, onder "Automatische checks".
MIN_GAP = 1.0          # px tussen losse delen (Lucide: 2 px op 24 bij lijn 2; hier lijn 1,25 op 16)
MIN_GAP_24 = 1.5       # px tussen losse delen in de 24 px-master
MIN_HOLE = 1.0         # px: een gat (binnenruimte) moet minstens zo breed zijn, anders loopt het dicht
MIN_PART = 2.0         # px²: kleiner deel is een vlekje
MAX_PARTS = 5          # losse delen (samenhangende vlakken) per icoon
MAX_ELEMENTS = 7       # lijnen, cirkels en vlakken in de tekening
MAX_DENSITY = 0.62     # hoogste gemiddelde dekking in een venster van 5 x 5 px (vervaagtest van Lucide)
MAX_INK = 0.36         # deel van het vlak van 16 x 16 dat inkt is
MIN_CRISP = 0.70       # scherpte: som(dekking²)/som(dekking); 1 is helemaal scherp
MAX_SIMILAR = 0.55     # gelijkenis (vervaagde overlap) tussen twee iconen in een groep
MAX_SHARED = 0.72      # deel van de inkt van het kleinere icoon dat precies op het andere valt
TOUCH = 0.06           # px: dichterbij raken twee vormen elkaar; load() sluit zulke naden
MIN_FAMILY_DIFF = 4.0  # px² vormverschil binnen een familie (Zoom + en Zoom −), na uitlijnen: niet kleur, plaats of maat
ALIGN_FINE = 0.25      # px: na het leggen op hetzelfde kader nog zoveel fijn bijschuiven
ALIGN_STEP = 0.05      # px: stap van het fijne bijschuiven
ALIGN_TOLERANCE = 0.05 # px: rest na uitlijnen telt niet als vormverschil
ALIGN_SCALES = (0.96, 0.98, 1.0, 1.02, 1.04)  # kleine maatverschillen die niet als vorm tellen
PART_SHIFT = 1.0       # px: zoveel mag een los deel (een plusje, een pijl) apart verschoven liggen
# Negatieve kopieproef per familie: (verschuiving x, y in px, schaal rond het midden, uiteinde rechtsonder 0,5 px
# langer). Elke kopie is dezelfde vorm.
COPY_PROOFS = ((0.1, 0.1, 1.0, False), (0.6, -0.4, 1.0, False), (2.5, 0.0, 1.0, False), (0.0, 0.0, 0.98, False),
               (0.3, -0.2, 1.03, False), (0.0, 0.0, 1.0, True), (1.2, 0.4, 1.0, True), (0.6, -0.4, 0.97, True))
COPY_PART_SHIFTS = ((0.5, 0.0), (0.0, -0.75), (0.75, 0.25))  # kopie waarin alleen het kleinste losse deel verschoven is


def layer(path_data: str):
    shape = Polygon()
    for ring in re.findall(r'M([^M]+?)Z', path_data):
        points = [tuple(map(float, p.strip().split())) for p in ring.split('L')]
        shape = shape.symmetric_difference(Polygon(points))
    return shape


def load(path: Path):
    """Inkt van een master: hoofdkleur en accent samen, plus de delen apart."""
    text = path.read_text(encoding='utf-8')
    parts = dict(re.findall(r'data-part="(\w+)"[^>]*\sd="([^"]*)"', text))
    primary = layer(parts.get('primary', ''))
    accent = layer(parts.get('accent', ''))
    # Delen die elkaar raken (accent vóór de hoofdkleur) zijn één vorm; sluit naden van rekenafronding.
    return shapely.union(primary, accent).buffer(0.03).buffer(-0.03), primary, accent


def raster(geometry, size=16):
    xs = np.arange(size, dtype=float)
    boxes = shapely.box(xs[None, :], xs[:, None], xs[None, :] + 1, xs[:, None] + 1)
    shapely.prepare(geometry)
    return shapely.area(shapely.intersection(boxes, geometry))


def blur(grid):
    padded = np.pad(grid, 1)
    k = np.array([1, 2, 1], dtype=float)
    rows = sum(k[i] * padded[:, i:i + grid.shape[1]] for i in range(3)) / 4
    return sum(k[i] * rows[i:i + grid.shape[0], :] for i in range(3)) / 4


def window_mean(grid, n=3):
    padded = np.pad(grid, n // 2)
    return max(padded[y:y + n, x:x + n].mean() for y in range(grid.shape[0]) for x in range(grid.shape[1]))


def polygons(geometry):
    if geometry.is_empty:
        return []
    return list(geometry.geoms) if hasattr(geometry, 'geoms') else [geometry]


def construction_elements(icon_id: str, manifest_icons: dict) -> int | None:
    icon = manifest_icons.get(icon_id)
    if not icon:
        return None
    model = icon['construction']['16']
    return len(model['paths']) + len(model['circles']) + len(model['fills'])


def measure(path: Path, elements: int | None = None):
    return measure_ink(*load(path), elements)


def two_colors(primary, accent) -> bool:
    """Eén doorlopende lijn heeft één kleur: raken hoofdkleur en accent elkaar, dan heeft één lijn er twee."""
    return not primary.is_empty and not accent.is_empty and primary.distance(accent) < TOUCH


def measure_ink(ink, primary, accent, elements: int | None = None):
    parts = polygons(ink)
    gaps = [a.distance(b) for a, b in itertools.combinations(parts, 2)]
    holes = [Polygon(r) for p in parts for r in p.interiors]
    grid = raster(ink)
    total = grid.sum()
    return {
        'parts': len(parts),
        'elements': elements,
        'min_gap': round(min(gaps), 3) if gaps else None,
        'narrow_holes': sum(h.buffer(-MIN_HOLE / 2).is_empty for h in holes),
        'smallest_part': round(min(p.area for p in parts), 3) if parts else 0,
        'density': round(float(window_mean(grid, 5)), 3),
        'ink': round(float(total / 256), 3),
        'crisp': round(float((grid ** 2).sum() / total), 3) if total else 0,
        'accent_area': round(accent.area, 3),
        'two_colors': two_colors(primary, accent),
        '_ink': ink,
        '_grid': grid,
    }


def legibility_errors(m) -> list[str]:
    errors = []
    if m['min_gap'] is not None and m['min_gap'] < MIN_GAP:
        errors.append(f"losse delen liggen {m['min_gap']} px uit elkaar (minimaal {MIN_GAP})")
    if m['narrow_holes']:
        errors.append(f"{m['narrow_holes']} gat(en) smaller dan {MIN_HOLE} px; dat loopt dicht")
    if m['smallest_part'] < MIN_PART:
        errors.append(f"kleinste deel is {m['smallest_part']} px², een vlekje (minimaal {MIN_PART})")
    if m['crisp'] < MIN_CRISP:
        errors.append(f"scherpte {m['crisp']} (minimaal {MIN_CRISP}); lijnen liggen naast het pixelraster")
    return errors


def colour_errors(m) -> list[str]:
    return ['hoofdkleur en accent raken elkaar: één doorlopende lijn heeft dan twee kleuren'] if m['two_colors'] else []


def detail_errors(m) -> list[str]:
    errors = []
    if m['parts'] > MAX_PARTS:
        errors.append(f"{m['parts']} losse delen (maximaal {MAX_PARTS})")
    if m['elements'] is not None and m['elements'] > MAX_ELEMENTS:
        errors.append(f"{m['elements']} lijnen, cirkels en vlakken (maximaal {MAX_ELEMENTS})")
    if m['density'] > MAX_DENSITY:
        errors.append(f"te vol: een plek van 5 x 5 px is {m['density']} dicht (maximaal {MAX_DENSITY})")
    if m['ink'] > MAX_INK:
        errors.append(f"{round(m['ink'] * 100)} % van het vlak is inkt (maximaal {round(MAX_INK * 100)} %)")
    return errors


def residual(a, a_wide, c, dx=0.0, dy=0.0) -> float:
    """Wat van a buiten c valt en van c buiten a, met ALIGN_TOLERANCE speling; c eerst dx, dy verschoven."""
    return (a.difference(affinity.translate(c.buffer(ALIGN_TOLERANCE), dx, dy)).area
            + affinity.translate(c, dx, dy).difference(a_wide).area)


def fine(a, c) -> tuple[float, float, float]:
    """Kleinste residu als c nog tot ALIGN_FINE bijschuift; met de verschuiving die het oplevert."""
    a_wide = a.buffer(ALIGN_TOLERANCE)
    n = int(round(ALIGN_FINE / ALIGN_STEP))
    return min((residual(a, a_wide, c, i * ALIGN_STEP, j * ALIGN_STEP), i * ALIGN_STEP, j * ALIGN_STEP)
               for i in range(-n, n + 1) for j in range(-n, n + 1))


def parts_difference(a, c) -> float | None:
    """Vormverschil per los deel: elk deel van c schuift apart (tot PART_SHIFT) naar het deel van a waar het het meest
    mee overlapt.
    Zo telt alleen het verplaatsen van een los teken (een plusje in de lens) niet als vorm. None als de delen niet
    één op één bij elkaar horen."""
    parts_a, parts_c = polygons(a), polygons(c)
    if len(parts_a) != len(parts_c) or len(parts_a) < 2:
        return None
    match = [max(parts_a, key=lambda p: p.intersection(q.buffer(PART_SHIFT)).area) for q in parts_c]
    if len({id(p) for p in match}) != len(match):
        return None
    total = 0.0
    for p, q in zip(match, parts_c):
        dx, dy = p.centroid.x - q.centroid.x, p.centroid.y - q.centroid.y
        if (dx * dx + dy * dy) ** 0.5 > PART_SHIFT:
            dx = dy = 0.0
        total += fine(p, affinity.translate(q, dx, dy))[0]
    return total


def shape_difference(a, b) -> float:
    """Vormverschil in px² na uitlijnen, het kleinste over een paar manieren om b op a te leggen:
    - b precies op het omhullende kader van a (een iets groter of kleiner getekende kopie);
    - b in een kleine maat (ALIGN_SCALES) met een hoek of het midden van zijn kader op dat van a. Zo valt een kopie
      weg die verschoven, iets geschaald of aan één uiteinde iets langer is, of een combinatie daarvan;
    - daarna ook per los deel (parts_difference): een plusje dat alleen een halve pixel verschoven is, telt niet.
    Eerst worden alle manieren zonder bijschuiven gemeten; de drie beste schuiven daarna tot ALIGN_FINE bij.
    Wat binnen ALIGN_TOLERANCE van de andere vorm ligt, telt niet. Spiegelen telt wel: bij Inspringen en
    Uitspringen is dat juist het verschil."""
    ax0, ay0, ax1, ay1 = a.bounds
    bx0, by0, bx1, by1 = b.bounds
    sx, sy = (ax1 - ax0) / (bx1 - bx0), (ay1 - ay0) / (by1 - by0)
    candidates = [affinity.affine_transform(b, [sx, 0, 0, sy, ax0 - bx0 * sx, ay0 - by0 * sy])]
    anchors = ((ax0, ay0, bx0, by0), (ax1, ay1, bx1, by1), (ax0, ay1, bx0, by1), (ax1, ay0, bx1, by0),
               ((ax0 + ax1) / 2, (ay0 + ay1) / 2, (bx0 + bx1) / 2, (by0 + by1) / 2))
    for k in ALIGN_SCALES:
        for pax, pay, pbx, pby in anchors:
            candidates.append(affinity.affine_transform(b, [k, 0, 0, k, pax - k * pbx, pay - k * pby]))
    a_wide = a.buffer(ALIGN_TOLERANCE)
    scored = sorted(((residual(a, a_wide, c), i, c) for i, c in enumerate(candidates)), key=lambda t: t[:2])
    if scored[0][0] == 0:
        return 0.0
    best, best_c = float('inf'), None
    for _, _, c in scored[:3]:
        value, dx, dy = fine(a, c)
        if value < best:
            best, best_c = value, affinity.translate(c, dx, dy)
    per_part = parts_difference(a, best_c)
    return best if per_part is None else min(best, per_part)


def pair(a, b):
    """Gelijkenis van twee iconen op 16 px: vervaagde overlap en gedeelde inkt."""
    ba, bb = blur(a['_grid']), blur(b['_grid'])
    similar = float(np.minimum(ba, bb).sum() / np.maximum(ba, bb).sum())
    shared_area = a['_ink'].intersection(b['_ink']).area
    shared = shared_area / min(a['_ink'].area, b['_ink'].area)
    return round(similar, 3), round(shared, 3)


def group_errors(group, metrics) -> list[str]:
    errors = []
    families = [set(f) for f in group.get('families', [])]
    for x, y in itertools.combinations(group['ids'], 2):
        if any({x, y} <= f for f in families):
            diff = round(shape_difference(metrics[x]['_ink'], metrics[y]['_ink']), 2)
            if diff < MIN_FAMILY_DIFF:
                errors.append(f'{x} en {y}: familie, maar het vormverschil na uitlijnen is {diff} px² (minimaal {MIN_FAMILY_DIFF}); '
                              'het verschil mag niet alleen kleur of een detail zijn')
            continue
        similar, shared = pair(metrics[x], metrics[y])
        if similar > MAX_SIMILAR:
            errors.append(f'{x} en {y} lijken te veel op elkaar: gelijkenis {similar} (maximaal {MAX_SIMILAR})')
        if shared > MAX_SHARED:
            errors.append(f'{x} en {y} delen {round(shared * 100)} % van hun vorm (maximaal {round(MAX_SHARED * 100)} %): '
                          'zelfde basis met een klein verschil')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--alle', action='store_true', help='meet ook de rest van de set (alleen informatie)')
    parser.add_argument('--json', type=Path, help='schrijf alle metingen als JSON')
    args = parser.parse_args()

    manifest = json.loads((ROOT / 'design/icon-set-b2/manifest.json').read_text(encoding='utf-8'))
    icons = {i['id']: i for i in manifest['icons']}
    groups = json.loads(GROUPS.read_text(encoding='utf-8'))
    guideline = set(REVISED) | {d[0] for d in NEW_DEFINITIONS}
    grouped = {i for g in groups['groepen'] for i in g['ids']}
    missing = sorted((guideline | grouped) - set(icons))
    if missing:
        raise SystemExit(f'onbekende ids: {missing}')

    failures = []
    metrics = {}
    for icon_id in sorted(guideline | grouped):
        metrics[icon_id] = measure(SVG16 / f'{icon_id}.svg', construction_elements(icon_id, icons))
    for icon_id in sorted(guideline):
        for error in legibility_errors(metrics[icon_id]) + detail_errors(metrics[icon_id]) + colour_errors(metrics[icon_id]):
            failures.append(f'{icon_id}: {error}')
        ink24, primary24, accent24 = load(SVG24 / f'{icon_id}.svg')
        if two_colors(primary24, accent24):
            failures.append(f'{icon_id}: in de 24 px-master raken hoofdkleur en accent elkaar: één doorlopende lijn heeft dan twee kleuren')
        parts24 = polygons(ink24)
        gap24 = min((a.distance(b) for a, b in itertools.combinations(parts24, 2)), default=None)
        if gap24 is not None and gap24 < MIN_GAP_24:
            failures.append(f'{icon_id}: in de 24 px-master liggen losse delen {round(gap24, 3)} px uit elkaar (minimaal {MIN_GAP_24})')
    for group in groups['groepen']:
        if not group['ids']:
            continue
        for error in group_errors(group, metrics):
            failures.append(f"groep {group['app']} › {group['tab']} › {group['naam']}: {error}")

    # Negatieve controle: de oude tekeningen moeten op de bedoelde regel vallen.
    controls = 0
    for control in groups.get('negatieve_controles', []):
        wrong = {i: measure(WRONG / f'{i}.svg') for i in control['ids']}
        if control['regel'] == 'gelijkenis':
            # Dezelfde groepsregels als de echte groep, ook de families; anders bewijst de controle niets over die groep.
            group = next((g for g in groups['groepen'] if set(control['ids']) <= set(g['ids'])), {})
            caught = group_errors({'ids': control['ids'], 'families': group.get('families', [])}, wrong)
        elif control['regel'] == 'kleur':
            caught = [e for i in control['ids'] for e in colour_errors(wrong[i])]
        elif control['regel'] == 'detail':
            caught = [e for i in control['ids'] for e in detail_errors(wrong[i])]
        else:
            caught = [e for i in control['ids'] for e in legibility_errors(wrong[i])]
        if not caught:
            failures.append(f"negatieve controle '{control['naam']}' vangt niets meer; de check is te los geworden")
        controls += 1

    # Negatieve kopieproef: een verschoven of iets geschaalde kopie van een familielid is dezelfde vorm en moet in de
    # echte familie falen.
    for group in groups['groepen']:
        for family in group.get('families', []):
            original = metrics[family[0]]
            for dx, dy, scale, longer in COPY_PROOFS:
                ink = original['_ink']
                if longer:
                    # Het uiteinde rechtsonder 0,5 px verder doortrekken, zoals een iets langer handvat.
                    x0, y0, x1, y1 = ink.bounds
                    ink = ink.union(affinity.translate(ink, 0.5, 0.5).intersection(box(x1 - 2, y1 - 2, x1 + 1, y1 + 1)))
                ink = affinity.translate(affinity.scale(ink, scale, scale, origin=(8, 8)), dx, dy)
                copy = measure_ink(ink, Polygon(), Polygon())
                caught = group_errors({'ids': [family[0], 'kopie'], 'families': [[family[0], 'kopie']]},
                                      {family[0]: original, 'kopie': copy})
                if not caught:
                    extra = ', uiteinde langer' if longer else ''
                    failures.append(f"familie {family}: een kopie van {family[0]} ({dx}/{dy} px verschoven, {scale:g} x{extra}) "
                                    'komt door de familiecontrole; die meet plaats of maat in plaats van vorm')
                controls += 1
            # Alleen het kleinste losse deel (het actieteken) verschoven: dezelfde vorm.
            parts = polygons(original['_ink'])
            if len(parts) > 1:
                small = min(parts, key=lambda q: q.area)
                for dx, dy in COPY_PART_SHIFTS:
                    ink = shapely.union_all([q for q in parts if q is not small] + [affinity.translate(small, dx, dy)])
                    copy = measure_ink(ink, Polygon(), Polygon())
                    caught = group_errors({'ids': [family[0], 'kopie'], 'families': [[family[0], 'kopie']]},
                                          {family[0]: original, 'kopie': copy})
                    if not caught:
                        failures.append(f"familie {family}: een kopie van {family[0]} met alleen het kleinste losse deel "
                                        f"{dx}/{dy} px verschoven komt door de familiecontrole")
                    controls += 1

    summary = {'status': 'geslaagd' if not failures else 'gefaald',
               'richtlijn_iconen': len(guideline), 'groepen': len(groups['groepen']),
               'negatieve_controles': controls, 'fouten': len(failures)}
    if args.alle:
        rest = sorted(set(icons) - guideline)
        passing = two_coloured = 0
        for icon_id in rest:
            m = measure(SVG16 / f'{icon_id}.svg', construction_elements(icon_id, icons))
            metrics[icon_id] = m
            passing += not (legibility_errors(m) + detail_errors(m) + colour_errors(m))
            two_coloured += m['two_colors']
        summary['rest_van_de_set'] = {'iconen': len(rest), 'halen_de_regels_nu': passing, 'lijn_in_twee_kleuren': two_coloured}
    if args.json:
        args.json.write_text(json.dumps({k: {n: v for n, v in m.items() if not n.startswith('_')}
                                         for k, m in metrics.items()}, ensure_ascii=False, indent=1), encoding='utf-8')
    for failure in failures:
        print('FOUT', failure)
    print(json.dumps(summary, ensure_ascii=False))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
