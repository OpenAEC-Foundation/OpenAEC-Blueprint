import { tokenValue } from "./load.mjs";

// Frappe Desk-variabele → tokenpad (zonder light/dark-segment).
const DESK_THEMED = {
  "--bg-color": "color.surface.bg",
  "--fg-color": "color.surface.panel",
  "--card-bg": "color.surface.panel",
  "--navbar-bg": "color.surface.panel",
  "--subtle-fg": "color.surface.muted",
  "--text-color": "color.text.primary",
  "--text-light": "color.text.secondary",
  "--text-muted": "color.text.muted",
  "--border-color": "color.border.default",
  "--dark-border-color": "color.border.strong",
};

function themed(leaves) {
  const map = new Map(leaves.map((l) => [l.path.join("."), l.value]));
  return Object.entries(DESK_THEMED).map(([v, p]) => {
    if (!map.has(p)) throw new Error(`Token ${p} ontbreekt voor ${v}`);
    return `  ${v}: ${map.get(p)};`;
  }).join("\n");
}

export function renderFrappeCss(tokens, fonts) {
  const amber = tokenValue(tokens, "color.brand.amber");
  const hover = tokenValue(tokens, "color.brand.primary-hover");
  const body = tokenValue(tokens, "font.family.body");
  const heading = tokenValue(tokens, "font.family.heading");
  const faces = fonts.map((f) => `@font-face {
  font-family: "${f.family}";
  src: url("/assets/openaec_theme/fonts/${f.file}") format("truetype");
  font-weight: ${f.weight};
  font-style: normal;
  font-display: swap;
}`).join("\n\n");
  return `${faces}

:root,
[data-theme="light"] {
  --primary: ${amber};
  --primary-color: ${amber};
  --btn-primary: ${amber};
  --primary-hover: ${hover};
  --font-stack: ${body};
${themed(tokens.light)}
}

[data-theme="dark"] {
${themed(tokens.dark)}
}

h1, h2, h3, h4, h5, h6,
.page-title .title-text,
.navbar-brand {
  font-family: ${heading};
}
`;
}
