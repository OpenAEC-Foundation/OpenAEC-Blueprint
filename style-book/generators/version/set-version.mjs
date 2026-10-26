import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";
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
const label = (root, f) => relative(root, f).replaceAll("\\", "/");

export function readVersions(root) {
  const out = new Map();
  out.set("Cargo.toml", CARGO_RE.exec(readFileSync(join(root, "Cargo.toml"), "utf8"))?.[2]);
  for (const f of packageJsonFiles(root)) out.set(label(root, f), JSON.parse(readFileSync(f, "utf8")).version);
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
