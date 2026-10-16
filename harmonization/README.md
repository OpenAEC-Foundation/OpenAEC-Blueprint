# OpenAEC UI-inventarisatie

Een brongepind onderzoeksarchief met 63 publiek beschikbare repositories in de OpenAEC-Foundation-organisatie, vier eerder onderzochte maar niet publiek bereikbare OpenAEC-namen en OpenCADStudio als externe referentie. De [dekkingsmatrix](../design/coverage-matrix.html) splitst UI-code, UI-gebruikte assetbestanden, iconbronbestanden, bibliotheekiconen en schermkandidaten per publieke repository uit; drie publieke repositories zijn leeg (GitHub-commits-API 409). Bereikbare bronnen zijn op een commit vastgelegd. Geen code uit de bronrepositories is uitgevoerd. De [actuele toegangsaudit](../design/public-access-audit.html) vergelijkt de 63 huidige openbare organisatierepositories met deze historische records; de [JSON-data](public-access-audit.json) legt de API-uitkomst vast.

De 63 publieke repositories hebben nu elk een verklaarde auditstatus: 49 met UI-bronscan, tien zonder aangetroffen studio-UI-bron, drie lege repositories en één grote toolchainreferentie (`llvm-project`) die niet als studio-app is doorgelicht. De laatste categorie is nadrukkelijk geen claim dat de hele toolchain geen interfacecode bevat.

Dit is een breed archief van visuele bronbestanden, geen telling van gebruikte UI-iconen: alle SVG/ICO/ICNS/XPM-bestanden en rasterbestanden met icon/logo/favicon/pictogram/toolbar/ribbon in het pad. Het omvat ook technische symbolen, tekeningen en branding. Inline iconen zijn als bronbestanden bewaard; externe iconpackages zijn geregistreerd, niet volledig gespiegeld. Voor UI-gebruik zie `asset-index.json`, `ui-code-references.json` en `../design/review.html`. Privérepositories zijn niet toegankelijk; buiten de ene genoemde OpenCADStudio-referentie zijn externe repositories niet geïnventariseerd.

De [Open Planner-lintindex](planner-ribbon-ui-icons.json) is een gerichte uitzondering voor een extern iconpackage: 85 bronbewezen Lucide-vectoren zijn uit de in `package-lock.json` vastgezette versie 0.575.0 geëxtraheerd, na SHA-512-verificatie van het pakket. De [visuele review](../design/planner-ribbon-icon-review.html) toont 16/24/32 px op licht en donker. De ISC/MIT-notice staat naast de kopieën in `ui-icons/open-planner-ribbon/`. Dit telt niet als 85 originele OpenAEC-ontwerpen of als onderdeel van de 577 bestandsassets.

De [Open Energy-index](energy-ui-icons.json) bevat 84 `lucide-react`-vectoren uit versie 0.577.0, na verificatie tegen de gepinde lockfile. In 41 UI-componenten zijn 251 JSX-aanroepen en zes dynamische statuskeuzes gevonden; elke vorm heeft een bronregel en SHA-256. De [review](../design/energy-ui-icon-review.html) toont alle vormen in drie maten op lichte en donkere ondergrond. De pakketnotice staat in `ui-icons/open-energy-studio/LUCIDE-LICENSE.txt`. Bibliotheekvectoren zijn geen originele OpenAEC-iconen en behoren niet tot de 577 bestandsassets of de goedgekeurde Rust-kern. De [betekenisreview](../design/energy-icon-crosswalk.html) en [beslisdata](../design/energy-icon-crosswalk.json) zetten iedere bronvorm naast zijn UI-actie en eventuele Rust-kandidaat; gemengde betekenissen blijven expliciet gescheiden.

