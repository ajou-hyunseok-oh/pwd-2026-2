// Usage: LECTURE=05 PLAYWRIGHT_PATH=/path/to/playwright node packages/web-deck/tests/authoring-layout.cjs
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const lecture = process.env.LECTURE || '05';
if (!/^(0[5-9]|1[0-3])$/.test(lecture)) throw new Error('LECTURE must be 05–13');
const deckPath = 'lectures/' + lecture + '/index.html';
const root = path.resolve(__dirname, '../../../lectures/' + lecture);
const count = (fs.readFileSync(path.join(root, 'index.html'), 'utf8').match(/data-wd-slide=/g) || []).length;
const output = process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-lecture-' + path.basename(root) + '/review');
fs.mkdirSync(output, {recursive: true});

(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  const page = await browser.newPage({viewport: {width: 1312, height: 818}});
  const errors = [], issues = [], translations = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if (r.status() >= 400) errors.push(r.status() + ' ' + r.url()); });
  try {
    await page.goto((process.env.DECK_URL || 'http://127.0.0.1:4305').replace(/\/$/, '') + '/' + deckPath);
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('[data-wd-slide]').count(), count);
    for (const locale of ['ko', 'en']) {
      await page.emulateMedia({media: 'screen'});
      await page.setViewportSize({width: 1312, height: 818});
      await page.click('[data-locale="' + locale + '"]');
      const translation = await page.evaluate(locale => {
        const dictionary = window.WEB_DECK_CONFIG.messages[locale];
        const mismatches = [];
        let checked = 0;
        for (const [binding, attribute] of [
          ['data-wd-i18n', null], ['data-wd-i18n-alt', 'alt'],
          ['data-wd-i18n-aria-label', 'aria-label'], ['data-wd-i18n-title', 'title']
        ]) {
          for (const node of document.querySelectorAll(`[${binding}]`)) {
            const key = node.getAttribute(binding), expected = dictionary[key];
            const actual = attribute ? node.getAttribute(attribute) : node.textContent;
            checked++;
            if (typeof expected !== 'string' || actual !== expected)
              mismatches.push({key, binding, actual, expected: expected ?? null});
          }
        }
        return {checked, mismatches};
      }, locale);
      translations.push({locale, checked:translation.checked, mismatches:translation.mismatches.length});
      issues.push(...translation.mismatches.map(issue => ({locale, type:'translation', ...issue})));
      for (const mode of ['screen', 'print']) {
        await page.emulateMedia({media: mode});
        for (let i = 0; i < count; i++) {
          await page.evaluate(i => document.querySelector('[data-web-deck]').__webDeck.goTo(i), i);
          const found = await page.locator('[data-wd-slide]').nth(i).evaluate(s => {
            const result = [], box = s.getBoundingClientRect();
            const limit = box.bottom - 30;
            for (const e of s.querySelectorAll('h1,h2,dt,dd,li,p,pre,table,img,figcaption')) {
              if (e.closest('[hidden],.wd-slide-footer')) continue;
              const r = e.getBoundingClientRect();
              // Flow arrows in ::after contribute to scrollWidth; measure real content too.
              const range = document.createRange();
              range.selectNodeContents(e);
              const content = range.getBoundingClientRect();
              const contentOverflow = e.scrollWidth > e.clientWidth + 2 &&
                (content.left < r.left - 2 || content.right > r.right + 2);
              if (r.bottom > limit || r.left < box.left - 1 || r.right > box.right + 1 || contentOverflow)
                result.push({type: 'bounds', tag: e.tagName, text: e.textContent.slice(0,80), bottom: r.bottom-box.top, limit: limit-box.top, sw: e.scrollWidth, cw: e.clientWidth});
              if (e.tagName === 'PRE') {
                const style = getComputedStyle(e), rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
                if (Math.abs(parseFloat(style.fontSize) / rem - .7) > .01 || style.whiteSpace !== 'pre')
                  result.push({type: 'code-legibility', fontSize: style.fontSize, whiteSpace: style.whiteSpace});
              }
            }
            const blocks = [...s.querySelectorAll('.wd-lesson-block')].map(e => e.getBoundingClientRect());
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
          const blocks = [...s.querySelectorAll('.wd-lesson-body > *')];
          const rects = blocks.map(e => e.getBoundingClientRect());
          return {
            overflow: document.documentElement.scrollWidth > innerWidth,
            overlap: rects.some((r, index) => index > 0 && r.top < rects[index - 1].bottom - 1),
            clippedCode: [...s.querySelectorAll('pre')].some(e => e.clientHeight + 2 < e.scrollHeight || parseFloat(getComputedStyle(e).fontSize) < 14)
          };
        }, i);
        if (mobile.overflow || mobile.overlap || mobile.clippedCode) issues.push({locale, mode:'mobile', slide:i+1, ...mobile});
      }
      await page.evaluate(() => document.querySelector('[data-web-deck]').__webDeck.goTo(Math.min(16, document.querySelectorAll('[data-wd-slide]').length - 1)));
      await page.screenshot({path:path.join(output,locale+'-mobile.png')});
    }
    fs.writeFileSync(path.join(output,'audit.json'),JSON.stringify({count,translations,errors,issues},null,2));
    console.log(JSON.stringify({count,translations,errors,issues,output},null,2));
    process.exitCode = errors.length || issues.length ? 1 : 0;
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
