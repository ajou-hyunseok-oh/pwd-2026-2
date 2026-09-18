"""Original teaching examples adapted from the linked language documentation."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
 'js-history': ['JavaScript: The First 20 Years', 'https://www.cs.tufts.edu/comp/150FP/archive/brendan-eich/js-hopl.pdf'],
 'ecma': ['Ecma · ECMA-262', 'https://ecma-international.org/publications-and-standards/standards/ecma-262/'],
 'grammar': ['MDN · Grammar and Types', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types'],
 'control': ['MDN · Control Flow', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling'],
 'loops': ['MDN · Loops and Iteration', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Loops_and_iteration'],
 'functions': ['MDN · Functions', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions'],
 'objects': ['MDN · Working with Objects', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects'],
 'spread': ['MDN · Spread Syntax', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax'],
 'filter': ['MDN · Array.filter', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter'],
 'map': ['MDN · Array.map', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map'],
 'events': ['MDN · addEventListener', 'https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener'],
 'fetch': ['MDN · Using Fetch', 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch'],
 'ts-history': ['Microsoft · Ten Years of TypeScript', 'https://devblogs.microsoft.com/typescript/ten-years-of-typescript/'],
 'basics': ['TypeScript · The Basics', 'https://www.typescriptlang.org/docs/handbook/2/basic-types.html'],
 'types': ['TypeScript · Everyday Types', 'https://www.typescriptlang.org/docs/handbook/2/everyday-types.html'],
 'narrow': ['TypeScript · Narrowing', 'https://www.typescriptlang.org/docs/handbook/2/narrowing.html'],
 'ts-functions': ['TypeScript · More on Functions', 'https://www.typescriptlang.org/docs/handbook/2/functions.html'],
 'generic': ['TypeScript · Generics', 'https://www.typescriptlang.org/docs/handbook/2/generics.html'],
 'modules': ['TypeScript · Modules', 'https://www.typescriptlang.org/docs/handbook/2/modules.html'],
 'compat': ['TypeScript · Type Compatibility', 'https://www.typescriptlang.org/docs/handbook/type-compatibility.html'],
 'classes': ['TypeScript · Classes', 'https://www.typescriptlang.org/docs/handbook/2/classes.html'],
 'pure': ['React · Keeping Components Pure', 'https://react.dev/learn/keeping-components-pure'],
 'react': ['React · Reacting to Input with State', 'https://react.dev/learn/reacting-to-input-with-state'],
 'vue': ['Vue · Computed Properties', 'https://vuejs.org/guide/essentials/computed.html'],
 'practice': ['실습 README / Lab README', './practice/README.md'],
}
BODY = {}
def bi(ko,en): return {'ko':ko,'en':en}
def code(label,lang,value,**kw):
 return {'kind':'code','label':bi(*label),'language':lang,'code':value.strip(),**kw}
def points(label,*rows):
 return {'kind':'points','label':bi(*label),'items':[bi(*r) for r in rows]}
def table(label,headers,rows):
 return {'kind':'table','label':bi(*label),'headers':[bi(*v) for v in headers],'rows':[[bi(*v) for v in row] for row in rows]}
def flow(label,*rows):
 return {'kind':'flow','label':bi(*label),'items':[bi(*r) for r in rows]}
def add(n,panels,sources=(),layout='split'):
 BODY[str(n)]={'panels':panels,'sources':list(sources),'layout':layout}

add(1, [
 table(('문서 · 서버 · 브라우저', 'Document, Server, and Browser'),
  [('구성', 'Component'), ('역할', 'Role'), ('주문 서비스', 'Order Service')], [
  [('HTML', 'HTML'), ('문서 구조', 'Document structure'), ('상품명 · 가격 표시', 'Product name and price')],
  [('서버 프로그램', 'Server program'), ('데이터 처리', 'Data processing'), ('상품 조회 · 주문 저장', 'Product queries and order storage')],
  [('브라우저 프로그램', 'Browser program'), ('사용자 상호작용', 'User interaction'), ('수량 입력 · 결과 갱신', 'Quantity input and result updates')]])], ['grammar'], layout='single')

add(2, [
 flow(('1995 · Netscape', '1995 · Netscape'),
  ('Brendan Eich의 브라우저 언어 설계', 'Browser language designed by Brendan Eich'),
  ('Mocha → LiveScript → JavaScript', 'Mocha → LiveScript → JavaScript'),
  ('웹페이지의 입력 처리와 상호작용', 'Input handling and interaction on web pages'))], ['js-history'], layout='single')

add(3, [
 table(('표준화의 주요 시점', 'Standardization Milestones'),
  [('시점', 'Date'), ('의미', 'Significance')], [
  [('1997', '1997'), ('ECMA-262 초판 · 공통 언어 규칙', 'First ECMA-262 edition · Shared language rules')],
  [('2015', '2015'), ('ES2015 · let, const, 화살표 함수, 모듈', 'ES2015 · let, const, arrow functions, modules')],
  [('TC39', 'TC39'), ('언어 사양의 제안과 검토', 'Language specification proposals and review')]]),
 code(('현대 JavaScript · ES2015 문법', 'Modern JavaScript · ES2015 Syntax'), 'javascript', """
const price = 3000;
let quantity = 2;
const lineTotal = (price, quantity) => price * quantity;
console.log(lineTotal(price, quantity));
""", output='6000')], ['ecma'], layout='split')

add(4, [
 code(('값과 변수 · JavaScript', 'Values and Variables · JavaScript'), 'javascript', """
