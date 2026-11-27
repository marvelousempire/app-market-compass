"""Receive GET responses through the existing qualified TableTHAT Bank stream."""
import hashlib
import http.client
import importlib.util
import logging
import re
import socket
import threading
from pathlib import Path

OWNER_REVISION = '2f9b66f77acf5cf8c0e33a71cdf5fa3a73e55a62'
OWNER_SHA256 = 'b733242c2565cc7d5710571b948d11863ba39b72bdd86bde575bcf418b1ce8e3'
READ_PATH = re.compile(
    r'/api/(?:avery-reader/(?:accounts|crypto/wallets)|bank-reader/uploadthat/domain/operations/'
    r'[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12})\Z'
)


def _module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_owner():
    # Receive the installed owner, not a copy of its keys, relay or route map.
    source = (Path.home() / '.local/share/tablethat-owner-links/releases'
              / OWNER_REVISION / 'source/scripts/owner-links.py')
    if (not source.is_file() or source.is_symlink()
            or hashlib.sha256(source.read_bytes()).hexdigest() != OWNER_SHA256):
        raise ValueError('Qualified Bank transport is unavailable.')
    owner = _module(source, 'market_qualified_table_owner')
    config = owner.checked_config(Path.home() / '.nephew/run/tablethat-owner-links/config.json')
    relay = _module(owner.relay_path(config), 'market_qualified_bank_relay')
    return owner, config, relay


def read_bank_owner(path, cookie):
    if not READ_PATH.fullmatch(path) or not cookie.startswith('nephew_session=') or any(
            c in cookie for c in '\r\n'):
        raise ValueError('Choose a qualified Bank history read.')
    owner, config, relay = _load_owner()
    command = owner.ssh_command(config, 'bank')
    # A request-scoped socket pair receives the existing stream. No TCP listener,
    # service installation, caller command, new credential or identity is created.
    local, remote = socket.socketpair()
    local.settimeout(30)

    def receive():
        try:
            relay.relay(remote, command)
        except (OSError, ValueError):
            pass
        finally:
            remote.close()

    worker = threading.Thread(target=receive, daemon=True)
    worker.start()
    connection = http.client.HTTPConnection('bank.localhost', timeout=30)
    connection.sock = local
    try:
        connection.request('GET', path, headers={
            'Host': 'bank.localhost', 'Accept': 'application/json',
            'Cookie': cookie, 'Connection': 'close',
        })
        response = connection.getresponse()
        raw = response.read(8_000_001)
        logging.getLogger('uvicorn.error').info(
            'Bank owner response: status=%s type=%s encoding=%s bytes=%s',
            response.status, response.headers.get_content_type(),
            response.headers.get('Content-Encoding', 'identity'), len(raw),
        )
        return response.status, response.headers.get_content_type(), raw
    finally:
        connection.close()
        worker.join(2)
