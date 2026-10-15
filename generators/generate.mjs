import { execFileSync } from "node:child_process";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { ROOT } from "./lib/paths.mjs";

// Elke stap: [naam, (root) => string[] | Promise<string[]>] — geeft geschreven bestanden terug.
// Latere tasks voegen bovenaan imports toe (zonder dubbelingen) en hieronder steps.push(...).
export const steps = [];

steps.push(["tokens-package", (root) => {
  execFileSync(process.execPath, ["build.js"], { cwd: join(root, "packages", "tokens"), stdio: "inherit" });
  return [];
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
