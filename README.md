# Patient Aid — Marketing Website

A fast, responsive, static marketing website for the **Patient Aid** Android application by
**ITmedicus Solutions**. It introduces the product, explains its features and Premium offering,
shows the interface, and sends visitors to the Google Play listing.

Built with plain HTML5, CSS3, and vanilla JavaScript. There is no backend, no build step, and no
runtime dependency other than optional web fonts.

---

## 1. Quick start

Open `index.html` directly in a browser, or serve the folder locally:

```powershell
# Python (already available in most environments)
python -m http.server 8000
# then open http://localhost:8000/
```

No compilation, installation, or configuration is required.

### Deploying

The project root **is** the production build — there is no bundling or compilation step.

Upload the whole folder (except `tools/`, which is development only) to any static host:

- **Netlify / Vercel / Cloudflare Pages** — drag the folder in, or connect the repository. No build command; publish directory is the project root.
- **GitHub Pages** — push to a repository and enable Pages for the branch root.
- **cPanel / shared hosting** — upload the files into `public_html`.

After the production domain is known, see §5 for the placeholder values to replace.

---

## 2. Project structure

```
patient-aid-website/
├── index.html               Home / product landing page
├── about.html               About Patient Aid
├── features.html            All 13 features + Premium teaser
├── premium.html             Premium overview
├── faq.html                 Full FAQ (10 questions + FAQPage schema)
├── contact.html             ITmedicus Solutions contact details
├── privacy.html             Privacy policy placeholder (replace before launch)
├── robots.txt
├── sitemap.xml
├── favicon.svg              Vector favicon
├── favicon-32.png
├── assets/
│   ├── css/style.css        Design system + all page styles
│   ├── js/main.js           Navigation, accordion, lightbox, reveal, tabs
│   └── img/
│       ├── og-image.png     1200×630 social preview
│       ├── apple-touch-icon.png
│       ├── patient-aid-logo.svg
│       └── screens/         12 genuine app screenshots (WebP)
└── tools/                   Development-only helpers (not deployed)
    ├── make_assets.py       Regenerates logo, favicon, and social preview
    ├── process_uploads.py   Crops/converts supplied screenshots to WebP
    ├── shot.mjs             Screenshot helper (headless Chrome + CDP)
    ├── qa.mjs               Automated QA suite
    └── preview/             QA screenshots and results (generated)
```

Every page shares the same header, footer, and design tokens. Navigation between pages is by relative
links, so the site works from any folder or subdirectory.

---

## 3. Screenshots and brand assets

> **Note:** the app screens are now genuine screenshots supplied by ITmedicus Solutions. The logo,
> favicon, and social preview are still generated brand placeholders — replace them with official
> files if available.

### 3.1 App screenshots

Twelve screenshots live in `assets/img/screens/` as WebP:

| File | Screen | Gallery caption |
| --- | --- | --- |
| `home.webp` | App home (Bangla) | Medicine, health tips, alarms & calculators |
| `medicine-search.webp` | Medicine search results | Search by brand or generic name |
| `medicine-details.webp` | Medicine details | Uses, side effects, packs & price |
| `directory-home.webp` | Healthcare directory | Doctors, hospitals, ambulance & blood bank |
| `symptoms-checker.webp` | Symptoms checker | Find the right doctor by symptom |
| `doctors.webp` | Doctor list | Find doctors by area & speciality |
| `doctor-details.webp` | Doctor details | Chambers, appointments & sharing |
| `calculators.webp` | Calculators & charts | IBW, BMI, EDD & weight charts |
| `bmi.webp` | BMI calculator | Check whether your weight is normal |
| `my-medicine.webp` | My Medicine | Your family's medicine lists |
| `medicine-reminder.webp` | Medicine alarm | Medicine alarms keep you on schedule |
| `medicine-cost.webp` | Cost calculator | Estimate your medicine costs |

The eight poster-style originals (captioned cards on coloured backgrounds) and four raw device
screenshots are kept in `tools/_uploads/` for reference. `tools/process_uploads.py` crops the app
screen out of each poster and converts everything to WebP:

```powershell
python tools/process_uploads.py
```

