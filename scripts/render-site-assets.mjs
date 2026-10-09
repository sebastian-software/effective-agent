import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";

// Render the original brand vectors; do not redraw or recolor their paths.
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const assets = resolve(root, "site/assets");
const executablePath = [
  process.env.CHROME_BIN,
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
].filter(Boolean).find(existsSync);
assert.ok(executablePath, "Chrome was not found; set CHROME_BIN to render site assets");
const svgData = async (path) => `data:image/svg+xml;base64,${(await readFile(path)).toString("base64")}`;
const icon = await svgData(resolve(assets, "brand/software-on-light.svg"));
const logo = await svgData(resolve(assets, "brand/logo-software.svg"));
const gptSeal = await svgData(resolve(assets, "seals/gpt-6.svg"));
const opusSeal = await svgData(resolve(assets, "seals/opus-5-5.svg"));
const headingFont = "https://assets.sebastian-software.com/fonts/Elena/Elena-Medium-latin-f0e984d3e709.woff2";
const browser = await chromium.launch({ executablePath, headless: true });

try {
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  const renderIcon = async (size, background = "transparent") => {
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<style>html,body{margin:0;width:100%;height:100%;background:${background}}img{display:block;width:100%;height:100%}</style><img src="${icon}" alt="">`);
    await page.locator("img").evaluate((image) => image.decode());
    return page.screenshot({ omitBackground: background === "transparent" });
  };
  const entries = [];
  for (const size of [16, 32, 48]) {
    const png = await renderIcon(size);
    entries.push({ size, png });
    if (size === 32) await writeFile(resolve(assets, "favicon-32.png"), png);
  }
  const header = Buffer.alloc(6 + 16 * entries.length);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(entries.length, 4);
  let offset = header.length;
  entries.forEach(({ size, png }, index) => {
    const start = 6 + index * 16;
    header[start] = size;
    header[start + 1] = size;
    header.writeUInt16LE(1, start + 4);
    header.writeUInt16LE(32, start + 6);
    header.writeUInt32LE(png.length, start + 8);
    header.writeUInt32LE(offset, start + 12);
    offset += png.length;
  });
  await writeFile(resolve(root, "site/favicon.ico"), Buffer.concat([header, ...entries.map(({ png }) => png)]));
  await writeFile(resolve(assets, "apple-touch-icon.png"), await renderIcon(180, "#e7f0f3"));

  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<!doctype html><html lang="en"><meta charset="utf-8"><style>
    @font-face{font-family:"Sebastian Slab";src:url("${headingFont}") format("woff2");font-weight:500;font-style:normal;font-display:swap}
    *{box-sizing:border-box}body{margin:0;background:#e7f0f3;color:#002731;font-family:system-ui,sans-serif}
    main{height:630px;padding:48px 64px 0;position:relative}
    header{display:flex;align-items:center;justify-content:space-between}
    header img{width:440px;height:auto}header span{font-size:18px;letter-spacing:3px;color:#005164}
    h1{font-family:"Sebastian Slab",Georgia,serif;font-size:65px;line-height:1.1;letter-spacing:-1.43px;font-weight:500;margin:55px 0 35px;max-width:670px}
    h1 span{color:#00718d}p{font-size:16px;letter-spacing:0.4px;word-spacing:5px;margin:0;color:#005164}
    .seals{position:absolute;right:55px;top:186px;display:flex;gap:12px}.seals img{width:175px;height:175px}
    footer{position:absolute;bottom:0;left:0;right:0;background:#005164;color:#e7f0f3;padding:26px 64px;font-size:22px}
  </style><main><header><img src="${logo}" alt="Sebastian Software"><span>EFFECTIVE AGENT</span></header>
  <h1>Better judgment.<br>From idea to <span>market.</span></h1>
  <div class="seals"><img src="${gptSeal}" alt="Tuned for GPT-6"><img src="${opusSeal}" alt="Tuned for Opus 5.5"></div>
  <p>PRODUCT · WEB · ENGINEERING · DELIVERY · MARKETING · WRITING · IMAGE</p>
  <footer>effective-agent.dev</footer></main></html>`);
  await page.locator("img").evaluateAll((images) => Promise.all(images.map((image) => image.decode())));
  await page.evaluate(() => document.fonts.ready);
  assert.ok(await page.evaluate(() => [...document.fonts].some(
    (font) => font.family === "Sebastian Slab" && font.status === "loaded"
  )), "The brand heading font must load before rendering the social preview");
  await page.screenshot({ path: resolve(assets, "og-card.png") });
  console.log("Rendered official brand favicons, Apple touch icon, and 1200×630 social preview.");
} finally {
  await browser.close();
}
