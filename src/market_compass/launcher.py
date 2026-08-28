from __future__ import annotations

import socket
import threading
import time
import webbrowser

import uvicorn

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"


def _open_when_ready() -> None:
    for _ in range(100):
        try:
            with socket.create_connection((HOST, PORT), timeout=0.1):
                webbrowser.open(URL)
                return
        except OSError:
            time.sleep(0.1)


def main() -> None:
    threading.Thread(target=_open_when_ready, daemon=True).start()
    uvicorn.run("market_compass.api:app", host=HOST, port=PORT)


if __name__ == "__main__":
    main()
