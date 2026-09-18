import type { ErrorCode, Result } from './types.js';

export function success<T>(data: T): Result<T> {
  return { ok: true, data };
}
export function failure(code: ErrorCode, message: string): Result<never> {
  return { ok: false, code, message };
}