De [Heatloss-inline-lintindex](heatloss-ribbon-ui-icons.json) bewijst zes gebruikte SVG-definities op negen knoppen in vier actieve linttabs; vier niet-aangeroepen definities zijn uitgesloten. De [Heatloss-Lucidereview](../design/heatloss-lucide-icon-review.html) en [index](heatloss-lucide-ui-icons.json) behandelen 35 vormen in acht actieve UI-bestanden, met de pakketnotice in `ui-icons/open-heatloss-studio/`. Beide [inline vormen](../design/heatloss-ribbon-icon-review.html) en bibliotheekvormen blijven reviewmateriaal. De oude `components/modeller/Ribbon.tsx` wordt door de huidige app-ribbon niet gerenderd. De [titelbalk- en Bestand-index](heatloss-chrome-ui-icons.json) koppelt daarnaast 26 UI-vormen aan 29 concrete plaatsen; [de atlas](../design/heatloss-chrome-icon-review.html) toont conditionele vensterstaten en drie zichtbare maar niet aangesloten snelknoppen. Twee gebouwbeeldmerken zijn uitgesloten. De [zijbalkindex](heatloss-sidebar-ui-icons.json) registreert negentien gebruikte iconcomponenten op 24 routes en negen groepen. De [rest-SVG-index](heatloss-remaining-svg-audit.json) classificeert elke overige letterlijke JSX-SVG op bronregel: 19 UI-icoonplaatsen en 15 uitgesloten diagrammen, illustraties, patronen of inactieve vormen; [de review](../design/heatloss-remaining-svg-review.html) toont de bruikbare vormen. De [route-index](heatloss-screen-routes.json) koppelt alle 26 pagina-routes aan hun broncomponent, zijbalkstatus en ribbonkoppeling; [de visuele routekaart](../design/heatloss-screen-route-review.html) markeert zestien routes zonder vaste tabkoppeling en hun verschillende directe-start- en navigatiegedrag.

De [Pointcloud-annotatiebesluiten](pointcloud-annotation-icon-review.json) leggen de werkelijke Tekst- en Leidlijnbronvormen, UI-aanroepen en SHA-256 vast. De [Light/Forge-review](../design/pointcloud-annotation-icon-review.html) vergelijkt de tweekleurige bron met de getypeerde Rust-domeiniconen op 16, 24 en 32 px. Hun 16px-vormen zijn apart getekend en Pointcloud haalt de knoppen nu uit de portable crate.

De [PDF-vensterchrome-index](pdf-chrome-ui-icons.json) volgt 41 letterlijke SVG-plaatsen in de gepinde Solid-titelbalk, Bestand-weergave, statusbalk, Vergelijken-tab en ribbon. De dynamische lintchevron heeft twee toestanden, samen 42 [reviewvectoren](../design/pdf-chrome-icon-review.html). Het geïmporteerde PNG-appbeeldmerk en de documentinhoud zijn geen UI-SVG-iconen. Uitgeschakelde navigatie, voorwaardelijke vergelijking en Tauri-vensterknoppen staan afzonderlijk in de data.

De [PDF-Tekenen-index](pdf-drawing-ui-icons.json) onderzoekt alle 38 letterlijke SVG’s uit de bronbereikbare DrawingTab. De placeholder zonder knopaanroep is uitgesloten; 37 gebruikte vormen bedienen 38 knopplaatsen. De [review](../design/pdf-drawing-icon-review.html) toont bronregel, knop-ID, Nederlandstalig label, toestand en 16/24/32px-weergave. Drie SVG’s gebruiken `<text>` en missen in de native renderer hun ‘1:N’ of ‘R’; [zes path-gebaseerde ontwerpvarianten](proposals/pdf-drawing-native/) voor 24 en 16 px staan daarom apart van de bronkopieën. De geïmporteerde `ribbonIcons.js`-vormen staan in de aansluitende catalogusaudit.

De [PDF-ribboncatalogusindex](pdf-ribbon-imported-ui-icons.json) toetst alle 122 SVG-exports in `ribbonIcons.js` aan tien ingebouwde, bereikbare Solid-consumenten. 109 vormen hebben samen 146 UI-referenties; 13 zijn alleen via extensies adresseerbaar. De [HTML-review](../design/pdf-ribbon-imported-icon-review.html) beoordeelt ook zeven identieke vormen met verschillende functies. [Native Light](../design/pdf-ribbon-imported-icons-light.png) en [Forge](../design/pdf-ribbon-imported-icons-forge.png) tonen de 109 gebruikte vormen; Tekst toevoegen en Tekstvak missen daarin de SVG-tekst en vragen nog een path-gebaseerd native ontwerp.

