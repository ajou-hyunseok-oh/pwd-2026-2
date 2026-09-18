import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const reference = process.argv.includes("--solution");
const folder = reference ? "solution" : "src";
const { parseQuantity, calculateLineTotal, createOrder } = await import(`../dist/${folder}/order.js`);
const { regularPrice, memberPrice } = await import(`../dist/${folder}/policies.js`);
let failed = 0;
let passed = 0;
async function test(name, run) {
  try { await run(); passed++; console.log(`PASS ${name}`); }
  catch (error) { failed++; console.error(`FAIL ${name}: ${error.message}`); }
}
const products = [{ id: "note", name: "노트", price: 3000, stock: 5 }, { id: "case", name: "필통", price: 8000, stock: 0 }];
for (const raw of ["", " ", "0", "-1", "1.5", "abc", "2abc", "Infinity", "NaN", "6"]) {
  await test(`수량 거부: ${JSON.stringify(raw)}`, () => {
    const result = parseQuantity(raw, 5);
    assert.equal(result.ok, false);
    assert.equal(typeof result.message, "string");
    assert.ok(result.message.length > 0);
  });
}
for (const raw of ["1", "2", " 2 ", "2.0", "2e0", "5"]) {
  await test(`수량 허용: ${raw}`, () => assert.deepEqual(parseQuantity(raw, 5), { ok: true, data: Number(raw) }));
}
await test("단가 × 수량", () => assert.equal(calculateLineTotal(3000, 2), 6000));
await test("일반 정책", () => assert.equal(regularPrice(6000), 6000));
await test("회원 정책 / 원 미만 버림", () => {
  assert.equal(memberPrice(6000), 5400);
  assert.equal(memberPrice(3001), 2700);
});
await test("없는 상품", () => assert.equal(createOrder(products, "missing", "1", regularPrice).ok, false));
await test("품절 상품", () => assert.equal(createOrder(products, "case", "1", regularPrice).ok, false));
await test("주문에서 잘못된 수량 거부", () => assert.equal(createOrder(products, "note", "6", regularPrice).ok, false));
await test("일반 / 회원 주문", () => {
  for (const [policy, total] of [[regularPrice, 6000], [memberPrice, 5400]]) {
    assert.deepEqual(createOrder(products, "note", "2", policy), {
      ok: true, data: { productId: "note", quantity: 2, subtotal: 6000, total },
    });
  }
});
await test("정책 교체와 원본 불변", () => {
  const before = structuredClone(products);
  const frozen = Object.freeze(products.map((product) => Object.freeze({ ...product })));
  let calls = 0;
  const result = createOrder(frozen, "note", "2", (amount) => { calls++; assert.equal(amount, 6000); return 1234; });
  assert.equal(calls, 1);
  assert.equal(result.ok, true);
  assert.equal(result.data.total, 1234);
  assert.deepEqual(products, before);
});
if (reference || process.argv.includes("--adapter")) {
  const { toProduct } = await import(`../dist/${folder}/adapters.js`);
  const { isApiProduct } = await import("../dist/src/api.js");
  for (const name of ["valid", "missing", "wrong"]) {
    await test(`외부 fixture: ${name}`, async () => {
      const raw = JSON.parse(await readFile(new URL(`../fixtures/api-${name}.json`, import.meta.url), "utf8"));
      assert.equal(raw.every(isApiProduct), name === "valid");
      if (name === "valid") assert.deepEqual(toProduct(raw[0]), products[0]);
    });
  }
  await test("검증기 null / 음수 / 소수 거부", () => {
    assert.equal(isApiProduct(null), false);
    for (const patch of [{ unit_price: -1 }, { stock: 1.5 }, { unit_price: Infinity }]) {
      assert.equal(isApiProduct({ id: "x", product_name: "x", unit_price: 100, stock: 1, ...patch }), false);
    }
  });
}
console.log(`${reference ? "강사용" : "학생용"}: ${passed} passed, ${failed} failed`);
process.exitCode = failed ? 1 : 0;
