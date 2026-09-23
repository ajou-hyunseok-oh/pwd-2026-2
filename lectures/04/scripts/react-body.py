"""Bilingual content for the 19 React topics in the 24-slide deck."""
from pathlib import Path
import json, re, textwrap
ROOT=Path(__file__).resolve().parents[1]
def p(s):
    parts=s.split('||'); return parts if len(parts)==2 else [s,s]
def prose(s):
    # Enumerations in reviewed explanation fields; code, URLs, and quotations use p().
    return [re.sub(r'[ \t]*·[ \t]*',' · ',value) for value in p(s)]
def points(title,*items): return dict(type='points',title=prose(title),items=[prose(x) for x in items])
def table(title,heads,*rows,widths=None):
    block=dict(type='table',title=prose(title),heads=[prose(x) for x in heads],rows=[[prose(x) for x in r] for r in rows])
    if widths: block['widths']=widths
    return block
def quote(title,text): return dict(type='quote',title=p(title),text=p(text))
def code(title,text,language='bash',caption=None,width=None,explanation=None):
    block=dict(type='code',title=p(title),text=p(text),language=language)
    if caption: block['caption']=p(caption)
    if width: block['width']=width
    if explanation: block['explanation']=explanation['sections']
    return block
def example(name):
    source=(ROOT/'scripts/comparison-examples.jsx').read_text()
    match=re.search(r'^[ \t]*// \[lesson:'+name+r'\]\n(.*?)^[ \t]*// \[/lesson:'+name+r'\]',source,re.M|re.S)
    return textwrap.dedent(match[1]).strip()
def demo(mode): return dict(type='demo',mode=mode)
def concepts(*sections):
    return dict(type='concepts',sections=[dict(definition=prose(t),details=[prose(x) for x in details]) for t,*details in sections])
def figure(src,alt,caption): return dict(type='figure',src=src,alt=p(alt),caption=p(caption))
slides=[]
def add(*blocks,refs=(),layout='stack',note=''):
    slides.append(dict(blocks=blocks,refs=refs,layout=layout,note=note))
# 03 · Establish the subject before introducing a problem or an example.
add(
    concepts(
        ('React - 데이터를 화면으로 표현하는 UI 라이브러리||React - A UI library for presenting data',)),
    table('웹 서비스 안에서의 위치||Its Place in a Web Service', ['구성||Part','담당 역할||Responsibility'],
        ['React','화면 구성 · 사용자 동작에 따른 UI 갱신||UI composition · Updates following user actions'],
        ['HTML · CSS · 브라우저||HTML · CSS · Browser','문서 구조 · 스타일 · 실제 화면 표시||Document structure · Styling · Display'],
        ['서버 · 데이터베이스||Server · Database','요청 처리 · 공유 데이터 저장||Request processing · Shared data storage']),
    refs=('R10','R16'),
    note='React는 UI 라이브러리. React 기반 프레임워크와 React 자체의 범위를 구분. 라우팅·서버·빌드 도구 상세는 생략.')
# 04 · Source PDF p.5: the problem that shifted UI design toward data.
add(
    table('웹 UI 개발 방식의 확장||Expanding Approaches to Web UI', ['방식||Approach','개발의 중심||Development Focus'],
        ['HTML · CSS','문서 구조와 스타일로 콘텐츠 표현||Content expressed through document structure and styling'],
        ['JavaScript · jQuery','DOM 요소 선택 · 이벤트 연결 · 화면 직접 수정||DOM selection · Event handling · Direct UI updates'],
        ['React의 컴포넌트||React Components','현재 데이터에 맞는 UI 정의와 조합||UI definition and composition for current data']),
    concepts(
        ('UI 관리 - 데이터와 DOM의 일치 유지||UI Management - Keeping data and DOM in sync',
         '이벤트별 갱신 코드의 분산 → 관리 부담 증가||Scattered update logic → Greater maintenance effort'),
        ('React의 접근(2013) - 컴포넌트 중심의 UI 구성||React’s Approach (2013) - UI composition with components',
         '화면 구조와 표시 로직의 결합||UI structure and display logic in the same component',
         '데이터 변화에 따른 갱신 계산||Updates calculated as data changes')),
    refs=('P05','R01','J01'),
    note='원본 PDF 5쪽의 웹 개발 변화·jQuery 관리 부담·React 접근을 재구성. 세 방식이 교체되는 엄밀한 1·2·3세대 구분이 아니라 공존하는 개발 관점. jQuery 자체가 상태 불일치나 성능 저하를 필연적으로 유발한다는 주장 제외.')
