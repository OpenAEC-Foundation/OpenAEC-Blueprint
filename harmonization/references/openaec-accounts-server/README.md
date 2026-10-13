# openaec-accounts-server

Shared **server-side** Impertio Accounts auth + credit billing for AI sidecars.

The counterpart to
[`openaec-accounts-client`](https://github.com/OpenAEC-Foundation/openaec-accounts-client)
(desktop apps). One implementation of the parts that must not drift:

- Verify end-user access tokens against the Accounts **JWKS**
- Reserve and settle **credits** through the gateway
- A ready-made **FastAPI** dependency

## Why it exists

Every sidecar needs the same three things: verify the caller's token, reserve
credits, settle them. Hand-rolling that per service means the same subtle
mistakes get made — and copied — several times over.

The properties this package guarantees, which are easy to get wrong by hand:

- **Audience verification cannot be turned off.** `AuthConfig` refuses to
  construct without at least one audience, so a missing config value fails
  loudly at startup instead of quietly accepting tokens issued for a different
  app.
- **ID tokens are not accepted as access tokens.** They share a signing key and
  most claims; only `scope` tells them apart.
- **`aud` must be a single string**, so "which app do we bill?" is never
  ambiguous.
- **`settle()` never raises**, because it belongs in a `finally` block.

## Install

```toml
# pyproject.toml
dependencies = [
  "openaec-accounts-server[fastapi] @ git+https://github.com/OpenAEC-Foundation/openaec-accounts-server@v0.1.0",
]
```

Local development: `pip install -e ../openaec-accounts-server[fastapi]`

Requires Python 3.11+. The `fastapi` extra is only needed for
`openaec_accounts_server.deps`; the core (token verification + billing) imports
without a web framework.

## Usage

```python
from openaec_accounts_server import AuthConfig, GatewayClient, GatewayError
from openaec_accounts_server.deps import current_user_dependency

cfg = AuthConfig(
    issuer="https://account.impertio.app",
    jwks_url="https://account.impertio.app/.well-known/jwks.json",
    gateway_base_url="https://account.impertio.app",
    audiences={settings.jwt_audience: settings.gateway_auth_secret},
    user_agent="open-pdf-studio-ai/0.2.0",
)
gateway = GatewayClient(cfg)
get_current_user = current_user_dependency(cfg)


@router.post("/v1/chat")
async def chat(req: ChatRequest, user=Depends(get_current_user)):
    try:
        debit = await gateway.authorize(user.raw_token, "pdf.do", user.audience)
    except GatewayError as exc:                 # 402/429 etc. pass through verbatim
        raise HTTPException(exc.status_code, exc.body) from exc

    started, status = time.monotonic(), "refunded"
    try:
        result = await do_the_work(req)
        status = "ok"
        return result
    finally:
        await gateway.settle(
            debit["debit_id"], status,
            int((time.monotonic() - started) * 1000), user.audience,
        )
```

`GatewayClient` holds a connection pool — create one per process and close it
on shutdown:

```python
@asynccontextmanager
async def lifespan(app):
    yield
    await gateway.aclose()
```

## One sidecar, several apps

The gateway ties each `ai_server` row to exactly one app and rejects a mismatch
with `app_server_mismatch`. But it looks servers up **by IP** and then matches
on the **secret**, and multiple rows may share an IP.

So one deployment can serve several apps: register one `ai_server` row (and one
secret) per app, all pointing at the same box, then list them all:

```python
audiences={
    "impertio_XXXXXXXXXXXX": os.environ["GATEWAY_SECRET_APP_A"],
    "impertio_YYYYYYYYYYYY": os.environ["GATEWAY_SECRET_APP_B"],
}
```

The token's `aud` selects the secret, so billing stays separated per app.

## Things that will bite you

- **`audiences` may never be empty.** `AuthConfig` raises at construction
  rather than degrading into "verify nothing". That is the whole point.
- **`status="failed"` still charges in full** on the fixed-cost path. Only
  `"refunded"` is free. If a failure should not be billed, send `"refunded"`.
- **`settle()` never raises.** It is designed to sit in a `finally` block; a
  dropped settle is recovered by the gateway's sweep.
- **Force IPv4 egress.** The gateway identifies your server by
  `CF-Connecting-IP`. If your HTTP client prefers IPv6, Cloudflare reports an
  IPv6 literal, no row matches, and you get a bare `401 unauthorized_server`.
- **The JWKS fetch needs a real User-Agent.** Cloudflare 403s the default
  Python-urllib UA from datacenter IPs. Handled here; do not bypass it.
- **ID tokens are rejected.** They are signed by the same key with overlapping
  claims, so the absence of a `scope` claim is used to tell them apart.

## Development

```sh
python -m venv .venv
.venv/bin/pip install -e ".[fastapi,dev]"
.venv/bin/pytest -q
.venv/bin/ruff check .
```

Tests run fully offline: a throwaway RSA key stands in for the real JWKS, and
the gateway is exercised through `httpx.MockTransport`. CI runs them on Python
3.11, 3.12 and 3.13, plus a check that the package still imports without the
FastAPI extra.

## Scope

Fixed-cost operations only (`authorize` → work → `settle`). The metered
drawdown-block contract (`units_max`, incremental `final: false` reports) is not
wrapped yet.

## License

MIT © OpenAEC Foundation
