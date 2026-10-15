# Visuele beoordeling · OpenAEC UI

Status: ontwerpbeoordeling van de huidige geharmoniseerde shell, 15 oktober 2026.
Dit document beoordeelt het ontwerp, niet de volledigheid van een toekomstige
migratie van alle OpenAEC-applicaties.

## Bronnen en zekerheid

- 68 repositoryrecords zijn geïnventariseerd: 63 publieke OpenAEC-repositories,
  de externe OpenCADStudio en vier niet toegankelijke of niet gevonden namen.
- 666 beeldverwijzingen zijn op commit vastgelegd in `screen-index.json`;
  645 hebben een unieke Git-blobinhoud en 472 zijn als mogelijke
  applicatieschermen geclassificeerd. De classificatie
  bewijst niet dat het unieke pagina's of huidige productiestaten zijn.
- 565 bestanden hebben een concrete UI-codeverwijzing of de actieve
  pyRevit-knopbundelconventie. De overige SVG's, CAD-symbolen, illustraties en
  technische tekeningen horen niet bij die telling.
- 686 iconimports in broncode verwijzen naar 219 pakket/naamcombinaties.
  Daarvan zijn 312 versiegebonden SVG's uit Lucide Static en Solid Icons
  gedownload; deze categorie is apart geïndexeerd en visueel vergelijkbaar.
  Op de vastgelegde broncommits zijn alle 686 importvoorkomens ook na de import
  aangetroffen: 608 rechtstreeks als JSX-tag en 78 als identifier die onder meer
  via een variabele of componentprop wordt doorgegeven. Bij de 312
  pakketversiegebonden vormen hebben 287 een directe JSX-verwijzing en 25 alleen
  een indirecte. De [bibliotheekicoonreview](library-icons.html) filtert deze
  bewijsvormen en linkt naar de gebruiksregel; statisch bronbewijs garandeert
  geen zichtbaarheid in iedere applicatietoestand.
- De [UI-icoonreviewwerkbank](icon-review-board.html) beperkt de standaardlijst tot de 565 bronbewezen UI-bestanden uit vijf repositories. Elk origineel staat op lichte en donkere ondergrond; 16, 24 en 32 px zijn omschakelbaar. Een besluit per item blijft lokaal in de browser en is als JSON exporteerbaar. Tien beoordeelde Pointcloud-adopties zijn apart gemarkeerd; naamovereenkomsten zijn nog geen goedkeuring.
- De [icoonbotsingreview](icon-collision-review.html) vergelijkt 14 exacte SHA-256-dubbelparen binnen deze 565 UI-bestanden. Zes paren representeren aantoonbaar verschillende handelingen; daarvoor zijn 12 nieuwe SVG-concepten getekend en in 16, 24 en 32 px op licht en donker bekeken. De overige acht paren zijn mogelijk bewuste hergebruikgevallen en vragen een contextbesluit. De voorstellen blijven buiten de publieke Rust-icoon-API totdat de visuele en semantische beoordeling is afgerond.
- De [schermcontactbladen](screen-contact-sheets.html) laten alle 666 geïnventariseerde beeldkandidaten naast elkaar zien, rechtstreeks uit hun vastgelegde Git-objecten gerenderd: 47 bladen en nul leesfouten. Van de 666 zijn 472 als mogelijk applicatiescherm ingedeeld. Vele beelden zijn historische states, detailuitsneden of testcaptures; hun aanwezigheid in een huidige repository maakt ze nog geen actuele UI-bron. De huidige schermstructuur wordt daarom tegen implementatiecode en recente native captures beoordeeld.
- De [naamgenotenreview](icon-name-review.html) vergelijkt 80 exacte naamgroepen met 189 UI-onderbouwde vormen uit meerdere tools, buiten de 26 gedeelde kernbetekenissen. 26 groepen zijn aan de hand van hun bronregels beoordeeld: achttien bevatten verschillende handelingen en acht verwante handelingen; 54 groepen wachten nog op contextbeoordeling. Zo blijkt `Download` in Pointcloud import te betekenen, maar in Planner, de AEC-extensie en BCF export. De twee groepen met identieke bronbytes (`solid`, `sphere`) blijken zelfs verschillende handelingen te representeren en krijgen daarom geen gedeelde commando-ID. De [beoordelingsdata](icon-name-review.json) bewaart alle kandidaatvormen, bronlinks, 189 ingelezen gebruiksfragmenten en statussen; geen fragment mist een leesbare vastgelegde bronregel.
- De [FEM/BIM-bronvergelijking](domain-candidate-review.html) toetst alle 54 bestandsnaamkandidaten bij 24 van de 109 iconconcepten aan hun UI-broncodeverwijzing. De voorlopige broncontextbeoordeling vindt 11 dezelfde betekenissen, 28 verwante maar andere commando's en 15 naamtoevallen. `zoom_window` is bijvoorbeeld geen BIM-raam; een Pointcloud-snedebox is geen FEM-profiel. De [beoordelingsdata](domain-candidate-assessment.json) legt per kandidaat de reden vast en valideert dat geen kandidaat stilzwijgend wegvalt bij een nieuwe inventaris. Een iconregistry kan varianten noemen die niet in een huidig scherm zichtbaar zijn. Dit is geen hergebruik- of licentiebesluit: de bronvormen moeten nog op alle gevraagde maten en thema's tegen de concepten worden gewogen.
- Het [semantische kruisverband](icon-semantic-crosswalk.html) vergelijkt de
  26 huidige gedeelde iconbetekenissen met 565 bewezen UI-bestanden en 312
  versiegebonden bibliotheekvarianten. 90 naamovereenkomsten zijn kandidaten;
  787 items blijven buiten de kern of vragen een domeinspecifieke betekenis.
  Dit is geen goedkeuring van vorm of functie. Tien Pointcloud-toolacties hebben na
  controle van hun commandobetekenis een expliciet
  [adoptiebesluit](icon-adoptions.json): Open, Export, Fit, Undo, Redo, Save, Zoom in, Zoom out, Pan en Fit selection. De vier geharmoniseerde [navigatievectoren](navigation-icon-review.html) zijn op 16/24/32 px in Light en Forge beoordeeld.
  Refresh LOD gebruikt nu zijn eigen Update-symbool in plaats van Fit.
  De Extensions-bestandspagina heeft een [eigen iconreview](extensions-icon-review.html):
  een nieuw getekend puzzelstuk vervangt de semantisch onjuiste 3D-kubus.
