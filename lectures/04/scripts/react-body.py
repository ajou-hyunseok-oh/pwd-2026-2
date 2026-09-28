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
    block=dict(type='table',heads=[prose(x) for x in heads],rows=[[prose(x) for x in r] for r in rows])
    if title: block['title']=prose(title)
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
# React's role in a web service.
add(
    dict(type='role_diagram',
         title=p('웹 서비스 안에서의 위치||Its Place in a Web Service'),
         server=p('서버 · 데이터베이스||Server · Database'),
         server_role=p('요청 처리 · 공유 데이터 저장||Process requests · Store shared data'),
         exchange=p('요청 · 데이터||Requests · Data'),
         browser=p('브라우저||Browser'),
         react=p('React'),
         react_role=p('컴포넌트로 UI 계산 · 변경 반영||Compute UI with components · Apply updates'),
         display=p('DOM · CSS'),
         display_role=p('문서 구조 · 스타일 · 화면 표시||Document structure · Styling · Display')),
    refs=('R10','R13'),
    note='React는 브라우저 안에서 UI를 구성하고 갱신하는 라이브러리. 서버·데이터베이스는 요청 처리와 공유 데이터 저장을 담당. 화살표는 요청·데이터 흐름과 UI 변경 반영을 개략적으로 나타내며, React가 CSS를 생성하거나 서버 역할을 맡는다는 뜻은 아님.')
# React's origins: the burden of manual DOM updates and React's response.
add(
    table('기존의 DOM 직접 수정 방식||Direct DOM Updates', ['상황||Situation','개발자가 관리하던 일||What the Developer Managed'],
        ['데이터 변경||Data changed','변경된 값과 영향을 받는 화면 요소 확인||Find changed values and affected UI elements'],
        ['화면 갱신||UI update','DOM 요소를 찾아 텍스트·속성·목록을 직접 수정||Select DOM nodes and update text, attributes, and lists'],
        ['화면 복잡화||Growing UI complexity','여러 갱신 코드가 데이터와 화면을 일치시키도록 관리||Keep scattered update code and displayed data in sync']),
    concepts(
        ('문제 - 화면 수정 책임이 개발 코드 곳곳에 분산||Problem - UI update logic spread across the code',
         '데이터가 바뀔 때마다 DOM과의 일치를 직접 유지||Manually keep the DOM in sync as data changes'),
        ('React의 제안(2013) - 현재 데이터에 맞는 화면을 기술||React’s Proposal (2013) - Describe the UI for current data',
         'React = re(다시) + act(작동): 바뀐 데이터에 맞는 화면을 다시 기술||React = re (again) + act: describe the UI again for the changed data',
         '컴포넌트가 데이터에 따른 화면을 반환||Components return a UI description from the data',
         'React가 이전 결과와 비교해 필요한 DOM 변경을 반영||React compares results and applies the needed DOM changes')),
    refs=('R01','R20'),
    note='Pete Hunt의 2013년 첫 블로그 글을 바탕으로 직접 DOM 갱신의 부담과 React의 접근을 설명. re + act 분해는 이름과 작동 방식을 연결하는 강의용 풀이이며, 이름에 관한 2016년 개발 회고는 상태·속성 변화에 반응한다는 Jordan Walke의 설명을 기록. React 이전의 모든 도구가 DOM을 직접 수정해야 했다는 뜻은 아님. jQuery 자체가 상태 불일치를 일으킨다는 주장도 아님.')
