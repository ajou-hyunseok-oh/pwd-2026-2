// Corrected teaching examples, checked with the Svelte 5 compiler.
const examples = {
  counterJS: `<script>
  let name = $state('world');
  let count = $state(0);
</script>

<h1>Hello {name}!</h1>
<input aria-label="Name" bind:value={name} />
<button onclick={() => count += 1}>
  clicks: {count}
</button>

<style>
  h1 { color: #5b3df5; }
</style>`,
  counterTS: `<script lang="ts">
  let name: string = $state('world');
  let count: number = $state(0);
</script>

<h1>Hello {name}!</h1>
<input aria-label="Name" bind:value={name} />
<button onclick={() => count += 1}>
  clicks: {count}
</button>

<style>
  h1 { color: #5b3df5; }
</style>`,
  routeLoad: `export function load({ params }) {
  return { id: params.id };
}`,
  routePage: `<script>
  let { data } = $props();
</script>

<h1>Blog post #{data.id}</h1>`,
  grade: `<script>
  let score = $state(0);
  let grade = $derived.by(() => {
    if (score >= 90) return 'A';
    if (score >= 60) return 'B';
    return 'C';
  });
</script>

<input type="number" min="0" max="100"
  aria-label="Score" bind:value={score} />
{#if grade === 'A'}
  <p>Excellent! (A)</p>
{:else if grade === 'B'}
  <p>Good (B)</p>
{:else}
  <p>Keep practicing (C)</p>
{/if}`,
  lifecycle: `<script>
  import { onMount } from 'svelte';
  let count = $state(0);

  onMount(() => {
    const timer = setInterval(() => count++, 1000);
    return () => clearInterval(timer);
  });

  $effect.pre(() => {
    console.log('Before DOM update:', count);
  });
  $effect(() => {
    console.log('After DOM update:', count);
  });
</script>

<h1>{count}</h1>`,
  binding: `<script>
  let name = $state('');
  let agree = $state(false);
  let color = $state('red');
  let level = $state(50);
  let files = $state();
</script>

<label>Name: <input bind:value={name} /></label>
<p>{name || '(empty)'}</p>
<label>
  <input type="checkbox" bind:checked={agree} />
  I agree
</label>
<p>{agree ? 'Yes' : 'No'}</p>
<label>Color:
  <select bind:value={color}>
    <option>red</option><option>green</option>
    <option>blue</option>
  </select>
</label>
<p>{color}</p>
<label>Level: {level}
  <input type="range" min="0" max="100"
    bind:value={level} />
</label>
<label>Files:
  <input type="file" multiple bind:files={files} />
</label>
{#if files}<p>{files.length} files</p>{/if}`,
  api: `import { json } from '@sveltejs/kit';

const projects = [
  { slug: 'timetable',
    title: 'Timetable Helper',
    summary: 'Classes and schedules' },
  { slug: 'gallery',
    title: 'Image Gallery',
    summary: 'A small image gallery' },
  { slug: 'memo',
    title: 'Memo Pad',
    summary: 'Local notes' }
];

export function GET() {
  return json(projects);
}`,
  projectsLoad: `import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
  const res = await fetch('/api/projects');
  if (!res.ok) {
    error(res.status, 'Load failed');
  }
  return { projects: await res.json() };
}`,
  projectsPage: `<script>
  import Card from '$lib/Card.svelte';
  let { data } = $props();
</script>

<h2>Projects</h2>
{#each data.projects as p (p.slug)}
  <Card title={p.title}
    summary={p.summary}
    href={'/projects/' + p.slug} />
{:else}
  <p>No projects yet.</p>
{/each}`
};

