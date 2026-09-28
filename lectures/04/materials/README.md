# 04회차 자료

## 04주차 실제 강의 페이지

[1교시 React 기초](../index.html)는 24장, [2교시 웹 서비스 설계 기초](../ai-design.html)는 19장의 독립 한·영 HTML 슬라이드입니다. 기존 공용 프레임워크의 언어 전환·키보드 이동·PDF 인쇄를 사용합니다. 일반 슬라이드는 제목과 서브타이틀로 시작하며, 표지 하단에는 `LECTURE 04`를 표시합니다.

## 1교시: 설명 위계 정리

2026-09-24: 전체 24장을 대상으로 `slide-explanation-cleanup`을 적용했습니다. 한·영 개념 설명과 코드 캡션은 굵은 `개념 - 짧은 정의`와 들여쓴 부연 설명으로 구분하고, 나열·순서 기호와 줄바꿈·간격을 정리했습니다. 비교표와 갱신 단계 도식, 기존 학습 순서, 실행 코드는 유지합니다.

작성 원본은 `../scripts/react-body.py`와 `../scripts/react-demos.jsx`, 설명 요소의 HTML 생성은 `../scripts/slide_body.py`, 1교시 전용 스타일은 `../react-cleanup.css`입니다. 시연 파일을 빌드한 뒤 `python3 lectures/04/scripts/build-outline.py --period 1`로 재생성합니다.

한·영 각 24장의 렌더링과 PDF 페이지 수를 확인했습니다. 화면·인쇄·모바일의 넘침·출처 겹침 검사, 공통 덱·코드 예제 검사와 상품 검색 시연 검사를 수행했습니다.

## 2교시: 웹 서비스 설계 기초

2026-09-28: 30장을 19장으로 줄이고 챕터마다 한 가지 역할을 맡도록 재구성했습니다. 원본 `[PWD Week9] 웹 서비스 설계 기초.pdf`의 핵심 개념과 NNN UGC Creator Hub 가상 사례를 사용합니다. 같은 문제·기능·흐름을 개념, 작성법, 사례, 결론에서 반복하던 부분을 덜어냈습니다.

| 챕터 | 범위 | 다룰 내용 |
| --- | --- | --- |
| 01 설계의 공통언어 | 02–04 | 기획·UX·UI의 관계와 UX 산출물의 역할 |
| 02 기획시 결정 사항 | 05–09 | 사용자 문제, 서비스 가치, 기능 우선순위, 기술의 역할 |
| 03 기획 사례 | 10–15 | UGC 서비스의 사용자 맥락에서 문제·가치·기능·흐름·화면까지 도출 |
| 04 프로젝트 기획 발표 | 16–19 | 상세 내용 선별, 완성 예시, 발표와 결과물 |

일반 개념은 1·2장에서 짧게 설명하고 3장에서 한 번만 사례에 적용합니다. 사용자 여정 단계 표, 기획서 목차 표, 별도 일정·KPI 분류, 사례 화면·시나리오 재진술, 원페이저 항목표, 학습 목표 재진술 슬라이드를 삭제했습니다. 흐름도와 와이어프레임은 사례의 기능 도출 다음으로 옮겼습니다. `build-design.py`, `design_blocks.py`, `design.css`가 작성 원본이며 한·영 슬라이드를 함께 재생성합니다.

- [2교시 강의 본문](week-04-service-planning.ko.txt): 19장 순서의 한국어 본문·메모·PDF 페이지 대응.
- `design-slides.json`, `design-sources.json`, `design-chapters.json`: 본문·출처·챕터 데이터.
- `period-2-outline.json`, `../period-2-content.js`: 실제 슬라이드 순서·한영 번역.

기획 결과물은 원페이저 PDF와 5분 이내 발표 영상입니다. 2026년 10월 11일 23:59까지 아주BB에 원페이저 PDF와 유튜브 영상 링크를 제출하고, 디스코드에도 영상 링크를 업데이트합니다. `week-04-ai-design.ko.txt`는 이전 AI 협업 중심 구성의 기록이며 현재 슬라이드 생성에 사용하지 않습니다.

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

2026-09-23에는 이전 30장 구성의 화면·인쇄·모바일 검사를 통과했습니다. 2026-09-28 재구성에서는 공통 덱 검사와 Chrome PDF 19쪽을 확인했습니다.

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

원본 「React 프레임워크를 이용한 웹 프론트엔드 개발」 4–8쪽을 검토하여 내용을 보강하고, 서비스 탐색 장과 React UI 설계 철학 설명 장을 추가했습니다. 현재 표지·챕터 5장, 본문 19장입니다. 상세 대응과 수정 근거는 [원본 PDF 보강 기록](react-pdf-enrichment.ko.txt)에 정리했습니다.

- 04번: HTML/CSS·jQuery·React로 확장된 UI 개발 방식과 데이터/DOM 관리 부담.
- 14번: 명령형·선언형의 정의와 같은 카운터의 jQuery·React 코드를 한 장에서 비교. PDF에서 실행 화면 없이도 차이를 읽을 수 있도록 구성.
- 17–20번: Virtual DOM의 개념 → DOM 직접 갱신과 React의 차이 → Trigger·Render·Commit → 효과와 한계.

14번의 코드 비교는 실제 jQuery API와 React 코드를 사용합니다. 원본 PDF의 숫자 변환 오류와 일반 DOM 코드를 jQuery로 잘못 표시한 부분은 수정했습니다. 17–20번은 두 방식 모두 실제 DOM에 반영한다는 점과 Virtual DOM의 계산 비용을 함께 설명합니다. 원본의 로고·정답/오답·속도 우열 아이콘은 강의 설명에 추가하지 않았습니다. 2교시는 변경하지 않았습니다.

## 서비스 탐색 슬라이드

08번 「React를 사용하는 서비스」: Instagram·Facebook·Netflix·Spotify·Airbnb·Microsoft Teams의 공식 아이콘을 3×2 그리드로 표시합니다. 아이콘과 이름을 포함한 각 영역을 누르면 해당 서비스가 새 탭으로 열립니다. 모바일에서는 2열로 표시합니다.

- 링크·이름·아이콘·React 활용 근거 원본: `react-services.json`
- 로컬 아이콘: `../assets/services/`
- 공식 사이트에서 제공한 원본 이미지와 수집 기록: `images/source-notes.txt`
