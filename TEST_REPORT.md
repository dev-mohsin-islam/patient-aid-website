# Patient Aid Website — Test Report

**Project:** Patient Aid marketing website (static HTML/CSS/JS)
**Prepared for:** ITmedicus Solutions
**Test date:** 10 November 2026
**Tested build:** `D:\patient-aid-website` (workspace source)
**Browser:** Google Chrome 157.0.8103.38 (headless, DevTools Protocol)
**Viewports:** desktop 1440 × 1000 · tablet 820 × 1100 · mobile 390 × 844

---

## 1. Result summary

| Area | Result |
| --- | --- |
| Automated checks | **509 / 509 passed (0 failures)** |
| Pages tested | 7 of 7 (`index`, `about`, `features`, `premium`, `faq`, `contact`, `privacy`) |
| Viewports tested | 3 (desktop, tablet, mobile) |
| Console errors / JS exceptions | 0 |
| Broken internal links or missing assets | 0 |
| Horizontal overflow (all pages, all viewports) | None detected |
| Broken images / missing `alt` text | None detected |
| Play Store links | Every download link on all 21 page/viewport combinations opens the correct listing in a new tab with `rel="noopener noreferrer"` |
| Manual visual review | Completed at all three viewports (layout, spacing, hierarchy, contrast) |

---

## 2. How the site was tested

1. **Automated suite** — `tools/qa.mjs` launches headless Chrome, loads every page at three viewports,
   and runs DOM, network, and interaction assertions. It also exercises the mobile menu, FAQ
   accordion, language switcher, and lightbox with real clicks and keyboard events.
2. **Visual review** — full-page and viewport screenshots were captured with `tools/shot.mjs` and
   inspected for spacing, alignment, typography, image cropping, and overlap at 1440 px, 820 px,
   and 390 px widths.
3. **Static review** — every relative `href`/`src` in the HTML was resolved against the file system to
   confirm the target exists (0 missing references), and the content was checked against the supplied
   brief for wording and scope.

Re-run with:

```powershell
node tools/qa.mjs
```

Raw results: `tools/preview/qa-results.json`.

---

## 3. Automated coverage

Each of the 21 page/viewport combinations was checked for the following (21 passes each unless noted):

| Check | Passed | Notes |
| --- | --- | --- |
| No horizontal overflow | 21/21 | `scrollWidth` never exceeds `innerWidth` |
| All images load | 21/21 | Includes lazy images forced to load |
| All images have `alt` | 21/21 | Descriptive alt on every screenshot and logo |
| Images declare width/height | 21/21 | Prevents layout shift |
| Exactly one `<h1>` per page | 21/21 | Logical heading hierarchy |
| No duplicate element IDs | 21/21 | Accordion, lightbox, and tab IDs are unique |
| In-page anchors resolve | 21/21 | e.g. `index.html#download`, privacy TOC links |
| No placeholder links (`#`, empty, `javascript:`) | 21/21 | |
| Play Store links correct | 21/21 | Exact listing URL, `target="_blank"`, `noopener` |
| Meta description length | 21/21 | Unique description per page, 70–320 chars |
| Open Graph + Twitter metadata | 21/21 | Title, description, image, card type |
| Canonical URL | 21/21 | Placeholder domain, documented in README |
| Responsive viewport meta | 21/21 | `width=device-width, initial-scale=1` |
| `<main>` landmark + skip link | 21/21 | Keyboard users can skip the navigation |
| Medical disclaimer in footer | 21/21 | Visible on every page |
| `lang` attribute | 21/21 | `lang="en"` |
| Sticky header | 14/14 | Desktop and tablet |
| Mobile menu button visible | 7/7 | Mobile only |
| Mobile menu opens and closes | 7/7 | `aria-expanded` toggles, Escape closes |
| FAQ accordion toggles | 3/3 | `aria-expanded`/`aria-hidden` + panel height |
| Language switcher works | 3/3 | Switches Bangla/English sample panels |
| Lightbox opens and closes | 3/3 | Opens correct image, Escape closes, body unlock |
| Title length | 21/21 | Unique titles, 46–60 characters |
| Robots + canonical | 21/21 | `index, follow, max-image-preview:large`; absolute HTTPS canonical |
| Structured data parses | 21/21 | `Organization`, `WebSite`, `WebPage` on every page; no JSON errors |
| Breadcrumb structured data | 21/21 | `BreadcrumbList` matches the visible breadcrumb on sub-pages |
| 404 page | 1/1 | `noindex`, no canonical, heading and recovery links present |
| Favicon set + web manifest | 21/21 | ICO, SVG, PNG icons, apple-touch icon, and manifest linked |
| Download, review and rating stats | 3/3 | Stats band renders 3M+ downloads, 150K+ reviews and a 4.5 rating with 5 stars |
| Scroll progress bar updates | 21/21 | Bar scales with page progress after scrolling |
| Hero entrance animations configured | 3/3 | Staggered copy, phone, glow, float cards, brand draw |
| Parallax disabled under reduced motion | 3/3 | Hero visual stays still for reduced-motion users |

