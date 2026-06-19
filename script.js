/* ===== CUSTOM CURSOR ===== */
const cursor = document.getElementById('cursor');
let mx = 0, my = 0, cx = 0, cy = 0;

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
addHover('a, button, .work-card, .faq-q, .svc-item, .r-dot, .r-arrow');

/* ===== NAV SCROLL BORDER ===== */
const mainNav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  mainNav.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

/* ===== MOBILE NAV ===== */
const mobOverlay = document.getElementById('mobOverlay');
document.getElementById('hamburger').addEventListener('click', () => mobOverlay.classList.add('open'));
document.getElementById('mobClose').addEventListener('click', () => mobOverlay.classList.remove('open'));
mobOverlay.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobOverlay.classList.remove('open')));

/* ===== SCROLL REVEAL ===== */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.14 });
document.querySelectorAll('.fade-up').forEach(el => revealObs.observe(el));

/* ===== WORK CARD VIDEOS ===== */
document.querySelectorAll('.work-card').forEach(card => {
  const v = card.querySelector('video');
  if (!v) return;
  card.addEventListener('mouseenter', () => v.play().catch(() => {}));
  card.addEventListener('mouseleave', () => { v.pause(); v.currentTime = 0; });
});

/* ===== SERVICES PANEL ===== */
const svcItems  = Array.from(document.querySelectorAll('.svc-item'));
const svcPanels = Array.from(document.querySelectorAll('.svc-panel'));

function activateSvc(idx) {
  svcItems.forEach(i  => i.classList.remove('active'));
  svcPanels.forEach(p => p.classList.remove('active'));
  svcItems[idx].classList.add('active');
  svcPanels[idx].classList.add('active');
}

svcItems.forEach((item, idx) => {
  item.addEventListener('click',      () => activateSvc(idx));
  item.addEventListener('mouseenter', () => activateSvc(idx));
});

/* ===== REVIEWS CAROUSEL ===== */
let cur = 0, autoTimer;
const slides = Array.from(document.querySelectorAll('.review-slide'));
const rDots  = Array.from(document.querySelectorAll('.r-dot'));

function showSlide(n) {
  cur = ((n % slides.length) + slides.length) % slides.length;
  slides.forEach(s => s.classList.remove('active'));
  rDots.forEach(d  => d.classList.remove('active'));
  slides[cur].classList.add('active');
  rDots[cur].classList.add('active');
}

function startAuto() { autoTimer = setInterval(() => showSlide(cur + 1), 5000); }
function stopAuto()  { clearInterval(autoTimer); }

document.getElementById('rPrev').addEventListener('click', () => { stopAuto(); showSlide(cur - 1); startAuto(); });
document.getElementById('rNext').addEventListener('click', () => { stopAuto(); showSlide(cur + 1); startAuto(); });
rDots.forEach((d, i) => d.addEventListener('click', () => { stopAuto(); showSlide(i); startAuto(); }));

const carousel = document.getElementById('reviewsCarousel');
carousel.addEventListener('mouseenter', stopAuto);
carousel.addEventListener('mouseleave', startAuto);
startAuto();

/* ===== FAQ ACCORDION ===== */
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
});

/* ===== CONTACT FORM ===== */
document.getElementById('contactForm').addEventListener('submit', e => {
  e.preventDefault();
  document.getElementById('contactForm').style.display = 'none';
  document.getElementById('formSuccess').style.display = 'flex';
});

/* ===== NEWSLETTER ===== */
document.getElementById('newsForm').addEventListener('submit', e => {
  e.preventDefault();
  e.currentTarget.innerHTML = '<p style="color:rgba(255,255,255,.5);font-size:14px;padding:8px 0;">Thanks, you\'re on the list.</p>';
});
