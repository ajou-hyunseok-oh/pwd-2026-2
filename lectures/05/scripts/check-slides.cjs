// Usage: PLAYWRIGHT_PATH=/absolute/path/to/playwright node lectures/05/scripts/check-slides.cjs
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const root = path.resolve(__dirname, '..');
const count = JSON.parse(fs.readFileSync(path.join(root, 'materials/slide-map.json'))).length;
const output = process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-week5-deck/review');
fs.mkdirSync(output, {recursive: true});

(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  const page = await browser.newPage({viewport: {width: 1312, height: 818}});
  const errors = [], issues = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if (r.status() >= 400) errors.push(r.status() + ' ' + r.url()); });
  try {
    await page.goto((process.env.DECK_URL || 'http://127.0.0.1:4305') + '/lectures/05/');
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('[data-wd-slide]').count(), count);
    for (const locale of ['ko', 'en']) {
      await page.emulateMedia({media: 'screen'});
      await page.setViewportSize({width: 1312, height: 818});
      await page.click('[data-locale="' + locale + '"]');
      for (const mode of ['screen', 'print']) {
        await page.emulateMedia({media: mode});
        for (let i = 0; i < count; i++) {
          await page.evaluate(i => document.querySelector('[data-web-deck]').__webDeck.goTo(i), i);
          const found = await page.locator('[data-wd-slide]').nth(i).evaluate(s => {
            const result = [], box = s.getBoundingClientRect();
            const footer = s.querySelector('.w5-references,.wd-slide-footer')?.getBoundingClientRect();
            const limit = footer ? footer.top - 8 : box.bottom - 30;
            for (const e of s.querySelectorAll('h1,h2,dt,dd,li,p,pre,table,img,figcaption')) {
              if (e.closest('[hidden],.wd-slide-footer')) continue;
              const r = e.getBoundingClientRect();
              if (r.bottom > limit || r.left < box.left - 1 || r.right > box.right + 1 || e.scrollWidth > e.clientWidth + 2)
                result.push({type: 'bounds', tag: e.tagName, text: e.textContent.slice(0,80), bottom: r.bottom-box.top, limit: limit-box.top, sw: e.scrollWidth, cw: e.clientWidth});
              if (e.tagName === 'H2' && r.height > parseFloat(getComputedStyle(e).lineHeight) * 1.5)
                result.push({type: 'title-wrap', text: e.textContent});
            }
            const blocks = [...s.querySelectorAll('.w5-block')].map(e => e.getBoundingClientRect());
            if (blocks.length === 2 && Math.abs(blocks[0].top - blocks[1].top) < 1 && blocks[0].right > blocks[1].left + 1)
              result.push({type: 'column-overlap'});
            return result;
          });
          issues.push(...found.map(x => ({locale, mode, slide: i + 1, ...x})));
          if (mode === 'screen')
            await page.locator('[data-wd-slide]').nth(i).screenshot({path: path.join(output, locale + '-' + String(i + 1).padStart(2,'0') + '.png')});
        }
        if (mode === 'print')
          await page.pdf({path: path.join(output, locale + '.pdf'), preferCSSPageSize: true, printBackground: true});
      }
      await page.emulateMedia({media:'screen'});
      await page.setViewportSize({width:390,height:844});
      for (let i = 0; i < count; i++) {
        const mobile = await page.evaluate(i => {
          document.querySelector('[data-web-deck]').__webDeck.goTo(i);
          const s = document.querySelectorAll('[data-wd-slide]')[i];
          const body = s.querySelector('.w5-body'), refs = s.querySelector('.w5-references');
          return {
            overflow: document.documentElement.scrollWidth > innerWidth,
            overlap: body && refs && body.getBoundingClientRect().top + body.scrollHeight > refs.getBoundingClientRect().top + 1
          };
        }, i);
        if (mobile.overflow || mobile.overlap) issues.push({locale, mode:'mobile', slide:i+1, ...mobile});
      }
      await page.evaluate(() => document.querySelector('[data-web-deck]').__webDeck.goTo(16));
      await page.screenshot({path:path.join(output,locale+'-mobile.png')});
    }
    fs.writeFileSync(path.join(output,'audit.json'),JSON.stringify({count,errors,issues},null,2));
    console.log(JSON.stringify({count,errors,issues,output},null,2));
    process.exitCode = errors.length || issues.length ? 1 : 0;
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
