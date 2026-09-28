const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const second = process.env.PERIOD === '2';
const slideCount = second ? 30 : 24;
const deckFile = second ? 'ai-design.html' : 'index.html';
const contentFile = second ? 'period-2-content.js' : 'lecture-content.js';
const root = path.resolve(__dirname, '..');
const output = process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-outline-review-' + (second ? '2' : '1'));
fs.mkdirSync(output, {recursive:true});
const sandbox = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,contentFile),'utf8'),sandbox);
const messages = sandbox.window.LECTURE_CONTENT;
const html = fs.readFileSync(path.join(root,deckFile),'utf8');
for(const [,key] of html.matchAll(/data-wd-i18n(?:-alt|-aria-label|-title)?="([^"]+)"/g)) {
 for(const locale of ['ko','en']) assert.ok(messages[locale][key] || key==='page_title', `${locale}.${key}`);
 assert.doesNotMatch(messages.ko[key] || '',/(?:니다|세요|십시오|는가|인가|을까|일까|하면|다면)(?:[.!?…]|$)/u, key);
}
(async()=>{
 const browser = await chromium.launch({channel:'chrome',headless:true});
 const errors=[]; const issues=[];
 try {
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
  await page.goto((process.env.DECK_URL || 'http://127.0.0.1:4304')+'/lectures/04/'+deckFile);
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('[data-wd-slide]').count(),slideCount);
  for(const locale of ['ko','en']) {
   await page.emulateMedia({media:'screen'});
   await page.click(`[data-locale="${locale}"]`);
   await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
   for(const mode of ['screen','print']) {
    await page.emulateMedia({media:mode});
    const found=await page.evaluate(()=>{
     const problems=[];const deck=document.querySelector('[data-web-deck]').__webDeck;
     [...document.querySelectorAll('[data-wd-slide]')].forEach((s,i)=>{
      deck.goTo(i);const box=s.getBoundingClientRect(), contentBottom=box.bottom-20;
      for(const el of s.querySelectorAll('h1,h2,h3,h4,p,li,blockquote,table,pre,img,.week4-body,.week4-wire,.react-demo,.react-explanation,.react-concepts dt,.react-concepts dd,.design-concepts dt,.design-concepts dd,.design-sequences,.design-wire,.design-onepager,.week4-table [role="cell"],.week4-table [role="rowheader"]')) {
       const r=el.getBoundingClientRect();if(!r.width)continue;
       if(r.bottom>contentBottom-6 || r.left<box.left-1||r.right>box.right+1||el.scrollWidth>el.clientWidth+2)
        problems.push({slide:i+1,type:'bounds',tag:el.tagName,text:el.textContent.slice(0,60),bottom:r.bottom-box.top,contentBottom:contentBottom-box.top});
      }
     });return problems;
    });
    issues.push(...found.map(x=>({locale,mode,...x})));
    if(mode==='print') {
     await page.pdf({path:path.join(output,`${locale}.pdf`),preferCSSPageSize:true,printBackground:true});
     // Capture the real presentation view at its 1280×720 slide size.
     await page.emulateMedia({media:'screen'});
     await page.setViewportSize({width:1312,height:818});
     for(let i=0;i<slideCount;i++) {
      await page.evaluate(index=>document.querySelector('[data-web-deck]').__webDeck.goTo(index),i);
      await page.evaluate(()=>document.fonts.ready);
      await page.locator('[data-wd-slide]').nth(i).screenshot({path:path.join(output,`${locale}-${String(i+1).padStart(2,'0')}.png`)});
     }
    }
   }
  }
  await page.emulateMedia({media:'screen'});await page.setViewportSize({width:390,height:844});
  for(const locale of ['ko','en']) {
   await page.emulateMedia({media:'screen'});
   await page.click(`[data-locale="${locale}"]`);
   await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
   for(let i=0;i<slideCount;i++) {
    const mobile=await page.evaluate(i=>{
     document.querySelector('[data-web-deck]').__webDeck.goTo(i);
     const slide=document.querySelectorAll('[data-wd-slide]')[i];
     return {
      overflow:document.documentElement.scrollWidth>innerWidth
     };
    },i);
    if(mobile.overflow)issues.push({locale,mode:'mobile',slide:i+1,type:'horizontal-overflow'});
   }
  }
  fs.writeFileSync(path.join(output,'audit.json'),JSON.stringify({slides:slideCount,errors,issues},null,2));
  console.log(JSON.stringify({slides:slideCount,errors,issues,output},null,2));
  process.exitCode=errors.length||issues.length?1:0;
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
