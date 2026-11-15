"""Five beginner-facing authorization slides aligned with Week 8 code."""
from chapter03_content import P, G, B, concept, table, Q, M


def flow(items, caption):
    return dict(kind='resource-flow', items=[dict(title=title, body=body) for title, body in items], caption=caption)


CHAPTER = dict(number=4,
    connection='챕터 3에서 확인한 사용자 ID·프로필을 실제 작업의 허용 판단과 연결.',
    scope='인증·인가 → 일반 사용자·관리자 역할 → 본인 프로필 → 미들웨어 검사 → API 키와 DB 접근. 가상의 자기 제보 수정과 RLS 정책 SQL은 보충 자료로 분리.',
    concepts=[
        concept('authorization', P('인증과 인가', 'Authentication and Authorization'),
                P('사용자 확인과 작업 허용 판단의 구분', 'Identifying users and deciding whether an operation is allowed'),
                'social-session authentication', '맛집 생성 요청에서 로그인 사용자 확인 후 관리자 역할을 별도 판단'),
        concept('role-access', P('사용자 역할과 허용 기능', 'User Roles and Permissions'),
                P('일반 사용자와 관리자의 기능 사용 범위', 'Operations available to regular users and administrators'),
                'authorization', '실제 라우트에 맞춘 공개 조회·본인 정보·제보 작성·관리 작업의 권한 표'),
        concept('owner-access', P('본인 정보의 처리', 'Updating Your Own Profile'),
                P('서버가 확인한 사용자 ID로 수정 대상 결정', 'Choose the profile to update with the server-verified user ID'),
                'role-access user-account account-link', 'PUT /api/users/profile → req.auth.id → 같은 ID의 profiles 수정'),
        concept('api-access', P('서버의 권한 검사 흐름', 'Server-Side Permission Checks'),
                P('요청한 기능을 실행하기 전 인증과 관리자 권한 검사', 'Check authentication and admin permission before running an operation'),
                'owner-access role-access jwt-validation trust-boundary', 'POST /api/restaurants → isAuthenticated → requireAdmin → controller.create'),
        concept('api-keys', P('API 키와 데이터베이스 접근', 'API Keys and Database Access'),
                P('사용자 토큰과 서버 전용 키의 역할 구분', 'Distinguish user access tokens, publishable keys and secret keys'),
                'api-access auth-token prior-data', '브라우저 키·서버 키·사용자 토큰 구분과 Express 인가 후 DB 접근'),
    ])

BODY = {
    'authorization': B('wide',
        G(P('인증(Authentication) - 요청한 사용자 확인', 'Authentication - identify the requesting user'),
          P('로그인 자격을 검증해 사용자 ID와 프로필 확인', 'Verify login credentials to identify the user and profile')),
        G(P('인가(Authorization) - 요청한 작업의 허용 여부 판단', 'Authorization - decide whether an operation is allowed'),
          P('확인한 사용자가 해당 기능을 사용해도 되는지 별도 검사', 'Separately check whether that user may perform the operation'))),
    'role-access': B('wide',
        G(P('역할(role) - 사용자에게 부여한 기능 사용 구분', 'Role - a user classification that determines permissions'),
          P('실습의 user는 일반 사용자 · admin은 관리자', 'In this project, user is a regular user and admin is an administrator'),
          P('서버가 조회한 프로필의 역할로 판단 · 요청에 적은 관리자 표시는 신뢰하지 않음', 'Use the role in the server-loaded profile, not a client-supplied admin flag'))),
    'owner-access': B('wide',
        G(P('본인 정보 - 인증된 사용자 ID에 연결된 개인 데이터', 'User profile - personal data associated with the authenticated user'),
          P('이름·이미지는 브라우저 입력으로 전달 · 수정 대상 ID는 서버가 결정', 'The browser sends the name and image; the server chooses the target ID')),
        G(P('req.auth - 인증 검사 후 요청에 연결한 사용자 정보', 'req.auth - user data attached after authentication'),
          P('isAuthenticated는 토큰·프로필을 확인해 req.auth를 채우는 서버 함수', 'isAuthenticated is the server function that checks the token and profile and populates req.auth'),
          P('req.auth.id로 본인의 프로필 선택 · 요청 본문의 userId로 대상을 바꾸지 않음', 'Select the profile with req.auth.id, rather than a userId in the request body'))),
    'api-access': B('wide',
        G(P('미들웨어(middleware) - 기능 실행 전 공통 조건을 확인하는 함수', 'Middleware - a function that checks conditions before an operation'),
          P('인증 검사 다음에 관리자 검사 · 필요한 검사를 통과한 요청만 실행', 'Check authentication, then admin permission; continue only if required checks pass')),
        G(P('화면과 서버 - 버튼 표시와 요청 허용의 구분', 'UI visibility and server-side authorization - separate responsibilities'),
          P('버튼을 숨겨도 직접 요청 가능 · 서버에서 권한을 검사해 거부', 'Users can send requests directly even if a button is hidden; the server must enforce permissions'))),
    'api-keys': B('wide',
        G(P('API 키 - Supabase 프로젝트에 접근하는 프로그램의 자격', 'API key - a program’s credentials for a Supabase project'),
          P('Publishable key는 브라우저 SDK에 사용 · 로그인 사용자의 토큰과 별개', 'The browser SDK uses a publishable key, separately from the user token'),
          P('Secret key는 Express 서버 전용 · 브라우저에 전달하지 않음', 'The secret key is for Express only and must not be sent to the browser')),
        G(P('사용자 액세스 토큰 - 로그인 사용자가 API에 제시하는 자격', 'User access token - a credential used to authenticate a signed-in user’s API requests'),
          P('Supabase가 발급 · Express가 요청자를 확인하는 데 사용 · 프로젝트 API 키와 구분', 'Issued by Supabase; Express uses it to identify the requester, separately from project API keys'))),
}

