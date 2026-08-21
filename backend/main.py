"""
Substrait starter app — a single backend that serves both its web page and its API.

Substrait requires three things of this file:
  1. the server listens on port 8000          (set in cicd/Dockerfile.backend)
  2. GET /health returns 200                  (Substrait's readiness check)
  3. the JSON API lives under /api            (Substrait routes /api here)

Because this project has no frontend/ folder, Substrait sends ALL traffic to this
backend — including "/" — so this file also serves the page you see in the browser.

To change the app, describe what you want to your AI assistant. It will edit this file.
"""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Change this when you change the app.
APP_NAME = "My First Substrait App"

app = FastAPI(title=APP_NAME, docs_url="/api/docs")  # keep openapi_url at its default
                                                     # /openapi.json — the platform falls
                                                     # back to harvesting it at runtime


# ── Required by Substrait ──────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
def health():
    """Substrait calls this to decide whether the app started correctly."""
    return {"status": "ok"}


# ── Your API goes here. Every route must start with /api ───────────────────────
@app.get("/api/info")
def info():
    """A tiny endpoint so the page can prove the backend is really running."""
    return {
        "app": APP_NAME,
        "server_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


# ── The web page ───────────────────────────────────────────────────────────────
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__APP_NAME__</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; display: grid; place-items: center;
    font: 16px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background: #f6f7f9; color: #1c1e21; padding: 24px;
  }
  .card {
    background: #fff; border: 1px solid #e3e6ea; border-radius: 14px;
    padding: 40px; max-width: 560px; width: 100%;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
  }
  h1 { margin: 0 0 8px; font-size: 26px; letter-spacing: -.01em; }
  p  { margin: 0 0 20px; color: #5c6169; }
  .pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 7px 14px; border-radius: 999px; font-size: 14px; font-weight: 500;
    background: #f0f1f3; color: #5c6169;
  }
  .pill.ok   { background: #e7f6ec; color: #10682f; }
  .pill.fail { background: #fdecec; color: #9a1f1f; }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
  .next { margin-top: 28px; padding-top: 20px; border-top: 1px solid #eceef1;
          font-size: 14px; color: #5c6169; }
  code { background: #f0f1f3; padding: 2px 6px; border-radius: 5px; font-size: 13px; }
</style>
</head>
<body>
  <main class="card">
    <h1>__APP_NAME__</h1>
    <p>Your app is deployed and running on Substrait.</p>

    <span class="pill" id="status"><span class="dot"></span> Checking the backend…</span>

    <div class="next">
      This page is served by <code>backend/main.py</code>.
      Tell your AI assistant what you want to build and it will edit that file,
      then deploy again to see your changes live.
    </div>
  </main>

<script>
  // Calls this app's own API on the same address — no URL to configure.
  fetch("/api/info")
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(d => {
      const el = document.getElementById("status");
      el.className = "pill ok";
      el.innerHTML = '<span class="dot"></span> Backend responding &middot; ' + d.server_time;
    })
    .catch(() => {
      const el = document.getElementById("status");
      el.className = "pill fail";
      el.innerHTML = '<span class="dot"></span> Backend not responding';
    });
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def homepage():
    return PAGE.replace("__APP_NAME__", APP_NAME)
