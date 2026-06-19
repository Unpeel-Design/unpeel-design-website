/* ═══════════════════════════════════════
   Unpeel Design — script v2
   ═══════════════════════════════════════ */

/* ═══ TOUCH DETECTION + CURSOR ═══ */
const isTouch = window.matchMedia('(hover: none)').matches;
const cursor  = document.getElementById('cursor');
let mx = 0, my = 0, cx = 0, cy = 0;

if (!isTouch) {
  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
  (function tick() {
    cx += (mx - cx) * 0.15;
    cy += (my - cy) * 0.15;
    cursor.style.left = cx + 'px';
    cursor.style.top  = cy + 'px';
    requestAnimationFrame(tick);
  })();
  function addHover(sel) {
    document.querySelectorAll(sel).forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
  }
  addHover('a, button, .work-card, .faq-q, .review-card, .lp-btn, .pkg-card');
}

/* ═══ NAV SCROLL BORDER ═══ */
const mainNav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  mainNav.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

/* ═══ MOBILE NAV ═══ */
const mobOverlay = document.getElementById('mobOverlay');
document.getElementById('hamburger').addEventListener('click', () => mobOverlay.classList.add('open'));
document.getElementById('mobClose').addEventListener('click',  () => mobOverlay.classList.remove('open'));
mobOverlay.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobOverlay.classList.remove('open')));



/* ═══ SCROLL REVEAL ═══ */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
document.querySelectorAll('.fade-up').forEach(el => revealObs.observe(el));

/* ═══ WORK CARD VIDEOS ═══ */
const worksEl = document.getElementById('works');
document.querySelectorAll('.work-card').forEach(card => {
  const v = card.querySelector('video');
  if (!v) return;
  card.addEventListener('mouseenter', () => {
    if (!worksEl || worksEl.dataset.video !== 'a') v.play().catch(() => {});
  });
  card.addEventListener('mouseleave', () => {
    if (!worksEl || worksEl.dataset.video !== 'a') { v.pause(); v.currentTime = 0; }
  });
});

/* ═══ SERVICES ACCORDION ═══ */
const accItems = Array.from(document.querySelectorAll('.acc-item'));
accItems.forEach(item => {
  const header = item.querySelector('.acc-header');
  header.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    accItems.forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

if (!isTouch) {
  addHover('.acc-header');
}

/* ═══ REVIEWS — multi-card carousel ═══ */
const reviewsWindow = document.getElementById('reviewsWindow');
const reviewsTrack  = document.getElementById('reviewsTrack');
const reviewCards   = Array.from(document.querySelectorAll('.review-card'));
const rDotsWrap     = document.getElementById('rDots');
let reviewPage = 0, reviewTimer;

function getPerPage() {
  if (window.innerWidth < 768)  return 1;
  if (window.innerWidth < 1100) return 2;
  return 3;
}

function buildDots(total) {
  rDotsWrap.innerHTML = '';
  for (let i = 0; i < total; i++) {
    const d = document.createElement('button');
    d.className = 'r-dot' + (i === reviewPage ? ' active' : '');
    d.setAttribute('aria-label', 'Group ' + (i + 1));
    d.addEventListener('click', () => { stopReviews(); goReview(i); startReviews(); });
    rDotsWrap.appendChild(d);
  }
}

function goReview(page, animated) {
  if (animated === undefined) animated = true;
  const pp    = getPerPage();
  const total = Math.ceil(reviewCards.length / pp);
  reviewPage  = ((page % total) + total) % total;

  const gap   = 24;
  const cardW = reviewCards[0] ? reviewCards[0].offsetWidth : 0;
  const offset = reviewPage * pp * (cardW + gap);

  reviewsTrack.style.transition = animated ? 'transform 400ms ease' : 'none';
  reviewsTrack.style.transform  = `translateX(-${offset}px)`;

  rDotsWrap.querySelectorAll('.r-dot').forEach((d, i) => d.classList.toggle('active', i === reviewPage));
}

function initReviews() {
  if (!reviewsWindow) return;
  const pp  = getPerPage();
  const gap = 24;
  const w   = reviewsWindow.offsetWidth;
  if (!w) return;
  const cardW = Math.floor((w - (pp - 1) * gap) / pp);
  reviewCards.forEach(c => { c.style.width = cardW + 'px'; c.style.minWidth = cardW + 'px'; });
  buildDots(Math.ceil(reviewCards.length / pp));
  goReview(reviewPage, false);
}

function startReviews() { reviewTimer = setInterval(() => goReview(reviewPage + 1), 6000); }
function stopReviews()  { clearInterval(reviewTimer); }

if (reviewsWindow) {
  document.getElementById('rPrev').addEventListener('click', () => { stopReviews(); goReview(reviewPage - 1); startReviews(); });
  document.getElementById('rNext').addEventListener('click', () => { stopReviews(); goReview(reviewPage + 1); startReviews(); });
  reviewsWindow.addEventListener('mouseenter', stopReviews);
  reviewsWindow.addEventListener('mouseleave', startReviews);
  window.addEventListener('resize', initReviews);
}

/* ═══ FAQ ═══ */
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
});

