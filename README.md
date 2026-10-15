# OpenAEC UI-harmonisatie

Deze repository bevat een volledig in Rust getekende desktop-Style Repo en een herbruikbare `openaec-ui`-crate. De native interface gebruikt `iced` en volgt de regio's, maten, thema's en typografie van de OpenAEC Tauri-template: titelbalk, ribbon, documenttabs, verkenner, werkgebied, eigenschappen, status en instellingen. Er is geen React, JavaScript, WebView of Tauri-runtime nodig.

Start de Style Repo met:

```bash
cargo run --bin style_repo
```

De app laat componenten, vijf thema's, de gedeelde layout, 18 studio-indelingen, 565 onderzochte UI-iconbestanden en 109 getekende FEM/BIM-iconconcepten zien. De broniconen en domeinconcepten zijn bedoeld voor beoordeling; de 21 iconen in `assets/icons/` vormen de huidige semantische kern van de crate. Thema, taal, schaal en paneelinstellingen worden opgeslagen in de gebruikersconfiguratie.

![Native Rust Style Repo](design/style-repo-native.png)

Een andere Rust-tool kan de shell via de `Application`-trait gebruiken. [`examples/studio.rs`](examples/studio.rs) is een klein integratievoorbeeld (`cargo run --example studio`).
Voor bestaande native applicaties met een eigen eventloop biedt [`src/frame.rs`](src/frame.rs) dezelfde buitenste bandindeling via `FrameSlots`; Pointcloud Studio gebruikt die adapter voor het volledige venster en behoudt zijn eigen 3D-canvas en commando's.

Open [`design/review.html`](design/review.html) in een browser voor het interactieve overzicht. De 565 via UI-broncode of actieve knopbundels onderbouwde iconbestanden staan in `harmonization/ui-icons/`. Daarnaast zijn 312 geïmporteerde Lucide- en Solid/Tabler-SVG's uit de gebruikte pakketversies bewaard en op light/dark te bekijken in [`design/library-icons.html`](design/library-icons.html). Die vormen blijven een aparte onderzoekscategorie. Het [semantische kruisverband](design/icon-semantic-crosswalk.html) koppelt beide categorieën als reviewkandidaten aan de 21 gedeelde iconbetekenissen en toont alle overige broniconen apart. Zes extra broniconen maken de vergelijking in [`design/icon-comparison.html`](design/icon-comparison.html) compleet. De volledige index van 436 gevonden schermbeeldkandidaten staat in [`design/screen-inventory.html`](design/screen-inventory.html); een gedeelde shell voor 18 studio's en negen schermtoestanden in [`design/harmonized.html`](design/harmonized.html). De 109 uitgewerkte FEM/BIM-vectorconcepten staan in [`design/domain-icon-atlas.html`](design/domain-icon-atlas.html); tien daarvan hebben ook een vereenvoudigde 16 px-versie. Ze zijn in de FEM- en BIM-ribbons geplaatst, maar blijven buiten de publieke icon-API tot de semantische en kleine-maatbeoordeling klaar is. De expliciete beoordeling en openstaande ontwerpstappen staan in [`design/assessment.md`](design/assessment.md). Het volledige bronarchief van circa 27.000 visuele bestanden blijft lokaal in `harmonization/sources/` en staat bewust buiten Git; de metadata en herkomst staan in `harmonization/asset-index.json`.

De vijf vaste vensterbanden en de standaardbreedte van beide zijpanelen zijn vastgelegd in [`design/layout-spec.json`](design/layout-spec.json) met een exacte Tauri-broncommit. `python3 scripts/check_layout_metrics.py` vergelijkt de Rust-crate en het HTML-prototype met die maten, en met de lokale Tauri-bron wanneer die naast deze repo staat.
`python3 scripts/check_icon_adoptions.py` controleert de zes iconbesluiten en identieke SVG-inhoud in de lokale Pointcloud-integratie.

De eerste productintegratie staat in de lokale `open-pointcloud-studio`-checkout op branch `feat/shared-rust-ui`. Daar draait een portable snapshot van deze crate als `native/ui`; de Pointcloud-titelbalk en [zes beoordeelde ribbonacties](design/icon-adoptions.json) gebruiken de canonieke iconen, naast de gebundelde lettertypen en 77 gedeelde kleurvelden per thema. De overige domeinribbon en panelen worden pas na de visuele en semantische beoordeling volledig overgezet.

## Via GitHub Desktop publiceren

1. Kies **File → Add local repository** en selecteer deze map: `/home/aia04/Documenten/GitHub/OpenAEC-app-kopie`.
2. De lokale startcommit staat al klaar. Kies **Publish repository** in GitHub Desktop.
3. Kies de gewenste eigenaar, repositorynaam en zichtbaarheid. Controleer die keuzes en publiceer.

Latere wijzigingen kun je in GitHub Desktop committen en met **Push origin** versturen. De Git-geschiedenis begint lokaal; er is nog geen GitHub-remote ingesteld. De bestaande repository `OpenAEC-style-book` wordt hierdoor niet gewijzigd.

De lokale map `harmonization/sources/` en Rust-buildmap `target/` staan in `.gitignore`, zodat ze niet per ongeluk meegepusht worden. Controleer licenties van bronassets vóór definitief gebruik in een gedeelde crate.
