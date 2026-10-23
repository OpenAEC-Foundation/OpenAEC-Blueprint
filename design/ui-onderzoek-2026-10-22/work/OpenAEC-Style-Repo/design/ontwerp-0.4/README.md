# Fase 2: het ontwerp voor versie 0.4

Status: **vastgesteld** op 2026-10-16, behalve de iconen (2.2). Dit is het werkplan voor fase 2 uit [`STAPPENPLAN.md`](../../STAPPENPLAN.md).

## Doel

Eén vastgesteld ontwerp waarmee alle apps uit [`APP-OVERZICHT.md`](../../APP-OVERZICHT.md) dezelfde stijl krijgen. Het ontwerp is de opdracht voor bibliotheek 0.4 en het webpakket.

Scope: de 15 actieve apps. Open FEM Studio volgt later en gebruikt dan hetzelfde ontwerp.

## Werkwijze

- **Per onderdeel een specificatie en een reviewpagina.** De specificatie in Markdown beschrijft wat en waarom. De reviewpagina in HTML laat het zien in alle thema's.
- **Elk besluit heeft een status.** Een *voorstel* is nog open. *Besloten* betekent goedgekeurd door de gebruiker of de leidinggevende, met datum. Alleen besloten punten gaan naar versie 0.4.
- **Bewijs uit de bestaande reviews.** Elk voorstel verwijst naar de bron of review waarop het steunt.
- **Ontwerptool.** Tot de vraag over een ontwerptool is beantwoord, ontwerpen we direct in de Style Repo.
- **Generators in `scripts/`.** Reviewpagina's worden gegenereerd uit de tokens, zodat ze niet verouderen.

## Onderdelen

| Nr. | Onderdeel | Status | Specificatie | Bouwt voort op |
| --- | --- | --- | --- | --- |
| 2.1 | Fundament: thema's, kleuren, contrast, typografie, maten, toestanden | **Besloten** | [`01-fundament.md`](01-fundament.md), [`tokens-0.4.json`](tokens-0.4.json), [review](fundament-review.html), [websiteanalyse](bron-website.md), [voorbeelden voor het overleg](overleg-voorbeelden.html) | Style Book-tokens, `assets/themes.css`, [`assessment.md`](../assessment.md) |
| 2.2 | Iconen: stijl, kernset, vaksets, app-iconen | **Bij Codex.** Stijl B gekozen, eerste 31 iconen goedgekeurd, tweede serie ter beoordeling. De voorbeeldpagina's gebruiken deze set al; alleen ontbrekende functies tonen nog een oud icoon | [Eerste serie](../icon-set-b2/index.html), [tweede serie](../icon-set-b2/series-2.html) | Iconreviews, [kruisverband](../icon-semantic-crosswalk.html), [botsingsreview](../icon-collision-review.html) |
| 2.3 | Tegels en kaarten | **Besloten** | [`03-tegels.md`](03-tegels.md), [review](tegels-review.html) | [Bestand-review](../backstage-review.html), [taaktegelreview](../backstage-task-review.html) |
| 2.4 | Componenten | **Besloten** | [`04-componenten.md`](04-componenten.md), [review](componenten-review.html) | Reviews van lint, documentbalk, eigenschappen, dialogen en instellingen |
| 2.5 | Layouts voor lint- en werkstroomapps | **Besloten** | [`05-layouts.md`](05-layouts.md), [review](layouts-review.html) | [`harmonized.html`](../harmonized.html), [Energy-werkstroom](../energy-workflow.html), [Field-routes](../field-route-review.html) |
| 2.6 | Vaststellen en bevriezen als 0.4 | **Vastgesteld** op 2026-10-16, behalve de iconen: [samenvatting](samenvatting.html) | | Alle bovenstaande |

## Volgorde

1. **Fundament eerst.** Iconen, tegels en componenten gebruiken de kleuren, maten en toestanden uit 2.1.
2. **Iconen en tegels** kunnen daarna tegelijk.
3. **Componenten** na het fundament. Ze gebruiken iconen, maar kunnen met de huidige kernset starten.
4. **Layouts** als de componenten in concept staan.
5. **Vaststellen** per onderdeel zodra het concept klaar is. Wacht niet tot alles af is.

## Per onderdeel

### 2.1 Fundament

Thema's, merkkleuren, kleurbetekenis, contrast, lettertypen en groottes, afstanden, hoeken, schaduwen, bandhoogtes van de schil, toestanden, toegankelijkheid en taal.

### 2.2 Iconen

- Stijl: raster, lijndikte, hoeken, vulling en een aparte 16 px-tekening.
- Kernset met algemene handelingen. Startpunt zijn de 35 canonieke iconen van het prototype.
- Vaksets voor PDF, puntenwolken, geotechniek, energie, planning en rekenen.
- App-iconen en logo, zodat alle apps in de taakbalk en de installer bij elkaar passen.
- Eén betekenis per icoon. De reviews tonen dat namen als Download, Copy en Scale nu verschillende handelingen dekken.

### 2.3 Tegels en kaarten

- Taaktegels in het Bestand-menu, zoals Nieuw, Openen en Recent.
- Projectkaarten en recente bestanden op startschermen.
- Kaarten in overzichten en instellingen.
- Per soort: maten, opbouw, iconen, tekst en toestanden.

### 2.4 Componenten

- **Basis:** knop, icoonknop, invoerveld, keuzelijst, checkbox, schakelaar, slider, voortgangsbalk, tooltip en scrollbalk.
- **Samengesteld:** linttab, lintgroep, lintknop, documenttab, paneel met kop, eigenschappenraster, boomstructuur, tabel, zoekbalk, melding, dialoog en lege staat.

### 2.5 Layouts

- **Lint-app:** titelbalk, lint, documenttabs, verkenner, werkruimte, eigenschappen en statusbalk.
- **Werkstroom-app:** titelbalk, stappen- of zijnavigatie, werkruimte en statusbalk.
- Per layout de kernschermen: start, werkruimte, Bestand-menu, instellingen, dialoog, voortgang, onopgeslagen wijzigingen, lege staat en fout.
- Uitgewerkt voorbeeld: Open Calc Studio, omdat die als eerste wordt omgebouwd.

### 2.6 Vaststellen

- Bespreek elk onderdeel met de leidinggevende en enkele gebruikers.
- Zet de besloten punten in de specificaties en bevries ze als versie 0.4.
