# Visuele beoordeling · OpenAEC UI

Status: ontwerpbeoordeling van de huidige geharmoniseerde shell, 14 oktober 2026.
Dit document beoordeelt het ontwerp, niet de volledigheid van een toekomstige
migratie van alle OpenAEC-applicaties.

## Bronnen en zekerheid

- 68 repositoryrecords zijn geïnventariseerd: 63 publieke OpenAEC-repositories,
  de externe OpenCADStudio en vier niet toegankelijke of niet gevonden namen.
- 436 screenshotverwijzingen zijn op commit vastgelegd in `screen-index.json`;
  415 hebben een unieke Git-blobinhoud en 322 zijn als mogelijke
  applicatieschermen geclassificeerd. De classificatie
  bewijst niet dat het unieke pagina's of huidige productiestaten zijn.
- 565 bestanden hebben een concrete UI-codeverwijzing of de actieve
  pyRevit-knopbundelconventie. De overige SVG's, CAD-symbolen, illustraties en
  technische tekeningen horen niet bij die telling.
- 684 iconimports in broncode verwijzen naar 219 pakket/naamcombinaties.
  Daarvan zijn 312 versiegebonden SVG's uit Lucide Static en Solid Icons
  gedownload; deze categorie is apart geïndexeerd en visueel vergelijkbaar.
- De eerste visuele vergelijking gebruikt het Tauri Style Book, PDF Studio v2,
  Pointcloud native en de 36 lokaal bewaarde bruikbare UI-referenties. De
  interactieve index laat de andere bronbeelden per repository inspecteren.
- `dynlex` en `feat/rust-native` van PDF Studio waren niet publiek beschikbaar
  bij de bronaudit. PDF Studio v3 is als afzonderlijke Slint-bron meegenomen.

## Besluiten voor de gedeelde shell

| Onderdeel | Besluit | Onderbouwing |
| --- | --- | --- |
| Regio's | Titelbalk, ribbon-tabs, ribbon-groepen, documenttabs, verkenner, werkruimte, eigenschappen en status zijn vaste componenten. | Deze ordening is zichtbaar in de Tauri-template en meerdere studio's. |
| Maatvoering | Titel 32 px, tabstrip 28 px, ribbon 94 px, documenttabs 30 px en status 22 px volgens de Tauri-template; standaardpanelen in het prototype 240/260 px. | De Rust-crate en het HTML-prototype gebruiken nu dezelfde bronmaten. |
| Kleur | Vijf Style Book-thema's; amber is selectie/focus, niet een willekeurige betekenis van een domeinresultaat. | De bestaande apps mengen amber, grijs en vakspecifieke kleuren verschillend. |
| Lettertype | Inter voor bediening, Space Grotesk voor koppen en JetBrains Mono voor code/waarden. | Gebundelde bestanden maken de rendering onafhankelijk van systeemfonts. |
| Iconen | 24×24 semantische bedieningsiconen als canonieke set; vakinhoudelijke iconen krijgen een aparte betekenislaag. | Een maatlijn, een constraint en een gemeten afstand lijken op elkaar maar zijn andere opdrachten. |
| Responsive | Ribbon scrollt horizontaal; op smalle vensters verdwijnt eerst het eigenschappenpaneel. | Getest in het browserprototype bij circa 695 px viewportbreedte. |

## Beoordeling van de huidige proef

| Toets | Resultaat | Vervolg |
| --- | --- | --- |
| Herkenbare gedeelde shell | Voldoende voor conceptreview: 18 studio's gebruiken dezelfde regio's en vijf thema's. | Per studio de exacte commando- en tabgroepen aan de broncode koppelen. |
| Nette opmaak | De compacte browserproef heeft consistente uitlijning, randen en witruimte. | Native screenshots op meerdere platformen vergelijken met de HTML-maten. |
| Semantiek van iconen | De 21 huidige canonieke bedieningstekens zijn een begin; 565 bronbestanden zijn onderzoeksdata. | Groepeer synoniemen, beoordeel tegen light/dark en teken de definitieve domeinsets. |
| FEM en BIM | 52 FEM- en 57 BIM-betekenissen hebben elk een uniek SVG-concept; de atlas toont ze op 16, 24 en 32 px in lichte en donkere omgeving. | Complexe vormen op 16 px verfijnen en de 24 mogelijke bronmatches inhoudelijk vergelijken. |
| Applicatieschermen | Negen gedeelde schermtoestanden zijn in het prototype selecteerbaar, waaronder import/export, voortgang, onopgeslagen werk en fouten. FEM- en BIM-ribbons gebruiken nu hun eigen concepticonen en commando's. | Per tool de echte inhoud, dialooginteractie en concrete foutafhandeling aan de broncode koppelen. |
| Werkelijke migratie | Pointcloud gebruikt de gedeelde crate voor titelbalkiconen, fonts, 77 algemene kleurvelden per thema, ribbonknopstijlen en de vijf vensterbandmaten. De documenttabs staan nu vensterbreed; software-renders voor Light en Forge zijn visueel beoordeeld. | Overige panelen en dialogen op gedeelde widgets aansluiten zonder 3D-functionaliteit te verliezen; echte vensterscreenshots op meerdere platformen vergelijken. |

De huidige HTML-werkruimte is bewust een wireframe. Een generieke geometrische
placeholder is geen pixelgetrouwe PDF-, BIM- of Pointcloud-canvas. De bronindex
en deze beoordeling voorkomen dat die mockup als voltooide productscreenshot
wordt behandeld.

## FEM/BIM iconbeoordeling · ronde 1

De [visuele atlas](domain-icon-atlas.html) bevat 109 verschillende vectorvormen
in negen betekenisgroepen. Alle bestanden zijn XML-geldig. De native Style Repo
toont ze voor review; de publieke icon-API van de Rust-crate bevat ze nog niet.
In 24 gevallen bestaat
een gelijknamige bronkandidaat; zo'n match is geen bewijs van dezelfde functie.

| Toets | Waarneming | Ontwerpactie |
| --- | --- | --- |
| Familiebeeld | Het 24 px raster, donkere neutrale lijn en afgeronde einden zijn consistent. | Na semantische review dezelfde meetwaarden als canonieke Rust-iconen vastzetten. |
| Kleine maat | Eenvoudige vormen als staaf, kolom, wand en grid blijven herkenbaar op 16 px. Details in onder meer terrein, gebouw, federatie en complexe belastingtekens vallen op die maat samen. | Vereenvoudigde 16 px varianten tekenen voor iconen met meerdere interne lijnen. |
| Betekenisbotsingen | `bim.level` lijkt op een maatpijl; `bim.survey-point` en `bim.project-origin` delen een kruis/doel-motief; `fem.beam` en `bim.beam` hebben terecht andere context maar kunnen in een gezamenlijke zoeklijst verwarren. | Peilmarkering duidelijker maken, oorsprong/meetpunt verder uiteen trekken en domeinlabels in zoekresultaten tonen. |
| Licht/donker | Het ontwerp contrasteert op beide atlasachtergronden. Donkere weergave gebruikt een kleurinversie van de concept-SVG; de uiteindelijke crate moet themakleur toepassen in plaats van een CSS-filter. | SVG's pas na goedkeuring als themabewuste native assets genereren. |
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
