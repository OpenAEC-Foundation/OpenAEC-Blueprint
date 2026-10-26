# Online standaardapplicatie

De Tauri-standaardapplicatie als gewone webapp, voor issue [#36](https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint/issues/36). Zo kan iedereen in de browser zien hoe een OpenAEC-tool eruitziet, zonder iets te installeren.

**Online:** <https://openaec-foundation.github.io/OpenAEC-Blueprint/>

## Hoe het werkt

De bron is de sjabloon in [`style-book/project-templates/Tauri+React`](../../style-book/project-templates/Tauri+React/). Die wordt niet aangepast: [`build.mjs`](build.mjs) bouwt hem met Vite en vervangt bij het bouwen alleen wat in een browser anders moet.

- **Tauri-functies.** Elke import van `@tauri-apps/*` gaat naar [`tauri-browser.ts`](tauri-browser.ts):
  - instellingen in `localStorage`;
  - losgemaakte weergaven als browservenster, met een `BroadcastChannel` om ze terug te zetten;
  - links in een nieuw tabblad;
  - de knop Maximaliseren schakelt naar volledig scherm.

  Rapporten maken en opslaan kan online niet, want daarvoor is de Rust-kant nodig.
- **Naam en versie.** De sjabloon noemt zich "Open Template" met versie 0.1.0. Online staat er "OpenAEC Blueprint" met de versie uit de hoofd-`Cargo.toml`, gelijk aan de laatste release (`JJJJ.W.N`, #1). Verandert de sjabloon zo dat een vervanging niet meer past, dan stopt de build met een melding.
- **Ontwerp 0.4.** De sjabloon zelf gebruikt de tokens, fonts en B2-iconen van het webpakket (`scripts/sync_tauri_template.py`), dus online geldt hetzelfde.

## Bouwen

```bash
cd style-book/project-templates/Tauri+React
npm ci --ignore-scripts
cd ../../..
node web/online/build.mjs
```

De uitvoer staat in `target/online/`. Met `node web/online/build.mjs --serve` bouw je hem en bekijk je hem op <http://localhost:4173/OpenAEC-Blueprint/>.

## Publiceren

[`.github/workflows/pages.yml`](../../.github/workflows/pages.yml) bouwt en publiceert de site na elke geslaagde release (workflow Release), vanaf de commit van die release. Met de hand starten kan ook, via Actions → Pages → Run workflow. De releaseworkflow zelf blijft ongewijzigd.