# 05 · A real, dated company screenshot.
add(
    figure('materials/images/facebook-2020-light.png',
        'Facebook.com의 탐색·스토리·피드·설정 화면||Facebook.com navigation, stories, feed, and settings',
        'Facebook.com · 2020년 기술 회고의 화면||Facebook.com · Image from the 2020 engineering report'),
    concepts(
        ('화면 영역 - 역할별 UI 구성||UI Areas - Composition by role',
         '왼쪽 - 탐색||Left - Navigation',
         '가운데 - 스토리 · 피드||Center - Stories · Feed',
         '오른쪽 - 설정 메뉴||Right - Settings'),
        ('React 적용 - 영역 조합과 상호작용||React’s Role - Composition and interaction',
         '사용자 동작에 반응하는 웹 UI||Web UI responding to user actions'),
        ('기술 구성 - UI와 기반 구조의 재설계||System - UI and infrastructure redesign',
         'React · Relay · CSS',
         '데이터 · 탐색 구조||Data · Navigation structure')),
    refs=('R07',),
    layout='visual',
    note='원문 이미지: https://engineering.fb.com/wp-content/uploads/2020/05/1.-Home-Setting-Light-Mode.png\nMeta의 2020-05-08 기술 회고. 현재 Facebook 화면으로 표기하지 않음. 로딩 개선을 React 단독 효과로 해석하지 않음.')
# 06
add(table('주요 전환점||Key Milestones',['시기||Date','변화||Change','의미||Significance'],['2013.05','React 공개||React released publicly','Facebook에서 발전한 UI 도구의 공개||Public release of the UI tool developed at Facebook'],['2019.02','React 16.8 · Hooks 도입||React 16.8 · Hooks introduced','함수 중심 작성 방식의 확대||Broader use of function-based components'],['2023.03','react.dev 학습 문서 공개||New react.dev learning docs','함수 컴포넌트 중심의 학습 체계||Learning organized around function components'],['2024.12','React 19 정식 출시||React 19 released','UI와 데이터 처리 기능의 확장||Expanded UI and data-handling features']),points('학습의 기준||Learning Focus','작성 문법의 변화에도 이어지는 컴포넌트·데이터·화면의 관계||Components, data, and UI across changes in syntax'),refs=('R02','R03','R04'),note='전환점을 고른 연혁이며 최신 버전 목록이 아님. Hooks API·클래스 문법 해설 제외.')
# 07
add(
    table('2025 Stack Overflow · 전문 개발자||2025 Stack Overflow · Professional Developers',
        ['선택 기술||Selected Technology','지난 1년 사용 경험||Used in the Past Year'],
        ['React','46.9%'], ['jQuery','24.1%'], ['Angular','19.8%'], ['Vue.js','18.4%'], ['Svelte','6.9%']),
    concepts(
        ('조사 범위 - 문항 응답자의 기술 사용 경험||Survey Scope - Technology use among respondents',
         '해당 문항 응답자 19,460명||19,460 responses to this question',
         '여러 기술 선택 가능||Multiple selections allowed',
         '전체 웹사이트 점유율 · 품질 순위와 구분||Distinct from website market share or quality rankings')),
    refs=('P04','R05','R06'),
    note='공식 HTML Professional Developers / Have Used 탭. 선택 기술 5개만 비교. 2025년 조사로 명시.')