# 05 · The 2020 Facebook.com redesign used React alongside CSS, code, data, and navigation changes.
add(
    figure('materials/images/facebook-2020-light.png',
        '2020년 재설계된 Facebook.com의 탐색·피드·설정 화면||Navigation, feed, and settings in the redesigned 2020 Facebook.com',
        'PHP 서버 화면 → React 기반 브라우저 앱 · 2020년||PHP server pages → React client app · 2020'),
    concepts(
        ('CSS - 스타일과 다크 모드||CSS - Styles and Dark Mode',
         '원자적 CSS로 홈 화면 CSS 80% 축소 · 변수로 테마 전환||Atomic CSS cut homepage CSS by 80%; variables switch themes'),
        ('JavaScript - 필요한 코드부터||JavaScript - Load What Is Needed First',
         '첫 화면 표시와 이후 기능에 맞춰 코드를 3단계로 분리||Code split into three tiers for first paint and later features'),
        ('데이터 - Relay·GraphQL||Data - Relay and GraphQL',
         '필요한 데이터를 미리 요청 · 피드 항목을 순차 전달||Preload needed data and stream feed stories as they arrive'),
        ('탐색 - 다음 화면 준비||Navigation - Prepare the Next Screen',
         '이동할 화면의 코드·데이터를 미리 가져와 전환 지연 감소||Prefetch code and data for the destination to reduce delays')),
    refs=('R07',),
    layout='visual',
    note='원문 이미지: https://engineering.fb.com/wp-content/uploads/2020/05/1.-Home-Setting-Light-Mode.png\nMeta의 2020-05-08 기술 회고. React 기반 클라이언트 앱으로 재설계하면서 CSS·JavaScript·데이터·탐색을 함께 개선. CSS 80% 감소는 기사에서 밝힌 새 홈 화면의 CSS 전송량 비교. 3단계는 JavaScript Loading Tiers. 데이터는 Relay·GraphQL의 선요청과 피드 스트리밍, 탐색은 경로 정의와 다음 화면 자원의 미리 가져오기를 요약. 성능 변화를 React 단독 효과로 해석하지 않음.')
# 06
add(
    table('', ['시기||Date','변화||Change','의미||Significance'],
        ['2013.05','React 오픈소스 공개||React open-sourced','데이터에 맞는 UI를 컴포넌트로 기술||Describe data-driven UI with components'],
        ['2017.09','React 16 · Fiber 도입||React 16 · Fiber','렌더링 코어 재작성 · 후속 비동기 기능의 기반||Rebuilt rendering core · Foundation for later async features'],
        ['2019.02','React 16.8 · Hooks 도입||React 16.8 · Hooks','함수 컴포넌트에서 상태와 로직 재사용||State and reusable logic in function components'],
        ['2022.03','React 18 · 동시성 렌더러||React 18 · Concurrent renderer','긴급도에 따른 화면 갱신 · 자동 배칭||Prioritized UI updates · Automatic batching'],
        ['2024.12','React 19 · Actions · 서버 컴포넌트||React 19 · Actions and Server Components','폼 작업 상태 관리 · 서버에서 컴포넌트 실행||Form action state · Components run on the server']),
    refs=('R02','R01','R21','R03','R22','R23'),
    note='기술의 설계·작성·렌더링 방식이 달라진 시점을 공식 릴리스 자료에서 선별. 2013년 공개 날짜는 React Versions의 최초 커밋 기준. React 16의 Fiber는 새 렌더링 코어였지만 16.0에서 비동기 렌더링 기능은 아직 활성화되지 않음. React 18의 동시성 기능은 해당 기능을 사용할 때 활성화. React 19의 서버 컴포넌트는 지원 프레임워크가 필요. react.dev 문서 공개는 기술 변곡점이 아니므로 제외.')
# 07
add(
    table('2025 Stack Overflow · 전문 개발자||2025 Stack Overflow · Professional Developers',
        ['선택 기술||Selected Technology','지난 1년 사용 경험||Used in the Past Year'],
        ['React','46.9%'], ['jQuery','24.1%'], ['Angular','19.8%'], ['Vue.js','18.4%'], ['Svelte','6.9%']),
    refs=('P04','R05','R06'),
    note='공식 HTML Professional Developers / Have Used 탭. 해당 문항 응답자 19,460명. 여러 기술 선택 가능. 선택 기술 5개만 비교. 전체 웹사이트 점유율 또는 품질 순위가 아님. 2025년 조사로 명시.')
# 10 · A compact definition before the component examples.
add(
    concepts(
        ('컴포넌트 - 화면을 나누어 조합하는 UI 단위||Component - A UI unit composed with others',
         '예 - 검색창 · 상품 목록 · 상품 행||Examples - Search field · Product list · Product row'),
        ('상태 - 컴포넌트가 기억하고 갱신하는 값||State - A value a component remembers and updates',
         '예 - 검색어 · 재고만 보기 선택 여부||Examples - Search query · In-stock-only selection')),
    dict(type='quote',text=p('상태 변경 → 관련 컴포넌트의 UI 재계산 → 조합된 페이지에 반영||State change → UI recalculated for affected components → Composed page updated')),
    refs=('R10','R24'),
    note='React 공식 Thinking in React의 컴포넌트 분해·시각적 상태·데이터 흐름과 State: A Component\'s Memory의 상태 정의를 강의용으로 요약. 마지막 흐름은 이 자료들에 근거한 설명이며 React 공식 문구를 그대로 인용한 것은 아님.')
