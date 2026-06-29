# abhilabs.app — Premium Redesign Spec

## Goal

Redesign abhilabs.app into a dark-luxury, motion-first marketing site that positions Abhi Labs as the most craft-focused Android app studio. Primary audience: app users arriving from Play Store. Goal sequence: **trust → understand → download**.

## Design Direction

**Dark luxury / motion-first.** Deep blacks, per-app accent color worlds, cinematic scroll-driven animations. Reference aesthetic: Linear, Raycast, Halide, Darkroom — but for Android, for app users, not developers.

**Signature interactions:**
1. **Each app = its own world** — visiting an app page transforms the entire environment (background, glow, particles) to match that app's identity
2. **Scroll-driven phone** — on app detail pages, a sticky phone mockup cross-fades between screenshots as the user scrolls through features
3. **Card hover world-shift** — on the homepage, hovering a card previews that app's world inside the card boundary

## Scope

**Full rewrite:**
- `index.html` — dramatic featured grid homepage
- `about/index.html` — premium studio page
- `apps/abhi-scan/index.html`
- `apps/abhi-scan-lite/index.html`
- `apps/lunavi/index.html`
- `apps/abhinidra/index.html`
- `apps/ai-qr-barcode/index.html`
- `styles/input.css` — extended design system

**Untouched:**
- `privacy/*/index.html` — already clean prose pages
- `404.html`
- `sitemap.xml`, `robots.txt`

## Tech Stack

- **Tailwind CLI** — keep current build (`npm run build`)
- **CSS custom properties** — extend current token system
- **GSAP 3.12.5 + ScrollTrigger** — loaded from cdnjs CDN via `defer` script tags, on app detail pages only. Homepage uses pure CSS.
- **Vanilla JS** — nav hamburger, screenshot swap logic (as fallback/complement to GSAP)
- **No new build dependencies**

## Per-App Worlds

| App | Accent | Background feel | CSS particle/texture |
|-----|--------|----------------|---------------------|
| AbhiScan Pro | `#0d9488` teal | Precision lab — deep teal radial, fine horizontal grid lines | Horizontal scan-line sweep, top→bottom, every 4s, opacity 0.03 |
| AbhiScan Lite | `#0d9488` teal | Lighter, cleaner variant of AbhiScan Pro | Same scan-line, slightly faster |
| Lunavi | `#e11d48` rose-crimson | Celestial, intimate — deep crimson radial | Slow radial pulse from center, 4s loop (heartbeat) |
| AbhiNidra | `#6366f1` indigo | Night, calm — indigo fog | Gentle vertical wave on bg edges, 6s loop |
| AI QR Barcode | `#0d9488` cyan-teal | Electric, fast — grid of faint dots | Grid dots pulse outward from center on load, settle at rest |

World gradient token:
```css
--world-gradient: radial-gradient(
  800px circle at 80% -10%,
  color-mix(in srgb, var(--accent) 15%, transparent),
  transparent 70%
);
```
Applied as `background-image` on `<body>` of app pages. Homepage uses `--brand` teal at 8% opacity.

## Design System Extensions (`styles/input.css`)

### New tokens
```css
:root {
  --noise-opacity: 0.035;
  --glow-spread: 120px;
  --card-bg: #0e0e10;
  --card-border: #1c1c1f;
  --card-hover-border: color-mix(in srgb, var(--accent) 40%, transparent);
  --card-hover-bg: color-mix(in srgb, var(--accent) 12%, var(--bg));
  --phone-frame: #1a1a1e;
  --phone-border: #2a2a2e;
  --featured-badge-bg: color-mix(in srgb, var(--accent) 20%, transparent);
}
```

### Noise texture overlay
Applied via `::before` pseudo-element on `<body>` for app pages:
```css
.has-noise::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* inline SVG noise */
  opacity: var(--noise-opacity);
  pointer-events: none;
  z-index: 0;
}
```

