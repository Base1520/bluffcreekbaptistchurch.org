/* Optional YouTube player. No iframe or YouTube request before activation.
   A frame's load event does not establish stream availability or playback. */
(function () {
  'use strict';

  function initialize(container, timers) {
    var button = container.querySelector('[data-watch-load]');
    var mount = container.querySelector('[data-watch-mount]');
    var status = container.querySelector('[data-watch-status]');
    var channel = container.getAttribute('data-watch-channel') || '';
    if (!button || !mount || !status) return false;
    if (!/^UC[A-Za-z0-9_-]{22}$/.test(channel)) return false;
    if (container.getAttribute('data-watch-initialized') === 'true') return false;

    timers = timers || window;
    var currentFrame = null;
    var waiting = false;
    var timeout = null;
    container.setAttribute('data-watch-initialized', 'true');
    container.setAttribute('data-watch-state', 'idle');
    button.hidden = false;

    button.addEventListener('click', function () {
      if (waiting) return;
      waiting = true;
      if (timeout !== null) timers.clearTimeout(timeout);
      button.setAttribute('aria-disabled', 'true');
      button.textContent = 'Loading YouTube player…';
      mount.setAttribute('aria-busy', 'true');
      container.setAttribute('data-watch-state', 'loading');
      status.textContent = 'Loading the YouTube player. The direct YouTube link remains available below.';

      var frame = container.ownerDocument.createElement('iframe');
      currentFrame = frame;
      frame.title = 'Bluff Creek Baptist Church YouTube player';
      frame.width = '960';
      frame.height = '540';
      frame.allow = 'encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';

      function finish(message, state) {
        if (currentFrame !== frame) return;
        if (timeout !== null) timers.clearTimeout(timeout);
        timeout = null;
        waiting = false;
        mount.setAttribute('aria-busy', 'false');
        button.setAttribute('aria-disabled', 'false');
        button.textContent = 'Reload YouTube player';
        container.setAttribute('data-watch-state', state);
        status.textContent = message;
        // Keep focus where the visitor placed it; loading never steals focus.
      }

      frame.addEventListener('load', function () {
        finish('If a service is available, use the player controls to watch. If nothing appears, open YouTube below.', 'attempted');
      });
      // Best effort only: browsers may report load even for failed frames.
      frame.addEventListener('error', function () {
        finish('The player could not be loaded here. Try again or open YouTube below.', 'retry');
      });
      timeout = timers.setTimeout(function () {
        finish('The player may still be loading. You can retry or open YouTube below.', 'waiting');
      }, 12000);

      // Preserve the existing channel live-stream shortcut. It is an attempt,
      // not an availability check; the direct channel links are authoritative.
      var source = new URL('https://www.youtube.com/embed/live_stream');
      source.searchParams.set('channel', channel);
      source.searchParams.set('autoplay', '0');
      source.searchParams.set('playsinline', '1');
      frame.src = source.href;
      mount.hidden = false;
      mount.replaceChildren(frame);
    });
    return true;
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { initialize: initialize };
  if (typeof document !== 'undefined') {
    document.querySelectorAll('[data-watch-player]').forEach(function (container) {
      initialize(container);
    });
  }
}());
