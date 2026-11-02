"""Follow one list request to completion, then explain creation, errors and storage."""


def pair(ko, en):
    return (ko, en)


def concept(term, *details):
    return dict(kind='concept', term=term, details=details)


def code(ident, label):
    return dict(kind='code', ident=ident, label=label)


def result(ident, label):
    return dict(kind='result', ident=ident, label=label)


def table(head, rows):
    return dict(kind='table', head=head, rows=rows)


def journey(kind, *current):
    return dict(kind=kind, current=list(current))


JOURNEY_STEPS = [
    pair('클라이언트', 'Client'), pair('미들웨어', 'Middleware'),
    pair('Router', 'Router'), pair('Controller', 'Controller'),
    pair('Service', 'Service'), pair('응답 수신', 'Receive response'),
]
JOURNEY_REQUESTS = {
    'get': pair('GET /api/restaurants', 'GET /api/restaurants'),
    'create': pair('생성 요청의 추가 처리 · POST /api/restaurants', 'Creation changes · POST /api/restaurants'),
    'error': pair('정상 요청의 실패 분기 · 400 / 404', 'Failure branches · 400 / 404'),
}

# Inclusive, ordered source ranges. README excerpts are integration examples.
EXCERPTS = {
    'server': ('server.ts', [('import createApp', 'export default app;')]),
    'client': ('README.md', [('const http =', 'const http ='),
        ('async function getData<T>', '}'),
        ('export const restaurantAPI = {', 'export const restaurantAPI = {'),
        ('  getRestaurants:', '  getRestaurants:'), ('};', '};')]),
    'app': ('src/app.ts', [('  app.use(cors());', '  app.use(express.urlencoded'),
        ("  app.use('/api/restaurants'", "  app.use('/api/restaurants'")]),
    'route-list': ('src/routes/restaurants.routes.ts', [("router.get('/',", "router.get('/',")]),
    'controller-list': ('src/controllers/restaurants.controller.ts', [('export const getRestaurants =', '});')]),
    'async-list': ('src/services/restaurants.service.ts', [('export async function getAllRestaurants()', '}')]),
    'async-error': ('src/utils/asyncHandler.ts', [('    Promise.resolve(handler', '    Promise.resolve(handler')]),
    'cache': ('src/services/restaurants.service.ts', [('let restaurantCache:', 'let restaurantCache:'),
        ('  restaurantCache = [...restaurantCache', '  restaurantCache = [...restaurantCache'),
        ('export function resetStore()', '}')]),
}

