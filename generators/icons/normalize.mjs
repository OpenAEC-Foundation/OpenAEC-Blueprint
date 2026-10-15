const SVG_NS = 'xmlns="http://www.w3.org/2000/svg"';
const COLOR_ATTR = /\b(fill|stroke|stop-color|color)\s*=\s*"([^"]*)"/gi;
const STYLE_ATTR = /\bstyle\s*=\s*"([^"]*)"/gi;
const STYLE_COLOR = /(fill|stroke|stop-color|color)\s*:\s*([^;"]+)/gi;
const FORBIDDEN = /<script\b|\son[a-z]+\s*=|(?:xlink:)?href\s*=\s*"(?!#)/i;
const NOT_A_COLOR = new Set(["none", "currentcolor", "transparent", "inherit"]);

export function normalizeColor(c) {
  const v = c.trim().toLowerCase();
  if (/^#[0-9a-f]{3}$/.test(v)) return "#" + [...v.slice(1)].map((x) => x + x).join("");
  return v;
}

export function extraColors(svg) {
  const found = new Set();
  const collect = (v) => {
    const n = normalizeColor(v);
    if (!NOT_A_COLOR.has(n) && !n.startsWith("url(")) found.add(n);
  };
  for (const m of svg.matchAll(COLOR_ATTR)) collect(m[2]);
  for (const m of svg.matchAll(STYLE_ATTR)) for (const s of m[1].matchAll(STYLE_COLOR)) collect(s[2]);
  return [...found].sort();
}

export function normalizeSvg(raw, { neutralColors = [] } = {}) {
  let svg = raw.replace(/\r\n?/g, "\n").trim()
    .replace(/<\?xml[^>]*>\s*/g, "")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<title>[\s\S]*?<\/title>/g, "");
  const root = /^<svg\b([^>]*)>/.exec(svg);
  if (!root) throw new Error("geen <svg>-root");
  if (FORBIDDEN.test(svg)) throw new Error("scripts, event-handlers of externe verwijzingen zijn niet toegestaan");
  const vb = /\bviewBox\s*=\s*"([^"]*)"/.exec(root[1]);
  const vbValue = vb ? vb[1].trim().split(/[\s,]+/).join(" ") : null;
  if (vbValue !== "0 0 24 24") throw new Error(`viewBox moet "0 0 24 24" zijn (gevonden: ${vbValue ?? "geen"})`);
  const attrs = root[1]
    .replace(/\s(width|height)\s*=\s*"[^"]*"/g, "")
    .replace(/\sxmlns\s*=\s*"[^"]*"/g, "")
    .replace(/\s+/g, " ")
    .trimEnd();
  svg = `<svg ${SVG_NS}${attrs.startsWith(" ") ? attrs : " " + attrs}>` + svg.slice(root[0].length);
  const neutral = new Set(neutralColors.map(normalizeColor));
  const recolor = (value) => {
    const n = normalizeColor(value);
    return n === "currentcolor" || neutral.has(n) ? "currentColor" : value.trim();
  };
  svg = svg
    .replace(COLOR_ATTR, (_, name, value) => `${name}="${recolor(value)}"`)
    .replace(STYLE_ATTR, (_, style) => `style="${style.replace(STYLE_COLOR, (__, p, v) => `${p}:${recolor(v)}`)}"`)
    .replace(/>\s+</g, "><")
    .replace(/[ \t]{2,}/g, " ");
  return { svg, colors: extraColors(svg) };
}
