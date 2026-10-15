import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { ROOT } from "../lib/paths.mjs";

// Op Windows is npm een .cmd-bestand en vereist een shell; één commandostring voorkomt de argumentenwaarschuwing.
function runNpm(args, options) {
  return process.platform === "win32"
    ? spawnSync(`npm ${args.join(" ")}`, { ...options, shell: true })
    : spawnSync("npm", args, options);
}

export function readPackages(root) {
  const dir = join(root, "packages");
  if (!existsSync(dir)) return [];
  return readdirSync(dir).sort()
    .map((p) => join(dir, p, "package.json"))
    .filter(existsSync)
    .map((f) => JSON.parse(readFileSync(f, "utf8")));
}

/** Bepaalt per package of er gepubliceerd moet worden. isPublished(naam, versie) is injecteerbaar. */
export function planPublish(packages, isPublished) {
  return packages.map((pkg) => {
    if (pkg.private === true) return { name: pkg.name, version: pkg.version, action: "skip-private" };
    if (isPublished(pkg.name, pkg.version)) return { name: pkg.name, version: pkg.version, action: "skip-published" };
    return { name: pkg.name, version: pkg.version, action: "publish" };
  });
}

function registryHas(name, version) {
  const r = runNpm(["view", `${name}@${version}`, "version"], { encoding: "utf8" });
  if (r.status === 0) return r.stdout.trim() === version;
  if (/E404|404 Not Found/.test(`${r.stderr}${r.stdout}`)) return false;
  throw new Error(`npm view ${name}@${version} mislukt:\n${r.stderr}`);
}

function main(argv) {
  const dryRun = argv.includes("--dry-run");
  const plan = planPublish(readPackages(ROOT), registryHas);
  for (const step of plan) {
    const id = `${step.name}@${step.version}`;
    if (step.action !== "publish") {
      console.log(`overgeslagen (${step.action === "skip-private" ? "privé" : "al gepubliceerd"}): ${id}`);
      continue;
    }
    console.log(`publiceren${dryRun ? " (dry-run)" : ""}: ${id}`);
    const args = ["publish", "-w", step.name, "--access", "public", ...(dryRun ? ["--dry-run"] : [])];
    const r = runNpm(args, { stdio: "inherit", cwd: ROOT });
    if (r.status !== 0) process.exit(r.status ?? 1);
  }
}

if (process.argv[1]?.endsWith("publish-npm.mjs")) main(process.argv.slice(2));
