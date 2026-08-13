/* ==========================================================================
   MoE, Explained — the animation engine
   --------------------------------------------------------------------------
   A figure is a hand-authored inline <svg> plus a render(step) function. This
   module supplies the transport: play/pause, step forward and back, a scrub
   slider, and a caption that changes with the step.

   Why steps and not a timeline: every animation in this book shows a *mechanism*,
   and mechanisms have discrete stages a reader wants to sit on. Scrubbing beats
   a GIF you cannot pause on the one frame that matters.

   No dependencies. ~4KB. Works offline.
   ========================================================================== */
(function () {
  "use strict";

  var REDUCE = window.matchMedia &&
               window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var ICON_PLAY  = '<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true"><path d="M2 1 L10 6 L2 11 Z" fill="currentColor"/></svg>';
  var ICON_PAUSE = '<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true"><rect x="2" y="1" width="3" height="10" fill="currentColor"/><rect x="7" y="1" width="3" height="10" fill="currentColor"/></svg>';
  var ICON_PREV  = '<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true"><path d="M10 1 L3 6 L10 11 Z" fill="currentColor"/><rect x="1" y="1" width="2" height="10" fill="currentColor"/></svg>';
  var ICON_NEXT  = '<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true"><path d="M2 1 L9 6 L2 11 Z" fill="currentColor"/><rect x="9" y="1" width="2" height="10" fill="currentColor"/></svg>';

  /**
   * @param {Object} o
   *   o.mount    {Element}  container the control bar is appended to
   *   o.steps    {Array}    one entry per stage: { caption: string }
   *   o.render   {Function} render(stepIndex) — paint the SVG for this stage
   *   o.interval {Number}   ms per stage while playing (default 1600)
   *   o.loop     {Boolean}  restart from 0 after the last stage (default true)
   *   o.autoplay {Boolean}  begin playing when scrolled into view (default true)
   */
  function create(o) {
    var steps = o.steps,
        n = steps.length,
        interval = o.interval || 1600,
        loop = o.loop !== false,
        i = 0,
        timer = null,
        started = false;

    // ---- control bar -----------------------------------------------------
    var bar = document.createElement("div");
    bar.className = "animbar";
    bar.innerHTML =
      '<button type="button" class="ab-play" aria-label="Play animation">' + ICON_PLAY + '</button>' +
      '<button type="button" class="ab-step" data-d="-1" aria-label="Previous stage">' + ICON_PREV + '</button>' +
      '<button type="button" class="ab-step" data-d="1" aria-label="Next stage">' + ICON_NEXT + '</button>' +
      '<input type="range" class="ab-scrub" min="0" max="' + (n - 1) + '" value="0" step="1" aria-label="Animation stage">' +
      '<span class="ab-count"></span>';

    var cap = document.createElement("p");
    cap.className = "animcap";
    cap.setAttribute("role", "status");
    cap.setAttribute("aria-live", "polite");

    o.mount.appendChild(bar);
    o.mount.appendChild(cap);

    var playBtn = bar.querySelector(".ab-play"),
        scrub   = bar.querySelector(".ab-scrub"),
        count   = bar.querySelector(".ab-count");

    // ---- painting --------------------------------------------------------
    function paint() {
      o.render(i);
      scrub.value = i;
      count.textContent = (i + 1) + " / " + n;
      // Stage captions are numbered so the prose can refer to "stage 4".
      cap.innerHTML = '<b>Stage ' + (i + 1) + '.</b> ' + steps[i].caption;
    }

    function go(next) {
      i = (next + n) % n;
      paint();
    }

    // ---- transport -------------------------------------------------------
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      playBtn.innerHTML = ICON_PLAY;
      playBtn.setAttribute("aria-label", "Play animation");
      o.mount.classList.remove("is-playing");
    }

    function play() {
      if (timer) return;
      playBtn.innerHTML = ICON_PAUSE;
      playBtn.setAttribute("aria-label", "Pause animation");
      o.mount.classList.add("is-playing");
      timer = setInterval(function () {
        if (i + 1 >= n && !loop) { stop(); return; }
        go(i + 1);
      }, interval);
    }

    playBtn.addEventListener("click", function () { timer ? stop() : play(); });

    Array.prototype.forEach.call(bar.querySelectorAll(".ab-step"), function (b) {
      b.addEventListener("click", function () {
        stop();
        go(i + (+b.dataset.d));
      });
    });

    scrub.addEventListener("input", function () {
      stop();
      go(+scrub.value);
    });

    // Pause when the figure scrolls away — no work happening off-screen, and
    // nothing is moving behind the reader's back.
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            if (!started && o.autoplay !== false && !REDUCE) { started = true; play(); }
          } else {
            stop();
          }
        });
      }, { threshold: 0.35 }).observe(o.mount);
    }

    // Reduced motion: land on the final stage, fully rendered, and let the
    // reader step through it by hand. Never autoplay.
    if (REDUCE) { i = n - 1; }
    paint();

    return { play: play, stop: stop, go: go };
  }

  // ---- small helpers used by the figures themselves ----------------------

  /** Set many attributes at once. */
  function attr(el, o) {
    for (var k in o) if (o.hasOwnProperty(k)) el.setAttribute(k, o[k]);
    return el;
  }

  /** Toggle a class on an element by id. */
  function cls(root, id, name, on) {
    var el = root.getElementById ? root.getElementById(id) : document.getElementById(id);
    if (el) el.classList[on ? "add" : "remove"](name);
    return el;
  }

  window.MoEAnim = { create: create, attr: attr, cls: cls, REDUCE: REDUCE };
})();
