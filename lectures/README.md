# 강의 슬라이드 작성 가이드

02회차 실습 관련 슬라이드를 작성·수정할 때는 [실습 내용과 제작 기준](02/materials/practice-context.md)과 해당 실습 소스를 먼저 확인합니다. 실제 실습은 Svelte 5·SvelteKit·GitHub·Vercel이며, 아래에 기록된 현재 슬라이드 구성과 `02/examples/`의 React·정적 HTML 예제는 실습 범위의 근거가 아닙니다. 실습 맥락이 불명확한 상태에서 내용을 추정하여 슬라이드를 제작하지 않습니다.

01–13회차 페이지는 `packages/web-deck/` 공용 프레임워크를 사용합니다. 01회차는 28장, 02회차는 54장으로 작성되어 있고, 03회차는 확정된 제목·서브타이틀에 본문·코드·표·흐름을 작성한 61장 한·영 강의이며, 04–13회차는 표지 한 장의 기본 골격으로 남아 있습니다.

02회차는 구성 요소와 역할(01–07) → 웹 브라우저의 렌더링 원리(08–14) → 웹 브라우저 렌더링 방식(15) → 웹 브라우저 렌더링 성능(16) → 시맨틱 HTML과 라우팅(17–20) → 웹 브라우저 개발자 도구(21–24) → 웹 프레임워크 개발·배포·실습·Q&A(25–54)로 구성합니다. 2026-09-14 전체 수정 요청에 따라 원본 PDF에서 가져온 주제와 54장 순서를 유지하면서 기술 오류를 바로잡고 모든 슬라이드의 한국어·영어 본문과 코드를 작성했습니다. 원본 PDF·SVG는 비교 자료로 보존하며, 한국어 페이지 전체 이미지를 영문 슬라이드에 재사용하지 않습니다. 이전에 미채택한 별도 주제·과제·부록은 추가하지 않습니다.

08–14번은 웹 브라우저 렌더링 과정 → DOM → CSSOM → 렌더 트리 → 레이아웃 → 페인트의 흐름입니다. 09번에는 원본 Week 2 PDF의 렌더링 도식을 사용합니다. 17번은 챕터 03 「시맨틱 HTML과 라우팅」 표지이며, 18번은 시맨틱 HTML, 19·20번은 라우팅입니다. 원본 PDF 8·12·13페이지를 바탕으로 기술 검토 권고를 반영해 HTML 슬라이드로 수정했습니다. 정의·URL 구성·문서 탐색 흐름을 명확히 하고, 속도와 SEO에 관한 단정적인 표현을 바로잡았습니다. 21번은 챕터 04 「웹 브라우저 개발자 도구」 표지입니다. 22–24번은 원본 PDF 14페이지의 세 주제를 문서 요소와 메타데이터 → 반응형 레이아웃과 뷰포트 → 원본 HTML과 응답 헤더로 나눠 설명합니다. 현재 02회차에는 부록이 없습니다.

## 슬라이드 추가

각 `lectures/XX/index.html`의 `[data-wd-stage]` 안에 다음 형식으로 섹션을 추가합니다.

```html
<section class="wd-slide" data-wd-slide="topic-id" role="region">
  <h2 data-wd-i18n="topic_title">주제 제목</h2>
  <p data-wd-i18n="topic_body">강의 내용</p>
</section>
```

`data-wd-slide` 값은 같은 강의 안에서 중복되지 않아야 합니다. 순서, 도트, 카운터, 키보드 이동은 DOM 순서를 기준으로 자동 생성됩니다.

## 강의별 번역 추가

강의 폴더에 `slides.js`를 만들고 다음 형태로 작성합니다.

```js
window.LECTURE_CONTENT = {
  ko: {
    topic_title: '주제 제목',
    topic_body: '한국어 강의 내용'
  },
  en: {
    topic_title: 'Topic title',
    topic_body: 'English lecture content'
  }
};
```

`index.html`에서 공통 설정 파일보다 먼저 불러옵니다.

```html
<script src="slides.js"></script>
<script src="../shared/lecture-deck.js"></script>
<script src="../../packages/web-deck/web-deck.js"></script>
```

이미지와 참고 자료는 해당 강의의 `materials/`에 보관합니다. 사용자에게 보이는 새 텍스트는 KO/EN을 함께 작성합니다.

## 문장 작성 규칙

슬라이드의 모든 텍스트(제목, 리드, 학습 목표, 섹션 표지, 본문, 노트)는 강의 자료이므로 간단 명료한 형식으로 씁니다. 풀어서 말하는 문장은 강의자가 말로 전달합니다.

