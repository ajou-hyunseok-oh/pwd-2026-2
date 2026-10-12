"""Single-concept bodies, matched by ID to the approved title outline.

Blocks are selected explicitly per concept. No helper invents a second
definition, a fixed number of bullets, or a mandatory code/result block.
"""

def P(ko, en):
    return (ko, en)


def D(ko, en, *details):
    return dict(kind='concepts', items=[(P(ko, en), list(details))])


def K(ko, en, code, *, width=58, lang='jsx'):
    return dict(kind='code', label=P(ko, en), code=code, width=width, lang=lang)


def T(head, *rows):
    return dict(kind='table', head=head, rows=rows)


def S(*steps):
    return dict(kind='steps', items=steps)


def lifecycle_flow(phase):
    return dict(kind='image', src=f'materials/images/component-lifecycle-{phase}.svg',
                alt=P('Update는 0회 이상 선택적으로 반복되며 Render 결과는 Commit 전에 폐기될 수 있는 생명주기와 실행 시점',
                      'Lifecycle with zero or more Updates; render output may be discarded before commit; operation timing'))


BODIES = {}


def body(ident, *blocks, layout='split', refs=()):
    key = 'concept-' + ident
    assert key not in BODIES, key
    BODIES[key] = dict(blocks=list(blocks), layout=layout,
                       sources=[('Official documentation', url) for url in refs])


# Chapter 02 — Components and JSX
body('function-component',
    D('함수 컴포넌트 - UI를 반환하는 JavaScript 함수', 'Function component - A JavaScript function that returns UI',
      P('컴포넌트 이름은 대문자로 시작하는 함수 이름',
        'A component name is a function name starting with a capital letter'),
      P('함수 본문은 표시할 UI를 계산하는 영역',
        'The function body computes the UI to display'),
      P('return은 계산한 UI를 반환하는 구문',
        'return is the statement that returns the computed UI'),
      P('다른 컴포넌트는 이 이름을 태그로 사용해 UI 배치',
        'Another component uses this name as a tag to place the UI'),
      P('React는 태그에 대응하는 함수를 호출해 반환된 UI로 화면 구성',
        'React calls the function associated with the tag and composes the screen from its returned UI')),
    K('React · src/App.tsx', 'React · src/App.tsx', '''
function ProductTitle() {
  return <h2>상품 목록</h2>;
}
export default function App() {
  return (
    <section>
      <ProductTitle />
      <p>사과</p>
    </section>
  );
}
''', lang='tsx'),
    K('클래스 방식 · ProductTitle.tsx', 'Class syntax · ProductTitle.tsx', '''
import { Component } from 'react';
export default class ProductTitle extends Component {
  render() {
    return <h2>상품 목록</h2>;
  }
}
''', lang='tsx') | dict(caption=P('함수 컴포넌트 사용 권장 - Hooks로 상태 관련 로직을 쉽게 분리·재사용', 'Prefer function components - reuse stateful logic with Hooks')), refs=['https://react.dev/learn/your-first-component',
                         'https://react.dev/reference/react/Component',
                         'https://ko.react.dev/reference/react/Component'])

body('component-lifecycle',
    D('컴포넌트 생명주기 - 첫 표시·업데이트·제거에 따른 처리 흐름', 'Component lifecycle - Processing the first display, updates, and removal',
      P('Mount는 첫 표시, Update는 새로운 입력·내부 값에 따른 UI 재계산', 'Mount is the first display; Update recalculates UI from new inputs or internal values'),
      P('Render는 컴포넌트 함수를 실행해 UI 계산 · 결과 폐기 가능', 'Render calls the component to calculate UI; its output may be discarded'),
      P('Commit은 선택한 계산 결과를 DOM·참조에 반영', 'Commit applies the selected output to the DOM and refs'),
      P('Effect는 외부 동기화 시작 · 의존성이 바뀌면 이전 작업 정리 후 재시작', 'Effects start external synchronization; when dependencies change, React runs cleanup and restarts synchronization'),
      P('Unmount는 화면 제거 · 남아 있는 동기화 작업 정리', 'Unmount removes the UI and cleans up remaining synchronization'),
      P('Update는 0회 이상 반복 · 같은 계산 결과에는 DOM 변경 없음', 'Updates repeat zero or more times; identical output needs no DOM changes')),
    dict(kind='image', src='materials/images/function-component-lifecycle.svg',
         alt=P('Mount와 Update에서 Render, Commit, 레이아웃 Effect로 진행. Paint와 useEffect는 상황에 따라 순서가 다르며, 의존성 변경과 Unmount에서 Effect 정리. Render 폐기 경로와 선택적 Update 반복 포함',
               'Mount and Update lead to Render, Commit, and layout Effects. Paint and useEffect ordering varies. Cleanup on dependency changes or unmount; optional Updates and discarded renders are shown')),
    refs=['https://wavez.github.io/react-hooks-lifecycle/',
          'https://react.dev/learn/render-and-commit',
          'https://react.dev/reference/react/useEffect',
          'https://react.dev/reference/react/useLayoutEffect',
          'https://react.dev/learn/lifecycle-of-reactive-effects'])

BODIES['concept-component-lifecycle']['sources'][0] = (
    'Reference diagram · supplied Week 3 PDF, page 17',
    'https://wavez.github.io/react-hooks-lifecycle/')
BODIES['concept-component-lifecycle']['sources'].append((
    'Supplied Week 3 PDF · page 17',
    'materials/[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf'))

body('jsx',
    D('JSX - JavaScript 안에서 작성하는 UI 구조', 'JSX - UI structure written inside JavaScript',
      P('JavaScript 안에서 XML과 유사한 태그로 UI 구조를 표현하는 문법',
        'Syntax for expressing UI structure with XML-like tags inside JavaScript'),
      P('return 뒤의 JSX로 화면에 표시할 요소 정의', 'The JSX after return defines the elements to display'),
      P('태그의 중첩으로 화면 요소의 포함 관계 표현', 'Nested tags express containment between UI elements'),
      P('빌드 도구가 브라우저에서 실행할 JavaScript로 변환', 'Build tools transform JSX into JavaScript for the browser')),
    K('React · ProductTitle.tsx', 'React · ProductTitle.tsx', '''
export default function ProductTitle() {
  return (
    <section>
      <h2>상품 목록</h2>
      <p>사과</p>
    </section>
  );
}
''', lang='tsx'), refs=['https://react.dev/learn/writing-markup-with-jsx'])

body('jsx-expressions',
    D('중괄호 - JSX 안에 JavaScript 표현식을 넣는 표기', 'Braces - Syntax for embedding JavaScript expressions in JSX',
      P('변수 참조와 계산 결과를 요소의 내용으로 사용', 'Use a variable or a calculated value as element content'),
      P('if·for 같은 문장은 중괄호 안의 표현식으로 사용 불가', 'Statements such as if and for cannot be used as expressions here')),
    K('React · ProductPrice.tsx', 'React · ProductPrice.tsx', '''
export default function ProductPrice() {
  const name = '사과';
  const price = 1000;
  const quantity = 2;
  return <p>{name} · {price * quantity}원</p>;
}
''', lang='tsx'),
    K('사용 불가 · if·for 문장 직접 삽입',
      'Invalid · Direct if/for statements', '''
<p>{if (true) { '사과' }}</p>

<ul>{for (let i = 0; i < 3; i++) {
  <li>사과</li>
}}</ul>
''', lang='text'),
    K('사용 가능 · 조건은 삼항 연산자, 반복은 map()',
      'Valid · Ternary for conditions, map() for lists', '''
<p>{true ? '사과' : '품절'}</p>

<ul>{[1, 2, 3].map(id => (
  <li key={id}>사과</li>
))}</ul>
''', lang='text'), refs=[
    'https://react.dev/learn/conditional-rendering',
    'https://react.dev/learn/rendering-lists'])


