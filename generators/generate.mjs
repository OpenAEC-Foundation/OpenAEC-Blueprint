import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { ROOT } from "./lib/paths.mjs";
import { writeGenerated } from "./lib/write.mjs";
import { loadI18n } from "./i18n/load.mjs";
import { renderI18nRust } from "./i18n/rust.mjs";
import { loadIconManifest } from "./icons/manifest.mjs";
import { renderIconsByIdTs, renderIconsTs } from "./icons/react.mjs";
import { renderIconsRust } from "./icons/rust.mjs";
import { loadTokens } from "./tokens/load.mjs";
import { renderTokensRust } from "./tokens/rust.mjs";

// Elke stap: [naam, (root) => string[] | Promise<string[]>] — geeft geschreven bestanden terug.
// Latere tasks voegen bovenaan imports toe (zonder dubbelingen) en hieronder steps.push(...).
export const steps = [];

steps.push(["tokens-package", (root) => {
  execFileSync(process.execPath, ["build.js"], { cwd: join(root, "packages", "tokens"), stdio: "inherit" });
  return [];
}]);

steps.push(["tokens-rust", (root) => [
  writeGenerated(join(root, "crates", "openaec-tokens", "src", "generated.rs"),
    renderTokensRust(loadTokens(join(root, "design", "tokens")))),
]]);

steps.push(["icons-react", (root) => {
  const icons = loadIconManifest(join(root, "design", "icons"));
  const dir = join(root, "packages", "icons", "src", "generated");
  return [
    writeGenerated(join(dir, "icons.ts"), renderIconsTs(icons)),
    writeGenerated(join(dir, "by-id.ts"), renderIconsByIdTs(icons)),
  ];
}]);

steps.push(["icons-rust", (root) => [
  writeGenerated(join(root, "crates", "openaec-icons", "src", "generated.rs"),
    renderIconsRust(loadIconManifest(join(root, "design", "icons")))),
]]);

steps.push(["i18n", (root) => {
  const src = join(root, "design", "i18n");
  const maps = loadI18n(src);
  const out = [];
  for (const lang of ["nl", "en"]) {
    // JSON zonder header; inhoud 1-op-1 uit de bron, opnieuw geformatteerd.
    const json = JSON.stringify(JSON.parse(readFileSync(join(src, lang, "openaec.json"), "utf8")), null, 2);
    out.push(writeGenerated(join(root, "packages", "i18n", "src", "generated", `${lang}.json`), json));
  }
  out.push(writeGenerated(join(root, "crates", "openaec-i18n", "src", "generated.rs"), renderI18nRust(maps)));
  return out;
}]);

export async function runAll(root = ROOT) {
  const written = [];
  for (const [name, run] of steps) {
    const files = await run(root);
    console.log(`✓ ${name}: ${files.length} bestanden`);
    written.push(...files);
  }
  return written;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  runAll().catch((err) => {
    console.error(`✗ ${err.message}`);
    process.exit(1);
  });
}