- 제목과 항목은 명사구로 끝냅니다. `웹 브라우저 렌더링 과정`, `파일 기반 라우팅`
- 제목은 해당 장에서 설명하는 구체적인 개념·대상·동작을 명시합니다. `코드에서 화면까지`처럼 주제를 추측해야 하는 추상적 표현은 쓰지 않습니다. 예: `HTML·CSS 파싱과 렌더링`
- 개념 설명 슬라이드의 리드·본문·캡션에는 실제 개념, 처리 과정, 인과관계, 관찰 결과를 씁니다. `같은 소개 문단을 코드·객체·화면에서 확인`, `같은 번호로 연결`처럼 제작 방법이나 검토 작업을 지시하는 문구는 슬라이드에 노출하지 않습니다. 실제 실습 절차를 안내하는 슬라이드의 작업 지시와는 구분합니다.
- 의문문·서술문 형태의 제목을 쓰지 않습니다. `~하는가`, `~인가`, `~할까`, `~하면` 같은 종결은 금지
- 경어체 종결(`~합니다`, `~세요`, `~십시오`)을 쓰지 않습니다.
- 설명이 필요하면 짧은 서술형 또는 명사형 종결을 씁니다. `각 요소의 위치와 크기 계산`, `빌드 시 HTML 생성 → CDN 제공`
- 모든 강의 슬라이드의 제목·본문·하단 노트에 다음 슬라이드나 섹션의 내용을 예고하거나 전환을 안내하는 문구를 넣지 않습니다. `다음 연결`, `이어서 살펴볼 내용`, `다음 슬라이드에서 설명`, `Connection to the Next Section`, `Up Next` 같은 안내 영역은 만들지 않습니다. 이 규칙은 기존·신규 슬라이드와 KO/EN 모두에 적용하며, 다음 내용으로의 전환 설명은 강의자가 말로 전달합니다.
- 각 슬라이드에는 해당 주제를 설명하는 코드·결과·핵심 개념만 남깁니다. 본문 반복, 말로 전달할 부연, 제작 의도, 범위 예고를 위한 하단 요약·주의문은 넣지 않습니다. 필요한 실행 조건은 관련 코드나 본문에 간결하게 표시합니다.
- 나열은 가운뎃점(` · `)으로, 흐름은 화살표(` → `)로 연결합니다.
- KO/EN 모두 같은 규칙을 따릅니다. 영어 제목은 Title Case 명사구, 본문은 짧은 구문으로 씁니다.

검증기(`npm test`)가 KO 문자열의 경어체·의문형 종결을 검사합니다. 제목의 구체성, 설명의 정확성, 제작 지시 문구의 혼입 여부는 코드·도식·실행 결과와 대조해 직접 검토합니다. 자동 검사 통과만으로 내용 검토를 완료한 것으로 보지 않습니다.

## 코드 예시 가독성 규칙

전체 강의와 새 슬라이드에 같은 규칙을 적용합니다. 파일명·용어처럼 짧은 인라인 코드는 기존 문장 안에 두고, 독립된 코드 예시는 공용 코드 블록을 사용합니다.

