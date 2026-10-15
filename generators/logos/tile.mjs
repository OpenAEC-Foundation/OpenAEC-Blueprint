import { normalizeSvg } from "../icons/normalize.mjs";

export const TILE = { radius: 0.22, glyph: 0.75 };

const fmt = (n) => String(Math.round(n * 100) / 100);

// Binnenwerk van de tegel (rect + pictogram) zonder omhullende <svg>; coördinaten voor een vierkant van `size`.
export function buildTileInner(pictogramSvg, colors, size = 1024) {
  const { svg } = normalizeSvg(pictogramSvg);
  const inner = svg.replace(/^<svg\b[^>]*>/, "").replace(/<\/svg>\s*$/, "");
  const rootAttrs = /^<svg\b([^>]*)>/.exec(svg)[1]
    .replace(/\s(xmlns|viewBox)="[^"]*"/g, "")
    .trim();
  const glyph = size * TILE.glyph;
  const offset = (size - glyph) / 2;
  const scale = glyph / 24;
  return `<rect width="${size}" height="${size}" rx="${fmt(size * TILE.radius)}" fill="${colors.tile}"/>` +
    `<g transform="translate(${fmt(offset)} ${fmt(offset)}) scale(${fmt(scale)})" color="${colors.glyph}">` +
    `<g ${rootAttrs}>${inner}</g></g>`;
}

export function buildTileSvg(pictogramSvg, colors, size = 1024) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}">` +
    `${buildTileInner(pictogramSvg, colors, size)}</svg>`;
}
