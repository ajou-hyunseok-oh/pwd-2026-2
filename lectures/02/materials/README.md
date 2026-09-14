# 02회차 자료

실습 안내 52·53번은 사용자 요청에 따라 원본 제목·학습 목표·요구사항·참고 링크·제출 안내를 유지합니다. 마감은 9월 20일 23:59이며 영어는 원문을 충실히 번역합니다. 소스 검토를 근거로 실습 요구사항이나 다운로드·설치 안내를 임의로 추가하지 않습니다. 53번의 원본 요구사항은 질문형 문체도 보존합니다.

2026-09-14 전체 수정 요청을 반영한 54장 한·영 슬라이드가 현재 기준입니다. 원본 PDF의 주제와 순서를 유지하며 잘못된 설명·수치·코드를 교정했습니다. 이전에 한국어 SVG 전체 페이지를 사용하던 23장도 번역 가능한 HTML로 작성했습니다. 원본 PDF·SVG·추출 JSON은 대조와 이력 보존용이며 현재 슬라이드 본문으로 사용하지 않습니다.

## 실습 기준과 배포 자료

실제 과제는 Svelte 5·SvelteKit 미니 포트폴리오 제작 및 GitHub·Vercel 배포입니다. Home, About, Projects, 동적 상세 페이지, 메모를 포함하며 서버 load와 API를 사용합니다. 정적 HTML 사이트나 React 과제가 아닙니다.

