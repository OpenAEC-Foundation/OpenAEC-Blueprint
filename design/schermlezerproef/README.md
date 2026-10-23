# Schermlezerproef iced — 23 oktober 2026

Kan een app die met iced is gebouwd met een schermlezer worden bediend op Windows? Deze proef hoort bij bevinding UI-001 van het [UI-onderzoek](../ui-onderzoek-2026-10-22/README.md): "Native hulptechnologie vroeg bewijzen".

## Stand van iced

- **iced 0.14.0** (december 2025, nu de basis van `openaec-ui`) heeft geen schermlezerondersteuning. Wel kreeg 0.14 nieuwe focusbewerkingen (`is_focused`, `unfocus`, Tab-ondersteuning in het venster), waarop een eigen toetsenbordroute kan voortbouwen.
- De maker van iced werkt er zelf aan. In maart 2026 wees hij een complete bijdrage af met "I'll work on this myself" ([PR #3281](https://github.com/iced-rs/iced/pull/3281)). Een datum is niet bekend. Het verzoek staat al sinds 2020 open ([issue #552](https://github.com/iced-rs/iced/issues/552)).
- Twee forks zeggen schermlezers al te ondersteunen via [AccessKit](https://accesskit.dev): de COSMIC-fork van System76 ([pop-os/iced](https://github.com/pop-os/iced)) en [plushie-iced](https://github.com/plushie-ui/plushie-iced). Die zijn hier getest.

## Opzet

Eén proefscherm ([`proef.rs`](proef.rs)) met wat een OpenAEC-app het meest nodig heeft: een invoerveld, twee knoppen, een checkbox, een schakelaar, een keuzelijst, een tabel van tekst en een dialoog. Het scherm gebruikt alleen gewone iced-widgets, zonder extra toegankelijkheidscode. Zo meet de proef wat een fork uit zichzelf aan een schermlezer geeft.

| Map | Basis | Versie |
|---|---|---|
| [`plushie/`](plushie/) | plushie-iced | 0.8.4 (8 mei 2026), feature `a11y` |
| [`cosmic/`](cosmic/) | pop-os/iced | commit `229186b` (15 oktober 2026), features `a11y` en `winit` |
| [`cosmic-gerepareerd/`](cosmic-gerepareerd/) | als `cosmic/` | met een reparatie van één regel in AccessKit, zie hieronder |

De meting gebruikt UI Automation, de interface waaruit Verteller en NVDA op Windows lezen:

- [`meet-uia.ps1`](meet-uia.ps1): de boom die een schermlezer krijgt (rol, naam, waarde, stand, acties) en de Tab-route.
- [`meet-tab.ps1`](meet-tab.ps1): de focus na elke Tab, met en zonder een geforceerde hertekening, plus een schermafbeelding.
- [`meet-acties.ps1`](meet-acties.ps1): de acties die een schermlezer de gebruiker biedt: knop indrukken, checkbox omzetten, tekst invullen en de dialoog openen.

## Uitslag

| Toets | plushie-iced | COSMIC-fork | COSMIC, gerepareerd |
|---|---|---|---|
| Bouwt op Windows met toegankelijkheid aan | ja | **nee**, AccessKit-koppeling compileert niet ([uitslag](uitslag-cosmic.txt)) | ja |
| Venster met titel in de boom | ja | — | nee, leeg venster zonder naam |
| Onderdelen in de boom ([uitslag](uitslag-plushie.txt)) | ja: `Edit`, `Button`, `CheckBox`, `ComboBox`, `Text` met naam, waarde en stand | — | nee ([uitslag](uitslag-cosmic-gerepareerd.txt)) |
| Schakelaar | als knop met stand; Windows heeft geen eigen rol | — | — |
| Tabel | losse tekstregels, geen rijen of kolomkoppen (de proef gebruikt geen tabelwidget) | — | — |
| Tab verplaatst de focus zichtbaar | ja | — | niet gemeten |
| Schermlezer hoort de nieuwe focus na Tab | **nee**, pas na een hertekening om een andere reden | — | nee |
| Knop indrukken via de schermlezer (Invoke) | ja | — | nee |
| Checkbox omzetten via de schermlezer (Toggle) | ja | — | nee |
| Tekst invullen via de schermlezer (SetValue) | **nee**, het veld blijft leeg | — | nee |
| Dialoog in de boom na openen | ja; de knoppen erachter blijven ook bereikbaar, want de proef gebruikt geen modaal widget | — | nee |

Verdere meetdetails:

- **Eerste aanvraag:** AccessKit geeft bij de eerste aanvraag alleen het venster terug en stuurt de volledige boom pas bij de volgende verandering. Daarom tekent het meetscript het venster één keer opnieuw door het 2 px te verbreden.
- **Focus na Tab in plushie-iced:** met zo'n hertekening na elke Tab ziet de schermlezer de focus wel goed verspringen: invoerveld, Opslaan, Rapport meesturen. Zonder hertekening blijft de focus voor de schermlezer op het venster staan, ook na 1,5 seconde wachten.
- **Reparatie van de COSMIC-fork:** de fork zet `wash2/accesskit` vast op commit `6c20249`. Daarin verwacht de Windows-code `&Window`, terwijl de winit van de fork `&dyn Window` geeft. Met die ene aanpassing ([`herstel-accesskit.sh`](herstel-accesskit.sh)) bouwt de fork wel, maar Windows krijgt dan nog steeds geen onderdelen te zien. De fork richt zich op Linux (Wayland); Windows is daar in de praktijk niet in gebruik.

## Oordeel

**Geen van beide forks is nu bruikbaar voor een OpenAEC-app op Windows.**

- **plushie-iced** is duidelijk het verst. Rollen, namen, standen, knoppen indrukken en de Tab-volgorde werken uit zichzelf. Er ontbreken nog twee dingen die een schermlezergebruiker meteen merkt: de focus wordt niet doorgegeven en tekst invullen via de schermlezer werkt niet. Daarnaast is het project klein: 4 sterren, één beheerder, de laatste release in mei 2026. De API volgt de ontwikkelversie van iced, niet 0.14, dus `openaec-ui` zou opnieuw moeten worden omgezet.
- **De COSMIC-fork** ondersteunt Windows in de praktijk niet.
- **iced zelf** krijgt het waarschijnlijk wel, maar wanneer is onbekend.

## Advies

1. **Blijf op iced 0.14.** Dat is gebeurd op 23 oktober 2026: `openaec-ui`, de galerij en de Style Repo draaien erop.
2. **Bouw nu de toetsenbordroute in `openaec-ui`** (UI-002 en UI-003): Tab-volgorde, activeren met Enter en spatie, focus die in een dialoog blijft, en focus terug na sluiten. Dat is op 0.14 mogelijk, is nuttig zonder schermlezer, en is precies wat een schermlezerlaag later nodig heeft.
3. **Geef elk onderdeel van de bibliotheek nu al een toegankelijke naam en rol** in zijn API, ook als iced die nog niet doorgeeft. Dan hoeven apps niets aan te passen zodra iced het ondersteunt.
4. **Laat apps alleen `openaec_ui::design` gebruiken**, niet rechtstreeks iced. Dan kan de basis later wisselen naar een iced-versie met toegankelijkheid, of naar een fork.
5. **Herhaal deze proef** bij elke nieuwe iced-release, en over drie maanden voor plushie-iced. De scripts hier zijn daarvoor gemaakt.
6. **Moet een app eerder met een schermlezer werken?** Kies dan voor die app het webpakket: in de browser krijgt HTML de toegankelijkheid van het platform er gratis bij. Of besluit als team om bij te dragen aan de toegankelijkheid van iced zelf.

## Grenzen

Dit is een technische meting van wat een schermlezer te zien krijgt, geen test met mensen. Niemand heeft Verteller of NVDA ook echt beluisterd; doe dat voordat de uitslag als bewijs dient. De proef draaide op één Windows 11-machine, zonder Mac of Linux. Er zijn alleen standaardwidgets getest, niet de eigen widgets van `openaec-ui`.

## Herhalen

```bash
cd design/schermlezerproef/plushie && cargo build --release
powershell -File design/schermlezerproef/meet-uia.ps1 -Exe target/schermlezerproef/plushie/release/schermlezerproef-plushie.exe
```

De proefmappen bouwen in `target/schermlezerproef/` (genegeerd door git). Voor `cosmic-gerepareerd/` eerst één keer `cargo build` in `cosmic/` draaien, zodat AccessKit is opgehaald, en daarna `sh design/schermlezerproef/herstel-accesskit.sh` vanuit de hoofdmap.
