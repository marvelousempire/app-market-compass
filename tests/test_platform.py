import ssl

from market_compass import launcher
from market_compass.data import SSL_CONTEXT


def test_ssl_context_verifies_certificates():
    assert SSL_CONTEXT.check_hostname is True
    assert SSL_CONTEXT.verify_mode == ssl.CERT_REQUIRED


def test_browser_opens_when_server_is_ready(monkeypatch):
    opened = []

    class Connection:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

    monkeypatch.setattr(launcher.socket, "create_connection", lambda *_args, **_kwargs: Connection())
    monkeypatch.setattr(launcher.webbrowser, "open", lambda url: opened.append(url))

    launcher._open_when_ready()

    assert opened == [launcher.URL]
