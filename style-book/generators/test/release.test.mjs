import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { planPublish, readPackages } from "../release/publish-npm.mjs";

const pkgs = [
  { name: "@x/a", version: "0.1.0" },
  { name: "@x/b", version: "0.1.0" },
  { name: "@x/priv", version: "0.1.0", private: true },
];

test("publiceert alleen ontbrekende, niet-private packages", () => {
  const plan = planPublish(pkgs, (n) => n === "@x/a");
  assert.deepEqual(plan.map((p) => [p.name, p.action]), [
    ["@x/a", "skip-published"],
    ["@x/b", "publish"],
    ["@x/priv", "skip-private"],
  ]);
});

test("private package wordt nooit bij het register opgevraagd", () => {
  const asked = [];
  planPublish(pkgs, (n, v) => (asked.push(`${n}@${v}`), false));
  assert.deepEqual(asked, ["@x/a@0.1.0", "@x/b@0.1.0"]);
});

test("alles al gepubliceerd: niets te doen (re-run)", () => {
  assert.ok(planPublish(pkgs, () => true).every((p) => p.action !== "publish"));
});

test("readPackages leest packages/*/package.json gesorteerd", () => {
  const root = mkdtempSync(join(tmpdir(), "oa-rel-"));
  for (const p of ["b", "a"]) {
    mkdirSync(join(root, "packages", p), { recursive: true });
    writeFileSync(join(root, "packages", p, "package.json"), JSON.stringify({ name: p, version: "0.1.0" }));
  }
  assert.deepEqual(readPackages(root).map((p) => p.name), ["a", "b"]);
  assert.deepEqual(readPackages(join(root, "leeg")), []);
});
