import { test } from "node:test";
import assert from "node:assert/strict";
import { renderSharedTabsRust } from "../ribbons/rust.mjs";

test("gedeelde tabs worden als ruwe strings ingebed, gesorteerd op naam", () => {
  const rs = renderSharedTabsRust([["viewer3d", 'shared = "viewer3d"\n'], ["ifc", 'shared = "ifc"\n']]);
  assert.match(rs, /\("ifc", r#"shared = "ifc"\n"#\),\n    \("viewer3d"/);
});
