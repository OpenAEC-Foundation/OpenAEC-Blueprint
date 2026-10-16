# Bron: de stijl van open-aec.com

Status: analyse van 2026-10-16, als input voor [`01-fundament.md`](01-fundament.md).

Onderzocht: de homepage, [Architectuur](https://www.open-aec.com/architectuur/) en [Roadmap](https://www.open-aec.com/roadmap/). Alle pagina's gebruiken één stylesheet, `shared/style.css?v=20261015`. De waarden hieronder zijn de berekende stijlen in de browser, niet de bedoelde waarden uit een ontwerp.

## Samenvatting

- **De website is de meest uitgewerkte versie van de huisstijl.** Hij gebruikt dezelfde merkkleuren, lettertypen, afstanden en hoeken als de Style Book-tokens, en voegt daar verlopen, schaduwen en vaste patronen voor labels, tegels en kaarten aan toe.
- **De website heeft geen licht of donker thema.** Hij wisselt lichte, warme secties af met donkere panelen. Die twee vlakken zijn een goed vertrekpunt voor de thema's Light en Forge.
- **Night Build is `#2A2A32`.** Daarin zijn de website en het Style Book het eens. Alleen het OpenAEC-thema gebruikt `#1C1917`.
- **De website lost een deel van het contrastprobleem al op.** Amber tekst op licht wordt `#B45309`, en labels op donker gebruiken Warm Gold. Op andere plekken haalt de website de norm ook niet.

## Kleuren

### Variabelen in de stylesheet

| Variabele | Waarde | Gebruik op de site |
| --- | --- | --- |
| `--amber` | `#D97706` | Knoppen, iconen, accentwoorden in koppen, actieve randen |
| `--signal-orange` | `#EA580C` | Hover van links en primaire knoppen |
| `--warm-gold` | `#F59E0B` | Labels en tabelkoppen op donker, hover van de Feedback-knop |
| `--deep-forge` | `#36363E` | Navigatiebalk, tekst op kaarten, omlijnde knoppen |
| `--night-build` | `#2A2A32` | Donkere panelen, hoofdtekst op licht |
| `--text-on-light` | `#2A2A32` | Tekst op lichte vlakken |
| `--text-on-dark` | `#EDEBE8` | Tekst op donkere vlakken. Iets warmer en zachter dan wit |
| `--surface-light-top` en `-bottom` | `#F7F5F2` naar `#F1EEEA` | Lichte, warme achtergrond |
| `--surface-dark-top` | `#33333C` | Bovenkant van het donkere verloop naar `#2A2A32` |
| `--concrete` | `#F5F5F4` | Labels, tegels en fotovakken |
| `--success`, `--error`, `--info` | `#16A34A`, `#DC2626`, `#2563EB` | Statuskleuren, zoals in het Style Book |

### Vlakken

| Vlak | Waarde |
| --- | --- |
| Pagina | `#F1EEEA`, warm lichtgrijs |
| Lichte kaart | Verloop van wit naar `#FAFAF9`, rand `#2A2A32` op 7% |
| Donker paneel | Verloop van `#33333C` naar `#2A2A32` bij 70% |
| Kaart op donker | Wit op 7% naar 2,4%, rand wit op 10% |
| Voettekst | Hetzelfde donkere verloop als de panelen |

### Accentgebruik

- **Amber `#D97706`:** primaire knoppen, iconen in tegels, het accentwoord in een kop, en een rand van 2 of 3 px om een uitgelichte kaart.
- **Warm Gold `#F59E0B`:** monospace-labels en tabelkoppen op donkere vlakken.
- **Donker amber `#B45309`:** amberkleurige tekst op lichte vlakken, zoals de labels Beta en Alpha en hover-tekst.
- **Signal Orange `#EA580C`:** alleen voor hover.
- **Amber als tint** van 8 tot 18%: de achtergrond van labels, icoontegels en badges.

## Typografie

De site laadt Inter, Space Grotesk en JetBrains Mono, net als het Style Book en het prototype.

| Rol | Lettertype | Grootte en gewicht | Bijzonderheden |
| --- | --- | --- | --- |
| Paginakop (H1) | Space Grotesk | 54 tot 56 px, vet | Letterafstand -0,02 em. Accentwoord in amber |
| Sectiekop (H2) | Space Grotesk | 32 tot 40 px, vet | Letterafstand -0,02 em |
| Kaartkop (H3) | Space Grotesk | 16 tot 20 px, vet | Letterafstand -0,02 em |
| Kleine kop (H4) | Space Grotesk | 14 tot 17 px, medium of halfvet | |
| Inleiding | Inter | 20 px, normaal | Regelhoogte 1,6 |
| Lopende tekst | Inter | 14 tot 16 px, normaal | Regelhoogte 1,6 |
| Navigatie | Inter | 14 px, medium | |
| Knoppen | Inter | 13 tot 16 px, halfvet | |
| Bovenlabel en sectielabel | JetBrains Mono | 12 px, medium | Hoofdletters, letterafstand 0,1 em |
| Badges en statuslabels | JetBrains Mono | 10 tot 12 px, medium | Hoofdletters |
| Datums, tellers, statistieken | JetBrains Mono | 10 tot 13 px | |
| Tabelkop | JetBrains Mono | 12 px, medium | Hoofdletters, Warm Gold op donker |

**Patroon:** Space Grotesk voor koppen, Inter voor tekst en bediening, en JetBrains Mono in hoofdletters voor alles wat een label, status of getal is.

## Vormen

### Hoeken

| Hoek | Aantal op de homepage | Gebruik |
| --- | --- | --- |
| 4 px | 24 | Kleine knoppen, taalkeuze, kleine labels |
| 8 px | 44 | Knoppen, invoervelden, icoontegels, afbeeldingen |
| 12 px | 32 | Kaarten, donkere panelen, tabellen |
| Rond | 37 | Pillabels, badges, filterknoppen, ronde icoonknoppen |

Dit is precies de schaal van het Style Book: 4, 8, 12 px en rond.

### Schaduwen en diepte

- **Zwevende kaart:** een witte binnenlijn van 1 px aan de bovenkant, plus een zachte schaduw naar onder.
- **Diep paneel:** een grote donkere schaduw onder de donkere panelen.
- **Amber gloed:** onder de primaire knop.
- **Hover:** kaarten en knoppen komen 1 tot 4 px omhoog. De rand wordt amber op 35 tot 60%, en de schaduw krijgt een amberkleurige gloed. De overgang duurt 0,15 tot 0,2 seconde.

### Terugkerende onderdelen

| Onderdeel | Opbouw |
| --- | --- |
| **Icoontegel** | 40 × 40 px, hoek 8 px, amber op 14% als vlak, amber op 30% als rand, icoon in amber |
| **Pillabel** | Rond, JetBrains Mono 12 px in hoofdletters, Warm Gold op amber 15%, vaak met een amberkleurige stip |
| **Statuslabel** | Rond, JetBrains Mono 10 tot 12 px in hoofdletters. Tint van 8 tot 14% met donkere tekst in dezelfde kleur, zoals `#166534` op groen of `#B45309` op amber |
| **Primaire knop** | Hoek 8 px, amberverloop van `#E08A12` naar `#D97706`, witte tekst, amber gloed |
| **Glazen knop** | Op donker: wit op 6%, rand wit op 14%. Hover: amber tint en amber rand |
| **Omlijnde knop** | Op licht: rand 2 px Deep Forge, transparant vlak |
| **Kleine knop** | Feedback: 34 px hoog, hoek 4 px, donkere tekst op amber |
| **Lichte kaart** | Hoek 12 px, opvulling 24 px, verloop wit, rand 7%, zwevende schaduw |
| **Uitgelichte kaart** | Als lichte kaart, met een amberkleurige rand van 2 px |
| **Kaart met accentlijn** | Op donker, met een amberkleurige lijn van 3 px aan één kant |
| **Chip** | Rond, Inter 13 px, wit op 5% met rand wit op 10%, op donker |
| **Invoerveld** | Hoek 8 px, `#FAFAF9`, rand `#2A2A32` op 15%, opvulling 12 × 16 px |

### Maten

- Inhoudsbreedte maximaal 1200 tot 1240 px.
- Afstanden op het raster van 4 px, met dezelfde stappen als het Style Book.
- Grote knoppen zijn 60 px hoog, de kleine Feedback-knop 34 px.

## Contrast op de website

Gemeten met dezelfde norm als in [`01-fundament.md`](01-fundament.md): WCAG 2.2 AA.

| Kleurpaar | Verhouding | Norm |
| --- | --- | --- |
| Tekst `#2A2A32` op pagina | 12,30 | Gehaald |
| Tekst `#EDEBE8` op donker paneel | 11,96 | Gehaald |
| Warm Gold-label op donker | 5,43 | Gehaald |
| Status `#166534` op groene tint | 6,24 | Gehaald |
| Amber kop op donker, als grote tekst | 4,47 | Gehaald |
| Label `#B45309` op amber tint over wit | 4,32 | Net te laag |
| Feedback: `#2A2A32` op amber | 4,47 | Net te laag |
| Wit op de primaire knop, onderkant van het verloop | 3,19 | Te laag |
| Wit op de primaire knop, bovenkant van het verloop | 2,69 | Te laag |
| Amber link op de pagina | 2,75 | Te laag |
| Amber icoon op zijn tegel | 2,74 | Te laag voor een icoon |

De website heeft dus dezelfde knelpunten als de thema's. **Besloten op 2026-10-16:** de website wordt niet aangepast. De apps lossen het contrast zelf op.

## Wat dit betekent voor de thema's

Dit zijn voorstellen. Ze staan ook in [`01-fundament.md`](01-fundament.md).

1. **Night Build wordt `#2A2A32`.** De website en het Style Book zijn het eens. Pas het OpenAEC-thema aan.
2. **Light volgt de lichte secties van de website.** Een warme achtergrond, witte kaarten en panelen, en tekst in `#2A2A32`.
3. **Forge volgt de donkere panelen van de website.** Basis `#2A2A32`, verhoogde vlakken `#33333C`, en tekst in `#EDEBE8`. Let op: Forge heeft nu een lichte werkruimte (`#FAFAF9`), OpenAEC een donkere (`#1C1917`). Dat verschil bepaalt of één donker thema genoeg is.
4. **Vaste rollen voor amber.** Amber voor vlakken, iconen en randen. `#B45309` voor amber tekst op licht. Warm Gold voor amber tekst op donker. Signal Orange alleen voor hover.
5. **Tintlabels als vast patroon.** Een tint van 10 tot 15% met donkere tekst in dezelfde kleur. Voor amber is `#92400E` nodig om de norm te halen.
6. **Mono-labels in de apps.** Lintgroeplabels, sectiekoppen in panelen en statuslabels in JetBrains Mono in hoofdletters, zoals op de website. Dat maakt de apps direct herkenbaar.
7. **Dezelfde hoeken als de website.** 4 px voor kleine bediening, 8 px voor knoppen, velden en icoontegels, 12 px voor kaarten en dialogen, en rond voor labels.
8. **De icoontegel als basis voor 2.3 Tegels.** Dezelfde tegel kan in het Bestand-menu, op startschermen en in de installer.
9. **Rustiger in de apps.** Desktopapps nemen de verlopen en de beweging bij hover niet over. Een vlakke kleur en een amberkleurige rand bij hover zijn genoeg, en houden de interface rustig.

## Te besluiten

1. ~~Volgen Light en Forge de vlakken van de website?~~ **Besloten:** ja.
2. ~~Worden Forge en OpenAEC samengevoegd?~~ **Besloten:** ja, met een lichte werkruimte zoals Forge.
3. ~~Krijgen de apps de mono-labels?~~ **Besloten:** ja.
4. ~~Nemen de apps de hoeken van de website over?~~ **Besloten:** variant D, 3, 6 en 10 px. Iets strakker dan de website.
5. ~~Wordt de website zelf ook aangepast voor contrast?~~ **Besloten:** nee, de website blijft zoals hij is.