# 09–12 · The same complete product UI and data throughout.
add(
    demo('components'),
    concepts(
        ('컴포넌트 - 역할을 가진 UI 단위||Component - A UI unit with a role',
         '검색 영역 · 결과 목록 · 상품 행으로 구성||Search area · Results · Product rows'),
        ('SearchBar - 검색 조건 입력||SearchBar - Search criteria input',
         '상품명 입력 · 재고 조건 선택||Product-name input · Stock selection'),
        ('ProductTable - 결과 목록 표시||ProductTable - Results display',
         '분류별 상품 · 검색 결과 개수||Products by category · Result count'),
        ('ProductRow - 상품 한 행의 표현||ProductRow - A single product row',
         '상품명 · 가격 · 재고 여부||Name · Price · Stock status')),
    refs=('R10',),
    layout='split',
    note='공식 Thinking in React의 6개 상품을 한글화. 원본 분류/가격/재고를 유지하고 수업용 결과 개수·재고 문구 추가. 장에서 실제 React로 전체 화면을 렌더. 버튼으로 컴포넌트 경계를 표시. 컴포넌트 분리의 유일한 정답을 주장하지 않음.')
add(
    demo('reuse'),
    concepts(
        ('컴포넌트 재사용 - 같은 UI 정의에 다른 데이터 적용||Component Reuse - One UI definition with different data',
         '사과 $1 · 용과 $1 · 패션프루트 $2||Apple $1 · Dragonfruit $1 · Passionfruit $2'),
        ('공통 표현 규칙 - 모든 상품 행의 표시 방식||Shared Rules - Presentation of every product row',
         '상품명 - 왼쪽||Name - Left',
         '가격 - 오른쪽||Price - Right',
         '품절 - 색상 · 문구로 구분||Out of stock - Color · Text'),
        ('일관성 - 같은 표시 규칙을 모든 행에 반영||Consistency - Shared rules across all rows',
         '표시 규칙 수정 → 모든 상품 행에 반영||Row rule change → All product rows updated')),
    refs=('R10',),
    layout='split',
    note='09번과 같은 상품 화면·데이터. 다른 서비스나 미제시 화면을 새로 가정하지 않음. Props 문법은 다루지 않음.')
add(demo('filter'),refs=('R10',),note='왼쪽 전체 6개와 오른쪽 재고 있는 4개를 동시 표시. 오른쪽 검색창·재고 필터 조작 가능. 이름/가격/재고 원본은 동일하며 결과 개수는 필터 결과에서 계산. Print에서도 두 화면 보존.')
# 12 · Definitions before application: the two approaches, then their UI responsibilities.
add(
    concepts(
        ('명령형 - 작업의 순서와 방법을 직접 지정||Imperative - Explicit steps and operations',
         'UI 개발 - 변경할 DOM 요소와 수정 명령 지정||UI development - DOM targets and update commands',
         '요소 선택 · 이벤트 처리 · 텍스트와 속성 수정||Element selection · Events · Text and attribute updates')),
    concepts(
        ('선언형 - 원하는 결과의 조건이나 형태를 정의||Declarative - Conditions or form of the desired result',
         'React - 현재 상태에 맞는 UI 선언||React - UI declared for the current state',
         '상태 변경 → UI 재계산 → 필요한 DOM 변경 반영||State change → UI recalculation → Required DOM updates')),
    refs=('P06','R01','R10'),
    layout='split',
    note='11번은 화면의 변화를 관찰하는 장, 12번은 명령형/선언형의 뜻과 UI 개발의 책임을 정의하는 장, 13번은 코드/실행으로 그 차이를 확인하는 장. 명령형/선언형은 일반적인 프로그래밍 접근이고 jQuery/React는 여기서 비교하는 UI 구현 사례. 단방향 데이터 흐름은 선언형의 정의와 구분되는 별도 개념으로 본 장의 정의에 섞지 않음.')

