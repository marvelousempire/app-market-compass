from fastapi.testclient import TestClient

from market_compass import api


client = TestClient(api.app)
REV = "a" * 40


def test_symbol_reader_serves_only_current_core_cohort(monkeypatch):
    requested = []

    def read(path):
        requested.append(path)
        if path.endswith("manifest.json"):
            return ('{"revision":"' + REV + '"}').encode()
        return b'export const SYMBOL_CORE_REVISION="' + REV.encode() + b'";'

    monkeypatch.setattr(api, "_symbol_owner_read", read)
    manifest = client.get("/api/ui-symbols/manifest")
    assert manifest.status_code == 200
    assert manifest.json() == {"revision": REV}
    assert manifest.headers["cache-control"] == "no-store"

    module = client.get(f"/api/ui-symbols/r/{REV}/symbols.mjs")
    assert module.status_code == 200
    assert module.headers["content-type"].startswith("text/javascript")
    assert requested[-1] == f"/core/v1/r/{REV}/symbols.mjs"

    assert client.get("/api/ui-symbols/r/not-a-revision/symbols.mjs").status_code == 404
    assert client.get(f"/api/ui-symbols/r/{'b' * 40}/symbols.mjs").status_code == 409


def test_symbol_reader_refuses_bad_manifest(monkeypatch):
    monkeypatch.setattr(api, "_symbol_owner_read", lambda _: b'{"revision":"bad"}')
    assert client.get("/api/ui-symbols/manifest").status_code == 503
