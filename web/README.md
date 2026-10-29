# Webpakket

Uitvoering van ontwerp 0.4 voor webapps, zoals BIM Validator.

- [`openaec-tokens.css`](openaec-tokens.css): kleuren van de vijf thema's, letters, ruimtes, hoeken, schilmaten, schaduwen en de instellingen Werkruimte en Statusbalk als CSS-variabelen met het voorvoegsel `--oa-`.
- [`openaec-components.css`](openaec-components.css): de componenten, met dezelfde maten en toestanden als de Rust-bibliotheek, en de websitestijl van de installer.
- [`openaec-components.js`](openaec-components.js): optioneel, klein script voor wat CSS niet kan: Escape verbergt een tooltip. Zonder het script werkt alles, behalve dat.
- [`icons/`](icons/): de B2-iconen, één sprite per app, zie [Iconen](#iconen).
- [`openaec-fonts.css`](openaec-fonts.css) en [`fonts/`](fonts/): de lettertypen van de Rust-bibliotheek, zie [Lettertypen](#lettertypen).
- [`react/`](react/README.md): React-componenten op deze CSS (issue #12): knoppen, velden, tegels, meldingen, dialoog, tabel en schil, met toetsenbord en aria.
- [`online/`](online/README.md): de Tauri-standaardapplicatie als webapp met 3D-weergave, gepubliceerd op GitHub Pages (#36).
- [`componenten.html`](componenten.html): overzicht van alle componenten in de vijf thema's. Kies het thema rechtsboven, of open bijvoorbeeld `componenten.html#dark`.

Het bestand wordt gemaakt door [`scripts/generate_tokens_04.py`](../scripts/generate_tokens_04.py) uit [`design/ontwerp-0.4/tokens-0.4.json`](../design/ontwerp-0.4/tokens-0.4.json). Pas het niet met de hand aan.

## Gebruik

```html
<link rel="stylesheet" href="openaec-tokens.css">
<html data-oa-theme="dark" data-oa-workspace="theme" data-oa-statusbar="theme" data-oa-text="standard">
```

- `data-oa-theme`: `light`, `dark`, `blueprint`, `high-contrast-dark` of `high-contrast-light`. Zonder attribuut geldt Licht.
- `data-oa-workspace`: `theme` (standaard), `light` of `dark`.
- `data-oa-statusbar`: `theme` (standaard) of `dark`.
- Kleurrollen voor apps (issues #41–#44): `--oa-field` voor de vulling van tekstvelden, keuzelijsten en zoekvelden; `--oa-border-subtle` voor rasterlijnen en scheidingen binnen een paneel, zoals tabelrijen en daglijnen in een Gantt-diagram; `--oa-text-muted` voor gedempte tekst die nog leesbaar moet zijn (minstens 4,5 : 1, in High contrast 7 : 1). `--oa-border` is de rand tussen vlakken.
- `data-oa-text`: Tekstgrootte (issue #27), `compact`, `standard` (standaard) of `large`. Het zet de `--oa-size-*` en de rijhoogte `--oa-row` (24, 28 of 32 px) voor menu's, eigenschappen, tabellen, knoppen en velden. Iconen blijven 16 en 24 px.
- High contrast negeert de instellingen voor werkruimte en statusbalk.

```css
.panel { background: var(--oa-panel); color: var(--oa-text); border-radius: var(--oa-radius-large); }
.workspace { background: var(--oa-workspace); color: var(--oa-workspace-text); }
```

## Lettertypen

```html
<link rel="stylesheet" href="openaec-fonts.css">
```

[`openaec-fonts.css`](openaec-fonts.css) laadt Inter, Space Grotesk, JetBrains Mono en Inter AEC uit [`fonts/`](fonts/), als WOFF2 met de TTF als terugval: dezelfde bestanden als de Rust-bibliotheek, zonder Google Fonts, zodat de app ook offline dezelfde letters toont. Kopieer de map `fonts/` mee naast het CSS-bestand; de OFL-licenties staan erin. Beschikbare gewichten: Inter 400, 500 en 600, Space Grotesk 500 en 700, JetBrains Mono 400, Inter AEC 400, 500 en 600. Inter AEC is Inter met cijfers van gelijke breedte en een duidelijke I en l, voor getallen (`--oa-font-numbers`, `oa-number`; issue #28). De TTF-bestanden blijven erin voor PDF-bibliotheken zoals jsPDF. Daarnaast staan Noto Sans en Noto Sans Symbols erin als terugval: de stapels in `openaec-tokens.css` noemen ze direct na het eigen font, zodat ⌀, Grieks in koppen en Ĳ in monospace op elke computer gelijk zijn. De browser haalt ze alleen op als een teken ze nodig heeft. Knoppen en invoervelden erven het lettertype via `openaec-components.css`; zonder die regel kiest de browser er Arial voor. Koppen gebruiken Space Grotesk Medium (500), net als `openaec_ui::fonts::HEADING`.

Map en CSS worden gemaakt door [`scripts/build_font_package.py`](../scripts/build_font_package.py) uit `crates/openaec-ui/assets/fonts`, samen met [`manifest.json`](../crates/openaec-ui/assets/fonts/manifest.json) met per bestand familie, gewicht, versie, SHA-256, WOFF2 en licentie (issue #24). Pas ze niet met de hand aan.

## Iconen

```html
<svg class="oa-icon"><use href="icons/pdf.svg#i16-file.save"/></svg>
<svg class="oa-icon oa-icon--24"><use href="icons/pdf.svg#i24-file.save"/></svg>
```

[`icons/`](icons/) heeft per app één sprite met alle B2-iconen van die app, in 16 en 24 px, met de ids `i16-<id>` en `i24-<id>`. `icons/standard.svg` heeft de iconen van de standaardapplicatie (lijst `STANDARD` in het script); de Tauri-sjabloon gebruikt die. Dat is dezelfde indeling als de features van de crate `openaec-icons`. [`icons/manifest.json`](icons/manifest.json) noemt per app de iconen, de grootte en de SHA-256. De kleuren volgen de CSS: de hoofdkleur is `currentColor`, het accent `--icon-accent` (standaard `currentColor`), net als bij `oa-icon` in `openaec-components.css`. Geef een icoon met betekenis een naam via de knop eromheen (`aria-label`); het icoon zelf is `aria-hidden`.

De sprites worden gemaakt door [`scripts/build_web_icons.py`](../scripts/build_web_icons.py) uit de B2-export (revisie 106). De export tekent bochten als heel veel korte lijnstukken met zes decimalen, ongeveer 30 kB per icoon. Voor het web worden punten weggelaten die binnen 0,01 px van de lijn liggen, en coördinaten houden twee decimalen. Geen punt verschuift meer dan 0,02 px en er blijft 8 % van de grootte over. Dat is in Chrome nagemeten tegen een exacte referentie (het icoon op 256 px getekend en teruggemiddeld naar 16 px). De compacte iconen zijn even nauwkeurig als de export: een gemiddelde afwijking van 3,43 tegenover 3,40 op 255, over 150 iconen. De grootste sprite, PDF met 404 iconen, is 1,9 MB, of 544 kB met gzip. `--check` maakt alles opnieuw en vergelijkt het met de bestanden. Een `<use>` naar een ander bestand werkt alleen via een webserver, niet vanaf `file://`.

## Componenten

```html
<link rel="stylesheet" href="openaec-tokens.css">
<link rel="stylesheet" href="openaec-components.css">
<body class="oa-app">
  <button class="oa-button oa-button--primary">Opslaan</button>
</body>
```

Alle klassen beginnen met `oa-`, varianten met `--`. Toestanden gebruiken de aria-attributen die HTML al heeft: `aria-pressed` voor een aan/uit-knop of actieve filterpil, `aria-selected` voor tabs en tabelrijen, `aria-current` voor de zijbalk en de stappenbalk, `aria-checked` voor keuzetegels en `aria-invalid` voor een fout veld.

- **Tooltips.** Een tooltip (`data-oa-tip`) verschijnt bij aanwijzen en bij toetsenbordfocus. Een rij met focus toont ook de tooltips van haar cellen. Met `openaec-components.js` verbergt Escape de tooltip tot de focus of de muis verdergaat; pas de volgende Escape bereikt de pagina (issue #7).
- **Iconknoppen.** Een tooltip is geen naam. Geef elke iconknop een `aria-label`, en een sneltoets ook als `aria-keyshortcuts`. `scripts/build_web_components.py` weigert een iconknop zonder `aria-label`.
- **Afgekorte tekst.** `oa-truncate` kort een tekst af met "…". Zet de volledige tekst in `data-oa-tip` op een ouder die focus kan krijgen, zoals de tab of de cel van een rij met `tabindex`. Op het afgekorte element zelf wordt de tooltip mee afgesneden.
- **Contrastthema's van Windows.** Daarin (`forced-colors`) verdwijnen schaduwen en eigen kleuren. Een geselecteerde tabelrij, de huidige zijbalkpagina, ingedrukte knoppen en filterpillen, en de huidige stap krijgen dan de systeemkleur `Highlight`. Tab- en documenttabstrepen worden een eigen streep in die kleur (issue #6). Getest met `chrome --force-high-contrast`.

| Groep | Klassen |
|---|---|
| Knoppen | `oa-button` (`--primary`, `--quiet`, `--danger`, `--compact`), `oa-icon-button` (`--small`), tooltip met `data-oa-tip` en `data-oa-keys` |
| Websitestijl | `oa-site-button` (`--primary`, `--glass`, `--small`), `oa-round-icon`, `oa-site-card` (`--featured`), `oa-dark-band`, `oa-glass-card` |
| Formulier | `oa-field` (input, select, textarea), `oa-field-message`, `oa-label`, `oa-check`, `oa-switch`, `oa-slider`, `oa-progress` |
| Labels | `oa-status` en `oa-chip` (`--error`, `--warning`, `--success`, `--info`), `oa-pill` met `oa-count` en `oa-pill-letter` |
| Tegels | `oa-icon-tile` (`--compact`, `--amber`), `oa-tile` (`--choice`), `oa-project-card`, `oa-info-card`, `oa-figure-tile`, `oa-recent` |
| Meldingen | `oa-banner` (met toon), `oa-toast`, `oa-dialog`, `oa-overlay`, `oa-menu`, `oa-empty` |
| Schil | `oa-panel`, `oa-panel-header`, `oa-property`, `oa-table`, `oa-tabs`, `oa-document-tabs`, `oa-statusbar` |
| Werkstroom | `oa-workflow`, `oa-sidebar`, `oa-steps`, `oa-form-card`, `oa-action-bar` |

De primaire knop houdt donkere tekst op amber; wit haalt het contrast niet. Het donkere vlak van de website blijft donker in elk thema, de rest volgt het thema. Hoog contrast zet verlopen, gloed en optillen uit en geeft randen 2 px.

## Iconen

De B2-iconen staan in [`design/icon-set-b2/svg`](../design/icon-set-b2/svg/). Zet ze inline in de pagina met de klasse `oa-icon`: de hoofdkleur volgt `currentColor` en het accent `--icon-accent`, standaard `--oa-accent-text`. Met `oa-icon--mono` is het icoon één kleur. Een los webbestand met de iconen volgt nog.

`componenten.html` wordt gemaakt door [`scripts/build_web_components.py`](../scripts/build_web_components.py); `openaec-components.css` is met de hand geschreven.
