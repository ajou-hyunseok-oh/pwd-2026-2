# 3주차 본문 작성과 검증 기록

작성일: 2026-09-17

## 작성 기준

- 사용자 확정 제목·서브타이틀과 61장 구성을 그대로 유지. 해시 검사로 제목 원본 보존 확인.
- 공식 문서의 문법·예제 구조를 참고해 상품 주문 맥락의 짧은 예제를 새로 작성. 원문 예제의 그대로 인용이나 당시 역사 코드의 재현으로 제시하지 않음.
- Microsoft TypeScript Handbook, 브라우저 개발사 문서인 MDN, React·Vue 공식 가이드, Ecma 표준 자료와 언어 설계자의 역사 논문 사용.
- 코드가 있는 슬라이드는 입력·처리·출력 또는 오류를 설명. 역사, 역할 비교, 검증 흐름, 제출 안내는 표와 흐름도 중심.
- 강의 예제의 상품명은 동일 코드로 읽을 수 있는 Notebook 등 영문 데이터 사용. 설명·표·레이블은 한·영 번역. 실제 실습 fixture는 한국어 상품명 사용.
- 예제는 독립된 ES 모듈 기준. 발췌 코드의 제공 함수 계약은 검증 메타데이터에 기록. React·Vue 문법은 코드 레이블로 구분.
- Strategy·Adapter 구조와 실습 단계는 수업용 설계. 언어 문서에서 규정하는 필수 패턴으로 설명하지 않음.
- 원안 45의 검증 예제는 검사 순서 발췌. 실제 실습에서는 제공된 Result<number> 반환 계약을 사용.

## 페이지별 자료와 적용 방식

아래 원안 번호는 기존 구성안 및 실습 안내의 번호이며 실제 슬라이드 번호와 구분한다. 각 참고 링크는 해당 슬라이드 하단에도 표시한다.

| 실제 슬라이드 | 원안 | 제목 | 표현 | 참고 자료 |
|---|---|---|---|---|
| 03 | 01 | 웹 문서와 프로그램의 역할 | 표 · 흐름 · 설명 | [MDN · Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types) |
| 04 | 02 | JavaScript의 탄생 | 표 · 흐름 · 설명 | [JavaScript: The First 20 Years](https://www.cs.tufts.edu/comp/150FP/archive/brendan-eich/js-hopl.pdf) |
| 05 | 03 | ECMAScript 표준화 | 코드 + 설명 | [Ecma · ECMA-262](https://ecma-international.org/publications-and-standards/standards/ecma-262/) |
| 07 | 04 | 값 · 타입 · 변수 | 코드 + 설명 | [MDN · Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types) |
| 08 | 05 | 연산자와 형 변환 | 코드 + 설명 | [MDN · Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types) |
| 09 | 06 | 조건문과 입력 검증 | 코드 + 설명 | [MDN · Control Flow](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling) |
| 10 | 07 | 배열과 반복문 | 코드 + 설명 | [MDN · Loops and Iteration](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Loops_and_iteration) |
| 11 | 08 | 함수와 블록 스코프 | 코드 + 설명 | [MDN · Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions), [MDN · Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types) |
| 12 | 09 | 일급 함수 · 콜백 · 클로저 | 코드 + 설명 | [MDN · Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions) |
| 13 | 10 | 객체 리터럴과 멤버 | 코드 + 설명 | [MDN · Working with Objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects) |
| 14 | 11 | 객체 참조와 얕은 복사 | 코드 + 설명 | [MDN · Spread Syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) |
| 15 | 12 | filter · map의 목록 변환 | 코드 + 설명 | [MDN · Array.filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [MDN · Array.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) |
| 16 | 13 | DOM 이벤트와 입력 처리 | 코드 + 설명 | [MDN · addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) |
| 17 | 14 | Promise와 async/await | 코드 + 설명 | [MDN · Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) |
| 19 | 15 | 동적 타입과 코드 조합 | 코드 + 설명 | [MDN · Array.filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [MDN · Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions) |
| 20 | 16 | 형 변환 · 오타 · 공유 상태 오류 | 코드 + 설명 | [TypeScript · The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html), [MDN · Spread Syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) |
| 21 | 17 | 타입 검사와 실행 시 검증 | 표 · 흐름 · 설명 | [TypeScript · The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) |
| 23 | 18 | TypeScript의 등장 배경 | 표 · 흐름 · 설명 | [Microsoft · Ten Years of TypeScript](https://devblogs.microsoft.com/typescript/ten-years-of-typescript/), [TypeScript · The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) |
| 24 | 19 | 정적 타입 검사와 코드 변환 | 코드 + 설명 | [TypeScript · The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) |
| 26 | 20 | 타입 표기와 추론 | 코드 + 설명 | [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) |
| 27 | 21 | 함수의 매개변수 · 반환 타입 | 코드 + 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html) |
| 28 | 22 | 객체 타입: type · interface | 코드 + 설명 | [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) |
| 29 | 23 | 리터럴 타입과 유니온 | 코드 + 설명 | [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) |
| 30 | 24 | 선택적 속성과 undefined | 코드 + 설명 | [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) |
| 31 | 25 | 조건문과 타입 좁히기 | 코드 + 설명 | [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) |
| 32 | 26 | any와 unknown | 코드 + 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html) |
| 33 | 27 | 타입 단언과 데이터 검증 | 코드 + 설명 | [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) |
| 34 | 28 | 제네릭과 타입 관계 | 코드 + 설명 | [TypeScript · Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) |
| 35 | 29 | 모듈과 구조적 타입 | 코드 + 설명 | [TypeScript · Modules](https://www.typescriptlang.org/docs/handbook/2/modules.html), [TypeScript · Type Compatibility](https://www.typescriptlang.org/docs/handbook/type-compatibility.html) |
| 37 | 30 | 명령형 · 절차적 주문 처리 | 코드 + 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html), [MDN · Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) |
| 38 | 31 | 순수 함수와 불변성 | 코드 + 설명 | [React · Keeping Components Pure](https://react.dev/learn/keeping-components-pure) |
| 39 | 32 | 캡슐화와 장바구니 상태 | 코드 + 설명 | [TypeScript · Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html) |
| 40 | 33 | 이벤트와 비동기 실행 | 코드 + 설명 | [MDN · addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener), [MDN · Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) |
| 41 | 34 | 선언형 UI와 반응형 계산 | 코드 + 설명 | [React · Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state), [Vue · Computed Properties](https://vuejs.org/guide/essentials/computed.html) |
| 42 | 35 | 패러다임 조합과 책임 분리 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |
| 44 | 36 | 할인 정책과 Strategy 패턴 | 코드 + 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html) |
| 45 | 37 | 함수 타입과 정책 교체 | 코드 + 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html) |
| 46 | 38 | 상품 형식과 Adapter 패턴 | 코드 + 설명 | [TypeScript · Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html), [실습 README / Lab README](../practice/README.md) |
| 47 | 39 | 입력 검증과 형식 변환 | 표 · 흐름 · 설명 | [MDN · Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) |
| 48 | 40 | Strategy · Adapter 적용 기준 | 표 · 흐름 · 설명 | [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html), [실습 README / Lab README](../practice/README.md) |
| 50 | 41 | 실습 화면과 요구사항 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |
| 51 | 42 | 실습 데이터와 주문 흐름 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |
| 52 | 43 | 프로젝트 구조와 실행 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md) |
| 53 | 44 | JavaScript 오류 재현 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md) |
| 54 | 45 | 수량 변환과 검증 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md) |
| 55 | 46 | 주문 코드의 TypeScript 전환 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md), [TypeScript · The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) |
| 56 | 47 | 타입 오류와 undefined 처리 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md), [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) |
| 57 | 48 | 할인 정책 분리 실습 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md) |
| 58 | 49 | Adapter 확장 실습 | 코드 + 설명 | [실습 README / Lab README](../practice/README.md) |
| 59 | 50 | 정상 · 실패 · 경계 검증 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |
| 60 | 51 | AI 코드 예측과 검토 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |
| 61 | 52 | 제출물과 코드 설명 | 표 · 흐름 · 설명 | [실습 README / Lab README](../practice/README.md) |

