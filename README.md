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
├── 404.html                 Not-found page (noindex, links back home)
├── robots.txt
├── sitemap.xml
├── favicon.ico              Multi-resolution icon (16/32/48)
├── favicon.svg              Vector favicon with the embedded app icon
├── favicon-16.png … -192.png  PNG icon set (16, 32, 48, 96, 192)
├── manifest.json         Web app manifest with 192/512 icons
├── assets/
│   ├── css/style.css        Design system + all page styles
│   ├── js/main.js           Navigation, accordion, lightbox, reveal, tabs
│   └── img/
│       ├── og-image.png     1200×630 social preview
│       ├── patient-aid-icon.png  Official app icon (source for all marks)
│       ├── apple-touch-icon.png
│       ├── patient-aid-logo.svg
│       └── screens/         12 genuine app screenshots (WebP)
└── tools/                   Development-only helpers (not deployed)
    ├── make_assets.py       Regenerates logo, favicon, and social preview
    ├── process_uploads.py   Crops/converts supplied screenshots to WebP
    ├── set_domain.py        Switches placeholder domain to production
    ├── shot.mjs             Screenshot helper (headless Chrome + CDP)
    ├── qa.mjs               Automated QA suite
    └── preview/             QA screenshots and results (generated)
```

Every page shares the same header, footer, and design tokens. Navigation between pages is by relative
links, so the site works from any folder or subdirectory.

---

## 3. Screenshots and brand assets

> **Note:** the app screens and the Patient Aid logo are the genuine assets supplied by ITmedicus
> Solutions. Every icon size (favicon, touch icon, social preview, wordmark) is generated from the
> supplied 96 × 96 icon — replace `assets/img/patient-aid-icon.png` if a higher-resolution or vector
> source becomes available, then re-run `tools/make_assets.py`.

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

The official Patient Aid app icon is in place (`assets/img/patient-aid-icon.png`, 96 × 96 transparent
PNG) and is used for:

- the header, footer, and hero brand marks (rendered from the PNG at 30–38 px);
- `assets/img/patient-aid-logo.svg` — the developer-panel wordmark, which embeds the icon;
- the browser icon set: `favicon.ico` (16/32/48), `favicon.svg`, `favicon-16/32/48/96/192.png`,
  `assets/img/apple-touch-icon.png`, and `manifest.json` (192/512);
- `assets/img/og-image.png` (1200 × 630) — social sharing image.

Favicons are generated on a full-bleed brand-blue square so mobile home screens mask them cleanly. The
16 px and 32 px versions have a slightly thickened white glyph so the stethoscope stays legible in a
browser tab.

Icon links carry a `?v=2` cache-buster. When the icon changes, bump that number in the `<head>` of every
page (and in `404.html`) so returning visitors fetch the new file instead of a cached copy.

If a higher-resolution or vector version of the icon becomes available, replace
`assets/img/patient-aid-icon.png` and run `python tools/make_assets.py` to regenerate every size.

Feature icons are hand-authored inline SVG paths (no third-party icon licence required). They can be
swapped for Lucide or Bootstrap Icons if you prefer.

### 3.3 Regenerating brand assets

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
| Domain | `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, schema URLs, `sitemap.xml`, `robots.txt` | Run `python tools/set_domain.py https://your-domain` — it updates every absolute URL and removes the TODO notes |
| Screenshots | `assets/img/screens/*.webp`, image `src`/`alt`, gallery `data-full` | Genuine screenshots are in place; refresh them if the app UI changes |
| Logo & icons | `assets/img/patient-aid-icon.png` + generated sizes | Official icon is in use; replace the source PNG and re-run `tools/make_assets.py` if a higher-resolution asset arrives |
| Privacy policy | `privacy.html` | Replace the placeholder text with the official policy, or point the links to the policy on itmedicus.com |
| Statistics | Home page stats band (`index.html`, `#stats`) | The figures **3M+ downloads**, **150K+ reviews** and a **4.5 / 5 rating** were supplied for this build. Confirm they are current and approved, then update `data-count-to` / `data-count-suffix` / `data-count-decimals`, the star row, **and** the visible fallback text together |
| Contact details | Footer, `contact.html`, structured data | Confirm address, email, and phone with ITmedicus |
| Premium terms | `premium.html`, home Premium section | Confirm current features, pricing, and subscription conditions |
| Demo notice | `privacy.html` callouts, `README`, `TEST_REPORT.md` | Remove placeholder notices once real content is in place |

