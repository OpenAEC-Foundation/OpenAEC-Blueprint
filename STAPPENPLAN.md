# Stappenplan: harmonisatie van de OpenAEC-apps

Status: **concept voor overleg**, bijgewerkt op 2026-10-16. Besluiten en open vragen staan ook in [`NOTES.md`](NOTES.md).

## Doel

Elke app uit de harmonisatiepagina [`design/harmonized.html`](design/harmonized.html) krijgt dezelfde stijl, in welke taal of techniek hij ook geschreven is. Een gebruiker moet aan elke app zien dat hij bij OpenAEC hoort. Open CAD Studio, Open BIM Studio en de Open 2D Studio AEC-extensie vallen hierbuiten. De installer hoort er wel bij. Het gaat om 17 apps.

Dat betekent dezelfde:

- **kleuren en thema's**, zoals Light en Forge;
- **lettertypen**, met dezelfde groottes en regelhoogtes;
- **iconen**, met één betekenis per icoon, plus de app-iconen en het logo;
- **tegels en kaarten**, zoals in het Bestand-menu, op startschermen en in overzichten;
- **maten en ruimte**, zoals bandhoogtes, afstanden, hoeken en randen;
- **componenten**, zoals knoppen, invoervelden, lint, tabs, panelen en dialogen;
- **schil en layout**, met titelbalk, lint of werkstroom, werkruimte en statusbalk;
- **gedrag**, zoals hover, focus, uitgeschakeld en foutmeldingen.

## Kernidee: één ontwerp, één bron, een uitvoering per techniek

```
          Ontwerp (Style Repo)
                  │
   Eén bron: tokens + iconen + tegels
                  │
             ┌─────────┴─────────┐
   Rust-bibliotheek      Webpakket
   (Iced)                (CSS, iconen, React)
```

Het ontwerp wordt één keer gemaakt. Kleuren, maten en iconen staan in één bronbestand. Daaruit worden per techniek de bestanden gegenereerd die een app nodig heeft. Zo kan geen app uit de pas lopen, ook niet als hij nog niet is omgebouwd.

## De apps per techniek

Het volledige overzicht per app, met interface, status in de Style Repo en licentie, staat in [`APP-OVERZICHT.md`](APP-OVERZICHT.md).

| Techniek | Apps | Hoe de stijl erin komt |
| --- | --- | --- |
| **Tauri + React** | Calc, Calculations, Planner, Geotechniek, Heatloss, Pile Plan, Reports, Energy, Field | Ombouwen naar de Rust-UI (besluit). Tot dan het webpakket |
| **Tauri + Solid** | PDF, Speech, Workspace Composer | Ombouwen naar de Rust-UI (besluit). De Rust-kant blijft |
| **Tauri + Svelte** | Frame | Ombouwen naar de Rust-UI (besluit). De Rust-kant blijft |
| **Rust + Iced** | Pointcloud | Rust-bibliotheek 0.4 |
| **Webapp, React** | BIM Validator | Webpakket |
| **Installer, Tauri + React** | OpenAEC Installer | Rust-UI. Geen wizard maar een hub in de stijl van open-aec.com: kop met mono-label, filterknoppen met aantallen, ecosysteemkaarten met de screenshots van de tools, installeren en bijwerken met voortgang, en webtools in tabs. Voorbeeld: `cargo run --release --features gpu --bin ui04 -- installer` |
| **Later** | FEM | Repository gaf een 404. Hier komen we later op terug |

Twaalf apps hebben een lint. Energy, Field, Speech en Workspace Composer hebben een werkstroom.

**Buiten de harmonisatie:** Open CAD Studio, waar niets aan verandert, Open BIM Studio, die niet hoeft, en de Open 2D Studio AEC-extensie, omdat Open 2D Studio is gestopt. Apps die niet op de harmonisatiepagina staan, vallen ook buiten de scope, behalve de installer. De Y/Z-app doet de gebruiker apart.

## Wat er al ligt

- **Style Book** (repository `OpenAEC-style-book`). Dit bevat de webpakketten `@openaec/design-tokens` 0.1.0 met CSS en een Tailwind-preset, en pakketten voor lint, schil en basiscomponenten in React. De kleuren van de huidige Rust-crate worden hier ook uit gehaald.
- **Repository `openaec-ui`**: gedeelde tokens en component-CSS voor het web.
- **Style Repo** (deze repository): het onderzoek naar alle iconen en schermen, de reviews, en het Rust-prototype `openaec-ui` 0.1.0. Pointcloud gebruikt dat prototype al.

Er zijn dus nu drie plekken met stijlinformatie. Eén van de eerste besluiten is welke daarvan de bron wordt.

