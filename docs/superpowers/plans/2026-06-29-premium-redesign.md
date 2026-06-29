# abhilabs.app Premium Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign abhilabs.app into a dark-luxury, motion-first Android app marketing site with per-app color worlds, scroll-driven phone mockups, and card hover world-shift effects.

**Architecture:** Full CSS design system replacement using Tailwind CLI + extended CSS custom properties. Homepage uses pure CSS hover effects. App detail pages use GSAP 3.12.5 + ScrollTrigger (CDN, defer) for scroll-driven phone. Each app page applies a per-app world via body class + CSS animations.

**Tech Stack:** Tailwind CLI 3.4, CSS custom properties, GSAP 3.12.5 + ScrollTrigger (cdnjs CDN), vanilla JS, GitHub Pages static hosting.

## Global Constraints

- Branch: `debug` — all commits go here
- Run `npm run build` after every CSS change before committing
- Lighthouse: maintain 95+ on all 4 categories
- Dark mode: `@media (prefers-color-scheme: dark)` only — no JS toggle
- GSAP: loaded via `<script defer>` from cdnjs — app pages only (not homepage, about, privacy)
- `prefers-reduced-motion`: disable all GSAP and CSS keyframe animations
- All images: `loading="lazy"` except hero first screenshot (`fetchpriority="high"`, no lazy)
- Font: Plus Jakarta Sans async preload pattern — copy exactly from existing pages
- Contact email everywhere: `contact@abhilabs.app`
- Copyright: `© 2026 Abhi Labs. Bangalore, India.`
- Privacy links: keep existing `/privacy/[app]/` paths unchanged
- Play Store package IDs: unchanged from current pages
- `styles/output.css` is gitignored — always build before commit
- Privacy pages (`privacy/*/index.html`) and `404.html` — DO NOT TOUCH

---

## File Map

| File | Action |
|------|--------|
| `styles/input.css` | Full replacement — new design system |
| `index.html` | Full rewrite — featured grid homepage |
| `about/index.html` | Full rewrite — premium studio page |
| `apps/abhi-scan/index.html` | Full rewrite — AbhiScan Pro world + GSAP |
| `apps/lunavi/index.html` | Full rewrite — Lunavi world + GSAP |
| `apps/abhi-scan-lite/index.html` | Full rewrite — AbhiScan Lite world + GSAP |
| `apps/abhinidra/index.html` | Full rewrite — AbhiNidra world + GSAP |
| `apps/ai-qr-barcode/index.html` | Full rewrite — AI QR world + GSAP |

---

### Task 1: CSS Design System (`styles/input.css`)

**Files:**
- Modify: `styles/input.css` (full replacement)

**Interfaces:**
- Produces: all CSS classes used by Tasks 2–8. Every class name used in later tasks is defined here.

- [ ] **Step 1: Replace `styles/input.css` with the complete new design system**

