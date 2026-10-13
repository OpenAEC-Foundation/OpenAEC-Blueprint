# OpenAEC — Marketing & PR strategie

> Status: kick-off mei 2026. Doel: van LinkedIn-bubbel naar **brede zichtbaarheid in NL AEC + open source community** binnen 12 maanden.

## Inhoud van deze map

| Bestand | Wat staat erin |
|---------|----------------|
| `README.md` (dit) | Strategie, doelgroepen, KPI's, prioriteiten |
| `channels.md` | Alle kanalen met owner-status, bereik, kosten |
| `article-pitches.md` | 8 ready-to-pitch artikel-ideeën voor NL vakbladen |
| `social-playbook.md` | Instagram + multi-platform contentplan |
| `analytics-setup.md` | Wat we eerst moeten meten voor we kunnen optimaliseren |

---

## Diagnose: waar staan we nu?

**Wat goed werkt:**
- Sterke productenrange (20 tools, 5.380+ downloads)
- Unieke positionering: open source + IFCX + BRO + GWW
- LinkedIn-aanwezigheid van Rick + de stichting
- Authentieke supporters (VORM, GAF, Bengcert, 3BM, Domera, Impertio, …)

**Wat ontbreekt:**
- **Géén analytics** op live demos én op website (eerst fixen — zie `analytics-setup.md`)
- Géén Instagram / Bluesky / Mastodon / YouTube-aanwezigheid
- Géén PR-perslijst, géén relatie met vakbladen
- Géén onboarding-funnel voor nieuwe bezoekers (mensen die binnenkomen kunnen niet "subscriben")
- "Show HN" of FOSDEM-presentatie is nooit gedaan — gratis groot publiek mis ik
- Tools die nog niet productie-rijp zijn (BCF Manager, Cloud Platform) drukken het beeld

---

## Doelgroepen — top drie

In volgorde van **marketing-prioriteit**, niet van waarde:

### 1. Nederlandse BIM-modelleurs & engineering bureaus (60% effort)
- Waar zitten ze: LinkedIn, Cobouw, BIM Magazine, Bouwbeurs Utrecht, BIM Loket
- Wat hen triggert: kostenbesparing tov Autodesk/Bluebeam, open IFC 4.3, BRO-koppeling
- Beste haakjes: **Open PDF Studio** (Bluebeam-alternatief), **Open Geotechniek Studio** (BRO uniek), **Open BIM Validator Studio** (IDS/ILS)

### 2. Studenten & docenten Bouw/Civiel HBO/WO (20% effort)
- Waar zitten ze: TU Delft (CiTG + Architecture), TU/e, Avans, HZ, ROC's
- Wat hen triggert: gratis licenties, leerbaar IFC-stack, scriptie-mogelijkheden
- Beste haakjes: **Curriculum-pakket** (les-PDFs, voorbeeldprojecten), guest lectures

### 3. Open source / BIM-internationaal (20% effort)
- Waar zitten ze: buildingSMART, GitHub trending, Hacker News, FOSDEM, FOSS4G
- Wat hen triggert: IFCX-leiderschap, geo-extensies, Rust/Tauri tech stack
- Beste haakjes: **IFCX**, **Open Geotechniek Studio** (BRO is uniek), tech-blogposts over Rust + IFC

---

## KPI's — wat meten we?

| Metric | Nu (mei 2026) | Q3 doel | Q4 doel | Bron |
|--------|--------------:|--------:|--------:|------|
| GitHub stars (org) | 403 | 600 | 800 | `data/stats.json` |
| Downloads (totaal) | 5.380 | 7.500 | 10.000 | `data/downloads.json` |
| LinkedIn followers stichting | ? | +30% | +60% | LinkedIn analytics |
| **Unique visitors website** | **onbekend ❌** | meten | 5k/mnd | **eerst Plausible installeren** |
| Instagram followers | 0 | 500 | 1.500 | (account aanmaken) |
| Newsletter subscribers | 0 | 100 | 400 | (lijst opzetten) |
| Artikelen in vakbladen | 0 | 1 | 3 | manueel bijhouden |
| Live demo views/mnd | **onbekend ❌** | meten | 2k/mnd | analytics op subdomains |
| Supporter-conversies | 11 | 14 | 18 | supporters/index.html |

> ⚠ **De eerste KPI's die "onbekend" zijn — daar gaat de eerste week aan op.** Geen meten = geen sturen.

---

## Strategische prioriteiten (in volgorde)

