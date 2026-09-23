# 05회차 자료 — React 심화 · 캠퍼스 푸드맵

[강의 슬라이드](../index.html)는 한국어·영어 전환을 지원하는 64장 HTML 덱입니다. 기존 웹 슬라이드의 탐색·전체 화면·PDF 인쇄 기능을 사용합니다.

## 구성

| 슬라이드 | 내용 |
| --- | --- |
| 1–5 | 4주차 복습: React, UI 선언, 렌더링, 데이터와 상태 설계 |
| 6–11 | 실습 완성 화면, 데이터 구조, 실행 환경, 파일과 진입점 |
| 12–19 | 컴포넌트, JSX, Props, 조합, 목록과 key, 카드 실습 |
| 20–27 | State, 스냅샷, 이벤트, 카테고리 필터, 좋아요 실습 |
| 28–35 | Hooks, Effect, 정리 함수, localStorage, 새로고침 후 복원 |
| 36–44 | 라이브러리 역할, Provider, 서비스, Query, HashRouter, 상세 조회 |
| 45–54 | 폼 등록·검증·정규화·저장, Mutation, 제보 승인, UI 피드백 |
| 55–64 | 정적 호스팅, Vercel 배포, 라우팅, 오류 해결, 완료 기준 |

각 실습에는 실행할 작업, 예상 결과, 확인할 파일이나 저장 키를 함께 제시했습니다. 코드 블록은 실제 파일의 발췌와 개념 예제를 구분합니다. 전체 코드는 실습 저장소를 사용합니다.

## 기준 자료

- 원본: 이 폴더의 `[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf` (26쪽)
- 복습: [4주차 슬라이드](../../04/index.html)
- 실습: `/Users/nnnceo/WorkspaceAjou/pwd-week5`, 커밋 `9d12cebf32d6e333e8cd69faa4a7c9c721e4be00`
- 슬라이드별 출처: [slide-map.json](slide-map.json), 슬라이드 하단 링크 및 숨겨진 출처 메모
- 화면 이미지: `images/list.png`, `images/detail.png`, `images/submit.png` — 실제 실습 앱을 격리된 브라우저에서 촬영

원본의 React 개념을 유지하면서 실행 절차는 현재 실습 코드에 맞췄습니다. 특히 원본의 Netlify·Netlify Forms 대신 Vercel 정적 배포와 localStorage 서비스를 설명하고, `App.jsx`의 실제 라우터인 HashRouter를 기준으로 URL을 표기했습니다. 인기 목록은 평점순이며, 제보 데이터는 브라우저별로 저장됩니다. 제보 승인 시 맛집 생성과 원래 제보의 상태 갱신을 구분합니다.

## 수정 및 재생성

내용은 `../scripts/lesson.py`, 레이아웃은 `../lecture.css`에서 수정합니다. 저장소 루트에서 실행합니다.

```sh
python3 lectures/05/scripts/build-slides.py
node packages/web-deck/scripts/code-examples.cjs --write --lecture 05
npm test --prefix packages/web-deck
```

생성 파일은 `../index.html`, `../lecture-content.js`, `slide-map.json`입니다. 생성된 HTML을 직접 수정하면 다음 빌드에서 덮어씁니다.

## 브라우저 검증 및 화면 갱신

Chrome과 Playwright가 있는 환경에서 저장소 루트에 정적 서버를 실행합니다.

```sh
python3 -m http.server 4305 --bind 127.0.0.1
```

별도 터미널에서 전체 슬라이드를 검사합니다. Playwright가 일반 모듈 경로에 없다면 `PLAYWRIGHT_PATH`에 설치된 패키지의 절대 경로를 지정합니다.

```sh
node lectures/05/scripts/check-slides.cjs
```

검사 결과와 한·영 슬라이드 PNG, 인쇄 확인용 PDF는 시스템 임시 폴더의 `pwd-week5-deck/review`에 생성됩니다. `DECK_URL`, `REVIEW_OUTPUT` 환경 변수로 서버 주소와 출력 폴더를 변경할 수 있습니다.

실습 화면을 갱신하려면 실습 저장소에서 `npm run dev -- --host 127.0.0.1 --port 5175`를 실행하고, 강의 저장소에서 다음 명령을 실행합니다.

```sh
node lectures/05/scripts/capture-practice.cjs
```

이 스크립트는 화면 3개를 저장하고 카테고리 필터, 빈 목록, 없는 상세 ID, 필수 입력 검증, 제보 저장, 메뉴 배열 변환, 새로고침 후 보존을 확인합니다. `PRACTICE_URL`로 실습 서버 주소를 변경할 수 있습니다.

검증 내역은 [content-review.ko.txt](content-review.ko.txt)에 기록했습니다.
