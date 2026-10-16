# Overdrachtsnotities

Gedeeld kladblok voor ChatGPT/Codex, Claude en de gebruiker. Werkwijze staat in [`AGENTS.md`](AGENTS.md).

## Nu bezig

<!-- Formaat: - **Assistent** – taak – bestanden/mappen – sinds JJJJ-MM-DD -->


















## Open punten

<!-- Onafgemaakt werk, vragen aan de gebruiker of bekende problemen. Verwijder een punt zodra het klaar is. -->

- Waarschuwingskleur: gebruiker wil oranje volgens overleg met Claude, maar `tokens-0.4.json` bevat nog geel. B2-review toont expliciet een oranje voorstel (Donker/Blueprint/HC donker `#FDBA74`, Licht `#9A3412`, HC licht `#7C2D12`). Gedeelde tokens en Claude-componenten zijn niet aangepast. Bij definitieve tokenkeuze voorstel vervangen door de gedeelde warning-rol.

- B2: dertien series, 116 ontwerpen/232 masters, revisie 23. Series 11–13 op `design/icon-set-b2/next-three-2.html`: Energie 3, Paalplan 7, Spraak/audio 5. Bepalende relatie nu geheel accent, geometrie behouden; andere 100 eerdere iconen bytegelijk behouden in `review/retained-series-1-10/`. 106 bronvoorbeelden, negen hergebruikkeuzes, 62 conflicten (177 records). Spraakiconen openen werkruimtes; thermische import heeft twee stapindicatoren en één deurgereedschap. Gedeelde broncluster DoorOpen heeft expliciet twee betekenissen via `canonical_functions`. Grote illustraties, paalsymbolen en app-logo’s zijn geen vaste bedieningsiconen. Vorige vormkeuzes behouden; warning-kleur blijft voorstel. Nog geen Rust-/app-integratie.

- Custom iconenset: gebruiker heeft B Constructief gekozen. De accentgeometrie van de 14 voorbeeldfuncties (28 masters voor 16/24 px) is herbouwd vanuit een vast 2D-vectormodel; voor/na staat in `design/icon-style-proposals/b-review.html`. Volgende stap: de gekozen familie uitbreiden per functioneel beoordeelde functie; dezelfde handeling mag over apps gecombineerd worden. A en C blijven referenties. Paletten op de proefpagina zijn losse voorbeelden, niet de thema’s die Claude beheert. De volledige iconenfamilie en Rust-integratie zijn nog niet gebouwd.

- Icoonset: het centrale overzicht staat in `design/function-icon-catalog.html`. De 2.854 bronrecords uit 6.326 vastgelegde bron-/assetbestanden zijn verzameld en technisch gevalideerd. Naam-/labelclusters en automatisch gevonden bronrollen vragen nog functionele beoordeling voordat de nieuwe set wordt vastgelegd; runtime-extensies en FEM blijven expliciete dekkingsgrenzen. De 1.487 clusters zijn geen telling van unieke functies of goedgekeurde iconen.

- Waarschuwing en informatie zijn nu beschikbaar als B2-SVG-ontwerp, samen met fout/geslaagd/bezig; meldingskleur via `currentColor` en de themarol. Opname in de nieuwe Rust-bibliotheek/componenten (2.4) volgt nog. Hoort bij 2.2 (Codex).
- Fase 2.1 fundament is besloten en staat in `design/ontwerp-0.4/tokens-0.4.json`. Volgende stappen: 2.2 iconen (Codex). 2.3 tegels is besloten, zie `design/ontwerp-0.4/03-tegels.md`. 2.4 componenten is besloten, inclusief het lint (variant B), ook de meldingen in Donker (Z2). 2.5 layouts staat als concept in `design/ontwerp-0.4/05-layouts.md` en is besloten. Fase 2 wacht nog op 2.2 iconen (Codex) en het overleg met de leidinggevende (2.6, samenvatting in `design/ontwerp-0.4/samenvatting.html`). De iconen van Codex worden de definitieve set en vervangen de tijdelijke iconen in alle voorbeeldpagina's. Waar de tokens uiteindelijk komen te staan, hoort bij fase 3.
- Welke licentie krijgt de bibliotheek? Het prototype gebruikt CC-BY-SA-4.0, die niet voor software bedoeld is. Voorstel Claude: LGPL-3.0, zoals de Foundation wil (repo-cleaner). Wacht op bevestiging.
- Open FEM Studio: repository gaf een 404 op GitHub. De gebruiker komt hier later op terug.

## Besluiten

- 2026-10-16: Screenshotronde serie 11–13: Openingen, Deur, Nieuw paalplan, Hernoemen, Kolommen en Coderingsconflicten anders; microfoon herkenbaarder, geluidsbogen ronder en vergaderaccent herstellen. Gebruiker sluit de opmerkingen af met "klaar".

- 2026-10-16: Bepalende relatie geheel in accentkleur; daarna de volgende drie onderwerpen uitwerken (Energie en warmte, Paalplan, Spraak en audio). Gebruiker vraagt opnieuw sneller door te werken.

- 2026-10-16: De eerste drie resterende onderwerpen samen uitwerken: Lijsten en bomen, Planning, Geotechniek. Gebruiker wil een hoger werktempo.

- 2026-10-16: Rapporten goedgekeurd ("perfect volgende"); volgende categorie maken en resterende categorieën met aantallen tonen. IFC-kubussen moeten betere, regelmatige vlakken krijgen, zo nodig vanuit een model (de gebruiker).

<!-- Vastgestelde uitgangspunten. Nieuwste bovenaan. Formaat: - JJJJ-MM-DD: besluit (bron). -->

- 2026-10-16: Energy en Field gaan naar de Rust-UI (keuze van Claude op verzoek van de gebruiker; Field opnieuw bekijken als tablet- of telefoongebruik nodig blijkt).
- 2026-10-16: PDF, Speech, Composer en Frame gaan naar de Rust-UI; alleen hun Solid- of Svelte-scherm wordt vervangen (de gebruiker).
- 2026-10-16: De gebruiker beslist zelf over het ontwerp; de 33 besluiten van fase 2 zijn vastgesteld en het ontwerp is bevroren als 0.4, behalve de iconen (lopen door bij Codex) (de gebruiker).
- 2026-10-16: De bron van tokens en ontwerp blijft de Style Repo (de gebruiker).
- 2026-10-16: De bibliotheek blijft voorlopig privé en wordt later openbaar (de gebruiker).
- 2026-10-16: De OpenAEC Installer hoort bij de harmonisatie. De Y/Z-app (Y-Next/Z-Next) doet de gebruiker los, apart van dit traject (de gebruiker).
- 2026-10-16: Tabelweergave: de bovenste horizontale rasterlijn aan de binnenkant moet accentkleur krijgen (de gebruiker).

