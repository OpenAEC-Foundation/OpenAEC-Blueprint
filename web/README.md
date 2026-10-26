# Webpakket

Uitvoering van ontwerp 0.4 voor webapps, zoals BIM Validator.

- [`openaec-tokens.css`](openaec-tokens.css): kleuren van de vijf thema's, letters, ruimtes, hoeken, schilmaten, schaduwen en de instellingen Werkruimte en Statusbalk als CSS-variabelen met het voorvoegsel `--oa-`.
- [`openaec-components.css`](openaec-components.css): de componenten, met dezelfde maten en toestanden als de Rust-bibliotheek, en de websitestijl van de installer.
- [`openaec-fonts.css`](openaec-fonts.css) en [`fonts/`](fonts/): de lettertypen van de Rust-bibliotheek, zie [Lettertypen](#lettertypen).
- [`componenten.html`](componenten.html): overzicht van alle componenten in de vijf thema's. Kies het thema rechtsboven, of open bijvoorbeeld `componenten.html#dark`.

Het bestand wordt gemaakt door [`scripts/generate_tokens_04.py`](../scripts/generate_tokens_04.py) uit [`design/ontwerp-0.4/tokens-0.4.json`](../design/ontwerp-0.4/tokens-0.4.json). Pas het niet met de hand aan.

## Gebruik

```html
<link rel="stylesheet" href="openaec-tokens.css">
<html data-oa-theme="dark" data-oa-workspace="theme" data-oa-statusbar="theme">
```

- `data-oa-theme`: `light`, `dark`, `blueprint`, `high-contrast-dark` of `high-contrast-light`. Zonder attribuut geldt Licht.
- `data-oa-workspace`: `theme` (standaard), `light` of `dark`.
- `data-oa-statusbar`: `theme` (standaard) of `dark`.
- High contrast negeert de instellingen voor werkruimte en statusbalk.

```css
.panel { background: var(--oa-panel); color: var(--oa-text); border-radius: var(--oa-radius-large); }
.workspace { background: var(--oa-workspace); color: var(--oa-workspace-text); }
```

## Lettertypen

```html
<link rel="stylesheet" href="openaec-fonts.css">
```

[`openaec-fonts.css`](openaec-fonts.css) laadt Inter, Space Grotesk en JetBrains Mono uit [`fonts/`](fonts/): dezelfde bestanden als de Rust-bibliotheek, zonder Google Fonts, zodat de app ook offline dezelfde letters toont. Kopieer de map `fonts/` mee naast het CSS-bestand; de OFL-licenties staan erin. Beschikbare gewichten: Inter 400, 500 en 600, Space Grotesk 500 en 700, JetBrains Mono 400. Daarnaast staan Noto Sans en Noto Sans Symbols erin als terugval: de stapels in `openaec-tokens.css` noemen ze direct na het eigen font, zodat ⌀, Grieks in koppen en Ĳ in monospace op elke computer gelijk zijn. De browser haalt ze alleen op als een teken ze nodig heeft. Knoppen en invoervelden erven het lettertype via `openaec-components.css`; zonder die regel kiest de browser er Arial voor. Koppen gebruiken Space Grotesk Medium (500), net als `openaec_ui::fonts::HEADING`.

Map en CSS worden gemaakt door [`scripts/build_font_package.py`](../scripts/build_font_package.py) uit `crates/openaec-ui/assets/fonts`, samen met [`manifest.json`](../crates/openaec-ui/assets/fonts/manifest.json) met per bestand familie, gewicht, versie, SHA-256 en licentie (issue #24). Pas ze niet met de hand aan.

## Componenten

```html
<link rel="stylesheet" href="openaec-tokens.css">
<link rel="stylesheet" href="openaec-components.css">
<body class="oa-app">
  <button class="oa-button oa-button--primary">Opslaan</button>
</body>
```

Alle klassen beginnen met `oa-`, varianten met `--`. Toestanden gebruiken de aria-attributen die HTML al heeft: `aria-pressed` voor een aan/uit-knop of actieve filterpil, `aria-selected` voor tabs en tabelrijen, `aria-current` voor de zijbalk en de stappenbalk, `aria-checked` voor keuzetegels en `aria-invalid` voor een fout veld.

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
