const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'C:/Users/hsoh/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const out = path.resolve(__dirname, '../materials/figures');
const base = process.env.EXAMPLE_URL || 'http://localhost:4183';
fs.mkdirSync(out, { recursive: true });
const save = (name, data) => fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,2));
(async () => {
  const browser = await chromium.launch({channel:'chrome',headless:true,args:['--remote-debugging-port=9241','--remote-allow-origins=devtools://devtools']});
  try {
    const page = await browser.newPage({viewport:{width:900,height:680},deviceScaleFactor:1});
    const observations = {browser:browser.version(),base,capturedAt:new Date().toISOString(),locales:{}};
    const shot = async (name, selector='main') => page.locator(selector).screenshot({path:path.join(out,name+'.png')});
    for (const locale of ['ko','en']) {
      const sub = locale==='en'?'en/':'';
      const record = observations.locales[locale]={};
      for (const name of ['index','about','projects']) {
        await page.goto(`${base}/portfolio/${sub}${name}.html`);
        await shot(`${locale}-${name}`,'body');
        if(name==='about') {
          await shot(`${locale}-intro-before`,'.profile');
          record.introBefore = await page.locator('#intro').textContent();
          await page.locator('#change').click();
          await shot(`${locale}-intro-after`,'.profile');
          record.introAfter = await page.locator('#intro').textContent();
          const cdp=await page.context().newCDPSession(page);
          const {nodes}=await cdp.send('Accessibility.getFullAXTree');
          record.accessibility=nodes.filter(n=>['button','paragraph'].includes(n.role?.value)).map(n=>({role:n.role.value,name:n.name?.value||'',properties:n.properties}));
          await cdp.detach();
        }
        if(name==='projects') {
          await shot(`${locale}-add-before`,'#updates');
          await page.locator('#add').click();
          await shot(`${locale}-add-after`,'#updates');
        }
      }
      await page.goto(`${base}/rendering/${sub}index.html`);
      record.layout=await page.locator('.profile').evaluate(el=>{
        const r=el.getBoundingClientRect(),b=el.querySelector('#change').getBoundingClientRect(),p=el.querySelector('p').getBoundingClientRect();
        return {x:r.x,y:r.y,width:r.width,height:r.height,padding:24,contentWidth:r.width-48,button:{x:b.x-r.x,y:b.y-r.y,width:b.width,height:b.height},paragraph:{x:p.x-r.x,y:p.y-r.y,width:p.width,height:p.height}};
      });
      await shot(`${locale}-layout-before`,'.profile');
      const cdp=await page.context().newCDPSession(page);
      const events=[];
      cdp.on('Tracing.dataCollected',data=>events.push(...data.value));
      await cdp.send('Tracing.start',{categories:'devtools.timeline,blink.user_timing,disabled-by-default-devtools.timeline',transferMode:'ReportEvents'});
      await page.locator('#width').click();
      await page.waitForTimeout(150);
      await shot(`${locale}-layout-after`,'.profile');
      record.narrow=await page.locator('.profile').evaluate(el=>({width:el.getBoundingClientRect().width,buttonY:el.querySelector('#change').getBoundingClientRect().y-el.getBoundingClientRect().y}));
      await page.locator('#color').click();
      await page.waitForTimeout(150);
      const complete=new Promise(resolve=>cdp.once('Tracing.tracingComplete',resolve));
      await cdp.send('Tracing.end');await complete;
      await shot(`${locale}-color-after`,'.profile');
      save(`${locale}-rendering.trace.json`,{traceEvents:events});
      const widthMark=events.find(e=>e.name==='change-width'),colorMark=events.find(e=>e.name==='change-background');
      record.rendering=events.filter(e=>['Layout','Paint','UpdateLayoutTree'].includes(e.name)&&e.ts>=widthMark.ts).map(e=>({name:e.name,change:e.ts<colorMark.ts?'width':'background',startMs:(e.ts-widthMark.ts)/1000,durationMs:(e.dur||0)/1000}));
      await cdp.detach();
      await page.goto(`${base}/rendering/${sub}cascade.html`);
      record.computed=await page.locator('#intro').evaluate(el=>({color:getComputedStyle(el).color,font:getComputedStyle(el).font,html:el.outerHTML}));
      await shot(`${locale}-cascade`,'.profile');
      for(const reserved of ['unreserved','reserved']) {
        await page.goto(`${base}/rendering/${sub}image-${reserved}.html`);
        await shot(`${locale}-image-${reserved}-before`,'.measure');
        const before=await page.locator('.measure p').boundingBox();
        await page.locator('#load').click();
        await page.waitForFunction(()=>document.querySelector('#hero').naturalWidth>0);
        await shot(`${locale}-image-${reserved}-after`,'.measure');
        const after=await page.locator('.measure p').boundingBox();
        record[reserved]={beforeY:before.y,afterY:after.y,deltaY:after.y-before.y};
      }
      record.generation={};
      for(const mode of ['csr','ssr','ssg']) {
        const response=await page.goto(`${base}/generation/${sub}${mode}.html`);
        const html=await response.text();
        record.generation[mode]={html,initialIntro:(html.match(/<p id="intro">(.*?)<\/p>/)||[])[1],domIntro:await page.locator('#intro').textContent()};
        await shot(`${locale}-${mode}`,'.profile');
      }
      const requests=[];
      const onRequest=request=>{if(request.resourceType()==='document')requests.push(request.url());};
      page.on('request',onRequest);
      await page.goto(`${base}/portfolio/${sub}index.html`);
      requests.length=0;
      await page.locator('nav a').nth(1).click();
      record.mpa={documents:[...requests],url:page.url()};
      await page.goto(`${base}/routing/${sub}index.html`);
      await shot(`${locale}-spa-before`,'body');
      requests.length=0;
      await page.locator('nav a').nth(1).click();
      await shot(`${locale}-spa-after`,'body');
      record.spa={documents:[...requests],url:page.url(),content:await page.locator('#page').textContent()};
      page.off('request',onRequest);
    }
    await page.goto('http://127.0.0.1:4175');
    await page.locator('.card').nth(1).waitFor();
    await shot('react-cards');
    observations.nodeOutput=execFileSync(process.execPath,[path.resolve(__dirname,'../examples/portfolio/demo.js')],{encoding:'utf8'}).trim();
    observations.nodeVersion=process.version;
    save('observations.json',observations);

    // Actual Chrome DevTools frontend connected to the same running examples.
    await page.goto(base+'/portfolio/about.html');
    const targets=await(await fetch('http://127.0.0.1:9241/json')).json();
    const target=targets.find(t=>t.url===base+'/portfolio/about.html');
    const devtools=await browser.newPage({viewport:{width:1100,height:420},deviceScaleFactor:1});
    await devtools.goto('devtools://devtools/bundled/inspector.html?ws='+target.webSocketDebuggerUrl.replace('ws://',''));
    await devtools.getByRole('button',{name:'Toggle screencast',exact:true}).waitFor();
    await devtools.getByRole('button',{name:'Toggle screencast',exact:true}).click();
    const cdp=await page.context().newCDPSession(page);
    for(const locale of ['ko','en']) {
      const sub=locale==='en'?'en/':'';
      await page.goto(`${base}/rendering/${sub}cascade.html`);
      await devtools.bringToFront();
      await devtools.getByRole('tab',{name:'Console',exact:true}).click();
      await devtools.getByRole('textbox',{name:'Console prompt',exact:true}).click();
      await devtools.keyboard.type('inspect(document.querySelector("#intro"))');
      await devtools.keyboard.press('Enter');
      await devtools.getByRole('tab',{name:'Elements',exact:true}).click();
      await devtools.waitForTimeout(300);
      await devtools.screenshot({path:path.join(out,`${locale}-devtools-elements.png`),clip:{x:0,y:0,width:1100,height:270}});
      await devtools.getByRole('tab',{name:'Computed',exact:true}).click();
      await devtools.getByRole('textbox',{name:'Filter',exact:true}).fill('color');
      await devtools.waitForTimeout(150);
      await devtools.screenshot({path:path.join(out,`${locale}-devtools-computed.png`)});
      await devtools.screenshot({path:path.join(out,`${locale}-devtools-computed-detail.png`),clip:{x:775,y:250,width:325,height:75}});
      await devtools.getByRole('textbox',{name:'Filter',exact:true}).fill('');
      await devtools.getByRole('tab',{name:'Styles',exact:true}).click();
    }
    await devtools.getByRole('tab',{name:'Network',exact:true}).click();
    await devtools.waitForTimeout(1000);
    await devtools.getByRole('option',{name:'Doc',exact:true}).click();
    for(const locale of ['ko','en']) {
      const sub=locale==='en'?'en/':'';
      await page.goto(`${base}/generation/${sub}csr.html`);
      await devtools.bringToFront();
      await devtools.waitForTimeout(1000);
      // Network request names are painted into a canvas by this Chrome version.
      // The Doc filter leaves the single document row immediately below the header.
      await devtools.mouse.click(100,200);
      await devtools.getByRole('tab',{name:'Response',exact:true}).click();
      await devtools.locator('.cm-scroller').evaluateAll(elements => elements.forEach(element => {
        if(element.getBoundingClientRect().height) element.scrollTop = 150;
      }));
      await devtools.waitForTimeout(250);
      await devtools.screenshot({path:path.join(out,`${locale}-devtools-network.png`),clip:{x:0,y:155,width:1100,height:250}});
    }
    await devtools.getByRole('tab',{name:'Console',exact:true}).click();
    await cdp.send('Runtime.evaluate',{expression:'console.clear();'});
    await devtools.getByRole('textbox',{name:'Console prompt',exact:true}).click();
    await devtools.keyboard.type('const projects = ["Timetable", "Memo"]; console.log(projects.length);');
    await devtools.keyboard.press('Enter');
    await devtools.waitForTimeout(200);
    await devtools.screenshot({path:path.join(out,'devtools-console.png'),clip:{x:0,y:0,width:1100,height:210}});
    await devtools.getByRole('tab',{name:'Performance',exact:true}).click();
    const inputs=devtools.locator('input[type="file"]');
    await inputs.first().setInputFiles(path.join(out,'ko-rendering.trace.json'));
    await devtools.waitForTimeout(1000);
    const closeTips = devtools.getByRole('button',{name:'Close',exact:true});
    if(await closeTips.count()) await closeTips.last().click();
    await devtools.waitForTimeout(200);
    await devtools.getByRole('button',{name:'Hide sidebar',exact:true}).click();
    const summaryTab = await devtools.getByRole('tab',{name:'Summary',exact:true}).boundingBox();
    await devtools.mouse.move(600,summaryTab.y-3);
    await devtools.mouse.down();
    await devtools.mouse.move(600,330,{steps:12});
    await devtools.mouse.up();
    await devtools.waitForTimeout(200);
    await devtools.screenshot({path:path.join(out,'devtools-performance.png')});
    await cdp.detach();
    console.log('Captured bilingual screenshots, Chrome DevTools and actual rendering/network/AX observations.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
