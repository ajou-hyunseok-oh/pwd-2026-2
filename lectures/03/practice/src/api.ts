import type { ApiProduct, Order, Product } from "./types.js";
import { toProduct } from "./adapters.js";

// 제공 코드: unknown을 바로 Product라고 단언하지 않는 이유를 설명하세요.
export function isApiProduct(value: unknown): value is ApiProduct {
  if (typeof value !== "object" || value === null) return false;
  return "id" in value && typeof value.id === "string" && value.id.trim() !== ""
    && "product_name" in value && typeof value.product_name === "string"
    && value.product_name.trim() !== ""
    && "unit_price" in value && typeof value.unit_price === "number"
    && Number.isSafeInteger(value.unit_price) && value.unit_price >= 0
    && "stock" in value && typeof value.stock === "number"
    && Number.isSafeInteger(value.stock) && value.stock >= 0;
}

export async function loadProducts(fail: boolean): Promise<Product[]> {
  if (fail) throw new Error("상품 조회 실패: 체크를 해제하고 다시 불러오세요.");
  const fixture = new URLSearchParams(location.search).get("fixture");
  const fixtures: Record<string, string> = {
    valid: "api-valid.json", missing: "api-missing.json", wrong: "api-wrong.json",
  };
  const filename = fixture ? fixtures[fixture] : "api-valid.json";
  if (!filename) throw new Error("지원하지 않는 fixture입니다.");
  const response = await fetch(`fixtures/${filename}`);
  if (!response.ok) throw new Error(`HTTP 오류: ${response.status}`);
  const raw: unknown = await response.json();
  if (!Array.isArray(raw) || !raw.every(isApiProduct)) {
    throw new Error("상품 데이터 형식 오류");
  }
  // 기본 모드는 제공된 변환 사용. ?fixture=valid는 학생 Adapter 사용.
  return raw.map((item) => fixture ? toProduct(item) : ({
    id: item.id, name: item.product_name, price: item.unit_price, stock: item.stock,
  }));
}

export async function saveOrder(order: Order, fail: boolean): Promise<string> {
  await new Promise<void>((resolve) => setTimeout(resolve, 500));
  if (fail) throw new Error("주문 요청 실패: 다시 시도하세요.");
  return `DEMO-${order.productId}`;
}
