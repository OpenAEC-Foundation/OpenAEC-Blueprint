---
name: iconen-ontwerpen
description: Ontwerp of herzie iconen van de OpenAEC Blueprint volgens docs/iconen.md, per tab van één programma. Gebruik deze skill als je een icoon tekent, een vorm kiest, een icoon voor een knop wisselt, een nieuw icoon-id maakt of de iconenchecks aanpast.
---

# Iconen ontwerpen

De regels staan in [`docs/iconen.md`](../../../docs/iconen.md). Lees die eerst. Deze skill geeft de stappen en de commando's.

## Grens

- Je werkt alleen in het iconendeel: tekeningen, functielijst met betekenissen, tekenscript, checks en richtlijn.
- Kleuren, lettertypes, de opbouw van het lint en de componenten blijven staan. Zie je daar een probleem, maak dan een issue.
- Lijndikte en de tint van het oranje accent verander je niet zonder besluit van de eigenaar.

## Stappen

### 1. Kies één tab

Werk per tab van één programma. Begin met één tab en laat die beoordelen voordat je verder gaat.

Maak een map `design/iconen/<tab>/` met een `knoppen.json`. Per knop: tab, groep, knop (het label in het lint), het B2-id en het icoon dat het programma nu heeft (`main`). Lees de knoppen uit de broncode van het programma op main, niet uit een schermafbeelding. Voorbeeld: [`design/iconen/planning/knoppen.json`](../../../design/iconen/planning/knoppen.json).

Zet de groepen uit het lint in [`design/iconen/groepen.json`](../../../design/iconen/groepen.json). Knoppen die hetzelfde ding met een andere actie zijn (Zoom + en Zoom −), zet je samen onder `families`.

### 2. Per knop: betekenis

Schrijf in één zin wat de gebruiker met de knop wil bereiken. Kijk in het manifest (`design/icon-set-b2/manifest.json`) naar `meaning` van het id dat de knop nu krijgt.

- Zelfde betekenis: gebruik het bestaande id.
- Andere betekenis: maak een nieuw id in `NEW_DEFINITIONS` in [`scripts/b2_richtlijn.py`](../../../scripts/b2_richtlijn.py), met de programma's in `NEW_APPS`. Het oude id blijft bestaan. Leg het bronbewijs vast in `harmonization/icon-set-b2/basis-sources.json` (bestand, regel, commit).
- Wil je een gedeeld id hertekenen? Zoek in `harmonization/icon-set-b2/function-plan.json` welke programma's de functie echt gebruiken. Het nieuwe icoon moet voor elk van die programma's beter zijn. Is dat niet zo, maak dan een eigen id.

### 3. Per knop: bekende vorm

Begin bij het icoon dat het programma nu heeft. Kijk daarna naar MS Project, Primavera P6 of het vakprogramma. Kies de vorm die de gebruiker al kent. Vervang die niet door iets nieuws, en vereenvoudig geen oude B2-tekening.

Leg het icoon van main vast als vergelijking:

```bash
python3 scripts/iconen_referentie_lucide.py <ops>/node_modules/lucide-react design/iconen/referentie/ops-main <naam> ...
```

### 4. Teken in de lijnstijl

Teken in `scripts/b2_richtlijn.py`, met de decorator `@design(id, reden)` en de klasse `Pen`:

- Elke maat heeft een eigen tekening: `if p.s == 16:` en `else:` voor 24.
- 16 px: lijndikte 1,25; rechte lijnen op x,5. 24 px: lijndikte 1,75; rechte lijnen op hele pixels.
- `p.line(...)`, `p.rect(...)`, `p.circle(...)`, `p.arc(...)`, `p.fill(...)`; met `accent=True` alleen op het deel dat de actie of het verschil toont.
- Ligt een oranje deel vóór een lijn van de hoofdkleur, geef dan `accent_front='<reden>'` mee aan `@design`. Zonder die tekst wint de hoofdkleur waar de twee elkaar raken.
- De reden noemt de bekende vorm en, als die er is, het issue.

Bouw daarna de keten. Zet eerst de runtime klaar als die er nog niet is:

```bash
uv pip install --python python3 --target harmonization/sources/b2-runtime -r scripts/requirements-icon-b2.txt
python3 scripts/build_icon_set_b2.py
python3 scripts/build_b2_lossless_library.py
python3 scripts/generate_icon_crate.py
python3 scripts/build_web_icons.py
```

### 5. Draai de checks

```bash
python3 scripts/check_icon_guideline.py
python3 scripts/check_icon_set_b2.py
python3 scripts/check_b2_lossless_library.py
python3 scripts/generate_icon_crate.py --check
python3 scripts/build_web_icons.py --check
```

`check_icon_guideline.py` meldt per icoon wat te dicht, te vol of te gelijk is, met de maat en de grens. Los het op in de tekening. Verander een grens alleen met een reden in `docs/iconen.md`, en houd de negatieve controles werkend.

### 6. Maak het overzichtsblad

```bash
python3 scripts/build_icon_overview.py design/iconen/<tab>
```

Dit maakt `overzicht-<n>.png` (licht en donker, ware grootte en 4 × vergroot) en `overzicht.html` (ware grootte in de browser). Kijk er zelf naar op ware grootte. Lees elke knop eerst in zijn groep, daarna los.

Heb je een principe of regel in `docs/iconen.md` veranderd? Maak dan ook de voorbeeldbeelden opnieuw:

```bash
python3 scripts/build_icon_overview.py --voorbeelden
```

`build_icon_overview.py` heeft `rsvg-convert` en Pillow nodig. Het draait op Linux.

### 7. Laat een aparte ontwerpcontrole kijken

Geef een aparte agent alleen `docs/iconen.md` en het overzichtsblad. Geef hem niet je eigen oordeel of je redenen. Vraag per knop: beter, gelijk of slechter dan main, met een reden, op 16 en 24 px, in licht en donker.

Zegt de controle bij een knop "gelijk" of "slechter", neem dan de vorm van main en teken die opnieuw in de lijnstijl.

### 8. Laat het zien in het programma

Een icoon beoordeel je in het programma zelf, op ware grootte, naast de andere knoppen. Zet de iconen in een eigen branch van het programma en start een dev-server. Laat licht en donker zien.

Voor Open Planner Studio zet `scripts/style-icons.py --source-dir <blueprint>` de tekeningen uit het manifest om naar `icons.generated.ts`.

## Afronden

- Werk `UI-HARMONISATIE.md` bij met een korte tussenstap: wat herzien is, welke checks, en het oordeel.
- Werk `NOTES.md` bij zoals `AGENTS.md` beschrijft.
- Zeg eerlijk welke checks je hebt gedraaid en wat niet getest is.