const price = 3000;
let quantity = 2;
quantity = 3;
const name = 'Notebook';
const available = true;
let selected;
console.log(typeof price, typeof name);
console.log(selected, null);
""", output='number string\nundefined null'),
 points(('선언과 값', 'Declarations and Values'),
  ('let · 재할당 가능 / const · 재할당 불가', 'let · Reassignment allowed / const · Reassignment blocked'),
  ('number · string · boolean', 'number · string · boolean'),
  ('undefined · 미지정 값 / null · 명시적 빈 값', 'undefined · Unset value / null · Explicit empty value'))], ['grammar'], layout='split')

add(5, [
 code(('같은 입력, 다른 연산', 'Same Input, Different Operations'), 'javascript', """
const raw = '2';
console.log(raw + 1);
console.log(raw - 1);
console.log(Number(raw) + 1);
console.log(Number(''));
console.log(Number('two'));
""", output='21\n1\n3\n0\nNaN'),
 points(('연산 결과 읽기', 'Reading the Results'),
  ('문자열 + 숫자 → 문자열 연결', 'String + number → String concatenation'),
  ('뺄셈 → 암묵적 숫자 변환', 'Subtraction → Implicit numeric conversion'),
  ('Number() → 명시적 숫자 변환', 'Number() → Explicit numeric conversion'),
  ('변환 불가 → NaN', 'Failed conversion → NaN'))], ['grammar'], layout='split')

add(6, [
 code(('수량과 재고 검사', 'Quantity and Stock Checks'), 'javascript', """
const quantity = Number('3');
const stock = 5;
const valid =
  Number.isInteger(quantity) &&
  quantity > 0 &&
  quantity <= stock;
if (valid) {
  console.log('ready');
} else {
  console.log('invalid');
}
""", output='ready'),
 points(('조건의 의미', 'Conditions'),
  ('Number.isInteger · 정수 검사', 'Number.isInteger · Integer check'),
  ('quantity > 0 · 양수 검사', 'quantity > 0 · Positive value check'),
  ('quantity <= stock · 재고 검사', 'quantity <= stock · Stock check'),
  ('&& · 모든 조건 충족', '&& · All conditions required'))], ['control'], layout='split')

add(7, [
 code(('주문 항목의 금액 합산', 'Summing Order Amounts'), 'javascript', """
const amounts = [3000, 1500, 6000];
let total = 0;
for (const amount of amounts) {
  total = total + amount;
}
console.log(total);
""", output='10500'),
 table(('반복별 값 변화', 'Values on Each Iteration'),
  [('amount', 'amount'), ('total', 'total')], [
  [('3000', '3000'), ('0 → 3000', '0 → 3000')],
  [('1500', '1500'), ('3000 → 4500', '3000 → 4500')],
  [('6000', '6000'), ('4500 → 10500', '4500 → 10500')]])], ['loops'], layout='split')

add(8, [
 code(('입력 · 반환 · 접근 범위', 'Inputs, Return Values, and Scope'), 'javascript', """
function calculateLineTotal(price, quantity) {
  const total = price * quantity;
  return total;
}
console.log(calculateLineTotal(3000, 2));
if (true) {
  let message = 'ready';
  console.log(message);
}
""", output='6000\nready'),
 points(('함수 호출 읽기', 'Reading a Function Call'),
  ('인수 3000, 2 → 매개변수 price, quantity', 'Arguments 3000, 2 → Parameters price, quantity'),
  ('return · 결과 반환과 함수 종료', 'return · Returns a result and ends the call'),
  ('total · 함수 내부 / message · if 블록 내부', 'total · Function scope / message · if block scope'))], ['functions', 'grammar'], layout='split')

add(9, [
 code(('할인 함수를 반환하는 함수', 'A Function Returning a Discount Function'), 'javascript', """
function makeDiscount(rate) {
  return (amount) => amount * (1 - rate);
}
const memberPrice = makeDiscount(0.1);
const totals = [3000, 6000].map(memberPrice);
console.log(totals);
""", output='[2700, 5400]'),
 points(('함수의 세 가지 사용', 'Three Uses of Functions'),
  ('일급 함수 · 변수 저장, 인수 전달, 반환', 'First-class functions · Stored, passed, and returned'),
  ('콜백 · map에 전달한 memberPrice', 'Callback · memberPrice passed to map'),
  ('클로저 · makeDiscount 종료 후에도 rate에 접근', 'Closure · Access to rate after makeDiscount returns'))], ['functions'], layout='split')

add(10, [
 code(('상품 객체와 메서드', 'Product Object and Method'), 'javascript', """
const product = {
  name: 'Notebook',
  price: 3000,
  stock: 5,
  inStock() {
    return this.stock > 0;
  }
};
console.log(product.name, product.inStock());
""", output='Notebook true'),
 points(('객체의 멤버', 'Object Members'),
  ('프로퍼티 · name, price, stock', 'Properties · name, price, stock'),
  ('메서드 · inStock()', 'Method · inStock()'),
  ('product.inStock()의 this → product', 'this in product.inStock() → product'))], ['objects'], layout='split')

add(11, [
 code(('공유 참조와 중첩 객체', 'Shared References and Nested Objects'), 'javascript', """
const product = { stock: { count: 5 } };
const shared = product;
const copied = { ...product };
shared.stock.count = 4;
copied.stock.count = 0;
console.log(product.stock.count);
console.log(copied === product);
console.log(copied.stock === product.stock);
""", output='0\nfalse\ntrue'),
 points(('복사의 깊이', 'Copy Depth'),
  ('대입 · 같은 객체의 참조 공유', 'Assignment · Shared reference to one object'),
  ('스프레드 · 바깥 객체만 복사', 'Spread · Copies the outer object'),
  ('중첩 stock · 참조 공유', 'Nested stock · Shared reference'))], ['spread'], layout='split')

add(12, [
 code(('상품 배열 → 상품명 배열', 'Products → Product Names'), 'javascript', """
