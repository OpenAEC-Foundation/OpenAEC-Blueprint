import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { readVersions, setVersion } from "../version/set-version.mjs";

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "oa-ver-"));
  writeFileSync(join(root, "Cargo.toml"), '[workspace]\nmembers = []\n\n[workspace.package]\nversion = "0.1.0"\nedition = "2021"\n');
  for (const p of ["a", "b"]) {
    mkdirSync(join(root, "packages", p), { recursive: true });
    writeFileSync(join(root, "packages", p, "package.json"), JSON.stringify({ name: p, version: "0.1.0" }, null, 2) + "\n");
  }
  mkdirSync(join(root, "generators"), { recursive: true });
  writeFileSync(join(root, "generators", "package.json"), JSON.stringify({ name: "g", version: "0.1.0" }, null, 2) + "\n");
  mkdirSync(join(root, "frappe", "openaec_theme", "openaec_theme"), { recursive: true });
  writeFileSync(join(root, "frappe", "openaec_theme", "openaec_theme", "__init__.py"), '__version__ = "0.1.0"\n');
  return root;
}

test("setVersion zet overal dezelfde versie", () => {
  const root = fixture();
  setVersion(root, "0.2.0");
  assert.deepEqual(new Set(readVersions(root).values()), new Set(["0.2.0"]));
  assert.equal(readVersions(root).size, 5);
});

test("ongeldige versie wordt geweigerd", () => {
  assert.throws(() => setVersion(fixture(), "v0.2"), /semver/);
});
