# About Page Redesign

## Goal

Rebuild `about/index.html` from a sparse 4-section placeholder into a full-quality page that earns trust, tells the studio story, and drives equal traffic to the portfolio and contact page. Match the visual quality of the privacy pages built in the previous session.

## Context

- Site: abhilabs.app — GitHub Pages, Tailwind CSS v3 CLI, static HTML
- Branch: `debug`
- Build command: `npm run build` (compiles `styles/input.css` → `styles/output.css`)
- CSS pattern: `@layer components` blocks in `styles/input.css`
- Existing patterns to reuse: `.reading-progress`, `.privacy-hero__orb`, `privacy-section__num`, `.social-proof-strip`, `.site-header`, `.site-footer`, `.mobile-nav`

## Studio facts (copy source of truth)

- **Team size:** 5 engineers
- **Background:** alumni of India's top IITs and NITs
- **Location:** Bangalore, India
- **Founded:** from frustration with bloated, privacy-invasive Android apps
- **Mission tagline:** "tomorrow's tech, today"
- **Descriptor:** "5 engineers from India's top IITs and NITs. One mission: apps that respect you."
- **Apps:** 5 published on Google Play
- **Subscriptions:** 0 across all apps
- **Cloud servers for user data:** 0
- **Android experience:** 10+ years

## Architecture

Two files change:
1. `about/index.html` — full rebuild
2. `styles/input.css` — new CSS block `/* === ABOUT PAGE === */`

No new files. No JS libraries.

## Page sections (in order)

### 0. Chrome (unchanged pattern)
- `<div class="reading-progress" id="reading-progress">` immediately before `<header>`
- Standard nav: logo img + nav-links + theme-toggle + hamburger
- Standard footer + mobile-nav
- Reading progress JS (same inline script as privacy pages)
- Theme toggle JS + hamburger JS (same inline scripts)

---

### 1. Hero (`<section class="about-hero">`)

**Label chip:**
```html
<p class="about-hero__chip">
  <svg><!-- map-pin icon --></svg>
  Bangalore, India · 5-person team
</p>
```

**H1:**
```
5 engineers from India's top IITs and NITs.
One mission: apps that respect you.
```

**Sub:**
```
Abhi Labs builds offline-first, privacy-first Android apps —
bringing tomorrow's tech to users today, without the bloat,
subscriptions, or data collection.
```

**Orb:** `<div class="about-hero__orb" aria-hidden="true"></div>` — same radial gradient glow as `privacy-hero__orb`, positioned behind hero content.

**CSS:**
```css
.about-hero {
  position: relative;
  max-width: 720px;
  margin: 0 auto;
  padding: 5rem 1.5rem 3rem;
  text-align: center;
  overflow: hidden;
}
.about-hero__orb {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 400px;
  background: radial-gradient(ellipse at center, color-mix(in srgb, var(--accent) 14%, transparent) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}
.about-hero > * { position: relative; z-index: 1; }
.about-hero__chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--accent);
  margin-bottom: 1.5rem;
}
.about-hero__title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -.025em;
  color: var(--text-1);
  margin-bottom: 1.25rem;
}
.about-hero__sub {
  font-size: 1.0625rem;
  line-height: 1.7;
  color: var(--text-2);
  max-width: 560px;
  margin: 0 auto;
}
```

---

### 2. Origin section (`<section class="about-origin" id="origin">`)

**Faded watermark number:** `<span class="about-section__num" aria-hidden="true">01</span>`

**Section head:**
```html
<div class="about-section__head">
  <span class="about-section__icon"><!-- spark / lightbulb SVG --></span>
  <h2 class="about-section__title">Why we started</h2>
</div>
```

**Body copy:**
```
We kept downloading apps that uploaded documents to cloud servers we'd
never agreed to. Cycle trackers sharing health data with advertisers.
Sleep apps that needed internet to play a rain sound.

As engineers, we knew this wasn't technically necessary — it was a choice.
We made a different one.
```

