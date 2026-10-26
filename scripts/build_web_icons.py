#!/usr/bin/env python3
"""B2 icons for web apps: one SVG sprite per app (issue #11).

Source: the lossless B2 export (design/icon-set-b2/library-lossless) and the
apps per icon in design/icon-set-b2/manifest.json, the same split as the
features of the `openaec-icons` crate. Writes:
  web/icons/<app>.svg      a sprite with <symbol id="i16-<id>"> and "i24-<id>"
  web/icons/manifest.json  revision, icons per app, sizes and SHA-256

The export draws curves as many short straight pieces with six decimals, about
30 kB per icon. For the web the path data is made compact: points that lie
within 0.01 px of the line through their neighbours are left out and
coordinates keep two decimals, so no point moves more than 0.02 px. That keeps
8 % of the size. Checked in Chrome against an exact reference (the icon drawn at
256 px and averaged down to 16 px): the compact icons are as accurate as the
export, 3.43 against 3.40 average error on 255 over 150 icons; both differ from
the reference by up to 84 on single edge pixels, which is the browser's own
anti-aliasing. Colours stay as in the export: `currentColor` and
`var(--icon-accent, currentColor)`.

Use: <svg class="oa-icon"><use href="icons/pdf.svg#i16-file.save"/></svg>
Run with --check to verify without writing.
"""

import functools
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_icon_crate import B2, EXPORT, FEATURES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web/icons"
# Largest distance (in pixels of the icon's own size) a left-out point may lie
# from the simplified line.
TOLERANCE = 0.01
# The icons of the standard application (src/bin/blueprint.rs and the Tauri
# template in style-book/project-templates/Tauri+React), as one extra sprite
# "standard" next to the app sprites.
STANDARD = [
    "data.chart", "data.table", "draw.arrow", "draw.circle", "draw.freehand", "draw.image", "draw.line", "draw.rectangle",
    "edit.copy", "edit.cut", "edit.paste", "edit.redo", "edit.undo", "extension.install-file", "extensions.manage",
    "file.new", "file.open", "file.print", "file.save", "format.align-center", "format.align-left", "format.align-right",
    "format.bold", "format.italic", "format.underline", "ifc.export", "ifc.import", "ifc.validate", "link.open-external",
    "measure.distance", "mesh.closed", "panel.left", "panel.model-tree", "panel.right", "project.folder",
    "project.properties", "report.cover", "report.generate", "report.template", "section.box", "software.catalog",
    "status.info", "status.success", "ui.help", "ui.settings", "view.fit", "view.orbit", "view.report-preview", "view.reset-camera",
    "window.close", "window.maximize", "window.minimize", "window.restore",
]


def subpaths(d):
    """Splits path data of absolute M, L and Z commands into point lists."""
    found, current = [], None
    for command, args in re.findall(r"([MLZ])([^MLZ]*)", d):
        numbers = [float(x) for x in args.split()]
        points = list(zip(numbers[::2], numbers[1::2]))
        if command == "M":
            current = {"points": points, "closed": False}
            found.append(current)
        elif command == "L":
            current["points"].extend(points)
        else:
            current["closed"] = True
    return found


