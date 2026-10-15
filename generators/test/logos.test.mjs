import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import { PNG } from "pngjs";
import { TILE, buildTileSvg } from "../logos/tile.mjs";
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
