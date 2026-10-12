// Compare every copied slide with Lecture 04, including the original live demos.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const base = process.env.DECK_URL || 'http://127.0.0.1:4305';
const output = process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-react-import');
const corrections = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../materials/import-text-corrections.json'), 'utf8'));
fs.mkdirSync(output, {recursive:true});

async function settle(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(img => img.complete ? null : new Promise(resolve => {
      img.addEventListener('load', resolve, {once:true});
      img.addEventListener('error', resolve, {once:true});
    })));
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
}

async function comparePixels(page, first, second) {
  if (first.equals(second)) return {maxChannelDelta:0};
  return page.evaluate(async ({first,second}) => {
    const images = await Promise.all([first,second].map(async data =>
      createImageBitmap(await (await fetch('data:image/png;base64,' + data)).blob())));
    if (images[0].width !== images[1].width || images[0].height !== images[1].height)
      return {maxChannelDelta:255};
    const canvas = document.createElement('canvas');
    canvas.width = images[0].width; canvas.height = images[0].height;
    const context = canvas.getContext('2d');
    const pixels = images.map(image => {
      context.drawImage(image,0,0);
      return context.getImageData(0,0,canvas.width,canvas.height).data;
    });
    let maxChannelDelta = 0;
    for (let i=0; i<pixels[0].length; i++) maxChannelDelta = Math.max(maxChannelDelta, Math.abs(pixels[0][i]-pixels[1][i]));
    return {maxChannelDelta};
  }, {first:first.toString('base64'),second:second.toString('base64')});
}

async function exerciseDemos(page) {
  const go = id => page.evaluate(id => {
    const slides = [...document.querySelectorAll('[data-wd-slide]')];
    document.querySelector('[data-web-deck]').__webDeck.goTo(slides.findIndex(s => s.dataset.wdSlide === id));
  }, id);
  await page.click('[data-locale="ko"]');
  await go('slide-11');
  const components = page.locator('[data-react-demo="components"]');
  const boundary = components.getByRole('button');
  assert.equal(await boundary.getAttribute('aria-pressed'), 'true');
  await boundary.click();
  assert.equal(await boundary.getAttribute('aria-pressed'), 'false');
  await boundary.click();
  assert.equal(await boundary.getAttribute('aria-pressed'), 'true');
  assert.equal(await components.locator('[data-product]').count(), 6);
  await go('slide-12');
  assert.equal(await page.locator('[data-react-demo="reuse"] [data-product]').count(), 6);
  await go('slide-13');
  const apps = page.locator('[data-react-demo="filter"] .react-product-app');
  const after = apps.nth(1);
  assert.equal(await apps.nth(0).locator('[data-product]').count(), 6);
  assert.equal(await after.locator('[data-product]').count(), 4);
  const search = after.getByRole('searchbox');
  await search.fill('사과');
  await after.getByText('검색 결과 1개', {exact:true}).waitFor();
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
  assert.equal(await apple.evaluate(el => el.isConnected), true);
  await page.click('[data-locale="en"]');
  await after.getByText('4 results', {exact:true}).waitFor();
  await search.fill('Apple');
  await after.getByText('1 result', {exact:true}).waitFor();
  await go('slide-24');
  assert.equal(await page.locator('[data-wd-slide="slide-24"] img').evaluateAll(images =>
    images.length === 1 && images.every(img => img.complete && img.naturalWidth > 0)), true);
}

