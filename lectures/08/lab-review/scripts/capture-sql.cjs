// Execute the original SQL in a disposable local database. No .env or cloud access.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const deck = path.resolve(__dirname, '..');
const source = path.resolve(process.env.SERVER_ROOT || path.join(deck, '../../../..', 'pwd-week7'));
const sourceRequire = createRequire(path.join(source, 'package.json'));
const { PGlite } = sourceRequire('@electric-sql/pglite');
const names = ['supabase/schema.sql', 'supabase/seed.sql', 'src/models/restaurant.model.ts'];
const hashes = () => names.map(file => ({ file, sha256: crypto.createHash('sha256').update(fs.readFileSync(path.join(source, file))).digest('hex') }));

(async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'pwd-week8-review-sql-'));
  const sourceFiles = hashes();
  let db = new PGlite(directory);
  const query = async sql => (await db.query(sql)).rows;
  try {
    await db.exec('create role anon; create role authenticated; create role service_role bypassrls;');
    await db.exec(fs.readFileSync(path.join(source, 'supabase/schema.sql'), 'utf8'));
    const empty = await query('select count(*)::int as count from public.restaurants');
    assert.equal(empty[0].count, 0);
    const seedSQL = fs.readFileSync(path.join(source, 'supabase/seed.sql'), 'utf8');
    await db.exec(seedSQL);
    const initial = await query('select * from public.restaurants order by id');
    assert.equal(initial.length, 3);
    await db.query("update public.restaurants set description=$1 where id=1", ['유지할 내용']);
    await db.exec(seedSQL);
    const reseeded = await query('select id,description from public.restaurants where id=1');
    assert.equal(reseeded[0].description, '유지할 내용');
    await db.exec('set role service_role');
    const insertSQL = 'insert into public.restaurants(name,category,location,recommended_menu) values ($1,$2,$3,$4) returning *';
    const input = ['영구 저장 확인 식당', '한식', '아주대학교 실습', ['김밥', '라면']];
    const inserted = (await db.query(insertSQL, input)).rows[0];
    assert.equal(inserted.id, 4);
    assert.equal(inserted.price_range, '정보 없음');
    await db.exec('reset role');
    await db.close();
    db = new PGlite(directory);
    const reopened = await query('select * from public.restaurants where id=4');
    assert.deepEqual(reopened[0], inserted);
    const permissions = {};
    for (const role of ['anon', 'authenticated']) {
      await db.exec(`set role ${role}`);
      try { await query('select * from public.restaurants'); assert.fail('Expected permission failure'); }
      catch (error) { assert.equal(error.code, '42501'); permissions[role] = error.code; }
      await db.exec('reset role');
    }
    await db.exec('set role service_role');
    permissions.service_role = (await query('select count(*)::int as count from public.restaurants'))[0].count;
    assert.equal(permissions.service_role, 4);
    await query('select public.reset_restaurant_demo_data()');
    const reset = await query('select id,name from public.restaurants order by id');
    assert.equal(reset.length, 3);
    assert.equal((await query("insert into public.restaurants(name,category,location) values ('다음 맛집','한식','캠퍼스') returning id"))[0].id, 4);
    assert.deepEqual(hashes(), sourceFiles);
    const evidence = {
      environment: 'PGlite 0.5.14, disposable local disk database; no Supabase Data API or Express HTTP execution',
      sourceCommit: execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(),
      sourceFiles, empty, initial, reseeded, insertSQL, input, inserted, reopened, permissions, reset
    };
    fs.writeFileSync(path.join(deck, 'materials/sql-evidence.json'), JSON.stringify(evidence, null, 2) + '\n');
    console.log('SQL evidence captured: schema, seed preservation, identity/defaults, reopen, roles, reset');
  } finally {
    await db.close();
    fs.rmSync(directory, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
