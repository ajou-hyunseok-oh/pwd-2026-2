# 2주차 슬라이드 최종 검토 — 2026-09-14

> 이 문서는 수정 전 발견 사항을 보존한 검토 기록이다. 이후 사용자의 전체 수정 및 영문 작성 요청을 반영했다. 현재 적용 내용과 검증 결과는 [수정 결과](completion-review-2026-09-14.md)를 기준으로 확인한다. 아래 ‘현재’, 줄 번호, 수정 필요 판정은 최초 검토 시점에 해당한다.

> 과제 마감은 이후 사용자 지정으로 **9월 20일 23:59**로 확정했다. 아래의 9월 12일 및 오전·오후 미확정 기록은 이전 검토 이력이다.

전체 54장을 검토한 결과, **현 상태를 오류 없는 최종본으로 판정할 수 없다.** 우선 수정 대상은 16번의 성능 지표·통계, 38번의 체크박스 동작, 41번의 코드 표기다. 설치 도구·CLI·렌더링·CI/CD·실습 범위 설명에도 아래 정정 사항이 남아 있다.

검토 기준은 현재 작업 트리의 `index.html`과 `lecture-content.js`다. 원본 이미지가 표시되는 23장은 SVG와 원문 JSON을 확인했고, 이미 HTML로 교체된 9장은 현재 화면의 내용을 기준으로 판단했다. 보관 중인 이전 원본의 오류를 현재 슬라이드 오류로 다시 집계하지 않았다. 번호는 화면의 **1–54번 순서**이며 `data-wd-slide` 값이나 원본 PDF 쪽수와 구분한다.

한국어 전체 내용, 제공되는 영어 번역, 코드·그림·실제 예제의 대응, 공식 문서, 브라우저 동작, 인쇄 배치를 확인했다. 실습 내용은 `../pwd-2026-practices/pwd-week2`의 현재 코드와 2026-09-14 갱신 README를 직접 확인했다. `materials/practice-context.md`의 9월 11일 버전 정보와 당시 README 문제는 현재 상태와 구분했다.

이번 작업은 검토다. 슬라이드·생성 스크립트·원본 PDF·실습 저장소는 수정하지 않았다. 아래 코드와 문구는 적용 전 수정안이다.

**수정이 필요한 내용**