# 11–13 · The same complete product UI and data throughout.
add(
    demo('components'),
    concepts(
        ('ProductApp - 상품 검색 화면 전체||ProductApp - The complete product search screen',
         'SearchBar와 ProductTable을 조합||Combines SearchBar and ProductTable'),
        ('SearchBar - 검색 조건 입력||SearchBar - Search criteria input',
         '상품명 입력 · 재고 조건 선택||Product-name input · Stock selection'),
        ('ProductTable - 결과 목록 표시||ProductTable - Results display',
         '분류별 상품 · 검색 결과 개수||Products by category · Result count'),
        ('ProductRow ×6 - 상품 한 행의 반복||ProductRow ×6 - Repeated product row',
         '각 행에 상품명 · 가격 · 재고 여부 표시||Each row shows name · price · availability')),
    refs=('R10',),
    layout='split',
    note='공식 Thinking in React의 6개 상품을 한글화. 원본 분류/가격/재고를 유지하고 수업용 결과 개수·재고 문구 추가. 실제 React로 전체 화면을 렌더. 컴포넌트 경계와 이름을 처음부터 표시하고 버튼으로 실제 UI와 비교 가능. ProductApp 아래 SearchBar와 ProductTable, 그 안의 ProductRow 반복을 설명. 분류 제목은 이 구현에서 별도 컴포넌트가 아님. 컴포넌트 분리의 유일한 정답을 주장하지 않음.')
add(
    demo('reuse'),
    concepts(
        ('ProductRow - 같은 UI 정의를 여섯 번 사용||ProductRow - One UI definition used six times',
         '사과 $1 · 용과 $1 · 패션프루트 $2 등 서로 다른 상품 데이터||Different product data such as Apple $1 · Dragonfruit $1 · Passionfruit $2'),
        ('표시 규칙 - 모든 상품 행에 공통 적용||Display rules - Shared by every product row',
         '상품명 - 왼쪽||Name - Left',
         '가격 - 오른쪽||Price - Right',
         '품절 - 색상 · 문구로 구분||Out of stock - Color · Text'),
        ('재사용의 효과 - 한 곳의 표시 규칙을 모든 행에 적용||Benefit of reuse - One set of display rules across all rows',
         'ProductRow 수정 → 여섯 상품 행에 함께 반영||Edit ProductRow → Apply to all six product rows')),
    refs=('R10',),
    layout='split',
    note='11번과 같은 상품 화면·데이터. 다른 서비스나 미제시 화면을 새로 가정하지 않음. Props 문법은 다루지 않음.')
add(demo('filter'),refs=('R10',),note='왼쪽 전체 6개와 오른쪽 재고 있는 4개를 동시 표시. 오른쪽 검색창·재고 필터 조작 가능. 재고 조건 선택으로 품절 2개가 목록에서 제외되고 결과 개수가 6→4로 바뀌는 초기 화면. 이름/가격/재고 원본은 동일하며 결과 개수는 필터 결과에서 계산. Print에서도 두 화면 보존.')
# 14 · Definitions and matching counter code on one print-friendly slide.
add(
    concepts(
        ('명령형 - 작업의 순서와 방법을 직접 지정||Imperative - Explicit steps and operations',
         'jQuery - 버튼을 만들고 클릭 이벤트를 연결||jQuery - Create the button and attach a click handler',
         '클릭 후 button.text(...)로 화면의 텍스트를 직접 수정||After a click, update the displayed text with button.text(...)')),
    concepts(
        ('선언형 - 원하는 결과의 조건이나 형태를 정의||Declarative - Conditions or form of the desired result',
         'React - 현재 count에 맞는 버튼 UI를 기술||React - Describe the button UI for the current count',
         '클릭 후 setCount(...)로 상태 변경 · React가 화면 갱신||After a click, setCount(...) changes state and React updates the UI')),
    code('jQuery · DOM 직접 수정||jQuery · Direct DOM Update', example('jquery'), 'javascript', width=64,
         caption='count 증가 → button.text(...) 호출||Increment count → Call button.text(...)'),
    code('React · 상태에 따른 UI||React · UI from State', example('react'), 'jsx', width=64,
         caption='setCount(...) 호출 → 현재 count에 맞는 버튼 UI||Call setCount(...) → Button UI for the current count'),
    layout='programming',
    refs=('P06','R01','R10','J02','J03','R18'),
    note='13번의 재고 필터 변화를 본 뒤, 같은 클릭 카운터를 jQuery와 React로 비교. 명령형·선언형의 일반적 정의와 각 UI 구현 사례를 한 장에서 연결. 두 코드는 모두 0에서 시작해 클릭마다 1 증가하며, PDF에서도 코드와 설명만으로 차이를 읽을 수 있도록 실행 화면을 제거. 표시 코드는 실행 모듈에서 추출. 전제: jQuery의 $와 React의 useState import, host는 jQuery 출력 DOM 영역, React는 Counter를 마운트. JSX와 useState는 현재 count에 맞는 화면을 기술하는 데 필요한 범위만 설명. 단방향 데이터 흐름은 선언형의 정의에 섞지 않음.')
