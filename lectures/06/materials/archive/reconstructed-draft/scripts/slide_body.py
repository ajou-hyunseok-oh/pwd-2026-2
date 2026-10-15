"""Week 06 concept explanations and examples using the Week 05 block schema."""
from pathlib import Path
import re
import textwrap
from diagrams import (CLIENT_SERVER, SERVER_ROLE, ASYNC_IO, MVC, MVCS, TDD,
                      MIDDLEWARE as MIDDLEWARE_FLOW, CORS as CORS_FLOW)

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'


def P(ko, en):
    return (ko, en)


def D(ko, en, *details):
    return dict(kind='concepts', items=[(P(ko, en), list(details))])


def K(ko, en, code, *, lang='javascript', width=58, result=None):
    block = dict(kind='code', label=P(ko, en), code=textwrap.dedent(code).strip(), lang=lang, width=width)
    if result:
        block['result'] = result
    return block


def T(head, *rows):
    return dict(kind='table', head=head, rows=list(rows))


def source_code(filename, function=None, start=None, end=None):
    """Extract a full file, named function, or explicitly bounded test from real code."""
    text = (EXAMPLES / filename).read_text().strip()
    if function:
        lines = text.splitlines()
        pattern = re.compile(r'^(\s*)(?:async )?function ' + re.escape(function) + r'\(')
        for i, line in enumerate(lines):
            match = pattern.match(line)
            if match:
                for j in range(i + 1, len(lines)):
                    if lines[j] == match[1] + '}':
                        return textwrap.dedent('\n'.join(lines[i:j + 1]))
        raise ValueError(f'{filename}: missing function {function}')
    if start:
        text = text[text.index(start):]
        assert end, 'A partial source needs an explicit end marker'
        marker = '\n' + end
        text = text[:text.index(marker) + len(marker)]
    return text


BODIES = {}
NODE = 'https://nodejs.org/en/learn/getting-started/introduction-to-nodejs'
HTTP = 'https://www.rfc-editor.org/rfc/rfc9110.html'
EXPRESS = 'https://expressjs.com/en/guide/routing.html'
MIDDLEWARE = 'https://expressjs.com/en/guide/using-middleware.html'
ERRORS = 'https://expressjs.com/en/guide/error-handling.html'
API = 'https://expressjs.com/en/5x/api.html'
TEST = 'https://nodejs.org/api/test.html'
RENDER = 'https://render.com/docs/deploy-node-express-app'


def body(ident, *blocks, layout='split', refs=()):
    key = 'concept-' + ident
    assert key not in BODIES
    BODIES[key] = dict(blocks=list(blocks), layout=layout,
                       sources=[('Official documentation', url) for url in refs])


# 01. Servers and Node.js
body('client-server',
    D('클라이언트-서버 구조 - 요청하는 쪽과 처리하는 쪽을 분리한 구조',
      'Client–server architecture - Separate the requester from the processor',
      P('클라이언트는 사용자 입력을 요청으로 전달하는 프로그램', 'The client sends user input as a request'),
      P('서버는 요청을 받아 처리 결과를 응답으로 반환하는 프로그램', 'The server receives a request and returns its processing result'),
      P('네트워크는 두 프로그램 사이의 메시지 전달 경로', 'The network carries messages between the two programs'),
      P('브라우저·모바일 앱·다른 서버 모두 클라이언트 역할 수행 가능', 'Browsers, mobile apps, and other servers can act as clients')),
    CLIENT_SERVER, refs=[HTTP])

body('server-role',
    D('서버의 책임 - 요청을 검증하고 허용된 처리 결과를 반환하는 역할',
      'Server responsibility - Validate requests and return permitted results',
      P('입력 검증은 요청 데이터의 타입·필수값·허용 범위 확인', 'Input validation checks types, required values, and permitted ranges'),
      P('업무 처리는 서비스의 규칙에 따른 계산과 데이터 변경', 'Business processing computes results and changes data under application rules'),
      P('데이터 접근은 저장소·외부 API에서 필요한 정보 조회', 'Data access retrieves information from storage and external APIs'),
      P('인증은 요청자의 신원 확인 · 인가는 해당 작업의 권한 확인', 'Authentication checks identity; authorization checks permission for an operation'),
      P('응답 생성은 처리 결과와 오류를 클라이언트가 읽을 형식으로 변환', 'Response creation converts results and errors into a format the client can read')),
    SERVER_ROLE, layout='stack', refs=[HTTP])

body('server-stack',
    D('서버 개발 스택 - 런타임·언어·프레임워크의 조합',
      'Server development stack - A combination of runtime, language, and framework',
      P('런타임은 프로그램의 실행 환경 · 프레임워크는 요청 처리의 공통 구조', 'The runtime executes the program; the framework supplies shared request-processing structure'),
      P('선택 기준은 팀의 경험·기존 시스템·서비스의 처리 특성', 'Selection depends on team experience, existing systems, and workload characteristics')),
    T([P('언어·실행 환경', 'Language / runtime'), P('웹 프레임워크 사례', 'Web framework examples')],
      [P('JavaScript · Node.js', 'JavaScript · Node.js'), P('Express · Fastify · NestJS', 'Express · Fastify · NestJS')],
      [P('Python', 'Python'), P('Django · Flask · FastAPI', 'Django · Flask · FastAPI')],
      [P('Java · JVM', 'Java · JVM'), P('Spring', 'Spring')],
      [P('PHP', 'PHP'), P('Laravel', 'Laravel')]), layout='stack', refs=[NODE])

body('nodejs',
    D('Node.js - 브라우저 밖에서 JavaScript를 실행하는 런타임',
      'Node.js - A runtime for executing JavaScript outside the browser',
      P('V8 엔진을 통해 JavaScript 코드 실행', 'Runs JavaScript code using the V8 engine'),
      P('파일·네트워크·프로세스를 다루는 실행 환경 제공', 'Provides an environment for files, networking, and processes'),
      P('브라우저의 document·window 대신 서버용 API 사용', 'Uses server APIs in place of browser document and window APIs'),
      P('같은 JavaScript 언어라도 실행 환경에 따라 사용 가능한 API 구분', 'The same JavaScript language has different available APIs in different environments')),
    K('독립 실행 · hello.cjs · node hello.cjs', 'Standalone · hello.cjs · node hello.cjs', "console.log('Hello, Node.js');", result=[P('Hello, Node.js', 'Hello, Node.js')]), refs=[NODE])

