import type { DiscountPolicy, Order, Product, Result } from "../src/types.js";

export function parseQuantity(raw: string, stock: number): Result<number> {
  if (raw.trim() === "") return { ok: false, message: "수량을 입력하세요." };
  const quantity = Number(raw);
  if (!Number.isFinite(quantity) || !Number.isInteger(quantity) || quantity <= 0) {
    return { ok: false, message: "수량은 유한한 양의 정수여야 합니다." };
  }
  if (quantity > stock) return { ok: false, message: "재고를 초과했습니다." };
  return { ok: true, data: quantity };
}
export function calculateLineTotal(price: number, quantity: number): number {
  return price * quantity;
}
export function createOrder(
  products: Product[], productId: string, rawQuantity: string, policy: DiscountPolicy,
): Result<Order> {
  const product = products.find((item) => item.id === productId);
  if (!product) return { ok: false, message: "상품을 찾을 수 없습니다." };
  const result = parseQuantity(rawQuantity, product.stock);
  if (!result.ok) return result;
  const quantity = result.data;
  const subtotal = calculateLineTotal(product.price, quantity);
  return { ok: true, data: { productId, quantity, subtotal, total: policy(subtotal) } };
}