To change a screenshot later, drop the replacement in `assets/img/screens/` with the same file name
(or update the `src`), keep the `width`/`height` attributes accurate, and update the gallery caption
and alt text. Screens also appear in the hero, the offline and My Medicine sections (`index.html`),
`about.html`, `features.html`, and `premium.html` — search for `assets/img/screens/` in those files.

### 3.2 Logo and icons

- `assets/img/patient-aid-logo.svg` — wordmark used in the developer panel. Replace with the official
  Patient Aid logo (SVG or transparent PNG).
- Header/footer brand mark is inline SVG (a simple cross). Replace the `<span class="brand-mark">`
  contents if you have an official app icon.
- `favicon.svg`, `favicon-32.png`, `assets/img/apple-touch-icon.png` — rebuild from the official icon.
- `assets/img/og-image.png` (1200 × 630) — social sharing image; replace with a brand-approved version.
- Feature icons are hand-authored inline SVG paths (no third-party icon licence required). They can be
  swapped for Lucide or Bootstrap Icons if you prefer.

### 3.3 Regenerating brand placeholders

`tools/make_assets.py` rebuilds the logo, favicon, touch icon, and social preview:

```powershell
python tools/make_assets.py
```

It requires Pillow. It no longer generates app screenshots — the site uses the genuine screens in
`assets/img/screens/`, produced by `tools/process_uploads.py`. Editing the SVGs directly is also fine.

---

## 4. Content and design system

### Pages

| Page | Purpose |
| --- | --- |
| `index.html` | Full landing page: hero, trust strip, download/review stats, about, features, offline, language, medicine information, My Medicine, Premium, screenshot gallery, why Patient Aid, developer, FAQ, download CTA |
| `about.html` | Product background, purpose, audience, goals, everyday use |
| `features.html` | All 13 features with full descriptions, offline/language callout, interface preview |
| `premium.html` | Premium benefits, how it works, good-to-know terms |
| `faq.html` | 10 questions with accessible accordion + `FAQPage` structured data |
| `contact.html` | Address, email, phone, website, app support, privacy contact |
| `privacy.html` | Placeholder policy — **replace with the official policy** |

### Design tokens (`assets/css/style.css`)

| Token | Value | Usage |
| --- | --- | --- |
| `--primary` | `#1686D9` | Buttons, links, highlights |
| `--secondary` | `#00A8B5` | Accents, supporting highlights |
| `--ink` | `#18324B` | Headings and primary text |
| `--muted` | `#6B7C8F` | Secondary text |
| `--body` | `#FFFFFF` | Page background |
| `--alt` | `#F4F9FC` | Alternating sections |

Typography: **Inter** (Google Fonts) with a system-font fallback; **Noto Sans Bengali** is loaded on
the home page for the Bangla language sample. To host fonts locally, download the WOFF2 files, add
them under `assets/fonts/`, and replace the Google Fonts `<link>` with `@font-face` rules.

### Interactions (`assets/js/main.js`)

- Sticky header state on scroll + back-to-top button
- Mobile hamburger menu (Escape to close, closes on link click, not on desktop resize)
- FAQ accordion (`aria-expanded`, `aria-hidden`, `inert`, one open item per list)
- Screenshot lightbox (click, arrow keys, Escape, focus trap, backdrop click)
- Bangla/English sample switcher (ARIA tabs, arrow-key support)
- Scroll progress bar along the top of the page
- Download, review and rating counters that count up when the stats band enters view
- Hero pointer parallax (desktop, fine pointers only)
- Scroll-reveal animations, disabled under `prefers-reduced-motion`
- Without JavaScript, all content remains visible and FAQ answers stay collapsed

### Motion

All animation lives in one clearly marked **“Motion layer”** block at the end of
`assets/css/style.css`, plus the scroll-progress/parallax code at the end of `main.js`. It is
transform/opacity only, so it stays on the compositor and does not cause layout shifts.

- **Hero choreography** — logo pill, headline, sub-headline, body, buttons, and meta row rise in
  sequence; the phone mockup scales up; the floating cards pop in; the plus in the brand mark draws
  itself.
