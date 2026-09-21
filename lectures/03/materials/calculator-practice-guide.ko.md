# 3주차 실습 · TypeScript 기본 계산기

현재 실습은 [pwd-week3 공개 저장소의 README](https://github.com/ajou-hyunseok-oh/pwd-week3#readme)를 따릅니다. 저장소는 완성본이며, 학생은 별도의 빈 폴더에 코드를 작성하면서 화면과 실행 흐름을 확인합니다.

## 진행 순서

1. 개발 환경 확인과 폴더 만들기.
2. TypeScript 설치와 설정: `package.json`, `tsconfig.json`, `.gitignore`.
3. `index.html`: 표시창과 `data-key` 버튼 작성.
4. `styles.css`: 4열 버튼 배치와 화면 꾸미기.
5. `operations.ts` → `calculator.ts` → `app.ts` 작성.
6. 타입 검사·컴파일 후 `index.html`을 브라우저에서 열기.
7. 계산·상태 변화·오류와 복구·좁은 화면 확인.
8. GitHub에 저장하고 GitHub Pages로 배포.

## 코드의 역할

| 파일 | 강의에서 먼저 읽을 내용 | 실습 중 확인 |
| --- | --- | --- |
| operations.ts | Operator, BinaryOperation, calculate | 숫자 두 개와 연산 함수를 받아 계산 |
| calculator.ts | CalculatorState, inputDigit, equals, handleKey | 문자열 입력과 숫자 계산, 상태 변화, 오류 저장 |
| app.ts | dataset.key, 클릭 콜백, render | 키 전달 후 DOM 갱신, 계산 값과 표시 형식 구분 |

실습은 `module: none`의 일반 스크립트입니다. 브라우저는 `operations.js → calculator.js → app.js` 순서로 읽으며 전역 범위를 공유합니다. 강의의 import/export와 React 화면 표현은 비교 예제이며, Adapter는 패턴 비교 표에서 소개합니다. 모듈 예제는 웹 서버와 `type="module"` 스크립트로 실행합니다.

## 실행과 검증

완성본을 내려받았다면 저장소 폴더에서 다음을 실행합니다.

```sh
npm ci
npm run check
npm run build
```

`index.html`을 브라우저에서 엽니다. 처음부터 작성하는 실습은 공개 README의 `npm install` 단계를 따릅니다. 이후에는 `.ts 수정 → 저장 → 빌드 성공 → 새로고침` 순서입니다. `npm run watch`는 자동 컴파일이며 브라우저는 직접 새로고침합니다.

각 시나리오 전에 AC를 누릅니다.

| 버튼 | 기대 결과 |
| --- | --- |
| 12 + 3 = / 12 − 3 = / 12 × 3 = / 12 ÷ 3 = | 15 / 9 / 36 / 4 |
| 12 ÷ 0 = → 7 | Error와 안내 → 새 입력 7 |
| 2 + 3 × 4 = | 20, 입력 순서대로 계산 |
| 2 + × 3 = | 6, 연산자 교체 |
| 2 + = / 2 + 3 = = | 2 / 5 |
| 200 + 10 % = | 200.1, 현재 숫자를 100으로 나누기 |
| 0.1 + 0.2 = | 화면 0.3, 내부 값과 표시를 구분 |
| 1.20 입력 / 123 → ⌫ / 6110000 입력 | 1.20 유지 / 12 / 6,110,000 |

## 완료와 제출

- HTML·CSS와 TypeScript 세 파일 작성, 타입 검사·빌드 통과.
- 배포된 계산기의 정상 동작과 오류 복구 확인.
- 배포에 필요한 `js/`를 Git에 포함하고 `node_modules/`는 제외.
- GitHub 저장소 URL과 GitHub Pages URL을 LMS에 제출. 마감은 9월 27일 오후 11시 59분.

강의의 번호별 연결은 [강의·코드 연결표](calculator-lecture-map.ko.md)를 참고합니다.
