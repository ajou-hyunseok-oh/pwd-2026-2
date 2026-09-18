// 제공: 표시만 12자리 유효숫자로 정리. 실제 결과·이력에는 원래 number 유지.
export function formatNumber(value: number): string {
  return Number(value.toPrecision(12)).toString();
}