Write this exact content to `styles/input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── Design Tokens ─────────────────────────────────── */
:root {
  --bg: #08080a;
  --bg-subtle: #0e0e10;
  --surface: #111113;
  --border: #1c1c1f;
  --text-1: #fafafa;
  --text-2: #a1a1aa;
  --text-3: #52525b;
  --brand: #0d9488;
  --accent: #0d9488;
  --accent-hover: #0a7a6e;
  --accent-subtle: rgba(13,148,136,0.12);
  --accent-text: #0d9488;
  --nav-bg: rgba(8, 8, 10, 0.85);
  --phone-frame: #1a1a1e;
  --phone-border: #2a2a2e;
  --card-bg: #0e0e10;
  --card-border: #1c1c1f;
  --noise-opacity: 0.035;
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.4);
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --radius-2xl: 40px;
}

/* Per-app accent classes */
.app-abhiscan { --accent:#0d9488; --accent-hover:#0a7a6e; --accent-subtle:rgba(13,148,136,0.12); --accent-text:#0d9488; }
.app-lunavi   { --accent:#e11d48; --accent-hover:#be123c; --accent-subtle:rgba(225,29,72,0.12);  --accent-text:#e11d48; }
.app-abhinidra{ --accent:#6366f1; --accent-hover:#4f46e5; --accent-subtle:rgba(99,102,241,0.12); --accent-text:#6366f1; }
.app-ai-qr    { --accent:#0d9488; --accent-hover:#0a7a6e; --accent-subtle:rgba(13,148,136,0.12); --accent-text:#0d9488; }

/* ── Base ──────────────────────────────────────────── */
@layer base {
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0ms !important; transition-duration: 150ms !important; }
    html { scroll-behavior: auto; }
  }
  body {
    background-color: var(--bg);
    color: var(--text-1);
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
    line-height: 1.6;
    min-height: 100vh;
  }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 4px; }
  img { max-width: 100%; display: block; }
}

/* ── World Backgrounds (app pages) ────────────────── */
.app-abhiscan body,
.app-ai-qr body {
  background-image: radial-gradient(800px circle at 80% -10%, rgba(13,148,136,0.15), transparent 70%);
  background-attachment: fixed;
}
.app-lunavi body {
  background-image: radial-gradient(800px circle at 80% -10%, rgba(225,29,72,0.15), transparent 70%);
  background-attachment: fixed;
}
.app-abhinidra body {
  background-image: radial-gradient(800px circle at 80% -10%, rgba(99,102,241,0.15), transparent 70%);
  background-attachment: fixed;
}

/* Noise texture overlay */
.has-noise::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity: var(--noise-opacity);
  pointer-events: none;
  z-index: 0;
}

/* World particle: scan-line (AbhiScan pages) */
@keyframes scanline {
  0%   { transform: translateY(-4px); opacity: 0; }
  5%   { opacity: 1; }
  95%  { opacity: 1; }
  100% { transform: translateY(100vh); opacity: 0; }
}
.world-scanline::after {
  content: '';
  position: fixed;
  left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  animation: scanline 5s linear infinite;
  pointer-events: none;
  z-index: 1;
  opacity: 0.04;
}
@media (prefers-reduced-motion: reduce) { .world-scanline::after { display: none; } }

/* World particle: heartbeat pulse (Lunavi) */
@keyframes heartbeat {
  0%, 100% { opacity: 0.03; transform: scale(1); }
  50%       { opacity: 0.06; transform: scale(1.04); }
}
.world-heartbeat::after {
  content: '';
  position: fixed;
  inset: -50%;
  background: radial-gradient(circle at center, var(--accent), transparent 60%);
  animation: heartbeat 3s ease-in-out infinite;
  pointer-events: none;
  z-index: 1;
}
@media (prefers-reduced-motion: reduce) { .world-heartbeat::after { display: none; } }

/* World particle: wave (AbhiNidra) */
@keyframes wave {
  0%, 100% { opacity: 0.02; transform: scaleX(1); }
  50%       { opacity: 0.04; transform: scaleX(1.02); }
}
.world-wave::after {
  content: '';
  position: fixed;
  left: -10%; right: -10%; bottom: -20%;
  height: 60%;
  background: radial-gradient(ellipse at bottom, var(--accent), transparent 70%);
  animation: wave 6s ease-in-out infinite;
  pointer-events: none;
  z-index: 1;
}
@media (prefers-reduced-motion: reduce) { .world-wave::after { display: none; } }

/* ── Components ────────────────────────────────────── */
@layer components {

/* Skip link */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 1rem;
  padding: 0.5rem 1rem;
  background: var(--accent);
  color: #fff;
  border-radius: var(--radius-sm);
  font-weight: 600;
  z-index: 9999;
  text-decoration: none;
}
.skip-link:focus { left: 1rem; }

/* Visually hidden */
.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border-width: 0;
}

/* ── Nav ───────────────────────────────────────────── */
.site-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: var(--nav-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  text-decoration: none; color: var(--text-1);
}
.nav-logo-mark {
  width: 32px; height: 32px;
  background: var(--accent);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 12px; color: #fff;
  letter-spacing: -0.02em;
}
.nav-logo-text { font-weight: 700; font-size: 15px; }
.nav-links {
  display: flex; align-items: center; gap: 0.25rem;
  list-style: none;
}
.nav-link {
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  color: var(--text-2);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s, background 0.2s;
}
.nav-link:hover, .nav-link[aria-current="page"] { color: var(--text-1); background: rgba(255,255,255,0.05); }
.nav-cta {
  padding: 0.4rem 1rem;
  background: var(--accent);
  color: #fff;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.2s, opacity 0.2s;
}
.nav-cta:hover { opacity: 0.85; }
.nav-hamburger {
  display: none;
  background: none; border: none;
  color: var(--text-2);
  cursor: pointer; padding: 0.5rem;
  border-radius: var(--radius-sm);
}
@media (max-width: 640px) {
  .nav-hamburger { display: flex; }
  .nav-links {
    display: none; position: absolute;
    top: 64px; left: 0; right: 0;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    flex-direction: column; align-items: stretch;
    padding: 1rem;
    gap: 0.25rem;
  }
  .nav-links--open { display: flex; }
  .nav-link, .nav-cta { padding: 0.75rem 1rem; border-radius: var(--radius-md); }
}

/* ── Phone Mockup ──────────────────────────────────── */
.phone-mockup { position: relative; display: inline-block; }

.phone-mockup__frame {
  position: relative;
  background: var(--phone-frame);
  border: 1.5px solid var(--phone-border);
  border-radius: 44px;
  padding: 14px 10px 18px;
  box-sizing: border-box;
  transition: transform 0.4s ease, filter 0.4s ease;
}
/* Power button */
.phone-mockup__frame::before {
  content: '';
  position: absolute; right: -3px; top: 110px;
  width: 3px; height: 44px;
  background: var(--phone-border);
  border-radius: 0 2px 2px 0;
}
/* Volume buttons */
.phone-mockup__frame::after {
  content: '';
  position: absolute; left: -3px; top: 90px;
  width: 3px; height: 36px;
  background: var(--phone-border);
  border-radius: 2px 0 0 2px;
  box-shadow: 0 52px 0 var(--phone-border);
}
.phone-mockup__top {
  display: flex; align-items: center;
  justify-content: center; gap: 8px;
  margin-bottom: 10px;
}
.phone-mockup__speaker {
  width: 48px; height: 5px;
  background: var(--phone-border);
  border-radius: 3px;
}
.phone-mockup__camera {
  width: 8px; height: 8px;
  background: #111115;
  border: 1px solid #333;
  border-radius: 50%; flex-shrink: 0;
}
.phone-mockup__screen {
  overflow: hidden;
  border-radius: 30px;
  background: #000;
  line-height: 0;
}
.phone-screen {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}

/* Large (hero / sticky section) */
.phone-mockup--lg .phone-mockup__frame { width: 280px; }
.phone-mockup--lg .phone-mockup__screen { width: 260px; height: 536px; }

/* Small (homepage cards) */
.phone-mockup--sm .phone-mockup__frame {
  width: 150px; border-radius: 28px;
  padding: 10px 7px 12px;
}
.phone-mockup--sm .phone-mockup__frame::before { top: 70px; height: 28px; }
.phone-mockup--sm .phone-mockup__frame::after  { top: 55px; height: 22px; box-shadow: 0 32px 0 var(--phone-border); }
.phone-mockup--sm .phone-mockup__top { margin-bottom: 7px; }
.phone-mockup--sm .phone-mockup__speaker { width: 30px; height: 4px; }
.phone-mockup--sm .phone-mockup__camera { width: 6px; height: 6px; }
.phone-mockup--sm .phone-mockup__screen { width: 136px; height: 280px; border-radius: 20px; }

/* Hero phone — tilted + floating */
@keyframes phone-float {
  0%, 100% { transform: perspective(1000px) rotateY(-15deg) rotateX(5deg) translateY(0); }
  50%       { transform: perspective(1000px) rotateY(-15deg) rotateX(5deg) translateY(-12px); }
}
.phone-mockup--hero .phone-mockup__frame {
  animation: phone-float 3s ease-in-out infinite;
  filter: drop-shadow(0 50px 100px color-mix(in srgb, var(--accent) 35%, transparent));
}
@media (prefers-reduced-motion: reduce) {
  .phone-mockup--hero .phone-mockup__frame {
    animation: none;
    transform: perspective(1000px) rotateY(-15deg) rotateX(5deg);
  }
}

/* Card phone — tilted, un-tilts on card hover */
.phone-mockup--card .phone-mockup__frame {
  transform: perspective(600px) rotateY(-12deg) rotateX(4deg);
  filter: drop-shadow(0 20px 40px color-mix(in srgb, var(--accent) 20%, transparent));
}
.app-card:hover .phone-mockup--card .phone-mockup__frame {
  transform: perspective(600px) rotateY(0deg) rotateX(0deg) scale(1.04);
  filter: drop-shadow(0 30px 60px color-mix(in srgb, var(--accent) 40%, transparent));
}

/* Sticky phone (GSAP controls, no CSS transform/animation) */
.phone-mockup--sticky .phone-mockup__frame {
  filter: drop-shadow(0 40px 80px color-mix(in srgb, var(--accent) 30%, transparent));
}

/* ── Homepage Hero ─────────────────────────────────── */
.home-hero {
  min-height: 55vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 7rem 2rem 4rem;
  position: relative;
  overflow: hidden;
}
.home-hero__orb {
  position: absolute;
  top: -120px; right: -180px;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(13,148,136,0.08), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
  animation: orb-slow 20s ease-in-out infinite alternate;
}
@keyframes orb-slow {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(-30px, 20px) scale(1.05); }
}
@media (prefers-reduced-motion: reduce) { .home-hero__orb { animation: none; } }
.home-hero__label {
  font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--accent); margin-bottom: 1.5rem;
  display: flex; align-items: center; gap: 8px; justify-content: center;
}
.home-hero__title {
  font-size: clamp(40px, 7vw, 80px);
  font-weight: 800; line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--text-1);
  margin-bottom: 1.25rem;
}
.home-hero__sub {
  font-size: clamp(16px, 2vw, 20px);
  color: var(--text-2); max-width: 480px;
  margin: 0 auto;
}

/* ── App Card Grid ─────────────────────────────────── */
.app-grid-section { padding: 0 2rem 6rem; max-width: 1200px; margin: 0 auto; }

.app-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-areas:
    "f1 f1 f1 f2 f2 f2"
    "s1 s1 s2 s2 s3 s3";
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}
.app-card--featured-1 { grid-area: f1; }
.app-card--featured-2 { grid-area: f2; }
.app-card--standard-1 { grid-area: s1; }
.app-card--standard-2 { grid-area: s2; }
.app-card--standard-3 { grid-area: s3; }

.app-card {
  background: var(--card-bg);
  padding: 1.75rem;
  position: relative;
  transition: background 0.4s ease;
  cursor: pointer;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.app-card--featured { padding: 2.5rem; }

/* Hover world-shift */
.app-card:hover { background: color-mix(in srgb, var(--accent) 10%, var(--bg)); }
.app-card:hover .app-card__border-glow { opacity: 1; }

.app-card__border-glow {
  position: absolute; inset: 0;
  border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
  border-radius: inherit;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.app-card__initial {
  font-size: 48px; font-weight: 800;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 0.75rem;
  opacity: 0.7;
}
.app-card__badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  border-radius: 100px;
  padding: 3px 10px;
  margin-bottom: 0.75rem;
}
.app-card__badge--featured::before {
  content: '★';
  font-size: 9px;
}
.app-card__name {
  font-size: 20px; font-weight: 700;
  color: var(--text-1);
  margin-bottom: 0.4rem;
}
.app-card--featured .app-card__name { font-size: 24px; }
.app-card__tagline {
  font-size: 14px; color: var(--text-2);
  margin-bottom: 1rem; line-height: 1.5;
}
.app-card__features {
  list-style: none; margin-bottom: 1.5rem;
  display: flex; flex-direction: column; gap: 0.4rem;
}
.app-card__features li {
  font-size: 13px; color: var(--text-2);
  display: flex; align-items: center; gap: 6px;
}
.app-card__features li::before {
  content: '';
  width: 5px; height: 5px;
  background: var(--accent);
  border-radius: 50%; flex-shrink: 0;
}
.app-card__phone-wrap {
  flex: 1; display: flex;
  align-items: flex-end; justify-content: center;
  margin-top: 1.5rem;
}
.app-card__cta {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; font-weight: 600;
  color: var(--accent);
  margin-top: 1.5rem;
  transition: gap 0.2s ease;
}
.app-card:hover .app-card__cta { gap: 10px; }

@media (max-width: 900px) {
  .app-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      "f1 f2"
      "s1 s2"
      "s3 s3";
  }
}
@media (max-width: 600px) {
  .app-grid {
    grid-template-columns: 1fr;
    grid-template-areas: "f1" "f2" "s1" "s2" "s3";
  }
  .app-grid-section { padding: 0 0 4rem; }
}

/* ── App Hero (detail pages) ───────────────────────── */
.app-hero {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 8rem 2rem 4rem;
}
.app-hero__label {
  font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--accent); margin-bottom: 1rem;
}
.app-hero__title {
  font-size: clamp(44px, 6vw, 80px);
  font-weight: 800; line-height: 1.0;
  letter-spacing: -0.03em;
  color: var(--text-1); margin-bottom: 1rem;
}
.app-hero__tagline {
  font-size: clamp(17px, 2vw, 20px);
  color: var(--text-2); margin-bottom: 1.75rem;
  line-height: 1.6; max-width: 420px;
}
.app-hero__bullets {
  list-style: none; margin-bottom: 2rem;
  display: flex; flex-direction: column; gap: 0.6rem;
}
.app-hero__bullets li {
  display: flex; align-items: center; gap: 8px;
  font-size: 15px; color: var(--text-2);
}
.app-hero__bullets li::before {
  content: '';
  width: 6px; height: 6px;
  background: var(--accent);
  border-radius: 50%; flex-shrink: 0;
}
.app-hero__phone {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
@media (max-width: 768px) {
  .app-hero {
    grid-template-columns: 1fr;
    min-height: auto;
    padding: 7rem 1.5rem 3rem;
    text-align: center;
  }
  .app-hero__bullets { align-items: center; }
  .app-hero__tagline { margin-left: auto; margin-right: auto; }
  .app-hero__phone { order: -1; }
  .phone-mockup--hero .phone-mockup__frame {
    animation: none;
    transform: perspective(1000px) rotateY(0deg) rotateX(0deg);
  }
}

/* ── Buttons ───────────────────────────────────────── */
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 0.875rem 1.75rem;
  background: var(--accent);
  color: #fff; border-radius: var(--radius-md);
  font-weight: 700; font-size: 16px;
  text-decoration: none;
  transition: opacity 0.2s;
}
.btn-primary:hover { opacity: 0.85; }
.btn-secondary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 0.875rem 1.75rem;
  background: rgba(255,255,255,0.06);
  color: var(--text-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-weight: 600; font-size: 15px;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-secondary:hover { background: rgba(255,255,255,0.1); }

/* ── Feature Scroll Section ────────────────────────── */
.feature-scroll-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
.feature-scroll-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6rem;
  align-items: start;
}
.feature-scroll__phone {
  position: sticky;
  top: 15vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.feature-scroll__content {
  display: flex;
  flex-direction: column;
}
.feature-item {
  min-height: 60vh;
  display: flex; flex-direction: column;
  justify-content: center;
  padding: 3rem 0;
  opacity: 0.25;
  transition: opacity 0.4s ease;
}
.feature-item.is-active { opacity: 1; }
.feature-num {
  display: block;
  font-size: 72px; font-weight: 800;
  color: var(--accent); opacity: 0.15;
  line-height: 1; margin-bottom: 0.5rem;
  letter-spacing: -0.04em;
}
.feature-name {
  font-size: 28px; font-weight: 700;
  color: var(--text-1); margin-bottom: 0.75rem;
  line-height: 1.2;
}
.feature-desc {
  font-size: 17px; color: var(--text-2);
  line-height: 1.75; max-width: 400px;
}
.feature-tag {
  display: inline-block;
  font-family: ui-monospace, 'Courier New', monospace;
  font-size: 11px; font-weight: 700;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  border-radius: 4px;
  padding: 3px 8px; margin-top: 1rem;
  letter-spacing: 0.06em;
}
@media (max-width: 768px) {
  .feature-scroll-inner { grid-template-columns: 1fr; gap: 2rem; }
  .feature-scroll__phone { position: static; margin-bottom: 2rem; }
  .feature-item { min-height: auto; padding: 1.5rem 0; opacity: 1; }
}

/* ── Social Proof Strip ────────────────────────────── */
.social-proof-strip {
  background: var(--surface);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 3rem 2rem;
  margin: 4rem 0;
}
.social-proof-inner {
  max-width: 900px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(3, 1fr);
  text-align: center; gap: 2rem;
}
.social-stat__value {
  display: block;
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800; letter-spacing: -0.04em;
  color: var(--accent); line-height: 1;
  margin-bottom: 0.4rem;
}
.social-stat__label {
  font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text-3);
}
.social-stat__sub {
  font-size: 13px; color: var(--text-3);
  margin-top: 0.25rem;
}

/* ── Download CTA ──────────────────────────────────── */
.download-cta {
  background: color-mix(in srgb, var(--accent) 8%, var(--bg));
  border-top: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  padding: 6rem 2rem;
  text-align: center;
}
.download-cta__heading {
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 800; letter-spacing: -0.03em;
  color: var(--text-1); margin-bottom: 0.75rem;
}
.download-cta__sub {
  font-size: 15px; color: var(--text-2);
  margin-bottom: 2.5rem;
}
.play-badge {
  display: inline-block;
  transition: opacity 0.2s, transform 0.2s;
}
.play-badge:hover { opacity: 0.85; transform: translateY(-2px); }
.play-badge img { height: 60px; width: auto; }

/* ── About Page ────────────────────────────────────── */
.about-hero {
  min-height: 60vh;
  display: flex; flex-direction: column;
  justify-content: center;
  max-width: 900px; margin: 0 auto;
  padding: 8rem 2rem 4rem;
}
.about-hero__title {
  font-size: clamp(40px, 6vw, 80px);
  font-weight: 800; line-height: 1.0;
  letter-spacing: -0.03em;
  color: var(--text-1); margin-bottom: 1.5rem;
}
.about-hero__desc {
  font-size: 20px; color: var(--text-2);
  line-height: 1.7; max-width: 560px;
}
.about-values {
  max-width: 1100px; margin: 0 auto;
  padding: 2rem 2rem 5rem;
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}
.about-value {
  background: var(--surface);
  padding: 2.5rem;
}
.about-value__num {
  display: block;
  font-size: 64px; font-weight: 800;
  color: var(--accent); opacity: 0.12;
  line-height: 1; margin-bottom: 0.75rem;
  letter-spacing: -0.04em;
}
.about-value__name {
  font-size: 20px; font-weight: 700;
  color: var(--text-1); margin-bottom: 0.75rem;
}
.about-value__desc { font-size: 15px; color: var(--text-2); line-height: 1.7; }
.about-contact {
  max-width: 700px; margin: 0 auto;
  padding: 5rem 2rem;
  border-top: 1px solid var(--border);
}
.about-contact__label {
  font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-3); margin-bottom: 1rem;
}
.about-contact__email {
  font-size: clamp(24px, 4vw, 40px);
  font-weight: 700; color: var(--accent);
  text-decoration: none;
  display: inline-flex; align-items: center; gap: 12px;
  position: relative;
}
.about-contact__email::after {
  content: '';
  position: absolute; bottom: -4px; left: 0; right: 100%;
  height: 2px; background: var(--accent);
  transition: right 0.3s ease;
}
.about-contact__email:hover::after { right: 0; }
@media (max-width: 768px) {
  .about-values { grid-template-columns: 1fr; }
}

/* ── Footer ────────────────────────────────────────── */
.site-footer {
  border-top: 1px solid var(--border);
  padding: 2rem;
  text-align: center;
}
.footer-copy {
  font-size: 13px; color: var(--text-3);
}
.footer-copy a { color: var(--accent); text-decoration: none; }
.footer-copy a:hover { text-decoration: underline; }

/* ── Prose pages (privacy) — keep unchanged ────────── */
.prose-page {
  max-width: 680px; margin: 0 auto;
  padding: 8rem 2rem 6rem;
}
.prose-page h1 {
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 800; letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}
.prose-page .updated {
  font-size: 13px; color: var(--text-3);
  margin-bottom: 3rem;
}
.prose-page h2 {
  font-size: 18px; font-weight: 700;
  margin: 2.5rem 0 0.75rem;
  color: var(--text-1);
}
.prose-page p { font-size: 15px; color: var(--text-2); line-height: 1.75; margin-bottom: 1rem; }
.prose-page ul { margin: 0.5rem 0 1rem 1.25rem; }
.prose-page li { font-size: 15px; color: var(--text-2); line-height: 1.75; margin-bottom: 0.35rem; }
.prose-page a { color: var(--accent); }

} /* end @layer components */
```

