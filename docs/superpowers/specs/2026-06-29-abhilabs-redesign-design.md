# Abhi Labs Website Redesign — Design Spec
**Date:** 2026-06-29  
**Status:** Approved  
**Scope:** Full structural rebuild of abhilabs.app (7 HTML pages + new privacy pages + 404)

---

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Primary conversion | App detail page → Play Store | Trust gap: direct-to-store from homepage wastes credibility-building opportunity |
| Color mode | System-adaptive (dark + light) | Respects user intent, no extra maintenance cost, screenshots pop on dark |
| Build system | Tailwind CLI (purged output) | CDN blocks render, ~3MB, Lighthouse 95+ impossible without it |
| Scope | Improve existing + Play Store social proof | Star ratings + download counts = highest-ROI trust addition for app portfolio |
| Theming | Shared design system + per-app `--accent` CSS variable | One component library, each app page swaps one variable |
| Approach | Structural rebuild (Approach B) | Same URLs/content, but DOM rebuilt mobile-first, semantic, accessible |

---

## Pages In Scope

| URL | File | Status |
|---|---|---|
| `/` | `index.html` | Rebuild |
| `/about/` | `about/index.html` | Rebuild |
| `/apps/abhi-scan/` | `apps/abhi-scan/index.html` | Rebuild |
| `/apps/abhi-scan-lite/` | `apps/abhi-scan-lite/index.html` | Rebuild |
| `/apps/lunavi/` | `apps/lunavi/index.html` | Rebuild |
| `/apps/abhinidra/` | `apps/abhinidra/index.html` | Rebuild |
| `/apps/ai-qr-barcode/` | `apps/ai-qr-barcode/index.html` | Rebuild |
| `/privacy/abhiscan/` | `privacy/abhiscan/index.html` | **New** |
| `/privacy/abhiscan-lite/` | `privacy/abhiscan-lite/index.html` | **New** |
| `/privacy/lunavi/` | `privacy/lunavi/index.html` | **New** |
| `/privacy/abhinidra/` | `privacy/abhinidra/index.html` | **New** |
| `/privacy/ai-qr-barcode/` | `privacy/ai-qr-barcode/index.html` | **New** |
| `/404.html` | `404.html` | **New** |

---

## Build System

**Tailwind CLI — no Node.js framework, no bundler.**

```
project/
├── styles/
│   ├── input.css        ← Tailwind directives + custom CSS variables
│   └── output.css       ← Built output (committed, served directly)
├── tailwind.config.js
├── package.json         ← scripts only: { "build:css": "tailwindcss -i ./styles/input.css -o ./styles/output.css --minify" }
└── [all HTML files]
```

- `<link rel="stylesheet" href="/styles/output.css">` replaces all CDN links
- Font Awesome: replace with inline SVG icons — eliminates external CSS + font file request entirely (~140KB saved)
- Google Fonts: keep `<link rel="preconnect">` + `display=swap` — already correct
- Build command: `npm run build:css` before every deploy
- GitHub Actions: add one step `npx tailwindcss -i ./styles/input.css -o ./styles/output.css --minify`

---

## Design System

### Color Tokens

Defined in `styles/input.css` as CSS custom properties. Auto-switches via `prefers-color-scheme`.

```css
:root {
  --bg:              #ffffff;
  --bg-subtle:       #f4f4f5;
  --surface:         #ffffff;
  --border:          #e4e4e7;
  --text-primary:    #09090b;
  --text-secondary:  #71717a;
  --text-tertiary:   #a1a1aa;
  --brand:           #0d9488;
  --brand-subtle:    #f0fdfa;
  --brand-dark:      #042f2e;

  /* Per-page accent — set inline on <html> element */
  --accent:          #0d9488;
  --accent-subtle:   #f0fdfa;
  --accent-dark:     #042f2e;

  /* Shadows */
  --shadow-sm:   0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md:   0 4px 16px rgba(0,0,0,0.08);
  --shadow-lg:   0 12px 40px rgba(0,0,0,0.10);
  --shadow-xl:   0 24px 80px rgba(0,0,0,0.12);

  /* Radius */
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   16px;
  --radius-xl:   24px;
  --radius-2xl:  32px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:              #09090b;
    --bg-subtle:       #111113;
    --surface:         #18181b;
    --border:          #27272a;
    --text-primary:    #fafafa;
    --text-secondary:  #a1a1aa;
    --text-tertiary:   #52525b;
    --brand:           #14b8a6;
    --brand-subtle:    #042f2e;
    --brand-dark:      #ccfbf1;

    --shadow-sm:   0 0 0 1px var(--border);
    --shadow-md:   0 0 0 1px var(--border), 0 4px 16px rgba(0,0,0,0.4);
    --shadow-lg:   0 0 0 1px var(--border), 0 8px 32px rgba(0,0,0,0.5);
    --shadow-xl:   0 0 0 1px var(--border), 0 16px 64px rgba(0,0,0,0.6);
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0ms !important;
    transition-duration: 0ms !important;
  }
}
```