function render(page,{add,t,p,grid,code}) {
  const supported=[20,21,22,24,27,30,33,35,36];
  if(!supported.includes(page.page))return false;
  const h=(key,ko,en)=>t('h3','sv_'+key,ko,en);
  const para=(key,ko,en,cls='')=>p('sv_'+key,ko,en,cls);
  const box=body=>`<section class="lesson-concept-box">${body}</section>`;
  const note=(key,ko,en)=>para(key,ko,en,'lesson-concept-note');
  const sample=(name,label,value=examples[name])=>code('sv_code_'+name,'text',value,label,[],58);
  const slide=(title,lead,body)=>add(page.id,page.page,title,lead,body);
  switch(page.page) {
    case 20:
      slide(['Svelte와 SvelteKit','Svelte and SvelteKit'],['HTML·CSS와 JavaScript 또는 TypeScript로 UI와 웹 애플리케이션 개발','Build UIs and web applications with HTML, CSS, and JavaScript or TypeScript'],
        grid(box(h('svelte','Svelte · UI 프레임워크','Svelte · UI Framework')+
          para('compiler','컴파일러가 컴포넌트를 브라우저에서 실행할 JavaScript·CSS로 변환','The compiler turns components into JavaScript and CSS for the browser')+
          para('dom','Virtual DOM 비교 대신 컴파일된 코드와 런타임으로 DOM 갱신','Compiled code and runtime update the DOM without Virtual DOM diffing')+
          para('ui','컴포넌트·반응형 상태·이벤트·스타일 제공','Provides components, reactive state, events and styles')+
          note('runtime','컴파일러 기반이어도 런타임 코드가 존재하며, 번들 크기와 성능은 앱에 따라 달라짐','Compiler-based does not mean runtime-free; bundle size and performance depend on the app')),
        box(h('kit','SvelteKit · 웹 애플리케이션 프레임워크','SvelteKit · Web Application Framework')+
          para('kit_features','파일 기반 라우팅·데이터 로드·서버 API·배포 기능 제공','Provides filesystem routing, data loading, server APIs and deployment support')+
          para('kit_render','SSR·사전 렌더링(SSG)·클라이언트 탐색 지원','Supports SSR, prerendering (SSG) and client-side navigation')+
          note('languages','Svelte와 SvelteKit 모두 JavaScript·TypeScript 지원 · TypeScript는 선택 사항','Both Svelte and SvelteKit support JavaScript and TypeScript; TypeScript is optional')))+
        grid(box(h('js','JavaScript','JavaScript')+'<code>&lt;script&gt; … &lt;/script&gt;</code>'+para('js_file','컴포넌트는 .svelte · 로드·API 파일은 .js','Components use .svelte; load and API files use .js')),
        box(h('ts','TypeScript','TypeScript')+'<code>&lt;script lang="ts"&gt; … &lt;/script&gt;</code>'+para('ts_file','컴포넌트는 동일하게 .svelte · 로드·API 파일은 .ts도 지원','Components still use .svelte; load and API files can use .ts'))));break;
    case 21:
      slide(['프론트엔드 UI 개발 방식 비교','Comparing Frontend UI Approaches'],['문법·반응성·DOM 갱신 방식의 차이','Differences in syntax, reactivity and DOM updates'],
        `<table class="lesson-table"><thead><tr><th>${t('span','sv_compare_dimension','비교 항목','Dimension')}</th><th>React</th><th>Vue</th><th>Svelte</th></tr></thead><tbody>${[
          ['syntax','UI 작성','UI syntax','JSX','Template / JSX','.svelte'],
          ['reactivity','상태·반응성','State / reactivity','useState / useReducer','ref / reactive','$state / $derived'],
          ['updates','DOM 갱신','DOM updates','렌더 결과 재조정','반응성·컴파일된 렌더 함수','컴파일된 갱신 코드'],
          ['language','개발 언어','Languages','JavaScript / TypeScript','JavaScript / TypeScript','JavaScript / TypeScript']
        ].map(([key,ko,en,...values])=>`<tr><th>${t('span','sv_compare_'+key,ko,en)}</th>${values.map((v,i)=>`<td>${t('span','sv_compare_'+key+i,v,key==='updates'?['Reconciliation','Reactivity and compiled render functions','Compiled update code'][i]:v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`+
        grid(box(h('size','번들 크기와 실행 성능','Bundle Size and Runtime Performance')+para('size_conditions','앱 기능·의존성·빌드 설정·측정 환경을 맞춰 비교해야 하며, 프레임워크 이름만으로 우열을 결정할 수 없음','Compare equivalent features, dependencies, build settings and environments; the framework name alone does not determine results')),
        box(h('choice','학습·유지보수 관점','Learning and Maintenance')+para('choice_conditions','팀의 언어·도구 경험, 필요한 라이브러리, 문서와 장기 유지보수 요구를 함께 고려','Consider the team’s experience, required libraries, documentation and long-term maintenance needs'))));break;
    case 22:
      slide(['Svelte 파일 구조와 개발 언어','Svelte File Structure and Languages'],['같은 .svelte 컴포넌트를 JavaScript 또는 TypeScript로 작성','Write the same .svelte component in JavaScript or TypeScript'],
        grid(sample('counterJS','Counter.svelte · JavaScript'),sample('counterTS','Counter.svelte · TypeScript'))+
        para('file_parts','script: 상태·함수 · 마크업: 화면 구조 · style: 컴포넌트 범위 CSS','script: state and functions · markup: UI structure · style: component-scoped CSS')+
        note('module','공유 모듈 코드는 <script module>에 작성하며 모듈 평가 시 실행 · onclick에는 두 언어 모두 함수를 전달','Shared module code belongs in <script module> and runs when the module is evaluated; both languages pass a function to onclick')+
        para('ts_scope','Svelte 5는 타입 표기·interface를 지원하며, enum 등 실행 코드가 필요한 TS 문법에는 전처리 설정 필요','Svelte 5 supports type annotations and interfaces; TS features that generate code, such as enums, require preprocessing','lesson-caption'));break;
    case 24:
      slide(['파일 기반 라우팅','Filesystem Routing'],['정적 경로는 폴더명으로, 동적 경로는 [매개변수]로 정의','Use directory names for static paths and [parameters] for dynamic paths'],
        para('static_route','src/routes/about/+page.svelte → /about','src/routes/about/+page.svelte → /about','lesson-devtools-shortcut')+
        grid(sample('routeLoad','src/routes/blog/[id]/+page.js'),sample('routePage','src/routes/blog/[id]/+page.svelte'))+
        `<div class="lesson-concept-flow"><div><code>/blog/42</code></div><span>→</span><div><code>params.id = "42"</code></div><span>→</span><div><code>return { id: params.id }</code></div><span>→</span><div><code>data.id = "42"</code></div></div>`+
        note('route_data','[id]는 경로 매개변수를 정의 · data는 load 반환값으로 전달되므로 params와 data를 구분','[id] defines a path parameter; data contains load results, so params and data are distinct')+
        para('nested_path','중첩 경로: src/routes/dashboard/reports/[id]/+page.svelte → /dashboard/reports/42','Nested route: src/routes/dashboard/reports/[id]/+page.svelte → /dashboard/reports/42'));break;
    case 27:
      slide(['조건문','Conditions'],['상태에서 등급을 계산하고, 등급에 맞는 UI를 선택','Derive a grade from state and select the corresponding UI'],
        grid(sample('grade','Grade.svelte'),box(h('derived','계산된 값 · $derived.by','Derived Value · $derived.by')+
          para('grade_flow','score 변경 → grade 재계산 → 조건에 맞는 문단 표시','score changes → grade is recalculated → matching paragraph is displayed')+
          para('derived_pure','if / else로 값을 계산하고 반환 · 다른 상태를 변경하지 않는 순수 계산','Use if / else to return a value without changing other state')+
          h('if','템플릿 조건 블록','Template Conditions')+para('if_syntax','{#if} · {:else if} · {:else}로 화면 분기','Use {#if}, {:else if} and {:else} to select UI')+
          note('no_effect','다른 상태로부터 계산할 수 있는 값은 $derived 사용 · $effect는 DOM·외부 시스템과의 동기화 등에 사용','Use $derived for values computed from state; use $effect for synchronization with the DOM or external systems'))));break;
    case 30:
      slide(['라이프사이클과 반응형 효과','Lifecycle and Reactive Effects'],['마운트·해제 시 리소스를 관리하고 DOM 갱신 전후의 작업을 구분','Manage resources on mount and teardown; distinguish work before and after DOM updates'],
        grid(sample('lifecycle','Timer.svelte'),box(h('mount','onMount · 마운트 이후','onMount · After Mount')+
          para('mount_note','브라우저에서 마운트 후 실행 · SSR에서는 실행되지 않음','Runs after mounting in the browser, not during SSR')+
          para('cleanup','동기 onMount 콜백이 반환한 함수는 해제 시 실행 → 타이머 정리','A function returned by a synchronous onMount callback runs on teardown to clear the timer')+
          h('effects','$effect.pre / $effect','$effect.pre / $effect')+
          para('effects_note','브라우저에서 최초 실행 후, 동기적으로 읽은 반응형 의존성이 변경되면 재실행','Run initially in the browser, then rerun when synchronously read reactive dependencies change')+
          para('effects_timing','$effect.pre: DOM 갱신 전 · $effect: DOM 갱신 후',' $effect.pre: before DOM updates · $effect: after DOM updates')+
          note('destroy','onDestroy도 해제 작업 등록에 사용 가능하며 SSR에서도 실행 · count는 $state로 선언해야 화면과 효과가 변경을 추적','onDestroy also registers teardown and runs during SSR; declare count with $state so the UI and effects track changes'))));break;
    case 33: {
      const split=examples.binding.indexOf('<label>Color:');
      slide(['양방향 바인딩','Two-way Binding'],['입력이 상태를 변경하고, 상태 변경이 연결된 입력과 화면에 반영','Input updates state, and state changes update the bound input and UI'],
        grid(sample('binding_start','Bindings.svelte · script / name / checkbox',examples.binding.slice(0,split).trimEnd()),sample('binding_end','Bindings.svelte · select / range / files',examples.binding.slice(split)))+
        note('binding_runes','Svelte 5 runes 모드: 변경되는 값은 $state · value는 입력값, checked는 체크 여부, files는 FileList와 연결','Svelte 5 runes mode: use $state for changing values; value binds the input value, checked the check state, and files a FileList'));
      break;
    }
    case 35:
      slide(['API 라우트와 요청 처리','API Routes and Request Handling'],['+server.js의 HTTP 메서드 함수가 요청을 처리하고 Response를 반환','HTTP method functions in +server.js handle requests and return a Response'],
        `<div class="lesson-concept-flow"><div><code>GET /api/projects</code></div><span>→</span><div><code>src/routes/api/projects/+server.js</code></div><span>→</span><div><code>export function GET()</code></div></div>`+
        grid(box(h('server','서버 전용 실행','Server-only Execution')+para('server_only','+server.js 코드는 브라우저 번들에 포함되지 않음 · DB·비밀키는 서버에서 사용','+server.js is not included in the browser bundle; access databases and secrets on the server')+note('secrets','응답으로 반환한 데이터는 클라이언트에 전달되므로 인증·권한 확인과 비밀정보 제외는 별도로 구현','Returned data reaches the client; implement authorization and exclude secrets from responses')+
          h('method','메서드와 응답','Methods and Responses')+para('method_response','GET·POST 등 메서드명으로 함수 export · Response 또는 json(data) 반환 · error(status, message)는 예외 발생','Export GET, POST or other method handlers; return Response or json(data); error(status, message) throws')),
        box(h('context','요청 컨텍스트','Request Context')+para('request_context','request: 요청 · url: URL·쿼리 · params: 경로 매개변수 · cookies: 쿠키','request: request · url: URL and query · params: path parameters · cookies: cookies')+para('locals','locals: 인증 사용자 등 요청별로 공유하는 서버 측 정보','locals: server-side information shared within a request, such as the authenticated user')+
          h('load_kind','페이지 데이터 로드','Page Data Loading')+para('load_kind_detail','+page.js: 서버·브라우저에서 실행 가능한 universal load\n+page.server.js: 서버에서만 실행되는 load','+page.js: universal load that can run on server and browser\n+page.server.js: server-only load'))));break;
    case 36:
      slide(['API 응답과 페이지 데이터','API Responses and Page Data'],['API 응답을 load에서 받아 페이지 컴포넌트에 전달','Fetch the API response in load and pass its data to the page component'],
        grid(sample('api','src/routes/api/projects/+server.js'),sample('projectsLoad','src/routes/projects/+page.js'),sample('projectsPage','src/routes/projects/+page.svelte'))+
        `<div class="lesson-concept-flow"><div><code>GET /api/projects</code></div><span>→</span><div><code>load → { projects }</code></div><span>→</span><div><code>data.projects → Card</code></div></div>`+
        note('api_card','Card는 앞서 정의한 src/lib/Card.svelte를 재사용 · API 처리, 데이터 로드, 화면 마크업은 서로 다른 파일','Reuse src/lib/Card.svelte from the component example; API handling, data loading and UI markup belong in different files'));break;
  }
  return true;
}
module.exports={render,examples};