/* ═══ CONTACT FORM — Formspree ═══ */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var btn = form.querySelector('.c-submit');
    var originalText = btn ? btn.textContent : '';
    if (btn) { btn.textContent = 'Sending…'; btn.disabled = true; }

    /* Remove any previous error */
    var prevErr = form.querySelector('.c-form-error');
    if (prevErr) prevErr.remove();

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    })
    .then(function (res) {
      if (res.ok) {
        /* Success — hide form, show success message */
        form.style.display = 'none';
        var success = document.getElementById('formSuccess');
        if (success) { success.style.display = 'flex'; }
      } else {
        /* Formspree returned an error */
        throw new Error('form_error');
      }
    })
    .catch(function () {
      /* Network error or Formspree error — show inline message */
      if (btn) { btn.textContent = originalText; btn.disabled = false; }
      var err = document.createElement('p');
      err.className = 'c-form-error';
      err.style.cssText = 'font-size:13px;color:#c0392b;margin-top:12px;line-height:1.6;';
      err.innerHTML = 'Something went wrong. Please email me directly at <a href="mailto:design.arnaudboone@gmail.com" style="color:inherit;text-decoration:underline;">design.arnaudboone@gmail.com</a>';
      form.appendChild(err);
    });
  });
})();

/* ═══ NEWSLETTER ═══ */
document.getElementById('newsForm').addEventListener('submit', e => {
  e.preventDefault();
  e.currentTarget.innerHTML = '<p style="color:rgba(255,255,255,.5);font-size:14px;padding:8px 0;">Thanks — you\'re on the list.</p>';
});

/* ═══ LAYOUT PANEL ═══ */
function applyLayout(target, val) {
  switch (target) {
    case 'hero': { const el = document.getElementById('hero'); if (el) el.dataset.layout = val; break; }
    case 'about': { const el = document.getElementById('about'); if (el) el.dataset.layout = val; break; }
    case 'services': { const el = document.getElementById('services'); if (el) el.dataset.layout = val; break; }
    case 'works': { if (worksEl) worksEl.dataset.layout = val; break; }
    case 'footer': { const el = document.querySelector('footer'); if (el) el.dataset.layout = val; break; }
    case 'works-video':
      if (!worksEl) break;
      worksEl.dataset.video = val;
      if (val === 'a') {
        document.querySelectorAll('.work-card video').forEach(v => v.play().catch(() => {}));
      } else {
        document.querySelectorAll('.work-card video').forEach(v => { v.pause(); v.currentTime = 0; });
      }
      break;
  }
}

/* Layout panel moved to Tweaks — expose applyLayout globally */
window.applyLayout = applyLayout;

/* ═══ INIT ═══ */
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    if (reviewsWindow) {
      initReviews();
      startReviews();
    }
  });
});


/* ═══ TITLE MASK-REVEAL (per-line, replays each time in view) ═══ */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var SEL = '.hero-h1, .section-title, .statement-text, .page-h1, .cs-h1, .svcp-h1, .pkgp-h1, .pp-h1, .ct-h1, .app-h1, .ab-h1, .app-diff-heading, .ab-diff-heading, .svcp-cta-h, .pkgp-dark-cta-h, .app-dark-cta-h, .ab-cta-h';
  var titles = Array.prototype.slice.call(document.querySelectorAll(SEL));
  if (!titles.length) return;
  titles.forEach(function (el) {
    if (el.dataset.trReveal) return;
    el.dataset.trReveal = '1';
    /* drop the one-time hero entrance so only the mask reveal plays */
    el.className = el.className.replace(/\bhero-anim\b/g, '').replace(/\bha\d\b/g, '').replace(/\s+/g, ' ').trim();
    var lines = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = lines.map(function (ln) {
      return '<span class="tr-mask"><span class="tr-line">' + ln + '</span></span>';
    }).join('');
    el.classList.add('tr-reveal');
  });
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { e.target.classList.toggle('is-in', e.isIntersecting); });
  }, { threshold: 0.2 });
  titles.forEach(function (el) { obs.observe(el); });
})();
