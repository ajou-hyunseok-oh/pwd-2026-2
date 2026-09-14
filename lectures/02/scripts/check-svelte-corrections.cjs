const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict');
const {createRequire}=require('node:module');
const practice=process.env.SVELTE_PRACTICE_ROOT||path.resolve(__dirname,'../../../../pwd-2026-practices/pwd-week2');
const req=createRequire(path.join(practice,'package.json'));
const {compile}=req('svelte/compiler');
const esbuild=req('esbuild');
const {chromium}=req('playwright');
const {examples}=require('./svelte-corrections.cjs');
const names=Object.keys(examples).filter(k=>examples[k].includes('<script'));
const out=fs.mkdtempSync(path.join(os.tmpdir(),'week2-svelte-check-'));
(async()=>{
  const result=await esbuild.build({stdin:{contents:`import {mount,unmount} from 'svelte';\n`+
    names.map(n=>`import ${n} from 'example:${n}';`).join('\n')+
    `\nconst components={${names.join(',')}};let active;window.show=async(name,props={})=>{if(active)await unmount(active);active=mount(components[name],{target:document.body,props});};`,
    resolveDir:practice,sourcefile:'checks.js'},bundle:true,write:false,format:'iife',platform:'browser',conditions:['browser'],plugins:[{
      name:'examples',setup(build){
        build.onResolve({filter:/^example:/},args=>({path:args.path.slice(8),namespace:'svelte-example'}));
        build.onResolve({filter:/^\$lib\/Card.svelte$/},()=>({path:path.join(practice,'src/lib/Card.svelte'),namespace:'svelte-card'}));
        const compileSource=(source,filename)=>{
          const result=compile(source,{filename,generate:'client',dev:true});
          assert.deepEqual(result.warnings.map(w=>w.code),[],filename);
          return {contents:result.js.code,loader:'js',resolveDir:practice};
        };
        build.onLoad({filter:/.*/,namespace:'svelte-example'},args=>compileSource(examples[args.path],args.path+'.svelte'));
        build.onLoad({filter:/.*/,namespace:'svelte-card'},args=>compileSource(fs.readFileSync(args.path,'utf8'),'Card.svelte'));
      }
    }]});
  fs.writeFileSync(path.join(out,'checks.js'),result.outputFiles[0].text);
  // Exercise the actual API/load snippets without changing the practice repository.
  const json=data=>new Response(JSON.stringify(data),{headers:{'content-type':'application/json'}});
  const error=(status,message)=>{throw Object.assign(new Error(message),{status});};
  const GET=new Function('json',examples.api.replace(/^import.*\n/,'').replace('export function','function')+'\nreturn GET;')(json);
  const load=new Function('error',examples.projectsLoad.replace(/^import.*\n/,'').replace('export async function','async function')+'\nreturn load;')(error);
  const data=await load({fetch:async url=>{assert.equal(url,'/api/projects');return GET();}});
  assert.equal(data.projects.length,3);
  await assert.rejects(load({fetch:async()=>new Response('',{status:500})}),e=>e.status===500);
  const routeLoad=new Function(examples.routeLoad.replace('export function','function')+'\nreturn load;')();
  assert.deepEqual(routeLoad({params:{id:'42'}}),{id:'42'});
  const browser=await chromium.launch({channel:'chrome',headless:true});
  try {
    const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto('about:blank');await page.addScriptTag({content:result.outputFiles[0].text});
    for(const name of ['counterJS','counterTS']){
      await page.evaluate(name=>window.show(name),name);await page.getByRole('button').click();
      assert.equal((await page.getByRole('button').textContent()).trim(),'clicks: 1');
      await page.getByRole('textbox').fill('Svelte');assert.equal(await page.locator('h1').textContent(),'Hello Svelte!');
    }
    await page.evaluate(()=>window.show('grade'));
    for(const [score,grade] of [[95,'A'],[70,'B'],[40,'C']]){
      await page.getByRole('spinbutton').fill(String(score));assert.match(await page.locator('p').textContent(),new RegExp('\\('+grade+'\\)'));
    }
    await page.evaluate(()=>window.show('binding'));
    await page.getByRole('textbox').fill('Test');assert.equal(await page.locator('p').nth(0).textContent(),'Test');
    await page.getByRole('checkbox').check();assert.equal(await page.locator('p').nth(1).textContent(),'Yes');
    await page.getByRole('combobox').selectOption('blue');assert.equal(await page.locator('p').nth(2).textContent(),'blue');
    await page.getByRole('slider').fill('75');assert.match(await page.getByRole('slider').locator('..').textContent(),/75/);
    await page.locator('input[type=file]').setInputFiles({name:'sample.txt',mimeType:'text/plain',buffer:Buffer.from('test')});
    assert.equal(await page.locator('p').last().textContent(),'1 files');
    await page.evaluate(()=>{const old=window.clearInterval;window.cleared=0;window.clearInterval=id=>{window.cleared++;return old(id);};return window.show('lifecycle');});
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent==='1');
    await page.evaluate(data=>window.show('routePage',{data}),routeLoad({params:{id:'42'}}));
    assert.equal(await page.locator('h1').textContent(),'Blog post #42');assert.equal(await page.evaluate(()=>window.cleared),1);
    await page.evaluate(data=>window.show('projectsPage',{data}),data);assert.equal(await page.locator('article').count(),3);
    assert.equal(await page.locator('article a').first().getAttribute('href'),'/projects/timetable');
    assert.deepEqual(errors,[]);
  } finally {await browser.close();}
  console.log(`Svelte ${req('svelte/package.json').version}: 7 components compile without warnings; counters, grades, bindings, timer cleanup, route data and API-to-page flow passed.`);
})().catch(e=>{console.error(e.message,e.frame||'');process.exitCode=1;});
