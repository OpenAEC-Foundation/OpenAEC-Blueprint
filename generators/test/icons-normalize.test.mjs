import { test } from "node:test";
import assert from "node:assert/strict";
import { extraColors, normalizeColor, normalizeSvg } from "../icons/normalize.mjs";

const wrap = (inner, attrs = 'viewBox="0 0 24 24"') => `<svg ${attrs}>${inner}</svg>`;

test("voegt xmlns toe en haalt width/height van de root", () => {
  const { svg } = normalizeSvg(wrap('<path d="M1 1"/>', 'viewBox="0 0 24 24" width="64" height="64"'));
  assert.ok(svg.startsWith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'));
  assert.ok(!/width=|height=/.test(svg.slice(0, svg.indexOf(">"))));
});

test("weigert andere viewBox, scripts en externe verwijzingen", () => {
  assert.throws(() => normalizeSvg(wrap("", 'viewBox="0 0 16 16"')), /viewBox/);
  assert.throws(() => normalizeSvg(wrap("<script>x</script>")), /niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<image href="https://x/y.png"/>')), /niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<path onclick="x()"/>')), /niet toegestaan/);
  assert.throws(() => normalizeSvg("<g/>"), /geen <svg>/);
});

test("neutrale kleuren worden currentColor, ook in style en als 3-cijferige hex", () => {
  const raw = wrap('<path stroke="#E0E0E0"/><path fill="#eee"/><path style="stroke:#e0e0e0;fill:#4CC9F0"/>');
  const { svg, colors } = normalizeSvg(raw, { neutralColors: ["#e0e0e0", "#eeeeee"] });
  assert.ok(svg.includes('stroke="currentColor"'));
  assert.ok(svg.includes('fill="currentColor"'));
  assert.ok(svg.includes("stroke:currentColor"));
  assert.deepEqual(colors, ["#4cc9f0"]);
});

test("currentColor in elke schrijfwijze telt niet als eigen kleur", () => {
  assert.deepEqual(extraColors(wrap('<path stroke="CurrentColor" fill="none"/>')), []);
  assert.equal(normalizeColor("#ABC"), "#aabbcc");
});
