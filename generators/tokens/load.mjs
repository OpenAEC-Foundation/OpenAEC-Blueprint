import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const THEMED_GROUPS = ["surface", "text", "border", "semantic"];

export function* walkTokens(tree, prefix = []) {
  for (const [key, val] of Object.entries(tree)) {
    if (key.startsWith("$")) continue;
    if (val && typeof val === "object" && "value" in val) {
      yield { path: [...prefix, key], value: String(val.value), comment: val.comment ?? null };
    } else if (val && typeof val === "object") {
      yield* walkTokens(val, [...prefix, key]);
    }
  }
}

export function classify(leaves) {
  const out = { static: [], light: [], dark: [] };
  for (const leaf of leaves) {
    const [root, group, mode, ...rest] = leaf.path;
    if (root === "color" && THEMED_GROUPS.includes(group) && (mode === "light" || mode === "dark")) {
      out[mode].push({ ...leaf, path: [root, group, ...rest] });
    } else {
      out.static.push(leaf);
    }
  }
  return out;
}

export function assertThemeParity(tokens) {
  const key = (l) => l.path.join(".");
  const light = new Set(tokens.light.map(key));
  const dark = new Set(tokens.dark.map(key));
  const missing = [...light].filter((k) => !dark.has(k)).map((k) => `${k} (dark ontbreekt)`)
    .concat([...dark].filter((k) => !light.has(k)).map((k) => `${k} (light ontbreekt)`));
  if (missing.length) throw new Error(`Thema's niet gelijk: ${missing.join(", ")}`);
}

export function loadTokens(tokensDir) {
  const files = readdirSync(tokensDir).filter((f) => f.endsWith(".json")).sort();
  const leaves = [];
  for (const f of files) leaves.push(...walkTokens(JSON.parse(readFileSync(join(tokensDir, f), "utf8"))));
  const tokens = classify(leaves);
  assertThemeParity(tokens);
  return tokens;
}

export function tokenValue(tokens, dottedPath) {
  const leaf = tokens.static.find((l) => l.path.join(".") === dottedPath);
  if (!leaf) throw new Error(`Token ${dottedPath} bestaat niet`);
  return leaf.value;
}
