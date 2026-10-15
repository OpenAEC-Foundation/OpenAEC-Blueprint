# OpenAEC UI-harmonisatie

Deze repository bevat een volledig in Rust getekende desktop-Style Repo en de afzonderlijk te verpakken [`openaec-ui`-crate](crates/openaec-ui/). De native interface gebruikt `iced` en volgt de regio's, maten, thema's en typografie van de OpenAEC Tauri-template: titelbalk, optionele ribbon of werkstroomnavigatie, documenttabs, werkgebied, status en instellingen. Er is geen React, JavaScript, WebView of Tauri-runtime nodig.

Start de Style Repo met:

```bash
cargo run --bin style_repo
```

De app laat componenten, vijf thema's, de gedeelde layout, 18 studio-indelingen met elk negen selecteerbare voorbeeldschermen, 565 onderzochte UI-iconbestanden en 109 getekende FEM/BIM-iconconcepten zien. De broniconen en domeinconcepten zijn bedoeld voor beoordeling; de 26 iconen in [`crates/openaec-ui/assets/icons/`](crates/openaec-ui/assets/icons/) vormen de huidige semantische kern van de crate. De gelijkgehouden kopie in `assets/icons/` bedient de HTML-review. Thema, taal, schaal en paneelinstellingen worden opgeslagen in de gebruikersconfiguratie.

![Native Rust Style Repo](design/style-repo-native.png)

De native studio-atlas toont de voorgestelde tabs en groepen in de echte Rust-ribbon; Energy gebruikt een afzonderlijke werkstroommodus zonder ribbon. Hij is in alle vijf thema's gerenderd: [Light](design/style-repo-atlas-light.png), [Forge](design/style-repo-atlas-forge.png), [OpenAEC](design/style-repo-atlas-openaec.png), [Blueprint](design/style-repo-atlas-blueprint.png) en [High contrast](design/style-repo-atlas-contrast.png). De native Energy-werkstroom toont nieuwbouw in [Light](design/style-repo-energy-workflow-light.png), [Forge](design/style-repo-energy-workflow-forge.png) en [utiliteit](design/style-repo-energy-workflow-utility-light.png), plus bestaande bouw voor [woning](design/style-repo-energy-workflow-existing-light.png) en [utiliteit](design/style-repo-energy-workflow-existing-utility-forge.png). De [FEM-Geometrie-ribbon](design/style-repo-fem-ribbon-light.png) en [BIM-Modelleren-ribbon](design/style-repo-bim-ribbon-forge.png) tonen de native concept-SVG's. De 109 domeiniconen blijven app-eigen reviewmateriaal en maken geen deel uit van de publieke `Icon::ALL`-set. Deze beelden zijn reproduceerbaar met `cargo test --bin style_repo render_tests::export_native_style_repo_previews -- --ignored`.
De [Planner-ribbon](design/style-repo-planner-ribbon-light.png) is aan de actuele bronregistry gespiegeld: de tabs, groepen en gedeelde acties zijn gecontroleerd; overige Lucide-vormen blijven broniconen ter review. De optionele AI-tab en de horizontale ribbon-scroll zijn zichtbaar.
De [Calc-ribbon](design/style-repo-calc-ribbon-light.png) volgt de echte linttabs en commandogroepen op broncommit b470427; de Nederlandse begroting en het rapport zijn als aparte referenties in de review opgenomen. De tafelinhoud in de atlas is nog een stijlproef.

De [Geotechniek-ribbon](design/style-repo-geotech-ribbon-light.png) volgt de kern- en extensietabs van de actuele bron. Kaart, sonderingsgrafiek en boorprofiel staan als afzonderlijke schermreferenties in de review.

De [Heatloss-ribbon](design/style-repo-heatloss-ribbon-light.png) gebruikt de actuele route-tabs; zijn IFC-lint is bewust leeg. Voor deze app ontbreken nog echte schermcaptures.

De [Calculations-ribbon](design/style-repo-calculations-ribbon-light.png) volgt de twee huidige tabs; zijn IFC-lint is bewust leeg. Ook hier zijn nog geen echte schermcaptures beschikbaar.

De [Reports-ribbon](design/style-repo-reports-ribbon-light.png) volgt de actuele Start-, Invoegen- en Beeld-groepen; echte schermcaptures ontbreken nog in deze bron.

De [BIM Validator-ribbon](design/style-repo-validator-ribbon-light.png) toont de brongecontroleerde Start- en Beeldgroepen in de niet-verbonden BCF-staat.

De [Pile Plan-ribbon in Forge](design/style-repo-pile-ribbon-forge.png) volgt Plan en Weergave; de HTML-review toont de Weergave-sliders als ontwerpproef naast drie echte broncaptures.

