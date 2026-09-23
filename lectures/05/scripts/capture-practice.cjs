// Capture the actual app in an isolated browser context, without changing its files.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const output = path.resolve(__dirname, '../materials/images');
fs.mkdirSync(output, {recursive:true});
(async()=>{
  const browser = await chromium.launch({channel:'chrome',headless:true});
  const page = await browser.newPage({viewport:{width:1180,height:830}});
  const base = process.env.PRACTICE_URL || 'http://127.0.0.1:5175';
  try {
    for (const [name, route] of [['list','list'],['detail','restaurant/1'],['submit','submit']]) {
      await page.goto(base + '/#/' + route);
      await page.waitForSelector(name === 'list' ? 'h3' : name === 'detail' ? 'h1' : 'form');
      await page.evaluate(async()=>{
        await document.fonts.ready;
        await Promise.all([...document.images].map(img=>img.decode().catch(()=>{})));
      });
      await page.screenshot({path:path.join(output,name+'.png')});
    }
    await page.goto(base + '/#/list');
    await page.getByRole('button',{name:'한식',exact:true}).click();
    await page.getByRole('heading',{name:'송림식당',exact:true}).waitFor();
    assert.equal(await page.getByRole('heading',{name:'별미떡볶이',exact:true}).count(),0);
    await page.getByRole('button',{name:'카페',exact:true}).click();
    await page.getByText('해당 카테고리에 맛집이 없습니다.').waitFor();
    await page.goto(base+'/#/restaurant/missing');
    await page.getByText('맛집을 찾을 수 없습니다.').waitFor();
    await page.goto(base+'/#/submit');
    await page.locator('button[type="submit"]').click();
    assert.equal(await page.evaluate(()=>localStorage.getItem('pwd-week5-submissions')),null);
    await page.locator('#restaurantName').fill('슬라이드 검증용 가상 식당');
    await page.locator('#category').selectOption({label:'한식'});
    await page.locator('#location').fill('캠퍼스 앞');
    await page.locator('#recommendedMenu').fill('메뉴 A, 메뉴 B');
    await page.locator('button[type="submit"]').click();
    await page.getByRole('heading',{name:'제보 감사합니다!'}).waitFor();
    const stored=await page.evaluate(()=>JSON.parse(localStorage.getItem('pwd-week5-submissions')));
    assert.equal(stored[0].status,'pending');
    assert.equal(stored[0].recommendedMenu.length,2);
    await page.reload();
    assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('pwd-week5-submissions')).length),1);
    console.log('Captured 3 app screens; filter, empty state, missing ID, validation, save, menu normalization, and reload checks passed.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});
