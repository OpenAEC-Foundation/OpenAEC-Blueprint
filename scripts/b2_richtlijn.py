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
    ('panel.properties', 'Eigenschappenpaneel tonen', 'Vensters en panelen',
     'Het paneel met eigenschappen van de selectie tonen; de knop toont dat het paneel nu zichtbaar is. Tegenhanger van panel.properties-hidden.'),
    ('panel.properties-hidden', 'Eigenschappenpaneel verborgen', 'Vensters en panelen',
     'Het paneel met eigenschappen van de selectie is verborgen; de knop toont het weer. Tegenhanger van panel.properties.'),
    ('panel.expand-full', 'Paneel naar volledige weergave', 'Vensters en panelen',
     'Een compact zijpaneel openen als volledige weergave. Geen volledig scherm van het programma; daarvoor blijft view.fullscreen.'),
    ('capture.mask', 'Gebied maskeren', 'Schermannotaties en logweergave',
     'Een gebied in een schermafbeelding afdekken voordat die wordt gedeeld. Geen redactie in een PDF; daarvoor blijft annotate.redact.'),
    ('ai.read-only-off', 'AI mag schrijven', 'AI-mutaties bedienen',
     'De knop toont dat de alleen-lezenstand van de AI uit staat; een klik zet hem aan. Tegenhanger van ai.read-only-toggle.'),
    ('planning.driving-unknown', 'Bepalende relatie onbekend', 'Planning',
     'Bij een relatie is niet bekend of hij bepalend is, omdat de planning nog niet is doorgerekend. Een toestand, geen opdracht. Naast planning.driving.'),
    ('extension.install-zip', 'Extensie uit ZIP installeren', 'Extensies en hulpfuncties',
     'Een extensiepakket als ZIP-bestand kiezen en installeren. Naast extension.install-js.'),
    ('extension.install-js', 'Extensie uit JS installeren', 'Extensies en hulpfuncties',
     'Een extensie als los JS-bestand kiezen en installeren. Naast extension.install-zip.'),
    ('guide.expand', 'Begeleiding uitgebreid tonen', 'Prestatiemeting en begeleiding',
     'Het begeleidingspaneel van compact naar uitgebreid zetten. Tegenhanger van guide.compact.'),
    ('task.note-add', 'Notitie toevoegen', 'Taken en planningsberekening',
     'Een notitie bij de taak toevoegen. Geen annotatie op een tekening; daarvoor blijft draw.note.'),
    ('panel.schedule-shift', 'Verschuivingenpaneel', 'Vensters en panelen',
     'Het paneel met de taken die bij het doorrekenen verschoven zijn omschakelen, met de reden per taak. Geen taak verplaatsen; daarvoor blijft planning.move-date.'),
    ('list.item-remove', 'Regel weghalen', 'Lijsten en bomen',
     'Eén regel uit een lijst of voorwaarde weghalen met een klein kruisje. Geen object verwijderen; daarvoor blijft edit.delete.'),
]
# Programma's waar de nieuwe betekenis voorkomt. Bij een bestaand id komt dit uit de broncatalogus.
NEW_APPS = {
    'solver.run': ['FEM', 'Planner'],
    'workspace.ribbon-collapse': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
    'workspace.ribbon-expand': ['Calc', 'Energy', 'Geotechniek', 'Heatloss', 'Pile Plan', 'Planner', 'Pointcloud', 'Workspace Composer'],
    'planning.progress-sheet-export': ['Planner'],
    'planning.progress-sheet-import': ['Planner'],
    'panel.properties': ['Planner'],
    'panel.properties-hidden': ['Planner'],
    'panel.expand-full': ['Planner'],
    'capture.mask': ['Planner'],
    'ai.read-only-off': ['Planner'],
    'panel.schedule-shift': ['Planner'],
    'planning.driving-unknown': ['Planner'],
    'extension.install-zip': ['Planner'],
    'extension.install-js': ['Planner'],
    'guide.expand': ['Planner'],
    'task.note-add': ['Planner'],
    'list.item-remove': ['Planner'],
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
        p.line([(12, 3), (22, 20), (2, 20)], closed=True, r=2)
        p.line([(12, 9.5), (12, 12.5)], r=0)
        p.circle(12, 16.25, 1.1, filled=True)


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
        p.line([(3.5, 2.5), (6, 1.75), (9, 3), (13.5, 2.25), (13.5, 9.25), (9, 10), (6, 8.75), (3.5, 9.5)], closed=False, r=1.2)
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
        for start, end in ((200, 315), (20, 135)):
            turn_arrow(p, 7.5, 7.5, 5.5, start, end, False, (2.5, 3.2))
    else:
        for start, end in ((200, 315), (20, 135)):
            turn_arrow(p, 12, 12, 8.5, start, end, False, (3.4, 4.6))


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


# ---------------------------------------------------------------- overige iconen van Open Planner Studio
# Derde ronde (31 oktober 2026, besluit van Ethan: "iconen door met de rest"). De koppeling per plek komt uit
# OPS #566 van nino2-aec; de vorm komt uit Open Planner Studio op main (Lucide), opnieuw getekend in de lijnstijl.
# Een vorm die in main op veel plekken staat (de plus, het kruis, de prullenbak), is hier één tekening met
# meerdere ids. De tabel VORMEN onderaan koppelt tekening, reden en ids.

def plus(p):
    if p.s == 16:
        p.line([(7.5, 2.5), (7.5, 12.5)], r=0)
        p.line([(2.5, 7.5), (12.5, 7.5)], r=0)
    else:
        p.line([(12, 4), (12, 20)], r=0)
        p.line([(4, 12), (20, 12)], r=0)


def cross(p):
    if p.s == 16:
        p.line([(3.5, 3.5), (12.5, 12.5)], r=0)
        p.line([(12.5, 3.5), (3.5, 12.5)], r=0)
    else:
        p.line([(5, 5), (19, 19)], r=0)
        p.line([(19, 5), (5, 19)], r=0)


def minus(p):
    p.line([(2.5, 7.5), (12.5, 7.5)] if p.s == 16 else [(4, 12), (20, 12)], r=0)


def check(p):
    if p.s == 16:
        p.line([(2.5, 8.5), (6.5, 12.5), (13.5, 5.5)], r=0.4)
    else:
        p.line([(4, 12.5), (9.5, 18), (20.5, 7)], r=0.6)


CHEVRONS = {16: {'right': [(5.5, 2.5), (10.5, 7.5), (5.5, 12.5)], 'left': [(10.5, 2.5), (5.5, 7.5), (10.5, 12.5)],
                 'down': [(2.5, 5.5), (7.5, 10.5), (12.5, 5.5)], 'up': [(2.5, 10.5), (7.5, 5.5), (12.5, 10.5)]},
            24: {'right': [(9, 5), (16, 12), (9, 19)], 'left': [(15, 5), (8, 12), (15, 19)],
                 'down': [(5, 9), (12, 16), (19, 9)], 'up': [(5, 15), (12, 8), (19, 15)]}}


def chevron(p, direction):
    p.line(CHEVRONS[p.s][direction], r=0.5 if p.s == 16 else 0.7)


def chevron_right(p):
    chevron(p, 'right')


def chevron_left(p):
    chevron(p, 'left')


def chevron_down(p):
    chevron(p, 'down')


def chevron_up(p):
    chevron(p, 'up')


def dropdown(p):
    p.line([(3.5, 5.5), (7.5, 9.5), (11.5, 5.5)] if p.s == 16 else [(6, 9), (12, 15), (18, 9)], r=0.4 if p.s == 16 else 0.6)


def chevrons_in(p):
    """Twee punthaken naar elkaar toe, zoals Alles inklappen in Open Planner Studio."""
    if p.s == 16:
        p.line([(3.5, 2.5), (7.5, 6.5), (11.5, 2.5)], r=0.4)
        p.line([(3.5, 13.5), (7.5, 9.5), (11.5, 13.5)], r=0.4)
    else:
        p.line([(6, 3.5), (12, 9.5), (18, 3.5)], r=0.6)
        p.line([(6, 20.5), (12, 14.5), (18, 20.5)], r=0.6)


def chevrons_out(p):
    """Twee punthaken van elkaar af, zoals Alles uitklappen in Open Planner Studio."""
    if p.s == 16:
        p.line([(3.5, 6.5), (7.5, 2.5), (11.5, 6.5)], r=0.4)
        p.line([(3.5, 9.5), (7.5, 13.5), (11.5, 9.5)], r=0.4)
    else:
        p.line([(6, 9.5), (12, 3.5), (18, 9.5)], r=0.6)
        p.line([(6, 14.5), (12, 20.5), (18, 14.5)], r=0.6)


def arrow(p, direction):
    if p.s == 16:
        shaft = {'left': [(13.5, 7.5), (2.5, 7.5)], 'right': [(2.5, 7.5), (13.5, 7.5)],
                 'up': [(7.5, 13.5), (7.5, 2.5)], 'down': [(7.5, 2.5), (7.5, 13.5)]}[direction]
        head = {'left': [(6.5, 3.5), (2.5, 7.5), (6.5, 11.5)], 'right': [(9.5, 3.5), (13.5, 7.5), (9.5, 11.5)],
                'up': [(3.5, 6.5), (7.5, 2.5), (11.5, 6.5)], 'down': [(3.5, 9.5), (7.5, 13.5), (11.5, 9.5)]}[direction]
        radius = 0.4
    else:
        shaft = {'left': [(21, 12), (3, 12)], 'right': [(3, 12), (21, 12)],
                 'up': [(12, 21), (12, 3)], 'down': [(12, 3), (12, 21)]}[direction]
        head = {'left': [(9, 6), (3, 12), (9, 18)], 'right': [(15, 6), (21, 12), (15, 18)],
                'up': [(6, 9), (12, 3), (18, 9)], 'down': [(6, 15), (12, 21), (18, 15)]}[direction]
        radius = 0.6
    p.line(shaft, r=0)
    p.line(head, r=radius)


def arrow_left(p):
    arrow(p, 'left')


def arrow_right(p):
    arrow(p, 'right')


def arrow_up(p):
    arrow(p, 'up')


def arrow_down(p):
    arrow(p, 'down')


def arrow_diagonal(p):
    if p.s == 16:
        p.line([(3.5, 12.5), (12.5, 3.5)], r=0)
        p.line([(9.5, 3.5), (12.5, 3.5), (12.5, 6.5)], r=0.6)
    else:
        p.line([(5, 19), (19, 5)], r=0)
        p.line([(8, 5), (19, 5), (19, 16)], r=0.6)


def arrows_sort(p):
    if p.s == 16:
        p.line([(4.5, 13.5), (4.5, 2.5)], r=0)
        p.line([(1.5, 5.5), (4.5, 2.5), (7.5, 5.5)], r=0.4)
        p.line([(11.5, 2.5), (11.5, 13.5)], r=0)
        p.line([(8.5, 10.5), (11.5, 13.5), (14.5, 10.5)], r=0.4)
    else:
        p.line([(7, 21), (7, 3)], r=0)
        p.line([(3, 7), (7, 3), (11, 7)], r=0.6)
        p.line([(17, 3), (17, 21)], r=0)
        p.line([(13, 17), (17, 21), (21, 17)], r=0.6)


def arrow_from_line(p):
    """Lijn met een oranje pijl omhoog, zoals In bibliotheek opnemen in Open Planner Studio; de hele pijl in één kleur."""
    if p.s == 16:
        p.line([(2.5, 13.5), (12.5, 13.5)], r=0)
        p.line([(7.5, 10.5), (7.5, 2.5)], True, r=0)
        p.line([(3.5, 6.5), (7.5, 2.5), (11.5, 6.5)], True, r=0.4)
    else:
        p.line([(4, 21), (20, 21)], r=0)
        p.line([(12, 17), (12, 3)], True, r=0)
        p.line([(6, 9), (12, 3), (18, 9)], True, r=0.6)


def undo(p):
    if p.s == 16:
        p.line([(2.5, 6.5), (13.5, 6.5), (13.5, 13.5), (6.5, 13.5)], r=3.4)
        p.line([(5.5, 3.5), (2.5, 6.5), (5.5, 9.5)], r=0.4)
    else:
        p.line([(3, 9), (21, 9), (21, 20), (10, 20)], r=5.4)
        p.line([(8, 4), (3, 9), (8, 14)], r=0.6)


def redo(p):
    undo(p)
    p.c.mirror()


def turn_back(p):
    """Draaipijl tegen de klok in, zoals Terugzetten en Herstellen in Open Planner Studio."""
    if p.s == 16:
        turn_arrow(p, 7.5, 8, 5.5, 10, 285, False, (2.7, 3.4))
    else:
        turn_arrow(p, 12, 12.5, 8, 10, 285, False, (3.8, 5))
    p.c.mirror()
    for f in p.c.fills:
        f['rings'] = [[(p.s - x, y) for x, y in ring] for ring in f['rings']]


def page(p):
    """Blad met een schuine hoek; op 24 px ook omgevouwen. Binnen het blad blijft ruimte voor een teken."""
    if p.s == 16:
        p.line([(2.5, 1.5), (9.5, 1.5), (12.5, 4.5), (12.5, 14.5), (2.5, 14.5)], closed=True, r=1.0)
    else:
        p.line([(4, 2), (15, 2), (20, 7), (20, 22), (4, 22)], closed=True, r=1.6)
        p.line([(15, 2), (15, 7), (20, 7)], r=0.7)


def page_new(p):
    page(p)
    if p.s == 16:
        p.line([(7.5, 7.5), (7.5, 11.5)], True, r=0)
        p.line([(5.5, 9.5), (9.5, 9.5)], True, r=0)
    else:
        p.line([(12, 11), (12, 18)], True, r=0)
        p.line([(8.5, 14.5), (15.5, 14.5)], True, r=0)


def page_lines(p):
    page(p)
    if p.s == 16:
        p.line([(5.5, 8.5), (9.5, 8.5)], r=0)
        p.line([(5.5, 11.5), (9.5, 11.5)], r=0)
    else:
        p.line([(8, 12), (16, 12)], r=0)
        p.line([(8, 17), (16, 17)], r=0)


def page_letter(p):
    """Blad met een hoofdletter T, zoals de bestandsaanduiding in Open Planner Studio."""
    page(p)
    if p.s == 16:
        p.line([(5, 6.5), (10, 6.5)], r=0)
        p.line([(7.5, 6.5), (7.5, 11.5)], r=0)
    else:
        p.line([(8, 11), (16, 11)], r=0)
        p.line([(12, 11), (12, 18)], r=0)


def page_zip(p):
    """Blad met een rits: streepjes en een ring, zoals FileArchive in Open Planner Studio."""
    page(p)
    if p.s == 16:
        p.line([(7.5, 3.75), (7.5, 4.5)], r=0)
        p.line([(7.5, 6.75), (7.5, 7.5)], r=0)
        p.circle(7.5, 11, 1.25)
    else:
        p.line([(10, 6.5), (10, 7.5)], r=0)
        p.line([(10, 11), (10, 12)], r=0)
        p.circle(10, 18, 2.75)


def page_code(p):
    page(p)
    if p.s == 16:
        p.line([(6, 7.5), (5, 9.5), (6, 11.5)], r=0.3)
        p.line([(9, 7.5), (10, 9.5), (9, 11.5)], r=0.3)
    else:
        p.line([(10, 11.5), (7.5, 15), (10, 18.5)], r=0.5)
        p.line([(14, 11.5), (16.5, 15), (14, 18.5)], r=0.5)


def floppy(p):
    if p.s == 16:
        p.line([(1.5, 1.5), (11.5, 1.5), (14.5, 4.5), (14.5, 14.5), (1.5, 14.5)], closed=True, r=1.2)
        p.line([(4.5, 14.5), (4.5, 9.5), (11.5, 9.5), (11.5, 14.5)], r=0.5)
        p.line([(4.5, 1.5), (4.5, 4.5), (9.5, 4.5)], r=0.5)
    else:
        p.line([(3, 3), (17, 3), (21, 7), (21, 21), (3, 21)], closed=True, r=1.6)
        p.line([(7, 21), (7, 14), (17, 14), (17, 21)], r=0.7)
        p.line([(7, 3), (7, 8), (15, 8)], r=0.7)


def floppy_copy(p):
    """Diskette met in oranje de hoek van een tweede exemplaar, zoals Opslaan als in Open Planner Studio."""
    if p.s == 16:
        p.line([(1.5, 1.5), (9.5, 1.5), (11.5, 3.5), (11.5, 11.5), (1.5, 11.5)], closed=True, r=1.2)
        p.line([(3.5, 11.5), (3.5, 9), (9.5, 9), (9.5, 11.5)], r=0.3)
        p.line([(4.5, 1.5), (4.5, 4), (7.5, 4)], r=0.3)
        p.line([(14.5, 6.5), (14.5, 14.5), (6.5, 14.5)], True, r=1.2)
    else:
        p.line([(3, 3), (14, 3), (17, 6), (17, 17), (3, 17)], closed=True, r=1.6)
        p.line([(7, 17), (7, 11), (13, 11), (13, 17)], r=0.7)
        p.line([(7, 3), (7, 7), (12, 7)], r=0.6)
        p.line([(21, 8), (21, 21), (8, 21)], True, r=1.6)


def folder_open(p):
    if p.s == 16:
        p.line([(12.5, 6.5), (12.5, 4.5), (8, 4.5), (6.5, 2.5), (1.5, 2.5), (1.5, 13.5)], r=1.2)
        p.line([(1.5, 13.5), (3.5, 7.5), (14.5, 7.5), (12.5, 13.5)], closed=True, r=0.9)
    else:
        p.line([(18, 9), (18, 7), (11.5, 7), (9.5, 4), (3, 4), (3, 20)], r=1.6)
        p.line([(3, 20), (6, 11), (22, 11), (19, 20)], closed=True, r=1.2)


def hard_drive(p):
    if p.s == 16:
        p.rect(1.5, 8.5, 14.5, 13.5, r=1.2)
        p.line([(1.5, 8.5), (4, 3.5), (12, 3.5), (14.5, 8.5)], r=0.8)
        p.circle(4.5, 11, 0.85, filled=True)
    else:
        p.rect(3, 13, 21, 20, r=1.6)
        p.line([(3, 13), (6.5, 5), (17.5, 5), (21, 13)], r=1.1)
        p.circle(7, 16.5, 1.1, filled=True)


def printer(p):
    if p.s == 16:
        p.line([(4.5, 5.5), (4.5, 1.5), (11.5, 1.5), (11.5, 5.5)], r=0.8)
        p.line([(4.5, 11.5), (1.5, 11.5), (1.5, 5.5), (14.5, 5.5), (14.5, 11.5), (11.5, 11.5)], r=1.2)
        p.rect(4.5, 9.5, 11.5, 14.5, r=0.5)
    else:
        p.line([(7, 8), (7, 3), (17, 3), (17, 8)], r=1.1)
        p.line([(7, 17), (3, 17), (3, 8), (21, 8), (21, 17), (17, 17)], r=1.6)
        p.rect(7, 14, 17, 21, r=0.7)


def tray_arrow_up(p):
    """Bakje met een oranje pijl omhoog: gegevens gaan het programma uit. De tegenhanger is software_install."""
    tray(p)
    if p.s == 16:
        p.line([(7.5, 10), (7.5, 1.5)], True, r=0)
        p.line([(4.5, 4.5), (7.5, 1.5), (10.5, 4.5)], True, r=0.4)
    else:
        p.line([(12, 15), (12, 3)], True, r=0)
        p.line([(7.5, 7.5), (12, 3), (16.5, 7.5)], True, r=0.6)


def book_open(p):
    if p.s == 16:
        p.line([(7.5, 4), (5.5, 2.5), (1.5, 2.5), (1.5, 12.5), (5.5, 12.5), (7.5, 13.5)], r=0.8)
        p.line([(7.5, 4), (9.5, 2.5), (13.5, 2.5), (13.5, 12.5), (9.5, 12.5), (7.5, 13.5)], r=0.8)
        p.line([(7.5, 4), (7.5, 13.5)], r=0)
    else:
        p.line([(12, 6), (9, 4), (3, 4), (3, 19), (9, 19), (12, 20.5)], r=1.1)
        p.line([(12, 6), (15, 4), (21, 4), (21, 19), (15, 19), (12, 20.5)], r=1.1)
        p.line([(12, 6), (12, 20.5)], r=0)


def building(p):
    """Toren met een lagere vleugel en ramen, zoals Bedrijfsbibliotheek in Open Planner Studio (Building2)."""
    if p.s == 16:
        p.line([(1.5, 14.5), (1.5, 2.5), (8.5, 1.5), (8.5, 14.5)], closed=True, r=0.7)
        p.line([(8.5, 7.5), (14.5, 7.5), (14.5, 14.5), (8.5, 14.5)], r=0.7)
        p.line([(4.5, 5.5), (5.5, 5.5)], r=0)
        p.line([(4.5, 8.5), (5.5, 8.5)], r=0)
        p.line([(4.5, 11.5), (5.5, 11.5)], r=0)
    else:
        p.line([(3, 22), (3, 3), (14, 2), (14, 22)], closed=True, r=1)
        p.line([(14, 9), (21, 9), (21, 22), (14, 22)], r=1)
        p.line([(7, 7), (10, 7)], r=0)
        p.line([(7, 12), (10, 12)], r=0)
        p.line([(7, 17), (10, 17)], r=0)


def books(p):
    if p.s == 16:
        p.line([(2.5, 2.5), (2.5, 13.5)], r=0)
        p.line([(6.5, 2.5), (6.5, 13.5)], r=0)
        p.line([(10, 2.5), (13.5, 13.5)], r=0)
    else:
        p.line([(4, 3), (4, 21)], r=0)
        p.line([(10, 3), (10, 21)], r=0)
        p.line([(15, 3), (20.5, 21)], r=0)


def copy_sheets(p):
    if p.s == 16:
        p.rect(5.5, 5.5, 14.5, 14.5, r=1.4)
        p.line([(1.5, 10.5), (1.5, 1.5), (10.5, 1.5)], r=1.4)
    else:
        p.rect(8, 8, 21, 21, r=2)
        p.line([(3, 16), (3, 3), (16, 3)], r=2)


def trash(p):
    if p.s == 16:
        p.line([(1.5, 4.5), (13.5, 4.5)], r=0)
        p.line([(4.5, 4.5), (4.5, 1.5), (10.5, 1.5), (10.5, 4.5)], r=0.4)
        p.line([(2.5, 4.5), (2.5, 14.5), (12.5, 14.5), (12.5, 4.5)], r=1.2)
        p.line([(5.5, 7.5), (5.5, 11.5)], r=0)
        p.line([(9.5, 7.5), (9.5, 11.5)], r=0)
    else:
        p.line([(2, 6), (22, 6)], r=0)
        p.line([(8, 6), (8, 3), (16, 3), (16, 6)], r=0.7)
        p.line([(5, 6), (5, 22), (19, 22), (19, 6)], r=1.6)
        p.line([(10, 11), (10, 17)], r=0)
        p.line([(14, 11), (14, 17)], r=0)


def pen_body(p):
    if p.s == 16:
        p.line([(1.5, 14.5), (2.5, 10.5), (10.5, 2.5), (13.5, 5.5), (5.5, 13.5)], closed=True, r=0.5)
    else:
        p.line([(2.5, 21.5), (4, 15), (16, 3), (21, 8), (9, 20)], closed=True, r=0.7)


def pencil(p):
    pen_body(p)
    if p.s == 16:
        p.line([(8.5, 4.5), (11.5, 7.5)], r=0)
    else:
        p.line([(13, 6), (18, 11)], r=0)


def letter_t(p):
    if p.s == 16:
        p.line([(2.5, 2.5), (12.5, 2.5)], r=0)
        p.line([(7.5, 2.5), (7.5, 13.5)], r=0)
        p.line([(5.5, 13.5), (9.5, 13.5)], r=0)
    else:
        p.line([(4, 4), (20, 4)], r=0)
        p.line([(12, 4), (12, 20)], r=0)
        p.line([(9, 20), (15, 20)], r=0)


def rectangle(p):
    if p.s == 16:
        p.rect(1.5, 3.5, 14.5, 12.5, r=1.2)
    else:
        p.rect(3, 5, 21, 19, r=1.6)


def square(p):
    if p.s == 16:
        p.rect(2.5, 2.5, 12.5, 12.5, r=1.2)
    else:
        p.rect(4, 4, 20, 20, r=1.6)


def arrows_both_ways(p):
    """Twee pijlen in tegengestelde richting, zoals Verschuivingen in Open Planner Studio."""
    if p.s == 16:
        p.line([(4.5, 1.5), (1.5, 4.5), (4.5, 7.5)], r=0.3)
        p.line([(1.5, 4.5), (14.5, 4.5)], r=0)
        p.line([(11.5, 8.5), (14.5, 11.5), (11.5, 14.5)], r=0.3)
        p.line([(14.5, 11.5), (1.5, 11.5)], r=0)
    else:
        p.line([(7, 3), (3, 7), (7, 11)], r=0.5)
        p.line([(3, 7), (21, 7)], r=0)
        p.line([(17, 13), (21, 17), (17, 21)], r=0.5)
        p.line([(21, 17), (3, 17)], r=0)


def stop_square(p):
    if p.s == 16:
        p.rect(1.5, 1.5, 13.5, 13.5, r=1.4)
    else:
        p.rect(3, 3, 21, 21, r=2)


def play(p):
    """Afspeelpijl die het vak vult, zoals Starten en Hervatten in Open Planner Studio."""
    if p.s == 16:
        p.line([(3.5, 1.5), (14, 7.5), (3.5, 13.5)], closed=True, r=1.2)
    else:
        p.line([(5, 3), (21.5, 12), (5, 21)], closed=True, r=1.8)


def corners(p):
    if p.s == 16:
        p.line([(1.5, 5.5), (1.5, 1.5), (5.5, 1.5)], r=0.9)
        p.line([(10.5, 1.5), (14.5, 1.5), (14.5, 5.5)], r=0.9)
        p.line([(14.5, 10.5), (14.5, 14.5), (10.5, 14.5)], r=0.9)
        p.line([(5.5, 14.5), (1.5, 14.5), (1.5, 10.5)], r=0.9)
    else:
        p.line([(3, 8), (3, 3), (8, 3)], r=1.2)
        p.line([(16, 3), (21, 3), (21, 8)], r=1.2)
        p.line([(21, 16), (21, 21), (16, 21)], r=1.2)
        p.line([(8, 21), (3, 21), (3, 16)], r=1.2)


def arrows_out(p):
    if p.s == 16:
        p.line([(13.5, 2.5), (9.5, 6.5)], r=0)
        p.line([(10.5, 2.5), (13.5, 2.5), (13.5, 5.5)], r=0.4)
        p.line([(2.5, 13.5), (6.5, 9.5)], r=0)
        p.line([(2.5, 10.5), (2.5, 13.5), (5.5, 13.5)], r=0.4)
    else:
        p.line([(21, 3), (14, 10)], r=0)
        p.line([(15, 3), (21, 3), (21, 9)], r=0.6)
        p.line([(3, 21), (10, 14)], r=0)
        p.line([(3, 15), (3, 21), (9, 21)], r=0.6)


def arrows_in(p):
    if p.s == 16:
        p.line([(13.5, 2.5), (9.5, 6.5)], r=0)
        p.line([(9.5, 3.5), (9.5, 6.5), (12.5, 6.5)], r=0.4)
        p.line([(2.5, 13.5), (6.5, 9.5)], r=0)
        p.line([(3.5, 9.5), (6.5, 9.5), (6.5, 12.5)], r=0.4)
    else:
        p.line([(21, 3), (14, 10)], r=0)
        p.line([(14, 4), (14, 10), (20, 10)], r=0.6)
        p.line([(3, 21), (10, 14)], r=0)
        p.line([(4, 14), (10, 14), (10, 20)], r=0.6)


def panel_right(p):
    if p.s == 16:
        p.rect(1.5, 2.5, 14.5, 13.5, r=1.4)
        p.line([(9.5, 2.5), (9.5, 13.5)], r=0)
    else:
        p.rect(3, 4, 21, 20, r=2)
        p.line([(15, 4), (15, 20)], r=0)


def split_view(p):
    if p.s == 16:
        p.line([(4.5, 2.5), (1.5, 2.5), (1.5, 13.5), (4.5, 13.5)], r=1.2)
        p.line([(10.5, 2.5), (13.5, 2.5), (13.5, 13.5), (10.5, 13.5)], r=1.2)
        p.line([(7.5, 1.5), (7.5, 14.5)], r=0)
    else:
        p.line([(8, 4), (3, 4), (3, 20), (8, 20)], r=1.6)
        p.line([(16, 4), (21, 4), (21, 20), (16, 20)], r=1.6)
        p.line([(12, 2), (12, 22)], r=0)


def folded_map(p):
    if p.s == 16:
        p.line([(1.5, 3.5), (5.5, 1.5), (10.5, 3.5), (14.5, 1.5), (14.5, 12.5), (10.5, 14.5), (5.5, 12.5), (1.5, 14.5)],
               closed=True, r=0.6)
        p.line([(5.5, 1.5), (5.5, 12.5)], r=0)
        p.line([(10.5, 3.5), (10.5, 14.5)], r=0)
    else:
        p.line([(3, 6), (9, 3), (15, 6), (21, 3), (21, 18), (15, 21), (9, 18), (3, 21)], closed=True, r=0.8)
        p.line([(9, 3), (9, 18)], r=0)
        p.line([(15, 6), (15, 21)], r=0)


def grid_four(p):
    if p.s == 16:
        for x0, y0 in ((1.5, 1.5), (9.5, 1.5), (1.5, 9.5), (9.5, 9.5)):
            p.rect(x0, y0, x0 + 5, y0 + 5, r=1.6)
    else:
        for x0, y0 in ((3, 3), (14, 3), (3, 14), (14, 14)):
            p.rect(x0, y0, x0 + 7, y0 + 7, r=1.2)


def columns(p):
    if p.s == 16:
        p.rect(1.5, 2.5, 14.5, 13.5, r=1.4)
        p.line([(5.5, 2.5), (5.5, 13.5)], r=0)
        p.line([(10.5, 2.5), (10.5, 13.5)], r=0)
    else:
        p.rect(3, 4, 21, 20, r=2)
        p.line([(9, 4), (9, 20)], r=0)
        p.line([(15, 4), (15, 20)], r=0)


def gantt_bars(p):
    if p.s == 16:
        p.line([(1.5, 4.5), (8.5, 4.5)], r=0)
        p.line([(4.5, 8.5), (11.5, 8.5)], r=0)
        p.line([(7.5, 12.5), (14.5, 12.5)], r=0)
    else:
        p.line([(2, 5), (12, 5)], r=0)
        p.line([(7, 12), (17, 12)], r=0)
        p.line([(12, 19), (22, 19)], r=0)


def list_tree(p):
    if p.s == 16:
        p.line([(1.5, 2.5), (14.5, 2.5)], r=0)
        p.line([(3.5, 2.5), (3.5, 12.5), (6.5, 12.5)], r=1.0)
        p.line([(3.5, 7.5), (6.5, 7.5)], r=0)
        p.line([(9.5, 7.5), (14.5, 7.5)], r=0)
        p.line([(9.5, 12.5), (14.5, 12.5)], r=0)
    else:
        p.line([(2, 4), (22, 4)], r=0)
        p.line([(5, 4), (5, 19), (10, 19)], r=1.4)
        p.line([(5, 12), (10, 12)], r=0)
        p.line([(14, 12), (22, 12)], r=0)
        p.line([(14, 19), (22, 19)], r=0)


def layers(p):
    if p.s == 16:
        p.line([(8, 1.5), (14.5, 5), (8, 8.5), (1.5, 5)], closed=True, r=0.6)
        p.line([(1.5, 9), (8, 12.5), (14.5, 9)], r=0.6)
    else:
        p.line([(12, 2), (22, 7.5), (12, 13), (2, 7.5)], closed=True, r=0.8)
        p.line([(2, 12), (12, 17.5), (22, 12)], r=0.8)
        p.line([(2, 16.5), (12, 22), (22, 16.5)], r=0.8)


def funnel(p):
    if p.s == 16:
        p.line([(1.5, 2.5), (14.5, 2.5), (9.5, 8.5), (9.5, 14.5), (6.5, 12.5), (6.5, 8.5)], closed=True, r=0.7)
    else:
        p.line([(2, 3), (22, 3), (14, 12.5), (14, 21.5), (10, 19), (10, 12.5)], closed=True, r=1.0)


def ring(p):
    if p.s == 16:
        p.circle(7.5, 7.5, 6)
    else:
        p.circle(12, 12, 9)


def ring_dot(p):
    ring(p)
    if p.s == 16:
        p.circle(7.5, 7.5, 1.75, filled=True)
    else:
        p.circle(12, 12, 2.75, filled=True)


def status_success(p):
    ring(p)
    if p.s == 16:
        p.line([(4.5, 7.5), (6.5, 9.5), (10.5, 5.5)], r=0.3)
    else:
        p.line([(7.5, 12), (10.5, 15), (16.5, 9)], r=0.5)


def exclamation(p):
    if p.s == 16:
        p.line([(7.5, 4.5), (7.5, 8)], r=0)
        p.circle(7.5, 10.5, 0.8, filled=True)
    else:
        p.line([(12, 7.5), (12, 13)], r=0)
        p.circle(12, 16.75, 1.15, filled=True)


def status_alert(p):
    ring(p)
    exclamation(p)


def status_error(p):
    if p.s == 16:
        p.line([(4.5, 1.5), (10.5, 1.5), (13.5, 4.5), (13.5, 10.5), (10.5, 13.5), (4.5, 13.5), (1.5, 10.5), (1.5, 4.5)],
               closed=True, r=0.6)
    else:
        p.line([(8, 3), (16, 3), (21, 8), (21, 16), (16, 21), (8, 21), (3, 16), (3, 8)], closed=True, r=0.8)
    exclamation(p)


def status_info(p):
    ring(p)
    if p.s == 16:
        p.circle(7.5, 4.75, 0.8, filled=True)
        p.line([(7.5, 7.5), (7.5, 10.5)], r=0)
    else:
        p.circle(12, 7.75, 1.15, filled=True)
        p.line([(12, 11.5), (12, 16.5)], r=0)


def question(p):
    ring(p)
    cx, cy, r, stem = (7.5, 5.75, 1.75, 8.25) if p.s == 16 else (12, 9.25, 2.75, 13.5)
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(190, 401, 15)]
    p.line(pts + [(cx, stem)], r=0)
    if p.s == 16:
        p.circle(7.5, 10.75, 0.8, filled=True)
    else:
        p.circle(12, 17, 1.1, filled=True)


