# 3주차 실습 · TypeScript 공학용 계산기

제공된 HTML·CSS와 화면 처리 코드 위에 TypeScript 계산 기능을 구현합니다. 실행 결과를 예측하고 코드를 따라 읽으며 값과 타입, 함수, 제어 흐름, 개발 패러다임, Strategy 패턴을 복습합니다.

## 실행

Node.js와 npm이 설치된 터미널에서 실행합니다.

```sh
cd lectures/03/calculator
npm ci
npm start
```

- 학생용: <http://127.0.0.1:4305/>
- 완성 예제: <http://127.0.0.1:4305/demo>

완성 예제는 `solution/`의 계산 함수를 사용합니다. 학생용 소스를 덮어쓰지 않으며, HTML·CSS와 화면 처리 코드는 두 페이지가 공유합니다.

다른 터미널의 같은 폴더에서 `npm run watch`를 실행합니다. TypeScript 파일을 저장하고 컴파일 성공을 확인한 후 브라우저를 새로고침합니다. 자동 새로고침은 제공하지 않습니다. 서버와 감시는 각각 `Ctrl+C`로 종료합니다.

## 구현 범위

| 단계 | 수정 파일 | 구현 내용 |
| --- | --- | --- |
| TODO 1 | `src/validation.ts` | `parseNumber`: 공백 제거, 빈 입력 구분, 숫자 형식과 유한성 검증 |
| TODO 2 | `src/operations.ts` | `subtract`, `multiply`, `divide`: 사칙연산과 0 나누기 처리 |
| TODO 3 | `src/operations.ts` | `square`, `sqrt`: 제곱·제곱근과 음수 제곱근 처리 |

학생이 완성하는 파일은 위 두 개입니다. `add`, 삼각함수·로그함수, DEG/RAD 변환, 연산 선택, 결과 표시, 최근 계산 이력은 제공 코드로 읽습니다. 계산기를 조작하면서 해당 함수의 입력·반환값과 호출 순서를 설명합니다.

초기 코드는 컴파일되지만 TODO 함수가 `NOT_IMPLEMENTED` 오류를 반환하므로 계산은 완료되지 않습니다. 실패하는 테스트가 구현해야 할 동작을 나타냅니다.

## 입력·출력 규칙

- 한 번에 연산 하나를 선택합니다. 사칙연산은 `x`, `y`, 나머지 연산은 `x`만 사용합니다.
- 십진수, 부호, 소수, 지수 표기를 허용합니다. 예: `-2`, `.5`, `2.`, `1e3`.
- 빈 입력, `Infinity`, `NaN`, 16진수, 쉼표가 포함된 수, `2+3` 같은 식은 허용하지 않습니다. 제공된 `decimalPattern`을 사용합니다.
- 단항 연산에서는 사용하지 않는 `y` 입력을 검사하지 않습니다.
- 0으로 나누기, 음수의 제곱근, 0 이하의 로그는 오류입니다.
- 삼각함수는 DEG/RAD를 선택합니다. `tan`은 `|cos(각도)| ≤ 10⁻¹²`인 입력을 정의역 오류로 처리합니다. 이는 이 실습에서 정한 근사 판정 기준입니다.
- 계산 결과가 유한하지 않으면 오류입니다. 성공 값은 `number`로 보관하고 화면에서만 최대 유효 숫자 12자리로 표시합니다.
- 성공한 계산만 최신 5개까지 기록합니다. 입력 초기화와 이력 삭제는 별개이며, 새로고침하면 이력은 사라집니다.

실패는 예외를 던지는 대신 `Result<T>`의 `ok: false`로 반환합니다. `success`와 `failure` 보조 함수를 사용할 수 있습니다. 입력 오류의 코드는 `EMPTY_INPUT`, `INVALID_NUMBER`, 나누기 오류는 `DIVISION_BY_ZERO`, 제곱근 오류는 `DOMAIN`입니다.

## 검증

```sh
npm run check
npm run trace
npm test
```

`check`는 타입을 검사하고, `trace`는 값·형 변환 예제를 실행하며, `test`는 학생용 계산 함수를 검증합니다. 시작 코드의 테스트 실패는 의도된 상태입니다. 구현 후 53개 테스트를 모두 통과시킵니다. 강사용 완성 예제는 `npm run test:solution`으로 별도 검증합니다.

## 읽기 순서

1. `src/types.ts`: 입력, 연산 종류, 성공·실패 타입
2. `src/validation.ts`: 문자열을 검증한 숫자로 변환
3. `src/operations.ts`, `src/scientific.ts`: 계산 함수와 연산별 함수 목록
4. `src/calculator.ts`: 검증 → 함수 선택 → 실행 → 결과 반환
5. `src/app.ts`, `src/ui.ts`: 이벤트와 화면 갱신
6. `src/history.ts`: 계산 이력을 보관하는 객체

값과 타입은 [읽기·실행 기록지](review.md), 진행 방법과 해설은 [강사용 안내](instructor.md), 수업 개념과의 연결은 [강의 구성안](../materials/calculator-lecture-map.ko.md)을 참고합니다.

제출물은 수정한 두 TypeScript 파일과 리뷰 기록지입니다. `node_modules/`, `dist/`, 완성 예제 `solution/`은 제출 대상이 아닙니다.