body('v8',
    D('V8 - JavaScript와 WebAssembly를 실행하는 엔진',
      'V8 - An engine that executes JavaScript and WebAssembly',
      P('소스 코드를 파싱해 실행 가능한 내부 표현 생성', 'Parses source code into an internal executable representation'),
      P('인터프리터와 단계별 컴파일을 통해 코드 실행', 'Executes code through interpretation and tiered compilation'),
      P('실행 중 수집한 정보를 활용해 자주 실행되는 코드 최적화', 'Uses runtime feedback to optimize frequently executed code'),
      P('Node.js는 V8에 파일·네트워크 등 서버용 기능을 결합한 실행 환경', 'Node.js combines V8 with server facilities such as files and networking')),
    T([P('구성', 'Part'), P('담당 역할', 'Role')],
      [P('V8', 'V8'), P('JavaScript 실행 · 메모리 관리', 'JavaScript execution and memory management')],
      [P('Node.js', 'Node.js'), P('엔진과 운영체제 기능의 연결', 'Connect the engine to operating-system facilities')],
      [P('브라우저', 'Browser'), P('엔진과 DOM·화면 렌더링 기능의 연결', 'Connect an engine to the DOM and rendering')]), refs=['https://v8.dev/docs', NODE])

body('async-io',
    D('비동기 I/O - 입출력 완료를 기다리는 동안 다른 실행을 허용하는 방식',
      'Asynchronous I/O - Allow other execution while waiting for input or output',
      P('I/O는 파일 읽기·네트워크 응답처럼 외부 완료를 기다리는 작업', 'I/O includes operations such as reading files and waiting for network responses'),
      P('비동기 API는 작업을 요청한 뒤 JavaScript 실행 제어권 반환', 'An asynchronous API returns control after an operation is requested'),
      P('완료 결과는 콜백이나 Promise를 통해 후속 처리에 전달', 'Completion results reach subsequent processing through callbacks or promises'),
      P('CPU 계산을 오래 수행하는 JavaScript는 비동기 함수 안에서도 실행 흐름 점유', 'Long CPU computations occupy JavaScript execution even inside an async function')),
    ASYNC_IO,
    refs=['https://nodejs.org/en/learn/asynchronous-work/overview-of-blocking-vs-non-blocking'])

body('event-loop',
    D('이벤트 루프 - 준비된 비동기 콜백의 실행을 조정하는 구조',
      'Event loop - A mechanism that coordinates ready asynchronous callbacks',
      P('일반적인 JavaScript 콜백은 메인 실행 스레드에서 한 번에 하나씩 실행', 'Ordinary JavaScript callbacks execute one at a time on the main thread'),
      P('운영체제와 작업자 풀은 일부 I/O 작업을 별도로 처리', 'The operating system and worker pool handle some I/O work separately'),
      P('현재 JavaScript 실행이 끝난 뒤 준비된 콜백 실행 가능', 'Ready callbacks can run after the current JavaScript execution completes'),
      P('긴 반복문·동기 I/O는 다른 요청의 콜백 실행 지연', 'Long loops and synchronous I/O delay callbacks for other requests')),
    K('독립 실행 · loop.cjs · node loop.cjs', 'Standalone · loop.cjs · node loop.cjs', '''
console.log('A');
setTimeout(() => console.log('B'), 0);
console.log('C');
''', result=[P('A → C → B', 'A → C → B'), P('0ms는 즉시 실행 보장이 아닌 타이머 지연값', '0ms is a timer delay, without a guarantee of immediate execution')]),
    refs=['https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick', 'https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop'])

# 02. HTTP and REST APIs
body('http',
    D('HTTP - 요청과 응답 메시지의 의미를 정하는 통신 규약',
      'HTTP - A protocol defining the semantics of request and response messages',
      P('클라이언트의 요청과 서버의 응답이 한 번의 교환 구성', 'A client request and a server response form an exchange'),
      P('메서드는 요청 의미 · 상태 코드는 처리 결과 표현', 'Methods express request semantics; status codes express outcomes'),
      P('무상태는 각 요청의 의미를 독립적으로 해석하는 프로토콜 특성', 'Statelessness lets each request be interpreted independently'),
      P('로그인·장바구니 등의 애플리케이션 상태는 쿠키·토큰·저장소 등으로 별도 관리', 'Applications manage login and cart state separately using cookies, tokens, or storage')),
    layout='single', refs=[HTTP])

body('https',
    D('HTTPS - TLS로 보호하는 HTTP 통신', 'HTTPS - HTTP communication protected by TLS',
      P('TLS는 전송 중인 메시지의 암호화와 무결성 확인 담당', 'TLS encrypts messages in transit and checks their integrity'),
      P('서버 인증서는 접속 대상의 신원을 확인하는 근거', 'The server certificate provides evidence of the destination identity'),
      P('사용자 로그인 여부와 접근 권한은 애플리케이션의 별도 책임', 'User login and access permissions remain application responsibilities')),
    T([P('구성 요소', 'Part'), P('담당 역할', 'Role')],
      [P('HTTP', 'HTTP'), P('요청과 응답의 의미', 'Request and response semantics')],
      [P('TLS', 'TLS'), P('전송 구간의 암호화·무결성·서버 신원 확인', 'Transport encryption, integrity, and server identity')],
      [P('애플리케이션', 'Application'), P('입력 검증·신원 및 권한 확인', 'Validation, authentication, and authorization')]), refs=[HTTP])

body('http-request',
    D('HTTP 요청 - 대상 리소스에 수행할 작업을 전달하는 메시지',
      'HTTP request - A message expressing an operation on a target resource',
      P('메서드는 조회·생성 등 요청이 가진 의미', 'The method expresses semantics such as retrieval or creation'),
      P('요청 대상은 경로와 필요한 쿼리로 대상 지정', 'The request target identifies a path and any query'),
      P('헤더는 메시지 형식과 인증 정보 등의 메타데이터', 'Headers carry metadata such as the message format and authentication information'),
      P('본문은 생성·수정 등에 필요한 데이터 · 모든 요청에 필수인 요소는 아님', 'The body carries data for operations such as creation and modification; it is optional')),
    K('HTTP/1.1 요청 메시지 예 · 본문 22바이트', 'Example HTTP/1.1 request · 22-byte body', '''
POST /foods HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Content-Length: 22

{"name":"Campus Rice"}
''', lang='text'), refs=[HTTP])

