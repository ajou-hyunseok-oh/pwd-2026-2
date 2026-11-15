"""Editable teaching resources for the 44 researched Week 8 content slides.

Titles and prerequisites live in title_outline.py. References are exported by
slide_references.py; no source URLs or authoring notes are rendered in the deck.
"""
from reused_resources import pair as P, code, table, message as M, sequence as Q


def resource(*blocks, right=None):
    return dict(layout='single' if right is None else 'split',
                columns=[list(blocks)] if right is None else [list(blocks), right])


def flow(items, caption):
    return dict(kind='resource-flow', items=[dict(title=t, body=b) for t, b in items], caption=caption)


def note(ko, en):
    return dict(kind='resource-note', text=P(ko, en))


def concepts(ko, en, *details):
    return dict(kind='concepts', items=[dict(term=P(ko, en), details=list(details))])


def branches(title, body, children, caption):
    return dict(kind='resource-branches', title=title, body=body,
                children=[dict(title=t, body=b) for t, b in children], caption=caption)


def timeline(events, caption):
    return dict(kind='resource-timeline', events=[dict(time=t, title=v, detail=d) for t, v, d in events], caption=caption)


BROWSER, SERVER = P('브라우저', 'Browser'), P('FoodMap 서버', 'FoodMap server')
API, AUTH = P('데이터 API', 'Data API'), P('인증 시스템', 'Authentication service')

