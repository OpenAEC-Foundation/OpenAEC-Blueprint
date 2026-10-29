"""Review of B2 revision 107: the 16 px masters on the pixel grid (issue #35).

Compares every 16 px master of revision 106 (review/raster-before/16) with the
current one (svg/16) at 100, 125 and 150 %, next to the 24 px master. The
sharpness is measured again from the exported contours, independently of the
generator: the share of drawn pixels that is at least 75 % covered.

Writes design/icon-set-b2/raster-review-107.html and raster-review-107.json.
Runtime: shapely in harmonization/sources/b2-runtime, as for build_icon_set_b2.py.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harmonization/sources/b2-runtime"))
import numpy  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

B2 = ROOT / "design/icon-set-b2"
BEFORE = B2 / "review/raster-before/16"
CELLS = shapely.box(*(a.ravel() for a in numpy.meshgrid(range(16), range(16))), *(a.ravel() + 1 for a in numpy.meshgrid(range(16), range(16))))


def contours(svg):
    """Both colour layers of an exported master as one shape (even-odd rings)."""
    shape = Polygon()
    for d in re.findall(r' d="([^"]*)"', svg):
        layer = Polygon()
        for ring in re.findall(r"M([^M]+?)Z", d):
            layer = layer.symmetric_difference(Polygon([tuple(map(float, p.split())) for p in ring.split("L")]))
        shape = unary_union([shape, layer])
    return shape


def sharpness(svg):
    cover = shapely.area(shapely.intersection(contours(svg), CELLS))
    ink = int((cover > 0.1).sum())
    return round(float((cover >= 0.75).sum()) / ink, 4) if ink else 0.0


def main():
    manifest = json.loads((B2 / "manifest.json").read_text(encoding="utf-8"))
    rows = []
    for icon in manifest["icons"]:
        key = icon["id"]
        before = (BEFORE / f"{key}.svg").read_text(encoding="utf-8")
        after = (B2 / icon["assets"]["16"]["path"]).read_text(encoding="utf-8")
        rows.append({"id": key, "label": icon["label"], "group": icon["group"], "before": sharpness(before), "after": sharpness(after)})
    rows.sort(key=lambda r: r["after"] - r["before"])
    mean = lambda k: round(sum(r[k] for r in rows) / len(rows) * 100, 1)
    summary = {
        "revision": manifest["revision"],
        "icons": len(rows),
        "sharpness_before_percent": mean("before"),
        "sharpness_after_percent": mean("after"),
        "sharper": sum(r["after"] > r["before"] + 0.005 for r in rows),
        "less_sharp": sum(r["after"] < r["before"] - 0.005 for r in rows),
        "rows": rows,
    }
    (B2 / "raster-review-107.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="")

    def cell(path):
        return "".join(f'<img src="{path}" width="16" height="16" class="z{z}" alt="">' for z in ("1", "125", "15"))

    body = "".join(
        f'<tr data-q="{html.escape((r["id"] + " " + r["label"] + " " + r["group"]).lower())}">'
        f'<td class="id"><code>{r["id"]}</code><br><span>{html.escape(r["label"])}</span></td>'
        f'<td>{cell("review/raster-before/16/" + r["id"] + ".svg")}<div class="n">{round(r["before"] * 100)} %</div></td>'
        f'<td>{cell("svg/16/" + r["id"] + ".svg")}<div class="n">{round(r["after"] * 100)} %</div></td>'
        f'<td><img src="svg/24/{r["id"]}.svg" width="24" height="24" alt=""></td>'
        f'<td class="d {"up" if r["after"] >= r["before"] else "down"}">{round((r["after"] - r["before"]) * 100):+d}</td></tr>'
        for r in rows
    )
    page = f"""<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>B2 revisie 107: 16 px op het raster</title>
<style>
body{{font:13px Inter,system-ui,sans-serif;margin:24px;color:#2a2a32;background:#fff}}
body.dark{{color:#edebe8;background:#2a2a32}} body.dark img{{filter:invert(1)}}
h1{{font-size:20px;margin:0 0 4px}} p{{max-width:820px;line-height:1.5}}
table{{border-collapse:collapse;margin-top:12px}} th,td{{padding:6px 12px;border-bottom:1px solid #8884;text-align:center;vertical-align:middle}}
th{{position:sticky;top:0;background:inherit}} .id{{text-align:left}} .id span{{color:#888;font-size:12px}}
img{{margin:0 6px;vertical-align:middle}} .z125{{zoom:1.25}} .z15{{zoom:1.5}}
.n{{font:12px monospace;color:#888;margin-top:4px}} .d{{font:12px monospace}} .up{{color:#166534}} .down{{color:#b91c1c}}
body.dark .up{{color:#4ade80}} body.dark .down{{color:#f87171}}
.bar{{display:flex;gap:16px;align-items:center;flex-wrap:wrap}} input{{font:inherit;padding:4px 8px}}
</style>
<h1>B2 revisie 107: iconen op 16 px op het pixelraster</h1>
<p>Issue #35. Tot en met revisie 106 was het 16 px-ontwerp het 24 px-ontwerp maal ⅔, met lijnen van 1,25 px; driekwart van de coördinaten viel op derden van een pixel. Sinds revisie 107 zijn de lijnen op 16 px 1 px breed met de middellijn op halve pixels, zodat de randen op hele pixels vallen. Per icoon kiest de generator de scherpste variant die de vorm behoudt: alles op het raster, alleen rechte lijnen op het raster, of de lijnen op hun plek. Het 24 px-ontwerp is niet veranderd.</p>
<p><b>Scherpte</b> (aandeel getekende pixels dat voor minstens 75 % bedekt is, gemeten uit de geëxporteerde contouren): gemiddeld <b>{summary["sharpness_before_percent"]} %</b> in revisie 106 en <b>{summary["sharpness_after_percent"]} %</b> in revisie 107. {summary["sharper"]} iconen worden scherper, {summary["less_sharp"]} iets minder scherp; die staan bovenaan.</p>
<div class="bar"><input id="q" type="search" placeholder="Zoek icoon, naam of groep…" aria-label="Zoek icoon"><label><input type="checkbox" id="dark"> Donker</label><span>Per kolom: 100 %, 125 % en 150 %.</span></div>
<table><thead><tr><th class="id">Icoon</th><th>Revisie 106</th><th>Revisie 107</th><th>24 px</th><th>Verschil</th></tr></thead><tbody>{body}</tbody></table>
<script>
const q=document.getElementById('q');q.oninput=()=>{{const v=q.value.toLowerCase();for(const r of document.querySelectorAll('tbody tr'))r.hidden=!r.dataset.q.includes(v)}};
document.getElementById('dark').onchange=e=>document.body.classList.toggle('dark',e.target.checked);
</script></html>
"""
    (B2 / "raster-review-107.html").write_text(page, encoding="utf-8", newline="")
    print(f"Revisie {summary['revision']}: scherpte {summary['sharpness_before_percent']} % -> {summary['sharpness_after_percent']} %, "
          f"{summary['sharper']} scherper, {summary['less_sharp']} minder scherp, {len(rows)} iconen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