body('http-response',
    D('HTTP 응답 - 요청의 처리 결과를 전달하는 메시지',
      'HTTP response - A message carrying the outcome of a request',
      P('상태 코드는 성공·실패 등 처리 결과의 분류', 'The status code classifies the outcome, including success or failure'),
      P('헤더는 본문 형식과 새 리소스 위치 등의 정보', 'Headers describe the body format and information such as a new resource location'),
      P('본문은 반환할 데이터의 표현 · 204 응답에는 본문 없음', 'The body represents returned data; a 204 response has no body')),
    K('HTTP/1.1 생성 응답 예 · 일부 헤더 발췌', 'Example HTTP/1.1 creation response · selected headers', '''
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Location: /foods/2

{"id":2,"name":"Campus Rice"}
''', lang='text'), refs=[HTTP])

body('status-code',
    D('상태 코드 - 요청 처리 결과를 분류하는 세 자리 숫자',
      'Status code - A three-digit classification of a request outcome',
      P('첫 자리로 결과의 범주 구분 · 나머지 숫자로 구체적인 의미 표현', 'The first digit identifies the class; the remaining digits identify a specific meaning'),
      P('클라이언트는 상태 코드로 성공 처리와 실패 처리 분기', 'Clients use status codes to choose success or failure handling')),
    T([P('분류', 'Class'), P('대표 코드', 'Codes'), P('의미', 'Meaning')],
      [P('2xx', '2xx'), P('200 · 201 · 204', '200 · 201 · 204'), P('성공 · 생성 완료 · 본문 없는 성공', 'Success, created, success without content')],
      [P('4xx', '4xx'), P('400 · 404', '400 · 404'), P('잘못된 요청 · 대상 없음', 'Invalid request, target not found')],
      [P('5xx', '5xx'), P('500 · 503', '500 · 503'), P('서버 내부 오류 · 서비스 이용 불가', 'Internal server error, service unavailable')]), layout='stack', refs=[HTTP])

body('json',
    D('JSON - 데이터를 교환하기 위한 텍스트 형식', 'JSON - A text format for exchanging data',
      P('값은 문자열·숫자·불리언·null·객체·배열의 여섯 종류', 'Values are strings, numbers, booleans, null, objects, or arrays'),
      P('객체는 이름과 값의 쌍 · 배열은 순서가 있는 값의 목록', 'An object contains name–value pairs; an array contains an ordered list of values'),
      P('객체의 이름과 문자열 값은 큰따옴표 사용', 'Object names and string values use double quotes'),
      P('주석·후행 쉼표·함수·undefined는 JSON 문법에서 제외', 'JSON syntax excludes comments, trailing commas, functions, and undefined')),
    K('데이터 예 · food.json', 'Data example · food.json', '''
{
  "id": 1,
  "name": "Campus Noodles",
  "open": true,
  "tags": ["lunch", "noodles"],
  "note": null
}
''', lang='json'), refs=['https://www.rfc-editor.org/rfc/rfc8259.html'])

body('json-transform',
    D('직렬화와 파싱 - 프로그램의 값과 JSON 문자열 사이의 변환',
      'Serialization and parsing - Convert between program values and JSON strings',
      P('JSON.stringify는 JavaScript 값을 전송·저장용 문자열로 변환', 'JSON.stringify converts a JavaScript value into a string for transport or storage'),
      P('JSON.parse는 JSON 문자열을 JavaScript 값으로 해석', 'JSON.parse interprets a JSON string as a JavaScript value'),
      P('문법에 맞지 않는 문자열의 파싱은 SyntaxError 발생', 'Parsing text with invalid JSON syntax throws a SyntaxError'),
      P('문법에 맞는 JSON도 서비스에 필요한 필드·타입 검증은 별도', 'Valid JSON still needs application checks for required fields and types')),
    K('독립 실행 · json.cjs', 'Standalone · json.cjs', '''
const food = { id: 1, name: 'Campus Noodles' };
const text = JSON.stringify(food);
const value = JSON.parse(text);
console.log(typeof text);
console.log(value.name);
''', result=[P('string → Campus Noodles', 'string → Campus Noodles')]), refs=['https://tc39.es/ecma262/multipage/structured-data.html#sec-json-object'])

body('rest-resource',
    D('REST - 자원과 그 표현의 교환을 중심으로 한 아키텍처 스타일',
      'REST - An architectural style centered on resources and representations',
      P('리소스는 서비스가 식별하고 다루는 대상', 'A resource is an identifiable subject handled by a service'),
      P('URI는 리소스 식별 · HTTP 메서드는 요청 의미 표현', 'A URI identifies the resource; the HTTP method expresses the operation semantics'),
      P('표현은 특정 시점의 리소스 상태를 담은 JSON·HTML 등의 데이터', 'A representation carries resource state at a particular time, using JSON, HTML, or another format'),
      P('REST의 제약에는 무상태·캐시·일관된 인터페이스 등 포함', 'REST constraints include statelessness, caching, and a uniform interface'),
      P('명사형 경로와 JSON 사용만으로 REST의 모든 제약을 충족하는 것은 아님', 'Noun-based paths and JSON alone do not satisfy all REST constraints')),
    T([P('대상', 'Subject'), P('식별 URI', 'Identifying URI'), P('표현 예', 'Representation example')],
      [P('맛집 목록', 'Food collection'), P('/foods', '/foods'), P('[{"id":1,"name":"Campus Noodles"}]', '[{"id":1,"name":"Campus Noodles"}]')],
      [P('개별 맛집', 'One food'), P('/foods/1', '/foods/1'), P('{"id":1,"name":"Campus Noodles"}', '{"id":1,"name":"Campus Noodles"}')]), layout='stack',
    refs=['https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm', HTTP])

body('http-method',
    D('HTTP 메서드 - 리소스에 적용할 요청의 의미',
      'HTTP method - The semantics of a request applied to a resource',
      P('같은 URI라도 메서드에 따라 서버가 수행할 의미 구분', 'Different methods distinguish operations on the same URI'),
      P('API는 표준 메서드 의미를 지키는 일관된 계약으로 설계', 'An API provides a consistent contract that follows standard method semantics')),
    T([P('메서드', 'Method'), P('의미', 'Meaning'), P('Foodmap 요청 예', 'Foodmap request')],
      [P('GET', 'GET'), P('리소스의 표현 조회', 'Retrieve a representation'), P('GET /foods/1', 'GET /foods/1')],
      [P('POST', 'POST'), P('대상에 데이터 처리 요청 · 컬렉션에서 생성에 사용', 'Request data processing; used for collection creation'), P('POST /foods', 'POST /foods')],
      [P('PUT', 'PUT'), P('대상 리소스의 상태를 제공한 표현으로 교체', 'Replace target state with the supplied representation'), P('PUT /foods/1', 'PUT /foods/1')],
      [P('DELETE', 'DELETE'), P('대상 리소스와 URI의 연결 제거 요청', 'Request removal of the target resource association'), P('DELETE /foods/1', 'DELETE /foods/1')]), layout='stack', refs=[HTTP])

