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
OAUTH_SECURITY_DOC = 'https://www.rfc-editor.org/rfc/rfc9700.html'


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
SERVER = pair('서비스 서버', 'Application server')
PROVIDER = pair('외부 제공자', 'External provider')
CLIENT_SERVER = [BROWSER, SERVER]
OAUTH_ACTORS = [BROWSER, pair('FoodMap 서버', 'FoodMap server'), PROVIDER]
OAUTH_CAPTION = pair('서버가 코드를 교환하는 사례 · ID 토큰은 OIDC 사용 시 반환',
                     'Server-side code exchange · An ID token is returned when using OIDC')


def token_sequence(jwt=False):
    """Separate token transport from the server's JWT acceptance decision."""
    if jwt:
        return sequence(CLIENT_SERVER, [
            message(0, 1, '맛집 생성 요청\nAuthorization: Bearer <JWT>', 'Create a restaurant\nAuthorization: Bearer <JWT>'),
            message(1, 1, 'sub=u123 읽기\n아직 신뢰하지 않음', 'Read sub=u123\nNot yet trusted'),
            message(1, 1, '서명·iss·aud·exp 검증', 'Verify signature, iss, aud, exp', focus=True),
            message(1, 1, '모두 통과 → u123로 인정\n실패 → 인증 거부', 'All checks pass → authenticate as u123\nAny check fails → reject authentication', focus=True),
        ], pair('JWT 검증 성공은 사용자 확인 · 맛집 생성 권한은 별도 판단',
                'JWT validation authenticates the user; permission to create a restaurant is checked separately'))
    return sequence(CLIENT_SERVER, [
        message(0, 1, '로그인 정보 전달', 'Submit login credentials'),
        message(1, 0, 'u123 인증 성공 후 토큰 발급', 'Issue a token after verifying u123', reply=True),
        message(0, 1, '맛집 생성 요청\nAuthorization: Bearer <token>', 'Create a restaurant\nAuthorization: Bearer <token>'),
        message(1, 1, '토큰 검증\n현재 요청의 사용자 u123 확인', 'Verify the token\nIdentify u123 for this request'),
    ], pair('Authorization: 토큰 등 인증 자격을 전달하는 HTTP 요청 헤더',
            'Authorization: an HTTP request header carrying authentication credentials'))


