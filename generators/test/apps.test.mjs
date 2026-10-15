import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { loadApps } from "../apps/load.mjs";
import { repoPath } from "../lib/paths.mjs";

test("het echte register is geldig", () => {
  const apps = loadApps(repoPath("design", "apps.toml"));
  assert.ok(apps.find((a) => a.id === "openaec-template" && a.logo === "openaec-template"));
});

test("fouten in het register worden gemeld", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-apps-"));
  mkdirSync(join(dir, "logos", "apps"), { recursive: true });
  const file = join(dir, "apps.toml");
  writeFileSync(file, `
[[app]]
id = "Bad Id"
display_name = "X"
category = 5
[[app]]
id = "dup"
display_name = "A"
category = 1
logo = "ontbreekt"
[[app]]
id = "dup"
display_name = "B"
category = 1
`);
  assert.throws(() => loadApps(file), (e) =>
    /ongeldig app-id: Bad Id/.test(e.message) && /categorie 5/.test(e.message) &&
    /dubbel app-id: dup/.test(e.message) && /pictogram ontbreekt: ontbreekt/.test(e.message));
});
