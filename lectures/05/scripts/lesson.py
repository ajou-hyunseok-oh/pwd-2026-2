"""Week 5 lesson source. Short teaching examples are explicitly labeled."""
from urllib.parse import quote

SLIDES = []
REPO = 'https://github.com/ajou-hyunseok-oh/pwd-week5'
COMMIT = '9d12cebf32d6e333e8cd69faa4a7c9c721e4be00'
PDF = 'materials/' + quote('[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf')

def P(ko, en): return (ko, en)
def C(*items): return dict(kind='concepts', items=items)
def K(label, code, lang='jsx', width=64): return dict(kind='code', label=label, code=code, lang=lang, width=width)
def T(head, *rows): return dict(kind='table', head=head, rows=rows)
def S(*items): return dict(kind='steps', items=items)
def I(name, ko, en): return dict(kind='image', src='materials/images/' + name + '.png', alt=P(ko, en), caption=P('pwd-week5 실제 실행 화면 · 한국어 UI', 'Running pwd-week5 app · Korean UI'))
def src(path): return (path, REPO + '/blob/' + COMMIT + '/' + path)
def pdf(page): return ('React PDF · p.' + str(page), PDF + '#page=' + str(page))
def doc(name, url): return (name, url)
def add(id, title, lead, *blocks, layout='split', sources=(), note=''):
    SLIDES.append(dict(id=id, chapter=CH, title=title, lead=lead, blocks=list(blocks), layout=layout, sources=list(sources), note=note))

JSX = doc('React · JSX', 'https://react.dev/learn/writing-markup-with-jsx')
COMP = doc('React · Components', 'https://react.dev/learn/your-first-component')
PROPS = doc('React · Props', 'https://react.dev/learn/passing-props-to-a-component')
STATE = doc('React · State', 'https://react.dev/learn/state-as-a-snapshot')
LIST = doc('React · Lists', 'https://react.dev/learn/rendering-lists')
EFFECT = doc('React · useEffect', 'https://react.dev/reference/react/useEffect')
RULES = doc('React · Hook Rules', 'https://react.dev/reference/rules/rules-of-hooks')
STORAGE = doc('MDN · localStorage', 'https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage')
QUERY = doc('TanStack · Query Keys', 'https://tanstack.com/query/latest/docs/framework/react/guides/query-keys')
INVALIDATE = doc('TanStack · Invalidation', 'https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation')
ROUTER = doc('React Router · HashRouter', 'https://reactrouter.com/api/declarative-routers/HashRouter')
FORM = doc('React Hook Form · Source', 'https://github.com/react-hook-form/react-hook-form')
VERCEL = doc('Vercel · Vite', 'https://vercel.com/docs/frameworks/frontend/vite')

CH = P('LECTURE 05 · 실전 웹 서비스 개발', 'LECTURE 05 · PRACTICAL WEB DEVELOPMENT')
add('cover', P('React 심화 · 캠퍼스 푸드맵', 'React Development · Campus Foodmap'),
    P('4주차 복습 · 컴포넌트와 상태 · 맛집 앱 구현과 Vercel 배포', 'Week 4 review · Components and state · Foodmap development and Vercel deployment'))

CH = P('01 · 4주차 학습 내용 복습', '01 · WEEK 4 REVIEW')
add('review-react', P('React와 개발 도구의 역할', 'React and Development Tools'),
    P('4주차의 Hello World 프로젝트를 구성한 도구와 실행 환경', 'The tools and runtime behind the Week 4 Hello World project'),
    T([P('구성 요소', 'Component'), P('역할', 'Role'), P('이번 실습의 사용 위치', 'Use in This Practice')],
      ['React', P('컴포넌트와 상태로 UI 표현', 'UI defined with components and state'), 'src/components/*.jsx'],
      ['React DOM', P('React UI를 브라우저 DOM에 반영', 'React UI committed to the browser DOM'), 'src/main.jsx'],
      ['Vite', P('개발 서버 · 소스 변환 · 배포 빌드', 'Dev server · Source transforms · Build'), 'vite.config.js'],
      ['Node.js · npm', P('개발 도구 실행 · 의존성 설치', 'Run tools · Install dependencies'), 'package.json · package-lock.json']),
    layout='single', sources=[('../04 · React 기초', '../04/index.html#/22'), src('package.json')])
add('review-ui', P('컴포넌트와 선언형 UI', 'Components and Declarative UI'),
    P('상품 목록에서 맛집 목록으로 이어지는 데이터 중심 화면 구성', 'The same data-driven UI model applied to restaurant listings'),
    C((P('컴포넌트 - 역할별 UI 단위', 'Component - A UI unit with a clear role'), [
        P('목록 · 카드 · 검색 조건의 분리', 'Separate the list, cards, and filters'),
        P('같은 카드에 서로 다른 맛집 데이터 전달', 'Pass different restaurant data to the same card')]),
      (P('선언형 UI - 상태에 맞는 화면 정의', 'Declarative UI - A view for the current state'), [
        P('한식 선택 → 조건 변경 → 일치하는 카드 표시', 'Select Korean food → Change filter → Show matching cards') ])),
    K(P('개념 예제 · 선택 조건과 화면', 'Teaching example · Filter and view'), """
const visible = restaurants.filter(
  (restaurant) => restaurant.category === category
);

return <RestaurantList restaurants={visible} />;
"""), sources=[('../04 · 컴포넌트와 선언형 UI', '../04/index.html#/9'), src('src/pages/ListPage.jsx')])
add('review-render', P('상태 변경과 화면 갱신', 'State Changes and Screen Updates'),
    P('이벤트 처리 · Render · Commit · 브라우저 렌더링의 구분', 'Events, render, commit, and browser rendering'),
    S((P('상태 변경 요청', 'Request a state update'), P('좋아요 버튼 클릭 → setLiked 호출', 'Click Like → Call setLiked')),
      (P('Render - UI 계산', 'Render - Calculate the UI'), P('새 상태로 컴포넌트 실행 · JSX 결과 비교', 'Run the component with new state · Compare UI output')),
      (P('Commit - DOM 변경 반영', 'Commit - Apply DOM updates'), P('버튼 문구 · 색상 등 필요한 DOM 갱신', 'Update the required DOM text and attributes')),
      (P('브라우저 표시', 'Browser rendering'), P('변경 내용에 따라 스타일 · 레이아웃 · 페인트 처리', 'Process style, layout, and paint as needed'))),
    C((P('Virtual DOM - UI의 메모리 표현', 'Virtual DOM - An in-memory UI representation'), [
        P('컴포넌트 재실행과 DOM 전체 교체는 별개', 'Re-running a component differs from replacing all DOM nodes'),
        P('직접 DOM 조작보다 항상 빠르다는 보장 없음', 'No guarantee of being faster than direct DOM updates')]),
      (P('상태의 소유자 - 변경 책임의 위치', 'State owner - The place responsible for updates'), [
        P('선택 조건은 ListPage · 좋아요는 RestaurantCard', 'Filter in ListPage · Like state in RestaurantCard') ])),
    sources=[pdf(7), ('React · Render and Commit', 'https://react.dev/learn/render-and-commit')])
add('review-planning', P('서비스 기획과 구현 단위', 'Service Plans and Implementation'),
    P('4주차의 사용자 흐름을 페이지 · 기능 · 데이터로 구체화', 'Translate the Week 4 user flow into pages, features, and data'),
    T([P('사용자 행동', 'User Action'), P('화면과 파일', 'Screen and File'), P('필요한 데이터', 'Required Data')],
      [P('주변 맛집 탐색', 'Browse restaurants'), 'ListPage.jsx', P('맛집 목록 · 선택 카테고리', 'Restaurants · Selected category')],
      [P('한 맛집의 정보 확인', 'Inspect one restaurant'), 'DetailPage.jsx', P('URL의 id · 해당 맛집 객체', 'URL id · Restaurant object')],
      [P('마음에 드는 맛집 표시', 'Like a restaurant'), 'RestaurantCard.jsx', P('좋아요 여부 · 개수', 'Like status · Count')],
      [P('새로운 맛집 제보', 'Submit a restaurant'), 'SubmitRestaurant.jsx', P('입력값 · 검증 오류 · 저장 결과', 'Input · Validation errors · Save result')]),
    layout='single', sources=[('../04 · 웹 서비스 기획', '../04/ai-design.html'), src('src/App.jsx')])

CH = P('02 · 실습 프로젝트와 개발 환경', '02 · PROJECT AND DEVELOPMENT ENVIRONMENT')
add('practice-target', P('캠퍼스 푸드맵의 실습 목표', 'Campus Foodmap Practice Goals'),
    P('탐색 · 상호작용 · 제보 · 배포를 연결하는 React 웹 앱', 'A React app combining browsing, interaction, submission, and deployment'),
    I('list', '카테고리 필터와 세 개의 맛집 카드', 'Category filters and three restaurant cards'),
    C((P('화면 구성 - 컴포넌트 조합', 'UI structure - Component composition'), [P('목록 · 상세 · 인기 · 제보 페이지', 'List · Detail · Ranking · Submission pages')]),
      (P('상호작용 - 상태와 이벤트', 'Interaction - State and events'), [P('카테고리 선택 · 좋아요 변경', 'Category selection · Like updates')]),
      (P('완료 기준 - 배포 주소의 기능 확인', 'Completion - Working features at the deployed URL'), [P('새로고침 후 저장값 유지 · Git 변경 반영', 'Saved values after reload · Deployed Git changes')])),
    layout='visual', sources=[src('README.md')])
add('practice-data', P('실습 데이터와 저장 범위', 'Practice Data and Storage Scope'),
    P('초기 예제 데이터와 현재 브라우저의 localStorage로 동작', 'Initial sample data and localStorage in the current browser'),
    T([P('대상', 'Item'), P('실제 구현', 'Current Implementation'), P('확인할 특징', 'Behavior to Check')],
      [P('맛집 목록', 'Restaurants'), 'src/services/api.jsx', P('초기 3개 예제 · 저장값 우선 조회', '3 initial examples · Saved values take priority')],
      [P('좋아요', 'Likes'), 'likedRestaurants · restaurantLikes', P('현재 브라우저의 선택과 개수', 'Choices and counts in this browser')],
      [P('제보', 'Submissions'), 'pwd-week5-submissions', P('사용자 간 공유 없는 브라우저 저장', 'Browser storage with no cross-user sharing')],
      [P('인기 목록', 'Ranking'), 'getPopularRestaurants()', P('평점 내림차순 · 최대 5개', 'Rating descending · Up to 5 items')]),
    layout='single', sources=[src('src/services/api.jsx'), src('src/components/RestaurantCard.jsx')],
    note='초기 음식점 이름·수치는 실습 데이터이며 실시간 식당 정보나 실제 인기 통계가 아님.')