body('jsx-tags',
    D('태그 구조 - 닫는 태그와 올바른 포함 관계', 'Tag structure - Closed tags and proper nesting',
      P('내용이 있는 요소는 시작·종료 태그를 쌍으로 작성', 'Pair opening and closing tags for elements with content'),
      P('내용이 없는 요소도 JSX에서는 명시적으로 닫기', 'Explicitly close elements without content in JSX')),
    T([P('작성 대상', 'Element'), P('JSX 표기', 'JSX syntax'), P('확인할 규칙', 'Rule')],
      [P('문구', 'Text'), P('<p>상품명</p>', '<p>상품명</p>'), P('시작·종료 태그의 이름 일치', 'Matching opening and closing tag names')],
      [P('입력 요소', 'Input'), P('<input />', '<input />'), P('자식이 없으면 자체 닫기', 'Self-close when there are no children')],
      [P('중첩 요소', 'Nesting'), P('<section><h2>상품</h2></section>', '<section><h2>상품</h2></section>'), P('안쪽 요소를 먼저 닫기', 'Close the inner element first')]),
    layout='single', refs=['https://react.dev/learn/writing-markup-with-jsx'])

body('jsx-attributes',
    D('JSX 속성 - 이름과 값으로 요소를 설정하는 방식', 'JSX attributes - Configure elements with names and values',
      P('문자열은 따옴표, JavaScript 값은 중괄호로 전달', 'Pass strings in quotes and JavaScript values in braces'),
      P('className - 요소에 적용할 CSS 클래스 이름 지정', 'className - Specify the CSS class name applied to an element'),
      P('htmlFor - label을 같은 id의 입력 요소와 연결', 'htmlFor - Associate a label with the input that has the matching id'),
      P('maxLength={40} - 숫자로 최대 입력 길이 지정', 'maxLength={40} - Set the maximum input length with a number'),
      P("style={{ color: 'green' }} - 객체로 CSS 속성 전달", "style={{ color: 'green' }} - Pass CSS properties as an object")),
    K('React · NameField.tsx', 'React · NameField.tsx', '''
export default function NameField() {
  return (
    <div className="field">
      <label htmlFor="name" style={{ color: 'green' }}>
        이름
      </label>
      <input id="name" type="text" maxLength={40} />
    </div>
  );
}
''', lang='tsx'),
    dict(kind='image', src='materials/images/jsx-name-field.png',
         alt=P('초록색 이름 레이블과 텍스트 입력란', 'Green name label and a text input'),
         caption=P('실행 결과', 'Rendered output')),
    layout='attributes', refs=['https://react.dev/learn/javascript-in-jsx-with-curly-braces'])

body('fragment',
    D('Fragment - 추가 DOM 요소 없이 여러 JSX 요소를 묶는 구조', 'Fragment - Group JSX elements without adding a DOM element',
      P('여러 JSX 요소를 함께 반환할 때 하나의 묶음으로 구성', 'Group multiple JSX elements to return them together'),
      P('<>...</>는 Fragment의 축약 표기', '<>...</> is shorthand for Fragment'),
      P('묶음 안의 요소만 DOM에 생성하며 형제 관계 유지', 'Only the grouped elements appear in the DOM, as siblings'),
      P('div와 달리 감싸는 DOM 요소를 추가하지 않음', 'Unlike div, Fragment adds no wrapper DOM element'),
      P('불필요한 묶음 없이 각 요소를 바로 배치', 'Arrange each element directly without an extra wrapper')),
    K('React · ProductSummary.tsx', 'React · ProductSummary.tsx', '''
export default function ProductSummary() {
  return (
    <>
      <h2>사과</h2>
      <p>1000원</p>
    </>
  );
}
''', lang='tsx'),
    K('생성된 DOM · 감싸는 요소 없이 형제 요소만 유지',
      'Resulting DOM · Sibling elements without a wrapper', '''
<h2>사과</h2>
<p>1000원</p>
''', lang='html'), refs=['https://react.dev/reference/react/Fragment'])

body('props',
    D('Props - 컴포넌트에 전달하는 입력 데이터', 'Props - Input data passed to a component',
      P('App에서 ProductName에 pName 값으로 상품명 전달', 'App passes a product name to ProductName through pName'),
      P('ProductName은 전달받은 값을 직접 변경하지 않고 UI 계산에 사용', 'ProductName uses the received values to calculate UI without mutating them'),
      P('기본값은 값이 없거나 undefined인 경우 적용', 'Defaults apply when a value is missing or undefined')),
    K('React · App.tsx', 'React · App.tsx', '''
type Props = { pName?: string };

function ProductName({ pName = '상품' }: Props) {
  return <p>{pName}</p>;
}
export default function App() {
  return (
    <section>
      <ProductName pName="사과" />
      <ProductName pName="용과" />
      <ProductName />
    </section>
  );
}
''', lang='tsx') | dict(result=[P('사과', '사과'), P('용과', '용과'), P('상품', '상품')]), refs=['https://react.dev/learn/passing-props-to-a-component'])

body('component-separation',
    D('설계 원칙 - 책임을 나누고 재사용·조합하기 쉬운 UI 구성', 'Design principles - UI units with clear responsibilities, reuse, and composition',
      P('단일 책임: 하나의 컴포넌트는 하나의 역할에 집중', 'Single responsibility: focus each component on one role'),
      P('재사용성: 여러 곳에서 같은 컴포넌트를 사용하도록 설계', 'Reusability: design a component for use in multiple places'),
      P('조합 가능성: 작은 컴포넌트를 조합해 전체 화면 구성', 'Composability: combine small components into a complete screen')),
    dict(kind='image', src='materials/images/component-separation.svg',
         alt=P('상품 검색 화면의 컴포넌트 분리 사례: 전체 화면 안에 검색 영역과 상품 목록, 상품 목록 안에 반복되는 상품 행',
               'Component separation example: a search area and product table inside the screen, with repeated rows inside the table')),
    T([P('분리 기준', 'When to separate'), P('판단할 상황', 'Situation')],
      [P('재사용', 'Reuse'), P('같은 UI를 여러 곳에서 사용해야 할 때', 'The same UI is needed in multiple places')],
      [P('복잡도', 'Complexity'), P('한 컴포넌트의 역할·로직이 복잡해질 때', 'A component has too many responsibilities or complex logic')],
      [P('성능', 'Performance'), P('화면 일부를 따로 최적화할 필요가 있을 때', 'Part of the UI needs separate optimization')],
      [P('테스트', 'Testing'), P('특정 UI·동작을 독립적으로 검증하고 싶을 때', 'A UI or behavior needs independent testing')]),
    refs=['https://react.dev/learn/thinking-in-react'])
