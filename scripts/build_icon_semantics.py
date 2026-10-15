#!/usr/bin/env python3
"""Build a traceable, provisional crosswalk from UI icon evidence to shared meanings."""

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"

# These are name candidates, not approvals of shape or meaning. Exact action
# context must be checked before replacing any product icon.
ALIASES = {
    "new": ["new", "filenew", "fileplus", "fileplus2"],
    "open": ["open", "openfile", "folderopen", "folder_open", "toolbarbuttonopenfile"],
    "save": ["save", "saveall"],
    "import": ["import", "fileinput", "cuiimport"],
    "export": ["export", "fileexport", "cuiexport"],
    "undo": ["undo", "undo2"],
    "redo": ["redo", "redo2"],
    "settings": ["settings", "preferences", "tboutlinesettings"],
    "close": ["close", "x", "tboutlinex"],
    "minimize": ["minimize", "minimize2"],
    "maximize": ["maximize", "maximize2"],
    "panel-left": ["panelleft", "sidebartoggle", "toolbarbuttonsidebartoggle"],
    "panel-right": ["panelright", "panelrightopen", "panelrightclose"],
    "search": ["search", "find", "toolbarbuttonsearch"],
    "measure": ["measure"],
    "fit": ["fit", "fitpage", "fitwidth", "zoomext"],
    "fit-selection": ["fitselection", "fit_selection", "frameselection"],
    "zoom-in": ["zoomin", "zoom_in"],
    "zoom-out": ["zoomout", "zoom_out"],
    "pan": ["pan"],
    "cube": ["cube"],
    "extensions": ["extensions", "plugin", "puzzle"],
    "help": ["help", "circlehelp"],
    "back": ["back"],
    "check": ["check", "tboutlinecheck"],
    "grid": ["grid", "grid2x2", "layoutgrid"],
}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def candidates(value: str) -> list[str]:
    key = norm(value)
    return [semantic for semantic, aliases in ALIASES.items() if key in {norm(alias) for alias in aliases}]


def icon_records() -> list[dict]:
    source = json.loads((ROOT / "harmonization/asset-index.json").read_text())
    repos = {r["name"]: r for r in json.loads((ROOT / "harmonization/inventory.json").read_text())}
    concrete = []
    for record in source:
        if record["category"] != "ui-used":
            continue
        preview = unquote(record["file"])
        assert (DESIGN / preview).is_file(), preview
        reference = record["ui_references"][0]
        commit = repos[record["repo"]].get("commit")
        source_url = (
            repos[record["repo"]]["url"].rstrip("/") + "/blob/" + commit + "/"
            + quote(reference["source"]) + (f'#L{reference["line"]}' if reference["line"] else "")
        ) if commit else record["url"]
        concrete.append({
            "kind": "ui-asset", "repo": record["repo"], "name": Path(record["path"]).stem,
            "path": record["path"], "preview": preview,
            "evidence": record["evidence_type"], "references": record["ui_references"],
            "sha256": record["sha256"], "source_url": source_url,
        })
    libraries = json.loads((ROOT / "harmonization/library-icon-index.json").read_text())
    for record in libraries["icons"]:
        preview = "../harmonization/" + record["file"]
        assert (DESIGN / preview).is_file(), preview
        source = record["sources"][0]
        source_url = (
            repos[source["repo"]]["url"].rstrip("/") + "/blob/" + source["commit"] + "/"
            + quote(source["source"]) + f'#L{source["line"]}'
        )
        concrete.append({
            "kind": "code-import", "repo": ", ".join(sorted({s["repo"] for s in record["sources"]})),
            "name": record["name"], "path": f'{record["package"]}@{record["version"]}/{record["name"]}',
            "preview": preview, "evidence": "source-import", "references": record["sources"],
            "sha256": record["sha256"], "source_url": source_url,
        })
    decisions = json.loads((DESIGN / "icon-adoptions.json").read_text())["decisions"]
    adopted = {decision["legacy_asset"]: decision["shared_icon"] for decision in decisions}
    for record in concrete:
        if record["repo"] == "open-pointcloud-studio" and record["path"] in adopted:
            assert candidates(record["name"]) == [adopted[record["path"]]]
            record["adoption"] = "native-adopted"
    assert sum(r.get("adoption") == "native-adopted" for r in concrete) == len(decisions)
    return concrete


