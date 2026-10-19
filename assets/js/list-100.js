"use strict";

// Upgrades the plain "✗ / ✓ / ◐" markdown list on /list-100/ into status rows
// with icons and filters, and keeps the tracker numbers in sync with the list.
(function initList100() {
  var list = document.querySelector(".prose > ol");
  if (!list) return;

  var STATUS = { "✓": "done", "◐": "active", "✗": "todo" };
  var ICONS = {
    done: '<svg class="goal-ico" viewBox="0 0 16 16" role="img" aria-label="Completed"><circle cx="8" cy="8" r="7" fill="var(--accent)"/><path d="M4.8 8.2l2.1 2.1 4.3-4.6" fill="none" stroke="var(--bg)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    active: '<svg class="goal-ico" viewBox="0 0 16 16" role="img" aria-label="In progress"><circle cx="8" cy="8" r="6.5" fill="none" stroke="var(--accent)" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="var(--accent)"/></svg>',
    todo: '<svg class="goal-ico" viewBox="0 0 16 16" role="img" aria-label="Not started"><circle cx="8" cy="8" r="6.5" fill="none" stroke="var(--muted)" stroke-width="1.5"/></svg>'
  };

  var counts = { done: 0, active: 0, todo: 0 };
  var items = Array.prototype.slice.call(list.children);

  items.forEach(function (li, index) {
    var holder = li.querySelector(":scope > p") || li;
    var html = holder.innerHTML.trim();
    var match = html.match(/^(✓|◐|✗)\s*/);
    if (!match) return;
    var status = STATUS[match[1]];
    counts[status] += 1;
    html = html.slice(match[0].length);

    var note = "";
    var noteMatch = html.match(/\s*\(([^()]*)\)\s*$/);
    if (noteMatch) {
      note = noteMatch[1];
      html = html.slice(0, noteMatch.index);
    }

    li.className = "goal is-" + status;
    li.dataset.status = status;
    li.innerHTML =
      '<span class="goal-num">' + String(index + 1).padStart(2, "0") + "</span>" +
      "<span>" + ICONS[status] + "</span>" +
      '<span><span class="goal-text">' + html + "</span>" +
      (note ? ' <span class="goal-note">— ' + note + "</span>" : "") +
      "</span>";
  });

  list.classList.add("goal-list");

  var total = counts.done + counts.active + counts.todo;
  if (!total) return;

  // Keep the tracker honest: numbers come from the list itself.
  function setText(sel, value) {
    var node = document.querySelector(sel);
    if (node) node.textContent = value;
  }
  setText('[data-goal-count="done"]', counts.done);
  setText('[data-goal-count="active"]', counts.active);
  setText('[data-goal-count="todo"]', counts.todo);
  var touched = counts.done + counts.active;
  setText("[data-goal-summary]", Math.round((touched / total) * 100) + "% touched · " + touched + " of " + total + " tracked");
  var bar = document.querySelector("[data-goal-bar]");
  if (bar) {
    bar.setAttribute("aria-label", counts.done + " of " + total + " completed, " + counts.active + " in progress");
    bar.children[0].style.width = ((counts.done / total) * 100).toFixed(1) + "%";
    bar.children[1].style.width = ((counts.active / total) * 100).toFixed(1) + "%";
  }

  // Filters
  var filters = [
    ["all", "All " + total],
    ["done", "Done " + counts.done],
    ["active", "In progress " + counts.active],
    ["todo", "To do " + counts.todo]
  ];
  var group = document.createElement("div");
  group.className = "goal-filters";
  group.setAttribute("role", "group");
  group.setAttribute("aria-label", "Filter goals");

  function apply(id) {
    items.forEach(function (li) {
      li.classList.toggle("is-hidden", id !== "all" && li.dataset.status !== id);
    });
    Array.prototype.forEach.call(group.children, function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.filter === id ? "true" : "false");
    });
  }

  filters.forEach(function (f) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "goal-filter";
    btn.dataset.filter = f[0];
    btn.textContent = f[1];
    btn.addEventListener("click", function () { apply(f[0]); });
    group.appendChild(btn);
  });

  list.before(group);
  apply("all");
})();