De [PDF-ribbonbetekenisreview](../design/pdf-ribbon-semantic-review.html) vergelijkt vijftien betekenissen uit zeven exacte bronvormgroepen. [Twaalf nieuwe 24px-SVG’s en vier optische 16px-varianten](proposals/pdf-ribbon-semantic/) volgen de huidige crate-lijndikte; drie betekenissen hergebruiken `Icon::Fit`, `Icon::Search` of `DomainIcon::DrawingText`. [Native Light](../design/pdf-ribbon-semantic-light.png) en [Forge](../design/pdf-ribbon-semantic-forge.png) tonen bron en voorstel in de echte Iced-renderer. Het [manifest](proposals/pdf-ribbon-semantic/review.json) koppelt alle vijftien betekenissen nu aan hun getypeerde Rust-crate-iconen. De twaalf nieuwe `DomainIcon::Pdf*`-vormen zijn bytegelijk aan de gereviewde ontwerpen; de JavaScript-bronapp is nog niet gemigreerd.

De [PDF-Openen-index](pdf-open-panel-ui-icons.json) toetst alle 19 letterlijke SVG-plaatsen in `OpenPanel.jsx` aan de daadwerkelijk via het Bestand-menu bereikbare UI. Er zijn 19 plaatsen en 15 exacte bronvormen; de [visuele review](../design/pdf-open-panel-icon-review.html) toont de vorm op 16/24/32 px, rol, toestand en bronregel. De PDF-tekst in het documentpictogram blijft een bekende native-rendererafwijking.

De [PDF-annotatiepaneel-index](pdf-annotations-panel-ui-icons.json) koppelt 14 letterlijke SVG-plaatsen in `AnnotationsPanel.jsx` aan 15 UI-plaatsingen. De [Light/Forge-review](../design/pdf-annotations-panel-icon-review.html) toont elke vorm op 16/24/32 px, inclusief open/gesloten groepschevrons. Vier menuregels zijn permanent uitgeschakeld; hun zichtbare vormen blijven onderdeel van de inventaris. De zeven geïmporteerde contextmenu-iconen zijn apart beoordeeld.

De [PDF-contextmenu-index](pdf-context-literal-ui-icons.json) koppelt de 14 letterlijke SVG-definities uit `ContextMenu.jsx` aan 15 directe UI-aanroepen. De [review](../design/pdf-context-literal-icon-review.html) maakt de lexicale botsing rond `selectAllIcon` en de dubbele invoegaanroep zichtbaar. De geïmporteerde `contextMenuIcons.js`-vormen zijn in de aansluitende index afzonderlijk beoordeeld.

De [geïmporteerde PDF-contextmenu-index](pdf-context-imported-ui-icons.json) volgt alle 52 exports uit `contextMenuIcons.js` naar 69 symboolreferenties in de bereikbare contextmenucomponent. De [HTML-review](../design/pdf-context-imported-icon-review.html) toont aanroepregels en 16/24/32px-vormen; [native Light](../design/pdf-context-imported-icons-light.png) en [Forge](../design/pdf-context-imported-icons-forge.png) bewaren de bronkleuren van de acht schikiconen. `pasteIcon`/`pagePasteIcon`, `deleteIcon`/`pageDeleteIcon` en `duplicateIcon`/`pageCopyIcon` zijn byte-identieke vormparen, maar hun commando-context verschilt.

De [mobiele schermindex](pdf-mobile-screen-states.json) legt vier bereikbare schermtoestanden en hun CSS-maten vast. De [HTML-studie](../design/pdf-mobile-screen-review.html) vergelijkt 320/360/412 px en twee thema’s; het PDF-canvas is bewust schematisch, omdat hiervoor geen broncreenshot als pixelreferentie is gebruikt.

De [mobiele PDF-index](pdf-mobile-ui-icons.json) beoordeelt alle 25 SVG-bronplaatsen in `MobileApp.jsx`, waarvan 24 echte UI-plaatsen zijn. Eén grote documentvorm is een lege-staatillustratie. De [review](../design/pdf-mobile-icon-review.html) toont 29 toestands- en gereedschapsvormen; de vijf gereedschappen komen uit één dynamische SVG-plaats. Bronhergebruik met andere betekenis blijft zichtbaar.

