# B2-iconen — verliesvrije bibliotheekexport

Deze map bevat de 945 B2-ontwerpen als **1.890 SVGZ-bestanden**, met afzonderlijke masters voor 16 en 24 px. SVGZ is gzip-compressie van de volledige originele SVG. Geen coördinaten zijn afgerond, geen punten zijn verwijderd en de geometrie, kleuren en tekenvolgorde zijn niet aangepast. Uitpakken levert exact dezelfde bytes als de ontwerpmasters in `../svg/`.

[`manifest.json`](manifest.json) koppelt elke icoon-ID aan de bestanden en vermeldt de bronrevisie, bestandsgroottes en SHA-256-hashes van zowel de gecomprimeerde bestanden als de oorspronkelijke SVG’s. De [onafhankelijke controle](../../../harmonization/icon-set-b2/lossless-library-validation.json) bewijst het exacte herstel van alle 1.890 bestanden.

## Gebruik in de bibliotheek

1. Neem de benodigde `.svgz`-bestanden als bytes op, bijvoorbeeld met Rust `include_bytes!`.
2. Pak een icoon bij eerste gebruik met een gzip-decoder uit naar de oorspronkelijke UTF-8-SVG.
3. Pas daarna de bestaande vervanging van hoofdkleur en accentkleur toe.
4. Maak de SVG-handle en hergebruik de bestaande cache. Pak alleen gebruikte iconen uit.

De huidige Rust-`glyph`-functie verwacht een SVG-string. Die vraagt dus nog een inleesadapter; een SVGZ-bestand kan daar niet rechtstreeks als string worden aangeboden. Deze export wijzigt de crate of de widgetcode niet. Opname in de crate en de daarbij behorende licentiecontrole volgen afzonderlijk. De functionele bronnen en ontwerpbesluiten blijven in `../manifest.json` en de bestaande B2-dossiers staan.

Compressie verkleint de opslag; het aantal tekenpunten en de parsekosten van de uitgepakte SVG blijven gelijk. De 16- en 24-px-masters blijven afzonderlijk behouden.

## Opnieuw bouwen en controleren

Voer vanuit de repository-root uit:

```powershell
python scripts/build_b2_lossless_library.py
python scripts/check_b2_lossless_library.py
```

De generator gebruikt geen bestandsnaam of tijdstempel in de gzip-header. Een ongewijzigde invoer levert binnen dezelfde Python/zlib-runtime dezelfde export op; bestaande gelijke bestanden worden niet herschreven. De checker controleert alle bestanden, hashes, bestandstellingen en het exacte herstel tegenover de actuele ontwerpmasters. Een nieuwere bronrevisie vraagt een nieuwe export.
