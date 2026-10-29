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

# Een herzien icoon: waarom, en welke kleur bij een aansluiting vóór ligt.
REVISED = {}
DRAWINGS = {}
ACCENT_FRONT = {}

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
]
# Programma's waar de nieuwe betekenis voorkomt. Bij een bestaand id komt dit uit de broncatalogus.
NEW_APPS = {
    'solver.run': ['FEM', 'Planner'],
    'workspace.ribbon-collapse': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
    'workspace.ribbon-expand': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
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


def design(key, reason, accent_front=None):
    def register(fn):
        DRAWINGS[key] = fn
        REVISED[key] = reason
        if accent_front:
            ACCENT_FRONT[key] = accent_front
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


@design('view.zoom-default', 'Hetzelfde vergrootglas als Zoom + en Zoom −, met een oranje punt: de standaardmaat (#52).')
def zoom_default(p):
    m, _ = magnifier(p)
    p.circle(m, m, 1.25 if p.s == 16 else 1.75, True, True)


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


@design('panel.warnings', 'Waarschuwingsdriehoek zoals in Open Planner Studio, zonder paneelkader (#56 a); het uitroepteken in oranje.')
def warnings(p):
    if p.s == 16:
        p.line([(7.5, 1.75), (14.25, 13.5), (0.75, 13.5)], closed=True, r=1.4)
        p.line([(7.5, 6.5), (7.5, 8.25)], True, r=0)
        p.circle(7.5, 10.75, 0.8, True, True)
    else:
        p.line([(12, 3), (22, 20.5), (2, 20.5)], closed=True, r=2)
        p.line([(12, 9.75), (12, 13)], True, r=0)
        p.circle(12, 16.5, 1.1, True, True)


# ---------------------------------------------------------------- groep Relaties

def stadium(p, x0, y0, x1, y1, w, accent=False):
    """Schakel van een ketting: een staaf met ronde einden tussen twee punten, breedte w (hartlijn)."""
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang), math.cos(ang)
    h = w / 2
    pts = []
    for (cx, cy), base in (((x1, y1), ang - math.pi / 2), ((x0, y0), ang + math.pi / 2)):
        for i in range(13):
            t = base + math.pi * i / 12
            pts.append((cx + h * math.cos(t), cy + h * math.sin(t)))
    p.line(pts, accent, True, 0)


@design('planning.relations-menu', 'Ketting zoals Relatie in Open Planner Studio en Taken koppelen in MS Project.')
def relations_menu(p):
    if p.s == 16:
        stadium(p, 3.5, 12.5, 8.5, 7.5, 4.5)
        stadium(p, 7.5, 8.5, 12.5, 3.5, 4.5)
    else:
        stadium(p, 5, 19, 12.5, 11.5, 6.5)
        stadium(p, 11.5, 12.5, 19, 5, 6.5)


@design('task.split-mode', 'Een taakbalk met een schuine knip, zoals Taak splitsen in MS Project; het afgesplitste deel in oranje.')
def split_mode(p):
    if p.s == 16:
        p.line([(1.5, 5.5), (8.5, 5.5), (6.5, 10.5), (1.5, 10.5)], closed=True, r=1.0)
        p.line([(11.5, 5.5), (14.5, 5.5), (14.5, 10.5), (9.5, 10.5)], True, True, r=1.0)
    else:
        p.line([(2, 8), (13, 8), (10, 16), (2, 16)], closed=True, r=1.5)
        p.line([(17, 8), (22, 8), (22, 16), (14, 16)], True, True, r=1.5)


def trace(p, successors):
    if p.s == 16:
        p.line([(2.5, 3), (2.5, 12)], r=0)
        p.line([(14, 7.5), (5.5, 7.5)], True, r=0)
        p.line([(9, 4), (5.5, 7.5), (9, 11)], True, r=0.6)
    else:
        p.line([(3, 5), (3, 19)], r=0)
        p.line([(21, 12), (7.5, 12)], True, r=0)
        p.line([(12.5, 7), (7.5, 12), (12.5, 17)], True, r=0.8)
    if successors:
        p.c.mirror()


@design('planning.trace-predecessors', 'Pijl naar een streep, zoals Voorgangers in Open Planner Studio; de pijl in oranje (#48).')
def trace_pred(p):
    trace(p, False)


@design('planning.trace-successors', 'Gespiegelde pijl naar een streep, zoals Opvolgers in Open Planner Studio (#48).')
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
        p.circle(x + ux * d, y + uy * d, r, True, True)
    return pts