MEDIA = {
    'authorization': [[flow([
        (P('사용자 확인', 'Identify the user'), P('로그인한 사용자의 프로필 조회', 'Load the signed-in user’s profile')),
        (P('작업 권한 확인', 'Check permission'), P('맛집 생성에 필요한 관리자 역할 검사', 'Check the admin role required to create a restaurant')),
        (P('허용된 작업 실행', 'Run the allowed operation'), P('관리자일 때 맛집 생성', 'Create the restaurant only for an administrator')),
    ], P('로그인 성공과 맛집 생성 권한은 별도로 판단', 'Successful login and permission to create a restaurant are separate decisions'))]],
    'role-access': [[table([
        P('기능', 'Operation'), P('로그인 전', 'Signed out'), P('일반 사용자', 'Regular user'), P('관리자', 'Admin')], [
        [P('맛집 조회', 'View restaurants'), P('허용', 'Allowed'), P('허용', 'Allowed'), P('허용', 'Allowed')],
        [P('내 프로필 수정', 'Edit own profile'), P('불가', 'Denied'), P('본인만', 'Own profile only'), P('본인만', 'Own profile only')],
        [P('제보 작성', 'Create a submission'), P('불가', 'Denied'), P('허용', 'Allowed'), P('허용', 'Allowed')],
        [P('맛집 생성·수정·삭제', 'Create, edit or delete restaurants'), P('불가', 'Denied'), P('불가', 'Denied'), P('허용', 'Allowed')],
        [P('제보 조회·승인·거절·삭제', 'View, approve, reject or delete submissions'), P('불가', 'Denied'), P('불가', 'Denied'), P('허용', 'Allowed')],
        [P('사용자 역할 변경', 'Change user roles'), P('불가', 'Denied'), P('불가', 'Denied'), P('허용', 'Allowed')],
    ])]],
    'owner-access': [[flow([
        (P('프로필 수정 요청', 'Request a profile update'), P('PUT /api/users/profile\n이름·이미지 전송', 'PUT /api/users/profile\nSend name and image')),
        (P('서버가 사용자 확인', 'The server identifies the user'), P('isAuthenticated\n검증 결과를 req.auth에 연결', 'isAuthenticated\nAttach verified user data to req.auth')),
        (P('본인 프로필 수정', 'Update the user’s own profile'), P('req.auth.id에 해당하는 profiles 수정', 'Update profiles for req.auth.id')),
    ], P('수정 대상은 요청 본문이 아닌 인증 결과로 결정', 'The verified identity, not a request-body ID, determines the target'))]],
    'api-access': [[flow([
        (P('요청 수신', 'Receive the request'), P('POST /api/restaurants', 'POST /api/restaurants')),
        (P('isAuthenticated', 'isAuthenticated'), P('토큰·프로필·활성 상태 확인', 'Check token, profile and active status')),
        (P('requireAdmin', 'requireAdmin'), P('프로필의 관리자 역할 확인', 'Check the profile’s admin role')),
        (P('controller.create', 'controller.create'), P('허용된 맛집 생성 작업 실행', 'Create the restaurant after authorization succeeds')),
    ], P('토큰 없음·무효: 401 · 관리자 권한 없음: 403', 'Missing or invalid token: 401 · Insufficient admin privileges: 403'))]],
    'api-keys': [[Q([P('브라우저', 'Browser'), P('Express 서버', 'Express server'), P('Supabase DB', 'Supabase DB')], [
        M(0, 1, '사용자 액세스 토큰을 첨부한 API 요청', 'API request with a user access token'),
        M(1, 1, '사용자 인증·작업 권한 검사', 'Check user identity and operation permission', focus=True),
        M(1, 2, '서버의 Secret key로 데이터 요청', 'Request data with the server’s secret key', focus=True),
        M(2, 1, '허용된 서버 요청의 데이터 반환', 'Return data for the permitted server request', reply=True),
    ], P('업무 데이터는 Express API를 통해 접근 · 브라우저 직접 DB 접근은 차단', 'Access application data through Express; direct browser access to these tables is blocked'))]],
}