- De eerste visuele vergelijking gebruikt het Tauri Style Book, PDF Studio v2,
  Pointcloud native en de 62 lokaal bewaarde visuele referenties. De
  interactieve index laat de andere bronbeelden per repository inspecteren.
- De Planner-audit omvat nu 145 brongepinde schermkandidaten, waaronder 142
  beelden onder `artifacts/` die de eerdere padfilter miste. Acht uiteenlopende
  licht/donkerbeelden zijn lokaal bewaard; de Gantt- en profieldialoogbeelden
  zijn visueel bekeken. De huidige ribbonregistry bevestigt
  Start, Planning, Resources, Weergave, Instellingen, Tabel, IFC en Rapport;
  AI is alleen zichtbaar wanneer de AI-modus aanstaat. De concepttabs en
  linker paneelbeschrijving zijn daarop aangepast.
- De tweede padaudit vond 29 beelden in de NTA 8800-handleiding van Energy
  Studio, 11 aparte redesign-mockups, 40 Planner Extensions-tutorialuitsneden
  en het [OpenCAD-werkruimtescherm](../harmonization/references/OpenCADStudio/site/workspace.png).
  Voorbeelden zijn het [huidige Energy-projectoverzicht](../harmonization/references/open-energy-studio/docs/handleiding-nta8800/img/projectoverzicht.png)
  en het [Energy-ontwerpsysteem](../harmonization/references/open-energy-studio/docs/ui-redesign/mockups/00-designsystem.png).
  De screenshot toont een navigatiesidebar en een dataformulier zonder ribbon;
  de ribbon in het algemene HTML-overzicht is dus een vergelijkingsvoorstel
  en geen pixelgetrouwe reconstructie van de huidige UI. De mockup is een concept,
  niet een opgeleverde applicatietoestand. De Planner-beelden tonen vooral
  detailuitsneden van de Gantt in tutorials, geen 40 unieke vensters.
- `dynlex` en `feat/rust-native` van PDF Studio waren niet publiek beschikbaar
  bij de bronaudit. PDF Studio v3 is als afzonderlijke Slint-bron meegenomen.

Open Speech Studio is op commit `4e8aa6176ae3` opnieuw beoordeeld. Acht echte screenshots onder `Socials/` tonen Speech, Transcribe, Meeting, Mic Test, Models, Dictionary, Settings en About. `src/App.tsx` en `src/components/Sidebar.tsx` bevestigen een zijbalk met negen routes (inclusief Text To Speech), zonder ribbon, documenttabs of permanent eigenschappenpaneel. De Rust-atlas en HTML-proef tonen daarom een zijbalkvariant en de broncaptures (zie [native review](style-repo-speech-sidebar-forge.png)); de inhoud is nog geen pixelgetrouwe Rust-herbouw.

Open PDF Studio is op commit `f754cb7c9d9a` tegen de Solid-componenten `Ribbon.jsx`, negen tabcomponenten en de Nederlandse ribbon-locale gecontroleerd. De zichtbare hoofdstructuur is Bestand, Start, Beeld, Tekenen, Annotatie, PDF bewerken & samenvoegen en Help; Opmaak, Schikken en Afbeelding zijn contextueel. De oude `measure`-tab-ID activeert Annotatie. De [native PDF-review](style-repo-pdf-ribbon-forge.png) en HTML-proef nemen de brongepinde groepsnamen over; keuzeregelaars in contexttabs zijn in Rust voorlopig gelabelde placeholders. De lokaal bewaarde `drawing-tools.jpg` toont versie 2.0.0 en is een historische visuele referentie. `dynlex` en `feat/rust-native` waren niet publiek toegankelijk bij de audit, zodat hiervoor geen brongetrouwe claim wordt gedaan.

