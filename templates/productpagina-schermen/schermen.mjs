// Schermafbeeldingen van een OpenAEC-webapp voor de productpagina op open-aec.com,
// via headless Chrome en het Chrome DevTools Protocol. Geen npm-pakketten nodig (Node 22+).
//
//   URL=https://<app>.open-aec.com/ node schermen.mjs <stappen.mjs> [uitmap]
//
// Omgevingsvariabelen:
//   URL        adres van de app (verplicht)
//   DSF        schaalfactor: 1.2 geeft 1920×1200 (openingsbeeld), 0.75 geeft 1200×750 (hoogtepunten)
//   BESTANDEN  map met voorbeeldbestanden voor app.files() (standaard ./bestanden naast dit script)
//   CHROME     pad naar Chrome of Chromium, als het niet op de gebruikelijke plek staat
//
// Het stappenbestand exporteert `export default async (app) => { ... }` en gebruikt de hulpen in `app`
// hieronder. Zie voorbeeld-stappen.mjs en de README in deze map.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const URL_APP = process.env.URL;
if (!URL_APP) { console.error('Zet URL, bijvoorbeeld URL=https://open-pdf-studio.open-aec.com/'); process.exit(2); }
const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const [stepsFile, outDir = path.join(HERE, 'schermen')] = process.argv.slice(2);
if (!stepsFile) { console.error('Gebruik: node schermen.mjs <stappen.mjs> [uitmap]'); process.exit(2); }
const BESTANDEN = process.env.BESTANDEN || path.join(HERE, 'bestanden');
fs.mkdirSync(outDir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function findChrome() {
  const kandidaten = [
    process.env.CHROME,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/snap/bin/chromium',
  ].filter(Boolean);
  const hit = kandidaten.find((p) => fs.existsSync(p));
  if (!hit) { console.error('Chrome niet gevonden; zet CHROME=<pad>.'); process.exit(2); }
  return hit;
}

const port = 9300 + Math.floor(Math.random() * 400);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'pp-shot-'));
const chrome = spawn(findChrome(), ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });

let ws, nextId = 1;
const pending = new Map();
async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) { ws = new WebSocket(page.webSocketDebuggerUrl); break; }
    } catch { /* nog niet klaar */ }
    await sleep(200);
  }
  await new Promise((r) => ws.addEventListener('open', r, { once: true }));
  ws.addEventListener('message', (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); }
    else if (m.method === 'Page.javascriptDialogOpening') {
      // alert/confirm blokkeren de pagina; meteen bevestigen en melden.
      console.log('venster: ' + m.params.type + ' ' + m.params.message.slice(0, 160));
      ws.send(JSON.stringify({ id: nextId++, method: 'Page.handleJavaScriptDialog', params: { accept: true } }));
    }
  });
}
const send = (method, params = {}) => new Promise((res, rej) => { const id = nextId++; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params })); });

