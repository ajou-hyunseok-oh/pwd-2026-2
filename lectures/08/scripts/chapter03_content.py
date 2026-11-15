"""Beginner-facing Chapter 3, aligned with the Week 8 repositories.

Detailed protocol material remains in the historical research records.
This module is the active contract for the five classroom slides.
"""


def P(ko, en):
    return (ko, en)


def concept(ident, title, lead, requires, example):
    return dict(id=ident, title=title, lead=lead, requires=requires.split(), example=example)


CHAPTER = dict(number=3,
    connection='외부 로그인에서 자주 쓰는 용어를 익히고 실제 Supabase Auth·SDK·Express 구현 흐름으로 연결.',
    scope='제공자와 인증 서비스 → OAuth·OIDC → 로그인과 복귀 → 인증 계정·프로필 → API 사용자 확인. state·PKCE 내부 계산·클레임 검증·수동 계정 병합은 본문에서 제외.',
    concepts=[
        concept('identity-provider', P('외부 인증 제공자', 'External Identity Providers'),
                P('외부 계정 인증과 FoodMap의 로그인 연결 역할', 'External account authentication and FoodMap login integration'),
                'authentication password-login', 'Google·네이버 선택 화면과 외부 제공자·Supabase Auth·브라우저 SDK의 역할 비교'),
        concept('oauth-delegation', P('OAuth와 OIDC의 역할', 'The Roles of OAuth and OIDC'),
                P('접근 권한 위임과 사용자 인증 결과 전달의 구분', 'Delegated access and user authentication results'),
                'identity-provider auth-token', '외부 액세스 토큰·ID 토큰의 목적 비교와 Supabase Auth의 처리 책임'),
        concept('authorization-code', P('소셜 로그인의 전체 흐름', 'The Social Login Flow'),
                P('로그인 선택부터 복귀와 SDK의 로그인 결과 처리까지', 'From choosing a provider to returning and processing the login result'),
                'oauth-delegation prior-web', 'signInWithOAuth → 외부 인증 → /auth/callback → exchangeCodeForSession'),
        concept('account-link', P('인증 계정과 FoodMap 사용자 정보', 'Authentication Accounts and FoodMap Profiles'),
                P('같은 사용자 ID로 인증 계정과 서비스 데이터를 연결', 'Linking authentication records and application data using the same user ID'),
                'authorization-code user-account prior-data', 'auth.users.id와 profiles.id의 같은 UUID, submissions.submitter_id의 연결'),
        concept('social-session', P('로그인 이후의 API 요청', 'API Requests After Login'),
                P('브라우저의 토큰 첨부와 Express 서버의 사용자 확인', 'The browser sends an access token; Express authenticates the request'),
                'account-link auth-token jwt-validation', 'getSession → Bearer 토큰 → getUser → 같은 ID의 profiles 조회 → 현재 사용자 반환'),
    ])


def G(term, *details):
    return dict(term=term, details=list(details))


def B(layout, *groups):
    return dict(layout=layout, explanation=dict(kind='concepts', items=list(groups)))


