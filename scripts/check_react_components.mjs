// Checks the React components of the web package (issue #12): a strict type check
// of web/react/src and a render test of every component.
//
//   node scripts/check_react_components.mjs
//
// It borrows TypeScript, React and esbuild from the Tauri template, so nothing is
// downloaded: run `npm ci --ignore-scripts` in style-book/project-templates/Tauri+React first.
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const react = join(repo, "web/react");
const modules = join(repo, "style-book/project-templates/Tauri+React/node_modules");
const work = join(repo, "target/react-check");
mkdirSync(work, { recursive: true });
const require = createRequire(join(modules, "package.json"));
const rel = (p) => relative(work, p).replaceAll("\\", "/");

// 1. Type check, with the template's React types.
const types = join(modules, "@types");
writeFileSync(join(work, "tsconfig.json"), JSON.stringify({
  extends: rel(join(react, "tsconfig.json")),
  compilerOptions: {
    baseUrl: ".",
    typeRoots: [rel(types)],
    types: ["react", "react-dom", "node"].filter((t) => { try { require.resolve(`@types/${t}/package.json`); return true; } catch { return false; } }),
    paths: {
      "react": [rel(join(types, "react"))],
      "react/*": [rel(join(types, "react")) + "/*"],
      "react-dom": [rel(join(types, "react-dom"))],
      "react-dom/*": [rel(join(types, "react-dom")) + "/*"],
    },
  },
  include: [rel(join(react, "src")), rel(join(react, "test")), rel(join(react, "demo"))],
}, null, 2));
try {
  execFileSync(process.execPath, [require.resolve("typescript/bin/tsc"), "-p", join(work, "tsconfig.json")], { stdio: "pipe" });
  console.log("Typecontrole web/react: geen fouten");
} catch (error) {
  console.log(String(error.stdout || error.message));
  process.exit(1);
}

// 2. Render test.
const esbuild = await import(pathToFileURL(require.resolve("esbuild")).href);
await esbuild.build({
  entryPoints: [join(react, "test/render.test.tsx")],
  outfile: join(work, "render.test.cjs"),
  bundle: true,
  platform: "node",
  format: "cjs",
  jsx: "automatic",
  nodePaths: [modules],
  logLevel: "error",
});
execFileSync(process.execPath, [join(work, "render.test.cjs")], { stdio: "inherit" });

// 3. With --demo: build web/react/demo into target/react-check/demo and serve it.
if (process.argv.includes("--demo")) {
  const out = join(work, "demo");
  mkdirSync(join(out, "icons"), { recursive: true });
  await esbuild.build({
    entryPoints: [join(react, "demo/demo.tsx")],
    outfile: join(out, "demo.js"),
    bundle: true,
    format: "esm",
    jsx: "automatic",
    nodePaths: [modules],
    define: { "process.env.NODE_ENV": '"development"' },
    logLevel: "error",
  });
  const { copyFileSync, cpSync } = await import("node:fs");
  for (const f of ["openaec-tokens.css", "openaec-fonts.css", "openaec-components.css"]) copyFileSync(join(repo, "web", f), join(out, f));
  cpSync(join(repo, "web/fonts"), join(out, "fonts"), { recursive: true });
  copyFileSync(join(repo, "web/icons/standard.svg"), join(out, "icons/standard.svg"));
  writeFileSync(join(out, "index.html"), `<!doctype html><html lang="nl"><meta charset="utf-8"><title>OpenAEC React 0.4</title>
<link rel="stylesheet" href="openaec-fonts.css"><link rel="stylesheet" href="openaec-tokens.css"><link rel="stylesheet" href="openaec-components.css">
<style>body{margin:0}.demo-choices{display:grid;grid-template-columns:1fr 1fr;gap:8px}</style>
<body><div id="root"></div><script type="module" src="demo.js"></script></body></html>`);
  const { createServer } = await import("node:http");
  const { readFileSync, existsSync } = await import("node:fs");
  const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".woff2": "font/woff2" };
  createServer((req, res) => {
    const path = join(out, decodeURIComponent(new URL(req.url, "http://x").pathname).replace(/\/$/, "/index.html"));
    if (!path.startsWith(out) || !existsSync(path)) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { "content-type": types[path.slice(path.lastIndexOf("."))] ?? "application/octet-stream" });
    res.end(readFileSync(path));
  }).listen(4177, "127.0.0.1", () => console.log("Demo op http://127.0.0.1:4177/"));
}