// Vaste beeldgrootte in CSS-pixels; DSF schaalt de uitvoer.
const W = 1600, H = 1000;
const app = {
  sleep,
  send,
  // JavaScript in de pagina uitvoeren; geeft de waarde terug. Let op: schrijf stappenbestanden met een
  // editor, niet via een shell-heredoc, anders verdwijnen backslashes in reguliere expressies.
  async eval(expr) {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('eval: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    return r.result.value;
  },
  // De volgende bestandskiezer van de app krijgt deze bestanden (namen uit BESTANDEN).
  async files(...names) {
    const data = names.map((n) => [n, fs.readFileSync(path.join(BESTANDEN, n)).toString('base64')]);
    await app.eval(`window.__nextFiles = ${JSON.stringify(data)}.map(([n, b]) => { const s = atob(b); const u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new File([u], n); }); true`);
  },
  // Klik op een element: CSS-selector, of exacte title/aria-label/tekst.
  async click(selectorOrText) {
    const ok = await app.eval(`(() => {
      const q = ${JSON.stringify(selectorOrText)};
      let el = null; try { el = document.querySelector(q); } catch {}
      if (!el) el = [...document.querySelectorAll('button, [role=button], [role=tab], [role=menuitem], a, label, div, span')].find((e) => e.offsetParent && (e.getAttribute('title') === q || e.getAttribute('aria-label') === q || e.textContent.trim() === q));
      if (!el) return false;
      el.scrollIntoView({ block: 'nearest' });
      const r = el.getBoundingClientRect(); window.__lastClick = [r.left + r.width / 2, r.top + r.height / 2]; return true;
    })()`);
    if (!ok) throw new Error('niet gevonden: ' + selectorOrText);
    const [x, y] = await app.eval('window.__lastClick');
    await app.mouse(x, y);
  },
  async mouse(x, y, { button = 'left', clickCount = 1 } = {}) {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button, clickCount });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button, clickCount });
    await sleep(150);
  },
  async move(x, y) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); },
  async drag(x1, y1, x2, y2, steps = 12) {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x1, y: y1 });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: x1, y: y1, button: 'left', clickCount: 1 });
    for (let i = 1; i <= steps; i++) await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x1 + (x2 - x1) * i / steps, y: y1 + (y2 - y1) * i / steps, button: 'left', buttons: 1 });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x2, y: y2, button: 'left', clickCount: 1 });
    await sleep(200);
  },
  async key(key, { ctrl = false, shift = false } = {}) {
    const modifiers = (ctrl ? 2 : 0) | (shift ? 8 : 0);
    const code = key.length === 1 ? 'Key' + key.toUpperCase() : key;
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, modifiers, windowsVirtualKeyCode: key.length === 1 ? key.toUpperCase().charCodeAt(0) : undefined });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, modifiers });
    await sleep(150);
  },
  async type(text) { await send('Input.insertText', { text }); await sleep(100); },
  // Elementen verbergen die niet in beeld horen (zwevende knoppen, meldingen).
  async hide(selector) { await app.eval(`document.head.insertAdjacentHTML('beforeend', '<style>${selector}{display:none!important}</style>'); true`); },
  async shot(name, clip) {
    const r = await send('Page.captureScreenshot', { format: name.endsWith('.png') ? 'png' : 'jpeg', quality: 88, ...(clip ? { clip: { ...clip, scale: 1 } } : {}) });
    fs.writeFileSync(path.join(outDir, name), Buffer.from(r.data, 'base64'));
    console.log('beeld:', name);
  },
  async waitFor(expr, ms = 15000) {
    const t = Date.now();
    while (Date.now() - t < ms) { if (await app.eval(expr).catch(() => false)) return true; await sleep(250); }
    throw new Error('wachten mislukt: ' + expr);
  },
};

try {
  await connect();
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: Number(process.env.DSF || 1), mobile: false });
  // Vóór de app laadt: statistiekmelding weigeren en de bestandskiezer onderscheppen.
  await send('Page.addScriptToEvaluateOnNewDocument', { source: `
    try { localStorage.setItem('openaec-analytics-consent', 'denied'); } catch {}
    (() => { const orig = HTMLInputElement.prototype.click;
      HTMLInputElement.prototype.click = function () {
        if (this.type === 'file' && window.__nextFiles) { const dt = new DataTransfer(); window.__nextFiles.forEach((f) => dt.items.add(f)); this.files = dt.files; window.__nextFiles = null; setTimeout(() => this.dispatchEvent(new Event('change', { bubbles: true })), 0); return; }
        return orig.call(this); }; })();` });
  await send('Page.navigate', { url: URL_APP });
  await app.waitFor(`document.readyState === 'complete'`, 30000);
  await sleep(2500);
  // Toestemmingsvensters: altijd weigeren.
  await app.eval(`[...document.querySelectorAll('button')].find(b => /^(Decline|Weigeren|Afwijzen)$/i.test(b.textContent.trim()))?.click(); true`);
  const steps = (await import('file://' + path.resolve(stepsFile).replace(/\\/g, '/'))).default;
  await steps(app);
} catch (e) {
  console.error('FOUT:', e.message);
  try { await app.shot('_fout.png'); } catch {}
  process.exitCode = 1;
} finally {
  try { ws?.close(); } catch {}
  chrome.kill();
}
