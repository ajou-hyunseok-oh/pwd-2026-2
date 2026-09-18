# 강사용 운영 및 해설

## 운영

슬라이드 소개 30분과 별도로 구현·리뷰 90분을 권장한다. HTML·CSS와 DOM 연결 코드는 완성해 제공하며 학생은 `src/order.ts`, `src/policies.ts`를 수정한다. 선택 과제는 `src/adapters.ts`다. `solution/`은 비교용으로 분리되어 있고 학생 화면에서 import하지 않는다. 학생에게 배포할 때 해설을 숨기려면 복사본에서 `solution/`과 이 문서를 제외한다. 필수 실행·검증에는 지장이 없다.

```sh
npm ci
npm run check
npm run test:solution
```

완성 예제를 브라우저에서 시연하려면 별도의 프로젝트 복사본을 만들고 `solution`의 세 파일을 `src`의 동명 파일에 복사한다. 복사한 파일의 타입 import 경로를 `../src/types.js`에서 `./types.js`로 바꾼 뒤 `npm start`로 실행한다. 원본 시작 코드는 그대로 보관한다.

## 단계별 해설

- 오류 A는 문자열 `31`, B는 `NaN`, C는 `TypeError`, D는 숫자 `0`이다. D는 `const` 재할당과 객체 변경이 다름을 드러낸다. TS도 공유 객체 변경 자체를 막지 않는다.
- TODO 1: `trim`으로 공백을 검사한다. `Number('')`는 0이므로 변환과 유효성을 구분한다. `parseInt('2abc')`처럼 잘못된 일부 문자열을 허용하지 않는다. `Number.isFinite`, `Number.isInteger`, 양수·재고 조건을 연결한다.
- TODO 2: 입력을 변경하지 않는 곱셈이다. 검증된 입력에 대한 순수 계산과 외부 입력 검증의 책임을 구분한다.
- TODO 3: `find()`의 `undefined`와 `Result` 유니온을 각각 좁힌다. `result.ok` 확인 후에만 `data`에 접근한다. 정책 호출은 성공 경로에 한 번만 있다.
- TODO 4: `DiscountPolicy`는 할인액이 아니라 결제 금액을 반환하는 계약이다. 회원 노트 2개는 5,400원이다. 타입만으로 10% 규칙의 정확성은 검사할 수 없다.
- TODO 5: 검증된 `ApiProduct`를 내부 `Product`로 변환한다. 필드 누락·문자열 가격은 검증 단계에서 실패한다. Adapter는 타입 단언이 아니다.
- `Result<T>`는 입력한 구체 타입에 따라 `data` 타입이 달라지는 읽기 예제다. 제네릭을 직접 새로 설계하게 하지는 않는다.
- `main.ts`는 이벤트·절차적 흐름, `order.ts`는 순수 계산, `ui.ts`는 명령형 DOM 갱신이다. 클래스나 프레임워크를 억지로 추가하지 않는다.

## 추가 읽기 활동

필수 구현 완료 후 구두 리뷰에 사용한다. 구현 범위를 늘리지 않는다.

```ts
function sum(amounts: number[]): number {
  let total = 0;
  for (const amount of amounts) total += amount;
  return total;
}
const makeDiscount = (rate: number) => (amount: number) => Math.floor(amount * (1 - rate));
const member = makeDiscount(0.1);
```

`sum([3000, 1500])`은 4,500이다. 지역 누적 변수는 외부 상태를 바꾸지 않는다. `member(6000)`은 5,400이며 반환 함수는 바깥의 `rate`에 접근한다. 다음 코드에서는 스프레드가 얕은 복사이므로 `original.stock.count`도 0이 된다.

```ts
const original = { stock: { count: 5 } };
const copied = { ...original };
copied.stock.count = 0;
```

## 검증 범위

필수 자동 검증은 정상·경계 수량, 없는 상품·품절·재고 초과, 가격 정책, 정책 전달, 입력 불변성을 확인한다. 선택 검증은 fixture와 검증기·Adapter를 확인한다. 시작 코드의 자동 검증 실패는 의도된 상태이며 정답을 자동으로 채워 넣지 않는다.

화면 검증: 초기 상품 3개/선택 2개, 일반·회원 결과, 오류 문구, 빠른 연속 제출, 요청 중 버튼 비활성화, 요청 실패 후 복구, 상품 조회 실패 후 재조회, 선택 fixture 성공·실패를 확인한다. 주문 모의 함수는 데이터를 서버에 저장하지 않고 재고를 차감하지 않는다.

타입 실험은 세 오류가 나타나는지 확인하고, 학생이 `any`·단언·`!`로 숨기지 않았는지 리뷰한다. 정답과 코드 모양이 달라도 계약과 요구 동작을 충족하면 인정한다.

## 제작 시 확인 결과 (2026-09-17)

- Node.js 24.12.0, TypeScript 5.9.3에서 `npm run check` 통과.
- `npm run test:solution`: 28개 통과. 시작 코드의 `npm test`: 14개 통과, 미구현 관련 10개 실패(의도된 상태).
- JavaScript 오류 재현: `31`, `NaN`, `TypeError`, `0` 확인.
- Chrome 자동화로 시작 화면의 상품 3개/선택 2개와 TODO 안내 확인.
- 완성 모듈을 브라우저 요청에 대체 주입해 일반·회원 금액, 잘못된 수량 8종, 요청 중 버튼 비활성화, 주문 실패 후 재시도, 상품 조회 실패 후 복구, fixture 3종을 확인. 학생 소스는 변경하지 않음.
- 375px 화면의 가로 넘침 없음, 확인 중 브라우저 미처리 예외 없음.

빠른 이중 제출은 제공된 `busy` 가드와 버튼 비활성화 코드를 읽고 수업 중 수동 체크리스트로도 확인한다. 위 검증은 실제 결제·원격 배포 검증을 포함하지 않는다.
