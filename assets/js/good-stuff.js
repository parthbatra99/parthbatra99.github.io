"use strict";

// Turns the markdown on /the-good-stuff/ into scannable pieces:
// books + podcasts become expandable rows, bio-hacking notes become tiles.
// Without JS the page stays plain, readable markdown.
(function initGoodStuff() {
  var root = document.querySelector("[data-good-stuff]");
  if (!root) return;

  var STOP = /^(H2|H3|HR)$/;
  var TILE_SECTIONS = { "bio-hacking": true };
  var ROW_SECTIONS = { books: true, podcasts: true };

  function sectionOf(el) {
    var prev = el.previousElementSibling;
    while (prev && prev.tagName !== "H2") prev = prev.previousElementSibling;
    return prev ? prev.id : "";
  }

  function collect(h3) {
    var parts = [];
    var node = h3.nextElementSibling;
    while (node && !STOP.test(node.tagName)) {
      if (/^currently curating/i.test(node.textContent.trim())) break;
      parts.push(node);
      node = node.nextElementSibling;
    }
    return parts;
  }

  function looksLikeByline(el) {
    return el && el.tagName === "P" && el.textContent.trim().length < 60 && !/[.!?]$/.test(el.textContent.trim());
  }

  var firstRow = true;
  var tileGrid = null;
  var tileCount = 0;

  Array.prototype.slice.call(root.querySelectorAll(":scope > h3")).forEach(function (h3) {
    var section = sectionOf(h3);
    var parts = collect(h3);
    var title = h3.textContent.trim();

    if (ROW_SECTIONS[section]) {
      var details = document.createElement("details");
      details.className = "rec";
      if (firstRow) { details.open = true; firstRow = false; }

      var summary = document.createElement("summary");
      var heading = document.createElement("h3");
      heading.className = "rec-title";
      heading.textContent = title;
      if (looksLikeByline(parts[0])) {
        var by = document.createElement("span");
        by.className = "rec-by";
        var byline = parts.shift();
        by.textContent = byline.textContent.trim();
        byline.remove();
        heading.appendChild(by);
      }
      var sign = document.createElement("span");
      sign.className = "rec-sign";
      sign.setAttribute("aria-hidden", "true");
      sign.textContent = "+";
      summary.appendChild(heading);
      summary.appendChild(sign);

      var body = document.createElement("div");
      body.className = "rec-body";
      parts.forEach(function (p) { body.appendChild(p); });

      details.appendChild(summary);
      details.appendChild(body);
      h3.replaceWith(details);
      return;
    }

    if (TILE_SECTIONS[section]) {
      if (!tileGrid || tileGrid.dataset.section !== section) {
        tileGrid = document.createElement("div");
        tileGrid.className = "tiles";
        tileGrid.dataset.section = section;
        h3.before(tileGrid);
        tileCount = 0;
      }
      tileCount += 1;
      var tile = document.createElement("article");
      tile.className = "tile";
      var num = document.createElement("span");
      num.className = "tile-num";
      num.textContent = String(tileCount).padStart(2, "0");
      var th = document.createElement("h3");
      th.textContent = title;
      tile.appendChild(num);
      tile.appendChild(th);
      parts.forEach(function (p) { tile.appendChild(p); });
      tileGrid.appendChild(tile);
      h3.remove();
    }
  });

  Array.prototype.forEach.call(root.querySelectorAll(":scope > p"), function (p) {
    if (/^(currently curating|coming soon)/i.test(p.textContent.trim())) p.classList.add("muted-note");
  });

  root.classList.add("is-enhanced");
})();
