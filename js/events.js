/* Public calendar enhancement. The verified weekly schedule also works without JS. */
(function () {
  'use strict';

  var calendar = typeof module !== 'undefined' && module.exports ? require('./calendar-feed.js') : window.CreekCalendar;
  if (!calendar) return;
  var churchToday = calendar.churchToday, validDate = calendar.validDate,
    startMinutes = calendar.startMinutes, upcomingEvents = calendar.upcomingEvents;

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

  function initialize(document, url, fetcher, now, csvUrl) {
    var feeds = Array.prototype.slice.call(document.querySelectorAll('[data-events-feed]'));
    if (!feeds.length) return Promise.resolve();
    var today = churchToday(now), minutes = calendar.churchMinutes(now);
    var fallback = calendar.expandFeed(calendar.DEFAULT_FEED, today).filter(function (event) {
      var start = startMinutes(event.time);
      return event.when > today || start === null || start >= minutes;
    });
    feeds.forEach(function (feed) { feed.setAttribute('aria-live', 'polite'); render(document, feed, fallback); });
    return calendar.load({ jsonUrl: url, csvUrl: csvUrl || calendar.CSV_URL, fetcher: fetcher, now: now }).then(function (result) {
      feeds.forEach(function (feed) { render(document, feed, result.events); });
      document.querySelectorAll('[data-events-status]').forEach(function (status) {
        status.textContent = result.sources.community === 'unavailable'
          ? 'Regular gatherings are shown. Community updates are temporarily unavailable.'
          : result.sources.community === 'cache'
            ? 'Showing saved calendar updates. Recent changes need an internet connection.'
            : 'All times Central. Approved updates may take a few minutes to appear.';
      });
      return result;
    });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { churchToday: churchToday, validDate: validDate, startMinutes: startMinutes,
      upcomingEvents: upcomingEvents, eventRow: eventRow, initialize: initialize };
  }
  if (typeof document !== 'undefined') {
    var script = document.currentScript;
    var url = script && script.getAttribute('data-events-url');
    if (url) initialize(document, url, function (address, options) { return fetch(address, options); }, undefined, script.getAttribute('data-events-csv-url'));
  }
}());
