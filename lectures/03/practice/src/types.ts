// 읽기: 속성 이름, 선택적 속성, 리터럴 유니온, 제네릭의 역할을 설명하세요.
export type Product = {
  id: string;
  name: string;
  price: number;
  stock: number;
  description?: string;
};
export type Result<T> = { ok: true; data: T } | { ok: false; message: string };
export type DiscountPolicy = (amount: number) => number;
export type PolicyName = "regular" | "member";
export type OrderStatus = "idle" | "submitting" | "success" | "error";
export type Order = { productId: string; quantity: number; subtotal: number; total: number };
export type ApiProduct = { id: string; product_name: string; unit_price: number; stock: number };
