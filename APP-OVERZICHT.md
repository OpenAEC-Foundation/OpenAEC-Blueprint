# Overzicht van de te harmoniseren apps

Status: bijgewerkt op 2026-10-16 voor het overleg over [`STAPPENPLAN.md`](STAPPENPLAN.md).

**Scope:** alleen de apps uit de harmonisatiepagina [`design/harmonized.html`](design/harmonized.html). Open CAD Studio, Open BIM Studio en de Open 2D Studio AEC-extensie staan daar ook op, maar vallen buiten de harmonisatie. Daarnaast hoort de OpenAEC Installer erbij. Dat geeft 17 apps.

Bronnen: de harmonisatiepagina, de broncatalogus in [`harmonization/repositories/`](harmonization/repositories/), de reviewpagina's in [`design/`](design/) en een controle op GitHub.

**Betekenis van de kolommen**

- **Interface.** Lint of werkstroom.
- **Style Repo.** Wat de Style Repo al voor de app heeft. "Lint uit bron" betekent dat het lint is overgenomen uit de echte app. "Lint voorgesteld" betekent dat het lint een ontwerpvoorstel is.
- **Licentie.** Zoals GitHub die herkent. "Onbekend" betekent dat GitHub geen licentie vond.

## Tauri + React

| App | Interface | Style Repo | Licentie |
| --- | --- | --- | --- |
| Open Calc Studio | Lint | Lint voorgesteld, review van linticonen en schermen | Onbekend |
| Open Calculations Studio | Lint | Lint voorgesteld, review van linticonen | Onbekend |
| Open Planner Studio | Lint | Lint voorgesteld, icoonreview en kruistabel | LGPL-3.0 |
| Open Geotechniek Studio | Lint | Lint voorgesteld, acht reviews | Onbekend |
| Open Heatloss Studio | Lint | Lint voorgesteld, zes reviews | Onbekend |
| Open Pile Plan Studio | Lint | Lint voorgesteld, vier reviews | LGPL-3.0 |
| Open Reports Studio | Lint | Lint voorgesteld, routereview | Onbekend |
| Open Energy Studio | Werkstroom | Werkstroomreview, icoonreview en kruistabel | LGPL-3.0 |
| Open Field Studio | Werkstroom | Bovennavigatie uit bron, routereview | Onbekend |

## Tauri + Solid

| App | Interface | Style Repo | Licentie |
| --- | --- | --- | --- |
| Open PDF Studio | Lint | Lint uit bron, 31 reviews. De Slint-versie v3 is als bron meegenomen | Niet herkend |
| Open Speech Studio | Werkstroom | Zijbalk uit bron, negen native schermen | Apache-2.0 |
| OpenAEC Workspace Composer | Werkstroom | Zijbalk uit bron, route- en icoonreview | MIT |

## Tauri + Svelte

| App | Interface | Style Repo | Licentie |
| --- | --- | --- | --- |
| Open Frame Studio | Lint | Lint uit bron, layout-, scherm- en icoonreview | CC-BY-SA-4.0 |

## Rust + Iced

| App | Interface | Style Repo | Licentie |
| --- | --- | --- | --- |
| Open Pointcloud Studio | Lint | Lint uit bron. Gebruikt het Rust-prototype al | Niet herkend |

## Webapp, React

| App | Interface | Style Repo | Licentie |
| --- | --- | --- | --- |
| Open BIM Validator Studio | Lint | Lint voorgesteld, routereview | Onbekend |

## Installer

Toegevoegd op 2026-10-16: de installer staat niet op de harmonisatiepagina, maar hoort wel bij de harmonisatie.

| App | Techniek | Interface | Style Repo | Licentie |
| --- | --- | --- | --- | --- |
| OpenAEC Installer | Tauri + React | Installer | Nog niets | CC-BY-SA-4.0 |

## Later

| App | Interface | Style Repo | Wat we weten |
| --- | --- | --- | --- |
| Open FEM Studio | Lint | Lint voorgesteld, FEM-iconen getekend | Repository gaf een 404. De gebruiker komt hier later op terug |

## Buiten de harmonisatie

| App | Reden |
| --- | --- |
| Open CAD Studio | Besluit: hieraan wordt niets veranderd |
| Open BIM Studio | Besluit: hoeft niet |
| Open 2D Studio AEC-extensie | Open 2D Studio is gestopt |

**Niet op de harmonisatiepagina, en daarom buiten de scope:** Y-Next/Z-Next, die de gebruiker apart doet, Open 3D Studio, OpenAEC Cloud Desktop, het BCF-platform, OpenAEC Docs, Zaagplan, Project OconDat, IfcGit voor Nextcloud, de Open-Monuments-apps, Dynlex en de BuildingPy-dialoog.

De installer en Y-Next/Z-Next stonden in de uitleg van de leidinggevende. De installer hoort erbij; de Y/Z-app doet de gebruiker apart.