add('setup-clone', P('완성 실습 저장소의 실행', 'Running the Practice Repository'),
    P('본 강의의 기준 경로 · 제공된 소스와 잠금 파일 사용', 'Main path for this lecture · Provided source and lockfile'),
    K(P('터미널 · 프로젝트를 둘 상위 폴더', 'Terminal · Parent folder for the project'), """
node --version
npm --version
git --version

git clone https://github.com/ajou-hyunseok-oh/pwd-week5.git
cd pwd-week5
npm ci
npm run dev
""", 'bash'),
    S((P('환경 확인', 'Check the environment'), P('실습 package.json의 Node.js 24.x 사용', 'Use Node.js 24.x specified in package.json')),
      (P('설치 위치 확인', 'Check the working directory'), P('package.json과 package-lock.json이 있는 폴더', 'The folder containing package.json and package-lock.json')),
      (P('브라우저 접속', 'Open the browser'), P('터미널의 Local 주소 접속 · 기본 포트 5173', 'Open the terminal’s Local URL · Default port 5173')),
      (P('성공 결과', 'Expected result'), P('홈 화면 표시 · 맛집 둘러보기 이동', 'Home screen · Navigation to the restaurant list'))),
    layout='code', sources=[src('README.md'), src('package.json')])
add('setup-new', P('빈 프로젝트 생성과 파일 적용', 'Creating and Populating a Project'),
    P('직접 작성 경로 · JavaScript + SWC 템플릿 사용', 'Build-from-scratch path · JavaScript + SWC template'),
    K(P('터미널 · 새 프로젝트 생성', 'Terminal · Create a new project'), """
mkdir pwd-week5
cd pwd-week5
npm create vite@7.1.2 . -- --template react-swc
npm install
npm run dev
""", 'bash'),
    S((P('파일 확장자 확인', 'Check file extensions'), P('4주차 .tsx → 이번 실습 .jsx · 타입 표기 없이 작성', 'Week 4 .tsx → This practice .jsx · No type annotations')),
      (P('의존성 적용', 'Apply dependencies'), P('실습 저장소의 package.json 적용 후 npm install', 'Apply the practice package.json, then run npm install')),
      (P('파일 구성 적용', 'Apply the source files'), P('실습 src/ · index.html · vite.config.js · vercel.json 사용', 'Use the practice src/, index.html, vite.config.js, and vercel.json')),
      (P('기준 소스 선택', 'Choose the reference source'), P('README와 차이가 있으면 실제 src/ 파일 기준', 'Use actual src/ files when README snippets differ'))),
    layout='code', sources=[src('README.md'), src('package.json')],
    note='본 강의 기본 경로는 완성 저장소 실행 후 개념별 코드 수정. 신규 생성은 대안이며 같은 폴더에서 두 경로를 연속 실행하지 않음.')
add('project-files', P('프로젝트 폴더와 역할', 'Project Folders and Responsibilities'),
    P('화면 구성 · 데이터 처리 · 스타일의 책임 구분', 'Separate UI composition, data operations, and styles'),
    K(P('pwd-week5 · 핵심 파일', 'pwd-week5 · Main files'), """
index.html
src/
  main.jsx
  App.jsx
  pages/
    ListPage.jsx
    DetailPage.jsx
  components/
    RestaurantList.jsx
    RestaurantCard.jsx
    SubmitRestaurant.jsx
  services/api.jsx
  styles/GlobalStyles.jsx
""", 'text'),
    C((P('pages - URL별 화면', 'pages - Screens selected by URL'), [P('조회와 상태 관리 · 컴포넌트 배치', 'Queries and state · Component composition')]),
      (P('components - 재사용 UI', 'components - Reusable UI'), [P('목록 · 카드 · 입력 폼의 표현과 동작', 'List, card, and form views and interactions')]),
      (P('services - 데이터 접근', 'services - Data access'), [P('조회 · 생성 · 수정 · 삭제 함수', 'Read · Create · Update · Delete functions')]),
      (P('styles - 공통 표현', 'styles - Shared presentation'), [P('전역 스타일과 컴포넌트별 Emotion', 'Global styles and component-level Emotion')])),
    sources=[src('src/App.jsx'), src('src/services/api.jsx')])
add('entry', P('index.html과 React 진입점', 'HTML and the React Entry Point'),
    P('root 요소에 App 컴포넌트를 연결하는 main.jsx', 'main.jsx mounts the App component into the root element'),
    K('src/main.jsx', """
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
"""),
    C((P('index.html - 최초 문서', 'index.html - The initial document'), [P('id가 root인 요소 · /src/main.jsx 모듈 로드', 'Element with id root · Load the /src/main.jsx module')]),
      (P('createRoot - React 관리 영역 생성', 'createRoot - Create a React root'), [P('render(<App />)로 최상위 컴포넌트 연결', 'Mount the top-level component with render(<App />)')]),
      (P('StrictMode - 개발 중 추가 검사', 'StrictMode - Extra development checks'), [P('순수한 렌더링과 Effect 정리 점검', 'Check render purity and Effect cleanup')])),
    layout='code', sources=[src('src/main.jsx'), doc('React · StrictMode', 'https://react.dev/reference/react/StrictMode')])

CH = P('03 · JSX와 컴포넌트', '03 · JSX AND COMPONENTS')
add('component-types', P('클래스형과 함수형 컴포넌트', 'Class and Function Components'),
    P('원본 PDF의 두 구현 방식과 이번 실습의 함수형 컴포넌트', 'The two forms in the original PDF and functions used in this practice'),
    T([P('구분', 'Aspect'), P('클래스형', 'Class Component'), P('함수형', 'Function Component')],
      [P('선언', 'Declaration'), 'class extends Component', 'function RestaurantCard()'],
      [P('화면 반환', 'View output'), 'render() { return ...; }', 'return (...);'],
      [P('상태', 'State'), 'this.state · this.setState', 'useState'],
      [P('외부 동기화', 'Synchronization'), 'componentDidMount · componentDidUpdate', 'useEffect · cleanup'],
      [P('학습 적용', 'Use in this lecture'), P('기존 코드의 구조 이해', 'Recognize existing class-based code'), P('src/ 전체의 함수형 구현 분석', 'Read function components throughout src/')]),
    layout='single', sources=[pdf(13), COMP, doc('React · Component', 'https://react.dev/reference/react/Component')])
add('function-component', P('함수형 컴포넌트의 구조', 'Function Component Structure'),
    P('입력을 받아 JSX를 반환하는 JavaScript 함수', 'A JavaScript function that receives input and returns JSX'),
    K(P('개념 예제 · 최소 맛집 카드', 'Teaching example · Minimal restaurant card'), """
export default function RestaurantCard({ restaurant }) {
  return (
    <article>
      <h3>{restaurant.name}</h3>
      <p>{restaurant.category}</p>
    </article>
  );
}
"""),
    C((P('대문자 이름 - 사용자 컴포넌트', 'Capitalized name - A custom component'), [P('RestaurantCard와 HTML의 article 구분', 'Distinguish RestaurantCard from HTML article')]),
      (P('return - 화면 표현 반환', 'return - Return the view'), [P('여러 줄 JSX는 괄호로 묶기', 'Wrap multiline JSX in parentheses')]),
      (P('export - 다른 파일에서 재사용', 'export - Reuse in another file'), [P('default export와 중괄호 없는 import 연결', 'Pair a default export with an import without braces')])),
    layout='code', sources=[pdf(11), pdf(13), COMP])
add('jsx-rules', P('JSX 작성 규칙', 'JSX Syntax Rules'),
    P('HTML과 비슷한 표현에 JavaScript 값을 결합하는 문법', 'HTML-like markup combined with JavaScript values'),
    K(P('개념 예제 · 카드와 버튼', 'Teaching example · Card and button'), """
return (
  <>
    <article className="card">
      <h3>{restaurant.name}</h3>
      <img src={restaurant.image} alt={restaurant.name} />
      <button onClick={handleLike}>Like</button>
    </article>
    {/* Additional UI */}
  </>
);
"""),
    C((P('루트 - 하나의 JSX 표현식', 'Root - A single JSX expression'), [P('형제 요소는 부모 요소 또는 Fragment로 묶기', 'Wrap siblings in a parent element or Fragment')]),
      (P('태그와 속성 - JSX 표기', 'Tags and props - JSX spelling'), [P('모든 태그 닫기 · className · onClick', 'Close all tags · className · onClick'), P('aria-* · data-*는 하이픈 유지', 'Keep hyphens in aria-* and data-*')]),
      (P('중괄호 - JavaScript 표현식', 'Braces - JavaScript expressions'), [P('문자열 · 숫자 · 함수 호출 결과 삽입', 'Insert strings, numbers, and function results')])),
    layout='code', sources=[pdf(9), pdf(10), JSX])
add('jsx-values', P('JSX의 값과 조건 표현', 'Values and Conditions in JSX'),
    P('문자열 · 속성 · 삼항 연산자의 서로 다른 사용 위치', 'Different uses of text, attributes, and conditional expressions'),
    K(P('개념 예제 · 값의 삽입', 'Teaching example · Inserting values'), """
const label = liked ? 'Liked' : 'Like';

return (
  <button
    className={liked ? 'active' : ''}
    onClick={handleLike}
  >
    {label} {likes}
  </button>
);
"""),
    C((P('따옴표 - 고정 문자열', 'Quotes - A fixed string'), [P('className="card"의 card는 그대로 전달', 'card in className="card" is a literal value')]),
      (P('중괄호 - 계산 결과', 'Braces - A computed value'), [P('{likes}는 현재 숫자 표시', '{likes} displays the current number')]),
      (P('조건부 표현 - 값에 따른 분기', 'Conditional expression - A value-based branch'), [P('liked가 true이면 Liked 표시', 'Display Liked when liked is true'), P('if 문은 JSX 밖 · 삼항 연산자는 JSX 안에서도 사용', 'Use if outside JSX · Ternaries may appear inside JSX')])),
    layout='code', sources=[JSX, src('src/components/RestaurantCard.jsx')])
add('props', P('Props 전달과 구조 분해', 'Passing and Destructuring Props'),
    P('부모의 맛집 객체를 자식 컴포넌트의 입력으로 전달', 'Pass a restaurant object from parent to child'),
    K(P('개념 예제 · 부모와 자식', 'Teaching example · Parent and child'), """
// Parent
<RestaurantCard restaurant={item} />;

// Child
function RestaurantCard({ restaurant }) {
  return <h3>{restaurant.name}</h3>;
}
"""),
    C((P('속성 이름 - 입력의 이름', 'Prop name - The input key'), [P('왼쪽 restaurant는 props의 키', 'restaurant on the left is the prop key')]),
      (P('속성 값 - 부모가 가진 데이터', 'Prop value - Data from the parent'), [P('오른쪽 item은 전달할 객체', 'item on the right is the object being passed')]),
      (P('구조 분해 - 필요한 값 추출', 'Destructuring - Extract the needed value'), [P('{ restaurant }는 props.restaurant 추출', '{ restaurant } extracts props.restaurant')]),
      (P('읽기 전용 - 자식의 직접 수정 금지', 'Read-only - No direct mutation by the child'), [P('변경이 필요하면 상태의 소유자에게 요청', 'Request updates from the state owner')])),
    layout='code', sources=[pdf(14), PROPS, src('src/components/RestaurantList.jsx')])
