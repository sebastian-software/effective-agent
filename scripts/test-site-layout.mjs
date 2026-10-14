import assert from "node:assert/strict";
import { existsSync, readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { chromium } from "playwright-core";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pageUrl = (name) => pathToFileURL(resolve(root, "site", name)).href;
const pages = [
  { name: "index.html", url: pageUrl("index.html"), isHome: true },
  { name: "comparisons.html", url: pageUrl("comparisons.html"), isHome: false },
  ...readdirSync(resolve(root, "site", "skills")).map((skill) => ({
    name: `skills/${skill}/index.html`,
    url: pageUrl(`skills/${skill}/index.html`),
    isHome: false,
    skill,
  })),
];
const mobileViewportMax = 400;
const viewports = [320, 360, 375, 400, 768, 1024, 1440];
const colorSchemes = ["light", "dark"];
const chromeCandidates = [
  process.env.CHROME_BIN,
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
].filter(Boolean);
const executablePath = chromeCandidates.find(existsSync);

assert.ok(
  executablePath,
  "Chrome was not found; set CHROME_BIN to run the viewport regression test"
);

const browser = await chromium.launch({ executablePath, headless: true });

const assertLayout = async (page, site, width, colorScheme) => {
  const layout = await page.evaluate(() => {
    const root = document.documentElement;
    const installer = document.querySelector(".installer");
    const codeBlocks = [...document.querySelectorAll(".code-block")];
    const breadcrumb = document.querySelector(".breadcrumbs");
    const header = document.querySelector(".site-header");
    return {
      breadcrumbBelowHeader: !breadcrumb || breadcrumb.getBoundingClientRect().top >= header.getBoundingClientRect().bottom,
      installerContained: Boolean(installer && installer.scrollWidth <= installer.clientWidth),
      clientWidth: root.clientWidth,
      codeBlocksContained: codeBlocks.every(
        (block) => block.scrollWidth <= block.clientWidth
      ),
      scrollWidth: root.scrollWidth,
      visibleInstallPanels: document.querySelectorAll(
        '.installer [role="tabpanel"]:not([hidden])'
      ).length,
    };
  });
  const context = `${site.name}, ${colorScheme}, ${width}px`;

  assert.ok(layout.breadcrumbBelowHeader, `${context}: the header must not cover the breadcrumb`);

  assert.ok(
    layout.scrollWidth <= layout.clientWidth,
    `${context}: document overflows: ${layout.scrollWidth}px > ${layout.clientWidth}px`
  );
  assert.ok(
    layout.codeBlocksContained,
    `${context}: installation commands must stay inside their cards`
  );
  if (site.isHome) {
    assert.ok(layout.installerContained, `${context}: the installer must stay inside its frame`);
    assert.equal(
      layout.visibleInstallPanels,
      1,
      `${context}: exactly one install panel must be visible`
    );
  }
};

const assertSelectedInstallTab = async (page, expectedIndex, checkFocus = false) => {
  const state = await page.evaluate(() => {
    const tabs = [...document.querySelectorAll('.installer [role="tab"]')];
    return {
      selected: tabs.map((tab) => tab.getAttribute("aria-selected") === "true"),
      tabStops: tabs.map((tab) => tab.tabIndex),
      visible: tabs
        .map((tab) => document.getElementById(tab.getAttribute("aria-controls")))
        .filter((panel) => panel && !panel.hidden)
        .map((panel) => panel.id),
      controls: tabs.map((tab) => tab.getAttribute("aria-controls")),
      relationships: tabs.map((tab) => {
        const panel = document.getElementById(tab.getAttribute("aria-controls"));
        return Boolean(
          panel?.getAttribute("role") === "tabpanel" &&
            panel.getAttribute("aria-labelledby") === tab.id
        );
      }),
      focusedIndex: tabs.indexOf(document.activeElement),
    };
  });
  assert.ok(state.relationships.every(Boolean), "tabs must label their controlled panels");
  assert.deepEqual(
    state.selected,
    state.selected.map((_, index) => index === expectedIndex),
    "selection must follow the activated tab"
  );
  assert.deepEqual(
    state.tabStops,
    state.tabStops.map((_, index) => index === expectedIndex ? 0 : -1),
    "only the selected tab belongs in the tab order"
  );
  assert.deepEqual(state.visible, [state.controls[expectedIndex]]);
  if (checkFocus) assert.equal(state.focusedIndex, expectedIndex);
};

const testInstallTabs = async (page, site, width, colorScheme) => {
  const tabs = page.locator('.installer [role="tab"]');
  const tabCount = await tabs.count();
  assert.ok(tabCount > 1);
  for (let index = 0; index < tabCount; index += 1) {
    await tabs.nth(index).click();
    await assertSelectedInstallTab(page, index);
    await assertLayout(page, site, width, colorScheme);
  }

  for (const [key, step] of [
    ["ArrowRight", 1], ["ArrowDown", 1],
    ["ArrowLeft", -1], ["ArrowUp", -1],
  ]) {
    await tabs.first().click();
    let selected = 0;
    for (let count = 0; count < tabCount; count += 1) {
      await page.keyboard.press(key);
      selected = (selected + step + tabCount) % tabCount;
      await assertSelectedInstallTab(page, selected, true);
    }
  }
  await page.keyboard.press("End");
  await assertSelectedInstallTab(page, tabCount - 1, true);
  await page.keyboard.press("Home");
  await assertSelectedInstallTab(page, 0, true);
};

try {
  for (const site of pages) {
    for (const colorScheme of colorSchemes) {
      for (const width of viewports) {
        const context = await browser.newContext({
          colorScheme,
          reducedMotion: "reduce",
          viewport: { width, height: 700 },
        });
        const page = await context.newPage();
        const pageErrors = [];
        page.on("pageerror", (error) => pageErrors.push(error.message));
        await page.goto(site.url, { waitUntil: "load" });
        await page.evaluate(() => document.fonts.ready);
        assert.ok(
          await page.evaluate(() => [...document.fonts].some(
            (font) => font.family === "Sebastian Slab" && font.status === "loaded"
          )),
          `${site.name}: the heading webfont must load before checking layout`
        );
        await assertLayout(page, site, width, colorScheme);

        if (site.isHome) {
          const optionalInstructions = page.locator("details").filter({
            has: page.locator("#optional-instructions-command"),
          });
          assert.equal(await optionalInstructions.count(), 1);
          assert.equal(await optionalInstructions.getAttribute("open"), null);
          await optionalInstructions.locator("summary").click();
          assert.notEqual(await optionalInstructions.getAttribute("open"), null);
          await assertLayout(page, site, width, colorScheme);
          if (width === viewports[0] || width === viewports.at(-1)) {
            await testInstallTabs(page, site, width, colorScheme);
          }
        }

        assert.deepEqual(pageErrors, [], `${site.name} must not raise JavaScript errors`);
        await context.close();
      }
    }
  }

  // Exercise the visitor journey, including the shared copy enhancement.
  const context = await browser.newContext({ reducedMotion: "reduce" });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, "clipboard", {
      value: { writeText: async (text) => { window.copiedCommand = text; } },
    });
  });
  const page = await context.newPage();
  for (const site of pages.filter((site) => site.skill)) {
    await page.goto(pageUrl("index.html"));
    await page.locator(`[data-skill="${site.skill}"] a`).click();
    assert.equal(page.url(), site.url, "skill cards must open the website detail page");
    await page.locator('.skill-toc a[href="#install"]').click();
    await page.locator('[data-copy-target="skill-command"]').click();
    await page.waitForFunction(() => Boolean(window.copiedCommand));
    assert.equal(await page.evaluate(() => window.copiedCommand),
      `npx skills add sebastian-software/effective-agent --skill ${site.skill}`);
    await page.locator(".breadcrumbs a").click();
    assert.equal(page.url(), `${pageUrl("index.html")}#library`);
  }
  await context.close();

  // Skill explanations, native anchor navigation, and install commands work without JS.
  const staticContext = await browser.newContext({ javaScriptEnabled: false });
  const staticPage = await staticContext.newPage();
  for (const site of pages.filter((site) => site.skill)) {
    await staticPage.goto(site.url);
    assert.equal(await staticPage.locator("h1").count(), 1);
    const expectedPromptCount = ["effective-image", "effective-video"].includes(site.skill) ? 4 : 3;
    assert.equal(await staticPage.locator(".skill-prompts li").count(), expectedPromptCount,
      `${site.name}: example prompts must match the published skill coverage`);
    await staticPage.locator('.skill-toc a[href="#install"]').click();
    assert.equal(staticPage.url(), `${site.url}#install`);
    assert.ok(await staticPage.locator("#skill-command").isVisible());
  }
  await staticContext.close();
} finally {
  await browser.close();
}