BODY = {
    'identity-provider': B('side',
        G(P('외부 인증 제공자 - 외부 계정의 사용자를 확인하는 서비스', 'Identity provider - a service that authenticates users of an external account'),
          P('Google·네이버가 자신의 서비스에서 사용자 로그인 처리', 'Google or Naver handles login to its own service'),
          P('FoodMap은 외부 계정의 비밀번호를 받아 저장하지 않음', 'FoodMap does not receive or store the external password')),
        G(P('외부 로그인 연결 - Supabase Auth와 브라우저 SDK의 협력', 'External login integration - Supabase Auth and the browser SDK'),
          P('Supabase Auth는 인증 서비스 · 외부 인증 결과를 확인해 FoodMap용 로그인 자격 발급', 'Supabase Auth is the auth service; it checks external results and issues FoodMap login credentials'),
          P('SDK는 인증 요청용 라이브러리 · 브라우저에서 로그인 시작과 복귀 결과 처리', 'The SDK is an authentication library that starts login and handles the callback in the browser'))),
    'oauth-delegation': B('wide',
        G(P('OAuth 2.0 - 다른 서비스의 자원 접근을 허용하는 체계', 'OAuth 2.0 - an authorization framework for delegated resource access'),
          P('사용자가 허용한 범위에서 다른 서비스의 API 호출', 'Call another service’s API within the permitted scope'),
          P('액세스 토큰은 해당 API에 접근할 때 제시하는 자격', 'An access token is a credential presented to that API')),
        G(P('OIDC(OpenID Connect) - OAuth 2.0 기반 사용자 인증 표준', 'OIDC (OpenID Connect) - an authentication layer built on OAuth 2.0'),
          P('외부 제공자가 수행한 사용자 인증 결과의 전달·검증 규칙', 'Rules for conveying and verifying the provider’s authentication result'),
          P('ID 토큰은 인증 결과를 받는 서비스의 사용자 확인에 사용', 'The receiving service uses an ID token to identify the authenticated user'))),
    'authorization-code': B('wide',
        G(P('콜백(callback) - 외부 인증 후 돌아오는 처리 주소', 'Callback URL - where the browser returns after external authentication'),
          P('실습의 /auth/callback 페이지에서 SDK로 복귀 결과 처리', 'The /auth/callback page processes the result with the SDK')),
        G(P('인가 코드와 SDK 세션 - 복귀값과 로그인 결과', 'Authorization code and SDK session - an exchange code and an authenticated session'),
          P('인가 코드는 토큰 교환용 일회용 값 · SDK 세션은 토큰·사용자 정보 묶음', 'An authorization code is exchanged once for tokens; the SDK session object contains tokens and user data'))),
    'account-link': B('wide',
        G(P('인증 계정과 프로필 - 로그인 정보와 서비스 정보의 구분', 'Authentication account and profile - authentication data and application data'),
          P('auth.users는 Supabase가 관리하는 인증 계정', 'auth.users contains authentication accounts managed by Supabase'),
          P('profiles는 FoodMap의 이름·역할·활성 상태를 저장하는 테이블', 'profiles stores the FoodMap name, role and active status')),
        G(P('UUID - 사용자를 구분하는 고유 ID', 'UUID - a unique ID identifying a user'),
          P('인증 계정과 프로필은 같은 UUID로 연결 · 제보도 이 ID를 참조', 'The auth account and profile share a UUID; submissions reference that ID'),
          P('이름·이메일이 아닌 검증된 사용자 ID로 데이터 조회', 'Look up data with the verified user ID rather than a name or email'))),
    'social-session': B('wide',
        G(P('Bearer 토큰 - API 요청에 첨부하는 로그인 자격', 'Bearer token - an access credential included in an API request'),
          P('브라우저는 Supabase 액세스 토큰을 Authorization 헤더에 첨부 · 외부 제공자 토큰과 구분', 'The browser sends the Supabase access token in the Authorization header, not a provider token'),
          P('Express 서버는 Supabase Auth로 토큰을 검증한 뒤 사용자 ID 확인', 'Express verifies the token with Supabase Auth to identify the user'))),
}


def table(head, rows):
    return dict(kind='table', head=head, rows=rows)


def M(start, end, ko, en, **options):
    return dict({'from': start, 'to': end, 'text': P(ko, en)}, **options)


def Q(actors, rows, caption):
    return dict(kind='resource-sequence', actors=actors, rows=rows, caption=caption)