### CSS phone mockup component (`.phone-mockup`)
Pure CSS/HTML — no image file:
```css
.phone-mockup { /* outer frame */ }
.phone-mockup__screen { /* screenshot container */ }
.phone-mockup__speaker { /* top slit */ }
.phone-mockup__camera { /* dot */ }
.phone-mockup__btn-power { /* ::before right side */ }
.phone-mockup__btn-vol { /* ::after left side */ }
```
Dimensions: `280px × 580px` (desktop hero), `180px × 375px` (homepage cards). Same HTML structure, different size class.

### Scan-line animation (AbhiScan pages)
```css
@keyframes scanline {
  0% { transform: translateY(-100%); opacity: 0; }
  10% { opacity: 0.03; }
  90% { opacity: 0.03; }
  100% { transform: translateY(100vh); opacity: 0; }
}
.world-scanline::after {
  content: '';
  position: fixed;
  left: 0; right: 0;
  height: 2px;
  background: var(--accent);
  animation: scanline 4s linear infinite;
  pointer-events: none;
  z-index: 1;
}
```

### Heartbeat pulse (Lunavi pages)
```css
@keyframes heartbeat {
  0%, 100% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--accent) 20%, transparent); }
  50% { box-shadow: 0 0 0 40px transparent; }
}
```

## Homepage (`index.html`)

### Hero
- Viewport: `min-height: 60vh` (not full-screen — cards are the hero)
- Background: `#08080a`, single teal orb radial 800px top-right at 8% opacity
- Headline: `clamp(40px, 6vw, 72px)`, white, 2 lines:
  ```
  Premium Android
  Apps. No Compromise.
  ```
- Subhead: `Offline-first. Privacy-first. Beautifully built.` — `var(--text-2)`
- No CTA buttons in hero — cards are the CTA

### App Grid

**Desktop layout:**
```
[AbhiScan Pro — 50%] [Lunavi — 50%]       ← featured row
[AbhiScan Lite — 33%] [AbhiNidra — 33%] [AI QR — 33%]  ← standard row
```

CSS:
```css
.app-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-areas:
    "f1 f1 f1 f2 f2 f2"
    "s1 s1 s2 s2 s3 s3";
}
/* AbhiScan Pro */ .app-card--featured-1 { grid-area: f1; }
/* Lunavi       */ .app-card--featured-2 { grid-area: f2; }
/* AbhiScan Lite*/ .app-card--standard-1 { grid-area: s1; }
/* AbhiNidra   */ .app-card--standard-2 { grid-area: s2; }
/* AI QR       */ .app-card--standard-3 { grid-area: s3; }
```

**Featured card extras** vs standard:
- `FEATURED` badge — pill, top-right, `var(--featured-badge-bg)`, accent text
- Phone mockup 20% larger (`336px × 696px`)
- 3 feature bullets (standard: 2)
- Second screenshot peeking behind phone (positioned `+20px right, +20px top`, 80% opacity, 90% scale)
- More padding: `2.5rem` vs `1.75rem`

**Card default state:**
- Background: `var(--card-bg)` `#0e0e10`
- Border: `1px solid var(--card-border)`
- Border-radius: `var(--radius-xl)` `24px`
- No gap between cards at grid level — borders create the separation

**Card hover state (400ms ease):**
1. `background`: → `var(--card-hover-bg)` (accent at 12%)
2. `border-color`: → `var(--card-hover-border)` (accent at 40%)
3. Phone: `rotateY(-15deg)` → `rotateY(0deg)`, scale `1.0` → `1.05`
4. Phone glow: `box-shadow: 0 40px 120px color-mix(in srgb, var(--accent) 30%, transparent)`
5. Screenshot: cross-fades to screenshot 2 (CSS `opacity` transition on `::after` pseudo holding second screenshot)
6. `Explore →` arrow: `translateX(0)` → `translateX(4px)`
7. `--accent` is set via inline style on each card, so the hover color is app-specific

**Card content layout (top to bottom):**
```
[App initial letter — large, accent-colored, 48px, top-left]
[App name — 20px semibold white]
[Tagline — 14px muted]
[Feature bullets — 2-3 × accent-icon + text]
[Phone mockup — centered, 3D tilted]
[Explore → — bottom, small, accent color]
```

