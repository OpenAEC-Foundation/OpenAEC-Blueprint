import { test } from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { runAll } from "../generate.mjs";
import { ROOT } from "../lib/paths.mjs";

const hash = (files) => files.map((f) => createHash("sha256").update(readFileSync(f)).digest("hex")).join();

test("twee keer genereren geeft byte-gelijke bestanden zonder CR", async () => {
  const first = await runAll(ROOT);
  const h1 = hash(first);
  const second = await runAll(ROOT);
  assert.equal(hash(second), h1);
  for (const f of second.filter((x) => /\.(rs|ts|css|json|svg|py)$/.test(x))) {
    assert.ok(!readFileSync(f).includes(0x0d), `${f} bevat CR`);
  }
});