const products = [
  { name: 'Notebook', stock: 5 },
  { name: 'Case', stock: 0 }
];
const names = products
  .filter((product) => product.stock > 0)
  .map((product) => product.name);
console.log(names);
""", output="['Notebook']"),
 points(('두 콜백의 역할', 'Roles of the Two Callbacks'),
  ('filter · stock > 0인 상품 선택', 'filter · Selects products with stock > 0'),
  ('map · 상품 객체를 name으로 변환', 'map · Converts each product to its name'),
  ('원본 2개 → 결과 1개 · 새 배열 생성', '2 original items → 1 result · New array'))], ['filter', 'map'], layout='split')

add(13, [
 code(('DOM 이벤트 등록', 'DOM Event Registration'), 'javascript', """
const input = document.querySelector('#quantity');
const button = document.querySelector('#submit');
button.addEventListener('click', () => {
  const quantity = Number(input.value);
  console.log(quantity);
});
""", context='dom'),
 points(('등록과 실행', 'Registration and Execution'),
  ('초기화 · 콜백 등록', 'Initialization · Callback registration'),
  ('클릭 · 콜백 실행', 'Click · Callback execution'),
  ('input.value: "2" → quantity: 2', 'input.value: "2" → quantity: 2'))], ['events'], layout='split')

add(14, [
 code(('HTTP 상태 확인과 예외 처리', 'HTTP Checks and Error Handling'), 'javascript', """
async function loadProducts() {
  const response = await fetch('/products.json');
  if (!response.ok) throw new Error('HTTP error');
  return response.json();
}
try {
  const products = await loadProducts();
  console.log(products.length);
} catch (error) {
  console.log('load failed');
}
""", context='fetch'),
 points(('비동기 실행의 경계', 'Async Boundaries'),
  ('await · 요청 완료까지 현재 실행 흐름 대기', 'await · Pauses the current flow until completion'),
  ('response.ok · HTTP 성공 상태 확인', 'response.ok · Checks HTTP success status'),
  ('catch · 요청 · JSON 해석 · throw 오류 처리', 'catch · Handles request, JSON parsing, and thrown errors'))], ['fetch'], layout='split')

add(15, [
 code(('필터 함수의 교체', 'Replacing a Filter Function'), 'javascript', """
const products = [
  { name: 'Notebook', price: 3000, stock: 5 },
  { name: 'Case', price: 8000, stock: 0 }
];
const inStock = (p) => p.stock > 0;
const affordable = (p) => p.price < 5000;
console.log(products.filter(inStock).length);
console.log(products.filter(affordable).length);
""", output='1\n1'),
 points(('유연성의 이점', 'Benefits of Flexibility'),
  ('객체 · 데이터 속성의 묶음', 'Objects · Grouped data properties'),
  ('함수 · 선택 조건의 교체', 'Functions · Replaceable selection conditions'))], ['filter', 'functions'], layout='split')

add(16, [
 code(('잘못된 실행 결과', 'Incorrect Results'), 'javascript', """
const product = { price: 3000, stock: 5 };
const alias = product;
console.log(2 + '3');
console.log(product.prcie * 2);
alias.stock = 0;
console.log(product.stock);
""", output='23\nNaN\n0'),
 points(('서로 다른 오류 원인', 'Different Error Causes'),
  ('23 · 숫자 덧셈 대신 문자열 연결', '23 · String concatenation instead of numeric addition'),
  ('NaN · 없는 속성 prcie의 undefined로 계산', 'NaN · Arithmetic with undefined from missing prcie'),
  ('0 · alias와 product의 참조 공유', '0 · Shared reference between alias and product'))], ['basics', 'spread'], layout='split')

add(17, [
 table(('오류와 검사 위치', 'Errors and Where to Check Them'),
  [('상황', 'Situation'), ('주요 검사', 'Primary Check')], [
  [('숫자 매개변수에 문자열', 'String passed to a number parameter'), ('타입 검사', 'Type checking')],
  [('product.prcie 오타', 'product.prcie typo'), ('타입 검사', 'Type checking')],
  [('수량 -1 · 재고 초과', 'Quantity -1 · Over stock'), ('실행 시 업무 규칙 검증', 'Runtime business validation')],
  [('외부 JSON의 누락 필드', 'Missing field in external JSON'), ('실행 시 데이터 검증', 'Runtime data validation')]]),
 points(('검사의 한계', 'Limits of Checking'),
  ('number는 양의 정수를 보장하지 않음', 'number does not guarantee a positive integer'),
  ('외부 응답은 실행 중 구조와 값 확인', 'External responses need runtime shape and value checks'))], ['basics'], layout='split')

add(18, [
 flow(('2012 · Microsoft', '2012 · Microsoft'),
  ('대규모 JavaScript 코드의 변경과 협업', 'Changes and collaboration in large JavaScript projects'),
  ('2012년 10월 1일 TypeScript 공개', 'TypeScript publicly unveiled on October 1, 2012'),
  ('타입 계약 · 편집기 지원 · 오류 조기 발견', 'Type contracts · Editor support · Earlier error detection')),
 points(('JavaScript와의 관계', 'Relationship to JavaScript'),
  ('기존 JavaScript 문법과 실행 환경 활용', 'Existing JavaScript syntax and runtimes'),
  ('타입으로 코드 구조와 사용법 표현', 'Types express code structure and expected usage'))], ['ts-history', 'basics'], layout='split')

add(19, [
 code(('TypeScript · 타입 표기', 'TypeScript · Type Annotations'), 'typescript', """
