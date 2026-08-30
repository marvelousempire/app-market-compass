from __future__ import annotations

import json
import socket
import threading
import time
import webbrowser
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn

HOST = "127.0.0.1"
DEFAULT_PORT = 8000
MAX_PORT_SCAN = 25
EXPECTED_SURFACE = "application-v0.5"


def _health(port: int) -> dict | None:
    try:
        with urlopen(f"http://{HOST}:{port}/health", timeout=0.4) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, ValueError, json.JSONDecodeError):
        return None


def _is_market_compass(port: int) -> bool:
    health = _health(port)
    return bool(
        health
        and health.get("status") == "ok"
        and health.get("surface") == EXPECTED_SURFACE
    )


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((HOST, port))
            return True
        except OSError:
            return False


def select_port(start: int = DEFAULT_PORT) -> tuple[int, bool]:
    """Return (port, reuse_existing_market_compass).

    Reuse any matching current surface in the scan range first. Only then bind
    the first free port. Checking only the default port used to spawn a second
    desk (and leave the promised URL dead) whenever 8000 was an older process.
    """
    for port in range(start, start + MAX_PORT_SCAN):
        if _is_market_compass(port):
            return port, True
    for port in range(start, start + MAX_PORT_SCAN):
        if _port_is_free(port):
            return port, False
    raise RuntimeError(f"No free local port found between {start} and {start + MAX_PORT_SCAN - 1}")


def _open_when_ready(port: int) -> None:
    url = f"http://{HOST}:{port}"
    for _ in range(120):
        if _is_market_compass(port):
            webbrowser.open(url)
            return
        time.sleep(0.1)


def main() -> None:
    port, reuse_existing = select_port()
    url = f"http://{HOST}:{port}"

    if reuse_existing:
        print(f"Market Compass is already running at {url}. Opening it in your browser.")
        webbrowser.open(url)
        return

    if port != DEFAULT_PORT:
        print(f"Port {DEFAULT_PORT} is in use. Starting Market Compass at {url} instead.")
    else:
        print(f"Starting Market Compass at {url}.")

    threading.Thread(target=_open_when_ready, args=(port,), daemon=True).start()
    uvicorn.run("market_compass.api:app", host=HOST, port=port)


if __name__ == "__main__":
    main()
