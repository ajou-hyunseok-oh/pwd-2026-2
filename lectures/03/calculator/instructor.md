# 공학용 계산기 · 강사용 안내

## 수업의 중심

실행되는 계산기 하나를 기준으로 입력과 반환값을 추적하고, 구현한 코드에서 패러다임과 패턴을 찾아 설명합니다. 학생의 필수 구현은 숫자 검증과 기본 연산이며, HTML·CSS·DOM 처리와 공학 함수는 제공 코드입니다.

`npm start` 후 `/demo`에서 완성 동작을 먼저 보여 줍니다. `/`는 학생용입니다. 완성 예제와 학생용은 `createCalculator`에 전달하는 함수만 다르고 동일한 화면을 사용합니다.

## 90분 실습 운영 예시

| 시간 | 활동 | 확인할 결과 |
| --- | --- | --- |
| 10분 | 완성 화면 조작, 입출력 규칙 확인 | `12 / 3`, `√9`, DEG `sin(30)`, `12 / 0`의 결과 |
| 15분 | 실행 결과 예측, 타입·호출 흐름 읽기 | 문자열과 숫자의 차이, `Result` 분기 |
| 30분 | TODO 1~3 구현 | 두 파일 수정, 타입 검사·테스트 통과 |
| 15분 | 실패·경계값 검증 | 빈 입력, 0 나누기, 음수 제곱근, 오버플로 |
| 20분 | 코드 리뷰, 패러다임·패턴 연결 | 순수 함수·명령형 흐름·상태·Strategy의 근거 설명 |

시간은 이 실습 구간의 예시입니다. 웹 프로그래밍 언어의 역사와 전체 문법 강의를 포함한 시간표가 아닙니다.

## 구현 해설

### 숫자 검증

`solution/validation.ts`는 `trim()` → 빈 값 검사 → 제공 정규식 검사 → `Number()` → `Number.isFinite()` 순서입니다. `Number('')`가 `0`이 되므로 빈 값 검사가 먼저 필요합니다. TypeScript의 `string` 타입만으로 문자열 내용이 올바른 숫자인지는 보장되지 않습니다.

정규식은 읽기 자료이며 학생이 새로 설계할 항목이 아닙니다. `parseFloat('12px')`처럼 일부 문자열만 숫자로 받아들이는 변환은 이 실습의 입력 규칙과 맞지 않습니다.

### 계산 함수

`solution/operations.ts`에서 함수는 숫자를 받아 `Result<number>`를 반환합니다. `divide`는 분모가 `0`인지, `sqrt`는 입력이 음수인지 먼저 확인합니다. 오류는 메시지가 있는 결과 값이며 브라우저 알림이나 DOM 변경을 계산 함수 안에 넣지 않습니다.

오버플로 검사는 공통 실행 함수 `src/calculator.ts`가 담당합니다. 연산 함수와 입력 검증 함수는 각자의 역할에 집중합니다. `Result<number>`라는 타입 자체가 유한한 숫자나 올바른 수학적 정의역을 보증하는 것은 아닙니다.

### 성공·실패와 타입 좁히기

`if (!x.ok) return x` 뒤에서는 `x.data`에 접근할 수 있습니다. `operation.kind`로 단항·이항 연산을 나누면 각 분기에서 `operation.id`가 해당 연산 ID로 좁혀집니다. 이 구조가 잘못된 함수 목록 접근을 타입 검사에서 발견하도록 돕습니다.

`reading/type-errors.ts.txt`의 세 오류는 유효한 연산 ID 선택, 숫자 인수 전달, `ok` 확인으로 수정합니다. `any`나 단언을 추가하는 수정은 타입 계약을 설명한 것으로 보지 않습니다.

## 코드와 수업 개념

