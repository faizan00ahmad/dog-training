/*
 * Paws & Path: Google tag (GA4 + Google Ads) and Meta Pixel with Consent Mode v2.
 *
 * Set the real IDs in build.py (TRACKING section), then run `python build.py`.
 * They reach this file through window.PP_CONFIG, written into every page <head>.
 * Until real IDs are set nothing is sent anywhere, and the consent banner stays hidden.
 *
 * Behaviour
 *  - Consent Mode v2 defaults to DENIED for ads and analytics before any tag loads.
 *  - Visitor choice is saved in localStorage ("pp-consent") and can be changed from the
 *    "Cookie settings" link in the footer.
 *  - Meta Pixel: consent is revoked until granted. PageView fires on load.
 *  - Events (sent to GA4 and Meta where relevant):
 *      Lead          lead form submitted (both Meta standard event and GA4 generate_lead)
 *      Contact       phone or email link clicked
 *      ViewContent   service or blog page viewed
 *      scroll_75     75% scroll depth on blog posts
 *  - Lead events carry an event_id so a server-side Conversions API call can deduplicate.
 */
(function () {
  'use strict';

  var CFG = window.PP_CONFIG || {};
  var isReal = function (v) { return !!v && !/YOUR_|XXXX|^$/.test(v); };
  var hasMeta = isReal(CFG.META_PIXEL_ID);
  var hasGA = isReal(CFG.GA4_ID);
  var hasAds = isReal(CFG.GADS_ID);
  var anyTracking = hasMeta || hasGA || hasAds;

  // ---- Google tag with Consent Mode v2 (defaults must be set before gtag.js loads) ----
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    wait_for_update: 500
  });
  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', true);

  var stored = null;
  try { stored = localStorage.getItem('pp-consent'); } catch (e) {}

  function setConsent(state) {
    var v = state === 'granted' ? 'granted' : 'denied';
    gtag('consent', 'update', {
      ad_storage: v, ad_user_data: v, ad_personalization: v, analytics_storage: v
    });
    if (hasMeta && window.fbq) { window.fbq('consent', v === 'granted' ? 'grant' : 'revoke'); }
    try { localStorage.setItem('pp-consent', v); } catch (e) {}
  }

  if (stored === 'granted' || stored === 'denied') {
    gtag('consent', 'update', {
      ad_storage: stored, ad_user_data: stored, ad_personalization: stored, analytics_storage: stored
    });
  }

  if (hasGA || hasAds) {
    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(hasGA ? CFG.GA4_ID : CFG.GADS_ID);
    document.head.appendChild(g);
    gtag('js', new Date());
    if (hasGA) { gtag('config', CFG.GA4_ID, { anonymize_ip: true }); }
    if (hasAds) { gtag('config', CFG.GADS_ID); }
  }

  // ---- Meta Pixel ----
  if (hasMeta) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('consent', stored === 'granted' ? 'grant' : 'revoke');
    window.fbq('init', CFG.META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }

  // ---- Shared event helper ----
  function uid() {
    return 'pp-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  }
  window.ppTrack = function (name, params) {
    params = params || {};
    var id = uid();
    if (hasMeta && window.fbq) {
      var standard = { Lead: 1, Contact: 1, ViewContent: 1, Schedule: 1 };
      window.fbq(standard[name] ? 'track' : 'trackCustom', name, params, { eventID: id });
    }
    if (hasGA || hasAds) {
      var map = { Lead: 'generate_lead', Contact: 'contact', ViewContent: 'view_item' };
      gtag('event', map[name] || name, Object.assign({ event_id: id }, params));
      if (name === 'Lead' && hasAds && CFG.GADS_LEAD_LABEL) {
        gtag('event', 'conversion', { send_to: CFG.GADS_ID + '/' + CFG.GADS_LEAD_LABEL });
      }
      if (name === 'Contact' && hasAds && CFG.GADS_CALL_LABEL) {
        gtag('event', 'conversion', { send_to: CFG.GADS_ID + '/' + CFG.GADS_CALL_LABEL });
      }
    }
    return id;
  };

  document.addEventListener('DOMContentLoaded', function () {
    var body = document.body;
    var type = body.getAttribute('data-page-type');
    var title = body.getAttribute('data-page-title') || document.title;

    if (type === 'service' || type === 'blog') {
      window.ppTrack('ViewContent', { content_name: title, content_category: type });
    }

    // Phone and email clicks
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
      if (!a) return;
      window.ppTrack('Contact', { method: a.href.indexOf('tel:') === 0 ? 'phone' : 'email', page: location.pathname });
    });

    // Scroll depth on blog posts
    if (type === 'blog') {
      var fired = false;
      window.addEventListener('scroll', function () {
        if (fired) return;
        var h = document.documentElement;
        var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight;
        if (pct > 0.75) { fired = true; window.ppTrack('scroll_75', { content_name: title }); }
      }, { passive: true });
    }

    // ---- Consent banner (only when tracking is configured and no choice is stored yet) ----
    var banner = document.createElement('div');
    banner.className = 'consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie preferences');
    banner.innerHTML =
      '<p>We use cookies to measure visits and show relevant ads. You choose. See our <a href="/privacy/">privacy policy</a>.</p>' +
      '<div class="btns"><button type="button" class="btn btn-primary btn-sm" data-c="granted">Accept</button>' +
      '<button type="button" class="btn btn-glass btn-sm" data-c="denied">Decline</button></div>';
    document.body.appendChild(banner);
    banner.addEventListener('click', function (e) {
      var c = e.target.getAttribute && e.target.getAttribute('data-c');
      if (!c) return;
      setConsent(c);
      banner.classList.remove('show');
    });
    if (anyTracking && !stored) { banner.classList.add('show'); }

    var reopen = document.querySelectorAll('[data-cookie-settings]');
    for (var i = 0; i < reopen.length; i++) {
      reopen[i].addEventListener('click', function (e) { e.preventDefault(); banner.classList.add('show'); });
    }
  });
})();
