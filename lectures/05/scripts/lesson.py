"""Lecture 05: seven chapters, 32 topics; React core and Next.js App Router."""
from urllib.parse import quote

SLIDES = []
PDF = 'materials/' + quote('[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf')
def P(ko, en): return (ko, en)
def C(*items): return dict(kind='concepts', items=items)
def K(label, code, lang='jsx', width=64): return dict(kind='code', label=label, code=code, lang=lang, width=width)
def T(head, *rows): return dict(kind='table', head=head, rows=rows)
def S(*items): return dict(kind='steps', items=items)
def pdf(page): return ('React PDF · p.' + str(page), PDF + '#page=' + str(page))
def react(path): return ('React · Official', 'https://react.dev/' + path)
def nextdoc(path): return ('Next.js · Official', 'https://nextjs.org/docs/app/' + path)
def add(id, title, lead, *blocks, layout='split', sources=(), note='', kind='topic', topic_number=None):
    SLIDES.append(dict(id=id, chapter=CH, title=title, lead=lead, blocks=list(blocks), layout=layout, sources=list(sources), note=note, kind=kind, topic_number=topic_number))
def chapter(n, ko, en, subko, suben):
    global CH
    CH = P(f'CHAPTER {n:02} · {ko}', f'CHAPTER {n:02} · {en}')
    add(f'chapter-{n:02}', P(ko,en), P(subko,suben), kind='chapter')
def topic(n, ko, en, subko, suben, code, points, source, label=None, layout='split'):
    concepts = C(*[(P(a,b), [P(c,d)]) for a,b,c,d in points])
    blocks = [concepts]
    if code:
        blocks.append(K(label or P('React · 개념 예제', 'React · Teaching example'), code))
    add(f'topic-{n:02}', P(ko,en), P(subko,suben), *blocks, sources=source, layout=layout if code else 'single', topic_number=n)

