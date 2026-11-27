"""Read confirmed financial imports from their existing owners; no financial effects."""
import http.cookies
import json
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
from uuid import UUID

from .bank_owner_reader import read_bank_owner


class ImportUnavailable(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def family_cookie(raw):
    if not raw or len(raw) > 16384 or any(c in raw for c in '\r\n'):
        raise PermissionError('Sign in with Family to read reviewed imports.')
    jar = http.cookies.SimpleCookie()
    try:
        jar.load(raw)
    except http.cookies.CookieError:
        raise PermissionError('Reconnect with Family.') from None
    token = jar.get('nephew_session')
    if not token or not token.value or any(c in token.value for c in '\r\n;'):
        raise PermissionError('Reconnect with Family.')
    return 'nephew_session=' + token.value


def owner_read(owner, path, cookie):
    try:
        if owner == 'bank':
            status, content_type, raw = read_bank_owner(path, cookie)
            if status in (401, 403):
                raise PermissionError('Reconnect with Family to read your imports.')
            if status != 200 or content_type != 'application/json' or len(raw) > 8_000_000:
                raise ValueError()
            return json.loads(raw)
        if owner != 'upload':
            raise ValueError()
        request = Request('http://search.localhost' + path,
                          headers={'Cookie': cookie, 'Accept': 'application/json'})
        with build_opener(ProxyHandler({}), NoRedirect()).open(request, timeout=30) as response:
            raw = response.read(8_000_001)
            if len(raw) > 8_000_000 or response.headers.get_content_type() != 'application/json':
                raise ValueError()
            return json.loads(raw)
    except HTTPError as error:
        if error.code in (401, 403):
            raise PermissionError('Reconnect with Family to read your imports.') from None
        raise ImportUnavailable('The import owner needs attention. No write was requested.') from None
    except PermissionError:
        raise
    except (OSError, ValueError):
        raise ImportUnavailable('The import owner is unavailable. Saved work is retained.') from None


def verified_projection(artifact, cookie, reader=owner_read):
    job = artifact['job']
    if (job.get('sourceApp') not in ('market-compass-studio', 'market-compass')
            or job.get('stage') not in ('settled', 'partial')
            or not job.get('profileDigest')
            or job.get('sheetReviewedDigest') != job.get('sheetDigest')
            or job.get('profileReviewedDigest') != job['profileDigest']):
        raise ImportUnavailable('Complete this import’s current sheet, profile and settlement first.')
    plan = job.get('plan', {})
    route = plan.get('bank', {}).get('route')
    if route not in ('trading-history', 'crypto-history') or 'bankthat' not in plan.get('destinations', []):
        raise ImportUnavailable('Choose a confirmed Bank-owned financial-history import.')
    receipts = [r for r in job.get('receipts', []) if r.get('destination') == 'bankthat']
    if len(receipts) != 1 or receipts[0].get('state') != 'verified':
        raise ImportUnavailable('This financial operation still needs owner verification.')
    operation = receipts[0].get('operationId')
    try:
        if str(UUID(operation)) != operation:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ImportUnavailable('The saved operation needs owner attention.') from None
    operation_record = reader('bank', '/api/bank-reader/uploadthat/domain/operations/' + operation, cookie)
    if (not isinstance(operation_record, dict) or operation_record.get('schema') != 'bank-reader.domain-operation/v1'
            or operation_record.get('readback') is not True
            or operation_record.get('operationId') != operation
            or operation_record.get('sourceSha256') != job.get('sha256')
            or operation_record.get('sheetDigest') != job.get('sheetDigest')
            or operation_record.get('memberId') != plan['bank'].get('memberId')
            or operation_record.get('kind') != route):
        raise ImportUnavailable('The owner’s readback differs from the confirmed upload.')
    rows, records = operation_record.get('rows'), operation_record.get('records')
    if (not isinstance(rows, list) or not isinstance(records, list) or not rows
            or len(rows) != len(records) or len(rows) > 5000):
        raise ImportUnavailable('The financial-history operation is incomplete.')
    scope_key = 'account_id' if route == 'trading-history' else 'wallet_id'
    ids = set()
    for row, record in zip(rows, records, strict=True):
        values = row.get('values') if isinstance(row, dict) else None
        if (not isinstance(values, dict) or not isinstance(record, dict)
                or not isinstance(values.get(scope_key), str)
                or not values[scope_key] or record.get(scope_key) != values[scope_key]
                or record.get('member_id') != operation_record['memberId']):
            raise ImportUnavailable('The financial-history source scope differs from its owner.')
        ids.add(values[scope_key])
    scopes = reader('bank', '/api/avery-reader/accounts' if route == 'trading-history'
                    else '/api/avery-reader/crypto/wallets', cookie)
    if not isinstance(scopes, list):
        raise ImportUnavailable('The financial account labels could not be read.')
    labels = []
    for ident in ids:
        matches = [scope for scope in scopes if isinstance(scope, dict) and scope.get('id') == ident]
        if len(matches) != 1:
            raise ImportUnavailable('The source account needs owner attention.')
        scope = matches[0]
        labels.append({'id': ident, 'name': scope.get('name') or ident,
                       'institution': scope.get('institution') if route == 'trading-history' else None,
                       'platform': scope.get('exchange_name') if route == 'crypto-history' else None})
    return {'reviewId': job['id'], 'name': job['name'], 'profileDigest': job['profileDigest'],
            'state': 'verified', 'operation': operation_record, 'scopes': labels}



def read_imports(raw_cookie, reader=owner_read):
    cookie = family_cookie(raw_cookie)
    value = reader('upload', '/api/ingest/uploadthat/staged', cookie)
    artifacts = value.get('artifacts') if isinstance(value, dict) else None
    if not isinstance(artifacts, list):
        raise ImportUnavailable('The saved upload list could not be read.')
    candidates = [a for a in artifacts if isinstance(a, dict) and isinstance(a.get('job'), dict)
                  and a['job'].get('sourceApp') in ('market-compass-studio', 'market-compass')]
    results = []
    for artifact in candidates[:5]:
        try:
            results.append(verified_projection(artifact, cookie, reader))
        except ImportUnavailable as error:
            results.append({'reviewId': artifact['job'].get('id'),
                            'name': artifact['job'].get('name'), 'state': 'needs-attention',
                            'message': str(error)})
    return {'schema': 'market-compass.uploadthat-imports/v1', 'readOnly': True,
            'recentLimit': 5, 'imports': results}