De huidige native Pointcloud-bron op lokale branch `feat/shared-rust-ui` (`native/desktop/src/main.rs`, gecontroleerd op `3ce530c`) heeft `RibbonTab::CORE = [Start]`, naast de Bestand-weergave. De tien Start-panelen zijn in de Nederlandse locale Bestand, Navigatie, Selectie, Snedebox, Oppervlak, Tekening, Meten, Annotatie, Index en Export. View-cube-bediening zit buiten de ribbon. Oudere screenshots tonen nog Beeld/Selecteren/Tools; die zijn historisch en bepalen de huidige tabtaxonomie niet. De [native atlasrender](style-repo-pointcloud-ribbon-forge.png) controleert labels, volgorde en iconbetekenissen; de echte Pointcloud-ribbon gebruikt compactere stapels en is dus nog niet pixelgelijk aan de generieke crate-ribbon.

De statusband is nu als `openaec_ui::frame::status_bar` in de gedeelde Rust-crate ondergebracht en wordt door de Style Repo-shell én Pointcloud gebruikt. Pointcloud behoudt de contextafhankelijke tellingen, zichtnaam, RAM, importannulering en compacte weergave; de crate tekent de 22 px-band met bovenrand en themakleuren. De vijf Pointcloud-statusbalktests en de vijf-thema-shelltest slagen. Alle zes opnieuw gerenderde Pointcloud-beelden zijn bytegelijk aan de eerdere beelden, inclusief Light en Forge met lege en geopende scan en de Extensions-pagina.

De 30 px-documentband wordt door de crate getekend volgens de gepinde Tauri-`DocumentBar.css`: 1 px boven- en onderrand, 4 px zijruimte en het thematische achtergrondtoken. Transparante CSS-randkleuren zijn vooraf met de documentachtergrond gemengd; een native pixeltest controleert de exacte Light- en Forge-randkleuren. De individuele tabstijl is nu eveneens gedeeld: 24 px hoogte, 1 px tussenruimte, actieve accent-soft-achtergrond en thematische omtrek. De [documentbalkreview](document-bar-review.html) vergelijkt vier echte Pointcloud-tabs met de CSS-reconstructie. Pointcloud behoudt tabidentiteit, middenklik, sluiting, ellipsis, scrollpositie en toetsenbordnavigatie; zeventien tabtests slagen. De actieve sluitknop houdt volle tekstkleur voor contrast. Een gedeelde 2 px-maskerlaag maakt nu ook in de native tab de onderrand transparant. Een renderregressietest controleert de actieve tab in Light en Forge op de exacte onderrandpixels. De sluitknop blijft voor contrast bewust helderder dan in de CSS-bron. De volledige huidige Pointcloud-suite sluit af met 686 geslaagde tests, nul fouten en drie genegeerde tests.

De ribbon-groepen gebruiken nu in beide Rust-applicaties `openaec_ui::widgets::ribbon_group`. De [bronvergelijking](ribbon-group-review.html) toont de gepinde Tauri-`Ribbon.css` naast de native Light- en Forge-renders: 94 px ribbon, 4 px bovenruimte, 8 px zijruimte, een 9 px-hoofdletterlabel met bovenregel en een rechter scheidslijn. De Pointcloud-pixeltest controleert de scheidslijn op y=64–153 en de labelregel op y=133. De Style Repo gebruikt een smalle horizontale scrollbar zodat de labels van lange ribbons zichtbaar blijven. De knoppen zelf verschillen nog per app: Pointcloud houdt compacte domeinclusters, de showroom catalogusknoppen. De volledige Pointcloud-suite sloot af met 684 geslaagde tests, nul fouten en drie genegeerde tests.

Het [eigenschappenpaneel in Light en Forge](property-grid-review.html) gebruikt nu in beide native applicaties dezelfde `openaec_ui::widgets::property_grid_row_with`, `property_grid_control_with` en `property_section_with`. De 28 px-rijen delen de 5:6 label/waarde-uitlijning en onderregel; 24 px-sectiekoppen gebruiken de themakleuren. De Style Repo toont de gedeelde rijen met catalogusmetadata. Pointcloud houdt de domeinvelden, vertalingen en interactieve invoer lokaal en levert die aan de gedeelde grid. De Tauri Style Book-bron definieert geen volledige property-gridmaatvoering; dit is een harmonisatievoorstel, te toetsen bij langere labels en smalle vensters. Het bestaande OpenCADStudio-afgeleide Pointcloud-bestand blijft in die applicatie; de nieuwe crate-implementatie is zelfstandig geschreven. De volledige Pointcloud-suite had 684 geslaagde tests en drie genegeerde tests; een aanvullend renderonderzoek bevestigt de 28 px-rijafstand in Light en Forge.

OpenCADStudio is op commit `77f19dafd017` tegen `src/modules/registry.rs`, `src/ui/ribbon/mod.rs` en de Nederlandse locale gecontroleerd. De kernribbon toont Tekenen, Parametrisch, Model, Invoegen, Annoteren, Beeld en Beheren. De geregistreerde Layout-module wordt expliciet uit de tabrij gefilterd en gebruikt de zijwerkbalk; plug-ins kunnen extra tabs toevoegen. De [native CAD-review](style-repo-cad-canvas-forge.png) toont de brongepinde groepsnamen en een compacte commandoselectie, met het eigenschappenpaneel links. De websitecapture is mogelijk ouder dan de bronregistry en dient als beeldreferentie, niet als bewijs voor de huidige tabvolgorde. Het tekenvlak is nog geen herbouwde CAD-canvas.

