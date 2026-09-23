# 04회차 자료

## 04주차 실제 강의 페이지

[1교시 React 기초](../index.html)는 24장, [2교시 웹 서비스 설계 기초](../ai-design.html)는 30장의 독립 한·영 HTML 슬라이드입니다. 기존 공용 프레임워크의 언어 전환·키보드 이동·PDF 인쇄를 사용합니다. 일반 슬라이드는 제목과 서브타이틀로 시작하며, 표지 하단에는 `LECTURE 04`를 표시합니다.

## 1교시: 설명 위계 정리

2026-09-24: 전체 24장을 대상으로 `slide-explanation-cleanup`을 적용했습니다. 한·영 개념 설명과 코드 캡션은 굵은 `개념 - 짧은 정의`와 들여쓴 부연 설명으로 구분하고, 나열·순서 기호와 줄바꿈·간격을 정리했습니다. 비교표와 갱신 단계 도식, 기존 학습 순서, 실행 코드는 유지합니다.

작성 원본은 `../scripts/react-body.py`와 `../scripts/react-demos.jsx`, 설명 요소의 HTML 생성은 `../scripts/slide_body.py`, 1교시 전용 스타일은 `../react-cleanup.css`입니다. 시연 파일을 빌드한 뒤 `python3 lectures/04/scripts/build-outline.py --period 1`로 재생성합니다.

한·영 각 24장의 렌더링과 PDF 페이지 수를 확인했습니다. 화면·인쇄·모바일의 넘침·출처 겹침 검사, 공통 덱·코드 예제 검사, 검색·카운터·시계와 입력 유지 시연 검사를 통과했습니다.

## 2교시: 웹 서비스 설계 기초

원본 `[PWD Week9] 웹 서비스 설계 기초.pdf`의 개념·기획서 구성·NNN UGC Creator Hub 가상 사례를 유지하고, 동의한 네 가지 교육적 보완을 적용했습니다. 가상 기획안의 수익 정책·통계·사업성·기능 우선순위를 비평하는 수업으로 변경하지 않았습니다.

- 수행 중심 학습 목표와 마지막 기획안 작성 기준의 연결.
- 사용자·문제·가치에 비중을 두고 API·DB 등은 역할 소개 수준으로 설명.
- 문제 → 가치, 목표 → 기능, 행동 → 화면의 작성 과정 시연.
- 상세 기획 → 원페이저 요약 과정과 같은 UGC 사례의 완성 원페이저.

전체 30장을 대상으로 `slide-explanation-cleanup` 규칙을 적용했습니다. 개념 설명은 굵은 `개념 - 짧은 정의`와 들여쓴 부연 설명으로 구분하고, 나열·순서 기호와 의미 단위의 줄바꿈을 정리했습니다. 비교표·흐름도·와이어프레임·완성 원페이저의 형식과 기존 학습 순서는 유지합니다. 한·영 본문을 함께 수정했으며 `build-design.py`, `design_blocks.py`, `design.css`에서 재생성할 수 있습니다.

| 슬라이드 | 내용 |
| --- | --- |
| 01–02 | 표지·수행 중심 학습 목표 |
| 03–07 | 웹서비스 설계 핵심 개념 |
| 08–18 | 기획서 작성법·UX·기능·기술·일정·KPI |
| 19–24 | UGC Creator Hub 기획 사례와 작성 과정 |
| 25–30 | 원페이저 구성·압축·완성 예시·작성 기준·발표 |

현재 작성 원본과 생성 결과:

- `../scripts/build-design.py`: 2교시의 한·영 본문·강의 메모·원본 PDF 대응.
- `../scripts/design_blocks.py`: 개념·정의·부연 설명, 역할별 시나리오, 와이어프레임, 작성 과정, 원페이저의 HTML 표현.
- `../design.css`: 2교시 전용 스타일.
- [2교시 강의 본문](week-04-service-planning.ko.txt): 30장 순서의 한국어 본문·메모·PDF 페이지 대응.
- `design-slides.json`, `design-sources.json`, `design-chapters.json`: 본문·출처·챕터 데이터.
- `period-2-outline.json`, `../period-2-content.js`: 실제 슬라이드 순서·한영 번역.

기획 결과물은 기존 안내의 원페이저 1페이지와 5분 이내 발표 영상입니다. 새 제출물·배점·마감일은 추가하지 않았으며, 원본의 2025 일정은 올해 제출 일정으로 사용하지 않았습니다. `week-04-ai-design.ko.txt`는 이전 AI 협업 중심 구성의 기록이며 현재 슬라이드 생성에 사용하지 않습니다.

## 생성과 확인

2교시만 재생성:

```sh
python3 lectures/04/scripts/build-outline.py --period 2
```

두 교시의 전체 재생성과 공통 검사:

```sh
python3 lectures/04/scripts/build-outline.py
npm test --prefix packages/web-deck
```

화면·인쇄·모바일 검사에는 저장소 루트의 HTTP 서버와 Playwright·Chrome이 필요합니다.

