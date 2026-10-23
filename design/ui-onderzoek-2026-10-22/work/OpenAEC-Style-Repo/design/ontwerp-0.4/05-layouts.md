# 2.5 Layouts

Status: **besloten**, 2026-10-16. Bekijk de [reviewpagina](layouts-review.html) voor alle schermen. Bovenaan kies je een van de vijf thema's.

De layouts gebruiken alleen wat al besloten is: de tokens uit [`tokens-0.4.json`](tokens-0.4.json), de tegels uit [`03-tegels.md`](03-tegels.md) en de componenten uit [`04-componenten.md`](04-componenten.md). Er komen geen nieuwe kleuren of maten bij.

## Twee soorten apps

| Soort | Apps | Kenmerk |
| --- | --- | --- |
| Lint-app | Calc, Calculations, Planner, Geotechniek, Heatloss, Pile Plan, Reports, PDF, Frame, Pointcloud, BIM Validator, FEM | Lint, documenttabs, verkenner, werkruimte en eigenschappen |
| Werkstroom-app | Energy, Speech, Workspace Composer, Field | Geen lint. Navigatie door secties of stappen |

## Lint-app

Van boven naar beneden:

| Band | Hoogte | Inhoud |
| --- | --- | --- |
| Titelbalk | 32 px | Logo en snelle acties (opslaan, ongedaan, opnieuw) links, appnaam in het midden, vensterknoppen rechts |
| Linttabs | 28 px | Bestand als afgeronde knop, daarna de tabs |
| Lint | 94 px | Groepen met grote en kleine lintknoppen |
| Documenttabs | 30 px | Open documenten, met een stip bij wijzigingen |
| Werkgebied | rest | Verkenner 240 px links, werkruimte in het midden, eigenschappen 240 px rechts |
| Statusbalk | 22 px | Status links, voortgang in het midden, kerngetallen rechts. Volgt het thema, met een lijn erboven |

De panelen links en rechts kun je verbergen via de groep Panelen in het lint. De werkruimte groeit dan mee.

### Kernschermen

1. **Werkruimte.** Het normale werkscherm met een geopend document.
2. **Startscherm.** Verschijnt bij het openen van de app. Geen lint en geen panelen. Opent iemand de app via een bestand, bijvoorbeeld door erop te dubbelklikken, dan opent dat bestand direct, zonder startscherm.
   - Links staat Nieuw, met taaktegels.
   - Rechts staan de recente projecten als projectkaarten en de recente bestanden als lijst.
3. **Bestand-menu.** Vervangt lint, documenttabs en panelen.
   - Links staat de navigatie van 260 px.
   - Rechts staan de taken en de recente bestanden.
4. **Lege staat.** Geen document open.
   - Lintknoppen die een document nodig hebben, zijn uitgeschakeld.
   - De panelen tonen "Geen project geopend" en "Geen selectie".
   - De werkruimte volgt het thema.
5. **Voortgang, fout en melding.**
   - Een lange taak toont zijn voortgang in de statusbalk.
   - Een fout staat als melding bovenaan het document.
   - Een afgeronde taak geeft een melding rechtsonder.
6. **Onopgeslagen wijzigingen.** Een dialoog van 420 px boven de gedimde app.

## Werkstroom-app

| Band | Hoogte | Inhoud |
| --- | --- | --- |
| Titelbalk | 32 px | Zoals bij de lint-app |
| Navigatie | zie hieronder | Zijbalk of stappen |
| Inhoud | rest | Een kop van 22 px, daaronder kaarten met formulieren of lijsten |
| Actiebalk | 52 px | Onderaan de inhoud: Vorige en Volgende rechts, de primaire knop helemaal rechts |
| Statusbalk | 22 px | Zoals bij de lint-app |

**Twee vormen van navigatie**

Beide vormen kunnen in elke werkstroom-app. Gebruikers kiezen in de instellingen bij Navigatie. Standaard is de zijbalk.

- **Zijbalk**, standaard, van 220 px met secties. Past het best bij apps waarin je de onderdelen in elke volgorde kunt bewerken, zoals Energy, Speech en Composer. Regels van 36 px, de actieve sectie krijgt de tint en een streep.
- **Stappen bovenaan** in een balk van 44 px. Past het best bij apps met een vaste volgorde, zoals Field. Genummerde stappen in mono. Een afgeronde stap krijgt een getinte cirkel, de actieve stap een amberkleurige cirkel en een streep eronder.

## High contrast

- Selectie in de boom, de navigatie en de tabel krijgt een omlijning van 2 px in plaats van een tint.
- Verder gelden de regels uit de componenten.

## Besluiten

Genomen door de gebruiker op 2026-10-16.

| Nr. | Besluit |
| --- | --- |
| 1 | Het startscherm verschijnt bij het openen van de app. Met de instelling "Laatste project direct openen" sla je het over. Start de app vanuit een bestand, dan opent dat bestand direct |
| 2 | Werkstroom-apps kunnen een zijbalk of stappen bovenaan tonen. Gebruikers kiezen in de instellingen bij Navigatie. Standaard is de zijbalk |
| 3 | De statusbalk volgt het thema, in Licht dus licht met een lijn erboven. Met de instelling Statusbalk kan hij altijd donker. De waarden staan onder `statusbar-setting` in het tokenbestand |