De repository `open-2D-studio-AEC-extension` is geen zelfstandige Open 2D Studio. `src/ribbonTabs.tsx` op commit `fd22965ed28a` registreert alleen de extra tabs AEC en Pile Plan; Export IFCX en Copy IFCX worden in de bestaande IFC-tab van de host ingebracht. De [native extensiereview](style-repo-2d-extension-forge.png) en HTML-proef tonen uitsluitend die geverifieerde groepen. De hostschil en overige hosttabs zijn niet toegankelijk in deze bron; de Bestand-knop van de algemene showcase is een harmonisatievoorstel, geen geverifieerd onderdeel van de extensie.

Open Field Studio gebruikt volgens `index.html`, `public/styles.css` en `public/app.js` op commit `8a4f104106b2` tien hoofdnavpagina’s onder de titelbalk: Project, Plattegronden, 3D BIM, Opname, Inspectie, Oplevering, Dashboard, Export, Koppelingen en Handleiding. Het is geen ribbonapp. De [route-review](field-route-review.html) koppelt alle tien navigatieknoppen aan hun schermsectie op die commit en toont de zes bestaande screenshots. Plattegronden, 3D BIM, Opname en Handleiding zijn alleen in code geverifieerd; voor deze vier ontbreekt een repositoryscreenshot. De gedeelde Rust-shell heeft hiervoor een topnavigatievariant zonder ribbon, documenttabs en vaste zijpanelen. [De native review](style-repo-field-topnav-light.png) toont het Project-scherm naast de broncapture; deze broncapture is onderzoeksdata en nog geen eigen Rust-implementatie van het formulier.

Open Frame Studio is op commit `eb77f9e4c5d3` tegen `ui/src/components/shell/Ribbon.svelte`, de Nederlandse locale en `ui/src/App.svelte` gecontroleerd. De echte tabs zijn Bestand, Home, Invoegen, IFC / Export, Productie en Beeld. De preview gebruikt hun groepsindeling en concrete commando’s; HTML toont Sjabloon-, IFC LOD- en Themakeuzes als selecties. De native ribbon heeft daarvoor voorlopig knopplaceholders. De werkruimte heeft een aparte reeks van circa twintig views, waaronder 2D Editor en 3D Viewer; een broncapture ontbreekt, dus [de render](style-repo-frame-ribbon-light.png) beoordeelt de shell en commandoverdeling, niet de pixelnauwkeurigheid van de bestaande app.

