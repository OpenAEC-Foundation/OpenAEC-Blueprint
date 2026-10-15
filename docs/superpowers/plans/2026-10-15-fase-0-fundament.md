# Fase 0 — UI-fundament: implementatieplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eén bron (`design/`) in OpenAEC-style-book voor tokens, iconen, i18n, gedeelde ribbon-tabs, fonts en logo's, met generators naar Rust-crates, React-packages, een Frappe-thema en app-logo-sets — klaar voor release `v0.1.0`.

**Architecture:** Handwerk gebeurt alleen in `design/`. Node-generators (`generators/`, ESM, `node:test`) lezen `design/` en schrijven gegenereerde code naar `crates/`, `packages/` en `frappe/`; die uitvoer wordt gecommit en CI controleert dat opnieuw genereren geen verschil geeft. Binaire logo-sets (`logos/`) zijn build-uitvoer en gaan als zip mee met de release. Ribbon-validatie zit in de Rust-crate `openaec-ribbon` (bibliotheek + CLI), zodat iced-apps hem later in `build.rs` kunnen hergebruiken.

**Tech Stack:** Node 24 / npm 11 workspaces, `smol-toml`, `@resvg/resvg-js`, `opentype.js`, `pngjs`; Rust stable (1.94) workspace met `serde`, `toml`, `resvg` (dev); Python 3.12 (`unittest`) voor de Frappe-app; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-15-ui-fundament-design.md`

## Global Constraints

- Nergens in repo-inhoud of commitberichten: namen van externe rekensoftware of concurrerende producten, en geen verwijzingen naar gesprekken met een assistent.
- Schrijfwijze "OpenAEC" (één woord); geen verwijzingen naar 3BM.
- Construction Amber `#D97706` nooit als achtergrondvlak — ook niet als app-tegel.
- App-tegel: Deep Forge `#36363E`, hoekafronding 22% van de breedte, pictogram amber, 75% van de breedte, gecentreerd.
- Iconen: viewBox `0 0 24 24`, primaire kleur `currentColor`; eigen kleuren alleen met tag `color`.
- Gegenereerde tekstbestanden: UTF-8 zonder BOM, LF, eindigen met één newline, header `@generated` waar het bestandstype commentaar toestaat.
- Deterministische uitvoer: sorteren op codepunt (`a < b`), geen tijdstempels of absolute paden in gegenereerde bestanden.
- Licenties: code MIT; merk-assets CC BY-SA 4.0; fonts SIL OFL 1.1 met licentietekst ernaast.
- Geen materiaal (iconen, code) uit OpenCADStudio (GPL-3.0, externe rechthebbende) vóór schriftelijke toestemming — zie Task 15.
- Eén versienummer voor alles: `0.1.0` in Cargo-workspace, alle `packages/*/package.json` en de Frappe-app.
- Werk op branch `ui-fundament`. Niet pushen of taggen zonder akkoord van de eigenaar. Elk commitbericht eindigt met `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Windows-checkout met CRLF** — opnieuw genereren op een Windows-machine moet byte-gelijke bestanden geven en `npm run check` mag geen verschil melden. (Test in Task 1 + `.gitattributes`; idempotentie-test in Task 12.)
2. **Kleuren in `style="…"`, hoofdletters of 3-cijferige hex** in een SVG — de tag `color` moet dan toch correct verplicht zijn. (Test in Task 4.)
3. **Niet-ASCII labels** (bijv. "Kopiëren") moeten ongeschonden in Rust, TypeScript en JSON terechtkomen. (Test in Task 8.)
4. **Typefout of onbekend veld in `ribbon.toml`** (bijv. `icn = …`) moet een fout met pad opleveren, niet stil genegeerd worden. (Test in Task 9.)
5. **Twee icoon-id's die naar dezelfde Rust-variant vertalen**, of hetzelfde SVG onder twee id's, moet de generator weigeren. (Tests in Task 4 en Task 7.)

---

## Bestandsstructuur na fase 0

```
package.json                     npm-workspaces + scripts generate/check/test
Cargo.toml                       Rust-workspace (crates/*)
.gitattributes                   LF voor tekst, binary voor png/ttf/ico/icns
.github/workflows/design.yml     CI
.github/workflows/release.yml    release op tag v*
design/
  tokens/*.json, tokens/extensions/*.json
  icons/<domein>/*.svg, icons/icons.toml
  i18n/{nl,en}/openaec.json
  ribbons/viewer3d.toml
  logos/foundation/*.svg, logos/apps/<app-id>.svg
  fonts/*.ttf, fonts/OFL-*.txt
  components/README.md
  apps.toml
generators/
  package.json
  lib/{paths,write,toml}.mjs
  tokens/{load,rust,frappe-css}.mjs
  icons/{normalize,manifest,import,react,rust}.mjs
  i18n/{load,react,rust}.mjs
  ribbons/rust.mjs
  apps/load.mjs
  logos/{tile,ico,icns,lockup,build}.mjs
  frappe/build.mjs
  version/set-version.mjs
  generate.mjs, check.mjs
  test/*.test.mjs
packages/
  tokens/          (bestaand; leest nu design/tokens)
  icons/           (nieuw, @openaec/icons)
  i18n/            (nieuw, @openaec/i18n)
crates/
  openaec-tokens/  openaec-icons/  openaec-i18n/  openaec-ribbon/
frappe/openaec_theme/
docs/integratie.md
```

`packages/i18n` (`@openaec/i18n`) is een kleine aanvulling op de packagelijst in de spec: de React-kant heeft net als de Rust-kant (`openaec-i18n`) een eigen drager voor de gedeelde termen nodig. `crates/openaec-ribbon` vult de cratelijst aan om dezelfde reden voor de ribbon-validatie.

---

### Task 1: Werkruimte, generator-basis en regeleindes

**Files:**
- Create: `package.json`, `.gitattributes`, `generators/package.json`, `generators/lib/paths.mjs`, `generators/lib/write.mjs`, `generators/generate.mjs`, `generators/check.mjs`, `generators/test/write.test.mjs`
- Delete: `packages/ribbon/package-lock.json`, `packages/shell/package-lock.json`, `packages/tokens/package-lock.json`, `packages/ui-primitives/package-lock.json` (vervangen door één root-lockfile)

**Interfaces:**
- Produces: `ROOT: string` en `repoPath(...segments): string` uit `generators/lib/paths.mjs`; `writeGenerated(filePath: string, content: string): string`, `normalizeText(text: string): string`, `headerFor(filePath: string): string` uit `generators/lib/write.mjs`; `generate.mjs` met een `steps`-lijst van `[naam: string, run: (root: string) => Promise<string[]> | string[]]`.

- [ ] **Step 1: Root-`package.json` en generator-package aanmaken**

`package.json`:
```json
{
  "name": "openaec-style-book",
  "private": true,
  "workspaces": ["generators", "packages/*"],
  "scripts": {
    "generate": "node generators/generate.mjs",
    "check": "node generators/check.mjs",
    "test": "node --test \"generators/test/**/*.test.mjs\""
  },
  "engines": { "node": ">=24" }
}
```

`generators/package.json`:
```json
{
  "name": "@openaec/generators",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "smol-toml": "^1.3.1"
  }
}
```

- [ ] **Step 2: `.gitattributes` aanmaken**

```
* text=auto eol=lf
*.png binary
*.ico binary
*.icns binary
*.ttf binary
*.woff2 binary
*.pdf binary
```

- [ ] **Step 3: Failing test schrijven** — `generators/test/write.test.mjs`

```js
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
```

- [ ] **Step 4: Test draaien en zien falen**

Run: `npm install && npm test`
Expected: FAIL — `Cannot find module '../lib/write.mjs'`

- [ ] **Step 5: Implementatie** — `generators/lib/paths.mjs`

```js
import { fileURLToPath } from "node:url";
import { join } from "node:path";

export const ROOT = fileURLToPath(new URL("../../", import.meta.url));

export function repoPath(...segments) {
  return join(ROOT, ...segments);
}
```

`generators/lib/write.mjs`:
```js
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, extname } from "node:path";

export const GENERATED_NOTICE =
  "GEGENEREERD door generators/ uit design/ — niet met de hand bewerken.";

export function headerFor(filePath) {
  const ext = extname(filePath);
  if ([".rs", ".ts", ".tsx", ".js", ".mjs"].includes(ext)) return `// @generated ${GENERATED_NOTICE}\n\n`;
  if (ext === ".css") return `/* @generated ${GENERATED_NOTICE} */\n\n`;
  if (ext === ".py") return `# @generated ${GENERATED_NOTICE}\n\n`;
  return "";
}

export function normalizeText(text) {
  const lf = text.replace(/\r\n?/g, "\n");
  return lf.endsWith("\n") ? lf : lf + "\n";
}

export function writeGenerated(filePath, content) {
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, normalizeText(headerFor(filePath) + content), "utf8");
  return filePath;
}
```

`generators/generate.mjs`:
```js
import { pathToFileURL } from "node:url";
import { ROOT } from "./lib/paths.mjs";

// Elke stap: [naam, (root) => string[] | Promise<string[]>] — geeft geschreven bestanden terug.
// Latere tasks voegen bovenaan imports toe (zonder dubbelingen) en hieronder steps.push(...).
export const steps = [];

export async function runAll(root = ROOT) {
  const written = [];
  for (const [name, run] of steps) {
    const files = await run(root);
    console.log(`✓ ${name}: ${files.length} bestanden`);
    written.push(...files);
  }
  return written;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  runAll().catch((err) => {
    console.error(`✗ ${err.message}`);
    process.exit(1);
  });
}
```

`generators/check.mjs`:
```js
import { execFileSync } from "node:child_process";
import { runAll } from "./generate.mjs";
import { ROOT } from "./lib/paths.mjs";

await runAll(ROOT);
const out = execFileSync(
  "git",
  ["status", "--porcelain", "--", "packages", "crates", "frappe", "design"],
  { cwd: ROOT, encoding: "utf8" },
);
if (out.trim()) {
  console.error("Gegenereerde bestanden wijken af van wat in git staat:\n" + out);
  process.exit(1);
}
console.log("✓ gegenereerde bestanden zijn actueel");
```

- [ ] **Step 6: Tests draaien**

Run: `npm test`
Expected: PASS (3 tests)

- [ ] **Step 7: Oude lockfiles weg, regeleindes normaliseren, committen**

```bash
git rm packages/ribbon/package-lock.json packages/shell/package-lock.json packages/tokens/package-lock.json packages/ui-primitives/package-lock.json
npm install
git add --renormalize .
git status --short
```
Expected: alleen de nieuwe bestanden, `package-lock.json` in de root, de verwijderde lockfiles en eventueel hernormaliseerde tekstbestanden (geen inhoudelijke wijzigingen; controleer met `git diff --cached --ignore-all-space --stat`).

```bash
git add package.json package-lock.json .gitattributes generators
git commit -m "build: npm-workspace en generator-basis voor design/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Tokens verhuizen naar `design/tokens`

**Files:**
- Move: `packages/tokens/tokens/*.json` → `design/tokens/`; `packages/tokens/extensions/warmteverlies.json` → `design/tokens/extensions/`
- Modify: `packages/tokens/build.js` (bronpaden + kopieerstap), `packages/tokens/package.json` (repository), `packages/tokens/README.md`, `.gitignore`
- Modify: `generators/generate.mjs` (stap toevoegen)
- Test: `generators/test/tokens-package.test.mjs`

**Interfaces:**
- Produces: tokenbron in `design/tokens/` (zelfde JSON-formaat als nu: `{ pad: { value, comment } }`); stap `"tokens-package"` in `generate.mjs`.

- [ ] **Step 1: Referentie-uitvoer vastleggen vóór de verhuizing**

```bash
cd packages/tokens && node build.js && cd ../..
node -e "const c=require('crypto'),f=require('fs');for(const x of ['tokens.css','tokens.js','tailwind.preset.js'])console.log(x,c.createHash('sha256').update(f.readFileSync('packages/tokens/dist/'+x)).digest('hex'))" > "$TEMP/tokens-voor.txt"
cat "$TEMP/tokens-voor.txt"
```

- [ ] **Step 2: Bestanden verplaatsen**

```bash
mkdir -p design/tokens/extensions
git mv packages/tokens/tokens/colors.json packages/tokens/tokens/radius.json packages/tokens/tokens/semantic.json packages/tokens/tokens/shadow.json packages/tokens/tokens/spacing.json packages/tokens/tokens/typography.json design/tokens/
git mv packages/tokens/extensions/warmteverlies.json design/tokens/extensions/
```

- [ ] **Step 3: Failing test schrijven** — `generators/test/tokens-package.test.mjs`

```js
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
```

- [ ] **Step 4: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — `build.js` vindt `tokens/` niet (ENOENT).

- [ ] **Step 5: `build.js` aanpassen**

Vervang in `packages/tokens/build.js` de padconstanten:
```js
const ROOT = __dirname;
const DESIGN_TOKENS_DIR = path.join(ROOT, "..", "..", "design", "tokens");
const TOKENS_DIR = DESIGN_TOKENS_DIR;
const EXT_DIR = path.join(DESIGN_TOKENS_DIR, "extensions");
const DIST_DIR = path.join(ROOT, "dist");
```
en voeg onderaan het script toe (na het schrijven van `dist/`):
```js
// Kopie van de bron-JSON in het package, zodat "files" en de export
// "./extensions/warmteverlies" na publicatie blijven werken.
function copyJsonDir(fromDir, toDir) {
  fs.mkdirSync(toDir, { recursive: true });
  for (const f of fs.readdirSync(fromDir)) {
    if (f.endsWith(".json")) fs.copyFileSync(path.join(fromDir, f), path.join(toDir, f));
  }
}
copyJsonDir(TOKENS_DIR, path.join(ROOT, "tokens"));
copyJsonDir(EXT_DIR, path.join(ROOT, "extensions"));
```
Controleer met `grep -n "readdirSync(TOKENS_DIR" packages/tokens/build.js` dat het inlezen alleen `.json`-bestanden pakt (de submap `extensions` mag niet als bestand gelezen worden); zo niet, filter op `.json`.

`.gitignore` aanvullen:
```
# Kopieën van design/tokens in het npm-package (gemaakt door build.js)
packages/tokens/tokens/
packages/tokens/extensions/
```

`packages/tokens/package.json`, veld `repository`:
```json
"repository": {
  "type": "git",
  "url": "https://github.com/OpenAEC-Foundation/OpenAEC-style-book",
  "directory": "packages/tokens"
},
```

In `packages/tokens/README.md` een alinea bovenaan toevoegen:
```markdown
> **Bron:** de tokens staan in [`design/tokens/`](../../design/tokens/). Pas ze daar aan;
> `npm run generate` in de root bouwt dit package opnieuw.
```

Stap registreren in `generators/generate.mjs` (boven `export async function runAll`):
```js
import { execFileSync } from "node:child_process";
import { join } from "node:path";

steps.push(["tokens-package", (root) => {
  execFileSync(process.execPath, ["build.js"], { cwd: join(root, "packages", "tokens"), stdio: "inherit" });
  return [];
}]);
```
(`dist/` en de JSON-kopieën zijn build-uitvoer en staan niet in git; daarom geeft deze stap geen bestanden terug.)

- [ ] **Step 6: Tests en vergelijking**

Run: `npm test`
Expected: PASS

```bash
node -e "const c=require('crypto'),f=require('fs');for(const x of ['tokens.css','tokens.js','tailwind.preset.js'])console.log(x,c.createHash('sha256').update(f.readFileSync('packages/tokens/dist/'+x)).digest('hex'))" | diff - "$TEMP/tokens-voor.txt"
```
Expected: geen uitvoer (dist is byte-gelijk aan vóór de verhuizing).

- [ ] **Step 7: Commit**