def history(p):
    """Klok, zoals Recent in Open Planner Studio. Een extra draaipijl maakte de wijzers op 16 px vaag."""
    if p.s == 16:
        p.circle(8, 8, 6.5)
        p.line([(8, 4.5), (8, 8), (10.5, 9.5)], r=0.3)
    else:
        p.circle(12, 12, 9.5)
        p.line([(12, 6.5), (12, 12), (16, 14)], r=0.5)


def compass(p):
    ring(p)
    if p.s == 16:
        p.fill([(10, 5), (8.5, 8.5), (5, 10), (6.5, 6.5)])
    else:
        p.fill([(16, 8), (13.5, 13.5), (8, 16), (10.5, 10.5)])


def star(p):
    cx, cy, big, small = (7.5, 8, 6.75, 3) if p.s == 16 else (12, 12.5, 10.25, 4.5)
    pts = [(cx + (big if i % 2 == 0 else small) * math.cos(math.radians(-90 + 36 * i)),
            cy + (big if i % 2 == 0 else small) * math.sin(math.radians(-90 + 36 * i))) for i in range(10)]
    p.line(pts, closed=True, r=0.4 if p.s == 16 else 0.6)


def lock_body(p):
    if p.s == 16:
        p.rect(1.5, 7.5, 13.5, 14.5, r=1.4)
    else:
        p.rect(3, 11, 21, 22, r=2)


