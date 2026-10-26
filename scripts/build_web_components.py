#!/usr/bin/env python3
"""Build web/componenten.html: every component of web/openaec-components.css in
all five themes, with the B2 icons of Codex inline, in the same compact form as
the sprites of scripts/build_web_icons.py. Run with --check to verify."""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web/componenten.html"
PREVIEWS = "../harmonization/references/openaec-installer/public/previews"
sys.path.insert(0, str(ROOT / "scripts"))
from build_installer_proposals import GITHUB  # noqa: E402
from build_web_icons import icons as b2_icons, symbol  # noqa: E402

ASSETS = {icon_id: assets for icon_id, _, _, assets in b2_icons()}

GITHUB_MARK = re.sub(r'<symbol id="gh" (viewBox="[^"]+")>(.*)</symbol>', r'<svg class="oa-icon" \1 aria-hidden="true">\2</svg>', GITHUB)


USED = {}


def i(icon_id, size=16, extra=""):
    """An inline icon that refers to one symbol per icon in the page's sprite."""
    key = f"i{size}-{icon_id}"
    if key not in USED:
        asset = ASSETS[icon_id][str(size)]
        USED[key] = symbol(icon_id, str(size), asset["path"], asset["original_sha256"])
    cls = "oa-icon" + (" oa-icon--24" if size == 24 else "") + (f" {extra}" if extra else "")
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{key}"/></svg>'


def section(title, intro, body):
    return f'''
  <section class="demo-section">
    <h2 class="oa-heading oa-heading--dialog">{title}</h2>
    <p class="oa-secondary">{intro}</p>
    {body}
  </section>'''


def site_card(name, slug, desc, chips, version, featured=False, update=False):
    chips_html = "".join(f'<span class="oa-chip{" oa-chip--" + t if t else ""}">{c}</span>' for c, t in chips)
    feat = " oa-site-card--featured" if featured else ""
    upd = f'<span class="oa-meta">v2026.38 → <span style="color:var(--oa-accent-text)">v{version}</span></span>' if update else f'<span class="oa-meta">v{version}</span>'
    return f'''<article class="oa-site-card{feat}">
        <img class="oa-preview-image" src="{PREVIEWS}/{slug}.jpg" alt="">
        <div style="display:flex;gap:12px;align-items:center">
          <span class="oa-icon-tile oa-icon-tile--amber">{i("software.install", 24)}</span>
          <div style="display:grid;gap:2px"><b class="oa-tile-title">{name}</b>{upd}</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">{chips_html}</div>
        <p class="oa-secondary" style="margin:0">{desc}</p>
        <div class="oa-card-actions">
          <a class="oa-site-button oa-site-button--primary oa-site-button--small" href="#">{i("update.install") if update else i("link.open-external")} {"Bijwerken" if update else "Openen"}</a>
          <span style="flex:1"></span>
          <a class="oa-round-icon" href="#" data-oa-tip="Broncode op GitHub">{GITHUB_MARK}</a>
          <a class="oa-round-icon" href="#" data-oa-tip="Website">{i("link.open-external")}</a>
        </div>
      </article>'''


