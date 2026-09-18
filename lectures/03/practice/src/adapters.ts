import type { ApiProduct, Product } from "./types.js";

export function toProduct(raw: ApiProduct): Product {
  // 선택 TODO 5: 이미 검증된 외부 필드 이름을 내부 Product 필드로 매핑하세요.
  // 임시 구현은 명시적으로 실패합니다. 기본 상품 모드에서는 호출하지 않습니다.
  throw new Error("선택 TODO 5: Adapter를 구현하세요.");
}
