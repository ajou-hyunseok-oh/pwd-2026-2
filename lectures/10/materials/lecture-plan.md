# 10주차 강의 준비안

2026학년도 2학기 · 실전 웹서비스개발 · 10주차  
주제: AI 시대의 웹 서비스 보안 · 3개 챕터(16개 본문 슬라이드) 구성 · 9주차 복습은 별도 덱

## 전체 강의 흐름 (3개 챕터 · 180분 기준)

1. **Chapter 01. 웹 서비스 보안의 현실과 패러다임 전환 (도입, 25분)**: 국내 웹사이트 방치 실태와 AI 공격 자동화 환경을 통해 설계 단계 보안(Security by Design)의 필요성을 체감한다.
2. **Chapter 02. 주요 웹 취약점과 방어 원리 (사례 중심, 65분)**: 실습 프로젝트를 배제하고 실제 침해 사례 및 보안 이슈를 중심으로 공격 원리와 방어 체계를 학습한다. (기존 HTTP·인증·인가·세션·토큰·소셜 로그인 기초는 8주차 학습 범위이므로 제외)
3. **Chapter 03. 실전 적용: 푸드맵 인증·인가 및 보안 설계 (실습, 60분)**: 1~2장의 보안 원리를 현재 푸드맵(React + Express + Supabase)에 적용하기 위한 구체적 설계·구현·검증 작업을 다룬다.
4. **정리 및 질의응답 (30분)**

---

## Chapter 01. 웹 서비스 보안의 현실과 패러다임 전환 (도입)

