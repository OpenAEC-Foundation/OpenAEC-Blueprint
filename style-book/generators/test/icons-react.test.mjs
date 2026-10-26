import { test } from "node:test";
import assert from "node:assert/strict";
import { exportName, renderIconsByIdTs, renderIconsTs } from "../icons/react.mjs";

const icons = [
  { id: "edit/undo", label: { nl: "Ongedaan maken", en: "Undo" }, svg: "<svg>u</svg>" },
  { id: "view/fit-all", label: { nl: "Passend", en: "Fit all" }, svg: "<svg>f`${x}</svg>" },
];

test("exportName maakt camelCase", () => {
  assert.equal(exportName("view/fit-all"), "viewFitAll");
  assert.equal(exportName("edit/undo"), "editUndo");
});

test("renderIconsTs exporteert per icoon een const en het IconId-type", () => {
  const ts = renderIconsTs(icons);
  assert.match(ts, /export const editUndo = "<svg>u<\/svg>";/);
  assert.ok(ts.includes(JSON.stringify("<svg>f`${x}</svg>")), "SVG wordt als JSON-string ge-escaped");
  assert.match(ts, /export type IconId = "edit\/undo" \| "view\/fit-all";/);
});

test("renderIconsByIdTs koppelt id aan export", () => {
  const ts = renderIconsByIdTs(icons);
  assert.match(ts, /"view\/fit-all": viewFitAll,/);
});
