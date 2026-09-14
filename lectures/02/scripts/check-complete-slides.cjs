const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { spawn } = require('node:child_process');
const practice = process.env.SVELTE_PRACTICE_ROOT || path.resolve(__dirname, '../../../../pwd-2026-practices/pwd-week2');
const req = createRequire(path.join(practice, 'package.json'));
const { compile } = req('svelte/compiler');
const esbuild = req('esbuild');
const { chromium } = req('playwright');
const { examples, localized } = require('./complete-examples.cjs');
const lecture = path.resolve(__dirname, '..');
const out = fs.mkdtempSync(path.join(os.tmpdir(), 'week2-complete-check-'));
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(lecture, 'lecture-content.js'), 'utf8'), sandbox);
const messages = sandbox.window.LECTURE_CONTENT;
const sources = {};
const owners = { state: 26, derived: 26, focus: 26, todos: 28, mouse: 29, Child: 32, Parent: 32, Card: 34, Cards: 34 };
const report = { svelte: req('svelte/package.json').version, components: [], interactions: [], navigation: [], locales: {} };
for (const [i, locale] of ['ko', 'en'].entries()) {
  for (const name of Object.keys(examples)) {
    const source = name === 'navigation'
      ? messages[locale].w2_31_guard_script + '\n\n' + messages[locale].w2_31_guard_markup
      : messages[locale][`w2_${owners[name]}_code_${name}`];
    assert.equal(source, localized(name)[i], `${locale} ${name}: visible code differs from its source`);
    const result = compile(source, { filename: name + '.svelte', generate: 'client', dev: true });
    assert.deepEqual(result.warnings.map(w => w.code), [], `${locale} ${name}: compiler warnings`);
    sources[`${locale}_${name}`] = source;
    report.components.push(`${locale}_${name}`);
  }
}

function write(relative, data) {
  const file = path.join(out, relative);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
}

