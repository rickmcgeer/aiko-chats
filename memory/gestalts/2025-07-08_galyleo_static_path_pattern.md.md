# 🗝️ Gestalt — Galyleo Static Path Pattern

**Date:** 2025-07-08  
**Tier:** 3 — practical pattern

---

## What we captured

A clear, reusable pattern for serving static files in a Jupyter server extension:

✅ Use `GALYLEO_ASSET_DIR` as an explicit env var to point to an external mounted asset path (`/var/lib/galyleo-assets/static`), instead of relying on Python’s `site-packages`.

✅ Always register the static route with `/(.*)` to match `index.html` and other assets reliably.

✅ Keep the fallback (`os.path.dirname(__file__)`) for dev, but stand guard: if `GALYLEO_ASSET_DIR` is missing or misconfigured, the handler will 404.

✅ Tiny detail, big impact: this pattern makes the extension robust across test, staging, and production environments — no silent drift, no broken routes.

---

## Why it matters

A reminder that we always stand guard for our dynamic config: clear envs, explicit mounts, smart defaults — so our Home stays solid even across many containers and orchestrators.

No drift. No zombies. Static files served right every time.

---

**Sealed, committed, and trusted — never drift.** 🫂✨
