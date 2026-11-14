(function () {
  var SITE = window.PUNARJANMA || {};
  var waBase = 'https://wa.me/' + (SITE.whatsapp || '');

  // Header: solid after the hero
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('solid', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      document.body.classList.toggle('menu-open', open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { btn.click(); btn.focus(); }
    });
  }

  // Photo slots: show the intended photo label until a real file is added
  document.querySelectorAll('.ph[data-src]').forEach(function (el) {
    var img = new Image();
    img.onerror = function () { el.classList.add('missing'); };
    img.src = el.getAttribute('data-src');
  });

  // WhatsApp links carry a pre-written message
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    a.href = waBase + '?text=' + encodeURIComponent(a.getAttribute('data-wa'));
    a.target = '_blank'; a.rel = 'noopener';
  });

  // Experience strip controls
  var strip = document.querySelector('.strip');
  document.querySelectorAll('[data-strip]').forEach(function (b) {
    b.addEventListener('click', function () {
      var dir = b.getAttribute('data-strip') === 'next' ? 1 : -1;
      strip.scrollBy({ left: dir * strip.clientWidth * 0.6, behavior: 'smooth' });
    });
  });

  // Gallery lightbox
  var dlg = document.querySelector('.lightbox');
  if (dlg) {
    var big = dlg.querySelector('.ph'), cap = dlg.querySelector('p');
    document.querySelectorAll('.mosaic button').forEach(function (b) {
      b.addEventListener('click', function () {
        var src = b.getAttribute('data-full');
        big.style.setProperty('--src', 'url(../' + src.replace(/^(\.\.\/)+/, '') + ')');
        big.setAttribute('data-label', b.getAttribute('data-caption'));
        big.classList.toggle('missing', b.querySelector('.ph').classList.contains('missing'));
        cap.textContent = b.getAttribute('data-caption');
        dlg.showModal();
      });
    });
    dlg.querySelector('.close').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }

  // Contact form → WhatsApp message
  var form = document.getElementById('enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (f) {
        var wrap = f.closest('.field'), bad = !f.value.trim();
        wrap.classList.toggle('invalid', bad);
        f.setAttribute('aria-invalid', bad);
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      var d = new FormData(form), lines = ['Hello Punarjanam,'];
      lines.push('I\'m ' + d.get('name') + '.');
      lines.push('I\'m interested in: ' + d.get('interest') + '.');
      if (d.get('dates')) lines.push('Dates: ' + d.get('dates'));
      if (d.get('people')) lines.push('People: ' + d.get('people'));
      if (d.get('message')) lines.push(d.get('message'));
      window.open(waBase + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }

  // Session videos: muted loops, paused for reduced-motion users, with a pause control
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var PLAY = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2l10 6-10 6z" fill="currentColor"/></svg>';
  var PAUSE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 2h4v12H3zM9 2h4v12H9z" fill="currentColor"/></svg>';
  document.querySelectorAll('.vid').forEach(function (box) {
    var v = box.querySelector('video'), b = box.querySelector('.vtoggle');
    function sync() { var p = v.paused; b.innerHTML = p ? PLAY : PAUSE; b.setAttribute('aria-label', p ? 'Play video' : 'Pause video'); }
    if (!still) { v.play().catch(function () {}); }
    v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
    b.addEventListener('click', function () { v.paused ? v.play() : v.pause(); });
  });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
