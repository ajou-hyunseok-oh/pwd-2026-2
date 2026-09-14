// Approved technical corrections to original PDF pages 8, 12 and 13.
module.exports = ({add,t,p,grid}) => {
  const heading=(key,ko,en)=>t('h3',key,ko,en);
  const box=(body)=>`<section class="lesson-concept-box">${body}</section>`;
  const flow=(items)=>`<div class="lesson-concept-flow">${items.map((item,i)=>(i?'<span aria-hidden="true">→</span>':'')+`<div>${item}</div>`).join('')}</div>`;
  const text=(key,ko,en)=>t('span',key,ko,en);
  add('original-semantic-html',8,['시맨틱 HTML','Semantic HTML'],
    ['콘텐츠의 의미와 역할에 맞는 HTML 요소로 문서 구조를 표현하는 방식','Expressing document structure with HTML elements that match the meaning and role of content'],
    grid(box(heading('c3_sem_structure','요소가 전달하는 문서의 역할','Document roles expressed by elements')+
      `<div class="lesson-semantic-map">${[
        ['header','문서·구역의 소개','Introduction to a document or section'],
        ['nav','주요 탐색 링크','Major navigation links'],
        ['main','페이지의 주요 콘텐츠','The page’s main content'],
        ['article','독립적으로 이해할 수 있는 콘텐츠','Self-contained content'],
        ['aside','주변 콘텐츠에 부수적으로 관련된 내용','Content tangentially related to its surroundings'],
        ['footer','문서·구역의 작성자·저작권 등','Authorship, copyright and related section information']
      ].map(([tag,ko,en])=>`<div><code>&lt;${tag}&gt;</code>${text('c3_tag_'+tag,ko,en)}</div>`).join('')}</div>`+
      p('c3_div','div는 의미가 정해지지 않은 컨테이너다. class="nav"만으로 탐색 영역의 의미가 생기지는 않는다.','div is a generic container. class="nav" alone does not give it navigation semantics.','lesson-concept-note')),
    box(heading('c3_search_understanding','검색엔진의 콘텐츠 이해','How Search Engines Understand Content')+
      p('c3_search_semantics','검색엔진은 콘텐츠와 HTML 구조를 분석하며, 의미에 맞는 요소는 문서의 역할을 전달하는 데 도움을 준다.','Search engines analyze content and HTML structure; appropriate elements help communicate document roles.')+
      flow([text('c3_crawl','크롤링\n페이지 수집','Crawling\nDiscover and fetch'),text('c3_index','인덱싱\n분석·색인 저장','Indexing\nAnalyze and store'),text('c3_rank','검색 요청\n결과 선택·순위 결정','Search query\nSelect and rank results')])+
      heading('c3_ax_title','접근성 트리','Accessibility Tree')+
      p('c3_ax_definition','브라우저가 DOM과 CSS·ARIA 정보를 바탕으로 요소의 역할·이름·상태 등을 구성해 보조 기술에 제공하는 트리','A tree built by the browser from DOM, CSS and ARIA information, exposing roles, names and states to assistive technologies')+
      p('c3_ax_effect','콘텐츠에 맞는 요소 사용 → 문서 영역 탐색 지원 · 코드의 의미와 가독성 개선','Appropriate elements support document navigation and make code easier to understand.','lesson-concept-note')))+
    `<div class="lesson-optimization-glossary">${[
      ['seo','SEO','Search Engine Optimization','검색엔진이 콘텐츠를 발견·이해해 관련 검색 결과에 제공할 수 있도록 개선하는 과정.','Improving content so search engines can discover, understand and present it for relevant searches.'],
      ['aeo','AEO','Answer Engine Optimization','질문에 직접 답하는 검색·응답 시스템이 콘텐츠를 답변으로 활용하기 쉽도록 정리하는 과정.','Organizing content so search and answer systems can use it to answer questions directly.'],
      ['geo','GEO','Generative Engine Optimization','생성형 AI의 답변에서 콘텐츠가 활용·인용될 수 있도록 내용과 구조를 개선하는 과정.','Improving content and structure so generative AI can use and cite it in answers.']
    ].map(([key,abbr,full,ko,en])=>`<section><h3>${abbr} <small>${full}</small></h3>${p('c3_glossary_'+key,ko,en)}</section>`).join('')}</div>`);

  add('original-routing-url',12,['라우팅과 URL 구조','Routing and URL Structure'],
    ['라우팅은 URL 경로에 맞는 페이지나 요청 처리 코드를 선택하는 과정','Routing selects a page or request handler for a URL path'],
    `<div class="lesson-url-parts"><div><code>https</code>${text('c3_scheme','스킴','Scheme')}</div><b>://</b><div><code>example.com</code>${text('c3_host','호스트','Host')}</div><div class="lesson-url-parts__path"><code>/blog/2024/first-post</code>${text('c3_path','경로 전체 (path)','Full path')}</div><div><code>?sort=date</code>${text('c3_query','쿼리 · sort의 값은 date','Query · sort = date')}</div><div><code>#comments</code>${text('c3_fragment','프래그먼트','Fragment')}</div></div>`+
    grid(box(heading('c3_segments_title','경로 세그먼트와 라우트 매개변수','Path Segments and Route Parameters')+
      p('c3_segments','blog · 2024 · first-post는 각각 /로 구분된 경로 세그먼트','blog, 2024 and first-post are path segments separated by /')+
      `<div class="lesson-route-example"><div>${text('c3_pattern','라우트 정의','Route pattern')}<code>/blog/[year]/[slug]</code></div><span aria-hidden="true">↓</span><div>${text('c3_actual','실제 경로','Actual path')}<code>/blog/2024/first-post</code></div><div><code>year = "2024"<br>slug = "first-post"</code></div></div>`+
      p('c3_dynamic','[year]·[slug]처럼 매개변수로 정의한 부분이 동적 세그먼트다. URL의 값만 보고 동적 여부를 판단할 수는 없다.','Segments are dynamic when declared as parameters such as [year] and [slug]. Actual URL values alone do not establish this.','lesson-concept-note')),
    box(heading('c3_url_route_title','URL에 맞는 페이지 선택','Selecting a Page for a URL')+
      flow(['<code>/about</code>',text('c3_match','라우터\n경로 매칭','Router\nMatch path'),text('c3_about','About\n페이지','About\npage')])+
      heading('c3_fragment_title','쿼리와 프래그먼트','Query and Fragment')+
      p('c3_query_detail','?sort=date: 요청에 포함되는 쿼리. 정렬 등 추가 조건을 전달하는 데 사용할 수 있다.','?sort=date: a query included in the request, usable for additional conditions such as sorting.')+
      p('c3_fragment_detail','#comments: 예를 들어 id="comments"인 요소로 이동한다. 프래그먼트는 HTTP 요청에 포함되지 않으며 브라우저에서 처리한다.','#comments: can navigate to an element with id="comments". The fragment is processed in the browser and is not sent in the HTTP request.'))));

  const step=(key,ko,en)=>`<li>${text(key,ko,en)}</li>`;
  add('original-routing-types',13,['서버 라우팅과 클라이언트 라우팅','Server and Client Routing'],
    ['페이지 이동 시 새 HTML 문서를 로드하거나, 기존 문서를 유지하며 화면을 전환','Navigation can load a new HTML document or update a view within the existing document'],
    grid(box(heading('c3_mpa','새 문서로 이동 · 전형적인 MPA','New-document Navigation · Typical MPA')+
      `<ol class="lesson-navigation-flow">${step('c3_mpa1','링크 선택 → /about 요청','Select link → request /about')}${step('c3_mpa2','서버가 경로에 맞는 HTML 응답 제공','Server returns the HTML response for the path')}${step('c3_mpa3','브라우저가 새 문서를 로드하여 표시','Browser loads and displays a new document')}${step('c3_mpa4','브라우저가 URL·방문 기록 관리','Browser manages the URL and session history')}</ol>`+
      p('c3_mpa_note','HTML은 정적 파일이거나 서버가 생성한 결과일 수 있다. 새 문서 탐색이 항상 깜빡임이나 느린 전환을 뜻하지 않는다.','HTML may be a static file or generated by the server. A new document does not necessarily mean flicker or slow navigation.','lesson-concept-note')),
    box(heading('c3_spa','기존 문서에서 전환 · SPA 방식','Same-document Navigation · SPA Style')+
      `<ol class="lesson-navigation-flow">${step('c3_spa1','링크 선택 → 클라이언트 라우터가 경로 처리','Select link → client router handles the path')}${step('c3_spa2','필요한 데이터·코드 준비 (기존 자료 재사용 가능)','Prepare data and code (reuse what is already available)')}${step('c3_spa3','기존 문서에서 해당 화면으로 전환','Update the view within the existing document')}${step('c3_spa4','라우터가 URL·방문 기록 갱신 및 뒤로 가기 처리','Router updates URL/history and handles back navigation')}</ol>`+
      p('c3_spa_note','SPA는 하나의 HTML 문서를 유지하며 여러 URL의 화면을 전환한다. JSON 요청은 매번 필요한 조건이 아님.','A SPA keeps one HTML document while navigating between views at multiple URLs. JSON requests are not required for every transition.','lesson-concept-note')))+
    `<div class="lesson-routing-factors">${box(heading('c3_rendering','렌더링과의 관계','Relation to Rendering')+p('c3_rendering_detail','SSR·CSR은 콘텐츠 생성 위치의 구분이다. 첫 요청은 SSR, 이후 이동은 클라이언트 라우팅으로 조합할 수 있다.','SSR/CSR describe where content is generated. Initial SSR can be combined with later client-side navigation.'))}${box(heading('c3_speed','속도','Speed')+p('c3_speed_detail','문서·UI 재사용은 빠른 전환에 유리하다. 실제 속도는 JavaScript 양·데이터 요청·캐시 등에 따라 달라진다.','Reusing the document and UI can help. Actual speed depends on JavaScript, data requests, caching and more.'))}${box(heading('c3_search','SEO','SEO')+p('c3_search_detail','라우팅 방식만으로 결정되지 않는다. 각 URL의 콘텐츠·링크·메타데이터를 검색엔진이 읽을 수 있어야 한다.','Routing alone does not determine SEO. Search engines must be able to access content, links and metadata for each URL.'))}</div>`);
};
