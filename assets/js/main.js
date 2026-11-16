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
    window.matchMedia('(min-width: 1100px)').addEventListener('change', function (mq) {
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

  /* ---------- Footer year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
