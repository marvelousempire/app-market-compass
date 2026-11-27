import json
from types import SimpleNamespace

import pytest

from market_compass import bank_owner_reader as bank
from market_compass import uploadthat_resident as resident


@pytest.mark.parametrize('path', [
    '/api/avery-reader/accounts?owner=other', '/api/bank-reader/accounts',
    '/api/avery-reader/accounts/delete', 'https://another-owner/accounts',
])
def test_unknown_or_write_scope_refuses_before_owner_loading(monkeypatch, path):
    monkeypatch.setattr(bank, '_load_owner', lambda: pytest.fail('Owner must stay untouched'))
    with pytest.raises(ValueError):
        bank.read_bank_owner(path, 'nephew_session=synthetic')


def test_changed_installed_transport_refuses_before_import(monkeypatch, tmp_path):
    monkeypatch.setattr(bank.Path, 'home', lambda: tmp_path)
    path = (tmp_path / '.local/share/tablethat-owner-links/releases'
            / bank.OWNER_REVISION / 'source/scripts/owner-links.py')
    path.parent.mkdir(parents=True)
    path.write_text('raise RuntimeError("changed source must never run")')
    monkeypatch.setattr(bank, '_module', lambda *args: pytest.fail('Changed source imported'))
    with pytest.raises(ValueError):
        bank._load_owner()


def test_request_uses_fixed_stream_get_and_preserves_person_auth(monkeypatch):
    captured = []

    def relay(sock, command):
        request = b''
        while b'\r\n\r\n' not in request:
            request += sock.recv(4096)
        captured.append((command, request.decode()))
        payload = b'{"readback":true}'
        sock.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                     + b'Content-Length: ' + str(len(payload)).encode()
                     + b'\r\nConnection: close\r\n\r\n' + payload)

    def command(config, route):
        assert config == {'qualified': True} and route == 'bank'
        return ['existing-owner', 'tablethat-bank']

    owner = SimpleNamespace(ssh_command=command)
    monkeypatch.setattr(bank, '_load_owner', lambda: (
        owner, {'qualified': True}, SimpleNamespace(relay=relay)))
    status, content_type, raw = bank.read_bank_owner(
        '/api/avery-reader/accounts', 'nephew_session=synthetic')
    assert (status, content_type, json.loads(raw)) == (200, 'application/json', {'readback': True})
    assert len(captured) == 1
    assert captured[0][0] == ['existing-owner', 'tablethat-bank']
    assert captured[0][1].startswith('GET /api/avery-reader/accounts HTTP/1.1\r\n')
    assert 'Cookie: nephew_session=synthetic\r\n' in captured[0][1]
    assert 'Connection: close\r\n' in captured[0][1]


def test_bank_auth_refusal_remains_a_family_connection_error(monkeypatch):
    monkeypatch.setattr(resident, 'read_bank_owner', lambda *args: (
        401, 'text/plain', b'Unauthorized'))
    with pytest.raises(PermissionError):
        resident.owner_read('bank', '/api/avery-reader/accounts', 'nephew_session=synthetic')


def test_upload_person_session_never_uses_environment_http_proxy(monkeypatch):
    seen = []

    class Response:
        headers = SimpleNamespace(get_content_type=lambda: 'application/json')
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return None
        def read(self, limit):
            return b'{"artifacts":[]}'

    class Opener:
        def open(self, request, **kwargs):
            assert request.full_url == 'http://search.localhost/api/ingest/uploadthat/staged'
            return Response()

    def opener(*handlers):
        seen.extend(handlers)
        return Opener()

    monkeypatch.setenv('http_proxy', 'http://unrelated-proxy.invalid:8080')
    monkeypatch.setattr(resident, 'build_opener', opener)
    assert resident.owner_read('upload', '/api/ingest/uploadthat/staged',
                               'nephew_session=synthetic') == {'artifacts': []}
    assert any(isinstance(handler, resident.ProxyHandler) and handler.proxies == {}
               for handler in seen)
