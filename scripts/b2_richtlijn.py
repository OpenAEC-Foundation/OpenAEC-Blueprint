"""Iconen die volgens de richtlijn in docs/iconen.md opnieuw getekend zijn.

Eerste ronde: de tab Planning van Open Planner Studio, met de knoppen die de eigenaar in zijn
controle van 29 oktober 2026 noemde (zoom, inklapknop van het lint, de schakelaars van
Baselines & voortgang). De werkwijze staat in .claude/skills/iconen-ontwerpen/SKILL.md.

Elke tekening staat hier twee keer, in de pixels van de master zelf:
- 16 px: lijndikte 1,25. Rechte lijnen liggen op het midden van een pixel (x,5), zodat ze scherp blijven.
- 24 px: lijndikte 1,75. Rechte lijnen liggen op hele pixels.
De vormen zijn bekende vormen (vergrootglas, kalender, vlag, pijl). De lijnen zijn hier zelf getekend;
er is geen geometrie uit een andere iconenset overgenomen.

`b2_geometry.construction` kijkt eerst hier. Een id in REVISED houdt zijn naam; alleen de vorm verandert.
Een nieuwe betekenis krijgt een nieuw id (NEW_DEFINITIONS); de oude naam blijft bestaan.
"""
import math

# Een herzien icoon: waarom.
REVISED = {}
DRAWINGS = {}

# Nieuwe betekenissen: (id, label, groep, betekenis). De groep volgt de bestaande B2-groepen.
NEW_DEFINITIONS = [
    ('solver.run', 'Doorrekenen', 'Taken en planningsberekening',
     'Een rekenkern het hele model of de hele planning opnieuw laten doorrekenen: datums, speling en kritiek pad '
     'in een planning, krachten en verplaatsingen in een constructie. Geen bedrag of hoeveelheid uitrekenen; '
     'daarvoor blijft de rekenmachine.'),
    ('workspace.ribbon-collapse', 'Lint inklappen', 'Werkruimte',
     'Het lint inklappen tot de tabbladen; de knop staat aan de rand van het lint. Tegenhanger van workspace.ribbon-expand.'),
    ('workspace.ribbon-expand', 'Lint uitklappen', 'Werkruimte',
     'Het ingeklapte lint weer volledig tonen; de knop staat aan de rand van het lint. Tegenhanger van workspace.ribbon-collapse.'),
    ('planning.progress-sheet-export', 'Voortgangsblad exporteren', 'Referenties, peildatum en relaties',
     'Een voortgangsblad (werkblad) wegschrijven waarin de uitvoering de voortgang per taak invult. Geen algemene export '
     'van het project; daarvoor blijft file.export. Tegenhanger van planning.progress-sheet-import.'),
    ('planning.progress-sheet-import', 'Voortgang bijwerken uit een blad', 'Referenties, peildatum en relaties',
     'De voortgang overnemen uit een ingevuld voortgangsblad: bestaande taken worden bijgewerkt. Geen algemene import; '
     'daarvoor blijft file.import. Tegenhanger van planning.progress-sheet-export.'),
]
# Programma's waar de nieuwe betekenis voorkomt. Bij een bestaand id komt dit uit de broncatalogus.
NEW_APPS = {
    'solver.run': ['FEM', 'Planner'],
    'workspace.ribbon-collapse': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
    'workspace.ribbon-expand': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
    'planning.progress-sheet-export': ['Planner'],
    'planning.progress-sheet-import': ['Planner'],
}
# Een bestaand id met een nieuwe betekenistekst. De naam blijft; de tekst zegt nu waar het icoon voor is.
MEANING_UPDATES = {
    'planning.calculate': 'Een bedrag of hoeveelheid uitrekenen (rekenmachine). Open Planner Studio gebruikt voor Bereken '
                          'sinds de richtlijn solver.run: daar laat een rekenkern de planning doorrekenen (#57).',
}


