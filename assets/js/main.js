/* Saravana Perumal R, site script. Small and dependency free. */
(function () {
  'use strict';

  var doc = document;
  doc.documentElement.classList.add('js');

  /* ---------- Mobile navigation ---------- */
  var toggle = doc.querySelector('.nav-toggle');
  var nav = doc.getElementById('site-nav');

  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setNav(false);
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 1200px)').addEventListener('change', function (mq) {
      if (mq.matches) setNav(false);
    });
  }

  /* ---------- Header border once the page scrolls ---------- */
  var header = doc.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- FAQPage JSON-LD, built from the visible FAQ ----------
     The answers on the page are the single source of truth, so the
     structured data can never drift from what visitors read. */
  var faqItems = doc.querySelectorAll('[data-faq-item]');
  if (faqItems.length) {
    var clean = function (s) { return s.replace(/\s+/g, ' ').trim(); };
    var schema = {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: Array.prototype.map.call(faqItems, function (item) {
        return {
          '@type': 'Question',
          name: clean(item.querySelector('[data-faq-q]').textContent),
          acceptedAnswer: {
            '@type': 'Answer',
            text: clean(item.querySelector('[data-faq-a]').textContent)
          }
        };
      })
    };
    var tag = doc.createElement('script');
    tag.type = 'application/ld+json';
    tag.id = 'faq-schema';
    tag.textContent = JSON.stringify(schema);
    doc.head.appendChild(tag);
  }

  /* ---------- Highlight the nav link for the section in view ---------- */
  var sectionLinks = doc.querySelectorAll('.site-nav a[href^="#"]');
  if ('IntersectionObserver' in window && sectionLinks.length) {
    var byId = {};
    sectionLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          sectionLinks.forEach(function (a) { a.classList.remove('is-active'); });
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) {
      var el = doc.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* ---------- Gentle reveal on scroll ---------- */
  var reveals = doc.querySelectorAll('.reveal');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduce) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Contact form: no server, so it hands off to WhatsApp or email ---------- */
  var form = doc.getElementById('enquiry-form');
  if (form) {
    var compose = function () {
      var get = function (name) { return (form.elements[name].value || '').trim(); };
      var lines = ['Hi Saravana, I\'m ' + get('name') + '.'];
      if (get('interest')) lines.push('Interested in: ' + get('interest'));
      if (get('organisation')) lines.push('Organisation: ' + get('organisation'));
      if (get('city')) lines.push('City: ' + get('city'));
      if (get('size')) lines.push('Group size: ' + get('size'));
      if (get('goal')) lines.push('Goal: ' + get('goal'));
      return lines.join('\n');
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      window.open('https://wa.me/917012753018?text=' + encodeURIComponent(compose()), '_blank', 'noopener');
    });

    var emailBtn = doc.getElementById('enquiry-email');
    if (emailBtn) {
      emailBtn.addEventListener('click', function () {
        if (!form.reportValidity()) return;
        var subject = 'AI training enquiry' + (form.elements.interest.value ? ': ' + form.elements.interest.value : '');
        window.location.href = 'mailto:saravanaperumalr14@gmail.com?subject=' +
          encodeURIComponent(subject) + '&body=' + encodeURIComponent(compose());
      });
    }
  }

  /* ---------- Career timeline: move "now" and the ongoing role to today ----------
     The HTML ships with positions computed for the build date, so it reads
     correctly without JS; this keeps them current. */
  var gantt = doc.querySelector('[data-gantt]');
  if (gantt) {
    var startParts = (gantt.getAttribute('data-start') || '2017-01').split('-');
    var totalMonths = parseFloat(gantt.getAttribute('data-months')) || 132;
    var today = new Date();
    var monthsIn = (today.getFullYear() - parseInt(startParts[0], 10)) * 12 +
      (today.getMonth() - (parseInt(startParts[1], 10) - 1)) + today.getDate() / 31;
    var nowPct = Math.max(0, Math.min(100, (monthsIn / totalMonths) * 100));
    gantt.style.setProperty('--now', nowPct.toFixed(2) + '%');
    gantt.querySelectorAll('[data-ongoing]').forEach(function (track) {
      track.style.setProperty('--e', nowPct.toFixed(2) + '%');
    });
  }

  /* ---------- Homepage thought blobs: tap to open (touch screens have no hover) ---------- */
  var blobs = doc.querySelectorAll('[data-blob]');
  blobs.forEach(function (blob) {
    blob.addEventListener('click', function () {
      var open = !blob.classList.contains('is-open');
      blobs.forEach(function (b) { b.classList.remove('is-open'); });
      blob.classList.toggle('is-open', open);
    });
    blob.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); blob.click(); }
      if (e.key === 'Escape') { blob.classList.remove('is-open'); blob.blur(); }
    });
  });

  /* ---------- Hero crane jar: each crane unfolds into a learner's note ----------
     Notes live in <template id="crane-notes"> in index.html (real reviews only). */
  var craneDialog = doc.getElementById('crane-note');
  var craneSpots = doc.querySelectorAll('.crane-spot');
  if (craneDialog && craneSpots.length) {
    var noteTpl = doc.getElementById('crane-notes');
    var notes = noteTpl ? Array.prototype.slice.call(noteTpl.content.querySelectorAll('blockquote')) : [];
    var paper = craneDialog.querySelector('.crane-paper');
    var textEl = craneDialog.querySelector('.crane-text p');
    var whoEl = craneDialog.querySelector('.crane-who');
    var lastSpot = null;

    var openNote = function (spot) {
      var i = parseInt(spot.getAttribute('data-crane'), 10) || 0;
      paper.style.setProperty('--paper', spot.getAttribute('data-color') || '#F6D06E');
      whoEl.textContent = '';
      if (notes.length) {
        var note = notes[i % notes.length];
        textEl.textContent = note.textContent.replace(/\s+/g, ' ').trim();
        var name = note.getAttribute('data-name'), role = note.getAttribute('data-role');
        if (name) { var b = doc.createElement('strong'); b.textContent = name; whoEl.appendChild(b); }
        if (role) { whoEl.appendChild(doc.createTextNode(role)); }
      } else {
        textEl.textContent = 'Notes from my learners are being folded into this jar. Check back soon.';
      }
      lastSpot = spot;
      if (typeof craneDialog.showModal === 'function') { craneDialog.showModal(); } else { craneDialog.setAttribute('open', ''); }
    };
    var closeNote = function () {
      if (typeof craneDialog.close === 'function') { craneDialog.close(); } else { craneDialog.removeAttribute('open'); }
    };
    craneSpots.forEach(function (spot) { spot.addEventListener('click', function () { openNote(spot); }); });
    craneDialog.querySelector('.crane-close').addEventListener('click', closeNote);
    craneDialog.addEventListener('click', function (e) { if (e.target === craneDialog) { closeNote(); } });
    craneDialog.addEventListener('close', function () { if (lastSpot) { lastSpot.focus(); } });
  }

  /* ---------- Footer year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
