<p align="center">
  <img src="brandbook/assets/logo/png/openaec-logo-amber-on-dark-2x.png" alt="OpenAEC Foundation" width="400">
</p>

<h3 align="center">Build free. Build together.</h3>

<p align="center">
  Free and open-source tools for the built environment.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC--BY--SA--4.0-D97706?style=flat-square" alt="License"></a>
  <a href="https://github.com/OpenAEC-Foundation/OpenAEC_stijlbook/issues"><img src="https://img.shields.io/badge/contributions-welcome-D97706?style=flat-square" alt="Contributions welcome"></a>
</p>

---

## About

This repository contains the **OpenAEC Foundation brand identity** — the complete visual language for our open-source AEC tools. Everything you need to build on-brand: logo's, color palette, typography, illustrations, and design system tokens.

## Desktop Application Template

A ready-to-use **Tauri v2 + React + TypeScript** template for building cross-platform desktop applications with the OpenAEC visual identity. All apps built from this template share the same look and feel.

<p align="center">
  <img src="project-templates/Tauri+React/screenshots/app-light-theme.png" alt="OpenAEC Desktop Template — Light Theme" width="800">
</p>

<p align="center">
  <img src="project-templates/Tauri+React/screenshots/settings-theme-switcher.png" alt="OpenAEC Desktop Template — Theme Switcher" width="800">
</p>

**Includes:** Ribbon toolbar with animated tab switching, document tab bar, backstage file menu, side panels, status bar, custom frameless titlebar, i18n (EN/NL), persistent settings, themed dropdowns, and two themes (Light & Dark).

See [`project-templates/Tauri+React/`](project-templates/Tauri+React/) for setup instructions.

## What's inside

```
design/                  # Enige bron: tokens, icons, i18n, ribbons, logos, fonts, apps.toml
generators/              # Zetten design/ om naar packages/, crates/, frappe/ en logos/
packages/                # npm (React): design-tokens, icons, i18n, ribbon, shell, ui-primitives
crates/                  # Rust: openaec-tokens, openaec-icons, openaec-i18n, openaec-ribbon
frappe/openaec_theme/    # Frappe-app met de huisstijl voor Desk en website
brandbook/               # Merkregels, styleguide, exports van logo's en illustraties
project-templates/       # Tauri+React desktop-template
docs/integratie.md       # Huisstijl gebruiken in een app
```

Wijzigingen aan de huisstijl gebeuren in `design/`; zie `design/README.md`.

## Machine-readable tokens

The design tokens specified in [`brandbook/DESIGN-SYSTEM.md`](brandbook/DESIGN-SYSTEM.md) §2 are also available as a machine-readable npm package in [`packages/tokens/`](packages/tokens/). Use this when integrating OpenAEC tokens into an application (Tailwind preset, CSS variables, or JS import).

See [`packages/tokens/README.md`](packages/tokens/README.md) for usage.

## Quick reference

| Token | Value |
|-------|-------|
| **Primary color** | `#D97706` Construction Amber |
| **Dark background** | `#36363E` Deep Forge |
| **Headings** | Space Grotesk 700 |
| **Body text** | Inter 400 |
| **Code** | JetBrains Mono 400 |
| **Gradient** | `linear-gradient(90deg, #D97706, #F59E0B, #EA580C)` |

All fonts are open-source (SIL Open Font License).

## Usage

### Use the logo

Pick the right variant for your context:

| Context | Variant |
|---------|---------|
| Dark backgrounds | `openaec-logo-amber-on-dark` |
| Light backgrounds | `openaec-logo-dark-on-light` |
| Monochrome / grayscale | `openaec-logo-white-on-dark` |
| Favicon / avatar | `openaec-symbol-transparent` |

### Use the design tokens

Copy the CSS starter from [`DESIGN-SYSTEM.md`](brandbook/DESIGN-SYSTEM.md#9-css-starter) into your project, or use the [Tailwind config](brandbook/DESIGN-SYSTEM.md#10-tailwind-css-mapping).

### Regenerate assets

```bash
python brandbook/assets/export_assets.py
```

Requires `cairosvg` and `svglib`. Exports PNG at 1x/2x/3x and PDF from SVG masters.

## Guidelines

- Read [`BRANDBOOK.md`](brandbook/BRANDBOOK.md) for the full brand story, tone of voice, and do's & don'ts.
- Read [`DESIGN-SYSTEM.md`](brandbook/DESIGN-SYSTEM.md) for implementation-ready tokens, component specs, and layout templates.
- The logo minimum size is 32px (digital) / 10mm (print).
- Always maintain a clearance zone of 1x the logo height around the logo.
- Never use Construction Amber as a background fill — it's an accent color.

## Contributing

We welcome contributions. Whether it's fixing a typo, adding a new asset, or translating the docs — every bit helps.

1. Fork this repository
2. Create a feature branch (`git checkout -b add-social-templates`)
3. Commit your changes
4. Open a pull request

First PR? Welcome. Check the [issues](https://github.com/OpenAEC-Foundation/OpenAEC_stijlbook/issues) for a good starting point.

## License

This work is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — you are free to share and adapt, as long as you give credit and share alike.

---

<p align="center">
  <sub>OpenAEC Foundation — Own your tools.</sub>
</p>