```bash
git add design/tokens packages/tokens .gitignore generators
git commit -m "refactor(tokens): bron verhuisd naar design/tokens

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Tokens naar Rust — crate `openaec-tokens`

**Files:**
- Create: `generators/tokens/load.mjs`, `generators/tokens/rust.mjs`, `generators/test/tokens.test.mjs`
- Create: `Cargo.toml` (workspace), `crates/openaec-tokens/Cargo.toml`, `crates/openaec-tokens/src/lib.rs`, `crates/openaec-tokens/tests/tokens.rs`
- Generated: `crates/openaec-tokens/src/generated.rs`
- Modify: `generators/generate.mjs`

**Interfaces:**
- Consumes: `writeGenerated`, `repoPath` (Task 1); `design/tokens/*.json` (Task 2).
- Produces:
  - `loadTokens(tokensDir: string): { static: Leaf[], light: Leaf[], dark: Leaf[] }` met `Leaf = { path: string[], value: string, comment: string|null }`; themed-paden zijn ontdaan van het `light`/`dark`-segment (`["color","surface","bg"]`).
  - `assertThemeParity(tokens)` — gooit als light en dark niet dezelfde paden hebben.
  - `hexToRgba(hex): [r,g,b,a]`, `lengthToPx(value): number`, `constName(segment, parent): string`, `renderTokensRust(tokens): string`.
  - Rust: `openaec_tokens::Rgba { r, g, b, a }` met `const fn new`, `to_hex()`, `to_f32()`; modules `color::{brand,neutral}`, `spacing`, `radius`, `font::{family,weight,size,line_height,letter_spacing}`; `struct Theme` met velden `surface_bg, surface_panel, surface_elevated, surface_muted, text_primary, text_secondary, text_muted, text_inverse, border_default, border_strong, border_focus, semantic_success, semantic_success_bg, semantic_error, semantic_error_bg, semantic_danger, semantic_danger_bg, semantic_warning, semantic_warning_bg, semantic_info, semantic_info_bg`; constanten `LIGHT`, `DARK`.

- [ ] **Step 1: Failing Node-test** — `generators/test/tokens.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { assertThemeParity, classify, loadTokens } from "../tokens/load.mjs";
import { constName, hexToRgba, lengthToPx, renderTokensRust } from "../tokens/rust.mjs";
import { repoPath } from "../lib/paths.mjs";

test("classify haalt light/dark uit themed paden", () => {
  const out = classify([
    { path: ["color", "surface", "light", "bg"], value: "#FFF", comment: null },
    { path: ["color", "surface", "dark", "bg"], value: "#000", comment: null },
    { path: ["color", "brand", "amber"], value: "#D97706", comment: null },
  ]);
  assert.deepEqual(out.light[0].path, ["color", "surface", "bg"]);
  assert.deepEqual(out.dark[0].path, ["color", "surface", "bg"]);
  assert.equal(out.static.length, 1);
});

test("assertThemeParity weigert ontbrekend dark-token", () => {
  const tokens = { static: [], light: [{ path: ["color", "text", "primary"] }], dark: [] };
  assert.throws(() => assertThemeParity(tokens), /color\.text\.primary/);
});

test("conversies", () => {
  assert.deepEqual(hexToRgba("#D97706"), [0xd9, 0x77, 0x06, 0xff]);
  assert.deepEqual(hexToRgba("#d9770680"), [0xd9, 0x77, 0x06, 0x80]);
  assert.throws(() => hexToRgba("rgb(1,2,3)"), /Ongeldige kleur/);
  assert.equal(lengthToPx("0"), 0);
  assert.equal(lengthToPx("0.25rem"), 4);
  assert.equal(lengthToPx("96px"), 96);
  assert.throws(() => lengthToPx("10vh"), /Onbekende lengte/);
  assert.equal(constName("2xl", "size"), "S2XL");
  assert.equal(constName("ribbon-height", "spacing"), "RIBBON_HEIGHT");
});

test("renderTokensRust bevat merk-, thema- en maatconstanten", () => {
  const rust = renderTokensRust(loadTokens(repoPath("design", "tokens")));
  assert.match(rust, /pub const AMBER: crate::Rgba = crate::Rgba::new\(0xD9, 0x77, 0x06, 0xFF\);/);
  assert.match(rust, /pub const RIBBON_HEIGHT: f32 = 96\.0;/);
  assert.match(rust, /pub const HEADING: &str = "Space Grotesk";/);
  assert.match(rust, /pub const LIGHT: Theme = Theme \{/);
  assert.match(rust, /surface_bg: crate::Rgba::new\(0xFA, 0xFA, 0xF9, 0xFF\)/);
  assert.ok(!rust.includes("shadow"), "schaduwen zijn CSS-specifiek en horen niet in Rust");
});
```

- [ ] **Step 2: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — `Cannot find module '../tokens/load.mjs'`

- [ ] **Step 3: `generators/tokens/load.mjs`**

```js
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const THEMED_GROUPS = ["surface", "text", "border", "semantic"];

export function* walkTokens(tree, prefix = []) {
  for (const [key, val] of Object.entries(tree)) {
    if (key.startsWith("$")) continue;
    if (val && typeof val === "object" && "value" in val) {
      yield { path: [...prefix, key], value: String(val.value), comment: val.comment ?? null };
    } else if (val && typeof val === "object") {
      yield* walkTokens(val, [...prefix, key]);
    }
  }
}

export function classify(leaves) {
  const out = { static: [], light: [], dark: [] };
  for (const leaf of leaves) {
    const [root, group, mode, ...rest] = leaf.path;
    if (root === "color" && THEMED_GROUPS.includes(group) && (mode === "light" || mode === "dark")) {
      out[mode].push({ ...leaf, path: [root, group, ...rest] });
    } else {
      out.static.push(leaf);
    }
  }
  return out;
}

export function assertThemeParity(tokens) {
  const key = (l) => l.path.join(".");
  const light = new Set(tokens.light.map(key));
  const dark = new Set(tokens.dark.map(key));
  const missing = [...light].filter((k) => !dark.has(k)).map((k) => `${k} (dark ontbreekt)`)
    .concat([...dark].filter((k) => !light.has(k)).map((k) => `${k} (light ontbreekt)`));
  if (missing.length) throw new Error(`Thema's niet gelijk: ${missing.join(", ")}`);
}

export function loadTokens(tokensDir) {
  const files = readdirSync(tokensDir).filter((f) => f.endsWith(".json")).sort();
  const leaves = [];
  for (const f of files) leaves.push(...walkTokens(JSON.parse(readFileSync(join(tokensDir, f), "utf8"))));
  const tokens = classify(leaves);
  assertThemeParity(tokens);
  return tokens;
}

export function tokenValue(tokens, dottedPath) {
  const leaf = tokens.static.find((l) => l.path.join(".") === dottedPath);
  if (!leaf) throw new Error(`Token ${dottedPath} bestaat niet`);
  return leaf.value;
}
```

- [ ] **Step 4: `generators/tokens/rust.mjs`**

```js
export function hexToRgba(hex) {
  const m = /^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$/.exec(hex.trim());
  if (!m) throw new Error(`Ongeldige kleur: ${hex}`);
  const rgb = [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16));
  return [...rgb, m[2] ? parseInt(m[2], 16) : 255];
}

export function lengthToPx(value) {
  const v = value.trim();
  if (v === "0") return 0;
  let m = /^(-?\d*\.?\d+)px$/.exec(v);
  if (m) return Number(m[1]);
  m = /^(-?\d*\.?\d+)rem$/.exec(v);
  if (m) return Number(m[1]) * 16;
  throw new Error(`Onbekende lengte: ${value}`);
}

export function constName(segment, parent) {
  const up = segment.replace(/-/g, "_").toUpperCase();
  return /^\d/.test(up) ? parent[0].toUpperCase() + up : up;
}

const modName = (s) => s.replace(/-/g, "_");
const f32 = (n) => (Number.isInteger(n) ? `${n}.0` : String(n));
const hex2 = (n) => "0x" + n.toString(16).toUpperCase().padStart(2, "0");
const rgbaExpr = (hex) => `crate::Rgba::new(${hexToRgba(hex).map(hex2).join(", ")})`;

function rustValue(leaf) {
  const [root, group] = leaf.path;
  if (root === "color") return { type: "crate::Rgba", expr: rgbaExpr(leaf.value) };
  if (root === "spacing" || root === "radius") return { type: "f32", expr: f32(lengthToPx(leaf.value)) };
  if (root === "font" && group === "family") {
    const first = leaf.value.split(",")[0].trim().replace(/^['"]|['"]$/g, "");
    return { type: "&str", expr: JSON.stringify(first) };
  }
  if (root === "font" && group === "weight") return { type: "u16", expr: String(Number(leaf.value)) };
  if (root === "font" && group === "size") return { type: "f32", expr: f32(lengthToPx(leaf.value)) };
  if (root === "font" && group === "line-height") return { type: "f32", expr: f32(Number(leaf.value)) };
  if (root === "font" && group === "letter-spacing") {
    return { type: "f32", expr: f32(leaf.value === "0" ? 0 : Number(leaf.value.replace(/em$/, ""))) };
  }
  return null; // shadow e.d.: CSS-specifiek
}

function renderModules(leaves) {
  const tree = {};
  for (const leaf of leaves) {
    const v = rustValue(leaf);
    if (!v) continue;
    let node = tree;
    for (const seg of leaf.path.slice(0, -1)) node = node[seg] ??= {};
    (node.$consts ??= []).push({ leaf, v });
  }
  const render = (node, indent) => {
    let out = "";
    for (const c of (node.$consts ?? []).sort((a, b) => (a.leaf.path.join(".") < b.leaf.path.join(".") ? -1 : 1))) {
      const name = constName(c.leaf.path.at(-1), c.leaf.path.at(-2));
      if (c.leaf.comment) out += `${indent}/// ${c.leaf.comment}\n`;
      out += `${indent}pub const ${name}: ${c.v.type} = ${c.v.expr};\n`;
    }
    for (const key of Object.keys(node).filter((k) => k !== "$consts").sort()) {
      out += `${indent}pub mod ${modName(key)} {\n${render(node[key], indent + "    ")}${indent}}\n`;
    }
    return out;
  };
  return render(tree, "");
}

const fieldName = (path) => path.slice(1).join("_").replace(/-/g, "_");

export function renderTokensRust(tokens) {
  const light = [...tokens.light].sort((a, b) => (fieldName(a.path) < fieldName(b.path) ? -1 : 1));
  const dark = new Map(tokens.dark.map((l) => [fieldName(l.path), l]));
  let out = renderModules(tokens.static);
  out += "\n/// Thema-afhankelijke kleuren (licht en donker).\n#[derive(Debug, Clone, Copy, PartialEq, Eq)]\npub struct Theme {\n";
  for (const l of light) out += `    pub ${fieldName(l.path)}: crate::Rgba,\n`;
  out += "}\n";
  for (const [name, get] of [["LIGHT", (l) => l], ["DARK", (l) => dark.get(fieldName(l.path))]]) {
    out += `\npub const ${name}: Theme = Theme {\n`;
    for (const l of light) out += `    ${fieldName(l.path)}: ${rgbaExpr(get(l).value)},\n`;
    out += "};\n";
  }
  return out;
}
```

- [ ] **Step 5: Node-tests draaien**

Run: `npm test`
Expected: PASS

- [ ] **Step 6: Rust-workspace en crate**

`Cargo.toml`:
```toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT"
repository = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book"
authors = ["OpenAEC Foundation"]
```

`crates/openaec-tokens/Cargo.toml`:
```toml
[package]
name = "openaec-tokens"
description = "OpenAEC design tokens (kleuren, typografie, maten) voor Rust"
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true
authors.workspace = true
```

`crates/openaec-tokens/src/lib.rs`:
```rust
//! OpenAEC design tokens voor Rust-applicaties.
//!
//! Bron: `design/tokens/` in OpenAEC-style-book. De constanten in `generated.rs`
//! worden door `npm run generate` gemaakt; pas de bron aan, niet die code.
//! Lengtes zijn in pixels (1rem = 16px); letterafstand in em.

mod generated;
pub use generated::*;

/// Kleur als 8-bit RGBA.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Rgba {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}

impl Rgba {
    pub const fn new(r: u8, g: u8, b: u8, a: u8) -> Self {
        Self { r, g, b, a }
    }

    /// `#RRGGBB`, of `#RRGGBBAA` als de kleur niet volledig dekkend is.
    pub fn to_hex(self) -> String {
        if self.a == 255 {
            format!("#{:02X}{:02X}{:02X}", self.r, self.g, self.b)
        } else {
            format!("#{:02X}{:02X}{:02X}{:02X}", self.r, self.g, self.b, self.a)
        }
    }

    /// Kanalen als 0.0–1.0, in de volgorde r, g, b, a.
    pub fn to_f32(self) -> [f32; 4] {
        [self.r, self.g, self.b, self.a].map(|c| c as f32 / 255.0)
    }
}
```

`crates/openaec-tokens/tests/tokens.rs`:
```rust
use openaec_tokens::{color, font, spacing, Rgba, DARK, LIGHT};

#[test]
fn merkkleuren() {
    assert_eq!(color::brand::AMBER.to_hex(), "#D97706");
    assert_eq!(color::brand::DEEP_FORGE.to_hex(), "#36363E");
}

#[test]
fn themas() {
    assert_eq!(LIGHT.surface_bg.to_hex(), "#FAFAF9");
    assert_eq!(DARK.surface_bg.to_hex(), "#36363E");
    assert_eq!(DARK.border_focus.to_hex(), "#F59E0B");
    assert_ne!(LIGHT, DARK);
}

#[test]
fn maten_en_fonts() {
    assert_eq!(spacing::S4, 16.0);
    assert_eq!(spacing::RIBBON_HEIGHT, 96.0);
    assert_eq!(font::size::S2XL, 24.0);
    assert_eq!(font::family::HEADING, "Space Grotesk");
    assert_eq!(font::weight::BOLD, 700);
}

#[test]
fn rgba_hulpfuncties() {
    assert_eq!(Rgba::new(255, 0, 0, 128).to_hex(), "#FF000080");
    assert_eq!(Rgba::new(255, 0, 0, 255).to_f32(), [1.0, 0.0, 0.0, 1.0]);
}
```

Stap registreren in `generators/generate.mjs`:
```js
import { loadTokens } from "./tokens/load.mjs";
import { renderTokensRust } from "./tokens/rust.mjs";
import { writeGenerated } from "./lib/write.mjs";

steps.push(["tokens-rust", (root) => [
  writeGenerated(join(root, "crates", "openaec-tokens", "src", "generated.rs"),
    renderTokensRust(loadTokens(join(root, "design", "tokens")))),
]]);
```

- [ ] **Step 7: Rust-test draaien**

Run: `npm run generate && cargo test -p openaec-tokens`
Expected: PASS (4 tests). Bij een compileerfout over een onbekende constante: kijk in `generated.rs` naar de echte naam en pas de test pas aan als de generatorregel (`constName`) correct is toegepast.

- [ ] **Step 8: Commit**

```bash
git add Cargo.toml Cargo.lock crates/openaec-tokens generators
git commit -m "feat(tokens): Rust-crate openaec-tokens uit design/tokens

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Iconen normaliseren en het manifest valideren

**Files:**
- Create: `generators/lib/toml.mjs`, `generators/icons/normalize.mjs`, `generators/icons/manifest.mjs`, `generators/test/icons-normalize.test.mjs`, `generators/test/icons-manifest.test.mjs`

**Interfaces:**
- Produces:
  - `parseToml(text: string): object`, `readToml(file: string): object` uit `lib/toml.mjs`.
  - `normalizeColor(c: string): string`, `normalizeSvg(raw: string, opts?: { neutralColors?: string[] }): { svg: string, colors: string[] }`, `extraColors(svg: string): string[]`.
  - `ID_PATTERN`, `loadIconManifest(iconsDir: string): Icon[]` met `Icon = { id, domain, name, label: { nl, en }, tags: string[], source: string, svg: string }`, gesorteerd op `id`; gooit `IconManifestError` (met `.errors: string[]`).
  - `icons.toml`-formaat:
    ```toml
    [[icon]]
    id = "edit/undo"
    label = { nl = "Ongedaan maken", en = "Undo" }
    tags = ["edit"]
    source = "openaec"
    ```

- [ ] **Step 1: Failing tests** — `generators/test/icons-normalize.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { extraColors, normalizeColor, normalizeSvg } from "../icons/normalize.mjs";

const wrap = (inner, attrs = 'viewBox="0 0 24 24"') => `<svg ${attrs}>${inner}</svg>`;

test("voegt xmlns toe en haalt width/height van de root", () => {
  const { svg } = normalizeSvg(wrap('<path d="M1 1"/>', 'viewBox="0 0 24 24" width="64" height="64"'));
  assert.ok(svg.startsWith('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'));
  assert.ok(!/width=|height=/.test(svg.slice(0, svg.indexOf(">"))));
});

test("weigert andere viewBox, scripts en externe verwijzingen", () => {
  assert.throws(() => normalizeSvg(wrap("", 'viewBox="0 0 16 16"')), /viewBox/);
  assert.throws(() => normalizeSvg(wrap("<script>x</script>")), /niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<image href="https://x/y.png"/>')), /niet toegestaan/);
  assert.throws(() => normalizeSvg(wrap('<path onclick="x()"/>')), /niet toegestaan/);
  assert.throws(() => normalizeSvg("<g/>"), /geen <svg>/);
});

test("neutrale kleuren worden currentColor, ook in style en als 3-cijferige hex", () => {
  const raw = wrap('<path stroke="#E0E0E0"/><path fill="#eee"/><path style="stroke:#e0e0e0;fill:#4CC9F0"/>');
  const { svg, colors } = normalizeSvg(raw, { neutralColors: ["#e0e0e0", "#eeeeee"] });
  assert.ok(svg.includes('stroke="currentColor"'));
  assert.ok(svg.includes('fill="currentColor"'));
  assert.ok(svg.includes("stroke:currentColor"));
  assert.deepEqual(colors, ["#4cc9f0"]);
});

test("currentColor in elke schrijfwijze telt niet als eigen kleur", () => {
  assert.deepEqual(extraColors(wrap('<path stroke="CurrentColor" fill="none"/>')), []);
  assert.equal(normalizeColor("#ABC"), "#aabbcc");
});
```

`generators/test/icons-manifest.test.mjs`:
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { loadIconManifest } from "../icons/manifest.mjs";

const SVG = '<svg viewBox="0 0 24 24"><path stroke="currentColor" d="M1 1L5 5"/></svg>';

function fixture(files, toml) {
  const dir = mkdtempSync(join(tmpdir(), "oa-icons-"));
  for (const [id, svg] of Object.entries(files)) {
    const [domain, name] = id.split("/");
    mkdirSync(join(dir, domain), { recursive: true });
    writeFileSync(join(dir, domain, `${name}.svg`), svg);
  }
  writeFileSync(join(dir, "icons.toml"), toml);
  return dir;
}

const entry = (id, extra = "") =>
  `[[icon]]\nid = "${id}"\nlabel = { nl = "N", en = "E" }\ntags = []\nsource = "openaec"\n${extra}\n`;

test("geldig manifest geeft gesorteerde iconen terug", () => {
  const dir = fixture({ "edit/undo": SVG, "edit/copy": SVG.replace("M1 1", "M2 2") }, entry("edit/undo") + entry("edit/copy"));
  const icons = loadIconManifest(dir);
  assert.deepEqual(icons.map((i) => i.id), ["edit/copy", "edit/undo"]);
  assert.equal(icons[0].domain, "edit");
});

test("meldt bestand zonder manifest, manifest zonder bestand, slecht id en ontbrekend label", () => {
  const dir = fixture({ "edit/undo": SVG, "edit/extra": SVG.replace("M1", "M3") },
    entry("edit/undo") + entry("edit/missing") + entry("Edit/Bad") +
    '[[icon]]\nid = "edit/nolabel"\nsource = "openaec"\n');
  assert.throws(() => loadIconManifest(dir), (err) => {
    const all = err.errors.join("\n");
    return /edit\/extra\.svg staat niet in icons\.toml/.test(all) &&
      /edit\/missing: bestand ontbreekt/.test(all) &&
      /ongeldig icoon-id: Edit\/Bad/.test(all) &&
      /edit\/nolabel: label\.nl en label\.en zijn verplicht/.test(all);
  });
});

test("eigen kleuren vereisen tag color, en omgekeerd", () => {
  const colored = '<svg viewBox="0 0 24 24"><path stroke="#4cc9f0"/></svg>';
  const toml = [
    '[[icon]]', 'id = "cad/a"', 'label = { nl = "N", en = "E" }', 'tags = []', 'source = "openaec"', '',
    '[[icon]]', 'id = "cad/b"', 'label = { nl = "N", en = "E" }', 'tags = ["color"]', 'source = "openaec"', '',
  ].join("\n");
  const dir = fixture({ "cad/a": colored, "cad/b": SVG }, toml);
  assert.throws(() => loadIconManifest(dir), (err) => {
    const all = err.errors.join("\n");
    return /cad\/a: bevat kleuren #4cc9f0 maar mist tag "color"/.test(all) &&
      /cad\/b: tag "color" maar geen eigen kleuren/.test(all);
  });
});

test("hetzelfde SVG onder twee id's wordt geweigerd", () => {
  const dir = fixture({ "edit/a": SVG, "edit/b": SVG }, entry("edit/a") + entry("edit/b"));
  assert.throws(() => loadIconManifest(dir), (err) => /edit\/b: zelfde SVG als edit\/a/.test(err.errors.join("\n")));
});
```

- [ ] **Step 2: Tests draaien en zien falen**

Run: `npm test`
Expected: FAIL — modules ontbreken.

- [ ] **Step 3: `generators/lib/toml.mjs`**

```js
import { readFileSync } from "node:fs";
import { parse } from "smol-toml";

export function parseToml(text) {
  return parse(text);
}

export function readToml(file) {
  return parse(readFileSync(file, "utf8"));
}
```

- [ ] **Step 4: `generators/icons/normalize.mjs`**

```js
const SVG_NS = 'xmlns="http://www.w3.org/2000/svg"';
const COLOR_ATTR = /\b(fill|stroke|stop-color|color)\s*=\s*"([^"]*)"/gi;
const STYLE_ATTR = /\bstyle\s*=\s*"([^"]*)"/gi;
const STYLE_COLOR = /(fill|stroke|stop-color|color)\s*:\s*([^;"]+)/gi;
const FORBIDDEN = /<script\b|\son[a-z]+\s*=|(?:xlink:)?href\s*=\s*"(?!#)/i;
const NOT_A_COLOR = new Set(["none", "currentcolor", "transparent", "inherit"]);

export function normalizeColor(c) {
  const v = c.trim().toLowerCase();
  if (/^#[0-9a-f]{3}$/.test(v)) return "#" + [...v.slice(1)].map((x) => x + x).join("");
  return v;
}

export function extraColors(svg) {
  const found = new Set();
  const collect = (v) => {
    const n = normalizeColor(v);
    if (!NOT_A_COLOR.has(n) && !n.startsWith("url(")) found.add(n);
  };
  for (const m of svg.matchAll(COLOR_ATTR)) collect(m[2]);
  for (const m of svg.matchAll(STYLE_ATTR)) for (const s of m[1].matchAll(STYLE_COLOR)) collect(s[2]);
  return [...found].sort();
}

export function normalizeSvg(raw, { neutralColors = [] } = {}) {
  let svg = raw.replace(/\r\n?/g, "\n").trim()
    .replace(/<\?xml[^>]*>\s*/g, "")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<title>[\s\S]*?<\/title>/g, "");
  const root = /^<svg\b([^>]*)>/.exec(svg);
  if (!root) throw new Error("geen <svg>-root");
  if (FORBIDDEN.test(svg)) throw new Error("scripts, event-handlers of externe verwijzingen zijn niet toegestaan");
  const vb = /\bviewBox\s*=\s*"([^"]*)"/.exec(root[1]);
  const vbValue = vb ? vb[1].trim().split(/[\s,]+/).join(" ") : null;
  if (vbValue !== "0 0 24 24") throw new Error(`viewBox moet "0 0 24 24" zijn (gevonden: ${vbValue ?? "geen"})`);
  const attrs = root[1]
    .replace(/\s(width|height)\s*=\s*"[^"]*"/g, "")
    .replace(/\sxmlns\s*=\s*"[^"]*"/g, "")
    .replace(/\s+/g, " ")
    .trimEnd();
  svg = `<svg ${SVG_NS}${attrs.startsWith(" ") ? attrs : " " + attrs}>` + svg.slice(root[0].length);
  const neutral = new Set(neutralColors.map(normalizeColor));
  const recolor = (value) => {
    const n = normalizeColor(value);
    return n === "currentcolor" || neutral.has(n) ? "currentColor" : value.trim();
  };
  svg = svg
    .replace(COLOR_ATTR, (_, name, value) => `${name}="${recolor(value)}"`)
    .replace(STYLE_ATTR, (_, style) => `style="${style.replace(STYLE_COLOR, (__, p, v) => `${p}:${recolor(v)}`)}"`)
    .replace(/>\s+</g, "><")
    .replace(/[ \t]{2,}/g, " ");
  return { svg, colors: extraColors(svg) };
}
```

- [ ] **Step 5: `generators/icons/manifest.mjs`**

```js
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { readToml } from "../lib/toml.mjs";
import { normalizeSvg } from "./normalize.mjs";