# 15 · React's influence on later UI frameworks.
add(
    dict(type='quote',text=p('React의 컴포넌트 기반·선언형 UI 접근은 다른 UI 프레임워크 설계에도 영향||React’s component-based, declarative approach also influenced other UI frameworks')),
    concepts(
        ('React Native - React의 UI 모델을 모바일 앱에 적용||React Native - React’s UI model applied to mobile apps',
         '컴포넌트와 상태 개념을 iOS·Android 개발에 활용||Components and state used to build iOS and Android apps'),
        ('Flutter - React에서 영감을 받은 UI 설계||Flutter - UI design inspired by React',
         '공식 문서에서 위젯·상태에 따른 선언형 화면 구성을 설명||Its official documentation describes declarative screens built from widgets and state')),
    refs=('R25','R26','R29'),
    note='React Native 공식 문서는 React의 핵심 개념인 컴포넌트·상태를 모바일 개발에 적용한다고 설명. Flutter 공식 UI 소개와 아키텍처 문서는 React에서 영감을 받은 설계라고 명시. 두 사례를 통해 React의 설계 접근이 다른 UI 프레임워크에 미친 영향을 소개하되, 모든 선언형 UI가 React에서 처음 나왔거나 모든 프레임워크가 동일하게 구현된다는 뜻은 아님.')
# 17–20 · Virtual DOM: concept, comparison, update process, and tradeoffs.
add(
    concepts(
        ('DOM - 브라우저가 관리하는 실제 문서 구조||DOM - The document structure managed by the browser',
         '화면의 요소·텍스트·속성을 담는 노드||Nodes containing screen elements, text, and attributes'),
        ('Virtual DOM - 원하는 UI를 나타내는 메모리의 표현||Virtual DOM - An in-memory representation of the desired UI',
         'React가 현재 UI와 다음 UI를 대조할 때 사용하는 개념적 모델||A conceptual model React uses to compare the current and next UI'),
        ('화면 표시 - 최종 변경은 실제 DOM에 반영||Display - Final changes are applied to the real DOM',
         '브라우저는 갱신된 DOM을 바탕으로 화면 표시||The browser displays the updated DOM')),
    refs=('R30','R13','R19'),
    note='React 구 공식 FAQ의 VDOM 정의와 최신 Render and Commit 문서로 확인. Virtual DOM은 별도 브라우저 화면이나 실제 DOM 전체의 복제본이 아님. React elements와 내부 Fiber를 모두 포함해 넓게 쓰이는 개념이므로 특정 JavaScript 객체 구조라고 단정하지 않음.')
add(
    table('같은 재고 필터 변경 · 검색 결과 6개 → 4개||Same Stock Filter Change · Results 6 → 4',
        ['비교||Comparison','DOM 직접 갱신||Direct DOM Updates','React · Virtual DOM 활용||React · Virtual DOM'],
        ['개발자가 작성||Developer writes','품절 행 제거 · 결과 개수 수정 명령||Commands to remove unavailable rows and change the count','재고 조건 상태와 그 상태에 맞는 UI||Stock-filter state and the UI for that state'],
        ['변경할 요소 결정||Who selects changes','개발 코드가 DOM 노드를 찾아 지정||Application code finds and selects DOM nodes','React가 이전·새 UI를 대조해 결정||React compares previous and next UI'],
        ['최종 화면||Final output','실제 DOM 갱신||Real DOM updated','실제 DOM 갱신||Real DOM updated'], widths='18% 41% 41%'),
    dict(type='quote',text=p('차이 - 실제 DOM 사용 여부가 아니라 변경할 요소를 결정하는 책임||Difference - Who decides which DOM nodes to change')),
    refs=('R30','R13','J02'),
    note='13번과 같은 재고 필터 6→4 사례를 사용. 직접 DOM 갱신도 필요한 노드만 수정할 수 있으므로 전체 화면 재생성 또는 느림으로 단정하지 않음. React 역시 최종적으로 실제 DOM을 바꾼다는 점을 표의 마지막 행에서 강조. VDOM은 React 내부 UI 표현을 설명하기 위한 강의용 용어.')
