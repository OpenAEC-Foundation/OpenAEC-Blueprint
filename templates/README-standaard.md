# README-standaard voor OpenAEC-repositories

**Status: concept.** Opgesteld naar de README van [Open Planner Studio](https://github.com/OpenAEC-Foundation/open-planner-studio) en voor het eerst toegepast op de README van deze repository ([`README.md`](../README.md), [`README.nl.md`](../README.nl.md)). Het sjabloon om mee te beginnen is [`README-tool.md`](README-tool.md).

## Waarom

Wie een OpenAEC-repository opent, ziet eerst de README. Elke README begint daarom op dezelfde manier: wat het is, hoe je het probeert, hoe je het installeert, en hoe het eruitziet. Daarna volgen de details voor wie verder leest, en altijd eerlijk wat nog niet kan.

## Bestanden

| Eis | Toelichting |
|-----|-------------|
| `README.md` in het Engels | Wat GitHub toont. Engels, want de tools zijn voor iedereen. |
| `README.nl.md` in het Nederlands | Zelfde opbouw, zelfde beelden, zelfde volgorde. Wie de ene wijzigt, wijzigt de andere mee. |
| Taalkeuze op de eerste regel | `**English** · [Nederlands](README.nl.md)` en omgekeerd `[English](README.md) · **Nederlands**`. |
| Beelden in `docs/images/readme/` | PNG, hoogstens 150 kB per beeld, breedte 1280 tot 1600 px. Een animatie (`demo.gif`) mag, liever onder 2 MB. |
| Meerdere schermafbeeldingen | Zoveel als relevant is, niet één. Elk beeld laat iets zien dat de andere niet laten zien: een ander scherm, een andere werkwijze, een ander thema of een andere vorm van de app. Twee beelden die bijna hetzelfde tonen, worden er één. |
| Beelden met een script | Elk beeld komt uit een script dat je opnieuw kunt draaien, niet uit een losse schermafdruk. Het script staat in de repository en wordt in de README of in `scripts/README.md` genoemd. Voorbeelden: `scripts/generate-readme-screenshots.mjs` in Planner, `scripts/build_readme_images.py` en `web/online/screenshots.mjs` hier. |

## Opbouw, in deze volgorde

Verplicht is **vet**. De rest neem je op als het voor die repository iets zegt; laat een sectie weg in plaats van haar leeg te laten.

1. **Kop, gecentreerd** (`<div align="center">`):
   - naam als `#`-kop;
   - één vetgedrukte zin: wat het is en wat het onderscheidt;
   - badges: versie of release, CI of releaseworkflow, licentie, en hoogstens twee feitelijke getallen (talen, iconen, downloads);
   - grote links: *Try in your browser* (als er een webversie is) · *Download*;
   - hoofdbeeld: een korte demo-animatie of de sterkste schermafbeelding, met een alt-tekst die zegt wat je ziet.
2. **Inleiding**: twee korte alinea's. Wat het is en voor wie, en waar het draait.
3. **Try it**: de snelste weg om het te zien, met wat de gebruiker daar meteen kan doen.
4. **Download**: tabel per platform met de bestandssoorten, hoe updaten gaat, en hoe de bestanden zijn ondertekend.
5. **Why use it?**: vier tot acht punten, elk met een vetgedrukte kern en één zin uitleg.
6. **Screenshots**: tabel van twee kolommen met minstens vier beelden, en meer als dat relevant is; elk beeld met een vetgedrukt bijschrift. Een oneven laatste cel blijft leeg. Staan beelden in een andere taal dan de README, zeg dat in één zin.
7. Inhoudelijke secties per hoofdfunctie (bij Planner: planning, uitwisseling, rapporten, MCP). Elke sectie verwijst naar de uitgebreide documentatie. Laat een sectie iets zien wat tekst slecht uitlegt, zet er dan eigen schermafbeeldingen bij, ook meerdere naast elkaar in een tabel van twee kolommen. Een beeld uit de galerij herhaal je daar niet.
8. **Interoperability** of **open formats**: welke formaten in en uit gaan, met wat er verloren gaat. Bij tools met IFC of IFCX verplicht.
9. **MCP**: als de tool een MCP-server heeft, wat die kan, wat de gebruiker in de hand houdt en waar hij draait.
10. **Testing and reliability**: wat er getest wordt, met getallen die uit de repository te tellen zijn, en waar die getallen vandaan komen. Geen beloftes die de tests niet dragen.
11. **Current limitations**: wat nog niet kan of niet af is, concreet. Elke beperking in één vetgedrukte zin met daarna de uitleg. Eindig met een link om een issue te maken.
12. **Under the hood**: de techniek in één alinea.
13. **Contributing**: issues, discussies, testbestanden, code; met links naar `CONTRIBUTING.md` en `AGENTS.md` als die er zijn.
14. **Quick start (developers)**: één codeblok van clonen tot draaien, daaronder de vereiste versies (Node, Rust, Python).
15. **License**: licentie en verwijzing naar `LICENSE`, en naar `NOTICE.md` als er onderdelen met een andere licentie zijn.
16. **Trademarks**: als de README merknamen van anderen noemt, zeg dat het project er los van staat.

Onder *Quick start* of *Contributing* staat één zin dat de tool bij de [OpenAEC Foundation](https://github.com/OpenAEC-Foundation) hoort.

## Schrijfwijze

- Korte zinnen, actieve vorm, de lezer als *you* / *je*.
- Getallen alleen als ze kloppen en te controleren zijn; noem de bron als het geen voor de hand liggende telling is.
- Geen marketingtaal: zeg wat het doet, niet hoe goed het is.
- Bestandsnamen, commando's en opties in `code`.
- Versienummers volgens het OpenAEC-schema `JJJJ.W.N` (zie de [README](../README.nl.md#versienummers)).
- Interne verwijzingen relatief (`docs/…`, `LICENSE`), externe met de volledige URL.

## Controle

Een repository die deze standaard volgt, heeft een controle die faalt als een README naar een beeld verwijst dat er niet is, als een beeld in `docs/images/readme/` door geen van beide README's wordt gebruikt, of als een beeld groter is dan 150 kB. In deze repository doet `python scripts/build_readme_images.py --check` dat.

## Nog uit te werken

- Deze standaard en het sjabloon in elke OpenAEC-repository toepassen; per repository een issue.
- Een gedeelde controle in [`conventions`](https://github.com/OpenAEC-Foundation/conventions), zodat elke repository hem kan aanroepen in plaats van een eigen script te hebben.
- Of de standaard daarna naar `conventions` verhuist, omdat andere repositories daar al naar verwijzen.
