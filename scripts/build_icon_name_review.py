"""Compare same-name UI icons across tools without equating their commands."""
from __future__ import annotations

import html
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_icon_semantics import ROOT, candidates, icon_records, norm

ASSESSMENTS = {
    "about": ("related-intent", "PDF en CAD tonen About als applicatie-informatieactie. De PDF-menuactie is nog een TODO; de bedoelde bestemming komt overeen, de implementatie nog niet."),
    "arrowleft": ("related-intent", "Planner en Energy gebruiken de pijl om naar een vorige stap of weergave terug te gaan."),
    "bookopen": ("related-intent", "Planner verwijst naar voorbeelden en Energy naar een handleiding. Beide openen leerinhoud, maar een ander soort bron."),
    "calendar": ("related-intent", "Planner opent de kalender; BCF gebruikt de kalender bij een vervaldatum. Het pictogram verwijst naar datumcontext, maar slechts één toepassing is een knop."),
    "eyeoff": ("related-intent", "Planner verbergt een token; Pointcloud verbergt een puntwolk. Beide schakelen zichtbaarheid uit, met andere privacy- en documentgevolgen."),
    "fileup": ("different-intent", "Planner gebruikt FileUp voor een voortgangsimport; Heatloss zet dezelfde vorm bij Exporteren. Pijlrichting en commando lopen uiteen."),
    "graduationcap": ("different-intent", "Planner gebruikt de afstudeerhoed voor een tutorial; Energy voor het gebouwtype onderwijs."),
    "hand": ("related-intent", "PDF en Heatloss koppelen Hand aan het verschuiven van de werkruimte of tekening. Dit is dezelfde navigatiehandeling in twee canvassen."),
    "hash": ("different-intent", "Planner gebruikt Hash voor automatische WBS-nummering; BCF toont het bij de index van een topic."),
    "home": ("different-intent", "CAD gebruikt Home voor de beginweergave; Energy gebruikt Home als symbool voor de woonfunctie van een gebouw."),
    "pencil": ("related-intent", "Planner en Energy gebruiken Pencil om bestaande gegevens te bewerken; de bewerkte objecten verschillen."),
    "refreshcw": ("different-intent", "Planner koppelt RefreshCw aan opnieuw proberen; de AEC-extensie aan Generate. Een draaipijl bewijst geen gelijke actie."),
    "scissors": ("related-intent", "Planner splitst een taak en Heatloss splitst een ruimte. Beide delen een bestaand object, met andere geometrie en gevolgen."),
    "type": ("related-intent", "Planner gebruikt Type voor tekst in een screenshotannotatie; Heatloss voor tekstannotatie in de modelleur. Beide plaatsen tekst in een canvas."),
    "userplus": ("related-intent", "Planner wijst een resource toe; BCF voegt een projectlid toe. Beide koppelen een persoon, met andere rechten en relaties."),
    "wrench": ("related-intent", "Planner gebruikt Wrench voor de categorie gereedschap; Energy voor de navigatie naar tools. De vorm duidt een tool aan, maar geen gedeeld commando."),
    "xcircle": ("different-intent", "Pointcloud gebruikt XCircle om selectie op te heffen; Energy toont het bij mislukte controles. Een kruis betekent hier actie tegenover status."),
    "chevrondown": ("related-intent", "De pijl opent of sluit een selectmenu, ribbonkeuze of geavanceerde sectie. De richting is gedeeld, maar het bediende object verschilt."),
    "trash2": ("related-intent", "Alle bronnen verwijderen of trekken een object in: bedrijfsbibliotheekitem, puntwolkobject, warmtebron of API-sleutel. Bevestiging en herstel verschillen."),
    "plus": ("different-intent", "Energy voegt een inventarisitem toe en BCF maakt een sleutel; Planner toont Plus ook als decoratieve extensiekaart. Een plusvorm is geen zelfstandige commando-ID."),
    "alertcircle": ("different-intent", "Planner en Energy tonen een afwijking of fout, terwijl BCF dezelfde vorm gebruikt bij een lege 'Geen issues'-toestand."),
    "alerttriangle": ("different-intent", "Planner toont quarantaine en Energy een waarschuwing; BCF gebruikt dezelfde driehoek voor de KPI 'Open'."),
    "checkcircle2": ("related-intent", "Planner meldt dat de app actueel is, Energy dat een controle slaagde en BCF dat een issue gesloten is. Alle drie zijn positieve statusindicaties met een andere levenscyclus."),
    "chevronright": ("different-intent", "Planner en Energy gebruiken de pijl voor uitklappen of navigeren; BCF gebruikt hem als scheidingsteken in een breadcrumb."),
    "filetext": ("different-intent", "Planner gebruikt FileText voor Nieuw project; de AEC-extensie gebruikt dezelfde vorm voor een PDF-underlay."),
    "layers": ("different-intent", "Planner koppelt Layers aan groeperen; de AEC-extensie koppelt het aan Wall Systems."),
    "building2": ("different-intent", "Planner gebruikt Building2 voor de bibliotheek, Pointcloud voor 3D BAG en Energy als pictogram voor het kantoorgebouwtype."),
    "camera": ("related-intent", "PDF gebruikt de camera voor Screenshot, Energy voor foto-evidence en BCF als beeldplaceholder. Het gaat steeds om beeld, maar niet om dezelfde actie."),
    "circledot": ("different-intent", "Planner gebruikt CircleDot bij een datumnotitie, de AEC-extensie bij IfcRebar en BCF bij de KPI Totaal."),
    "clock": ("related-intent", "Planner toont recente items, Energy een wachtende stap en BCF werk in uitvoering. De vorm duidt tijd aan, maar de statussen zijn verschillend."),
    "eye": ("different-intent", "Planner toont of verbergt een token, Pointcloud schakelt EDL-weergave en BCF labelt viewpoints."),
    "filter": ("different-intent", "Planner filtert plangegevens; Pointcloud gebruikt Filter voor punten uitdunnen. Het CAD-statusicoon heeft nog een aparte contextcontrole nodig."),
    "minus": ("related-intent", "Planner en Energy gebruiken Minus om het venster te minimaliseren. De losse CAD-UI-constante heeft nog geen bewezen gelijk commando."),
    "solid": ("different-intent", "Ondanks identieke SVG-bytes gebruikt Pointcloud solid.svg voor Building, terwijl CAD het als pictogram voor Shaded display inzet."),
    "sphere": ("different-intent", "Ondanks identieke SVG-bytes gebruikt Pointcloud sphere.svg voor Shading, terwijl CAD het bij een sphere-modelprimitief registreert."),
    "distance": ("different-intent", "PDF gebruikt Distance als meetactie; CAD gebruikt distance.svg voor een parametrische afstandsconstraint."),
    "angle": ("different-intent", "PDF gebruikt Angle als meetactie; CAD koppelt angle.svg aan de parametrische ACONSTRAINT-opdracht."),
    "area": ("related-intent", "PDF toont Area bij de meetgereedschappen; CAD gebruikt area.svg in Draw/Inquiry. Vergelijk bediening en resultaat voordat één icoon wordt gekozen."),
    "scale": ("different-intent", "Pointcloud en CAD gebruiken Scale voor geometrische schaling; Planner gebruikt de weegschaal voor resource leveling."),
    "copy": ("different-intent", "CAD kopieert geometrie; Planner, de AEC-extensie en het BCF-platform kopiëren tekst, JSON of sleutels naar het klembord."),
    "move": ("related-intent", "Pointcloud-Translate en CAD-Move verplaatsen geometrie; het extra CAD-UI-icoon vraagt nog een eigen contextcontrole."),
    "upload": ("different-intent", "Dezelfde Upload-vorm staat bij import in Planner en Energy, maar bij export in Pointcloud. De pijlrichting is geen betrouwbare commando-ID."),
    "download": ("different-intent", "Download staat bij export in Planner, AEC en BCF, maar bij import in Pointcloud. De commando-ID moet import en export onderscheiden."),
}