RESOURCES = {
    'identity-need': resource(
        table([P('맛집 생성 요청 사례', 'Restaurant creation request'), P('호출 API', 'API endpoint'),
               P('7주차 서버의 처리', 'Week 7 server behavior')], [
            [P('실제 맛집 정보 등록', 'Add a real restaurant'), P('POST /api/restaurants'),
             P('입력 검증 후 DB 저장 · 요청 사용자 확인 없음', 'Validate input and save to the database without authenticating the user')],
            [P('입력 형식만 맞춘 허위 맛집 등록', 'Add a fictitious restaurant using valid input'), P('POST /api/restaurants'),
             P('입력 검증을 통과하면 DB 저장 · 요청 사용자 확인 없음', 'Save if input validation passes, without authenticating the user')],
        ]),
        note('서비스의 데이터 작업을 사용자에 따라 다르게 허용하려면, 먼저 누구의 요청인지 구분할 수 있어야 한다.',
             'To enforce user-specific permissions, first identify the user making the request.')),
    'user-account': resource(
        table([P('계정의 사용자 ID', 'User ID'), P('표시 이름', 'Display name'),
               P('이메일', 'Email'), P('연결할 맛집 생성 요청', 'Associated creation request')], [
            [P('u123'), P('민수', 'Minsu'), P('minsu@example.com'), P('요청 A · POST /api/restaurants', 'Request A · POST /api/restaurants')],
            [P('u999'), P('민수', 'Minsu'), P('other@example.com'), P('요청 B · POST /api/restaurants', 'Request B · POST /api/restaurants')],
        ]),
        note('같은 이름의 계정을 고유 ID로 구분하고 맛집 생성 요청을 연결하는 설계 예시',
             'Design example: use IDs to distinguish users with the same name and associate their requests')),
    'trust-boundary': resource(
        Q([BROWSER, SERVER], [
            M(0, 0, '맛집 생성 요청 작성\nuserId=u123', 'Prepare a restaurant creation request\nuserId=u123'),
            M(0, 0, '전송 전 다른 계정의 ID로 변경\nuserId=u999', 'Replace with another account’s ID\nuserId=u999', focus=True),
            M(0, 1, 'POST /api/restaurants\n요청 본문 · userId=u999', 'POST /api/restaurants\nRequest body · userId=u999'),
            M(1, 1, '이 값만 믿고 u999에 연결하면\n다른 계정의 요청으로 오인 가능', 'Trusting this value can link\nthe request to the wrong account', focus=True),
        ], P('요청 본문의 ID로 계정을 연결한다고 가정한 사례',
             'Hypothetical design: link an account using the ID in the request body'))),
    'password-hash': resource(
        flow([(P('비밀번호 설정', 'Set a password'), P('u123 계정의 비밀번호 입력', 'Enter a password for u123')),
              (P('전용 해시 함수', 'Password hashing function'), P('검증값 계산', 'Compute the password hash')),
              (P('해시 보관', 'Store the hash'), P('u123 → hash-A', 'u123 → hash-A'))],
             P('hash-A는 검증값을 나타내는 설명용 기호', 'hash-A is a placeholder for a password hash')),
        table([P('저장 방식', 'Storage method'), P('DB 유출 시', 'If the database is compromised')], [
            [P('비밀번호 원문', 'Plaintext password'), P('비밀번호 자체가 노출', 'The password itself is exposed')],
            [P('비밀번호 해시', 'Password hash'), P('원문은 직접 드러나지 않음 · 추측 공격은 가능', 'No direct plaintext exposure; password guessing remains possible')],
        ])),
    'password-salt': resource(
        table([P('계정', 'Account'), P('설정 시 입력 비밀번호', 'Password entered at setup'), P('저장할 솔트', 'Salt to store'), P('저장할 해시', 'Hash to store')], [
            [P('u123'), P('same-password'), P('salt-A'), P('hash-A')],
            [P('u999'), P('same-password'), P('salt-B'), P('hash-B')],
        ])),
    'http-stateless': resource(
        Q([BROWSER, SERVER], [
            M(0, 1, '① 로그인 요청', '① Login request'),
            M(1, 1, '비밀번호 검증 성공\n현재 요청의 사용자 u123', 'Password verified\nUser for this request: u123'),
            M(1, 0, '로그인 결과', 'Authentication result', reply=True),
            M(0, 1, '② 맛집 생성 요청\n사용자를 확인할 정보 없음', '② Create a restaurant\nNo user credential attached', focus=True),
            M(1, 1, '이 요청도 u123의 요청인지\n판단할 근거 부족', 'Insufficient evidence that\nthis request is from u123', focus=True),
        ], P('로그인 유지 수단을 아직 적용하지 않은 상황',
             'Example without a mechanism for maintaining login state'))),
    'token-signature': resource(
        table([P('토큰의 사용자 정보', 'User data in token'), P('첨부된 서명', 'Attached signature'), P('신뢰하는 키로 검증', 'Verification with a trusted key')], [
            [P('u123 · 발급 당시 내용', 'u123 · original content'), P('signature-A'), P('서명 검증 성공', 'Signature verification passes')],
            [P('u999 · 사용자 정보 변경', 'u999 · altered user data'), P('signature-A · 그대로 사용', 'signature-A · unchanged'), P('서명 검증 실패', 'Signature verification fails')],
        ]),
        note('검증자는 신뢰하는 발급자의 키와 방법을 사용 · 서명만으로 내용이 숨겨지지는 않음',
             'Verification uses a trusted issuer’s key and method · signing does not hide the content')),
    'auth-expiry': resource(
        timeline([(P('09:00'), P('u123 로그인 성공', 'u123 logs in'), P('세션 또는 JWT 발급', 'Session or JWT issued')),
                  (P('09:10'), P('유효 기간 내 요청', 'Request before expiration'), P('다른 검증도 통과 → 인증 자격 수용', 'Other checks also pass → credential accepted')),
                  (P('09:30'), P('유효 기간 종료', 'Credentials expire'), P('세션의 최대 수명 또는 JWT의 exp 도달', 'Session maximum lifetime or JWT exp reached')),
                  (P('09:31'), P('같은 값으로 다시 요청', 'Request again with the same value'), P('값이 남아 있어도 만료로 인증 거부', 'Rejected as expired, even if still stored'))],
                 None),
        table([P('방식', 'Method'), P('만료 판단의 기준', 'Expiration criteria')], [
            [P('서버 세션', 'Server-side session'), P('비활동 시간 · 생성 후 최대 수명', 'Idle timeout and absolute session lifetime')],
            [P('JWT'), P('exp에 기록된 만료 시각', 'Expiration time recorded in exp')],
        ])),
    'refresh-token': resource(
        Q([BROWSER, API, AUTH], [
            M(0, 1, '액세스 토큰 A로 데이터 요청', 'Data request with access token A'),
            M(1, 0, '만료된 토큰 거부', 'Expired token rejected', reply=True),
            M(0, 2, '리프레시 토큰으로 갱신 요청', 'Refresh request with refresh token', focus=True),
            M(2, 2, '갱신 자격 확인\n만료·철회 시 거부', 'Validate the refresh token\nReject if expired or revoked'),
            M(2, 0, '검증 성공 시 새 액세스 토큰 B', 'New access token B if valid', reply=True),
            M(0, 1, '새 액세스 토큰 B로 재요청', 'Retry with new access token B'),
        ], P('로그인 시 리프레시 토큰도 발급받아 보관한 사례 · 갱신용 자격도 보호 필요',
             'Example with a refresh token issued at login; refresh tokens also require protection'))),
    'oidc': resource(
        table([P('토큰', 'Token'), P('확인하는 곳', 'Verified by'), P('사용 목적', 'Purpose')], [
            [P('ID 토큰', 'ID token'), P('FoodMap 서버', 'FoodMap server'), P('외부 제공자가 인증한 사용자 확인', 'Identify the user authenticated by the provider')],
            [P('액세스 토큰', 'Access token'), P('외부 프로필 API', 'External profile API'), P('허용된 프로필 정보 읽기', 'Read the permitted profile information')],
        ]),
        right=[flow([(P('외부 제공자가 ID 토큰 전달', 'The provider sends an ID token'),
                      P('외부 제공자의 사용자 인증 결과를 FoodMap 서버에 전달', 'Send the provider’s user authentication result to the FoodMap server')),
                     (P('FoodMap 서버가 토큰 검증', 'The FoodMap server validates it'),
                      P('서명·발급자·수신 대상·만료 등 확인', 'Check signature, issuer, audience and expiry')),
                     (P('FoodMap 서버가 사용자 확인', 'The FoodMap server identifies the user'),
                      P('검증 성공 시 해당 외부 계정의 사용자로 확인', 'If valid, identify the user of that external account'))],
                    P('검증 실패 시 인증 결과 거부', 'Reject the result if validation fails'))]),
    'account-link': resource(
        table([P('발급자 iss', 'Issuer iss'), P('외부 ID sub', 'External ID sub'), P('내부 사용자 ID', 'Internal user ID')], [
            [P('provider-A'), P('42'), P('u123')],
            [P('provider-B'), P('42'), P('u456')],
        ]),
        flow([(P('ID 토큰 검증', 'Validate the ID token'), P('서명·발급자·수신 대상·만료', 'Signature, issuer, audience, expiry')),
              (P('연결 기록 조회', 'Look up the association'), P('검증된 provider-A + 42', 'Verified provider-A + 42')),
              (P('내부 계정 확인', 'Identify the local account'), P('연결된 사용자 u123', 'Associated user u123'))],
             P('이미 연결된 외부 계정으로 로그인하는 사례',
               'Signing in with an external account already linked to the service'))),
    'social-session': resource(
        Q([P('외부 제공자', 'External provider'), SERVER, BROWSER], [
            M(0, 1, 'ID 토큰 · provider-A / 42', 'ID token · provider-A / 42'),
            M(1, 1, 'ID 토큰 검증 후\n연결 기록에서 u123 확인', 'Verify ID token\nFind linked user u123'),
            M(1, 2, 'FoodMap 세션 또는 토큰 발급', 'Issue FoodMap session or token', reply=True, focus=True),
            M(2, 1, '맛집 생성 요청 + FoodMap 로그인 자격', 'Create restaurant + FoodMap credentials', focus=True),
            M(1, 1, 'FoodMap 자격 검증\n현재 요청의 사용자 u123', 'Verify FoodMap credentials\nUser for this request: u123'),
        ], P('외부 제공자의 액세스 토큰은 해당 외부 API 접근에 사용',
             'The external provider’s access token is used for its external API'))),
    'role-access': resource(
        table([P('확인된 역할', 'Verified role'), P('제보 작성', 'Submit report'), P('맛집 생성', 'Create place'), P('전체 제보 조회', 'View all reports')], [
            [P('일반 사용자', 'Regular user'), P('허용', 'Allow'), P('거부', 'Deny'), P('거부', 'Deny')],
            [P('운영자', 'Operator'), P('허용', 'Allow'), P('허용', 'Allow'), P('허용', 'Allow')],
        ]),
        note('FoodMap 정책 설계 예시', 'Example FoodMap policy design')),
    'owner-access': resource(
        concepts('소유자 검사 - 요청자와 대상 데이터의 관계 확인', 'Ownership check - verify the requester’s relation to the target',
                 P('인증으로 확인한 사용자 ID와 행에 저장된 소유자 ID 비교',
                   'Compare the authenticated user ID with the owner stored on the row')),
        table([P('확인된 요청자', 'Verified requester'), P('대상 제보', 'Target report'), P('저장된 소유자', 'Stored owner'), P('조회·수정', 'Read or edit')], [
            [P('u123'), P('r101'), P('u123'), P('허용', 'Allow')],
            [P('u123'), P('r102'), P('u456'), P('거부', 'Deny')],
        ]), note('확장 설계 예시 · 일반 사용자는 본인 제보만 조회·수정',
                 'Extended design example · members may read or edit only their own reports')),
    'default-deny': resource(
        branches(P('요청의 허용 조건 확인', 'Check the allow condition'),
                 P('규칙이 요구하는 역할·소유 관계 검사', 'Check the role or ownership required by the rule'), [
            (P('조건 충족 → 허용', 'Condition met → allow'), P('공개 맛집 조회\n로그인 없이도 공개 규칙 충족', 'Read public places\nPublic-read rule met without login')),
            (P('조건 불충족 → 거부', 'Condition not met → deny'), P('일반 사용자 u123의 r102 수정\n저장된 소유자는 u456', 'Member u123 edits r102\nStored owner is u456')),
        ], P('허용 규칙이 없거나 필요한 근거를 확인하지 못한 요청도 거부',
             'Also deny when no allow rule applies or required evidence cannot be verified'))),
    'api-access': resource(
        Q([P('사용자 요청', 'User request'), API, P('DB')], [
            M(0, 1, '맛집 생성 API 직접 요청', 'Call the create-place API directly'),
            M(1, 1, '① 로그인 자격 검증\n실패 → 생성 거부', '① Verify login credential\nInvalid → deny creation'),
            M(1, 1, '② 신뢰하는 역할 확인\n운영자가 아니면 생성 거부', '② Check trusted role\nNot an operator → deny', focus=True),
            M(1, 2, '허용된 경우에만 맛집 생성', 'Create a place only if allowed'),
            M(2, 1, '생성 결과', 'Creation result', reply=True),
            M(1, 0, '응답', 'Response', reply=True),
        ], P('FoodMap 맛집 생성 사례 · 버튼 표시와 관계없이 서버에서 권한 검사',
             'FoodMap creation example · server permission checks apply regardless of button visibility'))),
    'rls': resource(
        code(P('Supabase · 자기 제보 SELECT 정책', 'Supabase · read-own-report policy'),
             'alter table public.reports\n  enable row level security;\n\ncreate policy "read own reports"\non public.reports for select\nto authenticated\nusing ((select auth.uid()) = user_id);', width=48),
        note('SELECT 권한이 있는 RLS 적용 역할 · 다른 허용 정책이 없는 예시',
             'RLS applies to a role with SELECT permission · no other allow policy in this example'),
        right=[table([P('행', 'Row'), P('user_id'), P('u123의 결과', 'Result for u123')], [
            [P('r101'), P('u123'), P('반환', 'Returned')],
            [P('r102'), P('u456'), P('제외', 'Excluded')],
            [P('r103'), P('u123'), P('반환', 'Returned')],
        ]), note('u123·u456은 UUID의 축약 표시 · auth.uid()는 Supabase Auth가 검증한 사용자 ID',
                 'u123 and u456 abbreviate UUIDs · auth.uid() is the identity verified by Supabase Auth')]),
    'api-keys': resource(
        table([P('Supabase 자격정보', 'Supabase credential'), P('식별·권한의 대상', 'Identity or authority'), P('사용 방식', 'Usage'), P('DB 접근', 'Database access')], [
            [P('publishable key'), P('애플리케이션', 'Application'), P('단독: anon · JWT와 함께: authenticated', 'Alone: anon · with JWT: authenticated'), P('활성화된 RLS 정책 적용', 'Subject to enabled RLS policies')],
            [P('secret key'), P('서버의 특권 접근', 'Privileged server access'), P('서버 전용', 'Server only'), P('RLS 우회 · API 권한 검사', 'Bypasses RLS · authorize in API')],
            [P('사용자 JWT', 'User JWT'), P('로그인한 사용자', 'Signed-in user'), P('공개 앱 키와 함께 전송', 'Send with publishable app key'), P('검증 후 사용자 문맥 제공', 'Verified user context')],
        ]),
        note('공개 가능한 앱 키만으로 로그인한 개인의 신원이 증명되지는 않음',
             'A publishable application key alone does not prove a user’s identity')),
    'foodmap-policy': resource(
        table([P('행위자 · 행동', 'Actor and action'), P('대상', 'Target'), P('API 검사', 'API check'), P('RLS 적용 경로의 조건', 'Condition on an RLS path')], [
            [P('누구나 · 맛집 조회', 'Anyone · read places'), P('공개 목록', 'Public list'), P('공개 조회 규칙', 'Public-read rule'), P('공개 대상 행', 'Publicly readable rows')],
            [P('운영자 · 맛집 생성', 'Operator · create place'), P('새 맛집', 'New place'), P('신뢰하는 운영자 역할', 'Trusted operator role'), P('운영자 조건의 INSERT 정책', 'Operator-only INSERT policy')],
            [P('작성자 · 제보 조회·수정', 'Author · read or edit report'), P('본인의 제보', 'Own reports'), P('사용자 ID = 소유자 ID', 'User ID = owner ID'), P('소유자 일치 · 작업별 정책', 'Owner policy per operation')],
            [P('운영자 · 전체 제보 조회', 'Operator · read all reports'), P('전체 제보', 'All reports'), P('신뢰하는 운영자 역할', 'Trusted operator role'), P('검증된 운영자 문맥', 'Verified operator context')],
        ]),
        note('FoodMap 확장 설계 예시 · 특권 키 경로의 권한 검사는 API에서 수행',
             'Extended FoodMap design example · the API authorizes privileged-key requests')),
}

