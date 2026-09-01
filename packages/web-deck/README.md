# @pwd/web-deck

## Typography

The package self-hosts the variable Noto Sans KR font for consistent Korean and English rendering in browsers and PDF output. The font is distributed under the SIL Open Font License 1.1; see `fonts/OFL-1.1.txt`.

Reusable content styles are available for `.wd-slide--content`, `.wd-slide-heading`, `.wd-slide-lead`, `.wd-content`, `.wd-columns`, `.wd-code`, `.wd-table`, and `.wd-caption`. A deck with one enabled slide automatically hides the progress rail and bottom navigation.

빌드 도구 없이 정적 HTML에서 사용하는 KO/EN 슬라이드 프레임워크입니다.

## 제공 기능

- 한국어/영어 전환 및 언어 설정 저장
- 이전/다음, 도트, 키보드, 모바일 스와이프
- `#/2` 형식의 슬라이드 딥링크
- 전체화면과 발표 중 컨트롤 자동 숨김
- 접근성 라벨, 비활성 슬라이드 `inert`, 전환 안내
- 1280×720 인쇄 레이아웃 및 PDF 저장용 인쇄 버튼
- 본편과 부록의 별도 번호 처리

## 기본 사용법

```html
<link rel="stylesheet" href="/packages/web-deck/web-deck.css">

<main class="wd-deck" data-web-deck>
  <div class="wd-viewport" data-wd-viewport>
    <div class="wd-stage" data-wd-stage>
      <section class="wd-slide is-active" data-wd-slide="cover" role="region">
        <h1 data-wd-i18n="title">강의 제목</h1>
      </section>
    </div>
  </div>
</main>

<script>
window.WEB_DECK_CONFIG = {
  brand: '실전 웹 서비스 개발 · 2026년 2학기',
  brandKey: 'course_title',
  homeHref: '../../',
  messages: {
    ko: { course_title: '실전 웹 서비스 개발 · 2026년 2학기', title: '강의 제목' },
    en: { course_title: 'Practical Web Service Development · Fall 2026', title: 'Lecture title' }
  }
};
</script>
<script src="/packages/web-deck/web-deck.js"></script>
```

`template/index.html`을 복사하면 한 장짜리 새 덱에서 바로 시작할 수 있습니다.

## 번역 속성

- `data-wd-i18n="key"`: 텍스트
- `data-wd-i18n-alt="key"`: 이미지 대체 텍스트
- `data-wd-i18n-aria-label="key"`: 접근성 라벨
- `data-wd-i18n-title="key"`: title 속성

번역 문자열은 `textContent`로 적용하므로 HTML을 삽입하지 않습니다.

## 조작

- 다음: `→`, `PageDown`, `Space`
- 이전: `←`, `PageUp`
- 처음/끝: `Home`, `End`
- 전체화면: `F`
- 모바일: 60px 이상의 수평 스와이프

PDF 버튼은 브라우저 인쇄 창을 엽니다. 배포용 PDF 자동 생성기는 추후 별도 빌드 도구로 추가할 수 있습니다.
