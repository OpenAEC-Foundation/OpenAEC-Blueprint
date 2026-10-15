# UI-fundament voor het OpenAEC-ecosysteem — ontwerp

- **Datum:** 2026-10-15
- **Status:** ontwerp, ter review
- **Repo:** `OpenAEC-Foundation/OpenAEC-style-book`

## 1. Doel

Alle OpenAEC-applicaties delen één huisstijl die vanuit één bron wordt beheerd.
Een wijziging in die bron — een nieuw icoon, een kleurcorrectie, een nieuwe
component — bereikt met één release alle applicaties, ongeacht het
UI-framework waarin ze gebouwd zijn.

Aanleiding: de applicaties draaien nu grotendeels op Tauri + React, met daarnaast
drie losse pogingen tot een volledig native Rust-UI (iced 0.14, iced 0.13 en egui
met een eigen UI-crate). Iconen en componenten worden tussen repo's gekopieerd.
Daardoor begint elke migratie opnieuw en loopt de huisstijl per app uit elkaar.

### Succescriteria

1. Een icoon toevoegen gebeurt op precies één plek (`design/icons/`) en is na één
   release in alle applicaties beschikbaar, zonder handwerk per app.
2. Geen enkele applicatie bevat nog eigen kopieën van huisstijl-iconen, tokens of
   schilcomponenten (ribbon, titelbalk, statusbalk, …).
3. iced- en React-implementaties van dezelfde component zijn visueel gelijk binnen
   een vastgelegde drempel, aantoonbaar via geautomatiseerde screenshots.
4. Het overzicht van alle ribbon-tabbladen van alle applicaties wordt automatisch
   uit de applicaties zelf opgebouwd.

## 2. Applicatiecategorieën

| # | Categorie | Applicaties | UI-techniek |
|---|---|---|---|
| 1 | Zware desktop-apps (GPU-viewport, grote datasets, realtime interactie) | OpenCADStudio, open-2d-studio, open-pointcloud-studio, open-3d-viewer, Open-FEM2D-Studio, open-pdf-studio, OpenAEC-BIM-validator | **iced** (native Rust) |
| 2 | Lichte desktop-apps (formulieren, rekenen, rapporteren) | o.a. open-calc-studio, open-heatloss-studio / warmteverliesberekening, Open-U-value-Studio, Open-Safety-Studio, open-mpg-studio, openaec-reports, open-speech-studio, open-orchestrator-studio, openaec-cloud-desktop | **Tauri + React** |
| 3 | Web-applicaties, in de basis Frappe-apps | Open Field Studio, Open Energy Studio | **Frappe**: standaard Desk-schermen met huisstijlthema; eigen schermen in **React** |
| 4 | Bedrijfsfrontends op ERPNext | Y-Next, Z-Next | **React + Tailwind** SPA (web, desktop, Android) |

Buiten scope: Open-Frame-Studio (blijft zoals het is) en
open-structural-engineer-studio (vervalt).

Gevolg: er zijn **twee componentbibliotheken** — één voor iced, één voor React.
Categorie 2, 3 en 4 delen de React-bibliotheek. Frappe Desk krijgt alleen een
CSS-thema, geen eigen componenten.

## 3. Structuur van de repo

```
OpenAEC-style-book/
├── brandbook/              merkregels, logo's, illustraties, styleguide (blijft)
├── design/                 ENIGE BRON — alleen hier wordt met de hand bewerkt
│   ├── tokens/             kleuren, typografie, spacing, radius, schaduw (uit packages/tokens/tokens)
│   ├── icons/<domein>/     SVG-iconen per domein: ui, file, view, cad, ifc, pdf, fem, report, …
│   │   └── icons.toml      per icoon: id, NL/EN-label, tags
│   ├── i18n/<taal>/        gedeelde termen (Bestand, Opslaan, Ongedaan maken, …), nl en en
│   ├── components/         één specificatie per component (zie §6)
│   ├── ribbons/            gedeelde ribbon-tabs (viewer3d, ifc, report, …)
│   └── apps.toml           register van alle app-repo's met categorie en gebruikte onderdelen
├── generators/             scripts die design/ omzetten naar onderstaande uitvoer
├── packages/               npm (React): tokens, icons, ribbon, shell, ui-primitives
├── crates/                 Rust (iced): openaec-tokens, openaec-icons, openaec-i18n, openaec-ui
├── frappe/openaec_theme/   Frappe-app: Desk-thema (CSS uit tokens), fonts, logo, favicon
└── project-templates/
    ├── Tauri+React/        gebruikt packages/ (geen eigen kopieën meer)
    └── iced/               nieuw startpunt voor zware apps, gebruikt crates/
```

