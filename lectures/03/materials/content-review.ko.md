# 3주차 강의 최종 검토와 검증 기록

최종 검토: 2026-09-21. 현재 자료는 **50장(표지 1 + 챕터 7 + 본문 41 + 실습 개요 1)**의 한·영 HTML 강의입니다. 아래의 과거 작업 기록에 등장하는 61장, Vue, 삭제된 예제와 이전 검사 수치는 현재판의 구성이 아닙니다.

## 현재판 수정 사항

- 실제 12·26번: 유효숫자 12자리 반올림은 표시용이며 원래 계산값의 정밀도를 높이지 않는다는 설명을 한·영으로 추가.
- 실제 14번: JavaScript 객체 리터럴에서 TypeScript 타입 표기를 제거. 원본 출처와 재구성 내역은 메타데이터에 유지하며 원문 발췌 검사와 구분.
- 실제 18번: 최상위 await의 모듈 실행 조건과 HTTP 서버·type="module" 사용 안내 추가. 검증 도구도 async 래퍼 적용 전에 일반 스크립트와 모듈의 문법을 구분해 검사.
- 실제 20·21번: 고차 함수와 함수 전달을 중심으로 용어 정리. 영문 부제에 유연성과 형 변환·공유 상태의 오류라는 한글 의미를 반영.
- 실제 32번: 선택적 속성을 읽을 때 string | undefined임을 유지하고, 명시적 undefined 대입과 exactOptionalPropertyTypes 설정의 관계 설명.
- 실제 40번: HTML 요소 생성 후 실행한다는 전제와 non-null assertion(!)이 런타임 검사가 아니라는 설명 추가. 이후 DOM 예제에도 같은 전제 적용.
- 실제 42번: State-driven UI updates로 용어 정리. 부모의 상태 setter 호출이 새 input prop을 통한 재렌더링으로 이어지는 과정 명시.
- 실습 안내의 클래스·Vue 예제 언급을 현재 구성에 맞게 수정. 모듈 연결표를 주제 54·55로 갱신.

## 현재판 검증 결과

- 공용 강의 구조 검사: 13개 강의 통과.
- 공용 코드 서식·구문 검사: 79개 코드 블록 / 156개 언어 변형 통과.
- 독립 예제: 36개, TS/TSX 모듈 19개, 의도된 타입 진단 5개, 실행 검사 31회 통과.
- 실습: 원문 발췌 6개, strict 타입 검사, 클릭 콜백 20개, 입력 시퀀스 17개 통과.
- 실습 원본: 형제 pwd-week3 저장소와 TypeScript 스냅샷 3개 일치 확인.
- 브라우저: 한·영 50장씩 화면·인쇄 총 200개 상태와 모바일 이동 100개 검사 통과. 넘침·본문 겹침·미처리 예외 없음.
- 수정한 9개 슬라이드의 한·영 캡처를 직접 확인. 추가 설명의 배치와 챕터 부제 줄바꿈을 조정.
- 전체 한·영 부제의 화면·인쇄 한 줄 표시 확인. 기존 챕터 제목의 다중행 배치는 유지.
- 코드 테마: 검정 배경·녹색 Consolas, 인쇄 14px 유지.

재현 명령은 [자료 안내](README.md)를 따릅니다. 실습 저장소와 기존 계산 동작은 변경하지 않았습니다.

## 보완 내용의 공식 근거

