export function renderI18nRust({ nl, en }) {
  const keys = [...nl.keys()].sort();
  const arms = (map) => keys.map((k) => `        ${JSON.stringify(k)} => Some(${JSON.stringify(map.get(k))}),`).join("\n");
  return `/// Alle gedeelde sleutels (zonder het voorvoegsel \`openaec.\`).
pub const KEYS: &[&str] = &[
${keys.map((k) => `    ${JSON.stringify(k)},`).join("\n")}
];

pub(crate) fn nl(key: &str) -> Option<&'static str> {
    match key {
${arms(nl)}
        _ => None,
    }
}

pub(crate) fn en(key: &str) -> Option<&'static str> {
    match key {
${arms(en)}
        _ => None,
    }
}
`;
}