add('composition', P('페이지와 컴포넌트의 조합', 'Page and Component Composition'),
    P('조회 · 필터 · 목록 표현을 서로 다른 책임으로 분리', 'Separate data queries, filtering, and list rendering'),
    T([P('컴포넌트', 'Component'), P('입력과 상태', 'Input and State'), P('주요 책임', 'Responsibility')],
      ['ListPage', 'selectedCategory · useQuery', P('목록 조회 · 카테고리 선택 · 필터 계산', 'Query restaurants · Select and apply a filter')],
      ['RestaurantList', 'restaurants', P('빈 목록 처리 · 카드 반복 생성', 'Handle an empty list · Render cards')],
      ['RestaurantCard', 'restaurant · liked · likes', P('한 맛집 표시 · 좋아요 처리', 'Show one restaurant · Handle likes')],
      ['SubmitPage', 'SubmitRestaurant', P('제보 컴포넌트를 URL에 연결', 'Connect the form component to a route')]),
    layout='single', sources=[pdf(12), src('src/pages/ListPage.jsx'), src('src/components/RestaurantList.jsx')])
add('map-key', P('목록 렌더링과 key', 'List Rendering and Keys'),
    P('배열의 맛집 객체를 식별 가능한 카드 목록으로 변환', 'Transform restaurant objects into an identifiable list of cards'),
    K(P('RestaurantList.jsx · 핵심 구조', 'RestaurantList.jsx · Core structure'), """
function RestaurantList({ restaurants }) {
  if (restaurants.length === 0) {
    return <NoResults>No restaurants in this category.</NoResults>;
  }

  return (
    <ListContainer>
      {restaurants.map((restaurant) => (
        <RestaurantCard
          key={restaurant.id}
          restaurant={restaurant}
        />
      ))}
    </ListContainer>
  );
}
""", width=64),
    C((P('map - 항목별 UI 생성', 'map - UI for each item'), [P('맛집 객체 하나 → 카드 하나', 'One restaurant object → One card')]),
      (P('key - 형제 항목의 안정적인 식별자', 'key - Stable identity among siblings'), [P('추가 · 삭제 · 순서 변경에도 같은 항목 추적', 'Track the same item across inserts, deletes, and reorders'), P('변하는 목록에서 index · Math.random() 사용 지양', 'Avoid indexes or Math.random() for changing lists')]),
      (P('props - key와 별도 전달', 'props - Passed separately from key'), [P('자식에서 id가 필요하면 restaurant.id 사용', 'Read restaurant.id when the child needs the id')])),
    layout='code', sources=[LIST, src('src/components/RestaurantList.jsx')],
    note='코드의 UI 문자열은 강의 예제용 영문으로 축약. NoResults와 ListContainer 정의·import는 실제 파일 참조.')
add('practice-card', P('실습 1 · 카드의 표시 정보 수정', 'Practice 1 · Editing Card Content'),
    P('Props와 JSX를 사용해 추천 메뉴를 카드에 추가', 'Use props and JSX to add recommended menus to a card'),
    K(P('RestaurantCard.jsx · CardContent 내부에 추가', 'RestaurantCard.jsx · Add inside CardContent'), """
<p>
  {(restaurant.recommendedMenu ?? []).join(', ')}
</p>
"""),
    S((P('수정 위치', 'Edit location'), P('RestaurantCard.jsx의 이름 · 카테고리 아래', 'Below the name and category in RestaurantCard.jsx')),
      (P('데이터 확인', 'Inspect the data'), P('services/api.jsx의 recommendedMenu 배열', 'The recommendedMenu array in services/api.jsx')),
      (P('기대 결과', 'Expected result'), P('송림식당 카드에 순두부 · 김치찌개 등 표시', 'Songnim’s card shows menu items such as soft tofu and kimchi stew')),
      (P('오류 확인', 'Check errors'), P('객체 자체 대신 문자열 · 배열의 join 결과 표시', 'Render strings or a joined array, not the whole object'))),
    layout='code', sources=[src('src/components/RestaurantCard.jsx'), src('src/services/api.jsx')])

CH = P('04 · State와 이벤트', '04 · STATE AND EVENTS')
add('state-props', P('Props · State · 파생값의 구분', 'Props, State, and Derived Values'),
    P('입력 · 변경 가능한 최소 정보 · 계산 결과를 구분하는 기준', 'Distinguish inputs, minimal changing data, and calculated results'),
    T([P('종류', 'Kind'), P('실습 예시', 'Practice Example'), P('관리 방식', 'How It Is Managed')],
      ['Props', 'restaurant', P('부모로부터 전달 · 자식에서 읽기', 'Passed by the parent · Read by the child')],
      ['State', 'selectedCategory · liked', P('useState로 보관 · setter로 갱신', 'Stored by useState · Updated through a setter')],
      [P('파생값', 'Derived value'), 'filteredData', P('현재 목록과 선택 조건으로 계산', 'Calculated from the list and selected category')],
      [P('영속 저장', 'Persistent storage'), 'localStorage', P('새로고침 이후 복원 · 별도 저장 필요', 'Restored after reload · Explicit writes required')]),
    layout='single', sources=[pdf(14), STATE, src('src/pages/ListPage.jsx')])
add('use-state', P('useState의 반환값과 갱신', 'useState Values and Updates'),
    P('현재 상태와 상태 변경 함수를 구조 분해로 받는 방식', 'Destructure the current state and its update function'),
    K(P('개념 예제 · 좋아요 토글', 'Teaching example · Like toggle'), """
import { useState } from 'react';

export default function LikeButton() {
  const [liked, setLiked] = useState(false);

  return (
    <button onClick={() => setLiked((prev) => !prev)}>
      {liked ? 'Liked' : 'Like'}
    </button>
  );
}
"""),
    C((P('초기값 - 첫 렌더의 상태', 'Initial value - State for the first render'), [P('false → 아직 좋아요를 선택하지 않은 상태', 'false → The restaurant is not liked yet')]),
      (P('setter - 갱신 요청 함수', 'Setter - A request to update state'), [P('setLiked 호출 → 새 상태로 다시 렌더링', 'Call setLiked → Render with the next state')]),
      (P('함수형 갱신 - 이전 상태로 계산', 'Updater function - Calculate from prior state'), [P('prev는 처리 중인 이전 상태', 'prev is the prior state being processed'), P('토글 · 누적처럼 이전 값에 의존할 때 사용', 'Useful for toggles and accumulated updates')])),
    layout='code', sources=[STATE, src('src/components/RestaurantCard.jsx')])
add('state-snapshot', P('상태 스냅샷과 연속 갱신', 'State Snapshots and Queued Updates'),
    P('한 이벤트 안에서 읽는 상태는 해당 렌더 시점의 값', 'State read inside an event belongs to that render'),
    K(P('개념 예제 · count가 0인 렌더', 'Teaching example · A render with count = 0'), """
function addThree() {
  setCount((n) => n + 1);
  setCount((n) => n + 1);
  setCount((n) => n + 1);
}

function replaceThreeTimes() {
  setCount(count + 1);
  setCount(count + 1);
  setCount(count + 1);
}
"""),
    C((P('함수형 갱신 - 대기 중인 값에 순차 적용', 'Updater functions - Apply to queued values'), [P('addThree: 0 → 1 → 2 → 3', 'addThree: 0 → 1 → 2 → 3')]),
      (P('값 전달 - 같은 계산 결과로 교체', 'Value updates - Replace with the same result'), [P('replaceThreeTimes: 1로 교체 요청 3회 → 1', 'replaceThreeTimes: Replace with 1 three times → 1')]),
      (P('이벤트 안의 변수 - 즉시 변경되지 않음', 'Event variables - Unchanged in this render'), [P('setter 호출 직후 count를 읽으면 기존 값', 'Reading count immediately after the setter gives the old value')])),
    layout='code', sources=[STATE, doc('React · Queued Updates', 'https://react.dev/learn/queueing-a-series-of-state-updates')])
add('events', P('이벤트 핸들러의 전달', 'Passing Event Handlers'),
    P('렌더 시 함수 전달과 이벤트 발생 시 함수 실행의 구분', 'Passing a function during render versus running it on an event'),
    K(P('개념 예제 · 클릭 이벤트', 'Teaching example · Click events'), """
<button onClick={handleLike}>Like</button>;

<button onClick={() => setSelectedCategory('한식')}>
  Korean food
</button>;
"""),
    C((P('함수 전달 - 클릭할 때 실행', 'Function reference - Run on click'), [P('onClick={handleLike}에 함수 자체 전달', 'Pass the function itself with onClick={handleLike}')]),
      (P('인자 전달 - 새 콜백으로 감싸기', 'Arguments - Wrap the call in a callback'), [P('카테고리 값은 화살표 함수 안에서 전달', 'Pass the category inside an arrow function')]),
      (P('즉시 호출 - 렌더 중 실행', 'Immediate call - Runs during render'), [P('onClick={handleLike()}는 클릭 전에 실행', 'onClick={handleLike()} runs before any click'), P('렌더 중 무조건적인 상태 갱신은 반복 렌더링 원인', 'Unconditional state updates during render can loop')])),
    layout='code', sources=[pdf(15), src('src/pages/ListPage.jsx')])
add('filter', P('카테고리 선택과 파생 목록', 'Category Selection and Derived Lists'),
    P('선택 값만 State로 보관하고 필터 결과는 렌더 중 계산', 'Store only the selected category; calculate the filtered list during render'),
    K(P('ListPage.jsx · 필터 계산', 'ListPage.jsx · Filter calculation'), """
const [selectedCategory, setSelectedCategory] =
  useState('전체');

const filteredData =
  selectedCategory === '전체'
    ? data?.data
    : data?.data.filter(
        (r) => r.category === selectedCategory
      );

return <RestaurantList restaurants={filteredData || []} />;
"""),
    C((P('전체 - 원본 목록 사용', 'All - Use the original list'), [P('카테고리 조건 없이 전체 데이터 표시', 'Display every item without a category condition')]),
      (P('선택 카테고리 - filter 조건', 'Selected category - The filter predicate'), [P('한식 선택 → category가 한식인 항목만 유지', 'Select Korean food → Keep matching items')]),
      (P('파생값 - 중복 상태 방지', 'Derived value - Avoid duplicated state'), [P('filteredData용 State와 Effect는 불필요', 'No separate state or Effect needed for filteredData')])),
    layout='code', sources=[src('src/pages/ListPage.jsx'), doc('React · Derived Values', 'https://react.dev/learn/you-might-not-need-an-effect')])
