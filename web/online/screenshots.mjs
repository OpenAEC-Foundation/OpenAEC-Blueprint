// Screenshots of the online standard application, for the README.
//
//   node web/online/build.mjs --serve        in one terminal
//   node web/online/screenshots.mjs          in another
//   node web/online/screenshots.mjs --url https://openaec-foundation.github.io/OpenAEC-Blueprint/
//
// Opens the app in headless Chrome (1600x900, scale 1, English) through the DevTools protocol and
// clicks through it like a user would. Settings are put in localStorage before the page loads, the
// same keys the app itself writes (tauri-browser.ts). Output: design/online/*.png. Chrome is looked
// up in the usual places; set CHROME to use another one. `scripts/build_readme_images.py` turns
// these and the Rust renders into the README images.
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const OUT = join(root, "design", "online");
const VIEWPORT = { width: 1600, height: 900 };
const PORT = 9333;
const argv = process.argv.slice(2);
const urlArg = argv.indexOf("--url");
const URL_ = urlArg >= 0 ? argv[urlArg + 1] : "http://localhost:4173/OpenAEC-Blueprint/";
const PREFIX = "openaec-blueprint:preferences.json:";

const SHOTS = [
  { name: "online-light", theme: "light", steps: [] },
  { name: "online-3d-dark", theme: "dark", steps: [["click-text", "3D Viewer"], ["wait", 4000]] },
  { name: "online-settings-blueprint", theme: "blueprint", steps: [["click-label", "Preferences"], ["wait", 600], ["click-text", "Appearance"], ["wait", 600]] },
];

function findChrome() {
  const candidates = [
    process.env.CHROME,
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
  ];
  const found = candidates.find((c) => c && existsSync(c));
  if (!found) throw new Error("Chrome not found; set CHROME to its path");
  return found;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function connect() {
  for (let i = 0; i < 40; i++) {
    try {
      const pages = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = pages.find((p) => p.type === "page");
      if (page) return page.webSocketDebuggerUrl;
    } catch { /* not ready yet */ }
    await sleep(250);
  }
  throw new Error("Chrome did not open its DevTools port");
}

function client(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0;
  const pending = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { ok, fail } = pending.get(msg.id);
      pending.delete(msg.id);
      msg.error ? fail(new Error(msg.error.message)) : ok(msg.result);
    }
  };
  const send = (method, params = {}) =>
    new Promise((ok, fail) => {
      pending.set(++id, { ok, fail });
      ws.send(JSON.stringify({ id, method, params }));
    });
  return new Promise((ok) => (ws.onopen = () => ok({ send, close: () => ws.close() })));
}

async function evaluate(cdp, expression) {
  const { result, exceptionDetails } = await cdp.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (exceptionDetails) throw new Error(exceptionDetails.exception?.description ?? exceptionDetails.text);
  return result.value;
}

async function load(cdp, url) {
  await cdp.send("Page.navigate", { url });
  for (let i = 0; i < 80; i++) {
    await sleep(250);
    if ((await evaluate(cdp, "document.readyState")) === "complete") break;
  }
  await evaluate(cdp, "document.fonts.ready.then(() => true)");
  await sleep(1200);
}

// Click the centre of an element, with a real mouse event, so the app sees what a user does.
async function click(cdp, finder, what) {
  const box = await evaluate(cdp, `(() => {
    const el = (${finder})();
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  })()`);
  if (!box) throw new Error(`not found: ${what}`);
  for (const type of ["mousePressed", "mouseReleased"]) {
    await cdp.send("Input.dispatchMouseEvent", { type, x: box.x, y: box.y, button: "left", clickCount: 1 });
  }
}

const byText = (text) => `() => [...document.querySelectorAll("button, [role=tab], li, a, div")].find((el) => el.textContent.trim() === ${JSON.stringify(text)})`;
const byLabel = (label) => `() => document.querySelector(${JSON.stringify(`[aria-label="${label}"]`)})`;

const chrome = findChrome();
const profile = mkdtempSync(join(tmpdir(), "oa-shots-"));
const proc = spawn(chrome, [
  "--headless=new",
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profile}`,
  "--use-angle=swiftshader",
  "--enable-unsafe-swiftshader",
  "--hide-scrollbars",
  "--lang=en-US",
  `--window-size=${VIEWPORT.width},${VIEWPORT.height}`,
  "about:blank",
], { stdio: "ignore" });

let failed = 0;
try {
  const cdp = await client(await connect());
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", { ...VIEWPORT, deviceScaleFactor: 1, mobile: false });
  mkdirSync(OUT, { recursive: true });
  await load(cdp, URL_);
  for (const shot of SHOTS) {
    try {
      const settings = { theme: shot.theme, language: "en" };
      await evaluate(cdp, `(() => {
        localStorage.clear();
        for (const [k, v] of Object.entries(${JSON.stringify(settings)})) localStorage.setItem(${JSON.stringify(PREFIX)} + k, JSON.stringify(v));
        return true;
      })()`);
      await load(cdp, URL_);
      for (const [step, arg] of shot.steps) {
        if (step === "wait") await sleep(arg);
        if (step === "click-text") await click(cdp, byText(arg), arg);
        if (step === "click-label") await click(cdp, byLabel(arg), arg);
      }
      const { data } = await cdp.send("Page.captureScreenshot", { format: "png" });
      writeFileSync(join(OUT, `${shot.name}.png`), Buffer.from(data, "base64"));
      console.log(`design/online/${shot.name}.png`);
    } catch (error) {
      failed++;
      console.error(`${shot.name}: ${error.message}`);
    }
  }
  cdp.close();
} finally {
  proc.kill();
  await sleep(500);
  rmSync(profile, { recursive: true, force: true, maxRetries: 5 });
}
process.exit(failed ? 1 : 0);