- 2026-10-16: Projectmap zonder accent; Tabelweergave-accent gaat fout; alle grafiekstaafjes in accent en tabel/assen in hoofdkleur (de gebruiker).

- 2026-10-16: Tekstopmaak met aangepaste OpenAEC-lettervormen is goedgekeurd ("perfect door naar de volgende") (de gebruiker).

- 2026-10-16: De letters van Vet, Cursief, Onderstrepen en Tekstkleur moeten meer aansluiten op het OpenAEC-thema en lettertype (de gebruiker). Codex gebruikt de gebundelde Space Grotesk als contourbron; B Bold, I/U/A Medium, I synthetisch schuin.

- 2026-10-16: Vensters en panelen is goedgekeurd ("perfect volgende"); doorgaan met de volgende functiegroep (de gebruiker).

- 2026-10-16: Resterende functiegroepen één voor één uitwerken en beoordelen (de gebruiker). Codex begint met Vensters en panelen, daarna volgende groep op basis van de review.

- 2026-10-16: Tekst toevoegen: alternatief met de gehele T in accentkleur. Cirkel tekenen: B met constructiestraal in accent. Gebruiker sluit af met "en dan is deze oke" (de gebruiker).

- 2026-10-16: Tweede screenshotronde: Tekst toevoegen geheel in hoofdkleur of geheel in accent, geen gedeeltelijk accent; Raster kiest het alternatief met alle binnenlijnen accent; Hulp-vraagteken iets kleiner voor meer marge; kwartsegment bij Cirkel nog niet de juiste oplossing (de gebruiker).

- 2026-10-16: Screenshotfeedback serie 2: aangesloten arcering voor oppervlak, ander cirkelaccent, tekstaccent herstellen, hele T in tekstvak accent, hulplijnen vrij van maatpijlen, ronde oogvormen, uitlijnas accent links/rechts, raster buitenrand of alle binnenlijnen accent, alle drie instellingsknoppen accent, oranje waarschuwing, Bezig eventueel klok/animatie, vloeiend vraagteken. Aanvullend: Veelhoek anders dan vierkant en Rechthoek met de vier accenthoekpunten (de gebruiker).

- 2026-10-16: Vierkante dingen in B2 mogen strakker: een vierkant moet gewoon een vierkant zijn, minder losjes (de gebruiker). Toegepast als haakse, regelmatige vormen met kleinere zachte hoeken in serie 2.

- 2026-10-16: Gebruiker geeft opdracht door te gaan na de nieuwste pijlaansluiting; eerste 31 B2-iconen vormen de behouden basis voor uitbreiding (de gebruiker).

- 2026-10-16: Werkstroom-apps: zijbalk of stappen via instelling Navigatie, standaard zijbalk. Statusbalk volgt het thema (in Licht licht); instelling Statusbalk kan hem altijd donker maken (de gebruiker; de statusbalkinstelling is door Claude toegevoegd naar het voorbeeld van de werkruimte).
- 2026-10-16: Startscherm bij het openen, met instelling "Laatste project direct openen"; start de app vanuit een bestand, dan opent dat bestand direct (de gebruiker).
- 2026-10-16: Bij de pijlen mag de steel in de hoofdkleur tot in de aanwijzer doorlopen; afgeronde aansluiting behouden (de gebruiker).

- 2026-10-16: Werkruimte volgt standaard het gekozen thema (Donker dus donker, `#26262D`); gebruikers kunnen het aanpassen met de instelling Werkruimte: Volgt thema, Altijd licht, Altijd donker. Vervangt het eerdere besluit voor een lichte werkruimte in Donker (de gebruiker).
- 2026-10-16: Met "blenden" bedoelt de gebruiker een afgeronde geometrische aansluiting, geen kleurverloop. Nieuwe vormen van Terug/Vooruit zijn goed, aansluitingen aanpassen. Documentplus tussen de vorige linksonder- en middenpositie zetten (de gebruiker).

- 2026-10-16: Meldingen in Donker: zachte maar volle tint, volle statuskleur voor 28% over het paneel (Z2) (de gebruiker). Claude heeft dezelfde regel op Blueprint toegepast.
- 2026-10-16: Afdrukken is goed. Nieuw document: plus meer naar het midden. Opslaan als en Plakken opnieuw ontwerpen. 3D-beeld draaien terug richting oude bol met omloop. Bij Ongedaan/Opnieuw en Terug/Vooruit hoofdkleur en accent meer laten overlopen; de aansluitingen van Terug/Vooruit herstellen (de gebruiker).

- 2026-10-16: Lint en documenttabs volgen variant B: licht en vlak, naar de website (de gebruiker).
- 2026-10-16: Accent niet altijd onder de hoofdkleur; per icoon beoordelen. Gebruiker noemt Afdrukken, Ongedaan maken, Opnieuw uitvoeren, Plakken, Terug en Vooruit voor accent vóór. Nieuw document, Opslaan als en 3D-beeld draaien vragen daarnaast vormcorrecties. Dit vervangt de eerdere algemene regel over de laagvolgorde (de gebruiker).

- 2026-10-16: Knoppen blijven bij hover en ingedrukt in dezelfde kleur, iets lichter en iets donkerder (variant A) (de gebruiker).
- 2026-10-16: Componenten: bediening 28 px, compact 24 px; tooltips in de kleur van het thema; meldingen rechtsonder verdwijnen na vijf seconden, behalve fouten (de gebruiker). Hover- en ingedrukt-kleuren van knoppen passen niet bij de thema's en worden herzien.
- 2026-10-16: Gebruiker bevestigt B2 met accent onder de hoofdkleur ("veel beter") en geeft opdracht te beginnen met de functielijst en eerste familie bestanden/bewerken/navigeren ("aan de slag dan maar").

- 2026-10-16: Tegels: taaktegels volgens variant B (icoontegel links, rand); startscherm met projectkaarten voor apps die met projecten werken; voorbeeldbeeld op projectkaarten waar mogelijk, anders het app-icoon (de gebruiker).
- 2026-10-16: B2 wordt de basis: meer ronde vormen voor een moderne zachte uitstraling. Accentlijnen liggen onder de witte lijnen; technisch betekent dit accent eerst en thema-afhankelijke hoofdkleur daarna (de gebruiker).

