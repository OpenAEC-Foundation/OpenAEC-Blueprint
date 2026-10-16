# Stappenplan: nieuw ontwerp en UI-bibliotheek 0.4

Dit plan beschrijft hoe we het nieuwe ontwerp voor alle OpenAEC-tools maken en daarna de UI-bibliotheek versie 0.4 bouwen. Het ombouwen van de tools zelf, te beginnen met Open Calc Studio, volgt na dit plan.

Status: **concept**, opgesteld op 2026-10-16. Besluiten en open vragen staan ook in [`NOTES.md`](NOTES.md).

## Uitgangspunten

- Alle tools worden omgebouwd naar de nieuwe UI.
- Bibliotheek 0.4 wordt vanaf nul gebouwd. De huidige crate `openaec-ui` 0.1.0 is een prototype: we gebruiken de kennis en de maten, niet de code als basis.
- De Style Repo blijft de plek waar het ontwerp wordt gemaakt, beoordeeld en vastgelegd.
- Er zijn vier soorten interfaces, en het ontwerp moet ze alle vier dekken:

| Soort | Voorbeelden | Kenmerk |
| --- | --- | --- |
| Ribbon-tool | Calc, Calculations, Planner, Pointcloud, CAD, PDF | Lint met tabs en groepen, documenttabs, panelen |
| Webachtige tool | Open Field Studio, Open Energy | Stapsgewijze werkstroom, geen lint |
| Communicatie-app | Y-Next, Z-Next | Webapplicatie, Y-Next draait op ERPNext |
| Installer | OpenAEC-installer | Korte wizard met voortgang |

## Deel A: het nieuwe ontwerp

### A1. Inventaris en prioriteit

- Zet alle tools in één lijst met hun interfacesoort, huidige techniek, eigenaar en volgorde van ombouwen.
- Kies per interfacesoort de kernschermen die het ontwerp moet laten zien, zoals hoofdscherm, Bestand-menu, instellingen, dialoog, lege staat, fout en voortgang.
- Bronnen: [`design/screen-inventory.html`](design/screen-inventory.html), [`design/harmonized.html`](design/harmonized.html) en [`design/assessment.md`](design/assessment.md).
- **Resultaat:** toollijst en lijst met kernschermen, vastgesteld met de leidinggevende.

### A2. Ontwerpprincipes en fundament

- Leg de principes vast: wat moet elke tool uitstralen, en waar mag een tool afwijken?
- Kleur: welke thema's blijven? Nu zijn dat Light, Forge, OpenAEC, Blueprint en High contrast. Leg de betekenis van kleuren vast, zoals amber voor selectie en focus.
- Typografie: lettertypen, groottes en regelhoogtes. Nu zijn dat Inter, Space Grotesk en JetBrains Mono.
- Maten: raster, afstanden, hoeken, randen en de vaste bandhoogtes van de schil.
- Toestanden: normaal, hover, ingedrukt, focus, uitgeschakeld en fout, voor alle bedieningselementen.
- Toegankelijkheid: minimaal contrast, toetsenbordbediening en zichtbare focus.
- Taal: Nederlands en Engels, en hoe teksten worden aangeleverd.
- **Resultaat:** één bronbestand met ontwerptokens. Daaruit worden zowel Rust-code als CSS gegenereerd, zodat ook de communicatie-apps en webtools dezelfde waarden gebruiken.

### A3. Iconen

- Stel de stijl vast: raster, lijndikte, hoeken, en een aparte 16 px-variant voor kleine maten.
- Maak de kernset van algemene bedieningsiconen definitief. Gebruik de bestaande reviews als bewijs.
- Daarna de domeinsets per vakgebied, zoals FEM, BIM, CAD en PDF.
- Leg per icoon één betekenis vast. De reviews laten zien dat dezelfde naam in verschillende tools iets anders kan betekenen.
- **Resultaat:** iconenset met naam, betekenis, 16 en 24 px, en goedkeuring per icoon.

### A4. Componenten

Ontwerp per component de opbouw, maten, toestanden en het gedrag.

- **Basis:** knop, icoonknop, invoerveld, keuzelijst, checkbox, schakelaar, slider, voortgangsbalk, tooltip en scrollbalk.
- **Samengesteld:** linttab, lintgroep, lintknop, documenttab, paneel met kop, eigenschappenraster, boomstructuur, tabel, zoekbalk, melding, dialoog en lege staat.
- **Schil:** titelbalk, lint, werkstroomnavigatie, documenttabs, panelen, werkruimte, statusbalk, Bestand-menu en instellingen.
- **Resultaat:** componentspecificatie met per component een reviewpagina in alle thema's.

### A5. Schermontwerpen per interfacesoort