add('like-state', P('좋아요 상태와 개수의 계산', 'Calculating Like State and Count'),
    P('현재 선택을 반전하고 좋아요 수가 음수가 되지 않도록 처리', 'Toggle the current choice and keep the count nonnegative'),
    K(P('RestaurantCard.jsx · handleLike 일부', 'RestaurantCard.jsx · Part of handleLike'), """
const newLikedState = !liked;
const newLikesCount = newLikedState
  ? likes + 1
  : Math.max(0, likes - 1);

setLiked(newLikedState);
setLikes(newLikesCount);
"""),
    C((P('liked - 선택 여부', 'liked - Whether the item is liked'), [P('false → true는 선택 · true → false는 취소', 'false → true selects · true → false cancels')]),
      (P('likes - 현재 브라우저의 개수', 'likes - The count in this browser'), [P('선택 시 +1 · 취소 시 -1 · 최솟값 0', '+1 on like · -1 on unlike · Minimum 0')]),
      (P('저장 실패 - UI와 저장값 불일치 가능', 'Write failure - UI and storage may diverge'), [P('현재 코드는 UI 변경 후 저장 · 실패 처리 확인 필요', 'Current code updates UI before storage; inspect failure handling')])),
    layout='code', sources=[src('src/components/RestaurantCard.jsx')])
add('immutable-state', P('객체와 배열 상태의 갱신', 'Updating Object and Array State'),
    P('기존 State를 직접 수정하지 않고 새 값을 전달하는 방식', 'Pass a new value instead of mutating existing state'),
    K(P('개념 예제 · 상태 갱신 패턴', 'Teaching example · State update patterns'), """
setForm((prev) => ({
  ...prev,
  restaurantName: nextName,
}));

setItems((prev) => [...prev, newItem]);

setItems((prev) =>
  prev.filter((item) => item.id !== deletedId)
);
"""),
    C((P('객체 - 전개 후 변경 필드 덮어쓰기', 'Objects - Spread, then replace a field'), [P('...prev로 나머지 필드 유지', 'Keep other fields with ...prev')]),
      (P('배열 - 새 배열 생성', 'Arrays - Create a new array'), [P('추가에 전개 구문 · 삭제에 filter 사용', 'Spread to add · filter to remove')]),
      (P('변경 대상 - React State 여부 확인', 'Update target - Check whether it is React state'), [P('저장소에서 새로 읽은 배열과 State 배열 구분', 'Distinguish newly read storage arrays from state arrays')])),
    layout='code', sources=[doc('React · Updating Arrays', 'https://react.dev/learn/updating-arrays-in-state'), src('src/services/api.jsx')])
add('practice-state', P('실습 2 · 필터와 좋아요 확인', 'Practice 2 · Filters and Likes'),
    P('입력 · 변경된 상태 · 화면 결과를 연결하는 동작 확인', 'Connect input, changed state, and visible results'),
    T([P('실행', 'Action'), P('기대 결과', 'Expected Result'), P('오류 확인 위치', 'Where to Inspect')],
      [P('한식 선택', 'Select Korean food'), P('초기 데이터 중 송림식당 1개 표시', 'Only Songnim shown in the initial data'), 'ListPage.jsx · selectedCategory'],
      [P('카페 선택', 'Select cafés'), P('초기 데이터 기준 빈 목록 안내', 'Empty-state message for the initial data'), 'RestaurantList.jsx · length'],
      [P('전체 선택', 'Select All'), P('초기 맛집 3개 복원', 'All 3 initial restaurants shown'), 'ListPage.jsx · filteredData'],
      [P('좋아요 클릭 · 다시 클릭', 'Like · Click again'), P('선택과 개수 증가 · 취소와 개수 복원', 'Like and increment · Unlike and restore'), 'RestaurantCard.jsx · handleLike']),
    layout='single', sources=[src('src/pages/ListPage.jsx'), src('src/components/RestaurantCard.jsx')])

CH = P('05 · Hooks와 브라우저 저장', '05 · HOOKS AND BROWSER STORAGE')
add('hook-rules', P('Hooks의 역할과 호출 규칙', 'Hook Roles and Calling Rules'),
    P('컴포넌트의 상태와 외부 동기화를 연결하는 함수 API', 'Function APIs for component state and external synchronization'),
    T([P('Hook', 'Hook'), P('역할', 'Role'), P('실습 사용 예', 'Practice Use')],
      ['useState', P('렌더 사이에 상태 보관', 'Retain state between renders'), 'liked · selectedCategory'],
      ['useEffect', P('외부 시스템과 동기화', 'Synchronize with an external system'), P('좋아요 저장값 복원', 'Restore saved likes')],
      ['useQuery', P('비동기 조회 결과와 상태 관리', 'Manage async query results and status'), 'ListPage · DetailPage'],
      ['useForm', P('입력 등록 · 검증 · 제출 관리', 'Register inputs · Validate · Submit'), 'SubmitRestaurant']),
    C((P('호출 위치 - 컴포넌트 최상위', 'Call location - Component top level'), [P('조건문 · 반복문 · 이벤트 핸들러 안에서 호출 금지', 'No calls inside conditions, loops, or event handlers'), P('조기 return보다 먼저 호출', 'Call before any early return')]),
      (P('라이브러리 Hooks - 같은 호출 규칙', 'Library Hooks - The same calling rules'), [P('useQuery · useForm도 컴포넌트 최상위에서 호출', 'Call useQuery and useForm at component top level too')])),
    sources=[pdf(16), RULES])
add('effects', P('useEffect와 의존성 배열', 'useEffect and Dependencies'),
    P('렌더 후 외부 상태를 동기화할 조건을 표현하는 방식', 'Describe when external state needs synchronization after a commit'),
    K(P('개념 예제 · 문서 제목 동기화', 'Teaching example · Synchronize the document title'), """
useEffect(() => {
  document.title = restaurant.name;
}, [restaurant.name]);
"""),
    C((P('Effect - 외부 상태와 동기화', 'Effect - Synchronization with external state'), [P('문서 제목 · 이벤트 구독 · 브라우저 저장', 'Document title · Event subscriptions · Browser storage')]),
      (P('의존성 - Effect가 읽는 반응형 값', 'Dependencies - Reactive values read by the Effect'), [P('restaurant.name 변경 시 다시 동기화', 'Synchronize again when restaurant.name changes'), P('의존성 생략은 모든 Commit 뒤 실행', 'Omitting the array runs after every commit')]),
      (P('빈 배열 - 반응형 의존성 없음', 'Empty array - No reactive dependencies'), [P('개발 StrictMode의 추가 setup·cleanup 가능', 'Development StrictMode may add a setup/cleanup cycle')])),
    layout='code', sources=[pdf(17), EFFECT])
add('effect-cleanup', P('Effect의 정리와 실행 순서', 'Effect Cleanup and Execution Order'),
    P('구독과 타이머의 수명을 setup · cleanup으로 관리', 'Manage subscriptions and timers through setup and cleanup'),
    K(P('개념 예제 · resize 구독', 'Teaching example · Resize subscription'), """
useEffect(() => {
  const onResize = () => {
    setWidth(window.innerWidth);
  };

  window.addEventListener('resize', onResize);

  return () => {
    window.removeEventListener('resize', onResize);
  };
}, []);
"""),
    C((P('마운트 - 첫 setup', 'Mount - Initial setup'), [P('DOM 반영 후 Effect 실행', 'Run the Effect after the DOM commit')]),
      (P('의존성 변경 - 정리 후 재설정', 'Dependency change - Cleanup, then setup'), [P('이전 cleanup → 새 setup', 'Previous cleanup → New setup')]),
      (P('언마운트 - 마지막 cleanup', 'Unmount - Final cleanup'), [P('화면에서 제거 시 구독 해제', 'Remove subscriptions when the component leaves')]),
      (P('실행 시점 - Commit 이후', 'Timing - After the commit'), [P('상호작용에 따른 Effect는 Paint 전에 실행 가능', 'An interaction-related Effect may run before paint')])),
    layout='code', sources=[pdf(17), EFFECT])
add('storage-api', P('localStorage와 JSON 변환', 'localStorage and JSON Conversion'),
    P('문자열 저장소에 배열과 객체를 저장하고 복원하는 과정', 'Store and restore arrays and objects through a string-based store'),
    K(P('개념 예제 · 좋아요 ID 배열', 'Teaching example · Liked restaurant IDs'), """
const ids = [1, 3];

localStorage.setItem(
  'likedRestaurants',
  JSON.stringify(ids)
);

const saved = JSON.parse(
  localStorage.getItem('likedRestaurants') || '[]'
);
""", 'javascript'),
    C((P('stringify - 값을 문자열로 변환', 'stringify - Convert a value to a string'), [P('[1, 3] 배열 → JSON 문자열 저장', 'Array [1, 3] → Store a JSON string')]),
      (P('parse - 문자열에서 값 복원', 'parse - Restore a value from a string'), [P('키가 없으면 null · 기본 문자열 사용', 'A missing key returns null · Supply a default string')]),
      (P('오류 - 읽기와 쓰기 실패 가능', 'Errors - Reads and writes may fail'), [P('잘못된 JSON · 저장 공간 · 브라우저 정책', 'Invalid JSON · Storage quota · Browser policy')])),
    layout='code', sources=[STORAGE, src('src/services/api.jsx')])
add('hook-selection', P('Hooks의 선택 기준', 'Choosing Hooks for a Task'),
    P('상태 · 참조 · 공유 · 성능 최적화의 서로 다른 목적', 'Distinct purposes for state, references, sharing, and optimization'),
    T([P('필요', 'Need'), P('Hook', 'Hook'), P('선택 기준', 'Selection Criterion')],
      [P('화면에 표시할 값', 'A value shown in the UI'), 'useState', P('변경 시 새 렌더링 필요', 'Changing it should request a render')],
      [P('렌더링과 무관한 보관', 'Storage without rendering'), 'useRef', P('DOM 참조 · 타이머 ID 등', 'DOM references · Timer IDs')],
      [P('하위 트리의 공통 값', 'Values shared in a subtree'), 'useContext', P('Provider가 제공한 문맥 읽기', 'Read context from a Provider')],
      [P('복잡한 상태 전이', 'Complex state transitions'), 'useReducer', P('여러 변경 규칙을 reducer로 모으기', 'Collect update rules in a reducer')],
      [P('측정된 반복 계산 비용', 'Measured repeated computation cost'), 'useMemo · useCallback', P('계산 결과 · 함수 참조 캐시 · 정확성의 전제 아님', 'Cache results or function references · Not required for correctness')]),
    layout='single', sources=[pdf(16), doc('React · Hooks', 'https://react.dev/reference/react/hooks'), src('src/pages/AdminPage.jsx')])
