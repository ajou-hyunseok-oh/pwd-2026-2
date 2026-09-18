# 03회차 자료

## 공학용 계산기 실습

현재 실습 기준은 TypeScript 공학용 계산기입니다. 실행 예제를 먼저 완성하고 코드의 실제 구조를 패러다임·디자인 패턴과 연결합니다.

- [실습 안내](calculator-practice-guide.ko.md) · [프로젝트와 실행 방법](../calculator/README.md)
- [계산기 기반 강의 구성안](calculator-lecture-map.ko.md): 코드 읽기 순서, 기존 주제 대응, 패러다임·Strategy 연결
- [리뷰 기록지](../calculator/review.md) · [강사용 해설](../calculator/instructor.md)

## 기존 슬라이드와 주문 예제

현재 슬라이드 본문은 상품 주문 예제 기준입니다. 계산기 기반 강의 구성안은 별도 문서이며 슬라이드에 아직 통합하지 않았습니다.

- [브라우저 슬라이드](../index.html): 확정 제목을 유지한 61장 한·영 강의
- [제목·서브타이틀 목록](week-03-slide-draft.ko.md): 실제 번호와 기존 구성안 번호의 대응
- [출처와 검증 기록](content-review.ko.md): 공식 자료, 코드 재구성, 검증 결과
- [기존 강의 구성안](week-03-slide-outline.ko.md): 주제별 상세 설계와 수업 시간 배정
- [기존 주문 실습 안내](practice-guide.ko.md) · [주문 프로젝트](../practice/README.md) · [주문 리뷰 기록지](../practice/review.md)
- [기존 주문 강사용 해설](../practice/instructor.md): 완성 예제와 운영 안내

## 작성 원본

- `slide-draft.json`: 사용자 확정 제목·서브타이틀. `approved-headings.sha256`으로 변경 여부 확인.
- `../scripts/lesson-body.py`: 한·영 본문, 코드, 출력, 표, 흐름도, 출처와 검증 메타데이터.
- `lesson-body.json`: 생성·포맷된 중간 데이터.
- `../scripts/build-slides.cjs`: 본문 생성 → 코드 포맷 → HTML·번역·제목 목록 생성.
- `../lecture.css`, `../code-theme.css`: 본문 배치와 2주차 기준 코드 테마.

강의 화면에는 주제별 핵심 설명과 예제만 표시하며 하단 보충 설명 영역을 사용하지 않습니다. 제작 메모와 상세한 검증 맥락은 별도 검토 문서에 기록합니다.

```sh
npm ci --prefix packages/web-deck
node lectures/03/scripts/build-slides.cjs
npm test --prefix packages/web-deck
```

루트에서 실행합니다. `build-draft.py`는 생성된 본문을 조립하는 내부 단계이므로 전체 변경 반영에는 `build-slides.cjs`를 사용합니다. 공용 `format:code`는 생성 결과를 포맷할 수 있지만, 영구 수정은 작성 원본에 반영합니다.

## 예제 검증

`npm ci --prefix lectures/03/practice`로 TypeScript 5.9.3을 설치합니다. React·Vue 예제 검증에는 별도의 검증 폴더가 필요합니다. 아래는 PowerShell 기준이며 `$env:WEEK3_CHECK_ROOT`를 지정하면 기본 임시 폴더 대신 해당 경로를 사용합니다.

```powershell
$reviewDir = Join-Path $env:TEMP 'week3-code-review'
npm install --prefix $reviewDir vue@3.5.21 react@19.1.1 @types/react@19.1.13 --ignore-scripts --no-audit --no-fund
node lectures/03/scripts/check-examples.cjs
```

예제는 표시 코드 그대로 타입 검사하며 의도된 오류만 허용합니다. 발췌 코드의 `declare` 보조 선언은 해당 슬라이드의 제공 함수·타입 계약을 나타냅니다. 원래 인수가 필요한 함수를 무조건 실행하지 않고 별도 검증 입력을 사용합니다. 터미널 안내 명령은 자동 실행하지 않습니다.

## 브라우저 검증

루트에서 `python -m http.server 4304 --bind 127.0.0.1`로 서버를 실행합니다. Chrome과 Playwright가 필요합니다. `PLAYWRIGHT_PATH`는 Playwright 패키지 경로, `DECK_URL`은 기본 `http://127.0.0.1:4304`를 대체하는 서버 주소입니다.

```sh
node lectures/03/scripts/check-slides.cjs
```

한·영 화면과 인쇄 244개 상태, 모바일 한·영 122개 페이지 이동, 코드 테마, 미처리 예외를 확인합니다. `%TEMP%/week3-slide-review`에 audit.json과 대표 캡처를 저장합니다. 서버는 검증 후 종료합니다.
