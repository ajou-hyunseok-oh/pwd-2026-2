// Capture the unmodified Week 5 client in a fresh, disposable browser context.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const root = path.resolve(__dirname, '..');
const clientRoot = process.env.CLIENT_ROOT || path.resolve(root, '../../../..', 'pwd-week5');
const appURL = process.env.CLIENT_URL || 'http://127.0.0.1:5176';
const output = path.join(root, 'materials/screens');

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const viewport = { width: 1200, height: 900 };
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const errors = [], captures = [], checks = [];
  page.on('pageerror', error => errors.push(error.message));
  async function shot(name, route, { selector = 'main', fromSelector, height = 690, padding = 0, bottomPadding = 0, evidence = [], targetPage = page } = {}) {
    await targetPage.evaluate(() => window.scrollTo(0, 0));
    await targetPage.mouse.move(0, 0);
    // React may have updated the list before the category's 300 ms color transition finishes.
    // Wait for the real UI to settle so selected controls and their results show the same state.
    await targetPage.evaluate(async () => {
      await Promise.all(document.getAnimations().filter(animation => animation instanceof CSSTransition)
        .map(animation => animation.finished.catch(() => {})));
    });
    const area = await targetPage.locator(selector).boundingBox();
    if (fromSelector) {
      const from = await targetPage.locator(fromSelector).boundingBox();
      area.width -= from.x - area.x;
      area.x = from.x;
    }
    const clip = { x: Math.max(0, area.x - padding), y: Math.max(0, area.y - padding),
      width: area.width + padding * 2, height: Math.min(area.height, height) + padding * 2 + bottomPadding };
    await targetPage.screenshot({ path: path.join(output, name + '.png'), clip, animations: 'disabled' });
    captures.push({ file: name + '.png', route, selector, fromSelector, clip, evidence });
  }
  async function go(route, heading) {
    await page.goto(appURL + '/#' + route);
    await page.getByRole('heading', { name: heading, exact: true }).waitFor();
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(img => img.complete ? null : new Promise(resolve => {
        img.addEventListener('load', resolve, { once: true });
        img.addEventListener('error', resolve, { once: true });
        setTimeout(resolve, 10000);
      })));
    });
  }
  try {
    await go('/', '우리 학교 맛집을 찾아보세요!');
    await shot('home', '/', { selector: '.app', height: 900, evidence: ['Header', 'HomePage', 'footer'] });
    await go('/list', '맛집 목록');
    assert.equal(await page.locator('main h3').count(), 3);
    await shot('list', '/list');
    await shot('app-list', '/list', { selector: '.app', height: 900, evidence: ['Header', 'ListPage', 'footer', 'detail links'] });
    await page.getByRole('button', { name: '한식', exact: true }).click();
    assert.equal(await page.locator('main h3').count(), 1);
    await shot('filtered-list', '/list · 한식', { evidence: ['한식 selected', '전체 inactive', 'one restaurant card'] });
    assert.equal(await page.getByRole('button', { name: '한식', exact: true }).evaluate(button => getComputedStyle(button).backgroundColor), 'rgb(102, 126, 234)');
    assert.equal(await page.getByRole('button', { name: '전체', exact: true }).evaluate(button => getComputedStyle(button).backgroundColor), 'rgb(255, 255, 255)');
    checks.push('Filtered screenshot has Korean selected, All inactive, and exactly one matching card after the transition');
    await page.locator('main a').filter({ hasText: '자세히 보기' }).click();
    await page.getByRole('heading', { name: '송림식당', exact: true }).waitFor();
    assert.equal(new URL(page.url()).hash, '#/restaurant/1');
    await shot('detail', '/restaurant/1', { height: 760 });
    checks.push('Three seed restaurants, Korean category filter and card-to-detail navigation');
    await go('/submit', '🍽️ 새로운 맛집 제보하기');
    await page.getByLabel('맛집 이름 *', { exact: true }).fill('아주대 실습 식당');
    await page.getByLabel('카테고리 *', { exact: true }).selectOption('한식');
    await page.getByLabel('위치 *', { exact: true }).fill('아주대학교 정문 앞');
    await page.getByLabel('추천 메뉴').fill('김치찌개, 제육볶음');
    assert.equal(await page.getByLabel('추천 메뉴').inputValue(), '김치찌개, 제육볶음');
    await shot('submit-menu', '/submit · 추천 메뉴 입력', { selector: '#recommendedMenu >> ..', padding: 12,
      evidence: ['추천 메뉴', '김치찌개, 제육볶음'] });
    await page.locator('button[type="submit"]').click();
    await page.getByRole('heading', { name: '제보 감사합니다!', exact: true }).waitFor();
    await shot('submit-success', '/submit · 저장 성공', { selector: 'main > div',
      evidence: ['제보 감사합니다!', '다른 맛집 제보하기'] });
    const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('pwd-week5-submissions')));
    assert.equal(saved.length, 1);
    assert.equal(saved[0].status, 'pending');
    assert.deepEqual(saved[0].recommendedMenu, ['김치찌개', '제육볶음']);
    await go('/submissions', '제보 관리');
    await page.getByText('아주대 실습 식당', { exact: true }).waitFor();
    await shot('submissions', '/submissions · 브라우저 A', { selector: 'main table', fromSelector: 'main table th:nth-child(2)', bottomPadding: 30,
      evidence: ['아주대 실습 식당', '김치찌개, 제육볶음', 'pending', '승인'] });
    const otherContext = await browser.newContext({ viewport, deviceScaleFactor: 1 });
    try {
      const otherPage = await otherContext.newPage();
      await otherPage.goto(appURL + '/#/submissions');
      await otherPage.getByRole('heading', { name: '제보 관리', exact: true }).waitFor();
      await otherPage.evaluate(() => document.fonts.ready);
      assert.equal(await otherPage.locator('main tbody tr').count(), 0);
      assert.equal(await otherPage.evaluate(() => localStorage.getItem('pwd-week5-submissions')), null);
      await shot('submissions-empty', '/submissions · 브라우저 B', { selector: 'main table', fromSelector: 'main table th:nth-child(2)', bottomPadding: 85,
        evidence: ['same URL', 'zero submission rows', 'isolated browser storage'], targetPage: otherPage });
    } finally { await otherContext.close(); }
    checks.push('The same submissions URL shows one saved item in browser A and zero in isolated browser B');
    checks.push('Form input transformed into a menu array, saved locally and shown as pending');
    await go('/admin', '관리자 - 레스토랑 관리');
    assert.equal(await page.locator('main tbody tr').count(), 3);
    await shot('restaurant-table', '/admin · 맛집 목록', { selector: 'main table', padding: 12,
      evidence: ['송림식당', '별미떡볶이', 'Sogo', 'getRestaurants result'] });
    await go('/popular', '🔥 이번 주 인기 TOP 5');
    await shot('popular', '/popular', { height: 690 });
    await go('/list', '맛집 목록');
    const firstCard = page.locator('main h3').filter({ hasText: '송림식당' }).locator('..').locator('..');
    await firstCard.getByRole('button').click();
    assert.equal(await page.evaluate(() => JSON.parse(localStorage.getItem('restaurantLikes'))['1']), 1);
    assert.deepEqual(await page.evaluate(() => JSON.parse(localStorage.getItem('likedRestaurants'))), [1]);
    checks.push('Card likes stored under separate browser keys rather than restaurantAPI');
    assert.deepEqual(errors, []);
    const files = ['index.html', 'package.json', 'vite.config.ts', 'src/main.tsx', 'src/App.tsx', 'src/types/index.ts',
      'src/components/Header.tsx', 'src/components/PopularRestaurants.tsx', 'src/pages/AdminPage.tsx',
      'src/components/RestaurantList.tsx', 'src/components/RestaurantCard.tsx', 'src/components/SubmitRestaurant.tsx',
      'src/pages/ListPage.tsx', 'src/pages/DetailPage.tsx', 'src/pages/PopularPage.tsx', 'src/pages/SubmissionsPage.tsx',
      'src/services/api.ts', 'src/services/storage.ts'];
    fs.writeFileSync(path.join(root, 'materials/capture-manifest.json'), JSON.stringify({
      capturedAt: new Date().toISOString(), client: 'pwd-week5', viewport,
      captures, checks, errors,
      sourceFiles: files.map(file => ({ file, sha256: crypto.createHash('sha256').update(fs.readFileSync(path.join(clientRoot, file))).digest('hex') })),
      images: await page.locator('img').evaluateAll(images => images.map(img => ({ src: img.src, loaded: img.complete && img.naturalWidth > 0 })))
    }, null, 2) + '\n');
    console.log(JSON.stringify({ captures: captures.length, checks, errors }, null, 2));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
