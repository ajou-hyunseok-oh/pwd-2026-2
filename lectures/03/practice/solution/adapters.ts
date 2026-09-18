import type { ApiProduct, Product } from "../src/types.js";
export function toProduct(raw: ApiProduct): Product {
  return { id: raw.id, name: raw.product_name, price: raw.unit_price, stock: raw.stock };
}