1. **[우선 수정] 16번 — Core Web Vitals 구성과 성능 통계 오류**

   위치: `index.html:733`, `materials/figures/original-slides.json:11`, `original-rendering-performance.svg`.

   현재 Core Web Vitals를 FCP·LCP·CLS로 제시한다. 올바른 구성은 **LCP·INP·CLS**다. FCP는 보조 로딩 지표다. LCP는 뷰포트 안에서 가장 큰 이미지·텍스트 콘텐츠의 표시 시점, INP는 사용자 상호작용에 대한 응답성을 설명하는 지표로 정리한다. [Google Web Vitals](https://web.dev/articles/vitals)

   CLS의 현재 문구인 ‘페이지 로드 중 발생하는 레이아웃 이동 총합’도 정정해야 한다. 페이지 이용 중 발생한 **예기치 않은 레이아웃 이동 점수의 세션 윈도 합계 중 최댓값**이며, 초기 로드에 한정된 모든 이동의 단순 합이 아니다. 강의 문구는 ‘페이지 이용 중 예기치 않은 화면 이동을 측정하는 시각적 안정성 지표’로 간결하게 쓸 수 있다. [CLS 정의](https://web.dev/articles/cls)

   ‘1초 7%·3초 32%·5초 90%·7초 103% 이탈’은 그대로 사용할 수 없다. 이탈률 103%는 성립하지 않는다. Google/SOASTA 2017 자료의 32%·90%는 각각 **1초에서 3초·5초로 느려질 때 이탈 확률의 상대 증가**이며, 특정 시간의 절대 이탈률이 아니다. 해당 자료의 다른 값은 1→6초 106% 증가, 1→10초 123% 증가다. 현재 슬라이드의 ‘7초 103%’, ‘경쟁사로 이동’, ‘1초 7%’는 이 자료로 뒷받침되지 않는다. 수치 표를 삭제하거나 조사 연도·비교 기준·상대 증가임을 표시한 표로 교체한다. [Google/SOASTA 원자료](https://www.thinkwithgoogle.com/_qs/documents/2453/64237_mobile-page-speed-new-industry-benchmarks_D2QxHYw.pdf)

2. **[우선 수정] 38번 — 체크박스를 클릭해도 상태가 유지되지 않음**

   위치: `index.html:813`, `materials/figures/framework-slides.json:95`, `original-framework-28.svg`.

   `bind:checked={todo.done}`와 `onchange={() => toggle(todo)}`가 같은 상태를 함께 변경한다. 현재 실습 의존성인 **Svelte 5.57.0**으로 슬라이드 코드를 컴파일해 Chrome에서 실행한 결과, 첫 체크박스는 초기 상태와 두 번의 클릭 후 모두 `false`였다. `onchange`를 제거한 대조 코드에서는 `false → true → false`로 정상 변경됐다. 컴파일만으로는 발견되지 않는 실행 오류다.

   수정안: 체크박스는 아래처럼 바인딩만 사용하고, 다른 곳에서 사용하지 않는 `toggle` 함수도 제거한다.

   ```svelte
   <input type="checkbox" bind:checked={todo.done} />
   ```

   [실행 결과](materials/final-review/results.json)의 `browser.todos`와 `browser.todosFixed`에 비교 결과를 보존했다. `bind:checked` 자체가 입력과 상태를 연결한다. [Svelte 바인딩](https://svelte.dev/docs/svelte/bind)

3. **[우선 수정] 41번 — 문자열 줄바꿈과 레이아웃 예제의 불완전성**

   위치: `index.html:833`, `materials/figures/framework-slides.json:116`, `original-framework-31.svg`.

   표시된 코드의 `confirm('변경사항이 저장되지 않았습니다. …')`는 작은따옴표 문자열 중간에서 줄이 바뀐다. **화면의 줄바꿈을 그대로 옮긴 경우** Svelte 컴파일러가 `Unterminated string constant`를 반환했다. 해당 줄바꿈을 공백으로 합치면 컴파일된다. 원본 작성 도구의 자동 줄바꿈일 가능성과 별개로, 학생이 따라 쓸 코드 표기는 유효한 문법이어야 한다. 다음처럼 문자열 밖에서 줄을 나눈다. [JavaScript 문자열과 줄바꿈](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/String_literal_EOL)

   ```javascript
   const ok = confirm(
     '변경사항이 저장되지 않았습니다. ' +
     '이동하시겠어요?'
   );
   ```

   파일명이 `src/routes/+layout.svelte`인데 자식 페이지를 렌더링하는 코드가 없다. 전체 파일 예제로 따라 쓰면 하위 페이지 콘텐츠를 표시하지 못한다. **발췌임을 명시하거나**, Svelte 5 형식으로 `let { children } = $props();`와 `{@render children()}`를 포함해야 한다. 기존 `on:input`은 Svelte 5가 지원하는 legacy 문법이므로 그 자체를 컴파일 오류로 판단하지 않았다. 새 예제에서는 다른 장과 맞춰 `oninput`을 사용하고 `<textarea></textarea>`로 닫으면, 자체 닫힘 태그 경고도 해소할 수 있다. [SvelteKit 레이아웃](https://svelte.dev/docs/kit/routing#layout)

   설명의 `onNavigate`를 단순히 ‘렌더 직전’으로 대응시키는 것도 부정확하다. `beforeNavigate`·`onNavigate`는 탐색 전 개입 지점이고, `onNavigate`가 반환한 함수는 DOM 갱신 후 실행된다. `afterNavigate`는 최초 마운트와 탐색 후에 실행된다. 앱 밖으로 나가거나 탭을 닫는 경우에는 브라우저의 기본 이탈 확인 동작을 구분해야 한다. 이 검토에서 실제 SvelteKit 탐색·탭 닫기까지 재현한 것은 아니다. [탐색 API](https://svelte.dev/docs/kit/$app-navigation)

4. **[정정] 53번 — ‘정적 사이트 제작’과 실제 실습 구현 불일치**

   위치: `index.html:910`, `materials/figures/framework-slides.json:200`, `original-framework-43.svg`.

   실제 실습에는 `/api/projects`의 `+server.js`, 동적 상세 경로의 `+page.server.js`, universal load인 `projects/+page.js`가 있다. 현재 설정은 `adapter-auto`이며 `prerender = true`나 `ssr = false` 설정이 없다. 현재의 2026-09-14 실습 README도 ‘HTML, CSS, JavaScript를 활용한 웹사이트 제작’으로 설명한다.

   수정안: **‘SvelteKit으로 페이지·API·동적 라우팅을 포함한 웹사이트 제작’** 또는 README와 동일한 문구. SvelteKit으로 정적 사이트를 만들 수 있다는 사실과, 이번 실습이 정적 사이트 생성 실습이라는 주장은 구분해야 한다. [페이지 옵션과 기본 렌더링](https://svelte.dev/docs/kit/page-options)

5. **[정정] 49번 — Continuous Delivery 정의 오류**

   위치: `index.html:906`, `materials/figures/framework-slides.json:172`, `original-framework-39.svg`.

   ‘Continuous Delivery: 개발자의 변경 사항이 저장소에 Release’는 핵심을 잘못 설명한다. Continuous Delivery는 변경 사항을 자동 빌드·테스트하여 **언제든 운영 환경에 배포할 수 있는 상태**로 유지하는 방식이다. 운영 배포에 사람의 승인·결정이 남을 수 있다. Continuous Deployment는 검증을 통과한 변경의 운영 배포까지 자동으로 진행한다. ‘저장소에 올림’과 ‘운영 환경에 올림’의 구분으로 가르치지 않는다. [AWS Continuous Delivery](https://aws.amazon.com/devops/continuous-delivery/)

6. **[정정] 29번 — npx의 설치 설명과 Create React App 예시 갱신**

   위치: `index.html:755`, `materials/figures/framework-slides.json:32`, `original-framework-19.svg`.

   ‘패키지를 설치하지 않고도 실행’은 부정확하다. 로컬에서 사용할 수 있는 패키지를 실행하고, 필요하면 npm 캐시에 받아 설치한 후 실행한다. **‘별도의 전역 설치 없이 패키지 명령 실행’**으로 바꾸고 캐시 동작을 덧붙인다. [npm npx](https://docs.npmjs.com/cli/v11/commands/npx/)

   `npx create-react-app my-project`는 현재 신규 React 프로젝트 생성 예제로 부적절하다. React 팀은 2025-02-14 Create React App을 deprecated로 공지했다. ‘실행 불가능’이라는 뜻은 아니다. 이 강의에서는 SvelteKit 생성 명령만 남기는 편이 범위에 맞으며, React 예제가 필요하다면 현재 공식 안내에 맞춘 예제를 사용한다. [React 공식 공지](https://react.dev/blog/2025/02/14/sunsetting-create-react-app)

   `npx sv create my-project` 자체는 유효하다. 다만 실제 실습 README는 재현을 위해 `npx sv@0.17.0 create pwd-week2`로 버전을 고정하므로, 슬라이드 명령이 일반 사용 예인지 실습 명령인지 구분하면 좋다. [sv create](https://svelte.dev/docs/cli/sv-create)

7. **[정정] 28번 — 터미널·셸·경로·재현성의 혼동**

   위치: `index.html:754`, `materials/figures/framework-slides.json:25`, `original-framework-18.svg`.

   PowerShell을 터미널의 예로 들고 다시 셸로 설명한다. 터미널 예는 **Windows Terminal·macOS Terminal**, 셸 예는 **PowerShell·bash·zsh**로 구분한다. Windows PowerShell의 전통적인 콘솔 창을 떠올릴 수 있지만, 도구의 역할을 구분하는 교육 자료에서는 명칭을 명확히 하는 것이 필요하다. [Microsoft Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/)

   `Path`는 파일·디렉터리의 위치를 나타내는 표현이며, 현재 작업 디렉터리는 `cwd`다. **‘경로(Path): 파일·폴더의 위치 표기 / 현재 작업 디렉터리(cwd): 상대 경로 해석의 기준’**으로 정정한다.

   ‘같은 명령을 실행하면 항상 같은 결과’는 잘못된 보장이다. 예를 들어 버전을 고정하지 않은 생성 명령은 최신 패키지 버전·현재 폴더·설정에 따라 결과가 달라진다. **‘환경·버전·입력을 고정하고 명령을 기록해 재현성 향상’**으로 바꾼다.

8. **[정정] 15번 — 렌더링 방식의 속도·SEO를 단정하는 표현**

   위치: `index.html:732`, `materials/figures/original-slides.json:4`, `original-rendering-methods.svg`.

   CSR은 항상 초기 로딩이 느리고 SSR은 항상 빠르다는 식으로 읽힌다. SSR도 서버 응답·리소스 로드·hydration 비용이 있으며, HTML 표시와 상호작용 가능 시점은 다를 수 있다. SSG의 CDN 사용도 정의의 필수 조건은 아니다. 20번은 이러한 조건을 정확하게 구분하고 있어 두 장 사이의 설명 강도가 맞지 않는다. [웹 렌더링 방식과 성능](https://web.dev/articles/rendering-on-the-web)

   수정안: **CSR ‘주요 콘텐츠 생성에 브라우저 JavaScript 실행 필요’, SSR ‘서버가 생성한 HTML 제공’, SSG ‘빌드 시 생성한 HTML 제공’**를 기본 정의로 사용한다. 속도·검색 처리상 이점은 조건부로 표현한다. SSR/SSG로 처음 표시한 뒤 CSR과 클라이언트 라우팅을 결합할 수 있다는 점도 일관되게 설명한다. Facebook·Instagram은 제품 전체가 단일 방식만 쓴다고 확인한 사례가 아니므로 ‘상호작용이 많은 피드·대시보드’ 같은 일반 용례로 바꾸는 편이 정확하다.

9. **[정정·경고] 36번 — `$effect` 설명과 DOM 참조 선언**

   위치: `index.html:794`, `materials/figures/framework-slides.json:81`, `original-framework-26.svg`.

   `$state`·`$derived`·`$effect`를 ‘값 유형’으로 묶지만 `$effect`는 값을 선언하는 자료형이 아니다. **‘반응성 관련 runes’**로 제목을 바꾼다. ‘순수 계산 금지’도 언어 규칙이 아니다. **‘표시용 파생값은 `$derived`로 계산하고, `$effect`는 외부 동작과의 동기화에 사용’**으로 고친다. `$effect` 안에서 `console.log(n * 2)`를 실행하는 코드는 정상 컴파일·실행됨을 확인했다.

   의존성은 **동기적으로 읽은 반응형 값**이며, 최초 실행도 있고 재실행은 묶여 처리된다. ‘읽힌 값 모두’, ‘바뀔 때마다’만으로 설명하면 일반 변수·비동기 콜백까지 추적하는 것으로 오해할 수 있다. 40번 본문의 더 정확한 설명과 맞춘다. [Svelte $effect](https://svelte.dev/docs/svelte/$effect)

   마지막 예제의 `let el;`은 현재 컴파일러에서 `non_reactive_update` 경고를 낸다. 현재 예제의 Open 클릭 후 포커스 이동은 성공했으므로 동작 불능으로 분류하지 않았다. `let el = $state();`로 바꾸면 경고 없이 컴파일된다. [실행·컴파일 결과](materials/final-review/results.json)

10. **[정정] 38번 — 반복문 설명의 오기와 불필요한 제약**

    위치는 위 38번과 같다. 반복문 설명인데 소제목이 **‘템플릿 조건 블록 (렌더 분기)’**다. **‘템플릿 반복 블록 (`{#each}`)’**으로 바꾼다.

    ‘결과를 UI에 쓰려면 `$state` 또는 `$derived`에 담아야 함’도 지나친 제약이다. `const items = [1, 2]`를 `{#each items as item}`으로 정상 표시하는 대조 예제를 확인했다. **‘변경에 따라 UI를 갱신할 값에는 반응형 상태·파생값 사용’**으로 정정한다. [실행 결과](materials/final-review/results.json)

11. **[정정] 40번 — 한국어 리드의 실행 시점 표현**

    위치: `index.html:815`, `lecture-content.js:73`, `scripts/svelte-corrections.cjs:200`.

    리드가 ‘상태 변경 전후의 DOM 작업을 구분’으로 되어 있다. `$effect.pre`가 상태 변경 전에 실행되는 것은 아니다. 본문·영어 리드와 맞춰 **‘마운트·해제 시 리소스를 관리하고 DOM 갱신 전후의 작업을 구분’**으로 수정한다. 타이머 생성·정리와 본문의 `$effect.pre`/`$effect` 설명은 검사를 통과했다. [Svelte $effect.pre](https://svelte.dev/docs/svelte/$effect#$effect.pre)

12. **[경미] 13번 — 영어 모드에서 도식 내부의 한국어 잔존**

    위치: `index.html:614`, `scripts/build-slides.cjs:104`의 `layoutDrawing()`.

    EN으로 바꿔도 도식의 ‘자기소개’, ‘나의 첫 웹사이트 제작 중’이 한국어로 남는다. 번역 사전에 `v2_layout_heading`·`v2_layout_text`는 존재하지만 해당 DOM에 번역 속성이 없다. 생성 스크립트와 결과 HTML의 두 요소에 `data-wd-i18n` 연결이 필요하다.

    실측값 자체는 정상이다. 한·영 예제를 모두 다시 측정해 카드 폭 360px, 좌우 padding 24px, 콘텐츠 폭 312px, 버튼 위치 x=24px·y=117.984375px를 확인했다. 슬라이드의 y=118.0px는 올바른 반올림이다.

13. **[경미] 26·27·33·35·44번 — 용어·오타·설명 범위 정리**

    | 슬라이드 | 현재 표현 | 정리안 |
    | --- | --- | --- |
    | 26 | UI 프레임워크 목록에 React 포함 | 분류명을 ‘UI 라이브러리·프레임워크’로 쓰면 더 정확함. 라우터·ORM 등을 모든 프레임워크의 필수 구성으로 단정하지 않고 예시로 표시 |
    | 27 | 단일 스레드·높은 성능·적은 메모리 | ‘JavaScript 콜백은 주로 이벤트 루프에서 처리’로 범위 명시. Node 전체가 한 스레드라는 뜻이 아니며 성능·메모리는 작업에 따라 달라짐 |
    | 33 | `ㅇmy-sveltekit-app/` | 앞의 불필요한 `ㅇ` 제거 |
    | 35 | `페이지(+page.svelte}` | `페이지(+page.svelte)`로 괄호 수정 |
    | 44 | ‘UI를 이루는 가장 작은 재사용 단위’ | ‘UI를 구성하는 재사용 가능한 단위’. 컴포넌트는 큰 페이지도 구성할 수 있음 |

    27번의 이벤트 루프와 worker pool 구분은 [Node.js 공식 설명](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)을 기준으로 했다. 33번의 프로젝트 트리는 예시로서 사용할 수 있으며, 모든 생성 옵션에서 동일한 파일이 자동 생성된다는 보장으로 설명하지 않는다.

14. **[접근 확인] 53번 — 참고 저장소의 비로그인 접근 404**

    `https://github.com/ajou-hyunseok-oh/pwd-week2`와 해당 GitHub 공개 API 주소가 모두 **HTTP 404**를 반환했다. 로컬 실습 저장소는 존재한다. 삭제·이전·비공개 여부를 이 응답만으로 단정할 수 없으므로, 학생 계정의 접근 권한 또는 실제 배포용 링크를 확인해야 한다. 공개 열람을 전제하는 안내로는 검증되지 않았다. 제공 중인 `week2-examples.zip`은 별도의 HTML·React 설명용 예제이며 SvelteKit 실습의 대체 배포본이 아니다.

    마감일 **9월 12일**은 자료에 기록된 기존 사용자 지정이므로 오류로 판단하거나 변경하지 않았다. ‘11시 59분’은 오전·오후가 불명확하므로 운영 안내에서는 시각을 명확히 표시할 필요가 있다. 23:59로 임의 추정하지 않았다.

**오류로 판단하지 않은 항목.** 42번 `const { msg } = $props()`는 현재 Svelte에서 정상 컴파일되고, 부모의 반응형 값 변경도 자식에 반영된다. 36번의 각 코드 상자는 별도 예제이므로 한 파일에 `<script>`가 세 개 있다는 오류로 판단하지 않았다. 원본 SVG 23장이 영어 모드에서도 한국어를 유지하는 것은 저장소에 명시된 의도이며, 13번 HTML 도식의 번역 누락과 구분했다. 30·31·32·34·37·40·43·45·46번은 이전에 교정된 현재 HTML 내용을 검토했다.

**검증 결과.** 실행 증거는 [results.json](materials/final-review/results.json)에 보존했다.

| 검사 | 결과와 한계 |
| --- | --- |
| `npm.cmd test --prefix packages/web-deck` | 통과. 13개 강의 덱 구조와 19개 코드 블록·36개 언어 변형 검사. SVG 내부의 코드 실행·문장 사실관계 검사는 포함하지 않음 |
| `node lectures/02/scripts/check-svelte-corrections.cjs` | 통과. Svelte 5.57.0, 7개 컴포넌트 무경고 컴파일. JS/TS 카운터, 등급, 입력·파일 바인딩, 타이머 해제, 경로 데이터, API→페이지 흐름 확인 |
| 원본 이미지의 Svelte 예제 별도 실행 | 36번 상태·합계·포커스, 39번 마우스, 42번 props 갱신, 44번 카드 표시 정상. 38번 체크박스 실패 재현. 41번 표시된 줄바꿈 보존 시 컴파일 실패 재현 |
| 오류 수정안의 대조 확인 | 38번 `onchange` 제거 후 정상. 36번 `el = $state()` 선언 후 컴파일 경고 없음. 41번 문자열 줄 연결 후 파싱 성공, textarea 자체 닫힘 경고는 남음 |
| CSS·좌표 대응 | 문단 글자색 `#333`, hover 배경 `#174f37`, 360−24−24=312px, 버튼 x=24·y≈118px 확인 |
| 한·영 54장 배치 검사 | 이미지 누락·코드 가로 넘침·코드 표식 누락·클라이언트 JS 예외 없음. 390×844 모바일 뷰포트에서 슬라이드 가로 넘침 없음 |
| `check-slides.cjs`의 종료 결과 | **실패(exit 1)**. 원본 SVG 23장 각각에 하단 20px 여백을 일괄 요구하면서 생긴 경고. 이미지 경계를 따로 측정한 결과 한·영 모두 슬라이드 경계 이탈 0건. 이를 실제 이미지 잘림으로 집계하지 않음 |
| PDF 출력 | 한국어 54쪽 생성 확인. 슬라이드당 1쪽, 16:9 크기 |
| 외부 서비스 | Svelte Playground 접근 성공. 실습 GitHub 공개 접근 404. GitHub 계정 연동·Vercel 배포·실제 학생 권한은 실행하거나 확인하지 않음 |

검토 중 생성한 캡처·PDF와 재현용 코드는 임시 폴더 `C:/Users/hsoh/AppData/Local/Temp/week2-slide-audit/`, `C:/Users/hsoh/AppData/Local/Temp/week2-final-review/`, `C:/Users/hsoh/AppData/Local/Temp/week2-final-review.cjs`에 있다. 보존한 JSON은 위 상대 링크로 열 수 있다.

**54장별 검토 기록.** ‘이상 없음’은 이번 범위에서 오류를 발견하지 않았다는 뜻이며 실제 외부 배포까지 보장하는 표현은 아니다.

| 번호 | 주제 | 판정 |
| --- | --- | --- |
| 01 | 표지 | 학기·주차 표시 이상 없음 |
| 02 | 학습 목표 | 현재 본문 범위와 일치 |
| 03 | 구성 요소와 역할 표지 | 이상 없음 |
| 04 | HTML·CSS·JavaScript 역할 | 설명과 소개 변경 데모 정상 |
| 05 | HTML | 문서 선언·요소·속성·defer 코드 이상 없음 |
| 06 | CSS | 선택자·선언·코드 이상 없음 |
| 07 | JavaScript | 언어와 브라우저 API 구분·함수 예제 이상 없음 |
| 08 | 렌더링 원리 표지 | 이상 없음 |
| 09 | 렌더링 과정 | 입문용 단계 도식으로 사용 가능 |
| 10 | DOM | 설명·예제 요소 대응 이상 없음 |
| 11 | CSSOM | 매칭·캐스케이드·상속 및 실제 색상 확인 |
| 12 | 렌더 트리 | 선택한 주요 요소·스타일의 개념도로 사용 가능 |
| 13 | 레이아웃 | 치수·좌표 정상. EN 도식 텍스트 번역 누락 |
| 14 | 페인트 | 색상 대응과 레이어 개념도 주의 문구 이상 없음 |
| 15 | CSR·SSR·SSG | 속도·SEO·CDN 관련 단정 완화 필요 |
| 16 | 렌더링 성능 | CWV 구성·CLS 정의·이탈 통계 우선 수정 |
| 17 | 시맨틱 HTML과 라우팅 표지 | 이상 없음 |
| 18 | 시맨틱 HTML | 요소 의미·검색 처리·접근성 설명에서 오류 미발견. SEO/AEO/GEO는 보장·배타적 분류로 제시되지 않음 |
| 19 | URL | path·query·fragment·매개변수 구분 정상 |
| 20 | 서버·클라이언트 라우팅 | 렌더링·탐색 구분과 조건부 성능 설명 정상 |
| 21 | 개발자 도구 표지 | 이미지 표시 정상 |
| 22 | Elements·메타데이터 | 현재 DOM과 응답 HTML 구분 정상 |
| 23 | 뷰포트 | CSS 픽셀·시뮬레이션 한계 설명 정상 |
| 24 | Network | 문서 선택·헤더·응답·DOM 구분 정상 |
| 25 | 웹 프레임워크 개발 표지 | 이상 없음 |
| 26 | 프레임워크 | 구성 요소는 예시임을 명확히 하고 UI 라이브러리 분류 보완 권장 |
| 27 | Node.js | 핵심 정의 정상. 단일 스레드·성능 표현 범위 보완 권장 |
| 28 | CLI | 터미널·셸·경로·재현성 설명 정정 |
| 29 | npm·npx | 설치 설명 정정, CRA 예시 갱신 |
| 30 | Svelte·SvelteKit | 역할·런타임·JS/TS 설명 정상 |
| 31 | 프론트엔드 비교 | 조건 없는 크기·성능 등급이 제거된 현재 표에서 오류 미발견 |
| 32 | Svelte 파일과 언어 | JS/TS 예제 무경고 컴파일·동작 정상 |
| 33 | 프로젝트 구조 | 루트 경로 앞 `ㅇ` 오타 |
| 34 | 파일 기반 라우팅 | params→load→data 흐름 정상 |
| 35 | 중첩 라우팅 | 개념 정상. 닫는 괄호 오타 |
| 36 | 변수·runes | `$effect` 설명 정정, `el` 선언 경고. 제시 동작은 정상 |
| 37 | 조건문 | `$derived.by`와 등급별 출력 정상 |
| 38 | 반복문 | 체크박스 실패 재현. 반복 블록 소제목·runes 필수 주장도 정정 |
| 39 | 이벤트 | 마우스 좌표 갱신 정상. 높이 100%는 부모 높이에 종속되므로 전체 화면 보장으로 읽지 않음 |
| 40 | 라이프사이클 | 코드·본문 정상. 한국어 리드의 ‘상태 변경 전후’ 정정 |
| 41 | 훅 | 문자열 줄바꿈·레이아웃 발췌 범위·탐색 훅 실행 시점 정리 |
| 42 | props | const 구조 분해와 부모→자식 갱신 확인 |
| 43 | 양방향 바인딩 | 입력·체크·선택·범위·파일 바인딩 정상 |
| 44 | 컴포넌트 | 카드 표시·링크 정상. ‘가장 작은’ 표현 정리 권장 |
| 45 | API 라우트 | 서버 코드·응답·요청별 locals·load 구분 정상 |
| 46 | API→페이지 | 정상·실패 응답 및 3개 카드 전달 검사 통과 |
| 47 | Playground | 표시 URL 접근 성공 |
| 48 | 배포 자동화 표지 | 이상 없음 |
| 49 | CI/CD | Continuous Delivery 정의 정정 |
| 50 | Vercel | 주요 기능·Rich Harris의 2021년 합류 사실 확인. 배포 성공을 검증한 것은 아님 |
| 51 | Vercel 시작 | 저장소 가져오기·SvelteKit 자동 감지·배포의 기본 흐름 정상. 실제 계정 화면·권한 검증 제외 |
| 52 | 실습 표지 | SvelteKit·Vercel 실습과 일치 |
| 53 | 실습 개요 | 정적 사이트 표현 정정. 공개 링크 404. 기존 마감일 유지, 시각 표기 명확화 필요 |
| 54 | Q&A | 이상 없음 |

배포 관련 대조에는 [Vercel의 SvelteKit 지원](https://vercel.com/docs/frameworks/full-stack/sveltekit), [Git 배포 안내](https://vercel.com/docs/git), [2021년 Rich Harris 합류 공지](https://vercel.com/blog/vercel-welcomes-rich-harris-creator-of-svelte)를 사용했다. 이번에 확인하지 않은 사용자 계정의 설정이나 과제 제출 상태를 이 문서에서 추정하지 않는다.

현재 SVG로 표시되는 오류를 고칠 때는 JSON의 원문이나 이미지 alt만 바꾸면 화면은 그대로 남는다. 실제 표시 자산 또는 해당 슬라이드를 생성하는 경로에 수정이 반영되어야 한다. HTML 슬라이드는 `scripts/build-slides.cjs`·`scripts/svelte-corrections.cjs`와 번역을 함께 맞춰야 재생성 시 오류가 되돌아오지 않는다.
