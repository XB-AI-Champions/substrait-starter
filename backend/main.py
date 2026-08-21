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

APP_NAME = "My First Substrait App"

app = FastAPI(title=APP_NAME, docs_url="/api/docs")


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/api/info")
def info():
    return {
        "app": APP_NAME,
        "server_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


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
    margin: 0;
    min-height: 100vh;
    display: grid;
    place-items: center;
    font: 16px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(180deg, #f4f7fb 0%, #eef2f7 100%);
    color: #172033;
    padding: 32px 24px;
  }
  .layout {
    width: 100%;
    max-width: 640px;
  }
  .hero {
    margin-bottom: 18px;
    text-align: left;
  }
  .eyebrow {
    display: inline-block;
    margin-bottom: 10px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(23, 32, 51, 0.06);
    color: #41506a;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .hero h1 {
    margin: 0;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    line-height: 1.05;
    letter-spacing: -0.04em;
    color: #0f172a;
  }
  .hero p {
    margin: 12px 0 0;
    max-width: 520px;
    color: #526076;
    font-size: 16px;
  }
  .card {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 22px;
    padding: 36px;
    width: 100%;
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(14px);
  }
  .card h2 {
    margin: 0 0 8px;
    font-size: 24px;
    letter-spacing: -0.02em;
    color: #0f172a;
  }
  .card p {
    margin: 0 0 20px;
    color: #5c6779;
  }
  .pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    background: #eef2f7;
    color: #526076;
  }
  .pill.ok { background: #e7f6ec; color: #10682f; }
  .pill.fail { background: #fdecec; color: #9a1f1f; }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
  }
  .next {
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid rgba(148, 163, 184, 0.22);
    font-size: 14px;
    color: #5c6779;
  }
  code {
    background: #eef2f7;
    padding: 2px 6px;
    border-radius: 5px;
    font-size: 13px;
  }
</style>
</head>
<body>
  <div class="layout">
    <section class="hero">
      <span class="eyebrow">Welcome</span>
      <h1>Hello World</h1>
      <p>A clean, modern starting point for your Substrait application.</p>
    </section>

    <main class="card">
      <h2>__APP_NAME__</h2>
      <p>Your app is deployed and running on Substrait.</p>

      <span class="pill" id="status"><span class="dot"></span> Checking the backend…</span>

      <div class="next">
        This page is served by <code>backend/main.py</code>.
        Tell your AI assistant what you want to build and it will edit that file,
        then deploy again to see your changes live.
      </div>
    </main>
  </div>

<script>
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
