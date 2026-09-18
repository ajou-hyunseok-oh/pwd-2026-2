// 실행 전에 출력값/예외를 먼저 기록하세요. 각 사례를 분리해 모두 실행합니다.
const product = { id: "note", name: "노트", price: 3000, stock: 5 };
console.log("A", "3" + 1);
console.log("B", product.prcie * 2);
try {
  const found = [product].find((item) => item.id === "missing");
  console.log("C", found.price);
} catch (error) {
  console.log("C", error.name);
}
const copy = product;
copy.stock = 0;
console.log("D", product.stock);