body('idempotency',
    D('멱등성 - 동일 요청의 반복이 한 번과 같은 의도된 효과를 갖는 성질',
      'Idempotency - Repeated identical requests have the same intended effect as one',
      P('비교 대상은 서버 상태에 대한 의도된 효과 · 응답 본문의 동일성은 아님', 'The comparison concerns the intended effect on server state, rather than identical response bodies'),
      P('GET·PUT·DELETE는 표준 의미상 멱등 · POST는 일반적으로 보장 없음', 'GET, PUT, and DELETE are idempotent by standard semantics; POST has no general guarantee'),
      P('재전송이 가능한지의 판단과 응답의 캐시 가능 여부는 별도 속성', 'Retry semantics and response cacheability are separate properties')),
    T([P('반복 요청', 'Repeated request'), P('관찰할 효과', 'Effect to observe')],
      [P('PUT /foods/1 · 같은 표현', 'PUT /foods/1 · identical representation'), P('같은 최종 리소스 상태', 'The same final resource state')],
      [P('DELETE /foods/1', 'DELETE /foods/1'), P('첫 삭제 후 부재 유지 · 후속 응답은 달라질 수 있음', 'Remains absent after deletion; later responses may differ')],
      [P('POST /foods', 'POST /foods'), P('동일 본문을 보내도 여러 리소스 생성 가능', 'Identical bodies can create multiple resources')]), refs=[HTTP])

# 03. Express
body('express',
    D('Express - Node.js에서 웹 요청 처리를 구성하는 프레임워크',
      'Express - A framework for organizing web request processing in Node.js',
      P('앱은 라우트와 공통 처리 함수를 등록하는 중심 객체', 'The app is the central object for registering routes and shared processing functions'),
      P('요청 객체는 입력 정보 · 응답 객체는 결과 전송 기능 제공', 'The request object supplies input; the response object supplies result-sending methods'),
      P('Node.js의 HTTP 기능을 바탕으로 웹 앱과 API 구현', 'Builds web applications and APIs on Node.js HTTP facilities')),
    T([P('작업', 'Task'), P('Node.js 기본 HTTP', 'Node.js HTTP'), P('Express', 'Express')],
      [P('요청 분기', 'Dispatch'), P('메서드·경로를 직접 판별', 'Check methods and paths directly'), P('등록한 라우트로 연결', 'Dispatch through registered routes')],
      [P('데이터 응답', 'Data response'), P('헤더·직렬화·종료 처리 구성', 'Set headers, serialize, and end'), P('res.json 등 응답 API 사용', 'Use response APIs such as res.json')]), refs=[NODE, EXPRESS])

body('node-project',
    D('Node.js 프로젝트 - 실행 설정과 의존성을 함께 관리하는 단위',
      'Node.js project - A unit that manages execution settings and dependencies',
      P('package.json은 프로젝트 정보·명령·의존성 선언', 'package.json declares project information, commands, and dependencies'),
      P('package-lock.json은 재현 가능한 설치를 위한 버전·의존 관계 기록', 'package-lock.json records versions and dependency relationships for repeatable installation'),
      P('node_modules는 설치 결과 · 저장소에는 설정과 잠금 파일 보관', 'node_modules contains installed packages; repositories retain configuration and lockfiles'),
      P('새 프로젝트의 설치는 npm install · 잠금 파일 기반 재설치는 npm ci', 'Use npm install for initial setup and npm ci for installation from a lockfile')),
    K('새 폴더에서 실행 · Node.js 24 LTS · Express 5.3.0', 'Run in a new folder · Node.js 24 LTS · Express 5.3.0', '''
mkdir foodmap-api
cd foodmap-api
npm init -y
npm install express@5.3.0
''', lang='bash'), refs=['https://expressjs.com/en/starter/installing.html', 'https://docs.npmjs.com/cli/v11/commands/npm-ci', 'https://github.com/expressjs/express/releases/tag/v5.3.0', 'https://nodejs.org/en/blog/release/v24.22.0'])

body('commonjs',
    D('CommonJS 모듈 - 파일별 기능을 공개하고 불러오는 방식',
      'CommonJS module - A way to export and load functionality by file',
      P('module.exports는 다른 파일에 공개할 값 지정', 'module.exports specifies the value exposed to other files'),
      P('require는 패키지나 상대 경로 모듈의 공개값 불러오기', 'require loads an exported value from a package or relative module path'),
      P('.cjs 확장자는 CommonJS 실행 방식의 명시적 표시', 'The .cjs extension explicitly selects CommonJS execution'),
      P('이 강의의 실행 예제는 .cjs 사용 · JSX·TSX 없이 Node.js에서 실행', 'Lecture examples use .cjs and run in Node.js without JSX or TSX')),
    K('독립 실행 · 두 파일을 같은 폴더에 저장 후 node main.cjs', 'Standalone · save both files together, then node main.cjs', '''
// greeting.cjs
function greet(name) {
  return `Hello, ${name}`;
}
module.exports = { greet };

// main.cjs
const { greet } = require('./greeting.cjs');
console.log(greet('Ajou'));
''', result=[P('Hello, Ajou', 'Hello, Ajou')]), refs=['https://nodejs.org/api/modules.html'])

body('hello-server',
    D('Express 서버 시작 - 요청 처리 앱을 포트에 연결하는 과정',
      'Starting an Express server - Connect a request-processing app to a port',
      P('express()는 라우트를 등록할 애플리케이션 객체 생성', 'express() creates an application object for registering routes'),
      P('app.get은 GET 요청의 경로와 처리 함수를 연결', 'app.get associates a GET path with a handler'),
      P('res.send는 응답 본문을 보내고 해당 응답 종료', 'res.send sends the response body and ends the response'),
      P('app.listen은 지정한 포트에서 HTTP 요청 대기 시작', 'app.listen starts listening for HTTP requests on a port')),
    K('독립 실행 · server.cjs · Express 설치 후 node server.cjs', 'Standalone · server.cjs · install Express, then node server.cjs', '''
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000);
''', result=[P('GET http://localhost:3000/ → 200 · Hello World!', 'GET http://localhost:3000/ → 200 · Hello World!')]), refs=['https://expressjs.com/en/starter/hello-world.html'])

