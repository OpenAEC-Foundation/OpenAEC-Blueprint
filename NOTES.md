# Overdrachtsnotities

Gedeeld kladblok voor ChatGPT/Codex, Claude en de gebruiker. Werkwijze staat in [`AGENTS.md`](AGENTS.md).

## Nu bezig

<!-- Formaat: - **Assistent** – taak – bestanden/mappen – sinds JJJJ-MM-DD -->

_Niemand._

## Open punten

<!-- Onafgemaakt werk, vragen aan de gebruiker of bekende problemen. Verwijder een punt zodra het klaar is. -->

- Gaan de webachtige tools (Open Field Studio, Open Energy) ook naar de nieuwe Rust-UI, of krijgen ze een webvariant van de stijl?
- Hoe krijgen de communicatie-apps Y-Next en Z-Next de stijl? Y-Next draait op ERPNext (Python/web) en kan de Rust-bibliotheek niet gebruiken.
- Welke licentie krijgt de bibliotheek? Het prototype gebruikt CC-BY-SA-4.0, die niet voor software bedoeld is.
- Waar komt de bibliotheek te staan? De Style Repo is privé, en publieke tools kunnen niet bouwen op een private Git-dependency.

## Besluiten

<!-- Vastgestelde uitgangspunten. Nieuwste bovenaan. Formaat: - JJJJ-MM-DD: besluit (bron). -->

- 2026-10-16: Tools zoals Open Calc Studio worden omgebouwd naar de nieuwe UI (de gebruiker, na overleg met leidinggevende).
- 2026-10-16: Y-Next en Z-Next zijn communicatie-apps, een eigen soort interface naast ribbon-tools, webachtige tools en de installer.
- 2026-10-16: De UI-bibliotheek versie 0.4 wordt vanaf nul opnieuw gebouwd. De huidige crate `openaec-ui` 0.1.0 en de reviews in deze repo dienen als prototype en ontwerpbron.
- Volgorde van het werk: ontwerpen in de Style Repo, dan bibliotheek 0.4 bouwen, dan tools ombouwen, te beginnen met Open Calc Studio.

## Logboek

<!-- Nieuwste bovenaan. Formaat: - JJJJ-MM-DD **Assistent**: wat er gedaan is. -->

- 2026-10-16 **Claude**: `STAPPENPLAN.md` opgesteld voor het nieuwe ontwerp (deel A) en bibliotheek 0.4 (deel B). Rust-build en `cargo test` slagen: 49 geslaagd, 45 bewust overgeslagen.
- 2026-10-16 **Claude**: Rust bleek al geïnstalleerd en is aan het gebruikerspad toegevoegd. `scripts/check_crate_package.py` werkt nu ook met Windows-paden. De vier Python-controles slagen.
- 2026-10-16 **Claude**: uitleg van de leidinggevende en de antwoorden van de gebruiker vastgelegd onder *Besluiten* en *Open punten*; eerste stappenplan in de chat opgesteld.
- 2026-10-16 **Claude**: repository gekloond en `AGENTS.md`, `CLAUDE.md` en `NOTES.md` toegevoegd met de samenwerkingsafspraken.