MEDIA = {
    'identity-provider': [[
        dict(kind='login-screen', social=True, caption=P('FoodMap의 외부 로그인 선택 화면', 'Choosing a social login provider in FoodMap')),
        table([P('구성 요소', 'Component'), P('담당', 'Responsibility')], [
            [P('Google·네이버', 'Google / Naver'), P('외부 계정 인증', 'External account authentication')],
            [P('Supabase Auth', 'Supabase Auth'), P('외부 로그인 연결·서비스용 토큰 발급', 'Integrate social login and issue application access tokens')],
            [P('브라우저 SDK', 'Browser SDK'), P('인증 요청·로그인 결과 보관', 'Authentication requests and session persistence')],
        ])]],
    'oauth-delegation': [[table([P('발급자와 토큰', 'Issuer and token'), P('목적', 'Purpose'), P('이 프로젝트에서의 처리', 'Used in this project')], [
        [P('외부 제공자 · 액세스 토큰', 'Provider · Access token'), P('외부 API의 데이터 접근', 'Access the provider’s API'), P('Supabase Auth가 외부 로그인 연결 과정에서 처리', 'Handled by Supabase Auth during external login')],
        [P('외부 제공자 · ID 토큰(OIDC)', 'Provider · ID token (OIDC)'), P('외부 제공자가 인증한 사용자 확인', 'Identify the user authenticated by the provider'), P('Supabase Auth가 인증 결과 검증', 'Supabase Auth verifies the authentication result')],
        [P('Supabase · 액세스 토큰', 'Supabase · Access token'), P('FoodMap API 요청의 사용자 확인', 'Identify the user making a FoodMap API request'), P('브라우저가 Express 요청에 첨부', 'The browser attaches it to requests to Express')],
    ])]],
    'authorization-code': [[Q([P('브라우저·SDK', 'Browser / SDK'), P('Supabase Auth', 'Supabase Auth'), P('외부 제공자', 'External provider')], [
        M(0, 1, '로그인 선택 · signInWithOAuth', 'Choose login · signInWithOAuth'),
        M(1, 0, '외부 제공자의 로그인 화면으로 이동 안내', 'Redirect to the provider’s login page', reply=True),
        M(0, 2, '외부 계정 로그인·접근 허용', 'Log in and approve access'),
        M(2, 1, '브라우저를 거쳐 외부 인증 결과 복귀', 'The provider redirects the browser back to Supabase Auth', reply=True),
        M(1, 0, '/auth/callback으로 이동 · 인가 코드', 'Redirect to /auth/callback with a code', reply=True),
        M(0, 1, 'SDK: exchangeCodeForSession(코드)', 'SDK: exchangeCodeForSession(code)', focus=True),
        M(1, 0, 'Supabase 액세스 토큰·사용자 정보 반환', 'Return a Supabase access token and user data', reply=True),
    ], P('외부 인증 뒤 Supabase Auth가 FoodMap용 로그인 결과 제공', 'Supabase Auth establishes the FoodMap session after external authentication'))]],
    'account-link': [[table([P('저장 위치', 'Storage'), P('저장 정보', 'Stored data'), P('연결 기준', 'Link')], [
        [P('auth.users', 'auth.users'), P('인증 계정', 'Authentication account'), P('id: 사용자 UUID', 'id: user UUID')],
        [P('public.profiles', 'public.profiles'), P('이름·역할·활성 상태', 'Name, role and active status'), P('id: 인증 계정과 같은 UUID', 'id: the same UUID as the auth account')],
        [P('public.submissions', 'public.submissions'), P('사용자가 작성한 제보', 'Submissions submitted by the user'), P('submitter_id: 프로필의 사용자 ID', 'submitter_id: the profile’s user ID')],
    ])]],
    'social-session': [[Q([P('브라우저·SDK', 'Browser / SDK'), P('FoodMap 서버', 'FoodMap server'), P('Supabase Auth', 'Supabase Auth'), P('프로필 DB', 'Profiles table')], [
        M(0, 1, 'GET /api/auth/me\nAuthorization: Bearer <supabase_access_token>', 'GET /api/auth/me\nAuthorization: Bearer <supabase_access_token>', focus=True),
        M(1, 2, 'getUser(토큰)으로 검증 요청', 'Verify with getUser(token)'),
        M(2, 1, '검증된 사용자 ID 반환', 'Return the verified user ID', reply=True),
        M(1, 3, '같은 ID로 profiles 조회', 'Look up profiles with that ID'),
        M(3, 1, '이름·역할·활성 상태 반환', 'Return name, role and active status', reply=True),
        M(1, 0, '활성 사용자 정보 반환', 'Return the active user’s profile', reply=True),
    ], P('토큰 검증 실패·비활성 계정은 거부 · 작업별 권한 판단은 별도', 'Reject invalid tokens or inactive accounts · Operation permissions are checked separately'))]],
}

