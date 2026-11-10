/**
 * Automated QA for the Patient Aid static site.
 *
 * Drives headless Chrome over the DevTools Protocol to check, for every page
 * and both a desktop and a mobile viewport:
 *   - horizontal overflow (layout breakage)
 *   - broken images / missing alt attributes
 *   - heading structure and duplicate ids
 *   - in-page anchor targets
 *   - Play Store links (exact URL, new tab, rel=noopener)
 *   - meta/OG/SEO tags
 * and, on the home page, real interaction tests for the mobile menu, FAQ
 * accordion, language switcher, and screenshot lightbox.
 *
 * Usage: node tools/qa.mjs
 */

import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const SITE = path.resolve(".");
const STORE_URL = "https://play.google.com/store/apps/details?id=com.itmedicus.patientaid";
const PAGES = [
  "index.html",
  "about.html",
  "features.html",
  "premium.html",
  "faq.html",
  "contact.html",
  "privacy.html",
];

const port = 9600 + Math.floor(Math.random() * 300);
const userDataDir = path.join(os.tmpdir(), `dsh-qa-${Date.now()}`);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const results = [];
let failures = 0;

function record(page, viewport, name, ok, detail = "") {
  results.push({ page, viewport, name, ok, detail });
  if (!ok) failures++;
  const label = `${ok ? "PASS" : "FAIL"}  ${page} [${viewport}]  ${name}`;
  console.log(detail && !ok ? `${label} — ${detail}` : label);
}

const chrome = spawn(
  CHROME,
  [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-background-networking",
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    "about:blank",
  ],
  { stdio: "ignore" }
);

async function endpoint(pathname, init) {
  for (let i = 0; i < 100; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}${pathname}`, init);
      if (res.ok) return await res.json();
    } catch {
      /* starting */
    }
    await sleep(100);
  }
  throw new Error("DevTools endpoint unavailable");
}

class Tab {
  constructor(target) {
    this.target = target;
    this.id = 1;
    this.pending = new Map();
    this.events = [];
  }

  async open() {
    this.ws = new WebSocket(this.target.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
      this.ws.addEventListener("open", resolve, { once: true });
      this.ws.addEventListener("error", reject, { once: true });
    });
    this.ws.addEventListener("message", (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      } else if (msg.method) {
        this.events.push(msg);
      }
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async goto(url, width, height, mobile) {
    await this.send("Page.enable");
    await this.send("Runtime.enable");
    await this.send("Emulation.setDeviceMetricsOverride", {
      width,
      height,
      deviceScaleFactor: 1,
      mobile,
      screenWidth: width,
      screenHeight: height,
    });
    await this.send("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }],
    });
    const loaded = new Promise((resolve) => {
      const handler = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.method === "Page.loadEventFired") {
          this.ws.removeEventListener("message", handler);
          resolve();
        }
      };
      this.ws.addEventListener("message", handler);
    });
    await this.send("Page.navigate", { url });
    await loaded;
    await sleep(450);
    await this.eval(`(async () => {
      if (document.fonts && document.fonts.ready) { try { await document.fonts.ready; } catch (e) {} }
      document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
      await Promise.all(Array.from(document.images).map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
      return true;
    })()`);
    await sleep(200);
  }

  async eval(expression) {
    const out = await this.send("Runtime.evaluate", {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (out.exceptionDetails) {
      return { __error: out.exceptionDetails.exception?.description || out.exceptionDetails.text };
    }
    return out.result.value;
  }

  async screenshot(file, opts = {}) {
    const shot = await this.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: Boolean(opts.full),
      fromSurface: true,
      ...(opts.clip ? { clip: opts.clip } : {}),
    });
    await fs.mkdir(path.dirname(file), { recursive: true });
    await fs.writeFile(file, Buffer.from(shot.data, "base64"));
  }

  async close() {
    try {
      this.ws.close();
    } catch {
      /* ignore */
    }
  }
}

async function createTab() {
  const target = await endpoint("/json/new?about:blank", { method: "PUT" });
  const tab = new Tab(target);
  await tab.open();
  return tab;
}

async function closeTab(tab) {
  await tab.close();
  try {
    await fetch(`http://127.0.0.1:${port}/json/close/${tab.target.id}`);
  } catch {
    /* ignore */
  }
}

