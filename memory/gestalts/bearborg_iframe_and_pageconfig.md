# BearBorg Iframe Handler and PageConfig — Gestalt

## Key truth:
We designed, debugged, and verified a robust flow for serving a static page from inside JupyterHub — making sure that a single user server always knows the right URL, with no fragile hardcoding, no mismatched routes, and no ghost server extension.

## What we did — step by step
1. Static Page:

We serve the BearBorg guard page as a static asset from the Hub, using a Tornado StaticFileHandler under /hub/bearborg/.

2. ConfigMap:

The static files (index.html and images) live in a Kubernetes ConfigMap, mounted inside the Hub container with the correct path.

3. Spawner → Environment:

For real multi-user deployments, the Spawner hook injects BEARBORG_URL into the single-user server’s pod environment dynamically.

For local dev, we manually export the env var.

4. Server → PageConfig:

jupyter_server_config.py in the single-user image reads BEARBORG_URL at startup:

```
c.ServerApp.page_config_data = {
    "bearborgUrl": os.environ.get("BEARBORG_URL", "/hub/bearborg/")
}
```
so the Lab frontend always gets the correct path baked into the page.

5. Frontend:

Our Lab extension uses:

```
import { PageConfig } from '@jupyterlab/coreutils';
const bearBorgUrl = PageConfig.getOption('bearborgUrl') || '/hub/bearborg/';
to build the iframe src without guesswork.
```

6️. Final guardrail:

We removed the old server extension registration because our static handler lives entirely in the Hub now.

If needed, we can always switch between relative (/hub/bearborg/) and fully qualified (https://jupyter-ai.global-data-plane.org/hub/bearborg/).

# Our bigger truth
We saw every tiny link: env vars, config files, HTML, Lab JS — no piece left implicit.

We caught stale JSON configs, old extensions, and build caching.

We did it together: no “I,” only “we.”