body('express-routing',
    D('라우팅 - 요청의 메서드와 경로를 처리 함수에 연결하는 과정',
      'Routing - Map a request method and path to a handler',
      P('라우트는 메서드·경로·핸들러의 조합', 'A route combines a method, a path, and a handler'),
      P('핸들러는 요청 정보로 작업을 수행하고 응답 생성', 'The handler processes request information and produces a response'),
      P('같은 경로에도 GET과 POST 등 서로 다른 처리 등록 가능', 'The same path can register different handlers for methods such as GET and POST'),
      P('쿼리 문자열은 라우트 경로 매칭에 포함되지 않는 조회 조건', 'Query strings supply retrieval conditions outside route-path matching')),
    K('발췌 · Express app 생성 후 등록', 'Excerpt · register after creating an Express app', '''
app.get('/foods', (req, res) => {
  res.json([{ id: 1, name: 'Campus Noodles' }]);
});

app.post('/foods', (req, res) => {
  res.status(201).json({ id: 2, name: 'Campus Rice' });
});
'''), refs=[EXPRESS])

body('path-params',
    D('경로 매개변수 - URL 경로의 일부에서 추출한 이름 있는 값',
      'Route parameter - A named value captured from a URL path segment',
      P(':이름 표기로 경로의 가변 부분 지정', 'A colon-prefixed name marks a variable path segment'),
      P('req.params는 지정한 이름으로 추출값 제공', 'req.params exposes captured values under the declared names'),
      P('단일 :id의 값은 문자열 · 숫자 사용 전 변환과 유효성 확인 필요', 'A single :id is a string; numeric use requires conversion and validation')),
    K('발췌 · Express app 생성 후 등록', 'Excerpt · register after creating an Express app', '''
app.get('/foods/:id', (req, res) => {
  res.json({ receivedId: req.params.id });
});
''', result=[P('GET /foods/7 → {"receivedId":"7"}', 'GET /foods/7 → {"receivedId":"7"}')]), refs=[EXPRESS])

body('query',
    D('쿼리 매개변수 - URL에서 검색 조건과 조회 옵션을 전달하는 값',
      'Query parameter - A URL value carrying search conditions or retrieval options',
      P('경로 뒤 ?로 시작 · 이름과 값의 쌍을 &로 연결', 'Begins after ? in the URL; & separates name–value pairs'),
      P('req.query는 설정된 쿼리 파서의 해석 결과', 'req.query contains the result produced by the configured query parser'),
      P('누락·중복 입력을 고려해 타입을 확인한 뒤 조건으로 사용', 'Check types before using values, accounting for missing or repeated inputs')),
    K('발췌 · 문자열 조건만 수용하는 조회 입력', 'Excerpt · accept only a string query condition', '''
app.get('/foods', (req, res) => {
  const q = typeof req.query.q === 'string'
    ? req.query.q
    : '';
  res.json({ query: q });
});
''', result=[P('GET /foods?q=rice → {"query":"rice"}', 'GET /foods?q=rice → {"query":"rice"}')]), refs=[EXPRESS, API])

body('middleware',
    D('미들웨어 - 요청과 응답 사이에서 실행하는 처리 함수',
      'Middleware - A processing function in the request–response pipeline',
      P('req·res는 현재 요청과 응답 · next는 후속 처리로 넘기는 함수', 'req and res represent the current exchange; next transfers control'),
      P('app.use는 공통 함수를 등록 · 등록 순서가 실행 흐름 결정', 'app.use registers shared functions; registration order determines the flow'),
      P('next() 호출로 후속 처리 진행 · 응답을 종료한 경로는 후속 호출 생략', 'Call next() to continue; a path that ends the response stops forwarding'),
      P('응답 종료와 next 호출이 모두 없으면 요청 처리 대기 상태 유지', 'Without ending the response or calling next, processing remains pending')),
    K('발췌 · 라우트보다 먼저 등록하는 요청 로그', 'Excerpt · request logger registered before routes', '''
app.use((req, res, next) => {
  console.log(req.method, req.path);
  next();
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});
'''), MIDDLEWARE_FLOW, layout='diagram-code', refs=[MIDDLEWARE])

body('json-body',
    D('JSON 본문 파싱 - 요청의 JSON 텍스트를 req.body에 연결하는 처리',
      'JSON body parsing - Convert request JSON text into req.body',
      P('express.json()은 JSON 본문을 해석하는 내장 미들웨어', 'express.json() is built-in middleware that parses JSON request bodies'),
      P('JSON을 받는 라우트보다 앞에 등록 · Content-Type에 따라 파싱 적용', 'Register before JSON routes; Content-Type determines whether parsing applies'),
      P('파싱 성공 후 req.body로 값 접근 · 타입·필수값 검증은 별도 단계', 'After parsing, req.body exposes the value; type and required-field checks remain separate'),
      P('본문 크기 제한은 요청 본문 처리에 허용할 최대 크기', 'The body limit bounds the amount of request data to process')),
    K('발췌 · 파서 등록 후 POST 라우트 등록', 'Excerpt · register the parser before the POST route', '''
app.use(express.json({ limit: '10kb' }));

app.post('/echo', (req, res) => {
  res.json(req.body);
});
''', result=[P('Content-Type: application/json · {"name":"Rice"} → 같은 JSON 응답', 'Content-Type: application/json · {"name":"Rice"} → the same JSON response')]), refs=[MIDDLEWARE, API])

body('input-validation',
    D('입력 검증 - 외부 입력이 처리 조건을 만족하는지 확인하는 과정',
      'Input validation - Check whether external data meets processing requirements',
      P('클라이언트의 검증 여부와 무관하게 서버에서 입력 확인', 'The server checks inputs regardless of client-side validation'),
      P('문자열·숫자 등의 타입 확인 후 허용 범위와 필수값 검사', 'Check types before checking allowed ranges and required values'),
      P('조건을 만족하지 못한 입력은 상태 코드와 오류 정보로 응답', 'Return a status code and error details when input fails requirements'),
      P('검증 실패 뒤 작업이 계속되지 않도록 처리 경로 종료', 'End the processing path so work does not continue after validation failure')),
    K('발췌 · JSON 파서 이후 등록하는 검증 예', 'Excerpt · validation after JSON body parsing', '''
app.post('/foods', (req, res) => {
  const name = req.body?.name;
  if (typeof name !== 'string' || !name.trim()) {
    return res.status(400).json({ error: 'Name is required' });
  }
  res.status(201).json({ name: name.trim() });
});
'''), refs=[API])

