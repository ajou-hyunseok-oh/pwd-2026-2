"""Chapter 01: Security reality and Security by Design (Introduction)."""
from dsl import P, chapter, concept, concepts_block, flow_block, note_block, slide, table_block

VIDEO_SRC = 'https://www.youtube.com/watch?v=DfhLUqZfGTo'

SLIDES = [
    chapter(
        'reality',
        '웹 서비스 보안의 현실과 패러다임 전환',
        'Web Security Reality and Paradigm Shift',
    ),
    slide(
        'abandoned-sites',
        P('방치된 웹사이트와 공격 표면', 'Abandoned Websites and Attack Surface'),
        P('국내 50만 개 웹 서비스의 관리 부재와 최초 침투 경로', 'Unmanaged Korean web services and initial entry points'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('공격 표면 - 외부에 노출되어 공격자가 접근할 수 있는 모든 경로',
                          'Attack surface - every exposed path an attacker can reach'),
                        P('관리 주체와 보안 업데이트가 끊긴 웹사이트 약 50만 개 방치',
                          'Roughly 500,000 websites left without active owners or patches'),
                        P('공식 자산 목록에서 누락된 Shadow IT가 최초 침투 경로로 악용',
                          'Shadow IT omitted from inventories serves as an initial entry point'),
                    )
                )
            ],
            [
                table_block(
                    [P('방치 자산 유형', 'Abandoned Asset'), P('발생 배경', 'Cause'), P('보안 위험', 'Risk')],
                    [
                        [
                            P('테스트·임시 서버', 'Test / Staging Server'),
                            P('개발 종료 후 미회수', 'Left running after testing'),
                            P('초기 계정 · 디버그 정보 노출', 'Default credentials and debug leaks'),
                        ],
                        [
                            P('방치된 서브도메인', 'Forgotten Subdomain'),
                            P('행사·과제 종료 후 방치', 'Unused after event or project'),
                            P('미패치 프레임워크 · 구형 API', 'Unpatched frameworks and legacy APIs'),
                        ],
                        [
                            P('관리·연동 도구', 'Admin / Integration Tool'),
                            P('자산 전수조사 누락', 'Missing from asset inventory'),
                            P('외부 직접 접속 및 내부 진입', 'Direct external exposure and lateral movement'),
                        ],
                    ],
                ),
            ],
        ],
        sources=[VIDEO_SRC],
        note='김승주 교수(고려대 정보보호대학원) 방송 핵심: 관리되지 않는 웹 자산의 규모와 위험.',
    ),
    slide(
        'ai-attack-automation',
        P('AI 기반 공격 자동화와 상시 위협', 'AI-Driven Attack Automation and Constant Threats'),
        P('취약점 탐색 비용 감소로 모든 공개 엔드포인트가 무차별 공격 대상', 'Lower discovery cost turns every public endpoint into a constant target'),
        'visual',
        [
            [
                concepts_block(
                    concept(
                        P('공격 자동화 - AI와 봇이 취약점 탐색과 침투를 자동 수행하는 환경',
                          'Attack automation - AI and bots automating discovery and exploitation'),
                        P('생성형 AI 보편화로 정찰 · 취약점 분석 · 공격 코드 생성 비용 급감',
                          'Generative AI lowers the cost of recon, triage, and exploit development'),
                        P('주요 기업뿐 아니라 소규모 웹 프로젝트까지 인터넷 전체 상시 스캔 대상',
                          'Both large enterprises and small web projects face continuous scanning'),
                    )
                )
            ],
            [
                flow_block(
                    [
                        (P('자동 정찰', 'Automated Recon'), P('공개 도메인 · API 경로 상시 수집', 'Continuous scan of domains and APIs')),
                        (P('취약점 판별', 'Flaw Detection'), P('AI 기반 설정 오류 · 알려진 결함 식별', 'AI-assisted triage of misconfigs and flaws')),
                        (P('무차별 시도', 'Mass Probing'), P('자동 생성 페이로드로 즉각 침투 시도', 'Immediate probing with generated payloads')),
                    ],
                    P('공격 대상의 규모와 무관하게 공개 즉시 자동화 도구의 탐색 범위 포함',
                      'Any newly exposed service enters automated scanning regardless of scale'),
                )
            ],
        ],
        sources=[VIDEO_SRC],
    ),
    slide(
        'solution-limits',
        P('보안 장비의 한계와 코드 취약점', 'Limits of Security Appliances and Code Flaws'),
        P('외부 방화벽이 대신 막아주지 못하는 애플리케이션 구현 결함', 'Application flaws that perimeter firewalls cannot block'),
        'split',
        [
            [
                concepts_block(
                    concept(
                        P('형식적 보안 - 인증 획득과 외부 장비 도입에만 의존하는 운영 방식',
                          'Checklist security - relying solely on compliance and perimeter tools'),
                        P('방화벽 · 백신 · 망분리 설치만으로 웹 애플리케이션 내부 결함 차단 불가',
                          'Firewalls, antivirus, and network isolation cannot fix flawed app logic'),
                        P('정상 HTTP 요청 경로를 통해 전달되는 인증 우회 · 권한 결함이 주요 침투 원인',
                          'Auth bypass and broken authorization arrive over valid HTTP traffic'),
                    )
                )
            ],
            [
                table_block(
                    [P('영역', 'Layer'), P('방어 대상', 'Protection Scope'), P('보안 한계', 'Blind Spot')],
                    [
                        [
                            P('네트워크 방화벽 · WAF', 'Firewall / WAF'),
                            P('비정상 포트 차단 · 알려진 패턴 탐지', 'Blocked ports and known attack signatures'),
                            P('요청자 권한 검증 누락 판별 불가', 'Cannot verify business-level user permissions'),
                        ],
                        [
                            P('애플리케이션 코드', 'Application Code'),
                            P('신원 확인 · 객체 소유권 검사 · 입력 처리', 'Identity checks, object ownership, input handling'),
                            P('설계 결함 시 정상 경로를 통한 정보 유출', 'Design flaws leak data through normal endpoints'),
                        ],
                    ],
                )
            ],
        ],
        sources=[VIDEO_SRC],
    ),
    slide(
        'security-by-design',
        P('설계 단계의 보안과 개발자의 책임', 'Security by Design and Developer Responsibility'),
        P('기능 구현과 동시에 내재화하는 인증·인가와 비밀정보 보호', 'Embedding authentication, authorization, and secret protection from day one'),
        'single',
        [
            [
                concepts_block(
                    concept(
                        P('설계 단계 보안 - 기능 완성 후 보완하지 않고 초기 설계부터 보안을 내재화하는 원칙',
                          'Security by Design - embedding security into initial architecture, not post-release'),
                        P('보안은 별도 팀의 사후 점검이 아닌 웹 서비스 개발자의 핵심 설계 책무',
                          'Security is a core developer design responsibility, not an afterthought'),
                        P('클라이언트 화면 제어와 별개로 서버 측 인증 · 인가 · 입력 처리 · 키 격리를 기본 구조로 설계',
                          'Build server auth, access checks, input handling, and key isolation independently of the UI'),
                    )
                ),
                flow_block(
                    [
                        (P('인증과 상태', 'Auth & State'), P('신원 확인과 세션·토큰 유지', 'Verify identity and manage sessions')),
                        (P('서버 인가 검증', 'Server AuthZ'), P('요청마다 역할·소유권 검증', 'Check role and ownership per request')),
                        (P('입력·출력 분리', 'Input / Output'), P('명령·코드 해석 경로 차단', 'Block query and script injection')),
                        (P('비밀정보 격리', 'Secret Isolation'), P('키 노출 방지와 환경 분리', 'Keep keys out of code and clients')),
                    ],
                    P('웹 서비스 개발 전 과정에 내재화해야 하는 4대 핵심 설계 축',
                      'Four foundational design pillars across web service development'),
                ),
            ]
        ],
        sources=[VIDEO_SRC],
    ),
]
