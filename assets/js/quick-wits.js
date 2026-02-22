"use strict";

(function initQuickWits() {
  const page = document.querySelector("[data-quick-wits-page]");
  const feed = page?.querySelector("[data-qw-feed]");
  if (!page || !feed) return;

  const toArray = (nodes) => Array.prototype.slice.call(nodes);

  function createMonthSection(label, index) {
    const section = document.createElement("section");
    section.className = "qw-month";

    const headingId = "qw-month-" + (index + 1);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "qw-month-toggle";
    button.setAttribute("aria-expanded", "true");
    button.setAttribute("aria-controls", headingId);
    button.innerHTML =
      '<span class="qw-month-label"></span><span class="qw-month-caret" aria-hidden="true"></span>';
    button.querySelector(".qw-month-label").textContent = label;

    const body = document.createElement("div");
    body.className = "qw-month-body";
    body.id = headingId;

    section.appendChild(button);
    section.appendChild(body);
    return section;
  }

  function normalizeLegacyMonthMarkup() {
    const existingMonths = feed.querySelectorAll(":scope > .qw-month");
    if (existingMonths.length > 0) return;

    const children = toArray(feed.children);
    const fragment = document.createDocumentFragment();
    let current = null;
    let monthIndex = 0;

    children.forEach((node) => {
      if (node.tagName === "H3") {
        current = createMonthSection(node.textContent.trim(), monthIndex++);
        fragment.appendChild(current);
        return;
      }

      if (node.tagName === "HR") return;

      if (!current) {
        current = createMonthSection("Archive", monthIndex++);
        fragment.appendChild(current);
      }

      current.querySelector(".qw-month-body").appendChild(node);
    });

    if (fragment.childElementCount > 0) {
      feed.innerHTML = "";
      feed.appendChild(fragment);
    }
  }

  function setMonthExpanded(monthEl, expanded) {
    const toggle = monthEl.querySelector(".qw-month-toggle");
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    monthEl.classList.toggle("is-collapsed", !expanded);
  }

  normalizeLegacyMonthMarkup();

  const months = toArray(feed.querySelectorAll(":scope > .qw-month"));
  months.forEach((monthEl, index) => {
    const toggle = monthEl.querySelector(".qw-month-toggle");
    if (!toggle) return;

    setMonthExpanded(monthEl, index === 0);
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      setMonthExpanded(monthEl, !expanded);
    });
  });

  const tweetCount = feed.querySelectorAll(".tweet-entry").length;
  const monthCount = months.length;
  const tweetStat = page.querySelector('[data-qw-stat="tweets"]');
  const monthStat = page.querySelector('[data-qw-stat="months"]');
  if (tweetStat) tweetStat.textContent = String(tweetCount);
  if (monthStat) monthStat.textContent = String(monthCount);

  page.classList.add("qw-ready");
})();
