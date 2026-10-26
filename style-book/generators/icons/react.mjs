export function exportName(id) {
  return id.split(/[/-]/).map((p, i) => (i === 0 ? p : p[0].toUpperCase() + p.slice(1))).join("");
}

export function renderIconsTs(icons) {
  let out = "";
  for (const icon of icons) {
    out += `/** ${icon.label.nl} — ${icon.label.en} (\`${icon.id}\`) */\n`;
    out += `export const ${exportName(icon.id)} = ${JSON.stringify(icon.svg)};\n`;
  }
  out += `\nexport type IconId = ${icons.map((i) => JSON.stringify(i.id)).join(" | ")};\n`;
  out += `\nexport const iconIds: readonly IconId[] = [${icons.map((i) => JSON.stringify(i.id)).join(", ")}];\n`;
  return out;
}

export function renderIconsByIdTs(icons) {
  let out = `import type { IconId } from "./icons";\nimport {\n`;
  for (const i of icons) out += `  ${exportName(i.id)},\n`;
  out += `} from "./icons";\n\n/** Alle iconen per id. Importeer dit alleen als je iconen dynamisch op id opzoekt. */\nexport const iconsById: Record<IconId, string> = {\n`;
  for (const i of icons) out += `  ${JSON.stringify(i.id)}: ${exportName(i.id)},\n`;
  return out + "};\n";
}
