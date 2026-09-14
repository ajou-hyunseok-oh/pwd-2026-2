const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'C:/Users/hsoh/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const out = path.join(process.env.TEMP || '.', 'week2-slide-audit');
fs.mkdirSync(out, { recursive: true });
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(process.env.DECK_URL || 'http://127.0.0.1:4186/lectures/02/');
  const slideCount=await page.locator('[data-wd-slide]').count();
  await page.evaluate(()=>document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  const results={};
  for (const locale of ['ko','en']) {
    await page.evaluate(locale=>document.querySelector('[data-web-deck]').__webDeck.setLocale(locale),locale);
    await page.waitForTimeout(200);
    results[locale]=await page.evaluate(()=>[...document.querySelectorAll('[data-wd-slide]')].map((slide,i)=>{
      const r=slide.getBoundingClientRect(),footer=slide.querySelector(':scope > .week2-reference--footer');
      const limit=footer?footer.getBoundingClientRect().top-8:r.bottom-(slide.classList.contains('lesson-original-slide')?0:20);
      const body=[...slide.children].filter(el=>el!==footer);
      const bottom=Math.max(...body.map(el=>el.getBoundingClientRect().bottom));
      const over=[];
      slide.querySelectorAll('pre').forEach(pre=>{if(pre.scrollWidth>pre.clientWidth+2)over.push({key:pre.dataset.wdI18n,width:pre.clientWidth,scroll:pre.scrollWidth});});
      const missingMarks=[...slide.querySelectorAll('[data-lesson-marks]')].flatMap(el=>JSON.parse(el.dataset.lessonMarks).filter(mark=>!el.textContent.includes(mark[1])).map(mark=>({key:el.dataset.wdI18n,mark})));
      return {n:i+1,id:slide.dataset.wdSlide,overflow:Math.round(bottom-limit),codeOverflow:over,missingMarks,missingImages:[...slide.querySelectorAll('img')].filter(img=>!img.complete||!img.naturalWidth).map(img=>img.getAttribute('src')),codeFont:[...new Set([...slide.querySelectorAll('.wd-code')].map(el=>getComputedStyle(el).fontSize))]};
    }));
    for(let n=1;n<=slideCount;n++)await page.locator('[data-wd-slide]').nth(n-1).screenshot({path:path.join(out,`${locale}-${String(n).padStart(2,'0')}.png`)});
    await page.pdf({path:path.join(out,`lecture-02-${locale}.pdf`),width:'1280px',height:'720px',printBackground:true,preferCSSPageSize:true});
  }
  await page.evaluate(()=>document.querySelector('[data-web-deck]').__webDeck.setLocale('ko'));
  await page.emulateMedia({media:'screen'});
  const desktop=[];
  for(const locale of ['ko','en']){
    await page.evaluate(locale=>document.querySelector('[data-web-deck]').__webDeck.setLocale(locale),locale);
    await page.waitForTimeout(50);
    const rows=await page.evaluate(()=>[...document.querySelectorAll('[data-wd-slide]')].map((slide,i)=>{
      const footer=slide.querySelector(':scope > .week2-reference--footer');
      const bottom=Math.max(...[...slide.children].filter(el=>el!==footer).map(el=>el.getBoundingClientRect().bottom));
      return {n:i+1,overflow:footer?Math.round(bottom-footer.getBoundingClientRect().top):0};
    }).filter(row=>row.overflow>0));
    desktop.push(...rows.map(row=>({locale,...row})));
  }
  await page.evaluate(()=>document.querySelector('[data-web-deck]').__webDeck.goTo(3));
  const demo=page.locator('[data-week2-demo] [aria-live]');
  const before=await demo.textContent();
  await page.locator('[data-week2-demo-toggle]').click();
  if(await demo.textContent()===before)errors.push('Slide 04 demo did not change');
  await page.setViewportSize({width:390,height:844});
  const mobile=[];
  for(const locale of ['ko','en']){
    await page.evaluate(locale=>document.querySelector('[data-web-deck]').__webDeck.setLocale(locale),locale);
    for(let i=0;i<slideCount;i++){
      await page.evaluate(i=>document.querySelector('[data-web-deck]').__webDeck.goTo(i),i);
      const bad=await page.locator('[data-wd-slide]').nth(i).evaluate(el=>({scroll:el.scrollWidth,width:el.clientWidth}));
      if(bad.scroll>bad.width+2)mobile.push({locale,n:i+1,...bad});
    }
  }
  const issues=Object.fromEntries(Object.entries(results).map(([locale,rows])=>[locale,rows.filter(row=>row.overflow>0||row.codeOverflow.length||row.missingImages.length||row.missingMarks.length)]));
  fs.writeFileSync(path.join(out,'audit.json'),JSON.stringify({results,errors,desktop,mobile},null,2));
  console.log(JSON.stringify({out,errors,desktop,mobile,issues},null,2));
  if(errors.length||desktop.length||mobile.length||Object.values(issues).some(rows=>rows.length))process.exitCode=1;
  await browser.close();
})().catch(error=>{console.error(error);process.exitCode=1;});
