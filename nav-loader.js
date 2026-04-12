/**
 * nav-loader.js — Rosetta Brands
 *
 * Two modes:
 *   INLINED  (production) — build.py has already stamped nav + footer HTML
 *     directly into the page. We detect data-inlined="true" on the placeholder
 *     div and skip all fetch() calls, going straight to initNav().
 *     Result: zero extra network requests, nav is visible on first paint.
 *
 *   FETCH  (development / local) — placeholders are empty divs. We fetch
 *     _nav.html and _footer.html as before. Requires a local HTTP server:
 *     python3 -m http.server
 *
 * The fade-in observer always runs independently of both modes.
 */
(function () {

  var currentPage = window.location.pathname.split('/').pop() || 'index.html';

  // ── 1. FAQ accordion — always runs ───────────────────────────────────────
  // Guard: data-faq-init prevents duplicate listeners when this script is
  // loaded more than once (deferred in <head> + inline at end of <body>).
  function initFAQ() {
    document.querySelectorAll('.faq-q').forEach(function (btn) {
      if (btn.dataset.faqInit) return;          // already wired — skip
      btn.dataset.faqInit = '1';
      var answer = btn.nextElementSibling;
      btn.addEventListener('click', function () {
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (answer) {
          if (expanded) { answer.setAttribute('hidden', ''); }
          else          { answer.removeAttribute('hidden'); }
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFAQ);
  } else {
    initFAQ();
  }

  // ── 3. Fade-in observer — always runs ────────────────────────────────────
  function initFadeIn() {
    var els = document.querySelectorAll('.fade-in');
    if (!els.length) return;
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { obs.observe(el); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFadeIn);
  } else {
    initFadeIn();
  }

  // ── 4. Nav init ────────────────────────────────────────────────────────────
  var navPh    = document.getElementById('nav-placeholder');
  var footerPh = document.getElementById('footer-placeholder');

  var navIsInlined    = navPh    && navPh.dataset.inlined    === 'true';
  var footerIsInlined = footerPh && footerPh.dataset.inlined === 'true';

  if (navIsInlined) {
    // ── INLINED mode: nav already in DOM, just wire it up ──────────────────
    document.addEventListener('DOMContentLoaded', function () {
      setActiveItem(currentPage);
      initNav();
    });
  } else {
    // ── FETCH mode: dev / file:// fallback ─────────────────────────────────
    fetch('_nav.html')
      .then(function (r) { return r.text(); })
      .then(function (html) {
        if (navPh) { navPh.outerHTML = html; }
        else { document.body.insertAdjacentHTML('afterbegin', html); }
        setActiveItem(currentPage);
        initNav();
      })
      .catch(function (e) {
        console.warn('[nav-loader] _nav.html not loaded (file:// or network error).', e);
      });
  }

  if (!footerIsInlined) {
    fetch('_footer.html')
      .then(function (r) { return r.text(); })
      .then(function (html) {
        if (footerPh) { footerPh.outerHTML = html; }
        else { document.body.insertAdjacentHTML('beforeend', html); }
      })
      .catch(function (e) {
        console.warn('[nav-loader] _footer.html not loaded (file:// or network error).', e);
      });
  }

  // ── 5. Mark current page active in mega menu ──────────────────────────────
  function setActiveItem(page) {
    document.querySelectorAll('a.mega-item[href]').forEach(function (a) {
      if (a.getAttribute('href').split('/').pop() === page) {
        a.classList.add('active');
      }
    });
  }

  // ── 6. Nav interaction ────────────────────────────────────────────────────
  function initNav() {

    var navEl = document.getElementById('nav');
    if (navEl) {
      window.addEventListener('scroll', function () {
        navEl.classList.toggle('scrolled', window.scrollY > 20);
      }, { passive: true });
    }

    var menuTriggers = document.querySelectorAll('[data-menu]');
    var menus        = document.querySelectorAll('.mega-menu');
    var closeTimeout = null;

    function openMenu(menuId) {
      clearTimeout(closeTimeout);
      menus.forEach(function (m) { m.classList.remove('active'); });
      var menu = document.getElementById('menu-' + menuId);
      if (menu) { menu.classList.add('active'); }
    }

    function scheduleClose() {
      closeTimeout = setTimeout(function () {
        menus.forEach(function (m) { m.classList.remove('active'); });
      }, 200);
    }

    menuTriggers.forEach(function (trigger) {
      trigger.addEventListener('mouseenter', function () { openMenu(trigger.dataset.menu); });
      trigger.addEventListener('mouseleave', scheduleClose);
    });

    menus.forEach(function (menu) {
      menu.addEventListener('mouseenter', function () { clearTimeout(closeTimeout); });
      menu.addEventListener('mouseleave', scheduleClose);
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-menu]') && !e.target.closest('.mega-menu')) {
        menus.forEach(function (m) { m.classList.remove('active'); });
      }
    });

    var hamburger = document.getElementById('hamburger-btn');
    var mobileNav = document.getElementById('mobile-nav');
    if (hamburger && mobileNav) {
      hamburger.addEventListener('click', function () {
        var isOpen = mobileNav.classList.toggle('open');
        hamburger.classList.toggle('open', isOpen);
        hamburger.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
    }
  }

})();
