# Afspraken voor AI-assistenten

Dit bestand geldt voor elke AI-assistent die in deze repository werkt, zoals ChatGPT/Codex en Claude. Codex leest dit bestand rechtstreeks; Claude leest het via `CLAUDE.md`. Wijzig de afspraken hier, niet in `CLAUDE.md`.

## Over de repository

- Native Rust Style Repo (`cargo run --bin style_repo`) en de afzonderlijk verpakte crate [`crates/openaec-ui`](crates/openaec-ui/).
- `scripts/` bevat Python-scripts die reviews, indexen en atlassen in `design/` en `harmonization/` genereren.
- `harmonization/sources/` en `target/` staan in `.gitignore` en horen nooit in een commit.
- De [README](README.md) is de inhoudelijke bron van waarheid. Houd die bij als je iets toevoegt of verandert dat erin beschreven staat.

## Samenwerken in dezelfde map

1. **Begin altijd met `NOTES.md`.** Lees eerst de secties *Nu bezig* en *Open punten*, en daarna de laatste logregels.
2. **Claim je werk.** Zet onder *Nu bezig* wie je bent, wat je doet en welke bestanden of mappen je aanraakt.
3. **Raak geen geclaimde bestanden aan.** Staat een bestand onder *Nu bezig* bij de andere assistent, laat het dan met rust en meld dit aan de gebruiker.
4. **Lees bestanden opnieuw vlak voor je ze bewerkt.** De andere assistent kan ze intussen hebben gewijzigd.
5. **Rond af in `NOTES.md`.** Haal je claim weg, voeg bovenaan het *Logboek* een korte regel toe en zet onafgemaakt werk onder *Open punten*.
6. **Draai `git status` voor en na je werk.** Wijzigingen die niet van jou zijn, laat je staan en noem je aan de gebruiker.

## Git

- Commit alleen als de gebruiker erom vraagt. Push nooit zelf; de gebruiker pusht via GitHub Desktop.
- Geen `git reset --hard`, force-push, rebase van gedeelde geschiedenis of het weggooien van andermans wijzigingen.
- Commitberichten in het Engels, kort en in de gebiedende wijs, zoals de bestaande geschiedenis (`Add native PDF split-dialog screen review`).
- Vermeld in de commit welke assistent het werk deed als de gebruiker daar om vraagt of als de tool dat standaard doet.
- `core.autocrlf` staat op deze Windows-machine aan. Maak geen commits die alleen regeleindes veranderen.

## Taal en stijl

- Documentatie, reviews en `NOTES.md` in het Nederlands. Code, identifiers en commitberichten in het Engels.
- Volg de bestaande opbouw van een review: bron, concrete UI-aanroep, hash of commit, en een expliciet oordeel.
- Noem iets pas "gedeeld" of "geharmoniseerd" als het echt in de Rust-crate zit. Concepten en reviewmateriaal blijven zo benoemd.
- Controleer licenties van bronassets voordat je ze in `crates/openaec-ui` opneemt.

## Controles

Draai na een wijziging de controles die bij dat deel horen:

```bash
python scripts/check_layout_metrics.py
python scripts/check_icon_adoptions.py
python scripts/check_portable_ui.py
python scripts/check_crate_package.py
python scripts/check_tokens_04.py
python scripts/generate_tokens_04.py --check
cargo test
cargo package -p openaec-ui
```

- Op deze Windows-machine heet de interpreter `python`, niet `python3`.
- Rust staat in `%USERPROFILE%\.cargo\bin` met de MSVC-toolchain en Visual Studio Build Tools 2022. Een terminal die al openstond vóór 2026-10-16 kent dat pad pas na opnieuw openen.
- `scripts/render_collision_drafts.py` en `scripts/render_domain_icon_review.py` gebruiken PyGObject met librsvg. Die draaien op Linux, niet op deze Windows-machine.
- Draai generatiescripts alleen voor het deel waaraan je werkt. Regenereer niet de hele `design/`-map zonder opdracht.
- Meld eerlijk welke controles je wel en niet hebt gedraaid, met de uitkomst.