### Sprint 1: maak meetbaar wat we doen (week 1, ~2 dagen werk)
1. **Plausible Analytics** installeren op `www.open-aec.com` + alle `*.open-aec.com` subdomeinen (10 min snippet, €9/mnd cloud of self-host gratis)
2. **UTM-tagging** standaard maken voor elke LinkedIn-post, footer in mails, etc.
3. Een `/marketing/dashboard.md` die wekelijks geüpdate wordt (gewoon copy-paste van Plausible)
4. **Newsletter-form** op homepage (Buttondown of EmailOctopus, geen Mailchimp — privacy)

### Sprint 2: ga waar onze doelgroep al is (week 2-4)
1. **Eén artikel pitchen bij Cobouw** met haak "Bluebeam-alternatief uit Nederland" — concept-tekst staat klaar in `article-pitches.md`
2. **Eén pitch bij Bouw en ICT** met IFCX-techniek-focus
3. **Instagram-account aanmaken** + eerste 10 reels-scripts schrijven (`social-playbook.md`)
4. **Mastodon/Bluesky account** + cross-poster opzetten — gratis bereik bij open-source publiek
5. **Awesome-lists** PR's: awesome-bim, awesome-open-source-construction, awesome-rust

### Sprint 3: één "show-stopper" moment (week 5-8)
Eén grote release/event waar alles op gericht is. Twee opties:
- **Optie A**: "Show HN: Open Geotechniek Studio — free BRO + IFC 4.3 CPT viewer" op Hacker News (donderdagochtend US tijd). Vereist: productpagina staat als een huis, geen GitHub-rommel zichtbaar.
- **Optie B**: **FOSDEM-talk** in januari 2027 pitchen (deadline september 2026): "Building an open IFC ecosystem for buildings + civil + GWW".

Mijn voorkeur: **Optie A in juli** + Optie B parallel pitchen voor januari.

### Sprint 4: bouw structurele relaties (maand 3-6)
- Maandelijks live demo-uur (YouTube live + Twitch). Eerste 3x doe je alleen, daarna nodig je supporters uit
- **Podcast-tour**: pitchen bij BIM Pioneers, Bouwgenoten, DigiDeal (zie `channels.md`)
- **TU Delft / TU/e** guest lecture aanvragen
- BIM Loket / NLdigital / buildingSMART NL gesprek aanvragen — strategische steun

---

## Quick wins (deze week nog mogelijk)

Geen excuus om deze nog niet te doen:

1. **Plausible.io** installeren — 10 minuten, kost €9/mnd
2. `<meta property="og:image">` + Twitter cards check op alle pagina's — sociale shares worden mooier
3. **Profiel op Mastodon** (@openaec@mastodon.nl) en **Bluesky** (@openaec.bsky.social) — gratis, 30 min werk
4. **Awesome-bim** PR maken op github.com/mfedderly/awesome-bim — 15 min, één-tijds-effort
5. Slack/Discord van **buildingSMART Netherlands** vinden + introduceren
6. **"Tools wij gebruiken" blogpost** schrijven — bestaande supporters, retentie + SEO
7. Een **`/pers/` pagina** op de site: persmap met logo's, korte bio, screenshots in hoge res, contact

---

## Wat we NIET gaan doen

Net zo belangrijk:

- ❌ **Geen Twitter/X-investering** — community is daar uit elkaar, EN-only bereik, lage conversie
- ❌ **Geen TikTok** — doelgroep (engineers 30-55) zit er niet
- ❌ **Geen betaalde Google/Meta ads** vóór Q1 2027 — eerst organische funnel werkend
- ❌ **Geen agency inhuren** voor copy — eigen stem is sterker dan een bureau

---

## Budget-indicatie

Voor 12 maanden, alle quick wins + sprint 1-4:

| Item | Kost/mnd | Kost/jaar |
|------|---------:|----------:|
| Plausible Analytics cloud | €9 | €108 |
| Newsletter (Buttondown 500 abo's) | €9 | €108 |
| Domains Mastodon/Bluesky | €0 | €0 |
| Instagram/LinkedIn ads (Q1 2027) | €0 | €0 → €500 budget Q1 |
| FOSDEM reis (1 persoon, Brussel) | — | €300 |
| Bouwbeurs ticket | — | €60 |
| Vakblad-artikel (meestal gratis, soms €0-150 voor placement) | — | €500 |
| Camera/microfoon voor demo's | — | €400 (eenmalig) |
| **Totaal jaar 1** | | **~€1.876** |

Volledig haalbaar binnen het bestaande sponsor-model.
