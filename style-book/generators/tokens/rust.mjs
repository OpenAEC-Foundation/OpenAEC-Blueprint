export function hexToRgba(hex) {
  const m = /^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$/.exec(hex.trim());
  if (!m) throw new Error(`Ongeldige kleur: ${hex}`);
  const rgb = [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16));
  return [...rgb, m[2] ? parseInt(m[2], 16) : 255];
}

export function lengthToPx(value) {
  const v = value.trim();
  if (v === "0") return 0;
  let m = /^(-?\d*\.?\d+)px$/.exec(v);
  if (m) return Number(m[1]);
  m = /^(-?\d*\.?\d+)rem$/.exec(v);
  if (m) return Number(m[1]) * 16;
  throw new Error(`Onbekende lengte: ${value}`);
}

export function constName(segment, parent) {
  const up = segment.replace(/-/g, "_").toUpperCase();
  return /^\d/.test(up) ? parent[0].toUpperCase() + up : up;
}

const modName = (s) => s.replace(/-/g, "_");
const f32 = (n) => (Number.isInteger(n) ? `${n}.0` : String(n));
const hex2 = (n) => "0x" + n.toString(16).toUpperCase().padStart(2, "0");
const rgbaExpr = (hex) => `crate::Rgba::new(${hexToRgba(hex).map(hex2).join(", ")})`;

function rustValue(leaf) {
  const [root, group] = leaf.path;
  if (root === "color") return { type: "crate::Rgba", expr: rgbaExpr(leaf.value) };
  if (root === "spacing" || root === "radius") return { type: "f32", expr: f32(lengthToPx(leaf.value)) };
  if (root === "font" && group === "family") {
    const first = leaf.value.split(",")[0].trim().replace(/^['"]|['"]$/g, "");
    return { type: "&str", expr: JSON.stringify(first) };
  }
  if (root === "font" && group === "weight") return { type: "u16", expr: String(Number(leaf.value)) };
  if (root === "font" && group === "size") return { type: "f32", expr: f32(lengthToPx(leaf.value)) };
  if (root === "font" && group === "line-height") return { type: "f32", expr: f32(Number(leaf.value)) };
  if (root === "font" && group === "letter-spacing") {
    return { type: "f32", expr: f32(leaf.value === "0" ? 0 : Number(leaf.value.replace(/em$/, ""))) };
  }
  return null; // shadow e.d.: CSS-specifiek
}

function renderModules(leaves) {
  const tree = {};
  for (const leaf of leaves) {
    const v = rustValue(leaf);
    if (!v) continue;
    let node = tree;
    for (const seg of leaf.path.slice(0, -1)) node = node[seg] ??= {};
    (node.$consts ??= []).push({ leaf, v });
  }
  const render = (node, indent) => {
    let out = "";
    for (const c of (node.$consts ?? []).sort((a, b) => (a.leaf.path.join(".") < b.leaf.path.join(".") ? -1 : 1))) {
      const name = constName(c.leaf.path.at(-1), c.leaf.path.at(-2));
      if (c.leaf.comment) out += `${indent}/// ${c.leaf.comment}\n`;
      out += `${indent}pub const ${name}: ${c.v.type} = ${c.v.expr};\n`;
    }
    for (const key of Object.keys(node).filter((k) => k !== "$consts").sort()) {
      out += `${indent}pub mod ${modName(key)} {\n${render(node[key], indent + "    ")}${indent}}\n`;
    }
    return out;
  };
  return render(tree, "");
}

const fieldName = (path) => path.slice(1).join("_").replace(/-/g, "_");

export function renderTokensRust(tokens) {
  const light = [...tokens.light].sort((a, b) => (fieldName(a.path) < fieldName(b.path) ? -1 : 1));
  const dark = new Map(tokens.dark.map((l) => [fieldName(l.path), l]));
  let out = renderModules(tokens.static);
  out += "\n/// Thema-afhankelijke kleuren (licht en donker).\n#[derive(Debug, Clone, Copy, PartialEq, Eq)]\npub struct Theme {\n";
  for (const l of light) out += `    pub ${fieldName(l.path)}: crate::Rgba,\n`;
  out += "}\n";
  for (const [name, get] of [["LIGHT", (l) => l], ["DARK", (l) => dark.get(fieldName(l.path))]]) {
    out += `\npub const ${name}: Theme = Theme {\n`;
    for (const l of light) out += `    ${fieldName(l.path)}: ${rgbaExpr(get(l).value)},\n`;
    out += "};\n";
  }
  return out;
}
