import { test } from "node:test";
import assert from "node:assert/strict";
import { assertThemeParity, classify, loadTokens } from "../tokens/load.mjs";
import { constName, hexToRgba, lengthToPx, renderTokensRust } from "../tokens/rust.mjs";
import { repoPath } from "../lib/paths.mjs";

test("classify haalt light/dark uit themed paden", () => {
  const out = classify([
    { path: ["color", "surface", "light", "bg"], value: "#FFF", comment: null },
    { path: ["color", "surface", "dark", "bg"], value: "#000", comment: null },
    { path: ["color", "brand", "amber"], value: "#D97706", comment: null },
  ]);
  assert.deepEqual(out.light[0].path, ["color", "surface", "bg"]);
  assert.deepEqual(out.dark[0].path, ["color", "surface", "bg"]);
  assert.equal(out.static.length, 1);
});

test("assertThemeParity weigert ontbrekend dark-token", () => {
  const tokens = { static: [], light: [{ path: ["color", "text", "primary"] }], dark: [] };
  assert.throws(() => assertThemeParity(tokens), /color\.text\.primary/);
});

test("conversies", () => {
  assert.deepEqual(hexToRgba("#D97706"), [0xd9, 0x77, 0x06, 0xff]);
  assert.deepEqual(hexToRgba("#d9770680"), [0xd9, 0x77, 0x06, 0x80]);
  assert.throws(() => hexToRgba("rgb(1,2,3)"), /Ongeldige kleur/);
  assert.equal(lengthToPx("0"), 0);
  assert.equal(lengthToPx("0.25rem"), 4);
  assert.equal(lengthToPx("96px"), 96);
  assert.throws(() => lengthToPx("10vh"), /Onbekende lengte/);
  assert.equal(constName("2xl", "size"), "S2XL");
  assert.equal(constName("ribbon-height", "spacing"), "RIBBON_HEIGHT");
});

test("renderTokensRust bevat merk-, thema- en maatconstanten", () => {
  const rust = renderTokensRust(loadTokens(repoPath("design", "tokens")));
  assert.match(rust, /pub const AMBER: crate::Rgba = crate::Rgba::new\(0xD9, 0x77, 0x06, 0xFF\);/);
  assert.match(rust, /pub const RIBBON_HEIGHT: f32 = 96\.0;/);
  assert.match(rust, /pub const HEADING: &str = "Space Grotesk";/);
  assert.match(rust, /pub const LIGHT: Theme = Theme \{/);
  assert.match(rust, /surface_bg: crate::Rgba::new\(0xFA, 0xFA, 0xF9, 0xFF\)/);
  assert.ok(!rust.includes("shadow"), "schaduwen zijn CSS-specifiek en horen niet in Rust");
});