def build():
    buttons = f'''
    <div class="demo-row">
      <button class="oa-button oa-button--primary">{i("file.save")} Opslaan</button>
      <button class="oa-button">{i("file.open")} Openen</button>
      <button class="oa-button oa-button--quiet">Niet opslaan</button>
      <button class="oa-button oa-button--danger">{i("edit.delete")} Verwijderen</button>
      <button class="oa-button oa-button--primary" disabled>Uitgeschakeld</button>
      <button class="oa-button oa-button--compact">Compact 24 px</button>
    </div>
    <div class="demo-row">
      <button class="oa-icon-button" aria-label="Ongedaan maken" aria-keyshortcuts="Control+Z" data-oa-tip="Ongedaan maken" data-oa-keys="Ctrl+Z">{i("edit.undo")}</button>
      <button class="oa-icon-button" aria-label="Opnieuw" aria-keyshortcuts="Control+Y" data-oa-tip="Opnieuw" data-oa-keys="Ctrl+Y">{i("edit.redo")}</button>
      <button class="oa-icon-button" aria-pressed="true" aria-label="Raster" data-oa-tip="Raster">{i("view.grid")}</button>
      <button class="oa-icon-button" aria-label="Zoeken" disabled>{i("view.search")}</button>
      <span class="demo-gap"></span>
      <a class="oa-site-button oa-site-button--primary" href="#">{i("software.install")} Installeren</a>
      <a class="oa-site-button" href="#">{i("link.open-external")} Naar de website</a>
      <a class="oa-site-button oa-site-button--small" href="#">Klein</a>
      <a class="oa-round-icon" href="#" data-oa-tip="Broncode">{GITHUB_MARK}</a>
      <a class="oa-round-icon" href="#" data-oa-tip="Openen in webtab">{i("software.open-webtab")}</a>
    </div>'''

    form = f'''
    <div class="demo-grid demo-grid--3">
      <label class="oa-label">Projectnaam <input class="oa-field" value="Kantoor Velp"></label>
      <label class="oa-label">Zoeken <input class="oa-field" placeholder="Typ om te zoeken"></label>
      <label class="oa-label">Discipline <select class="oa-field"><option>Constructie</option><option>Installaties</option></select></label>
      <div class="oa-label">Dikte (mm) <input class="oa-field" aria-invalid="true" value="-20"><div class="oa-field-message">Geef een waarde groter dan 0.</div></div>
      <label class="oa-label">Uitgeschakeld <input class="oa-field" disabled value="Alleen lezen"></label>
      <label class="oa-label">Opmerking <textarea class="oa-field">Twee regels tekst.</textarea></label>
    </div>
    <div class="demo-row">
      <label class="oa-check"><input type="checkbox" checked> Rapport meesturen</label>
      <label class="oa-check"><input type="radio" name="r" checked> Licht</label>
      <label class="oa-check"><input type="radio" name="r"> Donker</label>
      <label class="oa-switch"><input type="checkbox" role="switch" checked> Automatisch bijwerken</label>
      <input class="oa-slider" type="range" value="60">
      <div class="oa-progress" style="width:160px"><span style="width:62%"></span></div>
    </div>'''

    labels = f'''
    <div class="demo-row">
      <span class="oa-status oa-status--success">Gereed</span>
      <span class="oa-status oa-status--warning">Concept</span>
      <span class="oa-status oa-status--error">Fout</span>
      <span class="oa-status oa-status--info">Bezig</span>
      <span class="oa-status">Gearchiveerd</span>
      <span class="demo-gap"></span>
      <span class="oa-chip">Desktop</span><span class="oa-chip">Web</span><span class="oa-chip oa-chip--success">Nieuw</span><span class="oa-chip oa-chip--warning">Bèta</span>
    </div>
    <div class="demo-row">
      <button class="oa-pill" aria-pressed="true">Alle <span class="oa-count">18</span></button>
      <button class="oa-pill">Geïnstalleerd <span class="oa-count">7</span></button>
      <button class="oa-pill">Updates <span class="oa-count">2</span></button>
      <button class="oa-pill"><span class="oa-pill-letter">C</span> Constructie <span class="oa-count">5</span></button>
    </div>'''

    tiles = f'''
    <div class="demo-grid demo-grid--2">
      <div style="display:grid;gap:8px;max-width:620px;align-content:start">
        <a class="oa-tile" href="#"><span class="oa-icon-tile">{i("file.new", 24)}</span><span><span class="oa-tile-title">Nieuw project</span><br><span class="oa-tile-text">Begin met een leeg project of een sjabloon.</span></span></a>
        <a class="oa-tile" href="#"><span class="oa-icon-tile">{i("file.open", 24)}</span><span><span class="oa-tile-title">Project openen</span><br><span class="oa-tile-text">Kies een bestand op deze computer.</span></span></a>
        <div class="oa-recent">
          <a href="#">{i("project.folder")}<span><b>Kantoor Velp</b> <span class="oa-secondary">D:\\Projecten\\2026-041</span></span><span class="oa-meta">vandaag 09:12</span></a>
          <a href="#">{i("project.folder")}<span><b>Brug Arnhem</b> <span class="oa-secondary">D:\\Projecten\\2026-017</span></span><span class="oa-meta">gisteren</span></a>
        </div>
      </div>
      <div class="demo-grid demo-grid--2" role="radiogroup">
        <button class="oa-tile oa-tile--choice" role="radio" aria-checked="true"><span class="oa-icon-tile">{i("report.generate", 24)}</span><span class="oa-radio-dot"></span><span class="oa-tile-title">Volledig rapport</span><span class="oa-tile-text">Met alle berekeningen en bijlagen.</span></button>
        <button class="oa-tile oa-tile--choice" role="radio" aria-checked="false"><span class="oa-icon-tile">{i("report.template", 24)}</span><span class="oa-radio-dot"></span><span class="oa-tile-title">Samenvatting</span><span class="oa-tile-text">Alleen de uitkomsten op één pagina.</span></button>
        <button class="oa-tile oa-project-card"><span class="oa-preview" style="width:100%">{i("project.folder", 24)}</span><span class="oa-card-body"><b class="oa-tile-title">Kantoor Velp</b><span class="oa-meta">CALC · 14 OKT</span><span><span class="oa-status oa-status--success">Gereed</span></span></span></button>
        <div class="oa-info-card"><span class="oa-mono-label">Project</span><dl><dt>Nummer</dt><dd>2026-041</dd><dt>Opdrachtgever</dt><dd>Gemeente Velp</dd><dt>Fase</dt><dd>DO</dd></dl></div>
        <div class="oa-figure-tile"><div class="oa-figure oa-figure--accent">7</div><span class="oa-mono-label">Geïnstalleerd</span></div>
        <div class="oa-figure-tile"><div class="oa-figure">2</div><span class="oa-mono-label">Updates</span></div>
      </div>
    </div>'''

    website = f'''
    <div class="oa-dark-band" style="border-radius:12px 12px 0 0">
      <span class="oa-mono-label">OpenAEC Installer</span>
      <h3 class="oa-heading oa-heading--page" style="font-size:32px;margin:6px 0 8px">Open source software voor de bouw</h3>
      <p class="oa-secondary" style="max-width:520px;margin:0 0 16px">Het donkere vlak volgt de website en blijft donker in elk thema. Alles daaronder volgt het thema.</p>
      <div class="demo-row" style="margin:0">
        <a class="oa-site-button oa-site-button--primary" href="#">{i("software.install")} Alles bijwerken</a>
        <a class="oa-site-button oa-site-button--glass" href="#">{GITHUB_MARK} GitHub</a>
        <span class="demo-gap"></span>
        <div class="oa-glass-card" style="min-width:220px"><span class="oa-mono-label">Uitgelicht</span><div class="oa-heading oa-heading--dialog" style="margin-top:4px">Open PDF Studio</div></div>
      </div>
    </div>
    <div class="demo-grid demo-grid--3" style="padding:20px 0 0">
      {site_card("Open Planner Studio", "open-planner-studio", "Planningen met Gantt, afhankelijkheden en het kritieke pad.", [("Desktop", ""), ("C", "")], "2026.43", featured=True, update=True)}
      {site_card("Open PDF Studio", "open-pdf-studio", "Tekeningen en documenten markeren, meten en samenvoegen.", [("Desktop", ""), ("A", "")], "2026.41")}
      {site_card("BIM Validator", "open-bim-validator", "IFC-modellen toetsen aan IDS-eisen, in de browser.", [("Web", ""), ("Nieuw", "success")], "webtool")}
    </div>'''

    feedback = f'''
    <div style="display:grid;gap:8px">
      <div class="oa-banner oa-banner--warning" role="status">{i("status.warning")}<b>Let op.</b><span>Twee profielen hebben geen materiaal.</span><button class="oa-icon-button oa-icon-button--small" aria-label="Sluiten">{i("ui.close")}</button></div>
      <div class="oa-banner oa-banner--error" role="alert">{i("status.error")}<b>Fout.</b><span>Het bestand kon niet worden opgeslagen.</span><button class="oa-button oa-button--compact">Opnieuw</button></div>
      <div class="oa-banner oa-banner--success">{i("status.success")}<b>Gelukt.</b><span>Rapport gemaakt.</span></div>
      <div class="oa-banner oa-banner--info">{i("status.info")}<b>Info.</b><span>Er is een nieuwe versie beschikbaar.</span></div>
    </div>
    <div class="demo-row" style="align-items:flex-start;margin-top:16px">
      <div class="oa-toast">{i("status.success", extra="demo-success")}<div><b>Opgeslagen</b><span class="oa-secondary">Kantoor Velp.calc is bewaard.</span></div><button class="oa-icon-button oa-icon-button--small" aria-label="Sluiten">{i("ui.close")}</button></div>
      <div class="oa-menu" role="menu">
        <button role="menuitem">{i("edit.copy")} Kopiëren <kbd>Ctrl+C</kbd></button>
        <button role="menuitem">{i("edit.paste")} Plakken <kbd>Ctrl+V</kbd></button>
        <hr>
        <button role="menuitem" class="oa-danger">{i("edit.delete")} Verwijderen <kbd>Del</kbd></button>
      </div>
      <div class="oa-dialog" role="dialog" aria-labelledby="dlg">
        <h3 class="oa-heading oa-heading--dialog" id="dlg" style="margin-bottom:8px">Wijzigingen opslaan?</h3>
        <p class="oa-secondary" style="margin:0">Kantoor Velp heeft wijzigingen die nog niet zijn opgeslagen.</p>
        <div class="oa-dialog-actions"><button class="oa-button oa-button--quiet">Niet opslaan</button><button class="oa-button">Annuleren</button><button class="oa-button oa-button--primary">Opslaan</button></div>
      </div>
    </div>'''

    panels = f'''
    <div class="oa-tabs" role="tablist"><button role="tab" aria-selected="true">Start</button><button role="tab">Invoegen</button><button role="tab">Berekenen</button><button role="tab">Beeld</button></div>
    <div class="oa-document-tabs"><span class="oa-document-tab" aria-selected="true">Kantoor Velp <span class="oa-dirty"></span><button class="oa-icon-button oa-icon-button--small" aria-label="Sluiten">{i("ui.close")}</button></span><span class="oa-document-tab">Brug Arnhem<button class="oa-icon-button oa-icon-button--small" aria-label="Sluiten">{i("ui.close")}</button></span><span class="oa-document-tab" tabindex="0" data-oa-tip="Fundering en paalkoppen blok A, variant 2"><span class="oa-truncate">Fundering en paalkoppen blok A, variant 2</span><button class="oa-icon-button oa-icon-button--small" aria-label="Sluiten">{i("ui.close")}</button></span></div>
    <div class="demo-grid" style="grid-template-columns:240px 1fr;gap:0;border:1px solid var(--oa-border)">
      <div class="oa-panel" style="border:0;border-right:1px solid var(--oa-border);box-shadow:none">
        <div class="oa-panel-header"><span class="oa-mono-label">Eigenschappen</span><button class="oa-icon-button oa-icon-button--small" aria-label="Meer">{i("ui.more")}</button></div>
        <div class="oa-property"><span>Profiel</span><span>HEA 200</span></div>
        <div class="oa-property"><span>Lengte</span><span class="oa-number">6 000 mm</span></div>
        <div class="oa-property"><span>Materiaal</span><select class="oa-field oa-field--compact"><option>S235</option></select></div>
      </div>
      <table class="oa-table" style="background:var(--oa-workspace);color:var(--oa-workspace-text)">
        <thead><tr><th>Element</th><th>Profiel</th><th style="text-align:right">Unity check</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>Ligger 1</td><td>HEA 200</td><td class="oa-number">0,64</td><td><span class="oa-status oa-status--success">Voldoet</span></td></tr>
          <tr aria-selected="true"><td>Ligger 2</td><td>HEA 180</td><td class="oa-number">0,97</td><td><span class="oa-status oa-status--warning">Krap</span></td></tr>
          <tr><td>Kolom 3</td><td>HEB 160</td><td class="oa-number">1,12</td><td><span class="oa-status oa-status--error">Voldoet niet</span></td></tr>
          <tr tabindex="0"><td data-oa-tip="Randligger as A tot en met D, verdieping 2"><span class="oa-truncate" style="max-width:120px">Randligger as A tot en met D, verdieping 2</span></td><td>IPE 300</td><td class="oa-number">0,81</td><td><span class="oa-status oa-status--success">Voldoet</span></td></tr>
        </tbody>
      </table>
    </div>
    <div class="oa-statusbar"><span>Gereed</span><span class="oa-spacer"></span><span>3 elementen</span><span>S235</span><span>100%</span></div>'''

    workflow = f'''
    <div class="oa-workflow" style="border:1px solid var(--oa-border);min-height:320px">
      <nav class="oa-sidebar"><span class="oa-mono-label" style="padding:4px 10px 8px">Rapport</span>
        <a href="#">{i("project.properties")} Projectgegevens</a><a href="#" aria-current="page">{i("report.template")} Sjabloon</a><a href="#">{i("report.generate")} Maken</a></nav>
      <div style="display:flex;flex-direction:column">
        <ol class="oa-steps"><li class="oa-done">Gegevens</li><li aria-current="step">Sjabloon</li><li>Controle</li><li>Maken</li></ol>
        <div style="flex:1;padding:24px;background:var(--oa-frame)">
          <div class="oa-form-card"><h3 class="oa-heading oa-heading--page">Sjabloon kiezen</h3>
            <label class="oa-label">Sjabloon <select class="oa-field"><option>OpenAEC standaard</option></select></label>
            <label class="oa-check"><input type="checkbox" checked> Voorblad toevoegen</label></div>
        </div>
        <div class="oa-action-bar"><span class="oa-secondary">Stap 2 van 4</span><button class="oa-button">Vorige</button><button class="oa-button oa-button--primary">Volgende</button></div>
      </div>
    </div>
    <div class="oa-empty">{i("view.search", 24)}<b style="color:var(--oa-text)">Geen resultaten</b><span>Pas de zoekterm of de filters aan.</span><button class="oa-button">Filters wissen</button></div>'''

    themes = [("light", "Licht"), ("dark", "Donker"), ("blueprint", "Blueprint"), ("high-contrast-dark", "Hoog contrast donker"), ("high-contrast-light", "Hoog contrast licht")]
    options = "".join(f'<option value="{v}">{html.escape(n)}</option>' for v, n in themes)
    body = "".join([
        section("Knoppen", "Appknoppen van 28 px (24 px compact) met een B2-icoon, iconknoppen met tooltip, en de websiteknoppen van de installer.", buttons),
        section("Formulier", "Velden van 28 px. De focusring valt buiten het veld; dat kan op het web wel en in iced niet.", form),
        section("Labels", "Statuslabels in mono, chips en filterpillen met een teller zoals op open-aec.com.", labels),
        section("Tegels en kaarten", "Taaktegels, keuzetegels, projectkaarten, infokaarten en cijfertegels. Tegels komen niet omhoog, alleen de rand verandert.", tiles),
        section("Websitestijl", "Het donkere vlak en de kaarten van installervoorstel E, voor webtools en de installer.", website),
        section("Meldingen, menu en dialoog", "Een kleur is nooit het enige signaal: elke melding heeft een woord.", feedback),
        section("Lint, documenten, paneel en tabel", "Tabbladen met een amber lijn, documenttabs, een eigenschappenpaneel, een tabel zonder zebrastrepen en de statusbalk.", panels),
        section("Werkstroom", "Zijbalk, stappenbalk, formulierkaart en actiebalk, en een lege toestand.", workflow),
    ])
    return f'''<!doctype html>
<!-- Generated by scripts/build_web_components.py. Do not edit by hand. -->
<html lang="nl" data-oa-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenAEC webcomponenten 0.4</title>
<link rel="stylesheet" href="openaec-fonts.css">
<link rel="stylesheet" href="openaec-tokens.css">
<link rel="stylesheet" href="openaec-components.css">
<script src="openaec-components.js" defer></script>
<style>
  /* Layout of this overview only; not part of the package. */
  .demo-top {{ position: sticky; top: 0; z-index: 30; display: flex; align-items: center; gap: 12px; padding: 12px 24px; background: var(--oa-panel); border-bottom: 1px solid var(--oa-border); }}
  .demo-top .oa-heading {{ flex: 1; }}
  main {{ max-width: 1180px; margin: 0 auto; padding: 8px 24px 48px; }}
  .demo-section {{ padding: 24px 0; border-bottom: 1px solid var(--oa-border); }}
  .demo-section > p {{ margin: 4px 0 16px; }}
  .demo-row {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 0 0 12px; }}
  .demo-gap {{ width: 24px; }}
  .demo-grid {{ display: grid; gap: 12px; margin-bottom: 12px; }}
  .demo-grid--2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .demo-grid--3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
  .demo-success {{ color: var(--oa-success); --icon-accent: currentColor; }}
  @media (max-width: 860px) {{ .demo-grid--2, .demo-grid--3, .oa-workflow {{ grid-template-columns: 1fr; }} .oa-sidebar {{ display: none; }} }}
</style>
</head>
<body class="oa-app">
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{"".join(USED.values())}</svg>
<header class="demo-top">
  <h1 class="oa-heading oa-heading--panel">OpenAEC webcomponenten 0.4</h1>
  <label class="oa-secondary" for="theme">Thema</label>
  <select class="oa-field" id="theme">{options}</select>
</header>
<main>{body}
</main>
<script>
  const pick = document.getElementById("theme");
  const saved = location.hash.slice(1);
  if ([...pick.options].some(o => o.value === saved)) pick.value = saved;
  const apply = () => {{ document.documentElement.dataset.oaTheme = pick.value; history.replaceState(null, "", "#" + pick.value); }};
  pick.addEventListener("change", apply);
  apply();
</script>
</body>
</html>
'''


def main():
    text = build()
    # An icon button needs a name of its own; a tooltip alone is no name (issue #7).
    unnamed = [b for b in re.findall(r'<button class="oa-icon-button[^"]*"[^>]*>', text) if "aria-label" not in b]
    if unnamed:
        print(f"Iconknop zonder aria-label: {unnamed[0]}")
        return 1
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("web/componenten.html is verouderd, draai scripts/build_web_components.py")
            return 1
        print("web/componenten.html is actueel")
        return 0
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"web/componenten.html geschreven ({len(text) // 1024} kB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