CH = P('LECTURE 05 · 프로그래밍과 웹데이터', 'LECTURE 05 · PROGRAMMING AND WEB DATA')
add('cover', P('React Framework의 이해', 'Understanding React Framework'), P('컴포넌트와 상태에서 서버 데이터와 비동기 UI까지', 'From components and state to server data and async UI'), kind='cover')
chapter(1, 'React 애플리케이션의 이해', 'Understanding React Applications', '컴포넌트와 데이터로 구성하는 사용자 인터페이스', 'User interfaces composed from components and data')
topic(1,'React 기초 요약','React Fundamentals Recap','컴포넌트 구성과 현재 데이터에 따른 화면 표현','Components and views derived from current data', '''
function ProductRow({ product }) {
  return <li>{product.name}: {product.price}원</li>;
}
export default function App() {
  const product = { id: 'p1', name: '사과', price: 1000 };
  return <ul><ProductRow product={product} /></ul>;
}
''', [('컴포넌트의 조합','Component composition','App이 상품 데이터를 준비하고 ProductRow가 한 행을 표현한다.','App provides product data; ProductRow describes one row.'),('선언형 UI','Declarative UI','DOM 수정 명령 대신 현재 데이터에 대응하는 JSX를 반환한다.','Return JSX for current data instead of issuing DOM mutation commands.'),('관찰 결과','Observe','화면에는 “사과: 1000원”이 나타난다.','The screen displays “사과: 1000원”.')], [('Lecture 04','../04/'),react('learn/thinking-in-react')])
topic(2,'React와 프레임워크의 역할','React and Frameworks','UI 표현과 라우팅·데이터 처리·렌더링 도구의 관계','How UI relates to routing, data, and rendering tools', '''
// app/products/page.jsx (Next.js App Router)
import Link from 'next/link';
export default function ProductsPage() {
  return (
    <main>
      <h1>상품 목록</h1>
      <Link href="/products/p1">사과 상세 보기</Link>
    </main>
  );
}
''', [('React의 책임','React responsibilities','컴포넌트·상태·화면 갱신을 통해 UI를 구성한다.','Build UI through components, state, and updates.'),('프레임워크의 책임','Framework responsibilities','URL과 파일 연결, 서버 실행, 데이터 처리와 빌드를 통합한다.','Integrate URL conventions, server execution, data handling, and builds.'),('관찰 결과','Observe','Next.js에서 파일 경로가 /products 페이지를 만든다. Vite 단독에는 이 규칙이 없다.','Next.js maps this file to /products. Vite alone does not provide this convention.')], [react('learn/creating-a-react-app'),nextdoc('getting-started/layouts-and-pages')],P('Next.js · 페이지 파일 전체', 'Next.js · Complete page file'))
chapter(2,'JSX와 컴포넌트 기반 화면 구성','JSX and Component-Based UI','데이터를 UI로 표현하고 작은 단위로 조합하는 방법','Express data as UI and compose small units')
topic(3,'JSX의 역할','The Role of JSX','JavaScript 안에서 표현하는 UI 구조와 데이터','UI structure and data expressed in JavaScript', '''
export default function ProductTitle() {
  const product = { name: '사과', price: 1000 };
  return (
    <h2>
      {product.name} · {product.price * 2}원
    </h2>
  );
}
''', [('JSX는 문법 확장','JSX is a syntax extension','빌드 도구가 JSX를 JavaScript로 변환한다. HTML 문자열로 직접 삽입하지 않는다.','Build tools transform JSX into JavaScript; JSX is not an HTML string.'),('중괄호의 표현식','Expressions in braces','JavaScript 값을 UI 안에 삽입하고 계산할 수 있다.','Insert and compute JavaScript values inside the UI.'),('관찰 결과','Observe','상품명과 계산된 가격으로 “사과 · 2000원”을 표시한다.','Displays “사과 · 2000원” from the name and computed price.')], [pdf(9),react('learn/javascript-in-jsx-with-curly-braces')])
topic(4,'JSX 작성 규칙','JSX Rules','요소와 속성, 표현식과 Fragment','Elements, attributes, expressions, and Fragments', '''
export default function ProductField() {
  return (
    <>
      <label htmlFor="product">상품명</label>
      <input id="product" className="field" />
      <p style={{ color: 'green' }}>필수 입력</p>
    </>
  );
}
''', [('하나의 반환 구조','One returned structure','Fragment(<>)는 DOM 요소를 추가하지 않고 형제 요소를 묶는다.','A Fragment (<>) groups siblings without adding a DOM element.'),('태그와 속성','Tags and attributes','태그를 닫고 className·htmlFor를 사용한다. style에는 객체를 전달한다.','Close tags and use className and htmlFor. Pass an object to style.'),('관찰 결과','Observe','label과 input이 연결되고 설명 문장이 녹색으로 표시된다.','The label targets the input and the description appears green.')], [pdf(9),react('learn/writing-markup-with-jsx')])
topic(5,'함수 컴포넌트와 Props','Function Components and Props','입력 데이터를 받아 화면을 반환하는 함수','Functions that receive data and return UI', '''
function Price({ amount, unit = '원' }) {
  return <strong>{amount}{unit}</strong>;
}
export default function App() {
  return (
    <>
      <Price amount={1000} />
      <Price amount={2} unit="USD" />
    </>
  );
}
''', [('Props는 읽기 전용 입력','Props are read-only inputs','부모가 값을 전달한다. 자식은 Props를 직접 변경하지 않는다.','The parent passes values; the child does not mutate its props.'),('같은 정의, 다른 데이터','Same definition, different data','대문자로 시작하는 컴포넌트를 JSX에서 사용한다.','Use a capitalized component name in JSX.'),('관찰 결과','Observe','같은 Price가 “1000원”과 “2USD”를 각각 표시한다.','The same Price renders “1000원” and “2USD”.')], [pdf(13),react('learn/passing-props-to-a-component')])
topic(6,'컴포넌트의 분리와 조합','Splitting and Composing Components','책임 구분과 children을 통한 UI 재사용','Separate responsibilities and reuse UI through children', '''
function Card({ title, children }) {
  return (
    <section>
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}
export default function App() {
  return (
    <Card title="상품 정보">
      <p>사과 · 1000원</p>
    </Card>
  );
}
''', [('역할에 따른 분리','Separate by responsibility','카드는 공통 외형을, 내부 내용은 사용하는 쪽이 결정한다.','Card owns the shared structure; its caller chooses the content.'),('children으로 조합','Compose with children','여는 태그와 닫는 태그 사이의 JSX가 children으로 전달된다.','JSX between the opening and closing tags becomes children.'),('관찰 결과','Observe','동일한 카드 구조 안에 다른 상품·안내 내용을 넣을 수 있다.','The same card structure can contain different products or guidance.')], [pdf(13),react('learn/passing-props-to-a-component')])
topic(7,'조건부 렌더링과 목록','Conditional Rendering and Lists','조건에 따른 화면 표현과 map·key를 이용한 항목 구성','Conditions, map, and keys for list items', '''
export default function ProductList({ products }) {
  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name}
          {product.stocked ? ' · 재고 있음' : ' · 품절'}
        </li>
      ))}
    </ul>
  );
}
''', [('조건은 JavaScript로','Conditions use JavaScript','삼항 연산자로 재고 여부에 따른 문구를 선택한다.','A ternary expression selects the stock label.'),('목록 항목의 식별','Identify list items','map은 요소 배열을 만들고 안정적인 id를 key로 사용한다.','map produces elements; stable IDs serve as keys.'),('관찰 결과','Observe','products의 순서대로 표시된다. key는 화면 문구나 일반 Props로 전달되지 않는다.','Items follow products order. key is neither displayed text nor a normal prop.')], [react('learn/rendering-lists'),react('learn/conditional-rendering')],P('React · 컴포넌트 전체 / products는 부모가 전달','React · Complete component / parent supplies products'))
chapter(3,'사용자 행동과 상태 기반 화면 갱신','User Actions and State Updates','사용자의 입력을 기억하고 화면에 반영하는 원리','Remember user input and reflect it in the UI')
topic(8,'이벤트와 State','Events and State','사용자의 클릭·입력과 컴포넌트가 기억하는 값','User clicks and input, and values a component remembers', '''
import { useState } from 'react';
export default function Quantity() {
  const [quantity, setQuantity] = useState(1);
  return (
    <button onClick={() => setQuantity(quantity + 1)}>
      수량: {quantity}
    </button>
  );
}
''', [('State가 값을 기억','State remembers a value','일반 지역 변수와 달리 렌더 사이에 값이 유지된다.','Unlike local variables, state persists between renders.'),('이벤트에 함수 전달','Pass a function to the event','onClick에 함수를 전달하고 클릭했을 때 상태 변경을 요청한다.','Pass a function to onClick; a click requests an update.'),('관찰 결과','Observe','초기 수량 1이 클릭할 때마다 2, 3으로 증가한다.','The initial quantity 1 increases to 2 and 3 with clicks.')], [pdf(14),pdf(15),react('learn/state-a-components-memory')])
topic(9,'상태 변경과 화면 갱신','State Updates and Rendering','컴포넌트의 UI 계산과 DOM 반영, Render와 Commit','UI calculation and DOM changes: render and commit', '''
import { useState } from 'react';
export default function Quantity() {
  const [quantity, setQuantity] = useState(1);
  console.log('render', quantity);
  return (
    <div>
      <h2>상품 수량</h2>
      <button onClick={() => setQuantity(q => q + 1)}>
        {quantity}
      </button>
    </div>
  );
}
''', [('Render: 다음 UI 계산','Render: calculate the next UI','상태 변경으로 컴포넌트를 다시 실행한다. 렌더 중 외부 데이터를 변경하지 않는다.','An update re-runs the component. Do not mutate external data during render.'),('Commit: DOM에 반영','Commit: apply changes to DOM','React는 필요한 DOM 변경을 수행하고 브라우저가 화면을 그린다.','React applies needed DOM changes; the browser paints the screen.'),('관찰 결과','Observe','클릭 후 숫자가 바뀌지만 제목 DOM은 유지된다. 개발 Strict Mode는 render 로그를 추가 실행할 수 있다.','The number changes while the heading DOM stays. Development Strict Mode may produce extra render logs.')], [react('learn/render-and-commit')])
topic(10,'상태의 스냅샷과 업데이트','State Snapshots and Updates','각 렌더의 상태 값과 이전 상태를 이용한 갱신','Per-render state values and updates based on previous state', '''
import { useState } from 'react';
export default function Counter() {
  const [count, setCount] = useState(0);
  function replace() {
    setCount(count + 1);
    setCount(count + 1);
  }
  function increment() {
    setCount(c => c + 1);
    setCount(c => c + 1);
  }
  return <>
    <p>{count}</p>
    <button onClick={replace}>값 두 번</button>
    <button onClick={increment}>함수 두 번</button>
  </>;
}
''', [('렌더의 스냅샷','Snapshot of a render','같은 이벤트 안의 count는 해당 렌더의 값이다. setter가 지역 값을 즉시 바꾸지 않는다.','count in the event is that render’s value. A setter does not immediately mutate it.'),('업데이트 함수','Updater function','c => c + 1은 대기열에서 이전 결과를 받아 다음 값을 계산한다.','c => c + 1 computes the next value from the previous queued result.'),('관찰 결과','Observe','0에서 “값 두 번”은 1, 이어 “함수 두 번”은 3이 된다.','From 0, “값 두 번” gives 1; then “함수 두 번” gives 3.')], [react('learn/state-as-a-snapshot'),react('learn/queueing-a-series-of-state-updates')])
topic(11,'객체와 배열의 상태 변경','Updating Objects and Arrays','불변성을 유지하는 데이터 갱신','Update data while preserving immutability', '''
import { useState } from 'react';
export default function Stock() {
  const [products, setProducts] = useState([
    { id: 'p1', name: '사과', stocked: false }
  ]);
  function restock() {
    setProducts(items => items.map(p =>
      p.id === 'p1' ? { ...p, stocked: true } : p
    ));
  }
  return <button onClick={restock}>
    {products[0].stocked ? '재고 있음' : '품절'}
  </button>;
}
''', [('새 배열과 새 객체','New array and object','map으로 새 배열을 만들고 변경 항목만 객체 전개로 복사한다.','map creates a new array; spread copies the changed item.'),('원본 상태 보존','Preserve the previous state','products[0].stocked에 직접 대입하지 않는다. 복사는 필요한 깊이까지 수행한다.','Do not assign to products[0].stocked directly. Copy each level that changes.'),('관찰 결과','Observe','버튼의 “품절”이 클릭 후 “재고 있음”으로 바뀐다.','Clicking changes “품절” to “재고 있음”.')], [react('learn/updating-arrays-in-state'),react('learn/updating-objects-in-state')])
topic(12,'상태의 설계와 공유','Designing and Sharing State','최소 상태, 파생값과 공통 부모의 변경 책임','Minimal state, derived values, and a shared parent', '''
import { useState } from 'react';
export default function Search({ products }) {
  const [query, setQuery] = useState('');
  const visible = products.filter(p =>
    p.name.includes(query)
  );
  return <>
    <input value={query}
      onChange={e => setQuery(e.target.value)} />
    <p>{visible.length}개</p>
    <ul>{visible.map(p =>
      <li key={p.id}>{p.name}</li>
    )}</ul>
  </>;
}
''', [('최소 상태와 파생값','Minimal state and derived values','query만 상태로 둔다. visible과 개수는 매 렌더에서 계산한다.','Store query as state; calculate visible items and count during render.'),('단일 변경 책임','One owner of updates','입력과 목록의 공통 부모가 상태를 소유한다. 분리할 때 값과 콜백을 전달한다.','Their shared parent owns state. Pass values and callbacks when splitting components.'),('관찰 결과','Observe','검색어가 바뀌면 목록과 개수가 함께 갱신된다. 이를 위한 Effect는 필요 없다.','Changing the query updates both list and count, without an Effect.')], [react('learn/choosing-the-state-structure'),react('learn/sharing-state-between-components')],P('React · 컴포넌트 전체 / products는 부모가 전달','React · Complete component / parent supplies products'),layout='compact')
topic(13,'컴포넌트의 식별과 상태 보존','Component Identity and State','화면의 위치와 key에 따른 상태 유지·초기화','Preserve or reset state through position and keys', '''
import { useState } from 'react';
function Quantity() {
  const [count, setCount] = useState(1);
  return <button onClick={() => setCount(c => c + 1)}>
    수량: {count}
  </button>;
}
export default function App({ productId }) {
  return <Quantity key={productId} />;
}
''', [('위치·타입·key','Position, type, and key','React는 트리 안의 식별을 기준으로 상태를 보존한다.','React preserves state according to identity in the tree.'),('명시적 초기화','Explicit reset','상품 id가 바뀌면 Quantity의 key가 바뀌어 새 상태로 시작한다.','A new product ID changes Quantity’s key and starts fresh state.'),('비교 실험','Compare','수량을 3으로 만든 뒤 상품을 바꾸면 1로 초기화된다. key를 제거하면 3이 유지된다.','Set quantity to 3 and switch products: it resets to 1. Without key, 3 persists.')], [react('learn/preserving-and-resetting-state')],P('React · 컴포넌트 전체 / 부모가 선택한 productId 전달','React · Complete component / parent passes selected productId'))
chapter(4,'Hooks와 외부 시스템 동기화','Hooks and External Synchronization','상태 관리, 참조와 외부 연결의 역할 구분','Distinguish state, references, and external connections')
topic(14,'Hooks의 역할과 호출 규칙','Hooks and Their Rules','함수 컴포넌트의 기능 확장과 일관된 호출 순서','Extend function components with consistent Hook calls', '''
import { useState } from 'react';
export default function ProductPanel({ visible }) {
  const [count, setCount] = useState(1);
  if (!visible) return null;
  return <button onClick={() => setCount(c => c + 1)}>
    수량: {count}
  </button>;
}
''', [('최상위에서 호출','Call at the top level','Hook을 조건문·반복문·이벤트 안에서 호출하지 않는다. 조기 반환보다 먼저 호출한다.','Do not call Hooks in conditions, loops, or events. Call them before early returns.'),('호출 위치','Where Hooks belong','함수 컴포넌트와 커스텀 Hook 안에서 React의 기능을 사용한다.','Use React features inside function components or custom Hooks.'),('관찰 결과','Observe','visible이 바뀌어도 Hook 호출 순서는 같다. 부모가 컴포넌트를 제거하면 상태는 사라진다.','Hook order stays consistent when visible changes. Removing the component discards its state.')], [pdf(16),react('reference/rules/rules-of-hooks')])
topic(15,'State와 Ref의 구분','State Versus Ref','화면을 갱신하는 값과 렌더 사이에 유지하는 참조','Values that update UI and references that persist', '''
import { useRef, useState } from 'react';
export default function SearchField() {
  const inputRef = useRef(null);
  const [query, setQuery] = useState('');
  return <>
    <input ref={inputRef} value={query}
      onChange={e => setQuery(e.target.value)} />
    <button onClick={() => inputRef.current.focus()}>
      검색창으로 이동
    </button>
    <p>검색어: {query}</p>
  </>;
}
''', [('State: 화면 데이터','State: UI data','query가 바뀌면 렌더가 예약되고 검색어 표시가 갱신된다.','Changing query schedules a render and updates its display.'),('Ref: 유지되는 참조','Ref: persistent reference','inputRef.current로 DOM에 접근한다. Ref 변경 자체는 렌더를 예약하지 않는다.','inputRef.current accesses the DOM. Ref changes alone do not schedule renders.'),('관찰 결과','Observe','입력하면 문구가 바뀌고 버튼을 누르면 입력창에 포커스가 이동한다.','Typing updates the text; clicking the button focuses the input.')], [react('learn/referencing-values-with-refs'),react('learn/manipulating-the-dom-with-refs')])
topic(16,'이벤트 처리와 Effect','Events and Effects','사용자 행동에 따른 작업과 외부 시스템 동기화','User-triggered work and synchronization with external systems', '''
import { useEffect, useState } from 'react';
export default function ProductName() {
  const [name, setName] = useState('사과');
  useEffect(() => {
    const previous = document.title;
    document.title = `상품: ${name}`;
    return () => { document.title = previous; };
  }, [name]);
  return <input value={name}
    onChange={e => setName(e.target.value)} />;
}
''', [('이벤트: 특정 행동','Event: a specific action','사용자가 입력할 때 onChange에서 상태를 변경한다.','onChange updates state when the user types.'),('Effect: 외부와 동기화','Effect: synchronize externally','React 화면 밖의 브라우저 탭 제목을 name과 맞춘다. 파생값 계산은 렌더에서 한다.','Synchronize the browser tab title with name. Compute derived values during render.'),('관찰 결과','Observe','입력값을 바꾸면 탭 제목이 바뀐다. 제거되면 원래 제목으로 돌아간다.','Editing changes the tab title; unmounting restores the original title.')], [pdf(17),react('learn/synchronizing-with-effects'),react('learn/you-might-not-need-an-effect')])
topic(17,'Effect의 의존성과 정리','Effect Dependencies and Cleanup','연결의 시작·갱신·종료와 cleanup','Start, update, and stop connections with cleanup', '''
import { useEffect } from 'react';
export default function Poll({ productId }) {
  useEffect(() => {
    console.log('start', productId);
    const timer = setInterval(() => {
      console.log('poll', productId);
    }, 1000);
    return () => {
      clearInterval(timer);
      console.log('stop', productId);
    };
  }, [productId]);
  return <p>조회 대상: {productId}</p>;
}
''', [('의존성은 사용 값','Dependencies follow used values','Effect가 읽는 반응형 값 productId를 의존성으로 선언한다.','Declare the reactive value productId read by the Effect.'),('정리 후 다시 시작','Clean up before restarting','id 변경 시 이전 타이머를 정리하고 새 타이머를 만든다. 제거할 때도 정리한다.','Clean up the previous timer before starting a new one; also clean up on unmount.'),('관찰 결과','Observe','p1 → p2 변경 시 stop p1 뒤 start p2. 개발 Strict Mode에서는 추가 setup·cleanup 검사가 있다.','Switching p1 → p2 logs stop p1 then start p2. Development Strict Mode adds a setup/cleanup check.')], [pdf(17),react('reference/react/useEffect')],P('React · 로그로 연결 수명 관찰 / productId는 Props','React · Observe connection lifetime in logs / productId is a prop'))
topic(18,'커스텀 Hook과 로직 재사용','Custom Hooks and Logic Reuse','공통 상태·동기화 로직의 추출과 독립적인 상태','Extract shared logic while keeping state independent', '''
import { useState } from 'react';
function useQuantity() {
  const [value, setValue] = useState(1);
  return [value, () => setValue(v => v + 1)];
}
export default function TwoProducts() {
  const [apple, addApple] = useQuantity();
  const [pear, addPear] = useQuantity();
  return <>
    <button onClick={addApple}>사과: {apple}</button>
    <button onClick={addPear}>배: {pear}</button>
  </>;
}
''', [('로직의 추출','Extract logic','use로 시작하는 함수 안에 반복되는 Hook 사용을 묶는다.','Group repeated Hook usage in a function whose name starts with use.'),('상태는 호출마다 독립','Each call owns its state','같은 Hook을 호출해도 상태 값 자체를 공유하지 않는다. 공유가 필요하면 상태를 올린다.','Calling the same Hook does not share state. Lift state when sharing is needed.'),('관찰 결과','Observe','사과 버튼을 눌러도 배 수량은 1을 유지한다.','Clicking the apple button leaves the pear quantity at 1.')], [react('learn/reusing-logic-with-custom-hooks')])
chapter(5,'라우팅과 애플리케이션 데이터 흐름','Routing and Application Data Flow','하나의 화면을 여러 페이지의 서비스로 확장하는 방법','Expand one screen into a service with multiple pages')
topic(19,'URL과 페이지의 연결','Connecting URLs to Pages','경로, 동적 매개변수와 화면 선택','Paths, dynamic parameters, and page selection', '''
// app/products/[id]/page.jsx
export default async function ProductPage({ params }) {
  const { id } = await params;
  return <h1>상품 ID: {id}</h1>;
}
''', [('파일 기반 경로','File-based paths','app/products/[id]/page.jsx가 상품 상세 경로를 정의한다.','app/products/[id]/page.jsx defines the product detail route.'),('동적 매개변수','Dynamic parameters','[id] 부분의 URL 값은 params로 전달된다. 현재 App Router에서 await로 읽는다.','The [id] URL segment is provided through params, read with await in the current App Router.'),('관찰 결과','Observe','/products/p1 → “상품 ID: p1”, /products/p2 → “상품 ID: p2”.','/products/p1 displays “상품 ID: p1”; /products/p2 displays “상품 ID: p2”.')], [nextdoc('getting-started/layouts-and-pages')],P('Next.js App Router · 페이지 파일 전체','Next.js App Router · Complete page file'))
topic(20,'공통 레이아웃과 중첩 라우트','Shared Layouts and Nested Routes','여러 페이지가 공유하는 구조와 하위 화면 구성','Shared page structures and nested views', '''
// app/products/layout.jsx
import Link from 'next/link';
export default function ProductsLayout({ children }) {
  return <section>
    <nav><Link href="/products">상품 목록</Link></nav>
    <main>{children}</main>
  </section>;
}
''', [('레이아웃은 공통 구조','Layouts provide shared structure','상품 목록과 상세 페이지가 같은 메뉴를 사용한다.','Product list and detail pages share navigation.'),('중첩 경로와 children','Nested routes and children','프레임워크가 현재 하위 페이지를 children 위치에 구성한다. 루트 layout은 html·body를 포함한다.','The framework places the current nested page in children. The root layout includes html and body.'),('관찰 결과','Observe','목록에서 상세로 이동해도 상품 영역의 공통 메뉴는 유지된다.','Navigating from list to detail retains the shared product navigation.')], [nextdoc('getting-started/layouts-and-pages')],P('Next.js · 중첩 layout 파일 전체 / 루트 layout 별도','Next.js · Complete nested layout / root layout required separately'))
topic(21,'UI 상태와 서버 데이터','UI State and Server Data','검색 조건과 상품 데이터의 출처·수명·변경 책임','Origins, lifetimes, and ownership of filters and product data', '''
'use client';
import { useState } from 'react';
export default function ProductFilter({ products }) {
  const [query, setQuery] = useState('');
  const visible = products.filter(p =>
    p.name.includes(query)
  );
  return <>
    <input value={query}
      onChange={e => setQuery(e.target.value)} />
    <p>검색 결과: {visible.length}개</p>
  </>;
}
''', [('UI 상태','UI state','query는 이 화면에서 사용자가 입력하는 일시적인 값이다.','query is a temporary value entered by the user on this screen.'),('서버 데이터','Server data','products의 원본은 서버에 있다. 자식이 필터링해도 원본 저장 내용은 바뀌지 않는다.','The source of products lives on the server. Filtering in the child does not change stored data.'),('관찰 결과','Observe','입력은 결과 개수만 바꾼다. 상품 저장·수정은 별도의 서버 작업이 필요하다.','Typing changes the result count; storing or editing a product requires a server operation.')], [react('learn/thinking-in-react'),nextdoc('getting-started/fetching-data')],P('Next.js · Client Component 전체 / 서버에서 products 전달','Next.js · Complete Client Component / server supplies products'))
topic(22,'페이지에 필요한 데이터 조회','Fetching Page Data','라우트와 데이터 로딩의 연결','Connect a route to the data it needs', '''
// app/products/page.jsx
import { listProducts } from '@/lib/products';
export default async function ProductsPage() {
  const products = await listProducts();
  return <ul>{products.map(p =>
    <li key={p.id}>{p.name}</li>
  )}</ul>;
}
''', [('페이지가 필요한 데이터 선언','Declare data where it is needed','Server Component 페이지에서 조회를 기다린 뒤 UI를 반환한다.','The Server Component page awaits data before returning UI.'),('조회 계층의 역할','The data-access layer','listProducts는 서버 전용 DB 조회 함수다. DB 연결·실패 처리는 별도 구현한다.','listProducts is a server-only database query function. Connection and failure handling require a separate implementation.'),('관찰 결과','Observe','서버 조회 결과의 이름을 표시한다. 브라우저 useEffect가 서버 조회를 대신하지 않는다.','Displays names returned by the server query. A browser useEffect does not replace this server query.')], [nextdoc('getting-started/fetching-data')],P('Next.js · 구조 예시 / listProducts 구현 별도','Next.js · Structure example / listProducts implemented separately'))
topic(23,'데이터 변경과 화면 동기화','Mutations and UI Synchronization','저장·수정·삭제 이후 캐시와 데이터 재검증','Revalidate data and caches after saving, editing, or deleting', '''
'use server';
import { revalidatePath } from 'next/cache';
import { saveProduct } from '@/lib/products';
import { requireEditor } from '@/lib/auth';
export async function createProduct(formData) {
  await requireEditor();
  const name = String(formData.get('name') ?? '').trim();
  if (!name) return { error: '상품명을 입력하세요' };
  await saveProduct({ name });
  revalidatePath('/products');
  return { error: null };
}
''', [('변경과 조회는 다른 작업','Mutation and query differ','저장 성공만으로 모든 화면의 오래된 데이터가 자동 교체되지는 않는다.','A successful save does not automatically replace stale data everywhere.'),('재검증의 대상','Revalidation target','저장 후 /products 경로를 재검증한다. 실제 갱신 시점은 호출 위치·캐시 정책에 따라 달라진다.','Revalidate /products after saving; update timing depends on the call context and cache policy.'),('관찰할 흐름','Observe the flow','권한 검사 → 입력 검사 → 저장 → 재검증. 오류이면 저장과 재검증을 실행하지 않는다.','Authorization → validation → save → revalidate. A validation error skips saving and revalidation.')], [nextdoc('api-reference/functions/revalidatePath')],P('Next.js · Server Function 예시 / DB·권한 함수 별도','Next.js · Server Function example / DB and authorization helpers required'))
chapter(6,'렌더링 전략과 서버·클라이언트 경계','Rendering and Server–Client Boundaries','화면의 생성 시점과 코드의 실행 위치','When UI is generated and where code executes')
topic(24,'클라이언트 렌더링과 서버 렌더링','Client and Server Rendering','CSR·SSR·사전 렌더링의 화면 생성 과정','How CSR, SSR, and prerendering generate UI', '''
// CSR entry: browser execution
import { createRoot } from 'react-dom/client';
function App() { return <h1>상품 목록</h1>; }
createRoot(document.getElementById('root')).render(<App />);

// SSR API shape: separate server execution
import { renderToString } from 'react-dom/server';
const html = renderToString(<App />);
''', [('CSR: 브라우저에서 시작','CSR: begin in the browser','브라우저가 코드를 받아 UI를 구성한다. root 요소가 있는 HTML이 필요하다.','The browser receives code and builds UI. The HTML must include a root element.'),('SSR과 사전 렌더링','SSR and prerendering','SSR은 요청 시, 사전 렌더링은 요청 전에 HTML을 준비한다. Next.js는 경로와 정책에 따라 조합한다.','SSR prepares HTML on request; prerendering prepares it beforehand. Next.js combines these according to route policies.'),('코드의 실행 환경','Execution environments','위·아래 코드는 별도 환경의 API 비교다. renderToString 호출만으로 서버 서비스가 만들어지지는 않는다.','The blocks compare APIs in separate environments. Calling renderToString alone does not build a server service.')], [react('reference/react-dom/client/createRoot'),react('reference/react-dom/server/renderToString')],P('React DOM · 구조 비교 / 브라우저·서버 파일 분리','React DOM · API comparison / separate browser and server files'))
topic(25,'Hydration과 상호작용','Hydration and Interaction','서버에서 생성한 HTML과 브라우저 코드의 연결','Connect server-generated HTML to browser code', '''
// Shared component: server and browser
import { useState } from 'react';
function Quantity() {
  const [count, setCount] = useState(1);
  return <button onClick={() => setCount(c => c + 1)}>
    수량: {count}
  </button>;
}
// Browser entry after matching server HTML arrives
import { hydrateRoot } from 'react-dom/client';
hydrateRoot(document.getElementById('root'), <Quantity />);
''', [('HTML 표시와 상호작용 연결','HTML display and interactivity','서버가 Quantity의 초기 HTML을 보낸 뒤 브라우저가 같은 트리를 연결한다.','The server sends initial Quantity HTML; the browser attaches the same tree.'),('초기 결과의 일치','Matching initial output','서버 HTML과 브라우저의 첫 렌더가 일치해야 한다. 시간·난수·환경 분기에 주의한다.','Server HTML must match the first browser render. Time, randomness, and environment branches can cause mismatches.'),('관찰 결과','Observe','서버 HTML은 “수량: 1”을 먼저 보여주고 Hydration 후 클릭으로 2가 된다. Next.js는 연결을 관리한다.','Server HTML shows “수량: 1”; after hydration, a click gives 2. Next.js manages hydration.')], [react('reference/react-dom/client/hydrateRoot')],P('React DOM · 구조 예시 / 서버가 같은 Quantity HTML 제공','React DOM · Structure example / server supplies matching Quantity HTML'))
topic(26,'Server Components와 Client Components','Server and Client Components','서버의 데이터 처리와 브라우저의 상태·이벤트 분담','Split server data work from browser state and events', '''
// app/products/page.jsx — Server Component
import Quantity from './quantity';
import { listProducts } from '@/lib/products';
export default async function Page() {
  const products = await listProducts();
  return <>
    <h1>{products[0].name}</h1>
    <Quantity />
  </>;
}
// quantity.jsx starts with 'use client'
// Quantity is the state/event component from topic 08.
''', [('서버 컴포넌트','Server Component','기본 App Router 페이지는 서버에서 실행하며 DB에 접근할 수 있다. 브라우저용 상태·이벤트는 쓰지 않는다.','An App Router page runs on the server by default and can access a database. Browser state and events belong elsewhere.'),('클라이언트 경계','Client boundary','quantity.jsx 맨 위의 use client가 클라이언트 모듈 경계를 선언한다. 초기 HTML은 서버에서 준비될 수도 있다.','use client at the top of quantity.jsx declares a client module boundary. Its initial HTML may still be prepared on the server.'),('구분의 기준','Distinction','RSC는 코드 실행 경계이고 SSR은 HTML 생성 전략이다. 같은 의미로 사용하지 않는다.','RSC describes code execution boundaries; SSR is an HTML generation strategy.')], [nextdoc('getting-started/server-and-client-components'),react('reference/rsc/server-components')],P('Next.js · 구조 예시 / 별도 Quantity·조회 함수, 상품 1개 이상 가정','Next.js · Structure example / separate Quantity and query helper; assumes a product exists'))
topic(27,'서버·클라이언트 데이터 전달','Passing Data Across the Boundary','컴포넌트 경계, 직렬화와 서버 전용 정보','Serialization and server-only information at component boundaries', '''
// app/products/page.jsx — server
import ProductFilter from './product-filter';
import { listProducts } from '@/lib/products';
export default async function Page() {
  const products = await listProducts();
  const publicProducts = products.map(p => ({
    id: p.id, name: p.name, price: p.price
  }));
  return <ProductFilter products={publicProducts} />;
}
''', [('전달할 데이터 선택','Select data to pass','클라이언트에 필요한 필드만 전달한다. 비밀 키·내부 원가·DB 연결 객체는 제외한다.','Pass only required fields; exclude secrets, internal costs, and database connection objects.'),('직렬화 가능한 Props','Serializable props','React가 지원하는 직렬화 가능한 값을 전달한다. JSON에만 한정되지는 않는다.','Pass values supported by React serialization; this is not limited to JSON.'),('관찰 결과','Observe','주제 21의 ProductFilter가 받은 데이터로 브라우저에서 검색한다. 전달된 데이터는 사용자가 볼 수 있다.','ProductFilter from topic 21 filters the received data in the browser. Users can inspect data sent to the client.')], [nextdoc('getting-started/server-and-client-components'),nextdoc('guides/data-security')],P('Next.js · 구조 예시 / 주제 21 컴포넌트·DB 함수 별도','Next.js · Structure example / topic 21 component and DB helper required'))
chapter(7,'비동기 작업과 폼 제출','Async Work and Form Submission','대기·성공·실패를 포함하는 사용자 작업의 완성','Complete user tasks through waiting, success, and failure')
topic(28,'비동기 작업의 UI 상태','UI States for Async Work','로딩, 빈 결과, 제출 중과 실패 상태','Loading, empty results, pending submission, and failure', '''
export default function Results({ status, products }) {
  if (status === 'loading') return <p>조회 중</p>;
  if (status === 'error') return <p role="alert">조회 실패</p>;
  if (products.length === 0) return <p>검색 결과 없음</p>;
  return <ul>{products.map(p =>
    <li key={p.id}>{p.name}</li>
  )}</ul>;
}
''', [('상태에 따라 다른 화면','Different views for different states','조회 중과 실패는 빈 결과와 구분한다. 성공 후 항목이 없는 경우에만 빈 결과를 보여준다.','Distinguish loading and failure from empty results. Show empty only after a successful query with no items.'),('제출 중의 피드백','Submission feedback','조회 중은 읽기 작업, 제출 중은 변경 작업이다. 진행 표시와 중복 제출 방지를 함께 설계한다.','Loading concerns reads; pending submission concerns mutations. Provide progress feedback and prevent duplicate submission.'),('비교 입력','Compare inputs','loading → 조회 중, error → 조회 실패, success + [] → 검색 결과 없음.','loading → 조회 중; error → 조회 실패; success + [] → 검색 결과 없음.')], [react('learn/reacting-to-input-with-state')],P('React · 표시 컴포넌트 전체 / status·products는 부모가 관리','React · Complete display component / parent manages status and products'))
topic(29,'Suspense와 점진적 화면 표시','Suspense and Progressive Display','준비 중인 영역의 fallback과 스트리밍','Fallbacks and streaming for areas still being prepared', '''
// app/products/page.jsx
import { Suspense } from 'react';
import { listProducts } from '@/lib/products';
async function ProductList() {
  const products = await listProducts();
  return <p>{products.map(p => p.name).join(' · ')}</p>;
}
export default function Page() {
  return <>
    <h1>상품 목록</h1>
    <Suspense fallback={<p>상품 조회 중</p>}>
      <ProductList />
    </Suspense>
  </>;
}
''', [('경계 안의 준비 대기','Wait within a boundary','제목은 먼저 표시하고 데이터가 준비되는 목록에 fallback을 표시할 수 있다.','The title can appear first while a fallback covers the list waiting for data.'),('지원되는 데이터 연결','Supported data integration','App Router의 async Server Component 예시다. Effect 안의 fetch를 Suspense가 자동 감지하지 않는다.','This uses an async Server Component in App Router. Suspense does not automatically detect fetch inside an Effect.'),('관찰 결과','Observe','목록 조회가 대기하면 “상품 조회 중”을 거쳐 목록이 나타난다. 캐시·응답 속도에 따라 대기가 보이지 않을 수 있다.','A slow query may show “상품 조회 중” before the list. Cached or fast responses may hide the wait.')], [react('reference/react/Suspense'),nextdoc('getting-started/fetching-data')],P('Next.js · 페이지 구조 예시 / 조회 함수 별도','Next.js · Page structure example / query helper required'))
topic(30,'폼 제출과 Actions','Forms and Actions','입력 데이터 수집과 제출 결과·진행 상태 관리','Collect input and manage submission results and progress', '''
import { useActionState } from 'react';
async function validateName(previous, formData) {
  await new Promise(resolve => setTimeout(resolve, 500));
  const name = String(formData.get('name') ?? '').trim();
  return name ? `확인: ${name}` : '상품명을 입력하세요';
}
export default function ProductForm() {
  const [message, action, pending] = useActionState(
    validateName, ''
  );
  return <form action={action}>
    <input name="name" aria-label="상품명" />
    <button disabled={pending}>
      {pending ? '확인 중' : '확인'}
    </button>
    <p role="status">{message}</p>
  </form>;
}
''', [('FormData와 Action','FormData and an Action','name 속성으로 입력을 수집한다. action 함수는 폼 제출을 처리한다.','The name attribute identifies submitted fields. An action function handles form submission.'),('결과·진행 상태','Result and pending state','useActionState는 이전 결과·FormData를 함수에 전달하고 결과와 pending을 제공한다.','useActionState passes previous state and FormData, and exposes the result and pending state.'),('관찰 결과','Observe','제출 중 버튼이 비활성화되고 확인 결과가 표시된다. 이 예제는 지연·입력 확인만 하며 저장하지 않는다.','The button is disabled while pending, then shows the validation result. This example simulates delay and validates input without saving.')], [react('reference/react/useActionState'),react('reference/react-dom/components/form')],layout='compact')
topic(31,'서버의 데이터 변경과 검증','Server Mutations and Validation','Server Function·라우트 action의 역할과 입력·권한 검사','Server Functions, route actions, and input and permission checks', '''
'use server';
import { requireEditor } from '@/lib/auth';
import { saveProduct } from '@/lib/products';
export async function createProduct(previous, formData) {
  await requireEditor();
  const name = String(formData.get('name') ?? '').trim();
  if (!name || name.length > 40) {
    return { error: '상품명은 1~40자입니다' };
  }
  await saveProduct({ name });
  return { error: null };
}
''', [('서버에서도 검사','Validate on the server too','브라우저 검사는 우회 가능하다. 서버 진입점에서 인증·권한과 입력을 검사한다.','Browser checks can be bypassed. Check authentication, authorization, and inputs at the server entry point.'),('프레임워크의 변경 진입점','Framework mutation entry points','Next.js는 Server Function을, React Router는 라우트 action을 제공한다. 여기서는 Next.js API를 사용한다.','Next.js offers Server Functions; React Router offers route actions. This example uses Next.js APIs.'),('연결과 결과','Integration and results','주제 30의 action 함수 대신 연결할 때 초기 결과는 { error: null }로 맞춘다. 저장 후 재검증은 주제 23처럼 추가한다.','When replacing the topic 30 action, initialize state as { error: null }. Add post-save revalidation as in topic 23.')], [nextdoc('guides/data-security'),react('reference/rsc/use-server')],P('Next.js · Server Function 예시 / DB·권한 함수 별도','Next.js · Server Function example / DB and authorization helpers required'))
topic(32,'낙관적 UI와 오류 복구','Optimistic UI and Error Recovery','응답 전 화면 갱신과 실패 시 결과 처리','Update before the response and handle failure', '''
import { useOptimistic, useState } from 'react';
export default function Stock({ initial, saveStock }) {
  const [stocked, setStocked] = useState(initial);
  const [shown, show] = useOptimistic(stocked);
  const [error, setError] = useState('');
  async function action() {
    setError('');
    show(true);
    await saveStock(true)
      .then(setStocked)
      .catch(() => setError('저장 실패: 다시 시도하세요'));
  }
  return <form action={action}>
    <p>{shown ? '재고 있음' : '품절'}</p>
    <button>입고 처리</button>
    <p role="alert">{error}</p>
  </form>;
}
''', [('임시 표시와 확정 상태','Temporary view and confirmed state','useOptimistic은 Action 중 임시로 재고를 표시한다. 서버 응답을 받은 뒤 확정 상태를 갱신한다.','useOptimistic temporarily shows stock during an Action. Update confirmed state after the server response.'),('실패 시 복구','Recovery on failure','실패하면 확정 상태를 바꾸지 않는다. Action이 끝나면 표시가 확정 상태로 돌아가고 오류를 알린다.','On failure, leave confirmed state unchanged. When the Action ends, display returns to that state and shows the error.'),('비교 실험','Compare','initial=false에서 지연 성공은 품절 → 재고 있음 유지. 지연 실패는 재고 있음 → 품절 복구.','With initial=false, delayed success keeps 재고 있음; delayed failure restores 품절.')], [react('reference/react/useOptimistic')],P('React · 컴포넌트 전체 / saveStock은 Promise<boolean> 반환 또는 reject','React · Complete component / saveStock returns Promise<boolean> or rejects'),layout='compact')

assert len(SLIDES) == 40
assert [s['topic_number'] for s in SLIDES if s['kind'] == 'topic'] == list(range(1,33))
