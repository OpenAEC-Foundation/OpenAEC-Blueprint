# 2.4 Componenten

Status: **besloten**, 2026-10-16. Bekijk de [reviewpagina](componenten-review.html) voor alle componenten in hun toestanden.

Alle kleuren, hoeken en lettergroottes komen uit [`tokens-0.4.json`](tokens-0.4.json). Maten van lint, documenttabs en panelen volgen de Tauri-template, zoals besloten in [`01-fundament.md`](01-fundament.md). De reviewpagina meet de kleurparen van alle componenten, en ze halen allemaal hun minimum.

## Algemene regels

| Regel | Waarde |
| --- | --- |
| Hoogte van bediening | 28 px standaard, 24 px compact in panelen en het eigenschappenraster |
| Hoeken | 3 px voor lintknoppen, icoonknoppen, checkboxen en tooltips. 6 px voor knoppen en velden. 10 px voor menu's en dialogen. Rond voor schakelaars, sliders en labels |
| Tekst | 12 px. Labels en sneltoetsen 11 px. Paneelkoppen, groepslabels en tabelkoppen in mono-hoofdletters, 11 px |
| Getallen en codes | Getallen in Inter AEC (Inter met cijfers van gelijke breedte en een duidelijke I en l, issue #28), rechts uitgelijnd in tabellen en het eigenschappenraster. Codes en bestandsnamen in JetBrains Mono |
| Hover en ingedrukt | Blijven in dezelfde kleur: iets lichter bij hover, iets donkerder bij ingedrukt. Neutrale onderdelen gebruiken `hover` en `pressed`. In High contrast een rand in `accent` |
| Aan of geselecteerd | `selected` met een streep of rand in `selected-bar`. In High contrast een omlijning |
| Focus | Focusring van 2 px in `focus`. Bij losse knoppen, velden en tegels staat hij buiten het onderdeel, met 2 px ruimte. Waar onderdelen dicht op elkaar staan, staat hij binnen het onderdeel: in het lint, menu's, de boomstructuur, tabellen en documenttabs |
| Uitgeschakeld | `text-disabled`, geen hover. In High contrast met stippellijnen |
| Werkruimte-accent | Iets dat op een geopend document staat, gebruikt de accentkleur die bij de werkruimte past. Een lichte werkruimte in een donker thema krijgt `#92400E`, een donkere werkruimte in een licht thema `#FBBF24`. Een lege staat volgt het thema |

## Basiscomponenten

### Knop

| Soort | Gebruik | Uiterlijk |
| --- | --- | --- |
| Primair | De hoofdactie. Maximaal één per scherm of dialoog | `accent` met `text-on-accent`. Hover `accent-hover`, ingedrukt `accent-pressed` |
| Secundair | Andere acties | `raised` met rand `border-strong`. Hover `hover`, ingedrukt `pressed` |
| Stil | Minder belangrijke acties, zoals "Niet opslaan" | Geen vlak en geen rand. Hover `hover`, ingedrukt `pressed` |
| Gevaarlijk | Verwijderen en andere onomkeerbare acties | Tekst en rand in `error`. Hover en ingedrukt geven een lichte rode tint: 8% en 16% op licht, 6% en 10% op donker |

- Hoogte 28 px, of 24 px compact.
- Binnenruimte 12 px links en rechts, 8 px compact.
- Tekst 12 px halfvet. Een icoon van 16 px links mag.

### Icoonknop

- 28 × 28 px, of 20 × 20 px in een paneelkop. Het icoon is 16 px.
- Een icoonknop die aan of uit staat, krijgt in de aan-stand `selected` en een rand in `selected-bar`.
- Elke icoonknop heeft een tooltip met de naam en de sneltoets.

### Invoerveld, keuzelijst en zoekveld

- Hoogte 28 px, of 24 px in het eigenschappenraster.
- Vlak `raised`, rand 1 px `border-strong`, hoek 6 px. Hulptekst in `text-secondary`.
- Hover geeft een rand in `text`.
- Een fout geeft een rand van 2 px in `error`, met de melding in 11 px onder het veld.
- De keuzelijst heeft een pijltje rechts. Het zoekveld heeft een vergrootglas links.

### Checkbox, keuzerondje en schakelaar

- Checkbox en keuzerondje zijn 16 px, met een rand van 1,5 px in `border-strong`.
- Aan is `accent` met een vinkje in `text-on-accent`, of een stip in `selected-bar`.
- De schakelaar is 32 × 18 px. Aan is `accent` met een witte knop.
- **Wanneer welke?** Een schakelaar werkt direct, zoals een raster tonen. Een checkbox gebruik je in een formulier dat je nog bevestigt.

### Slider, voortgangsbalk en scrollbalk

- **Slider:** een spoor van 4 px in `border-strong`, het gevulde deel in `accent`, en een knop van 14 px met een amberkleurige rand. De waarde staat in mono ernaast.
- **Voortgangsbalk:** 6 px hoog. Bij onbekende duur loopt een blokje heen en weer.
- **Scrollbalk:** 10 px breed, met een ronde greep in `border-strong`.

### Tooltip en menu

- **Tooltip:** `raised` met rand en pop-upschaduw, hoek 3 px, tekst 11 px. De sneltoets staat in mono. Hij verschijnt na 0,5 seconde.
- **Menu en open keuzelijst:** `raised`, pop-upschaduw, hoek 10 px.
  - Regels van 28 px, met een icoon van 14 px.
  - De sneltoets staat rechts in mono.
  - Een vinkje toont wat aan staat.
  - Scheidingslijnen staan in `border`.

## Samengestelde componenten

### Lint

Besloten: variant B, licht en vlak, naar de website. De maten volgen de Tauri-template.

| Onderdeel | Uiterlijk |
| --- | --- |
| Linttabs | Band van 28 px zonder kaders. Tabs zijn tekst in `text-secondary`, 12 px medium, met 12 px ruimte. De actieve tab is `text` halfvet met een streep van 2 px in `accent` eronder |
| Bestand | Een afgeronde knop van 22 px hoog in `accent` met `text-on-accent`, hoek 6 px, zoals de Feedback-knop op de website |
| Lint | 94 px, `panel`. Groepen worden gescheiden door een korte verticale lijn in `border`, met 10 px ruimte boven en onder |
| Grote lintknop | 56 × 66 px, hoek 6 px, icoon 22 px in een vlak van 32 × 32 px, label 11 px op maximaal twee regels |
| Kleine lintknop | 22 px hoog, icoon 16 px, label 11 px, hoek 3 px |
| Actief | Het icoon staat in een icoontegel: `selected` met een rand in de accenttint en het icoon in `accent-text` |
| Hover | De hele knop krijgt `hover` |
| Groepslabel | Mono-hoofdletters, 11 px, `text-secondary`, onderaan gecentreerd |

In de template waren de labels 9 en 10 px. Door het besluit over de kleinste lettergrootte worden ze 11 px.

### Documenttabs

- Een balk van 30 px in `docbar`, met tabs van 24 px zonder kaders en 4 px ruimte ertussen.
- De actieve tab heeft de kleur van de werkruimte, halfvette tekst en afgeronde bovenhoeken van 6 px. Zo loopt hij over in de werkruimte.
- Een stip van 6 px in `accent` toont niet-opgeslagen wijzigingen. De sluitknop is 16 px.

### Paneel, boomstructuur en eigenschappenraster

- **Paneelkop:** 24 px, met een mono-label en icoonknoppen van 20 px.
- **Boomstructuur:**
  - Regels van 24 px en 16 px inspringing per niveau.
  - Een pijltje van 12 px en een icoon van 14 px.
  - De gekozen regel krijgt de tint en een streep links.
- **Eigenschappenraster:**
  - Regels van 28 px. Labels nemen 40% van de breedte in, in `text-secondary`.
  - Compacte velden van 24 px. Getallen in Inter AEC, rechts uitgelijnd.
  - Sectiekoppen van 24 px in mono, met een pijltje om in en uit te klappen.

### Tabel

- Een kop van 28 px in mono-hoofdletters, met een lijn in `border-strong` eronder.
- Regels van 28 px met een lijn in `border`. Geen zebrastrepen.
- Codes en getallen in mono. Getallen en bedragen staan rechts uitgelijnd.
- De gekozen regel krijgt de tint en een streep links.

### Meldingen

- **Melding in de pagina:** de tint van de statuskleur, een streep van 3 px links, een icoon en een vetgedrukt woord als "Fout." of "Let op.". Er staat een sluitknop bij.
- **Melding rechtsonder:** `raised`, pop-upschaduw en hoek 10 px.
  - Een icoon in de statuskleur, een titel en een korte regel.
  - Eventueel een actie als link.
  - Hij verdwijnt na vijf seconden. Een fout blijft staan tot je hem sluit.
- Kleur is nooit het enige signaal. Er staat altijd een icoon en een woord bij.

### Dialoog

- 420 px breed, of 560 px voor een dialoog met meer inhoud.
- `raised`, dialoogschaduw, hoek 10 px, met de overlay van het thema erachter.
- Titel in Space Grotesk 16 px, met een sluitknop rechts.
- Knoppen rechtsonder, met de primaire knop helemaal rechts. Een stille knop als "Niet opslaan" staat links.
- Escape sluit de dialoog. Enter kiest de primaire knop.

### Instellingen voor weergave

In het instellingenvenster, onder Weergave, staan na de themakeuze drie instellingen.

**Werkruimte**

- In het instellingenvenster, onder Weergave, direct na de themakeuze.
- Een keuzelijst met drie keuzes: **Volgt thema** (standaard), **Altijd licht** en **Altijd donker**.
- Een korte uitleg eronder: "Kleur van het vlak waarin je document staat."
- In High contrast is de keuzelijst uitgeschakeld, omdat dat thema zelf de werkruimte bepaalt.

**Statusbalk**

- Keuzes: **Volgt thema** (standaard) en **Altijd donker**.
- In High contrast uitgeschakeld.

**Navigatie**

- Alleen in werkstroom-apps.
- Keuzes: **Zijbalk** (standaard) en **Stappen bovenaan**.

### Lege staat

- Gecentreerd waar het document zou staan.
- Volgt de kleuren van het thema: vlak `panel`, titel `text`, uitleg `text-secondary`, icoon `accent-text`. In Donker is hij dus donker, niet wit.
- Een icoon van 32 px, een titel van 13 px halfvet en een korte uitleg van 12 px.
- Maximaal één primaire knop.

## High contrast

- Geen tinten. Hover en selectie worden randen en omlijningen in `accent`.
- Uitgeschakelde onderdelen krijgen stippellijnen.
- Tekst haalt overal 7:1.

## Wat nog ontbreekt

- **Iconen.** De reviewpagina gebruikt de iconen van Codex, ook voor fout, gelukt, waarschuwing en info. Waar Codex nog geen icoon heeft, staat tijdelijk een oud icoon uit het prototype.

## Besluiten

Genomen door de gebruiker op 2026-10-16.

| Nr. | Besluit |
| --- | --- |
| 1 | Bediening is 28 px hoog, en 24 px compact in panelen en het eigenschappenraster |
| 2 | Tooltips hebben de kleur van het thema |
| 3 | Een melding rechtsonder verdwijnt na vijf seconden. Een fout blijft staan tot je hem sluit |
| 4 | Knoppen blijven bij hover en ingedrukt in dezelfde kleur: iets lichter bij hover, iets donkerder bij ingedrukt (variant A). Geen sprong naar Signal Orange en geen perzikkleurige tint |
| 5 | Lint en documenttabs volgen variant B: licht en vlak, naar de website. Tabs als tekst met een amberkleurige streep, Bestand als afgeronde knop, een actieve lintknop als icoontegel en documenttabs zonder kaders |
| 6 | Meldingen in Donker en Blueprint hebben een zachte maar volle tint: de volle statuskleur voor 28% over het paneel (Z2). De tinten staan als `error-tint`, `success-tint`, `warning-tint` en `info-tint` in het tokenbestand |
| 7 | De werkruimte volgt standaard het thema. In de instellingen staat een keuzelijst Werkruimte met Volgt thema, Altijd licht en Altijd donker. De waarden staan onder `workspace-setting` in het tokenbestand |

**Gevolgen van besluit 4 voor de tokens**

| Thema | `accent-hover` | `accent-pressed` | `hover` | `pressed` |
| --- | --- | --- | --- | --- |
| Licht | `#E78A08` | `#C36B05` | `#F2F2F3` | `#E5E5E6` |
| Donker | `#E78A08` | `#C36B05` | `#3E3E46` | `#494951` |
| Blueprint | `#93C5FD` | `#5694E1` | `#1C273A` | `#283346` |
| High contrast donker | `#FBBF24` | `#D88B0A` | `#000000` | `#000000` |
| High contrast licht | `#7C2D12` | `#7C360C` | `#FFFFFF` | `#FFFFFF` |

- De foutkleur van Blueprint is `#FCA5A5` geworden, zoals in Donker. Met `#F87171` haalde de ingedrukte gevaarlijke knop de norm niet.