- [ ] **Step 2: Build and verify**

```bash
cd /path/to/repo && npm run build
```

Expected: exits 0, no errors. `styles/output.css` is updated.

- [ ] **Step 3: Quick visual check**

Open `http://localhost:3100` in browser. The existing page will look broken (old classes gone) — that is expected. Confirm the CSS file compiles.

- [ ] **Step 4: Commit**

```bash
git add styles/input.css styles/output.css
git commit -m "feat: replace design system with premium dark-luxury CSS tokens and components"
```

---

### Task 2: Homepage (`index.html`)

**Files:**
- Modify: `index.html` (full rewrite)

**Interfaces:**
- Consumes: all CSS classes from Task 1
- Produces: working homepage with 2 featured + 3 standard app cards

**App card accent colors (inline style on each `.app-card`):**
- AbhiScan Pro: `--accent:#0d9488`
- Lunavi: `--accent:#e11d48`
- AbhiScan Lite: `--accent:#0d9488`
- AbhiNidra: `--accent:#6366f1`
- AI QR Barcode: `--accent:#0d9488`

- [ ] **Step 1: Write `index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/developer_logo.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Abhi Labs — Premium Android Apps</title>
  <meta name="description" content="Premium Android apps built by Abhi Labs. Offline-first, privacy-first, beautifully crafted.">
  <link rel="canonical" href="https://abhilabs.app/">
  <meta property="og:title" content="Abhi Labs — Premium Android Apps">
  <meta property="og:description" content="Premium Android apps built by Abhi Labs. Offline-first, privacy-first, beautifully crafted.">
  <meta property="og:url" content="https://abhilabs.app/">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="og:image" content="https://abhilabs.app/assets/developer_logo.png">
  <meta name="twitter:image" content="https://abhilabs.app/assets/developer_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" onload="this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/styles/output.css">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Abhi Labs",
    "url": "https://abhilabs.app",
    "description": "Premium Android app studio based in Bangalore, India.",
    "contactPoint": { "@type": "ContactPoint", "email": "contact@abhilabs.app" }
  }
  </script>
</head>
<body>
<a href="#main-content" class="skip-link">Skip to content</a>

<header class="site-header" role="banner">
  <nav class="nav-container" aria-label="Main navigation">
    <a href="/" class="nav-logo" aria-label="Abhi Labs home">
      <span class="nav-logo-mark">AL</span>
      <span class="nav-logo-text">Abhi Labs</span>
    </a>
    <ul class="nav-links" role="list" id="nav-menu">
      <li><a href="/" class="nav-link" aria-current="page">Portfolio</a></li>
      <li><a href="/about/" class="nav-link">About</a></li>
      <li><a href="mailto:contact@abhilabs.app" class="nav-cta">Contact</a></li>
    </ul>
    <button class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </button>
  </nav>
</header>

<main id="main-content">

  <!-- Hero -->
  <section class="home-hero" aria-label="Introduction">
    <div class="home-hero__orb" aria-hidden="true"></div>
    <div style="position:relative;z-index:2">
      <p class="home-hero__label">
        <svg width="8" height="8" viewBox="0 0 8 8" fill="currentColor" aria-hidden="true"><circle cx="4" cy="4" r="4"/></svg>
        Bangalore, India · Android Studio
      </p>
      <h1 class="home-hero__title">Premium Android<br>Apps. No Compromise.</h1>
      <p class="home-hero__sub">Offline-first. Privacy-first. Beautifully built.</p>
    </div>
  </section>

  <!-- App Grid -->
  <section id="portfolio" class="app-grid-section" aria-label="App portfolio">
    <h2 class="sr-only">Our Apps</h2>
    <div class="app-grid">

      <!-- AbhiScan Pro — FEATURED -->
      <a href="/apps/abhi-scan/" class="app-card app-card--featured app-card--featured-1" style="--accent:#0d9488" aria-label="AbhiScan Pro — view app">
        <div class="app-card__border-glow" aria-hidden="true"></div>
        <div>
          <div class="app-card__badge app-card__badge--featured" style="--accent:#0d9488">Featured · Scanner</div>
          <h3 class="app-card__name">AbhiScan Pro</h3>
          <p class="app-card__tagline">Professional offline PDF scanner with OpenCV edge detection and full-text OCR search.</p>
          <ul class="app-card__features">
            <li>OpenCV Auto Edge Detection</li>
            <li>Full-Text OCR Search</li>
            <li>7 Scan Modes · Batch 35 pages</li>
          </ul>
        </div>
        <div class="app-card__phone-wrap">
          <div class="phone-mockup phone-mockup--sm phone-mockup--card">
            <div class="phone-mockup__frame">
              <div class="phone-mockup__top">
                <div class="phone-mockup__speaker"></div>
                <div class="phone-mockup__camera"></div>
              </div>
              <div class="phone-mockup__screen">
                <img src="/apps/abhi-scan/assets/1.png" alt="AbhiScan Pro scanning interface" width="136" height="280" loading="lazy">
              </div>
            </div>
          </div>
        </div>
        <div class="app-card__cta">
          Explore<span class="sr-only"> AbhiScan Pro</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </a>

      <!-- Lunavi — FEATURED -->
      <a href="/apps/lunavi/" class="app-card app-card--featured app-card--featured-2" style="--accent:#e11d48" aria-label="Lunavi — view app">
        <div class="app-card__border-glow" aria-hidden="true"></div>
        <div>
          <div class="app-card__badge app-card__badge--featured" style="--accent:#e11d48">Featured · Health</div>
          <h3 class="app-card__name">Lunavi</h3>
          <p class="app-card__tagline">Your cycle, your data. AI ovulation predictions that never leave your device.</p>
          <ul class="app-card__features">
            <li>AI Ovulation Predictions</li>
            <li>100% Offline · Zero Ads</li>
            <li>Mood &amp; Symptom Tracking</li>
          </ul>
        </div>
        <div class="app-card__phone-wrap">
          <div class="phone-mockup phone-mockup--sm phone-mockup--card">
            <div class="phone-mockup__frame">
              <div class="phone-mockup__top">
                <div class="phone-mockup__speaker"></div>
                <div class="phone-mockup__camera"></div>
              </div>
              <div class="phone-mockup__screen">
                <img src="/apps/lunavi/assets/1.png" alt="Lunavi cycle tracking" width="136" height="280" loading="lazy">
              </div>
            </div>
          </div>
        </div>
        <div class="app-card__cta">
          Explore<span class="sr-only"> Lunavi</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </a>

      <!-- AbhiScan Lite — standard -->
      <a href="/apps/abhi-scan-lite/" class="app-card app-card--standard-1" style="--accent:#0d9488" aria-label="AbhiScan Lite — view app">
        <div class="app-card__border-glow" aria-hidden="true"></div>
        <div class="app-card__initial">AS</div>
        <div class="app-card__badge">Scanner · Lite</div>
        <h3 class="app-card__name">AbhiScan Lite</h3>
        <p class="app-card__tagline">Full scanner power in a featherweight 5 MB install.</p>
        <ul class="app-card__features">
          <li>5 MB Install Size</li>
          <li>Offline Always</li>
        </ul>
        <div class="app-card__cta">
          Explore<span class="sr-only"> AbhiScan Lite</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </a>

      <!-- AbhiNidra — standard -->
      <a href="/apps/abhinidra/" class="app-card app-card--standard-2" style="--accent:#6366f1" aria-label="AbhiNidra — view app">
        <div class="app-card__border-glow" aria-hidden="true"></div>
        <div class="app-card__initial">AN</div>
        <div class="app-card__badge">Sleep · Sounds</div>
        <h3 class="app-card__name">AbhiNidra</h3>
        <p class="app-card__tagline">Sleep sounds with adaptive volume. Your sleep is private.</p>
        <ul class="app-card__features">
          <li>50+ Sleep Sounds</li>
          <li>Adaptive Volume</li>
        </ul>
        <div class="app-card__cta">
          Explore<span class="sr-only"> AbhiNidra</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </a>

      <!-- AI QR Barcode — standard -->
      <a href="/apps/ai-qr-barcode/" class="app-card app-card--standard-3" style="--accent:#0d9488" aria-label="AI QR Barcode — view app">
        <div class="app-card__border-glow" aria-hidden="true"></div>
        <div class="app-card__initial">QR</div>
        <div class="app-card__badge">Scanner · AI</div>
        <h3 class="app-card__name">AI QR Barcode</h3>
        <p class="app-card__tagline">Every code format. AI safety check. All on-device.</p>
        <ul class="app-card__features">
          <li>ML Kit Safety Verify</li>
          <li>Create QR Codes</li>
        </ul>
        <div class="app-card__cta">
          Explore<span class="sr-only"> AI QR Barcode</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </a>

    </div>
  </section>

</main>

<footer class="site-footer" role="contentinfo">
  <p class="footer-copy">© 2026 Abhi Labs. Bangalore, India. · <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a></p>
</footer>

<script>
  const btn = document.querySelector('.nav-hamburger');
  const links = document.querySelector('.nav-links');
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    links.classList.toggle('nav-links--open');
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-container')) {
      btn.setAttribute('aria-expanded', 'false');
      links.classList.remove('nav-links--open');
    }
  });
</script>
</body>
</html>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: exits 0.

- [ ] **Step 3: Visual verification**

Open `http://localhost:3100`. Verify:
- Dark background `#08080a`
- Hero headline renders at display size
- 2 featured cards (AbhiScan Pro, Lunavi) fill top row equally
- 3 standard cards fill bottom row equally
- Hover on any card: background shifts to app's accent color tint, phone un-tilts and glows, border glows
- Mobile (< 600px in DevTools): all cards stack single column

