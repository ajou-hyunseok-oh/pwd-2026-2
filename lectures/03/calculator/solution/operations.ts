import { failure, success } from '../src/result.js';
import { sin, cos, tan, ln, log10 } from '../src/scientific.js';
import type { BinaryStrategy, UnaryStrategy, OperationRegistry } from '../src/types.js';

export const add: BinaryStrategy = (x, y) => success(x + y);
export const subtract: BinaryStrategy = (x, y) => success(x - y);
export const multiply: BinaryStrategy = (x, y) => success(x * y);
export const divide: BinaryStrategy = (x, y) => {
  if (y === 0) return failure('DIVISION_BY_ZERO', '0으로 나눌 수 없습니다.');
  return success(x / y);
};
export const square: UnaryStrategy = (x) => success(x * x);
export const sqrt: UnaryStrategy = (x) => {
  if (x < 0) return failure('DOMAIN', '음수의 실수 제곱근은 계산할 수 없습니다.');
  return success(Math.sqrt(x));
};
export const operations: OperationRegistry = {
  binary: { add, subtract, multiply, divide },
  unary: { square, sqrt, sin, cos, tan, ln, log10 },
};
