# Visuele beoordeling · OpenAEC UI

Status: ontwerpbeoordeling van de huidige geharmoniseerde shell, 15 oktober 2026.
Dit document beoordeelt het ontwerp, niet de volledigheid van een toekomstige
migratie van alle OpenAEC-applicaties.

## Bronnen en zekerheid

- 68 repositoryrecords zijn geïnventariseerd: 63 publieke OpenAEC-repositories,
  de externe OpenCADStudio en vier niet toegankelijke of niet gevonden namen.
- 658 beeldverwijzingen zijn op commit vastgelegd in `screen-index.json`;
  637 hebben een unieke Git-blobinhoud en 464 zijn als mogelijke
  applicatieschermen geclassificeerd. De classificatie
  bewijst niet dat het unieke pagina's of huidige productiestaten zijn.
- 565 bestanden hebben een concrete UI-codeverwijzing of de actieve
  pyRevit-knopbundelconventie. De overige SVG's, CAD-symbolen, illustraties en
  technische tekeningen horen niet bij die telling.
- 686 iconimports in broncode verwijzen naar 219 pakket/naamcombinaties.
  Daarvan zijn 312 versiegebonden SVG's uit Lucide Static en Solid Icons
  gedownload; deze categorie is apart geïndexeerd en visueel vergelijkbaar.
- Het [semantische kruisverband](icon-semantic-crosswalk.html) vergelijkt de
  22 huidige gedeelde iconbetekenissen met 565 bewezen UI-bestanden en 312
  versiegebonden bibliotheekvarianten. 79 naamovereenkomsten zijn kandidaten;
  798 items blijven buiten de kern of vragen een domeinspecifieke betekenis.
  Dit is geen goedkeuring van vorm of functie. Zes Pointcloud-toolacties hebben na
  controle van hun commandobetekenis een expliciet
  [adoptiebesluit](icon-adoptions.json): Open, Export, Fit, Undo, Redo en Save.
  Refresh LOD gebruikt nu zijn eigen Update-symbool in plaats van Fit.
  De Extensions-bestandspagina heeft een [eigen iconreview](extensions-icon-review.html):
  een nieuw getekend puzzelstuk vervangt de semantisch onjuiste 3D-kubus.
- De eerste visuele vergelijking gebruikt het Tauri Style Book, PDF Studio v2,
  Pointcloud native en de 51 lokaal bewaarde visuele referenties. De
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
de 22-iconenkern en de overige vormen zijn broniconen ter beoordeling.

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
| Semantiek van iconen | De 22 huidige canonieke bedieningstekens zijn een begin; 565 bronbestanden zijn onderzoeksdata. | Groepeer synoniemen, beoordeel tegen light/dark en teken de definitieve domeinsets. |
| FEM en BIM | 52 FEM- en 57 BIM-betekenissen hebben elk een uniek SVG-concept; de atlas toont ze op 16, 24 en 32 px in lichte en donkere omgeving. | Complexe vormen op 16 px verfijnen en de 24 mogelijke bronmatches inhoudelijk vergelijken. |
| Applicatieschermen | Negen gedeelde schermtoestanden zijn in HTML en de native Rust-atlas voor alle 18 studio's selecteerbaar, waaronder import/export, voortgang, onopgeslagen werk en fouten. De native ribbon volgt nu per studio de voorgestelde tabs. FEM en BIM tonen hun eigen concepticonen als themagekleurde app-eigen SVG's; de publieke iconset blijft 22 canonieke betekenissen groot. | Per tool de echte inhoud, dialooginteractie en concrete foutafhandeling aan de broncode koppelen; concepttabs en -iconen vakinhoudelijk beoordelen. |
| Werkelijke migratie | Pointcloud gebruikt de gedeelde crate voor de complete buitenste venstercompositie, beide paneelkoppen, titelbalkiconen, zes beoordeelde algemene tooliconen en het Extensions-icoon, fonts, 77 Tauri-kleurvelden plus de stevige randkleur uit de merktokens per thema, ribbon- en formulierknoppen, invoervelden, keuzelijsten, checkboxen, sliders, voortgangsbalken, scrollbalken, tooltips en vijf vensterbandmaten. Ook de 27 px hoge dialoogknop met 75 px minimumbreedte en identieke tekstuitlijning wordt nu door de crate gebouwd en in beide apps gebruikt. De portable kopie is op 11 Rust-bestanden, 28 assets en dependencies gelijk gecontroleerd. De documenttabs staan vensterbreed; Light- en Forge-renders zijn met lege en geopende scan beoordeeld. Zes Pointcloud-renders zijn na deze controlintegratie bytegelijk gebleven; de instellingenrenders tonen de gesloten keuzelijsten in Light en Forge. | Domeinpanelen en dialogen op gedeelde widgets aansluiten zonder 3D-functionaliteit te verliezen; echte vensterscreenshots op meerdere platformen vergelijken. |

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
Rust-bronnen, zes fonts, drie OFL-licentieteksten en 22 canonieke iconen. De onderzoeksiconen,
FEM/BIM-concepten en reviewbeelden blijven in het niet-publiceerbare
Style Repo-package. De Root/Pointcloud-kopieën van code en assets worden
met `scripts/check_portable_ui.py` op inhoud gecontroleerd.