class Pen:
    """Tekent in de pixels van de master; geen schaal naar 24."""

    def __init__(self, c):
        self.c = c
        self.s = c.size

    def line(self, points, accent=False, closed=False, r=None):
        radius = (1.5 if self.s == 16 else 2.0) if r is None else r
        self.c.paths.append({'points': [(float(x), float(y)) for x, y in points], 'closed': closed,
                             'radius': float(radius), 'tone': 'accent' if accent else 'primary'})

    def rect(self, x0, y0, x1, y1, accent=False, r=None):
        self.line([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], accent, True, r)

    def circle(self, x, y, r, accent=False, filled=False):
        self.c.circles.append({'x': float(x), 'y': float(y), 'r': float(r),
                               'tone': 'accent' if accent else 'primary', 'filled': filled})

    def arc(self, cx, cy, r, start, end, accent=False, steps=None):
        """Boog van `start` naar `end` graden (0 = rechts, met de klok mee, want y loopt omlaag)."""
        n = steps or max(8, int(abs(end - start) / 6))
        pts = [(cx + r * math.cos(math.radians(start + (end - start) * i / n)),
                cy + r * math.sin(math.radians(start + (end - start) * i / n))) for i in range(n + 1)]
        self.line(pts, accent, False, 0)
        return pts

    def fill(self, points, accent=False):
        self.c.fills.append({'rings': [[(float(x), float(y)) for x, y in points]], 'tone': 'accent' if accent else 'primary'})


def design(key, reason):
    def register(fn):
        DRAWINGS[key] = fn
        REVISED[key] = reason
        return fn
    return register


# ---------------------------------------------------------------- zoom: vergrootglas met oranje teken (#52)

def magnifier(p):
    if p.s == 16:
        p.circle(7.5, 7.5, 5)
        p.line([(11.25, 11.25), (14.25, 14.25)], r=0)
        return 7.5, 2.0
    p.circle(11, 11, 7.5)
    p.line([(16.5, 16.5), (21, 21)], r=0)
    return 11, 3.0


@design('view.zoom-in', 'Vergrootglas zoals in Open Planner Studio, met de plus in oranje (#52).')
def zoom_in(p):
    m, a = magnifier(p)
    p.line([(m - a, m), (m + a, m)], True, r=0)
    p.line([(m, m - a), (m, m + a)], True, r=0)


@design('view.zoom-out', 'Vergrootglas zoals in Open Planner Studio, met de min in oranje (#52).')
def zoom_out(p):
    m, a = magnifier(p)
    p.line([(m - a, m), (m + a, m)], True, r=0)


@design('view.zoom-default', 'Hetzelfde vergrootglas als Zoom + en Zoom −, met een oranje punt: de standaardmaat (#52). '
                             'De punt is een vol blokje op het pixelraster, zodat hij niet op een kleine plus lijkt.')
def zoom_default(p):
    m, _ = magnifier(p)
    h, c = (1.5, 0.5) if p.s == 16 else (2.0, 0.6)
    p.fill([(m - h + c, m - h), (m + h - c, m - h), (m + h, m - h + c), (m + h, m + h - c),
            (m + h - c, m + h), (m - h + c, m + h), (m - h, m + h - c), (m - h, m - h + c)], True)


# ---------------------------------------------------------------- groep Planning

@design('solver.run', 'Afspeelpijl: de rekenkern laten lopen, zoals Bereken in Open Planner Studio (#55, #57).')
def solver_run(p):
    if p.s == 16:
        p.line([(4.5, 2.5), (13.5, 8), (4.5, 13.5)], closed=True, r=1.6)
    else:
        p.line([(6, 3.5), (20.5, 12), (6, 20.5)], closed=True, r=2.2)


def calendar_clock(p, accent):
    if p.s == 16:
        p.line([(13.5, 5.5), (13.5, 3.5), (1.5, 3.5), (1.5, 14.5), (5.5, 14.5)])
        p.line([(4.5, 1.5), (4.5, 4.5)], r=0)
        p.line([(10.5, 1.5), (10.5, 4.5)], r=0)
        p.line([(1.5, 7.5), (5.5, 7.5)], r=0)
        p.circle(11, 11, 3.75, accent)
        p.line([(11, 9.6), (11, 11), (12.2, 11.7)], accent, r=0.3)
    else:
        p.line([(20, 8.5), (20, 4), (3, 4), (3, 21), (9, 21)])
        p.line([(8, 2), (8, 6)], r=0)
        p.line([(15, 2), (15, 6)], r=0)
        p.line([(3, 10), (9, 10)], r=0)
        p.circle(17, 17, 5.25, accent)
        p.line([(17, 15.1), (17, 17), (18.6, 18)], accent, r=0.4)


@design('planning.move-date', 'Kalender met klok zoals in Open Planner Studio; het klokje in oranje (#55).')
def move_date(p):
    calendar_clock(p, True)


@design('planning.status-date', 'Veldaanduiding bij de statusdatum: dezelfde kalender met klok als in Open Planner '
                                'Studio, zonder oranje, want het veld is geen actie.')
def status_date(p):
    calendar_clock(p, False)