function lineTotal(
  price: number,
  quantity: number
): number {
  return price * quantity;
}
console.log(lineTotal(3000, 2));
""", output='6000'),
 code(('JavaScript · 타입 제거', 'JavaScript · Type Erasure'), 'javascript', """
function lineTotal(price, quantity) {
  return price * quantity;
}
console.log(lineTotal(3000, 2));
""", output='6000')], ['basics'], layout='equal')

add(20, [
 code(('타입 추론과 표기', 'Inference and Annotations'), 'typescript', """
let quantity = 2;
const price: number = 3000;
const name: string = 'Notebook';
const available: boolean = true;
const amounts: number[] = [3000, 6000];
quantity = '2';
""", errors=[2322]),
 points(('컴파일러의 판단', 'Compiler Reasoning'),
  ('quantity = 2 → number 추론', 'quantity = 2 → number inferred'),
  ('price: number → 타입 명시', 'price: number → Explicit annotation'),
  ('quantity = "2" → 타입 불일치', 'quantity = "2" → Type mismatch'))], ['types'], layout='split')

add(21, [
 code(('함수 계약', 'Function Contract'), 'typescript', """
function calculateLineTotal(
  price: number,
  quantity: number
): number {
  return price * quantity;
}
calculateLineTotal(3000, 2);
calculateLineTotal(3000, '2');
""", errors=[2345]),
 points(('입력과 반환', 'Arguments and Return Values'),
  ('price · quantity → number 인수', 'price · quantity → number arguments'),
  ('반환값 → number', 'Return value → number'),
  ('문자열 "2" 전달 → 타입 오류', 'Passing string "2" → Type error'))], ['ts-functions'], layout='split')

add(22, [
 code(('type으로 상품 구조 정의', 'Product Shape with type'), 'typescript', """
type Product = {
  id: string;
  name: string;
  price: number;
  stock: number;
};
const product: Product = {
  id: 'note',
  name: 'Notebook',
  price: 3000,
  stock: 5
};
"""),
 code(('interface로 상품 구조 정의', 'Product Shape with interface'), 'typescript', """
interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
}
const product: Product = {
  id: 'note',
  name: 'Notebook',
  price: 3000,
  stock: 5
};
""")], ['types'], layout='equal')

add(23, [
 code(('주문 상태 유니온', 'Order Status Union'), 'typescript', """
type OrderStatus =
  'idle' | 'submitting' | 'success' | 'error';
let status: OrderStatus = 'idle';
status = 'submitting';
status = 'done';
""", errors=[2322]),
 flow(('허용 상태와 전환', 'Allowed States and Transitions'),
  ('idle · 입력 대기', 'idle · Waiting for input'),
  ('submitting · 요청 진행', 'submitting · Request in progress'),
  ('success 또는 error · 요청 결과', 'success or error · Request result'))], ['types'], layout='split')

add(24, [
 code(('선택적 값과 검색 결과', 'Optional Values and Search Results'), 'typescript', """
type Product = {
  id: string;
  price: number;
  discountPrice?: number;
};
const products: Product[] = [
  { id: 'note', price: 3000 }
];
const found = products.find((p) => p.id === 'note');
if (found !== undefined) {
  console.log(found.discountPrice ?? found.price);
}
""", output='3000'),
 points(('두 가지 빈 값', 'Two Missing-Value Cases'),
  ('find 결과 → Product 또는 undefined', 'find result → Product or undefined'),
  ('discountPrice → number 또는 undefined', 'discountPrice → number or undefined'),
  ('존재 확인 후 속성 접근', 'Property access after an existence check'),
  ('?? · null과 undefined에 대체값 적용', '?? · Fallback for null and undefined'))], ['narrow', 'types'], layout='split')

add(25, [
 code(('판별 속성 ok로 결과 분기', 'Branching on the ok Discriminant'), 'typescript', """
type Result =
  | { ok: true; data: number }
  | { ok: false; message: string };
function describe(result: Result): string {
  if (result.ok) {
    return `quantity: ${result.data}`;
  }
  return result.message;
}
console.log(describe({ ok: true, data: 2 }));
""", output='quantity: 2'),
 points(('분기 안의 타입', 'Types Inside Each Branch'),
  ('ok: true → data 사용', 'ok: true → Access data'),
  ('ok: false → message 사용', 'ok: false → Access message'),
  ('조건 검사 전 data 접근 → 타입 오류', 'Access to data before narrowing → Type error'))], ['narrow'], layout='split')

add(26, [
 code(('any · 검사 우회', 'any · Bypassing Checks'), 'typescript', """
const raw: any = 3000;
raw.toUpperCase();
""", runtimeError='TypeError'),
 code(('unknown · 검사 후 사용', 'unknown · Check Before Use'), 'typescript', """
function normalize(raw: unknown): string {
  if (typeof raw === 'string') {
    return raw.toUpperCase();
  }
  return 'not a string';
}
console.log(normalize(3000));
""", output='not a string')], ['ts-functions'], layout='equal')

add(27, [
 code(('as는 값 검사나 변환이 아님', 'as Does Not Validate or Convert Values'), 'typescript', """