### Per-App Accent Values

Set on `<html>` element of each app page:

| App | `--accent` | `--accent-subtle` | `--accent-dark` |
|---|---|---|---|
| AbhiScan Pro | `#0d9488` | `#f0fdfa` | `#042f2e` |
| AbhiScan Lite | `#0d9488` | `#f0fdfa` | `#042f2e` |
| Lunavi | `#e11d48` | `#fff1f2` | `#4c0519` |
| AbhiNidra | `#6366f1` | `#eef2ff` | `#1e1b4b` |
| AI QR Barcode | `#0d9488` | `#f0fdfa` | `#042f2e` |

### Typography

**Font:** Plus Jakarta Sans (keep existing Google Fonts import)

| Name | Size | Weight | Usage |
|---|---|---|---|
| display | 64–80px | 900 | Hero headlines |
| h1 | 48px | 800 | Page titles |
| h2 | 36px | 800 | Section headings |
| h3 | 24px | 700 | Card titles |
| h4 | 18px | 700 | Sub-sections |
| body-lg | 18px | 400 | Hero subhead |
| body | 16px | 400 | Body copy |
| body-sm | 14px | 400 | Secondary text |
| label | 11px | 700 | Badges, eyebrows |
| mono | 13px | 600 | Code badges |

Line-heights: `1.0` display · `1.2` headings · `1.6` body  
Letter-spacing: `-0.04em` display · `-0.02em` headings · `0.1em` labels

### Spacing Scale (4px base)
`4 8 12 16 20 24 32 40 48 64 80 96 128 160`

### Container
- Max width: `1280px`, `mx-auto`
- Padding: `px-5` (< 768px) · `px-8` (768–1024px) · `px-12` (> 1024px)

### Animation
- Micro interactions: `150ms ease-out`
- Hover transitions: `200ms ease-out`
- Scroll reveals: `600ms cubic-bezier(0.22, 1, 0.36, 1)`
- Orb animations: `20s / 25s linear infinite` (GPU-composited, `will-change: transform`)

### Buttons

**Primary:** `bg-[var(--accent)] text-white px-6 py-3 rounded-[var(--radius-lg)] font-semibold text-sm min-h-[44px]`  
**Secondary:** `border border-[var(--border)] text-[var(--text-primary)] px-6 py-3 rounded-[var(--radius-lg)] font-semibold text-sm min-h-[44px]`  
**Ghost:** `text-[var(--text-secondary)] hover:text-[var(--text-primary)] px-4 py-2 min-h-[44px]`

Focus: `outline: 2px solid var(--accent); outline-offset: 2px` (`:focus-visible` only)

---

## Navigation

**Structure:** Fixed, `height: 64px`, `bg-[var(--surface)]/80 backdrop-blur border-b border-[var(--border)]`

**Desktop links:** `Our Apps` · `About` · `Download` (primary button → AbhiScan Play Store)

**Mobile:** hamburger toggle, full-width slide-down panel, `min-height: 48px` per link

**Fixes:**
- Repair broken `<a>` tag on logo
- `<nav aria-label="Main navigation">`
- `aria-current="page"` on active link
- Skip-to-content: `<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>` as first child of `<body>`
- Hamburger: `aria-expanded`, `aria-label` toggled by JS, Escape closes, focus trapped
- Logo alt: `"Abhi Labs — Home"`

---

## Homepage (`index.html`)

### Hero

