/**
 * PakAgri — Main JavaScript
 * Handles: nav scroll effects, card hover enhancements, image previews,
 * flash message auto-dismiss, and utility helpers.
 */

'use strict';

// ── DOM Ready ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

    // ── Navbar scroll shadow ─────────────────────────────────
    const nav = document.getElementById('mainNav');
    if (nav) {
        const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 20);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll(); // run once on load
    }

    // ── Mobile nav toggle ────────────────────────────────────
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');
    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('open');
            menu.classList.toggle('open');
        });
        // Close menu when a link is clicked
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                toggle.classList.remove('open');
                menu.classList.remove('open');
            });
        });
        // Close menu on outside click
        document.addEventListener('click', e => {
            if (!nav.contains(e.target)) {
                toggle.classList.remove('open');
                menu.classList.remove('open');
            }
        });
    }

    // ── Flash message auto-dismiss ───────────────────────────
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((el, i) => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateX(16px)';
            setTimeout(() => el.remove(), 400);
        }, 4000 + i * 200);
    });

    // ── Confidence bar animation ─────────────────────────────
    const confBars = document.querySelectorAll('.confidence-bar-fill[data-target]');
    if (confBars.length > 0) {
        const animateBars = () => {
            confBars.forEach(bar => {
                const rect = bar.getBoundingClientRect();
                if (rect.top < window.innerHeight) {
                    bar.style.width = bar.dataset.target + '%';
                }
            });
        };
        window.addEventListener('scroll', animateBars, { passive: true });
        setTimeout(animateBars, 400);
    }

    // ── Recent scan card hover image zoom ────────────────────
    document.querySelectorAll('.card img').forEach(img => {
        const card = img.closest('.card');
        if (card) {
            card.addEventListener('mouseenter', () => { img.style.transform = 'scale(1.05)'; });
            card.addEventListener('mouseleave', () => { img.style.transform = 'scale(1)'; });
        }
    });

    // ── Fade-in on scroll (Intersection Observer) ────────────
    const fadeEls = document.querySelectorAll('.fade-in');
    if (fadeEls.length > 0 && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.style.opacity = '1';
                    e.target.style.transform = 'translateY(0)';
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.1 });

        fadeEls.forEach((el, i) => {
            // Only animate elements that are not already in the viewport
            const rect = el.getBoundingClientRect();
            if (rect.top > window.innerHeight) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(24px)';
                el.style.transition = `opacity 0.5s ease ${i * 0.08}s, transform 0.5s ease ${i * 0.08}s`;
                io.observe(el);
            }
        });
    }

    // ── Tab switching (recommendation page) ─────────────────
    const tabBtns = document.querySelectorAll('.tab-btn[data-tab]');
    if (tabBtns.length) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                const target = this.dataset.tab;
                document.querySelectorAll('.tab-btn[data-tab]').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                document.querySelectorAll('.advice-section, .tab-pane').forEach(s => s.classList.remove('active'));
                this.classList.add('active');
                this.setAttribute('aria-selected', 'true');
                const section = document.getElementById('tab-' + target);
                if (section) section.classList.add('active');
            });
        });
    }
});

// ── Global loading overlay helper ────────────────────────────
// Called from detection/index.html when form is submitted.
function showPakAgriLoading(message, submessage) {
    const overlay = document.getElementById('pakagri-loading-overlay');
    if (!overlay) return;

    const msgEl = document.getElementById('pakagri-loading-message');
    const subEl = document.getElementById('pakagri-loading-submessage');

    if (message && msgEl) msgEl.textContent = message;
    if (subEl) subEl.textContent = submessage || '';

    overlay.classList.add('active');

    // Cycle through loading steps
    const stepIds = ['step1', 'step2', 'step3', 'step4'];
    let current = 0;

    const tick = () => {
        stepIds.forEach((id, idx) => {
            const el = document.getElementById(id);
            if (!el) return;
            el.classList.remove('active', 'done');
            if (idx < current) el.classList.add('done');
            else if (idx === current) el.classList.add('active');
        });
        current++;
        if (current < stepIds.length) setTimeout(tick, 2000);
    };

    tick();
}