export const ID_PATTERN = /^[a-z][a-z0-9]*\/[a-z0-9]+(?:-[a-z0-9]+)*$/;
const byId = (a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);

export class IconManifestError extends Error {
  constructor(errors) {
    super(`icons.toml bevat ${errors.length} fout(en):\n- ${errors.join("\n- ")}`);
    this.errors = errors;
  }
}

export function listSvgIds(iconsDir) {
  const ids = [];
  for (const domain of readdirSync(iconsDir).sort()) {
    const dir = join(iconsDir, domain);
    if (!statSync(dir).isDirectory()) continue;
    for (const f of readdirSync(dir).sort()) if (f.endsWith(".svg")) ids.push(`${domain}/${f.slice(0, -4)}`);
  }
  return ids;
}

export function loadIconManifest(iconsDir) {
  const entries = readToml(join(iconsDir, "icons.toml")).icon ?? [];
  const errors = [];
  const seen = new Set();
  for (const e of entries) {
    if (!ID_PATTERN.test(e.id ?? "")) errors.push(`ongeldig icoon-id: ${e.id}`);
    if (seen.has(e.id)) errors.push(`dubbel icoon-id: ${e.id}`);
    seen.add(e.id);
    if (!e.label?.nl || !e.label?.en) errors.push(`${e.id}: label.nl en label.en zijn verplicht`);
    if (!e.source) errors.push(`${e.id}: source is verplicht`);
  }
  for (const id of listSvgIds(iconsDir)) if (!seen.has(id)) errors.push(`${id}.svg staat niet in icons.toml`);

  const icons = [];
  const bySvg = new Map();
  for (const e of [...entries].filter((x) => ID_PATTERN.test(x.id ?? "")).sort(byId)) {
    const [domain, name] = e.id.split("/");
    const file = join(iconsDir, domain, `${name}.svg`);
    if (!existsSync(file)) { errors.push(`${e.id}: bestand ontbreekt`); continue; }
    let result;
    try { result = normalizeSvg(readFileSync(file, "utf8")); }
    catch (err) { errors.push(`${e.id}: ${err.message}`); continue; }
    const tags = e.tags ?? [];
    if (result.colors.length && !tags.includes("color")) {
      errors.push(`${e.id}: bevat kleuren ${result.colors.join(", ")} maar mist tag "color"`);
    }
    if (!result.colors.length && tags.includes("color")) errors.push(`${e.id}: tag "color" maar geen eigen kleuren`);
    if (bySvg.has(result.svg)) errors.push(`${e.id}: zelfde SVG als ${bySvg.get(result.svg)}`);
    else bySvg.set(result.svg, e.id);
    icons.push({ id: e.id, domain, name, label: e.label, tags, source: e.source, svg: result.svg });
  }
  if (errors.length) throw new IconManifestError(errors);
  return icons;
}
```

- [ ] **Step 6: Tests draaien**

Run: `npm test`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add generators
git commit -m "feat(icons): normalisatie en validatie van het iconenmanifest

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Eigen iconen importeren naar `design/icons`

**Files:**
- Create: `generators/icons/import.mjs`, `generators/icons/import-openaec.mjs`, `generators/test/icons-import.test.mjs`
- Generated (eenmalig, daarna bron): `design/icons/**/*.svg`, `design/icons/icons.toml`

**Interfaces:**
- Consumes: `normalizeSvg` (Task 4), `loadIconManifest` (Task 4).
- Produces: `readTsIconModule(file): Map<string, string>`, `importIcons(entries, iconsDir, opts?): { written, duplicates }`, `manifestToml(entries): string`, `readSvgDirectory(dir, { domainFor, nameFor }): { id, svg }[]` (gebruikt in Task 15).

- [ ] **Step 1: Failing test** — `generators/test/icons-import.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { importIcons, manifestToml, readTsIconModule } from "../icons/import.mjs";
import { parseToml } from "../lib/toml.mjs";

test("readTsIconModule leest export const xIcon = `<svg…>`", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-ts-"));
  const file = join(dir, "icons.ts");
  writeFileSync(file, 'export const undoIcon = `<svg viewBox="0 0 24 24"></svg>`;\nexport const x = 1;\n');
  assert.deepEqual([...readTsIconModule(file).keys()], ["undoIcon"]);
});

test("importIcons schrijft genormaliseerde SVG's en slaat dubbelen over", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-imp-"));
  const svg = '<svg viewBox="0 0 24 24"><path stroke="currentColor" d="M1 1"/></svg>';
  const { written, duplicates } = importIcons(
    [{ id: "edit/undo", svg }, { id: "edit/again", svg }], dir);
  assert.deepEqual(written.map((w) => w.id), ["edit/undo"]);
  assert.deepEqual(duplicates, [["edit/again", "edit/undo"]]);
  assert.ok(readFileSync(join(dir, "edit", "undo.svg"), "utf8").startsWith('<svg xmlns="http://www.w3.org/2000/svg"'));
});

test("manifestToml is leesbaar en gesorteerd", () => {
  const toml = manifestToml([
    { id: "edit/undo", label: { nl: "Ongedaan maken", en: "Undo" }, tags: [], source: "openaec" },
    { id: "edit/copy", label: { nl: "Kopiëren", en: "Copy" }, tags: ["edit"], source: "openaec" },
  ]);
  const parsed = parseToml(toml);
  assert.deepEqual(parsed.icon.map((i) => i.id), ["edit/copy", "edit/undo"]);
  assert.equal(parsed.icon[0].label.nl, "Kopiëren");
});
```

- [ ] **Step 2: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — module ontbreekt.

- [ ] **Step 3: `generators/icons/import.mjs`**

```js
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { normalizeSvg } from "./normalize.mjs";

export function readTsIconModule(file) {
  const out = new Map();
  for (const m of readFileSync(file, "utf8").matchAll(/export const (\w+)\s*=\s*`([^`]*)`/g)) out.set(m[1], m[2]);
  return out;
}

export function readSvgDirectory(dir, { domainFor, nameFor }) {
  const out = [];
  const walk = (d, rel) => {
    for (const f of readdirSync(d, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : 1))) {
      if (f.isDirectory()) walk(join(d, f.name), [...rel, f.name]);
      else if (f.name.endsWith(".svg")) {
        const base = f.name.slice(0, -4);
        out.push({ id: `${domainFor(rel, base)}/${nameFor(rel, base)}`, svg: readFileSync(join(d, f.name), "utf8") });
      }
    }
  };
  walk(dir, []);
  return out;
}

export function importIcons(entries, iconsDir, { neutralColors = [] } = {}) {
  const seen = new Map();
  const written = [];
  const duplicates = [];
  for (const e of entries) {
    const { svg } = normalizeSvg(e.svg, { neutralColors });
    if (seen.has(svg)) { duplicates.push([e.id, seen.get(svg)]); continue; }
    seen.set(svg, e.id);
    const [domain, name] = e.id.split("/");
    const file = join(iconsDir, domain, `${name}.svg`);
    mkdirSync(dirname(file), { recursive: true });
    writeFileSync(file, svg + "\n", "utf8");
    written.push(e);
  }
  return { written, duplicates };
}

const q = (s) => JSON.stringify(s);

export function manifestToml(entries) {
  const sorted = [...entries].sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return sorted.map((e) => [
    "[[icon]]",
    `id = ${q(e.id)}`,
    `label = { nl = ${q(e.label.nl)}, en = ${q(e.label.en)} }`,
    `tags = [${(e.tags ?? []).map(q).join(", ")}]`,
    `source = ${q(e.source)}`,
    "",
  ].join("\n")).join("\n");
}
```

- [ ] **Step 4: Tests draaien**

Run: `npm test`
Expected: PASS

- [ ] **Step 5: Eenmalig importscript** — `generators/icons/import-openaec.mjs`

De twee eigen sets (`project-templates/Tauri+React/src/components/ribbon/icons.ts` en `packages/ribbon/src/icons.ts`) zijn inhoudelijk gelijk (42 iconen, allemaal `currentColor`, viewBox 24). Ze worden onder deze id's en labels opgenomen:

```js
import { writeFileSync } from "node:fs";
import { repoPath } from "../lib/paths.mjs";
import { importIcons, manifestToml, readTsIconModule } from "./import.mjs";

// exportnaam → [id, nl, en, tags]
const MAP = {
  settingsIcon: ["ui/settings", "Instellingen", "Settings", ["ui"]],
  helpIcon: ["ui/help", "Help", "Help", ["ui"]],
  infoIcon: ["ui/info", "Informatie", "Information", ["ui"]],
  extensionBrowseIcon: ["ui/extension-browse", "Extensies zoeken", "Browse extensions", ["ui", "extension"]],
  extensionInstallIcon: ["ui/extension-install", "Extensie installeren", "Install extension", ["ui", "extension"]],
  extensionManageIcon: ["ui/extension-manage", "Extensies beheren", "Manage extensions", ["ui", "extension"]],
  projectIcon: ["file/project", "Project", "Project", ["file"]],
  pasteIcon: ["edit/paste", "Plakken", "Paste", ["edit", "clipboard"]],
  cutIcon: ["edit/cut", "Knippen", "Cut", ["edit", "clipboard"]],
  copyIcon: ["edit/copy", "Kopiëren", "Copy", ["edit", "clipboard"]],
  undoIcon: ["edit/undo", "Ongedaan maken", "Undo", ["edit", "history"]],
  redoIcon: ["edit/redo", "Opnieuw", "Redo", ["edit", "history"]],
  boldIcon: ["text/bold", "Vet", "Bold", ["text"]],
  italicIcon: ["text/italic", "Cursief", "Italic", ["text"]],
  underlineIcon: ["text/underline", "Onderstrepen", "Underline", ["text"]],
  alignLeftIcon: ["text/align-left", "Links uitlijnen", "Align left", ["text", "align"]],
  alignCenterIcon: ["text/align-center", "Centreren", "Center", ["text", "align"]],
  alignRightIcon: ["text/align-right", "Rechts uitlijnen", "Align right", ["text", "align"]],
  pencilIcon: ["draw/pencil", "Potlood", "Pencil", ["draw"]],
  lineIcon: ["draw/line", "Lijn", "Line", ["draw"]],
  arrowIcon: ["draw/arrow", "Pijl", "Arrow", ["draw"]],
  circleIcon: ["draw/circle", "Cirkel", "Circle", ["draw"]],
  rectangleIcon: ["draw/rectangle", "Rechthoek", "Rectangle", ["draw"]],
  imageIcon: ["insert/image", "Afbeelding", "Image", ["insert"]],
  tableIcon: ["insert/table", "Tabel", "Table", ["insert"]],
  linkIcon: ["insert/link", "Koppeling", "Link", ["insert"]],
  viewerLoadIcon: ["view/load-model", "Model laden", "Load model", ["view", "3d"]],
  viewerOrbitIcon: ["view/orbit", "Roteren", "Orbit", ["view", "3d", "navigation"]],
  viewerFitIcon: ["view/fit-all", "Passend", "Fit all", ["view", "3d", "navigation"]],
  viewerSectionIcon: ["view/section", "Doorsnede", "Section", ["view", "3d", "analysis"]],
  viewerMeasureIcon: ["view/measure", "Meten", "Measure", ["view", "3d", "analysis"]],
  viewerWireframeIcon: ["view/wireframe", "Draadmodel", "Wireframe", ["view", "3d", "display"]],
  ifcImportIcon: ["ifc/import", "IFC importeren", "Import IFC", ["ifc"]],
  ifcExportIcon: ["ifc/export", "IFC exporteren", "Export IFC", ["ifc"]],
  ifcTreeIcon: ["ifc/tree", "IFC-structuur", "IFC tree", ["ifc"]],
  ifcValidateIcon: ["ifc/validate", "IFC valideren", "Validate IFC", ["ifc"]],
  ifcStatsIcon: ["ifc/stats", "IFC-statistieken", "IFC statistics", ["ifc"]],
  reportNewIcon: ["report/new", "Nieuw rapport", "New report", ["report"]],
  reportTemplateIcon: ["report/template", "Rapportsjabloon", "Report template", ["report"]],
  reportGenerateIcon: ["report/generate", "Rapport genereren", "Generate report", ["report"]],
  reportPreviewIcon: ["report/preview", "Voorbeeld", "Preview", ["report"]],
  reportCoverIcon: ["report/cover", "Voorblad", "Cover page", ["report"]],
};

const template = readTsIconModule(repoPath("project-templates", "Tauri+React", "src", "components", "ribbon", "icons.ts"));
const pkg = readTsIconModule(repoPath("packages", "ribbon", "src", "icons.ts"));

for (const [name, svg] of pkg) {
  if (template.has(name) && template.get(name) !== svg) throw new Error(`${name} verschilt tussen template en packages/ribbon`);
}
const unknown = [...template.keys()].filter((n) => !MAP[n]);
if (unknown.length) throw new Error(`Geen id voor: ${unknown.join(", ")}`);

const entries = [...template].map(([name, svg]) => {
  const [id, nl, en, tags] = MAP[name];
  return { id, svg, label: { nl, en }, tags, source: "openaec" };
});
const iconsDir = repoPath("design", "icons");
const { written, duplicates } = importIcons(entries, iconsDir);
writeFileSync(repoPath("design", "icons", "icons.toml"), manifestToml(written), "utf8");
console.log(`${written.length} iconen geschreven`);
for (const [a, b] of duplicates) console.log(`dubbel: ${a} = ${b} (overgeslagen)`);
```

- [ ] **Step 6: Import draaien en valideren**

Run: `node generators/icons/import-openaec.mjs && node -e "import('./generators/icons/manifest.mjs').then(m=>console.log(m.loadIconManifest('design/icons').length))"`
Expected: `42 iconen geschreven` (of minder met "dubbel:"-regels) en daarna hetzelfde aantal uit het manifest, zonder fouten. Bij "dubbel": controleer visueel of het echt hetzelfde icoon is; zo ja, is overslaan correct.

- [ ] **Step 7: Commit**

```bash
git add design/icons generators
git commit -m "feat(icons): eigen iconen verzameld in design/icons

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Iconen naar React — package `@openaec/icons`

**Files:**
- Create: `generators/icons/react.mjs`, `generators/test/icons-react.test.mjs`
- Create: `packages/icons/package.json`, `packages/icons/README.md`, `packages/icons/tsconfig.json`, `packages/icons/src/index.ts`, `packages/icons/src/Icon.tsx`
- Generated: `packages/icons/src/generated/icons.ts`, `packages/icons/src/generated/by-id.ts`
- Modify: `generators/generate.mjs`

**Interfaces:**
- Consumes: `loadIconManifest` (Task 4).
- Produces: `exportName(id): string` (`"view/fit-all"` → `"viewFitAll"`), `renderIconsTs(icons): string`, `renderIconsByIdTs(icons): string`. React-API: benoemde exports per icoon (`editUndo: string`), `type IconId`, `iconIds: readonly IconId[]`, `iconsById: Record<IconId, string>` (aparte module), component `<Icon svg={…} size={20} title="…" />`.

- [ ] **Step 1: Failing test** — `generators/test/icons-react.test.mjs`

```js
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
```

- [ ] **Step 2: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — module ontbreekt.

- [ ] **Step 3: `generators/icons/react.mjs`**

```js
export function exportName(id) {
  return id.split(/[/-]/).map((p, i) => (i === 0 ? p : p[0].toUpperCase() + p.slice(1))).join("");
}

export function renderIconsTs(icons) {
  let out = "";
  for (const icon of icons) {
    out += `/** ${icon.label.nl} — ${icon.label.en} (\`${icon.id}\`) */\n`;
    out += `export const ${exportName(icon.id)} = ${JSON.stringify(icon.svg)};\n`;
  }
  out += `\nexport type IconId = ${icons.map((i) => JSON.stringify(i.id)).join(" | ")};\n`;
  out += `\nexport const iconIds: readonly IconId[] = [${icons.map((i) => JSON.stringify(i.id)).join(", ")}];\n`;
  return out;
}

export function renderIconsByIdTs(icons) {
  let out = `import type { IconId } from "./icons";\nimport {\n`;
  for (const i of icons) out += `  ${exportName(i.id)},\n`;
  out += `} from "./icons";\n\n/** Alle iconen per id. Importeer dit alleen als je iconen dynamisch op id opzoekt. */\nexport const iconsById: Record<IconId, string> = {\n`;
  for (const i of icons) out += `  ${JSON.stringify(i.id)}: ${exportName(i.id)},\n`;
  return out + "};\n";
}
```

- [ ] **Step 4: Package-bestanden**

`packages/icons/package.json`:
```json
{
  "name": "@openaec/icons",
  "version": "0.1.0",
  "description": "OpenAEC-iconen als SVG-strings en React-component",
  "license": "MIT",
  "author": "OpenAEC Foundation",
  "repository": {
    "type": "git",
    "url": "https://github.com/OpenAEC-Foundation/OpenAEC-style-book",
    "directory": "packages/icons"
  },
  "type": "module",
  "sideEffects": false,
  "main": "src/index.ts",
  "types": "src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./by-id": "./src/generated/by-id.ts"
  },
  "files": ["src/", "README.md"],
  "peerDependencies": { "react": ">=18" },
  "devDependencies": { "@types/react": "^19.0.0", "typescript": "^5.6.0" }
}
```

Controleer of de bestaande packages (`packages/ribbon/package.json`) TypeScript-bron publiceren zonder build (`"main": "src/index.ts"`); zo ja, volg dat patroon zoals hierboven. Zo niet, neem hun build-opzet over.

`packages/icons/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

