/**
 * Abhi Labs - Elite Class Interaction Engine v3.1
 * Centralized logic for high-end web experiences.
 */

document.addEventListener('DOMContentLoaded', () => {
    initSmoothScroll();
    initScrollReveal();
    initCustomCursor();
    initMagneticElements();
    initStaggerEntrance();
    initFluidTransitions();
    initLaboratoryInteractions();
    initBackgroundDynamics();
    initScrambleText();
});

/**
 * Ultra-Smooth Scroll Engine
 */
function initSmoothScroll() {
    document.documentElement.style.scrollBehavior = 'smooth';
}

/**
 * Scroll Reveal Animation Engine
 */
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Custom Cursor Engine
 */
function initCustomCursor() {
    // Disable on touch devices
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const dot = document.getElementById('cursor-dot');
    const outline = document.getElementById('cursor-outline');

    if (!dot || !outline) return;

    document.body.style.cursor = 'none';

    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let outlineX = 0, outlineY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        const dotLerp = 0.2;
        const outlineLerp = 0.1;

        dotX += (mouseX - dotX) * dotLerp;
        dotY += (mouseY - dotY) * dotLerp;

        outlineX += (mouseX - outlineX) * outlineLerp;
        outlineY += (mouseY - outlineY) * outlineLerp;

        dot.style.transform = `translate(${dotX - 4}px, ${dotY - 4}px)`;
        outline.style.transform = `translate(${outlineX - 20}px, ${outlineY - 20}px)`;

        requestAnimationFrame(animate);
    }
    animate();

    const interactiveElements = document.querySelectorAll('a, button, .group, .magnetic-button, input, textarea');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            document.body.classList.add('cursor-active');
        });
        el.addEventListener('mouseleave', () => {
            document.body.classList.remove('cursor-active');
        });
    });
}

/**
 * Magnetic & 3D Interaction Engine
 */
function initMagneticElements() {
    const magneticElements = document.querySelectorAll('.magnetic-button, a, .group');

    magneticElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            const strength = el.classList.contains('magnetic-button') ? 0.3 : 0.15;

            requestAnimationFrame(() => {
                el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
            });
        });

        el.addEventListener('mouseleave', () => {
            requestAnimationFrame(() => {
                el.style.transform = 'translate(0px, 0px)';
            });
        });
    });
}

/**
 * Stagger Entrance Animation for Hero
 */
function initStaggerEntrance() {
    const heroElements = document.querySelectorAll('header .reveal');
    heroElements.forEach((el, index) => {
        el.style.transitionDelay = `${index * 0.1}s`;
    });
}

/**
 * Fluid Page Transitions
 */
function initFluidTransitions() {
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1)';

    document.querySelectorAll('a').forEach(link => {
        if (link.hostname === window.location.hostname &&
            !link.hash &&
            link.target !== '_blank' &&
            !link.href.includes('mailto:')) {

            link.addEventListener('click', (e) => {
                // Allow standard browser behaviors (Cmd/Ctrl click, middle click)
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;

                e.preventDefault();
                const destination = link.href;

                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = destination;
                }, 500);
            });
        }
    });
}

/**
 * Laboratory-specific micro-interactions
 */
function initLaboratoryInteractions() {
    const labCards = document.querySelectorAll('.md\\:col-span-4, .md\\:col-span-7, .md\\:col-span-5, .glass-premium');

    labCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const icon = card.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.15) rotate(8deg)';
                icon.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
            }
        });

        card.addEventListener('mouseleave', () => {
            const icon = card.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

/**
 * Reactive Background Dynamics
 */
function initBackgroundDynamics() {
    if (window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches) return;

    const canvas = document.createElement('canvas');
    canvas.id = 'bg-particles';
    Object.assign(canvas.style, {
        position: 'fixed', top: '0', left: '0', width: '100%', height: '100%',
        pointerEvents: 'none', zIndex: '0', opacity: '0.4'
    });
    document.body.prepend(canvas);

    const ctx = canvas.getContext('2d');
    let width, height, particles = [];

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 1.5 + 0.5;
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x > width) this.x = 0;
            if (this.x < 0) this.x = width;
            if (this.y > height) this.y = 0;
            if (this.y < 0) this.y = height;
        }
        draw() {
            ctx.fillStyle = 'rgba(13, 148, 136, 0.2)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    for (let i = 0; i < 50; i++) particles.push(new Particle());

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => { p.update(); p.draw(); });
        requestAnimationFrame(animate);
    }
    animate();
}

/**
 * Scramble Text Effect
 */
function initScrambleText() {
    const chars = '!<>-_\\/[]{}—=+*^?#________';

    class Scrambler {
        constructor(el) {
            this.el = el;
            this.text = el.innerText;
            this.update = this.update.bind(this);
        }

        scramble() {
            const length = this.text.length;
            const promise = new Promise((resolve) => this.resolve = resolve);
            this.queue = [];
            for (let i = 0; i < length; i++) {
                const from = this.text[i];
                const to = this.text[i];
                const start = Math.floor(Math.random() * 40);
                const end = start + Math.floor(Math.random() * 40);
                this.queue.push({ from, to, start, end });
            }
            cancelAnimationFrame(this.frameRequest);
            this.frame = 0;
            this.update();
            return promise;
        }

        update() {
            let output = '';
            let complete = 0;
            for (let i = 0, n = this.queue.length; i < n; i++) {
                let { from, to, start, end, char } = this.queue[i];
                if (this.frame >= end) {
                    complete++;
                    output += to;
                } else if (this.frame >= start) {
                    if (!char || Math.random() < 0.28) {
                        char = chars[Math.floor(Math.random() * chars.length)];
                        this.queue[i].char = char;
                    }
                    output += `<span class="opacity-50 text-business">${char}</span>`;
                } else {
                    output += from;
                }
            }
            this.el.innerHTML = output;
            if (complete === this.queue.length) {
                this.resolve();
            } else {
                this.frameRequest = requestAnimationFrame(this.update);
                this.frame++;
            }
        }
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const scrambler = new Scrambler(entry.target);
                scrambler.scramble();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.scramble-text').forEach(el => observer.observe(el));
}