De native iconenpagina toont de 26 canonieke Rust-iconen afzonderlijk van de 565 onderzoeksbronnen: [Light](design/style-repo-icons-light.png) en [Forge](design/style-repo-icons-forge.png).
De [componentenpagina in Light](design/style-repo-components-light.png) en [Forge](design/style-repo-components-forge.png) toont de gedeelde primaire, secundaire en uitgeschakelde knoppen, plus een werkende checkbox en slider. Pointcloud tekent ook zijn scrollbalken, tooltips en voortgangsbalken met de stijlfuncties uit dezelfde crate.
De [instellingen in Light](design/style-repo-settings-light.png) en [Forge](design/style-repo-settings-forge.png) tonen de gedeelde keuzelijst- en invoerstijl; Pointcloud gebruikt dezelfde Rust-functies voor velden en het open keuzemenu.

Een andere Rust-tool kan de shell via de `Application`-trait gebruiken. [`examples/studio.rs`](examples/studio.rs) is een klein integratievoorbeeld (`cargo run --example studio`).
Voor bestaande native applicaties met een eigen eventloop biedt [`crates/openaec-ui/src/frame.rs`](crates/openaec-ui/src/frame.rs) dezelfde buitenste bandindeling via `FrameSlots`; Pointcloud Studio gebruikt die adapter voor het volledige venster en behoudt zijn eigen 3D-canvas en commando's.

Open [`design/review.html`](design/review.html) in een browser voor het interactieve overzicht. De 565 via UI-broncode of actieve knopbundels onderbouwde iconbestanden staan in `harmonization/ui-icons/`. Daarnaast zijn 312 geïmporteerde Lucide- en Solid/Tabler-SVG's uit de gebruikte pakketversies bewaard en op light/dark te bekijken in [`design/library-icons.html`](design/library-icons.html). Die vormen blijven een aparte onderzoekscategorie. De [UI-icoonreviewwerkbank](design/icon-review-board.html) toont alle 565 bewezen UI-bestanden op licht en donker in 16/24/32 px en kan lokale ontwerpbesluiten als JSON exporteren. Het [semantische kruisverband](design/icon-semantic-crosswalk.html) koppelt beide categorieën als reviewkandidaten aan de 26 gedeelde iconbetekenissen en toont alle overige broniconen apart. Zes extra broniconen maken de vergelijking in [`design/icon-comparison.html`](design/icon-comparison.html) compleet. De volledige index van 666 gevonden schermbeeldkandidaten, waaronder 145 van Planner Studio, staat in [`design/screen-inventory.html`](design/screen-inventory.html); een gedeelde shell voor 18 studio's, met brongetrouwe Speech-zijbalk en negen gedeelde schermtoestanden voor de 16 overige studio's in [`design/harmonized.html`](design/harmonized.html). De 109 uitgewerkte FEM/BIM-vectorconcepten staan in [`design/domain-icon-atlas.html`](design/domain-icon-atlas.html); tien daarvan hebben ook een vereenvoudigde 16 px-versie. De [FEM/BIM-bronvergelijking](design/domain-candidate-review.html) toont de 54 naamkandidaten bij 24 concepten, met een voorlopig oordeel en direct UI-codebewijs per bronicoon. De concepten zijn in de FEM- en BIM-ribbons geplaatst, maar blijven buiten de publieke icon-API tot de semantische en kleine-maatbeoordeling klaar is. De [Energy-werkstroomreview](design/energy-workflow.html) vergelijkt de actuele routevarianten met een brongepind projectbeeld. De expliciete beoordeling en openstaande ontwerpstappen staan in [`design/assessment.md`](design/assessment.md). Het volledige bronarchief van circa 27.000 visuele bestanden blijft lokaal in `harmonization/sources/` en staat bewust buiten Git; de metadata en herkomst staan in `harmonization/asset-index.json`.

Alle 666 gevonden screenshotkandidaten zijn rechtstreeks uit hun vastgelegde Git-commit gerenderd op [47 schermcontactbladen](design/screen-contact-sheets.html). Het overzicht toont de 472 als applicatiescherm ingedeelde beelden naast handleidingbeelden, mockups, tutorialuitsneden en websitebeelden; historische captures worden niet als bewijs voor de actuele UI behandeld. De [volledige bronindex](design/screen-inventory.html) blijft per bestand doorzoekbaar.

