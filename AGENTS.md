# Afspraken voor AI-assistenten

Dit bestand geldt voor elke AI-assistent die in deze repository werkt, zoals ChatGPT/Codex en Claude. Codex leest dit bestand rechtstreeks; Claude leest het via `CLAUDE.md`. Wijzig de afspraken hier, niet in `CLAUDE.md`.

## Over de repository

- Native Rust Style Repo (`cargo run --bin style_repo`) en de afzonderlijk verpakte crate [`crates/openaec-ui`](crates/openaec-ui/).
- `scripts/` bevat Python-scripts die reviews, indexen en atlassen in `design/` en `harmonization/` genereren.
- `harmonization/sources/` en `target/` staan in `.gitignore` en horen nooit in een commit.
- De README is de korte ingang, in het Engels ([`README.md`](README.md)) en het Nederlands ([`README.nl.md`](README.nl.md)) met dezelfde opbouw en beelden; wijzig ze samen. Ze volgen [`templates/README-standaard.md`](templates/README-standaard.md); de beelden in `docs/images/readme/` maak je met `scripts/build_readme_images.py` (bron: renders in `design/`, en `node web/online/screenshots.mjs` voor de browserversie). De details van alle reviews en tussenstappen staan in [`UI-HARMONISATIE.md`](UI-HARMONISATIE.md). Samen zijn ze de inhoudelijke bron van waarheid. Houd ze bij als je iets toevoegt of verandert dat erin beschreven staat; nieuwe reviews en tussenstappen gaan in `UI-HARMONISATIE.md`.

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
- Op de machine van de maker (Windows) staat `core.autocrlf` aan. Maak geen commits die alleen regeleindes veranderen.

## Taal en stijl

- Documentatie, reviews en `NOTES.md` in het Nederlands. Code, identifiers en commitberichten in het Engels. Uitzondering: `README.md` is Engels, met `README.nl.md` als Nederlandse versie.
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
python scripts/generate_icon_crate.py --check
python scripts/build_web_components.py --check
python scripts/build_web_icons.py --check
python scripts/sync_tauri_template.py --check
python scripts/build_font_package.py --check
python scripts/check_font_glyphs.py
python scripts/check_report_pdf.py --self-test
python scripts/version.py --check
python scripts/build_readme_images.py --check
cargo test
cargo test -p openaec-icons --features all
cargo package -p openaec-ui
```

- Op de machine van de maker (Windows) heet de interpreter `python`, niet `python3`. Op Linux heet hij `python3`.
- `scripts/build_font_package.py` (zonder `--check`) en `scripts/build_inter_aec.py` hebben fontTools en brotli nodig: `python -m pip install --target harmonization/sources/font-runtime -r scripts/requirements-fonts.txt`. De `--check` werkt zonder.
- Op de machine van de maker staat Rust in `%USERPROFILE%\.cargo\bin` met de MSVC-toolchain en Visual Studio Build Tools 2022. Een terminal die al openstond vóór 2026-10-16 kent dat pad pas na opnieuw openen. Op Linux staat Rust via rustup in `~/.cargo/bin`.
- `scripts/render_collision_drafts.py` en `scripts/render_domain_icon_review.py` gebruiken PyGObject met librsvg. Die draaien op Linux, niet op de Windows-machine van de maker. Op Debian of Ubuntu: `sudo apt install python3-gi python3-gi-cairo gir1.2-rsvg-2.0 python3-pil`.
- Draai generatiescripts alleen voor het deel waaraan je werkt. Regenereer niet de hele `design/`-map zonder opdracht.
- Meld eerlijk welke controles je wel en niet hebt gedraaid, met de uitkomst.
