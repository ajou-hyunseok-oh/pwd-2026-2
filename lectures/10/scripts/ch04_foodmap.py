"""Chapter 04: Practical FoodMap application of authentication, authorization, and security."""
from dsl import (
    P,
    chapter,
    code_block,
    concept,
    concepts_block,
    note_block,
    slide,
    table_block,
)

SLIDES = [
    chapter(
        'foodmap-apply',
        '실전 적용: 푸드맵 인증·인가 및 보안 설계',
        'Practice: FoodMap Security and Auth Design',
    ),
    slide(
        'foodmap-security-gap',
        P('현재 푸드맵의 보안 공백 진단', 'Auditing Security Gaps in Current FoodMap'),
        P('인증 없는 API와 브라우저 localStorage 의존 구조 점검', 'Reviewing unauthenticated APIs and localStorage reliance'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('현재 구현 범위 (7~9주차) - React 클라이언트 · Express API · Supabase DB 구조',
                          'Current scope (Weeks 7–9) - React client, Express API, and Supabase DB'),
                        P('맛집 목록 조회는 동작하나 제보·좋아요가 localStorage에 남거나 비인증 요청 허용',
                          'Restaurant listing works, but submissions rely on localStorage or allow unauthenticated writes'),
                        P('누구나 가짜 제보를 대량 등록하거나 타인 데이터를 조작할 수 있는 무방비 상태',
                          'Anyone can flood fake submissions or tamper with records without user verification'),
                    )
                )
            ],
            [
                table_block(
                    [P('점검 항목', 'Area'), P('현재 상태 (적용 전)', 'Current State'), P('보안 적용 목표', 'Security Target')],
                    [
                        [
                            P('맛집 제보 저장', 'Submissions'),
                            P('localStorage · 비인증 저장', 'localStorage / unauthenticated'),
                            P('로그인 사용자 식별 후 DB 저장', 'Authenticated user linked in DB'),
                        ],
                        [
                            P('제보 승인 · 거절', 'Admin Approval'),
                            P('역할 구분 · 관리자 검증 없음', 'No role or admin check'),
                            P('서버 관리자 권한 검사 필수', 'Server-side admin role enforcement'),
                        ],
                        [
                            P('통신 및 비밀키', 'Transport & Keys'),
                            P('로컬 환경 위주 연결', 'Local development defaults'),
                            P('엄격한 CORS · 쿠키 · 키 분리', 'Strict CORS, cookies, key isolation'),
                        ],
                    ],
                )
            ],
        ],
        sources=['lectures/08/lab-review/index.html', 'lectures/10/materials/lecture-plan.md'],
        note='7~9주차 구현 사실과 10주차 신규 보안 적용 설계 과제를 구분.',
    ),
    slide(
        'foodmap-role-matrix',
        P('역할별 권한 매트릭스와 데이터 모델', 'Role-Based Access Matrix and Data Model'),
        P('비로그인·일반 사용자·관리자 정책과 사용자 스키마 확장', 'Access policy by role and schema extension for users and submissions'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('권한 명세 - 비로그인·일반 사용자·관리자별 API 허용과 거부 계약',
                          'Access contract - explicit API allow and deny rules per user role'),
                        P('화면에서 승인 버튼을 숨기는 것은 보안이 아니며 서버 응답(401·403)으로 강제',
                          'Hiding UI buttons is not security; enforce rules with server 401 and 403 responses'),
                    ),
                    concept(
                        P('데이터 모델 확장 - 사용자 신원과 제보 소유권 연결',
                          'Schema extension - linking user identity and submission ownership'),
                        P('users 테이블에 단방향 해시 비밀번호(bcrypt/argon2)와 role 저장 · submissions에 user_id 연결',
                          'Store hashed passwords and role in users; link submissions via user_id foreign key'),
                    ),
                )
            ],
            [
                table_block(
                    [P('요청 (API)', 'Request'), P('비로그인', 'Anonymous'), P('일반 사용자', 'User'), P('관리자', 'Admin')],
                    [
                        [P('맛집 목록 조회', 'List restaurants'), P('허용', 'Allow'), P('허용', 'Allow'), P('허용', 'Allow')],
                        [P('맛집 제보 등록', 'Submit restaurant'), P('거부 (401)', 'Deny (401)'), P('허용', 'Allow'), P('허용', 'Allow')],
                        [P('본인 제보 수정', 'Edit own submission'), P('거부 (401)', 'Deny (401)'), P('본인만 허용', 'Owner only'), P('허용', 'Allow')],
                        [P('제보 승인 · 거절', 'Approve / Reject'), P('거부 (401)', 'Deny (401)'), P('거부 (403)', 'Deny (403)'), P('허용', 'Allow')],
                    ],
                )
            ],
        ],
        sources=['https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html'],
    ),
    slide(
        'foodmap-auth-cors',
        P('인증 흐름과 교차 출처(CORS·쿠키) 설정', 'Auth Flow and Cross-Origin (CORS & Cookie) Setup'),
        P('안전한 로그인·세션 전달과 Vercel–Render 간 출처 허용', 'Secure session delivery and strict CORS origin configuration'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('로그인 파이프라인 - 해시 비교 검증 후 보호 속성이 적용된 세션 쿠키 발급',
                          'Login pipeline - verify password hash and issue protected session cookie'),
                        P('HttpOnly · Secure · 적절한 SameSite 속성 적용 · 로그아웃 시 서버 저장소 무효화',
                          'Set HttpOnly, Secure, and SameSite flags; invalidate the server session on logout'),
                        P('로그인 비밀번호와 세션 식별자 원문은 서버 로그에 기록 금지',
                          'Never write passwords or raw session identifiers to server logs'),
                    ),
                    concept(
                        P('교차 출처 허용 설정 - 배포된 프론트엔드 주소(CLIENT_URL)만 API 읽기 허용',
                          'CORS policy - allow only the deployed frontend origin (CLIENT_URL)'),
                        P('Vercel(UI)과 Render(API) 출처가 다르므로 와일드카드(*) 대신 명시적 출처 지정',
                          'Vercel UI and Render API have different origins; specify an explicit origin instead of *'),
                    ),
                )
            ],
            [
                code_block(
                    P('Express · 명시적 출처 CORS와 보호 쿠키 설정 예시', 'Express · explicit CORS origin and protected cookie setup'),
                    "app.use(\n  cors({\n    origin: process.env.CLIENT_URL,\n    credentials: true\n  })\n);\n\nres.cookie('sid', sessionId, {\n  httpOnly: true,\n  secure: process.env.NODE_ENV === 'production',\n  sameSite: 'lax'\n});",
                    'javascript',
                    64,
                )
            ],
        ],
        sources=['lectures/08/materials/chapter06-supplement.ko.txt'],
    ),
    slide(
        'foodmap-server-defenses',
        P('서버 인가 및 입력·쿼리·출력 방어 구현', 'Server Authorization and Input, Query, and Output Defenses'),
        P('Express 미들웨어 권한 검사와 3대 취약점 코드 수준 방어', 'Express authorization middleware and code-level defenses'),
        'code',
        [
            [
                concepts_block(
                    concept(
                        P('서버 인가 미들웨어 - 라우트 실행 전 인증(401)·역할(403)·소유권 확인',
                          'Server auth middleware - check identity (401), role (403), and ownership'),
                        P('isAuthenticated → requireAdmin 순서로 관리자 라우트 보호',
                          'Chain isAuthenticated and requireAdmin before admin controllers'),
                    ),
                    concept(
                        P('코드 수준 3대 방어 - 입력 범위 검증 · 매개변수화 쿼리 · React 텍스트 출력',
                          'Three code defenses - input checks, parameterized SQL, and React text binding'),
                        P('파싱된 name·latitude 검증으로 비정상 입력 차단 · $1 쿼리로 SQL 인젝션 방어',
                          'Validate parsed name and latitude; parameterize queries with $1'),
                        P('제보 설명을 JSX 문자열 자식으로 출력해 스크립트 실행(XSS) 차단',
                          'Render submission text as JSX text children to prevent XSS'),
                    ),
                )
            ],
            [
                code_block(
                    P('서버 JS · 입력 검증 및 매개변수화 쿼리', 'Server JS · input validation and parameterized query'),
                    "const nameOK = typeof name === 'string' && name.trim().length > 0;\nconst latOK =\n  Number.isFinite(latitude) && latitude >= -90 && latitude <= 90;\nif (!nameOK || !latOK) {\n  return res.status(400).json({ error: 'Invalid input' });\n}\n\nawait client.query(\n  'SELECT name FROM restaurants WHERE name = $1',\n  [searchTerm]\n);",
                    'javascript',
                    66,
                ),
                code_block(
                    P('React JSX · 안전한 텍스트 출력', 'React JSX · safe text rendering'),
                    "function ReportText({ report }) {\n  return <p>{report.description}</p>;\n}",
                    'jsx',
                    52,
                ),
            ],
        ],
        sources=['lectures/08/scripts/new_resources.py'],
        note='8주차에서 분리된 푸드맵 입력 검증 · SQL 인젝션 · XSS 방어 예제를 실전 적용 장으로 통합.',
    ),
    slide(
        'foodmap-secrets-verify',
        P('비밀정보 격리 · AI 경계 · 보안 검증', 'Secret Isolation, AI Boundaries, and Security Verification'),
        P('환경변수 번들 분리와 가상 AI 요약·권한 우회 테스트 계획', 'Client/server env separation, read-only AI design, and verification harness'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('환경변수 분리 - 브라우저 번들(VITE_*)과 서버 전용 키(SERVER_SECRET) 엄격 격리',
                          'Env separation - isolate browser VITE_* vars from server secrets'),
                        P('Supabase Service Role Key와 세션 비밀키는 Express 서버 환경에서만 로드',
                          'Load the Supabase Service Role Key and session secrets only on the Express server'),
                    ),
                    concept(
                        P('가상 AI 제보 요약 경계 - 외부 제보 텍스트와 관리자 승인 도구의 권한 분리',
                          'Hypothetical AI summarizer boundary - isolate untrusted reports from admin tools'),
                        P('요약기는 읽기 전용으로 동작하며 제보 승인·삭제나 DB 직접 변경 권한 부여 금지',
                          'Keep the summarizer read-only with no approval or database write permissions'),
                    ),
                )
            ],
            [
                table_block(
                    [P('환경 설정', 'Config'), P('전달 경로', 'Delivery Path'), P('노출 범위', 'Visibility')],
                    [
                        [
                            P('SUPABASE_SERVICE_ROLE_KEY', 'SUPABASE_SERVICE_ROLE_KEY'),
                            P('환경 → Express 프로세스', 'Env → Express server'),
                            P('서버 전용 (절대 노출 금지)', 'Server only (never expose)'),
                        ],
                        [
                            P('VITE_API_BASE_URL', 'VITE_API_BASE_URL'),
                            P('환경 → 빌드 → 브라우저 번들', 'Env → build → browser bundle'),
                            P('사용자 열람 가능 (공개 주소만)', 'Publicly readable (URLs only)'),
                        ],
                    ],
                ),
                note_block(P('보안 수용 조건 검증 (하네스): 비로그인 제보(401) · 일반 사용자 승인(403) · 타인 수정(403) · 로그아웃 후 재요청 거부 확인',
                             'Security acceptance tests: verify 401 on anonymous submit, 403 on user approval or editing others’ entries, and post-logout rejection')),
            ],
        ],
        sources=['lectures/08/scripts/new_resources.py', 'lectures/10/materials/incident-vulnerability-analysis.md'],
        note='가상 AI 제보 요약은 수업용 위협 모델링 시나리오이며 현재 푸드맵 구현 사실이 아니다.',
    ),
]
