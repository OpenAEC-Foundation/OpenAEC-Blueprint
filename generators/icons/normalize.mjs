import { XMLParser, XMLValidator } from "fast-xml-parser";

const SVG_NS = "http://www.w3.org/2000/svg";
const NOT_A_COLOR = new Set(["none", "currentcolor", "transparent", "inherit"]);

const ELEMENTS = new Set([
  "g", "path", "circle", "ellipse", "line", "polyline", "polygon", "rect",
  "defs", "linearGradient", "radialGradient", "stop", "clipPath", "mask",
]);
const DROPPED_ELEMENTS = new Set(["title", "desc", "metadata"]);

// Presentatie-eigenschappen: toegestaan als attribuut én als eigenschap in `style`.
const PRESENTATION = new Set([
  "fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-linecap",
  "stroke-linejoin", "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset",
  "stroke-opacity", "opacity", "clip-path", "clip-rule", "mask", "stop-color",
  "stop-opacity", "color", "vector-effect",
]);
const COLOR_PROPS = new Set(["fill", "stroke", "stop-color", "color"]);
const ATTRIBUTES = new Set([
  ...PRESENTATION,
  "id", "d", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height",
  "points", "transform", "offset", "gradientUnits", "gradientTransform", "style",
]);
const ROOT_ONLY = new Set(["viewBox"]);
const STRIPPED_ATTR = /^(?:xmlns(?::.*)?|sodipodi:.*|inkscape:.*|data-.*)$/;

const parser = new XMLParser({
  preserveOrder: true,
  ignoreAttributes: false,
  attributeNamePrefix: "@_",
  parseAttributeValue: false,
  parseTagValue: false,
  trimValues: false,
  ignoreDeclaration: true,
  ignorePiTags: true,
  processEntities: true,
});

