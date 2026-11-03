#!/usr/bin/env python3
"""Dedicated localhost preview. Keeps the original automatic market analysis."""
from __future__ import annotations

import json
import socket
import threading
import time
import webbrowser
from urllib.request import urlopen
from urllib.error import URLError

import uvicorn

HOST = "127.0.0.1"
START_PORT = 18340
MAX_PORTS = 20


def is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((HOST, port))
            return True
        except OSError:
            return False


def select_free_port() -> int:
    for port in range(START_PORT, START_PORT + MAX_PORTS):
        if is_free(port):
            return port
    raise RuntimeError("No free dedicated preview port; stop an old preview and retry.")


def open_when_ready(port: int) -> None:
    # Only open a server that includes the actual HCCK profile catalog.
    base = f"http://{HOST}:{port}"
    for _ in range(120):
        try:
            with urlopen(base + "/api/hcck/profiles", timeout=0.5) as response:
                payload = json.load(response)
            if payload.get("schema") == "market-compass.hybrid-cck-profile-schedule/v1":
                webbrowser.open(base + "/#hcck-profiles")
                return
        except (OSError, URLError, ValueError, TimeoutError):
            pass
        time.sleep(0.1)
    print("Preview did not answer with an HCCK catalog. Check server logs.")


def main() -> None:
    port = select_free_port()
    print(f"Market Compass full preview: http://{HOST}:{port}/#hcck-profiles", flush=True)
    print("Original market auto-analysis remains ON; simulator is additive.", flush=True)
    threading.Thread(target=open_when_ready, args=(port,), daemon=True).start()
    uvicorn.run("market_compass.api:app", host=HOST, port=port, log_level="info")


if __name__ == "__main__":
    main()
