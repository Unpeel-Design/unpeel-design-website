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
  e.currentTarget.innerHTML = '<p style="color:rgba(255,255,255,.5);font-size:14px;padding:8px 0;">Thanks, you\'re on the list.</p>';
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
  /* scroll-based visibility, started only after webfonts are ready: the async bold-700 swap
     must not interrupt the reveal transition (an IntersectionObserver was getting toggled by
     the font reflow and leaving transitions stuck) */
  function inView(el) {
    var r = el.getBoundingClientRect(), vh = window.innerHeight || document.documentElement.clientHeight;
    return r.top < vh * 0.9 && r.bottom > vh * 0.1;
  }
  function update() {
    for (var i = 0; i < titles.length; i++) titles[i].classList.toggle('is-in', inView(titles[i]));
  }
  var ticking = false;
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; update(); }); }
  }
  var started = false;
  function start() {
    if (started) return; started = true;
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start);
  setTimeout(start, 1200);   /* fallback so titles never stay hidden if fonts are slow/blocked */
})();


/* ═══ FILM GRAIN: static fine grain overlay with dust specks and soft defocused blobs across the whole site ═══ */
(function () {
  if (document.getElementById('film-grain')) return;

  /* deterministic PRNG (mulberry32) so the texture is stable, not flickering */
  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  /* the overlay element: top-most layer, never blocks clicks, static */
  var o = document.createElement('div');
  o.id = 'film-grain';
  o.setAttribute('aria-hidden', 'true');
  o.style.cssText =
    'position:fixed;inset:0;pointer-events:none;z-index:2147483647;' +
    'opacity:0.3;background-repeat:no-repeat;background-size:cover;';
  (document.body || document.documentElement).appendChild(o);

  /* build a full-viewport SVG: a fine neutral film grain (kept light), then
     scattered dust specks and a few soft defocused blobs on top. specks and
     blobs mix light and dark so they read on white AND on dark areas
     (images, footer). plain normal blend at low master opacity. */
  function build() {
    var W = Math.max(window.innerWidth || 0, document.documentElement.clientWidth || 0,
                     (window.visualViewport && window.visualViewport.width) || 0);
    var H = Math.max(window.innerHeight || 0, document.documentElement.clientHeight || 0,
                     (window.visualViewport && window.visualViewport.height) || 0);
    /* guard against a browser reporting a degenerate viewport size */
    if (W < 360) W = (window.screen && window.screen.width) || 1440;
    if (H < 360) H = (window.screen && window.screen.height) || 900;
    var r = rng(20240607);                 /* fixed seed: same look every load */
    var area = W * H;
    var p = [];

    /* fine neutral film grain, kept light (rect opacity below master). forced
       opaque + desaturated so its strength is predictable. */
    p.push("<filter id='fgN'>"
         + "<feTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/>"
         + "<feColorMatrix type='saturate' values='0'/>"
         + "<feComponentTransfer><feFuncA type='discrete' tableValues='1'/></feComponentTransfer>"
         + "</filter>");
    /* soft blur for the defocused dust blobs */
    p.push("<filter id='fgB' x='-60%' y='-60%' width='220%' height='220%'><feGaussianBlur stdDeviation='3.6'/></filter>");
    p.push("<rect width='" + W + "' height='" + H + "' filter='url(#fgN)' opacity='0.5'/>");

    /* scattered dust specks, mix of light and dark so they read everywhere */
    var dust = Math.round(area / 28000);
    for (var i = 0; i < dust; i++) {
      var x = (r() * W).toFixed(1), y = (r() * H).toFixed(1);
      var rad = (0.4 + r() * r() * 1.9).toFixed(2);    /* mostly small, a few brighter dots */
      var light = r() < 0.58;
      var op = (0.35 + r() * 0.55).toFixed(2);
      p.push("<circle cx='" + x + "' cy='" + y + "' r='" + rad + "' fill='" + (light ? '#fff' : '#111') + "' opacity='" + op + "'/>");
    }

    /* a few soft defocused blobs (out-of-focus dust): mostly light, and any
       dark ones kept very faint so they never read as smudges on white */
    var blobs = Math.max(4, Math.round(area / 230000));
    for (i = 0; i < blobs; i++) {
      var bx = (r() * W).toFixed(1), by = (r() * H).toFixed(1);
      var brad = (6 + r() * 18).toFixed(1);
      var bl = r() < 0.75;
      var bop = (bl ? (0.12 + r() * 0.18) : (0.05 + r() * 0.06)).toFixed(2);
      p.push("<circle cx='" + bx + "' cy='" + by + "' r='" + brad + "' fill='" + (bl ? '#fff' : '#111') + "' opacity='" + bop + "' filter='url(#fgB)'/>");
    }

    var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='" + W + "' height='" + H + "'>" + p.join('') + "</svg>";
    o.style.backgroundImage = 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '")';
  }

  build();
  /* regenerate on resize (debounced) so the texture always fills the viewport */
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(build, 200); }, { passive: true });
})();