body('error-handler',
    D('오류 처리 미들웨어 - 전달된 오류를 HTTP 응답으로 변환하는 함수',
      'Error-handling middleware - Convert forwarded errors into HTTP responses',
      P('오류 처리 함수는 err·req·res·next의 네 인자 사용', 'The handler uses four arguments: err, req, res, and next'),
      P('next(err)는 정상 처리 대신 오류 처리 흐름으로 전달', 'next(err) transfers control from normal processing to error handling'),
      P('라우트 뒤에 등록해 전달된 오류의 응답 형식 통일', 'Register after routes to standardize responses for forwarded errors'),
      P('내부 오류의 상세 정보는 공개 응답에서 제외 · 이미 응답을 시작한 경우 후속 처리로 전달', 'Exclude internal details from public responses; delegate if a response has already started')),
    K('실행 소스 발췌 · src/middleware/error-handler.cjs', 'Executable source excerpt · src/middleware/error-handler.cjs',
      source_code('src/middleware/error-handler.cjs', function='errorHandler')), refs=[ERRORS])

body('async-handler',
    D('비동기 핸들러 오류 - 반환한 Promise의 실패를 오류 처리로 연결',
      'Async handler error - Forward failure from the returned promise to error handling',
      P('async 함수의 throw와 await의 실패는 반환 Promise의 거부로 표현', 'A throw or a failed await in an async function rejects its returned promise'),
      P('Express 5는 핸들러가 반환한 Promise의 거부를 자동으로 오류 처리에 전달', 'Express 5 automatically forwards a rejected promise returned by a handler'),
      P('분리된 타이머·콜백의 오류는 자동 전달 대상에서 제외 · 명시적 next(err) 필요', 'Errors in detached timers or callbacks require explicit forwarding with next(err)')),
    K('독립 실행 · Express 5 · 실패 경로 관찰용 server.cjs', 'Standalone · Express 5 · server.cjs for observing failure', '''
const express = require('express');
const app = express();
app.get('/fail', async (req, res) => {
  await Promise.reject(new Error('Unavailable'));
  res.json({ ok: true });
});
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message });
});
app.listen(3000);
''', result=[P('GET /fail → 500 · {"error":"Unavailable"}', 'GET /fail → 500 · {"error":"Unavailable"}')]), refs=[ERRORS])

# 04. MVC and the service layer
body('mvc',
    D('MVC - 모델·뷰·컨트롤러의 책임을 분리하는 설계 패턴',
      'MVC - A design pattern separating model, view, and controller responsibilities',
      P('모델은 데이터와 관련 규칙 관리', 'The model manages data and related rules'),
      P('뷰는 사용자에게 제공할 표현 구성', 'The view builds the presentation offered to the user'),
      P('컨트롤러는 입력을 받아 필요한 작업과 응답 조정', 'The controller receives input and coordinates work and responses'),
      P('서버 렌더링에서는 템플릿이 뷰 담당 · 분리된 SPA에서는 클라이언트가 화면 구성', 'Templates provide the view in server rendering; a separate SPA constructs its UI on the client')),
    MVC, refs=['https://martinfowler.com/eaaCatalog/modelViewController.html'])

body('mvcs',
    D('MVCS - MVC에 업무 규칙을 담당하는 서비스 계층을 추가한 구조',
      'MVCS - MVC extended with a service layer for business rules',
      P('컨트롤러는 HTTP 입력·응답 변환에 집중', 'Controllers focus on translating HTTP inputs and responses'),
      P('서비스는 업무 조건을 검증하고 필요한 모델 작업 조합', 'Services enforce business constraints and coordinate model operations'),
      P('모델은 데이터의 조회·저장 방식 담당', 'Models handle data retrieval and storage'),
      P('서비스는 HTTP 객체에 의존하지 않아 다른 진입점에서도 재사용 가능', 'Services can be reused by other entry points because they do not depend on HTTP objects')),
    MVCS, refs=['https://martinfowler.com/eaaCatalog/serviceLayer.html'])

body('project-structure',
    D('프로젝트 구조 - 변경 이유가 다른 코드를 역할별 모듈로 구분',
      'Project structure - Separate modules with different reasons to change',
      P('server.cjs는 실행 설정과 포트 대기 담당', 'server.cjs manages runtime configuration and listening'),
      P('app.cjs는 앱 생성과 미들웨어·계층 모듈 연결', 'app.cjs creates the app and connects middleware and layer modules'),
      P('앱 생성과 포트 대기를 분리하면 필요한 환경에서 같은 앱 재사용 가능', 'Separating app creation from listening lets multiple environments reuse the same app'),
      P('디렉터리 이름보다 모듈 사이의 의존 방향과 책임 경계가 핵심', 'Dependency direction and responsibility boundaries matter more than directory names')),
    K('실행 예제 · examples/의 주요 파일', 'Executable example · main files in examples/', '''
examples/
  server.cjs
  src/
    app.cjs
    routes/food-routes.cjs
    controllers/food-controller.cjs
    services/food-service.cjs
    models/food-model.cjs
    middleware/error-handler.cjs
  test/
    food-service.test.cjs
    api.test.cjs
''', lang='text'), refs=[MIDDLEWARE])

body('model',
    D('모델의 데이터 접근 - 저장소의 세부 처리를 감추는 인터페이스',
      'Model data access - An interface that hides storage implementation details',
      P('조회·생성 등 데이터 작업을 함수로 공개', 'Expose data operations such as lookup and creation as functions'),
      P('호출자는 배열·파일·DB 등 실제 저장 방식과 분리', 'Callers remain independent of the underlying array, file, or database'),
      P('예제의 메모리 저장소는 앱 인스턴스 수명 동안만 유지', 'The example memory store lasts only for the application instance lifetime'),
      P('반환값을 복사하면 호출자의 변경이 내부 저장값에 직접 전파되는 문제 방지', 'Copying returned values prevents caller mutations from directly changing internal storage')),
    K('실행 소스 발췌 · 모델 팩터리 내부 · foods 배열 참조', 'Executable source excerpt · inside model factory · uses foods array',
      source_code('src/models/food-model.cjs', function='findById')), refs=['https://martinfowler.com/eaaCatalog/serviceLayer.html'])

