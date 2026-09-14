const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH || 'C:/Users/hsoh/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
(async()=>{
  const browser=await chromium.launch({channel:'chrome',headless:true});
  try {
    for(const locale of ['ko','en'])for(const [kind,width] of [['mobile',390],['tablet',820]]) {
      const page=await browser.newPage({viewport:{width,height:660},deviceScaleFactor:1});
      await page.goto(pathToFileURL(path.resolve(__dirname,'../examples/portfolio',locale==='en'?'en/about.html':'about.html')).href);
      await page.evaluate(()=>document.fonts.ready);
      await page.screenshot({path:path.resolve(__dirname,`../materials/figures/${locale}-devtools-viewport-${kind}.png`)});
      await page.close();
    }
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