@design('panel.warnings', 'Waarschuwingsdriehoek zoals in Open Planner Studio, zonder paneelkader (#56 a). Eén ding, dus geen oranje.')
def warnings(p):
    if p.s == 16:
        p.line([(7.5, 1.75), (14.25, 13.5), (0.75, 13.5)], closed=True, r=1.4)
        p.line([(7.5, 6.5), (7.5, 8.25)], r=0)
        p.circle(7.5, 10.75, 0.8, filled=True)
    else:
        p.line([(12, 3), (22, 20.5), (2, 20.5)], closed=True, r=2)
        p.line([(12, 9.75), (12, 13)], r=0)
        p.circle(12, 16.5, 1.1, filled=True)


# ---------------------------------------------------------------- groep Relaties

def link_half(p, c, d, length, r, open_deg, short):
    """Eén helft van een schakel langs de diagonaal: een staaf met ronde kop buiten en een open binnenkant.

    c is het midden van het icoon, d de afstand van c tot de binnenkop, length de afstand tussen de kopmiddens.
    De binnenkop loopt maar `open_deg` graden door; de andere zijde is met `short` ingekort, zodat de
    helften niet in elkaar lopen."""
    ux, uy = math.sqrt(0.5), -math.sqrt(0.5)          # naar rechtsboven
    nx, ny = math.sqrt(0.5), math.sqrt(0.5)           # dwars, naar rechtsonder
    ix, iy = c[0] + ux * d, c[1] + uy * d             # midden van de binnenkop
    ox, oy = ix + ux * length, iy + uy * length       # midden van de buitenkop
    base = math.degrees(math.atan2(ny, nx))            # 45 graden: de zijde rechtsonder
    pts = [(ix + r * math.cos(math.radians(base + open_deg - i * open_deg / 10)),
            iy + r * math.sin(math.radians(base + open_deg - i * open_deg / 10))) for i in range(11)]
    pts += [(ox + r * math.cos(math.radians(base - i * 18)), oy + r * math.sin(math.radians(base - i * 18))) for i in range(11)]
    ex, ey = ox - nx * r, oy - ny * r
    pts.append((ex - ux * length * (1 - short), ey - uy * length * (1 - short)))
    return pts


@design('planning.relations-menu', 'Schakel zoals Relatie in Open Planner Studio: twee open helften langs de diagonaal. '
                                   'De ontwerpcontrole vond de gesloten ketting niet beter dan main (29 oktober 2026).')
def relations_menu(p):
    c, args = ((8, 8), (1.75, 2.9, 3.1, 95, 0.5)) if p.s == 16 else ((12, 12), (2.6, 4.3, 4.6, 95, 0.5))
    half = link_half(p, c, *args)
    p.line(half, r=0)
    p.line([(2 * c[0] - x, 2 * c[1] - y) for x, y in half], r=0)


@design('task.split-mode', 'Schaar zoals Taak splitsen in Open Planner Studio. De gesplitste taakbalk was op 16 px te klein '
                           '(ontwerpcontrole 29 oktober 2026). De schaar staat in Open Planner Studio alleen bij deze knop.')
def split_mode(p):
    if p.s == 16:
        r, (a, b), tip = 2.25, (4, 12), 13.5
    else:
        r, (a, b), tip = 3.25, (6, 18), 20.5
    k = r * math.sqrt(0.5)
    p.circle(a, a, r)
    p.circle(a, b, r)
    p.line([(a + k, a + k), (tip, tip)], r=0)
    p.line([(a + k, b - k), (tip, a + b - tip)], r=0)


def trace(p, successors):
    if p.s == 16:
        p.line([(2.5, 3), (2.5, 12)], r=0)
        p.line([(14, 7.5), (6, 7.5)], True, r=0)
        p.line([(9, 4), (5.5, 7.5), (9, 11)], True, r=0.6)
    else:
        p.line([(3, 5), (3, 19)], r=0)
        p.line([(21, 12), (8, 12)], True, r=0)
        p.line([(12.5, 7), (7.5, 12), (12.5, 17)], True, r=0.8)
    if successors:
        p.c.mirror()


@design('planning.trace-predecessors', 'Pijl naar een streep, zoals Voorgangers in Open Planner Studio; de hele pijl in oranje, '
                                       'want één doorlopende lijn heeft één kleur (Ethan, 30 oktober 2026) (#48).')
def trace_pred(p):
    trace(p, False)


@design('planning.trace-successors', 'Gespiegelde pijl naar een streep, zoals Opvolgers in Open Planner Studio; de hele pijl in '
                                     'oranje, zoals bij Voorgangers (#48).')