- 2026-10-16: B Constructief wordt de richting voor de custom iconenset; de accentlijnen moeten zorgvuldig gecorrigeerd worden (de gebruiker). Codex heeft hiervoor een 2D-vectormodel met gedeelde ankerpunten toegepast; de herziening staat ter beoordeling op de voor/na-pagina.
- 2026-10-16: Akkoord op statuskleuren per thema, drie niveaus schaduw en de toestanden geselecteerd en uitgeschakeld. Fase 2.1 fundament is daarmee volledig besloten (de gebruiker).
- 2026-10-16: Akkoord op vaste lettergroottes (11/12/13/16/22 px, mono-labels 11 px), afstanden op een raster van 4 px, en teksten uit vertaalbestanden (de gebruiker).
- 2026-10-16: Desktopapps houden de maten van de Tauri-template; knoppen en andere onderdelen worden wel opnieuw ontworpen. Blueprint houdt een blauw accent. WCAG 2.2 AA is definitief het doel (de gebruiker).
- 2026-10-16: Hoeken variant D (3, 6 en 10 px); donker thema met lichte werkruimte zoals Forge; High contrast in een donkere en een lichte variant; Blueprint wordt bijgewerkt voor contrast (de gebruiker).
- 2026-10-16: Fundament: thema's volgen de vlakken van de website; Forge en OpenAEC samengevoegd tot één donker thema; Blueprint blijft; High contrast krijgt nieuwe kleuren; Night Build `#2A2A32`; primaire knop donkere tekst op amber; mono-labels; minimaal 11 px; Nederlands als standaardtaal; WCAG 2.2 AA voorlopig. Zie *Besluiten* in `design/ontwerp-0.4/01-fundament.md` (de gebruiker).
- 2026-10-16: De website open-aec.com wordt niet aangepast. De apps lossen contrastproblemen zelf op (de gebruiker).
- 2026-10-16: Open 2D Studio is gestopt, dus de AEC-extensie valt buiten de scope. Er blijven 16 apps over (de gebruiker).
- 2026-10-16: Open FEM Studio blijft in de scope, maar wacht tot de gebruiker erop terugkomt (de gebruiker).
- 2026-10-16: Scope is alleen de apps uit `design/harmonized.html`, zonder Open CAD Studio en Open BIM Studio. Zie `APP-OVERZICHT.md` (de gebruiker).
- 2026-10-16: Open BIM Studio hoeft niet geharmoniseerd te worden (de gebruiker).
- 2026-10-16: Y-Next en Z-Next zijn varianten van dezelfde app, de Y-app op ERPNext (de gebruiker).
- 2026-10-16: Doel is dat elke app binnen de scope dezelfde stijl heeft (kleuren, tegels, iconen enzovoort), ongeacht de techniek (de gebruiker).
- 2026-10-16: Open CAD Studio valt buiten de harmonisatie; daar wordt niets aan veranderd (de gebruiker).
- 2026-10-16: Tools zoals Open Calc Studio worden omgebouwd naar de nieuwe UI (de gebruiker, na overleg met leidinggevende).
- 2026-10-16: Y-Next en Z-Next zijn communicatie-apps, een eigen soort interface naast ribbon-tools, webachtige tools en de installer.
- 2026-10-16: De UI-bibliotheek versie 0.4 wordt vanaf nul opnieuw gebouwd. De huidige crate `openaec-ui` 0.1.0 en de reviews in deze repo dienen als prototype en ontwerpbron.
- Volgorde van het werk: ontwerpen in de Style Repo, dan bibliotheek 0.4 bouwen, dan tools ombouwen, te beginnen met Open Calc Studio.

## Logboek

<!-- Nieuwste bovenaan. Formaat: - JJJJ-MM-DD **Assistent**: wat er gedaan is. -->

- 2026-10-16 **Codex**: gebruiker vraagt alle huidige wijzigingen samen te committen en na het weekend verder te gaan. Hervatten bij review `design/icon-set-b2/next-three-2.html`, 116 iconen, revisie 23; potloden van Hernoemen en Legenda zijn als laatste aangepast. Overige bronkandidaten en Rust-/app-integratie blijven open. Werk van Claude wordt meegenomen. Geen push en geen automatische vervolgtaak. Tokencontrole: vijf thema’s en 190 contrastparen slagen. Bron-SVG’s behouden oorspronkelijke witruimte voor hun exacte hashes; staged witruimtecontrole slaagt buiten die bronkopieën. `.gitattributes` bewaart exacte bytes van iconen, metadata en nieuwe scripts, zodat Git de SHA-256-invoer niet door regeleinden verandert.


- 2026-10-16 **Codex**: Hernoemen en Legenda krijgen één gedeeld potloodmodel: parallelle schacht, gelijke hoek, punt op dezelfde as; op 16 px minder detail. Naamveld 1 eenheid smaller voor vrije ruimte naast potlood. Vorige 116 in `review/before-pencil-fix/`, overige 114 bytegelijk behouden. Revisie 23, review/manifest/ZIP/README bijgewerkt. Checker slaagt voor 232 masters, behoud, bron/hash/ZIP en bestaande geometrie-/contrastcontroles. Visueel op 16/24/32 px in donker bekeken; `preview-pencils.png`. Claude-werk behouden; geen Rust/Cargo-wijziging; niets gecommit/gepusht.


- 2026-10-16 **Codex**: negen iconen herzien op screenshotfeedback, revisie 22. Raamopening in gevel, frontale deur met knop, funderingspaal/grondlijn, naamveld met potlood, kolomkeuze met vinkje, dubbele codes met uitroepteken, capsulemicrofoon, echte cirkelbogen voor geluid en volledige tweede persoon in accent. Vorige 116 iconen in `review/before-round-11-13/`; exportchecker toetst behoud van de overige 107. Review/manifest/ZIP/README vernieuwd; negen iconen visueel op 16/24/32 px in donker bekeken, `preview-feedback-11-13.png` opgeslagen. Claude-werk behouden, Rust ongewijzigd; geen Cargo nodig, niets gecommit/gepusht.


- 2026-10-16 **Codex**: Bepalende relatie geheel accent via rootkleur, vorm vergeleken met vorige masters. Series 11–13 toegevoegd: 15 ontwerpen uit Heatloss/Pile Plan/Speech, met zeven extra hergebruikkeuzes en elf bronconflicten. Broncluster met meerdere functies expliciet als lijst gemodelleerd; filters bijgewerkt. Eerste 100 overige ontwerpen bytegelijk behouden. Gecombineerde en afzonderlijke seriepagina’s, manifest/ZIP en README vernieuwd. Nieuwe iconen visueel op 16/24/32 px bekeken in donker; screenshot `preview-next-three-2.png`. JS-syntax en `git diff --check` slagen. Exportcontrole apart uitgevoerd. Claude-werk behouden, Rust niet gewijzigd, geen Cargo nodig; niets gecommit/gepusht.


