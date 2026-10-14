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
| Maatvoering | Titel 32 px, tabstrip 34 px, ribbon 100 px, documenttabs 32 px, status 26 px; standaardpanelen 240/260 px. | Vastgelegd in de Rust-crate en in het HTML-prototype zodat dezelfde app op alle tools identieke maten gebruikt. |
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
| FEM en BIM | 52 FEM- en 57 BIM-betekenissen zijn beschreven. | Unieke vectorvormen ontwerpen en op 16, 20 en 24 px toetsen. |
| Applicatieschermen | Start, werkgebied, bestand, instellingen en lege toestand zijn in het prototype navigeerbaar. | Import/export, voortgang, onopgeslagen werk en fouttoestanden per studio uitwerken. |
| Werkelijke migratie | Pointcloud gebruikt de gedeelde crate voor titelbalkiconen, fonts en 77 algemene kleurvelden per thema. | Ribbon, panelen en dialoogcomponenten gefaseerd op de gedeelde shell aansluiten zonder 3D-functionaliteit te verliezen. |

De huidige HTML-werkruimte is bewust een wireframe. Een generieke geometrische
placeholder is geen pixelgetrouwe PDF-, BIM- of Pointcloud-canvas. De bronindex
en deze beoordeling voorkomen dat die mockup als voltooide productscreenshot
wordt behandeld.
