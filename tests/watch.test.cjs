const test = require('node:test');
const assert = require('node:assert/strict');
const { initialize } = require('../js/watch.js');

class Node {
  constructor(tag = '') { this.tag = tag; this.attrs = {}; this.handlers = {}; this.children = []; this.hidden = false; this.textContent = ''; }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return this.attrs[name] || null; }
  addEventListener(type, fn) { (this.handlers[type] ||= []).push(fn); }
  emit(type) { (this.handlers[type] || []).forEach(fn => fn()); }
  replaceChildren(...nodes) { this.children = nodes; }
}
function fixture(channel = 'UC75FUMm1TckzTRpfYHd_ILQ') {
  const root = new Node();
  const button = new Node('button'); button.hidden = true;
  const mount = new Node('div'); mount.hidden = true;
  const status = new Node('p');
  const fallback = new Node('a'); fallback.href = 'https://www.youtube.com/channel/' + channel + '/live';
  const nodes = { '[data-watch-load]': button, '[data-watch-mount]': mount, '[data-watch-status]': status };
  root.querySelector = selector => nodes[selector] || null;
  root.ownerDocument = { createElement: tag => new Node(tag) };
  root.setAttribute('data-watch-channel', channel);
  const pending = new Map(); let serial = 0;
  const timers = {
    setTimeout(fn) { const id = ++serial; pending.set(id, fn); return id; },
    clearTimeout(id) { pending.delete(id); },
    run() { const callbacks = [...pending.values()]; pending.clear(); callbacks.forEach(fn => fn()); }
  };
  return { root, button, mount, status, fallback, timers };
}

test('initialization creates no iframe; malformed/missing channel leaves static fallback usable', () => {
  for (const channel of ['UC75FUMm1TckzTRpfYHd_ILQ', '', 'https://example.invalid/track']) {
    const f = fixture(channel);
    assert.equal(initialize(f.root, f.timers), channel === 'UC75FUMm1TckzTRpfYHd_ILQ');
    assert.equal(f.mount.children.length, 0);
    assert.equal(f.button.hidden, channel !== 'UC75FUMm1TckzTRpfYHd_ILQ');
    assert.equal(f.fallback.hidden, false);
  }
});

test('explicit activation creates one non-autoplay iframe, suppresses repeat clicks, and keeps the fallback', () => {
  const f = fixture(); initialize(f.root, f.timers);
  f.button.emit('click');
  const frame = f.mount.children[0];
  const url = new URL(frame.src);
  assert.equal(url.origin, 'https://www.youtube.com');
  assert.equal(url.searchParams.get('channel'), 'UC75FUMm1TckzTRpfYHd_ILQ');
  assert.equal(url.searchParams.get('autoplay'), '0');
  assert.equal(url.searchParams.get('playsinline'), '1');
  assert.ok(frame.title);
  f.button.emit('click');
  assert.deepEqual(f.mount.children, [frame]);
  assert.equal(f.button.getAttribute('aria-disabled'), 'true');
  assert.equal(f.fallback.hidden, false);
});

test('slow load offers retry without claiming offline; old iframe cannot alter a later attempt', () => {
  const f = fixture(); initialize(f.root, f.timers);
  f.button.emit('click');
  const old = f.mount.children[0];
  f.timers.run();
  assert.match(f.status.textContent, /may still be loading/);
  assert.equal(f.button.getAttribute('aria-disabled'), 'false');
  assert.deepEqual(f.mount.children, [old]);
  f.button.emit('click');
  const current = f.mount.children[0];
  assert.notEqual(current, old);
  old.emit('load');
  assert.equal(f.root.getAttribute('data-watch-state'), 'loading');
  assert.equal(f.button.getAttribute('aria-disabled'), 'true');
  current.emit('load');
  assert.equal(f.root.getAttribute('data-watch-state'), 'attempted');
  assert.match(f.status.textContent, /If a service is available/);
  assert.equal(f.button.getAttribute('aria-disabled'), 'false');
});

test('reported frame error restores retry; repeated initialization cannot double-bind the button', () => {
  const f = fixture(); initialize(f.root, f.timers);
  assert.equal(initialize(f.root, f.timers), false);
  assert.equal(f.button.handlers.click.length, 1);
  f.button.emit('click');
  f.mount.children[0].emit('error');
  assert.equal(f.root.getAttribute('data-watch-state'), 'retry');
  assert.equal(f.mount.getAttribute('aria-busy'), 'false');
  assert.equal(f.button.getAttribute('aria-disabled'), 'false');
  assert.equal(f.fallback.hidden, false);
});