### Regels

1. **Gegenereerde uitvoer wordt nooit met de hand bewerkt.** CI draait alle
   generators en faalt als dat een verschil oplevert.
2. **Iconen bestaan alleen in `design/icons/`.** Bestaande sets (OpenCADStudio
   ±255, Tauri+React-template 42, `packages/ribbon`, kopieën in
   open-pointcloud-studio) worden eenmalig verzameld, ontdubbeld en genormaliseerd
   (24×24 viewBox, `currentColor`; meerkleurige iconen alleen met tag `color`).
   Daarna verdwijnen ze uit de app-repo's.
3. **Ribbons van applicaties staan in de app-repo** (`ribbon.toml`), niet in het
   stijlbook. Alleen tabs die meerdere apps delen staan in `design/ribbons/`.

### Wie gebruikt wat

| Categorie | Gebruikt |
|---|---|
| 1. iced | `crates/` |
| 2. Tauri + React | `packages/` |
| 3. Frappe-apps | `frappe/openaec_theme` + `packages/` voor eigen schermen |
| 4. Y-Next / Z-Next | `packages/` (Tailwind-preset, iconen, gewenste componenten) |

## 4. Versies en uitrol

### Eén versienummer

Eén git-tag (`vX.Y.Z`) geldt tegelijk voor tokens, iconen, npm-packages,
Rust-crates en het Frappe-thema.

| Wijziging | Versie |
|---|---|
| Nieuw icoon, kleurcorrectie, bugfix | patch |
| Nieuwe component of optie, niets breekt | minor |
| Iets verdwijnt of wordt hernoemd | major |

Icoon-id's en tokennamen worden nooit stil hernoemd: de oude naam blijft één
major-versie bestaan als alias, met een waarschuwing tijdens de build.

### Distributie per categorie

| Categorie | Kanaal | Voorbeeld |
|---|---|---|
| 1. iced | Cargo git-dependency op tag | `openaec-ui = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.5.0" }` |
| 2 en 4. React | openbare npm-registry, scope `@openaec` | `"@openaec/ribbon": "0.5.0"` |
| 3. Frappe | release-workflow zet `frappe/openaec_theme` met dezelfde tag in een eigen repo `openaec_theme` (bench verwacht de app in de root van een repo) | containerrecept pint `openaec_theme@v0.5.0` |

iced-apps gebruiken iced uitsluitend via de re-export `openaec_ui::iced`, zodat een
iced-upgrade op één plek gebeurt.

### Uitrol

1. Wijziging in `design/` via een PR. CI toont een preview (nieuwe iconen in alle
   maten, licht en donker, in iced en React).
2. Na merge en tag draait de **release-workflow**: generators, tests, publicatie
   van npm-packages, Frappe-thema naar eigen repo, GitHub Release met changelog.
3. De **uitrol-workflow** leest `design/apps.toml` en opent per app-repo één PR die
   de versie ophoogt (npm en Cargo samen).
   - patch: automatisch mergen zodra de CI van de app groen is;
   - minor en major: PR blijft open voor review.
4. Desktop-apps nemen de wijziging mee in hun volgende release, web-apps bij hun
   volgende deploy.

Bewust een eigen workflow in plaats van een generieke dependency-bot: de lijst
apps is bekend, er is één PR per app voor npm én Cargo nodig, en Cargo
git-tags worden door generieke bots niet altijd goed ondersteund.

### Lokaal ontwikkelen

Bij gelijktijdig werken aan stijlbook en app: Cargo `[patch]` respectievelijk npm
`overrides`/`link` naar de lokale map. Dit wordt beschreven in de
integratiehandleiding.

### Omvang

