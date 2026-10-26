# OpenAEC Application Template — Tauri + React + TypeScript

The official starter template for building OpenAEC Foundation desktop applications. Every application built from this template shares the same interface structure, visual language, and interaction patterns — ensuring a unified experience across the entire OpenAEC ecosystem.

## Purpose

OpenAEC develops multiple tools for the AEC industry. End users should perceive all these applications as part of one coherent product family. This template enforces that consistency by providing a pre-built application shell with standardized layout, theming, navigation, and internationalization — so teams can focus on domain-specific features instead of reinventing chrome.

## What's Included

### Application Shell

| Component | Description |
|-----------|-------------|
| **Title Bar** | Custom window title bar with integrated settings and feedback controls |
| **Ribbon** | Tabbed ribbon toolbar (Home, Edit, Insert, Format, Tools, View, Help) following familiar desktop UX conventions |
| **Backstage View** | Full-screen overlay for file operations, account, and app-level settings |
| **Side Panels** | Resizable left (Explorer) and right (Properties) panels with collapsible sections |
| **Status Bar** | Bottom status bar for contextual information |
| **Main View** | Central content area — your application's workspace |

### Built-in Features

- **Design 0.4** — The five themes (Light, Dark, Blueprint, High contrast dark, High contrast light), fonts (Inter, Space Grotesk, JetBrains Mono) and B2 icons of the OpenAEC design system, from the web package in the OpenAEC-Blueprint repository; the choice is persisted across sessions
- **Internationalization (i18n)** — Full i18n setup with `react-i18next`, auto-detection of system language, and manual override. Ships with English and Dutch; easily extensible
- **Persistent Settings** — Key-value store via `@tauri-apps/plugin-store` for user preferences (theme, language, etc.)
- **Feedback Dialog** — Built-in user feedback mechanism
- **Settings Dialog** — Centralized settings UI for theme and language selection
- **Modal System** — Reusable modal component for dialogs
- **OS Integration** — Platform detection via `@tauri-apps/plugin-os`
- **Custom Window Chrome** — Frameless window with custom decorations for a native look

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Desktop runtime | [Tauri](https://v2.tauri.app/) | v2 |
| Frontend framework | [React](https://react.dev/) | v19 |
| Language (frontend) | TypeScript | v5.9 |
| Build tool | [Vite](https://vite.dev/) | v7 |
| Language (backend) | Rust | 2021 edition |
| i18n | react-i18next | v16 |

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (LTS recommended)
- [Rust](https://www.rust-lang.org/tools/install) toolchain
- [Tauri v2 prerequisites](https://v2.tauri.app/start/prerequisites/) for your platform

### Installation

```bash
npm install
```

### Development

```bash
npm run tauri dev
```

This starts the Vite dev server on `http://localhost:3020` and launches the Tauri window with hot module replacement.

### Production Build

```bash
npm run tauri build
```

Produces platform-specific installers (NSIS for Windows, DMG for macOS, DEB/AppImage for Linux).

## Project Structure

```
├── src/                          # Frontend source (React + TypeScript)
│   ├── App.tsx                   # Main application layout and panel logic
│   ├── App.css                   # Application-level styles
│   ├── themes.css                # --theme-* names on top of the 0.4 tokens
│   ├── openaec/                  # 0.4 tokens and fonts (copied from web/, do not edit)
│   ├── store.ts                  # Tauri store helpers for persistent settings
│   ├── components/
│   │   ├── TitleBar.tsx          # Custom window title bar
│   │   ├── StatusBar.tsx         # Bottom status bar
│   │   ├── Modal.tsx             # Reusable modal dialog
│   │   ├── ribbon/               # Ribbon toolbar and tab components
│   │   ├── backstage/            # Backstage (File menu) view
│   │   ├── settings/             # Settings dialog
│   │   └── feedback/             # Feedback dialog
│   └── i18n/
│       ├── config.ts             # i18n initialization and language switching
│       └── locales/
│           ├── en/               # English translations
│           └── nl/               # Dutch translations
├── src-tauri/                    # Tauri backend (Rust)
│   ├── src/                      # Rust source
│   ├── tauri.conf.json           # Tauri app configuration
│   ├── Cargo.toml                # Rust dependencies
│   ├── capabilities/             # Tauri permission capabilities
│   └── icons/                    # Application icons (all sizes)
├── public/                       # Static assets
├── index.html                    # HTML entry point
├── vite.config.ts                # Vite configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Node dependencies and scripts
```

## Creating a New Application

> **Volledige integratieguide:** zie [`INTEGRATION.md`](INTEGRATION.md) voor stap-voor-stap instructies,
> Tailwind bridge setup, en veelgemaakte fouten.
>
> **Component referentie:** zie [`COMPONENT-MANIFEST.md`](COMPONENT-MANIFEST.md) voor per-component
> documentatie (verplicht/optioneel/aanpassen).

1. **Copy** this template directory and rename it to your application name
2. **Update identifiers** in the following files:
   - `package.json` — `name` field
   - `src-tauri/tauri.conf.json` — `productName`, `identifier`, and window `title`
   - `src-tauri/Cargo.toml` — `name`, `description`, and lib `name`
3. **Replace icons** in `src-tauri/icons/` with your application-specific icons
4. **Set up the Tailwind bridge** — see `tailwind.config.ts` (maps CSS custom properties to Tailwind tokens)
5. **Add your content** to the main view area in `App.tsx`
6. **Extend the ribbon** by modifying or adding tab components in `src/components/ribbon/`
7. **Define domain tokens** — add `--domain-*` CSS custom properties in `themes.css`
8. **Add translations** for any new UI strings in both `en/` and `nl/` locale directories
9. **Run the cleanup checklist** in `INTEGRATION.md` — remove unused buttons, settings tabs, and template text

> Keep the shell structure (title bar, ribbon, side panels, status bar) intact to maintain visual consistency across OpenAEC applications.

## Adding a New Language

1. Create a new locale directory under `src/i18n/locales/` (e.g., `de/`)
2. Copy the English JSON files as a starting point and translate
3. Import the new locale files in `src/i18n/config.ts`
4. Add the language entry to the `LANGUAGES` array
5. Register the translations in the `resources` object

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)

## License

CC BY-SA 4.0 — see the repository root for full license text.

---

Part of the [OpenAEC Foundation](https://github.com/OpenAEC-Foundation) open-source ecosystem.
*Build free. Build together.*

## Design 0.4

The template follows design 0.4 of the [OpenAEC Blueprint](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint), the same design as the Rust library `openaec-ui`.

- **Tokens and fonts** come from `src/openaec/` and the icons from `public/icons/standard.svg`. Do not edit these files: in the Blueprint repository, `python scripts/sync_tauri_template.py` copies them from the web package `web/`, and `--check` checks that they are current.
- **Colours** — components use the `--theme-*` names; `themes.css` maps every one to a 0.4 token (`--oa-*`). The theme is set with `<html data-oa-theme="…">`.
- **Icons** — use `b2("file.save")` from `components/ribbon/icons.ts` for ribbon buttons, or `<B2Icon id="file.save" />`. To add an icon, put its B2 id in `STANDARD` in `scripts/build_web_icons.py` and run that script and `sync_tauri_template.py`.
- **Text** — body text 12 px, labels 11 px, panel headings 13 px (`--oa-size-*`). Text in the accent colour uses `--theme-accent-tint`; dark text on amber (`--theme-accent-text`).
- **View cube** — the 3D view has a view cube in the top-right corner (`components/panels/ViewCube.ts`), as in Revit and AutoCAD: it turns with the camera, a click on a face, edge or corner turns the camera to that view, and the home button returns to the starting view. Use it in your own 3D view with `new ViewCube(camera, controls, labels, homeIcon)` and call `update()` every frame.