(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const errors = [], comparisons = [];
  try {
    const pages = await Promise.all([browser.newPage(), browser.newPage()]);
    pages.forEach(page => {
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => { if (response.status() >= 400) errors.push(response.status() + ' ' + response.url()); });
    });
    await Promise.all(pages.map((page,i) => page.goto(base + '/lectures/0' + (i + 4) + '/')));
    await Promise.all(pages.map(settle));
    const count = await pages[0].locator('[data-wd-slide]').count();
    assert.equal(await pages[1].locator('[data-wd-import="04/react"]').count(), count);
    for (const locale of ['ko','en']) {
      await Promise.all(pages.map(async page => {
        await page.emulateMedia({media:'screen'});
        await page.setViewportSize({width:1312,height:818});
        await page.click('[data-locale="' + locale + '"]');
        await settle(page);
      }));
      // Compare against the exact approved Week 5 translation while retaining
      // pixel/layout comparison for the whole slide and every other sentence.
      for (const correction of corrections.filter(item => item.locale === locale)) {
        const selector = `[data-wd-slide="${correction.source_slide}"] [data-wd-i18n="${correction.key}"]`;
        const original = pages[0].locator(selector);
        const imported = pages[1].locator(selector);
        assert.equal(await original.count(), 1, 'Correction must identify one original node');
        assert.equal(await imported.count(), 1, 'Correction must identify one imported node');
        assert.equal(await original.textContent(), correction.before, 'Original correction text changed');
        assert.equal(await imported.textContent(), correction.after, 'Imported translation correction missing');
        await original.evaluate((element, value) => {element.textContent = value;}, correction.after);
      }
      for (const mode of ['screen','print','mobile']) {
        await Promise.all(pages.map(async page => {
          await page.emulateMedia({media:mode === 'print' ? 'print' : 'screen'});
          await page.setViewportSize(mode === 'mobile' ? {width:390,height:844} : {width:1312,height:818});
        }));
        for (let i = 0; i < count; i++) {
          // Screens 24–25 were explicitly rewritten; checked by the layout audit.
          if (i === 22 || i === 23) continue;
          const captures = await Promise.all(pages.map(async (page,j) => {
            await page.evaluate(index => document.querySelector('[data-web-deck]').__webDeck.goTo(index), i + j);
            await settle(page);
            const slide = page.locator('[data-wd-slide]').nth(i + j);
            const metrics = await slide.evaluate(s => {
              const box = s.getBoundingClientRect();
              const round = n => Math.round(n * 100) / 100;
              return [...s.querySelectorAll('h1,h2,h3,h4,p,dt,dd,li,pre,img,figcaption,input,button')]
                .filter(e => !e.closest('[hidden]') && e.getClientRects().length).map(e => {
                  const r = e.getBoundingClientRect(), style = getComputedStyle(e);
                  return {tag:e.tagName,text:e.textContent,x:round(r.left-box.left),y:round(r.top-box.top),
                    w:round(r.width),h:round(r.height),font:style.font,fontFamily:style.fontFamily,color:style.color,
                    background:style.backgroundColor,sw:e.scrollWidth,cw:e.clientWidth,
                    ...(e.tagName === 'IMG' ? {loaded:e.complete && e.naturalWidth > 0} : {})};
                });
            });
            const file = path.join(output, `${locale}-${mode}-${String(i+1).padStart(2,'0')}-${j ? 'copy' : 'source'}.png`);
            return {metrics, png:await slide.screenshot({path:file, animations:'disabled'})};
          }));
          const label = `${locale}/${mode}/source slide ${i+1}`;
          assert.deepEqual(captures[1].metrics, captures[0].metrics, label + ': displayed content or layout changed');
          const pixels = await comparePixels(pages[1],captures[0].png,captures[1].png);
          // Raster image resampling may round a color channel by one level.
          assert.ok(pixels.maxChannelDelta <= 1, label + ': rendered image changed');
          comparisons.push({locale,mode,sourceSlide:i+1,copiedSlide:i+2,...pixels});
        }
      }
    }
    await pages[1].emulateMedia({media:'screen'});
    await pages[1].setViewportSize({width:1312,height:818});
    await exerciseDemos(pages[1]);
    assert.deepEqual(errors, []);
    fs.writeFileSync(path.join(output,'import-audit.json'), JSON.stringify({count,comparisons,corrections,errors,demos:'passed'},null,2));
    console.log(JSON.stringify({count,comparisons:comparisons.length,textCorrections:corrections.length,errors,demos:'passed',output},null,2));
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode=1;});
