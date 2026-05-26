#!/usr/bin/env python3
"""Smoke-test demo pages over a local HTTP server.

The test checks that every demo page and its referenced JS/CSS assets are
served successfully. If Chrome is available, it also writes screenshots and
checks that they are non-empty.
"""

import argparse
import http.server
import json
import shutil
import socketserver
import subprocess
import threading
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "analysis" / "outputs" / "demo_screenshots"
PAGES = [
    "/demos/risk_dashboard_demo/",
    "/demos/employee_app_demo/",
    "/demos/noticer_local_guarded_demo/",
    "/demos/bench_playground/",
]
ASSETS = [
    "/presence-sdk-js/src/presence-guard.js",
    "/presence-policy/presence.guard.policy.json",
    "/demos/shared.css",
    "/demos/bench_playground/main.js",
    "/demos/bench_playground/profiles.js",
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


def fetch(base_url, path):
    with urllib.request.urlopen(base_url + path, timeout=10) as response:
        body = response.read()
        return {"path": path, "status": response.status, "bytes": len(body)}


def find_chrome():
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("chrome"),
        shutil.which("chromium"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def screenshot(chrome, base_url, path):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    name = path.strip("/").replace("/", "_") or "root"
    output = OUTPUT / f"{name}.png"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1280,900",
            "--virtual-time-budget=2000",
            f"--screenshot={output}",
            base_url + path,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return {"path": path, "screenshot": str(output), "bytes": output.stat().st_size}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8030)
    parser.add_argument("--screenshots", action="store_true")
    args = parser.parse_args(argv)

    handler = lambda *handler_args, **handler_kwargs: QuietHandler(*handler_args, directory=str(ROOT), **handler_kwargs)
    server = socketserver.TCPServer(("127.0.0.1", args.port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)

    base_url = f"http://127.0.0.1:{args.port}"
    try:
        rows = [fetch(base_url, path) for path in PAGES + ASSETS]
        shots = []
        if args.screenshots:
          chrome = find_chrome()
          if chrome:
              shots = [screenshot(chrome, base_url, path) for path in PAGES]
        result = {
            "passed": all(row["status"] == 200 and row["bytes"] > 0 for row in rows)
            and all(item["bytes"] > 5000 for item in shots),
            "http": rows,
            "screenshots": shots,
        }
    finally:
        server.shutdown()
        server.server_close()

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
