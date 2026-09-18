import { failure } from './result.js';
import type { Result } from './types.js';

// 제공: 십진수·소수·지수 표기. 0x10, 2abc, 자유 수식은 허용하지 않음.
export const decimalPattern = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i;

export function parseNumber(raw: string): Result<number> {
  // TODO 1: trim → 빈 입력 → decimalPattern.test → Number → 유한한 값 검사.
  // 성공은 { ok: true, data: 숫자 }, 실패는 { ok: false, code, message }.
  // 빈 입력: EMPTY_INPUT / 형식 오류·무한대: INVALID_NUMBER.
  return failure('NOT_IMPLEMENTED', 'TODO 1: 숫자 입력 검증을 구현하세요.');
}
