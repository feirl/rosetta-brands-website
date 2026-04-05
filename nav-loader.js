/**
 * nav-loader.js — Rosetta Brands
 * Fetches _nav.html and _footer.html, injects them, wires all nav behaviour,
 * and sets the active mega-menu item based on the current page.
 *
 * The fade-in observer is intentionally decoupled from the fetch so that
 * page content is always visible — including on file:// for local preview.
 * For full nav/footer locally, serve via: python3 -m http.server
 */
(function () {

  var currentPage = window.location.pathname.split('/').pop() || 'index.html';

  // ── 1. Fade-in — always runs, regardless of fetch success ─────────────────
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

  // ── 2. Inject nav ──────────────────────────────────────────────────────────
  fetch('_nav.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var ph = document.getElementById('nav-placeholder');
      if (ph) { ph.outerHTML = html; } else { document.body.insertAdjacentHTML('afterbegin', html); }
      setActiveItem(currentPage);
      initNav();
    })
    .catch(function (e) {
      console.warn('[nav-loader] _nav.html not loaded (file:// restriction or network error).', e);
    });

  // ── 3. Inject footer ───────────────────────────────────────────────────────
  fetch('_footer.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var ph = document.getElementById('footer-placeholder');
      if (ph) { ph.outerHTML = html; } else { document.body.insertAdjacentHTML('beforeend', html); }
    })
    .catch(function (e) {
      console.warn('[nav-loader] _footer.html not loaded (file:// restriction or network error).', e);
    });

  // ── 4. Mark the current page active in the mega menu ──────────────────────
  function setActiveItem(page) {
    document.querySelectorAll('a.mega-item[href]').forEach(function (a) {
      if (a.getAttribute('href').split('/').pop() === page) {
        a.classList.add('active');
      }
    });
  }

  // ── 5. Nav interaction (runs after nav HTML is in the DOM) ────────────────
  function initNav() {

    // Scroll shadow on nav bar
    var navEl = document.getElementById('nav');
    if (navEl) {
      window.addEventListener('scroll', function () {
        navEl.classList.toggle('scrolled', window.scrollY > 20);
      }, { passive: true });
    }

    // Mega menu open/close via data-menu triggers
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

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-menu]') && !e.target.closest('.mega-menu')) {
        menus.forEach(function (m) { m.classList.remove('active'); });
      }
    });

    // Hamburger / mobile nav
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
