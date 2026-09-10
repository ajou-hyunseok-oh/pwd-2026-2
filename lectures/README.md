# 강의 슬라이드 작성 가이드

01–13회차 페이지는 `packages/web-deck/` 공용 프레임워크를 사용합니다. 01회차는 작년도 PDF를 기반으로 한 28장 강의안이 작성되어 있고, 02–13회차는 표지 한 장의 기본 골격으로 남아 있습니다.

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
- 의문문·서술문 형태의 제목을 쓰지 않습니다. `~하는가`, `~인가`, `~할까`, `~하면` 같은 종결은 금지
- 경어체 종결(`~합니다`, `~세요`, `~십시오`)을 쓰지 않습니다.
- 설명이 필요하면 짧은 서술형 또는 명사형 종결을 씁니다. `각 요소의 위치와 크기 계산`, `빌드 시 HTML 생성 → CDN 제공`
- 나열은 가운뎃점(` · `)으로, 흐름은 화살표(` → `)로 연결합니다.
- KO/EN 모두 같은 규칙을 따릅니다. 영어 제목은 Title Case 명사구, 본문은 짧은 구문으로 씁니다.

검증기(`npm test`)가 KO 문자열의 경어체·의문형 종결을 검사합니다.

## 검증

```sh
cd packages/web-deck
npm test
```

상단 PDF 버튼은 브라우저 인쇄 창을 열며, 인쇄 시 슬라이드 한 장이 PDF 한 페이지가 됩니다.
