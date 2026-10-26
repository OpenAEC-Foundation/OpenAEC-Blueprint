import { test } from "node:test";
import assert from "node:assert/strict";
import { copyFileSync, cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import { PNG } from "pngjs";
import { TILE, buildTileInner, buildTileSvg } from "../logos/tile.mjs";
import { buildLockupSvg } from "../logos/lockup.mjs";
import { buildLogos } from "../logos/build.mjs";
import { loadTokens, tokenValue } from "../tokens/load.mjs";
import { packIco } from "../logos/ico.mjs";
import { packIcns } from "../logos/icns.mjs";
import { repoPath } from "../lib/paths.mjs";

const PICTO = readFileSync(repoPath("design", "logos", "apps", "openaec-template.svg"), "utf8");
const COLORS = { tile: "#36363E", glyph: "#D97706" };
const render = (svg, size) => new Resvg(svg, { fitTo: { mode: "width", value: size } }).render();

test("tegel volgt de regels: kleur, afronding en 75%-pictogram", () => {
  const svg = buildTileSvg(PICTO, COLORS, 1024);
  assert.match(svg, /<rect width="1024" height="1024" rx="225\.28" fill="#36363E"\/>/);
  assert.match(svg, /<g transform="translate\(128 128\) scale\(32\)" color="#D97706">/);
  assert.equal(TILE.glyph, 0.75);
});

test("pictogram blijft binnen het 75%-vak", () => {
  const img = render(buildTileSvg(PICTO, { tile: "#000000", glyph: "#FFFFFF" }, 256), 256);
  const px = img.pixels;
  for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
    const inBox = x >= 32 && x < 224 && y >= 32 && y < 224;
    const i = (y * 256 + x) * 4;
    if (!inBox && px[i] > 128 && px[i + 1] > 128 && px[i + 2] > 128) assert.fail(`lichte pixel buiten vak op ${x},${y}`);
  }
});

test("ICO- en ICNS-containers zijn geldig", () => {
  const png = (s) => ({ size: s, data: Buffer.from(render(buildTileSvg(PICTO, COLORS, s), s).asPng()) });
  const ico = packIco([png(16), png(32), png(256)]);
  assert.equal(ico.readUInt16LE(2), 1);
  assert.equal(ico.readUInt16LE(4), 3);
  assert.equal(ico[6 + 2 * 16], 0, "256 px wordt als 0 opgeslagen");
  const icns = packIcns([png(16), png(32), png(128), png(256), png(512), png(1024)]);
  assert.equal(icns.subarray(0, 4).toString("ascii"), "icns");
  assert.equal(icns.readUInt32BE(4), icns.length);
});

test("snapshots op 16, 32 en 256 px", () => {
  const dir = repoPath("generators", "test", "snapshots", "logos");
  mkdirSync(dir, { recursive: true });
  for (const size of [16, 32, 256]) {
    const actual = PNG.sync.read(Buffer.from(render(buildTileSvg(PICTO, COLORS, size), size).asPng()));
    const file = join(dir, `openaec-template.${size}.png`);
    if (process.env.UPDATE_SNAPSHOTS || !existsSync(file)) {
      if (!process.env.UPDATE_SNAPSHOTS) assert.fail(`snapshot ontbreekt: ${file} — draai met UPDATE_SNAPSHOTS=1`);
      writeFileSync(file, PNG.sync.write(actual));
      continue;
    }
    const expected = PNG.sync.read(readFileSync(file));
    let diff = 0;
    for (let i = 0; i < actual.data.length; i += 4) {
      if ([0, 1, 2, 3].some((c) => Math.abs(actual.data[i + c] - expected.data[i + c]) > 2)) diff++;
    }
    assert.ok(diff * 200 <= size * size, `${size}px wijkt af (${diff} pixels)`);
  }
});