고려대학교 정보보호대학원 김승주 교수의 방송([한국 웹사이트 50만개 무방비 상태. 한국 보안의 충격적 민낯](https://www.youtube.com/watch?v=DfhLUqZfGTo))을 바탕으로, 학생들이 웹 개발자로서 보안의 중요성을 체감할 수 있도록 구성한 4단계 오프닝 챕터다.

### 연결된 핵심 맥락 (한 문장 요약)
> **국내 50만 개에 달하는 웹사이트가 관리 부재로 방치된 가운데, AI 기반 공격 자동화로 모든 공개 웹이 상시 표적이 되고 있으므로, 외부 보안 솔루션에만 의존하지 않고 개발자가 설계 단계부터 코드 수준의 인증·인가와 보안(Security by Design)을 직접 구현해야 한다.**

### 슬라이드 구성 (01~04)

| 번호 | ID | 슬라이드 타이틀 | 서브타이틀 | 핵심 개념 및 다룰 내용 |
| :---: | :--- | :--- | :--- | :--- |
| **01** | `abandoned-sites` | 방치된 웹사이트와 공격 표면 | 국내 50만 개 웹 서비스의 관리 부재와 최초 침투 경로 | 자산 식별 부재(Shadow IT) · 방치된 서버와 패치 공백 |
| **02** | `ai-attack-automation` | AI 기반 공격 자동화와 상시 위협 | 취약점 탐색 비용 감소로 모든 공개 엔드포인트가 무차별 공격 대상 | AI 스캐너·공격 도구 보편화 · 소규모 서비스까지 상시 표적화 |
| **03** | `solution-limits` | 보안 장비의 한계와 코드 취약점 | 외부 방화벽이 대신 막아주지 못하는 애플리케이션 구현 결함 | 솔루션 만능주의와 체크리스트 보안의 맹점 |
| **04** | `security-by-design` | 설계 단계의 보안과 개발자의 책임 | 기능 구현과 동시에 내재화하는 인증·인가와 비밀정보 보호 | Security by Design 원칙 · 개발자의 기본 설계 책무 |

---

## Chapter 02. 주요 웹 취약점과 방어 원리 (사례 중심)

실습 프로젝트(푸드맵) 예시를 배제하고 실제 국내외 보안 이슈·침해 사례를 기반으로 취약점의 공격 경로와 방어 원리를 다룬다. 공개 공시로 확인된 사실과 수업용 일반 점검 원리를 명확히 구분한다.

### 슬라이드 구성 (05~11) — [사례 근거 문서](case-evidence-sources.md) 기준 검증 완료

| 번호 | ID | 슬라이드 타이틀 | 서브타이틀 | 검증된 보안 이슈 근거 및 방어 원리 |
| :---: | :--- | :--- | :--- | :--- |
| **05** | `broken-object-auth` | 객체 수준 인가 결함과 접근 통제 | 요청 파라미터 변조로 타인의 자원에 접근하는 취약점 방어 | 한국파파존스(2025 개보위 조사 · URL 주문번호 변조) · Optus(2022) / BOLA 방어 |
| **06** | `input-and-sqli` | 입력 검증과 SQL 인젝션 | 사용자 입력이 데이터베이스 명령 구조로 해석되는 경로 차단 | 여기어때(2017 민관합동조사단 · SQLi) · MOVEit(CVE-2023-34362) / 매개변수화 쿼리 |
| **07** | `xss-and-script-control` | XSS와 스크립트 실행 통제 | 외부 입력과 제3자 스크립트가 브라우저에서 실행되는 위험 차단 | TweetDeck XSS 웜(2014) · Optimizely(2026-11 JS 변조) / 이스케이프·정제·CSP |
| **08** | `origin-sop-cors` | 웹 출처 · 동일 출처 정책과 CORS | 브라우저의 교차 출처 접근 경계와 허용 범위 오설정 방어 | 미 국방부(DoD) HackerOne 리포트(임의 Origin 반사 오설정) / SOP · CORS |
| **09** | `csrf-and-cookie-attrs` | CSRF와 쿠키 보호 속성의 한계 | 자동 첨부되는 로그인 쿠키 악용과 서버 측 요청 의도 검증 | Facebook CSRF(2019 · 계정 탈취) · 옥션 관리자 CSRF(2008) / 토큰·Origin·쿠키 속성 |
| **10** | `secrets-and-supply-chain` | 비밀정보 유출과 외부 경계 관리 | 개발자 키 탈취·하드코딩 및 외부 업체·백업 경로 침해 대응 | 티빙(2026-09 과기정통부 · 키 탈취+43개 하드코딩) · KARTE · JPMorgan · 더존비즈온 |
| **11** | `prompt-injection-ai` | AI 시대의 경계: 간접 프롬프트 인젝션 | 외부 입력이 에이전트의 실행 지시로 승격되는 위험 통제 | M365 Copilot EchoLeak(CVE-2025-32711) · Comment and Control 연구 / 최소 권한 · 출력 통제 |

---

## Chapter 03. 실전 적용: 푸드맵 인증·인가 및 보안 설계 (실습)

1~2장에서 학습한 보안 원리를 기존 푸드맵 서비스(React + Express + Supabase)에 적용하기 위해 개발자가 처리해야 할 설계·구현·검증 작업을 다룬다.

### 슬라이드 구성 (12~16)

| 번호 | ID | 슬라이드 타이틀 | 서브타이틀 | 푸드맵에 적용할 처리 작업 |
| :---: | :--- | :--- | :--- | :--- |
| **12** | `foodmap-security-gap` | 현재 푸드맵의 보안 공백 진단 | 인증 없는 API와 브라우저 localStorage 의존 구조 점검 | 7~9주차 구현 범위 점검 및 무인증·localStorage 한계 식별 |
| **13** | `foodmap-role-matrix` | 역할별 권한 매트릭스와 데이터 모델 | 비로그인·일반 사용자·관리자 정책과 사용자 스키마 확장 | 목록·제보·승인 요청 계약 표 · `users`/`submissions` 관계 및 해싱 |
| **14** | `foodmap-auth-cors` | 인증 흐름과 교차 출처(CORS·쿠키) 설정 | 안전한 로그인·세션 전달과 Vercel–Render 간 출처 허용 | 로그인 파이프라인 · `HttpOnly`/`Secure`/`SameSite` · `CLIENT_URL` CORS |
| **15** | `foodmap-server-defenses` | 서버 인가 및 입력·쿼리·출력 방어 구현 | Express 미들웨어 권한 검사와 3대 취약점 코드 수준 방어 | `isAuthenticated`/`requireAdmin` + 입력 검증 + `$1` 쿼리 + React 출력 |
| **16** | `foodmap-secrets-verify` | 비밀정보 격리 · AI 경계 · 보안 검증 | 환경변수 번들 분리와 가상 AI 요약·권한 우회 테스트 계획 | `SERVER_SECRET` vs `VITE_*` 격리 · 가상 AI 읽기 전용 경계 · 하네스 검증 |

---

## 자료 및 내용 검토 기록

- [김승주 교수: 한국 웹사이트 50만개 무방비 상태. 한국 보안의 충격적 민낯](https://www.youtube.com/watch?v=DfhLUqZfGTo): 자산 식별 부재(Shadow IT), AI 기반 공격 자동화로 인한 공격 비용 제로화, 보안 솔루션 만능주의의 한계와 개발 단계 보안(Security by Design)의 필요성 근거.
- [보안프로젝트: 모의해킹 취업을 위한 웹 해킹 학습 로드맵과 실무 가이드](https://youtu.be/F1Co-NqpxH0?si=L3ZikJ5eQBAyO78O): HTTP/HTTPS 프로토콜 선수 이해, 프록시 변조(Burp Suite) 관점에서의 서버 측 검증 필연성, OWASP Top 10 진단 기준 참고.
- [Chapter 03 보안 사고 사례 근거 및 원인 검증](case-evidence-sources.md): 파파존스(개보위 조사), 여기어때(민관합동조사단), MOVEit(CVE-2023-34362), TweetDeck·Optimizely, DoD CORS, Facebook CSRF, 티빙(과기정통부 발표), EchoLeak(CVE-2025-32711)의 실제 원인 매핑 기록.
- [국내외 웹서비스 침해사고 자료](web-security-incidents-2026.md) · [침해 사례별 취약점 분석](incident-vulnerability-analysis.md): 2026년 9~11월 공개 보도·공지 및 AI 보안 연구 출처.
- [8주차 이월 보안 챕터 원본](../../08/materials/security-deferred-review.json): `origin`, `same-origin-policy`, `cors`, `csrf`, `cookie-protection`, `input-validation`, `sql-injection`, `xss`, `secret-management`의 한영 설명·도식·푸드맵 코드 활용.
- [OpenID Foundation: How OpenID Connect Works](https://openid.net/developers/how-connect-works/): OAuth 권한 위임과 OIDC 인증 구분.
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) · [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) · [OWASP LLM Top 10 (2025)](https://genai.owasp.org/llm-top-10/).
