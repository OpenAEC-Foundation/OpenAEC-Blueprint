import { test } from "node:test";
import assert from "node:assert/strict";
import { rawString, renderIconsRust, variantName } from "../icons/rust.mjs";

const icon = (id, svg = "<svg/>") => ({ id, label: { nl: "Kopiëren", en: "Copy" }, tags: [], svg });

test("variantName maakt PascalCase", () => {
  assert.equal(variantName("view/fit-all"), "ViewFitAll");
});

test("rawString kiest genoeg hekjes", () => {
  assert.equal(rawString('a"b'), 'r#"a"b"#');
  assert.equal(rawString('a"#b'), 'r##"a"#b"##');
});

test("renderIconsRust bevat enum, ALL, id, svg en from_id", () => {
  const rs = renderIconsRust([icon("edit/copy"), icon("view/fit-all", "<svg>2</svg>")]);
  assert.match(rs, /pub enum Icon \{\n    EditCopy,\n    ViewFitAll,\n\}/);
  assert.match(rs, /"edit\/copy" => Some\(Icon::EditCopy\)/);
  assert.match(rs, /Icon::EditCopy => "Kopiëren"/);
});

test("botsende variantnamen worden geweigerd", () => {
  // Het id-patroon maakt echte botsingen vrijwel onmogelijk; de generator vangt ze toch af.
  assert.throws(() => renderIconsRust([icon("a/b"), icon("a/b", "<svg>x</svg>")]), /zelfde Rust-naam/);
});
