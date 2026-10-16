"""Inject the reviewed studio taxonomy into the shared shell design study.

Since 2026-10-16 the page uses the UI 0.4 design: colours come from
design/ontwerp-0.4/tokens-0.4.json (five themes) and the ribbon follows
variant B from design/ontwerp-0.4/04-componenten.md. The template keeps its
original --theme-* variables; they are filled from the 0.4 tokens here.
"""
import json
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

(root / "design/harmonized.html").write_text(page, encoding="utf-8")
print(f"Generated shared shell for {len(apps)} tool interfaces with UI 0.4 tokens ({len(tokens['themes'])} themes)")