BODIES['concept-component-separation']['sources'].append((
    'Provided lecture PDF (page 12)',
    'materials/%5BPWD%20Week%203%5D%20React%20프레임워크를%20이용한%20웹%20프론트엔드%20개발.pdf#page=12'))

body('component-files',
    D('파일 분리 - export와 import로 연결하는 컴포넌트', 'Component files - Components connected with export and import',
      P('export - 다른 파일에서 사용할 수 있도록 함수·변수·타입 등을 내보내는 예약어', 'export - A keyword that exposes functions, variables, types, and more for use in other files'),
      P('import - 다른 파일에서 내보낸 함수·변수·타입 등을 가져오는 예약어', 'import - A keyword that brings in functions, variables, types, and more exported from other files')),
    K('React · src/ProductRow.tsx', 'React · src/ProductRow.tsx', '''
export type Product = {
  id: string;
  name: string;
  price: number;
  stocked: boolean;
};
type RowProps = { product: Product };
export default function ProductRow({ product }: RowProps) {
  return (
    <tr>
      <td>{product.name}</td>
      <td>{product.price}달러</td>
    </tr>
  );
}
''', lang='tsx'),
    K('React · src/App.tsx', 'React · src/App.tsx', '''
import ProductRow from './ProductRow';
const apple = {
  id: 'apple', name: '사과', price: 1, stocked: true
};
export default function App() {
  return (
    <table>
      <tbody><ProductRow product={apple} /></tbody>
    </table>
  );
}
''', lang='tsx'), layout='modules', refs=['https://react.dev/learn/importing-and-exporting-components'])

body('children',
    D('children - 컴포넌트 태그 사이의 내용을 받는 Props', 'children - The prop that receives content between component tags',
      P('태그 사이에 넣은 JSX·텍스트 등을 children으로 전달', 'JSX, text, and other content between the tags are passed as children'),
      P('컴포넌트 내부의 {children} 위치에 전달받은 내용 표시', 'Display the received content at {children} inside the component'),
      P('공통 화면 틀을 재사용하면서 내부 내용은 사용하는 곳에서 지정', 'Reuse a common UI frame while specifying its content where it is used'),
      P('내용이 바뀌어도 화면 틀 코드를 다시 작성할 필요 없음', 'Changing the content requires no rewriting of the UI frame')),
    K('React · App.tsx', 'React · App.tsx', '''
import type { ReactNode } from 'react';
type PanelProps = { children: ReactNode };

function ProductPanel({ children }: PanelProps) {
  return <section>{children}</section>;
}

export default function App() {
  return (
    <ProductPanel>
      <h2>상품 목록</h2>
      <p>이름과 가격</p>
    </ProductPanel>
  );
}
''', lang='tsx'), refs=['https://react.dev/learn/passing-props-to-a-component'])

body('conditional-rendering',
    D('조건부 렌더링 - 조건에 따른 UI 선택', 'Conditional rendering - UI selected by a condition',
      P('데이터나 사용자 상태에 맞는 내용 표시', 'Display content suited to the data or user state'),
      P('필요한 요소만 표시하고 불필요한 요소는 숨김', 'Show only the elements needed and hide unnecessary ones'),
      P('하나의 컴포넌트로 여러 상황에 맞는 화면 구성', 'Use one component to present UI for different situations')),
    K('React · ProductRow.tsx / product는 부모가 전달', 'React · ProductRow.tsx / parent supplies product', '''
export type Product = {
  id: string;
  name: string;
  price: number;
  stocked: boolean;
};
type RowProps = { product: Product };
export default function ProductRow({ product }: RowProps) {
  const { name, stocked } = product;
  const label = stocked ? name : name + ' (품절)';
  return (
    <tr>
      <td>{label}</td>
      <td>{product.price}달러</td>
    </tr>
  );
}
''', width=64, lang='tsx'), layout='example', refs=['https://react.dev/learn/conditional-rendering'])

body('list-rendering',
    D('목록 렌더링 - 배열의 각 데이터를 같은 형태의 UI로 표시', 'List rendering - Display each array item with the same UI structure',
      P('map으로 각 데이터를 UI 요소로 변환해 순서대로 표시', 'Use map to transform each item into a UI element and display them in order'),
      P('항목마다 같은 UI 코드를 반복 작성할 필요 없음', 'Avoid writing the same UI code separately for every item'),
      P('배열의 항목 수에 맞춰 목록을 자동으로 구성', 'Build the list automatically to match the number of array items')),
    K('React · src/App.tsx', 'React · src/App.tsx', '''
const products = [
  { id: 'apple', pName: '사과' },
  { id: 'pear', pName: '배' }
];

export default function App() {
  return (
    <section>
      {products.map(item => (
        <p key={item.id}>{item.pName}</p>
      ))}
    </section>
  );
}
''', lang='tsx') | dict(result=[P('사과', '사과'), P('배', '배')]),
    refs=['https://react.dev/learn/rendering-lists'])

body('list-key',
    D('key - React가 목록의 각 항목을 식별하는 값', 'key - A value React uses to identify each list item',
      P('같은 목록 안에서 고유하고 변하지 않는 ID 사용', 'Use an ID that is unique within the list and remains stable'),
      P('항목의 추가·삭제·순서 변경 전후에 같은 항목을 연결', 'Match the same items before and after insertion, deletion, or reordering'),
      P('입력값·상태가 다른 항목과 뒤섞이지 않도록 유지', 'Keep input values and state associated with the correct item'),
      P('React가 사용하는 특수 Props로, 컴포넌트 내부에서 직접 읽을 수 없음', 'A special prop used by React that cannot be read directly inside the component')),
    K('React · src/App.tsx', 'React · src/App.tsx', '''
const products = [
  { id: 'apple', pName: '사과' },
  { id: 'pear', pName: '배' }
];

export default function App() {
  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>{product.pName}</li>
      ))}
    </ul>
  );
}
''', lang='tsx'), layout='example', refs=['https://react.dev/learn/rendering-lists'])

body('static-product-ui',
    D('정적 구현 - 사용자 동작을 연결하기 전 화면을 완성하는 단계', 'Static implementation - Build the UI before connecting user interactions',
      P('화면에 필요한 요소와 배치를 먼저 구성', 'First define the elements and layout the UI needs'),
      P('화면 구조와 표시 내용을 미리 확인하고 수정 가능', 'Review and refine the UI structure and content early'),
      P('화면 구성과 동작 구현을 나눠 개발 복잡도 감소', 'Reduce development complexity by separating UI construction from interaction logic'),
      P('입력란·체크박스를 조작해도 목록을 바꾸는 기능은 아직 연결하지 않음', 'Inputs and checkboxes are not yet connected to logic that changes the list')),
    K('React · src/App.tsx', 'React · src/App.tsx', '''
export default function App() {
  return (
    <main>
      <input placeholder="상품 검색" />
      <label>
        <input type="checkbox" /> 재고만 보기
      </label>
      <ul>
        <li>사과 · 1달러</li>
        <li>배 · 2달러</li>
      </ul>
    </main>
  );
}
''', lang='tsx'),
    dict(kind='image', src='materials/images/static-product-ui.png',
         alt=P('상품 검색 입력란과 재고만 보기 체크박스 아래에 사과 1달러와 배 2달러 목록이 표시된 실행 화면',
               'Rendered UI with a product search input, an in-stock checkbox, and a list showing apple for 1 dollar and pear for 2 dollars'),
         caption=P('실행 결과', 'Rendered output')),
    layout='attributes', refs=['https://react.dev/learn/thinking-in-react'])


