import opentype from "opentype.js";

// Lockup: app-tegel + weergavenaam als paden. "Open" (als eerste woord) in amber.
export function buildLockupSvg({ tileSvg, displayName, mode, colors, fontFile }) {
  const font = opentype.loadSync(fontFile);
  const height = 128;
  const fontSize = 64;
  const baseline = 86;
  let x = height + 32;
  const words = displayName.startsWith("Open ") ? [["Open", colors.accent], [displayName.slice(5), colors.text[mode]]]
    : [[displayName, colors.text[mode]]];
  let paths = "";
  for (const [i, [text, fill]] of words.entries()) {
    const t = i > 0 ? " " + text : text;
    const p = font.getPath(t, x, baseline, fontSize);
    paths += `<path d="${p.toPathData(2)}" fill="${fill}"/>`;
    x += font.getAdvanceWidth(t, fontSize);
  }
  const tile = tileSvg.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">',
    `<svg x="0" y="0" width="${height}" height="${height}" viewBox="0 0 1024 1024">`);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${Math.ceil(x)} ${height}">${tile}${paths}</svg>`;
}