add('restore-likes', P('좋아요 저장값의 복원', 'Restoring Saved Likes'),
    P('카드 마운트와 맛집 의존성 변경 시 저장값 조회', 'Read saved values on mount and when restaurant dependencies change'),
    K(P('RestaurantCard.jsx · useEffect 발췌', 'RestaurantCard.jsx · useEffect excerpt'), """
useEffect(() => {
  try {
    const likedRestaurants = JSON.parse(
      localStorage.getItem('likedRestaurants') || '[]'
    );
    if (likedRestaurants.includes(restaurant.id)) {
      setLiked(true);
    }
    const savedLikes = JSON.parse(
      localStorage.getItem('restaurantLikes') || '{}'
    );
    if (savedLikes[restaurant.id] !== undefined) {
      setLikes(savedLikes[restaurant.id]);
    }
  } catch (error) {
    console.error('LocalStorage read error:', error);
  }
}, [restaurant.id, restaurant.likes]);
"""),
    C((P('likedRestaurants - 선택한 ID 목록', 'likedRestaurants - Selected IDs'), [P('includes(id)로 현재 맛집 선택 여부 확인', 'Check the current restaurant with includes(id)')]),
      (P('restaurantLikes - ID별 개수', 'restaurantLikes - Count by ID'), [P('저장된 개수가 0인 경우도 복원', 'Restore a saved count even when it is 0')]),
      (P('State 갱신 - 복원 결과를 화면에 반영', 'State update - Show the restored result'), [P('새로고침 후 동일 브라우저에서 확인', 'Verify after reloading in the same browser')])),
    layout='code', sources=[src('src/components/RestaurantCard.jsx'), EFFECT],
    note='실제 Effect 발췌. 로그 문자열만 영문 축약. id 변경 시 미선택을 false로 초기화하는 일반화된 구현은 아니며 목록은 id 기반 key로 카드 인스턴스를 구분.')
add('storage-keys', P('저장 키와 사이트 주소의 관계', 'Storage Keys and Site Origins'),
    P('프로토콜 · 호스트 · 포트가 같은 출처 안에서 유지되는 데이터', 'Data persists within an origin defined by scheme, host, and port'),
    T([P('키', 'Key'), P('내용', 'Contents'), P('확인 위치', 'Inspect In')],
      ['likedRestaurants', P('선택한 맛집 ID 배열', 'Array of liked IDs'), 'RestaurantCard.jsx'],
      ['restaurantLikes', P('ID별 좋아요 개수 객체', 'Object of like counts by ID'), 'RestaurantCard.jsx'],
      ['pwd-week5-restaurants', P('관리 기능으로 저장한 맛집 목록', 'Restaurant list saved by management actions'), 'services/api.jsx'],
      ['pwd-week5-submissions', P('제보 목록과 처리 상태', 'Submissions and their status'), 'services/api.jsx']),
    C((P('같은 출처 - 새로고침 뒤 유지', 'Same origin - Persists across reloads'), [P('주소의 #/list와 #/submit은 같은 저장 공간', '#/list and #/submit use the same storage')]),
      (P('다른 출처 - 별도 저장 공간', 'Different origins - Separate stores'), [P('localhost · 배포 주소 · Preview 주소는 서로 분리', 'localhost, production, and preview URLs are separate')])),
    sources=[STORAGE, src('src/services/api.jsx')])
add('practice-storage', P('실습 3 · 저장과 새로고침 확인', 'Practice 3 · Storage and Reloads'),
    P('DevTools에서 화면 상태와 저장 데이터를 함께 확인', 'Inspect UI state and saved data together in DevTools'),
    S((P('좋아요 선택', 'Like one restaurant'), P('맛집 한 개 선택 후 개수 기록', 'Like one restaurant and note its count')),
      (P('저장 키 확인', 'Inspect storage keys'), P('Application → Local Storage → 현재 사이트 선택', 'Application → Local Storage → Current site')),
      (P('새로고침', 'Reload the page'), P('likedRestaurants와 restaurantLikes의 값 유지 확인', 'Verify likedRestaurants and restaurantLikes persist')),
      (P('다른 브라우저 비교', 'Compare another browser'), P('동일 URL에서도 별도 브라우저 저장값 사용', 'Even the same URL uses separate browser storage'))),
    C((P('빈 저장소 - 정상 초기 상태', 'Empty storage - A normal initial state'), [P('맛집 목록은 초기 데이터로 표시', 'The list falls back to initial sample data')]),
      (P('실습 초기화 - 관련 키만 삭제', 'Practice reset - Remove only relevant keys'), [P('실습 사이트의 네 개 키 삭제 후 새로고침', 'Delete the four practice keys at the practice origin, then reload'), P('저장된 제보 · 수정 내용도 함께 초기화', 'This also resets saved submissions and edits')])),
    sources=[STORAGE, src('src/services/api.jsx')])

CH = P('06 · 데이터 조회와 라우팅', '06 · DATA QUERIES AND ROUTING')
add('ecosystem', P('실습 라이브러리의 역할', 'Libraries Used in the Practice'),
    P('필요한 기능을 React 주변 라이브러리로 조합', 'Compose supporting libraries around React'),
    T([P('기능', 'Feature'), P('라이브러리', 'Library'), P('실습 사용', 'Use in This App')],
      [P('URL과 화면 연결', 'URL-to-screen mapping'), 'react-router-dom', 'HashRouter · Routes · Link · useParams'],
      [P('조회 · 캐시 · 갱신', 'Queries · Cache · Updates'), '@tanstack/react-query', 'useQuery · useMutation'],
      [P('입력과 검증', 'Inputs and validation'), 'react-hook-form', 'register · handleSubmit · errors'],
      [P('스타일과 피드백', 'Styles and feedback'), 'Emotion · Toastify · Icons · Spinners', P('스타일 · 알림 · 아이콘 · 로딩 표시', 'Styles · Toasts · Icons · Loading indicators')],
      ['HTTP', 'axios', P('의존성에 포함 · 현재 서비스 계층에서 미사용', 'Installed dependency · Unused in the current service layer')]),
    layout='single', sources=[pdf(18), src('package.json'), src('src/services/api.jsx')])
add('app-providers', P('App의 Provider와 공통 화면', 'Providers and Shared UI in App'),
    P('공통 기능을 최상위에 배치하고 페이지에서 사용', 'Place shared capabilities above the pages that use them'),
    K(P('App.jsx · 구조 축약', 'App.jsx · Structural outline'), """
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <HashRouter>
        <GlobalStyles />
        <Header />
        <Routes>{/* Page routes */}</Routes>
        <ToastContainer />
      </HashRouter>
    </QueryClientProvider>
  );
}
"""),
    C((P('QueryClientProvider - 조회 캐시 공유', 'QueryClientProvider - Share the query cache'), [P('컴포넌트 밖에서 QueryClient 생성', 'Create QueryClient outside the component')]),
      (P('HashRouter - 라우팅 문맥 제공', 'HashRouter - Provide routing context'), [P('내부에서 Link · Routes · useParams 사용', 'Use Link, Routes, and useParams inside it')]),
      (P('공통 컴포넌트 - 모든 페이지의 기반', 'Shared components - UI across pages'), [P('Header · GlobalStyles · ToastContainer', 'Header · GlobalStyles · ToastContainer')])),
    layout='code', sources=[src('src/App.jsx')])
add('service-layer', P('가상 API의 비동기 인터페이스', 'The Mock API’s Async Interface'),
    P('HTTP 요청 없이 Promise와 data 객체를 반환하는 서비스 계층', 'A service layer returning Promises and data objects without HTTP requests'),
    K(P('services/api.jsx · 핵심 구조 발췌', 'services/api.jsx · Core excerpt'), """
const RESTAURANTS_KEY = 'pwd-week5-restaurants';

export const restaurantAPI = {
  getRestaurants: async () => ({
    data: readItems(RESTAURANTS_KEY, initialRestaurants),
  }),
};
"""),
    C((P('async - Promise 반환', 'async - Return a Promise'), [P('동기적인 localStorage 결과를 비동기 인터페이스로 제공', 'Expose synchronous storage through an async interface')]),
      (P('readItems - 저장값 또는 초기값', 'readItems - Saved data or fallback'), [P('키가 없으면 initialRestaurants의 복제 반환', 'Return a clone of initialRestaurants when the key is absent')]),
      (P('data - 응답의 목록 필드', 'data - The list inside the response'), [P('useQuery의 data 안에 서비스 응답의 data 존재', 'Query data contains another data field from the service')])),
    layout='code', sources=[src('src/services/api.jsx')])
add('use-query', P('useQuery의 조회와 캐시 키', 'Queries and Cache Keys with useQuery'),
    P('조회 함수 · 결과 · 진행 상태를 하나의 Hook으로 연결', 'Connect a query function, result, and progress state in one Hook'),
    K(P('ListPage.jsx · 실제 조회 설정', 'ListPage.jsx · Query configuration'), """
const { data, isLoading, error } = useQuery({
  queryKey: ['restaurants'],
  queryFn: restaurantAPI.getRestaurants,
});

const restaurants = data?.data || [];
"""),
    C((P('queryKey - 캐시의 식별자', 'queryKey - Identity of cached data'), [P('같은 키를 쓰는 화면에서 조회 결과 공유', 'Views with the same key share cached results')]),
      (P('queryFn - 실행할 조회 함수', 'queryFn - The function to run'), [P('함수를 전달 · Promise가 반환되거나 오류 발생', 'Pass a function that returns a Promise or throws')]),
      (P('data?.data - 아직 없는 응답 처리', 'data?.data - Handle an absent response'), [P('조회 전 undefined 가능 · 목록 기본값 []', 'May be undefined before success · Default list []')])),
    layout='code', sources=[QUERY, src('src/pages/ListPage.jsx')])
add('query-states', P('로딩 · 오류 · 빈 목록의 구분', 'Loading, Error, and Empty States'),
    P('조회 상태와 조회된 데이터의 개수를 별도로 판단', 'Evaluate query status separately from the result count'),
    K(P('ListPage와 RestaurantList · 구조 축약', 'ListPage and RestaurantList · Outline'), """
if (isLoading) return <p>Loading...</p>;
if (error) return <p>{error.message}</p>;

const restaurants = data?.data || [];

if (restaurants.length === 0) {
  return <p>No results.</p>;
}

return <RestaurantList restaurants={restaurants} />;
"""),
    C((P('로딩 - 결과 대기', 'Loading - Waiting for a result'), [P('ClipLoader와 안내 문구 표시', 'Show ClipLoader and a loading message')]),
      (P('오류 - 조회 실패', 'Error - The query failed'), [P('잘못된 저장 데이터의 JSON 오류도 포함', 'Includes malformed JSON in saved data')]),
      (P('빈 목록 - 성공한 조회의 0개 결과', 'Empty - A successful query with no results'), [P('목록 자체가 비었거나 필터 결과가 0개', 'The data is empty or the filter matches nothing')]),
      (P('빠른 조회 - 로딩 표시 생략 가능', 'Fast queries - Loading may be imperceptible'), [P('로컬 데이터는 빠르게 완료되어 관찰이 어려울 수 있음', 'Local queries may finish too quickly to observe')])),
    layout='code', sources=[src('src/pages/ListPage.jsx'), src('src/components/RestaurantList.jsx')])
