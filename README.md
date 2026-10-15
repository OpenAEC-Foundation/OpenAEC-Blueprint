# OpenAEC UI-harmonisatie

Deze repository bevat een volledig in Rust getekende desktop-Style Repo en de afzonderlijk te verpakken [`openaec-ui`-crate](crates/openaec-ui/). De native interface gebruikt `iced` en volgt de regio's, maten, thema's en typografie van de OpenAEC Tauri-template: titelbalk, ribbon, documenttabs, verkenner, werkgebied, eigenschappen, status en instellingen. Er is geen React, JavaScript, WebView of Tauri-runtime nodig.

Start de Style Repo met:

```bash
cargo run --bin style_repo
```

De app laat componenten, vijf thema's, de gedeelde layout, 18 studio-indelingen met elk negen selecteerbare voorbeeldschermen, 565 onderzochte UI-iconbestanden en 109 getekende FEM/BIM-iconconcepten zien. De broniconen en domeinconcepten zijn bedoeld voor beoordeling; de 22 iconen in [`crates/openaec-ui/assets/icons/`](crates/openaec-ui/assets/icons/) vormen de huidige semantische kern van de crate. De gelijkgehouden kopie in `assets/icons/` bedient de HTML-review. Thema, taal, schaal en paneelinstellingen worden opgeslagen in de gebruikersconfiguratie.

![Native Rust Style Repo](design/style-repo-native.png)

De native studio-atlas is in alle vijf thema's gerenderd: [Light](design/style-repo-atlas-light.png), [Forge](design/style-repo-atlas-forge.png), [OpenAEC](design/style-repo-atlas-openaec.png), [Blueprint](design/style-repo-atlas-blueprint.png) en [High contrast](design/style-repo-atlas-contrast.png). Deze beelden zijn reproduceerbaar met `cargo test --bin style_repo render_tests::export_native_style_repo_previews -- --ignored`.
De native iconenpagina toont de 22 canonieke Rust-iconen afzonderlijk van de 565 onderzoeksbronnen: [Light](design/style-repo-icons-light.png) en [Forge](design/style-repo-icons-forge.png).
De [componentenpagina in Light](design/style-repo-components-light.png) en [Forge](design/style-repo-components-forge.png) toont de gedeelde primaire, secundaire en uitgeschakelde knoppen, plus een werkende checkbox en slider. Pointcloud tekent ook zijn scrollbalken, tooltips en voortgangsbalken met de stijlfuncties uit dezelfde crate.
De [instellingen in Light](design/style-repo-settings-light.png) en [Forge](design/style-repo-settings-forge.png) tonen de gedeelde keuzelijst- en invoerstijl; Pointcloud gebruikt dezelfde Rust-functies voor velden en het open keuzemenu.

Een andere Rust-tool kan de shell via de `Application`-trait gebruiken. [`examples/studio.rs`](examples/studio.rs) is een klein integratievoorbeeld (`cargo run --example studio`).
Voor bestaande native applicaties met een eigen eventloop biedt [`crates/openaec-ui/src/frame.rs`](crates/openaec-ui/src/frame.rs) dezelfde buitenste bandindeling via `FrameSlots`; Pointcloud Studio gebruikt die adapter voor het volledige venster en behoudt zijn eigen 3D-canvas en commando's.

Open [`design/review.html`](design/review.html) in een browser voor het interactieve overzicht. De 565 via UI-broncode of actieve knopbundels onderbouwde iconbestanden staan in `harmonization/ui-icons/`. Daarnaast zijn 312 geïmporteerde Lucide- en Solid/Tabler-SVG's uit de gebruikte pakketversies bewaard en op light/dark te bekijken in [`design/library-icons.html`](design/library-icons.html). Die vormen blijven een aparte onderzoekscategorie. Het [semantische kruisverband](design/icon-semantic-crosswalk.html) koppelt beide categorieën als reviewkandidaten aan de 22 gedeelde iconbetekenissen en toont alle overige broniconen apart. Zes extra broniconen maken de vergelijking in [`design/icon-comparison.html`](design/icon-comparison.html) compleet. De volledige index van 436 gevonden schermbeeldkandidaten staat in [`design/screen-inventory.html`](design/screen-inventory.html); een gedeelde shell voor 18 studio's en negen schermtoestanden in [`design/harmonized.html`](design/harmonized.html). De 109 uitgewerkte FEM/BIM-vectorconcepten staan in [`design/domain-icon-atlas.html`](design/domain-icon-atlas.html); tien daarvan hebben ook een vereenvoudigde 16 px-versie. Ze zijn in de FEM- en BIM-ribbons geplaatst, maar blijven buiten de publieke icon-API tot de semantische en kleine-maatbeoordeling klaar is. De expliciete beoordeling en openstaande ontwerpstappen staan in [`design/assessment.md`](design/assessment.md). Het volledige bronarchief van circa 27.000 visuele bestanden blijft lokaal in `harmonization/sources/` en staat bewust buiten Git; de metadata en herkomst staan in `harmonization/asset-index.json`.