**Pull-quote callout** (reuse `.privacy-callout` class, already in CSS):
```html
<div class="privacy-callout" role="note">
  <svg><!-- shield-check icon --></svg>
  <p>Privacy isn't a premium feature. Working offline shouldn't require a subscription.</p>
</div>
```

**CSS for section wrapper (shared by all 3 numbered sections):**
```css
.about-section {
  position: relative;
  max-width: 760px;
  margin: 0 auto 3rem;
  padding: 2.5rem 2rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.about-section__num {
  position: absolute;
  top: -0.5rem;
  right: 1rem;
  font-size: 88px;
  font-weight: 900;
  color: var(--text-1);
  opacity: .04;
  line-height: 1;
  user-select: none;
  pointer-events: none;
}
.about-section__head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.about-section__icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.about-section__title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-1);
}
.about-section p {
  font-size: 0.9375rem;
  line-height: 1.75;
  color: var(--text-2);
  margin-bottom: 1rem;
}
.about-section p:last-child { margin-bottom: 0; }
```

---

### 3. Team section (`<section class="about-section about-team" id="team">`)

**Faded watermark:** `02`

**Section head:** icon (people/group) + `<h2>Who we are</h2>`

**Identity block:**
```html
<div class="about-team__identity">
  <div class="about-team__stat">
    <span class="about-team__num">5</span>
    <span class="about-team__label">engineers</span>
  </div>
  <div class="about-team__divider" aria-hidden="true"></div>
  <div>
    <p class="about-team__origin">IIT &amp; NIT alumni</p>
    <p class="about-team__loc">
      <svg><!-- map-pin --></svg>
      Bangalore, India
    </p>
  </div>
</div>
```

**Role tags (flex-wrap):**
```html
<div class="about-team__tags" aria-label="Team skills">
  <span class="about-team__tag">Android Dev</span>
  <span class="about-team__tag">AI / ML</span>
  <span class="about-team__tag">UI Design</span>
  <span class="about-team__tag">Product</span>
  <span class="about-team__tag">Backend</span>
</div>
```

**CSS:**
```css
.about-team__identity {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem 1.5rem;
  background: color-mix(in srgb, var(--accent) 6%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  border-radius: var(--radius-md);
}
.about-team__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}
.about-team__num {
  font-size: 3rem;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}
.about-team__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--text-3);
}
.about-team__divider {
  width: 1px;
  height: 48px;
  background: var(--border);
  flex-shrink: 0;
}
.about-team__origin {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-1);
  margin-bottom: 0.25rem;
}
.about-team__loc {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.875rem;
  color: var(--text-3);
}
.about-team__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.about-team__tag {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--surface-3);
  color: var(--text-2);
  border: 1px solid var(--border);
}
@media (max-width: 600px) {
  .about-team__identity { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .about-team__divider { width: 40px; height: 1px; }
}
```

---

### 4. Principles section (`<section class="about-section" id="principles">`)

**Faded watermark:** `03`

**Section head:** icon (settings/sliders) + `<h2>How we build</h2>`

**Intro line:** "Three principles we've held since day one — proven by the apps we ship."

**3-column principle grid:**
```html
<div class="about-principle-grid">
  <div class="about-principle">
    <div class="about-principle__icon"><!-- wifi-off SVG --></div>
    <h3 class="about-principle__name">Offline-First</h3>
    <p class="about-principle__desc">Every app works completely without internet. No cloud dependency, no outages, no waiting.</p>
    <a href="/apps/abhi-scan/" class="about-principle__proof">See it in AbhiScan →</a>
  </div>
  <div class="about-principle">
    <div class="about-principle__icon"><!-- shield SVG --></div>
    <h3 class="about-principle__name">Privacy-First</h3>
    <p class="about-principle__desc">Your data never leaves your device unless you share it. We don't operate user data servers.</p>
    <a href="/apps/lunavi/" class="about-principle__proof">See it in Lunavi →</a>
  </div>
  <div class="about-principle">
    <div class="about-principle__icon"><!-- award/star SVG --></div>
    <h3 class="about-principle__name">Quality-Obsessed</h3>
    <p class="about-principle__desc">No subscriptions. No dark patterns. No feature bloat. Ships when it's genuinely good.</p>
    <a href="/" class="about-principle__proof">5 apps, 0 subscriptions →</a>
  </div>
</div>
```