`packages/icons/src/Icon.tsx`:
```tsx
import type { CSSProperties } from "react";

export interface IconProps {
  /** SVG-string, bijv. `editUndo` uit `@openaec/icons`. */
  svg: string;
  /** Breedte en hoogte in px (standaard 20). */
  size?: number;
  /** Toegankelijke naam; zonder title is het icoon decoratief. */
  title?: string;
  className?: string;
  style?: CSSProperties;
}

export function Icon({ svg, size = 20, title, className, style }: IconProps) {
  return (
    <span
      className={className}
      role={title ? "img" : undefined}
      aria-label={title}
      aria-hidden={title ? undefined : true}
      style={{ display: "inline-flex", width: size, height: size, ...style }}
      dangerouslySetInnerHTML={{ __html: svg.replace("<svg ", `<svg width="${size}" height="${size}" `) }}
    />
  );
}
```

`packages/icons/src/index.ts`:
```ts
export * from "./generated/icons";
export { Icon } from "./Icon";
export type { IconProps } from "./Icon";
```

`packages/icons/README.md`:
```markdown
# @openaec/icons

OpenAEC-iconen. Bron: [`design/icons/`](../../design/icons/) — voeg daar iconen toe,
niet hier. `src/generated/` wordt gemaakt door `npm run generate`.

```tsx
import { Icon, editUndo } from "@openaec/icons";

<Icon svg={editUndo} size={20} title="Ongedaan maken" />
```

Iconen zijn `currentColor`: ze nemen de tekstkleur van hun omgeving over.
Dynamisch op id opzoeken (bijv. vanuit een ribbon-definitie) kan via
`import { iconsById } from "@openaec/icons/by-id"`; dat laadt wel alle iconen.
```

Stap registreren in `generators/generate.mjs`:
```js
import { loadIconManifest } from "./icons/manifest.mjs";
import { renderIconsByIdTs, renderIconsTs } from "./icons/react.mjs";

steps.push(["icons-react", (root) => {
  const icons = loadIconManifest(join(root, "design", "icons"));
  const dir = join(root, "packages", "icons", "src", "generated");
  return [
    writeGenerated(join(dir, "icons.ts"), renderIconsTs(icons)),
    writeGenerated(join(dir, "by-id.ts"), renderIconsByIdTs(icons)),
  ];
}]);
```

- [ ] **Step 5: Tests, generatie en typecheck**

Run: `npm test && npm install && npm run generate && npx -w @openaec/icons tsc -p .`
Expected: tests PASS; generate meldt `icons-react: 2 bestanden`; `tsc` zonder fouten.

- [ ] **Step 6: Commit**

```bash
git add generators packages/icons package-lock.json
git commit -m "feat(icons): React-package @openaec/icons

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Iconen naar Rust — crate `openaec-icons` met render-snapshots

**Files:**
- Create: `generators/icons/rust.mjs`, `generators/test/icons-rust.test.mjs`
- Create: `crates/openaec-icons/Cargo.toml`, `crates/openaec-icons/src/lib.rs`, `crates/openaec-icons/tests/render.rs`
- Generated: `crates/openaec-icons/src/generated.rs`; snapshots `crates/openaec-icons/tests/snapshots/*.png` (via `UPDATE_SNAPSHOTS=1`)
- Modify: `generators/generate.mjs`

**Interfaces:**
- Consumes: `loadIconManifest` (Task 4); `openaec_tokens::{LIGHT, DARK}` (Task 3, dev-dependency).
- Produces: `variantName(id): string` (`"view/fit-all"` → `"ViewFitAll"`), `rawString(s): string`, `renderIconsRust(icons): string`. Rust-API: `enum Icon`, `Icon::ALL: &'static [Icon]`, `Icon::id(self) -> &'static str`, `Icon::svg(self) -> &'static str`, `Icon::label_nl/label_en(self) -> &'static str`, `Icon::has_own_colors(self) -> bool`, `Icon::from_id(&str) -> Option<Icon>`, `Icon::svg_colored(self, hex: &str) -> String`.

- [ ] **Step 1: Failing Node-test** — `generators/test/icons-rust.test.mjs`

```js
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
```

- [ ] **Step 2: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — module ontbreekt.

- [ ] **Step 3: `generators/icons/rust.mjs`**

```js
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
```

- [ ] **Step 4: Crate**

`crates/openaec-icons/Cargo.toml`:
```toml
[package]
name = "openaec-icons"
description = "OpenAEC-iconen als SVG voor Rust-applicaties"
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true
authors.workspace = true

[dev-dependencies]
openaec-tokens = { path = "../openaec-tokens" }
resvg = "0.45"
```

`crates/openaec-icons/src/lib.rs`:
```rust
//! OpenAEC-iconen. Bron: `design/icons/` in OpenAEC-style-book;
//! `generated.rs` wordt door `npm run generate` gemaakt.

mod generated;
pub use generated::Icon;

impl Icon {
    /// SVG met `currentColor` vervangen door een vaste kleur (bijv. `"#36363E"`).
    /// Nodig voor renderers die geen `currentColor` kennen.
    pub fn svg_colored(self, hex: &str) -> String {
        self.svg().replace("currentColor", hex)
    }
}
```

`crates/openaec-icons/tests/render.rs`:
```rust
use openaec_icons::Icon;
use openaec_tokens::{DARK, LIGHT};
use resvg::{tiny_skia, usvg};
use std::path::PathBuf;

const SIZE: u32 = 48;

fn render(svg: &str) -> tiny_skia::Pixmap {
    let tree = usvg::Tree::from_str(svg, &usvg::Options::default()).expect("SVG moet parsen");
    let mut pixmap = tiny_skia::Pixmap::new(SIZE, SIZE).unwrap();
    let scale = SIZE as f32 / tree.size().width();
    resvg::render(&tree, tiny_skia::Transform::from_scale(scale, scale), &mut pixmap.as_mut());
    pixmap
}

fn snapshot_path(icon: Icon, theme: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/snapshots")
        .join(format!("{}.{theme}.png", icon.id().replace('/', "__")))
}

/// Max. 0,5% van de pixels mag meer dan 2 per kanaal afwijken (afrondingsverschillen per platform).
fn close_enough(a: &tiny_skia::Pixmap, b: &tiny_skia::Pixmap) -> bool {
    let diff = a.data().chunks(4).zip(b.data().chunks(4))
        .filter(|(p, q)| p.iter().zip(q.iter()).any(|(x, y)| x.abs_diff(*y) > 2))
        .count();
    diff * 200 <= (SIZE * SIZE) as usize
}

#[test]
fn ids_zijn_uniek_en_terug_te_vinden() {
    for icon in Icon::ALL {
        assert_eq!(Icon::from_id(icon.id()), Some(*icon));
    }
    assert_eq!(Icon::from_id("bestaat/niet"), None);
}

#[test]
fn elk_icoon_rendert_en_komt_overeen_met_snapshot() {
    let update = std::env::var("UPDATE_SNAPSHOTS").is_ok();
    for icon in Icon::ALL {
        for (theme, color) in [("light", LIGHT.text_primary), ("dark", DARK.text_primary)] {
            let pixmap = render(&icon.svg_colored(&color.to_hex()));
            assert!(pixmap.data().iter().skip(3).step_by(4).any(|a| *a > 0), "{} rendert leeg", icon.id());
            let path = snapshot_path(*icon, theme);
            if update {
                std::fs::create_dir_all(path.parent().unwrap()).unwrap();
                pixmap.save_png(&path).unwrap();
                continue;
            }
            let expected = tiny_skia::Pixmap::load_png(&path)
                .unwrap_or_else(|_| panic!("snapshot ontbreekt: {} — draai met UPDATE_SNAPSHOTS=1", path.display()));
            assert!(close_enough(&pixmap, &expected), "{} ({theme}) wijkt af van snapshot", icon.id());
        }
    }
}
```

Stap registreren in `generators/generate.mjs`:
```js
import { renderIconsRust } from "./icons/rust.mjs";

steps.push(["icons-rust", (root) => [
  writeGenerated(join(root, "crates", "openaec-icons", "src", "generated.rs"),
    renderIconsRust(loadIconManifest(join(root, "design", "icons")))),
]]);
```

- [ ] **Step 5: Tests draaien en snapshots maken**

Run: `npm test && npm run generate && UPDATE_SNAPSHOTS=1 cargo test -p openaec-icons && cargo test -p openaec-icons`
Expected: Node PASS; eerste cargo-run schrijft 84 PNG's (42 iconen × 2 thema's); tweede run PASS (2 tests). Bekijk een paar PNG's (bijv. `edit__undo.light.png`) om te zien dat ze kloppen.

(Op Windows-PowerShell: `$env:UPDATE_SNAPSHOTS=1; cargo test -p openaec-icons; Remove-Item Env:UPDATE_SNAPSHOTS`.)

- [ ] **Step 6: Commit**

```bash
git add generators crates/openaec-icons Cargo.lock
git commit -m "feat(icons): Rust-crate openaec-icons met render-snapshots

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Gedeelde termen (i18n) — `@openaec/i18n` en `openaec-i18n`

**Files:**
- Create: `design/i18n/nl/openaec.json`, `design/i18n/en/openaec.json`
- Create: `generators/i18n/load.mjs`, `generators/i18n/rust.mjs`, `generators/test/i18n.test.mjs`
- Create: `packages/i18n/package.json`, `packages/i18n/README.md`, `packages/i18n/src/index.ts`
- Create: `crates/openaec-i18n/Cargo.toml`, `crates/openaec-i18n/src/lib.rs`, `crates/openaec-i18n/tests/i18n.rs`
- Generated: `packages/i18n/src/generated/nl.json`, `packages/i18n/src/generated/en.json`, `crates/openaec-i18n/src/generated.rs`
- Modify: `generators/generate.mjs`

**Interfaces:**
- Produces:
  - `flatten(obj, prefix?): Map<string,string>` (`{ action: { copy } }` → `"action.copy"`), `loadI18n(i18nDir): { nl: Map, en: Map }` (gooit bij ongelijke sleutels of lege waarden), `renderI18nRust({ nl, en }): string`.
  - Rust: `enum Lang { Nl, En }`, `t(lang, key) -> Option<&'static str>`, `has_key(key) -> bool`, `KEYS: &[&str]`.
  - React: `openaecResources = { nl: { openaec: {...} }, en: { openaec: {...} } }` voor i18next (namespace `openaec`).
  - Sleutelconventie in ribbons: label `"openaec.<sleutel>"` verwijst naar deze gedeelde termen.

- [ ] **Step 1: Bronbestanden**

`design/i18n/nl/openaec.json`:
```json
{
  "action": {
    "ok": "OK", "cancel": "Annuleren", "save": "Opslaan", "save-as": "Opslaan als",
    "close": "Sluiten", "delete": "Verwijderen", "edit": "Bewerken", "apply": "Toepassen",
    "reset": "Herstellen", "yes": "Ja", "no": "Nee", "export": "Exporteren",
    "import": "Importeren", "print": "Afdrukken", "copy": "Kopiëren", "cut": "Knippen",
    "paste": "Plakken", "undo": "Ongedaan maken", "redo": "Opnieuw", "search": "Zoeken",
    "open": "Openen", "new": "Nieuw", "preferences": "Voorkeuren"
  },
  "window": { "minimize": "Minimaliseren", "maximize": "Maximaliseren", "restore": "Herstellen" },
  "status": { "ready": "Gereed" },
  "panel": { "explorer": "Verkenner", "properties": "Eigenschappen" },
  "ribbon": {
    "tab": { "file": "Bestand", "help": "Help", "viewer3d": "3D Viewer" },
    "group": { "file": "Bestand", "navigation": "Navigatie", "analysis": "Analyse", "display": "Weergave" }
  },
  "command": {
    "view": {
      "load-model": "Model laden", "orbit": "Roteren", "fit-all": "Passend",
      "section": "Doorsnede", "measure": "Meten", "wireframe": "Draadmodel"
    }
  }
}
```

`design/i18n/en/openaec.json`:
```json
{
  "action": {
    "ok": "OK", "cancel": "Cancel", "save": "Save", "save-as": "Save as",
    "close": "Close", "delete": "Delete", "edit": "Edit", "apply": "Apply",
    "reset": "Reset", "yes": "Yes", "no": "No", "export": "Export",
    "import": "Import", "print": "Print", "copy": "Copy", "cut": "Cut",
    "paste": "Paste", "undo": "Undo", "redo": "Redo", "search": "Search",
    "open": "Open", "new": "New", "preferences": "Preferences"
  },
  "window": { "minimize": "Minimize", "maximize": "Maximize", "restore": "Restore" },
  "status": { "ready": "Ready" },
  "panel": { "explorer": "Explorer", "properties": "Properties" },
  "ribbon": {
    "tab": { "file": "File", "help": "Help", "viewer3d": "3D Viewer" },
    "group": { "file": "File", "navigation": "Navigation", "analysis": "Analysis", "display": "Display" }
  },
  "command": {
    "view": {
      "load-model": "Load model", "orbit": "Orbit", "fit-all": "Fit all",
      "section": "Section", "measure": "Measure", "wireframe": "Wireframe"
    }
  }
}
```

- [ ] **Step 2: Failing test** — `generators/test/i18n.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { flatten, loadI18n } from "../i18n/load.mjs";
import { renderI18nRust } from "../i18n/rust.mjs";
import { repoPath } from "../lib/paths.mjs";

test("flatten maakt puntsleutels", () => {
  assert.deepEqual([...flatten({ a: { b: "x", c: { d: "y" } } })], [["a.b", "x"], ["a.c.d", "y"]]);
});

test("ontbrekende of lege vertaling wordt gemeld", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-i18n-"));
  mkdirSync(join(dir, "nl")); mkdirSync(join(dir, "en"));
  writeFileSync(join(dir, "nl", "openaec.json"), JSON.stringify({ a: "x", b: "y" }));
  writeFileSync(join(dir, "en", "openaec.json"), JSON.stringify({ a: "" }));
  assert.throws(() => loadI18n(dir), (e) => /b \(en ontbreekt\)/.test(e.message) && /a \(en leeg\)/.test(e.message));
});

test("echte bron is volledig en niet-ASCII blijft heel", () => {
  const { nl } = loadI18n(repoPath("design", "i18n"));
  assert.equal(nl.get("action.copy"), "Kopiëren");
  const rs = renderI18nRust(loadI18n(repoPath("design", "i18n")));
  assert.match(rs, /"action\.copy" => Some\("Kopiëren"\)/);
});
```

- [ ] **Step 3: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — module ontbreekt.

- [ ] **Step 4: Implementatie**

`generators/i18n/load.mjs`:
```js
import { readFileSync } from "node:fs";
import { join } from "node:path";

export const LANGS = ["nl", "en"];

export function flatten(obj, prefix = "") {
  const out = new Map();
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === "object") for (const [kk, vv] of flatten(v, key)) out.set(kk, vv);
    else out.set(key, String(v));
  }
  return out;
}

export function loadI18n(i18nDir) {
  const maps = Object.fromEntries(LANGS.map((l) =>
    [l, flatten(JSON.parse(readFileSync(join(i18nDir, l, "openaec.json"), "utf8")))]));
  const all = new Set(LANGS.flatMap((l) => [...maps[l].keys()]));
  const errors = [];
  for (const key of [...all].sort()) {
    for (const l of LANGS) {
      if (!maps[l].has(key)) errors.push(`${key} (${l} ontbreekt)`);
      else if (!maps[l].get(key).trim()) errors.push(`${key} (${l} leeg)`);
    }
  }
  if (errors.length) throw new Error(`Vertalingen onvolledig: ${errors.join(", ")}`);
  return maps;
}
```

`generators/i18n/rust.mjs`:
```js
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
```

`crates/openaec-i18n/Cargo.toml`:
```toml
[package]
name = "openaec-i18n"
description = "Gedeelde OpenAEC-termen (nl, en) voor Rust-applicaties"
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true
authors.workspace = true
```

`crates/openaec-i18n/src/lib.rs`:
```rust
//! Gedeelde OpenAEC-termen. Bron: `design/i18n/` in OpenAEC-style-book.

mod generated;
pub use generated::KEYS;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Lang {
    Nl,
    En,
}

/// Vertaling van een gedeelde sleutel, bijv. `t(Lang::Nl, "action.copy")`.
/// Het voorvoegsel `openaec.` mag erbij staan of weggelaten worden.
pub fn t(lang: Lang, key: &str) -> Option<&'static str> {
    let key = key.strip_prefix("openaec.").unwrap_or(key);
    match lang {
        Lang::Nl => generated::nl(key),
        Lang::En => generated::en(key),
    }
}

/// `true` als de sleutel in alle talen bestaat (de generator garandeert gelijke sleutels).
pub fn has_key(key: &str) -> bool {
    t(Lang::Nl, key).is_some()
}
```

`crates/openaec-i18n/tests/i18n.rs`:
```rust
use openaec_i18n::{has_key, t, Lang, KEYS};

#[test]
fn vertalingen() {
    assert_eq!(t(Lang::Nl, "action.copy"), Some("Kopiëren"));
    assert_eq!(t(Lang::En, "openaec.action.copy"), Some("Copy"));
    assert_eq!(t(Lang::Nl, "bestaat.niet"), None);
}

#[test]
fn alle_sleutels_in_beide_talen() {
    for key in KEYS {
        assert!(t(Lang::Nl, key).is_some() && t(Lang::En, key).is_some(), "{key}");
        assert!(has_key(key));
    }
}
```

`packages/i18n/package.json`:
```json
{
  "name": "@openaec/i18n",
  "version": "0.1.0",
  "description": "Gedeelde OpenAEC-termen (nl, en) voor i18next",
  "license": "MIT",
  "author": "OpenAEC Foundation",
  "repository": {
    "type": "git",
    "url": "https://github.com/OpenAEC-Foundation/OpenAEC-style-book",
    "directory": "packages/i18n"
  },
  "type": "module",
  "sideEffects": false,
  "main": "src/index.ts",
  "types": "src/index.ts",
  "files": ["src/", "README.md"]
}
```

`packages/i18n/src/index.ts`:
```ts
import nl from "./generated/nl.json";
import en from "./generated/en.json";

/** i18next-resources met namespace `openaec`: `t("openaec:action.copy")`. */
export const openaecResources = {
  nl: { openaec: nl },
  en: { openaec: en },
} as const;
```

`packages/i18n/README.md`:
```markdown
# @openaec/i18n

Gedeelde OpenAEC-termen in het Nederlands en Engels. Bron:
[`design/i18n/`](../../design/i18n/); `src/generated/` wordt gemaakt door
`npm run generate`.

```ts
import i18next from "i18next";
import { openaecResources } from "@openaec/i18n";

i18next.init({ resources: openaecResources, ns: ["openaec", "app"] });
i18next.t("openaec:action.copy"); // "Kopiëren"
```
```

Stap registreren in `generators/generate.mjs`:
```js
import { loadI18n } from "./i18n/load.mjs";
import { renderI18nRust } from "./i18n/rust.mjs";
import { readFileSync } from "node:fs";