# Chapter 03 — State-based UI updates
body('event-handler',
    D('이벤트 핸들러 - 사용자 행동이 발생할 때 실행되는 함수', 'Event handler - A function that runs when a user action occurs',
      P('클릭·입력 같은 이벤트에 실행할 함수를 연결', 'Connect a function to an event such as a click or input'),
      P('사용자 행동에 반응하는 상호작용 구현', 'Implement interactions that respond to user actions'),
      P('화면 구조와 동작을 처리하는 로직을 구분해 관리', 'Manage UI structure separately from the logic that handles actions')),
    K('React · AddButton.jsx', 'React · AddButton.jsx', '''
export default function AddButton() {
  function handleClick() {
    alert('상품을 선택했습니다');
  }
  return (
    <button onClick={handleClick}>
      상품 선택
    </button>
  );
}
'''),
    T([P('상황', 'Situation'), P('대표 핸들러', 'Handlers'), P('구체적인 사례', 'Example')],
      [P('클릭', 'Click'), P('onClick', 'onClick'), P('버튼을 눌러 상품 선택', 'Select a product with a button')],
      [P('마우스 진입·이탈', 'Mouse enter / leave'), P('onMouseEnter · onMouseLeave', 'onMouseEnter · onMouseLeave'), P('마우스 포인터가 요소 안으로 들어오거나 밖으로 나감', 'Move the pointer into or out of an element')],
      [P('키보드 입력', 'Keyboard'), P('onKeyDown · onKeyUp', 'onKeyDown · onKeyUp'), P('키를 누르거나 뗌', 'Press or release a key')],
      [P('포커스 이동', 'Focus'), P('onFocus · onBlur', 'onFocus · onBlur'), P('입력란을 선택하거나 다른 곳으로 이동', 'Focus an input or move away')],
      [P('입력값 변경', 'Value change'), P('onChange', 'onChange'), P('검색어 수정·체크박스 선택 변경', 'Edit search text or toggle a checkbox')],
      [P('폼 제출', 'Form submit'), P('onSubmit', 'onSubmit'), P('제출 버튼이나 Enter로 폼 제출', 'Submit a form with a button or Enter')]),
    refs=['https://react.dev/learn/responding-to-events',
          'https://react.dev/reference/react-dom/components/common',
          'https://react.dev/reference/react-dom/components/input'])

body('state',
    K('사용 구조', 'Usage structure', '''
const [state, setState] = useState(initialState);
''') | dict(hide_label=True),
    D('useState - 함수 컴포넌트에 상태를 추가하는 React 함수', 'useState - A React function that adds state to a function component',
      P('initialState: 처음 화면을 만들 때 사용할 초깃값', 'initialState: the initial value used for the first render'),
      P('state: 반환 배열의 첫 번째 항목인 현재 상태 값', 'state: the first array item, containing the current state'),
      P('setState: 반환 배열의 두 번째 항목인 상태 변경 함수', 'setState: the second array item, a function that updates state'),
      P('[state, setState]: 배열 구조 분해로 두 반환값을 순서대로 받는 문법', '[state, setState]: array destructuring that reads both returned items in order'),
      P('변수 이름은 직접 정하며 두 항목의 역할은 순서로 결정', 'Choose variable names freely; their positions determine their roles'),
      P('setState(다음 값) 호출로 다음 상태와 화면 갱신 요청', 'Call setState(nextValue) to request the next state and a UI update')),
    K('React · Quantity.jsx', 'React · Quantity.jsx', '''
import { useState } from 'react';

export default function Quantity() {
  const [quantity, setQuantity] = useState(1);
  return (
    <button onClick={() => setQuantity(quantity + 1)}>
      수량: {quantity}
    </button>
  );
}
''') | dict(result=[P('수량: 1 → 클릭 → 수량: 2 → 클릭 → 수량: 3', '수량: 1 → click → 수량: 2 → click → 수량: 3')]),
    refs=['https://react.dev/learn/state-a-components-memory', 'https://react.dev/reference/react/useState'])

body('render',
    D('Render - 현재 값으로 다음 UI를 계산하는 단계', 'Render - Calculate the next UI from current values',
      P('컴포넌트 함수를 실행해 현재 Props·State에 맞는 JSX 계산', 'Calculate JSX from current props and state'),
      P('Mount에서는 첫 UI 계산, Update에서는 현재 값으로 UI 다시 계산', 'Mount: calculate the first UI · Update: recalculate UI'),
      P('Render 결과는 폐기될 수 있으며, 실제 반영할 결과만 Commit으로 전달', 'Render output may be discarded without a commit'),
      P('계산 결과가 같으면 DOM 변경 없음', 'Identical output needs no DOM changes'),
      P('같은 입력에는 같은 결과 반환 · Render 중 외부 데이터 변경 금지', 'Keep render pure: same inputs, same output; do not mutate external data during render')),
    K('React · Quantity.jsx', 'React · Quantity.jsx', '''
import { useState } from 'react';

export default function Quantity() {
  const [quantity, setQuantity] = useState(1);
  console.log('Render:', quantity);
  return (
    <button onClick={() => setQuantity(quantity + 1)}>
      수량: {quantity}
    </button>
  );
}
''') | dict(result_label=P('콘솔 · 프로덕션 실행 예시 · 최초 표시 후 두 번 클릭', 'Console · Production run · Initial render and two clicks'),
           result=[P('Render: 1', 'Render: 1'), P('Render: 2', 'Render: 2'), P('Render: 3', 'Render: 3'),
                   P('개발 StrictMode: 각 Render 로그 두 번 출력', 'Development StrictMode: each Render log appears twice')]),
    lifecycle_flow('render'),
    refs=['https://react.dev/learn/render-and-commit', 'https://react.dev/reference/react/Component#render', 'https://react.dev/reference/react/StrictMode'])

body('commit',
    D('Commit - 계산한 UI를 실제 DOM에 반영하는 단계', 'Commit - Apply the calculated UI to the actual DOM',
      P('Mount: Render로 계산한 첫 UI의 DOM을 문서에 연결', 'Mount: attach the DOM for the first UI calculated during render'),
      P('Update: Render 결과에서 달라진 부분만 DOM에 반영', 'Update: apply only differences in the render output to the DOM'),
      P('Unmount: 해당 컴포넌트의 DOM을 문서에서 제거', 'Unmount: remove that component’s DOM from the document'),
      P('변경된 DOM을 브라우저가 그려 현재 상태에 맞는 화면 표시', 'The browser paints the updated DOM to display the current state')),
    dict(kind='image', src='materials/images/commit-before.png',
         alt=P('클릭 전 수량: 1을 표시하는 버튼', 'Button displaying 수량: 1 before the click'),
         caption=P('Commit 전 · 수량: 1', 'Before commit · 수량: 1')),
    dict(kind='image', src='materials/images/commit-after.png',
         alt=P('클릭 후 같은 버튼에 수량: 2를 표시하는 화면', 'The same button displaying 수량: 2 after the click'),
         caption=P('Commit 후 · 같은 버튼의 텍스트를 수량: 2로 변경', 'After commit · Update the same button’s text to 수량: 2')),
    lifecycle_flow('commit'),
    layout='attributes', refs=['https://react.dev/learn/render-and-commit'])

