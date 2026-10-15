"""Eight-slide review of the actual pwd-week5 client, in Week 05 format."""


def pair(ko, en):
    return (ko, en)


def code(ident, label):
    return dict(kind='code', ident=ident, label=label)


def screen(name, caption):
    return dict(kind='screen', name=name, caption=caption)


def concept(term, *details):
    return dict(kind='concept', term=term, details=details)


def table(head, rows):
    return dict(kind='table', head=head, rows=rows)


# Each range is an inclusive, verbatim excerpt. Only whitespace is formatted.
EXCERPTS = {
    'entry': ('src/main.tsx', [('const root =', ')')]),
    'routes': ('src/App.tsx', [('<Routes>', '<Route path="/restaurant/:id"'), ('</Routes>', '</Routes>')]),
    'detail-link': ('src/components/RestaurantCard.tsx', [('<DetailLink to=', '</DetailLink>')]),
    'list': ('src/components/RestaurantList.tsx', [('<ListContainer>', '</ListContainer>')]),
    'card': ('src/components/RestaurantCard.tsx', [('<CardHeader>', '</CardHeader>')]),
    'query': ('src/pages/ListPage.tsx', [('const [selectedCategory', 'const [selectedCategory'),
        ('const { data, isLoading, error } = useQuery', '  });'),
        ('const filteredData', ': data?.data.filter')]),
    'menu-input': ('src/components/SubmitRestaurant.tsx', [('const recommendedMenuArray', ': [];')]),
    'submit': ('src/components/SubmitRestaurant.tsx', [('await submissionAPI.createSubmission', '      reset();')]),
    'get-restaurants': ('src/services/api.ts', [('  getRestaurants:', '  }),')]),
}