steps.push(["i18n", (root) => {
  const src = join(root, "design", "i18n");
  const maps = loadI18n(src);
  const out = [];
  for (const lang of ["nl", "en"]) {
    // JSON zonder header; inhoud 1-op-1 uit de bron, opnieuw geformatteerd.
    const json = JSON.stringify(JSON.parse(readFileSync(join(src, lang, "openaec.json"), "utf8")), null, 2);
    out.push(writeGenerated(join(root, "packages", "i18n", "src", "generated", `${lang}.json`), json));
  }
  out.push(writeGenerated(join(root, "crates", "openaec-i18n", "src", "generated.rs"), renderI18nRust(maps)));
  return out;
}]);
```

- [ ] **Step 5: Tests**

Run: `npm test && npm run generate && cargo test -p openaec-i18n`
Expected: PASS (Node en 2 Rust-tests).

- [ ] **Step 6: Commit**

```bash
git add design/i18n generators packages/i18n crates/openaec-i18n Cargo.lock package-lock.json
git commit -m "feat(i18n): gedeelde termen voor React en Rust

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Ribbon-formaat — crate `openaec-ribbon` met validator en CLI

**Files:**
- Create: `design/ribbons/viewer3d.toml`
- Create: `generators/ribbons/rust.mjs`, `generators/test/ribbons.test.mjs`
- Create: `crates/openaec-ribbon/Cargo.toml`, `crates/openaec-ribbon/src/lib.rs`, `crates/openaec-ribbon/src/model.rs`, `crates/openaec-ribbon/src/validate.rs`, `crates/openaec-ribbon/src/main.rs`, `crates/openaec-ribbon/tests/validate.rs`, `crates/openaec-ribbon/tests/fixtures/*.toml`
- Generated: `crates/openaec-ribbon/src/generated.rs`
- Modify: `generators/generate.mjs`

**Interfaces:**
- Consumes: `openaec_icons::Icon::from_id` (Task 7), `openaec_i18n::has_key` (Task 8).
- Produces (Rust):
  - Model: `RibbonFile { app, format, include, quick_access, tabs }`, `SharedTabFile { shared, format, tabs }`, `Tab { id, label, contextual, groups }`, `Group { id, label, items }`, `Item { kind: ItemKind, command, icon, label, shortcut, tooltip, slot, items: Vec<MenuEntry> }`, `ItemKind { Large, Small, Toggle, Dropdown, LargeDropdown, Split, Combo, Custom }`, `MenuEntry { command, icon, label, shortcut }`, `QuickAccess { items }`.
  - `parse_ribbon(src: &str) -> Result<RibbonFile, String>`, `parse_shared(src: &str) -> Result<SharedTabFile, String>`.
  - `AppLabels { nl: HashSet<String>, en: HashSet<String> }` + `AppLabels::from_json(nl: &str, en: &str) -> Result<AppLabels, String>`.
  - `Issue { path: String, message: String }`, `validate_ribbon(&RibbonFile, Option<&AppLabels>) -> Vec<Issue>`, `validate_shared(&SharedTabFile) -> Vec<Issue>`.
  - `shared_tab_source(name: &str) -> Option<&'static str>`, `SHARED_TABS: &[(&str, &str)]` (gegenereerd).
  - `STANDARD_COMMANDS: &[&str]`.
  - CLI: `openaec-ribbon check <ribbon.toml> [--nl <nl.json> --en <en.json>]`, `openaec-ribbon check-shared <map>`; exitcode 0 = geldig, 1 = fouten, 2 = gebruik/IO-fout.

- [ ] **Step 1: Gedeelde tab** — `design/ribbons/viewer3d.toml`

```toml
shared = "viewer3d"
format = 1

[[tab]]
id = "viewer3d"
label = "openaec.ribbon.tab.viewer3d"

  [[tab.group]]
  id = "file"
  label = "openaec.ribbon.group.file"
  items = [
    { type = "large", command = "view.load-model", icon = "view/load-model", label = "openaec.command.view.load-model" },
  ]

  [[tab.group]]
  id = "navigation"
  label = "openaec.ribbon.group.navigation"
  items = [
    { type = "toggle", command = "view.orbit", icon = "view/orbit", label = "openaec.command.view.orbit" },
    { type = "large", command = "view.fit-all", icon = "view/fit-all", label = "openaec.command.view.fit-all" },
  ]

  [[tab.group]]
  id = "analysis"
  label = "openaec.ribbon.group.analysis"
  items = [
    { type = "toggle", command = "view.section", icon = "view/section", label = "openaec.command.view.section" },
    { type = "toggle", command = "view.measure", icon = "view/measure", label = "openaec.command.view.measure" },
  ]

  [[tab.group]]
  id = "display"
  label = "openaec.ribbon.group.display"
  items = [
    { type = "toggle", command = "view.wireframe", icon = "view/wireframe", label = "openaec.command.view.wireframe" },
  ]
```

- [ ] **Step 2: Generator voor ingebedde gedeelde tabs (test eerst)** — `generators/test/ribbons.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { renderSharedTabsRust } from "../ribbons/rust.mjs";

test("gedeelde tabs worden als ruwe strings ingebed, gesorteerd op naam", () => {
  const rs = renderSharedTabsRust([["viewer3d", 'shared = "viewer3d"\n'], ["ifc", 'shared = "ifc"\n']]);
  assert.match(rs, /\("ifc", r#"shared = "ifc"\n"#\),\n    \("viewer3d"/);
});
```

`generators/ribbons/rust.mjs`:
```js
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { rawString } from "../icons/rust.mjs";

export function readSharedTabs(dir) {
  return readdirSync(dir).filter((f) => f.endsWith(".toml")).sort()
    .map((f) => [f.slice(0, -5), readFileSync(join(dir, f), "utf8").replace(/\r\n?/g, "\n")]);
}

export function renderSharedTabsRust(tabs) {
  const sorted = [...tabs].sort((a, b) => (a[0] < b[0] ? -1 : 1));
  return `/// Gedeelde ribbon-tabs uit \`design/ribbons/\`: (naam, TOML-bron).
pub const SHARED_TABS: &[(&str, &str)] = &[
${sorted.map(([n, src]) => `    (${JSON.stringify(n)}, ${rawString(src)}),`).join("\n")}
];
`;
}
```

Run: `npm test`
Expected: PASS na het toevoegen van de module (eerst FAIL zonder module).

Stap registreren in `generators/generate.mjs`:
```js
import { readSharedTabs, renderSharedTabsRust } from "./ribbons/rust.mjs";

steps.push(["ribbons-rust", (root) => [
  writeGenerated(join(root, "crates", "openaec-ribbon", "src", "generated.rs"),
    renderSharedTabsRust(readSharedTabs(join(root, "design", "ribbons")))),
]]);
```

- [ ] **Step 3: Failing Rust-tests** — fixtures en `crates/openaec-ribbon/tests/validate.rs`

`crates/openaec-ribbon/tests/fixtures/valid.toml`:
```toml
app = "voorbeeld-app"
format = 1
include = ["openaec:viewer3d"]

[quick_access]
items = ["file.save", "edit.undo", "view.fit-all"]

[[tab]]
id = "home"
label = "app.tab.home"

  [[tab.group]]
  id = "clipboard"
  label = "app.group.clipboard"
  items = [
    { type = "large", command = "edit.paste", icon = "edit/paste", label = "openaec.action.paste" },
    { type = "small", command = "edit.cut", icon = "edit/cut", label = "openaec.action.cut" },
    { type = "small", command = "edit.copy", icon = "edit/copy", label = "openaec.action.copy" },
    { type = "split", command = "insert.table", icon = "insert/table", label = "app.cmd.table", items = [
        { command = "insert.table.grid", label = "app.cmd.table.grid" } ] },
  ]

  [[tab.group]]
  id = "custom"
  label = "app.group.custom"
  items = [ { type = "custom", slot = "layer-combo" } ]
```

`crates/openaec-ribbon/tests/fixtures/app-nl.json`:
```json
{ "app": { "tab": { "home": "Start" }, "group": { "clipboard": "Klembord", "custom": "Eigen" },
  "cmd": { "table": "Tabel", "table.grid": "Raster" } } }
```
`crates/openaec-ribbon/tests/fixtures/app-en.json`:
```json
{ "app": { "tab": { "home": "Home" }, "group": { "clipboard": "Clipboard", "custom": "Custom" },
  "cmd": { "table": "Table", "table.grid": "Grid" } } }
```

`crates/openaec-ribbon/tests/validate.rs`:
```rust
use openaec_ribbon::*;

fn fixture(name: &str) -> String {
    std::fs::read_to_string(format!("{}/tests/fixtures/{name}", env!("CARGO_MANIFEST_DIR"))).unwrap()
}

fn labels() -> AppLabels {
    AppLabels::from_json(&fixture("app-nl.json"), &fixture("app-en.json")).unwrap()
}

fn issues(src: &str) -> Vec<String> {
    let file = parse_ribbon(src).expect("parse");
    validate_ribbon(&file, Some(&labels())).into_iter().map(|i| format!("{}: {}", i.path, i.message)).collect()
}

#[test]
fn geldige_ribbon_heeft_geen_fouten() {
    assert_eq!(issues(&fixture("valid.toml")), Vec::<String>::new());
}

#[test]
fn onbekend_veld_is_een_parsefout() {
    let src = fixture("valid.toml").replace("icon = \"edit/paste\"", "icn = \"edit/paste\"");
    let err = parse_ribbon(&src).unwrap_err();
    assert!(err.contains("icn"), "{err}");
}

#[test]
fn onbekend_icoon_en_ontbrekend_label() {
    let src = fixture("valid.toml")
        .replace("icon = \"edit/cut\"", "icon = \"edit/bestaat-niet\"")
        .replace("label = \"app.cmd.table\"", "label = \"app.cmd.ontbreekt\"");
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("edit/bestaat-niet") && m.contains("onbekend icoon")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("app.cmd.ontbreekt") && m.contains("ontbreekt in nl")), "{found:?}");
}

#[test]
fn verplichte_en_verboden_velden_per_type() {
    let src = fixture("valid.toml").replace(
        "{ type = \"custom\", slot = \"layer-combo\" }",
        "{ type = \"custom\", slot = \"layer-combo\", label = \"app.group.custom\" }, { type = \"large\", command = \"x.y\", label = \"app.group.custom\" }",
    );
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("custom") && m.contains("label is niet toegestaan")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("icon is verplicht")), "{found:?}");
}

#[test]
fn dubbele_ids_onbekende_include_en_quick_access() {
    let src = fixture("valid.toml")
        .replace("include = [\"openaec:viewer3d\"]", "include = [\"openaec:viewer3d\", \"openaec:bestaat-niet\"]")
        .replace("id = \"custom\"", "id = \"clipboard\"")
        .replace("\"view.fit-all\"]", "\"view.fit-all\", \"nergens.gedefinieerd\"]");
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("openaec:bestaat-niet")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("dubbele groep-id clipboard")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("nergens.gedefinieerd")), "{found:?}");
}

#[test]
fn gedeelde_tabs_zijn_geldig() {
    for (name, src) in SHARED_TABS {
        let file = parse_shared(src).unwrap_or_else(|e| panic!("{name}: {e}"));
        assert_eq!(file.shared, *name);
        assert!(validate_shared(&file).is_empty(), "{name}: {:?}", validate_shared(&file));
    }
}
```

- [ ] **Step 4: Tests draaien en zien falen**

Run: `npm run generate && cargo test -p openaec-ribbon`
Expected: FAIL — crate bestaat nog niet / compileert niet.

- [ ] **Step 5: Crate implementeren**

`crates/openaec-ribbon/Cargo.toml`:
```toml
[package]
name = "openaec-ribbon"
description = "Model en validatie van ribbon.toml voor OpenAEC-applicaties"
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true
authors.workspace = true

[dependencies]
openaec-icons = { path = "../openaec-icons" }
openaec-i18n = { path = "../openaec-i18n" }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
toml = "0.8"
```

`crates/openaec-ribbon/src/model.rs`:
```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RibbonFile {
    pub app: String,
    pub format: u32,
    #[serde(default)]
    pub include: Vec<String>,
    pub quick_access: Option<QuickAccess>,
    #[serde(default, rename = "tab")]
    pub tabs: Vec<Tab>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SharedTabFile {
    pub shared: String,
    pub format: u32,
    #[serde(rename = "tab")]
    pub tabs: Vec<Tab>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct QuickAccess {
    pub items: Vec<String>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Tab {
    pub id: String,
    pub label: String,
    pub contextual: Option<String>,
    #[serde(default, rename = "group")]
    pub groups: Vec<Group>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Group {
    pub id: String,
    pub label: String,
    #[serde(default)]
    pub items: Vec<Item>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum ItemKind {
    Large,
    Small,
    Toggle,
    Dropdown,
    LargeDropdown,
    Split,
    Combo,
    Custom,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Item {
    #[serde(rename = "type")]
    pub kind: ItemKind,
    pub command: Option<String>,
    pub icon: Option<String>,
    pub label: Option<String>,
    pub shortcut: Option<String>,
    pub tooltip: Option<String>,
    pub slot: Option<String>,
    #[serde(default)]
    pub items: Vec<MenuEntry>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct MenuEntry {
    pub command: String,
    pub icon: Option<String>,
    pub label: String,
    pub shortcut: Option<String>,
}
```

`crates/openaec-ribbon/src/validate.rs`:
```rust
use crate::model::*;
use std::collections::HashSet;

/// Commands die elke app via de vaste schil heeft en dus in quick access mogen staan.
pub const STANDARD_COMMANDS: &[&str] = &[
    "file.new", "file.open", "file.save", "file.save-as", "file.print", "edit.undo", "edit.redo",
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Issue {
    pub path: String,
    pub message: String,
}

/// Labels van de app zelf (alles wat niet met `openaec.` begint), per taal als puntsleutels.
#[derive(Debug, Default)]
pub struct AppLabels {
    pub nl: HashSet<String>,
    pub en: HashSet<String>,
}

impl AppLabels {
    pub fn from_json(nl: &str, en: &str) -> Result<Self, String> {
        Ok(Self { nl: flatten_json(nl)?, en: flatten_json(en)? })
    }
}

fn flatten_json(src: &str) -> Result<HashSet<String>, String> {
    let value: serde_json::Value = serde_json::from_str(src).map_err(|e| e.to_string())?;
    let mut out = HashSet::new();
    fn walk(v: &serde_json::Value, prefix: &str, out: &mut HashSet<String>) {
        match v {
            serde_json::Value::Object(map) => {
                for (k, vv) in map {
                    let key = if prefix.is_empty() { k.clone() } else { format!("{prefix}.{k}") };
                    walk(vv, &key, out);
                }
            }
            _ => {
                out.insert(prefix.to_string());
            }
        }
    }
    walk(&value, "", &mut out);
    Ok(out)
}

struct Checker<'a> {
    issues: Vec<Issue>,
    labels: Option<&'a AppLabels>,
    commands: HashSet<String>,
}

fn is_id(s: &str) -> bool {
    let mut chars = s.chars();
    matches!(chars.next(), Some('a'..='z')) && chars.all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-')
}

fn is_command(s: &str) -> bool {
    let parts: Vec<&str> = s.split('.').collect();
    parts.len() >= 2 && is_id(parts[0]) && parts[1..].iter().all(|p| !p.is_empty() && p.chars().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-'))
}

impl<'a> Checker<'a> {
    fn err(&mut self, path: &str, message: impl Into<String>) {
        self.issues.push(Issue { path: path.to_string(), message: message.into() });
    }

    fn label(&mut self, path: &str, key: &str) {
        if let Some(shared) = key.strip_prefix("openaec.") {
            if !openaec_i18n::has_key(shared) {
                self.err(path, format!("onbekende gedeelde term {key}"));
            }
            return;
        }
        if let Some(labels) = self.labels {
            if !labels.nl.contains(key) { self.err(path, format!("label {key} ontbreekt in nl")); }
            if !labels.en.contains(key) { self.err(path, format!("label {key} ontbreekt in en")); }
        }
    }

    fn icon(&mut self, path: &str, id: &str) {
        if openaec_icons::Icon::from_id(id).is_none() {
            self.err(path, format!("onbekend icoon {id}"));
        }
    }

    fn command(&mut self, path: &str, cmd: &str) {
        if !is_command(cmd) { self.err(path, format!("ongeldige command-naam {cmd}")); }
        self.commands.insert(cmd.to_string());
    }

    fn item(&mut self, path: &str, item: &Item) {
        use ItemKind::*;
        // (command, icon, label, items, slot): Some(true)=verplicht, Some(false)=verboden, None=optioneel
        let rule: [Option<bool>; 5] = match item.kind {
            Large | Small | Toggle => [Some(true), Some(true), Some(true), Some(false), Some(false)],
            Dropdown => [Some(false), None, Some(true), Some(true), Some(false)],
            LargeDropdown => [Some(false), Some(true), Some(true), Some(true), Some(false)],
            Split => [Some(true), Some(true), Some(true), Some(true), Some(false)],
            Combo => [Some(true), None, Some(true), Some(false), Some(false)],
            Custom => [Some(false), Some(false), Some(false), Some(false), Some(true)],
        };
        let kind = match item.kind {
            Large => "large", Small => "small", Toggle => "toggle", Dropdown => "dropdown",
            LargeDropdown => "large-dropdown", Split => "split", Combo => "combo", Custom => "custom",
        };
        let present = [item.command.is_some(), item.icon.is_some(), item.label.is_some(), !item.items.is_empty(), item.slot.is_some()];
        for (i, name) in ["command", "icon", "label", "items", "slot"].iter().enumerate() {
            match (rule[i], present[i]) {
                (Some(true), false) => self.err(path, format!("{kind}: {name} is verplicht")),
                (Some(false), true) => self.err(path, format!("{kind}: {name} is niet toegestaan")),
                _ => {}
            }
        }
        if let Some(c) = &item.command { self.command(path, c); }
        if let Some(i) = &item.icon { self.icon(path, i); }
        if let Some(l) = &item.label { self.label(path, l); }
        for (n, e) in item.items.iter().enumerate() {
            let p = format!("{path}.items[{n}]");
            self.command(&p, &e.command);
            if let Some(i) = &e.icon { self.icon(&p, i); }
            self.label(&p, &e.label);
        }
    }

    fn tabs(&mut self, prefix: &str, tabs: &[Tab], seen_tabs: &mut HashSet<String>) {
        for tab in tabs {
            let tp = format!("{prefix}tab[{}]", tab.id);
            if !is_id(&tab.id) { self.err(&tp, format!("ongeldig tab-id {}", tab.id)); }
            if !seen_tabs.insert(tab.id.clone()) { self.err(&tp, format!("dubbele tab-id {}", tab.id)); }
            self.label(&tp, &tab.label);
            let mut seen_groups = HashSet::new();
            for group in &tab.groups {
                let gp = format!("{tp}.group[{}]", group.id);
                if !is_id(&group.id) { self.err(&gp, format!("ongeldig groep-id {}", group.id)); }
                if !seen_groups.insert(group.id.clone()) { self.err(&gp, format!("dubbele groep-id {}", group.id)); }
                self.label(&gp, &group.label);
                for (n, item) in group.items.iter().enumerate() {
                    self.item(&format!("{gp}.items[{n}]"), item);
                }
            }
        }
    }
}

pub fn validate_ribbon(file: &RibbonFile, labels: Option<&AppLabels>) -> Vec<Issue> {
    let mut c = Checker { issues: vec![], labels, commands: HashSet::new() };
    if file.format != 1 { c.err("format", format!("onbekend formaat {}", file.format)); }
    if !is_id(&file.app) { c.err("app", format!("ongeldige app-id {}", file.app)); }
    let mut seen_tabs = HashSet::new();
    for inc in &file.include {
        match inc.strip_prefix("openaec:").and_then(crate::shared_tab_source) {
            Some(src) => match crate::parse_shared(src) {
                Ok(shared) => c.tabs(&format!("include[{inc}]."), &shared.tabs, &mut seen_tabs),
                Err(e) => c.err("include", format!("{inc}: {e}")),
            },
            None => c.err("include", format!("onbekende gedeelde tab {inc}")),
        }
    }
    c.tabs("", &file.tabs, &mut seen_tabs);
    if let Some(qa) = &file.quick_access {
        for cmd in &qa.items {
            if !c.commands.contains(cmd) && !STANDARD_COMMANDS.contains(&cmd.as_str()) {
                c.err("quick_access", format!("command {cmd} staat niet in de ribbon en is geen standaard-command"));
            }
        }
    }
    c.issues
}

pub fn validate_shared(file: &SharedTabFile) -> Vec<Issue> {
    let mut c = Checker { issues: vec![], labels: None, commands: HashSet::new() };
    if file.format != 1 { c.err("format", format!("onbekend formaat {}", file.format)); }
    for tab in &file.tabs {
        let all_shared = std::iter::once(&tab.label)
            .chain(tab.groups.iter().map(|g| &g.label))
            .chain(tab.groups.iter().flat_map(|g| g.items.iter().filter_map(|i| i.label.as_ref())))
            .all(|l| l.starts_with("openaec."));
        if !all_shared { c.err(&format!("tab[{}]", tab.id), "gedeelde tabs gebruiken alleen openaec.*-labels"); }
    }
    c.tabs("", &file.tabs, &mut HashSet::new());
    c.issues
}
```

