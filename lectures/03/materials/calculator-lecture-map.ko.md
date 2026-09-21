# 3주차 강의와 기본 계산기 코드 연결

기준은 [pwd-week3](https://github.com/ajou-hyunseok-oh/pwd-week3)의 기본 계산기입니다. 2026-09-19 확인한 커밋은 `a321051435d95970ac6e082b933fd49464b7e974`이며, 실제 세 TypeScript 파일을 [스냅샷](practice-source/)으로 보관합니다.

## 강의에서 실습으로 이어지는 순서

한 번의 `12 + 3 =` 계산을 서로 다른 관점에서 다시 읽습니다. 초반에는 문자열과 숫자, 중반에는 타입 계약, 후반에는 상태 변화와 함수 호출 관계를 설명합니다. 후반 실습 안내에서 새로운 프로젝트를 다시 소개하지 않고 이미 읽은 파일을 직접 작성하도록 연결합니다.

| 주제 번호 | 실제 슬라이드 | 코드·개념 | 학생이 연결할 동작 |
| --- | --- | --- | --- |
| 01, 03–08 | 03, 05, 07–12 | HTML/CSS/JS 역할, input, Number, setResult, formatNumber | 숫자 키 1과 2가 문자열 12가 되는 과정 |
| 09–13 | 13–17 | 클릭 콜백, button 클로저, state, dataset.key | 버튼 하나에서 handleKey와 render 호출 |
| 15–17 | 21–23 | 함수 전달, 속성 오타, 타입 검사와 실행 검사 | add 함수 교체, 0 나누기와 무한대 처리 |
| 19–25 | 26, 28–33 | 타입 제거, BinaryOperation, CalculatorState, Operator, null 검사 | 컴파일 결과와 연산 가능 조건 |
| 30–33 | 40–43 | 이벤트·상태·화면, 최소 상태·파생 값, 명령형·선언형, 계산·부수 효과 | 간단한 숫자 입력과 덧셈을 연결한 개념 예제 |
| 39–40 | 48–49 | 세 파일의 책임, operations, calculate | 역할 분리와 공통 호출을 통한 연산 교체 |
| 실습 개요 (번호 없음) | 50 | 학습 목표·요구사항·참고 저장소·제출 안내 | 계산기 구현·검증과 GitHub Pages 배포 |

주제 번호는 `sourcePage`이며 실제 슬라이드 번호와 다릅니다. 전체 제목은 [50장 목록](week-03-slide-draft.ko.md)에 있습니다.

## 실제 호출 흐름

```text
버튼 클릭
  → app.ts: button.dataset.key → handleKey(key)
  → calculator.ts: inputDigit / selectOperator / equals
  → operations.ts: calculate(left, right, operations[operator])
  → calculator.ts: setResult와 상태 정리
  → app.ts: render → 표시창·계산식·오류 DOM 갱신
```

숫자 키는 문자열로 이어 붙입니다. 계산할 때 Number로 바꾸고 결과는 String으로 저장합니다. 기다림 상태의 표시에는 formatNumber가 적용되고, formatDisplay가 정수 부분에 쉼표를 넣습니다.

오류 흐름은 `divide의 throw → handleKey의 catch → state.error → render`입니다. 오류 뒤 숫자 키를 누르면 inputDigit이 clear를 호출해 새 입력을 시작합니다.

## 실제 구현과 비교 예제의 경계

| 개념 | 현재 실습 | 강의 비교 |
| --- | --- | --- |
| 일급 함수·Strategy | BinaryOperation, operations, calculate | 함수 선택으로 연산 교체 |
| 순수 함수·상태 | 계산·표시 함수와 전역 state | 모든 함수가 순수한 것은 아님 |
| 상태·파생 값 | 입력 등은 state, 표시 문자열은 formatDisplay에서 생성 | 31: 정수 입력의 쉼표 표시로 단순화한 예제 |
| 모듈 | module: none, defer 스크립트 순서 | 54·55: JavaScript 모듈과 TypeScript 타입 공유 |
| 비동기 | 계산과 render는 동기 실행 | 14: HTTP 예제 · 패러다임 챕터에서는 제외 |
| 선언형 UI | 상태 변경 후 render 직접 호출 | 32: DOM 변경 코드와 React Display 비교 |
| 제네릭·외부 데이터 | DOM 타입 인수, catch 오류 좁히기 | 26–28: 일반 타입 관계·데이터 검증 |
| Adapter | 외부 API 연동 없음 | 38: 주요 패턴 비교에서 외부 상품 형식 연결 사례로 소개 |

`formatDisplay`는 표시 함수입니다. 형식이 바뀐다는 이유만으로 Adapter 구현이라고 설명하지 않습니다. 현재 과제에는 공학 함수·이력 클래스·Result<T>·TODO 채우기·모의 주문 요청이 없습니다.

## 발췌와 검증

코드는 세 파일에서 추출하고 독립된 줄 주석을 생략한 뒤 포맷하여 검은 배경·녹색 Consolas로 표시합니다. 실행 구문은 유지하며, 코드 제목과 설명은 각 슬라이드의 개념에 맞춥니다. “실습 원본”, “함수 내부 발췌”, “별도 예제” 같은 출처·제작 문구는 표시하지 않습니다. 파일명은 모듈이나 빌드 구조의 설명에 필요한 곳에서만 사용합니다. 파일·줄 출처와 재구성 여부는 작성 메타데이터와 검토 문서에 보관합니다.

`check-practice.cjs`는 6개 발췌의 일치, 세 파일의 strict 타입 검사, 실제 클릭 콜백과 17개 입력 시퀀스, 상태 표, 오류 복구, 순수성, 입력 제한을 검사합니다. 자세한 명령은 [자료 안내](README.md)를 따릅니다.

2026-09-21: 조건문 다음에 배열과 객체 개념 슬라이드(실제 10번, 주제 ID 53)를 추가했습니다. 기존 10번 이후의 화면 페이지는 한 장씩 뒤로 이동하며 주제 ID는 유지합니다.
