import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { rawString } from "../icons/rust.mjs";

export function readSharedTabs(dir) {
  return readdirSync(dir).filter((f) => f.endsWith(".toml")).sort()
    .map((f) => [f.slice(0, -5), readFileSync(join(dir, f), "utf8").replace(/\r\n?/g, "\n")]);
}

export function renderSharedTabsRust(tabs) {
  const sorted = [...tabs].sort((a, b) => (a[0] < b[0] ? -1 : 1));
  return `/// Gedeelde ribbon-tabs uit \`design/ribbons/\`: (naam, TOML-bron).
pub const SHARED_TABS: &[(&str, &str)] = &[
${sorted.map(([n, src]) => `    (${JSON.stringify(n)}, ${rawString(src)}),`).join("\n")}
];
`;
}