**Total: 509 checks, 509 passed.**

---

## 4. Feature verification (home page)

| Feature | Expected | Result |
| --- | --- | --- |
| Sticky navigation | Header remains at top while scrolling; border/shadow appears after scroll | Pass |
| Primary navigation | Home, About, Features, Premium, FAQ, Contact link to the correct pages | Pass |
| Active page indicator | Current page underlined and marked `aria-current="page"` | Pass |
| Download App button (header) | Opens the Patient Aid Play Store listing in a new tab | Pass |
| Hero primary CTA | Same listing, new tab, `rel="noopener noreferrer"` | Pass |
| Hero secondary CTA | Navigates to `features.html` | Pass |
| Hero supporting points | "Available for Android", "Free to Download", "Bangla & English" shown with check icons | Pass |
| Trust strip | Four qualitative facts; no unverified statistics | Pass |
| Stats band | 3M+ downloads, 150K+ reviews and a 4.5 / 5 rating with stars; counters animate on first view | Pass |
| Feature cards | 12 cards on home, 13 on features page + Premium card | Pass |
| Offline section | Benefits list + internet-requirement qualification note | Pass |
| Bangla/English section | Tabs switch sample content; Bangla renders with fallback font | Pass |
| Medicine information | Six sub-topics plus medicine-details mockup | Pass |
| My Medicine | Benefits list, Premium link, family-profiles mockup | Pass |
| Premium | Benefit list, terms qualification, Play Store CTA | Pass |
| Screenshot gallery | 12 captioned genuine screenshots, 4/3/2-column responsive grid, lightbox | Pass |
| Lightbox | Click opens larger preview with caption; ←/→ navigate; Esc closes; focus returns | Pass |
| Why Patient Aid | Six reasons | Pass |
| Developer section | ITmedicus copy, outbound website link, logo | Pass |
| FAQ accordion | Six questions; single open item; keyboard operable | Pass |
| Final CTA | Store badge + "It's Free to Get Started" line | Pass |
| Footer | Quick links, useful links, contact details, disclaimer, copyright | Pass |
| Back-to-top button | Appears after scrolling; returns to top | Pass (manual) |

---

## 5. Responsive layout review

| Viewport | Findings |
| --- | --- |
| **1440 × 1000 (desktop)** | Two-column hero with phone mockup and two floating cards; 3-column feature grid; 5-column gallery; 4-column footer. No overflow, no clipping. |
| **820 × 1100 (tablet)** | Navigation collapses to hamburger below 860 px; hero stacks with the phone centred; 2-column grids; gallery 3 columns; footer 2 columns. No overflow. |
| **390 × 844 (mobile)** | Single column, full-width CTAs, phone mockup scaled, feature cards stacked, gallery 2 columns, footer stacked, lightbox controls moved below the image. No overflow; tap targets ≥ 44 px for the menu button and lightbox controls. |

Manual checks at each viewport included: heading line breaks, text line length, card heights,
screenshot aspect ratios (no stretching), float-card overlap, footer column balance, and contrast of
muted text on alternating backgrounds.

---

## 6. Accessibility checks

- Semantic landmarks (`header`, `nav`, `main`, `footer`, `section`), one `h1` per page, ordered headings.
- Skip-to-content link as the first focusable element.
- Visible `:focus-visible` outlines on links, buttons, tabs, and gallery items.
- FAQ buttons expose `aria-expanded`, `aria-controls`, and hidden/inert panels for screen readers.
- Lightbox is a labelled `role="dialog"` with `aria-modal="true"`, focus moved to the close button,
  focus trapped while open, and focus restored on close.
- Mobile menu button exposes `aria-expanded` and an accessible name that changes between open/close.
- Language tabs follow the ARIA tabs pattern with arrow-key support.
- Images have descriptive `alt` text; decorative icons are `aria-hidden="true"`.
- Animations respect `prefers-reduced-motion`.
- No text smaller than 13 px; body copy 16–16.5 px with a minimum 4.5:1 contrast target.

Not covered by automation: a full WCAG 2.1 AA audit with assistive technology, and real-device
testing. Both are recommended before launch.

### Motion

The animation layer was verified in both motion modes:

| Behaviour | Normal motion | Reduced motion |
| --- | --- | --- |
| Hero entrance choreography | Staggered rise, phone scale-in, float-card pop | Instant, static |
| Logo settle | Pops in gently on load | Instant |
| Scroll progress bar | Tracks page progress | Tracks page progress (decorative) |
| Hero pointer parallax | Follows pointer within ~7 px | Disabled (asserted by the suite) |
| Section reveals | Fade/slide in on entry | Instant, visible |
| Stat counters | Count up when the stats band enters view | Final values immediately |
| Hover micro-interactions | Button sheen, icon lift, card lift | Transitions reduced to near-zero |

