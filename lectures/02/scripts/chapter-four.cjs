// Original PDF page 14, split into its three topics.
module.exports=({add,t,p,grid})=>{
  const h=(key,ko,en)=>t('h3',key,ko,en);
  const box=body=>`<section class="lesson-concept-box">${body}</section>`;
  const steps=items=>`<ol class="lesson-navigation-flow">${items.map(([key,ko,en])=>t('li',key,ko,en)).join('')}</ol>`;
  const line=(key,ko,en)=>p(key,ko,en,'lesson-concept-note');
  add('devtools-elements',14,['문서 요소와 메타데이터','Document Elements and Metadata'],
    ['Elements 패널에서 현재 DOM의 구조·속성과 요소에 적용된 스타일 확인','Inspect the current DOM structure, attributes and element styles in the Elements panel'],
    p('c4_open','Chrome 개발자 도구 열기 · Windows: F12 / Ctrl+Shift+I · macOS: ⌥⌘I','Open Chrome DevTools · Windows: F12 / Ctrl+Shift+I · macOS: ⌥⌘I','lesson-devtools-shortcut')+
    grid(box(h('c4_elements_steps','Elements에서 확인','Inspect in Elements')+steps([
      ['c4_inspect','화면의 요소를 우클릭 → 검사(Inspect)','Right-click an element → Inspect'],
      ['c4_dom','선택된 DOM 노드의 태그·속성·부모와 자식 확인','Read the selected node’s tag, attributes, parents and children'],
      ['c4_semantic','header · nav · main · footer의 문서 역할 확인','Check the document roles of header, nav, main and footer'],
      ['c4_styles','Styles: 적용 규칙 · Computed: 계산된 스타일 확인','Styles: CSS rules · Computed: computed styles']
    ])+line('c4_live_dom','Elements는 JavaScript 변경이 반영된 현재 DOM을 표시한다. 서버가 보낸 HTML과 다를 수 있다.','Elements shows the current DOM, including JavaScript changes; it can differ from the HTML response.')),
    box(h('c4_dom_map','문서 구조와 확인 위치','Document Structure and Inspection Targets')+
      `<div class="lesson-devtools-tree"><code>html</code><section><code>head</code>${p('c4_head','title → 문서 제목\nmeta[name="description"] → 페이지 설명\nmeta[name="viewport"] → 모바일 뷰포트 설정','title → document title\nmeta[name="description"] → page description\nmeta[name="viewport"] → mobile viewport settings')}</section><section><code>body</code>${p('c4_body','header · nav → 소개·탐색 영역\nmain → 주요 콘텐츠\nfooter → 문서 관련 정보','header · nav → introduction and navigation\nmain → main content\nfooter → document information')}</section></div>`+
      line('c4_metadata','head를 펼쳐 title·meta의 내용을 확인한다. 요소의 존재만으로 검색 노출이나 순위가 보장되지는 않는다.','Expand head to read title and meta values; their presence alone does not guarantee search visibility or ranking.'))));

  const viewport=(width,kind)=>`<figure class="lesson-viewport-example"><figcaption>${width} CSS px</figcaption><img src="./materials/figures/ko-devtools-viewport-${kind}.png" data-lesson-image="devtools-viewport-${kind}" width="${width}" height="660" alt="${kind==='mobile'?tAlt('c4_mobile_alt','390 CSS px에서 표시한 자기소개 페이지','Portfolio page at a viewport width of 390 CSS pixels'):tAlt('c4_tablet_alt','820 CSS px에서 표시한 자기소개 페이지','Portfolio page at a viewport width of 820 CSS pixels')}" data-wd-i18n-alt="${kind==='mobile'?'c4_mobile_alt':'c4_tablet_alt'}" /></figure>`;
  // Register alt translations through the same helper as visible text.
  function tAlt(key,ko,en){return t('span',key,ko,en).replace(/^<span[^>]*>/,'').replace(/<\/span>$/,'');}
  add('devtools-viewport',14,['반응형 레이아웃과 뷰포트','Responsive Layout and Viewport'],
    ['Device Toolbar에서 뷰포트의 너비·높이를 바꾸며 배치와 넘침 확인','Use the Device Toolbar to change viewport dimensions and inspect layout and overflow'],
    p('c4_device_toggle','개발자 도구에서 Device Toolbar 전환 · Windows: Ctrl+Shift+M · macOS: ⇧⌘M','Toggle Device Toolbar in DevTools · Windows: Ctrl+Shift+M · macOS: ⇧⌘M','lesson-devtools-shortcut')+
    grid(box(h('c4_device_steps','뷰포트별 확인','Inspect at Different Viewports')+steps([
      ['c4_responsive','Dimensions에서 Responsive 또는 기기 프리셋 선택','Choose Responsive or a device preset under Dimensions'],
      ['c4_dimensions','너비·높이 변경 · 회전 버튼으로 세로/가로 전환','Change width and height; rotate between portrait and landscape'],
      ['c4_wrap','메뉴·문단의 줄바꿈과 이미지 크기 확인','Check menu and paragraph wrapping and image sizing'],
      ['c4_overflow','가로 스크롤·콘텐츠 잘림·요소 겹침 확인','Check horizontal scrolling, clipped content and overlap']
    ])+line('c4_css_pixels','너비·높이는 CSS 픽셀 기준이다. 실제 기기의 물리 픽셀 해상도와 구분한다.','Dimensions are in CSS pixels, not the physical pixel resolution of a device.')+line('c4_device_limit','Device Mode는 화면과 입력 환경의 시뮬레이션이다. 실제 모바일 브라우저에서도 확인이 필요하다.','Device Mode simulates display and input conditions; real mobile browsers also need testing.')),
    `<div class="lesson-viewport-examples">${viewport(390,'mobile')}${viewport(820,'tablet')}${p('c4_viewport_caption','같은 자기소개 페이지 · 뷰포트 너비 390 / 820 CSS px','The same portfolio page at viewport widths of 390 / 820 CSS pixels','lesson-caption')}</div>`));

  add('devtools-network',14,['원본 HTML과 응답 헤더','HTML Response and Response Headers'],
    ['Network 패널에서 문서 요청을 선택해 응답의 형식과 HTML 본문 확인','Select the document request in Network to inspect its response type and HTML body'],
    p('c4_network_path','Network → 페이지 새로고침 → Doc 필터 → 현재 페이지 URL의 문서 요청 선택','Network → reload the page → Doc filter → select the document request for the current page URL','lesson-devtools-shortcut')+
    grid(box(h('c4_headers','Headers · 응답 정보','Headers · Response Information')+
      `<div class="lesson-response-fields"><div><b>General</b><code>Request URL<br>Status Code</code></div><div><b>Response Headers</b><code>Content-Type: text/html; charset=utf-8</code></div></div>`+
      p('c4_headers_example','HTML 응답 헤더의 예시','Example HTML response header','lesson-caption')+steps([
      ['c4_request_url','Request URL: 확인하려는 문서의 주소인지 확인','Request URL: check that this is the intended document'],
      ['c4_status','Status Code: 응답 상태 확인 (예: 200 OK)','Status Code: inspect the response status (for example, 200 OK)'],
      ['c4_content_type','Content-Type: text/html은 HTML 형식, charset=utf-8은 문자 인코딩 선언','Content-Type: text/html declares HTML; charset=utf-8 declares the text encoding']
    ])+line('c4_charset','charset이 헤더에 없을 수도 있다. HTML의 meta charset 등 인코딩 선언도 함께 확인한다.','charset may be absent from the header; also inspect encoding declarations such as meta charset in the HTML.')),
    box(h('c4_response','Response · HTML 본문','Response · HTML Body')+
      `<div class="lesson-concept-flow"><div>Response${p('c4_response_html','응답으로 받은 HTML','HTML received in the response')}</div><span aria-hidden="true">→</span><div>Elements${p('c4_response_dom','파싱·변경 후 현재 DOM','Current DOM after parsing and changes')}</div></div>`+steps([
      ['c4_response_tab','Response 탭에서 문서 응답의 HTML 확인','Open Response to inspect the document’s HTML body'],
      ['c4_response_content','title·meta·본문 콘텐츠가 응답에 포함되는지 확인','Check whether title, meta and main content are in the response'],
      ['c4_response_compare','Elements와 비교해 응답 HTML과 현재 DOM의 차이 확인','Compare with Elements to distinguish response HTML from current DOM']
    ])+line('c4_doc_select','Doc 목록의 첫 항목으로 단정하지 않고 URL로 선택한다. 클라이언트 라우팅은 새 문서 요청 없이 동작할 수 있다.','Select by URL, not simply the first Doc entry; client-side navigation may not request a new document.'))));
};
