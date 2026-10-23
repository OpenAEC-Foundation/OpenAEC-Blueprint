# 2.1 Fundament

Status: **besloten**, 2026-10-16. Alle besluiten staan onderaan onder *Besluiten*.

**Tokenbestand:** alle besluiten staan als vaste waarden in [`tokens-0.4.json`](tokens-0.4.json), met vijf thema's. [`scripts/check_tokens_04.py`](../../scripts/check_tokens_04.py) toetst het contrast van 162 kleurparen. De [reviewpagina](fundament-review.html) toont de thema's.

Bekijk de [reviewpagina](fundament-review.html) voor de kleuren, het contrast en de voorbeelden in alle thema's.

**Bronnen**

- Thema's: [`assets/themes.css`](../../assets/themes.css) en [`assets/tokens.json`](../../assets/tokens.json), 80 velden per thema.
- Style Book-tokens: [`harmonization/references/OpenAEC-style-book/packages/tokens/tokens/`](../../harmonization/references/OpenAEC-style-book/packages/tokens/tokens/), commit `dfdcd41` van 2026-10-16.
- Rust-prototype: `crates/openaec-ui`, en de maten die [`scripts/check_layout_metrics.py`](../../scripts/check_layout_metrics.py) bewaakt.
- Eerdere besluiten: [`design/assessment.md`](../assessment.md).
- De website open-aec.com: [`bron-website.md`](bron-website.md).

## Samenvatting voor het overleg

1. **Contrast.** In Light en Forge haalt de amberkleur als tekst de toegankelijkheidsnorm niet. Dat geldt ook voor witte tekst op amberkleurige knoppen. Een paar kleine kleuraanpassingen lossen dat op, zonder dat het merk verandert.
2. **Twee bronnen spreken elkaar tegen.** Night Build, de betekenis van "accent", de lintmaat en de paneelbreedte verschillen tussen het Style Book en de thema's.
3. **Desktop en web vragen andere maten.** Het Style Book is ingericht op websites met tekst van 16 px. De desktopapps gebruiken vooral 11 en 12 px.
4. **Er ontbreken toestanden.** Er is geen kleur voor uitgeschakeld, en succes, waarschuwing en info zitten niet in de thema's.
5. **Thema's, besloten:** Light, één donker thema, Blueprint en een nieuw High contrast.

## 1. Thema's

De huidige vijf thema's:

| Thema | Achtergrond | Tekst | Accent | Karakter |
| --- | --- | --- | --- | --- |
| Light | `#FAFAF9` | `#36363E` | `#D97706` amber | Licht, standaard |
| Forge | `#36363E` | `#FAFAF9` | `#D97706` amber | Donker grijs |
| OpenAEC | `#27272A` | `#FAFAF9` | `#D97706` amber | Donkerder grijs |
| Blueprint | `#0F1B2D` | `#E0E7FF` | `#60A5FA` blauw | Donkerblauw |
| High contrast | `#000000` | `#FFFFFF` | `#FFD700` geel | Toegankelijkheid |

**Thema's voor versie 0.4**

| Thema | Basis |
| --- | --- |
| Licht | Lichte vlakken van de website |
| Donker | Samenvoeging van Forge en OpenAEC, in de donkere vlakken van de website, met een donkere werkruimte `#26262D` |
| Blueprint | Wordt bijgewerkt voor contrast. Het accent blijft blauw |
| High contrast | Nieuwe kleuren, in een donkere en een lichte variant |

- **Besloten:** Forge en OpenAEC worden samengevoegd tot één donker thema in de kleuren van de website. Blueprint blijft. High contrast blijft, maar krijgt nieuwe kleuren.

### Nieuw High contrast (voorstel)

Het huidige High contrast gebruikt felgeel `#FFD700` op zwart. Dat haalt de norm ruim, maar heeft niets met de merkkleuren te maken. Het voorstel gebruikt de merkkleuren en mikt op de strengste norm, 7:1.

