import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { readToml } from "../lib/toml.mjs";

const STATUS = ["actief", "buiten-scope"];
const ID = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;

export function loadApps(file) {
  const apps = readToml(file).app ?? [];
  const errors = [];
  if (apps.length === 0) errors.push("geen apps in het register");
  const seen = new Set();
  for (const a of apps) {
    if (!ID.test(a.id ?? "")) errors.push(`ongeldig app-id: ${a.id}`);
    if (seen.has(a.id)) errors.push(`dubbel app-id: ${a.id}`);
    seen.add(a.id);
    if (!a.display_name) errors.push(`${a.id}: display_name ontbreekt`);
    if (![1, 2, 3, 4].includes(a.category)) errors.push(`${a.id}: categorie ${a.category} bestaat niet (1–4)`);
    if (a.status !== undefined && !STATUS.includes(a.status)) errors.push(`${a.id}: status ${a.status} bestaat niet (${STATUS.join(" | ")})`);
    if (a.logo && !existsSync(join(dirname(file), "logos", "apps", `${a.logo}.svg`))) {
      errors.push(`${a.id}: pictogram ontbreekt: ${a.logo}`);
    }
  }
  if (errors.length) throw new Error(`apps.toml: ${errors.join("; ")}`);
  return apps;
}
