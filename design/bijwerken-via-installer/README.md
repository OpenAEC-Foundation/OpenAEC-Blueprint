# Bijwerken via de OpenAEC Installer

Voorstel bij issue [#33](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/33). Status: **concept, wacht op besluit van de gebruiker en het team.** Er is nog niets aan de installer of de apps veranderd.

Bronnen, bekeken op 2026-10-26:

| Bron | Commit | Wat |
| --- | --- | --- |
| [openaec-installer](https://github.com/OpenAEC-Foundation/openaec-installer) | `8b39bae` | `src-tauri/src/github.rs`, `installer.rs`, `registry.rs`, `linux.rs`, `src/App.tsx`, `src/data/catalog.ts` |
| [JM-Orgue](https://github.com/orgelmaker/JM-Orgue) | `7076f85` | `.github/workflows/release-build.yml`, `.github/scripts/build-latest-json.sh`, `VirtualPipeOrgan/BUILDING.md`, `src-tauri/tauri.conf.json`, `ui/src/lib/updater.js`, `commands.rs` (`prepare_for_update`) |
| Style Repo | werkkopie | `crates/openaec-ui/src/design/update.rs` (in bewerking door een andere sessie) |
| Tauri | `main` | `plugins/updater/src/updater.rs`, `tauri-bundler/.../nsis/installer.nsi`, `msi/main.wxs` |
| Releases | API, 2026-10-26 | laatste release van alle 17 desktop-apps uit de catalogus |

JM-Orgue is alleen als voorbeeld van de werkwijze gebruikt. Er is geen code uit overgenomen; de repository staat op "alle rechten voorbehouden". Besluit 4 van #33 zei dat JM-Orgue niet als voorbeeld dient; de gebruiker vroeg er op 2026-10-26 juist wel om.

## Oordeel in het kort

Het idee van #33 klopt: één plek die bijwerkt. Alleen werkt de installer nu als een downloadknop die een setup opent. Hij weet niet zeker welke versie er is, controleert niet wat hij downloadt, sluit de app niet, start hem niet opnieuw en kiest soms het verkeerde soort setup. JM-Orgue laat zien hoe het wel kan: de **release levert een ondertekende `latest.json`**, de bouwstraat weigert een release met een foute handtekening, en de update draait **stil** en start de app daarna zelf weer.

Voorstel: de installer gebruikt per app dezelfde `latest.json` en dezelfde handtekening als de Tauri-updater, maar voert de update zelf uit. De apps houden geen eigen updater; ze melden alleen en geven het stokje door.

## Wat er nu misgaat in de installer

1. **Versie geraden uit een bestandsnaam.** `github.rs:56` vraagt de GitHub-API om de laatste release en `extract_version` (`github.rs:199`) haalt de versie uit de naam van het setupbestand. Bij Monty IFC Viewer is de tag `v1.0.1` en het bestand `1.0.0`; dat werkt alleen dankzij die omweg.
2. **API-limiet.** Ongeauthenticeerd mag de API 60 keer per uur. Met 17 apps is dat na drie verversingen op. Daarom bestaat er een cache van zes uur (`App.tsx:46`), waardoor een nieuwe release pas uren later te zien is.
3. **Geen controle van de download.** De enige eis is dat het adres met `https://github.com/` begint (`installer.rs:41`). Een handtekening of hash wordt niet gecontroleerd.
4. **Verkeerde soort setup.** `score_windows_asset` (`github.rs:166`) kiest altijd eerst de per-gebruiker-setup, dan de gewone NSIS-setup, dan de MSI. Hoe de app nu geïnstalleerd is, telt niet mee: `registry.rs` ziet wel of de app in HKCU (NSIS) of HKLM (MSI) staat, maar geeft dat niet door. Wie met de MSI installeerde, krijgt een NSIS-setup en houdt twee installaties naast elkaar. JM-Orgue documenteert precies dit probleem en zet daarom een aparte `windows-x86_64-msi`- en `windows-x86_64-nsis`-sleutel in `latest.json`.
5. **De gebruiker doorloopt de hele setup.** `run_installer` (`installer.rs:112`) opent de setup gewoon, met taalkeuze, map, vinkjes en soms UAC. Een update is daardoor een herinstallatie.
6. **De app blijft open.** Niets sluit de app vóór de setup. De NSIS-setup vraagt dan om het programma te sluiten; niet-opgeslagen werk loopt risico.
7. **Geen herstart en geen bevestiging.** Na het starten van de setup meldt de installer "installer gestart" en weet hij niet of het gelukt is; de app start niet vanzelf opnieuw.
8. **Zelf bijwerken op Windows** werkt net zo: de installer opent zijn eigen setup terwijl hij nog draait.
9. **Apps kunnen de installer niet aansturen.** Er is geen opdrachtregel (`--update <app>`), geen single-instance en er wordt geen statusbestand geschreven. Het contract uit `design::update` (statusbestand `updates.json`, `<installer> --update <app id>`) heeft aan de installerkant nog geen tegenhanger.

## Wat de apps nu doen

Laatste release per app (2026-10-26):

| App | Tag | `latest.json` | Handtekeningen | Setupbestanden |
| --- | --- | --- | --- | --- |
| Open PDF Studio | v2026.43.4 | ja | NSIS | NSIS, user-setup |
| Open Planner Studio | v2026.43.0 | ja | NSIS (`.nsis.zip`) | NSIS |
| Open 2D Studio | v0.35.0 | ja | NSIS, MSI | NSIS, MSI (repo is privé) |
| Open Calc Studio | v0.13.0 | nee | nee | NSIS, MSI |
| Open Frame Studio | v0.6.0 | nee | nee | NSIS, MSI, user-setup |
| Open Field Studio | v0.3.6 | nee | nee | NSIS, MSI, user-setup |
| Open Calculations Studio | v2026.39.0 | nee | nee | NSIS, user-setup |
| Open FEM2D Studio | v2026.42.0 | nee | nee | NSIS, MSI |
| Open Speech Studio | v0.12.2 | nee | nee | NSIS, MSI |
| Monty IFC Viewer | v1.0.1 | nee | nee | NSIS, MSI (bestand 1.0.0) |
| Open 3D Studio | v0.8.0 | nee | nee | NSIS |
| Open Geotechniek Studio | v0.4.1 | nee | nee | NSIS |
| Open Pointcloud Studio | v2026.44.0 | nee | nee | NSIS |
| Open CAD Studio (extern) | v2026.43 | nee | nee | alleen MSI |
| Open STL-3DMap Studio | v1.1.1 | nee | nee | geen Windows-setup |
| BIM-validator, Paalplan | — | — | — | geen release |

PDF, Planner, 2D en Cloud Desktop hebben daarnaast een eigen `tauri-plugin-updater` met een eigen sleutel. Volgens #33 verdwijnt dat. In PDF wijst het updateadres nog naar de oude reponaam `OpenPDFStudio`.

## Voorstel

### De keten

```
release van een app (CI)
  setup.exe + .sig, setup.msi + .sig, AppImage + .sig
  latest.json als laatste, pas na controle van elke handtekening
        |
        v
OpenAEC Installer
  haalt per app releases/latest/download/latest.json (geen API, geen limiet)
  schrijft updates.json  ---------------------------->  app leest updates.json bij start
                                                         toont "Versie x staat klaar  [Bijwerken]"
                                                         sluitplan: alles opgeslagen of bewust niet
  <----------------  start  installer --update <app> <pid>  en sluit af
  wacht tot proces <pid> weg is
  downloadt, controleert de handtekening met de sleutel uit de catalogus
  installeert stil, in dezelfde soort als de bestaande installatie
  start de app opnieuw, schrijft updates.json bij
```

### 1. Wat een release van elke app moet leveren

Hetzelfde voor elke app, in één gedeeld script (zie *Waar het script komt*):

- `bundle.createUpdaterArtifacts: true` (niet `"v1Compatible"`), zodat er naast elke setup een `.sig` komt en de update gewoon de `.exe` of `.msi` is, geen `.nsis.zip`.
- Ondertekenen met een minisign-sleutelpaar per app. De privésleutel staat als secret `TAURI_SIGNING_PRIVATE_KEY(_PASSWORD)` in de repo; de publieke sleutel gaat naar de catalogus van de installer. Een app hoeft de sleutel niet meer in zijn eigen `tauri.conf.json` te hebben.
- `latest.json` met per platform een sleutel: `windows-x86_64-nsis`, `windows-x86_64-msi`, `windows-x86_64` (terugval naar NSIS), `linux-x86_64` (AppImage) en, zodra macOS meedoet, `darwin-aarch64` en `darwin-x86_64` (een `darwin-universal` kent Tauri niet).
- Fail-closed, zoals JM-Orgue: het script controleert elke `.sig` met `minisign -V` tegen de publieke sleutel, weigert een concept of pre-release en hangt `latest.json` er pas als **laatste** aan. Zonder `latest.json` ziet niemand de update, dus kan er nooit een update verschijnen waarvan de setup nog ontbreekt.
- Een poort die de tag vergelijkt met de versie in `tauri.conf.json`. Anders blijft een update zich eindeloos aanbieden (het Monty-geval). Dit past bij de afspraak jaar.week (`2026.43.x`, #1).
- Een kopie met vaste naam (`Open-Calc-Studio-setup.exe`) voor de website, zodat `releases/latest/download/<naam>` blijft werken.
- Geen privérepo's voor apps in de catalogus: de installer kan Open 2D Studio nu niet ophalen.

### 2. Wat er in de installer verandert

| Onderdeel | Nu | Wordt |
| --- | --- | --- |
| Catalogus `catalog.ts` | `repo`, `registryName`, `exeName` | plus `pubkey` en eventueel een eigen `updateUrl` |
| Laatste versie | GitHub-API, versie uit bestandsnaam | `latest.json` via `releases/latest/download/`; versie uit het bestand. Terugval op de API alleen voor apps zonder `latest.json` (overgangstijd) |
| Installatiesoort | niet bekend | `registry.rs` geeft `scope: user/machine` en `kind: nsis/msi` terug; de installer kiest `windows-x86_64-nsis` of `-msi` |
| Controle | alleen `https://github.com/` | handtekening controleren met de crate `minisign-verify` (wat de Tauri-updater ook doet); bij een fout niets installeren |
| Uitvoeren NSIS | setup openen | `setup.exe /S /UPDATE /R`, dezelfde vlaggen als de Tauri-updater: stil, in updatemodus (geen WebView2-installatie, app-gegevens en autostart blijven staan) en daarna de app starten (`.onInstSuccess` in het Tauri-sjabloon) |
| Uitvoeren MSI | `msiexec /i` | `msiexec /i <msi> /passive /promptrestart AUTOLAUNCHAPP=True`, ook zoals de Tauri-updater; vraagt UAC, net als nu |
| Linux | AppImage vervangen | blijft, met handtekeningcontrole |
| App open? | niet gecontroleerd | wachten tot het proces van de app weg is; anders vragen om de app te sluiten |
| Opdrachtregel | geen | `--update <app id> [pid]` en `--check` (zonder venster: alleen `updates.json` verversen), met `tauri-plugin-single-instance` zodat een al geopende installer de opdracht overneemt |
| Statusbestand | geen | na elke controle `updates.json` schrijven volgens `design::update::StatusFile` |
| Zelf bijwerken | eigen setup openen | de installer is de enige met `tauri-plugin-updater` en een eigen `latest.json`, precies volgens de JM-Orgue-route; `installMode: "quiet"`, zelf herstarten |
| Melding na afloop | "installer gestart" | "Bijgewerkt naar 2026.44.1", met link naar de release op GitHub |

### 3. Wat er in de apps en de bibliotheek verandert

- `tauri-plugin-updater` en de eigen updatebanner gaan uit PDF, Planner, 2D en Cloud Desktop. De CI-stappen voor ondertekening en `latest.json` blijven, want die gebruikt de installer nu.
- Elke app gebruikt `design::update` uit `openaec-ui` (native) of de webtegenhanger: `updates.json` lezen, melding in de titelbalk, sluitplan en daarna `open_installer`.
- Aanvulling op het contract in `design::update`:
  - de app geeft zijn eigen proces-id mee (`--update <app> <pid>`), zodat de installer weet waarop hij moet wachten;
  - is `updates.json` ouder dan een dag, dan start de app `installer --check` op de achtergrond. De app gaat zo zelf niet online en het bestand blijft vers, ook als niemand de installer opent;
  - een app-eigen opruimstap vóór het afsluiten, zoals JM-Orgue `prepare_for_update` heeft (audio, MIDI of een lopende berekening netjes stoppen), hoort in het sluitplan.

Deze punten raken bestanden die een andere sessie nu bewerkt; ze staan hier alleen als voorstel.

### Waar het script komt

Voorstel: in de installer-repo, als `release-kit/` met het script voor `latest.json` en een voorbeeldworkflow die elke app kopieert. De installer is de enige afnemer van `latest.json`, dus het formaat hoort daar. Een herbruikbare workflow (`uses: OpenAEC-Foundation/openaec-installer/...`) kan ook, maar JM-Orgue noemt een nadeel: "Re-run failed jobs" slaat de laatste taak dan vaker over. Daarom ook een handmatige noodknop die `latest.json` voor een bestaande tag opnieuw maakt.

## Volgorde

1. **Installer leest `latest.json` en controleert de handtekening**, met terugval op de huidige API-route. *Gebouwd op 2026-10-26 in `openaec-installer`, branch `latest-json-updates`, commit `9bf0d36`.* Alleen Planner heeft een sleutel: de `latest.json` van PDF ondertekent alleen de systeembrede setup, terwijl de installer PDF's per-gebruiker-setup kiest. PDF volgt bij stap 2, of zodra PDF zijn per-gebruiker-setup ook ondertekent.
2. **Stil installeren in de juiste soort**, plus wachten tot de app gesloten is en herstarten. Dit lost het meest zichtbare ongemak op. *Gebouwd op 2026-10-26 op dezelfde branch, commit `5eb213f`; de Planner-update 2026.10.0 → 2026.43.0 is echt uitgevoerd en klopte.* De soort komt uit het register (`WindowsInstaller`/`UninstallString` voor MSI, HKCU of HKLM voor het bereik); een update van een per-gebruiker-installatie neemt de `…_user-setup.exe` als die er is. Het Tauri-sjabloon sluit een draaiende app in stille modus geforceerd af (`RmForceShutdown`), daarom wacht de installer tot de gebruiker zelf afsluit. PDF kan pas een sleutel krijgen als zijn `latest.json` ook de per-gebruiker-setup ondertekent; tot dan loopt PDF via de API-route, nu wel in de juiste soort. Op deze pc staat PDF al dubbel (per gebruiker 2026.43.4 en systeembreed 2026.42.11), het voorbeeld van wat dit voorkomt.
3. **`--update`, `--check`, single-instance en `updates.json`** in de installer; daarmee werkt de knop in de apps.
4. **Release-kit** in de installer-repo, en per app de CI omzetten (sleutel, `latest.json`, tagpoort). Begin met Calc en Pointcloud (fase 5).
5. **Eigen updaters weghalen** uit PDF, Planner, 2D en Cloud Desktop, pas nadat de installer stap 1 tot en met 3 heeft.
6. **Zelf bijwerken van de installer** omzetten naar de JM-Orgue-route.

## Open vragen voor het team

- Eén sleutel voor alle apps (eenvoudig beheer) of één per app (een gelekte sleutel raakt maar één app)? Advies: één per app; de catalogus heeft dan per app een `pubkey`.
- Moet de installer ook bijwerken als iemand de app nooit via de installer installeerde? Advies: ja, zolang de app in het register staat.
- macOS: zonder Apple-ondertekening geen stille update; daar blijft het voorlopig bij een link naar de release.
- Open CAD Studio en Open STL-3DMap Studio staan in repo's waar wij de releases niet maken. Die houden de API-route.
