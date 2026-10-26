export function variantName(id) {
  return id.split(/[/-]/).map((p) => p[0].toUpperCase() + p.slice(1)).join("");
}

export function rawString(s) {
  let hashes = 1;
  while (s.includes('"' + "#".repeat(hashes))) hashes++;
  const h = "#".repeat(hashes);
  return `r${h}"${s}"${h}`;
}

export function renderIconsRust(icons) {
  const names = new Map();
  for (const i of icons) {
    const v = variantName(i.id);
    if (names.has(v)) throw new Error(`${i.id} en ${names.get(v)} krijgen dezelfde Rust-naam ${v} (zelfde Rust-naam)`);
    names.set(v, i.id);
  }
  const arm = (fn) => icons.map((i) => `            Icon::${variantName(i.id)} => ${fn(i)},`).join("\n");
  return `/// Alle OpenAEC-iconen. Bron: \`design/icons/\`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Icon {
${icons.map((i) => `    ${variantName(i.id)},`).join("\n")}
}

impl Icon {
    pub const ALL: &'static [Icon] = &[
${icons.map((i) => `        Icon::${variantName(i.id)},`).join("\n")}
    ];

    /// Id zoals in \`icons.toml\` en \`ribbon.toml\`, bijv. \`"edit/undo"\`.
    pub const fn id(self) -> &'static str {
        match self {
${arm((i) => JSON.stringify(i.id))}
        }
    }

    /// Genormaliseerde SVG (viewBox 0 0 24 24, primaire kleur \`currentColor\`).
    pub const fn svg(self) -> &'static str {
        match self {
${arm((i) => rawString(i.svg))}
        }
    }

    pub const fn label_nl(self) -> &'static str {
        match self {
${arm((i) => JSON.stringify(i.label.nl))}
        }
    }

    pub const fn label_en(self) -> &'static str {
        match self {
${arm((i) => JSON.stringify(i.label.en))}
        }
    }

    /// \`true\` als het icoon eigen kleuren heeft naast \`currentColor\` (tag \`color\`).
    pub const fn has_own_colors(self) -> bool {
        match self {
${arm((i) => String(i.tags.includes("color")))}
        }
    }

    pub fn from_id(id: &str) -> Option<Icon> {
        match id {
${icons.map((i) => `            ${JSON.stringify(i.id)} => Some(Icon::${variantName(i.id)}),`).join("\n")}
            _ => None,
        }
    }
}
`;
}
