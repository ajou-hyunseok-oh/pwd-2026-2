# 05회차 자료 — React Framework의 이해

[강의 슬라이드](../index.html)는 확정한 7개 챕터·32개 주제에 표지와 챕터 표지 7장을 더한 **40장 한·영 HTML 강의**입니다. 각 주제에 개념 설명, 짧은 코드, 관찰 결과를 연결했습니다. 상품 목록·검색·수량·입고를 공통 사례로 사용합니다.

| 화면 번호 | 챕터 | 주제 번호 |
| --- | --- | --- |
| 1 | 강의 표지 | — |
| 2–4 | 01. React 애플리케이션의 이해 | 01–02 |
| 5–10 | 02. JSX와 컴포넌트 기반 화면 구성 | 03–07 |
| 11–17 | 03. 사용자 행동과 상태 기반 화면 갱신 | 08–13 |
| 18–23 | 04. Hooks와 외부 시스템 동기화 | 14–18 |
| 24–29 | 05. 라우팅과 애플리케이션 데이터 흐름 | 19–23 |
| 30–34 | 06. 렌더링 전략과 서버·클라이언트 경계 | 24–27 |
| 35–40 | 07. 비동기 작업과 폼 제출 | 28–32 |

각 범위의 첫 장은 챕터 표지입니다. [slide-map.json](slide-map.json)에 현재 화면 번호, 주제 번호, ID, 챕터, 타이틀, 서브타이틀, 출처를 기록합니다. 스킬의 기본 입력 번호는 **표지와 챕터 표지를 포함한 화면 번호**입니다.

## 기준 자료와 실행 환경

- Lecture 04의 상품 UI 설계·컴포넌트·선언형 UI를 요약하여 시작합니다.
- `[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf`의 JSX·Props·State·이벤트·Hooks 코드를 개념별로 재구성합니다. 코드 표시는 원본의 검정 배경, 녹색 Consolas 디자인을 사용합니다.
- 현대 React 개념과 API는 [React 공식 학습 자료](https://react.dev/learn)와 API 문서를 사용합니다.
- 페이지·레이아웃·데이터 처리·서버 경계는 [Next.js App Router 공식 문서](https://nextjs.org/docs/app) 기준입니다. React Router의 route action은 개념 비교로만 언급합니다.
- 현재 범위는 Chapter 07까지입니다. 과거 덱의 Netlify 배포·Forms 실습은 이번 강의에서 제외했습니다.

코드 32개는 강의용 예제입니다. 표지와 챕터 표지에는 코드를 넣지 않습니다. 기본 React 컴포넌트는 React 프로젝트에서 사용할 수 있으며, 부모가 전달해야 하는 Props를 라벨에 명시합니다. Next.js 파일은 별도의 App Router 프로젝트와 루트 layout이 필요합니다. `@/lib/products`, `@/lib/auth`, `saveStock`은 설명용 의존성으로, 실제 DB 저장·권한 검사를 별도로 구현해야 합니다. 슬라이드는 운영 서버나 DB 구현을 포함하지 않습니다.

주제 30의 폼은 500ms 지연과 입력 검사를 수행하며 저장하지 않습니다. 주제 31의 Server Function을 연결할 때 결과 객체·초기 상태·결과 표시를 함께 맞춰야 합니다. 주제 32는 `saveStock`이 확정된 boolean을 반환하거나 실패 시 reject하는 계약입니다. 브라우저 검증에서는 지연 성공·실패를 주입하여 표시와 복구를 확인합니다.

## 수정 및 검증

작성 원본은 `../scripts/lesson.py`, 생성기는 `../scripts/build-slides.py`, 레이아웃은 `../lecture.css`입니다. 생성 파일은 HTML, 번역 JS, 슬라이드 맵입니다.

```sh
python3 lectures/05/scripts/build-slides.py
node packages/web-deck/scripts/code-examples.cjs --write --lecture 05
npm test --prefix packages/web-deck
```

Chrome과 Playwright가 있는 환경에서 정적 서버와 배치 검사를 실행합니다.

```sh
python3 -m http.server 4305 --bind 127.0.0.1
# 별도 터미널
node lectures/05/scripts/check-slides.cjs
node lectures/05/scripts/check-examples.cjs
```

`PLAYWRIGHT_PATH`로 Playwright 패키지 경로를 지정할 수 있습니다. 코드 실행 검사는 기본적으로 Lecture 04의 `scripts/node_modules`에 있는 React·React DOM·Vite를 사용하며, `REACT_MODULES`로 다른 설치 경로를 지정합니다. 슬라이드 코드 원문을 임시 React 앱에 추출하므로 복사본을 따로 유지하지 않습니다.

배치 검사는 한·영 발표·인쇄·모바일을 확인합니다. 출력은 시스템 임시 폴더의 `pwd-week5-deck/review`이며 `DECK_URL`, `REVIEW_OUTPUT`으로 변경할 수 있습니다. 실행 검사는 상태 스냅샷, DOM 보존, key 초기화, Ref, Effect 정리, 독립 Hook, 비동기 상태, Action과 낙관적 UI를 확인합니다. 서버·DB·Next.js 통합 실행은 이 검사의 범위에 포함하지 않습니다.

`images/`와 `capture-practice.cjs`는 과거 실습 자료로 보존하며 현재 덱에서 사용하지 않습니다. [검토 기록](content-review.ko.txt)에 실제 검증 결과를 기록합니다.
