# openaec-icons

De B2-iconen van OpenAEC UI 0.4, getekend door Codex, als getypte Rust-lijst. Elk icoon heeft een master van 16 px en van 24 px, opgeslagen als gzip-gecomprimeerde SVG. De bestanden zijn byte voor byte gelijk aan `design/icon-set-b2/library-lossless`.

## Gebruik

Zet alleen de feature van je eigen app aan. Dan komen alleen die iconen in de binary, en is een icoon van een andere app een compileerfout.

```toml
[dependencies]
openaec-icons = { path = "../openaec-icons", features = ["pdf"] }
```

```rust
use openaec_icons::{Icon, Size};

let svg: &'static str = Icon::FileSave.svg(Size::S16);
let glyph = openaec_ui::design::widgets::glyph(svg, 16.0, color, accent);
```

- `svg(Size)` pakt het icoon één keer uit en bewaart de tekst; `svg_for(px)` kiest de master bij een maat (16 tot en met 18 px, daarboven 24).
- `id()`, `label()` en `group()` geven het functie-id, het Nederlandse label en de groep uit de B2-set; `Icon::from_id("file.save")` werkt andersom.
- De hoofdkleur is `currentColor` en het accent `var(--icon-accent, currentColor)`, zoals `glyph` verwacht.

Features: `calc`, `calculations`, `composer`, `energy`, `field`, `frame`, `geotechniek`, `heatloss`, `installer`, `pdf`, `pile-plan`, `planner`, `pointcloud`, `reports`, `speech`, `validator` en `all`.

## Bijwerken

Deze crate wordt gegenereerd. Pas niets met de hand aan, maar draai na een nieuwe export van Codex:

```bash
python scripts/generate_icon_crate.py
python scripts/generate_icon_crate.py --check
cargo test -p openaec-icons --features all
```

## Licentie

Voorlopig LGPL-3.0-only, net als `openaec-ui`. De licentie van de iconen is nog niet besloten; zie `NOTES.md`.