const raw: unknown = { price: '3000' };
const claimed = raw as { price: number };
console.log(claimed.price + 1);
if (
  typeof raw === 'object' &&
  raw !== null &&
  'price' in raw &&
  typeof raw.price === 'number'
) {
  console.log(raw.price + 1);
} else {
  console.log('invalid price');
}
""", output='30001\ninvalid price'),
 points(('단언과 검증의 결과', 'Assertion Versus Validation'),
  ('as 이후에도 price는 문자열', 'price remains a string after as'),
  ('컴파일러의 판단만 number로 변경', 'Only the compiler’s assumption changes to number'),
  ('typeof 검사 → 문자열 가격 거부', 'typeof check → Rejects the string price'))], ['narrow', 'types'], layout='split')

add(28, [
 code(('첫 원소의 타입 관계', 'The Type Relationship of a First Element'), 'typescript', """
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const amount = first([3000, 1500]);
const product = first([{ id: 'note', price: 3000 }]);
console.log(amount);
console.log(product?.id);
console.log(first<number>([]));
""", output='3000\nnote\nundefined'),
 points(('T의 의미', 'Meaning of T'),
  ('숫자 배열 → number 또는 undefined', 'Number array → number or undefined'),
  ('상품 배열 → 상품 타입 또는 undefined', 'Product array → Product type or undefined'),
  ('빈 배열 → undefined', 'Empty array → undefined'))], ['generic'], layout='split')

add(29, [
 code(('types.ts · 필요한 구조 내보내기', 'types.ts · Exporting a Required Shape'), 'typescript', """
export type Named = { name: string };
export function label(item: Named): string {
  return item.name;
}
""", file='types.ts'),
 code(('main.ts · 모듈 사용과 구조적 호환', 'main.ts · Modules and Structural Compatibility'), 'typescript', """
import { label } from './types.js';
import type { Named } from './types.js';
const product = { name: 'Notebook', price: 3000 };
const named: Named = product;
console.log(label(named));
""", file='main.ts', context='modules', output='Notebook')], ['modules', 'compat'], layout='equal')

add(30, [
 code(('주문 처리 절차', 'Order Procedure'), 'typescript', """
async function submitOrder(raw: string) {
  const quantity = Number(raw);
  if (!Number.isInteger(quantity) || quantity <= 0) {
    throw new Error('invalid quantity');
  }
  const total = 3000 * quantity;
  await saveOrder(total);
  return { status: 'success', total };
}
""", prelude='declare function saveOrder(total: number): Promise<void>;'),
 flow(('절차와 실패 경로', 'Procedure and Failure Paths'),
  ('수량 검증 → 실패하면 종료', 'Validate quantity → Stop on failure'),
  ('금액 계산 → 저장 요청', 'Calculate amount → Request storage'),
  ('요청 완료 → 성공 결과 반환', 'Await completion → Return success'))], ['ts-functions', 'fetch'], layout='split')

add(31, [
 code(('지역 변수로 계산하는 순수 함수', 'A Pure Function with Local Variables'), 'typescript', """
function calculateTotal(amounts: number[]): number {
  let total = 0;
  for (const amount of amounts) {
    total += amount;
  }
  return total;
}
const amounts = [3000, 1500];
console.log(calculateTotal(amounts));
console.log(amounts.length);
""", output='4500\n2'),
 points(('순수성의 기준', 'Criteria for Purity'),
  ('같은 입력 → 같은 결과', 'Same input → Same result'),
  ('입력 배열과 외부 상태 유지', 'Input array and external state unchanged'),
  ('지역 변수 total만 변경', 'Only the local variable total changes'))], ['pure'], layout='split')

add(32, [
 code(('상태 접근을 제한하는 Cart', 'Cart with Controlled State Access'), 'typescript', """
class Cart {
  private items: string[] = [];
  add(productId: string): void {
    this.items.push(productId);
  }
  get count(): number {
    return this.items.length;
  }
}
const cart = new Cart();
cart.add('note');
console.log(cart.count);
""", output='1'),
 points(('상태와 동작의 책임', 'Responsibility for State and Behavior'),
  ('private items · 외부 접근 제한', 'private items · Restricted external access'),
  ('add() · 내부 배열 변경', 'add() · Changes the internal array'),
  ('count · 배열의 개수 공개', 'count · Exposes the array length'))], ['classes'], layout='split')

add(33, [
 code(('늦게 끝난 이전 요청 무시', 'Ignoring a Stale Response'), 'typescript', """
let latestRequest = 0;
async function search(query: string): Promise<void> {
  const requestId = ++latestRequest;
  const products = await loadProducts(query);
  if (requestId !== latestRequest) return;
  renderProducts(products);
}
""", prelude='declare function loadProducts(query: string): Promise<string[]>;\ndeclare function renderProducts(products: string[]): void;'),
 table(('응답 순서의 역전', 'Responses Arriving Out of Order'),
  [('시간', 'Time'), ('실행', 'Action')], [
  [('1', '1'), ('검색 A 시작 · 요청 번호 1', 'Search A starts · Request 1')],
  [('2', '2'), ('검색 B 시작 · 요청 번호 2', 'Search B starts · Request 2')],
  [('3', '3'), ('B 완료 → 화면 갱신', 'B completes → Update UI')],
  [('4', '4'), ('A 완료 → 번호 불일치로 무시', 'A completes → Ignore stale request')]])], ['events', 'fetch'], layout='split')

add(34, [
 code(('React TSX · 상태에 따른 버튼', 'React TSX · Button Based on State'), 'tsx', """
function OrderButton({ busy }: { busy: boolean }) {
  return (
    <button disabled={busy}>
      {busy ? 'Sending' : 'Order'}
    </button>
  );
}
""", context='react'),
 code(('Vue · 반응형 합계', 'Vue · Reactive Total'), 'typescript', """