def lock(p):
    lock_body(p)
    if p.s == 16:
        p.line([(4.5, 7.5), (4.5, 1.5), (10.5, 1.5), (10.5, 7.5)], r=2.9)
    else:
        p.line([(7.5, 11), (7.5, 2), (16.5, 2), (16.5, 11)], r=4.4)


def lock_open(p):
    lock_body(p)
    if p.s == 16:
        p.line([(4.5, 7.5), (4.5, 1.5), (10.5, 1.5), (10.5, 3)], r=2.9)
    else:
        p.line([(7.5, 11), (7.5, 2), (16.5, 2), (16.5, 4.5)], r=4.4)


def link_chain(p, middle=True):
    """Twee ronde schakels; de einden zijn halve cirkels, anders leest de vorm als twee haken."""
    cy, r, left, right, tip = (7.5, 3, 4.5, 10.5, 6 if middle else 5.5) if p.s == 16 else (12, 5, 7, 17, 10 if middle else 8.5)
    bend = lambda cx, angles: [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in angles]
    p.line([(tip, cy - r)] + bend(left, range(270, 89, -15)) + [(tip, cy + r)], r=0)
    other = left + right - tip
    p.line([(other, cy - r)] + bend(right, range(-90, 91, 15)) + [(other, cy + r)], r=0)
    if middle:
        p.line([(5.5, 7.5), (9.5, 7.5)] if p.s == 16 else [(8, 12), (16, 12)], r=0)