De [Energy-werkstroomreview](energy-workflow.html) toont nieuwbouw voor woning en utiliteit en de opnamevariant voor bestaande bouw in dezelfde kleur-, type- en vensterbandtaal. De routevolgorde volgt de broncode op commit e9a485d; de kaarten en invoervelden zijn ontwerpelementen en geen overgenomen berekeningsinterface. De gekoppelde handleidingscreenshot kan een andere historische schermstaat tonen. De Rust-crate heeft nu een optionele `ChromeMode::Workflow` met 32/30/22 px titel-, document- en statusbanden. De native atlas laat de vier brongebaseerde navigatiemodi kiezen: [nieuwbouw woning](style-repo-energy-workflow-light.png), [nieuwbouw utiliteit](style-repo-energy-workflow-utility-light.png), [bestaande bouw woning](style-repo-energy-workflow-existing-light.png) en [bestaande bouw utiliteit](style-repo-energy-workflow-existing-utility-forge.png). Bestaande-bouwonderdelen zijn klikbaar in de sidebar; de inhoudskaarten blijven een stijlproef, geen port van de Energy-rekenkern of de echte formulieren.

De Calc-audit op [broncommit b470427](https://github.com/OpenAEC-Foundation/open-calc-studio/blob/b47042704efa388d95eb59ce77d23aeb5ee0e44c/src/components/ribbon/Ribbon.tsx) corrigeert de eerdere generieke lintindeling. Het bronlint bestaat uit Bestand, Begroting, Offerte, Rapportage, Spreadsheet, 3D, PDF en IFC; Tekstopmaak verschijnt alleen bij een tekst- of witregel. Bij `VITE_HIDE_EXPERIMENTAL=true` verdwijnen Offerte, 3D en PDF. De [Nederlandse begrotingscapture](../harmonization/references/open-calc-studio/docs/screenshots/nl/1-begroting.png) toont een Start/Structuurkolom, brede hiërarchische tabel, Eigenschappenpaneel, documenttab boven en werkbladtab onder. Het [Nederlandse rapport](../harmonization/references/open-calc-studio/docs/screenshots/nl/2-rapport.png) is een aparte print-/exportsurface; de [Engelse tabeluitsnede](../harmonization/references/open-calc-studio/docs/screenshots/en/2-grid.png) toont de celhiërarchie. De [native lintpreview](style-repo-calc-ribbon-light.png) en HTML-atlas volgen nu de bronlabels en hoofdgroepen. De tabelinhoud in de atlas blijft een stijlproef: selectie, rijhoogtes, kolomset en rapportopmaak zijn nog geen pixelgelijke Rust-port.

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