**CSS:**
```css
.about-principle-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}
.about-principle {
  padding: 1.25rem;
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.about-principle__icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
}
.about-principle__name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-1);
}
.about-principle__desc {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--text-2);
  flex: 1;
}
.about-principle__proof {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--accent);
  text-decoration: none;
  margin-top: 0.5rem;
}
.about-principle__proof:hover { text-decoration: underline; }
@media (max-width: 700px) {
  .about-principle-grid { grid-template-columns: 1fr; }
}
```

---

### 5. Stats strip (existing `.social-proof-strip`)

Update from 3 to 4 stats:

```html
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
    <div class="social-stat">
      <span class="social-stat__value">0</span>
      <span class="social-stat__label">Cloud Servers</span>
      <span class="social-stat__sub">for user data</span>
    </div>
  </div>
</div>
```

No CSS change needed — `.social-proof-inner` already uses `flex + gap + wrap`.

---

### 6. Dual CTA section (`<section class="about-cta-section">`)

```html
<section class="about-cta-section" aria-label="Next steps">
  <div class="about-cta-grid">
    <a href="/" class="about-cta-card">
      <div class="about-cta-card__icon"><!-- grid/apps SVG --></div>
      <p class="about-cta-card__title">See our apps</p>
      <p class="about-cta-card__sub">5 apps built on these principles, on Google Play now.</p>
      <span class="about-cta-card__arrow">
        View portfolio
        <svg><!-- arrow right --></svg>
      </span>
    </a>
    <a href="/contact/" class="about-cta-card">
      <div class="about-cta-card__icon"><!-- mail SVG --></div>
      <p class="about-cta-card__title">Get in touch</p>
      <p class="about-cta-card__sub">Partnership, feedback, or just want to say hi.</p>
      <span class="about-cta-card__arrow">
        Contact us
        <svg><!-- arrow right --></svg>
      </span>
    </a>
  </div>
  <p class="about-cta-email">
    Or email directly:
    <a href="mailto:contact@abhilabs.app">contact@abhilabs.app</a>
  </p>
</section>
```

**CSS:**
```css
.about-cta-section {
  max-width: 760px;
  margin: 0 auto 4rem;
  padding: 0 1.5rem;
  text-align: center;
}
.about-cta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.about-cta-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 1.5rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  text-decoration: none;
  transition: border-color .2s, transform .2s;
}
.about-cta-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}
.about-cta-card__icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
}
.about-cta-card__title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-1);
}
.about-cta-card__sub {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--text-2);
  flex: 1;
}
.about-cta-card__arrow {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--accent);
  margin-top: 0.5rem;
}
.about-cta-email {
  font-size: 0.875rem;
  color: var(--text-3);
}
.about-cta-email a { color: var(--accent); font-weight: 600; }
@media (max-width: 600px) {
  .about-cta-grid { grid-template-columns: 1fr; }
}
```

---

## Implementation files

| File | Change |
|---|---|
| `about/index.html` | Full rebuild — all 6 sections |
| `styles/input.css` | Add `/* === ABOUT PAGE === */` block with all new classes above |

## Global constraints

- Root-absolute asset paths (`/assets/...`, `/apps/...`) — never relative
- No `has-noise` body class (about page doesn't use it currently; don't add)
- Accent: `var(--accent)` (no `html` class like `app-*` — about page uses default teal from `:root`)
- Inline scripts only — no external JS
- Same 3 script blocks as privacy pages: hamburger, theme toggle, reading progress
- `npm run build` must be run after CSS changes
- No new fonts, no new external dependencies