## 검증 결과

- 본문 52장 전체 작성. 코드 블록 47개: JavaScript·TypeScript·TSX 46개와 터미널 안내 1개. 표지 9장에는 코드 없음.
- `npm test --prefix packages/web-deck` 통과: 전체 13개 강의 구조·번역·리소스와 84개 코드 블록(166개 언어 변형) 서식·구문 검사.
- `npm run format:code --prefix packages/web-deck` 통과: JSON 형식 번역 원본도 지원하도록 공용 포매터 보완.
- `check-examples.cjs` 통과: 확정 제목 해시, TypeScript·TSX 모듈 29개, 의도된 타입 오류 4개, 실행 시나리오 45개.
- 실제 React 19.1.1 요소의 disabled·children과 Vue 3.5.21 computed의 6,000 → 9,000 갱신 확인. React 전체 앱 마운트 검증은 포함하지 않음.
- DOM 콜백 등록 시 미실행·클릭 시 실행, Fetch 성공·HTTP 오류·네트워크 오류, 늦은 이전 응답 무시 확인.
- `check-slides.cjs` 통과: KO/EN 각 61장 화면·인쇄 총 244개 상태에서 글자 잘림·코드 가로 넘침·본문과 하단 설명의 겹침 없음.
- 모바일 375px에서 한·영 122개 슬라이드 이동과 페이지 가로 넘침 없음. 긴 코드는 코드 영역에서 가로 스크롤.
- 코드 테마의 계산 스타일 확인: 검정 rgb(0, 0, 0), 녹색 rgb(0, 255, 0), Consolas 우선, 인쇄 14px.
- 수량 검증·React/Vue 등 대표 화면 캡처 직접 확인. 의도된 오류를 제외한 미처리 브라우저 예외 없음.

## 재현 환경과 한계

Node.js 24.12.0 · TypeScript 5.9.3 · 로컬 Chrome/Playwright. 실행 명령과 검증용 의존성 설치는 [README](README.md)에 기록. 네트워크 요청은 고정 응답과 실패 모의 코드로 검증하며 실제 외부 결제나 운영 서버에 요청하지 않음. 인쇄 검증은 브라우저의 print 미디어 배치 검사이며 물리 프린터 검증은 아님.

## 강의 화면 문구 정리 (2026-09-17)

- 표지·챕터 9장과 주제 52장 전체 검토. 확정 제목·서브타이틀 유지.
- 52개 하단 보충 설명 제거. 본문 반복, 제작 메모, 이후 내용·범위 예고 삭제.
- 본문 목록 171개 → 133개. 직접적인 개념과 코드 해석에 필요한 설명으로 축약.
- 첫 주제의 역할 도식·설명은 표 하나로 통합. JavaScript 역사 페이지의 중복 설명 제거.
- 절차 목록의 본문 번호와 자동 번호 중복 제거. 코드 오류 표시는 실제 오류 정보만 유지.
- 공식 자료 출처와 실습 실행 명령 유지. 코드 예제와 검증용 메타데이터 변경 없음.
- 전체 재생성 후 공용 검증, 예제 검증, 한·영 화면·인쇄·모바일 배치 검사 통과.
