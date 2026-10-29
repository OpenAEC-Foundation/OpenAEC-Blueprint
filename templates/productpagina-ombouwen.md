# Een app-pagina ombouwen naar de productpagina-standaard

Stappenplan om een bestaande app-pagina op open-aec.com om te bouwen naar de [productpagina-standaard](productpagina-standaard.md). Het is geschreven zodat een AI-assistent (Claude, Codex) het op elke computer kan uitvoeren. Een pagina per keer: de pagina wordt eerst lokaal bekeken, en pas na akkoord gaat hij live.

**Voorbeelden:** [Open Planner Studio](https://open-aec.com/open-planner-studio/) (de eerste) en [Open PDF Studio](https://open-aec.com/open-pdf-studio/), met nieuwe beelden uit een script. Begin met het [sjabloon](productpagina.html) en kijk bij twijfel hoe die twee pagina's het doen.

## 0. Voorbereiden

- Clone de [website-repository](https://github.com/OpenAEC-Foundation/website) en draai een lokale server in de hoofdmap, bijvoorbeeld `npx serve -l 4500` of `python -m http.server 4500`. Open `http://localhost:4500/<slug>/`.
- Node 22 of nieuwer en Google Chrome of Chromium (voor de schermafbeeldingen).
- Zie welke pagina's nog niet omgebouwd zijn: `node scripts/check-product-pages.js`.
- Lees de huidige pagina, `shared/translations/<slug>.json` en de README en release notes van de app (`gh release view -R OpenAEC-Foundation/<repo>`). Schrijf alleen wat de app vandaag kan.
- Werk de SuperCloud-pagina's (`supercloud/`) niet om; die hebben een eigen opzet.
- Ververs de release notes van de app, zodat *Nieuw in vX* en de tijdlijn bij de nieuwste versie beginnen:

  ```bash
  GITHUB_TOKEN=$(gh auth token) node scripts/generate-release-notes.js
  git checkout -- $(git diff --name-only data/release-notes | grep -v "/<repo>.json")   # alleen jouw app houden
  ```

- Heeft de app een gegenereerde functielijst (zoals `data/open-pdf-studio-functies.json` via `scripts/genereer-opds-functies.mjs <pad-naar-app-repo>`), genereer die dan opnieuw uit de broncode van de nieuwste release. Neem getallen op de pagina (aantal functies, MCP-gereedschappen, talen) daaruit over.

## 1. Onderwerpen kiezen en voorleggen

Leg dit voor aan de eigenaar voordat je iets bouwt:

- de **tagline** (één zin over wat de gebruiker ermee wint);
- **drie tot vijf tabbladen** tussen *Hoogtepunten* en *Alle functies*;
- **vier tot zes hoogtepunten**, elk met wat er op het beeld komt;
- welke **voorbeelddata** er in beeld komt. Gebruik een zelfgemaakt, fictief voorbeeld: geen echte projecten, namen of adressen.

## 2. Schermafbeeldingen maken

Gebruik het script in [`productpagina-schermen/`](productpagina-schermen/). Het bedient de webversie van de app in headless Chrome:

```bash
cd templates/productpagina-schermen
URL=https://<app>.open-aec.com/ DSF=1.2  BEELD=hero    node schermen.mjs mijn-stappen.mjs uit
URL=https://<app>.open-aec.com/ DSF=0.75 BEELD=<onderwerp> node schermen.mjs mijn-stappen.mjs uit
```

- `DSF=1.2` geeft het openingsbeeld op 1920×1200, `DSF=0.75` de hoogtepunten op 1200×750 (beide 16:10).
- Schrijf per beeld een scène in je stappenbestand; [`voorbeeld-stappen.mjs`](productpagina-schermen/voorbeeld-stappen.mjs) laat zien hoe.
- Zoek eerst uit welke knoppen er zijn. Log met `app.eval` de `id` en `title` van alle knoppen per lint-tabblad, en maak een verkenningsbeeld voordat je de echte scène schrijft.
- Bekijk elk beeld. Let op losse selectiekaders, tooltips, de muisaanwijzer, zwevende knoppen (verberg ze met `app.hide`) en meldingen.
- Vind je in de app een fout die in beeld komt, laat dat stuk dan weg en meld de fout aan de eigenaar van de app.
- Namen: `shared/assets/screenshots/<slug>-hero.png` en `<slug>-feat-<onderwerp>.png`.

Valkuilen die we tegenkwamen:

- `alert`/`confirm` blokkeert de pagina; het script bevestigt ze en logt de tekst.
- Gereedschappen die een lijn of vlak maken, sluiten vaak af met een **dubbelklik**, niet met een tweede klik.
- Na een contextueel lint-tabblad (bijvoorbeeld *Opmaak* na een selectie) zijn de knoppen van het gewone tabblad weg: klik dat tabblad eerst weer aan.
- Schrijf stappenbestanden met een editor. Via een shell-heredoc verdwijnen backslashes, en dan breken reguliere expressies in `app.eval`.

## 3. De pagina bouwen

- Kopieer [`productpagina.html`](productpagina.html) en vul de `{{…}}` in. Houd de kop en de footer van de huidige pagina, zoals `lang-boot`, `hreflang`, de schema-blokken en de navigatie.
- **Slider in de kop:** eerst het openingsbeeld, dan de beelden van de hoogtepunten in dezelfde volgorde en met dezelfde `data-i18n`-sleutels voor de alt-tekst.
- **Download:** links naar de bestanden van de nieuwste release (`gh release view <tag> --json assets`), met de groottes in MB (bytes / 1048576). Met een Android-app: `pp-files pp-files-4`.
- Werk de JSON-LD bij: `SoftwareApplication` (versie, platforms, `featureList`, schermafbeelding) en een `FAQPage` met dezelfde vragen als op de pagina.
- Haal oude sliderscripts en downloadscripts uit de pagina; dat doet `shared/productpagina.js` nu.
- Verhoog `?v=` bij `productpagina.css`/`.js` als je die gedeelde bestanden wijzigt, op **alle** pagina's die ze laden.

## 4. Vertalen

- Nederlands staat in de HTML. Zet alle teksten in het Engels in `shared/translations/<slug>.json`, met dezelfde sleutels als de `data-i18n`-attributen.
- Controleer of elke sleutel een tekst heeft:

  ```bash
  node -e "const h=require('fs').readFileSync('<slug>/index.html','utf8');const j=require('./shared/translations/<slug>.json');const g=k=>k.split('.').reduce((o,p)=>o&&o[p],j);console.log([...new Set([...h.matchAll(/data-i18n=\"([^\"]+)\"/g)].map(m=>m[1]))].filter(k=>typeof g(k)!=='string'))"
  ```

- Maak daarna `.fr.json`, `.tr.json` en `.es.json` met precies dezelfde sleutels. Volg de woordkeus van de bestaande vertalingen van Open Planner Studio.

## 5. Controleren

- `node scripts/check-product-pages.js`: de pagina moet 9/9 hebben.
- `node scripts/check-*.js` en `node --test scripts/*.test.js`. Noem controles die al faalden voordat je begon apart.
- Bekijk de pagina lokaal op desktop (1440 px) en op een telefoon (375 px):
  - geen horizontale scroll;
  - de slider bladert;
  - de tabbladen tellen goed;
  - de downloadknop kiest het juiste platform;
  - op Android biedt hij de `.apk` aan als die er is.

## 6. Taalversies maken

De scripts `build-i18n-pages.js`, `build-release-notes-static.js` en `build-schema.js` herschrijven **alle** pagina's van de site. Draai ze, en zet daarna alles terug behalve wat bij jouw pagina hoort:

```bash
node scripts/build-i18n-pages.js && node scripts/build-release-notes-static.js && node scripts/build-schema.js
rm -rf en/_voorbeeld fr/_voorbeeld tr/_voorbeeld es/_voorbeeld
# behoud: <slug>/index.html, {en,fr,tr,es}/<slug>/index.html, shared/*, scripts/* en data/* die je zelf wijzigde
git diff --name-only | grep -v -e '^<slug>/' -e '^\(en\|fr\|tr\|es\)/<slug>/' -e '^shared/' -e '^scripts/' -e '^data/' | xargs -r git checkout --
```

Zet ook `sitemap.xml` terug als daarin alleen regeleindes veranderden.

## 7. Live zetten

- Laat de pagina lokaal zien en wacht op akkoord.
- Commit als Engelse Conventional Commit, bijvoorbeeld `feat(<slug>): product page on the 9-block standard`.
- Push naar `main`. Dat zet de site binnen een paar minuten live.
- Controleer daarna de live pagina.
