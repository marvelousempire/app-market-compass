import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import test from 'node:test';

const source = readFileSync(new URL('../src/market_compass/web/market-data-settings.js', import.meta.url), 'utf8');

function mount(configureOk) {
  const classes = new Set();
  const connection = {dataset: {}, textContent: '', offsetWidth: 1,
    classList: {add: name => classes.add(name), remove: name => classes.delete(name)}};
  const button = {disabled: false};
  const form = {elements: {client_id: {value: 'client123'}, client_secret: {value: 'secret123'}},
    querySelector: () => button, addEventListener: (name, handler) => { form[name] = handler; },
    reset: () => { form.elements.client_id.value = ''; form.elements.client_secret.value = ''; }};
  const start = {disabled: true, addEventListener() {}};
  const output = {textContent: ''};
  const ids = {'market-data-current': output, 'alpaca-connect-status': connection,
    'alpaca-connect-form': form, 'alpaca-connect-start': start};
  let configured = false;
  const fetch = async url => {
    if (url === '/api/alpaca-connect/status') return {ok: true, json: async () => ({configured, connected: false})};
    if (url === '/api/alpaca-connect/configure') {
      if (!configureOk) return {ok: false, json: async () => ({detail: 'Keychain did not confirm the save.'})};
      configured = true;
      return {ok: true, json: async () => ({configured: true})};
    }
    return {ok: false};
  };
  runInNewContext(source, {document: {getElementById: id => ids[id] || null}, fetch,
    window: {location: {search: ''}, dispatchEvent() {}}, URLSearchParams, CustomEvent: class {}});
  return {form, button, connection, classes, start};
}

test('confirmed Keychain readback plays success and clears the fields', async () => {
  const {form, button, connection, classes, start} = mount(true);
  await form.submit({preventDefault() {}});
  assert.equal(connection.dataset.saveState, 'saved');
  assert.match(connection.textContent, /saved on this Mac/);
  assert.match(connection.textContent, /Finish your app registration in Alpaca/);
  assert.equal(classes.has('just-saved'), true);
  assert.equal(form.elements.client_secret.value, '');
  assert.equal(start.disabled, false);
  assert.equal(button.disabled, false);
});

test('failed save keeps entries and never plays success', async () => {
  const {form, button, connection, classes} = mount(false);
  await form.submit({preventDefault() {}});
  assert.equal(connection.dataset.saveState, 'error');
  assert.equal(connection.textContent, 'Keychain did not confirm the save.');
  assert.equal(classes.has('just-saved'), false);
  assert.equal(form.elements.client_secret.value, 'secret123');
  assert.equal(button.disabled, false);
});
