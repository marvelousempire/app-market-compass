import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';

const presenter = new URL('../src/market_compass/web/vendor/bank-reader/market-compass-projection.mjs', import.meta.url);
const source = readFileSync(new URL('../src/market_compass/web/uploadthat-resident.js', import.meta.url), 'utf8')
  .replace("'/static/vendor/bank-reader/market-compass-projection.mjs'", JSON.stringify(presenter.href));

class Element {
  children = [];
  textContent = '';
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(name, value) { this[name] = value; }
  addEventListener(name, handler) { this[name] = handler; }
  set innerHTML(_) { throw Error('Imported values must stay text, not markup'); }
}

test('Family connection recovery retains research and never navigates the caller', async () => {
  const button = new Element(), output = new Element();
  const research = Object.freeze({player: 'AAPL', horizon: 37});
  const calls = [];
  globalThis.location = Object.freeze({protocol: 'https:', hostname: 'market-compass.localhost'});
  globalThis.document = {
    getElementById: id => id === 'load-reviewed-imports' ? button : id === 'reviewed-imports' ? output : research,
    createElement: tag => Object.assign(new Element(), {tag}),
  };
  globalThis.fetch = async (...args) => {
    calls.push(args);
    return {status: 401, ok: false, json: async () => ({detail: 'Connect with Family'})};
  };
  await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
  await button.click();
  assert.equal(button.disabled, false);
  assert.equal(output.children[1].textContent, 'Connect with Family');
  assert.equal(output.children[1].href, 'https://market-compass.localhost/signin?return=%2F');
  assert.equal(output.children[1].target, '_blank');
  assert.equal(output.children[1].rel, 'noopener');
  assert.equal(research.player, 'AAPL');
  assert.equal(research.horizon, 37);
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], '/api/uploadthat/imports');
  assert.equal(calls[0][1].credentials, 'same-origin');
  assert.equal(calls[0][1].cache, 'no-store');
  assert.equal(calls[0][1].method, undefined); // native fetch default GET

  globalThis.fetch = async () => ({status: 200, ok: true, json: async () => ({imports: []})});
  await button.click();
  assert.equal(button.disabled, false);
  assert.equal(output.children.length, 1);
  assert.equal(output.children[0].textContent, 'No recent Market Compass uploads were returned.');
  assert.equal(research.player, 'AAPL');

  const account = 'synthetic-account', member = 'synthetic-member';
  const rows = Array.from({length: 101}, (_, index) => ({values: {
    account_id: account, date: '2026-01-02', symbol: 'SYNTH', transaction_type: 'buy', quantity: '0.00000001',
  }}));
  const operation = {schema: 'bank-reader.domain-operation/v1', readback: true, kind: 'trading-history',
    memberId: member, rows, records: rows.map((_, index) => ({id: `record-${index}`, member_id: member, account_id: account}))};
  let reads = 0;
  globalThis.fetch = async () => {
    reads++;
    return {status: 200, ok: true, json: async () => ({imports: [{state: 'verified',
      name: '<img onerror=unsafe> synthetic history', reviewId: '22222222-2222-4222-8222-222222222222',
      operation, scopes: [{id: account, name: 'Synthetic account', institution: 'Synthetic broker'}]}]})};
  };
  await button.click();
  const section = output.children[0], group = section.children.at(-1);
  const table = group.children[2].children[0], body = table.children[1];
  const paging = group.children[3], [previous, next] = group.children[4].children;
  assert.equal(section.children[0].textContent, '<img onerror=unsafe> synthetic history');
  assert.equal(section.children[1].href, 'https://uploadthat.localhost/?source=market-compass#22222222-2222-4222-8222-222222222222');
  assert.equal(body.children.length, 100);
  assert.equal(previous.disabled, true);
  assert.equal(next.disabled, false);
  next.onclick();
  assert.equal(body.children.length, 1);
  assert.equal(body.children[0].children[3].textContent, '0.00000001');
  assert.equal(paging.textContent, 'Records 101–101 of 101');
  assert.equal(next.disabled, true);
  previous.onclick();
  assert.equal(body.children.length, 100);
  assert.equal(previous.disabled, true);
  assert.equal(reads, 1);
  assert.equal(research.player, 'AAPL');
});
