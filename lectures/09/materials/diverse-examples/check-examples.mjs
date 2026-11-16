import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { before, after } from './photo-permissions.mjs';
import './delivery-fee.mjs';

// Teaching contract: total is a nonnegative integer amount in KRW.
const source = readFileSync(new URL('./delivery-fee.mjs', import.meta.url), 'utf8');
const body = source.replace(/^import[^\n]+\n/, '');
assert.throws(() => vm.runInNewContext(body.replace('>= 30000', '> 30000'), { assert }), assert.AssertionError);

// user is null or an authenticated server-side identity with a string ID.
// photo.ownerId comes from the server's stored record.
const photo = { ownerId: 'u1' };
const rows = [
  { name: 'owner', user: { id: 'u1' }, before: true, after: true },
  { name: 'another user', user: { id: 'u2' }, before: true, after: false },
  { name: 'anonymous', user: null, before: false, after: false },
];
for (const row of rows) {
  assert.equal(before(row.user, photo), row.before);
  assert.equal(after(row.user, photo), row.after);
}
console.log(JSON.stringify({
  delivery: { cases: 3, passed: 3, incorrectBoundaryDetected: true },
  photoPermission: rows.map(({ name, before, after }) => ({ name, before, after })),
}, null, 2));
