const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'C:/Users/hsoh/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const output = path.join(os.tmpdir(), 'week3-slide-review');
fs.mkdirSync(output, { recursive: true });
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const issues = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error' && message.text().includes('[WebDeck]')) errors.push(message.text()); });
    await page.goto((process.env.DECK_URL || 'http://127.0.0.1:4304') + '/lectures/03/');
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('[data-wd-slide]').count(), 61);
    for (const locale of ['ko', 'en']) {
      await page.click(`[data-locale="${locale}"]`);
      for (const mode of ['screen', 'print']) {
        await page.emulateMedia({ media: mode });
        const result = await page.evaluate(() => {
          const issues = [];
          const slides = [...document.querySelectorAll('[data-wd-slide]')];
          const deck = document.querySelector('[data-web-deck]').__webDeck;
          for (const [index, slide] of slides.entries()) {
            deck.goTo(index);
            const box = slide.getBoundingClientRect();
            const body = slide.querySelector('.week3-body');
            for (const el of slide.querySelectorAll('h1,h2,h3,p,li,pre,samp,table,footer')) {
              const r = el.getBoundingClientRect();
              if (r.bottom > box.bottom + 1 || r.right > box.right + 1 || r.left < box.left - 1 || el.scrollWidth > el.clientWidth + 1) {
                issues.push({ slide: index + 1, id: slide.dataset.wdSlide, type: 'bounds', tag: el.tagName, text: el.textContent.slice(0, 100), height: r.height });
              }
            }
            if (body) {
              for (const panel of body.children) {
                if (panel.getBoundingClientRect().bottom > body.getBoundingClientRect().bottom + 1) {
                  issues.push({ slide: index + 1, id: slide.dataset.wdSlide, type: 'body-overlap', extra: Math.round(panel.getBoundingClientRect().bottom - body.getBoundingClientRect().bottom) });
                }
              }
            }
          }
          return issues;
        });
        issues.push(...result.map(issue => ({ locale, mode, ...issue })));
      }
      await page.emulateMedia({ media: 'screen' });
      for (const topic of ['topic-07', 'topic-22', 'topic-34', 'topic-45', 'topic-50']) {
        await page.evaluate(topic => {
          const slides = [...document.querySelectorAll('[data-wd-slide]')];
          document.querySelector('[data-web-deck]').__webDeck.goTo(slides.findIndex(s => s.dataset.wdSlide === topic));
        }, topic);
        await page.locator('[data-wd-slide].is-active').screenshot({ path: path.join(output, `${locale}-${topic}.png`) });
      }
    }
    await page.emulateMedia({ media: 'print' });
    const codeStyle = await page.locator('pre.wd-code').first().evaluate(el => {
      const s = getComputedStyle(el); return { font: s.fontFamily, size: s.fontSize, color: s.color, background: s.backgroundColor };
    });
    assert.ok(codeStyle.font.startsWith('Consolas'));
    assert.equal(codeStyle.size, '14px');
    assert.equal(codeStyle.color, 'rgb(0, 255, 0)');
    assert.equal(codeStyle.background, 'rgb(0, 0, 0)');
    await page.emulateMedia({ media: 'screen' });
    await page.setViewportSize({ width: 375, height: 812 });
    for (const locale of ['ko', 'en']) {
      await page.click(`[data-locale="${locale}"]`);
      for (let index = 0; index < 61; index++) {
        const ok = await page.evaluate(index => {
          document.querySelector('[data-web-deck]').__webDeck.goTo(index);
          return document.documentElement.scrollWidth <= innerWidth;
        }, index);
        if (!ok) issues.push({ locale, mode: 'mobile', slide: index + 1, type: 'page-overflow' });
      }
    }
    assert.deepEqual(errors, []);
    fs.writeFileSync(path.join(output, 'audit.json'), JSON.stringify({ codeStyle, issues }, null, 2));
    console.log(JSON.stringify({ issues, codeStyle, output }, null, 2));
    process.exitCode = issues.length ? 1 : 0;
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