body('state-snapshot',
    D('상태 스냅샷 - 하나의 렌더에서 참조하는 고정된 상태 값', 'State snapshot - The fixed state values used by a particular render',
      P('React는 화면을 만들 때 컴포넌트에 그 시점의 상태 값을 제공', 'React provides the component with the current state values when creating the UI'),
      P('상태 변경 함수는 현재 실행의 값을 바꾸지 않고 다음 렌더를 요청', 'A state setter requests the next render without changing values in the current execution'),
      P('기존 핸들러와 타이머는 만들어질 때 받은 이전 값을 계속 참조', 'Existing handlers and timers continue to refer to the values from the render that created them'),
      P('이벤트 처리 도중 값이 바뀌지 않아 같은 기준으로 계산 가능', 'Values remain stable during event handling, so calculations use a consistent basis')),
    K('React · Counter.jsx', 'React · Counter.jsx', '''
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  function handleClick() {
    setCount(count + 1);
    setTimeout(() => alert(count), 1000);
  }
  return <button onClick={handleClick}>{count}</button>;
}
''') | dict(result_label=P('실행 결과 · 최초 표시 후 한 번 클릭', 'Rendered output · Initial display and one click'),
           result=[P('버튼: 0 → 클릭 → 1', 'Button: 0 → click → 1'),
                   P('1초 뒤 알림: 0', 'Alert after one second: 0')]),
    refs=['https://react.dev/learn/state-as-a-snapshot'])

body('state-updater',
    D('함수형 상태 업데이트 - 이전 상태를 받아 다음 상태를 계산하는 방식', 'Functional state update - Calculate the next state from the previous state',
      P('상태 변경 함수에 다음 값 대신 계산 함수를 전달', 'Pass a calculation function to the state setter instead of the next value'),
      P('React는 각 함수에 앞선 업데이트까지 반영한 상태 값을 전달', 'React passes each function the state resulting from preceding updates'),
      P('여러 변경 요청을 순서대로 누적해 이전 상태에 따른 갱신 가능', 'Accumulate multiple update requests in order when the next state depends on previous state'),
      P('계산 함수는 다음 상태를 반환하며 외부 데이터를 변경하지 않음', 'The calculation function returns the next state without changing external data')),
    K('React · Counter.jsx', 'React · Counter.jsx', '''
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  function increment() {
    setCount(c => c + 1);
    setCount(c => c + 1);
  }
  return <button onClick={increment}>{count}</button>;
}
''') | dict(result_label=P('실행 결과 · 최초 표시 후 한 번 클릭', 'Rendered output · Initial display and one click'),
           result=[P('상태 계산: 0 → 1 → 2', 'State calculation: 0 → 1 → 2'),
                   P('버튼: 0 → 클릭 → 2', 'Button: 0 → click → 2')]),
    refs=['https://react.dev/learn/queueing-a-series-of-state-updates'])

body('state-immutability',
    D('상태 불변성 - 기존 상태를 직접 수정하지 않고 새 값으로 교체하는 원칙', 'State immutability - Replace state with a new value without mutating the existing state',
      P('배열·객체 상태는 변경 내용을 담은 새 배열·객체로 갱신', 'Update array and object state using new arrays and objects containing the changes'),
      P('직접 수정하면 React가 변경을 놓치거나 이전 렌더의 값이 바뀔 수 있음', 'Direct mutation can cause React to miss changes or alter values used by earlier renders'),
      P('이전 상태를 보존해 지난 렌더에서 사용한 값의 변경 방지', 'Preserve previous state so values used by earlier renders remain unchanged'),
      P('새 참조를 전달해 React가 상태 변경을 인식할 수 있도록 함', 'Pass a new reference so React can recognize the state change'),
      P('변경하지 않은 항목은 기존 객체를 재사용해 불필요한 복사 감소', 'Reuse unchanged objects to avoid unnecessary copying')),
    K('React · Stock.jsx', 'React · Stock.jsx', '''
import { useState } from 'react';

export default function Stock() {
  const [products, setProducts] = useState([
    { id: 'p1', name: '사과', stocked: false }
  ]);
  function restock() {
    setProducts(items => items.map(product =>
      product.id === 'p1'
        ? { ...product, stocked: true }
        : product
    ));
  }
  const { stocked } = products[0];
  const label = stocked ? '재고 있음' : '품절';
  return <button onClick={restock}>{label}</button>;
}
''', width=58) | dict(result_label=P('실행 결과 · 최초 표시 후 한 번 클릭', 'Rendered output · Initial display and one click'),
                     result=[P('버튼: 품절 → 클릭 → 재고 있음', 'Button: 품절 → click → 재고 있음')]),
    refs=['https://react.dev/learn/updating-arrays-in-state', 'https://react.dev/learn/updating-objects-in-state'])

body('derived-values',
    D('파생값 - 기존 입력이나 상태에서 계산하는 값', 'Derived value - A value calculated from existing inputs or state',
      P('계산에 필요한 원본 데이터와 변경 가능한 조건만 보관', 'Keep only the source data and conditions that can change'),
      P('결과 목록·개수처럼 계산 가능한 값은 렌더할 때 구함', 'Calculate values such as result lists and counts during render'),
      P('같은 정보를 상태에 중복 저장하지 않아 갱신 누락 방지', 'Avoid duplicated state to prevent missed updates'),
      P('원본이나 조건이 바뀌면 계산 결과도 함께 바뀌어 데이터 일관성 유지', 'Keep data consistent by recalculating results when the source or conditions change')),
    K('React · Search.jsx', 'React · Search.jsx', '''
import { useState } from 'react';

export default function Search() {
  const products = ['사과', '배'];
  const [query, setQuery] = useState('');
  const visible = products.filter(pName =>
    pName.includes(query)
  );
  return (
    <>
      <button onClick={() => setQuery('사과')}>검색</button>
      <p>{visible.join(' · ')} · {visible.length}개</p>
    </>
  );
}
''') | dict(result_label=P('실행 결과 · 검색 버튼 한 번 클릭', 'Rendered output · Click the search button once'),
           result=[P('사과 · 배 · 2개 → 검색 클릭 → 사과 · 1개', '사과 · 배 · 2개 → click search → 사과 · 1개')]),
    refs=['https://react.dev/learn/thinking-in-react', 'https://react.dev/learn/choosing-the-state-structure'])

