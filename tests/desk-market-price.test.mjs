import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const source = readFileSync(new URL('../src/market_compass/web/desk-market-price.js', import.meta.url), 'utf8');
function mount() {
  const listeners = {}, published = [], requests = [];
  const host = {prepend(node) { this.current = node; }};
  const document = {getElementById: id => id === 'identity-strip' ? host : null,
    createElement: () => ({children: [], setAttribute() {}, append(node) { this.children.push(node); }})};
  runInNewContext(source, {document, Date, Number, encodeURIComponent,
    CustomEvent: class {constructor(type, options) {this.type = type; this.detail = options.detail;}},
    window: {addEventListener: (name, fn) => listeners[name] = fn, dispatchEvent: event => published.push(event.detail)},
    fetch: url => new Promise(resolve => requests.push({url, resolve}))});
  return {host, published, requests, report: symbol => listeners.marketcompassreport({detail:{report:{symbol}}})};
}
const quote = (symbol, price) => ({state:'observed',symbol,price,as_of:new Date().toISOString(),source:'Alpaca',feed:'IEX',real_time:true});
const finish = async (request, value) => {request.resolve({ok:true,json:async()=>value}); await new Promise(resolve => setImmediate(resolve));};
test('selected symbol gets dated actual price and provenance', async () => {
  const app = mount(); app.report('BB');
  await finish(app.requests[0], quote('BB',9.06));
  assert.equal(app.published.at(-1).observation.price,9.06);
  assert.match(app.host.current.children[1].textContent,/Alpaca IEX/);
});
test('late response for previous symbol cannot overwrite new selection', async () => {
  const app = mount(); app.report('BB'); app.report('AAPL');
  await finish(app.requests[1],quote('AAPL',358.68));
  await finish(app.requests[0],quote('BB',9.06));
  assert.equal(app.published.at(-1).symbol,'AAPL');
  assert.equal(app.published.at(-1).observation.price,358.68);
});
test('invalid or mismatched observations never become scenario inputs', async () => {
  for (const value of [quote('QQQ',9),quote('BB',-1),{...quote('BB',9),as_of:'invalid'}, {...quote('BB',9),state:'held'}]) {
    const app = mount(); app.report('BB'); await finish(app.requests[0],value);
    assert.equal(app.published.at(-1).observation,null);
    assert.match(app.host.current.children[0].textContent,/unavailable/);
  }
});