SLIDES = [
    dict(id='cover', kind='cover',
         title=pair('실전 웹서비스개발 – 7주차', 'Practical Web Service Development – Week 7'),
         lead=pair('6주차 실습 리뷰 · Ajou Campus Foodmap API', 'Week 6 Practice Review · Ajou Campus Foodmap API')),
    dict(id='project', title=pair('서버 실행 준비', 'Preparing the Server'),
         lead=pair('요청이 도착하기 전 앱 생성과 포트 대기', 'Create the app and start listening before a request arrives'),
         left=[concept(pair('서버 시작 - 앱을 구성하고 HTTP 요청 수신을 준비하는 과정', 'Server startup - configure the app and begin listening for HTTP requests'),
                       pair('앱 생성 함수는 미들웨어와 요청 경로를 서버에 등록', 'The app creation function registers middleware and routes'),
                       pair('환경변수 PORT는 코드 밖에서 전달하는 서버 포트 설정값', 'The PORT environment variable sets the listening port from outside the code'),
                       pair('개발은 tsx로 TypeScript 실행 · 배포는 JavaScript로 변환한 뒤 실행', 'tsx runs TypeScript during development; deployment runs JavaScript built from that source')),
               table([pair('파일', 'File'), pair('시작할 때의 역할', 'Startup responsibility')], [
                   [pair('server.ts', 'server.ts'), pair('앱 생성·포트 설정·수신 시작', 'Create the app, choose a port, and start listening')],
                   [pair('src/app.ts', 'src/app.ts'), pair('요청 처리에 사용할 함수와 경로 구성', 'Configure the functions and routes that will handle requests')],
               ])],
         right=[code('server', pair('pwd-week6/server.ts · 진입 파일', 'pwd-week6/server.ts · entry file')),
                result('health', pair('시작 확인 · GET /health', 'Startup check · GET /health'))],
         sources=['server.ts', 'src/app.ts', 'package.json']),
    dict(id='client', title=pair('클라이언트의 목록 조회 요청', 'Requesting the Restaurant List'),
         lead=pair('서버 기본 주소에 GET /api/restaurants 요청', 'Send GET /api/restaurants to the server base URL'),
         journey=journey('get', 0),
         left=[concept(pair('조회 요청 - 서버의 목록을 가져오기 위한 HTTP 호출', 'List request - an HTTP call that asks the server for its list'),
                       pair('Axios는 HTTP 요청을 보내는 라이브러리', 'Axios is the library used to send HTTP requests'),
                       pair('서버 기본 주소에 기능별 경로인 엔드포인트를 붙여 요청', 'The endpoint path identifies the operation at the server base URL'),
                       pair('페이지는 서비스 함수를 호출해 데이터 접근 방법과 분리', 'The page calls a service function that hides the data access method')),
               table([pair('요청 요소', 'Request part'), pair('목록 조회의 값', 'Value for this request')], [
                   [pair('기본 주소', 'Base URL'), pair('VITE_API_BASE_URL의 서버 주소', 'Server address from VITE_API_BASE_URL')],
                   [pair('HTTP 메서드', 'HTTP method'), pair('GET · 데이터 조회', 'GET · read data')],
                   [pair('경로', 'Path'), pair('/api/restaurants', '/api/restaurants')],
               ])],
         right=[code('client', pair('pwd-week6/README.md · Axios 조회 연동 예제 발췌', 'pwd-week6/README.md · Axios integration example excerpts'))],
         sources=['README.md', 'https://vite.dev/guide/env-and-mode']),
    dict(id='middleware', title=pair('Express의 요청 수신', 'Receiving the Request in Express'),
         lead=pair('공통 미들웨어를 거쳐 맛집 Router로 전달', 'Pass through common middleware to the restaurant router'),
         journey=journey('get', 1),
         left=[concept(pair('미들웨어 - 요청을 처리하거나 다음 처리기로 넘기는 함수', 'Middleware - functions that handle a request or pass it to the next handler'),
                       pair('등록 순서에 따라 공통 처리를 거친 뒤 Router로 전달', 'Common middleware runs in registration order before the router'),
                       pair('출처(origin)는 프로토콜·호스트·포트의 조합', 'An origin is the combination of protocol, host, and port'),
                       pair('CORS(Cross-Origin Resource Sharing)는 다른 출처의 응답 읽기 허용 정보 제공', 'CORS (Cross-Origin Resource Sharing) tells the browser which origins may read a response'),
                       pair('본문 해석기는 JSON·폼 입력을 req.body에 배치', 'Body parsers place JSON or form input in req.body'),
                       pair('목록 GET 요청은 본문 없이 /api/restaurants 경로로 전달', 'This GET request has no body and reaches the /api/restaurants router'))],
         right=[code('app', pair('src/app.ts · 공통 미들웨어와 맛집 Router 등록 발췌', 'src/app.ts · common middleware and restaurant router excerpts'))],
         sources=['src/app.ts', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS',
                  'https://developer.mozilla.org/en-US/docs/Glossary/Origin']),
    dict(id='mvcs', title=pair('Router와 Controller의 요청 연결', 'Routing the Request to the Controller'),
         lead=pair('GET 경로 선택에서 목록 Service 호출로 연결', 'Select the GET handler and call the list service'),
         journey=journey('get', 2, 3),
         left=[concept(pair('역할 분리 - 경로 선택과 HTTP 처리의 책임을 나누는 구조', 'Separation of roles - keep route selection apart from HTTP handling'),
                       pair('Router는 메서드·경로에 맞는 Controller 선택', 'The router selects a controller by method and path'),
                       pair('Controller는 요청을 Service에 전달하고 반환값으로 응답 구성', 'The controller calls the service and builds a response from its result'),
                       pair('MVCS(Model·View·Controller·Service)에서 View는 React 화면', 'In MVCS (Model–View–Controller–Service), React provides the View')),
               table([pair('단계', 'Step'), pair('목록 조회에서의 연결', 'Connection for the list request')], [
                   [pair('Router', 'Router'), pair('GET /api/restaurants → getRestaurants', 'GET /api/restaurants → getRestaurants')],
                   [pair('Controller', 'Controller'), pair('getAllRestaurants() 호출', 'Call getAllRestaurants()')],
                   [pair('응답 약속', 'Response contract'), pair('Service 결과를 { data: ... }로 전달', 'Wrap the service result in { data: ... }')],
               ])],
         right=[code('route-list', pair('restaurants.routes.ts · 목록 경로 발췌', 'restaurants.routes.ts · list route excerpt')),
                code('controller-list', pair('restaurants.controller.ts · 목록 Controller', 'restaurants.controller.ts · list controller'))],
         sources=['src/routes/restaurants.routes.ts', 'src/controllers/restaurants.controller.ts']),
    dict(id='async-query', title=pair('Service의 목록 조회와 응답 완료', 'Completing the List Request'),
         lead=pair('메모리 목록을 반환하고 같은 요청의 응답을 클라이언트에서 수신', 'Return the list from memory and receive the response in the client'),
         journey=journey('get', 4, 5),
         left=[concept(pair('Service - 조회 규칙을 처리하고 데이터 결과를 반환하는 계층', 'Service - the layer that retrieves and returns data'),
                       pair('Promise는 비동기 작업의 성공 결과나 실패를 나타내는 객체', "A Promise is an object representing an asynchronous task's result or failure"),
                       pair('await는 현재 비동기 함수에서 Promise의 결과를 기다리는 표현', 'await waits for the result within the current async function'),
                       pair('Model은 맛집 한 개의 데이터 객체 · 캐시는 이 객체들을 메모리에 보관', 'A Model represents one restaurant; the cache keeps these objects in memory for reuse'),
                       pair('20ms 타이머 대기는 시뮬레이션 · 대기 중 다른 요청 처리 가능', 'A 20 ms timer simulates waiting while other requests can run')),
               table([pair('응답 전달 단계', 'Response handoff'), pair('전달되는 값', 'Value received')], [
                   [pair('Service → Controller', 'Service → Controller'), pair('맛집 3개의 배열', 'An array of three restaurants')],
                   [pair('Controller → HTTP', 'Controller → HTTP'), pair('{ data: [맛집 3개] }', '{ data: [three restaurants] }')],
                   [pair('Axios의 response.data', 'Axios response.data'), pair('HTTP 응답 본문 객체', 'The HTTP response body object')],
                   [pair('본문의 data', 'The body data field'), pair('페이지에서 사용할 맛집 배열', 'The restaurant array for the page')],
               ])],
         right=[code('async-list', pair('restaurants.service.ts · 목록 조회 발췌', 'restaurants.service.ts · list retrieval excerpt')),
                result('list-result', pair('같은 GET /api/restaurants 응답 · id·name 발췌', 'Same GET /api/restaurants response · selected id and name fields'))],
         sources=['src/services/restaurants.service.ts', 'src/models/restaurant.model.ts', 'src/controllers/restaurants.controller.ts', 'README.md',
                  'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise']),
    dict(id='create', title=pair('생성 요청에서 달라지는 처리', 'Changes for a Create Request'),
         lead=pair('같은 요청 구조에 입력 변환·필수 값 확인·데이터 추가 적용', 'Use the same request structure with input conversion, checks, and insertion'),
         journey=journey('create', 3, 4, 5),
         left=[concept(pair('생성 처리 - 입력으로 새 리소스를 만들고 결과를 반환하는 과정', 'Creation - build a new resource from input and return the result'),
                       pair('메뉴 문자열·배열을 같은 문자열 배열 형태로 통일', 'Convert menu text or array input into an array of strings'),
                       pair('이름·분류·위치의 누락 확인 후 새 ID 부여', 'Check for missing name, category, or location before assigning an ID'),
                       pair('새 맛집을 메모리에 추가한 뒤 201 응답', 'Add the new restaurant to memory and respond with HTTP 201')),
               table([pair('구분', 'Difference'), pair('목록 조회 GET', 'List GET'), pair('생성 POST', 'Create POST')], [
                   [pair('입력', 'Input'), pair('요청 본문 없음', 'No request body'), pair('맛집 정보·추천 메뉴', 'Restaurant fields and menu')],
                   [pair('처리', 'Work'), pair('기존 목록 복사', 'Copy the existing list'), pair('형식 변환·확인·추가', 'Convert, check, and add')],
                   [pair('성공', 'Success'), pair('200 · 맛집 배열', '200 · restaurant array'), pair('201 · 신규 맛집', '201 · new restaurant')],
               ])],
         right=[result('create-input', pair('POST /api/restaurants · JSON 요청 본문', 'POST /api/restaurants · JSON request body')),
                result('created', pair('생성 결과 · id·recommendedMenu만 발췌', 'Creation response · selected id and recommendedMenu fields'))],
         sources=['src/controllers/restaurants.controller.ts', 'src/services/restaurants.service.ts', 'src/models/restaurant.model.ts']),
    dict(id='errors', title=pair('실패했을 때의 처리', 'Handling a Failed Request'),
         lead=pair('정상 응답 대신 실패 원인을 상태 코드와 JSON으로 전달', 'Return the failure as a status code and JSON error response'),
         journey=journey('error', 3, 4, 5),
         left=[concept(pair('실패 분기 - 처리 결과에 따라 오류 응답으로 이어지는 경로', 'Failure branch - a path that ends in an error response'),
                       pair('HttpError는 HTTP 상태 코드·오류 메시지를 담는 객체', 'HttpError carries the HTTP status code and error message'),
                       pair('next(error)는 오류 처리 미들웨어로 오류를 전달하는 호출', 'next(error) passes the error to Express error-handling middleware'),
                       pair('stack trace는 오류가 발생한 함수 호출 경로 · 운영 응답에서 생략', 'A stack trace lists function calls leading to an error; production responses omit it')),
               table([pair('실패 사례', 'Failure case'), pair('정상 흐름에서 달라지는 경로', 'Path taken on failure')], [
                   [pair('400 · category 누락', '400 · missing category'), pair('Service의 HttpError → 오류 처리기', 'Service HttpError → error handler')],
                   [pair('404 · 없는 맛집 id', '404 · missing restaurant ID'), pair('Controller에서 직접 응답', 'Direct response from the controller')],
               ])],
         right=[code('async-error', pair('asyncHandler.ts · 비동기 오류 전달 문장 발췌', 'asyncHandler.ts · asynchronous error forwarding excerpt')),
                result('invalid', pair('POST /api/restaurants · name만 입력', 'POST /api/restaurants · name only')),
                result('missing', pair('GET /api/restaurants/999 · 없는 맛집', 'GET /api/restaurants/999 · missing restaurant'))],
         sources=['src/utils/asyncHandler.ts', 'src/utils/httpError.ts', 'src/middleware/error.middleware.ts', 'src/controllers/restaurants.controller.ts',
                  'https://expressjs.com/en/guide/error-handling/']),
    dict(id='persistence', title=pair('메모리 저장의 한계', 'The Limits of Memory Storage'),
         lead=pair('완료된 요청의 변경 데이터도 서버 재시작 후 소멸', 'Even a successful change is lost when the server restarts'),
         left=[concept(pair('메모리 저장 - 실행 중인 서버 프로그램 안에 데이터 보관', 'Memory storage - keeping data inside the running server program'),
                       pair('프로세스(process)는 실행 중인 프로그램 · 메모리는 이 실행 동안 유지', 'A process is a running program; its memory lasts for that execution'),
                       pair('시드(seed)는 서버 시작 시 불러오는 초기 JSON 데이터', 'Seed data is the initial JSON loaded when the server starts'),
                       pair('여러 클라이언트는 같은 서버의 데이터를 공유해도 재시작 후 신규 맛집 소멸', 'Clients share the same server data, but new restaurants are lost after a restart'),
                       pair('DB의 영구 저장은 서버 재시작 후에도 변경 데이터를 보존하는 방식', 'A database provides persistent storage, so saved changes survive a server restart')),
               table([pair('데이터', 'Data'), pair('6주차 저장 위치', 'Week 6 storage')], [
                   [pair('초기 맛집(시드)', 'Initial restaurants (seed)'), pair('restaurants.json → 메모리', 'restaurants.json → memory')],
                   [pair('새로 등록한 맛집', 'New restaurants'), pair('서버 메모리 · 재시작 후 소멸', 'Server memory · lost after restart')],
                   [pair('제보·좋아요', 'Submissions and likes'), pair('브라우저 내 저장소(localStorage)', 'localStorage in each browser')],
               ])],
         right=[code('cache', pair('restaurants.service.ts · 저장·초기화 발췌', 'restaurants.service.ts · storage and reset excerpts')),
                result('restart', pair('생성 성공 → 다른 요청의 조회 → 서버 재시작', 'Successful creation → later request → server restart'))],
         sources=['src/services/restaurants.service.ts', 'src/data/restaurants.json', 'README.md']),
]

assert [slide['id'] for slide in SLIDES] == [
    'cover', 'project', 'client', 'middleware', 'mvcs', 'async-query', 'create', 'errors', 'persistence',
]