def unlink_chain(p):
    link_chain(p, False)


def zap(p):
    if p.s == 16:
        p.line([(8.5, 1.5), (3, 9), (7.5, 9), (6.5, 14.5), (12.5, 6.5), (8, 6.5)], closed=True, r=0.3)
    else:
        p.line([(13, 2), (4, 14), (11, 14), (10, 22), (20, 10), (13, 10)], closed=True, r=0.5)


def plug(p):
    if p.s == 16:
        p.line([(5.5, 1.5), (5.5, 5.5)], r=0)
        p.line([(9.5, 1.5), (9.5, 5.5)], r=0)
        p.line([(3.5, 5.5), (11.5, 5.5), (11.5, 8), (9, 10.5), (6, 10.5), (3.5, 8)], closed=True, r=1.0)
        p.line([(7.5, 10.5), (7.5, 14.5)], r=0)
    else:
        p.line([(9, 2), (9, 8)], r=0)
        p.line([(15, 2), (15, 8)], r=0)
        p.line([(5, 8), (19, 8), (19, 12), (15, 16), (9, 16), (5, 12)], closed=True, r=1.4)
        p.line([(12, 16), (12, 22)], r=0)


def pause(p):
    if p.s == 16:
        p.rect(2.5, 1.5, 5.5, 13.5, r=0.7)
        p.rect(9.5, 1.5, 12.5, 13.5, r=0.7)
    else:
        p.rect(5, 3, 10, 21, r=1.1)
        p.rect(14, 3, 19, 21, r=1.1)


