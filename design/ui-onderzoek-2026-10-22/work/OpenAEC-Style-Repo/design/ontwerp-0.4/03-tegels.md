# 2.3 Tegels en kaarten

Status: **besloten**, 2026-10-16. Bekijk de [reviewpagina](tegels-review.html) voor alle voorbeelden in de vijf thema's.

Alle kleuren, hoeken en maten komen uit [`tokens-0.4.json`](tokens-0.4.json). Waar een tegel een eigen kleur nodig heeft, is die gemengd uit bestaande tokens. Er komen dus geen nieuwe kleuren bij.

**Bronnen**

- Tauri-template: de exportkaarten en het Bestand-menu in `harmonization/references/OpenAEC-style-book/project-templates/Tauri+React/src/components/backstage/`.
- Rust-prototype: de taaktegels in [`backstage-task-review.html`](../backstage-task-review.html).
- Website: de icoontegels en kaarten in [`bron-website.md`](bron-website.md).

## Bouwsteen: de icoontegel

Een vierkant vlak met een icoon erin. Hij komt terug in taaktegels, keuzetegels en de navigatie.

| Eigenschap | Waarde |
| --- | --- |
| Maat | 40 × 40 px, of 32 × 32 px in compacte lijsten |
| Hoek | 6 px (`radius.medium`) |
| Vlak | `selected`, de lichte accenttint |
| Rand | 1 px, `accent` voor 35% gemengd met `raised` |
| Icoon | 22 px, kleur `accent-text` |
| High contrast | Vlak `panel`, rand `accent`, icoon `accent-text` |

## Soorten

### 1. Taaktegel

Voor acties in het Bestand-menu, zoals Nieuw, Openen, Opslaan als, Exporteren en Afdrukken.

| Eigenschap | Waarde |
| --- | --- |
| Opbouw | Icoontegel links, daarnaast titel en omschrijving |
| Binnenruimte | 12 px boven en onder, 16 px links en rechts |
| Ruimte tussen icoon en tekst | 12 px |
| Hoek | 10 px (`radius.large`) |
| Vlak en rand | `raised`, rand 1 px `border` |
| Titel | 13 px, halfvet, `text` |
| Omschrijving | 12 px, `text-secondary` |
| Kolom | Maximaal 620 px breed, 8 px tussen de tegels |

### 2. Rij met recente bestanden

Voor de lijst met recente bestanden in het Bestand-menu.

| Eigenschap | Waarde |
| --- | --- |
| Hoogte | 40 px |
| Opbouw | Bestandsicoon 18 px, naam 12 px, pad 11 px, datum in mono 11 px rechts |
| Lijst | Eén kader met hoek 10 px en rand, rijen gescheiden door een lijn |

### 3. Projectkaart

Voor recente projecten op een startscherm.

| Eigenschap | Waarde |
| --- | --- |
| Breedte | Minimaal 200 px, in een raster |
| Voorbeeldbeeld | 96 px hoog, in de kleur van de werkruimte |
| Tekst | Naam 13 px halfvet, metadata in mono 11 px |
| Status | Rond statuslabel in mono 11 px, in de statuskleur |
| Vorm | Hoek 10 px, rand, paneelschaduw |

### 4. Keuzetegel

Voor een keuze uit een groep, zoals een sjabloon of een thema.

| Eigenschap | Waarde |
| --- | --- |
| Opbouw | Icoontegel, titel 13 px, omschrijving 12 px, keuzerondje rechtsboven |
| Gekozen | Rand van 2 px in `selected-bar` en een gevuld rondje |

### 5. Infokaart en cijfertegel

Voor informatie die je leest maar niet aanklikt, zoals het Over-scherm, instellingen en overzichten.

- **Infokaart:** een mono-kop en rijen met sleutel en waarde.
- **Cijfertegel:** een getal in Space Grotesk van 22 px, met een mono-label eronder.
- Geen hover, omdat ze niet klikbaar zijn.

## Toestanden

| Toestand | Licht, Donker en Blueprint | High contrast |
| --- | --- | --- |
| Normaal | Rand `border` | Rand `border` |
| Hover | Rand 1 px `accent` | Rand 2 px `accent` |
| Ingedrukt | Vlak `selected`, rand `accent` | Rand van 4 px in `accent` |
| Focus | Focusring van 2 px in `focus`, met 2 px ruimte | Hetzelfde |
| Uitgeschakeld | Tekst en icoon in `text-disabled`, geen tint in de icoontegel | Hetzelfde, met stippellijnen |
| Gekozen, alleen bij een keuzetegel | Rand 2 px `selected-bar` | Hetzelfde |

Tegels komen niet omhoog bij hover. De website doet dat wel, maar het past niet bij een rustige app.

## Navigatie in het Bestand-menu

Zoals al besloten in de [Bestand-review](../backstage-review.html):

- een kolom van 260 px;
- rijen van 40 px;
- een actieve rij met een streep van 3 px.

Nieuw is dat de actieve rij ook de lichte accenttint krijgt en de tekst in `accent-text`. De kolom op de reviewpagina is smaller, alleen om ruimte te sparen.

## Contrast

De reviewpagina meet 45 combinaties, negen per thema. Ze halen allemaal hun minimum. Tekst haalt 4,5:1, in High contrast 7:1. Iconen, randen en de focusring halen 3:1.

## Besluiten

Genomen door de gebruiker op 2026-10-16.

| Nr. | Besluit |
| --- | --- |
| 1 | Taaktegels volgen variant B: icoontegel links, titel en omschrijving rechts, met een rand |
| 2 | Apps die met projecten werken krijgen een startscherm met projectkaarten |
| 3 | Projectkaarten tonen een voorbeeldbeeld van het project waar de app dat kan maken. Anders tonen ze het app-icoon |