`crates/openaec-ribbon/src/lib.rs`:
```rust
//! Model en validatie van `ribbon.toml` (formaat 1) voor OpenAEC-applicaties.
//! Specificatie: `docs/superpowers/specs/2026-10-15-ui-fundament-design.md` §5.

mod generated;
mod model;
mod validate;

pub use generated::SHARED_TABS;
pub use model::*;
pub use validate::{validate_ribbon, validate_shared, AppLabels, Issue, STANDARD_COMMANDS};

pub fn parse_ribbon(src: &str) -> Result<RibbonFile, String> {
    toml::from_str(src).map_err(|e| e.to_string())
}

pub fn parse_shared(src: &str) -> Result<SharedTabFile, String> {
    toml::from_str(src).map_err(|e| e.to_string())
}

pub fn shared_tab_source(name: &str) -> Option<&'static str> {
    SHARED_TABS.iter().find(|(n, _)| *n == name).map(|(_, src)| *src)
}
```

`crates/openaec-ribbon/src/main.rs`:
```rust
use openaec_ribbon::*;
use std::process::ExitCode;

fn read(path: &str) -> Result<String, String> {
    std::fs::read_to_string(path).map_err(|e| format!("{path}: {e}"))
}

fn report(name: &str, issues: &[Issue]) -> bool {
    for i in issues {
        eprintln!("{name}: {}: {}", i.path, i.message);
    }
    issues.is_empty()
}

fn run(args: &[String]) -> Result<bool, String> {
    match args.first().map(String::as_str) {
        Some("check") => {
            let file = args.get(1).ok_or("gebruik: openaec-ribbon check <ribbon.toml> [--nl <nl.json> --en <en.json>]")?;
            let opt = |flag: &str| args.iter().position(|a| a == flag).and_then(|i| args.get(i + 1));
            let labels = match (opt("--nl"), opt("--en")) {
                (Some(nl), Some(en)) => Some(AppLabels::from_json(&read(nl)?, &read(en)?)?),
                (None, None) => {
                    eprintln!("let op: app-labels niet gecontroleerd (geef --nl en --en mee)");
                    None
                }
                _ => return Err("--nl en --en horen samen".into()),
            };
            let ribbon = parse_ribbon(&read(file)?).map_err(|e| format!("{file}: {e}"))?;
            Ok(report(file, &validate_ribbon(&ribbon, labels.as_ref())))
        }
        Some("check-shared") => {
            let dir = args.get(1).ok_or("gebruik: openaec-ribbon check-shared <map>")?;
            let mut ok = true;
            let mut entries: Vec<_> = std::fs::read_dir(dir).map_err(|e| e.to_string())?
                .filter_map(|e| e.ok()).map(|e| e.path())
                .filter(|p| p.extension().is_some_and(|x| x == "toml")).collect();
            entries.sort();
            for path in entries {
                let name = path.display().to_string();
                let shared = parse_shared(&read(&name)?).map_err(|e| format!("{name}: {e}"))?;
                ok &= report(&name, &validate_shared(&shared));
            }
            Ok(ok)
        }
        _ => Err("gebruik: openaec-ribbon check|check-shared …".into()),
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match run(&args) {
        Ok(true) => { println!("✓ geldig"); ExitCode::SUCCESS }
        Ok(false) => ExitCode::from(1),
        Err(e) => { eprintln!("{e}"); ExitCode::from(2) }
    }
}
```

- [ ] **Step 6: Tests en CLI draaien**

Run: `npm run generate && cargo test -p openaec-ribbon && cargo run -q -p openaec-ribbon -- check-shared design/ribbons && cargo run -q -p openaec-ribbon -- check crates/openaec-ribbon/tests/fixtures/valid.toml --nl crates/openaec-ribbon/tests/fixtures/app-nl.json --en crates/openaec-ribbon/tests/fixtures/app-en.json`
Expected: 6 tests PASS; beide CLI-aanroepen printen `✓ geldig` met exitcode 0.

Let op: `"table.grid"` in de app-JSON-fixtures is één sleutel met een punt erin; `flatten_json` maakt daarvan `app.cmd.table.grid`, wat overeenkomt met het label. Laat dat zo.

- [ ] **Step 7: Commit**

