import type { DiscountPolicy } from "./types.js";

// TODO 4: 할인액이 아니라 최종 결제 금액을 반환합니다. 일반 정책을 읽고 회원 정책을 완성하세요.
export const regularPrice: DiscountPolicy = (amount) => amount;
export const memberPrice: DiscountPolicy = (amount) => amount; // 회원 10% 할인, 원 미만 버림.