De nieuwe Planner-referenties corrigeren een concrete fout in de eerste
taxonomie. Op het [Gantt-scherm](../harmonization/references/open-planner-studio/artifacts/tabel-overhaul/22-gantt-wide-1280-en-dark.jpg)
staat de taak/WBS-tabel naast de tijdlijn, met eigenschappen rechts. De
[profieldialoog](../harmonization/references/open-planner-studio/artifacts/profielblok/eigen-profiel-bewerken-licht.png)
laat zien dat compacte formulierregels en statuslabels ook bij lange inhoud
leesbaar moeten blijven. In de [bronregistry op commit 5a65f6b865a7](https://github.com/OpenAEC-Foundation/open-planner-studio/blob/5a65f6b865a7/src/components/layout/Ribbon/ribbonConfig.tsx)
staan Berekenen en taakacties in Start/Planning, niet in aparte top-level
tabs. Daarom vervallen de eerder voorgestelde tabs Taken en Berekenen.
De [native Planner-preview](style-repo-planner-ribbon-light.png) volgt de
gecontroleerde tab- en groepsstructuur; gemeenschappelijke acties gebruiken
de 26-iconenkern en de overige vormen zijn broniconen ter beoordeling.

De [Energy-router op commit e9a485d](https://github.com/OpenAEC-Foundation/open-energy-studio/blob/e9a485db4ac695ff502a48cd2ded50dec5b5a1a6/src/core/navigation/routes.ts)
bevestigt tien hoofdschermen in vier werkstroomgroepen: Invoer (Project,
Gebouw, Installaties), Berekening (Controle, Resultaten), Bestaande bouw
(Basisopname, Maatwerkadvies, Herlabelen) en Oplevering (Rapport,
Registratie). Daaronder liggen 7 gebouw-, 10 installatie-, 2 controle-,
6 resultaat-, 5 advies- en 4 rapportsubpagina's. Basisopname gebruikt een
apart, projectafhankelijk vragenpad. Gereedschap heeft vier functies buiten
de genummerde werkstroom. De [navigatiecomponent](https://github.com/OpenAEC-Foundation/open-energy-studio/blob/e9a485db4ac695ff502a48cd2ded50dec5b5a1a6/src/components/shell/WorkflowNav.tsx)
toont bovendien verschillende stappen voor nieuwbouw en bestaande bouw.
Een harmonisatie die alle tien hoofdschermen als vaste ribbontabs tekent,
zou die werkstroom verliezen. Het gedeelde Rust-frame ondersteunt nu een
werkstroomvariant met navigatie links en zonder ribbon of permanent
eigenschappenpaneel. De Energy-preview in de native atlas gebruikt die variant;
de algemene HTML-ribbon blijft een vergelijking met de andere studio's.
Een software-render liet zien dat de horizontale scrollbar de groepsnamen
overlapte. De gedeelde Rust-shell reserveert nu de volledige ribbonhoogte voor
de scrollbar; een renderregressietest controleert dat de groepsnaam leesbaar
blijft. De preview is nog geen pixelkopie van de bestaande Planner-app, die
compacte knopstapels en een eigen taak/Gantt-werkgebied gebruikt.

## Besluiten voor de gedeelde shell

| Onderdeel | Besluit | Onderbouwing |
| --- | --- | --- |
| Regio's | Titelbalk, ribbon-tabs, ribbon-groepen, documenttabs, verkenner, werkruimte, eigenschappen en status zijn vaste componenten. | Deze ordening is zichtbaar in de Tauri-template en meerdere studio's. |
| Maatvoering | Titel 32 px, tabstrip 28 px, ribbon 94 px, documenttabs 30 px, status 22 px en beide paneelwerkbalken 24 px volgens de Tauri-template; beide standaardpanelen 240 px. | De Rust-crate, Pointcloud en het HTML-prototype gebruiken dezelfde bronmaten voor de standaardweergave. |
| Kleur | Vijf Style Book-thema's; amber is selectie/focus, niet een willekeurige betekenis van een domeinresultaat. | De bestaande apps mengen amber, grijs en vakspecifieke kleuren verschillend. |
| Lettertype | Inter voor bediening, Space Grotesk voor koppen en JetBrains Mono voor code/waarden. | Gebundelde bestanden maken de rendering onafhankelijk van systeemfonts. |
| Iconen | 24×24 semantische bedieningsiconen als canonieke set; vakinhoudelijke iconen krijgen een aparte betekenislaag. | Een maatlijn, een constraint en een gemeten afstand lijken op elkaar maar zijn andere opdrachten. |
| Responsive | Ribbon scrollt horizontaal; op smalle vensters verdwijnt eerst het eigenschappenpaneel. | Getest in het browserprototype bij circa 695 px viewportbreedte. |

## Beoordeling van de huidige proef

| Toets | Resultaat | Vervolg |
| --- | --- | --- |
| Herkenbare gedeelde shell | Voldoende voor conceptreview: 18 studio's gebruiken dezelfde regio's en vijf thema's. | Per studio de exacte commando- en tabgroepen aan de broncode koppelen. |
| Nette opmaak | De compacte browserproef heeft consistente uitlijning, randen en witruimte. | Native screenshots op meerdere platformen vergelijken met de HTML-maten. |
| Semantiek van iconen | De 26 huidige canonieke bedieningstekens zijn een begin; 565 bronbestanden zijn onderzoeksdata. | Groepeer synoniemen, beoordeel tegen light/dark en teken de definitieve domeinsets. |
| FEM en BIM | 52 FEM- en 57 BIM-betekenissen hebben elk een uniek SVG-concept; de atlas toont ze op 16, 24 en 32 px in lichte en donkere omgeving. | Complexe vormen op 16 px verfijnen en de 24 mogelijke bronmatches inhoudelijk vergelijken. |
| Applicatieschermen | Voor 16 studio's zijn negen gedeelde schermtoestanden in HTML en de native Rust-atlas selecteerbaar, waaronder import/export, voortgang, onopgeslagen werk en fouten. Speech toont in de Rust-atlas negen echte zijbalkroutes en acht broncaptures; Field tien topnavigatiepagina’s en zes broncaptures. De native ribbon volgt nu per studio de voorgestelde tabs. FEM en BIM tonen hun eigen concepticonen als themagekleurde app-eigen SVG's; de publieke iconset blijft 26 canonieke betekenissen groot. | Per tool de echte inhoud, dialooginteractie en concrete foutafhandeling aan de broncode koppelen; concepttabs en -iconen vakinhoudelijk beoordelen. |
| Werkelijke migratie | Pointcloud gebruikt de gedeelde crate voor de complete buitenste venstercompositie, beide paneelkoppen, titelbalkiconen, tien beoordeelde algemene tooliconen en het Extensions-icoon, fonts, 77 Tauri-kleurvelden plus de stevige randkleur uit de merktokens per thema, ribbon- en formulierknoppen, invoervelden, keuzelijsten, checkboxen, sliders, voortgangsbalken, scrollbalken, tooltips en vijf vensterbandmaten. Ook de 27 px hoge dialoogknop met 75 px minimumbreedte en identieke tekstuitlijning wordt nu door de crate gebouwd en in beide apps gebruikt. De portable kopie is op 11 Rust-bestanden, 32 assets en dependencies gelijk gecontroleerd. De documenttabs staan vensterbreed; Light- en Forge-renders zijn met lege en geopende scan beoordeeld. De Pointcloud- en Style Repo-renders zijn na de navigatie-iconadoptie opnieuw gegenereerd; de instellingenrenders tonen de gesloten keuzelijsten in Light en Forge. | Domeinpanelen en dialogen op gedeelde widgets aansluiten zonder 3D-functionaliteit te verliezen; echte vensterscreenshots op meerdere platformen vergelijken. |

De actieve en hoverstaat van de 28 px ribbon-tab komen nu uit één
`openaec-ui::widgets::ribbon_tab_style` in zowel de Rust-showcase als
Pointcloud. De 13 Pointcloud-shelltests slagen; zes opnieuw gerenderde
Pointcloud-vensters in Light en Forge zijn bytegelijk aan de vorige beelden.
De Style Repo-beelden zijn na de tabwijziging opnieuw gerenderd en visueel
bekeken in Light en Forge.

Het [interactieve HTML-prototype](harmonized.html) toont de standaardindeling
met twee zijpanelen van 240 px en paneelwerkbalken van 24 px.
De [reviewpagina](review.html) toont zes native Pointcloud-renders van lege en
geopende projecten en de Extensions-bestandspagina in Light en Forge.
De native Style Repo-atlas is in [alle vijf thema's](review.html) als
software-render gecontroleerd. De [FEM-ribbon](style-repo-fem-ribbon-light.png)
en [BIM-ribbon](style-repo-bim-ribbon-forge.png) zijn afzonderlijk op
1280 × 800 px gerenderd: de FEM-groep past binnen het venster, de bredere
BIM-groepen gebruiken de horizontale ribbon-scroll. Dit zijn ontwerpvoorstellen,
geen geverifieerde productfuncties.

De herbruikbare `openaec-ui` is nu een afzonderlijk Cargo-package onder
`crates/openaec-ui/`. `cargo package -p openaec-ui` heeft het uitgepakte
pakket zelfstandig gecompileerd: 49 verpakte bestanden, waaronder 11
Rust-bronnen, zes fonts, drie OFL-licentieteksten en 26 canonieke iconen. De onderzoeksiconen,
FEM/BIM-concepten en reviewbeelden blijven in het niet-publiceerbare
Style Repo-package. De Root/Pointcloud-kopieën van code en assets worden
met `scripts/check_portable_ui.py` op inhoud gecontroleerd.

De [Energy-werkstroomreview](energy-workflow.html) toont nieuwbouw voor woning en utiliteit en de opnamevariant voor bestaande bouw in dezelfde kleur-, type- en vensterbandtaal. De routevolgorde volgt de broncode op commit e9a485d; de kaarten en invoervelden zijn ontwerpelementen en geen overgenomen berekeningsinterface. De gekoppelde handleidingscreenshot kan een andere historische schermstaat tonen. De Rust-crate heeft nu een optionele `ChromeMode::Workflow` met 32/30/22 px titel-, document- en statusbanden. De native atlas laat de vier brongebaseerde navigatiemodi kiezen: [nieuwbouw woning](style-repo-energy-workflow-light.png), [nieuwbouw utiliteit](style-repo-energy-workflow-utility-light.png), [bestaande bouw woning](style-repo-energy-workflow-existing-light.png) en [bestaande bouw utiliteit](style-repo-energy-workflow-existing-utility-forge.png). Bestaande-bouwonderdelen zijn klikbaar in de sidebar; de inhoudskaarten blijven een stijlproef, geen port van de Energy-rekenkern of de echte formulieren.

De Calc-audit op [broncommit b470427](https://github.com/OpenAEC-Foundation/open-calc-studio/blob/b47042704efa388d95eb59ce77d23aeb5ee0e44c/src/components/ribbon/Ribbon.tsx) corrigeert de eerdere generieke lintindeling. Het bronlint bestaat uit Bestand, Begroting, Offerte, Rapportage, Spreadsheet, 3D, PDF en IFC; Tekstopmaak verschijnt alleen bij een tekst- of witregel. Bij `VITE_HIDE_EXPERIMENTAL=true` verdwijnen Offerte, 3D en PDF. De [Nederlandse begrotingscapture](../harmonization/references/open-calc-studio/docs/screenshots/nl/1-begroting.png) toont een Start/Structuurkolom, brede hiërarchische tabel, Eigenschappenpaneel, documenttab boven en werkbladtab onder. Het [Nederlandse rapport](../harmonization/references/open-calc-studio/docs/screenshots/nl/2-rapport.png) is een aparte print-/exportsurface; de [Engelse tabeluitsnede](../harmonization/references/open-calc-studio/docs/screenshots/en/2-grid.png) toont de celhiërarchie. De [native lintpreview](style-repo-calc-ribbon-light.png) en HTML-atlas volgen nu de bronlabels en hoofdgroepen. De tabelinhoud in de atlas blijft een stijlproef: selectie, rijhoogtes, kolomset en rapportopmaak zijn nog geen pixelgelijke Rust-port.

De Geotechniek-audit op [broncommit 8182b48](https://github.com/OpenAEC-Foundation/open-geotechniek-studio/blob/8182b48afc3f662e8d78650c7a1f21a7780d7e5f/apps/desktop/src/components/ribbon/Ribbon.tsx) corrigeert eveneens de generieke tabs: Home, Kaart, Rapport en IFC zijn vast; Situatietekening en Berekeningen zijn afhankelijk van extensies. De geselecteerde beelden tonen [sonderingsgrafieken](../harmonization/references/open-geotechniek-studio/docs/screenshots/03.png), de [BRO-kaart](../harmonization/references/open-geotechniek-studio/docs/screenshots/03-kaart-bro.jpg) en een [boorprofiel](../harmonization/references/open-geotechniek-studio/docs/screenshots/02-bhr-boring.jpg). Ze onderbouwen de verkenner links, documenttabs boven, werkgebied midden, locatie/legenda rechts en de compacte Home-/Kaart-ribbons. De [native lintpreview](style-repo-geotech-ribbon-light.png) en HTML-atlas volgen die groepen. Berekeningen is in de bron een dynamische projectlijst en IFC toont automatische generatie; de preview gebruikt hiervoor expliciete statusplaatsaanduidingen. De kaartlagen, sonderingsgrafiek en bodemstroken zijn nog geen pixelgelijke Rust-port.

De Heatloss-audit op [broncommit e233aec](https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/e233aec70e16771ecb42a57d6eab3ca6cb0e75a8/frontend/src/components/ribbon/Ribbon.tsx) vond zes routegestuurde tabs: Vertrekken, Constructies, Modeller ❄️, IFC, Resultaten en Rapport. De gedeelde stijl toont hiervoor Modeller zonder emoji, omdat de gebundelde Rust-lettertypen anders lege blokjes tonen. [AppShell.tsx](https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/e233aec70e16771ecb42a57d6eab3ca6cb0e75a8/frontend/src/components/layout/AppShell.tsx) toont een vaste linker Sidebar en het werkgebied zonder globaal rechter eigenschappenpaneel. [IfcTab.tsx](https://github.com/OpenAEC-Foundation/open-heatloss-studio/blob/e233aec70e16771ecb42a57d6eab3ca6cb0e75a8/frontend/src/components/ribbon/IfcTab.tsx) geeft bewust `null` terug: kopieer- en downloadacties staan op de IFC-pagina. De [native lintpreview](style-repo-heatloss-ribbon-light.png) en HTML-atlas volgen de huidige tabnamen; de Rust-preview bewaart de lege IFC-groepen. Voor deze repository zijn geen UI-screenshots gevonden, dus schermmaten en visuele paginastaten zijn nog niet onafhankelijk beoordeeld. De rechterstrook in de generieke atlas is hier alleen een harmonisatievoorstel en geen bestaande Heatloss-interface.

De Calculations-audit op [broncommit 21d218c](https://github.com/OpenAEC-Foundation/Open-Calculations-Studio/blob/21d218c996d09b92018ad21b730c883c665dc035/packages/desktop/src/components/ribbon/Ribbon.tsx) vond alleen Start en IFC naast Bestand. [CalcTab.tsx](https://github.com/OpenAEC-Foundation/Open-Calculations-Studio/blob/21d218c996d09b92018ad21b730c883c665dc035/packages/desktop/src/components/ribbon/CalcTab.tsx) groepeert Bestand, Bewerken, Invoegen en Exporteren. [IfcTab.tsx](https://github.com/OpenAEC-Foundation/Open-Calculations-Studio/blob/21d218c996d09b92018ad21b730c883c665dc035/packages/desktop/src/components/ribbon/IfcTab.tsx) is bewust leeg; de IFC-documentweergave bevat de relevante handelingen. De [native lintpreview](style-repo-calculations-ribbon-light.png) en HTML-atlas volgen die staat. `App.tsx` toont ProjectBrowser links, met rekenblad, rapport of IFC midden; een globaal rechter eigenschappenpaneel is niet zichtbaar in de broncode. Er zijn geen bruikbare UI-screenshots in de repository, dus de atlaspagina blijft een visueel onbeoordeeld stijlvoorstel.

De Reports-audit op [broncommit 818e581](https://github.com/OpenAEC-Foundation/openaec-reports/blob/818e58118c0f046410137a3f5a948e4871d21e77/frontend/src/components/chrome/ribbon/Ribbon.tsx) vervangt de generieke tabs door Start, Invoegen en Beeld. De bron groepeert blokken, paginacommando's, validatie en PDF-uitvoer op Start; secties en inhoud op Invoegen; weergavemodi en zijpaneel op Beeld. De [native lintpreview](style-repo-reports-ribbon-light.png) en HTML-atlas tonen die actuele commandoverdeling. De repository bevat geen bruikbare UI-screenshots, dus werkbladmaat, panelen en PDF-preview zijn nog niet visueel onafhankelijk beoordeeld. De generieke atlasinhoud is hier een harmonisatievoorstel.

De BIM Validator-audit op [broncommit 8f837dd](https://github.com/OpenAEC-Foundation/OpenAEC-BIM-validator/blob/8f837dd9a56e12d9b61ddd9dd2b341abe9794256/viewer/src/components/chrome/ribbon/Ribbon.tsx) corrigeert de atlas naar twee linttabs: Start en Beeld. Start groepeert Project, Modellen, Validatie en BCF; Beeld groepeert Panelen, 3D Beeld en Doorsnede. BCF Push en Inloggen hangen van de verbindingsstatus af, terwijl Cloud-acties alleen verschijnen indien ingeschakeld. De [native lintpreview](style-repo-validator-ribbon-light.png) en HTML-atlas tonen de niet-verbonden BCF-staat; de overige staten wachten op afzonderlijke beoordeling. Er zijn geen bruikbare UI-screenshots in de repository gevonden, zodat model-, issue- en rapportpanelen nog niet pixelmatig kunnen worden beoordeeld.

De Pile Plan-audit op [broncommit ffe979d](https://github.com/OpenAEC-Foundation/pile-plan-studio/blob/ffe979d3b85976fe1f523d31a411c97ebd331e2f/apps/pile-plan-studio/src/components/template/ribbon/Ribbon.tsx) vervangt zes verzonnen tabs door het echte Plan en Weergave. De drie bronbeelden tonen [bronimport](../harmonization/references/pile-plan-studio/docs/screenshots/import_data.png), [optimalisatie](../harmonization/references/pile-plan-studio/docs/screenshots/optimization.png) en [paalopties](../harmonization/references/pile-plan-studio/docs/screenshots/pile_options.png). Ze bewijzen het donkere lint, de verkenner links, het 2D-palenplan en het wisselende rechtertaakpaneel. De [native Plan-ribbon](style-repo-pile-ribbon-forge.png) toont de brongecontroleerde groepen. De HTML-atlas heeft in Weergave echte sliders en een voorgrondkeuze als ontwerpproef; de Rust-ribbon gebruikt daar nog gelabelde plaatsaanduidingen, omdat de gedeelde `RibbonGroup` momenteel alleen commandoknoppen draagt. Deze kloof en de getekende planinhoud moeten vóór pixelgelijke inbouw worden opgelost.

De huidige HTML-werkruimte is bewust een wireframe. Een generieke geometrische
placeholder is geen pixelgetrouwe PDF-, BIM- of Pointcloud-canvas. De bronindex
en deze beoordeling voorkomen dat die mockup als voltooide productscreenshot
wordt behandeld.

## FEM/BIM iconbeoordeling · ronde 1

De [visuele atlas](domain-icon-atlas.html) bevat 109 verschillende vectorvormen
in negen betekenisgroepen. Tien drukke betekenissen hebben na vergelijking op
ware 16 px een aparte vereenvoudigde variant; de
[FEM-contactsheet](fem-icon-small-review.png) en
[BIM-contactsheet](bim-icon-small-review.png) tonen 16 px, 24 px en 16 px op
donkere achtergrond. Alle bestanden zijn XML-geldig. De native Style Repo
toont de kleine en grote vorm naast elkaar voor review; de publieke icon-API
van de Rust-crate bevat ze nog niet.
De nieuwe kleine vormen zijn FEM: diaphragm, mesh, mesh-refine en surface-load;
BIM: federate, curtain-wall, opening, zone, array en revision. De overige
drukke 16 px-kandidaten voor een tweede ronde zijn onder meer local-axes,
wind-load, site, building, space, clash en section-box.
In 24 gevallen bestaat
een gelijknamige bronkandidaat; zo'n match is geen bewijs van dezelfde functie.

| Toets | Waarneming | Ontwerpactie |
| --- | --- | --- |
| Familiebeeld | Het 24 px raster, donkere neutrale lijn en afgeronde einden zijn consistent. | Na semantische review dezelfde meetwaarden als canonieke Rust-iconen vastzetten. |
| Kleine maat | Eenvoudige vormen als staaf, kolom, wand en grid blijven herkenbaar op 16 px. Tien drukke vormen kregen een kleinere variant met minder lijnen; de contactbladen tonen de verbetering. | De resterende complexe belasting-, terrein- en gebouwtekens op ware 16 px beoordelen en waar nodig verder vereenvoudigen. |
| Betekenisbotsingen | `bim.level` lijkt op een maatpijl; `bim.survey-point` en `bim.project-origin` delen een kruis/doel-motief; `fem.beam` en `bim.beam` hebben terecht andere context maar kunnen in een gezamenlijke zoeklijst verwarren. | Peilmarkering duidelijker maken, oorsprong/meetpunt verder uiteen trekken en domeinlabels in zoekresultaten tonen. |
| Licht/donker | De HTML-atlas gebruikt een kleurinversie op donkere achtergrond. De native Rust-ribbon kleurt app-eigen SVG's met de actieve thematekstkleur; Light en Forge zijn als software-render gecontroleerd. | Na goedkeuring de definitieve SVG's per thema en op kleine maten toetsen voordat ze publieke crate-assets worden. |
| Bronvergelijking | Kandidaten zijn op bestandsnaam geselecteerd en als tooltips zichtbaar. | De 24 paren visueel en functioneel per opdracht beoordelen; dubbele betekenissen samenvoegen. |

De native Pointcloud-renders lieten bovendien zien dat oude OpenCAD-SVG's met
vaste donkere lijnen op Forge wegvallen. De eerste integratie kleurt hun hele
silhouet op donkere thema's met de gedeelde tekstkleur. Dat herstelt contrast,
maar is geen vervanging voor per icoon beoordeelde vectorvormen en semantische
kleuren.

De negen toestanden in `harmonized.html` zijn nu opmaaksjablonen. Hun knoppen
simuleren nog geen bestanden of berekeningen. Pixelgelijkheid vereist daarna
native screenshots per besturingssysteem, venstermaat en thema, plus vergelijking
met een echte referentietool. Deze visuele ronde keurt de domeiniconen nog niet
voor productie goed.