De [PDF-symboolpalet-index](pdf-symbol-palette-ui-icons.json) toetst acht letterlijke SVG-bronplaatsen: zeven UI-bedieningsvormen op elf plaatsen en één SVG-wrapper rond door de gebruiker geüploade afbeelding, die als tekeningsymbool wordt opgeslagen. De [review](../design/pdf-symbol-palette-icon-review.html) toont alleen de UI-vormen. De dynamische `cat.icon`-categoriebeelden hebben een afzonderlijke [bronindex](pdf-symbol-category-ui-icons.json) en [review](../design/pdf-symbol-category-icon-review.html): zeven SVG-definities leveren twaalf ingebouwde categorieplaatsen plus optionele eigen groepen. `sym.svg`-miniaturen blijven plaatsbare tekeningsymbolen en tellen niet als vaste bediening.

De [PDF-Start-index](pdf-home-tab-ui-icons.json) toetst acht letterlijke SVG’s in de via `Ribbon.jsx` bereikbare Start-tab: vijf ribbonknoppen en drie opties in het screenshotmenu. De [Light/Forge-review](../design/pdf-home-tab-icon-review.html) toont ze op 16/24/32 px en legt vast dat de IFC-report-bronvorm de in het broncommentaar genoemde uitgaande pijl mist; `DomainIcon::PdfIfcReportExport` in de gedeelde Rust-crate voegt de pijl toe met een eigen 16px-vorm.

De [PDF-toolpalet-index](pdf-tool-palette-ui-icons.json) beoordeelt acht in `App.jsx` bereikbare SVG-bronplaatsen: twee gereedschappen, vier bedieningsvormen en twee alleen tijdens slepen zichtbare dockdoelen. De [review](../design/pdf-tool-palette-icon-review.html) toont ze op 16/24/32 px in Light en Forge. De andere 18 geïmporteerde gereedschapsvormen horen bij de afzonderlijke ribboncatalogus.

De [PDF-Import/Export/Extensies-index](pdf-transfer-panel-ui-icons.json) koppelt alle 14 letterlijke SVG-plaatsen in drie bereikbare panelen aan hun bedieningsrol en zichtbaarheid. De [review](../design/pdf-transfer-panel-icon-review.html) toont ze op 16/24/32 px in Light en Forge. CAD, XFDF en BCF gebruiken voor import en export identieke bronvormen, hoewel de richting verschilt. ODT, DOCX en XLSX zijn tekstbadges, geen SVG-iconen.

De [PDF-Zoekbalk-index](pdf-find-bar-ui-icons.json) koppelt vijf letterlijke SVG-knoppen aan hun bereikbare bronplaatsen en legt de CSS-maten en toestanden vast. De [schermreview](../design/pdf-find-bar-screen-review.html) gebruikt de originele `find-bar.css` en SVG-geometrie om breedte, thema en resultaattoestanden te vergelijken. Aa, vinkjes en uitklaptekens zijn bediening, maar geen SVG’s; zoekmarkeringen zijn documentoverlays.

De [PDF-linkerpanelen-index](pdf-left-panel-content-ui-icons.json) beoordeelt 32 SVG-bronplaatsen uit Bijlagen, Bladwijzers, Formuliervelden, Koppelingen, Handtekeningen en het apart gedockte Markeringslagen-paneel. De [review](../design/pdf-left-panel-content-review.html) scheidt 19 opdrachtknoppen, vier lijstmarkeringen, zes veldtypen en drie handtekeningstaten. De twaalf verticale tabiconen uit `leftPanelIcons.js` blijven buiten deze JSX-telling.

De [PDF-dialoogindex](pdf-dialog-ui-visuals.json) classificeert 25 SVG-bronplaatsen uit acht via `DialogHost` bereikbare dialogen: zeventien zijn generieke actie- of navigatieiconen; acht zijn kenmerkbadges, een klikbaar merkbeeld, een lijstmarkering of toestandsemblemen. De [HTML-review](../design/pdf-dialog-ui-visual-review.html) toont 16/24/32 px en de bronmaten van tekst-, samenvoeg- en afdrukwerkbalken. GitHub-geometrie en semantische statuskleuren blijven bewust herkenbaar.