- [ ] **Step 4: Commit**

```bash
git add index.html styles/output.css
git commit -m "feat: premium homepage — dark hero, featured card grid with hover world-shift"
```

---

### Task 3: About Page (`about/index.html`)

**Files:**
- Modify: `about/index.html` (full rewrite)

**Interfaces:**
- Consumes: CSS from Task 1 (`.about-hero`, `.about-values`, `.about-value`, `.about-contact`, `.social-proof-strip`)

- [ ] **Step 1: Write `about/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/developer_logo.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About — Abhi Labs</title>
  <meta name="description" content="Abhi Labs is a Bangalore-based Android app studio. Offline-first, privacy-first, quality-obsessed.">
  <link rel="canonical" href="https://abhilabs.app/about/">
  <meta property="og:title" content="About — Abhi Labs">
  <meta property="og:description" content="Abhi Labs is a Bangalore-based Android app studio. Offline-first, privacy-first, quality-obsessed.">
  <meta property="og:url" content="https://abhilabs.app/about/">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="og:image" content="https://abhilabs.app/assets/developer_logo.png">
  <meta name="twitter:image" content="https://abhilabs.app/assets/developer_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" onload="this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/styles/output.css">
</head>
<body>
<a href="#main-content" class="skip-link">Skip to content</a>

<header class="site-header" role="banner">
  <nav class="nav-container" aria-label="Main navigation">
    <a href="/" class="nav-logo" aria-label="Abhi Labs home">
      <span class="nav-logo-mark">AL</span>
      <span class="nav-logo-text">Abhi Labs</span>
    </a>
    <ul class="nav-links" role="list" id="nav-menu">
      <li><a href="/" class="nav-link">Portfolio</a></li>
      <li><a href="/about/" class="nav-link" aria-current="page">About</a></li>
      <li><a href="mailto:contact@abhilabs.app" class="nav-cta">Contact</a></li>
    </ul>
    <button class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </button>
  </nav>
</header>

<main id="main-content">

  <section class="about-hero" aria-label="Studio introduction">
    <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);margin-bottom:1.25rem">Bangalore, India</p>
    <h1 class="about-hero__title">We build software<br>people love to use.</h1>
    <p class="about-hero__desc">Abhi Labs is an independent Android app studio focused on offline-first, privacy-respecting apps that feel premium on any device.</p>
  </section>

  <div class="about-values" role="list" aria-label="Our values">
    <div class="about-value" role="listitem">
      <span class="about-value__num" aria-hidden="true">01</span>
      <h2 class="about-value__name">Offline-First</h2>
      <p class="about-value__desc">Every app works completely without internet. No cloud dependency, no service outages, no waiting for a server response.</p>
    </div>
    <div class="about-value" role="listitem">
      <span class="about-value__num" aria-hidden="true">02</span>
      <h2 class="about-value__name">Privacy-First</h2>
      <p class="about-value__desc">Your data never leaves your device unless you explicitly share it. We don't operate user data servers. We can't see your data because we never receive it.</p>
    </div>
    <div class="about-value" role="listitem">
      <span class="about-value__num" aria-hidden="true">03</span>
      <h2 class="about-value__name">Quality-Obsessed</h2>
      <p class="about-value__desc">No subscriptions. No dark patterns. No feature bloat. Every app ships when it's genuinely good — not when a roadmap says so.</p>
    </div>
  </div>

  <div class="social-proof-strip" aria-label="Studio stats">
    <div class="social-proof-inner">
      <div class="social-stat">
        <span class="social-stat__value">5</span>
        <span class="social-stat__label">Apps Published</span>
        <span class="social-stat__sub">on Google Play</span>
      </div>
      <div class="social-stat">
        <span class="social-stat__value">10+</span>
        <span class="social-stat__label">Years Android</span>
        <span class="social-stat__sub">development experience</span>
      </div>
      <div class="social-stat">
        <span class="social-stat__value">0</span>
        <span class="social-stat__label">Subscriptions</span>
        <span class="social-stat__sub">across all apps</span>
      </div>
    </div>
  </div>

  <div class="about-contact" aria-label="Contact">
    <p class="about-contact__label">Get in touch</p>
    <a href="mailto:contact@abhilabs.app" class="about-contact__email">
      contact@abhilabs.app
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
    <p style="font-size:14px;color:var(--text-3);margin-top:1rem">Questions, feedback, or partnership inquiries — we'd love to hear from you.</p>
  </div>

</main>

<footer class="site-footer" role="contentinfo">
  <p class="footer-copy">© 2026 Abhi Labs. Bangalore, India. · <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a></p>
</footer>

<script>
  const btn = document.querySelector('.nav-hamburger');
  const links = document.querySelector('.nav-links');
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    links.classList.toggle('nav-links--open');
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-container')) {
      btn.setAttribute('aria-expanded', 'false');
      links.classList.remove('nav-links--open');
    }
  });
</script>
</body>
</html>
```