def cylinder_turn(p):
    """Database met een oranje draaipijl, zoals Automatische back-up in Open Planner Studio."""
    cx, cy, rx, ry, side, low = (6.5, 3.5, 5, 2, 6, 11.5) if p.s == 16 else (10, 5, 8, 3, 9, 18)
    ellipse = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(0, 360, 15)]
    p.line(ellipse, closed=True, r=0)
    p.line([(cx - rx, cy), (cx - rx, low)] + [(cx + rx * math.cos(math.radians(a)), low + ry * math.sin(math.radians(a)))
                                              for a in range(165, 84, -15)], r=0)
    p.line([(cx + rx, cy), (cx + rx, side)], r=0)
    if p.s == 16:
        turn_arrow(p, 11.5, 11.5, 3, -70, 195, True, (1.9, 2.5))
    else:
        turn_arrow(p, 17.25, 17.25, 4.75, -70, 195, True, (2.8, 3.7))


def lens(p):
    cx, w, h = (7.5, 6.5, 4.5) if p.s == 16 else (12, 10.5, 7)
    top = [(cx + w * t / 10, cx - h * (1 - (t / 10) ** 2)) for t in range(-10, 11)]
    p.line(top + [(x, 2 * cx - y) for x, y in reversed(top[1:-1])], closed=True, r=0)
    return cx


def eye(p):
    cx = lens(p)
    p.circle(cx, cx, 2 if p.s == 16 else 3.25)


def eye_off(p):
    """Oog zonder iris met een streep erdoor: met iris loopt de streep op 16 px dicht."""
    lens(p)
    p.line([(2.5, 1.5), (12.5, 13.5)] if p.s == 16 else [(4, 2), (20, 22)], r=0)


def gauge(p):
    if p.s == 16:
        p.arc(7.5, 9.5, 6, 135, 405)
        p.line([(7.5, 9.5), (9.5, 7.5)], r=0)
    else:
        p.arc(12, 14, 9, 135, 405)
        p.line([(12, 14), (15.5, 10.5)], r=0)


def bars(p):
    if p.s == 16:
        p.line([(1.5, 1.5), (1.5, 14.5), (14.5, 14.5)], r=1.2)
        p.line([(5.5, 11.5), (5.5, 7.5)], r=0)
        p.line([(8.5, 11.5), (8.5, 3.5)], r=0)
        p.line([(11.5, 11.5), (11.5, 9.5)], r=0)
    else:
        p.line([(3, 3), (3, 21), (21, 21)], r=1.6)
        p.line([(8, 17), (8, 11)], r=0)
        p.line([(13, 17), (13, 5)], r=0)
        p.line([(18, 17), (18, 14)], r=0)