export function normalizeColor(c) {
  const v = c.trim().toLowerCase();
  if (/^#[0-9a-f]{3}$/.test(v)) return "#" + [...v.slice(1)].map((x) => x + x).join("");
  return v;
}

/** Parseert naar { name, attrs: [[naam, waarde]], children } en gooit bij misvormde XML. */
function parseTree(raw) {
  const text = raw.replace(/^﻿/, "");
  if (/<!(?:DOCTYPE|ENTITY)/i.test(text)) throw new Error("DOCTYPE en entiteiten zijn niet toegestaan");
  const valid = XMLValidator.validate(text);
  if (valid !== true) throw new Error(`ongeldige XML: ${valid.err.msg}`);
  const build = (nodes) => {
    const out = [];
    for (const node of nodes) {
      if ("#text" in node) {
        out.push({ text: String(node["#text"]) });
        continue;
      }
      const name = Object.keys(node).find((k) => k !== ":@");
      const attrs = Object.entries(node[":@"] ?? {}).map(([k, v]) => [k.slice(2), String(v)]);
      out.push({ name, attrs, children: build(node[name]) });
    }
    return out;
  };
  return build(parser.parse(text));
}

function styleDeclarations(style) {
  rejectEscapes("style", style);
  return style.split(";").map((d) => d.trim()).filter(Boolean).map((d) => {
    const i = d.indexOf(":");
    if (i < 1) throw new Error(`ongeldige style-declaratie: ${d}`);
    return [d.slice(0, i).trim(), d.slice(i + 1).trim()];
  });
}

function rejectEscapes(name, value) {
  if (value.includes("\\") || value.includes("/*")) {
    throw new Error(`${name}: backslash-escapes en commentaar zijn niet toegestaan`);
  }
}

const URL_REF = String.raw`url\(#[A-Za-z_][\w.-]*\)`;
const NAMED_COLOR = /^[a-zA-Z]+$/;
const HEX_COLOR = /^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/;
const RGB_COLOR = /^rgba?\(\s*[\d.]+%?\s*(?:,\s*[\d.]+%?\s*){2}(?:,\s*[\d.]+%?\s*)?\)$/i;
const isPlainColor = (v) => NAMED_COLOR.test(v) || HEX_COLOR.test(v) || RGB_COLOR.test(v);
const URL_ONLY = new RegExp(`^${URL_REF}$`);
const URL_WITH_FALLBACK = new RegExp(String.raw`^${URL_REF}(?:\s+(.+))?$`);

/** Valideert één attribuut- of style-waarde; gooit bij escapes, vreemde url()'s en ongeldige kleuren. */
function checkValue(name, value) {
  rejectEscapes(name, value);
  const v = value.trim();
  const hasUrl = /url\s*\(/i.test(v);
  if (name === "clip-path" || name === "mask") {
    if (hasUrl && !URL_ONLY.test(v)) throw new Error(`${name}: alleen url(#id) is toegestaan (gevonden: ${v})`);
    return;
  }
  if (name === "fill" || name === "stroke") {
    if (hasUrl) {
      const m = URL_WITH_FALLBACK.exec(v);
      if (!m || (m[1] !== undefined && !isPlainColor(m[1].trim()))) {
        throw new Error(`${name}: alleen url(#id) met optionele kleur-fallback is toegestaan (gevonden: ${v})`);
      }
      return;
    }
  } else if (hasUrl) {
    throw new Error(`${name}: url() is hier niet toegestaan (gevonden: ${v})`);
  }
  if (COLOR_PROPS.has(name) && !isPlainColor(v)) throw new Error(`ongeldige kleurwaarde voor ${name}: ${v}`);
}

function collectColors(nodes, found) {
  const add = (v) => {
    const n = normalizeColor(v.replace(new RegExp(String.raw`^\s*${URL_REF}`), ""));
    if (n && !NOT_A_COLOR.has(n)) found.add(n);
  };
  for (const node of nodes) {
    if (!node.name) continue;
    for (const [k, v] of node.attrs) {
      if (COLOR_PROPS.has(k)) add(v);
      else if (k === "style") for (const [p, val] of styleDeclarations(v)) if (COLOR_PROPS.has(p)) add(val);
    }
    collectColors(node.children, found);
  }
}

export function extraColors(svg) {
  const found = new Set();
  collectColors(parseTree(svg), found);
  return [...found].sort();
}

const escapeXml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function normalizeSvg(raw, { neutralColors = [] } = {}) {
  const neutral = new Set(neutralColors.map(normalizeColor));
  const recolor = (value) => {
    const n = normalizeColor(value);
    return n === "currentcolor" || neutral.has(n) ? "currentColor" : value.trim();
  };

  const top = parseTree(raw);
  const roots = top.filter((n) => n.name || n.text.trim());
  if (roots.length !== 1 || roots[0].name !== "svg") throw new Error("geen <svg>-root");
  const root = roots[0];

  const vb = root.attrs.find(([k]) => k === "viewBox")?.[1];
  const vbValue = vb === undefined ? null : vb.trim().split(/[\s,]+/).join(" ");
  if (vbValue !== "0 0 24 24") throw new Error(`viewBox moet "0 0 24 24" zijn (gevonden: ${vbValue ?? "geen"})`);

  const serializeAttrs = (node, isRoot) => {
    const out = [];
    for (const [k, v] of node.attrs) {
      if (STRIPPED_ATTR.test(k)) continue;
      if (isRoot && (k === "width" || k === "height")) continue;
      if (!(ATTRIBUTES.has(k) || (isRoot && ROOT_ONLY.has(k)))) {
        throw new Error(`attribuut ${k} is niet toegestaan`);
      }
      if (k !== "style") checkValue(k, v);
      let value = v;
      if (k === "style") {
        const decls = styleDeclarations(v);
        for (const [p, val] of decls) {
          if (!PRESENTATION.has(p)) throw new Error(`style-eigenschap ${p} is niet toegestaan`);
          checkValue(p, val);
        }
        value = decls.map(([p, val]) => `${p}:${COLOR_PROPS.has(p) ? recolor(val) : val}`).join(";");
      } else if (COLOR_PROPS.has(k)) {
        value = recolor(v);
      }
      out.push(` ${k}="${escapeXml(value.trim())}"`);
    }
    return out.join("");
  };

  const serialize = (node, isRoot) => {
    const attrs = serializeAttrs(node, isRoot);
    let inner = "";
    for (const child of node.children) {
      if (!child.name) {
        if (child.text.trim()) throw new Error("tekstinhoud is niet toegestaan");
        continue;
      }
      if (DROPPED_ELEMENTS.has(child.name)) continue;
      if (!ELEMENTS.has(child.name)) throw new Error(`element <${child.name}> is niet toegestaan`);
      inner += serialize(child, false);
    }
    const name = node.name;
    if (isRoot) return `<svg xmlns="${SVG_NS}"${attrs}>${inner}</svg>`;
    return inner ? `<${name}${attrs}>${inner}</${name}>` : `<${name}${attrs}/>`;
  };

  const svg = serialize(root, true);
  const found = new Set();
  collectColors(parseTree(svg), found);
  return { svg, colors: [...found].sort() };
}
