/**
 * Screenshot helper (no dependencies): drives headless Chrome over the
 * DevTools Protocol to capture full-page or viewport screenshots and to
 * report console/page errors.
 *
 * Usage:
 *   node tools/shot.mjs --url file:///D:/site/index.html --out shot.png \
 *        --width 1440 --height 1000 [--full] [--mobile] [--scale 1]
 */

import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function arg(name, fallback = undefined) {
  const i = process.argv.indexOf(`--${name}`);
  if (i === -1) return fallback;
  const v = process.argv[i + 1];
  return v === undefined || v.startsWith("--") ? true : v;
}

const url = arg("url");
const out = arg("out");
const width = Number(arg("width", 1440));
const height = Number(arg("height", 1000));
const full = Boolean(arg("full", false));
const mobile = Boolean(arg("mobile", false));
const motion = Boolean(arg("motion", false));
const scale = Number(arg("scale", 1));
const waitMs = Number(arg("wait", 900));
const evalJs = arg("eval", "");

if (!url || !out) {
  console.error("missing --url or --out");
  process.exit(2);
}

const port = 9400 + Math.floor(Math.random() * 400);
const userDataDir = path.join(os.tmpdir(), `dsh-shot-${Date.now()}`);

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

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function getJson(pathname) {
  for (let i = 0; i < 100; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}${pathname}`);
      if (res.ok) return await res.json();
    } catch {
      /* not up yet */
    }
    await sleep(100);
  }
  throw new Error("Chrome DevTools endpoint did not start");
}

const cleanup = async () => {
  try {
    chrome.kill();
  } catch {
    /* ignore */
  }
  await sleep(150);
  try {
    await fs.rm(userDataDir, { recursive: true, force: true });
  } catch {
    /* ignore */
  }
};

try {
  const targets = await getJson("/json/list");
  const page = targets.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  const pending = new Map();
  let nextId = 1;
  const errors = [];

  const send = (method, params = {}) =>
    new Promise((resolve, reject) => {
      const id = nextId++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });

  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  ws.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(`${msg.error.message} (${msg.error.code})`));
      else resolve(msg.result);
      return;
    }
    if (msg.method === "Runtime.exceptionThrown") {
      const d = msg.params.exceptionDetails;
      errors.push(`exception: ${d.exception?.description || d.text}`);
    }
    if (msg.method === "Log.entryAdded" && msg.params.entry.level === "error") {
      errors.push(`log: ${msg.params.entry.text} ${msg.params.entry.url || ""}`);
    }
  });

  await send("Page.enable");
  await send("Runtime.enable");
  await send("Log.enable");

  await send("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: scale,
    mobile,
    screenWidth: width,
    screenHeight: height,
  });
  if (!motion) {
    await send("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }],
    });
  }

  const loaded = new Promise((resolve) => {
    const handler = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.method === "Page.loadEventFired") {
        ws.removeEventListener("message", handler);
        resolve();
      }
    };
    ws.addEventListener("message", handler);
  });

  await send("Page.navigate", { url });
  await loaded;
  await sleep(waitMs);

  await send("Runtime.evaluate", {
    expression: `(async () => {
      if (document.fonts && document.fonts.ready) { try { await document.fonts.ready; } catch (e) {} }
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
      // Force lazy images to load so full-page captures are complete.
      document.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; });
      await Promise.all(Array.from(document.images).map(img =>
        img.complete ? Promise.resolve() : new Promise(res => { img.onload = img.onerror = res; })
      ));
      // WebP/PNG decoding can finish after load; wait for actual decode where supported.
      await Promise.all(Array.from(document.images).map(img =>
        img.decode ? img.decode().catch(() => {}) : Promise.resolve()
      ));
      return document.images.length;
    })()`,
    awaitPromise: true,
    returnByValue: true,
  });
  await sleep(400);

  if (typeof evalJs === "string" && evalJs.length > 0) {
    await send("Runtime.evaluate", {
      expression: evalJs,
      awaitPromise: true,
      returnByValue: true,
    });
    await sleep(350);
  }

  let clip;
  if (full) {
    const metrics = await send("Page.getLayoutMetrics");
    const size = metrics.cssContentSize || metrics.contentSize;
    clip = { x: 0, y: 0, width: Math.ceil(size.width), height: Math.ceil(size.height), scale: 1 };
  }

  const result = await send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: full,
    fromSurface: true,
    ...(clip ? { clip } : {}),
  });

  await fs.mkdir(path.dirname(out), { recursive: true });
  await fs.writeFile(out, Buffer.from(result.data, "base64"));
  console.log(`saved ${out}` + (errors.length ? `\nERRORS:\n${errors.join("\n")}` : "\nno console errors"));
} finally {
  await cleanup();
}