(async () => {
  const names = Object.keys(sources).filter(name => !name.endsWith('_navigation'));
  const result = await esbuild.build({
    stdin: { contents: "import {mount,unmount} from 'svelte';\n" + names.map(n => `import ${n} from 'example:${n}';`).join('\n') + `\nconst components={${names.join(',')}};let active;window.show=async(name,props={})=>{if(active)await unmount(active);active=mount(components[name],{target:document.body,props});};`, resolveDir: practice },
    bundle: true, write: false, format: 'iife', platform: 'browser', conditions: ['browser'],
    plugins: [{ name: 'examples', setup(build) {
      build.onResolve({ filter: /^example:/ }, a => ({ path: a.path.slice(8), namespace: 'example' }));
      build.onResolve({ filter: /(?:Card|Child)\.svelte$/ }, a => ({ path: a.importer.slice(0, 3) + (a.path.includes('Card') ? 'Card' : 'Child'), namespace: 'example' }));
      build.onLoad({ filter: /.*/, namespace: 'example' }, a => ({ contents: compile(sources[a.path], { filename: a.path + '.svelte', generate: 'client', dev: true }).js.code, loader: 'js', resolveDir: practice }));
    }}]
  });
  write('package.json', JSON.stringify({ type: 'module', devDependencies: { '@sveltejs/kit': '*', svelte: '*', vite: '*' } }));
  write('svelte.config.js', 'export default {};');
  write('vite.config.js', "import {sveltekit} from '@sveltejs/kit/vite';export default {plugins:[sveltekit()]};");
  write('src/app.html', '<!doctype html><html lang="en"><head><meta charset="utf-8" />%sveltekit.head%</head><body><div>%sveltekit.body%</div></body></html>');
  for (const locale of ['ko', 'en']) {
    write(`src/routes/${locale}/+layout.svelte`, sources[locale + '_navigation'] + `\n<nav><a href="/${locale}/about">About</a><a href="/${locale}">Home</a></nav>`);
    write(`src/routes/${locale}/+page.svelte`, '<h1>Home page</h1>');
    write(`src/routes/${locale}/about/+page.svelte`, '<h1>About page</h1>');
  }
  fs.symlinkSync(path.join(practice, 'node_modules'), path.join(out, 'node_modules'), process.platform === 'win32' ? 'junction' : 'dir');
  const vite = path.join(path.dirname(req.resolve('vite/package.json')), 'bin/vite.js');
  const port = 4197;
  const server = spawn(process.execPath, [vite, '--host', '127.0.0.1', '--port', String(port), '--strictPort'], { cwd: out, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  let logs = '';
  server.stdout.on('data', data => { logs += data; });
  server.stderr.on('data', data => { logs += data; });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage();
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto('about:blank'); await page.addScriptTag({ content: result.outputFiles[0].text });
    for (const locale of ['ko', 'en']) {
      const show = (name, props = {}) => page.evaluate(({ name, props }) => window.show(name, props), { name: `${locale}_${name}`, props });
      await show('state'); await page.getByRole('textbox').fill('Svelte'); await page.getByRole('button').nth(1).click();
      assert.equal(await page.locator('p').textContent(), 'Svelte / 2');
      await page.getByRole('button').first().click(); assert.equal((await page.getByRole('button').first().textContent()).trim(), 'ON');
      await show('derived'); assert.match(await page.locator('p').textContent(), locale === 'ko' ? /6500 \/ 6,500원/ : /6500 \/ 6,500 KRW/);
      await show('focus'); await page.getByRole('button').click(); assert.equal(await page.getByRole('textbox').evaluate(el => el === document.activeElement), true);
      await show('todos'); const checkbox = page.getByRole('checkbox').first();
      assert.equal(await checkbox.isChecked(), false); await checkbox.click(); assert.equal(await checkbox.isChecked(), true);
      await checkbox.click(); assert.equal(await checkbox.isChecked(), false);
      await page.getByRole('button').click(); assert.equal(await page.locator('li').count(), 3);
      await show('mouse'); await page.mouse.move(120, 80); assert.match(await page.locator('p').textContent(), /120 × 80/);
      await show('Parent'); await page.getByRole('button').click(); assert.equal(await page.locator('p').textContent(), locale === 'ko' ? '변경된 인사말' : 'Updated!');
      await show('Cards', { data: { projects: [{ slug: 'memo', title: 'Memo', summary: 'Notes' }] } });
      assert.equal(await page.locator('article a').getAttribute('href'), '/projects/memo');
      await show('Cards', { data: { projects: [] } }); assert.equal(await page.locator('article').count(), 0);
      assert.equal(await page.locator('p').textContent(), locale === 'ko' ? '등록된 프로젝트 없음' : 'No projects yet.');
      report.interactions.push({ locale, state: true, derived: true, focus: true, checkbox: true, add: true, mouse: true, props: true, cards: true, emptyList: true });
    }
    // Exercise the actual $app/navigation implementation in a temporary SvelteKit app.
    for (const locale of ['ko', 'en']) {
      const navigationPage = await browser.newPage();
      navigationPage.on('pageerror', e => errors.push(e.message));
      await navigationPage.goto(`http://127.0.0.1:${port}/${locale}`, { waitUntil: 'networkidle' });
      assert.equal(await navigationPage.locator('h1').textContent(), 'Home page');
      await navigationPage.getByRole('textbox').fill('Unsaved draft');
      let dialogType;
      navigationPage.once('dialog', async dialog => { dialogType = dialog.type(); await dialog.dismiss(); });
      await navigationPage.getByRole('link', { name: 'About', exact: true }).click();
      assert.equal(dialogType, 'confirm'); assert.equal(new URL(navigationPage.url()).pathname, `/${locale}`);
      navigationPage.once('dialog', async dialog => { await dialog.accept(); });
      await navigationPage.getByRole('link', { name: 'About', exact: true }).click();
      await navigationPage.waitForURL(`**/${locale}/about`); assert.equal(await navigationPage.locator('h1').textContent(), 'About page');
      await navigationPage.getByRole('textbox').fill('Unsaved on reload');
      dialogType = null;
      navigationPage.once('dialog', async dialog => { dialogType = dialog.type(); await dialog.dismiss(); });
      await navigationPage.reload({ waitUntil: 'domcontentloaded', timeout: 3000 }).catch(e => { if (!/ERR_ABORTED|Timeout/.test(e.message)) throw e; });
      assert.equal(dialogType, 'beforeunload'); assert.equal(await navigationPage.getByRole('textbox').inputValue(), 'Unsaved on reload');
      // A new page avoids carrying the intentional unsaved-change guard into the next case.
      await navigationPage.close();
      report.navigation.push({ locale, children: true, reject: true, accept: true, nativeUnload: true });
    }
    assert.deepEqual(errors, []);
    const deck = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await deck.goto(process.env.DECK_URL || 'http://127.0.0.1:4186/lectures/02/');
    await deck.emulateMedia({ media: 'print' });
    for (const locale of ['ko', 'en', 'ko']) {
      await deck.evaluate(locale => document.querySelector('[data-web-deck]').__webDeck.setLocale(locale), locale);
      await deck.waitForTimeout(100);
      const rows = await deck.locator('[data-wd-slide]').evaluateAll(slides => slides.map((s, i) => ({ number: i + 1, title: s.querySelector('h1,h2')?.textContent, text: s.innerText, missing: [...s.querySelectorAll('img')].filter(img => !img.complete || !img.naturalWidth).length })));
      assert.equal(rows.length, 54); assert.equal(await deck.locator('.lesson-original-slide').count(), 0);
      assert.deepEqual(rows.filter(r => r.missing), []);
      if (locale === 'en') assert.deepEqual(rows.filter(r => /[\uac00-\ud7a3]/.test(r.text)), [], 'Korean text remains in English slides');
      else assert.equal(rows.filter(r => /[\uac00-\ud7a3]/.test(r.text)).length, 54);
      report.locales[locale] = { slides: rows.length, missingImages: 0, titles: rows.map(r => r.title) };
    }
  } finally {
    await browser.close(); server.kill(); fs.writeFileSync(path.join(out, 'server.log'), logs);
  }
  fs.writeFileSync(path.join(lecture, 'materials/final-review/completion-check.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(`Svelte ${report.svelte}: 20 KO/EN component compilations, bilingual interactions, actual SvelteKit navigation and all 54 translated slides passed.\nEvidence: ${out}`);
})().catch(e => { console.error(e); process.exitCode = 1; });
