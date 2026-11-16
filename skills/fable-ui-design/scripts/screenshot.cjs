#!/usr/bin/env node
/*
 * Capture a page at phone, tablet and desktop widths in light and dark color
 * schemes, and report problems that are easy to miss by eye: horizontal
 * overflow and console errors.
 *
 *   node screenshot.cjs <url-or-html-file> [out-dir]
 *        [--widths 390,768,1440] [--schemes light,dark] [--wait 300]
 *
 * Needs Playwright (`playwright`, `playwright-core` or `@playwright/test`) to be
 * resolvable. Set CHROMIUM_PATH to use a specific browser binary.
 *
 * Exit status: 0 when every capture succeeded (problems found are reported, not
 * fatal), 1 when a capture failed, 2 on bad usage or missing Playwright.
 */
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

function usage(message) {
  if (message) console.error(`error: ${message}`);
  console.error('usage: node screenshot.cjs <url-or-html-file> [out-dir] [--widths 390,768,1440] [--schemes light,dark] [--wait 300]');
  process.exit(2);
}

function parseArgs(argv) {
  const options = { widths: [390, 768, 1440], schemes: ['light', 'dark'], wait: 300 };
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--widths') options.widths = String(argv[++i] || '').split(',').map(Number);
    else if (arg === '--schemes') options.schemes = String(argv[++i] || '').split(',');
    else if (arg === '--wait') options.wait = Number(argv[++i]);
    else if (arg.startsWith('--')) usage(`unknown option ${arg}`);
    else positional.push(arg);
  }
  if (positional.length < 1 || positional.length > 2) usage();
  if (options.widths.some((w) => !Number.isInteger(w) || w < 200)) usage('--widths takes whole numbers of 200 or more');
  if (options.schemes.some((s) => s !== 'light' && s !== 'dark')) usage('--schemes takes light and/or dark');
  if (!Number.isFinite(options.wait) || options.wait < 0) usage('--wait takes milliseconds');
  options.target = positional[0];
  options.outDir = positional[1] || 'ui-shots';
  return options;
}

function loadChromium() {
  for (const name of ['playwright', 'playwright-core', '@playwright/test']) {
    try {
      const mod = require(name);
      if (mod.chromium) return mod.chromium;
    } catch (error) {
      if (error.code !== 'MODULE_NOT_FOUND') throw error;
    }
  }
  console.error('error: Playwright is not installed here. Install it (npm i -D playwright && npx playwright install chromium) or use another browser tool.');
  process.exit(2);
}

function toUrl(target) {
  if (/^(https?|file):/i.test(target)) return target;
  const file = path.resolve(target);
  if (!fs.existsSync(file)) usage(`no such file: ${target}`);
  return pathToFileURL(file).href;
}

function viewportFor(width) {
  if (width < 600) return { name: 'phone', height: 844 };
  if (width < 1000) return { name: 'tablet', height: 1024 };
  return { name: 'desktop', height: 900 };
}

// Runs in the page, after the screenshot: how far content spills past the viewport,
// and which element causes it. Wide elements stretch their siblings and ancestors
// too, so position alone can't name the cause: hide each candidate in turn,
// deepest first, and see whose absence removes the most overflow.
function measureOverflow() {
  const root = document.documentElement;
  const excessNow = () => Math.max(root.scrollWidth - root.clientWidth, 0);
  const excess = excessNow();
  if (excess <= 1) return null;
  const depthOf = (el) => { let d = 0; for (let n = el; n.parentElement; n = n.parentElement) d += 1; return d; };
  const candidates = [...document.body.querySelectorAll('*')]
    .filter((el) => el.getBoundingClientRect().right > root.clientWidth + 1)
    .map((el) => ({ el, depth: depthOf(el) }))
    .sort((a, b) => b.depth - a.depth)
    .slice(0, 300);
  let best = null;
  for (const { el } of candidates) {
    const value = el.style.getPropertyValue('display');
    const priority = el.style.getPropertyPriority('display');
    el.style.setProperty('display', 'none', 'important');
    const remaining = excessNow();
    el.style.setProperty('display', value, priority);
    if (!best || remaining < best.remaining) best = { el, remaining };
    if (remaining <= 1) break;
  }
  let culprit = '';
  if (best && best.remaining < excess) {
    const el = best.el;
    const cls = typeof el.className === 'string' && el.className.trim() ? `.${el.className.trim().split(/\s+/)[0]}` : '';
    culprit = `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${cls}`;
  }
  return { excess, culprit };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const chromium = loadChromium();
  const url = toUrl(options.target);
  fs.mkdirSync(options.outDir, { recursive: true });

  const launchOptions = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const browser = await chromium.launch(launchOptions);
  let failed = false;
  try {
    for (const width of options.widths) {
      const { name, height } = viewportFor(width);
      for (const scheme of options.schemes) {
        const file = path.join(options.outDir, `${name}-${width}-${scheme}.png`);
        const context = await browser.newContext({ viewport: { width, height }, colorScheme: scheme, deviceScaleFactor: 1 });
        const page = await context.newPage();
        const errors = [];
        page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
        page.on('pageerror', (error) => errors.push(error.message));
        try {
          await page.goto(url, { waitUntil: 'load', timeout: 30000 });
          await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
          await page.waitForTimeout(options.wait);
          await page.screenshot({ path: file, fullPage: true });
          const overflow = await page.evaluate(measureOverflow);
          const notes = [];
          if (overflow) notes.push(`overflow: page is ${overflow.excess}px wider than the viewport${overflow.culprit ? ` (caused by: ${overflow.culprit})` : ''}`);
          if (errors.length) notes.push(`${errors.length} console error(s): ${errors[0].slice(0, 160)}`);
          console.log(`${file}  ${notes.length ? notes.join('; ') : 'ok'}`);
        } catch (error) {
          failed = true;
          console.log(`${file}  CAPTURE FAILED: ${error.message.split('\n')[0]}`);
        } finally {
          await context.close();
        }
      }
    }
  } finally {
    await browser.close();
  }
  process.exit(failed ? 1 : 0);
}

main().catch((error) => {
  console.error(`error: ${error.message}`);
  process.exit(1);
});
