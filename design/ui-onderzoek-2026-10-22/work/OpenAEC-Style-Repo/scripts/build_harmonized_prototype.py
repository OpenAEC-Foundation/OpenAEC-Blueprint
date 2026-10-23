"""Inject the reviewed studio taxonomy into the shared shell design study.

Since 2026-10-16 the page uses the UI 0.4 design: colours come from
design/ontwerp-0.4/tokens-0.4.json (five themes) and the ribbon follows
variant B from design/ontwerp-0.4/04-componenten.md. The template keeps its
original --theme-* variables; they are filled from the 0.4 tokens here.
Ribbon and title bar icons come from Codex's B2 set where the meaning matches;
other commands keep their source or prototype icon.
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_tokens_04 import mix  # noqa: E402


def read(path):
    return (root / path).read_text(encoding="utf-8")


apps = json.loads(read("design/app-layouts.json"))
domain_icons = json.loads(read("design/domain-icon-drafts.json"))
template = read("design/harmonized-template.html")
tokens = json.loads(read("design/ontwerp-0.4/tokens-0.4.json"))
payload = json.dumps(apps, ensure_ascii=False).replace("</", "<\\/")
icons_payload = json.dumps(domain_icons, ensure_ascii=False).replace("</", "<\\/")

page = template.replace("/*APP_DATA*/", payload).replace("/*DOMAIN_ICON_DATA*/", icons_payload)
for mark, name in [("CALC", "calc"), ("GEOTECH", "geotech"), ("HEATLOSS", "heatloss"), ("CALCULATIONS", "calculations"),
                   ("REPORTS", "reports"), ("VALIDATOR", "validator"), ("PILE", "pile"), ("FRAME", "frame"),
                   ("2D_EXTENSION", "2d-extension"), ("CAD", "cad"), ("POINTCLOUD", "pointcloud"), ("PDF", "pdf")]:
    page = page.replace(f"/*{mark}_RIBBON*/", read(f"design/{name}-ribbon.js"))


# ---------- UI 0.4: theme variables from the tokens ----------
def theme_block(tid, th):
    c = th["color"]
    hc = th.get("high-contrast", False)
    v = {
        "--theme-bg": c["frame"], "--theme-bg-lighter": c["panel"], "--theme-surface": c["panel"],
        "--theme-content-bg": c["workspace"], "--theme-docbar-bg": c["docbar"],
        "--theme-text": c["text"], "--theme-text-secondary": c["text-secondary"],
        "--theme-border": c["border"], "--theme-border-subtle": c["border"],
        "--theme-accent": c["accent"], "--theme-accent-soft": c["panel"] if hc else c["selected"],
        "--theme-accent-text": c["text-on-accent"],
        "--theme-file-tab-bg": c["accent"], "--theme-file-tab-text": c["text-on-accent"],
        "--theme-hover": c["hover"],
        "--theme-ribbon-btn-active-bg": c["panel"] if hc else c["selected"],
        "--theme-ribbon-btn-active-border": c["accent"] if hc else mix(c["accent"], 0.35, c["panel"]),
        "--theme-ribbon-btn-active-text": c["accent-text"],
        "--theme-ribbon-group-label": c["text-secondary"], "--theme-ribbon-group-separator": c["border"],
        "--theme-status-bg": c["statusbar"], "--theme-status-border": c["border"], "--theme-status-text": c["statusbar-text"],
        "--ws-text": c["workspace-text"], "--sel-bar": c["selected-bar"], "--focus": c["focus"],
        "--icon-filter": "none" if th["kind"] == "light" else "invert(1)",
    }
    return f'body[data-theme="{tid}"]{{' + ";".join(f"{k}:{val}" for k, val in v.items()) + "}"


THEME_CSS = "".join(theme_block(tid, th) for tid, th in tokens["themes"].items())

SHAPE_CSS = """
@font-face{font-family:"JetBrains Mono";src:url("../assets/fonts/JetBrainsMono-Regular.ttf")}
.quick img,.cmd img{filter:var(--icon-filter)!important}
.work{color:var(--ws-text)!important}
.work .settings p,.work .backmain p,.work .empty,.work .empty h2{color:inherit!important}
.tabs{align-items:stretch;padding:0 8px;background:var(--theme-bg-lighter)}
.tabs button{height:auto;border-radius:0;color:var(--theme-text-secondary);font-weight:500;border-bottom:2px solid transparent}
.tabs button.active{background:transparent;color:var(--theme-text);font-weight:600;border-bottom-color:var(--theme-accent)}
.tabs button.file{align-self:center;height:22px;margin-right:8px;border-radius:6px;border-bottom:0;background:var(--theme-file-tab-bg);color:var(--theme-file-tab-text);font-weight:600}
.group{position:relative;border-right:0}
.group:after{content:"";position:absolute;right:0;top:10px;bottom:10px;width:1px;background:var(--theme-ribbon-group-separator)}
.cmd{border-radius:6px}
.cmd:hover{background:var(--theme-hover);border-color:transparent;color:var(--theme-text)}
.cmd.selected{background:var(--theme-ribbon-btn-active-bg);border-color:var(--theme-ribbon-btn-active-border);color:var(--theme-text)}
.groupname{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.08em}
.paneltitle{font-family:"JetBrains Mono",monospace;font-weight:400;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--theme-text-secondary)}
.title{color:var(--theme-ribbon-btn-active-text)}
.document{border:0;border-radius:6px 6px 0 0;background:transparent;color:var(--theme-text-secondary);font-size:12px;margin-right:4px}
.document.active{background:var(--theme-content-bg);color:var(--ws-text);font-weight:600;border-top:0}
.treeitem{border-radius:3px}
.treeitem.sel,body[data-chrome="sidebar"] .treeitem.sel{background:var(--theme-accent-soft);color:var(--theme-text);font-weight:600;border:0;box-shadow:inset 3px 0 0 var(--sel-bar)}
.status{border-top:1px solid var(--theme-status-border)}
.workcard{border-radius:10px}
body[data-chrome="topnav"] .tabs{border-bottom:1px solid var(--theme-border)}
body[data-theme^="high-contrast"] .treeitem.sel{box-shadow:inset 0 0 0 2px var(--sel-bar)}
"""

THEME_OPTIONS = "".join(f'<option value="{tid}">{th["name"]}</option>' for tid, th in tokens["themes"].items())
OLD_OPTIONS = ('<option value="light">Blueprint Light</option><option value="forge">Deep Forge</option>'
               '<option value="openaec">Night Build</option><option value="blueprint">Blueprint</option>'
               '<option value="contrast">Contrast</option>')
assert OLD_OPTIONS in page, "theme options not found in template"
page = page.replace(OLD_OPTIONS, THEME_OPTIONS, 1)
assert "</style>" in page
page = page.replace("</style>", THEME_CSS + SHAPE_CSS + "</style>", 1)

# ---------- UI 0.4: B2 icons by Codex where the meaning is the same ----------
# Per app only commands whose source call Codex reviewed for that function
# (harmonization/icon-set-b2/function-plan.json); no automatic approval of
# other calls with the same label. Generic shell commands use a fixed list.
B2_DIR = root / "design/icon-set-b2/svg"
APP_NAMES = {"pdf": "PDF", "pointcloud": "Pointcloud", "planner": "Planner", "calc": "Calc",
             "geotech": "Geotechniek", "heatloss": "Heatloss", "energy": "Energy",
             "calculations": "Calculations", "reports": "Reports", "frame": "Frame", "field": "Field",
             "validator": "BIM Validator", "speech": "Speech", "composer": "Workspace Composer", "pile": "Pile Plan"}
GENERIC = {"Nieuw": "file.new", "Openen": "file.open", "Opslaan": "file.save", "Importeren": "file.import",
           "Exporteren": "file.export", "Zoeken": "view.search", "Passend": "view.fit",
           "Eigenschappen": "panel.right", "Instellingen": "ui.settings", "Help": "ui.help",
           "Ongedaan": "edit.undo", "Opnieuw": "edit.redo"}
# Same label, different command elsewhere in the same ribbon.
EXCLUDE = {("pdf", "Samenvoegen"), ("pdf", "Verwijderen"), ("calc", "Verwijder")}
QUICK = {"new": "file.new", "open": "file.open", "save": "file.save", "undo": "edit.undo", "settings": "ui.settings"}


def has_b2(fid):
    return (B2_DIR / "16" / f"{fid}.svg").exists() and (B2_DIR / "24" / f"{fid}.svg").exists()


plan = json.loads(read("harmonization/icon-set-b2/function-plan.json"))
records = {r["id"]: r for r in json.loads(read("harmonization/function-icon-catalog.json"))["records"]}
reviewed, rejected = {}, set()
for a in plan["record_assessments"]:
    r = records[a["record_id"]]
    key = (r["app"], r["label"])
    if a["assessment"] == "niet samenvoegen":
        rejected.add(key)
    elif a["canonical_function"] and a["assessment"] in ("bronvoorbeeld beoordeeld", "bestaand B2-ontwerp hergebruiken"):
        reviewed.setdefault(key, set()).add(a["canonical_function"])

b2_map = {"*": {k: v for k, v in GENERIC.items() if has_b2(v)}}
for app_id, name in APP_NAMES.items():
    m = {}
    ribbon = root / f"design/{app_id}-ribbon.js"
    # Commands drawn with a source icon file are also reviewed under that file name.
    src = ribbon.read_text(encoding="utf-8") if ribbon.exists() else ""
    files = dict(re.findall(r"'([^']+)':\s*'([A-Z][A-Za-z0-9]+)'", src))
    # Only commands that this page actually draws on the ribbon.
    shown = {a or b for a, b in re.findall(r"'([^']+)'|\"([^\"]+)\"", src)}
    labels = ({lab for (app, lab) in reviewed if app == name} & shown) | set(GENERIC) | set(files)
    for lab in labels:
        funcs = reviewed.get((name, lab)) or reviewed.get((name, files.get(lab, "")))
        if (app_id, lab) in EXCLUDE or (name, lab) in rejected or (funcs and len(funcs) > 1):
            m[lab] = None
        elif funcs and has_b2(next(iter(funcs))):
            m[lab] = next(iter(funcs))
    b2_map[app_id] = {k: v for k, v in m.items() if not (v is None and k not in GENERIC)}

used_cmd = {v for m in b2_map.values() for v in m.values() if v}
used_quick = {v for v in QUICK.values() if has_b2(v)}
used = used_cmd | used_quick
symbols = []
for master, ids in (("24", used_cmd), ("16", used_quick)):
    for fid in sorted(ids):
        svg = (B2_DIR / master / f"{fid}.svg").read_text(encoding="utf-8")
        inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
        symbols.append(f'<symbol id="b2-{master}-{fid}" viewBox="0 0 {master} {master}">{inner}</symbol>')
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(symbols) + "</svg>"

OLD_CMD = "const cmdIcon=c=>domainIndex[c]?"
OLD_END = "icon(iconMap[c]||'grid');"
assert page.count(OLD_CMD) == 1 and page.count(OLD_END) == 1, "cmdIcon not found in template"
b2_js = ("const b2Map=" + json.dumps(b2_map, ensure_ascii=False) + ";"
         "const b2Cmd=c=>{const m=b2Map[apps[+E('studio').value].id]||{};const id=c in m?m[c]:b2Map['*'][c];"
         "return id?'<svg class=\"b2i\" aria-hidden=\"true\"><use href=\"#b2-24-'+id+'\"/></svg>':''};")
page = page.replace(OLD_CMD, b2_js + "const cmdIcon=c=>b2Cmd(c)||(domainIndex[c]?", 1).replace(OLD_END, "icon(iconMap[c]||'grid'));", 1)
for old, fid in QUICK.items():
    tag = f'<img src="../assets/icons/{old}.svg" alt="">'
    if has_b2(fid) and tag in page:
        page = page.replace(tag, f'<svg class="b2i" aria-hidden="true"><use href="#b2-16-{fid}"/></svg>')
page = page.replace("</style>", ".b2i{--icon-accent:var(--theme-accent);flex:none}.quick .b2i{width:16px;height:16px}"
                    ".cmd .b2i{width:22px;height:22px}</style>", 1)
page = page.replace("</body>", SPRITE + "</body>", 1) if "</body>" in page else page + SPRITE

(root / "design/harmonized.html").write_text(page, encoding="utf-8")
n_cmd = sum(1 for k, m in b2_map.items() if k != "*" for v in m.values() if v)
print(f"Generated shared shell for {len(apps)} tool interfaces with UI 0.4 tokens ({len(tokens['themes'])} themes); "
      f"{len(used)} B2-iconen van Codex: {n_cmd} beoordeelde appknoppen en {len(b2_map['*'])} algemene knoppen")