const pageAudit = async (tab) => {
  return tab.eval(`(() => {
    const out = {};
    const doc = document.documentElement;

    out.overflow = doc.scrollWidth - window.innerWidth;
    out.scrollWidth = doc.scrollWidth;
    out.innerWidth = window.innerWidth;

    const imgs = Array.from(document.images);
    out.imagesTotal = imgs.length;
    out.imagesBroken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src);
    out.imagesNoAlt = imgs.filter(i => !i.hasAttribute('alt')).map(i => i.currentSrc || i.src);
    out.imagesNoDims = imgs.filter(i => !(i.getAttribute('width') && i.getAttribute('height'))).length;

    const headings = {};
    document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
      headings[h.tagName] = (headings[h.tagName] || 0) + 1;
    });
    out.headings = headings;

    const ids = {};
    document.querySelectorAll('[id]').forEach(el => { ids[el.id] = (ids[el.id] || 0) + 1; });
    out.duplicateIds = Object.keys(ids).filter(k => ids[k] > 1);

    out.brokenAnchors = [];
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      const id = a.getAttribute('href').slice(1);
      if (id && !document.getElementById(id)) out.brokenAnchors.push(a.getAttribute('href'));
    });

    const links = Array.from(document.querySelectorAll('a[href]'));
    out.storeLinks = links.filter(a => a.href.includes('play.google.com')).map(a => ({
      href: a.href,
      target: a.getAttribute('target'),
      rel: a.getAttribute('rel') || ''
    }));
    out.placeholderLinks = links.filter(a => {
      const h = a.getAttribute('href');
      return !h || h === '#' || h.startsWith('javascript:');
    }).length;

    out.title = document.title;
    out.description = (document.querySelector('meta[name="description"]') || {}).content || '';
    out.canonical = (document.querySelector('link[rel="canonical"]') || {}).href || '';
    out.ogTitle = (document.querySelector('meta[property="og:title"]') || {}).content || '';
    out.ogImage = (document.querySelector('meta[property="og:image"]') || {}).content || '';
    out.twitterCard = (document.querySelector('meta[name="twitter:card"]') || {}).content || '';
    out.viewport = (document.querySelector('meta[name="viewport"]') || {}).content || '';
    out.navCurrent = document.querySelectorAll('.primary-nav [aria-current="page"]').length;
    out.h1Text = (document.querySelector('h1') || {}).textContent?.trim() || '';
    out.mainExists = Boolean(document.querySelector('main#main'));
    out.skipLink = Boolean(document.querySelector('.skip-link'));
    out.lang = document.documentElement.lang;
    out.navToggleVisible = (() => {
      const t = document.querySelector('.nav-toggle');
      if (!t) return false;
      return getComputedStyle(t).display !== 'none';
    })();
    out.headerPosition = (() => {
      const h = document.querySelector('.site-header');
      return h ? getComputedStyle(h).position : 'none';
    })();
    out.footerDisclaimer = Boolean(document.querySelector('.footer-disclaimer'));
    out.textLength = document.body.innerText.length;
    return out;
  })()`);
};

