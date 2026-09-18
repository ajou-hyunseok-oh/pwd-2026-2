import { failure, success } from './result.js';
import { sin, cos, tan, ln, log10 } from './scientific.js';
import type { BinaryStrategy, UnaryStrategy, OperationRegistry } from './types.js';

// 제공 예제: 입력을 변경하지 않고 계산 결과만 반환.
export const add: BinaryStrategy = (x, y) => success(x + y);

// TODO 2: 뺄셈·곱셈·나눗셈. 0으로 나누면 DIVISION_BY_ZERO 실패 반환.
export const subtract: BinaryStrategy = (x, y) =>
  failure('NOT_IMPLEMENTED', 'TODO 2: 뺄셈을 구현하세요.');
export const multiply: BinaryStrategy = (x, y) =>
  failure('NOT_IMPLEMENTED', 'TODO 2: 곱셈을 구현하세요.');
export const divide: BinaryStrategy = (x, y) =>
  failure('NOT_IMPLEMENTED', 'TODO 2: 나눗셈을 구현하세요.');

// TODO 3: 제곱·제곱근. 제곱근에 음수가 들어오면 DOMAIN 실패 반환.
export const square: UnaryStrategy = (x) =>
  failure('NOT_IMPLEMENTED', 'TODO 3: 제곱을 구현하세요.');
export const sqrt: UnaryStrategy = (x) =>
  failure('NOT_IMPLEMENTED', 'TODO 3: 제곱근을 구현하세요.');

// 제공: Strategy의 교체 지점. 각 함수가 공통 계약을 따름.
export const operations: OperationRegistry = {
  binary: { add, subtract, multiply, divide },
  unary: { square, sqrt, sin, cos, tan, ln, log10 },
};
