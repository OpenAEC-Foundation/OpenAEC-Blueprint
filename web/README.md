# Webpakket

Uitvoering van ontwerp 0.4 voor webapps. Voorlopig alleen de tokens.

- [`openaec-tokens.css`](openaec-tokens.css): kleuren van de vijf thema's, letters, ruimtes, hoeken, schilmaten, schaduwen en de instellingen Werkruimte en Statusbalk als CSS-variabelen met het voorvoegsel `--oa-`.

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

De lettertypen Inter, Space Grotesk en JetBrains Mono laadt de app zelf. Componenten en iconen volgen in fase 4.
