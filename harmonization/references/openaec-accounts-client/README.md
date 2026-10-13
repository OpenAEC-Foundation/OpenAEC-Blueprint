# openaec-accounts-client

Shared **"Sign in with OpenAEC"** client for Impertio desktop apps (Tauri v2).

One copy of the security-sensitive parts, so a fix lands everywhere at once:

- OIDC **Authorization Code + PKCE** through the system browser, loopback redirect (RFC 8252)
- Tokens in the **OS keyring** — they never reach the webview
- Automatic refresh on `401`, with a **safe distinction** between a rejected session (tokens cleared) and a transient network failure (tokens kept)
- Authenticated calls to **two hosts**: the Accounts API and the AI sidecar
- Expiry-aware session restore, so a dead session never renders as "signed in"

## Usage

Add the dependency:

```toml
# local development — adjust the depth to wherever your src-tauri/Cargo.toml
# sits relative to this checkout (in a nested Tauri layout it is often ../../../)
openaec-accounts-client = { path = "../../openaec-accounts-client" }

# once published — always pin a tag, never a branch
openaec-accounts-client = { git = "https://github.com/OpenAEC-Foundation/openaec-accounts-client", tag = "v0.1.0" }
```

## Platform support

Windows, macOS and Linux. The keyring backend is selected per target, so no
feature flags are needed in the consuming app:

| Target | Backend |
|---|---|
| Windows | Credential Manager |
| macOS | Keychain |
| Linux | Secret Service (via D-Bus) |

⚠️ **Linux needs a Secret Service provider at runtime** — gnome-keyring, KWallet
or equivalent. On a headless box or a minimal container there is nowhere to put
the tokens and sign-in fails when it tries to save them. Building on Linux also
needs `libdbus-1-dev` (plus the usual Tauri webkit packages).

Initialise once in `run()`, **before** any command executes:

```rust
openaec_accounts_client::init(openaec_accounts_client::Setup {
    keyring_service: "my-app-openaec".into(),   // MUST be unique per app
    config_env_var: "OPENAEC_ACCOUNTS_CONFIG".into(),
    app_name: "My App".into(),
    defaults: openaec_accounts_client::AccountsConfig {
        issuer: "https://account.impertio.app".into(),
        client_id: "impertio_XXXXXXXXXXXX".into(),
        redirect_uri: "http://127.0.0.1:53682/callback".into(),
        scopes: "openid profile email offline_access".into(),
        accounts_api_url: "https://account.impertio.app".into(),
        ai_api_url: "https://open-pdf-studio-ai.impertio.app".into(),
    },
});
```

Register the commands:

```rust
tauri::generate_handler![
    openaec_accounts_client::client::accounts_sign_in,
    openaec_accounts_client::client::accounts_get_user,
    openaec_accounts_client::client::accounts_sign_out,
    openaec_accounts_client::client::accounts_fetch,
    openaec_accounts_client::client::ai_fetch,
    openaec_accounts_client::client::accounts_portal_url,
    openaec_accounts_client::client::accounts_upload_file,
    openaec_accounts_client::client::accounts_download_file,
    openaec_accounts_client::client::accounts_brand_logo,
]
```

## Calling it from the frontend

This is the interface your app actually uses. All commands go through Tauri's
`invoke`. **Arguments are camelCase** (`pageText`, not `page_text`) — Tauri
converts them to snake_case on the Rust side.

### Sign in / out

```js
import { invoke } from '@tauri-apps/api/core';

// Opens the system browser. Resolves with the profile once the user returns.
// pageText is optional; supply it from your i18n so the page the browser
// lands on speaks the user's language instead of falling back to English.
const user = await invoke('accounts_sign_in', {
  pageText: {
    okTitle: t('signedIn'),
    okBody: t('closeThisWindow'),
    cancelledTitle: t('signInCancelled'),
    cancelledBody: t('closeThisWindow'),
  },
});
// -> { sub: "…", name: "Ada Lovelace", email: "ada@example.com" }

await invoke('accounts_sign_out');   // wipes the local tokens, returns nothing
```

### Restore the session at startup

```js
const user = await invoke('accounts_get_user');   // profile, or null
```

Checks `exp`, and transparently refreshes when the access token has expired but
the session is still renewable.

> **Call this from ONE place.** Refresh tokens rotate with reuse detection
> server-side: two concurrent refreshes revoke the whole session. The crate
> serialises refreshes internally, but you should still single-flight this in
> your store rather than calling it from every component:
>
> ```js
> let inFlight = null;
> export function loadUser() {
>   if (!inFlight) inFlight = invoke('accounts_get_user').finally(() => { inFlight = null; });
>   return inFlight;
> }
> ```

### Authenticated requests