- [ ] **Step 2: Build and verify**

```bash
npm run build
```

Open `http://localhost:3100/about/`. Verify:
- Display headline renders correctly
- 3 value cards in a row (desktop), stacked (mobile < 768px)
- Stats strip with accent-colored numbers
- Email link has underline animation on hover
- Mobile: values stack to 1 column

- [ ] **Step 3: Commit**

```bash
git add about/index.html styles/output.css
git commit -m "feat: premium about page — values grid, stats strip, contact"
```

---

### Task 4: AbhiScan Pro App Page (`apps/abhi-scan/index.html`)

**Files:**
- Modify: `apps/abhi-scan/index.html` (full rewrite)

**Interfaces:**
- Consumes: CSS from Task 1. GSAP 3.12.5 + ScrollTrigger from cdnjs.
- Produces: pattern for Tasks 5–8 (same structure, different content/world/screenshots)

**Screenshot sequence:** `assets/1.png` → `assets/2.png` → `assets/3.png` → `assets/4.png` → `assets/5.png` → `assets/6.png`

**World class on `<html>`:** `app-abhiscan`
**Body classes:** `has-noise world-scanline`

- [ ] **Step 1: Write `apps/abhi-scan/index.html`**

```html
<!DOCTYPE html>
<html lang="en" class="app-abhiscan">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/developer_logo.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AbhiScan Pro — Professional Document Scanner | Abhi Labs</title>
  <meta name="description" content="Professional offline PDF scanner with OpenCV edge detection, full-text OCR search, and 7 scan modes. No cloud. No subscription.">
  <link rel="canonical" href="https://abhilabs.app/apps/abhi-scan/">
  <meta property="og:title" content="AbhiScan Pro — Professional Document Scanner">
  <meta property="og:description" content="Professional offline PDF scanner with OpenCV edge detection, full-text OCR search, and 7 scan modes.">
  <meta property="og:url" content="https://abhilabs.app/apps/abhi-scan/">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="og:image" content="https://abhilabs.app/assets/developer_logo.png">
  <meta name="twitter:image" content="https://abhilabs.app/assets/developer_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" onload="this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/styles/output.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MobileApplication",
    "name": "AbhiScan Pro",
    "operatingSystem": "Android",
    "applicationCategory": "UtilitiesApplication",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "url": "https://play.google.com/store/apps/details?id=com.abhilabs.pdfscanner"
  }
  </script>
</head>
<body class="has-noise world-scanline">
<a href="#main-content" class="skip-link">Skip to content</a>

<header class="site-header" role="banner">
  <nav class="nav-container" aria-label="Main navigation">
    <a href="/" class="nav-logo" aria-label="Abhi Labs home">
      <span class="nav-logo-mark">AL</span>
      <span class="nav-logo-text">Abhi Labs</span>
    </a>
    <ul class="nav-links" role="list" id="nav-menu">
      <li><a href="/" class="nav-link">Portfolio</a></li>
      <li><a href="/about/" class="nav-link">About</a></li>
      <li><a href="mailto:contact@abhilabs.app" class="nav-cta">Contact</a></li>
    </ul>
    <button class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </button>
  </nav>
</header>

<main id="main-content">

  <!-- Hero -->
  <section class="app-hero" aria-label="AbhiScan Pro overview">
    <div class="app-hero__text">
      <p class="app-hero__label">Document Scanner · Abhi Labs</p>
      <h1 class="app-hero__title">AbhiScan Pro</h1>
      <p class="app-hero__tagline">Professional document scanning. Entirely on your phone.</p>
      <ul class="app-hero__bullets">
        <li>OpenCV auto edge detection</li>
        <li>Full-text OCR search</li>
        <li>7 scan modes · Batch 35 pages</li>
      </ul>
      <a href="https://play.google.com/store/apps/details?id=com.abhilabs.pdfscanner" class="btn-primary" target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor" aria-hidden="true"><path d="M1 1l16 8-16 8V1z"/></svg>
        Get on Google Play
      </a>
      <p style="margin-top:.75rem;font-size:13px;color:var(--text-3)">
        Free · No subscription · <a href="/privacy/abhiscan/" style="color:var(--text-3)">Privacy Policy</a>
      </p>
    </div>
    <div class="app-hero__phone" aria-hidden="true">
      <div class="phone-mockup phone-mockup--lg phone-mockup--hero">
        <div class="phone-mockup__frame">
          <div class="phone-mockup__top">
            <div class="phone-mockup__speaker"></div>
            <div class="phone-mockup__camera"></div>
          </div>
          <div class="phone-mockup__screen">
            <img src="assets/1.png" alt="AbhiScan Pro main screen" width="260" height="536" fetchpriority="high">
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Scroll-driven features -->
  <section class="feature-scroll-section" aria-label="Features">
    <div class="feature-scroll-inner">
      <div class="feature-scroll__phone" aria-hidden="true">
        <div class="phone-mockup phone-mockup--lg phone-mockup--sticky">
          <div class="phone-mockup__frame">
            <div class="phone-mockup__top">
              <div class="phone-mockup__speaker"></div>
              <div class="phone-mockup__camera"></div>
            </div>
            <div class="phone-mockup__screen">
              <img src="assets/1.png" alt="" class="phone-screen" id="sticky-screen" width="260" height="536" loading="lazy">
            </div>
          </div>
        </div>
      </div>
      <div class="feature-scroll__content">
        <div class="feature-item is-active" data-screenshot="assets/1.png">
          <span class="feature-num" aria-hidden="true">01</span>
          <h2 class="feature-name">Auto Edge Detection</h2>
          <p class="feature-desc">OpenCV precision cropping finds your document's edges from any angle, any lighting. Point, shoot, done.</p>
          <span class="feature-tag">ON_DEVICE_OPENCV</span>
        </div>
        <div class="feature-item" data-screenshot="assets/2.png">
          <span class="feature-num" aria-hidden="true">02</span>
          <h2 class="feature-name">Full-Text OCR Search</h2>
          <p class="feature-desc">Every word in every scan is indexed locally in SQLite FTS4. Find any document by searching its content.</p>
          <span class="feature-tag">SQLITE_FTS4_LOCAL</span>
        </div>
        <div class="feature-item" data-screenshot="assets/3.png">
          <span class="feature-num" aria-hidden="true">03</span>
          <h2 class="feature-name">7 Scan Modes</h2>
          <p class="feature-desc">Documents, receipts, business cards, whiteboards, books, ID cards, and photos. A mode built for every surface.</p>
        </div>
        <div class="feature-item" data-screenshot="assets/4.png">
          <span class="feature-num" aria-hidden="true">04</span>
          <h2 class="feature-name">Magic Color Enhancement</h2>
          <p class="feature-desc">Adaptive contrast makes text crisp and readable in any lighting — fluorescent office, dim room, bright sunlight.</p>
          <span class="feature-tag">ADAPTIVE_CONTRAST</span>
        </div>
        <div class="feature-item" data-screenshot="assets/5.png">
          <span class="feature-num" aria-hidden="true">05</span>
          <h2 class="feature-name">Batch Scanning</h2>
          <p class="feature-desc">Scan up to 35 pages in a single session and merge them into one PDF. Contracts, reports, books — done in one go.</p>
        </div>
        <div class="feature-item" data-screenshot="assets/6.png">
          <span class="feature-num" aria-hidden="true">06</span>
          <h2 class="feature-name">Export &amp; Share</h2>
          <p class="feature-desc">Export as PDF or JPEG. Share directly to any app on your phone. Your files, your way, no cloud required.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Social proof -->
  <div class="social-proof-strip" aria-label="App stats">
    <div class="social-proof-inner">
      <div class="social-stat">
        <span class="social-stat__value">★ 4.6</span>
        <span class="social-stat__label">Google Play Rating</span>
        <span class="social-stat__sub">by verified users</span>
      </div>
      <div class="social-stat">
        <span class="social-stat__value">10K+</span>
        <span class="social-stat__label">Downloads</span>
        <span class="social-stat__sub">and counting</span>
      </div>
      <div class="social-stat">
        <span class="social-stat__value">0</span>
        <span class="social-stat__label">Cloud Uploads</span>
        <span class="social-stat__sub">ever, by design</span>
      </div>
    </div>
  </div>

  <!-- Download CTA -->
  <section class="download-cta" aria-label="Download AbhiScan Pro">
    <h2 class="download-cta__heading">Ready to scan smarter?</h2>
    <p class="download-cta__sub">Free · No subscription · No account required</p>
    <a href="https://play.google.com/store/apps/details?id=com.abhilabs.pdfscanner" class="play-badge" target="_blank" rel="noopener" aria-label="Get AbhiScan Pro on Google Play">
      <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" alt="Get it on Google Play" width="200" height="77" loading="lazy">
    </a>
  </section>

</main>

<footer class="site-footer" role="contentinfo">
  <p class="footer-copy">© 2026 Abhi Labs. Bangalore, India. · <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a></p>
</footer>

<script>
  /* Nav hamburger */
  const btn = document.querySelector('.nav-hamburger');
  const navLinks = document.querySelector('.nav-links');
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    navLinks.classList.toggle('nav-links--open');
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-container')) {
      btn.setAttribute('aria-expanded', 'false');
      navLinks.classList.remove('nav-links--open');
    }
  });
</script>
<script>
  /* GSAP scroll-driven phone */
  (function () {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) {
      document.querySelectorAll('.feature-item').forEach(function (el) { el.style.opacity = '1'; });
      return;
    }
    var mobile = window.innerWidth < 768;
    if (mobile) {
      document.querySelectorAll('.feature-item').forEach(function (el) { el.style.opacity = '1'; });
      return;
    }
    window.addEventListener('load', function () {
      if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        document.querySelectorAll('.feature-item').forEach(function (el) { el.style.opacity = '1'; });
        return;
      }
      gsap.registerPlugin(ScrollTrigger);
      var screen = document.getElementById('sticky-screen');

      document.querySelectorAll('.feature-item').forEach(function (item) {
        ScrollTrigger.create({
          trigger: item,
          start: 'top 60%',
          end: 'bottom 40%',
          onEnter: function () { swap(item.dataset.screenshot); activate(item); },
          onEnterBack: function () { swap(item.dataset.screenshot); activate(item); },
        });
      });

      function swap(src) {
        if (!screen) return;
        var filename = src.split('/').pop();
        if (screen.src.endsWith(filename)) return;
        gsap.to(screen, {
          opacity: 0, duration: 0.15,
          onComplete: function () {
            screen.src = src;
            gsap.to(screen, { opacity: 1, duration: 0.25 });
          }
        });
      }

      function activate(active) {
        document.querySelectorAll('.feature-item').forEach(function (el) { el.classList.remove('is-active'); });
        active.classList.add('is-active');
      }
    });
  })();
</script>
</body>
</html>
```

