/* ==========================================================================
   MoE, Explained — comments, via giscus (GitHub Discussions)
   --------------------------------------------------------------------------
   The same setup "How To Scale Your Model" uses. Threads live in GitHub
   Discussions, so there is no database, no tracking, and no account for us to
   administer — and the people who show up are people who can argue with the math.

   This is the only third-party script in the book. Everything that renders the
   content itself — diagrams, animations, math — is local and works offline.
   tools/to_artifact.py strips this file when packaging a chapter for sharing.
   ========================================================================== */
(function () {
  "use strict";

  var mount = document.getElementById("giscus-mount");
  if (!mount) return;

  // Mirror the page's own three-state theme logic: an explicit data-theme wins,
  // otherwise fall back to the OS preference.
  function theme() {
    var stamped = document.documentElement.getAttribute("data-theme");
    if (stamped === "dark") return "dark";
    if (stamped === "light") return "light";
    return window.matchMedia &&
           window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark" : "light";
  }

  var s = document.createElement("script");
  s.src = "https://giscus.app/client.js";
  s.async = true;
  s.crossOrigin = "anonymous";
  var attrs = {
    "data-repo":              "Noman654/moe-explained",
    "data-repo-id":           "R_kgDOT4sqcQ",
    "data-category":          "Announcements",
    "data-category-id":       "DIC_kwDOT4sqcc4DDY5u",
    "data-mapping":           "pathname",   // one thread per chapter
    "data-strict":            "1",
    "data-reactions-enabled": "1",
    "data-emit-metadata":     "0",
    "data-input-position":    "top",
    "data-theme":             theme(),
    "data-lang":              "en",
    "data-loading":           "lazy"
  };
  for (var k in attrs) if (attrs.hasOwnProperty(k)) s.setAttribute(k, attrs[k]);
  mount.appendChild(s);

  // If giscus cannot load, say what happened instead of showing a raw error.
  // Two failure modes need covering: the script never producing an iframe
  // (blocked network), and — the sneaky one — giscus creating its iframe and
  // then erroring *inside* it (e.g. the GitHub App not installed on the repo).
  // giscus broadcasts that second kind via postMessage, so listen for it.
  function fallback() {
    if (mount.querySelector(".commentfallback")) return;
    var f = mount.querySelector("iframe.giscus-frame");
    if (f) f.style.display = "none";
    var note = document.createElement("p");
    note.className = "commentfallback";
    note.innerHTML =
      "The comment box isn’t available right now — the giscus app isn’t " +
      "installed on this repository yet (a one-click step for the owner). " +
      'Until it is, <a href="https://github.com/Noman654/moe-explained/issues/new">' +
      "an issue</a> reaches me just as well.";
    mount.appendChild(note);
  }
  window.addEventListener("message", function (e) {
    if (e.origin !== "https://giscus.app") return;
    if (e.data && e.data.giscus && e.data.giscus.error) fallback();
  });
  setTimeout(function () {
    if (!mount.querySelector("iframe.giscus-frame")) fallback();
  }, 6000);

  // Keep the embedded thread in step if the viewer flips their OS theme mid-read.
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function () {
      var frame = document.querySelector("iframe.giscus-frame");
      if (!frame) return;
      frame.contentWindow.postMessage(
        { giscus: { setConfig: { theme: theme() } } }, "https://giscus.app");
    };
    mq.addEventListener ? mq.addEventListener("change", onChange)
                        : mq.addListener(onChange);
  }
})();