| | High contrast donker | High contrast licht |
| --- | --- | --- |
| Achtergrond | Zwart `#000000` | Wit `#FFFFFF` |
| Tekst, ook secundaire tekst | Wit `#FFFFFF`, 21:1 | Zwart `#000000`, 21:1 |
| Accent, focus en selectie | Warm Gold `#F59E0B`, 9,78:1 | Donker amber `#92400E`, 7,09:1 |
| Primaire knop | Zwarte tekst op Warm Gold, 9,78:1 | Witte tekst op `#92400E`, 7,09:1 |
| Randen | Wit, 1 px, zonder doorzichtigheid | Zwart, 1 px, zonder doorzichtigheid |

Vaste regels voor beide varianten:

- Geen halfdoorzichtige kleuren en geen grijze tekst.
- Selectie en focus altijd met een omlijning van 2 px, niet alleen met een kleurvlak.
- Links en klikbare tekst onderstreept.

**Besloten:** beide varianten.

## 2. Kleuren

### Merkkleuren

| Naam | Kleur | Gebruik volgens het Style Book |
| --- | --- | --- |
| Construction Amber | `#D97706` | Primaire merkkleur, knoppen en accenten. Nooit als groot vlak |
| Signal Orange | `#EA580C` | Hover en opvallende acties |
| Warm Gold | `#F59E0B` | Markeringen en badges |
| Deep Forge | `#36363E` | Donkere vlakken, tekst op licht |
| Scaffold Gray | `#A1A1AA` | Secundaire tekst en randen |
| Blueprint White | `#FAFAF9` | Lichte achtergrond |
| Concrete | `#F5F5F4` | Kaarten en secties |
| Night Build | **`#1C1917` of `#2A2A32`** | Donkerste achtergrond. Zie tegenstrijdigheden |

### Kleurbetekenis

Eerder besloten in [`assessment.md`](../assessment.md): amber betekent selectie en focus, niet zomaar een vakinhoudelijke betekenis.

**Voorstel:** leg per kleur één betekenis vast.

- **Amber:** primaire actie, selectie en focus.
- **Rood:** fout en gevaarlijke actie.
- **Groen:** gelukt.
- **Geel:** waarschuwing. Niet goud, omdat dat te veel op amber lijkt.
- **Blauw:** informatie.
- **Vakkleuren**, zoals spanningen in FEM of grondlagen in geotechniek: een eigen palet, apart van de bedieningskleuren.

### Tegenstrijdigheden

| Punt | Thema's (`themes.css`) | Style Book-tokens | Voorstel |
| --- | --- | --- | --- |
| Night Build | `#1C1917`, gebruikt in het OpenAEC-thema | `#2A2A32` | `#2A2A32`, zoals de website en het Style Book |
| Betekenis van "accent" | Amber `#D97706` | Signal Orange `#EA580C`, als oude alias | Accent is amber. Schrap de alias |
| Grijsschaal | Niet gebruikt | Stap 900 `#2A2A32` is donkerder dan stap 950 `#36363E` | Zet de schaal op volgorde |
| Status-kleuren | Alleen fout (`danger`) | Succes, waarschuwing, info en fout, voor licht en donker | Neem alle vier op in elk thema |
| Uitgeschakeld | Geen veld | Geen veld | Voeg een veld toe per thema |

## 3. Contrast

Norm: WCAG 2.2 niveau AA. Tekst moet 4,5:1 halen. Grote tekst en de randen van bedieningselementen moeten 3:1 halen. Halfdoorzichtige kleuren zijn eerst met de achtergrond gemengd.

**Resultaat per thema**, voor 13 belangrijke kleurparen:

| Thema | Gehaald | Niet gehaald |
| --- | --- | --- |
| Light | 4 | 9 |
| Forge | 4 | 9 |
| OpenAEC | 9 | 4 |
| Blueprint | 10 | 3 |
| High contrast | 13 | 0 |

**De belangrijkste problemen in Light en Forge**

| Kleurpaar | Light | Forge | Nodig |
| --- | --- | --- | --- |
| Tekst op primaire knop | 3,19 | 3,76 | 4,5 |
| Amber als tekst, bijvoorbeeld een actieve linttab | 3,19 | 3,76 | 4,5 |
| Lintgroeplabel | 2,51 | 2,92 | 4,5 |
| Dialoogkop | 2,92 | 3,03 | 4,5 |
| Gedempte tekst | 2,75 | 4,16 | 4,5 |
| Rand van een invoerveld | 1,24 | 1,37 | 3,0 |