- [ ] **Step 2: Build**

```bash
npm run build
```

Expected: exits 0.

- [ ] **Step 3: Visual verification**

Open `http://localhost:3100/apps/abhi-scan/`. Verify:
- Teal radial glow visible in top-right of background
- Scan-line animation sweeps slowly top to bottom (very subtle, ~4% opacity)
- Hero: phone mockup tilted with teal glow drop-shadow + float animation
- Scroll down: phone panel stays sticky on left, feature items scroll on right
- As each feature item enters viewport center: phone screen cross-fades to its screenshot, item brightens to full opacity, others dim to 25%
- Mobile (< 768px in DevTools): sticky collapses, all features show at full opacity, no GSAP
- Check with System Settings → Accessibility → Reduce Motion: animations stop, all items show at full opacity

- [ ] **Step 4: Commit**

```bash
git add apps/abhi-scan/index.html styles/output.css
git commit -m "feat: AbhiScan Pro premium page — teal world, scroll-driven phone, GSAP features"
```

---

### Task 5: Lunavi App Page (`apps/lunavi/index.html`)

**Files:**
- Modify: `apps/lunavi/index.html` (full rewrite)

**World class on `<html>`:** `app-lunavi`
**Body classes:** `has-noise world-heartbeat`
**Screenshot sequence:** `assets/1.png` → `assets/2.png` → `assets/3.png` → `assets/4.png` → `assets/5.png` → `assets/6.png` → `assets/7.png` → `assets/8.png`
**Play Store ID:** `com.abhilabs.lunavi`

- [ ] **Step 1: Write `apps/lunavi/index.html`**

Same full HTML structure as Task 4 with these substitutions:

**`<html>` class:** `app-lunavi`
**`<body>` class:** `has-noise world-heartbeat`
**`<title>`:** `Lunavi — Cycle Tracker & Ovulation App | Abhi Labs`
**`<meta name="description">`:** `AI ovulation predictions and cycle tracking entirely on your device. No cloud, no ads, no compromise.`
**Canonical URL:** `https://abhilabs.app/apps/lunavi/`
**OG title:** `Lunavi — Cycle Tracker & Ovulation App`
**JSON-LD name:** `Lunavi`, **Play URL:** `https://play.google.com/store/apps/details?id=com.abhilabs.lunavi`
**Hero label:** `Cycle Tracker · Abhi Labs`
**Hero title:** `Lunavi`
**Hero tagline:** `Your cycle, your data. No cloud. No compromise.`
**Hero bullets:** `AI ovulation predictions` / `100% offline — zero cloud` / `Zero advertisements, ever`
**Play Store link:** `https://play.google.com/store/apps/details?id=com.abhilabs.lunavi`
**Privacy link:** `/privacy/lunavi/`
**Sticky screen ID:** `sticky-screen` (same)
**First screenshot:** `assets/1.png` (hero img `src` AND `fetchpriority="high"`)

**Feature items:**
```html
<div class="feature-item is-active" data-screenshot="assets/1.png">
  <span class="feature-num" aria-hidden="true">01</span>
  <h2 class="feature-name">AI Ovulation Predictions</h2>
  <p class="feature-desc">On-device machine learning predicts your fertile window. Predictions update as your cycle data grows — no internet, no cloud.</p>
  <span class="feature-tag">ON_DEVICE_ML</span>
</div>
<div class="feature-item" data-screenshot="assets/2.png">
  <span class="feature-num" aria-hidden="true">02</span>
  <h2 class="feature-name">Cycle Tracking</h2>
  <p class="feature-desc">Log period start and end, flow intensity, and symptoms. Lunavi builds your personal baseline over time.</p>
</div>
<div class="feature-item" data-screenshot="assets/3.png">
  <span class="feature-num" aria-hidden="true">03</span>
  <h2 class="feature-name">Mood Logging</h2>
  <p class="feature-desc">Track emotional patterns alongside your cycle. See which moods correlate with which phase over months of data.</p>
</div>
<div class="feature-item" data-screenshot="assets/4.png">
  <span class="feature-num" aria-hidden="true">04</span>
  <h2 class="feature-name">Cycle Insights</h2>
  <p class="feature-desc">Beautiful charts show your patterns across months. Cycle length trends, symptom frequency, mood shifts — all local, all private.</p>
</div>
<div class="feature-item" data-screenshot="assets/5.png">
  <span class="feature-num" aria-hidden="true">05</span>
  <h2 class="feature-name">Zero Advertisements</h2>
  <p class="feature-desc">Lunavi contains no advertising SDKs. Not a single ad, ever. Your health data is not a product.</p>
  <span class="feature-tag">ZERO_ADS</span>
</div>
<div class="feature-item" data-screenshot="assets/6.png">
  <span class="feature-num" aria-hidden="true">06</span>
  <h2 class="feature-name">Privacy by Architecture</h2>
  <p class="feature-desc">All data is stored in a local Android Room database. The developer has no server to receive your data — because there isn't one.</p>
  <span class="feature-tag">LOCAL_ROOM_DB</span>
</div>
<div class="feature-item" data-screenshot="assets/7.png">
  <span class="feature-num" aria-hidden="true">07</span>
  <h2 class="feature-name">Private Reminders</h2>
  <p class="feature-desc">Period and fertile window reminders are local notifications. Nothing leaves your device to deliver them.</p>
</div>
<div class="feature-item" data-screenshot="assets/8.png">
  <span class="feature-num" aria-hidden="true">08</span>
  <h2 class="feature-name">Data Export</h2>
  <p class="feature-desc">Export your complete cycle history to a file whenever you want. Your data, your file, on your terms.</p>
</div>
```

