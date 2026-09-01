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

## 검증

```sh
cd packages/web-deck
npm test
```

상단 PDF 버튼은 브라우저 인쇄 창을 열며, 인쇄 시 슬라이드 한 장이 PDF 한 페이지가 됩니다.
