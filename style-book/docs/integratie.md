# Huisstijl gebruiken in een OpenAEC-app

Eén versienummer voor alles: gebruik in een app overal dezelfde versie.

## Categorie 1 — iced (Rust)

```toml
[dependencies]
openaec-tokens = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-icons  = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-i18n   = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-ribbon = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
```

`ribbon.toml` controleren:
```bash
cargo install --git https://github.com/OpenAEC-Foundation/OpenAEC-style-book --tag v0.1.0 openaec-ribbon
openaec-ribbon check ribbon.toml --nl src/i18n/nl.json --en src/i18n/en.json
```

## Categorie 2 en 4 — React

```bash
npm install @openaec/design-tokens@0.1.0 @openaec/icons@0.1.0 @openaec/i18n@0.1.0
```

## Categorie 3 — Frappe

```bash
bench get-app https://github.com/OpenAEC-Foundation/openaec_theme --branch v0.1.0
bench --site <site> install-app openaec_theme
```

## App-logo's

Download `openaec-logos-v0.1.0.zip` bij de GitHub Release en neem de map van je
app over (`icon.ico`, `icon.icns`, `icon-*.png`, favicons, lockups). Staat je app
niet in `design/apps.toml` of heeft hij nog geen pictogram: zie `design/README.md`.

## Lokaal tegelijk aan stijlbook en app werken

Rust — in de `Cargo.toml` van de app:
```toml
[patch."https://github.com/OpenAEC-Foundation/OpenAEC-style-book"]
openaec-icons = { path = "../OpenAEC-style-book/crates/openaec-icons" }
```

npm — in de `package.json` van de app:
```json
"overrides": { "@openaec/icons": "file:../OpenAEC-style-book/packages/icons" }
```
