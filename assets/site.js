/* Mimac site: three small enhancements. Everything works without this file. */
(function () {
  "use strict";
  /* Mobile navigation toggle */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("menu");
  if (toggle && menu) {
    var setOpen = function (open) {
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    };
    toggle.addEventListener("click", function () {
      setOpen(!document.body.classList.contains("nav-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
  }

  /* FAQ accordions: keep one answer open per group */
  var groups = document.querySelectorAll(".faq");
  for (var i = 0; i < groups.length; i++) {
    groups[i].addEventListener("toggle", function (e) {
      var d = e.target;
      if (!d.open) return;
      var open = this.querySelectorAll("details[open]");
      for (var j = 0; j < open.length; j++) {
        if (open[j] !== d) open[j].open = false;
      }
    }, true);
  }

  /* Comparison tables: click or focus a row to pin its highlight */
  var rows = document.querySelectorAll("table.compare tbody tr");
  for (var k = 0; k < rows.length; k++) {
    rows[k].addEventListener("click", function () {
      this.classList.toggle("pinned");
    });
  }
})();
