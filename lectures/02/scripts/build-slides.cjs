const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const prettier = require('../../../packages/web-deck/node_modules/prettier');
const formatOptions = require('../../../packages/web-deck/code-format.json');
const observation = JSON.parse(fs.readFileSync(path.join(root,'materials/figures/observations.json'),'utf8'));
const original = fs.readFileSync(path.join(root,'index.html'),'utf8');
const context = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'lecture-content.js'),'utf8'),context);
const messages = {ko:{},en:{}};
const sources = [];
const slideMap = [];
const slides = [];
const escape = value => String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
function tr(key, ko, en=ko) { messages.ko[key]=ko;messages.en[key]=en;return escape(ko); }
function t(tag,key,ko,en=ko,cls='') {return `<${tag}${cls?` class="${cls}"`:''} data-wd-i18n="${key}">${tr(key,ko,en)}</${tag}>`;}
const p=(key,ko,en,cls='')=>t('p',key,ko,en,cls);
const tag=(n)=>`<b class="lesson-tag lesson-tag--${n}" aria-hidden="true">${n}</b>`;
const arrow=()=>'<span class="lesson-arrow" aria-hidden="true">→</span>';
const grid=(...body)=>`<div class="lesson-grid${body.length===3?' lesson-grid--three':''}">${body.map(b=>`<div class="lesson-col">${b}</div>`).join('')}</div>`;
const panel=(key,ko,en,body,n)=>`<section class="lesson-panel">${n?tag(n):''}${t('h3',key,ko,en)}${body}</section>`;
const takeaway=(key,ko,en)=>p(key,ko,en,'lesson-takeaway');
function pair(file){const slash=file.indexOf('/');return [file, ['portfolio','rendering','generation','routing'].includes(file.slice(0,slash))?file.slice(0,slash+1)+'en/'+file.slice(slash+1):file];}
function source(file, start, end) {
  const text=fs.readFileSync(path.join(root,'examples',file),'utf8');
  if(!start)return text.trimEnd();
  const a=text.indexOf(start);
  if(a<0)throw new Error('Source start missing: '+file+' '+start);
  const b=end?text.indexOf(end,a)+end.length:text.length;
  if(end&&b<end.length)throw new Error('Source end missing: '+file+' '+end);
  const snippet=text.slice(a,b).trimEnd();
  sources.push({file,start,end:end||null,snippet});
  return snippet;
}
function localizedSource(file,start,end) {return pair(file).map(f=>source(f,start,end));}
function code(key,lang,values,label,marks=[],width=64) {
  if(typeof values==='string')values=[values,values];
  const markAttr=marks.length?` data-lesson-marks="${escape(JSON.stringify(marks))}"`:'';
  return `<div class="lesson-code"><div class="lesson-code__label">${escape(label)}</div><div class="lesson-code__body"><pre class="wd-code" data-wd-code="${lang}" data-wd-code-width="${width}" data-wd-i18n="${key}"${markAttr}>${tr(key,...values)}</pre></div></div>`;
}
function image(key,name,ko,en,cls='') {
  return `<figure class="lesson-shot ${cls}"><img src="./materials/figures/ko-${name}.png" data-lesson-image="${name}" alt="${tr(key+'_alt',ko,en)}" data-wd-i18n-alt="${key}_alt" loading="eager"/>${t('figcaption',key,ko,en)}</figure>`;
}
function commonImage(key,name,ko,en,cls='') {return `<figure class="lesson-shot ${cls}"><img src="./materials/figures/${name}.png" alt="${tr(key+'_alt',ko,en)}" data-wd-i18n-alt="${key}_alt" loading="eager"/>${t('figcaption',key,ko,en)}</figure>`;}
function link(file,ko,en,key='v2_live') { const [a,b]=pair(file);return `<a href="./examples/${a}" data-lesson-href-ko="./examples/${a}" data-lesson-href-en="./examples/${b}" target="_blank" rel="noopener" data-wd-i18n="${key}">${tr(key,ko,en)}</a>`; }
function add(id,old,title,lead,body,refs=[],example,appendix=false) {
  slideMap.push({number:slides.length+8,id,previous:old,title:title[0],appendix});
  slides.push(`<section class="wd-slide wd-slide--content week2-slide lesson-slide" data-wd-slide="${id}"${appendix?' data-wd-appendix':''} role="region">${t('h2','v2_'+id+'_title',...title,'wd-slide-heading')}${lead?p('v2_'+id+'_lead',...lead,'wd-slide-lead'):''}${body}</section>`);
}
function chapter(id,old,number,title,lead){slideMap.push({number:slides.length+8,id,previous:old,title:title[0],appendix:false});slides.push(`<section class="wd-slide week2-section week2-slide" data-wd-slide="${id}" role="region"><p class="week2-section__number">${number}</p>${t('h2','v2_'+id+'_title',...title)}${lead?p('v2_'+id+'_lead',...lead,'week2-section__lead'):''}</section>`);}
function node(n,label,detail='',cls='') {return `<div class="lesson-node ${cls}">${n?tag(n):''}<code>${escape(label)}</code>${detail?`<small>${escape(detail)}</small>`:''}</div>`;}
function domTree(key,{hidden=false,render=false}={}) {
  return `<div class="lesson-tree"><div>${node(0,render?'main box':'main')}</div><div class="lesson-tree__stem"></div><div>${node(1,render?'section box':'section')}</div><div class="lesson-tree__branches"><div>${node(0,render?'h1 box':'h1')}${t('p',key+'_h1','자기소개','About Me','lesson-tree__text')}</div><div class="${hidden?'lesson-excluded':''}">${node(2,render?'p box':'p','id="intro"')}${t('p',key+'_text',render?'웹 개발 학습 중':'#text: 웹 개발 학습 중',render?'Learning web development.':'#text: Learning web development.','lesson-tree__text')}</div><div>${node(3,render?'button box':'button','id="change"')}${t('p',key+'_button',render?'소개 바꾸기':'#text: 소개 바꾸기',render?'Change Introduction':'#text: Change Introduction','lesson-tree__text')}</div></div></div>`;
}
const domRef=[['https://www.w3schools.com/jsref/dom_obj_document.asp','W3Schools · DOM']];
const renderRef=[['https://web.dev/articles/rendering-performance','web.dev · Rendering']];
function paintLayers() {
  return `<div class="lesson-paint-stack"><div class="lesson-paint-stack__back"><span>#f0f3ef</span></div><div class="lesson-paint-stack__front">${t('strong','v2_layer_heading','자기소개','About Me')}${t('span','v2_layer_text','웹 개발 학습 중','Learning web development.')}${t('b','v2_layer_button','소개 바꾸기','Change Introduction')}</div></div>`;
}
function recordedEvents(change) {
  return ['UpdateLayoutTree','Layout','Paint'].map(name=>{
    const event=observation.locales.ko.rendering.find(event=>event.change===change&&event.name===name);
    return node(0,name,event?`${event.durationMs.toFixed(3)} ms`:'—');
  }).join('');
}

