import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { loadIconManifest } from "../icons/manifest.mjs";

const SVG = '<svg viewBox="0 0 24 24"><path stroke="currentColor" d="M1 1L5 5"/></svg>';

function fixture(files, toml) {
  const dir = mkdtempSync(join(tmpdir(), "oa-icons-"));
  for (const [id, svg] of Object.entries(files)) {
    const [domain, name] = id.split("/");
    mkdirSync(join(dir, domain), { recursive: true });
    writeFileSync(join(dir, domain, `${name}.svg`), svg);
  }
  writeFileSync(join(dir, "icons.toml"), toml);
  return dir;
}

const entry = (id, extra = "") =>
  `[[icon]]\nid = "${id}"\nlabel = { nl = "N", en = "E" }\ntags = []\nsource = "openaec"\n${extra}\n`;

test("geldig manifest geeft gesorteerde iconen terug", () => {
  const dir = fixture({ "edit/undo": SVG, "edit/copy": SVG.replace("M1 1", "M2 2") }, entry("edit/undo") + entry("edit/copy"));
  const icons = loadIconManifest(dir);
  assert.deepEqual(icons.map((i) => i.id), ["edit/copy", "edit/undo"]);
  assert.equal(icons[0].domain, "edit");
});

test("meldt bestand zonder manifest, manifest zonder bestand, slecht id en ontbrekend label", () => {
  const dir = fixture({ "edit/undo": SVG, "edit/extra": SVG.replace("M1", "M3") },
    entry("edit/undo") + entry("edit/missing") + entry("Edit/Bad") +
    '[[icon]]\nid = "edit/nolabel"\nsource = "openaec"\n');
  assert.throws(() => loadIconManifest(dir), (err) => {
    const all = err.errors.join("\n");
    return /edit\/extra\.svg staat niet in icons\.toml/.test(all) &&
      /edit\/missing: bestand ontbreekt/.test(all) &&
      /ongeldig icoon-id: Edit\/Bad/.test(all) &&
      /edit\/nolabel: label\.nl en label\.en zijn verplicht/.test(all);
  });
});

test("eigen kleuren vereisen tag color, en omgekeerd", () => {
  const colored = '<svg viewBox="0 0 24 24"><path stroke="#4cc9f0"/></svg>';
  const toml = [
    '[[icon]]', 'id = "cad/a"', 'label = { nl = "N", en = "E" }', 'tags = []', 'source = "openaec"', '',
    '[[icon]]', 'id = "cad/b"', 'label = { nl = "N", en = "E" }', 'tags = ["color"]', 'source = "openaec"', '',
  ].join("\n");
  const dir = fixture({ "cad/a": colored, "cad/b": SVG }, toml);
  assert.throws(() => loadIconManifest(dir), (err) => {
    const all = err.errors.join("\n");
    return /cad\/a: bevat kleuren #4cc9f0 maar mist tag "color"/.test(all) &&
      /cad\/b: tag "color" maar geen eigen kleuren/.test(all);
  });
});

test("hetzelfde SVG onder twee id's wordt geweigerd", () => {
  const dir = fixture({ "edit/a": SVG, "edit/b": SVG }, entry("edit/a") + entry("edit/b"));
  assert.throws(() => loadIconManifest(dir), (err) => /edit\/b: zelfde SVG als edit\/a/.test(err.errors.join("\n")));
});