**Voorstellen, doorgerekend**

| Voorstel | Light | Forge |
| --- | --- | --- |
| Amber als tekst: Light gebruikt `#B45309`, Forge gebruikt Warm Gold `#F59E0B` | 5,02 op wit | 5,57 op `#36363E` |
| Primaire knop, optie A: donkere tekst `#1C1917` op amber | 5,49 | 5,49 |
| Primaire knop, optie B: witte tekst op donkerder amber `#B45309` | 5,02 | 5,02 |
| Gedempte tekst: minimaal 4,5:1, daaronder alleen voor decoratie | Nader uit te werken | Nader uit te werken |
| Randen van invoervelden: minimaal 3:1. Scheidingslijnen mogen zachter | Nader uit te werken | Nader uit te werken |

**Besloten:** optie A, donkere tekst `#1C1917` op amber `#D97706`. De merkkleur blijft exact.

## 4. Typografie

**Lettertypen.** Het Style Book en het prototype zijn het eens:

- **Inter** voor bediening en tekst;
- **Space Grotesk** voor koppen;
- **JetBrains Mono** voor code en getallen.

Alle drie worden met de app meegeleverd, zodat de weergave niet afhangt van de computer.

**Groottes**

| Bron | Gebruik |
| --- | --- |
| Style Book | 12, 14, 16, 18, 20, 24, 32 en 40 px. Basis 16 px, ingericht op websites |
| Rust-prototype | Meestal 11 en 12 px, soms 9, 10, 13 en 14 px. Koppen tot 29 px |

**Voorstel:** een aparte schaal voor desktopapps.

| Rol | Grootte |
| --- | --- |
| Klein: statusbalk, lintgroeplabel, sneltoetsen | 11 px |
| Standaard: knoppen, velden, lijsten, panelen | 12 px |
| Paneel- en sectiekop | 13 px |
| Dialoogkop | 16 px |
| Paginakop in Bestand-menu en startscherm | 22 px |

- Kleiner dan 11 px komt niet voor.
- Webapps zoals BIM Validator gebruiken de Style Book-schaal.

## 5. Maten

### Bandhoogtes van de schil

| Onderdeel | Tauri-template en Rust-prototype | Style Book-tokens |
| --- | --- | --- |
| Titelbalk | 32 px | 48 px, als topbalk van een webapp |
| Linttabs | 28 px | Geen waarde |
| Lint | 94 px | 96 px |
| Documenttabs | 30 px | Geen waarde |
| Paneelwerkbalk | 24 px | Geen waarde |
| Statusbalk | 22 px | Geen waarde |
| Zijpaneel | 240 px | 280 px |

**Besloten:** desktopapps volgen de maten van de Tauri-template. Die zijn in Pointcloud bewezen en worden automatisch gecontroleerd. De Style Book-maten gelden voor webapps. Pas het Style Book aan, zodat beide bronnen hetzelfde zeggen.

### Afstanden

- Het Style Book gebruikt een raster van 4 px: 4, 8, 12, 16, 20, 24, 32 en verder.
- Het prototype gebruikt ook 2, 3, 5, 6 en 11 px.
- **Voorstel:** alle afstanden op het raster van 4 px. Alleen 2 px mag, voor fijne details zoals de ruimte tussen icoon en rand.

### Hoeken

- Het Style Book gebruikt 4, 8 en 12 px.
- Het prototype gebruikt vooral 0 tot 4 px, zoals de Tauri-template.
- De website gebruikt dezelfde schaal als het Style Book. Zie [`bron-website.md`](bron-website.md).
- **Besloten, variant D:** 3 px voor kleine bediening zoals lintknoppen en checkboxen, 6 px voor knoppen, velden en icoontegels, 10 px voor tegels, kaarten en dialogen, en rond voor labels. Dat is iets strakker dan de website. Banden van de schil, zoals lint en statusbalk, blijven recht.

### Schaduwen

- De thema's hebben schaduwen voor dialogen, panelen en pop-ups.
- Het Style Book heeft klein, middel, groot en een focusring.
- **Voorstel:** drie niveaus. Paneel, pop-up en dialoog, plus de focusring.

## 6. Toestanden

