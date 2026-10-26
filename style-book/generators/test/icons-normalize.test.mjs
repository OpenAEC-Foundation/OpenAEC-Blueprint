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

const VB = 'viewBox="0 0 24 24"';

test("regressie: injectie-probes uit de review worden geweigerd", () => {
  const probes = [
    `<svg/onload=alert(1) ${VB}></svg>`,
    wrap('<path d="M1 1"onclick="alert(1)"/>'),
    wrap('<path/onclick=alert(1) d="M1 1"/>'),
    wrap("<a href='javascript:alert(1)'/>"),
    wrap("<a href=javascript:alert(1)/>"),
    wrap('<foreignObject><iframe src="javascript:alert(1)"/></foreignObject>'),
    wrap("<style>@import url(http://evil/x.css);</style>"),
    wrap('<animate attributeName="href" values="javascript:alert(1)"/>'),
    wrap('<set attributeName="href" to="javascript:alert(1)"/>'),
    wrap('<use href="#a"/>'),
    wrap('<path xlink:href="#a"/>'),
    wrap('<path class="a"/>'),
    wrap("<g><g>"),
  ];
  for (const p of probes) assert.throws(() => normalizeSvg(p), undefined, p);
});

test("regressie: elementen en attributen buiten de allow-list noemen de naam", () => {
  assert.throws(() => normalizeSvg(wrap("<script>x</script>")), /element <script> is niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<path onclick="x()"/>')), /attribuut onclick is niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<path flood-color="red"/>')), /attribuut flood-color/);
  assert.throws(() => normalizeSvg(wrap('<svg viewBox="0 0 24 24"/>')), /element <svg>/);
  assert.throws(() => normalizeSvg(wrap('<path viewBox="0 0 24 24"/>')), /attribuut viewBox/);
  assert.throws(() => normalizeSvg(wrap('<path style="behavior:x"/>')), /style-eigenschap behavior/);
});

test("regressie: url() moet naar #id verwijzen", () => {
  const ok = normalizeSvg(wrap('<defs><linearGradient id="g"><stop offset="0" stop-color="#4cc9f0"/></linearGradient></defs><path fill="url(#g)"/>'));
  assert.ok(ok.svg.includes('fill="url(#g)"'));
  assert.deepEqual(ok.colors, ["#4cc9f0"]);
  assert.throws(() => normalizeSvg(wrap('<path fill="url(http://x/y)"/>')), /url\(#id\)/);
  assert.throws(() => normalizeSvg(wrap('<path style="fill:url(http://x/y)"/>')), /url\(#id\)/);
});

test("regressie: kleuren in enkele aanhalingstekens en style tellen mee", () => {
  assert.deepEqual(normalizeSvg(wrap("<path fill='#FF0000'/>")).colors, ["#ff0000"]);
  assert.deepEqual(normalizeSvg(wrap("<path style='fill:#ff0000'/>")).colors, ["#ff0000"]);
  assert.deepEqual(extraColors(wrap("<path fill='#ff0000'/>")), ["#ff0000"]);
  assert.throws(() => normalizeSvg(wrap('<style>.a{fill:#ff0000}</style><path class="a"/>')), /niet toegestaan/);
});

test("regressie: ruis van editors en een > in een attribuutwaarde", () => {
  const raw = `<?xml version="1.0"?><svg xmlns='http://www.w3.org/2000/svg' width='48' height='48' ${VB} data-x=">" ` +
    `xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" inkscape:version="1.0">` +
    `<title>t</title><desc>d</desc><metadata><x/></metadata>` +
    `<path d="M1 1" data-fill="blue" inkscape:label="a" sodipodi:nodetypes="cc"/></svg>`;
  const { svg, colors } = normalizeSvg(raw);
  assert.equal(svg, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M1 1"/></svg>`);
  assert.deepEqual(colors, []);
});

test("regressie: misvormde XML en tekstinhoud worden geweigerd", () => {
  assert.throws(() => normalizeSvg(wrap("<path>")), /ongeldige XML/);
  assert.throws(() => normalizeSvg(wrap("<g>tekst</g>")), /tekstinhoud/);
  assert.throws(() => normalizeSvg(`<!DOCTYPE svg [<!ENTITY a "b">]>${wrap("")}`), /DOCTYPE/);
  assert.throws(() => normalizeSvg(wrap("") + "<svg/>"), /ongeldige XML|geen <svg>/);
});

test("regressie: uitvoer is deterministisch, ge-escaped en zelfsluitend", () => {
  const { svg } = normalizeSvg(wrap('<g>\n  <path d="M1 1" id="a&amp;b"/>\n  <g></g>\n</g>'));
  assert.equal(svg, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g><path d="M1 1" id="a&amp;b"/><g/></g></svg>');
});

test("regressie ronde 2: escapes en commentaar in attribuutwaarden worden geweigerd", () => {
  const probes = [
    '<path fill="\\75rl(http://x/y)"/>',
    '<path fill="u\\72l(http://x/y)"/>',
    '<path fill="url/**/(http://x/y)"/>',
    '<path clip-path="\\75rl(http://x/y#a)"/>',
  ];
  for (const p of probes) assert.throws(() => normalizeSvg(wrap(p)), /niet toegestaan/, p);
});

test("regressie ronde 2: ongeldige kleurwaarden worden geweigerd", () => {
  assert.throws(() => normalizeSvg(wrap('<path fill="javascript:alert(1)"/>')), /ongeldige kleurwaarde/);
  assert.throws(() => normalizeSvg(wrap('<path style="fill:expression(alert(1))"/>')), /ongeldige kleurwaarde/);
  assert.throws(() => normalizeSvg(wrap('<path stroke="#12"/>')), /ongeldige kleurwaarde/);
  assert.throws(() => normalizeSvg(wrap('<path fill="url(#g) javascript:x"/>')), /fallback/);
  assert.throws(() => normalizeSvg(wrap('<path clip-path="url(http://x/y#a)"/>')), /url\(#id\)/);
  assert.throws(() => normalizeSvg(wrap('<path opacity="url(#a)"/>')), /url\(\) is hier niet toegestaan/);
});

test("regressie ronde 2: geldige kleurwaarden blijven werken", () => {
  const { svg, colors } = normalizeSvg(wrap(
    '<path fill="rgb(1,2,3)"/><path fill="#abc"/><path fill="red"/><path stroke="url(#g)"/>' +
    '<path fill="url(#g) none"/><path fill="url(#g) #FF0000"/><path clip-path="url(#c)"/>' +
    '<path style="fill:RGBA(1, 2, 3, 0.5);stroke:#aabbccdd"/><path fill="Transparent" stroke="inherit"/>'));
  assert.ok(svg.includes('fill="url(#g) none"') && svg.includes('clip-path="url(#c)"'));
  assert.deepEqual(colors, ["#aabbcc", "#aabbccdd", "#ff0000", "red", "rgb(1,2,3)", "rgba(1, 2, 3, 0.5)"]);
});