**Social proof stats:**
- `★ 4.7` / Google Play Rating / by verified users
- `50K+` / Downloads / and counting
- `0` / Cloud Uploads / ever, by design

**Download CTA heading:** `Ready to understand your cycle?`
**Download CTA sub:** `Free · No subscription · No account · No ads`
**Play Store link (CTA):** `https://play.google.com/store/apps/details?id=com.abhilabs.lunavi`

GSAP script: copy exactly from Task 4 — identical JS, the data-screenshot attributes on `.feature-item` elements drive the behavior.

- [ ] **Step 2: Build**

```bash
npm run build
```

- [ ] **Step 3: Visual verification**

Open `http://localhost:3100/apps/lunavi/`. Verify:
- Background has crimson/rose radial gradient (not teal)
- Heartbeat pulse animation visible on background (very subtle, ~3–6% opacity)
- All 8 features scroll correctly, phone advances through 8 screenshots
- Mobile and reduced-motion fallbacks work as in Task 4

- [ ] **Step 4: Commit**

```bash
git add apps/lunavi/index.html styles/output.css
git commit -m "feat: Lunavi premium page — crimson world, heartbeat pulse, 8-feature scroll"
```

---

### Task 6: AbhiScan Lite App Page (`apps/abhi-scan-lite/index.html`)

**Files:**
- Modify: `apps/abhi-scan-lite/index.html` (full rewrite)

**World class on `<html>`:** `app-abhiscan`
**Body classes:** `has-noise world-scanline`
**Screenshot sequence:** `assets/screen-1.png` → `assets/screen-2.png` → `assets/screen-3.png` → `assets/screen-4.png` → `assets/screen-5.png` → `assets/screen-6.png` → `assets/screen-7.png`
**Play Store ID:** `com.abhilabs.pdfscannerlite`

- [ ] **Step 1: Write `apps/abhi-scan-lite/index.html`**

Same full HTML structure as Task 4 with these substitutions:

**`<html>` class:** `app-abhiscan`
**`<body>` class:** `has-noise world-scanline`
**`<title>`:** `AbhiScan Lite — Lightweight PDF Scanner | Abhi Labs`
**`<meta name="description">`:** `Full scanner power in a featherweight 5 MB install. Offline-first, privacy-first, subscription-free.`
**Canonical:** `https://abhilabs.app/apps/abhi-scan-lite/`
**OG title:** `AbhiScan Lite — Lightweight PDF Scanner`
**JSON-LD name:** `AbhiScan Lite`, **Play URL:** `https://play.google.com/store/apps/details?id=com.abhilabs.pdfscannerlite`
**Hero label:** `Document Scanner · Lite · Abhi Labs`
**Hero title:** `AbhiScan Lite`
**Hero tagline:** `All the power of AbhiScan in a featherweight 5 MB install.`
**Hero bullets:** `5 MB install size` / `Auto edge detection · Offline always` / `35-page batch mode`
**Play Store link:** `https://play.google.com/store/apps/details?id=com.abhilabs.pdfscannerlite`
**Privacy link:** `/privacy/abhiscan-lite/`
**First screenshot:** `assets/screen-1.png`

**Feature items:**
```html
<div class="feature-item is-active" data-screenshot="assets/screen-1.png">
  <span class="feature-num" aria-hidden="true">01</span>
  <h2 class="feature-name">Auto Edge Detection</h2>
  <p class="feature-desc">On-device precision cropping finds document edges automatically. No manual adjustment needed.</p>
  <span class="feature-tag">ON_DEVICE_PROCESSING</span>
</div>
<div class="feature-item" data-screenshot="assets/screen-2.png">
  <span class="feature-num" aria-hidden="true">02</span>
  <h2 class="feature-name">Privacy Mode</h2>
  <p class="feature-desc">Scans never leave your device. No cloud upload, no sync, no account. What you scan stays with you.</p>
  <span class="feature-tag">ZERO_CLOUD</span>
</div>
<div class="feature-item" data-screenshot="assets/screen-3.png">
  <span class="feature-num" aria-hidden="true">03</span>
  <h2 class="feature-name">5 MB Install</h2>
  <p class="feature-desc">Half the size of competing scanners. AbhiScan Lite fits on any device without hogging storage.</p>
</div>
<div class="feature-item" data-screenshot="assets/screen-4.png">
  <span class="feature-num" aria-hidden="true">04</span>
  <h2 class="feature-name">35-Page Batch Mode</h2>
  <p class="feature-desc">Scan entire documents, reports, or manuals in a single session. Merge all pages into one clean PDF.</p>
</div>
<div class="feature-item" data-screenshot="assets/screen-5.png">
  <span class="feature-num" aria-hidden="true">05</span>
  <h2 class="feature-name">No Account Required</h2>
  <p class="feature-desc">Open the app, start scanning. No sign-up, no email, no password, no terms-of-service trap.</p>
</div>
<div class="feature-item" data-screenshot="assets/screen-6.png">
  <span class="feature-num" aria-hidden="true">06</span>
  <h2 class="feature-name">Professional PDF Output</h2>
  <p class="feature-desc">Generates clean, properly formatted PDFs ready for email, print, or archiving. Quality matches scanners twice the size.</p>
</div>
<div class="feature-item" data-screenshot="assets/screen-7.png">
  <span class="feature-num" aria-hidden="true">07</span>
  <h2 class="feature-name">Offline Always</h2>
  <p class="feature-desc">Works in airplane mode, basements, rural areas — anywhere. No internet connection ever needed to scan.</p>
</div>
```

**Social proof:** `★ 4.5` / `5K+` Downloads / `0` Cloud Uploads
**Download CTA heading:** `Ready to scan without the bloat?`
**Download CTA sub:** `Free · No subscription · No account required`

GSAP script: copy exactly from Task 4.

- [ ] **Step 2: Build, verify, commit**

```bash
npm run build
```

Open `http://localhost:3100/apps/abhi-scan-lite/`. Verify teal world active, 7 screenshots advance on scroll.

```bash
git add apps/abhi-scan-lite/index.html styles/output.css
git commit -m "feat: AbhiScan Lite premium page — teal world, 7-feature scroll"
```

---

### Task 7: AbhiNidra App Page (`apps/abhinidra/index.html`)

**Files:**
- Modify: `apps/abhinidra/index.html` (full rewrite)

**World class on `<html>`:** `app-abhinidra`
**Body classes:** `has-noise world-wave`
**Screenshot sequence:** `assets/1.png` → `assets/2.png` → `assets/3.png` → `assets/4.png` → `assets/5.png` → `assets/6.png` → `assets/7.png` → `assets/8.png`
**Play Store ID:** `com.abhilabs.abhinidra`

- [ ] **Step 1: Write `apps/abhinidra/index.html`**

Same full HTML structure as Task 4 with these substitutions:

**`<html>` class:** `app-abhinidra`
**`<body>` class:** `has-noise world-wave`
**`<title>`:** `AbhiNidra — Sleep Sounds & White Noise | Abhi Labs`
**`<meta name="description">`:** `50+ sleep sounds with adaptive volume. Your sleep is private — no cloud, no data collection.`
**Canonical:** `https://abhilabs.app/apps/abhinidra/`
**OG title:** `AbhiNidra — Sleep Sounds & White Noise`
**JSON-LD name:** `AbhiNidra`, **Play URL:** `https://play.google.com/store/apps/details?id=com.abhilabs.abhinidra`
**Hero label:** `Sleep Sounds · Abhi Labs`
**Hero title:** `AbhiNidra`
**Hero tagline:** `Your sleep is private. 50+ sounds, adaptive volume, zero data collection.`
**Hero bullets:** `50+ scientifically selected sleep sounds` / `Adaptive Volume — ambient-aware, audio discarded instantly` / `Ads only in menus — never during sleep`
**Play Store link:** `https://play.google.com/store/apps/details?id=com.abhilabs.abhinidra`
**Privacy link:** `/privacy/abhinidra/`
**First screenshot:** `assets/1.png`