SLIDES = [
    dict(id='cover', kind='cover', title=pair('실전 웹서비스개발 – 6주차', 'Practical Web Service Development – Week 6'),
         lead=pair('Ajou Campus Foodmap 클라이언트 코드 리뷰', 'Ajou Campus Foodmap Client Code Review')),
    dict(id='project', title=pair('React 프로젝트의 실행 구조', 'React project structure'),
         lead=pair('진입 파일에서 App으로 이어지는 화면 구성', 'How the entry point mounts the application'),
         left=[screen('home', pair('App의 렌더링 결과 · Header·HomePage·footer', 'App output · Header, HomePage and footer')),
               table([pair('파일·폴더', 'File / folder'), pair('역할', 'Role')], [
                    [pair('package.json · vite.config.ts', 'package.json · vite.config.ts'), pair('실행 명령·의존성·Vite 설정', 'Scripts, dependencies and Vite')],
                    [pair('src/App.tsx', 'src/App.tsx'), pair('공통 레이아웃·페이지 연결·Query 설정', 'Layout, routes and Query setup')],
                    [pair('src/pages · components', 'src/pages · components'), pair('경로별 화면 · 재사용 UI', 'Page screens · reusable UI')],
                    [pair('src/services · types', 'src/services · types'), pair('데이터 접근·검증 · 데이터 타입', 'Data access and validation · data types')],
                    [pair('src/styles · CSS', 'src/styles · CSS'), pair('전역 스타일·화면 배치', 'Global styles and layout')],
                ])],
         right=[concept(pair('진입점 - React 화면을 브라우저에 연결하는 시작 위치', 'Entry point - where React attaches the UI to the browser'),
                        pair('index.html의 root 요소를 main.tsx에서 찾아 App 배치', 'main.tsx finds the root element in index.html and mounts App')),
                code('entry', pair('src/main.tsx · root 검색과 App 연결 발췌', 'src/main.tsx · finding root and mounting App'))],
         sources=['index.html', 'src/main.tsx', 'src/App.tsx', 'package.json', 'vite.config.ts']),
    dict(id='routing', title=pair('공통 레이아웃과 페이지 라우팅', 'Shared layout and page routing'),
         lead=pair('같은 앱 안에서 경로에 따라 바뀌는 본문', 'The URL selects the content inside the shared application'),
         left=[screen('app-list', pair('#/list · Header·목록 본문·footer', '#/list · Header, list content and footer')),
               concept(pair('라우팅 - URL에 대응하는 페이지 선택', 'Routing - selecting a page for a URL'),
                       pair('Header·footer는 공통 영역, Routes는 페이지 영역', 'Header and footer form the shared layout around Routes'),
                       pair('HashRouter는 # 뒤 경로 사용 · :id는 상세 항목 식별', 'HashRouter uses the path after # · :id identifies the detail item'))],
         right=[code('routes', pair('src/App.tsx · 홈·목록·상세 경로 발췌', 'src/App.tsx · home, list and detail routes')),
                code('detail-link', pair('RestaurantCard.tsx · 상세 화면 링크', 'RestaurantCard.tsx · detail link'))],
         sources=['src/App.tsx', 'src/components/Header.tsx', 'src/components/RestaurantCard.tsx', 'src/pages/DetailPage.tsx']),
    dict(id='components', title=pair('목록과 카드의 컴포넌트 분리', 'Separating the list and card components'),
         lead=pair('목록은 반복 배치, 카드는 한 항목의 표시 담당', 'The list repeats items, while each card renders one restaurant'),
         left=[screen('list', pair('전체 목록 · 같은 카드 구조에 서로 다른 맛집 데이터', 'All restaurants · one card structure with different data')),
               concept(pair('컴포넌트 분리 - 역할에 따라 UI를 나누는 구조', 'Component separation - dividing the UI by responsibility'),
                       pair('부모는 목록을 순회하며 각 항목을 Props로 전달', 'The parent maps over the list and passes each item through props'),
                       pair('자식은 받은 데이터로 카드의 이름·분류·정보 표시', 'Each child renders the name, category and information from its data'))],
         right=[code('list', pair('RestaurantList.tsx · 목록 반복 발췌', 'RestaurantList.tsx · repeated cards')),
                code('card', pair('RestaurantCard.tsx · 카드 제목 영역 발췌', 'RestaurantCard.tsx · card header'))],
         sources=['src/components/RestaurantList.tsx', 'src/components/RestaurantCard.tsx', 'https://react.dev/learn/passing-props-to-a-component']),
    dict(id='query-state', title=pair('조회 데이터와 화면 상태', 'Query data and UI state'),
         lead=pair('원본 목록을 가져온 뒤 선택한 카테고리로 필터링', 'Fetch the source list, then filter it by the selected category'),
         left=[screen('filtered-list', pair('한식 선택 · 전체 데이터에서 조건에 맞는 카드만 표시', 'Korean category selected · only matching cards are shown')),
               concept(pair('상태 분리 - 조회 결과와 화면 선택값을 따로 관리', 'State separation - keeping query results apart from UI choices'),
                       pair('useQuery는 조회 결과·로딩·오류 관리', 'useQuery manages query results, loading and errors'),
                       pair('useState는 선택값 관리 · 필터 결과는 렌더링 중 계산', 'useState holds the selection · filtering is calculated during rendering'))],
         right=[code('query', pair('src/pages/ListPage.tsx · 조회·필터 발췌', 'src/pages/ListPage.tsx · query and filter excerpts'))],
         sources=['src/pages/ListPage.tsx', 'src/App.tsx', 'https://tanstack.com/query/v5/docs/framework/react/guides/queries']),
    dict(id='form', title=pair('제보 폼의 저장 흐름', 'Saving a restaurant submission'),
         lead=pair('메뉴 입력의 변환과 저장 성공에 따른 화면 전환', 'Transform menu input, then switch screens after saving'),
         left=[screen('submit-menu', pair('추천 메뉴 입력 · 김치찌개, 제육볶음', 'Menu input · 김치찌개, 제육볶음')),
               screen('submit-success', pair('저장 성공 후 화면', 'Screen after a successful save'))],
         right=[concept(pair('폼 처리 - 입력값을 저장 형태로 변환해 전달하는 과정', 'Form handling - converting input into a format for saving'),
                        pair('쉼표·줄바꿈으로 구분한 메뉴 문자열을 배열로 변환', 'Split menu text into an array at commas and line breaks'),
                        pair('저장 요청의 성공 후 완료 상태로 화면 전환', 'Switch to the completed state after the save succeeds')),
                code('menu-input', pair('SubmitRestaurant.tsx · 메뉴 입력 변환 발췌', 'SubmitRestaurant.tsx · menu input transformation')),
                code('submit', pair('SubmitRestaurant.tsx · 저장 성공 처리 발췌', 'SubmitRestaurant.tsx · handling a successful save'))],
         sources=['src/components/SubmitRestaurant.tsx', 'src/services/api.ts', 'src/types/index.ts', 'https://react-hook-form.com/docs/useform/handlesubmit']),
    dict(id='service', title=pair('서비스 함수의 데이터 접근', 'Data access through service functions'),
         lead=pair('현재 브라우저 저장소와 앞으로 연결할 서버 사이의 경계', 'The boundary between local browser storage and a future server'),
         left=[screen('restaurant-table', pair('AdminPage의 맛집 3개 · getRestaurants() 조회 결과', 'Three restaurants in AdminPage · getRestaurants() result')),
               table([pair('현재 구현', 'Current implementation'), pair('서버 연결 시 대체', 'With a server')], [
                   [pair('initialRestaurants · readItems', 'initialRestaurants · readItems'), pair('서버 API로 목록·상세 조회', 'List and detail queries via API')],
                   [pair('writeItems · localStorage', 'writeItems · localStorage'), pair('서버 API로 데이터 변경·저장', 'Updates and persistence via API')],
                   [pair('비동기 함수 · { data: ... }', 'Async functions · { data: ... }'), pair('페이지가 기대하는 응답 형태 유지', 'Keep the response shape for pages')],
               ])],
         right=[concept(pair('서비스 계층 - 데이터 접근 방법을 모으는 경계', 'Service layer - a boundary that groups data access'),
                        pair('페이지는 비동기 함수를 호출하고 { data: ... } 결과 사용', 'Pages call async functions and use a { data: ... } result'),
                        pair('현재는 HTTP 요청 없이 localStorage에서 읽기·저장', 'Currently reads and writes localStorage without HTTP')),
                code('get-restaurants', pair('src/services/api.ts · restaurantAPI 내부 발췌', 'src/services/api.ts · excerpt from restaurantAPI'))],
         sources=['src/services/api.ts', 'src/services/storage.ts', 'src/pages/AdminPage.tsx']),
    dict(id='server-data', title=pair('서버가 맡을 데이터 책임', 'Data responsibilities for the server'),
         lead=pair('브라우저별 저장과 서버로 공유할 데이터', 'Browser-local storage and the data to share through a server'),
         left=[screen('submissions', pair('브라우저 A · 제보 저장 후 1건', 'Browser A · one saved submission')),
               screen('submissions-empty', pair('브라우저 B · 같은 #/submissions에서 0건', 'Browser B · zero items at the same #/submissions')),
               concept(pair('공유 데이터 - 서버에서 함께 조회·변경하는 원본', 'Shared data - a source that users read and update through a server'),
                       pair('현재 제보는 브라우저별 저장 · 다른 브라우저에 미공유', 'Submissions currently stay in each browser and are not shared'),
                       pair('선택 카테고리·입력 중인 값은 클라이언트 상태', 'The selected category and in-progress form values remain UI state'))],
         right=[table([pair('대상', 'Data'), pair('현재 코드', 'Current code'), pair('서버의 책임', 'Server responsibility')], [
                    [pair('맛집', 'Restaurants'), pair('initialRestaurants · 브라우저 저장소', 'initialRestaurants · browser storage'), pair('DB의 목록·상세·생성·수정·삭제', 'Database list, detail, create, update and delete')],
                    [pair('제보·승인', 'Submissions / approval'), pair('브라우저 저장 · 관리자 화면에서 변경', 'Browser storage · changes from the admin screen'), pair('입력 재검증·관리자 권한·승인 일괄 처리', 'Input validation, admin authorization and atomic approval')],
                    [pair('좋아요', 'Likes'), pair('카드가 별도 localStorage 키에 직접 저장', 'Cards write directly to separate localStorage keys'), pair('사용자별 중복 제어·공유 개수 집계', 'Per-user deduplication and shared counts')],
                    [pair('인기 순위', 'Popularity ranking'), pair('rating 내림차순 · 주간 집계 없음', 'rating descending · no weekly aggregation'), pair('조회 기간·정렬·집계 기준 적용', 'Apply the ranking period, sorting and aggregation rules')],
                ])], sources=['src/services/api.ts', 'src/components/RestaurantCard.tsx', 'src/components/PopularRestaurants.tsx', 'src/pages/SubmissionsPage.tsx']),
]

assert len(SLIDES) == 8
