import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { normalizeSvg } from "./normalize.mjs";

export function readTsIconModule(file) {
  const out = new Map();
  for (const m of readFileSync(file, "utf8").matchAll(/export const (\w+)\s*=\s*`([^`]*)`/g)) out.set(m[1], m[2]);
  return out;
}

export function readSvgDirectory(dir, { domainFor, nameFor }) {
  const out = [];
  const walk = (d, rel) => {
    for (const f of readdirSync(d, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : 1))) {
      if (f.isDirectory()) walk(join(d, f.name), [...rel, f.name]);
      else if (f.name.endsWith(".svg")) {
        const base = f.name.slice(0, -4);
        out.push({ id: `${domainFor(rel, base)}/${nameFor(rel, base)}`, svg: readFileSync(join(d, f.name), "utf8") });
      }
    }
  };
  walk(dir, []);
  return out;
}

export function importIcons(entries, iconsDir, { neutralColors = [] } = {}) {
  const seen = new Map();
  const written = [];
  const duplicates = [];
  for (const e of entries) {
    const { svg } = normalizeSvg(e.svg, { neutralColors });
    if (seen.has(svg)) { duplicates.push([e.id, seen.get(svg)]); continue; }
    seen.set(svg, e.id);
    const [domain, name] = e.id.split("/");
    const file = join(iconsDir, domain, `${name}.svg`);
    mkdirSync(dirname(file), { recursive: true });
    writeFileSync(file, svg + "\n", "utf8");
    written.push(e);
  }
  return { written, duplicates };
}

const q = (s) => JSON.stringify(s);

export function manifestToml(entries) {
  const sorted = [...entries].sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return sorted.map((e) => [
    "[[icon]]",
    `id = ${q(e.id)}`,
    `label = { nl = ${q(e.label.nl)}, en = ${q(e.label.en)} }`,
    `tags = [${(e.tags ?? []).map(q).join(", ")}]`,
    `source = ${q(e.source)}`,
    "",
  ].join("\n")).join("\n");
}
