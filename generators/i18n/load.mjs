import { readFileSync } from "node:fs";
import { join } from "node:path";

const CONTROL = /[\u0000-\u001f\u007f]/;

export const LANGS = ["nl", "en"];

export function flatten(obj, prefix = "") {
  const out = new Map();
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === "object") for (const [kk, vv] of flatten(v, key)) out.set(kk, vv);
    else out.set(key, String(v));
  }
  return out;
}

export function loadI18n(i18nDir) {
  const maps = Object.fromEntries(LANGS.map((l) =>
    [l, flatten(JSON.parse(readFileSync(join(i18nDir, l, "openaec.json"), "utf8")))]));
  const all = new Set(LANGS.flatMap((l) => [...maps[l].keys()]));
  const errors = [];
  for (const key of [...all].sort()) {
    for (const l of LANGS) {
      if (!maps[l].has(key)) errors.push(`${key} (${l} ontbreekt)`);
      else if (!maps[l].get(key).trim()) errors.push(`${key} (${l} leeg)`);
      else if (CONTROL.test(maps[l].get(key))) errors.push(`${key} (${l} bevat besturingstekens)`);
    }
  }
  if (errors.length) throw new Error(`Vertalingen onvolledig: ${errors.join(", ")}`);
  return maps;
}