All motion is implemented with `transform`/`opacity` only, so it runs on the compositor and cannot
cause layout shift. Entrance animations use `both` fill: the settled state is identical to the
unanimated layout, so nothing can remain hidden or displaced. Animations never run on the critical
path for content: text is painted as the fade begins rather than after it completes.

---

## 7. SEO verification

| Item | Result |
| --- | --- |
| Unique titles | 7/7, 46–60 characters, keyword-led |
| Meta descriptions | 7/7, 121–155 characters |
| Canonical URLs | Absolute HTTPS on every page (placeholder domain until launch) |
| Robots meta | `index, follow, max-image-preview:large` on all public pages |
| Open Graph + Twitter | 7/7 with 1200 × 630 image and alt text |
| Structured data | `Organization`, `WebSite`, `WebPage` sitewide; `BreadcrumbList` on sub-pages; `SoftwareApplication` + `aggregateRating` on home; `FAQPage` on the FAQ |
| Sitemap / robots | `sitemap.xml` lists all 7 pages; `robots.txt` allows crawl, blocks `/tools/`, declares the sitemap |
| 404 page | `noindex, follow`, no canonical, recovery links |
| Language | `html lang="en"`; the Bangla sample is marked `lang="bn"` |
| Images | Descriptive alt text, explicit dimensions, lazy below the fold, hero preloaded |
| Internal linking | Header, footer, breadcrumbs, and in-content links |

`tools/set_domain.py` was tested against a copy of the project: 125 absolute URLs across the seven
pages, `sitemap.xml`, and `robots.txt` switched to the new origin, and the TODO comments were removed.

> The `aggregateRating` (4.5, 150,000 ratings) mirrors the visible stats band and must be kept in sync
> with the live Google Play listing.

---

## 8. Performance considerations

- No frameworks or libraries; one CSS file (~57 KB unminified) and one JS file (~12 KB).
- Animation is GPU-friendly (`transform`/`opacity` only) and respects `prefers-reduced-motion`.
- Twelve genuine app screenshots are WebP (25–83 KB each) with explicit dimensions.
- Hero image is preloaded with `fetchpriority="high"`; all other images are `loading="lazy"` with
  `decoding="async"`.
- Fonts use `preconnect` + `display=swap` with a system fallback stack, so text renders before the
  webfont arrives.
- No layout shift from images (dimensions declared), no web font blocking of first paint.

---

## 9. Content and scope review

- All marketing copy follows the supplied brief. The download (3M+), review (150K+) and rating (4.5 / 5)
  figures were supplied by the client for this build; no other statistics, ratings, or medical claims
  are shown.
- No medicine search, doctor search, hospital search, booking, account, or backend features exist on
  the site; all such functionality is described as app-only.
- The medical disclaimer appears in the footer of every page and as a dedicated note on `faq.html`.
- Premium claims match the brief, with the "subject to the terms displayed within the application"
  qualification retained.
- The `privacy.html` page is clearly marked as a placeholder pending the official policy.

---

## 10. Known limitations before launch

| Item | Status |
| --- | --- |
| App screenshots | Genuine screenshots supplied and in use (WebP); refresh if the app UI changes |
| Logo, favicon, social image | Official app icon supplied; all sizes generated from it (refresh if a higher-resolution source arrives) |
| Domain in canonical/OG/sitemap/robots | `patientaid.example.com` placeholder; run `python tools/set_domain.py https://your-domain` before launch |
| Privacy policy | Placeholder outline; replace with the official policy URL/content |
| App statistics / ratings | 3M+ downloads, 150K+ reviews and a 4.5 / 5 rating are displayed as supplied; confirm all three against the live Google Play listing before launch |
| Contact details | Taken from the brief; reconfirm with ITmedicus before publishing |
| Accessibility audit | Automated + manual review only; full assistive-technology audit recommended |
| Real-device testing | Recommended for iOS/Android browsers before launch |

---

## 11. Sign-off checklist

- [x] All 7 pages render without console errors
- [x] Navigation, footer links, and in-page anchors resolve
- [x] Every download button opens the correct Google Play listing in a new tab
- [x] Screenshot gallery and lightbox work with mouse, keyboard, and touch-sized controls
- [x] FAQ accordion and language switcher work with keyboard
- [x] Mobile menu opens, closes, and closes on Escape
- [x] Responsive layouts verified at 1440 px, 820 px, and 390 px
- [x] SEO metadata, Open Graph, Twitter card, sitemap, robots, favicon present
- [x] Medical disclaimer visible site-wide
- [x] README documents setup, deployment, and asset replacement
- [ ] Replace demo screenshots, logo, and social image (client)
- [ ] Confirm production domain and privacy policy URL (client)
- [ ] Verify contact details, Premium terms, and any statistics (client)