PARAGRAPHS = {
    'authorization': '인증은 요청한 사용자를 확인하는 과정이고 인가는 그 사용자에게 특정 작업을 허용할지 판단하는 과정이다. 챕터 3의 토큰 검증·프로필 조회 결과를 이어받되 로그인 성공 자체가 맛집 생성 허용을 뜻하지 않음을 설명한다. 본문 정의 뒤 사용자 확인 → 관리자 역할 검사 → 허용된 맛집 생성의 흐름을 배치한다. 실제 restaurants.routes.ts의 isAuthenticated·requireAdmin·controller.create 순서가 근거다.',
    'role-access': '역할은 사용자의 기능 사용 범위를 구분하는 기준이며 실습의 user와 admin을 일반 사용자와 관리자로 정의한다. 역할은 클라이언트가 적어 보낸 표시가 아니라 서버가 조회한 profiles.user_type에서 확인한다. 공개 맛집 조회, 본인 프로필 수정, 로그인 사용자의 제보 작성, 관리자 맛집·제보 관리와 역할 변경을 실제 라우트에 맞춰 비교한다. 일반 사용자의 자기 제보 조회·수정은 현재 실습 기능이 아니므로 허용 기능에 넣지 않는다. 관리자 작업은 추가 업무 조건에도 제한될 수 있으며 역할만으로 모든 DB 변경이 무조건 성공한다고 설명하지 않는다.',
    'owner-access': 'isAuthenticated를 처음 사용하는 본문에서 토큰·프로필을 확인해 req.auth를 채우는 서버 함수로 짧게 설명한다. 본인 정보는 인증된 사용자 ID에 연결된 개인 데이터다. req.auth는 인증 검사 뒤 요청에 연결한 프로필 정보이며 req.auth.id는 서버가 확인한 ID다. 브라우저는 이름·이미지 입력을 보내지만 서버의 users.controller.ts는 updateProfile(req.auth.id, req.body)를 호출하고 users.service.ts가 같은 ID의 profiles 행만 수정한다. 본문의 userId는 신뢰하지 않을 입력을 설명하는 이름이며 실제 요청에 그 필드를 요구하는 것은 아니다. 가상의 제보 소유자 정책 대신 현재 구현의 본인 프로필 수정을 사례로 사용한다.',
    'api-access': '미들웨어는 요청한 기능 실행 전에 공통 조건을 확인하는 함수다. POST /api/restaurants는 isAuthenticated로 Bearer 토큰·프로필·활성 상태를 확인하고 requireAdmin으로 req.auth.userType을 검사한 뒤 controller.create를 실행한다. 필요한 검사에 실패하면 다음 단계로 진행하지 않는다. 토큰 누락·무효는 401, 관리자 역할 부족은 403으로 구분한다. 실제 구현은 프로필 누락·비활성에 403, 인증 서비스 장애에 503도 사용할 수 있으므로 모든 실패를 두 상태로 일반화하지 않는다. React의 AdminRoute는 화면 접근을 안내하지만 서버 권한 검사를 대신하지 않는다.',
    'api-keys': 'API 키는 프로그램의 Supabase 프로젝트 접근 자격이며 사용자의 액세스 토큰과 구분한다. Publishable key는 브라우저 SDK, Secret key는 Express 서버 전용이다. Supabase가 발급한 사용자 액세스 토큰은 Express 요청에 첨부하여 요청자를 확인한다. 본문은 사용자 토큰·브라우저 키·서버 키의 역할에 집중하고 RLS의 정의·정책·Secret key의 우회 경로는 챕터4 보충 자료로 이동한다. 브라우저 키가 사용자의 관리자 권한을 증명하는 것은 아니며 Express가 사용자와 작업 권한을 검사한다. 현재 DB 권한 구조는 바꾸지 않는다.',
}

SOURCES = [
    ('OWASP Authorization', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'),
    ('Express Middleware', 'https://expressjs.com/en/guide/using-middleware.html'),
    ('Supabase API keys', 'https://supabase.com/docs/guides/getting-started/api-keys'),
    ('Supabase RLS', 'https://supabase.com/docs/guides/database/postgres/row-level-security'),
    ('Supabase getUser', 'https://supabase.com/docs/reference/javascript/auth-getuser'),
]

REVIEW = dict(assessment='본문 8장을 5장으로 통합. 용어 정의 → 실제 허용 기능 → 본인 ID → 미들웨어 흐름 → 키와 DB 경로 순서.',
              boundary='클라이언트·서버·DB의 책임을 구분하고 실제 구현과 확장 설계를 혼합하지 않음. RLS SQL·DB 역할 체계·범용 소유자 정책은 보충 자료. 승인 업무 조건과 트랜잭션은 챕터 5.',
              caution='코드·스키마를 읽어 대조한 내용이며 실환경 로그인·DB 변경 테스트 결과가 아님. Secret key를 가진 서버에서 별도 인가를 수행하는 현재 구조를 설명.')