RESOURCES.update({
    'admin-system': resource(
        dict(kind='resource-workspaces', panes=[
            dict(title=P('사용자 서비스', 'User service'), role=P('맛집 탐색 · 제보', 'Explore and submit'),
                 rows=[P('아주식당 · 위치 보기', 'Ajou Kitchen · view location'), P('새로운 맛집 제보', 'Submit a new place')]),
            dict(title=P('관리자 시스템', 'Admin system'), role=P('전체 제보 조회 · 관리', 'Review and manage all reports'),
                 rows=[P('r101 · 작성자 u123', 'r101 · submitted by u123'), P('r102 · 작성자 u456', 'r102 · submitted by u456')]),
        ], caption=P('FoodMap 화면 구성 예시 · 공통 서버·DB를 사용해도 관리 요청에는 운영자 권한 필요',
                     'Example FoodMap screens · shared infrastructure still requires operator authorization for admin requests'))),
    'admin-boundary': resource(
        table([P('권한', 'Authority'), P('관리 대상', 'Target'), P('허용 업무 예시', 'Example work'), P('자동으로 포함되지 않는 권한', 'Not automatically included')], [
            [P('FoodMap 운영자', 'FoodMap operator'), P('서비스의 제보', 'Service reports'), P('제보 조회·관리', 'View and manage reports'), P('DB 구조 변경', 'Alter database schema')],
            [P('DB 관리 권한', 'DB administration'), P('테이블·정책', 'Tables and policies'), P('스키마·접근 정책 변경', 'Change schema and policies'), P('배포 계정 관리', 'Manage deployment accounts')],
            [P('플랫폼 관리 권한', 'Platform administration'), P('프로젝트·배포', 'Projects and deployments'), P('프로젝트 설정·멤버 관리', 'Manage project settings and members'), P('앱 내부 운영자 역할', 'An operator role in the app')],
        ]),
        note('업무에 필요한 권한을 해당 시스템에서 별도로 부여', 'Grant the authority needed for each job within the relevant system')),
    'workflow-state': resource(
        branches(P('검토 대기 · pending', 'Awaiting review · pending'),
                 P('r101의 현재 상태 확인', 'Check the current state of r101'), [
            (P('승인 · approved', 'Approved · approved'), P('운영자 확인 + 대기 상태\n제보를 받아들이는 결정', 'Verified operator + pending state\nAccept the report')),
            (P('반려 · rejected', 'Rejected · rejected'), P('운영자 확인 + 대기 상태\n제보를 받아들이지 않는 결정', 'Verified operator + pending state\nDecline the report')),
        ], P('FoodMap 예시 정책 · 이미 처리된 제보의 상태 변경은 조건 불충족',
             'Example policy · an already processed report does not meet the transition condition'))),
    'publication-state': resource(
        table([P('검토 결과', 'Review result'), P('공개 여부', 'Visibility'), P('사용자 목록', 'Public list'), P('업무 상황', 'Situation')], [
            [P('승인', 'Approved'), P('공개', 'Visible'), P('노출', 'Shown'), P('검토와 정보 확인 완료', 'Review and information checks complete')],
            [P('승인', 'Approved'), P('비공개', 'Hidden'), P('미노출', 'Hidden'), P('추가 정보 확인 중', 'Checking additional information')],
            [P('대기·반려', 'Pending or rejected'), P('비공개', 'Hidden'), P('미노출', 'Hidden'), P('공개 조건 미충족', 'Publication conditions not met')],
        ]),
        note('예시 공개 조건: 승인 AND 공개 · 노출 중지 후에도 승인 이력 유지',
             'Example publication rule: approved AND visible · approval history remains after hiding content')),
    'admin-transaction': resource(
        dict(kind='resource-transaction', operations=[P('① r101 승인 상태 변경', '① Mark r101 approved'),
                                                       P('② 맛집 place-01 등록', '② Create place-01')],
             results=[(P('모두 성공', 'Both succeed'), P('승인 + 등록 함께 반영', 'Approval and place are committed together')),
                      (P('등록 실패', 'Place creation fails'), P('승인 변경도 함께 취소', 'The approval change is rolled back too'))]),
        note('같은 DB 트랜잭션 안의 변경에 적용 · 별도 외부 API까지 자동으로 묶이지 않음',
             'Applies to changes within one DB transaction · separate external API calls are not automatically included')),
    'idempotency': resource(
        Q([P('운영자 화면', 'Operator UI'), SERVER, P('처리 기록 · DB', 'Result store · DB')], [
            M(0, 1, '승인 요청 · key=approve:r101', 'Approve · key=approve:r101'),
            M(1, 2, '최초 처리 · 맛집 1건과 결과 기록', 'First execution · one place and saved result'),
            M(1, 0, '응답 유실', 'Response lost', reply=True),
            M(0, 1, '같은 키·같은 작업으로 재요청', 'Retry the same operation with the same key', focus=True),
            M(1, 2, '기존 처리 결과 조회', 'Look up the stored result', focus=True),
            M(2, 1, '저장된 처리 결과', 'Stored result', reply=True),
            M(1, 0, '기존 결과 반환 · 맛집은 1건 유지', 'Return saved result · still one place', reply=True),
        ], P('서버에서 키·요청 일치 확인, 중복 제약과 원자적 결과 기록을 함께 적용',
             'Server-side key/payload checks, uniqueness constraints and atomic result recording work together'))),
    'audit-log': resource(
        table([P('기록 항목', 'Field'), P('승인 작업의 예시 값', 'Example approval event'), P('확인할 내용', 'What it answers')], [
            [P('시각', 'Time'), P('2026-11-07 10:00 +09:00'), P('언제', 'When')],
            [P('행위자', 'Actor'), P('op-01'), P('누가', 'Who')],
            [P('대상', 'Target'), P('report:r101'), P('어떤 기록을', 'Which record')],
            [P('행동 · 결과', 'Action and outcome'), P('approve · success'), P('어떻게 처리했는지', 'What happened')],
            [P('사유', 'Reason'), P('정보 확인 완료', 'Information verified'), P('왜 처리했는지', 'Why')],
        ]),
        note('가상 감사 기록 · 조회·변경 권한 제한 · 비밀번호와 토큰 원문 제외',
             'Synthetic audit event · restrict read/write access · exclude passwords and raw tokens')),
    'input-validation': resource(
        code(P('서버 JavaScript · 파싱한 name·latitude 검사', 'Server JavaScript · validate parsed name and latitude'),
             "const nameOK =\n  typeof name === 'string' &&\n  name.trim().length > 0 &&\n  name.length <= 100;\nconst latitudeOK =\n  Number.isFinite(latitude) &&\n  latitude >= -90 &&\n  latitude <= 90;\n\nif (!nameOK || !latitudeOK) {\n  throw new Error('Invalid report input');\n}", 'javascript', 48),
        right=[table([P('입력', 'Input'), P('결과', 'Result')], [
            [P('아주식당 · 37.28', 'Ajou Kitchen · 37.28'), P('통과', 'Pass')],
            [P('공백 이름 · 37.28', 'Blank name · 37.28'), P('거부', 'Reject')],
            [P('아주식당 · 91', 'Ajou Kitchen · 91'), P('범위 초과', 'Out of range')],
            [P('아주식당 · "37.28"', 'Ajou Kitchen · "37.28"'), P('숫자가 아닌 문자열', 'String, not a number')],
        ]), note('100자 제한은 예시 정책 · 오류를 입력 오류 응답으로 바꾸는 핸들러는 생략',
                 'The 100-character limit is illustrative · the input-error response handler is omitted')]),
    'sql-injection': resource(
        concepts('매개변수 쿼리 - SQL 구조와 입력값의 분리', 'Parameterized query - separate SQL structure from input values',
                 P('문자열 결합은 입력을 명령문에 섞는 방식 · 매개변수는 값을 데이터로 전달',
                   'Concatenation mixes input into the command · parameters send values as data')),
        code(P('서버 node-postgres · 연결된 client와 검색 문자열', 'Server node-postgres · connected client and search string'),
             "const result = await client.query(\n  'SELECT name FROM restaurants WHERE name = $1',\n  [searchTerm]\n);", 'javascript', 64),
        note('searchTerm = "김\'s 식당" → 따옴표도 값으로 처리 · $1은 테이블명·열명 치환용이 아님',
             'searchTerm = "Kim\'s Kitchen" → the quote stays part of the value · $1 cannot substitute table or column names')),
    'xss': resource(
        code(P('React · 문자열을 표시하는 컴포넌트', 'React · component displaying a string'),
             'function ReportText({ report }) {\n  return <p>{report.description}</p>;\n}', 'jsx', 48),
        table([P('사용자 입력 문자열', 'User-supplied string'), P('텍스트 출력 결과', 'Text output')], [
            [P('<strong>추천</strong>', '<strong>Great</strong>'), P('<strong>추천</strong>', '<strong>Great</strong>')],
        ]),
        right=[branches(P('사용자 콘텐츠', 'User content'), P('출력 문맥에 따라 달라지는 해석', 'Interpretation depends on output context'), [
            (P('문자열 자식', 'String child'), P('태그를 포함한 텍스트로 표시', 'Display the tags as text')),
            (P('HTML로 해석', 'Interpret as HTML'), P('구조·실행 코드로 처리될 위험', 'May become markup or executable code')),
        ], P('HTML 허용 시 허용 요소를 제한하는 정제 필요', 'Allowing HTML requires sanitization that limits permitted content'))]),
    'origin': resource(
        table([P('기준: https://app.example.com', 'Base: https://app.example.com'), P('달라진 부분', 'Difference'), P('출처 판정', 'Origin')], [
            [P('https://app.example.com/reports'), P('경로', 'Path'), P('같음', 'Same')],
            [P('https://app.example.com:443'), P('기본 포트 명시', 'Explicit default port'), P('같음', 'Same')],
            [P('https://app.example.com:8443'), P('포트', 'Port'), P('다름', 'Different')],
            [P('https://api.example.com'), P('호스트', 'Host'), P('다름', 'Different')],
            [P('http://app.example.com'), P('프로토콜', 'Scheme'), P('다름', 'Different')],
        ]),
        note('출처 = 프로토콜 + 호스트 + 포트 · 경로는 출처의 구성 요소에서 제외',
             'Origin = scheme + host + port · the path is not part of the origin')),
    'site': resource(
        table([P('기준: https://app.example.com', 'Base: https://app.example.com'), P('같은 출처', 'Same origin'), P('같은 사이트', 'Same site')], [
            [P('https://app.example.com/reports'), P('예', 'Yes'), P('예', 'Yes')],
            [P('https://app.example.com:8443'), P('아니오', 'No'), P('예', 'Yes')],
            [P('https://api.example.com'), P('아니오', 'No'), P('예', 'Yes')],
            [P('http://app.example.com'), P('아니오', 'No'), P('아니오', 'No')],
            [P('https://other.example.org'), P('아니오', 'No'), P('아니오', 'No')],
        ]),
        note('사이트 = 프로토콜 + 등록 가능한 도메인 · example.com, example.co.kr 등의 단위',
             'Site = scheme + registrable domain · units such as example.com or example.co.kr')),
    'same-origin-policy': resource(
        Q([P('외부 페이지 코드', 'External page script'), P('브라우저 경계', 'Browser boundary'), API], [
            M(0, 2, '일부 교차 출처 요청은 전송 가능', 'Some cross-origin requests can be sent'),
            M(2, 2, '요청을 받은 서버의 처리', 'Server receives and handles the request'),
            M(2, 1, '서버 응답 도착', 'Server response arrives', reply=True),
            M(1, 1, '허용되지 않은 응답 읽기 차단', 'Block unauthorized response reads', focus=True),
        ], P('요청의 서버 도착과 스크립트의 응답 읽기는 서로 다른 판단',
             'Whether a request reaches the server and whether script can read its response are separate decisions'))),
    'cors': resource(
        Q([BROWSER, P('API 서버', 'API server')], [
            M(0, 1, 'Origin: https://app.example.com'),
            M(1, 0, 'Access-Control-Allow-Origin:\nhttps://app.example.com', reply=True, focus=True),
            M(0, 0, '브라우저가 허용 조건 확인\n응답 읽기 허용', 'Browser checks permission\nAllows reading the response'),
        ], P('기본 요청의 응답 읽기 허용', 'Allow reading the response to a basic request')),
        right=[flow([(P('사전 확인이 필요한 요청', 'Request requiring preflight'), P('예: application/json POST', 'Example: application/json POST')),
                     (P('OPTIONS 확인', 'OPTIONS check'), P('출처 · 메서드 · 헤더 허용', 'Origin, method and headers allowed')),
                     (P('실제 요청', 'Actual request'), P('허용된 조건으로 전송', 'Send under the allowed conditions'))],
                    P('모든 요청에 사전 확인이 필요한 것은 아님', 'Not every request requires preflight')),
               note('자격정보 요청은 허용 출처를 구체적으로 지정 · API 인증·인가는 별도',
                    'Credentialed requests need a specific allowed origin · API authentication and authorization remain separate')]),
    'csrf': resource(
        Q([P('다른 사이트', 'Another site'), P('로그인된 브라우저', 'Signed-in browser'), SERVER], [
            M(0, 1, '사용자 의도와 다른 요청 유발', 'Trigger an unintended request'),
            M(1, 2, '상태 변경 요청 · 조건에 맞으면 쿠키 첨부', 'State-changing request · eligible cookies attached'),
            M(2, 2, '로그인 자격만으로\n사용자 의도 판단 불가', 'Login credentials alone\ndo not prove user intent', focus=True),
            M(2, 2, 'CSRF 확인값 · 요청 출처 검증\n실패 시 상태 변경 거부', 'Verify CSRF token and origin\nReject changes on failure', focus=True),
        ], P('쿠키 첨부 조건과 별도로 서버에서 상태 변경 요청의 정당성 확인',
             'Beyond cookie eligibility, the server validates state-changing requests'))),
    'login-rate-limit': resource(
        timeline([(P('시도 1', 'Attempt 1'), P('로그인 실패', 'Login fails'), P('계정별 실패 기록', 'Record failure for the account')),
                  (P('시도 2…', 'Attempts 2…'), P('반복 실패 관측', 'Observe repeated failures'), P('계정과 요청 출처 등 확인', 'Consider account and request source')),
                  (P('관찰 구간', 'Observation window'), P('지연 · 일시 제한', 'Delay or temporary limit'), P('반복 추측의 비용 증가', 'Increase the cost of guessing'))],
                 P('횟수·기간은 서비스 정책에 따라 결정 · 무기한 계정 잠금의 악용 가능성 고려',
                   'Thresholds and durations depend on policy · consider abuse of indefinite account lockouts'))),
    'environments': resource(
        dict(kind='resource-environments', database=False),
        note('각 실행 환경 안에 사용자 화면과 관리자 화면 포함 · 업무 분리와 환경 분리는 서로 다른 기준',
             'Each environment contains user and admin functions · functional separation and environment separation are different dimensions')),
    'secret-management': resource(
        table([P('설정', 'Setting'), P('전달 경로', 'Delivery path'), P('노출 범위', 'Visibility')], [
            [P('SERVER_SECRET'), P('환경 → 서버 프로세스', 'Environment → server process'), P('서버에서만 사용', 'Used only on the server')],
            [P('VITE_API_URL'), P('환경 → 빌드 → 브라우저 번들', 'Environment → build → browser bundle'), P('사용자가 읽을 수 있음', 'Readable by users')],
        ]),
        flow([(P('키 노출 확인', 'Detect exposed key'), P('저장소 · 로그 · 배포 파일', 'Repository, logs or deployed files')),
              (P('기존 키 폐기', 'Revoke the old key'), P('유출된 자격의 효력 중단', 'Stop the exposed credential working')),
              (P('새 키 적용', 'Apply a new key'), P('서버의 안전한 경로로 주입', 'Inject through a secure server path'))],
             P('VITE_는 Vite의 공개 설정 규칙 · 파일에서 삭제하는 것만으로 키의 효력이 끝나지는 않음',
               'VITE_ is Vite’s public-setting convention · deleting a key from a file does not revoke it'))),
    'environment-data': resource(
        dict(kind='resource-environments', database=True),
        note('주소가 달라도 같은 DB를 사용하면 데이터는 공유 · 테스트 초기화는 테스트 DB에서 수행',
             'Different URLs can still share one database · reset test data only in the test database')),
    'deployment': resource(
        flow([(P('검증 환경', 'Staging'), P('버전 v2 + 검증 설정\n로그인 · 조회 · 관리 기능 확인', 'Version v2 + staging settings\nCheck login, reads and admin actions')),
              (P('운영 반영', 'Deploy to production'), P('검증한 버전 + 운영 설정\n실제 연결 대상 확인', 'Verified version + production settings\nConfirm the connection target')),
              (P('반영 후 확인', 'Verify after deployment'), P('주요 요청의 정상 처리\n배포 버전 확인', 'Exercise key requests\nConfirm the deployed version'))],
             P('프로세스 실행 여부와 서비스 기능의 정상 동작을 함께 확인',
               'Check both the running process and actual service behavior'))),
    'db-migration': resource(
        code(P('SQL 변경 파일 · 확장 단계 발췌', 'SQL migration file · expansion step'),
             '-- 20261107_add_report_review_status.sql\nalter table public.reports\nadd column review_status text;', width=48),
        note('기존 행의 새 열 값은 NULL · 현재 실제 DB에 대한 실행 지시가 아닌 구조 변경 예시',
             'Existing rows have NULL in the new column · an illustrative schema change'),
        right=[table([P('순서', 'Order'), P('확인할 내용', 'Check')], [
            [P('열 추가', 'Add column'), P('이전 코드와의 호환성', 'Compatibility with old code')],
            [P('기존 행 보완', 'Backfill existing rows'), P('기록의 의미에 맞는 상태', 'State appropriate to each record')],
            [P('새 코드 적용', 'Deploy new code'), P('새 열을 읽고 쓰는 동작', 'Reads and writes of the new column')],
            [P('제약 보강', 'Add constraints'), P('데이터·코드의 준비 상태', 'Readiness of data and code')],
        ])]),
    'monitoring': resource(
        dict(kind='resource-metrics', times=['09:00','09:05','09:10','09:15','09:20'],
             series=[dict(title=P('요청 실패율 · 5xx / 전체 요청', 'Request failure rate · 5xx / all requests'),
                          values=[0,1,1,7,9], max=10, unit='%'),
                     dict(title=P('p95 응답 시간', 'p95 response time'),
                          values=[180,190,185,520,650], max=700, unit='ms')], deploy_index=2),
        note('p95: 요청의 95%가 이 시간 이내에 응답 · 가상 관측값',
             'p95: 95% of requests complete within this time · synthetic data'),
        note('09:10 v2 배포 · 09:15 DB 연결 오류 기록 · 시점의 일치만으로 원인 확정 불가',
             'v2 deployed at 09:10 · DB connection error at 09:15 · timing alone does not establish causation')),
    'backup': resource(
        timeline([(P('09:00'), P('백업 사본 생성', 'Create backup copy'), P('이 시점의 데이터 확보', 'Data through this point is retained')),
                  (P('09:15'), P('새 제보 저장', 'New report saved'), P('사본 이후의 정상 변경', 'Valid changes after the backup')),
                  (P('09:30'), P('데이터 장애', 'Data incident'), P('사본 이후 변경의 보존 여부 확인', 'Check preservation of later changes'))],
                 P('시간은 예시 · 백업 주기·보관 기간과 실제 복원 가능성 확인',
                   'Illustrative times · verify backup frequency, retention and recoverability')),
        note('Supabase DB 백업에 Storage 파일 본문은 포함되지 않음 · 파일 사본은 별도 범위',
             'Supabase database backups exclude Storage file contents · file copies are a separate scope')),
    'rollback': resource(
        table([P('대상', 'Target'), P('장애 시점', 'At the incident'), P('앱 롤백 후', 'After app rollback')], [
            [P('실행 버전', 'Application version'), P('v2'), P('이전 정상 버전 v1', 'Previous working version v1')],
            [P('DB 구조', 'Database schema'), P('새 열이 있는 현재 구조', 'Current schema with the new column'), P('현재 구조 유지', 'Current schema remains')],
            [P('DB 데이터', 'Database data'), P('현재 데이터', 'Current data'), P('자동 복원되지 않음', 'Not automatically restored')],
        ]),
        note('이전 앱과 현재 DB·설정의 호환성 확인 후 복귀',
             'Check that the old app is compatible with the current database and settings before reverting')),
    'restore': resource(
        flow([(P('복원 시점 선택', 'Choose recovery point'), P('09:00 사본\n이후 정상 변경 별도 보존', '09:00 backup\nPreserve valid later changes separately')),
              (P('격리 DB에서 검증', 'Verify in an isolated DB'), P('데이터 내용 확인\n서비스 동작 확인', 'Check restored records\nVerify application behavior')),
              (P('반영 범위 결정', 'Choose what to apply'), P('필요한 기록 병합 또는 전환\n반영 후 무결성 확인', 'Merge required records or switch over\nVerify integrity after applying'))],
             P('삭제된 제보를 되살리는 예시 · 실제 복원 방식은 저장소의 지원 범위에 맞춰 선택',
               'Example recovery of deleted reports · choose a method supported by the data store'))),
})



