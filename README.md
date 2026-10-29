**English** · [Nederlands](README.nl.md)

<div align="center">

# OpenAEC Blueprint

**The blueprint for every OpenAEC tool. One standard application in Tauri, Rust and the browser, with shared design tokens, fonts, 948 icons, a version scheme and signed releases.**

[![Release](https://img.shields.io/github/v/release/OpenAEC-Foundation/OpenAEC-Blueprint?label=release&color=D97706)](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/releases/latest)
[![Release workflow](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/actions/workflows/release.yml/badge.svg)](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/actions/workflows/release.yml)
[![Icons](https://img.shields.io/badge/icons-948-informational)](crates/openaec-icons/)
[![Themes](https://img.shields.io/badge/themes-5-informational)](design/ontwerp-0.4/tokens-0.4.json)
[![License](https://img.shields.io/badge/license-LGPL--3.0%20%C2%B7%20CC%20BY--SA%204.0-blue)](#license)

### [Try in your browser](https://openaec-foundation.github.io/OpenAEC-Blueprint/) &nbsp;·&nbsp; [Download](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/releases/latest) &nbsp;·&nbsp; [README template](templates/README-tool.md)

![The standard application in the browser: the 3D view with the view cube, theme Dark](docs/images/readme/hero-3d.png)

</div>

OpenAEC Blueprint is where every OpenAEC tool starts. It holds the empty standard application that each tool builds on, the shared look (colours, sizes, fonts and icons), the version scheme and the release workflow that signs everything. A tool that follows the blueprint looks and behaves like the other OpenAEC tools from its first build.

The standard application comes in three forms: a Tauri app with React, a native Rust app, and the Tauri app as a web page that needs no installation.

## Try it

**[Open the browser version](https://openaec-foundation.github.io/OpenAEC-Blueprint/)**. It is the Tauri standard application, built as a web app: ribbon, document tabs, side panels, settings with five themes, and a 3D view with a view cube. Your theme stays after a reload.

The Rust version runs on your own computer: download it below, or build it with `cargo run --bin blueprint`.

## Download

Every release is on the [releases page](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/releases/latest).

| Platform | Standard application | Library for other languages |
|----------|----------------------|-----------------------------|
| **Windows** | `.exe` installer (x64), `.zip` | `.dll` in `openaec-blueprint-sdk_…_windows-x64.zip` |
| **macOS** | `.dmg` (universal: Apple silicon and Intel) | `.dylib` in `openaec-blueprint-sdk_…_macos-universal.tar.gz` |
| **Linux** | `.deb`, `.rpm`, `.AppImage`, `.tar.gz` | `.so` in `openaec-blueprint-sdk_…_linux-x64.tar.gz` |

Every file is signed: Windows with Authenticode, macOS with a Developer ID and notarized by Apple, Linux with the OpenAEC OpenPGP key and a build attestation. `SHA256SUMS` checks all files at once.

## Why use it?

- **One look for all tools.** Colours, sizes and fonts come from one file, [`tokens-0.4.json`](design/ontwerp-0.4/tokens-0.4.json). Rust, CSS and the C library are generated from it.
- **Start with a working shell.** Title bar, ribbon or workflow, document tabs, side panels, status bar and settings are already there. A tool adds its own work in the middle.
- **Behaviour you do not have to rebuild.** Save and close through one close plan (also on Alt+F4), undo per document, the update notice, your own keyboard shortcuts and an accessible name for every control.
- **Five themes.** Light, Dark, Blueprint, High contrast dark and High contrast light, in every form of the application.
- **948 icons** at 16 and 24 px, one style for every tool. A tool picks only the icons it uses.
- **Any language.** A C library (`.dll`, `.dylib`, `.so`) gives tokens and icons to tools that are not written in Rust.
- **Releases that are checked and signed.** One tag starts the checks, the builds for three systems, the signatures and the release.

## Screenshots

| | |
|---|---|
| ![Rust standard application](docs/images/readme/rust-app.png) **The Rust standard application** | ![Four themes](docs/images/readme/themes.png) **Light, Dark, Blueprint and High contrast dark** |
| ![Tauri standard application](docs/images/readme/tauri-app.png) **The Tauri standard application** | ![Settings in the Blueprint theme](docs/images/readme/settings.png) **Settings, theme Blueprint** |
| ![Workflow app](docs/images/readme/workflow-app.png) **A workflow app with steps in a side bar** | ![Icons](docs/images/readme/icons.png) **The icon browser with all icons** |
| ![Installer](docs/images/readme/installer.png) **The OpenAEC Installer in the same style** | |

The Rust screens are in Dutch, the language of the example data. The browser screens are in English.

## The standard application

| Form | Where | Start |
|------|-------|-------|
| **Tauri** (Tauri 2, React, TypeScript) | [`style-book/project-templates/Tauri+React`](style-book/project-templates/Tauri+React/) | see the README of the template |
| **Online** (web build of the Tauri app) | [`web/online/`](web/online/README.md), published on GitHub Pages | [openaec-foundation.github.io/OpenAEC-Blueprint](https://openaec-foundation.github.io/OpenAEC-Blueprint/), or locally `node web/online/build.mjs --serve` |
| **Rust** (iced, library 0.4) | [`src/bin/blueprint.rs`](src/bin/blueprint.rs) | `cargo run --bin blueprint` |

A Rust tool copies `blueprint.rs`, puts its own work in the workspace and its commands in `commands()`. The gallery `ui04` shows more example screens: a ribbon app, a workflow app, the installer, all icons and a type specimen (`cargo run --release --features gpu --bin ui04`).

| | |
|---|---|
| ![File screen of the Rust app](docs/images/readme/rust-file.png) **File screen with recent files** | ![Settings of the Rust app](docs/images/readme/rust-settings.png) **Settings: theme, workspace, status bar and shortcuts** |
| ![Start screen of a ribbon app](docs/images/readme/start-screen.png) **Start screen of a ribbon app, from the gallery** | ![Workflow app with steps at the top](docs/images/readme/workflow-steps.png) **Workflow app with steps at the top, from the gallery** |

The Tauri app comes first, then the same empty app in Rust. Both get a signed release ([#37](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/37)). The online version ([#36](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/36)) is published again after every release.

## What is in this repository

| Part | Where |
|------|-------|
| UI library for Rust | [`crates/openaec-ui`](crates/openaec-ui/) |
| All 948 icons (16 and 24 px), per app to choose | [`crates/openaec-icons`](crates/openaec-icons/) |
| How to design an icon, and the icon checks | [`docs/iconen.md`](docs/iconen.md) |
| C library with tokens and icons for any language | [`crates/openaec-blueprint-sdk`](crates/openaec-blueprint-sdk/) |
| Colours, sizes and fonts (one source) | [`design/ontwerp-0.4/tokens-0.4.json`](design/ontwerp-0.4/tokens-0.4.json) |
| Web package: CSS, fonts and icons per app | [`web/`](web/) |
| Design 0.4: foundation, components, tiles, layouts | [`design/ontwerp-0.4/`](design/ontwerp-0.4/README.md) |
| README template and the README standard | [`templates/`](templates/) |
| Plan for harmonizing all apps | [`STAPPENPLAN.md`](STAPPENPLAN.md) |
| Overview of the apps | [`APP-OVERZICHT.md`](APP-OVERZICHT.md) |
| All reviews and studies so far | [`UI-HARMONISATIE.md`](UI-HARMONISATIE.md) |

The documents behind these links are in Dutch. Code conventions and the shared issue workflow stay in [`conventions`](https://github.com/OpenAEC-Foundation/conventions), because other repositories call them from there.

## Versions

All OpenAEC tools use **year.week**: `YYYY.W.N`. That is the year, the ISO week without a leading zero, and a number within the week that starts at 0.

| Example | Meaning |
|---------|---------|
| `2026.44.0` | first release in week 44 of 2026 |
| `2026.44.1` | second release in the same week |
| `2026.45.0` | first release of the next week |
| `v2026.44.0` | the matching Git tag and GitHub release |

Dots, not a dash: `2026-44` is not a valid version in npm, Cargo or Tauri. See [#1](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/1). All crates in this repository carry the same number, and the release workflow refuses a tag that does not match. `python scripts/version.py --check` checks this locally, `--set 2026.44.1` sets a number in every crate, and `--next` picks the next number for today.

## Releases and signing

A tag `vYYYY.W.N` starts [`release.yml`](.github/workflows/release.yml): first all repository checks and tests, then the builds and signatures per platform, then the release with release notes. If a key is missing, the release notes say so per file and the release becomes a pre-release. Packaging is in [`packaging/`](packaging/). Open Pointcloud Studio was the example.

## Testing and reliability

- **Eleven repository checks** run before every release: version, layout metrics, icon adoptions, portable UI, crate package, tokens, generated tokens, icon crate, web components, font package and web icons. They are the first step of [`release.yml`](.github/workflows/release.yml).
- **Rust tests** for the whole workspace, and once more for the icon crate with all icons switched on.
- **Generated files are checked, not trusted.** Tokens, icons, web components, fonts, the Tauri template and these README images each have a script with `--check` that fails when the committed file differs from what the source would give.
- **Screens are rendered by the tests.** `cargo test --bin blueprint -- --ignored` writes the screens of the Rust app in four themes to [`design/blueprint/`](design/blueprint/). `node web/online/screenshots.mjs` takes the screens of the browser version.

The full list of checks is in [`AGENTS.md`](AGENTS.md#controles).

## Current limitations

- **The checks run on release, not on every pull request.** There is no separate CI workflow yet.
- **The licence of the B2 icons is still open** ([#15](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/15)). Check it before you ship the icons in another product.
- **Agreements for MCP servers and IFCX are not written yet**, and neither is the ecosystem plan with a schedule.
- **The online version cannot make or save reports.** That needs the Rust side of the desktop app.
- **Some names still say Style Repo.** The repository was called OpenAEC-Style-Repo until 26 October 2026; the binary `style_repo` and some texts have not been renamed. GitHub forwards old links.

Found something? [Open an issue](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues).

## Under the hood

The Rust library is built on [iced](https://iced.rs/) and draws every screen itself, with the same tokens as the web package. The Tauri template uses Tauri 2, React and TypeScript, with Three.js for the 3D view. The online version builds that template unchanged with Vite and replaces only what works differently in a browser: settings in `localStorage`, links in a new tab. The C library is a `cdylib` and `staticlib` from [`openaec-blueprint-sdk`](crates/openaec-blueprint-sdk/), with a header and a C example.

## Contributing

- **Report a problem or an idea** as an [issue](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues). Describe what you did, what you expected and what happened.
- **Building a tool?** Start from the standard application and the [README template](templates/README-tool.md). The requirements for a README are in [`templates/README-standaard.md`](templates/README-standaard.md).
- **Working in this repository**, alone or with an AI assistant: read [`AGENTS.md`](AGENTS.md) and start every task with [`NOTES.md`](NOTES.md).

## Quick start (developers)

```bash
git clone https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint.git
cd OpenAEC-Blueprint
cargo run --bin blueprint
cargo test
```

Rust with the MSVC toolchain on Windows. The scripts in `scripts/` need Python 3. The Tauri template and the online version need Node 22 or later.

OpenAEC Blueprint is part of the [OpenAEC Foundation](https://github.com/OpenAEC-Foundation) family of apps.

## License

The UI library falls under LGPL-3.0-only, with its own licences for the fonts and some vectors; see [`crates/openaec-ui/NOTICE.md`](crates/openaec-ui/NOTICE.md). The rest of this repository falls under CC BY-SA 4.0, see [`LICENSE`](LICENSE). The licence of the B2 icons is still open ([#15](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/15)).