# 13 · Source PDF p.6, corrected and executed with real jQuery and React.
add(
    demo('programming'),
    code('명령형(jQuery)||Imperative (jQuery)', example('jquery'), 'javascript', width=64,
        explanation=concepts(
            ('DOM 갱신 - 수정 순서의 직접 지정||DOM Updates - Explicit update steps',
             '버튼 생성 → 이벤트 연결 → 텍스트 수정||Button creation → Event handling → Text updates',
             'host - 버튼을 추가할 DOM 요소||host - The DOM element receiving the button'))),
    code('선언형(React)||Declarative (React)', example('react'), 'jsx', width=64,
        explanation=concepts(
            ('JSX - JavaScript 안의 UI 표현||JSX - UI expressed within JavaScript',
             '현재 count에 맞는 버튼 UI 선언||Button UI declared for the current count'),
            ('useState(0) - 상태 초기값 0||useState(0) - Initial state value 0',
             'setCount → 상태 변경 → React의 버튼 텍스트 갱신||setCount → State change → React updates the button text'))),
    layout='programming',
    refs=('P06','J02','J03','R18'),
    note='PDF 6쪽의 동일 클릭 카운터 비교를 재사용. 기존 명령형 코드는 jQuery가 아닌 일반 DOM API이며 parseInt(\'Click me\')에서 NaN 발생. 실제 jQuery 코드와 별도 숫자 변수로 교정. 양쪽 count=0에서 시작, 클릭마다 1 증가. 위 버튼은 아래 표시 코드와 같은 모듈을 실행. 전제: jQuery의 $와 React의 useState import, host는 jQuery 출력 DOM 영역, React는 Counter를 마운트. Hooks/JSX는 읽는 데 필요한 뜻만 설명하며 실습·API 상세 수업으로 확장하지 않음.')
# 14 · Expansion only after the core concepts have been introduced.
add(quote('Shopify · 2025년 기술 회고||Shopify · 2025 Engineering Retrospective','iOS·Android에서 반복되는 개발을 줄이기 위한 React Native 활용||React Native to reduce duplicated development across iOS and Android'),table('공유하는 관점과 달라지는 대상||Shared Concepts and Different Targets',['관점||Aspect','웹 · React + React DOM||Web · React + React DOM','모바일 · React Native||Mobile · React Native'],['설계 방식||Design','컴포넌트 조합·데이터에 따른 UI||Component composition and data-driven UI','컴포넌트 조합·데이터에 따른 UI||Component composition and data-driven UI'],['표시 대상||Render target','브라우저의 DOM||Browser DOM','플랫폼의 네이티브 UI||Platform-native UI'],['플랫폼 연결||Platform integration','웹 API와 HTML 요소||Web APIs and HTML elements','기기 기능·플랫폼별 처리||Device features and platform-specific behavior']),refs=('R08',),note='Shopify 자체 회고를 도입 맥락으로 사용. 웹 HTML/CSS 코드를 변경 없이 모바일에서 실행한다는 의미가 아님. 생산성 수치로 일반화하지 않음.')
# 15–17 · Concrete correspondence, one process, one live observation.
add(demo('dom'),refs=('P07','R13','R19'),note='상품 검색 결과의 일부를 화면·DOM·메모리 UI 표현으로 대응. UI 구조는 강의용 축약이며 React 내부 객체의 실제 필드 형식이 아님. 원본 PDF 7쪽의 JavaScript 객체로 표현하는 UI 트리 설명을 보강. Virtual DOM은 별도 브라우저 화면이나 실제 DOM 전체의 복제본이 아님.')
add(demo('commit'),refs=('P07','R13'),note='같은 상품 데이터의 이전 UI와 새 UI에서 6→4와 품절 행 제거를 표시. Trigger → Render(컴포넌트 실행·새 UI 계산/비교) → Commit(DOM 반영) → Browser(필요한 스타일·레이아웃·페인트) 구분. 원본의 Commit과 레이아웃/페인트 혼합을 교정. 비교는 Render 작업의 일부로 설명. 모든 렌더가 DOM 변경을 일으키거나 Virtual DOM이 항상 더 빠르다는 주장 제외.')
add(
    demo('clock'),
    concepts(
        ('UI 재계산 - 새 시간 데이터에 맞는 화면 계산||UI Recalculation - UI calculated from new time data',
         '1초마다 바뀌는 시간||Time updated every second'),
        ('DOM 반영 - 변경된 시간 텍스트의 갱신||DOM Updates - Changes to the time text',
         '동일한 입력 요소 유지||The same input element retained'),
        ('입력 보존 - 작성 중인 내용과 위치의 유지||Input Preservation - Retained text and editing position',
         '문자열 · 포커스 · 커서 위치 유지||Typed text · Focus · Caret position')),
    refs=('R13',),
    layout='split',
    note='실제 React 컴포넌트가 1초마다 다시 렌더. 입력창은 uncontrolled input이며 동일 위치의 동일 DOM 노드 유지. 강사는 입력 후 시계 갱신과 커서 유지를 관찰. key·재마운트·상태 초기화 API 해설 제외.')
