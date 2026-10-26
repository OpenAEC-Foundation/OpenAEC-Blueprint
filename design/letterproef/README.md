# Letterproef tekstfont (issue #29)

Een letterproef in de echte Rust-weergave. Het team kan hiermee vóór het besluit in [#19](https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/issues/19) zien hoe de kandidaat-tekstfonts in iced uitpakken. Een browser rendert anders, daarom staat de proef in de galerij.

## Openen

```bash
cargo run --bin ui04 letterproef
```

Of kies **Letterproef** rechtsboven in de galerij. Je kunt kiezen:

- **Tekstfont:** Inter, Inter AEC, IBM Plex Sans, Source Sans 3 of Atkinson Hyperlegible Next.
- **Grootte:** 12, 13 of 14 px.
- **Gelijke x-hoogte:** elk font wordt zo geschaald dat zijn x-hoogte gelijk is aan die van Inter op de gekozen grootte.
- **Schaal:** 100, 125 of 150 %. Dit geldt alleen in deze weergave; de rest van de galerij blijft op 100 %.
- **Thema:** Licht, Donker, Blueprint en de twee hoogcontrastthema's, rechtsboven.

De proef toont:

- **Vier echte schermdelen:** een lint, een tabel met codes en getallen, een formulier met eenheden, en een stuk rapporttekst.
- **Alle kandidaten onder elkaar:** daaronder dezelfde regel in elk font, met de verwisselbare tekens I l 1, O 0, rn m, 5 S en 2 Z, en met ⌀, σ en Ĳ.

## Renders

Gemaakt met `cargo test --bin ui04 export_specimen_renders -- --ignored`, op 13 px en 100 %. De knoppen zijn grijs: iced kent de toestand van een knop pas na het eerste event, en een testrender heeft geen events.

| Bestand | Inhoud |
|---|---|
| [1-inter.png](1-inter.png) | Inter, Licht |
| [2-inter-aec.png](2-inter-aec.png) | Inter AEC (#28), Licht |
| [3-ibm-plex-sans.png](3-ibm-plex-sans.png) | IBM Plex Sans, Licht |
| [4-source-sans-3.png](4-source-sans-3.png) | Source Sans 3, Licht |
| [5-atkinson-hyperlegible-next.png](5-atkinson-hyperlegible-next.png) | Atkinson Hyperlegible Next, Licht |
| [x-hoogte-gelijk.png](x-hoogte-gelijk.png) | Alle kandidaten op gelijke x-hoogte |
| [thema-dark.png](thema-dark.png), [thema-high-contrast-dark.png](thema-high-contrast-dark.png), [thema-high-contrast-light.png](thema-high-contrast-light.png) | Inter in Donker en de hoogcontrastthema's |

De schaal van 125 en 150 % werkt alleen in het geopende venster. Die staat niet in de renders en is niet nagekeken in een render.

## Kandidaten

Gemeten in de fontbestanden zelf. De breedte is die van "Funderingsbalk 400×600" in em; bij Source Sans 3 geldt de standaardinstantie van het variabele bestand (ExtraLight 200), dus op gewicht 400 is hij iets breder.

| Font | x-hoogte | Cijfers | Breedte | Ĳ | ⌀ | Bron | Licentie |
|---|---|---|---|---|---|---|---|
| Inter 4.001 | 0,546 em | ongelijk breed | 12,02 em | ja | nee, via Noto | fontpakket | OFL, geen gereserveerde naam |
| Inter AEC (#28) | 0,546 em | gelijk breed | 12,12 em | ja | nee, via Noto | fontpakket, `scripts/build_inter_aec.py` | OFL, geen gereserveerde naam |
| IBM Plex Sans 3.201 | 0,516 em | gelijk breed | 11,37 em | ja | nee, via Noto | google/fonts | OFL, gereserveerde naam "Plex" |
| Source Sans 3 3.052 | 0,478 em | gelijk breed | 9,68 em | ja | nee, via Noto | google/fonts | OFL, gereserveerde naam "Source" |
| Atkinson Hyperlegible Next 2.001 | 0,496 em | ongelijk breed | 11,38 em | ja | nee, via Noto | google/fonts | OFL, geen gereserveerde naam |

- **Bron.** De drie nieuwe kandidaten komen onveranderd uit [google/fonts](https://github.com/google/fonts) op commit `e7db6ca603fd4862010383ff17ffd6cc4ffac1c0`. Ze staan in [`fonts/`](fonts/) met hun OFL-tekst en een [manifest](fonts/manifest.json) met SHA-256 per bestand. Ze zitten alleen in de galerij, niet in de crate `openaec-ui`.
- **Variabele bestanden.** Het zijn variabele fonts. `openaec_ui::fonts::load_variable` registreert ze voor gewicht 400 en 600, waarna iced die gewichten van de `wght`-as tekent. Er wordt dus geen vaste versie gemaakt. Dat is nodig voor Plex en Source: een gewijzigde versie mag hun gereserveerde naam niet dragen.

## Wat opvalt

Dit zijn waarnemingen, nog geen oordeel:

- **Grootte.** Op dezelfde grootte ogen Source Sans 3 en Atkinson duidelijk kleiner, door hun lagere x-hoogte. Vergelijk daarom ook met **Gelijke x-hoogte**; Source Sans 3 wordt dan ongeveer 15 px bij 13 px Inter.
- **Breedte.** Source Sans 3 is het smalst: lange omschrijvingen passen beter in een kolom.
- **Cijfers.** Inter en Atkinson hebben cijfers van ongelijke breedte. Getallen in tabellen gebruiken daarom Inter AEC (#28). IBM Plex Sans en Source Sans 3 hebben standaard al gelijke cijfers.
- **Verwisselbare tekens.** I, l en 1 zijn goed te onderscheiden in Inter AEC, IBM Plex Sans en Atkinson. In gewone Inter en in Source Sans 3 lijken I en l sterk op elkaar.
- **Nul.** Atkinson heeft een doorgestreepte nul. Die lijkt op Ø en ⌀ in wapening- en paalcodes.
- **⌀.** Geen van de kandidaten heeft ⌀; dat teken komt overal uit Noto Sans Symbols (#25).

## Oordeel

Nog geen besluit. Het besluit over font en grootte ligt bij het team, in #19. Deze proef is het materiaal daarvoor.
