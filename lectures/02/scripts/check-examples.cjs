const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'C:/Users/hsoh/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const root = path.resolve(__dirname, '../examples');
const base = process.env.EXAMPLE_URL || 'http://localhost:4183';
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  try {
    for (const locale of ['ko', 'en']) {
      const sub = locale === 'en' ? 'en/' : '';
      const before = locale === 'ko' ? '웹 개발 학습 중' : 'Learning web development.';
      const after = locale === 'ko' ? '나의 첫 웹사이트 제작 중' : 'Building my first website.';
      for (const file of ['index', 'about', 'projects']) {
        await page.goto(`${base}/portfolio/${sub}${file}.html`);
        for (const href of await page.locator('nav a').evaluateAll(links => links.map(a => a.href))) assert.equal((await page.request.get(href)).status(), 200);
      }
      for (const key of ['Enter', 'Space']) {
        await page.goto(`${base}/portfolio/${sub}about.html`);
        assert.equal(await page.locator('#intro').textContent(), before);
        for (let n = 0; n < 4; n++) await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(() => document.activeElement.id), 'change');
        await page.keyboard.press(key);
        assert.equal(await page.locator('#intro').textContent(), after);
      }
      await page.goto(`${base}/portfolio/${sub}projects.html`);
      assert.equal(await page.locator('#updates p').count(), 0);
      await page.locator('#add').click();
      assert.equal(await page.locator('#updates p').count(), 1);
      await page.goto(`${base}/rendering/${sub}index.html`);
      const dimensions = () => page.locator('.profile').evaluate(el => ({ width: el.getBoundingClientRect().width, height: el.getBoundingClientRect().height, paragraph: el.querySelector('p').getBoundingClientRect().height }));
      const initial = await dimensions();
      await page.locator('#width').click();
      const narrow = await dimensions();
      assert.equal(initial.width, 360);
      assert.equal(narrow.width, 220);
      assert.ok(narrow.paragraph > initial.paragraph);
      await page.locator('#color').click();
      assert.deepEqual(await dimensions(), narrow);
      assert.equal(await page.locator('.profile').evaluate(el => getComputedStyle(el).backgroundColor), 'rgb(220, 234, 245)');
      await page.locator('#hide').click();
      assert.equal(await page.locator('#intro').count(), 1);
      assert.equal(await page.locator('#intro').isVisible(), false);
      await page.goto(`${base}/rendering/${sub}cascade.html`);
      assert.equal(await page.locator('#intro').evaluate(el => getComputedStyle(el).color), 'rgb(154, 53, 31)');
      for (const reserved of [false, true]) {
        await page.goto(`${base}/rendering/${sub}image-${reserved ? 'reserved' : 'unreserved'}.html`);
        const y = (await page.locator('.measure p').boundingBox()).y;
        await page.locator('#load').click();
        await page.waitForFunction(() => document.querySelector('#hero').naturalWidth > 0);
        const delta = (await page.locator('.measure p').boundingBox()).y - y;
        if (reserved) assert.equal(delta, 0); else assert.ok(delta > 100);
      }
      for (const mode of ['csr', 'ssr', 'ssg']) {
        const response = await page.goto(`${base}/generation/${sub}${mode}.html`);
        assert.equal(response.status(), 200);
        const html = await response.text();
        assert.equal((html.match(/<p id="intro">([^<]*)<\/p>/) || [])[1], mode === 'csr' ? '' : before);
        assert.equal(await page.locator('#intro').textContent(), before);
      }
      const requests = [];
      const record = request => { if (request.resourceType() === 'document') requests.push(request.url()); };
      page.on('request', record);
      await page.goto(`${base}/portfolio/${sub}index.html`);
      requests.length = 0;
      await page.locator('nav a').nth(1).click();
      assert.equal(requests.length, 1);
      await page.goto(`${base}/routing/${sub}index.html`);
      const header = await page.locator('header').innerHTML();
      requests.length = 0;
      await page.locator('nav a').nth(1).click();
      assert.equal(requests.length, 0);
      assert.equal(await page.locator('#page').textContent(), before);
      assert.equal(await page.locator('header').innerHTML(), header);
      await page.goBack();
      assert.ok(!page.url().includes('page=about'));
      await page.goForward();
      assert.equal(await page.locator('#page').textContent(), before);
      await page.reload();
      assert.equal(await page.locator('#page').textContent(), before);
      page.off('request', record);
    }
    await page.goto(base + '/components/dist/index.html');
    assert.deepEqual(await page.locator('.card h2').allTextContents(), ['Timetable', 'Memo']);
    await page.goto(base + '/source.html?file=portfolio/about.html');
    assert.equal(await page.locator('#source').textContent(), fs.readFileSync(path.join(root, 'portfolio/about.html'), 'utf8'));
    assert.equal(execFileSync(process.execPath, [path.join(root, 'portfolio/demo.js')], { encoding: 'utf8' }).trim(), '2');
    const staticSSG = fs.readFileSync(path.join(root, 'generation/ssg.html'), 'utf8');
    assert.ok(staticSSG.includes('웹 개발 학습 중'));
    assert.deepEqual(errors, []);
    console.log('Passed: bilingual navigation, DOM changes, keyboard, layout, image reservation, CSR/SSR/SSG, SPA history/refresh, React build, source viewer and Node output.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