add(
    dict(type='update_flow',steps=[
        (p('Trigger'),p('상태 변경||State change')),
        (p('Render'),p('UI 계산·대조||Calculate · Compare UI')),
        (p('Commit'),p('DOM 변경||Update DOM')),
        (p('Browser'),p('화면 표시||Display screen'))]),
    concepts(
        ('① Trigger - 재고 조건 상태 변경||① Trigger - Stock-filter state changes',
         '「재고 있는 상품만」 선택||Select “Only products in stock”'),
        ('② Render - 새 UI 계산과 이전 결과 대조||② Render - Calculate and compare the next UI',
         '컴포넌트 실행 · 결과 4개와 상품 행 구성 계산||Run components · Calculate four results and their rows'),
        ('③ Commit - 필요한 DOM 변경 반영||③ Commit - Apply necessary DOM changes',
         '품절 행 2개 제거 · 결과 개수 6 → 4||Remove two unavailable rows · Change result count 6 → 4'),
        ('④ Browser - 갱신된 화면 표시||④ Browser - Display the updated screen',
         'DOM 변경 후 브라우저가 화면을 그림||The browser paints after DOM changes')),
    refs=('R13','R30'),
    note='React 공식 Render and Commit의 Trigger·Render·Commit과 Browser paint를 13번 상품 필터 사례에 적용. Render에서는 새 UI 계산과 이전 결과에 따른 변경 판단, Commit에서는 실제 DOM 반영. 단순화된 설명이며 모든 렌더가 DOM 변경을 만드는 것은 아님. 브라우저의 스타일·레이아웃·페인트는 DOM 반영 뒤 필요한 범위에서 수행.')
add(
    concepts(
        ('효과 - UI 정의와 DOM 갱신 책임 분리||Effect - Separate UI definition from DOM update decisions',
         '개발자는 상태에 맞는 화면을 기술 · React가 필요한 변경을 반영||Developers describe the UI for state · React applies required changes'),
        ('장점 - 변경 범위 관리와 기존 요소 유지||Benefit - Manage updates and preserve existing elements',
         '차이가 없는 DOM 노드는 유지 · 복잡한 화면의 갱신 코드 감소||Unchanged DOM nodes remain · Less manual update code for complex screens'),
        ('비용 - UI 계산과 대조 작업||Cost - UI calculation and comparison',
         '메모리의 UI 표현 · 컴포넌트 재실행에 필요한 작업량||In-memory UI representation · Work to re-run components'),
        ('한계 - 성능 우위는 자동으로 보장되지 않음||Limit - Performance is not automatically better',
         '단순한 직접 갱신이 더 적은 작업일 수 있음 · 실제 속도는 측정으로 판단||A simple direct update may do less work · Measure actual performance')),
    refs=('R30','R13','R31'),
    note='VDOM의 핵심 효과는 선언형 UI와 변경 결정의 자동화. DOM을 적게 수정하는 결과를 얻을 수 있으나 직접 DOM 코드도 필요한 부분만 수정 가능. React Render and Commit은 상위 컴포넌트 갱신 시 하위 컴포넌트 재실행 비용을 설명하고, memo 문서는 비교가 렌더보다 빠른지 실제 측정을 권함. VDOM 자체가 항상 빠르다는 주장은 피함.')
