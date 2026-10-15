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
