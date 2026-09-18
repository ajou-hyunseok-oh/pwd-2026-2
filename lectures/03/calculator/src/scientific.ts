import { failure, success } from './result.js';
import type { AngleUnit, UnaryStrategy } from './types.js';

export function toRadians(value: number, unit: AngleUnit): number {
  return unit === 'deg' ? (value / 180) * Math.PI : value;
}
// 제공 코드: Math의 삼각함수는 라디안을 받음.
export const sin: UnaryStrategy = (x, unit) => success(Math.sin(toRadians(x, unit)));
export const cos: UnaryStrategy = (x, unit) => success(Math.cos(toRadians(x, unit)));
export const tan: UnaryStrategy = (x, unit) => {
  const radians = toRadians(x, unit);
  // 수업용 규칙: cos의 절댓값이 1e-12 이하면 특이점 근처로 처리.
  if (Math.abs(Math.cos(radians)) <= 1e-12) {
    return failure('DOMAIN', 'tan은 이 각도에서 계산할 수 없습니다.');
  }
  return success(Math.tan(radians));
};
export const ln: UnaryStrategy = (x) => {
  if (x <= 0) return failure('DOMAIN', '로그의 입력은 0보다 커야 합니다.');
  return success(Math.log(x));
};
export const log10: UnaryStrategy = (x) => {
  if (x <= 0) return failure('DOMAIN', '로그의 입력은 0보다 커야 합니다.');
  return success(Math.log10(x));
};