# Service examples appear immediately after the React usage survey.
services=json.loads((ROOT/'materials/react-services.json').read_text())
service_refs=tuple(f'S{i+1:02}' for i in range(len(services)))
add(dict(type='services',items=services),refs=service_refs,
    note='React 사용 현황 다음의 서비스 탐색 장. 여섯 서비스의 공식 아이콘과 서비스명으로 3×2 링크 그리드 구성. 링크는 새 탭에서 서비스 자체로 이동. 공식 기술 자료는 React 활용의 근거이며 발행 시점은 react-services.json에 별도 기록. 사이트 전체와 모든 모바일 앱이 동일 기술로 구현됐다는 주장은 하지 않음.')
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
add(
    code('터미널 · 생성 → 설치 → 실행||Terminal · Scaffold → Install → Run',
         'npm create vite@latest pwd-week4-demo -- --template react-ts\ncd pwd-week4-demo\nnpm install\nnpm run dev',
         caption='첫 명령은 한 줄로 입력 · 설치 확인 메시지가 나오면 y 선택||Enter the first command on one line · If npm asks to install, enter y'),
    code('터미널 · 실행 출력 예시||Terminal · Example Output',
         'VITE v8.x.x  ready\n➜  Local:   http://localhost:5173/', 'text',
         caption='실제 접속 주소는 터미널의 Local 출력 확인||Use the Local URL shown in your terminal'),
    figure('materials/images/vite-start.png',
           'Vite React TypeScript 프로젝트의 초기 브라우저 화면||Initial browser screen of a Vite React TypeScript project',
           'Local 주소 접속 · React + TypeScript 템플릿||Open the Local URL · React + TypeScript template'),
    layout='setup',refs=('R16','R17'),
    note='강사 시연. 표시한 명령을 임시 폴더에서 2026-09-28에 다시 실행해 create-vite react-ts 생성·npm install·기본 개발 서버 localhost:5173 접속·App.tsx 변경·npm run build 검증. 출력의 버전과 포트는 예시이며 다른 포트가 할당될 수 있으므로 터미널 Local 주소 사용. 그림은 과거 실제 실행 화면 캡처로 촬영 시 --host 127.0.0.1 --port 4320 옵션 사용.')
add(code('src/App.tsx · 최초 화면||src/App.tsx · First Screen','export default function App() {\n  return <h1>Hello, World!</h1>;\n}', 'tsx'),code('src/App.tsx · 문구 변경 후 저장||src/App.tsx · Text Changed and Saved','export default function App() {\n  return <h1>Hello, React!</h1>;\n}', 'tsx'),demo('hello'),layout='hello',refs=('R16','R17'),note='실제 Vite react-ts 프로젝트에서 App.tsx의 Hello, World! → Hello, React! 저장 후 HMR 검증. 두 이미지는 각 상태의 실제 브라우저 캡처. 슬라이드에는 실제 캡처된 두 결과를 함께 표시. src/index.css의 기본 스타일 유지. JSX는 화면 구조를 적는 문법 수준으로만 소개.')
assert len(slides)==19
slides[0], slides[1] = slides[1], slides[0]
slides.insert(5, slides.pop(15))  # Service examples become slide 08, after the usage survey.
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
    'R20':['Our First 50,000 Stars','https://legacy.reactjs.org/blog/2016/09/28/our-first-50000-stars.html','2026-09-28 확인'],
    'R21':['React 16 release','https://legacy.reactjs.org/blog/2017/09/26/react-v16.0.html','2026-09-28 확인'],
    'R22':['React 18 release','https://react.dev/blog/2022/03/29/react-v18','2026-09-28 확인'],
    'R23':['React 19 release','https://react.dev/blog/2024/12/05/react-19','2026-09-28 확인'],
    'R24':["State: A Component's Memory",'https://react.dev/learn/state-a-components-memory','2026-09-28 확인'],
    'R25':['React Native · Learn once, write anywhere','https://reactnative.dev/','2026-09-28 확인'],
    'R26':['React Native · Learn the Basics','https://reactnative.dev/docs/tutorial','2026-09-28 확인'],
    'R27':['React DOM APIs','https://react.dev/reference/react-dom','2026-09-28 확인'],
    'R29':['Flutter · Building user interfaces','https://docs.flutter.dev/ui','2026-09-28 확인'],
    'R30':['React · Virtual DOM and Internals','https://legacy.reactjs.org/docs/faq-internals.html','2026-09-28 확인'],
    'R31':['React · memo','https://react.dev/reference/react/memo','2026-09-28 확인'],
})
for ref,service in zip(service_refs,services):
    sources[ref]=[service['source_title'],service['source_url'],service['published']+' 발행 · '+service['checked']+' 확인']
(ROOT/'materials/react-body.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
(ROOT/'materials/react-sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(f'Built content for {len(slides)} React topics')
