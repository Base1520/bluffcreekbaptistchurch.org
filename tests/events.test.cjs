const test = require('node:test');
const assert = require('node:assert/strict');
const events = require('../js/events.js');

const event = (overrides = {}) => ({when: '2026-09-06', time: '9:00a', title: 'Sunday School', where: 'Fellowship Building', tag: 'Weekly', ...overrides});

test('church date uses Chicago through UTC midnight and winter offset', () => {
  assert.equal(events.churchToday(new Date('2026-09-07T01:00:00Z')), '2026-09-06');
  assert.equal(events.churchToday(new Date('2026-12-07T05:30:00Z')), '2026-12-06');
});

test('real dates and 12-hour time boundaries are validated', () => {
  for (const value of ['2026-02-30', '2026-13-01', '2026-09-31', '0000-01-01', '2026-9-06', '<img>']) assert.equal(events.validDate(value), false, value);
  assert.equal(events.validDate('2028-02-29'), true);
  for (const [value, minutes] of [['12:00a', 0], ['12:00p', 720], ['9 AM', 540], ['6p', 1080], ['10:15a', 615]]) assert.equal(events.startMinutes(value), minutes);
  for (const value of ['00:15a', '9:60a', '13:00p', '9:00', 'noon', 900]) assert.equal(events.startMinutes(value), null);
});

test('expired/invalid entries are removed, dates and same-day times sort correctly', () => {
  const result = events.upcomingEvents([event({time:'6:00p'}), event({when:'2026-09-07'}), event({time:'10:15a'}), event(), event({when:'2026-09-05'}), event({when:'2026-02-30'}), event({time:'99:99a'}), event({tag:'Private'}), event({title:123}), null], '2026-09-06');
  assert.deepEqual(result.map(item => `${item.when} ${item.time}`), ['2026-09-06 9:00a','2026-09-06 10:15a','2026-09-06 6:00p','2026-09-07 9:00a']);
});

// Small DOM adapter for behavior tests: HTML-string sinks deliberately throw.
class Node {
  constructor(tag = '') { this.tag = tag; this.children = []; this.attrs = {}; this.parent = null; this.className = ''; this.textContent = ''; }
  set innerHTML(value) { throw new Error('Calendar must create text nodes, never inject HTML'); }
  appendChild(node) { if (node.tag === 'fragment') node.children.forEach(child => this.appendChild(child)); else { node.parent = this; this.children.push(node); } return node; }
  replaceChildren(...nodes) { this.children = []; nodes.forEach(node => this.appendChild(node)); }
  setAttribute(name, value) { this.attrs[name] = value; }
  getAttribute(name) { return this.attrs[name] ?? null; }
  remove() { this.parent.children = this.parent.children.filter(child => child !== this); }
  matches(selector) { return selector === '.event-row' ? this.className === 'event-row' : selector === 'time[datetime]' ? this.tag === 'time' && 'datetime' in this.attrs : selector === '[data-events-feed]' ? 'data-events-feed' in this.attrs : false; }
  querySelectorAll(selector) { return this.children.flatMap(child => [...(child.matches(selector) ? [child] : []), ...child.querySelectorAll(selector)]); }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
}
class Document extends Node {
  createElement(tag) { return new Node(tag); }
  createTextNode(text) { const node = new Node('text'); node.textContent = text; return node; }
  createDocumentFragment() { return new Node('fragment'); }
}
function fixture(rows) {
  const document = new Document();
  const feed = document.createElement('div'); feed.setAttribute('data-events-feed', '3'); document.appendChild(feed);
  rows.forEach(row => feed.appendChild(events.eventRow(document, row)));
  return {document, feed};
}
const now = new Date('2026-09-07T01:00:00Z'); // Still Sept 6 in Clinton.

test('failed request removes expired build rows while preserving current fallback', async () => {
  const {document, feed} = fixture([event({when:'2026-09-05'}), event()]);
  await events.initialize(document, '/events.json', () => Promise.reject(new Error('offline')), now);
  assert.equal(feed.querySelectorAll('.event-row').length, 1);
  assert.equal(feed.querySelector('time[datetime]').getAttribute('datetime'), '2026-09-06');
});

test('valid empty feed and expired offline fallback both show a weekly schedule link', async () => {
  for (const fetcher of [() => Promise.resolve({ok: true, json: async () => ({events: []})}), () => Promise.reject(new Error('offline'))]) {
    const {document, feed} = fixture([event({when:'2026-09-05'})]);
    await events.initialize(document, '/events.json', fetcher, now);
    assert.equal(feed.querySelectorAll('.event-row').length, 0);
    assert.equal(feed.children[0].className, 'events-empty');
    assert.equal(feed.children[0].children[0].href, 'times.html');
  }
});

test('successful refresh replaces fallback with sorted literal text, including hostile text', async () => {
  const {document, feed} = fixture([event({title:'Build fallback'})]);
  const hostile = '<img src=x onerror="alert(1)">';
  await events.initialize(document, '/events.json', async () => ({ok:true, json: async () => ({events:[event({time:'6:00p'}), event({title:hostile})]})}), now);
  assert.equal(feed.querySelectorAll('.event-row').length, 2);
  assert.equal(feed.children[0].children[1].children[0].textContent, hostile);
  assert.equal(feed.children[0].children[1].children[0].children.length, 0);
  assert.equal(feed.getAttribute('aria-live'), 'polite');
});

test('malformed JSON shape preserves valid build fallback', async () => {
  const {document, feed} = fixture([event({title:'Build fallback'})]);
  await events.initialize(document, '/events.json', async () => ({ok:true, json: async () => ({unexpected: []})}), now);
  assert.equal(feed.children[0].children[1].children[0].textContent, 'Build fallback');
});
