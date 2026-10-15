import { execFileSync } from "node:child_process";
import { runAll } from "./generate.mjs";
import { ROOT } from "./lib/paths.mjs";

await runAll(ROOT);
const out = execFileSync(
  "git",
  ["status", "--porcelain", "--", "packages", "crates", "frappe", "design"],
  { cwd: ROOT, encoding: "utf8" },
);
if (out.trim()) {
  console.error("Gegenereerde bestanden wijken af van wat in git staat:\n" + out);
  process.exit(1);
}
console.log("✓ gegenereerde bestanden zijn actueel");