**Content:**
```
[badge: 5 Android Apps · Privacy-First · 100% Offline]

We build Android apps
people actually trust.

100% offline. No tracking. No cloud.
Engineered by a team with 15+ years in product.

[Explore Our Apps]    [4.8★ on Play Store]

[5 app icons — each links to app detail page]
```

**Mobile:** `pt-24 pb-16`, `h1` at `text-4xl`, CTAs stacked full-width, icon row horizontal scroll  
**Desktop:** `pt-40 pb-32`, `h1` at `text-6xl`, CTAs inline side-by-side, icon row inline

**Semantic:** `<header>` · `<h1>` · CTAs are `<a>` elements

### Portfolio Section

**Section heading:** "Our Apps" — `<h2>`, left-aligned

**Card structure per app:**

```html
<article> <!-- one per app -->
  <header>
    <img> <!-- app icon, 56px -->
    <div>
      <span><!-- eyebrow: "Featured" / "New" --></span>
      <h3><!-- App Name --></h3>
    </div>
    <div><!-- star rating + download count badges --></div>
  </header>
  <p><!-- one-sentence description --></p>
  <dl><!-- 2 tech specs --></dl>
  <div class="screenshot-gallery"><!-- horizontal scroll --></div>
  <footer>
    <a href="/apps/.../">Explore Details</a>
    <a href="https://play.google.com/...">Play Store</a>
  </footer>
</article>
```

**Social proof values — REQUIRES USER INPUT before implementation:**
- AbhiScan Pro: `[rating]★ · [count]+ downloads` — check Play Console
- AbhiScan Lite: `[rating]★ · [count]+ downloads` — check Play Console
- Lunavi: `[rating]★ · [count]+ downloads` — check Play Console
- AbhiNidra: `[rating]★ · New` (if < 100 ratings, show "New" instead)
- AI QR Barcode: `[rating]★ · New` (if < 100 ratings, show "New" instead)
- If an app has no public rating yet, show only `"100% Offline"` trust badge instead

**All cards:** `bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-2xl)]`  
**Accent color per card:** border-top `3px solid var(--accent)` using inline style or data attribute

**Screenshot gallery:** `overflow-x-auto scroll-snap-type-x`, images `lazy` loaded, `h-48` mobile / `h-64` desktop

**AbhiScan Lite:** Own card, smaller visual weight, `"Lite Version"` badge, positioned after AbhiScan Pro

**Bottom grid:** Pipeline card (dashed border) + Collab card (dark surface) — `md:grid-cols-2`

---

## App Detail Pages

**Shared structure (copy-paste identical nav + footer across all pages):**

```
<html style="--accent: [app color]; --accent-subtle: [...]; --accent-dark: [...]">

NAV (identical)

<main id="main">
  BREADCRUMB: Home → [App Name]
  
  HERO:
    [icon 80px] [App Name] [App Category]
    [social proof badges]
    [value prop — 1 sentence]
    [Play Store CTA] [Back to Apps]
  
  FEATURE IMAGE (lazy, full-bleed)
  
  SCREENSHOTS (lazy, h-[360px] mobile / h-[520px] desktop, snap-scroll)
  
  FEATURES GRID (1-col mobile / 2-col tablet / 3-col desktop)
  
  TECH SPECS (dl list, 2-col desktop / 1-col mobile)
  
  PRIVACY BLOCK:
    "All processing on-device. No internet permission required."
    [View Privacy Policy →]
  
  CROSS-SELL STRIP:
    "Also from Abhi Labs" + [icon + name] for other 3 apps
  
</main>

FOOTER (identical)
```

**Breadcrumb:** `<nav aria-label="Breadcrumb"><ol><li><a>Home</a></li><li>[App]</li></ol></nav>`

**Images:** all `loading="lazy"` except feature image above fold (eager)  
**Feature image:** `loading="eager" fetchpriority="high"`

---

## About Page

**Shorter hero:** eyebrow + `<h1>` + 1-line subhead. No animated orbs.

**Stats grid:** `2-up` mobile, `4-up` desktop. Values: `15+` `10+` `05` `MNC`

**Mission cards:** 3 values — Simplicity · Reliability · **Smart** (add missing third)

**Benchmarks card:** Keep structure. Fix dark mode (use `var(--surface)` tokens).

---

## Privacy Pages (new)

Simple semantic HTML, no hero, no screenshots.

