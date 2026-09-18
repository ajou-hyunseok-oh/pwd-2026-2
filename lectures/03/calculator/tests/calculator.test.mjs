import assert from 'node:assert/strict';
import { createCalculator } from '../dist/src/calculator.js';
import { CalculationHistory } from '../dist/src/history.js';
import { formatNumber } from '../dist/src/format.js';
import { toRadians } from '../dist/src/scientific.js';
const reference = process.argv.includes('--solution');
const folder = reference ? 'solution' : 'src';
const { parseNumber } = await import(`../dist/${folder}/validation.js`);
const { operations } = await import(`../dist/${folder}/operations.js`);
const calculate = createCalculator(parseNumber, operations);
let passed = 0,
  failed = 0;
function test(name, run) {
  try {
    run();
    passed++;
    console.log(`PASS ${name}`);
  } catch (error) {
    failed++;
    console.error(`FAIL ${name}: ${error.message}`);
  }
}
function input(operation, x, y = '', unit = 'deg') {
  return { operation, x, y, unit };
}
function value(operation, x, y, unit) {
  const result = calculate(input(operation, x, y, unit));
  assert.equal(result.ok, true, result.message);
  return result.data.value;
}
function error(raw, code) {
  const result = calculate(raw);
  assert.equal(result.ok, false);
  assert.equal(result.code, code);
  assert.equal(typeof result.message, 'string');
  assert.ok(result.message.length > 0);
}
function close(actual, expected) {
  assert.ok(Math.abs(actual - expected) <= 1e-12, `${actual} ≈ ${expected}`);
}
for (const [raw, expected] of [
  ['0', 0],
  ['-2.5', -2.5],
  [' +3 ', 3],
  ['.5', 0.5],
  ['1.', 1],
  ['1e3', 1000],
  ['-1E-3', -0.001],
]) {
  test(`숫자 입력 ${JSON.stringify(raw)}`, () =>
    assert.deepEqual(parseNumber(raw), { ok: true, data: expected }));
}
for (const raw of ['', '   ']) {
  test(`빈 값 ${JSON.stringify(raw)}`, () => {
    const result = parseNumber(raw);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'EMPTY_INPUT');
  });
}
for (const raw of [
  'abc',
  '2abc',
  '0x10',
  '0b10',
  '1+2',
  '1,000',
  'NaN',
  'Infinity',
  '1e309',
  '--2',
  '1e',
]) {
  test(`잘못된 숫자 ${raw}`, () => {
    const result = parseNumber(raw);
    assert.equal(result.ok, false);
    assert.equal(result.code, 'INVALID_NUMBER');
  });
}
for (const [op, x, y, expected] of [
  ['add', '12', '3', 15],
  ['subtract', '12', '3', 9],
  ['multiply', '-2', '3', -6],
  ['divide', '12', '3', 4],
  ['divide', '0', '3', 0],
]) {
  test(`${op}(${x}, ${y})`, () => assert.equal(value(op, x, y), expected));
}
test('0으로 나누기', () => error(input('divide', '1', '0'), 'DIVISION_BY_ZERO'));
test('-0으로 나누기', () => error(input('divide', '1', '-0'), 'DIVISION_BY_ZERO'));
test('제곱', () => assert.equal(value('square', '-3'), 9));
test('제곱근', () => assert.equal(value('sqrt', '9'), 3));
test('0의 제곱근', () => assert.equal(value('sqrt', '0'), 0));
test('음수 제곱근', () => error(input('sqrt', '-1'), 'DOMAIN'));
test('단항 연산은 y를 읽지 않음', () =>
  assert.equal(value('square', '3', 'invalid'), 9));
test('이항 연산은 y가 필요', () => error(input('add', '3', ''), 'EMPTY_INPUT'));
test('도 → 라디안', () => close(toRadians(180, 'deg'), Math.PI));
test('sin(30 DEG)', () => close(value('sin', '30'), 0.5));
test('cos(60 DEG)', () => close(value('cos', '60'), 0.5));
test('tan(45 DEG)', () => close(value('tan', '45'), 1));
test('sin(π/2 RAD)', () => close(value('sin', String(Math.PI / 2), '', 'rad'), 1));
test('tan 특이점 DEG', () => error(input('tan', '90'), 'DOMAIN'));
test('tan 특이점 RAD', () =>
  error(input('tan', String(Math.PI / 2), '', 'rad'), 'DOMAIN'));
test('ln(e)', () => close(value('ln', String(Math.E)), 1));
test('log10(100)', () => close(value('log10', '100'), 2));
test('ln(0)', () => error(input('ln', '0'), 'DOMAIN'));
test('log10(-1)', () => error(input('log10', '-1'), 'DOMAIN'));
test('제곱 오버플로', () => error(input('square', '1e308'), 'NON_FINITE_RESULT'));
test('곱셈 오버플로', () =>
  error(input('multiply', '1e308', '10'), 'NON_FINITE_RESULT'));
test('지원하지 않는 연산', () =>
  error(input('__proto__', '2', '3'), 'UNKNOWN_OPERATION'));
test('지원하지 않는 각도 단위', () =>
  error(input('sin', '30', '', 'grad'), 'INVALID_UNIT'));
test('입력 원본 유지', () => {
  const raw = Object.freeze(input('add', '2', '3'));
  const before = { ...raw };
  assert.equal(calculate(raw).ok, true);
  assert.deepEqual(raw, before);
});
test('Strategy 교체', () => {
  let calls = 0;
  const replaced = {
    ...operations,
    binary: {
      ...operations.binary,
      add: (x, y) => {
        calls++;
        assert.equal(x, 2);
        assert.equal(y, 3);
        return { ok: true, data: 42 };
      },
    },
  };
  const result = createCalculator(parseNumber, replaced)(input('add', '2', '3'));
  assert.equal(result.ok, true);
  assert.equal(result.data.value, 42);
  assert.equal(calls, 1);
});
test('결과의 오차와 표시의 분리', () => {
  const raw = value('add', '0.1', '0.2');
  assert.equal(raw, 0.30000000000000004);
  assert.equal(formatNumber(raw), '0.3');
  assert.equal(formatNumber(1e-13), '1e-13');
  assert.equal(formatNumber(-0), '0');
});
test('최근 5개 이력 · 최신순', () => {
  const history = new CalculationHistory();
  for (let i = 0; i < 7; i++) history.add({ expression: String(i), value: i });
  assert.deepEqual(
    history.list().map((item) => item.value),
    [6, 5, 4, 3, 2],
  );
});
test('이력 입력과 반환값의 참조 분리', () => {
  const history = new CalculationHistory();
  const entry = { expression: '2 + 3', value: 5 };
  history.add(entry);
  entry.value = 999;
  const snapshot = history.list();
  snapshot[0].value = 888;
  snapshot.pop();
  assert.deepEqual(history.list(), [{ expression: '2 + 3', value: 5 }]);
  history.clear();
  assert.deepEqual(history.list(), []);
});
console.log(
  `${reference ? '완성 예제' : '학생용'}: ${passed} passed, ${failed} failed`,
);
process.exitCode = failed ? 1 : 0;
