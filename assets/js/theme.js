"use strict";

(function initTheme() {
  var STORAGE_KEY = "theme";
  var root = document.documentElement;

  function getStored() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === "light" || saved === "dark") return saved;
    } catch (e) {}
    return null;
  }

  function systemPrefersDark() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    );
  }

  function currentTheme() {
    var explicit = root.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    return systemPrefersDark() ? "dark" : "light";
  }

  function apply(theme) {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.setAttribute("data-theme", "light");
    }
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

  // Follow OS changes — but only while the user hasn't made an explicit choice.
  if (window.matchMedia) {
    var mql = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function () {
      if (getStored()) return;
      apply(systemPrefersDark() ? "dark" : "light");
    };
    if (mql.addEventListener) {
      mql.addEventListener("change", onChange);
    } else if (mql.addListener) {
      mql.addListener(onChange);
    }
  }
})();
