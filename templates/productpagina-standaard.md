# Productpagina-standaard voor open-aec.com

**Status: vastgesteld op 2026-10-29.** Dit is de standaard voor de pagina van elke OpenAEC-app op [open-aec.com](https://open-aec.com). Een nieuwe app krijgt meteen zo'n pagina; de bestaande pagina's worden één voor één omgebouwd.

Opgesteld naar de pagina van [Open Planner Studio](https://open-aec.com/open-planner-studio/) (bron: [`open-planner-studio/index.html`](https://github.com/OpenAEC-Foundation/website/blob/main/open-planner-studio/index.html) in de website-repository), die volgde uit [open-planner-studio#342](https://github.com/OpenAEC-Foundation/open-planner-studio/discussions/342). **Die pagina is het voorbeeld.** Het sjabloon om mee te beginnen is [`productpagina.html`](productpagina.html).

Geldt alleen voor open-aec.com. De app-pagina's van de SuperCloud (`open-aec.com/supercloud/apps/…`) volgen hun eigen opzet.

## Waarom

Elke app-pagina was anders opgebouwd: hier een paar schermafbeeldingen, daar losse kaarten of panelen, de download soms bovenaan en soms onderaan. Een bezoeker moest per app opnieuw zoeken. Met één vaste opbouw weet hij op elke pagina meteen waar de functies, de download, het nieuws, de vragen en de releases staan.

## Waar de onderdelen staan

De pagina's staan in de [website-repository](https://github.com/OpenAEC-Foundation/website) en worden van daaruit uitgerold. De gedeelde onderdelen ook:

| Bestand | Wat |
|---------|-----|
| `shared/style.css` | huisstijl van de hele site (kop, panelen, kaarten, knoppen) |
| `shared/productpagina.css` | de vaste onderdelen van deze standaard, voorvoegsel `pp-` |
| `shared/productpagina.js` | tabs bij Functies, plakkende navigatie, release notes inklappen, download per besturingssysteem |
| `shared/release-notes.js` | de release notes, live uit `data/release-notes/<repo>.json` |
| `shared/translations/<slug>*.json` | de teksten in het Engels, Frans, Turks en Spaans (Nederlands staat in de HTML) |

Bouw geen eigen varianten van deze onderdelen in een pagina. Mist er iets, voeg het dan toe aan `productpagina.css`/`.js`, zodat elke pagina het krijgt.

## Opbouw, in deze volgorde

Verplicht is **vet**. Een extra blok neem je op als het voor die app iets zegt; laat het weg in plaats van het leeg te laten.

1. **Kop** (`header.product-head`, id `top`)
   - categorie als `pill-label` (bijvoorbeeld *Bouwplanning*);
   - naam als `h1`, het onderscheidende woord in `span.accent`;
   - **tagline** (`p.pp-tagline`): één zin over wat de bezoeker ermee wint;
   - **lead**: één of twee zinnen over wat het is en hoe je het gebruikt;
   - **drie knoppen**, in deze volgorde: *Open in de browser* (glow; anders *Download* als glow) · *Download* (naar `#download`) · *Broncode*;
   - **feitenchips** (`ul.chip-row.pp-proof`): drie tot vijf feiten, zoals bestandsformaten, talen, platforms, licentie;
   - **grote schermafbeelding** (`.shot-float.shot-overlap`) van het belangrijkste scherm.
   - *Optioneel:* een smalle melding onder de kop (`p.pp-notice`), bijvoorbeeld "testers gezocht".
2. **Plakkende navigatie** (`nav.pp-subnav`): Functies · Download · Nieuw · Vragen · Releases. Alleen de blokken die er zijn.
3. **Functies** (`section#features.pp-anchor`)
   - kop met `pill-label`, `h2` en één zin uitleg;
   - **tabs** (`.pp-tabs`): *Hoogtepunten* eerst, dan drie tot vijf onderwerpen, *Alle functies* laatst. De tellers vult het script;
   - **Hoogtepunten**: vier tot zes rijen (`article.pp-hl-row`), elk met een schermafbeelding (16:10), een genummerde kicker (`01 Onderwerp`), een titel die het voordeel noemt, twee of drie zinnen, en *Meer lezen* naar de handleiding of wiki. Beeld en tekst wisselen links en rechts;
   - **Alle functies**: tegels (`li.pp-tile`) met `data-cats="<onderwerp> …"`; een tegel kan bij meer onderwerpen horen.
4. **Download** (`section#download.pp-anchor`, alleen als er een desktop- of mobiele app is)
   - `data-pp-repo="OpenAEC-Foundation/<repo>"` op de sectie; het script haalt de nieuwste release op;
   - één hoofdknop (`data-pp-primary`) die het besturingssysteem van de bezoeker kiest;
   - *Andere platforms* (`details.pp-dl-other`) met alle bestanden per platform: sleutels `windows`, `macos`, `linux-deb`, `linux-rpm`, `linux-appimage`, `linux-snap`, `android`;
   - de browserversie als alternatief (`p.pp-dl-note`);
   - zonder JavaScript wijzen alle links al naar de bestanden van de release in de HTML.
5. **Nieuw in vX** (`section#whats-new.pp-anchor`, donker paneel): `pill-label` *Nieuw in vX*, titel, korte samenvatting, knoppen *Volledige changelog* en *Probeer het in de browser*, en vier tot zes kaarten (`split-card`) met de belangrijkste wijzigingen. Bijwerken bij elke release met nieuwe functies.
6. **Veelgestelde vragen** (`section#faq.pp-anchor`): zes tot tien vragen als `details.pp-faq-item`. Vaste vragen, in deze volgorde en alleen als ze kloppen:
   - Welke bestanden kan ik openen? (en uit welk programma)
   - Moet ik iets installeren?
   - Wat kost het?
   - In welk bestandsformaat wordt mijn werk opgeslagen?
   - Op welke systemen draait het?
   - Sluit het aan op de bouwpraktijk? (normen, werkwijzen)
   - Wat kan een AI-assistent ermee? (MCP, API)
   - daarna twee tot vier vragen die bij deze app horen.
7. **Technologie** (`section#technology`): zes kaarten (`features features-compact`) over waarmee het gebouwd is, voor wie dat wil weten.
8. **Release notes** (`section#releases.pp-releases`): `<div data-release-notes="<repo>">`, met `data-release-notes-timeline` als er hoogtepunten per release zijn. De laatste drie staan open; daaronder *Toon alle releases* · *Alle releases op GitHub* · *Changelog* (`p.pp-rel-more`).
9. **Slotvlak** (`section.surface-spot.panel`): de naam en dezelfde knoppen als in de kop.

*Extra's*, tussen 7 en 8, alleen als ze er zijn: handleiding (eigen pagina `/<slug>/handleiding/`), tabel met bestandsformaten, MCP of API, video.

## Inhoud

| Eis | Toelichting |
|-----|-------------|
| Echte schermafbeeldingen | Uit de app zelf, met realistische voorbeelddata (een echt project, geen "Test 1"). Geen persoonsgegevens, browsertabbladen of adressen in beeld. |
| Eén beeld per hoogtepunt | 16:10, minstens 1600 px breed, JPEG of PNG, in `shared/assets/screenshots/<slug>-feat-<onderwerp>.*`. Elk beeld laat iets anders zien. |
| Beelden met een script | Liefst gemaakt met een script dat je opnieuw kunt draaien (in de app-repository), zodat ze bij een nieuwe versie mee kunnen. |
| Verkooptaal | Schrijf wat de gebruiker ermee wint, niet hoe het intern heet. Vaktermen alleen in Technologie. |
| Kloppende teksten | Alleen wat de app vandaag kan. Komt iets later, zet het niet in de functies maar hooguit in de FAQ als "nog niet". |
| Vijf talen | Nederlands in de HTML, Engels, Frans, Turks en Spaans in `shared/translations/<slug>*.json`. Elke zichtbare tekst heeft een `data-i18n`-sleutel. |
| Toegankelijkheid | Alt-tekst bij elk beeld die zegt wat er te zien is; tabs en navigatie werken met het toetsenbord (zit in het script). |

## Controleren

- De website-repository krijgt een controle die per productpagina meldt welke blokken ontbreken.
- Bekijk de pagina op desktop en op een telefoon: geen horizontale scroll, de download kiest het juiste platform.
- Maak daarna de taalversies opnieuw (`scripts/build-i18n-pages.js`, dan `build-release-notes-static.js` en `build-schema.js`).
