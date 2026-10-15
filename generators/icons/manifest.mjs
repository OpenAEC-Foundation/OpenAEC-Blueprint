import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { readToml } from "../lib/toml.mjs";
import { normalizeSvg } from "./normalize.mjs";

export const ID_PATTERN = /^[a-z][a-z0-9]*\/[a-z0-9]+(?:-[a-z0-9]+)*$/;
const byId = (a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);

export class IconManifestError extends Error {
  constructor(errors) {
    super(`icons.toml bevat ${errors.length} fout(en):\n- ${errors.join("\n- ")}`);
    this.errors = errors;
  }
}

export function listSvgIds(iconsDir) {
  const ids = [];
  for (const domain of readdirSync(iconsDir).sort()) {
    const dir = join(iconsDir, domain);
    if (!statSync(dir).isDirectory()) continue;
    for (const f of readdirSync(dir).sort()) if (f.endsWith(".svg")) ids.push(`${domain}/${f.slice(0, -4)}`);
  }
  return ids;
}

export function loadIconManifest(iconsDir) {
  const entries = readToml(join(iconsDir, "icons.toml")).icon ?? [];
  const errors = [];
  const seen = new Set();
  for (const e of entries) {
    if (!ID_PATTERN.test(e.id ?? "")) errors.push(`ongeldig icoon-id: ${e.id}`);
    if (seen.has(e.id)) errors.push(`dubbel icoon-id: ${e.id}`);
    seen.add(e.id);
    if (!e.label?.nl || !e.label?.en) errors.push(`${e.id}: label.nl en label.en zijn verplicht`);
    if (!e.source) errors.push(`${e.id}: source is verplicht`);
  }
  for (const id of listSvgIds(iconsDir)) if (!seen.has(id)) errors.push(`${id}.svg staat niet in icons.toml`);

  const icons = [];
  const bySvg = new Map();
  for (const e of [...entries].filter((x) => ID_PATTERN.test(x.id ?? "")).sort(byId)) {
    const [domain, name] = e.id.split("/");
    const file = join(iconsDir, domain, `${name}.svg`);
    if (!existsSync(file)) { errors.push(`${e.id}: bestand ontbreekt`); continue; }
    let result;
    try { result = normalizeSvg(readFileSync(file, "utf8")); }
    catch (err) { errors.push(`${e.id}: ${err.message}`); continue; }
    const tags = e.tags ?? [];
    if (result.colors.length && !tags.includes("color")) {
      errors.push(`${e.id}: bevat kleuren ${result.colors.join(", ")} maar mist tag "color"`);
    }
    if (!result.colors.length && tags.includes("color")) errors.push(`${e.id}: tag "color" maar geen eigen kleuren`);
    if (bySvg.has(result.svg)) errors.push(`${e.id}: zelfde SVG als ${bySvg.get(result.svg)}`);
    else bySvg.set(result.svg, e.id);
    icons.push({ id: e.id, domain, name, label: e.label, tags, source: e.source, svg: result.svg });
  }
  if (errors.length) throw new IconManifestError(errors);
  return icons;
}
