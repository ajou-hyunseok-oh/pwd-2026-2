import type { Calculation } from './types.js';

// 제공: 상태를 소유하고 add/list/clear로 접근을 제한하는 캡슐화 예제.
export class CalculationHistory {
  #entries: Calculation[] = [];

  add(calculation: Calculation): void {
    this.#entries = [{ ...calculation }, ...this.#entries].slice(0, 5);
  }
  list(): Calculation[] {
    return this.#entries.map((entry) => ({ ...entry }));
  }
  clear(): void {
    this.#entries = [];
  }
}