add('query-settings', P('캐시의 유효 시간과 재조회', 'Freshness and Query Refreshes'),
    P('저장 데이터와 메모리 캐시의 서로 다른 수명', 'Persistent data and the in-memory cache have different lifetimes'),
    K(P('App.jsx · QueryClient 설정 발췌', 'App.jsx · QueryClient options'), """
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
    },
  },
});
"""),
    C((P('staleTime - 5분간 신선한 데이터', 'staleTime - Fresh data for five minutes'), [P('5분 뒤 자동 삭제 또는 정기 조회를 뜻하지 않음', 'Does not mean automatic deletion or five-minute polling')]),
      (P('retry - 실패 후 추가 시도', 'retry - Additional attempts after failure'), [P('조회 실패 시 한 번 재시도', 'Retry a failed query once')]),
      (P('invalidateQueries - 오래된 결과 표시', 'invalidateQueries - Mark results as stale'), [P('변경 후 관련 캐시 무효화 · 활성 조회 재실행', 'Invalidate related cache after a change · Refetch active queries')])),
    layout='code', sources=[src('src/App.jsx'), INVALIDATE])
add('routes', P('HashRouter와 페이지 경로', 'HashRouter and Page Routes'),
    P('URL의 해시 영역으로 현재 화면을 식별하는 실습 구조', 'The practice app identifies its screen through the URL hash'),
    T([P('접속 주소의 끝부분', 'URL Ending'), P('Route path', 'Route Path'), P('페이지', 'Page')],
      ['/#/', '/', 'HomePage'],
      ['/#/list', '/list', 'ListPage'],
      ['/#/restaurant/1', '/restaurant/:id', 'DetailPage'],
      ['/#/popular', '/popular', 'PopularPage'],
      ['/#/submit', '/submit', 'SubmitPage'],
      ['/#/admin · /#/submissions', '/admin · /submissions', 'AdminPage · SubmissionsPage']),
    layout='single', sources=[src('src/App.jsx'), ROUTER],
    note='표의 두 관리 경로는 학습용이며 실제 인증이나 권한 검증이 구현되어 있지 않음.')
add('links-detail', P('Link와 동적 경로의 id', 'Links and Dynamic Route IDs'),
    P('카드의 식별자를 URL에 넣고 상세 페이지에서 다시 읽기', 'Put a card’s ID in the URL and read it on the detail page'),
    K(P('개념 예제 · 카드에서 상세 조회까지', 'Teaching example · From card to detail query'), """
<Link to={'/restaurant/' + restaurant.id}>
  Details
</Link>;

const { id } = useParams();

const { data, isLoading, error } = useQuery({
  queryKey: ['restaurant', id],
  queryFn: () => restaurantAPI.getRestaurantById(id),
});
"""),
    C((P('Link - 앱 안의 화면 이동', 'Link - Navigation within the app'), [P('to에는 /restaurant/1 · #은 Router가 처리', 'Use /restaurant/1 in to · The router handles #')]),
      (P('useParams - URL 값 읽기', 'useParams - Read URL parameters'), [P('id는 문자열 · 서비스에서 String(id)로 비교', 'id is a string · The service compares String(id)')]),
      (P('queryKey - 맛집마다 다른 결과', 'queryKey - A distinct result per restaurant'), [P('id를 포함해 1번과 2번의 캐시 구분', 'Include id to distinguish cached restaurants 1 and 2')])),
    layout='code', sources=[src('src/pages/DetailPage.jsx'), src('src/components/RestaurantCard.jsx'), QUERY])
add('practice-routing', P('실습 4 · 상세와 인기 화면 확인', 'Practice 4 · Detail and Ranking Pages'),
    P('화면 이동 · 직접 접속 · 없는 데이터의 결과 점검', 'Check navigation, direct access, and missing-data behavior'),
    I('detail', '송림식당 상세 정보 화면', 'Songnim restaurant detail screen'),
    S((P('상세 정보 확인', 'Check restaurant details'), P('첫 카드의 상세보기 → 이름 · 위치 · 추천 메뉴', 'Open the first card → Name, location, and menu')),
      (P('직접 접속과 새로고침', 'Direct access and reload'), P('/#/restaurant/1을 새 탭에서 열고 새로고침', 'Open /#/restaurant/1 in a new tab and reload')),
      (P('없는 id 확인', 'Try a missing ID'), P('/#/restaurant/missing → 맛집을 찾을 수 없음', '/#/restaurant/missing → Restaurant not found')),
      (P('인기 순위 확인', 'Check the ranking'), P('초기 데이터는 평점 순 3개 · 좋아요와 별도', '3 initial entries in rating order · Independent of likes'))),
    layout='visual', sources=[src('src/pages/DetailPage.jsx'), src('src/services/api.jsx')])

CH = P('07 · 폼 입력과 데이터 변경', '07 · FORMS AND DATA MUTATIONS')
add('form-flow', P('제보 폼의 처리 단계', 'Submission Form Processing'),
    P('입력 등록 → 검증 → 정규화 → 저장 → 결과 표시', 'Register inputs → Validate → Normalize → Save → Show the result'),
    I('submit', '맛집 이름과 카테고리 등 제보 입력 폼', 'Restaurant submission form with name, category, and other fields'),
    C((P('필수 입력 - 제보의 기본 정보', 'Required inputs - Basic submission data'), [P('맛집 이름 · 카테고리 · 위치', 'Restaurant name · Category · Location')]),
      (P('선택 입력 - 추가 설명', 'Optional inputs - Extra detail'), [P('가격대 · 추천 메뉴 · 후기 · 제보자 정보', 'Price range · Menu · Review · Submitter information')]),
      (P('제출 결과 - 저장 성공 후 표시', 'Result - Shown after a successful save'), [P('성공 화면 · 토스트 · 입력 초기화', 'Success view · Toast · Form reset')])),
    layout='visual', sources=[src('src/components/SubmitRestaurant.jsx')])
add('register', P('useForm과 입력 등록', 'useForm and Input Registration'),
    P('입력 이름과 검증 규칙을 register에 함께 지정', 'Register an input name together with validation rules'),
    K(P('SubmitRestaurant.jsx · 입력 구조 축약', 'SubmitRestaurant.jsx · Input outline'), """
const {
  register,
  handleSubmit,
  formState: { errors, isSubmitting },
  reset,
} = useForm();

<input
  {...register('restaurantName', {
    required: 'Restaurant name is required',
  })}
/>;
"""),
    C((P('register - 입력과 폼 상태 연결', 'register - Connect an input to form state'), [P('이름 · 변경 핸들러 · ref 등을 입력에 전달', 'Provide the name, change handler, ref, and related props')]),
      (P('전개 구문 - 속성 묶음 적용', 'Spread syntax - Apply the returned props'), [P('{...register(...)}를 input에 적용', 'Apply {...register(...)} to the input')]),
      (P('required - 빈 값 검증', 'required - Validate missing input'), [P('오류 문구는 errors.restaurantName.message', 'Read the error at errors.restaurantName.message')])),
    layout='code', sources=[src('src/components/SubmitRestaurant.jsx'), FORM])
add('form-submit', P('폼 제출과 중복 클릭 처리', 'Form Submission and Repeated Clicks'),
    P('검증을 통과한 값만 onSubmit으로 전달', 'Pass validated values to onSubmit'),
    K(P('SubmitRestaurant.jsx · 폼 구조 축약', 'SubmitRestaurant.jsx · Form outline'), """
<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('restaurantName', { required: true })} />
  {errors.restaurantName && <p>Name is required.</p>}

  <button type="submit" disabled={isSubmitting}>
    {isSubmitting ? 'Submitting...' : 'Submit'}
  </button>
</form>;
"""),
    C((P('handleSubmit - 검증 후 제출 실행', 'handleSubmit - Validate, then submit'), [P('오류가 있으면 onSubmit 실행 대신 오류 표시', 'On validation failure, show errors instead of calling onSubmit')]),
      (P('isSubmitting - 비동기 제출 진행 상태', 'isSubmitting - Async submission progress'), [P('제출 함수의 Promise 완료까지 버튼 비활성화', 'Disable the button until the submission Promise settles')]),
      (P('이벤트 제어 - 서로 다른 두 동작', 'Event control - Two distinct operations'), [P('preventDefault: 기본 동작 취소', 'preventDefault: Cancel the default action'), P('stopPropagation: 부모로의 이벤트 전파 중단', 'stopPropagation: Stop propagation to ancestors')])),
    layout='code', sources=[src('src/components/SubmitRestaurant.jsx'), src('src/components/RestaurantCard.jsx')])
add('normalization', P('입력 문자열과 저장 데이터', 'Input Strings and Stored Data'),
    P('추천 메뉴 문자열을 배열로 바꾸고 불필요한 공백 제거', 'Convert menu text into an array and remove surrounding whitespace'),
    K(P('SubmitRestaurant.jsx · 정규화 축약', 'SubmitRestaurant.jsx · Normalization outline'), r"""
const recommendedMenuArray = data.recommendedMenu
  .split(/[\n,]/)
  .map((item) => item.trim())
  .filter(Boolean);

const payload = {
  restaurantName: data.restaurantName?.trim(),
  category: data.category,
  location: data.location?.trim(),
  recommendedMenu: recommendedMenuArray,
};
""", 'javascript'),
    C((P('split - 쉼표와 줄바꿈으로 분리', 'split - Separate by commas or newlines'), [P('김치찌개, 순두부 → 두 개 항목', 'Kimchi stew, soft tofu → Two items')]),
      (P('trim · filter - 항목 정리', 'trim · filter - Clean the items'), [P('양끝 공백 제거 · 비어 있는 항목 제거', 'Trim surrounding spaces · Remove empty items')]),
      (P('데이터 계약 - 필드 이름과 타입', 'Data contract - Field names and types'), [P('제보는 restaurantName · 맛집은 name', 'Submissions use restaurantName · Restaurants use name'), P('실제 파일에는 입력 타입별 분기와 선택 필드 포함', 'The full file also handles input types and optional fields')])),
    layout='code', sources=[src('src/components/SubmitRestaurant.jsx')])