import { computed, ref } from 'vue';
const quantity = ref(2);
const total = computed(() => 3000 * quantity.value);
console.log(total.value);
quantity.value = 3;
console.log(total.value);
""", context='vue', output='6000\n9000')], ['react', 'vue'], layout='equal')

add(35, [
 flow(('하나의 주문 기능', 'One Order Feature'),
  ('입력 → 이벤트 처리', 'Input → Event handling'),
  ('검증 → 순수 계산 → 저장 요청', 'Validation → Pure calculation → Storage'),
  ('결과 상태 → 화면 갱신', 'Result state → UI update')),
 table(('실습 파일의 책임', 'Responsibilities in Lab Files'),
  [('파일', 'File'), ('역할', 'Role')], [
  [('main.ts', 'main.ts'), ('이벤트와 절차 조정', 'Events and procedure coordination')],
  [('order.ts · policies.ts', 'order.ts · policies.ts'), ('계산과 검증', 'Calculation and validation')],
  [('api.ts', 'api.ts'), ('외부 데이터와 모의 요청', 'External data and mock requests')],
  [('ui.ts', 'ui.ts'), ('명령형 DOM 갱신', 'Imperative DOM updates')]])], ['practice'], layout='split')

add(36, [
 code(('정책 이름으로 분기', 'Branching on Policy Names'), 'typescript', """
function checkout(amount: number, kind: string) {
  if (kind === 'member') {
    return Math.floor(amount * 0.9);
  }
  return amount;
}
"""),
 points(('교체 지점의 분리', 'Separating a Replacement Point'),
  ('정책 추가 → checkout 분기 증가', 'New policy → More checkout branches'),
  ('Strategy · 계산 함수를 별도로 정의', 'Strategy · Separately defined calculation functions'),
  ('주문 함수 · 전달받은 정책 호출', 'Order function · Calls the supplied policy'))], ['ts-functions'], layout='split')

add(37, [
 code(('공통 함수 타입과 정책 전달', 'Shared Function Type and Policy Passing'), 'typescript', """
type DiscountPolicy = (amount: number) => number;
const regularPrice: DiscountPolicy = (amount) => amount;
const memberPrice: DiscountPolicy = (amount) =>
  Math.floor(amount * 0.9);
function checkout(
  amount: number,
  policy: DiscountPolicy
) {
  return policy(amount);
}
console.log(checkout(6000, regularPrice));
console.log(checkout(6000, memberPrice));
""", output='6000\n5400'),
 points(('계약과 변경', 'Contract and Change'),
  ('입력 · 할인 전 금액', 'Input · Amount before discount'),
  ('반환 · 결제 금액', 'Return · Payable amount'),
  ('회원 정책 · 10% 할인, 원 미만 버림', 'Member policy · 10% discount, rounded down'),
  ('checkout · 전달받은 policy 호출', 'checkout · Calls the supplied policy'))], ['ts-functions'], layout='split')

add(38, [
 code(('검증된 외부 값의 변환', 'Converting Validated External Values'), 'typescript', """
type ApiProduct = {
  product_name: string;
  unit_price: number;
};
type Product = { name: string; price: number };
function toProduct(raw: ApiProduct): Product {
  return {
    name: raw.product_name,
    price: raw.unit_price
  };
}
"""),
 points(('Adapter의 경계', 'Adapter Boundary'),
  ('product_name → name', 'product_name → name'),
  ('unit_price → price', 'unit_price → price'),
  ('입력 · 검증된 ApiProduct', 'Input · Validated ApiProduct'),
  ('반환 · 새로운 Product 객체', 'Return · New Product object'))], ['types', 'practice'], layout='split')

add(39, [
 flow(('외부 데이터의 입력 경계', 'External Data Boundary'),
  ('unknown · 아직 확인하지 않은 값', 'unknown · An unchecked value'),
  ('검증기 · 필드 존재와 실제 타입 확인', 'Validator · Checks fields and actual types'),
  ('ApiProduct → Adapter → Product', 'ApiProduct → Adapter → Product'),
  ('주문 계산 · 내부 계약만 사용', 'Order calculation · Uses only the internal contract')),
 points(('각 단계의 실패 원인', 'Failure Causes by Stage'),
  ('필드 누락 · 문자열 가격 → 검증 실패', 'Missing fields or string prices → Validation failure'),
  ('잘못된 필드 매핑 → 변환 오류', 'Incorrect field mapping → Conversion error'))], ['fetch', 'narrow'], layout='split')

add(40, [
 table(('요구사항에 따른 선택', 'Selection by Requirement'),
  [('변경 요구', 'Change'), ('적용', 'Choice')], [
  [('일반 · 회원 · 쿠폰 정책 교체', 'Regular, member, or coupon pricing'), ('Strategy · 계산 함수 교체', 'Strategy · Replace calculation functions')],
  [('외부 API의 상품 필드 변경', 'External API product fields change'), ('Adapter · 내부 형식으로 매핑', 'Adapter · Map to the internal format')],
  [('고정된 단가 × 수량 계산', 'Fixed unit price × quantity'), ('단순 함수 유지', 'Keep a simple function')]]),
 points(('추상화 비용', 'Abstraction Cost'),
  ('함수 · 파일 증가 → 코드 탐색 비용 증가', 'More functions and files → Higher navigation cost'),
  ('계약 추가 → 호출 관계의 복잡도 증가', 'More contracts → More complex call relationships'))], ['ts-functions', 'practice'], layout='split')

add(41, [
 table(('모의 주문서', 'Mock Order Form'),
  [('입력', 'Input'), ('선택값', 'Value')], [
  [('상품', 'Product'), ('노트 · 단가 3,000원', 'Notebook · 3,000 won each')],
  [('수량', 'Quantity'), ('2', '2')],
  [('할인', 'Discount'), ('회원 · 10%', 'Member · 10%')],
  [('결과', 'Result'), ('6,000원 → 5,400원', '6,000 won → 5,400 won')]]),
 points(('구현 범위', 'Implementation Scope'),
  ('제공 · HTML · CSS · 이벤트 골격', 'Provided · HTML, CSS, event scaffolding'),
  ('필수 · 수량 검증 · 주문 계산 · 회원 정책', 'Required · Quantity validation, order calculation, member policy'),
  ('선택 · 외부 데이터 Adapter', 'Optional · External data Adapter'))], ['practice'], layout='split')

add(42, [
 flow(('노트 2개 · 회원 주문', 'Two Notebooks · Member Order'),
  ('Product · price: 3000, stock: 5', 'Product · price: 3000, stock: 5'),
  ('입력 "2" → 수량 2 → 검증 통과', 'Input "2" → Quantity 2 → Valid'),
  ('상품 금액 6000 → 회원 정책 → 5400', 'Subtotal 6000 → Member policy → 5400'),
  ('Result<Order> → 모의 요청 → 화면', 'Result<Order> → Mock request → UI')),
 points(('주문 데이터', 'Order Data'),
  ('productId · 상품 검색 키', 'productId · Product lookup key'),
  ('quantity · 검증된 수량', 'quantity · Validated quantity'),
  ('subtotal · 할인 전 금액', 'subtotal · Amount before discount'),
  ('total · 정책 적용 금액', 'total · Amount after the policy'))], ['practice'], layout='split')

add(43, [
 code(('practice · localhost:4303', 'practice · localhost:4303'), 'bash', """