**Mobile:** 1 column. Featured cards same width as standard. Badge retained.

### Footer
Single line, centered, `var(--text-3)`:
`© 2026 Abhi Labs · Bangalore, India · contact@abhilabs.app`

## App Detail Pages (`apps/*/index.html`)

### `<html>` class
Keep existing per-app classes: `.app-abhiscan`, `.app-lunavi`, `.app-abhinidra`, `.app-ai-qr`

Add `.has-noise` and world particle class (`.world-scanline` etc.) to `<body>`.

### Head additions (app pages only)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
```

### Hero Section

Two-column grid, `min-height: 100vh`:

**Left column (text):**
```
[App name — display, clamp(48px, 7vw, 96px), white]
[Tagline — 20px, var(--text-2)]
[3 feature bullets — accent SVG dot + 16px text]
[Play Store button — large, accent bg, white, 52px height]
[Privacy Policy — 12px muted link below button]
```

**Right column (phone hero):**
- `.phone-mockup` large size `280px × 580px`
- CSS 3D: `transform: perspective(1000px) rotateY(-15deg) rotateX(5deg)`
- Glow: `filter: drop-shadow(0 60px 120px color-mix(in srgb, var(--accent) 40%, transparent))`
- Float: `animation: float 3s ease-in-out infinite`
- Shows screenshot 1 on load

```css
@keyframes float {
  0%, 100% { transform: perspective(1000px) rotateY(-15deg) rotateX(5deg) translateY(0); }
  50% { transform: perspective(1000px) rotateY(-15deg) rotateX(5deg) translateY(-12px); }
}
```

**Body background (app pages):**
```css
body {
  background-color: var(--bg);  /* #09090b */
  background-image: var(--world-gradient);
  background-attachment: fixed;
}
```

### Scroll-Driven Feature Section (GSAP)

Structure:
```html
<section class="feature-scroll">
  <div class="feature-scroll__phone-col">
    <div class="phone-mockup phone-mockup--sticky">
      <img class="phone-screen" src="assets/1.png" alt="">
    </div>
  </div>
  <div class="feature-scroll__content-col">
    <div class="feature-item" data-screenshot="assets/1.png">...</div>
    <div class="feature-item" data-screenshot="assets/2.png">...</div>
    <div class="feature-item" data-screenshot="assets/3.png">...</div>
    ...
  </div>
</section>
```

Phone column: `position: sticky; top: 15vh; height: 80vh` — stays visible.

GSAP ScrollTrigger per feature item:
```js
document.querySelectorAll('.feature-item').forEach(item => {
  ScrollTrigger.create({
    trigger: item,
    start: 'top center',
    end: 'bottom center',
    onEnter: () => swapScreenshot(item.dataset.screenshot),
    onEnterBack: () => swapScreenshot(item.dataset.screenshot),
  });
});