def pulse(p):
    if p.s == 16:
        p.line([(1.5, 7.5), (4.5, 7.5), (6.5, 13.5), (9.5, 2.5), (11.5, 7.5), (14.5, 7.5)], r=0.3)
    else:
        p.line([(2, 12), (6, 12), (9, 21), (15, 3), (18, 12), (22, 12)], r=0.5)


def terminal(p):
    if p.s == 16:
        p.line([(2.5, 3.5), (6.5, 7.5), (2.5, 11.5)], r=0.4)
        p.line([(7.5, 12.5), (13.5, 12.5)], r=0)
    else:
        p.line([(4, 6), (10, 12), (4, 18)], r=0.6)
        p.line([(12, 19), (20, 19)], r=0)


def puzzle(p):
    if p.s == 16:
        p.line([(1.5, 5.5), (5.5, 5.5), (5.5, 2.5), (9.5, 2.5), (9.5, 5.5), (12.5, 5.5), (12.5, 7.5), (14.5, 7.5),
                (14.5, 11.5), (12.5, 11.5), (12.5, 14.5), (1.5, 14.5)], closed=True, r=0.8)
    else:
        p.line([(2, 8), (8, 8), (8, 3), (14, 3), (14, 8), (19, 8), (19, 11), (22, 11), (22, 17), (19, 17), (19, 22),
                (2, 22)], closed=True, r=1.1)


def gear(p):
    cx, outer, inner, hole = (8, 6.75, 4.4, 2) if p.s == 16 else (12, 10, 7, 3)
    pts = []
    for i in range(6):
        for da, radius in ((-23, inner), (-13, outer), (13, outer), (23, inner)):
            a = math.radians(i * 60 + da)
            pts.append((cx + radius * math.cos(a), cx + radius * math.sin(a)))
    p.line(pts, closed=True, r=0.3 if p.s == 16 else 0.5)
    p.circle(cx, cx, hole)


def keyboard(p):
    if p.s == 16:
        p.rect(1.5, 3.5, 14.5, 12.5, r=1.4)
        for x in (4.5, 8, 11.5):
            p.circle(x, 6.5, 0.8, filled=True)
        p.line([(5.5, 9.5), (10.5, 9.5)], r=0)
    else:
        p.rect(2, 4, 22, 20, r=2)
        for x in (6, 10, 14, 18):
            p.circle(x, 8, 1, filled=True)
        for x in (8, 12, 16):
            p.circle(x, 11.5, 1, filled=True)
        p.line([(8, 16), (16, 16)], r=0)


def grad_cap(p):
    if p.s == 16:
        p.line([(7.5, 2.5), (14.5, 6), (7.5, 9.5), (0.5, 6)], closed=True, r=0.5)
        p.line([(3.5, 8.5), (3.5, 11.5), (7.5, 13.5), (11.5, 11.5), (11.5, 8.5)], r=0.8)
        p.line([(14.5, 6), (14.5, 10.5)], r=0)
    else:
        p.line([(12, 4), (22, 9), (12, 14), (2, 9)], closed=True, r=0.7)
        p.line([(6, 13), (6, 17), (12, 20), (18, 17), (18, 13)], r=1.1)
        p.line([(22, 9), (22, 15)], r=0)


def users(p):
    if p.s == 16:
        p.circle(5.5, 4.5, 2.5)
        p.line([(1.5, 13.5), (1.5, 11.5), (3.5, 9.5), (7.5, 9.5), (9.5, 11.5), (9.5, 13.5)], r=1.6)
        p.arc(10.5, 4.5, 2.5, -70, 70)
        p.line([(12.5, 9.5), (14.5, 11.5), (14.5, 13.5)], r=1.2)
    else:
        p.circle(9, 7, 3.75)
        p.line([(3, 21), (3, 18), (6, 15), (12, 15), (15, 18), (15, 21)], r=2.4)
        p.arc(16, 7, 3.75, -70, 70)
        p.line([(19, 15), (22, 18), (22, 21)], r=1.8)


def user_add(p):
    if p.s == 16:
        p.circle(5.5, 4.5, 2.5)
        p.line([(1.5, 13.5), (1.5, 11.5), (3.5, 9.5), (7.5, 9.5), (9.5, 11.5), (9.5, 13.5)], r=1.6)
        p.line([(12.5, 3.5), (12.5, 7.5)], True, r=0)
        p.line([(10.5, 5.5), (14.5, 5.5)], True, r=0)
    else:
        p.circle(9, 7, 3.75)
        p.line([(3, 21), (3, 18), (6, 15), (12, 15), (15, 18), (15, 21)], r=2.4)
        p.line([(19.5, 5), (19.5, 11)], True, r=0)
        p.line([(16.5, 8), (22.5, 8)], True, r=0)