```bash
git add design/ribbons generators crates/openaec-ribbon Cargo.lock
git commit -m "feat(ribbon): ribbon.toml-model, validator en CLI met gedeelde tab viewer3d

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Fonts en Frappe-thema `openaec_theme`

**Files:**
- Create: `design/fonts/` (TTF's + OFL-licenties)
- Create: `generators/tokens/frappe-css.mjs`, `generators/frappe/build.mjs`, `generators/test/frappe.test.mjs`
- Create: `frappe/openaec_theme/pyproject.toml`, `frappe/openaec_theme/README.md`, `frappe/openaec_theme/license.txt`, `frappe/openaec_theme/openaec_theme/__init__.py`, `frappe/openaec_theme/openaec_theme/hooks.py`, `frappe/openaec_theme/openaec_theme/modules.txt`, `frappe/openaec_theme/openaec_theme/patches.txt`, `frappe/openaec_theme/openaec_theme/openaec_theme/__init__.py`, `frappe/openaec_theme/tests/test_static.py`
- Generated: `frappe/openaec_theme/openaec_theme/public/css/openaec_theme.css`, `…/public/fonts/*`, `…/public/images/openaec-symbol.svg`
- Modify: `generators/generate.mjs`

**Interfaces:**
- Consumes: `loadTokens`, `tokenValue` (Task 3); foundation-symbool uit `design/logos/foundation/` (Task 11 verplaatst de logo's; deze task leest het symbool uit `brandbook/assets/logo/svg/` tot Task 11 klaar is — zie Step 5).
- Produces: `renderFrappeCss(tokens, fonts): string` met `fonts = [{ family, file, weight }]`; Frappe-app met `app_include_css`, `web_include_css`, `app_logo_url`.

- [ ] **Step 1: Fonts naar `design/fonts`**

```bash
mkdir -p design/fonts
cp "project-templates/Tauri+React/src-tauri/tenants/openaec_foundation/fonts/"*.ttf design/fonts/
ls design/fonts
```
Expected: `Inter-Medium.ttf Inter-Regular.ttf Inter-SemiBold.ttf JetBrainsMono-Regular.ttf SpaceGrotesk-Bold.ttf SpaceGrotesk-Medium.ttf`.

Licentieteksten ophalen (SIL OFL 1.1, uit de officiële font-repo's):
```bash
curl -fsSL -o design/fonts/OFL-Inter.txt https://raw.githubusercontent.com/rsms/inter/master/LICENSE.txt
curl -fsSL -o design/fonts/OFL-SpaceGrotesk.txt https://raw.githubusercontent.com/floriankarsten/space-grotesk/master/OFL.txt
curl -fsSL -o design/fonts/OFL-JetBrainsMono.txt https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/OFL.txt
head -3 design/fonts/OFL-*.txt
```
Expected: elk bestand noemt "SIL Open Font License". Faalt een URL (404), zoek in die repo het licentiebestand op de standaardbranch en gebruik dat pad.

- [ ] **Step 2: Failing test** — `generators/test/frappe.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { loadTokens } from "../tokens/load.mjs";
import { renderFrappeCss } from "../tokens/frappe-css.mjs";
import { repoPath } from "../lib/paths.mjs";

const fonts = [
  { family: "Inter", file: "Inter-Regular.ttf", weight: 400 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Bold.ttf", weight: 700 },
];

test("Desk-variabelen voor licht en donker uit de tokens", () => {
  const css = renderFrappeCss(loadTokens(repoPath("design", "tokens")), fonts);
  assert.match(css, /:root,\s*\[data-theme="light"\]\s*\{[^}]*--primary:\s*#D97706;/s);
  assert.match(css, /\[data-theme="light"\][^}]*--bg-color:\s*#FAFAF9;/s);
  assert.match(css, /\[data-theme="dark"\]\s*\{[^}]*--bg-color:\s*#36363E;/s);
  assert.match(css, /--font-stack:\s*'Inter'/);
  assert.match(css, /@font-face\s*\{[^}]*font-family:\s*"Space Grotesk";[^}]*\/assets\/openaec_theme\/fonts\/SpaceGrotesk-Bold\.ttf/s);
});
```

- [ ] **Step 3: Test draaien en zien falen**

Run: `npm test`
Expected: FAIL — module ontbreekt.

- [ ] **Step 4: `generators/tokens/frappe-css.mjs`**

```js
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
```

- [ ] **Step 5: Frappe-app**

`frappe/openaec_theme/pyproject.toml`:
```toml
[project]
name = "openaec_theme"
authors = [{ name = "OpenAEC Foundation" }]
description = "OpenAEC-huisstijl voor Frappe Desk en website"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]
dependencies = []

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[tool.bench.frappe-dependencies]
frappe = ">=15.0.0,<17.0.0"
```

`frappe/openaec_theme/openaec_theme/__init__.py`:
```python
__version__ = "0.1.0"
```

`frappe/openaec_theme/openaec_theme/hooks.py`:
```python
app_name = "openaec_theme"
app_title = "OpenAEC Theme"
app_publisher = "OpenAEC Foundation"
app_description = "OpenAEC-huisstijl voor Frappe Desk en website"
app_license = "MIT"

app_include_css = ["/assets/openaec_theme/css/openaec_theme.css"]
web_include_css = ["/assets/openaec_theme/css/openaec_theme.css"]
app_logo_url = "/assets/openaec_theme/images/openaec-symbol.svg"
```

`frappe/openaec_theme/openaec_theme/modules.txt`:
```
OpenAEC Theme
```
`frappe/openaec_theme/openaec_theme/patches.txt`: leeg bestand.
`frappe/openaec_theme/openaec_theme/openaec_theme/__init__.py`: leeg bestand.

`frappe/openaec_theme/license.txt`: de MIT-licentietekst met "Copyright (c) 2026 OpenAEC Foundation" (zelfde tekst als de MIT-licentie die de packages noemen).

`frappe/openaec_theme/README.md`:
```markdown
# openaec_theme

Frappe-app met de OpenAEC-huisstijl voor Desk en website: kleuren (licht en
donker), fonts en logo. Gegenereerd vanuit
[OpenAEC-style-book](https://github.com/OpenAEC-Foundation/OpenAEC-style-book)
(`frappe/openaec_theme/`); wijzigingen horen daar, niet in deze kopie.

```bash
bench get-app https://github.com/OpenAEC-Foundation/openaec_theme --branch v0.1.0
bench --site <site> install-app openaec_theme
```

Fonts: SIL Open Font License 1.1 (zie `openaec_theme/public/fonts/OFL-*.txt`).
```

`frappe/openaec_theme/tests/test_static.py`:
```python
import ast
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parents[1] / "openaec_theme"


class StaticChecks(unittest.TestCase):
    def test_hooks_verwijzen_naar_bestaande_assets(self):
        tree = ast.parse((APP / "hooks.py").read_text(encoding="utf-8"))
        values = {
            t.id: ast.literal_eval(node.value)
            for node in tree.body if isinstance(node, ast.Assign)
            for t in node.targets if isinstance(t, ast.Name)
        }
        self.assertEqual(values["app_name"], "openaec_theme")
        for url in values["app_include_css"] + [values["app_logo_url"]]:
            rel = url.removeprefix("/assets/openaec_theme/")
            self.assertTrue((APP / "public" / rel).is_file(), url)

    def test_versie_en_fonts(self):
        self.assertIn('__version__ = "', (APP / "__init__.py").read_text(encoding="utf-8"))
        fonts = APP / "public" / "fonts"
        self.assertTrue(any(fonts.glob("*.ttf")))
        self.assertTrue(any(fonts.glob("OFL-*.txt")))


if __name__ == "__main__":
    unittest.main()
```

`generators/frappe/build.mjs`:
```js
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { loadTokens } from "../tokens/load.mjs";
import { renderFrappeCss } from "../tokens/frappe-css.mjs";
import { writeGenerated } from "../lib/write.mjs";

const FONTS = [
  { family: "Inter", file: "Inter-Regular.ttf", weight: 400 },
  { family: "Inter", file: "Inter-Medium.ttf", weight: 500 },
  { family: "Inter", file: "Inter-SemiBold.ttf", weight: 600 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Medium.ttf", weight: 500 },
  { family: "Space Grotesk", file: "SpaceGrotesk-Bold.ttf", weight: 700 },
  { family: "JetBrains Mono", file: "JetBrainsMono-Regular.ttf", weight: 400 },
];

export function symbolSource(root) {
  const moved = join(root, "design", "logos", "foundation", "openaec-symbol-transparent.svg");
  return existsSync(moved) ? moved : join(root, "brandbook", "assets", "logo", "svg", "openaec-symbol-transparent.svg");
}

export function buildFrappeTheme(root) {
  const app = join(root, "frappe", "openaec_theme", "openaec_theme", "public");
  const out = [writeGenerated(join(app, "css", "openaec_theme.css"),
    renderFrappeCss(loadTokens(join(root, "design", "tokens")), FONTS))];
  mkdirSync(join(app, "fonts"), { recursive: true });
  for (const f of readdirSync(join(root, "design", "fonts")).sort()) {
    copyFileSync(join(root, "design", "fonts", f), join(app, "fonts", f));
    out.push(join(app, "fonts", f));
  }
  out.push(writeGenerated(join(app, "images", "openaec-symbol.svg"), readFileSync(symbolSource(root), "utf8")));
  return out;
}
```

Stap registreren in `generators/generate.mjs`:
```js
import { buildFrappeTheme } from "./frappe/build.mjs";

steps.push(["frappe-theme", (root) => buildFrappeTheme(root)]);
```

- [ ] **Step 6: Tests**

Run: `npm test && npm run generate && python -m unittest discover -s frappe/openaec_theme/tests -v`
Expected: Node PASS; Python 2 tests OK.

- [ ] **Step 7: Commit**

```bash
git add design/fonts generators frappe
git commit -m "feat(frappe): openaec_theme met Desk-kleuren, fonts en logo uit design/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Logo's — foundation-bron, app-register en logo-generator

**Files:**
- Move: `brandbook/assets/logo/svg/*.svg` → `design/logos/foundation/`
- Modify: `brandbook/assets/export_assets.py` (bronmap), `brandbook/DESIGN-SYSTEM.md` (§ logo-bestanden), `brandbook/styleguide.html` (tabelregel bronmap)
- Create: `design/apps.toml`, `design/logos/apps/openaec-template.svg`
- Create: `generators/apps/load.mjs`, `generators/logos/tile.mjs`, `generators/logos/ico.mjs`, `generators/logos/icns.mjs`, `generators/logos/lockup.mjs`, `generators/logos/build.mjs`, `generators/test/apps.test.mjs`, `generators/test/logos.test.mjs`
- Create: `generators/test/snapshots/logos/*.png` (via `UPDATE_SNAPSHOTS=1`)
- Modify: `generators/package.json` (dependencies), `.gitignore` (`logos/`), `generators/generate.mjs`

**Interfaces:**
- Consumes: `loadTokens`, `tokenValue` (Task 3); `normalizeSvg` (Task 4); `readToml` (Task 4); fonts uit `design/fonts` (Task 10).
- Produces:
  - `design/apps.toml`-formaat: `[[app]] id, display_name, category (1–4), repo?, logo?, status?` (`status = "actief" | "buiten-scope"`).
  - `loadApps(file): App[]` (gooit bij ongeldig id, categorie buiten 1–4, dubbel id, of `logo` zonder pictogrambestand).
  - `TILE = { radius: 0.22, glyph: 0.75 }`, `buildTileSvg(pictogramSvg, colors: { tile, glyph }, size = 1024): string`.
  - `packIco(pngs: { size: number, data: Buffer }[]): Buffer`, `packIcns(pngs: { size, data }[]): Buffer`.
  - `buildLockupSvg({ tileSvg, displayName, mode, colors, fontFile }): string`.
  - `buildLogos(root): string[]` → schrijft `logos/<app-id>/…` (niet in git).

- [ ] **Step 1: Foundation-logo's verplaatsen**

```bash
mkdir -p design/logos/foundation
git mv brandbook/assets/logo/svg/*.svg design/logos/foundation/
```
In `brandbook/assets/export_assets.py` de bronmap aanpassen:
```python
SVG_DIR = BASE.parent.parent / "design" / "logos" / "foundation"
```
(`BASE` is `brandbook/assets`; controleer met `python -c "from pathlib import Path; print((Path('brandbook/assets').parent.parent / 'design/logos/foundation').resolve())"` dat het pad klopt.)
In `brandbook/DESIGN-SYSTEM.md` (regel met `| SVG | \`assets/logo/svg/\``) en `brandbook/styleguide.html` (tabelregel met `logo/svg/`) de bronmap vervangen door `design/logos/foundation/`. In `CLAUDE.md` de regel `brandbook/assets/logo/svg/` vervangen door `design/logos/foundation/`.

Controle: `git grep -n "logo/svg"` geeft alleen nog historische of irrelevante treffers; `README.md` verwijst naar `brandbook/assets/logo/png/…` en blijft werken.

- [ ] **Step 2: App-register** — `design/apps.toml`

```toml
# Register van alle applicaties in het OpenAEC-ecosysteem.
# category: 1 = zwaar (iced), 2 = licht (Tauri + React), 3 = web (Frappe), 4 = bedrijfsfrontend (ERPNext)
# logo: app-id van het pictogram in design/logos/apps/ (leeg = nog geen logo ontworpen)

[[app]]
id = "openaec-template"
display_name = "Open Template"
category = 2
repo = "OpenAEC-Foundation/OpenAEC-style-book"
logo = "openaec-template"

[[app]]
id = "open-cad-studio"
display_name = "Open CAD Studio"
category = 1
repo = "HakanSeven12/OpenCADStudio"

[[app]]
id = "open-2d-studio"
display_name = "Open 2D Studio"
category = 1
repo = "OpenAEC-Foundation/open-2d-studio"

[[app]]
id = "open-pointcloud-studio"
display_name = "Open Pointcloud Studio"
category = 1
repo = "OpenAEC-Foundation/open-pointcloud-studio"

[[app]]
id = "open-3d-viewer"
display_name = "Open 3D Viewer"
category = 1
repo = "OpenAEC-Foundation/open-3d-viewer"

[[app]]
id = "open-fem-studio"
display_name = "Open FEM Studio"
category = 1
repo = "OpenAEC-Foundation/open-fem-studio"

[[app]]
id = "open-pdf-studio"
display_name = "Open PDF Studio"
category = 1
repo = "OpenAEC-Foundation/open-pdf-studio"

[[app]]
id = "openaec-bim-validator"
display_name = "OpenAEC BIM Validator"
category = 1
repo = "OpenAEC-Foundation/OpenAEC-BIM-validator"

[[app]]
id = "open-calc-studio"
display_name = "Open Calc Studio"
category = 2
repo = "OpenAEC-Foundation/open-calc-studio"

[[app]]
id = "open-heatloss-studio"
display_name = "Open Heatloss Studio"
category = 2
repo = "OpenAEC-Foundation/open-heatloss-studio"

[[app]]
id = "open-u-value-studio"
display_name = "Open U-value Studio"
category = 2
repo = "OpenAEC-Foundation/Open-U-value-Studio"

[[app]]
id = "open-safety-studio"
display_name = "Open Safety Studio"
category = 2
repo = "OpenAEC-Foundation/Open-Safety-Studio"

[[app]]
id = "open-ecoscore-studio"
display_name = "Open MPG Studio"
category = 2
repo = "OpenAEC-Foundation/open-ecoscore-studio"

[[app]]
id = "openaec-reports"
display_name = "OpenAEC Reports"
category = 2
repo = "OpenAEC-Foundation/openaec-reports"

[[app]]
id = "open-speech-studio"
display_name = "Open Speech Studio"
category = 2
repo = "OpenAEC-Foundation/open-speech-studio"

[[app]]
id = "open-orchestrator-studio"
display_name = "Open Orchestrator Studio"
category = 2
repo = "DutchSailor/open-orchestrator-studio"

[[app]]
id = "openaec-cloud-desktop"
display_name = "OpenAEC Cloud Desktop"
category = 2
repo = "OpenAEC-Foundation/openaec-cloud-desktop"

[[app]]
id = "open-field-studio"
display_name = "Open Field Studio"
category = 3

[[app]]
id = "open-energy-studio"
display_name = "Open Energy Studio"
category = 3
repo = "OpenAEC-Foundation/open-energy-studio"

[[app]]
id = "y-next"
display_name = "Y-Next"
category = 4
repo = "OpenAEC-Foundation/Y-app-ERPNext"

[[app]]
id = "z-next"
display_name = "Z-Next"
category = 4

[[app]]
id = "open-frame-studio"
display_name = "Open Frame Studio"
category = 2
status = "buiten-scope"
```

Controleer vóór het committen met de eigenaar of de `display_name`-waarden de gewenste productnamen zijn (vooral "Open MPG Studio" bij repo `open-ecoscore-studio`, en de categorie van Open Frame Studio).

- [ ] **Step 3: Testpictogram** — `design/logos/apps/openaec-template.svg`

Neem het pictogram van het icoon `file/project` over:
```bash
mkdir -p design/logos/apps
cp design/icons/file/project.svg design/logos/apps/openaec-template.svg
```

- [ ] **Step 4: Dependencies**

`generators/package.json` → `dependencies` aanvullen:
```json
"@resvg/resvg-js": "^2.6.2",
"opentype.js": "^1.3.4",
"pngjs": "^7.0.0"
```
Run: `npm install`

`.gitignore` aanvullen:
```
# Build-uitvoer: app-logo-sets (gaan als zip mee met de release)
/logos/
```

- [ ] **Step 5: Failing tests** — `generators/test/apps.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { loadApps } from "../apps/load.mjs";
import { repoPath } from "../lib/paths.mjs";

test("het echte register is geldig", () => {
  const apps = loadApps(repoPath("design", "apps.toml"));
  assert.ok(apps.find((a) => a.id === "openaec-template" && a.logo === "openaec-template"));
});

test("fouten in het register worden gemeld", () => {
  const dir = mkdtempSync(join(tmpdir(), "oa-apps-"));
  mkdirSync(join(dir, "logos", "apps"), { recursive: true });
  const file = join(dir, "apps.toml");
  writeFileSync(file, `
[[app]]
id = "Bad Id"
display_name = "X"
category = 5
[[app]]
id = "dup"
display_name = "A"
category = 1
logo = "ontbreekt"
[[app]]
id = "dup"
display_name = "B"
category = 1
`);
  assert.throws(() => loadApps(file), (e) =>
    /ongeldig app-id: Bad Id/.test(e.message) && /categorie 5/.test(e.message) &&
    /dubbel app-id: dup/.test(e.message) && /pictogram ontbreekt: ontbreekt/.test(e.message));
});
```

`generators/test/logos.test.mjs`:
```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import { PNG } from "pngjs";
import { TILE, buildTileSvg } from "../logos/tile.mjs";
import { packIco } from "../logos/ico.mjs";
import { packIcns } from "../logos/icns.mjs";
import { repoPath } from "../lib/paths.mjs";

const PICTO = readFileSync(repoPath("design", "logos", "apps", "openaec-template.svg"), "utf8");
const COLORS = { tile: "#36363E", glyph: "#D97706" };
const render = (svg, size) => new Resvg(svg, { fitTo: { mode: "width", value: size } }).render();

test("tegel volgt de regels: kleur, afronding en 75%-pictogram", () => {
  const svg = buildTileSvg(PICTO, COLORS, 1024);
  assert.match(svg, /<rect width="1024" height="1024" rx="225\.28" fill="#36363E"\/>/);
  assert.match(svg, /<g transform="translate\(128 128\) scale\(32\)" color="#D97706">/);
  assert.equal(TILE.glyph, 0.75);
});

test("pictogram blijft binnen het 75%-vak", () => {
  const img = render(buildTileSvg(PICTO, { tile: "#000000", glyph: "#FFFFFF" }, 256), 256);
  const px = img.pixels;
  for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
    const inBox = x >= 32 && x < 224 && y >= 32 && y < 224;
    const i = (y * 256 + x) * 4;
    if (!inBox && px[i] > 128 && px[i + 1] > 128 && px[i + 2] > 128) assert.fail(`lichte pixel buiten vak op ${x},${y}`);
  }
});

test("ICO- en ICNS-containers zijn geldig", () => {
  const png = (s) => ({ size: s, data: Buffer.from(render(buildTileSvg(PICTO, COLORS, s), s).asPng()) });
  const ico = packIco([png(16), png(32), png(256)]);
  assert.equal(ico.readUInt16LE(2), 1);
  assert.equal(ico.readUInt16LE(4), 3);
  assert.equal(ico[6 + 2 * 16], 0, "256 px wordt als 0 opgeslagen");
  const icns = packIcns([png(16), png(32), png(128), png(256), png(512), png(1024)]);
  assert.equal(icns.subarray(0, 4).toString("ascii"), "icns");
  assert.equal(icns.readUInt32BE(4), icns.length);
});

test("snapshots op 16, 32 en 256 px", () => {
  const dir = repoPath("generators", "test", "snapshots", "logos");
  mkdirSync(dir, { recursive: true });
  for (const size of [16, 32, 256]) {
    const actual = PNG.sync.read(Buffer.from(render(buildTileSvg(PICTO, COLORS, size), size).asPng()));
    const file = join(dir, `openaec-template.${size}.png`);
    if (process.env.UPDATE_SNAPSHOTS || !existsSync(file)) {
      if (!process.env.UPDATE_SNAPSHOTS) assert.fail(`snapshot ontbreekt: ${file} — draai met UPDATE_SNAPSHOTS=1`);
      writeFileSync(file, PNG.sync.write(actual));
      continue;
    }
    const expected = PNG.sync.read(readFileSync(file));
    let diff = 0;
    for (let i = 0; i < actual.data.length; i += 4) {
      if ([0, 1, 2, 3].some((c) => Math.abs(actual.data[i + c] - expected.data[i + c]) > 2)) diff++;
    }
    assert.ok(diff * 200 <= size * size, `${size}px wijkt af (${diff} pixels)`);
  }
});
```

- [ ] **Step 6: Tests draaien en zien falen**

Run: `npm test`
Expected: FAIL — modules ontbreken.

- [ ] **Step 7: Implementatie**

`generators/apps/load.mjs`:
```js
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { readToml } from "../lib/toml.mjs";

const ID = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;

export function loadApps(file) {
  const apps = readToml(file).app ?? [];
  const errors = [];
  const seen = new Set();
  for (const a of apps) {
    if (!ID.test(a.id ?? "")) errors.push(`ongeldig app-id: ${a.id}`);
    if (seen.has(a.id)) errors.push(`dubbel app-id: ${a.id}`);
    seen.add(a.id);
    if (!a.display_name) errors.push(`${a.id}: display_name ontbreekt`);
    if (![1, 2, 3, 4].includes(a.category)) errors.push(`${a.id}: categorie ${a.category} bestaat niet (1–4)`);
    if (a.logo && !existsSync(join(dirname(file), "logos", "apps", `${a.logo}.svg`))) {
      errors.push(`${a.id}: pictogram ontbreekt: ${a.logo}`);
    }
  }
  if (errors.length) throw new Error(`apps.toml: ${errors.join("; ")}`);
  return apps;
}
```

`generators/logos/tile.mjs`:
```js
import { normalizeSvg } from "../icons/normalize.mjs";

export const TILE = { radius: 0.22, glyph: 0.75 };

const fmt = (n) => String(Math.round(n * 100) / 100);

export function buildTileSvg(pictogramSvg, colors, size = 1024) {
  const { svg } = normalizeSvg(pictogramSvg);
  const inner = svg.replace(/^<svg\b[^>]*>/, "").replace(/<\/svg>\s*$/, "");
  const rootAttrs = /^<svg\b([^>]*)>/.exec(svg)[1]
    .replace(/\s(xmlns|viewBox)="[^"]*"/g, "")
    .trim();
  const glyph = size * TILE.glyph;
  const offset = (size - glyph) / 2;
  const scale = glyph / 24;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}">` +
    `<rect width="${size}" height="${size}" rx="${fmt(size * TILE.radius)}" fill="${colors.tile}"/>` +
    `<g transform="translate(${fmt(offset)} ${fmt(offset)}) scale(${fmt(scale)})" color="${colors.glyph}">` +
    `<g ${rootAttrs}>${inner}</g></g></svg>`;
}
```

`generators/logos/ico.mjs`:
```js
// ICO met PNG-afbeeldingen (ondersteund sinds Windows Vista).
export function packIco(pngs) {
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(pngs.length, 4);
  const entries = [];
  let offset = 6 + 16 * pngs.length;
  for (const { size, data } of pngs) {
    const e = Buffer.alloc(16);
    e[0] = size >= 256 ? 0 : size;
    e[1] = size >= 256 ? 0 : size;
    e[2] = 0;
    e[3] = 0;
    e.writeUInt16LE(1, 4);
    e.writeUInt16LE(32, 6);
    e.writeUInt32LE(data.length, 8);
    e.writeUInt32LE(offset, 12);
    entries.push(e);
    offset += data.length;
  }
  return Buffer.concat([header, ...entries, ...pngs.map((p) => p.data)]);
}
```

`generators/logos/icns.mjs`:
```js
// ICNS met PNG-afbeeldingen. Type per pixelgrootte.
const TYPES = { 16: "icp4", 32: "icp5", 64: "icp6", 128: "ic07", 256: "ic08", 512: "ic09", 1024: "ic10" };

export function packIcns(pngs) {
  const chunks = pngs.map(({ size, data }) => {
    const type = TYPES[size];
    if (!type) throw new Error(`Geen ICNS-type voor ${size}px`);
    const head = Buffer.alloc(8);
    head.write(type, 0, "ascii");
    head.writeUInt32BE(8 + data.length, 4);
    return Buffer.concat([head, data]);
  });
  const body = Buffer.concat(chunks);
  const head = Buffer.alloc(8);
  head.write("icns", 0, "ascii");
  head.writeUInt32BE(8 + body.length, 4);
  return Buffer.concat([head, body]);
}
```

`generators/logos/lockup.mjs`:
```js
import opentype from "opentype.js";

// Lockup: app-tegel + weergavenaam als paden. "Open" (als eerste woord) in amber.
export function buildLockupSvg({ tileSvg, displayName, mode, colors, fontFile }) {
  const font = opentype.loadSync(fontFile);
  const height = 128;
  const fontSize = 64;
  const baseline = 86;
  let x = height + 32;
  const words = displayName.startsWith("Open ") ? [["Open", colors.accent], [displayName.slice(5), colors.text[mode]]]
    : [[displayName, colors.text[mode]]];
  let paths = "";
  for (const [i, [text, fill]] of words.entries()) {
    const t = i > 0 ? " " + text : text;
    const p = font.getPath(t, x, baseline, fontSize);
    paths += `<path d="${p.toPathData(2)}" fill="${fill}"/>`;
    x += font.getAdvanceWidth(t, fontSize);
  }
  const tile = tileSvg.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">',
    `<svg x="0" y="0" width="${height}" height="${height}" viewBox="0 0 1024 1024">`);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${Math.ceil(x)} ${height}">${tile}${paths}</svg>`;
}
```

`generators/logos/build.mjs`:
```js
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import { loadApps } from "../apps/load.mjs";
import { loadTokens, tokenValue } from "../tokens/load.mjs";
import { buildTileSvg } from "./tile.mjs";
import { packIco } from "./ico.mjs";
import { packIcns } from "./icns.mjs";
import { buildLockupSvg } from "./lockup.mjs";

const PNG_SIZES = [16, 32, 48, 64, 128, 256, 512, 1024];

export function buildLogos(root) {
  const tokens = loadTokens(join(root, "design", "tokens"));
  const colors = {
    tile: tokenValue(tokens, "color.brand.deep-forge"),
    glyph: tokenValue(tokens, "color.brand.amber"),
    accent: tokenValue(tokens, "color.brand.amber"),
    text: { light: tokenValue(tokens, "color.brand.deep-forge"), dark: tokenValue(tokens, "color.brand.blueprint-white") },
  };
  const fontFile = join(root, "design", "fonts", "SpaceGrotesk-Bold.ttf");
  const written = [];
  for (const app of loadApps(join(root, "design", "apps.toml")).filter((a) => a.logo)) {
    const picto = readFileSync(join(root, "design", "logos", "apps", `${app.logo}.svg`), "utf8");
    const out = join(root, "logos", app.id);
    mkdirSync(out, { recursive: true });
    const tile = buildTileSvg(picto, colors, 1024);
    const png = {};
    for (const s of PNG_SIZES) {
      png[s] = Buffer.from(new Resvg(tile, { fitTo: { mode: "width", value: s } }).render().asPng());
      writeFileSync(join(out, `icon-${s}.png`), png[s]);
    }
    writeFileSync(join(out, "icon.ico"), packIco([16, 32, 48, 64, 128, 256].map((s) => ({ size: s, data: png[s] }))));
    writeFileSync(join(out, "icon.icns"), packIcns([16, 32, 64, 128, 256, 512, 1024].map((s) => ({ size: s, data: png[s] }))));
    writeFileSync(join(out, "favicon.svg"), tile);
    writeFileSync(join(out, "favicon.ico"), packIco([16, 32, 48].map((s) => ({ size: s, data: png[s] }))));
    for (const s of [192, 512]) {
      writeFileSync(join(out, `web-${s}.png`), Buffer.from(new Resvg(tile, { fitTo: { mode: "width", value: s } }).render().asPng()));
    }
    // Maskable: volle tegel zonder afronding, zodat het platform zelf kan afsnijden.
    const maskable = tile.replace(/rx="[^"]*"/, 'rx="0"');
    writeFileSync(join(out, "web-maskable-512.png"), Buffer.from(new Resvg(maskable, { fitTo: { mode: "width", value: 512 } }).render().asPng()));
    for (const mode of ["light", "dark"]) {
      writeFileSync(join(out, `lockup-${mode}.svg`), buildLockupSvg({ tileSvg: tile, displayName: app.display_name, mode, colors, fontFile }));
    }
    written.push(out);
  }
  return written;
}
```

Stap registreren in `generators/generate.mjs` (logo's zijn build-uitvoer; `check.mjs` kijkt niet naar `logos/`):
```js
import { buildLogos } from "./logos/build.mjs";

steps.push(["logos", (root) => { buildLogos(root); return []; }]);
```

- [ ] **Step 8: Tests, snapshots en visuele controle**

Run: `npm test` → de snapshot-test faalt met "snapshot ontbreekt". Dan:
```bash
UPDATE_SNAPSHOTS=1 npm test
npm test
npm run generate
ls logos/openaec-template
```
Expected: tweede `npm test` PASS; `logos/openaec-template/` bevat `icon-16.png … icon-1024.png`, `icon.ico`, `icon.icns`, `favicon.svg`, `favicon.ico`, `web-192.png`, `web-512.png`, `web-maskable-512.png`, `lockup-light.svg`, `lockup-dark.svg`. Open `icon-256.png` en `lockup-dark.svg` en controleer: Deep Forge-tegel, groot amber pictogram, "Open" in amber gevolgd door "Template".

- [ ] **Step 9: Commit**

```bash
git add design/logos design/apps.toml brandbook CLAUDE.md generators .gitignore package-lock.json
git commit -m "feat(logos): app-register en logo-generator (tegel, ico, icns, favicon, lockup)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Volledige generatie, versiescript en CI

**Files:**
- Create: `generators/version/set-version.mjs`, `generators/test/version.test.mjs`, `generators/test/generate.test.mjs`, `.github/workflows/design.yml`
- Modify: `package.json` (script `version:set`)

**Interfaces:**
- Consumes: alle stappen in `generate.mjs` (Tasks 2–11).
- Produces: `setVersion(root, version)` — zet de versie in `Cargo.toml` (`[workspace.package] version`), elke `packages/*/package.json`, `generators/package.json` en `frappe/openaec_theme/openaec_theme/__init__.py`; `readVersions(root): Map<string, string>`.

- [ ] **Step 1: Failing tests** — `generators/test/version.test.mjs`

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { cpSync, mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { readVersions, setVersion } from "../version/set-version.mjs";

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "oa-ver-"));
  writeFileSync(join(root, "Cargo.toml"), '[workspace]\nmembers = []\n\n[workspace.package]\nversion = "0.1.0"\nedition = "2021"\n');
  for (const p of ["a", "b"]) {
    mkdirSync(join(root, "packages", p), { recursive: true });
    writeFileSync(join(root, "packages", p, "package.json"), JSON.stringify({ name: p, version: "0.1.0" }, null, 2) + "\n");
  }
  mkdirSync(join(root, "generators"), { recursive: true });
  writeFileSync(join(root, "generators", "package.json"), JSON.stringify({ name: "g", version: "0.1.0" }, null, 2) + "\n");
  mkdirSync(join(root, "frappe", "openaec_theme", "openaec_theme"), { recursive: true });
  writeFileSync(join(root, "frappe", "openaec_theme", "openaec_theme", "__init__.py"), '__version__ = "0.1.0"\n');
  return root;
}

test("setVersion zet overal dezelfde versie", () => {
  const root = fixture();
  setVersion(root, "0.2.0");
  assert.deepEqual(new Set(readVersions(root).values()), new Set(["0.2.0"]));
  assert.equal(readVersions(root).size, 5);
});

test("ongeldige versie wordt geweigerd", () => {
  assert.throws(() => setVersion(fixture(), "v0.2"), /semver/);
});
```

