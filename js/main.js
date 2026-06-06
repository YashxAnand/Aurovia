// ══════════════════════════════════════════════
// INTRO OVERLAY — dismiss after animation
// ══════════════════════════════════════════════
(function () {
    const overlay = document.getElementById('intro-overlay');
    if (!overlay) return;

    // If the user has already seen the intro this session, skip it instantly
    if (sessionStorage.getItem('introSeen')) {
        overlay.style.display = 'none';
        document.body.classList.remove('intro-active');
        window.dispatchEvent(new CustomEvent('introComplete'));
        return;
    }

    // Dismiss after 3.8 s (progress bar finishes at ~3.7 s)
    setTimeout(() => {
        overlay.classList.add('fade-out');

        // After fade-out transition (0.9 s), fully hide and unlock scroll
        overlay.addEventListener('transitionend', () => {
            overlay.style.display = 'none';
            document.body.classList.remove('intro-active');
            sessionStorage.setItem('introSeen', '1');
            // Signal chatbot to open
            window.dispatchEvent(new CustomEvent('introComplete'));
        }, { once: true });
    }, 3800);
})();

document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation Scroll Effect
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Mobile Menu Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // Animate hamburger icon (optional enhancement)
            const spans = mobileBtn.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // 3. Scroll Reveal Animations using Intersection Observer
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
});
