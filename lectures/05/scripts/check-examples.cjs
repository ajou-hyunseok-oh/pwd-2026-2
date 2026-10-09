// Execute slide code directly in a temporary React app (no example duplication).
// PLAYWRIGHT_PATH=/path/to/playwright node lectures/05/scripts/check-examples.cjs
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const root = path.resolve(__dirname, '..');
const modules = process.env.REACT_MODULES || path.resolve(root, '../04/scripts/node_modules');
const app = fs.mkdtempSync(path.join(os.tmpdir(), 'pwd-week5-examples-'));
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'lecture-content.js'), 'utf8'), context);
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const topics = [8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 28, 30, 32];
for (const n of topics) {
  const id = 'topic-' + String(n).padStart(2, '0');
  const section = html.split('data-wd-slide="' + id + '"')[1].split('</section>')[0];
  const key = section.match(/<pre\b[^>]*data-wd-i18n="([^"]+)"/)[1];
  fs.writeFileSync(path.join(app, id + '.jsx'), context.window.LECTURE_CONTENT.ko[key]);
}
fs.symlinkSync(modules, path.join(app, 'node_modules'), 'dir');
fs.writeFileSync(path.join(app, 'index.html'), '<div id="root"></div><script type="module" src="/main.jsx"></script>');
fs.writeFileSync(path.join(app, 'main.jsx'), `
import React from 'react';
import { createRoot } from 'react-dom/client';
${topics.map(n => `import Topic${n} from './topic-${String(n).padStart(2, '0')}.jsx';`).join('\n')}
const components = {${topics.map(n => `${n}: Topic${n}`).join(',')}};
let root;
window.mount = (n, props = {}) => {
  root?.unmount();
  root = createRoot(document.getElementById('root'));
  root.render(React.createElement(components[n], props));
};
window.changeId = () => root.render(<Topic17 productId="p2" />);
window.changeProduct = () => root.render(<Topic13 productId="p2" />);
window.mountStock = fail => window.mount(32, {
  initial: false,
  saveStock: () => new Promise((resolve, reject) => {
    window.finishStock = () => fail ? reject(Error('failed')) : resolve(true);
  })
});
window.unmount = () => root.unmount();
`);
(async () => {
  const { createServer } = await import(pathToFileURL(path.join(modules, 'vite/dist/node/index.js')));
  const server = await createServer({root: app, configFile: false, server: {host: '127.0.0.1', port: 0}});
  await server.listen();
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  const page = await browser.newPage();
  const errors = [], logs = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', msg => { if (msg.type() === 'log') logs.push(msg.text()); });
  const mount = async (n, props) => { await page.evaluate(([n,p]) => window.mount(n,p), [n,props || {}]); await page.waitForTimeout(80); };
  const text = async (selector, value) => assert.equal(await page.locator(selector).textContent(), value);
  try {
    await page.goto('http://127.0.0.1:' + server.httpServer.address().port);
    await page.waitForFunction(() => window.mount);
    await mount(8); await page.locator('button').click(); await text('button','수량: 2');
    await mount(9);
    await page.evaluate(() => window.originalHeading = document.querySelector('h2'));
    await page.locator('button').click(); await text('button','2');
    assert.ok(await page.evaluate(() => document.querySelector('h2') === window.originalHeading));
    await mount(10); await page.getByText('값 두 번').click(); await text('p','1');
    await page.getByText('함수 두 번').click(); await text('p','3');
    await mount(11); await text('button','품절'); await page.locator('button').click(); await text('button','재고 있음');
    await mount(12,{products:[{id:'p1',name:'사과'},{id:'p2',name:'배'}]});
    await page.locator('input').fill('사'); await text('p','1개'); await text('li','사과');
    await mount(13,{productId:'p1'}); await page.locator('button').click(); await page.locator('button').click();
    await text('button','수량: 3'); await page.evaluate(() => window.changeProduct()); await page.waitForTimeout(80); await text('button','수량: 1');
    await mount(15); await page.locator('input').fill('사과'); await text('p','검색어: 사과');
    await page.locator('button').click(); assert.ok(await page.locator('input').evaluate(e => e === document.activeElement));
    await page.evaluate(() => document.title = 'Original');
    await mount(16); await page.locator('input').fill('배');
    await page.waitForFunction(() => document.title === '상품: 배');
    await page.evaluate(() => window.unmount()); assert.equal(await page.title(),'Original');
    await mount(17,{productId:'p1'}); await page.evaluate(() => window.changeId());
    await page.waitForFunction(() => document.querySelector('p')?.textContent === '조회 대상: p2');
    await page.waitForTimeout(1100); await page.evaluate(() => window.unmount());
    assert.ok(logs.indexOf('stop p1') < logs.indexOf('start p2'));
    assert.ok(logs.includes('poll p2') && logs.includes('stop p2'));
    const polls = logs.filter(x => x.startsWith('poll')).length;
    await page.waitForTimeout(1100); assert.equal(logs.filter(x => x.startsWith('poll')).length,polls);
    await mount(18); await page.getByText('사과: 1').click(); await text('button:first-child','사과: 2'); await text('button:last-child','배: 1');
    for (const [status, products, expected] of [['loading', [], '조회 중'],['error', [], '조회 실패'],['success', [], '검색 결과 없음']]) {
      await mount(28,{status,products}); await text('p',expected);
    }
    await mount(30); await page.locator('button').click(); assert.ok(await page.locator('button').isDisabled());
    await page.waitForFunction(() => document.querySelector('[role="status"]').textContent === '상품명을 입력하세요');
    await page.locator('input').fill('사과'); await page.locator('button').click();
    await page.waitForFunction(() => document.querySelector('[role="status"]').textContent === '확인: 사과');
    for (const fail of [false,true]) {
      await page.evaluate(f => window.mountStock(f), fail); await page.waitForTimeout(80);
      await text('p:first-child','품절'); await page.locator('button').click(); await text('p:first-child','재고 있음');
      await page.evaluate(() => window.finishStock());
      await page.waitForFunction(fail => document.querySelector('p').textContent === (fail ? '품절' : '재고 있음'),fail);
      await page.waitForTimeout(80); await text('[role="alert"]', fail ? '저장 실패: 다시 시도하세요' : '');
    }
    assert.deepEqual(errors,[]);
    console.log('React slide examples: 13 topics; state, commit, snapshot, immutability, derived values, key reset, refs, cleanup, independent Hooks, async states, Actions, optimistic success/failure passed');
  } finally {
    await browser.close(); await server.close(); fs.rmSync(app,{recursive:true,force:true});
  }
})().catch(e => {console.error(e); process.exitCode = 1;});
