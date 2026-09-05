/* Public calendar enhancement. The verified weekly schedule also works without JS. */
(function () {
  'use strict';

  var DATE = /^\d{4}-\d{2}-\d{2}$/;
  var TIME = /^(1[0-2]|[1-9])(?::([0-5]\d))?\s*([ap])m?$/i;

  function churchToday(now) {
    var parts = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/Chicago', year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(now || new Date());
    var fields = {};
    parts.forEach(function (part) { fields[part.type] = part.value; });
    return fields.year + '-' + fields.month + '-' + fields.day;
  }

  function validDate(value) {
    if (typeof value !== 'string' || !DATE.test(value)) return false;
    if (Number(value.slice(0, 4)) < 1) return false;
    var date = new Date(value + 'T12:00:00Z');
    return !isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
  }

  function startMinutes(value) {
    if (typeof value !== 'string') return null;
    var match = TIME.exec(value.trim());
    if (!match) return null;
    return ((Number(match[1]) % 12) + (match[3].toLowerCase() === 'p' ? 12 : 0)) * 60 + Number(match[2] || 0);
  }

  function upcomingEvents(events, today) {
    if (!Array.isArray(events)) return [];
    return events.filter(function (event) {
      if (!event || typeof event !== 'object') return false;
      if (['when', 'time', 'title', 'where', 'tag'].some(function (key) {
        return typeof event[key] !== 'string' || !event[key].trim();
      })) return false;
      return ['Weekly', 'Monthly', 'Special'].indexOf(event.tag) !== -1 &&
        validDate(event.when) && event.when >= today && startMinutes(event.time) !== null;
    }).sort(function (a, b) {
      return a.when.localeCompare(b.when) || startMinutes(a.time) - startMinutes(b.time);
    });
  }

  function element(document, tag, text, className) {
    var node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function emptyState(document) {
    var paragraph = element(document, 'p', 'Find a place in the week. ', 'events-empty');
    var link = element(document, 'a', 'View our weekly gathering times ');
    link.href = 'times.html';
    var arrow = element(document, 'span', '→');
    arrow.setAttribute('aria-hidden', 'true');
    link.appendChild(arrow);
    paragraph.appendChild(link);
    return paragraph;
  }

  function eventRow(document, event) {
    var row = element(document, 'article', undefined, 'event-row');
    var time = element(document, 'time');
    time.setAttribute('datetime', event.when);
    var date = new Date(event.when + 'T12:00:00Z');
    time.appendChild(element(document, 'span', ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][date.getUTCDay()]));
    time.appendChild(document.createTextNode(String(date.getUTCDate())));
    var detail = element(document, 'div');
    detail.appendChild(element(document, 'h3', event.title));
    detail.appendChild(element(document, 'p', event.time + ' · ' + event.where));
    row.appendChild(time);
    row.appendChild(detail);
    return row;
  }

  function render(document, feed, events) {
    var limit = Math.max(1, Math.min(parseInt(feed.getAttribute('data-events-feed'), 10) || 3, 50));
    var fragment = document.createDocumentFragment();
    events.slice(0, limit).forEach(function (event) { fragment.appendChild(eventRow(document, event)); });
    if (!events.length) fragment.appendChild(emptyState(document));
    feed.replaceChildren(fragment);
  }

  function cleanFallback(document, feed, today) {
    Array.prototype.slice.call(feed.querySelectorAll('.event-row')).forEach(function (row) {
      var time = row.querySelector('time[datetime]');
      var date = time && time.getAttribute('datetime');
      if (!validDate(date) || date < today) row.remove();
    });
    if (!feed.querySelector('.event-row')) render(document, feed, []);
  }

  function initialize(document, url, fetcher, now) {
    var feeds = Array.prototype.slice.call(document.querySelectorAll('[data-events-feed]'));
    if (!feeds.length) return Promise.resolve();
    var today = churchToday(now);
    feeds.forEach(function (feed) {
      feed.setAttribute('aria-live', 'polite');
      cleanFallback(document, feed, today);
    });
    // Remove expired build-time rows before requesting the feed. An offline or
    // invalid response therefore cannot resurrect dated events from a stale build.
    return Promise.resolve().then(function () {
      return fetcher(url, { cache: 'no-cache' });
    }).then(function (response) {
      if (!response.ok) throw new Error('Calendar response unavailable');
      return response.json();
    }).then(function (data) {
      if (!data || !Array.isArray(data.events)) throw new Error('Calendar response invalid');
      var events = upcomingEvents(data.events, today);
      feeds.forEach(function (feed) { render(document, feed, events); });
    }).catch(function () {
      // The current build-time rows or the useful weekly-schedule link remain.
    });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { churchToday: churchToday, validDate: validDate, startMinutes: startMinutes,
      upcomingEvents: upcomingEvents, eventRow: eventRow, initialize: initialize };
  }
  if (typeof document !== 'undefined') {
    var script = document.currentScript;
    var url = script && script.getAttribute('data-events-url');
    if (url) initialize(document, url, function (address, options) { return fetch(address, options); });
  }
}());