| 자료 | 용도 |
| --- | --- |
| [실습 내용과 제작 기준](practice-context.md) | 현재 소스 기준 및 기존 기능·화면 검토 기록 |
| [원본 실습 저장소](https://github.com/ajou-hyunseok-oh/pwd-week2) | 53번 원본 참고 링크 |
| [이전 검토용 패키지 기록](final-review/practice-package.json) | 로컬 검토 당시의 커밋·해시 기록; 학생용 다운로드로 배포하지 않음 |
| [수정 결과](../completion-review-2026-09-14.md) | 전체 수정 사항, 검증 결과와 확인 범위 |
| [최초 최종 검토](../final-review-2026-09-14.md) | 수정 전 발견 사항과 공식 근거 |
| `practice-review/` | 2026-09-11 실습 실행 관찰·출처·검증 기록 |
| `figures/` | 렌더링·DevTools 도식, 한·영 UI 캡처, 원본 비교 자료 |
| `week2-examples.zip`, `../examples/` | 별도 브라우저 개념 보조 예제; 실제 과제 소스와 구분 |

실습 원본은 `C:/Users/hsoh/Workspace/pwd-2026-practices/pwd-week2`입니다. 보관된 패키지 기준은 커밋 `5f4456240702bc6b599b83e91f9ecd816f90a1fb`입니다. `.git`, 설치 결과, 빌드 결과, 환경 변수 파일은 ZIP에 포함하지 않습니다. 사용자 요청에 따라 슬라이드의 실습 소스 다운로드 버튼과 관련 안내를 제거했습니다. 재생성 시에도 다운로드를 추가하지 않습니다.

검토 과정에서 만든 실습 소스 ZIP과 별도 영문 실습 안내는 학생용 배포 자료에서 제외합니다. 원본 슬라이드의 학습 목표·요구사항을 배포 기준으로 사용합니다.

## 슬라이드 작성 원본

| 범위 | 작성 원본 |
| --- | --- |
| 01–07 | 기존 index.html과 lecture-content.js; 재생성 시 보존 |
| 08–16, 21 및 전체 조립 | scripts/build-slides.cjs |
| 18–20 | scripts/chapter-three.cjs |
| 22–24 | scripts/chapter-four.cjs |
| 30·31·32·34·37·40·43·45·46 | scripts/svelte-corrections.cjs |
| 나머지 원본 이미지 23장 | scripts/complete-slides.cjs 및 complete-examples.cjs |

17·21·25·48·52번은 챕터 표지입니다. 13번 레이아웃 도식의 라벨도 번역하며 21번 DevTools 이미지는 언어별로 교체합니다. 54번 Q&A까지 모든 본문·제목·코드 UI 문구를 해당 언어로 제공합니다. 코드 글꼴 크기는 14px 인쇄 기준을 유지하고 검정 배경·녹색 Consolas 테마를 사용합니다. 09번 이후 별도의 우측 하단 참고 링크를 추가하지 않습니다.

```sh
node lectures/02/scripts/build-slides.cjs
npm run format:code --prefix packages/web-deck
npm test --prefix packages/web-deck
node lectures/02/scripts/check-svelte-corrections.cjs
node lectures/02/scripts/check-complete-slides.cjs
node lectures/02/scripts/check-slides.cjs
```

`refresh-svelte-slides.cjs`는 전체 생성기를 호출하는 호환 명령입니다. 브라우저 검증에는 저장소 루트의 HTTP 서버(기본 4186), Chrome, Playwright가 필요합니다. `DECK_URL`과 `PLAYWRIGHT_PATH`로 해당 경로를 지정할 수 있습니다. Svelte 예제 검증은 실습 폴더의 설치된 의존성을 사용하며 `SVELTE_PRACTICE_ROOT`로 경로를 변경할 수 있습니다. 실습 원본을 변경하지 않고 임시 폴더에서 실행합니다.

`check-svelte-corrections.cjs`는 기존 교정 예제의 컴파일·동작·load/API 성공 및 실패 처리를 검증합니다. `check-complete-slides.cjs`는 추가한 10개 예제의 한·영 20개 컴파일, 브라우저 상호작용, 실제 SvelteKit의 이동 취소와 하위 페이지 렌더링, 54장의 언어 전환과 이미지를 검사합니다. `check-slides.cjs`는 한·영 54장의 코드·본문 잘림과 모바일 가로 넘침을 확인하고 임시 폴더 `week2-slide-audit`에 108개 화면·한영 PDF·audit.json을 만듭니다. 원격 GitHub/Vercel 배포 여부는 이 로컬 검증으로 판정하지 않습니다.

## 사실 확인 근거

- [웹 렌더링 방식](https://web.dev/articles/rendering-on-the-web), [Core Web Vitals](https://web.dev/articles/vitals), [CLS](https://web.dev/articles/cls)
- [Google 모바일 로딩 속도 연구](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-new-industry-benchmarks/)
- [HTML 표준](https://html.spec.whatwg.org/multipage/), [CSSOM](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Object_Model), [CSS 캐스케이드](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction)
- [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/), [Device Mode](https://developer.chrome.com/docs/devtools/device-mode), [Network](https://developer.chrome.com/docs/devtools/network/reference/)
- [Node.js 소개](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs), [npx](https://docs.npmjs.com/cli/v11/commands/npx/), [sv create](https://svelte.dev/docs/cli/sv-create)
- [Svelte 문서](https://svelte.dev/docs/svelte/overview), [Runes](https://svelte.dev/docs/svelte/what-are-runes), [바인딩](https://svelte.dev/docs/svelte/bind), [props](https://svelte.dev/docs/svelte/$props)
- [SvelteKit 라우팅](https://svelte.dev/docs/kit/routing), [load](https://svelte.dev/docs/kit/load), [navigation](https://svelte.dev/docs/kit/$app-navigation)
- [Continuous Delivery](https://continuousdelivery.com/), [Vercel SvelteKit](https://vercel.com/docs/frameworks/full-stack/sveltekit), [Vercel Git](https://vercel.com/docs/git)

원본 그림의 재추출 스크립트는 `extract-rendering-diagram.py`, `extract-devtools-image.py`, `extract-original-slides.py`, `extract-framework-slides.py`입니다. 전체 페이지 재추출은 현재의 교정된 HTML이나 영문 내용을 덮어쓰지 않습니다.