- Maak de kernschermen uit A1 voor elk van de vier interfacesoorten.
- Toon ze in alle thema's, en op een breed en een smal venster.
- Werk één echte tool uit als voorbeeld, bij voorkeur Open Calc Studio, omdat die als eerste wordt omgebouwd.
- **Resultaat:** referentieschermen die als doel dienen voor de bibliotheek.

### A6. Vaststellen

- Bespreek het ontwerp met de leidinggevende en enkele gebruikers.
- Verwerk de feedback en bevries het ontwerp voor versie 0.4. Wijzigingen daarna gaan naar een volgende versie.
- **Resultaat:** goedgekeurde ontwerpversie 0.4.

## Deel B: bibliotheek 0.4

Stap B1 en B2 kunnen al starten tijdens deel A. Vanaf B3 is het fundament uit A2 nodig.

### B1. Architectuurbesluiten

Leg elk besluit kort vast met de reden.

- **Iced-versie.** Het prototype gebruikt Iced 0.13.1. Kies bewust een versie en een plan voor upgrades.
- **Renderer.** GPU met wgpu, software met tiny-skia, of allebei met terugval.
- **Indeling.** Eén crate of meerdere, bijvoorbeeld tokens, iconen, widgets en schil apart.
- **Gebruik door tools.** Een volledige app-schil, losse widgets, of een adapter voor tools met een eigen eventloop zoals Pointcloud.
- **Thema-API.** Hoe een tool een thema kiest en hoe tokens in code beschikbaar zijn.
- **Iconen-API.** Getypeerde iconen per betekenis in plaats van bestandsnamen.
- **Vertaling.** Hoe teksten in het Nederlands en Engels worden aangeleverd.
- **Licentie.** Het prototype gebruikt CC-BY-SA-4.0. Die licentie is niet bedoeld voor software. Kies een softwarelicentie die past bij de tools.
- **Publicatie.** De Style Repo is privé, en publieke tools kunnen niet bouwen op een private repository. Kies een openbare repository, crates.io, of een andere route.
- **Resultaat:** architectuurdocument.

### B2. Opzet en werkwijze

- Maak de nieuwe crate aan, in deze repo of in een eigen repository, afhankelijk van B1.
- Richt automatische controles in: opmaak, lint, tests en beeldvergelijking op Windows en Linux.
- Leg de versie- en releaseafspraken vast, met een changelog.
- **Resultaat:** lege maar werkende crate met controles.

### B3. Fundament

- Tokens, gegenereerd uit het bronbestand van A2.
- Thema's en lettertypen.
- Iconen uit A3.
- **Resultaat:** een voorbeeldscherm dat kleuren, tekst en iconen in elk thema correct toont.

### B4. Basiscomponenten

- Bouw de basiscomponenten uit A4, met alle toestanden.
- Schrijf per component een test die het beeld vergelijkt met het ontwerp.

### B5. Samengestelde componenten en schil

- Bouw de samengestelde componenten en de schil uit A4.
- Zorg dat de schil werkt als volledige app en als adapter voor tools met een eigen eventloop.

### B6. Layouts per interfacesoort

- Bouw de layouts voor ribbon-tool, werkstroomtool en installer.
- Maak per layout een klein voorbeeldprogramma.
- Lever voor communicatie-apps en webtools de tokens als CSS en de iconen als SVG. Zij gebruiken de Rust-bibliotheek niet.

### B7. Documentatie en showcase

- Documenteer elke publieke functie.
- Laat de Style Repo-app alle componenten uit de nieuwe bibliotheek tonen, zodat hij als levende catalogus dient.
- Schrijf een handleiding voor het ombouwen van een tool.

### B8. Release 0.4

- Controleer alle referentieschermen uit A5 tegen de bibliotheek.
- Publiceer versie 0.4 met changelog en handleiding.
- **Daarna:** proefproject Open Calc Studio. Wat daar ontbreekt, komt terug als versie 0.4.x.

## Samenwerking

- De leidinggevende en de gebruiker nemen de ontwerpbesluiten en keuren goed.
- ChatGPT en Claude kunnen inventarissen maken, reviewpagina's genereren, code schrijven en controles draaien. Ze werken volgens [`AGENTS.md`](AGENTS.md) en houden [`NOTES.md`](NOTES.md) bij.

## Open beslissingen

- Gaan Open Field Studio en Open Energy ook naar de Rust-UI, of krijgen ze een webvariant?
- Hoeveel van de stijl krijgen de communicatie-apps: alleen kleuren en iconen, of ook componenten in hun eigen webtechniek?
- Waarin worden de ontwerpen gemaakt: direct in de Style Repo, of eerst in een ontwerptool zoals Figma of Penpot?
- Welke thema's blijven in versie 0.4?
- Welke licentie krijgt de bibliotheek, en waar wordt hij gepubliceerd?
- Wie is eigenaar van het ontwerp, van de bibliotheek en van elke tool?
