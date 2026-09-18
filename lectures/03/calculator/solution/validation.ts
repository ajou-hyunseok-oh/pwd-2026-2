import { failure, success } from '../src/result.js';
import { decimalPattern } from '../src/validation.js';
import type { Result } from '../src/types.js';

export function parseNumber(raw: string): Result<number> {
  const value = raw.trim();
  if (value === '') return failure('EMPTY_INPUT', '숫자를 입력하세요.');
  if (!decimalPattern.test(value)) {
    return failure('INVALID_NUMBER', '십진수 또는 지수 표기의 숫자를 입력하세요.');
  }
  const number = Number(value);
  if (!Number.isFinite(number))
    return failure('INVALID_NUMBER', '유한한 숫자를 입력하세요.');
  return success(number);
}
