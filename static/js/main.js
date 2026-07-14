/* =============================================================================
   main.js — Efeitos da Landing Page
   - Typing effect no hero
   - Navbar scroll
   - Parallax do glow
   - Posicionamento orbital dos skills
   - AOS init
   ============================================================================= */

document.addEventListener('DOMContentLoaded', function () {

    // =========================================================================
    // AOS — Animate On Scroll
    // =========================================================================
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 80,
            disable: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
        });
    }

    // =========================================================================
    // Navbar scroll effect
    // =========================================================================
    const navbar = document.querySelector('.navbar-portfolio');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // =========================================================================
    // Typing effect
    // =========================================================================
    const typingElement = document.getElementById('typing-text');
    if (typingElement) {
        const text = typingElement.getAttribute('data-text') || '';
        const speed = 80;
        let i = 0;
        typingElement.textContent = '';

        function typeChar() {
            if (i < text.length) {
                typingElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeChar, speed);
            }
        }

        // Start typing after a short delay
        setTimeout(typeChar, 500);
    }

    // =========================================================================
    // Parallax glow (hero)
    // =========================================================================
    const heroGlow = document.querySelector('.hero-glow');
    if (heroGlow && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.addEventListener('mousemove', function (e) {
            const x = (e.clientX / window.innerWidth - 0.5) * 30;
            const y = (e.clientY / window.innerHeight - 0.5) * 30;
            heroGlow.style.transform = `translate(calc(-50% + ${x}px), ${y}px)`;
        });
    }

    // =========================================================================
    // Skills orbit positioning
    // =========================================================================
    const orbitContainer = document.querySelector('.skills-orbit-container');
    if (orbitContainer) {
        const skillItems = orbitContainer.querySelectorAll('.skill-item');
        const containerSize = orbitContainer.offsetWidth;
        const centerX = containerSize / 2;
        const centerY = containerSize / 2;

        skillItems.forEach(function (item, index) {
            const total = skillItems.length;
            const angle = (index / total) * 2 * Math.PI - Math.PI / 2;

            // Alternate between inner and outer ring
            const radius = index % 2 === 0
                ? containerSize * 0.28  // inner ring
                : containerSize * 0.43; // outer ring

            const x = centerX + radius * Math.cos(angle) - 25;
            const y = centerY + radius * Math.sin(angle) - 25;

            item.style.left = x + 'px';
            item.style.top = y + 'px';
        });
    }

    // =========================================================================
    // Smooth scroll for nav links
    // =========================================================================
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeight = navbar ? navbar.offsetHeight : 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth',
                });
            }
        });
    });

});