De [PDF-JSX-dekkingskaart](pdf-jsx-svg-coverage.json) telt 317 letterlijke `<svg>`-bronplaatsen in 68 van 172 Solid JSX/TSX-bestanden. Eenendertig bestanden met 251 plaatsen zijn volledig op UI-rol beoordeeld; de overige 66 zijn een expliciete werkvoorraad, geen icoontelling. De [HTML-kaart](../design/pdf-jsx-svg-coverage.html) toont per bestand aantal en reviewstatus, inclusief de aparte mobiele route en de gedeeltelijke Opmaak-/Schikken-reviews.

De [Open Frame Svelte-index](frame-svelte-svg-audit.json) doorloopt alle 127 letterlijke SVG-plaatsen en bewaart bronregel, label en hash voor de 118 UI-icoonplaatsen; negen inhoudsgraphics zijn uitgesloten. [De atlas](../design/frame-svelte-icon-review.html) toont licht/donker op drie maten. De [schermindex](frame-screen-map.json) koppelt 20 tabkeuzes uit `App.svelte` aan schermcomponenten; [de interactieve kaart](../design/frame-screen-review.html) laat ook de twee editor-canvasvarianten en gedeelde zijpanelen zien. Er zijn geen bron-screenshots voor pixelbeoordeling. De [layoutmaatindex](frame-layout-evidence.json) vergelijkt zes bronmaten met de Rust-constanten en legt ook het contrast van inactieve tabs in het lichte thema vast; [de browserreview](../design/frame-layout-review.html) toont een schaalbare CSS-replica.

BuildingPy heeft een [aparte bronreview](../design/building-py-location-review.html) voor zijn PySide2/Qt-locatiedialoog; `construction/panel.py` is geometrische modelcode, geen paneel in de gebruikersinterface.

Project OconDat is apart op zijn twee webinterfaces geauditeerd: 19 UI-codebestanden en 74 bronregels. De [schermreview](../design/ocondat-ui-review.html) beschrijft de componentenbrowser, Nederlandse standaardenbibliotheek en iconclassificatie. De duizenden SVG-bestanden met bouwcomponenten en tekenpatronen zijn technische inhoud, geen UI-iconen.

Een eerste aparte audit voor SVG's die direct in UI-code staan heeft [18 gebruikte BCF Platform-iconen](../design/bcf-inline-icon-review.html) geëxtraheerd. Hun [index](bcf-inline-ui-icons.json) bevat de definitieregel, de aanroepregel en de hash op commit `e98fb97f5f23`; de zelfstandige SVG-reviewkopieën staan onder `inline-ui-icons/openaec-bcf-platform/`. Deze vormen zijn nog geen canonieke crate-iconen en worden niet bij de 577 bestandsassets opgeteld zonder de categorie te vermelden. Vier ongebruikte BCF-definities blijven buiten de telling.

Ook [47 gebruikte Open Calc Studio-linticonen](../design/calc-inline-icon-review.html) zijn geëxtraheerd. Hun [index](calc-inline-ui-icons.json) volgt `icons.ts` naar concrete aanroepen in Home, Offerte, Rapportage en Tekstopmaak op commit `b47042704efa`; de SVG-reviewkopieën staan onder `inline-ui-icons/open-calc-studio/`. Andere codegetekende SVG's, bijvoorbeeld diagrammen en concepttekeningen, zijn hierdoor niet automatisch UI-iconen.

Voor Open Calculations Studio bevat de [gerichte review](../design/calculations-inline-icon-review.html) acht huidige Calc-knopiconen. De [index](calculations-inline-ui-icons.json) laat tegelijk zien welke twintig definities uit `calcIcons.ts` niet door de huidige knoppen worden aangeroepen en waarom de 42 vormen in de oudere `icons.ts` buiten de telling blijven. De losse reviewvectoren staan onder `inline-ui-icons/Open-Calculations-Studio/`.

De [Geotechniek-review](../design/geotech-inline-icon-review.html) bevat dertig daadwerkelijk gebruikte inline linticonen uit Start, Kaart, Rapport en Sonderingstekening op commit `8182b48afc3f`. De [index](geotech-inline-ui-icons.json) bewaart definitie, knopaanroep en hash; zelfstandige reviewvectoren staan onder `inline-ui-icons/open-geotechniek-studio/`. De 42 oude `icons.ts`-definities worden door deze vier linttabs niet geïmporteerd en zijn apart gehouden. Andere schermcomponenten en technische SVG's vragen nog een afzonderlijke audit.

