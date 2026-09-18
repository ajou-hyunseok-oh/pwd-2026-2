const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 960 } });
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    const base = process.env.CALCULATOR_URL || 'http://127.0.0.1:4305';
    await page.goto(base);
    await page.click('#calculate');
    assert.match(await page.locator('#status').innerText(), /TODO 1/);
    assert.equal(await page.locator('#history li').count(), 0);
    await page.goto(base + '/demo');
    await page.click('#calculate');
    assert.equal(await page.locator('#result').innerText(), '15');
    await page.click('[data-operation="divide"]');
    assert.equal(await page.locator('#result').innerText(), '—');
    await page.fill('#y', '0');
    await page.click('#calculate');
    assert.equal(await page.locator('#status').getAttribute('data-state'), 'error');
    assert.equal(await page.locator('#history li').count(), 1);
    await page.fill('#y', '3');
    await page.press('#y', 'Enter');
    assert.equal(await page.locator('#result').innerText(), '4');
    await page.click('[data-operation="sqrt"]');
    assert.equal(await page.locator('#y').isDisabled(), true);
    assert.equal(await page.locator('#y-field').isVisible(), false);
    await page.fill('#x', '-1');
    await page.click('#calculate');
    assert.equal(await page.locator('#status').getAttribute('data-state'), 'error');
    await page.fill('#x', '9');
    await page.click('#calculate');
    assert.equal(await page.locator('#result').innerText(), '3');
    assert.equal(await page.locator('#expression').innerText(), '√(9)');
    await page.click('[data-operation="sin"]');
    assert.equal(await page.locator('#unit').isDisabled(), false);
    await page.fill('#x', '30');
    await page.click('#calculate');
    assert.equal(await page.locator('#result').innerText(), '0.5');
    await page.selectOption('#unit', 'rad');
    assert.equal(await page.locator('#result').innerText(), '—');
    await page.fill('#x', String(Math.PI / 2));
    await page.click('#calculate');
    assert.equal(await page.locator('#result').innerText(), '1');
    await page.click('[data-operation="add"]');
    assert.equal(await page.locator('#y').isDisabled(), false);
    assert.equal(await page.locator('#unit').isDisabled(), true);
    await page.fill('#x', '0.1');
    await page.fill('#y', '0.2');
    await page.click('#calculate');
    assert.equal(await page.locator('#result').innerText(), '0.3');
    assert.equal(await page.locator('#history li').count(), 5);
    assert.match(await page.locator('#history li').first().innerText(), /0.1 \+ 0.2/);
    await page.fill('#x', '1e308');
    await page.fill('#y', '1e308');
    await page.click('#calculate');
    assert.equal(await page.locator('#status').getAttribute('data-state'), 'error');
    assert.equal(await page.locator('#history li').count(), 5);
    await page.click('#clear');
    assert.equal(await page.locator('#x').inputValue(), '');
    assert.equal(await page.locator('#y').inputValue(), '');
    assert.equal(await page.locator('#result').innerText(), '—');
    assert.equal(await page.locator('#history li').count(), 5);
    await page.click('#clear-history');
    assert.equal(await page.locator('#history li').count(), 0);
    assert.equal(await page.locator('#clear-history').isDisabled(), true);
    await page.fill('#x', '12');
    await page.fill('#y', '3');
    await page.click('#calculate');
    const directory = path.join(os.tmpdir(), 'week3-calculator-review');
    fs.mkdirSync(directory, { recursive: true });
    await page.screenshot({
      path: path.join(directory, 'desktop.png'),
      fullPage: true,
    });
    await page.setViewportSize({ width: 375, height: 812 });
    assert.equal(
      await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
      true,
    );
    await page.screenshot({ path: path.join(directory, 'mobile.png'), fullPage: true });
    await page.reload();
    assert.equal(await page.locator('#history li').count(), 0);
    assert.deepEqual(errors, []);
    console.log(
      'PASS starter TODO, demo calculations, error recovery, arity, DEG/RAD, history, Enter, clear, reload, mobile bounds; ' +
        directory,
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