chapter('browser-rendering',8,'02',['웹 브라우저의 렌더링 원리','Web Browser Rendering Principles'],['코드의 요소·규칙이 문서 모델과 화면으로 바뀌는 과정','From source elements and style rules to document models and the screen']);
// Original Week 2 PDF, page 9: retain its five steps and embedded diagram.
add('source-to-screen',9,['웹 브라우저 렌더링 과정','Web Browser Rendering Process'],null,
  `<div class="lesson-browser-rendering"><ol class="lesson-browser-rendering__steps">${t('li','v2_render_html','HTML 파싱 → DOM 트리','HTML parsing → DOM tree')}${t('li','v2_render_css','CSS 파싱 → CSSOM 트리','CSS parsing → CSSOM tree')}${t('li','v2_render_tree','DOM + CSSOM → Render Tree','DOM + CSSOM → Render Tree')}${t('li','v2_render_layout','Layout (위치, 크기 계산)','Layout (position and size calculation)')}${t('li','v2_render_paint','Paint (픽셀로 그리기)','Paint (drawing pixels)')}</ol><figure class="lesson-browser-rendering__diagram"><img src="./materials/figures/browser-rendering-original.jpeg" width="1700" height="712" alt="${tr('v2_render_diagram_alt','HTML → DOM, CSS → CSSOM, JavaScript의 DOM·CSSOM 변경, DOM·CSSOM → Render Tree → Layout → Paint','HTML → DOM, CSS → CSSOM, JavaScript modifying DOM and CSSOM, DOM and CSSOM → Render Tree → Layout → Paint')}" data-wd-i18n-alt="v2_render_diagram_alt" loading="eager"/></figure></div>`);

