const test = require('node:test');
const assert = require('node:assert/strict');
const { once } = require('node:events');
const { createApp } = require('../src/app.cjs');

async function serve(t, options) {
  const server = createApp(options).listen(0, '127.0.0.1');
  t.after(() => new Promise(resolve => server.close(resolve)));
  await once(server, 'listening');
  return `http://127.0.0.1:${server.address().port}`;
}

test('GET /foods returns the initial list', async t => {
  const base = await serve(t);
  const response = await fetch(`${base}/foods`);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), [{ id: 1, name: 'Campus Noodles' }]);
});

test('POST creates a food with 201, Location, and a retrievable resource', async t => {
  const base = await serve(t);
  const response = await fetch(`${base}/foods`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Campus Rice' })
  });
  assert.equal(response.status, 201);
  assert.equal(response.headers.get('location'), '/foods/2');
  const food = await response.json();
  assert.deepEqual(food, { id: 2, name: 'Campus Rice' });
  const detail = await fetch(`${base}${response.headers.get('location')}`);
  assert.deepEqual(await detail.json(), food);
});

test('returns JSON errors for invalid input, missing route, and missing resource', async t => {
  const base = await serve(t);
  for (const [url, status] of [['/foods/x', 400], ['/foods/999', 404], ['/missing', 404]]) {
    const response = await fetch(base + url);
    assert.equal(response.status, status);
    assert.equal(typeof (await response.json()).error, 'string');
  }
  for (const body of ['{}', '{"name":"  "}', '{bad json']) {
    const response = await fetch(`${base}/foods`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body
    });
    assert.equal(response.status, 400);
    assert.equal(typeof (await response.json()).error, 'string');
  }
});

test('hides internal errors and forwards rejected async handlers in Express 5', async t => {
  const model = { async findAll() { throw new Error('private database details'); } };
  const base = await serve(t, { model });
  const response = await fetch(`${base}/foods`);
  assert.equal(response.status, 500);
  assert.deepEqual(await response.json(), { error: 'Internal server error' });
});

test('CORS headers allow the configured browser origin and JSON preflight', async t => {
  const base = await serve(t);
  const response = await fetch(`${base}/foods`, {
    method: 'OPTIONS',
    headers: {
      Origin: 'http://localhost:5173',
      'Access-Control-Request-Method': 'POST',
      'Access-Control-Request-Headers': 'content-type'
    }
  });
  assert.equal(response.status, 204);
  assert.equal(response.headers.get('access-control-allow-origin'), 'http://localhost:5173');
  assert.match(response.headers.get('access-control-allow-methods'), /POST/);
});

test('health check and model lifetime belong to the application instance', async t => {
  const first = await serve(t);
  const health = await fetch(`${first}/health`);
  assert.deepEqual(await health.json(), { status: 'ok' });
  await fetch(`${first}/foods`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: '{"name":"New Food"}'
  });
  const second = await serve(t);
  assert.equal((await (await fetch(`${second}/foods`)).json()).length, 1);
});
