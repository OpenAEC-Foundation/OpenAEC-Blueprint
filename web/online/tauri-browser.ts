// Browser stand-ins for the Tauri APIs the standard application uses (issue #36).
// The online build aliases every `@tauri-apps/*` import to this file, so the
// template in style-book/ runs unchanged in a plain browser tab.

declare const __OPENAEC_VERSION__: string;

const params = new URLSearchParams(window.location.search);
const label = params.get("detached") === "true" ? `detached-${params.get("view") ?? "view"}` : "main";

// @tauri-apps/api/app
export const getVersion = async () => __OPENAEC_VERSION__;
export const getName = async () => "OpenAEC Blueprint";
export const getTauriVersion = async () => "";

// @tauri-apps/api/window: window buttons have nothing to do in a browser tab.
const windowMethods: Record<string, unknown> = {
  label,
  isMaximized: async () => false,
  isMinimized: async () => false,
  isFullscreen: async () => !!document.fullscreenElement,
  isVisible: async () => true,
  toggleMaximize: async () => {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen().catch(() => {});
  },
  close: async () => window.close(),
};
const currentWindow = new Proxy(windowMethods, {
  get(target, prop: string) {
    if (prop in target) return target[prop];
    if (prop === "then") return undefined;
    // onResized, onCloseRequested, listen, once, …: return an unlisten function.
    if (prop.startsWith("on") || prop === "listen" || prop === "once") return async () => () => {};
    return async () => undefined;
  },
});
export const getCurrentWindow = () => currentWindow;
export const getCurrentWebviewWindow = getCurrentWindow;
export const Window = { getCurrent: getCurrentWindow };

// @tauri-apps/api/webviewWindow: a detached view opens as a browser window.
const opened = new Map<string, globalThis.Window>();
export class WebviewWindow {
  label: string;
  constructor(windowLabel: string, options: { url?: string; width?: number; height?: number } = {}) {
    this.label = windowLabel;
    const popup = window.open(options.url ?? "index.html", windowLabel, `popup,width=${options.width ?? 800},height=${options.height ?? 600}`);
    if (popup) opened.set(windowLabel, popup);
  }
  once() {
    return Promise.resolve(() => {});
  }
  async close() {
    opened.get(this.label)?.close();
    opened.delete(this.label);
  }
  static async getByLabel(windowLabel: string) {
    if (!opened.has(windowLabel)) return null;
    const handle = Object.create(WebviewWindow.prototype) as WebviewWindow;
    handle.label = windowLabel;
    return handle;
  }
}

// @tauri-apps/api/event: events between windows go over a BroadcastChannel.
const channel = "BroadcastChannel" in window ? new BroadcastChannel("openaec-blueprint") : null;
export async function emit(event: string, payload?: unknown) {
  channel?.postMessage({ event, payload });
}
export async function listen(event: string, handler: (e: { event: string; payload: unknown }) => void) {
  const onMessage = (m: MessageEvent) => {
    if (m.data?.event === event) handler({ event, payload: m.data.payload });
  };
  channel?.addEventListener("message", onMessage);
  return () => channel?.removeEventListener("message", onMessage);
}
export const once = listen;

// @tauri-apps/api/core: there is no Rust side online.
export async function invoke(command: string): Promise<never> {
  throw new Error(`"${command}" is not available in the online version`);
}

// @tauri-apps/plugin-store: settings live in localStorage.
const PREFIX = "openaec-blueprint:";
export class Store {
  constructor(private file: string) {}
  private key(k: string) {
    return `${PREFIX}${this.file}:${k}`;
  }
  async get<T>(k: string): Promise<T | undefined> {
    try {
      const raw = localStorage.getItem(this.key(k));
      return raw === null ? undefined : (JSON.parse(raw) as T);
    } catch {
      return undefined;
    }
  }
  async set(k: string, value: unknown) {
    try {
      localStorage.setItem(this.key(k), JSON.stringify(value));
    } catch {
      // Private windows may refuse storage; settings then last for this tab only.
    }
  }
  async delete(k: string) {
    try {
      localStorage.removeItem(this.key(k));
    } catch {
      // See set().
    }
    return true;
  }
  async save() {}
}
export const load = async (file: string) => new Store(file);

// @tauri-apps/plugin-opener
export async function openUrl(url: string) {
  window.open(url, "_blank", "noopener,noreferrer");
}
export const openPath = async () => {};

// @tauri-apps/plugin-dialog: no file system online.
export const save = async () => null;
export const open = async () => null;
export const message = async (text: string) => window.alert(text);
export const ask = async (text: string) => window.confirm(text);
export const confirm = ask;

// @tauri-apps/plugin-os
export const type = () => "Browser";
export const platform = () => "browser";
export const version = () => navigator.userAgent;
export const arch = () => "";
