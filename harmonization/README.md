# OpenAEC UI-inventarisatie

Een brongepind onderzoeksarchief met 63 publiek beschikbare repositories in de OpenAEC-Foundation-organisatie, vier eerder onderzochte maar niet publiek bereikbare OpenAEC-namen en OpenCADStudio als externe referentie. De [dekkingsmatrix](../design/coverage-matrix.html) splitst UI-code, UI-gebruikte assetbestanden, iconbronbestanden, bibliotheekiconen en schermkandidaten per publieke repository uit; drie publieke repositories zijn leeg (GitHub-commits-API 409). Bereikbare bronnen zijn op een commit vastgelegd. Geen code uit de bronrepositories is uitgevoerd. De [actuele toegangsaudit](../design/public-access-audit.html) vergelijkt de 63 huidige openbare organisatierepositories met deze historische records; de [JSON-data](public-access-audit.json) legt de API-uitkomst vast.

Dit is een breed archief van visuele bronbestanden, geen telling van gebruikte UI-iconen: alle SVG/ICO/ICNS/XPM-bestanden en rasterbestanden met icon/logo/favicon/pictogram/toolbar/ribbon in het pad. Het omvat ook technische symbolen, tekeningen en branding. Inline iconen zijn als bronbestanden bewaard; externe iconpackages zijn geregistreerd, niet volledig gespiegeld. Voor UI-gebruik zie `asset-index.json`, `ui-code-references.json` en `../design/review.html`. Privérepositories zijn niet toegankelijk; buiten de ene genoemde OpenCADStudio-referentie zijn externe repositories niet geïnventariseerd.

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
