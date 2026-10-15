"""Bilingual, editable diagrams derived from the reviewed original PDF.

Only concepts already introduced on the associated slide are represented.
Old raster text, decorative logos, and the 2025 ranking are not copied.
"""


def P(ko, en):
    return (ko, en)


def N(ko, en, detail_ko, detail_en):
    return (P(ko, en), P(detail_ko, detail_en))


def flow(caption, alt, *rows, vertical=False, repeat=None):
    return dict(kind='diagram', variant='vertical' if vertical else 'flow',
                caption=caption, alt=alt, rows=list(rows), repeat=repeat)


CLIENT_SERVER = dict(
    kind='diagram', variant='exchange',
    caption=P('클라이언트와 서버의 메시지 교환', 'Messages between a client and server'),
    alt=P('클라이언트가 네트워크를 통해 서버에 요청 전달. 서버는 처리 결과를 클라이언트에 응답으로 반환.',
          'A client sends a request to a server over the network. The server returns the result to the client in a response.'),
    nodes=[N('클라이언트', 'Client', '사용자 입력·화면', 'User input and UI'),
           N('서버', 'Server', '요청 처리·결과', 'Processing and results')],
    links=[P('요청', 'Request'), P('응답', 'Response')])

SERVER_ROLE = flow(
    P('요청 한 건의 서버 처리', 'Server processing for one request'),
    P('요청 수신, 입력 검증, 업무 규칙과 데이터 처리, 응답 생성 순서.',
      'Receive a request, validate input, apply business and data operations, and construct a response.'),
    dict(nodes=[N('수신', 'Receive', '요청 입력 수집', 'Collect request inputs'),
                N('검증', 'Validate', '타입·권한 확인', 'Check types and permissions'),
                N('처리', 'Process', '규칙·데이터 접근', 'Rules and data access'),
                N('반환', 'Respond', '결과·오류 전달', 'Send results or errors')]))

ASYNC_IO = flow(
    P('I/O 완료와 JavaScript 실행', 'I/O completion and JavaScript execution'),
    P('I/O 요청 후 제어권 반환. 외부 완료 대기 중 다른 JavaScript 실행 가능. 준비된 결과를 후속 처리에 전달.',
      'Control returns after requesting I/O. Other JavaScript can run while external work completes. The ready result reaches subsequent processing.'),
    dict(nodes=[N('작업 요청', 'Request work', '외부 I/O 시작', 'Start external I/O'),
                N('제어권 반환', 'Return control', '대기 중 다른 코드 실행', 'Run other code while waiting'),
                N('결과 전달', 'Deliver result', '완료된 값의 후속 처리', 'Process the completed value')]), vertical=True)

MIDDLEWARE = flow(
    P('GET /health의 정상 처리', 'Normal processing of GET /health'),
    P('GET /health 요청은 로그 미들웨어에서 next 호출 후 라우트에 도달. 라우트의 JSON 응답으로 요청 처리 종료.',
      'A GET /health request passes the logger through next, reaches the route, and ends with a JSON response.'),
    dict(nodes=[N('요청', 'Request', 'GET /health', 'GET /health'),
                N('로그', 'Logger', 'next()', 'next()'),
                N('라우트', 'Route', 'res.json(…)', 'res.json(…)'),
                N('응답', 'Response', '200 · status: ok', '200 · status: ok')]))

MVC = flow(
    P('서버 렌더링 MVC의 요청·응답 관계', 'Request and response in server-rendered MVC'),
    P('요청을 받은 컨트롤러가 모델에 작업을 요청하고 결과를 반환받은 뒤 뷰에 전달. 뷰가 화면 표현 구성.',
      'The controller receives input, calls the model, receives its result, and supplies it to a view that builds the presentation.'),
    dict(label=P('입력과 데이터 처리', 'Input and data processing'),
         nodes=[N('Request', 'Request', '사용자 입력', 'User input'),
                N('Controller', 'Controller', '요청 조정', 'Coordinate the request'),
                N('Model', 'Model', '데이터·규칙', 'Data and rules')]),
    dict(label=P('결과와 화면 표현', 'Result and presentation'),
         nodes=[N('Model', 'Model', '처리 결과', 'Processing result'),
                N('Controller', 'Controller', '결과 전달', 'Supply the result'),
                N('View', 'View', '화면 구성', 'Build the presentation')]))

MVCS = flow(
    P('Foodmap API 계층의 값 전달', 'Values passed through Foodmap API layers'),
    P('컨트롤러는 HTTP 입력을 서비스에 전달. 서비스는 업무 규칙에 따라 모델을 호출. 결과는 역순으로 반환.',
      'The controller passes HTTP inputs to the service. The service calls the model under business rules. Results return through the layers in reverse order.'),
    dict(bidirectional=True, nodes=[
        N('Controller', 'Controller', 'HTTP 입력·응답', 'HTTP inputs and responses'),
        N('Service', 'Service', '업무 규칙', 'Business rules'),
        N('Model', 'Model', '데이터 조회·저장', 'Retrieve and store data')]))

TDD = flow(
    P('빈 이름 거부 규칙의 개발 주기', 'Development cycle for rejecting blank names'),
    P('Red에서 빈 이름 거부 테스트의 실패 확인. Green에서 최소 검증 구현. Refactor에서 테스트 성공을 유지하며 개선. 새 요구사항으로 반복.',
      'Red checks that blank-name rejection fails. Green implements minimal validation. Refactor improves the code while tests pass. Repeat with a new requirement.'),
    dict(nodes=[N('Red', 'Red', '의도한 요구 위반의 실패', 'Fail for the intended requirement'),
                N('Green', 'Green', '테스트 통과 최소 구현', 'Implement enough to pass'),
                N('Refactor', 'Refactor', '동작 유지·구조 개선', 'Preserve behavior and improve structure')]),
    repeat=P('새 요구사항의 실패 테스트로 반복', 'Repeat with a failing test for the next requirement'))

CORS = flow(
    P('응답을 받은 뒤의 브라우저 처리', 'Browser processing after receiving a response'),
    P('서버가 응답에 허용 출처 헤더를 추가. 브라우저가 요청 출처와 허용 조건을 확인. 허용된 경우 JavaScript가 응답을 읽을 수 있음.',
      'The server adds an allowed-origin header. The browser checks the calling origin against this permission. JavaScript can read the response when allowed.'),
    dict(nodes=[N('서버', 'Server', '허용 출처 헤더', 'Allowed-origin header'),
                N('브라우저', 'Browser', '출처·헤더 확인', 'Check the origin and header'),
                N('JavaScript', 'JavaScript', '허용된 응답 읽기', 'Read the permitted response')]))