iced-apps bakken de iconen in de binary (±300 SVG's, ruwweg 300 KB). Is dat te
veel, dan komen er Cargo-features per domein (`cad`, `pdf`, `ifc`, …). React
verwijdert ongebruikte iconen via tree-shaking.

## 5. Ribbon-definitie (`ribbon.toml`)

Elke applicatie met een ribbon beschrijft die in `ribbon.toml` in de root van haar
repo.

```toml
app = "open-cad-studio"
format = 1
include = ["openaec:viewer3d"]          # gedeelde tab uit design/ribbons/

[quick_access]                          # knoppen in de titelbalk
items = ["file.save", "edit.undo", "edit.redo"]

[[tab]]
id = "home"
label = "ribbon.tab.home"               # i18n-sleutel; openaec.* = gedeelde term

  [[tab.group]]
  id = "draw"
  label = "ribbon.group.draw"
  items = [
    { type = "large",          command = "draw.line", icon = "cad/line", label = "cmd.line", shortcut = "L" },
    { type = "large-dropdown", icon = "cad/arc",  label = "cmd.arc", items = [
        { command = "draw.arc.3p",  icon = "cad/arc-3p",  label = "cmd.arc.3p" },
        { command = "draw.arc.sce", icon = "cad/arc-sce", label = "cmd.arc.sce" } ] },
    { type = "small",  command = "draw.hatch", icon = "cad/hatch", label = "cmd.hatch" },
    { type = "toggle", command = "view.ortho", icon = "cad/ortho", label = "cmd.ortho" },
  ]

  [[tab.group]]
  id = "layers"
  label = "ribbon.group.layers"
  items = [ { type = "custom", slot = "layer-combo" } ]

[[tab]]
id = "wall-edit"
label = "ribbon.tab.wall"
contextual = "selection:wall"           # alleen zichtbaar bij deze selectie
```

### Itemtypen

| Type | Gedrag |
|---|---|
| `large` | groot icoon met label |
| `small` | klein icoon met label; worden automatisch per drie gestapeld |
| `toggle` | aan/uit; toestand komt van de app |
| `dropdown` / `large-dropdown` | knop die een menu opent |
| `split` | klik = standaardactie, pijl = menu |
| `combo` | keuzelijst; waarden komen van de app |
| `custom` | slot waarin de app een eigen widget plaatst |

### Vast in elke applicatie (niet in `ribbon.toml`)

Bestand-tab (backstage) als eerste tab, Help-menu, vensterknoppen.

### Koppeling met code

- **iced:** `build.rs` leest `ribbon.toml` en genereert `enum Command`. Een
  ontbrekende handler is een compileerfout.
- **React:** de generator levert een TypeScript-type `CommandId`.
  Gebruik: `<Ribbon def={ribbon} onCommand={…} state={…} />`.
- **Toestand** (checked, enabled, visible) levert de app per command-id aan; de
  ribbon houdt zelf geen toestand bij.

### Validatie

De generator faalt bij: onbekend icoon-id, ontbrekende i18n-sleutel in nl of en,
dubbele id's, onbekend itemtype, onbekende `include`.

### Overzicht van alle tabbladen

Het stijlbook haalt via `design/apps.toml` de `ribbon.toml` van elke app op en
genereert een overzichtspagina in de styleguide: alle apps, tabs, groepen en
knoppen, met iconen.

## 6. Componentspecificaties

`design/components/<component>.md` beschrijft per component: opbouw, maten en
kleuren als tokens, toestanden (normaal, hover, actief, uitgeschakeld, focus),
toetsenbordgedrag en labels. De iced- en React-implementatie volgen beide exact
deze specificatie. De bestaande `COMPONENT-MANIFEST.md` van de Tauri+React-template
is het vertrekpunt.

### Versie 1

| Groep | Componenten |
|---|---|
| Schil | TitleBar (met quick access), Ribbon, Backstage, DocumentTabs, StatusBar, dockbare zijpanelen, Startscherm |
| Basis | Button, IconButton, Input, Select/Combo, Checkbox/Toggle, Dialog, Tooltip, Contextmenu, Toast |
| Data | Table/DataGrid, Tree, PropertyGrid |
| Viewer | NavigationCube met Home-knop |

Frappe Desk krijgt geen componenten, alleen een CSS-thema uit de tokens. Y-Next en
Z-Next gebruiken de React-componenten die ze nodig hebben; zij gebruiken geen
ribbon als ze een webnavigatie hebben.

## 7. Migratievolgorde

Per repo werkt steeds één ontwikkelspoor tegelijk; fasen in verschillende repo's
mogen parallel lopen.

| Fase | Inhoud | Opmerking |
|---|---|---|
| 0. Fundament | `design/` opzetten, tokens verhuizen, iconen verzamelen en ontdubbelen, generators (Rust, React, Frappe), validator `ribbon.toml`, npm-scope regelen, release `v0.1.0` | alleen het stijlbook |
| 1a. `openaec-ui` (iced) | ribbon, titelbalk en overige schil uit OpenCADStudio overzetten naar de crate; OpenCADStudio wordt de eerste gebruiker | bewijst de crate op bestaande, werkende code |
| 1b. React | Tauri+React-template overzetten op `packages/` en `ribbon.toml` | voorbeeld voor alle lichte apps |
| 2. Proefmigraties iced | ① open-pointcloud-studio (iced 0.13 → 0.14, op de crates) ② open-3d-viewer (Tauri → iced, inclusief NavigationCube) | levert het migratiedraaiboek op |
| 3. Overige zware apps | Open-FEM2D-Studio → OpenAEC-BIM-validator → open-2d-studio (egui → iced) → open-pdf-studio (na korte proef met een PDF-render-engine) | grootste risico's als laatste |
| 4. Lichte apps | eigen componenten vervangen door `packages/`, `ribbon.toml` toevoegen | parallel mogelijk vanaf 1b, één app per spoor |
| 5. Web | `openaec_theme` voor Open Field Studio en Open Energy Studio; Tailwind-preset en iconen voor Y-Next en Z-Next | afstemmen met het SaaS-platformontwerp |

### Migratiedraaiboek (iced)

1. Bestaande ribbon omzetten naar `ribbon.toml`.
2. Tauri-commands verplaatsen naar een core-crate van de app (gewone functies).
3. Schermen omzetten naar iced-views met uitsluitend `openaec-ui`-componenten —
   volledige adoptie, geen eigen kopieën.
4. Functionaliteitschecklist oud ↔ nieuw afwerken.
5. Screenshotvergelijking oud ↔ nieuw.
6. Bèta-release naast de bestaande versie; oude versie daarna uitfaseren.

## 8. Testen

### Stijlbook-CI

- Generators leveren geen diff op.
- Schemavalidatie van `icons.toml`, `apps.toml`, `design/ribbons/*.toml`.
- Unit-tests voor de generators.
- Elk icoon wordt naar PNG gerenderd (licht en donker) en vergeleken met een
  snapshot.

### Componenten

- Showcase-app voor iced en voor React met alle componenten in alle toestanden.
- Automatische screenshots: React via Playwright; iced via headless rendering met
  de testvoorzieningen van iced 0.14.
- Styleguide toont iced en React naast elkaar met pixelvergelijking; CI faalt
  boven de afgesproken drempel.

### App-CI

Bouwen tegen de gepinde tag, `ribbon.toml` valideren, opstart-rooktest.

### Uitrol

Eenmalige proefrelease die alleen een testapp ophoogt, om de keten
"één keer toevoegen, overal zichtbaar" end-to-end te bewijzen.

## 9. Buiten scope

- Open-Frame-Studio en open-structural-engineer-studio.
- Infrastructuur van het SaaS-platform.
- Nieuwe functionaliteit in applicaties (migraties zijn functioneel gelijkwaardig).

## 10. Open punten

1. Beschikbaarheid van de npm-scope `@openaec` (of alternatieve scope).
2. Of de testvoorzieningen van iced 0.14 headless screenshots ondersteunen;
   anders een alternatieve renderroute voor de iced-showcase.
3. Keuze van de PDF-render-engine voor open-pdf-studio (korte proef in fase 3).
4. Locatie en huidige stack van de Z-Next-repo bevestigen.
5. Werkaanname bevestigen: eigen schermen in de Frappe-apps (categorie 3) worden
   in React gebouwd.
6. Drempelwaarde voor de visuele vergelijking iced ↔ React.