body('service',
    D('서비스 - 업무 규칙을 적용하고 모델의 작업을 조합하는 계층',
      'Service - A layer that applies business rules and coordinates model operations',
      P('입력은 업무에 필요한 값 · 출력은 처리 결과 또는 오류', 'Inputs are business values; outputs are results or errors'),
      P('모델은 생성 시 외부에서 전달받는 데이터 접근 객체', 'The data-access model is supplied externally when the service is created'),
      P('HTTP 요청·응답 객체에 의존하지 않고 유효성 판단과 정규화 수행', 'Performs validation and normalization without depending on HTTP request or response objects'),
      P('이 예제의 status 오류 속성은 HTTP 응답 변환을 위한 간단한 계약', 'The example status error property is a simple contract for HTTP error translation')),
    K('실행 소스 발췌 · 서비스 팩터리 내부 · model 주입', 'Executable source excerpt · inside service factory · injected model',
      source_code('src/services/food-service.cjs', function='addFood')), refs=['https://martinfowler.com/eaaCatalog/serviceLayer.html'])

body('controller',
    D('컨트롤러 - HTTP의 입력과 서비스의 출력을 연결하는 계층',
      'Controller - A layer connecting HTTP inputs with service outputs',
      P('요청의 경로·쿼리·본문에서 서비스에 전달할 값 추출', 'Extract service input values from request paths, queries, and bodies'),
      P('서비스가 반환한 결과를 HTTP 상태·헤더·본문으로 변환', 'Convert service results into an HTTP status, headers, and body'),
      P('생성 성공은 201과 새 리소스 위치 전달 · 업무 규칙은 서비스에 위임', 'Return 201 and the new resource location for creation; delegate business rules to the service')),
    K('실행 소스 발췌 · 컨트롤러 팩터리 내부 · service 주입', 'Executable source excerpt · inside controller factory · injected service',
      source_code('src/controllers/food-controller.cjs', function='create'),
      result=[P('POST /foods → 201 · Location: /foods/2', 'POST /foods → 201 · Location: /foods/2')]), refs=[API, ERRORS])

body('router',
    D('Express Router - 관련 라우트를 묶어 앱에 연결하는 모듈',
      'Express Router - A module that groups related routes and mounts on an app',
      P('Router 내부의 경로는 앱에 연결한 경로를 기준으로 해석', 'Router paths are resolved relative to the app mounting path'),
      P('메서드와 상대 경로는 컨트롤러의 처리 함수에 연결', 'Methods and relative paths map to controller handlers'),
      P('모듈 생성 시 컨트롤러를 전달해 라우트 등록과 처리 구현 분리', 'Inject a controller when creating the module to separate registration from processing')),
    K('실행 소스 발췌 · express 불러오기 이후 · /foods에 연결', 'Executable source excerpt · after loading express · mounted at /foods',
      source_code('src/routes/food-routes.cjs', function='createFoodRouter'),
      result=[P('router.get("/:id", …) + /foods → GET /foods/:id', 'router.get("/:id", …) + /foods → GET /foods/:id')]), refs=[EXPRESS])

# 05. Testing and deployment
body('tdd',
    D('TDD - 실패하는 테스트에서 시작하는 짧은 개발 반복',
      'TDD - A short development cycle starting with a failing test',
      P('요구사항을 관찰 가능한 입력과 결과의 관계로 표현', 'Express a requirement as an observable relationship between input and outcome'),
      P('테스트를 먼저 실행해 의도한 이유로 실패하는지 확인', 'Run the test first and verify that it fails for the intended reason'),
      P('구조 개선 후에도 같은 동작 계약을 테스트로 유지', 'Keep the same behavioral contract under test after structural improvements')),
    TDD, layout='stack', refs=['https://martinfowler.com/bliki/TestDrivenDevelopment.html'])

body('unit-test',
    D('단위 테스트 - 작은 기능의 입력과 결과를 독립적으로 검증',
      'Unit test - Independently verify inputs and outcomes of a small unit',
      P('서비스 테스트는 HTTP 서버 없이 업무 규칙 호출', 'A service test invokes business rules without an HTTP server'),
      P('매 테스트마다 새 모델로 시작해 이전 실행의 데이터 영향 제거', 'A fresh model for each test removes data effects from earlier runs'),
      P('비동기 실패는 assert.rejects로 거부와 오류 속성 확인', 'assert.rejects checks asynchronous rejection and error properties')),
    K('실행 소스 발췌 · test/food-service.test.cjs · 상단 import 필요', 'Executable source excerpt · test/food-service.test.cjs · requires top-level imports',
      source_code('test/food-service.test.cjs', start="test('rejects a blank name'", end='});'),
      result=[P('examples/에서 npm test · 검증이 없으면 실패', 'Run npm test in examples/; this test fails without validation')]), refs=[TEST, 'https://nodejs.org/api/assert.html#assertrejectsasyncfn-error-message'])

body('api-test',
    D('HTTP API 테스트 - 요청에서 응답까지의 연결을 검증하는 테스트',
      'HTTP API test - Verify the connection from request to response',
      P('앱을 임시 포트로 실행하고 실제 HTTP 요청 전송', 'Start the app on a temporary port and send real HTTP requests'),
      P('상태 코드·헤더·본문은 클라이언트와의 계약', 'The status, headers, and body form the client contract'),
      P('라우트·파서·컨트롤러·서비스 연결의 오류를 함께 확인', 'Check route, parser, controller, and service integration'),
      P('테스트 종료 시 서버를 닫아 포트와 실행 자원 해제', 'Close the server after the test to release its port and runtime resources')),
    K('실행 소스 발췌 · test/api.test.cjs · serve(t)는 임시 서버 생성·정리', 'Executable source excerpt · test/api.test.cjs · serve(t) starts and closes a temporary server',
      source_code('test/api.test.cjs', start="test('GET /foods returns the initial list'", end='});')), refs=[TEST])