Hetzelfde broncommit levert [elf gebruikte iconen in Bestand](../design/geotech-backstage-icon-review.html). De [Bestand-index](geotech-backstage-ui-icons.json) verwijst voor elke `ICONS`-string naar zijn `MenuItem`-aanroep en SHA-256. Het overige SVG-gebruik in `Backstage.tsx`, waaronder het applicatielogo, valt buiten deze elf menu-iconen.

De [titel- en documentreview](../design/geotech-chrome-icon-review.html) bevat dertien gerenderde JSX-SVG-vormen uit `TitleBar.tsx` en `DocumentBar.tsx`. De [index](geotech-chrome-ui-icons.json) koppelt elke vorm aan het zichtbare element of de aangeroepen component, noteert de bronmaat en bewaart SHA-256. Het titelbalkbeeldmerk is branding; de vier zichtbare sneltoetsiconen zonder `onClick` worden expliciet als nog niet gekoppelde bediening gemarkeerd.

De [kruisverwijzing van 54 Geotechniek-vormen](../design/geotech-icon-crosswalk.html) koppelt deze drie bronaudits aan de gedeelde Rust-kern, drie nieuw beoordeelde algemene betekenissen en de domein- en twijfelgevallen. De [gestructureerde beslisdata](../design/geotech-icon-crosswalk.json) bewaren de bronhash en beide gebruiksregels waar een vorm meer dan één actie afbeeldt. De ontwerpen voor Print, Opslaan als en Herstellen staan als beoordeelde schetsen onder `design/icon-core-drafts/` en als definitieve bytes in `crates/openaec-ui/assets/icons/`.

Gedownloade bronbestanden staan in `sources/` en worden **niet** meegeleverd in de Rust-crate. De repositorylicentie is een aanwijzing; afwijkende assetlicenties moeten bij selectie worden gecontroleerd.