| Toestand | Nu aanwezig | Voorstel |
| --- | --- | --- |
| Normaal | Ja | |
| Hover | `hover`, `hover-strong` | Zo houden |
| Ingedrukt | `active` | Zo houden |
| Geselecteerd | Verspreid over lint en dialogen | Eén veld voor alle componenten |
| Focus | `focus-color`, focusring in het Style Book | Altijd zichtbaar bij toetsenbordbediening |
| Uitgeschakeld | Ontbreekt | Nieuw veld per thema |
| Fout | `danger-color` | Aanvullen met succes, waarschuwing en info |

## 7. Toegankelijkheid

**Wat is WCAG 2.2 AA?** WCAG is de internationale richtlijn voor toegankelijke software en websites. Versie 2.2 is de nieuwste. Er zijn drie niveaus: A is het minimum, AA is de gangbare norm, en AAA is het strengste. Overheden en grote organisaties eisen meestal AA. Nederlandse overheden moeten hun digitale diensten volgens deze richtlijn toegankelijk maken. Sinds juni 2025 geldt in de EU ook de Europese toegankelijkheidswet voor een aantal producten en diensten. De bijbehorende Europese norm is gebaseerd op WCAG 2.1 AA. Versie 2.2 voegt daar een paar eisen aan toe.

In de praktijk betekent AA voor onze apps:

- **Leesbaar contrast.** Gewone tekst heeft minimaal 4,5 keer zoveel contrast als de achtergrond. Grote tekst, iconen en randen van velden minimaal 3 keer.
- **Alles met het toetsenbord.** Elke knop en elk veld is met Tab en Enter te bereiken, zonder muis.
- **Zichtbare focus.** Je ziet altijd waar je met het toetsenbord bent.
- **Niet alleen kleur.** Een fout of status is ook te herkennen aan een icoon of tekst, zodat kleurenblinden het zien.
- **Grote genoeg klikdoelen.** Minimaal 24 bij 24 px.
- **Vergroting.** De interface blijft bruikbaar als de tekst groter wordt gezet.

**Besloten:** alle apps halen WCAG 2.2 niveau AA.

- Contrast volgens hoofdstuk 3.
- Alles is met het toetsenbord te bedienen, en de focus is altijd zichtbaar.
- Betekenis wordt nooit alleen met kleur getoond, maar ook met een icoon of tekst.
- Klikdoelen zijn minimaal 24 bij 24 px.
- High contrast blijft beschikbaar.

## 8. Taal

- Het prototype ondersteunt Nederlands en Engels.
- **Voorstel:** alle teksten komen uit vertaalbestanden, nooit vast in de code.
- **Besloten:** Nederlands is de standaardtaal. Engels is de tweede taal.

## Uitkomst van de websiteanalyse