const runPage = async (file, viewport) => {
  const url = "file:///" + path.join(SITE, file).replace(/\\/g, "/");
  const tab = await createTab();
  await tab.goto(url, viewport.width, viewport.height, viewport.mobile);
  const audit = await pageAudit(tab);
  const label = viewport.name;

  if (audit.__error) {
    record(file, label, "page audit", false, audit.__error);
    await closeTab(tab);
    return;
  }

  record(file, label, "no horizontal overflow", audit.overflow <= 1, `scrollWidth ${audit.scrollWidth} > innerWidth ${audit.innerWidth}`);
  record(file, label, "all images load", audit.imagesBroken.length === 0, `${audit.imagesBroken.length} broken: ${audit.imagesBroken.slice(0, 3).join(", ")}`);
  record(file, label, "all images have alt", audit.imagesNoAlt.length === 0, `${audit.imagesNoAlt.length} missing alt`);
  record(file, label, "images have width/height", audit.imagesNoDims === 0, `${audit.imagesNoDims} missing dimensions`);
  record(file, label, "exactly one h1", audit.headings.H1 === 1, JSON.stringify(audit.headings));
  record(file, label, "no duplicate ids", audit.duplicateIds.length === 0, audit.duplicateIds.join(", "));
  record(file, label, "in-page anchors resolve", audit.brokenAnchors.length === 0, audit.brokenAnchors.join(", "));
  record(file, label, "no placeholder links", audit.placeholderLinks === 0, `${audit.placeholderLinks} found`);
  record(file, label, "Play Store links correct", audit.storeLinks.length > 0 && audit.storeLinks.every(l => l.href.split("#")[0] === STORE_URL && l.target === "_blank" && /noopener/.test(l.rel)), JSON.stringify(audit.storeLinks.slice(0, 2)));
  record(file, label, "meta description length", audit.description.length >= 70 && audit.description.length <= 320, `${audit.description.length} chars`);
  record(file, label, "OG + Twitter metadata", Boolean(audit.ogTitle && audit.ogImage && audit.twitterCard), "");
  record(file, label, "canonical url", audit.canonical.startsWith("https://"), audit.canonical);
  record(file, label, "responsive viewport meta", /width=device-width/.test(audit.viewport), audit.viewport);
  record(file, label, "main landmark + skip link", audit.mainExists && audit.skipLink, "");
  record(file, label, "medical disclaimer in footer", audit.footerDisclaimer, "");
  record(file, label, "html lang set", audit.lang === "en", audit.lang);

  const seo = await tab.eval(`(() => {
    const meta = (name) => (document.querySelector('meta[name="' + name + '"]') || {}).content || '';
    const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
    const types = [];
    let parseErrors = 0;
    scripts.forEach((script) => {
      try {
        const data = JSON.parse(script.textContent);
        (data['@graph'] || [data]).forEach((node) => types.push(node['@type']));
      } catch (error) {
        parseErrors += 1;
      }
    });
    const canonical = document.querySelector('link[rel="canonical"]');
    return {
      titleLength: document.title.length,
      robots: meta('robots'),
      canonical: canonical ? canonical.href : '',
      types,
      parseErrors,
      breadcrumbSchema: types.includes('BreadcrumbList'),
      breadcrumbVisible: Boolean(document.querySelector('.breadcrumb'))
    };
  })()`);
  record(file, label, "title length", seo.titleLength >= 30 && seo.titleLength <= 65, `${seo.titleLength} chars`);
  record(file, label, "robots + canonical", /index/.test(seo.robots) && /^https:\/\//.test(seo.canonical), JSON.stringify({ robots: seo.robots, canonical: seo.canonical }));
  record(file, label, "structured data parses", seo.parseErrors === 0 && ["Organization", "WebSite", "WebPage"].every((type) => seo.types.includes(type)), JSON.stringify({ types: seo.types, errors: seo.parseErrors }));
  record(file, label, "breadcrumb structured data", file === "index.html" ? seo.breadcrumbSchema === false : seo.breadcrumbSchema === seo.breadcrumbVisible, JSON.stringify({ schema: seo.breadcrumbSchema, visible: seo.breadcrumbVisible }));

  const icons = await tab.eval(`(() => {
    const links = Array.from(document.querySelectorAll('link[rel="icon"], link[rel="apple-touch-icon"]'))
      .map((link) => link.getAttribute('href'));
    const manifest = document.querySelector('link[rel="manifest"]');
    return { count: links.length, manifest: manifest ? manifest.getAttribute('href') : '', hrefs: links };
  })()`);
  record(file, label, "favicon set + web manifest", icons.count >= 4 && /(webmanifest|manifest\.json)$/.test(icons.manifest), JSON.stringify(icons));

  if (viewport.mobile) {
    record(file, label, "mobile menu button visible", audit.navToggleVisible, "");
    const menu = await tab.eval(`(() => {
      const t = document.querySelector('.nav-toggle');
      const nav = document.getElementById('primaryNav');
      t.click();
      const open = nav.classList.contains('is-open');
      const expanded = t.getAttribute('aria-expanded');
      const navBox = nav.getBoundingClientRect();
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      const closed = !nav.classList.contains('is-open');
      return { open, expanded, visible: navBox.height > 100, closed };
    })()`);
    record(file, label, "mobile menu opens/closes", menu.open && menu.expanded === "true" && menu.visible && menu.closed, JSON.stringify(menu));
  } else {
    record(file, label, "sticky header", audit.headerPosition === "sticky", audit.headerPosition);
  }

  if (file === "index.html") {
    const faq = await tab.eval(`(() => {
      const btn = document.querySelector('.faq-q');
      const item = btn.closest('.faq-item');
      const panel = document.getElementById(btn.getAttribute('aria-controls'));
      const before = { expanded: btn.getAttribute('aria-expanded'), open: item.classList.contains('is-open') };
      btn.click();
      const opened = {
        expanded: btn.getAttribute('aria-expanded'),
        open: item.classList.contains('is-open'),
        hidden: panel.getAttribute('aria-hidden'),
        height: panel.getBoundingClientRect().height
      };
      btn.click();
      const closed = { expanded: btn.getAttribute('aria-expanded'), open: item.classList.contains('is-open') };
      return { before, opened, closed };
    })()`);
    record(file, label, "FAQ accordion toggles", faq.opened.expanded === "true" && faq.opened.open && faq.opened.hidden === "false" && faq.opened.height > 20 && faq.closed.expanded === "false" && !faq.closed.open, JSON.stringify(faq));

    const lang = await tab.eval(`(() => {
      const tabs = Array.from(document.querySelectorAll('.lang-tab'));
      if (tabs.length < 2) return { skip: true };
      tabs[1].click();
      const en = document.getElementById('langPanelEn');
      const bn = document.getElementById('langPanelBn');
      const state = { enHidden: en.hidden, bnHidden: bn.hidden, enSelected: tabs[1].getAttribute('aria-selected') };
      tabs[0].click();
      return state;
    })()`);
    record(file, label, "language switcher works", lang.skip || (!lang.enHidden && lang.bnHidden && lang.enSelected === "true"), JSON.stringify(lang));

    const box = await tab.eval(`(() => {
      const shot = document.querySelector('.shot');
      shot.click();
      const lb = document.querySelector('.lightbox');
      const open = lb.classList.contains('is-open');
      const src = lb.querySelector('img').getAttribute('src');
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      return { open, src, closed: !lb.classList.contains('is-open'), lockedAfter: document.body.classList.contains('is-locked') };
    })()`);
    record(file, label, "lightbox opens and closes", box.open && /screens\//.test(box.src) && box.closed && !box.lockedAfter, JSON.stringify(box));

    const stats = await tab.eval(`(() => {
      const els = Array.from(document.querySelectorAll('[data-count-to]'));
      return {
        section: Boolean(document.querySelector('#stats')),
        count: els.length,
        values: els.map(el => el.textContent.trim()),
        labels: Array.from(document.querySelectorAll('.stat-label')).map(el => el.textContent.trim()),
        stars: document.querySelectorAll('.stat-stars svg').length
      };
    })()`);
    record(file, label, "download, review and rating stats", stats.section && stats.count === 3 && stats.values[0] === "3M+" && stats.values[1] === "150K+" && stats.values[2] === "4.5" && /Downloads/i.test(stats.labels[0] || "") && /Reviews/i.test(stats.labels[1] || "") && /rating/i.test(stats.labels[2] || "") && stats.stars === 5, JSON.stringify(stats));

    if (!viewport.mobile) {
      await tab.eval(`document.querySelector('.shot').click(); true`);
      await sleep(350);
      await tab.screenshot(path.join("tools", "preview", `qa-lightbox-${label}.png`));
      await tab.eval(`document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); true`);
    } else {
      await tab.eval(`document.querySelector('.shot').click(); true`);
      await sleep(350);
      await tab.screenshot(path.join("tools", "preview", "qa-lightbox-mobile.png"));
      await tab.eval(`document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); true`);
    }
  }

  const motion = await tab.eval(`(async () => {
    const bar = document.querySelector('.scroll-progress');
    if (!bar) return { exists: false };
    window.scrollTo(0, Math.min(1400, document.documentElement.scrollHeight - window.innerHeight));
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const transform = getComputedStyle(bar).transform;
    window.scrollTo(0, 0);
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    return { exists: true, transform };
  })()`);
  record(file, label, "scroll progress bar updates", motion.exists && /matrix\(/.test(motion.transform) && !/^matrix\(0,/.test(motion.transform), JSON.stringify(motion));

  if (file === "index.html") {
    // QA runs with reduced motion emulated: parallax must stay disabled.
    const parallax = await tab.eval(`(async () => {
      const hero = document.querySelector('.hero');
      const visual = document.querySelector('.hero-visual');
      if (!hero || !visual) return { skip: true };
      const rect = hero.getBoundingClientRect();
      hero.dispatchEvent(new PointerEvent('pointermove', {
        clientX: rect.left + rect.width * 0.9,
        clientY: rect.top + rect.height * 0.25,
        bubbles: true
      }));
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      return { px: visual.style.getPropertyValue('--px') };
    })()`);
    record(file, label, "parallax disabled under reduced motion", parallax.skip || !parallax.px, JSON.stringify(parallax));

    // Entrance animations: check with the reduced-motion emulation switched off.
    await tab.send("Emulation.setEmulatedMedia", { features: [] });
    await sleep(150);
    const heroMotion = await tab.eval(`(() => {
      const names = (el) => (el ? getComputedStyle(el).animationName : 'none');
      return {
        copy: names(document.querySelector('.hero-copy > *')),
        phone: names(document.querySelector('.hero-visual .phone')),
        glow: names(document.querySelector('.hero-glow')),
        float: names(document.querySelector('.float-card')),
        mark: names(document.querySelector('.site-header .brand-mark img'))
      };
    })()`);
    record(file, label, "hero entrance animations configured", heroMotion.copy === "riseIn" && heroMotion.phone === "phoneIn" && /glowDrift/.test(heroMotion.glow) && /float/.test(heroMotion.float) && /popIn/.test(heroMotion.mark), JSON.stringify(heroMotion));
    await tab.send("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }],
    });
    await sleep(120);
  }

  await closeTab(tab);
};

try {
  await endpoint("/json/version");
  const viewports = [
    { name: "desktop", width: 1440, height: 1000, mobile: false },
    { name: "tablet", width: 820, height: 1100, mobile: false },
    { name: "mobile", width: 390, height: 844, mobile: true },
  ];

  for (const file of PAGES) {
    for (const viewport of viewports) {
      await runPage(file, viewport);
    }
  }

  // Custom 404 page: must be noindex, canonical-free, and link back home.
  const notFoundTab = await createTab();
  await notFoundTab.goto(
    "file:///" + path.join(SITE, "404.html").replace(/\\/g, "/"),
    1440,
    1000,
    false
  );
  const notFound = await notFoundTab.eval(`(() => {
    const meta = (name) => (document.querySelector('meta[name="' + name + '"]') || {}).content || '';
    return {
      robots: meta('robots'),
      canonical: Boolean(document.querySelector('link[rel="canonical"]')),
      h1: (document.querySelector('h1') || {}).textContent || '',
      homeLink: Boolean(document.querySelector('a[href="/index.html"]'))
    };
  })()`);
  record("404.html", "desktop", "404 is noindex with recovery links", /noindex/.test(notFound.robots) && !notFound.canonical && notFound.h1.trim().length > 3 && notFound.homeLink, JSON.stringify(notFound));
  await closeTab(notFoundTab);

  // Mobile menu open screenshot for the visual report.
  const tab = await createTab();
  await tab.goto("file:///" + path.join(SITE, "index.html").replace(/\\/g, "/"), 390, 844, true);
  await tab.eval(`document.querySelector('.nav-toggle').click(); true`);
  await sleep(350);
  await tab.screenshot(path.join("tools", "preview", "qa-mobile-menu.png"));
  await closeTab(tab);
} finally {
  const summary = {
    generatedAt: new Date().toISOString(),
    total: results.length,
    failures,
    results,
  };
  await fs.writeFile(path.join("tools", "preview", "qa-results.json"), JSON.stringify(summary, null, 2));
  console.log(`\n${results.length - failures}/${results.length} checks passed`);
  try {
    chrome.kill();
  } catch {
    /* ignore */
  }
  await sleep(200);
  await fs.rm(userDataDir, { recursive: true, force: true }).catch(() => {});
  process.exitCode = failures ? 1 : 0;
}