SOURCE_LINK = re.compile(r"/blob/([0-9a-f]+)/(.+?)(?:#L(\d+))?$")
source_cache: dict[tuple[str, str, str], list[str]] = {}


def usage_context(icon: dict) -> str:
    """Read the pinned UI line, without treating source text as instructions."""
    url = urlsplit(icon["source_url"])
    match = SOURCE_LINK.search(url.path + ("#" + url.fragment if url.fragment else ""))
    if not match or not match.group(3):
        return "Actieve knopbundel of codeverwijzing zonder regelnummer"
    repo = url.path.split("/")[2]
    commit, source, line = match.group(1), unquote(match.group(2)), int(match.group(3))
    key = (repo, commit, source)
    if key not in source_cache:
        checkout = Path("/tmp/openaec-inventory") / repo
        if not (checkout / ".git").exists():
            return "Broncode lokaal niet beschikbaar"
        result = subprocess.run(
            ["git", "-C", str(checkout), "show", f"{commit}:{source}"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            return "Bronregel lokaal niet leesbaar"
        source_cache[key] = result.stdout.splitlines()
    lines = source_cache[key]
    if not 1 <= line <= len(lines):
        return "Bronregel valt buiten het bestand"
    excerpt = " ".join(lines[max(0, line - 2):min(len(lines), line + 1)])
    excerpt = re.sub(r"\s+", " ", excerpt).strip()
    return excerpt[:240] + ("…" if len(excerpt) > 240 else "")


def build() -> None:
    groups = defaultdict(list)
    for record in icon_records():
        if not candidates(record["name"]):
            groups[norm(record["name"])].append(record)
    clusters = []
    for key, records in groups.items():
        repositories = sorted({repo for record in records for repo in record["repositories"]})
        if len(records) < 2 or len(repositories) < 2:
            continue
        status, reason = ASSESSMENTS.get(key, ("needs-review", "Dezelfde naam bewijst nog geen gelijke functie of vorm."))
        clusters.append({
            "id": key,
            "label": records[0]["name"],
            "status": status,
            "assessment": reason,
            "repositories": repositories,
            "same_artwork": len({record["sha256"] for record in records}) == 1,
            "icons": records,
        })
    clusters.sort(key=lambda group: (-len(group["repositories"]), -len(group["icons"]), group["id"]))
    assert len(clusters) == 80 and sum(len(group["icons"]) for group in clusters) == 189
    assert set(ASSESSMENTS) <= {group["id"] for group in clusters}
    for group in clusters:
        for icon in group["icons"]:
            icon["usage_context"] = usage_context(icon)
    output = {
        "status": "cross-repository-name-review",
        "note": "Only icons without a canonical shared-name match are grouped. Same names and shapes are research candidates, not automatic adoption decisions.",
        "cluster_count": len(clusters),
        "icon_count": sum(len(group["icons"]) for group in clusters),
        "assessed_count": sum(group["status"] != "needs-review" for group in clusters),
        "clusters": clusters,
    }
    (ROOT / "design/icon-name-review.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")

    cards = []
    for group in clusters:
        thumbs = []
        for icon in group["icons"]:
            label = html.escape(icon["repo"] + ": " + icon["path"])
            thumbs.append(
                f'<a class="candidate" href="{html.escape(icon["source_url"], quote=True)}" target="_blank" rel="noopener" title="{label}">'
                f'<span class="preview"><img loading="lazy" src="{html.escape(icon["preview"], quote=True)}" alt=""></span>'
                f'<span class="detail"><b>{html.escape(icon["name"])}</b><small>{html.escape(icon["repo"])}</small>'
                f'<small>{html.escape(icon["evidence"])} · code ↗</small>'
                f'<small class="context">{html.escape(icon["usage_context"])}</small></span></a>'
            )
        category = {
            "different-intent": "Verschillende handelingen",
            "related-intent": "Verwante handelingen",
            "needs-review": "Nog beoordelen",
        }[group["status"]]
        cards.append(
            f'<article class="cluster" data-status="{group["status"]}" data-search="{html.escape((group["id"] + " " + " ".join(group["repositories"])).lower(), quote=True)}">'
            f'<div class="heading"><div><small>{len(group["repositories"])} repositories · {len(group["icons"])} vormen</small><h2>{html.escape(group["label"])}</h2></div>'
            f'<span class="badge {group["status"]}">{category}</span></div>'
            f'<p>{html.escape(group["assessment"])}</p>'
            f'<div class="shape">{"Identieke bronbytes" if group["same_artwork"] else "Verschillende bronvormen"}</div>'
            f'<div class="candidates">{"".join(thumbs)}</div></article>'
        )
    page = '''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenAEC · Naamgenoten onder UI-iconen</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f5f7;color:#2b3139;font:14px/1.5 Inter,"Segoe UI",Arial,sans-serif}header{background:#292e36;border-bottom:4px solid #d97706;color:white;padding:28px max(24px,calc((100vw - 1360px)/2))}header small{color:#efba6e;font-size:11px;letter-spacing:.14em;font-weight:700}h1{font-size:32px;margin:7px 0;letter-spacing:-.025em}header p{color:#d0d4d9;max-width:850px}main{max-width:1408px;margin:auto;padding:24px}.note{background:#fff4e6;border-left:3px solid #d97706;padding:13px 16px;margin-bottom:20px}.controls{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-bottom:19px}.controls input,.controls select{height:38px;padding:0 11px;border:1px solid #cfd4da;border-radius:4px;background:white;color:inherit;font:inherit}.controls input[type=search]{width:280px}.controls input[type=checkbox]{width:16px;height:16px;padding:0;accent-color:#d97706}.controls label{display:flex;align-items:center;gap:7px;white-space:nowrap}.count{margin-left:auto;color:#65707c}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}.cluster{background:white;border:1px solid #dce0e5;border-radius:7px;padding:15px;min-width:0}.heading{display:flex;gap:10px;justify-content:space-between;align-items:start}.heading small{color:#697482;font-size:11px}.heading h2{font-size:20px;margin:3px 0 0}.badge{font-size:11px;font-weight:700;border-radius:4px;padding:4px 7px;white-space:nowrap}.different-intent{background:#fce9e4;color:#a33b21}.related-intent{background:#e8effb;color:#345c9d}.needs-review{background:#fff0d7;color:#875708}.cluster p{min-height:42px;margin:10px 0;color:#4f5a66;font-size:12px}.shape{font-size:11px;color:#67717b;margin-bottom:8px}.candidates{display:grid;gap:6px}.candidate{display:flex;align-items:center;gap:10px;border:1px solid #e1e5e9;border-radius:4px;padding:7px;text-decoration:none;color:inherit;min-width:0}.candidate:hover{border-color:#c8731e;background:#fffaf3}.preview{background:#f7f8f9;display:grid;place-items:center;flex:none;width:48px;height:48px}.preview img{width:var(--icon-size,24px);height:var(--icon-size,24px);object-fit:contain}.dark .preview{background:#27272d}.dark .preview img{filter:invert(1)}.detail{min-width:0}.detail b,.detail small{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.detail small{font-size:11px;color:#68727e}.detail .context{white-space:normal;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;margin-top:3px;color:#4f5b68}.hidden{display:none!important}footer{border-top:1px solid #dce0e5;margin-top:24px;padding:18px 0;font-size:12px;color:#68727e}a{color:#92500b}@media(max-width:600px){header{padding:22px 16px}main{padding:16px}.grid{grid-template-columns:1fr}.count{width:100%;margin-left:0}}
</style></head><body><header><small>OPENAEC · SEMANTISCHE REVIEW</small><h1>Naamgenoten onder UI-iconen</h1><p>80 naamgroepen verbinden 189 met UI-code of actieve knopbundels onderbouwde iconvarianten uit meerdere tools. Acht groepen zijn op hun commando-context beoordeeld; de overige blijven open. De bronregel staat op elke kaart.</p></header><main><div class="note">Een gelijke bestands- of componentnaam kan een ander commando betekenen. Zelfs identieke SVG-bytes zijn geen besluit om functies samen te voegen. De 26 bestaande gedeelde iconbetekenissen staan in de <a href="icon-semantic-crosswalk.html">semantische kruisvergelijking</a>.</div><div class="controls"><input id="search" type="search" placeholder="Zoek naam of repository" aria-label="Zoek naamgroepen"><select id="status" aria-label="Beoordeling"><option value="">Alle beoordelingen</option><option value="different-intent">Verschillende handelingen</option><option value="related-intent">Verwante handelingen</option><option value="needs-review">Nog beoordelen</option></select><select id="size" aria-label="Icoongrootte"><option value="16">16 px</option><option value="24" selected>24 px</option><option value="32">32 px</option></select><label><input id="dark" type="checkbox"> Donkere achtergrond</label><span id="count" class="count"></span></div><div id="grid" class="grid">''' + "\n".join(cards) + '''</div><footer><a href="review.html">Terug naar ontwerpreview</a> · <a href="icon-name-review.json">Beoordelingsdata en bronregels</a></footer></main><script>
const cards=[...document.querySelectorAll('.cluster')];function filter(){const q=document.getElementById('search').value.trim().toLowerCase(),status=document.getElementById('status').value;let visible=0;for(const card of cards){const show=(!status||card.dataset.status===status)&&(!q||card.dataset.search.includes(q));card.classList.toggle('hidden',!show);if(show)visible++}document.getElementById('count').textContent=visible+' / '+cards.length+' groepen'}for(const id of ['search','status'])document.getElementById(id).addEventListener('input',filter);document.getElementById('size').onchange=e=>document.documentElement.style.setProperty('--icon-size',e.target.value+'px');document.getElementById('dark').onchange=e=>document.body.classList.toggle('dark',e.target.checked);filter();
</script></body></html>'''
    page = page.replace("Acht groepen zijn op hun commando-context beoordeeld", f"{output['assessed_count']} groepen zijn op hun commando-context beoordeeld")
    (ROOT / "design/icon-name-review.html").write_text(page)
    print(f"{len(clusters)} groups, {output['icon_count']} variants, {output['assessed_count']} assessed")


if __name__ == "__main__":
    build()
