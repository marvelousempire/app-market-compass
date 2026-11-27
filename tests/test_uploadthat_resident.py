import copy

import pytest

from market_compass.uploadthat_resident import ImportUnavailable, read_imports, verified_projection

OP = '22222222-2222-4222-8222-222222222222'


def artifact():
    return {'job': {'id': 'review', 'name': 'Synthetic history', 'sourceApp': 'market-compass-studio',
                    'stage': 'settled', 'sha256': 'a' * 64, 'sheetDigest': 'b' * 64,
                    'sheetReviewedDigest': 'b' * 64, 'profileDigest': 'c' * 64,
                    'profileReviewedDigest': 'c' * 64,
                    'plan': {'destinations': ['bankthat'], 'bank': {'route': 'crypto-history', 'memberId': 'synthetic'}},
                    'receipts': [{'destination': 'bankthat', 'operationId': OP, 'state': 'verified'}]}}


def projection():
    return {'schema': 'bank-reader.domain-operation/v1', 'readback': True,
            'operationId': OP, 'sourceSha256': 'a' * 64, 'sheetDigest': 'b' * 64,
            'memberId': 'synthetic', 'kind': 'crypto-history', 'currency': 'USD',
            'rows': [{'values': {'wallet_id': 'test-wallet', 'date': '2099-01-02',
                                 'token_symbol': 'TEST', 'quantity': '0.00000001'}}],
            'records': [{'id': 'test-record', 'wallet_id': 'test-wallet', 'member_id': 'synthetic'}]}


def scopes():
    return [{'id': 'test-wallet', 'name': 'Synthetic wallet', 'exchange_name': 'Synthetic broker',
             'address': 'Private field must not cross into the receiving view'}]


def test_read_requires_family_session_before_any_owner_call():
    calls = []
    with pytest.raises(PermissionError):
        read_imports('', lambda *args: calls.append(args))
    assert not calls


def test_reads_each_owner_and_binds_receipt_without_financial_effects():
    calls = []
    def reader(owner, path, cookie):
        calls.append((owner, path, cookie))
        return {'artifacts': [artifact()]} if owner == 'upload' else scopes() if path.endswith('/wallets') else projection()
    result = read_imports('unrelated=private; nephew_session=synthetic', reader)
    assert result['imports'][0]['state'] == 'verified'
    assert [c[0] for c in calls] == ['upload', 'bank', 'bank']
    assert calls[1][1] == '/api/bank-reader/uploadthat/domain/operations/' + OP
    assert calls[2][1] == '/api/avery-reader/crypto/wallets'
    assert all(c[2] == 'nephew_session=synthetic' for c in calls)
    assert result['imports'][0]['operation']['rows'][0]['values']['quantity'] == '0.00000001'
    assert 'address' not in result['imports'][0]['scopes'][0]


@pytest.mark.parametrize('key,value', [('sourceApp', 'another-app'), ('stage', 'confirmation'),
                                    ('sheetReviewedDigest', 'changed'), ('profileReviewedDigest', None)])
def test_stale_or_foreign_handoff_refuses_before_bank_read(key, value):
    a = artifact(); a['job'][key] = value; calls = []
    with pytest.raises(ImportUnavailable):
        verified_projection(a, 'nephew_session=synthetic', lambda *args: calls.append(args))
    assert not calls


@pytest.mark.parametrize('key,value', [('sourceSha256', 'd' * 64), ('memberId', 'foreign'),
                                    ('readback', False), ('sheetDigest', 'changed'),
                                    ('kind', 'contacts'), ('records', []), ('rows', [])])
def test_mismatched_owner_readback_never_becomes_a_verified_import(key, value):
    p = copy.deepcopy(projection()); p[key] = value
    with pytest.raises(ImportUnavailable):
        verified_projection(artifact(), 'nephew_session=synthetic', lambda *args: p)


def test_unavailable_owner_does_not_report_empty_storage():
    with pytest.raises(ImportUnavailable):
        read_imports('nephew_session=synthetic', lambda *args: {'error': 'unavailable'})


def test_missing_or_duplicate_scope_refuses_without_inventing_broker_labels():
    for labels in [[], scopes() + scopes(), {'error': 'unavailable'}]:
        def reader(owner, path, cookie, labels=labels):
            return labels if path.endswith('/wallets') else projection()
        with pytest.raises(ImportUnavailable):
            verified_projection(artifact(), 'nephew_session=synthetic', reader)


def test_owner_or_account_rebinding_in_records_refuses_before_label_read():
    for key, value in [('member_id', 'foreign'), ('wallet_id', 'another-wallet')]:
        p = projection(); p['records'][0][key] = value; calls = []
        with pytest.raises(ImportUnavailable):
            verified_projection(artifact(), 'nephew_session=synthetic', lambda *args, calls=calls, p=p: calls.append(args) or p)
        assert len(calls) == 1


def test_received_bank_presenter_is_exact_and_served_by_the_actual_app():
    import hashlib
    import json
    from importlib.resources import files

    from fastapi.testclient import TestClient

    from market_compass.api import app
    root = files('market_compass').joinpath('web/vendor/bank-reader')
    binding = json.loads(root.joinpath('source.json').read_text())
    source = root.joinpath('market-compass-projection.mjs').read_bytes()
    assert binding['owner'] == 'averygoodman/bank-reader'
    assert binding['revision'] == 'a9f0fa8c06c5012650b9f1615933ed7c236c1f54'
    assert hashlib.sha256(source).hexdigest() == binding['sha256']
    response = TestClient(app).get('/static/vendor/bank-reader/market-compass-projection.mjs')
    assert response.status_code == 200
    assert response.content == source


def test_bank_reader_is_pinned_to_settlement_owner_without_mac_fallback(monkeypatch):
    import market_compass.uploadthat_resident as resident
    calls = []

    def unavailable(path, cookie):
        calls.append((path, cookie))
        raise OSError('owner link unavailable')

    monkeypatch.setattr(resident, 'read_bank_owner', unavailable)
    monkeypatch.setattr(resident, 'build_opener', lambda *args: pytest.fail('Wrong owner fallback'))
    with pytest.raises(ImportUnavailable):
        resident.owner_read('bank', '/api/avery-reader/accounts', 'nephew_session=synthetic')
    assert calls == [('/api/avery-reader/accounts', 'nephew_session=synthetic')]


def test_actual_upload_entrance_uses_registered_source_and_retains_research():
    from html.parser import HTMLParser
    from importlib.resources import files

    class Links(HTMLParser):
        entry = None
        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            if tag == 'a' and values.get('data-node-id') == 'uploadthat.receive':
                self.entry = values

    parser = Links()
    parser.feed(files('market_compass').joinpath('web/index.html').read_text())
    assert parser.entry['href'] == 'https://uploadthat.localhost/?source=market-compass'
    assert parser.entry['target'] == '_blank'
    assert parser.entry['rel'] == 'noopener'


def test_browser_connection_refusal_and_recovery():
    import shutil
    import subprocess
    from pathlib import Path

    node = shutil.which('node')
    if node is None:
        pytest.skip('Node is required for the browser module behavior test.')
    subprocess.run([node, '--test', str(Path(__file__).with_name('uploadthat-browser.test.mjs'))],
                   check=True, capture_output=True, text=True)
