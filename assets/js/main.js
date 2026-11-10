/* ==========================================================================
   Patient Aid — site interactions
   Vanilla JavaScript, no dependencies.
   Handles: sticky header state, mobile navigation, FAQ accordion,
   screenshot lightbox, language switcher, scroll reveals, back-to-top.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document;
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------ Header -- */
  var header = doc.querySelector(".site-header");
  var toTop = doc.querySelector(".to-top");

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) {
      header.classList.toggle("is-scrolled", y > 8);
    }
    if (toTop) {
      toTop.classList.toggle("is-visible", y > 720);
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  }

  /* ------------------------------------------------- Mobile navigation -- */
  var navToggle = doc.querySelector(".nav-toggle");
  var primaryNav = doc.getElementById("primaryNav");

  function setNav(open) {
    if (!navToggle || !primaryNav) return;
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    primaryNav.classList.toggle("is-open", open);
  }

  if (navToggle && primaryNav) {
    navToggle.addEventListener("click", function () {
      setNav(navToggle.getAttribute("aria-expanded") !== "true");
    });

    primaryNav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setNav(false);
    });

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
        setNav(false);
        navToggle.focus();
      }
    });

    doc.addEventListener("click", function (event) {
      if (
        navToggle.getAttribute("aria-expanded") === "true" &&
        !event.target.closest(".primary-nav") &&
        !event.target.closest(".nav-toggle")
      ) {
        setNav(false);
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 860) setNav(false);
    });
  }

  /* ------------------------------------------------------ FAQ accordion -- */
  var faqButtons = Array.prototype.slice.call(doc.querySelectorAll(".faq-q"));

  faqButtons.forEach(function (button) {
    var item = button.closest(".faq-item");
    var panel = doc.getElementById(button.getAttribute("aria-controls"));

    if (!item || !panel) return;

    // Start from the markup state so deep links / no-JS behaviour stay sane.
    var expanded = button.getAttribute("aria-expanded") === "true";
    panel.setAttribute("aria-hidden", expanded ? "false" : "true");
    if (!expanded) panel.setAttribute("inert", "");

    button.addEventListener("click", function () {
      var isOpen = button.getAttribute("aria-expanded") === "true";
      var group = item.parentElement;

      // Only one open answer per list keeps long pages tidy.
      if (!isOpen && group) {
        Array.prototype.forEach.call(group.querySelectorAll(".faq-item.is-open"), function (other) {
          if (other === item) return;
          var otherButton = other.querySelector(".faq-q");
          var otherPanel = otherButton && doc.getElementById(otherButton.getAttribute("aria-controls"));
          other.classList.remove("is-open");
          if (otherButton) otherButton.setAttribute("aria-expanded", "false");
          if (otherPanel) {
            otherPanel.setAttribute("aria-hidden", "true");
            otherPanel.setAttribute("inert", "");
          }
        });
      }

      item.classList.toggle("is-open", !isOpen);
      button.setAttribute("aria-expanded", isOpen ? "false" : "true");
      panel.setAttribute("aria-hidden", isOpen ? "true" : "false");
      if (isOpen) {
        panel.setAttribute("inert", "");
      } else {
        panel.removeAttribute("inert");
      }
    });
  });

  /* -------------------------------------------------- Language switcher -- */
  var langTabs = Array.prototype.slice.call(doc.querySelectorAll(".lang-tab"));

  langTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      langTabs.forEach(function (other) {
        var panel = doc.getElementById(other.getAttribute("aria-controls"));
        var active = other === tab;
        other.setAttribute("aria-selected", active ? "true" : "false");
        other.setAttribute("tabindex", active ? "0" : "-1");
        if (panel) panel.hidden = !active;
      });
    });

    tab.addEventListener("keydown", function (event) {
      if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
      event.preventDefault();
      var index = langTabs.indexOf(tab);
      var next = event.key === "ArrowRight" ? index + 1 : index - 1;
      var target = langTabs[(next + langTabs.length) % langTabs.length];
      target.focus();
      target.click();
    });
  });

  /* ------------------------------------------------------------ Lightbox -- */
  var shots = Array.prototype.slice.call(doc.querySelectorAll(".shot"));
  var lightbox = doc.querySelector(".lightbox");

  if (shots.length && lightbox) {
    var lightboxImg = lightbox.querySelector(".lightbox img");
    var lightboxCaption = lightbox.querySelector(".lightbox-caption");
    var closeBtn = lightbox.querySelector(".lightbox-close");
    var prevBtn = lightbox.querySelector(".lightbox-nav--prev");
    var nextBtn = lightbox.querySelector(".lightbox-nav--next");
    var current = 0;
    var lastFocused = null;

    function render(index) {
      current = (index + shots.length) % shots.length;
      var shot = shots[current];
      var full = shot.getAttribute("data-full");
      var img = shot.querySelector("img");
      var caption = shot.getAttribute("data-caption") || (img ? img.alt : "");

      if (full) lightboxImg.src = full;
      lightboxImg.alt = caption ? caption + " — Patient Aid app screenshot" : "Patient Aid app screenshot";
      if (lightboxCaption) lightboxCaption.textContent = caption;
      lightbox.setAttribute("aria-label", caption ? caption + " preview" : "Screenshot preview");
    }

    function open(index) {
      lastFocused = doc.activeElement;
      render(index);
      lightbox.classList.add("is-open");
      lightbox.removeAttribute("aria-hidden");
      doc.body.classList.add("is-locked");
      if (closeBtn) closeBtn.focus();
    }

    function close() {
      lightbox.classList.remove("is-open");
      lightbox.setAttribute("aria-hidden", "true");
      doc.body.classList.remove("is-locked");
      if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
    }

    shots.forEach(function (shot, index) {
      shot.addEventListener("click", function () {
        open(index);
      });
    });

    if (closeBtn) closeBtn.addEventListener("click", close);
    if (prevBtn) prevBtn.addEventListener("click", function () { render(current - 1); });
    if (nextBtn) nextBtn.addEventListener("click", function () { render(current + 1); });

    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox) close();
    });

    doc.addEventListener("keydown", function (event) {
      if (!lightbox.classList.contains("is-open")) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") render(current - 1);
      if (event.key === "ArrowRight") render(current + 1);
      if (event.key === "Tab") {
        // Keep focus inside the dialog.
        var focusable = [closeBtn, prevBtn, nextBtn].filter(Boolean);
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (event.shiftKey && doc.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && doc.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  /* ------------------------------------------------------ Scroll reveal -- */
  var revealItems = Array.prototype.slice.call(doc.querySelectorAll(".reveal"));

  if (revealItems.length) {
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      revealItems.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      // Small stagger inside grids, based on DOM order within the same parent.
      revealItems.forEach(function (el) {
        var siblings = Array.prototype.filter.call(el.parentElement.children, function (child) {
          return child.classList.contains("reveal");
        });
        var index = siblings.indexOf(el);
        if (index > 0 && index < 6) {
          el.style.transitionDelay = (index * 70) + "ms";
        }
      });

      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

      revealItems.forEach(function (el) { observer.observe(el); });
    }
  }

  /* ---------------------------------------------------- Scroll progress -- */
  var progressBar = doc.createElement("div");
  progressBar.className = "scroll-progress";
  progressBar.setAttribute("aria-hidden", "true");
  doc.body.appendChild(progressBar);

  var progressQueued = false;

  function updateProgress() {
    var max = doc.documentElement.scrollHeight - window.innerHeight;
    var scrolled = window.scrollY || window.pageYOffset;
    var value = max > 0 ? Math.min(1, Math.max(0, scrolled / max)) : 0;
    progressBar.style.transform = "scaleX(" + value.toFixed(4) + ")";
    progressQueued = false;
  }

  function queueProgress() {
    if (progressQueued) return;
    progressQueued = true;
    window.requestAnimationFrame(updateProgress);
  }

  window.addEventListener("scroll", queueProgress, { passive: true });
  window.addEventListener("resize", queueProgress);
  window.addEventListener("load", queueProgress);
  updateProgress();

  /* ------------------------------------------------------ Hero parallax -- */
  var hero = doc.querySelector(".hero");
  var heroVisual = doc.querySelector(".hero-visual");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  if (hero && heroVisual && finePointer && !prefersReducedMotion) {
    var parallaxQueued = false;
    var pointerX = 0;
    var pointerY = 0;

    hero.addEventListener("pointermove", function (event) {
      var rect = hero.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      pointerX = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
      pointerY = ((event.clientY - rect.top) / rect.height - 0.5) * 2;
      if (parallaxQueued) return;
      parallaxQueued = true;
      window.requestAnimationFrame(function () {
        heroVisual.style.setProperty("--px", (pointerX * 7).toFixed(2) + "px");
        heroVisual.style.setProperty("--py", (pointerY * 6).toFixed(2) + "px");
        parallaxQueued = false;
      });
    });

    hero.addEventListener("pointerleave", function () {
      heroVisual.style.setProperty("--px", "0px");
      heroVisual.style.setProperty("--py", "0px");
    });
  }

  /* ------------------------------------------------------- Stat counters -- */
  var counters = Array.prototype.slice.call(doc.querySelectorAll("[data-count-to]"));

  if (counters.length) {
    var formatCounter = function (el, value) {
      var decimals = parseInt(el.getAttribute("data-count-decimals") || "0", 10);
      var number = decimals > 0 ? value.toFixed(decimals) : String(Math.round(value));
      return number + (el.getAttribute("data-count-suffix") || "");
    };

    var finalCounterValue = function (el) {
      return formatCounter(el, parseFloat(el.getAttribute("data-count-to")) || 0);
    };

    var runCounter = function (el) {
      var target = parseFloat(el.getAttribute("data-count-to")) || 0;
      var duration = 1400;
      var startTime = null;

      var tick = function (now) {
        if (startTime === null) startTime = now;
        var progress = Math.min(1, (now - startTime) / duration);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = formatCounter(el, target * eased);
        if (progress < 1) {
          window.requestAnimationFrame(tick);
        } else {
          el.textContent = formatCounter(el, target);
        }
      };

      window.requestAnimationFrame(tick);
    };

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      counters.forEach(function (el) {
        el.textContent = finalCounterValue(el);
      });
    } else {
      var counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          runCounter(entry.target);
          counterObserver.unobserve(entry.target);
        });
      }, { threshold: 0.55 });

      counters.forEach(function (el) {
        el.textContent = formatCounter(el, 0);
        counterObserver.observe(el);
      });

      // Safety net: never leave a zero on screen if the observer cannot fire.
      window.setTimeout(function () {
        counters.forEach(function (el) {
          if (el.textContent === formatCounter(el, 0)) {
            el.textContent = finalCounterValue(el);
          }
        });
      }, 4000);
    }
  }

  /* --------------------------------------------------------- Year stamp -- */
  var yearTargets = doc.querySelectorAll("[data-year]");
  Array.prototype.forEach.call(yearTargets, function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
