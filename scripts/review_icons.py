"""Icon lookup for the UI 0.4 review pages.

Prefers the B2 icon set by Codex (design/icon-set-b2/svg/<16|24>/<function>.svg)
and falls back to the prototype icons in crates/openaec-ui/assets/icons.
Pass a B2 function id such as "file.save", or an old icon name. Old names are
only mapped to B2 where the meaning is the same everywhere.

B2 icons are emitted once as <symbol> elements via sprite() and referenced with
<use>, because their paths are large. Generators put SPRITE_MARK in the page and
replace it with sprite() after all icons are rendered.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B2 = ROOT / "design/icon-set-b2/svg"
OLD = ROOT / "crates/openaec-ui/assets/icons"
SPRITE_MARK = "<!--B2-SPRITE-->"

ALIAS = {
    "back": "nav.back",
    "close": "window.close",
    "duplicate": "edit.duplicate",
    "export": "file.export",
    "import": "file.import",
    "new": "file.new",
    "open": "file.open",
    "print": "file.print",
    "save": "file.save",
    "saveas": "file.save-as",
    "undo": "edit.undo",
    "redo": "edit.redo",
    "search": "view.search",
    "settings": "ui.settings",
    "help": "ui.help",
    "panelleft": "panel.left",
    "panelright": "panel.right",
    "zoomin": "view.zoom-in",
}
REVERSE = {v: k for k, v in ALIAS.items()}
USED = {"b2": set(), "old": set()}
_SYMBOLS = {}


def icon(name, size=16):
    """Return SVG markup for an icon at the given pixel size."""
    b2_id = name if "." in name else ALIAS.get(name)
    if b2_id:
        master = "16" if size <= 18 else "24"
        path = B2 / master / f"{b2_id}.svg"
        if path.exists():
            sym = f"b2-{master}-{b2_id}"
            if sym not in _SYMBOLS:
                svg = path.read_text(encoding="utf-8")
                inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
                _SYMBOLS[sym] = f'<symbol id="{sym}" viewBox="0 0 {master} {master}">{inner}</symbol>'
            USED["b2"].add(b2_id)
            return f'<svg width="{size}" height="{size}" aria-hidden="true" class="b2"><use href="#{sym}"/></svg>'
    old_name = REVERSE.get(name, name)
    svg = (OLD / f"{old_name}.svg").read_text(encoding="utf-8")
    svg = svg.replace('stroke="#000"', 'stroke="currentColor"').replace('fill="#000"', 'fill="currentColor"')
    USED["old"].add(old_name)
    return re.sub(r"<svg ", f'<svg width="{size}" height="{size}" aria-hidden="true" ', svg, count=1)


def sprite():
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(_SYMBOLS.values()) + "</svg>"


def usage():
    return f"{len(USED['b2'])} B2-iconen van Codex, {len(USED['old'])} tijdelijke iconen uit het prototype ({', '.join(sorted(USED['old']))})"