**Feature items:**
```html
<div class="feature-item is-active" data-screenshot="assets/1.png">
  <span class="feature-num" aria-hidden="true">01</span>
  <h2 class="feature-name">Sleep Sound Library</h2>
  <p class="feature-desc">50+ sounds selected for sleep science: rain, brown noise, ocean waves, forest, fans, and more. All stored locally — no streaming.</p>
  <span class="feature-tag">LOCAL_AUDIO_LIBRARY</span>
</div>
<div class="feature-item" data-screenshot="assets/2.png">
  <span class="feature-num" aria-hidden="true">02</span>
  <h2 class="feature-name">Adaptive Volume</h2>
  <p class="feature-desc">The optional microphone feature detects ambient noise and adjusts playback volume automatically. Audio is discarded within milliseconds — never stored or transmitted.</p>
  <span class="feature-tag">AUDIO_DISCARDED_INSTANTLY</span>
</div>
<div class="feature-item" data-screenshot="assets/3.png">
  <span class="feature-num" aria-hidden="true">03</span>
  <h2 class="feature-name">Sleep Timer</h2>
  <p class="feature-desc">Set sounds to fade out after 15, 30, 60, or 90 minutes. Fall asleep without worrying about draining your battery all night.</p>
</div>
<div class="feature-item" data-screenshot="assets/4.png">
  <span class="feature-num" aria-hidden="true">04</span>
  <h2 class="feature-name">Mix Sounds</h2>
  <p class="feature-desc">Layer up to 3 sounds at custom volumes to create your perfect sleep environment. Rain + fan + distant thunder? Done.</p>
</div>
<div class="feature-item" data-screenshot="assets/5.png">
  <span class="feature-num" aria-hidden="true">05</span>
  <h2 class="feature-name">Sleep Journal</h2>
  <p class="feature-desc">Log how you slept each morning. Spot patterns between sound choices and sleep quality — all stored locally.</p>
</div>
<div class="feature-item" data-screenshot="assets/6.png">
  <span class="feature-num" aria-hidden="true">06</span>
  <h2 class="feature-name">Baby Mode</h2>
  <p class="feature-desc">Gentle sounds curated for infant sleep, for parents and caregivers. Lullabies, womb sounds, gentle white noise.</p>
</div>
<div class="feature-item" data-screenshot="assets/7.png">
  <span class="feature-num" aria-hidden="true">07</span>
  <h2 class="feature-name">Custom Presets</h2>
  <p class="feature-desc">Save your favourite sound combinations as named presets. One tap to your perfect sleep setup every night.</p>
</div>
<div class="feature-item" data-screenshot="assets/8.png">
  <span class="feature-num" aria-hidden="true">08</span>
  <h2 class="feature-name">Ad-Free During Sleep</h2>
  <p class="feature-desc">Ads appear only in navigation menus — never during active playback or sleep sessions. Your rest is uninterrupted.</p>
  <span class="feature-tag">ADS_NEVER_DURING_SLEEP</span>
</div>
```

**Social proof:** `★ 4.6` / `20K+` Downloads / `0` Sleep Interruptions
**Download CTA heading:** `Ready to sleep better?`
**Download CTA sub:** `Free · No subscription · No account required`

GSAP script: copy exactly from Task 4.

- [ ] **Step 2: Build, verify, commit**

```bash
npm run build
```

Open `http://localhost:3100/apps/abhinidra/`. Verify indigo world, wave animation on bottom edge, 8 screenshots advance.

```bash
git add apps/abhinidra/index.html styles/output.css
git commit -m "feat: AbhiNidra premium page — indigo world, wave bg, 8-feature scroll"
```

---

### Task 8: AI QR Barcode App Page (`apps/ai-qr-barcode/index.html`)

**Files:**
- Modify: `apps/ai-qr-barcode/index.html` (full rewrite)

**World class on `<html>`:** `app-ai-qr`
**Body classes:** `has-noise world-scanline`
**Screenshot sequence:** `assets/2.png` → `assets/3.png` → `assets/4.png` → `assets/5.png` → `assets/6.png` → `assets/7.png` → `assets/8.png` (no `assets/1.png`)
**Play Store ID:** `com.abhilabs.aiqrbarcodescanner`

- [ ] **Step 1: Write `apps/ai-qr-barcode/index.html`**

Same full HTML structure as Task 4 with these substitutions:

**`<html>` class:** `app-ai-qr`
**`<body>` class:** `has-noise world-scanline`
**`<title>`:** `AI QR Barcode Scanner — Every Code Format | Abhi Labs`
**`<meta name="description">`:** `Scan any QR code or barcode with AI safety verification. All on-device, scan history stored locally, no cloud.`
**Canonical:** `https://abhilabs.app/apps/ai-qr-barcode/`
**OG title:** `AI QR Barcode Scanner — Every Code Format`
**JSON-LD name:** `AI QR Barcode Scanner`, **Play URL:** `https://play.google.com/store/apps/details?id=com.abhilabs.aiqrbarcodescanner`
**Hero label:** `QR & Barcode Scanner · Abhi Labs`
**Hero title:** `AI QR Barcode`
**Hero tagline:** `Every code format. AI safety check. All on-device.`
**Hero bullets:** `QR, EAN, UPC, Code 128, Data Matrix + more` / `Google ML Kit safety verification — on-device` / `Create QR codes for URLs, WiFi, contacts`
**Play Store link:** `https://play.google.com/store/apps/details?id=com.abhilabs.aiqrbarcodescanner`
**Privacy link:** `/privacy/ai-qr-barcode/`
**First screenshot (hero img src + fetchpriority):** `assets/2.png`

**Feature items:**
```html
<div class="feature-item is-active" data-screenshot="assets/2.png">
  <span class="feature-num" aria-hidden="true">01</span>
  <h2 class="feature-name">Every Code Format</h2>
  <p class="feature-desc">QR codes, EAN-8, EAN-13, UPC-A, UPC-E, Code 128, Code 39, Data Matrix, Aztec, PDF417, and more. One scanner for every barcode you'll ever encounter.</p>
</div>
<div class="feature-item" data-screenshot="assets/3.png">
  <span class="feature-num" aria-hidden="true">02</span>
  <h2 class="feature-name">AI Safety Verification</h2>
  <p class="feature-desc">Google ML Kit checks scanned URLs for malicious content entirely on your device. No URL is sent to an external server for verification.</p>
  <span class="feature-tag">ON_DEVICE_ML_KIT</span>
</div>
<div class="feature-item" data-screenshot="assets/4.png">
  <span class="feature-num" aria-hidden="true">03</span>
  <h2 class="feature-name">WiFi Connect</h2>
  <p class="feature-desc">Scan a WiFi QR code to connect to the network instantly. No typing, no password hunting. Location permission is used only for WiFi connection — never for tracking.</p>
</div>
<div class="feature-item" data-screenshot="assets/5.png">
  <span class="feature-num" aria-hidden="true">04</span>
  <h2 class="feature-name">Local Scan History</h2>
  <p class="feature-desc">All scan history, favourites, and notes are stored in a local on-device database. Search, filter, and delete — all without touching a server.</p>
  <span class="feature-tag">LOCAL_DATABASE</span>
</div>
<div class="feature-item" data-screenshot="assets/6.png">
  <span class="feature-num" aria-hidden="true">05</span>
  <h2 class="feature-name">Create QR Codes</h2>
  <p class="feature-desc">Generate QR codes for URLs, plain text, email addresses, phone numbers, WiFi networks, and contacts. Share or save to your device.</p>
</div>
<div class="feature-item" data-screenshot="assets/7.png">
  <span class="feature-num" aria-hidden="true">06</span>
  <h2 class="feature-name">Batch Scanning</h2>
  <p class="feature-desc">Scan multiple codes in a single session without leaving the camera view. Ideal for inventory, event check-in, or retail.</p>
</div>
<div class="feature-item" data-screenshot="assets/8.png">
  <span class="feature-num" aria-hidden="true">07</span>
  <h2 class="feature-name">Full Dark Mode</h2>
  <p class="feature-desc">Complete system dark mode support — every screen, every control. Follows your device's theme automatically.</p>
</div>
```

**Social proof:** `★ 4.5` / `15K+` Downloads / `0` URLs Sent to Servers
**Download CTA heading:** `Ready to scan anything?`
**Download CTA sub:** `Free · No subscription · No account required`

GSAP script: copy exactly from Task 4.

- [ ] **Step 2: Build, verify, commit**

```bash
npm run build
```

Open `http://localhost:3100/apps/ai-qr-barcode/`. Verify teal world, 7 screenshots advance (starting from screen 2).

```bash
git add apps/ai-qr-barcode/index.html styles/output.css
git commit -m "feat: AI QR Barcode premium page — teal world, 7-feature scroll"
```

---

## Self-Review Checklist (run before handing off to SDD)

- [ ] Every `.app-card`, `.phone-mockup`, `.feature-item`, `.social-proof-strip`, `.download-cta`, `.about-values`, `.about-contact` class defined in Task 1 CSS
- [ ] All 5 app pages: `fetchpriority="high"` on hero first screenshot, `loading="lazy"` on all others including sticky phone screen
- [ ] AI QR Barcode starts at `assets/2.png` (no `assets/1.png` exists)
- [ ] AbhiScan Lite uses `screen-N.png` naming, not `N.png`
- [ ] All Play Store links use correct package IDs
- [ ] All pages: `contact@abhilabs.app`, `© 2026 Abhi Labs. Bangalore, India.`
- [ ] GSAP scripts only on app pages (Tasks 4–8), not homepage or about
- [ ] `npm run build` passes after every task
- [ ] Privacy pages untouched
