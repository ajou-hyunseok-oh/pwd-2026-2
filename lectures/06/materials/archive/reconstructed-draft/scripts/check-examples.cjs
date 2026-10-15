// Execute the actual generated slide code, then verify browser fetch/CORS behavior.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const {createRequire} = require('node:module');
const {execFileSync} = require('node:child_process');
const {once} = require('node:events');
const http = require('node:http');
const root = path.resolve(__dirname, '..');
const requireExample = createRequire(path.join(root, 'examples/package.json'));
const express = requireExample('express');
const {createApp} = requireExample('./src/app.cjs');
const {createFoodModel} = requireExample('./src/models/food-model.cjs');
const output = process.env.REVIEW_OUTPUT || path.join(os.tmpdir(), 'pwd-lecture-06/review');
const sandbox = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root, 'lecture-content.js'), 'utf8'), sandbox);
const messages = sandbox.window.LECTURE_CONTENT;
const map = JSON.parse(fs.readFileSync(path.join(root, 'materials/slide-map.json'), 'utf8'));
const results = [];
function code(id) {
  const row = map.find(row => row.id === 'concept-' + id);
  assert.ok(row, id);
  const key = Object.keys(messages.ko).find(key => key.startsWith(`w6_${String(row.number).padStart(2,'0')}_b`) && key.endsWith('_code'));
  assert.ok(key, id + ': missing example');
  assert.equal(messages.ko[key], messages.en[key], id + ': code differs by language');
  return messages.ko[key];
}
function passed(name) { results.push({name, passed:true}); }
function runNode(id, expected) {
  const actual = execFileSync(process.execPath, ['--eval', code(id)], {encoding:'utf8'}).trim();
  assert.equal(actual, expected, id);
  passed(id);
}
const servers = [];
async function listen(app) {
  const server = app.listen(0, '127.0.0.1');
  servers.push(server);
  await once(server, 'listening');
  return `http://127.0.0.1:${server.address().port}`;
}
async function fragment(id, {json=false}={}) {
  const snippet = code(id);
  const prefix = "const express = require('express'); const app = express();" + (json ? 'app.use(express.json());' : '');
  const app = new Function('require', 'console', prefix + '\n' + snippet + '\nreturn app;')(requireExample, {log(){}});
  return listen(app);
}
async function standaloneServer(id) {
  let captured;
  const wrapped = () => {
    const app = express();
    app.listen = () => {
      captured = express.application.listen.call(app, 0, '127.0.0.1');
      servers.push(captured);
      return captured;
    };
    return app;
  };
  new Function('require', 'console', code(id))(name => name === 'express' ? wrapped : requireExample(name), console);
  await once(captured, 'listening');
  return `http://127.0.0.1:${captured.address().port}`;
}