De vijf vaste vensterbanden, 24 px-paneelwerkbalken en de standaardbreedte van beide zijpanelen zijn vastgelegd in [`design/layout-spec.json`](design/layout-spec.json) met een exacte Tauri-broncommit. `python3 scripts/check_layout_metrics.py` vergelijkt de Rust-crate en het HTML-prototype met die maten, en met de lokale Tauri-bron wanneer die naast deze repo staat.
`python3 scripts/check_icon_adoptions.py` controleert de zes iconbesluiten en identieke SVG-inhoud in de lokale Pointcloud-integratie.
`python3 scripts/check_portable_ui.py` vergelijkt de volledige portable crate met deze bron: Rust-code na formattering, alle 28 gebundelde fonts/iconen en de runtime-dependencies.
`python3 scripts/check_crate_package.py` controleert de pakketgrens en `cargo package -p openaec-ui` bouwt de zelfstandige crate uit het verpakte archief. Het pakket bevat 53 bestanden: 11 Rust-bronnen, zes fonts met drie meegeleverde OFL-licentieteksten en 26 canonieke iconen. De Style Repo-app staat als afzonderlijk, niet-publiceerbaar Cargo-package in dezelfde workspace. De 565 onderzoeksiconen, FEM/BIM-concepten en reviewbeelden gaan niet mee in het `openaec-ui`-pakket. Voor gebruik in een andere Git-checkout kan de crate via een Git-dependency of een lokale path-dependency worden toegevoegd; er is nog geen remote voor deze repository ingesteld.

De eerste productintegratie staat in de lokale `open-pointcloud-studio`-checkout op branch `feat/shared-rust-ui`. Daar draait een portable snapshot van deze crate als `native/ui`; de Pointcloud-titelbalk, [tien beoordeelde toolacties en de Extensions-bestandspagina](design/icon-adoptions.json) gebruiken de canonieke iconen, naast de gebundelde lettertypen, knoppen, invoervelden, keuzelijsten, checkboxen, sliders, voortgangsbalken, scrollbalken, tooltips en 77 gedeelde Tauri-kleurvelden per thema. De stevige randkleur voor sliders en voortgangsbalken komt aanvullend uit de vastgelegde Style Book-merktokens. De [Extensions-iconreview](design/extensions-icon-review.html) onderbouwt waarom die pagina een puzzelstuk krijgt in plaats van een 3D-kubus. De vier nieuw beoordeelde navigatie-iconen zijn in de [Light/Forge-review](design/navigation-icon-review.html) op 16, 24 en 32 px naast hun bronvormen gezet. De overige domeinribbon en panelen worden na de visuele en semantische beoordeling verder overgezet.

De [documentbalkreview](design/document-bar-review.html) zet de gepinde Tauri-CSS en de native Light- en Forge-renders naast elkaar. De gedeelde Rust-crate tekent nu de 30 px-band én de 24 px-tabstijl in Style Repo en Pointcloud; vier echte Pointcloud-tabs tonen de integratie. De review benoemt de resterende 1 px-onderrand en de contrastverbetering van de actieve sluitknop.

De [ribbon-groepsreview](design/ribbon-group-review.html) vergelijkt de Tauri-`Ribbon.css` met native Pointcloud- en Style Repo-renders. `widgets::ribbon_group` tekent in beide applicaties dezelfde 94 px-groep, 4 px bovenruimte, 8 px zijruimte, labelregel en rechter scheidslijn. Pointcloud behoudt zijn adaptieve inklapgedrag; de Style Repo toont de groepslabels boven een smalle horizontale scrollbar.

De [eigenschappenreview](design/property-grid-review.html) toont de rechterpanelen van beide native applicaties in Light en Forge. De gedeelde Rust-crate tekent daar 28 px label/waarde-rijen en 24 px sectiekoppen; de domeinvelden en bedieningen blijven van de betreffende applicatie.

De [icoonbotsingreview](design/icon-collision-review.html) maakt 14 paren met exact dezelfde bronbytes zichtbaar. Voor zes paren met verschillende handelingen zijn twaalf onderscheidende vectorconcepten in 16/24/32 px gemaakt; de acht andere paren blijven ter contextbeoordeling. De concepten staan nog buiten de publieke Rust-icoon-API.

## Via GitHub Desktop publiceren

1. Kies **File → Add local repository** en selecteer deze map: `/home/aia04/Documenten/GitHub/OpenAEC-app-kopie`.
2. De lokale startcommit staat al klaar. Kies **Publish repository** in GitHub Desktop.
3. Kies de gewenste eigenaar, repositorynaam en zichtbaarheid. Controleer die keuzes en publiceer.

Latere wijzigingen kun je in GitHub Desktop committen en met **Push origin** versturen. De Git-geschiedenis begint lokaal; er is nog geen GitHub-remote ingesteld. De bestaande repository `OpenAEC-style-book` wordt hierdoor niet gewijzigd.

De lokale map `harmonization/sources/` en Rust-buildmap `target/` staan in `.gitignore`, zodat ze niet per ongeluk meegepusht worden. Controleer licenties van bronassets vóór definitief gebruik in een gedeelde crate.