| Repository | UI-techniek (manifest) | Visuele bronbestanden | Icon-gerelateerde bronbestanden | Fouten |
|---|---|---:|---:|---:|
| [acadifc](https://github.com/OpenAEC-Foundation/acadifc) | Niet vastgesteld | 0 | 0 | 0 |
| [blender-bonsai-training](https://github.com/OpenAEC-Foundation/blender-bonsai-training) | Niet vastgesteld | 263 | 0 | 0 |
| [building-py](https://github.com/OpenAEC-Foundation/building-py) | Niet vastgesteld | 109 | 0 | 0 |
| [Computational-Design-Day-Delft-March-2026](https://github.com/OpenAEC-Foundation/Computational-Design-Day-Delft-March-2026) | Niet vastgesteld | 0 | 0 | 0 |
| [conventions](https://github.com/OpenAEC-Foundation/conventions) | Niet vastgesteld | 0 | 0 | 0 |
| [crates-warehouse](https://github.com/OpenAEC-Foundation/crates-warehouse) | Niet vastgesteld | 0 | 0 | 0 |
| [dynlex](https://github.com/OpenAEC-Foundation/dynlex) | Dynlex, Slint | 4 | 0 | 0 |
| [ERPNext-NL-Translation](https://github.com/OpenAEC-Foundation/ERPNext-NL-Translation) | Niet vastgesteld | 0 | 0 | 0 |
| [ext-drawing-statistics](https://github.com/OpenAEC-Foundation/ext-drawing-statistics) | Niet vastgesteld | 0 | 0 | 0 |
| [gis2bim-openanalysis](https://github.com/OpenAEC-Foundation/gis2bim-openanalysis) | Niet vastgesteld | 1 | 0 | 0 |
| [github](https://github.com/OpenAEC-Foundation/github) | Niet vastgesteld | 1 | 0 | 0 |
| [ifccad](https://github.com/OpenAEC-Foundation/ifccad) | Niet vastgesteld | 1 | 0 | 0 |
| [ifccad-prototype](https://github.com/OpenAEC-Foundation/ifccad-prototype) | Niet vastgesteld | 0 | 0 | 0 |
| [ifcgit-4-nextcloud](https://github.com/OpenAEC-Foundation/ifcgit-4-nextcloud) | Vue | 0 | 0 | 0 |
| [inb-template](https://github.com/OpenAEC-Foundation/inb-template) | Niet vastgesteld | 159 | 0 | 0 |
| [llvm-project](https://github.com/OpenAEC-Foundation/llvm-project) | Slint | 48 | 0 | 0 |
| [master-builder-library](https://github.com/OpenAEC-Foundation/master-builder-library) | Niet vastgesteld | 0 | 0 | 0 |
| [monty-ifc-viewer](https://github.com/OpenAEC-Foundation/monty-ifc-viewer) | Niet vastgesteld | 0 | 0 | 0 |
| [nextcloud-sharelink](https://github.com/OpenAEC-Foundation/nextcloud-sharelink) | Niet vastgesteld | 0 | 0 | 0 |
| [open-2d-studio](https://github.com/OpenAEC-Foundation/open-2d-studio) | Niet vastgesteld | 0 | 0 | 1 |
| [open-2D-studio-AEC-extension](https://github.com/OpenAEC-Foundation/open-2D-studio-AEC-extension) | Niet vastgesteld | 0 | 0 | 0 |
| [open-3d-studio](https://github.com/OpenAEC-Foundation/open-3d-studio) | React, Tauri | 51 | 0 | 0 |
| [open-aec-master-builder-I-OAMBI](https://github.com/OpenAEC-Foundation/open-aec-master-builder-I-OAMBI) | Niet vastgesteld | 0 | 0 | 0 |
| [open-baken-studio-releases](https://github.com/OpenAEC-Foundation/open-baken-studio-releases) | Niet vastgesteld | 0 | 0 | 0 |
| [open-bim-studio](https://github.com/OpenAEC-Foundation/open-bim-studio) | Niet vastgesteld | 0 | 0 | 1 |
| [open-books](https://github.com/OpenAEC-Foundation/open-books) | Niet vastgesteld | 0 | 0 | 0 |
| [open-calc-studio](https://github.com/OpenAEC-Foundation/open-calc-studio) | React, Tauri | 54 | 1 | 0 |
| [open-calc-studio-extensions](https://github.com/OpenAEC-Foundation/open-calc-studio-extensions) | Niet vastgesteld | 0 | 0 | 0 |
| [Open-Calculations-Studio](https://github.com/OpenAEC-Foundation/Open-Calculations-Studio) | React, Tauri | 54 | 2 | 0 |
| [open-energy-studio](https://github.com/OpenAEC-Foundation/open-energy-studio) | React, Tauri | 56 | 0 | 0 |
| [open-fem-studio](https://github.com/OpenAEC-Foundation/open-fem-studio) | Niet vastgesteld | 0 | 0 | 1 |
| [open-fem2d-studio](https://github.com/OpenAEC-Foundation/open-fem2d-studio) | Niet vastgesteld | 0 | 0 | 1 |
| [Open-Field-Studio](https://github.com/OpenAEC-Foundation/Open-Field-Studio) | React, Slint, Tauri | 54 | 0 | 0 |
| [open-frame-studio](https://github.com/OpenAEC-Foundation/open-frame-studio) | Svelte, Tauri | 6 | 0 | 0 |
| [open-geotechniek-studio](https://github.com/OpenAEC-Foundation/open-geotechniek-studio) | React, Tauri | 63 | 1 | 0 |
| [open-heatloss-studio](https://github.com/OpenAEC-Foundation/open-heatloss-studio) | React, Tauri | 54 | 1 | 0 |
| [open-monuments-core](https://github.com/OpenAEC-Foundation/open-monuments-core) | Niet vastgesteld | 0 | 0 | 0 |
| [open-monuments-inspect](https://github.com/OpenAEC-Foundation/open-monuments-inspect) | Niet vastgesteld | 0 | 0 | 0 |
| [open-monuments-mjop](https://github.com/OpenAEC-Foundation/open-monuments-mjop) | Niet vastgesteld | 0 | 0 | 0 |
| [open-pdf-studio](https://github.com/OpenAEC-Foundation/open-pdf-studio) | Tauri | 125 | 5 | 0 |
| [open-pdf-studio-library](https://github.com/OpenAEC-Foundation/open-pdf-studio-library) | Niet vastgesteld | 526 | 0 | 0 |
| [open-pdf-studio-v3](https://github.com/OpenAEC-Foundation/open-pdf-studio-v3) | Slint | 70 | 0 | 0 |
| [open-planner-studio](https://github.com/OpenAEC-Foundation/open-planner-studio) | React, Slint, Tauri | 55 | 5 | 0 |
| [open-planner-studio-extensions](https://github.com/OpenAEC-Foundation/open-planner-studio-extensions) | Niet vastgesteld | 0 | 0 | 0 |
| [open-pointcloud-studio](https://github.com/OpenAEC-Foundation/open-pointcloud-studio) | React, Tauri, iced | 137 | 1 | 0 |
| [open-speech-studio](https://github.com/OpenAEC-Foundation/open-speech-studio) | Tauri | 52 | 0 | 0 |
| [Open-STL-3DMap-Studio](https://github.com/OpenAEC-Foundation/Open-STL-3DMap-Studio) | Niet vastgesteld | 0 | 1 | 0 |
| [openaec-accounts-client](https://github.com/OpenAEC-Foundation/openaec-accounts-client) | Tauri | 0 | 0 | 0 |
| [openaec-accounts-server](https://github.com/OpenAEC-Foundation/openaec-accounts-server) | Niet vastgesteld | 0 | 0 | 0 |
| [openaec-bcf-platform](https://github.com/OpenAEC-Foundation/openaec-bcf-platform) | React, Slint | 1 | 1 | 0 |
| [OpenAEC-BIM-validator](https://github.com/OpenAEC-Foundation/OpenAEC-BIM-validator) | React | 2 | 1 | 0 |
| [openaec-cloud](https://github.com/OpenAEC-Foundation/openaec-cloud) | Niet vastgesteld | 0 | 0 | 0 |
| [openaec-cloud-desktop](https://github.com/OpenAEC-Foundation/openaec-cloud-desktop) | Tauri | 51 | 0 | 0 |
| [openaec-docs](https://github.com/OpenAEC-Foundation/openaec-docs) | React, Slint | 4 | 0 | 0 |
| [openaec-installer](https://github.com/OpenAEC-Foundation/openaec-installer) | React, Tauri | 19 | 1 | 0 |
| [openaec-reports](https://github.com/OpenAEC-Foundation/openaec-reports) | React, Tauri | 6 | 2 | 0 |
| [OpenAEC-style-book](https://github.com/OpenAEC-Foundation/OpenAEC-style-book) | React, Tauri | 63 | 2 | 0 |
| [openaec-ui](https://github.com/OpenAEC-Foundation/openaec-ui) | Niet vastgesteld | 0 | 0 | 0 |
| [OpenAEC-Workspace-Composer](https://github.com/OpenAEC-Foundation/OpenAEC-Workspace-Composer) | Tauri | 28 | 0 | 0 |
| [OpenAEC-zaagplan](https://github.com/OpenAEC-Foundation/OpenAEC-zaagplan) | React, Slint | 0 | 0 | 0 |
| [OpenCADStudio](https://github.com/HakanSeven12/OpenCADStudio) | iced, winit | 394 | 2 | 0 |
| [pile-plan-studio](https://github.com/OpenAEC-Foundation/pile-plan-studio) | React, Tauri | 2 | 1 | 0 |
| [project-ocondat](https://github.com/OpenAEC-Foundation/project-ocondat) | Niet vastgesteld | 24422 | 0 | 0 |
| [pyrevit-gis2bim](https://github.com/OpenAEC-Foundation/pyrevit-gis2bim) | Niet vastgesteld | 139 | 6 | 0 |
| [repo-cleaner](https://github.com/OpenAEC-Foundation/repo-cleaner) | Niet vastgesteld | 1 | 0 | 0 |
| [website](https://github.com/OpenAEC-Foundation/website) | Niet vastgesteld | 15 | 0 | 0 |
| [Y-app-ERPNext](https://github.com/OpenAEC-Foundation/Y-app-ERPNext) | Niet vastgesteld | 2 | 1 | 0 |
| [zaagplan](https://github.com/OpenAEC-Foundation/zaagplan) | React, Slint | 0 | 0 | 0 |

Totaal: 68 repositories, 27092 visuele bronbestanden, 26452 unieke bestandshashes.