`generators/test/generate.test.mjs`:
```js
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
```

Let op: `generate.test.mjs` importeert `generate.mjs`; zorg dat de stap-registraties uit de vorige tasks in `generate.mjs` zelf staan (niet in het `if (import.meta.url …)`-blok), zodat `runAll` alle stappen kent.

- [ ] **Step 2: Tests draaien en zien falen**

Run: `npm test`
Expected: FAIL — `set-version.mjs` ontbreekt (de generate-test kan al slagen).

- [ ] **Step 3: `generators/version/set-version.mjs`**

```js
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT } from "../lib/paths.mjs";

const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/;
const CARGO_RE = /(\[workspace\.package\][^\[]*?\bversion\s*=\s*")([^"]+)(")/s;
const PY_RE = /(__version__\s*=\s*")([^"]+)(")/;

function packageJsonFiles(root) {
  const dir = join(root, "packages");
  const pkgs = existsSync(dir) ? readdirSync(dir).sort().map((p) => join(dir, p, "package.json")).filter(existsSync) : [];
  return [...pkgs, join(root, "generators", "package.json")].filter(existsSync);
}

const pyFile = (root) => join(root, "frappe", "openaec_theme", "openaec_theme", "__init__.py");

export function readVersions(root) {
  const out = new Map();
  out.set("Cargo.toml", CARGO_RE.exec(readFileSync(join(root, "Cargo.toml"), "utf8"))?.[2]);
  for (const f of packageJsonFiles(root)) out.set(f.slice(root.length + 1), JSON.parse(readFileSync(f, "utf8")).version);
  if (existsSync(pyFile(root))) out.set("frappe", PY_RE.exec(readFileSync(pyFile(root), "utf8"))?.[2]);
  return out;
}

export function setVersion(root, version) {
  if (!SEMVER.test(version)) throw new Error(`"${version}" is geen semver-versie (bijv. 0.2.0)`);
  const cargo = join(root, "Cargo.toml");
  const cargoSrc = readFileSync(cargo, "utf8");
  if (!CARGO_RE.test(cargoSrc)) throw new Error("Cargo.toml mist [workspace.package] version");
  writeFileSync(cargo, cargoSrc.replace(CARGO_RE, `$1${version}$3`));
  for (const f of packageJsonFiles(root)) {
    const pkg = JSON.parse(readFileSync(f, "utf8"));
    pkg.version = version;
    writeFileSync(f, JSON.stringify(pkg, null, 2) + "\n");
  }
  if (existsSync(pyFile(root))) writeFileSync(pyFile(root), readFileSync(pyFile(root), "utf8").replace(PY_RE, `$1${version}$3`));
}

if (process.argv[1]?.endsWith("set-version.mjs")) {
  const version = process.argv[2];
  if (!version) { console.error("gebruik: npm run version:set -- 0.2.0"); process.exit(2); }
  setVersion(ROOT, version);
  for (const [f, v] of readVersions(ROOT)) console.log(`${f}: ${v}`);
}
```

`package.json` → `scripts` aanvullen:
```json
"version:set": "node generators/version/set-version.mjs"
```

- [ ] **Step 4: Tests draaien**

Run: `npm test`
Expected: PASS

- [ ] **Step 5: CI-workflow** — `.github/workflows/design.yml`

```yaml
name: design

on:
  push:
    branches: [main]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: npm ci
      - name: Node-tests
        run: npm test
      - name: Gegenereerde bestanden actueel
        run: npm run check
      - name: Rust-tests
        run: cargo test --workspace
      - name: Gedeelde ribbon-tabs
        run: cargo run -q -p openaec-ribbon -- check-shared design/ribbons
      - name: Frappe-app
        run: python -m unittest discover -s frappe/openaec_theme/tests -v
      - name: Versies gelijk
        run: node -e "import('./generators/version/set-version.mjs').then(m=>{const v=new Set(m.readVersions(process.cwd()).values());if(v.size!==1){console.error([...v]);process.exit(1)}})"
```

- [ ] **Step 6: Lokaal de hele keten draaien**

Run: `npm test && npm run check && cargo test --workspace && python -m unittest discover -s frappe/openaec_theme/tests`
Expected: alles PASS; `npm run check` meldt `✓ gegenereerde bestanden zijn actueel` (na het committen van eerdere tasks; draai `check` pas nadat alle wijzigingen gecommit zijn, anders meldt hij terecht de nog niet gecommitte bestanden).

- [ ] **Step 7: Commit**

```bash
git add generators package.json .github/workflows/design.yml
git commit -m "ci: generatiecontrole, tests en versiecontrole voor design/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: Release-workflow en documentatie

**Files:**
- Create: `.github/workflows/release.yml`, `docs/integratie.md`, `design/components/README.md`, `design/README.md`
- Modify: `README.md` (sectie "What's inside"), `CLAUDE.md` (tabel belangrijke bestanden, scope)

**Interfaces:**
- Consumes: alles uit Tasks 1–12.
- Produces: releaseproces op tag `v*`; integratiehandleiding per categorie.

- [ ] **Step 1: Release-workflow** — `.github/workflows/release.yml`

```yaml
name: release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          registry-url: https://registry.npmjs.org
          cache: npm
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: npm ci
      - name: Tag en versies komen overeen
        run: |
          node -e "import('./generators/version/set-version.mjs').then(m=>{const want=process.env.GITHUB_REF_NAME.replace(/^v/,'');const v=[...m.readVersions(process.cwd())];const bad=v.filter(([,x])=>x!==want);if(bad.length){console.error('versie wijkt af van tag',bad);process.exit(1)}})"
      - run: npm test
      - run: npm run check
      - run: cargo test --workspace
      - run: python -m unittest discover -s frappe/openaec_theme/tests
      - name: Logo-sets inpakken
        run: |
          npm run generate
          cd logos && zip -r "../openaec-logos-${GITHUB_REF_NAME}.zip" . && cd ..
      - name: npm-packages publiceren
        run: npm publish --workspaces --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      - name: Frappe-thema naar eigen repo
        env:
          THEME_REPO_TOKEN: ${{ secrets.THEME_REPO_TOKEN }}
        run: |
          git config user.name "openaec-release"
          git config user.email "release@users.noreply.github.com"
          git subtree split --prefix frappe/openaec_theme -b theme-release
          git push "https://x-access-token:${THEME_REPO_TOKEN}@github.com/OpenAEC-Foundation/openaec_theme.git" theme-release:main
          git push "https://x-access-token:${THEME_REPO_TOKEN}@github.com/OpenAEC-Foundation/openaec_theme.git" "theme-release:refs/tags/${GITHUB_REF_NAME}"
      - name: GitHub Release
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release create "$GITHUB_REF_NAME" "openaec-logos-${GITHUB_REF_NAME}.zip" --generate-notes
```

`npm publish --workspaces` publiceert alleen packages zonder `"private": true`; `@openaec/generators` is privé en wordt overgeslagen. Controleer dat `packages/ribbon`, `packages/shell` en `packages/ui-primitives` op versie `0.1.0` staan (`npm run version:set -- 0.1.0` zet alles gelijk).

- [ ] **Step 2: `design/README.md`**

```markdown
# design/ — de enige bron

Alles in deze map wordt met de hand bewerkt. Alles daarbuiten in `packages/`,
`crates/`, `frappe/` en `logos/` dat met `@generated` begint of door
`npm run generate` wordt gemaakt, bewerk je **niet** met de hand.

| Map | Inhoud | Gaat naar |
|---|---|---|
| `tokens/` | kleuren, typografie, maten | `@openaec/design-tokens`, `openaec-tokens`, Frappe-thema |
| `icons/` + `icons.toml` | iconen (24×24, `currentColor`) | `@openaec/icons`, `openaec-icons` |
| `i18n/` | gedeelde termen nl/en | `@openaec/i18n`, `openaec-i18n` |
| `ribbons/` | gedeelde ribbon-tabs | `openaec-ribbon` |
| `logos/foundation/` | OpenAEC-logo en -symbool | brandbook-exports, Frappe-thema |
| `logos/apps/` | pictogram per app | logo-sets in de release-zip |
| `fonts/` | Space Grotesk, Inter, JetBrains Mono (OFL) | Frappe-thema |
| `components/` | componentspecificaties | iced- en React-implementaties |
| `apps.toml` | register van alle apps | logo's, uitrol |

## Een icoon toevoegen

1. Zet `design/icons/<domein>/<naam>.svg` neer: viewBox `0 0 24 24`, lijnen en
   vlakken in `currentColor`.
2. Voeg in `design/icons/icons.toml` een `[[icon]]`-blok toe met `id`,
   `label = { nl, en }`, `tags` en `source = "openaec"`.
3. `npm run generate` en `npm test`; voor de Rust-snapshots eenmalig
   `UPDATE_SNAPSHOTS=1 cargo test -p openaec-icons`.
4. PR openen. Na merge en release krijgen alle apps het icoon via hun versie-update.
```

- [ ] **Step 3: `design/components/README.md`**

```markdown
# Componentspecificaties

Per component één bestand `<component>.md` met: opbouw, maten en kleuren als
tokens, toestanden (normaal, hover, actief, uitgeschakeld, focus),
toetsenbordgedrag en labels. De iced-implementatie (`openaec-ui`) en de
React-implementatie (`packages/`) volgen beide exact deze specificatie.

Vertrekpunt: `project-templates/Tauri+React/COMPONENT-MANIFEST.md`.

Versie 1 (specificaties worden geschreven in fase 1a/1b, per component vóór de bouw):

| Groep | Componenten |
|---|---|
| Schil | TitleBar, Ribbon, Backstage, DocumentTabs, StatusBar, zijpanelen, Startscherm |
| Basis | Button, IconButton, Input, Select/Combo, Checkbox/Toggle, Dialog, Tooltip, Contextmenu, Toast |
| Data | Table/DataGrid, Tree, PropertyGrid |
| Viewer | NavigationCube |
```

- [ ] **Step 4: `docs/integratie.md`**

```markdown
# Huisstijl gebruiken in een OpenAEC-app

Eén versienummer voor alles: gebruik in een app overal dezelfde versie.

## Categorie 1 — iced (Rust)

```toml
[dependencies]
openaec-tokens = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-icons  = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-i18n   = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
openaec-ribbon = { git = "https://github.com/OpenAEC-Foundation/OpenAEC-style-book", tag = "v0.1.0" }
```

`ribbon.toml` controleren:
```bash
cargo install --git https://github.com/OpenAEC-Foundation/OpenAEC-style-book --tag v0.1.0 openaec-ribbon
openaec-ribbon check ribbon.toml --nl src/i18n/nl.json --en src/i18n/en.json
```

## Categorie 2 en 4 — React

```bash
npm install @openaec/design-tokens@0.1.0 @openaec/icons@0.1.0 @openaec/i18n@0.1.0
```

## Categorie 3 — Frappe

```bash
bench get-app https://github.com/OpenAEC-Foundation/openaec_theme --branch v0.1.0
bench --site <site> install-app openaec_theme
```

## App-logo's

Download `openaec-logos-v0.1.0.zip` bij de GitHub Release en neem de map van je
app over (`icon.ico`, `icon.icns`, `icon-*.png`, favicons, lockups). Staat je app
niet in `design/apps.toml` of heeft hij nog geen pictogram: zie `design/README.md`.

## Lokaal tegelijk aan stijlbook en app werken

Rust — in de `Cargo.toml` van de app:
```toml
[patch."https://github.com/OpenAEC-Foundation/OpenAEC-style-book"]
openaec-icons = { path = "../OpenAEC-style-book/crates/openaec-icons" }
```

npm — in de `package.json` van de app:
```json
"overrides": { "@openaec/icons": "file:../OpenAEC-style-book/packages/icons" }
```
```

- [ ] **Step 5: README en CLAUDE.md**

In `README.md` de codeblok-structuur onder "What's inside" vervangen door:
```
design/                  # Enige bron: tokens, icons, i18n, ribbons, logos, fonts, apps.toml
generators/              # Zetten design/ om naar packages/, crates/, frappe/ en logos/
packages/                # npm (React): design-tokens, icons, i18n, ribbon, shell, ui-primitives
crates/                  # Rust: openaec-tokens, openaec-icons, openaec-i18n, openaec-ribbon
frappe/openaec_theme/    # Frappe-app met de huisstijl voor Desk en website
brandbook/               # Merkregels, styleguide, exports van logo's en illustraties
project-templates/       # Tauri+React desktop-template
docs/integratie.md       # Huisstijl gebruiken in een app
```
en een korte alinea toevoegen: "Wijzigingen aan de huisstijl gebeuren in `design/`; zie `design/README.md`."

In `CLAUDE.md`, tabel "Belangrijke Bestanden", rijen toevoegen:
```
| `design/` | Enige bron voor tokens, iconen, i18n, ribbons, logo's, fonts en app-register |
| `generators/` | Generators (`npm run generate`, `npm run check`) |
| `crates/` | Rust-crates voor iced-apps |
| `frappe/openaec_theme/` | Frappe-thema |
| `docs/integratie.md` | Integratie per app-categorie |
```

- [ ] **Step 6: Controle en commit**

Run: `npm test && npm run check && cargo test --workspace`
Expected: PASS

```bash
git add .github/workflows/release.yml docs/integratie.md design/README.md design/components/README.md README.md CLAUDE.md
git commit -m "docs: integratiehandleiding, design/-uitleg en release-workflow

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 14: Handmatige stappen voor de eigenaar (niet door een agent)

Deze stappen vragen accounts, rechten of een akkoord en worden door de eigenaar uitgevoerd. De agent bereidt ze voor en meldt ze; hij voert ze niet uit.

- [ ] **Step 1: npm-organisatie** — op npmjs.com de organisatie `openaec` aanmaken (of bevestigen dat die van de foundation is). Is de naam bezet, dan kiest de eigenaar een alternatieve scope; daarna `name` in alle `packages/*/package.json` aanpassen.
- [ ] **Step 2: Repo `OpenAEC-Foundation/openaec_theme`** — lege publieke repo aanmaken.
- [ ] **Step 3: Secrets in `OpenAEC-Foundation/OpenAEC-style-book`** — `NPM_TOKEN` (automation-token met publicatierecht op `@openaec`) en `THEME_REPO_TOKEN` (fine-grained token met schrijfrecht op `openaec_theme`).
- [ ] **Step 4: Branch reviewen en mergen** — `ui-fundament` pushen, PR openen, CI groen, mergen.
- [ ] **Step 5: Release** — op `main`: `git tag v0.1.0 && git push origin v0.1.0`; controleer daarna dat de npm-packages, de `openaec_theme`-tag en de GitHub Release met `openaec-logos-v0.1.0.zip` er zijn.

---

### Task 15: Iconen uit OpenCADStudio importeren — ALLEEN na schriftelijke toestemming

**Voorwaarde:** de eigenaar bevestigt schriftelijke toestemming van de rechthebbende van OpenCADStudio om de iconen onder de licentie van dit repo (MIT voor code/packages, CC BY-SA 4.0 voor merk-assets) op te nemen. Zonder die bevestiging wordt deze task niet uitgevoerd.

**Files:**
- Create: `generators/icons/import-opencadstudio.mjs`
- Modify: `design/icons/**`, `design/icons/icons.toml`, `crates/openaec-icons/tests/snapshots/*`

**Interfaces:**
- Consumes: `readSvgDirectory`, `importIcons`, `manifestToml` (Task 5); `loadIconManifest` (Task 4).

- [ ] **Step 1: Importscript** — `generators/icons/import-opencadstudio.mjs`

```js
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { repoPath } from "../lib/paths.mjs";
import { parseToml } from "../lib/toml.mjs";
import { importIcons, manifestToml, readSvgDirectory } from "./import.mjs";

const source = process.argv[2];
if (!source) { console.error("gebruik: node generators/icons/import-opencadstudio.mjs <pad-naar-assets/icons>"); process.exit(2); }

// Lichte grijstinten van de bron (ontworpen voor donkere achtergrond) worden currentColor.
const NEUTRAL = ["#e0e0e0", "#eeeeee", "#e1e1e1", "#cccccc", "#aaaaaa", "#888888"];
const SKIP_VIEWBOX = new Set(["ui/tri_down", "ui/tri_left", "ui/tri_right", "ui/tri_up"]); // geen 24×24

const raw = readSvgDirectory(source, {
  domainFor: (rel) => (rel[0] === "ui" ? "ui" : "cad"),
  nameFor: (rel, base) => [...rel.filter((r) => r !== "ui"), base].join("-").replace(/_/g, "-"),
}).filter((e) => !SKIP_VIEWBOX.has(e.id.replace(/-/g, "_")));

const existing = parseToml(readFileSync(repoPath("design", "icons", "icons.toml"), "utf8")).icon;
const taken = new Set(existing.map((e) => e.id));
const fresh = raw.filter((e) => !taken.has(e.id));
const { written, duplicates } = importIcons(fresh, repoPath("design", "icons"), { neutralColors: NEUTRAL });

const added = written.map((e) => ({
  id: e.id,
  label: { nl: e.id.split("/")[1], en: e.id.split("/")[1] },
  tags: [],
  source: "opencadstudio",
}));
writeFileSync(repoPath("design", "icons", "icons.toml"), manifestToml([...existing, ...added]), "utf8");
console.log(`${written.length} geïmporteerd, ${duplicates.length} dubbel overgeslagen, ${raw.length - fresh.length} id al in gebruik`);
```

- [ ] **Step 2: Draaien en de manifestfouten oplossen**

Run: `node generators/icons/import-opencadstudio.mjs ../OpenCADStudio/assets/icons && npm run generate`
Expected: `generate` faalt met een lijst iconen die eigen kleuren hebben (bijv. de cyaan accentkleur `#4cc9f0`) zonder tag `color`. Leg die lijst aan de eigenaar voor met de keuze: (a) accentkleur behouden en tag `color` toevoegen, of (b) accentkleur omzetten naar de huisstijl (bijv. amber) — dat is een ontwerpbeslissing van de eigenaar. Verwerk de keuze, vul de NL/EN-labels in `icons.toml` in (de placeholder-labels zijn de bestandsnaam) en draai opnieuw.

- [ ] **Step 3: Snapshots en tests**

Run: `UPDATE_SNAPSHOTS=1 cargo test -p openaec-icons && npm test && cargo test --workspace && npm run check`
Expected: PASS na het committen.

- [ ] **Step 4: Commit**

```bash
git add design/icons generators crates/openaec-icons
git commit -m "feat(icons): CAD-iconen opgenomen in design/icons (met toestemming rechthebbende)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
