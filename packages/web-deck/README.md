# @pwd/web-deck

## Typography

The package self-hosts the variable Noto Sans KR font for consistent Korean and English rendering in browsers and PDF output. The font is distributed under the SIL Open Font License 1.1; see `fonts/OFL-1.1.txt`.

Reusable content styles are available for `.wd-slide--content`, `.wd-slide-heading`, `.wd-slide-lead`, `.wd-content`, `.wd-columns`, `.wd-code`, `.wd-table`, and `.wd-caption`. A deck with one enabled slide automatically hides the progress rail and bottom navigation.

05 이후 본문 강의는 [작성 하네스](../../lectures/authoring/README.md)의 `authoring.css`와 `.wd-lesson-*` 블록을 재사용합니다. `data-wd-authoring="v1"`으로 적용을 표시하며 `npm test`가 문체·정의 위계·HTML 기본값·불필요한 반복 영역을 함께 확인합니다.

현재 05회차는 React 기초·컴포넌트·JSX·상태·Hooks, 부록과 실습 안내로 구성한 65장 덱이며 공용 코드 블록은 41개입니다. [05회차 자료 안내](../../lectures/05/materials/README.md)에 원본 가져오기 예외와 생성·검증 명령을 기록합니다. 실제 발표·인쇄·모바일 배치와 React 예제 동작은 별도 브라우저 검사로 확인합니다.

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
<script src="/packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="/packages/web-deck/web-deck.js"></script>
```

`template/index.html`을 복사하면 한 장짜리 새 덱에서 바로 시작할 수 있습니다.

## 번역 속성

- `data-wd-i18n="key"`: 텍스트
- `data-wd-i18n-alt="key"`: 이미지 대체 텍스트
- `data-wd-i18n-aria-label="key"`: 접근성 라벨
- `data-wd-i18n-title="key"`: title 속성

번역 문자열은 `textContent`로 적용하므로 HTML을 삽입하지 않습니다. `pre[data-wd-code]`는 번역 후 로컬 Prism으로 구문 강조를 다시 적용하며, 복사되는 코드 원문은 유지합니다.

## 코드 예시

공용 `wd-code`와 언어 지정 속성을 사용합니다. 상세한 [코드 예시 가독성 규칙](../../lectures/README.md#코드-예시-가독성-규칙)은 전체 강의에 적용합니다.

구문 강조기를 공용 런타임보다 먼저 불러옵니다. 기본 템플릿과 모든 강의에는 이미 포함되어 있습니다.

```html
<script src="/packages/web-deck/vendor/prism/prism.js" data-manual></script>
<script src="/packages/web-deck/web-deck.js"></script>
```

`npm run format:code`로 코드 예시를 정리하고 `npm test`로 서식·문법·번역을 검증합니다. 개발 도구는 `npm ci`로 설치하며, 슬라이드 실행에는 설치나 빌드가 필요하지 않습니다.

## 조작

- 다음: `→`, `PageDown`, `Space`
- 이전: `←`, `PageUp`
- 처음/끝: `Home`, `End`
- 전체화면: `F`
- 모바일: 60px 이상의 수평 스와이프

PDF 버튼은 브라우저 인쇄 창을 엽니다. 배포용 PDF 자동 생성기는 추후 별도 빌드 도구로 추가할 수 있습니다.

## 문장 어투

한국어 강의 콘텐츠는 간결한 명사형 또는 서술형 종결을 사용합니다. `~니다`, `~세요`, `~십시오`와 같은 존댓말 종결은 사용하지 않습니다. 공용 인터페이스 안내 문구를 제외한 `lecture-content.js`의 한국어 콘텐츠는 `npm test`에서 이 규칙을 자동으로 검사합니다.
