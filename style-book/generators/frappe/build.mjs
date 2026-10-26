import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { loadTokens } from "../tokens/load.mjs";
import { renderFrappeCss } from "../tokens/frappe-css.mjs";
import { writeGenerated } from "../lib/write.mjs";

const FONTS = [
  { family: "Inter", file: "Inter-Regular.ttf", weight: 400 },
  { family: "Inter", file: "Inter-Medium.ttf", weight: 500 },
  { family: "Inter", file: "Inter-SemiBold.ttf", weight: 600 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Medium.ttf", weight: 500 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Bold.ttf", weight: 700 },
  { family: "JetBrains Mono", file: "JetBrainsMono-Regular.ttf", weight: 400 },
];

export function symbolSource(root) {
  const moved = join(root, "design", "logos", "foundation", "openaec-symbol-transparent.svg");
  return existsSync(moved) ? moved : join(root, "brandbook", "assets", "logo", "svg", "openaec-symbol-transparent.svg");
}

export function buildFrappeTheme(root) {
  const app = join(root, "frappe", "openaec_theme", "openaec_theme", "public");
  const out = [writeGenerated(join(app, "css", "openaec_theme.css"),
    renderFrappeCss(loadTokens(join(root, "design", "tokens")), FONTS))];
  mkdirSync(join(app, "fonts"), { recursive: true });
  for (const f of readdirSync(join(root, "design", "fonts")).sort()) {
    copyFileSync(join(root, "design", "fonts", f), join(app, "fonts", f));
    out.push(join(app, "fonts", f));
  }
  out.push(writeGenerated(join(app, "images", "openaec-symbol.svg"), readFileSync(symbolSource(root), "utf8")));
  return out;
}