```sh
PERIOD=2 PLAYWRIGHT_PATH=/absolute/path/to/playwright node lectures/04/scripts/check-outline.cjs
```

`PERIOD=2`를 생략하면 1교시를 검사합니다. 기본 서버는 `http://127.0.0.1:4304`이며 `DECK_URL`로 변경할 수 있습니다. 검토 이미지는 임시 폴더에 생성하며 `REVIEW_OUTPUT`으로 위치를 지정할 수 있습니다.

2026-09-23 확인: 한·영 각 30장의 화면·인쇄 영역, 모바일 가로 넘침과 본문·출처 겹침 검사 통과. 모든 슬라이드의 렌더링을 직접 검토하고 한·영 PDF 각 30쪽을 확인했습니다. 공통 덱·코드 예제 검사도 통과했습니다.

1교시의 구성·코드 시연·자료는 이번 2교시 재제작에서 수정하지 않았습니다. [1교시 구성 검토 기록](react-structure-review.ko.txt)과 [원본 PDF 보강 기록](react-pdf-enrichment.ko.txt)을 참고합니다.

## React 시연의 소스와 재생성

상품 검색은 React 공식 Thinking in React의 6개 상품 예시를 수업용으로 재구성했습니다. 같은 화면으로 컴포넌트·재사용·검색 조건·선언형 UI를 연결합니다. 시계는 Render and Commit의 입력 유지 관찰을 실제 React로 구현했습니다. 세부 API 설명과 학생 실습은 추가하지 않았습니다.

- 본문: `../scripts/react-body.py`
- 시연: `../scripts/react-demos.jsx`
- 표시 코드와 실제 실행을 공유하는 비교 예제: `../scripts/comparison-examples.jsx`
- 브라우저용 파일: `../assets/react-demos.js` · 로컬에 React·jQuery 포함, CDN 연결 불필요
- 이미지 출처·실행 캡처 기록: `images/source-notes.txt`
- 의존성 변경 없이 재빌드: 아래 명령 사용

```sh
npm ci --prefix lectures/04/scripts
npm run build:demos --prefix lectures/04/scripts
python3 lectures/04/scripts/build-outline.py
PLAYWRIGHT_PATH=/absolute/path/to/playwright node lectures/04/scripts/check-react-demos.cjs
```

본문·제목만 수정할 때는 `build-outline.py`만 실행합니다. 시연의 React 코드를 수정할 때는 `build:demos`도 실행합니다. `check-react-demos.cjs`는 검색·빈 결과·개수 계산·언어 전환·DOM 재사용·시계 갱신 중 입력/포커스/커서 유지를 확인합니다.

## 원본 PDF의 등장 배경·VDOM 내용 보강

원본 「React 프레임워크를 이용한 웹 프론트엔드 개발」 4–8쪽을 검토하여 23장으로 보강한 뒤, 실습 전 서비스 탐색 장을 추가했습니다. 현재 표지·챕터 5장, 본문 19장입니다. 상세 대응과 수정 근거는 [원본 PDF 보강 기록](react-pdf-enrichment.ko.txt)에 정리했습니다.

- 04번: HTML/CSS·jQuery·React로 확장된 UI 개발 방식과 데이터/DOM 관리 부담.
- 12번: 명령형·선언형의 정의와 UI 개발에서의 책임 비교.
- 13번: 앞서 정의한 개념을 같은 카운터의 jQuery·React 코드와 실제 동작으로 확인. 표시 코드를 실행 모듈에서 추출하여 일치 유지.
- 16–17번: 메모리의 UI 트리, 이전/새 UI의 차이, Trigger·Render·Commit·브라우저 표시.
- 19번: 실제 DOM 관찰과 갱신 책임 비교. 항상 빠름/느림이라는 단정 제거.

13번과 19번의 버튼을 클릭하면 두 구현의 동작을 볼 수 있으며, 19번은 DOM 관찰 결과도 표시합니다. jQuery 4.0.0은 로컬 번들에 포함됩니다. 원본 PDF의 숫자 변환 오류와 일반 DOM 코드를 jQuery로 잘못 표시한 부분은 수정했습니다. 원본의 로고·정답/오답·속도 우열 아이콘은 강의 설명에 추가하지 않았습니다. 2교시는 변경하지 않았습니다.

## 마지막 서비스 탐색 슬라이드

20번 「React를 사용하는 서비스」: Instagram·Facebook·Netflix·Spotify·Airbnb·Microsoft Teams의 공식 아이콘을 3×2 그리드로 표시합니다. 아이콘과 이름을 포함한 각 영역을 누르면 해당 서비스가 새 탭으로 열립니다. 모바일에서는 2열로 표시합니다.

- 링크·이름·아이콘·React 활용 근거 원본: `react-services.json`
- 로컬 아이콘: `../assets/services/`
- 공식 사이트에서 제공한 원본 이미지와 수집 기록: `images/source-notes.txt`
