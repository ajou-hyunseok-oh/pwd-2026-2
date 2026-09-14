// Replaces the remaining PDF-only pages with corrected Korean/English slides.
const { localized } = require('./complete-examples.cjs');
const deadline = { ko: '9월 20일 23:59', en: 'September 20, 23:59' };

function render(page, { add, t, p, grid, code, chapter }) {
  const n = page.id.startsWith('original-framework-') ? page.page : page.id;
  const supported = ['original-rendering-methods', 'original-rendering-performance', 15, 16, 17, 18, 19, 23, 25, 26, 28, 29, 31, 32, 34, 37, 38, 39, 40, 41, 42, 43, 44];
  if (!supported.includes(n)) return false;
  const key = suffix => 'w2_' + String(n).replaceAll('-', '_') + '_' + suffix;
  const heading = (suffix, ko, en) => t('h3', key(suffix), ko, en);
  const para = (suffix, ko, en, cls = '') => p(key(suffix), ko, en, cls);
  const box = (suffix, ko, en, body) => `<section class="lesson-concept-box">${heading(suffix, ko, en)}${body}</section>`;
  const note = (suffix, ko, en) => para(suffix, ko, en, 'lesson-concept-note');
  const list = (suffix, pairs, ordered = false) => `<${ordered ? 'ol' : 'ul'} class="lesson-navigation-flow">${pairs.map(([ko, en], i) => t('li', key(suffix + i), ko, en)).join('')}</${ordered ? 'ol' : 'ul'}>`;
  const sample = (name, label, width = 58) => code(key('code_' + name), 'text', localized(name), label, [], width);
  const plainCode = (suffix, values, label, width = 58, lang = 'text') => code(key(suffix), lang, values, label, [], width);
  const slide = (title, lead, body) => add(page.id, page.page, title, lead, body);
  const flow = (suffix, pairs) => `<div class="lesson-concept-flow">${pairs.map(([ko, en], i) => `${i ? '<span aria-hidden="true">→</span>' : ''}<div>${t('span', key(suffix + i), ko, en)}</div>`).join('')}</div>`;

  switch (n) {
    case 'original-rendering-methods':
      slide(['웹 브라우저 렌더링 방식', 'Web Rendering Strategies'],
        ['주요 콘텐츠를 생성하는 위치와 시점의 차이', 'Differences in where and when page content is generated'],
        grid(
          box('csr', 'CSR · 클라이언트 렌더링', 'CSR · Client-side Rendering',
            para('csr_flow', 'HTML 골격 → JavaScript → 브라우저에서 UI 생성', 'HTML shell → JavaScript → UI generated in the browser') +
            list('csr_points', [
              ['실행 후 상태 변경에 따라 화면 갱신', 'UI updates in response to state changes'],
              ['초기 콘텐츠 표시에 JavaScript 다운로드·실행 필요', 'Initial content depends on JavaScript download and execution'],
              ['검색 처리 시 JavaScript 렌더링 지원·실행 비용 고려', 'Search processing depends on JavaScript support and rendering cost']
            ]) + note('csr_use', '용례: 상호작용이 많은 피드·대시보드', 'Typical use: interactive feeds and dashboards')),
          box('ssr', 'SSR · 서버 렌더링', 'SSR · Server-side Rendering',
            para('ssr_flow', '요청 → 서버에서 HTML 생성 → 브라우저에 제공', 'Request → HTML generated on the server → browser') +
            list('ssr_points', [
              ['초기 응답에 주요 콘텐츠 포함', 'Main content included in the initial response'],
              ['서버 처리 시간·부하·캐시 전략 고려', 'Server response time, load and caching matter'],
              ['화면 표시와 상호작용 준비 시점은 다를 수 있음', 'Content can appear before hydration makes it interactive']
            ]) + note('ssr_use', '용례: 요청 시점의 데이터가 필요한 페이지', 'Typical use: pages requiring request-time data')),
          box('ssg', 'SSG · 정적 사이트 생성', 'SSG · Static Site Generation',
            para('ssg_flow', '빌드 시 HTML 생성 → 정적 파일 제공', 'HTML generated at build time → served as static files') +
            list('ssg_points', [
              ['요청마다 HTML을 생성할 필요 없음', 'No need to generate HTML for every request'],
              ['CDN 캐싱에 적합 · CDN은 필수 조건이 아님', 'Well suited to CDN caching; a CDN is optional'],
              ['미리 생성한 콘텐츠 변경에는 재생성 필요', 'Changes to pregenerated content require regeneration']
            ]) + note('ssg_use', '용례: 문서·블로그·마케팅 페이지', 'Typical use: documentation, blogs and marketing pages'))
        ) + note('combine', 'SSR·SSG의 초기 HTML과 클라이언트 갱신을 조합 가능 · 속도와 SEO는 코드·콘텐츠·네트워크·캐시에도 좌우됨', 'Initial SSR or SSG can be combined with client updates; performance and SEO also depend on code, content, networks and caching'));
      break;
    case 'original-rendering-performance':
      slide(['웹 브라우저 렌더링 성능', 'Web Rendering Performance'],
        ['로딩·상호작용·화면 안정성이 사용자 경험에 미치는 영향', 'Loading, responsiveness and visual stability shape the user experience'],
        grid(
          box('vitals', 'Core Web Vitals · LCP / INP / CLS', 'Core Web Vitals · LCP / INP / CLS',
            heading('lcp', 'LCP · Largest Contentful Paint', 'LCP · Largest Contentful Paint') +
            para('lcp_body', '뷰포트 안의 가장 큰 이미지·텍스트 콘텐츠가 표시되는 시점 · 로딩 성능', 'When the largest image or text content in the viewport is rendered · loading performance') +
            heading('inp', 'INP · Interaction to Next Paint', 'INP · Interaction to Next Paint') +
            para('inp_body', '클릭·탭·키보드 입력부터 다음 화면 표시까지의 지연을 바탕으로 상호작용 응답성 평가', 'Responsiveness based on delays from clicks, taps and keyboard input to the next paint') +
            heading('cls', 'CLS · Cumulative Layout Shift', 'CLS · Cumulative Layout Shift') +
            para('cls_body', '페이지 이용 중 예기치 않은 레이아웃 이동 점수 · 세션 윈도 합계 중 최댓값', 'Unexpected layout shift scores throughout a page visit · the largest session-window total') +
            note('fcp', 'FCP는 첫 텍스트·이미지 등의 표시 시점인 보조 로딩 지표', 'FCP is a supporting loading metric for the first text, image or other content')),
          box('bounce', '로딩 지연과 이탈 확률', 'Load Delay and Bounce Probability',
            para('study', 'Google/SOASTA 모바일 연구 · 2017년 · 1초 로딩 대비 상대 증가', 'Google/SOASTA mobile research · 2017 · relative increases compared with a 1-second load') +
            `<table class="lesson-table"><thead><tr><th>${t('span', key('load'), '로딩 시간 변화', 'Load-time Change')}</th><th>${t('span', key('increase'), '이탈 확률 증가', 'Increase in Bounce Probability')}</th></tr></thead><tbody><tr><td>1s → 3s</td><td>+32%</td></tr><tr><td>1s → 5s</td><td>+90%</td></tr><tr><td>1s → 6s</td><td>+106%</td></tr></tbody></table>` +
            note('relative', '절대 이탈률이 아닌 상대 증가율 · 모든 사이트에 같은 값이 적용되는 법칙이 아님', 'Relative increases, not absolute bounce rates or universal predictions for every site') +
            para('seo', '성능 개선은 사용자 경험과 검색 품질에 도움 · 특정 검색 순위나 전환율을 보장하지 않음', 'Better performance supports user experience and search quality; it does not guarantee rankings or conversion rates'))
        ));
      break;
    case 15:
      chapter(page.id, page.page, '05', ['웹 프레임워크를 활용한 개발', 'Development with Web Frameworks'], ['Svelte · SvelteKit · 컴포넌트 · 데이터', 'Svelte · SvelteKit · Components · Data']);
      break;
    case 16:
      slide(['웹 개발 프레임워크', 'Web Development Frameworks'],
        ['반복 작업과 프로젝트 구조를 위한 규칙·도구', 'Conventions and tools for project structure and recurring development tasks'],
        grid(box('parts', '제공 기능의 예', 'Examples of Framework Features', list('parts_items', [
          ['구조: 폴더·파일 규칙, 역할별 코드 분리', 'Structure: file conventions and separation of responsibilities'],
          ['요청 처리: 라우터·미들웨어·입력 검증·인증 연동', 'Request handling: routing, middleware, validation and authentication integration'],
          ['데이터: 로드 함수·데이터베이스 접근 도구', 'Data: loading functions and database access tools'],
          ['빌드·실행: 번들링·코드 분할·렌더링·배포', 'Build and runtime: bundling, code splitting, rendering and deployment']
        ]) + note('parts_note', '기능은 프레임워크마다 다르며 추가 라이브러리가 필요할 수 있음', 'Features vary by framework and may require additional libraries')),
        box('types', '개발 영역별 도구', 'Tools by Development Area',
          heading('ui', 'UI 라이브러리·프레임워크', 'UI Libraries and Frameworks') + para('ui_names', 'React · Vue · Angular · Svelte', 'React · Vue · Angular · Svelte') +
          heading('backend', '백엔드 프레임워크', 'Backend Frameworks') + para('backend_names', 'Express · NestJS · Django · FastAPI · Spring Boot', 'Express · NestJS · Django · FastAPI · Spring Boot') +
          heading('full', '풀스택 프레임워크', 'Full-stack Frameworks') + para('full_names', 'Next.js · Nuxt · SvelteKit', 'Next.js · Nuxt · SvelteKit'))) +
        note('choose', '선택 기준: 팀의 언어·경험, 필요한 렌더링·서버 기능, 호스팅 환경, 문서·생태계·유지보수', 'Selection criteria: team skills, rendering and server needs, hosting, documentation, ecosystem and maintenance'));
      break;
    case 17:
      slide(['Node.js 실행 환경', 'The Node.js Runtime'],
        ['V8 엔진을 사용해 브라우저 밖에서 JavaScript 실행', 'JavaScript outside the browser, powered by the V8 engine'],
        grid(box('runtime', '실행 환경과 용도', 'Runtime and Uses', list('runtime_items', [
          ['개발 서버·빌드 도구·CLI·서버 프로그램 실행', 'Runs development servers, build tools, CLIs and server programs'],
          ['브라우저의 document·window 대신 파일·프로세스 등 서버 API 사용', 'File and process APIs instead of browser globals such as document and window'],
          ['npm으로 프로젝트 의존성과 실행 명령 관리', 'npm manages project dependencies and scripts']
        ]) + plainCode('node_code', "console.log('Hello from Node.js');", 'hello.js', 56, 'javascript') + plainCode('node_cmd', 'node hello.js', 'Terminal', 56, 'bash')),
        box('io', '비동기 I/O와 이벤트 루프', 'Asynchronous I/O and the Event Loop', list('io_items', [
          ['I/O 완료를 기다리는 동안 다른 요청의 작업 진행 가능', 'Other requests can make progress while I/O is pending'],
          ['JavaScript 콜백은 주로 하나의 이벤트 루프에서 처리', 'JavaScript callbacks run mainly on one event loop'],
          ['일부 I/O·연산은 운영체제와 worker pool 등이 처리', 'The OS and worker pool handle some I/O and other work'],
          ['긴 동기 연산은 이벤트 루프를 막아 다른 요청도 지연', 'Long synchronous work blocks the event loop and delays other requests']
        ]) + note('io_note', '비동기 구조만으로 높은 성능·적은 메모리가 보장되지는 않음', 'Asynchronous design alone does not guarantee speed or low memory use'))) +
        para('version', '실습 환경: Node.js 24 · node -v / npm -v로 확인', 'Practice environment: Node.js 24 · verify with node -v / npm -v', 'lesson-devtools-shortcut'));
      break;
    case 18:
      slide(['CLI · 명령줄 인터페이스', 'CLI · Command-line Interface'],
        ['텍스트 명령으로 도구를 실행하고 작업을 자동화하는 인터페이스', 'An interface for running tools and automating tasks with text commands'],
        grid(box('terms', '터미널·셸·경로', 'Terminal, Shell and Paths',
          heading('terminal', '터미널', 'Terminal') + para('terminal_body', '입력·출력을 표시하는 프로그램 · Windows Terminal, macOS Terminal', 'An application displaying input and output · Windows Terminal, macOS Terminal') +
          heading('shell', '셸', 'Shell') + para('shell_body', '명령을 해석·실행하는 프로그램 · PowerShell, bash, zsh', 'A program interpreting and executing commands · PowerShell, bash, zsh') +
          heading('path', '경로와 현재 작업 디렉터리', 'Paths and the Working Directory') + para('path_body', 'Path: 파일·폴더의 위치 표기 · cwd: 상대 경로 해석의 기준 폴더', 'Path: a file or directory location · cwd: the directory used to resolve relative paths') +
          para('prompt', '프롬프트: 입력 대기 표시 · . 현재 폴더 · .. 상위 폴더 · ~ 홈 폴더', 'Prompt: ready for input · . current directory · .. parent directory · ~ home directory')),
        box('commands', '프로젝트에서 명령 실행', 'Running Commands in a Project',
          plainCode('cli', 'cd pwd-week2\nnode -v\nnpm -v\nnpm run dev', 'Terminal', 56, 'bash') +
          list('cli_items', [
            ['같은 절차를 스크립트로 반복·자동화', 'Repeat and automate procedures with scripts'],
            ['버전·입력·환경을 고정해 재현성 향상', 'Improve reproducibility by fixing versions, inputs and environments'],
            ['같은 명령도 작업 폴더·설정·버전에 따라 결과가 달라짐', 'The same command can differ with the directory, configuration or version']
          ]))));
      break;
    case 19:
      slide(['npm과 npx', 'npm and npx'],
        ['프로젝트 의존성 관리와 패키지 명령 실행', 'Managing project dependencies and running package commands'],
        grid(box('npm', 'npm · 패키지와 스크립트 관리', 'npm · Packages and Scripts',
          list('npm_points', [
            ['package.json: 의존성과 scripts 정의', 'package.json: dependencies and script definitions'],
            ['package-lock.json: 재현 가능한 설치를 위한 버전 기록', 'package-lock.json: resolved versions for reproducible installation'],
            ['npm install: 의존성 설치 · npm run dev: dev 스크립트 실행', 'npm install: install dependencies · npm run dev: run the dev script']
          ]) + plainCode('npm_commands', 'npm --version\nnpm install\nnpm run dev', 'Terminal · npm', 56, 'bash') +
          note('ci', '받은 실습 소스는 npm ci로 잠금 파일에 맞춰 설치', 'For the supplied practice source, use npm ci to install from the lockfile')),
        box('npx', 'npx · 패키지 명령 실행', 'npx · Running Package Commands',
          para('npx_body', '별도의 전역 설치 없이 명령 실행 · 로컬 패키지를 사용하거나 필요 시 npm 캐시에 설치', 'Runs commands without a separate global installation; uses local packages or installs them in the npm cache') +
          plainCode('npx_commands', 'npx sv@0.17.0 create pwd-week2\ncd pwd-week2\nnpm run dev', 'Terminal · SvelteKit', 56, 'bash') +
          note('npx_scope', '새 프로젝트 생성 명령 · 이미 받은 프로젝트에서 다시 실행하지 않음', 'For creating a new project; do not rerun it inside the supplied project') +
          para('windows', 'PowerShell 실행 정책 오류 시 npm.cmd·npx.cmd 사용', 'If PowerShell blocks the .ps1 launcher, use npm.cmd and npx.cmd'))));
      break;
    case 23:
      slide(['SvelteKit 프로젝트 구조', 'SvelteKit Project Structure'],
        ['파일의 위치와 이름으로 페이지·공유 코드·설정의 역할 구분', 'File locations and names distinguish pages, shared code and configuration'],
        grid(plainCode('tree', `pwd-week2/
├─ src/
│  ├─ routes/
│  ├─ lib/
│  ├─ app.html
│  └─ app.css
├─ static/
├─ package.json
├─ package-lock.json
├─ svelte.config.js
├─ vite.config.js
├─ .gitignore
└─ README.md`, 'Project Files', 52),
        box('roles', '주요 파일과 폴더', 'Key Files and Directories', list('roles_list', [
          ['src/routes: 페이지·레이아웃·load·API 라우트', 'src/routes: pages, layouts, load functions and API routes'],
          ['src/lib: 재사용 코드 · $lib 별칭으로 import', 'src/lib: shared code imported with the $lib alias'],
          ['src/app.html: HTML 바깥 틀 · app.css: 가져와 적용할 전역 스타일', 'src/app.html: HTML shell · app.css: global styles to import'],
          ['static: 변환 없이 제공할 정적 파일', 'static: assets served without transformation'],
          ['설정 파일: 패키지·SvelteKit·Vite의 동작 구성', 'Configuration files: package, SvelteKit and Vite settings']
        ]) + note('installed', 'node_modules는 설치 시 생성 · Git에 추가하지 않음', 'node_modules is generated during installation and excluded from Git'))) +
        note('options', '실습 프로젝트의 구조 예시 · 생성 옵션과 사용하는 도구에 따라 파일 구성은 달라질 수 있음', 'Structure of the practice project; generated files vary with selected options and tools'));
      break;
    case 25:
      slide(['중첩 라우팅과 공유 레이아웃', 'Nested Routes and Shared Layouts'],
        ['폴더 계층으로 URL을 구성하고 공통 UI와 데이터를 재사용', 'Directory nesting defines URLs and supports shared UI and data'],
        grid(plainCode('nested_tree', `src/routes/
├─ +layout.svelte
├─ +layout.js
├─ +page.svelte
└─ dashboard/
   ├─ +layout.svelte
   ├─ +layout.js
   ├─ +page.svelte
   └─ reports/
      ├─ +page.svelte
      └─ [id]/
         └─ +page.svelte`, 'Route Files', 52),
        box('nested', '경로와 파일의 대응', 'Paths and Their Files',
          para('root_page', 'routes/+page.svelte → /', 'routes/+page.svelte → /') +
          para('dashboard_page', 'dashboard/+page.svelte → /dashboard', 'dashboard/+page.svelte → /dashboard') +
          para('report_page', 'reports/+page.svelte → /dashboard/reports', 'reports/+page.svelte → /dashboard/reports') +
          para('id_page', 'reports/[id]/+page.svelte → /dashboard/reports/42', 'reports/[id]/+page.svelte → /dashboard/reports/42') +
          note('layout_scope', '+layout.svelte: 해당 경로와 하위 페이지의 공통 UI · children을 렌더링해 페이지 표시', '+layout.svelte: shared UI for the route and descendants; render children to display the page') +
          para('parent', '하위 load에서 await parent()로 상위 레이아웃의 load 결과 재사용', 'A child load function can await parent() to reuse parent layout data'))) +
        note('optional', '모든 폴더에 +page·+layout이 필요한 것은 아님 · +layout.js는 공유 데이터가 필요할 때 추가', 'Not every directory needs a page or layout; add +layout.js when shared data is required'));
      break;
    case 26:
      slide(['상태·파생값·반응형 효과', 'State, Derived Values and Effects'],
        ['let·const 선언과 Svelte의 반응성 관련 runes', 'JavaScript declarations and Svelte reactivity runes'],
        grid(
          box('state', '$state · 변경되는 상태', '$state · Mutable State', para('state_body', '입력·토글·배열 변경을 화면에 반영', 'Input, toggle and array changes reflected in the UI') + sample('state', 'State.svelte', 44)),
          box('derived', '$derived · 계산된 값', '$derived · Computed Values', para('derived_body', '의존성이 바뀌면 무효화 · 값을 읽을 때 재계산', 'Invalidated when dependencies change; recomputed when read') + sample('derived', 'Total.svelte', 44)),
          box('effect', '$effect · 외부 동작 동기화', '$effect · External Synchronization', para('effect_body', '브라우저에서 최초 실행 · 동기적으로 읽은 반응형 의존성 변경 시 재실행', 'Runs initially in the browser and reruns when synchronously read reactive dependencies change') + sample('focus', 'Focus.svelte', 44))
        ) + note('effect_purpose', '표시용 파생값에는 $derived 사용 · $effect 안의 계산 자체가 금지되는 것은 아님', 'Use $derived for computed UI values; calculations inside an effect are not prohibited'));
      break;
    case 28:
      slide(['반복문과 목록 렌더링', 'Loops and List Rendering'],
        ['배열 항목을 반복 표시하고 각 항목의 상태를 갱신', 'Render array items and update each item’s state'],
        grid(box('each', '템플릿 반복 블록 · {#each}', 'Template Iteration · {#each}',
          list('each_points', [
            ['as todo: 항목 · as todo, i: 항목과 인덱스', 'as todo: item · as todo, i: item and index'],
            ['(todo.id): 항목을 추적하는 고유하고 안정적인 key', '(todo.id): a unique, stable key for tracking each item'],
            ['추가 버튼: 배열에 새 항목 삽입 → 목록 갱신', 'Add button: insert an item into the array → update the list'],
            ['bind:checked: 체크박스와 done을 연결', 'bind:checked: connects the checkbox and done']
          ]) + heading('js', '스크립트의 반복·계산', 'Iteration and Calculation in Scripts') +
          para('js_body', 'for·for…of·map·forEach 등 사용 가능 · 변경에 따라 UI를 갱신할 값에 반응형 상태·파생값 사용', 'Use for, for…of, map or forEach; use reactive state or derived values when changes should update the UI') +
          note('static', '고정 배열도 {#each}로 표시 가능 · 모든 UI 데이터에 runes가 필수인 것은 아님', 'A fixed array can also be rendered with {#each}; not every UI value requires runes')),
        sample('todos', 'Todos.svelte', 58)));
      break;
    case 29:
      slide(['이벤트와 처리 함수', 'Events and Handlers'],
        ['사용자 입력과 브라우저의 이벤트에 함수를 연결', 'Connect functions to user input and browser events'],
        grid(box('events', '이벤트 속성', 'Event Attributes',
          para('syntax', 'onclick={handler} · oninput={handler} · onmousemove={handler}', 'onclick={handler} · oninput={handler} · onmousemove={handler}') +
          list('event_points', [
            ['click: 클릭 · input: 입력 변화 · submit: 폼 제출', 'click: activation · input: value change · submit: form submission'],
            ['keydown: 키 입력 · mousemove: 마우스 이동', 'keydown: key press · mousemove: mouse movement'],
            ['event 객체로 입력 값·좌표 등 이벤트 정보 확인', 'Read values, coordinates and other details from the event object']
          ]) + note('window', 'svelte:window는 브라우저 창의 이벤트에 연결 · 해제 시 리스너 정리', 'svelte:window handles window events and cleans up listeners on teardown')),
        sample('mouse', 'Mouse.svelte', 58)) +
        flow('mouse_flow', [['마우스 이동', 'Mouse movement'], ['event.clientX / clientY', 'event.clientX / clientY'], ['m.x / m.y 갱신', 'Update m.x / m.y'], ['좌표 표시', 'Display coordinates']]) +
        note('coords', 'clientX·clientY는 뷰포트 기준 CSS 픽셀 좌표', 'clientX and clientY are viewport-relative coordinates in CSS pixels'));
      break;
    case 31: {
      const source = localized('navigation');
      const scriptParts = source.map(s => s.slice(0, s.indexOf('</script>') + 9));
      const markupParts = source.map(s => s.slice(s.indexOf('</script>') + 9).trim());
      slide(['훅과 페이지 탐색 제어', 'Hooks and Navigation Control'],
        ['정해진 실행 시점에 콜백을 등록해 동작 확장·제어', 'Register callbacks at defined points to extend or control behavior'],
        grid(plainCode('guard_script', scriptParts, 'src/routes/+layout.svelte · script', 58),
          box('hooks', '주요 실행 지점', 'Key Execution Points',
            para('life', 'onMount·onDestroy: 컴포넌트 생성 후·해제 시 리소스 관리', 'onMount and onDestroy: resource management on mount and teardown') +
            para('before', 'beforeNavigate: 탐색 전 검사·취소', 'beforeNavigate: inspect or cancel a navigation') +
            para('on', 'onNavigate: 탐색 전 실행 · 반환한 함수는 DOM 갱신 후 실행', 'onNavigate: runs before navigation; a returned function runs after the DOM update') +
            para('after', 'afterNavigate: 최초 마운트·탐색 완료 후 실행', 'afterNavigate: runs on initial mount and after navigation') +
            para('load', 'load: 페이지·레이아웃의 데이터 준비', 'load: prepares page or layout data') +
            plainCode('guard_markup', markupParts, 'src/routes/+layout.svelte · markup', 58))) +
        note('leave', '앱 내부 이동: confirm 결과로 취소 · 탭 닫기 등 leave 탐색: cancel()로 브라우저 기본 이탈 확인 요청', 'In-app navigation: cancel based on confirm; leave navigations such as closing the tab: cancel() requests the browser’s native confirmation'));
      break;
    }
    case 32:
      slide(['Props · 부모에서 자식으로 전달하는 값', 'Props · Values from Parent to Child'],
        ['컴포넌트의 입력값을 $props()로 받아 화면에 사용', 'Receive component inputs with $props() and use them in the UI'],
        grid(sample('Parent', 'Parent.svelte', 58), sample('Child', 'Child.svelte', 58)) +
        flow('prop_flow', [['부모의 message', 'Parent message'], ['<Child msg={message} />', '<Child msg={message} />'], ['$props()의 msg', 'msg from $props()'], ['자식의 문단 갱신', 'Child paragraph updates']]) +
        note('prop_rules', '부모의 값 변경은 자식에 반영 · props는 읽기 전용 입력으로 사용 · 자식에서 변경을 요청할 때 콜백 활용', 'Parent updates reach the child; treat props as read-only inputs and use callbacks to request changes'));
      break;
    case 34:
      slide(['컴포넌트와 UI 재사용', 'Components and UI Reuse'],
        ['마크업·동작·상태·스타일을 묶는 재사용 가능한 UI 단위', 'Reusable UI units combining markup, behavior, state and styles'],
        grid(sample('Card', 'src/lib/Card.svelte', 58), sample('Cards', 'src/routes/projects/+page.svelte', 58)) +
        grid(box('inputs', '입력과 합성', 'Inputs and Composition', para('inputs_body', '각 카드에 title·summary·href 전달 · 페이지에서 Card를 반복 사용', 'Pass title, summary and href to each card; compose the page from repeated Card instances')),
          box('value', '유지보수와 협업', 'Maintenance and Collaboration', para('value_body', '공통 UI의 변경 위치 통합 · 독립적 테스트·역할별 코드 관리', 'Centralized UI changes, isolated testing and clear code responsibilities'))) +
        note('data', 'data.projects는 페이지 load의 반환값 · 컴포넌트는 작은 버튼부터 큰 페이지까지 구성 가능', 'data.projects comes from the page load function; components can range from small buttons to entire pages'));
      break;
    case 37:
      slide(['Svelte Playground', 'Svelte Playground'], ['브라우저에서 컴포넌트 코드와 실행 결과 확인', 'Explore component code and its output in the browser'],
        `<div class="lesson-playground"><a href="https://svelte.dev/playground/" target="_blank" rel="noopener">svelte.dev/playground</a>${list('steps', [
          ['.svelte 컴포넌트의 script·마크업·style 입력', 'Enter the script, markup and style of a .svelte component'],
          ['상태·이벤트·바인딩을 바꾸며 출력과 비교', 'Change state, events and bindings and compare the output'],
          ['컴파일 오류·경고 메시지와 해당 코드 위치 확인', 'Inspect compiler errors, warnings and their locations']
        ], true)}</div>` +
        note('kit_limit', 'SvelteKit의 +page·+layout·API·$app 모듈 예제는 로컬 SvelteKit 프로젝트에서 실행', 'Run SvelteKit pages, layouts, APIs and $app module examples in a local SvelteKit project'));
      break;
    case 38:
      chapter(page.id, page.page, '06', ['웹 서비스 배포 자동화', 'Automating Web Service Deployment'], ['GitHub · 빌드·검증 · Vercel', 'GitHub · Build and Validation · Vercel']);
      break;
    case 39:
      slide(['CI/CD와 DevOps', 'CI/CD and DevOps'],
        ['코드 통합·검증·배포를 반복 가능한 과정으로 구성', 'A repeatable process for integration, validation and deployment'],
        grid(box('ci', 'CI · Continuous Integration', 'CI · Continuous Integration',
          para('ci_def', '작은 변경을 공유 코드에 자주 통합하고 자동 빌드·테스트로 검증', 'Frequently integrate small changes and validate them with automated builds and tests') +
          list('ci_goals', [['통합 오류와 회귀 문제의 조기 발견', 'Early detection of integration errors and regressions'], ['변경 검증·릴리스 준비 시간 단축', 'Faster validation and release preparation']])) ,
        box('cd', 'CD · Delivery / Deployment', 'CD · Delivery / Deployment',
          heading('delivery', 'Continuous Delivery', 'Continuous Delivery') + para('delivery_def', '변경을 항상 배포 가능한 상태로 준비 · 운영 배포에는 사람의 결정이 남을 수 있음', 'Keep changes ready for release; production deployment can retain a human decision') +
          heading('deployment', 'Continuous Deployment', 'Continuous Deployment') + para('deployment_def', '검증을 통과한 변경을 운영 환경까지 자동 배포', 'Automatically deploy validated changes to production')))+
        flow('pipeline', [['코드 변경', 'Code change'], ['빌드·테스트', 'Build and test'], ['배포 가능한 결과물', 'Releasable artifact'], ['운영 배포', 'Production deployment']]) +
        note('devops', 'DevOps: 개발과 운영의 협업·자동화·피드백 문화와 실천 · 특정 직무나 도구 하나로 한정되지 않음', 'DevOps: collaborative practices, automation and feedback across development and operations; not a single job title or tool'));
      break;
    case 40:
      slide(['Vercel', 'Vercel'], ['웹 애플리케이션의 빌드·미리보기·배포를 위한 클라우드 플랫폼', 'A cloud platform for building, previewing and deploying web applications'],
        grid(box('platform', '플랫폼과 프레임워크', 'Platform and Frameworks',
          para('next', 'Next.js 개발 · SvelteKit 등 여러 프레임워크 지원', 'Develops Next.js and supports frameworks including SvelteKit') +
          para('rich', '2021년 11월 Svelte 창시자 Rich Harris 합류 · Svelte 개발 지원', 'Svelte creator Rich Harris joined in November 2021 to work on Svelte') +
          note('support', '프레임워크 preset과 adapter가 빌드 결과를 배포 환경에 연결', 'The framework preset and adapter connect build output to the deployment platform')),
        box('features', '주요 기능', 'Key Features', list('features_list', [
          ['정적 파일 전송·CDN·서버 함수 실행', 'Static delivery, CDN caching and server functions'],
          ['Git 연동에 따른 자동 빌드·배포', 'Automatic builds and deployments from Git'],
          ['변경 사항별 Preview 배포 URL', 'Preview deployment URLs for changes'],
          ['HTTPS 인증서·사용자 도메인·관측 도구', 'HTTPS certificates, custom domains and observability tools']
        ]))) +
        note('tests', '자동 배포가 테스트의 자동 작성을 뜻하지는 않음 · 테스트 명령과 배포 조건은 프로젝트에 설정', 'Automatic deployment does not create tests; configure test commands and deployment conditions for the project'));
      break;
    case 41:
      slide(['Vercel 프로젝트 연결과 배포', 'Connecting and Deploying a Vercel Project'],
        ['GitHub 저장소를 연결하고 배포 결과와 후속 변경을 확인', 'Connect a GitHub repository and verify deployments and later changes'],
        grid(box('setup', '계정·저장소 연결', 'Account and Repository Connection',
          list('setup_steps', [
            ['Vercel 계정 생성·로그인', 'Create a Vercel account or sign in'],
            ['새 프로젝트에서 GitHub 연동과 저장소 권한 부여', 'Connect GitHub and grant repository access for a new project'],
            ['배포할 저장소 Import · 프로젝트 폴더 선택', 'Import the repository and select the project directory'],
            ['SvelteKit 프레임워크 자동 감지 확인', 'Confirm the detected SvelteKit framework preset']
          ], true)),
        box('deploy', '설정·검증·배포', 'Configuration, Validation and Deployment',
          list('deploy_steps', [
            ['Node.js 24.x · 필요한 환경 변수 설정', 'Set Node.js 24.x and any required environment variables'],
            ['Output Directory는 SvelteKit 자동 설정 유지', 'Keep the automatically configured SvelteKit output directory'],
            ['Deploy 실행 · 빌드 로그와 배포 URL 확인', 'Deploy and inspect the build log and deployment URL'],
            ['Home·About·Projects·상세·메모 동작 확인', 'Check Home, About, Projects, detail pages and notes']
          ], true))) +
        flow('push_flow', [['코드 변경·커밋', 'Change and commit'], ['GitHub에 push', 'Push to GitHub'], ['Vercel 재빌드', 'Vercel rebuild'], ['배포 결과 확인', 'Verify deployment']]) +
        note('url', '제출에는 대시보드의 실제 Production URL 사용 · 브랜치·설정에 따라 Preview와 Production 배포 구분', 'Submit the actual Production URL from the dashboard; branch and project settings determine Preview versus Production deployments'));
      break;
    case 42:
      chapter(page.id, page.page, '07', ['실습: SvelteKit을 이용한 웹사이트 제작과 Vercel 배포', 'Practice: Building a Website with SvelteKit and Deploying to Vercel'], null);
      break;
    case 43:
      // Preserve the instructor's assignment; only the deadline and translation differ from the source.
      slide(['실습 개요', 'Practice Overview'],
        ['SvelteKit을 이용한 웹사이트 제작과 Vercel 배포', 'Building a Website with SvelteKit and Deploying to Vercel'],
        grid(box('goals', '학습 목표', 'Learning Objectives',
          list('goals_items', [
            ['Node.js와 npm 환경 구축', 'Set up a Node.js and npm environment'],
            ['SvelteKit 프레임워크로 정적 사이트 제작', 'Build a static site with the SvelteKit framework'],
            ['Git/GitHub를 활용한 버전 관리', 'Manage versions with Git/GitHub'],
            ['Vercel을 통한 자동 배포 파이프라인 구축', 'Set up an automated deployment pipeline with Vercel']
          ]) + heading('requirements', '요구사항', 'Requirements') +
          list('requirements_items', [
            ['GitHub 저장소에 프로젝트 버전 관리가 바르게 되고 있는가?', 'Is the project properly version-controlled in a GitHub repository?'],
            ['Vercel에 GitHub 저장소가 연결되어 자동 배포가 이루어 지고 있는가?', 'Is the GitHub repository connected to Vercel for automatic deployment?'],
            ['Vercel 배포한 웹서비스에서 제시한 프로젝트 코드가 모두 바르게 동작하는가? (Home, About, Projects)', 'Does all the provided project code work correctly in the web service deployed to Vercel? (Home, About, Projects)']
          ]) + `<p>${t('span', key('reference'), '참고', 'Reference')}: <a href="https://github.com/ajou-hyunseok-oh/pwd-week2" target="_blank" rel="noopener">https://github.com/ajou-hyunseok-oh/pwd-week2</a></p>`),
        box('submit', '과제 마감일', 'Assignment Deadline',
          para('deadline_value', deadline.ko, deadline.en, 'lesson-deadline-value') +
          list('deliverables', [['GitHub 저장소 URL', 'GitHub repository URL'], ['Vercel App URL', 'Vercel App URL']]) +
          para('github_example', '(예: https://github.com/username/pwd-week2)', '(Example: https://github.com/username/pwd-week2)') +
          para('vercel_example', '(예: https://pwd-week2-[random].vercel.app)', '(Example: https://pwd-week2-[random].vercel.app)'))));
      break;
    case 44:
      chapter(page.id, page.page, 'Q&A', ['질의응답', 'Questions and Discussion'], ['웹 페이지 · 렌더링 · SvelteKit · 배포', 'Web Pages · Rendering · SvelteKit · Deployment']);
      break;
  }
  return true;
}

module.exports = { render, deadline };
