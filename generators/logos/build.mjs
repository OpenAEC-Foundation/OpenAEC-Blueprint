import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import { loadApps } from "../apps/load.mjs";
import { loadTokens, tokenValue } from "../tokens/load.mjs";
import { buildTileSvg } from "./tile.mjs";
import { packIco } from "./ico.mjs";
import { packIcns } from "./icns.mjs";
import { buildLockupSvg } from "./lockup.mjs";

const PNG_SIZES = [16, 32, 48, 64, 128, 256, 512, 1024];

export function buildLogos(root) {
  const tokens = loadTokens(join(root, "design", "tokens"));
  const colors = {
    tile: tokenValue(tokens, "color.brand.deep-forge"),
    glyph: tokenValue(tokens, "color.brand.amber"),
    accent: tokenValue(tokens, "color.brand.amber"),
    text: { light: tokenValue(tokens, "color.brand.deep-forge"), dark: tokenValue(tokens, "color.brand.blueprint-white") },
  };
  const fontFile = join(root, "design", "fonts", "SpaceGrotesk-Bold.ttf");
  const written = [];
  for (const app of loadApps(join(root, "design", "apps.toml")).filter((a) => a.logo)) {
    const picto = readFileSync(join(root, "design", "logos", "apps", `${app.logo}.svg`), "utf8");
    const out = join(root, "logos", app.id);
    mkdirSync(out, { recursive: true });
    const tile = buildTileSvg(picto, colors, 1024);
    const png = {};
    for (const s of PNG_SIZES) {
      png[s] = Buffer.from(new Resvg(tile, { fitTo: { mode: "width", value: s } }).render().asPng());
      writeFileSync(join(out, `icon-${s}.png`), png[s]);
    }
    writeFileSync(join(out, "icon.ico"), packIco([16, 32, 48, 64, 128, 256].map((s) => ({ size: s, data: png[s] }))));
    writeFileSync(join(out, "icon.icns"), packIcns([16, 32, 64, 128, 256, 512, 1024].map((s) => ({ size: s, data: png[s] }))));
    writeFileSync(join(out, "favicon.svg"), tile);
    writeFileSync(join(out, "favicon.ico"), packIco([16, 32, 48].map((s) => ({ size: s, data: png[s] }))));
    for (const s of [192, 512]) {
      writeFileSync(join(out, `web-${s}.png`), Buffer.from(new Resvg(tile, { fitTo: { mode: "width", value: s } }).render().asPng()));
    }
    // Maskable: volle tegel zonder afronding, zodat het platform zelf kan afsnijden.
    const maskable = tile.replace(/rx="[^"]*"/, 'rx="0"');
    writeFileSync(join(out, "web-maskable-512.png"), Buffer.from(new Resvg(maskable, { fitTo: { mode: "width", value: 512 } }).render().asPng()));
    for (const mode of ["light", "dark"]) {
      writeFileSync(join(out, `lockup-${mode}.svg`), buildLockupSvg({ tileSvg: tile, displayName: app.display_name, mode, colors, fontFile }));
    }
    written.push(out);
  }
  return written;
}
