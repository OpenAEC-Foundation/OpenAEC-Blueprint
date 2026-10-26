import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { headerFor, normalizeText, writeGenerated } from "../lib/write.mjs";

test("normalizeText zet CRLF en CR om naar LF en eindigt met één newline", () => {
  assert.equal(normalizeText("a\r\nb\rc"), "a\nb\nc\n");
  assert.equal(normalizeText("a\n"), "a\n");
});

test("headerFor kiest commentaarstijl per bestandstype", () => {
  assert.match(headerFor("x.rs"), /^\/\/ @generated /);
  assert.match(headerFor("x.ts"), /^\/\/ @generated /);
  assert.match(headerFor("x.css"), /^\/\* @generated .* \*\//);
  assert.match(headerFor("x.py"), /^# @generated /);
  assert.equal(headerFor("x.json"), "");
  assert.equal(headerFor("x.svg"), "");
});

test("writeGenerated schrijft UTF-8 zonder BOM, met header en mappen", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-write-"));
  const file = join(dir, "sub", "a.rs");
  writeGenerated(file, "pub const X: &str = \"Kopiëren\";\r\n");
  const bytes = readFileSync(file);
  assert.notDeepEqual([...bytes.subarray(0, 3)], [0xef, 0xbb, 0xbf]);
  const text = bytes.toString("utf8");
  assert.ok(text.startsWith("// @generated "));
  assert.ok(text.includes("Kopiëren"));
  assert.ok(!text.includes("\r"));
});