function swapScreenshot(src) {
  const screen = document.querySelector('.phone-screen');
  gsap.to(screen, { opacity: 0, duration: 0.2, onComplete: () => {
    screen.src = src;
    gsap.to(screen, { opacity: 1, duration: 0.3 });
  }});
}
```

Feature item entrance animation (GSAP ScrollTrigger):
```js
gsap.from('.feature-item', {
  x: -40, opacity: 0, duration: 0.6, ease: 'power2.out',
  scrollTrigger: { trigger: '.feature-item', start: 'top 80%' }
});
```

**`prefers-reduced-motion` fallback:**
```js
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // skip all GSAP animations, show all screenshots statically
}
```

**Mobile fallback (< 768px):**
Sticky layout disabled. Phone shows once at top of section as static image (screenshot 1). Features stack as standard cards below. No GSAP on mobile.

### Feature Item Layout
```
[Accent-colored number — 01, 02... — large, decorative, 64px, low opacity]
[Feature name — 24px semibold white]
[Feature description — 16px, var(--text-2), max 3 lines]
[Optional: mono code-style tag — e.g. "ON_DEVICE_OCR"]
```

Min-height per feature item: `60vh` — ensures clean scroll triggering, one feature at a time.

### Social Proof Strip
Full-width, `var(--surface)` background, `border-top` and `border-bottom` `var(--border)`:
```
[★ 4.6]              [10K+ Downloads]         [Offline-First]
Google Play Rating   Since launch             No cloud. Ever.
```
Numbers: `clamp(32px, 4vw, 48px)`, `var(--accent)`.
Labels: `11px`, uppercase, letter-spacing, `var(--text-3)`.

### Download CTA Section
Background: `color-mix(in srgb, var(--accent) 8%, var(--bg))`.
Border-top: `1px solid color-mix(in srgb, var(--accent) 20%, transparent)`.

Center:
```
[Heading — 40px — "Ready to scan smarter?" etc, per app]
[Play Store badge — official Google badge SVG, 200px wide]
[Subtext — "Free · No subscription · No account required"]
```

## About Page (`about/index.html`)

No per-app world — Abhi Labs brand world. Single teal orb, `--brand` color.

**Hero:**
```
We build software
people love to use.
```
`clamp(40px, 6vw, 80px)`. No animation — stillness is the statement.
Subtext: 2 sentences about the studio.

**Values section — 3 columns desktop:**
```
[01 Offline-First]   [02 Privacy-First]   [03 Quality-Obsessed]
```
Each: large decorative number `var(--accent)` at 15% opacity, value name `20px semibold`, 2-sentence description `var(--text-2)`.

**Stats strip** (same style as app social proof):
```
[5]              [10+]            [0]
Apps Published   Years Android    Subscriptions
```

**Contact block:**
```
Got a question?
contact@abhilabs.app   [→]
```
Email: `clamp(24px, 3vw, 40px)`, accent-colored, `mailto:` link. Underline slides in on hover from left (CSS `text-decoration` + `transition`).

## Global Constraints

- Lighthouse: maintain 95+ on all 4 categories (Performance, Accessibility, Best Practices, SEO)
- Dark mode only via `@media (prefers-color-scheme: dark)` — no JS toggle
- GSAP loaded only on app pages (not homepage, not about, not privacy)
- `prefers-reduced-motion`: disable all GSAP transitions, disable CSS float/scanline/pulse animations
- All images: `loading="lazy"` except first screenshot in hero (`fetchpriority="high"`)
- Play Store links: keep existing package IDs unchanged
- Privacy policy links: keep existing `/privacy/[app]/` paths
- Copyright: `© 2026 Abhi Labs. Bangalore, India.`
- Contact email: `contact@abhilabs.app` everywhere
- Font: Plus Jakarta Sans (existing async preload pattern — keep unchanged)
- `styles/output.css` gitignored — always run `npm run build` before committing HTML
- Branch: `debug`
- No new npm dependencies except GSAP via CDN

## Screenshot Mapping Per App

| App | Hero (screenshot 1) | Feature scroll sequence |
|-----|---------------------|------------------------|
| AbhiScan Pro | `assets/1.png` | 1→2→3→4→5→6 |
| AbhiScan Lite | `assets/screen-1.png` | screen-1→2→3→4→5→6→7 |
| Lunavi | `assets/1.png` | 1→2→3→4→5→6→7→8 |
| AbhiNidra | `assets/1.png` | 1→2→3→4→5→6→7→8 |
| AI QR Barcode | `assets/2.png` (no 1.png) | 2→3→4→5→6→7→8 |

## Featured App Copy

### AbhiScan Pro (featured)
- Hero tagline: `Professional document scanning. Entirely on your phone.`
- Feature bullets (hero): OpenCV Edge Detection · Full-Text OCR Search · 7 Scan Modes
- Download CTA heading: `Ready to scan smarter?`

### Lunavi (featured)
- Hero tagline: `Your cycle, your data. No cloud. No compromise.`
- Feature bullets (hero): AI Ovulation Predictions · Offline-First · Zero Ads
- Download CTA heading: `Ready to understand your cycle?`