- 2026-10-16 **Claude**: B2-iconen `tree.expand` en `tree.collapse` (serie 8) gebruikt in de boom en de inklapbare secties van `componenten-review.html` en `layouts-review.html`. Tijdelijk blijven: vinkje, keuzelijstpijl, submenupijl, hernoemen, kubus, raster-als-onderdeel, recente bestanden en de navigatie-iconen van Energy en Field; daar heeft B2 nog geen icoon met dezelfde betekenis.
- 2026-10-16 **Codex**: series 8–10 gebouwd via `b2_tree_planning_geo.py`, 13 nieuwe ontwerpen/26 masters. Twee expliciete hergebruikkeuzes; veertien bronconflicten apart gezet. Boring, sonderingsraster en RD-coördinaat uit verkeerd ingedeelde bronclusters toegevoegd. Eén gezamenlijke review plus drie afzonderlijke seriepagina’s. Canonieke functie-ID’s gekoppeld aan oorspronkelijke broncluster-ID’s in manifest/werklijst; gecombineerde serie-/bronfilters toegevoegd. Ongewijzigde oude ontwerpen worden bij identiek model en SHA-256 behouden voor snellere generatie; onafhankelijke exportchecker controleert alle bytes. Checker slaagt: 202 exporten, behoud eerdere 88, 124 laagvarianten, acht alternatieven, drie foutcontroles, 40 contrasten, hashes/brondekking/fontlicentie en ZIP 205 bestanden. JS-syntax en `git diff --check` slagen. Nieuwe iconen visueel bekeken op 16/24/32 px in donker/licht en monochroom; `preview-next-three.png`. README bijgewerkt inclusief Claude’s 0.4-HTML-themaopmerking; Claude-werk behouden. Rust ongewijzigd, geen Cargo nodig; niets gecommit/gepusht.


- 2026-10-16 **Claude**: besluiten over Energy, Field en de Solid/Svelte-apps vastgelegd in `STAPPENPLAN.md`; licentievoorstel LGPL-3.0.
- 2026-10-16 **Claude**: antwoorden op de overlegvragen verwerkt in `STAPPENPLAN.md`, `APP-OVERZICHT.md`, `tokens-0.4.json` (versie 0.4.0) en de samenvatting. Installer in scope; Y/Z-app doet de gebruiker apart.
- 2026-10-16 **Codex**: serie 6 Rapporten afgerond (revisie 17) en door gebruiker goedgekeurd. Serie 7 IFC en BIM toegevoegd via `b2_ifc_series.py`; drie concrete bronvoorbeelden uit Frame/Calc/BIM Validator, twee foutieve validatiebetekenissen apart gezet. Op screenshotfeedback kubus vanuit orthografisch isometrisch eenheidsmodel herbouwd (revisie 19); gelijke ribben en identieke geometrie voor drie functies gecontroleerd. Eerste 85 mastersparen bytegelijk behouden, eerdere IFC-vormen in `review/ifc-before/`. Checker slaagt: 176 exportmasters, 124 historische laagvarianten, acht alternatieven, drie foutcontroles, bron-/generator-/font-/ZIP-hashes, 40 contrasten en ZIP met 179 bestanden. JavaScript-syntax slaagt. Drie iconen op 16/24/32 px visueel gecontroleerd in donker/licht en monochroom; `preview-series-7.png` vernieuwd. Resterende categorieën geteld: 1.400 bronkandidaten, nadrukkelijk geen unieke iconen. README bijgewerkt. Claude-wijzigingen behouden, Rust ongewijzigd, geen Cargo nodig; niets gecommit/gepusht.


