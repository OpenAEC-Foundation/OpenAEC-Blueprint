import { test } from "node:test";
import assert from "node:assert/strict";
import { loadTokens } from "../tokens/load.mjs";
import { renderFrappeCss } from "../tokens/frappe-css.mjs";
import { repoPath } from "../lib/paths.mjs";

const fonts = [
  { family: "Inter", file: "Inter-Regular.ttf", weight: 400 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Bold.ttf", weight: 700 },
];

test("Desk-variabelen voor licht en donker uit de tokens", () => {
  const css = renderFrappeCss(loadTokens(repoPath("design", "tokens")), fonts);
  assert.match(css, /:root,\s*\[data-theme="light"\]\s*\{[^}]*--primary:\s*#D97706;/s);
  assert.match(css, /\[data-theme="light"\][^}]*--bg-color:\s*#FAFAF9;/s);
  assert.match(css, /\[data-theme="dark"\]\s*\{[^}]*--bg-color:\s*#36363E;/s);
  assert.match(css, /--font-stack:\s*'Inter'/);
  assert.match(css, /@font-face\s*\{[^}]*font-family:\s*"Space Grotesk";[^}]*\/assets\/openaec_theme\/fonts\/SpaceGrotesk-Bold\.ttf/s);
});