def thumb(record: dict) -> str:
    label = f'{record["repo"]}: {record["path"]}'
    adopted = record.get("adoption") == "native-adopted"
    return (
        f'<a class="candidate{" adopted" if adopted else ""}" data-search="{html.escape(label.lower(), quote=True)}" '
        f'href="{html.escape(record["source_url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
        f'<img src="{html.escape(record["preview"], quote=True)}" alt="">'
        f'<span><b>{html.escape(record["name"])}</b><small>{html.escape(record["repo"])}'
        f' · {html.escape(record["kind"])}{" · Rust" if adopted else ""}</small></span></a>'
    )


def main() -> None:
    canonical_names = {path.stem for path in (ROOT / "assets/icons").glob("*.svg")}
    assert canonical_names == {key.replace("-", "") for key in ALIASES}, "Canonical icon catalogue differs from semantic crosswalk"
    records = icon_records()
    assert len([r for r in records if r["kind"] == "ui-asset"]) == 565
    assert len([r for r in records if r["kind"] == "code-import"]) == 312
    grouped = defaultdict(list)
    unmatched = []
    for record in records:
        names = candidates(record["name"])
        if len(names) == 1:
            grouped[names[0]].append(record)
        else:
            unmatched.append(record)
    output = {
        "status": "name-candidate-only",
        "note": "UI assets have direct code or framework-bundle evidence; imported icons are a separate source-code category. A matching name does not approve semantics or artwork.",
        "source_counts": {"ui_assets": 565, "code_import_variants": 312},
        "adopted_count": len(json.loads((DESIGN / "icon-adoptions.json").read_text())["decisions"]),
        "native_chrome_decisions_count": len(json.loads((DESIGN / "icon-adoptions.json").read_text())["chrome_decisions"]),
        "canonical": [
            {"id": key, "aliases": aliases, "candidates": grouped[key]}
            for key, aliases in ALIASES.items()
        ],
        "unmatched": unmatched,
    }
    (DESIGN / "icon-semantic-crosswalk.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    )
    cards = []
    for key, aliases in ALIASES.items():
        matches = grouped[key]
        cards.append(
            f'<article class="concept" data-search="{html.escape((key + " " + " ".join(aliases)).lower(), quote=True)}">'
            f'<header><img src="../assets/icons/{html.escape(key.replace("-", ""))}.svg" alt="">'
            f'<h2>{html.escape(key)}</h2><span>{len(matches)} kandidaten</span></header>'
            f'<p>{html.escape(", ".join(aliases))}</p>'
            f'<div class="candidates">{"".join(thumb(r) for r in matches) or "<em>Geen naamkandidaat</em>"}</div></article>'
        )
    # Canonical filenames use panelleft/panelright, matching the enum assets.
    unmatched_by_repo = defaultdict(list)
    for record in unmatched:
        unmatched_by_repo[(record["kind"], record["repo"])].append(record)
    rest = []
    for (kind, repo), items in sorted(unmatched_by_repo.items()):
        rest.append(
            f'<details><summary>{html.escape(repo)} · {html.escape(kind)} · {len(items)}</summary>'
            f'<div class="candidates">{"".join(thumb(r) for r in items)}</div></details>'
        )
    counts = Counter(r["kind"] for r in records)
    page = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · Iconbetekenissen</title><style>
@font-face{{font-family:Inter;src:url("../assets/fonts/Inter-Regular.ttf")}}*{{box-sizing:border-box}}
body{{margin:0;background:#f2f3f5;color:#30343b;font:12px/1.4 Inter,"Segoe UI",sans-serif}}
.top{{position:sticky;top:0;z-index:2;background:#272b32;color:#fff;border-bottom:3px solid #d97706;padding:13px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.top b{{font-size:14px;letter-spacing:.04em}}.top input{{width:280px;max-width:100%;padding:7px 9px;border:1px solid #808994;border-radius:4px}}
.top span{{color:#c7ccd2}}main{{max-width:1500px;margin:auto;padding:20px}}.intro{{background:white;border-left:4px solid #d97706;padding:12px 16px;margin-bottom:18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}}.concept,details{{background:#fff;border:1px solid #d7dbe0;border-radius:5px;padding:12px}}
.concept header{{display:flex;align-items:center;gap:9px}}.concept header img{{width:22px;height:22px}}h2{{font-size:15px;margin:0;flex:1}}h1{{font-size:18px;margin:22px 0 10px}}
.concept header span{{color:#a65908;font-size:11px}}.concept p{{color:#6c737b;margin:5px 0 9px}}.candidates{{display:grid;grid-template-columns:repeat(auto-fill,minmax(135px,1fr));gap:5px;max-height:260px;overflow:auto}}
.candidate{{display:flex;align-items:center;gap:7px;min-width:0;padding:5px;background:#f6f7f8;border:1px solid #e4e6e9;border-radius:3px;color:inherit;text-decoration:none}}
.candidate:hover{{border-color:#d97706;background:#fff8ef}}
.candidate.adopted{{border-color:#d97706;background:#fff4e7}}
.candidate img{{width:24px;height:24px;object-fit:contain;flex:none}}.candidate span{{min-width:0;overflow:hidden}}.candidate b,.candidate small{{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.candidate small{{font-size:9px;color:#777e87}}details{{margin:8px 0}}summary{{cursor:pointer;font-weight:600}}details .candidates{{margin-top:9px;max-height:360px}}
.hidden{{display:none!important}}
</style></head><body><div class="top"><b>OPENAEC · ICONBETEKENISSEN</b><input id="search" placeholder="Zoek betekenis, bron of icoon…" aria-label="Zoek iconen"><span>{counts['ui-asset']} UI-bestanden · {counts['code-import']} code-importvarianten · {len(ALIASES)} gedeelde betekenissen</span></div>
<main><div class="intro">Naamovereenkomsten zijn <b>reviewkandidaten</b>. Tien Pointcloud-toolacties zijn na semantische beoordeling in de Rust-kern ingebouwd en oranje gemarkeerd. Daarnaast gebruikt de zichtbare Extensions-bestandspagina nu een eigen, nieuw getekend puzzelicoon in plaats van de 3D-kubus. De 565 UI-bestanden hebben broncode- of actieve knopbundel-evidence. De 312 bibliotheekvarianten komen uit broncode-imports en blijven apart; import alleen bewijst geen zichtbare knop. Vakinhoudelijke commando's zonder veilige generieke match staan onderaan.</div>
<h1>Gedeelde kern · {sum(map(len, grouped.values()))} naamkandidaten</h1><div class="grid">{''.join(cards)}</div>
<h1>Overige UI- en domeiniconen · {len(unmatched)}</h1>{''.join(rest)}
</main><script>
const search=document.getElementById('search');search.oninput=()=>{{const q=search.value.trim().toLowerCase();for(const c of document.querySelectorAll('.candidate'))c.classList.toggle('hidden',!c.dataset.search.includes(q));for(const c of document.querySelectorAll('.concept'))c.classList.toggle('hidden',q&&!c.dataset.search.includes(q)&&!c.querySelector('.candidate:not(.hidden)'));for(const d of document.querySelectorAll('details')){{const hide=q&&!d.querySelector('.candidate:not(.hidden)');d.classList.toggle('hidden',hide);if(q&&!hide)d.open=true;}}}};
</script></body></html>'''
    (DESIGN / "icon-semantic-crosswalk.html").write_text(page)
    print(f"{len(records)} evidence records: {sum(map(len, grouped.values()))} name candidates, {len(unmatched)} remaining")


if __name__ == "__main__":
    main()
