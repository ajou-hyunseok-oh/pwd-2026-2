import { loadProducts, saveOrder } from "./api.js";
import { createOrder } from "./order.js";
import { regularPrice, memberPrice } from "./policies.js";
import { ui, renderProducts, renderStatus, renderOrder } from "./ui.js";
import type { Product } from "./types.js";

let products: Product[] = [];
let busy = false;
function lock(value: boolean): void {
  busy = value;
  ui.submit.disabled = value || products.length === 0;
  ui.reload.disabled = value;
  ui.product.disabled = value;
  ui.quantity.disabled = value;
  ui.policy.disabled = value;
}
async function refresh(): Promise<void> {
  if (busy) return;
  lock(true);
  products = [];
  renderProducts(products);
  renderStatus("idle", "상품을 불러오는 중입니다.");
  try {
    products = await loadProducts(ui.loadFailure.checked);
    renderProducts(products);
    renderStatus("idle", "상품과 수량을 선택하세요.");
  } catch (error: unknown) {
    renderStatus("error", error instanceof Error ? error.message : "알 수 없는 오류");
  } finally {
    lock(false);
  }
}
ui.reload.addEventListener("click", () => { void refresh(); });
ui.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  const policyName = ui.policy.value;
  if (policyName !== "regular" && policyName !== "member") {
    renderStatus("error", "지원하지 않는 할인 정책입니다.");
    return;
  }
  const policy = policyName === "member" ? memberPrice : regularPrice;
  const result = createOrder(products, ui.product.value, ui.quantity.value, policy);
  if (!result.ok) {
    renderStatus("error", result.message);
    return;
  }
  lock(true);
  renderStatus("submitting", "주문 요청 중입니다.");
  try {
    const receipt = await saveOrder(result.data, ui.saveFailure.checked);
    renderStatus("success", `주문 완료 · ${receipt}`);
    renderOrder(result.data);
  } catch (error: unknown) {
    renderStatus("error", error instanceof Error ? error.message : "알 수 없는 오류");
  } finally {
    lock(false);
  }
});
void refresh();
