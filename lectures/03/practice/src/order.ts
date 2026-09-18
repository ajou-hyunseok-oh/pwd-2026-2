import type { DiscountPolicy, Order, Product, Result } from "./types.js";

export function parseQuantity(raw: string, stock: number): Result<number> {
  // TODO 1: 공백/빈 값 → Number 변환 → 유한한 양의 정수 → 재고 순으로 확인.
  // 실패는 { ok: false, message: "이유" }, 성공은 { ok: true, data: 수량 }.
  return { ok: false, message: "TODO 1: 수량 검증을 구현하세요." };
}

export function calculateLineTotal(price: number, quantity: number): number {
  // TODO 2: 함수 입력과 반환 타입을 읽고 상품 금액을 계산하세요.
  return 0;
}

export function createOrder(
  products: Product[], productId: string, rawQuantity: string, policy: DiscountPolicy,
): Result<Order> {
  // TODO 3: find → 상품 없음 처리 → parseQuantity → 실패 처리 → 계산 → 정책 호출.
  // products를 변경하지 않고 새 Order를 반환하세요. 타입 단언이나 any는 필요 없습니다.
  return { ok: false, message: "TODO 3: 주문 계산을 구현하세요." };
}
