# Schermafbeeldingen voor een productpagina

Script dat de webversie van een OpenAEC-app in headless Chrome bedient en er de beelden voor de productpagina op open-aec.com van maakt. Hoort bij de [productpagina-standaard](../productpagina-standaard.md); de werkwijze staat in [het stappenplan](../productpagina-ombouwen.md), stap 2.

| Bestand | Wat |
|---------|-----|
| `schermen.mjs` | het script: start Chrome, opent de app en voert een stappenbestand uit |
| `voorbeeld-stappen.mjs` | voorbeeld van een stappenbestand (Open PDF Studio, beeld *Meten*) |
| `maak-tekening.js` | maakt een fictieve tekeningenset "Woning type A" in revisie A en B (vector-PDF, A3) |
| `bestanden/` | voorbeeldbestanden voor `app.files()`; nu de twee revisies van die tekeningenset |

Nodig: Node 22 of nieuwer, en Google Chrome of Chromium. Er zijn geen npm-pakketten nodig.

```bash
URL=https://open-pdf-studio.open-aec.com/ DSF=0.75 BEELD=meten node schermen.mjs voorbeeld-stappen.mjs uit
```

Wat het script vooraf regelt:

- het weigert de statistiekmelding;
- het onderschept de bestandskiezer, zodat `app.files('x.pdf')` gevolgd door *Openen* dat bestand laadt;
- het bevestigt `alert`/`confirm`-vensters en logt hun tekst;
- bij een fout bewaart het een `_fout.png`.

| Hulp in `app` | Doet |
|---------------|------|
| `eval(js)` | JavaScript in de pagina, geeft de waarde terug |
| `files(...namen)` | de volgende bestandskiezer krijgt deze bestanden uit `bestanden/` |
| `click(selector of tekst)` | klikt op een element: CSS-selector, of exacte `title`, `aria-label` of tekst |
| `mouse(x, y, {clickCount})`, `move(x, y)`, `drag(x1, y1, x2, y2)` | muis, in CSS-pixels van het venster van 1600×1000 |
| `key(toets, {ctrl, shift})`, `type(tekst)` | toetsenbord |
| `hide(selector)` | verbergt elementen die niet in beeld horen |
| `shot(naam)` | bewaart een schermafbeelding in de uitmap |
| `waitFor(js, ms)`, `sleep(ms)` | wachten |

Gebruik alleen fictieve voorbeelddata. Een eigen voorbeeldbestand voor een andere app zet je in `bestanden/`, met het script dat het maakt ernaast.