```
NAV

<main>
  <h1>[App Name] Privacy Policy</h1>
  <p>Last updated: [date]</p>
  <section>...</section>  ← same content as current Google Sites page
</main>

FOOTER
```

Replace all `sites.google.com/view/*/home` links across all app pages with `/privacy/[app]/`.

---

## 404 Page (new)

```
NAV

<main>
  <h1>Page not found</h1>
  <p>This page doesn't exist or was moved.</p>
  <a href="/">← Back to Abhi Labs</a>
</main>

FOOTER
```

No animations, no hero, no orbs.

---

## Accessibility Requirements

- WCAG 2.1 AA minimum, target AAA where achievable
- All interactive elements: `min 44×44px` touch target
- Color contrast: `4.5:1` normal text, `3:1` large text / UI components
- No color as sole information carrier
- All images: meaningful `alt` text or `alt=""` if decorative
- All icon-only buttons: `aria-label`
- Keyboard: Tab order matches visual order, all interactive elements reachable
- Screen reader: landmarks (`<header>` `<nav>` `<main>` `<footer>`), headings in logical order
- Focus: `:focus-visible` outline on all interactive elements, never `outline: none` without replacement
- Motion: `prefers-reduced-motion` removes all animations

---

## Performance Targets

| Metric | Target |
|---|---|
| Lighthouse Performance | 95+ |
| Lighthouse Accessibility | 95+ |
| Lighthouse Best Practices | 95+ |
| Lighthouse SEO | 100 |
| LCP | < 2.5s |
| CLS | < 0.1 |
| INP | < 200ms |

**How we hit these:**
- Tailwind CLI output: ~8KB minified/gzipped (vs 3MB CDN)
- `loading="lazy"` on all below-fold images
- `fetchpriority="high"` on hero/feature images
- `<link rel="preconnect">` for Google Fonts (already in place)
- `font-display: swap` (already in place via Google Fonts URL)
- Remove hits.sh badge (external image, blocks LCP)
- Remove `animate-ping` from hero dot — replace with `width: 8px; height: 8px; border-radius: 50%; background: var(--brand)` static
- GPU-composite orb animations: `will-change: transform; transform: translateZ(0)`
- No external JS libraries

---

## SEO

- Each page: unique `<title>` + `<meta name="description">`
- `<link rel="canonical">` on every page
- Open Graph tags: `og:title` `og:description` `og:image` `og:url`
- App pages: `og:image` = hero post image (already exists)
- Structured data: `Organization` schema on homepage, `SoftwareApplication` schema on each app page
- `robots.txt` — verify exists (not currently in repo)
- `sitemap.xml` — create

---

## File Structure After Rebuild

```
/
├── styles/
│   ├── input.css          ← Tailwind + CSS vars
│   └── output.css         ← Built (committed)
├── assets/
│   └── developer_logo.png
├── apps/
│   ├── abhi-scan/
│   │   ├── index.html
│   │   └── assets/
│   ├── abhi-scan-lite/
│   │   ├── index.html
│   │   └── assets/
│   ├── abhinidra/
│   │   ├── index.html
│   │   └── assets/
│   ├── ai-qr-barcode/
│   │   ├── index.html
│   │   └── assets/
│   └── lunavi/
│       ├── index.html
│       └── assets/
├── privacy/
│   ├── abhiscan/index.html
│   ├── abhiscan-lite/index.html
│   ├── lunavi/index.html
│   ├── abhinidra/index.html
│   └── ai-qr-barcode/index.html
├── about/
│   └── index.html
├── 404.html
├── index.html
├── sitemap.xml            ← New
├── robots.txt             ← New/verify
├── tailwind.config.js     ← New
├── package.json           ← New (scripts only)
├── CNAME
├── app-ads.txt
└── LICENSE
```

---

## Implementation Order

1. Build system setup (Tailwind CLI, `styles/input.css`, config)
2. Design system CSS (`input.css` — tokens, base styles, components)
3. Shared nav + footer HTML snippet (reference template)
4. Homepage (`index.html`) — hero + portfolio cards
5. App detail pages (5 pages, shared structure, `--accent` swap)
6. About page
7. Privacy pages (5 pages)
8. 404 page
9. `sitemap.xml` + `robots.txt`
10. Structured data (JSON-LD)
11. Lighthouse audit + fixes