add('save-submission', P('제보 저장과 성공·실패 처리', 'Saving Submissions and Handling Results'),
    P('저장 완료를 확인한 뒤 성공 화면과 입력 초기화 수행', 'Show success and reset inputs after the save completes'),
    K(P('SubmitRestaurant.jsx · 저장 단계 발췌', 'SubmitRestaurant.jsx · Save-stage excerpt'), """
try {
  await submissionAPI.createSubmission(payload);
  setSubmitted(true);
  toast.success('Submission saved');
  reset();
  setTimeout(() => setSubmitted(false), 5000);
} catch {
  toast.error('Submission failed');
}
"""),
    C((P('await - 저장 성공까지 대기', 'await - Wait for the save'), [P('실패한 Promise는 catch에서 처리', 'Handle a rejected Promise in catch')]),
      (P('성공 - 화면과 입력 상태 변경', 'Success - Update the view and inputs'), [P('성공 안내 · 입력값 초기화 · 5초 뒤 폼 복원', 'Show success · Reset inputs · Restore the form after 5 seconds')]),
      (P('실패 - 성공 안내 생략', 'Failure - Do not show success'), [P('localStorage 쓰기 실패는 서비스에서 호출자에게 전달', 'The service propagates storage write failures to its caller')])),
    layout='code', sources=[src('src/components/SubmitRestaurant.jsx'), src('src/services/api.jsx')])
add('submission-record', P('제보 객체와 저장 키', 'Submission Records and Storage Keys'),
    P('입력 데이터에 식별자와 대기 상태를 붙여 저장', 'Add an identifier and pending status before saving'),
    K(P('services/api.jsx · createSubmission 발췌', 'services/api.jsx · createSubmission excerpt'), """
const createSubmission = async (payload) => {
  const items = readItems(SUBMISSIONS_KEY);
  const item = {
    ...payload,
    id: crypto.randomUUID(),
    status: 'pending',
  };
  writeItems(SUBMISSIONS_KEY, [...items, item]);
  return { data: item };
};
""", 'javascript'),
    C((P('id - 제보의 식별자', 'id - Submission identity'), [P('crypto.randomUUID()로 새 문자열 ID 생성', 'Create a new string ID with crypto.randomUUID()')]),
      (P('status - 처리 상태', 'status - Processing status'), [P('pending → approved 또는 rejected', 'pending → approved or rejected')]),
      (P('별도 목록 - 제보와 맛집 구분', 'Separate lists - Submissions and restaurants'), [P('제보 저장만으로 맛집 목록에 즉시 추가되지 않음', 'Saving a submission does not immediately add a restaurant')])),
    layout='code', sources=[src('src/services/api.jsx')])
add('practice-form', P('실습 5 · 제보 검증과 저장 확인', 'Practice 5 · Validation and Saving'),
    P('정상 입력과 실패 입력을 모두 재현하는 폼 점검', 'Exercise both valid and invalid form input'),
    T([P('실행', 'Action'), P('기대 결과', 'Expected Result'), P('확인 대상', 'Inspect')],
      [P('필수 입력 없이 제출', 'Submit without required inputs'), P('검증 오류 · 저장 없음', 'Validation errors · No saved record'), 'errors · Local Storage'],
      [P('가상 맛집 정보 입력', 'Enter fictional restaurant data'), P('성공 안내와 폼 초기화', 'Success message and form reset'), 'submitted · reset()'],
      [P('추천 메뉴 두 개 입력', 'Enter two menu items'), P('문자열이 배열 두 항목으로 저장', 'Text saved as an array of two items'), 'recommendedMenu'],
      [P('새로고침 후 키 확인', 'Reload and inspect storage'), P('제보와 pending 상태 유지', 'Submission and pending status remain'), 'pwd-week5-submissions'],
      [P('/#/submissions 접속', 'Open /#/submissions'), P('대기 목록에 제보 표시', 'Submission appears in Pending'), 'SubmissionsPage.jsx']),
    layout='single', sources=[src('src/components/SubmitRestaurant.jsx'), src('src/pages/SubmissionsPage.jsx')])
add('mutation', P('관리 기능과 useMutation', 'Management Actions and useMutation'),
    P('데이터 변경 요청과 변경 후 목록 갱신의 연결', 'Connect a data mutation to a refreshed list'),
    K(P('AdminPage.jsx · 생성 설정 발췌', 'AdminPage.jsx · Create mutation excerpt'), """
const createMutation = useMutation({
  mutationFn: restaurantAPI.createRestaurant,
  onSuccess: () => {
    toast.success('Created');
    queryClient.invalidateQueries({
      queryKey: ['restaurants'],
    });
    reset();
  },
});
"""),
    C((P('mutationFn - 변경 함수', 'mutationFn - A function that changes data'), [P('create · update · delete 함수 연결', 'Connect create, update, and delete functions')]),
      (P('onSuccess - 저장 이후 처리', 'onSuccess - Work after a successful write'), [P('알림 표시 · 관련 목록 캐시 갱신', 'Show feedback · Refresh the related list cache')]),
      (P('학습용 관리 화면 - 인증 없음', 'Practice management UI - No authentication'), [P('/#/admin과 /#/submissions는 접근 제한 없는 예제', '/#/admin and /#/submissions have no access restrictions')])),
    layout='code', sources=[src('src/pages/AdminPage.jsx'), INVALIDATE])
add('approve-flow', P('제보 승인과 맛집 데이터 변환', 'Approvals and Restaurant Data Mapping'),
    P('제보 필드를 맛집 필드로 바꾸어 등록하는 과정', 'Map submission fields to a restaurant record'),
    T([P('제보 필드', 'Submission Field'), P('맛집 필드', 'Restaurant Field'), P('처리', 'Processing')],
      ['restaurantName', 'name', P('이름 필드 변환', 'Rename the field')],
      ['review', 'description', P('후기를 소개로 사용', 'Use the review as the description')],
      ['recommendedMenu', 'recommendedMenu', P('배열 형태 유지', 'Preserve the array')]),
    C((P('status - 원래 제보의 처리 상태', 'status - Status on the original submission'), [P('맛집 등록 후 제보를 pending → approved로 갱신', 'After creating the restaurant, update the submission to approved')]),
      (P('조회 갱신 - 관련 캐시 선택', 'Refresh - Select related cache keys'), [P('현재 승인 코드는 submissions · restaurants 무효화', 'Approval invalidates submissions and restaurants'), P('상세 · 인기 캐시는 별도 키이므로 추가 갱신 필요 가능', 'Detail and ranking use separate keys that may need invalidation')]),
      (P('두 번의 저장 - 원자적 처리 없음', 'Two writes - No atomic transaction'), [P('맛집 생성과 제보 상태 저장 사이 실패 가능', 'Failure is possible between restaurant creation and status update')])),
    layout='visual', sources=[src('src/pages/SubmissionsPage.jsx'), src('src/services/api.jsx')])
add('styling', P('Emotion과 화면 피드백', 'Emotion and UI Feedback'),
    P('상태에 따른 스타일과 사용자 동작의 결과 표현', 'Express state through styles and interaction feedback'),
    T([P('표현', 'Presentation'), P('실습 구현', 'Implementation'), P('관찰', 'Observation')],
      [P('선택된 카테고리', 'Selected category'), 'FilterButton · active', P('배경색과 글자색 변경', 'Background and text colors change')],
      [P('좋아요 상태', 'Liked state'), 'LikeButton · $liked', P('선택과 취소에 따른 버튼 색상', 'Button color follows the choice')],
      [P('저장 성공 · 실패', 'Save success or failure'), 'toast.success · toast.error', P('오른쪽 아래 알림', 'Bottom-right notification')],
      [P('반응형 목록', 'Responsive list'), 'grid · auto-fill · minmax', P('화면 폭에 맞춰 카드 열 수 변경', 'Card column count changes with width')]),
    layout='single', sources=[src('src/components/RestaurantCard.jsx'), src('src/components/RestaurantList.jsx')])

CH = P('08 · 빌드 · 배포 · 실습 완료', '08 · BUILD, DEPLOYMENT, AND COMPLETION')
add('serverless', P('정적 호스팅과 서버리스 기능', 'Static Hosting and Serverless Features'),
    P('배포 플랫폼의 기능과 이번 앱이 실제 사용하는 기능의 구분', 'Distinguish platform capabilities from features used by this app'),
    T([P('구분', 'Type'), P('처리 위치와 역할', 'Execution and Role'), P('이번 실습', 'This Practice')],
      [P('정적 호스팅', 'Static hosting'), P('빌드한 HTML · CSS · JS 파일 제공', 'Serve built HTML, CSS, and JavaScript'), P('Vercel에서 dist 파일 배포', 'Deploy dist files on Vercel')],
      [P('브라우저 실행', 'Browser execution'), P('React 화면 계산 · 입력 처리 · localStorage', 'React UI · Input handling · localStorage'), P('이번 앱의 조회 · 저장 처리', 'Queries and storage in this app')],
      [P('서버리스 함수', 'Serverless functions'), P('관리형 서버 환경에서 요청별 코드 실행', 'Run request-handling code on managed infrastructure'), P('함수 코드 미구현', 'No function code implemented')],
      [P('관리형 데이터 서비스', 'Managed data services'), P('여러 사용자가 공유하는 DB · 인증 · 파일 저장', 'Shared database, authentication, and file storage'), P('브라우저 저장과 별도 구성 필요', 'Requires setup beyond browser storage')]),
    layout='single', sources=[pdf(21), VERCEL])
add('pdf-deployment', P('원본 PDF와 현재 실습의 배포', 'Original PDF and Current Deployment'),
    P('React 개념은 유지하고 배포와 제보 저장은 현재 소스로 적용', 'Retain the React concepts and follow the current deployment and storage code'),
    T([P('항목', 'Item'), P('원본 PDF', 'Original PDF'), P('이번 실습', 'This Practice')],
      [P('호스팅', 'Hosting'), 'Netlify', 'Vercel · Vite'],
      [P('폼 저장', 'Form storage'), 'Netlify Forms', 'localStorage · submissionAPI'],
      [P('화면 라우팅', 'Screen routing'), 'BrowserRouter', P('실제 src/App.jsx의 HashRouter', 'HashRouter in the actual src/App.jsx')],
      [P('서버 기능', 'Server features'), P('Forms · 서버리스 개념 소개', 'Forms · Serverless introduction'), P('정적 파일 배포 · 브라우저에서 앱 실행', 'Static files deployed · App runs in the browser')]),
    layout='single', sources=[pdf(20), pdf(21), pdf(22), src('src/App.jsx'), VERCEL],
    note='Netlify Forms의 hidden form·POST 예제는 현재 코드와 맞지 않으므로 실행 절차에 포함하지 않음. 정적 프론트엔드 배포 자체를 서버리스 함수 구현으로 설명하지 않음.')