def hard_hat(p):
    """Bouwhelm: koepel met een kam en een brede rand, zoals HardHat in Open Planner Studio."""
    low, top, side, ridge, band, brim, r = (10.5, 2.5, 2.5, 5.5, 7.5, (1.5, 13.5, 13.5), 4) if p.s == 16 else (15, 4, 4, 10, 10, (2, 22, 19), 6)
    right = (p.s - 1 if p.s == 16 else p.s)
    p.rect(brim[0], low, brim[1], brim[2], r=0.8 if p.s == 16 else 1.2)
    p.line([(ridge, band), (ridge, top), (right - ridge, top), (right - ridge, band)], r=0.7 if p.s == 16 else 1)
    cy = low - 2 if p.s == 16 else low - 3
    p.line([(side, low)] + [(side + r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
                            for a in range(180, 256, 15)], r=0)
    p.line([(right - side - r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in range(-75, 1, 15)] + [(right - side, low)], r=0)


def truck(p):
    if p.s == 16:
        p.line([(2.5, 11.5), (1.5, 11.5), (1.5, 3.5), (9.5, 3.5), (9.5, 11.5), (6.5, 11.5)], r=1.0)
        p.line([(9.5, 6.5), (12.5, 6.5), (14.5, 8.5), (14.5, 11.5), (13.5, 11.5)], r=0.8)
        p.circle(4.5, 12.5, 1.5)
        p.circle(11.5, 12.5, 1.5)
    else:
        p.line([(4, 17), (2, 17), (2, 5), (14, 5), (14, 17), (10, 17)], r=1.4)
        p.line([(14, 9), (18.5, 9), (22, 12.5), (22, 17), (20.5, 17)], r=1.1)
        p.circle(7, 18, 2.75)
        p.circle(17.5, 18, 2.75)


def wrench(p):
    """Steeksleutel als gesloten omtrek met een open bek, zoals Wrench in Open Planner Studio."""
    k = 2 / 3 if p.s == 16 else 1
    cx, cy, r = 15.5 * k, 8 * k, 6.5 * k
    round_part = lambda a, b, step: [(cx + r * math.cos(math.radians(x)), cy + r * math.sin(math.radians(x)))
                                     for x in range(a, b + 1, step)]
    p.line([(15 * k, 6 * k), (17.5 * k, 8.5 * k)] + round_part(-26, 111, 15)
           + [(6 * k, 21 * k), (3 * k, 18 * k)] + round_part(152, 299, 15), closed=True, r=0.4 if p.s == 16 else 0.6)


def route(p):
    if p.s == 16:
        p.circle(3.5, 12.5, 2)
        p.circle(12.5, 3.5, 2)
        p.line([(5.5, 12.5), (11.5, 12.5), (11.5, 7.5), (4.5, 7.5), (4.5, 3.5), (10.5, 3.5)], r=1.9)
    else:
        p.circle(5, 19, 2.75)
        p.circle(19, 5, 2.75)
        p.line([(7.75, 19), (17, 19), (17, 12), (7, 12), (7, 5), (16.25, 5)], r=3)


def signpost(p):
    if p.s == 16:
        p.line([(7.5, 1.5), (7.5, 3.5)], r=0)
        p.line([(2.5, 3.5), (11.5, 3.5), (14, 6), (11.5, 8.5), (2.5, 8.5)], closed=True, r=0.6)
        p.line([(7.5, 8.5), (7.5, 14.5)], r=0)
    else:
        p.line([(12, 2), (12, 5)], r=0)
        p.line([(4, 5), (17, 5), (21, 9), (17, 13), (4, 13)], closed=True, r=0.8)
        p.line([(12, 13), (12, 22)], r=0)


def diamond(p):
    if p.s == 16:
        p.line([(7.5, 1.5), (13.5, 7.5), (7.5, 13.5), (1.5, 7.5)], closed=True, r=0.8)
    else:
        p.line([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=1.1)


def calendar_range(p):
    calendar_manage(p)
    if p.s == 16:
        p.line([(4.5, 10.5), (11.5, 10.5)], True, r=0)
    else:
        p.line([(7, 15.5), (17, 15.5)], True, r=0)


def balance(p):
    if p.s == 16:
        p.line([(7.5, 3.5), (7.5, 13.5)], r=0)
        p.line([(4.5, 13.5), (10.5, 13.5)], r=0)
        p.line([(2.5, 3.5), (12.5, 3.5)], r=0)
        p.line([(2.5, 3.5), (4.5, 10.5), (1, 10.5)], closed=True, r=0.4)
        p.line([(12.5, 3.5), (14, 10.5), (10.5, 10.5)], closed=True, r=0.4)
    else:
        p.line([(12, 3), (12, 21)], r=0)
        p.line([(7, 21), (17, 21)], r=0)
        p.line([(4, 5), (20, 5)], r=0)
        p.line([(5, 5), (8.5, 13), (1.5, 13)], closed=True, r=0.6)
        p.line([(19, 5), (22.5, 13), (15.5, 13)], closed=True, r=0.6)


def eraser(p):
    if p.s == 16:
        p.line([(9.5, 2.5), (14.5, 7.5), (8.5, 13.5), (4.5, 13.5), (1.5, 10.5)], closed=True, r=0.6)
        p.line([(5.5, 6.5), (10.5, 11.5)], r=0)
        p.line([(8.5, 13.5), (14.5, 13.5)], r=0)
    else:
        p.line([(14, 3), (22, 11), (13, 20), (7, 20), (2, 15)], closed=True, r=0.8)
        p.line([(8, 9), (16, 17)], r=0)
        p.line([(13, 20), (22, 20)], r=0)


VORMEN = [
    (plus, 'Plus, zoals deze knoppen in Open Planner Studio. Eén teken, dus geen oranje; ook op 10 tot 12 px leesbaar.',
     ['task.add', 'resource.new', 'calendar.new', 'calendar.holiday-add', 'calendar.work-band-add', 'calendar.promote-menu',
      'company.new', 'documents.new-or-open', 'layout.manage', 'planning.code-type-add', 'planning.code-value-add',
      'planning.custom-field-add', 'planning.dependency-add', 'planning.interruption-add', 'planning.profile-new',
      'resource.availability-step-add', 'table.column-add-menu', 'task.note-add']),
    (cross, 'Kruis, zoals sluiten in Open Planner Studio.', ['ui.close', 'document.close', 'window.close', 'list.item-remove']),
    (minus, 'Min, zoals in Open Planner Studio.', ['table.column-hide', 'window.minimize']),
    (check, 'Vinkje, zoals in Open Planner Studio.', ['input.confirm-draft', 'selection.mark', 'status.column-present']),
    (chevron_right, 'Punthaak naar rechts, zoals in Open Planner Studio.', ['tree.expand', 'resource.next', 'tabs.scroll-end']),
    (chevron_left, 'Punthaak naar links, zoals in Open Planner Studio.', ['resource.previous', 'tabs.scroll-start']),
    (chevron_down, 'Punthaak omlaag, zoals in Open Planner Studio.', ['tree.collapse', 'input.time-decrease', 'guide.compact']),
    (chevron_up, 'Punthaak omhoog, zoals in Open Planner Studio.', ['input.time-increase', 'guide.expand']),
    (dropdown, 'Kleine punthaak omlaag aan de rand van een keuzeveld, zoals in Open Planner Studio.', ['ui.dropdown']),
    (chevrons_in, 'Twee punthaken naar elkaar toe, zoals Alles inklappen in Open Planner Studio.', ['tree.collapse-scope']),
    (chevrons_out, 'Twee punthaken van elkaar af, zoals Alles uitklappen in Open Planner Studio.', ['tree.expand-scope']),
    (arrow_left, 'Pijl naar links, zoals Terug in Open Planner Studio. Een pijl is één ding, dus geen oranje.', ['nav.back']),
    (arrow_right, 'Pijl naar rechts, zoals in Open Planner Studio.', ['status.library-suggestion']),
    (arrow_up, 'Pijl omhoog, zoals in Open Planner Studio.', ['status.install-size-larger']),
    (arrow_down, 'Pijl omlaag, zoals in Open Planner Studio.', ['status.install-size-smaller']),
    (arrow_diagonal, 'Schuine pijl, zoals het pijlgereedschap in Open Planner Studio.', ['draw.arrow']),
    (arrows_sort, 'Twee pijlen tegen elkaar in, zoals Sorteren in Open Planner Studio.', ['list.sort-fields']),
    (arrow_from_line, 'Lijn met een oranje pijl omhoog, zoals In bibliotheek opnemen in Open Planner Studio.', ['calendar.promote']),
    (undo, 'Teruggebogen pijl, zoals Ongedaan maken in Open Planner Studio. Eén lijn, dus geen oranje.', ['edit.undo']),
    (redo, 'Gespiegelde pijl van Ongedaan maken, zoals in Open Planner Studio.', ['edit.redo']),
    (check_updates, 'Twee draaipijlen, zoals Vernieuwen in Open Planner Studio.', ['ui.refresh', 'status.busy', 'credential.regenerate']),
    (turn_back, 'Draaipijl tegen de klok in, zoals Terugzetten in Open Planner Studio.', ['backup.recover', 'table.columns-reset']),
    (page_new, 'Blad met een oranje plus, zoals Nieuw project in Open Planner Studio.', ['file.new']),
    (page_lines, 'Blad met regels: een projectbestand. Een aanduiding, dus geen oranje.', ['file.type-project']),
    (page_letter, 'Blad met de letter T, zoals FileType in Open Planner Studio: een ander bestand. Een aanduiding, dus geen oranje.', ['file.type-other']),
    (page_zip, 'Blad met rits, zoals Installeren uit ZIP in Open Planner Studio.', ['extension.install-zip']),
    (page_code, 'Blad met punthaken, zoals Installeren uit JS in Open Planner Studio.', ['extension.install-js']),
    (floppy, 'Diskette, zoals Opslaan in Open Planner Studio.', ['file.save', 'backup.create']),
    (floppy_copy, 'Diskette met in oranje de hoek van een tweede exemplaar, zoals Opslaan als in Open Planner Studio.', ['file.save-as']),
    (folder_open, 'Open map, zoals Openen in Open Planner Studio.', ['file.open', 'backup.folder']),
    (hard_drive, 'Harde schijf, zoals Van deze pc in Open Planner Studio.', ['file.local', 'extension.runtime-desktop']),
    (printer, 'Printer, zoals Afdrukvoorbeeld in Open Planner Studio.', ['report.workspace', 'report.print-entry']),
    (tray_arrow_up, 'Bakje met een oranje pijl omhoog. Gedeeld met tien programma\'s: exporteren gaat omhoog en het programma uit. '
                    'Open Planner Studio had hier de pijl omlaag (Download).', ['file.export', 'file.export-options']),
    (software_install, 'Bakje met een oranje pijl omlaag. Gedeeld met negen programma\'s: importeren gaat het programma in. '
                       'Open Planner Studio had hier de pijl omhoog (Upload).', ['file.import']),
    (software_install, 'Bakje met een oranje pijl omlaag, zoals Update downloaden in Open Planner Studio.', ['status.update-available']),
    (book_open, 'Open boek, zoals Voorbeelden in Open Planner Studio.', ['file.examples']),
    (building, 'Gebouw, zoals Bedrijfsbibliotheek in Open Planner Studio.', ['company.library']),
    (books, 'Boeken op een plank, zoals Uit bibliotheek in Open Planner Studio.', ['status.library-linked']),
    (copy_sheets, 'Twee vellen, zoals Kopiëren in Open Planner Studio.', ['edit.copy', 'calendar.duplicate', 'calendar.copy-workdays', 'window.restore']),
    (trash, 'Prullenbak, zoals Verwijderen in Open Planner Studio.', ['edit.delete', 'activity.clear', 'capture.clear-annotations', 'planning.interruption-remove']),
    (pencil, 'Potlood, zoals Bewerken in Open Planner Studio.', ['object.rename', 'calendar.edit', 'capture.annotate']),
    (pen_body, 'Pen, zoals het tekengereedschap in Open Planner Studio.', ['draw.freehand']),
    (letter_t, 'Letter T: de letter is hier de betekenis, zoals het tekstgereedschap in Open Planner Studio. Eén ding, dus geen oranje.', ['draw.text']),
    (rectangle, 'Rechthoek, zoals het rechthoekgereedschap in Open Planner Studio.', ['draw.rectangle']),
    (square, 'Vierkant, zoals Maximaliseren in Open Planner Studio.', ['window.maximize']),
    (stop_square, 'Vierkant, zoals Stoppen in Open Planner Studio.', ['ai.bridge-stop']),
    (corners, 'Vier hoeken: alles past in het kader. Open Planner Studio had hier dezelfde pijlen als Presentatiemodus; '
              'de hoeken geven een eigen vorm in de groep.', ['view.fit']),
    (arrows_out, 'Twee schuine pijlen naar buiten, zoals in Open Planner Studio.', ['view.fullscreen', 'panel.expand-full']),
    (arrows_in, 'Twee schuine pijlen naar binnen, zoals in Open Planner Studio.', ['view.fullscreen-exit']),
    (panel_right, 'Vlak met een paneel rechts, zoals in Open Planner Studio.', ['panel.right', 'resource.dock']),
    (split_view, 'Vlak in twee helften, zoals Twee tijdschalen in Open Planner Studio.', ['view.gantt-split']),
    (folded_map, 'Gevouwen kaart, zoals Planningsoverzicht in Open Planner Studio.', ['view.minimap']),
    (grid_four, 'Vier vlakken, zoals Alle projecten in Open Planner Studio.', ['documents.overview']),
    (columns, 'Vlak met drie kolommen, zoals Kolommen in Open Planner Studio.', ['table.columns']),
    (gantt_bars, 'Drie verspringende balken, de vorm uit de Gantt-indeling van Open Planner Studio, zonder het kader: '
                 'met kader leek het op de algemene indeling en de kalender ernaast.', ['planning.gantt']),
    (wbs_templates, 'Indelingsvlak met drie vakken, zoals de algemene indeling in Open Planner Studio.', ['layout.identity']),
    (list_tree, 'Lijst met boomlijnen, zoals in Open Planner Studio.', ['layout.task-tree', 'status.structure-locked']),
    (layers, 'Lagen, zoals Groeperen in Open Planner Studio.', ['list.group-by']),
    (funnel, 'Trechter, zoals Filter in Open Planner Studio.', ['list.filter', 'layout.filter']),
    (ring_dot, 'Ring met een punt: aan. Kleur is niet het enige verschil met Bridge uit.', ['status.bridge-live', 'status.recorded-dates']),
    (ring, 'Open ring: uit. Kleur is niet het enige verschil met Bridge actief.', ['status.bridge-off']),
    (status_success, 'Cirkel met vinkje, zoals in Open Planner Studio.', ['status.success']),
    (status_alert, 'Cirkel met uitroepteken, zoals in Open Planner Studio.', ['status.library-item-missing', 'status.library-item-deviated']),
    (status_error, 'Achthoek met uitroepteken, zoals fouten in het waarschuwingenpaneel van Open Planner Studio.', ['status.error']),
    (warnings, 'Waarschuwingsdriehoek, zoals in Open Planner Studio.', ['status.warning', 'status.schedule-preview', 'status.schedule-last-result', 'status.resource-overallocated']),
    (status_info, 'Cirkel met de letter i, zoals in Open Planner Studio.', ['status.info', 'help.context-hint', 'project.properties']),
    (question, 'Cirkel met vraagteken, zoals Hulp in Open Planner Studio.', ['ui.help', 'planning.driving-unknown']),
    (history, 'Klok, zoals Recent in het lint van Open Planner Studio.', ['project.recent']),
    (compass, 'Kompas, zoals Rondleiding in Open Planner Studio.', ['ui.tour']),
    (star, 'Ster, zoals in Open Planner Studio.', ['company.default', 'company.default-status', 'status.project-calendar', 'layout.star']),
    (lock, 'Slot, zoals in Open Planner Studio.', ['ai.read-only-toggle', 'status.assignment-protected']),
    (lock_open, 'Open slot, zoals in Open Planner Studio.', ['ai.read-only-off']),
    (arrows_both_ways, 'Twee pijlen, zoals Verschuivingen in Open Planner Studio. Eén ding, dus geen oranje.', ['panel.schedule-shift']),
    (link_chain, 'Schakel met een middenlijn, zoals Koppelen in Open Planner Studio.', ['planning.external-relation', 'library.link-recognized']),
    (unlink_chain, 'Schakel zonder middenlijn, zoals Losmaken in Open Planner Studio.', ['resource.unlink-library']),
    (relations_menu, 'Dezelfde schakel als Relatie: in deze stand teken je relaties.', ['planning.dependency-draw-mode']),
    (zap, 'Bliksem, zoals Bepalende relatie in Open Planner Studio.', ['planning.driving']),
    (plug, 'Stekker, zoals Verbinding in Open Planner Studio.', ['ai.connection-menu', 'ai.connection-details']),
    (pause, 'Twee strepen, zoals Pauzeren in Open Planner Studio.', ['ai.pause', 'log.pause-view']),
    (play, 'Afspeelpijl, zoals Starten en Hervatten in Open Planner Studio.', ['ai.resume', 'ai.bridge-start', 'log.resume-view', 'diagnostics.run-benchmark']),
    (cylinder_turn, 'Database met een oranje draaipijl, zoals Automatische back-up in Open Planner Studio.', ['backup.auto']),
    (eye, 'Oog, zoals in Open Planner Studio.', ['credential.show', 'panel.properties']),
    (eye_off, 'Doorgestreept oog, zoals in Open Planner Studio.', ['credential.hide', 'panel.properties-hidden', 'capture.mask']),
    (gauge, 'Meter, zoals Prestatiemeting in Open Planner Studio.', ['diagnostics.benchmark']),
    (bars, 'Assen met drie balken, zoals in Open Planner Studio.', ['data.chart', 'stats.downloads', 'assignment.hours-distribution']),
    (pulse, 'Hartslaglijn, zoals AI-activiteit in Open Planner Studio.', ['panel.ai-activity']),
    (terminal, 'Prompt met regel, zoals Debugterminal in Open Planner Studio.', ['panel.debug-terminal']),
    (puzzle, 'Puzzelstuk, zoals Extensies in Open Planner Studio.', ['extensions.manage', 'extension.item']),
    (globe, 'Wereldbol, zoals bij de browserrisico\'s van een extensie in Open Planner Studio.', ['extension.runtime-browser']),
    (gear, 'Tandwiel, zoals Instellingen in Open Planner Studio.', ['ui.settings']),
    (keyboard, 'Toetsenbord, zoals Sneltoetsen in Open Planner Studio.', ['ui.shortcuts']),
    (grad_cap, 'Afstudeerhoed, zoals Tutorials in Open Planner Studio.', ['guide.tutorials']),
    (users, 'Twee personen, zoals Resources in Open Planner Studio.', ['resource.workspace', 'layout.resources']),
    (user_add, 'Persoon met een oranje plus, zoals Resource toewijzen in Open Planner Studio.', ['resource.assign']),
    (hard_hat, 'Bouwhelm, zoals de ploegindeling in Open Planner Studio.', ['layout.crew']),
    (truck, 'Vrachtwagen, zoals de materieelindeling in Open Planner Studio.', ['layout.equipment']),
    (wrench, 'Moersleutel, zoals de gereedschapsindeling in Open Planner Studio.', ['layout.tools']),
    (route, 'Route met twee punten, zoals de kritiekpadindeling in Open Planner Studio.', ['layout.critical']),
    (signpost, 'Wegwijzer, zoals de mijlpaalindeling in Open Planner Studio.', ['layout.milestone']),
    (diamond, 'Ruit: de vorm van een mijlpaal op de Gantt, zoals in Open Planner Studio.', ['task.milestone-menu']),
    (progress_menu, 'Vlag, zoals de vlagindeling in Open Planner Studio.', ['layout.flag']),
    (calendar_range, 'Kalender met een oranje periode, zoals de periode-indeling in Open Planner Studio.', ['layout.period']),
    (balance, 'Weegschaal, zoals Vereffenen in Open Planner Studio.', ['resource.level']),
    (eraser, 'Gum, zoals Vereffening wissen in Open Planner Studio.', ['resource.clear-level']),
    (magnifier, 'Vergrootglas zonder teken, dezelfde lens als de zoomknoppen, zoals Zoeken in Open Planner Studio.', ['view.search']),
]

for tekening, reden, ids in VORMEN:
    for key in ids:
        design(key, reden)(tekening)


def revised_construction(c):
    """Vul een lege Construction met de tekening uit dit bestand."""
    DRAWINGS[c.key](Pen(c))
    return c