De website [open-aec.com](https://www.open-aec.com/) is onderzocht in [`bron-website.md`](bron-website.md). De belangrijkste gevolgen voor de thema's:

- **Light** volgt de lichte, warme secties van de website.
- **Forge** volgt de donkere panelen: basis `#2A2A32`, verhoogd `#33333C`, tekst `#EDEBE8`. Daarmee is OpenAEC als apart thema overbodig.
- **Amber heeft vaste rollen.** Vlakken, iconen en randen in `#D97706`. Tekst op licht in `#B45309`, tekst op donker in Warm Gold, en Signal Orange alleen voor hover.
- **Labels in JetBrains Mono, in hoofdletters**, zoals op de website.

## Besluiten

Genomen door de gebruiker op 2026-10-16.

| Nr. | Besluit |
| --- | --- |
| 1 | De thema's volgen de vlakken van de website. Licht: warme achtergrond `#F1EEEA`, witte panelen, tekst `#2A2A32`. Donker: `#2A2A32` en `#33333C`, tekst `#EDEBE8` |
| 2 | Forge en OpenAEC worden samengevoegd tot één donker thema |
| 3 | Blueprint blijft. High contrast blijft en krijgt nieuwe kleuren |
| 4 | Night Build is `#2A2A32` |
| 5 | Primaire knop: donkere tekst `#1C1917` op amber `#D97706` (optie A) |
| 6 | Labels in de apps in JetBrains Mono, hoofdletters, zoals op de website |
| 7 | De kleinste lettergrootte in de apps is 11 px |
| 8 | Nederlands is de standaardtaal |
| 9 | WCAG 2.2 AA is het doel voor alle apps |
| 10 | Hoeken volgens variant D: 3 px voor kleine bediening, 6 px voor knoppen, velden en icoontegels, 10 px voor tegels, kaarten en dialogen, rond voor labels |
| 11 | Herzien: de werkruimte volgt standaard het gekozen thema, dus in Donker donker (`#26262D`). Gebruikers kunnen dat in de instellingen aanpassen: Volgt thema, Altijd licht of Altijd donker |
| 12 | High contrast komt in twee varianten: donker en licht |
| 13 | Blueprint wordt bijgewerkt, zodat het alle contrastparen haalt. Het accent blijft blauw |
| 14 | Desktopapps houden de maten van de Tauri-template: titelbalk 32, linttabs 28, lint 94, documenttabs 30, paneelkop 24, statusbalk 22 en zijpanelen 240 px. Webapps volgen het Style Book. De vormgeving van knoppen en andere onderdelen wordt wel opnieuw ontworpen, in stap 2.4 |
| 15 | Lettergroottes in de apps: 11 px voor statusbalk en labels, ook de mono-labels; 12 px voor knoppen, velden en lijsten; 13 px voor paneelkoppen; 16 px voor dialoogkoppen; 22 px voor paginakoppen |
| 16 | Afstanden op een raster van 4 px: 4, 8, 12, 16, 24 en 32 px. Alleen voor fijne details 2 px |
| 17 | Alle teksten komen uit vertaalbestanden per taal, nooit vast in de code |
| 18 | Statuskleuren hebben in elk thema dezelfde betekenis, met een tint per thema. Waarschuwing is geel. In Blueprint is info turquoise. Zie de tabel hieronder |
| 19 | Schaduwen in drie niveaus: paneel, pop-up en dialoog, plus een focusring. Op donker met een dun licht randje |
| 20 | Geselecteerd: lichte tint van het accent met een streep links. Uitgeschakeld: vervaagd. In High contrast een omlijning en een stippellijn |

## Uitwerking van besluit 18 tot en met 20

Besloten op 2026-10-16, zoals op de [voorbeeldpagina](overleg-voorbeelden.html) in secties 7 en 8.

1. **Statuskleuren met een tint per thema.** Elke statuskleur heeft dezelfde betekenis in alle thema's, maar de tint past zich aan. Zie sectie 7 van de voorbeeldpagina en de tabel hieronder.
2. **Schaduwen in drie niveaus:** paneel, pop-up en dialoog, plus de focusring. Op donker komt er een dun licht randje bij. Zie sectie 8.
3. **Toestanden.** Geselecteerd is een lichte tint van het accent met een streep links. Uitgeschakeld is vervaagd. In High contrast worden dat een omlijning en een stippellijn. Zie sectie 7.

**Statuskleuren per thema**

| Thema | Fout | Gelukt | Waarschuwing | Info |
| --- | --- | --- | --- | --- |
| Licht | `#B91C1C` | `#166534` | `#854D0E` | `#1D4ED8` |
| Donker | `#FCA5A5` | `#4ADE80` | `#FACC15` | `#93C5FD` |
| Blueprint | `#FCA5A5` | `#4ADE80` | `#FACC15` | `#2DD4BF`, turquoise omdat blauw het accent is |
| High contrast donker | `#FF8080` | `#4ADE80` | `#FDE047` | `#7DD3FC` |
| High contrast licht | `#991B1B` | `#166534` | `#713F12` | `#1E3A8A` |

- Alle kleuren halen de norm als tekst, ook op hun eigen tint. High contrast haalt 7:1.
- De tinten staan als vaste kleuren in het tokenbestand (`error-tint` en verder). In Licht is het de statuskleur voor 10% over het paneel. In Donker en Blueprint is het een volle statuskleur voor 28% over het paneel, zie besluit 6 in [`04-componenten.md`](04-componenten.md). High contrast heeft geen tint.
- Waarschuwing is geel in plaats van Warm Gold, omdat Warm Gold te veel op het amber van selectie en focus lijkt.
- Amberkleurige labeltekst is `#92400E` op licht en `#FBBF24` op donker.