npm ci
npm start

# Second terminal
npm run watch
npm run check
npm test
"""),
 table(('파일과 작업', 'Files and Tasks'),
  [('파일', 'File'), ('작업', 'Task')], [
  [('src/order.ts', 'src/order.ts'), ('TODO 1–3 · 필수 구현', 'TODO 1–3 · Required')],
  [('src/policies.ts', 'src/policies.ts'), ('TODO 4 · 회원 정책', 'TODO 4 · Member policy')],
  [('src/adapters.ts', 'src/adapters.ts'), ('TODO 5 · 선택 구현', 'TODO 5 · Optional')],
  [('main.ts · ui.ts · api.ts', 'main.ts · ui.ts · api.ts'), ('제공 코드 읽기', 'Read provided code')]])], ['practice'], layout='split')

add(44, [
 code(('reading/bugs.js · 실행 전 예측', 'reading/bugs.js · Predict Before Running'), 'javascript', """
const product = { price: 3000, stock: 5 };
console.log('3' + 1);
console.log(product.prcie * 2);
const found = [product].find((p) => p.price === 0);
console.log(found.price);
""", runtimeError='TypeError', output='31\nNaN\nTypeError'),
 points(('오류 원인', 'Error Causes'),
  ('"3" + 1 · 문자열 연결', '"3" + 1 · String concatenation'),
  ('product.prcie · 없는 속성', 'product.prcie · Missing property'),
  ('found.price · undefined의 속성 접근', 'found.price · Property access on undefined'))], ['practice'], layout='split')

add(45, [
 code(('order.ts · 수량 검증', 'order.ts · Quantity Validation'), 'typescript', """
function parseQuantity(raw: string, stock: number) {
  if (raw.trim() === '') {
    return { ok: false, message: 'empty' };
  }
  const quantity = Number(raw);
  if (
    !Number.isFinite(quantity) ||
    !Number.isInteger(quantity) ||
    quantity <= 0
  ) {
    return { ok: false, message: 'invalid' };
  }
  if (quantity > stock) {
    return { ok: false, message: 'over stock' };
  }
  return { ok: true, data: quantity };
}
"""),
 points(('확인할 입력', 'Inputs to Check'),
  ('빈 값 · 공백 · abc · Infinity → 실패', 'Empty, whitespace, abc, Infinity → Failure'),
  ('0 · -1 · 1.5 → 실패', '0, -1, 1.5 → Failure'),
  ('재고 5: 수량 5 → 성공 / 6 → 실패', 'Stock 5: quantity 5 → Success / 6 → Failure'))], ['practice'], layout='split')

add(46, [
 code(('전환 전 · JavaScript', 'Before · JavaScript'), 'javascript', """
function calculateLineTotal(price, quantity) {
  return price * quantity;
}
const product = {
  id: 'note',
  name: 'Notebook',
  price: 3000,
  stock: 5
};
"""),
 code(('전환 후 · TypeScript', 'After · TypeScript'), 'typescript', """
function calculateLineTotal(
  price: number,
  quantity: number
): number {
  return price * quantity;
}
const product: Product = {
  id: 'note',
  name: 'Notebook',
  price: 3000,
  stock: 5
};
""", prelude='type Product = { id: string; name: string; price: number; stock: number };')], ['practice', 'basics'], layout='equal')

add(47, [
 code(('존재 검사 전', 'Before an Existence Check'), 'typescript', """
const products = [{ id: 'note', price: 3000 }];
const found = products.find((p) => p.id === 'missing');
console.log(found.price);
""", errors=[18048]),
 code(('존재 검사 후', 'After an Existence Check'), 'typescript', """
