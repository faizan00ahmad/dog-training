(function () {
  'use strict';
  var root = document.documentElement;

  // ---- Theme: light by default, choice remembered on this device ----
  var themeBtn = document.getElementById('themeBtn');
  var moon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.7 6.7 0 0 0 9.8 9.8z"/></svg>';
  var sun = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  function applyTheme(mode) {
    root.setAttribute('data-theme', mode);
    if (!themeBtn) return;
    themeBtn.innerHTML = mode === 'dark' ? sun : moon;
    var next = mode === 'dark' ? 'light' : 'dark';
    themeBtn.setAttribute('aria-label', 'Switch to ' + next + ' mode');
    themeBtn.title = 'Switch to ' + next + ' mode';
  }
  var saved = null;
  try { saved = localStorage.getItem('pp-theme'); } catch (e) {}
  applyTheme(saved === 'dark' ? 'dark' : 'light');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('pp-theme', next); } catch (e) {}
    });
  }

  // ---- Mobile menu ----
  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menuBtn.textContent = open ? '✕' : '☰';
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.textContent = '☰';
      });
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // ---- Seamless loops: ticker and video reel ----
  function loopify(trackId, wrapperId) {
    var track = document.getElementById(trackId);
    if (!track) return;
    Array.prototype.slice.call(track.children).forEach(function (el) {
      var c = el.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.querySelectorAll('video').forEach(function (v) { v.muted = true; v.setAttribute('tabindex', '-1'); });
      track.appendChild(c);
    });
    if (wrapperId) { var w = document.getElementById(wrapperId); if (w) w.classList.add('is-ready'); }
  }
  loopify('tickerTrack');
  loopify('reelTrack', 'reel');

  // ---- Lead forms (front-end only: connect to a scheduler or form service) ----
  document.querySelectorAll('form.lead-form').forEach(function (form) {
    var msg = form.querySelector('.note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var invalid = Array.prototype.slice.call(form.querySelectorAll('[required]')).find(function (f) { return !f.value.trim(); });
      if (invalid) {
        msg.textContent = 'Please complete the highlighted fields so we can reach you.';
        msg.style.color = '#b3261e';
        invalid.focus();
        return;
      }
      var need = form.querySelector('[name="need"]');
      if (window.ppTrack) {
        window.ppTrack('Lead', {
          content_name: need ? need.value : 'consultation',
          content_category: 'dog_training',
          page: location.pathname
        });
      }
      msg.style.color = '';
      msg.textContent = "Thank you! We'll be in touch within one business day.";
      form.reset();
    });
  });

  // ---- Hide the mobile call bar while a booking form is on screen ----
  var callBar = document.getElementById('callBar');
  var book = document.getElementById('book');
  if (callBar && book && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      callBar.style.display = entries[0].isIntersecting ? 'none' : '';
    }, { threshold: 0.2 }).observe(book);
  }
})();
