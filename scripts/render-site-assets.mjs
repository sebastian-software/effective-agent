import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";

// Render the Field Guide product identity. The corporate master vectors remain separate.
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
const icon = await svgData(resolve(assets, "brand/field-guide.svg"));
const hero = `data:image/png;base64,${(await readFile(resolve(assets, "illustrations/field-guide-desk.png"))).toString("base64")}`;
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
  await writeFile(resolve(assets, "apple-touch-icon.png"), await renderIcon(180, "#f8f5ec"));

  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<!doctype html><html lang="en"><meta charset="utf-8"><style>
    @font-face{font-family:"Sebastian Slab";src:url("${headingFont}") format("woff2");font-weight:500;font-style:normal;font-display:swap}
    *{box-sizing:border-box}body{margin:0;background:#f8f5ec;color:#18372b;font-family:system-ui,sans-serif}
    main{height:630px;padding:48px 60px;position:relative;overflow:hidden}
    header{display:flex;align-items:center;gap:14px}header img{width:60px;height:60px}
    .brand{font:500 30px/1.2 "Sebastian Slab",Georgia,serif}
    .eyebrow{margin:55px 0 18px;font-size:13px;letter-spacing:2px;color:#774021}
    h1{position:relative;z-index:1;font:500 70px/1.06 "Sebastian Slab",Georgia,serif;letter-spacing:-2px;margin:0;max-width:560px}
    .intro{position:relative;z-index:1;font-size:20px;line-height:1.5;max-width:430px;color:#4c5b50;margin:24px 0}
    .art{position:absolute;right:-12px;top:140px;width:640px;height:auto}
    footer{position:absolute;bottom:34px;left:60px;right:60px;padding-top:20px;border-top:1px solid #d4d7ca;color:#18372b;font-size:18px}
  </style><main><header><img src="${icon}" alt=""><div class="brand">Effective Agent</div></header>
  <p class="eyebrow">OPEN-SOURCE SKILLS FOR AI AGENTS</p>
  <h1>Practical skills.<br>Better work.</h1>
  <p class="intro">A small library for bigger work.<br>Install the skill your next task needs.</p>
  <img class="art" src="${hero}" alt="An illustrated collection of field guides">
  <footer>effective-agent.dev</footer></main></html>`);
  await page.locator("img").evaluateAll((images) => Promise.all(images.map((image) => image.decode())));
  await page.evaluate(() => document.fonts.ready);
  assert.ok(await page.evaluate(() => [...document.fonts].some(
    (font) => font.family === "Sebastian Slab" && font.status === "loaded"
  )), "The brand heading font must load before rendering the social preview");
  await page.screenshot({ path: resolve(assets, "og-card.png") });
  console.log("Rendered Field Guide product favicons, Apple touch icon, and 1200×630 social preview.");
} finally {
  await browser.close();
}