add('dom-nodes',10,['DOM (Document Object Model)','DOM (Document Object Model)'],['HTML 문서를 객체 트리로 표현하고, 프로그램이 문서의 구조와 내용을 읽고 변경할 수 있게 하는 인터페이스','An interface representing an HTML document as an object tree, allowing programs to read and modify its structure and content'],
  grid(code('v2_dom_html','html',localizedSource('portfolio/about.html','<section class="profile">','</section>'),'portfolio/about.html · section',[[1,'<section'],[2,'id="intro"'],[3,'id="change"']],64),
    domTree('v2_dom'))+
  `<div class="lesson-inline-result">${tag(2)}${t('span','v2_dom_target','p#intro가 화면의 소개 문단에 대응','p#intro corresponds to the introduction paragraph')}${image('v2_dom_visible','intro-before','화면의 문단','Visible paragraph','lesson-shot--tiny')}</div>`,domRef,'portfolio/about.html');

const cssomColorRules = [['body','color'],['button','background'],['button:hover','background']].map(([selector,property])=>{
  const rule=source('portfolio/style.css',selector+' {','}');
  const declaration=rule.split('\n').find(line=>line.trimStart().startsWith(property+':'));
  if(!declaration)throw new Error('Missing CSSOM example declaration: '+selector+' '+property);
  return `${selector} {\n${declaration}\n}`;
}).join('\n');
add('css-rule-objects',11,['CSSOM (CSS Object Model)','CSSOM (CSS Object Model)'],['CSS 스타일시트와 규칙을 객체로 표현하고, 프로그램이 이를 읽고 변경할 수 있게 하는 인터페이스','An interface representing CSS stylesheets and rules as objects that programs can read and modify'],
  grid(code('v2_css_rules','css',cssomColorRules,'portfolio/style.css · color declarations',[[1,'body {'],[2,'button {'],[3,'button:hover {']],56),
    `<div class="lesson-cssom-rules">${p('v2_css_sheet','CSSOM · style.css','CSSOM · style.css','lesson-label')}${p('v2_css_rule_fields','선택자와 선언(속성·값)으로 구성된 규칙 객체','Rule objects containing a selector and declarations (properties and values)','lesson-caption')}${node(1,'body','color: #333')}${node(2,'button','background: #1f6b4a')}${node(3,'button:hover','background: #174f37')}</div>`)+
  `<div class="lesson-css-concepts"><section>${t('h3','v2_css_matching_title','매칭 (Matching)','Matching')}${p('v2_css_matching_definition','선택자 조건을 만족하는 요소를 찾는 과정','Finding elements that satisfy a selector’s conditions')}${p('v2_css_matching_example','마우스를 올린 버튼 → button · button:hover 모두 해당','A hovered button matches both button and button:hover','lesson-css-concepts__example')}</section><section>${t('h3','v2_css_cascade_title','캐스케이드 (Cascade)','Cascade')}${p('v2_css_cascade_definition','같은 요소·속성에 겹치는 선언 중 우선순위로 적용값 결정','Choosing a declaration by priority when several target the same property on the same element')}${p('v2_css_cascade_example','이 예제에서는 더 구체적인 button:hover의 배경색 #174f37 적용','Here, the more specific button:hover sets the background to #174f37','lesson-css-concepts__example')}</section><section>${t('h3','v2_css_inheritance_title','상속 (Inheritance)','Inheritance')}${p('v2_css_inheritance_definition','color처럼 상속되는 속성에 선언이 없으면 부모 요소의 값 사용','Using the parent’s value when an inherited property such as color has no declaration')}${p('v2_css_inheritance_example','color를 지정하지 않은 p → body의 글자색 #333 상속','p has no color declaration → inherits #333 through its parents from body','lesson-css-concepts__example')}</section></div>`);

