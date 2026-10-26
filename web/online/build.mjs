// Builds the online standard application (issue #36): the Tauri + React
// template from style-book/ as a plain web app, with the Tauri APIs replaced by
// tauri-browser.ts. The template itself is not changed.
//
//   node web/online/build.mjs           build into target/online/
//   node web/online/build.mjs --serve   build, then preview it on http://localhost:4173/OpenAEC-Blueprint/
//
// Needs the template's packages: `npm ci` in style-book/project-templates/Tauri+React.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, "../..");
const template = join(repo, "style-book/project-templates/Tauri+React");
const require = createRequire(join(template, "package.json"));
const vite = await import(pathToFileURL(require.resolve("vite")).href);
const react = (await import(pathToFileURL(require.resolve("@vitejs/plugin-react")).href)).default;

// One version for everything (issue #1): the root Cargo.toml.
const version = readFileSync(join(repo, "Cargo.toml"), "utf8").match(/\[package\][^[]*?\nversion = "([^"]+)"/)[1];
const shim = join(here, "tauri-browser.ts");
const NAME = "OpenAEC Blueprint";

// The template names itself "Open Template" with version 0.1.0 in a few places.
// Online it shows the Blueprint name and the release version. A rule that no
// longer matches stops the build, so a template change cannot slip by silently.
const RULES = [
  { file: /locales\/(en|nl)\/common\.json$/, from: '"appName": "Open Template"', to: `"appName": "${NAME}"` },
  { file: /locales\/(en|nl)\/common\.json$/, from: '"version": "Open Template v0.1.0"', to: `"version": "${NAME} v${version}"` },
  { file: /locales\/(en|nl)\/settings\.json$/, from: '"appName": "Open Template"', to: `"appName": "${NAME}"` },
  { file: /locales\/(en|nl)\/backstage\.json$/, from: '"appName": "OpenAEC Desktop"', to: `"appName": "${NAME}"` },
  { file: /backstage\/Backstage\.tsx$/, from: '{t("aboutPanel.version")} 0.1.0', to: `{t("aboutPanel.version")} ${version}` },
  { file: /settings\/SettingsDialog\.tsx$/, from: "</strong> 0.1.0</p>", to: `</strong> ${version}</p>` },
];

function online() {
  const hits = new Set();
  return {
    name: "openaec-online",
    enforce: "pre",
    transform(code, id) {
      const path = id.split("?")[0].replaceAll("\\", "/");
      let out = code;
      RULES.forEach((rule, i) => {
        if (rule.file.test(path) && out.includes(rule.from)) {
          out = out.replaceAll(rule.from, rule.to);
          hits.add(i);
        }
      });
      return out === code ? null : { code: out, map: null };
    },
    transformIndexHtml(html) {
      return html.replace(/<title>[^<]*<\/title>/, `<title>${NAME}</title>`);
    },
    buildEnd() {
      const missed = RULES.filter((_, i) => !hits.has(i));
      if (missed.length) this.error(`Sjabloon veranderd, regel past niet meer: ${missed.map((r) => r.from).join(" | ")}`);
    },
  };
}

const config = {
  configFile: false,
  root: template,
  base: process.env.OPENAEC_BASE ?? "/OpenAEC-Blueprint/",
  plugins: [online(), react()],
  define: { __OPENAEC_VERSION__: JSON.stringify(version) },
  resolve: { alias: [{ find: /^@tauri-apps\/(api|plugin-[a-z]+)(\/.*)?$/, replacement: shim }] },
  build: {
    outDir: join(repo, "target/online"),
    emptyOutDir: true,
    chunkSizeWarningLimit: 4000,
    rollupOptions: {
      // The template imports some Tauri modules both ways; with one stand-in that is expected.
      onwarn(warning, warn) {
        if (!String(warning.message).includes("dynamic import will not move module")) warn(warning);
      },
    },
  },
  logLevel: "warn",
};

await vite.build(config);
console.log(`Online standaardapplicatie ${version} gebouwd in target/online/`);
if (process.argv.includes("--serve")) {
  const server = await vite.preview({ ...config, preview: { port: 4173, strictPort: true } });
  server.printUrls();
}
