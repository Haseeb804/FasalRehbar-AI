/**
 * FasalRehbar AI — Master Client Interaction Script
 * Handles: Drag & Drop upload, file picker trigger, Grad-CAM toggle,
 * animated stage loaders, tab switches, and Chart.js analytics.
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Navbar Scroll Shadow Effect ───────────────────────
    const nav = document.getElementById('mainNav');
    if (nav) {
        const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 20);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // ── 2. Mobile Navigation Drawer ───────────────────────────
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
        });
        document.addEventListener('click', (e) => {
            if (!nav.contains(e.target)) {
                navMenu.classList.remove('open');
            }
        });
    }

    // ── 3. Flash Messages Auto-Dismiss ────────────────────────
    const flashMessages = document.querySelectorAll('.flash-message, .alert-dismissible');
    flashMessages.forEach((el, i) => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-10px)';
            setTimeout(() => el.remove(), 400);
        }, 4500 + i * 200);
    });

    // ── 4. Drag & Drop + Click File Upload with Instant Preview ─
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('id_image');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImage');
    const previewInfo = document.getElementById('previewInfo');
    const uploadActions = document.getElementById('uploadActions');
    const clearBtn = document.getElementById('clearBtn');
    const uploadForm = document.getElementById('uploadForm');

    if (dropZone && fileInput) {
        // Direct click on dropzone opens native file picker
        dropZone.addEventListener('click', (e) => {
            // Prevent double-trigger if clicking label or clear button
            if (e.target.id !== 'clearBtn' && !e.target.closest('#uploadActions')) {
                fileInput.click();
            }
        });

        // Keyboard accessible trigger
        dropZone.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                fileInput.click();
            }
        });

        // Drag & drop listeners
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        fileInput.addEventListener('change', function () {
            if (this.files && this.files.length > 0) {
                handleFileSelect(this.files[0]);
            }
        });

        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                resetUploadZone();
            });
        }
    }

    function handleFileSelect(file) {
        if (!file.type.match('image.*')) {
            alert('Please select a valid image file (JPG, PNG, WebP).');
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            if (previewImg) previewImg.src = e.target.result;
            if (uploadPlaceholder) uploadPlaceholder.style.display = 'none';
            if (imagePreview) imagePreview.style.display = 'block';
            if (uploadActions) uploadActions.style.display = 'block';

            const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
            if (previewInfo) {
                previewInfo.innerHTML = `<strong>${file.name}</strong> (${sizeMb} MB) — Ready for analysis`;
            }
        };
        reader.readAsDataURL(file);
    }

    function resetUploadZone() {
        if (fileInput) fileInput.value = '';
        if (previewImg) previewImg.src = '';
        if (imagePreview) imagePreview.style.display = 'none';
        if (uploadActions) uploadActions.style.display = 'none';
        if (uploadPlaceholder) uploadPlaceholder.style.display = 'block';
    }

    // ── 5. Multi-Stage Animated Loading on Submit ──────────────
    if (uploadForm) {
        uploadForm.addEventListener('submit', function () {
            showPakAgriLoading();
        });
    }

    // ── 6. Image View Mode Toggle (Original vs Grad-CAM) ───────
    const viewBtns = document.querySelectorAll('.btn-view-mode[data-mode]');
    const originalImg = document.getElementById('viewOriginalImg');
    const gradcamImg = document.getElementById('viewGradcamImg');

    viewBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const mode = this.dataset.mode;
            viewBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            if (mode === 'gradcam' && gradcamImg) {
                if (originalImg) originalImg.style.display = 'none';
                gradcamImg.style.display = 'block';
            } else {
                if (gradcamImg) gradcamImg.style.display = 'none';
                if (originalImg) originalImg.style.display = 'block';
            }
        });
    });

    // ── 7. Recommendation Tab Switching ──────────────────────
    const tabBtns = document.querySelectorAll('.rec-tab-btn[data-tab]');
    const tabPanes = document.querySelectorAll('.rec-tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const target = this.dataset.tab;
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.style.display = 'none');

            this.classList.add('active');
            const activePane = document.getElementById('tab-' + target);
            if (activePane) activePane.style.display = 'block';
        });
    });

    // ── 8. Interactive Checklist Toggle ───────────────────────
    const checkItems = document.querySelectorAll('.checklist-item');
    checkItems.forEach(item => {
        item.addEventListener('click', function () {
            this.classList.toggle('completed');
            const icon = this.querySelector('.check-icon');
            if (icon) {
                if (this.classList.contains('completed')) {
                    icon.className = 'fas fa-check-circle check-icon text-success';
                } else {
                    icon.className = 'far fa-circle check-icon';
                }
            }
        });
    });

    // ── 9. Circular Gauge Initializer ────────────────────────
    const gauges = document.querySelectorAll('.circular-gauge-svg[data-progress]');
    gauges.forEach(gauge => {
        const progress = parseFloat(gauge.dataset.progress) || 0;
        const circle = gauge.querySelector('.gauge-progress');
        if (circle) {
            const radius = circle.r.baseVal.value;
            const circumference = 2 * Math.PI * radius;
            circle.style.strokeDasharray = `${circumference} ${circumference}`;
            const offset = circumference - (progress / 100) * circumference;
            setTimeout(() => {
                circle.style.strokeDashoffset = offset;
            }, 300);
        }
    });

});

// Global Loading Animation Sequence
function showPakAgriLoading() {
    const overlay = document.getElementById('pakagri-loading-overlay');
    if (!overlay) return;

    overlay.classList.add('active');

    const steps = [
        document.getElementById('loadingStep1'),
        document.getElementById('loadingStep2'),
        document.getElementById('loadingStep3'),
        document.getElementById('loadingStep4')
    ];

    let current = 0;
    const interval = setInterval(() => {
        if (steps[current]) {
            steps[current].classList.add('done');
            steps[current].classList.remove('active');
        }
        current++;
        if (steps[current]) {
            steps[current].classList.add('active');
        }
        if (current >= steps.length) {
            clearInterval(interval);
        }
    }, 1200);
}