const renderTreeStyles = [['.profile',['background']],['h1',['font-size']],['button',['background','color']]].map(([selector,properties])=>{
  const rule=source('portfolio/style.css',selector+' {','}');
  return properties.map(property=>{
    const line=rule.split('\n').find(line=>line.trimStart().startsWith(property+':'));
    if(!line)throw new Error('Missing render-tree style: '+selector+' '+property);
    return line.trim().replace(/;$/,'');
  }).join(' · ');
});
function renderExampleTree(styled) {
  return `<div class="lesson-render-branch">${node(1,'section.profile',styled?renderTreeStyles[0]:'')}<ul><li>${node(2,'h1',styled?renderTreeStyles[1]:'')}${p('v2_render_heading_text','자기소개','About Me','lesson-render-branch__text')}</li><li>${node(3,'p#intro')}${p('v2_render_paragraph_text','웹 개발 학습 중','Learning web development.','lesson-render-branch__text')}</li><li>${node(4,'button#change',styled?renderTreeStyles[2]:'')}${p('v2_render_button_text','소개 바꾸기','Change Introduction','lesson-render-branch__text')}</li></ul></div>`;
}
add('rendering-box-tree',12,['렌더 트리 (Render Tree)','Render Tree'],['DOM의 요소에 CSSOM의 스타일을 반영해, 화면에 그릴 대상을 구성한 트리','A tree of rendering objects built from DOM elements and their CSSOM styles'],
  `<div class="lesson-render-flow"><section>${t('h3','v2_render_dom_title','DOM · 요소와 내용','DOM · Elements and Content')}${renderExampleTree(false)}</section><span class="lesson-render-flow__operator" aria-hidden="true">+</span><section>${t('h3','v2_render_cssom_title','CSSOM · 스타일 규칙','CSSOM · Style Rules')}<div class="lesson-render-rules">${node(0,'style.css')}${node(1,'.profile',renderTreeStyles[0])}${node(2,'h1',renderTreeStyles[1])}${node(4,'button',renderTreeStyles[2])}</div></section><span class="lesson-render-flow__operator" aria-hidden="true">→</span><section class="lesson-render-flow__result">${t('h3','v2_render_result_title','Render Tree','Render Tree')}${renderExampleTree(true)}</section></div>`+
  p('v2_render_scope','portfolio/about.html · portfolio/style.css — 자기소개 영역의 주요 요소·스타일','portfolio/about.html · portfolio/style.css — selected elements and styles from the profile section','lesson-caption'));

function layoutDrawing(){const m=observation.locales.ko.layout;return `<div class="lesson-dimensions"><div class="lesson-dimensions__width">① width: ${m.width}px</div><div class="lesson-dimensions__box"><div class="lesson-dimensions__padding">② padding: 24px</div><div class="lesson-dimensions__content">${t('strong','v2_layout_heading','자기소개','About Me')}${p('v2_layout_text','나의 첫 웹사이트 제작 중','Building my first website.')}<div class="lesson-dimensions__button">③ button · x: 24px<br>y: <span data-lesson-measure="buttonY">${m.button.y.toFixed(1)}</span>px</div></div><div class="lesson-dimensions__inner">content: ${m.contentWidth}px</div></div></div>`;}
add('layout-geometry',13,['레이아웃: 위치와 크기 계산','Layout: Position and Size'],['CSS 값이 실제 박스의 치수와 자식 요소의 위치를 결정','CSS values determine box dimensions and child positions'],
  grid(code('v2_layout_css','css',source('rendering/style.css','* {','}')+'\n\n'+source('rendering/style.css','.profile {','}'),'rendering/style.css',[[1,'width: 360px'],[2,'padding: 24px']],56)+p('v2_layout_measure','실측: 카드 안의 버튼 위치 · 좌표 원점은 카드의 왼쪽 위','Measured button position · origin at the card’s top-left corner','lesson-caption'),layoutDrawing())+
  takeaway('v2_layout_equation','border-box · 360 − 24 − 24 = 콘텐츠 폭 312px · 테두리 없음','border-box · 360 − 24 − 24 = 312px content width · no border'),renderRef,'rendering/index.html');

add('paint-composite',13,['페인트','Paint'],['레이아웃에서 계산한 위치와 크기에 따라 요소의 배경·글자·테두리를 그리는 과정','Drawing element backgrounds, text, and borders using the positions and sizes calculated during layout'],
  grid(code('v2_paint_css','css','.profile {\n  background: #f0f3ef;\n}\n\nbutton {\n  background: #1f6b4a;\n  color: white;\n}','portfolio/style.css · relevant declarations',[[1,'background: #f0f3ef'],[2,'background: #1f6b4a'],[3,'color: white']],40),
    image('v2_paint_screen','intro-before','① 카드 배경 · ② 버튼 배경 · ③ 버튼 글자','① Card background · ② Button background · ③ Button text')+
    `<div class="lesson-layers">${paintLayers()}${arrow()}<div>${t('span','v2_paint_frame','합성된 최종 화면','Composited frame')}</div></div>`)+
  takeaway('v2_paint_note','레이어 경계는 DOM 태그와 1:1 관계가 아님 · 아래 레이어 표현은 개념도','Layer boundaries do not map one-to-one to DOM tags · the layer illustration is conceptual'),renderRef,'portfolio/about.html');