- 2026-10-16 **Claude**: `design/harmonized.html` gebruikt nu ontwerp 0.4. `scripts/build_harmonized_prototype.py` vult de oude `--theme-*`-variabelen uit `tokens-0.4.json` (vijf nieuwe thema's), voegt lint B, hoeken, mono-labels en paneelkoppen toe, en leest en schrijft nu in UTF-8. De sjabloonpagina is ongewijzigd; een herbouw zonder 0.4-toevoegingen leverde exact de oude pagina op.
- 2026-10-16 **Codex**: revisie 16 geeft de bovenste tabelbinnenlijn een ononderbroken accent. Accent vóór kolomverdelers, eindpunten binnen de hoofdgekleurde buitenrand. Alleen tabel gewijzigd; eerdere masters in `review/data-header-before/`. Silhouetbehoud, doorlopend accent bij elke kolom en hoofdgekleurde buitenrand op beide masters gecontroleerd. Checker slaagt voor 166 masters, behoud eerste 80, hashes/font/licentie/ZIP, 124 laagvarianten, acht alternatieven, 40 contrasten en drie foutcontroles. Visueel op 16/24/32 px bekeken; screenshot `preview-table-header.png`. Claude-werk en Rust behouden; geen Cargo-controle; niets gecommit/gepusht.

- 2026-10-16 **Codex**: revisie 15 corrigeert de kleurverdeling van de drie gegevensiconen: Projectmap/Tabelweergave geheel hoofdkleur, Grafiekweergave drie accentstaafjes en hoofdgekleurde assen. Vorige masters in `review/data-accent-before/`; silhouetten op 16/24 px gecontroleerd en behouden. Hoofdreviews/manifest/ZIP vernieuwd. Checker slaagt voor 166 masters, behoud eerste 80, hashes/font/licentie/ZIP, 124 laagvarianten, acht alternatieven, 40 contrasten en drie foutcontroles. Visueel op 16/24/32 px bekeken; screenshot `preview-data-accents.png`. Claude-werk en Rust behouden; geen Cargo-controle; niets gecommit/gepusht.

- 2026-10-16 **Codex**: serie 5 Projecten en gegevens: Projectmap, Tabelweergave en Grafiekweergave (zes masters) met drie expliciet gelezen bronaanroepen. Vier afwijkende aanroepen voor tabel invoegen/downloadstatistieken/urenverdeling apart gezet. Totaal 83 functies/166 masters, manifest revisie 14, ZIP 169 bestanden; eerste 80 iconen bytegelijk behouden. Checker slaagt voor exporten, font-/generatorhashes, 124 laagvarianten, acht alternatieven, 40 contrasten, bron/ZIP/licentie en drie foutcontroles; JS-syntax slaagt. Drie iconen op 16/24/32 px in donker/licht en monochroom bekeken; screenshot `preview-series-5.png`. Claude-claim en werk behouden; geen Rust-wijziging/Cargo-controle; niets gecommit/gepusht. Volgende groep nog niet gestart.

- 2026-10-16 **Claude**: tegel-, componenten- en layoutpagina gebruiken nu de B2-iconen van Codex via `scripts/review_icons.py` (alleen lezen uit `design/icon-set-b2/svg/`, als `<symbol>` één keer per pagina). Oude prototype-iconen alleen nog voor cube, grid, check, controls, rename, measure en de uitklappijltjes. Statusiconen voor meldingen komen nu uit B2.
- 2026-10-16 **Codex**: vier lettericonen herbouwd uit gebundelde Space Grotesk-fonts; gevulde vectorcontouren zonder runtime-font. `b2_font_geometry.py`, FontTools 4.60.1 gepind, glyph/gewicht/font-SHA/helling in manifest revisie 13, SIL OFL 1.1-licentie mee in ZIP (163 bestanden). Vorige vier masters in `review/typography-before/`; overige 76 iconen behouden, waaronder de drie tekstuitlijningen. Checker slaagt voor 160 masters, font-/generatorhashes, 124 laagvarianten, acht alternatieven, 40 contrasten, ZIP/licentie en drie foutcontroles. B/A-binnenruimtes gecontroleerd; op 16/24/32 px in donker/licht en monochroom bekeken; screenshot `preview-typography.png`. Claude-werk en Rust behouden; geen Cargo-controle nodig; niets gecommit/gepusht.

- 2026-10-16 **Codex**: serie 4 Tekstopmaak gebouwd: zeven functies/14 masters, zes expliciete bronvoorbeelden; tekstkleur als ontwerpcontract, twee Planner-kleurplaatsen als betekenisbotsing gemarkeerd. Tekstuitlijning apart van objectuitlijning. Totaal 80 functies/160 masters, manifest revisie 12, ZIP 162 bestanden. Eerste 73 iconen bytegelijk behouden. Checker slaagt voor exporten, 124 laagvarianten, acht alternatieven, 40 contrasten, bron/hashes/ZIP en drie foutcontroles; JS-syntax slaagt. B-contour verbonden en U vrij van onderstreping gecontroleerd; zeven iconen visueel bekeken op 16/24/32 px in donker/licht en monochroom, screenshot `preview-series-4.png`. Claude-werk en Rust behouden; geen Cargo-controle nodig; niets gecommit/gepusht. Volgende groep nog niet gestart.

- 2026-10-16 **Codex**: serie 3 Vensters en panelen gebouwd (acht functies/16 masters), met acht expliciet gelezen bronaanroepen. Maximaliseren/herstellen/volledig scherm onderscheiden; generieke Sluiten-cluster niet automatisch overgenomen. `scripts/b2_window_series.py`, eigen seriefilter en `series-3.html`; totaal 73 functies/146 masters, manifest revisie 11 en ZIP 148 bestanden. Alle eerste 65 masters bytegelijk behouden. Checker slaagt voor 146 masters, 124 laagvarianten, acht alternatieven, 40 contrasten, bron/hashes/ZIP en drie foutcontroles. JS-syntax slaagt; alle acht op 16/24/32 px in donker/licht en monochroom bekeken, seriefilters 8/34/73 gecontroleerd; screenshot `preview-series-3.png`. Claude-werk en Rust behouden, geen Cargo-controle nodig; niets gecommit/gepusht. Volgende functiegroep nog niet gestart.

- 2026-10-16 **Codex**: keuzes vastgelegd in revisie 10: Cirkel B bytegelijk aan het gekozen alternatief op 16/24 px; T krijgt volledige accentkleur via SVG-kleurrol (`whole_icon_accent` in manifest), met fallback en monochroom. Eerdere twee ontwerpen bewaard in `review/selected-before/`. Hoofdoverzicht, feedback, manifest en ZIP vernieuwd. Checker slaagt voor 130 masters, 124 laagvarianten, acht alternatiefmasters, hashes/ZIP, drie foutcontroles en 40 contrasten. Hoofdoverzicht visueel bekeken; paarse accentkleur en monochrome T in browser gecontroleerd, screenshot `preview-selected.png`. Gedeelde thema’s/Claude-werk behouden; geen Rust/Cargo-wijziging; niets gecommit/gepusht.

- 2026-10-16 **Codex**: revisie 9: Raster bytegelijk aan gekozen binnenlijnen-alternatief; Hulp-vraagteken 20% verkleind met gelijk buitenkader en lijndikte; Tekst één kleur met geheel-accentvariant via kleurrol; Cirkel drie opties (geen/straal/middelpunt), neutrale export voorlopig zonder accent. Vier iconen gewijzigd, overige 61 bytegelijk, inclusief de eerste 31. Snapshot `review/feedback-round-2-before/`; hoofdreview/feedback/manifest/ZIP vernieuwd. Checker slaagt voor 130 masters, 124 laagvarianten, acht alternatiefmasters, hashes/ZIP, drie foutcontroles en 40 contrasten; JavaScript-syntax slaagt. Op 16/24/32 px visueel bekeken, licht/donker en tekstmonochroom gecontroleerd; screenshot `preview-feedback-round-2.png`. Claude-werk behouden; geen Rust-wijziging/Cargo-controle; niets gecommit/gepusht.

- 2026-10-16 **Codex**: revisie 8 verwerkt alle screenshotfeedback: veertien SVG-vormen herzien, 51 iconen bytegelijk behouden (inclusief eerste 31); waarschuwing als oranje reviewvoorstel, Bezig met CSS-animatie/uitknop/minder-beweging-regel. Zestien voor/na-kaarten in `feedback.html`, vier alternatiefmasters voor raster-binnenlijnen en klokje, eerdere SVG’s in `review/feedback-before/`. Arceringsfragmenten bij de buitenhoeken gevonden en hersteld; drie aangesloten binnenlijnen en vrije maatpijlen op beide masters gecontroleerd. Checker slaagt voor 130 SVG’s, 124 laagvarianten, vier alternatiefmasters, hashes/ZIP, drie foutcontroles en 40 contrasten. JavaScript-syntax gecontroleerd; alle zestien reviewkaarten visueel bekeken op 16/24/32 px, licht/donker, vijf themawaarden, monochroom en animatie aan/uit gecontroleerd. Screenshot `preview-feedback.png`. Geen Rust-wijzigingen/Cargo-controle; Claude-bestanden behouden, kleurafstemming staat open. Niets gecommit/gepusht.

- 2026-10-16 **Codex**: revisie 7 maakt tien iconen van serie 2 strakker: haakse polylijn/veelhoek, vierkant bij rechthoek en oppervlak, kleinere vaste hoekafronding voor tekstvak/leidlijn/rotatie/slot/raster. Vorige masters bewaard in `review/square-before/`; overige 55 iconen behouden, inclusief alle 31 kerniconen. Hoofdreviews, manifest en ZIP vernieuwd. Checker slaagt voor 130 masters, 124 laagvarianten, hashes/ZIP, brondekking, drie foutcontroles en 35 contrasten. Visueel bekeken op 16/24/32 px in de relevante groepen, oppervlak ook in licht; `preview-squared.png`. Alleen iconen en eigen documentatie aangepast; Claude-werk behouden. Geen Rust-wijziging of Cargo-controle; niets gecommit/gepusht.

- 2026-10-16 **Claude**: stap 2.6: `scripts/build_samenvatting_04.py` maakt `design/ontwerp-0.4/samenvatting.html` uit de besluittabellen (33 besluiten), met open punten voor het overleg en voorwaarden om te bevriezen.
- 2026-10-16 **Codex**: tweede B2-serie met 34 functies gebouwd (65 totaal, 130 masters), eigen seriefilter/review, 29 extra bronvoorbeelden en twaalf extra betekenisconflicten. Eén nieuw informatie-meldingscontract apart van de 1.487 oorspronkelijke clusters. Statusiconen gebruiken uitsluitend de semantische themakleur. Eerste 31 masters bytegelijk behouden. Checker slaagt voor 130 exporten, 124 laagvarianten, bron/hash/ZIP-controles, drie foutcontroles en 35 contrasten. Nieuwe groepen visueel op 16/24/32 px bekeken; statuskleuren in de vijf thema’s en seriefilters gecontroleerd. Geen Rust- of Claude-themawijzigingen, geen Cargo-controle nodig; niets gecommit of gepusht.

- 2026-10-16 **Claude**: statusbalk in Licht is nu `panel` met `text-secondary` en een lijn erboven; `statusbar-setting` toegevoegd aan `tokens-0.4.json`. Instellingen Werkruimte, Statusbalk en Navigatie beschreven in `04-componenten.md`; stap 2.5 besloten in `05-layouts.md`. Controle: 190 kleurparen, alles haalt het minimum.
- 2026-10-16 **Claude**: `layouts-review.html` heeft nu een vergelijking van Energy en Field in beide werkstroomvormen, en een vergelijking van een donkere en lichte statusbalk in Licht.
- 2026-10-16 **Claude**: stap 2.5 gestart. `scripts/build_layouts_review.py` maakt `layouts-review.html` met zes kernschermen van Open Calc Studio en twee werkstroomschermen (zijbalk zoals Energy, stappen zoals Field), wisselbaar tussen de vijf thema's. Specificatie in `05-layouts.md`.
- 2026-10-16 **Codex**: revisie 5: bij vier pijlen het primaire kleurvlak doorgetrokken tot in de aanwijzer; buitenvorm en afgeronde aansluiting behouden. Overige 27 iconen bytegelijk aan vorige revisie; snapshot `review/stem-before/`. Voor/na, manifest, hoofdreview en ZIP bijgewerkt; nieuwste gedeelde thematokens opnieuw ingelezen na gelijktijdige wijziging elders. Checker slaagt voor 62 SVG’s + 124 laagvarianten, acht steekproeven voor hoofdgekleurde steel bij de pijlpunt, behoud van silhouetten, hashes, ZIP, drie foutcontroles en tien thema-contrasten. Visueel bekeken op 16/24/32 px in licht/donker; screenshot `preview-stems.png`. Claude-bestanden en Rust-code niet gewijzigd; geen Cargo-controle nodig. Niets gecommit of gepusht.

- 2026-10-16 **Claude**: werkruimte in Donker is nu `#26262D` met tekst `#EDEBE8`; `workspace-setting` toegevoegd aan `tokens-0.4.json` met de drie keuzes. Specificaties bijgewerkt en de instelling beschreven in `04-componenten.md`.
- 2026-10-16 **Claude**: voorbeeld toegevoegd in sectie 11b van `componenten-review.html`: Donker met lichte werkruimte (nu) naast donkere werkruimte `#26262D`, voor een tabel en een tekening. Keuze ligt bij de gebruiker.
- 2026-10-16 **Codex**: revisie 4: verloop verwijderd uit alle actuele SVG’s, vier pijlen uit één silhouet langs een afgeronde kleurgrens verdeeld, buitenvorm gelijk aan vorige revisie. Plus op (12,13.5) in 24px-model, exact halverwege beide eerdere posities. Vijf vergelijkingen met de vorige revisie; hoofdoverzicht, manifest en ZIP bijgewerkt. Checker slaagt: 62 exporten + 124 varianten, geen verlopen/extra definities, behoud van 26 iconen en vier pijlsilhouetten, hashes, ZIP, drie foutcontroles en tien contrasten. Browser op 16/24/32 px in donker/licht bekeken; nieuwe uitvoering bevat nul verlopen en monochroom toont één kleur. Screenshot `preview-rounded-joints.png`. Claude-werk en Rust niet gewijzigd; geen Cargo-controle nodig; niets gecommit of gepusht.

- 2026-10-16 **Claude**: app-achtergrond rond dialoog en lege staat teruggedraaid op verzoek. De lege staat volgt nu de kleuren van het thema (`panel`, `text`, `accent-text`) in plaats van de lichte werkruimte; in Donker dus donker.
- 2026-10-16 **Claude**: dialoog en lege staat op de componentenpagina staan nu in een kleine app-achtergrond; de lege staat heeft geen kader meer en gebruikt werkruimtekleuren. Op verzoek van de gebruiker, omdat Donker niet goed oogde.
- 2026-10-16 **Claude**: Z2 doorgevoerd. `tokens-0.4.json` heeft nu `error-tint`, `success-tint`, `warning-tint` en `info-tint` per thema; `status-tint-alpha` is vervallen. Controle, fundament-, tegel- en componentenpagina gebruiken de nieuwe tokens; alles haalt de norm.
- 2026-10-16 **Codex**: acht iconen verfijnd volgens feedback; Afdrukken en overige 22 iconen gelijk aan vorige revisie. Documentplus gecentreerd, diagonale pen met vrijgehouden ruimte op diskette, klembord met vel/invoegpijl, bol met gekantelde ellips. Vier pijlen: uitstekende steeluiteinden hersteld en kort SVG-verloop van accent naar hoofdkleur toegevoegd. Manifest revisie 3, hoofdreview/voor-na/laagreview/ZIP bijgewerkt; snapshots in `review/refinement-before/`. SVG-instanties krijgen unieke verloop-ID’s. Checker slaagt voor 62 exporten + 124 laagvarianten, drie foutcontroles, bron-/hash-/ZIP-controles, behoud van 23 iconen en 105 contrastmetingen (incl. 95 verloopkleuren). Browser: acht iconen op 16/24/32 px bekeken in donker/licht; monochroom maakt beide verloopstops dezelfde kleur; 16 verloop-ID’s zijn uniek. Geen wijzigingen aan Claude-thema’s of Rust; geen Cargo-controle nodig. Niets gecommit of gepusht.

- 2026-10-16 **Claude**: gebruiker kiest zachte meldingen in Donker, maar minder licht. Sectie 10b toont nu de huidige tint naast Z1 (volle kleur 20%), Z2 (28%) en Z3 (diep 50%); alle halen de norm.
- 2026-10-16 **Claude**: meldingen in Donker vergeleken: huidige 18%-tint (verzadiging 0,09 tot 0,24) naast de diepe Style Book-achtergronden (0,61 tot 0,78), in sectie 10b van `componenten-review.html`. Beide halen de norm.
- 2026-10-16 **Claude**: focusring staat in dichte onderdelen (lint, menu's, boom, tabellen, documenttabs) nu binnen het onderdeel; bij losse knoppen en velden blijft hij buiten. Op verzoek van de gebruiker, omdat de ring tegen buren aan kwam.
- 2026-10-16 **Claude**: lintvariant B vastgelegd in `04-componenten.md`; componentenpagina toont B als besloten, met focusvoorbeeld, en de themastrook gebruikt de tabs van B.
- 2026-10-16 **Claude**: gebruiker vindt het lint te veel als de oude template. Drie lintvarianten toegevoegd aan `componenten-review.html` (A template, B licht en vlak, C donkere kopbalk), met dezelfde maten. 185 contrastparen halen hun minimum.
- 2026-10-16 **Codex**: zes door gebruiker genoemde iconen krijgen accent vóór; laagvolgorde en reden per icoon in `b2_geometry.py` en manifest revisie 2. Drie vormen hertekend: aangesloten documentvouw, diskette met losse pen, cirkelpijl rond kubus. Voor/na-review (`shapes.html`) en laagvergelijking (`layers.html`), 62 eerdere masters bewaard. Generator bijgewerkt, hoofdoverzicht en ZIP vernieuwd. `check_icon_set_b2.py` slaagt voor 62 gekozen exporten + 124 laagvarianten, gelijk silhouet tussen laagvarianten, 22 ongewijzigde iconen, drie foutcontroles, hashes, ZIP en thema-contrasten. Zes aansluitingen en drie vormen visueel op 16/24/32 px bekeken; licht/donker en monochroom gecontroleerd. Claude-thema’s/lintvarianten en Rust-code niet gewijzigd; geen Cargo-controle nodig. Niets gecommit of gepusht.

- 2026-10-16 **Claude**: variant A verwerkt. `tokens-0.4.json` heeft nu `accent-pressed`, `hover` en `pressed` per thema, en `accent-hover` is in Licht en Donker `#E78A08`. Blueprint-fout is `#FCA5A5`. `check_tokens_04.py` toetst 177 paren; de componentenpagina 165 paren; alles haalt het minimum.
- 2026-10-16 **Codex**: eerste B2-familie (31 functies, 62 gevulde SVG’s) gebouwd met `b2_geometry.py` en `build_icon_set_b2.py`. Accent geometrisch uitgesneden onder hoofdkleur, ronde curven uitgewerkt met Shapely 2.2.0 in genegeerde runtimecache; afhankelijkheid gepind. Manifest met constructies/bronaanroepen/hashes, ZIP met 64 bestanden, interactieve review, CSV/JSON-werklijst voor alle 1.487 clusters en beoordelingen voor alle 2.854 bronrecords. 28 concrete bronvoorbeelden als onderbouwing gelezen; 15 betekenisconflicten apart gezet, geen automatische clustergelijke adoptie. `check_icon_set_b2.py` slaagt voor 62 exporten, drie foutcontroles, brondekking, hashes, ZIP en tien kleurcontrasten >=3:1; maximale numerieke kleuroverlap 0,00000181 vierkante viewBox-eenheid (tolerantie 0,00005). Alle 31 iconen visueel op 16/24/32 px bekeken; vijf thema’s, zoek-/groepfilter, 1.487-rijenwerklijst, 15 conflicten, bronuitklap, eigen paars en monochroom gecontroleerd. Screenshot opgeslagen. Geen wijzigingen aan Claude-thema’s of Rust; geen Cargo-controle nodig. Niets gecommit of gepusht.

- 2026-10-16 **Claude**: stap 2.4 gestart. `design/ontwerp-0.4/04-componenten.md` beschrijft 23 componenten met maten en toestanden. `scripts/build_componenten_review.py` maakt `componenten-review.html` uit `tokens-0.4.json`; 145 contrastparen halen hun minimum. Nieuwe regel: werkruimte-accent (`#92400E` op een lichte werkruimte in het donkere thema).
- 2026-10-16 **Codex**: B2-keuze vastgelegd. Tekenvolgorde van afgeronde voorstellen omgezet naar accent → hoofdkleur; generator controleert die volgorde voor alle 40 afgeronde SVG-varianten, alle 60 SVG’s parsen. Bij Openen sluit het accent nu aan op de echte afgeronde contour in plaats van de verwijderde scherpe hoek. Vijf voorbeelden in de browser bekeken op 16/24/32 px, licht/donker gecontroleerd en screenshot vernieuwd. Geen Rust- of Claude-themawijzigingen; geen Cargo-controle nodig. Niets gecommit of gepusht.

- 2026-10-16 **Codex**: aparte vergelijking voor vijf door gebruiker genoemde iconen: drie vormrichtingen × twee accentplaatsingen × twee maten = 60 SVG-ontwerpvarianten. Nieuwe accenten op mapopening, tekstregel, pijlpunt, zoeksteel en maatstreepjes. `build_icon_rounding_review.py` controleert XML bij generatie. Browser: alle vijf bekeken, 16/24/32 px, oude/nieuwe accenten, licht/donker, eigen accentkleur en monochroom; screenshot opgeslagen. Ronde lens verbeterd na rastercontrole: opeenvolgende segmenten van dezelfde kleur vormen één pad. Eerdere B-masters en Claude-thema’s behouden. Alleen concepten, geen Rust-wijzigingen of Cargo-controle; niets gecommit of gepusht.

- 2026-10-16 **Codex**: B herbouwd met `scripts/icon_geometry.py`: accentvlakken volgen dezelfde berekende contour als de basiskleur. 28 oorspronkelijke masters bewaard onder `review/before/`; nieuw `model-b.json`, `geometry-validation.json`, voor/na-review en screenshots. `check_icon_geometry.py` controleert alle 84 SVG-hashes, 28 geëxporteerde B-masters op begrenzing en kleuroverlap (maximaal 0), twee foutcontroles en ZIP met 87 bestanden; alles slaagt, evenals `git diff --check`. Alle 14 functies visueel bekeken op 16/24/32 px; eigen accentkleur, monochroom, contrastthema en ankerpunten gecontroleerd in de browser. README en keuze-status bijgewerkt. Claude-thema’s en Rust-code niet gewijzigd; geen Cargo-controle nodig. Niets gecommit of gepusht.
- 2026-10-16 **Claude**: stap 2.3 gestart. `design/ontwerp-0.4/03-tegels.md` beschrijft icoontegel, taaktegel, rij met recente bestanden, projectkaart, keuzetegel, infokaart en cijfertegel, met toestanden. `scripts/build_tegels_review.py` maakt `tegels-review.html` uit `tokens-0.4.json` en de canonieke iconen; 45 contrastparen halen hun minimum.
- 2026-10-16 **Claude**: `design/ontwerp-0.4/tokens-0.4.json` gemaakt met vijf thema's (licht, donker, blueprint, high-contrast-dark, high-contrast-light), lettertypen, afstanden, hoeken en schilmaten. `scripts/check_tokens_04.py` toetst 162 kleurparen; alle halen hun minimum. `scripts/build_fundament_review.py` toont de nieuwe thema's bovenaan `fundament-review.html`. Controle toegevoegd aan `AGENTS.md`.
- 2026-10-16 **Codex**: drie originele SVG-stijlrichtingen getekend op basis van de OpenAEC-website; 84 bestanden (3 × 14 functies × 2 optische masters), interactieve kleur-/thema-/monochroomproef, ware 16/24/32px-vergelijking en voorbeeldlint. ZIP, manifest en screenshots in `design/icon-style-proposals/`. Website-CSS alleen als genegeerde broncache vastgelegd. XML, 84 SHA-256-hashes, ZIP-inhoud/-integriteit en `git diff --check` slagen. Browsercontrole: stijlkeuze, aparte 16px-master, 32px-weergave, licht/donker, monochroom, eigen paars accent en contrastmodus zonder doorzichtige disabled-iconen werken. Productiethema’s, fundamentbestanden en Rust-crate niet gewijzigd; geen Cargo-controle nodig. Stijlkeuze staat open; niets gecommit of gepusht.

- 2026-10-16 **Codex**: centrale icooninventaris voor de 16 afgesproken apps gebouwd: zelfstandig HTML-overzicht per functie, app×functie-matrix, SVG/bibliotheek/bestands-/Rust-/manifestbronnen, licht/donker en 16/24/32 px, bronverwijzingen en JSON/CSV. 128 appoverstijgende functiekandidaten; 151 clusters met verschillende geometriebeschrijvingen; gelijke vormen met verschillende functiekandidaten apart filterbaar. Broncache is genegeerd. `check_function_icon_catalog.py` slaagt voor alle 2.854 records en 2.098 previewbestanden; `git diff --check` slaagt. Zoeken, appfilter, matrix, dekking, thema en 16px-weergave in browser getest; preview-PNG opgeslagen. Alleen inventaris/review toegevoegd; geen Rust-code gewijzigd, geen Cargo-tests nodig. Wijzigingen van Claude behouden, niets gecommit of gepusht.

- 2026-10-16 **Claude**: `design/ontwerp-0.4/overleg-voorbeelden.html` gemaakt met voorbeelden voor het overleg: vlakken van de website, Forge en OpenAEC (lichte of donkere werkruimte), mono-labels en drie varianten voor hoeken. Let op: Forge heeft een lichte werkruimte, OpenAEC een donkere.
- 2026-10-16 **Claude**: stijl van open-aec.com geanalyseerd in `design/ontwerp-0.4/bron-website.md` (kleuren, typografie, hoeken, schaduwen, componenten, contrast). Voorstellen in `01-fundament.md` bijgewerkt: Night Build `#2A2A32`, hoeken 4/8/12 px zoals de website, Forge volgt de donkere panelen van de site.
- 2026-10-16 **Claude**: fase 2 gestart. Werkplan in `design/ontwerp-0.4/README.md`, conceptspecificatie fundament in `01-fundament.md`, reviewpagina `fundament-review.html` gegenereerd door `scripts/build_fundament_review.py`. Style Book-tokens vastgezet in `harmonization/references/OpenAEC-style-book/packages/tokens/` op commit `dfdcd41`. Belangrijkste bevinding: amber als tekst en witte tekst op amberknoppen halen WCAG AA niet in Light en Forge.
- 2026-10-16 **Claude**: 2D-extensie uit de scope gehaald en FEM Studio op later gezet in `APP-OVERZICHT.md` en `STAPPENPLAN.md`.
- 2026-10-16 **Claude**: `APP-OVERZICHT.md` en `STAPPENPLAN.md` beperkt tot de 17 apps uit de harmonisatiepagina. Slint, Frappe en Dynlex vallen daardoor uit het plan.
- 2026-10-16 **Claude**: `APP-OVERZICHT.md` opgesteld met alle apps per techniek, inclusief de 19 uit `design/harmonized.html`, OconDat en BuildingPy.
- 2026-10-16 **Claude**: `STAPPENPLAN.md` herschreven rond harmonisatie per techniek, met een app-overzicht uit de broncatalogus. Let op: de catalogus telt `eslint` als Slint, dus 'React, Slint' betekent daar gewoon React.
- 2026-10-16 **Claude**: `STAPPENPLAN.md` opgesteld voor het nieuwe ontwerp (deel A) en bibliotheek 0.4 (deel B). Rust-build en `cargo test` slagen: 49 geslaagd, 45 bewust overgeslagen.
- 2026-10-16 **Claude**: Rust bleek al geïnstalleerd en is aan het gebruikerspad toegevoegd. `scripts/check_crate_package.py` werkt nu ook met Windows-paden. De vier Python-controles slagen.
- 2026-10-16 **Claude**: uitleg van de leidinggevende en de antwoorden van de gebruiker vastgelegd onder *Besluiten* en *Open punten*; eerste stappenplan in de chat opgesteld.
- 2026-10-16 **Claude**: repository gekloond en `AGENTS.md`, `CLAUDE.md` en `NOTES.md` toegevoegd met de samenwerkingsafspraken.