def distance(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    return ((x - x1 - t * dx) ** 2 + (y - y1 - t * dy) ** 2) ** 0.5


def simplify(points, tolerance):
    """Ramer-Douglas-Peucker: keeps the points that matter for the shape."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        best, index = 0.0, None
        for i in range(a + 1, b):
            d = distance(points[i], points[a], points[b])
            if d > best:
                best, index = d, i
        if index is not None and best > tolerance:
            keep[index] = True
            stack += [(a, index), (index, b)]
    return [p for p, k in zip(points, keep) if k]


def number(v):
    text = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def compact(d):
    if re.search(r"[^MLZ0-9.\s-]", d):
        raise ValueError("path data with commands other than M, L and Z")
    parts = []
    for sub in subpaths(d):
        points = simplify(sub["points"], TOLERANCE)
        pairs = [f"{number(x)} {number(y)}" for x, y in points]
        parts.append("M" + pairs[0] + ("L" + " ".join(pairs[1:]) if len(pairs) > 1 else "") + ("Z" if sub["closed"] else ""))
    return "".join(parts)


@functools.lru_cache(maxsize=None)
def symbol(icon_id, size, svgz_path, original_sha256):
    """One icon as a <symbol>, read from the export and made compact."""
    data = gzip.decompress((EXPORT / svgz_path).read_bytes())
    assert hashlib.sha256(data).hexdigest() == original_sha256, f"{svgz_path} differs from the export manifest"
    svg = data.decode("utf-8").strip()
    head, inner = re.match(r"<svg([^>]*)>(.*)</svg>$", svg, re.S).groups()
    box = re.search(r'viewBox="([^"]+)"', head).group(1)
    rest = re.sub(r'\s(xmlns|width|height|viewBox)="[^"]*"', "", head)
    inner = re.sub(r' d="([^"]+)"', lambda m: f' d="{compact(m.group(1))}"', inner)
    return f'<symbol id="i{size}-{icon_id}" viewBox="{box}"><g{rest}>{inner}</g></symbol>'


def icons():
    """(id, label, apps, assets) for every icon of the export."""
    design = {i["id"]: i for i in json.loads((B2 / "manifest.json").read_text(encoding="utf-8"))["icons"]}
    export = json.loads((EXPORT / "manifest.json").read_text(encoding="utf-8"))
    for icon in sorted(export["icons"], key=lambda i: i["id"]):
        meta = design.get(icon["id"], {})
        apps = sorted({FEATURES[a] for a in meta.get("candidate_apps") or [] if a in FEATURES})
        yield icon["id"], meta.get("label", ""), apps, icon["assets"]


def build():
    export = json.loads((EXPORT / "manifest.json").read_text(encoding="utf-8"))
    revision = export.get("source_revision")
    per_app = {}
    for icon_id, label, apps, assets in icons():
        for app in apps + (["standard"] if icon_id in STANDARD else []):
            per_app.setdefault(app, []).append((icon_id, label, assets))
    missing = sorted(set(STANDARD) - {icon_id for icon_id, _, _ in per_app.get("standard", [])})
    assert not missing, f"STANDARD names icons that are not in the export: {missing}"
    writes, summary = {}, {}
    for app, entries in sorted(per_app.items()):
        symbols = [symbol(icon_id, size, assets[size]["path"], assets[size]["original_sha256"]) for icon_id, _, assets in entries for size in sorted(assets)]
        text = (
            f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
            f"<!-- OpenAEC B2 icons for {app}, revision {revision}: {len(entries)} icons in 16 and 24 px. "
            f"Generated by scripts/build_web_icons.py from design/icon-set-b2/library-lossless; do not edit. -->\n"
            + "\n".join(symbols)
            + "\n</svg>\n"
        )
        data = text.encode("utf-8")
        writes[OUT / f"{app}.svg"] = data
        summary[app] = {
            "file": f"{app}.svg",
            "icons": len(entries),
            "bytes": len(data),
            "gzip_bytes": len(gzip.compress(data, mtime=0)),
            "sha256": hashlib.sha256(data).hexdigest(),
            "ids": [icon_id for icon_id, _, _ in entries],
        }
    manifest = {
        "about": "B2-iconen voor webapps, één sprite per app (issue #11). Gemaakt door scripts/build_web_icons.py; niet met de hand aanpassen.",
        "revision": revision,
        "tolerance_px": TOLERANCE,
        "use": '<svg class="oa-icon"><use href="icons/<app>.svg#i16-<id>"/></svg>',
        "apps": summary,
    }
    writes[OUT / "manifest.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return writes, summary


def main():
    check = "--check" in sys.argv[1:]
    writes, summary = build()
    stale = [p for p, data in writes.items() if not p.exists() or p.read_bytes() != data]
    extra = [p for p in OUT.glob("*") if p not in writes] if OUT.exists() else []
    total = sum(s["bytes"] for s in summary.values()) // 1024
    if check:
        if stale or extra:
            print(f"Webiconen verouderd, draai scripts/build_web_icons.py: {len(stale) + len(extra)} bestanden, bijvoorbeeld {(stale + extra)[0].relative_to(ROOT).as_posix()}")
            return 1
        print(f"Webiconen actueel: {len(summary)} apps, {total} kB")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for path in stale:
        path.write_bytes(writes[path])
    for path in extra:
        path.unlink()
    print(f"Webiconen: {len(summary)} apps, {total} kB, {len(stale)} bestanden bijgewerkt, {len(extra)} verwijderd")
    for app, s in summary.items():
        print(f"  {app}: {s['icons']} iconen, {s['bytes'] // 1024} kB, {s['gzip_bytes'] // 1024} kB gzip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
