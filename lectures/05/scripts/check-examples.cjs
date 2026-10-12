// Execute the current slide code in an isolated React development app.
// PLAYWRIGHT_PATH=/path/to/playwright node lectures/05/scripts/check-examples.cjs
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');

const directory = path.resolve(__dirname, '..');
const modules = path.resolve(process.env.REACT_MODULES || path.join(directory, '../04/scripts/node_modules'));
const reactTypes = path.resolve(process.env.REACT_TYPES || path.join(modules, '@types'));
const output = path.resolve(process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-lecture-05/review'));
const componentIds = [
  'function-component', 'jsx', 'jsx-expressions', 'jsx-attributes', 'fragment',
  'props', 'component-files', 'children', 'conditional-rendering', 'list-rendering',
  'list-key', 'static-product-ui', 'event-handler', 'state', 'render',
  'state-snapshot', 'state-updater', 'state-immutability', 'derived-values',
  'controlled-inputs', 'lifting-state', 'state-preservation', 'state-reset-key',
  'hook-rules', 'ref', 'effect', 'effect-dependencies', 'effect-cleanup', 'custom-hook'
];

function readExamples() {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.join(directory, 'lecture-content.js'), 'utf8'), context);
  const messages = context.window.LECTURE_CONTENT;
  const html = fs.readFileSync(path.join(directory, 'index.html'), 'utf8');
  const sections = [...html.matchAll(/<section\b[^>]*data-wd-slide="([^"]+)"[^>]*>[\s\S]*?<\/section>/g)];
  assert.equal(sections.length, 65, 'Update example coverage when the current 65-slide deck changes');
  const examples = new Map();
  for (const [markup, slideId] of sections) {
    if (!slideId.startsWith('concept-')) continue;
    const blocks = [...markup.matchAll(/<pre\b([^>]*data-wd-i18n="([^"]+)"[^>]*)>/g)].map(match => {
      const [, attributes, key] = match;
      const language = attributes.match(/data-wd-code="([^"]+)"/)[1];
      const labels = [...markup.slice(0, match.index).matchAll(/<p\b[^>]*class="wd-lesson-code-label"[^>]*data-wd-i18n="([^"]+)"/g)];
      assert.equal(typeof messages.ko[key], 'string', `${slideId}: missing code for ${key}`);
      assert.equal(messages.ko[key], messages.en[key], `${slideId}: runtime code differs between locales`);
      return { code: messages.ko[key], language, label: messages.ko[labels.at(-1)?.[1]] || '' };
    });
    if (blocks.length) examples.set(slideId.slice('concept-'.length), blocks);
  }
  const complete = new Map();
  for (const [id, blocks] of examples) {
    let candidates = blocks.filter(block => ['jsx', 'tsx'].includes(block.language)
      && /export\s+default\s+function\b/.test(block.code));
    if (id === 'component-files') {
      candidates = candidates.filter(block => /import\s+ProductRow\s+from\s+['"]\.\/ProductRow['"]/.test(block.code));
    } else if (id === 'hook-rules') {
      // The second complete-looking component intentionally violates the Rules of Hooks.
      candidates = candidates.filter(block => block.label.startsWith('올바른'));
    }
    if (candidates.length) {
      assert.equal(candidates.length, 1, `${id}: identify one primary complete component`);
      complete.set(id, candidates[0]);
    }
  }
  assert.deepEqual([...complete.keys()].sort(), [...componentIds].sort(),
    'Every current complete function example needs an explicit runtime check');
  const classExample = examples.get('function-component').find(block => /export\s+default\s+class\b/.test(block.code));
  assert.ok(classExample, 'The function-component slide also needs its class example checked');
  complete.set('function-component-class', classExample);
  return { examples, complete, slides: sections.length };
}

async function run() {
  let app, server, browser, failure;
  try {
    const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
    const ts = require('../../../packages/web-deck/node_modules/typescript');
    const { examples, complete, slides } = readExamples();
    assert.ok(fs.existsSync(path.join(reactTypes, 'react/index.d.ts')),
      'Set REACT_TYPES to an @types directory containing @types/react');
    app = fs.mkdtempSync(path.join(os.tmpdir(), 'pwd-week5-examples-'));
    fs.symlinkSync(modules, path.join(app, 'node_modules'), 'dir');
    const entries = new Map();
    const typedFiles = [];
    for (const [id, block] of complete) {
      const folder = path.join(app, id);
      fs.mkdirSync(folder);
      const filename = `index.${block.language}`;
      const entry = path.join(folder, filename);
      fs.writeFileSync(entry, block.code);
      entries.set(id, `./${id}/${filename}`);
      if (block.language === 'tsx') typedFiles.push(entry);
      if (id === 'component-files') {
        const module = examples.get(id).find(item => /export\s+default\s+function\s+ProductRow\b/.test(item.code));
        assert.ok(module, 'Component files must include the imported ProductRow module');
        const dependency = path.join(folder, 'ProductRow.tsx');
        fs.writeFileSync(dependency, module.code);
        typedFiles.push(dependency);
      }
    }
    const program = ts.createProgram(typedFiles, {
      target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext,
      moduleResolution: ts.ModuleResolutionKind.Bundler, jsx: ts.JsxEmit.ReactJSX,
      strict: true, noEmit: true, skipLibCheck: true, typeRoots: [reactTypes],
      paths: {
        react: [path.join(reactTypes, 'react/index.d.ts')],
        'react/*': [path.join(reactTypes, 'react/*')]
      }
    });
    const diagnostics = ts.getPreEmitDiagnostics(program);
    assert.equal(diagnostics.length, 0, ts.formatDiagnosticsWithColorAndContext(diagnostics, {
      getCanonicalFileName: filename => filename, getCurrentDirectory: () => app, getNewLine: () => '\n'
    }));
    fs.writeFileSync(path.join(app, 'index.html'), '<meta charset="utf-8"><link rel="icon" href="data:,"><title>Examples</title><div id="root"></div><script type="module" src="/main.jsx"></script>');
    fs.writeFileSync(path.join(app, 'main.jsx'), `
import React from 'react';
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';
${[...entries].map(([id, entry], index) => `import Component${index} from '${entry}';`).join('\n')}
const components = {${[...entries.keys()].map((id, index) => `${JSON.stringify(id)}: Component${index}`).join(',')}};
const review = window.review = { logs: [], alerts: [] };
const print = console.log.bind(console);
console.log = (...args) => { review.logs.push(args.map(String).join(' ')); print(...args); };
window.alert = value => review.alerts.push(String(value));
let root, currentId, currentProps, currentStrict;
const element = () => {
  const child = React.createElement(components[currentId], currentProps);
  const content = currentId === 'conditional-rendering'
    ? React.createElement('table', null, React.createElement('tbody', null, child)) : child;
  return currentStrict ? React.createElement(React.StrictMode, null, content) : content;
};
review.mount = (id, props = {}, strict = false) => {
  root?.unmount();
  review.logs = []; review.alerts = [];
  currentId = id; currentProps = props; currentStrict = strict;
  root = createRoot(document.getElementById('root'));
  flushSync(() => root.render(element()));
};
review.rerender = props => { currentProps = props; flushSync(() => root.render(element())); };
review.flush = () => flushSync(() => {});
review.unmount = () => { root?.unmount(); root = null; };
`);
    const { createServer } = await import(pathToFileURL(path.join(modules, 'vite/dist/node/index.js')));
    server = await createServer({ root: app, configFile: false, server: { host: '127.0.0.1', port: 0 } });
    await server.listen();
    browser = await chromium.launch({ channel: 'chrome', headless: true });
    const page = await browser.newPage();
    const errors = [], tested = new Set(), strictMode = {};
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => {
      if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`);
    });
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
    });
    // Advance the examples' actual setTimeout/setInterval callbacks without real one-second sleeps.
    await page.clock.install();
    await page.goto(`http://127.0.0.1:${server.httpServer.address().port}`);
    await page.waitForFunction(() => typeof window.review?.mount === 'function');
    const mount = async (id, props = {}, strict = false) => {
      tested.add(id);
      await page.evaluate(([id, props, strict]) => window.review.mount(id, props, strict), [id, props, strict]);
    };
    const flush = () => page.evaluate(() => window.review.flush());
    const logs = () => page.evaluate(() => window.review.logs);
    const text = async (selector, expected) => {
      await page.waitForFunction(({ selector, expected }) => document.querySelector(selector)?.textContent === expected,
        { selector, expected }, { timeout: 3000 });
      assert.equal(await page.locator(selector).textContent(), expected);
    };
    const texts = async (selector, expected) => {
      await page.waitForFunction(({ selector, expected }) =>
        JSON.stringify([...document.querySelectorAll(selector)].map(element => element.textContent)) === JSON.stringify(expected),
      { selector, expected }, { timeout: 3000 });
      assert.deepEqual(await page.locator(selector).allTextContents(), expected);
    };

    await mount('function-component'); await text('h2', '상품 목록'); await text('p', '사과');
    await mount('function-component-class'); await text('h2', '상품 목록');
    await mount('jsx'); await text('h2', '상품 목록'); await text('p', '사과');
    await mount('jsx-expressions'); await text('p', '사과 · 2000원');
    await mount('jsx-attributes');
    assert.equal(await page.locator('input').getAttribute('maxlength'), '40');
    assert.equal(await page.locator('label').getAttribute('for'), await page.locator('input').getAttribute('id'));
    assert.equal(await page.locator('label').evaluate(element => getComputedStyle(element).color), 'rgb(0, 128, 0)');
    await mount('fragment'); assert.equal(await page.locator('#root > *').count(), 2);
    await mount('props'); await texts('p', ['사과', '용과', '상품']);
    await mount('component-files'); await texts('td', ['사과', '1달러']);
    await mount('children'); await text('section > h2', '상품 목록'); await text('section > p', '이름과 가격');
    for (const [stocked, expected] of [[true, '사과'], [false, '사과 (품절)']]) {
      await mount('conditional-rendering', { product: { id: 'p1', name: '사과', price: 1, stocked } });
      await text('td:first-child', expected);
    }
    await mount('list-rendering'); await texts('p', ['사과', '배']);
    await mount('list-key'); await texts('li', ['사과', '배']);
    await mount('static-product-ui');
    await page.getByRole('textbox').fill('없는 상품'); await page.getByRole('checkbox').check();
    await texts('li', ['사과 · 1달러', '배 · 2달러']);
    await mount('event-handler'); await page.locator('button').click();
    assert.equal(await page.evaluate(() => window.review.alerts.at(-1)), '상품을 선택했습니다');
    await mount('state'); await text('button', '수량: 1');
    await page.locator('button').click(); await text('button', '수량: 2');
    await page.locator('button').click(); await text('button', '수량: 3');
    await mount('render');
    const originalButton = await page.locator('button').elementHandle();
    await page.locator('button').click(); await text('button', '수량: 2');
    await page.locator('button').click(); await text('button', '수량: 3');
    assert.ok(await originalButton.evaluate(element => element === document.querySelector('button')));
    assert.deepEqual(await logs(), ['Render: 1', 'Render: 2', 'Render: 3']);
    await mount('state-snapshot'); await page.locator('button').click(); await text('button', '1');
    await page.clock.runFor(1000);
    await page.waitForFunction(() => window.review.alerts.length === 1);
    assert.deepEqual(await page.evaluate(() => window.review.alerts), ['0']);
    await mount('state-updater'); await page.locator('button').click(); await text('button', '2');
    await mount('state-immutability'); await text('button', '품절');
    await page.locator('button').click(); await text('button', '재고 있음');
    await mount('derived-values'); await text('p', '사과 · 배 · 2개');
    await page.locator('button').click(); await text('p', '사과 · 1개');
    await mount('controlled-inputs');
    await page.getByRole('textbox').fill('사과'); await page.getByRole('checkbox').check();
    assert.equal(await page.getByRole('textbox').inputValue(), '사과');
    assert.ok(await page.getByRole('checkbox').isChecked());
    await mount('lifting-state'); await page.locator('button').click();
    await text('button', '추가: 1'); await text('p', '수량: 1');
    await mount('state-preservation');
    await page.locator('button').nth(1).click(); await page.locator('button').nth(1).click();
    await page.locator('button').first().click(); await text('button:last-child', '상품 수량: 2');
    await mount('state-reset-key'); await page.locator('input').fill('사과 수정 중');
    await page.locator('button').click(); assert.equal(await page.locator('input').inputValue(), '배');
    await mount('hook-rules', { hidden: false }); await page.locator('input').fill('사과');
    await page.evaluate(() => window.review.rerender({ hidden: true }));
    assert.equal(await page.locator('input').count(), 0);
    await page.evaluate(() => window.review.rerender({ hidden: false }));
    assert.equal(await page.locator('input').inputValue(), '사과');
    await mount('ref'); await page.locator('button').click();
    assert.ok(await page.locator('input').evaluate(element => element === document.activeElement));
    await mount('effect'); await page.waitForFunction(() => document.title === '상품: 사과'); await text('h2', '사과');
    await mount('effect-dependencies'); assert.deepEqual(await logs(), ['sync 사과']);
    await page.getByText('테마 변경', { exact: true }).click(); await flush();
    assert.equal(await page.locator('section').evaluate(element => getComputedStyle(element).backgroundColor), 'rgb(255, 192, 203)');
    assert.equal(await page.title(), '상품: 사과'); assert.deepEqual(await logs(), ['sync 사과']);
    await page.getByText('상품 변경', { exact: true }).click(); await flush();
    assert.equal(await page.title(), '상품: 배'); assert.deepEqual(await logs(), ['sync 사과', 'sync 배']);
    await mount('effect-cleanup'); await page.clock.runFor(1000);
    assert.ok((await logs()).includes('poll 사과'));
    await page.getByText('값 변경', { exact: true }).click(); await flush();
    assert.equal((await logs()).at(-1), 'stop 사과');
    const applePolls = (await logs()).filter(line => line === 'poll 사과').length;
    await page.clock.runFor(1000);
    assert.ok((await logs()).includes('poll 배'));
    assert.equal((await logs()).filter(line => line === 'poll 사과').length, applePolls);
    await page.getByText('컴포넌트 제거', { exact: true }).click(); await flush();
    assert.equal((await logs()).at(-1), 'stop 배');
    const finishedLogs = await logs();
    await page.clock.runFor(1100); assert.deepEqual(await logs(), finishedLogs);
    await mount('custom-hook'); await texts('button', ['사과: 1', '배: 1']);
    await page.locator('button').first().click(); await texts('button', ['사과: 2', '배: 1']);
    await page.locator('button').last().click(); await texts('button', ['사과: 2', '배: 2']);
    assert.deepEqual([...tested].sort(), [...complete.keys()].sort(), 'Exercise every complete slide example');

    // Match the default Vite project's root StrictMode behavior in development.
    await mount('render', {}, true);
    await page.locator('button').click(); await text('button', '수량: 2');
    await page.locator('button').click(); await text('button', '수량: 3');
    strictMode.render = await logs();
    assert.deepEqual(strictMode.render, ['Render: 1', 'Render: 1', 'Render: 2', 'Render: 2', 'Render: 3', 'Render: 3']);
    await mount('effect-dependencies', {}, true);
    strictMode.effectDependencies = await logs();
    assert.deepEqual(strictMode.effectDependencies, ['sync 사과', 'sync 사과']);
    await mount('effect-cleanup', {}, true);
    strictMode.initialCleanup = (await logs()).filter(line => line.startsWith('stop '));
    assert.deepEqual(strictMode.initialCleanup, ['stop 사과']);
    await page.clock.runFor(1000);
    assert.deepEqual((await logs()).filter(line => line.startsWith('poll ')), ['poll 사과'],
      'The extra StrictMode cleanup must leave only one active interval');
    await page.evaluate(() => window.review.unmount());
    const unmountedLogs = await logs();
    await page.clock.runFor(1100); assert.deepEqual(await logs(), unmountedLogs);
    assert.deepEqual(errors, []);
    const result = {
      slides, components: componentIds.length, supplementalComponents: ['function-component-class'],
      strictTypeScriptFiles: typedFiles.length, tested: [...tested], errors, strictMode,
      reactVersion: require(path.join(modules, 'react/package.json')).version,
      resultFile: path.join(output, 'examples.json')
    };
    fs.mkdirSync(output, { recursive: true });
    fs.writeFileSync(result.resultFile, JSON.stringify(result, null, 2) + '\n');
    return result;
  } catch (error) {
    failure = error;
    throw error;
  } finally {
    const cleanups = await Promise.allSettled([
      browser ? browser.close() : Promise.resolve(),
      server ? server.close() : Promise.resolve()
    ]);
    if (app) fs.rmSync(app, { recursive: true, force: true });
    const cleanupErrors = cleanups.filter(result => result.status === 'rejected').map(result => result.reason);
    if (cleanupErrors.length && !failure) throw new AggregateError(cleanupErrors, 'Example-test cleanup failed');
  }
}

run().then(result => console.log(JSON.stringify(result, null, 2))).catch(error => {
  console.error(error);
  process.exitCode = 1;
});
