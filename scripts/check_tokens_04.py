#!/usr/bin/env python3
"""Validate the UI 0.4 design tokens: structure and WCAG 2.2 contrast per theme.

Usage: python scripts/check_tokens_04.py
Exits with status 1 when a theme is incomplete or a colour pair misses its minimum.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "design/ontwerp-0.4/tokens-0.4.json"

TEXT = "text"   # normal text: 4.5:1, high contrast 7:1
UI = "ui"       # component boundaries and focus: 3:1

# (label, foreground, [backgrounds], kind)
PAIRS = [
    ("Tekst", "text", ["frame", "panel", "raised", "selected", "field"], TEXT),
    ("Secundaire tekst", "text-secondary", ["frame", "panel", "raised", "field"], TEXT),
    ("Gedempte tekst", "text-muted", ["frame", "panel", "raised", "field"], TEXT),
    ("Accenttekst", "accent-text", ["panel", "raised", "selected"], TEXT),
    ("Tekst op primaire knop", "text-on-accent", ["accent"], TEXT),
    ("Tekst op knop bij hover", "text-on-accent", ["accent-hover"], TEXT),
    ("Tekst op knop bij ingedrukt", "text-on-accent", ["accent-pressed"], TEXT),
    ("Tekst op hover-vlak", "text", ["hover", "pressed"], TEXT),
    ("Statusbalk", "statusbar-text", ["statusbar"], TEXT),
    ("Werkruimte", "workspace-text", ["workspace"], TEXT),
    ("Fout", "error", ["panel", "raised", "@tint"], TEXT),
    ("Gelukt", "success", ["panel", "raised", "@tint"], TEXT),
    ("Waarschuwing", "warning", ["panel", "raised", "@tint"], TEXT),
    ("Info", "info", ["panel", "raised", "@tint"], TEXT),
    ("Rand van invoerveld", "border-strong", ["panel", "frame", "raised", "field"], UI),
    ("Focusring", "focus", ["panel", "frame", "raised"], UI),
    ("Selectiestreep", "selected-bar", ["selected", "panel"], UI),
]

HEX = re.compile(r"^#[0-9A-F]{6}$")


def rgb(value):
    return [int(value[i:i + 2], 16) for i in (1, 3, 5)]


def mix(fg, alpha, bg):
    a, b = rgb(fg), rgb(bg)
    return "#" + "".join(f"{round(a[i] * alpha + b[i] * (1 - alpha)):02X}" for i in range(3))


def luminance(value):
    out = []
    for v in rgb(value):
        v /= 255
        out.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def minimum(kind, theme):
    if kind == UI:
        return 3.0
    return 7.0 if theme.get("high-contrast") else 4.5


def evaluate(tokens):
    """Return (problems, rows). Rows: theme id, label, fg, bg name, bg hex, ratio, minimum."""
    problems, rows = [], []
    themes = tokens["themes"]
    keys = None
    for tid, theme in themes.items():
        colors = theme["color"]
        if keys is None:
            keys = set(colors)
        elif set(colors) != keys:
            problems.append(f"{tid}: andere kleurvelden dan het eerste thema: {sorted(set(colors) ^ keys)}")
        for k, v in colors.items():
            if not HEX.match(v):
                problems.append(f"{tid}: {k} is geen hexkleur zonder doorzichtigheid: {v}")
    if problems:
        return problems, rows
    for tid, theme in themes.items():
        c = theme["color"]
        for label, fg, bgs, kind in PAIRS:
            need = minimum(kind, theme)
            for bg in bgs:
                if bg == "@tint":
                    if c[f"{fg}-tint"] == c["panel"]:
                        continue
                    bg_hex, bg_name = c[f"{fg}-tint"], f"{fg}-tint"
                else:
                    bg_hex, bg_name = c[bg], bg
                r = contrast(c[fg], bg_hex)
                rows.append((tid, label, fg, bg_name, bg_hex, r, need))
                if r < need:
                    problems.append(f"{tid}: {label} ({fg} {c[fg]} op {bg_name} {bg_hex}) is {r:.2f}, minimaal {need}")
    setting = tokens.get("workspace-setting", {}).get("options", {})
    light_accent = themes["light"]["color"]["accent-text"]
    dark_accent = themes["dark"]["color"]["accent-text"]
    for tid, theme in themes.items():
        if theme.get("high-contrast"):
            continue
        for opt, values in setting.items():
            if "workspace" not in values:
                continue
            ws, wt = values["workspace"], values["workspace-text"]
            ws_light = luminance(ws) > 0.5
            same_kind = ws_light == (theme["kind"] == "light")
            accent = theme["color"]["accent-text"] if same_kind else (light_accent if ws_light else dark_accent)
            for label, fg, need in (("Werkruimte " + opt + ": tekst", wt, 4.5), ("Werkruimte " + opt + ": accent", accent, 3.0)):
                r = contrast(fg, ws)
                rows.append((tid, label, fg, "workspace " + opt, ws, r, need))
                if r < need:
                    problems.append(f"{tid}: {label} ({fg} op {ws}) is {r:.2f}, minimaal {need}")
    for opt, values in tokens.get("statusbar-setting", {}).get("options", {}).items():
        if "statusbar" not in values:
            continue
        r = contrast(values["statusbar-text"], values["statusbar"])
        rows.append(("alle", "Statusbalk " + opt, values["statusbar-text"], "statusbar " + opt, values["statusbar"], r, 4.5))
        if r < 4.5:
            problems.append(f"Statusbalk {opt}: {r:.2f}, minimaal 4.5")
    return problems, rows


def main():
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    problems, rows = evaluate(tokens)
    for p in problems:
        print("FOUT  " + p)
    if problems:
        sys.exit(1)
    print(f"Tokens 0.4: {len(tokens['themes'])} thema's, {len(rows)} kleurparen, alle paren halen hun minimum")


if __name__ == "__main__":
    main()
