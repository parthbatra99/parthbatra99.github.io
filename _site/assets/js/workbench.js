"use strict";

// Turns each workbench entry (### title, dated log paragraphs, > summary)
// into a project card with a status pill, stack chips and a folding build log.
// Without JS the page stays plain markdown.
(function initWorkbench() {
  var root = document.querySelector("[data-workbench]");
  if (!root) return;

  var DATE = /^\s*\[(\d{4}-\d{2}-\d{2})\]\s*$/;

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  var first = true;

  Array.prototype.slice.call(root.querySelectorAll(":scope > h3")).forEach(function (h3) {
    var logs = [];
    var quote = null;
    var node = h3.nextElementSibling;
    var toRemove = [];

    while (node && !/^(H2|H3|HR)$/.test(node.tagName)) {
      var strong = node.tagName === "P" ? node.querySelector(":scope > strong:first-child") : null;
      if (strong && DATE.test(strong.textContent)) {
        logs.push(node);
      } else if (node.tagName === "BLOCKQUOTE") {
        quote = node;
      }
      toRemove.push(node);
      node = node.nextElementSibling;
    }
    if (node && node.tagName === "HR") toRemove.push(node);

    var card = el("article", "proj");
    var top = el("div", "proj-top");
    var title = el("h3", "proj-title", h3.textContent.trim());
    top.appendChild(title);
    card.appendChild(top);

    if (quote) {
      var paras = Array.prototype.slice.call(quote.querySelectorAll("p"));
      paras.forEach(function (p) {
        var code = p.querySelector("code");
        var text = p.textContent.trim();
        if (/^summary:/i.test(text)) {
          var summary = el("p", "proj-summary", text.replace(/^summary:\s*/i, ""));
          card.appendChild(summary);
        } else if (code && p.textContent.trim() === code.textContent.trim()) {
          var stack = el("div", "stack");
          code.textContent.split("·").forEach(function (item) {
            if (item.trim()) stack.appendChild(el("span", "chip", item.trim()));
          });
          card.appendChild(stack);
        } else {
          // status line: "<emoji> Status — links"
          var head = text.split("—")[0].replace(/^[^A-Za-z]+/, "").trim();
          if (head) {
            var wip = !/shipped|done|live/i.test(head);
            top.appendChild(el("span", "status " + (wip ? "status--wip" : "status--done"), head));
          }
          var links = el("p", "proj-links");
          var anchors = p.querySelectorAll("a");
          if (anchors.length) {
            Array.prototype.forEach.call(anchors, function (a) { links.appendChild(a.cloneNode(true)); });
          } else {
            var rest = text.split("—").slice(1).join("—").trim();
            if (rest) links.appendChild(el("span", "", rest));
          }
          if (links.childNodes.length) card.appendChild(links);
        }
      });
    }

    if (logs.length) {
      var details = el("details", "proj-log");
      if (first) details.open = true;
      details.appendChild(el("summary", "", "Build log · " + logs.length + (logs.length === 1 ? " entry" : " entries")));
      logs.forEach(function (p) {
        var strong = p.querySelector(":scope > strong:first-child");
        var date = strong.textContent.replace(/[\[\]\s]/g, "");
        strong.remove();
        var row = el("div", "log-row");
        row.appendChild(el("span", "log-date", date));
        var body = el("p");
        body.innerHTML = p.innerHTML.trim();
        row.appendChild(body);
        details.appendChild(row);
      });
      card.appendChild(details);
    }

    first = false;
    h3.replaceWith(card);
    toRemove.forEach(function (n) { n.remove(); });
  });

  root.classList.add("is-enhanced");
})();