- 기본 개념과 세부 문법 목록은 별도 영역으로 구분합니다. 예를 들어 요소·속성 설명과 문서 선언·태그 목록은 하나의 목록에 섞지 않습니다.
- 코드 블록은 고정폭 글꼴, `0.7rem` 글자 크기(1280×720 인쇄 기준 14px), 줄 높이 `1.45`를 사용합니다. 모바일은 14px을 유지하며, 슬라이드별로 글자 크기를 줄이지 않습니다.
- 들여쓰기는 공백 2칸, 기본 줄 길이는 64자입니다. 좁은 열은 `data-wd-code-width="32"`, 넓은 단일 코드 열은 `data-wd-code-width="80"`처럼 32–80자 범위에서 지정합니다. 발표·인쇄 화면에 줄 전체가 들어오는 폭을 사용합니다. Prettier가 문법 단위로 줄을 나누며, 문자열은 강제로 자르지 않습니다.
- HTML 속성값은 큰따옴표, JavaScript 문자열은 작은따옴표를 사용합니다. CSS 선언과 JavaScript 문장은 개별 줄에 작성하고, 논리 단위 사이에 빈 줄을 둡니다.
- 긴 예시는 의미 단위로 여러 블록이나 슬라이드에 나눕니다. 글자를 줄이거나 화면 폭에 맞춰 코드 중간을 임의로 접지 않습니다. 발표·인쇄 화면에서는 전체 코드가 보여야 하며, 모바일의 긴 줄은 가로 스크롤로 읽습니다.
- 파일명 또는 코드의 역할을 블록 위에 표시합니다. 태그·속성·키워드·문자열·주석은 공용 색상으로 구분합니다.
- 02회차는 사용자 지정에 따라 `02/code-theme.css`로 검은 배경·녹색(#00ff00) Consolas 코드를 사용합니다. 실제 코드 블록과 실행 출력에만 적용하고, 파일명·경로·인라인 표기·코드 블록의 제목은 기존 설명용 스타일을 유지합니다. 구문 토큰도 녹색으로 통일하며, 이 회차에서는 위 공용 구문 색상 규칙보다 우선합니다. Consolas가 없는 환경은 대체 글꼴을 사용하고, 한글은 사용 가능한 한글 글꼴로 표시합니다. 원본 PDF의 코드 블록은 기존 검정·녹색 Consolas 표현을 유지합니다.
- 모든 `pre`는 `class="wd-code"`와 `data-wd-code`를 지정합니다. 지원 언어는 `html`, `css`, `javascript`, `jsx`, `typescript`, `tsx`, `json`, `bash`, `text`입니다. 실행 출력은 `samp`로 구분합니다. HTML의 `htmlWhitespaceSensitivity: "ignore"` 설정으로 시작·종료 태그를 읽기 쉽게 정리합니다.
- HTML 원문은 이스케이프해 저장합니다. 구문 강조용 마크업을 직접 넣지 않습니다. 공용 런타임이 번역 후 코드 내용을 보존하며 강조를 적용합니다.
- 한·영 코드 문자열과 HTML의 한국어 기본값을 함께 갱신합니다. 터미널 명령과 텍스트 그림은 내용·들여쓰기를 보존하며, 검증 중 명령을 실행하지 않습니다.

```html
<p class="week2-code-label">index.html</p>
<pre class="wd-code" data-wd-code="html">&lt;h1&gt;자기소개&lt;/h1&gt;</pre>
```

서식 기준은 `packages/web-deck/code-format.json`, 공통 표시는 `packages/web-deck/web-deck.css`에 있습니다. 구문 강조기는 로컬 파일로 제공하므로 인터넷 연결 없이도 동작합니다.

```sh
npm ci --prefix packages/web-deck
npm run format:code --prefix packages/web-deck
npm run check:code --prefix packages/web-deck
```

`format:code`는 모든 강의의 코드 예시와 한·영 번역, HTML 기본값을 함께 정리합니다. `check:code`는 공용 형식 사용, 서식, HTML 린트, JavaScript·JSON 구문과 번역 일치를 검사합니다. 구문 강조기 버전을 변경하면 `npm run vendor:code --prefix packages/web-deck`로 배포 파일과 라이선스를 다시 생성합니다.

## 학습 참고 링크

02회차 09번 이후에는 우측 하단 참고·실행 예제 링크를 추가하지 않습니다. 생성 스크립트에도 같은 기준을 적용합니다.

W3Schools처럼 슬라이드 전체의 학습을 보충하는 링크는 본문 열에 넣지 않고 슬라이드 마지막 자식인 공통 하단 영역에 둡니다. 02회차는 `week2-slide--reference`와 `week2-reference week2-reference--footer`를 사용해 우측 3rem, 하단 1rem 위치를 맞춥니다. 본문과 링크가 겹치지 않도록 하단 공간을 확보하며, 모바일에서는 본문 다음에 우측 정렬합니다. 참고 사이트를 비교하는 목록 안의 링크는 해당 목록에 유지합니다.

## 검증

```sh
cd packages/web-deck
npm test
```

상단 PDF 버튼은 브라우저 인쇄 창을 열며, 인쇄 시 슬라이드 한 장이 PDF 한 페이지가 됩니다.

## 02회차 예제와 캡처 관리

실제 과제용 SvelteKit 자료는 53번의 원본 GitHub 참고 링크를 기준으로 안내합니다. 사용자 요청에 따라 별도의 실습 소스 다운로드와 추가 실습 요구사항을 제공하지 않습니다. 검토 과정에서 만든 소스 ZIP과 내부 검토 기록은 Pages 배포 대상에서 제외합니다.

브라우저 개념을 보충하는 별도 자료는 [실행 예제](02/examples/index.html), [전체 소스](02/examples/source.html), [실행 안내](02/examples/README.md), [보조 예제 ZIP](02/materials/week2-examples.zip)에 있습니다. SSR은 예제의 Node 서버가 필요하고, 나머지 정적 예제와 React 빌드 결과는 정적 호스팅에서도 실행됩니다. React의 소스·잠금 파일과 빌드 결과를 함께 제공하며 설치 결과인 `node_modules`는 복사·배포·ZIP에서 제외합니다.

원본 PDF의 주제별 적용 근거와 개편 전후 대응은 [검토 기록](02/review-08-onward.md)에 남깁니다. `02/scripts/build-examples.cjs`와 `build-slides.cjs`는 예제와 08번 이후 슬라이드의 작성 원본입니다. 재생성 시 01–07번과 해당 번역은 보존합니다. `materials/figures/observations.json`은 실제 측정값, `code-sources.json`은 파일 발췌, `slide-map.json`은 번호 대응입니다. UI 캡처를 바꾸면 코드·도식의 값도 함께 확인합니다.

```sh
node lectures/02/scripts/build-examples.cjs
node lectures/02/scripts/format-examples.cjs
npm run build --prefix lectures/02/examples
npm run build --prefix lectures/02/examples/components
node lectures/02/scripts/build-catalog.cjs
node lectures/02/scripts/capture-examples.cjs
node lectures/02/scripts/build-slides.cjs
npm run format:code --prefix packages/web-deck
python lectures/02/scripts/package-examples.py
npm test --prefix packages/web-deck
```

캡처에는 실행 중인 예제 서버(4183)와 React 개발 서버(4175), Chrome, Playwright가 필요합니다. `PLAYWRIGHT_PATH`로 Playwright 모듈 경로를 지정할 수 있습니다. `check-examples.cjs`는 동작을, `check-slides.cjs`는 한·영 인쇄 및 모바일 배치를 검증합니다. 후자는 저장소 루트의 HTTP 서버(4186)를 사용하고 임시 폴더에 검토 이미지·PDF를 생성합니다.

25–54번은 원본 PDF 15–44페이지의 주제 순서를 따르는 한·영 HTML 슬라이드입니다. `svelte-corrections.cjs`는 기존 9개 교정 슬라이드, `complete-slides.cjs`와 `complete-examples.cjs`는 나머지 원본 이미지 슬라이드의 교정 내용과 실행 가능한 예제를 관리합니다. `build-slides.cjs`로 전체를 재생성하며 `refresh-svelte-slides.cjs`도 같은 생성기를 호출합니다. `check-complete-slides.cjs`는 양쪽 언어의 Svelte 예제, 실제 SvelteKit 이동 취소, 54장 번역과 자료 링크를 검증합니다. 현재 변경 사항과 검증 범위는 [수정 결과](02/completion-review-2026-09-14.md)를 기준으로 확인합니다.

## 03회차 코드 기반 강의

현재 실습 기준은 [TypeScript 공학용 계산기](03/calculator/README.md)입니다. 제공 HTML·CSS에 숫자 검증과 계산 함수를 구현하고, [계산기 기반 강의 구성안](03/materials/calculator-lecture-map.ko.md)에 따라 코드의 실행 흐름·순수 함수·캡슐화·Strategy를 연결합니다. 아래 61장 슬라이드 본문은 기존 상품 주문 예제 기준이며 계산기 예제의 슬라이드 통합은 별도 단계입니다.

3주차는 확정된 제목·서브타이틀을 유지한 61장(표지 1 + 챕터 8 + 주제 52)입니다. 제목 원본은 `03/materials/slide-draft.json`, 본문 작성 원본은 `03/scripts/lesson-body.py`입니다. 본문은 공식 문서의 개념·예제를 상품 주문 맥락으로 재구성했으며 [출처와 검증 기록](03/materials/content-review.ko.md)에 적용 범위와 검증 결과를 기록합니다.

코드는 2주차와 같은 검정 배경·녹색 Consolas이며 1280×720 인쇄에서 14px을 유지합니다. 역사·구조·실습 안내는 필요에 따라 표와 흐름도로 구성합니다. TypeScript·TSX는 공용 포매터와 로컬 Prism의 지원 언어에 포함됩니다.

```sh
node lectures/03/scripts/build-slides.cjs
npm test --prefix packages/web-deck
node lectures/03/scripts/check-examples.cjs
node lectures/03/scripts/check-slides.cjs
```

검증 도구의 의존성과 실행 환경은 `03/materials/README.md`를 참고합니다.
