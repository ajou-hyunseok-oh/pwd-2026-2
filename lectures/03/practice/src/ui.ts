import type { Order, OrderStatus, Product } from "./types.js";

// 제공된 DOM 경계 검사: 실제 요소 종류를 확인합니다.
function element(id: string): HTMLElement {
  const value = document.getElementById(id);
  if (!value) throw new Error(`요소 없음: ${id}`);
  return value;
}
function input(id: string): HTMLInputElement {
  const value = element(id);
  if (!(value instanceof HTMLInputElement)) throw new Error(`input 아님: ${id}`);
  return value;
}
function select(id: string): HTMLSelectElement {
  const value = element(id);
  if (!(value instanceof HTMLSelectElement)) throw new Error(`select 아님: ${id}`);
  return value;
}
function button(id: string): HTMLButtonElement {
  const value = element(id);
  if (!(value instanceof HTMLButtonElement)) throw new Error(`button 아님: ${id}`);
  return value;
}
export const ui = {
  form: element("order-form"), product: select("product"), quantity: input("quantity"),
  policy: select("policy"), submit: button("submit"), reload: button("reload"),
  loadFailure: input("load-failure"), saveFailure: input("save-failure"),
};
const won = (value: number): string => `${value.toLocaleString("ko-KR")}원`;
export function renderProducts(products: Product[]): void {
  element("products").replaceChildren(...products.map((product) => {
    const li = document.createElement("li");
    li.textContent = `${product.name} · ${won(product.price)} · 재고 ${product.stock}개`;
    return li;
  }));
  ui.product.replaceChildren(...products.filter((product) => product.stock > 0).map((product) => {
    const option = document.createElement("option");
    option.value = product.id;
    option.textContent = product.name;
    return option;
  }));
}
export function renderStatus(state: OrderStatus, message: string): void {
  const status = element("status");
  status.dataset.state = state;
  status.textContent = message;
  element("result").textContent = "";
}
export function renderOrder(order: Order): void {
  element("result").textContent = `${order.quantity}개 · 상품 금액 ${won(order.subtotal)} → 결제 금액 ${won(order.total)}`;
}
