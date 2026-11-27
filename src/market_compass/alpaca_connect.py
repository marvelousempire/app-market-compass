"""Local Alpaca Connect market-data authorization. No trading endpoints are used."""
from __future__ import annotations

import json
import secrets
import subprocess
import time
from threading import Lock
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CALLBACK = "http://market-compass.localhost/api/alpaca-connect/callback"
SERVICE = "app.market-compass.alpaca-connect"
_pending: dict[str, float] = {}
_lock = Lock()


def _read(account: str) -> str:
    result = subprocess.run(["security", "find-generic-password", "-s", SERVICE, "-a", account, "-w"],
                            capture_output=True, text=True, check=False, timeout=5)
    return result.stdout.strip() if result.returncode == 0 else ""


def _save(account: str, value: str) -> None:
    # -w last reads from stdin; the secret never appears in process arguments.
    result = subprocess.run(["security", "add-generic-password", "-s", SERVICE, "-a", account,
                             "-U", "-w"], input=value + "\n" + value + "\n", capture_output=True,
                            text=True, check=False, timeout=10)
    if result.returncode:
        raise RuntimeError("The Mac could not save the Alpaca connection in Keychain.")


def _delete(account: str) -> None:
    subprocess.run(["security", "delete-generic-password", "-s", SERVICE, "-a", account],
                   capture_output=True, text=True, check=False, timeout=5)


def status() -> dict:
    configured = bool(_read("client-id") and _read("client-secret"))
    connected = bool(_read("data-token"))
    return {"configured": configured, "connected": connected,
            "scope": "market data only", "account": "paper", "callback": CALLBACK}


def configure(client_id: str, client_secret: str) -> dict:
    client_id, client_secret = client_id.strip(), client_secret.strip()
    if not 8 <= len(client_id) <= 256 or not 8 <= len(client_secret) <= 512:
        raise ValueError("Enter the Alpaca Connect Client ID and Client Secret, not Paper Trading API keys.")
    if any(c.isspace() for c in client_id + client_secret):
        raise ValueError("The Alpaca Connect credentials cannot contain spaces.")
    if _read("client-id") != client_id:
        _delete("data-token")
    _save("client-id", client_id)
    _save("client-secret", client_secret)
    return status()


def authorization_url() -> str:
    client_id = _read("client-id")
    if not client_id or not _read("client-secret"):
        raise ValueError("Add your Alpaca Connect app credentials first.")
    state = secrets.token_urlsafe(32)
    with _lock:
        _pending.clear()
        _pending[state] = time.monotonic() + 600
    return "https://app.alpaca.markets/oauth/authorize?" + urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": CALLBACK,
        "state": state, "scope": "data", "env": "paper"})


def exchange(code: str, state: str) -> None:
    with _lock:
        expiry = _pending.pop(state, 0)
    if not expiry or time.monotonic() > expiry:
        raise ValueError("The Alpaca sign-in expired. Start again in Market Compass Settings.")
    body = urlencode({"grant_type": "authorization_code", "code": code,
                      "client_id": _read("client-id"), "client_secret": _read("client-secret"),
                      "redirect_uri": CALLBACK}).encode()
    request = Request("https://api.alpaca.markets/oauth/token", data=body,
                      headers={"Content-Type": "application/x-www-form-urlencoded",
                               "Accept": "application/json"}, method="POST")
    with urlopen(request, timeout=10) as response:
        payload = json.load(response)
    scopes = set(str(payload.get("scope", "")).split())
    token = payload.get("access_token")
    if payload.get("token_type", "").lower() != "bearer" or not isinstance(token, str) or not token:
        raise ValueError("Alpaca did not return a usable data connection.")
    if "data" not in scopes or scopes.intersection({"trading", "account:write"}):
        raise ValueError("Alpaca returned permissions beyond market data. Nothing was connected.")
    _save("data-token", token)


def data_token() -> str:
    return _read("data-token")