body('controlled-inputs',
    D('제어 입력 - React의 상태로 입력란의 현재 값을 관리하는 방식', 'Controlled input - Manage an input’s current value with React state',
      P('문자 입력은 value, 체크박스는 checked로 상태와 연결', 'Connect state through value for text inputs and checked for checkboxes'),
      P('onChange에서 사용자의 변경을 받아 상태 갱신', 'Update state from user changes received through onChange'),
      P('갱신된 상태를 다시 표시해 입력란과 데이터의 값 일치', 'Display updated state to keep the input and data in sync'),
      P('입력값을 React에서 관리해 검사·초기화·다른 UI와 공유 가능', 'Manage input values in React for validation, resetting, and sharing with other UI'),
      P('입력란의 표시 값과 프로그램이 사용하는 상태를 일치시켜, 입력 처리와 초기화를 일관되게 관리', 'Keep displayed input values aligned with program state to manage input handling and resetting consistently')),
    K('React · SearchBar.jsx', 'React · SearchBar.jsx', '''
import { useState } from 'react';

export default function SearchBar() {
  const [text, setText] = useState('');
  const [stock, setStock] = useState(false);
  return (
    <section>
      <input value={text} onChange={e => setText(e.target.value)} />
      <label>
        <input type="checkbox" checked={stock}
          onChange={e => setStock(e.target.checked)} />
        재고만 보기
      </label>
    </section>
  );
}
''', width=70) | dict(result_label=P('실행 결과 · 사과 입력 후 체크박스 선택', 'Rendered output · Type 사과 and select the checkbox'),
                     result=[P('입력란: 사과 · 재고만 보기 체크박스: 선택됨', 'Text input: 사과 · In-stock checkbox: selected')]),
    layout='example', refs=['https://react.dev/reference/react-dom/components/input'])

body('lifting-state',
    D('상태 끌어올리기 - 여러 컴포넌트가 함께 쓰는 상태를 공통 부모 컴포넌트에서 관리', 'Lifting state up - Manage shared state in a common parent component',
      P('여러 컴포넌트가 함께 쓰는 상태를 한 곳에 보관', 'Keep state shared by several components in one place'),
      P('상태 값과 변경 함수를 필요한 컴포넌트에 Props로 전달', 'Pass state values and update callbacks as props to the components that need them'),
      P('각 컴포넌트는 전달받은 값으로 표시하고 변경 함수로 갱신 요청', 'Each component displays the received values and requests updates through callbacks'),
      P('같은 상태를 기준으로 동작해 중복 저장과 값 불일치 방지', 'Use the same state to avoid duplicate storage and inconsistent values')),
    K('React · App.jsx', 'React · App.jsx', '''
import { useState } from 'react';

function QuantityButton({ value, onAdd }) {
  return <button onClick={onAdd}>추가: {value}</button>;
}
function QuantityDisplay({ value }) {
  return <p>수량: {value}</p>;
}
export default function App() {
  const [quantity, setQuantity] = useState(0);
  const add = () => setQuantity(quantity + 1);
  return (
    <>
      <QuantityButton value={quantity} onAdd={add} />
      <QuantityDisplay value={quantity} />
    </>
  );
}
''', width=68) | dict(result_label=P('실행 결과 · 추가 버튼 한 번 클릭', 'Rendered output · Click the add button once'),
                     result=[P('버튼: 추가: 0 → 추가: 1 · 수량 표시: 0 → 1', 'Button: 추가: 0 → 추가: 1 · Quantity display: 0 → 1')]),
    layout='example', refs=['https://react.dev/learn/sharing-state-between-components'])

body('state-preservation',
    D('상태 보존 - Props가 바뀌어도 기존 상태를 이어서 사용', 'State preservation - Keep using existing state when props change',
      P('React는 상태를 컴포넌트 함수 바깥에 컴포넌트별로 저장', 'React stores state outside component functions, separately for each component'),
      P('같은 위치의 같은 타입이면 기존 컴포넌트로 인식해 저장된 상태 연결', 'The same type at the same position is recognized as the existing component and linked to its stored state'),
      P('Props 변경으로 함수를 다시 실행해도 useState는 저장된 현재 상태를 반환', 'When a prop change reruns the function, useState returns the stored current state'),
      P('초깃값은 새 컴포넌트를 만들 때만 사용하므로 기존 상태가 초기화되지 않음', 'The initial value is used only when creating a new component, so existing state is not reset')),
    K('React · App.jsx', 'React · App.jsx', '''
import { useState } from 'react';

function Counter({ label }) {
  const [count, setCount] = useState(0);
  const increment = () => setCount(count + 1);
  const text = `${label}: ${count}`;
  return <button onClick={increment}>{text}</button>;
}

export default function App() {
  const [label, setLabel] = useState('수량');
  const rename = () => setLabel('상품 수량');
  return (
    <>
      <button onClick={rename}>이름 변경</button>
      <Counter label={label} />
    </>
  );
}
''', width=68) | dict(result_label=P('실행 결과 · 수량 두 번 클릭 후 이름 변경', 'Rendered output · Click the counter twice, then rename'),
                     result=[P('수량: 0 → 수량: 2 → 상품 수량: 2', '수량: 0 → 수량: 2 → 상품 수량: 2')]),
    layout='example', refs=['https://react.dev/learn/preserving-and-resetting-state'])

body('state-reset-key',
    D('key를 이용한 상태 초기화 - 다른 key의 컴포넌트를 새로 생성', 'Reset state with a key - Create a new component for a different key',
      P('key는 같은 위치에서 컴포넌트를 구별하는 식별값', 'A key identifies components at the same position'),
      P('key가 바뀌면 기존 컴포넌트의 상태를 버리고 새 상태 생성', 'Changing the key discards the existing component’s state and creates new state'),
      P('새 컴포넌트의 useState는 초깃값부터 다시 시작', 'The new component’s useState starts again from its initial value'),
      P('편집 대상을 바꿀 때 이전 대상의 임시 입력이 남는 문제 방지', 'Prevent temporary input from the previous item from remaining when switching items')),
    K('React · App.jsx', 'React · App.jsx', '''
import { useState } from 'react';

function Editor({ pName }) {
  const [draft, setDraft] = useState(pName);
  const change = e => setDraft(e.target.value);
  return <input value={draft} onChange={change} />;
}

export default function App() {
  const [pName, setPName] = useState('사과');
  const selectPear = () => setPName('배');
  return (
    <>
      <button onClick={selectPear}>배 선택</button>
      <Editor key={pName} pName={pName} />
    </>
  );
}
''', width=68) | dict(result_label=P('실행 결과 · 입력 수정 후 배 선택', 'Rendered output · Edit the input, then select pear'),
                     result=[P('입력란: 사과 → 사과 수정 중 → 배', 'Input: 사과 → 사과 수정 중 → 배')]),
    layout='example', refs=['https://react.dev/learn/preserving-and-resetting-state'])

# Chapter 04 — Hooks
body('hook-introduction',
    D('Hook - 함수 컴포넌트에서 React 기능을 사용하는 함수', 'Hook - A function for using React features in function components',
      P('2018년 공개, 2019년 2월 6일 React 16.8에서 정식 지원', 'Introduced in 2018; stable support released in React 16.8 on February 6, 2019'),
      P('도입 배경: 클래스 방식의 분산된 상태 관련 코드는 이해와 재사용이 어려움', 'Motivation: stateful logic scattered across class methods was hard to understand and reuse'),
      P('목적: 클래스 없이 React 기능을 사용하고 관련 로직을 함수로 묶어 재사용', 'Purpose: use React features without classes and group related logic into reusable functions'),
      P('useState 호출: Mount의 Render에서 초기 상태 준비, Update의 Render에서 현재 상태 반환', 'useState calls: prepare initial state in the mount render; return current state in update renders'),
      P('Unmount에서는 React가 해당 컴포넌트의 상태 제거', 'On unmount, React discards that component’s state')),
    lifecycle_flow('state'),
    refs=['https://react.dev/reference/react/hooks',
          'https://react.dev/learn/preserving-and-resetting-state',
          'https://legacy.reactjs.org/docs/hooks-intro.html',
          'https://legacy.reactjs.org/blog/2019/02/06/react-v16.8.0.html'])