// Keep the approved order; all teaching content now has native KO/EN text.
const originalPages = JSON.parse(fs.readFileSync(path.join(root,'materials/figures/original-slides.json'),'utf8'));
for (const page of originalPages) {
  if (page.id === 'original-semantic-html') {
    slideMap.push({number:slides.length+8,id:'routing-semantic-html',previous:null,title:'시맨틱 HTML과 라우팅',appendix:false});
    slides.push(`<section class="wd-slide week2-section week2-slide" data-wd-slide="routing-semantic-html" role="region"><p class="week2-section__number">03</p>${t('h2','v2_routing-semantic-html_title','시맨틱 HTML과 라우팅','Semantic HTML and Routing')}</section>`);
    require('./chapter-three.cjs')({add,t,p,grid});
    break;
  }
  if(!require('./complete-slides.cjs').render(page,{add,t,p,grid,code,chapter}))throw new Error('Missing bilingual slide: '+page.id);
}

slideMap.push({number:slides.length+8,id:'browser-devtools',previous:null,title:'웹 브라우저 개발자 도구',appendix:false});
slides.push(`<section class="wd-slide week2-section week2-slide week2-devtools-chapter" data-wd-slide="browser-devtools" role="region"><div><p class="week2-section__number">04</p>${t('h2','c4_chapter_title','웹 브라우저 개발자 도구','Web Browser Developer Tools')}</div><img src="./materials/figures/devtools-original.jpeg" data-lesson-src-ko="./materials/figures/devtools-original.jpeg" data-lesson-src-en="./materials/figures/en-devtools-elements.png" alt="Chrome DevTools: Elements and Styles" loading="eager" /></section>`);
require('./chapter-four.cjs')({add,t,p,grid});

// Corrected bilingual continuation, retaining the original subject order.
for (const page of JSON.parse(fs.readFileSync(path.join(root,'materials/figures/framework-slides.json'),'utf8'))) {
  if(require('./svelte-corrections.cjs').render(page,{add,t,p,grid,code}))continue;
  if(!require('./complete-slides.cjs').render(page,{add,t,p,grid,code,chapter}))throw new Error('Missing bilingual slide: '+page.id);
}

(async()=>{
  const boundary=original.search(/\s*<section[^>]*data-wd-slide="browser-rendering"/);
  if(boundary<0)throw new Error('Slide 08 boundary missing');
  let prefix=original.slice(0,boundary);
  if(!prefix.includes('./lesson.css'))prefix=prefix.replace('</head>','  <link rel="stylesheet" href="./lesson.css" />\n  </head>');
  const ending='\n        </div>\n      </div>\n    </main>'+original.slice(original.lastIndexOf('</main>')+7);
  for(const match of prefix.matchAll(/data-wd-i18n(?:-alt|-title|-aria-label)?="([^"]+)"/g)) {
    for(const locale of ['ko','en']) if(context.window.LECTURE_CONTENT[locale][match[1]]!==undefined) messages[locale][match[1]]=context.window.LECTURE_CONTENT[locale][match[1]];
  }
  for(const key of ['s47_preview_after','s47_preview_reset'])for(const locale of ['ko','en'])messages[locale][key]=context.window.LECTURE_CONTENT[locale][key];
  const html=await prettier.format(prefix+'\n'+slides.join('\n')+ending,{parser:'html',printWidth:120,tabWidth:2});
  fs.writeFileSync(path.join(root,'index.html'),html);
  const quote=s=>"'"+s.replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\r/g,'\\r').replace(/\n/g,'\\n')+"'";
  let content='window.LECTURE_CONTENT = {\n';
  for(const locale of ['ko','en'])content+=`  ${locale}: {\n`+Object.entries(messages[locale]).map(([key,value])=>`    ${/^[a-zA-Z0-9_]+$/.test(key)?key:quote(key)}: ${quote(value)}`).join(',\n')+'\n  }'+(locale==='ko'?',':'')+'\n';
  fs.writeFileSync(path.join(root,'lecture-content.js'),content+'};\n');
  fs.writeFileSync(path.join(root,'materials/figures/code-sources.json'),JSON.stringify(sources,null,2)+'\n');
  fs.writeFileSync(path.join(root,'materials/figures/slide-map.json'),JSON.stringify(slideMap,null,2)+'\n');
  console.log(`Built ${slides.length+7} slides: ${slides.filter(s=>!s.includes('data-wd-appendix')).length+7} main + ${slides.filter(s=>s.includes('data-wd-appendix')).length} appendix.`);
})().catch(error=>{console.error(error);process.exitCode=1;});
