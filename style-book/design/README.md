# design/ — de enige bron

Alles in deze map wordt met de hand bewerkt. Alles daarbuiten in `packages/`,
`crates/`, `frappe/` en `logos/` dat met `@generated` begint of door
`npm run generate` wordt gemaakt, bewerk je **niet** met de hand.

| Map | Inhoud | Gaat naar |
|---|---|---|
| `tokens/` | kleuren, typografie, maten | `@openaec/design-tokens`, `openaec-tokens`, Frappe-thema |
| `icons/` + `icons.toml` | iconen (24×24, `currentColor`) | `@openaec/icons`, `openaec-icons` |
| `i18n/` | gedeelde termen nl/en | `@openaec/i18n`, `openaec-i18n` |
| `ribbons/` | gedeelde ribbon-tabs | `openaec-ribbon` |
| `logos/foundation/` | OpenAEC-logo en -symbool | brandbook-exports, Frappe-thema |
| `logos/apps/` | pictogram per app | logo-sets in de release-zip |
| `fonts/` | Space Grotesk, Inter, JetBrains Mono (OFL) | Frappe-thema |
| `components/` | componentspecificaties | iced- en React-implementaties |
| `apps.toml` | register van alle apps | logo's, uitrol |

## Een icoon toevoegen

1. Zet `design/icons/<domein>/<naam>.svg` neer: viewBox `0 0 24 24`, lijnen en
   vlakken in `currentColor`.
2. Voeg in `design/icons/icons.toml` een `[[icon]]`-blok toe met `id`,
   `label = { nl, en }`, `tags` en `source = "openaec"`.
3. `npm run generate` en `npm test`; voor de Rust-snapshots eenmalig
   `UPDATE_SNAPSHOTS=1 cargo test -p openaec-icons`.
4. Overgenomen iconen uit een open-source set: zet `source` op de naam van de set en
   leg de licentietekst vast als `design/icons/LICENSE-<set>.txt` (gaat automatisch mee
   in `@openaec/icons` en `openaec-icons`). Nu: Lucide (ISC/MIT) voor de UI-basisset.
5. PR openen. Na merge en release krijgen alle apps het icoon via hun versie-update.