## Stappen

### Fase 1: inventaris afronden

- Bepaal later de techniek van Open FEM Studio.
- Bevestig per app of hij een lint of een werkstroom heeft.
- Noteer per app de eigenaar en de volgorde van harmoniseren.
- **Resultaat:** het app-overzicht, compleet en vastgesteld.

### Fase 2: het ontwerp

Gestart op 2026-10-16. Werkplan en voortgang staan in [`design/ontwerp-0.4/README.md`](design/ontwerp-0.4/README.md).

- **Fundament.** Thema's, kleurbetekenis, lettertypen, maten, toestanden en toegankelijkheid.
- **Iconen.** Eén stijl en raster, met een 16 px-variant. Eerst de algemene set, dan de vaksets zoals FEM, PDF, geotechniek en puntenwolken, en dan de app-iconen.
- **Tegels en kaarten.** Eén ontwerp voor tegels in het Bestand-menu, op startschermen en in overzichten.
- **Componenten.** Opbouw, maten en toestanden van elk bedieningselement.
- **Layouts.** Referentieschermen voor een lint-app en een werkstroom-app, in alle thema's.
- **Vaststellen.** Bespreken met leidinggevende en gebruikers, daarna het ontwerp bevriezen als versie 0.4.

### Fase 3: één bron

- De bron staat in de Style Repo: [`design/ontwerp-0.4/tokens-0.4.json`](design/ontwerp-0.4/tokens-0.4.json) (besloten 2026-10-16).
- **Klaar (2026-10-22):** [`scripts/generate_tokens_04.py`](scripts/generate_tokens_04.py) maakt daaruit de Rust-module `openaec_ui::design` en [`web/openaec-tokens.css`](web/openaec-tokens.css). Met `--check` controleert het script of beide actueel zijn.
- Nog te doen: de iconen van Codex en de tegelmaten in dezelfde bron opnemen.
- **Resultaat:** één wijziging in de bron komt automatisch in alle uitvoeringen.

### Fase 4: uitvoeringen per techniek