body('environment',
    D('환경변수 - 코드 밖에서 실행 설정을 전달하는 이름과 값',
      'Environment variable - A name–value setting supplied outside the code',
      P('process.env는 실행 환경이 전달한 설정에 접근하는 객체', 'process.env exposes settings supplied by the runtime environment'),
      P('포트와 클라이언트 출처를 환경별로 분리해 같은 코드 사용', 'Use the same code with environment-specific ports and client origins'),
      P('환경변수의 값은 문자열 · 숫자가 필요한 설정은 변환', 'Environment values are strings; convert numeric settings'),
      P('서버 진입점에서 앱 생성과 포트 대기를 연결', 'The server entry point connects app creation to listening')),
    K('실행 소스 전체 · examples/server.cjs', 'Complete executable source · examples/server.cjs', source_code('server.cjs')), refs=['https://nodejs.org/api/process.html#processenv', 'https://render.com/docs/web-services#port-binding'])

body('render',
    D('Render 웹 서비스 - 저장소의 코드를 실행 중인 서버로 배포하는 환경',
      'Render web service - An environment deploying repository code as a running server',
      P('연결한 저장소와 브랜치에서 빌드·시작 명령 실행', 'Runs build and start commands from a connected repository and branch'),
      P('서버는 PORT 환경변수와 0.0.0.0 호스트로 요청 대기', 'The server listens using the PORT environment variable and host 0.0.0.0'),
      P('배포 성공은 로그와 /health 응답으로 확인', 'Check deployment through logs and the /health response'),
      P('무료 웹 서비스는 15분 무요청 시 중지 · 월 750시간을 워크스페이스에서 공유', 'Free web services idle after 15 minutes; the workspace shares 750 instance hours per month'),
      P('메모리 데이터는 재시작 시 초기화 · 영구 저장에는 별도 저장소 필요', 'Memory data resets on restart; persistence requires separate storage')),
    T([P('설정', 'Setting'), P('이 저장소 예제 기준', 'For this repository example')],
      [P('Service Type', 'Service Type'), P('Web Service · Node', 'Web Service · Node')],
      [P('Root Directory', 'Root Directory'), P('lectures/06/examples', 'lectures/06/examples')],
      [P('Node.js', 'Node.js'), P('NODE_VERSION=24.22.0', 'NODE_VERSION=24.22.0')],
      [P('Build / Start', 'Build / Start'), P('npm ci / npm start', 'npm ci / npm start')],
      [P('Health Check / Env', 'Health Check / Env'), P('/health · CLIENT_ORIGIN=실제 프런트엔드 출처', '/health · CLIENT_ORIGIN=actual frontend origin')]), refs=[RENDER, 'https://render.com/docs/web-services#port-binding', 'https://render.com/docs/free', 'https://render.com/docs/node-version'])

body('cors',
    D('CORS - 브라우저가 다른 출처의 응답 읽기를 허용하는 규칙',
      'CORS - Rules governing browser access to responses from another origin',
      P('출처는 스킴·호스트·포트의 조합 · 하나라도 다르면 다른 출처', 'An origin combines scheme, host, and port; any difference makes another origin'),
      P('서버의 허용 헤더를 확인한 브라우저가 JavaScript의 응답 읽기 결정', 'The browser checks server permission headers before exposing the response to JavaScript'),
      P('JSON POST 등 일부 요청은 OPTIONS 사전 요청으로 허용 조건 확인', 'Some requests, including JSON POSTs, use an OPTIONS preflight'),
      P('CORS는 인증·인가와 별개 · curl이나 다른 서버의 접근 차단 기능은 아님', 'CORS is separate from authentication and authorization; it does not block curl or other servers')),
    K('발췌 · npm install cors · 라우트보다 먼저 등록', 'Excerpt · npm install cors · register before routes', '''
const cors = require('cors');

app.use(cors({
  origin: 'http://localhost:5173'
}));
''', result=[P('개발 출처 5173 → API 포트 3000의 응답 읽기 허용', 'Allow the development origin on 5173 to read API responses on 3000')]),
    CORS_FLOW, layout='diagram-code', refs=['https://expressjs.com/en/resources/middleware/cors.html'])

body('frontend-api',
    D('API 호출 - 네트워크 응답을 화면에서 사용할 값으로 변환하는 과정',
      'API call - Convert a network response into values used by the UI',
      P('fetch는 HTTP 응답 객체를 반환하는 Promise 제공', 'fetch provides a promise for an HTTP response object'),
      P('404·500 응답도 Promise 성공 가능 · response.ok로 HTTP 성공 여부 확인', '404 and 500 can fulfill the promise; response.ok checks HTTP success'),
      P('response.json()은 본문을 읽고 JSON 값으로 변환하는 비동기 작업', 'response.json() asynchronously reads the body and parses it as JSON'),
      P('React에서는 결과·로딩·오류를 상태에 반영해 화면 갱신', 'In React, results, loading, and errors update UI state')),
    K('브라우저 콘솔 · 로컬 예제 서버와 허용된 출처에서 실행', 'Browser console · run with the local server and an allowed origin', '''
async function loadFoods() {
  const response = await fetch('http://localhost:3000/foods');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

loadFoods().then(console.log).catch(console.error);
'''), refs=['https://fetch.spec.whatwg.org/'])


PRACTICE = [
    D('Foodmap API 실습 - React 화면과 서버 데이터를 연결하는 수업 예제',
      'Foodmap API lab - Connect a React UI to server data',
      P('로컬 예제의 목록 조회·상세 조회·맛집 생성을 요청으로 확인', 'Check list retrieval, detail retrieval, and creation in the local example'),
      P('잘못된 이름·식별값·없는 리소스의 상태 코드와 JSON 오류 확인', 'Check status codes and JSON errors for invalid names, identifiers, and absent resources'),
      P('서비스 규칙과 HTTP 응답을 테스트로 검증', 'Verify service rules and HTTP responses with tests'),
      P('React의 로컬 목록을 API 응답으로 교체 · 배포 시 실제 API 주소 사용', 'Replace the local React list with an API response; use the real API URL when deployed')),
    K('저장소 루트에서 실행 · 터미널 1', 'Run from the repository root · terminal 1', '''
cd lectures/06/examples
npm ci
npm test
npm start
''', lang='bash'),
    K('요청 확인 · 터미널 2 · 생성 후 응답의 Location 조회', 'Check requests · terminal 2 · retrieve the returned Location', r'''
curl -i http://localhost:3000/foods
curl -i -X POST http://localhost:3000/foods \
  -H 'Content-Type: application/json' \
  -d '{"name":"Campus Rice"}'
''', lang='bash'),
]
