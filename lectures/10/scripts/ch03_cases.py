"""Chapter 03: Web vulnerabilities and defenses grounded in verified real-world security incidents."""
from dsl import (
    P,
    branches_block,
    chapter,
    code_block,
    concept,
    concepts_block,
    evidence_block,
    flow_block,
    msg,
    note_block,
    seq_block,
    slide,
    table_block,
)

SLIDES = [
    chapter(
        'vulnerabilities',
        '주요 웹 취약점과 방어 원리',
        'Web Vulnerabilities and Defense Principles',
    ),
    slide(
        'broken-object-auth',
        P('객체 수준 인가 결함과 접근 통제', 'Broken Access Control and Object-Level Authorization'),
        P('요청 파라미터 변조로 타인의 자원에 접근하는 취약점 방어', 'Defending against parameter tampering to access unauthorized resources'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('객체 수준 인가 결함 (BOLA/IDOR) - 로그인 여부와 무관하게 대상 자원의 소유권을 누락하는 결함',
                          'Broken Object-Level Auth (BOLA/IDOR) - failing to verify resource ownership per request'),
                        P('확정 사례: 한국파파존스(2025 개보위 조사 · URL 주문번호 변조) · 호주 Optus(2022 · 미인증 API ID 순차 변조)',
                          'Verified cases: Papa John’s Korea (2025, URL order-ID tampering) & Optus (2022, API ID enumeration)'),
                        P('프록시 도구로 요청 ID 변조 가능 — UI 버튼 숨김이나 예측 불가 ID에 의존 금지',
                          'Attackers tamper with request IDs via proxies; never rely on hidden UI or unguessable IDs'),
                    )
                ),
                evidence_block(
                    'assets/cases/case-08-papajohns.jpg',
                    P('사례 보도 · 데일리시큐 (2025-06-27)', 'Case Report · DailySecu (2025-06-27)'),
                    P('개인정보위, 한국파파존스 고객정보 유출 조사…파라미터 변조 취약점 ‘경고’ ↗',
                      'PIPC Investigates Papa John’s Korea Breach over URL Parameter Tampering ↗'),
                    'https://www.dailysecu.com/news/articleView.html?idxno=167409',
                    P('주문 조회 URL 번호 변조만으로 비로그인 타인 주문·주소·카드정보 노출 확인',
                      'Tampering with order-page URL digits exposed customer orders and card details without login'),
                ),
            ],
            [
                seq_block(
                    [P('공격자 (프록시)', 'Attacker (Proxy)'), P('API 서버', 'API Server'), P('DB', 'Database')],
                    [
                        msg(0, 1, P('GET /orders/1004 (본인)', 'GET /orders/1004 (own)')),
                        msg(0, 1, P('GET /orders/1005 (ID 변조)', 'GET /orders/1005 (tampered)'), focus=True),
                        msg(1, 1, P('소유권 검증 누락 시 타인 노출', 'Leaks data if ownership unchecked')),
                        msg(1, 2, P('요청자 === 소유자 검증 적용', 'Verify requester === owner'), focus=True),
                        msg(1, 0, P('권한 불일치 → 403 Forbidden', 'Mismatch → 403 Forbidden'), reply=True, focus=True),
                    ],
                    P('파파존스(개보위 조사, 2025)·Optus(2022) 사례 근거: 모든 조회·변경 API에서 서버 소유권 검증 필수',
                      'Grounded in Papa John’s (2025) & Optus (2022): enforce server ownership checks on every endpoint'),
                )
            ],
        ],
        sources=[
            'https://www.dailysecu.com/news/articleView.html?idxno=167409',
            'https://www.bleepingcomputer.com/news/security/optus-hacker-apologizes-and-allegedly-deletes-all-stolen-data/',
            'https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/',
            'lectures/10/materials/case-evidence-sources.md',
        ],
        note='근거: 2025-06 개보위 한국파파존스 현장 조사 보도(URL 파라미터 변조) 및 2022 Optus API IDOR 사고.',
    ),
    slide(
        'input-and-sqli',
        P('입력 검증과 SQL 인젝션', 'Input Validation and SQL Injection'),
        P('사용자 입력이 데이터베이스 명령 구조로 해석되는 경로 차단', 'Preventing user input from altering database query structure'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('입력 검증 - 서버가 수신한 데이터의 형식·자료형·범위를 확인하는 1차 방어',
                          'Input validation - server-side checks on format, type, and permitted range'),
                        P('클라이언트 입력 제한은 우회 가능하므로 서버 측 재검증 필수',
                          'Client-side checks are bypassable; always revalidate on the server'),
                    ),
                    concept(
                        P('SQL 인젝션 - 입력 문자열이 SQL 구문에 섞여 명령 구조 자체를 바꾸는 공격',
                          'SQL injection - input strings concatenated into SQL altering query structure'),
                        P('확정 사례: 여기어때(2017 민관합동조사단 · SQLi로 관리자 세션 탈취) · MOVEit(2023 CVE-2023-34362)',
                          'Verified cases: Yeogi Eottae (2017, SQLi stole admin sessions) & MOVEit (CVE-2023-34362)'),
                        P('문자열 결합 대신 SQL 구조와 값을 분리하는 매개변수화 쿼리 적용',
                          'Use parameterized queries to separate SQL syntax from user values'),
                    ),
                ),
                evidence_block(
                    'assets/cases/case-09-moveit.jpg',
                    P('사례 보도 · SecurityWeek (2023-06-05)', 'Case Report · SecurityWeek (2023-06-05)'),
                    P('Ransomware Group Used MOVEit Exploit to Steal Data From Dozens of Organizations ↗',
                      'Ransomware Group Used MOVEit Exploit to Steal Data From Dozens of Organizations ↗'),
                    'https://www.securityweek.com/ransomware-group-used-moveit-exploit-to-steal-data-from-dozens-of-organizations/',
                    P('MOVEit Transfer SQL 인젝션(CVE-2023-34362) 악용으로 다수 기관 데이터 탈취',
                      'Exploitation of MOVEit Transfer SQL injection (CVE-2023-34362) exfiltrated multi-org data'),
                ),
            ],
            [
                code_block(
                    P('취약한 문자열 결합 vs 안전한 매개변수화 쿼리 (일반 예시)', 'Unsafe concatenation vs. parameterized query (general example)'),
                    "// Vulnerable: user input changes query structure\nconst bad = `SELECT * FROM orders WHERE id = '${orderId}'`;\n\n// Safe: structure fixed, input bound as parameter\nconst result = await client.query(\n  'SELECT id, status FROM orders WHERE id = $1 AND user_id = $2',\n  [orderId, req.userId]\n);",
                    'javascript',
                    72,
                ),
                note_block(P('$1·$2 매개변수는 값 전달 전용 — 테이블명·열명 치환 용도로 사용 불가',
                             'Parameters like $1 and $2 bind values only, never table or column names')),
            ],
        ],
        sources=[
            'https://www.securityweek.com/ransomware-group-used-moveit-exploit-to-steal-data-from-dozens-of-organizations/',
            'https://nvd.nist.gov/vuln/detail/CVE-2023-34362',
            'lectures/10/materials/case-evidence-sources.md',
        ],
        note='근거: 2017 여기어때 침해사고 민관합동조사단 발표(SQL 인젝션) 및 2023 MOVEit CVE-2023-34362 CISA 권고.',
    ),
    slide(
        'xss-and-script-control',
        P('XSS와 스크립트 실행 통제', 'XSS and Script Execution Control'),
        P('외부 입력과 제3자 스크립트가 브라우저에서 실행되는 위험 차단', 'Blocking untrusted inputs and third-party scripts from executing in browsers'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('브라우저 스크립트 위협 - 저장형 XSS와 제3자 스크립트 변조로 브라우저 코드 실행',
                          'Browser script threats - stored XSS and compromised third-party scripts executing in browsers'),
                        P('확정 사례: TweetDeck XSS 웜(2014 · 트윗 입력 필터링 누락) · Optimizely(2026-11 · 프로젝트 JS 변조)',
                          'Verified cases: TweetDeck XSS worm (2014, unfiltered input) & Optimizely (Nov 2026, compromised JS)'),
                        P('일반 텍스트는 출력 문맥 이스케이프 · HTML 허용 시 정제(Sanitize) 필수',
                          'Escape plain text by output context; sanitize any permitted HTML with strict allowlists'),
                        P('CSP(script-src · connect-src)와 스크립트 변경 감시로 실행·외부 전송 통제',
                          'Control execution and exfiltration with CSP (script-src, connect-src) and integrity monitoring'),
                    )
                ),
                evidence_block(
                    'assets/cases/case-10-optimizely.webp',
                    P('사례 보도 · Help Net Security (2026-11-17)', 'Case Report · Help Net Security (2026-11-17)'),
                    P('Malware spread through Optimizely hits 178 organizations, including BBC, CNN and Zoom ↗',
                      'Malware spread through Optimizely hits 178 organizations, including BBC, CNN and Zoom ↗'),
                    'https://www.helpnetsecurity.com/2026/11/17/optimizely-vulnerability-malicious-javascript/',
                    P('고객 계정 사칭으로 프로젝트 JS에 악성 스크립트 삽입 · 178개 사이트 방문자 실행',
                      'Impersonated customer accounts injected malicious Project JavaScript across 178 websites'),
                ),
            ],
            [
                branches_block(
                    P('브라우저로 전달되는 콘텐츠', 'Content delivered to the browser'),
                    P('입력 XSS와 외부 스크립트 공급망 경계를 구분해 통제', 'Control both input XSS and third-party script paths'),
                    [
                        (
                            P('사용자 입력 출력 (이스케이프)', 'User-supplied text (Escaped)'),
                            P('HTML 태그를 문자로 표시\n저장형 XSS 실행 차단', 'Render tags as literal text\nBlock stored XSS execution'),
                        ),
                        (
                            P('HTML · 제3자 스크립트', 'HTML or vendor scripts'),
                            P('허용 목록 정제(Sanitize)\nCSP · 무결성·변경 감시 적용', 'Allowlist sanitization\nApply CSP and integrity monitoring'),
                        ),
                    ],
                    P('허용된 외부 공급자 스크립트 자체가 변조되면 도메인 허용만으로는 부족 — 변경 감시 병행',
                      'If a trusted vendor script is modified, domain allowlists alone fail; monitor changes'),
                )
            ],
        ],
        sources=[
            'https://www.helpnetsecurity.com/2026/11/17/optimizely-vulnerability-malicious-javascript/',
            'https://support.optimizely.com/hc/en-us/articles/50521849710605-Security-Advisory-Web-Experimentation-Security-Incident-Updated-November-19-2026',
            'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP',
            'lectures/10/materials/case-evidence-sources.md',
        ],
        note='TweetDeck(입력 필터링 누락 XSS)과 Optimizely(가입 흐름 결함으로 프로젝트 JS 변조)의 원인을 구분해 설명.',
    ),
    slide(
        'origin-sop-cors',
        P('웹 출처 · 동일 출처 정책과 CORS', 'Web Origins, Same-Origin Policy, and CORS'),
        P('브라우저의 교차 출처 접근 경계와 허용 범위 오설정 방어', 'Browser cross-origin boundaries and preventing CORS misconfiguration'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('출처 (Origin)와 동일 출처 정책 (SOP) - 프로토콜·호스트·포트가 다르면 응답 읽기를 막는 원칙',
                          'Origin & Same-Origin Policy (SOP) - blocking scripts from reading cross-origin responses'),
                        P('요청의 서버 도달 여부와 브라우저 스크립트의 응답 읽기 가능 여부는 별개 판단',
                          'Whether a request reaches the server and whether scripts can read its response are separate checks'),
                    ),
                    concept(
                        P('CORS 오설정 - 임의 Origin 반사나 과도한 허용으로 민감 API 응답이 노출되는 결함',
                          'CORS misconfiguration - unvalidated Origin reflection exposing sensitive responses'),
                        P('확정 사례: StackStorm(2019 CVE-2019-9580 · null Origin CORS 우회) · 미 국방부(DoD) HackerOne 리포트',
                          'Verified cases: StackStorm (CVE-2019-9580, null Origin bypass) & U.S. DoD HackerOne report'),
                        P('CORS는 브라우저 접근 규칙일 뿐 서버 API의 인증·인가를 대신하지 않음',
                          'CORS is a browser policy and never replaces server API authentication or authorization'),
                    ),
                ),
                evidence_block(
                    'assets/cases/case-11-stackstorm.jpg',
                    P('사례 보도 · The Hacker News (2019-03)', 'Case Report · The Hacker News (Mar 2019)'),
                    P('Severe Flaw Disclosed In StackStorm DevOps Automation Software ↗',
                      'Severe Flaw Disclosed In StackStorm DevOps Automation Software ↗'),
                    'https://thehackernews.com/2019/03/stackstorm-security-vulnerability.html',
                    P('CVE-2019-9580: null Origin 허용으로 CORS 보호 우회 및 교차 출처 API 요청 노출',
                      'CVE-2019-9580: trusting null Origin bypassed CORS checks in StackStorm Web UI'),
                ),
            ],
            [
                seq_block(
                    [P('브라우저 (app)', 'Browser (app)'), P('API 서버 (api)', 'API Server (api)')],
                    [
                        msg(0, 1, P('Origin: https://app.example.com', 'Origin: https://app.example.com')),
                        msg(1, 0, P('Access-Control-Allow-Origin:\nhttps://app.example.com', 'Access-Control-Allow-Origin:\nhttps://app.example.com'), reply=True, focus=True),
                        msg(0, 0, P('허용 조건 확인 후 응답 읽기 허용', 'Browser checks header and allows read'), focus=True),
                    ],
                    P('출처 = 프로토콜 + 호스트 + 포트 · 자격정보 포함 요청은 명시적 출처 화이트리스트 필수',
                      'Origin = scheme + host + port; credentialed requests require explicit allowlists'),
                ),
                table_block(
                    [P('비교 대상', 'Target'), P('기준: https://app.example.com', 'Base: https://app.example.com'), P('출처 판정', 'Origin')],
                    [
                        [P('경로 변경', 'Path'), P('https://app.example.com/list', 'https://app.example.com/list'), P('같음', 'Same')],
                        [P('호스트 변경', 'Host'), P('https://api.example.com', 'https://api.example.com'), P('다름 (CORS)', 'Different')],
                        [P('프로토콜 변경', 'Scheme'), P('http://app.example.com', 'http://app.example.com'), P('다름', 'Different')],
                    ],
                ),
            ],
        ],
        sources=[
            'https://thehackernews.com/2019/03/stackstorm-security-vulnerability.html',
            'https://nvd.nist.gov/vuln/detail/CVE-2019-9580',
            'https://hackerone.com/reports/733017',
            'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS',
            'lectures/10/materials/case-evidence-sources.md',
        ],
    ),
    slide(
        'csrf-and-cookie-attrs',
        P('CSRF와 쿠키 보호 속성의 한계', 'CSRF and Limits of Cookie Security Attributes'),
        P('자동 첨부되는 로그인 쿠키 악용과 서버 측 요청 의도 검증', 'Preventing forged cross-site requests and setting cookie boundaries'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('크로스 사이트 요청 위조 (CSRF) - 다른 사이트가 로그인 브라우저로 의도치 않은 요청을 보내는 공격',
                          'CSRF - external site triggering unintended requests via an authenticated browser'),
                        P('확정 사례: Facebook CSRF 버그바운티(2019 · 계정 탈취 가능) · 옥션 관리자 세션 악용(2008)',
                          'Verified cases: Facebook CSRF bounty (2019, account takeover) & Auction admin CSRF (2008)'),
                        P('상태 변경 요청에 요청 출처(Origin) 및 공격자가 알 수 없는 CSRF 토큰 검증',
                          'Validate request origin and unpredictable CSRF tokens on state changes'),
                    ),
                    concept(
                        P('쿠키 보호 속성 - Secure · HttpOnly · SameSite의 방어 범위와 한계',
                          'Cookie attributes - scope and limits of Secure, HttpOnly, and SameSite'),
                        P('HttpOnly는 스크립트 쿠키 읽기를 막으나 XSS를 통한 요청 전송까지 막지는 못함',
                          'HttpOnly blocks script reads of cookies but cannot prevent XSS-driven requests'),
                    ),
                ),
                evidence_block(
                    'assets/cases/case-12-fb-csrf.jpg',
                    P('사례 보도 · SecurityWeek (2019-02-15)', 'Case Report · SecurityWeek (2019-02-15)'),
                    P('CSRF Vulnerability in Facebook Earns Researcher $25,000 ↗',
                      'CSRF Vulnerability in Facebook Earns Researcher $25,000 ↗'),
                    'https://www.securityweek.com/csrf-vulnerability-facebook-earns-researcher-25000',
                    P('엔드포인트 CSRF 검증 우회로 피해자 링크 열람 시 계정 설정 변경·탈취 가능',
                      'CSRF validation bypass allowed unauthorized account changes when opening a crafted link'),
                ),
            ],
            [
                seq_block(
                    [P('다른 사이트', 'Other Site'), P('로그인 브라우저', 'Signed-in Browser'), P('서버', 'Server')],
                    [
                        msg(0, 1, P('의도와 다른 요청 유발', 'Trigger unintended request')),
                        msg(1, 2, P('상태 변경 요청 + 쿠키 자동 첨부', 'State-changing request + auto-sent cookie')),
                        msg(2, 2, P('CSRF 토큰 · 출처 검증\n실패 시 변경 거부', 'Verify CSRF token & origin\nReject on failure'), focus=True),
                    ],
                    P('쿠키 보호 속성 설정과 함께 서버에서 상태 변경 요청의 정당성 확인',
                      'Validate state-changing requests on the server alongside cookie flags'),
                ),
                table_block(
                    [P('쿠키 속성', 'Attribute'), P('보호 범위', 'Protection'), P('주의할 한계', 'Limit')],
                    [
                        [P('Secure', 'Secure'), P('HTTPS에서만 전송', 'HTTPS only'), P('전송만 보호', 'Transport only')],
                        [P('HttpOnly', 'HttpOnly'), P('JS 읽기 차단', 'Block JS read'), P('XSS 요청 허용', 'XSS requests pass')],
                        [P('SameSite=Lax', 'SameSite=Lax'), P('교차 POST 제한', 'Limit cross-site POST'), P('동일 사이트 허용', 'Same-site allowed')],
                    ],
                ),
            ],
        ],
        sources=[
            'https://www.securityweek.com/csrf-vulnerability-facebook-earns-researcher-25000',
            'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html',
            'lectures/10/materials/case-evidence-sources.md',
        ],
    ),
    slide(
        'secrets-and-supply-chain',
        P('비밀정보 유출과 외부 경계 관리', 'Secret Exposure and External Boundary Management'),
        P('개발자 키 탈취·하드코딩 및 외부 업체·백업 경로 침해 대응', 'Defending against key theft, hardcoding, vendor breaches, and backup leaks'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('비밀정보 유출 - 접속키 탈취와 소스코드 평문 하드코딩으로 서비스 전체가 노출되는 위험',
                          'Secret exposure - key theft and hardcoded secrets exposing entire environments'),
                        P('확정 사례: 티빙(2026-09 과기정통부 발표 · 개발자 접속키 탈취 + 소스코드 운영키 43개 하드코딩)',
                          'Verified case: TVING (Sep 2026 MSIT report — dev key theft & 43 hardcoded prod keys in source)'),
                        P('확정 사례: PLAID KARTE(2026-11 공시 · 서버 취약점 통한 DB 연결 자격증명 탈취)',
                          'Verified case: PLAID KARTE (Nov 2026 disclosure — DB credentials stolen via server flaw)'),
                    )
                ),
                evidence_block(
                    'assets/cases/case-13-tving-etnews.png',
                    P('사례 보도 · 전자신문 (2026-09-03)', 'Case Report · ETNews (2026-09-03)'),
                    P('티빙 해킹, 접속키 하나에서 시작됐다…드러난 보안 허점 ↗',
                      'TVING Breach Began with a Single Stolen Access Key ↗'),
                    'https://www.etnews.com/20260903000283',
                    P('개발환경 접속키 탈취 후 소스코드 하드코딩 운영키 43개 악용 · 3,954만 계정 유출',
                      'Stolen dev key uncovered 43 hardcoded prod keys in source, exposing 39.54M accounts'),
                ),
            ],
            [
                concepts_block(
                    concept(
                        P('외부 경계 확장 - 위탁 업체와 백업 솔루션까지 포함된 공격 표면',
                          'Expanded boundary - third-party vendors and backup tools are attack surfaces'),
                        P('확정 사례: JPMorgan·Visa·Mastercard 위탁사 침해(2026-11) · 더존비즈온 백업 침해(2026-10)',
                          'Verified cases: JPMorgan/Visa/Mastercard vendor breach (Nov 2026) & Douzone backup breach (Oct 2026)'),
                    )
                ),
                table_block(
                    [P('경계 영역', 'Boundary'), P('핵심 방어 조치', 'Core Defense')],
                    [
                        [P('개발자 키 · 소스코드', 'Dev Keys & Source'), P('하드코딩 금지 · 환경별 분리 · 단기 키 및 즉시 폐기', 'No hardcoding, env isolation, short-lived keys & rotation')],
                        [P('외부 위탁사 · SaaS', 'Vendors & SaaS'), P('제공 데이터 최소화 · 계약 종료 시 토큰 회수', 'Data minimization, immediate token revocation')],
                        [P('백업 · 관리 도구', 'Backups & Admin'), P('네트워크 격리 · 관리자 MFA · 암호화 키 분리', 'Network isolation, MFA, separate encryption keys')],
                    ],
                ),
            ],
        ],
        sources=[
            'https://www.etnews.com/20260903000283',
            'https://m.korea.kr/briefing/pressReleaseView.do?gubun=pressRelease&newsId=156780136&pageIndex=3&repCode=',
            'https://tdnet-pdf.kabutan.jp/20261116/140120261116581662.pdf',
            'https://apnews.com/article/8470d475450721b66858bdace47091c0',
            'https://www.douzone.com/board/read.jsp?code=notice&id=3508',
            'lectures/10/materials/case-evidence-sources.md',
        ],
    ),
    slide(
        'prompt-injection-ai',
        P('AI 시대의 경계: 간접 프롬프트 인젝션', 'AI-Era Boundary: Indirect Prompt Injection'),
        P('외부 입력이 에이전트의 실행 지시로 승격되는 위험 통제', 'Controlling the boundary where untrusted data turns into agent instructions'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('간접 프롬프트 인젝션 - 외부 이메일·문서·댓글의 숨은 지시가 AI 행동을 바꾸는 취약점',
                          'Indirect prompt injection - hidden instructions in external text redirecting AI agents'),
                        P('확정 사례: Microsoft 365 Copilot EchoLeak(2025 CVE-2025-32711 · 이메일 기반 제로클릭 유출)',
                          'Verified case: M365 Copilot EchoLeak (CVE-2025-32711, zero-click email exfiltration patched)'),
                        P('연구 시연: Comment and Control(2026-04 · PR/이슈 통한 자격증명 노출) · Slack AI 주입 연구',
                          'Research demos: Comment & Control (Apr 2026) & Slack AI channel injection studies'),
                    )
                ),
                evidence_block(
                    'assets/cases/case-14-echoleak.jpg',
                    P('사례 보도 · BleepingComputer (2025-06-11)', 'Case Report · BleepingComputer (2025-06-11)'),
                    P('Zero-click AI data leak flaw uncovered in Microsoft 365 Copilot ↗',
                      'Zero-click AI data leak flaw uncovered in Microsoft 365 Copilot ↗'),
                    'https://www.bleepingcomputer.com/news/security/zero-click-ai-data-leak-flaw-uncovered-in-microsoft-365-copilot/',
                    P('외부 이메일 속 숨은 지시로 EchoLeak(CVE-2025-32711) 발생 · M365 내부 데이터 유출',
                      'Hidden email prompts triggered CVE-2025-32711 (EchoLeak) zero-click M365 data exfiltration'),
                ),
            ],
            [
                flow_block(
                    [
                        (P('비신뢰 입력 격리', 'Isolate Untrusted Input'), P('외부 이메일 · 댓글 · 문서를\n작업 지시와 명확히 분리', 'Separate external text\nfrom system instructions')),
                        (P('에이전트 최소 권한', 'Agent Least Privilege'), P('읽기·승인·실행 권한 분리\n모델 밖에서 정책·승인 검사', 'Split read and write tools\nEnforce checks outside model')),
                        (P('AI 출력·전송 통제', 'Output & Egress Control'), P('생성 HTML · SQL 직접 실행 금지\n외부 URL 요청·도구 호출 제한', 'Never run raw AI HTML/SQL\nRestrict egress and tool calls')),
                    ],
                    P('OWASP LLM Top 10 (2025) 및 EchoLeak 대응 원칙(입력 격리·출력 외부 전송 차단) 반영',
                      'Aligned with OWASP LLM Top 10 (2025) and EchoLeak mitigations'),
                )
            ],
        ],
        sources=[
            'https://www.bleepingcomputer.com/news/security/zero-click-ai-data-leak-flaw-uncovered-in-microsoft-365-copilot/',
            'https://nvd.nist.gov/vuln/detail/CVE-2025-32711',
            'https://oddguan.com/blog/comment-and-control/',
            'https://genai.owasp.org/llm-top-10/',
            'lectures/10/materials/case-evidence-sources.md',
        ],
        note='실제 패치된 취약점(EchoLeak CVE-2025-32711)과 통제된 연구 시연(Comment and Control)을 구분.',
    ),
]
