import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { repoPath } from "../lib/paths.mjs";

test("packages/tokens bouwt uit design/tokens en kopieert de JSON mee", () => {
  execFileSync(process.execPath, ["build.js"], { cwd: repoPath("packages", "tokens") });
  const css = readFileSync(repoPath("packages", "tokens", "dist", "tokens.css"), "utf8");
  assert.match(css, /--color-brand-amber:\s*#D97706/i);
  assert.ok(existsSync(repoPath("packages", "tokens", "tokens", "colors.json")));
  assert.ok(existsSync(repoPath("packages", "tokens", "extensions", "warmteverlies.json")));
});

test("tokens.css bevat geen CSS-variabelen die (via een keten) naar zichzelf verwijzen", () => {
  execFileSync(process.execPath, ["build.js"], { cwd: repoPath("packages", "tokens") });
  const css = readFileSync(repoPath("packages", "tokens", "dist", "tokens.css"), "utf8");
  // Per regelblok (:root, [data-theme=dark], media-blok) de var()-verwijzingen volgen.
  for (const block of css.split("}")) {
    const refs = new Map();
    for (const m of block.matchAll(/(--[\w-]+)\s*:\s*var\((--[\w-]+)\)/g)) refs.set(m[1], m[2]);
    for (const start of refs.keys()) {
      const seen = new Set([start]);
      let cur = refs.get(start);
      while (cur && refs.has(cur)) {
        assert.ok(!seen.has(cur), `${start} verwijst via ${[...seen].join(" → ")} naar zichzelf`);
        seen.add(cur);
        cur = refs.get(cur);
      }
      assert.notEqual(cur, start, `${start} verwijst naar zichzelf`);
    }
  }
  // De thema-tekst- en randkleuren hebben in het lichte :root-blok een echte kleurwaarde.
  const root = css.slice(css.indexOf(":root {"), css.indexOf("}", css.indexOf(":root {")));
  for (const name of ["text-secondary", "text-muted", "text-inverse", "border-strong", "border-focus"]) {
    assert.match(root, new RegExp(`--color-${name}:\\s*#[0-9A-Fa-f]{6}`), `--color-${name} mist een kleur in :root`);
  }
});