def trace_succ(p):
    trace(p, True)


# ---------------------------------------------------------------- groep Kalender

@design('calendar.manage', 'Kalenderblad zoals in Open Planner Studio, zonder stippen in het vlak.')
def calendar_manage(p):
    if p.s == 16:
        p.rect(1.5, 3.5, 14.5, 14.5)
        p.line([(4.5, 1.5), (4.5, 4.5)], r=0)
        p.line([(11.5, 1.5), (11.5, 4.5)], r=0)
        p.line([(1.5, 7.5), (14.5, 7.5)], r=0)
    else:
        p.rect(3, 4, 21, 21, r=2.2)
        p.line([(8, 2), (8, 6)], r=0)
        p.line([(16, 2), (16, 6)], r=0)
        p.line([(3, 10), (21, 10)], r=0)


# ---------------------------------------------------------------- groep Structuur

def tag(p, tip, length, width, angle, accent=False, hole=None):
    """Etiket met punt bij `tip`, lengte langs `angle` (graden), breedte `width` (hartlijn)."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    t = width / 2
    x, y = tip
    pts = [(x, y),
           (x + ux * t + nx * t, y + uy * t + ny * t),
           (x + ux * length + nx * t, y + uy * length + ny * t),
           (x + ux * length - nx * t, y + uy * length - ny * t),
           (x + ux * t - nx * t, y + uy * t - ny * t)]
    p.line(pts, accent, True, 1.0 if p.s == 16 else 1.4)
    if hole:
        d, r = hole
        p.circle(x + ux * d, y + uy * d, r, filled=True)
    return pts


@design('planning.structure', 'Twee etiketten, zoals Codes & velden in Open Planner Studio (#53). Eén ding, dus geen oranje.')
def structure(p):
    if p.s == 16:
        tag(p, (3.25, 1.75), 10.5, 6.5, 45, hole=(3.8, 0.9))
        p.line([(1.55, 8.6), (6.1, 13.15)], r=0)
    else:
        tag(p, (4.875, 2.625), 15.75, 9.75, 45, hole=(5.7, 1.35))
        p.line([(2.3, 12.9), (9.15, 19.75)], r=0)


def hash_sign(p, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    ys = (y0 + round(h * 0.3 * 2) / 2, y0 + round(h * 0.7 * 2) / 2) if p.s == 16 else (y0 + round(h * 0.3), y0 + round(h * 0.7))
    for yy in ys:
        p.line([(x0, yy), (x1, yy)], r=0)
    sl = h * 0.12
    for xx in ((x0 + w * 0.36, x0 + w * 0.72) if p.s == 24 else (x0 + w * 0.34, x0 + w * 0.7)):
        p.line([(xx + sl, y0), (xx - sl, y1)], r=0)


@design('wbs.auto-number', 'Hekje voor nummering, zoals WBS auto in Open Planner Studio; geen cijfers.')
def wbs_auto(p):
    if p.s == 16:
        hash_sign(p, 2, 1.5, 14, 14.5)
    else:
        hash_sign(p, 3, 2, 21, 22)


def refresh(p, cx, cy, r, accent=True, start=-60, end=230):
    """Draaipijl: open boog met één gevulde pijlpunt aan het eind, die in de open ruimte wijst."""
    p.arc(cx, cy, r, start, end, accent)
    a = math.radians(end)
    ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)   # raaklijn in looprichting
    nx, ny = math.cos(a), math.sin(a)    # naar buiten
    w, length = (1.7, 2.4) if p.s == 16 else (2.6, 3.6)
    p.fill([(ex + nx * w, ey + ny * w), (ex + tx * length, ey + ty * length), (ex - nx * w, ey - ny * w)], accent)


@design('wbs.renumber', 'Hekje met een oranje draaipijl: de nummering opnieuw doen. Geen kleine cijfers 1 en 2, die op 16 px onleesbaar zijn.')
def wbs_renumber(p):
    if p.s == 16:
        p.line([(1.5, 3.5), (11.5, 3.5)], r=0)
        p.line([(1.5, 8.5), (8.5, 8.5)], r=0)
        p.line([(4.5, 1.5), (3.5, 12.5)], r=0)
        p.line([(9, 1.5), (8.5, 8.5)], r=0)
        refresh(p, 12.25, 12.25, 2.75, start=-20, end=250)
    else:
        hash_sign(p, 2, 2, 14, 14)
        refresh(p, 18.5, 18.5, 3.75, start=-20, end=250)


@design('wbs.templates', 'Indelingsvlak met drie vakken, zoals Sjablonen in Open Planner Studio.')
def wbs_templates(p):
    if p.s == 16:
        p.rect(1.5, 1.5, 14.5, 6.5, r=1.2)
        p.rect(1.5, 9.5, 8.5, 14.5, r=1.2)
        p.rect(11.5, 9.5, 14.5, 14.5, r=1.2)
    else:
        p.rect(3, 3, 21, 10, r=1.6)
        p.rect(3, 14, 12, 21, r=1.6)
        p.rect(16, 14, 21, 21, r=1.6)


def indent(p, out):
    if p.s == 16:
        for y in (2.5, 7.5, 12.5):
            p.line([(7.5, y), (14.5, y)], r=0)
        pts = [(1.75, 4.25), (4.75, 7.5), (1.75, 10.75)]
        if out:
            pts = [(6.5 - x, y) for x, y in pts]
    else:
        for y in (5, 12, 19):
            p.line([(11, y), (21, y)], r=0)
        pts = [(3, 7.5), (7.5, 12), (3, 16.5)]
        if out:
            pts = [(10.5 - x, y) for x, y in pts]
    p.line(pts, True, r=0.6)


@design('task.indent', 'Regels met een oranje punthaak naar rechts, zoals Inspringen in Open Planner Studio.')
def task_indent(p):
    indent(p, False)


@design('task.outdent', 'Regels met een oranje punthaak naar links, zoals Uitspringen in Open Planner Studio.')
def task_outdent(p):
    indent(p, True)


# ---------------------------------------------------------------- groep Baselines & voortgang (tab Planning)

@design('planning.baselines', 'Twee versies met pijlen ertussen, zoals Baselines beheren in Open Planner Studio. '
                               'De knop opent een venster; geen deel toont een actie, dus geen oranje.')
def baselines(p):
    if p.s == 16:
        p.circle(3.5, 3.5, 1.75)
        p.circle(12.5, 12.5, 1.75)
        p.line([(7.5, 3.5), (10.5, 3.5), (12.5, 5.5), (12.5, 8.5)], r=1.5)
        p.line([(9.5, 1.5), (7.5, 3.5), (9.5, 5.5)], r=0.4)
        p.line([(8.5, 12.5), (5.5, 12.5), (3.5, 10.5), (3.5, 7.5)], r=1.5)
        p.line([(6.5, 10.5), (8.5, 12.5), (6.5, 14.5)], r=0.4)
    else:
        p.circle(5, 5, 2.5)
        p.circle(19, 19, 2.5)
        p.line([(11.5, 5), (16, 5), (19, 8), (19, 12)], r=2.2)
        p.line([(14, 2.5), (11.5, 5), (14, 7.5)], r=0.6)
        p.line([(12.5, 19), (8, 19), (5, 16), (5, 12)], r=2.2)
        p.line([(10, 16.5), (12.5, 19), (10, 21.5)], r=0.6)


@design('planning.clear-status-date', 'Klein kruisje zoals het wisknopje bij de statusdatum in Open Planner Studio; zelfde maat als daar.')
def clear_status_date(p):
    if p.s == 16:
        p.line([(5.5, 5.5), (10.5, 10.5)], r=0)
        p.line([(10.5, 5.5), (5.5, 10.5)], r=0)
    else:
        p.line([(8, 8), (16, 16)], r=0)
        p.line([(16, 8), (8, 16)], r=0)


@design('planning.progress-menu', 'Vlag zoals het ingeklapte menu Baselines & voortgang in Open Planner Studio.')
def progress_menu(p):
    if p.s == 16:
        p.line([(3.5, 1.5), (3.5, 14.5)], r=0)
        p.line([(3.5, 2.5), (6, 1.75), (9, 3), (13, 2.25), (13, 9.25), (9, 10), (6, 8.75), (3.5, 9.5)], closed=False, r=1.2)
    else:
        p.line([(5, 2), (5, 22)], r=0)
        p.line([(5, 3.5), (9, 2.5), (13.5, 4.5), (19.5, 3.5), (19.5, 14), (13.5, 15), (9, 13), (5, 14)], closed=False, r=1.6)


def sheet_arrow(p, down):
    """Blad met omgevouwen hoek en een oranje pijl, zoals Voortgang in Open Planner Studio (FileDown, FileUp)."""
    if p.s == 16:
        p.line([(2.5, 1.5), (8.5, 1.5), (12.5, 5.5), (12.5, 14.5), (2.5, 14.5)], closed=True, r=1.2)
        p.line([(8.5, 1.5), (8.5, 5.5), (12.5, 5.5)], r=0.6)
        p.line([(7.5, 8), (7.5, 12)], True, r=0)
        p.line([(5.5, 10), (7.5, 12), (9.5, 10)] if down else [(5.5, 10), (7.5, 8), (9.5, 10)], True, r=0.4)
    else:
        p.line([(4, 2), (14, 2), (20, 8), (20, 22), (4, 22)], closed=True, r=1.6)
        p.line([(14, 2), (14, 8), (20, 8)], r=0.8)
        p.line([(12, 11), (12, 18)], True, r=0)
        p.line([(9, 15), (12, 18), (15, 15)] if down else [(9, 14), (12, 11), (15, 14)], True, r=0.6)


@design('planning.progress-sheet-export', 'Blad met pijl omlaag, zoals Voortgangsblad exporteren in Open Planner Studio (FileDown). '
                                          'Eigen id: file.export is gedeeld en blijft het bakje met pijl; de ontwerpcontrole '
                                          'vond dat op deze knop slechter dan main (29 oktober 2026).')
def progress_sheet_export(p):
    sheet_arrow(p, True)


@design('planning.progress-sheet-import', 'Blad met pijl omhoog, zoals Voortgang bijwerken uit een blad in Open Planner Studio (FileUp). '
                                          'Eigen id om dezelfde reden als planning.progress-sheet-export.')
def progress_sheet_import(p):
    sheet_arrow(p, False)


# ---------------------------------------------------------------- inklapknop van het lint (#40)

@design('workspace.ribbon-collapse', 'Klein pijltje omhoog aan de rand van het lint, zoals in Open Planner Studio vóór B2 (#40, #56 c).')
def ribbon_collapse(p):
    if p.s == 16:
        p.line([(4.5, 9.75), (8, 6.25), (11.5, 9.75)], r=0.6)
    else:
        p.line([(7, 14.5), (12, 9.5), (17, 14.5)], r=0.8)


@design('workspace.ribbon-expand', 'Klein pijltje omlaag aan de rand van het lint, de tegenhanger van Lint inklappen (#40).')
def ribbon_expand(p):
    if p.s == 16:
        p.line([(4.5, 6.25), (8, 9.75), (11.5, 6.25)], r=0.6)
    else:
        p.line([(7, 9.5), (12, 14.5), (17, 9.5)], r=0.8)


# ---------------------------------------------------------------- schakelaars Baselines & voortgang (tab Beeld)
# Elke schakelaar tekent alleen het ding dat hij op de Gantt aan- of uitzet, zonder gedeeld assenkader (#56 b, #48).
# De actieve stand toont de lintknop zelf, zoals bij elke andere schakelaar in het lint.

@design('planning.baseline-overlay', 'Taakbalk met de baseline eronder in oranje, zoals de grijze baselinebalk in MS Project; geen assenkader.')
def baseline_overlay(p):
    if p.s == 16:
        p.rect(1.5, 2.5, 11.5, 7.5, r=1.2)
        p.line([(4.5, 11.5), (14.5, 11.5)], True, r=0)
    else:
        p.rect(2, 4, 17, 11, r=1.6)
        p.line([(6, 17), (22, 17)], True, r=0)


@design('planning.progress-line', 'Getande verticale lijn: de voortgangslijn zoals P6 en MS Project hem op de Gantt tekenen; geen assenkader.')
def progress_line(p):
    if p.s == 16:
        p.line([(7.5, 1.5), (7.5, 3), (12.5, 5.75), (7.5, 8.5), (2.5, 11.25), (7.5, 13.5), (7.5, 14.5)], r=0.5)
    else:
        p.line([(11, 2), (11, 5), (18, 9), (11, 13), (5, 16.5), (11, 20), (11, 22)], r=0.7)


@design('planning.status-date-line', 'Verticale lijn met een plat oranje merkteken erboven: de statusdatumlijn op de Gantt; geen assenkader. '
                                     'Merkteken los van de lijn, zodat het niet op een trechter lijkt.')
def status_date_line(p):
    if p.s == 16:
        p.line([(7.5, 6.5), (7.5, 14.5)], r=0)
        p.fill([(4, 1), (11, 1), (7.5, 4.5)], True)
    else:
        p.line([(12, 10), (12, 22)], r=0)
        p.fill([(6, 2), (18, 2), (12, 7.5)], True)


def palette(p):
    """Palet: een ronde plank met een ondiepe duimuitsparing rechtsonder."""
    cx, cy, r = (8, 8, 6.25) if p.s == 16 else (12, 12, 9.5)
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(68, 383, 6)]
    pts += [(cx + r * 0.58 * math.cos(math.radians(45)), cy + r * 0.58 * math.sin(math.radians(45)))]
    p.line(pts, closed=True, r=1.0 if p.s == 16 else 1.5)
    if p.s == 16:
        return [(4.75, 7.5, 1.05), (7.25, 4.75, 1.05), (10.25, 5.75, 1.05)]
    return [(7, 11, 1.5), (11, 6.5, 1.5), (15.75, 8.5, 1.5)]


@design('planning.bar-colors', 'Palet zoals Balkkleuren in Open Planner Studio; de verfklodders in oranje.')
def bar_colors(p):
    for x, y, r in palette(p):
        p.circle(x, y, r, True, True)


@design('planning.resource-accent', 'Persoon met een oranje lichaam: de resource krijgt een eigen kleur. Eigen vorm naast het palet ernaast.')
def resource_accent(p):
    if p.s == 16:
        p.circle(8, 4.25, 2.6)
        p.arc(8, 15.25, 6, 180, 360, True)
    else:
        p.circle(12, 6.25, 3.75)
        p.arc(12, 22.5, 9, 180, 360, True)


@design('planning.float-band', 'Pijl in twee richtingen voor speling, zoals Spelingsband in Open Planner Studio.')
def float_band(p):
    if p.s == 16:
        p.line([(1.5, 7.5), (14.5, 7.5)], r=0)
        p.line([(4.5, 4.5), (1.5, 7.5), (4.5, 10.5)], r=0.5)
        p.line([(11.5, 4.5), (14.5, 7.5), (11.5, 10.5)], r=0.5)
    else:
        p.line([(2, 12), (22, 12)], r=0)
        p.line([(6, 8), (2, 12), (6, 16)], r=0.7)
        p.line([(18, 8), (22, 12), (18, 16)], r=0.7)


@design('planning.relations-visible', 'Afhankelijkheidspijl einde-begin zoals op de Gantt: haaks naar beneden en naar rechts. '
                                      'Eén doorlopende lijn heeft één kleur, en het icoon is alleen dat ding, dus geen oranje.')
def relations_visible(p):
    if p.s == 16:
        p.line([(1.5, 3.5), (5.5, 3.5), (5.5, 11.5), (12.5, 11.5)], r=1.4)
        p.line([(10, 8.5), (13, 11.5), (10, 14.5)], r=0.5)
    else:
        p.line([(2, 5), (8, 5), (8, 17), (19, 17)], r=2)
        p.line([(15.5, 12.5), (20, 17), (15.5, 21.5)], r=0.7)


# ---------------------------------------------------------------- installeren, bijwerken, openen en starten
# Tweede ronde (30 oktober 2026): de knoppen van de OpenAEC Installer en dezelfde betekenissen elders in de
# Blueprint. Ze waren allemaal een venster met een klein oranje teken eronder; op 16 px leken ze op elkaar
# en liet het teken niet zien of er iets gedownload, ververst of geopend wordt (principes 3, 4 en 5).
# De vormen zijn die van de installer vóór ontwerp E (openaec-installer 8b39bae) en de bekende vormen
# voor downloaden, verversen en extern openen.

def tray(p):
    """Open bakje onderaan: het doel van een download."""
    if p.s == 16:
        p.line([(1.5, 10.5), (1.5, 13.5), (13.5, 13.5), (13.5, 10.5)], r=1.2)
    else:
        p.line([(3, 15), (3, 20), (21, 20), (21, 15)], r=1.6)


@design('software.install', 'Pijl omlaag in een bakje: de bekende vorm voor downloaden, zoals de knoppen van de installer '
                            'vóór ontwerp E. Het venster met een klein pijltje eronder leek op 16 px op Starten en Tab openen.')
def software_install(p):
    tray(p)
    if p.s == 16:
        p.line([(7.5, 1.5), (7.5, 10)], True, r=0)
        p.line([(4.5, 7), (7.5, 10), (10.5, 7)], True, r=0.4)
    else:
        p.line([(12, 3), (12, 15)], True, r=0)
        p.line([(7.5, 10.5), (12, 15), (16.5, 10.5)], True, r=0.6)


def turn_arrow(p, cx, cy, r, start, end, accent=True, head=None):
    """Draaipijl met een grote pijlpunt: de punt moet ook op 16 px te zien zijn, anders leest hij als open cirkel."""
    p.arc(cx, cy, r, start, end, accent)
    a = math.radians(end)
    ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    nx, ny = math.cos(a), math.sin(a)
    w, length = head or ((2.2, 3.0) if p.s == 16 else (3.2, 4.4))
    p.fill([(ex + nx * w, ey + ny * w), (ex + tx * length, ey + ty * length), (ex - nx * w, ey - ny * w)], accent)


@design('software.update', 'Dezelfde pijl omlaag in een bakje als Installeren: bijwerken is de nieuwe versie downloaden en '
                           'installeren (besluit van de gebruiker, 30 oktober 2026). Op een kaart staat altijd maar één van de '
                           'twee; het label zegt welke. Eigen vorm naast Controleren op updates.')
def software_update(p):
    software_install(p)


@design('update.install', 'Zelfde betekenis als software.update (een appupdate installeren), dus hetzelfde icoon (principe 2).')
def update_install(p):
    software_install(p)


@design('ui.check-updates', 'Twee ververspijlen in één kleur: opnieuw ophalen of er updates zijn. Op 16 px bijna 12 x 12 groot, '
                            'met ruimte tussen de pijlen. De draaipijl met een pijltje erin was op 16 px een vlek (principe 3); '
                            'één ding, dus geen oranje. Eigen vorm naast Bijwerken (bakje met pijl) en Webtool herladen (één pijl).')
def check_updates(p):
    if p.s == 16:
        for start, end in ((195, 325), (15, 145)):
            turn_arrow(p, 7.5, 7.5, 5.75, start, end, False, (1.9, 2.6))
    else:
        for start, end in ((195, 325), (15, 145)):
            turn_arrow(p, 12, 12, 7.75, start, end, False, (2.8, 3.8))


@design('view.web-reload', 'Eén cirkelpijl met de punt bovenaan, zoals de herlaadknop in een browser. Geen venster eromheen en '
                           'geen oranje: één ding. Anders dan Controleren op updates, dat twee pijlen heeft.')
def web_reload(p):
    if p.s == 16:
        turn_arrow(p, 7.5, 8, 5.5, -45, 250, False)
    else:
        turn_arrow(p, 12, 12.5, 8, -45, 250, False)


def globe(p):
    """Wereldbol: cirkel, één meridiaan en de evenaar."""
    cx, r, rx = (7.5, 6.4, 2.75) if p.s == 16 else (12, 9.25, 4.25)
    p.circle(cx, cx, r)
    p.line([(cx + rx * math.sin(math.radians(a)), cx - r * math.cos(math.radians(a))) for a in range(0, 361, 10)],
           closed=True, r=0)
    p.line([(cx - r, cx), (cx + r, cx)], r=0)


@design('software.open-webtab', 'Wereldbol: een webtool openen, de bekendste vorm voor web (besluit van de gebruiker, '
                                '30 oktober 2026). Eén ding, dus geen oranje. Eigen vorm naast Extern openen (vierkant met pijl) '
                                'en Installeren (bakje). Het venster met een tab las niet als openen.')
def open_webtab(p):
    globe(p)


@design('link.open-external', 'Vierkant met een oranje pijl schuin naar buiten: de bekende vorm voor openen in de browser '
                              '(external-link), zoals in de installer vóór ontwerp E. De ketting las als koppeling, niet als openen.')
def open_external(p):
    if p.s == 16:
        p.line([(6.5, 4.5), (1.5, 4.5), (1.5, 14.5), (11.5, 14.5), (11.5, 9.5)], r=1.2)
        p.line([(6.5, 9.5), (13, 3)], True, r=0)
        p.line([(10, 2.5), (13.5, 2.5), (13.5, 6)], True, r=0.4)
    else:
        p.line([(10, 6), (3, 6), (3, 21), (18, 21), (18, 14)], r=1.6)
        p.line([(10, 14), (21, 3)], True, r=0)
        p.line([(15, 3), (21, 3), (21, 9)], True, r=0.6)


@design('software.launch', 'Afspeelpijl: een geïnstalleerde app starten, zoals de afspeelknop op de kaart van de installer vóór '
                           'ontwerp E. Dezelfde tekening als solver.run: beide laten iets lopen, en ze komen niet in hetzelfde '
                           'programma voor. Een cirkel eromheen leek op de wereldbol van Openen op dezelfde kaart, en een volle '
                           'driehoek is op 16 px te vol. Eén ding, dus geen oranje.')
def software_launch(p):
    solver_run(p)


def revised_construction(c):
    """Vul een lege Construction met de tekening uit dit bestand."""
    DRAWINGS[c.key](Pen(c))
    return c
