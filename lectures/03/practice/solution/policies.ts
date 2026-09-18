import type { DiscountPolicy } from "../src/types.js";
export const regularPrice: DiscountPolicy = (amount) => amount;
export const memberPrice: DiscountPolicy = (amount) => Math.floor(amount * 0.9);