- **Scroll progress** — a 3 px gradient line at the top of the viewport follows page progress.
- **Reveals** — sections fade up as they enter the viewport, cards stagger in groups, and split-section
  media slides in from the side.
- **Parallax** — the hero visual follows the pointer by a few pixels on desktop (pointer-fine devices
  only, never on touch).
- **Stat counters** — the download, review, and rating numbers count up once when the stats band
  scrolls into view (static final values when reduced motion is on).
- **Micro-interactions** — button sheen sweep, feature-icon lift, card hovers, gallery caption colour,
  lightbox/panel entrance, FAQ answer fade.

To remove or tone down motion: delete the “Motion layer” block, or keep it and adjust durations and
delays there. Every entrance uses `both` fill, so the final state is identical to no animation.

**Accessibility:** `prefers-reduced-motion: reduce` disables every entrance, drift, parallax, and
transition (delays are zeroed), so content appears immediately and statically. The scroll progress bar
is decorative (`aria-hidden`).

---

## 5. Before launch — replace these placeholders

| Item | Where | What to do |
| --- | --- | --- |
| Domain | `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, `sitemap.xml`, `robots.txt` | Replace `patientaid.example.com` with the production domain |
| Screenshots | `assets/img/screens/*.webp`, image `src`/`alt`, gallery `data-full` | Genuine screenshots are in place; refresh them if the app UI changes |
| Logo & icons | `assets/img/patient-aid-logo.svg`, favicon, touch icon, OG image | Use official brand assets |
| Privacy policy | `privacy.html` | Replace the placeholder text with the official policy, or point the links to the policy on itmedicus.com |
| Statistics | Home page stats band (`index.html`, `#stats`) | The figures **3M+ downloads**, **150K+ reviews** and a **4.5 / 5 rating** were supplied for this build. Confirm they are current and approved, then update `data-count-to` / `data-count-suffix` / `data-count-decimals`, the star row, **and** the visible fallback text together |
| Contact details | Footer, `contact.html`, structured data | Confirm address, email, and phone with ITmedicus |
| Premium terms | `premium.html`, home Premium section | Confirm current features, pricing, and subscription conditions |
| Demo notice | `privacy.html` callouts, `README`, `TEST_REPORT.md` | Remove placeholder notices once real content is in place |

The site displays no star rating and makes no "doctor approved" style claims. The only figures shown are
the client-supplied download and review counts in the stats band; confirm them against the live Google
Play listing before launch, and add any further figures only with product-owner approval.

---

## 6. Quality checks

The site was verified with an automated suite (403 checks across 7 pages × 3 viewports) covering
horizontal overflow, image loading and alt text, heading structure, duplicate IDs, in-page anchors,
Play Store links, meta/OG tags, mobile menu, FAQ accordion, language switcher, and lightbox. See
`TEST_REPORT.md` for the results.

Re-run the checks after changes:

```powershell
node tools/qa.mjs
```

Take a screenshot of any page:

```powershell
node tools/shot.mjs --url file:///D:/patient-aid-website/index.html --out tools/preview/home.png --width 1440 --height 1000
node tools/shot.mjs --url file:///D:/patient-aid-website/index.html --out tools/preview/home-mobile.png --width 390 --height 844 --mobile --full
```

`tools/` is development-only and is disallowed in `robots.txt`; it does not need to be uploaded.

---

## 7. Browser support

Tested in current Chromium (Chrome/Edge). The layout uses modern but widely supported CSS: grid,
flexbox, `clamp()`, `aspect-ratio`, `:focus-visible`, CSS masks, `backdrop-filter`, and
`prefers-reduced-motion`. Internet Explorer is not supported.

---

## 8. Medical disclaimer

The disclaimer is present in the footer of every page and on `faq.html`:

> Patient Aid provides healthcare and medicine information for general educational and informational
> purposes only. The information available in the application is not a substitute for professional
> medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional regarding
> medical conditions, medications, or treatment decisions.
#   p a t i e n t - a i d - w e b s i t e  
 #   p a t i e n t - a i d - w e b s i t e  
 #   p a t i e n t - a i d - w e b s i t e  
 