// 사칙연산과 함수형 Strategy: 상태나 DOM을 변경하지 않습니다.
type Operator = '+' | '-' | '*' | '/';
type BinaryOperation = (left: number, right: number) => number;

const add: BinaryOperation = (left, right) => left + right;
const subtract: BinaryOperation = (left, right) => left - right;
const multiply: BinaryOperation = (left, right) => left * right;
const divide: BinaryOperation = (left, right) => {
  if (right === 0) throw new Error('0으로 나눌 수 없습니다.');
  return left / right;
};

// 함수도 값이므로 객체에 보관하고 다른 함수의 인수로 전달할 수 있습니다.
const operations = { '+': add, '-': subtract, '*': multiply, '/': divide };

function calculate(left: number, right: number, operation: BinaryOperation): number {
  return operation(left, right);
}
