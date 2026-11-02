// Query disposable processes of the actual Week 6 TypeScript API. No external services.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { spawn, execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const serverRoot = process.env.SERVER_ROOT || path.resolve(root, '../../../..', 'pwd-week6');
const files = ['README.md', 'package.json', 'package-lock.json', 'server.ts', 'scripts/copy-data.ts',
  'src/app.ts', 'src/routes/restaurants.routes.ts', 'src/controllers/restaurants.controller.ts',
  'src/services/restaurants.service.ts', 'src/models/restaurant.model.ts', 'src/data/restaurants.json',
  'src/middleware/error.middleware.ts', 'src/middleware/notFound.middleware.ts',
  'src/utils/asyncHandler.ts', 'src/utils/httpError.ts', 'src/types/restaurant.types.ts', 'src/types/api.types.ts',
  'tests/restaurants.routes.test.ts'];
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(path.join(serverRoot, file))).digest('hex');
const sourceFiles = files.map(file => ({ file, sha256: hash(file) }));
const requests = {}, children = [];

function start() {
  return new Promise((resolve, reject) => {
    // tsx loads the source, avoiding reliance on a potentially stale dist build.
    const loader = require.resolve('tsx/cjs', { paths: [serverRoot] });
    const child = spawn(process.execPath, ['--require', loader, '-e',
      "const app=require('./src/app.ts').default();const server=app.listen(0,'127.0.0.1',()=>console.log(JSON.stringify({port:server.address().port})));"],
      { cwd: serverRoot, env: { ...process.env, NODE_ENV: 'production' }, stdio: ['ignore', 'pipe', 'pipe'] });
    children.push(child);
    let stdout = '', stderr = '', ready = false;
    const timeout = setTimeout(() => { child.kill(); reject(new Error('API startup timeout: ' + stderr)); }, 15000);
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', error => { clearTimeout(timeout); reject(error); });
    child.on('exit', code => { if (!ready) { clearTimeout(timeout); reject(new Error('API exited ' + code + ': ' + stderr)); } });
    child.stdout.on('data', chunk => {
      stdout += chunk;
      if (!stdout.includes('\n') || ready) return;
      try {
        const { port } = JSON.parse(stdout.split('\n')[0]);
        ready = true; clearTimeout(timeout);
        resolve({ child, url: 'http://127.0.0.1:' + port });
      } catch (error) { clearTimeout(timeout); reject(error); }
    });
  });
}

async function stop(child) {
  if (child.exitCode !== null) return;
  const done = new Promise(resolve => child.once('exit', resolve));
  child.kill('SIGTERM');
  await done;
}

async function request(server, id, method, route, body) {
  const response = await fetch(server.url + route, { method,
    headers: { Origin: 'http://localhost:5173', ...(body ? { 'Content-Type': 'application/json' } : {}) },
    ...(body ? { body: JSON.stringify(body) } : {}) });
  const json = await response.json();
  requests[id] = { method, route, ...(body ? { body } : {}), status: response.status,
    cors: response.headers.get('access-control-allow-origin'), response: json };
  return requests[id];
}

(async () => {
  try {
    const first = await start();
    assert.deepEqual((await request(first, 'health', 'GET', '/health')).response, { status: 'ok' });
    assert.equal(requests.health.status, 200);
    const list = await request(first, 'list', 'GET', '/api/restaurants');
    assert.equal(list.status, 200); assert.equal(list.cors, '*');
    assert.equal(list.response.data.length, 3);
    const sync = await request(first, 'sync', 'GET', '/api/restaurants/sync-demo');
    assert.equal(sync.response.meta.execution, 'synchronous');
    assert.deepEqual(sync.response.data, list.response.data);
    const popular = await request(first, 'popular', 'GET', '/api/restaurants/popular?limit=2');
    assert.deepEqual(popular.response.data.map(r => r.id), [1, 2]);
    assert.deepEqual(popular.response.data.map(r => r.rating), [4.99, 4.92]);
    const invalid = await request(first, 'invalid', 'POST', '/api/restaurants', { name: '테스트' });
    assert.equal(invalid.status, 400); assert.equal(invalid.response.error.message, "'category' is required");
    const missing = await request(first, 'missing', 'GET', '/api/restaurants/999');
    assert.equal(missing.status, 404);
    const unknown = await request(first, 'not-found', 'GET', '/unknown');
    assert.equal(unknown.status, 404);
    const created = await request(first, 'created', 'POST', '/api/restaurants', {
      name: '아주대 실습 식당', category: '한식', location: '아주대 정문', recommendedMenu: '김밥, 라면, '
    });
    assert.equal(created.status, 201); assert.equal(created.response.data.id, 4);
    assert.deepEqual(created.response.data.recommendedMenu, ['김밥', '라면']);
    const shared = await request(first, 'shared', 'GET', '/api/restaurants/4');
    assert.deepEqual(shared.response.data, created.response.data);
    const afterCreate = await request(first, 'after-create', 'GET', '/api/restaurants');
    assert.equal(afterCreate.response.data.length, 4);
    for (const [id, menu, expected] of [['array-menu', ['김밥', 123], ['김밥']], ['null-menu', null, []]]) {
      const item = await request(first, id, 'POST', '/api/restaurants', {
        name: '메뉴 확인', category: '분식', location: '캠퍼스', recommendedMenu: menu
      });
      assert.equal(item.status, 201); assert.deepEqual(item.response.data.recommendedMenu, expected);
    }
    await stop(first.child);
    const second = await start();
    const restarted = await request(second, 'restarted', 'GET', '/api/restaurants');
    assert.deepEqual(restarted.response.data, list.response.data);
    const lost = await request(second, 'lost', 'GET', '/api/restaurants/4');
    assert.equal(lost.status, 404);
    await stop(second.child);
    for (const item of sourceFiles) assert.equal(hash(item.file), item.sha256, 'Source changed: ' + item.file);
    const checks = ['Health 200 and CORS', 'Seed list and synchronous comparison', 'Popular rating order and limit',
      'Missing values 400 and missing resources 404', 'Creation 201 and menu normalization',
      'Created restaurant shared by a later HTTP request', 'Restart restores seed and loses new restaurants',
      'Source files including seed JSON unchanged'];
    const capture = { capturedAt: new Date().toISOString(), server: 'pwd-week6',
      commit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: serverRoot, encoding: 'utf8' }).trim(),
      environment: { node: process.version, mode: 'production', execution: 'TypeScript source via tsx' },
      sourceFiles, requests, checks };
    fs.writeFileSync(path.join(root, 'materials/runtime-evidence.json'), JSON.stringify(capture, null, 2) + '\n');
    console.log(JSON.stringify({ requests: Object.keys(requests).length, checks }, null, 2));
  } finally { for (const child of children) await stop(child); }
})().catch(error => { console.error(error); process.exitCode = 1; });