const TOKENS = loadTokens(repoPath("design", "tokens"));
const BRAND = {
  tile: tokenValue(TOKENS, "color.brand.deep-forge"),
  glyph: tokenValue(TOKENS, "color.brand.amber"),
  accent: tokenValue(TOKENS, "color.brand.amber"),
  text: { light: tokenValue(TOKENS, "color.brand.deep-forge"), dark: tokenValue(TOKENS, "color.brand.blueprint-white") },
};
const FONT = repoPath("design", "fonts", "SpaceGrotesk-Bold.ttf");
const lockup = (displayName, mode) => buildLockupSvg({
  tileInner: buildTileInner(PICTO, BRAND, 1024), displayName, mode, colors: BRAND, fontFile: FONT,
});
const pathFills = (svg) => [...svg.matchAll(/<path d="[^"]*" fill="([^"]*)"\/>/g)].map((m) => m[1]);

test("buildTileSvg is de omhulling van buildTileInner", () => {
  const inner = buildTileInner(PICTO, COLORS, 512);
  assert.equal(buildTileSvg(PICTO, COLORS, 512),
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${inner}</svg>`);
});

for (const mode of ["light", "dark"]) {
  test(`lockup ${mode}: tegel van 128 px, "Open" amber, rest in tekstkleur`, () => {
    const svg = lockup("Open Template", mode);
    assert.match(svg, /<svg x="0" y="0" width="128" height="128" viewBox="0 0 1024 1024"><rect width="1024" height="1024" rx="225\.28" fill="#36363E"\/>/i);
    assert.ok(svg.includes(buildTileInner(PICTO, BRAND, 1024)), "tegelbinnenwerk volledig aanwezig");
    assert.match(svg, /^<svg xmlns="http:\/\/www\.w3\.org\/2000\/svg" viewBox="0 0 \d+ 128">/);
    assert.deepEqual(pathFills(svg), [BRAND.accent, BRAND.text[mode]]);
  });
}

for (const name of ["OpenAEC Reports", "Y-Next"]) {
  for (const mode of ["light", "dark"]) {
    test(`lockup ${mode}: "${name}" heeft één tekstkleur zonder amber woord`, () => {
      const fills = pathFills(lockup(name, mode));
      assert.deepEqual(fills, [BRAND.text[mode]]);
      assert.ok(!fills.includes(BRAND.accent));
    });
  }
}

test("ICO: map en afbeeldingen komen exact terug", () => {
  const sizes = [16, 32, 48, 64, 128, 256];
  const input = sizes.map((s) => ({ size: s, data: Buffer.from(render(buildTileSvg(PICTO, COLORS, s), s).asPng()) }));
  const ico = packIco(input);
  assert.equal(ico.readUInt16LE(0), 0);
  assert.equal(ico.readUInt16LE(2), 1);
  assert.equal(ico.readUInt16LE(4), input.length);
  input.forEach(({ size, data }, i) => {
    const e = 6 + 16 * i;
    const dim = size === 256 ? 0 : size;
    assert.equal(ico[e], dim, `breedte van ${size}`);
    assert.equal(ico[e + 1], dim, `hoogte van ${size}`);
    assert.equal(ico.readUInt16LE(e + 4), 1, "planes");
    assert.equal(ico.readUInt16LE(e + 6), 32, "bpp");
    const len = ico.readUInt32LE(e + 8);
    const offset = ico.readUInt32LE(e + 12);
    assert.equal(len, data.length);
    assert.ok(ico.subarray(offset, offset + len).equals(data), `PNG-data van ${size} komt terug`);
  });
});

test("ICNS: type per grootte, chunklengte en payload kloppen", () => {
  const types = { 16: "icp4", 32: "icp5", 64: "icp6", 128: "ic07", 256: "ic08", 512: "ic09", 1024: "ic10" };
  const input = Object.keys(types).map(Number).map((s) => ({ size: s, data: Buffer.from(render(buildTileSvg(PICTO, COLORS, s), s).asPng()) }));
  const icns = packIcns(input);
  assert.equal(icns.readUInt32BE(4), icns.length);
  let pos = 8;
  for (const { size, data } of input) {
    assert.equal(icns.subarray(pos, pos + 4).toString("ascii"), types[size], `type voor ${size}`);
    const len = icns.readUInt32BE(pos + 4);
    assert.equal(len, 8 + data.length, `chunklengte voor ${size}`);
    assert.ok(icns.subarray(pos + 8, pos + len).equals(data), `payload voor ${size}`);
    pos += len;
  }
  assert.equal(pos, icns.length, "geen restbytes");
  assert.throws(() => packIcns([{ size: 20, data: Buffer.alloc(1) }]), /Geen ICNS-type voor 20px/);
});

test("buildLogos schrijft de volledige set voor een app", () => {
  const root = mkdtempSync(join(tmpdir(), "oa-logos-"));
  cpSync(repoPath("design", "tokens"), join(root, "design", "tokens"), { recursive: true });
  mkdirSync(join(root, "design", "fonts"), { recursive: true });
  copyFileSync(FONT, join(root, "design", "fonts", "SpaceGrotesk-Bold.ttf"));
  mkdirSync(join(root, "design", "logos", "apps"), { recursive: true });
  writeFileSync(join(root, "design", "logos", "apps", "demo.svg"), PICTO);
  writeFileSync(join(root, "design", "apps.toml"), `
[[app]]
id = "demo"
display_name = "Open Demo"
category = 2
logo = "demo"

[[app]]
id = "zonder-logo"
display_name = "Zonder Logo"
category = 2
`);
  const written = buildLogos(root);
  assert.deepEqual(written, [join(root, "logos", "demo")]);
  const expected = [
    "favicon.ico", "favicon.svg",
    ...[1024, 128, 16, 256, 32, 48, 512, 64].map((s) => `icon-${s}.png`),
    "icon.icns", "icon.ico", "lockup-dark.svg", "lockup-light.svg",
    "web-192.png", "web-512.png", "web-maskable-512.png",
  ].sort();
  assert.deepEqual(readdirSync(join(root, "logos", "demo")).sort(), expected);
  assert.ok(!existsSync(join(root, "logos", "zonder-logo")), "app zonder logo krijgt geen set");
});
