import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, extname } from "node:path";

export const GENERATED_NOTICE =
  "GEGENEREERD door generators/ uit design/ — niet met de hand bewerken.";

export function headerFor(filePath) {
  const ext = extname(filePath);
  if ([".rs", ".ts", ".tsx", ".js", ".mjs"].includes(ext)) return `// @generated ${GENERATED_NOTICE}\n\n`;
  if (ext === ".css") return `/* @generated ${GENERATED_NOTICE} */\n\n`;
  if (ext === ".py") return `# @generated ${GENERATED_NOTICE}\n\n`;
  return "";
}

export function normalizeText(text) {
  const lf = text.replace(/\r\n?/g, "\n");
  return lf.endsWith("\n") ? lf : lf + "\n";
}

export function writeGenerated(filePath, content) {
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, normalizeText(headerFor(filePath) + content), "utf8");
  return filePath;
}
