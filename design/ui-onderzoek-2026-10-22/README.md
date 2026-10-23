# OpenAEC UI-onderzoek — 22/23 oktober 2026

Uitgebreid bureauonderzoek voor de harmonisatie van website en technische OpenAEC-apps. Het pakket bevat het oorspronkelijke typografie-/vormonderzoek, vijftien UI-onderwerpen, bronnen, bevindingen, uitgevoerde geïsoleerde proeven en zes voorgestelde volledige taakproeven.

## Begin hier

- [Ochtendadvies en keuzes voor het gezamenlijke plan](outputs/OpenAEC-UI-ochtendoverzicht.html)
- [Volledig verdiepend UI-onderzoek](outputs/OpenAEC-UI-verdiepingsonderzoek.html)
- [Lettertype, rondingen, kleur en interactieve letterproef](outputs/OpenAEC-ontwerponderzoek.html)
- [Zes voorgestelde taakproeven](outputs/OpenAEC-UI-taakproeven.html)

Download de map of open de HTML-bestanden vanuit een lokale checkout; GitHub toont HTML doorgaans als broncode. De oorspronkelijke letterproef bevat de benodigde fontbestanden en notices ingebed. Publicatie van dit pakket verandert geen bestaande ontwerpbesluiten of productiecomponenten.

## Bewijs en grenzen

- [Bronregister](outputs/OpenAEC-UI-bronnen.json): primaire documentatie, onderzoek, openbare ervaringen en gepinde OpenAEC-bronplaatsen.
- [Bevindingen](outputs/OpenAEC-UI-bevindingen.json) en [dekkingsmatrix](outputs/OpenAEC-UI-dekkingsmatrix.json): prioriteiten zijn voorstellen; bureauonderzoek betekent geen volledige productconformiteit.
- [Uitgevoerde proeven](outputs/OpenAEC-UI-proeven.json): exacte scope en bronversie per geïsoleerde proef.
- [Versieaudit](outputs/OpenAEC-UI-versieaudit.json): oorspronkelijke snapshots, nieuwere 0.4-implementatie en laatste PDF-versiecontrole.
- [Componentcontracten](outputs/OpenAEC-UI-componentcontracten.json) en [voorkeurenaudit](outputs/OpenAEC-UI-voorkeurenaudit.json).
- [Oorspronkelijk font-/contrastbewijs](outputs/OpenAEC-onderzoeksbewijs.json).

De zes volledige taakproeven zijn **voorstellen en niet uitgevoerd**. Native-/browserintegratie, hulptechnologie, echte apparaten, printeruitvoer, crash-/offlineherstel en gebruikersvalidatie blijven te toetsen. Een individuele geslaagde functieproef bewijst niet de volledige app. De lokale browsercontrole voor de latere rapportuitbreidingen werd door een URL-policy geblokkeerd; daarvoor is geen omweg gebruikt.

## Opbouw en herkomst

`outputs/` bevat alle vijftien oorspronkelijke opleverbestanden. `work/` bewaart de rapportbouwers, moduleteksten, bron-/bevindingregisters, website-/fontsnapshots, proefharnassen, uitvoer, audits en overdracht. Serverlogs, proces-ID’s, Python-cache en de gecompileerde tijdelijke proefbinary zijn weggelaten; proefbron en resultaten zijn aanwezig.

`work/OpenAEC-Style-Repo/` is een **gedeeltelijke historische bronkopie** van `befcbff7790e8c593b2ec47ae18d43115a4f530c`, geen tweede werkende checkout. Zij bewaart de oorspronkelijke bronhashes nadat de hoofdrepository verder is ontwikkeld. Nieuwere gepinde bronnen staan in `work/ui-research/upstream/`. De kopieën, scripts en historische instructies dienen als onderzoeksbewijs; zij vervangen de actuele afspraken en code van de repository niet.

Herkomst-URL’s, commits en hashes staan in de bronregisters en `manifest.json`-bestanden. Fontnotices zijn ingebed in de letterproef en aanwezig bij de bronbestanden; de gepinde iced-bronkopie bevat de oorspronkelijke MIT-license. De oorspronkelijke herkomst en notices blijven behouden.

## Controle en onderhoud

Voer de artifactcontrole uit vanaf deze map:

```bash
python3 work/validate_ui_research.py --no-write
```

Dit controleert rapport-/ankerlinks, registerrelaties, gepinde bronhashes en de elf ingebedde fonts. De publicatievariant heeft `--no-write` om de bewaarde QA-uitvoer intact te laten. Het voert geen productieapp of volledige taakproef uit. De oorspronkelijke afsluitcontrole staat in `work/ui-research/report-qa-final.json`; de publicatiecontrole staat in `work/ui-research/report-qa-publication.json`.

De twee rapportbouwers kunnen de bestaande teksten opnieuw samenstellen:

```bash
python3 work/build_ui_task_plan.py
python3 work/build_ui_research.py
```

De `record_ui_run_*`, `append_ui_*`, `close_ui_research.py` en oorspronkelijke audit-/proefscripts documenteren eenmalige onderzoeksstappen. Voer ze niet als algemene bouwopdracht opnieuw uit: ze kunnen historische registers/uitvoer aanpassen of de oorspronkelijke lokale omgeving verwachten. Nieuwe validatie krijgt een eigen versie en resultaat; behoud het oorspronkelijke bewijs.

`publication-manifest.json` beschrijft de opgenomen bestanden en hun SHA-256-hashes. Een lokale `.gitattributes` bewaart de exacte bytes, ook bij een checkout met automatische regeleindconversie. Whitespacecontroles zijn voor de historische bron-/bewijsbestanden uitgezet zodat CRLF en spaties in oorspronkelijke notices niet worden herschreven.