(async () => {
  let browser;
  try {
    runNode('nodejs', 'Hello, Node.js');
    runNode('event-loop', 'A\nC\nB');
    runNode('json-transform', 'string\nCampus Noodles');
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'pwd-week6-modules-'));
    try {
      const [greeting, main] = code('commonjs').split('// main.cjs');
      fs.writeFileSync(path.join(directory, 'greeting.cjs'), greeting.replace('// greeting.cjs', ''));
      fs.writeFileSync(path.join(directory, 'main.cjs'), main);
      assert.equal(execFileSync(process.execPath, [path.join(directory, 'main.cjs')], {encoding:'utf8'}).trim(), 'Hello, Ajou');
      passed('commonjs');
    } finally { fs.rmSync(directory, {recursive:true, force:true}); }

    const hello = await standaloneServer('hello-server');
    assert.equal(await (await fetch(hello)).text(), 'Hello World!');
    passed('hello-server');
    const failed = await standaloneServer('async-handler');
    const failure = await fetch(failed + '/fail');
    assert.equal(failure.status, 500);
    assert.deepEqual(await failure.json(), {error:'Unavailable'});
    passed('async-handler');

    const routes = await fragment('express-routing');
    assert.deepEqual(await (await fetch(routes + '/foods')).json(), [{id:1,name:'Campus Noodles'}]);
    assert.equal((await fetch(routes + '/foods', {method:'POST'})).status, 201);
    passed('express-routing');
    const params = await fragment('path-params');
    assert.deepEqual(await (await fetch(params + '/foods/7')).json(), {receivedId:'7'});
    passed('path-params');
    const query = await fragment('query');
    for (const [url, expected] of [['/foods?q=rice','rice'], ['/foods',''], ['/foods?q=a&q=b','']]) {
      assert.deepEqual(await (await fetch(query + url)).json(), {query:expected});
    }
    passed('query');
    const logging = await fragment('middleware');
    assert.deepEqual(await (await fetch(logging + '/health')).json(), {status:'ok'});
    passed('middleware-next');
    const json = await fragment('json-body');
    const echoed = await fetch(json + '/echo', {method:'POST', headers:{'Content-Type':'application/json'}, body:'{"name":"Rice"}'});
    assert.deepEqual(await echoed.json(), {name:'Rice'});
    passed('json-body');
    const validation = await fragment('input-validation', {json:true});
    for (const [body, status] of [[{},400], [{name:' '},400], [{name:42},400], [{name:' Rice '},201]]) {
      const response = await fetch(validation + '/foods', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
      assert.equal(response.status, status);
      if (status === 201) assert.deepEqual(await response.json(), {name:'Rice'});
    }
    passed('input-validation');

    // Reproduce Red/Green/Refactor against the same blank-name requirement.
    const serviceSource = fs.readFileSync(path.join(root, 'examples/src/services/food-service.cjs'), 'utf8');
    const validationSource = /    if \(typeof input\?\.name[\s\S]*?\n    }\n/;
    assert.match(serviceSource, validationSource);
    const loadService = source => {
      const context = {module:{exports:{}}};
      vm.runInNewContext(source, context);
      return context.module.exports.createFoodService(createFoodModel());
    };
    const red = loadService(serviceSource.replace(validationSource, ''));
    let rejected = false;
    try { await red.addFood({name:' '}); } catch { rejected = true; }
    assert.equal(rejected, false, 'Red: missing validation must violate the rejection requirement');
    for (const source of [serviceSource, serviceSource.replace('!input.name.trim()', 'input.name.trim().length === 0')]) {
      await assert.rejects(loadService(source).addFood({name:' '}), error => error.status === 400);
    }
    passed('tdd-red-green-refactor');

    const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
    const web = http.createServer((req,res) => { res.writeHead(200, {'Content-Type':'text/html'}); res.end('<!doctype html><title>API check</title>'); });
    const origin = await listen(web);
    const api = await listen(createApp({origin}));
    const blockedApi = await listen(createApp({origin:'http://different.example'}));
    browser = await chromium.launch({channel:'chrome',headless:true});
    const page = await browser.newPage();
    await page.goto(origin);
    const source = code('frontend-api').replace('http://localhost:3000', api);
    const foodList = await page.evaluate(async source => {
      const received = [], errors = [];
      // Preserve the slide's final invocation while observing its console handlers.
      await new Function('console', source.replace('loadFoods().then', 'return loadFoods().then'))({log:value => received.push(value),error:error => errors.push(error.message)});
      return {received, errors};
    }, source);
    assert.deepEqual(foodList, {received:[[{id:1,name:'Campus Noodles'}]],errors:[]});
    const created = await page.evaluate(async api => {
      const response = await fetch(api + '/foods', {method:'POST',headers:{'Content-Type':'application/json'},body:'{"name":"Browser Rice"}'});
      return {status:response.status,food:await response.json()};
    }, api);
    assert.equal(created.status, 201);
    assert.equal(created.food.name, 'Browser Rice');
    const corsBlocked = await page.evaluate(async api => {
      try { await fetch(api + '/foods'); return false; } catch { return true; }
    }, blockedApi);
    assert.equal(corsBlocked, true);
    // An HTTP 404 fulfills fetch; the slide explicitly turns it into a failure.
    const error = await page.evaluate(async source => {
      const errors = [];
      await new Function('console', source.replace('loadFoods().then', 'return loadFoods().then'))({log(){},error:error => errors.push(error.message)});
      return errors;
    }, source.replace('/foods', '/missing'));
    assert.deepEqual(error, ['HTTP 404']);
    passed('browser-fetch-preflight-cors-and-http-error');

    fs.mkdirSync(output, {recursive:true});
    fs.writeFileSync(path.join(output,'examples.json'), JSON.stringify({results},null,2));
    console.log(JSON.stringify({checks:results.length, results, output},null,2));
  } finally {
    if (browser) await browser.close();
    await Promise.all(servers.map(server => new Promise(resolve => server.close(resolve))));
  }
})().catch(error => { console.error(error); process.exitCode=1; });
