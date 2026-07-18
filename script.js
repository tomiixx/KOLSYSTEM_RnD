/* ==========================================================================
   KOLSYSTEM Sp. z o.o. - script.js
   Nawigacja mobilna, scroll spy, animacje pojawiania, przycisk "na górę",
   walidacja formularza kontaktowego.
   ========================================================================== */

(function () {
  'use strict';

  /* Klasa .js na <html> - style ukrywające elementy przed animacją
     działają tylko wtedy, gdy JavaScript jest dostępny. */
  document.documentElement.classList.add('js');

  var prefersReducedMotion =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Nawigacja mobilna ---------- */

  var header = document.querySelector('.site-header');
  var navToggle = document.querySelector('.nav-toggle');
  var siteNav = document.getElementById('site-nav');

  function closeNav() {
    if (!siteNav.classList.contains('is-open')) return;
    siteNav.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
  }

  function openNav() {
    siteNav.classList.add('is-open');
    navToggle.setAttribute('aria-expanded', 'true');
  }

  if (navToggle && siteNav) {
    navToggle.addEventListener('click', function () {
      if (siteNav.classList.contains('is-open')) {
        closeNav();
      } else {
        openNav();
      }
    });

    /* Zamknij menu po wybraniu pozycji */
    siteNav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });

    /* Zamknij menu klawiszem Escape */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeNav();
        navToggle.focus();
      }
    });

    /* Zamknij menu po kliknięciu poza nagłówkiem */
    document.addEventListener('click', function (e) {
      if (!header.contains(e.target)) closeNav();
    });
  }

  /* ---------- Nagłówek: cień po przewinięciu + przycisk "na górę" ---------- */

  var toTop = document.getElementById('to-top');

  function onScroll() {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
    if (toTop) {
      toTop.classList.toggle('is-visible', window.scrollY > 600);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({
        top: 0,
        behavior: prefersReducedMotion ? 'auto' : 'smooth'
      });
    });
  }

  /* ---------- Scroll spy: podświetlanie aktywnej pozycji menu ---------- */

  var navLinks = document.querySelectorAll('.site-nav a[href^="#"]');
  var sections = [];

  navLinks.forEach(function (link) {
    var section = document.querySelector(link.getAttribute('href'));
    if (section) sections.push(section);
  });

  function setActiveLink(id) {
    navLinks.forEach(function (link) {
      link.classList.toggle('is-active', link.getAttribute('href') === '#' + id);
    });
  }

  if ('IntersectionObserver' in window && sections.length) {
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActiveLink(entry.target.id);
        });
      },
      { rootMargin: '-40% 0px -55% 0px' }
    );
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Animacje pojawiania się sekcji ---------- */

  var revealEls = document.querySelectorAll('[data-reveal]');

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -8% 0px' }
    );
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------- Rok w stopce ---------- */

  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- Zgoda na cookies i mapa Google ---------- */

  /* Jedyny własny plik cookie strony: zapamiętuje decyzję użytkownika.
     'all' = zgoda na treści zewnętrzne (mapa Google), 'necessary' = tylko
     niezbędne. Mapa ładowana jest wyłącznie po zgodzie (wymóg RODO/ePrivacy). */
  var CONSENT_COOKIE = 'ks_consent';
  var CONSENT_MAX_AGE = 60 * 60 * 24 * 180; /* 180 dni */

  var cookieBanner = document.getElementById('cookie-banner');
  var mapEmbed = document.getElementById('map-embed');

  function getConsent() {
    var match = document.cookie.match(
      new RegExp('(?:^|; )' + CONSENT_COOKIE + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : '';
  }

  function setConsent(value) {
    document.cookie = CONSENT_COOKIE + '=' + encodeURIComponent(value) +
      '; max-age=' + CONSENT_MAX_AGE + '; path=/; SameSite=Lax';
  }

  function loadMap() {
    if (!mapEmbed || mapEmbed.querySelector('iframe')) return;
    var iframe = document.createElement('iframe');
    iframe.src = mapEmbed.getAttribute('data-src');
    iframe.title = 'Mapa dojazdu - KOLSYSTEM Sp. z o.o., ul. Radockiego 76/8, 40-645 Katowice';
    iframe.loading = 'lazy';
    iframe.referrerPolicy = 'no-referrer-when-downgrade';
    iframe.allowFullscreen = true;
    mapEmbed.innerHTML = '';
    mapEmbed.appendChild(iframe);
  }

  function showBanner() {
    if (!cookieBanner) return;
    cookieBanner.hidden = false;
    requestAnimationFrame(function () {
      cookieBanner.classList.add('is-visible');
    });
  }

  function hideBanner() {
    if (!cookieBanner) return;
    cookieBanner.classList.remove('is-visible');
    cookieBanner.hidden = true;
  }

  if (cookieBanner) {
    var acceptBtn = document.getElementById('cookie-accept');
    var necessaryBtn = document.getElementById('cookie-necessary');
    var settingsBtn = document.getElementById('cookie-settings');
    var mapLoadBtn = document.getElementById('map-load-btn');

    if (acceptBtn) {
      acceptBtn.addEventListener('click', function () {
        setConsent('all');
        hideBanner();
        loadMap();
      });
    }

    if (necessaryBtn) {
      necessaryBtn.addEventListener('click', function () {
        setConsent('necessary');
        hideBanner();
      });
    }

    /* Zmiana decyzji w dowolnym momencie - link w stopce */
    if (settingsBtn) {
      settingsBtn.addEventListener('click', showBanner);
    }

    /* Wczytanie mapy z placeholdera = zgoda na treści zewnętrzne */
    if (mapLoadBtn) {
      mapLoadBtn.addEventListener('click', function () {
        setConsent('all');
        hideBanner();
        loadMap();
      });
    }

    var consent = getConsent();
    if (consent === 'all') {
      loadMap();
    } else if (!consent) {
      showBanner();
    }
  }

  /* ---------- Formularz kontaktowy ---------- */

  var form = document.getElementById('contact-form');

  if (form) {
    var successBox = document.getElementById('form-success');

    var fields = {
      name: {
        input: document.getElementById('f-name'),
        error: document.getElementById('err-name'),
        validate: function (value) {
          if (value.trim().length < 3) return 'Podaj imię i nazwisko.';
          return '';
        }
      },
      company: {
        input: document.getElementById('f-company'),
        error: document.getElementById('err-company'),
        validate: function () { return ''; } /* pole opcjonalne */
      },
      email: {
        input: document.getElementById('f-email'),
        error: document.getElementById('err-email'),
        validate: function (value) {
          if (!value.trim()) return 'Podaj adres e-mail.';
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value.trim())) {
            return 'Podaj poprawny adres e-mail.';
          }
          return '';
        }
      },
      phone: {
        input: document.getElementById('f-phone'),
        error: document.getElementById('err-phone'),
        validate: function (value) {
          if (!value.trim()) return ''; /* pole opcjonalne */
          if (!/^[+]?[\d\s\-()]{7,}$/.test(value.trim())) {
            return 'Podaj poprawny numer telefonu.';
          }
          return '';
        }
      },
      message: {
        input: document.getElementById('f-message'),
        error: document.getElementById('err-message'),
        validate: function (value) {
          if (value.trim().length < 10) {
            return 'Wpisz treść wiadomości (min. 10 znaków).';
          }
          return '';
        }
      },
      consent: {
        input: document.getElementById('f-consent'),
        error: document.getElementById('err-consent'),
        validate: function (_value, input) {
          if (!input.checked) return 'Zgoda jest wymagana do wysłania formularza.';
          return '';
        }
      }
    };

    function showError(field, message) {
      field.error.textContent = message;
      field.error.hidden = false;
      field.input.setAttribute('aria-invalid', 'true');
      field.input.setAttribute('aria-describedby', field.error.id);
    }

    function clearError(field) {
      field.error.textContent = '';
      field.error.hidden = true;
      field.input.removeAttribute('aria-invalid');
      field.input.removeAttribute('aria-describedby');
    }

    function validateField(field) {
      var message = field.validate(field.input.value || '', field.input);
      if (message) {
        showError(field, message);
        return false;
      }
      clearError(field);
      return true;
    }

    /* Czyszczenie błędu podczas poprawiania pola */
    Object.keys(fields).forEach(function (key) {
      var field = fields[key];
      var eventName = field.input.type === 'checkbox' ? 'change' : 'input';
      field.input.addEventListener(eventName, function () {
        if (field.input.getAttribute('aria-invalid')) validateField(field);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (successBox) successBox.hidden = true;

      var firstInvalid = null;
      Object.keys(fields).forEach(function (key) {
        var valid = validateField(fields[key]);
        if (!valid && !firstInvalid) firstInvalid = fields[key].input;
      });

      if (firstInvalid) {
        firstInvalid.focus();
        return;
      }

      /* Strona działa bez backendu, więc wiadomość trafia do klienta
         pocztowego użytkownika przez mailto:. Po podpięciu własnego
         endpointu wystarczy zastąpić poniższy blok wywołaniem fetch(). */
      var name = fields.name.input.value.trim();
      var company = fields.company.input.value.trim();
      var email = fields.email.input.value.trim();
      var phone = fields.phone.input.value.trim();
      var message = fields.message.input.value.trim();

      var subject = 'Zapytanie ze strony kolsystem.pl - ' +
        (company ? name + ' (' + company + ')' : name);

      var body =
        'Imię i nazwisko: ' + name + '\n' +
        (company ? 'Firma: ' + company + '\n' : '') +
        'E-mail: ' + email + '\n' +
        (phone ? 'Telefon: ' + phone + '\n' : '') +
        '\n' + message;

      window.location.href =
        'mailto:kontakt@kolsystem.pl' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);

      if (successBox) {
        successBox.hidden = false;
        successBox.scrollIntoView({
          behavior: prefersReducedMotion ? 'auto' : 'smooth',
          block: 'nearest'
        });
      }
      form.reset();
    });
  }
})();
