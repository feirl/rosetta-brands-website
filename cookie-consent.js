/**
 * cookie-consent.js — Rosetta Brands
 * Manages GDPR cookie consent: Essential / Analytics / Advertising
 *
 * HOW TO GATE A SCRIPT:
 *   Change <script src="..."> to <script type="text/plain" data-consent="analytics" src="...">
 *   or for inline scripts: <script type="text/plain" data-consent="advertising">...</script>
 *   This prevents the browser executing them until consent is granted.
 *   On consent, this module swaps type back to text/javascript and re-injects.
 *
 * STORAGE KEY: rosetta_consent  (JSON in localStorage)
 * SCHEMA: { version, essential, analytics, advertising, timestamp }
 */

(function () {
  'use strict';

  var STORAGE_KEY   = 'rosetta_consent';
  var CONSENT_VER   = '1';

  /* ─── Helpers ──────────────────────────────────────────────────── */

  function getConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (obj.version !== CONSENT_VER) return null;
      return obj;
    } catch (e) { return null; }
  }

  function saveConsent(prefs) {
    var obj = {
      version:     CONSENT_VER,
      essential:   true,
      analytics:   !!prefs.analytics,
      advertising: !!prefs.advertising,
      timestamp:   new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(obj));
    return obj;
  }

  /* ─── Script activation ─────────────────────────────────────────── */

  function activateScripts(consent) {
    var gated = document.querySelectorAll('script[type="text/plain"][data-consent]');
    for (var i = 0; i < gated.length; i++) {
      var orig     = gated[i];
      var category = orig.getAttribute('data-consent');
      if (!consent[category]) continue;

      var s = document.createElement('script');
      var attrs = orig.attributes;
      for (var j = 0; j < attrs.length; j++) {
        var a = attrs[j];
        if (a.name === 'type' || a.name === 'data-consent') continue;
        s.setAttribute(a.name, a.value);
      }
      s.type = 'text/javascript';
      if (orig.src) {
        s.src = orig.src;
      } else {
        s.textContent = orig.textContent;
      }
      orig.parentNode.replaceChild(s, orig);
    }
  }

  /* ─── Banner / Modal visibility ────────────────────────────────── */

  function show(el)  { if (el) el.style.display = 'flex'; }
  function hide(el)  { if (el) el.style.display = 'none'; }

  function openModal() {
    var consent = getConsent();
    var analyticsBox    = document.getElementById('rc-analytics');
    var advertisingBox  = document.getElementById('rc-advertising');
    if (analyticsBox)   analyticsBox.checked   = consent ? !!consent.analytics   : false;
    if (advertisingBox) advertisingBox.checked  = consent ? !!consent.advertising : false;
    show(document.getElementById('rc-overlay'));
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    hide(document.getElementById('rc-overlay'));
    document.body.style.overflow = '';
  }

  function hideBanner() {
    hide(document.getElementById('rc-banner'));
  }

  /* ─── Actions ───────────────────────────────────────────────────── */

  function acceptAll() {
    var consent = saveConsent({ analytics: true, advertising: true });
    activateScripts(consent);
    hideBanner();
    closeModal();
  }

  function savePreferences() {
    var consent = saveConsent({
      analytics:   document.getElementById('rc-analytics')   ? document.getElementById('rc-analytics').checked   : false,
      advertising: document.getElementById('rc-advertising') ? document.getElementById('rc-advertising').checked : false
    });
    activateScripts(consent);
    hideBanner();
    closeModal();
  }

  /* ─── Wire up ───────────────────────────────────────────────────── */

  function bindButtons() {
    var b;
    b = document.getElementById('rc-accept-all');     if (b) b.addEventListener('click', acceptAll);
    b = document.getElementById('rc-accept-all-2');   if (b) b.addEventListener('click', acceptAll);
    b = document.getElementById('rc-manage');         if (b) b.addEventListener('click', openModal);
    b = document.getElementById('rc-save');           if (b) b.addEventListener('click', savePreferences);
    b = document.getElementById('rc-close');          if (b) b.addEventListener('click', closeModal);

    var overlay = document.getElementById('rc-overlay');
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeModal();
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
    });
  }

  /* ─── Init ──────────────────────────────────────────────────────── */

  function init() {
    var consent = getConsent();
    if (consent) {
      // Already consented — silently activate scripts, no banner
      activateScripts(consent);
    } else {
      // First visit — show banner
      show(document.getElementById('rc-banner'));
    }
    bindButtons();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose globally so the "Change cookie preferences" link in footer can call openModal()
  window.rosettaOpenCookieModal = openModal;

})();
