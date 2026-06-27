"use strict";

(function initTheme() {
  var STORAGE_KEY = "theme";
  var root = document.documentElement;

  function currentTheme() {
    var explicit = root.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    // Light is the default unless the user has explicitly chosen dark.
    return "light";
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    syncToggle(theme);
  }

  function syncToggle(theme) {
    var isDark = theme === "dark";
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", isDark ? "true" : "false");
      btn.setAttribute(
        "aria-label",
        isDark ? "Switch to light theme" : "Switch to dark theme"
      );
    });
  }

  // On boot, the inline head script already applied an explicit data-theme if
  // one was stored. Make sure the toggle reflects the effective theme.
  syncToggle(currentTheme());

  // Wire up the toggle(s).
  document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (e) {}
      apply(next);
    });
  });
})();