```js
// Accounts API (accountsApiUrl)
const apps = await invoke('accounts_fetch', { path: '/me/apps' });               // GET
const made = await invoke('accounts_fetch', { path: '/me/apps', method: 'POST', body: { name: 'x' } });

// AI sidecar (aiApiUrl) — a DIFFERENT host. Using accounts_fetch here would
// send the request to the wrong server.
const answer = await invoke('ai_fetch', {
  path: '/v1/chat',
  method: 'POST',                       // defaults to POST
  body: { action: 'summarize', text, stream: false },
});

const portal = await invoke('accounts_portal_url');   // "https://account.impertio.app"
```

Both return the parsed JSON body. A non-JSON body comes back as a plain string.

### Other commands

```js
await invoke('accounts_upload_file', { fileName: 'a/b.pdf', content: [...bytes] });
const base64 = await invoke('accounts_download_file', { id: 'file_123' });
const logo   = await invoke('accounts_brand_logo');   // data: URL, or null on 404
```

### Errors

Commands **reject with a string**, so `catch` receives a message rather than an
object. The stable shapes worth matching on:

| Pattern | Means |
|---|---|
| `not signed in` | No token in the keyring |
| `no refresh token — sign in again` | Session cannot be renewed |
| `refresh rejected (400): …` | Server refused the refresh; tokens were cleared |
| `Accounts API returned 402: …` | Out of credits (`INSUFFICIENT_CREDITS` in the body) |
| `AI-server returned 429: …` | Rate limited |
| `AI-server returned 5xx: …` | Service is down |
| `… unreachable (url): …` | Could not connect |
| `… timed out` | Connected, but no answer within the timeout |

The service name is `Accounts API` or `AI-server` depending on which host was
called — don't assume one.

```js
try {
  await invoke('ai_fetch', { path: '/v1/chat', method: 'POST', body });
} catch (e) {
  const raw = String(e);
  const status = Number((raw.match(/(?:Accounts API|AI-server) returned (\d{3})/) || [])[1]) || null;
  if (/not signed in|no refresh token/i.test(raw) || status === 401) showSignIn();
  else if (status === 402) showOutOfCredits();
  else if (/unreachable/i.test(raw)) showOffline();
}
```

> Signed-in state is a **UI hint**, never an authorization decision. The server
> verifies every request; this only avoids showing a stale label.

## Runtime config

`config_env_var` points at a JSON file that overrides `defaults` — handy for
switching an app between dev and production without a rebuild. Keys are
camelCase:

```json
{
  "issuer": "https://account.impertio.app",
  "clientId": "impertio_XXXXXXXXXXXX",
  "redirectUri": "http://127.0.0.1:53682/callback",
  "scopes": "openid profile email offline_access",
  "accountsApiUrl": "https://account.impertio.app",
  "aiApiUrl": "https://open-pdf-studio-ai.impertio.app"
}
```

## Things that will bite you

- **`keyring_service` must be unique per app.** Two apps sharing it will
  overwrite each other's tokens.
- **Register the redirect URI as `127.0.0.1`, not `localhost`.** accounts-impertio
  applies RFC 8252 §7.3's port-agnostic loopback rule only to `127.0.0.1` and
  `[::1]`. With `localhost` the URI must match exactly, port included, and
  sign-in breaks the moment that port is taken.
- **The callback page text comes from the caller** (`page_text` on
  `accounts_sign_in`), so it follows the app's own translations. Omit it and it
  falls back to English.
- **`accounts_fetch` and `ai_fetch` target different hosts.** `/v1/chat` lives on
  the AI sidecar; sending it through `accounts_fetch` reaches the wrong server.
- **Signed-in state is a UI hint, never an authorization decision.** The server
  verifies every request; this crate only avoids showing a stale label.

- **`init()` must run before any command.** The commands read the setup through
  a `OnceLock` and panic with a clear message if it is missing, rather than
  silently using a placeholder.

## Development

```sh
cargo test          # unit tests — no network, no keyring
cargo clippy --all-targets
cargo fmt --all --check
```

CI runs all three on Windows, macOS and Linux. The tests cover the pure logic
(token expiry, refresh classification, callback parsing, config parsing);
anything needing a live Accounts instance or a real keyring is deliberately
left to integration testing in a consuming app.

## Commands

| Command | Purpose |
|---|---|
| `accounts_sign_in` | System-browser OIDC login; returns the profile |
| `accounts_get_user` | Restore session (expiry-checked, refreshes if needed) |
| `accounts_sign_out` | Wipe tokens locally |
| `accounts_fetch` | Authenticated call to the Accounts API |
| `ai_fetch` | Authenticated call to the AI sidecar |
| `accounts_portal_url` | Portal base URL, from config |
| `accounts_upload_file` / `accounts_download_file` | Cloud storage |
| `accounts_brand_logo` | Tenant branding |

## License

MIT © OpenAEC Foundation