# Active, implementation-aligned Chapter 3. Earlier definitions are historical.
from chapter03_content import MEDIA as CHAPTER3_MEDIA
RESOURCES.pop('oidc')
RESOURCES['account-link']['columns'] = CHAPTER3_MEDIA['account-link']
RESOURCES['social-session']['columns'] = CHAPTER3_MEDIA['social-session']

# Active beginner-facing Chapter 4.
from chapter04_content import MEDIA as CHAPTER4_MEDIA
RESOURCES.pop('default-deny')
RESOURCES.pop('rls')
RESOURCES.pop('foodmap-policy')
RESOURCES['role-access']['columns'] = CHAPTER4_MEDIA['role-access']
RESOURCES['owner-access']['columns'] = CHAPTER4_MEDIA['owner-access']
RESOURCES['api-access']['columns'] = CHAPTER4_MEDIA['api-access']
RESOURCES['api-keys']['columns'] = CHAPTER4_MEDIA['api-keys']

# Active beginner-facing Chapter 5.
from chapter05_content import MEDIA as CHAPTER5_MEDIA
for ident in ('admin-boundary','publication-state','audit-log'):
    RESOURCES.pop(ident)
for ident, columns in CHAPTER5_MEDIA.items():
    RESOURCES[ident] = dict(layout='single', columns=columns)

# Web attacks and defenses are deferred to next week's lecture.
from curriculum_scope import DEFERRED_SECURITY_IDS
for ident in DEFERRED_SECURITY_IDS:
    RESOURCES.pop(ident, None)

from chapter06_content import MEDIA as CHAPTER6_MEDIA, RETIRED as CHAPTER6_RETIRED
for ident in CHAPTER6_RETIRED:
    RESOURCES.pop(ident)
for ident, columns in CHAPTER6_MEDIA.items():
    RESOURCES[ident] = dict(layout='single', columns=columns)