add('build-preview', P('빌드와 배포 전 미리보기', 'Build and Preview Before Deployment'),
    P('개발 서버가 아닌 dist 결과물로 기능 확인', 'Verify features using the built dist output'),
    K(P('터미널 · pwd-week5 프로젝트 루트', 'Terminal · pwd-week5 project root'), """
npm run lint
npm run build
npm run preview
""", 'bash'),
    S((P('lint - 코드 규칙 점검', 'lint - Check code rules'), P('오류가 있는 파일과 줄 확인 · 수정 후 재실행', 'Inspect the reported file and line · Fix and rerun')),
      (P('build - 배포 파일 생성', 'build - Produce deployment files'), P('dist/ 생성 · import와 파일명 오류 확인', 'Generate dist/ · Check imports and filenames')),
      (P('preview - 빌드 결과 실행', 'preview - Run the built output'), P('터미널의 URL 접속 · 기본 포트 4173', 'Open the terminal URL · Default port 4173')),
      (P('기능 재확인', 'Verify features again'), P('목록 · 필터 · 상세 · 좋아요 · 제보 · 새로고침', 'List · Filter · Detail · Likes · Submit · Reload'))),
    layout='code', sources=[src('package.json'), doc('Vite · Static Deploy', 'https://vite.dev/guide/static-deploy.html')])
add('git-own-repo', P('개인 GitHub 저장소 연결', 'Connecting a Personal GitHub Repository'),
    P('완성 저장소를 복제한 경우 자신의 저장소로 origin 변경', 'After cloning the practice repository, point origin to your own repository'),
    K(P('터미널 · YOUR_USERNAME을 본인 계정으로 변경', 'Terminal · Replace YOUR_USERNAME with your account'), """
git remote -v

git remote set-url origin \\
  https://github.com/YOUR_USERNAME/pwd-week5.git
git add .
git commit -m "Customize campus foodmap"
git push -u origin main
""", 'bash', width=80),
    S((P('원격 저장소 생성', 'Create the remote repository'), P('GitHub에 빈 pwd-week5 저장소 생성', 'Create an empty pwd-week5 repository on GitHub')),
      (P('원격 주소 확인', 'Inspect the remote URL'), P('git remote -v로 자신의 계정 주소 확인', 'Check that git remote -v shows your own account')),
      (P('변경 기록과 업로드', 'Commit and upload changes'), P('수정 파일 커밋 · main 브랜치 push', 'Commit edited files · Push the main branch')),
      (P('신규 프로젝트의 차이', 'For a new project'), P('원격이 없으면 git init 후 remote add origin 사용', 'If there is no remote, use git init and remote add origin'))),
    layout='code', sources=[src('README.md')],
    note='기존 origin의 원본 수업 저장소에 push하도록 안내하지 않음. 커밋 명령은 실제 변경 파일이 있을 때 수행.')
add('vercel-settings', P('Vercel 프로젝트와 빌드 설정', 'Vercel Project and Build Settings'),
    P('GitHub 저장소를 가져와 Vite 빌드 결과 배포', 'Import the GitHub repository and deploy the Vite build'),
    T([P('설정', 'Setting'), P('값', 'Value'), P('확인 기준', 'Check')],
      ['Framework Preset', 'Vite', P('프레임워크 자동 감지 결과', 'The detected framework')],
      ['Root Directory', P('프로젝트 루트', 'Project root'), P('package.json이 있는 디렉터리', 'Directory containing package.json')],
      ['Build Command', 'npm run build', P('로컬에서 성공한 빌드 명령', 'The build command verified locally')],
      ['Output Directory', 'dist', P('Vite가 만든 배포 파일', 'Output generated by Vite')],
      ['Node.js · Branch', '24.x · main', P('package.json · 실제 기본 브랜치와 일치', 'Match package.json and the actual default branch')],
      ['Environment Variables', P('이번 실습에서는 없음', 'None for this practice'), P('외부 API 주소나 DB 연결 없음', 'No external API or database connection')]),
    layout='single', sources=[src('vercel.json'), src('package.json'), VERCEL])
add('vercel-deploy', P('Vercel 배포와 변경 반영', 'Deploying and Updating on Vercel'),
    P('최초 Import · 배포 로그 · 서비스 주소 · Git 연동 확인', 'Check import, build logs, the service URL, and Git integration'),
    S((P('프로젝트 가져오기', 'Import the project'), P('Vercel → Add New → Project → 자신의 GitHub 저장소', 'Vercel → Add New → Project → Your GitHub repository')),
      (P('설정 확인 후 Deploy', 'Review settings and deploy'), P('Vite · build · dist · Node 설정 확인', 'Check Vite, build, dist, and Node settings')),
      (P('배포 로그와 주소 확인', 'Inspect logs and the URL'), P('빌드 성공 후 실제 할당된 Production 주소 접속', 'After a successful build, open the assigned production URL')),
      (P('변경 반영 확인', 'Verify an update'), P('HomePage 문구 수정 → commit · push → 새 배포 확인', 'Edit HomePage text → Commit and push → Check the new deployment'))),
    C((P('배포 명령 - 대시보드와 Git 연동', 'Deployment - Dashboard and Git integration'), [P('저장소의 npm run deploy는 GitHub Pages용', 'The repository’s npm run deploy targets GitHub Pages'), P('Vercel 실습에서는 대시보드 Deploy 사용', 'Use the dashboard Deploy action for this practice')]),
      (P('데이터 - 배포 주소에서 새로 시작', 'Data - A separate store at the deployment URL'), [P('로컬의 좋아요와 제보는 자동 이전되지 않음', 'Local likes and submissions do not migrate automatically')])),
    sources=[src('README.md'), src('package.json'), VERCEL])
add('routing-deploy', P('배포 주소와 새로고침 처리', 'Deployed URLs and Reloads'),
    P('HashRouter와 BrowserRouter의 요청 경로 차이', 'HashRouter and BrowserRouter use different request paths'),
    T([P('방식', 'Router'), P('상세 주소', 'Detail URL'), P('새로고침 동작', 'Reload Behavior')],
      ['HashRouter', '/#/restaurant/1', P('서버에는 / 요청 · # 뒤 경로는 브라우저 처리', 'Server receives / · The browser handles the hash')],
      ['BrowserRouter', '/restaurant/1', P('서버에도 상세 경로 요청 · SPA rewrite 필요', 'Server receives the detail path · Requires an SPA rewrite')]),
    K(P('vercel.json · 제공된 SPA rewrite', 'vercel.json · Provided SPA rewrite'), """
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
""", 'json'),
    sources=[src('src/App.jsx'), src('vercel.json'), ROUTER, VERCEL])
add('troubleshooting', P('실습 오류와 확인 순서', 'Troubleshooting the Practice'),
    P('에러 메시지 → 관련 파일 → 실행 조건 순서로 원인 확인', 'Inspect the error message, related file, and execution conditions'),
    T([P('증상', 'Symptom'), P('우선 확인', 'First Check'), P('조치', 'Action')],
      ['package.json ENOENT', P('터미널 현재 폴더', 'Current terminal directory'), P('pwd-week5 폴더로 이동', 'Change to the pwd-week5 folder')],
      ['Module not found', P('파일명 대소문자 · import · 의존성', 'Filename case · Import · Dependencies'), P('실제 파일 경로 확인 · npm ci 재실행', 'Check the actual path · Rerun npm ci')],
      ['Too many re-renders', P('렌더 중 setter 호출', 'Setter called during render'), P('onClick에 함수 전달', 'Pass a function to onClick')],
      [P('제보 미표시', 'Submission missing'), P('현재 출처 · 저장 키 · pending 필터', 'Current origin · Storage key · Pending filter'), P('같은 주소의 Local Storage 확인', 'Inspect Local Storage at the same origin')],
      [P('수정 후 오래된 화면', 'Old data after an edit'), P('조회 캐시의 key와 무효화', 'Query key and invalidation'), P('관련 캐시 갱신 · 새로고침으로 비교', 'Refresh related cache · Compare after reload')]),
    layout='single', sources=[src('src/App.jsx'), src('src/pages/SubmissionsPage.jsx'), src('README.md')])
add('completion', P('실습 완료 기준', 'Practice Completion Criteria'),
    P('코드 · 동작 · 저장 · 배포를 직접 재현할 수 있는 상태', 'Reproducible code, behavior, storage, and deployment'),
    T([P('확인 영역', 'Area'), P('완료 기준', 'Completion Criterion')],
      [P('컴포넌트', 'Components'), P('Props의 데이터가 JSX와 목록에 표시되는 과정 설명', 'Explain how props become JSX and list items')],
      [P('상태와 이벤트', 'State and events'), P('필터 · 좋아요 동작과 새로고침 후 복원 확인', 'Verify filters, likes, and restored values after reload')],
      [P('라우팅과 조회', 'Routing and queries'), P('상세 URL 직접 접속 · 없는 id의 결과 확인', 'Open a detail URL directly · Check a missing ID')],
      [P('폼과 저장', 'Forms and storage'), P('필수 검증 · 정상 제출 · 저장 키와 제보 내용 확인', 'Validate required fields · Submit · Inspect the stored record')],
      [P('빌드와 배포', 'Build and deployment'), P('lint · build 통과 · 배포 URL과 GitHub URL 준비', 'Pass lint and build · Prepare deployment and GitHub URLs')],
      [P('실습 제출 일정', 'Submission deadline'), P('2026. 10. 18. 23:59 · 한국시간 · 실습 README 기준', 'October 18, 2026, 23:59 KST · As listed in the practice README')]),
    layout='single', sources=[src('README.md')])
add('resources', P('실습 코드와 복습 자료', 'Practice Code and Review Resources'),
    P('코드의 실행 결과와 공식 문서를 연결하는 복습 기준', 'Review behavior alongside source code and official documentation'),
    C((P('JSX와 컴포넌트', 'JSX and components'), [P('RestaurantList · RestaurantCard의 props · map · key', 'Props, map, and keys in RestaurantList and RestaurantCard')]),
      (P('상태와 Hooks', 'State and Hooks'), [P('ListPage의 파생값 · RestaurantCard의 State와 Effect', 'Derived data in ListPage · State and Effects in RestaurantCard')]),
      (P('조회와 저장', 'Queries and storage'), [P('services/api.jsx의 응답 · SubmitRestaurant의 입력 처리', 'Service responses in api.jsx · Form handling in SubmitRestaurant')])),
    S((P('실습 저장소', 'Practice repository'), P('하단 pwd-week5 링크에서 전체 코드 확인', 'Open pwd-week5 below for the complete source')),
      (P('학습 자료', 'Learning references'), P('각 슬라이드 하단의 원본 PDF · 공식 문서 확인', 'Use the original PDF and official links under each slide')),
      (P('결과 설명', 'Explain the result'), P('사용자 행동 → 상태 변경 → UI 반영 → 저장의 흐름 설명', 'Explain action → State update → UI update → Storage'))),
    sources=[('pwd-week5', REPO), ('React · Learn', 'https://react.dev/learn'), ('Vercel · Vite', VERCEL[1]), ('Original PDF', PDF)])