- **Rust-bibliotheek 0.4**, vanaf nul gebouwd. Architectuur, fundament, componenten, schil, layouts, documentatie en release. Het Rust-prototype dient als referentie.
  - **Klaar (2026-10-22):** fundament, componenten, tegels en kaarten, en de navigatie van werkstroom-apps in `openaec_ui::design`. De galerij `cargo run --release --features gpu --bin ui04` toont een lint-app met startscherm, Bestand-scherm en instellingen, en een werkstroom-app met zijbalk of stappen.
  - **Klaar (2026-10-22):** de eigen titelbalk met werkende vensterknoppen (slepen, dubbelklikken, minimaliseren, maximaliseren, sluiten met de vraag om op te slaan), versleepbare panelen en menu's (rechtermuisknop op tabel, boom en documenttabs, en het menu in de titelbalk).
  - **Klaar (2026-10-22):** de iconen van Codex als vaste set in de crate [`crates/openaec-icons`](crates/openaec-icons/): 945 iconen in 16 en 24 px, per app een feature, zodat een app alleen haar eigen iconen meeneemt. De galerij toont ze allemaal: `cargo run --release --features gpu --bin ui04 -- iconen`. Gemaakt door [`scripts/generate_icon_crate.py`](scripts/generate_icon_crate.py) uit de verliesvrije export.
  - **Klaar (2026-10-23):** overgestapt van iced 0.13.1 naar iced 0.14.0 (`openaec-ui`, galerij en Style Repo). Schermlezerproef op Windows: iced 0.14 en de COSMIC-fork geven nog niets door, plushie-iced het meeste maar zonder focusmeldingen. Advies: op 0.14 blijven, nu de toetsenbordroute en toegankelijke namen in de bibliotheek bouwen, en de proef herhalen bij elke iced-release. Zie [`design/schermlezerproef/`](design/schermlezerproef/README.md).
  - **Klaar (2026-10-23):** toetsenbordroute in `openaec_ui::design` (issue [#2](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/2)): Tab en Shift+Tab langs alle bedienbare onderdelen, Enter en spatie om te activeren, focusrand alleen bij toetsenbordgebruik, en een dialoog die de focus vasthoudt en teruggeeft. De pijltjestoetsen volgen nog.
  - Nog te doen: pijltjestoetsen (#2), toegankelijke namen (#3) en de eerste app die de bibliotheek echt gebruikt (fase 5).
- **Webpakket.** CSS en iconen die in elk webframework werken, met componenten voor React. Dit bouwt voort op het Style Book of vervangt het, afhankelijk van fase 3.
  - **Klaar (2026-10-22):** [`web/openaec-components.css`](web/openaec-components.css) met de componenten van 0.4 en de websitestijl van de installer, voor webtools zoals BIM Validator. Overzicht in vijf thema's: [`web/componenten.html`](web/componenten.html).
  - Nog te doen: de iconen als los webbestand en de React-componenten.
- **Resultaat:** per techniek een uitvoering met een voorbeeld en een korte handleiding.

### Fase 5: apps harmoniseren

- **Testversie van de hele nieuwe UI.** Zodra de bibliotheek 0.4 en de iconen klaar zijn, bouwen we één app als testversie met de volledige nieuwe UI: thema's, lint, panelen, tegels, startscherm, instellingen en iconen. Die beoordeelt de gebruiker als geheel voordat de andere apps volgen. Gekozen (2026-10-22): Open Planner Studio, Open PDF Studio en Open Calc Studio. Fase 5 begint later.
- **Proefproject:** Open Calc Studio ombouwen naar de Rust-UI. Wat ontbreekt, gaat terug naar de bibliotheek.
- **Daarna per groep**, in deze volgorde:
  1. Pointcloud, die al dezelfde techniek gebruikt;
  2. de overige Tauri-apps;
  3. BIM Validator, met het webpakket;
  4. FEM, zodra de techniek bekend is.
- **Meten.** Houd per app bij hoeveel van de checklist hieronder klaar is.

## Wanneer is een app geharmoniseerd?

Een app is geharmoniseerd als hij:

- [ ] de kleuren en thema's uit de bron gebruikt, zonder eigen kleurwaarden;
- [ ] de gedeelde lettertypen gebruikt;
- [ ] voor elke algemene handeling het gedeelde icoon gebruikt;
- [ ] de gedeelde tegels en kaarten gebruikt;
- [ ] de schil voor zijn interfacesoort volgt;
- [ ] de gedeelde componenten of hun exacte stijl gebruikt;
- [ ] in elk thema door een visuele review is gekomen.

## Samenwerking

- De leidinggevende en de gebruiker nemen de ontwerpbesluiten en keuren goed.
- ChatGPT en Claude maken inventarissen, genereren reviewpagina's, schrijven code en draaien controles. Ze werken volgens [`AGENTS.md`](AGENTS.md) en houden [`NOTES.md`](NOTES.md) bij.

## Besloten na het overleg

Op 2026-10-16 door de gebruiker, die over het ontwerp beslist.

1. **De besluiten van fase 2 zijn vastgesteld.** Het ontwerp is bevroren als versie 0.4. De iconen lopen nog door bij Codex.
2. **De bron is de Style Repo.** Tokens en ontwerp staan in [`design/ontwerp-0.4/`](design/ontwerp-0.4/).
3. **De bibliotheek blijft voorlopig privé** en wordt later openbaar.
4. **De installer hoort erbij.** De Y/Z-app doet de gebruiker apart, buiten dit traject.
5. **Thema's, ontwerpwerkwijze en Open FEM Studio** zijn eerder besloten: vijf thema's, ontwerpen in de Style Repo, en FEM komt later.
6. **Energy en Field gaan naar de Rust-UI.** Energy heeft al een Rust-rekenkern. Voor Field is dat de keuze van Claude, op verzoek van de gebruiker.
7. **PDF, Speech, Composer en Frame gaan naar de Rust-UI.** Alleen hun scherm in Solid of Svelte wordt vervangen. De Rust-kant blijft.
8. **De bibliotheek valt onder LGPL-3.0-only** (2026-10-22), zoals de `repo-cleaner` van de Foundation voorschrijft. De makers van de bestaande code stemmen in. De lettertypen houden OFL, het microfoonicoon Apache-2.0 en de oude Style Book-vectoren van het prototype CC BY-SA 4.0; zie `crates/openaec-ui/NOTICE.md`. De Style Repo-app en het ontwerpmateriaal in `design/` houden hun huidige licentie.

## Nog open

1. **Licentie van de iconen van Codex.** Onder LGPL of een aparte iconenlicentie; de gebruiker controleert eerst of ze nieuw getekend zijn. Issue [#15](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/15).
2. **Field op tablet of telefoon.** Field gaat naar de Rust-UI, die voor desktop is. Blijkt Field op locatie op een tablet of telefoon nodig, dan kijken we opnieuw naar het webpakket. Issue [#20](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/20).
3. **Eigenaarschap.** Wie is eigenaar van het ontwerp, van elke uitvoering en van elke app? Issue [#21](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/21).

Alle open werk staat als issue op GitHub, ook de vervolgstappen van fase 4 en 5.