body('hook-rules',
    D('Hook 호출 규칙 - 렌더마다 같은 순서로 호출', 'Hook call rules - Call Hooks in the same order on every render',
      P('useState 같은 Hook은 Render 중 컴포넌트 함수의 최상위에서 호출', 'Call Hooks such as useState at the top level of a component function during render'),
      P('조건문·반복문·이벤트 핸들러 안과 조건부 return 뒤에서는 호출 금지', 'Do not call Hooks inside conditions, loops, or event handlers, or after a conditional return'),
      P('React는 호출 순서를 기준으로 각 Hook과 저장된 상태를 연결', 'React uses call order to associate each Hook with its stored state'),
      P('호출이 생략되거나 순서가 바뀌면 상태 연결이 어긋나 오류 발생 가능', 'Skipping calls or changing their order can break state associations and cause errors')),
    K('올바른 코드 · return 전에 Hook 호출', 'Correct · Call the Hook before the return', '''
import { useState } from 'react';

export default function Search({ hidden }) {
  const [query, setQuery] = useState('');
  const change = e => setQuery(e.target.value);
  if (hidden) return null;
  return <input value={query} onChange={change} />;
}
''', width=68),
    K('잘못된 코드 · return 뒤에서 Hook 호출', 'Incorrect · Call the Hook after the return', '''
import { useState } from 'react';

export default function Search({ hidden }) {
  if (hidden) return null;
  const [query, setQuery] = useState('');
  const change = e => setQuery(e.target.value);
  return <input value={query} onChange={change} />;
}
''', width=68),
    layout='attributes', refs=['https://react.dev/reference/rules/rules-of-hooks', 'https://react.dev/learn/state-a-components-memory'])

body('ref',
    D('Ref - 렌더가 반복돼도 유지되는 값이나 DOM 참조의 저장 공간', 'Ref - Values or DOM references retained across renders',
      P('useRef가 반환한 객체의 current에 값이나 DOM 참조 보관', 'Store a value or DOM reference in the current property of the object returned by useRef'),
      P('저장한 DOM 참조로 포커스 이동·스크롤 등 직접 제어', 'Use stored DOM references to control focus and scrolling')),
    K('React · SearchFocus.jsx', 'React · SearchFocus.jsx', '''
import { useRef } from 'react';

export default function SearchFocus() {
  const inputRef = useRef(null);
  return <>
    <input ref={inputRef} aria-label="검색어" />
    <button onClick={() => inputRef.current.focus()}>
      검색어 입력
    </button>
  </>;
}
''') | dict(result_figure=dict(kind='image', src='materials/images/ref-focus-result.png',
         alt=P('검색어 입력 버튼을 누른 뒤 검색 입력란에 포커스가 이동한 화면', 'Search input focused after clicking the 검색어 입력 button'),
         caption=P('실행 결과 · 버튼 클릭 → 입력란에 포커스 이동', 'Result · Click the button → focus moves to the input'))), T([P('구분', 'Aspect'), P('useState', 'useState'), P('useRef', 'useRef')],
      [P('용도', 'Purpose'), P('화면 계산에 사용하는 값', 'Values used to calculate UI'), P('화면 계산에 쓰지 않는 값·DOM 참조', 'Nonvisual values / DOM refs')],
      [P('값 읽기', 'Read'), P('상태 변수', 'State variable'), P('ref.current', 'ref.current')],
      [P('값 변경', 'Update'), P('상태 변경 함수 호출', 'Call the state setter'), P('ref.current에 직접 대입', 'Assign to ref.current')],
      [P('렌더 요청', 'Re-render'), P('다른 값으로 변경 시 요청', 'Requested for a different value'), P('값 변경만으로 요청하지 않음', 'Changing current does not request one')],
      [P('사용 예', 'Examples'), P('수량·검색어·선택 여부', 'Quantity / query / selection'), P('입력 DOM·타이머 ID', 'Input DOM / timer ID')]),
    refs=['https://react.dev/learn/referencing-values-with-refs', 'https://react.dev/reference/react/useRef', 'https://react.dev/learn/manipulating-the-dom-with-refs'])

body('effect',
    D('Effect - React 외부 시스템을 현재 값에 맞춰 동기화하는 작업', 'Effect - Synchronize an external system with current values',
      P('브라우저 기능·타이머·서버 연결 등 React 밖의 작업 처리', 'Work with browser APIs, timers, and server connections'),
      P('DOM 반영 뒤 동기화해 화면과 외부 시스템의 값 일치', 'Synchronize after commit to keep UI and external values consistent'),
      P('컴포넌트가 유지되는 동안에도 동기화 시작·중지 주기 반복 가능', 'Synchronization can start and stop repeatedly while mounted'),
      P('렌더에서 계산 가능한 값에는 Effect 불필요', 'Values calculable during render do not need an Effect')),
    K('React · ProductTitle.jsx', 'React · ProductTitle.jsx', """
import { useEffect } from 'react';

export default function ProductTitle() {
  const pName = '사과';
  useEffect(() => {
    document.title = `상품: ${pName}`;
  });
  return <h2>{pName}</h2>;
}
""") | dict(result_figure=dict(kind='image', src='materials/images/effect-title-result.png',
         alt=P('화면에 사과를 표시하는 실행 결과', 'Rendered output displaying 사과'),
         caption=P('실행 결과 · 화면: 사과 / 브라우저 탭 제목: 상품: 사과', 'Result · UI: 사과 / Browser tab title: 상품: 사과'))),
    refs=['https://react.dev/reference/react/useEffect', 'https://react.dev/learn/lifecycle-of-reactive-effects'])

body('effect-dependencies',
    D('의존성 배열 - Effect에서 사용하는 Props·State 등을 적는 목록', 'Dependency array - A list of props, state, and other values used by an Effect',
      P('처음 화면이 표시되면 Effect 실행', 'Run the Effect when the screen first appears'),
      P('이후에는 배열의 값을 이전 값과 비교해, 달라진 값이 있으면 다시 실행', 'Then compare the listed values with their previous values and rerun if any changed'),
      P('Effect에서 사용하는 Props·State는 배열에 빠짐없이 포함', 'Include every prop and state value used by the Effect'),
      P('관련 없는 값이 바뀔 때는 다시 실행하지 않아 불필요한 작업 방지', 'Avoid unnecessary work by skipping reruns when unrelated values change')) | dict(
        result_label=P('개발 실행 · StrictMode', 'Development · StrictMode'),
        result=[P('최초 표시 시 sync 사과 두 번 출력', 'sync 사과 is logged twice on mount')]),
    K('React · ProductTitle.jsx', 'React · ProductTitle.jsx', """
import { useEffect, useState } from 'react';

export default function ProductTitle() {
  const [pName, setPName] = useState('사과');
  const [theme, setTheme] = useState('white');
  useEffect(() => {
    console.log('sync', pName);
    document.title = `상품: ${pName}`;
  }, [pName]);
  return (
    <section style={{ background: theme }}>
      <h2>{pName}</h2>
      <button onClick={() => setPName('배')}>상품 변경</button>
      <button onClick={() => setTheme('pink')}>테마 변경</button>
    </section>
  );
}
""", width=72) | dict(
        result_label=P('프로덕션 실행 예시 · 최초 표시 → 테마 변경 → 상품 변경', 'Production run · Initial display → theme change → product change'),
        result=[P('최초: 사과 · 탭 제목 상품: 사과 · 콘솔 sync 사과', 'Initial: 사과 · tab 상품: 사과 · console sync 사과'),
                P('theme만 변경: 배경 흰색 → 분홍색 · 탭 제목 유지 · 추가 로그 없음', 'theme only: white → pink · tab unchanged · no new log'),
                P('pName 변경: 사과 → 배 · 탭 제목 상품: 배 · 콘솔 sync 배', 'pName: 사과 → 배 · tab 상품: 배 · console sync 배')]),
    refs=['https://react.dev/reference/react/useEffect', 'https://react.dev/learn/removing-effect-dependencies', 'https://react.dev/reference/react/StrictMode'])