- [ECMAScript 모듈](https://tc39.es/ecma262/multipage/ecmascript-language-scripts-and-modules.html#sec-modules): 최상위 await의 실행 문맥.
- [TypeScript exactOptionalPropertyTypes](https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html): 선택적 속성의 undefined 대입.
- [TypeScript non-null assertion](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#non-null-assertion-operator-postfix-): 런타임 검사와의 차이.
- [React State](https://react.dev/learn/state-a-components-memory): 상태 setter와 재렌더링.
- [TypeScript 함수 합성 예제](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#higher-order-type-inference-from-generic-functions): 고차 함수 전달과 함수 합성 용어의 구별.

---

## 과거 작업 기록 — 당시 구성과 검증 결과

아래 기록은 변경 이력을 보존하기 위한 것으로, 최신 장수·예제·검증 수치는 위의 현재판 기준을 따릅니다.

### 강의 코드 통합과 검증 기록

갱신일: 2026-09-19

## 기준과 적용 범위

실습 기준은 [pwd-week3 기본 계산기](https://github.com/ajou-hyunseok-oh/pwd-week3)입니다. 로컬 저장소가 변경 없는 상태인 것을 확인하고 커밋 [a321051](https://github.com/ajou-hyunseok-oh/pwd-week3/tree/a321051435d95970ac6e082b933fd49464b7e974)의 `operations.ts`, `calculator.ts`, `app.ts`를 사용했습니다. 실습 저장소 자체는 수정하지 않았습니다.

61장(표지 1 + 챕터 8 + 주제 52)과 개념 순서는 유지했습니다. 주문 실습에 종속된 제목·서브타이틀과 실습 안내는 기본 계산기로 갱신하고 제목 해시 기준도 함께 갱신했습니다. 강의에서 문자열 입력 → 타입 계약 → 상태 변화 → 함수 선택 → 화면 갱신을 단계적으로 소개합니다.

세 소스 파일은 `practice-source/`에 동일하게 보관합니다. 생성기는 지정된 줄 범위를 읽고 독립된 줄 주석을 생략한 뒤 포맷하여 슬라이드 안에 검은 배경·녹색 Consolas로 표시합니다. 실행 구문은 유지합니다. 원본 링크는 이 검토 문서와 작성 메타데이터에만 보관하며 슬라이드 하단에는 표시하지 않습니다. 실습 저장소가 없어도 강의 재생성과 검증이 가능합니다.

## 실제 소스 발췌

같은 함수를 서로 다른 개념에서 다시 읽는 경우도 포함합니다. 아래 슬라이드 번호는 표지와 챕터 표지를 포함한 실제 번호입니다.

| 슬라이드 | 주제 | 파일·원본 줄 |
| --- | --- | --- |
| 09 | 조건문 | [calculator.ts:64–71](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L64-L71) |
| 12 | 일급 함수 · 콜백 · 클로저 | [app.ts:22–31](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/app.ts#L22-L31) |
| 13 | 객체 리터럴과 프로퍼티 | [calculator.ts:12–20](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L12-L20) |
| 16 | DOM 이벤트 처리 | [app.ts:24–30](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/app.ts#L24-L30) |
| 24 | 정적 타입 검사와 컴파일 | [calculator.ts:22–24](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L22-L24) |
| 27 | 함수의 매개변수와 반환 타입 | [operations.ts:3–7](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/operations.ts#L3-L7) |
| 28 | 객체 타입 정의 | [calculator.ts:2–10](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L2-L10) |
| 29 | 리터럴 타입과 유니온 | [operations.ts:2–3](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/operations.ts#L2-L3) |
| 30 | 선택적 속성과 undefined | [app.ts:25–29](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/app.ts#L25-L29) |
| 31 | 조건문과 타입 좁히기 | [calculator.ts:84–93](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L84-L93) |
| 37 | 명령형 · 절차적 프로그래밍 | [calculator.ts:84–93](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L84-L93) |
| 38 | 순수 함수와 부수 효과 | [calculator.ts:22–24](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L22-L24) |
| 44 | Strategy 패턴 | [operations.ts:14–18](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/operations.ts#L14-L18) |
| 45 | Strategy의 선택과 실행 | [calculator.ts:73–82](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L73-L82) |
| 54 | 숫자 입력 처리 | [calculator.ts:53–61](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L53-L61) |
| 55 | TypeScript 컴파일과 타입 제거 | [operations.ts:2–7](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/operations.ts#L2-L7) |
| 56 | undefined 확인과 타입 오류 수정 | [app.ts:25–29](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/app.ts#L25-L29) |
| 57 | 예외 처리와 오류 복구 | [operations.ts:8–11](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/operations.ts#L8-L11) |
| 57 | 예외 처리와 오류 복구 | [calculator.ts:122–122](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/calculator.ts#L122-L122) |
| 58 | 상태와 DOM 갱신 | [app.ts:15–20](https://github.com/ajou-hyunseok-oh/pwd-week3/blob/a321051435d95970ac6e082b933fd49464b7e974/app.ts#L15-L20) |

JavaScript 단원의 타입 제거 예제, 잘못된 호출 실험, 입력 예측 코드는 실습을 바탕으로 재구성했습니다. 화면의 레이블은 코드의 역할과 개념을 설명합니다. 타입 오류 4개는 설명을 위한 의도된 오류입니다. 실제 소스에서 추출한 코드는 원본 프로그램의 문맥에서 검증합니다.

## 실습과 별도 예제 구분

- 실습은 `module: none`과 일반 `defer` 스크립트 세 개를 사용합니다. 모듈 단원의 import/export는 대안 비교이며 현재 실습에 적용된 구조로 설명하지 않습니다.
- 계산·상태 변경·render는 동기 실행입니다. HTTP, Promise, 늦은 응답 처리는 별도 서버 요청 예제입니다.
- 상태는 전역 객체입니다. 파일 분리를 캡슐화라고 설명하지 않으며 private 클래스를 별도 비교합니다.
- 실제 Strategy는 `BinaryOperation → operations → calculate`입니다. Adapter는 저장된 계산 입력을 불러오는 상황을 가정한 별도 확장 예제입니다.
- 화면 표시 함수 formatDisplay는 일반적인 포맷 함수입니다. 실습의 render 호출과 React/Vue의 선언형·반응형 처리를 구분합니다.
- DOM의 타입 인수와 non-null 단언은 요소 존재를 실행 시 검증하지 않습니다. HTML의 ID와 로딩 순서를 함께 확인합니다.
- 실습은 예외를 throw하고 catch에서 state.error에 저장합니다. 이전 공학용 실습의 Result<T>, TODO, 이력 클래스, 공학 함수를 현재 코드로 소개하지 않습니다.

공식 문서·원본 소스·실습 README의 하단 링크를 강의 화면에서 모두 제거했습니다. 근거 확인용 출처는 `lesson-body.json`의 `sources`와 `sourceUrl`, 이 검토 문서에 보관합니다. 실제 구현의 근거는 공개 실습 코드이며, 별도 문법·프레임워크 예제의 의미와 검증은 기존 공식 자료 및 실행 검사에 따릅니다.

## 검증 결과

- `build-slides.cjs`: 한·영 61장 재생성. Python 실행 파일은 `PYTHON` 또는 기본 `python3`.
- `npm test --prefix packages/web-deck`: 13개 강의 구조·번역·리소스 검사, 86개 코드 블록 / 170개 언어 변형 서식·구문 검사 통과.
- `check-examples.cjs`: 현재 제목 해시, 독립 코드 예제 28개, TypeScript·TSX 모듈 15개, 의도된 타입 진단 4개, 실행 검사 27개 통과. Fetch 성공·실패, React/Vue, 늦은 응답 포함.
- `check-practice.cjs`: 실제 발췌 20개 일치, 세 소스 파일 strict 타입 검사, 실제 클릭 콜백 20개, UI 입력 시퀀스 17개 통과.
- 실제 실습 저장소와 스냅샷이 바이트 단위로 같은지 확인.
- `12 + 3 =`의 4단계 상태 표, 오류 뒤 숫자 입력 복구, 소수점·12자리 제한, Strategy 함수 교체, 유한성 검사, 순수 함수의 상태 보존 확인.
- 코드의 실행 구문과 오류 메시지는 보존하고 독립된 줄 주석은 표시에서 생략. 강의 문체 검사는 코드 바깥 본문에 적용.

- `check-slides.cjs`: 한·영 61장씩 화면·인쇄 총 244개 상태에서 넘침·본문 겹침 0건. 모바일 375px에서 122개 슬라이드 이동과 페이지 가로 넘침 검사 통과.
- 한·영 대표 화면에서 실제 이벤트 코드, 상태 표, 절차, 오류 처리, 입력 검증, 경계 시나리오의 배치 직접 확인.
- 기존 검정 배경·녹색 Consolas, 인쇄 14px 유지. 미처리 브라우저 예외 없음.

검증 환경은 Node.js 26.8.2, TypeScript 5.9.3, Python 3, 로컬 Chrome/Playwright입니다. 실습 이벤트 검사는 실제 소스와 모의 DOM을 사용하고, 강의 화면은 실제 브라우저로 검사했습니다. 인쇄 검사는 print 미디어 배치 검사이며 물리 프린터 검사는 아닙니다. 재현 명령과 의존성은 [자료 안내](README.md)를 참고합니다.

## 폐기된 실습 예제 제거

실제 슬라이드 17·33·34·35·40·41·46·47번에 남아 있던 상품 조회, 가격 단언, 상품 배열·객체, 주문 버튼, 수량별 금액, 상품 Adapter를 제거했습니다. 각각 계산 예제 목록, 숫자 값 검증, 연산 배열·객체, 계산 버튼, 두 수의 반응형 덧셈, 저장된 피연산자 변환으로 교체했습니다. 한·영 제목·본문·실행 출력·검증 코드를 함께 갱신했습니다.

삭제된 `practice/` 폴더를 복구하지 않고 검증용 TypeScript 의존성을 `packages/web-deck`으로 이동했습니다. 슬라이드에는 원본·참고 링크를 표시하지 않으며 실제 코드는 검은 배경·녹색 Consolas로 유지합니다.

## 개념 중심 설명으로 정리

코드 패널 20곳의 파일명·원본·발췌 레이블을 개념에 맞는 제목으로 교체했습니다. 본문의 실습 위치 안내, 별도 예제라는 분류, 실제 구현과의 차이 안내를 제거하고 값·타입·함수·상태·처리 경계의 설명으로 바꿨습니다. 캡슐화는 메서드와 접근자, 책임 분리는 역할별 처리 방식, Adapter는 외부 필드와 내부 입력의 차이에 집중합니다. 모듈과 컴파일 구조에 필요한 파일명은 유지합니다. 원본 스냅샷과 실습 저장소는 수정하지 않았습니다.

## 제목·서브타이틀 전체 검토

표지 1장·챕터 표지 8장·본문 52장, 총 61장의 제목과 서브타이틀을 본문과 대조했습니다. 제목 36개를 핵심 개념에 맞게 수정했고 모든 서브타이틀을 학습 내용을 설명하는 한 줄로 정리했습니다. 한국어는 '~한다.' 종결과 마침표 없이 명사형 표현으로 작성합니다.

| 실제 슬라이드 | 기존 제목 또는 문제 | 수정한 제목·방향 |
| --- | --- | --- |
| 09 | 조건문과 결과 검증: 예제 용도를 학습 개념과 병렬 배치 | 조건문: 조건의 참·거짓에 따른 실행 흐름 설명 |
| 11 | 함수와 블록 스코프: 본문은 함수 매개변수의 범위 설명 | 함수와 스코프 |
| 13 | 객체 리터럴과 멤버: 서브타이틀에 본문에 없는 함수 보관 포함 | 객체 리터럴과 프로퍼티: 속성 읽기·변경 설명 |
| 19 | 동적 타입과 코드 조합: 본문은 함수 전달 예제 | 함수 값과 코드 조합 |
| 30 | 검색 결과의 존재 확인: 본문에 검색 예제 없음 | 선택적 속성과 undefined: 속성의 존재 확인 설명 |
| 37 | 명령형 · 절차적 계산 처리: 예제 용도가 제목에 포함 | 명령형 · 절차적 프로그래밍 |
| 40 | 이벤트와 비동기 실행: 본문은 응답 순서 제어 | 비동기 요청과 응답 순서 |
| 44·46 | 연산 선택·계산 입력 형식이 패턴명과 병렬 배치 | Strategy 패턴 · Adapter 패턴 |
| 55 | 계산 코드와 TypeScript 변환: 변환 방향이 모호 | TypeScript 컴파일과 타입 제거 |

제목은 핵심 개념을 명사구로, 서브타이틀은 배울 관계·동작을 설명하는 간결한 표현으로 작성합니다. 한국어 서브타이틀에는 '~한다.' 체를 사용하지 않습니다. 파일 위치·제작 안내·키워드 나열로 학습 설명을 대신하지 않습니다. 전체 목록은 [제목·서브타이틀 목록](week-03-slide-draft.ko.md)을 기준으로 확인합니다. 생성 원본과 제목 해시를 함께 갱신했습니다.

한·영 61장씩 화면·인쇄에서 서브타이틀이 한 줄로 표시되는 것을 확인했습니다. 영문 챕터 문장 5개는 글자 크기를 바꾸지 않고 축약했습니다. 전체 배치·모바일·코드 테마 검사와 공용 구조·번역 검사를 통과했습니다.

## 개념의 정의와 설명 보완

확정된 제목·서브타이틀·코드·실행 결과를 유지하고 본문 52장의 한·영 설명을 검토·수정했습니다. 표지와 챕터 표지는 유지했습니다. 설명은 용어의 정의, 작동 원리, 화면의 코드에 적용되는 의미 순으로 구성하고 단순한 동작 나열과 파일 작성 안내는 줄였습니다.

- 실제 17번: Promise를 작업의 향후 결과를 나타내는 객체로 먼저 정의하고 async 선언, await의 대기·결과 전달, 대기 중 이벤트 처리, HTTP 오류와 예외 처리의 차이를 설명합니다.
- 값·변수·스코프·콜백·클로저·객체 참조·얕은 복사·DOM은 개념을 정의한 뒤 코드의 변수와 동작을 연결합니다.
- 타입 표기·추론·유니온·타입 좁히기·제네릭·구조적 타이핑은 검사 기준과 허용 범위를 설명합니다. 타입 표기·단언·소거가 실행 중 값을 검사하거나 변환하지 않는다는 경계도 명시합니다.
- 명령형·절차형·선언형·반응형, 순수 함수·부수 효과, 캡슐화, Strategy·Adapter는 각 개념의 정의와 책임을 설명합니다.
- 요구사항·상태 전이·입력 처리·오류 복구·테스트·AI 검토는 동작 기준과 판단 원리를 설명합니다. 제출 안내의 필수 요건은 유지합니다.
- 코드 비교만 있던 슬라이드에는 각 코드 아래 짧은 설명을 추가했습니다. 코드 서식과 글자 크기를 바꾸지 않았고, 출처 링크나 실습 위치 안내를 강의 화면에 추가하지 않았습니다.

수정 전후 데이터 비교에서 제목 원본의 SHA-256 및 모든 코드 패널의 코드·출력·진단·검증 메타데이터가 동일했습니다. 설명을 제외한 코드 패널 변경은 0건입니다. 전체 구조·번역·코드 실행·실제 소스 발췌 검사, 한·영 화면·인쇄 244개 배치와 모바일 122개 상태 검사를 통과했습니다. 대표 화면은 Promise, 클로저, 타입 단언, 제네릭, 모듈, 응답 순서, 선언형·반응형, Adapter, 검증·변환, 예외 처리를 중심으로 확인했습니다.

## 04번 슬라이드 역사 부연 설명 (2026-09-20)

Brendan Eich의 [JavaScript at 20](https://brendaneich.github.io/ModernWeb.tw-2015/) 발표에서 1995년 5월 10일간 초기 구현을 작성한 사실과 파서·인터프리터 구현을 확인했습니다. “10일”은 첫 프로토타입의 구현 기간으로 표시했습니다. 한·영 본문에 동일하게 반영하고 출처 키 `js-origin-talk`를 추가했습니다.

## 05번 슬라이드 표준화 기관 설명 (2026-09-21)

[Ecma International의 Mission](https://ecma-international.org/mission/), [TC39 소개](https://ecma-international.org/technical-committees/tc39/), [ECMA-262](https://ecma-international.org/publications-and-standards/standards/ecma-262/)를 확인하여 기관·위원회·언어 사양·표준 문서 번호의 관계를 한·영 본문에 반영했습니다.


## 2026-09-21 · 웹 프로그래밍 패러다임 챕터 재구성

챕터 6의 표지(실제 39번)와 본문 6장(40–45번, 주제 ID 30–35)을 다시 작성했습니다. 앞선 날짜의 발췌·프레임워크·응답 순서 관련 기록은 당시 검증 이력이며, 현재 챕터 구성과 검증은 이 절을 기준으로 합니다.

기존 순서는 절차 코드, 순수 함수, private 문법, 요청 번호 비교, React/Vue 문법을 먼저 보여 주고 패러다임을 끝에서 정의했습니다. 개편본은 웹 기능 전체를 먼저 제시한 뒤 이벤트·비동기 → 명령형·선언형 → 함수형 → 객체지향 → 조합 순서로 설명합니다. 네 가지 설계 관점은 강의 목적에 따른 교육적 분류이며 공식 중요도 순위가 아닙니다. 비동기는 기다림의 실행 방식, 반응형은 의존 값 변화의 전파로 구분합니다.

동일한 계산기 맥락을 사용하되, 객체지향 클래스는 현재 실습의 전역 state에 대한 대안입니다. React의 선언형 UI도 직접 render를 호출하는 실습 구현과 구분합니다. 요청 번호, TypeScript private와 # 필드의 차이, Vue computed 문법은 이 챕터에서 제외했습니다. add와 Calculator의 짧은 코드 두 개만 남겨 핵심 개념을 뒷받침합니다. 입력·출력 설명은 함수형 전체의 엄밀한 정의를 대신하지 않으며 순수성·불변성·함수 조합을 함께 소개합니다.

### 조사 근거와 적용 위치

2026-09-21에 다음 공식 자료를 열어 확인했습니다. 근거 링크는 기존 강의 정책에 따라 화면 하단 대신 작성 메타데이터와 이 문서에 보관합니다.

- [MDN · JavaScript language overview](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Language_overview): 다중 패러다임 언어라는 전제 → 주제 30·35.
- [MDN · Introducing asynchronous JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Introducing): 기다리는 작업과 동기 작업의 차이, 이벤트 핸들러, 응답성 → 주제 31.
- [React · Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state): 직접 화면 변경과 상태 기반 선언의 차이 → 주제 32·35.
- [React · Keeping Components Pure](https://react.dev/learn/keeping-components-pure): 같은 입력의 결과, 외부 상태 변경과 부수 효과 분리 → 주제 33.
- [MDN · Object-oriented programming](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object-oriented_programming): 관련 데이터·동작을 객체로 묶는 관점과 캡슐화 → 주제 34.

### 현재 검증

- 한·영 64장 재생성, 챕터 밖 제목과 본문 유지.
- 공용 검사: 13개 강의 구조·번역·리소스와 88개 코드 블록 / 174개 언어 변형 통과.
- 독립 예제: 36개, TS/TSX 파일 18개, 의도한 진단 6개, 실행 30회 통과.
- 실습: 실제 발췌 14개 일치, strict 타입 검사, 클릭 콜백 20개와 입력 시퀀스 17개 통과.
- 삭제한 React/Vue·응답 역전 코드의 전용 검사도 제거. 새 순수 계산·객체 예제는 타입과 출력 검증에 포함.


## 2026-09-21 · 합의한 본문 4장 적용

사용자와 합의한 제목·개념을 기준으로 챕터 6을 다시 작성했습니다. 앞의 6장 개편안은 대체되었으며, 현재 구성은 챕터 표지 39번과 본문 40–43번(주제 ID 30–33)입니다. 전체는 62장입니다. 주제 ID 34·35는 제거하고 이후 ID를 보존했습니다.

1. 웹 프로그램의 동작 흐름: 클릭 → 입력 상태 → render. 숫자 2 버튼을 누르면 1 → 12.
2. 상태와 파생 값의 구분: 원본 입력 1234와 표시 문자열 1,234. 연산 결과도 후속 계산에 필요하면 상태가 될 수 있음을 명시.
3. 상태를 기준으로 화면 표현: TypeScript의 DOM 변경과 React Display의 JSX를 비교. render에 DOM 변경을 모으는 것과 선언형 구현을 구분.
4. 계산과 부수 효과의 분리: add는 값만 반환하고 클릭 콜백이 결과 저장·화면 반영을 수행.

본문 코드는 교육 목적의 독립된 계산기 예제입니다. 현재 실습 파일의 정확한 발췌로 표시하지 않습니다. DOM 예제는 버튼 하나와 output 하나가 존재하고 요소가 로드된 뒤 실행하는 문맥이며, 마지막 버튼은 현재 입력에 3을 더합니다. 정수 표시 함수는 파생 값 설명용으로서 입력 중인 소수점·끝자리 0을 보존하는 실습 formatDisplay의 대체 구현이 아닙니다. React 예제는 부모가 입력 상태를 prop으로 전달하는 문맥입니다. 학생의 실습 저장소는 수정하지 않았습니다.

근거: [Thinking in React](https://react.dev/learn/thinking-in-react)의 최소 상태와 소유, [The Elm Architecture](https://guide.elm-lang.org/architecture/)의 Model·Update·View, [Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)의 명령형·선언형 비교, [Keeping Components Pure](https://react.dev/learn/keeping-components-pure)의 계산과 부수 효과 분리. 출처는 작성 메타데이터에도 연결했습니다.

검증: 13개 강의 구조·번역 검사, 코드 91블록/180개 언어 변형, 독립 예제 39개/TS·TSX 파일 21개/실행 33회/의도한 진단 6개 통과. DOM 모의 객체로 초기 화면과 연속 클릭의 결과(1 → 12 → 122, 12 → 15 → 18)를 확인하고, add 반복 호출의 동일 결과와 상태 미변경, React Display에 서로 다른 입력 전달 결과를 검사했습니다. 실제 실습은 발췌 14개·클릭 콜백 20개·입력 시퀀스 17개 통과.

한·영 62장 화면·인쇄 총 248개 상태, 모바일 이동 124개 검사에서 넘침·겹침·미처리 예외 0건. 변경한 4장 한·영 화면을 직접 확인했습니다.

## 2026-09-21 · 챕터 07 디자인 패턴 입문 재구성

사용자가 선택한 간결한 안에 따라 표지와 본문 5장(주제 36–40)을 유지했습니다. 챕터는 ‘웹 프로그래밍과 디자인 패턴’으로 바꾸고, 개념·필요성 → 웹 설계 문제 → MVC·Observer·Strategy·Adapter 비교 → 계산기 역할 분리 → 실제 Strategy 순으로 재작성했습니다. 제목·서브타이틀은 기존 명사형 문체를 따르며 한·영 본문과 작성 원본, 제목 기준 해시를 함께 갱신했습니다.

Adapter 상세 구현·검증 단계는 비교 표로 축약했습니다. 계산기에 MVC·Observer·Adapter가 구현되어 있다고 설명하지 않습니다. Strategy는 practice-source/operations.ts의 실제 코드이며, 새 연산 추가 시 타입·버튼·입력 분기도 확인하도록 명시했습니다. 실습 소스는 변경하지 않았습니다.

검증: 패키지·13개 강의 구조, 코드 서식·구문, 13개 실습 발췌 일치 및 17개 입력 시퀀스, 38개 독립 코드 예제 검사 통과. 한·영 화면·인쇄·모바일 배치 검사를 수행하고 챕터 6장의 한·영 캡처를 검토했습니다.