const products = [{ id: 'note', price: 3000 }];
const found = products.find((p) => p.id === 'missing');
if (found === undefined) {
  console.log('product not found');
} else {
  console.log(found.price);
}
""", output='product not found')], ['practice', 'narrow'], layout='equal')

add(48, [
 code(('policies.ts · 공통 정책 계약', 'policies.ts · Shared Policy Contract'), 'typescript', """
type DiscountPolicy = (amount: number) => number;
const regularPrice: DiscountPolicy = (amount) => amount;
const memberPrice: DiscountPolicy = (amount) =>
  Math.floor(amount * 0.9);
console.log(regularPrice(6000));
console.log(memberPrice(6000));
console.log(memberPrice(3001));
""", output='6000\n5400\n2700'),
 points(('정책 전달', 'Policy Passing'),
  ('main.ts · 일반 또는 회원 정책 선택', 'main.ts · Selects the regular or member policy'),
  ('createOrder · 정책 함수 전달', 'createOrder · Receives the policy function'),
  ('policy(subtotal) · 결제 금액 반환', 'policy(subtotal) · Returns the payable amount'))], ['practice'], layout='split')

add(49, [
 code(('adapters.ts · 검증 이후의 변환', 'adapters.ts · Conversion After Validation'), 'typescript', """
function toProduct(raw: ApiProduct): Product {
  return {
    id: raw.id,
    name: raw.product_name,
    price: raw.unit_price,
    stock: raw.stock
  };
}
""", prelude='type ApiProduct = { id: string; product_name: string; unit_price: number; stock: number };\ntype Product = { id: string; name: string; price: number; stock: number };'),
 table(('fixture와 기대 결과', 'Fixtures and Expected Results'),
  [('주소의 쿼리', 'URL Query'), ('기대 결과', 'Expected Result')], [
  [('?fixture=valid', '?fixture=valid'), ('검증 → 변환 → 상품 표시', 'Validate → Adapt → Display')],
  [('?fixture=missing', '?fixture=missing'), ('필드 누락으로 검증 실패', 'Validation fails: missing field')],
  [('?fixture=wrong', '?fixture=wrong'), ('문자열 가격으로 검증 실패', 'Validation fails: string price')]])], ['practice'], layout='split')

add(50, [
 table(('검증 시나리오', 'Verification Scenarios'),
  [('시나리오', 'Scenario'), ('기대 결과', 'Expected Result')], [
  [('노트 2개 · 일반 / 회원', 'Two notebooks · Regular / Member'), ('6,000원 / 5,400원', '6,000 / 5,400 won')],
  [('0 · 음수 · 소수 · 재고 초과', 'Zero · Negative · Fraction · Over stock'), ('주문 요청 전 거부', 'Reject before sending an order')],
  [('없는 상품 ID · 품절 상품', 'Unknown product ID · Out of stock'), ('실패 결과 반환', 'Return a failure result')],
  [('요청 실패 → 체크 해제 → 재시도', 'Request failure → Uncheck → Retry'), ('오류 표시 → 버튼 복구 → 성공', 'Error → Button restored → Success')]]),
 points(('자동 검사와 화면 검사', 'Automated and UI Checks'),
  ('npm run check · 타입 검사', 'npm run check · Type checking'),
  ('npm test · 계산과 경계값 검사', 'npm test · Calculation and boundary checks'),
  ('브라우저 · 중복 제출 방지와 실패 후 복구', 'Browser · Duplicate prevention and failure recovery'))], ['practice'], layout='split')

add(51, [
 flow(('AI 코드 검토 절차', 'AI Code Review Procedure'),
  ('실행 전 결과와 타입 예측', 'Predict results and types before execution'),
  ('특정 줄의 설명과 반례 요청', 'Request an explanation and counterexamples'),
  ('변경 전후 비교와 직접 수정', 'Compare changes and edit deliberately'),
  ('반례 실행과 결과 기록', 'Run counterexamples and record results')),
 points(('검토 예시 · 수량 변환', 'Review Example · Quantity Conversion'),
  ('제안 · Number 대신 parseInt 사용', 'Suggestion · Use parseInt instead of Number'),
  ('반례 · parseInt("2abc") → 2', 'Counterexample · parseInt("2abc") → 2'),
  ('판단 · 잘못된 수량 문자열 허용으로 제안 거절', 'Decision · Reject because invalid quantity strings are accepted'))], ['practice'], layout='split')

add(52, [
 table(('제출물', 'Deliverables'),
  [('자료', 'Item'), ('내용', 'Contents')], [
  [('소스 코드', 'Source code'), ('필수 TODO 구현 · 실행 안내 · 잠금 파일', 'Required TODOs · Run instructions · Lockfile')],
  [('review.md', 'review.md'), ('예측 · 실제 결과 · 수정 원인', 'Predictions · Observations · Reasons for changes')],
  [('검증 결과', 'Verification results'), ('타입 검사 · 기능 검사 · 브라우저 실패 시나리오', 'Type checks · Behavior tests · Browser failures')]]),
 points(('코드 설명 기준', 'Code Explanation Criteria'),
  ('입력 → 검증 → 계산 → 요청 → 화면 추적', 'Trace input → Validation → Calculation → Request → UI'),
  ('타입 검사로 찾은 오류 설명', 'Explain an error caught by type checking'),
  ('실행 검증이 필요한 오류 설명', 'Explain an error requiring runtime validation'))], ['practice'], layout='split')

assert set(BODY) == {str(n) for n in range(1,53)}
(ROOT/'materials/lesson-body.json').write_text(json.dumps({'sources':SOURCES,'slides':BODY},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Authored all 52 topic bodies; covers and chapter dividers remain code-free.')