body('effect-cleanup',
    D('정리 함수 - Effect에서 시작한 작업을 종료하는 함수', 'Cleanup - A function that stops work started by an Effect',
      P('Effect 안에서 함수를 반환하면 React가 필요할 때 실행', 'Return a function from the Effect for React to call when needed'),
      P('의존성 배열의 값이 바뀌면, 이전 작업을 종료한 뒤 새 값으로 시작', 'When a dependency changes, stop the old work before starting with the new value'),
      P('컴포넌트가 화면에서 제거되면 마지막으로 시작한 작업 종료', 'Stop the last running work when the component is removed'),
      P('타이머 중복 실행과 불필요하게 남아 있는 연결 방지', 'Prevent duplicate timers and connections left running unnecessarily')) | dict(
        result_label=P('개발 실행 · StrictMode', 'Development · StrictMode'),
        result=[P('최초 표시 시 stop 사과 한 번 추가', 'Initial mount adds one stop 사과 log')]),
    K('React · App.jsx', 'React · App.jsx', """
import { useEffect, useState } from 'react';

function Poller({ pName }) {
  useEffect(() => {
    const timer = setInterval(() => console.log('poll', pName), 1000);
    return () => {
      clearInterval(timer);
      console.log('stop', pName);
    };
  }, [pName]);
  return <p>조회 대상: {pName}</p>;
}
export default function App() {
  const [pName, setPName] = useState('사과');
  return <>
    <button onClick={() => setPName('배')}>값 변경</button>
    <button onClick={() => setPName(null)}>컴포넌트 제거</button>
    {pName && <Poller pName={pName} />}
  </>;
}
""", width=76) | dict(
        result_label=P('콘솔 · 프로덕션 실행 예시 · 처음에는 1초마다 poll 사과', 'Console · Production run · Initially poll 사과 every second'),
        result=[P('값 변경: stop 사과 → 1초마다 poll 배', 'Change value: stop 사과 → poll 배 every second'),
                P('컴포넌트 제거: stop 배 → 이후 poll 출력 없음', 'Remove component: stop 배 → no further poll output')]),
    refs=['https://react.dev/reference/react/useEffect', 'https://react.dev/learn/lifecycle-of-reactive-effects', 'https://react.dev/reference/react/StrictMode'])

body('custom-hook',
    D('커스텀 Hook - Hook을 사용하는 로직을 재사용하는 함수', 'Custom Hook - A reusable function containing Hook logic',
      P('이름을 use로 시작하고, 함수 안에서 useState 등 기존 Hook 사용', 'Start the name with use and call existing Hooks such as useState inside'),
      P('여러 컴포넌트에서 같은 로직을 가져다 써 중복 코드 감소', 'Reuse the same logic across components to reduce duplicate code'),
      P('공통 로직을 한곳에서 수정해 유지보수 단순화', 'Maintain shared logic in one place'),
      P('같은 Hook을 호출해도 상태는 각 컴포넌트에서 따로 유지', 'Each component keeps its own state even when using the same Hook')),
    K('React · App.jsx', 'React · App.jsx', """
import { useState } from 'react';

function useQuantity() {
  const [value, setValue] = useState(1);
  return [value, () => setValue(v => v + 1)];
}
function Quantity({ pName }) {
  const [value, increment] = useQuantity();
  return <button onClick={increment}>{`${pName}: ${value}`}</button>;
}
export default function App() {
  return <>
    <Quantity pName="사과" />
    <Quantity pName="배" />
  </>;
}
""", width=76) | dict(
        result_label=P('실행 결과 · 버튼별 수량', 'Result · Quantity on each button'),
        result=[P('처음: [사과: 1] [배: 1]', 'Initially: [사과: 1] [배: 1]'),
                P('사과 클릭: [사과: 2] [배: 1] → 사과 상태만 변경', 'Click 사과: [사과: 2] [배: 1] → only 사과 changes'),
                P('이어서 배 클릭: [사과: 2] [배: 2] → 배 상태만 변경', 'Then click 배: [사과: 2] [배: 2] → only 배 changes')]),
    refs=['https://react.dev/learn/reusing-logic-with-custom-hooks'])

body('more-hooks',
    D('추가 Hook - 필요한 기능에 따라 선택해 사용하는 React 함수', 'Additional Hooks - React functions selected for a specific need'),
    T([P('Hook', 'Hook'), P('역할', 'Role'), P('사용 사례', 'Example use')],
      [P('useContext', 'useContext'), P('여러 컴포넌트에 제공된 공통 값 읽기', 'Read a shared value provided to components'), P('로그인 정보·화면 테마', 'Login information, theme')],
      [P('useReducer', 'useReducer'), P('상태 변경 규칙을 별도 함수에 모아 관리', 'Manage state changes through a dedicated update function'), P('여러 동작이 있는 폼·장바구니', 'Forms or carts with multiple actions')],
      [P('useMemo', 'useMemo'), P('계산 결과를 저장해 같은 계산의 반복 줄이기', 'Cache a calculation result to avoid repeating work'), P('많은 데이터의 필터링·정렬', 'Filtering or sorting large datasets')],
      [P('useCallback', 'useCallback'), P('함수를 저장해 필요할 때 같은 함수 재사용', 'Cache a function to reuse the same reference'), P('최적화한 컴포넌트에 함수 전달', 'Passing functions to optimized components')],
      [P('useId', 'useId'), P('접근성 속성 연결에 사용할 고유 ID 생성', 'Generate unique IDs for accessibility relationships'), P('label과 input 연결', 'Linking a label to an input')],
      [P('useLayoutEffect', 'useLayoutEffect'), P('브라우저가 화면을 그리기 전에 크기 측정·위치 조정', 'Measure or adjust layout before the browser paints'), P('툴팁의 위치 계산', 'Positioning a tooltip')],
      [P('useTransition', 'useTransition'), P('일부 상태 변경을 덜 급하게 처리해 입력 반응 유지', 'Mark updates as non-blocking to keep input responsive'), P('탭 전환 중에도 버튼·입력 반응 유지', 'Responsive input during a tab switch')],
      [P('useDeferredValue', 'useDeferredValue'), P('값의 화면 반영을 늦춰 더 급한 화면 변경을 먼저 처리', 'Defer a value update so more urgent UI can update first'), P('검색어 입력을 먼저, 결과 목록 갱신은 나중에', 'Update search input before a slow result list')]),
    layout='single', refs=['https://react.dev/reference/react/hooks'])