# 19 · Source PDF p.8: actual updates instead of a blanket speed ranking.
add(
    demo('dom-updates'),
    table('같은 결과에 도달하는 서로 다른 책임||Different Responsibilities for the Same Result',
        ['관점||Aspect','jQuery','React'],
        ['갱신 지시||Update logic','개발자가 button.text(...) 호출||Developer calls button.text(...)','개발자는 UI 정의 · React가 DOM 변경 계산||Developer defines UI · React calculates DOM changes'],
        ['이 버튼의 변경||Observed changes','버튼 노드 유지 · 안의 텍스트 교체||Button retained · Its text replaced','버튼 노드 유지 · 숫자 텍스트 갱신||Button retained · Number text updated'], widths='16% 38% 46%'),
    concepts(
        ('갱신 비용 - 화면 갱신에 필요한 작업량||Update Cost - The work needed to update the screen',
         'UI 계산 · 비교 · DOM 변경 · 브라우저의 레이아웃 · 페인트||UI calculation · Comparison · DOM changes · Browser layout · Paint'),
        ('VDOM - UI 갱신을 관리하는 방법||VDOM - A way to manage UI updates',
         '실제 속도 - 구현과 측정으로 판단||Actual speed - Judged through implementation and measurement')),
    refs=('P08','J02','R13'),
    note='PDF 8쪽의 직접 DOM 조작 vs VDOM 구도를 유지하면서 jQuery=전체 재렌더링/느림, React=항상 빠름이라는 단정 제거. 두 실제 라이브러리의 동일 카운터에 MutationObserver를 연결해 버튼 노드 정체성과 텍스트 변화를 관찰. 수치는 성능 벤치마크가 아니며 속도 측정을 시도하지 않음. 자동 배치는 여러 상태 갱신에 관한 후속 주제로 본 장의 단일 클릭 예시에서 성능 근거로 확대하지 않음.')
# 20 · Explore familiar React services before the setup chapter.
services=json.loads((ROOT/'materials/react-services.json').read_text())
service_refs=tuple(f'S{i+1:02}' for i in range(len(services)))
add(dict(type='services',items=services),refs=service_refs,
    note='실습 챕터 앞의 서비스 탐색 장. 여섯 서비스의 공식 아이콘과 서비스명으로 3×2 링크 그리드 구성. 링크는 새 탭에서 서비스 자체로 이동. 공식 기술 자료는 React 활용의 근거이며 발행 시점은 react-services.json에 별도 기록. 사이트 전체와 모든 모바일 앱이 동일 기술로 구현됐다는 주장은 하지 않음.')