De vijf vaste vensterbanden, 24 px-paneelwerkbalken en de standaardbreedte van beide zijpanelen zijn vastgelegd in [`design/layout-spec.json`](design/layout-spec.json) met een exacte Tauri-broncommit. `python3 scripts/check_layout_metrics.py` vergelijkt de Rust-crate en het HTML-prototype met die maten, en met de lokale Tauri-bron wanneer die naast deze repo staat.
`python3 scripts/check_icon_adoptions.py` controleert de zes iconbesluiten en identieke SVG-inhoud in de lokale Pointcloud-integratie.
`python3 scripts/check_portable_ui.py` vergelijkt de volledige portable crate met deze bron: Rust-code na formattering, alle 28 gebundelde fonts/iconen en de runtime-dependencies.
`python3 scripts/check_crate_package.py` controleert de pakketgrens en `cargo package -p openaec-ui` bouwt de zelfstandige crate uit het verpakte archief. Het pakket bevat 49 bestanden: 11 Rust-bronnen, zes fonts met drie meegeleverde OFL-licentieteksten en 22 canonieke iconen. De Style Repo-app staat als afzonderlijk, niet-publiceerbaar Cargo-package in dezelfde workspace. De 565 onderzoeksiconen, FEM/BIM-concepten en reviewbeelden gaan niet mee in het `openaec-ui`-pakket. Voor gebruik in een andere Git-checkout kan de crate via een Git-dependency of een lokale path-dependency worden toegevoegd; er is nog geen remote voor deze repository ingesteld.

De eerste productintegratie staat in de lokale `open-pointcloud-studio`-checkout op branch `feat/shared-rust-ui`. Daar draait een portable snapshot van deze crate als `native/ui`; de Pointcloud-titelbalk, [zes beoordeelde toolacties en de Extensions-bestandspagina](design/icon-adoptions.json) gebruiken de canonieke iconen, naast de gebundelde lettertypen, knoppen, invoervelden, keuzelijsten, checkboxen, sliders, voortgangsbalken, scrollbalken, tooltips en 77 gedeelde Tauri-kleurvelden per thema. De stevige randkleur voor sliders en voortgangsbalken komt aanvullend uit de vastgelegde Style Book-merktokens. De [Extensions-iconreview](design/extensions-icon-review.html) onderbouwt waarom die pagina een puzzelstuk krijgt in plaats van een 3D-kubus. De overige domeinribbon en panelen worden pas na de visuele en semantische beoordeling volledig overgezet.

## Via GitHub Desktop publiceren

1. Kies **File → Add local repository** en selecteer deze map: `/home/aia04/Documenten/GitHub/OpenAEC-app-kopie`.
2. De lokale startcommit staat al klaar. Kies **Publish repository** in GitHub Desktop.
3. Kies de gewenste eigenaar, repositorynaam en zichtbaarheid. Controleer die keuzes en publiceer.

Latere wijzigingen kun je in GitHub Desktop committen en met **Push origin** versturen. De Git-geschiedenis begint lokaal; er is nog geen GitHub-remote ingesteld. De bestaande repository `OpenAEC-style-book` wordt hierdoor niet gewijzigd.

De lokale map `harmonization/sources/` en Rust-buildmap `target/` staan in `.gitignore`, zodat ze niet per ongeluk meegepusht worden. Controleer licenties van bronassets vóór definitief gebruik in een gedeelde crate.