@design('planning.structure', 'Twee etiketten, zoals Codes & velden in Open Planner Studio (#53); het gat in het voorste etiket in oranje.')
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
    """Draaipijl: open cirkel met één pijlpunt aan het eind."""
    pts = p.arc(cx, cy, r, start, end, accent)
    ex, ey = pts[-1]
    a = math.radians(end)
    tx, ty = -math.sin(a), math.cos(a)   # raaklijn in looprichting
    nx, ny = math.cos(a), math.sin(a)    # naar buiten
    k = 1.7 if p.s == 16 else 2.4
    p.line([(ex + nx * k - tx * k * 0.2, ey + ny * k - ty * k * 0.2), (ex, ey), (ex - nx * k - tx * k * 0.2, ey - ny * k - ty * k * 0.2)][::-1],
           accent, r=0.3)


@design('wbs.renumber', 'Hekje met een oranje draaipijl: de nummering opnieuw doen. Geen kleine cijfers 1 en 2, die op 16 px onleesbaar zijn.')
def wbs_renumber(p):
    if p.s == 16:
        p.line([(1.5, 4.5), (10, 4.5)], r=0)
        p.line([(1.5, 9.5), (8.75, 9.5)], r=0)
        p.line([(4.25, 1.5), (3.25, 12.5)], r=0)
        p.line([(8.75, 1.5), (7.85, 11.5)], r=0)
        refresh(p, 12.5, 12.5, 2.25, start=10, end=300)
    else:
        hash_sign(p, 2, 2, 15, 15)
        refresh(p, 18.5, 18.5, 3.5, start=10, end=300)


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

@design('planning.baselines', 'Twee versies met pijlen ertussen, zoals Baselines beheren in Open Planner Studio; de pijlen in oranje.')
def baselines(p):
    if p.s == 16:
        p.circle(3.5, 3.5, 1.75)
        p.circle(12.5, 12.5, 1.75)
        p.line([(7.75, 3.5), (10.5, 3.5), (12.5, 5.5), (12.5, 8)], True, r=1.5)
        p.line([(9.25, 2), (7.75, 3.5), (9.25, 5)], True, r=0.4)
        p.line([(8.25, 12.5), (5.5, 12.5), (3.5, 10.5), (3.5, 8)], True, r=1.5)
        p.line([(6.75, 11), (8.25, 12.5), (6.75, 14)], True, r=0.4)
    else:
        p.circle(5, 5, 2.5)
        p.circle(19, 19, 2.5)
        p.line([(11.5, 5), (16, 5), (19, 8), (19, 12)], True, r=2.2)
        p.line([(14, 2.5), (11.5, 5), (14, 7.5)], True, r=0.6)
        p.line([(12.5, 19), (8, 19), (5, 16), (5, 12)], True, r=2.2)
        p.line([(10, 16.5), (12.5, 19), (10, 21.5)], True, r=0.6)


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
        p.line([(7.5, 1.5), (7.5, 3.5), (12, 6), (7.5, 8.5), (3.5, 11), (7.5, 13), (7.5, 14.5)], r=0.5)
    else:
        p.line([(11, 2), (11, 5), (18, 9), (11, 13), (5, 16.5), (11, 20), (11, 22)], r=0.7)


@design('planning.status-date-line', 'Verticale lijn met een oranje merkteken bovenaan: de statusdatumlijn op de Gantt; geen assenkader.',
        'Het oranje merkteken ligt vóór de lijn, zodat de punt heel blijft.')
def status_date_line(p):
    if p.s == 16:
        p.line([(7.5, 4), (7.5, 14.5)], r=0)
        p.fill([(4, 1.25), (11, 1.25), (7.5, 5.75)], True)
    else:
        p.line([(12, 6), (12, 22)], r=0)
        p.fill([(7, 1.5), (17, 1.5), (12, 8)], True)


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


@design('planning.relations-visible', 'Afhankelijkheidspijl einde-begin zoals op de Gantt: haaks naar beneden en naar rechts, met de punt in oranje.',
        'De oranje pijlpunt ligt vóór de lijn.')
def relations_visible(p):
    if p.s == 16:
        p.line([(1.5, 3.5), (5.5, 3.5), (5.5, 11.5), (12.5, 11.5)], r=1.4)
        p.line([(10, 8.5), (13, 11.5), (10, 14.5)], True, r=0.5)
    else:
        p.line([(2, 5), (8, 5), (8, 17), (19, 17)], r=2)
        p.line([(15.5, 12.5), (20, 17), (15.5, 21.5)], True, r=0.7)


def revised_construction(c):
    """Vul een lege Construction met de tekening uit dit bestand."""
    DRAWINGS[c.key](Pen(c))
    return c