RESOURCES = {
    'authentication': resource('I09-login', [9],
        '원본 로그인 입력 화면을 유지하고 계정 지정·서버 검증·성공/실패 흐름을 함께 배치. 04번 minsu@example.com·u123 계정 재사용. 입력 역할은 본문과 흐름에 대응. 해시·솔트·세션·권한 판단 제외.',
        [[dict(kind='resource-flow', items=[
            dict(title=pair('계정 지정', 'Identify the account'),
                 body=pair('이메일 minsu@example.com\n서버가 확인할 계정: u123', 'Email: minsu@example.com\nAccount to authenticate: u123')),
            dict(title=pair('서버의 증거 검증', 'Verify the credentials'),
                 body=pair('입력한 비밀번호가\nu123 계정의 증거로 유효한지 검증', 'Verify the submitted password\nagainst account u123’s stored credentials')),
            dict(title=pair('인증 성공·실패 판단', 'Return the authentication result'),
                 body=pair('성공 → 현재 요청의 사용자 u123로 인정\n실패 → u123 사용자로 인정하지 않음', 'Success → authenticate this request as u123\nFailure → reject authentication')),
        ], caption=pair('현재 인증 요청의 사용자 확인 · 로그인 상태 유지와 작업 권한 판단은 별도',
                        'Authentication applies to this request; session management and authorization are separate'))],
         [dict(kind='login-screen', email='minsu@example.com',
               caption=pair('이메일로 계정 지정 · 비밀번호로 증거 제출',
                            'The email identifies the account; the password is the credential'))]], layout='split'),
    'password-login': resource('I09-flow', [9],
        '원본 입력→신원 확인 흐름을 로그인 입력·계정/저장 정보 조회·검증 함수·판단의 4단계로 재구성. minsu@example.com·u123·salt-A·hash-A 재사용. 상태 유지·권한 판단 제외.',
        [[dict(kind='resource-flow', items=[
            dict(title=pair('로그인 정보 입력', 'Enter credentials'),
                 body=pair('minsu@example.com · 입력 비밀번호\n브라우저 → 서버', 'minsu@example.com and entered password\nBrowser → server')),
            dict(title=pair('계정과 저장 정보 조회', 'Look up the account and stored data'),
                 body=pair('이메일로 찾은 계정: u123\n저장 정보: salt-A · hash-A', 'Account found by email: u123\nStored data: salt-A and hash-A')),
            dict(title=pair('검증 함수 실행', 'Run password verification'),
                 body=pair('입력 비밀번호와\nu123의 salt-A·hash-A 전달', 'Supply the entered password\nand u123’s salt-A and hash-A')),
            dict(title=pair('현재 요청의 사용자 판단', 'Identify the user for this request'),
                 body=pair('검증 성공 → 조회한 계정의 ID u123\n계정 없음·검증 실패 → 인증 거부', 'Success → account ID u123\nNo account or failed verification → reject login')),
        ], caption=pair('확인 범위는 현재 로그인 요청 · 이후 요청의 로그인 유지는 별도',
                        'This login request establishes identity; maintaining authentication across requests is separate'))]]),
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
        'I11의 요청 순서를 편집 가능한 시퀀스로 복원. sid-A를 생성·쿠키 전달·조회·서버 저장 예시에 통일. JSON은 세션 ID와 상태 정보의 대응을 보여주는 개념 모델이며 실제 ID 생성값이나 저장소 구현이 아님.',
        [[sequence(CLIENT_SERVER, [
            message(0, 1, '로그인 정보 전달', 'Submit login credentials'),
            message(1, 1, '검증 후 세션 생성\nsid-A에 userId=u123 저장', 'Create session after verification\nStore userId=u123 under sid-A'),
            message(1, 0, 'Set-Cookie: session_id=sid-A', reply=True),
            message(0, 1, 'Cookie: session_id=sid-A'),
            message(1, 1, 'sid-A의 유효한 기록 조회\nuserId=u123 확인', 'Look up valid record for sid-A\nRead userId=u123'),
            message(1, 0, '요청 처리 결과', 'Response', reply=True),
        ], pair('브라우저는 세션 ID 전달 · 서버는 연결된 상태 정보 조회', 'Browser sends the session ID · server looks up the linked state'))],
         [code(pair('서버의 세션 저장 예시 · 세션 ID → 상태 정보', 'Example session store · session ID → state'),
               '{ "sid-A": { "userId": "u123" } }', 'json', 48)]], layout='visual', refs=[SESSION_DOC]),
    'auth-token': resource('I14', [14],
        'JWT를 일반 토큰으로 바꾸고 서명 세부 제거. u123 인증 후 발급·요청 첨부·사용자 재확인 성공 흐름. localStorage를 기본 저장 위치로 지정하지 않음.',
        [[token_sequence()]]),
    'jwt-structure': resource('I15 C15-header C15-payload', [15],
        '원본 구조 그림 보존. JSON의 role·iat·생략기호를 제거하고 sub·iss·aud·exp 예시로 수정. HS256은 예시 알고리즘으로 명시.',
        [[dict(kind='figure', src=SOURCE_DIR+'p15-i15.jpg',
               alt=pair('마침표로 구분된 JWT 헤더·페이로드·서명', 'JWT header, payload and signature separated by dots'),
               caption=pair('서명형 JWT · 인코딩은 암호화가 아니므로 비밀정보 제외', 'Signed JWT · encoding is not encryption; exclude secrets')),
          table([pair('필드', 'Claim'), pair('의미', 'Meaning')], [
              [pair('sub'), pair('사용자 식별자', 'Subject identifier')],
              [pair('iss'), pair('발급자', 'Issuer')],
              [pair('aud'), pair('수신 대상', 'Intended audience')],
              [pair('exp'), pair('만료 시각 · Unix 초', 'Expiration time · Unix seconds')],
          ])],
         [code(pair('Header를 풀어 읽은 JSON · HS256 예시', 'Decoded header JSON · HS256 example'),
               '{\n  "alg": "HS256",\n  "typ": "JWT"\n}', 'json', 48),
          code(pair('Payload를 풀어 읽은 JSON · API 액세스 토큰 예시', 'Decoded payload JSON · API access token example'),
               '{\n  "sub": "u123",\n  "iss": "https://auth.example.com",\n  "aud": "foodmap-api",\n  "exp": 1800000000\n}', 'json', 48)]], layout='split', refs=[JWT_DOC]),
    'jwt-validation': resource('I14', [14,15],
        '2.4의 발급 과정을 반복하지 않고 JWT 수신·읽기·검증·판단에 집중. 2.6의 sub=u123·iss·aud 값을 이어받아 허용 알고리즘·신뢰 키·서명·iss·aud·exp를 확인.',
        [[token_sequence(True)],
         [table([pair('검증 대상', 'Check'), pair('수용 조건', 'Acceptance condition')], [
             [pair('서명', 'Signature'), pair('내용 변조 확인 · 허용한 알고리즘·신뢰하는 키 사용', 'Check integrity · allowed algorithm and trusted key')],
             [pair('iss · 발급자', 'iss · issuer'), pair('신뢰하는 발급자인지 확인\nhttps://auth.example.com', 'Match the trusted issuer\nhttps://auth.example.com')],
             [pair('aud · 수신 대상', 'aud · audience'), pair('이 API용인지 확인 · foodmap-api', 'Match this API · foodmap-api')],
             [pair('exp · 만료', 'exp · expiration'), pair('현재 시각이 만료 시각 이전인지 확인', 'Check that the token has not expired')],
         ])]], layout='split', refs=[JWT_DOC, JWT_BCP]),
    'logout': resource('T16', [16,22],
        '원본 무효화 행을 처리 대상별 표로 재구성. sid-A 무효화와 갱신 자격 철회·기존 액세스 토큰 B의 남은 효력을 구분. B가 JWT인 경우를 명시해 19번의 일반 액세스 토큰 예시와 연결.',
        [[table([pair('처리 대상', 'Target'), pair('처리', 'Action'), pair('효력', 'Effect')], [
            [pair('브라우저', 'Browser'), pair('보관한 쿠키·토큰 삭제', 'Remove stored cookies or tokens'), pair('다른 곳에 복사된 자격정보의 효력은 별도', 'Copies elsewhere may remain valid')],
            [pair('세션 sid-A', 'Session sid-A'), pair('서버의 세션 기록 무효화', 'Invalidate the server session'), pair('sid-A로 다시 요청해도 인증 거부', 'Reject requests that use sid-A')],
            [pair('리프레시 토큰', 'Refresh token'), pair('갱신 자격 철회', 'Revoke the refresh token'), pair('새 액세스 토큰 발급 중단', 'Stop issuing new access tokens')],
            [pair('액세스 토큰 B · JWT인 경우', 'Access token B · if a JWT'), pair('만료 검사 · 즉시 차단 시 철회 여부도 검사', 'Check expiration and, for immediate rejection, revocation'), pair('갱신 차단만으로는 B가 만료까지 유효할 수 있음', 'Token B may remain valid until it expires after refresh is revoked')],
        ])]]),
    'identity-provider': resource('I09-login T27-global T27-korea', [9,17,27],
        '원본 화면의 Google·Naver 선택 영역을 유지. 제공자·계정 이름 표를 Google 인증 → 결과 전달 → FoodMap 검증의 개념 흐름으로 대체. 실제 전송 경로·토큰·내부 계정 연결은 후속 장에 남김.',
        [[dict(kind='login-screen', social=True, caption=pair('FoodMap에서 외부 계정으로 인증을 시작하는 화면', 'Start authentication with an external account from FoodMap'))],
         [dict(kind='resource-flow', items=[
             dict(title=pair('Google에서 계정 인증', 'Authenticate at Google'),
                  body=pair('사용자가 Google 계정으로 인증', 'The user authenticates with a Google account')),
             dict(title=pair('Google이 인증 결과 전달', 'Google conveys the result'),
                  body=pair('FoodMap에 사용자 인증 결과 전달', 'Google conveys the authentication result to FoodMap')),
             dict(title=pair('FoodMap이 결과 검증', 'FoodMap verifies the result'),
                  body=pair('전달받은 결과를 검증해 사용자 확인', 'FoodMap verifies the result to identify the user')),
         ], caption=pair('Google로 로그인을 선택한 뒤의 역할 흐름', 'Responsibilities after choosing Sign in with Google'))]], layout='split'),
    'oauth-delegation': resource('I17', [17,18],
        '기존 외부 프로필 사례와 4개 참여자·연결 유지. 자원 소유자·클라이언트·인가 서버·자원 서버 역할 병기. 프로필 읽기 허용·토큰 발급·제출·검증의 관계 명확화. 인가 서버와 자원 서버는 역할 구분이며 다른 운영 주체나 물리 서버를 뜻하지 않음. 인가 코드 등 실제 전송 경로는 3.4에 남김.',
        [[sequence([pair('사용자\n자원 소유자', 'User\nResource owner'), pair('FoodMap 앱\n클라이언트', 'FoodMap app\nClient'), pair('외부 제공자\n인가 서버', 'External provider\nAuthorization server'), pair('외부 프로필 API\n자원 서버', 'External profile API\nResource server')], [
            message(0, 2, 'FoodMap의 내 외부 프로필 읽기 허용', 'Allow FoodMap to read my external profile'),
            message(2, 1, '프로필 읽기 토큰 발급', 'Issue profile-read token', reply=True),
            message(1, 3, '프로필 조회 요청 + 액세스 토큰', 'Profile request + access token'),
            message(3, 3, '토큰 유효성·프로필 읽기 허용 검사', 'Validate token and profile-read permission'),
            message(3, 1, '허용된 프로필 정보 반환', 'Return permitted profile data', reply=True),
        ], pair('외부 API 접근 위임의 개념 흐름 · 사용자 인증 결과 검증과 구분',
                'Conceptual flow of delegated API access · Distinct from verifying user identity'))]], refs=[OAUTH_DOC]),
    'authorization-code': resource('I18', [18],
        '사용자 후속 요청에 따라 표를 시퀀스 도식으로 교체. 브라우저·FoodMap 서버·외부 제공자 세로선을 유지하며 브라우저 이동과 서버 간 통신을 두 구간으로 구분. 로그인·접근 허용, 코드 복귀, 서버 교환과 응답을 방향 화살표로 표시. 공용 HTML 도식 사용으로 한영·인쇄·모바일 대응 유지.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 0, '외부 로그인 화면으로 이동 안내', 'Redirect to the external login page', reply=True,
                    phase=pair('① 브라우저를 통한 이동', '1. Browser navigation')),
            message(0, 2, '외부 인증 화면에서 로그인·접근 허용', 'Log in and approve access on the provider’s page'),
            message(2, 0, '인가 코드 발급 · 복귀 주소로 이동 안내', 'Issue code · Redirect to the callback URL', reply=True),
            message(0, 1, '복귀 주소로 인가 코드 전달', 'Carry the code to FoodMap’s callback URL', focus=True),
            message(1, 2, '토큰 발급 API에 코드 제출', 'Submit code to the token API', focus=True,
                    phase=pair('② 서버 간 통신', '2. Server-to-server communication')),
            message(2, 1, '교환 조건 확인 후 토큰 반환', 'Check exchange conditions and return tokens', reply=True),
        ], pair('액세스 토큰 반환 · OIDC 사용 시 ID 토큰도 반환',
                'Returns an access token · With OIDC, also an ID token'))]], refs=[OAUTH_DOC, OIDC_DOC]),
    'oauth-state': resource('I18', [18],
        '3.4와 같은 참여자·복귀 경로 유지. 무작위 state-A를 해당 브라우저의 시도에 연결해 보관, 복귀값 대조, 누락·불일치 거부를 표시. PKCE는 제외.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 1, '이 브라우저의 시도\nstate-A 생성·보관', 'Bind state-A to this\nbrowser’s login attempt', focus=True),
            message(1, 0, '외부 인증 주소 · state-A', 'Authorization URL · state-A', reply=True),
            message(0, 2, '인가 요청 · state-A', 'Authorization request · state-A', focus=True),
            message(2, 0, '인증·동의 후 복귀 · code + state', 'After login and consent · code + state', reply=True),
            message(0, 1, '복귀 주소 · code + state', 'Redirect URI · code + state', focus=True),
            message(1, 1, 'state-A와 대조\n누락·불일치 → 거부', 'Compare with state-A\nMissing or mismatch → reject', focus=True),
            message(1, 2, '일치한 요청의 code 교환', 'Exchange code for the matching request'),
            message(2, 1, '검증 후 토큰 응답', 'Tokens after validation', reply=True),
        ], OAUTH_CAPTION)]], refs=[OAUTH_DOC, OIDC_DOC, OAUTH_SECURITY_DOC]),
    'pkce': resource('I18', [18],
        '동일 서버 교환 사례에 verifier/challenge의 바인딩 추가. 브라우저에는 verifier를 보내지 않음. 제공자 측 변환·비교와 불일치 시 교환 거부를 표시. S256 계산식 유지.',
        [[sequence(OAUTH_ACTORS, [
            message(1, 1, 'verifier 생성·서버 보관\nS256 변환 → challenge', 'Store secret verifier\nS256 → challenge', focus=True),
            message(1, 0, '외부 인증 주소 · state + challenge', 'Authorization URL · state + challenge', reply=True),
            message(0, 2, 'state · code_challenge · code_challenge_method=S256', focus=True),
            message(2, 0, '인증·동의 후 복귀 · code + state', 'After login and consent · code + state', reply=True),
            message(0, 1, '복귀값 전달 → 서버의 state 확인', 'Return response → server checks state'),
            message(1, 2, 'code + code_verifier', focus=True),
            message(2, 2, 'verifier 변환값과\n코드에 연결된 challenge 비교', 'Compare S256(verifier)\nwith code’s challenge', focus=True),
            message(2, 1, '검증 성공 → 토큰 · 불일치 → 거부', 'Valid → tokens · mismatch → reject', reply=True),
        ], pair('S256: ASCII(verifier) → SHA-256 → Base64url(패딩 제외) → challenge',
                'S256: ASCII(verifier) → SHA-256 → Base64url (no padding) → challenge'))]], refs=[PKCE_DOC, OAUTH_DOC, OAUTH_SECURITY_DOC]),
    'authorization': resource('I06', [6],
        '원본 영문 이미지 보존. 인증·인가 비교를 u123의 맛집 생성 요청으로 연결하되 역할 규칙은 다음 장에서 설명.',
        [[dict(kind='figure', src=SOURCE_DIR+'p06-i06.jpg',
               alt=pair('왼쪽 인증은 신원 확인, 오른쪽 인가는 기능별 허용·거부', 'Authentication verifies identity; authorization allows or denies specific actions'),
               caption=pair('u123임을 확인한 뒤에도 맛집 생성의 허용 여부는 별도 판단', 'Identifying u123 does not yet decide permission to create a place'))]]),
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

# Active, implementation-aligned Chapter 3. Earlier definitions are historical.
from chapter03_content import MEDIA as CHAPTER3_MEDIA
RESOURCES.pop('oauth-state')
RESOURCES.pop('pkce')
RESOURCES['identity-provider']['columns'] = CHAPTER3_MEDIA['identity-provider']
RESOURCES['oauth-delegation']['columns'] = CHAPTER3_MEDIA['oauth-delegation']
RESOURCES['authorization-code']['columns'] = CHAPTER3_MEDIA['authorization-code']

# Active beginner-facing Chapter 4.
from chapter04_content import MEDIA as CHAPTER4_MEDIA
RESOURCES['authorization']['columns'] = CHAPTER4_MEDIA['authorization']

# Web attacks and defenses are deferred to next week's lecture.
from curriculum_scope import DEFERRED_SECURITY_IDS
for ident in DEFERRED_SECURITY_IDS:
    RESOURCES.pop(ident, None)

# Replace the historical SESSION_SECRET example with actual Week 8 settings.
RESOURCES.pop('environment-config')
