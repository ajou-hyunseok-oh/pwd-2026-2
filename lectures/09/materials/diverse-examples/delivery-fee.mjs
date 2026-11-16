import assert from 'node:assert/strict';

function deliveryFee(total) {
  return total >= 30000 ? 0 : 3000;
}

assert.equal(deliveryFee(29999), 3000);
assert.equal(deliveryFee(30000), 0);
assert.equal(deliveryFee(30001), 0);