# 22–24 · Instructor demonstration, not a student lab.
add(
    table('개발 도구의 역할||Development Tool Roles', ['도구||Tool','역할||Role'],
        ['Node.js','개발 도구를 컴퓨터에서 실행하는 환경||Environment for running development tools'],
        ['npm','프로젝트 생성 도구 실행 · 패키지 설치||Project scaffolding tools · Package installation'],
        ['Vite','개발 서버 · 변경 반영 · 배포용 빌드||Dev server · Live updates · Production builds']),
    code('터미널 · 설치 확인||Terminal · Installation Checks','node -v\nnpm -v'),
    concepts(
        ('실행 조건 - Vite 가이드의 Node.js 버전 요구사항||Runtime Requirement - The Node.js versions in the Vite guide',
         'Node.js 20.19+ 또는 22.12+||Node.js 20.19+ or 22.12+',
         '템플릿의 추가 버전 조건 확인||Check for higher version requirements in the template')),
    refs=('R17',),
    note='강사 시연. 수업 직전 실제 Node/Vite 템플릿 지원 버전 재확인. npm은 Node 설치 환경에 함께 제공. 학생 실습 지시나 새 과제 없음.')
add(code('터미널 · 생성 → 설치 → 실행||Terminal · Scaffold → Install → Run','npm create vite@latest pwd-week4-demo -- --template react-ts\ncd pwd-week4-demo\nnpm install\nnpm run dev'),code('터미널 · 실행 출력||Terminal · Run Output','VITE v8.3.0  ready in 110 ms\n➜  Local:   http://127.0.0.1:4320/', 'text'),figure('materials/images/vite-start.png','Vite React TypeScript 프로젝트의 초기 브라우저 화면||Initial browser screen of a Vite React TypeScript project','Local 주소 접속 · React + TypeScript 템플릿||Open the Local URL · React + TypeScript template'),layout='setup',refs=('R16','R17'),note='강사 시연. 출력은 제작 시 실제 실행 기록이며 촬영용 --host 127.0.0.1 --port 4320 옵션 사용. 자료 제작 환경에서 실제 create-vite react-ts 생성·npm install·개발 서버 실행·브라우저 접속 검증. 그림은 실제 실행 화면 캡처. 포트 번호는 터미널 Local 출력 사용.')
add(code('src/App.tsx · 최초 화면||src/App.tsx · First Screen','export default function App() {\n  return <h1>Hello, World!</h1>;\n}', 'tsx'),code('src/App.tsx · 문구 변경 후 저장||src/App.tsx · Text Changed and Saved','export default function App() {\n  return <h1>Hello, React!</h1>;\n}', 'tsx'),demo('hello'),layout='hello',refs=('R16','R17'),note='실제 Vite react-ts 프로젝트에서 App.tsx의 Hello, World! → Hello, React! 저장 후 HMR 검증. 두 이미지는 각 상태의 실제 브라우저 캡처. 슬라이드에는 실제 캡처된 두 결과를 함께 표시. src/index.css의 기본 스타일 유지. JSX는 화면 구조를 적는 문법 수준으로만 소개.')
assert len(slides)==19
research=(ROOT/'materials/week-04-react-research.ko.txt').read_text()
sources={m[0]:[m[1],m[2],'2026-09-23 확인'] for m in re.findall(r'### (R\d+)\. ([^\n]+).*?링크: (\S+)',research,re.S)}
from urllib.parse import quote as urlquote
pdf_path='../05/materials/'+urlquote('[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf')
for number in range(4,9):
    sources[f'P{number:02}']=[f'2025 React PDF · p.{number}',pdf_path+f'#page={number}','2026-09-23 원본 확인']
sources.update({
    'J01':['jQuery Overview','https://jquery.com/','2026-09-23 확인'],
    'J02':['jQuery .text()','https://api.jquery.com/text/','2026-09-23 확인'],
    'J03':['jQuery .on()','https://api.jquery.com/on/','2026-09-23 확인'],
    'R18':['React useState','https://react.dev/reference/react/useState','2026-09-23 확인'],
    'R19':['MDN · DOM','https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model','2026-09-23 확인'],
})
for ref,service in zip(service_refs,services):
    sources[ref]=[service['source_title'],service['source_url'],service['published']+' 발행 · '+service['checked']+' 확인']
(ROOT/'materials/react-body.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
(ROOT/'materials/react-sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print('Built content for 19 React topics')
