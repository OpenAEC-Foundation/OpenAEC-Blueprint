import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { importIcons, manifestToml, readTsIconModule } from "../icons/import.mjs";
import { parseToml } from "../lib/toml.mjs";

test("readTsIconModule leest export const xIcon = `<svg…>`", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-ts-"));
  const file = join(dir, "icons.ts");
  writeFileSync(file, 'export const undoIcon = `<svg viewBox="0 0 24 24"></svg>`;\nexport const x = 1;\n');
  assert.deepEqual([...readTsIconModule(file).keys()], ["undoIcon"]);
});

test("importIcons schrijft genormaliseerde SVG's en slaat dubbelen over", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-imp-"));
  const svg = '<svg viewBox="0 0 24 24"><path stroke="currentColor" d="M1 1"/></svg>';
  const { written, duplicates } = importIcons(
    [{ id: "edit/undo", svg }, { id: "edit/again", svg }], dir);
  assert.deepEqual(written.map((w) => w.id), ["edit/undo"]);
  assert.deepEqual(duplicates, [["edit/again", "edit/undo"]]);
  assert.ok(readFileSync(join(dir, "edit", "undo.svg"), "utf8").startsWith('<svg xmlns="http://www.w3.org/2000/svg"'));
});

test("manifestToml is leesbaar en gesorteerd", () => {
  const toml = manifestToml([
    { id: "edit/undo", label: { nl: "Ongedaan maken", en: "Undo" }, tags: [], source: "openaec" },
    { id: "edit/copy", label: { nl: "Kopiëren", en: "Copy" }, tags: ["edit"], source: "openaec" },
  ]);
  const parsed = parseToml(toml);
  assert.deepEqual(parsed.icon.map((i) => i.id), ["edit/copy", "edit/undo"]);
  assert.equal(parsed.icon[0].label.nl, "Kopiëren");
});