| 개념 | 실제 코드 | 리뷰 질문 |
| --- | --- | --- |
| 명령형·절차적 처리 | `calculator.ts`의 검증·분기·실행·반환 | 오류가 발생하면 어디에서 멈추는가? |
| 순수 함수 | 계산 함수, `toRadians`, `formatNumber` | 같은 입력에서 같은 결과를 내며 외부 상태를 변경하지 않는가? |
| 일급 함수·클로저 | `createCalculator(parseNumber, strategies)` | 반환된 함수가 기억하는 값은 무엇인가? |
| 이벤트 기반 처리 | `app.ts`의 `submit`, `input`, `change` | 사용자 행동이 어떤 실행을 시작하는가? |
| 캡슐화 | `history.ts`의 `#entries`, `add/list/clear` | 이력의 외부 변경을 어떻게 제한하는가? |
| Strategy | `operations`와 함수 타입, 선택된 함수 호출 | 호출부를 유지한 채 어떤 함수를 교체할 수 있는가? |
| 책임 분리 | 계산, 상태, DOM 모듈 | 화면을 바꾸지 않고 계산을 검증할 수 있는가? |

`CalculationHistory`는 상태를 가진 객체이며 순수 함수가 아닙니다. 복사된 항목은 현재 문자열과 숫자만 포함하므로 얕은 복사로 외부 변경을 분리할 수 있습니다. 중첩 객체가 추가되면 이 전제를 다시 검토합니다.

이 계산기의 DOM 갱신은 명령형입니다. 선언형 UI·반응형 계산은 별도 프레임워크 예제로 비교합니다. 이벤트 콜백이 있다는 사실만으로 계산 함수가 비동기 함수가 되지는 않습니다. 비동기 요청·`unknown` 외부 데이터 검증도 별도 예제로 다룹니다. DEG/RAD 변환은 단위 변환이며 이를 곧바로 Adapter 패턴이라고 설명하지 않습니다.

## 수치와 표현의 범위

실수 범위의 JavaScript `number` 계산기입니다. `0.1 + 0.2`의 내부 값은 `0.30000000000000004`이며 화면의 `0.3`은 표시 자릿수 제한 결과입니다. 큰 정수의 정밀도 한계와 매우 작은 값의 언더플로까지 보정하는 정밀 계산기는 아닙니다.

삼각함수 입력은 라디안으로 바꿔 `Math` 함수에 전달합니다. `tan`의 `|cos(x)| ≤ 10⁻¹²` 판정은 수업용 정책입니다. 이 임계값 주변의 유한한 탄젠트 값도 거부할 수 있으며, 매우 큰 각도에서 정확한 특이점 판정을 보장하지 않습니다.

## 검증 기록

2026-09-17 기준:

- `npm run check`: 통과
- `npm run test:solution`: 53개 통과
- 학생용 시작 코드 `npm test`: 5개 통과, 48개 실패 — TODO로 인한 의도된 실패
- Chrome: 학생용 TODO 표시, 완성 계산·오류 복구, 단항/이항 입력, DEG/RAD, Enter 실행, 이력 제한·삭제, 새로고침 확인
- 데스크톱 1280px·모바일 375px: 화면 확인, 모바일 가로 넘침 없음

브라우저 검증은 개발용 선택 검사입니다. 실행 중인 계산기 서버, Chrome, Playwright가 필요합니다. `PLAYWRIGHT_PATH`에 설치된 Playwright 패키지 경로를 지정하거나 로컬에서 `require('playwright')`가 가능해야 합니다.

```sh
node tests/browser.cjs
```

`CALCULATOR_URL`로 기본 서버 주소 `http://127.0.0.1:4305`를 바꿀 수 있습니다. 캡처는 OS 임시 폴더의 `week3-calculator-review`에 생성합니다. 학생 필수 검증은 추가 브라우저 도구 없이 `npm run check`와 `npm test`로 수행합니다.

## 공식 자료와 재구성 범위

- [TypeScript · Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html): 판별 유니온과 조건에 따른 타입 좁히기. 실습의 `Result`와 `Operation`에 적용.
- [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html): 함수 타입, 함수 값 전달, 제네릭의 타입 관계. 실습의 Strategy와 `Result<T>`에 적용.
- [MDN · Math.sin](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sin): 라디안 입력과 도 단위 변환.
- [MDN · Math.sqrt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sqrt): 음수 입력의 `NaN` 결과. 실습은 이를 사전 검증하여 오류 값으로 반환.
- [MDN · Math.tan](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/tan): 탄젠트와 라디안 입력. 근사 임계값 정책은 실습 자체 규칙.

계산기 UI, 파일 구성, 이력, 입력 문법과 오류 계약은 이 수업을 위한 자체 예제입니다. 공식 문서가 동일한 프로젝트나 디자인 패턴 구성을 제공하는 것으로 설명하지 않습니다.
