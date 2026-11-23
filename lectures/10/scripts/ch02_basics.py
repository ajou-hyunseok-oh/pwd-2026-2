"""Chapter 02: Web mechanics and authentication/authorization fundamentals (Review)."""
from dsl import P, chapter, concept, concepts_block, msg, seq_block, slide, table_block

WEEK6_PDF = 'lectures/08/materials/[PWD Week6] 웹 서비스 인증과 보안.pdf'

SLIDES = [
    chapter(
        'basics',
        '웹 동작 원리와 인증·인가 기초',
        'Web Mechanics and Auth Fundamentals',
    ),
    slide(
        'http-stateless-id',
        P('HTTP 무상태성과 사용자 식별', 'HTTP Statelessness and User Identification'),
        P('독립적인 HTTP 요청 사이에서 신원을 유지하는 원리', 'Maintaining identity across independent HTTP requests'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('무상태성 - 서버가 이전 HTTP 요청의 맥락을 자동 보관하지 않는 성질',
                          'Statelessness - servers do not retain context from prior HTTP requests'),
                        P('요청마다 독립적으로 처리되므로 후속 요청의 주체를 식별할 수단 필요',
                          'Each request is independent, requiring an explicit identity mechanism'),
                        P('개인화 화면 · 사용자별 권한 제어 · 감사 기록의 출발점',
                          'Foundation for personalization, access control, and audit logging'),
                    )
                )
            ],
            [
                seq_block(
                    [P('브라우저', 'Browser'), P('서버', 'Server')],
                    [
                        msg(0, 1, P('1. 로그인 요청 (자격 증명)', '1. Login request (credentials)')),
                        msg(1, 1, P('신원 검증 · 식별자 발급', 'Verify identity · issue identifier'), focus=True),
                        msg(1, 0, P('응답과 식별자 전달', 'Return response with identifier'), reply=True),
                        msg(0, 1, P('2. 후속 요청 + 식별자', '2. Next request + identifier')),
                        msg(1, 1, P('식별자로 요청 주체 확인', 'Identify requester from credential'), focus=True),
                    ],
                    P('후속 요청이 이전 로그인과 같은 사용자임을 연결하는 식별 흐름',
                      'Linking subsequent requests back to an authenticated identity'),
                )
            ],
        ],
        sources=[WEEK6_PDF],
    ),
    slide(
        'authn-vs-authz',
        P('인증과 인가의 구분', 'Authentication and Authorization'),
        P('사용자 신원 확인과 자원 접근 권한 판단의 책임 분리', 'Separating identity verification from access permission decisions'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('인증 (AuthN) - 요청 주체가 누구인지 신원을 확인하는 과정',
                          'Authentication (AuthN) - verifying who the requester is'),
                        P('아이디·비밀번호 검증 또는 외부 인증 제공자의 확인 결과 검증',
                          'Verifying credentials or external identity provider assertions'),
                    ),
                    concept(
                        P('인가 (AuthZ) - 확인된 주체에게 작업 권한이 있는지 판단하는 과정',
                          'Authorization (AuthZ) - deciding whether the verified subject may act'),
                        P('로그인 성공 여부와 별개로 요청마다 역할(Role)과 소유권 확인',
                          'Checking role and ownership per request beyond login status'),
                    ),
                )
            ],
            [
                table_block(
                    [P('구분', 'Stage'), P('핵심 질문', 'Core Question'), P('실패 시 응답', 'Failure Status')],
                    [
                        [
                            P('인증 (AuthN)', 'Authentication'),
                            P('요청자가 누구인지 확인', 'Who is making the request'),
                            P('401 Unauthorized', '401 Unauthorized'),
                        ],
                        [
                            P('인가 (AuthZ)', 'Authorization'),
                            P('이 작업을 허용할지 판단', 'Is this action permitted'),
                            P('403 Forbidden', '403 Forbidden'),
                        ],
                    ],
                )
            ],
        ],
        sources=[WEEK6_PDF],
    ),
    slide(
        'cookie-and-session',
        P('쿠키와 서버 세션의 경계', 'Cookies and Server Sessions'),
        P('브라우저 전달 수단과 서버 상태 저장소의 역할 구분', 'Distinguishing browser transport from server-side state'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('쿠키 - 서버가 Set-Cookie로 내리고 브라우저가 자동 전송하는 값',
                          'Cookie - browser-stored value set by Set-Cookie and sent automatically'),
                        P('브라우저가 도메인·경로 조건에 맞는 요청의 Cookie 헤더에 자동 첨부',
                          'Automatically attached to requests matching domain and path scope'),
                    ),
                    concept(
                        P('서버 세션 - 예측 불가능한 세션 ID로 서버 저장소의 상태를 조회하는 방식',
                          'Server session - looking up server state with an unpredictable session ID'),
                        P('실제 신원과 권한은 서버에 보관하며 로그아웃 시 서버 저장소에서 무효화',
                          'Identity and permissions stay on the server and expire on logout'),
                    ),
                )
            ],
            [
                table_block(
                    [P('비교 항목', 'Dimension'), P('쿠키 (전달 수단)', 'Cookie (Transport)'), P('서버 세션 (상태)', 'Server Session (State)')],
                    [
                        [
                            P('저장 위치', 'Storage'),
                            P('클라이언트 (브라우저)', 'Client (Browser)'),
                            P('서버 메모리 · DB · Redis', 'Server memory / DB / Redis'),
                        ],
                        [
                            P('보관 대상', 'Contents'),
                            P('세션 ID 등 전달 식별자', 'Session ID or carrier token'),
                            P('사용자 ID · 역할 · 만료 시각', 'User ID, role, expiry'),
                        ],
                        [
                            P('무효화', 'Revocation'),
                            P('클라이언트 만료 · 덮어쓰기', 'Client expiry or overwrite'),
                            P('서버 삭제 시 즉시 효력 상실', 'Immediate invalidation on server'),
                        ],
                    ],
                )
            ],
        ],
        sources=[WEEK6_PDF, 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'],
    ),
    slide(
        'token-and-oauth',
        P('토큰(JWT)과 소셜 로그인', 'Tokens (JWT) and Social Login'),
        P('서명된 토큰 검증과 OAuth·OIDC 기반 인증 위임', 'Validating signed tokens and delegating identity via OAuth and OIDC'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('JWT - 헤더·페이로드·서명으로 클레임을 전달하는 서명 토큰',
                          'JWT - signed token conveying claims via header, payload, and signature'),
                        P('Base64URL 인코딩은 암호화가 아니므로 민감정보 저장 금지',
                          'Base64URL encoding is not encryption; avoid storing sensitive data'),
                        P('서버에서 서명 · 발급자(iss) · 대상(aud) · 만료(exp) 검증 필수',
                          'Server must validate signature, issuer, audience, and expiration'),
                    )
                )
            ],
            [
                concepts_block(
                    concept(
                        P('OAuth 2.0과 OIDC - 권한 위임 프레임워크와 그 위의 인증 계층',
                          'OAuth 2.0 and OIDC - delegated authorization and identity layer'),
                        P('OAuth 2.0은 자원 접근 권한 위임 · OpenID Connect는 신원 확인용 ID 토큰 제공',
                          'OAuth delegates resource access; OIDC adds ID tokens for identity'),
                        P('access token 보유만으로 임의로 로그인 처리하지 않고 검증 절차 준수',
                          'Follow provider verification rather than trusting raw access tokens alone'),
                    )
                )
            ],
        ],
        sources=[WEEK6_PDF, 'https://openid.net/developers/how-connect-works/'],
    ),
]