The site displays no star rating and makes no "doctor approved" style claims. The only figures shown are
the client-supplied download and review counts in the stats band; confirm them against the live Google
Play listing before launch, and add any further figures only with product-owner approval.

---

## 6. SEO

Everything search engines need is in the HTML itself — no plugin, build step, or JavaScript rendering required.

### Metadata

Every page has a unique, keyword-led title (46–60 characters) and meta description (121–155 characters), a canonical URL, Open Graph and Twitter card tags with the 1200 × 630 preview image, `robots` directives (`index, follow, max-image-preview:large`), and an author tag. Open Graph descriptions are slightly longer than the meta descriptions and are safe to edit independently.

### Production domain

All absolute URLs currently use `https://patientaid.example.com` as a placeholder. Switch every
canonical, Open Graph URL, schema URL, sitemap entry, and robots link in one command:

```powershell
python tools/set_domain.py https://www.patientaid.com
```

It rewrites 125 URLs across the seven pages, `sitemap.xml`, and `robots.txt`, and removes the
"replace the domain" TODO comments. The script validates the argument before touching anything.

### Structured data

| Page | Schema types |
| --- | --- |
| All pages | `Organization`, `WebSite`, `WebPage` (shared `@id`s) |
| Sub-pages | `BreadcrumbList` matching the visible breadcrumb |
| Home | `SoftwareApplication` — Android, HealthApplication, free offer, screenshots, download URL, `aggregateRating` 4.5 / 150K ratings |
| FAQ | `FAQPage` with all ten questions and answers |

> Keep the `aggregateRating` values aligned with the stats band and the live Google Play listing. If the rating or review count changes, update both the visible numbers and this schema block in `index.html`.

### Crawling and indexing

- `robots.txt` allows the site, blocks `/tools/`, and declares the sitemap.
- `sitemap.xml` lists all seven pages with `lastmod`, `changefreq`, and priority.
- `404.html` is `noindex, follow` with a clear route back to the main pages. Point the host at it for
  unknown paths (Netlify and GitHub Pages do this automatically; on Apache add
  `ErrorDocument 404 /404.html`).
- Semantic landmarks, a single `H1` per page, descriptive `alt` text on every screenshot, and `lang="bn"` on the Bangla sample content.
- A complete favicon set (`favicon.ico`, SVG, 16–192 px PNGs), apple-touch icon, and `manifest.json`.
- Internal links come from the header, footer, breadcrumbs, and contextual links in body copy.

### Core Web Vitals

- Hero screenshot is preloaded (`fetchpriority="high"`) and is the LCP element.
- All other images are lazy-loaded with explicit `width`/`height`, so there is no layout shift.
- WebP screenshots (25–83 KB each), one CSS file, one JS file, `preconnect` + `display=swap` fonts.

### After launch

1. Run `python tools/set_domain.py https://your-domain` and deploy.
2. Add the property in Google Search Console and submit `sitemap.xml`.
3. Check the home page in the [Rich Results Test](https://search.google.com/test/rich-results).
4. Re-check the download, review, and rating figures against the Play listing each quarter.

---

## 7. Quality checks

The site was verified with an automated suite (509 checks across 7 pages × 3 viewports) covering
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

## 8. Browser support

Tested in current Chromium (Chrome/Edge). The layout uses modern but widely supported CSS: grid,
flexbox, `clamp()`, `aspect-ratio`, `:focus-visible`, CSS masks, `backdrop-filter`, and
`prefers-reduced-motion`. Internet Explorer is not supported.

---

## 9. Medical disclaimer

The disclaimer is present in the footer of every page and on `faq.html`:

> Patient Aid provides healthcare and medicine information for general educational and informational
> purposes only. The information available in the application is not a substitute for professional
> medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional regarding
> medical conditions, medications, or treatment decisions.
#
