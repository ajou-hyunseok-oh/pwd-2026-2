const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1312, height: 818}});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto((process.env.DECK_URL || 'http://127.0.0.1:4304') + '/lectures/04/index.html?lang=ko');
    const go = n => page.evaluate(n => document.querySelector('[data-web-deck]').__webDeck.goTo(n - 1), n);
    await go(9);
    const components = page.locator('[data-react-demo="components"]');
    await components.getByRole('button').click();
    assert.equal(await components.getByRole('button').getAttribute('aria-pressed'), 'true');
    assert.equal(await components.locator('[data-product]').count(), 6);
    await go(11);
    const apps = page.locator('[data-react-demo="filter"] .react-product-app');
    const after = apps.nth(1);
    assert.equal(await apps.nth(0).locator('[data-product]').count(), 6);
    assert.equal(await after.locator('[data-product]').count(), 4);
    const search = after.getByRole('searchbox');
    await search.fill('사과');
    await after.getByText('검색 결과 1개', {exact:true}).waitFor();
    assert.equal(await after.locator('[data-product]').count(), 1);
    await search.fill('패션');
    await after.getByText('조건에 맞는 상품 없음', {exact:true}).waitFor();
    await after.getByRole('checkbox').uncheck();
    await after.getByText('검색 결과 1개', {exact:true}).waitFor();
    assert.equal(await after.locator('[data-product="passionfruit"]').count(), 1);
    await search.fill('');
    await after.getByText('검색 결과 6개', {exact:true}).waitFor();
    const apple = await after.locator('[data-product="apple"]').elementHandle();
    await after.getByRole('checkbox').check();
    await after.getByText('검색 결과 4개', {exact:true}).waitFor();
    assert.equal(await apple.evaluate(el => el.isConnected), true, 'Retained product row keeps its DOM node');
    await page.getByRole('button', {name:'EN', exact:true}).click();
    await after.getByText('4 results', {exact:true}).waitFor();
    await search.fill('Apple');
    await after.getByText('1 result', {exact:true}).waitFor();
    assert.equal(await after.locator('[data-product="apple"]').count(), 1);
    await go(18);
    const clock = page.locator('[data-react-demo="clock"]');
    const input = clock.getByRole('textbox');
    await input.fill('Keep this input');
    const inputNode = await input.elementHandle();
    await input.evaluate(el => el.setSelectionRange(4,4));
    const before = await clock.locator('time').textContent();
    await page.waitForFunction(before => document.querySelector('[data-react-demo="clock"] time').textContent !== before, before);
    assert.equal(await input.inputValue(), 'Keep this input');
    assert.equal(await inputNode.evaluate(el => el === document.querySelector('[data-react-demo="clock"] input')), true);
    assert.equal(await input.evaluate(el => document.activeElement === el && el.selectionStart === 4), true);
    await input.press('ArrowLeft');
    assert.equal(await input.evaluate(el => el.selectionStart), 3);
    assert.equal(await page.locator('[data-wd-slide].is-active').getAttribute('data-wd-slide'), 'slide-18');
    await go(24);
    assert.equal(await page.locator('.react-hello-results img').evaluateAll(images => images.every(im => im.complete && im.naturalWidth > 0)), true);
    for (const [slide, mode] of [[13, 'programming'], [19, 'dom-updates']]) {
      await go(slide);
      const demo = page.locator(`[data-react-demo="${mode}"]`);
      for (const engine of ['jquery', 'react']) {
        const container = demo.locator(`[data-counter-engine="${engine}"]`);
        const button = container.getByRole('button');
        const node = await button.elementHandle();
        assert.equal(await button.textContent(), 'Clicked 0 times');
        for (let count = 1; count <= 3; count++) {
          await button.click();
          await container.getByRole('button', {name: `Clicked ${count} times`, exact:true}).waitFor();
        }
        assert.equal(await node.evaluate(el => el.isConnected), true, `${engine}: original button retained`);
        if (mode === 'dom-updates') {
          await container.locator('[data-retained="true"]').waitFor();
          assert.match(await container.locator('.react-counter-observation').textContent(), /Same button retained/);
        }
        await button.focus();
        await button.press('Space');
        await container.getByRole('button', {name: 'Clicked 4 times', exact:true}).waitFor();
        assert.equal(await page.locator('[data-wd-slide].is-active').getAttribute('data-wd-slide'), `slide-${slide}`);
      }
    }
    await page.getByRole('button', {name:'KO', exact:true}).click();
    await page.locator('[data-react-demo="dom-updates"] .react-counter-observation').first().filter({hasText:'기존 버튼 유지'}).waitFor();
    await go(17);
    assert.equal(await page.locator('[data-ui-snapshot="before"] .is-removed').count(), 2);
    assert.equal(await page.locator('[data-ui-snapshot="after"] .react-snapshot-row').count(), 4);
    assert.equal(await page.locator('.react-committed-output [data-product]').count(), 4);
    const copiedCode = await page.locator('[data-wd-slide="slide-13"] pre').allTextContents();
    assert.ok(copiedCode[0].includes("button.text(`Clicked ${count} times`)"));
    assert.ok(copiedCode[1].includes('setCount(count + 1)'));
    assert.deepEqual(errors, []);
    console.log('React demos: component boundaries, filters, empty results, derived counts, EN translation, retained DOM/input/focus/caret, deck keyboard isolation, output images, both counter implementations, DOM observations, keyboard clicks, and UI differences passed.');
  } finally { await browser.close(); }
})().catch(e => {console.error(e); process.exitCode=1});
