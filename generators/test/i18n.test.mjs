import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { flatten, loadI18n } from "../i18n/load.mjs";
import { renderI18nRust } from "../i18n/rust.mjs";
import { repoPath } from "../lib/paths.mjs";

test("flatten maakt puntsleutels", () => {
  assert.deepEqual([...flatten({ a: { b: "x", c: { d: "y" } } })], [["a.b", "x"], ["a.c.d", "y"]]);
});

test("ontbrekende of lege vertaling wordt gemeld", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-i18n-"));
  mkdirSync(join(dir, "nl")); mkdirSync(join(dir, "en"));
  writeFileSync(join(dir, "nl", "openaec.json"), JSON.stringify({ a: "x", b: "y" }));
  writeFileSync(join(dir, "en", "openaec.json"), JSON.stringify({ a: "" }));
  assert.throws(() => loadI18n(dir), (e) => /b \(en ontbreekt\)/.test(e.message) && /a \(en leeg\)/.test(e.message));
});

test("echte bron is volledig en niet-ASCII blijft heel", () => {
  const { nl } = loadI18n(repoPath("design", "i18n"));
  assert.equal(nl.get("action.copy"), "Kopiëren");
  const rs = renderI18nRust(loadI18n(repoPath("design", "i18n")));
  assert.match(rs, /"action\.copy" => Some\("Kopiëren"\)/);
});