PARAGRAPHS = {
    'identity-provider': '챕터 1~2는 수정하지 않고 이 장의 앞부분에서 인증 서비스·SDK의 뜻을 짧게 확인한 뒤 외부 제공자 연결의 역할로 설명을 제한한다. 외부 인증 제공자는 외부 계정의 사용자를 인증하는 서비스다. FoodMap에서 Google·네이버를 선택하면 해당 제공자가 자신의 계정으로 사용자를 인증한다. FoodMap은 외부 비밀번호를 받아 저장하지 않는다. Supabase Auth는 외부 인증 결과를 처리해 서비스용 로그인 자격을 발급하고 브라우저 SDK는 인증 요청·토큰 보관·갱신을 연결하는 라이브러리다. 기존 로그인 선택 화면을 유지하고 세 구성 요소의 책임을 비교한다. 실제 구현 근거는 클라이언트 authApi.js·config/supabase.js이며 실제 로그인 시연 결과로 표시하지 않는다.',
    'oauth-delegation': '외부 제공자가 발급한 액세스 토큰·ID 토큰과 Supabase가 FoodMap API용으로 발급한 액세스 토큰을 표의 별도 행으로 구분한다. OAuth 2.0은 다른 서비스의 자원 접근을 허용하는 인가 프레임워크이고 OIDC는 OpenID Connect의 약칭으로 OAuth 2.0에 사용자 인증 결과 전달·검증 규칙을 더한 표준이다. 외부 액세스 토큰은 외부 API 접근, ID 토큰은 수신 서비스의 사용자 확인에 쓰인다. 실습에서 외부 제공자의 토큰 처리는 Supabase Auth가 맡으며 FoodMap Express API에는 Supabase Auth가 발급한 서비스용 액세스 토큰을 보낸다. 모든 외부 로그인이 동일한 OIDC 절차라고 일반화하지 않는다. scope·클레임·수동 서명 검증은 제외하고 두 용어의 목적과 실제 담당만 설명한다.',
    'authorization-code': '콜백은 외부 인증 뒤 돌아오는 처리 주소이며 실습은 /auth/callback 페이지에서 SDK로 결과를 처리한다. 인가 코드는 토큰 교환용 일회용 값이고 SDK 세션은 토큰·사용자 정보를 묶은 객체로 서버 세션 ID와 다르다. 로그인 선택은 signInWithOAuth로 Supabase Auth에 전달되고 외부 제공자의 인증을 거친 브라우저가 Auth로 돌아온다. Auth는 FoodMap 콜백으로 코드를 전달하고 브라우저 SDK의 exchangeCodeForSession이 Auth와 교환해 서비스용 토큰·사용자 정보를 받는다. 외부 제공자와 Auth 사이의 교환과 Auth와 브라우저 사이의 교환을 FoodMap Express 서버의 직접 외부 코드 교환으로 설명하지 않는다. state·PKCE 내부 계산은 본문에서 제외하되 실제 SDK 설정이 PKCE임을 보충 기록에 남긴다. 근거: authApi.js, config/supabase.js, utils/oauthCallback.js.',
    'account-link': 'auth.users는 Supabase가 관리하는 인증 계정이고 public.profiles는 FoodMap의 이름·역할·활성 상태 테이블이다. UUID는 사용자를 구분하는 고유 ID이며 profiles.id는 auth.users.id와 같은 UUID를 사용한다. 제보의 submitter_id는 프로필 ID를 참조하므로 이름·이메일 대신 검증된 사용자 ID로 사용자와 서비스 데이터를 연결한다. 기존 u123·provider-A/42의 수동 외부 계정 매핑 예시는 실습 스키마의 실제 연결로 교체하며 임의 숫자 ID를 넣지 않는다. 근거: 서버 supabase/schema.sql의 외래 키와 계정 생성 시 프로필 생성 트리거.',
    'social-session': 'Express에 첨부하는 값은 Supabase 액세스 토큰이며 외부 제공자의 액세스 토큰·ID 토큰과 구분한다. Bearer는 API 요청에 토큰을 제시하는 방식이다. 브라우저의 api.jsx는 SDK의 getSession으로 액세스 토큰을 읽어 Authorization 헤더에 첨부한다. GET /api/auth/me에서 Express는 Supabase Auth의 getUser로 토큰을 검증하고 반환된 사용자 ID로 profiles를 조회한다. 프로필이 없거나 비활성 계정이면 거부하고 성공하면 현재 사용자 정보를 반환한다. SDK 저장값 읽기와 서버의 사용자 검증은 구분하며 외부 제공자의 토큰을 FoodMap API에 보내는 것으로 설명하지 않는다. 작업별 관리자 권한은 다음 챕터에 남긴다. 근거: 클라이언트 api.jsx·authApi.js와 서버 middleware/auth.middleware.ts·routes/auth.routes.ts·controllers/users.controller.ts.',
}

SOURCES = [
    ('OAuth 2.0', 'https://www.rfc-editor.org/rfc/rfc6749.html'),
    ('OpenID Connect', 'https://openid.net/specs/openid-connect-core-1_0.html#Introduction'),
    ('Supabase Social Login', 'https://supabase.com/docs/guides/auth/social-sign-in'),
    ('Supabase PKCE flow', 'https://supabase.com/docs/guides/auth/sessions/pkce-flow'),
    ('signInWithOAuth', 'https://supabase.com/docs/reference/javascript/auth-signinwithoauth'),
    ('exchangeCodeForSession', 'https://supabase.com/docs/reference/javascript/auth-exchangecodeforsession'),
    ('getUser', 'https://supabase.com/docs/reference/javascript/auth-getuser'),
    ('User profiles', 'https://supabase.com/docs/guides/auth/managing-user-data'),
]

REVIEW = dict(assessment='본문 8장을 5장으로 통합. 용어·책임 분리 → OAuth/OIDC → 실제 SDK 로그인·복귀 → 인증 계정·프로필 → API 사용자 확인 순서.',
              boundary='SDK 호출 이름은 실제 구현과 연결하는 라벨로 사용하고 전체 코드를 외우게 하지 않음. 내부 계정 병합·state·PKCE 계산·클레임 검증은 별도 보충 자료. 사용자별 작업 허용은 챕터 4.',
              caution='실제 코드 경로를 검토한 설명이며 외부 제공자 로그인 실환경 테스트를 수행한 것은 아님. Auth·브라우저 SDK·Express 서버를 구분하고 외부 토큰과 서비스용 토큰을 혼동하지 않음.')
