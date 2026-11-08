"""The 16 Week 6 resource adaptations used with the completed slide bodies.

Keep audit source files intact. New resources live in new_resources.py;
slide_body.py composes these examples with their bilingual explanations.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = next((ROOT / 'materials').glob('[[]PWD Week6]*.pdf')).name
SOURCE_DIR = 'materials/week6-asset-audit/source-assets/'
COOKIE_DOC = 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie'
SESSION_DOC = 'https://expressjs.com/en/resources/middleware/session/'
JWT_DOC = 'https://www.rfc-editor.org/rfc/rfc7519.html'
JWT_BCP = 'https://www.rfc-editor.org/rfc/rfc8725.html'
OAUTH_DOC = 'https://www.rfc-editor.org/rfc/rfc6749.html'
OIDC_DOC = 'https://openid.net/specs/openid-connect-core-1_0.html'
PKCE_DOC = 'https://www.rfc-editor.org/rfc/rfc7636.html'


def pair(ko, en=None):
    return (ko, ko if en is None else en)


def code(label, text, language='text', width=64):
    return dict(kind='code', label=label, text=pair(text), language=language, width=width)


def table(head, rows):
    return dict(kind='table', head=head, rows=rows)


def message(start, end, ko, en=None, **options):
    return dict({'from': start, 'to': end, 'text': pair(ko, en)}, **options)


def sequence(actors, rows, caption):
    return dict(kind='resource-sequence', actors=actors, rows=rows, caption=caption)


def resource(assets, pages, correction, columns, *, layout='single', refs=()):
    return dict(assets=assets.split(), pages=pages, correction=correction,
                layout=layout, columns=columns,
                sources=[f'materials/{PDF} · PDF {", ".join(map(str, pages))}쪽', *refs])


BROWSER = pair('브라우저', 'Browser')
SERVER = pair('서비스 서버', 'Service server')
PROVIDER = pair('외부 제공자', 'External provider')
CLIENT_SERVER = [BROWSER, SERVER]
OAUTH_ACTORS = [BROWSER, pair('FoodMap 서버', 'FoodMap server'), PROVIDER]
OAUTH_CAPTION = pair('서버가 코드를 교환하는 사례 · ID 토큰은 OIDC 사용 시 반환',
                     'Server-side code exchange · An ID token is returned when using OIDC')


def token_sequence(jwt=False):
    """The same source geometry supports generic tokens, then JWT validation."""
    name = 'JWT' if jwt else 'token'
    check = pair('서명·발급 조건 검증', 'Verify signature and claims') if jwt else pair('토큰 확인', 'Check the token')
    return sequence(CLIENT_SERVER, [
        message(0, 1, '로그인 정보 전달', 'Submit login credentials'),
        message(1, 0, 'JWT 발급' if jwt else '토큰 발급', 'Issue JWT' if jwt else 'Issue token', reply=True),
        message(0, 1, f'Authorization: Bearer <{name}>'),
        message(1, 1, *check, focus=jwt),
        message(1, 0, '검증 후 요청 처리 결과', 'Request result after validation', reply=True),
    ], pair('Bearer 전달 사례 · 꺾쇠 안의 값은 자격정보의 자리표시',
            'Bearer transport example · Angle brackets mark a credential placeholder'))


RESOURCES = {
    'authentication': resource('I09-login', [9],
        '원본의 이메일·비밀번호 영역을 HTML로 재구성. 주소를 예시 값으로 바꾸고 외부 로그인 버튼 제거.',
        [[dict(kind='login-screen', caption=pair('이메일·비밀번호 입력 화면 예시', 'Example email and password form'))],
         [table([pair('입력', 'Input'), pair('역할', 'Role')], [
             [pair('이메일', 'Email'), pair('확인할 계정의 선택', 'Identify the account to check')],
             [pair('비밀번호', 'Password'), pair('해당 계정에 대한 증거', 'Provide evidence for that account')],
         ])]], layout='split'),
    'password-login': resource('I09-flow', [9],
        '원본의 입력→신원 확인을 편집 가능한 흐름으로 변환. 해시·솔트 검증과 사용자 ID 결과 보강. 상태 기억 단계 제외.',
        [[dict(kind='resource-flow', items=[
            dict(title=pair('로그인 정보 입력', 'Enter credentials'),
                 body=pair('이메일·비밀번호\n브라우저 → 서버', 'Email and password\nBrowser → server')),
            dict(title=pair('서버의 증거 검증', 'Server verification'),
                 body=pair('계정의 저장된 해시·솔트\n입력 비밀번호와 대조', 'Stored hash and salt\nVerify the entered password')),
            dict(title=pair('사용자 ID 확인', 'Establish the user ID'),
                 body=pair('검증 성공 → u123\n검증 실패 → 인증 거부', 'Valid evidence → u123\nInvalid evidence → reject login')),
        ], caption=pair('비밀번호 전용 검증 함수 사용 · u123은 사용자 ID의 예시',
                        'Use a password verification function · u123 is an example user ID'))]]),
    'cookies': resource('C12', [12],
        '헤더의 값 저장·첨부 부분만 발췌. 날짜와 보호 속성은 제외. name=value를 전후 요청에 동일하게 사용.',
        [[sequence(CLIENT_SERVER, [
            message(1, 0, '응답 · Set-Cookie: name=value', 'Response · Set-Cookie: name=value', reply=True),
            message(0, 0, '브라우저에 값 저장', 'Store the value in the browser'),
            message(0, 1, '이후 요청 · Cookie: name=value', 'Later request · Cookie: name=value'),
        ], pair('조건에 맞는 요청에 브라우저가 자동 첨부', 'The browser attaches the cookie to eligible requests'))],
         [code(pair('응답 헤더 · 발췌', 'Response header · excerpt'), 'Set-Cookie: name=value'),
          code(pair('이후 요청 헤더 · 발췌', 'Later request header · excerpt'), 'Cookie: name=value')]],
        layout='visual', refs=[COOKIE_DOC]),
    'server-session': resource('I11 C13-object', [11,13],
        'I11의 잘린 라벨과 요청 순서를 편집 가능한 시퀀스로 복원. C13 객체는 userId만 유지. I13 저장 위치 그림은 대안으로 보류.',
        [[sequence(CLIENT_SERVER, [
            message(0, 1, '로그인 정보 전달', 'Submit login credentials'),
            message(1, 1, '검증 후 세션 생성\n임의 세션 ID → userId', 'Create session after verification\nRandom session ID → userId'),
            message(1, 0, 'Set-Cookie: session_id=<random-id>', reply=True),
            message(0, 1, 'Cookie: session_id=<random-id>'),
            message(1, 1, 'ID로 서버 세션 조회\n연결된 사용자 확인', 'Look up server session by ID\nIdentify the associated user'),
            message(1, 0, '요청 처리 결과', 'Request result', reply=True),
        ], pair('random-id는 예측 불가능한 식별자의 자리표시', 'random-id stands for an unpredictable identifier'))],
         [code(pair('서버에 보관한 세션 정보 · 예시', 'Session data held on the server · example'),
               '{\n  "userId": "u123"\n}', 'json', 40)]], layout='visual', refs=[SESSION_DOC]),
    'auth-token': resource('I14', [14],
        'JWT를 일반 토큰으로 바꾸고 서명 세부 제거. localStorage를 기본 저장 위치로 지정하지 않음.',
        [[token_sequence()]]),
    'jwt-structure': resource('I15 C15-header C15-payload', [15],
        '원본 구조 그림 보존. JSON의 role·iat·생략기호를 제거하고 sub·iss·aud·exp 예시로 수정. HS256은 예시 알고리즘으로 명시.',
        [[dict(kind='figure', src=SOURCE_DIR+'p15-i15.jpg',
               alt=pair('마침표로 구분된 JWT 헤더·페이로드·서명', 'JWT header, payload and signature separated by dots'),
               caption=pair('서명형 JWT의 세 부분 · aaaaa 등은 자리표시', 'Three parts of a signed JWT · aaaaa and similar strings are placeholders')),
          table([pair('필드', 'Claim'), pair('의미', 'Meaning')], [
              [pair('sub'), pair('사용자 식별자', 'Subject identifier')],
              [pair('iss'), pair('발급자', 'Issuer')],
              [pair('aud'), pair('수신 대상', 'Intended audience')],
              [pair('exp'), pair('만료 시각 · Unix 초', 'Expiration time · Unix seconds')],
          ])],
         [code(pair('Header · HS256을 선택한 예시', 'Header · an example using HS256'),
               '{\n  "alg": "HS256",\n  "typ": "JWT"\n}', 'json', 48),
          code(pair('Payload · 설명용 값', 'Payload · illustrative values'),
               '{\n  "sub": "u123",\n  "iss": "https://auth.example.com",\n  "aud": "foodmap-api",\n  "exp": 1800000000\n}', 'json', 48)]], layout='split', refs=[JWT_DOC]),
    'jwt-validation': resource('I14', [14,15],
        '2.4와 동일한 시퀀스에 JWT 검증을 구체화. 허용 알고리즘·신뢰 키·서명·iss·aud·exp를 확인.',
        [[token_sequence(True)],
         [table([pair('검증 대상', 'Check'), pair('수용 조건', 'Acceptance condition')], [
             [pair('서명', 'Signature'), pair('허용한 알고리즘·신뢰하는 키로 검증', 'Verify with an allowed algorithm and trusted key')],
             [pair('iss'), pair('신뢰하는 발급자와 일치', 'Matches the trusted issuer')],
             [pair('aud'), pair('이 API가 수신 대상', 'This API is the intended audience')],
             [pair('exp'), pair('만료 시각 이전', 'Before the expiration time')],
         ])]], layout='split', refs=[JWT_DOC, JWT_BCP]),
    'logout': resource('T16', [16,22],
        '원본 무효화 행을 종료 위치별 표로 재구성. 브라우저 삭제와 서버 철회 구분, 이미 발급된 JWT의 남은 효력 명시.',
        [[table([pair('종료 위치', 'Where to end access'), pair('처리', 'Action'), pair('효력', 'Effect')], [
            [pair('브라우저', 'Browser'), pair('보관한 쿠키·토큰 삭제', 'Remove stored cookies or tokens'), pair('다른 곳에 복사된 자격정보의 효력은 별도', 'Copies held elsewhere are a separate concern')],
            [pair('서버 세션', 'Server session'), pair('서버의 세션 기록 무효화', 'Invalidate the server session'), pair('해당 세션 ID의 조회 실패', 'That session ID no longer resolves')],
            [pair('리프레시 토큰', 'Refresh token'), pair('갱신 자격 철회', 'Revoke renewal credentials'), pair('새 액세스 토큰 발급 중단', 'Stop issuing new access tokens')],
            [pair('발급된 JWT', 'Issued JWT'), pair('만료 또는 추가 철회 검사', 'Expiration or an extra revocation check'), pair('서명·시간만 검사하면 만료까지 유효 가능', 'May remain valid until expiry with signature/time checks alone')],
        ])]]),
    'identity-provider': resource('I09-login T27-global T27-korea', [9,17,27],
        '원본 화면의 Google·Naver 선택 영역만 HTML로 재구성. 제공자 표는 익숙한 이름만 발췌. 인기·API 기능 설명 제외.',
        [[dict(kind='login-screen', social=True, caption=pair('외부 로그인 선택 화면 예시', 'Example external sign-in choices'))],
         [table([pair('인증을 맡는 서비스', 'Service handling authentication'), pair('사용하는 계정', 'Account used')], [
             [pair('Google'), pair('Google 계정', 'Google account')],
             [pair('Naver'), pair('네이버 계정', 'Naver account')],
             [pair('Kakao'), pair('카카오 계정', 'Kakao account')],
         ])]], layout='split'),
    'oauth-delegation': resource('I17', [17,18],
        '4개 참여자와 위임·외부 API 접근 관계만 남김. 코드·state·PKCE·ID 토큰 제거. 추상 흐름이며 실제 전송 경로는 3.4에서 제시.',
        [[sequence([pair('사용자', 'User'), pair('FoodMap 앱', 'FoodMap app'), PROVIDER, pair('외부 API', 'External API')], [
            message(0, 2, 'FoodMap에 허용할 범위 동의', 'Consent to the scope granted to FoodMap'),
            message(2, 1, '동의한 범위의 액세스 토큰 발급', 'Access token for approved scope', reply=True),
            message(1, 3, '액세스 토큰을 첨부한 요청', 'Request with the access token'),
            message(3, 3, '토큰·허용 범위 확인', 'Check token and scope'),
            message(3, 1, '허용된 데이터 반환', 'Return permitted data', reply=True),
        ], pair('참여자의 역할 관계 · scope는 사용자가 동의한 접근 범위',
                'Participant responsibilities · scope describes the access approved by the user'))]], refs=[OAUTH_DOC]),
    'authorization-code': resource('I18', [18],
        '브라우저 경유 복귀와 서버 간 코드 교환을 분리. state·PKCE의 세부는 후속 도식에서 확장. 제공자 검증 뒤 응답을 분리해 원본 화살표 교정.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 0, '외부 인증 주소로 이동 안내', 'Redirect to the external authorization URL', reply=True),
            message(0, 2, '등록한 복귀 주소를 포함한 요청', 'Request with the registered redirect URI'),
            message(2, 0, '인증·동의 후 복귀 안내 · code', 'After login and consent: redirect with code', reply=True),
            message(0, 1, '복귀 주소 요청 · code', 'Request to the redirect URI · code', focus=True),
            message(1, 2, '일회용 code의 교환 요청', 'Exchange the one-time code', focus=True),
            message(2, 1, '코드·클라이언트 조건 검증 후 토큰', 'Tokens after code and client checks', reply=True),
        ], OAUTH_CAPTION)]], refs=[OAUTH_DOC, OIDC_DOC]),
    'oauth-state': resource('I18', [18],
        '3.4와 같은 참여자·복귀 경로 유지. 무작위 state의 임시 보관·왕복·검사·불일치 거부 단계 추가. PKCE는 제외.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 1, '무작위 state 생성·보관', 'Generate and store random state', focus=True),
            message(1, 0, '외부 인증 주소 · state', 'Authorization URL · state', reply=True),
            message(0, 2, '인가 요청 · state', 'Authorization request · state', focus=True),
            message(2, 0, '인증·동의 후 복귀 · code + state', 'After login and consent · code + state', reply=True),
            message(0, 1, '복귀 주소 · code + state', 'Redirect URI · code + state', focus=True),
            message(1, 1, '시작한 요청의 state와 비교\n불일치 → 거부', 'Compare saved state\nMismatch → reject', focus=True),
            message(1, 2, '일치한 요청의 code 교환', 'Exchange code for the matching request'),
            message(2, 1, '검증 후 토큰 응답', 'Tokens after validation', reply=True),
        ], OAUTH_CAPTION)]], refs=[OAUTH_DOC, OIDC_DOC]),
    'pkce': resource('I18', [18],
        '동일 서버 교환 사례에 verifier/challenge의 바인딩 추가. 브라우저에는 verifier를 보내지 않음. 제공자 측 변환·비교를 표시하고 Base64url 보완.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 1, 'verifier 생성·서버 보관\nS256 변환 → challenge', 'Store secret verifier\nS256 → challenge', focus=True),
            message(1, 0, '외부 인증 주소 · state + challenge', 'Authorization URL · state + challenge', reply=True),
            message(0, 2, 'state · code_challenge · code_challenge_method=S256', focus=True),
            message(2, 0, '인증·동의 후 복귀 · code + state', 'After login and consent · code + state', reply=True),
            message(0, 1, '복귀값 전달 → 서버의 state 확인', 'Return response → server checks state'),
            message(1, 2, 'code + code_verifier', focus=True),
            message(2, 2, 'verifier 변환값과\n코드에 연결된 challenge 비교', 'Compare S256(verifier)\nwith code’s challenge', focus=True),
            message(2, 1, '일치·코드 검증 성공 시 토큰', 'Tokens only after matching and code validation', reply=True),
        ], pair('S256: ASCII(verifier) → SHA-256 → Base64url(패딩 제외) → challenge',
                'S256: ASCII(verifier) → SHA-256 → Base64url (no padding) → challenge'))]], refs=[PKCE_DOC, OAUTH_DOC]),
    'authorization': resource('I06', [6],
        '원본 영문 이미지 그대로 사용. 인가를 이미 배운 인증과 비교하는 위치에 배치.',
        [[dict(kind='figure', src=SOURCE_DIR+'p06-i06.jpg',
               alt=pair('왼쪽 인증은 신원 확인, 오른쪽 인가는 기능별 허용·거부', 'Authentication verifies identity; authorization allows or denies specific actions'),
               caption=pair('인증된 사용자에 대해 행동·대상별 허용 여부 판단', 'Evaluate actions and targets for an authenticated user'))]]),
    'cookie-protection': resource('C12 C13', [12,13,23],
        '2.2의 name=value를 유지하며 보호 속성 추가. 원본의 SameSite=Non 교정. 운영 환경 이름 분기·maxAge·하드코딩 키 제거. 각 헤더를 유효한 한 줄로 표시.',
        [[code(pair('응답 헤더 · HTTPS 서비스의 예시', 'Response header · HTTPS service example'),
               'Set-Cookie: name=value; Secure; HttpOnly; SameSite=Lax', width=80),
          table([pair('속성', 'Attribute'), pair('보호 범위', 'Protection')], [
              [pair('Secure'), pair('HTTPS 연결에서 쿠키 전송', 'Send the cookie over HTTPS')],
              [pair('HttpOnly'), pair('스크립트의 쿠키 읽기 제한', 'Prevent script access to the cookie')],
              [pair('SameSite=Lax'), pair('교차 사이트 첨부 제한 · 일부 최상위 탐색 허용', 'Restrict cross-site attachment; allow some top-level navigations')],
              [pair('SameSite=None'), pair('교차 사이트 사용이 필요한 경우 · Secure 필수', 'For cross-site use when needed · Secure required')],
          ])]], refs=[COOKIE_DOC, SESSION_DOC]),
    'environment-config': resource('C13', [13,21],
        'process.env.SESSION_SECRET 참조만 발췌. 하드코딩 대체값 제거. 누락 시 실패하는 설정 읽기 예제로 한정하고 실제 키 값은 포함하지 않음.',
        [[code(pair('서버 설정 읽기 · Node.js 발췌', 'Read server configuration · Node.js excerpt'),
               "const secret = process.env.SESSION_SECRET;\n\nif (!secret) {\n  throw new Error('SESSION_SECRET is required');\n}\n\nconst sessionConfig = { secret };", 'javascript', 56)],
         [table([pair('설정 요소', 'Configuration element'), pair('역할', 'Role')], [
             [pair('SESSION_SECRET'), pair('환경에서 주입하는 서버 설정 이름', 'Name of a server setting injected by the environment')],
             [pair('process.env'), pair('실행 중인 서버 환경의 설정 읽기', 'Read configuration from the server environment')],
             [pair('설정 누락', 'Missing setting'), pair('기본 비밀키로 대체하지 않고 시작 실패', 'Fail startup instead of using a default secret')],
         ])]], layout='split', refs=[SESSION_DOC]),
}
